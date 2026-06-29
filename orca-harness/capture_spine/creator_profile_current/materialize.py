"""Build the static creator-profile-current view from sibling source ledgers."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from capture_spine.creator_profile_current.validation import (
    CREATOR_PROFILE_CURRENT_VIEW_SCHEMA_VERSION,
    validate_creator_profile_current_view,
)


WRAPPER_KEY = "creator_profile_current_view"
ACCOUNT_LEDGER_POINTER = (
    "orca/product/spines/capture/core/source_families/social_media/"
    "creator_public_handle_linkage_ledger_v0.json"
)
YOUTUBE_METRIC_SEED_POINTER = (
    "orca/product/spines/capture/core/source_families/social_media/youtube/"
    "youtube_shorts_fragrance_creator_metric_seed_v0.json"
)

_PROFILE_ROLLUP_FIELDS = (
    "metric_rollup_id",
    "platform_scope",
    "platform_account_ids",
    "rollup_window",
    "rollup_window_description",
    "content_kind_inclusion_rule",
    "metric_rollups",
    "source_metric_observation_ids",
    "observation_count",
    "view_count_min",
    "view_count_max",
    "calculation_recipe_version",
    "computed_at",
    "freshness_state",
    "limitations",
    "sample_support",
)


def load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON document must be an object: {path}")
    return value


def build_creator_profile_current_view_from_files(
    *,
    account_ledger_path: str | Path,
    metric_seed_path: str | Path,
    generated_at_utc: str,
) -> dict[str, Any]:
    account_path = Path(account_ledger_path)
    metric_path = Path(metric_seed_path)
    account_document = load_json(account_path)
    metric_seed_document = load_json(metric_path)
    return build_creator_profile_current_view_document(
        account_ledger=account_document["creator_public_handle_linkage_ledger"],
        metric_seed=metric_seed_document["youtube_shorts_fragrance_creator_metric_seed"],
        generated_at_utc=generated_at_utc,
        source_input_hashes={
            ACCOUNT_LEDGER_POINTER: _sha256_repo_text(account_path),
            YOUTUBE_METRIC_SEED_POINTER: _sha256_repo_text(metric_path),
        },
    )


def build_creator_profile_current_view_document(
    *,
    account_ledger: dict[str, Any],
    metric_seed: dict[str, Any],
    generated_at_utc: str,
    source_input_hashes: dict[str, str],
) -> dict[str, Any]:
    accounts = account_ledger["platform_accounts"]
    rollups = metric_seed["metric_rollups"]
    accounts_by_id = {account["platform_account_id"]: account for account in accounts}
    rollups_by_subject = {rollup["profile_subject_id"]: rollup for rollup in rollups}
    if set(accounts_by_id) != set(rollups_by_subject):
        missing_rollups = sorted(set(accounts_by_id) - set(rollups_by_subject))
        missing_accounts = sorted(set(rollups_by_subject) - set(accounts_by_id))
        raise ValueError(
            "creator profile materialization requires one metric rollup per platform account; "
            f"missing_rollups={missing_rollups!r}; missing_accounts={missing_accounts!r}"
        )

    account_index = {account["platform_account_id"]: index for index, account in enumerate(accounts)}
    rollup_index = {rollup["profile_subject_id"]: index for index, rollup in enumerate(rollups)}
    profiles = [
        _build_platform_account_profile(
            account=account,
            account_index=account_index[account["platform_account_id"]],
            rollup=rollups_by_subject[account["platform_account_id"]],
            rollup_index=rollup_index[account["platform_account_id"]],
            generated_at_utc=generated_at_utc,
        )
        for account in accounts
    ]

    wrapper = {
        "schema_version": CREATOR_PROFILE_CURRENT_VIEW_SCHEMA_VERSION,
        "view_id": "creator_profile_current_view_v0",
        "view_mode": "source_backed_static_json_export",
        "generated_at_utc": generated_at_utc,
        "source_policy_posture": (
            "Static creator-profile-current export derived from the public-handle "
            "platform-account ledger and the YouTube creator metric seed. Profiles "
            "are account-scoped unless promoted public-handle linkage exists."
        ),
        "authority_pointers": [
            "orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md",
            "orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md",
            "orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md",
        ],
        "source_inputs": [
            {
                "source_pointer": ACCOUNT_LEDGER_POINTER,
                "sha256": source_input_hashes[ACCOUNT_LEDGER_POINTER],
                "role": "source-backed platform accounts and identity state",
            },
            {
                "source_pointer": YOUTUBE_METRIC_SEED_POINTER,
                "sha256": source_input_hashes[YOUTUBE_METRIC_SEED_POINTER],
                "role": "source-backed metric observations and admitted-pool metric rollups",
            },
        ],
        "counts": _counts(profiles),
        "profiles": profiles,
        "accepted_residuals": [
            "Profiles are static JSON export rows, not a runtime database or dashboard.",
            "All current rows are YouTube platform_account subjects; creator_record subjects remain absent until promoted cross-platform linkage exists.",
            "Aggregate views are admitted-pool rollups, not full-channel or all-content creator averages.",
            "Missing engagement inputs remain explicit missingness rather than zero-filled metrics.",
        ],
        "non_claims": [
            "not SQLite adoption",
            "not data-lake physicalization",
            "not dashboard implementation",
            "not buyer proof",
            "not live capture authorization",
            "not cross-platform identity proof",
            "not engagement-rate support",
            "not channel-wide influence",
        ],
    }
    document = {WRAPPER_KEY: wrapper}
    validate_creator_profile_current_view(document)
    return document


def dump_creator_profile_current_view(document: dict[str, Any]) -> str:
    return json.dumps(document, indent=2, ensure_ascii=False) + "\n"


def _build_platform_account_profile(
    *,
    account: dict[str, Any],
    account_index: int,
    rollup: dict[str, Any],
    rollup_index: int,
    generated_at_utc: str,
) -> dict[str, Any]:
    account_id = account["platform_account_id"]
    metric_rollup_pointer = f"{YOUTUBE_METRIC_SEED_POINTER}#/youtube_shorts_fragrance_creator_metric_seed/metric_rollups/{rollup_index}"
    source_pointers = [account["handle_source_pointer"]]
    display_pointer = account.get("display_name_source_pointer_or_none")
    if display_pointer:
        source_pointers.append(display_pointer)

    return {
        "profile_subject_kind": "platform_account",
        "profile_subject_id": account_id,
        "platform_account_id_or_none": account_id,
        "creator_record_id_or_none": None,
        "identity_state": "single_platform_observed",
        "link_state_or_none": None,
        "review_state_or_none": None,
        "platform_accounts": [deepcopy(account)],
        "identity_evidence_summary": {
            "summary": (
                "Single-platform YouTube public account observed from source-backed "
                "creator observation rows; no promoted cross-platform public-handle "
                "linkage exists in this ledger."
            ),
            "account_pointer": (
                f"{ACCOUNT_LEDGER_POINTER}#/creator_public_handle_linkage_ledger/"
                f"platform_accounts/{account_index}"
            ),
            "source_pointers": source_pointers,
        },
        "current_metric_rollups": [_profile_rollup(rollup, metric_rollup_pointer)],
        "ideal_audience_profile": None,
        "wind_calling_summary": None,
        "freshness": {
            "identity_updated_at": account["handle_observed_at"],
            "metrics_computed_at_or_none": rollup["computed_at"],
            "audience_computed_at_or_none": None,
            "profile_view_computed_at": generated_at_utc,
        },
        "source_drill_back": {
            "identity_ledger_pointer": (
                f"{ACCOUNT_LEDGER_POINTER}#/creator_public_handle_linkage_ledger/"
                f"platform_accounts/{account_index}"
            ),
            "metric_rollup_pointer": metric_rollup_pointer,
            "metric_seed_pointer": YOUTUBE_METRIC_SEED_POINTER,
            "source_metric_observation_ids": deepcopy(rollup["source_metric_observation_ids"]),
        },
        "limitations": [
            "Profile is account-scoped to one YouTube platform account; it is not a linked creator_record.",
            "Metric rollup covers the admitted fragrance Shorts source pool only; it is not a channel-wide average.",
            "Engagement rate, average likes, and average total comments are unavailable until source-backed numerator fields exist.",
            "Ideal/content-fit audience profile is not joined in this static view.",
            "Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.",
            "Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.",
            "The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.",
        ],
        "non_claims": [
            "not channel-wide creator influence",
            "not engagement rate",
            "not buyer proof",
            "not public person-level identity",
            "not contact or outreach authorization",
            "not cross-platform rollup",
            "not dashboard readiness",
            "not SQLite or data-lake physicalization",
        ],
    }


def _profile_rollup(rollup: dict[str, Any], metric_rollup_pointer: str) -> dict[str, Any]:
    profile_rollup = {"metric_rollup_id": rollup["metric_rollup_id"], "metric_rollup_pointer": metric_rollup_pointer}
    for field in _PROFILE_ROLLUP_FIELDS:
        if field == "metric_rollup_id":
            continue
        profile_rollup[field] = deepcopy(rollup[field])
    return profile_rollup


def _counts(profiles: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "profiles_total": len(profiles),
        "platform_account_profiles": sum(1 for profile in profiles if profile["profile_subject_kind"] == "platform_account"),
        "creator_record_profiles": sum(1 for profile in profiles if profile["profile_subject_kind"] == "creator_record"),
        "profiles_with_metric_rollups": sum(1 for profile in profiles if profile["current_metric_rollups"]),
        "profiles_with_ideal_audience_profiles": sum(1 for profile in profiles if profile["ideal_audience_profile"] is not None),
        "engagement_rate_observed_profiles": sum(
            1
            for profile in profiles
            if any(
                rollup["metric_rollups"]["engagement_rate"]["posture"] == "observed"
                for rollup in profile["current_metric_rollups"]
            )
        ),
        "cross_platform_rollup_profiles": sum(
            1
            for profile in profiles
            if any(rollup["platform_scope"] == "cross_platform" for rollup in profile["current_metric_rollups"])
        ),
    }


def _sha256_repo_text(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
