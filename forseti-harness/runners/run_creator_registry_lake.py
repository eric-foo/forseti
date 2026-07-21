"""Migrate, rebuild, query, and admit the lake-native Creator Registry."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.creator_registry import (
    CreatorRegistryLakeError,
    admit_tiktok_creator_account,
    load_current_creator_profiles,
    load_current_creator_registry,
    migrate_legacy_registry,
    monitoring_eligible_accounts,
    publish_creator_registry_generation,
)
from data_lake.root import DataLakeRoot, DataLakeRootError


ROOT = Path(__file__).resolve().parents[2]
LEGACY_ROOT = (
    ROOT
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_registry"
)
DEFAULT_LEDGER = LEGACY_ROOT / "creator_public_handle_linkage_ledger_v0.json"
DEFAULT_INDEX = LEGACY_ROOT / "creator_registry_index_v0.json"
DEFAULT_PROFILE = LEGACY_ROOT / "creator_profile_current_view_v0.json"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    migrate = commands.add_parser("migrate")
    migrate.add_argument("--data-root", required=True)
    migrate.add_argument("--account-ledger", type=Path, default=DEFAULT_LEDGER)
    migrate.add_argument("--registry-index", type=Path, default=DEFAULT_INDEX)
    migrate.add_argument("--profile-current", type=Path, default=DEFAULT_PROFILE)
    mode = migrate.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--write", action="store_true")

    rebuild = commands.add_parser("rebuild")
    rebuild.add_argument("--data-root", required=True)

    show = commands.add_parser("show")
    show.add_argument("--data-root", required=True)
    show.add_argument("--view", choices=("internal", "public"), required=True)

    eligible = commands.add_parser("eligible")
    eligible.add_argument("--data-root", required=True)
    eligible.add_argument("--platform", choices=("instagram", "tiktok", "youtube"))

    admit = commands.add_parser("admit-tiktok")
    admit.add_argument("--data-root", required=True)
    admit.add_argument("--packet-id", required=True)
    admit.add_argument("--judgment-outcome", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        root = DataLakeRoot.resolve(explicit=args.data_root)
        if args.command == "migrate":
            result = migrate_legacy_registry(
                data_root=root,
                account_ledger_path=args.account_ledger,
                registry_index_path=args.registry_index,
                profile_current_path=args.profile_current,
                dry_run=args.dry_run,
            )
        elif args.command == "rebuild":
            result = publish_creator_registry_generation(root)
        elif args.command == "show":
            result = (
                load_current_creator_registry(root)
                if args.view == "internal"
                else load_current_creator_profiles(root)
            )
        elif args.command == "eligible":
            rows = monitoring_eligible_accounts(root, platform=args.platform)
            result = {"platform": args.platform, "count": len(rows), "accounts": rows}
        else:
            result = admit_tiktok_creator_account(
                data_root=root,
                packet_id=args.packet_id,
                judgment_outcome_path=args.judgment_outcome,
            )
    except (CreatorRegistryLakeError, DataLakeRootError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, sort_keys=True))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
