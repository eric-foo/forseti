"""Bounded Reddit subreddit grid capture (radar lane, public dual-track route).

Captures ONE old Reddit listing page per named subreddit (the grid: the page
carries both the thread grid and the venue titlebox envelope) as a Source
Capture Packet with ``source_family="reddit_subreddit_grid"``, either into a
local output root or committed into the data lake (``--data-root``).

Owner contracts:
- forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_radar_grid_capture_maintenance_design_v0.md
- forseti/product/spines/capture/core/source_families/social_media/reddit/README.md (radar cadence + dual-track posture)

This runner performs one GET per subreddit per invocation with the shared
politeness cadence. It does not follow links, expand comments, capture
users/profiles, schedule itself, or claim ToS sufficiency; each run records
its source-policy posture receipt in the packet limitations.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness_utils import utc_now_z_microseconds
from runners._scaffold import exit_on_failure
from capture_spine.reddit_subreddit_grid.grid_projection import (
    GRID_PROJECTION_PARSER_VERSION,
    build_grid_content_record,
)
from runners.run_source_capture_http_packet import run_source_capture_http_packet
from source_capture import CaptureModeCategory
from source_capture.cadence import CadenceMode, build_cadence_plan
from source_capture.content_extraction import (
    CAPTURE_RETENTION_MODES,
    CONTENT_EXTRACTION_FAILED_EXIT_CODE,
    ContentExtractionSpec,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot

GRID_SOURCE_FAMILY = "reddit_subreddit_grid"
GRID_SOURCE_SURFACE = "old_reddit_direct_http"
ALLOWED_LISTINGS = ("hot", "new", "top", "rising")
ALLOWED_TIME_WINDOWS = ("hour", "day", "week", "month", "year", "all")
DEFAULT_MAX_SUBREDDITS = 10
DEFAULT_DELAY_SECONDS = 30.0
DEFAULT_TIMEOUT_SECONDS = 20.0
DEFAULT_MAX_BYTES = 5_000_000
# Content-mode is the standard fleet posture (storage-and-retention doctrine,
# 2026-07-17): derived record preserved, raw hashed then discarded. Raw and
# Raw remains the explicit operator-selected evidence posture.
DEFAULT_RETENTION_MODE = "content"

# The receipt carries its own escalation logic on purpose. A re-check that
# compares an observation against a prior DESCRIPTION escalates on any wording or
# scope drift; one that compares against the DECISION PREDICATE escalates only
# when the decision could actually change. The 2026-07-22 re-check halted an
# authorized pass on a same-direction change because the older receipt read as a
# scope claim -- hence the split below.
SOURCE_POLICY_PREDICATE = (
    "the old-Reddit subreddit listing surface this runner captures is robots-disallowed "
    "for us, and the owner accepted capturing it anyway as a bounded single-page pass "
    "under the measured-risk dual-track posture (Reddit lane README, 2026-07-16)"
)
SOURCE_POLICY_PREDICATE_STATUS = "TRUE as of 2026-07-22 re-check"
SOURCE_POLICY_ESCALATE_IF = (
    "HALT and return to the owner only if: the captured surface becomes ALLOWED (the "
    "measured-risk posture is then moot and must be re-derived, not silently kept); a "
    "hard access gate appears (403, CAPTCHA, legal notice, account action); the accepted "
    "bound is exceeded (more than one listing page per subreddit per pass, or cadence "
    "beyond the accepted radar rate); or capture becomes commercial-grade, which the "
    "dual-track posture routes to the sanctioned API path"
)
SOURCE_POLICY_DO_NOT_HALT_ON = (
    "do NOT halt on a same-direction change: a broader disallow, a reworded or reshaped "
    "directive list, or a differently-served variant. The predicate is unchanged, so the "
    "authorization stands. Record it, and surface it for the next posture review"
)
SOURCE_POLICY_OBSERVED = (
    "observed 2026-07-22: 'User-agent: * / Disallow: /' on www and old.reddit, "
    "user-agent-independent across three probes and byte-identical to an independent "
    "archive crawl of 2026-04-14; a variant allowing only '/$' is served interchangeably "
    "and likewise disallows listings. The granular per-surface file described by the "
    "2026-06-08 record was last served in 2025"
)
SOURCE_POLICY_POSTURE_RECEIPT = (
    f"source-policy posture predicate: {SOURCE_POLICY_PREDICATE} [{SOURCE_POLICY_PREDICATE_STATUS}]. "
    f"{SOURCE_POLICY_ESCALATE_IF}. {SOURCE_POLICY_DO_NOT_HALT_ON}. {SOURCE_POLICY_OBSERVED}. "
    "Not ToS sufficiency, not legal advice"
)


def build_grid_listing_url(*, subreddit: str, listing: str, time_window: str | None) -> str:
    name = _validate_subreddit(subreddit)
    if listing not in ALLOWED_LISTINGS:
        raise ValueError(f"listing must be one of {ALLOWED_LISTINGS}, got {listing!r}")
    url = f"https://old.reddit.com/r/{name}/{listing}/"
    if listing == "top":
        window = time_window or "day"
        if window not in ALLOWED_TIME_WINDOWS:
            raise ValueError(f"time window must be one of {ALLOWED_TIME_WINDOWS}, got {window!r}")
        url += f"?t={window}"
    elif time_window is not None:
        raise ValueError("time window applies only to the top listing")
    return url


def run_reddit_grid_capture(
    *,
    subreddits: Sequence[str],
    listing: str,
    time_window: str | None,
    output_root: Path,
    decision_question: str,
    data_root: "DataLakeRoot | None" = None,
    max_subreddits: int = DEFAULT_MAX_SUBREDDITS,
    delay_seconds: float = DEFAULT_DELAY_SECONDS,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = DEFAULT_MAX_BYTES,
    cadence_mode: CadenceMode = "fixed",
    cadence_window_seconds: float | None = None,
    cadence_min_gap_seconds: float | None = None,
    cadence_max_gap_seconds: float | None = None,
    cadence_random_seed: int | None = None,
    requested_retention_mode: str = DEFAULT_RETENTION_MODE,
) -> tuple[int, str]:
    if requested_retention_mode not in CAPTURE_RETENTION_MODES:
        raise ValueError(
            f"requested_retention_mode must be one of {CAPTURE_RETENTION_MODES}, "
            f"got {requested_retention_mode!r}"
        )
    _validate_grid_inputs(
        subreddits=subreddits,
        output_root=output_root,
        max_subreddits=max_subreddits,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
    )
    names = [_validate_subreddit(name) for name in subreddits]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise ValueError(f"duplicate subreddit value(s): {duplicates}")
    urls = [build_grid_listing_url(subreddit=name, listing=listing, time_window=time_window) for name in names]

    cadence_plan = build_cadence_plan(
        slot_count=len(names),
        mode=cadence_mode,
        delay_seconds=delay_seconds,
        window_seconds=cadence_window_seconds,
        min_gap_seconds=cadence_min_gap_seconds,
        max_gap_seconds=cadence_max_gap_seconds,
        random_seed=cadence_random_seed,
    )
    output_root.mkdir(parents=True, exist_ok=True)
    summary_path = output_root / "grid_batch_summary.json"
    if summary_path.exists():
        raise ValueError(f"grid batch summary already exists: {summary_path}")

    results: list[dict[str, Any]] = []
    for index, (name, url) in enumerate(zip(names, urls)):
        row: dict[str, Any] = {
            "subreddit": name,
            "listing_url": url,
            "capture_exit": None,
            "capture_message": None,
            "packet_path": None,
            "planned_start_offset_seconds": cadence_plan.planned_offsets_seconds[index],
            "capture_started_at": None,
            "capture_finished_at": None,
            "content_extraction_failed": False,
        }
        extraction_spec = ContentExtractionSpec(
                requested_retention_mode=requested_retention_mode,
                extractor_version=GRID_PROJECTION_PARSER_VERSION,
                extractor=(
                    lambda html_text, _final_url, _name=name, _url=url: build_grid_content_record(
                        html_text=html_text,
                        subreddit=_name,
                        listing_url=_url,
                    )
                ),
            )
        try:
            row["capture_started_at"] = utc_now_z_microseconds()
            capture_exit, capture_message = run_source_capture_http_packet(
                url=url,
                source_family=GRID_SOURCE_FAMILY,
                source_surface=GRID_SOURCE_SURFACE,
                decision_question=decision_question,
                output_directory=None if data_root is not None else output_root / f"{name}_grid_packet",
                data_root=data_root,
                capture_context=(
                    "bounded reddit subreddit grid pass; one declared listing page per subreddit; "
                    "no link following, comment expansion, user/profile capture, or self-scheduling"
                ),
                operator_category="reddit_grid_capture_operator",
                capture_mode=CaptureModeCategory.STRUCTURED_ACCESS,
                session_id=None,
                actor_audience_context=None,
                visible_mode_changes=[],
                source_publication_or_event=None,
                source_edit_or_version=None,
                cutoff_posture=None,
                recapture_time=None,
                re_capture_relationship=None,
                warnings=[],
                limitations=[
                    SOURCE_POLICY_POSTURE_RECEIPT,
                    f"grid runner listing={listing} time_window={time_window or 'n/a'}",
                    f"grid runner cadence_mode={cadence_plan.mode}",
                    f"grid runner planned_start_offset_seconds={cadence_plan.planned_offsets_seconds[index]}",
                    "grid runner retry_count=0",
                ],
                timeout_seconds=timeout_seconds,
                max_bytes=max_bytes,
                content_extraction=extraction_spec,
            )
            row["capture_exit"] = capture_exit
            row["capture_message"] = capture_message
            if capture_exit in (0, CONTENT_EXTRACTION_FAILED_EXIT_CODE):
                row["packet_path"] = capture_message
            if capture_exit == CONTENT_EXTRACTION_FAILED_EXIT_CODE:
                row["content_extraction_failed"] = True
        except Exception as exc:
            row["capture_exit"] = 2
            row["capture_message"] = f"{type(exc).__name__}: {exc}"
        finally:
            row["capture_finished_at"] = utc_now_z_microseconds()

        results.append(row)
        if index < len(cadence_plan.planned_waits_seconds):
            wait_seconds = cadence_plan.planned_waits_seconds[index]
            if wait_seconds > 0:
                time.sleep(wait_seconds)

    summary = {
        "runner": "reddit_grid_capture",
        "method": GRID_SOURCE_SURFACE,
        "listing": listing,
        "time_window": time_window,
        "requested_retention_mode": requested_retention_mode,
        "content_extraction_failure_count": sum(
            1 for row in results if row["content_extraction_failed"]
        ),
        "lake_committed": data_root is not None,
        "source_policy_posture": SOURCE_POLICY_POSTURE_RECEIPT,
        "non_claims": [
            "not crawler",
            "not monitoring or self-scheduling",
            "not link following or comment expansion",
            "not user or profile capture",
            "not ToS sufficiency",
            "not demand proof or venue scoring",
        ],
        "cadence": cadence_plan.to_dict(),
        "max_subreddits": max_subreddits,
        "subreddit_count": len(names),
        "capture_success_count": sum(1 for row in results if row["capture_exit"] == 0),
        "results": results,
    }
    summary_path.write_text(
        f"{json.dumps(summary, indent=2, sort_keys=True)}\n",
        encoding="utf-8",
        newline="\n",
    )
    return 0, str(summary_path)


def _validate_subreddit(name: str) -> str:
    stripped = name.strip().lower().removeprefix("r/")
    if (
        not stripped
        or not stripped.isascii()
        or not stripped.replace("_", "").isalnum()
    ):
        raise ValueError(f"invalid subreddit name: {name!r}")
    return stripped


def _validate_grid_inputs(
    *,
    subreddits: Sequence[str],
    output_root: Path,
    max_subreddits: int,
    timeout_seconds: float,
    max_bytes: int,
) -> None:
    if not subreddits:
        raise ValueError("grid capture requires at least one subreddit")
    if max_subreddits <= 0:
        raise ValueError("max_subreddits must be greater than zero")
    if len(subreddits) > max_subreddits:
        raise ValueError(f"received {len(subreddits)} subreddit(s), above max_subreddits={max_subreddits}")
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than zero")
    if max_bytes <= 0:
        raise ValueError("max_bytes must be greater than zero")
    if output_root.exists() and not output_root.is_dir():
        raise ValueError(f"output_root exists and is not a directory: {output_root}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Capture one old Reddit listing (grid) page per named subreddit as a "
            "reddit_subreddit_grid Source Capture Packet, locally or into the data lake."
        )
    )
    parser.add_argument("--subreddit", action="append", required=True, dest="subreddits")
    parser.add_argument("--listing", choices=ALLOWED_LISTINGS, default="top")
    parser.add_argument("--time-window", choices=ALLOWED_TIME_WINDOWS, default=None)
    parser.add_argument("--output-root", type=Path, required=True,
                        help="Local root for the grid batch summary (and packets when --data-root is not used).")
    parser.add_argument("--data-root", default=None,
                        help="Commit packets into the Forseti data lake at this root instead of --output-root.")
    parser.add_argument("--decision-question", required=True)
    parser.add_argument("--max-subreddits", type=int, default=DEFAULT_MAX_SUBREDDITS)
    parser.add_argument("--delay-seconds", type=float, default=DEFAULT_DELAY_SECONDS)
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    parser.add_argument("--cadence-mode", choices=["fixed", "bounded_jitter"], default="fixed")
    parser.add_argument("--cadence-window-seconds", type=float, default=None)
    parser.add_argument("--cadence-min-gap-seconds", type=float, default=None)
    parser.add_argument("--cadence-max-gap-seconds", type=float, default=None)
    parser.add_argument("--cadence-random-seed", type=int, default=None)
    parser.add_argument(
        "--retention-mode",
        choices=list(CAPTURE_RETENTION_MODES),
        default=DEFAULT_RETENTION_MODE,
        help=(
            "content (default): preserve the content record, hash then discard raw; "
            "raw: preserve the source response."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    with exit_on_failure(parser, runner_name="reddit grid capture"):
        data_root = None
        if args.data_root is not None:
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)
        exit_code, message = run_reddit_grid_capture(
            subreddits=args.subreddits,
            listing=args.listing,
            time_window=args.time_window,
            output_root=args.output_root,
            data_root=data_root,
            decision_question=args.decision_question,
            max_subreddits=args.max_subreddits,
            delay_seconds=args.delay_seconds,
            timeout_seconds=args.timeout_seconds,
            max_bytes=args.max_bytes,
            cadence_mode=args.cadence_mode,
            cadence_window_seconds=args.cadence_window_seconds,
            cadence_min_gap_seconds=args.cadence_min_gap_seconds,
            cadence_max_gap_seconds=args.cadence_max_gap_seconds,
            cadence_random_seed=args.cadence_random_seed,
            requested_retention_mode=args.retention_mode,
        )

    print(message)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
