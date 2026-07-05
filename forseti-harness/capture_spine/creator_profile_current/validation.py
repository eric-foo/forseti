"""Validate the creator-profile-current structural contract.

This module is the always-on structural and posture floor for the static creator
profile current view. It validates shape, identity/metric boundary posture,
rollup coupling, and non-claim guards. It does not rehash source inputs, rebuild
metric magnitudes from sibling ledgers, query a live lake, or prove
source-backed numeric truth; fixture rebuild and source-hash freshness checks
remain separate test concerns until a source-rebuild validator is added.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from capture_spine.creator_profile_current.ideal_audience_snapshot import (
    validate_creator_ideal_audience_profile_snapshot,
)
from capture_spine.creator_public_handle_linkage.models import CreatorPublicHandleLinkageError
from capture_spine.creator_public_handle_linkage.validation import assert_no_forbidden_output_fields


CREATOR_PROFILE_CURRENT_VIEW_SCHEMA_VERSION = "creator_profile_current_view_v0"
_WRAPPER_KEY = "creator_profile_current_view"

_ALLOWED_TOP_LEVEL_KEYS = frozenset({_WRAPPER_KEY})
_ALLOWED_WRAPPER_KEYS = frozenset(
    {
        "schema_version",
        "view_id",
        "view_mode",
        "generated_at_utc",
        "source_policy_posture",
        "authority_pointers",
        "source_inputs",
        "counts",
        "profiles",
        "accepted_residuals",
        "non_claims",
    }
)
_ALLOWED_SOURCE_INPUT_KEYS = frozenset({"source_pointer", "sha256", "role"})
_ALLOWED_COUNTS_KEYS = frozenset(
    {
        "profiles_total",
        "platform_account_profiles",
        "creator_record_profiles",
        "profiles_with_metric_rollups",
        "profiles_with_ideal_audience_profiles",
        "engagement_rate_observed_profiles",
        "cross_platform_rollup_profiles",
    }
)
_ALLOWED_PROFILE_KEYS = frozenset(
    {
        "profile_subject_kind",
        "profile_subject_id",
        "platform_account_id_or_none",
        "creator_record_id_or_none",
        "identity_state",
        "link_state_or_none",
        "review_state_or_none",
        "platform_accounts",
        "identity_evidence_summary",
        "current_metric_rollups",
        "ideal_audience_profile",
        "wind_calling_summary",
        "freshness",
        "source_drill_back",
        "limitations",
        "non_claims",
    }
)
_ALLOWED_PLATFORM_ACCOUNT_KEYS = frozenset(
    {
        "platform_account_id",
        "platform",
        "platform_public_account_id_or_none",
        "public_handle",
        "public_profile_url",
        "handle_source_pointer",
        "handle_observed_at",
        "public_display_name_or_none",
        "display_name_source_pointer_or_none",
        "display_name_source_field_or_none",
    }
)
_ALLOWED_ROLLUP_KEYS = frozenset(
    {
        "metric_rollup_id",
        "metric_rollup_pointer",
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
        "sample_support",
        "calculation_recipe_version",
        "computed_at",
        "freshness_state",
        "limitations",
    }
)
_ALLOWED_METRIC_KEYS = frozenset(
    {
        "average_views",
        "median_views",
        "engagement_rate",
        "average_like_count",
        "average_comment_count",
        "posting_cadence",
        "recent_velocity",
    }
)
_ALLOWED_METRIC_VALUE_KEYS = frozenset(
    {"value_or_none", "posture", "posture_reason_or_none", "metric_unit"}
)
_ALLOWED_SAMPLE_SUPPORT_KEYS = frozenset(
    {"observation_count", "sample_adequacy", "representativeness_posture", "surface_handling"}
)
_ALLOWED_FRESHNESS_KEYS = frozenset(
    {
        "identity_updated_at",
        "metrics_computed_at_or_none",
        "audience_computed_at_or_none",
        "profile_view_computed_at",
    }
)
_ALLOWED_IDENTITY_EVIDENCE_SUMMARY_KEYS = frozenset(
    {"summary", "account_pointer", "source_pointers"}
)
_ALLOWED_SOURCE_DRILL_BACK_KEYS = frozenset(
    {
        "identity_ledger_pointer",
        "metric_rollup_pointer",
        "metric_snapshot_pointer",
        "source_metric_observation_ids",
    }
)
_ALLOWED_PROFILE_SUBJECT_KINDS = frozenset({"platform_account", "creator_record"})
_PROMOTED_LINK_STATES = frozenset({"probable_public_account_link", "declared_public_account_link"})
_UNPROMOTED_LINK_STATES = frozenset({"candidate_public_account_link", "rejected_public_account_link"})
_ALLOWED_IDENTITY_STATES = frozenset({"single_platform_observed", *_PROMOTED_LINK_STATES, *_UNPROMOTED_LINK_STATES})
_REQUIRED_NON_CLAIM_FRAGMENTS = (
    "channel-wide creator influence",
    "engagement rate",
    "buyer proof",
    "public person-level identity",
    "contact or outreach authorization",
    "cross-platform rollup",
    "dashboard readiness",
    "not SQLite or data-lake physicalization",
)
_SHA256_RE = re.compile(r"[0-9a-f]{64}")


class CreatorProfileCurrentError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def load_creator_profile_current_view(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        _fail("invalid_json_fixture", "creator_profile_current view must be a JSON object")
    validate_creator_profile_current_view(value)
    return value


def validate_creator_profile_current_view(view_document: Mapping[str, Any]) -> None:
    try:
        assert_no_forbidden_output_fields(view_document)
    except CreatorPublicHandleLinkageError as exc:
        _fail(getattr(exc, "code", "forbidden_output_field"), str(exc))
    _reject_unknown_keys(view_document, _ALLOWED_TOP_LEVEL_KEYS, "view top-level")
    wrapper = view_document.get(_WRAPPER_KEY)
    if not isinstance(wrapper, Mapping):
        _fail("missing_view_wrapper", f"{_WRAPPER_KEY} wrapper is required")
    _validate_wrapper(wrapper)


def _validate_wrapper(wrapper: Mapping[str, Any]) -> None:
    _reject_unknown_keys(wrapper, _ALLOWED_WRAPPER_KEYS, "creator_profile_current_view")
    _require(
        wrapper,
        (
            "schema_version",
            "view_id",
            "view_mode",
            "generated_at_utc",
            "source_policy_posture",
            "authority_pointers",
            "source_inputs",
            "counts",
            "profiles",
        ),
        "creator_profile_current_view",
    )
    if wrapper["schema_version"] != CREATOR_PROFILE_CURRENT_VIEW_SCHEMA_VERSION:
        _fail("invalid_schema_version", "unexpected creator_profile_current schema_version")
    if wrapper["view_mode"] != "source_backed_static_json_export":
        _fail("invalid_view_mode", "view_mode must be source_backed_static_json_export")
    _validate_str_list(wrapper["authority_pointers"], "authority_pointers", allow_empty=False)
    _validate_source_inputs(wrapper["source_inputs"])
    profiles = _validate_profiles(wrapper["profiles"])
    _validate_counts(wrapper["counts"], profiles)
    if "non_claims" in wrapper:
        _validate_str_list(wrapper["non_claims"], "view_non_claims", allow_empty=False)
    if "accepted_residuals" in wrapper:
        _validate_str_list(wrapper["accepted_residuals"], "accepted_residuals", allow_empty=False)


def _validate_source_inputs(value: Any) -> None:
    if not _is_list(value) or not value:
        _fail("invalid_source_inputs", "source_inputs must be a non-empty list")
    for source_input in value:
        if not isinstance(source_input, Mapping):
            _fail("invalid_source_input", "source_inputs entries must be mappings")
        _reject_unknown_keys(source_input, _ALLOWED_SOURCE_INPUT_KEYS, "source_input")
        _require(source_input, ("source_pointer", "sha256", "role"), "source_input")
        _validate_non_empty_str(source_input["source_pointer"], "source_pointer")
        _validate_non_empty_str(source_input["role"], "source_input_role")
        if not _SHA256_RE.fullmatch(str(source_input["sha256"])):
            _fail("invalid_source_input_sha256", "source_input sha256 must be lowercase hex sha256")


def _validate_profiles(value: Any) -> list[Mapping[str, Any]]:
    if not _is_list(value):
        _fail("invalid_profiles", "profiles must be a list")
    profile_ids: set[str] = set()
    profiles: list[Mapping[str, Any]] = []
    for profile in value:
        if not isinstance(profile, Mapping):
            _fail("invalid_profile", "profile entries must be mappings")
        _reject_unknown_keys(profile, _ALLOWED_PROFILE_KEYS, "profile")
        _require(profile, tuple(_ALLOWED_PROFILE_KEYS), "profile")
        subject_kind = str(profile["profile_subject_kind"])
        subject_id = _validate_non_empty_str(profile["profile_subject_id"], "profile_subject_id")
        if subject_kind not in _ALLOWED_PROFILE_SUBJECT_KINDS:
            _fail("invalid_profile_subject_kind", "profile_subject_kind must be platform_account or creator_record")
        if subject_id in profile_ids:
            _fail("duplicate_profile_subject_id", f"duplicate profile_subject_id: {subject_id}")
        profile_ids.add(subject_id)
        _validate_identity_boundary(profile, subject_kind, subject_id)
        _validate_platform_accounts(profile["platform_accounts"], subject_kind, profile)
        _validate_identity_evidence_summary(profile["identity_evidence_summary"])
        _validate_profile_non_claims(profile["non_claims"])
        _validate_str_list(profile["limitations"], "profile_limitations", allow_empty=False)
        rollups = _validate_rollups(profile["current_metric_rollups"], profile)
        _validate_ideal_audience_profile(profile["ideal_audience_profile"], profile)
        _validate_unjoined_profile_surface(profile["wind_calling_summary"], "wind_calling_summary")
        _validate_source_drill_back(profile["source_drill_back"], profile["identity_evidence_summary"], rollups)
        _validate_freshness(profile["freshness"])
        profiles.append(profile)
    return profiles


def _validate_identity_boundary(profile: Mapping[str, Any], subject_kind: str, subject_id: str) -> None:
    identity_state = str(profile["identity_state"])
    if identity_state not in _ALLOWED_IDENTITY_STATES:
        _fail("invalid_identity_state", "identity_state is not allowed")
    platform_account_id = profile["platform_account_id_or_none"]
    creator_record_id = profile["creator_record_id_or_none"]
    link_state = profile["link_state_or_none"]
    review_state = profile["review_state_or_none"]

    if subject_kind == "platform_account":
        if platform_account_id != subject_id:
            _fail("platform_account_subject_mismatch", "platform account profile_subject_id must match platform_account_id_or_none")
        if creator_record_id is not None:
            _fail("platform_account_has_creator_record_id", "platform_account profiles must not carry creator_record_id_or_none")
    else:
        if creator_record_id != subject_id:
            _fail("creator_record_subject_mismatch", "creator_record profile_subject_id must match creator_record_id_or_none")
        if platform_account_id is not None:
            _fail("creator_record_has_single_platform_account_id", "creator_record profiles must not use platform_account_id_or_none")

    if identity_state == "single_platform_observed":
        if link_state is not None or review_state is not None:
            _fail("single_platform_link_state_present", "single_platform_observed profiles must not carry link/review state")
    else:
        if link_state != identity_state:
            _fail("identity_link_state_mismatch", "link_state_or_none must mirror identity_state when linked or reviewable")
        if not isinstance(review_state, str) or not review_state.strip():
            _fail("missing_review_state", "review_state_or_none is required when link_state_or_none is present")


def _validate_platform_accounts(value: Any, subject_kind: str, profile: Mapping[str, Any]) -> None:
    if not _is_list(value) or not value:
        _fail("invalid_platform_accounts", "profile platform_accounts must be a non-empty list")
    account_ids: list[str] = []
    for account in value:
        if not isinstance(account, Mapping):
            _fail("invalid_platform_account", "platform account entries must be mappings")
        _reject_unknown_keys(account, _ALLOWED_PLATFORM_ACCOUNT_KEYS, "platform_account")
        _require(
            account,
            (
                "platform_account_id",
                "platform",
                "public_handle",
                "public_profile_url",
                "handle_source_pointer",
                "handle_observed_at",
            ),
            "platform_account",
        )
        account_ids.append(_validate_non_empty_str(account["platform_account_id"], "platform_account_id"))
        _validate_non_empty_str(account["platform"], "platform")
        _validate_non_empty_str(account["public_handle"], "public_handle")
        _validate_non_empty_str(account["public_profile_url"], "public_profile_url")
    if len(account_ids) != len(set(account_ids)):
        _fail("duplicate_platform_account_ref", "profile platform_accounts must be unique")
    if subject_kind == "platform_account" and account_ids != [profile["platform_account_id_or_none"]]:
        _fail("platform_account_profile_account_mismatch", "platform_account profile must list only its own platform account")


def _validate_identity_evidence_summary(value: Any) -> None:
    if not isinstance(value, Mapping):
        _fail("invalid_identity_evidence_summary", "identity_evidence_summary must be a mapping")
    _reject_unknown_keys(value, _ALLOWED_IDENTITY_EVIDENCE_SUMMARY_KEYS, "identity_evidence_summary")
    _require(value, tuple(_ALLOWED_IDENTITY_EVIDENCE_SUMMARY_KEYS), "identity_evidence_summary")
    _validate_non_empty_str(value["summary"], "identity_evidence_summary.summary")
    _validate_non_empty_str(value["account_pointer"], "identity_evidence_summary.account_pointer")
    _validate_str_list(value["source_pointers"], "identity_evidence_summary.source_pointers", allow_empty=False)


def _validate_unjoined_profile_surface(value: Any, context: str) -> None:
    if value is not None:
        _fail(f"unsupported_{context}", f"{context} is not joined into creator_profile_current_view_v0")


def _validate_ideal_audience_profile(value: Any, profile: Mapping[str, Any]) -> None:
    if value is None:
        return
    if not isinstance(value, Mapping):
        _fail("invalid_ideal_audience_profile", "ideal_audience_profile must be an object or null")
    try:
        snapshot = validate_creator_ideal_audience_profile_snapshot(value)
    except ValueError as exc:
        _fail("invalid_ideal_audience_profile", f"invalid ideal_audience_profile snapshot: {exc}")
    if snapshot["profile_subject_kind"] != profile["profile_subject_kind"]:
        _fail("ideal_audience_profile_subject_mismatch", "ideal_audience_profile subject kind must match profile")
    if snapshot["profile_subject_id"] != profile["profile_subject_id"]:
        _fail("ideal_audience_profile_subject_mismatch", "ideal_audience_profile subject id must match profile")
    if profile["profile_subject_kind"] == "platform_account":
        if snapshot["platform_account_ids"] != [profile["platform_account_id_or_none"]]:
            _fail(
                "ideal_audience_profile_subject_mismatch",
                "platform_account ideal_audience_profile must point at the same platform account",
            )
    elif snapshot["creator_record_id_or_none"] != profile["creator_record_id_or_none"]:
        _fail(
            "ideal_audience_profile_subject_mismatch",
            "creator_record ideal_audience_profile must point at the same creator record",
        )


def _validate_rollups(value: Any, profile: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    if not _is_list(value):
        _fail("invalid_current_metric_rollups", "current_metric_rollups must be a list")
    rollups: list[Mapping[str, Any]] = []
    for rollup in value:
        if not isinstance(rollup, Mapping):
            _fail("invalid_metric_rollup", "current_metric_rollups entries must be mappings")
        _reject_unknown_keys(rollup, _ALLOWED_ROLLUP_KEYS, "metric_rollup")
        _require(rollup, tuple(_ALLOWED_ROLLUP_KEYS), "metric_rollup")
        _validate_rollup_identity(rollup, profile)
        _validate_observation_count(rollup["observation_count"])
        _validate_metric_values(rollup["metric_rollups"])
        _validate_source_observation_ids(rollup)
        _validate_sample_support(rollup)
        _validate_rollup_limitations(rollup["limitations"])
        rollups.append(rollup)
    return rollups


def _validate_source_drill_back(
    value: Any,
    identity_evidence_summary: Mapping[str, Any],
    rollups: Sequence[Mapping[str, Any]],
) -> None:
    if not isinstance(value, Mapping):
        _fail("invalid_source_drill_back", "source_drill_back must be a mapping")
    _reject_unknown_keys(value, _ALLOWED_SOURCE_DRILL_BACK_KEYS, "source_drill_back")
    missing = sorted(key for key in _ALLOWED_SOURCE_DRILL_BACK_KEYS if key not in value)
    if missing:
        _fail("missing_source_drill_back_field", f"source_drill_back missing field(s): {missing}")
    identity_pointer = _validate_non_empty_str(value["identity_ledger_pointer"], "source_drill_back.identity_ledger_pointer")
    if identity_pointer != identity_evidence_summary["account_pointer"]:
        _fail(
            "source_drill_back_identity_pointer_mismatch",
            "source_drill_back identity pointer must match identity evidence account pointer",
        )
    if not rollups:
        if value["metric_rollup_pointer"] is not None or value["metric_snapshot_pointer"] is not None:
            _fail(
                "identity_only_source_drill_back_has_metric_pointer",
                "identity-only profiles must not carry metric drill-back pointers",
            )
        source_ids = value["source_metric_observation_ids"]
        if not _is_list(source_ids) or source_ids:
            _fail(
                "identity_only_source_drill_back_has_metric_observations",
                "identity-only profiles must carry an empty source_metric_observation_ids list",
            )
        return
    _validate_non_empty_str(value["metric_rollup_pointer"], "source_drill_back.metric_rollup_pointer")
    _validate_non_empty_str(value["metric_snapshot_pointer"], "source_drill_back.metric_snapshot_pointer")
    source_ids = _validate_str_list(
        value["source_metric_observation_ids"],
        "source_drill_back.source_metric_observation_ids",
        allow_empty=False,
    )
    expected_source_ids = [
        source_id
        for rollup in rollups
        for source_id in rollup["source_metric_observation_ids"]
    ]
    if source_ids != expected_source_ids:
        _fail(
            "source_drill_back_observation_ids_mismatch",
            "source_drill_back source_metric_observation_ids must match rollup observation ids",
        )


def _validate_rollup_identity(rollup: Mapping[str, Any], profile: Mapping[str, Any]) -> None:
    platform_scope = str(rollup["platform_scope"])
    account_ids = rollup["platform_account_ids"]
    if not _is_list(account_ids) or not account_ids:
        _fail("invalid_platform_account_ids", "rollup platform_account_ids must be a non-empty list")
    if platform_scope == "cross_platform":
        if profile["profile_subject_kind"] != "creator_record" or profile["identity_state"] not in _PROMOTED_LINK_STATES:
            _fail("cross_platform_rollup_without_promoted_linkage", "cross-platform rollups require promoted public-handle linkage")
    elif profile["profile_subject_kind"] == "platform_account":
        if account_ids != [profile["platform_account_id_or_none"]]:
            _fail("account_rollup_subject_mismatch", "account-scoped rollup must point at the profile platform account")
    if profile["identity_state"] in _UNPROMOTED_LINK_STATES and platform_scope == "cross_platform":
        _fail("candidate_or_rejected_cross_platform_rollup", "candidate/rejected links must not produce cross-platform rollups")


def _validate_metric_values(value: Any) -> None:
    if not isinstance(value, Mapping):
        _fail("invalid_metric_rollups", "metric_rollups must be a mapping")
    _reject_unknown_keys(value, _ALLOWED_METRIC_KEYS, "metric_rollups")
    _require(value, tuple(_ALLOWED_METRIC_KEYS), "metric_rollups")
    for metric_name, metric in value.items():
        if not isinstance(metric, Mapping):
            _fail("invalid_metric_value", f"metric value for {metric_name} must be a mapping")
        _reject_unknown_keys(metric, _ALLOWED_METRIC_VALUE_KEYS, f"metric_rollups.{metric_name}")
        _require(metric, ("value_or_none", "posture", "metric_unit"), f"metric_rollups.{metric_name}")
        posture = str(metric["posture"])
        observed = posture == "observed"
        metric_value = metric["value_or_none"]
        if observed:
            if isinstance(metric_value, bool) or not isinstance(metric_value, (int, float)):
                _fail("observed_metric_missing_value", f"observed metric {metric_name} requires a numeric value")
            if metric.get("posture_reason_or_none") not in (None, ""):
                _fail("observed_metric_has_reason", f"observed metric {metric_name} must not carry a reason")
        else:
            if metric_value is not None:
                _fail("metric_value_for_non_observed_posture", f"non-observed metric {metric_name} must have null value")
            reason = metric.get("posture_reason_or_none")
            if not isinstance(reason, str) or not reason.strip():
                _fail("missing_metric_posture_reason", f"non-observed metric {metric_name} requires posture_reason_or_none")


def _validate_observation_count(value: Any) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        _fail("invalid_observation_count", "observation_count must be a positive integer")


def _validate_source_observation_ids(rollup: Mapping[str, Any]) -> None:
    source_ids = rollup["source_metric_observation_ids"]
    if not _is_list(source_ids) or not source_ids:
        _fail("invalid_source_metric_observation_ids", "rollup must list source_metric_observation_ids")
    if len(source_ids) != len(set(str(item) for item in source_ids)):
        _fail("duplicate_source_metric_observation_id", "source_metric_observation_ids must be unique")
    if rollup["observation_count"] != len(source_ids):
        _fail("observation_count_mismatch", "observation_count must match source_metric_observation_ids length")


def _validate_sample_support(rollup: Mapping[str, Any]) -> None:
    sample = rollup["sample_support"]
    if not isinstance(sample, Mapping):
        _fail("missing_sample_support", "rollup sample_support is required")
    _reject_unknown_keys(sample, _ALLOWED_SAMPLE_SUPPORT_KEYS, "sample_support")
    _require(sample, tuple(_ALLOWED_SAMPLE_SUPPORT_KEYS), "sample_support")
    observation_count = rollup["observation_count"]
    if sample["observation_count"] != observation_count:
        _fail("sample_support_count_mismatch", "sample_support observation_count must match rollup observation_count")
    expected_adequacy = _sample_support_label(observation_count)
    if sample["sample_adequacy"] != expected_adequacy:
        _fail("sample_adequacy_mismatch", f"sample_adequacy must be {expected_adequacy}")
    if sample["representativeness_posture"] != "admitted_pool_only_not_representative_creator_average":
        _fail("invalid_representativeness_posture", "rollups must not claim representative creator averages")
    expected_handling = _surface_handling(observation_count)
    if sample["surface_handling"] != expected_handling:
        _fail("surface_handling_mismatch", f"surface_handling must be {expected_handling}")


def _validate_rollup_limitations(value: Any) -> None:
    limitations = _validate_str_list(value, "rollup_limitations", allow_empty=False)
    joined = " ".join(limitations)
    if "not a representative creator average" not in joined:
        _fail("missing_representativeness_limitation", "rollup limitations must name non-representativeness")
    if "selection can bias view averages" not in joined:
        _fail("missing_selection_bias_limitation", "rollup limitations must name admitted-pool selection bias")


def _validate_freshness(value: Any) -> None:
    if not isinstance(value, Mapping):
        _fail("invalid_freshness", "freshness must be a mapping")
    _reject_unknown_keys(value, _ALLOWED_FRESHNESS_KEYS, "freshness")
    _require(value, ("identity_updated_at", "profile_view_computed_at"), "freshness")


def _validate_counts(counts: Any, profiles: Sequence[Mapping[str, Any]]) -> None:
    if not isinstance(counts, Mapping):
        _fail("invalid_counts", "counts must be a mapping")
    _reject_unknown_keys(counts, _ALLOWED_COUNTS_KEYS, "counts")
    _require(counts, tuple(_ALLOWED_COUNTS_KEYS), "counts")
    _assert_equal(counts["profiles_total"], len(profiles), "profiles_total")
    _assert_equal(
        counts["platform_account_profiles"],
        sum(1 for profile in profiles if profile["profile_subject_kind"] == "platform_account"),
        "platform_account_profiles",
    )
    _assert_equal(
        counts["creator_record_profiles"],
        sum(1 for profile in profiles if profile["profile_subject_kind"] == "creator_record"),
        "creator_record_profiles",
    )
    _assert_equal(
        counts["profiles_with_metric_rollups"],
        sum(1 for profile in profiles if profile["current_metric_rollups"]),
        "profiles_with_metric_rollups",
    )
    _assert_equal(
        counts["profiles_with_ideal_audience_profiles"],
        sum(1 for profile in profiles if profile["ideal_audience_profile"] is not None),
        "profiles_with_ideal_audience_profiles",
    )
    _assert_equal(
        counts["engagement_rate_observed_profiles"],
        sum(
            1
            for profile in profiles
            if any(
                rollup["metric_rollups"]["engagement_rate"]["posture"] == "observed"
                for rollup in profile["current_metric_rollups"]
            )
        ),
        "engagement_rate_observed_profiles",
    )
    _assert_equal(
        counts["cross_platform_rollup_profiles"],
        sum(
            1
            for profile in profiles
            if any(rollup["platform_scope"] == "cross_platform" for rollup in profile["current_metric_rollups"])
        ),
        "cross_platform_rollup_profiles",
    )


def _validate_profile_non_claims(value: Any) -> None:
    claims = _validate_str_list(value, "profile_non_claims", allow_empty=False)
    joined = " ".join(claims)
    for fragment in _REQUIRED_NON_CLAIM_FRAGMENTS:
        if fragment not in joined:
            _fail("missing_required_non_claim", f"profile non_claims must include {fragment!r}")


def _sample_support_label(observation_count: int) -> str:
    if observation_count <= 3:
        return "thin_n_1_to_3"
    if observation_count <= 7:
        return "limited_n_4_to_7"
    return "stronger_admitted_pool_n_8_plus"


def _surface_handling(observation_count: int) -> str:
    if observation_count <= 3:
        return "downgrade_or_withhold_summary_claim"
    return "show_only_with_visible_admitted_pool_limitation"


def _validate_str_list(value: Any, context: str, *, allow_empty: bool) -> list[str]:
    if not _is_list(value) or (not allow_empty and not value):
        _fail(f"invalid_{context}", f"{context} must be a list")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            _fail(f"invalid_{context}", f"{context} entries must be non-empty strings")
        result.append(item)
    return result


def _validate_non_empty_str(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(f"invalid_{context}", f"{context} must be a non-empty string")
    return value


def _reject_unknown_keys(value: Mapping[str, Any], allowed: frozenset[str], context: str) -> None:
    unknown = sorted(set(str(key) for key in value) - allowed)
    if unknown:
        _fail("unknown_field", f"unknown field(s) in {context}: {', '.join(unknown)}")


def _require(value: Mapping[str, Any], keys: Sequence[str], context: str) -> None:
    for key in keys:
        if key not in value:
            _fail(f"missing_{key}", f"{context} missing required field: {key}")


def _assert_equal(actual: Any, expected: Any, context: str) -> None:
    if actual != expected:
        _fail("derived_count_mismatch", f"{context} mismatch: expected {expected!r}, got {actual!r}")


def _is_list(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _fail(code: str, message: str) -> None:
    raise CreatorProfileCurrentError(code, message)
