"""LinkedIn live-adapter -- slice 3a: Live Access Envelope contract record (NO runtime).

Per the accepted live-layer ADR
(``data_capture_spine_linkedin_live_layer_architecture_v0``, amended via the
assumption-gate to Opt 2): a thin SATELLITE record carrying the live-access
POSTURE -- owner-presence attested, no entitlement-gate bypass, attended live
mode -- as VALIDATED PREDICATE fields. These fields live here, in the adapter,
NOT in the no-live core: the core has no such fields and adding them would widen
it, which the isolation invariant forbids. NO live runtime, NO browser / session
/ fetch -- this is the contract + fail-closed validator only, mirroring how
slices 1+2 shipped. The error type + the forbidden-output-field walk are IMPORTED
from ``linkedin_lane`` (slice 1): a one-way import (adapter -> core), never the
reverse, so deleting this package leaves slices 1+2 untouched.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

from capture_spine.linkedin_lane.models import LinkedInLaneError

__all__ = [
    "LinkedInLaneError",
    "LINKEDIN_LIVE_ACCESS_ENVELOPE_SCHEMA_VERSION",
    "DEFAULT_LINKEDIN_LIVE_ADAPTER_NON_CLAIMS",
    "LiveAccessMode",
    "LiveAccessEnvelope",
]


LINKEDIN_LIVE_ACCESS_ENVELOPE_SCHEMA_VERSION = "linkedin_live_access_envelope_v0"


# non_claims default: each declared as a NEGATED claim so the validator's
# negated-category check is satisfied by the lane defaults (a hollow override
# still fails). Mirrors the slice-1/2 non_claims posture.
DEFAULT_LINKEDIN_LIVE_ADAPTER_NON_CLAIMS: tuple[str, ...] = (
    "not live LinkedIn access in this contract record",
    "not no-entitlement gate bypass",
    "not a live runner or execution authorization",
    "not automatic promotion or capture",
    "not contact acquisition or lead list",
    "not follower/connection/commenter graph capture",
    "not profile body or content capture",
    "not Source Capture Packet output",
    "not Data Capture handoff",
    "not Outreach Lane execution",
    "not commercial use, validation, or readiness",
)


class LiveAccessMode(StrEnum):
    # The two owner-present / attended live modes (ADR-accepted). No unattended mode.
    ATTENDED_MANUAL = "attended_manual"
    OWNER_PRESENT_ATTENDED_AUTOMATION = "owner_present_attended_automation"


@dataclass(frozen=True)
class LiveAccessEnvelope:
    live_access_id: str
    run_id: str
    live_access_mode: LiveAccessMode
    source_policy_posture: str
    stop_condition: str
    # Presence is an ATTESTED predicate (a bool the validator requires True),
    # backed by a stated check method -- not a mere enum label.
    owner_presence_attested: bool
    attended_presence_check_method: str
    caps: dict[str, int]
    schema_version: str = LINKEDIN_LIVE_ACCESS_ENVELOPE_SCHEMA_VERSION
    # Hard-stop predicates (validator enforces these exact booleans).
    entitlement_gate_bypass: bool = False
    execution_authorized: bool = False
    optional_poc_risk_mode: bool = False
    non_commercial_posture: str = "pre_commercial"
    exclusions: tuple[str, ...] = ()
    non_claims: tuple[str, ...] = DEFAULT_LINKEDIN_LIVE_ADAPTER_NON_CLAIMS

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


def _enum_values(value: Any) -> Any:
    if isinstance(value, StrEnum):
        return value.value
    if isinstance(value, tuple):
        return [_enum_values(item) for item in value]
    if isinstance(value, list):
        return [_enum_values(item) for item in value]
    if isinstance(value, dict):
        return {key: _enum_values(item) for key, item in value.items()}
    return value
