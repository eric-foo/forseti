"""Append generic Retail/PDP Silver records through Cleaning."""
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
    derive_retail_pdp_silver,
)


def run_producer(
    data_root: DataLakeRoot, *, packet_id: str
) -> RetailPdpSilverResult:
    return derive_retail_pdp_silver(
        data_root=data_root,
        packet_id=packet_id,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Append generic Retail/PDP Silver records from one packet through "
            "Cleaning-owned content adaptation."
        )
    )
    parser.add_argument("--data-root", default=None)
    parser.add_argument("--packet-id", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
        result = run_producer(
            data_root,
            packet_id=args.packet_id,
        )
    except (DataLakeRootError, OSError, ValueError) as exc:
        parser.exit(
            status=2,
            message=f"Retail/PDP Silver producer failed: {type(exc).__name__}: {exc}\n",
        )

    print(
        f"appended {len(result.records)} Retail/PDP Silver record(s) "
        f"from Cleaning basis {result.cleaning_basis}"
    )
    for path in result.paths:
        print(f"  silver: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
