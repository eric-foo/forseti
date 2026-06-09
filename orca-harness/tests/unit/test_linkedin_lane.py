"""Tests for the LinkedIn Lane no-live harness (slice 1).

Fake-success guard: every negative asserts the validator RAISES
``LinkedInLaneError`` on the bad case -- a forbidden field, a person row missing
its public-actor basis or a privacy/minimization flag, non-planning_only output,
a forbidden retained-flag, a secret-like value, and an under-specified run
envelope. Plus a precision test that the allowed ``*_count_or_none`` influence
fields do NOT trip the forbidden-field walk.
"""
from __future__ import annotations

import pytest

from capture_spine.linkedin_lane import (
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
    StopReason,
    VisibleInfluenceNumbers,
    validate_candidate_row,
    validate_run_envelope,
)


def _envelope(**overrides) -> RunEnvelope:
    fields = dict(
        run_id="linkedin_lane_pilot_001",
        declared_theme_or_decision_context="competitor X pricing-sensitivity decision",
        run_purpose="bounded operator pilot for LinkedIn Lane discovery",
        candidate_classes=(CandidateClass.BUSINESS, CandidateClass.SENIOR_DECISION_MAKER),
        source_surface_allowlist=(SourceSurface.OPERATOR_SUPPLIED_SEED_LIST,),
        method_mode=MethodMode.AGENT_ASSISTED_ROWING_ONLY,
        stop_condition=StopReason.CAPS_REACHED,
        source_policy_posture="discoverable_or_entitled_disclosable",
        minimization_rule=MinimizationRule.NAME_ROLE_LOCATOR_ONLY,
        promotion_owner="operator",
        max_businesses=25,
        max_organizations=25,
        max_people=15,
        max_source_surfaces=5,
        time_window_days=30,
    )
    fields.update(overrides)
    return RunEnvelope(**fields)


def _business_row(**overrides) -> CandidateRow:
    fields = dict(
        candidate_id="cand-0001",
        run_id="linkedin_lane_pilot_001",
        candidate_class=CandidateClass.BUSINESS,
        entity_type=EntityType.BUSINESS_ENTITY,
        display_name="Competitor X",
        source_surface=SourceSurface.COMPANY_WEBSITE_BLOG_PRESS_PRICING,
        source_policy_posture="discoverable_or_entitled_disclosable",
        method_mode=MethodMode.AGENT_ASSISTED_ROWING_ONLY,
        declared_theme_or_decision_context="competitor X pricing-sensitivity decision",
        run_purpose="bounded operator pilot",
        business_relevance_note="direct competitor in the declared theme",
        privacy_sensitivity=PrivacySensitivity.BUSINESS_LOW,
        minimization_rule=MinimizationRule.BUSINESS_ENTITY_ONLY,
        person_data_minimized=PersonDataMinimized.NOT_APPLICABLE,
        provenance_timestamp="2026-06-09T00:00:00Z",
    )
    fields.update(overrides)
    return CandidateRow(**fields)


def _person_row(**overrides) -> CandidateRow:
    fields = dict(
        candidate_id="cand-0002",
        run_id="linkedin_lane_pilot_001",
        candidate_class=CandidateClass.SENIOR_DECISION_MAKER,
        entity_type=EntityType.INDIVIDUAL_PERSON,
        display_name="Jane Public",
        source_surface=SourceSurface.CONFERENCE_PODCAST_NEWSLETTER_PUBLICATION,
        source_policy_posture="discoverable_or_entitled_disclosable",
        method_mode=MethodMode.AGENT_ASSISTED_ROWING_ONLY,
        declared_theme_or_decision_context="competitor X pricing-sensitivity decision",
        run_purpose="bounded operator pilot",
        business_relevance_note="named decision-maker for the declared theme",
        privacy_sensitivity=PrivacySensitivity.PUBLIC_ACTOR_STRICT,
        minimization_rule=MinimizationRule.NAME_ROLE_LOCATOR_ONLY,
        person_data_minimized=PersonDataMinimized.YES,
        provenance_timestamp="2026-06-09T00:00:00Z",
        senior_role_or_public_actor_basis_or_none="keynote speaker at a named public conference under her own name",
    )
    fields.update(overrides)
    return CandidateRow(**fields)


# --- positive / round-trip ---

def test_valid_envelope_passes_and_serializes_enums() -> None:
    env = _envelope()
    validate_run_envelope(env)
    dumped = env.to_dict()
    assert dumped["candidate_classes"] == ["business", "senior_decision_maker"]
    assert dumped["stop_condition"] == "caps_reached"
    assert dumped["schema_version"] == "linkedin_lane_run_envelope_v0"


def test_valid_business_and_person_rows_pass() -> None:
    validate_candidate_row(_business_row().to_dict())
    validate_candidate_row(_person_row().to_dict())


def test_row_to_dict_serializes_enums_to_strings() -> None:
    dumped = _person_row().to_dict()
    assert dumped["candidate_class"] == "senior_decision_maker"
    assert dumped["entity_type"] == "individual_person"
    assert dumped["allowed_downstream_use"] == "planning_only"
    assert dumped["promotion_required"] is True


def test_visible_influence_counts_do_not_trip_the_forbidden_walk() -> None:
    # precision check: *_count_or_none is allowed; only follower LISTS are banned
    row = _person_row(
        visible_influence_numbers_or_none=VisibleInfluenceNumbers(
            follower_count_or_none="12k",
            connection_count_band_or_none="500+",
        )
    )
    validate_candidate_row(row.to_dict())


# --- negatives: every one must raise ---

def test_forbidden_field_present_raises() -> None:
    bad = {**_business_row().to_dict(), "followers": ["a", "b", "c"]}
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(bad)


def test_nested_forbidden_field_present_raises() -> None:
    bad = {**_business_row().to_dict(), "extra": {"connection_list": ["x"]}}
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(bad)


def test_person_row_missing_public_actor_basis_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(_person_row(senior_role_or_public_actor_basis_or_none=None).to_dict())


def test_person_row_wrong_privacy_sensitivity_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(_person_row(privacy_sensitivity=PrivacySensitivity.BUSINESS_LOW).to_dict())


def test_person_row_not_applicable_minimized_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(_person_row(person_data_minimized=PersonDataMinimized.NOT_APPLICABLE).to_dict())


def test_non_planning_only_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(_business_row(allowed_downstream_use="capture").to_dict())


def test_wrong_intake_status_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(_business_row(capture_unit_intake_status="promoted").to_dict())


def test_promotion_not_required_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(_business_row(promotion_required=False).to_dict())


def test_retained_contact_fields_flag_true_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(_business_row(contact_fields_retained=True).to_dict())


def test_profile_body_captured_flag_true_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(_business_row(profile_body_captured=True).to_dict())


def test_secret_like_value_raises() -> None:
    bad = _business_row(business_relevance_note="auth via Bearer abcdef0123456789abcdef").to_dict()
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(bad)


def test_envelope_zero_source_surfaces_cap_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_run_envelope(_envelope(max_source_surfaces=0))


def test_envelope_empty_candidate_classes_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_run_envelope(_envelope(candidate_classes=()))


def test_envelope_all_zero_entity_caps_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_run_envelope(_envelope(max_businesses=0, max_organizations=0, max_people=0))


def test_envelope_missing_theme_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_run_envelope(_envelope(declared_theme_or_decision_context="  "))


# --- negatives added after the no-repo delegated review (F1-F4) ---

def test_candidate_row_unknown_or_aliased_field_raises() -> None:
    # F1/F3: a banned concept under an alias key is rejected by the top-level allowlist.
    bad = {**_business_row().to_dict(), "email_or_none": "person@example.com"}
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(bad)


def test_candidate_row_missing_required_field_raises() -> None:
    # F1: an under-specified row (missing display_name) must not pass.
    bad = _business_row().to_dict()
    del bad["display_name"]
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(bad)


def test_candidate_row_missing_entity_type_raises() -> None:
    # F1: a person-shaped row that omits entity_type must not slip past the person gate.
    bad = _person_row().to_dict()
    del bad["entity_type"]
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(bad)


def test_candidate_row_invalid_enum_value_raises() -> None:
    # F1: a garbage closed-enum value is rejected, not silently accepted.
    bad = _business_row().to_dict()
    bad["candidate_class"] = "totally_bogus_class"
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(bad)


def test_candidate_row_wrong_source_family_raises() -> None:
    bad = _business_row().to_dict()
    bad["source_family"] = "some_other_source"
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(bad)


def test_nested_aliased_forbidden_field_raises() -> None:
    # F3: an aliased forbidden key nested under an allowed container is still caught.
    bad = {
        **_business_row().to_dict(),
        "visible_influence_numbers_or_none": {
            "follower_count_or_none": "12k",
            "email_or_none": "person@example.com",
        },
    }
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(bad)


def test_person_row_org_chart_basis_raises() -> None:
    # F2: an excluded basis (org chart) is rejected even though it is non-empty text.
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(
            _person_row(
                senior_role_or_public_actor_basis_or_none="listed in the employer org chart"
            ).to_dict()
        )


def test_person_row_follower_basis_raises() -> None:
    with pytest.raises(LinkedInLaneError):
        validate_candidate_row(
            _person_row(
                senior_role_or_public_actor_basis_or_none="surfaced as a follower of the company page"
            ).to_dict()
        )


def test_envelope_hollow_non_claims_raises() -> None:
    # F4: a non-empty but hollow non_claims override must fail the required-category check.
    with pytest.raises(LinkedInLaneError):
        validate_run_envelope(_envelope(non_claims=("not ready",)))
