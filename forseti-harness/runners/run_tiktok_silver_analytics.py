"""Build a fused, non-Judgment TikTok Cleaning/Silver analytics readout.

Inputs are explicit JSON artifacts so the runner is scratch-safe and cannot
silently select live-lake siblings. Product extraction remains owned by
``run_tiktok_product_extract``; this runner consumes its mention records.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cleaning.tiktok_silver_analytics import (
    ANALYTICS_POLICY_VERSION,
    comment_engagement_context,
    product_readout,
    resolve_product_mentions,
    temporal_signal,
)


def _load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _videos(payloads: Iterable[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    selected: dict[str, Mapping[str, Any]] = {}
    for payload in payloads:
        rows = payload.get("videos")
        if not isinstance(rows, list):
            raise ValueError("TikTok batch payload requires a videos list")
        for row in rows:
            if not isinstance(row, Mapping):
                raise ValueError("TikTok batch video rows must be objects")
            video_id = str(row.get("video_id") or row.get("id") or "").strip()
            if not video_id:
                raise ValueError("TikTok batch video row lacks video_id")
            selected[video_id] = row
    return [selected[key] for key in sorted(selected)]


def _mentions(records: Iterable[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    result: list[Mapping[str, Any]] = []
    for record in records:
        rows = record.get("mentions")
        if not isinstance(rows, list):
            raise ValueError("product mention record requires a mentions list")
        result.extend(row for row in rows if isinstance(row, Mapping))
    return result


def build_readout(
    *,
    batch_payloads: list[Mapping[str, Any]],
    mention_records: list[Mapping[str, Any]],
    entity_catalog: Mapping[str, Any],
    semantic_labels: Mapping[str, Any] | None = None,
    temporal_observations: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    videos = _videos(batch_payloads)
    resolved = resolve_product_mentions(_mentions(mention_records), entity_catalog)
    temporal = temporal_observations or {}
    comment_views = [
        comment_engagement_context(video, semantic_labels=semantic_labels) for video in videos
    ]
    return {
        "analytics_policy_version": ANALYTICS_POLICY_VERSION,
        "entity_catalog_version": entity_catalog["version"],
        "video_count": len(videos),
        "comments": {
            "video_count": len(comment_views),
            "captured_comment_count": sum(row["captured_comment_count"] for row in comment_views),
            "semantic_posture": "classified" if semantic_labels is not None else "not_attempted",
            "videos": comment_views,
        },
        "products": product_readout(resolved),
        "temporal": {
            key: temporal_signal(rows if isinstance(rows, list) else [])
            for key, rows in sorted(temporal.items())
        }
        or {
            "creator_metrics": temporal_signal([]),
        },
        "non_claims": [
            "not_comment_credibility_or_decision_impact",
            "not_full_comment_census",
            "not_cross_platform_entity_identity",
            "not_velocity_or_acceleration_without_genuine_repeated_observations",
        ],
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=Path, action="append", required=True)
    parser.add_argument("--mentions", type=Path, action="append", default=[])
    parser.add_argument("--entity-catalog", type=Path, required=True)
    parser.add_argument("--comment-labels", type=Path)
    parser.add_argument("--temporal-observations", type=Path)
    parser.add_argument("--out", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        readout = build_readout(
            batch_payloads=[_load_object(path) for path in args.batch],
            mention_records=[_load_object(path) for path in args.mentions],
            entity_catalog=_load_object(args.entity_catalog),
            semantic_labels=_load_object(args.comment_labels) if args.comment_labels else None,
            temporal_observations=(
                _load_object(args.temporal_observations) if args.temporal_observations else None
            ),
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, sort_keys=True))
        return 2
    body = json.dumps(readout, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(body, encoding="utf-8")
        print(json.dumps({"status": "written", "path": str(args.out)}, indent=2, sort_keys=True))
    else:
        print(body, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
