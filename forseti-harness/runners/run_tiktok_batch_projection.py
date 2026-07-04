"""CLI: build a mechanical projection from an admitted TikTok batch packet."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.tiktok.batch_projection import (  # noqa: E402
    build_tiktok_batch_projection_from_lake,
    build_tiktok_batch_projection_from_packet_directory,
    tiktok_batch_projection_json_text,
    write_tiktok_batch_projection,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a deterministic, text-free projection from an admitted TikTok batch packet."
        )
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--packet", type=Path, help="Packet directory or manifest.json path.")
    source.add_argument("--packet-id", help="Committed raw packet id in the Orca data lake.")
    parser.add_argument(
        "--data-root",
        default=None,
        help="Orca data-lake root for --packet-id. ORCA_DATA_ROOT is used when omitted.",
    )
    parser.add_argument("--output", type=Path, default=None, help="Optional output JSON path; stdout when omitted.")
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing an existing --output path.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.packet is not None:
            if args.data_root is not None:
                raise ValueError("--data-root is only valid with --packet-id")
            projection = build_tiktok_batch_projection_from_packet_directory(args.packet)
        else:
            if args.data_root is None and not os.environ.get("ORCA_DATA_ROOT"):
                raise ValueError("--data-root or ORCA_DATA_ROOT is required with --packet-id")
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)
            projection = build_tiktok_batch_projection_from_lake(data_root, args.packet_id)

        if args.output is not None:
            written = write_tiktok_batch_projection(
                projection=projection,
                output_path=args.output,
                overwrite=args.overwrite,
            )
            print(written)
            return 0

        print(tiktok_batch_projection_json_text(projection), end="")
        return 0
    except ValueError as exc:
        parser.exit(status=2, message=f"tiktok batch projection failed: {exc}\n")
    except Exception as exc:  # noqa: BLE001 - surface packet/lake/read failures visibly
        parser.exit(status=3, message=f"tiktok batch projection failed: {type(exc).__name__}: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
