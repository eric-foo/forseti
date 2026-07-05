"""LinkedIn Lane Graph Frontier Register -- slice 2 data models.

Mirrors the capture_spine reddit_graph_frontier pattern (frozen dataclass +
StrEnum + module-level validate_* in validation.py), adapted to the LinkedIn
lane's frontier vocabulary and person-privacy posture. It REUSES
``LinkedInLaneError`` and (in validation.py) the slice-1 forbidden-output-field
walk -- imported, NOT duplicated -- mirroring how reddit_graph_frontier reuses
reddit_candidate_intake. The forbidden set is identical across the LinkedIn lane,
so a same-family import (not a Reddit import, not a duplicate) is correct.

Slice 2 scope: FrontierNode + FrontierEdge + FrontierDecision + NextRunEnvelope
+ their validators. The register BUILDER and PromotionReceipt are deferred to
later slices. Frontier decisions live in a separate ``frontier_decisions[]``
structure and a stop is a field/event -- they are NOT FrontierNode instances (no
source shape), mirroring the reddit pattern and the owner-locked "separate
structures, not nodes" decision. No live runner, no promotion/capture execution,
no persistence beyond a local planning artifact.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

from capture_spine.linkedin_lane.models import LinkedInLaneError

__all__ = [
    "LinkedInLaneError",
    "LINKEDIN_GRAPH_FRONTIER_REGISTER_SCHEMA_VERSION",
    "LINKEDIN_GRAPH_FRONTIER_NEXT_RUN_ENVELOPE_SCHEMA_VERSION",
    "DEFAULT_LINKEDIN_GRAPH_FRONTIER_NON_CLAIMS",
    "FrontierNodeType",
    "FrontierEdgeType",
    "ProjectionDecision",
    "PERSON_CANDIDATE_NODE_TYPES",
    "FrontierNode",
    "FrontierEdge",
    "FrontierDecision",
    "NextRunEnvelope",
]


LINKEDIN_GRAPH_FRONTIER_REGISTER_SCHEMA_VERSION = "linkedin_graph_frontier_register_v0"
LINKEDIN_GRAPH_FRONTIER_NEXT_RUN_ENVELOPE_SCHEMA_VERSION = (
    "linkedin_graph_frontier_next_run_envelope_v0"
)


DEFAULT_LINKEDIN_GRAPH_FRONTIER_NON_CLAIMS: tuple[str, ...] = (
    "not live LinkedIn access",
    "not Graph Frontier-owned live fetch",
    "not implementation authorization",
    "not automatic promotion or capture",
    "not contact acquisition or lead list",
    "not follower/connection/commenter graph capture",
    "not profile body or content capture",
    "not Source Capture Packet output",
    "not Data Capture handoff",
    "not Outreach Lane execution",
    "not commercial use, validation, or readiness",
)


class FrontierNodeType(StrEnum):
    # Source-shaped nodes only. ``frontier_decision`` and ``stop_event`` from the
    # architecture's conceptual node vocabulary are NOT modeled as nodes here --
    # decisions live in frontier_decisions[] and a stop is a field/event (the
    # owner-locked "separate structures, not nodes" decision; mirrors reddit).
    RUN = "run"
    THEME = "theme"
    SOURCE_LOCATOR = "source_locator"
    BUSINESS_CANDIDATE = "business_candidate"
    ORGANIZATION_CANDIDATE = "organization_candidate"
    PUBLIC_PROFESSIONAL_ACTOR_CANDIDATE = "public_professional_actor_candidate"
    SENIOR_DECISION_MAKER_CANDIDATE = "senior_decision_maker_candidate"
    CREATOR_OR_INFLUENCER_CANDIDATE = "creator_or_influencer_candidate"


class FrontierEdgeType(StrEnum):
    DISCOVERED_FROM_RUN = "discovered_from_run"
    FOUND_ON_SOURCE_SURFACE = "found_on_source_surface"
    SAME_THEME_OVERLAP = "same_theme_overlap"
    SAME_COMPANY_OR_ORG_CONTEXT = "same_company_or_org_context"
    PUBLIC_ROLE_CONTEXT = "public_role_context"
    SOURCE_LOCATOR_OVERLAP = "source_locator_overlap"
    PRIOR_SEEN = "prior_seen"
    SELECTED_AS_FRONTIER = "selected_as_frontier"
    HELD_FOR_REVIEW = "held_for_review"
    QUARANTINED_PRIVACY = "quarantined_privacy"
    DEAD_END = "dead_end"


class ProjectionDecision(StrEnum):
    # Semantic Projection classes (architecture); carried on the decision record.
    PROMOTE = "promote"
    HOLD = "hold"
    QUARANTINE = "quarantine"
    DEAD_END = "dead_end"


# Person-candidate node types carry the slice-1 person-privacy posture.
PERSON_CANDIDATE_NODE_TYPES: frozenset[FrontierNodeType] = frozenset(
    {
        FrontierNodeType.PUBLIC_PROFESSIONAL_ACTOR_CANDIDATE,
        FrontierNodeType.SENIOR_DECISION_MAKER_CANDIDATE,
        FrontierNodeType.CREATOR_OR_INFLUENCER_CANDIDATE,
    }
)


@dataclass(frozen=True)
class FrontierNode:
    node_id: str
    node_type: FrontierNodeType
    run_id: str
    source_surface: str
    source_url_or_locator: str
    query_or_seed: str
    timestamp: str
    method_mode: str
    access_mode: str
    source_policy_posture: str
    caps_applied: dict[str, int]
    exclusions: tuple[str, ...]
    stop_reason: str
    non_claims: tuple[str, ...] = DEFAULT_LINKEDIN_GRAPH_FRONTIER_NON_CLAIMS
    prior_pointer_or_none: str | None = None
    candidate_value_or_none: str | None = None
    # Person-privacy posture -- required on person-candidate nodes (see validator).
    privacy_sensitivity_or_none: str | None = None
    minimization_rule_or_none: str | None = None
    person_data_minimized_or_none: str | None = None
    senior_role_or_public_actor_basis_or_none: str | None = None
    # Visible influence -- counts / coarse bands only, never graphs.
    visible_follower_count_or_none: str | None = None
    visible_connection_count_band_or_none: str | None = None
    visible_influence_absent_reason_or_none: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class FrontierEdge:
    edge_id: str
    edge_type: FrontierEdgeType
    from_node_id: str
    to_node_id: str
    run_id: str
    source_surface: str
    timestamp: str
    method_mode: str
    stop_reason: str
    non_claims: tuple[str, ...] = DEFAULT_LINKEDIN_GRAPH_FRONTIER_NON_CLAIMS
    # A public_role_context edge must carry a theme linkage (not general tracking).
    theme_linkage_or_none: str | None = None
    prior_pointer_or_none: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class FrontierDecision:
    decision_id: str
    selected_node_id: str
    projection_decision: ProjectionDecision
    frontier_selection_reason: str
    frontier_selection_actor: str
    frontier_selection_timestamp: str
    next_run_id_or_none: str | None = None
    non_claims: tuple[str, ...] = DEFAULT_LINKEDIN_GRAPH_FRONTIER_NON_CLAIMS

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class NextRunEnvelope:
    next_run_id: str
    originating_run_id: str
    selected_node_id: str
    prior_register_pointer: str
    declared_theme_or_decision_context: str
    declared_seed_or_surface: str
    candidate_surface_allowlist: tuple[str, ...]
    caps: dict[str, int]
    exclusions: tuple[str, ...]
    method_mode: str
    access_mode: str
    source_policy_posture: str
    stop_condition: str
    schema_version: str = LINKEDIN_GRAPH_FRONTIER_NEXT_RUN_ENVELOPE_SCHEMA_VERSION
    non_commercial_posture: str = "pre_commercial"
    execution_authorized: bool = False
    non_claims: tuple[str, ...] = DEFAULT_LINKEDIN_GRAPH_FRONTIER_NON_CLAIMS

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


def _enum_values(value: Any) -> Any:
    if isinstance(value, StrEnum):
        return value.value
    if isinstance(value, tuple):
        return [_enum_values(item) for item in value]
    if isinstance(value, list):
        return [_enum_values(item) for item in value]
    if isinstance(value, dict):
        return {key: _enum_values(item) for key, item in value.items()}
    return value
