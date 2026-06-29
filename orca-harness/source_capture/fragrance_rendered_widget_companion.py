from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any, Callable, Iterable, Literal, Mapping, Sequence
from urllib.parse import urlparse

from pydantic import Field

from schemas.case_models import StrictModel
from source_capture.adapters.browser_snapshot import (
    BrowserPageObservationSuccess,
    BrowserPageResponse,
    BrowserSnapshotFailure,
    fetch_browser_page_observation_capture,
)
from source_capture.fragrance_review_coverage import (
    FragranceReviewCoverageInputError,
    FragranceReviewCoverageReceipt,
    build_fragrance_review_coverage,
)

FRAGRANCE_RENDERED_WIDGET_COMPANION_METHOD = "fragrance_rendered_widget_companion"
FRAGRANCE_RENDERED_WIDGET_COMPANION_VERSION = "v0"
FRAGRANCE_RENDERED_WIDGET_COMPANION_CERTIFICATION = (
    "rendered_widget_companion; passive_first_bounded_fallback; not_judgment_ready"
)

_DOM_EXTRACT_SCRIPT = """
() => {
  const vw = window.innerWidth;
  const vh = window.innerHeight;
  const seen = [];
  const used = new Set();
  const candidates = Array.from(document.querySelectorAll('body *'));
  for (const el of candidates) {
    const rect = el.getBoundingClientRect();
    if (rect.width < 2 || rect.height < 2) continue;
    if (rect.bottom <= 0 || rect.top >= vh || rect.right <= 0 || rect.left >= vw) continue;
    const style = window.getComputedStyle(el);
    if (style.visibility === 'hidden' || style.display === 'none' || Number(style.opacity || 1) === 0) continue;
    const text = (el.innerText || el.getAttribute('aria-label') || el.getAttribute('alt') || '').replace(/\s+/g, ' ').trim();
    if (!text) continue;
    if (text.length > 220) continue;
    const key = `${Math.round(rect.top)}|${Math.round(rect.left)}|${text}`;
    if (used.has(key)) continue;
    used.add(key);
    seen.push({
      tag: el.tagName.toLowerCase(),
      text,
      top: Math.round(rect.top),
      left: Math.round(rect.left),
      width: Math.round(rect.width),
      height: Math.round(rect.height),
    });
  }
  seen.sort((a, b) => a.top - b.top || a.left - b.left);
  const jsonLdTexts = Array.from(document.querySelectorAll('script[type="application/ld+json"]'))
    .map((node) => node.textContent || '')
    .filter((text) => text.trim().length > 0);
  return {
    title: document.title,
    url: location.href,
    viewport: {width: vw, height: vh},
    scroll_y: window.scrollY,
    items: seen.slice(0, 160),
    json_ld_texts: jsonLdTexts,
  };
}
"""

_REVIEW_RESPONSE_KINDS = frozenset({"judgeme_reviews_for_widget", "yotpo_v3_reviews"})


class FragranceRenderedWidgetCompanionInputError(ValueError):
    """A rendered+widget companion input cannot be normalized honestly."""


class FragranceAboveFoldCompanion(StrictModel):
    viewport_width: int = Field(ge=1)
    viewport_height: int = Field(ge=1)
    title: str | None = None
    final_url: str
    visible_text_sha256: str | None = None
    visible_text_byte_count: int = Field(ge=0)
    item_count: int = Field(ge=0)
    items: list[dict[str, Any | None]] = Field(default_factory=list)
    rating_or_review_count_visible: bool = False
    review_section_visible: bool = False
    price_visible: bool = False
    cta_visible: bool = False
    stock_or_pickup_visible: bool = False
    size_or_variant_visible: bool = False
    residuals: list[str] = Field(default_factory=list)


class FragranceWidgetResponseCapture(StrictModel):
    response_index: int = Field(ge=1)
    response_origin: Literal["render_passive", "bounded_fallback"]
    response_kind: Literal[
        "judgeme_reviews_for_widget",
        "yotpo_v3_reviews",
        "yotpo_v3_ratings",
        "yotpo_v3_reviews_media",
        "unknown_widget_response",
    ]
    requested_url: str
    final_url: str
    status: int
    ok: bool
    body_sha256: str | None = None
    body_byte_count: int = Field(ge=0)
    body_text: str | None = None
    response_headers: dict[str, str] = Field(default_factory=dict)
    limitation_notes: list[str] = Field(default_factory=list)


class FragranceRenderedWidgetCompanionReceipt(StrictModel):
    companion_method: Literal["fragrance_rendered_widget_companion"] = FRAGRANCE_RENDERED_WIDGET_COMPANION_METHOD
    companion_version: Literal["v0"] = FRAGRANCE_RENDERED_WIDGET_COMPANION_VERSION
    certification: Literal[
        "rendered_widget_companion; passive_first_bounded_fallback; not_judgment_ready"
    ] = FRAGRANCE_RENDERED_WIDGET_COMPANION_CERTIFICATION
    source_id: str
    source_site: str
    product_url: str
    widget_route: dict[str, Any | None] = Field(default_factory=dict)
    rendered_companion: FragranceAboveFoldCompanion
    widget_responses: list[FragranceWidgetResponseCapture] = Field(default_factory=list)
    focused_review_coverage: FragranceReviewCoverageReceipt | None = None
    fallback_needed: bool = False
    route_health: list[str] = Field(default_factory=list)
    residuals: list[str] = Field(default_factory=list)
    warning_notes: list[str] = Field(default_factory=list)
    limitation_notes: list[str] = Field(default_factory=list)
    non_claims: list[str] = Field(
        default_factory=lambda: [
            "not one literal HTTP request",
            "not source-wide review coverage",
            "not proof that below-fold widgets fired",
            "not durable Attachment Records",
            "not ECR, Cleaning, Judgment, pain/pleasure labeling, or review-integrity scoring",
        ]
    )


def capture_fragrance_rendered_widget_companion(
    *,
    url: str,
    source_id: str,
    source_site: str,
    product_url: str | None = None,
    widget_route: Mapping[str, Any | None] | None = None,
    as_of_date: date | None = None,
    max_selected_rows: int | None = None,
    source_media_filter_count: int | None = None,
    timeout_seconds: float = 45.0,
    wait_until: str = "load",
    viewport_width: int = 1365,
    viewport_height: int = 900,
    max_response_bytes: int = 5_000_000,
    settle_seconds: float = 3.0,
    selector: str | None = None,
    selector_timeout_seconds: float = 5.0,
    block_heavy_assets: bool = False,
    headless: bool = True,
    browser_channel: str | None = None,
    observation_fetcher: Callable[..., BrowserPageObservationSuccess | BrowserSnapshotFailure] = fetch_browser_page_observation_capture,
    fallback_widget_urls: Sequence[str] = (),
    fallback_fetcher: Callable[..., Sequence[BrowserPageResponse]] | None = None,
) -> FragranceRenderedWidgetCompanionReceipt:
    observation = observation_fetcher(
        url=url,
        dom_extract_script=_DOM_EXTRACT_SCRIPT,
        dom_extract_arg={},
        response_url_predicate=is_fragrance_widget_response_url,
        timeout_seconds=timeout_seconds,
        wait_until=wait_until,
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        max_response_bytes=max_response_bytes,
        settle_seconds=settle_seconds,
        selector=selector,
        selector_timeout_seconds=selector_timeout_seconds,
        block_resource_types=("image", "media", "font") if block_heavy_assets else (),
        headless=headless,
        browser_channel=browser_channel,
    )
    if isinstance(observation, BrowserSnapshotFailure):
        raise FragranceRenderedWidgetCompanionInputError(
            f"rendered widget companion capture failed: {observation.failure_kind.value}: {observation.message}"
        )

    initial_receipt = build_fragrance_rendered_widget_companion_from_observation(
        observation,
        source_id=source_id,
        source_site=source_site,
        product_url=product_url or url,
        widget_route=widget_route,
        as_of_date=as_of_date,
        max_selected_rows=max_selected_rows,
        source_media_filter_count=source_media_filter_count,
    )
    if not initial_receipt.fallback_needed or not fallback_widget_urls:
        return initial_receipt

    fetcher = fallback_fetcher or fetch_fragrance_widget_fallback_responses
    fallback_responses = list(
        fetcher(
            urls=fallback_widget_urls,
            timeout_seconds=timeout_seconds,
            max_response_bytes=max_response_bytes,
        )
    )
    return build_fragrance_rendered_widget_companion_from_observation(
        observation,
        source_id=source_id,
        source_site=source_site,
        product_url=product_url or url,
        widget_route=widget_route,
        as_of_date=as_of_date,
        max_selected_rows=max_selected_rows,
        source_media_filter_count=source_media_filter_count,
        fallback_responses=fallback_responses,
    )


def write_fragrance_rendered_widget_companion(
    *,
    output_path: Path,
    **kwargs: Any,
) -> FragranceRenderedWidgetCompanionReceipt:
    receipt = capture_fragrance_rendered_widget_companion(**kwargs)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        f"{json.dumps(receipt.model_dump(mode='json'), indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )
    return receipt


def build_fragrance_rendered_widget_companion_from_observation(
    observation: BrowserPageObservationSuccess,
    *,
    source_id: str,
    source_site: str,
    product_url: str,
    widget_route: Mapping[str, Any | None] | None = None,
    as_of_date: date | None = None,
    max_selected_rows: int | None = None,
    source_media_filter_count: int | None = None,
    fallback_responses: Sequence[BrowserPageResponse] = (),
) -> FragranceRenderedWidgetCompanionReceipt:
    residuals: list[str] = []
    route_health: list[str] = ["rendered_page_observation_present"]
    rendered = _rendered_companion_from_observation(observation)
    if rendered.item_count:
        route_health.append("above_fold_geometry_present")
    else:
        residuals.append("above_fold_geometry_absent")

    passive_responses = _widget_response_captures(observation.responses, response_origin="render_passive")
    fallback_response_captures = _widget_response_captures(
        fallback_responses,
        response_origin="bounded_fallback",
        starting_index=len(passive_responses) + 1,
    )
    widget_responses = passive_responses + fallback_response_captures
    route_health.append(f"passive_widget_response_count:{len(passive_responses)}")
    if fallback_response_captures:
        route_health.append(f"bounded_fallback_widget_response_count:{len(fallback_response_captures)}")
    elif fallback_responses:
        residuals.append("bounded_fallback_widget_responses_unrecognized")
    if not passive_responses:
        residuals.append("passive_widget_not_observed_during_render")

    review_response_bodies = [
        response.body_text
        for response in widget_responses
        if response.response_kind in _REVIEW_RESPONSE_KINDS and response.body_text
    ]
    focused_review_coverage: FragranceReviewCoverageReceipt | None = None
    pdp_html = _pdp_html_from_dom_observation(observation.dom_observation)
    if review_response_bodies:
        try:
            focused_review_coverage = build_fragrance_review_coverage(
                widget_responses=review_response_bodies,
                pdp_html=pdp_html,
                source_id=source_id,
                source_site=source_site,
                product_url=product_url,
                widget_route=widget_route,
                as_of_date=as_of_date,
                max_selected_rows=max_selected_rows,
                source_media_filter_count=source_media_filter_count,
            )
        except FragranceReviewCoverageInputError as exc:
            residuals.append(f"widget_review_coverage_parse_failed:{exc}")
        else:
            route_health.append("focused_review_coverage_built_from_widget_responses")
            if focused_review_coverage.coverage_summary.total_rows == 0:
                residuals.append("widget_responses_did_not_yield_review_rows")
    else:
        residuals.append("widget_review_responses_absent")

    fallback_needed = _fallback_needed(focused_review_coverage)
    if fallback_needed:
        residuals.append("bounded_direct_widget_fallback_needed_for_row_completion")

    return FragranceRenderedWidgetCompanionReceipt(
        source_id=source_id,
        source_site=source_site,
        product_url=product_url,
        widget_route=dict(widget_route or {}),
        rendered_companion=rendered,
        widget_responses=widget_responses,
        focused_review_coverage=focused_review_coverage,
        fallback_needed=fallback_needed,
        route_health=route_health,
        residuals=_dedup(residuals),
        warning_notes=list(observation.warning_notes),
        limitation_notes=list(observation.limitation_notes),
    )


def is_fragrance_widget_response_url(url: str) -> bool:
    return _widget_response_kind(url) is not None


def fetch_fragrance_widget_fallback_responses(
    *,
    urls: Sequence[str],
    timeout_seconds: float,
    max_response_bytes: int,
) -> list[BrowserPageResponse]:
    if timeout_seconds <= 0:
        raise FragranceRenderedWidgetCompanionInputError("timeout_seconds must be greater than zero")
    if max_response_bytes <= 0:
        raise FragranceRenderedWidgetCompanionInputError("max_response_bytes must be greater than zero")

    responses: list[BrowserPageResponse] = []
    for url in urls:
        _validate_fallback_widget_url(url)
        responses.append(
            _fetch_fallback_widget_response(
                url,
                timeout_seconds=timeout_seconds,
                max_response_bytes=max_response_bytes,
            )
        )
    return responses


def _rendered_companion_from_observation(observation: BrowserPageObservationSuccess) -> FragranceAboveFoldCompanion:
    dom = _dom_mapping(observation.dom_observation)
    viewport = dom.get("viewport") if isinstance(dom.get("viewport"), Mapping) else {}
    items = _normalize_items(dom.get("items"))
    text_blob = "\n".join(str(item.get("text") or "") for item in items)
    visible_text = observation.visible_text or ""
    residuals: list[str] = []
    if not items:
        residuals.append("above_fold_items_absent")
    return FragranceAboveFoldCompanion(
        viewport_width=_int_or_default(viewport.get("width"), int(observation.metadata.get("viewport_width") or 0)),
        viewport_height=_int_or_default(viewport.get("height"), int(observation.metadata.get("viewport_height") or 0)),
        title=observation.title,
        final_url=observation.final_url,
        visible_text_sha256=hashlib.sha256(visible_text.encode("utf-8")).hexdigest() if visible_text else None,
        visible_text_byte_count=len(visible_text.encode("utf-8")),
        item_count=len(items),
        items=items,
        rating_or_review_count_visible=_contains_any(text_blob, ("review", "reviews", "stars")) or _rating_count_pattern(text_blob),
        review_section_visible=_contains_any(text_blob, ("customer review", "customer reviews", "write a review")),
        price_visible=_price_pattern(text_blob),
        cta_visible=_contains_any(text_blob, ("add to cart", "add to bag", "add to basket")),
        stock_or_pickup_visible=_contains_any(text_blob, ("in stock", "availability", "pickup", "online only", "ready in")),
        size_or_variant_visible=_contains_any(text_blob, ("size", "ml", "sample", "traveler")),
        residuals=residuals,
    )


def _widget_response_captures(
    responses: Sequence[BrowserPageResponse],
    *,
    response_origin: Literal["render_passive", "bounded_fallback"],
    starting_index: int = 1,
) -> list[FragranceWidgetResponseCapture]:
    preserved: list[FragranceWidgetResponseCapture] = []
    seen: set[tuple[str, int]] = set()
    for response in responses:
        kind = _widget_response_kind(response.requested_url)
        if kind is None:
            continue
        identity = (response.requested_url, response.status)
        if identity in seen:
            continue
        seen.add(identity)
        body = response.body_text or ""
        preserved.append(
            FragranceWidgetResponseCapture(
                response_index=starting_index + len(preserved),
                response_origin=response_origin,
                response_kind=kind,
                requested_url=response.requested_url,
                final_url=response.final_url,
                status=response.status,
                ok=response.ok,
                body_sha256=hashlib.sha256(body.encode("utf-8")).hexdigest() if body else None,
                body_byte_count=len(body.encode("utf-8")),
                body_text=body or None,
                response_headers=dict(response.response_headers),
                limitation_notes=list(response.limitation_notes),
            )
        )
    return preserved


def _fetch_fallback_widget_response(
    url: str,
    *,
    timeout_seconds: float,
    max_response_bytes: int,
) -> BrowserPageResponse:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (compatible; OrcaSourceCapture/0.1)",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            body_text, limitation_notes = _read_response_body_with_cap(
                response,
                max_response_bytes=max_response_bytes,
            )
            status = int(response.getcode())
            return BrowserPageResponse(
                requested_url=url,
                final_url=str(response.geturl()),
                status=status,
                ok=200 <= status < 400,
                body_text=body_text,
                response_headers=_headers_without_cookies(response.headers.items()),
                limitation_notes=limitation_notes,
            )
    except urllib.error.HTTPError as exc:
        body_text, limitation_notes = _read_response_body_with_cap(
            exc,
            max_response_bytes=max_response_bytes,
        )
        return BrowserPageResponse(
            requested_url=url,
            final_url=str(exc.geturl()),
            status=int(exc.code),
            ok=False,
            body_text=body_text,
            response_headers=_headers_without_cookies(exc.headers.items() if exc.headers else ()),
            limitation_notes=limitation_notes,
        )
    except Exception as exc:
        return BrowserPageResponse(
            requested_url=url,
            final_url=url,
            status=0,
            ok=False,
            body_text="",
            response_headers={},
            limitation_notes=[f"bounded_fallback_fetch_failed:{type(exc).__name__}:{exc}"],
        )


def _read_response_body_with_cap(response: Any, *, max_response_bytes: int) -> tuple[str, list[str]]:
    raw = response.read(max_response_bytes + 1)
    if len(raw) > max_response_bytes:
        return "", [f"bounded_fallback_response_body_exceeded_cap:{len(raw)}>{max_response_bytes}"]
    charset = response.headers.get_content_charset() if response.headers else None
    return raw.decode(charset or "utf-8", errors="replace"), []


def _headers_without_cookies(items: Iterable[tuple[str, str]]) -> dict[str, str]:
    return {
        str(key): str(value)
        for key, value in items
        if str(key).lower() not in {"set-cookie", "cookie"}
    }


def _validate_fallback_widget_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise FragranceRenderedWidgetCompanionInputError(
            "fallback widget URL must be an absolute http:// or https:// URL"
        )
    if parsed.username is not None or parsed.password is not None:
        raise FragranceRenderedWidgetCompanionInputError(
            "fallback widget URL must not include embedded credentials"
        )
    if _widget_response_kind(url) is None:
        raise FragranceRenderedWidgetCompanionInputError(
            f"fallback widget URL is not a supported fragrance widget endpoint: {url}"
        )


def _widget_response_kind(
    url: str,
) -> Literal[
    "judgeme_reviews_for_widget",
    "yotpo_v3_reviews",
    "yotpo_v3_ratings",
    "yotpo_v3_reviews_media",
    "unknown_widget_response",
] | None:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    if host == "api.judge.me" and path == "/reviews/reviews_for_widget":
        return "judgeme_reviews_for_widget"
    if host == "api-cdn.yotpo.com" and "/v3/storefront/" in path:
        if path.endswith("/reviewsmedia") or "/reviewsmedia" in path:
            return "yotpo_v3_reviews_media"
        if path.endswith("/ratings") or "/ratings" in path:
            return "yotpo_v3_ratings"
        if path.endswith("/reviews") or "/reviews" in path:
            return "yotpo_v3_reviews"
        return "unknown_widget_response"
    return None


def _pdp_html_from_dom_observation(dom_observation: object) -> str | None:
    dom = _dom_mapping(dom_observation)
    raw_texts = dom.get("json_ld_texts")
    if not isinstance(raw_texts, list):
        return None
    scripts = [str(text).strip() for text in raw_texts if str(text).strip()]
    if not scripts:
        return None
    return "\n".join(f'<script type="application/ld+json">{script}</script>' for script in scripts)


def _fallback_needed(coverage: FragranceReviewCoverageReceipt | None) -> bool:
    if coverage is None:
        return True
    summary = coverage.coverage_summary
    if summary.total_rows == 0:
        return True
    if summary.widget_total_count is not None and summary.total_rows < summary.widget_total_count:
        return True
    return False


def _dom_mapping(value: object) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise FragranceRenderedWidgetCompanionInputError("DOM observation must be an object")
    return value


def _normalize_items(value: object) -> list[dict[str, Any | None]]:
    if not isinstance(value, list):
        return []
    normalized: list[dict[str, Any | None]] = []
    for raw in value:
        if not isinstance(raw, Mapping):
            continue
        text = str(raw.get("text") or "").strip()
        if not text:
            continue
        normalized.append(
            {
                "tag": str(raw.get("tag") or ""),
                "text": text,
                "top": _int_or_none(raw.get("top")),
                "left": _int_or_none(raw.get("left")),
                "width": _int_or_none(raw.get("width")),
                "height": _int_or_none(raw.get("height")),
            }
        )
    return normalized


def _contains_any(text: str, needles: Sequence[str]) -> bool:
    lowered = text.casefold()
    return any(needle.casefold() in lowered for needle in needles)


def _price_pattern(text: str) -> bool:
    return bool(re.search(r"(?:\$|s\$|usd|sgd|regular price)", text, re.IGNORECASE))


def _rating_count_pattern(text: str) -> bool:
    return bool(re.search(r"\b\d(?:\.\d{1,2})?\s*\(\d+\)", text))


def _int_or_none(value: object) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(float(str(value)))
    except (TypeError, ValueError):
        return None


def _int_or_default(value: object, default: int) -> int:
    parsed = _int_or_none(value)
    return parsed if parsed is not None and parsed > 0 else default


def _dedup(values: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped


__all__ = [
    "FRAGRANCE_RENDERED_WIDGET_COMPANION_CERTIFICATION",
    "FRAGRANCE_RENDERED_WIDGET_COMPANION_METHOD",
    "FRAGRANCE_RENDERED_WIDGET_COMPANION_VERSION",
    "FragranceAboveFoldCompanion",
    "FragranceWidgetResponseCapture",
    "FragranceRenderedWidgetCompanionInputError",
    "FragranceRenderedWidgetCompanionReceipt",
    "build_fragrance_rendered_widget_companion_from_observation",
    "capture_fragrance_rendered_widget_companion",
    "fetch_fragrance_widget_fallback_responses",
    "is_fragrance_widget_response_url",
    "write_fragrance_rendered_widget_companion",
]