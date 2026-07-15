"""Strict contracts for creator-audience Judgment and registry projection."""
from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from schemas.case_models import StrictModel


AudienceClaimAxis = Literal[
    "category_knowledge",
    "purchase_decision_stage",
    "price_value_posture",
    "product_brand_affinity",
    "language_community_norms",
    "objections",
    "aspirations_identity",
    "presentation_style_resonance",
    "engagement_memorability_effect",
]


class AudienceTriangulationClaim(StrictModel):
    claim_id: str
    axis: AudienceClaimAxis
    statement: str
    commercial_implication: str
    modality: Literal[
        "creator_content", "observed_comments", "engagement_elevated", "fused"
    ]
    relation: Literal[
        "agreement", "contradiction", "audience_emergent", "creator_only", "missing"
    ]
    support_scope: Literal[
        "single_comment", "single_video", "multi_video", "content_only", "mixed_multi_video"
    ]
    representative_evidence_ids: list[str] = Field(min_length=1, max_length=5)
    all_support_evidence_ids: list[str] = Field(min_length=1)
    counterevidence_ids: list[str] = []
    source_video_ids: list[str] = Field(min_length=1)
    limitation: str | None = None

    @field_validator("claim_id", "statement", "commercial_implication")
    @classmethod
    def non_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("claim text must be non-blank")
        return value.strip()


class AudienceProjectionPoint(StrictModel):
    statement: str
    claim_ids: list[str] = Field(min_length=1)

    @field_validator("statement")
    @classmethod
    def non_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("projection statement must be non-blank")
        return value.strip()


class AudienceJudgmentClaimSet(StrictModel):
    claims: list[AudienceTriangulationClaim] = Field(min_length=1)
    agreements: list[str]
    contradictions: list[str]
    missing_evidence: list[str]


class CreatorSignalProjection(StrictModel):
    hire_verdict: AudienceProjectionPoint
    product_advantage: AudienceProjectionPoint
    creator_specific_execution: AudienceProjectionPoint
    observed_audience_response: AudienceProjectionPoint
    strongest_campaign_jobs: list[AudienceProjectionPoint] = Field(min_length=1)
    briefing_instructions: list[AudienceProjectionPoint] = Field(min_length=1)
    wrong_hire_boundary: AudienceProjectionPoint
    robustness_stamp: str | None = None


class CreatorAudienceTriangulationSnapshot(StrictModel):
    schema_version: Literal["creator_audience_triangulation_snapshot_v0"]
    snapshot_id: str
    profile_subject_kind: Literal["platform_account"]
    profile_subject_id: str
    platform_account_id: str
    creator_id: str
    platform_scope: Literal["tiktok"]
    generated_at: str
    evidence_cutoff: str
    input_bundle_id: str
    input_bundle_hash: str
    judgment_claim_set: AudienceJudgmentClaimSet
    creator_signal_projection: CreatorSignalProjection
    limitations: list[str]
    non_claims: list[str]
    actual_audience_demographics: Literal["not_estimated"] = "not_estimated"

    @field_validator(
        "snapshot_id",
        "profile_subject_id",
        "platform_account_id",
        "creator_id",
        "generated_at",
        "evidence_cutoff",
        "input_bundle_id",
        "input_bundle_hash",
    )
    @classmethod
    def snapshot_text_non_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("snapshot field must be non-blank")
        return value.strip()


__all__ = [
    "AudienceJudgmentClaimSet",
    "AudienceProjectionPoint",
    "AudienceTriangulationClaim",
    "CreatorAudienceTriangulationSnapshot",
    "CreatorSignalProjection",
]
