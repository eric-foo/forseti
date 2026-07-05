"""Schemas for YouTube transcript -> product mention extraction (Pass 1, silver).

Data shapes for Pass 1 (LLM extraction -> ProductMention, the `cleaning/` LLM lane)
and the DEFERRED Pass 2 (deterministic verdict fusion, `scoring/`). Mirrors the
audience-inference EvidenceRecord discipline: closed enums, a source_pointer that is
required here and (in the extractor) verified as a real transcript substring (CE9);
the LLM emits signed evidence + a creator-stated rating but NEVER its own verdict
(CE4/CE10). A ProductMention carries no verdict field by construction.

Spec: forseti/product/spines/capture/core/source_families/social_media/youtube/
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


# --- Pass-2 shapes (gold verdict). Consumed by the deterministic, LLM-free fusion in
# scoring/product_fusion.py (fuse_product_verdicts). ---


class Verdict(StrEnum):
    POSITIVE = "positive"
    MIXED = "mixed"
    NEGATIVE = "negative"
    UNKNOWN = "unknown"


class ProductVerdict(ProductMentionModel):
    """Per-product verdict for one creator across their videos (Pass 2) — deterministic,
    evidence-cited. Produced by ``scoring/product_fusion.py`` from the creator's
    ``ProductMention``s. Carries NO engagement/resonance signal: engagement interpretation
    is the Judgment-owned Engagement Logic Registry's domain
    (``forseti/product/shared/engagement_registry/engagement_logic_registry_v0.md``), never this
    fusion. The verdict answers only "what the creator said about this product."
    """

    brand: str
    line: str
    verdict: Verdict
    mention_count: int = Field(ge=0)
    # Supporting (positive-contribution) vs opposing (negative-contribution) mention_ids,
    # kept separate so a ``mixed`` verdict is auditable from evidence on both sides.
    evidence_ids: list[str] = Field(default_factory=list)
    counterevidence_ids: list[str] = Field(default_factory=list)
    # Squashed positive-direction support strength in [0, 1] (uncalibrated; calibration deferred).
    uncalibrated_support_score: float = Field(ge=0.0, le=1.0, default=0.0)
    # Squashed opposition strength in [0, 1] — carried so Judgment sees a negative/mixed verdict's
    # MAGNITUDE and the support-vs-oppose asymmetry, not just polarity (uncalibrated). A pure
    # negative reports support 0.0 / oppose high; mixed reports both high.
    uncalibrated_oppose_score: float = Field(ge=0.0, le=1.0, default=0.0)

    @model_validator(mode="after")
    def _decided_needs_evidence(self) -> ProductVerdict:
        # Per-verdict-type evidence invariant: positive cites supporting evidence, negative
        # cites counterevidence, mixed cites both. (unknown cites nothing.) This rejects
        # side-unsound verdicts (e.g. positive with only counterevidence), not just "no
        # evidence at all".
        if self.verdict in (Verdict.POSITIVE, Verdict.MIXED) and not self.evidence_ids:
            raise ValueError(f"a {self.verdict.value} verdict must cite supporting evidence_ids")
        if self.verdict in (Verdict.NEGATIVE, Verdict.MIXED) and not self.counterevidence_ids:
            raise ValueError(f"a {self.verdict.value} verdict must cite counterevidence_ids")
        return self


class ProductVerdictSet(ProductMentionModel):
    """All Pass-2 product verdicts for ONE creator — the container ``fuse_product_verdicts``
    returns. Mirrors ``IdealAudienceProfile``: carries the creator id, the per-product
    verdicts, the products that abstained to ``unknown``, the fusion config version, a
    timestamp, and provenance, so a run is re-derivable and auditable. ``creator_id`` is
    supplied by the caller (``ProductMention`` carries none) and scopes input to one creator.
    """

    creator_id: str
    verdicts: list[ProductVerdict] = Field(default_factory=list)
    abstentions: list[str] = Field(default_factory=list)
    fusion_config_version: str
    generated_at: str
    provenance: dict = Field(default_factory=dict)

    @field_validator("creator_id", "fusion_config_version", "generated_at")
    @classmethod
    def _required_non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("field must be non-empty")
        return value
