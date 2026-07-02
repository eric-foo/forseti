"""Build the static creator-profile-current view from sibling source ledgers."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Sequence

from capture_spine.creator_profile_current.validation import (
    CREATOR_PROFILE_CURRENT_VIEW_SCHEMA_VERSION,
    validate_creator_profile_current_view,
)


WRAPPER_KEY = "creator_profile_current_view"
ACCOUNT_LEDGER_POINTER = (
    "orca/product/spines/capture/core/source_families/social_media/creator_registry/"
    "creator_public_handle_linkage_ledger_v0.json"
)
YOUTUBE_METRIC_SEED_POINTER = (
    "orca/product/spines/capture/core/source_families/social_media/youtube/"
    "youtube_shorts_fragrance_creator_metric_seed_v0.json"
)
INSTAGRAM_METRIC_SEED_POINTER = (
    "orca/product/spines/capture/core/source_families/social_media/instagram/"
    "instagram_reels_creator_metric_seed_v0.json"
)
INSTAGRAM_SNAPSHOT_POINTER = (
    "orca/product/spines/capture/core/source_families/social_media/instagram/"
    "instagram_reels_creator_metric_rollup_snapshot_v0.json"
)
YOUTUBE_SNAPSHOT_POINTER = (
    "orca/product/spines/capture/core/source_families/social_media/youtube/"
    "youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json"
)

# Lake cut-over §5/§8: both Instagram and YouTube rollups are read from the
# committed lake SNAPSHOT (value-equal to the retained seed, which stays as the
# no-drift oracle). The seed entries are retained so the equivalence/oracle
# paths can still materialize from them.
_METRIC_SEED_CONFIG_BY_NAME = {
    "youtube_shorts_fragrance_creator_metric_seed_v0.json": {
        "wrapper": "youtube_shorts_fragrance_creator_metric_seed",
        "pointer": YOUTUBE_METRIC_SEED_POINTER,
        "role": "source-backed metric observations and admitted-pool YouTube metric rollups",
    },
    "youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json": {
        "wrapper": "creator_metric_rollup_snapshot",
        "pointer": YOUTUBE_SNAPSHOT_POINTER,
        "role": "lake-backed admitted-pool YouTube metric rollups (live-lake snapshot)",
    },
    "instagram_reels_creator_metric_rollup_snapshot_v0.json": {
        "wrapper": "creator_metric_rollup_snapshot",
        "pointer": INSTAGRAM_SNAPSHOT_POINTER,
        "role": "lake-backed selected-grid Instagram metric rollups (live-lake snapshot)",
    },
    "instagram_reels_creator_metric_seed_v0.json": {
        "wrapper": "instagram_reels_creator_metric_seed",
        "pointer": INSTAGRAM_METRIC_SEED_POINTER,
        "role": "source-backed metric observations and selected-grid Instagram metric rollups",
    },
}

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
    metric_seed_path: str | Path | None = None,
    metric_seed_paths: Sequence[str | Path] | None = None,
    generated_at_utc: str,
) -> dict[str, Any]:
    account_path = Path(account_ledger_path)
    account_document = load_json(account_path)
    metric_paths = _normalize_metric_seed_paths(metric_seed_path=metric_seed_path, metric_seed_paths=metric_seed_paths)
    metric_seed_inputs = [_load_metric_seed_input(path) for path in metric_paths]
    return build_creator_profile_current_view_document(
        account_ledger=account_document["creator_public_handle_linkage_ledger"],
        metric_seeds=[seed_input["seed"] for seed_input in metric_seed_inputs],
        generated_at_utc=generated_at_utc,
        source_input_hashes={
            ACCOUNT_LEDGER_POINTER: _sha256_repo_text(account_path),
            **{
                seed_input["pointer"]: _sha256_repo_text(seed_input["path"])
                for seed_input in metric_seed_inputs
            },
        },
        metric_seed_inputs=metric_seed_inputs,
    )


def build_creator_profile_current_view_document(
    *,
    account_ledger: dict[str, Any],
    metric_seed: dict[str, Any] | None = None,
    metric_seeds: Sequence[dict[str, Any]] | None = None,
    generated_at_utc: str,
    source_input_hashes: dict[str, str],
    metric_seed_inputs: Sequence[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    accounts = account_ledger["platform_accounts"]
    seeds = _normalize_metric_seeds(metric_seed=metric_seed, metric_seeds=metric_seeds)
    rollup_records = _collect_metric_rollup_records(seeds, metric_seed_inputs)
    accounts_by_id = {account["platform_account_id"]: account for account in accounts}
    rollups_by_subject = {record["rollup"]["profile_subject_id"]: record for record in rollup_records}
    if len(rollups_by_subject) != len(rollup_records):
        duplicate_subjects = sorted(
            {
                record["rollup"]["profile_subject_id"]
                for record in rollup_records
                if sum(
                    1
                    for other in rollup_records
                    if other["rollup"]["profile_subject_id"] == record["rollup"]["profile_subject_id"]
                )
                > 1
            }
        )
        raise ValueError(f"creator profile materialization received duplicate metric rollups: {duplicate_subjects!r}")
    if set(accounts_by_id) != set(rollups_by_subject):
        missing_rollups = sorted(set(accounts_by_id) - set(rollups_by_subject))
        missing_accounts = sorted(set(rollups_by_subject) - set(accounts_by_id))
        raise ValueError(
            "creator profile materialization requires one metric rollup per platform account; "
            f"missing_rollups={missing_rollups!r}; missing_accounts={missing_accounts!r}"
        )

    account_index = {account["platform_account_id"]: index for index, account in enumerate(accounts)}
    rollup_index = {record["rollup"]["profile_subject_id"]: record["rollup_index"] for record in rollup_records}
    profiles = [
        _build_platform_account_profile(
            account=account,
            account_index=account_index[account["platform_account_id"]],
            rollup=rollups_by_subject[account["platform_account_id"]]["rollup"],
            rollup_index=rollup_index[account["platform_account_id"]],
            metric_source_pointer=rollups_by_subject[account["platform_account_id"]]["pointer"],
            metric_source_wrapper=rollups_by_subject[account["platform_account_id"]]["wrapper"],
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
            "platform-account ledger and platform creator metric seeds. Profiles "
            "are account-scoped unless promoted public-handle linkage exists."
        ),
        "authority_pointers": [
            "orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md",
            "orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md",
            "orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md",
        ],
        "source_inputs": [
            {
                "source_pointer": ACCOUNT_LEDGER_POINTER,
                "sha256": source_input_hashes[ACCOUNT_LEDGER_POINTER],
                "role": "source-backed platform accounts and identity state",
            },
            *[
                {
                    "source_pointer": seed_input["pointer"],
                    "sha256": source_input_hashes[seed_input["pointer"]],
                    "role": seed_input["role"],
                }
                for seed_input in _metric_seed_inputs_for_source_list(seeds, metric_seed_inputs)
            ],
        ],
        "counts": _counts(profiles),
        "profiles": profiles,
        "accepted_residuals": [
            "Profiles are static JSON export rows, not a runtime database or dashboard.",
            "Current rows are platform_account subjects; creator_record subjects remain absent until promoted cross-platform linkage exists.",
            "Aggregate views are admitted-pool or selected-grid rollups, not full-channel or all-content creator averages.",
            "Engagement inputs remain platform/source limited; missing inputs stay explicit missingness rather than zero-filled metrics.",
        ],
        "non_claims": [
            "not SQLite adoption",
            "not data-lake physicalization",
            "not dashboard implementation",
            "not buyer proof",
            "not live capture authorization",
            "not cross-platform identity proof",
            "not universal engagement-rate support",
            "not channel-wide influence",
        ],
    }
    document = {WRAPPER_KEY: wrapper}
    validate_creator_profile_current_view(document)
    return document


def dump_creator_profile_current_view(document: dict[str, Any]) -> str:
    # Canonical key ordering (sort_keys=True) so the serialized view is stable
    # regardless of the source rollups' internal key order. Lake cut-over §5
    # prerequisite: rollups lifted from canonical Silver records carry sorted
    # nested keys while the hand-authored seed's order is arbitrary, and
    # _profile_rollup deep-copies those nested dicts into the view -- without this,
    # re-pointing materialize from the seed onto the snapshot would reorder nested
    # metric keys and spuriously change the committed view's bytes.
    return json.dumps(document, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def _build_platform_account_profile(
    *,
    account: dict[str, Any],
    account_index: int,
    rollup: dict[str, Any],
    rollup_index: int,
    metric_source_pointer: str,
    metric_source_wrapper: str,
    generated_at_utc: str,
) -> dict[str, Any]:
    account_id = account["platform_account_id"]
    platform = account["platform"]
    metric_rollup_pointer = f"{metric_source_pointer}#/{metric_source_wrapper}/metric_rollups/{rollup_index}"
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
                f"Single-platform {platform} public account observed from source-backed "
                "creator metric or observation rows; no promoted cross-platform public-handle "
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
            "metric_snapshot_pointer": metric_source_pointer,
            "source_metric_observation_ids": deepcopy(rollup["source_metric_observation_ids"]),
        },
        "limitations": _profile_limitations(platform=platform, rollup=rollup),
        "non_claims": [
            "not channel-wide creator influence",
            "not platform-wide engagement rate",
            "not buyer proof",
            "not public person-level identity",
            "not contact or outreach authorization",
            "not cross-platform rollup",
            "not dashboard readiness",
            "not SQLite or data-lake physicalization",
        ],
    }


def _profile_limitations(*, platform: str, rollup: dict[str, Any]) -> list[str]:
    engagement = rollup["metric_rollups"]["engagement_rate"]
    if engagement["posture"] == "observed":
        engagement_limitation = (
            "Engagement rate is source-backed only for the admitted/selected source pool; "
            "it is not a platform-wide engagement benchmark."
        )
    else:
        engagement_limitation = (
            "Engagement rate, average likes, and average total comments are unavailable until "
            "source-backed numerator fields exist."
        )
    return [
        f"Profile is account-scoped to one {platform} platform account; it is not a linked creator_record.",
        "Metric rollup covers the admitted/selected source pool only; it is not a channel-wide average.",
        engagement_limitation,
        "Ideal/content-fit audience profile is not joined in this static view.",
        "Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.",
        "Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.",
        "The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.",
    ]


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


def _normalize_metric_seed_paths(
    *,
    metric_seed_path: str | Path | None,
    metric_seed_paths: Sequence[str | Path] | None,
) -> list[Path]:
    if metric_seed_path is not None and metric_seed_paths is not None:
        raise ValueError("provide either metric_seed_path or metric_seed_paths, not both")
    if metric_seed_paths is not None:
        paths = [Path(path) for path in metric_seed_paths]
    elif metric_seed_path is not None:
        paths = [Path(metric_seed_path)]
    else:
        raise ValueError("at least one metric seed path is required")
    if not paths:
        raise ValueError("at least one metric seed path is required")
    return paths


def _load_metric_seed_input(path: Path) -> dict[str, Any]:
    config = _METRIC_SEED_CONFIG_BY_NAME.get(path.name)
    if config is None:
        raise ValueError(f"unsupported metric seed file: {path}")
    document = load_json(path)
    wrapper = config["wrapper"]
    if wrapper not in document:
        raise ValueError(f"metric seed file missing wrapper {wrapper!r}: {path}")
    return {
        "path": path,
        "seed": document[wrapper],
        "wrapper": wrapper,
        "pointer": config["pointer"],
        "role": config["role"],
    }


def _normalize_metric_seeds(
    *,
    metric_seed: dict[str, Any] | None,
    metric_seeds: Sequence[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    if metric_seed is not None and metric_seeds is not None:
        raise ValueError("provide either metric_seed or metric_seeds, not both")
    if metric_seeds is not None:
        seeds = list(metric_seeds)
    elif metric_seed is not None:
        seeds = [metric_seed]
    else:
        raise ValueError("at least one metric seed is required")
    if not seeds:
        raise ValueError("at least one metric seed is required")
    return seeds


def _metric_seed_inputs_for_source_list(
    seeds: Sequence[dict[str, Any]],
    metric_seed_inputs: Sequence[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    if metric_seed_inputs is not None:
        return list(metric_seed_inputs)
    if len(seeds) == 1:
        return [
            {
                "wrapper": "youtube_shorts_fragrance_creator_metric_seed",
                "pointer": YOUTUBE_METRIC_SEED_POINTER,
                "role": _METRIC_SEED_CONFIG_BY_NAME["youtube_shorts_fragrance_creator_metric_seed_v0.json"]["role"],
            }
        ]
    raise ValueError("metric_seed_inputs are required when materializing multiple in-memory seeds")


def _collect_metric_rollup_records(
    seeds: Sequence[dict[str, Any]],
    metric_seed_inputs: Sequence[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    seed_inputs = _metric_seed_inputs_for_source_list(seeds, metric_seed_inputs)
    if len(seed_inputs) != len(seeds):
        raise ValueError("metric_seed_inputs length must match metric_seeds length")
    records: list[dict[str, Any]] = []
    for seed, seed_input in zip(seeds, seed_inputs, strict=True):
        rollups = seed["metric_rollups"]
        for index, rollup in enumerate(rollups):
            records.append(
                {
                    "rollup": rollup,
                    "rollup_index": index,
                    "pointer": seed_input["pointer"],
                    "wrapper": seed_input["wrapper"],
                }
            )
    return records


def _sha256_repo_text(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
