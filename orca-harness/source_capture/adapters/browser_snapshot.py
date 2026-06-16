from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from importlib import import_module
from pathlib import Path
from typing import Protocol, Sequence, TypeAlias
from urllib.parse import urlparse

from harness_utils import utc_now_z


DEFAULT_TIMEOUT_SECONDS = 20.0
DEFAULT_VIEWPORT_WIDTH = 1280
DEFAULT_VIEWPORT_HEIGHT = 720
DEFAULT_MAX_ARTIFACT_BYTES = 5_000_000
ALLOWED_WAIT_UNTIL = {"commit", "domcontentloaded", "load", "networkidle"}
# Pause after each scroll-to-bottom pass so lazy-loaded (infinite-scroll / "load
# more") content can fetch and render before the next pass or the capture.
_SCROLL_PASS_SETTLE_MS = 2000
# Safety cap so an infinite-scroll page (whose scrollHeight keeps growing) cannot
# loop unbounded even if a caller passes a very large scroll_passes.
_MAX_SCROLL_PASSES = 40


class BrowserSnapshotFailureKind(StrEnum):
    DEPENDENCY_UNAVAILABLE = "dependency_unavailable"
    TIMEOUT = "timeout"
    CAPTURE_FAILED = "capture_failed"
    EMPTY_RENDERED_DOM = "empty_rendered_dom"
    EMPTY_SCREENSHOT = "empty_screenshot"
    SIZE_CAP_EXCEEDED = "size_cap_exceeded"


@dataclass(frozen=True)
class BrowserSnapshotSuccess:
    requested_url: str
    final_url: str
    title: str | None
    rendered_dom: str
    visible_text: str
    screenshot_png: bytes
    metadata: dict[str, object]
    warning_notes: list[str]
    limitation_notes: list[str]


@dataclass(frozen=True)
class BrowserSnapshotFailure:
    requested_url: str
    failure_kind: BrowserSnapshotFailureKind
    message: str
    final_url: str | None = None


BrowserSnapshotResult: TypeAlias = BrowserSnapshotSuccess | BrowserSnapshotFailure


@dataclass(frozen=True)
class BrowserContextRequest:
    request_id: str
    url: str
    headers: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class BrowserContextResponse:
    request_id: str
    requested_url: str
    final_url: str
    status: int
    ok: bool
    body_text: str
    response_headers: dict[str, str]


@dataclass(frozen=True)
class BrowserContextResponsesSuccess:
    page_url: str
    final_page_url: str
    responses: list[BrowserContextResponse]
    metadata: dict[str, object]
    warning_notes: list[str]
    limitation_notes: list[str]


BrowserContextResponsesResult: TypeAlias = BrowserContextResponsesSuccess | BrowserSnapshotFailure


class BrowserSnapshotEngineResult(Protocol):
    final_url: str
    title: str | None
    rendered_dom: str
    visible_text: str
    screenshot_png: bytes
    warning_notes: list[str]


class BrowserSnapshotEngine(Protocol):
    def capture(
        self,
        *,
        url: str,
        timeout_seconds: float,
        wait_until: str,
        viewport_width: int,
        viewport_height: int,
        storage_state_path: Path | None = None,
        scroll_passes: int = 0,
        scroll_step_px: int = 0,
    ) -> BrowserSnapshotEngineResult:
        ...


class BrowserContextResponseEngine(Protocol):
    def capture_context_responses(
        self,
        *,
        page_url: str,
        requests: Sequence[BrowserContextRequest],
        timeout_seconds: float,
        wait_until: str,
        viewport_width: int,
        viewport_height: int,
        storage_state_path: Path | None = None,
    ) -> BrowserContextResponsesSuccess:
        ...


def fetch_browser_snapshot_capture(
    *,
    url: str,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    wait_until: str = "load",
    viewport_width: int = DEFAULT_VIEWPORT_WIDTH,
    viewport_height: int = DEFAULT_VIEWPORT_HEIGHT,
    max_artifact_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
    storage_state_path: Path | None = None,
    scroll_passes: int = 0,
    scroll_step_px: int = 0,
    engine: BrowserSnapshotEngine | None = None,
) -> BrowserSnapshotResult:
    normalized_url = _validate_http_url(url)
    _validate_positive_number("timeout_seconds", timeout_seconds)
    _validate_positive_int("viewport_width", viewport_width)
    _validate_positive_int("viewport_height", viewport_height)
    _validate_positive_int("max_artifact_bytes", max_artifact_bytes)
    if scroll_passes < 0:
        raise ValueError("scroll_passes must be zero or greater")
    if scroll_step_px < 0:
        raise ValueError("scroll_step_px must be zero or greater")
    if wait_until not in ALLOWED_WAIT_UNTIL:
        allowed = ", ".join(sorted(ALLOWED_WAIT_UNTIL))
        raise ValueError(f"wait_until must be one of: {allowed}")

    capture_engine = engine or _PlaywrightBrowserSnapshotEngine()
    try:
        engine_result = capture_engine.capture(
            url=normalized_url,
            timeout_seconds=timeout_seconds,
            wait_until=wait_until,
            viewport_width=viewport_width,
            viewport_height=viewport_height,
            storage_state_path=storage_state_path,
            scroll_passes=scroll_passes,
            scroll_step_px=scroll_step_px,
        )
    except _BrowserSnapshotDependencyUnavailable as exc:
        return BrowserSnapshotFailure(
            requested_url=normalized_url,
            failure_kind=BrowserSnapshotFailureKind.DEPENDENCY_UNAVAILABLE,
            message=str(exc),
        )
    except Exception as exc:
        return BrowserSnapshotFailure(
            requested_url=normalized_url,
            failure_kind=_failure_kind_from_exception(exc),
            message=f"Browser snapshot capture failed: {exc}",
        )

    if not engine_result.rendered_dom:
        return BrowserSnapshotFailure(
            requested_url=normalized_url,
            final_url=engine_result.final_url,
            failure_kind=BrowserSnapshotFailureKind.EMPTY_RENDERED_DOM,
            message="Browser snapshot returned an empty rendered DOM",
        )
    if not engine_result.screenshot_png:
        return BrowserSnapshotFailure(
            requested_url=normalized_url,
            final_url=engine_result.final_url,
            failure_kind=BrowserSnapshotFailureKind.EMPTY_SCREENSHOT,
            message="Browser snapshot returned an empty screenshot",
        )

    artifact_sizes = {
        "rendered_dom": len(engine_result.rendered_dom.encode("utf-8")),
        "visible_text": len(engine_result.visible_text.encode("utf-8")),
        "screenshot_png": len(engine_result.screenshot_png),
    }
    oversized = {
        name: size
        for name, size in artifact_sizes.items()
        if size > max_artifact_bytes
    }
    if oversized:
        details = ", ".join(f"{name}={size}" for name, size in sorted(oversized.items()))
        return BrowserSnapshotFailure(
            requested_url=normalized_url,
            final_url=engine_result.final_url,
            failure_kind=BrowserSnapshotFailureKind.SIZE_CAP_EXCEEDED,
            message=(
                f"Browser snapshot artifact exceeded max-artifact-bytes cap "
                f"({max_artifact_bytes}): {details}"
            ),
        )

    warning_notes: list[str] = []
    if engine_result.final_url != normalized_url:
        warning_notes.append(
            f"browser_snapshot landed at {engine_result.final_url} from requested URL {normalized_url}"
        )
    warning_notes.extend(engine_result.warning_notes)

    metadata = {
        "requested_url": normalized_url,
        "final_url": engine_result.final_url,
        "title": engine_result.title,
        "capture_timestamp": utc_now_z(),
        "timeout_seconds": timeout_seconds,
        "wait_until": wait_until,
        "viewport_width": viewport_width,
        "viewport_height": viewport_height,
        "screenshot_mode": "viewport",
        "storage_state_loaded": storage_state_path is not None,
        "rendered_dom_byte_count": artifact_sizes["rendered_dom"],
        "visible_text_byte_count": artifact_sizes["visible_text"],
        "screenshot_byte_count": artifact_sizes["screenshot_png"],
    }

    return BrowserSnapshotSuccess(
        requested_url=normalized_url,
        final_url=engine_result.final_url,
        title=engine_result.title,
        rendered_dom=engine_result.rendered_dom,
        visible_text=engine_result.visible_text,
        screenshot_png=engine_result.screenshot_png,
        metadata=metadata,
        warning_notes=warning_notes,
        limitation_notes=[],
    )


def fetch_browser_context_responses(
    *,
    page_url: str,
    requests: Sequence[BrowserContextRequest],
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    wait_until: str = "load",
    viewport_width: int = DEFAULT_VIEWPORT_WIDTH,
    viewport_height: int = DEFAULT_VIEWPORT_HEIGHT,
    max_response_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
    storage_state_path: Path | None = None,
    engine: BrowserContextResponseEngine | None = None,
) -> BrowserContextResponsesResult:
    """Run same-browser-context fetches and preserve response bodies.

    This is intentionally narrower than a crawler: callers provide a fixed,
    bounded request list, and HTTP statuses are returned as observed response
    facts instead of being converted into success/failure.
    """
    normalized_page_url = _validate_http_url(page_url)
    if not requests:
        raise ValueError("at least one browser context request is required")
    normalized_requests: list[BrowserContextRequest] = []
    for request in requests:
        request_id = request.request_id.strip()
        if not request_id:
            raise ValueError("browser context request_id must be non-empty")
        normalized_requests.append(
            BrowserContextRequest(
                request_id=request_id,
                url=_validate_http_url(request.url),
                headers=dict(request.headers),
            )
        )
    _validate_positive_number("timeout_seconds", timeout_seconds)
    _validate_positive_int("viewport_width", viewport_width)
    _validate_positive_int("viewport_height", viewport_height)
    _validate_positive_int("max_response_bytes", max_response_bytes)
    if wait_until not in ALLOWED_WAIT_UNTIL:
        allowed = ", ".join(sorted(ALLOWED_WAIT_UNTIL))
        raise ValueError(f"wait_until must be one of: {allowed}")

    response_engine = engine or _PlaywrightBrowserSnapshotEngine()
    try:
        result = response_engine.capture_context_responses(
            page_url=normalized_page_url,
            requests=normalized_requests,
            timeout_seconds=timeout_seconds,
            wait_until=wait_until,
            viewport_width=viewport_width,
            viewport_height=viewport_height,
            storage_state_path=storage_state_path,
        )
    except _BrowserSnapshotDependencyUnavailable as exc:
        return BrowserSnapshotFailure(
            requested_url=normalized_page_url,
            failure_kind=BrowserSnapshotFailureKind.DEPENDENCY_UNAVAILABLE,
            message=str(exc),
        )
    except Exception as exc:
        return BrowserSnapshotFailure(
            requested_url=normalized_page_url,
            failure_kind=_failure_kind_from_exception(exc),
            message=f"Browser context response capture failed: {exc}",
        )

    oversized = [
        response
        for response in result.responses
        if len(response.body_text.encode("utf-8")) > max_response_bytes
    ]
    if oversized:
        details = ", ".join(
            f"{response.request_id}={len(response.body_text.encode('utf-8'))}"
            for response in oversized
        )
        return BrowserSnapshotFailure(
            requested_url=normalized_page_url,
            final_url=result.final_page_url,
            failure_kind=BrowserSnapshotFailureKind.SIZE_CAP_EXCEEDED,
            message=(
                f"Browser context response body exceeded max-response-bytes cap "
                f"({max_response_bytes}): {details}"
            ),
        )
    return result


class _PlaywrightBrowserSnapshotEngine:
    def capture(
        self,
        *,
        url: str,
        timeout_seconds: float,
        wait_until: str,
        viewport_width: int,
        viewport_height: int,
        storage_state_path: Path | None = None,
        scroll_passes: int = 0,
        scroll_step_px: int = 0,
    ) -> BrowserSnapshotEngineResult:
        try:
            sync_api = import_module("playwright.sync_api")
        except ModuleNotFoundError as exc:
            raise _BrowserSnapshotDependencyUnavailable(
                "Playwright is not installed. Install the browser optional dependency before running browser snapshots."
            ) from exc

        timeout_ms = timeout_seconds * 1000
        with sync_api.sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch(headless=True)
            except Exception as exc:
                if _looks_like_missing_browser_binary(exc):
                    raise _BrowserSnapshotDependencyUnavailable(
                        "Playwright Chromium browser binary is not installed. "
                        "Run `python -m playwright install chromium` before running browser snapshots."
                    ) from exc
                raise
            try:
                context_kwargs: dict[str, object] = {
                    "viewport": {
                        "width": viewport_width,
                        "height": viewport_height,
                    }
                }
                if storage_state_path is not None:
                    context_kwargs["storage_state"] = str(storage_state_path)
                context = browser.new_context(**context_kwargs)
                try:
                    page = context.new_page()
                    page.goto(url, wait_until=wait_until, timeout=timeout_ms)
                    if scroll_step_px > 0:
                        position = 0
                        for _ in range(_MAX_SCROLL_PASSES):
                            height = page.evaluate("() => document.body.scrollHeight")
                            if position >= height:
                                break
                            position += scroll_step_px
                            page.evaluate("(y) => window.scrollTo(0, y)", position)
                            page.wait_for_timeout(_SCROLL_PASS_SETTLE_MS)
                    elif scroll_passes > 0:
                        for _ in range(min(scroll_passes, _MAX_SCROLL_PASSES)):
                            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                            page.wait_for_timeout(_SCROLL_PASS_SETTLE_MS)
                    rendered_dom = page.content()
                    warning_notes: list[str] = []
                    try:
                        visible_text = page.locator("body").inner_text(timeout=timeout_ms)
                    except Exception as exc:
                        visible_text = ""
                        warning_notes.append(f"browser_snapshot visible_text extraction failed: {exc}")
                    screenshot_png = page.screenshot(
                        type="png",
                        full_page=False,
                        timeout=timeout_ms,
                    )
                    return _EngineResult(
                        final_url=page.url,
                        title=page.title(),
                        rendered_dom=rendered_dom,
                        visible_text=visible_text,
                        screenshot_png=screenshot_png,
                        warning_notes=warning_notes,
                    )
                finally:
                    context.close()
            finally:
                browser.close()

    def capture_context_responses(
        self,
        *,
        page_url: str,
        requests: Sequence[BrowserContextRequest],
        timeout_seconds: float,
        wait_until: str,
        viewport_width: int,
        viewport_height: int,
        storage_state_path: Path | None = None,
    ) -> BrowserContextResponsesSuccess:
        try:
            sync_api = import_module("playwright.sync_api")
        except ModuleNotFoundError as exc:
            raise _BrowserSnapshotDependencyUnavailable(
                "Playwright is not installed. Install the browser optional dependency before running browser context responses."
            ) from exc

        timeout_ms = timeout_seconds * 1000
        with sync_api.sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch(headless=True)
            except Exception as exc:
                if _looks_like_missing_browser_binary(exc):
                    raise _BrowserSnapshotDependencyUnavailable(
                        "Playwright Chromium browser binary is not installed. "
                        "Run `python -m playwright install chromium` before running browser context responses."
                    ) from exc
                raise
            try:
                context_kwargs: dict[str, object] = {
                    "viewport": {
                        "width": viewport_width,
                        "height": viewport_height,
                    }
                }
                if storage_state_path is not None:
                    context_kwargs["storage_state"] = str(storage_state_path)
                context = browser.new_context(**context_kwargs)
                try:
                    page = context.new_page()
                    page.goto(page_url, wait_until=wait_until, timeout=timeout_ms)
                    warning_notes: list[str] = []
                    if page.url != page_url:
                        warning_notes.append(
                            f"browser_context landed at {page.url} from requested URL {page_url}"
                        )
                    responses: list[BrowserContextResponse] = []
                    for request in requests:
                        raw = page.evaluate(
                            """async ({url, headers, timeoutMs}) => {
                                const controller = new AbortController();
                                const timeout = setTimeout(() => controller.abort(), timeoutMs);
                                try {
                                    const response = await fetch(url, {
                                        headers,
                                        credentials: "same-origin",
                                        signal: controller.signal
                                    });
                                    const responseHeaders = {};
                                    response.headers.forEach((value, key) => {
                                        responseHeaders[key] = value;
                                    });
                                    return {
                                        finalUrl: response.url,
                                        status: response.status,
                                        ok: response.ok,
                                        bodyText: await response.text(),
                                        headers: responseHeaders
                                    };
                                } finally {
                                    clearTimeout(timeout);
                                }
                            }""",
                            {
                                "url": request.url,
                                "headers": request.headers,
                                "timeoutMs": timeout_ms,
                            },
                        )
                        responses.append(
                            BrowserContextResponse(
                                request_id=request.request_id,
                                requested_url=request.url,
                                final_url=str(raw["finalUrl"]),
                                status=int(raw["status"]),
                                ok=bool(raw["ok"]),
                                body_text=str(raw["bodyText"]),
                                response_headers=dict(raw["headers"]),
                            )
                        )
                    metadata = {
                        "page_url": page_url,
                        "final_page_url": page.url,
                        "capture_timestamp": utc_now_z(),
                        "timeout_seconds": timeout_seconds,
                        "wait_until": wait_until,
                        "viewport_width": viewport_width,
                        "viewport_height": viewport_height,
                        "storage_state_loaded": storage_state_path is not None,
                        "request_count": len(responses),
                    }
                    return BrowserContextResponsesSuccess(
                        page_url=page_url,
                        final_page_url=page.url,
                        responses=responses,
                        metadata=metadata,
                        warning_notes=warning_notes,
                        limitation_notes=[],
                    )
                finally:
                    context.close()
            finally:
                browser.close()


@dataclass(frozen=True)
class _EngineResult:
    final_url: str
    title: str | None
    rendered_dom: str
    visible_text: str
    screenshot_png: bytes
    warning_notes: list[str] = field(default_factory=list)


class _BrowserSnapshotDependencyUnavailable(RuntimeError):
    pass


def _validate_http_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Browser snapshot capture requires an absolute http:// or https:// URL")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("Browser snapshot capture does not accept URLs with embedded credentials")
    return parsed.geturl()


def _validate_positive_number(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")


def _validate_positive_int(name: str, value: int) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")


def _failure_kind_from_exception(error: Exception) -> BrowserSnapshotFailureKind:
    text = f"{type(error).__name__}: {error}".lower()
    if "timeout" in text or "timed out" in text or "aborterror" in text or "aborted" in text:
        return BrowserSnapshotFailureKind.TIMEOUT
    return BrowserSnapshotFailureKind.CAPTURE_FAILED


def _looks_like_missing_browser_binary(error: Exception) -> bool:
    text = f"{type(error).__name__}: {error}".lower()
    return (
        "executable doesn't exist" in text
        or "browser has not been installed" in text
        or "playwright install" in text
    )
