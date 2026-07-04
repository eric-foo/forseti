"""Deterministic runner for on-demand creator ideal-audience profile snapshots.

This is Pass 2 only: it consumes already-produced ``EvidenceRecord`` JSON and
emits a registry-joinable snapshot document. It performs no live LLM extraction,
no source capture, and no data-lake writes.
"""

from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.ideal_audience_snapshot import (
    build_creator_ideal_audience_profile_snapshot_from_evidence,
    build_creator_ideal_audience_snapshot_document,
    dump_creator_ideal_audience_snapshot_document,
    load_evidence_records,
)


def _now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build an on-demand Tier-1 creator ideal-audience profile snapshot from "
            "pre-existing EvidenceRecord JSON. No LLM, capture, or lake write occurs."
        )
    )
    parser.add_argument("--evidence-records", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--profile-subject-id", help="Defaults to the sole creator_id in evidence.")
    parser.add_argument(
        "--profile-subject-kind",
        choices=("platform_account", "creator_record"),
        default="platform_account",
    )
    parser.add_argument(
        "--platform-account-id",
        action="append",
        dest="platform_account_ids",
        help="Platform account id(s) represented by this snapshot. Defaults to profile-subject-id.",
    )
    parser.add_argument("--creator-record-id")
    parser.add_argument(
        "--platform-scope",
        choices=("instagram", "tiktok", "youtube", "cross_platform"),
        help="Defaults to the platform implied by the fused profile pillars, or cross_platform.",
    )
    parser.add_argument("--observation-window-start", required=True)
    parser.add_argument("--observation-window-end", required=True)
    parser.add_argument("--computed-at", help="Defaults to now (UTC).")
    parser.add_argument("--snapshot-id")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        records = load_evidence_records(args.evidence_records)
        creator_ids = sorted({record.creator_id for record in records})
        if len(creator_ids) != 1:
            raise ValueError(f"evidence must reference exactly one creator_id, got {creator_ids!r}")
        subject_id = args.profile_subject_id or creator_ids[0]
        computed_at = args.computed_at or _now_utc()
        snapshot = build_creator_ideal_audience_profile_snapshot_from_evidence(
            records,
            profile_subject_kind=args.profile_subject_kind,
            profile_subject_id=subject_id,
            platform_account_ids=args.platform_account_ids,
            creator_record_id_or_none=args.creator_record_id,
            platform_scope=args.platform_scope,
            observation_window_start=args.observation_window_start,
            observation_window_end=args.observation_window_end,
            computed_at=computed_at,
            snapshot_id=args.snapshot_id,
        )
        document = build_creator_ideal_audience_snapshot_document([snapshot], generated_at_utc=computed_at)
    except Exception as exc:
        parser.exit(status=2, message=f"creator ideal-audience snapshot failed: {type(exc).__name__}: {exc}\n")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        dump_creator_ideal_audience_snapshot_document(document),
        encoding="utf-8",
        newline="\n",
    )
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
