from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.retail_grid_projection import write_retail_grid_projection


def run_retail_grid_projection(*, packet_directory: Path, output_path: Path) -> Path:
    projection = write_retail_grid_projection(
        packet_directory=packet_directory, output_path=output_path
    )
    if projection.completeness.status == "incomplete":
        raise ValueError(
            "retail grid completeness reconciliation failed closed: "
            + "; ".join(projection.completeness.residuals)
        )
    return output_path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a local, no-network Walmart/Target/Sephora/Ulta retail-grid projection JSON "
            "from an existing Source Capture Packet directory."
        )
    )
    parser.add_argument("--packet-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        output_path = run_retail_grid_projection(
            packet_directory=args.packet_dir, output_path=args.output
        )
    except Exception as exc:
        parser.exit(status=2, message=f"retail grid projection failed: {exc}\n")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
