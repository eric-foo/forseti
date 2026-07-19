"""Capture Sephora Most-Answers Q&A and non-incentivized age counts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.root import DataLakeRoot
from source_capture.sephora_onboarding_capture import (
    DEFAULT_QUESTION_LIMIT,
    capture_sephora_onboarding_packet,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Use a hash-verified rendered Sephora PDP packet to capture a raw-preserved "
            "Bazaarvoice onboarding companion. The data root is explicit because this "
            "command performs live structured acquisition and commits append-only raw evidence."
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
    parser.add_argument("--timeout-seconds", type=float, default=20.0)
    parser.add_argument("--max-bytes", type=int, default=8_000_000)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = DataLakeRoot.resolve(explicit=args.data_root)
    exit_code, result = capture_sephora_onboarding_packet(
        data_root=root,
        parent_packet_id=args.parent_packet_id,
        question_limit=args.question_limit,
        timeout_seconds=args.timeout_seconds,
        max_bytes=args.max_bytes,
    )
    summary = result["summary"]
    compact = {
        "packet_id": result["packet_id"],
        "output_directory": result["output_directory"],
        "record_kind": summary.get("record_kind"),
        "questions": summary.get("questions", {}),
        "reviews": summary.get("reviews", {}),
        "parser_fit": summary.get("parser_fit"),
        "projection_equivalence": summary.get("projection_equivalence"),
        "loss_ledger": summary.get("loss_ledger"),
        "raw_failure_fallback": summary.get("raw_failure_fallback"),
    }
    if isinstance(compact["questions"], dict):
        compact["questions"] = {
            key: value
            for key, value in compact["questions"].items()
            if key != "question_inventory"
        }
    print(json.dumps(compact, indent=2, sort_keys=True, ensure_ascii=False))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
