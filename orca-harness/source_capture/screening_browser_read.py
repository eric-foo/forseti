from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, TypeAlias
from urllib.parse import urlparse

from source_capture.adapters.cloakbrowser_snapshot import (
    CloakBrowserSnapshotFailure,
    CloakBrowserSnapshotEngine,
    fetch_cloakbrowser_snapshot_capture,
)
from source_capture.block_shell import CaptureBodyClass, classify_capture_body


SCREENING_ORCHESTRATOR_CONTEXT = "screen_orchestrator"


@dataclass(frozen=True)
class ScreeningBrowserRead:
    """Screen-light browser read: visible text only, no packet, no manifest, no ECR."""

    requested_url: str
    final_url: str
    title: str | None
    visible_text: str
    byte_count: int
    content_class: str
    content_signal: str | None
    content_detail: str
    warning_notes: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class ScreeningBrowserReadRefused:
    requested_url: str
    reason: Literal[
        "not_orchestrator_invoked",
        "entitlement_gated",
        "fetch_failed",
    ]
    message: str


ScreeningBrowserReadResult: TypeAlias = ScreeningBrowserRead | ScreeningBrowserReadRefused


def screening_browser_read(
    *,
    url: str,
    invocation_context: str,
    timeout_seconds: float = 20.0,
    wait_until: str = "load",
    viewport_width: int = 1280,
    viewport_height: int = 720,
    max_artifact_bytes: int = 5_000_000,
    settle_seconds: float = 0.0,
    scroll_passes: int = 0,
    scroll_step_px: int = 0,
    engine: CloakBrowserSnapshotEngine | None = None,
) -> ScreeningBrowserReadResult:
    """Render one public URL through CloakBrowser and classify rendered visible text.

    This is a screening-only wrapper over the existing adapter. It deliberately
    returns no screenshot/rendered DOM, writes no packet, and classifies only the
    visible text with block_shell so residual challenge scripts in the full DOM
    cannot create a false block-shell result after a page has rendered.
    """
    if invocation_context != SCREENING_ORCHESTRATOR_CONTEXT:
        return ScreeningBrowserReadRefused(
            requested_url=url,
            reason="not_orchestrator_invoked",
            message="screening_browser_read is orchestrator-invoked only; walker-direct calls are refused",
        )

    gate_refusal = _public_url_gate(url)
    if gate_refusal is not None:
        return gate_refusal

    result = fetch_cloakbrowser_snapshot_capture(
        url=url,
        timeout_seconds=timeout_seconds,
        wait_until=wait_until,
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        max_artifact_bytes=max_artifact_bytes,
        settle_seconds=settle_seconds,
        scroll_passes=scroll_passes,
        scroll_step_px=scroll_step_px,
        engine=engine,
    )
    if isinstance(result, CloakBrowserSnapshotFailure):
        return ScreeningBrowserReadRefused(
            requested_url=url,
            reason="fetch_failed",
            message=result.message,
        )

    visible_body = result.visible_text.encode("utf-8")
    body_class = classify_capture_body(status=0, headers={}, body=visible_body)
    limitation_notes = list(result.limitation_notes)
    if body_class.classification == CaptureBodyClass.BLOCK_SHELL:
        limitation_notes.append(
            "access_failed: screening_browser_read visible text classified as block_shell; "
            f"signal={body_class.signal}"
        )

    return ScreeningBrowserRead(
        requested_url=result.requested_url,
        final_url=result.final_url,
        title=result.title,
        visible_text=result.visible_text,
        byte_count=len(visible_body),
        content_class=body_class.classification.value,
        content_signal=body_class.signal,
        content_detail=body_class.detail,
        warning_notes=list(result.warning_notes),
        limitation_notes=limitation_notes,
        metadata={
            "route": "screening_browser_read",
            "browser_engine": "cloakbrowser",
            "block_shell_input": "visible_text",
            "visible_text_byte_count": len(visible_body),
            "timeout_seconds": timeout_seconds,
            "wait_until": wait_until,
            "settle_seconds": settle_seconds,
            "scroll_passes": scroll_passes,
            "scroll_step_px": scroll_step_px,
            "packet_written": False,
            "ecr_touched": False,
        },
    )


def _public_url_gate(url: str) -> ScreeningBrowserReadRefused | None:
    try:
        parsed = urlparse(url)
    except Exception as exc:
        return ScreeningBrowserReadRefused(
            requested_url=url,
            reason="entitlement_gated",
            message=f"URL could not be parsed ({exc!r}); refusing without fetch.",
        )
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ScreeningBrowserReadRefused(
            requested_url=url,
            reason="entitlement_gated",
            message="screening browser read requires an absolute http:// or https:// URL",
        )
    if parsed.username is not None or parsed.password is not None:
        return ScreeningBrowserReadRefused(
            requested_url=url,
            reason="entitlement_gated",
            message="credential-bearing URLs are refused without fetch",
        )
    return None
