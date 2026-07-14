from __future__ import annotations

import io
import json
import shutil
import uuid
from dataclasses import dataclass, field
from pathlib import Path

import pytest

import source_capture.adapters.browser_snapshot as browser_snapshot_module
from runners import run_source_capture_browser_packet as browser_runner
from runners.run_source_capture_browser_packet import BROWSER_SNAPSHOT_NON_CLAIMS
from source_capture import CaptureModeCategory
from source_capture.adapters.browser_snapshot import (
    BrowserContextRequest,
    BrowserContextResponse,
    BrowserContextResponsesSuccess,
    BrowserPageObservationSuccess,
    BrowserPagePointerAction,
    BrowserPageWheelAction,
    BrowserPageResponse,
    BrowserSnapshotFailure,
    BrowserSnapshotFailureKind,
    BrowserSnapshotSuccess,
    CloakBrowserPageObservationSessionEngine,
    ChromeCdpPageObservationSessionEngine,
    fetch_browser_context_responses,
    fetch_browser_page_observation_capture,
    fetch_browser_snapshot_capture,
)
from source_capture.proxy_profiles import ProxyCategory, ProxyProfile
from source_capture.source_detail_sufficiency import SourceDetailSufficiencyRequirements


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"source_capture_browser_snapshot_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


@dataclass(frozen=True)
class _FakeEngineResult:
    final_url: str
    title: str | None
    rendered_dom: str
    visible_text: str
    screenshot_png: bytes
    warning_notes: list[str] = field(default_factory=list)


class _FakeBrowserEngine:
    def __init__(self, result: _FakeEngineResult | Exception) -> None:
        self.result = result
        self.capture_kwargs: dict[str, object] | None = None

    def capture(self, **kwargs: object) -> _FakeEngineResult:
        self.capture_kwargs = dict(kwargs)
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


class _FakeContextResponseEngine:
    def __init__(self, result: BrowserContextResponsesSuccess | Exception) -> None:
        self.result = result
        self.capture_kwargs: dict[str, object] | None = None

    def capture_context_responses(self, **kwargs: object) -> BrowserContextResponsesSuccess:
        self.capture_kwargs = dict(kwargs)
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


class _FakePageObservationEngine:
    def __init__(self, result: BrowserPageObservationSuccess | Exception) -> None:
        self.result = result
        self.capture_kwargs: dict[str, object] | None = None

    def capture_page_observation(self, **kwargs: object) -> BrowserPageObservationSuccess:
        self.capture_kwargs = dict(kwargs)
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


class _FakeLazyScrollPage:
    def __init__(self, *, height: int = 3_000) -> None:
        self.height = height
        self.scrolled_to: list[object] = []
        self.waits: list[int] = []

    def evaluate(self, script: str, arg: object | None = None) -> int | None:
        if "scrollTo" in script:
            self.scrolled_to.append(arg if arg is not None else "bottom")
            return None
        if "scrollHeight" in script:
            return self.height
        return None

    def wait_for_timeout(self, timeout_ms: int) -> None:
        self.waits.append(timeout_ms)


class _FakeObservationRequest:
    def __init__(self, *, method: str = "GET", resource_type: str = "fetch") -> None:
        self.method = method
        self.resource_type = resource_type


class _FakeObservationResponse:
    def __init__(
        self,
        event_log: list[str],
        *,
        url: str = "https://api.example.test/widget",
        method: str = "GET",
        resource_type: str = "fetch",
    ) -> None:
        self.event_log = event_log
        self.url = url
        self.status = 200
        self.ok = True
        self.headers = {"content-type": "application/json"}
        self.request = _FakeObservationRequest(method=method, resource_type=resource_type)

    def text(self) -> str:
        self.event_log.append("response_text")
        return "{}"


class _FakeObservationLocator:
    def __init__(self, event_log: list[str]) -> None:
        self.event_log = event_log

    def inner_text(self, *, timeout: float) -> str:
        self.event_log.append("inner_text")
        return "before scroll"


class _FakeObservationMouse:
    def __init__(self, page: "_FakeObservationPage") -> None:
        self.page = page
        self.moves: list[tuple[float, float, int]] = []
        self.clicks: list[tuple[float, float]] = []
        self.wheels: list[tuple[float, float]] = []

    def move(self, x: float, y: float, *, steps: int = 1) -> None:
        self.moves.append((x, y, steps))
        self.page.event_log.append(f"mouse_move:{steps}")

    def click(self, x: float, y: float) -> None:
        self.clicks.append((x, y))
        self.page.event_log.append("mouse_click")
        self.page.emit_response_once()

    def wheel(self, delta_x: float, delta_y: float) -> None:
        self.wheels.append((delta_x, delta_y))
        self.page.scroll_y = max(0.0, self.page.scroll_y + delta_y)
        self.page.event_log.append("mouse_wheel")


class _FakeObservationPage:
    def __init__(
        self,
        event_log: list[str],
        *,
        height: int = 3_000,
        pointer_target: dict[str, object] | None = None,
        pointer_targets: list[dict[str, object]] | None = None,
        screenshot_png: bytes = b"",
        screenshot_pngs: list[bytes] | None = None,
        post_click_absence_result: dict[str, object] | None = None,
        marker_match_results: list[dict[str, object]] | None = None,
        response_url: str = "https://api.example.test/widget",
        response_method: str = "GET",
        response_resource_type: str = "fetch",
    ) -> None:
        self.event_log = event_log
        self.height = height
        self.scroll_y = 0.0
        self.url = "https://example.com/source"
        self.response_callback: object | None = None
        self.route_bindings: list[tuple[str, object]] = []
        self.response_emitted = False
        self.pointer_target = pointer_target
        self.pointer_targets = list(pointer_targets or [])
        self.screenshot_png = screenshot_png
        self.screenshot_pngs = list(screenshot_pngs or [])
        self.response_url = response_url
        self.response_method = response_method
        self.response_resource_type = response_resource_type
        self.post_click_absence_result = post_click_absence_result or {
            "checked": True,
            "marker_count": 0,
            "absent": True,
            "matched_marker": None,
        }
        self.marker_match_results = list(marker_match_results or [])
        self.mouse = _FakeObservationMouse(self)

    def route(self, pattern: str, handler: object) -> None:
        self.route_bindings.append((pattern, handler))
        self.event_log.append("route")

    def unroute(self, pattern: str, handler: object) -> None:
        assert (pattern, handler) in self.route_bindings
        self.route_bindings.remove((pattern, handler))
        self.event_log.append("unroute")

    def on(self, event: str, callback: object) -> None:
        assert event == "response"
        self.response_callback = callback

    def remove_listener(self, event: str, callback: object) -> None:
        assert event == "response"
        assert self.response_callback is callback
        self.response_callback = None
        self.event_log.append("remove_listener")

    def goto(self, *_args: object, **_kwargs: object) -> None:
        self.event_log.append("goto")

    def wait_for_timeout(self, timeout_ms: float) -> None:
        self.event_log.append(f"wait:{int(timeout_ms)}")

    def wait_for_selector(self, *_args: object, **_kwargs: object) -> None:
        self.event_log.append("wait_for_selector")

    def screenshot(self, **_kwargs: object) -> bytes:
        self.event_log.append("screenshot")
        if self.screenshot_pngs:
            return self.screenshot_pngs.pop(0)
        return self.screenshot_png

    def emit_response_once(self) -> None:
        if self.response_callback is not None and not self.response_emitted:
            self.response_callback(
                _FakeObservationResponse(
                    self.event_log,
                    url=self.response_url,
                    method=self.response_method,
                    resource_type=self.response_resource_type,
                )
            )  # type: ignore[operator]
            self.response_emitted = True

    def locator(self, selector: str) -> _FakeObservationLocator:
        assert selector == "body"
        return _FakeObservationLocator(self.event_log)

    def evaluate(self, script: str, arg: object | None = None) -> object:
        if "viewport_width" in script and "viewport_height" in script:
            self.event_log.append("wheel_viewport_lookup")
            return {
                "scroll_y": self.scroll_y,
                "viewport_width": 1280,
                "viewport_height": 720,
            }
        if "scroll_y: Math.max" in script:
            self.event_log.append("wheel_after_lookup")
            return {"scroll_y": self.scroll_y}
        if "scrollTo" in script:
            self.event_log.append("scroll")
            self.emit_response_once()
            return None
        if "scrollHeight" in script:
            self.event_log.append("scroll_height")
            return self.height
        if "postLoadAction" in script:
            self.event_log.append("post_load_action")
            self.emit_response_once()
            return {"postLoadAction": arg}
        if "human_challenge_marker_match" in script:
            self.event_log.append("human_marker_match")
            if self.marker_match_results:
                return self.marker_match_results.pop(0)
            return {
                "checked": True,
                "matched": False,
                "matched_marker": None,
                "marker_count": 0,
            }
        if "matched_marker" in script and "absent" in script:
            self.event_log.append("post_click_absence_lookup")
            return self.post_click_absence_result
        if "candidate_selector" in script and "target_found" in script:
            self.event_log.append("pointer_target_lookup")
            if self.pointer_targets:
                return self.pointer_targets.pop(0)
            return self.pointer_target or {
                "candidate_count": 0,
                "matched_count": 0,
                "target_found": False,
                "target_kind": None,
                "box": None,
            }
        self.event_log.append("dom_extract")
        return {"items": [{"text": "before scroll"}]}

    def title(self) -> str:
        return "Rendered Source"


class _FakeObservationContext:
    def __init__(self, page: _FakeObservationPage) -> None:
        self.page = page

    def new_page(self) -> _FakeObservationPage:
        self.page.event_log.append("new_page")
        return self.page

    def close(self) -> None:
        self.page.event_log.append("context_close")


class _FakeObservationBrowser:
    def __init__(self, page: _FakeObservationPage) -> None:
        self.page = page

    def new_context(self, **_kwargs: object) -> _FakeObservationContext:
        return _FakeObservationContext(self.page)

    def close(self) -> None:
        self.page.event_log.append("browser_close")


class _FakeObservationChromium:
    def __init__(self, page: _FakeObservationPage) -> None:
        self.page = page

    def launch(self, **_kwargs: object) -> _FakeObservationBrowser:
        return _FakeObservationBrowser(self.page)


class _FakeObservationPlaywright:
    def __init__(self, page: _FakeObservationPage) -> None:
        self.chromium = _FakeObservationChromium(page)


class _FakeSyncPlaywright:
    def __init__(self, page: _FakeObservationPage) -> None:
        self.page = page

    def __enter__(self) -> _FakeObservationPlaywright:
        return _FakeObservationPlaywright(self.page)

    def __exit__(self, *_args: object) -> None:
        return None


class _FakePlaywrightSyncApi:
    def __init__(self, page: _FakeObservationPage) -> None:
        self.page = page

    def sync_playwright(self) -> _FakeSyncPlaywright:
        return _FakeSyncPlaywright(self.page)


class _FakeCloakBrowserModule:
    def __init__(self, page: _FakeObservationPage) -> None:
        self.page = page
        self.launch_kwargs: dict[str, object] | None = None

    def launch(self, **kwargs: object) -> _FakeObservationBrowser:
        self.launch_kwargs = dict(kwargs)
        return _FakeObservationBrowser(self.page)


def _install_fake_playwright(monkeypatch: pytest.MonkeyPatch, page: _FakeObservationPage) -> None:
    original_import_module = browser_snapshot_module.import_module

    def fake_import_module(name: str) -> object:
        if name == "playwright.sync_api":
            return _FakePlaywrightSyncApi(page)
        return original_import_module(name)

    monkeypatch.setattr(browser_snapshot_module, "import_module", fake_import_module)


def _visual_x_screenshot_png() -> bytes:
    from PIL import Image, ImageDraw

    image = Image.new("RGB", (240, 120), "white")
    draw = ImageDraw.Draw(image)
    draw.line((198, 10, 220, 32), fill="black", width=3)
    draw.line((220, 10, 198, 32), fill="black", width=3)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def _visual_x_modal_and_far_right_screenshot_png() -> bytes:
    from PIL import Image, ImageDraw

    image = Image.new("RGB", (240, 120), "white")
    draw = ImageDraw.Draw(image)
    draw.line((148, 14, 166, 32), fill="black", width=3)
    draw.line((166, 14, 148, 32), fill="black", width=3)
    draw.line((218, 8, 236, 26), fill="black", width=3)
    draw.line((236, 8, 218, 26), fill="black", width=3)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def _blank_screenshot_png() -> bytes:
    from PIL import Image

    image = Image.new("RGB", (240, 120), "white")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def test_fetch_browser_snapshot_capture_with_fake_engine_preserves_browser_artifacts() -> None:
    result = fetch_browser_snapshot_capture(
        url="https://example.com/source",
        timeout_seconds=5,
        wait_until="domcontentloaded",
        viewport_width=1024,
        viewport_height=768,
        max_artifact_bytes=10_000,
        engine=_FakeBrowserEngine(
            _FakeEngineResult(
                final_url="https://example.com/rendered",
                title="Rendered Source",
                rendered_dom="<html><body><h1>Rendered source</h1></body></html>",
                visible_text="Rendered source",
                screenshot_png=b"\x89PNG\r\n\x1a\nbrowser",
            )
        ),
    )

    assert isinstance(result, BrowserSnapshotSuccess)
    assert result.requested_url == "https://example.com/source"
    assert result.final_url == "https://example.com/rendered"
    assert result.warning_notes == [
        "browser_snapshot landed at https://example.com/rendered from requested URL https://example.com/source"
    ]
    assert result.metadata["wait_until"] == "domcontentloaded"
    assert result.metadata["viewport_width"] == 1024
    assert result.metadata["viewport_height"] == 768
    assert result.metadata["screenshot_mode"] == "viewport"
    assert result.metadata["settle_seconds"] == 0.0
    assert result.metadata["headless"] is True
    assert result.metadata["browser_channel"] is None
    assert result.metadata["access_blocked"] is False
    assert result.metadata["access_block_reason"] is None
    assert result.metadata["rendered_access_classification"] == "no_block_marker"
    assert result.metadata["storage_state_loaded"] is False
    assert result.metadata["rendered_dom_byte_count"] == len(result.rendered_dom.encode("utf-8"))
    assert result.metadata["visible_text_byte_count"] == len(result.visible_text.encode("utf-8"))
    assert result.metadata["screenshot_byte_count"] == len(result.screenshot_png)


def test_fetch_browser_snapshot_capture_passes_storage_state_without_recording_path(
    scratch_dir: Path,
) -> None:
    state_path = scratch_dir / "state.json"
    state_path.write_text('{"cookies": [], "origins": []}', encoding="utf-8")
    engine = _FakeBrowserEngine(
        _FakeEngineResult(
            final_url="https://example.com/rendered",
            title="Rendered Source",
            rendered_dom="<html><body><h1>Rendered source</h1></body></html>",
            visible_text="Rendered source",
            screenshot_png=b"\x89PNG\r\n\x1a\nbrowser",
        )
    )

    result = fetch_browser_snapshot_capture(
        url="https://example.com/source",
        storage_state_path=state_path,
        engine=engine,
    )

    assert isinstance(result, BrowserSnapshotSuccess)
    assert engine.capture_kwargs is not None
    assert engine.capture_kwargs["storage_state_path"] == state_path
    assert result.metadata["storage_state_loaded"] is True
    assert str(state_path) not in json.dumps(result.metadata)


def test_fetch_browser_snapshot_capture_passes_proxy_without_recording_secret() -> None:
    proxy = ProxyProfile(
        proxy_endpoint="http://proxy_user:proxy_pass@example.proxy.test:1234",
        proxy_category=ProxyCategory.RESIDENTIAL_ROTATING,
        geoip_enabled=False,
        timezone="America/New_York",
        locale="en-US",
    )
    engine = _FakeBrowserEngine(
        _FakeEngineResult(
            final_url="https://example.com/rendered",
            title="Rendered Source",
            rendered_dom="<html><body><h1>Rendered source</h1></body></html>",
            visible_text="Rendered source",
            screenshot_png=b"\x89PNG\r\n\x1a\nbrowser",
        )
    )

    result = fetch_browser_snapshot_capture(
        url="https://example.com/source",
        proxy_profile=proxy,
        engine=engine,
    )

    assert isinstance(result, BrowserSnapshotSuccess)
    assert engine.capture_kwargs is not None
    assert engine.capture_kwargs["proxy_profile"] is proxy
    assert result.metadata["proxy_used"] is True
    assert result.metadata["proxy_category"] == "residential_rotating"
    assert result.metadata["proxy_disclosure"] == "category_only"
    assert result.metadata["proxy_endpoint_recorded"] is False
    assert result.metadata["proxy_exit_ip_recorded"] is False
    serialized = json.dumps(result.metadata)
    assert "example.proxy.test" not in serialized
    assert "proxy_user" not in serialized
    assert "proxy_pass" not in serialized


def test_fetch_browser_context_responses_preserves_status_and_body() -> None:
    engine = _FakeContextResponseEngine(
        BrowserContextResponsesSuccess(
            page_url="https://www.instagram.com/hyram/",
            final_page_url="https://www.instagram.com/hyram/",
            responses=[
                BrowserContextResponse(
                    request_id="web_profile_info",
                    requested_url="https://www.instagram.com/api/v1/users/web_profile_info/?username=hyram",
                    final_url="https://www.instagram.com/api/v1/users/web_profile_info/?username=hyram",
                    status=429,
                    ok=False,
                    body_text="",
                    response_headers={"content-type": "application/json"},
                )
            ],
            metadata={"request_count": 1},
            warning_notes=[],
            limitation_notes=[],
        )
    )

    result = fetch_browser_context_responses(
        page_url="https://www.instagram.com/hyram/",
        requests=[
            BrowserContextRequest(
                request_id="web_profile_info",
                url="https://www.instagram.com/api/v1/users/web_profile_info/?username=hyram",
                headers={"X-IG-App-ID": "936619743392459"},
            )
        ],
        timeout_seconds=7,
        max_response_bytes=100,
        engine=engine,
    )

    assert isinstance(result, BrowserContextResponsesSuccess)
    assert engine.capture_kwargs is not None
    assert engine.capture_kwargs["requests"][0].headers == {"X-IG-App-ID": "936619743392459"}
    assert result.responses[0].status == 429
    assert result.responses[0].ok is False


def test_fetch_browser_context_responses_threads_proxy_to_engine() -> None:
    proxy = ProxyProfile(
        proxy_endpoint="http://proxy_user:proxy_pass@example.proxy.test:1234",
        proxy_category=ProxyCategory.RESIDENTIAL_ROTATING,
        geoip_enabled=False,
    )
    engine = _FakeContextResponseEngine(
        BrowserContextResponsesSuccess(
            page_url="https://www.instagram.com/hyram/",
            final_page_url="https://www.instagram.com/hyram/",
            responses=[
                BrowserContextResponse(
                    request_id="web_profile_info",
                    requested_url="https://www.instagram.com/api/v1/users/web_profile_info/?username=hyram",
                    final_url="https://www.instagram.com/api/v1/users/web_profile_info/?username=hyram",
                    status=200,
                    ok=True,
                    body_text="{}",
                    response_headers={"content-type": "application/json"},
                )
            ],
            metadata={},
            warning_notes=[],
            limitation_notes=[],
        )
    )

    result = fetch_browser_context_responses(
        page_url="https://www.instagram.com/hyram/",
        requests=[
            BrowserContextRequest(
                request_id="web_profile_info",
                url="https://www.instagram.com/api/v1/users/web_profile_info/?username=hyram",
            )
        ],
        proxy_profile=proxy,
        engine=engine,
    )

    assert isinstance(result, BrowserContextResponsesSuccess)
    assert engine.capture_kwargs is not None
    assert engine.capture_kwargs["proxy_profile"] is proxy


def test_fetch_browser_context_responses_enforces_response_body_size_cap() -> None:
    result = fetch_browser_context_responses(
        page_url="https://www.instagram.com/hyram/",
        requests=[
            BrowserContextRequest(
                request_id="web_profile_info",
                url="https://www.instagram.com/api/v1/users/web_profile_info/?username=hyram",
            )
        ],
        max_response_bytes=2,
        engine=_FakeContextResponseEngine(
            BrowserContextResponsesSuccess(
                page_url="https://www.instagram.com/hyram/",
                final_page_url="https://www.instagram.com/hyram/",
                responses=[
                    BrowserContextResponse(
                        request_id="web_profile_info",
                        requested_url="https://www.instagram.com/api/v1/users/web_profile_info/?username=hyram",
                        final_url="https://www.instagram.com/api/v1/users/web_profile_info/?username=hyram",
                        status=200,
                        ok=True,
                        body_text="too large",
                        response_headers={},
                    )
                ],
                metadata={},
                warning_notes=[],
                limitation_notes=[],
            )
        ),
    )

    assert isinstance(result, BrowserSnapshotFailure)
    assert result.failure_kind == BrowserSnapshotFailureKind.SIZE_CAP_EXCEEDED
    assert "web_profile_info" in result.message


def test_fetch_browser_snapshot_capture_returns_size_cap_failure() -> None:
    result = fetch_browser_snapshot_capture(
        url="https://example.com/source",
        max_artifact_bytes=5,
        engine=_FakeBrowserEngine(
            _FakeEngineResult(
                final_url="https://example.com/source",
                title=None,
                rendered_dom="<html><body>ok</body></html>",
                visible_text="ok",
                screenshot_png=b"x" * 51,
            )
        ),
    )

    assert isinstance(result, BrowserSnapshotFailure)
    assert result.failure_kind == BrowserSnapshotFailureKind.SIZE_CAP_EXCEEDED
    assert "screenshot_png=51" in result.message


def test_fetch_browser_snapshot_capture_carries_engine_warnings() -> None:
    result = fetch_browser_snapshot_capture(
        url="https://example.com/source",
        engine=_FakeBrowserEngine(
            _FakeEngineResult(
                final_url="https://example.com/source",
                title=None,
                rendered_dom="<html><body>ok</body></html>",
                visible_text="",
                screenshot_png=b"\x89PNG\r\n\x1a\nbrowser",
                warning_notes=["browser_snapshot visible_text extraction failed: synthetic locator error"],
            )
        ),
    )

    assert isinstance(result, BrowserSnapshotSuccess)
    assert result.warning_notes == ["browser_snapshot visible_text extraction failed: synthetic locator error"]


def test_fetch_browser_snapshot_capture_classifies_timeout() -> None:
    result = fetch_browser_snapshot_capture(
        url="https://example.com/source",
        engine=_FakeBrowserEngine(TimeoutError("navigation timed out")),
    )

    assert isinstance(result, BrowserSnapshotFailure)
    assert result.failure_kind == BrowserSnapshotFailureKind.TIMEOUT


def test_fetch_browser_snapshot_capture_classifies_permission_denied_as_environment_failure() -> None:
    result = fetch_browser_snapshot_capture(
        url="https://example.com/source",
        engine=_FakeBrowserEngine(PermissionError(13, "Access is denied")),
    )

    assert isinstance(result, BrowserSnapshotFailure)
    assert result.failure_kind == BrowserSnapshotFailureKind.ENVIRONMENT_PERMISSION_DENIED
    assert "browser subprocess startup was denied" in result.message
    assert "before source access" in result.message


def test_fetch_browser_context_responses_classifies_fetch_abort_as_timeout() -> None:
    result = fetch_browser_context_responses(
        page_url="https://www.instagram.com/hyram/",
        requests=[
            BrowserContextRequest(
                request_id="web_profile_info",
                url="https://www.instagram.com/api/v1/users/web_profile_info/?username=hyram",
            )
        ],
        timeout_seconds=3,
        engine=_FakeContextResponseEngine(RuntimeError("AbortError: The operation was aborted")),
    )

    assert isinstance(result, BrowserSnapshotFailure)
    assert result.failure_kind == BrowserSnapshotFailureKind.TIMEOUT


def test_fetch_browser_context_responses_classifies_permission_denied_as_environment_failure() -> None:
    result = fetch_browser_context_responses(
        page_url="https://www.instagram.com/hyram/",
        requests=[
            BrowserContextRequest(
                request_id="web_profile_info",
                url="https://www.instagram.com/api/v1/users/web_profile_info/?username=hyram",
            )
        ],
        engine=_FakeContextResponseEngine(PermissionError(13, "Access is denied")),
    )

    assert isinstance(result, BrowserSnapshotFailure)
    assert result.failure_kind == BrowserSnapshotFailureKind.ENVIRONMENT_PERMISSION_DENIED
    assert "browser subprocess startup was denied" in result.message
    assert "before source access" in result.message


def test_fetch_browser_snapshot_capture_returns_empty_rendered_dom_failure() -> None:
    result = fetch_browser_snapshot_capture(
        url="https://example.com/source",
        engine=_FakeBrowserEngine(
            _FakeEngineResult(
                final_url="https://example.com/source",
                title=None,
                rendered_dom="",
                visible_text="text without dom",
                screenshot_png=b"\x89PNG\r\n\x1a\nbrowser",
            )
        ),
    )

    assert isinstance(result, BrowserSnapshotFailure)
    assert result.failure_kind == BrowserSnapshotFailureKind.EMPTY_RENDERED_DOM
    assert "empty rendered DOM" in result.message


def test_fetch_browser_snapshot_capture_returns_empty_screenshot_failure() -> None:
    result = fetch_browser_snapshot_capture(
        url="https://example.com/source",
        engine=_FakeBrowserEngine(
            _FakeEngineResult(
                final_url="https://example.com/source",
                title=None,
                rendered_dom="<html><body>ok</body></html>",
                visible_text="ok",
                screenshot_png=b"",
            )
        ),
    )

    assert isinstance(result, BrowserSnapshotFailure)
    assert result.failure_kind == BrowserSnapshotFailureKind.EMPTY_SCREENSHOT
    assert "empty screenshot" in result.message


def test_fetch_browser_snapshot_capture_rejects_embedded_credentials_url() -> None:
    with pytest.raises(ValueError, match="embedded credentials"):
        fetch_browser_snapshot_capture(
            url="https://user:pass@example.com/source",
            engine=_FakeBrowserEngine(
                _FakeEngineResult(
                    final_url="https://example.com/source",
                    title=None,
                    rendered_dom="<html><body>ok</body></html>",
                    visible_text="ok",
                    screenshot_png=b"\x89PNG\r\n\x1a\nbrowser",
                )
            ),
        )


def _ok_engine() -> _FakeBrowserEngine:
    return _FakeBrowserEngine(
        _FakeEngineResult(
            final_url="https://example.com/source",
            title=None,
            rendered_dom="<html><body>ok</body></html>",
            visible_text="ok",
            screenshot_png=b"\x89PNG\r\n\x1a\nbrowser",
        )
    )


def _ok_page_observation_engine() -> _FakePageObservationEngine:
    return _FakePageObservationEngine(
        BrowserPageObservationSuccess(
            requested_url="https://example.com/source",
            final_url="https://example.com/source",
            title="Rendered Source",
            visible_text="Rendered source",
            dom_observation={"items": []},
            responses=[
                BrowserPageResponse(
                    requested_url="https://api.example.test/widget",
                    final_url="https://api.example.test/widget",
                    status=200,
                    ok=True,
                    body_text="{}",
                    response_headers={},
                )
            ],
            metadata={"response_count": 1},
            warning_notes=[],
            limitation_notes=[],
        )
    )


def test_fetch_browser_page_observation_capture_threads_lazy_load_scroll_controls_to_engine() -> None:
    engine = _ok_page_observation_engine()

    result = fetch_browser_page_observation_capture(
        url="https://example.com/source",
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_action_script="() => true",
        post_load_action_arg={"target": "comments"},
        lazy_load_scroll_passes=2,
        lazy_load_scroll_step_px=650,
        engine=engine,
    )

    assert isinstance(result, BrowserPageObservationSuccess)
    assert engine.capture_kwargs is not None
    assert engine.capture_kwargs["post_load_action_script"] == "() => true"
    assert engine.capture_kwargs["post_load_action_arg"] == {"target": "comments"}
    assert engine.capture_kwargs["post_load_pointer_action"] is None
    assert engine.capture_kwargs["lazy_load_scroll_passes"] == 2
    assert engine.capture_kwargs["lazy_load_scroll_step_px"] == 650


def test_fetch_browser_page_observation_capture_threads_pointer_action_to_engine() -> None:
    engine = _ok_page_observation_engine()
    pointer_action = BrowserPagePointerAction(
        action_name=" open_comments ",
        candidate_selector=" button ",
        text_markers=(" Comments ",),
        page_text_markers=(" Drag the slider ",),
        exact_text_markers=(" X ",),
        random_seed=7,
        prefer_top_right=True,
    )

    result = fetch_browser_page_observation_capture(
        url="https://example.com/source",
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_action=pointer_action,
        engine=engine,
    )

    assert isinstance(result, BrowserPageObservationSuccess)
    assert engine.capture_kwargs is not None
    assert engine.capture_kwargs["post_load_action_script"] is None
    assert engine.capture_kwargs["post_load_pointer_action"] == BrowserPagePointerAction(
        action_name="open_comments",
        candidate_selector="button",
        text_markers=("comments",),
        page_text_markers=("drag the slider",),
        exact_text_markers=("x",),
        random_seed=7,
        prefer_top_right=True,
    )




def test_fetch_browser_page_observation_capture_threads_pointer_actions_to_engine() -> None:
    engine = _ok_page_observation_engine()
    pointer_actions = (
        BrowserPagePointerAction(
            action_name=" open_comments ",
            candidate_selector=" button ",
            text_markers=(" Comments ",),
            page_text_markers=(" Drag the slider ",),
            exact_text_markers=(" X ",),
            random_seed=7,
        ),
        BrowserPagePointerAction(
            action_name=" more_like_this ",
            candidate_selector=" [role='tab'] ",
            text_markers=(" More like this ",),
            random_seed=8,
            prefer_smallest_match=True,
        ),
    )

    result = fetch_browser_page_observation_capture(
        url="https://example.com/source",
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_actions=pointer_actions,
        engine=engine,
    )

    assert isinstance(result, BrowserPageObservationSuccess)
    assert engine.capture_kwargs is not None
    assert engine.capture_kwargs["post_load_action_script"] is None
    assert engine.capture_kwargs["post_load_pointer_action"] is None
    assert engine.capture_kwargs["post_load_pointer_actions"] == (
        BrowserPagePointerAction(
            action_name="open_comments",
            candidate_selector="button",
            text_markers=("comments",),
            page_text_markers=("drag the slider",),
            exact_text_markers=("x",),
            random_seed=7,
        ),
        BrowserPagePointerAction(
            action_name="more_like_this",
            candidate_selector="[role='tab']",
            text_markers=("more like this",),
            random_seed=8,
            prefer_smallest_match=True,
        ),
    )


def test_fetch_browser_page_observation_capture_rejects_unknown_browser_backend() -> None:
    with pytest.raises(ValueError, match="browser_backend must be one of"):
        fetch_browser_page_observation_capture(
            url="https://example.com/source",
            dom_extract_script="() => ({items: []})",
            dom_extract_arg={},
            response_url_predicate=lambda url: "widget" in url,
            browser_backend="unknown",
            engine=_ok_page_observation_engine(),
        )


def test_fetch_browser_page_observation_capture_rejects_chrome_cdp_without_engine() -> None:
    """chrome_cdp must never silently fall back to a disposable launched browser.

    Without an explicit engine there is no operator-owned Chrome to attach to,
    so this must fail loudly instead of defaulting to
    ``_PlaywrightBrowserSnapshotEngine`` (which would launch and discard a
    fresh browser per capture).
    """
    with pytest.raises(ValueError, match="browser_backend='chrome_cdp' requires an explicit session engine"):
        fetch_browser_page_observation_capture(
            url="https://example.com/source",
            dom_extract_script="() => ({items: []})",
            dom_extract_arg={},
            response_url_predicate=lambda url: "widget" in url,
            browser_backend="chrome_cdp",
        )


def test_fetch_browser_page_observation_capture_rejects_cloakbrowser_channel_mix() -> None:
    with pytest.raises(ValueError, match="browser_channel is not supported"):
        fetch_browser_page_observation_capture(
            url="https://example.com/source",
            dom_extract_script="() => ({items: []})",
            dom_extract_arg={},
            response_url_predicate=lambda url: "widget" in url,
            browser_backend="cloakbrowser",
            browser_channel="chrome",
            engine=_ok_page_observation_engine(),
        )


def test_cloakbrowser_page_observation_uses_cloak_launch(monkeypatch: pytest.MonkeyPatch) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(event_log)
    fake_cloakbrowser = _FakeCloakBrowserModule(page)

    def fake_import_module(name: str) -> object:
        if name == "playwright.sync_api":
            return _FakePlaywrightSyncApi(page)
        if name == "cloakbrowser":
            return fake_cloakbrowser
        raise ModuleNotFoundError(name)

    monkeypatch.setattr(browser_snapshot_module, "import_module", fake_import_module)

    result = browser_snapshot_module._CloakBrowserPageObservationEngine(
        cloakbrowser_humanize=True
    ).capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
    )

    assert fake_cloakbrowser.launch_kwargs is not None
    assert "backend" not in fake_cloakbrowser.launch_kwargs
    assert fake_cloakbrowser.launch_kwargs["stealth_args"] is True
    assert fake_cloakbrowser.launch_kwargs["humanize"] is True
    assert result.metadata["browser_backend"] == "cloakbrowser"
    assert result.metadata["cloakbrowser_humanize"] is True


def test_cloakbrowser_engine_rejects_non_observation_methods() -> None:
    engine = browser_snapshot_module._CloakBrowserPageObservationEngine()

    with pytest.raises(NotImplementedError, match="page observation only"):
        engine.capture(
            url="https://example.com/source",
            timeout_seconds=1,
            wait_until="load",
            viewport_width=1280,
            viewport_height=720,
        )

    with pytest.raises(NotImplementedError, match="page observation only"):
        engine.capture_context_responses(
            page_url="https://example.com/source",
            requests=(),
            timeout_seconds=1,
            wait_until="load",
            viewport_width=1280,
            viewport_height=720,
        )


def test_page_observation_human_challenge_handoff_after_named_pointer_action(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_target={
            "candidate_count": 1,
            "matched_count": 1,
            "target_found": True,
            "target_kind": "button",
            "box": {"x": 10, "y": 20, "width": 100, "height": 50},
        },
        marker_match_results=[
            {
                "checked": True,
                "matched": True,
                "matched_marker": "drag the slider",
                "marker_count": 1,
            },
            {
                "checked": True,
                "matched": False,
                "matched_marker": None,
                "marker_count": 1,
            },
        ],
    )
    _install_fake_playwright(monkeypatch, page)
    monkeypatch.setattr(
        browser_snapshot_module,
        "_show_human_challenge_prompt",
        lambda _prompt: "test_prompt",
    )

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine(
        human_challenge_handoff_markers=("drag the slider",),
        human_challenge_handoff_after_action_names=("challenge_close",),
        human_challenge_handoff_timeout_seconds=1,
    ).capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_actions=(
            BrowserPagePointerAction(
                action_name="challenge_close",
                candidate_selector="button",
                text_markers=("close",),
                wait_after_ms=0,
            ),
        ),
    )

    attempts = result.metadata["human_challenge_handoff_attempts"]
    assert attempts == [
        {
            "action_name": "human_challenge_handoff_v0",
            "action_mode": "source_access_intervention",
            "action_taken": True,
            "captcha_solving_by_agent": False,
            "prompted": True,
            "prompt_surface": "test_prompt",
            "matched_marker": "drag the slider",
            "marker_count": 1,
            "timeout_seconds": 1,
            "cleared": True,
            "wait_ms": 0,
            "after_action_name": "challenge_close",
        }
    ]
    assert event_log.count("human_marker_match") == 2


def test_post_action_handoff_stops_remaining_actions_when_challenge_persists(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    target = {
        "candidate_count": 1,
        "matched_count": 1,
        "target_found": True,
        "target_kind": "button",
        "box": {"x": 10, "y": 20, "width": 100, "height": 50},
    }
    page = _FakeObservationPage(
        event_log,
        pointer_targets=[target, target],
        marker_match_results=[
            {
                "checked": True,
                "matched": True,
                "matched_marker": "drag the slider",
                "marker_count": 1,
            },
            {
                "checked": True,
                "matched": True,
                "matched_marker": "drag the slider",
                "marker_count": 1,
            },
        ],
    )
    _install_fake_playwright(monkeypatch, page)
    monkeypatch.setattr(
        browser_snapshot_module,
        "_show_human_challenge_prompt",
        lambda _prompt: "test_prompt",
    )

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine(
        human_challenge_handoff_markers=("drag the slider",),
        human_challenge_handoff_after_action_names=("first_action",),
        human_challenge_handoff_timeout_seconds=0,
    ).capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_actions=(
            BrowserPagePointerAction(
                action_name="first_action",
                candidate_selector="button",
                text_markers=("comments",),
                wait_after_ms=0,
            ),
            BrowserPagePointerAction(
                action_name="second_action",
                candidate_selector="button",
                text_markers=("more",),
                wait_after_ms=0,
            ),
        ),
    )

    assert result.metadata["pointer_actions_suppressed_by_human_challenge_handoff"] is True
    assert event_log.count("mouse_click") == 1
    attempts = result.metadata["human_challenge_handoff_attempts"]
    assert len(attempts) == 1
    assert attempts[0]["after_action_name"] == "first_action"
    assert attempts[0]["cleared"] is False
    assert attempts[0]["timeout_exceeded"] is True


def test_page_load_account_safety_stop_suppresses_actions_without_handoff(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_target={
            "candidate_count": 1,
            "matched_count": 1,
            "target_found": True,
            "target_kind": "button",
            "box": {"x": 10, "y": 20, "width": 100, "height": 50},
        },
        marker_match_results=[
            {
                "checked": True,
                "matched": True,
                "matched_marker": "account might be at risk",
                "marker_count": 1,
            }
        ],
    )
    _install_fake_playwright(monkeypatch, page)
    monkeypatch.setattr(
        browser_snapshot_module,
        "_show_human_challenge_prompt",
        lambda _prompt: pytest.fail("account safety stop must not prompt CAPTCHA handoff"),
    )

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine(
        pre_action_stop_markers=("account might be at risk",),
    ).capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_actions=(
            BrowserPagePointerAction(
                action_name="must_not_run",
                candidate_selector="button",
                text_markers=("continue",),
                wait_after_ms=0,
            ),
        ),
    )

    assert result.metadata["pointer_actions_suppressed_by_pre_action_stop"] is True
    assert result.metadata["pointer_actions_suppressed_by_human_challenge_handoff"] is False
    assert result.metadata["human_challenge_handoff_attempts"] == []
    assert result.metadata["post_load_pointer_actions"] == []
    assert result.metadata["pre_action_stop_attempts"][0]["automatic_retry_allowed"] is False
    assert "pointer_target_lookup" not in event_log
    assert "mouse_click" not in event_log


def test_page_load_account_safety_stop_suppresses_lazy_load_scrolls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        marker_match_results=[
            {
                "checked": True,
                "matched": True,
                "matched_marker": "account might be at risk",
                "marker_count": 1,
            }
        ],
    )
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine(
        pre_action_stop_markers=("account might be at risk",),
    ).capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda _url: False,
        lazy_load_scroll_passes=2,
        lazy_load_scroll_step_px=500,
    )

    assert result.metadata["pointer_actions_suppressed_by_pre_action_stop"] is True
    assert result.metadata["lazy_load_scroll_passes_executed"] == 0
    assert result.metadata["lazy_load_scroll_stop_reason"] == "scripted_actions_suppressed"
    assert "page_evaluate" not in event_log


def test_page_load_handoff_suppresses_pointer_actions_until_challenge_clears(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_target={
            "candidate_count": 1,
            "matched_count": 1,
            "target_found": True,
            "target_kind": "button",
            "box": {"x": 10, "y": 20, "width": 100, "height": 50},
        },
        marker_match_results=[
            {
                "checked": True,
                "matched": True,
                "matched_marker": "drag the slider",
                "marker_count": 1,
            },
            {
                "checked": True,
                "matched": True,
                "matched_marker": "drag the slider",
                "marker_count": 1,
            },
        ],
    )
    _install_fake_playwright(monkeypatch, page)
    monkeypatch.setattr(
        browser_snapshot_module,
        "_show_human_challenge_prompt",
        lambda _prompt: "test_prompt",
    )

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine(
        human_challenge_handoff_markers=("drag the slider",),
        human_challenge_handoff_after_action_names=(
            browser_snapshot_module.PAGE_LOAD_BEFORE_POINTER_ACTIONS_HANDOFF_NAME,
        ),
        human_challenge_handoff_timeout_seconds=0,
    ).capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_actions=(
            BrowserPagePointerAction(
                action_name="must_not_run",
                candidate_selector="button",
                text_markers=("continue",),
                wait_after_ms=0,
            ),
        ),
    )

    assert result.metadata["pointer_actions_suppressed_by_human_challenge_handoff"] is True
    assert result.metadata["post_load_pointer_actions"] == []
    assert "pointer_target_lookup" not in event_log
    assert "mouse_click" not in event_log
    attempt = result.metadata["human_challenge_handoff_attempts"][0]
    assert attempt["after_action_name"] == (
        browser_snapshot_module.PAGE_LOAD_BEFORE_POINTER_ACTIONS_HANDOFF_NAME
    )
    assert attempt["cleared"] is False
    assert attempt["timeout_exceeded"] is True


def test_cloakbrowser_page_load_handoff_suppresses_pointer_actions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Backend parity: the chowdakr_sg_tiktok profile forces the cloakbrowser
    # backend, so the page-load suppression the bound outcome depends on must
    # hold on the CloakBrowser engine, not only the Playwright engine covered by
    # test_page_load_handoff_suppresses_pointer_actions_until_challenge_clears.
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_target={
            "candidate_count": 1,
            "matched_count": 1,
            "target_found": True,
            "target_kind": "button",
            "box": {"x": 10, "y": 20, "width": 100, "height": 50},
        },
        marker_match_results=[
            {
                "checked": True,
                "matched": True,
                "matched_marker": "drag the slider",
                "marker_count": 1,
            },
            {
                "checked": True,
                "matched": True,
                "matched_marker": "drag the slider",
                "marker_count": 1,
            },
        ],
    )
    fake_cloakbrowser = _FakeCloakBrowserModule(page)

    def fake_import_module(name: str) -> object:
        if name == "cloakbrowser":
            return fake_cloakbrowser
        raise ModuleNotFoundError(name)

    monkeypatch.setattr(browser_snapshot_module, "import_module", fake_import_module)
    monkeypatch.setattr(
        browser_snapshot_module,
        "_show_human_challenge_prompt",
        lambda _prompt: "test_prompt",
    )

    result = browser_snapshot_module._CloakBrowserPageObservationEngine(
        human_challenge_handoff_markers=("drag the slider",),
        human_challenge_handoff_after_action_names=(
            browser_snapshot_module.PAGE_LOAD_BEFORE_POINTER_ACTIONS_HANDOFF_NAME,
        ),
        human_challenge_handoff_timeout_seconds=0,
    ).capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_actions=(
            BrowserPagePointerAction(
                action_name="must_not_run",
                candidate_selector="button",
                text_markers=("continue",),
                wait_after_ms=0,
            ),
        ),
        lazy_load_scroll_passes=2,
        lazy_load_scroll_step_px=500,
    )

    assert result.metadata["browser_backend"] == "cloakbrowser"
    assert result.metadata["pointer_actions_suppressed_by_human_challenge_handoff"] is True
    assert result.metadata["post_load_pointer_actions"] == []
    assert result.metadata["lazy_load_scroll_passes_executed"] == 0
    assert result.metadata["lazy_load_scroll_stop_reason"] == "scripted_actions_suppressed"
    assert "pointer_target_lookup" not in event_log
    assert "mouse_click" not in event_log
    assert "scroll" not in event_log
    attempt = result.metadata["human_challenge_handoff_attempts"][0]
    assert attempt["after_action_name"] == (
        browser_snapshot_module.PAGE_LOAD_BEFORE_POINTER_ACTIONS_HANDOFF_NAME
    )
    assert attempt["cleared"] is False
    assert attempt["timeout_exceeded"] is True


def test_cloakbrowser_account_safety_stop_suppresses_actions_without_handoff(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_target={
            "candidate_count": 1,
            "matched_count": 1,
            "target_found": True,
            "target_kind": "button",
            "box": {"x": 10, "y": 20, "width": 100, "height": 50},
        },
        marker_match_results=[
            {
                "checked": True,
                "matched": True,
                "matched_marker": "account might be at risk",
                "marker_count": 1,
            }
        ],
    )
    fake_cloakbrowser = _FakeCloakBrowserModule(page)

    def fake_import_module(name: str) -> object:
        if name == "cloakbrowser":
            return fake_cloakbrowser
        raise ModuleNotFoundError(name)

    monkeypatch.setattr(browser_snapshot_module, "import_module", fake_import_module)
    monkeypatch.setattr(
        browser_snapshot_module,
        "_show_human_challenge_prompt",
        lambda _prompt: pytest.fail("account safety stop must not prompt CAPTCHA handoff"),
    )

    result = browser_snapshot_module._CloakBrowserPageObservationEngine(
        pre_action_stop_markers=("account might be at risk",),
    ).capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda _url: False,
        post_load_pointer_actions=(
            BrowserPagePointerAction(
                action_name="must_not_run",
                candidate_selector="button",
                text_markers=("continue",),
                wait_after_ms=0,
            ),
        ),
    )

    assert result.metadata["pointer_actions_suppressed_by_pre_action_stop"] is True
    assert result.metadata["human_challenge_handoff_attempts"] == []
    assert result.metadata["post_load_pointer_actions"] == []
    assert "mouse_click" not in event_log


def test_pointer_action_target_script_matches_data_attributes() -> None:
    script = browser_snapshot_module._POINTER_ACTION_TARGET_SCRIPT
    assert "data-e2e" in script
    assert "data-testid" in script
    assert "data-test-id" in script
    assert "dataE2E === 'comment-icon'" in script
    assert "page_text_markers" in script
    assert "exact_text_markers" in script
    assert "prefer_top_right" in script
    assert "prefer_smallest_match" in script
    assert "page_text_matched_marker" in script
    assert "node.getAttribute('class')" in script
    assert "document.body.textContent" not in script


def test_fetch_browser_page_observation_capture_rejects_negative_lazy_load_scroll_controls() -> None:
    with pytest.raises(ValueError, match="lazy_load_scroll_passes must be zero or greater"):
        fetch_browser_page_observation_capture(
            url="https://example.com/source",
            dom_extract_script="() => ({items: []})",
            dom_extract_arg={},
            response_url_predicate=lambda _: False,
            lazy_load_scroll_passes=-1,
            engine=_ok_page_observation_engine(),
        )
    with pytest.raises(ValueError, match="lazy_load_scroll_step_px must be zero or greater"):
        fetch_browser_page_observation_capture(
            url="https://example.com/source",
            dom_extract_script="() => ({items: []})",
            dom_extract_arg={},
            response_url_predicate=lambda _: False,
            lazy_load_scroll_step_px=-1,
            engine=_ok_page_observation_engine(),
        )
    with pytest.raises(ValueError, match="post_load_action_script must not be blank"):
        fetch_browser_page_observation_capture(
            url="https://example.com/source",
            dom_extract_script="() => ({items: []})",
            dom_extract_arg={},
            response_url_predicate=lambda _: False,
            post_load_action_script="   ",
            engine=_ok_page_observation_engine(),
        )
    with pytest.raises(ValueError, match="mutually exclusive"):
        fetch_browser_page_observation_capture(
            url="https://example.com/source",
            dom_extract_script="() => ({items: []})",
            dom_extract_arg={},
            response_url_predicate=lambda _: False,
            post_load_action_script="() => true",
            post_load_pointer_action=BrowserPagePointerAction(
                action_name="open",
                candidate_selector="button",
                text_markers=("comment",),
            ),
            engine=_ok_page_observation_engine(),
        )
    with pytest.raises(ValueError, match="text_markers"):
        fetch_browser_page_observation_capture(
            url="https://example.com/source",
            dom_extract_script="() => ({items: []})",
            dom_extract_arg={},
            response_url_predicate=lambda _: False,
            post_load_pointer_action=BrowserPagePointerAction(
                action_name="open",
                candidate_selector="button",
                text_markers=("   ",),
            ),
            engine=_ok_page_observation_engine(),
        )


def test_playwright_page_observation_extracts_dom_before_lazy_load_scroll_and_reads_responses_after(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(event_log)
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        lazy_load_scroll_passes=1,
        lazy_load_scroll_step_px=500,
    )

    assert result.metadata["dom_observation_stage"] == "pre_lazy_load_scroll"
    assert result.metadata["post_load_action_executed"] is False
    assert result.metadata["lazy_load_scroll_passes_executed"] == 1
    assert result.metadata["lazy_load_scroll_stop_reason"] == "requested_passes_complete"
    assert result.dom_observation == {"items": [{"text": "before scroll"}]}
    assert result.responses[0].body_text == "{}"
    assert event_log.index("inner_text") < event_log.index("dom_extract")
    assert event_log.index("dom_extract") < event_log.index("scroll")
    assert event_log.index("scroll") < event_log.index("response_text")


def test_playwright_page_observation_runs_post_load_action_before_dom_and_reads_responses(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(event_log)
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_action_script="async (arg) => { window.__postLoadAction = arg; }",
        post_load_action_arg={"target": "comments"},
    )

    assert result.metadata["post_load_action_executed"] is True
    assert result.responses[0].body_text == "{}"
    assert event_log.index("post_load_action") < event_log.index("inner_text")
    assert event_log.index("post_load_action") < event_log.index("dom_extract")
    assert event_log.index("dom_extract") < event_log.index("response_text")


def test_playwright_page_observation_runs_pointer_action_before_dom_and_reads_responses(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_target={
            "candidate_count": 3,
            "matched_count": 1,
            "target_found": True,
            "target_kind": "button",
            "page_text_gate_matched": True,
            "page_text_matched_marker": "drag the slider",
            "selection_strategy": "top_right",
            "box": {"x": 10, "y": 20, "width": 100, "height": 50},
        },
    )
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_action=BrowserPagePointerAction(
            action_name="test_pointer_v0",
            candidate_selector="button",
            text_markers=("comments",),
            page_text_markers=("drag the slider",),
            exact_text_markers=("x",),
            wait_after_ms=2500,
            move_steps_min=7,
            move_steps_max=7,
            random_seed=11,
            prefer_top_right=True,
        ),
    )

    receipt = result.metadata["post_load_pointer_action"]
    assert isinstance(receipt, dict)
    assert receipt["action_name"] == "test_pointer_v0"
    assert receipt["candidate_count"] == 3
    assert receipt["matched_count"] == 1
    assert receipt["target_found"] is True
    assert receipt["clicked"] is True
    assert receipt["move_steps"] == 7
    assert receipt["wait_ms"] == 2500
    assert receipt["target_kind"] == "button"
    assert receipt["page_text_gate_matched"] is True
    assert receipt["page_text_matched_marker"] == "drag the slider"
    assert receipt["selection_strategy"] == "top_right"
    assert receipt["target_geometry_freshly_resolved"] is True
    assert receipt["target_box_width"] == 100.0
    assert receipt["target_box_height"] == 50.0
    assert 0.35 <= receipt["click_fraction_x"] <= 0.65
    assert 0.35 <= receipt["click_fraction_y"] <= 0.65
    assert "x" not in receipt
    assert "y" not in receipt
    assert result.metadata["post_load_action_executed"] is True
    assert result.responses[0].body_text == "{}"
    assert event_log.index("pointer_target_lookup") < event_log.index("mouse_move:7")
    assert event_log.index("mouse_move:7") < event_log.index("mouse_click")
    assert event_log.index("mouse_click") < event_log.index("wait:2500")
    assert event_log.index("wait:2500") < event_log.index("inner_text")
    assert event_log.index("dom_extract") < event_log.index("response_text")


def test_playwright_page_observation_runs_bounded_wheel_burst_before_dom(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(event_log)
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda _: False,
        post_load_wheel_action=BrowserPageWheelAction(
            action_name="test_grid_wheel_v0",
            direction="down",
            viewport_fraction_min=0.75,
            viewport_fraction_max=0.75,
            wheel_chunk_px_min=30,
            wheel_chunk_px_max=30,
            wheel_pause_ms_min=10,
            wheel_pause_ms_max=10,
            settle_ms_min=500,
            settle_ms_max=500,
            random_seed=11,
        ),
    )

    receipt = result.metadata["post_load_wheel_action"]
    assert receipt["completed"] is True
    assert receipt["input_method"] == "page.mouse.wheel_burst"
    assert receipt["planned_delta_y_px"] == 540
    assert receipt["actual_scroll_delta_y_px"] == 540
    assert receipt["wheel_event_count"] == 18
    assert len(page.mouse.wheels) == 18
    assert all(delta_x == 0 and 0 < delta_y <= 30 for delta_x, delta_y in page.mouse.wheels)
    assert result.metadata["post_load_action_executed"] is True
    assert event_log.index("wheel_viewport_lookup") < event_log.index("mouse_move:1")
    assert event_log.index("mouse_wheel") < event_log.index("dom_extract")




def test_playwright_page_observation_runs_pointer_action_sequence_before_dom(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_targets=[
            {
                "candidate_count": 3,
                "matched_count": 1,
                "target_found": True,
                "target_kind": "tab",
                "box": {"x": 10, "y": 20, "width": 100, "height": 50},
            },
            {
                "candidate_count": 5,
                "matched_count": 2,
                "target_found": True,
                "target_kind": "button",
                "box": {"x": 30, "y": 40, "width": 120, "height": 60},
            },
        ],
    )
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_actions=(
            BrowserPagePointerAction(
                action_name="open_more_like_this",
                candidate_selector="[role='tab']",
                text_markers=("more like this",),
                wait_after_ms=1000,
                move_steps_min=3,
                move_steps_max=3,
                random_seed=11,
            ),
            BrowserPagePointerAction(
                action_name="reopen_comments",
                candidate_selector="button",
                text_markers=("comments",),
                wait_after_ms=2000,
                move_steps_min=4,
                move_steps_max=4,
                random_seed=12,
            ),
        ),
    )

    receipts = result.metadata["post_load_pointer_actions"]
    assert isinstance(receipts, list)
    assert [receipt["action_name"] for receipt in receipts] == [
        "open_more_like_this",
        "reopen_comments",
    ]
    assert receipts[0]["target_kind"] == "tab"
    assert receipts[1]["target_kind"] == "button"
    assert result.metadata["post_load_pointer_action"] == receipts[-1]
    assert result.metadata["post_load_action_executed"] is True
    assert result.responses[0].body_text == "{}"
    assert event_log.count("pointer_target_lookup") == 2
    assert event_log.count("mouse_click") == 2
    assert event_log.index("wait:2000") < event_log.index("inner_text")
    assert event_log.index("dom_extract") < event_log.index("response_text")


def test_playwright_page_observation_stops_pointer_sequence_on_observed_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_targets=[
            {
                "candidate_count": 1,
                "matched_count": 1,
                "target_found": True,
                "target_kind": "button",
                "box": {"x": 10, "y": 20, "width": 100, "height": 50},
            },
            {
                "candidate_count": 1,
                "matched_count": 1,
                "target_found": True,
                "target_kind": "button",
                "box": {"x": 30, "y": 40, "width": 120, "height": 60},
            },
        ],
    )
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_actions=(
            BrowserPagePointerAction(
                action_name="open_comments",
                candidate_selector="button",
                text_markers=("comments",),
                wait_after_ms=2000,
                move_steps_min=3,
                move_steps_max=3,
                stop_wait_on_observed_response=True,
                stop_sequence_on_observed_response=True,
                random_seed=11,
            ),
            BrowserPagePointerAction(
                action_name="open_more_like_this",
                candidate_selector="button",
                text_markers=("more like this",),
                wait_after_ms=2000,
                move_steps_min=4,
                move_steps_max=4,
                random_seed=12,
            ),
        ),
    )

    receipts = result.metadata["post_load_pointer_actions"]
    assert isinstance(receipts, list)
    assert [receipt["action_name"] for receipt in receipts] == ["open_comments"]
    assert receipts[0]["observed_response_count_before"] == 0
    assert receipts[0]["observed_response_count_after"] == 1
    assert receipts[0]["observed_response_delta"] == 1
    assert receipts[0]["observed_response_seen"] is True
    assert receipts[0]["wait_ms"] == 0
    assert "wait:2000" not in event_log
    assert event_log.count("pointer_target_lookup") == 1

def test_playwright_page_observation_can_wait_early_without_stopping_sequence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_targets=[
            {
                "candidate_count": 1,
                "matched_count": 1,
                "target_found": True,
                "target_kind": "button",
                "box": {"x": 10, "y": 20, "width": 100, "height": 50},
            },
            {
                "candidate_count": 1,
                "matched_count": 1,
                "target_found": True,
                "target_kind": "button",
                "box": {"x": 30, "y": 40, "width": 120, "height": 60},
            },
        ],
        response_url="https://www.tiktok.com/api/comment/list/?aweme_id=739&cursor=0",
        response_method="OPTIONS",
        response_resource_type="fetch",
    )
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "/api/comment/list" in url,
        post_load_pointer_actions=(
            BrowserPagePointerAction(
                action_name="open_comments",
                candidate_selector="button",
                text_markers=("comments",),
                wait_after_ms=2000,
                move_steps_min=3,
                move_steps_max=3,
                stop_wait_on_observed_response=True,
                random_seed=11,
            ),
            BrowserPagePointerAction(
                action_name="open_more_like_this",
                candidate_selector="button",
                text_markers=("more like this",),
                wait_after_ms=0,
                move_steps_min=4,
                move_steps_max=4,
                random_seed=12,
            ),
        ),
    )

    receipts = result.metadata["post_load_pointer_actions"]
    assert isinstance(receipts, list)
    assert [receipt["action_name"] for receipt in receipts] == [
        "open_comments",
        "open_more_like_this",
    ]
    assert receipts[0]["observed_response_delta"] == 1
    assert receipts[0]["wait_ms"] == 0
    assert "wait:2000" not in event_log
    assert event_log.count("pointer_target_lookup") == 2

def test_playwright_page_observation_stops_pointer_sequence_on_failed_post_click_verification(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_targets=[
            {
                "candidate_count": 1,
                "matched_count": 1,
                "target_found": True,
                "target_kind": "button",
                "page_text_gate_matched": True,
                "box": {"x": 10, "y": 20, "width": 100, "height": 50},
            },
            {
                "candidate_count": 5,
                "matched_count": 2,
                "target_found": True,
                "target_kind": "button",
                "box": {"x": 30, "y": 40, "width": 120, "height": 60},
            },
        ],
        screenshot_png=_visual_x_screenshot_png(),
        post_click_absence_result={
            "checked": True,
            "marker_count": 1,
            "absent": True,
            "matched_marker": None,
        },
    )
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_actions=(
            BrowserPagePointerAction(
                action_name="challenge_close",
                candidate_selector="button",
                text_markers=("close",),
                page_text_markers=("drag the slider",),
                post_click_absent_text_markers=("drag the slider",),
                post_click_visual_target_absence_check=True,
                stop_sequence_on_failed_post_click_verification=True,
                wait_after_ms=1000,
                move_steps_min=3,
                move_steps_max=3,
                random_seed=11,
            ),
            BrowserPagePointerAction(
                action_name="reopen_comments",
                candidate_selector="button",
                text_markers=("comments",),
                wait_after_ms=2000,
                move_steps_min=4,
                move_steps_max=4,
                random_seed=12,
            ),
        ),
    )

    receipts = result.metadata["post_load_pointer_actions"]
    assert isinstance(receipts, list)
    assert [receipt["action_name"] for receipt in receipts] == ["challenge_close"]
    assert receipts[0]["clicked"] is True
    assert receipts[0]["post_click_absence_verified"] is True
    assert receipts[0]["post_click_visual_target_absent"] is False
    assert event_log.count("pointer_target_lookup") == 1
    assert event_log.count("mouse_click") == 1
    assert result.metadata["post_load_pointer_action"] == receipts[-1]

def test_playwright_page_observation_records_pointer_no_target_without_click(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_target={
            "candidate_count": 4,
            "matched_count": 0,
            "target_found": False,
            "target_kind": None,
            "box": None,
        },
    )
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_action=BrowserPagePointerAction(
            action_name="test_pointer_v0",
            candidate_selector="button",
            text_markers=("comments",),
            random_seed=11,
        ),
    )

    receipt = result.metadata["post_load_pointer_action"]
    assert isinstance(receipt, dict)
    assert receipt["candidate_count"] == 4
    assert receipt["matched_count"] == 0
    assert receipt["target_found"] is False
    assert receipt["clicked"] is False
    assert "mouse_click" not in event_log
    assert not any(event.startswith("mouse_move:") for event in event_log)


def test_playwright_page_observation_uses_visual_x_fallback_without_dom_target(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_target={
            "candidate_count": 0,
            "matched_count": 0,
            "target_found": False,
            "target_kind": None,
            "page_text_gate_matched": True,
            "selection_strategy": "top_right",
            "box": None,
        },
        screenshot_png=_visual_x_screenshot_png(),
    )
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_action=BrowserPagePointerAction(
            action_name="challenge_close_diag",
            candidate_selector="button",
            text_markers=("close",),
            exact_text_markers=("x",),
            page_text_markers=("drag the slider",),
            wait_after_ms=2000,
            move_steps_min=5,
            move_steps_max=5,
            random_seed=11,
            prefer_top_right=True,
            visual_top_right_x_fallback=True,
        ),
    )

    receipt = result.metadata["post_load_pointer_action"]
    assert isinstance(receipt, dict)
    assert receipt["candidate_count"] == 0
    assert receipt["matched_count"] == 0
    assert receipt["page_text_gate_matched"] is True
    assert receipt["target_found"] is True
    assert receipt["target_kind"] == "visual_x"
    assert receipt["selection_strategy"] == "top_right_visual_x"
    assert receipt["clicked"] is True
    assert receipt["move_steps"] == 5
    assert receipt["wait_ms"] == 2000
    assert receipt["visual_fallback_attempted"] is True
    assert receipt["visual_fallback_target_found"] is True
    assert receipt["visual_fallback_candidate_count"] >= 1
    assert receipt["visual_fallback_confidence"] > 0
    assert len(receipt["visual_fallback_screenshot_sha256"]) == 64
    assert receipt["visual_fallback_crop_box"] == {
        "x": 108,
        "y": 0,
        "width": 132,
        "height": 42,
    }
    click_x, click_y = page.mouse.clicks[0]
    assert receipt["click_point"] == {
        "x": round(click_x, 3),
        "y": round(click_y, 3),
    }
    assert receipt["target_box"]["x"] <= receipt["click_point"]["x"]
    assert receipt["target_box"]["y"] <= receipt["click_point"]["y"]
    assert receipt["click_point"]["x"] <= (
        receipt["target_box"]["x"] + receipt["target_box"]["width"]
    )
    assert receipt["click_point"]["y"] <= (
        receipt["target_box"]["y"] + receipt["target_box"]["height"]
    )
    assert "x" not in receipt
    assert "y" not in receipt
    assert event_log.index("pointer_target_lookup") < event_log.index("screenshot")
    assert event_log.index("screenshot") < event_log.index("mouse_move:5")
    assert event_log.index("mouse_move:5") < event_log.index("mouse_click")
    assert event_log.index("mouse_click") < event_log.index("wait:2000")


def test_playwright_page_observation_can_prefer_center_modal_visual_x(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_target={
            "candidate_count": 0,
            "matched_count": 0,
            "target_found": False,
            "target_kind": None,
            "page_text_gate_matched": True,
            "selection_strategy": "top_right",
            "box": None,
        },
        screenshot_png=_visual_x_modal_and_far_right_screenshot_png(),
    )
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_action=BrowserPagePointerAction(
            action_name="challenge_modal_close",
            candidate_selector="button",
            text_markers=("close",),
            exact_text_markers=("x",),
            page_text_markers=("drag the slider",),
            move_steps_min=5,
            move_steps_max=5,
            random_seed=11,
            prefer_top_right=True,
            visual_top_right_x_fallback=True,
            visual_x_target_zone="center_modal",
        ),
    )

    receipt = result.metadata["post_load_pointer_action"]
    assert isinstance(receipt, dict)
    assert receipt["visual_fallback_candidate_count"] >= 2
    assert receipt["visual_fallback_target_zone"] == "center_modal"
    assert receipt["selection_strategy"] == "center_modal_visual_x"
    assert receipt.get("visual_fallback_geometric_target") is not True
    assert receipt["target_box"]["x"] < 190
    assert receipt["clicked"] is True


def test_playwright_page_observation_records_post_click_close_verification(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_target={
            "candidate_count": 0,
            "matched_count": 0,
            "target_found": False,
            "target_kind": None,
            "page_text_gate_matched": True,
            "selection_strategy": "top_right",
            "box": None,
        },
        screenshot_pngs=[
            _visual_x_modal_and_far_right_screenshot_png(),
            _blank_screenshot_png(),
        ],
        post_click_absence_result={
            "checked": True,
            "marker_count": 4,
            "absent": True,
            "matched_marker": None,
        },
    )
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_action=BrowserPagePointerAction(
            action_name="challenge_modal_close",
            candidate_selector="button",
            text_markers=("close",),
            exact_text_markers=("x",),
            page_text_markers=("drag the slider",),
            post_click_absent_text_markers=("drag the slider", "verify to continue", "captcha", "security check"),
            post_click_visual_target_absence_check=True,
            move_steps_min=5,
            move_steps_max=5,
            random_seed=11,
            prefer_top_right=True,
            visual_top_right_x_fallback=True,
            visual_x_target_zone="center_modal",
        ),
    )

    receipt = result.metadata["post_load_pointer_action"]
    assert isinstance(receipt, dict)
    assert receipt["clicked"] is True
    assert receipt["post_click_absence_checked"] is True
    assert receipt["post_click_absence_marker_count"] == 4
    assert receipt["post_click_absence_verified"] is True
    assert receipt["post_click_visual_check_attempted"] is True
    assert receipt["post_click_visual_target_found"] is False
    assert receipt["post_click_visual_target_absent"] is True
    assert receipt["post_click_visual_candidate_count"] == 0
    assert len(receipt["post_click_visual_screenshot_sha256"]) == 64
    screenshot_indexes = [
        index for index, event in enumerate(event_log) if event == "screenshot"
    ]
    assert len(screenshot_indexes) == 2
    assert event_log.index("mouse_click") < event_log.index("wait:2500")
    assert event_log.index("wait:2500") < event_log.index("post_click_absence_lookup")
    assert event_log.index("post_click_absence_lookup") < screenshot_indexes[1]


def test_playwright_page_observation_post_click_visual_candidates_are_not_absent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_target={
            "candidate_count": 0,
            "matched_count": 0,
            "target_found": False,
            "target_kind": None,
            "page_text_gate_matched": True,
            "selection_strategy": "top_right",
            "box": None,
        },
        screenshot_pngs=[
            _visual_x_modal_and_far_right_screenshot_png(),
            _visual_x_screenshot_png(),
        ],
        post_click_absence_result={
            "checked": True,
            "marker_count": 4,
            "absent": True,
            "matched_marker": None,
        },
    )
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_action=BrowserPagePointerAction(
            action_name="challenge_modal_close",
            candidate_selector="button",
            text_markers=("close",),
            exact_text_markers=("x",),
            page_text_markers=("drag the slider",),
            post_click_absent_text_markers=("drag the slider", "verify to continue", "captcha", "security check"),
            post_click_visual_target_absence_check=True,
            move_steps_min=5,
            move_steps_max=5,
            random_seed=11,
            prefer_top_right=True,
            visual_top_right_x_fallback=True,
            visual_x_target_zone="center_modal",
        ),
    )

    receipt = result.metadata["post_load_pointer_action"]
    assert isinstance(receipt, dict)
    assert receipt["clicked"] is True
    assert receipt["post_click_visual_check_attempted"] is True
    assert receipt["post_click_visual_target_found"] is False
    assert receipt["post_click_visual_candidate_count"] > 0
    assert receipt["post_click_visual_target_absent"] is False


def test_playwright_page_observation_center_modal_reports_zone_candidate_count(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_target={
            "candidate_count": 0,
            "matched_count": 0,
            "target_found": False,
            "target_kind": None,
            "page_text_gate_matched": True,
            "selection_strategy": "top_right",
            "box": None,
        },
        # Click-time screenshot has a center-modal X plus a stray far-right X;
        # the post-click screenshot has only the stray far-right X (center modal
        # cleared). The broad candidate count cannot tell those apart; the zone
        # count can.
        screenshot_pngs=[
            _visual_x_modal_and_far_right_screenshot_png(),
            _visual_x_screenshot_png(),
        ],
        post_click_absence_result={
            "checked": True,
            "marker_count": 4,
            "absent": True,
            "matched_marker": None,
        },
    )
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_action=BrowserPagePointerAction(
            action_name="challenge_modal_close",
            candidate_selector="button",
            text_markers=("close",),
            exact_text_markers=("x",),
            page_text_markers=("drag the slider",),
            post_click_absent_text_markers=(
                "drag the slider",
                "verify to continue",
                "captcha",
                "security check",
            ),
            post_click_visual_target_absence_check=True,
            move_steps_min=5,
            move_steps_max=5,
            random_seed=11,
            prefer_top_right=True,
            visual_top_right_x_fallback=True,
            visual_x_target_zone="center_modal",
        ),
    )

    receipt = result.metadata["post_load_pointer_action"]
    assert isinstance(receipt, dict)
    # Click-time: the crop holds both X-glyphs, but only one is in the modal zone.
    assert receipt["visual_fallback_candidate_count"] >= 2
    assert receipt["visual_fallback_zone_candidate_count"] == 1
    # Post-click: the center modal is gone (zone count 0) but a stray glyph keeps
    # the broad candidate count above zero.
    assert receipt["post_click_visual_candidate_count"] > 0
    assert receipt["post_click_visual_zone_candidate_count"] == 0
    # Acceptance is deliberately unchanged: it still fails closed on the broad
    # candidate count, so the diagnostic zone count does not loosen the gate.
    assert receipt["post_click_visual_target_absent"] is False


def test_playwright_page_observation_center_modal_uses_geometric_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_target={
            "candidate_count": 0,
            "matched_count": 0,
            "target_found": False,
            "target_kind": None,
            "page_text_gate_matched": True,
            "selection_strategy": "top_right",
            "box": None,
        },
        screenshot_png=_visual_x_screenshot_png(),
    )
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_action=BrowserPagePointerAction(
            action_name="challenge_modal_close",
            candidate_selector="button",
            text_markers=("close",),
            exact_text_markers=("x",),
            page_text_markers=("drag the slider",),
            move_steps_min=5,
            move_steps_max=5,
            random_seed=11,
            prefer_top_right=True,
            visual_top_right_x_fallback=True,
            visual_x_target_zone="center_modal",
        ),
    )

    receipt = result.metadata["post_load_pointer_action"]
    assert isinstance(receipt, dict)
    assert receipt["visual_fallback_target_zone"] == "center_modal"
    assert receipt["selection_strategy"] == "center_modal_visual_x"
    assert receipt["visual_fallback_geometric_target"] is True
    assert 130 <= receipt["target_box"]["x"] <= 160
    assert receipt["clicked"] is True



def test_playwright_page_observation_can_disable_center_modal_geometric_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_target={
            "candidate_count": 0,
            "matched_count": 0,
            "target_found": False,
            "target_kind": None,
            "page_text_gate_matched": True,
            "selection_strategy": "top_right",
            "box": None,
        },
        screenshot_png=_visual_x_screenshot_png(),
    )
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_action=BrowserPagePointerAction(
            action_name="challenge_modal_close",
            candidate_selector="button",
            text_markers=("close",),
            exact_text_markers=("x",),
            page_text_markers=("drag the slider",),
            move_steps_min=5,
            move_steps_max=5,
            random_seed=11,
            prefer_top_right=True,
            visual_top_right_x_fallback=True,
            visual_x_target_zone="center_modal",
            visual_x_geometric_fallback=False,
        ),
    )

    receipt = result.metadata["post_load_pointer_action"]
    assert isinstance(receipt, dict)
    assert receipt["visual_fallback_target_zone"] == "center_modal"
    assert receipt["visual_fallback_candidate_count"] >= 1
    assert "visual_fallback_geometric_target" not in receipt
    assert receipt["target_found"] is False
    assert receipt["clicked"] is False
    assert "mouse_click" not in event_log

def test_playwright_page_observation_skips_visual_x_fallback_without_page_gate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(
        event_log,
        pointer_target={
            "candidate_count": 0,
            "matched_count": 0,
            "target_found": False,
            "target_kind": None,
            "page_text_gate_matched": False,
            "selection_strategy": "top_right",
            "box": None,
        },
        screenshot_png=_visual_x_screenshot_png(),
    )
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        post_load_pointer_action=BrowserPagePointerAction(
            action_name="challenge_close_diag",
            candidate_selector="button",
            text_markers=("close",),
            exact_text_markers=("x",),
            page_text_markers=("drag the slider",),
            random_seed=11,
            visual_top_right_x_fallback=True,
        ),
    )

    receipt = result.metadata["post_load_pointer_action"]
    assert isinstance(receipt, dict)
    assert receipt["target_found"] is False
    assert receipt["clicked"] is False
    assert receipt["visual_fallback_attempted"] is False
    assert "screenshot" not in event_log
    assert "mouse_click" not in event_log

def test_playwright_page_observation_reports_lazy_load_cap_warning(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(event_log)
    _install_fake_playwright(monkeypatch, page)

    result = browser_snapshot_module._PlaywrightBrowserSnapshotEngine().capture_page_observation(
        url="https://example.com/source",
        timeout_seconds=1,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        dom_extract_script="() => ({items: []})",
        dom_extract_arg={},
        response_url_predicate=lambda url: "widget" in url,
        lazy_load_scroll_passes=browser_snapshot_module._MAX_SCROLL_PASSES + 2,
        lazy_load_scroll_step_px=0,
    )

    assert (
        result.metadata["lazy_load_scroll_passes_executed"]
        == browser_snapshot_module._MAX_SCROLL_PASSES
    )
    assert result.metadata["lazy_load_scroll_stop_reason"] == "capped_pass_limit"
    assert result.warning_notes == [
        "browser_page_observation lazy_load_scroll_passes capped "
        f"from {browser_snapshot_module._MAX_SCROLL_PASSES + 2} "
        f"to {browser_snapshot_module._MAX_SCROLL_PASSES}"
    ]
    assert event_log.count("scroll") == browser_snapshot_module._MAX_SCROLL_PASSES


def test_read_observed_page_responses_omits_cookie_headers() -> None:
    event_log: list[str] = []
    response = _FakeObservationResponse(event_log)
    response.headers = {
        "content-type": "application/json",
        "cookie": "session=SECRET",
        "set-cookie": "session=SECRET",
    }

    preserved = browser_snapshot_module._read_observed_page_responses(
        [response],
        max_response_bytes=100,
    )

    assert preserved[0].response_headers == {"content-type": "application/json"}
    assert preserved[0].body_text == "{}"
    assert preserved[0].request_method == "GET"
    assert preserved[0].resource_type == "fetch"


def test_bounded_lazy_load_scrolls_stepwise_after_observation_extraction() -> None:
    page = _FakeLazyScrollPage(height=2_000)

    result = browser_snapshot_module._run_bounded_lazy_load_scrolls(
        page,
        scroll_passes=3,
        scroll_step_px=500,
    )

    assert result.executed_passes == 3
    assert result.stop_reason == "requested_passes_complete"
    assert page.scrolled_to == [500, 1_000, 1_500]
    assert page.waits == [browser_snapshot_module._SCROLL_PASS_SETTLE_MS] * 3


def test_bounded_lazy_load_scrolls_cap_pass_count() -> None:
    page = _FakeLazyScrollPage()

    result = browser_snapshot_module._run_bounded_lazy_load_scrolls(
        page,
        scroll_passes=browser_snapshot_module._MAX_SCROLL_PASSES + 5,
        scroll_step_px=0,
    )

    assert result.executed_passes == browser_snapshot_module._MAX_SCROLL_PASSES
    assert result.stop_reason == "capped_pass_limit"
    assert len(page.scrolled_to) == browser_snapshot_module._MAX_SCROLL_PASSES


def test_bounded_lazy_load_scrolls_reports_page_end_and_zero_noop() -> None:
    page = _FakeLazyScrollPage(height=900)

    page_end = browser_snapshot_module._run_bounded_lazy_load_scrolls(
        page,
        scroll_passes=3,
        scroll_step_px=500,
    )

    assert page_end.executed_passes == 2
    assert page_end.stop_reason == "page_end"
    assert page.scrolled_to == [500, 1_000]

    no_scroll_page = _FakeLazyScrollPage()
    no_scroll = browser_snapshot_module._run_bounded_lazy_load_scrolls(
        no_scroll_page,
        scroll_passes=0,
        scroll_step_px=500,
    )

    assert no_scroll.executed_passes == 0
    assert no_scroll.stop_reason is None
    assert no_scroll_page.scrolled_to == []
    assert no_scroll_page.waits == []


def test_fetch_browser_snapshot_capture_threads_scroll_params_to_engine() -> None:
    engine = _ok_engine()
    fetch_browser_snapshot_capture(
        url="https://example.com/source", scroll_passes=3, scroll_step_px=500, engine=engine
    )
    assert engine.capture_kwargs is not None
    assert engine.capture_kwargs["scroll_passes"] == 3
    assert engine.capture_kwargs["scroll_step_px"] == 500


def test_fetch_browser_snapshot_capture_scroll_defaults_to_zero_preserving_single_url_contract() -> None:
    engine = _ok_engine()
    fetch_browser_snapshot_capture(url="https://example.com/source", engine=engine)
    assert engine.capture_kwargs is not None
    assert engine.capture_kwargs["scroll_passes"] == 0
    assert engine.capture_kwargs["scroll_step_px"] == 0
    assert engine.capture_kwargs["settle_seconds"] == 0.0
    assert engine.capture_kwargs["headless"] is True
    assert engine.capture_kwargs["browser_channel"] is None


def test_fetch_browser_snapshot_capture_threads_standard_browser_controls_to_engine() -> None:
    engine = _ok_engine()
    result = fetch_browser_snapshot_capture(
        url="https://example.com/source",
        settle_seconds=4.5,
        headless=False,
        browser_channel=" chrome ",
        engine=engine,
    )

    assert isinstance(result, BrowserSnapshotSuccess)
    assert engine.capture_kwargs is not None
    assert engine.capture_kwargs["settle_seconds"] == 4.5
    assert engine.capture_kwargs["headless"] is False
    assert engine.capture_kwargs["browser_channel"] == "chrome"
    assert result.metadata["settle_seconds"] == 4.5
    assert result.metadata["headless"] is False
    assert result.metadata["browser_channel"] == "chrome"


def test_fetch_browser_snapshot_capture_flags_rendered_cloudflare_interstitial() -> None:
    result = fetch_browser_snapshot_capture(
        url="https://example.com/source",
        engine=_FakeBrowserEngine(
            _FakeEngineResult(
                final_url="https://example.com/source",
                title="Just a moment...",
                rendered_dom="<html><script>window.__cf_chl_tk = 'token'</script></html>",
                visible_text="Enable JavaScript and cookies to continue",
                screenshot_png=b"\x89PNG\r\n\x1a\nbrowser",
            )
        ),
    )

    assert isinstance(result, BrowserSnapshotSuccess)
    assert result.access_block_reason == "cloudflare_interstitial"
    assert result.metadata["access_blocked"] is True
    assert result.metadata["rendered_access_classification"] == "access_blocked"
    assert any("access_failed" in item for item in result.limitation_notes)


def test_fetch_browser_snapshot_capture_rejects_negative_scroll() -> None:
    with pytest.raises(ValueError, match="scroll_passes must be zero or greater"):
        fetch_browser_snapshot_capture(url="https://example.com/source", scroll_passes=-1, engine=_ok_engine())
    with pytest.raises(ValueError, match="scroll_step_px must be zero or greater"):
        fetch_browser_snapshot_capture(url="https://example.com/source", scroll_step_px=-5, engine=_ok_engine())
    with pytest.raises(ValueError, match="settle_seconds must be zero or greater"):
        fetch_browser_snapshot_capture(url="https://example.com/source", settle_seconds=-1, engine=_ok_engine())
    with pytest.raises(ValueError, match="browser_channel must not be blank"):
        fetch_browser_snapshot_capture(url="https://example.com/source", browser_channel="  ", engine=_ok_engine())


def test_browser_snapshot_runner_writes_packet_with_four_artifacts(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = scratch_dir / "packet"
    captured_kwargs: dict[str, object] = {}

    def fake_capture(**kwargs: object) -> BrowserSnapshotSuccess:
        captured_kwargs.update(kwargs)
        return BrowserSnapshotSuccess(
            requested_url="https://example.com/source",
            final_url="https://example.com/source",
            title="Rendered Source",
            rendered_dom="<html><body><main>Visible source language</main></body></html>",
            visible_text="Visible source language",
            screenshot_png=b"\x89PNG\r\n\x1a\nbrowser",
            metadata={
                "requested_url": "https://example.com/source",
                "final_url": "https://example.com/source",
                "title": "Rendered Source",
                "capture_timestamp": "2026-06-03T01:02:03Z",
                "timeout_seconds": kwargs["timeout_seconds"],
                "wait_until": kwargs["wait_until"],
                "viewport_width": kwargs["viewport_width"],
                "viewport_height": kwargs["viewport_height"],
                "screenshot_mode": "viewport",
                "rendered_dom_byte_count": 64,
                "visible_text_byte_count": 23,
                "screenshot_byte_count": 15,
            },
            warning_notes=[],
            limitation_notes=[],
        )

    monkeypatch.setattr(browser_runner, "fetch_browser_snapshot_capture", fake_capture)

    exit_code, message = browser_runner.run_source_capture_browser_packet(
        url="https://example.com/source",
        source_family="web_page",
        source_surface="browser_snapshot",
        decision_question="What rendered source was visible before cutoff?",
        output_directory=output_dir,
        capture_context="test browser snapshot",
        operator_category="browser_snapshot_cli_operator",
        capture_mode=CaptureModeCategory.MULTIMODAL,
        session_id=None,
        actor_audience_context=None,
        visible_mode_changes=[],
        source_publication_or_event=None,
        source_edit_or_version=None,
        cutoff_posture=None,
        recapture_time=None,
        re_capture_relationship=None,
        warnings=[],
        limitations=["operator-visible limitation travels"],
        timeout_seconds=20,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        max_artifact_bytes=5_000,
        settle_seconds=2.0,
        headless=False,
        browser_channel="chrome",
    )

    assert captured_kwargs["settle_seconds"] == 2.0
    assert captured_kwargs["headless"] is False
    assert captured_kwargs["browser_channel"] == "chrome"
    assert exit_code == 0
    assert message == str(output_dir.resolve())
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["source_surface"] == "browser_snapshot"
    assert manifest["capture_mode"] == "multimodal"
    assert manifest["source_slices"][0]["slice_id"] == "browser_snapshot_01"
    assert manifest["source_slices"][0]["preserved_file_ids"] == [
        "file_01",
        "file_02",
        "file_03",
        "file_04",
    ]
    assert [item["relative_packet_path"] for item in manifest["preserved_files"]] == [
        "raw/01_browser_rendered_dom.html",
        "raw/02_browser_visible_text.txt",
        "raw/03_browser_viewport_screenshot.png",
        "raw/04_browser_snapshot_metadata.json",
    ]
    assert manifest["receipt_metadata"]["non_claims"] == BROWSER_SNAPSHOT_NON_CLAIMS
    assert "operator-visible limitation travels" in manifest["limitations"]
    assert "Visible source language" in (output_dir / "raw" / "02_browser_visible_text.txt").read_text(
        encoding="utf-8"
    )
    assert not (output_dir.parent / "browser_rendered_dom.html").exists()
    assert not (output_dir.parent / "browser_snapshot_metadata.json").exists()
    receipt_text = (output_dir / "receipt.md").read_text(encoding="utf-8")
    for non_claim in BROWSER_SNAPSHOT_NON_CLAIMS:
        assert non_claim in receipt_text


def test_browser_snapshot_runner_writes_access_blocked_packet(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = scratch_dir / "packet"

    def fake_capture(**kwargs: object) -> BrowserSnapshotSuccess:
        return BrowserSnapshotSuccess(
            requested_url="https://example.com/source",
            final_url="https://example.com/source",
            title="Just a moment...",
            rendered_dom="<html><script>window.__cf_chl_tk = 'token'</script></html>",
            visible_text="Enable JavaScript and cookies to continue",
            screenshot_png=b"\x89PNG\r\n\x1a\nbrowser",
            metadata={
                "requested_url": "https://example.com/source",
                "final_url": "https://example.com/source",
                "title": "Just a moment...",
                "capture_timestamp": "2026-06-03T01:02:03Z",
                "timeout_seconds": kwargs["timeout_seconds"],
                "wait_until": kwargs["wait_until"],
                "viewport_width": kwargs["viewport_width"],
                "viewport_height": kwargs["viewport_height"],
                "screenshot_mode": "viewport",
                "access_blocked": True,
                "access_block_reason": "cloudflare_interstitial",
                "rendered_access_classification": "access_blocked",
                "rendered_access_signal": "cloudflare_interstitial",
                "rendered_access_detail": "rendered challenge shell",
                "rendered_dom_byte_count": 64,
                "visible_text_byte_count": 41,
                "screenshot_byte_count": 15,
            },
            warning_notes=[],
            limitation_notes=[
                "access_failed: browser_snapshot rendered an access-block/interstitial page instead of source content: cloudflare_interstitial; block artifacts preserved"
            ],
            access_block_reason="cloudflare_interstitial",
        )

    monkeypatch.setattr(browser_runner, "fetch_browser_snapshot_capture", fake_capture)

    exit_code, message = browser_runner.run_source_capture_browser_packet(
        url="https://example.com/source",
        source_family="web_page",
        source_surface="browser_snapshot",
        decision_question="What rendered source was visible before cutoff?",
        output_directory=output_dir,
        capture_context="test browser snapshot",
        operator_category="browser_snapshot_cli_operator",
        capture_mode=CaptureModeCategory.MULTIMODAL,
        session_id=None,
        actor_audience_context=None,
        visible_mode_changes=[],
        source_publication_or_event=None,
        source_edit_or_version=None,
        cutoff_posture=None,
        recapture_time=None,
        re_capture_relationship=None,
        warnings=[],
        limitations=[],
        timeout_seconds=20,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        max_artifact_bytes=5_000,
    )

    assert exit_code == 0
    assert message == str(output_dir.resolve())
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert "source content was not captured" in manifest["receipt_metadata"]["summary"]
    assert any("access_failed" in item for item in manifest["limitations"])
    metadata = json.loads(
        (output_dir / "raw" / "04_browser_snapshot_metadata.json").read_text(encoding="utf-8")
    )
    assert metadata["access_blocked"] is True
    assert metadata["access_block_reason"] == "cloudflare_interstitial"

def test_browser_snapshot_runner_returns_3_without_packet_on_capture_failure(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = scratch_dir / "packet"

    def fail_capture(**kwargs: object) -> BrowserSnapshotFailure:
        return BrowserSnapshotFailure(
            requested_url="https://example.com/source",
            failure_kind=BrowserSnapshotFailureKind.CAPTURE_FAILED,
            message="browser failed visibly",
        )

    monkeypatch.setattr(browser_runner, "fetch_browser_snapshot_capture", fail_capture)

    exit_code, message = browser_runner.run_source_capture_browser_packet(
        url="https://example.com/source",
        source_family="web_page",
        source_surface="browser_snapshot",
        decision_question="What rendered source was visible before cutoff?",
        output_directory=output_dir,
        capture_context="test browser snapshot",
        operator_category="browser_snapshot_cli_operator",
        capture_mode=CaptureModeCategory.MULTIMODAL,
        session_id=None,
        actor_audience_context=None,
        visible_mode_changes=[],
        source_publication_or_event=None,
        source_edit_or_version=None,
        cutoff_posture=None,
        recapture_time=None,
        re_capture_relationship=None,
        warnings=[],
        limitations=[],
        timeout_seconds=20,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        max_artifact_bytes=50_000,
    )

    assert exit_code == 3
    assert message == "browser failed visibly"
    assert not output_dir.exists()


def test_browser_snapshot_runner_cleans_staged_files_when_metadata_write_fails(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = scratch_dir / "packet"

    def fake_capture(**kwargs: object) -> BrowserSnapshotSuccess:
        return BrowserSnapshotSuccess(
            requested_url="https://example.com/source",
            final_url="https://example.com/source",
            title="Rendered Source",
            rendered_dom="<html><body>ok</body></html>",
            visible_text="ok",
            screenshot_png=b"\x89PNG\r\n\x1a\nbrowser",
            metadata={"bad": object()},
            warning_notes=[],
            limitation_notes=[],
        )

    monkeypatch.setattr(browser_runner, "fetch_browser_snapshot_capture", fake_capture)

    with pytest.raises(TypeError):
        browser_runner.run_source_capture_browser_packet(
            url="https://example.com/source",
            source_family="web_page",
            source_surface="browser_snapshot",
            decision_question="What rendered source was visible before cutoff?",
            output_directory=output_dir,
            capture_context="test browser snapshot",
            operator_category="browser_snapshot_cli_operator",
            capture_mode=CaptureModeCategory.MULTIMODAL,
            session_id=None,
            actor_audience_context=None,
            visible_mode_changes=[],
            source_publication_or_event=None,
            source_edit_or_version=None,
            cutoff_posture=None,
            recapture_time=None,
            re_capture_relationship=None,
            warnings=[],
            limitations=[],
            timeout_seconds=30,
            wait_until="load",
            viewport_width=1280,
            viewport_height=720,
            max_artifact_bytes=50_000,
        )

    assert not output_dir.exists()
    assert not (output_dir.parent / "browser_rendered_dom.html").exists()
    assert not (output_dir.parent / "browser_visible_text.txt").exists()
    assert not (output_dir.parent / "browser_viewport_screenshot.png").exists()
    assert not (output_dir.parent / "browser_snapshot_metadata.json").exists()


def test_browser_snapshot_runner_records_source_detail_sufficiency_pass(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = scratch_dir / "packet"

    def fake_capture(**kwargs: object) -> BrowserSnapshotSuccess:
        return BrowserSnapshotSuccess(
            requested_url="https://example.com/source",
            final_url="https://example.com/source",
            title="Rendered Source",
            rendered_dom="<html><body><main>Visible source language</main></body></html>",
            visible_text="Visible source language",
            screenshot_png=b"\x89PNG\r\n\x1a\nbrowser",
            metadata={
                "requested_url": "https://example.com/source",
                "final_url": "https://example.com/source",
                "title": "Rendered Source",
                "capture_timestamp": "2026-06-03T01:02:03Z",
                "timeout_seconds": kwargs["timeout_seconds"],
                "wait_until": kwargs["wait_until"],
                "viewport_width": kwargs["viewport_width"],
                "viewport_height": kwargs["viewport_height"],
                "screenshot_mode": "viewport",
                "access_blocked": False,
                "access_block_reason": None,
                "rendered_dom_byte_count": 64,
                "visible_text_byte_count": 23,
                "screenshot_byte_count": 15,
            },
            warning_notes=[],
            limitation_notes=[],
            access_block_reason=None,
        )

    monkeypatch.setattr(browser_runner, "fetch_browser_snapshot_capture", fake_capture)

    exit_code, message = browser_runner.run_source_capture_browser_packet(
        url="https://example.com/source",
        source_family="web_page",
        source_surface="browser_snapshot",
        decision_question="What rendered source was visible before cutoff?",
        output_directory=output_dir,
        capture_context="test browser snapshot",
        operator_category="browser_snapshot_cli_operator",
        capture_mode=CaptureModeCategory.MULTIMODAL,
        session_id=None,
        actor_audience_context=None,
        visible_mode_changes=[],
        source_publication_or_event=None,
        source_edit_or_version=None,
        cutoff_posture=None,
        recapture_time=None,
        re_capture_relationship=None,
        warnings=[],
        limitations=[],
        source_detail_sufficiency_requirements=SourceDetailSufficiencyRequirements(
            require_not_access_blocked=True,
            min_visible_text_bytes=10,
            visible_text_contains=("Visible source language",),
            rendered_dom_regexes=(r"<main>Visible source",),
        ),
        timeout_seconds=20,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        max_artifact_bytes=5_000,
    )

    assert exit_code == 0
    assert message == str(output_dir.resolve())
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert "source_detail_sufficiency_passed" in manifest["visible_mode_changes"]
    assert not any("source_detail_sufficiency_failed" in item for item in manifest["limitations"])

def test_bounded_lazy_load_scrolls_stops_when_response_target_is_reached() -> None:
    page = _FakeLazyScrollPage()
    checks = 0

    def stop_condition() -> bool:
        nonlocal checks
        checks += 1
        return checks >= 2

    result = browser_snapshot_module._run_bounded_lazy_load_scrolls(
        page,
        scroll_passes=10,
        scroll_step_px=0,
        stop_condition=stop_condition,
    )

    assert result.executed_passes == 1
    assert result.stop_reason == "response_target_reached"
    assert page.scrolled_to == ["bottom"]


def test_cloakbrowser_page_observation_session_reuses_one_context_and_closes_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_log: list[str] = []
    page = _FakeObservationPage(event_log)
    cloakbrowser = _FakeCloakBrowserModule(page)
    original_import_module = browser_snapshot_module.import_module

    def fake_import_module(name: str) -> object:
        if name == "cloakbrowser":
            return cloakbrowser
        return original_import_module(name)

    monkeypatch.setattr(browser_snapshot_module, "import_module", fake_import_module)
    engine = CloakBrowserPageObservationSessionEngine()

    for index in range(2):
        result = fetch_browser_page_observation_capture(
            url=f"https://example.com/source?capture={index}",
            dom_extract_script="() => ({ok: true})",
            dom_extract_arg=None,
            response_url_predicate=lambda _: False,
            browser_backend="cloakbrowser",
            block_resource_types=("image",),
            engine=engine,
        )
        assert isinstance(result, BrowserPageObservationSuccess)

    before_close = engine.lifecycle_receipt
    assert before_close["browser_launch_count"] == 1
    assert before_close["context_creation_count"] == 1
    assert before_close["page_creation_count"] == 1
    assert before_close["page_reuse_policy"] == "reuse_one_page_until_closed"
    assert before_close["capture_attempt_count"] == 2
    assert before_close["capture_success_count"] == 2
    assert before_close["closed"] is False
    assert "context_close" not in event_log
    assert event_log.count("new_page") == 1
    assert event_log.count("remove_listener") == 2
    assert "browser_close" not in event_log
    assert event_log.count("route") == 2
    assert event_log.count("unroute") == 2

    engine.close()
    engine.close()

    assert engine.lifecycle_receipt["closed"] is True
    assert event_log.count("context_close") == 1
    assert event_log.count("browser_close") == 1


def test_chrome_cdp_session_detaches_without_closing_context_or_page(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events: list[str] = []

    class FakePage:
        def is_closed(self) -> bool:
            return False

    page = FakePage()

    class FakeContext:
        def new_page(self) -> FakePage:
            events.append("new_page")
            return page

        def close(self) -> None:
            events.append("context_close")

    context = FakeContext()

    class FakeBrowser:
        contexts = [context]

        def close(self) -> None:
            events.append("browser_disconnect")

    browser = FakeBrowser()

    class FakeChromium:
        def connect_over_cdp(self, endpoint: str) -> FakeBrowser:
            events.append(f"attach:{endpoint}")
            return browser

    class FakePlaywrightOwner:
        chromium = FakeChromium()

        def stop(self) -> None:
            events.append("playwright_stop")

    owner = FakePlaywrightOwner()

    class FakeSyncPlaywright:
        @staticmethod
        def start() -> FakePlaywrightOwner:
            return owner

    class FakeSyncApi:
        @staticmethod
        def sync_playwright() -> FakeSyncPlaywright:
            return FakeSyncPlaywright()

    original_import_module = browser_snapshot_module.import_module

    def fake_import_module(name: str) -> object:
        if name == "playwright.sync_api":
            return FakeSyncApi()
        return original_import_module(name)

    monkeypatch.setattr(browser_snapshot_module, "import_module", fake_import_module)
    engine = ChromeCdpPageObservationSessionEngine(
        humanize_context_fn=lambda _context: events.append("humanize:careful")
    )
    proxy = engine._launch_page_observation_browser(
        playwright=object(), proxy_profile=None, headless=False, browser_channel=None
    )
    proxy.new_context(viewport={"width": 1280, "height": 720}, storage_state="ignored")

    assert engine._get_or_create_page() is page
    engine.close()
    assert events == [
        "attach:http://127.0.0.1:9222",
        "humanize:careful",
        "new_page",
        "browser_disconnect",
        "playwright_stop",
    ]
    assert engine.lifecycle_receipt["close_policy"] == (
        "detach_only_leave_browser_and_page_open"
    )


def test_chrome_cdp_session_adopts_latest_tiktok_page_and_discloses_exact_matches() -> None:
    class FakePage:
        def __init__(self, url: str, *, closed: bool = False) -> None:
            self.url = url
            self.closed = closed

        def is_closed(self) -> bool:
            return self.closed

    unrelated = FakePage("https://www.tiktok.com/@someone_else")
    first_exact = FakePage("http://www.tiktok.com/@Creator/?from=old#grid")
    closed_exact = FakePage("https://www.tiktok.com/@creator", closed=True)
    latest_exact = FakePage("https://tiktok.com/@creator?lang=en")

    class FakeContext:
        pages = [unrelated, first_exact, closed_exact, latest_exact]

        def new_page(self) -> FakePage:
            raise AssertionError("an exact target page must be adopted")

    engine = ChromeCdpPageObservationSessionEngine(humanize_context_fn=lambda _: None)
    engine._real_context = FakeContext()
    engine._pending_requested_page_url = "https://www.tiktok.com/@CREATOR/"

    assert engine._get_or_create_page() is latest_exact
    assert engine._get_or_create_page() is latest_exact
    receipt = engine.lifecycle_receipt
    assert receipt["page_acquisition_policy"] == "adopt_same_platform_else_create"
    assert receipt["initial_platform_match_count"] == 3
    assert receipt["initial_exact_match_count"] == 2
    assert receipt["page_adoption_count"] == 1
    assert receipt["page_creation_count"] == 0
    assert receipt["adopted_page_enumeration_index_or_none"] == 3
    assert receipt["duplicate_platform_match_policy"] == (
        "adopt_most_recently_enumerated_non_closed_platform_match"
    )


def test_chrome_cdp_session_adopts_latest_unrelated_tiktok_page() -> None:
    class FakePage:
        def __init__(self, url: str) -> None:
            self.url = url

        def is_closed(self) -> bool:
            return False

    unrelated_creator = FakePage("https://www.tiktok.com/@someone_else")
    unrelated_path = FakePage("https://www.tiktok.com/@creator/video/123")
    created = FakePage("about:blank")

    class FakeContext:
        pages = [unrelated_creator, unrelated_path]

        def new_page(self) -> FakePage:
            return created

    engine = ChromeCdpPageObservationSessionEngine(humanize_context_fn=lambda _: None)
    engine._real_context = FakeContext()
    engine._pending_requested_page_url = "https://www.tiktok.com/@creator"

    assert engine._get_or_create_page() is unrelated_path
    receipt = engine.lifecycle_receipt
    assert receipt["initial_platform_match_count"] == 2
    assert receipt["initial_exact_match_count"] == 0
    assert receipt["page_adoption_count"] == 1
    assert receipt["page_creation_count"] == 0


def test_chrome_cdp_session_creates_only_when_no_tiktok_page_exists() -> None:
    class FakePage:
        def __init__(self, url: str) -> None:
            self.url = url

        def is_closed(self) -> bool:
            return False

    created = FakePage("about:blank")

    class FakeContext:
        pages = [FakePage("https://example.com/"), FakePage("https://chatgpt.com/")]

        def new_page(self) -> FakePage:
            return created

    engine = ChromeCdpPageObservationSessionEngine(humanize_context_fn=lambda _: None)
    engine._real_context = FakeContext()
    engine._pending_requested_page_url = "https://www.tiktok.com/@creator"

    assert engine._get_or_create_page() is created
    receipt = engine.lifecycle_receipt
    assert receipt["initial_platform_match_count"] == 0
    assert receipt["page_adoption_count"] == 0
    assert receipt["page_creation_count"] == 1


def test_chrome_cdp_session_suppresses_same_target_navigation_only() -> None:
    class FakePage:
        def __init__(self) -> None:
            self.url = "https://www.tiktok.com/@creator?lang=en#grid"
            self.goto_calls: list[str] = []

        def goto(self, url: str, **_kwargs: object) -> str:
            self.goto_calls.append(url)
            self.url = url
            return "navigated"

    page = FakePage()
    engine = ChromeCdpPageObservationSessionEngine(humanize_context_fn=lambda _: None)

    assert engine._navigate_page(page, "http://tiktok.com/@CREATOR/") is None
    assert engine._navigate_page(page, "https://www.tiktok.com/@other") == "navigated"
    assert page.goto_calls == ["https://www.tiktok.com/@other"]
    receipt = engine.lifecycle_receipt
    assert receipt["same_url_navigation_suppression_count"] == 1
    assert receipt["page_navigation_count"] == 1
