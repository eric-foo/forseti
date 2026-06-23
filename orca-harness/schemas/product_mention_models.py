"""Schemas for YouTube transcript -> product mention extraction (Pass 1, silver).

Data shapes for Pass 1 (LLM extraction -> ProductMention, the `cleaning/` LLM lane)
and the DEFERRED Pass 2 (deterministic verdict fusion, `scoring/`). Mirrors the
audience-inference EvidenceRecord discipline: closed enums, a source_pointer that is
required here and (in the extractor) verified as a real transcript substring (CE9);
the LLM emits signed evidence + a creator-stated rating but NEVER its own verdict
(CE4/CE10). A ProductMention carries no verdict field by construction.

Spec: orca/product/spines/capture/core/source_families/social_media/youtube/
youtube_transcript_product_extraction_spec_v0.md (CE1-CE10 / D1-D8).
"""

from __future__ import annotations

import math
from enum import StrEnum
from typing import Any, Mapping, Self

from pydantic import ConfigDict, Field, field_validator, model_validator

from schemas.case_models import StrictModel


class Concentration(StrEnum):
    """Closed concentration enum (CE3). `unknown` is valid (often unstated in speech)."""

    EDT = "edt"
    EDP = "edp"
    PARFUM = "parfum"
    ELIXIR = "elixir"
    COLOGNE = "cologne"
    UNKNOWN = "unknown"


class TranscriptSource(StrEnum):
    ASR = "asr"
    CAPTION = "caption"


class ProductMentionModel(StrictModel):
    """Strict base for audit-critical product-mention records (mirrors the audience base):
    forbid extras, validate on assignment, and route unsafe construction back through
    validation so CE invariants cannot be skipped."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True, validate_assignment=True)

    @classmethod
    def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:
        return cls.model_validate(values)

    def model_copy(self, *, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self:
        data = self.model_dump(mode="python")
        if update:
            data.update(update)
        return type(self).model_validate(data)


class StatedRating(ProductMentionModel):
    """A score the CREATOR explicitly stated, with its own verbatim quote.

    This is EVIDENCE (a witnessed fact), never the LLM's own judgment (CE10). The
    extractor admits it only when its `source_pointer` is a real transcript substring.
    """

    value: float
    scale_max: float = Field(gt=0)
    source_pointer: str

    @field_validator("source_pointer")
    @classmethod
    def _quote_required(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("CE10: stated_rating requires a non-empty source_pointer")
        return value

    @model_validator(mode="after")
    def _value_in_range(self) -> StatedRating:
        # NaN/Inf slip past <,> comparisons (unlike pydantic ge/le); reject them so a hostile
        # model cannot persist a non-finite, non-RFC-JSON rating (CE3/CE8).
        if not (math.isfinite(self.value) and math.isfinite(self.scale_max)):
            raise ValueError("stated_rating value/scale_max must be finite")
        if self.value < 0 or self.value > self.scale_max:
            raise ValueError("stated_rating.value must be within [0, scale_max]")
        return self


class ProductMention(ProductMentionModel):
    """One product mention extracted from a transcript cue-span (Pass 1, silver).

    Signed evidence + a code-verified quote + a cue timestamp. Identity comes from the
    INPUT (CE1); the LLM never supplies it. `start_ms`/`end_ms` are assigned by code from
    the cue that contains the located quote (CE5), never by the model. There is NO verdict
    field (CE4): the verdict is the deterministic Pass-2 job.
    """

    mention_id: str
    video_id: str
    transcript_anchor: str
    transcript_source: TranscriptSource
    brand: str  # "unknown" allowed (frequently unstated in speech)
    line: str
    concentration: Concentration
    # Signed evidence in [-1, 1]: support (+) / opposition (-). NOT a verdict.
    stance_vote: float = Field(ge=-1.0, le=1.0)
    stated_rating: StatedRating | None = None
    # CE2: a non-empty quote is required; the extractor additionally verifies it is a
    # real transcript substring (CE9).
    source_pointer: str
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=0)
    creator_authored: bool = False
    possible_negation_or_irony: bool = False
    extractor_confidence: float = Field(ge=0.0, le=1.0)
    provenance: dict = Field(default_factory=dict)

    @field_validator("source_pointer")
    @classmethod
    def _ce2_source_pointer_required(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("CE2: product mention requires a non-empty source_pointer")
        return value

    @field_validator("mention_id", "video_id", "transcript_anchor", "line")
    @classmethod
    def _required_non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("field must be non-empty")
        return value

    @field_validator("brand")
    @classmethod
    def _brand_non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("brand must be non-empty (use 'unknown' if unstated)")
        return value

    @model_validator(mode="after")
    def _end_after_start(self) -> ProductMention:
        if self.end_ms < self.start_ms:
            raise ValueError("end_ms must be >= start_ms")
        return self


# --- Deferred Pass-2 shapes (gold verdict). Declared for the schema's completeness;
# the fusion that produces them lives in scoring/ and is NOT built in v0. ---


class Verdict(StrEnum):
    POSITIVE = "positive"
    MIXED = "mixed"
    NEGATIVE = "negative"
    UNKNOWN = "unknown"


class ProductVerdict(ProductMentionModel):
    """Per-product verdict for one video (Pass 2, DEFERRED) — deterministic, evidence-cited."""

    brand: str
    line: str
    verdict: Verdict
    mention_count: int = Field(ge=0)
    evidence_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _decided_needs_evidence(self) -> ProductVerdict:
        if self.verdict != Verdict.UNKNOWN and not self.evidence_ids:
            raise ValueError("a decided verdict must cite evidence_ids")
        return self
