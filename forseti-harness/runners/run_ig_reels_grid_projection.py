from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.root import DataLakeRoot
from source_capture.ig_reels_grid_projection import (
    build_ig_reels_grid_projection_from_packet_directory,
    project_ig_reels_grid_from_bronze_catalog,
    project_ig_reels_grid_into_lake,
    write_ig_reels_grid_projection,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Project one existing IG reels-grid Source Capture Packet into view-only metric rows."
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--packet", type=Path, help="Packet directory or manifest.json path.")
    input_group.add_argument("--packet-id", help="Committed raw packet id in the Forseti data lake.")
    input_group.add_argument(
        "--bronze-source-surface",
        action="store_true",
        help="Project IG reels-grid packets discovered through the generated Bronze source-surface catalog.",
    )
    parser.add_argument(
        "--data-root",
        default=None,
        help="Forseti data-lake root for --packet-id mode (or set FORSETI_DATA_ROOT (legacy ORCA_DATA_ROOT)).",
    )
    parser.add_argument(
        "--record-id",
        default=None,
        help="Optional create-only derived record id for --packet-id mode; .json is appended.",
    )
    parser.add_argument(
        "--record-id-prefix",
        default=None,
        help="Optional stable derived record id namespace for --bronze-source-surface mode.",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help=(
            "With --bronze-source-surface, skip stable projection records that already exist "
            "instead of failing the rerun."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output JSON path for --packet mode. If omitted, projection JSON is printed to stdout.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing an existing --output path.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.packet_id is not None:
            if args.output is not None:
                raise ValueError("--output is only valid with --packet; lake mode appends a derived record")
            if args.record_id_prefix is not None:
                raise ValueError("--record-id-prefix is only valid with --bronze-source-surface")
            if args.skip_existing:
                raise ValueError("--skip-existing is only valid with --bronze-source-surface")
            if args.data_root is None and not (os.environ.get("FORSETI_DATA_ROOT") or os.environ.get("ORCA_DATA_ROOT")):
                raise ValueError("--data-root/FORSETI_DATA_ROOT/ORCA_DATA_ROOT is required with --packet-id")
            data_root = DataLakeRoot.resolve(explicit=args.data_root)
            _projection, derived_path = project_ig_reels_grid_into_lake(
                data_root=data_root,
                packet_id=args.packet_id,
                record_id=args.record_id,
            )
            print(derived_path)
            return 0

        if args.bronze_source_surface:
            if args.output is not None:
                raise ValueError("--output is only valid with --packet; lake mode appends derived records")
            if args.record_id is not None:
                raise ValueError("--record-id is only valid with --packet-id")
            if args.data_root is None and not (os.environ.get("FORSETI_DATA_ROOT") or os.environ.get("ORCA_DATA_ROOT")):
                raise ValueError("--data-root/FORSETI_DATA_ROOT/ORCA_DATA_ROOT is required with --bronze-source-surface")
            data_root = DataLakeRoot.resolve(explicit=args.data_root)
            projected = project_ig_reels_grid_from_bronze_catalog(
                data_root=data_root,
                record_id_prefix=args.record_id_prefix,
                skip_existing=args.skip_existing,
            )
            print(json.dumps([str(path) for _projection, path in projected], indent=2))
            return 0

        if args.record_id is not None:
            raise ValueError("--record-id is only valid with --packet-id")
        if args.record_id_prefix is not None:
            raise ValueError("--record-id-prefix is only valid with --bronze-source-surface")
        if args.skip_existing:
            raise ValueError("--skip-existing is only valid with --bronze-source-surface")
        if args.data_root is not None:
            raise ValueError("--data-root is only valid with --packet-id or --bronze-source-surface")
        if args.output is not None:
            write_ig_reels_grid_projection(
                packet_or_manifest_path=args.packet,
                output_path=args.output,
                overwrite=args.overwrite,
            )
            print(args.output)
            return 0

        projection = build_ig_reels_grid_projection_from_packet_directory(
            packet_or_manifest_path=args.packet,
        )
    except Exception as exc:
        parser.exit(status=2, message=f"ig reels-grid projection failed: {exc}\n")

    print(json.dumps(projection.model_dump(mode="json"), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())