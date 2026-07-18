from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from runners import run_fragrantica_parser_fit_check as checker
from runners import run_source_capture_cloakbrowser_packet as cloak_runner
from source_capture import CaptureModeCategory
from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess
from source_capture.content_capture import RenderedContentCaptureSpec
from source_capture.fragrantica_projection import (
    FRAGRANTICA_PARSER_VERSION,
    build_fragrantica_content_record,
)


URL = "https://www.fragrantica.com/perfume/Test/Test-Fragrance-1.html"
SURFACE = "fragrantica_product_page_cloakbrowser_initial_viewport"
HTML = """
<html><head>
<link rel="canonical" href="https://www.fragrantica.com/perfume/Test/Test-Fragrance-1.html"/>
<meta name="description" content="Test Fragrance by Test House is a fragrance."/>
<title>Test Fragrance Test House perfume</title>
</head><body><div id="perfume-description-content">Test Fragrance by Test House</div></body></html>
"""


def _packet(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, mode: str = "sample"
) -> Path:
    monkeypatch.setattr(
        cloak_runner,
        "fetch_cloakbrowser_snapshot_capture",
        lambda **_kwargs: CloakBrowserSnapshotSuccess(
            requested_url=URL,
            final_url=URL,
            title="Test Fragrance",
            rendered_dom=HTML,
            visible_text="Test Fragrance by Test House",
            screenshot_png=b"\x89PNG\r\n\x1a\nfixture",
            metadata={
                "requested_url": URL,
                "final_url": URL,
                "capture_timestamp": "2026-07-18T00:00:00Z",
            },
            warning_notes=[],
            limitation_notes=[],
        ),
    )
    output = tmp_path / f"packet_{mode}"
    exit_code, _message = cloak_runner.run_source_capture_cloakbrowser_packet(
        url=URL,
        source_family="fragrance_native_database",
        source_surface=SURFACE,
        decision_question="What was visible?",
        output_directory=output,
        capture_context="parser-fit fixture",
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
            parser_version=FRAGRANTICA_PARSER_VERSION,
            projector=lambda dom, text, final_url: build_fragrantica_content_record(
                rendered_dom=dom,
                visible_text=text,
                source_url=final_url,
                source_surface=SURFACE,
            ),
        ),
    )
    assert exit_code == 0
    return output


def _artifact_path(packet: Path, filename: str) -> Path:
    manifest = json.loads((packet / "manifest.json").read_text(encoding="utf-8"))
    relative = next(
        item["relative_packet_path"]
        for item in manifest["preserved_files"]
        if Path(item["relative_packet_path"]).name.endswith(filename)
    )
    return packet / relative


def _rewrite_artifact_and_manifest(packet: Path, filename: str, body: bytes) -> None:
    artifact = _artifact_path(packet, filename)
    artifact.write_bytes(body)
    manifest_path = packet / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entry = next(
        item
        for item in manifest["preserved_files"]
        if Path(item["relative_packet_path"]).name.endswith(filename)
    )
    entry["sha256"] = hashlib.sha256(body).hexdigest()
    entry["size_bytes"] = len(body)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def test_fragrantica_parser_fit_matches_sample(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet = _packet(tmp_path, monkeypatch)

    result = checker.check_fragrantica_parser_fit(packet_or_manifest_path=packet)

    assert result["status"] == "match"
    assert result["current_parser_version"] == FRAGRANTICA_PARSER_VERSION


def test_fragrantica_parser_fit_detects_drift(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet = _packet(tmp_path, monkeypatch)
    path = _artifact_path(packet, "content_record.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["rows"][0]["source_object_name"] = "Drifted"
    _rewrite_artifact_and_manifest(
        packet,
        "content_record.json",
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )

    result = checker.check_fragrantica_parser_fit(packet_or_manifest_path=packet)

    assert result["status"] == "drift"
    assert result["difference"]["stored_sha256"] != result["difference"]["current_sha256"]


def test_fragrantica_parser_fit_rejects_parser_version_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet = _packet(tmp_path, monkeypatch)
    path = _artifact_path(packet, "content_capture_metadata.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["parser_version"] = "obsolete"
    _rewrite_artifact_and_manifest(
        packet,
        "content_capture_metadata.json",
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )

    with pytest.raises(checker.ParserFitCheckError) as exc:
        checker.check_fragrantica_parser_fit(packet_or_manifest_path=packet)
    assert exc.value.code == "parser_version_mismatch"


def test_fragrantica_parser_fit_rejects_bad_preserved_hash(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet = _packet(tmp_path, monkeypatch)
    _artifact_path(packet, "cloakbrowser_rendered_dom.html").write_text(
        "tampered", encoding="utf-8"
    )

    with pytest.raises(checker.ParserFitCheckError) as exc:
        checker.check_fragrantica_parser_fit(packet_or_manifest_path=packet)
    assert exc.value.code == "preserved_file_hash_mismatch"


@pytest.mark.parametrize("mode", ["content", "raw"])
def test_fragrantica_parser_fit_rejects_non_sample_packets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mode: str
) -> None:
    packet = _packet(tmp_path, monkeypatch, mode=mode)

    with pytest.raises(checker.ParserFitCheckError) as exc:
        checker.check_fragrantica_parser_fit(packet_or_manifest_path=packet)
    assert exc.value.code in {"sample_required", "preserved_file_mismatch"}


def test_fragrantica_parser_fit_rejects_source_mismatch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet = _packet(tmp_path, monkeypatch)
    manifest_path = packet / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["source_surface"] = "fragrantica_product_page_direct_http"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    with pytest.raises(checker.ParserFitCheckError) as exc:
        checker.check_fragrantica_parser_fit(packet_or_manifest_path=packet)
    assert exc.value.code == "source_mismatch"


def test_fragrantica_parser_fit_rejects_malformed_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    packet = _packet(tmp_path, monkeypatch)
    _rewrite_artifact_and_manifest(packet, "content_record.json", b"[]\n")

    with pytest.raises(checker.ParserFitCheckError) as exc:
        checker.check_fragrantica_parser_fit(packet_or_manifest_path=packet)
    assert exc.value.code == "content_record_shape"
