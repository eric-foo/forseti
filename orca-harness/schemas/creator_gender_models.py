"""Schemas for the IG creator-gender demographic signal (Pass 1 silver + Pass 2 fusion output).

A SOFT, confidence-weighted creator-gender LEAN — never a hard categorical label. Sibling to
product/audience inference (do NOT fold into product-stance). The agent-in-the-loop inference
that POPULATES `CreatorGenderSignal` (cleaning/ zone) and the gender x product-stance join are
DEFERRED; this file is the deterministic contract the no-LLM fusion (`scoring/creator_gender_fusion.py`)
consumes.

Minimization posture (owner-decided): store ONLY a signed soft lean + confidence + the cue + a
short verbatim basis + typed inferred provenance. There is deliberately NO categorical gender
field, and provenance is a TYPED model (not an open dict) so a hard label or commenter gender
cannot hide inside it — a hard label is genuinely UNREPRESENTABLE. No commenter gender. Binary
male-vs-female axis; non-binary creators are an accepted residual handled by abstention (lean ~0 /
low confidence), never a forced label.

Scope/intent: docs/decisions/ig_creator_gender_demographic_signal_lane_scope_defer_v0.md.
"""

from __future__ import annotations

import math
from enum import StrEnum
from typing import Any, Literal, Mapping, Self

from pydantic import ConfigDict, Field, field_validator, model_validator

from schemas.case_models import StrictModel


class GenderCueKind(StrEnum):
    """How a per-reel gender lean was cued, so the fusion can weight cues by trust.

    `self_presentation` is the trusted, circularity-free spine (explicit first-person/self-
    reference). `product_marketed_gender` is RETAINED as an auditable cue kind but EXCLUDED from
    decisive fusion in this slice: inferring gender from the products a creator reviews, then
    cutting product-stance by gender, is circular (and cross-gender reviewing is common). A
    non-circular, owner-approved use would re-enable it.
    """

    SELF_PRESENTATION = "self_presentation"
    PRODUCT_MARKETED_GENDER = "product_marketed_gender"


class CreatorGenderModel(StrictModel):
    """Strict base (mirrors ProductMentionModel): forbid extras, validate on assignment, and route
    unsafe construction back through validation so the soft-lean invariants cannot be skipped."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True, validate_assignment=True)

    @classmethod
    def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:
        return cls.model_validate(values)

    def model_copy(self, *, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self:
        data = self.model_dump(mode="python")
        if update:
            data.update(update)
        return type(self).model_validate(data)


# A short cue is enough to audit a self-presentation read; bound it so the verbatim `basis` cannot
# smuggle a transcript or extra free-text payload past the minimization posture.
CREATOR_GENDER_BASIS_MAX_CHARS = 160

# Output contract for a decisive fused lean. Sub-floor signals may still be kept as abstained
# audit evidence, but they must not become decisive output records.
CREATOR_GENDER_DECISIVE_CONFIDENCE_FLOOR = 0.40


class CreatorGenderSignalProvenance(CreatorGenderModel):
    """Typed, minimal provenance for a per-reel signal.

    Closes the untyped-`dict` back door: with `extra="forbid"`, a categorical gender or
    commenter-gender key cannot hide inside provenance (e.g. `{"gender": "male"}` is rejected).
    """

    inference_origin: Literal["agent_in_the_loop"] = "agent_in_the_loop"
    source_zone: Literal["cleaning"] = "cleaning"


class CreatorGenderLeanProvenance(CreatorGenderModel):
    """Typed, minimal provenance for the fused creator-level lean."""

    fusion_config_version: str

    @field_validator("fusion_config_version")
    @classmethod
    def _required_non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("field must be non-empty")
        return value


class CreatorGenderSignal(CreatorGenderModel):
    """One per-reel creator-gender lean cue (Pass 1, silver).

    What the DEFERRED agent-in-the-loop cleaning inference will produce per reel. `gender_lean` is
    a signed SOFT lean in [-1, 1] (convention: negative = female-leaning, positive = male-leaning,
    ~0 = neutral / insufficient). There is NO categorical gender field and provenance is typed, so
    a hard label is unrepresentable. `basis` is a short, length-bounded verbatim cue, kept for
    auditability; provenance marks the read inferred.
    """

    creator_id: str
    signal_id: str
    reel_ref: str
    gender_lean: float = Field(ge=-1.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    cue_kind: GenderCueKind
    basis: str = Field(max_length=CREATOR_GENDER_BASIS_MAX_CHARS)
    provenance: CreatorGenderSignalProvenance = Field(default_factory=CreatorGenderSignalProvenance)

    @field_validator("creator_id", "signal_id", "reel_ref", "basis")
    @classmethod
    def _required_non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("field must be non-empty")
        return value

    @model_validator(mode="after")
    def _finite(self) -> Self:
        # NaN/Inf slip past pydantic ge/le (comparison-based); reject them so a non-finite lean or
        # confidence cannot persist (mirrors StatedRating / ProductMention finite discipline).
        if not (math.isfinite(self.gender_lean) and math.isfinite(self.confidence)):
            raise ValueError("gender_lean and confidence must be finite")
        return self


class CreatorGenderLean(CreatorGenderModel):
    """The fused creator-level gender lean (Pass 2 output) — deterministic, evidence-cited, SOFT.

    `gender_lean` is the signed soft lean in [-1, 1]; `confidence` is the squashed signal strength
    in [0, 1]. `abstained` True means the net signal was too weak/contested to call: `gender_lean`
    is reported 0.0 while `confidence` retains the sub-floor strength for audit. NO categorical
    label. UNCALIBRATED v0 (see `scoring/creator_gender_fusion.py`).

    ACCEPTED RESIDUAL: `abstained` conflates several distinct cases — no signal, weak signal,
    contested/net-zero signal, and outside-the-binary-axis (non-binary). That may be the right
    minimization tradeoff for now, but it is an accepted residual, not a solved one; a future
    `abstain_reason` could disambiguate.
    """

    creator_id: str
    gender_lean: float = Field(ge=-1.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    abstained: bool
    evidence_ids: list[str] = Field(default_factory=list)
    fusion_config_version: str
    generated_at: str
    provenance: CreatorGenderLeanProvenance

    @field_validator("creator_id", "fusion_config_version", "generated_at")
    @classmethod
    def _required_non_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("field must be non-empty")
        return value

    @field_validator("evidence_ids")
    @classmethod
    def _evidence_ids_non_empty(cls, value: list[str]) -> list[str]:
        if any(not item or not item.strip() for item in value):
            raise ValueError("evidence_ids must contain only non-empty IDs")
        return value

    @model_validator(mode="after")
    def _coherent_output_state(self) -> Self:
        if not (math.isfinite(self.gender_lean) and math.isfinite(self.confidence)):
            raise ValueError("gender_lean and confidence must be finite")
        if self.abstained:
            if self.gender_lean != 0.0:
                raise ValueError("abstained output must report gender_lean as 0.0")
            return self
        if self.gender_lean == 0.0:
            raise ValueError("non-abstained output must carry a non-zero gender_lean")
        if self.confidence < CREATOR_GENDER_DECISIVE_CONFIDENCE_FLOOR:
            raise ValueError("non-abstained output must meet the decisive confidence floor")
        if not self.evidence_ids:
            raise ValueError("non-abstained output must carry evidence_ids")
        return self
