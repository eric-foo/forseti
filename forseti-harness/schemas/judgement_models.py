from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from schemas.case_models import StrictModel


class RecommendedAction(StrictModel):
    ladder_level: int = Field(ge=0, le=8)
    action_label: str
    rationale: str


class ContestantBandClaim(StrictModel):
    claimed_floor: int = Field(ge=0, le=8)
    claimed_ceiling: int = Field(ge=0, le=8)
    reasoning: str
    advisory_only: bool = True


class EvidenceUsed(StrictModel):
    claim_id: str
    claim_text: str
    claim_role: Literal["load_bearing", "supporting", "contextual"]
    evidence_unit_ids: list[str]


class LoadBearingAssumption(StrictModel):
    statement: str
    evidence_unit_ids: list[str]
    would_flip_if_false: bool


class BlindJudgement(StrictModel):
    case_id: str
    contestant_id: str
    run_id: str
    model_id: str
    model_family: str
    model_snapshot_if_available: str | None = None
    prompt_hash: str
    temperature: float
    seed_if_supported: int | None = None
    harness_version: str
    judgement_class: Literal["recommend", "abstain", "wait", "escalate", "irreducible_uncertainty"]
    decision_shape: Literal[
        "action_band",
        "ceiling_trap",
        "underreach_trap",
        "abstention_required",
        "false_abstention_trap",
        "escalation_required",
        "forecast_shaped",
        "high_conviction_action",
        "option_creation",
        "unsupported_load_bearing_claim_trap",
        "private_context_dominant",
    ]
    recommended_action: RecommendedAction
    contestant_band_claim: ContestantBandClaim | None = None
    evidence_used: list[EvidenceUsed]
    must_address_items_covered: list[str] = Field(default_factory=list)
    load_bearing_assumption: LoadBearingAssumption | None = None
    advisory_phase_1_fields: dict = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_judgement_class_ladder(self) -> "BlindJudgement":
        ladder_level = self.recommended_action.ladder_level
        judgement_class = self.judgement_class

        if judgement_class == "abstain" and ladder_level != 0:
            raise ValueError("abstain must use ladder level 0")
        if judgement_class == "wait" and ladder_level != 1:
            raise ValueError("wait must use ladder level 1")
        if judgement_class == "escalate" and ladder_level != 6:
            raise ValueError("escalate must use ladder level 6")
        if judgement_class == "irreducible_uncertainty":
            if ladder_level != 0:
                raise ValueError("irreducible_uncertainty must use ladder level 0")
            if not self.must_address_items_covered:
                raise ValueError("irreducible_uncertainty requires must-address coverage")
        if judgement_class == "recommend" and ladder_level not in {2, 3, 4, 5, 7, 8}:
            raise ValueError("recommend must use levels 2, 3, 4, 5, 7, or 8")
        return self
