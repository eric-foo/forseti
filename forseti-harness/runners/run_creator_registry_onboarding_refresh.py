from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.creator_registry_onboarding import (
    derive_onboarding_snapshot,
    dump_creator_registry_index,
    refresh_creator_registry_index_document,
    sha256_repo_text,
)
from data_lake.root import DataLakeRoot
from harness_utils import utc_now_z
from capture_spine.creator_profile_current.materialize import (
    build_creator_profile_current_view_from_files,
    dump_creator_profile_current_view,
)
from runners.run_creator_profile_current_materialize import (
    DEFAULT_METRIC_SEEDS,
    DEFAULT_OUTPUT as DEFAULT_PROFILE_VIEW,
    _enforce_new_account_preflight,
)
from runners.run_tiktok_creator_onboarding_coordinator import (
    _discover_retained_audience_pairs,
    _verify_existing_audience_joins_preserved,
)


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


def refresh_creator_registry_projections(
    *,
    data_root: DataLakeRoot,
    index_path: Path = DEFAULT_INDEX,
    account_ledger_path: Path = DEFAULT_LEDGER,
    profile_view_path: Path = DEFAULT_PROFILE_VIEW,
    generated_at_utc: str | None = None,
    preflight_receipt_path: Path | None = None,
) -> dict[str, Any]:
    """Refresh the account index and front-door view after a lake admission.

    The current view is rebuilt from its owning sources. Existing validated
    audience joins are discovered from the view's hash-bound source inputs and
    retained, so an onboarding refresh cannot silently erase them.
    """

    current_index = _json(index_path)
    ledger_document = _json(account_ledger_path)
    ledger = ledger_document["creator_public_handle_linkage_ledger"]
    onboarding_snapshot = derive_onboarding_snapshot(
        data_root=data_root,
        platform_accounts=ledger["platform_accounts"],
    )
    projection_generated_at = (
        generated_at_utc or _existing_generated_at(index_path) or utc_now_z()
    )
    generated_index = refresh_creator_registry_index_document(
        current_document=current_index,
        account_ledger=ledger,
        onboarding_by_account=onboarding_snapshot["accounts"],
        generated_at_utc=projection_generated_at,
        data_root_uuid=data_root.root_uuid,
        account_ledger_sha256=sha256_repo_text(account_ledger_path),
        derivation_diagnostics=onboarding_snapshot["diagnostics"],
    )
    rendered_index = dump_creator_registry_index(generated_index)

    _enforce_new_account_preflight(
        account_ledger_path=account_ledger_path,
        output_path=index_path,
        preflight_receipt_path=preflight_receipt_path,
    )
    _enforce_new_account_preflight(
        account_ledger_path=account_ledger_path,
        output_path=profile_view_path,
        preflight_receipt_path=preflight_receipt_path,
    )

    previous_index = index_path.read_bytes() if index_path.is_file() else None
    previous_profile = (
        profile_view_path.read_bytes() if profile_view_path.is_file() else None
    )
    previous_profile_document = (
        json.loads(previous_profile) if previous_profile is not None else {}
    )
    retained_snapshots, retained_outcomes = _discover_retained_audience_pairs(
        previous_document=previous_profile_document,
        target_profile_subject_id="",
    )

    index_path.parent.mkdir(parents=True, exist_ok=True)
    profile_view_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=index_path.parent,
        prefix=f".{index_path.name}.",
        suffix=".candidate",
        delete=False,
    ) as candidate_index_file:
        candidate_index_path = Path(candidate_index_file.name)
    with tempfile.NamedTemporaryFile(
        dir=profile_view_path.parent,
        prefix=f".{profile_view_path.name}.",
        suffix=".candidate",
        delete=False,
    ) as candidate_profile_file:
        candidate_profile_path = Path(candidate_profile_file.name)

    try:
        candidate_index_path.write_text(
            rendered_index, encoding="utf-8", newline="\n"
        )
        profile_generated_at = (
            generated_at_utc
            or _existing_profile_generated_at(profile_view_path)
            or projection_generated_at
        )
        generated_profile = build_creator_profile_current_view_from_files(
            account_ledger_path=account_ledger_path,
            creator_registry_index_path=candidate_index_path,
            metric_seed_paths=DEFAULT_METRIC_SEEDS,
            audience_triangulation_snapshot_paths=retained_snapshots,
            audience_judgment_outcome_paths=retained_outcomes,
            generated_at_utc=profile_generated_at,
        )
        _verify_existing_audience_joins_preserved(
            previous_output=previous_profile,
            candidate_document=generated_profile,
        )
        rendered_profile = dump_creator_profile_current_view(generated_profile)
        candidate_profile_path.write_text(
            rendered_profile, encoding="utf-8", newline="\n"
        )

        if (index_path.read_bytes() if index_path.is_file() else None) != previous_index:
            raise ValueError("Creator Registry index changed during projection refresh")
        if (
            profile_view_path.read_bytes() if profile_view_path.is_file() else None
        ) != previous_profile:
            raise ValueError("creator profile current view changed during projection refresh")

        os.replace(candidate_index_path, index_path)
        os.replace(candidate_profile_path, profile_view_path)
        if index_path.read_text(encoding="utf-8") != rendered_index:
            raise ValueError("fresh-read Creator Registry index verification failed")
        if profile_view_path.read_text(encoding="utf-8") != rendered_profile:
            raise ValueError("fresh-read creator profile view verification failed")
    finally:
        candidate_index_path.unlink(missing_ok=True)
        candidate_profile_path.unlink(missing_ok=True)

    counts = generated_index["creator_registry_index"]["counts"]
    return {
        "registry_index": str(index_path),
        "profile_current_view": str(profile_view_path),
        "platform_accounts_by_onboarding_state": counts[
            "platform_accounts_by_onboarding_state"
        ],
        "retained_audience_join_count": len(retained_snapshots),
        "derivation_diagnostics": onboarding_snapshot["diagnostics"],
    }


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
            generated_at_utc=args.generated_at_utc or _existing_generated_at(args.output) or utc_now_z(),
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


def _existing_generated_at(path: Path) -> str | None:
    if not path.is_file():
        return None
    wrapper = _json(path).get("creator_registry_index")
    if not isinstance(wrapper, dict):
        return None
    value = wrapper.get("generated_at_utc")
    return value if isinstance(value, str) and value else None


def _existing_profile_generated_at(path: Path) -> str | None:
    if not path.is_file():
        return None
    wrapper = _json(path).get("creator_profile_current_view")
    if not isinstance(wrapper, dict):
        return None
    value = wrapper.get("generated_at_utc")
    return value if isinstance(value, str) and value else None


if __name__ == "__main__":
    raise SystemExit(main())
