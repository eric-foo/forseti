"""LinkedIn live-adapter -- data models (no runtime).

Per the accepted live-layer ADR
(``data_capture_spine_linkedin_live_layer_architecture_v0``): a thin SATELLITE
that carries the live-access POSTURE and the minimized OBSERVATIONS as validated
records, NOT in the no-live core. NO live runtime, NO browser / session / fetch.
The error type + (in validation.py) the shared fail-closed primitives are
IMPORTED from ``linkedin_lane`` -- a one-way import (adapter -> core), never the
reverse, so deleting this package leaves slices 1+2 intact.

- ``LiveAccessEnvelope`` (slice 3a): the live-access posture (owner-presence
  attested, no entitlement-gate bypass, attended mode, no execution authorized).
- ``LiveObservation`` (slice 3b): one minimized observed candidate, BEFORE
  projection into the core ``CandidateRow``. The §6.2 minimization boundary lives
  here AT THE CONTRACT LEVEL: the record is named-fields-only (no STRUCTURED field
  / dict bag for a profile body / contact / follower list / content), the
  retained/captured flags must be False, and the free-text fields are
  length-capped. A free-text field could still carry small forbidden *content* as
  text -- full content-level read-time minimization (what the adapter READ/KEPT)
  is the 3c runtime tape-test, NOT this contract. It REFERENCES the
  ``LiveAccessEnvelope`` via ``live_access_id`` (posture/non_claims lives on that
  run-level record); that envelope is BOUND to the observation only at the
  slice-3b-2 mint-path -- ``validate_live_observation`` alone is the shape gate,
  not the full posture gate. Projection + the mint-path are 3b-2.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

from capture_spine.linkedin_lane.models import LinkedInLaneError

__all__ = [
    "LinkedInLaneError",
    "LINKEDIN_LIVE_ACCESS_ENVELOPE_SCHEMA_VERSION",
    "LINKEDIN_LIVE_OBSERVATION_SCHEMA_VERSION",
    "DEFAULT_LINKEDIN_LIVE_ADAPTER_NON_CLAIMS",
    "LiveAccessMode",
    "LiveAccessEnvelope",
    "LiveObservation",
]


LINKEDIN_LIVE_ACCESS_ENVELOPE_SCHEMA_VERSION = "linkedin_live_access_envelope_v0"
LINKEDIN_LIVE_OBSERVATION_SCHEMA_VERSION = "linkedin_live_observation_v0"


# non_claims default for the access envelope: each declared as a NEGATED claim so
# the shared negated-category check is satisfied by the lane defaults.
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


@dataclass(frozen=True)
class LiveObservation:
    """One minimized observed candidate (pre-projection). Named-fields-only: no
    STRUCTURED field (no dict bag) for a profile body / contact / follower list /
    content. The validator also requires the retained/captured flags to be False
    and length-caps the free-text fields (the §6.2 boundary at the contract level).
    A free-text field could still hold small forbidden *content* as text -- full
    content minimization is the 3c runtime tape-test, not this contract."""

    observation_id: str
    live_access_id: str
    run_id: str
    observed_entity_type: str
    observed_display_name: str
    observed_source_surface: str
    observed_source_locator: str
    provenance_timestamp: str
    minimization_rule: str
    schema_version: str = LINKEDIN_LIVE_OBSERVATION_SCHEMA_VERSION
    person_data_minimized: str = "not_applicable"
    # Observed minimized public signal -- counts / coarse bands only, never lists.
    observed_public_role_or_title_or_none: str | None = None
    observed_location_or_none: str | None = None
    senior_role_or_public_actor_basis_or_none: str | None = None
    visible_follower_count_or_none: str | None = None
    visible_connection_count_band_or_none: str | None = None
    exclusions: tuple[str, ...] = ()
    # Minimization boundary -- must stay False on every observation.
    contact_fields_retained: bool = False
    network_or_follower_list_retained: bool = False
    profile_body_captured: bool = False
    content_captured: bool = False

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
