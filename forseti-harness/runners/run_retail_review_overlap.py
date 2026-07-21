from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cleaning.retail_review_overlap import (
    write_depth_selection,
    write_review_linkage,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Select evidence-backed retail review depth or derive deterministic "
            "cross-retailer review overlap without mutating native occurrences."
        )
    )
    subparsers = parser.add_subparsers(dest="operation", required=True)
    for operation in ("select-depth", "link-reviews"):
        child = subparsers.add_parser(operation)
        child.add_argument("--commission", type=Path, required=True)
        child.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.operation == "select-depth":
            write_depth_selection(
                commission_path=args.commission,
                output_path=args.output,
            )
        else:
            write_review_linkage(
                commission_path=args.commission,
                output_path=args.output,
            )
    except Exception as exc:
        parser.exit(
            status=2,
            message=f"retail review {args.operation} failed: {exc}" + chr(10),
        )
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())