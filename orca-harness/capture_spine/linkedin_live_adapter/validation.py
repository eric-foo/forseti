"""LinkedIn live-adapter -- slice 3a validators.

Translate the accepted live-layer ADR's slice-3a predicates into raising
validators (``LinkedInLaneError``): every negative is a raise, so a test proves
the gate fails bad input rather than passing hollow. Hardened to the slice-1/2
standard: a fail-closed top-level KEY allowlist (derived from the dataclass), the
IMPORTED forbidden-output-field walk (from ``linkedin_lane``), and a NEGATED
non_claims check (a positive inverse claim must not satisfy a category).

The load-bearing predicates (ADR refinement B / slice 3a) -- the point of this
slice -- are enforced here, NOT carried as enum labels: owner-presence is
ATTESTED (a bool that must be True + a stated check method), entitlement-gate
bypass is FORBIDDEN (must be False), execution is NOT authorized (this is a
no-runtime contract record, must be False), the live mode is one of the two
attended modes, and the autonomous attended mode must carry the POC-risk flag.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import fields
from typing import Any

from capture_spine.linkedin_lane.models import LinkedInLaneError
from capture_spine.linkedin_lane.validation import assert_no_forbidden_output_fields
from capture_spine.linkedin_live_adapter.models import (
    LINKEDIN_LIVE_ACCESS_ENVELOPE_SCHEMA_VERSION,
    LiveAccessEnvelope,
    LiveAccessMode,
)


# Fail-closed top-level allowlist, derived from the dataclass so it tracks the
# schema with zero drift and rejects aliased banned keys wholesale.
_ALLOWED_LIVE_ACCESS_ENVELOPE_KEYS = frozenset(f.name for f in fields(LiveAccessEnvelope))
_ALLOWED_LIVE_ACCESS_MODES = frozenset(v.value for v in LiveAccessMode)
# The autonomous (vs purely manual) attended mode carries the POC-risk posture.
_POC_RISK_LIVE_ACCESS_MODE_VALUES = frozenset(
    {LiveAccessMode.OWNER_PRESENT_ATTENDED_AUTOMATION.value}
)

# Required descriptive (str/enum) fields -- must be present and non-empty. The
# boolean predicates (presence/bypass/execution) are checked separately below.
_REQUIRED_LIVE_ACCESS_ENVELOPE_FIELDS: tuple[str, ...] = (
    "live_access_id",
    "run_id",
    "live_access_mode",
    "source_policy_posture",
    "stop_condition",
    "attended_presence_check_method",
)

# non_claims must DISCLAIM (negate) each hard-stop category -- a positive inverse
# claim like "live LinkedIn access" must NOT satisfy "live" (mirrors slice 2).
_REQUIRED_NON_CLAIM_CATEGORIES: tuple[str, ...] = (
    "live",
    "promotion",
    "source capture packet",
    "data capture",
    "outreach",
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
    # Presence is an ATTESTED predicate, not a label: the bool must be True
    # (the required check-method backs it via _require above).
    if envelope.get("owner_presence_attested") is not True:
        _fail(
            "presence_not_attested",
            "owner_presence_attested must be True (a live access run requires confirmed owner presence)",
        )
    # No entitlement-gate bypass (hard stop) -- enforced as a predicate, not only declared.
    if envelope.get("entitlement_gate_bypass") is not False:
        _fail(
            "entitlement_gate_bypass_forbidden",
            "entitlement_gate_bypass must be False (no circumventing login walls, caps, or paid tiers)",
        )
    # No runtime in the contract slice: execution must not be authorized here.
    if envelope.get("execution_authorized") is not False:
        _fail(
            "execution_authorization_forbidden",
            "execution_authorized must be False (this is a no-runtime contract record, not a live runner)",
        )
    caps = envelope.get("caps")
    if not isinstance(caps, Mapping) or not caps:
        _fail("missing_caps", "caps are required (a live access run must declare its caps)")
    # Consistency (iff, per ADR §8): the POC-risk flag is True EXACTLY for the
    # autonomous attended mode -- enforced both ways, so the flag cannot
    # over-attest POC-risk on a non-POC (manual) mode.
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


def _reject_unknown_keys(value_map: Mapping[str, Any], allowed_keys: frozenset[str], label: str) -> None:
    unknown = sorted(str(key) for key in value_map if str(key) not in allowed_keys)
    if unknown:
        _fail("unknown_field", f"{label} contains unknown field(s): {unknown}")


def _require(value_map: Mapping[str, Any], field_names: tuple[str, ...], label: str) -> None:
    for field_name in field_names:
        value = value_map.get(field_name)
        if value is None or (isinstance(value, str) and not value.strip()):
            _fail(f"missing_{field_name}", f"{label} missing required field: {field_name}")


def _validate_non_claims(value: Any, label: str) -> None:
    if not _is_list(value):
        _fail("missing_non_claims", f"{label} requires non_claims")
    claims = [str(item).strip().lower() for item in value]
    missing = [
        category
        for category in _REQUIRED_NON_CLAIM_CATEGORIES
        if not any(category in claim and _is_negated(claim) for claim in claims)
    ]
    if missing:
        _fail(
            "incomplete_non_claims",
            f"{label} non_claims must DISCLAIM (negate) the required hard-stop categories; missing: {missing}",
        )


# An expansive / exceptive qualifier reverses a leading negation ("not ONLY X",
# "not merely X", "... but X", "... also X"), so the claim does NOT disclaim the
# category. Lexical negation cannot be fully robust against a determined adversary
# (a contrived "not X; X is enabled" still reads as negated); this closes the
# demonstrated reversal class. A canonical accepted-disclaimer allowlist would be
# the fully-robust form -- deferred. (Slice-2's _is_negated shares this weakness.)
_NON_DISCLAIMER_MARKERS: tuple[str, ...] = (
    "only",
    "merely",
    "also",
    "as well",
    "but ",
    "however",
    "except",
)


def _is_negated(claim: str) -> bool:
    if not (claim.startswith("not ") or claim.startswith("no ")):
        return False
    return not any(marker in claim for marker in _NON_DISCLAIMER_MARKERS)


def _is_list(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _fail(code: str, message: str) -> None:
    raise LinkedInLaneError(code, message)
