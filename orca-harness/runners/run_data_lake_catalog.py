from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.catalog import inspect_catalog, rebuild_catalog
from data_lake.root import DataLakeRoot, DataLakeRootError


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Inspect or rebuild the generated Bronze catalog index."
    )
    parser.add_argument("--data-root", help="Explicit Orca data root path.")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Replace the generated catalog from committed raw packets.",
    )
    args = parser.parse_args(argv)

    try:
        root = DataLakeRoot.resolve(explicit=args.data_root)
        report = rebuild_catalog(root) if args.rebuild else inspect_catalog(root)
    except DataLakeRootError as exc:
        report = {"status": "error", "error": str(exc)}
        print(json.dumps(report, indent=2, sort_keys=True))
        return 2

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report.get("status") in {"ok", "rebuilt"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
