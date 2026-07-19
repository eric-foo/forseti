from __future__ import annotations

import io
import random
import time
from contextlib import nullcontext
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
BROWSER_BACKEND_PLAYWRIGHT = "playwright"
BROWSER_BACKEND_CLOAKBROWSER = "cloakbrowser"
BROWSER_BACKEND_CHROME_CDP = "chrome_cdp"
ALLOWED_BROWSER_BACKENDS = {
    BROWSER_BACKEND_PLAYWRIGHT,
    BROWSER_BACKEND_CLOAKBROWSER,
    BROWSER_BACKEND_CHROME_CDP,
}
DEFAULT_HUMAN_CHALLENGE_HANDOFF_TIMEOUT_SECONDS = 180.0
PAGE_LOAD_BEFORE_POINTER_ACTIONS_HANDOFF_NAME = "page_load_before_pointer_actions_v0"
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
    prefer_smallest_match: bool = False
    visual_top_right_x_fallback: bool = False
    visual_x_target_zone: str = "top_right"
    visual_x_geometric_fallback: bool = True
    post_click_absent_text_markers: tuple[str, ...] = ()
    post_click_visual_target_absence_check: bool = False
    stop_sequence_on_failed_post_click_verification: bool = False
    stop_wait_on_observed_response: bool = False
    stop_sequence_on_observed_response: bool = False
    observed_response_wait_poll_ms: int = 100
    random_seed: int | None = None


@dataclass(frozen=True)
class BrowserPageWheelAction:
    action_name: str
    direction: str
    viewport_fraction_min: float = 0.65
    viewport_fraction_max: float = 0.90
    wheel_chunk_px_min: int = 20
    wheel_chunk_px_max: int = 40
    wheel_pause_ms_min: int = 8
    wheel_pause_ms_max: int = 20
    settle_ms_min: int = 400
    settle_ms_max: int = 800
    cursor_fraction_min: float = 0.30
    cursor_fraction_max: float = 0.70
    random_seed: int | None = None


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


BrowserPageResponseStopCondition: TypeAlias = Callable[
    [Sequence[BrowserPageResponse]], bool
]


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
        post_load_wheel_action: BrowserPageWheelAction | None = None,
        post_load_pointer_action: BrowserPagePointerAction | None = None,
        post_load_pointer_actions: Sequence[BrowserPagePointerAction] = (),
        selector: str | None = None,
        selector_timeout_seconds: float = 5.0,
        max_response_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
        settle_seconds: float = 0.0,
        lazy_load_scroll_passes: int = 0,
        lazy_load_scroll_step_px: int = 0,
        lazy_load_response_stop_condition: BrowserPageResponseStopCondition | None = None,
        dom_extract_after_lazy_load: bool = False,
        block_resource_types: Sequence[str] = (),
        proxy_profile: ProxyProfile | None = None,
        storage_state_path: Path | None = None,
        headless: bool = True,
        browser_channel: str | None = None,
        force_same_url_reload: bool = False,
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
    post_load_wheel_action: BrowserPageWheelAction | None = None,
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
    lazy_load_response_stop_condition: BrowserPageResponseStopCondition | None = None,
    dom_extract_after_lazy_load: bool = False,
    selector: str | None = None,
    selector_timeout_seconds: float = 5.0,
    block_resource_types: Sequence[str] = (),
    proxy_profile: ProxyProfile | None = None,
    storage_state_path: Path | None = None,
    headless: bool = True,
    browser_channel: str | None = None,
    browser_backend: str = BROWSER_BACKEND_PLAYWRIGHT,
    force_same_url_reload: bool = False,
    cloakbrowser_humanize: bool = False,
    human_challenge_handoff_markers: Sequence[str] = (),
    human_challenge_handoff_after_action_names: Sequence[str] = (),
    human_challenge_handoff_timeout_seconds: float = DEFAULT_HUMAN_CHALLENGE_HANDOFF_TIMEOUT_SECONDS,
    human_challenge_handoff_prompt: str | None = None,
    engine: BrowserPageObservationEngine | None = None,
) -> BrowserPageObservationResult:
    """Capture a rendered page observation plus selected same-load responses."""
    normalized_url = _validate_http_url(url)
    normalized_browser_channel = _normalize_browser_channel(browser_channel)
    normalized_browser_backend = _normalize_browser_backend(browser_backend)
    normalized_handoff_markers = _normalize_lower_text_tuple(
        human_challenge_handoff_markers,
        name="human_challenge_handoff_markers",
    )
    normalized_handoff_action_names = _normalize_name_tuple(
        human_challenge_handoff_after_action_names,
        name="human_challenge_handoff_after_action_names",
    )
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
    if human_challenge_handoff_timeout_seconds < 0:
        raise ValueError("human_challenge_handoff_timeout_seconds must be zero or greater")
    if (
        normalized_browser_backend == BROWSER_BACKEND_CLOAKBROWSER
        and normalized_browser_channel is not None
    ):
        raise ValueError("browser_channel is not supported with browser_backend='cloakbrowser'")
    if force_same_url_reload and normalized_browser_backend != BROWSER_BACKEND_CHROME_CDP:
        raise ValueError(
            "force_same_url_reload is supported only with browser_backend='chrome_cdp'"
        )
    if post_load_action_script is not None and not post_load_action_script.strip():
        raise ValueError("post_load_action_script must not be blank")
    normalized_pointer_action = _normalize_pointer_action(post_load_pointer_action)
    normalized_pointer_actions = _normalize_pointer_actions(post_load_pointer_actions)
    normalized_wheel_action = _normalize_wheel_action(post_load_wheel_action)
    if normalized_pointer_action is not None and normalized_pointer_actions:
        raise ValueError(
            "post_load_pointer_action and post_load_pointer_actions are mutually exclusive"
        )
    configured_post_load_action_count = sum(
        (
            post_load_action_script is not None,
            normalized_wheel_action is not None,
            normalized_pointer_action is not None or bool(normalized_pointer_actions),
        )
    )
    if configured_post_load_action_count > 1:
        raise ValueError(
            "post-load script, wheel, and pointer actions are mutually exclusive"
        )
    if wait_until not in ALLOWED_WAIT_UNTIL:
        allowed = ", ".join(sorted(ALLOWED_WAIT_UNTIL))
        raise ValueError(f"wait_until must be one of: {allowed}")

    if engine is not None:
        observation_engine = engine
    elif normalized_browser_backend == BROWSER_BACKEND_CHROME_CDP:
        raise ValueError(
            "browser_backend='chrome_cdp' requires an explicit session engine; "
            "it is never auto-constructed so a missing engine fails loudly "
            "instead of silently launching a disposable browser"
        )
    elif normalized_browser_backend == BROWSER_BACKEND_CLOAKBROWSER:
        observation_engine = _CloakBrowserPageObservationEngine(
            cloakbrowser_humanize=cloakbrowser_humanize,
            human_challenge_handoff_markers=normalized_handoff_markers,
            human_challenge_handoff_after_action_names=normalized_handoff_action_names,
            human_challenge_handoff_timeout_seconds=human_challenge_handoff_timeout_seconds,
            human_challenge_handoff_prompt=human_challenge_handoff_prompt,
        )
    else:
        observation_engine = _PlaywrightBrowserSnapshotEngine(
            human_challenge_handoff_markers=normalized_handoff_markers,
            human_challenge_handoff_after_action_names=normalized_handoff_action_names,
            human_challenge_handoff_timeout_seconds=human_challenge_handoff_timeout_seconds,
            human_challenge_handoff_prompt=human_challenge_handoff_prompt,
        )
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
            post_load_wheel_action=normalized_wheel_action,
            post_load_pointer_action=normalized_pointer_action,
            post_load_pointer_actions=normalized_pointer_actions,
            selector=selector,
            selector_timeout_seconds=selector_timeout_seconds,
            max_response_bytes=max_response_bytes,
            settle_seconds=settle_seconds,
            lazy_load_scroll_passes=lazy_load_scroll_passes,
            lazy_load_scroll_step_px=lazy_load_scroll_step_px,
            lazy_load_response_stop_condition=lazy_load_response_stop_condition,
            dom_extract_after_lazy_load=dom_extract_after_lazy_load,
            block_resource_types=tuple(block_resource_types),
            proxy_profile=proxy_profile,
            storage_state_path=storage_state_path,
            headless=headless,
            browser_channel=normalized_browser_channel,
            **(
                {"force_same_url_reload": True}
                if force_same_url_reload
                else {}
            ),
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
    def __init__(
        self,
        *,
        browser_backend: str = BROWSER_BACKEND_PLAYWRIGHT,
        cloakbrowser_humanize: bool = False,
        pre_action_stop_markers: Sequence[str] = (),
        human_challenge_handoff_markers: Sequence[str] = (),
        human_challenge_handoff_after_action_names: Sequence[str] = (),
        human_challenge_handoff_timeout_seconds: float = DEFAULT_HUMAN_CHALLENGE_HANDOFF_TIMEOUT_SECONDS,
        human_challenge_handoff_prompt: str | None = None,
    ) -> None:
        self.browser_backend = browser_backend
        self.cloakbrowser_humanize = bool(cloakbrowser_humanize)
        self.pre_action_stop_markers = tuple(
            marker.strip().lower() for marker in pre_action_stop_markers if marker.strip()
        )
        self.human_challenge_handoff_markers = tuple(human_challenge_handoff_markers)
        self.human_challenge_handoff_after_action_names = tuple(
            human_challenge_handoff_after_action_names
        )
        self.human_challenge_handoff_timeout_seconds = human_challenge_handoff_timeout_seconds
        self.human_challenge_handoff_prompt = human_challenge_handoff_prompt

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

    def _launch_page_observation_browser(
        self,
        *,
        playwright: object,
        proxy_profile: ProxyProfile | None,
        headless: bool,
        browser_channel: str | None,
    ) -> object:
        launch_kwargs: dict[str, object] = {}
        if proxy_profile is not None:
            launch_kwargs["proxy"] = _playwright_proxy_settings(proxy_profile)
        if browser_channel is not None:
            launch_kwargs["channel"] = browser_channel
        return playwright.chromium.launch(headless=headless, **launch_kwargs)

    def _should_run_human_challenge_handoff_after_action(self, action_name: str) -> bool:
        if not self.human_challenge_handoff_markers:
            return False
        if not self.human_challenge_handoff_after_action_names:
            return True
        return action_name in self.human_challenge_handoff_after_action_names

    def _open_page_observation_runtime(self) -> object:
        """Return a context manager yielding the runtime handle passed to
        ``_launch_page_observation_browser`` (the Playwright driver here;
        engines that own their runtime yield ``None``)."""
        try:
            sync_api = import_module("playwright.sync_api")
        except ModuleNotFoundError as exc:
            raise _BrowserSnapshotDependencyUnavailable(
                "Playwright is not installed. Install the browser optional dependency before running browser page observations."
            ) from exc
        return sync_api.sync_playwright()

    def _page_observation_missing_browser_binary_message(self) -> str:
        """Dependency-unavailable message when the page-observation browser
        launch fails with a missing browser binary."""
        return (
            "Playwright Chromium browser binary is not installed. "
            "Run `python -m playwright install chromium` before running browser page observations."
        )

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
        post_load_wheel_action: BrowserPageWheelAction | None = None,
        post_load_pointer_action: BrowserPagePointerAction | None = None,
        post_load_pointer_actions: Sequence[BrowserPagePointerAction] = (),
        selector: str | None = None,
        selector_timeout_seconds: float = 5.0,
        max_response_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
        settle_seconds: float = 0.0,
        lazy_load_scroll_passes: int = 0,
        lazy_load_scroll_step_px: int = 0,
        lazy_load_response_stop_condition: BrowserPageResponseStopCondition | None = None,
        dom_extract_after_lazy_load: bool = False,
        block_resource_types: Sequence[str] = (),
        proxy_profile: ProxyProfile | None = None,
        storage_state_path: Path | None = None,
        headless: bool = True,
        browser_channel: str | None = None,
        force_same_url_reload: bool = False,
    ) -> BrowserPageObservationSuccess:
        del force_same_url_reload
        page_observation_runtime = self._open_page_observation_runtime()

        timeout_ms = timeout_seconds * 1000
        selector_timeout_ms = selector_timeout_seconds * 1000
        blocked_resource_types = set(block_resource_types)
        selected_responses: list[object] = []
        with page_observation_runtime as playwright:
            try:
                browser = self._launch_page_observation_browser(
                    playwright=playwright,
                    proxy_profile=proxy_profile,
                    headless=headless,
                    browser_channel=browser_channel,
                )
            except Exception as exc:
                if _looks_like_missing_browser_binary(exc):
                    raise _BrowserSnapshotDependencyUnavailable(
                        self._page_observation_missing_browser_binary_message()
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
                    wheel_action_receipt: dict[str, object] | None = None
                    pre_action_stop_receipts: list[dict[str, object]] = []

                    def maybe_stop_before_action(after_action_name: str) -> bool:
                        receipt = _pre_action_stop_marker_receipt(
                            page,
                            markers=self.pre_action_stop_markers,
                            after_action_name=after_action_name,
                        )
                        if receipt is None:
                            return False
                        pre_action_stop_receipts.append(receipt)
                        warning_notes.append(
                            "browser_page_observation terminal account-safety marker "
                            "suppressed scripted actions"
                        )
                        return True
                    human_challenge_handoff_receipts: list[dict[str, object]] = []

                    def maybe_run_handoff(after_action_name: str) -> bool:
                        if not self._should_run_human_challenge_handoff_after_action(
                            after_action_name
                        ):
                            return False
                        handoff_receipt = _run_human_challenge_handoff(
                            page,
                            markers=self.human_challenge_handoff_markers,
                            timeout_seconds=self.human_challenge_handoff_timeout_seconds,
                            prompt=self.human_challenge_handoff_prompt,
                        )
                        if handoff_receipt is None:
                            return False
                        handoff_receipt["after_action_name"] = after_action_name
                        human_challenge_handoff_receipts.append(handoff_receipt)
                        if handoff_receipt.get("cleared") is True:
                            return False
                        warning_notes.append(
                            "browser_page_observation human challenge handoff did not clear visible markers"
                        )
                        return True

                    pointer_actions_suppressed_by_pre_action_stop = (
                        maybe_stop_before_action(
                            PAGE_LOAD_BEFORE_POINTER_ACTIONS_HANDOFF_NAME
                        )
                    )
                    pointer_actions_suppressed = (
                        pointer_actions_suppressed_by_pre_action_stop
                        or maybe_run_handoff(PAGE_LOAD_BEFORE_POINTER_ACTIONS_HANDOFF_NAME)
                    )
                    if pointer_actions_suppressed:
                        warning_notes.append(
                            "browser_page_observation scripted actions suppressed pending owner challenge clearance"
                        )
                    else:
                        if post_load_action_script is not None:
                            page.evaluate(post_load_action_script, post_load_action_arg)
                        if post_load_wheel_action is not None:
                            wheel_action_receipt = _run_wheel_action(
                                page, post_load_wheel_action
                            )
                        observed_response_count = lambda: len(selected_responses)
                        if post_load_pointer_action is not None:
                            pointer_action_receipt = _run_pointer_action(
                                page,
                                post_load_pointer_action,
                                observed_response_count=observed_response_count,
                            )
                            pointer_action_receipts.append(pointer_action_receipt)
                            pointer_actions_suppressed = (
                                maybe_stop_before_action(post_load_pointer_action.action_name)
                                or maybe_run_handoff(post_load_pointer_action.action_name)
                            )
                        for pointer_action in post_load_pointer_actions:
                            pointer_action_receipt = _run_pointer_action(
                                page,
                                pointer_action,
                                observed_response_count=observed_response_count,
                            )
                            pointer_action_receipts.append(pointer_action_receipt)
                            if maybe_stop_before_action(pointer_action.action_name):
                                pointer_actions_suppressed = True
                                break
                            if maybe_run_handoff(pointer_action.action_name):
                                pointer_actions_suppressed = True
                                break
                            if _should_stop_pointer_action_sequence(
                                pointer_action, pointer_action_receipt
                            ):
                                break
                    try:
                        visible_text = page.locator("body").inner_text(timeout=timeout_ms)
                    except Exception as exc:
                        visible_text = ""
                        warning_notes.append(
                            f"browser_page_observation visible_text extraction failed: {exc}"
                        )
                    def response_stop_reached() -> bool:
                        if lazy_load_response_stop_condition is None:
                            return False
                        try:
                            observed = _read_observed_page_responses(
                                selected_responses,
                                max_response_bytes=max_response_bytes,
                            )
                            return bool(lazy_load_response_stop_condition(observed))
                        except Exception as exc:
                            warning_notes.append(
                                f"browser_page_observation response stop check failed: {exc}"
                            )
                            return False

                    dom_observation: object = None
                    if not dom_extract_after_lazy_load:
                        dom_observation = page.evaluate(dom_extract_script, dom_extract_arg)
                    if pointer_actions_suppressed:
                        lazy_load_scroll_result = _LazyLoadScrollResult(
                            executed_passes=0,
                            stop_reason="scripted_actions_suppressed",
                        )
                    else:
                        lazy_load_scroll_result = _run_bounded_lazy_load_scrolls(
                            page,
                            scroll_passes=lazy_load_scroll_passes,
                            scroll_step_px=lazy_load_scroll_step_px,
                            stop_condition=response_stop_reached,
                        )
                    if dom_extract_after_lazy_load:
                        dom_observation = page.evaluate(dom_extract_script, dom_extract_arg)
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
                        "dom_observation_stage": (
                            "post_lazy_load_scroll"
                            if dom_extract_after_lazy_load
                            else "pre_lazy_load_scroll"
                        ),
                        "post_load_action_executed": post_load_action_script is not None
                        or wheel_action_receipt is not None
                        or bool(pointer_action_receipts),
                        "post_load_wheel_action": wheel_action_receipt,
                        "post_load_pointer_action": pointer_action_receipt,
                        "post_load_pointer_actions": pointer_action_receipts,
                        "lazy_load_scroll_passes": lazy_load_scroll_passes,
                        "lazy_load_scroll_step_px": lazy_load_scroll_step_px,
                        "lazy_load_scroll_passes_executed": lazy_load_scroll_result.executed_passes,
                        "lazy_load_scroll_stop_reason": lazy_load_scroll_result.stop_reason,
                        "lazy_load_response_stop_condition_configured": lazy_load_response_stop_condition is not None,
                        "headless": headless,
                        "browser_channel": browser_channel,
                        "browser_backend": self.browser_backend,
                        "cloakbrowser_humanize": (
                            self.cloakbrowser_humanize
                            if self.browser_backend == BROWSER_BACKEND_CLOAKBROWSER
                            else False
                        ),
                        "human_challenge_handoff_marker_count": len(
                            self.human_challenge_handoff_markers
                        ),
                        "human_challenge_handoff_after_action_names": list(
                            self.human_challenge_handoff_after_action_names
                        ),
                        "human_challenge_handoff_timeout_seconds": (
                            self.human_challenge_handoff_timeout_seconds
                        ),
                        "human_challenge_handoff_attempts": human_challenge_handoff_receipts,
                        "pre_action_stop_marker_count": len(self.pre_action_stop_markers),
                        "pre_action_stop_attempts": pre_action_stop_receipts,
                        "pointer_actions_suppressed_by_pre_action_stop": bool(
                            pre_action_stop_receipts
                        ),
                        "viewport_width": viewport_width,
                        "viewport_height": viewport_height,
                        "pointer_actions_suppressed_by_human_challenge_handoff": (
                            pointer_actions_suppressed and bool(human_challenge_handoff_receipts)
                        ),
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


class _CloakBrowserPageObservationEngine(_PlaywrightBrowserSnapshotEngine):
    def __init__(
        self,
        *,
        cloakbrowser_humanize: bool = False,
        pre_action_stop_markers: Sequence[str] = (),
        human_challenge_handoff_markers: Sequence[str] = (),
        human_challenge_handoff_after_action_names: Sequence[str] = (),
        human_challenge_handoff_timeout_seconds: float = DEFAULT_HUMAN_CHALLENGE_HANDOFF_TIMEOUT_SECONDS,
        human_challenge_handoff_prompt: str | None = None,
    ) -> None:
        super().__init__(
            browser_backend=BROWSER_BACKEND_CLOAKBROWSER,
            cloakbrowser_humanize=cloakbrowser_humanize,
            pre_action_stop_markers=pre_action_stop_markers,
            human_challenge_handoff_markers=human_challenge_handoff_markers,
            human_challenge_handoff_after_action_names=human_challenge_handoff_after_action_names,
            human_challenge_handoff_timeout_seconds=human_challenge_handoff_timeout_seconds,
            human_challenge_handoff_prompt=human_challenge_handoff_prompt,
        )

    def capture(self, **_: object) -> BrowserSnapshotEngineResult:
        raise NotImplementedError(
            "CloakBrowser supports page observation only; browser snapshot capture "
            "would otherwise run through the Playwright engine."
        )

    def capture_context_responses(self, **_: object) -> BrowserContextResponsesSuccess:
        raise NotImplementedError(
            "CloakBrowser supports page observation only; browser context responses "
            "would otherwise run through the Playwright engine."
        )

    def _open_page_observation_runtime(self) -> object:
        return nullcontext()

    def _page_observation_missing_browser_binary_message(self) -> str:
        return (
            "CloakBrowser could not launch its browser binary. "
            "Reinstall or repair the CloakBrowser browser runtime before running CloakBrowser page observations."
        )

    def _launch_page_observation_browser(
        self,
        *,
        playwright: object,
        proxy_profile: ProxyProfile | None,
        headless: bool,
        browser_channel: str | None,
    ) -> object:
        del playwright
        if browser_channel is not None:
            raise ValueError("browser_channel is not supported with browser_backend='cloakbrowser'")
        try:
            cloakbrowser = import_module("cloakbrowser")
        except ModuleNotFoundError as exc:
            raise _BrowserSnapshotDependencyUnavailable(
                "CloakBrowser is not installed. Install cloakbrowser before running CloakBrowser page observations."
            ) from exc
        launch_kwargs: dict[str, object] = {
            "headless": headless,
            "stealth_args": True,
            "humanize": self.cloakbrowser_humanize,
        }
        if proxy_profile is not None:
            launch_kwargs["proxy"] = _playwright_proxy_settings(proxy_profile)
            if proxy_profile.timezone is not None:
                launch_kwargs["timezone"] = proxy_profile.timezone
            if proxy_profile.locale is not None:
                launch_kwargs["locale"] = proxy_profile.locale
        return cloakbrowser.launch(**launch_kwargs)


class ChromeCdpPageObservationSessionEngine(_CloakBrowserPageObservationEngine):
    """Attach to one operator-owned local Chrome process without closing it."""

    def __init__(
        self,
        *,
        cdp_endpoint: str = "http://127.0.0.1:9222",
        pre_action_stop_markers: Sequence[str] = (),
        human_challenge_handoff_markers: Sequence[str] = (),
        human_challenge_handoff_after_action_names: Sequence[str] = (),
        human_challenge_handoff_timeout_seconds: float = DEFAULT_HUMAN_CHALLENGE_HANDOFF_TIMEOUT_SECONDS,
        human_challenge_handoff_prompt: str | None = None,
        humanize_context_fn: Callable[[object], None] | None = None,
        monotonic_fn: Callable[[], float] = time.monotonic,
    ) -> None:
        super().__init__(
            cloakbrowser_humanize=False,
            pre_action_stop_markers=pre_action_stop_markers,
            human_challenge_handoff_markers=human_challenge_handoff_markers,
            human_challenge_handoff_after_action_names=human_challenge_handoff_after_action_names,
            human_challenge_handoff_timeout_seconds=human_challenge_handoff_timeout_seconds,
            human_challenge_handoff_prompt=human_challenge_handoff_prompt,
        )
        parsed = urlparse(cdp_endpoint)
        if (
            parsed.scheme not in {"http", "https"}
            or parsed.username is not None
            or parsed.password is not None
            or parsed.hostname not in {"localhost", "127.0.0.1", "::1"}
        ):
            raise ValueError(
                "cdp_endpoint must be a credential-free loopback http(s) URL"
            )
        self.browser_backend = BROWSER_BACKEND_CHROME_CDP
        self.cdp_endpoint = parsed.geturl()
        self._playwright_owner: object | None = None
        self._real_browser: object | None = None
        self._real_context: object | None = None
        self._real_page: object | None = None
        self._launch_settings: tuple[ProxyProfile | None, bool, str | None] | None = None
        self._humanize_context_fn = humanize_context_fn
        self._context_settings: dict[str, object] | None = None
        self._closed = False
        self._pending_requested_page_url: str | None = None
        self._initial_page_count: int | None = None
        self._initial_platform_match_count: int | None = None
        self._initial_exact_match_count: int | None = None
        self._adopted_page_enumeration_index_or_none: int | None = None
        self._page_adoption_count = 0
        self._page_creation_count = 0
        self._page_navigation_count = 0
        self._page_reload_count = 0
        self._same_url_navigation_suppression_count = 0
        self._force_same_url_reload = False
        self._capture_attempt_count = 0
        self._capture_success_count = 0
        self._monotonic_fn = monotonic_fn
        self._capture_elapsed_seconds_total = 0.0
        self._capture_elapsed_seconds_max = 0.0
        self._capture_timings: list[dict[str, object]] = []

    def capture_page_observation(self, **kwargs: object) -> BrowserPageObservationSuccess:
        if self._closed:
            raise RuntimeError("Chrome CDP page-observation session is already closed")
        requested_url = kwargs.get("url")
        force_same_url_reload = kwargs.pop("force_same_url_reload", False)
        if not isinstance(force_same_url_reload, bool):
            raise ValueError("force_same_url_reload must be a boolean")
        self._force_same_url_reload = force_same_url_reload
        if self._real_page is None and isinstance(requested_url, str):
            self._pending_requested_page_url = requested_url
        self._capture_attempt_count += 1
        capture_index = self._capture_attempt_count
        capture_started = self._monotonic_fn()
        try:
            result = super().capture_page_observation(**kwargs)
        except Exception:
            self._record_capture_timing(
                capture_index=capture_index,
                requested_url=requested_url,
                final_url=None,
                kwargs=kwargs,
                elapsed_seconds=max(0.0, self._monotonic_fn() - capture_started),
                outcome="failed",
            )
            raise
        finally:
            self._force_same_url_reload = False
        self._capture_success_count += 1
        capture_elapsed_seconds = max(
            0.0, self._monotonic_fn() - capture_started
        )
        self._record_capture_timing(
            capture_index=capture_index,
            requested_url=requested_url,
            final_url=result.final_url,
            kwargs=kwargs,
            elapsed_seconds=capture_elapsed_seconds,
            outcome="success",
        )
        result.metadata.update(
            {
                "session_capture_index": capture_index,
                "session_capture_elapsed_seconds": round(
                    capture_elapsed_seconds, 6
                ),
                "page_acquisition_policy": "adopt_same_platform_else_create",
                "initial_platform_match_count": self._initial_platform_match_count,
                "initial_exact_match_count": self._initial_exact_match_count,
                "page_adoption_count": self._page_adoption_count,
                "page_creation_count": self._page_creation_count,
                "page_navigation_count": self._page_navigation_count,
                "page_reload_count": self._page_reload_count,
                "same_url_navigation_suppression_count": (
                    self._same_url_navigation_suppression_count
                ),
                "humanized_pointer_layer": (
                    "cloakbrowser.patch_context(resolve_config('careful'))"
                ),
                "outer_move_steps_semantics": (
                    "BrowserPagePointerAction routing input; not the internal "
                    "CloakBrowser humanized pointer path"
                ),
            }
        )
        return result

    def _record_capture_timing(
        self,
        *,
        capture_index: int,
        requested_url: object,
        final_url: str | None,
        kwargs: dict[str, object],
        elapsed_seconds: float,
        outcome: str,
    ) -> None:
        self._capture_elapsed_seconds_total += elapsed_seconds
        self._capture_elapsed_seconds_max = max(
            self._capture_elapsed_seconds_max, elapsed_seconds
        )
        action_names: list[str] = []
        wheel_action = kwargs.get("post_load_wheel_action")
        if isinstance(wheel_action, BrowserPageWheelAction):
            action_names.append(wheel_action.action_name)
        pointer_action = kwargs.get("post_load_pointer_action")
        if isinstance(pointer_action, BrowserPagePointerAction):
            action_names.append(pointer_action.action_name)
        pointer_actions = kwargs.get("post_load_pointer_actions")
        if isinstance(pointer_actions, Sequence):
            action_names.extend(
                action.action_name
                for action in pointer_actions
                if isinstance(action, BrowserPagePointerAction)
            )
        if kwargs.get("post_load_action_script") is not None:
            action_names.append("post_load_action_script")
        self._capture_timings.append(
            {
                "capture_index": capture_index,
                "requested_url_or_none": (
                    requested_url if isinstance(requested_url, str) else None
                ),
                "final_url_or_none": final_url,
                "action_names": action_names,
                "settle_seconds": kwargs.get("settle_seconds", 0.0),
                "elapsed_seconds": round(elapsed_seconds, 6),
                "outcome": outcome,
            }
        )

    def capture_current_viewport_png(self, *, timeout_seconds: float) -> bytes:
        """Capture a real PNG from the page retained by this CDP session."""

        if self._closed:
            raise RuntimeError("Chrome CDP page-observation session is already closed")
        if self._real_page is None:
            raise RuntimeError("Chrome CDP page observation must complete before screenshot capture")
        screenshot = self._real_page.screenshot(  # type: ignore[attr-defined]
            type="png",
            full_page=False,
            timeout=timeout_seconds * 1000,
        )
        if not isinstance(screenshot, bytes) or not screenshot:
            raise RuntimeError("Chrome CDP viewport screenshot returned no bytes")
        return screenshot

    def _launch_page_observation_browser(
        self,
        *,
        playwright: object,
        proxy_profile: ProxyProfile | None,
        headless: bool,
        browser_channel: str | None,
    ) -> object:
        del playwright
        if proxy_profile is not None:
            raise ValueError("Chrome CDP attach does not accept a harness proxy profile")
        if browser_channel is not None:
            raise ValueError("browser_channel is not supported with Chrome CDP attach")
        settings = (proxy_profile, headless, browser_channel)
        if self._launch_settings is None:
            try:
                sync_api = import_module("playwright.sync_api")
            except ModuleNotFoundError as exc:
                raise _BrowserSnapshotDependencyUnavailable(
                    "Playwright is required for Chrome CDP attachment."
                ) from exc
            self._playwright_owner = sync_api.sync_playwright().start()
            self._real_browser = self._playwright_owner.chromium.connect_over_cdp(  # type: ignore[attr-defined]
                self.cdp_endpoint
            )
            self._launch_settings = settings
        elif settings != self._launch_settings:
            raise ValueError("Chrome CDP launch settings changed mid-session")
        return _SessionBrowserProxy(self)

    def _new_scoped_context(self, context_kwargs: dict[str, object]) -> object:
        normalized = {
            key: value
            for key, value in context_kwargs.items()
            if key not in {"storage_state", "viewport"}
        }
        if self._real_browser is None:
            raise RuntimeError("Chrome CDP browser was not attached")
        if self._real_context is None:
            contexts = list(getattr(self._real_browser, "contexts", ()))
            if not contexts:
                raise RuntimeError("Chrome CDP browser exposed no persistent context")
            self._real_context = contexts[0]
            if self._humanize_context_fn is not None:
                self._humanize_context_fn(self._real_context)
            else:
                try:
                    from cloakbrowser.human import patch_context
                    from cloakbrowser.human.config import resolve_config

                    patch_context(self._real_context, resolve_config("careful", None))
                except ModuleNotFoundError as exc:
                    raise _BrowserSnapshotDependencyUnavailable(
                        "CloakBrowser human input support is required for Chrome CDP capture."
                    ) from exc
            self._context_settings = normalized
        elif normalized != self._context_settings:
            raise ValueError("Chrome CDP context settings changed mid-session")
        return _SessionContextProxy(self)

    def _get_or_create_page(self) -> object:
        if self._real_context is None:
            raise RuntimeError("Chrome CDP context was not acquired")
        if self._real_page is not None:
            is_closed = getattr(self._real_page, "is_closed", None)
            if callable(is_closed) and is_closed():
                self._real_page = None
        if self._real_page is None:
            if self._initial_platform_match_count is None:
                requested_identity = _normalized_tiktok_target_identity(
                    self._pending_requested_page_url
                )
                requested_is_tiktok = _is_tiktok_platform_url(
                    self._pending_requested_page_url
                )
                enumerated_pages = list(getattr(self._real_context, "pages", ()))
                self._initial_page_count = len(enumerated_pages)
                platform_matches: list[tuple[int, object]] = []
                exact_matches: list[tuple[int, object]] = []
                for index, page in enumerate(enumerated_pages):
                    is_closed = getattr(page, "is_closed", None)
                    if callable(is_closed) and is_closed():
                        continue
                    page_url = getattr(page, "url", None)
                    if requested_is_tiktok and _is_tiktok_platform_url(page_url):
                        platform_matches.append((index, page))
                    if (
                        requested_identity is not None
                        and _normalized_tiktok_target_identity(page_url)
                        == requested_identity
                    ):
                        exact_matches.append((index, page))
                self._initial_platform_match_count = len(platform_matches)
                self._initial_exact_match_count = len(exact_matches)
                if platform_matches:
                    selected_index, self._real_page = platform_matches[-1]
                    self._adopted_page_enumeration_index_or_none = selected_index
                    self._page_adoption_count += 1
            if self._real_page is None:
                self._real_page = self._real_context.new_page()  # type: ignore[attr-defined]
                self._page_creation_count += 1
        return self._real_page

    def _navigate_page(self, page: object, url: str, **kwargs: object) -> object:
        current_identity = _normalized_tiktok_target_identity(
            getattr(page, "url", None)
        )
        requested_identity = _normalized_tiktok_target_identity(url)
        if current_identity is not None and current_identity == requested_identity:
            if self._force_same_url_reload:
                self._page_reload_count += 1
                return page.reload(**kwargs)  # type: ignore[attr-defined]
            self._same_url_navigation_suppression_count += 1
            return None
        self._page_navigation_count += 1
        return page.goto(url, **kwargs)  # type: ignore[attr-defined]

    @property
    def lifecycle_receipt(self) -> dict[str, object]:
        return {
            "engine": "chrome_cdp_page_observation_session",
            "browser_attach_count": 1 if self._real_browser is not None else 0,
            "context_acquisition_count": 1 if self._real_context is not None else 0,
            "page_acquisition_policy": "adopt_same_platform_else_create",
            "initial_page_count": self._initial_page_count,
            "initial_platform_match_count": self._initial_platform_match_count,
            "initial_exact_match_count": self._initial_exact_match_count,
            "duplicate_platform_match_policy": (
                "adopt_most_recently_enumerated_non_closed_platform_match"
            ),
            "adopted_page_enumeration_index_or_none": (
                self._adopted_page_enumeration_index_or_none
            ),
            "page_adoption_count": self._page_adoption_count,
            "page_creation_count": self._page_creation_count,
            "page_navigation_count": self._page_navigation_count,
            "page_reload_count": self._page_reload_count,
            "same_url_navigation_suppression_count": (
                self._same_url_navigation_suppression_count
            ),
            "page_reuse_policy": "reuse_one_runner_page_until_detached",
            "capture_attempt_count": self._capture_attempt_count,
            "capture_success_count": self._capture_success_count,
            "capture_elapsed_seconds_total": round(
                self._capture_elapsed_seconds_total, 6
            ),
            "capture_elapsed_seconds_max": round(
                self._capture_elapsed_seconds_max, 6
            ),
            "capture_timings": list(self._capture_timings),
            "browser_ownership": "operator_owned",
            "close_policy": "detach_only_leave_browser_and_page_open",
            "humanized_input_preset": "careful",
            "closed": self._closed,
        }

    def close(self) -> None:
        if self._closed:
            return
        try:
            if self._real_browser is not None:
                self._real_browser.close()  # type: ignore[attr-defined]
        finally:
            try:
                if self._playwright_owner is not None:
                    self._playwright_owner.stop()  # type: ignore[attr-defined]
            finally:
                self._closed = True


class CloakBrowserPageObservationSessionEngine(_CloakBrowserPageObservationEngine):
    """Reuse one CloakBrowser context across sequential page observations.

    The first observation fixes launch and context settings. Later observations
    must use the same settings, so a caller cannot silently change identity,
    storage state, viewport, or proxy posture inside one supervised session.
    Observations reuse one page and navigate it forward; per-capture listeners
    and routes are detached between observations. ``close`` owns the single
    terminal context/browser close and is idempotent.
    """

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self._real_browser: object | None = None
        self._real_context: object | None = None
        self._real_page: object | None = None
        self._launch_settings: tuple[ProxyProfile | None, bool, str | None] | None = None
        self._context_settings: dict[str, object] | None = None
        self._closed = False
        self._page_creation_count = 0
        self._capture_attempt_count = 0
        self._capture_success_count = 0

    def __enter__(self) -> "CloakBrowserPageObservationSessionEngine":
        if self._closed:
            raise RuntimeError("CloakBrowser page-observation session is already closed")
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def capture_page_observation(self, **kwargs: object) -> BrowserPageObservationSuccess:
        if self._closed:
            raise RuntimeError("CloakBrowser page-observation session is already closed")
        self._capture_attempt_count += 1
        result = super().capture_page_observation(**kwargs)
        self._capture_success_count += 1
        return result

    def _launch_page_observation_browser(
        self,
        *,
        playwright: object,
        proxy_profile: ProxyProfile | None,
        headless: bool,
        browser_channel: str | None,
    ) -> object:
        if self._closed:
            raise RuntimeError("CloakBrowser page-observation session is already closed")
        settings = (proxy_profile, headless, browser_channel)
        if self._launch_settings is None:
            self._real_browser = super()._launch_page_observation_browser(
                playwright=playwright,
                proxy_profile=proxy_profile,
                headless=headless,
                browser_channel=browser_channel,
            )
            self._launch_settings = settings
        elif settings != self._launch_settings:
            raise ValueError(
                "CloakBrowser page-observation session launch settings changed mid-session"
            )
        return _SessionBrowserProxy(self)

    def _new_scoped_context(self, context_kwargs: dict[str, object]) -> object:
        if self._real_browser is None:
            raise RuntimeError("CloakBrowser page-observation browser was not launched")
        if self._real_context is None:
            self._real_context = self._real_browser.new_context(**context_kwargs)  # type: ignore[attr-defined]
            self._context_settings = dict(context_kwargs)
        elif context_kwargs != self._context_settings:
            raise ValueError(
                "CloakBrowser page-observation context settings changed mid-session"
            )
        return _SessionContextProxy(self)

    def _get_or_create_page(self) -> object:
        if self._real_context is None:
            raise RuntimeError("CloakBrowser page-observation context was not created")
        if self._real_page is not None:
            is_closed = getattr(self._real_page, "is_closed", None)
            if callable(is_closed) and is_closed():
                self._real_page = None
        if self._real_page is None:
            self._real_page = self._real_context.new_page()  # type: ignore[attr-defined]
            self._page_creation_count += 1
        return self._real_page

    def _navigate_page(self, page: object, url: str, **kwargs: object) -> object:
        return page.goto(url, **kwargs)  # type: ignore[attr-defined]

    @property
    def lifecycle_receipt(self) -> dict[str, object]:
        return {
            "engine": "cloakbrowser_page_observation_session",
            "browser_launch_count": 1 if self._real_browser is not None else 0,
            "context_creation_count": 1 if self._real_context is not None else 0,
            "page_creation_count": self._page_creation_count,
            "page_reuse_policy": "reuse_one_page_until_closed",
            "capture_attempt_count": self._capture_attempt_count,
            "capture_success_count": self._capture_success_count,
            "closed": self._closed,
        }

    def close(self) -> None:
        if self._closed:
            return
        try:
            if self._real_context is not None:
                self._real_context.close()  # type: ignore[attr-defined]
        finally:
            try:
                if self._real_browser is not None:
                    self._real_browser.close()  # type: ignore[attr-defined]
            finally:
                self._closed = True


class _SessionBrowserProxy:
    def __init__(self, owner: CloakBrowserPageObservationSessionEngine) -> None:
        self._owner = owner

    def new_context(self, **kwargs: object) -> object:
        return self._owner._new_scoped_context(dict(kwargs))

    def close(self) -> None:
        return None


class _SessionContextProxy:
    def __init__(self, owner: CloakBrowserPageObservationSessionEngine) -> None:
        self._owner = owner
        self._page_proxy: _SessionPageProxy | None = None

    def new_page(self) -> object:
        self._page_proxy = _SessionPageProxy(
            self._owner._get_or_create_page(), owner=self._owner
        )
        return self._page_proxy

    def close(self) -> None:
        if self._page_proxy is not None:
            self._page_proxy.detach_capture_bindings()
            self._page_proxy = None


class _SessionPageProxy:
    def __init__(self, page: object, owner: object | None = None) -> None:
        self._page = page
        self._owner = owner
        self._listeners: list[tuple[str, object]] = []
        self._routes: list[tuple[str, object]] = []

    def __getattr__(self, name: str) -> object:
        return getattr(self._page, name)

    def on(self, event: str, callback: object) -> object:
        self._listeners.append((event, callback))
        return self._page.on(event, callback)  # type: ignore[attr-defined]

    def route(self, pattern: str, handler: object) -> object:
        self._routes.append((pattern, handler))
        return self._page.route(pattern, handler)  # type: ignore[attr-defined]

    def goto(self, url: str, **kwargs: object) -> object:
        navigate = getattr(self._owner, "_navigate_page", None)
        if callable(navigate):
            return navigate(self._page, url, **kwargs)
        return self._page.goto(url, **kwargs)  # type: ignore[attr-defined]

    def detach_capture_bindings(self) -> None:
        remove_listener = getattr(self._page, "remove_listener", None)
        if not callable(remove_listener):
            remove_listener = getattr(self._page, "off", None)
        if self._listeners and not callable(remove_listener):
            raise RuntimeError(
                "persistent page cannot detach per-capture response listeners"
            )
        for event, callback in reversed(self._listeners):
            remove_listener(event, callback)
        self._listeners.clear()

        unroute = getattr(self._page, "unroute", None)
        if self._routes and not callable(unroute):
            raise RuntimeError("persistent page cannot detach per-capture routes")
        for pattern, handler in reversed(self._routes):
            unroute(pattern, handler)
        self._routes.clear()


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


def _normalized_tiktok_target_identity(value: object) -> tuple[str, str] | None:
    """Return the scheme/query/fragment-insensitive TikTok host/path identity."""

    if not isinstance(value, str) or not value.strip():
        return None
    parsed = urlparse(value)
    host = parsed.hostname.lower() if parsed.hostname else ""
    if host == "www.tiktok.com":
        host = "tiktok.com"
    if host != "tiktok.com":
        return None
    path = parsed.path.rstrip("/").lower() or "/"
    return host, path


def _is_tiktok_platform_url(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    parsed = urlparse(value)
    host = parsed.hostname.lower() if parsed.hostname else ""
    return host == "tiktok.com" or host.endswith(".tiktok.com")


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
    # Narrow on purpose: a wrong-type caller (no .request) still gets (None, None),
    # but any other failure now surfaces instead of being masked as absent metadata.
    try:
        request = getattr(response, "request")
    except AttributeError:
        return None, None
    method = str(getattr(request, "method", "") or "").upper() or None
    resource_type = str(getattr(request, "resource_type", "") or "").lower() or None
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
  const preferSmallestMatch = Boolean(args.prefer_smallest_match);
  const result = {
    candidate_count: 0,
    matched_count: 0,
    target_found: false,
    target_kind: null,
    box: null,
    page_text_gate_matched: pageTextMarkers.length === 0 ? null : false,
    page_text_matched_marker: null,
    selection_strategy: preferTopRight ? 'top_right' : preferSmallestMatch ? 'smallest_match' : 'first_match',
  };
  if (pageTextMarkers.length > 0) {
    const pageText = [
      document.title,
      document.body ? document.body.innerText : '',
    ].filter(Boolean).join(' ').toLowerCase();
    const pageTextMatchedMarker = pageTextMarkers.find((marker) => pageText.includes(marker)) || null;
    if (pageTextMatchedMarker === null) {
      return result;
    }
    result.page_text_gate_matched = true;
    result.page_text_matched_marker = pageTextMatchedMarker;
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
      target_kind: tag === 'button' ? 'button' : role === 'button' ? 'role_button' : role === 'tab' ? 'tab' : tag === 'a' ? 'link' : 'candidate',
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
      node.getAttribute('href'),
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
  if (preferSmallestMatch && matches.length > 0) {
    selected = matches.slice().sort((left, right) => {
      const leftArea = left.box.width * left.box.height;
      const rightArea = right.box.width * right.box.height;
      if (leftArea !== rightArea) {
        return leftArea - rightArea;
      }
      if (left.box.y !== right.box.y) {
        return left.box.y - right.box.y;
      }
      return left.box.x - right.box.x;
    })[0];
  }
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


_PAGE_TEXT_MARKER_MATCH_SCRIPT = r"""
(markersArg) => {
  const markers = Array.isArray(markersArg)
    ? markersArg.map((value) => String(value || '').trim().toLowerCase()).filter(Boolean)
    : [];
  const pageText = [
    document.title,
    document.body ? document.body.innerText : '',
  ].filter(Boolean).join(' ').toLowerCase();
  const matched = markers.find((marker) => pageText.includes(marker)) || null;
  return {
    human_challenge_marker_match: true,
    checked: markers.length > 0,
    matched: matched !== null,
    matched_marker: matched,
    marker_count: markers.length,
  };
}
""".strip()


_PAGE_TEXT_MARKER_ABSENCE_SCRIPT = r"""
(markersArg) => {
  const markers = Array.isArray(markersArg)
    ? markersArg.map((value) => String(value || '').trim().toLowerCase()).filter(Boolean)
    : [];
  const pageText = [
    document.title,
    document.body ? document.body.innerText : '',
  ].filter(Boolean).join(' ').toLowerCase();
  const matched = markers.find((marker) => pageText.includes(marker)) || null;
  return {
    checked: markers.length > 0,
    marker_count: markers.length,
    absent: markers.length > 0 ? matched === null : null,
    matched_marker: matched,
  };
}
""".strip()


def _normalize_wheel_action(
    action: BrowserPageWheelAction | None,
) -> BrowserPageWheelAction | None:
    if action is None:
        return None
    if not isinstance(action, BrowserPageWheelAction):
        raise ValueError("post_load_wheel_action must be BrowserPageWheelAction")
    if not action.action_name.strip():
        raise ValueError("post_load_wheel_action.action_name must not be blank")
    if action.direction not in {"up", "down"}:
        raise ValueError("post_load_wheel_action.direction must be up or down")
    for field_name, value in (
        ("viewport_fraction_min", action.viewport_fraction_min),
        ("viewport_fraction_max", action.viewport_fraction_max),
        ("cursor_fraction_min", action.cursor_fraction_min),
        ("cursor_fraction_max", action.cursor_fraction_max),
    ):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"post_load_wheel_action.{field_name} must be numeric")
        if not 0 < float(value) < 1:
            raise ValueError(
                f"post_load_wheel_action.{field_name} must be between zero and one"
            )
    if action.viewport_fraction_min > action.viewport_fraction_max:
        raise ValueError(
            "post_load_wheel_action.viewport_fraction_min must be <= viewport_fraction_max"
        )
    if action.cursor_fraction_min > action.cursor_fraction_max:
        raise ValueError(
            "post_load_wheel_action.cursor_fraction_min must be <= cursor_fraction_max"
        )
    for minimum_name, maximum_name, minimum, maximum in (
        (
            "wheel_chunk_px_min",
            "wheel_chunk_px_max",
            action.wheel_chunk_px_min,
            action.wheel_chunk_px_max,
        ),
        (
            "wheel_pause_ms_min",
            "wheel_pause_ms_max",
            action.wheel_pause_ms_min,
            action.wheel_pause_ms_max,
        ),
        (
            "settle_ms_min",
            "settle_ms_max",
            action.settle_ms_min,
            action.settle_ms_max,
        ),
    ):
        if (
            isinstance(minimum, bool)
            or not isinstance(minimum, int)
            or isinstance(maximum, bool)
            or not isinstance(maximum, int)
            or minimum < 0
            or maximum < minimum
        ):
            raise ValueError(
                f"post_load_wheel_action.{minimum_name}/{maximum_name} are invalid"
            )
    if action.wheel_chunk_px_min <= 0:
        raise ValueError("post_load_wheel_action.wheel_chunk_px_min must be positive")
    return action


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
    post_click_absent_text_markers = tuple(
        marker.strip().lower()
        for marker in action.post_click_absent_text_markers
        if marker.strip()
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
    visual_x_target_zone = action.visual_x_target_zone.strip().lower()
    if visual_x_target_zone not in {"top_right", "center_modal"}:
        raise ValueError(
            "post_load_pointer_action.visual_x_target_zone must be top_right or center_modal"
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
        prefer_smallest_match=bool(action.prefer_smallest_match),
        visual_top_right_x_fallback=bool(action.visual_top_right_x_fallback),
        visual_x_target_zone=visual_x_target_zone,
        visual_x_geometric_fallback=bool(action.visual_x_geometric_fallback),
        post_click_absent_text_markers=post_click_absent_text_markers,
        post_click_visual_target_absence_check=bool(
            action.post_click_visual_target_absence_check
        ),
        stop_sequence_on_failed_post_click_verification=bool(
            action.stop_sequence_on_failed_post_click_verification
        ),
        stop_wait_on_observed_response=bool(action.stop_wait_on_observed_response),
        stop_sequence_on_observed_response=bool(
            action.stop_sequence_on_observed_response
        ),
        observed_response_wait_poll_ms=max(1, int(action.observed_response_wait_poll_ms)),
        random_seed=(
            int(action.random_seed) if action.random_seed is not None else None
        ),
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


def _find_visual_top_right_x_target(
    page: object,
    *,
    target_zone: str = "top_right",
    allow_geometric: bool = True,
) -> dict[str, object]:
    result: dict[str, object] = {
        "target_found": False,
        "target_kind": "visual_x",
        "visual_fallback_target_zone": target_zone,
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
    try:
        candidates = _visual_x_candidates(image, crop_x, crop_y, crop_width, crop_height)
    except _VisualPixelReadError:
        result["visual_fallback_failure"] = "visual_fallback_pixel_read_failed"
        return result
    result["visual_fallback_candidate_count"] = len(candidates)
    modal_candidates: list[dict[str, float]] | None = None
    if target_zone == "center_modal":
        # The broad candidate_count spans the whole top-right crop and so includes
        # unrelated page X-glyphs; the zone count isolates the center-modal close
        # candidates the action actually targets, so a receipt reader can tell a
        # persisting modal from stray glyphs. It is a diagnostic count only and
        # does not change close-acceptance.
        modal_candidates = _center_modal_visual_x_candidates(
            candidates, image_width, image_height
        )
        result["visual_fallback_zone_candidate_count"] = len(modal_candidates)
    if not candidates:
        return result
    selected = None
    if target_zone == "center_modal":
        if modal_candidates:
            selected = max(modal_candidates, key=lambda candidate: candidate["score"])
        elif allow_geometric:
            selected = _center_modal_geometric_close_candidate(image_width, image_height)
            result["visual_fallback_geometric_target"] = True
        else:
            return result
    if selected is None:
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


def _center_modal_visual_x_candidates(
    candidates: Sequence[dict[str, float]],
    image_width: int,
    image_height: int,
) -> list[dict[str, float]]:
    modal_candidates: list[dict[str, float]] = []
    for candidate in candidates:
        center_x = (candidate["x"] + candidate["width"] / 2.0) / max(1, image_width)
        center_y = (candidate["y"] + candidate["height"] / 2.0) / max(1, image_height)
        if 0.58 <= center_x <= 0.68 and 0.14 <= center_y <= 0.35:
            modal_candidates.append(candidate)
    return modal_candidates


def _center_modal_geometric_close_candidate(
    image_width: int,
    image_height: int,
) -> dict[str, float]:
    width = max(16.0, min(28.0, image_width * 0.018))
    height = max(16.0, min(28.0, image_height * 0.03))
    center_x = image_width * 0.628
    center_y = image_height * 0.275
    return {
        "x": max(0.0, center_x - width / 2.0),
        "y": max(0.0, center_y - height / 2.0),
        "width": width,
        "height": height,
        "score": 0.0,
    }


class _VisualPixelReadError(RuntimeError):
    """Every pixel read in the visual-X crop failed -- a systematic decode
    failure that must not be reported as an empty candidate signal."""


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
    attempted_reads = 0
    failed_reads = 0
    for y in range(crop_y, y_end):
        for x in range(crop_x, x_end):
            attempted_reads += 1
            try:
                value = int(pixels[x, y])
            except Exception:
                # Single-pixel oddities stay skippable; only a 100% failure
                # rate is surfaced below as systematic, not empty signal.
                failed_reads += 1
                continue
            if value <= 96:
                foreground_sets[0].add((x, y))
            elif value >= 216:
                foreground_sets[1].add((x, y))
    if attempted_reads and failed_reads == attempted_reads:
        raise _VisualPixelReadError(
            f"all {attempted_reads} pixel reads failed in the visual-X crop: "
            "systematic decode failure, not an empty signal"
        )

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

def _page_text_marker_match_result(
    page: object,
    markers: Sequence[str],
) -> dict[str, object]:
    result: dict[str, object] = {
        "checked": bool(markers),
        "matched": False,
        "matched_marker": None,
        "marker_count": len(markers),
    }
    if not markers:
        return result
    try:
        marker_result = page.evaluate(_PAGE_TEXT_MARKER_MATCH_SCRIPT, list(markers))
    except Exception:
        result["failure"] = "human_challenge_marker_lookup_failed"
        return result
    if not isinstance(marker_result, dict):
        result["failure"] = "human_challenge_marker_lookup_failed"
        return result
    matched = marker_result.get("matched")
    if isinstance(matched, bool):
        result["matched"] = matched
    matched_marker = marker_result.get("matched_marker")
    if isinstance(matched_marker, str) and matched_marker:
        result["matched_marker"] = matched_marker
    marker_count = marker_result.get("marker_count")
    try:
        result["marker_count"] = int(marker_count)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        pass
    return result


def _page_text_marker_absence_result(
    page: object,
    markers: Sequence[str],
) -> dict[str, object]:
    result: dict[str, object] = {
        "post_click_absence_checked": True,
        "post_click_absence_marker_count": len(markers),
        "post_click_absence_verified": False,
    }
    try:
        marker_result = page.evaluate(_PAGE_TEXT_MARKER_ABSENCE_SCRIPT, list(markers))
    except Exception:
        result["post_click_absence_failure"] = "post_click_absence_lookup_failed"
        return result
    if not isinstance(marker_result, dict):
        result["post_click_absence_failure"] = "post_click_absence_lookup_failed"
        return result
    absent = marker_result.get("absent")
    if isinstance(absent, bool):
        result["post_click_absence_verified"] = absent
    matched_marker = marker_result.get("matched_marker")
    if isinstance(matched_marker, str) and matched_marker:
        result["post_click_absence_matched_marker"] = matched_marker
    marker_count = marker_result.get("marker_count")
    try:
        result["post_click_absence_marker_count"] = int(marker_count)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        pass
    return result


def _post_click_visual_absence_result(
    page: object,
    action: BrowserPagePointerAction,
) -> dict[str, object]:
    visual_target = _find_visual_top_right_x_target(
        page,
        target_zone=action.visual_x_target_zone,
        allow_geometric=False,
    )
    target_found = bool(visual_target.get("target_found"))
    failure = visual_target.get("visual_fallback_failure")
    candidate_count = _safe_int(
        visual_target.get("visual_fallback_candidate_count"),
        default=-1,
    )
    result: dict[str, object] = {
        "post_click_visual_check_attempted": True,
        "post_click_visual_target_found": target_found,
        "post_click_visual_target_absent": (
            not target_found and failure is None and candidate_count == 0
        ),
        "post_click_visual_candidate_count": candidate_count,
    }
    zone_candidate_count = visual_target.get("visual_fallback_zone_candidate_count")
    if zone_candidate_count is not None:
        result["post_click_visual_zone_candidate_count"] = _safe_int(
            zone_candidate_count, default=-1
        )
    confidence = visual_target.get("visual_fallback_confidence")
    if confidence is not None:
        result["post_click_visual_confidence"] = confidence
    screenshot_sha256 = visual_target.get("visual_fallback_screenshot_sha256")
    if isinstance(screenshot_sha256, str) and screenshot_sha256:
        result["post_click_visual_screenshot_sha256"] = screenshot_sha256
    crop_box = visual_target.get("visual_fallback_crop_box")
    if isinstance(crop_box, dict):
        result["post_click_visual_crop_box"] = crop_box
    box = visual_target.get("box")
    if isinstance(box, dict):
        result["post_click_visual_target_box"] = box
    if isinstance(failure, str) and failure:
        result["post_click_visual_failure"] = failure
    return result


def _post_click_verification_accepted(receipt: dict[str, object]) -> bool:
    verification_values = [
        value
        for value in (
            receipt.get("post_click_absence_verified"),
            receipt.get("post_click_visual_target_absent"),
        )
        if isinstance(value, bool)
    ]
    return bool(verification_values) and all(verification_values)


def _should_stop_pointer_action_sequence(
    action: BrowserPagePointerAction,
    receipt: dict[str, object],
) -> bool:
    if action.stop_sequence_on_observed_response:
        response_count = max(
            _safe_int(receipt.get("observed_response_count_before"), default=0),
            _safe_int(receipt.get("observed_response_count_after"), default=0),
        )
        if response_count > 0:
            return True
    if not action.stop_sequence_on_failed_post_click_verification:
        return False
    clicked = receipt.get("clicked") is True
    if receipt.get("page_text_gate_matched") is False and not clicked:
        return False
    if not clicked:
        return True
    return not _post_click_verification_accepted(receipt)


def _pre_action_stop_marker_receipt(
    page: object,
    *,
    markers: Sequence[str],
    after_action_name: str,
) -> dict[str, object] | None:
    if not markers:
        return None
    match = _page_text_marker_match_result(page, markers)
    if match.get("matched") is not True:
        current_url = str(getattr(page, "url", "")).lower()
        url_marker = next(
            (
                marker
                for marker in markers
                if marker.startswith("/") and marker in current_url
            ),
            None,
        )
        if url_marker is None:
            return None
        match = {
            "matched": True,
            "matched_marker": url_marker,
            "marker_count": len(markers),
        }
    return {
        "action_name": "pre_action_terminal_stop_v0",
        "action_mode": "account_safety_circuit_breaker",
        "action_taken": False,
        "after_action_name": after_action_name,
        "matched_marker": match.get("matched_marker"),
        "marker_count": match.get("marker_count"),
        "scripted_actions_suppressed": True,
        "automatic_retry_allowed": False,
    }


def _run_human_challenge_handoff(
    page: object,
    *,
    markers: Sequence[str],
    timeout_seconds: float,
    prompt: str | None,
) -> dict[str, object] | None:
    initial_match = _page_text_marker_match_result(page, markers)
    if initial_match.get("matched") is not True:
        return None
    prompt_text = prompt or (
        "A slider/captcha/security marker is visible. Solve it manually in the "
        "open browser if authorized, then click OK here."
    )
    receipt: dict[str, object] = {
        "action_name": "human_challenge_handoff_v0",
        "action_mode": "source_access_intervention",
        "action_taken": True,
        "captcha_solving_by_agent": False,
        "prompted": True,
        "prompt_surface": _show_human_challenge_prompt(prompt_text),
        "matched_marker": initial_match.get("matched_marker"),
        "marker_count": initial_match.get("marker_count"),
        "timeout_seconds": timeout_seconds,
        "cleared": False,
        "wait_ms": 0,
    }
    timeout_ms = int(timeout_seconds * 1000)
    elapsed_ms = 0
    poll_ms = 1000
    while True:
        current_match = _page_text_marker_match_result(page, markers)
        if current_match.get("matched") is not True:
            receipt["cleared"] = True
            receipt["wait_ms"] = elapsed_ms
            return receipt
        matched_marker = current_match.get("matched_marker")
        if isinstance(matched_marker, str) and matched_marker:
            receipt["final_matched_marker"] = matched_marker
        if elapsed_ms >= timeout_ms:
            receipt["timeout_exceeded"] = True
            receipt["wait_ms"] = elapsed_ms
            return receipt
        step_ms = min(poll_ms, timeout_ms - elapsed_ms)
        if step_ms <= 0:
            receipt["timeout_exceeded"] = True
            receipt["wait_ms"] = elapsed_ms
            return receipt
        page.wait_for_timeout(step_ms)
        elapsed_ms += step_ms


def _show_human_challenge_prompt(prompt: str) -> str:
    try:
        import ctypes

        ctypes.windll.user32.MessageBoxW(
            0,
            prompt,
            "TikTok challenge handoff",
            0x00000040 | 0x00040000,
        )
        return "windows_message_box"
    except Exception:
        print(prompt, flush=True)
        return "stdout"


def _run_wheel_action(
    page: object,
    action: BrowserPageWheelAction,
) -> dict[str, object]:
    receipt: dict[str, object] = {
        "action_name": action.action_name,
        "direction": action.direction,
        "input_method": "page.mouse.wheel_burst",
        "cloakbrowser_pointer_layer_applies_to_cursor_move": True,
        "cloakbrowser_pointer_layer_applies_to_wheel_burst": False,
        "completed": False,
    }
    try:
        before = page.evaluate(  # type: ignore[attr-defined]
            "() => ({scroll_y: Math.max(0, window.scrollY || 0), "
            "viewport_width: Math.max(1, window.innerWidth || 1), "
            "viewport_height: Math.max(1, window.innerHeight || 1)})"
        )
        if not isinstance(before, dict):
            raise ValueError("wheel viewport observation was not an object")
        scroll_y_before = max(0.0, float(before["scroll_y"]))
        viewport_width = max(1.0, float(before["viewport_width"]))
        viewport_height = max(1.0, float(before["viewport_height"]))
    except Exception:
        receipt["failure"] = "wheel_action_viewport_lookup_failed"
        return receipt

    rng = (
        random.Random(action.random_seed)
        if action.random_seed is not None
        else random.SystemRandom()
    )
    viewport_fraction = rng.uniform(
        action.viewport_fraction_min, action.viewport_fraction_max
    )
    distance_px = max(1, round(viewport_height * viewport_fraction))
    direction_sign = -1 if action.direction == "up" else 1
    cursor_fraction_x = rng.uniform(
        action.cursor_fraction_min, action.cursor_fraction_max
    )
    cursor_fraction_y = rng.uniform(
        action.cursor_fraction_min, action.cursor_fraction_max
    )
    wheel_event_count = 0
    pause_total_ms = 0
    try:
        page.mouse.move(  # type: ignore[attr-defined]
            viewport_width * cursor_fraction_x,
            viewport_height * cursor_fraction_y,
        )
        remaining = distance_px
        while remaining > 0:
            chunk_px = min(
                remaining,
                rng.randint(action.wheel_chunk_px_min, action.wheel_chunk_px_max),
            )
            page.mouse.wheel(0, direction_sign * chunk_px)  # type: ignore[attr-defined]
            wheel_event_count += 1
            remaining -= chunk_px
            if remaining > 0:
                pause_ms = rng.randint(
                    action.wheel_pause_ms_min, action.wheel_pause_ms_max
                )
                if pause_ms > 0:
                    page.wait_for_timeout(pause_ms)  # type: ignore[attr-defined]
                    pause_total_ms += pause_ms
        settle_ms = rng.randint(action.settle_ms_min, action.settle_ms_max)
        if settle_ms > 0:
            page.wait_for_timeout(settle_ms)  # type: ignore[attr-defined]
        after = page.evaluate(  # type: ignore[attr-defined]
            "() => ({scroll_y: Math.max(0, window.scrollY || 0)})"
        )
        if not isinstance(after, dict):
            raise ValueError("wheel post-action observation was not an object")
        scroll_y_after = max(0.0, float(after["scroll_y"]))
    except Exception:
        receipt["failure"] = "wheel_action_failed"
        receipt["wheel_event_count"] = wheel_event_count
        return receipt

    receipt.update(
        {
            "completed": True,
            "viewport_fraction": round(viewport_fraction, 6),
            "planned_delta_y_px": direction_sign * distance_px,
            "wheel_event_count": wheel_event_count,
            "wheel_pause_total_ms": pause_total_ms,
            "settle_ms": settle_ms,
            "cursor_fraction_x": round(cursor_fraction_x, 6),
            "cursor_fraction_y": round(cursor_fraction_y, 6),
            "scroll_y_before": round(scroll_y_before, 3),
            "scroll_y_after": round(scroll_y_after, 3),
            "actual_scroll_delta_y_px": round(
                scroll_y_after - scroll_y_before, 3
            ),
        }
    )
    return receipt


def _run_pointer_action(
    page: object,
    action: BrowserPagePointerAction,
    *,
    observed_response_count: Callable[[], int] | None = None,
) -> dict[str, object]:
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

    def current_observed_response_count() -> int | None:
        if observed_response_count is None:
            return None
        try:
            return max(0, int(observed_response_count()))
        except (TypeError, ValueError):
            return None

    response_count_before = current_observed_response_count()
    if response_count_before is not None:
        receipt["observed_response_count_before"] = response_count_before
    try:
        target = page.evaluate(
            _POINTER_ACTION_TARGET_SCRIPT,
            {
                "candidate_selector": action.candidate_selector,
                "text_markers": list(action.text_markers),
                "page_text_markers": list(action.page_text_markers),
                "exact_text_markers": list(action.exact_text_markers),
                "prefer_top_right": action.prefer_top_right,
                "prefer_smallest_match": action.prefer_smallest_match,
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
    page_text_matched_marker = target.get("page_text_matched_marker")
    if isinstance(page_text_matched_marker, str) and page_text_matched_marker:
        receipt["page_text_matched_marker"] = page_text_matched_marker
    selection_strategy = target.get("selection_strategy")
    if isinstance(selection_strategy, str) and selection_strategy:
        receipt["selection_strategy"] = selection_strategy
    box = target.get("box")
    if not receipt["target_found"] or not isinstance(box, dict):
        if action.visual_top_right_x_fallback and receipt.get("page_text_gate_matched") is not False:
            visual_target = _find_visual_top_right_x_target(
                page,
                target_zone=action.visual_x_target_zone,
                allow_geometric=action.visual_x_geometric_fallback,
            )
            for key in (
                "visual_fallback_attempted",
                "visual_fallback_target_found",
                "visual_fallback_candidate_count",
                "visual_fallback_zone_candidate_count",
                "visual_fallback_confidence",
                "visual_fallback_screenshot_sha256",
                "visual_fallback_crop_box",
                "visual_fallback_target_zone",
                "visual_fallback_geometric_target",
                "visual_fallback_failure",
            ):
                value = visual_target.get(key)
                if value is not None:
                    receipt[key] = value
            visual_box = visual_target.get("box")
            if bool(visual_target.get("target_found")) and isinstance(visual_box, dict):
                receipt["target_found"] = True
                receipt["target_kind"] = "visual_x"
                receipt["selection_strategy"] = f"{action.visual_x_target_zone}_visual_x"
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

    rng = (
        random.Random(action.random_seed)
        if action.random_seed is not None
        else random.SystemRandom()
    )
    click_fraction_x = rng.uniform(
        action.target_fraction_min, action.target_fraction_max
    )
    click_fraction_y = rng.uniform(
        action.target_fraction_min, action.target_fraction_max
    )
    click_x = x + width * click_fraction_x
    click_y = y + height * click_fraction_y
    move_steps = rng.randint(action.move_steps_min, action.move_steps_max)
    try:
        page.mouse.move(click_x, click_y, steps=move_steps)
        page.mouse.click(click_x, click_y)
        wait_ms = 0
        if action.wait_after_ms > 0:
            if action.stop_wait_on_observed_response and observed_response_count is not None:
                poll_ms = max(
                    1,
                    min(action.observed_response_wait_poll_ms, action.wait_after_ms),
                )
                while wait_ms < action.wait_after_ms:
                    current_count = current_observed_response_count()
                    if (
                        response_count_before is not None
                        and current_count is not None
                        and current_count > response_count_before
                    ):
                        break
                    step_ms = min(poll_ms, action.wait_after_ms - wait_ms)
                    page.wait_for_timeout(step_ms)
                    wait_ms += step_ms
            else:
                page.wait_for_timeout(action.wait_after_ms)
                wait_ms = action.wait_after_ms
    except Exception:
        receipt["failure"] = "pointer_action_click_failed"
        return receipt
    receipt["clicked"] = True
    receipt["move_steps"] = move_steps
    receipt["wait_ms"] = wait_ms
    receipt["target_geometry_freshly_resolved"] = True
    receipt["target_box_width"] = round(width, 3)
    receipt["target_box_height"] = round(height, 3)
    receipt["click_fraction_x"] = round(click_fraction_x, 6)
    receipt["click_fraction_y"] = round(click_fraction_y, 6)
    receipt["target_fraction_min"] = action.target_fraction_min
    receipt["target_fraction_max"] = action.target_fraction_max
    response_count_after = current_observed_response_count()
    if response_count_after is not None:
        receipt["observed_response_count_after"] = response_count_after
        if response_count_before is not None:
            receipt["observed_response_delta"] = max(
                0,
                response_count_after - response_count_before,
            )
        receipt["observed_response_seen"] = response_count_after > 0
    receipt["target_box"] = {
        "x": round(x, 3),
        "y": round(y, 3),
        "width": round(width, 3),
        "height": round(height, 3),
    }
    receipt["click_point"] = {
        "x": round(click_x, 3),
        "y": round(click_y, 3),
    }
    if action.post_click_absent_text_markers:
        receipt.update(
            _page_text_marker_absence_result(
                page,
                action.post_click_absent_text_markers,
            )
        )
    if action.post_click_visual_target_absence_check:
        receipt.update(_post_click_visual_absence_result(page, action))
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
    stop_condition: Callable[[], bool] | None = None,
) -> _LazyLoadScrollResult:
    executed = 0
    if stop_condition is not None and stop_condition():
        return _LazyLoadScrollResult(executed, "response_target_reached")
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
            if stop_condition is not None and stop_condition():
                return _LazyLoadScrollResult(executed, "response_target_reached")
        stop_reason = "capped_pass_limit" if capped else "requested_passes_complete"
        return _LazyLoadScrollResult(executed, stop_reason)

    for _ in range(bounded_passes):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(_SCROLL_PASS_SETTLE_MS)
        executed += 1
        if stop_condition is not None and stop_condition():
            return _LazyLoadScrollResult(executed, "response_target_reached")
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


def _normalize_browser_backend(browser_backend: str) -> str:
    normalized = browser_backend.strip().lower()
    if not normalized:
        raise ValueError("browser_backend must not be blank")
    if normalized not in ALLOWED_BROWSER_BACKENDS:
        allowed = ", ".join(sorted(ALLOWED_BROWSER_BACKENDS))
        raise ValueError(f"browser_backend must be one of: {allowed}")
    return normalized


def _normalize_lower_text_tuple(markers: Sequence[str], *, name: str) -> tuple[str, ...]:
    normalized = tuple(marker.strip().lower() for marker in markers if marker.strip())
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"{name} must not contain duplicate entries")
    return normalized


def _normalize_name_tuple(values: Sequence[str], *, name: str) -> tuple[str, ...]:
    normalized = tuple(value.strip() for value in values if value.strip())
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"{name} must not contain duplicate entries")
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
