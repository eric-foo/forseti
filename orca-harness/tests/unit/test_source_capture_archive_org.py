from __future__ import annotations

import json
import shutil
import subprocess
import sys
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

import runners.run_source_capture_archive_packet as archive_runner
from runners.run_source_capture_archive_packet import ARCHIVE_ORG_NON_CLAIMS
from source_capture.adapters.archive_org import (
    ArchiveOrgCaptureFailure,
    ArchiveOrgCaptureSuccess,
    fetch_archive_org_capture,
)


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"source_capture_archive_org_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


@pytest.fixture
def archive_server():
    cdx_payloads = {
        "https://example.com/no-snapshot": [
            ["timestamp", "original", "statuscode", "mimetype", "digest"],
        ],
        "https://example.com/with-body": [
            ["timestamp", "original", "statuscode", "mimetype", "digest"],
            ["20240101000000", "https://example.com/with-body", "200", "text/html", "DIGEST1"],
        ],
        "https://example.com/body-fails": [
            ["timestamp", "original", "statuscode", "mimetype", "digest"],
            ["20240101000000", "https://example.com/body-fails", "200", "text/html", "DIGEST2"],
        ],
        "https://example.com/body-404": [
            ["timestamp", "original", "statuscode", "mimetype", "digest"],
            ["20240101000000", "https://example.com/body-404", "404", "text/html", "DIGEST3"],
        ],
        "https://example.com/multi": [
            ["timestamp", "original", "statuscode", "mimetype", "digest"],
            ["20250101000000", "https://example.com/multi", "200", "text/html", "NEW"],
            ["20240101000000", "https://example.com/multi", "200", "text/html", "OLD"],
        ],
        "https://example.com/post-cutoff-only": [
            ["timestamp", "original", "statuscode", "mimetype", "digest"],
            ["20250101000000", "https://example.com/post-cutoff-only", "200", "text/html", "FUTURE"],
        ],
    }

    body_payloads = {
        ("20240101000000", "https://example.com/with-body"): (200, b"<html>archived body</html>"),
        ("20240101000000", "https://example.com/body-fails"): (204, b""),
        ("20240101000000", "https://example.com/body-404"): (404, b"archived error body"),
        ("20240101000000", "https://example.com/multi"): (200, b"old archived body"),
        ("20250101000000", "https://example.com/multi"): (200, b"new archived body"),
        ("20240101000000", "https://example.com/dict-format"): (200, b"dict archived body"),
    }

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            if parsed.path == "/cdx/search/cdx":
                query = parse_qs(parsed.query)
                original_url = query.get("url", [""])[0]
                if original_url == "https://example.com/availability-fails":
                    self.send_response(204)
                    self.end_headers()
                    return
                if original_url == "https://example.com/malformed-cdx":
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(b"{not valid json")
                    return
                if original_url == "https://example.com/dict-format":
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    payload = {
                        "url": "https://example.com/dict-format",
                        "archived_snapshots": {
                            "closest": {
                                "available": True,
                                "timestamp": "20240101000000",
                                "status": "200",
                                "url": f"{base}/web/20240101000000/https://example.com/dict-format",
                            }
                        },
                    }
                    self.wfile.write(json.dumps(payload).encode("utf-8"))
                    return
                payload = cdx_payloads.get(original_url)
                if payload is None:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(b"unexpected cdx url")
                    return
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(payload).encode("utf-8"))
                return

            if parsed.path.startswith("/web/"):
                _, _, timestamp, original_url = parsed.path.split("/", 3)
                key = (timestamp, original_url)
                response = body_payloads.get(key)
                if response is None:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(b"unexpected snapshot url")
                    return
                status, body = response
                self.send_response(status)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                if body:
                    self.wfile.write(body)
                return

            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"unexpected path")

        def log_message(self, format: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base = f"http://127.0.0.1:{server.server_address[1]}"
        yield {
            "base": base,
            "cdx_endpoint": f"{base}/cdx/search/cdx",
            "snapshot_base_url": f"{base}/web",
        }
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_fetch_archive_org_capture_selects_cutoff_snapshot(archive_server: dict[str, str]) -> None:
    result = fetch_archive_org_capture(
        original_url="https://example.com/multi",
        cutoff_timestamp="20240601000000",
        cdx_endpoint=archive_server["cdx_endpoint"],
        snapshot_base_url=archive_server["snapshot_base_url"],
        timeout_seconds=5,
        max_bytes=1024,
    )

    assert isinstance(result, ArchiveOrgCaptureSuccess)
    assert result.selected_snapshot is not None
    assert result.selected_snapshot.timestamp == "20240101000000"
    assert result.body_result is not None


def test_archive_runner_writes_no_snapshot_metadata_packet(
    archive_server: dict[str, str],
    scratch_dir: Path,
) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_archive_runner(
        archive_server=archive_server,
        output_dir=output_dir,
        original_url="https://example.com/no-snapshot",
    )

    assert result.returncode == 0, result.stderr
    manifest = _read_manifest(output_dir)
    assert manifest["source_surface"] == "archive_org_wayback"
    assert len(manifest["preserved_files"]) == 1
    assert [item["slice_id"] for item in manifest["source_slices"]] == ["archive_availability"]
    assert manifest["archive_history_posture"]["value"] == "attempt_failed"
    _assert_receipt_non_claims(output_dir)


def test_archive_runner_writes_metadata_and_body_packet(
    archive_server: dict[str, str],
    scratch_dir: Path,
) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_archive_runner(
        archive_server=archive_server,
        output_dir=output_dir,
        original_url="https://example.com/with-body",
    )

    assert result.returncode == 0, result.stderr
    manifest = _read_manifest(output_dir)
    assert len(manifest["preserved_files"]) == 3
    assert [item["slice_id"] for item in manifest["source_slices"]] == [
        "archive_availability",
        "archive_snapshot_body",
    ]
    body_slice = manifest["source_slices"][1]
    assert body_slice["preserved_file_ids"] == ["file_02", "file_03"]
    availability_slice = manifest["source_slices"][0]
    assert availability_slice["timing"]["source_edit_or_version"]["value"].startswith(
        "Archive.org availability metadata"
    )
    assert manifest["archive_history_posture"]["value"] == "archived"
    assert (output_dir / "raw" / "02_archive_snapshot_body.bin").read_bytes() == b"<html>archived body</html>"
    _assert_receipt_non_claims(output_dir)


def test_archive_runner_writes_metadata_packet_when_body_fails(
    archive_server: dict[str, str],
    scratch_dir: Path,
) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_archive_runner(
        archive_server=archive_server,
        output_dir=output_dir,
        original_url="https://example.com/body-fails",
    )

    assert result.returncode == 0, result.stderr
    manifest = _read_manifest(output_dir)
    assert len(manifest["preserved_files"]) == 1
    body_slice = manifest["source_slices"][1]
    assert body_slice["slice_id"] == "archive_snapshot_body"
    assert body_slice["preserved_file_ids"] == []
    assert body_slice["timing"]["capture_time"]["status"] == "unknown_with_reason"
    assert any("archive_snapshot_body_not_preserved" in item for item in manifest["limitations"])
    _assert_receipt_non_claims(output_dir)


def test_archive_runner_fails_without_packet_when_availability_lookup_fails(
    archive_server: dict[str, str],
    scratch_dir: Path,
) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_archive_runner(
        archive_server=archive_server,
        output_dir=output_dir,
        original_url="https://example.com/availability-fails",
    )

    assert result.returncode == 3
    assert "empty body" in result.stderr
    assert not output_dir.exists()


def test_archive_runner_preserves_non_2xx_body_with_access_failed_limitation(
    archive_server: dict[str, str],
    scratch_dir: Path,
) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_archive_runner(
        archive_server=archive_server,
        output_dir=output_dir,
        original_url="https://example.com/body-404",
    )

    assert result.returncode == 0, result.stderr
    manifest = _read_manifest(output_dir)
    body_slice = manifest["source_slices"][1]
    assert body_slice["access_posture"]["value"].startswith("archive_org snapshot body access_failed")
    assert body_slice["preserved_file_ids"] == ["file_02", "file_03"]
    assert any("access_failed" in item for item in manifest["limitations"])
    _assert_receipt_non_claims(output_dir)


def test_archive_runner_writes_metadata_packet_when_cdx_parse_fails(
    archive_server: dict[str, str],
    scratch_dir: Path,
) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_archive_runner(
        archive_server=archive_server,
        output_dir=output_dir,
        original_url="https://example.com/malformed-cdx",
    )

    assert result.returncode == 0, result.stderr
    manifest = _read_manifest(output_dir)
    assert len(manifest["preserved_files"]) == 1
    assert [item["slice_id"] for item in manifest["source_slices"]] == ["archive_availability"]
    assert manifest["archive_history_posture"]["value"] == "attempt_failed"
    assert any("parse_failed" in item for item in manifest["limitations"])
    metadata = json.loads((output_dir / "raw" / "01_archive_availability_metadata.json").read_text(encoding="utf-8"))
    assert metadata["parse_warning"].startswith("archive_org availability metadata parse_failed")
    _assert_receipt_non_claims(output_dir)


def test_archive_runner_writes_metadata_packet_when_cutoff_filters_all_snapshots(
    archive_server: dict[str, str],
    scratch_dir: Path,
) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_archive_runner(
        archive_server=archive_server,
        output_dir=output_dir,
        original_url="https://example.com/post-cutoff-only",
    )

    assert result.returncode == 0, result.stderr
    manifest = _read_manifest(output_dir)
    assert len(manifest["preserved_files"]) == 1
    assert [item["slice_id"] for item in manifest["source_slices"]] == ["archive_availability"]
    assert manifest["archive_history_posture"]["value"] == "attempt_failed"
    metadata = json.loads((output_dir / "raw" / "01_archive_availability_metadata.json").read_text(encoding="utf-8"))
    assert metadata["snapshot_count"] == 1
    assert metadata["selected_snapshot"] is None
    _assert_receipt_non_claims(output_dir)


def test_fetch_archive_org_capture_returns_failure_for_availability_lookup_failure(
    archive_server: dict[str, str],
) -> None:
    result = fetch_archive_org_capture(
        original_url="https://example.com/availability-fails",
        cdx_endpoint=archive_server["cdx_endpoint"],
        snapshot_base_url=archive_server["snapshot_base_url"],
        timeout_seconds=5,
        max_bytes=1024,
    )

    assert isinstance(result, ArchiveOrgCaptureFailure)


def test_fetch_archive_org_capture_parses_availability_dict_payload(
    archive_server: dict[str, str],
) -> None:
    result = fetch_archive_org_capture(
        original_url="https://example.com/dict-format",
        cdx_endpoint=archive_server["cdx_endpoint"],
        snapshot_base_url=archive_server["snapshot_base_url"],
        timeout_seconds=5,
        max_bytes=1024,
    )

    assert isinstance(result, ArchiveOrgCaptureSuccess)
    assert result.selected_snapshot is not None
    assert result.selected_snapshot.timestamp == "20240101000000"
    assert result.selected_snapshot.snapshot_url.endswith("/web/20240101000000/https://example.com/dict-format")
    assert result.body_result is not None


def test_archive_runner_cleans_snapshot_metadata_staging_after_metadata_write_failure(
    archive_server: dict[str, str],
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_dir = scratch_dir / "packet"
    real_write_text = Path.write_text

    def fail_after_partial_metadata_write(
        self: Path,
        data: str,
        encoding: str | None = None,
        errors: str | None = None,
        newline: str | None = None,
    ) -> int:
        if self.name == "archive_snapshot_body_metadata.json":
            self.write_bytes(b"partial metadata")
            raise OSError("simulated body metadata write failure")
        return real_write_text(self, data, encoding=encoding, errors=errors, newline=newline)

    monkeypatch.setattr(Path, "write_text", fail_after_partial_metadata_write)

    with pytest.raises(OSError, match="simulated body metadata write failure"):
        archive_runner.run_source_capture_archive_packet(
            original_url="https://example.com/with-body",
            source_family="archive_org",
            source_surface="archive_org_wayback",
            decision_question="What archived source state was visible before cutoff?",
            output_directory=output_dir,
            capture_context="Archive.org test capture",
            operator_category="test_operator",
            capture_mode=archive_runner.CaptureModeCategory.ARCHIVE_HISTORY,
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
            cutoff_timestamp="20240601000000",
            cdx_endpoint=archive_server["cdx_endpoint"],
            snapshot_base_url=archive_server["snapshot_base_url"],
            timeout_seconds=5,
            max_bytes=1024,
        )

    assert not (scratch_dir / "archive_snapshot_body.bin").exists()
    assert not (scratch_dir / "archive_snapshot_body_metadata.json").exists()


def _run_archive_runner(
    *,
    archive_server: dict[str, str],
    output_dir: Path,
    original_url: str,
) -> subprocess.CompletedProcess[str]:
    project_root = Path(__file__).resolve().parents[2]
    return subprocess.run(
        [
            sys.executable,
            "runners/run_source_capture_archive_packet.py",
            "--url",
            original_url,
            "--decision-question",
            "What archived source state was visible before cutoff?",
            "--cdx-endpoint",
            archive_server["cdx_endpoint"],
            "--snapshot-base-url",
            archive_server["snapshot_base_url"],
            "--cutoff-timestamp",
            "20240601000000",
            "--output",
            str(output_dir),
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
    for non_claim in ARCHIVE_ORG_NON_CLAIMS:
        assert non_claim in receipt_text
