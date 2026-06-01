from __future__ import annotations

from schemas.case_models import BandInputs
from scoring.mapping_table import (
    AUTHORITY_ACQUISITION_CAP,
    AUTHORITY_CAP,
    AUTHORITY_FLOOR_CAP,
    BASE_CEILING,
    CAPABILITY_BUILD_CAP,
    CAPABILITY_CAP,
    CAPABILITY_FLOOR_CAP,
    EVIDENCE_INDEPENDENCE_DELTA,
    EVIDENCE_STRENGTH_FLOOR_CAP,
    INFORMATION_DECAY_FLOOR,
    LOSS_SHAPE_CAP,
    LOSS_SHAPE_FLOOR_CAP,
    OPPORTUNITY_COST_FLOOR,
    OPTION_VALUE_FLOOR,
    REVERSIBILITY_COST_CAP,
    REVERSIBILITY_FEASIBILITY_CAP,
    UPSIDE_SHAPE_FLOOR,
    URGENCY_FLOOR,
    derive_action_band,
)


def test_frozen_v0_14_mapping_tables() -> None:
    assert BASE_CEILING == {"none": 0, "weak": 3, "moderate": 5, "strong": 7}
    assert EVIDENCE_INDEPENDENCE_DELTA == {
        "correlated": -1,
        "partially_independent": 0,
        "independent": 1,
    }
    assert LOSS_SHAPE_CAP == {
        "symmetric": 8,
        "asymmetric_down": 6,
        "ruinous_tail": 3,
        "unknown": 4,
    }
    assert REVERSIBILITY_FEASIBILITY_CAP == {"low": 3, "medium": 5, "high": 8}
    assert REVERSIBILITY_COST_CAP == {"low": 8, "medium": 6, "high": 5, "ruinous": 3}
    assert AUTHORITY_CAP == {"absent": 1, "partial": 5, "full": 8}
    assert AUTHORITY_ACQUISITION_CAP == {"low": 6, "medium": 5, "high": 3, "impossible": 1}
    assert CAPABILITY_CAP == {"absent": 1, "partial": 5, "full": 8}
    assert CAPABILITY_BUILD_CAP == {"low": 6, "medium": 5, "high": 3, "impossible": 1}
    assert OPPORTUNITY_COST_FLOOR == {"none": 0, "low": 1, "moderate": 3, "severe": 5}
    assert INFORMATION_DECAY_FLOOR == {"none": 0, "slow": 1, "fast": 3, "expiring": 5}
    assert OPTION_VALUE_FLOOR == {"none": 0, "low": 1, "moderate": 3, "high": 4}
    assert UPSIDE_SHAPE_FLOOR == {
        "none": 0,
        "symmetric": 1,
        "asymmetric_up": 3,
        "convex": 4,
        "once_only_window": 5,
    }
    assert URGENCY_FLOOR == {"none": 0, "low": 1, "medium": 3, "critical": 5}
    assert EVIDENCE_STRENGTH_FLOOR_CAP == {"none": 1, "weak": 3, "moderate": 6, "strong": 8}
    assert LOSS_SHAPE_FLOOR_CAP == {
        "symmetric": 8,
        "asymmetric_down": 5,
        "ruinous_tail": 3,
        "unknown": 4,
    }
    assert AUTHORITY_FLOOR_CAP == {"absent": 6, "partial": 6, "full": 8}
    assert CAPABILITY_FLOOR_CAP == {"absent": 6, "partial": 6, "full": 8}


def test_tr_casetext_conflict_escalates_to_exact_six() -> None:
    result = derive_action_band(
        BandInputs(
            evidence_strength="moderate",
            evidence_independence="partially_independent",
            reversibility_feasibility="low",
            reversibility_cost="high",
            authority="partial",
            authority_acquisition_cost="medium",
            capability="partial",
            capability_build_cost="high",
            loss_shape="asymmetric_down",
            opportunity_cost="moderate",
            information_decay="fast",
            option_value="high",
            upside_shape="asymmetric_up",
            urgency="medium",
        )
    )
    assert result.action_floor == 6
    assert result.action_ceiling == 6
    assert result.band_status.value == "conflict_escalate"


def test_option_value_moderate_produces_three_to_three_normal() -> None:
    result = derive_action_band(
        BandInputs(
            evidence_strength="moderate",
            evidence_independence="partially_independent",
            reversibility_feasibility="low",
            reversibility_cost="high",
            authority="partial",
            authority_acquisition_cost="medium",
            capability="partial",
            capability_build_cost="high",
            loss_shape="asymmetric_down",
            opportunity_cost="moderate",
            information_decay="fast",
            option_value="moderate",
            upside_shape="asymmetric_up",
            urgency="medium",
        )
    )
    assert result.action_floor == 3
    assert result.action_ceiling == 3
    assert result.band_status.value == "normal"


def test_low_precision_boundary() -> None:
    result = derive_action_band(
        BandInputs(
            evidence_strength="strong",
            evidence_independence="independent",
            reversibility_feasibility="high",
            reversibility_cost="low",
            authority="full",
            authority_acquisition_cost="low",
            capability="full",
            capability_build_cost="low",
            loss_shape="symmetric",
            opportunity_cost="low",
            information_decay="none",
            option_value="none",
            upside_shape="none",
            urgency="low",
        )
    )
    assert result.action_floor == 1
    assert result.action_ceiling == 8
    assert result.band_status.value == "low_precision_band"


def test_band_status_domain_does_not_include_ceiling_trap() -> None:
    result = derive_action_band(
        BandInputs(
            evidence_strength="weak",
            evidence_independence="correlated",
            reversibility_feasibility="medium",
            reversibility_cost="medium",
            authority="partial",
            authority_acquisition_cost="medium",
            capability="partial",
            capability_build_cost="medium",
            loss_shape="unknown",
            opportunity_cost="low",
            information_decay="slow",
            option_value="low",
            upside_shape="none",
            urgency="none",
        )
    )
    assert result.band_status.value in {"normal", "low_precision_band", "conflict_escalate"}
    assert result.band_status.value != "ceiling_trap"


def test_full_authority_ignores_authority_acquisition_cost() -> None:
    low = derive_action_band(
        BandInputs(
            evidence_strength="strong",
            evidence_independence="independent",
            reversibility_feasibility="high",
            reversibility_cost="low",
            authority="full",
            authority_acquisition_cost="low",
            capability="full",
            capability_build_cost="low",
            loss_shape="symmetric",
            opportunity_cost="none",
            information_decay="none",
            option_value="none",
            upside_shape="none",
            urgency="none",
        )
    )
    impossible = derive_action_band(
        BandInputs(
            evidence_strength="strong",
            evidence_independence="independent",
            reversibility_feasibility="high",
            reversibility_cost="low",
            authority="full",
            authority_acquisition_cost="impossible",
            capability="full",
            capability_build_cost="low",
            loss_shape="symmetric",
            opportunity_cost="none",
            information_decay="none",
            option_value="none",
            upside_shape="none",
            urgency="none",
        )
    )
    assert low.action_ceiling == impossible.action_ceiling == 8


def test_full_capability_ignores_capability_build_cost() -> None:
    low = derive_action_band(
        BandInputs(
            evidence_strength="strong",
            evidence_independence="independent",
            reversibility_feasibility="high",
            reversibility_cost="low",
            authority="full",
            authority_acquisition_cost="low",
            capability="full",
            capability_build_cost="low",
            loss_shape="symmetric",
            opportunity_cost="none",
            information_decay="none",
            option_value="none",
            upside_shape="none",
            urgency="none",
        )
    )
    impossible = derive_action_band(
        BandInputs(
            evidence_strength="strong",
            evidence_independence="independent",
            reversibility_feasibility="high",
            reversibility_cost="low",
            authority="full",
            authority_acquisition_cost="low",
            capability="full",
            capability_build_cost="impossible",
            loss_shape="symmetric",
            opportunity_cost="none",
            information_decay="none",
            option_value="none",
            upside_shape="none",
            urgency="none",
        )
    )
    assert low.action_ceiling == impossible.action_ceiling == 8


def test_all_required_monotonicity_properties_hold() -> None:
    _assert_nondecreasing(BASE_CEILING, ["none", "weak", "moderate", "strong"])
    _assert_nondecreasing(EVIDENCE_INDEPENDENCE_DELTA, ["correlated", "partially_independent", "independent"])
    _assert_nonincreasing(LOSS_SHAPE_CAP, ["symmetric", "asymmetric_down", "unknown", "ruinous_tail"])
    _assert_nondecreasing(REVERSIBILITY_FEASIBILITY_CAP, ["low", "medium", "high"])
    _assert_nonincreasing(REVERSIBILITY_COST_CAP, ["low", "medium", "high", "ruinous"])
    _assert_nondecreasing(AUTHORITY_CAP, ["absent", "partial", "full"])
    _assert_nonincreasing(AUTHORITY_ACQUISITION_CAP, ["low", "medium", "high", "impossible"])
    _assert_nondecreasing(CAPABILITY_CAP, ["absent", "partial", "full"])
    _assert_nonincreasing(CAPABILITY_BUILD_CAP, ["low", "medium", "high", "impossible"])
    _assert_nondecreasing(OPPORTUNITY_COST_FLOOR, ["none", "low", "moderate", "severe"])
    _assert_nondecreasing(INFORMATION_DECAY_FLOOR, ["none", "slow", "fast", "expiring"])
    _assert_nondecreasing(OPTION_VALUE_FLOOR, ["none", "low", "moderate", "high"])
    _assert_nondecreasing(UPSIDE_SHAPE_FLOOR, ["none", "symmetric", "asymmetric_up", "convex", "once_only_window"])
    _assert_nondecreasing(URGENCY_FLOOR, ["none", "low", "medium", "critical"])
    _assert_nondecreasing(EVIDENCE_STRENGTH_FLOOR_CAP, ["none", "weak", "moderate", "strong"])
    _assert_nonincreasing(LOSS_SHAPE_FLOOR_CAP, ["symmetric", "asymmetric_down", "unknown", "ruinous_tail"])
    _assert_nondecreasing(AUTHORITY_FLOOR_CAP, ["absent", "partial", "full"])
    _assert_nondecreasing(CAPABILITY_FLOOR_CAP, ["absent", "partial", "full"])


def _assert_nondecreasing(mapping: dict[str, int], keys: list[str]) -> None:
    values = [mapping[key] for key in keys]
    assert values == sorted(values)


def _assert_nonincreasing(mapping: dict[str, int], keys: list[str]) -> None:
    values = [mapping[key] for key in keys]
    assert values == sorted(values, reverse=True)
