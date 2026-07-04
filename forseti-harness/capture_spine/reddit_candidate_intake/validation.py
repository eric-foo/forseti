from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

from capture_spine.reddit_candidate_intake.models import (
    CandidateSurface,
    CapType,
    CoverageClaim,
    PromotionReceipt,
    RedditCandidateIntakeError,
    RunEnvelope,
)


DEFAULT_CAPS: dict[CapType, dict[str, int | CoverageClaim]] = {
    CapType.PROBE: {
        "coverage_claim": CoverageClaim.BOUNDED_PROBE_ONLY,
        "max_subreddits": 5,
        "max_threads_per_subreddit": 25,
        "max_pages_or_result_surfaces": 2,
        "time_window_days": 30,
    },
    CapType.WORKING_BATCH: {
        "coverage_claim": CoverageClaim.BOUNDED_BATCH_ONLY,
        "max_subreddits": 20,
        "max_threads_per_subreddit": 75,
        "max_pages_or_result_surfaces": 5,
        "time_window_days": 180,
    },
    CapType.HIGH_RECALL_PASS: {
        "coverage_claim": CoverageClaim.HIGH_RECALL_ATTEMPT_WITH_LIMITS,
        "max_subreddits": 50,
        "max_threads_per_subreddit": 150,
        "max_pages_or_result_surfaces": 10,
        "time_window_days": 365,
    },
}

FORBIDDEN_OUTPUT_FIELDS = {
    "body",
    "body_text",
    "selftext",
    "selftext_html",
    "body_html",
    "comment",
    "comments",
    "comment_body",
    "comment_text",
    "profile",
    "user_profile",
    "user_data",
    "raw_html",
    "html",
    "rendered_dom",
    "dom",
    "parser_output",
    "screenshot",
    "screenshot_path",
    "cookie",
    "cookies",
    "session",
    "session_state",
    "hidden_session_state",
    "authorization_header",
    "source_capture_packet",
    "packet_manifest",
    "ecr",
    "cleaning",
    "judgment",
    "source_quality_score",
    "author",
    "author_fullname",
}

_OLD_REDDIT_LISTING_RE = re.compile(
    r"^https://old\.reddit\.com/r/(?P<subreddit>[A-Za-z0-9_]{1,80})(?:/)?(?:[?#].*)?$"
)
_OLD_REDDIT_HTML_LISTING_INPUT_RE = re.compile(
    r"^https://old\.reddit\.com/r/(?P<subreddit>[A-Za-z0-9_]{1,80})"
    r"(?:/(?:hot|new|top|rising|controversial|search))?/?(?:[?#].*)?$"
)
_OLD_REDDIT_THREAD_RE = re.compile(
    r"^https://old\.reddit\.com/r/(?P<subreddit>[A-Za-z0-9_]{1,80})/comments/"
    r"(?P<thread_id>[A-Za-z0-9]{1,16})(?:/[^/?#]*)?/?(?:[?#].*)?$"
)


def validate_run_envelope(envelope: RunEnvelope) -> None:
    if not envelope.run_id.strip():
        _fail("missing_run_id", "run_id is required")
    if not envelope.run_purpose.strip():
        _fail("missing_run_purpose", "run_purpose is required")
    if not envelope.declared_topic_theme_query and not envelope.seed_subreddits:
        _fail("missing_declared_scope", "declared topic/theme/query or seed subreddits are required")
    if envelope.coverage_claim != DEFAULT_CAPS[envelope.cap_type]["coverage_claim"]:
        _fail("coverage_claim_mismatch", "coverage_claim must match cap_type")
    if envelope.max_subreddits < 1:
        _fail("invalid_max_subreddits", "max_subreddits must be positive")
    if envelope.max_threads_per_subreddit < 1:
        _fail("invalid_max_threads_per_subreddit", "max_threads_per_subreddit must be positive")
    if envelope.max_pages_or_result_surfaces < 1:
        _fail("invalid_max_pages_or_result_surfaces", "max_pages_or_result_surfaces must be positive")
    if envelope.time_window_days < 1:
        _fail("invalid_time_window_days", "time_window_days must be positive")
    if CandidateSurface.OUTBOUND_LINKS in envelope.candidate_surface_allowlist:
        # Separate outbound numeric caps are owner policy; the local model only enforces explicit opt-in.
        return


def validate_old_reddit_listing_url(url: str) -> str:
    match = _OLD_REDDIT_LISTING_RE.match(url.strip())
    if not match:
        _fail("non_old_reddit_listing_url", "expected old Reddit subreddit listing URL")
    return match.group("subreddit")


def validate_old_reddit_html_listing_input_url(url: str) -> str:
    stripped = url.strip()
    if _is_reddit_json_url(stripped):
        _fail("reddit_json_input_forbidden", "Reddit .json URLs are blocked for Candidate URL Intake")
    if stripped.startswith(("https://www.reddit.com/", "https://reddit.com/")):
        _fail("new_reddit_non_default", "new Reddit URLs are non-default for Candidate URL Intake")
    if "/comments/" in stripped:
        _fail("reddit_thread_input_forbidden", "thread pages are candidate outputs, not intake input surfaces")
    match = _OLD_REDDIT_HTML_LISTING_INPUT_RE.match(stripped)
    if not match:
        _fail("non_old_reddit_html_listing_input_url", "expected old Reddit HTML listing or search URL")
    return match.group("subreddit")


def validate_old_reddit_thread_url(url: str) -> tuple[str, str]:
    stripped = url.strip()
    if _is_reddit_json_url(stripped):
        _fail("reddit_json_input_forbidden", "Reddit .json URLs are blocked for Candidate URL Intake")
    if stripped.startswith(("https://www.reddit.com/", "https://reddit.com/")):
        _fail("new_reddit_non_default", "new Reddit URLs are non-default for Candidate URL Intake")
    match = _OLD_REDDIT_THREAD_RE.match(stripped)
    if not match:
        _fail("non_old_reddit_thread_url", "expected old Reddit thread URL")
    return match.group("subreddit"), match.group("thread_id")


def validate_candidate_row_mapping(row: Mapping[str, Any]) -> None:
    assert_no_forbidden_output_fields(row)
    if row.get("capture_unit_intake_status") != "candidate_or_scouting":
        _fail("invalid_capture_unit_intake_status", "candidate rows must remain candidate_or_scouting")
    if row.get("allowed_downstream_use") != "planning_only":
        _fail("invalid_allowed_downstream_use", "candidate rows must remain planning_only")
    if row.get("same_run_traversal_authorized") is True:
        _fail("same_run_traversal_forbidden", "same-run traversal from candidate rows is forbidden")


# Conservative secret-VALUE markers: defense-in-depth beyond the field-name
# blocklist above. The key blocklist stops secret-NAMED fields (cookie, session,
# authorization_header); this stops a credential that lands in a legitimately
# named field. Each pattern anchors on an unambiguous credential marker, never on
# entropy, so it does not false-positive on the candidate/frontier value
# vocabulary (base36 thread ids, hash-like node ids, permalinks, subreddit names,
# run ids). The design favors false negatives over false positives: a missed
# secret is a containable gap; a rejected legitimate value breaks the pipeline.
_FORBIDDEN_OUTPUT_VALUE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("pem_private_key", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("bearer_token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=\-]{16,}")),
    ("credentialed_url_userinfo", re.compile(r"://[^/\s:@]+:[^/\s:@]+@")),
    ("set_cookie_header", re.compile(r"(?i)\bset-cookie:\s*[^=\s;]+=[^=\s;]+")),
)


def assert_no_forbidden_output_fields(value: Any, *, path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            lowered = str(key).lower()
            if lowered in FORBIDDEN_OUTPUT_FIELDS:
                _fail("forbidden_output_field", f"forbidden output field at {path}.{key}")
            assert_no_forbidden_output_fields(child, path=f"{path}.{key}")
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, child in enumerate(value):
            assert_no_forbidden_output_fields(child, path=f"{path}[{index}]")
        return
    if isinstance(value, str):
        _assert_no_forbidden_output_value(value, path=path)


def _assert_no_forbidden_output_value(value: str, *, path: str) -> None:
    for marker, pattern in _FORBIDDEN_OUTPUT_VALUE_PATTERNS:
        if pattern.search(value):
            _fail("forbidden_output_value", f"forbidden secret-like value ({marker}) at {path}")


def validate_promotion_receipt(receipt: PromotionReceipt) -> None:
    if receipt.source_capture_armory_execution_happened:
        _fail("armory_execution_forbidden", "promotion receipt cannot record Armory execution as already happened")
    if not receipt.capture_not_yet_authorized:
        _fail("capture_authorization_leak", "promotion receipt must carry capture_not_yet_authorized: yes")
    if not receipt.known_limitations:
        _fail("missing_known_limitations", "promotion receipt must carry known limitations from intake provenance")
    if receipt.decision_frame_or_capture_unit_authority and receipt.capture_not_yet_authorized:
        return


def _fail(code: str, message: str) -> None:
    raise RedditCandidateIntakeError(code, message)


def _is_reddit_json_url(url: str) -> bool:
    path = url.split("?", 1)[0].split("#", 1)[0].rstrip("/")
    return path.endswith(".json")
