from __future__ import annotations

import argparse
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.source_quality import build_source_quality_state_census


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a read-only Source Quality State Assembler census from explicit "
            "queue rows and existing Source Capture Packet manifests."
        )
    )
    parser.add_argument("--queue", type=Path, required=True, help="YAML or JSON queue file with rows.")
    parser.add_argument("--output", type=Path, required=True, help="New YAML output path for the state census.")
    parser.add_argument(
        "--base-dir",
        type=Path,
        help="Base directory for relative packet paths. Defaults to the current working directory.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        rows = _load_rows(args.queue)
        if args.output.exists():
            raise ValueError(f"output already exists: {args.output}")
        census = build_source_quality_state_census(
            rows=rows,
            base_path=args.base_dir or Path.cwd(),
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(yaml.safe_dump(census, sort_keys=False), encoding="utf-8")
    except Exception as exc:
        parser.exit(status=2, message=f"source-quality state assembler failed: {exc}\n")

    print(args.output)
    return 0


def _load_rows(path: Path) -> list[Mapping[str, Any]]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    rows = loaded.get("rows") if isinstance(loaded, dict) else loaded
    if not isinstance(rows, list):
        raise ValueError("queue must be a list of rows or a mapping with a rows list")
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, Mapping):
            raise ValueError(f"queue row {index} must be a mapping")
    return rows


if __name__ == "__main__":
    raise SystemExit(main())
