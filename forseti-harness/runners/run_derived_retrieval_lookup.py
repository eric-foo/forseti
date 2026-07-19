"""Read-only creator/product lookup over stable identity and generated views.

Creator lookup starts from the stable Git-backed creator_profile_current row
and joins its Creator Vault account envelope directly. The envelope remains a
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
    PLATFORM_ACCOUNT_ID_ALIAS_FIELDS,
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
_ACCOUNT_ID_FIELDS = PLATFORM_ACCOUNT_ID_ALIAS_FIELDS
_SAFE_ACCOUNT_KEY = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")


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
    if _SAFE_ACCOUNT_KEY.fullmatch(platform_account_id) is None:
        raise ValueError("stable registry platform account id is not a safe read-model key")
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


def _load_unfiled_accounts(
    root: DataLakeRoot,
) -> tuple[list[dict[str, Any]], dict | None]:
    creator_root = root.path.joinpath(*SILVER_VAULT_CREATOR_PARTS)
    view_path = creator_root / "unfiled_accounts.json"
    manifest_path = creator_root / "manifests" / "unfiled_accounts.json"
    view_exists = view_path.is_file()
    manifest_exists = manifest_path.is_file()
    if not view_exists and not manifest_exists:
        return [], None
    if not view_exists or not manifest_exists:
        raise ValueError("Creator Vault unfiled-account view/manifest pair is incomplete")
    view_bytes = view_path.read_bytes()
    view = json.loads(view_bytes.decode("utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    residuals = view.get("residuals") if isinstance(view, dict) else None
    if (
        not isinstance(view, dict)
        or not isinstance(manifest, dict)
        or view.get("view") != "creator_vault_unfiled_accounts"
        or manifest.get("view") != view.get("view")
        or view.get("generation_id") != manifest.get("generation_id")
        or not isinstance(residuals, list)
        or any(not isinstance(row, dict) for row in residuals)
    ):
        raise ValueError("Creator Vault unfiled-account view/manifest is invalid")
    if manifest.get("view_sha256") != hashlib.sha256(view_bytes).hexdigest():
        raise ValueError("Creator Vault unfiled-account view_sha256 mismatch")
    return residuals, manifest


def _provenance(manifest: dict | None) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        return {"manifest": "absent"}
    return {
        "generation_id": manifest.get("generation_id"),
        "generated_at": manifest.get("generated_at"),
        "source_ref_set_fingerprint_sha256": manifest.get(
            "source_ref_set_fingerprint_sha256"
        ),
        "source_high_watermark": manifest.get("source_high_watermark"),
        "selection_policy_versions": manifest.get("selection_policy_versions"),
        "stale_if": manifest.get("stale_if"),
    }


def _parse_creator_query(query: str) -> tuple[str | None, str]:
    namespace_filter = None
    value = query
    if ":" in query:
        prefix, _, value = query.partition(":")
        namespace_filter = _normalized(prefix)
    wanted = _normalized(value).lstrip("@")
    if not wanted:
        raise ValueError("creator query must contain a non-empty account id or alias")
    return namespace_filter, wanted


def _registry_matches(
    profile_view: dict[str, Any] | None,
    *,
    namespace_filter: str | None,
    wanted: str,
) -> list[dict[str, Any]]:
    if not isinstance(profile_view, dict):
        return []
    wrapper = profile_view.get("creator_profile_current_view")
    profiles = wrapper.get("profiles") if isinstance(wrapper, dict) else None
    if not isinstance(profiles, list):
        return []
    matches: dict[tuple[str, str, str], dict[str, Any]] = {}
    for profile in profiles:
        if not isinstance(profile, dict):
            continue
        profile_subject_id = str(profile.get("profile_subject_id") or "")
        for account in profile.get("platform_accounts", []):
            if not isinstance(account, dict):
                continue
            platform = _normalized(account.get("platform"))
            if not platform or (namespace_filter and platform != namespace_filter):
                continue
            account_id = str(account.get("platform_account_id") or "").strip()
            public_handle = str(account.get("public_handle") or "").strip()
            tokens = {
                _normalized(account_id).lstrip("@"),
                _normalized(public_handle).lstrip("@"),
            }
            tokens.update(
                _normalized(account.get(field)).lstrip("@")
                for field in PLATFORM_ACCOUNT_ID_ALIAS_FIELDS
                if account.get(field)
            )
            tokens.discard("")
            if wanted not in tokens:
                continue
            key = (profile_subject_id, platform, account_id)
            matches[key] = {
                "platform": platform,
                "platform_account_id": account_id,
                "public_handle": public_handle,
                "profile": profile,
            }
    return [matches[key] for key in sorted(matches)]


def _matching_unfiled_residuals(
    residuals: list[dict[str, Any]],
    *,
    platform: str,
    platform_account_id: str,
    public_handle: str,
) -> list[dict[str, Any]]:
    wanted_ids = {
        _normalized(platform_account_id).lstrip("@"),
        _normalized(public_handle).lstrip("@"),
    }
    wanted_ids.discard("")
    return [
        residual
        for residual in residuals
        if _normalized(residual.get("platform")) == _normalized(platform)
        and (
            _normalized(residual.get("native_id")).lstrip("@") in wanted_ids
            or any(
                _normalized(value).lstrip("@") in wanted_ids
                for value in residual.get("platform_account_ids", [])
            )
        )
    ]


def lookup_creator(
    root: DataLakeRoot,
    query: str,
    *,
    profile_view: dict[str, Any] | None = None,
) -> dict[str, Any]:
    namespace_filter, wanted = _parse_creator_query(query)
    registry_matches = _registry_matches(
        profile_view,
        namespace_filter=namespace_filter,
        wanted=wanted,
    )
    if not registry_matches:
        return {
            "status": "unknown_to_registry",
            "query": query,
            "matches": [],
            "zero_rows_meaning": (
                "the stable creator registry has no matching platform account; "
                "this does not assert that Silver lacks evidence"
            ),
        }
    if len(registry_matches) > 1:
        return {
            "status": "conflicted",
            "query": query,
            "matches": [],
            "registry_candidates": [
                {
                    "profile_subject_id": row["profile"].get("profile_subject_id"),
                    "platform": row["platform"],
                    "platform_account_id": row["platform_account_id"],
                    "public_handle": row["public_handle"],
                }
                for row in registry_matches
            ],
            "reason": "creator query matched multiple stable registry accounts",
        }

    registry_match = registry_matches[0]
    platform = registry_match["platform"]
    account_id = registry_match["platform_account_id"]
    if not account_id:
        return {
            "status": "conflicted",
            "query": query,
            "matches": [],
            "reason": "stable registry account is missing platform_account_id",
        }
    unfiled, unfiled_manifest = _load_unfiled_accounts(root)
    matching_residuals = _matching_unfiled_residuals(
        unfiled,
        platform=platform,
        platform_account_id=account_id,
        public_handle=registry_match["public_handle"],
    )
    envelope, envelope_manifest = (
        _load_account_envelope(root, platform, account_id)
        if _SAFE_ACCOUNT_KEY.fullmatch(account_id) is not None
        else (None, None)
    )
    metrics_status = (
        "generated"
        if envelope is not None
        else "captured_but_unfileable"
        if matching_residuals
        else "not_captured_or_not_processed"
    )
    match = {
        "namespace": platform,
        "identity_kind": "stable_registry_platform_account",
        "native_id": registry_match["public_handle"],
        "aliases": {"platform_account_id": account_id},
        "registry_profile_or_none": registry_match["profile"],
        "creator_vault_account_or_none": envelope,
        "current_profile_metrics_status": metrics_status,
        "creator_vault_residuals": matching_residuals,
        "creator_vault_provenance": _provenance(envelope_manifest),
        "creator_vault_residual_provenance": _provenance(unfiled_manifest),
    }
    return {
        "status": "found",
        "query": query,
        "matches": [match],
        "zero_rows_meaning": (
            "an absent Creator Vault envelope means metrics were not captured, not "
            "processed, or were explicitly unfileable; it never means zero"
        ),
        "authority_note": (
            "stable registry identity joined to a rebuildable Creator Vault metric "
            "summary; Silver remains metric authority"
        ),
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
    if result["status"] in {"not_found", "unknown_to_registry"}:
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())