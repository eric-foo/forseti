from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class GraphFrontierError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class FrontierNodeType(StrEnum):
    # Node types are discovered sources plus the run that found them. Frontier
    # decisions live in a separate frontier_decisions[] structure and a stop is a
    # field/event -- they are not FrontierNode instances (no source shape).
    RUN = "run"
    SUBREDDIT_CANDIDATE = "subreddit_candidate"
    THREAD_URL_CANDIDATE = "thread_url_candidate"
    OUTBOUND_URL_CANDIDATE = "outbound_url_candidate"


class FrontierEdgeType(StrEnum):
    DISCOVERED_FROM_RUN = "discovered_from_run"
    FOUND_ON_SURFACE = "found_on_surface"
    CROSSPOST_RELATION = "crosspost_relation"
    RELATED_SUBREDDIT_RELATION = "related_subreddit_relation"
    RECOMMENDATION_RELATION = "recommendation_relation"
    MORE_LIKE_THIS_RELATION = "more_like_this_relation"
    OUTBOUND_LINK_RELATION = "outbound_link_relation"
    SELECTED_AS_NEXT_FRONTIER = "selected_as_next_frontier"
    REJECTED_FOR_FRONTIER = "rejected_for_frontier"
    ALREADY_SEEN = "already_seen"
    BLOCKED_OR_EMPTY = "blocked_or_empty"


DEFAULT_GRAPH_FRONTIER_NON_CLAIMS: tuple[str, ...] = (
    "not Graph Frontier-owned live Reddit fetch",
    "not implementation authorization",
    "not automatic capture",
    "not broad crawling authorization",
    "not Source Capture",
    "not Source Capture Packet output",
    "not Data Capture handoff",
    "not source-quality scoring",
    "not ECR, Cleaning, Judgment, fixture admission, or commercial permission",
)

GRAPH_FRONTIER_REGISTER_SCHEMA_VERSION = "reddit_graph_frontier_register_v0"
GRAPH_FRONTIER_NEXT_RUN_ENVELOPE_SCHEMA_VERSION = (
    "reddit_graph_frontier_next_run_envelope_v0"
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
    method_category: str
    access_mode: str
    caps_applied: dict[str, int]
    exclusions: tuple[str, ...]
    stop_reason: str
    non_claims: tuple[str, ...] = DEFAULT_GRAPH_FRONTIER_NON_CLAIMS
    prior_pointer_or_none: str | None = None
    sort_order_or_none: str | None = None
    time_window_or_none: int | None = None
    candidate_value_or_none: str | None = None
    visible_subscriber_count_or_none: str | None = None
    visible_active_user_count_or_none: str | None = None
    visible_volume_signal_absent_reason_or_none: str | None = None

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
    method_category: str
    stop_reason: str
    non_claims: tuple[str, ...] = DEFAULT_GRAPH_FRONTIER_NON_CLAIMS
    prior_pointer_or_none: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class FrontierDecision:
    decision_id: str
    selected_node_id: str
    frontier_selection_reason: str
    frontier_selection_actor: str
    frontier_selection_timestamp: str
    decision: str = "selected_as_next_frontier"
    next_run_id_or_none: str | None = None
    non_claims: tuple[str, ...] = DEFAULT_GRAPH_FRONTIER_NON_CLAIMS

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class NextRunEnvelope:
    next_run_id: str
    selected_node_id: str
    prior_register_pointer: str
    declared_topic_theme_or_query: str
    declared_seed_or_surface: str
    candidate_surface_allowlist: tuple[str, ...]
    caps: dict[str, int]
    exclusions: tuple[str, ...]
    access_mode: str
    source_policy_posture: str
    stop_condition: str
    schema_version: str = GRAPH_FRONTIER_NEXT_RUN_ENVELOPE_SCHEMA_VERSION
    non_commercial_posture: str = "pre_commercial"
    execution_authorized: bool = False
    non_claims: tuple[str, ...] = DEFAULT_GRAPH_FRONTIER_NON_CLAIMS

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
