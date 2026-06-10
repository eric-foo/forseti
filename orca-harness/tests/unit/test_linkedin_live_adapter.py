"""Tests for the LinkedIn live-adapter (slice 3a): Live Access Envelope contract.

Fake-success guard: every negative asserts validate_live_access_envelope RAISES
``LinkedInLaneError`` on the bad case -- presence not attested, entitlement-gate
bypass, execution authorized (no runtime in the contract slice), a non-attended
mode value, a missing presence-check method, the POC-risk mode without its flag,
an aliased forbidden field, an unknown field, and a hollow / positive non_claims
override. Plus happy-path round-trips for both attended modes.
"""
from __future__ import annotations

import pytest

from capture_spine.linkedin_live_adapter import (
    LinkedInLaneError,
    LiveAccessEnvelope,
    LiveAccessMode,
    validate_live_access_envelope,
)


def _envelope(**overrides) -> LiveAccessEnvelope:
    fields = dict(
        live_access_id="live-0001",
        run_id="linkedin_lane_pilot_001",
        live_access_mode=LiveAccessMode.ATTENDED_MANUAL,
        source_policy_posture="discoverable_or_entitled_disclosable",
        stop_condition="caps_reached",
        owner_presence_attested=True,
        attended_presence_check_method="operator confirmed present at keyboard during this run",
        caps={"max_profiles": 25, "max_searches": 10},
    )
    fields.update(overrides)
    return LiveAccessEnvelope(**fields)


# --- positive / round-trip ---

def test_valid_attended_manual_envelope_passes_and_serializes() -> None:
    env = _envelope()
    validate_live_access_envelope(env.to_dict())
    dumped = env.to_dict()
    assert dumped["live_access_mode"] == "attended_manual"
    assert dumped["execution_authorized"] is False
    assert dumped["entitlement_gate_bypass"] is False
    assert dumped["schema_version"] == "linkedin_live_access_envelope_v0"


def test_valid_owner_present_automation_with_poc_flag_passes() -> None:
    env = _envelope(
        live_access_mode=LiveAccessMode.OWNER_PRESENT_ATTENDED_AUTOMATION,
        optional_poc_risk_mode=True,
    )
    validate_live_access_envelope(env.to_dict())


# --- negatives: every one must raise ---

def test_presence_not_attested_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_live_access_envelope(_envelope(owner_presence_attested=False).to_dict())


def test_entitlement_gate_bypass_true_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_live_access_envelope(_envelope(entitlement_gate_bypass=True).to_dict())


def test_execution_authorized_true_raises() -> None:
    # no runtime in the contract slice
    with pytest.raises(LinkedInLaneError):
        validate_live_access_envelope(_envelope(execution_authorized=True).to_dict())


def test_missing_presence_check_method_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_live_access_envelope(_envelope(attended_presence_check_method="  ").to_dict())


def test_empty_caps_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_live_access_envelope(_envelope(caps={}).to_dict())


def test_poc_risk_mode_without_flag_raises() -> None:
    # the autonomous attended mode must carry optional_poc_risk_mode=True
    with pytest.raises(LinkedInLaneError):
        validate_live_access_envelope(
            _envelope(live_access_mode=LiveAccessMode.OWNER_PRESENT_ATTENDED_AUTOMATION).to_dict()
        )


def test_non_attended_mode_value_raises() -> None:
    # an unattended-mode value (dict tampering past the enum) is rejected fail-closed
    bad = _envelope().to_dict()
    bad["live_access_mode"] = "unattended_automation"
    with pytest.raises(LinkedInLaneError):
        validate_live_access_envelope(bad)


def test_aliased_forbidden_field_raises() -> None:
    bad = {**_envelope().to_dict(), "cookies": "session=abc123"}
    with pytest.raises(LinkedInLaneError):
        validate_live_access_envelope(bad)


def test_unknown_field_raises() -> None:
    bad = {**_envelope().to_dict(), "some_unexpected_field": "x"}
    with pytest.raises(LinkedInLaneError):
        validate_live_access_envelope(bad)


def test_hollow_non_claims_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_live_access_envelope(_envelope(non_claims=("not ready",)).to_dict())


def test_positive_live_claim_does_not_satisfy_category_raises() -> None:
    # a POSITIVE inverse claim ("live access enabled") must NOT satisfy the "live" category
    with pytest.raises(LinkedInLaneError):
        validate_live_access_envelope(
            _envelope(
                non_claims=(
                    "live access enabled",  # positive -- must not satisfy "live"
                    "not promotion",
                    "not source capture packet",
                    "not data capture",
                    "not outreach",
                )
            ).to_dict()
        )


# --- negatives added after the cross-vendor code review (GPT-5.5 F1, F2) ---

def test_reversal_negation_does_not_satisfy_category_raises() -> None:
    # F1: a syntactically-negated but semantically-positive claim
    # ("not only live access; it also authorizes it") must NOT satisfy "live".
    with pytest.raises(LinkedInLaneError):
        validate_live_access_envelope(
            _envelope(
                non_claims=(
                    "not only live access; it also authorizes it",
                    "not promotion",
                    "not source capture packet",
                    "not data capture",
                    "not outreach",
                )
            ).to_dict()
        )


def test_poc_flag_on_manual_mode_raises() -> None:
    # F2: optional_poc_risk_mode=True is valid only for the autonomous mode;
    # manual mode + flag=True must raise (the consistency predicate is iff, not one-way).
    with pytest.raises(LinkedInLaneError):
        validate_live_access_envelope(
            _envelope(
                live_access_mode=LiveAccessMode.ATTENDED_MANUAL,
                optional_poc_risk_mode=True,
            ).to_dict()
        )
