"""Build creator-profile-current from identity, onboarding, and metric sources."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any, Sequence

from capture_spine.creator_profile_current.audience_triangulation_snapshot import (
    SNAPSHOT_WRAPPER_KEY as AUDIENCE_SNAPSHOT_WRAPPER_KEY,
    load_creator_audience_triangulation_snapshot_document,
)
from capture_spine.creator_profile_current.validation import (
    CREATOR_PROFILE_CURRENT_VIEW_SCHEMA_VERSION,
    validate_creator_profile_current_view,
)

from schemas.creator_audience_models import CreatorAudienceJudgmentOutcomeV1
from schemas.tiktok_audience_evidence_models import CreatorAudienceJudgmentOutcome



WRAPPER_KEY = "creator_profile_current_view"
ACCOUNT_LEDGER_POINTER = (
    "forseti/product/spines/capture/core/source_families/social_media/creator_registry/"
    "creator_public_handle_linkage_ledger_v0.json"
)
CREATOR_REGISTRY_INDEX_POINTER = (
    "forseti/product/spines/capture/core/source_families/social_media/creator_registry/"
    "creator_registry_index_v0.json"
)
YOUTUBE_METRIC_SEED_POINTER = (
    "forseti/product/spines/capture/core/source_families/social_media/youtube/"
    "youtube_shorts_fragrance_creator_metric_seed_v0.json"
)
INSTAGRAM_METRIC_SEED_POINTER = (
    "forseti/product/spines/capture/core/source_families/social_media/instagram/"
    "instagram_reels_creator_metric_seed_v0.json"
)
INSTAGRAM_SNAPSHOT_POINTER = (
    "forseti/product/spines/capture/core/source_families/social_media/instagram/"
    "instagram_reels_creator_metric_rollup_snapshot_v0.json"
)
YOUTUBE_SNAPSHOT_POINTER = (
    "forseti/product/spines/capture/core/source_families/social_media/youtube/"
    "youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json"
)
TIKTOK_SNAPSHOT_POINTER = (
    "forseti/product/spines/capture/core/source_families/social_media/tiktok/"
    "tiktok_profile_grid_creator_metric_rollup_snapshot_v0.json"
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
    # TikTok has no committed seed JSON (its metric document is built live from
    # batch-admission lake packets); the snapshot is its only committed artifact.
    "tiktok_profile_grid_creator_metric_rollup_snapshot_v0.json": {
        "wrapper": "creator_metric_rollup_snapshot",
        "pointer": TIKTOK_SNAPSHOT_POINTER,
        "role": "lake-backed profile-grid TikTok metric rollups (live-lake snapshot)",
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
    creator_registry_index_path: str | Path,
    metric_seed_path: str | Path | None = None,
    metric_seed_paths: Sequence[str | Path] | None = None,
    audience_triangulation_snapshot_path: str | Path | None = None,
    audience_triangulation_snapshot_paths: Sequence[str | Path] | None = None,
    audience_judgment_outcome_path: str | Path | None = None,
    audience_judgment_outcome_paths: Sequence[str | Path] | None = None,
    generated_at_utc: str,
) -> dict[str, Any]:
    account_path = Path(account_ledger_path)
    registry_index_path = Path(creator_registry_index_path)
    account_document = load_json(account_path)
    registry_document = load_json(registry_index_path)
    onboarding_by_account = _onboarding_by_account_from_registry(registry_document)
    metric_paths = _normalize_metric_seed_paths(metric_seed_path=metric_seed_path, metric_seed_paths=metric_seed_paths)
    metric_seed_inputs = [_load_metric_seed_input(path) for path in metric_paths]
    audience_paths = _normalize_audience_snapshot_paths(
        audience_triangulation_snapshot_path=audience_triangulation_snapshot_path,
        audience_triangulation_snapshot_paths=audience_triangulation_snapshot_paths,
    )
    audience_snapshot_inputs = [_load_audience_snapshot_input(path) for path in audience_paths]
    audience_outcome_paths = _normalize_audience_outcome_paths(
        audience_judgment_outcome_path=audience_judgment_outcome_path,
        audience_judgment_outcome_paths=audience_judgment_outcome_paths,
    )
    verify_audience_judgment_outcomes(audience_paths, audience_outcome_paths)

    return build_creator_profile_current_view_document(
        account_ledger=account_document["creator_public_handle_linkage_ledger"],
        onboarding_by_account=onboarding_by_account,
        metric_seeds=[seed_input["seed"] for seed_input in metric_seed_inputs],
        audience_triangulation_snapshots=[
            snapshot
            for snapshot_input in audience_snapshot_inputs
            for snapshot in snapshot_input["snapshots"]
        ],
        generated_at_utc=generated_at_utc,
        source_input_hashes={
            ACCOUNT_LEDGER_POINTER: _sha256_repo_text(account_path),
            CREATOR_REGISTRY_INDEX_POINTER: _sha256_repo_text(registry_index_path),
            **{
                seed_input["pointer"]: _sha256_repo_text(seed_input["path"])
                for seed_input in metric_seed_inputs
            },
            **{
                snapshot_input["pointer"]: _sha256_repo_text(snapshot_input["path"])
                for snapshot_input in audience_snapshot_inputs
            },
        },
        metric_seed_inputs=metric_seed_inputs,
        audience_snapshot_inputs=audience_snapshot_inputs,
    )


def build_creator_profile_current_view_document(
    *,
    account_ledger: dict[str, Any],
    onboarding_by_account: Mapping[str, Mapping[str, Any]],
    metric_seed: dict[str, Any] | None = None,
    metric_seeds: Sequence[dict[str, Any]] | None = None,
    audience_triangulation_snapshots: Sequence[dict[str, Any]] | None = None,
    generated_at_utc: str,
    source_input_hashes: dict[str, str],
    metric_seed_inputs: Sequence[dict[str, Any]] | None = None,
    audience_snapshot_inputs: Sequence[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    accounts = account_ledger["platform_accounts"]
    seeds = _normalize_metric_seeds(metric_seed=metric_seed, metric_seeds=metric_seeds)
    rollup_records = _collect_metric_rollup_records(seeds, metric_seed_inputs)
    accounts_by_id = {account["platform_account_id"]: account for account in accounts}
    if set(onboarding_by_account) != set(accounts_by_id):
        raise ValueError(
            "Creator Registry onboarding rows must exactly match linkage-ledger accounts; "
            f"missing={sorted(set(accounts_by_id) - set(onboarding_by_account))!r}, "
            f"extra={sorted(set(onboarding_by_account) - set(accounts_by_id))!r}"
        )
    rollups_by_subject = {record["rollup"]["profile_subject_id"]: record for record in rollup_records}
    audience_by_subject = _collect_audience_snapshots_by_subject(
        snapshots=audience_triangulation_snapshots or [],
        known_profile_subject_ids=set(accounts_by_id),
    )
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
    missing_accounts = sorted(set(rollups_by_subject) - set(accounts_by_id))
    if missing_accounts:
        raise ValueError(
            "creator profile materialization received metric rollups for unknown platform accounts; "
            f"missing_accounts={missing_accounts!r}"
        )

    account_index = {account["platform_account_id"]: index for index, account in enumerate(accounts)}
    rollup_index = {record["rollup"]["profile_subject_id"]: record["rollup_index"] for record in rollup_records}
    profiles = []
    for account in accounts:
        account_id = account["platform_account_id"]
        rollup_record = rollups_by_subject.get(account_id)
        if rollup_record is None:
            profiles.append(
                _build_identity_only_platform_account_profile(
                    account=account,
                    onboarding=onboarding_by_account[account_id],
                    account_index=account_index[account_id],
                    audience_triangulation_snapshot=audience_by_subject.get(account_id),
                    generated_at_utc=generated_at_utc,
                )
            )
            continue
        profiles.append(
            _build_platform_account_profile(
                account=account,
                onboarding=onboarding_by_account[account_id],
                account_index=account_index[account_id],
                rollup=rollup_record["rollup"],
                rollup_index=rollup_index[account_id],
                metric_source_pointer=rollup_record["pointer"],
                metric_source_wrapper=rollup_record["wrapper"],
                audience_triangulation_snapshot=audience_by_subject.get(account_id),
                generated_at_utc=generated_at_utc,
            )
        )

    wrapper = {
        "schema_version": CREATOR_PROFILE_CURRENT_VIEW_SCHEMA_VERSION,
        "view_id": "creator_profile_current_view_v0",
        "view_mode": "source_backed_static_json_export",
        "generated_at_utc": generated_at_utc,
        "source_policy_posture": (
            "Static creator-profile-current export derived from the public-handle "
            "platform-account ledger, Bronze-derived Creator Registry onboarding "
            "projection, and platform creator metric seeds. Profiles are account-scoped "
            "unless promoted public-handle linkage exists."
        ),
        "authority_pointers": [
            "forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md",
            "forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md",
            "forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md",
        ],
        "source_inputs": [
            {
                "source_pointer": ACCOUNT_LEDGER_POINTER,
                "sha256": source_input_hashes[ACCOUNT_LEDGER_POINTER],
                "role": "source-backed platform accounts and identity state",
            },
            {
                "source_pointer": CREATOR_REGISTRY_INDEX_POINTER,
                "sha256": source_input_hashes[CREATOR_REGISTRY_INDEX_POINTER],
                "role": "account-level onboarding state derived from verified committed Bronze evidence",
            },
            *[
                {
                    "source_pointer": seed_input["pointer"],
                    "sha256": source_input_hashes[seed_input["pointer"]],
                    "role": seed_input["role"],
                }
                for seed_input in _metric_seed_inputs_for_source_list(seeds, metric_seed_inputs)
            ],
            *[
                {
                    "source_pointer": snapshot_input["pointer"],
                    "sha256": source_input_hashes[snapshot_input["pointer"]],
                    "role": snapshot_input["role"],
                }
                for snapshot_input in (audience_snapshot_inputs or [])
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
    onboarding: Mapping[str, Any],
    account_index: int,
    rollup: dict[str, Any],
    rollup_index: int,
    metric_source_pointer: str,
    metric_source_wrapper: str,
    audience_triangulation_snapshot: dict[str, Any] | None,
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
        "onboarding": deepcopy(dict(onboarding)),
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
        "audience_triangulation": (
            deepcopy(audience_triangulation_snapshot) if audience_triangulation_snapshot else None
        ),
        "wind_calling_summary": None,
        "freshness": {
            "identity_updated_at": account["handle_observed_at"],
            "metrics_computed_at_or_none": rollup["computed_at"],
            "audience_computed_at_or_none": (
                audience_triangulation_snapshot["generated_at"]
                if audience_triangulation_snapshot
                else None
            ),
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
        "limitations": _profile_limitations(
            platform=platform,
            rollup=rollup,
            audience_triangulation_joined=audience_triangulation_snapshot is not None,
        ),
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

def _build_identity_only_platform_account_profile(
    *,
    account: dict[str, Any],
    onboarding: Mapping[str, Any],
    account_index: int,
    audience_triangulation_snapshot: dict[str, Any] | None,
    generated_at_utc: str,
) -> dict[str, Any]:
    account_id = account["platform_account_id"]
    platform = account["platform"]
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
        "onboarding": deepcopy(dict(onboarding)),
        "platform_accounts": [deepcopy(account)],
        "identity_evidence_summary": {
            "summary": (
                f"Single-platform {platform} public account observed from source-backed "
                "creator registry identity evidence; no metric rollup exists yet."
            ),
            "account_pointer": (
                f"{ACCOUNT_LEDGER_POINTER}#/creator_public_handle_linkage_ledger/"
                f"platform_accounts/{account_index}"
            ),
            "source_pointers": source_pointers,
        },
        "current_metric_rollups": [],
        "audience_triangulation": (
            deepcopy(audience_triangulation_snapshot) if audience_triangulation_snapshot else None
        ),
        "wind_calling_summary": None,
        "freshness": {
            "identity_updated_at": account["handle_observed_at"],
            "metrics_computed_at_or_none": None,
            "audience_computed_at_or_none": (
                audience_triangulation_snapshot["generated_at"]
                if audience_triangulation_snapshot
                else None
            ),
            "profile_view_computed_at": generated_at_utc,
        },
        "source_drill_back": {
            "identity_ledger_pointer": (
                f"{ACCOUNT_LEDGER_POINTER}#/creator_public_handle_linkage_ledger/"
                f"platform_accounts/{account_index}"
            ),
            "metric_rollup_pointer": None,
            "metric_snapshot_pointer": None,
            "source_metric_observation_ids": [],
        },
        "limitations": _identity_only_profile_limitations(
            platform=platform,
            audience_triangulation_joined=audience_triangulation_snapshot is not None,
        ),
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

def _profile_limitations(
    *, platform: str, rollup: dict[str, Any], audience_triangulation_joined: bool
) -> list[str]:
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
        (
            "Audience triangulation is joined from transcript, observed-comment, and persisted "
            "comment-attention evidence; demographics remain not_estimated."
            if audience_triangulation_joined
            else "Audience triangulation is not joined in this static view."
        ),
        "Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.",
        "Average/median view rollups are directional admitted-pool statistics; sample_support must be shown or used to downgrade thin rows before influence-summary presentation.",
        "The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative to the creator's full Shorts or channel output.",
    ]

def _identity_only_profile_limitations(
    *, platform: str, audience_triangulation_joined: bool
) -> list[str]:
    return [
        f"Profile is account-scoped to one {platform} platform account; it is not a linked creator_record.",
        "No creator metric rollup is joined yet; do not infer average views, engagement rate, posting cadence, or comment performance.",
        "Identity evidence is source-backed, but metrics remain unavailable until a separate source-backed metric observation and rollup exists.",
        (
            "Audience triangulation is joined from transcript, observed-comment, and persisted "
            "comment-attention evidence; demographics remain not_estimated."
            if audience_triangulation_joined
            else "Audience triangulation is not joined in this static view."
        ),
        "Cross-platform aggregate influence is blocked until promoted public-handle linkage evidence exists.",
        "sample_support is unavailable because no metric rollup is joined; downgrade or withhold influence-summary presentation.",
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
        "profiles_with_audience_triangulation": sum(
            1 for profile in profiles if profile["audience_triangulation"] is not None
        ),
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
        "onboarded_profiles": sum(
            1 for profile in profiles if profile["onboarding"]["onboarding_state"] == "onboarded"
        ),
        "not_onboarded_profiles": sum(
            1
            for profile in profiles
            if profile["onboarding"]["onboarding_state"] == "not_onboarded"
        ),
    }


def _onboarding_by_account_from_registry(document: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    wrapper = document.get("creator_registry_index")
    if not isinstance(wrapper, Mapping):
        raise ValueError("creator_registry_index wrapper is required")
    rows = wrapper.get("platform_accounts")
    if not isinstance(rows, list):
        raise ValueError("creator_registry_index platform_accounts must be a list")
    result: dict[str, Mapping[str, Any]] = {}
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("creator_registry_index platform account rows must be objects")
        account_id = row.get("platform_account_id")
        onboarding = row.get("onboarding")
        if not isinstance(account_id, str) or not account_id or not isinstance(onboarding, Mapping):
            raise ValueError("creator_registry_index row requires platform_account_id and onboarding")
        if account_id in result:
            raise ValueError(f"duplicate Creator Registry onboarding row: {account_id!r}")
        result[account_id] = onboarding
    return result


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


def _normalize_audience_snapshot_paths(
    *,
    audience_triangulation_snapshot_path: str | Path | None,
    audience_triangulation_snapshot_paths: Sequence[str | Path] | None,
) -> list[Path]:
    if (
        audience_triangulation_snapshot_path is not None
        and audience_triangulation_snapshot_paths is not None
    ):
        raise ValueError(
            "provide either audience_triangulation_snapshot_path or "
            "audience_triangulation_snapshot_paths, not both"
        )
    if audience_triangulation_snapshot_paths is not None:
        return [Path(path) for path in audience_triangulation_snapshot_paths]
    if audience_triangulation_snapshot_path is not None:
        return [Path(audience_triangulation_snapshot_path)]
    return []



def _normalize_audience_outcome_paths(
    *,
    audience_judgment_outcome_path: str | Path | None,
    audience_judgment_outcome_paths: Sequence[str | Path] | None,
) -> list[Path]:
    if (
        audience_judgment_outcome_path is not None
        and audience_judgment_outcome_paths is not None
    ):
        raise ValueError(
            "provide either audience_judgment_outcome_path or "
            "audience_judgment_outcome_paths, not both"
        )
    if audience_judgment_outcome_paths is not None:
        return [Path(path) for path in audience_judgment_outcome_paths]
    if audience_judgment_outcome_path is not None:
        return [Path(audience_judgment_outcome_path)]
    return []


def verify_audience_judgment_outcomes(
    snapshot_paths: Sequence[Path], outcome_paths: Sequence[Path]
) -> None:
    """Require one exact successful Judgment outcome for every audience snapshot."""

    if len(snapshot_paths) != len(outcome_paths):
        raise ValueError(
            "each audience triangulation snapshot requires one paired successful "
            "Judgment outcome"
        )
    for snapshot_path, outcome_path in zip(snapshot_paths, outcome_paths):
        snapshots = load_creator_audience_triangulation_snapshot_document(snapshot_path)
        if len(snapshots) != 1:
            raise ValueError(
                f"paired audience snapshot must contain exactly one record: {snapshot_path}"
            )
        snapshot = snapshots[0]
        raw_outcome = load_json(outcome_path)
        outcome_model = (
            CreatorAudienceJudgmentOutcomeV1
            if raw_outcome.get("schema_version") == "creator_audience_judgment_outcome_v1"
            else CreatorAudienceJudgmentOutcome
        )
        outcome = outcome_model.model_validate(raw_outcome)
        if outcome.status != "validated" or outcome.snapshot_or_none is None:
            raise ValueError(
                f"audience Judgment outcome is not successful: {outcome_path}"
            )
        snapshot_sha256 = f"sha256:{hashlib.sha256(snapshot_path.read_bytes()).hexdigest()}"
        if outcome.snapshot_sha256_or_none != snapshot_sha256:
            raise ValueError(
                f"audience snapshot bytes do not match Judgment outcome: {snapshot_path}"
            )
        if outcome.snapshot_or_none.model_dump(mode="json") != snapshot:
            raise ValueError(
                f"audience snapshot content does not match Judgment outcome: {snapshot_path}"
            )
        if (
            outcome.snapshot_id_or_none != snapshot.get("snapshot_id")
            or outcome.bundle_id != snapshot.get("input_bundle_id")
            or outcome.bundle_hash != snapshot.get("input_bundle_hash")
            or outcome.creator_id != snapshot.get("creator_id")
            or outcome.profile_subject_id != snapshot.get("profile_subject_id")
        ):
            raise ValueError(
                f"audience snapshot identity does not match Judgment outcome: {snapshot_path}"
            )

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


def _load_audience_snapshot_input(path: Path) -> dict[str, Any]:
    return {
        "path": path,
        "snapshots": load_creator_audience_triangulation_snapshot_document(path),
        "wrapper": AUDIENCE_SNAPSHOT_WRAPPER_KEY,
        "pointer": _source_pointer_for_path(path),
        "role": "validated transcript/comment audience triangulation snapshots",
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


def _collect_audience_snapshots_by_subject(
    *,
    snapshots: Sequence[dict[str, Any]],
    known_profile_subject_ids: set[str],
) -> dict[str, dict[str, Any]]:
    by_subject: dict[str, dict[str, Any]] = {}
    for snapshot in snapshots:
        subject_id = snapshot["profile_subject_id"]
        if subject_id in by_subject:
            raise ValueError(f"creator profile materialization received duplicate audience snapshot: {subject_id!r}")
        by_subject[subject_id] = snapshot
    unknown_subjects = sorted(set(by_subject) - known_profile_subject_ids)
    if unknown_subjects:
        raise ValueError(
            "creator profile materialization received audience snapshots without matching profiles: "
            f"{unknown_subjects!r}"
        )
    return by_subject


def _sha256_repo_text(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _source_pointer_for_path(path: Path) -> str:
    try:
        root = Path(__file__).resolve().parents[3]
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()
