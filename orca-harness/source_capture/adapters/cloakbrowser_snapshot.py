from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from importlib import import_module
from typing import Protocol, TypeAlias
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from harness_utils import utc_now_z
from source_capture.proxy_profiles import ProxyProfile


DEFAULT_TIMEOUT_SECONDS = 20.0
DEFAULT_VIEWPORT_WIDTH = 1280
DEFAULT_VIEWPORT_HEIGHT = 720
DEFAULT_MAX_ARTIFACT_BYTES = 5_000_000
ALLOWED_WAIT_UNTIL = {"commit", "domcontentloaded", "load", "networkidle"}
# Pause after each scroll-to-bottom pass so lazy-loaded ("load more" / infinite
# scroll) content has time to fetch and render before the next pass or capture.
_SCROLL_PASS_SETTLE_MS = 2000
# Max time to wait for an operator-supplied "load more" control to become
# clickable before giving up that pass (treated as end-of-list, not an error).
_LOAD_MORE_CLICK_TIMEOUT_MS = 5000
# Pause after each progressive scroll step so an IntersectionObserver-gated
# section (e.g. a lazy-rendered reviews widget) can enter the viewport, fetch,
# and render before the next step or the capture.
_PROGRESSIVE_SCROLL_PAUSE_MS = 1500
# Safety cap on progressive scroll steps so an infinite-scroll page (whose
# scrollHeight keeps growing) cannot loop unbounded.
_MAX_PROGRESSIVE_SCROLL_STEPS = 40
CLOAKBROWSER_METHOD_CATEGORY = "anti_blocking_browser"
CLOAKBROWSER_BACKEND = "playwright"
HEAVY_RESOURCE_TYPES = frozenset({"font", "image", "media"})
SECRET_LIKE_QUERY_KEYS = {
    "access_token",
    "api_key",
    "auth",
    "authorization",
    "bearer",
    "client_secret",
    "code",
    "cookie",
    "key",
    "password",
    "refresh_token",
    "session",
    "sid",
    "token",
}
SECRET_LIKE_WARNING_TERMS = SECRET_LIKE_QUERY_KEYS | {
    "set-cookie",
    "storage_state",
    "user_data_dir",
}


class CloakBrowserSnapshotFailureKind(StrEnum):
    DEPENDENCY_UNAVAILABLE = "dependency_unavailable"
    TIMEOUT = "timeout"
    CAPTURE_FAILED = "capture_failed"
    ACCESS_BLOCKED = "access_blocked"
    EMPTY_RENDERED_DOM = "empty_rendered_dom"
    EMPTY_SCREENSHOT = "empty_screenshot"
    SIZE_CAP_EXCEEDED = "size_cap_exceeded"


@dataclass(frozen=True)
class CloakBrowserSnapshotSuccess:
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
class CloakBrowserSnapshotFailure:
    requested_url: str
    failure_kind: CloakBrowserSnapshotFailureKind
    message: str
    final_url: str | None = None


CloakBrowserSnapshotResult: TypeAlias = CloakBrowserSnapshotSuccess | CloakBrowserSnapshotFailure


class CloakBrowserSnapshotEngineResult(Protocol):
    final_url: str
    title: str | None
    rendered_dom: str
    visible_text: str
    screenshot_png: bytes
    warning_notes: list[str]


class CloakBrowserSnapshotEngine(Protocol):
    def capture(
        self,
        *,
        url: str,
        timeout_seconds: float,
        wait_until: str,
        viewport_width: int,
        viewport_height: int,
        proxy_profile: ProxyProfile | None,
        block_heavy_assets: bool,
        settle_seconds: float,
        scroll_passes: int,
        load_more_selector: str | None,
        load_more_clicks: int,
        scroll_step_px: int,
    ) -> CloakBrowserSnapshotEngineResult:
        ...


def fetch_cloakbrowser_snapshot_capture(
    *,
    url: str,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    wait_until: str = "load",
    viewport_width: int = DEFAULT_VIEWPORT_WIDTH,
    viewport_height: int = DEFAULT_VIEWPORT_HEIGHT,
    max_artifact_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
    proxy_profile: ProxyProfile | None = None,
    block_heavy_assets: bool = False,
    settle_seconds: float = 0.0,
    scroll_passes: int = 0,
    load_more_selector: str | None = None,
    load_more_clicks: int = 0,
    scroll_step_px: int = 0,
    engine: CloakBrowserSnapshotEngine | None = None,
) -> CloakBrowserSnapshotResult:
    normalized_url = _validate_http_url(url)
    _validate_positive_number("timeout_seconds", timeout_seconds)
    _validate_positive_int("viewport_width", viewport_width)
    _validate_positive_int("viewport_height", viewport_height)
    _validate_positive_int("max_artifact_bytes", max_artifact_bytes)
    if settle_seconds < 0:
        raise ValueError("settle_seconds must be zero or greater")
    if scroll_passes < 0:
        raise ValueError("scroll_passes must be zero or greater")
    if scroll_step_px < 0:
        raise ValueError("scroll_step_px must be zero or greater")
    if load_more_clicks < 0:
        raise ValueError("load_more_clicks must be zero or greater")
    if load_more_clicks > 0 and not load_more_selector:
        raise ValueError("load_more_selector is required when load_more_clicks is greater than zero")
    if wait_until not in ALLOWED_WAIT_UNTIL:
        allowed = ", ".join(sorted(ALLOWED_WAIT_UNTIL))
        raise ValueError(f"wait_until must be one of: {allowed}")

    capture_engine = engine or _CloakBrowserSnapshotEngine()
    try:
        engine_result = capture_engine.capture(
            url=normalized_url,
            timeout_seconds=timeout_seconds,
            wait_until=wait_until,
            viewport_width=viewport_width,
            viewport_height=viewport_height,
            proxy_profile=proxy_profile,
            block_heavy_assets=block_heavy_assets,
            settle_seconds=settle_seconds,
            scroll_passes=scroll_passes,
            load_more_selector=load_more_selector,
            load_more_clicks=load_more_clicks,
            scroll_step_px=scroll_step_px,
        )
    except _CloakBrowserSnapshotDependencyUnavailable as exc:
        return CloakBrowserSnapshotFailure(
            requested_url=normalized_url,
            failure_kind=CloakBrowserSnapshotFailureKind.DEPENDENCY_UNAVAILABLE,
            message=_redact_proxy_secret(str(exc), proxy_profile=proxy_profile),
        )
    except Exception as exc:
        return CloakBrowserSnapshotFailure(
            requested_url=normalized_url,
            failure_kind=_failure_kind_from_exception(exc),
            message=_redact_proxy_secret(
                f"CloakBrowser snapshot capture failed: {exc}", proxy_profile=proxy_profile
            ),
        )

    final_url = _sanitize_engine_final_url(engine_result.final_url)
    if final_url is None:
        return CloakBrowserSnapshotFailure(
            requested_url=normalized_url,
            failure_kind=CloakBrowserSnapshotFailureKind.CAPTURE_FAILED,
            message="CloakBrowser snapshot returned a final URL with embedded credentials",
        )

    if not engine_result.rendered_dom:
        return CloakBrowserSnapshotFailure(
            requested_url=normalized_url,
            final_url=final_url,
            failure_kind=CloakBrowserSnapshotFailureKind.EMPTY_RENDERED_DOM,
            message="CloakBrowser snapshot returned an empty rendered DOM",
        )
    if not engine_result.screenshot_png:
        return CloakBrowserSnapshotFailure(
            requested_url=normalized_url,
            final_url=final_url,
            failure_kind=CloakBrowserSnapshotFailureKind.EMPTY_SCREENSHOT,
            message="CloakBrowser snapshot returned an empty screenshot",
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
        return CloakBrowserSnapshotFailure(
            requested_url=normalized_url,
            final_url=final_url,
            failure_kind=CloakBrowserSnapshotFailureKind.SIZE_CAP_EXCEEDED,
            message=(
                f"CloakBrowser snapshot artifact exceeded max-artifact-bytes cap "
                f"({max_artifact_bytes}): {details}"
            ),
        )

    warning_notes: list[str] = []
    if final_url != normalized_url:
        warning_notes.append(
            f"cloakbrowser_snapshot landed at {final_url} from requested URL {normalized_url}"
        )
    warning_notes.extend(
        _sanitize_engine_warning_notes(engine_result.warning_notes, proxy_profile=proxy_profile)
    )
    access_block_reason = _detect_access_blocked_page(
        title=engine_result.title,
        rendered_dom=engine_result.rendered_dom,
        visible_text=engine_result.visible_text,
    )
    limitation_notes: list[str] = []
    if access_block_reason is not None:
        limitation_notes.append(
            "access_failed: CloakBrowser rendered an access-block/interstitial page "
            f"instead of source content: {access_block_reason}; block artifacts preserved"
        )

    metadata = {
        "requested_url": normalized_url,
        "final_url": final_url,
        "title": engine_result.title,
        "capture_timestamp": utc_now_z(),
        "timeout_seconds": timeout_seconds,
        "wait_until": wait_until,
        "settle_seconds": settle_seconds,
        "scroll_passes": scroll_passes,
        "scroll_step_px": scroll_step_px,
        "load_more_selector": load_more_selector,
        "load_more_clicks": load_more_clicks,
        "viewport_width": viewport_width,
        "viewport_height": viewport_height,
        "screenshot_mode": "viewport",
        "method_category": CLOAKBROWSER_METHOD_CATEGORY,
        "browser_engine": "cloakbrowser",
        "cloakbrowser_backend": CLOAKBROWSER_BACKEND,
        "profile_persistence": "none",
        "storage_state_loaded": False,
        "proxy_used": proxy_profile is not None,
        "proxy_category": proxy_profile.proxy_category.value if proxy_profile is not None else None,
        "proxy_disclosure": "category_only" if proxy_profile is not None else "none",
        "proxy_endpoint_recorded": False,
        "proxy_exit_ip_recorded": False,
        "geoip_used": proxy_profile.geoip_enabled if proxy_profile is not None else False,
        "proxy_timezone": proxy_profile.timezone if proxy_profile is not None else None,
        "proxy_locale": proxy_profile.locale if proxy_profile is not None else None,
        "extension_paths_loaded": False,
        "heavy_assets_blocked": block_heavy_assets,
        "blocked_resource_types": sorted(HEAVY_RESOURCE_TYPES) if block_heavy_assets else [],
        "access_blocked": access_block_reason is not None,
        "access_block_reason": access_block_reason,
        "rendered_dom_byte_count": artifact_sizes["rendered_dom"],
        "visible_text_byte_count": artifact_sizes["visible_text"],
        "screenshot_byte_count": artifact_sizes["screenshot_png"],
    }

    return CloakBrowserSnapshotSuccess(
        requested_url=normalized_url,
        final_url=final_url,
        title=engine_result.title,
        rendered_dom=engine_result.rendered_dom,
        visible_text=engine_result.visible_text,
        screenshot_png=engine_result.screenshot_png,
        metadata=metadata,
        warning_notes=warning_notes,
        limitation_notes=limitation_notes,
        access_block_reason=access_block_reason,
    )


class _CloakBrowserSnapshotEngine:
    def capture(
        self,
        *,
        url: str,
        timeout_seconds: float,
        wait_until: str,
        viewport_width: int,
        viewport_height: int,
        proxy_profile: ProxyProfile | None,
        block_heavy_assets: bool,
        settle_seconds: float = 0.0,
        scroll_passes: int = 0,
        load_more_selector: str | None = None,
        load_more_clicks: int = 0,
        scroll_step_px: int = 0,
    ) -> CloakBrowserSnapshotEngineResult:
        try:
            cloakbrowser = import_module("cloakbrowser")
        except ModuleNotFoundError as exc:
            raise _CloakBrowserSnapshotDependencyUnavailable(
                "CloakBrowser is not installed. Install the cloakbrowser optional dependency before "
                "running CloakBrowser snapshots."
            ) from exc

        launch = getattr(cloakbrowser, "launch", None)
        if not callable(launch):
            raise _CloakBrowserSnapshotDependencyUnavailable(
                "CloakBrowser is installed but does not expose cloakbrowser.launch. "
                "Install a compatible cloakbrowser package before running CloakBrowser snapshots."
            )

        timeout_ms = timeout_seconds * 1000
        try:
            browser = launch(
                headless=True,
                proxy=proxy_profile.proxy_endpoint if proxy_profile is not None else None,
                args=None,
                stealth_args=True,
                timezone=proxy_profile.timezone if proxy_profile is not None else None,
                locale=proxy_profile.locale if proxy_profile is not None else None,
                geoip=proxy_profile.geoip_enabled if proxy_profile is not None else False,
                backend=CLOAKBROWSER_BACKEND,
                humanize=False,
                extension_paths=None,
            )
        except Exception as exc:
            if _looks_like_cloakbrowser_dependency_failure(exc):
                raise _CloakBrowserSnapshotDependencyUnavailable(
                    f"CloakBrowser dependency unavailable: {exc}"
                ) from exc
            raise

        try:
            context = browser.new_context(
                viewport={
                    "width": viewport_width,
                    "height": viewport_height,
                }
            )
            try:
                page = context.new_page()
                if block_heavy_assets:
                    page.route(
                        "**/*",
                        lambda route: (
                            route.abort()
                            if route.request.resource_type in HEAVY_RESOURCE_TYPES
                            else route.continue_()
                        ),
                    )
                page.goto(url, wait_until=wait_until, timeout=timeout_ms)
                if settle_seconds > 0:
                    page.wait_for_timeout(settle_seconds * 1000)
                if scroll_step_px > 0:
                    position = 0
                    for _ in range(_MAX_PROGRESSIVE_SCROLL_STEPS):
                        height = page.evaluate("() => document.body.scrollHeight")
                        if position >= height:
                            break
                        position += scroll_step_px
                        page.evaluate("(y) => window.scrollTo(0, y)", position)
                        page.wait_for_timeout(_PROGRESSIVE_SCROLL_PAUSE_MS)
                for _ in range(scroll_passes):
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    page.wait_for_timeout(_SCROLL_PASS_SETTLE_MS)
                if load_more_selector and load_more_clicks > 0:
                    for _ in range(load_more_clicks):
                        if page.locator(load_more_selector).count() == 0:
                            break
                        try:
                            page.locator(load_more_selector).first.click(timeout=_LOAD_MORE_CLICK_TIMEOUT_MS)
                        except Exception:
                            break
                        page.wait_for_timeout(_SCROLL_PASS_SETTLE_MS)
                rendered_dom = page.content()
                warning_notes: list[str] = []
                try:
                    visible_text = page.locator("body").inner_text(timeout=timeout_ms)
                except Exception as exc:
                    visible_text = ""
                    warning_notes.append(f"cloakbrowser_snapshot visible_text extraction failed: {exc}")
                screenshot_png = page.screenshot(
                    type="png",
                    full_page=False,
                    timeout=timeout_ms,
                )
                return _LiveEngineResult(
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


@dataclass(frozen=True)
class _LiveEngineResult:
    final_url: str
    title: str | None
    rendered_dom: str
    visible_text: str
    screenshot_png: bytes
    warning_notes: list[str] = field(default_factory=list)


class _CloakBrowserSnapshotDependencyUnavailable(RuntimeError):
    pass


def _validate_http_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("CloakBrowser snapshot capture requires an absolute http:// or https:// URL")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("CloakBrowser snapshot capture does not accept URLs with embedded credentials")
    return parsed.geturl()


def _sanitize_engine_final_url(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return url
    if parsed.username is not None or parsed.password is not None:
        return None

    redacted_query: list[tuple[str, str]] = []
    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        if _is_secret_like_key(key):
            redacted_query.append((key, "[redacted]"))
        else:
            redacted_query.append((key, value))
    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            urlencode(redacted_query, doseq=True),
            parsed.fragment,
        )
    )


def _sanitize_engine_warning_notes(
    notes: list[str], *, proxy_profile: ProxyProfile | None = None
) -> list[str]:
    sanitized: list[str] = []
    for note in notes:
        lowered = note.lower()
        if any(term in lowered for term in SECRET_LIKE_WARNING_TERMS):
            sanitized.append("cloakbrowser_snapshot engine warning redacted because it contained secret-like text")
        else:
            sanitized.append(_redact_proxy_secret(note, proxy_profile=proxy_profile))
    return sanitized


def _redact_proxy_secret(text: str, *, proxy_profile: ProxyProfile | None) -> str:
    """Strip the in-memory proxy endpoint and its credentials out of operator-
    facing text before it can reach a failure message, CLI output, log, warning
    note, or packet artifact.

    The proxy endpoint string is handed straight to the CloakBrowser launch
    call, so a launch, connection, or dependency exception can echo it (and the
    embedded credentials) verbatim. This is the single point where engine and
    dependency strings are turned into surfaced text, so any endpoint substring
    is masked here. Full endpoint, password, and host[:port] are all redacted so
    a reformatted echo (host-only, credential-only) is also covered; over-
    redaction of a failure string is acceptable, leaking the endpoint is not.
    """
    if proxy_profile is None:
        return text
    endpoint = proxy_profile.proxy_endpoint
    if not endpoint:
        return text
    redacted = text.replace(endpoint, "[redacted-proxy-endpoint]")
    parsed = urlparse(endpoint)
    if parsed.password:
        redacted = redacted.replace(parsed.password, "[redacted-proxy-credential]")
    host = parsed.hostname
    if host:
        if parsed.port is not None:
            redacted = redacted.replace(f"{host}:{parsed.port}", "[redacted-proxy-endpoint]")
        redacted = redacted.replace(host, "[redacted-proxy-endpoint]")
    return redacted


def _detect_access_blocked_page(
    *,
    title: str | None,
    rendered_dom: str,
    visible_text: str,
) -> str | None:
    title_text = (title or "").strip().lower()
    body_text = visible_text.strip().lower()
    probe_text = f"{title_text}\n{body_text}\n{rendered_dom[:5000].lower()}"
    if (
        "you've been blocked by network security" in probe_text
        and "file a ticket" in probe_text
    ):
        return "reddit_network_security_block"
    return None


def _is_secret_like_key(key: str) -> bool:
    lowered = key.lower()
    return any(term in lowered for term in SECRET_LIKE_QUERY_KEYS)


def _validate_positive_number(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")


def _validate_positive_int(name: str, value: int) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")


def _failure_kind_from_exception(error: Exception) -> CloakBrowserSnapshotFailureKind:
    text = f"{type(error).__name__}: {error}".lower()
    if "timeout" in text or "timed out" in text:
        return CloakBrowserSnapshotFailureKind.TIMEOUT
    return CloakBrowserSnapshotFailureKind.CAPTURE_FAILED


def _looks_like_cloakbrowser_dependency_failure(error: Exception) -> bool:
    text = f"{type(error).__name__}: {error}".lower()
    if "geoip2" in text or "socksio" in text:
        return True
    return "cloakbrowser" in text and (
        "binary" in text
        or "chromium" in text
        or "download" in text
        or "executable" in text
        or "not found" in text
    )
