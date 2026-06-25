"""Schemas for IG creator ideal-audience inference (Tier-1 v0).

Data shapes shared by Pass 1 (LLM extraction -> EvidenceRecord, built later as
Slice B in the `cleaning/` LLM lane) and Pass 2 (deterministic fusion ->
IdealAudienceProfile, `scoring/audience_fusion.py`).

Tier-1 ONLY: segment / audience_role / purchase_intent / skill_level / price_tier.
The Tier-2-A demographic slice (gender_skew / age_band) is gated (owner council +
ledger-schema home) and is deliberately NOT representable here in v0; extend
``OutputField`` when that slice is activated.

Spec: orca/product/spines/capture/core/source_families/social_media/instagram/
ig_creator_ideal_audience_inference_spec_v0.md (CE1-CE12 / D1-D7).
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal, Mapping, Self

from pydantic import ConfigDict, Field, field_validator, model_validator

from schemas.case_models import StrictModel

# Canonical Tier-1 output fields (mirrors OutputField; gender/age excluded in v0).
TIER1_FIELDS: tuple[str, ...] = (
    "segment",
    "audience_role",
    "purchase_intent",
    "skill_level",
    "price_tier",
)


class ModalityFamily(StrEnum):
    """Signal family of an evidence item. No `visual` in v0 (VLM deferred)."""

    TEXT = "text"
    COMMERCIAL = "commercial"
    STRUCTURAL = "structural"
    COMMENT = "comment"


class OutputField(StrEnum):
    """Tier-1 output fields only. Gender/age (Tier-2-A) are gated and omitted in v0."""

    SEGMENT = "segment"
    AUDIENCE_ROLE = "audience_role"
    PURCHASE_INTENT = "purchase_intent"
    SKILL_LEVEL = "skill_level"
    PRICE_TIER = "price_tier"


class SupportBand(StrEnum):
    """Coarse evidence-strength band. Not calibrated confidence (CE7)."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    ABSTAIN = "abstain"


UNKNOWN_LABEL = "unknown"


class AudienceInferenceModel(StrictModel):
    """Strict model variant for audit-critical audience inference records."""

    model_config = ConfigDict(
        extra="forbid", populate_by_name=True, validate_assignment=True
    )

    @classmethod
    def model_construct(
        cls, _fields_set: set[str] | None = None, **values: Any
    ) -> Self:
        # These schemas encode CE invariants; unsafe construction must not skip them.
        return cls.model_validate(values)

    def model_copy(
        self, *, update: Mapping[str, Any] | None = None, deep: bool = False
    ) -> Self:
        data = self.model_dump(mode="python")
        if update:
            data.update(update)
        return type(self).model_validate(data)


class EvidenceRecord(AudienceInferenceModel):
    """One extracted, source-pointed observation that votes on one Tier-1 field.

    Produced by Pass 1 (LLM, D1-D9). Pass 2 consumes these; it never sees raw content.
    """

    evidence_id: str
    creator_id: str
    platform: str
    post_id: str
    pillar_label: str | None = None
    signal_id: str
    modality: ModalityFamily
    target_field: OutputField
    label: str
    # Directional vote in [-1, 1]: support (+) or opposition (-) for `label`.
    vote: float = Field(ge=-1.0, le=1.0)
    # Base reliability from the W1-W5 weight scale, normalized to [0, 1].
    base_reliability: float = Field(ge=0.0, le=1.0)
    extractor_confidence: float = Field(ge=0.0, le=1.0)
    creator_authored: bool = False
    possible_negation_or_irony: bool = False
    # Items sharing a creative_cluster_id are dependence-discounted (one creative
    # repeated should not count as independent evidence).
    creative_cluster_id: str | None = None
    # CE9: every evidence item must cite where it came from.
    source_pointer: str

    @field_validator("source_pointer")
    @classmethod
    def _ce9_source_pointer_required(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("CE9: evidence record requires a non-empty source_pointer")
        return value

    @field_validator("evidence_id")
    @classmethod
    def _evidence_id_required(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("evidence_id must be non-empty")
        return value

    @field_validator("label")
    @classmethod
    def _label_not_unknown(cls, value: str) -> str:
        if value == UNKNOWN_LABEL or not value.strip():
            raise ValueError("evidence label must be a concrete, non-'unknown' label")
        return value


class FieldResult(AudienceInferenceModel):
    """Fused result for one output field within one pillar."""

    field: OutputField
    label: str  # a concrete label, or UNKNOWN_LABEL when abstaining
    support_band: SupportBand
    # CE7: evidence strength, NOT calibrated accuracy.
    uncalibrated_support_score: float = Field(ge=0.0, le=1.0)
    evidence_ids: list[str] = Field(default_factory=list)
    counterevidence_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _ce12_evidence_for_known_label(self) -> FieldResult:
        decided = self.label != UNKNOWN_LABEL and self.support_band != SupportBand.ABSTAIN
        if decided and not self.evidence_ids:
            raise ValueError("CE12: a decided (non-unknown) field result must carry evidence_ids")
        return self

    @field_validator("evidence_ids", "counterevidence_ids")
    @classmethod
    def _evidence_ids_non_empty(cls, value: list[str]) -> list[str]:
        if any(not item or not item.strip() for item in value):
            raise ValueError("evidence id lists must contain only non-empty IDs")
        return value


class PillarProfile(AudienceInferenceModel):
    """Per-content-pillar profile. Pillars are NOT merged when divergent (CE8)."""

    pillar_id: str
    pillar_label: str
    positioning_share: float = Field(ge=0.0, le=1.0)
    field_results: list[FieldResult]


class IdealAudienceProfile(AudienceInferenceModel):
    """The Pass-2 output: who the creator's content is best-fit for (ideal, not actual)."""

    creator_id: str
    # CE10: the schema forbids any actual-audience claim.
    actual_audience: Literal["not_estimated"] = "not_estimated"
    ideal_audience_profiles: list[PillarProfile] = Field(default_factory=list)
    abstentions: list[str] = Field(default_factory=list)
    fusion_config_version: str
    generated_at: str
    provenance: dict = Field(default_factory=dict)
