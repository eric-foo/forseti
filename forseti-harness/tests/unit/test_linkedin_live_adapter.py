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

from capture_spine.linkedin_lane.models import (
    CandidateClass,
    MethodMode,
    MinimizationRule,
    RunEnvelope,
    SourceSurface,
    StopReason,
)
from capture_spine.linkedin_lane.validation import validate_candidate_row
from capture_spine.linkedin_live_adapter import (
    LinkedInLaneError,
    LiveAccessEnvelope,
    LiveAccessMode,
    LiveObservation,
    project_observation_to_candidate_row,
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


def test_observation_visible_influence_free_text_raises() -> None:
    # Cross-vendor F1, now enforced at the OBSERVATION gate (not only at projection):
    # a short prose value in a count/band field is rejected by the shared guard.
    bad = _observation(visible_follower_count_or_none="ex-Google fintech PM, ten years").to_dict()
    with pytest.raises(LinkedInLaneError) as exc:
        validate_live_observation(bad)
    assert exc.value.code == "invalid_visible_influence_number"


def test_observation_visible_influence_oversized_raises() -> None:
    # A format-valid but over-length value trips the length cap (distinct code).
    bad = _observation(visible_connection_count_band_or_none="1" * 65).to_dict()
    with pytest.raises(LinkedInLaneError) as exc:
        validate_live_observation(bad)
    assert exc.value.code == "oversized_visible_influence_number"


def test_observation_valid_visible_influence_passes() -> None:
    validate_live_observation(
        _observation(
            visible_follower_count_or_none="12,345",
            visible_connection_count_band_or_none="500+",
        ).to_dict()
    )


# --- carried-field closed-value / shape gate (cross-vendor 3c-1 review fold) ---

def test_observation_invalid_source_surface_raises() -> None:
    bad = _observation(observed_source_surface="totally_made_up_surface").to_dict()
    with pytest.raises(LinkedInLaneError) as exc:
        validate_live_observation(bad)
    assert exc.value.code == "invalid_observed_source_surface"


def test_observation_invalid_minimization_rule_raises() -> None:
    bad = _observation(minimization_rule="keep everything actually").to_dict()
    with pytest.raises(LinkedInLaneError) as exc:
        validate_live_observation(bad)
    assert exc.value.code == "invalid_minimization_rule"


def test_observation_invalid_person_data_minimized_raises() -> None:
    # A business observation with a garbage person_data_minimized value: the person
    # gate would not catch it (non-person), so the carried-field closed-value check does.
    bad = _observation(person_data_minimized="some smuggled narrative").to_dict()
    with pytest.raises(LinkedInLaneError) as exc:
        validate_live_observation(bad)
    assert exc.value.code == "invalid_person_data_minimized"


def test_observation_unsafe_id_raises() -> None:
    bad = _observation(observation_id="obs 0001 with a pasted bio paragraph and spaces").to_dict()
    with pytest.raises(LinkedInLaneError) as exc:
        validate_live_observation(bad)
    assert exc.value.code == "invalid_observation_id"


def test_observation_bad_provenance_timestamp_raises() -> None:
    bad = _observation(provenance_timestamp="last Tuesday afternoon").to_dict()
    with pytest.raises(LinkedInLaneError) as exc:
        validate_live_observation(bad)
    assert exc.value.code == "invalid_provenance_timestamp"


def test_observation_timestamp_plus_utc_offset_passes() -> None:
    # F2 (v1 review): +00:00 is a legitimate ISO-8601 UTC spelling (e.g. from
    # datetime.isoformat()) and must not be false-rejected.
    validate_live_observation(
        _observation(provenance_timestamp="2026-06-10T00:00:00+00:00").to_dict()
    )


def test_observation_exclusions_must_be_empty_raises() -> None:
    # F1 (v1 review): the gate must reject carried exclusion content for ANY caller,
    # not only rely on the minimizer forcing it safe.
    bad = _observation().to_dict()
    bad["exclusions"] = ["a pasted narrative masquerading as an exclusion receipt"]
    with pytest.raises(LinkedInLaneError) as exc:
        validate_live_observation(bad)
    assert exc.value.code == "invalid_observation_exclusions"


# --- slice 3b-2: projection (LiveObservation -> CandidateRow) + mint-path + binding ---

def _run_envelope(**overrides) -> RunEnvelope:
    fields = dict(
        run_id="linkedin_lane_pilot_001",
        declared_theme_or_decision_context="competitor pricing and packaging moves in the X market",
        run_purpose="map competitor pricing changes for a planning review",
        candidate_classes=(CandidateClass.BUSINESS, CandidateClass.PUBLIC_PROFESSIONAL_ACTOR),
        source_surface_allowlist=(
            SourceSurface.COMPANY_WEBSITE_BLOG_PRESS_PRICING,
            SourceSurface.CONFERENCE_PODCAST_NEWSLETTER_PUBLICATION,
        ),
        method_mode=MethodMode.MANUAL_OPERATOR_BROWSING,
        stop_condition=StopReason.CAPS_REACHED,
        source_policy_posture="discoverable_or_entitled_disclosable",
        minimization_rule=MinimizationRule.BUSINESS_ENTITY_ONLY,
        promotion_owner="eric",
        max_businesses=25,
        max_organizations=5,
        max_people=10,
        max_source_surfaces=5,
        time_window_days=30,
    )
    fields.update(overrides)
    return RunEnvelope(**fields)


def _project_business(**overrides):
    kwargs = dict(
        observation=_observation(),
        access_envelope=_envelope(),
        run_envelope=_run_envelope(),
        candidate_class=CandidateClass.BUSINESS,
        business_relevance_note="ships a directly competing pricing page in our segment",
    )
    kwargs.update(overrides)
    return project_observation_to_candidate_row(**kwargs)


# --- positive / mint-path ---

def test_project_business_observation_mints_valid_candidate_row() -> None:
    row = _project_business()
    # The returned dict is already validated; prove the mint-path invariant by
    # re-validating it (the exported function returns ONLY validated rows).
    validate_candidate_row(row)
    assert row["candidate_class"] == "business"
    assert row["entity_type"] == "business_entity"
    assert row["method_mode"] == "manual_operator_browsing"
    assert row["privacy_sensitivity"] == "business_low"
    assert row["source_policy_posture"] == "discoverable_or_entitled_disclosable"
    assert row["run_id"] == "linkedin_lane_pilot_001"
    assert row["source_family"] == "linkedin_adjacent"
    assert row["promotion_required"] is True
    assert row["allowed_downstream_use"] == "planning_only"


def test_project_person_observation_mints_valid_candidate_row() -> None:
    row = project_observation_to_candidate_row(
        observation=_person_observation(),
        access_envelope=_envelope(),
        run_envelope=_run_envelope(),
        candidate_class=CandidateClass.PUBLIC_PROFESSIONAL_ACTOR,
        business_relevance_note="keynote framing signals the competitor's roadmap direction",
    )
    validate_candidate_row(row)
    assert row["entity_type"] == "individual_person"
    assert row["privacy_sensitivity"] == "public_actor_strict"
    assert row["person_data_minimized"] == "yes"
    assert row["senior_role_or_public_actor_basis_or_none"]


def test_project_owner_present_automation_maps_method_mode_and_poc_flag() -> None:
    row = _project_business(
        access_envelope=_envelope(
            live_access_mode=LiveAccessMode.OWNER_PRESENT_ATTENDED_AUTOMATION,
            optional_poc_risk_mode=True,
        ),
    )
    assert row["method_mode"] == "owner_present_attended_automation_optional_poc_risk"
    assert row["optional_poc_risk_mode"] is True


def test_project_carries_minimized_visible_influence_numbers() -> None:
    row = _project_business(
        observation=_observation(
            visible_follower_count_or_none="12,345",
            visible_connection_count_band_or_none="500+",
        )
    )
    assert row["visible_influence_numbers_or_none"] == {
        "follower_count_or_none": "12,345",
        "connection_count_band_or_none": "500+",
        "subscriber_count_or_none": None,
        "engagement_count_or_none": None,
    }


def test_project_visible_influence_free_text_smuggling_raises() -> None:
    # F1 (cross-vendor): a gross over-capture in a "count" field exceeds the cap.
    with pytest.raises(LinkedInLaneError) as exc:
        _project_business(
            observation=_observation(
                visible_follower_count_or_none=("copied profile body with narrative text " * 20)
            )
        )
    assert exc.value.code == "oversized_visible_influence_number"


def test_project_visible_influence_short_freetext_raises() -> None:
    # Home-model add: a SHORT prose smuggle (under the length cap) must still be
    # rejected by the count/band format gate -- pins invalid_ distinct from oversized_.
    with pytest.raises(LinkedInLaneError) as exc:
        _project_business(
            observation=_observation(visible_follower_count_or_none="ex-Google fintech PM"),
        )
    assert exc.value.code == "invalid_visible_influence_number"


def test_project_drops_unmapped_observation_location() -> None:
    # observed_location_or_none has no CandidateRow target -- it must be dropped,
    # not smuggled. observed_public_role_or_title_or_none IS carried.
    row = _project_business(
        observation=_observation(
            observed_location_or_none="London, UK",
            observed_public_role_or_title_or_none="enterprise pricing page",
        ),
    )
    assert "observed_location_or_none" not in row
    assert "London, UK" not in row.values()
    assert row["role_or_influence_basis_or_none"] == "enterprise pricing page"


# --- negatives: every one raises with a pinned code ---

def test_project_live_access_id_mismatch_raises() -> None:
    with pytest.raises(LinkedInLaneError) as exc:
        _project_business(observation=_observation(live_access_id="live-9999"))
    assert exc.value.code == "live_access_id_mismatch"


def test_project_run_id_mismatch_raises() -> None:
    with pytest.raises(LinkedInLaneError) as exc:
        _project_business(run_envelope=_run_envelope(run_id="some_other_run"))
    assert exc.value.code == "run_id_mismatch"


def test_project_undeclared_candidate_class_raises() -> None:
    with pytest.raises(LinkedInLaneError) as exc:
        _project_business(candidate_class=CandidateClass.EXECUTIVE)
    assert exc.value.code == "candidate_class_not_declared"


def test_project_undeclared_source_surface_raises() -> None:
    # The run envelope did not declare manual_search_result_review as a surface.
    with pytest.raises(LinkedInLaneError) as exc:
        _project_business(
            observation=_observation(observed_source_surface="manual_search_result_review"),
        )
    assert exc.value.code == "source_surface_not_declared"


def test_project_empty_business_relevance_note_raises() -> None:
    # The operator judgment is required; the candidate-row gate rejects an empty note.
    with pytest.raises(LinkedInLaneError) as exc:
        _project_business(business_relevance_note="   ")
    assert exc.value.code == "missing_required_candidate_field"


def test_project_invalid_observation_does_not_bypass_shape_gate() -> None:
    # A minimization-boundary breach on the observation must raise INSIDE the
    # projection (it runs validate_live_observation first -- no mint without it).
    with pytest.raises(LinkedInLaneError) as exc:
        _project_business(observation=_observation(profile_body_captured=True))
    assert exc.value.code == "forbidden_profile_body_captured"
