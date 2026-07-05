from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from source_capture.adapters.cloakbrowser_snapshot import (
    CloakBrowserSnapshotFailure,
    CloakBrowserSnapshotFailureKind,
    CloakBrowserSnapshotSuccess,
)
from source_capture.block_shell import CaptureBodyClass, classify_capture_body
from source_capture.screening_browser_read import (
    BrowserScreenLight,
    BrowserScreeningReadRefused,
    screening_browser_read,
)
from source_capture.screening_read import ScreeningReadDispatch


_HARNESS_ROOT = Path(__file__).resolve().parents[2]
_MODULE_PATH = _HARNESS_ROOT / "source_capture" / "screening_browser_read.py"


def _dispatch() -> ScreeningReadDispatch:
    return ScreeningReadDispatch(screen_id="screen-1", question="What visible text does this public page show?")


def _browser_success(*, rendered_dom: str, visible_text: str) -> CloakBrowserSnapshotSuccess:
    return CloakBrowserSnapshotSuccess(
        requested_url="https://www.basenotes.com/source",
        final_url="https://www.basenotes.com/source",
        title="Visible Source",
        rendered_dom=rendered_dom,
        visible_text=visible_text,
        screenshot_png=b"\x89PNG\r\n\x1a\ncloakbrowser",
        metadata={
            "requested_url": "https://www.basenotes.com/source",
            "final_url": "https://www.basenotes.com/source",
            "title": "Visible Source",
            "capture_timestamp": "2026-06-21T00:00:00Z",
            "timeout_seconds": 20,
            "wait_until": "load",
            "viewport_width": 1280,
            "viewport_height": 720,
            "method_category": "anti_blocking_browser",
            "browser_engine": "cloakbrowser",
            "profile_persistence": "none",
            "storage_state_loaded": False,
            "proxy_used": False,
            "proxy_endpoint_recorded": False,
            "proxy_exit_ip_recorded": False,
            "rendered_dom_byte_count": len(rendered_dom.encode("utf-8")),
            "visible_text_byte_count": len(visible_text.encode("utf-8")),
            "screenshot_byte_count": 20,
        },
        warning_notes=[],
        limitation_notes=[],
    )


def test_browser_read_returns_visible_text_only_with_screen_light_shape() -> None:
    rendered_dom = "<html><body><main>Visible Basenotes discussion</main></body></html>"
    visible_text = "Visible Basenotes discussion"
    with patch(
        "source_capture.screening_browser_read.fetch_cloakbrowser_snapshot_capture",
        return_value=_browser_success(rendered_dom=rendered_dom, visible_text=visible_text),
    ) as mock_fetch:
        result = screening_browser_read(
            url="https://www.basenotes.com/source",
            dispatch=_dispatch(),
            timeout_seconds=9,
            wait_until="domcontentloaded",
            block_heavy_assets=True,
            settle_seconds=1,
            scroll_passes=1,
        )

    mock_fetch.assert_called_once()
    _, kwargs = mock_fetch.call_args
    assert kwargs["proxy_profile"] is None
    assert kwargs["pre_capture"] is None
    assert kwargs["timeout_seconds"] == 9
    assert kwargs["wait_until"] == "domcontentloaded"
    assert kwargs["block_heavy_assets"] is True
    assert isinstance(result, BrowserScreenLight)
    assert result.visible_text == visible_text
    assert result.visible_text_byte_count == len(visible_text.encode("utf-8"))
    assert result.content_class == CaptureBodyClass.CONTENT_UNVERIFIED.value
    assert not hasattr(result, "rendered_dom")
    assert not hasattr(result, "screenshot_png")
    assert any("visible text only" in note for note in result.warning_notes)


def test_browser_read_classifies_visible_text_not_full_dom_for_cloudflare_residual_script() -> None:
    rendered_dom = """
    <html>
      <head><script src="/cdn-cgi/challenge-platform/h/b/orchestrate/jsch/v1"></script></head>
      <body><main>Basenotes Mojave Ghost forum discussion text</main></body>
    </html>
    """
    visible_text = "Basenotes Mojave Ghost forum discussion text"
    with patch(
        "source_capture.screening_browser_read.fetch_cloakbrowser_snapshot_capture",
        return_value=_browser_success(rendered_dom=rendered_dom, visible_text=visible_text),
    ):
        result = screening_browser_read(url="https://www.basenotes.com/source", dispatch=_dispatch())

    assert isinstance(result, BrowserScreenLight)
    assert result.content_class == CaptureBodyClass.CONTENT_UNVERIFIED.value
    full_dom_class = classify_capture_body(status=200, headers={}, body=rendered_dom.encode("utf-8"))
    assert full_dom_class.classification is CaptureBodyClass.BLOCK_SHELL
    assert full_dom_class.signal == "cloudflare_challenge"


def test_browser_read_refuses_walker_direct_before_render() -> None:
    dispatch = ScreeningReadDispatch(
        screen_id="screen-1",
        question="one source",
        invoked_by="walker",  # type: ignore[arg-type]
    )
    with patch("source_capture.screening_browser_read.fetch_cloakbrowser_snapshot_capture") as mock_fetch:
        result = screening_browser_read(url="https://www.basenotes.com/source", dispatch=dispatch)

    mock_fetch.assert_not_called()
    assert isinstance(result, BrowserScreeningReadRefused)
    assert result.reason == "not_orchestrator_invoked"


def test_browser_read_refuses_auth_surface_before_render() -> None:
    with patch("source_capture.screening_browser_read.fetch_cloakbrowser_snapshot_capture") as mock_fetch:
        result = screening_browser_read(url="https://www.basenotes.com/login", dispatch=_dispatch())

    mock_fetch.assert_not_called()
    assert isinstance(result, BrowserScreeningReadRefused)
    assert result.reason == "entitlement_gated"


def test_browser_read_failure_is_refusal_without_packet_path() -> None:
    with patch(
        "source_capture.screening_browser_read.fetch_cloakbrowser_snapshot_capture",
        return_value=CloakBrowserSnapshotFailure(
            requested_url="https://www.basenotes.com/source",
            failure_kind=CloakBrowserSnapshotFailureKind.CAPTURE_FAILED,
            message="render failed visibly",
        ),
    ):
        result = screening_browser_read(url="https://www.basenotes.com/source", dispatch=_dispatch())

    assert isinstance(result, BrowserScreeningReadRefused)
    assert result.reason == "fetch_failed"
    assert "render failed visibly" in result.message


def test_browser_screen_light_has_no_packet_or_ecr_fields() -> None:
    fields = {field.name for field in BrowserScreenLight.__dataclass_fields__.values()}
    forbidden = {"packet", "packet_path", "manifest", "manifest_path", "staged_artifacts", "ecr"}
    assert not (fields & forbidden)
