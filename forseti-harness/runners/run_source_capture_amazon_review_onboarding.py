"""Adapt exact Amazon-native top-review rows from a committed PDP packet."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.root import DataLakeRoot
from source_capture.amazon_review_onboarding_capture import (
    capture_amazon_review_onboarding_packet,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Commit a bounded Amazon-native PDP top-review companion; not Bazaarvoice, "
            "Most Helpful, Most Recent, or a complete corpus."
        )
    )
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--parent-packet-id", required=True)
    args = parser.parse_args(argv)
    root = DataLakeRoot.resolve(explicit=args.data_root)
    code, result = capture_amazon_review_onboarding_packet(
        data_root=root, parent_packet_id=args.parent_packet_id
    )
    summary = result["summary"]
    reviews = dict(summary["reviews"])
    reviews.pop("review_inventory", None)
    keys = (
        "record_kind",
        "provider",
        "identity",
        "review_aggregate",
        "questions",
        "extraction_target_matrix",
        "loss_ledger",
        "content_qualification",
    )
    compact = {key: summary[key] for key in keys}
    compact.update(
        {
            "packet_id": result["packet_id"],
            "output_directory": result["output_directory"],
            "reviews": reviews,
        }
    )
    print(json.dumps(compact, indent=2, sort_keys=True, ensure_ascii=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
