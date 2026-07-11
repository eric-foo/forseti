"""Append generic Retail/PDP Silver records from one exact projection record."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.root import DataLakeRoot, DataLakeRootError
from source_capture.retail_pdp_silver import (
    RetailPdpSilverResult,
    derive_retail_pdp_silver_from_projection,
)


def run_producer(
    data_root: DataLakeRoot, *, packet_id: str, projection_record_id: str
) -> RetailPdpSilverResult:
    return derive_retail_pdp_silver_from_projection(
        data_root=data_root,
        packet_id=packet_id,
        projection_record_id=projection_record_id,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Append generic Retail/PDP Silver records from one exact "
            "projection_retail_pdp record."
        )
    )
    parser.add_argument("--data-root", default=None)
    parser.add_argument("--packet-id", required=True)
    parser.add_argument(
        "--projection-record-id",
        required=True,
        help="Exact record filename in projection_retail_pdp; no sibling guessing.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
        result = run_producer(
            data_root,
            packet_id=args.packet_id,
            projection_record_id=args.projection_record_id,
        )
    except (DataLakeRootError, OSError, ValueError) as exc:
        parser.exit(
            status=2,
            message=f"Retail/PDP Silver producer failed: {type(exc).__name__}: {exc}\n",
        )

    print(
        f"appended {len(result.records)} Retail/PDP Silver record(s) "
        f"from projection {result.projection_record_id}"
    )
    for path in result.paths:
        print(f"  silver: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
