from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.catalog import catalog_coverage_census, inspect_catalog, rebuild_catalog
from data_lake.root import DataLakeRoot, DataLakeRootError


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Inspect or rebuild the generated Bronze catalog index."
    )
    parser.add_argument("--data-root", help="Explicit Forseti data root path.")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Replace the generated catalog from committed raw packets.",
    )
    parser.add_argument(
        "--census",
        action="store_true",
        help="Emit a read-only Bronze source-surface and Attachment Record coverage census.",
    )
    args = parser.parse_args(argv)
    if args.rebuild and args.census:
        parser.error("--census cannot be combined with --rebuild")

    try:
        root = DataLakeRoot.resolve(explicit=args.data_root)
        if args.rebuild:
            report = rebuild_catalog(root)
        elif args.census:
            report = catalog_coverage_census(root)
        else:
            report = inspect_catalog(root)
    # helper-delta: vs runners/_scaffold.exit_on_failure -- this runner reports
    # failures as a machine-readable JSON report on stdout with a returned exit
    # code (no parser.exit/stderr), and has no --output/--data-root pair for
    # runners/_scaffold.resolve_output_root; both blocks stay local on purpose.
    except DataLakeRootError as exc:
        report = {"status": "error", "error": str(exc)}
        print(json.dumps(report, indent=2, sort_keys=True))
        return 2

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report.get("status") in {"ok", "rebuilt"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
