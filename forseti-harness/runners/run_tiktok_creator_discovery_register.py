"""Build a TikTok Creator Discovery Frontier register and persist it.

Default output is the data lake (derived record anchored to the parent-grid
packet), so routine scans write operational lake records instead of opening a
repo PR per scan. An explicit ``--output`` file path is the local escape.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import os

from capture_spine.tiktok_creator_discovery_frontier.register_lake_writer import (
    write_tiktok_creator_discovery_frontier_register,
)
from capture_spine.tiktok_creator_discovery_frontier.register_writer import (
    build_tiktok_creator_discovery_frontier_register,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build a validated TikTok creator discovery frontier register from a "
            "scan receipt + suggested-account observations, and write it to the "
            "data lake by default (or a local --output file)."
        )
    )
    parser.add_argument("--scan-receipt-json", required=True, type=Path)
    parser.add_argument(
        "--suggested-accounts-json",
        required=True,
        type=Path,
        help="JSON list of suggested-account observation objects.",
    )
    parser.add_argument("--prior-register-pointer", required=True)
    parser.add_argument(
        "--record-id",
        default=None,
        help="Derived record id. Defaults to <register_id>.json from the receipt.",
    )
    target = parser.add_mutually_exclusive_group(required=False)
    target.add_argument("--output", type=Path, default=None)
    target.add_argument(
        "--data-root",
        default=None,
        help=(
            "Commit into the Forseti data lake at this root; FORSETI_DATA_ROOT is "
            "used only when --output is omitted; legacy ORCA_DATA_ROOT is also accepted."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        data_root_requested = args.data_root is not None or (
            args.output is None
            and (os.environ.get("FORSETI_DATA_ROOT") or os.environ.get("ORCA_DATA_ROOT"))
        )
        if args.output is None and not data_root_requested:
            parser.exit(
                status=2,
                message=(
                    "tiktok creator discovery register failed: exactly one of --output "
                    "or --data-root/FORSETI_DATA_ROOT/ORCA_DATA_ROOT is required\n"
                ),
            )
        scan_receipt = _load_json(args.scan_receipt_json)
        suggested_accounts = _load_json(args.suggested_accounts_json)
        if not isinstance(suggested_accounts, list):
            raise ValueError("suggested-accounts JSON must be a list of observation objects")
        register = build_tiktok_creator_discovery_frontier_register(
            scan_receipt=scan_receipt,
            suggested_accounts=suggested_accounts,
            prior_register_pointer=args.prior_register_pointer,
        )
        if args.output is not None:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(register, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
                newline="\n",
            )
            print(args.output)
            return 0
        from data_lake.root import DataLakeRoot

        data_root = DataLakeRoot.resolve(explicit=args.data_root)
        register_id = register["tiktok_creator_discovery_frontier_register"]["register_id"]
        record_id = args.record_id or f"{register_id}.json"
        written = write_tiktok_creator_discovery_frontier_register(
            register, data_root, record_id=record_id
        )
        print(written)
        return 0
    except Exception as exc:
        parser.exit(status=2, message=f"tiktok creator discovery register failed: {exc}\n")


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    raise SystemExit(main())
