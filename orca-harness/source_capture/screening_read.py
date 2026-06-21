from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from typing import TypeAlias
from urllib.parse import urljoin, urlparse

from source_capture.adapters.anti_blocking_http import (
    AntiBlockingHttpCaptureFailure,
    fetch_anti_blocking_http_capture,
)
from source_capture.adapters.direct_http import DirectHttpCaptureFailure, fetch_direct_http_capture
from source_capture.block_shell import CaptureBodyClass, classify_capture_body
from source_capture.reddit_consolidation.html_dom import HtmlNode, parse_html_document
from source_capture.screening_browser_read import (
    SCREENING_ORCHESTRATOR_CONTEXT,
    ScreeningBrowserRead,
    ScreeningBrowserReadRefused,
    screening_browser_read,
)
from source_capture.screening_reddit_read import (
    RATE_CEILING_NOTE,
    _post_fetch_entitlement_gate,
    _pre_fetch_entitlement_gate,
)


class ScreeningReadRoute(StrEnum):
    REDDIT_OLD_SEARCH = "reddit_old_search"
    DIRECT_HTTP = "direct_http"
    ANTI_BLOCKING_HTTP = "anti_blocking_http"
    BROWSER = "screening_browser_read"


@dataclass(frozen=True)
class ScreeningReadRecord:
    """Screen-light record: status/bytes/classification/extracts only; no packet/ECR."""

    route: str
    requested_url: str
    final_url: str
    status: int | None
    byte_count: int
    content_class: str
    content_signal: str | None
    content_detail: str
    extracted_fields: dict[str, object] = field(default_factory=dict)
    warning_notes: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class ScreeningReadRefused:
    route: str
    requested_url: str
    reason: str
    message: str


ScreeningReadResult: TypeAlias = ScreeningReadRecord | ScreeningReadRefused


def screening_read(
    *,
    url: str,
    route: ScreeningReadRoute | str,
    invocation_context: str,
    timeout_seconds: float = 20.0,
    max_bytes: int = 2_000_000,
    browser_settle_seconds: float = 0.0,
    browser_scroll_passes: int = 0,
    browser_scroll_step_px: int = 0,
) -> ScreeningReadResult:
    """Orchestrator-only screening read over existing source-capture adapters.

    The service is deliberately not a crawler, scheduler, packet writer, or ECR
    writer. It executes one supplied URL through one supplied route and returns
    a screen-light record for the screen orchestrator.
    """
    if invocation_context != SCREENING_ORCHESTRATOR_CONTEXT:
        return ScreeningReadRefused(
            route=str(route),
            requested_url=url,
            reason="not_orchestrator_invoked",
            message="screening_read is orchestrator-invoked only; walker-direct calls are refused",
        )
    try:
        selected_route = ScreeningReadRoute(route)
    except ValueError:
        return ScreeningReadRefused(
            route=str(route),
            requested_url=url,
            reason="unsupported_route",
            message=f"unsupported screening read route: {route!r}",
        )

    if selected_route == ScreeningReadRoute.REDDIT_OLD_SEARCH:
        return _screening_reddit_old_search_read(
            url=url,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
        )
    if selected_route == ScreeningReadRoute.DIRECT_HTTP:
        return _screening_direct_http_read(
            url=url,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
        )
    if selected_route == ScreeningReadRoute.ANTI_BLOCKING_HTTP:
        return _screening_anti_blocking_http_read(
            url=url,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
        )
    if selected_route == ScreeningReadRoute.BROWSER:
        return _screening_browser_route_read(
            url=url,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
            settle_seconds=browser_settle_seconds,
            scroll_passes=browser_scroll_passes,
            scroll_step_px=browser_scroll_step_px,
        )
    raise AssertionError(f"unhandled screening read route: {selected_route}")


def _screening_reddit_old_search_read(
    *, url: str, timeout_seconds: float, max_bytes: int
) -> ScreeningReadResult:
    pre_gate = _pre_fetch_entitlement_gate(url)
    if pre_gate is not None:
        return ScreeningReadRefused(
            route=ScreeningReadRoute.REDDIT_OLD_SEARCH.value,
            requested_url=url,
            reason=pre_gate.reason,
            message=pre_gate.message,
        )
    result = fetch_direct_http_capture(
        url=url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
    )
    if isinstance(result, DirectHttpCaptureFailure):
        return ScreeningReadRefused(
            route=ScreeningReadRoute.REDDIT_OLD_SEARCH.value,
            requested_url=url,
            reason="fetch_failed",
            message=result.message,
        )
    body_text = result.body.decode("utf-8", errors="replace")
    post_gate = _post_fetch_entitlement_gate(url, result, body_text=body_text)
    if post_gate is not None:
        return ScreeningReadRefused(
            route=ScreeningReadRoute.REDDIT_OLD_SEARCH.value,
            requested_url=url,
            reason=post_gate.reason,
            message=post_gate.message,
        )
    body_class = classify_capture_body(status=result.status, headers={}, body=result.body)
    extracted_fields = extract_old_reddit_listing_fields(
        html=body_text,
        base_url=result.final_url,
    )
    extracted_fields["rate_ceiling_note"] = RATE_CEILING_NOTE
    return _http_record(
        route=ScreeningReadRoute.REDDIT_OLD_SEARCH.value,
        requested_url=result.requested_url,
        final_url=result.final_url,
        status=result.status,
        body=result.body,
        body_class=body_class,
        extracted_fields=extracted_fields,
        warning_notes=result.warning_notes,
        limitation_notes=result.limitation_notes,
        metadata={
            "first_act_old_reddit_receipt": True,
            "comments_marker_count": body_text.count("/comments/"),
            "packet_written": False,
            "ecr_touched": False,
        },
    )


def _screening_direct_http_read(
    *, url: str, timeout_seconds: float, max_bytes: int
) -> ScreeningReadResult:
    pre_gate = _public_url_gate(
        route=ScreeningReadRoute.DIRECT_HTTP.value,
        url=url,
    )
    if pre_gate is not None:
        return pre_gate
    result = fetch_direct_http_capture(
        url=url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
    )
    if isinstance(result, DirectHttpCaptureFailure):
        return ScreeningReadRefused(
            route=ScreeningReadRoute.DIRECT_HTTP.value,
            requested_url=url,
            reason="fetch_failed",
            message=result.message,
        )
    body_class = classify_capture_body(status=result.status, headers={}, body=result.body)
    return _http_record(
        route=ScreeningReadRoute.DIRECT_HTTP.value,
        requested_url=result.requested_url,
        final_url=result.final_url,
        status=result.status,
        body=result.body,
        body_class=body_class,
        extracted_fields={},
        warning_notes=result.warning_notes,
        limitation_notes=result.limitation_notes,
        metadata={"packet_written": False, "ecr_touched": False},
    )


def _screening_anti_blocking_http_read(
    *, url: str, timeout_seconds: float, max_bytes: int
) -> ScreeningReadResult:
    pre_gate = _public_url_gate(
        route=ScreeningReadRoute.ANTI_BLOCKING_HTTP.value,
        url=url,
    )
    if pre_gate is not None:
        return pre_gate
    result = fetch_anti_blocking_http_capture(
        url=url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
    )
    if isinstance(result, AntiBlockingHttpCaptureFailure):
        return ScreeningReadRefused(
            route=ScreeningReadRoute.ANTI_BLOCKING_HTTP.value,
            requested_url=url,
            reason="fetch_failed",
            message=result.message,
        )
    body_class = classify_capture_body(
        status=result.status,
        headers=result.response_headers,
        body=result.body,
    )
    return _http_record(
        route=ScreeningReadRoute.ANTI_BLOCKING_HTTP.value,
        requested_url=result.requested_url,
        final_url=result.final_url,
        status=result.status,
        body=result.body,
        body_class=body_class,
        extracted_fields={},
        warning_notes=result.warning_notes,
        limitation_notes=result.limitation_notes,
        metadata={
            "method_category": result.method_category,
            "impersonation_profile": result.impersonation_profile,
            "packet_written": False,
            "ecr_touched": False,
        },
    )


def _screening_browser_route_read(
    *,
    url: str,
    timeout_seconds: float,
    max_bytes: int,
    settle_seconds: float,
    scroll_passes: int,
    scroll_step_px: int,
) -> ScreeningReadResult:
    result = screening_browser_read(
        url=url,
        invocation_context=SCREENING_ORCHESTRATOR_CONTEXT,
        timeout_seconds=timeout_seconds,
        max_artifact_bytes=max_bytes,
        settle_seconds=settle_seconds,
        scroll_passes=scroll_passes,
        scroll_step_px=scroll_step_px,
    )
    if isinstance(result, ScreeningBrowserReadRefused):
        return ScreeningReadRefused(
            route=ScreeningReadRoute.BROWSER.value,
            requested_url=url,
            reason=result.reason,
            message=result.message,
        )
    assert isinstance(result, ScreeningBrowserRead)
    return ScreeningReadRecord(
        route=ScreeningReadRoute.BROWSER.value,
        requested_url=result.requested_url,
        final_url=result.final_url,
        status=None,
        byte_count=result.byte_count,
        content_class=result.content_class,
        content_signal=result.content_signal,
        content_detail=result.content_detail,
        extracted_fields={},
        warning_notes=result.warning_notes,
        limitation_notes=result.limitation_notes,
        metadata=dict(result.metadata),
    )


def extract_old_reddit_listing_fields(*, html: str, base_url: str) -> dict[str, object]:
    """Extract old-Reddit listing/search fields using title-row-local locators.

    Post dates are read only from the same listing row as the candidate title.
    The extractor never computes a global min() over page datetimes, because
    sidebars can carry unrelated subreddit-age timestamps.
    """
    root = parse_html_document(html)
    rows: list[dict[str, object]] = []
    for anchor in _title_anchors(root):
        row = _nearest_thing(anchor)
        if row is None:
            continue
        href = anchor.attrs.get("href", "")
        time_node = row.first_descendant(tag="time")
        date_value = time_node.attrs.get("datetime") if time_node is not None else None
        date_status, date_detail = _post_date_sanity(date_value)
        rows.append(
            {
                "title": anchor.text_content(),
                "url": urljoin(base_url, href),
                "post_date": date_value if date_status == "range_sane" else None,
                "post_date_status": date_status,
                "post_date_detail": date_detail,
            }
        )
    comments_marker_count = html.count("/comments/")
    return {
        "comments_marker_count": comments_marker_count,
        "candidate_count": len(rows),
        "candidate_rows": rows,
        "extraction_method": "old_reddit_title_row_local_locators",
        "range_sanity_guard": "reddit_launch_to_now_plus_one_day",
    }


def _http_record(
    *,
    route: str,
    requested_url: str,
    final_url: str,
    status: int,
    body: bytes,
    body_class,
    extracted_fields: dict[str, object],
    warning_notes: list[str],
    limitation_notes: list[str],
    metadata: dict[str, object],
) -> ScreeningReadRecord:
    notes = list(limitation_notes)
    if body_class.classification == CaptureBodyClass.BLOCK_SHELL:
        notes.append(
            f"access_failed: {route} body classified as block_shell; signal={body_class.signal}"
        )
    return ScreeningReadRecord(
        route=route,
        requested_url=requested_url,
        final_url=final_url,
        status=status,
        byte_count=len(body),
        content_class=body_class.classification.value,
        content_signal=body_class.signal,
        content_detail=body_class.detail,
        extracted_fields=extracted_fields,
        warning_notes=list(warning_notes),
        limitation_notes=notes,
        metadata=metadata,
    )


def _public_url_gate(*, route: str, url: str) -> ScreeningReadRefused | None:
    try:
        parsed = urlparse(url)
    except Exception as exc:
        return ScreeningReadRefused(
            route=route,
            requested_url=url,
            reason="entitlement_gated",
            message=f"URL could not be parsed ({exc!r}); refusing without fetch.",
        )
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ScreeningReadRefused(
            route=route,
            requested_url=url,
            reason="entitlement_gated",
            message="screening read requires an absolute http:// or https:// URL",
        )
    if parsed.username is not None or parsed.password is not None:
        return ScreeningReadRefused(
            route=route,
            requested_url=url,
            reason="entitlement_gated",
            message="credential-bearing URLs are refused without fetch",
        )
    return None


def _title_anchors(root: HtmlNode) -> list[HtmlNode]:
    anchors: list[HtmlNode] = []
    for node in root.descendants():
        if node.tag != "a":
            continue
        classes = node.classes()
        href = node.attrs.get("href", "")
        if "may-blank" not in classes or "/comments/" not in href:
            continue
        if "search-title" in classes or "title" in classes:
            anchors.append(node)
    return anchors


def _nearest_thing(node: HtmlNode) -> HtmlNode | None:
    current = node.parent
    while current is not None:
        if "thing" in current.classes():
            return current
        current = current.parent
    return None


def _post_date_sanity(value: str | None) -> tuple[str, str]:
    if not value:
        return "absent", "no time datetime attribute found in the title row"
    parsed = _parse_datetime(value)
    if parsed is None:
        return "invalid", f"could not parse title-row datetime {value!r}"
    reddit_launch = datetime(2005, 6, 23, tzinfo=timezone.utc)
    upper = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(days=1)
    if parsed < reddit_launch or parsed > upper:
        return "out_of_range", f"title-row datetime {value!r} is outside Reddit launch..now+1d"
    return "range_sane", "title-row datetime is inside Reddit launch..now+1d"


def _parse_datetime(value: str) -> datetime | None:
    text = value.strip()
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)
