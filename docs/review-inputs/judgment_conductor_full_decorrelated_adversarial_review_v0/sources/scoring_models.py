from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import Field, field_validator

from harness_utils import NON_CLAIM_NOTICE
from schemas.case_models import StrictModel


class BandStatus(StrEnum):
    NORMAL = "normal"
    LOW_PRECISION_BAND = "low_precision_band"
    CONFLICT_ESCALATE = "conflict_escalate"


class MappingTraceStep(StrictModel):
    step_name: str
    input_name: str | None = None
    input_value: str | None = None
    effect: str


class ActionBandResult(StrictModel):
    mapping_table_version: str
    action_floor: int = Field(ge=0, le=8)
    action_ceiling: int = Field(ge=0, le=8)
    band_status: BandStatus
    band_width: int
    mapping_trace: list[MappingTraceStep]
    warnings: list[str] = Field(default_factory=list)


class EvidenceIdCheckResult(StrictModel):
    evidence_id_presence_pass: bool
    pre_decision_status_pass: bool
    load_bearing_claim_citation_pass: bool
    missing_evidence_ids: list[str] = Field(default_factory=list)
    excluded_evidence_ids_cited: list[str] = Field(default_factory=list)
    uncertain_timestamp_evidence_ids_cited: list[str] = Field(default_factory=list)


class MustAddressCoverageResult(StrictModel):
    pass_: bool = Field(alias="pass")
    covered_ids: list[str]
    missed_ids: list[str]


class FailureEvent(StrictModel):
    event_id: str
    created_at: str
    harness_version: str
    batch_id: str | None = None
    case_id: str | None = None
    contestant_id: str | None = None
    run_id: str | None = None
    scoring_result_ref: str | None = None
    scoring_result_hash: str | None = None
    failure_type: str
    severity: Literal["info", "minor", "material", "blocking"]
    mechanical_source: str
    details: dict
    not_a_rule: bool = True
    promotion_allowed: bool = False

    @field_validator("promotion_allowed")
    @classmethod
    def reject_promotion(cls, value: bool) -> bool:
        if value:
            raise ValueError("promotion_allowed must remain false in Phase 1")
        return value


class ScoringResult(StrictModel):
    scoring_result_id: str
    case_id: str
    contestant_id: str
    run_id: str
    blind_judgement_hash: str
    facilitator_ledger_hash: str
    participant_packet_hash: str
    mapping_table_version: str
    labeling_rubric_version: str
    action_band_result: ActionBandResult
    recommended_level: int
    in_band: bool
    over_band: bool
    under_band: bool
    overreach_distance: int
    underreach_distance: int
    underreach_primary: bool
    evidence_id_check_result: EvidenceIdCheckResult
    must_address_coverage_result: MustAddressCoverageResult
    memorization_probe_result: Literal["pass", "fail", "ambiguous", "not_run"]
    failure_event_ids: list[str] = Field(default_factory=list)
    scored_at: str
    scorer_version: str


class ContestantScoreSummary(StrictModel):
    contestant_id: str
    run_id: str
    scoring_result_id: str
    in_band: bool
    over_band: bool
    under_band: bool
    overreach_distance: int
    underreach_distance: int
    blocking_failures: int


class CaseReport(StrictModel):
    case_id: str
    batch_id: str
    mapping_table_version: str
    facilitator_ledger_hash: str
    contestant_results: list[ContestantScoreSummary]
    failure_event_summary: dict
    non_claim_notice: str
    generated_at: str

    @field_validator("non_claim_notice")
    @classmethod
    def validate_non_claim_notice(cls, value: str) -> str:
        if value != NON_CLAIM_NOTICE:
            raise ValueError("non_claim_notice must match the exact required claim boundary")
        return value
