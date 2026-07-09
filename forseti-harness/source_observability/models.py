from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import Field

from schemas.case_models import StrictModel


class ObservablePosture(StrEnum):
    PRESERVED = "preserved"
    PARAPHRASED = "paraphrased"
    POINTER_ONLY = "pointer_only"
    INACCESSIBLE = "inaccessible"
    FAILED = "failed"
    NOT_ATTEMPTED = "not_attempted"
    NOT_APPLICABLE = "not_applicable"


class SourceObservabilityRecord(StrictModel):
    record_id: str
    source_ref: str
    source_family: str
    source_language_posture: ObservablePosture
    source_structure_posture: ObservablePosture
    archive_body_posture: ObservablePosture
    media_posture: ObservablePosture
    access_posture: ObservablePosture
    locator_visible: bool
    cutoff_visible: bool
    source_language_anchor_count: int = Field(ge=0)
    source_language_anchor_required: bool = False
    source_structure_required: bool = False
    media_required: bool = False
    archive_body_expected: bool = False
    limitation_notes: list[str] = Field(default_factory=list)


class SourceObservabilityLimitation(StrictModel):
    record_id: str
    source_ref: str
    limitation_type: Literal[
        "source_language_anchor_missing",
        "source_structure_not_preserved",
        "media_not_preserved",
        "archive_body_not_retrieved",
        "access_failure_visible",
        "access_failure_context_missing",
        "unnoted_non_preserved_posture",
    ]
    posture: ObservablePosture | None = None
    detail: str


class SourceObservabilityCheckResult(StrictModel):
    record_count: int
    limitations: list[SourceObservabilityLimitation] = Field(default_factory=list)

    @property
    def has_visible_limitations(self) -> bool:
        return bool(self.limitations)
