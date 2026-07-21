"""Capture Ulta PowerReviews review and Q&A onboarding evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.root import DataLakeRoot
from source_capture.ulta_onboarding_capture import (
    DEFAULT_PAGES_PER_ROLE,
    DEFAULT_QUESTION_LIMIT,
    DEFAULT_REVIEW_PAGE_SIZE,
    capture_ulta_onboarding_packet,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Use a hash-verified, US/USD-pin-admitted rendered Ulta PDP packet to "
            "resolve the page-declared public PowerReviews display configuration "
            "and commit a raw-preserved three-role onboarding companion."
        )
    )
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--parent-packet-id", required=True)
    parser.add_argument(
        "--review-page-size",
        type=int,
        default=DEFAULT_REVIEW_PAGE_SIZE,
        help=(
            "Rows per display response (1-25; default 25 — the display route "
            "silently returns zero rows above 25)."
        ),
    )
    parser.add_argument(
        "--pages-per-role",
        type=int,
        default=DEFAULT_PAGES_PER_ROLE,
        help="Bounded offset pages per Helpful/Recent role (1-4; default 4).",
    )
    parser.add_argument(
        "--question-limit",
        type=int,
        default=DEFAULT_QUESTION_LIMIT,
        help="Bounded question window (1-25; default 25).",
    )
    parser.add_argument("--timeout-seconds", type=float, default=30.0)
    parser.add_argument("--max-bytes", type=int, default=8_000_000)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = DataLakeRoot.resolve(explicit=args.data_root)
    exit_code, result = capture_ulta_onboarding_packet(
        data_root=root,
        parent_packet_id=args.parent_packet_id,
        review_page_size=args.review_page_size,
        pages_per_role=args.pages_per_role,
        question_limit=args.question_limit,
        timeout_seconds=args.timeout_seconds,
        max_bytes=args.max_bytes,
    )
    summary = result["summary"]
    compact = {
        "packet_id": result["packet_id"],
        "output_directory": result["output_directory"],
        "record_kind": summary.get("record_kind"),
        "identity": summary.get("identity"),
        "review_aggregates": summary.get("review_aggregates"),
        "reviews": summary.get("reviews"),
        "questions": summary.get("questions"),
        "extraction_target_matrix": summary.get("extraction_target_matrix"),
        "loss_ledger": summary.get("loss_ledger"),
        "content_qualification": summary.get("content_qualification"),
        "raw_failure_fallback": summary.get("raw_failure_fallback"),
    }
    if isinstance(compact["questions"], dict):
        compact["questions"] = {
            key: value
            for key, value in compact["questions"].items()
            if key != "question_inventory"
        }
    if isinstance(compact["reviews"], dict):
        compact["reviews"] = dict(compact["reviews"])
        for view_name in ("most_helpful", "most_recent"):
            view = compact["reviews"].get(view_name)
            if isinstance(view, dict):
                compact["reviews"][view_name] = {
                    key: value
                    for key, value in view.items()
                    if key != "review_inventory"
                }
    print(json.dumps(compact, indent=2, sort_keys=True, ensure_ascii=False))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
