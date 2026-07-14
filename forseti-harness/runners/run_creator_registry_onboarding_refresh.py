from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.creator_registry_onboarding import (
    derive_onboarding_snapshot,
    dump_creator_registry_index,
    refresh_creator_registry_index_document,
    sha256_repo_text,
)
from data_lake.root import DataLakeRoot
from runners.run_creator_profile_current_materialize import _enforce_new_account_preflight


ROOT = Path(__file__).resolve().parents[2]
CREATOR_REGISTRY_ROOT = (
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
DEFAULT_INDEX = CREATOR_REGISTRY_ROOT / "creator_registry_index_v0.json"
DEFAULT_LEDGER = CREATOR_REGISTRY_ROOT / "creator_public_handle_linkage_ledger_v0.json"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Refresh account-level Creator Registry onboarding state from exact, "
            "verified committed Bronze evidence. The runner never writes the data lake."
        )
    )
    parser.add_argument("--data-root", type=Path, help="Forseti data lake root; defaults to configured environment.")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--account-ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--output", type=Path, default=DEFAULT_INDEX)
    parser.add_argument(
        "--generated-at-utc",
        help="Projection timestamp; defaults to the existing output timestamp when present.",
    )
    parser.add_argument(
        "--preflight-receipt",
        type=Path,
        help="Exact-match Creator Registry preflight receipt required when new accounts are introduced.",
    )
    parser.add_argument("--check", action="store_true", help="Fail if the checked-in index is stale.")
    parser.add_argument("--write", action="store_true", help="Write the refreshed registry index.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    if args.check == args.write:
        parser.error("choose exactly one of --check or --write")
    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
        current_document = _json(args.index)
        ledger_document = _json(args.account_ledger)
        ledger = ledger_document["creator_public_handle_linkage_ledger"]
        onboarding_snapshot = derive_onboarding_snapshot(
            data_root=data_root,
            platform_accounts=ledger["platform_accounts"],
        )
        generated = refresh_creator_registry_index_document(
            current_document=current_document,
            account_ledger=ledger,
            onboarding_by_account=onboarding_snapshot["accounts"],
            generated_at_utc=args.generated_at_utc or _existing_generated_at(args.output) or _now_utc(),
            data_root_uuid=data_root.root_uuid,
            account_ledger_sha256=sha256_repo_text(args.account_ledger),
            derivation_diagnostics=onboarding_snapshot["diagnostics"],
        )
        rendered = dump_creator_registry_index(generated)
        if args.check:
            if not args.output.is_file():
                raise ValueError(f"registry index does not exist: {args.output}")
            if args.output.read_text(encoding="utf-8") != rendered:
                raise ValueError(f"Creator Registry onboarding projection is stale: {args.output}")
            print(f"up to date: {args.output}")
            return 0

        _enforce_new_account_preflight(
            account_ledger_path=args.account_ledger,
            output_path=args.output,
            preflight_receipt_path=args.preflight_receipt,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
        counts = generated["creator_registry_index"]["counts"]
        print(
            json.dumps(
                {
                    "output": str(args.output),
                    "data_root_uuid": data_root.root_uuid,
                    "platform_accounts_total": counts["platform_accounts_total"],
                    "platform_accounts_by_onboarding_state": counts[
                        "platform_accounts_by_onboarding_state"
                    ],
                    "derivation_diagnostics": onboarding_snapshot["diagnostics"],
                },
                sort_keys=True,
            )
        )
        return 0
    except Exception as exc:
        parser.exit(status=2, message=f"Creator Registry onboarding refresh failed: {exc}\n")


def _json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON document must be an object: {path}")
    return value


def _now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _existing_generated_at(path: Path) -> str | None:
    if not path.is_file():
        return None
    wrapper = _json(path).get("creator_registry_index")
    if not isinstance(wrapper, dict):
        return None
    value = wrapper.get("generated_at_utc")
    return value if isinstance(value, str) and value else None


if __name__ == "__main__":
    raise SystemExit(main())
