from __future__ import annotations

from schemas.case_models import BandInputs
from schemas.scoring_models import ActionBandResult, BandStatus, MappingTraceStep
from harness_utils import MAPPING_TABLE_VERSION

BASE_CEILING = {
    "none": 0,
    "weak": 3,
    "moderate": 5,
    "strong": 7,
}

EVIDENCE_INDEPENDENCE_DELTA = {
    "correlated": -1,
    "partially_independent": 0,
    "independent": 1,
}

LOSS_SHAPE_CAP = {
    "symmetric": 8,
    "asymmetric_down": 6,
    "ruinous_tail": 3,
    "unknown": 4,
}

REVERSIBILITY_FEASIBILITY_CAP = {
    "low": 3,
    "medium": 5,
    "high": 8,
}

REVERSIBILITY_COST_CAP = {
    "low": 8,
    "medium": 6,
    "high": 5,
    "ruinous": 3,
}

AUTHORITY_CAP = {
    "absent": 1,
    "partial": 5,
    "full": 8,
}

AUTHORITY_ACQUISITION_CAP = {
    "low": 6,
    "medium": 5,
    "high": 3,
    "impossible": 1,
}

CAPABILITY_CAP = {
    "absent": 1,
    "partial": 5,
    "full": 8,
}

CAPABILITY_BUILD_CAP = {
    "low": 6,
    "medium": 5,
    "high": 3,
    "impossible": 1,
}

OPPORTUNITY_COST_FLOOR = {
    "none": 0,
    "low": 1,
    "moderate": 3,
    "severe": 5,
}

INFORMATION_DECAY_FLOOR = {
    "none": 0,
    "slow": 1,
    "fast": 3,
    "expiring": 5,
}

OPTION_VALUE_FLOOR = {
    "none": 0,
    "low": 1,
    "moderate": 3,
    "high": 4,
}

UPSIDE_SHAPE_FLOOR = {
    "none": 0,
    "symmetric": 1,
    "asymmetric_up": 3,
    "convex": 4,
    "once_only_window": 5,
}

URGENCY_FLOOR = {
    "none": 0,
    "low": 1,
    "medium": 3,
    "critical": 5,
}

EVIDENCE_STRENGTH_FLOOR_CAP = {
    "none": 1,
    "weak": 3,
    "moderate": 6,
    "strong": 8,
}

LOSS_SHAPE_FLOOR_CAP = {
    "symmetric": 8,
    "asymmetric_down": 5,
    "ruinous_tail": 3,
    "unknown": 4,
}

AUTHORITY_FLOOR_CAP = {
    "absent": 6,
    "partial": 6,
    "full": 8,
}

CAPABILITY_FLOOR_CAP = {
    "absent": 6,
    "partial": 6,
    "full": 8,
}


def _clamp(value: int, lower: int, upper: int) -> int:
    return max(lower, min(upper, value))


def derive_action_band(inputs: BandInputs) -> ActionBandResult:
    trace: list[MappingTraceStep] = []

    base_ceiling = BASE_CEILING[inputs.evidence_strength]
    trace.append(
        MappingTraceStep(
            step_name="base_ceiling",
            input_name="evidence_strength",
            input_value=inputs.evidence_strength,
            effect=f"base_ceiling={base_ceiling}",
        )
    )

    evidence_adjusted_ceiling = _clamp(
        base_ceiling + EVIDENCE_INDEPENDENCE_DELTA[inputs.evidence_independence],
        0,
        8,
    )
    trace.append(
        MappingTraceStep(
            step_name="evidence_adjusted_ceiling",
            input_name="evidence_independence",
            input_value=inputs.evidence_independence,
            effect=f"evidence_adjusted_ceiling={evidence_adjusted_ceiling}",
        )
    )

    authority_acquisition_cap = (
        8
        if inputs.authority == "full"
        else AUTHORITY_ACQUISITION_CAP[inputs.authority_acquisition_cost]
    )
    capability_build_cap = (
        8
        if inputs.capability == "full"
        else CAPABILITY_BUILD_CAP[inputs.capability_build_cost]
    )

    caps = {
        "loss_shape_cap": LOSS_SHAPE_CAP[inputs.loss_shape],
        "reversibility_feasibility_cap": REVERSIBILITY_FEASIBILITY_CAP[inputs.reversibility_feasibility],
        "reversibility_cost_cap": REVERSIBILITY_COST_CAP[inputs.reversibility_cost],
        "authority_cap": AUTHORITY_CAP[inputs.authority],
        "authority_acquisition_cost_cap": authority_acquisition_cap,
        "capability_cap": CAPABILITY_CAP[inputs.capability],
        "capability_build_cost_cap": capability_build_cap,
    }
    raw_ceiling = min([evidence_adjusted_ceiling, *caps.values()])
    trace.append(
        MappingTraceStep(
            step_name="constraint_caps",
            effect=f"raw_ceiling={raw_ceiling}; caps={caps}",
        )
    )

    floors = {
        "opportunity_cost_floor": OPPORTUNITY_COST_FLOOR[inputs.opportunity_cost],
        "information_decay_floor": INFORMATION_DECAY_FLOOR[inputs.information_decay],
        "option_value_floor": OPTION_VALUE_FLOOR[inputs.option_value],
        "upside_shape_floor": UPSIDE_SHAPE_FLOOR[inputs.upside_shape],
        "urgency_floor": URGENCY_FLOOR[inputs.urgency],
    }
    raw_floor = max(floors.values())
    trace.append(
        MappingTraceStep(
            step_name="action_pressure_floors",
            effect=f"raw_floor={raw_floor}; floors={floors}",
        )
    )

    dampeners = {
        "evidence_strength_floor_cap": EVIDENCE_STRENGTH_FLOOR_CAP[inputs.evidence_strength],
        "loss_shape_floor_cap": LOSS_SHAPE_FLOOR_CAP[inputs.loss_shape],
        "authority_floor_cap": AUTHORITY_FLOOR_CAP[inputs.authority],
        "capability_floor_cap": CAPABILITY_FLOOR_CAP[inputs.capability],
    }
    dampened_floor = min([raw_floor, *dampeners.values()])
    trace.append(
        MappingTraceStep(
            step_name="floor_dampeners",
            effect=f"dampened_floor={dampened_floor}; dampeners={dampeners}",
        )
    )

    warnings: list[str] = []
    if dampened_floor > raw_ceiling:
        if min(caps["authority_cap"], caps["authority_acquisition_cost_cap"]) < 6:
            warnings.append("escalation_forced_under_authority_cap_below_6")
        if min(caps["capability_cap"], caps["capability_build_cost_cap"]) < 6:
            warnings.append("escalation_forced_under_capability_cap_below_6")
        trace.append(
            MappingTraceStep(
                step_name="conflict_resolution",
                effect="dampened_floor > raw_ceiling -> canonical escalation 6..6",
            )
        )
        return ActionBandResult(
            mapping_table_version=MAPPING_TABLE_VERSION,
            action_floor=6,
            action_ceiling=6,
            band_status=BandStatus.CONFLICT_ESCALATE,
            band_width=0,
            mapping_trace=trace,
            warnings=warnings,
        )

    band_width = raw_ceiling - dampened_floor
    band_status = (
        BandStatus.LOW_PRECISION_BAND if band_width > 3 else BandStatus.NORMAL
    )
    trace.append(
        MappingTraceStep(
            step_name="band_status",
            effect=f"band_width={band_width}; band_status={band_status.value}",
        )
    )
    return ActionBandResult(
        mapping_table_version=MAPPING_TABLE_VERSION,
        action_floor=dampened_floor,
        action_ceiling=raw_ceiling,
        band_status=band_status,
        band_width=band_width,
        mapping_trace=trace,
        warnings=warnings,
    )
