"""Read-only creator/product lookup over generated lake views.

Creator lookup combines the stable Git-backed creator_profile_current row with
its daily generated Creator Vault account envelope. The envelope remains a
rebuildable, non-authoritative view over Silver; absent metrics never mean zero.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.validation import load_creator_profile_current_view
from data_lake.derived_retrieval_views import (
    SILVER_VAULT_CORE_PARTS,
    SILVER_VAULT_CREATOR_PARTS,
)
from data_lake.root import DataLakeRoot, DataLakeRootError

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = (
    ROOT
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_registry"
    / "creator_profile_current_view_v0.json"
)
_ACCOUNT_ID_FIELDS = (
    "platform_account_id",
    "forseti_platform_account_id",
    "orca_platform_account_id",
)


def _normalized(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().casefold())


def _load_view(root: DataLakeRoot, view_name: str) -> tuple[dict | None, dict | None]:
    core = root.path.joinpath(*SILVER_VAULT_CORE_PARTS)
    view_path = core / "query_tables" / f"{view_name}.json"
    manifest_path = core / "manifests" / f"{view_name}.json"
    view_exists = view_path.is_file()
    manifest_exists = manifest_path.is_file()
    if not view_exists and not manifest_exists:
        return None, None
    if not view_exists or not manifest_exists:
        raise ValueError(f"{view_name} generated view/manifest pair is incomplete")
    view_bytes = view_path.read_bytes()
    view = json.loads(view_bytes.decode("utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(view, dict) or not isinstance(manifest, dict):
        raise ValueError(f"{view_name} generated view/manifest must both be JSON objects")
    if view.get("view") != view_name or manifest.get("view") != view_name:
        raise ValueError(f"{view_name} generated view/manifest identity mismatch")
    if view.get("view_schema_version") != manifest.get("view_schema_version"):
        raise ValueError(f"{view_name} generated view/manifest schema mismatch")
    actual_sha256 = hashlib.sha256(view_bytes).hexdigest()
    if manifest.get("view_sha256") != actual_sha256:
        raise ValueError(f"{view_name} view_sha256 mismatch: manifest does not match stored view bytes")
    return view, manifest


def _load_account_envelope(
    root: DataLakeRoot,
    platform: str,
    platform_account_id: str,
) -> tuple[dict | None, dict | None]:
    creator_root = root.path.joinpath(*SILVER_VAULT_CREATOR_PARTS)
    envelope_path = creator_root / "accounts" / platform / platform_account_id / "envelope.json"
    manifest_path = creator_root / "manifests" / "accounts" / platform / f"{platform_account_id}.json"
    envelope_exists = envelope_path.is_file()
    manifest_exists = manifest_path.is_file()
    if not envelope_exists and not manifest_exists:
        return None, None
    if not envelope_exists or not manifest_exists:
        raise ValueError("Creator Vault account envelope/manifest pair is incomplete")
    envelope_bytes = envelope_path.read_bytes()
    envelope = json.loads(envelope_bytes.decode("utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(envelope, dict) or not isinstance(manifest, dict):
        raise ValueError("Creator Vault account envelope/manifest must be JSON objects")
    account_key = envelope.get("account_key")
    if (
        envelope.get("platform") != platform
        or not isinstance(account_key, dict)
        or account_key.get("platform_account_id") != platform_account_id
        or manifest.get("platform") != platform
        or manifest.get("platform_account_id") != platform_account_id
    ):
        raise ValueError("Creator Vault account envelope/manifest identity mismatch")
    if envelope.get("read_model_manifest_id") != manifest.get("read_model_manifest_id"):
        raise ValueError("Creator Vault account envelope/manifest generation mismatch")
    if manifest.get("envelope_sha256") != hashlib.sha256(envelope_bytes).hexdigest():
        raise ValueError("Creator Vault account envelope_sha256 mismatch")
    return envelope, manifest


def _provenance(manifest: dict | None) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        return {"manifest": "absent"}
    return {
        "generation_id": manifest.get("generation_id"),
        "generated_at": manifest.get("generated_at"),
        "source_high_watermark": manifest.get("source_high_watermark"),
        "selection_policy_versions": manifest.get("selection_policy_versions"),
        "stale_if": manifest.get("stale_if"),
    }


def _profile_for_match(
    profile_view: dict[str, Any] | None,
    *,
    platform: str,
    native_id: str,
    aliases: dict[str, Any],
) -> dict[str, Any] | None:
    if not isinstance(profile_view, dict):
        return None
    wrapper = profile_view.get("creator_profile_current_view")
    profiles = wrapper.get("profiles") if isinstance(wrapper, dict) else None
    if not isinstance(profiles, list):
        return None
    account_ids = {str(aliases[field]) for field in _ACCOUNT_ID_FIELDS if aliases.get(field)}
    exact: list[dict[str, Any]] = []
    handle_matches: list[dict[str, Any]] = []
    for profile in profiles:
        if not isinstance(profile, dict):
            continue
        for account in profile.get("platform_accounts", []):
            if not isinstance(account, dict) or _normalized(account.get("platform")) != _normalized(platform):
                continue
            if str(account.get("platform_account_id") or "") in account_ids:
                exact.append(profile)
            elif _normalized(account.get("public_handle")) == _normalized(native_id):
                handle_matches.append(profile)
    matches = exact or handle_matches
    unique = {str(row.get("profile_subject_id")): row for row in matches}
    if len(unique) > 1:
        raise ValueError("creator lookup matched multiple stable registry profiles")
    return next(iter(unique.values())) if unique else None


def _account_id_for_match(
    aliases: dict[str, Any],
    profile: dict[str, Any] | None,
    *,
    platform: str,
    native_id: str,
) -> str | None:
    values = {str(aliases[field]) for field in _ACCOUNT_ID_FIELDS if aliases.get(field)}
    if len(values) > 1:
        raise ValueError("creator lookup has conflicting platform account aliases")
    if values:
        return next(iter(values))
    if isinstance(profile, dict):
        matching = {
            str(account.get("platform_account_id"))
            for account in profile.get("platform_accounts", [])
            if isinstance(account, dict)
            and _normalized(account.get("platform")) == _normalized(platform)
            and _normalized(account.get("public_handle")) == _normalized(native_id)
            and account.get("platform_account_id")
        }
        if len(matching) > 1:
            raise ValueError("stable registry profile has conflicting platform account ids")
        if matching:
            return next(iter(matching))
    return None


def lookup_creator(
    root: DataLakeRoot,
    query: str,
    *,
    profile_view: dict[str, Any] | None = None,
) -> dict[str, Any]:
    view, manifest = _load_view(root, "by_creator")
    if view is None:
        return {
            "status": "view_not_built",
            "hint": "run runners/run_data_lake_indexes_rebuild.py --target derived_retrieval",
        }
    wanted = _normalized(query)
    namespace_filter = None
    if ":" in query:
        prefix, _, rest = query.partition(":")
        namespace_filter = _normalized(prefix)
        wanted = _normalized(rest)
    if not wanted:
        raise ValueError("creator query must contain a non-empty account id or alias")
    matches = []
    for namespace, kinds in view.get("creators", {}).items():
        if namespace_filter and _normalized(namespace) != namespace_filter:
            continue
        for identity_kind, ids in kinds.items():
            for native_id, entry in ids.items():
                aliases = entry.get("aliases", {})
                candidates = {_normalized(native_id)} | {_normalized(alias) for alias in aliases.values()}
                if wanted not in candidates:
                    continue
                profile = _profile_for_match(
                    profile_view,
                    platform=namespace,
                    native_id=native_id,
                    aliases=aliases,
                )
                account_id = _account_id_for_match(
                    aliases,
                    profile,
                    platform=namespace,
                    native_id=native_id,
                )
                envelope, envelope_manifest = (
                    _load_account_envelope(root, namespace, account_id)
                    if account_id is not None
                    else (None, None)
                )
                matches.append({
                    "namespace": namespace,
                    "identity_kind": identity_kind,
                    "native_id": native_id,
                    **entry,
                    "registry_profile_or_none": profile,
                    "creator_vault_account_or_none": envelope,
                    "current_profile_metrics_status": (
                        "generated" if envelope is not None else "not_captured_or_not_processed"
                    ),
                    "creator_vault_provenance": _provenance(envelope_manifest),
                })
    return {
        "status": "found" if matches else "not_found",
        "query": query,
        "matches": matches,
        "zero_rows_meaning": view.get("zero_rows_meaning"),
        "authority_note": view.get("semantics"),
        "view_provenance": _provenance(manifest),
    }


def lookup_mention(root: DataLakeRoot, query: str) -> dict[str, Any]:
    view, manifest = _load_view(root, "by_mention")
    if view is None:
        return {
            "status": "view_not_built",
            "hint": "run runners/run_data_lake_indexes_rebuild.py --target derived_retrieval",
        }
    wanted = _normalized(query)
    if not wanted:
        raise ValueError("mention query must contain a non-empty brand or line identity")
    matches: list[dict[str, Any]] = []
    for section in ("mentions", "native_product_pages"):
        for brand, lines in view.get(section, {}).items():
            for line, refs in lines.items():
                tokens = {_normalized(brand), _normalized(line), _normalized(f"{brand} {line}")}
                if wanted in tokens:
                    matches.append({"source_class": section, "brand": brand, "line": line, "refs": refs})
    return {
        "status": "found" if matches else "not_found",
        "query": query,
        "matches": matches,
        "zero_rows_meaning": view.get("zero_rows_meaning"),
        "authority_note": view.get("semantics"),
        "view_provenance": _provenance(manifest),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", "--data-root", dest="data_root", help="Explicit Forseti data root path (falls back to FORSETI_DATA_ROOT).")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY, help="Stable creator_profile_current JSON used for creator lookups.")
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--creator", help="Creator query: bare handle/account id, or namespace:native_id.")
    target.add_argument("--mention", help="Brand/line product entity query (normalized exact brand, line, or combined identity).")
    args = parser.parse_args(argv)
    try:
        root = DataLakeRoot.resolve_readonly(explicit=args.data_root)
        if args.creator is not None:
            profile_view = load_creator_profile_current_view(args.registry)
            result = lookup_creator(root, args.creator, profile_view=profile_view)
        else:
            result = lookup_mention(root, args.mention)
    except (DataLakeRootError, OSError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if result["status"] == "found":
        return 0
    if result["status"] == "not_found":
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())