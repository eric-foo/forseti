from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from runners import run_source_capture_cloakbrowser_packet as runner
from source_capture import CaptureModeCategory
from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess
from source_capture.content_capture import RenderedContentCaptureSpec


def _logical_name(relative_packet_path: str) -> str:
    return re.sub(r"^\d+_", "", Path(relative_packet_path).name)


def _success(*, secret: str = "") -> CloakBrowserSnapshotSuccess:
    rendered_dom = f"<html><body>Fragrantica product {secret}</body></html>"
    return CloakBrowserSnapshotSuccess(
        requested_url="https://www.fragrantica.com/perfume/Test/Test-1.html",
        final_url="https://www.fragrantica.com/perfume/Test/Test-1.html",
        title="Test fragrance",
        rendered_dom=rendered_dom,
        visible_text="Fragrantica product",
        screenshot_png=b"\x89PNG\r\n\x1a\ncloakbrowser",
        metadata={
            "requested_url": "https://www.fragrantica.com/perfume/Test/Test-1.html",
            "final_url": "https://www.fragrantica.com/perfume/Test/Test-1.html",
            "capture_timestamp": "2026-07-18T00:00:00Z",
        },
        warning_notes=[],
        limitation_notes=[],
    )


def _run(
    *,
    output: Path,
    monkeypatch: pytest.MonkeyPatch,
    mode: str,
    projector=None,
    secret: str = "",
) -> tuple[int, str]:
    monkeypatch.setattr(
        runner,
        "fetch_cloakbrowser_snapshot_capture",
        lambda **_kwargs: _success(secret=secret),
    )
    return runner.run_source_capture_cloakbrowser_packet(
        url="https://www.fragrantica.com/perfume/Test/Test-1.html",
        source_family="fragrance_native_database",
        source_surface="fragrantica_product_page_cloakbrowser_initial_viewport",
        decision_question="What was visible?",
        output_directory=output,
        capture_context="test rendered content capture",
        operator_category="unit_test",
        capture_mode=CaptureModeCategory.MULTIMODAL,
        session_id=None,
        proxy_profile=None,
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
        block_heavy_assets=False,
        content_capture=RenderedContentCaptureSpec(
            capture_artifact_mode=mode,
            parser_version="test_parser_v1",
            projector=projector
            or (
                lambda rendered_dom, visible_text, final_url: {
                    "dom_bytes": len(rendered_dom),
                    "text_bytes": len(visible_text),
                    "source_url": final_url,
                }
            ),
        ),
    )


@pytest.mark.parametrize(
    ("mode", "expected", "absent"),
    [
        (
            "content",
            {
                "content_record.json",
                "content_capture_metadata.json",
                "cloakbrowser_viewport_screenshot.png",
                "cloakbrowser_snapshot_metadata.json",
            },
            {"cloakbrowser_rendered_dom.html", "cloakbrowser_visible_text.txt"},
        ),
        (
            "sample",
            {
                "content_record.json",
                "content_capture_metadata.json",
                "cloakbrowser_rendered_dom.html",
                "cloakbrowser_visible_text.txt",
                "cloakbrowser_viewport_screenshot.png",
                "cloakbrowser_snapshot_metadata.json",
            },
            set(),
        ),
        (
            "raw",
            {
                "content_capture_metadata.json",
                "cloakbrowser_rendered_dom.html",
                "cloakbrowser_visible_text.txt",
                "cloakbrowser_viewport_screenshot.png",
                "cloakbrowser_snapshot_metadata.json",
            },
            {"content_record.json"},
        ),
    ],
)
def test_rendered_content_capture_modes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mode: str,
    expected: set[str],
    absent: set[str],
) -> None:
    output = tmp_path / mode
    exit_code, _message = _run(output=output, monkeypatch=monkeypatch, mode=mode)

    assert exit_code == 0
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    names = {_logical_name(item["relative_packet_path"]) for item in manifest["preserved_files"]}
    assert names == expected
    assert names.isdisjoint(absent)
    metadata_name = next(
        item["relative_packet_path"]
        for item in manifest["preserved_files"]
        if _logical_name(item["relative_packet_path"]) == "content_capture_metadata.json"
    )
    metadata = json.loads((output / metadata_name).read_text(encoding="utf-8"))
    assert metadata["capture_artifact_mode"] == mode
    assert metadata["projection_status"] == (
        "not_attempted: raw mode" if mode == "raw" else "succeeded"
    )
    by_role = {item["role"]: item for item in metadata["inputs"]}
    assert by_role["screenshot"]["preserved"] is True
    assert by_role["browser_metadata"]["preserved"] is True
    assert by_role["rendered_dom"]["preserved"] is (mode != "content")
    assert by_role["visible_text"]["preserved"] is (mode != "content")
    if mode == "content":
        receipt = (output / "receipt.md").read_text(encoding="utf-8")
        assert "hashed then discarded" in receipt
        assert "with rendered DOM, visible text" not in receipt


def test_rendered_projection_failure_preserves_inputs_and_returns_exit_4(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail(*_args):
        raise RuntimeError("fixture drift")

    output = tmp_path / "failure"
    exit_code, _message = _run(
        output=output,
        monkeypatch=monkeypatch,
        mode="content",
        projector=fail,
    )

    assert exit_code == 4
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    names = {_logical_name(item["relative_packet_path"]) for item in manifest["preserved_files"]}
    assert "cloakbrowser_rendered_dom.html" in names
    assert "cloakbrowser_visible_text.txt" in names
    assert "content_record.json" not in names
    metadata_path = next(
        output / item["relative_packet_path"]
        for item in manifest["preserved_files"]
        if _logical_name(item["relative_packet_path"]) == "content_capture_metadata.json"
    )
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert metadata["projection_status"].startswith("failed: RuntimeError: fixture drift")


def test_rendered_content_capture_rejects_browser_secret_text(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    with pytest.raises(ValueError, match="browser-secret material"):
        _run(
            output=tmp_path / "secret",
            monkeypatch=monkeypatch,
            mode="content",
            secret="cf_clearance=secret",
        )


def test_browser_secret_guard_allows_inert_cookie_script_literals() -> None:
    runner._assert_no_browser_secret_bytes(
        [
            (
                "rendered_dom",
                b'<script>const labels = ["Cookie:", "Set-Cookie"];</script>',
            ),
            ("visible_text", b"Learn how document.cookie is used."),
        ]
    )


def test_browser_secret_guard_rejects_cookie_header_values() -> None:
    with pytest.raises(ValueError, match="browser-secret material"):
        runner._assert_no_browser_secret_bytes(
            [("rendered_dom", b"Cookie: session_id=secret")]
        )


def test_browser_secret_guard_rejects_storage_state_metadata() -> None:
    with pytest.raises(ValueError, match="browser-secret material"):
        runner._assert_no_browser_secret_bytes(
            [("browser_metadata", b'{"cookies":[],"origins": []}')]
        )
