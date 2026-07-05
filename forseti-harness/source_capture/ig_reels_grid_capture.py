"""Live browser-adapter capture for IG public creator grid observations.

The parser in ``ig_reels_grid`` stays pure and network-free. This module owns
IG-specific capture policy: one public reels page load, no hover/click/item
fan-out, DOM media-anchor extraction, and passive JSON response preservation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import TypeAlias

from source_capture.adapters.browser_snapshot import (
    BrowserPageResponse,
    BrowserSnapshotFailure,
    fetch_browser_page_observation_capture,
)
from source_capture.ig_reels_grid import (
    CLIPS_USER_JSON_METADATA,
    PROFILE_FEED_JSON_METADATA,
    WEB_PROFILE_INFO_JSON_METADATA,
    source_surface_from_url_or_path,
)
from source_capture.proxy_profiles import ProxyProfile

DEFAULT_IG_REELS_VIEWPORT_WIDTH = 1080
DEFAULT_IG_REELS_VIEWPORT_HEIGHT = 1920
# Widen the post-load settle window so the passive ``clips/user`` XHR (which
# populates per-reel engagement) more reliably lands before the DOM snapshot.
# A short window loses a race against a slow XHR and drops grid rows to the
# honest ``no_passive_json_join_for_shortcode`` gap -- a permanent per-timepoint
# hole in any momentum series. A late XHR is still recorded as a gap, not faked.
DEFAULT_IG_REELS_SETTLE_SECONDS = 4.0
DEFAULT_IG_REELS_TIMEOUT_SECONDS = 25.0
DEFAULT_IG_REELS_MAX_RESPONSE_BYTES = 5_000_000

_PRESERVED_RESPONSE_SURFACES = {
    CLIPS_USER_JSON_METADATA,
    WEB_PROFILE_INFO_JSON_METADATA,
    PROFILE_FEED_JSON_METADATA,
}
_HEAVY_RESOURCE_TYPES = ("font", "image", "media")
_DOM_GRID_SELECTOR = 'a[href*="/reel/"], a[href*="/p/"]'


@dataclass(frozen=True)
class IgReelsGridPassiveResponse:
    source_surface: str
    requested_url: str
    final_url: str
    status: int
    ok: bool
    body_text: str
    response_headers: dict[str, str]
    limitation_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class IgReelsGridCaptureSuccess:
    requested_url: str
    final_url: str
    title: str | None
    visible_text: str
    dom_rows: list[dict[str, object]]
    passive_json_responses: list[IgReelsGridPassiveResponse]
    metadata: dict[str, object]
    warning_notes: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class IgReelsGridCaptureFailure:
    requested_url: str
    failure_kind: str
    message: str
    final_url: str | None = None


IgReelsGridCaptureResult: TypeAlias = IgReelsGridCaptureSuccess | IgReelsGridCaptureFailure


def fetch_ig_reels_grid_capture(
    *,
    reels_url: str,
    profile_handle: str,
    timeout_seconds: float = DEFAULT_IG_REELS_TIMEOUT_SECONDS,
    viewport_width: int = DEFAULT_IG_REELS_VIEWPORT_WIDTH,
    viewport_height: int = DEFAULT_IG_REELS_VIEWPORT_HEIGHT,
    settle_seconds: float = DEFAULT_IG_REELS_SETTLE_SECONDS,
    max_response_bytes: int = DEFAULT_IG_REELS_MAX_RESPONSE_BYTES,
    max_rows: int = 12,
    block_heavy_assets: bool = True,
    proxy_profile: ProxyProfile | None = None,
    storage_state_path: Path | None = None,
    headless: bool = True,
    browser_channel: str | None = None,
) -> IgReelsGridCaptureResult:
    """Capture one bounded IG creator-grid page load."""

    observation = fetch_browser_page_observation_capture(
        url=reels_url,
        dom_extract_script=_DOM_ROW_EXTRACT_SCRIPT,
        dom_extract_arg={"profileHandle": profile_handle, "maxRows": max_rows},
        response_url_predicate=_should_preserve_response,
        timeout_seconds=timeout_seconds,
        wait_until="load",
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        max_response_bytes=max_response_bytes,
        settle_seconds=settle_seconds,
        selector=_DOM_GRID_SELECTOR,
        selector_timeout_seconds=5.0,
        block_resource_types=_HEAVY_RESOURCE_TYPES if block_heavy_assets else (),
        proxy_profile=proxy_profile,
        storage_state_path=storage_state_path,
        headless=headless,
        browser_channel=browser_channel,
    )
    if isinstance(observation, BrowserSnapshotFailure):
        return IgReelsGridCaptureFailure(
            requested_url=reels_url,
            final_url=observation.final_url,
            failure_kind=observation.failure_kind.value,
            message=observation.message,
        )

    try:
        dom_rows = _normalize_dom_rows(observation.dom_observation)
    except ValueError as exc:
        return IgReelsGridCaptureFailure(
            requested_url=reels_url,
            final_url=observation.final_url,
            failure_kind="capture_failed",
            message=str(exc),
        )

    passive_json_responses = _read_passive_responses(observation.responses)
    metadata = {
        **observation.metadata,
        "block_heavy_assets": block_heavy_assets,
        "max_rows": max_rows,
        "dom_row_count": len(dom_rows),
        "passive_json_response_count": len(passive_json_responses),
    }
    limitation_notes = list(observation.limitation_notes)
    return IgReelsGridCaptureSuccess(
        requested_url=reels_url,
        final_url=observation.final_url,
        title=observation.title,
        visible_text=observation.visible_text,
        dom_rows=dom_rows,
        passive_json_responses=passive_json_responses,
        metadata=metadata,
        warning_notes=list(observation.warning_notes),
        limitation_notes=limitation_notes,
    )


def _should_preserve_response(url: str) -> bool:
    return source_surface_from_url_or_path(url) in _PRESERVED_RESPONSE_SURFACES


def _read_passive_responses(
    responses: list[BrowserPageResponse],
) -> list[IgReelsGridPassiveResponse]:
    preserved: list[IgReelsGridPassiveResponse] = []
    seen: set[tuple[str, int]] = set()
    for response in responses:
        surface = source_surface_from_url_or_path(response.requested_url)
        if surface not in _PRESERVED_RESPONSE_SURFACES:
            continue
        identity = (response.requested_url, response.status)
        if identity in seen:
            continue
        seen.add(identity)
        preserved.append(
            IgReelsGridPassiveResponse(
                source_surface=surface,
                requested_url=response.requested_url,
                final_url=response.final_url,
                status=response.status,
                ok=response.ok,
                body_text=response.body_text,
                response_headers=dict(response.response_headers),
                limitation_notes=list(response.limitation_notes),
            )
        )
    return preserved


def _normalize_dom_rows(dom_observation: object) -> list[dict[str, object]]:
    if not isinstance(dom_observation, list):
        raise ValueError("IG grid DOM extraction returned a non-list observation")
    rows: list[dict[str, object]] = []
    for row in dom_observation:
        if not isinstance(row, dict):
            raise ValueError("IG grid DOM extraction returned a non-object row")
        rows.append(dict(row))
    return rows

_DOM_ROW_EXTRACT_SCRIPT = r"""
({profileHandle, maxRows}) => {
  const numericPattern = /^\d[\d,.]*(?:[KMB])?$/i;
  const numericFindPattern = /\d[\d,.]*(?:[KMB])?/gi;

  function numericTexts(text) {
    if (!text) return [];
    const values = text.match(numericFindPattern) || [];
    return values.filter((value) => numericPattern.test(value));
  }

  function leafNumericTexts(root) {
    const out = [];
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const text = (walker.currentNode.nodeValue || "").trim();
      if (numericPattern.test(text)) {
        out.push({ text });
      }
    }
    return out;
  }

  function pathFromHref(href) {
    try {
      return new URL(href, window.location.href).pathname;
    } catch (_error) {
      return href || "";
    }
  }

  function isMediaPath(path) {
    return path.includes("/reel/") || path.includes("/p/");
  }

  const handle = (profileHandle || "").toLowerCase();
  const rows = [];
  const seen = new Set();
  const anchors = Array.from(document.querySelectorAll("a[href]"));
  for (const anchor of anchors) {
    const href = anchor.href || anchor.getAttribute("href") || "";
    const path = pathFromHref(href);
    if (!isMediaPath(path)) continue;
    const parts = path.split("/").filter(Boolean);
    if (handle && parts[0] && !["p", "reel"].includes(parts[0]) && parts[0].toLowerCase() !== handle) {
      continue;
    }
    const rect = anchor.getBoundingClientRect();
    if (rect.width <= 0 || rect.height <= 0) continue;
    if (rect.bottom < 0 || rect.top > window.innerHeight) continue;
    const identity = path.replace(/\/$/, "");
    if (seen.has(identity)) continue;
    seen.add(identity);
    const visibleText = anchor.innerText || "";
    rows.push({
      href,
      path,
      visibleText,
      visibleNumericTexts: numericTexts(visibleText),
      leafNumericTexts: leafNumericTexts(anchor),
      rect: {
        x: rect.x,
        y: rect.y,
        width: rect.width,
        height: rect.height,
      },
    });
    if (rows.length >= maxRows) break;
  }
  return rows;
}
"""


__all__ = [
    "DEFAULT_IG_REELS_MAX_RESPONSE_BYTES",
    "DEFAULT_IG_REELS_SETTLE_SECONDS",
    "DEFAULT_IG_REELS_TIMEOUT_SECONDS",
    "DEFAULT_IG_REELS_VIEWPORT_HEIGHT",
    "DEFAULT_IG_REELS_VIEWPORT_WIDTH",
    "IgReelsGridCaptureFailure",
    "IgReelsGridCaptureResult",
    "IgReelsGridCaptureSuccess",
    "IgReelsGridPassiveResponse",
    "fetch_ig_reels_grid_capture",
]
