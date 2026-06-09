"""LinkedIn Lane Graph Frontier Register (slice 2).

Dataclass + module-level validators, mirroring the capture_spine
reddit_graph_frontier support and REUSING the slice-1 linkedin_lane error +
forbidden-output-field walk (imported, not duplicated). Slice 2 = FrontierNode +
FrontierEdge + FrontierDecision + NextRunEnvelope + their validators. The
register builder and PromotionReceipt are later slices. No live runner, no
promotion/capture execution, no persistence beyond a local planning artifact.
"""
from __future__ import annotations

from capture_spine.linkedin_graph_frontier.models import (
    DEFAULT_LINKEDIN_GRAPH_FRONTIER_NON_CLAIMS,
    LINKEDIN_GRAPH_FRONTIER_NEXT_RUN_ENVELOPE_SCHEMA_VERSION,
    LINKEDIN_GRAPH_FRONTIER_REGISTER_SCHEMA_VERSION,
    PERSON_CANDIDATE_NODE_TYPES,
    FrontierDecision,
    FrontierEdge,
    FrontierEdgeType,
    FrontierNode,
    FrontierNodeType,
    LinkedInLaneError,
    NextRunEnvelope,
    ProjectionDecision,
)
from capture_spine.linkedin_graph_frontier.validation import (
    validate_graph_frontier_register,
    validate_next_run_envelope,
)

__all__ = [
    "DEFAULT_LINKEDIN_GRAPH_FRONTIER_NON_CLAIMS",
    "LINKEDIN_GRAPH_FRONTIER_NEXT_RUN_ENVELOPE_SCHEMA_VERSION",
    "LINKEDIN_GRAPH_FRONTIER_REGISTER_SCHEMA_VERSION",
    "PERSON_CANDIDATE_NODE_TYPES",
    "FrontierDecision",
    "FrontierEdge",
    "FrontierEdgeType",
    "FrontierNode",
    "FrontierNodeType",
    "LinkedInLaneError",
    "NextRunEnvelope",
    "ProjectionDecision",
    "validate_graph_frontier_register",
    "validate_next_run_envelope",
]
