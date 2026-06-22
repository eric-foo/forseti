from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from ipaddress import ip_address
from typing import Literal, TypeAlias
from urllib.parse import quote_plus, urlparse

from source_capture.adapters.anti_blocking_http import (
    AntiBlockingHttpCaptureFailure,
    AntiBlockingHttpCaptureSuccess,
    fetch_anti_blocking_http_capture,
)
from source_capture.adapters.direct_http import (
    DirectHttpCaptureFailure,
    DirectHttpCaptureSuccess,
    fetch_direct_http_capture,
)
from source_capture.block_shell import classify_capture_body
from source_capture.screening_extraction import extract_screening_fields
from source_capture.screening_reddit_read import (
    RATE_CEILING_NOTE,
    RedditScreeningReadRefused,
    RedditScreenLight,
    reddit_screening_read,
)


HUMAN_RATE_NOTE = (
    "orchestrator-invoked screening read; one source / one question; "
    "human-rate; no standing service, crawler, scheduler, packet, manifest, or ECR"
)
OLD_REDDIT_FIRST_ACT_SUBREDDIT = "beauty"
OLD_REDDIT_FIRST_ACT_QUERY = "skincare moisturizer"


class ScreeningReadRoute(StrEnum):
    REDDIT_SCREENING_READ = "reddit_screening_read"
    DIRECT_HTTP = "direct_http"
    ANTI_BLOCKING_HTTP = "anti_blocking_http"
    BROWSER = "screening_browser_read"


@dataclass(frozen=True)
class ScreeningReadDispatch:
    screen_id: str
    question: str
    invoked_by: Literal["screen_orchestrator"] = "screen_orchestrator"


@dataclass(frozen=True)
class ScreeningReadRecord:
    requested_url: str
    final_url: str
    route: str
    status: int | None
    byte_count: int
    content_class: str
    content_signal: str | None
    content_class_detail: str
    extracted_fields: dict[str, object] = field(default_factory=dict)
    content_type: str | None = None
    warning_notes: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)
    human_rate_note: str = HUMAN_RATE_NOTE


@dataclass(frozen=True)
class ScreeningReadRefused:
    requested_url: str
    route: str
    reason: Literal[
        "not_orchestrator_invoked",
        "unbounded_dispatch",
        "entitlement_gated",
        "login_redirect",
        "fetch_failed",
    ]
    message: str


ScreeningReadResult: TypeAlias = ScreeningReadRecord | ScreeningReadRefused


def screening_read(
    *,
    url: str,
    route: ScreeningReadRoute | str,
    dispatch: ScreeningReadDispatch,
    timeout_seconds: float = 20.0,
    max_bytes: int = 2_000_000,
    browser_wait_until: str = "load",
    browser_viewport_width: int = 1280,
    browser_viewport_height: int = 720,
    browser_block_heavy_assets: bool = False,
    browser_settle_seconds: float = 0.0,
    browser_scroll_passes: int = 0,
    browser_load_more_selector: str | None = None,
    browser_load_more_clicks: int = 0,
    browser_scroll_step_px: int = 0,
    old_reddit_submission_min_datetime: str | None = None,
    old_reddit_submission_max_datetime: str | None = None,
) -> ScreeningReadResult:
    """One orchestrator-invoked, screen-light source read.

    This entry returns status/bytes/content-class/extracted fields only. It
    deliberately has no CLI, no scheduler, no packet runner import, no packet
    staging call, no manifest write, and no ECR import.
    """
    normalized_route = ScreeningReadRoute(route)
    dispatch_refusal = _validate_dispatch(dispatch, requested_url=url, route=normalized_route.value)
    if dispatch_refusal is not None:
        return dispatch_refusal

    if normalized_route is ScreeningReadRoute.REDDIT_SCREENING_READ:
        reddit_result = reddit_screening_read(
            url=url,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
            old_reddit_submission_min_datetime=old_reddit_submission_min_datetime,
            old_reddit_submission_max_datetime=old_reddit_submission_max_datetime,
        )
        return _record_from_reddit_result(
            requested_url=url,
            route=normalized_route.value,
            result=reddit_result,
        )

    gate_refusal = _public_url_gate(url, route=normalized_route.value)
    if gate_refusal is not None:
        return gate_refusal

    if normalized_route is ScreeningReadRoute.BROWSER:
        from source_capture.screening_browser_read import screening_browser_read as browser_screening_read

        browser_result = browser_screening_read(
            url=url,
            dispatch=dispatch,
            timeout_seconds=timeout_seconds,
            wait_until=browser_wait_until,
            viewport_width=browser_viewport_width,
            viewport_height=browser_viewport_height,
            max_artifact_bytes=max_bytes,
            block_heavy_assets=browser_block_heavy_assets,
            settle_seconds=browser_settle_seconds,
            scroll_passes=browser_scroll_passes,
            load_more_selector=browser_load_more_selector,
            load_more_clicks=browser_load_more_clicks,
            scroll_step_px=browser_scroll_step_px,
        )
        return _record_from_browser_result(
            requested_url=url,
            route=normalized_route.value,
            result=browser_result,
        )


    if normalized_route is ScreeningReadRoute.DIRECT_HTTP:
        fetch_result = fetch_direct_http_capture(
            url=url,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
        )
        return _record_from_direct_http_result(
            requested_url=url,
            route=normalized_route.value,
            result=fetch_result,
            old_reddit_submission_min_datetime=old_reddit_submission_min_datetime,
            old_reddit_submission_max_datetime=old_reddit_submission_max_datetime,
        )

    fetch_result = fetch_anti_blocking_http_capture(
        url=url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
    )
    return _record_from_antiblock_result(
        requested_url=url,
        route=normalized_route.value,
        result=fetch_result,
        old_reddit_submission_min_datetime=old_reddit_submission_min_datetime,
        old_reddit_submission_max_datetime=old_reddit_submission_max_datetime,
    )


def close_old_reddit_search_surface_receipt(
    *,
    dispatch: ScreeningReadDispatch,
    subreddit: str = OLD_REDDIT_FIRST_ACT_SUBREDDIT,
    query: str = OLD_REDDIT_FIRST_ACT_QUERY,
    timeout_seconds: float = 20.0,
    max_bytes: int = 500_000,
) -> ScreeningReadResult:
    """First-act receipt helper for the route-decision residual."""
    url = (
        f"https://old.reddit.com/r/{subreddit}/search"
        f"?q={quote_plus(query)}&restrict_sr=on&sort=new"
    )
    return screening_read(
        url=url,
        route=ScreeningReadRoute.REDDIT_SCREENING_READ,
        dispatch=dispatch,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
    )


def _record_from_reddit_result(
    *,
    requested_url: str,
    route: str,
    result: RedditScreenLight | RedditScreeningReadRefused,
) -> ScreeningReadResult:
    if isinstance(result, RedditScreeningReadRefused):
        return ScreeningReadRefused(
            requested_url=requested_url,
            route=route,
            reason=result.reason,
            message=result.message,
        )
    extracted_fields = dict(result.extracted_fields)
    extracted_fields.setdefault("comments_marker_count", result.comments_marker_count)
    extracted_fields.setdefault("rate_ceiling_note", RATE_CEILING_NOTE)
    return ScreeningReadRecord(
        requested_url=requested_url,
        final_url=result.final_url,
        route=route,
        status=result.status,
        byte_count=result.byte_count,
        content_class=result.content_class,
        content_signal=result.content_signal,
        content_class_detail=result.content_class_detail,
        extracted_fields=extracted_fields,
        limitation_notes=list(result.limitation_notes),
    )


def _record_from_direct_http_result(
    *,
    requested_url: str,
    route: str,
    result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure,
    old_reddit_submission_min_datetime: str | None,
    old_reddit_submission_max_datetime: str | None,
) -> ScreeningReadResult:
    if isinstance(result, DirectHttpCaptureFailure):
        return ScreeningReadRefused(
            requested_url=requested_url,
            route=route,
            reason="fetch_failed",
            message=result.message,
        )
    body_text = result.body.decode("utf-8", errors="replace")
    login_refusal = _post_fetch_login_gate(
        requested_url=requested_url,
        final_url=result.final_url,
        body_text=body_text,
        route=route,
    )
    if login_refusal is not None:
        return login_refusal
    classification = classify_capture_body(
        status=result.status,
        headers=_headers_from_direct_metadata(result),
        body=result.body,
    )
    return ScreeningReadRecord(
        requested_url=requested_url,
        final_url=result.final_url,
        route=route,
        status=result.status,
        byte_count=int(result.metadata["byte_count"]),
        content_class=classification.classification.value,
        content_signal=classification.signal,
        content_class_detail=classification.detail,
        extracted_fields=extract_screening_fields(
            url=result.final_url,
            body_text=body_text,
            old_reddit_submission_min_datetime=old_reddit_submission_min_datetime,
            old_reddit_submission_max_datetime=old_reddit_submission_max_datetime,
        ),
        content_type=_metadata_str(result.metadata.get("content_type")),
        warning_notes=list(result.warning_notes),
        limitation_notes=list(result.limitation_notes),
    )


def _record_from_antiblock_result(
    *,
    requested_url: str,
    route: str,
    result: AntiBlockingHttpCaptureSuccess | AntiBlockingHttpCaptureFailure,
    old_reddit_submission_min_datetime: str | None,
    old_reddit_submission_max_datetime: str | None,
) -> ScreeningReadResult:
    if isinstance(result, AntiBlockingHttpCaptureFailure):
        return ScreeningReadRefused(
            requested_url=requested_url,
            route=route,
            reason="fetch_failed",
            message=result.message,
        )
    body_text = result.body.decode("utf-8", errors="replace")
    login_refusal = _post_fetch_login_gate(
        requested_url=requested_url,
        final_url=result.final_url,
        body_text=body_text,
        route=route,
    )
    if login_refusal is not None:
        return login_refusal
    classification = classify_capture_body(
        status=result.status,
        headers=result.response_headers,
        body=result.body,
    )
    return ScreeningReadRecord(
        requested_url=requested_url,
        final_url=result.final_url,
        route=route,
        status=result.status,
        byte_count=int(result.metadata["byte_count"]),
        content_class=classification.classification.value,
        content_signal=classification.signal,
        content_class_detail=classification.detail,
        extracted_fields=extract_screening_fields(
            url=result.final_url,
            body_text=body_text,
            old_reddit_submission_min_datetime=old_reddit_submission_min_datetime,
            old_reddit_submission_max_datetime=old_reddit_submission_max_datetime,
        ),
        content_type=_metadata_str(result.metadata.get("content_type")),
        warning_notes=list(result.warning_notes),
        limitation_notes=list(result.limitation_notes),
    )


def _record_from_browser_result(
    *,
    requested_url: str,
    route: str,
    result: object,
) -> ScreeningReadResult:
    from source_capture.screening_browser_read import BrowserScreeningReadRefused

    if isinstance(result, BrowserScreeningReadRefused):
        return ScreeningReadRefused(
            requested_url=requested_url,
            route=route,
            reason=result.reason,
            message=result.message,
        )
    return ScreeningReadRecord(
        requested_url=requested_url,
        final_url=result.final_url,
        route=route,
        status=None,
        byte_count=result.visible_text_byte_count,
        content_class=result.content_class,
        content_signal=result.content_signal,
        content_class_detail=result.content_class_detail,
        extracted_fields={
            "title": result.title,
            "visible_text": result.visible_text,
            "access_block_reason": result.access_block_reason,
            "status_note": result.status_note,
        },
        warning_notes=list(result.warning_notes),
        limitation_notes=list(result.limitation_notes),
    )


def _validate_dispatch(
    dispatch: ScreeningReadDispatch,
    *,
    requested_url: str,
    route: str,
) -> ScreeningReadRefused | None:
    if dispatch.invoked_by != "screen_orchestrator":
        return ScreeningReadRefused(
            requested_url=requested_url,
            route=route,
            reason="not_orchestrator_invoked",
            message="screening reads must be invoked by the screen orchestrator, not walkers directly",
        )
    if not dispatch.screen_id.strip() or not dispatch.question.strip():
        return ScreeningReadRefused(
            requested_url=requested_url,
            route=route,
            reason="unbounded_dispatch",
            message="screening reads require a per-screen id and one bounded question",
        )
    return None


def _public_url_gate(url: str, *, route: str) -> ScreeningReadRefused | None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ScreeningReadRefused(
            requested_url=url,
            route=route,
            reason="entitlement_gated",
            message="screening reads require an absolute public http:// or https:// URL",
        )
    if parsed.username is not None or parsed.password is not None:
        return ScreeningReadRefused(
            requested_url=url,
            route=route,
            reason="entitlement_gated",
            message="URLs with embedded credentials are not public logged-out screening surfaces",
        )
    host = (parsed.hostname or "").lower()
    if host in {"localhost"} or host.endswith(".local") or _is_non_public_ip_literal(host):
        return ScreeningReadRefused(
            requested_url=url,
            route=route,
            reason="entitlement_gated",
            message=f"host {host!r} is not a public logged-out screening surface",
        )
    path_segments = {segment.lower() for segment in (parsed.path or "").split("/") if segment}
    if path_segments & {"login", "signin", "sign-in", "register", "account", "accounts", "oauth", "auth"}:
        return ScreeningReadRefused(
            requested_url=url,
            route=route,
            reason="entitlement_gated",
            message="URL path looks like an auth/account surface; refused before fetch",
        )
    return None


def _post_fetch_login_gate(
    *,
    requested_url: str,
    final_url: str,
    body_text: str,
    route: str,
) -> ScreeningReadRefused | None:
    final_lower = final_url.lower()
    if any(marker in final_lower for marker in ("/login", "/signin", "/register", "/account")):
        return ScreeningReadRefused(
            requested_url=requested_url,
            route=route,
            reason="login_redirect",
            message=f"screening read landed on an auth/account URL: {final_url!r}",
        )
    body_lower = body_text.lower()
    if any(
        marker in body_lower
        for marker in (
            'action="/login"',
            'action="/signin"',
            "please log in",
            "please sign in",
            "log in to continue",
            "sign in to continue",
        )
    ):
        return ScreeningReadRefused(
            requested_url=requested_url,
            route=route,
            reason="login_redirect",
            message="screening read received a login/sign-in page; content is access-gated",
        )
    return None


def _headers_from_direct_metadata(result: DirectHttpCaptureSuccess) -> dict[str, str]:
    headers: dict[str, str] = {}
    content_type = _metadata_str(result.metadata.get("content_type"))
    if content_type:
        headers["Content-Type"] = content_type
    content_encoding = _metadata_str(result.metadata.get("content_encoding"))
    if content_encoding:
        headers["Content-Encoding"] = content_encoding
    return headers


def _is_non_public_ip_literal(host: str) -> bool:
    try:
        parsed = ip_address(host)
    except ValueError:
        return False
    return (
        parsed.is_private
        or parsed.is_loopback
        or parsed.is_link_local
        or parsed.is_multicast
        or parsed.is_reserved
        or parsed.is_unspecified
    )


def _metadata_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)


__all__ = [
    "HUMAN_RATE_NOTE",
    "OLD_REDDIT_FIRST_ACT_QUERY",
    "OLD_REDDIT_FIRST_ACT_SUBREDDIT",
    "ScreeningReadDispatch",
    "ScreeningReadRecord",
    "ScreeningReadRefused",
    "ScreeningReadResult",
    "ScreeningReadRoute",
    "close_old_reddit_search_surface_receipt",
    "screening_read",
]
