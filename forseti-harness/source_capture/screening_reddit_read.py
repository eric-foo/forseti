from __future__ import annotations

# Bounded screening-read entry for public Reddit surfaces.
# Wires fetch_direct_http_capture (the screen-light adapter) only.
# Never imports or calls stage_and_write_packet / run_source_capture_http_packet.
# Contract: docs/decisions/screening_reddit_read_route_decision_v0.md

from dataclasses import dataclass, field
from typing import Literal
from urllib.parse import unquote, urlparse

from source_capture.adapters.direct_http import (
    DirectHttpCaptureFailure,
    DirectHttpCaptureSuccess,
    fetch_direct_http_capture,
)
from source_capture.access_gate import detect_login_gate
from source_capture.block_shell import classify_capture_body
from source_capture.screening_extraction import extract_screening_fields


_ALLOWED_HOSTS: frozenset[str] = frozenset({"old.reddit.com", "www.reddit.com"})
_PUBLIC_PATH_PREFIX = "/r/"
_ALLOWED_SCHEMES: frozenset[str] = frozenset({"https"})

RATE_CEILING_NOTE = (
    "Unauthenticated old.reddit HTML: human-rate, one bounded GET. "
    "The .json variant is rate-limited (~60 req/min unauthenticated) and "
    "ToS-bounded; treat as direct-HTTP rung at human rate with backoff. "
    "No scheduler, no crawler, no standing service."
)

@dataclass(frozen=True)
class RedditScreenLight:
    """Screen-light result: recorded fields only, no disk artifact, no ECR path."""

    final_url: str
    status: int
    byte_count: int
    comments_marker_count: int
    content_class: str = "content_unverified"
    content_signal: str | None = None
    content_class_detail: str = "not classified"
    extracted_fields: dict[str, object] = field(default_factory=dict)
    limitation_notes: list[str] = field(default_factory=list)
    rate_ceiling_note: str = field(default=RATE_CEILING_NOTE)


@dataclass(frozen=True)
class RedditScreeningReadRefused:
    """Entitlement gate refusal or fetch failure; no network call was made for gated URLs."""

    url: str
    reason: Literal["entitlement_gated", "login_redirect", "fetch_failed"]
    message: str


RedditScreeningReadResult = RedditScreenLight | RedditScreeningReadRefused


def reddit_screening_read(
    *,
    url: str,
    timeout_seconds: float = 20.0,
    max_bytes: int = 2_000_000,
    old_reddit_submission_min_datetime: str | None = None,
    old_reddit_submission_max_datetime: str | None = None,
) -> RedditScreeningReadResult:
    """
    Entitlement-gated, bounded screening read for public Reddit surfaces.

    Invocation: in-process import (not CLI subprocess). One bounded GET per call;
    orchestrator-invoked only; no standing service.

    Entitlement gate (pre-fetch): only old.reddit.com and www.reddit.com URLs
    whose path begins with /r/ are permitted. Auth-gated URLs are refused without
    a network call. Post-fetch: login redirects are detected and refused.

    Returns RedditScreenLight (screen-light, no packet/staging/ECR) or
    RedditScreeningReadRefused (gate refusal or fetch failure).
    """
    refused = _pre_fetch_entitlement_gate(url)
    if refused is not None:
        return refused

    result = fetch_direct_http_capture(
        url=url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
    )

    if isinstance(result, DirectHttpCaptureFailure):
        return RedditScreeningReadRefused(
            url=url,
            reason="fetch_failed",
            message=result.message,
        )

    body_text = result.body.decode("utf-8", errors="replace")

    post_gate = _post_fetch_entitlement_gate(url, result, body_text=body_text)
    if post_gate is not None:
        return post_gate

    marker_count = body_text.count("/comments/")
    classification = classify_capture_body(
        status=result.status,
        headers=_headers_from_direct_metadata(result),
        body=result.body,
    )
    extracted_fields = extract_screening_fields(
        url=result.final_url,
        body_text=body_text,
        old_reddit_submission_min_datetime=old_reddit_submission_min_datetime,
        old_reddit_submission_max_datetime=old_reddit_submission_max_datetime,
    )

    return RedditScreenLight(
        final_url=result.final_url,
        status=result.status,
        byte_count=int(result.metadata["byte_count"]),
        comments_marker_count=marker_count,
        content_class=classification.classification.value,
        content_signal=classification.signal,
        content_class_detail=classification.detail,
        extracted_fields=extracted_fields,
        limitation_notes=list(result.limitation_notes),
    )


def _pre_fetch_entitlement_gate(url: str) -> RedditScreeningReadRefused | None:
    """Classify public-vs-gated before any network call. Returns refusal if gated."""
    try:
        parsed = urlparse(url)
    except Exception as exc:
        return RedditScreeningReadRefused(
            url=url,
            reason="entitlement_gated",
            message=f"URL could not be parsed ({exc!r}); refusing without fetch.",
        )

    if parsed.scheme.lower() not in _ALLOWED_SCHEMES or not parsed.netloc:
        return RedditScreeningReadRefused(
            url=url,
            reason="entitlement_gated",
            message=(
                f"URL scheme {parsed.scheme!r} is not permitted; "
                "only absolute https:// Reddit URLs are permitted. "
                "Refused without a network call."
            ),
        )

    host = (parsed.hostname or "").lower()
    if host not in _ALLOWED_HOSTS:
        return RedditScreeningReadRefused(
            url=url,
            reason="entitlement_gated",
            message=(
                f"Host {host!r} is not a permitted public Reddit surface "
                f"(allowed: {sorted(_ALLOWED_HOSTS)}). "
                "Only old.reddit.com and www.reddit.com public /r/<sub>/... paths are permitted. "
                "Refused without a network call."
            ),
        )

    path = parsed.path or ""
    if not path.startswith(_PUBLIC_PATH_PREFIX):
        return RedditScreeningReadRefused(
            url=url,
            reason="entitlement_gated",
            message=(
                f"Path {path!r} does not begin with '/r/'; "
                "only public subreddit paths are permitted. "
                "Refused without a network call."
            ),
        )

    decoded_path = unquote(path)
    path_segments = decoded_path.split("/")
    if "." in path_segments or ".." in path_segments:
        return RedditScreeningReadRefused(
            url=url,
            reason="entitlement_gated",
            message=(
                f"Path {path!r} contains dot-segment traversal; "
                "only direct public subreddit paths are permitted. "
                "Refused without a network call."
            ),
        )

    return None


def _post_fetch_entitlement_gate(
    requested_url: str, result: DirectHttpCaptureSuccess, *, body_text: str
) -> RedditScreeningReadRefused | None:
    """Detect login redirects after the fetch; refuse if content was gated at the response level."""
    detection = detect_login_gate(final_url=result.final_url, body_text=body_text)
    if detection is None:
        return None
    return RedditScreeningReadRefused(
        url=requested_url,
        reason="login_redirect",
        message=(
            f"Reddit served an access-gated response ({detection.detail}); "
            "screen-light refused."
        ),
    )


def _headers_from_direct_metadata(result: DirectHttpCaptureSuccess) -> dict[str, str]:
    headers: dict[str, str] = {}
    content_type = result.metadata.get("content_type")
    if content_type is not None:
        headers["Content-Type"] = str(content_type)
    content_encoding = result.metadata.get("content_encoding")
    if content_encoding is not None:
        headers["Content-Encoding"] = str(content_encoding)
    return headers
