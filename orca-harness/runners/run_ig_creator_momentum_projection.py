from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.ig_projection import (
    build_ig_creator_momentum_projection_from_packet_directory,
    write_ig_creator_momentum_projection,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Project one existing IG Source Capture Packet into view-only creator-momentum rows."
    )
    parser.add_argument("--packet", type=Path, required=True, help="Packet directory or manifest.json path.")
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional output JSON path. If omitted, projection JSON is printed to stdout.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing an existing output path.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.output is not None:
            write_ig_creator_momentum_projection(
                packet_or_manifest_path=args.packet,
                output_path=args.output,
                overwrite=args.overwrite,
            )
            print(args.output)
            return 0

        projection = build_ig_creator_momentum_projection_from_packet_directory(
            packet_or_manifest_path=args.packet,
        )
    except Exception as exc:
        parser.exit(status=2, message=f"ig projection failed: {exc}\n")

    print(json.dumps(projection.model_dump(mode="json"), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
