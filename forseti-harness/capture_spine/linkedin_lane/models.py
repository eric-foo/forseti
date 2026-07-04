"""LinkedIn Lane no-live discovery harness -- slice 1 data models.

Mirrors the capture_spine Reddit lane-support pattern (frozen dataclass +
StrEnum + a custom ``*Error(ValueError)`` + module-level ``validate_*`` in
``validation.py``), NOT the signal_content pydantic pattern: this is an
internal, high-volume capture record, so it sits on the dataclass side of the
pydantic-at-the-boundary / dataclass-internal split.

Slice 1 scope: ``RunEnvelope`` + ``CandidateRow`` only. The Graph Frontier
register and ``PromotionReceipt`` are deferred to slice 2. Field set is a
mechanical translation of the committed LinkedIn Lane architecture Candidate Row
Schema; the validators (``validation.py``) translate the review-cleared pilot
acceptance gate. No live runner, no supervised-browser-assist execution, no
promotion/capture execution, no persistence beyond a local planning artifact.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


LINKEDIN_LANE_CANDIDATE_ROW_SCHEMA_VERSION = "linkedin_lane_candidate_row_v0"
LINKEDIN_LANE_RUN_ENVELOPE_SCHEMA_VERSION = "linkedin_lane_run_envelope_v0"


DEFAULT_LINKEDIN_LANE_NON_CLAIMS: tuple[str, ...] = (
    "not live LinkedIn access",
    "not supervised browser-assist unless explicitly opted in",
    "not no-entitlement gate bypass",
    "not contact acquisition or lead list",
    "not follower/connection/commenter graph capture",
    "not profile body or content capture",
    "not Source Capture Packet output",
    "not Data Capture handoff",
    "not Outreach Lane execution",
    "not auto-promotion to Capture or Outreach",
    "not commercial use, validation, or readiness",
)


class LinkedInLaneError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class CandidateClass(StrEnum):
    BUSINESS = "business"
    ORGANIZATION = "organization"
    PUBLIC_PROFESSIONAL_ACTOR = "public_professional_actor"
    SENIOR_DECISION_MAKER = "senior_decision_maker"
    EXECUTIVE = "executive"
    CREATOR_OR_INFLUENCER = "creator_or_influencer"
    ANALYST_OR_INVESTOR = "analyst_or_investor"
    EVENT_OR_PUBLIC_ROLE_ACTOR = "event_or_public_role_actor"


class EntityType(StrEnum):
    BUSINESS_ENTITY = "business_entity"
    ORGANIZATION_ENTITY = "organization_entity"
    INDIVIDUAL_PERSON = "individual_person"


class MethodMode(StrEnum):
    MANUAL_OPERATOR_BROWSING = "manual_operator_browsing"
    SALES_NAVIGATOR_MANUAL_ENTITLED = "sales_navigator_manual_entitled"
    OPERATOR_SUPPLIED_LINK_OR_NOTE = "operator_supplied_link_or_note"
    AGENT_ASSISTED_ROWING_ONLY = "agent_assisted_rowing_only"
    SUPERVISED_BROWSER_ASSIST_OPTIONAL_POC_RISK = "supervised_browser_assist_optional_poc_risk"
    OWNER_PRESENT_ATTENDED_AUTOMATION_OPTIONAL_POC_RISK = "owner_present_attended_automation_optional_poc_risk"


class SourceSurface(StrEnum):
    OPERATOR_SUPPLIED_SEED_LIST = "operator_supplied_seed_list"
    COMPANY_WEBSITE_BLOG_PRESS_PRICING = "company_website_blog_press_pricing"
    CONFERENCE_PODCAST_NEWSLETTER_PUBLICATION = "conference_podcast_newsletter_publication"
    PUBLIC_DIRECTORY_OR_ECOSYSTEM_LIST = "public_directory_or_ecosystem_list"
    MANUAL_SEARCH_RESULT_REVIEW = "manual_search_result_review"
    SALES_NAVIGATOR_MANUAL_ENTITLED = "sales_navigator_manual_entitled"
    LINKEDIN_COMPANY_PAGE_OR_POST = "linkedin_company_page_or_post"
    LINKEDIN_PUBLIC_OR_PERSON_URL = "linkedin_public_or_person_url"
    SUPERVISED_BROWSER_ASSIST = "supervised_browser_assist"


class StopReason(StrEnum):
    CAPS_REACHED = "caps_reached"
    SCOPE_EXHAUSTED = "scope_exhausted"
    EMPTY_RESULT = "empty_result"
    BLOCKED_RESULT = "blocked_result"
    PRIVACY_DRIFT = "privacy_drift"
    OPERATOR_STOP = "operator_stop"
    HARD_STOP_TRIGGERED = "hard_stop_triggered"


class PrivacySensitivity(StrEnum):
    BUSINESS_LOW = "business_low"
    PERSON_STRICT = "person_strict"
    PUBLIC_ACTOR_STRICT = "public_actor_strict"
    QUARANTINE = "quarantine"


class MinimizationRule(StrEnum):
    BUSINESS_ENTITY_ONLY = "business_entity_only"
    NAME_ROLE_LOCATOR_ONLY = "name_role_locator_only"
    NO_CONTACT_FIELDS = "no_contact_fields"
    REVIEW_REQUIRED = "review_required"


class PersonDataMinimized(StrEnum):
    YES = "yes"
    NO = "no"
    NOT_APPLICABLE = "not_applicable"


# Person rows carry stricter flags than business/org rows (architecture). These
# sets are the validator's notion of "this row is about a person".
PERSON_ENTITY_TYPES: frozenset[EntityType] = frozenset({EntityType.INDIVIDUAL_PERSON})
PERSON_PRIVACY_SENSITIVITIES: frozenset[PrivacySensitivity] = frozenset(
    {
        PrivacySensitivity.PERSON_STRICT,
        PrivacySensitivity.PUBLIC_ACTOR_STRICT,
        PrivacySensitivity.QUARANTINE,
    }
)


@dataclass(frozen=True)
class VisibleInfluenceNumbers:
    """Visible counts / coarse bands only -- influence context, NOT network capture.

    Field names are deliberately ``*_count_or_none`` / ``*_band_or_none`` so they
    never collide with the forbidden follower/connection LIST field names the
    output walk rejects.
    """

    follower_count_or_none: str | None = None
    connection_count_band_or_none: str | None = None
    subscriber_count_or_none: str | None = None
    engagement_count_or_none: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class RunEnvelope:
    run_id: str
    declared_theme_or_decision_context: str
    run_purpose: str
    candidate_classes: tuple[CandidateClass, ...]
    source_surface_allowlist: tuple[SourceSurface, ...]
    method_mode: MethodMode
    stop_condition: StopReason
    source_policy_posture: str
    minimization_rule: MinimizationRule
    promotion_owner: str
    max_businesses: int
    max_organizations: int
    max_people: int
    max_source_surfaces: int
    time_window_days: int
    schema_version: str = LINKEDIN_LANE_RUN_ENVELOPE_SCHEMA_VERSION
    optional_poc_risk_mode: bool = False
    non_commercial_posture: str = "pre_commercial"
    watch_window_or_none: str | None = None
    exclusions: tuple[str, ...] = ()
    non_claims: tuple[str, ...] = DEFAULT_LINKEDIN_LANE_NON_CLAIMS

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class CandidateRow:
    candidate_id: str
    run_id: str
    candidate_class: CandidateClass
    entity_type: EntityType
    display_name: str
    source_surface: SourceSurface
    source_policy_posture: str
    method_mode: MethodMode
    declared_theme_or_decision_context: str
    run_purpose: str
    business_relevance_note: str
    privacy_sensitivity: PrivacySensitivity
    minimization_rule: MinimizationRule
    person_data_minimized: PersonDataMinimized
    provenance_timestamp: str
    schema_version: str = LINKEDIN_LANE_CANDIDATE_ROW_SCHEMA_VERSION
    source_family: str = "linkedin_adjacent"
    capture_unit_intake_status: str = "candidate_or_scouting"
    allowed_downstream_use: str = "planning_only"
    promotion_required: bool = True
    optional_poc_risk_mode: bool = False
    canonical_locator_or_none: str | None = None
    source_locators: tuple[str, ...] = ()
    role_or_influence_basis_or_none: str | None = None
    senior_role_or_public_actor_basis_or_none: str | None = None
    visible_influence_numbers_or_none: VisibleInfluenceNumbers | None = None
    influence_number_source_surface_or_none: str | None = None
    excluded_fields_receipt: tuple[str, ...] = ()
    visible_stop_reason_if_any_or_none: str | None = None
    contact_fields_retained: bool = False
    network_or_follower_list_retained: bool = False
    profile_body_captured: bool = False
    content_captured: bool = False

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
