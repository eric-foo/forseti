"""Tests for the LinkedIn live-runtime capture harness (slice 3c-2, no live access).

Exercises run_live_capture entirely offline via a StubFetcher: the legal gate (refuses
without explicit owner authorization + presence), the fetch->minimize->validate->project
wiring, and the cap. No browser, no LinkedIn -- the real BrowserFetcher (3c-2b) is the
only live part and is owner-validated, not tested here.

Fake-success guard: the gate negatives assert run_live_capture RAISES with a pinned
code; the wiring test asserts the minted rows pass validate_candidate_row AND that
planted over-capture in the raw bag is dropped.
"""
from __future__ import annotations

import json

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
from capture_spine.linkedin_live_adapter import LiveAccessEnvelope, LiveAccessMode
from capture_spine.linkedin_live_runtime import (
    CaptureTarget,
    LinkedInLaneError,
    StubFetcher,
    run_live_capture,
)


_LIVE_ACCESS_ID = "live-0001"
_RUN_ID = "linkedin_lane_pilot_001"


def _access_envelope(**overrides) -> LiveAccessEnvelope:
    fields = dict(
        live_access_id=_LIVE_ACCESS_ID,
        run_id=_RUN_ID,
        live_access_mode=LiveAccessMode.ATTENDED_MANUAL,
        source_policy_posture="discoverable_or_entitled_disclosable",
        stop_condition="caps_reached",
        owner_presence_attested=True,
        attended_presence_check_method="operator confirmed present at keyboard during this run",
        caps={"max_profiles": 25, "max_searches": 10},
    )
    fields.update(overrides)
    return LiveAccessEnvelope(**fields)


def _run_envelope(**overrides) -> RunEnvelope:
    fields = dict(
        run_id=_RUN_ID,
        declared_theme_or_decision_context="competitor pricing and packaging moves",
        run_purpose="map competitor pricing changes for a planning review",
        candidate_classes=(CandidateClass.BUSINESS,),
        source_surface_allowlist=(SourceSurface.COMPANY_WEBSITE_BLOG_PRESS_PRICING,),
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


def _raw_bag(locator: str, observation_id: str = "obs-0001", **overrides) -> dict:
    bag = dict(
        observation_id=observation_id,
        live_access_id=_LIVE_ACCESS_ID,
        run_id=_RUN_ID,
        observed_entity_type="business_entity",
        observed_display_name="Competitor X",
        observed_source_surface="company_website_blog_press_pricing",
        observed_source_locator=locator,
        provenance_timestamp="2026-06-10T00:00:00Z",
        minimization_rule="business_entity_only",
        # planted over-capture -- the minimizer must drop it:
        profile_body="SHOULD_BE_DROPPED " * 20,
    )
    bag.update(overrides)
    return bag


def _target(locator: str = "https://competitorx.example/pricing") -> CaptureTarget:
    return CaptureTarget(
        locator=locator,
        candidate_class=CandidateClass.BUSINESS,
        business_relevance_note="ships a directly competing pricing page in our segment",
    )


def _run(**overrides):
    target = overrides.pop("target", _target())
    kwargs = dict(
        access_envelope=_access_envelope(),
        run_envelope=_run_envelope(),
        targets=[target],
        fetcher=StubFetcher({target.locator: _raw_bag(target.locator)}),
        live_run_authorized=True,
        owner_present_confirmed=True,
        max_captures=10,
    )
    kwargs.update(overrides)
    return run_live_capture(**kwargs)


# --- the legal gate: refuse without explicit owner authorization + presence ---

def test_run_refuses_without_live_run_authorization() -> None:
    with pytest.raises(LinkedInLaneError) as exc:
        _run(live_run_authorized=False)
    assert exc.value.code == "live_run_not_authorized"


def test_run_refuses_without_owner_present() -> None:
    with pytest.raises(LinkedInLaneError) as exc:
        _run(owner_present_confirmed=False)
    assert exc.value.code == "owner_not_present"


# --- the wiring: fetch -> minimize -> validate -> project ---

def test_run_wires_pipeline_and_mints_validated_rows() -> None:
    rows = _run()
    assert len(rows) == 1
    row = rows[0]
    validate_candidate_row(row)  # the minted row is a valid candidate row
    assert row["candidate_class"] == "business"
    assert row["run_id"] == _RUN_ID
    # the planted over-capture was dropped by the minimizer
    assert "SHOULD_BE_DROPPED" not in json.dumps(row)


# --- the cap ---

def test_run_stops_at_cap() -> None:
    targets = [_target(f"https://competitorx.example/p{i}") for i in range(3)]
    bags = {t.locator: _raw_bag(t.locator, observation_id=f"obs-{i}") for i, t in enumerate(targets)}
    rows = run_live_capture(
        access_envelope=_access_envelope(),
        run_envelope=_run_envelope(),
        targets=targets,
        fetcher=StubFetcher(bags),
        live_run_authorized=True,
        owner_present_confirmed=True,
        max_captures=2,
    )
    assert len(rows) == 2


def test_run_cap_exceeding_posture_raises() -> None:
    with pytest.raises(LinkedInLaneError) as exc:
        _run(max_captures=999)  # the envelope's declared caps total 35
    assert exc.value.code == "max_captures_exceeds_caps"


def test_run_zero_cap_raises() -> None:
    with pytest.raises(LinkedInLaneError) as exc:
        _run(max_captures=0)
    assert exc.value.code == "invalid_max_captures"


@pytest.mark.parametrize(
    "caps",
    [
        {"max_profiles": "2"},          # string value, not int
        {"max_profiles": True},         # bool value (int subclass) rejected
        {"max_profiles": -1, "max_searches": 3},  # negative cap
        {"": 1},                        # empty cap name
    ],
)
def test_run_rejects_malformed_declared_caps(caps) -> None:
    # Caps are validated at the envelope gate (folded there) -- a malformed declaration
    # is rejected before any capture, not coerced via int() (cross-vendor 3c-2a F1).
    with pytest.raises(LinkedInLaneError) as exc:
        _run(access_envelope=_access_envelope(caps=caps))
    assert exc.value.code == "invalid_cap"


def test_run_rejects_bool_max_captures() -> None:
    with pytest.raises(LinkedInLaneError) as exc:
        _run(max_captures=True)
    assert exc.value.code == "invalid_max_captures"


# --- stub fetcher honesty (no silent pass on a missing fixture) ---

def test_stub_fetcher_unknown_target_raises() -> None:
    with pytest.raises(KeyError):
        StubFetcher({}).fetch("https://unseeded.example/")
