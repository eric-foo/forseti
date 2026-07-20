"""Capture Target Bazaarvoice review and Q&A onboarding evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.root import DataLakeRoot
from source_capture.target_onboarding_capture import (
    DEFAULT_QUESTION_LIMIT,
    DEFAULT_REVIEW_LIMIT,
    capture_target_onboarding_packet,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Use a hash-verified rendered Target PDP packet to resolve Target's "
            "public Bazaarvoice configuration and commit a raw-preserved three-role "
            "onboarding companion."
        )
    )
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--parent-packet-id", required=True)
    parser.add_argument(
        "--question-limit",
        type=int,
        default=DEFAULT_QUESTION_LIMIT,
        help="Bounded Most Answers question window (1-100; default 100).",
    )
    parser.add_argument(
        "--review-limit",
        type=int,
        default=DEFAULT_REVIEW_LIMIT,
        help="Rows in each Helpful and Recent response (1-100; default 100).",
    )
    parser.add_argument("--timeout-seconds", type=float, default=20.0)
    parser.add_argument("--max-bytes", type=int, default=8_000_000)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = DataLakeRoot.resolve(explicit=args.data_root)
    exit_code, result = capture_target_onboarding_packet(
        data_root=root,
        parent_packet_id=args.parent_packet_id,
        question_limit=args.question_limit,
        review_limit=args.review_limit,
        timeout_seconds=args.timeout_seconds,
        max_bytes=args.max_bytes,
    )
    summary = result["summary"]
    compact = {
        "packet_id": result["packet_id"],
        "output_directory": result["output_directory"],
        "record_kind": summary.get("record_kind"),
        "identity": summary.get("identity"),
        "product": summary.get("product"),
        "questions": summary.get("questions"),
        "reviews": summary.get("reviews"),
        "extraction_target_matrix": summary.get("extraction_target_matrix"),
        "loss_ledger": summary.get("loss_ledger"),
        "content_qualification": summary.get("content_qualification"),
        "raw_failure_fallback": summary.get("raw_failure_fallback"),
    }
    if isinstance(compact["questions"], dict):
        compact["questions"] = {
            key: value
            for key, value in compact["questions"].items()
            if key not in {"question_inventory", "answer_inventory"}
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
