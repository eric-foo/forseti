"""Weekly demand read over committed reddit_subreddit_grid top/week packets.

Evidence-layer reader (weekly demand radar spec, section E): discovers this
week's ``top/?t=week`` grid packets for the lake-registry roster, ranks
problem candidates by discussion density and evidence volume, and emits one
JSON document. Pure read -- no lake writes, no network, no analysis persisted.

Owner contract:
- forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_weekly_demand_radar_spec_v0.md
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path
from typing import Any, Sequence
from urllib.parse import urlparse

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.reddit_subreddit_grid.materializer import (
    RegistryRefreshError,
    read_grid_packet,
)
from data_lake.reddit_subreddit_registry import known_subreddits
from data_lake.root import DataLakeRoot
from runners._scaffold import exit_on_failure

GRID_SOURCE_FAMILY = "reddit_subreddit_grid"
# Candidate gate parameters, dogfooded 2026-07-22 (5-sub cycle, one brief):
# density separates unmet-need threads from broadcast virality; the smoothing
# constant damps the ratio where score is too small to trust; the comment
# floor drops threads with nothing to mine.
DEFAULT_DENSITY_FLOOR = 0.7
DEFAULT_MIN_COMMENTS = 15
DEFAULT_SMOOTH_K = 10
# Page-1 score floor above which a subreddit genuinely overflows one page
# (top-10 carries 65% of weekly score on the measured distribution; a floor
# past 50 means real traction ran off the page and the next pass should
# capture page 2 for that subreddit).
PAGE_OVERFLOW_SCORE_FLOOR = 50


def _int_or_none(value: str | None) -> int | None:
    if value is None:
        return None
    digits = value.replace(",", "").strip()
    if digits.lstrip("-").isdigit():
        return int(digits)
    return None


def _is_top_week(listing_url: str) -> bool:
    parsed = urlparse(listing_url)
    parts = [part for part in parsed.path.split("/") if part]
    return bool(parts) and parts[-1] == "top" and "t=week" in (parsed.query or "").split("&")


def run_weekly_demand_read(
    *,
    data_root: DataLakeRoot,
    as_of: _dt.date,
    density_floor: float = DEFAULT_DENSITY_FLOOR,
    min_comments: int = DEFAULT_MIN_COMMENTS,
    smooth_k: int = DEFAULT_SMOOTH_K,
) -> dict[str, Any]:
    window_start = as_of - _dt.timedelta(days=6)
    roster = known_subreddits(data_root)

    # Newest qualifying packet per subreddit; a re-run within the week
    # supersedes rather than double-counts.
    per_sub: dict[str, Any] = {}
    unreadable: list[dict[str, str]] = []
    for packet_id in data_root.list_available(source_family=GRID_SOURCE_FAMILY):
        container = data_root.find_packet(packet_id)
        if container is None:
            continue
        try:
            read = read_grid_packet(packet_or_manifest_path=container)
        except RegistryRefreshError as exc:
            unreadable.append({"packet_id": packet_id, "error": f"[{exc.code}] {exc.message}"})
            continue
        if not _is_top_week(read.grid_view.listing_url):
            continue
        observed = _dt.date.fromisoformat(read.observed_at)
        if not window_start <= observed <= as_of:
            continue
        key = read.subreddit
        if key not in roster:
            continue
        current = per_sub.get(key)
        if current is None or (read.observed_at, packet_id) > (current[0].observed_at, current[1]):
            per_sub[key] = (read, packet_id)

    sub_health: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    floor_tripwire: list[str] = []
    for name in sorted(per_sub):
        read, packet_id = per_sub[name]
        rows = [
            row
            for row in read.grid_view.thread_rows
            if not row.stickied and not row.promoted
        ]
        scored = [
            (row, _int_or_none(row.visible_score_or_none), _int_or_none(row.visible_comment_count_or_none))
            for row in rows
        ]
        usable = [(row, score, comments) for row, score, comments in scored
                  if score is not None and comments is not None]
        total_score = sum(score for _, score, _ in usable)
        total_comments = sum(comments for _, _, comments in usable)
        score_floor = min((score for _, score, _ in usable), default=None)
        if score_floor is not None and score_floor > PAGE_OVERFLOW_SCORE_FLOOR:
            floor_tripwire.append(name)
        sub_health.append(
            {
                "subreddit": name,
                "packet_id": packet_id,
                "observed_at": read.observed_at,
                "created_utc_or_none": read.grid_view.created_utc_or_none,
                "posts": len(usable),
                "rows_dropped_unparsed": len(scored) - len(usable),
                "weekly_score": total_score,
                "weekly_comments": total_comments,
                "page1_score_floor": score_floor,
            }
        )
        for row, score, comments in usable:
            density = comments / (max(score, 0) + smooth_k)
            if density >= density_floor and comments >= min_comments:
                candidates.append(
                    {
                        "subreddit": name,
                        "thread_url": row.thread_url,
                        "title_or_none": row.visible_title_or_none,
                        "flair_or_none": row.flair_or_none,
                        "timestamp_utc_ms_or_none": row.timestamp_utc_ms_or_none,
                        "score": score,
                        "comments": comments,
                        "density": round(density, 3),
                    }
                )

    candidates.sort(key=lambda item: (-item["comments"], item["thread_url"]))
    return {
        "reader": "reddit_weekly_demand_read",
        "as_of": as_of.isoformat(),
        "window_start": window_start.isoformat(),
        "gate": {
            "density_floor": density_floor,
            "min_comments": min_comments,
            "smooth_k": smooth_k,
            "page_overflow_score_floor": PAGE_OVERFLOW_SCORE_FLOOR,
        },
        "roster_count": len(roster),
        "subs_read": len(per_sub),
        "subs_missing_weekly_packet": sorted(set(roster) - set(per_sub)),
        "unreadable_packets": unreadable,
        "sub_health": sub_health,
        "candidates_found": len(candidates),
        "candidates": candidates,
        "page_overflow_tripwire": floor_tripwire,
        "non_claims": [
            "not metric authority",
            "not demand proof or venue scoring",
            "not a lake write (recompute from packets at will)",
        ],
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Read this week's top/?t=week reddit_subreddit_grid packets for the "
            "registry roster and emit ranked problem candidates as JSON."
        )
    )
    parser.add_argument("--data-root", default=None, help="Lake root (defaults to resolution).")
    parser.add_argument("--as-of", default=None, help="ISO date closing the 7-day window; defaults to today (UTC).")
    parser.add_argument("--density-floor", type=float, default=DEFAULT_DENSITY_FLOOR)
    parser.add_argument("--min-comments", type=int, default=DEFAULT_MIN_COMMENTS)
    parser.add_argument("--smooth-k", type=int, default=DEFAULT_SMOOTH_K)
    parser.add_argument("--output", type=Path, default=None, help="Also write the JSON document here.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    with exit_on_failure(parser, runner_name="reddit weekly demand read"):
        if args.data_root is not None:
            data_root = DataLakeRoot.resolve_readonly(explicit=args.data_root)
        else:
            data_root = DataLakeRoot.resolve_readonly()
        as_of = (
            _dt.date.fromisoformat(args.as_of)
            if args.as_of
            else _dt.datetime.now(_dt.timezone.utc).date()
        )
        payload = run_weekly_demand_read(
            data_root=data_root,
            as_of=as_of,
            density_floor=args.density_floor,
            min_comments=args.min_comments,
            smooth_k=args.smooth_k,
        )
        text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)
        if args.output is not None:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text + "\n", encoding="utf-8")
        print(text)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
