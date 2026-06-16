from __future__ import annotations

import json
import shutil
import uuid
from dataclasses import dataclass, field
from pathlib import Path

import pytest

from runners import run_source_capture_browser_packet as browser_runner
from runners.run_source_capture_browser_packet import BROWSER_SNAPSHOT_NON_CLAIMS
from source_capture import CaptureModeCategory
from source_capture.adapters.browser_snapshot import (
    BrowserContextRequest,
    BrowserContextResponse,
    BrowserContextResponsesSuccess,
    BrowserSnapshotFailure,
    BrowserSnapshotFailureKind,
    BrowserSnapshotSuccess,
    fetch_browser_context_responses,
    fetch_browser_snapshot_capture,
)


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


def test_fetch_browser_snapshot_capture_rejects_negative_scroll() -> None:
    with pytest.raises(ValueError, match="scroll_passes must be zero or greater"):
        fetch_browser_snapshot_capture(url="https://example.com/source", scroll_passes=-1, engine=_ok_engine())
    with pytest.raises(ValueError, match="scroll_step_px must be zero or greater"):
        fetch_browser_snapshot_capture(url="https://example.com/source", scroll_step_px=-5, engine=_ok_engine())


def test_browser_snapshot_runner_writes_packet_with_four_artifacts(
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
    )

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
