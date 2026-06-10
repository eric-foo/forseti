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
    LiveObservation,
    validate_live_access_envelope,
    validate_live_observation,
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


# --- slice 3b: Live Observation (minimization boundary, no runtime) ---

def _observation(**overrides) -> LiveObservation:
    fields = dict(
        observation_id="obs-0001",
        live_access_id="live-0001",
        run_id="linkedin_lane_pilot_001",
        observed_entity_type="business_entity",
        observed_display_name="Competitor X",
        observed_source_surface="company_website_blog_press_pricing",
        observed_source_locator="https://competitorx.example/pricing",
        provenance_timestamp="2026-06-10T00:00:00Z",
        minimization_rule="business_entity_only",
    )
    fields.update(overrides)
    return LiveObservation(**fields)


def _person_observation(**overrides) -> LiveObservation:
    fields = dict(
        observation_id="obs-0002",
        live_access_id="live-0001",
        run_id="linkedin_lane_pilot_001",
        observed_entity_type="individual_person",
        observed_display_name="Jane Public",
        observed_source_surface="conference_podcast_newsletter_publication",
        observed_source_locator="https://conf.example/speakers/jane-public",
        provenance_timestamp="2026-06-10T00:00:00Z",
        minimization_rule="name_role_locator_only",
        person_data_minimized="yes",
        senior_role_or_public_actor_basis_or_none="keynote speaker at a named public conference under her own name",
    )
    fields.update(overrides)
    return LiveObservation(**fields)


def test_valid_business_observation_passes_and_serializes() -> None:
    obs = _observation()
    validate_live_observation(obs.to_dict())
    assert obs.to_dict()["schema_version"] == "linkedin_live_observation_v0"
    assert obs.to_dict()["profile_body_captured"] is False


def test_valid_person_observation_passes() -> None:
    validate_live_observation(_person_observation().to_dict())


def test_observation_forbidden_field_raises() -> None:
    bad = {**_observation().to_dict(), "follower_list": ["a", "b"]}
    with pytest.raises(LinkedInLaneError):
        validate_live_observation(bad)


def test_observation_unknown_field_raises() -> None:
    bad = {**_observation().to_dict(), "some_unexpected_field": "x"}
    with pytest.raises(LinkedInLaneError):
        validate_live_observation(bad)


def test_observation_profile_body_captured_flag_raises() -> None:
    # minimization boundary: a captured-content flag set True must raise
    with pytest.raises(LinkedInLaneError):
        validate_live_observation(_observation(profile_body_captured=True).to_dict())


def test_observation_network_list_retained_flag_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_live_observation(_observation(network_or_follower_list_retained=True).to_dict())


def test_person_observation_missing_basis_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_live_observation(
            _person_observation(senior_role_or_public_actor_basis_or_none=None).to_dict()
        )


def test_person_observation_excluded_basis_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_live_observation(
            _person_observation(senior_role_or_public_actor_basis_or_none="listed in the org chart").to_dict()
        )


def test_person_observation_not_minimized_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_live_observation(_person_observation(person_data_minimized="not_applicable").to_dict())


def test_observation_invalid_entity_type_raises() -> None:
    bad = _observation().to_dict()
    bad["observed_entity_type"] = "not_a_real_type"
    with pytest.raises(LinkedInLaneError):
        validate_live_observation(bad)


def test_observation_missing_required_field_raises() -> None:
    bad = _observation().to_dict()
    del bad["observed_display_name"]
    with pytest.raises(LinkedInLaneError):
        validate_live_observation(bad)


# --- negatives added after the cross-vendor slice-3b review (F1, F2, F4) ---

def test_person_observation_data_minimized_no_raises() -> None:
    # F2: a person observation is the minimization seam -- "no" (= not minimized)
    # must NOT pass; only "yes" is acceptable. (Code-pinned per F4.)
    with pytest.raises(LinkedInLaneError) as exc:
        validate_live_observation(_person_observation(person_data_minimized="no").to_dict())
    assert exc.value.code == "person_data_not_minimized"


def test_observation_oversized_freetext_field_raises() -> None:
    # F1: a free-text field carrying a gross over-capture (e.g. a copied profile
    # body) exceeds the minimized-signal length cap and must raise. (Code-pinned.)
    bad = _observation(observed_public_role_or_title_or_none="x" * 600).to_dict()
    with pytest.raises(LinkedInLaneError) as exc:
        validate_live_observation(bad)
    assert exc.value.code == "oversized_observed_public_role_or_title_or_none"
