"""Tests for the LinkedIn live-runtime (slice 3c-1): read-time minimizer.

The TAPE-TEST: feed an over-captured raw bag (legit minimized crumbs + planted
forbidden over-capture -- a profile body, an email, a follower list, raw html, True
retained-flags) and prove the minimizer keeps ONLY the crumbs and the forbidden
content is GONE from the output (and the output passes the §6.2 observation gate). No
live access: the bag is an offline fixture (a dict), never a real page.

Fake-success guard: the negatives assert validate RAISES with a pinned code; the
tape-test asserts the planted forbidden strings are ABSENT from the serialized output.
"""
from __future__ import annotations

import json

import pytest

from capture_spine.linkedin_live_adapter import validate_live_observation
from capture_spine.linkedin_live_runtime import (
    LinkedInLaneError,
    minimize_capture_to_observation,
)


_PLANTED_EMAIL = "ceo@competitorx.example"
_PLANTED_BIO = "FULL_BIO_NARRATIVE " * 40  # a copied profile body
_PLANTED_FOLLOWER = "alice_should_be_dropped"


def _over_captured_business_bag(**overrides) -> dict:
    bag = dict(
        # legit minimized crumbs
        observation_id="obs-0001",
        live_access_id="live-0001",
        run_id="linkedin_lane_pilot_001",
        observed_entity_type="business_entity",
        observed_display_name="Competitor X",
        observed_source_surface="company_website_blog_press_pricing",
        observed_source_locator="https://competitorx.example/pricing",
        provenance_timestamp="2026-06-10T00:00:00Z",
        minimization_rule="business_entity_only",
        # PLANTED forbidden over-capture -- must all be dropped:
        profile_body=_PLANTED_BIO,
        email=_PLANTED_EMAIL,
        follower_list=[_PLANTED_FOLLOWER, "bob", "carol"],
        raw_html="<html><body>...</body></html>",
        about_section="lots of narrative text",
        # planted True retained-flags -- must be forced safe (never carried):
        contact_fields_retained=True,
        profile_body_captured=True,
    )
    bag.update(overrides)
    return bag


def test_minimize_drops_over_captured_content_tape_test() -> None:
    obs = minimize_capture_to_observation(_over_captured_business_bag())
    result = obs.to_dict()
    # the minimized output passes the §6.2 observation gate
    validate_live_observation(result)
    # the forbidden KEYS are not present on the observation
    for forbidden_key in ("profile_body", "email", "follower_list", "raw_html", "about_section"):
        assert forbidden_key not in result
    # the forbidden VALUES are gone from the serialized output
    serialized = json.dumps(result)
    assert _PLANTED_EMAIL not in serialized
    assert _PLANTED_FOLLOWER not in serialized
    assert "FULL_BIO_NARRATIVE" not in serialized
    # the planted True flags were forced to the safe default
    assert result["contact_fields_retained"] is False
    assert result["profile_body_captured"] is False
    # the allowed crumbs survived
    assert result["observed_display_name"] == "Competitor X"
    assert result["schema_version"] == "linkedin_live_observation_v0"


def test_minimize_oversized_smuggle_in_allowed_field_raises() -> None:
    # Content smuggled INTO an allowed field (a bio pasted into the display name) is
    # caught by the observation gate's length cap, on the minimizer's output.
    bag = _over_captured_business_bag(observed_display_name="x" * 600)
    with pytest.raises(LinkedInLaneError) as exc:
        minimize_capture_to_observation(bag)
    assert exc.value.code == "oversized_observed_display_name"


def test_minimize_influence_smuggle_in_allowed_field_raises() -> None:
    # Prose smuggled into a count/band field is caught by the shared influence guard.
    bag = _over_captured_business_bag(visible_follower_count_or_none="ex-Google fintech PM")
    with pytest.raises(LinkedInLaneError) as exc:
        minimize_capture_to_observation(bag)
    assert exc.value.code == "invalid_visible_influence_number"


def test_minimize_missing_required_field_raises() -> None:
    bag = _over_captured_business_bag()
    del bag["observed_display_name"]
    with pytest.raises(LinkedInLaneError) as exc:
        minimize_capture_to_observation(bag)
    assert exc.value.code == "missing_observed_display_name"


def test_minimize_non_mapping_raises() -> None:
    with pytest.raises(LinkedInLaneError) as exc:
        minimize_capture_to_observation(["not", "a", "bag"])  # type: ignore[arg-type]
    assert exc.value.code == "invalid_raw_capture"


def test_minimize_person_bag_produces_valid_person_observation() -> None:
    bag = _over_captured_business_bag(
        observation_id="obs-0002",
        observed_entity_type="individual_person",
        observed_display_name="Jane Public",
        observed_source_surface="conference_podcast_newsletter_publication",
        observed_source_locator="https://conf.example/speakers/jane-public",
        minimization_rule="name_role_locator_only",
        person_data_minimized="yes",
        senior_role_or_public_actor_basis_or_none="keynote speaker at a named public conference under her own name",
    )
    obs = minimize_capture_to_observation(bag)
    result = obs.to_dict()
    validate_live_observation(result)
    assert result["observed_entity_type"] == "individual_person"
    assert result["person_data_minimized"] == "yes"
    # forbidden over-capture still dropped on the person path
    assert "FULL_BIO_NARRATIVE" not in json.dumps(result)


def test_minimize_drops_raw_exclusions() -> None:
    # exclusions is a runtime-generated receipt, not raw page text -- the minimizer
    # forces it to the safe default rather than carrying narrative from the bag.
    obs = minimize_capture_to_observation(
        _over_captured_business_bag(exclusions=["a pasted narrative masquerading as an exclusion receipt"])
    )
    assert obs.to_dict()["exclusions"] == []


def test_minimize_smuggle_via_minimization_rule_now_caught() -> None:
    # The carried-but-unchecked smuggle path (cross-vendor 3c-1 finding) is now closed
    # at the observation gate, which the minimizer runs on its output.
    bag = _over_captured_business_bag(minimization_rule="keep the whole bio please")
    with pytest.raises(LinkedInLaneError) as exc:
        minimize_capture_to_observation(bag)
    assert exc.value.code == "invalid_minimization_rule"


def test_minimize_clean_business_bag_happy_path() -> None:
    bag = dict(
        observation_id="obs-0003",
        live_access_id="live-0001",
        run_id="linkedin_lane_pilot_001",
        observed_entity_type="business_entity",
        observed_display_name="Competitor Y",
        observed_source_surface="company_website_blog_press_pricing",
        observed_source_locator="https://competitory.example/",
        provenance_timestamp="2026-06-10T00:00:00Z",
        minimization_rule="business_entity_only",
        visible_follower_count_or_none="12,345",
    )
    obs = minimize_capture_to_observation(bag)
    result = obs.to_dict()
    validate_live_observation(result)
    assert result["observed_display_name"] == "Competitor Y"
    assert result["visible_follower_count_or_none"] == "12,345"
