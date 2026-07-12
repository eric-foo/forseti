"""Strict evidence rows for TikTok transcript audience triangulation."""
from __future__ import annotations

from enum import StrEnum
from pydantic import Field, field_validator
from schemas.case_models import StrictModel


class AudienceLayer(StrEnum):
    ADDRESSED = "addressed_audience"
    BENEFICIARY = "beneficiary_content_fit"


class AudienceDimension(StrEnum):
    CATEGORY_RELATIONSHIP = "category_relationship"
    ASSUMED_KNOWLEDGE = "assumed_knowledge"
    VALUE_SOUGHT = "value_sought"
    PRICE_VALUE_POSTURE = "price_value_posture"
    CONTENT_MECHANISM = "preferred_content_mechanism"
    EXCLUSION = "exclusion"


class TikTokAudienceEvidence(StrictModel):
    evidence_id: str
    creator_id: str
    video_id: str
    audience_layer: AudienceLayer
    dimension: AudienceDimension
    label: str
    content_pillar: str
    vote: float = Field(ge=-1.0, le=1.0)
    source_pointer: str
    possible_negation_or_irony: bool = False

    @field_validator("evidence_id", "creator_id", "video_id", "label", "content_pillar", "source_pointer")
    @classmethod
    def non_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("field must be non-blank")
        return value.strip()


class TikTokAudienceProfile(StrictModel):
    creator_id: str
    primary_hypothesis: str
    knowledge_level: str
    shopping_stage: str
    product_range: list[str]
    recurring_decision_jobs: list[str]
    engagement_style: str
    price_posture: str
    likely_exclusions: list[str]
    evidence_ids: list[str]
    counterevidence_ids: list[str] = []
    support_band: str
    actual_audience: str = "not_estimated"

    @field_validator("creator_id", "primary_hypothesis", "knowledge_level", "shopping_stage", "engagement_style", "price_posture")
    @classmethod
    def profile_non_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("profile field must be non-blank")
        return value.strip()

    @field_validator("support_band")
    @classmethod
    def support_band_closed(cls, value: str) -> str:
        if value not in {"high", "medium", "low", "abstain"}:
            raise ValueError("support_band must be high|medium|low|abstain")
        return value

    @field_validator("actual_audience")
    @classmethod
    def actual_unknown(cls, value: str) -> str:
        if value != "not_estimated":
            raise ValueError("actual_audience must remain not_estimated")
        return value


__all__ = ["AudienceDimension", "AudienceLayer", "TikTokAudienceEvidence", "TikTokAudienceProfile"]
