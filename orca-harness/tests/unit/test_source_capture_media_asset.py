from __future__ import annotations

import json
import shutil
import subprocess
import sys
import threading
import uuid
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from runners import run_source_capture_media_packet as media_runner
from runners.run_source_capture_media_packet import MEDIA_ASSET_NON_CLAIMS
from source_capture import CaptureModeCategory
from source_capture.adapters.media_asset import (
    MediaAssetCaptureFailure,
    MediaAssetCaptureSuccess,
    fetch_media_assets,
)


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"source_capture_media_asset_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


@dataclass(frozen=True)
class _RouteResponse:
    status: int
    body: bytes
    headers: dict[str, str]


@pytest.fixture
def http_server():
    routes = {
        "/image": _RouteResponse(
            status=200,
            body=b"\x89PNG\r\n\x1a\norca-media-one",
            headers={
                "Content-Type": "image/png",
                "ETag": '"asset-etag-1"',
                "Last-Modified": "Tue, 02 Jun 2026 00:00:00 GMT",
                "Set-Cookie": "asset_session=should_not_be_preserved",
            },
        ),
        "/image-2": _RouteResponse(
            status=200,
            body=b"\xff\xd8\xfforca-media-two",
            headers={
                "Content-Type": "image/jpeg",
            },
        ),
        "/missing-with-body": _RouteResponse(
            status=404,
            body=b"asset missing but body present",
            headers={
                "Content-Type": "text/plain",
            },
        ),
        "/empty": _RouteResponse(
            status=204,
            body=b"",
            headers={
                "Content-Type": "image/png",
            },
        ),
        "/too-large": _RouteResponse(
            status=200,
            body=b"abcdef",
            headers={
                "Content-Type": "image/png",
                "Content-Length": "6",
            },
        ),
    }

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            route = routes.get(self.path)
            if route is None:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"unexpected path")
                return

            self.send_response(route.status)
            for key, value in route.headers.items():
                self.send_header(key, value)
            self.end_headers()
            if route.body:
                self.wfile.write(route.body)

        def log_message(self, format: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_fetch_media_assets_collects_successes_and_failures(http_server: str) -> None:
    batch = fetch_media_assets(
        asset_urls=[f"{http_server}/image", f"{http_server}/empty"],
        timeout_seconds=5,
        max_bytes=1024,
    )

    assert [item.asset_index for item in batch.successes] == [1]
    assert [item.asset_index for item in batch.failures] == [2]
    assert isinstance(batch.successes[0], MediaAssetCaptureSuccess)
    assert isinstance(batch.failures[0], MediaAssetCaptureFailure)


def test_media_runner_writes_single_asset_packet(http_server: str, scratch_dir: Path) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_media_runner(
        http_server=http_server,
        output_dir=output_dir,
        extra_args=[
            "--asset-url",
            f"{http_server}/image",
            "--cutoff-posture",
            "pre-cutoff explicit media asset capture",
        ],
    )

    assert result.returncode == 0, result.stderr
    manifest = _read_manifest(output_dir)
    assert manifest["source_surface"] == "media_asset_explicit_url"
    assert manifest["media_modality_posture"]["value"] == "media_asset preserved 1 asset body/bodies; 0 asset(s) not preserved"
    assert manifest["source_slices"][0]["slice_id"] == "asset_01"
    assert manifest["source_slices"][0]["preserved_file_ids"] == ["file_01", "file_02"]
    assert manifest["preserved_files"][0]["relative_packet_path"] == "raw/01_asset_01_body.bin"
    assert manifest["preserved_files"][1]["relative_packet_path"] == "raw/02_asset_01_metadata.json"
    assert manifest["receipt_metadata"]["non_claims"] == MEDIA_ASSET_NON_CLAIMS
    _assert_receipt_non_claims(output_dir)

    metadata = json.loads((output_dir / "raw" / "02_asset_01_metadata.json").read_text(encoding="utf-8"))
    assert metadata["asset_index"] == 1
    assert metadata["asset_url"] == f"{http_server}/image"
    assert metadata["direct_http_metadata"]["content_type"] == "image/png"
    assert "Set-Cookie" not in metadata["direct_http_metadata"]
    assert not (output_dir.parent / "asset_01_body.bin").exists()
    assert not (output_dir.parent / "asset_01_metadata.json").exists()


def test_media_runner_writes_multi_asset_packet(http_server: str, scratch_dir: Path) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_media_runner(
        http_server=http_server,
        output_dir=output_dir,
        extra_args=[
            "--asset-url",
            f"{http_server}/image",
            "--asset-url",
            f"{http_server}/image-2",
        ],
    )

    assert result.returncode == 0, result.stderr
    manifest = _read_manifest(output_dir)
    assert [item["slice_id"] for item in manifest["source_slices"]] == ["asset_01", "asset_02"]
    assert len(manifest["preserved_files"]) == 4
    assert manifest["source_slices"][1]["preserved_file_ids"] == ["file_03", "file_04"]
    assert manifest["preserved_files"][2]["relative_packet_path"] == "raw/03_asset_02_body.bin"
    assert manifest["preserved_files"][3]["relative_packet_path"] == "raw/04_asset_02_metadata.json"
    _assert_receipt_non_claims(output_dir)


def test_media_runner_keeps_mixed_failure_visible(http_server: str, scratch_dir: Path) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_media_runner(
        http_server=http_server,
        output_dir=output_dir,
        extra_args=[
            "--asset-url",
            f"{http_server}/image",
            "--asset-url",
            f"{http_server}/empty",
        ],
    )

    assert result.returncode == 0, result.stderr
    manifest = _read_manifest(output_dir)
    assert manifest["access_posture"]["value"] == "media_asset preserved 1 of 2 explicit asset URL(s)"
    failed_slice = manifest["source_slices"][1]
    assert failed_slice["slice_id"] == "asset_02"
    assert failed_slice["preserved_file_ids"] == []
    assert failed_slice["timing"]["capture_time"]["status"] == "unknown_with_reason"
    assert "not preserved" in failed_slice["media_modality_posture"]["value"]
    assert any("asset_02_not_preserved" in item for item in manifest["limitations"])
    _assert_receipt_non_claims(output_dir)


def test_media_runner_fails_without_packet_when_all_assets_fail(http_server: str, scratch_dir: Path) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_media_runner(
        http_server=http_server,
        output_dir=output_dir,
        extra_args=[
            "--asset-url",
            f"{http_server}/empty",
            "--asset-url",
            f"{http_server}/too-large",
            "--max-bytes",
            "5",
        ],
    )

    assert result.returncode == 3
    assert "no media assets were preserved" in result.stderr
    assert not output_dir.exists()


def test_media_runner_rejects_invalid_asset_url_without_packet(scratch_dir: Path) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_media_runner(
        http_server="",
        output_dir=output_dir,
        extra_args=[
            "--asset-url",
            "not-a-url",
        ],
    )

    assert result.returncode == 2
    assert "absolute http:// or https:// URL" in result.stderr
    assert not output_dir.exists()


def test_media_runner_rejects_existing_staging_file_without_packet(
    http_server: str,
    scratch_dir: Path,
) -> None:
    output_dir = scratch_dir / "packet"
    staging_file = output_dir.parent / "asset_01_body.bin"
    staging_file.write_bytes(b"leftover")

    result = _run_media_runner(
        http_server=http_server,
        output_dir=output_dir,
        extra_args=[
            "--asset-url",
            f"{http_server}/image",
        ],
    )

    assert result.returncode == 2
    assert "staging files already exist" in result.stderr
    assert staging_file.exists()
    assert not output_dir.exists()


def test_media_runner_cleans_staged_body_when_metadata_write_fails(
    http_server: str,
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = scratch_dir / "packet"

    def unserializable_metadata(*args: object, **kwargs: object) -> dict[str, object]:
        return {"bad": object()}

    monkeypatch.setattr(media_runner, "_asset_metadata", unserializable_metadata)

    with pytest.raises(TypeError):
        media_runner.run_source_capture_media_packet(
            asset_urls=[f"{http_server}/image"],
            source_family="media_asset",
            source_surface="media_asset_explicit_url",
            decision_question="Which source-meaningful media asset was visible before cutoff?",
            output_directory=output_dir,
            capture_context="test metadata failure",
            operator_category="media_asset_cli_operator",
            capture_mode=CaptureModeCategory.STRUCTURED_ACCESS,
            session_id=None,
            source_locator=None,
            actor_audience_context=None,
            visible_mode_changes=[],
            source_publication_or_event=None,
            source_edit_or_version=None,
            cutoff_posture=None,
            recapture_time=None,
            re_capture_relationship=None,
            warnings=[],
            limitations=[],
            timeout_seconds=5,
            max_bytes=1024,
        )

    assert not (output_dir.parent / "asset_01_body.bin").exists()
    assert not (output_dir.parent / "asset_01_metadata.json").exists()
    assert not output_dir.exists()


def test_media_runner_preserves_non_2xx_body_with_access_failed_limitation(
    http_server: str,
    scratch_dir: Path,
) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_media_runner(
        http_server=http_server,
        output_dir=output_dir,
        extra_args=[
            "--asset-url",
            f"{http_server}/missing-with-body",
        ],
    )

    assert result.returncode == 0, result.stderr
    manifest = _read_manifest(output_dir)
    assert manifest["source_slices"][0]["access_posture"]["value"].startswith(
        "media_asset access_failed with HTTP 404"
    )
    assert any("access_failed" in item for item in manifest["limitations"])


def _run_media_runner(*, http_server: str, output_dir: Path, extra_args: list[str]) -> subprocess.CompletedProcess[str]:
    project_root = Path(__file__).resolve().parents[2]
    return subprocess.run(
        [
            sys.executable,
            "runners/run_source_capture_media_packet.py",
            "--decision-question",
            "What source-meaningful media asset was visible before cutoff?",
            "--output",
            str(output_dir),
            *extra_args,
        ],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )


def _read_manifest(output_dir: Path) -> dict[str, object]:
    return json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))


def _assert_receipt_non_claims(output_dir: Path) -> None:
    receipt_text = (output_dir / "receipt.md").read_text(encoding="utf-8")
    for non_claim in MEDIA_ASSET_NON_CLAIMS:
        assert non_claim in receipt_text
