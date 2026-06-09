"""LinkedIn Lane no-live harness -- slice 1 validators.

These translate the review-cleared pilot acceptance gate into code: every
negative is a raise (``LinkedInLaneError``), so a test can prove the gate
actually fails bad input rather than passing hollow. The forbidden-field walk is
duplicated from the Reddit lane-support pattern (its set differs from this one),
deliberately not imported, to avoid a linkedin_lane -> reddit_candidate_intake
coupling.

The candidate-row gate is schema-conformant, not just invariant-spot-checking:
it rejects unknown / aliased keys (a fail-closed top-level allowlist derived from
the ``CandidateRow`` schema), requires the descriptive fields, and validates the
closed-enum and fixed values. That closes three classes a spot-check misses:
under-specified rows, a row that omits ``entity_type`` to skip the person gate,
and banned concepts reaching the output under alias keys the exact denylist did
not enumerate.
"""
from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import fields
from typing import Any

from capture_spine.linkedin_lane.models import (
    PERSON_ENTITY_TYPES,
    PERSON_PRIVACY_SENSITIVITIES,
    CandidateClass,
    CandidateRow,
    EntityType,
    LinkedInLaneError,
    MethodMode,
    MinimizationRule,
    PersonDataMinimized,
    PrivacySensitivity,
    RunEnvelope,
    SourceSurface,
)


# Forbidden OUTPUT field NAMES, exact case-insensitive key match. Precision is
# load-bearing: follower/connection/commenter *lists and graphs* are forbidden,
# but the visible-influence *_count_or_none / *_band_or_none fields are allowed
# -- exact matching keeps `follower_count_or_none` out of this set. The retained-
# flag fields (`contact_fields_retained`, `network_or_follower_list_retained`,
# `content_captured`) are also distinct exact strings from the banned names.
# Substring matching is NOT safe here: the schema's own legitimate fields embed
# banned stems (contact_fields_retained, network_or_follower_list_retained,
# content_captured, profile_body_captured, *_count_or_none) -- so the denylist
# stays exact-match and the top-level allowlist (below) is what closes aliasing.
FORBIDDEN_OUTPUT_FIELDS = {
    # contact acquisition
    "email",
    "emails",
    "email_address",
    "email_or_none",
    "phone",
    "phone_number",
    "phone_numbers",
    "phone_or_none",
    "phone_number_or_none",
    "contact",
    "contacts",
    "contact_info",
    "contact_details",
    "contact_route",
    "contact_routes",
    "private_contact_route",
    "private_contact_routes",
    "contact_graph",
    "enrichment",
    "enrichment_output",
    # follower / connection / commenter LISTS + GRAPHS (not counts)
    "followers",
    "follower_list",
    "follower_lists",
    "follower_graph",
    "connections",
    "connection_list",
    "connection_lists",
    "connection_graph",
    "commenters",
    "commenter_list",
    "commenter_lists",
    "commenter_graph",
    "network_graph",
    "relationship_graph",
    "relationship_list",
    "relationship_lists",
    # employment / org-chart graphs
    "employment_history",
    "employment_graph",
    "employment_history_graph",
    "org_chart",
    "org_charts",
    "org_chart_graph",
    "full_org_chart",
    "full_org_chart_graph",
    # lead lists
    "lead",
    "leads",
    "lead_list",
    "lead_lists",
    "lead_emails",
    "lead_contacts",
    # profile body / post content
    "profile_body",
    "profile_html",
    "profile_text",
    "about_section",
    "headline_text",
    "post_content",
    "post_text",
    "posts",
    "content",
    # raw capture / secrets
    "raw_html",
    "html",
    "rendered_dom",
    "dom",
    "parser_output",
    "screenshot",
    "screenshot_path",
    "cookie",
    "cookies",
    "session",
    "session_state",
    "hidden_session_state",
    "authorization_header",
    # downstream-stage leakage
    "source_capture_packet",
    "packet_manifest",
    "ecr",
    "cleaning",
    "judgment",
    "source_quality_score",
}


# Fail-closed top-level allowlist: a candidate row may carry only the keys the
# Candidate Row Schema defines. Derived from the dataclass so it tracks the schema
# with zero drift, and it rejects aliased banned keys (email_or_none,
# contact_route, relationship_list, ...) wholesale without any substring risk.
CANDIDATE_ROW_ALLOWED_KEYS: frozenset[str] = frozenset(f.name for f in fields(CandidateRow))


# Required descriptive fields (the schema's non-default fields). Must be present
# and non-empty on every candidate row, so an under-specified mapping cannot pass
# and a row cannot omit entity_type to skip the person gate.
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


# A person qualifies only on a concrete public-actor basis that stands OUTSIDE the
# employer org chart (architecture). These markers name bases the architecture
# disqualifies outright. Conservative, fail-closed lexical exclusion on the
# free-text basis: it cannot prove a basis is genuine (operator judgment remains),
# but it rejects the named excluded bases.
_EXCLUDED_PERSON_BASIS_MARKERS: tuple[str, ...] = (
    "org chart",
    "org-chart",
    "orgchart",
    "organization chart",
    "organisation chart",
    "reporting line",
    "reports to",
    "mentioned by",
    "tagged by",
    "mention/tag",
    "routine post",
    "routine work update",
    "routine update",
    "commenter",
    "follower",
    "connection",
)


# The run envelope's non_claims must CONTAIN the pilot acceptance-gate hard-stop
# categories, not merely be non-empty -- a hollow override like ("not ready",)
# must fail. Each token must appear (case-insensitively) in some declared
# non-claim; the lane defaults satisfy this set.
_REQUIRED_NON_CLAIM_TOKENS: tuple[str, ...] = (
    "live",
    "source capture packet",
    "data capture",
    "outreach",
    "promotion",
)


# Defense-in-depth on secret VALUES that could land in a legitimately named
# field. Each pattern anchors on an unambiguous credential marker, not entropy,
# so it does not false-positive on candidate vocabulary (names, locators,
# coarse counts). Favors false negatives over false positives.
_FORBIDDEN_OUTPUT_VALUE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("pem_private_key", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("bearer_token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=\-]{16,}")),
    ("credentialed_url_userinfo", re.compile(r"://[^/\s:@]+:[^/\s:@]+@")),
    ("set_cookie_header", re.compile(r"(?i)\bset-cookie:\s*[^=\s;]+=[^=\s;]+")),
)


def assert_no_forbidden_output_fields(value: Any, *, path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            lowered = str(key).lower()
            if lowered in FORBIDDEN_OUTPUT_FIELDS:
                _fail("forbidden_output_field", f"forbidden output field at {path}.{key}")
            assert_no_forbidden_output_fields(child, path=f"{path}.{key}")
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, child in enumerate(value):
            assert_no_forbidden_output_fields(child, path=f"{path}[{index}]")
        return
    if isinstance(value, str):
        _assert_no_forbidden_output_value(value, path=path)


def _assert_no_forbidden_output_value(value: str, *, path: str) -> None:
    for marker, pattern in _FORBIDDEN_OUTPUT_VALUE_PATTERNS:
        if pattern.search(value):
            _fail("forbidden_output_value", f"forbidden secret-like value ({marker}) at {path}")


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
    if not envelope.non_claims:
        _fail("missing_non_claims", "run envelope must declare non_claims")
    joined_non_claims = " || ".join(envelope.non_claims).lower()
    missing_non_claims = [t for t in _REQUIRED_NON_CLAIM_TOKENS if t not in joined_non_claims]
    if missing_non_claims:
        _fail(
            "incomplete_non_claims",
            "run envelope non_claims must declare the required hard-stop categories; missing: "
            + ", ".join(missing_non_claims),
        )


def validate_candidate_row(row: Mapping[str, Any]) -> None:
    # Fail-closed top-level allowlist: reject any key outside the Candidate Row
    # Schema (closes aliased banned keys without substring risk).
    unknown = sorted(k for k in row if k not in CANDIDATE_ROW_ALLOWED_KEYS)
    if unknown:
        _fail("unknown_candidate_row_field", f"candidate row carries unknown field(s): {unknown}")
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
    basis = row.get("senior_role_or_public_actor_basis_or_none")
    if not isinstance(basis, str) or not basis.strip():
        _fail(
            "missing_public_actor_basis",
            "a person row requires a concrete org-chart-independent public-actor / senior-role basis",
        )
    lowered_basis = basis.lower()
    for marker in _EXCLUDED_PERSON_BASIS_MARKERS:
        if marker in lowered_basis:
            _fail(
                "excluded_public_actor_basis",
                "a person-row basis must stand outside the employer org chart and must not be a mention/tag, "
                f"routine post, commenter, follower, or connection (matched excluded basis: {marker!r})",
            )
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


def _fail(code: str, message: str) -> None:
    raise LinkedInLaneError(code, message)
