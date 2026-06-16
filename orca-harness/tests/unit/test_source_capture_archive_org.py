from __future__ import annotations

import json
import shutil
import subprocess
import sys
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import parse_qs, urlparse

import pytest

import runners.run_source_capture_archive_packet as archive_runner
from runners.run_source_capture_archive_packet import ARCHIVE_ORG_NON_CLAIMS
from source_capture.adapters import archive_org
from source_capture.adapters.archive_org import (
    DEFAULT_CDX_LIMIT,
    ArchiveOrgCaptureFailure,
    ArchiveOrgCaptureSuccess,
    build_cdx_availability_url,
    fetch_archive_org_capture,
)
from source_capture.adapters.direct_http import (
    DirectHttpCaptureFailure,
    DirectHttpCaptureFailureKind,
    DirectHttpCaptureSuccess,
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
        "https://example.com/served-leak": [
            ["timestamp", "original", "statuscode", "mimetype", "digest"],
            ["20240101000000", "https://example.com/served-leak", "200", "text/html", "LEAK"],
        ],
        # Many-snapshot history spanning a cutoff. The fake CDX server returns the
        # full list (it ignores the server-side to=/limit bound); client-side
        # select_snapshot must still return the latest pre-cutoff row, proving the
        # selection invariant holds when the bound only shrinks the response.
        "https://example.com/many": [
            ["timestamp", "original", "statuscode", "mimetype", "digest"],
            ["20251201000000", "https://example.com/many", "200", "text/html", "M12"],
            ["20250901000000", "https://example.com/many", "200", "text/html", "M11"],
            ["20250601000000", "https://example.com/many", "200", "text/html", "M10"],
            ["20240701000000", "https://example.com/many", "200", "text/html", "M09"],
            ["20240515000000", "https://example.com/many", "200", "text/html", "M08"],
            ["20240301000000", "https://example.com/many", "200", "text/html", "M07"],
            ["20231101000000", "https://example.com/many", "200", "text/html", "M06"],
            ["20230815000000", "https://example.com/many", "200", "text/html", "M05"],
            ["20230101000000", "https://example.com/many", "200", "text/html", "M04"],
            ["20220601000000", "https://example.com/many", "200", "text/html", "M03"],
            ["20211231000000", "https://example.com/many", "200", "text/html", "M02"],
            ["20200101000000", "https://example.com/many", "200", "text/html", "M01"],
        ],
    }

    body_payloads = {
        ("20240101000000", "https://example.com/with-body"): (200, b"<html>archived body</html>"),
        ("20240101000000", "https://example.com/body-fails"): (204, b""),
        ("20240101000000", "https://example.com/body-404"): (404, b"archived error body"),
        ("20240101000000", "https://example.com/multi"): (200, b"old archived body"),
        ("20250101000000", "https://example.com/multi"): (200, b"new archived body"),
        ("20240101000000", "https://example.com/dict-format"): (200, b"dict archived body"),
        ("20240515000000", "https://example.com/many"): (200, b"<html>latest pre-cutoff body</html>"),
        ("20250101000000", "https://example.com/served-leak"): (200, b"<html>post-cutoff leaked body</html>"),
    }

    # Slice G: a pre-cutoff selected snapshot whose replay 302s to a POST-cutoff capture.
    body_redirects = {
        ("20240101000000", "https://example.com/served-leak"): "20250101000000",
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
                redirect_ts = body_redirects.get((timestamp, original_url))
                if redirect_ts is not None:
                    self.send_response(302)
                    self.send_header("Location", f"{base}/web/{redirect_ts}/{original_url}")
                    self.end_headers()
                    return
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


def test_build_cdx_availability_url_bounds_query_with_cutoff_and_limit() -> None:
    url = build_cdx_availability_url(
        original_url="https://example.com/page",
        cutoff_timestamp="20240601000000",
        limit=-10,
    )

    query = parse_qs(urlparse(url).query)
    assert query["to"] == ["20240601000000"]
    assert query["limit"] == ["-10"]
    assert query["collapse"] == ["digest"]
    assert query["url"] == ["https://example.com/page"]


def test_build_cdx_availability_url_omits_to_without_cutoff() -> None:
    url = build_cdx_availability_url(
        original_url="https://example.com/page",
        limit=-10,
    )

    query = parse_qs(urlparse(url).query)
    assert "to" not in query
    assert query["limit"] == ["-10"]
    assert query["collapse"] == ["digest"]


def test_fetch_archive_org_capture_bounds_cdx_query_and_selects_latest_pre_cutoff(
    archive_server: dict[str, str],
) -> None:
    result = fetch_archive_org_capture(
        original_url="https://example.com/many",
        cutoff_timestamp="20240601000000",
        cdx_endpoint=archive_server["cdx_endpoint"],
        snapshot_base_url=archive_server["snapshot_base_url"],
        timeout_seconds=5,
        max_bytes=1024,
    )

    assert isinstance(result, ArchiveOrgCaptureSuccess)
    query = parse_qs(urlparse(result.availability_url).query)
    assert query["to"] == ["20240601000000"]
    assert query["limit"] == [str(DEFAULT_CDX_LIMIT)]
    assert query["collapse"] == ["digest"]
    assert result.selected_snapshot is not None
    assert result.selected_snapshot.timestamp == "20240515000000"
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


def test_archive_runner_emits_typed_archive_snapshot_time(
    archive_server: dict[str, str],
    scratch_dir: Path,
) -> None:
    # Anchor goal: the archived snapshot's own time is a typed producer field, normalized to
    # ISO-8601 Z, on the packet timing and both archive slices -- and capture_time stays the
    # (distinct) fetch/access time, never collapsed onto the snapshot time.
    output_dir = scratch_dir / "packet"
    result = _run_archive_runner(
        archive_server=archive_server,
        output_dir=output_dir,
        original_url="https://example.com/with-body",
    )

    assert result.returncode == 0, result.stderr
    manifest = _read_manifest(output_dir)

    snapshot_time = manifest["timing"]["archive_snapshot_time"]
    assert snapshot_time["status"] == "known"
    assert snapshot_time["value"] == "2024-01-01T00:00:00Z"

    capture_time = manifest["timing"]["capture_time"]
    assert capture_time["status"] == "known"
    # capture_time is the fetch wall-clock; it must NOT be repurposed as the snapshot time.
    assert capture_time["value"] != snapshot_time["value"]

    availability_slice, body_slice = manifest["source_slices"]
    assert availability_slice["timing"]["archive_snapshot_time"] == snapshot_time
    assert body_slice["timing"]["archive_snapshot_time"] == snapshot_time


def test_archive_runner_types_archive_snapshot_time_unknown_when_no_snapshot(
    archive_server: dict[str, str],
    scratch_dir: Path,
) -> None:
    # Absent path: no snapshot selected -> typed unknown_with_reason, never fabricated or fetch
    # time.
    output_dir = scratch_dir / "packet"
    result = _run_archive_runner(
        archive_server=archive_server,
        output_dir=output_dir,
        original_url="https://example.com/no-snapshot",
    )

    assert result.returncode == 0, result.stderr
    manifest = _read_manifest(output_dir)
    snapshot_time = manifest["timing"]["archive_snapshot_time"]
    assert snapshot_time["status"] == "unknown_with_reason"
    assert snapshot_time["reason"] == "no Archive.org snapshot was selected"


def test_normalize_wayback_timestamp_present_and_unparseable() -> None:
    # Present: 14-digit Wayback form -> ISO-8601 Z.
    assert archive_runner._normalize_wayback_timestamp("20240101000000") == "2024-01-01T00:00:00Z"
    assert archive_runner._normalize_wayback_timestamp("20231231235959") == "2023-12-31T23:59:59Z"
    # Unparseable: wrong length, non-numeric, empty, or an impossible date -> None.
    assert archive_runner._normalize_wayback_timestamp("2024") is None
    assert archive_runner._normalize_wayback_timestamp("not-a-timestamp") is None
    assert archive_runner._normalize_wayback_timestamp("") is None
    assert archive_runner._normalize_wayback_timestamp("20241301000000") is None  # month 13


def test_archive_snapshot_time_fact_present_absent_unparseable() -> None:
    present = SimpleNamespace(selected_snapshot=SimpleNamespace(timestamp="20240101000000"))
    fact = archive_runner._archive_snapshot_time_fact(present)
    assert fact.status == "known"
    assert fact.value == "2024-01-01T00:00:00Z"

    absent = SimpleNamespace(selected_snapshot=None)
    fact = archive_runner._archive_snapshot_time_fact(absent)
    assert fact.status == "unknown_with_reason"
    assert fact.reason == "no Archive.org snapshot was selected"

    unparseable = SimpleNamespace(selected_snapshot=SimpleNamespace(timestamp="2024"))
    fact = archive_runner._archive_snapshot_time_fact(unparseable)
    assert fact.status == "unknown_with_reason"
    assert "not a parseable 14-digit Wayback timestamp" in fact.reason


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


def test_archive_runner_rejects_non_2xx_body_as_not_decision_grade(
    archive_server: dict[str, str],
    scratch_dir: Path,
) -> None:
    # A selected pre-cutoff snapshot whose body fetch returns a non-2xx (HTTP 404) WITH a body:
    # direct_http preserves it as a DirectHttpCaptureSuccess, but availability is not body honesty.
    # The 2xx gate in verify_archive_body fails it, so the body is NOT preserved as addressable
    # content (G-002), the posture is attempt_failed (not "archived"), and the failure is recorded.
    output_dir = scratch_dir / "packet"
    result = _run_archive_runner(
        archive_server=archive_server,
        output_dir=output_dir,
        original_url="https://example.com/body-404",
    )

    assert result.returncode == 0, result.stderr
    manifest = _read_manifest(output_dir)
    assert manifest["archive_history_posture"]["value"] == "attempt_failed"
    body_slice = manifest["source_slices"][1]
    assert body_slice["slice_id"] == "archive_snapshot_body"
    assert body_slice["archive_history_posture"]["value"] == "attempt_failed"
    # G-002: the non-2xx body is NOT preserved as addressable content -- only availability (file_01).
    assert body_slice["preserved_file_ids"] == []
    assert len(manifest["preserved_files"]) == 1
    assert not (output_dir / "raw" / "02_archive_snapshot_body.bin").exists()
    assert any(
        "archive_body_verification_failed" in item and "body_http_status_not_usable" in item
        for item in manifest["limitations"]
    )
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


def test_fetch_with_retry_recovers_after_transient_rate_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    # A 503 (empty-body failure form) on the first two attempts, then a 200: the
    # retry wrapper backs off and recovers instead of surfacing the transient
    # throttle as a capture failure. This is the recurring CDX 503 the batch hit.
    sleeps: list[float] = []
    calls = {"n": 0}

    def fake_fetch(*, url: str, timeout_seconds: float, max_bytes: int):
        calls["n"] += 1
        if calls["n"] < 3:
            return DirectHttpCaptureFailure(
                requested_url=url,
                failure_kind=DirectHttpCaptureFailureKind.NO_BODY,
                message="HTTP 503 empty body",
                status=503,
            )
        return DirectHttpCaptureSuccess(
            requested_url=url,
            final_url=url,
            status=200,
            reason="OK",
            metadata={},
            body=b"ok",
            warning_notes=[],
            limitation_notes=[],
        )

    monkeypatch.setattr(archive_org, "fetch_direct_http_capture", fake_fetch)
    monkeypatch.setattr(archive_org.time, "sleep", lambda seconds: sleeps.append(seconds))

    result = archive_org._fetch_with_retry(
        url="https://web.archive.org/cdx/search/cdx",
        timeout_seconds=5,
        max_bytes=1024,
        max_attempts=4,
        retry_backoff_seconds=2.0,
    )

    assert isinstance(result, DirectHttpCaptureSuccess)
    assert result.status == 200
    assert calls["n"] == 3  # two retries, then success
    assert sleeps == [2.0, 4.0]  # exponential backoff between attempts


def test_fetch_with_retry_exhausts_then_returns_last_rate_limited(monkeypatch: pytest.MonkeyPatch) -> None:
    # Persistent 503 across all attempts: give up after exactly max_attempts and
    # return the last (still rate-limited) result, so the caller's existing honest
    # recording (access_failed limitation / non-zero runner exit) applies -- never
    # a fabricated success.
    calls = {"n": 0}

    def fake_fetch(*, url: str, timeout_seconds: float, max_bytes: int):
        calls["n"] += 1
        return DirectHttpCaptureFailure(
            requested_url=url,
            failure_kind=DirectHttpCaptureFailureKind.NO_BODY,
            message="HTTP 503 empty body",
            status=503,
        )

    monkeypatch.setattr(archive_org, "fetch_direct_http_capture", fake_fetch)
    monkeypatch.setattr(archive_org.time, "sleep", lambda seconds: None)

    result = archive_org._fetch_with_retry(
        url="https://web.archive.org/cdx/search/cdx",
        timeout_seconds=5,
        max_bytes=1024,
        max_attempts=3,
        retry_backoff_seconds=0,
    )

    assert calls["n"] == 3
    assert getattr(result, "status", None) == 503


def test_fetch_with_retry_does_not_retry_non_rate_limit_status(monkeypatch: pytest.MonkeyPatch) -> None:
    # A 404 is a real result, not a transient throttle: return it on the first
    # attempt without retrying, so genuine non-2xx is neither slowed nor masked.
    calls = {"n": 0}

    def fake_fetch(*, url: str, timeout_seconds: float, max_bytes: int):
        calls["n"] += 1
        return DirectHttpCaptureSuccess(
            requested_url=url,
            final_url=url,
            status=404,
            reason="Not Found",
            metadata={},
            body=b"missing",
            warning_notes=[],
            limitation_notes=[],
        )

    monkeypatch.setattr(archive_org, "fetch_direct_http_capture", fake_fetch)
    monkeypatch.setattr(
        archive_org.time, "sleep", lambda seconds: pytest.fail("must not sleep on a non-rate-limit status")
    )

    result = archive_org._fetch_with_retry(
        url="https://web.archive.org/cdx/search/cdx",
        timeout_seconds=5,
        max_bytes=1024,
        max_attempts=4,
        retry_backoff_seconds=2.0,
    )

    assert calls["n"] == 1
    assert getattr(result, "status", None) == 404


def _body_success_for(final_url: str) -> DirectHttpCaptureSuccess:
    return DirectHttpCaptureSuccess(
        requested_url=final_url,
        final_url=final_url,
        status=200,
        reason="OK",
        metadata={},
        body=b"<html>archived</html>",
        warning_notes=[],
        limitation_notes=[],
    )


_ARCHIVE_BASE = "https://web.archive.org/web"


def test_verify_archive_body_clean_pre_cutoff_passes() -> None:
    v = archive_org.verify_archive_body(
        body_result=_body_success_for(f"{_ARCHIVE_BASE}/20230101000000/https://example.com/p"),
        requested_original_url="https://example.com/p",
        cutoff_timestamp="20230601000000",
        snapshot_base_url=_ARCHIVE_BASE,
    )
    assert v is not None and v.ok
    assert v.served_timestamp == "20230101000000"
    assert v.reason is None


def test_verify_archive_body_served_time_leak_fails() -> None:
    # Selection said pre-cutoff, but the SERVED snapshot (final_url after a 302) is post-cutoff.
    v = archive_org.verify_archive_body(
        body_result=_body_success_for(f"{_ARCHIVE_BASE}/20230912135629/https://example.com/p"),
        requested_original_url="https://example.com/p",
        cutoff_timestamp="20230101000000",
        snapshot_base_url=_ARCHIVE_BASE,
    )
    assert v is not None and not v.ok
    assert v.served_timestamp == "20230912135629"
    assert "served_time_leak" in (v.reason or "")


def test_verify_archive_body_equal_timestamp_boundary_passes() -> None:
    # served == cutoff is NOT a leak: the line is <= cutoff.
    v = archive_org.verify_archive_body(
        body_result=_body_success_for(f"{_ARCHIVE_BASE}/20230601000000/https://example.com/p"),
        requested_original_url="https://example.com/p",
        cutoff_timestamp="20230601000000",
        snapshot_base_url=_ARCHIVE_BASE,
    )
    assert v is not None and v.ok and v.served_timestamp == "20230601000000"


def test_verify_archive_body_tolerates_wayback_replay_modifier() -> None:
    # G-001: a clean pre-cutoff body served via an id_/if_ replay modifier must NOT false-fail.
    v = archive_org.verify_archive_body(
        body_result=_body_success_for(f"{_ARCHIVE_BASE}/20230101000000id_/https://example.com/p"),
        requested_original_url="https://example.com/p",
        cutoff_timestamp="20230601000000",
        snapshot_base_url=_ARCHIVE_BASE,
    )
    assert v is not None and v.ok
    assert v.served_timestamp == "20230101000000"


def test_verify_archive_body_off_archive_host_fails() -> None:
    # G-001: an off-archive redirect that mimics the /web/<ts>/<url> shape must NOT false-pass.
    v = archive_org.verify_archive_body(
        body_result=_body_success_for("https://evil.example/web/20230101000000/https://example.com/p"),
        requested_original_url="https://example.com/p",
        cutoff_timestamp="20230601000000",
        snapshot_base_url=_ARCHIVE_BASE,
    )
    assert v is not None and not v.ok
    assert "served_off_archive_host" in (v.reason or "")


def test_verify_archive_body_url_identity_mismatch_fails() -> None:
    v = archive_org.verify_archive_body(
        body_result=_body_success_for(f"{_ARCHIVE_BASE}/20230101000000/https://evil.example/other"),
        requested_original_url="https://example.com/p",
        cutoff_timestamp="20230601000000",
        snapshot_base_url=_ARCHIVE_BASE,
    )
    assert v is not None and not v.ok
    assert "served_url_identity_mismatch" in (v.reason or "")


def test_verify_archive_body_unparseable_served_time_with_cutoff_fails() -> None:
    # On-host but no parseable 14-digit ts + a cutoff set -> unverifiable is a FAILURE, not a pass.
    v = archive_org.verify_archive_body(
        body_result=_body_success_for(f"{_ARCHIVE_BASE}/garbage/https://example.com/p"),
        requested_original_url="https://example.com/p",
        cutoff_timestamp="20230601000000",
        snapshot_base_url=_ARCHIVE_BASE,
    )
    assert v is not None and not v.ok
    assert v.served_timestamp is None
    assert "served_time_unverifiable" in (v.reason or "")


def test_verify_archive_body_no_cutoff_does_not_leak_check() -> None:
    # No cutoff -> no leak check; an on-host parseable body passes and records its served ts.
    v = archive_org.verify_archive_body(
        body_result=_body_success_for(f"{_ARCHIVE_BASE}/20230101000000/https://example.com/p"),
        requested_original_url="https://example.com/p",
        cutoff_timestamp=None,
        snapshot_base_url=_ARCHIVE_BASE,
    )
    assert v is not None and v.ok and v.served_timestamp == "20230101000000"


def test_verify_archive_body_none_when_no_preserved_body() -> None:
    assert (
        archive_org.verify_archive_body(
            body_result=None,
            requested_original_url="https://example.com/p",
            cutoff_timestamp="20230601000000",
            snapshot_base_url=_ARCHIVE_BASE,
        )
        is None
    )
    failure = DirectHttpCaptureFailure(
        requested_url=f"{_ARCHIVE_BASE}/20230101000000/https://example.com/p",
        failure_kind=DirectHttpCaptureFailureKind.NO_BODY,
        message="HTTP 503 empty body",
        status=503,
    )
    assert (
        archive_org.verify_archive_body(
            body_result=failure,
            requested_original_url="https://example.com/p",
            cutoff_timestamp="20230601000000",
            snapshot_base_url=_ARCHIVE_BASE,
        )
        is None
    )


def test_archive_runner_flags_served_time_leak_as_not_decision_grade(
    archive_server: dict[str, str],
    scratch_dir: Path,
) -> None:
    # End-to-end: the selected snapshot is pre-cutoff (20240101 <= 20240601) but its replay
    # 302s to a post-cutoff capture (20250101). Slice G must flag it, never silently pass it.
    output_dir = scratch_dir / "packet"
    result = _run_archive_runner(
        archive_server=archive_server,
        output_dir=output_dir,
        original_url="https://example.com/served-leak",
    )

    assert result.returncode == 0, result.stderr
    manifest = _read_manifest(output_dir)
    assert manifest["archive_history_posture"]["value"] == "attempt_failed"
    assert any(
        "archive_body_verification_failed" in item and "served_time_leak" in item
        for item in manifest["limitations"]
    )
    body_slice = manifest["source_slices"][1]
    assert body_slice["slice_id"] == "archive_snapshot_body"
    assert body_slice["archive_history_posture"]["value"] == "attempt_failed"
    # G-002: the leaked post-cutoff body is NOT preserved as addressable content -- only the
    # availability metadata (file_01) survives; the served ts lives in the leak limitation.
    assert body_slice["preserved_file_ids"] == []
    assert len(manifest["preserved_files"]) == 1
    assert not (output_dir / "raw" / "02_archive_snapshot_body.bin").exists()
    _assert_receipt_non_claims(output_dir)


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
