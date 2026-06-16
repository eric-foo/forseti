from __future__ import annotations

import json
import subprocess
import sys
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pytest

_CUTOFF = "2024-06-01T00:00:00Z"
_ARCHIVED_BODY = b"<html>cross-archive verified body</html>"


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"historical_capture_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        import shutil

        shutil.rmtree(path, ignore_errors=True)


def _cdx(rows: list[list[str]]) -> bytes:
    return json.dumps(rows).encode("utf-8")


def _timemap_body(*, base: str, original: str, mementos: list[str]) -> bytes:
    lines = [
        f"<{original}>; rel=\"original\"",
        f"<{base}/timegate/{original}>; rel=\"timegate\"",
    ]
    for index, timestamp in enumerate(mementos):
        rel = "first memento" if index == 0 else "memento"
        lines.append(f"<{base}/{timestamp}/{original}>; rel=\"{rel}\"; datetime=\"Mon, 01 Jan 2024 00:00:00 GMT\"")
    return (",\n".join(lines) + "\n").encode("utf-8")


_CDX_HEADER = ["timestamp", "original", "statuscode", "mimetype", "digest"]


@pytest.fixture
def combined_server():
    base_holder: dict[str, str] = {}

    # Wayback CDX rows per original (empty rows => Wayback miss).
    cdx_rows = {
        "https://example.com/wb-hit": [
            _CDX_HEADER,
            ["20240101000000", "https://example.com/wb-hit", "200", "text/html", "D1"],
        ],
        "https://example.com/at-hit": [_CDX_HEADER],
        "https://example.com/at-leak": [_CDX_HEADER],
        "https://example.com/all-miss": [_CDX_HEADER],
    }
    # archive.today TimeMap mementos per original.
    timemap_mementos = {
        "https://example.com/at-hit": ["20240101000000"],
        "https://example.com/at-leak": ["20240101000000"],
        "https://example.com/all-miss": ["20250101000000"],  # post-cutoff only -> archive.today miss
    }
    # archive.today memento body 302 -> post-cutoff capture (served-time leak).
    memento_redirects = {("20240101000000", "https://example.com/at-leak"): "20250101000000"}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args) -> None:
            return

        def do_GET(self) -> None:  # noqa: N802
            base = base_holder["base"]
            parsed = urlparse(self.path)
            route = parsed.path

            if route == "/cdx/search/cdx":
                original = parse_qs(parsed.query).get("url", [""])[0]
                rows = cdx_rows.get(original)
                if rows is None:
                    self._send(500, b"unexpected cdx url", "text/plain")
                    return
                self._send(200, _cdx(rows), "application/json")
                return

            if route.startswith("/web/"):
                _, _, _timestamp, original = route.split("/", 3)
                self._send(200, _ARCHIVED_BODY, "text/html")
                return

            if route.startswith("/timemap/"):
                original = route[len("/timemap/"):]
                mementos = timemap_mementos.get(original)
                if mementos is None:
                    self._send(500, b"unexpected timemap url", "text/plain")
                    return
                self._send(200, _timemap_body(base=base, original=original, mementos=mementos), "application/link-format")
                return

            segments = route.lstrip("/").split("/", 1)
            if len(segments) == 2 and segments[0].isdigit() and len(segments[0]) == 14:
                timestamp, original = segments
                redirect_ts = memento_redirects.get((timestamp, original))
                if redirect_ts is not None:
                    self.send_response(302)
                    self.send_header("Location", f"{base}/{redirect_ts}/{original}")
                    self.end_headers()
                    return
                self._send(200, _ARCHIVED_BODY, "text/html")
                return

            self._send(404, b"not found", "text/plain")

        def _send(self, status: int, body: bytes, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.end_headers()
            if body:
                self.wfile.write(body)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        base = f"http://127.0.0.1:{port}"
        base_holder["base"] = base
        yield {
            "base": base,
            "cdx_endpoint": f"{base}/cdx/search/cdx",
            "snapshot_base_url": f"{base}/web",
            "timemap_base_url": f"{base}/timemap",
            "host": f"127.0.0.1:{port}",
        }
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def _run_runner(*, server: dict[str, str], output_dir: Path, url: str) -> subprocess.CompletedProcess[str]:
    project_root = Path(__file__).resolve().parents[2]
    return subprocess.run(
        [
            sys.executable,
            "runners/run_source_capture_historical_packet.py",
            "--url",
            url,
            "--decision-question",
            "What did this URL look like at or before the cutoff (any archive)?",
            "--cutoff-timestamp",
            _CUTOFF,
            "--output",
            str(output_dir),
            "--wayback-cdx-endpoint",
            server["cdx_endpoint"],
            "--wayback-snapshot-base-url",
            server["snapshot_base_url"],
            "--archive-today-timemap-base-url",
            server["timemap_base_url"],
            "--archive-today-host",
            server["host"],
            "--max-attempts",
            "1",
        ],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )


def _read_manifest(output_dir: Path) -> dict[str, object]:
    return json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))


def _read_locate_metadata(output_dir: Path) -> dict[str, object]:
    return json.loads((output_dir / "raw" / "01_archive_locate_metadata.json").read_text(encoding="utf-8"))


def test_wayback_hit_selected_and_archive_today_not_tried(combined_server, scratch_dir: Path) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_runner(server=combined_server, output_dir=output_dir, url="https://example.com/wb-hit")
    assert result.returncode == 0, result.stderr

    manifest = _read_manifest(output_dir)
    assert manifest["archive_history_posture"]["value"] == "archived"
    assert [item["slice_id"] for item in manifest["source_slices"]] == [
        "historical_locate_ladder",
        "historical_capture_body",
    ]
    locate = _read_locate_metadata(output_dir)
    assert locate["archive_selected"] == "wayback"
    assert locate["body_rung_used"] == "wayback"
    assert [entry["rung"] for entry in locate["archives_tried"]] == ["wayback"]  # stopped at first verified
    assert (output_dir / "raw" / "02_historical_capture_body.bin").read_bytes() == _ARCHIVED_BODY


def test_wayback_miss_archive_today_hit_records_ladder(combined_server, scratch_dir: Path) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_runner(server=combined_server, output_dir=output_dir, url="https://example.com/at-hit")
    assert result.returncode == 0, result.stderr

    manifest = _read_manifest(output_dir)
    assert manifest["archive_history_posture"]["value"] == "archived"
    locate = _read_locate_metadata(output_dir)
    assert locate["archive_selected"] == "archive_today"
    assert [entry["rung"] for entry in locate["archives_tried"]] == ["wayback", "archive_today"]
    assert locate["archives_tried"][0]["located"] is False  # wayback miss recorded
    assert locate["archives_tried"][1]["verified_body"] is True
    assert (output_dir / "raw" / "02_historical_capture_body.bin").read_bytes() == _ARCHIVED_BODY


def test_all_miss_is_honest_no_go_packet_with_locate_trace(combined_server, scratch_dir: Path) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_runner(server=combined_server, output_dir=output_dir, url="https://example.com/all-miss")
    assert result.returncode == 0, result.stderr

    manifest = _read_manifest(output_dir)
    assert manifest["archive_history_posture"]["value"] == "attempt_failed"
    assert [item["slice_id"] for item in manifest["source_slices"]] == ["historical_locate_ladder"]
    assert len(manifest["preserved_files"]) == 1  # only the locate trace
    assert any("historical_capture_no_go" in note for note in manifest["limitations"])
    locate = _read_locate_metadata(output_dir)
    assert locate["archive_selected"] is None
    assert all(entry["verified_body"] is False for entry in locate["archives_tried"])
    assert not (output_dir / "raw" / "02_historical_capture_body.bin").exists()


def test_served_time_leak_body_not_preserved(combined_server, scratch_dir: Path) -> None:
    output_dir = scratch_dir / "packet"
    result = _run_runner(server=combined_server, output_dir=output_dir, url="https://example.com/at-leak")
    assert result.returncode == 0, result.stderr

    manifest = _read_manifest(output_dir)
    # Leak => archive.today body not verified; no other rung => honest NO-GO; leaked body NOT preserved.
    assert manifest["archive_history_posture"]["value"] == "attempt_failed"
    assert len(manifest["preserved_files"]) == 1
    assert not (output_dir / "raw" / "02_historical_capture_body.bin").exists()
    locate = _read_locate_metadata(output_dir)
    archive_today_entry = next(e for e in locate["archives_tried"] if e["rung"] == "archive_today")
    assert archive_today_entry["located"] is True
    assert archive_today_entry["verified_body"] is False
    assert "served_time_leak" in archive_today_entry["body_detail"]
