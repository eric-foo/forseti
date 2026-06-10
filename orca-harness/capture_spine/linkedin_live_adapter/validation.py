"""LinkedIn live-adapter validators (no runtime).

Every negative is a raise (``LinkedInLaneError``), so a test proves the gate
fails bad input rather than passing hollow. The generic fail-closed primitives
(forbidden-output-field walk, key allowlist, required-field check, NEGATED
non_claims category check, excluded public-actor-basis markers) are IMPORTED from
``linkedin_lane.shared_validation`` (the single source of truth).

- ``validate_live_access_envelope`` (slice 3a): owner-presence ATTESTED, no
  entitlement-gate bypass, execution NOT authorized, attended mode, POC-risk iff.
- ``validate_live_observation`` (slice 3b): the §6.2 minimization boundary -- the
  record is named-fields-only and the retained/captured flags must be False, so
  over-captured state (profile body / contact / follower list / content) cannot
  pass; person observations carry the shared public-actor-basis gate. No runtime,
  no projection into ``CandidateRow`` yet (that is slice 3b-2).
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import fields
from typing import Any

from capture_spine.linkedin_lane.models import EntityType, PERSON_ENTITY_TYPES
from capture_spine.linkedin_lane.shared_validation import (
    assert_no_forbidden_output_fields,
    fail as _fail,
    reject_unknown_keys as _reject_unknown_keys,
    require_fields as _require,
    validate_non_claims_categories as _validate_non_claims,
    validate_public_actor_basis,
)
from capture_spine.linkedin_live_adapter.models import (
    LINKEDIN_LIVE_ACCESS_ENVELOPE_SCHEMA_VERSION,
    LINKEDIN_LIVE_OBSERVATION_SCHEMA_VERSION,
    LiveAccessEnvelope,
    LiveAccessMode,
    LiveObservation,
)


# --- slice 3a: Live Access Envelope ---
_ALLOWED_LIVE_ACCESS_ENVELOPE_KEYS = frozenset(f.name for f in fields(LiveAccessEnvelope))
_ALLOWED_LIVE_ACCESS_MODES = frozenset(v.value for v in LiveAccessMode)
_POC_RISK_LIVE_ACCESS_MODE_VALUES = frozenset(
    {LiveAccessMode.OWNER_PRESENT_ATTENDED_AUTOMATION.value}
)
_REQUIRED_LIVE_ACCESS_ENVELOPE_FIELDS: tuple[str, ...] = (
    "live_access_id",
    "run_id",
    "live_access_mode",
    "source_policy_posture",
    "stop_condition",
    "attended_presence_check_method",
)


def validate_live_access_envelope(envelope: Mapping[str, Any]) -> None:
    assert_no_forbidden_output_fields(envelope)
    _reject_unknown_keys(envelope, _ALLOWED_LIVE_ACCESS_ENVELOPE_KEYS, "live_access_envelope")
    _require(envelope, _REQUIRED_LIVE_ACCESS_ENVELOPE_FIELDS, "live_access_envelope")
    if envelope.get("schema_version") != LINKEDIN_LIVE_ACCESS_ENVELOPE_SCHEMA_VERSION:
        _fail(
            "invalid_schema_version",
            f"live access envelope schema_version must be {LINKEDIN_LIVE_ACCESS_ENVELOPE_SCHEMA_VERSION}",
        )
    if envelope.get("live_access_mode") not in _ALLOWED_LIVE_ACCESS_MODES:
        _fail(
            "invalid_live_access_mode",
            "live_access_mode must be an attended mode "
            "(attended_manual / owner_present_attended_automation); no unattended mode",
        )
    if envelope.get("owner_presence_attested") is not True:
        _fail(
            "presence_not_attested",
            "owner_presence_attested must be True (a live access run requires confirmed owner presence)",
        )
    if envelope.get("entitlement_gate_bypass") is not False:
        _fail(
            "entitlement_gate_bypass_forbidden",
            "entitlement_gate_bypass must be False (no circumventing login walls, caps, or paid tiers)",
        )
    if envelope.get("execution_authorized") is not False:
        _fail(
            "execution_authorization_forbidden",
            "execution_authorized must be False (this is a no-runtime contract record, not a live runner)",
        )
    caps = envelope.get("caps")
    if not isinstance(caps, Mapping) or not caps:
        _fail("missing_caps", "caps are required (a live access run must declare its caps)")
    is_poc_mode = envelope.get("live_access_mode") in _POC_RISK_LIVE_ACCESS_MODE_VALUES
    poc_flag_set = envelope.get("optional_poc_risk_mode") is True
    if is_poc_mode and not poc_flag_set:
        _fail(
            "poc_risk_mode_not_attested",
            "owner_present_attended_automation is a POC-risk mode; optional_poc_risk_mode must be True",
        )
    if poc_flag_set and not is_poc_mode:
        _fail(
            "poc_risk_mode_overattested",
            "optional_poc_risk_mode=True is valid only for owner_present_attended_automation "
            "(no over-attesting POC-risk on a non-POC mode)",
        )
    _validate_non_claims(envelope.get("non_claims"), "live_access_envelope")


# --- slice 3b: Live Observation (minimization boundary; no projection yet) ---
_ALLOWED_LIVE_OBSERVATION_KEYS = frozenset(f.name for f in fields(LiveObservation))
_ALLOWED_OBSERVED_ENTITY_TYPES = frozenset(v.value for v in EntityType)
_PERSON_ENTITY_TYPE_VALUES = frozenset(v.value for v in PERSON_ENTITY_TYPES)
# A person OBSERVATION is the minimization seam, so it must be minimized:
# person_data_minimized must be exactly "yes" (reject "no" / "not_applicable").
_PERSON_OBSERVATION_MINIMIZED_REQUIRED = "yes"
# Defense-in-depth length cap: named-fields-only blocks a STRUCTURED bag, but a
# free-text field could still hold a copied profile body; the cap catches GROSS
# over-capture. Small forbidden content (e.g. an email in a basis field) is NOT
# fully caught here -- that is the 3c runtime read-time-minimization concern.
_MAX_OBSERVED_FREETEXT_LEN = 512
_LENGTH_CAPPED_FREETEXT_FIELDS: tuple[str, ...] = (
    "observed_display_name",
    "observed_source_locator",
    "observed_public_role_or_title_or_none",
    "observed_location_or_none",
    "senior_role_or_public_actor_basis_or_none",
)
_REQUIRED_LIVE_OBSERVATION_FIELDS: tuple[str, ...] = (
    "observation_id",
    "live_access_id",
    "run_id",
    "observed_entity_type",
    "observed_display_name",
    "observed_source_surface",
    "observed_source_locator",
    "provenance_timestamp",
    "minimization_rule",
)
# The §6.2 minimization boundary: these must be False on every observation. (The
# record carries no field for the captured content itself -- named-fields-only --
# so the boundary is structural; the flags are the attested belt-and-suspenders.)
_MINIMIZATION_BOUNDARY_FLAGS: tuple[str, ...] = (
    "contact_fields_retained",
    "network_or_follower_list_retained",
    "profile_body_captured",
    "content_captured",
)


def validate_live_observation(observation: Mapping[str, Any]) -> None:
    # Contract-level validation only: checks ONE observation's shape + minimization
    # boundary. It does NOT bind the referenced LiveAccessEnvelope (matching
    # live_access_id / run_id + a validated envelope) -- that posture binding is the
    # slice-3b-2 mint-path. The observation is NOT safe standalone; this is the shape
    # gate, not the full posture gate.
    assert_no_forbidden_output_fields(observation)
    _reject_unknown_keys(observation, _ALLOWED_LIVE_OBSERVATION_KEYS, "live_observation")
    _require(observation, _REQUIRED_LIVE_OBSERVATION_FIELDS, "live_observation")
    if observation.get("schema_version") != LINKEDIN_LIVE_OBSERVATION_SCHEMA_VERSION:
        _fail(
            "invalid_schema_version",
            f"live observation schema_version must be {LINKEDIN_LIVE_OBSERVATION_SCHEMA_VERSION}",
        )
    if observation.get("observed_entity_type") not in _ALLOWED_OBSERVED_ENTITY_TYPES:
        _fail("invalid_observed_entity_type", "observed_entity_type must be a valid EntityType value")
    # Minimization boundary: every retained/captured flag must be False.
    for flag in _MINIMIZATION_BOUNDARY_FLAGS:
        if observation.get(flag) is not False:
            _fail(
                f"forbidden_{flag}",
                f"{flag} must be false on every observation (minimization boundary)",
            )
    # Defense-in-depth: free-text fields must not exceed the minimized-signal length
    # cap (catches a gross over-capture like a copied profile body; small forbidden
    # content is the 3c runtime concern).
    for field_name in _LENGTH_CAPPED_FREETEXT_FIELDS:
        value = observation.get(field_name)
        if isinstance(value, str) and len(value) > _MAX_OBSERVED_FREETEXT_LEN:
            _fail(
                f"oversized_{field_name}",
                f"{field_name} exceeds the minimized-signal length cap ({_MAX_OBSERVED_FREETEXT_LEN} chars)",
            )
    # Person observations: the shared public-actor-basis gate + must be minimized.
    if observation.get("observed_entity_type") in _PERSON_ENTITY_TYPE_VALUES:
        validate_public_actor_basis(
            observation.get("senior_role_or_public_actor_basis_or_none"), "person observation"
        )
        if observation.get("person_data_minimized") != _PERSON_OBSERVATION_MINIMIZED_REQUIRED:
            _fail(
                "person_data_not_minimized",
                "a person observation is the minimization seam: person_data_minimized must be 'yes' "
                "(an unminimized person observation must not pass)",
            )
