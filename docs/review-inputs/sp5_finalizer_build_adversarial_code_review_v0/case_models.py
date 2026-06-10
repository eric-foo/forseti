from __future__ import annotations

from datetime import date, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class PreDecisionStatus(StrEnum):
    VERIFIED_PRE_DECISION = "verified_pre_decision"
    UNCERTAIN_TIMESTAMP = "uncertain_timestamp"
    EXCLUDED = "excluded"


class SourceManifestItem(StrictModel):
    source_id: str
    source: str
    retrieval_timestamp: str
    hash: str

    @field_validator("retrieval_timestamp", mode="before")
    @classmethod
    def normalize_retrieval_timestamp(cls, value: object) -> object:
        if isinstance(value, datetime):
            return value.isoformat().replace("+00:00", "Z")
        return value


class ParticipantPacketFrontmatter(StrictModel):
    case_id: str
    decision_question: str
    decision_date_or_cutoff: str
    role_frame: str
    authority_constraints: str
    capability_constraints: str
    permitted_assumptions: list[str]
    forbidden_information_notice: str
    source_manifest: list[SourceManifestItem]

    @field_validator("decision_date_or_cutoff", mode="before")
    @classmethod
    def normalize_cutoff(cls, value: object) -> object:
        if isinstance(value, (date, datetime)):
            return value.isoformat()
        return value


class EvidenceUnit(StrictModel):
    evidence_id: str
    source_id: str
    source: str
    source_type: str
    timestamp: str
    retrieval_timestamp: str
    hash: str
    hash_basis: str
    pre_decision_status: PreDecisionStatus
    pre_decision_basis: str
    summary: str

    @field_validator("timestamp", "retrieval_timestamp", mode="before")
    @classmethod
    def normalize_temporal_fields(cls, value: object) -> object:
        if isinstance(value, datetime):
            return value.isoformat().replace("+00:00", "Z")
        if isinstance(value, date):
            return value.isoformat()
        return value


class BandInputs(StrictModel):
    evidence_strength: Literal["none", "weak", "moderate", "strong"]
    evidence_independence: Literal["correlated", "partially_independent", "independent"]
    reversibility_feasibility: Literal["low", "medium", "high"]
    reversibility_cost: Literal["low", "medium", "high", "ruinous"]
    authority: Literal["absent", "partial", "full"]
    authority_acquisition_cost: Literal["low", "medium", "high", "impossible"]
    capability: Literal["absent", "partial", "full"]
    capability_build_cost: Literal["low", "medium", "high", "impossible"]
    loss_shape: Literal["symmetric", "asymmetric_down", "ruinous_tail", "unknown"]
    opportunity_cost: Literal["none", "low", "moderate", "severe"]
    information_decay: Literal["none", "slow", "fast", "expiring"]
    option_value: Literal["none", "low", "moderate", "high"]
    upside_shape: Literal["none", "symmetric", "asymmetric_up", "convex", "once_only_window"]
    urgency: Literal["none", "low", "medium", "critical"]


class SecondLabelDiff(StrictModel):
    input_name: str
    primary_label: str
    second_label: str
    final_label: str
    resolution_reason: str


class LedgerAuthors(StrictModel):
    primary_labeler: str
    second_labeler: str
    second_labeler_type: Literal["human_operator", "separate_model_family_advisory"]


class MustAddressItem(StrictModel):
    must_address_item_id: str
    description: str
    evidence_unit_ids: list[str] = Field(default_factory=list)


class UnderreachObservability(StrictModel):
    present: bool
    basis: Literal[
        "opportunity_cost",
        "window_closure",
        "information_decay",
        "option_value_loss",
        "other",
    ] | None = None
    notes: str | None = None
    evidence_unit_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_basis(self) -> "UnderreachObservability":
        if self.present and self.basis is None:
            raise ValueError("basis is required when underreach observability is present")
        if not self.present and self.basis is not None:
            raise ValueError("basis must be omitted when underreach observability is not present")
        return self


class LeakageAudit(StrictModel):
    memorization_probe_required: bool
    known_fame_risk: str
    spoiler_inventory: str


class FacilitatorLedger(StrictModel):
    case_id: str
    batch_id: str
    case_family: str
    decision_shape: str
    labeling_rubric_version: str
    mapping_table_version_pin: str
    ledger_authors: LedgerAuthors
    second_label_diffs: list[SecondLabelDiff] = Field(default_factory=list)
    frozen_band_inputs: BandInputs
    must_address_items: list[MustAddressItem] = Field(default_factory=list)
    underreach_observability: UnderreachObservability
    leakage_audit: LeakageAudit
    fixture_status: Literal["QUARANTINED", "ADMITTED"]
    fixture_grade: Literal["plumbing_grade", "judgment_quality_candidate"]
    committed_at: str
    ledger_freeze_hash: str

    @field_validator("committed_at", mode="before")
    @classmethod
    def normalize_committed_at(cls, value: object) -> object:
        if isinstance(value, datetime):
            return value.isoformat().replace("+00:00", "Z")
        return value
