"""Bounded Reddit Candidate URL Intake projection and receipt support."""

from capture_spine.reddit_candidate_intake.models import (
    CandidateSubredditRow,
    CandidateSurface,
    CandidateThreadUrlRow,
    CapType,
    CoverageClaim,
    OutboundUrlCandidateRow,
    PromotionReceipt,
    RedditCandidateIntakeError,
    RunEnvelope,
    RunProvenanceReceipt,
    StopReason,
)
from capture_spine.reddit_candidate_intake.validation import (
    DEFAULT_CAPS,
    assert_no_forbidden_output_fields,
    validate_old_reddit_html_listing_input_url,
    validate_old_reddit_listing_url,
    validate_old_reddit_thread_url,
    validate_promotion_receipt,
    validate_run_envelope,
)
from capture_spine.reddit_candidate_intake.projection import (
    project_old_reddit_html_candidate_subreddits,
    project_old_reddit_html_listing,
)
from capture_spine.reddit_candidate_intake.writer import (
    build_candidate_intake_output,
    write_candidate_intake_output,
)

__all__ = [
    "DEFAULT_CAPS",
    "CandidateSubredditRow",
    "CandidateSurface",
    "CandidateThreadUrlRow",
    "CapType",
    "CoverageClaim",
    "OutboundUrlCandidateRow",
    "PromotionReceipt",
    "RedditCandidateIntakeError",
    "RunEnvelope",
    "RunProvenanceReceipt",
    "StopReason",
    "assert_no_forbidden_output_fields",
    "build_candidate_intake_output",
    "project_old_reddit_html_listing",
    "project_old_reddit_html_candidate_subreddits",
    "validate_old_reddit_html_listing_input_url",
    "validate_old_reddit_listing_url",
    "validate_old_reddit_thread_url",
    "validate_promotion_receipt",
    "validate_run_envelope",
    "write_candidate_intake_output",
]
