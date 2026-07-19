"""Print a read-only Silver observation census generated from lake authority."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from time import perf_counter

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.root import DataLakeRoot, DataLakeRootError
from data_lake.silver_census import build_silver_observation_census


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate the deterministic, read-only Silver Vault observation census."
    )
    parser.add_argument("--data-root", help="Explicit verified Forseti lake root.")
    parser.add_argument("--pretty", action="store_true", help="Indent JSON output.")
    args = parser.parse_args(argv)
    command_started = perf_counter()

    def emit_progress(event: dict[str, object]) -> None:
        print(json.dumps(event, sort_keys=True), file=sys.stderr, flush=True)

    try:
        data_root = DataLakeRoot.resolve_readonly(explicit=args.data_root)
        census = build_silver_observation_census(
            data_root,
            progress=emit_progress,
        )
    except (DataLakeRootError, OSError, TypeError, ValueError) as exc:
        emit_progress(
            {
                "phase": "silver_observation_census",
                "status": "phase_failed",
                "elapsed_seconds": round(
                    max(0.0, perf_counter() - command_started), 3
                ),
                "error_type": type(exc).__name__,
            }
        )
        parser.exit(status=2, message=f"Silver census unavailable: {exc}\n")
    print(
        json.dumps(
            census,
            ensure_ascii=False,
            sort_keys=True,
            indent=2 if args.pretty else None,
            separators=None if args.pretty else (",", ":"),
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
