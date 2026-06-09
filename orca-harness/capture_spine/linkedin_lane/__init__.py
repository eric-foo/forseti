"""LinkedIn Lane no-live discovery harness (slice 1).

Dataclass + module-level validators, mirroring the capture_spine Reddit lane
support. Slice 1 = RunEnvelope + CandidateRow + their validators; the Graph
Frontier register and PromotionReceipt are slice 2. No live runner, no
supervised-browser-assist execution, no promotion/capture execution.
"""
from __future__ import annotations

from capture_spine.linkedin_lane.models import (
    DEFAULT_LINKEDIN_LANE_NON_CLAIMS,
    LINKEDIN_LANE_CANDIDATE_ROW_SCHEMA_VERSION,
    LINKEDIN_LANE_RUN_ENVELOPE_SCHEMA_VERSION,
    CandidateClass,
    CandidateRow,
    EntityType,
    LinkedInLaneError,
    MethodMode,
    MinimizationRule,
    PersonDataMinimized,
    PrivacySensitivity,
    RunEnvelope,
    SourceSurface,
    StopReason,
    VisibleInfluenceNumbers,
)
from capture_spine.linkedin_lane.validation import (
    FORBIDDEN_OUTPUT_FIELDS,
    assert_no_forbidden_output_fields,
    validate_candidate_row,
    validate_run_envelope,
)

__all__ = [
    "DEFAULT_LINKEDIN_LANE_NON_CLAIMS",
    "LINKEDIN_LANE_CANDIDATE_ROW_SCHEMA_VERSION",
    "LINKEDIN_LANE_RUN_ENVELOPE_SCHEMA_VERSION",
    "CandidateClass",
    "CandidateRow",
    "EntityType",
    "LinkedInLaneError",
    "MethodMode",
    "MinimizationRule",
    "PersonDataMinimized",
    "PrivacySensitivity",
    "RunEnvelope",
    "SourceSurface",
    "StopReason",
    "VisibleInfluenceNumbers",
    "FORBIDDEN_OUTPUT_FIELDS",
    "assert_no_forbidden_output_fields",
    "validate_candidate_row",
    "validate_run_envelope",
]
