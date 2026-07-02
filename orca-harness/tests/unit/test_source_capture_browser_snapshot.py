from __future__ import annotations

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
    BrowserPageResponse,
    BrowserSnapshotFailure,
    BrowserSnapshotFailureKind,
    BrowserSnapshotSuccess,
    fetch_browser_context_responses,
    fetch_browser_page_observation_capture,
    fetch_browser_snapshot_capture,
)
from source_capture.proxy_profiles import ProxyCategory, ProxyProfile


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
    def __init__(self, event_log: list[str], *, method: str = "GET", resource_type: str = "fetch") -> None:
        self.event_log = event_log
        self.url = "https://api.example.test/widget"
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

    def move(self, x: float, y: float, *, steps: int) -> None:
        self.moves.append((x, y, steps))
        self.page.event_log.append(f"mouse_move:{steps}")

    def click(self, x: float, y: float) -> None:
        self.clicks.append((x, y))
        self.page.event_log.append("mouse_click")
        self.page.emit_response_once()


class _FakeObservationPage:
    def __init__(
        self,
        event_log: list[str],
        *,
        height: int = 3_000,
        pointer_target: dict[str, object] | None = None,
        pointer_targets: list[dict[str, object]] | None = None,
    ) -> None:
        self.event_log = event_log
        self.height = height
        self.url = "https://example.com/source"
        self.response_callback: object | None = None
        self.response_emitted = False
        self.pointer_target = pointer_target
        self.pointer_targets = list(pointer_targets or [])
        self.mouse = _FakeObservationMouse(self)

    def route(self, *_args: object, **_kwargs: object) -> None:
        self.event_log.append("route")

    def on(self, event: str, callback: object) -> None:
        assert event == "response"
        self.response_callback = callback

    def goto(self, *_args: object, **_kwargs: object) -> None:
        self.event_log.append("goto")

    def wait_for_timeout(self, timeout_ms: float) -> None:
        self.event_log.append(f"wait:{int(timeout_ms)}")

    def wait_for_selector(self, *_args: object, **_kwargs: object) -> None:
        self.event_log.append("wait_for_selector")

    def emit_response_once(self) -> None:
        if self.response_callback is not None and not self.response_emitted:
            self.response_callback(_FakeObservationResponse(self.event_log))  # type: ignore[operator]
            self.response_emitted = True

    def locator(self, selector: str) -> _FakeObservationLocator:
        assert selector == "body"
        return _FakeObservationLocator(self.event_log)

    def evaluate(self, script: str, arg: object | None = None) -> object:
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


def _install_fake_playwright(monkeypatch: pytest.MonkeyPatch, page: _FakeObservationPage) -> None:
    original_import_module = browser_snapshot_module.import_module

    def fake_import_module(name: str) -> object:
        if name == "playwright.sync_api":
            return _FakePlaywrightSyncApi(page)
        return original_import_module(name)

    monkeypatch.setattr(browser_snapshot_module, "import_module", fake_import_module)


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
        random_seed=7,
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
        random_seed=7,
    )




def test_fetch_browser_page_observation_capture_threads_pointer_actions_to_engine() -> None:
    engine = _ok_page_observation_engine()
    pointer_actions = (
        BrowserPagePointerAction(
            action_name=" open_comments ",
            candidate_selector=" button ",
            text_markers=(" Comments ",),
            random_seed=7,
        ),
        BrowserPagePointerAction(
            action_name=" more_like_this ",
            candidate_selector=" [role='tab'] ",
            text_markers=(" More like this ",),
            random_seed=8,
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
            random_seed=7,
        ),
        BrowserPagePointerAction(
            action_name="more_like_this",
            candidate_selector="[role='tab']",
            text_markers=("more like this",),
            random_seed=8,
        ),
    )
def test_pointer_action_target_script_matches_data_attributes() -> None:
    script = browser_snapshot_module._POINTER_ACTION_TARGET_SCRIPT
    assert "data-e2e" in script
    assert "data-testid" in script
    assert "data-test-id" in script
    assert "dataE2E === 'comment-icon'" in script


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
            wait_after_ms=2500,
            move_steps_min=7,
            move_steps_max=7,
            random_seed=11,
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
    assert "x" not in receipt
    assert "y" not in receipt
    assert result.metadata["post_load_action_executed"] is True
    assert result.responses[0].body_text == "{}"
    assert event_log.index("pointer_target_lookup") < event_log.index("mouse_move:7")
    assert event_log.index("mouse_move:7") < event_log.index("mouse_click")
    assert event_log.index("mouse_click") < event_log.index("wait:2500")
    assert event_log.index("wait:2500") < event_log.index("inner_text")
    assert event_log.index("dom_extract") < event_log.index("response_text")




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
