"""Admit one already-captured TikTok grid window as a grid-only Bronze packet."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.root import DataLakeRoot, DataLakeRootError
from source_capture.tiktok.grid_packet import write_tiktok_grid_packet


def run_tiktok_grid_packet(
    *,
    grid_window_json_path: Path,
    observed_at_utc: str | None,
    output_directory: Path | None = None,
    data_root: DataLakeRoot | None = None,
) -> tuple[int, str]:
    return write_tiktok_grid_packet(
        grid_window_json=grid_window_json_path.read_bytes(),
        observed_at_utc=observed_at_utc,
        output_directory=output_directory,
        data_root=data_root,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grid-window-json", required=True, type=Path)
    parser.add_argument(
        "--observed-at-utc",
        help="Required for legacy grid artifacts whose collection receipt lacks capture_timestamp.",
    )
    destination = parser.add_mutually_exclusive_group(required=True)
    destination.add_argument("--output-directory", type=Path)
    destination.add_argument("--data-root")
    args = parser.parse_args(argv)
    try:
        data_root = (
            DataLakeRoot.resolve(explicit=args.data_root) if args.data_root is not None else None
        )
        exit_code, output = run_tiktok_grid_packet(
            grid_window_json_path=args.grid_window_json,
            observed_at_utc=args.observed_at_utc,
            output_directory=args.output_directory,
            data_root=data_root,
        )
    except (OSError, ValueError, DataLakeRootError) as exc:
        parser.exit(status=2, message=f"TikTok grid packet admission failed: {exc}\n")
    print(output)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
