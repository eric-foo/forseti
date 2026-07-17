from __future__ import annotations

from enum import StrEnum


class CreatorPublicHandleLinkageError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class Platform(StrEnum):
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"


class LinkState(StrEnum):
    DECLARED = "declared_public_account_link"
    PROBABLE = "probable_public_account_link"
    CANDIDATE = "candidate_public_account_link"
    REJECTED = "rejected_public_account_link"


class ReviewState(StrEnum):
    HUMAN_REVIEWED_DECLARED = "human_reviewed_declared"
    AUTO_PROMOTED_OFFICIAL_LINK_HUB = "auto_promoted_official_link_hub"
    HUMAN_REVIEWED_PROBABLE = "human_reviewed_probable"
    CANDIDATE_NEEDS_REVIEW = "candidate_needs_review"
    OPERATOR_REJECTED = "operator_rejected"


class EvidenceStrength(StrEnum):
    STRONG = "strong"
    WEAK = "weak"
    DISCONFIRMING = "disconfirming"


class EvidenceType(StrEnum):
    SELF_DECLARED_CROSS_LINK = "self_declared_cross_link"
    MUTUAL_PROFILE_LINK = "mutual_profile_link"
    OFFICIAL_LINK_HUB = "official_link_hub"
    HANDLE_SIMILARITY = "handle_similarity"
    PUBLIC_DISPLAY_NAME_SIMILARITY = "public_display_name_similarity"
    BIO_TEXT_OVERLAP = "bio_text_overlap"
    SHARED_PUBLIC_LINK_DESTINATION = "shared_public_link_destination"
    CONTENT_TOPIC_OVERLAP = "content_topic_overlap"
    CONFLICTING_SELF_DECLARATION = "conflicting_self_declaration"
    CONFLICTING_PUBLIC_LINK_HUB = "conflicting_public_link_hub"
    DIFFERENT_PUBLIC_ENTITY_SIGNAL = "different_public_entity_signal"
    OPERATOR_REJECTED_MATCH = "operator_rejected_match"


CREATOR_PUBLIC_HANDLE_LINKAGE_LEDGER_SCHEMA_VERSION = "creator_public_handle_linkage_ledger_v0"
SYNTHETIC_FIXTURE_MODE = "synthetic_fixture"
PUBLIC_HANDLE_LEDGER_MODE = "public_handle_ledger"

DEFAULT_LINKAGE_NON_CLAIMS: tuple[str, ...] = (
    "not real-world identity proof",
    "not non-public-handle join",
    "not contact or outreach authorization",
    "not follower or audience graph",
    "not public person-level product surface",
)
