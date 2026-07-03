from __future__ import annotations

import io
import random
from hashlib import sha256
from dataclasses import dataclass, field
from enum import StrEnum
from importlib import import_module
from pathlib import Path
from typing import Callable, Protocol, Sequence, TypeAlias
from urllib.parse import unquote, urlparse, urlunparse

from harness_utils import utc_now_z
from source_capture.proxy_profiles import ProxyProfile
from source_capture.rendered_access import RenderedAccessClass, classify_rendered_access


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


@dataclass(frozen=True)
class BrowserPagePointerAction:
    action_name: str
    candidate_selector: str
    text_markers: tuple[str, ...]
    page_text_markers: tuple[str, ...] = ()
    exact_text_markers: tuple[str, ...] = ()
    wait_after_ms: int = 2500
    move_steps_min: int = 6
    move_steps_max: int = 12
    target_fraction_min: float = 0.35
    target_fraction_max: float = 0.65
    prefer_top_right: bool = False
    visual_top_right_x_fallback: bool = False
    random_seed: int = 0


class BrowserSnapshotFailureKind(StrEnum):
    DEPENDENCY_UNAVAILABLE = "dependency_unavailable"
    ENVIRONMENT_PERMISSION_DENIED = "environment_permission_denied"
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
    access_block_reason: str | None = None


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


@dataclass(frozen=True)
class BrowserPageResponse:
    requested_url: str
    final_url: str
    status: int
    ok: bool
    body_text: str
    response_headers: dict[str, str]
    limitation_notes: list[str] = field(default_factory=list)
    request_method: str | None = None
    resource_type: str | None = None


@dataclass(frozen=True)
class BrowserPageObservationSuccess:
    requested_url: str
    final_url: str
    title: str | None
    visible_text: str
    dom_observation: object
    responses: list[BrowserPageResponse]
    metadata: dict[str, object]
    warning_notes: list[str]
    limitation_notes: list[str]


@dataclass(frozen=True)
class _LazyLoadScrollResult:
    executed_passes: int
    stop_reason: str | None = None


BrowserContextResponsesResult: TypeAlias = BrowserContextResponsesSuccess | BrowserSnapshotFailure
BrowserPageObservationResult: TypeAlias = BrowserPageObservationSuccess | BrowserSnapshotFailure


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
        proxy_profile: ProxyProfile | None = None,
        storage_state_path: Path | None = None,
        scroll_passes: int = 0,
        scroll_step_px: int = 0,
        settle_seconds: float = 0.0,
        headless: bool = True,
        browser_channel: str | None = None,
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
        proxy_profile: ProxyProfile | None = None,
        storage_state_path: Path | None = None,
    ) -> BrowserContextResponsesSuccess:
        ...


class BrowserPageObservationEngine(Protocol):
    def capture_page_observation(
        self,
        *,
        url: str,
        timeout_seconds: float,
        wait_until: str,
        viewport_width: int,
        viewport_height: int,
        dom_extract_script: str,
        dom_extract_arg: object,
        response_url_predicate: Callable[[str], bool],
        post_load_action_script: str | None = None,
        post_load_action_arg: object = None,
        post_load_pointer_action: BrowserPagePointerAction | None = None,
        post_load_pointer_actions: Sequence[BrowserPagePointerAction] = (),
        selector: str | None = None,
        selector_timeout_seconds: float = 5.0,
        max_response_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
        settle_seconds: float = 0.0,
        lazy_load_scroll_passes: int = 0,
        lazy_load_scroll_step_px: int = 0,
        block_resource_types: Sequence[str] = (),
        proxy_profile: ProxyProfile | None = None,
        storage_state_path: Path | None = None,
        headless: bool = True,
        browser_channel: str | None = None,
    ) -> BrowserPageObservationSuccess:
        ...


def fetch_browser_snapshot_capture(
    *,
    url: str,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    wait_until: str = "load",
    viewport_width: int = DEFAULT_VIEWPORT_WIDTH,
    viewport_height: int = DEFAULT_VIEWPORT_HEIGHT,
    max_artifact_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
    proxy_profile: ProxyProfile | None = None,
    storage_state_path: Path | None = None,
    scroll_passes: int = 0,
    scroll_step_px: int = 0,
    settle_seconds: float = 0.0,
    headless: bool = True,
    browser_channel: str | None = None,
    engine: BrowserSnapshotEngine | None = None,
) -> BrowserSnapshotResult:
    normalized_url = _validate_http_url(url)
    normalized_browser_channel = _normalize_browser_channel(browser_channel)
    _validate_positive_number("timeout_seconds", timeout_seconds)
    _validate_positive_int("viewport_width", viewport_width)
    _validate_positive_int("viewport_height", viewport_height)
    _validate_positive_int("max_artifact_bytes", max_artifact_bytes)
    if scroll_passes < 0:
        raise ValueError("scroll_passes must be zero or greater")
    if scroll_step_px < 0:
        raise ValueError("scroll_step_px must be zero or greater")
    if settle_seconds < 0:
        raise ValueError("settle_seconds must be zero or greater")
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
            proxy_profile=proxy_profile,
            storage_state_path=storage_state_path,
            scroll_passes=scroll_passes,
            scroll_step_px=scroll_step_px,
            settle_seconds=settle_seconds,
            headless=headless,
            browser_channel=normalized_browser_channel,
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
            message=_capture_failure_message(
                "Browser snapshot capture failed", exc, proxy_profile=proxy_profile
            ),
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

    rendered_access = classify_rendered_access(
        title=engine_result.title,
        rendered_dom=engine_result.rendered_dom,
        visible_text=engine_result.visible_text,
    )
    access_block_reason = (
        rendered_access.signal
        if rendered_access.classification == RenderedAccessClass.ACCESS_BLOCKED
        else None
    )
    limitation_notes: list[str] = []
    if access_block_reason is not None:
        limitation_notes.append(
            "access_failed: browser_snapshot rendered an access-block/interstitial page "
            f"instead of source content: {access_block_reason}; block artifacts preserved"
        )
    elif rendered_access.classification == RenderedAccessClass.RESIDUAL_CHALLENGE_MARKER:
        limitation_notes.append(
            "rendered_access_warning: browser_snapshot rendered DOM still contains "
            f"{rendered_access.signal}; visible text may be source content, but content "
            "sufficiency is not asserted"
        )

    metadata = {
        "requested_url": normalized_url,
        "final_url": engine_result.final_url,
        "title": engine_result.title,
        "capture_timestamp": utc_now_z(),
        "timeout_seconds": timeout_seconds,
        "wait_until": wait_until,
        "settle_seconds": settle_seconds,
        "headless": headless,
        "browser_channel": normalized_browser_channel,
        "viewport_width": viewport_width,
        "viewport_height": viewport_height,
        "screenshot_mode": "viewport",
        "storage_state_loaded": storage_state_path is not None,
        "access_blocked": access_block_reason is not None,
        "access_block_reason": access_block_reason,
        "rendered_access_classification": rendered_access.classification.value,
        "rendered_access_signal": rendered_access.signal,
        "rendered_access_detail": rendered_access.detail,
        "rendered_dom_byte_count": artifact_sizes["rendered_dom"],
        "visible_text_byte_count": artifact_sizes["visible_text"],
        "screenshot_byte_count": artifact_sizes["screenshot_png"],
        **_proxy_metadata(proxy_profile),
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
        limitation_notes=limitation_notes,
        access_block_reason=access_block_reason,
    )


def fetch_browser_page_observation_capture(
    *,
    url: str,
    dom_extract_script: str,
    dom_extract_arg: object,
    response_url_predicate: Callable[[str], bool],
    post_load_action_script: str | None = None,
    post_load_action_arg: object = None,
    post_load_pointer_action: BrowserPagePointerAction | None = None,
    post_load_pointer_actions: Sequence[BrowserPagePointerAction] = (),
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    wait_until: str = "load",
    viewport_width: int = DEFAULT_VIEWPORT_WIDTH,
    viewport_height: int = DEFAULT_VIEWPORT_HEIGHT,
    max_response_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
    settle_seconds: float = 0.0,
    lazy_load_scroll_passes: int = 0,
    lazy_load_scroll_step_px: int = 0,
    selector: str | None = None,
    selector_timeout_seconds: float = 5.0,
    block_resource_types: Sequence[str] = (),
    proxy_profile: ProxyProfile | None = None,
    storage_state_path: Path | None = None,
    headless: bool = True,
    browser_channel: str | None = None,
    engine: BrowserPageObservationEngine | None = None,
) -> BrowserPageObservationResult:
    """Capture a rendered page observation plus selected same-load responses."""
    normalized_url = _validate_http_url(url)
    normalized_browser_channel = _normalize_browser_channel(browser_channel)
    _validate_positive_number("timeout_seconds", timeout_seconds)
    _validate_positive_int("viewport_width", viewport_width)
    _validate_positive_int("viewport_height", viewport_height)
    _validate_positive_int("max_response_bytes", max_response_bytes)
    if settle_seconds < 0:
        raise ValueError("settle_seconds must be zero or greater")
    if lazy_load_scroll_passes < 0:
        raise ValueError("lazy_load_scroll_passes must be zero or greater")
    if lazy_load_scroll_step_px < 0:
        raise ValueError("lazy_load_scroll_step_px must be zero or greater")
    if selector_timeout_seconds < 0:
        raise ValueError("selector_timeout_seconds must be zero or greater")
    if post_load_action_script is not None and not post_load_action_script.strip():
        raise ValueError("post_load_action_script must not be blank")
    normalized_pointer_action = _normalize_pointer_action(post_load_pointer_action)
    normalized_pointer_actions = _normalize_pointer_actions(post_load_pointer_actions)
    if normalized_pointer_action is not None and normalized_pointer_actions:
        raise ValueError(
            "post_load_pointer_action and post_load_pointer_actions are mutually exclusive"
        )
    if post_load_action_script is not None and (
        normalized_pointer_action is not None or normalized_pointer_actions
    ):
        raise ValueError("post_load_action_script and post_load_pointer_action are mutually exclusive")
    if wait_until not in ALLOWED_WAIT_UNTIL:
        allowed = ", ".join(sorted(ALLOWED_WAIT_UNTIL))
        raise ValueError(f"wait_until must be one of: {allowed}")

    observation_engine = engine or _PlaywrightBrowserSnapshotEngine()
    try:
        return observation_engine.capture_page_observation(
            url=normalized_url,
            timeout_seconds=timeout_seconds,
            wait_until=wait_until,
            viewport_width=viewport_width,
            viewport_height=viewport_height,
            dom_extract_script=dom_extract_script,
            dom_extract_arg=dom_extract_arg,
            response_url_predicate=response_url_predicate,
            post_load_action_script=post_load_action_script,
            post_load_action_arg=post_load_action_arg,
            post_load_pointer_action=normalized_pointer_action,
            post_load_pointer_actions=normalized_pointer_actions,
            selector=selector,
            selector_timeout_seconds=selector_timeout_seconds,
            max_response_bytes=max_response_bytes,
            settle_seconds=settle_seconds,
            lazy_load_scroll_passes=lazy_load_scroll_passes,
            lazy_load_scroll_step_px=lazy_load_scroll_step_px,
            block_resource_types=tuple(block_resource_types),
            proxy_profile=proxy_profile,
            storage_state_path=storage_state_path,
            headless=headless,
            browser_channel=normalized_browser_channel,
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
            message=_capture_failure_message(
                "Browser page observation capture failed", exc, proxy_profile=proxy_profile
            ),
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
    proxy_profile: ProxyProfile | None = None,
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
            proxy_profile=proxy_profile,
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
            message=_capture_failure_message(
                "Browser context response capture failed", exc, proxy_profile=proxy_profile
            ),
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
        proxy_profile: ProxyProfile | None = None,
        storage_state_path: Path | None = None,
        scroll_passes: int = 0,
        scroll_step_px: int = 0,
        settle_seconds: float = 0.0,
        headless: bool = True,
        browser_channel: str | None = None,
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
                launch_kwargs: dict[str, object] = {}
                if proxy_profile is not None:
                    launch_kwargs["proxy"] = _playwright_proxy_settings(proxy_profile)
                if browser_channel is not None:
                    launch_kwargs["channel"] = browser_channel
                browser = playwright.chromium.launch(headless=headless, **launch_kwargs)
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
                if proxy_profile is not None and proxy_profile.timezone is not None:
                    context_kwargs["timezone_id"] = proxy_profile.timezone
                if proxy_profile is not None and proxy_profile.locale is not None:
                    context_kwargs["locale"] = proxy_profile.locale
                context = browser.new_context(**context_kwargs)
                try:
                    page = context.new_page()
                    page.goto(url, wait_until=wait_until, timeout=timeout_ms)
                    if settle_seconds > 0:
                        page.wait_for_timeout(settle_seconds * 1000)
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

    def capture_page_observation(
        self,
        *,
        url: str,
        timeout_seconds: float,
        wait_until: str,
        viewport_width: int,
        viewport_height: int,
        dom_extract_script: str,
        dom_extract_arg: object,
        response_url_predicate: Callable[[str], bool],
        post_load_action_script: str | None = None,
        post_load_action_arg: object = None,
        post_load_pointer_action: BrowserPagePointerAction | None = None,
        post_load_pointer_actions: Sequence[BrowserPagePointerAction] = (),
        selector: str | None = None,
        selector_timeout_seconds: float = 5.0,
        max_response_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
        settle_seconds: float = 0.0,
        lazy_load_scroll_passes: int = 0,
        lazy_load_scroll_step_px: int = 0,
        block_resource_types: Sequence[str] = (),
        proxy_profile: ProxyProfile | None = None,
        storage_state_path: Path | None = None,
        headless: bool = True,
        browser_channel: str | None = None,
    ) -> BrowserPageObservationSuccess:
        try:
            sync_api = import_module("playwright.sync_api")
        except ModuleNotFoundError as exc:
            raise _BrowserSnapshotDependencyUnavailable(
                "Playwright is not installed. Install the browser optional dependency before running browser page observations."
            ) from exc

        timeout_ms = timeout_seconds * 1000
        selector_timeout_ms = selector_timeout_seconds * 1000
        blocked_resource_types = set(block_resource_types)
        selected_responses: list[object] = []
        with sync_api.sync_playwright() as playwright:
            try:
                launch_kwargs: dict[str, object] = {}
                if proxy_profile is not None:
                    launch_kwargs["proxy"] = _playwright_proxy_settings(proxy_profile)
                if browser_channel is not None:
                    launch_kwargs["channel"] = browser_channel
                browser = playwright.chromium.launch(headless=headless, **launch_kwargs)
            except Exception as exc:
                if _looks_like_missing_browser_binary(exc):
                    raise _BrowserSnapshotDependencyUnavailable(
                        "Playwright Chromium browser binary is not installed. "
                        "Run `python -m playwright install chromium` before running browser page observations."
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
                if proxy_profile is not None and proxy_profile.timezone is not None:
                    context_kwargs["timezone_id"] = proxy_profile.timezone
                if proxy_profile is not None and proxy_profile.locale is not None:
                    context_kwargs["locale"] = proxy_profile.locale
                context = browser.new_context(**context_kwargs)
                try:
                    page = context.new_page()
                    if blocked_resource_types:
                        page.route(
                            "**/*",
                            lambda route: route.abort()
                            if route.request.resource_type in blocked_resource_types
                            else route.continue_(),
                        )
                    page.on(
                        "response",
                        lambda response: selected_responses.append(response)
                        if response_url_predicate(str(response.url))
                        else None,
                    )
                    page.goto(url, wait_until=wait_until, timeout=timeout_ms)
                    if settle_seconds > 0:
                        page.wait_for_timeout(settle_seconds * 1000)

                    warning_notes: list[str] = []
                    if lazy_load_scroll_passes > _MAX_SCROLL_PASSES:
                        warning_notes.append(
                            "browser_page_observation lazy_load_scroll_passes capped "
                            f"from {lazy_load_scroll_passes} to {_MAX_SCROLL_PASSES}"
                        )
                    if selector is not None:
                        try:
                            page.wait_for_selector(selector, timeout=selector_timeout_ms)
                        except Exception as exc:
                            warning_notes.append(
                                f"browser_page_observation selector wait failed: {exc}"
                            )
                    pointer_action_receipt: dict[str, object] | None = None
                    pointer_action_receipts: list[dict[str, object]] = []
                    if post_load_action_script is not None:
                        page.evaluate(post_load_action_script, post_load_action_arg)
                    if post_load_pointer_action is not None:
                        pointer_action_receipt = _run_pointer_action(page, post_load_pointer_action)
                        pointer_action_receipts.append(pointer_action_receipt)
                    for pointer_action in post_load_pointer_actions:
                        pointer_action_receipt = _run_pointer_action(page, pointer_action)
                        pointer_action_receipts.append(pointer_action_receipt)
                    try:
                        visible_text = page.locator("body").inner_text(timeout=timeout_ms)
                    except Exception as exc:
                        visible_text = ""
                        warning_notes.append(
                            f"browser_page_observation visible_text extraction failed: {exc}"
                        )
                    dom_observation = page.evaluate(dom_extract_script, dom_extract_arg)
                    lazy_load_scroll_result = _run_bounded_lazy_load_scrolls(
                        page,
                        scroll_passes=lazy_load_scroll_passes,
                        scroll_step_px=lazy_load_scroll_step_px,
                    )
                    responses = _read_observed_page_responses(
                        selected_responses,
                        max_response_bytes=max_response_bytes,
                    )
                    final_url = page.url
                    title = page.title()
                    if final_url != url:
                        warning_notes.append(
                            f"browser_page_observation landed at {final_url} from requested URL {url}"
                        )
                    limitation_notes = [
                        note
                        for response in responses
                        for note in response.limitation_notes
                    ]
                    metadata = {
                        "requested_url": url,
                        "final_url": final_url,
                        "title": title,
                        "capture_timestamp": utc_now_z(),
                        "timeout_seconds": timeout_seconds,
                        "wait_until": wait_until,
                        "settle_seconds": settle_seconds,
                        "dom_observation_stage": "pre_lazy_load_scroll",
                        "post_load_action_executed": post_load_action_script is not None
                        or bool(pointer_action_receipts),
                        "post_load_pointer_action": pointer_action_receipt,
                        "post_load_pointer_actions": pointer_action_receipts,
                        "lazy_load_scroll_passes": lazy_load_scroll_passes,
                        "lazy_load_scroll_step_px": lazy_load_scroll_step_px,
                        "lazy_load_scroll_passes_executed": lazy_load_scroll_result.executed_passes,
                        "lazy_load_scroll_stop_reason": lazy_load_scroll_result.stop_reason,
                        "headless": headless,
                        "browser_channel": browser_channel,
                        "viewport_width": viewport_width,
                        "viewport_height": viewport_height,
                        "storage_state_loaded": storage_state_path is not None,
                        "blocked_resource_types": sorted(blocked_resource_types),
                        "max_response_bytes": max_response_bytes,
                        "response_count": len(responses),
                        **_proxy_metadata(proxy_profile),
                    }
                    return BrowserPageObservationSuccess(
                        requested_url=url,
                        final_url=final_url,
                        title=title,
                        visible_text=visible_text,
                        dom_observation=dom_observation,
                        responses=responses,
                        metadata=metadata,
                        warning_notes=warning_notes,
                        limitation_notes=limitation_notes,
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
        proxy_profile: ProxyProfile | None = None,
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
                launch_kwargs: dict[str, object] = {}
                if proxy_profile is not None:
                    launch_kwargs["proxy"] = _playwright_proxy_settings(proxy_profile)
                browser = playwright.chromium.launch(headless=True, **launch_kwargs)
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
                if proxy_profile is not None and proxy_profile.timezone is not None:
                    context_kwargs["timezone_id"] = proxy_profile.timezone
                if proxy_profile is not None and proxy_profile.locale is not None:
                    context_kwargs["locale"] = proxy_profile.locale
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
                        **_proxy_metadata(proxy_profile),
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


def _read_observed_page_responses(
    responses: Sequence[object],
    *,
    max_response_bytes: int,
) -> list[BrowserPageResponse]:
    preserved: list[BrowserPageResponse] = []
    seen: set[tuple[str, int]] = set()
    for response in responses:
        url = str(response.url)
        status = int(response.status)
        identity = (url, status)
        if identity in seen:
            continue
        seen.add(identity)
        headers = {
            str(key): str(value)
            for key, value in response.headers.items()
            if str(key).lower() not in {"set-cookie", "cookie"}
        }
        request_method, resource_type = _response_request_metadata(response)
        limitations: list[str] = []
        body_text = ""
        try:
            candidate = response.text()
        except Exception as exc:
            limitations.append(f"observed_response_body_unavailable: {type(exc).__name__}: {exc}")
        else:
            size = len(candidate.encode("utf-8"))
            if size > max_response_bytes:
                limitations.append(
                    f"observed_response_body_exceeded_cap: {size} > {max_response_bytes}; body omitted"
                )
            else:
                body_text = candidate
        preserved.append(
            BrowserPageResponse(
                requested_url=url,
                final_url=url,
                status=status,
                ok=bool(response.ok),
                body_text=body_text,
                response_headers=headers,
                limitation_notes=limitations,
                request_method=request_method,
                resource_type=resource_type,
            )
        )
    return preserved


def _response_request_metadata(response: object) -> tuple[str | None, str | None]:
    try:
        request = getattr(response, "request")
    except Exception:
        return None, None
    try:
        method = str(getattr(request, "method", "") or "").upper() or None
    except Exception:
        method = None
    try:
        resource_type = str(getattr(request, "resource_type", "") or "").lower() or None
    except Exception:
        resource_type = None
    return method, resource_type


_POINTER_ACTION_TARGET_SCRIPT = r"""
(args) => {
  const normalizeMarkers = (values) => Array.isArray(values)
    ? values.map((value) => String(value || '').trim().toLowerCase()).filter(Boolean)
    : [];
  const markers = normalizeMarkers(args.text_markers);
  const exactMarkers = normalizeMarkers(args.exact_text_markers);
  const pageTextMarkers = normalizeMarkers(args.page_text_markers);
  const preferTopRight = Boolean(args.prefer_top_right);
  const result = {
    candidate_count: 0,
    matched_count: 0,
    target_found: false,
    target_kind: null,
    box: null,
    page_text_gate_matched: pageTextMarkers.length === 0 ? null : false,
    selection_strategy: preferTopRight ? 'top_right' : 'first_match',
  };
  if (pageTextMarkers.length > 0) {
    const pageText = [
      document.title,
      document.body ? document.body.innerText : '',
    ].filter(Boolean).join(' ').toLowerCase();
    if (!pageTextMarkers.some((marker) => pageText.includes(marker))) {
      return result;
    }
    result.page_text_gate_matched = true;
  }
  const candidates = Array.from(document.querySelectorAll(String(args.candidate_selector || '')));
  result.candidate_count = candidates.length;
  let fallback = null;
  let priority = null;
  const matches = [];
  const candidateFromNode = (node) => {
    const rect = node.getBoundingClientRect();
    if (!rect || rect.width <= 0 || rect.height <= 0) {
      return null;
    }
    const tag = String(node.tagName || '').toLowerCase();
    const role = String(node.getAttribute('role') || '').toLowerCase();
    return {
      target_kind: tag === 'button' ? 'button' : role === 'button' ? 'role_button' : tag === 'a' ? 'link' : 'candidate',
      box: {
        x: rect.x,
        y: rect.y,
        width: rect.width,
        height: rect.height,
      },
    };
  };
  const textFieldsForNode = (node) => {
    const dataE2E = String(node.getAttribute('data-e2e') || '').toLowerCase();
    const fields = [
      node.getAttribute('aria-label'),
      node.getAttribute('title'),
      dataE2E,
      node.getAttribute('data-testid'),
      node.getAttribute('data-test-id'),
      node.getAttribute('class'),
      node.textContent,
    ].filter(Boolean).map((value) => String(value).trim().toLowerCase()).filter(Boolean);
    return {dataE2E, fields, joined: fields.join(' ')};
  };
  const markerMatches = (fields, joined) => {
    if (markers.some((marker) => joined.includes(marker))) {
      return true;
    }
    return exactMarkers.some((marker) => fields.some((field) => field === marker));
  };
  for (const node of candidates) {
    const {dataE2E, fields, joined} = textFieldsForNode(node);
    if (!markerMatches(fields, joined)) {
      continue;
    }
    result.matched_count += 1;
    const candidate = candidateFromNode(node);
    if (candidate === null) {
      continue;
    }
    matches.push(candidate);
    if (fallback === null) {
      fallback = candidate;
    }
    if (priority === null && dataE2E === 'comment-icon') {
      priority = candidate;
    }
  }
  let selected = priority || fallback;
  if (preferTopRight && matches.length > 0) {
    selected = matches.slice().sort((left, right) => {
      if (left.box.y !== right.box.y) {
        return left.box.y - right.box.y;
      }
      return right.box.x - left.box.x;
    })[0];
  }
  if (selected !== null) {
    result.target_found = true;
    result.target_kind = selected.target_kind;
    result.box = selected.box;
  }
  return result;
}
""".strip()


def _normalize_pointer_action(
    action: BrowserPagePointerAction | None,
) -> BrowserPagePointerAction | None:
    if action is None:
        return None
    action_name = action.action_name.strip()
    if not action_name:
        raise ValueError("post_load_pointer_action.action_name must not be blank")
    candidate_selector = action.candidate_selector.strip()
    if not candidate_selector:
        raise ValueError("post_load_pointer_action.candidate_selector must not be blank")
    text_markers = tuple(marker.strip().lower() for marker in action.text_markers if marker.strip())
    page_text_markers = tuple(
        marker.strip().lower() for marker in action.page_text_markers if marker.strip()
    )
    exact_text_markers = tuple(
        marker.strip().lower() for marker in action.exact_text_markers if marker.strip()
    )
    if not text_markers and not exact_text_markers:
        raise ValueError(
            "post_load_pointer_action text_markers or exact_text_markers must contain at least one marker"
        )
    if action.wait_after_ms < 0:
        raise ValueError("post_load_pointer_action.wait_after_ms must be zero or greater")
    if action.move_steps_min <= 0 or action.move_steps_max <= 0:
        raise ValueError("post_load_pointer_action move steps must be greater than zero")
    if action.move_steps_min > action.move_steps_max:
        raise ValueError("post_load_pointer_action.move_steps_min must be <= move_steps_max")
    if not 0.0 <= action.target_fraction_min <= 1.0:
        raise ValueError("post_load_pointer_action.target_fraction_min must be between 0 and 1")
    if not 0.0 <= action.target_fraction_max <= 1.0:
        raise ValueError("post_load_pointer_action.target_fraction_max must be between 0 and 1")
    if action.target_fraction_min > action.target_fraction_max:
        raise ValueError(
            "post_load_pointer_action.target_fraction_min must be <= target_fraction_max"
        )
    return BrowserPagePointerAction(
        action_name=action_name,
        candidate_selector=candidate_selector,
        text_markers=text_markers,
        page_text_markers=page_text_markers,
        exact_text_markers=exact_text_markers,
        wait_after_ms=action.wait_after_ms,
        move_steps_min=action.move_steps_min,
        move_steps_max=action.move_steps_max,
        target_fraction_min=action.target_fraction_min,
        target_fraction_max=action.target_fraction_max,
        prefer_top_right=bool(action.prefer_top_right),
        visual_top_right_x_fallback=bool(action.visual_top_right_x_fallback),
        random_seed=int(action.random_seed),
    )



def _normalize_pointer_actions(
    actions: Sequence[BrowserPagePointerAction],
) -> tuple[BrowserPagePointerAction, ...]:
    normalized: list[BrowserPagePointerAction] = []
    for action in actions:
        normalized_action = _normalize_pointer_action(action)
        if normalized_action is None:
            raise ValueError("post_load_pointer_actions entries must not be None")
        normalized.append(normalized_action)
    return tuple(normalized)


def _find_visual_top_right_x_target(page: object) -> dict[str, object]:
    result: dict[str, object] = {
        "target_found": False,
        "target_kind": "visual_x",
        "box": None,
        "visual_fallback_attempted": True,
        "visual_fallback_target_found": False,
        "visual_fallback_candidate_count": 0,
        "visual_fallback_confidence": None,
        "visual_fallback_screenshot_sha256": None,
        "visual_fallback_crop_box": None,
        "visual_fallback_failure": None,
    }
    try:
        screenshot_png = page.screenshot(full_page=False)
    except Exception:
        result["visual_fallback_failure"] = "visual_fallback_screenshot_failed"
        return result
    if not isinstance(screenshot_png, bytes) or not screenshot_png:
        result["visual_fallback_failure"] = "visual_fallback_empty_screenshot"
        return result
    result["visual_fallback_screenshot_sha256"] = sha256(screenshot_png).hexdigest()
    try:
        from PIL import Image
    except Exception:
        result["visual_fallback_failure"] = "visual_fallback_image_dependency_unavailable"
        return result
    try:
        image = Image.open(io.BytesIO(screenshot_png)).convert("L")
    except Exception:
        result["visual_fallback_failure"] = "visual_fallback_image_decode_failed"
        return result

    image_width, image_height = image.size
    if image_width <= 0 or image_height <= 0:
        result["visual_fallback_failure"] = "visual_fallback_invalid_image_size"
        return result
    crop_x = int(image_width * 0.45)
    crop_y = 0
    crop_width = image_width - crop_x
    crop_height = max(1, int(image_height * 0.35))
    result["visual_fallback_crop_box"] = {
        "x": crop_x,
        "y": crop_y,
        "width": crop_width,
        "height": crop_height,
    }
    candidates = _visual_x_candidates(image, crop_x, crop_y, crop_width, crop_height)
    result["visual_fallback_candidate_count"] = len(candidates)
    if not candidates:
        return result
    selected = max(candidates, key=lambda candidate: candidate["score"])
    result["target_found"] = True
    result["visual_fallback_target_found"] = True
    result["visual_fallback_confidence"] = round(float(selected["score"]), 3)
    result["box"] = {
        "x": float(selected["x"]),
        "y": float(selected["y"]),
        "width": float(selected["width"]),
        "height": float(selected["height"]),
    }
    return result


def _visual_x_candidates(
    image: object,
    crop_x: int,
    crop_y: int,
    crop_width: int,
    crop_height: int,
) -> list[dict[str, float]]:
    pixels = image.load()  # type: ignore[attr-defined]
    foreground_sets: list[set[tuple[int, int]]] = [set(), set()]
    x_end = crop_x + crop_width
    y_end = crop_y + crop_height
    for y in range(crop_y, y_end):
        for x in range(crop_x, x_end):
            try:
                value = int(pixels[x, y])
            except Exception:
                continue
            if value <= 96:
                foreground_sets[0].add((x, y))
            elif value >= 216:
                foreground_sets[1].add((x, y))

    candidates: list[dict[str, float]] = []
    for foreground_pixels in foreground_sets:
        visited: set[tuple[int, int]] = set()
        for seed in foreground_pixels:
            if seed in visited:
                continue
            stack = [seed]
            visited.add(seed)
            component: list[tuple[int, int]] = []
            while stack:
                x, y = stack.pop()
                component.append((x, y))
                for nx in (x - 1, x, x + 1):
                    for ny in (y - 1, y, y + 1):
                        if nx == x and ny == y:
                            continue
                        neighbor = (nx, ny)
                        if neighbor in visited or neighbor not in foreground_pixels:
                            continue
                        visited.add(neighbor)
                        stack.append(neighbor)
            candidate = _score_visual_x_component(
                component, crop_x, crop_y, crop_width, crop_height
            )
            if candidate is not None:
                candidates.append(candidate)
    return candidates


def _score_visual_x_component(
    component: list[tuple[int, int]],
    crop_x: int,
    crop_y: int,
    crop_width: int,
    crop_height: int,
) -> dict[str, float] | None:
    if len(component) < 12:
        return None
    xs = [point[0] for point in component]
    ys = [point[1] for point in component]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    if width < 8 or height < 8 or width > 44 or height > 44:
        return None
    ratio = width / height
    if ratio < 0.55 or ratio > 1.8:
        return None
    density = len(component) / float(width * height)
    if density < 0.08 or density > 0.65:
        return None
    diagonal_tolerance = 0.24
    main_diagonal = 0
    anti_diagonal = 0
    center = 0
    for x, y in component:
        nx = (x - min_x) / max(1, width - 1)
        ny = (y - min_y) / max(1, height - 1)
        if abs(nx - ny) <= diagonal_tolerance:
            main_diagonal += 1
        if abs((nx + ny) - 1.0) <= diagonal_tolerance:
            anti_diagonal += 1
        if 0.25 <= nx <= 0.75 and 0.25 <= ny <= 0.75:
            center += 1
    component_size = float(len(component))
    main_share = main_diagonal / component_size
    anti_share = anti_diagonal / component_size
    center_share = center / component_size
    if main_share < 0.22 or anti_share < 0.22 or center_share < 0.08:
        return None
    x_position = ((min_x + max_x) / 2.0 - crop_x) / max(1, crop_width)
    y_position = ((min_y + max_y) / 2.0 - crop_y) / max(1, crop_height)
    score = (
        min(main_share, anti_share)
        + (center_share * 0.35)
        + (x_position * 0.2)
        + ((1.0 - y_position) * 0.15)
    )
    padding = 4
    return {
        "x": float(max(0, min_x - padding)),
        "y": float(max(0, min_y - padding)),
        "width": float(width + padding * 2),
        "height": float(height + padding * 2),
        "score": score,
    }

def _run_pointer_action(page: object, action: BrowserPagePointerAction) -> dict[str, object]:
    receipt: dict[str, object] = {
        "action_name": action.action_name,
        "candidate_count": 0,
        "matched_count": 0,
        "target_found": False,
        "clicked": False,
        "move_steps": None,
        "wait_ms": 0,
        "target_kind": None,
        "page_text_gate_matched": None,
        "selection_strategy": None,
    }
    if action.visual_top_right_x_fallback:
        receipt["visual_fallback_attempted"] = False
    try:
        target = page.evaluate(
            _POINTER_ACTION_TARGET_SCRIPT,
            {
                "candidate_selector": action.candidate_selector,
                "text_markers": list(action.text_markers),
                "page_text_markers": list(action.page_text_markers),
                "exact_text_markers": list(action.exact_text_markers),
                "prefer_top_right": action.prefer_top_right,
            },
        )
    except Exception:
        receipt["failure"] = "pointer_action_lookup_failed"
        return receipt

    if not isinstance(target, dict):
        receipt["failure"] = "pointer_action_lookup_failed"
        return receipt
    receipt["candidate_count"] = _safe_int(target.get("candidate_count"), default=0)
    receipt["matched_count"] = _safe_int(target.get("matched_count"), default=0)
    receipt["target_found"] = bool(target.get("target_found"))
    target_kind = target.get("target_kind")
    if isinstance(target_kind, str) and target_kind:
        receipt["target_kind"] = target_kind
    page_text_gate_matched = target.get("page_text_gate_matched")
    if isinstance(page_text_gate_matched, bool):
        receipt["page_text_gate_matched"] = page_text_gate_matched
    selection_strategy = target.get("selection_strategy")
    if isinstance(selection_strategy, str) and selection_strategy:
        receipt["selection_strategy"] = selection_strategy
    box = target.get("box")
    if not receipt["target_found"] or not isinstance(box, dict):
        if action.visual_top_right_x_fallback and receipt.get("page_text_gate_matched") is not False:
            visual_target = _find_visual_top_right_x_target(page)
            for key in (
                "visual_fallback_attempted",
                "visual_fallback_target_found",
                "visual_fallback_candidate_count",
                "visual_fallback_confidence",
                "visual_fallback_screenshot_sha256",
                "visual_fallback_crop_box",
                "visual_fallback_failure",
            ):
                value = visual_target.get(key)
                if value is not None:
                    receipt[key] = value
            visual_box = visual_target.get("box")
            if bool(visual_target.get("target_found")) and isinstance(visual_box, dict):
                receipt["target_found"] = True
                receipt["target_kind"] = "visual_x"
                receipt["selection_strategy"] = "top_right_visual_x"
                box = visual_box
            else:
                return receipt
        else:
            return receipt

    try:
        x = float(box["x"])
        y = float(box["y"])
        width = float(box["width"])
        height = float(box["height"])
    except (KeyError, TypeError, ValueError):
        receipt["failure"] = "pointer_action_lookup_failed"
        return receipt
    if width <= 0 or height <= 0:
        receipt["failure"] = "pointer_action_lookup_failed"
        return receipt

    rng = random.Random(action.random_seed)
    click_x = x + width * rng.uniform(action.target_fraction_min, action.target_fraction_max)
    click_y = y + height * rng.uniform(action.target_fraction_min, action.target_fraction_max)
    move_steps = rng.randint(action.move_steps_min, action.move_steps_max)
    try:
        page.mouse.move(click_x, click_y, steps=move_steps)
        page.mouse.click(click_x, click_y)
        if action.wait_after_ms > 0:
            page.wait_for_timeout(action.wait_after_ms)
    except Exception:
        receipt["failure"] = "pointer_action_click_failed"
        return receipt
    receipt["clicked"] = True
    receipt["move_steps"] = move_steps
    receipt["wait_ms"] = action.wait_after_ms
    return receipt


def _safe_int(value: object, *, default: int) -> int:
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default

def _run_bounded_lazy_load_scrolls(
    page: object,
    *,
    scroll_passes: int,
    scroll_step_px: int,
) -> _LazyLoadScrollResult:
    executed = 0
    if scroll_passes <= 0:
        return _LazyLoadScrollResult(executed)
    bounded_passes = min(scroll_passes, _MAX_SCROLL_PASSES)
    capped = scroll_passes > _MAX_SCROLL_PASSES
    if scroll_step_px > 0:
        position = 0
        for _ in range(bounded_passes):
            height = int(page.evaluate("() => document.body.scrollHeight") or 0)
            if position >= height:
                return _LazyLoadScrollResult(executed, "page_end")
            position += scroll_step_px
            page.evaluate("(y) => window.scrollTo(0, y)", position)
            page.wait_for_timeout(_SCROLL_PASS_SETTLE_MS)
            executed += 1
        stop_reason = "capped_pass_limit" if capped else "requested_passes_complete"
        return _LazyLoadScrollResult(executed, stop_reason)

    for _ in range(bounded_passes):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(_SCROLL_PASS_SETTLE_MS)
        executed += 1
    stop_reason = "capped_pass_limit" if capped else "requested_passes_complete"
    return _LazyLoadScrollResult(executed, stop_reason)


def _playwright_proxy_settings(proxy_profile: ProxyProfile) -> dict[str, str]:
    endpoint = proxy_profile.proxy_endpoint
    parsed = urlparse(endpoint)
    if not parsed.scheme or not parsed.hostname:
        return {"server": endpoint}

    host = parsed.hostname
    if ":" in host and not host.startswith("["):
        host = f"[{host}]"
    netloc = f"{host}:{parsed.port}" if parsed.port is not None else host
    server = urlunparse((parsed.scheme, netloc, "", "", "", ""))
    settings = {"server": server}
    if parsed.username is not None:
        settings["username"] = unquote(parsed.username)
    if parsed.password is not None:
        settings["password"] = unquote(parsed.password)
    return settings


def _proxy_metadata(proxy_profile: ProxyProfile | None) -> dict[str, object]:
    return {
        "proxy_used": proxy_profile is not None,
        "proxy_category": proxy_profile.proxy_category.value if proxy_profile is not None else None,
        "proxy_disclosure": "category_only" if proxy_profile is not None else "none",
        "proxy_endpoint_recorded": False,
        "proxy_exit_ip_recorded": False,
        "proxy_timezone": proxy_profile.timezone if proxy_profile is not None else None,
        "proxy_locale": proxy_profile.locale if proxy_profile is not None else None,
    }


def _redact_proxy_secret(text: str, *, proxy_profile: ProxyProfile | None) -> str:
    if proxy_profile is None:
        return text
    endpoint = proxy_profile.proxy_endpoint
    redacted = text.replace(endpoint, "[redacted-proxy-endpoint]")
    parsed = urlparse(endpoint)
    if parsed.username:
        redacted = redacted.replace(parsed.username, "[redacted-proxy-credential]")
        redacted = redacted.replace(unquote(parsed.username), "[redacted-proxy-credential]")
    if parsed.password:
        redacted = redacted.replace(parsed.password, "[redacted-proxy-credential]")
        redacted = redacted.replace(unquote(parsed.password), "[redacted-proxy-credential]")
    host = parsed.hostname
    if host:
        if parsed.port is not None:
            redacted = redacted.replace(f"{host}:{parsed.port}", "[redacted-proxy-endpoint]")
        redacted = redacted.replace(host, "[redacted-proxy-endpoint]")
    return redacted


def _normalize_browser_channel(browser_channel: str | None) -> str | None:
    if browser_channel is None:
        return None
    normalized = browser_channel.strip()
    if not normalized:
        raise ValueError("browser_channel must not be blank")
    return normalized


def _validate_positive_number(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")


def _validate_positive_int(name: str, value: int) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")


def _failure_kind_from_exception(error: Exception) -> BrowserSnapshotFailureKind:
    text = f"{type(error).__name__}: {error}".lower()
    if _looks_like_environment_permission_denied(error):
        return BrowserSnapshotFailureKind.ENVIRONMENT_PERMISSION_DENIED
    if "timeout" in text or "timed out" in text or "aborterror" in text or "aborted" in text:
        return BrowserSnapshotFailureKind.TIMEOUT
    return BrowserSnapshotFailureKind.CAPTURE_FAILED


def _capture_failure_message(
    prefix: str,
    error: Exception,
    *,
    proxy_profile: ProxyProfile | None,
) -> str:
    if _looks_like_environment_permission_denied(error):
        return (
            f"{prefix}: browser subprocess startup was denied by the local execution "
            "environment. Run this browser capture from an environment that permits "
            "Playwright/Chromium subprocesses; the failure happened before source access."
        )
    return _redact_proxy_secret(f"{prefix}: {error}", proxy_profile=proxy_profile)


def _looks_like_environment_permission_denied(error: Exception) -> bool:
    text = f"{type(error).__name__}: {error}".lower()
    return isinstance(error, PermissionError) or "winerror 5" in text or "access is denied" in text


def _looks_like_missing_browser_binary(error: Exception) -> bool:
    text = f"{type(error).__name__}: {error}".lower()
    return (
        "executable doesn't exist" in text
        or "browser has not been installed" in text
        or "playwright install" in text
    )
