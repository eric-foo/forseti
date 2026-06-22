from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, TypeAlias

from source_capture.adapters.cloakbrowser_snapshot import (
    CloakBrowserSnapshotEngine,
    CloakBrowserSnapshotFailure,
    CloakBrowserSnapshotSuccess,
    fetch_cloakbrowser_snapshot_capture,
)
from source_capture.block_shell import classify_capture_body
from source_capture.screening_read import (
    HUMAN_RATE_NOTE,
    ScreeningReadDispatch,
    _post_fetch_login_gate,
    _public_url_gate,
    _validate_dispatch,
)


@dataclass(frozen=True)
class BrowserScreenLight:
    requested_url: str
    final_url: str
    title: str | None
    visible_text: str
    visible_text_byte_count: int
    content_class: str
    content_signal: str | None
    content_class_detail: str
    access_block_reason: str | None = None
    warning_notes: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)
    human_rate_note: str = HUMAN_RATE_NOTE
    status_note: str = "browser_rendered_no_http_status"


@dataclass(frozen=True)
class BrowserScreeningReadRefused:
    requested_url: str
    reason: Literal[
        "not_orchestrator_invoked",
        "unbounded_dispatch",
        "entitlement_gated",
        "login_redirect",
        "fetch_failed",
    ]
    message: str


BrowserScreeningReadResult: TypeAlias = BrowserScreenLight | BrowserScreeningReadRefused


def screening_browser_read(
    *,
    url: str,
    dispatch: ScreeningReadDispatch,
    timeout_seconds: float = 20.0,
    wait_until: str = "load",
    viewport_width: int = 1280,
    viewport_height: int = 720,
    max_artifact_bytes: int = 5_000_000,
    block_heavy_assets: bool = False,
    settle_seconds: float = 0.0,
    scroll_passes: int = 0,
    load_more_selector: str | None = None,
    load_more_clicks: int = 0,
    scroll_step_px: int = 0,
    engine: CloakBrowserSnapshotEngine | None = None,
) -> BrowserScreeningReadResult:
    """Render a public page and return visible text only.

    The wrapper intentionally classifies block-shell posture on visible text,
    not the rendered DOM, because a passed Cloudflare page can retain challenge
    scripts in the DOM after the human-visible page is clean.
    """
    dispatch_refusal = _validate_dispatch(dispatch, requested_url=url, route="screening_browser_read")
    if dispatch_refusal is not None:
        return BrowserScreeningReadRefused(
            requested_url=url,
            reason=dispatch_refusal.reason,
            message=dispatch_refusal.message,
        )
    gate_refusal = _public_url_gate(url, route="screening_browser_read")
    if gate_refusal is not None:
        return BrowserScreeningReadRefused(
            requested_url=url,
            reason=gate_refusal.reason,
            message=gate_refusal.message,
        )

    result = fetch_cloakbrowser_snapshot_capture(
        url=url,
        timeout_seconds=timeout_seconds,
        wait_until=wait_until,
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        max_artifact_bytes=max_artifact_bytes,
        proxy_profile=None,
        block_heavy_assets=block_heavy_assets,
        settle_seconds=settle_seconds,
        scroll_passes=scroll_passes,
        load_more_selector=load_more_selector,
        load_more_clicks=load_more_clicks,
        scroll_step_px=scroll_step_px,
        pre_capture=None,
        engine=engine,
    )
    if isinstance(result, CloakBrowserSnapshotFailure):
        return BrowserScreeningReadRefused(
            requested_url=url,
            reason="fetch_failed",
            message=result.message,
        )
    return _screen_light_from_browser_result(requested_url=url, result=result)


def _screen_light_from_browser_result(
    *,
    requested_url: str,
    result: CloakBrowserSnapshotSuccess,
) -> BrowserScreeningReadResult:
    login_refusal = _post_fetch_login_gate(
        requested_url=requested_url,
        final_url=result.final_url,
        body_text=result.visible_text,
        route="screening_browser_read",
    )
    if login_refusal is not None:
        return BrowserScreeningReadRefused(
            requested_url=requested_url,
            reason=login_refusal.reason,
            message=login_refusal.message,
        )
    visible_text_bytes = result.visible_text.encode("utf-8")
    classification = classify_capture_body(
        status=200,
        headers={},
        body=visible_text_bytes,
    )
    warning_notes = list(result.warning_notes)
    warning_notes.append("screening_browser_read returned visible text only; rendered DOM and screenshot were not returned")
    return BrowserScreenLight(
        requested_url=requested_url,
        final_url=result.final_url,
        title=result.title,
        visible_text=result.visible_text,
        visible_text_byte_count=len(visible_text_bytes),
        content_class=classification.classification.value,
        content_signal=classification.signal,
        content_class_detail=classification.detail,
        access_block_reason=result.access_block_reason,
        warning_notes=warning_notes,
        limitation_notes=list(result.limitation_notes),
    )


__all__ = [
    "BrowserScreenLight",
    "BrowserScreeningReadRefused",
    "BrowserScreeningReadResult",
    "screening_browser_read",
]
