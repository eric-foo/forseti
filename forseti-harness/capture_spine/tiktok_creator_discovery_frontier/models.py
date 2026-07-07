"""Data models for the TikTok Creator Discovery Frontier register.

This package is intentionally validator-only. It does not launch TikTok, write
Source Capture Packets, mutate Creator Registry data, or authorize next runs.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


TIKTOK_CREATOR_DISCOVERY_FRONTIER_REGISTER_SCHEMA_VERSION = (
    "tiktok_creator_discovery_frontier_register_v0"
)
TIKTOK_CREATOR_DISCOVERY_NEXT_RUN_ENVELOPE_SCHEMA_VERSION = (
    "tiktok_creator_discovery_next_run_envelope_v0"
)
TIKTOK_CREATOR_DISCOVERY_SCAN_RECEIPT_SCHEMA_VERSION = (
    "tiktok_creator_discovery_scan_receipt_v0"
)

DEFAULT_TIKTOK_CREATOR_DISCOVERY_FRONTIER_NON_CLAIMS: tuple[str, ...] = (
    "not Creator Registry identity proof",
    "not follower graph",
    "not following graph",
    "not endorsement proof",
    "not country/region evidence",
    "not metric rollup",
    "not capture execution authorization",
    "not source-access authorization",
    "not standing crawler or monitor",
    "not account completeness proof",
)


class TikTokCreatorDiscoveryFrontierError(ValueError):
    """Raised when a TikTok creator discovery frontier artifact is invalid."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class FrontierNodeType(StrEnum):
    RUN = "run"
    TIKTOK_CREATOR_SEED = "tiktok_creator_seed"
    TIKTOK_CREATOR_CANDIDATE = "tiktok_creator_candidate"


class FrontierEdgeType(StrEnum):
    DISCOVERED_FROM_RUN = "discovered_from_run"
    PLATFORM_SUGGESTED_ACCOUNT_RELATION = "platform_suggested_account_relation"
    ALREADY_SEEN = "already_seen"
    SELECTED_AS_NEXT_FRONTIER = "selected_as_next_frontier"
    REJECTED_FOR_FRONTIER = "rejected_for_frontier"
    BLOCKED_OR_EMPTY = "blocked_or_empty"


class ProjectionDecision(StrEnum):
    PROMOTE = "promote"
    HOLD = "hold"
    REJECT = "reject"
    ALREADY_SEEN = "already_seen"


class RefreshOutcome(StrEnum):
    NOT_NEEDED = "not_needed"
    NO_VISIBLE_REFRESH_CONTROL = "no_visible_refresh_control"
    CLICKED_ONCE_RECOVERED = "clicked_once_recovered"
    CLICKED_ONCE_NO_RECOVERY = "clicked_once_no_recovery"
    VISIBLE_REFRESH_NOT_AUTHORIZED = "visible_refresh_not_authorized"


@dataclass(frozen=True)
class ScanReceipt:
    receipt_id: str
    run_id: str
    register_id: str
    root_seed: dict[str, str]
    source_surface: str
    captured_at_utc: str
    method_mode: str
    access_mode: str
    extraction_method: str
    browser_session_label_or_none: str | None
    parent_grid_packet_id_or_none: str | None
    parent_grid_packet_path_or_none: str | None
    source_packet_id_or_none: str | None
    source_packet_path_or_none: str | None
    parent_profile_capture_status: str
    suggested_accounts_capture_status: str
    browser_closed_by_runner: bool
    refresh_attempt_count: int
    refresh_outcome: RefreshOutcome
    pagination_bound: int
    suggested_accounts_observed: int
    candidate_profiles_opened: int
    follow_unfollow_actions_taken: int
    screenshots_emitted_to_chat: int
    caps_applied: dict[str, int]
    stop_reason: str
    exclusions: tuple[str, ...]
    schema_version: str = TIKTOK_CREATOR_DISCOVERY_SCAN_RECEIPT_SCHEMA_VERSION
    non_claims: tuple[str, ...] = DEFAULT_TIKTOK_CREATOR_DISCOVERY_FRONTIER_NON_CLAIMS

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class SuggestedAccountObservation:
    handle: str
    display_name_or_none: str | None = None
    source_url_or_locator: str | None = None
    registry_preflight_status_or_none: str | None = None
    platform_capture_status: str = "tiktok_suggested_account_target_only_not_profile_captured"
    cross_platform_graph_status: str = "not_started"
    confidence: str = "weak_platform_suggestion_only"
    observed_sections: tuple[str, ...] = ("suggested_accounts",)

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class FrontierNode:
    node_id: str
    node_type: FrontierNodeType
    platform: str
    handle_or_none: str | None
    display_name_or_none: str | None
    source_url_or_locator: str
    run_id: str
    source_surface: str
    timestamp: str
    method_mode: str
    access_mode: str
    caps_applied: dict[str, int]
    exclusions: tuple[str, ...]
    stop_reason: str
    registry_preflight_status_or_none: str | None
    platform_capture_status: str
    cross_platform_graph_status: str
    non_claims: tuple[str, ...] = DEFAULT_TIKTOK_CREATOR_DISCOVERY_FRONTIER_NON_CLAIMS

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
    source_packet_id_or_none: str | None
    observed_sections: tuple[str, ...]
    timestamp: str
    method_mode: str
    stop_reason: str
    confidence: str
    non_claims: tuple[str, ...] = DEFAULT_TIKTOK_CREATOR_DISCOVERY_FRONTIER_NON_CLAIMS

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
    non_claims: tuple[str, ...] = DEFAULT_TIKTOK_CREATOR_DISCOVERY_FRONTIER_NON_CLAIMS

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class NextRunEnvelope:
    next_run_id: str
    selected_node_id: str
    prior_register_pointer: str
    declared_seed_or_surface: str
    candidate_surface_allowlist: tuple[str, ...]
    caps: dict[str, int]
    exclusions: tuple[str, ...]
    method_mode: str
    access_mode: str
    source_policy_posture: str
    stop_condition: str
    schema_version: str = TIKTOK_CREATOR_DISCOVERY_NEXT_RUN_ENVELOPE_SCHEMA_VERSION
    execution_authorized: bool = False
    non_claims: tuple[str, ...] = DEFAULT_TIKTOK_CREATOR_DISCOVERY_FRONTIER_NON_CLAIMS

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
