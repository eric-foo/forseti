"""LinkedIn Lane no-live harness -- slice 1 validators.

These translate the review-cleared pilot acceptance gate into code: every
negative is a raise (``LinkedInLaneError``), so a test can prove the gate
actually fails bad input rather than passing hollow.

The generic fail-closed primitives -- the forbidden-output-field walk, the
fail-closed key allowlist, the required-field check, the NEGATED non_claims
category check, and the excluded public-actor-basis markers -- are IMPORTED from
``shared_validation`` (the single source of truth for the lane), not
re-implemented here. (This closed two drifts: slice-1 previously used a WEAKER
substring non_claims check -- a positive "live LinkedIn access" satisfied "live"
-- and its excluded-basis marker list lagged slice-2's; both now inherit the
stronger/superset shared form.)

The candidate-row gate is schema-conformant: it rejects unknown / aliased keys (a
fail-closed allowlist derived from the ``CandidateRow`` schema), requires the
descriptive fields, and validates the closed-enum and fixed values.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import fields
from typing import Any

from capture_spine.linkedin_lane.models import (
    LINKEDIN_LANE_RUN_ENVELOPE_SCHEMA_VERSION,
    PERSON_ENTITY_TYPES,
    PERSON_PRIVACY_SENSITIVITIES,
    CandidateClass,
    CandidateRow,
    EntityType,
    MethodMode,
    MinimizationRule,
    PersonDataMinimized,
    PrivacySensitivity,
    RunEnvelope,
    SourceSurface,
    StopReason,
)
from capture_spine.linkedin_lane.shared_validation import (
    assert_no_forbidden_output_fields,
    fail as _fail,
    reject_unknown_keys,
    validate_non_claims_categories,
    validate_public_actor_basis,
)


# Fail-closed top-level allowlist: a candidate row may carry only the keys the
# Candidate Row Schema defines. Derived from the dataclass so it tracks the schema
# with zero drift, and it rejects aliased banned keys wholesale.
CANDIDATE_ROW_ALLOWED_KEYS: frozenset[str] = frozenset(f.name for f in fields(CandidateRow))


# Required descriptive fields (the schema's non-default fields). Must be present
# and non-empty, so an under-specified mapping cannot pass and a row cannot omit
# entity_type to skip the person gate.
_REQUIRED_CANDIDATE_ROW_FIELDS: tuple[str, ...] = (
    "candidate_id",
    "run_id",
    "candidate_class",
    "entity_type",
    "display_name",
    "source_surface",
    "source_policy_posture",
    "method_mode",
    "declared_theme_or_decision_context",
    "run_purpose",
    "business_relevance_note",
    "privacy_sensitivity",
    "minimization_rule",
    "person_data_minimized",
    "provenance_timestamp",
)


# Closed-enum fields: enumerated values must be valid members, so a garbage enum
# string is rejected rather than silently accepted.
_CLOSED_ENUM_FIELDS: tuple[tuple[str, frozenset[str]], ...] = (
    ("candidate_class", frozenset(v.value for v in CandidateClass)),
    ("entity_type", frozenset(v.value for v in EntityType)),
    ("source_surface", frozenset(v.value for v in SourceSurface)),
    ("method_mode", frozenset(v.value for v in MethodMode)),
    ("privacy_sensitivity", frozenset(v.value for v in PrivacySensitivity)),
    ("minimization_rule", frozenset(v.value for v in MinimizationRule)),
    ("person_data_minimized", frozenset(v.value for v in PersonDataMinimized)),
)


# RunEnvelope closed-enum value sets. RunEnvelope is a dataclass -- type hints are
# NOT enforced at runtime -- so these must be validated like CandidateRow's closed
# enums (a StrEnum member compares equal to its value, so a valid member passes
# and a bogus string fails).
_ALLOWED_METHOD_MODE_VALUES = frozenset(v.value for v in MethodMode)
_ALLOWED_CANDIDATE_CLASS_VALUES = frozenset(v.value for v in CandidateClass)
_ALLOWED_SOURCE_SURFACE_VALUES = frozenset(v.value for v in SourceSurface)
_ALLOWED_MINIMIZATION_RULE_VALUES = frozenset(v.value for v in MinimizationRule)
_ALLOWED_STOP_REASON_VALUES = frozenset(v.value for v in StopReason)


def validate_run_envelope(envelope: RunEnvelope) -> None:
    if not envelope.run_id.strip():
        _fail("missing_run_id", "run_id is required")
    if not envelope.declared_theme_or_decision_context.strip():
        _fail("missing_declared_theme", "declared_theme_or_decision_context is required")
    if not envelope.run_purpose.strip():
        _fail("missing_run_purpose", "run_purpose is required")
    if not envelope.candidate_classes:
        _fail("missing_candidate_classes", "at least one candidate_class is required")
    if not envelope.source_surface_allowlist:
        _fail("missing_source_surface_allowlist", "at least one source surface is required")
    if not envelope.source_policy_posture.strip():
        _fail("missing_source_policy_posture", "source_policy_posture is required")
    if not envelope.promotion_owner.strip():
        _fail("missing_promotion_owner", "promotion_owner is required")
    for name, val in (
        ("max_businesses", envelope.max_businesses),
        ("max_organizations", envelope.max_organizations),
        ("max_people", envelope.max_people),
    ):
        if val < 0:
            _fail(f"invalid_{name}", f"{name} must not be negative")
    if envelope.max_source_surfaces < 1:
        _fail("invalid_max_source_surfaces", "max_source_surfaces must be positive")
    if envelope.time_window_days < 1:
        _fail("invalid_time_window_days", "time_window_days must be positive")
    if (envelope.max_businesses + envelope.max_organizations + envelope.max_people) < 1:
        _fail(
            "missing_entity_caps",
            "at least one entity cap (businesses / organizations / people) must be positive",
        )
    # Closed-enum + schema validation. RunEnvelope is a dataclass (type hints not
    # enforced at runtime), so out-of-schema values must be rejected here, matching
    # the strictness validate_candidate_row already uses for closed enums.
    if envelope.schema_version != LINKEDIN_LANE_RUN_ENVELOPE_SCHEMA_VERSION:
        _fail(
            "invalid_schema_version",
            f"run envelope schema_version must be {LINKEDIN_LANE_RUN_ENVELOPE_SCHEMA_VERSION}",
        )
    if envelope.method_mode not in _ALLOWED_METHOD_MODE_VALUES:
        _fail("invalid_method_mode", "method_mode must be a valid MethodMode value")
    for candidate_class in envelope.candidate_classes:
        if candidate_class not in _ALLOWED_CANDIDATE_CLASS_VALUES:
            _fail("invalid_candidate_class", "each candidate_class must be a valid CandidateClass value")
    for surface in envelope.source_surface_allowlist:
        if surface not in _ALLOWED_SOURCE_SURFACE_VALUES:
            _fail(
                "invalid_source_surface",
                "each source_surface_allowlist entry must be a valid SourceSurface value",
            )
    if envelope.minimization_rule not in _ALLOWED_MINIMIZATION_RULE_VALUES:
        _fail("invalid_minimization_rule", "minimization_rule must be a valid MinimizationRule value")
    if envelope.stop_condition not in _ALLOWED_STOP_REASON_VALUES:
        _fail("invalid_stop_condition", "stop_condition must be a valid StopReason value")
    # Shared NEGATED non_claims check (closes slice-1's F4 substring weakness).
    validate_non_claims_categories(envelope.non_claims, "run_envelope")


def validate_candidate_row(row: Mapping[str, Any]) -> None:
    # Fail-closed top-level allowlist: reject any key outside the Candidate Row
    # Schema (closes aliased banned keys without substring risk).
    reject_unknown_keys(row, CANDIDATE_ROW_ALLOWED_KEYS, "candidate row")
    # Recursive denylist (nested values + defense-in-depth) and secret-value scan.
    assert_no_forbidden_output_fields(row)
    # Required descriptive fields must be present and non-empty.
    for field_name in _REQUIRED_CANDIDATE_ROW_FIELDS:
        value = row.get(field_name)
        if value is None or (isinstance(value, str) and not value.strip()):
            _fail("missing_required_candidate_field", f"candidate row requires a non-empty {field_name}")
    # Fixed values.
    if row.get("source_family") != "linkedin_adjacent":
        _fail("invalid_source_family", "candidate rows must carry source_family linkedin_adjacent")
    if row.get("capture_unit_intake_status") != "candidate_or_scouting":
        _fail("invalid_capture_unit_intake_status", "candidate rows must remain candidate_or_scouting")
    if row.get("allowed_downstream_use") != "planning_only":
        _fail("invalid_allowed_downstream_use", "candidate rows must remain planning_only")
    if row.get("promotion_required") is not True:
        _fail("missing_promotion_required", "candidate rows must carry promotion_required: true")
    # Closed-enum validity.
    for field_name, allowed in _CLOSED_ENUM_FIELDS:
        if row.get(field_name) not in allowed:
            _fail(f"invalid_{field_name}", f"{field_name} must be a valid {field_name} value")
    # Retained flags must be false on every row.
    for retained in (
        "contact_fields_retained",
        "network_or_follower_list_retained",
        "profile_body_captured",
        "content_captured",
    ):
        if row.get(retained) is not False:
            _fail(f"forbidden_{retained}", f"{retained} must be false on every candidate row")
    # Person-row gate (entity_type is guaranteed present + valid by the checks above).
    if row.get("entity_type") in {entity.value for entity in PERSON_ENTITY_TYPES}:
        _validate_person_row(row)


def _validate_person_row(row: Mapping[str, Any]) -> None:
    # Shared public-actor-basis check (non-empty + excluded-marker SUPERSET).
    validate_public_actor_basis(row.get("senior_role_or_public_actor_basis_or_none"), "person row")
    if row.get("privacy_sensitivity") not in {p.value for p in PERSON_PRIVACY_SENSITIVITIES}:
        _fail(
            "invalid_person_privacy_sensitivity",
            "a person row requires privacy_sensitivity person_strict / public_actor_strict / quarantine",
        )
    if not str(row.get("minimization_rule", "")).strip():
        _fail("missing_minimization_rule", "a person row requires a minimization_rule")
    if row.get("person_data_minimized") not in {
        PersonDataMinimized.YES.value,
        PersonDataMinimized.NO.value,
    }:
        _fail(
            "person_data_minimized_not_set",
            "a person row requires person_data_minimized set (yes/no), not not_applicable",
        )
