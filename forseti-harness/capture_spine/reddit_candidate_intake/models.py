from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class RedditCandidateIntakeError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class CapType(StrEnum):
    PROBE = "probe"
    WORKING_BATCH = "working_batch"
    HIGH_RECALL_PASS = "high_recall_pass"


class CoverageClaim(StrEnum):
    BOUNDED_PROBE_ONLY = "bounded_probe_only"
    BOUNDED_BATCH_ONLY = "bounded_batch_only"
    HIGH_RECALL_ATTEMPT_WITH_LIMITS = "high_recall_attempt_with_limits"


class StopReason(StrEnum):
    CAPS_REACHED = "caps_reached"
    SCOPE_EXHAUSTED = "scope_exhausted"
    EMPTY_RESULT = "empty_result"
    BLOCKED_RESULT = "blocked_result"
    OPERATOR_STOP = "operator_stop"
    HARD_STOP_TRIGGERED = "hard_stop_triggered"
    COMMERCIAL_REROUTE_REQUIRED = "commercial_reroute_required"


class CandidateSurface(StrEnum):
    SEED_SUBREDDITS = "seed_subreddits"
    REDDIT_SEARCH_LISTING = "reddit_search_listing"
    SUBREDDIT_LISTING = "subreddit_listing"
    CROSS_POST = "cross_post"
    RELATED_SUBREDDIT = "related_subreddit"
    RECOMMENDATION = "recommendation"
    MORE_LIKE_THIS = "more_like_this"
    OUTBOUND_LINKS = "outbound_links"


@dataclass(frozen=True)
class RunEnvelope:
    run_id: str
    run_purpose: str
    cap_type: CapType
    coverage_claim: CoverageClaim
    max_subreddits: int
    max_threads_per_subreddit: int
    max_pages_or_result_surfaces: int
    time_window_days: int
    sort_order: str
    method_category: str
    stop_condition: StopReason
    declared_topic_theme_query: str | None = None
    seed_subreddits: tuple[str, ...] = ()
    exclusions: tuple[str, ...] = ()
    candidate_surface_allowlist: tuple[CandidateSurface, ...] = (
        CandidateSurface.SEED_SUBREDDITS,
        CandidateSurface.REDDIT_SEARCH_LISTING,
        CandidateSurface.SUBREDDIT_LISTING,
        CandidateSurface.CROSS_POST,
        CandidateSurface.RELATED_SUBREDDIT,
    )
    non_commercial_posture: str = "pre_commercial"

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class CandidateSubredditRow:
    run_id: str
    candidate_subreddit: str
    source_surface: CandidateSurface
    source_url: str
    query_or_seed: str
    timestamp: str
    method_category: str
    exclusion_receipt: tuple[str, ...] = ()
    visible_subscriber_count_or_none: str | None = None
    visible_active_user_count_or_none: str | None = None
    visible_volume_signal_absent_reason_or_none: str | None = None
    capture_unit_intake_status: str = "candidate_or_scouting"
    allowed_downstream_use: str = "planning_only"
    same_run_traversal_authorized: bool = False

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class CandidateThreadUrlRow:
    run_id: str
    candidate_thread_url: str
    subreddit: str
    source_surface: CandidateSurface
    query_or_seed: str
    timestamp: str
    method_category: str
    visible_listing_title: str | None = None
    visible_listing_timestamp: str | None = None
    visible_listing_score_state: str | None = None
    exclusion_receipt: tuple[str, ...] = ()
    capture_unit_intake_status: str = "candidate_or_scouting"
    allowed_downstream_use: str = "planning_only"
    same_run_traversal_authorized: bool = False

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class OutboundUrlCandidateRow:
    run_id: str
    outbound_url: str
    originating_reddit_url: str
    source_surface: CandidateSurface
    timestamp: str
    method_category: str
    exclusion_receipt: tuple[str, ...] = ()
    requires_separate_source_family_intake: bool = True
    capture_unit_intake_status: str = "candidate_or_scouting"
    allowed_downstream_use: str = "planning_only"

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class RunProvenanceReceipt:
    run_id: str
    caps_applied: dict[str, int]
    source_surface: str
    query_or_listing_path: str
    sort_order: str
    time_window_days: int
    method_category: str
    timestamp: str
    row_counts: dict[str, int]
    stop_reason: StopReason
    exclusions_applied: tuple[str, ...] = ()
    non_commercial_posture: str = "pre_commercial"
    non_claims: tuple[str, ...] = (
        "not live Reddit access",
        "not Source Capture Packet output",
        "not body/comment/profile capture",
        "not Data Capture handoff",
        "not source-quality scoring",
    )

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class PromotionReceipt:
    promoted_url: str
    originating_run_id: str
    candidate_row_pointer: str
    reason_for_promotion: str
    known_limitations: tuple[str, ...]
    selected_downstream_capture_method: str
    approved_downstream_access_route: str | None
    decision_frame_or_capture_unit_authority: str | None
    non_promoted_candidate_rows: tuple[str, ...]
    source_capture_armory_execution_happened: bool = False
    capture_not_yet_authorized: bool = True

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
