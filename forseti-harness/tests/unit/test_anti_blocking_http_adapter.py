import json

import pytest

import runners.run_source_capture_antiblock_http_packet as antiblock_runner
from source_capture import CaptureModeCategory
from source_capture.adapters.anti_blocking_http import (
    ANTI_BLOCKING_HTTP_METHOD_CATEGORY,
    DEFAULT_IMPERSONATION_PROFILE,
    AntiBlockingHttpCaptureFailure,
    AntiBlockingHttpCaptureFailureKind,
    AntiBlockingHttpCaptureSuccess,
    _capture_response,
    _validate_http_url,
    header_complete_profile,
)


class _FakeResponse:
    """Minimal duck-typed stand-in for an http.client response / HTTPError."""

    def __init__(self, *, status, body, headers=None, url="https://example.test/"):
        self._status = status
        self._buf = body
        self._off = 0
        self.headers = dict(headers or {})
        self._url = url
        self.reason = "OK" if status == 200 else "Forbidden"

    def getcode(self):
        return self._status

    def geturl(self):
        return self._url

    def read(self, size):
        chunk = self._buf[self._off : self._off + size]
        self._off += len(chunk)
        return chunk


def test_header_profile_is_browser_complete():
    headers = header_complete_profile()
    assert "Chrome/" in headers["User-Agent"]
    # Accept-Encoding identity keeps preserved bytes == served bytes (hash-honest).
    assert headers["Accept-Encoding"] == "identity"
    assert headers["Accept-Language"].startswith("en-US")
    assert "Sec-Fetch-Mode" in headers
    assert headers["Sec-CH-UA-Mobile"] == "?0"


def test_validate_http_url_rejects_non_http():
    with pytest.raises(ValueError):
        _validate_http_url("ftp://example.test/x")
    with pytest.raises(ValueError):
        _validate_http_url("not-a-url")


def test_capture_response_success_records_provenance():
    resp = _FakeResponse(status=200, body=b"<html>hello</html>", headers={"Content-Type": "text/html"})
    result = _capture_response(
        requested_url="https://example.test/",
        response=resp,
        timeout_seconds=10.0,
        max_bytes=1_000_000,
        impersonation_profile=DEFAULT_IMPERSONATION_PROFILE,
    )
    assert isinstance(result, AntiBlockingHttpCaptureSuccess)
    assert result.method_category == ANTI_BLOCKING_HTTP_METHOD_CATEGORY
    assert result.impersonation_profile == DEFAULT_IMPERSONATION_PROFILE
    assert result.body == b"<html>hello</html>"
    assert result.metadata["method_category"] == ANTI_BLOCKING_HTTP_METHOD_CATEGORY
    assert result.status == 200
    assert result.response_headers.get("Content-Type") == "text/html"


def test_capture_response_empty_body_is_no_body_failure():
    resp = _FakeResponse(status=200, body=b"")
    result = _capture_response(
        requested_url="https://example.test/",
        response=resp,
        timeout_seconds=10.0,
        max_bytes=1_000_000,
        impersonation_profile=DEFAULT_IMPERSONATION_PROFILE,
    )
    assert isinstance(result, AntiBlockingHttpCaptureSuccess)
    assert result.body == b""
    assert result.metadata["byte_count"] == 0


def test_capture_response_encoded_body_carries_limitation():
    resp = _FakeResponse(status=200, body=b"\x1f\x8bbytes", headers={"Content-Encoding": "gzip"})
    result = _capture_response(
        requested_url="https://example.test/",
        response=resp,
        timeout_seconds=10.0,
        max_bytes=1_000_000,
        impersonation_profile=DEFAULT_IMPERSONATION_PROFILE,
    )
    assert isinstance(result, AntiBlockingHttpCaptureSuccess)
    assert any("encoded_response_body" in item for item in result.limitation_notes)


def test_antiblock_runner_surfaces_empty_body_at_slice_and_capture_level(
    monkeypatch: pytest.MonkeyPatch, tmp_path
):
    result = AntiBlockingHttpCaptureSuccess(
        requested_url="https://example.test/",
        final_url="https://example.test/",
        status=200,
        reason="OK",
        impersonation_profile=DEFAULT_IMPERSONATION_PROFILE,
        method_category=ANTI_BLOCKING_HTTP_METHOD_CATEGORY,
        response_headers={"Content-Type": "text/html"},
        metadata={
            "requested_url": "https://example.test/",
            "final_url": "https://example.test/",
            "status": 200,
            "reason": "OK",
            "method_category": ANTI_BLOCKING_HTTP_METHOD_CATEGORY,
            "impersonation_profile": DEFAULT_IMPERSONATION_PROFILE,
            "content_type": "text/html",
            "content_length": 0,
            "content_encoding": None,
            "date": None,
            "last_modified": None,
            "etag": None,
            "response_headers": {"Content-Type": "text/html"},
            "capture_timestamp": "2026-06-06T00:00:00Z",
            "timeout_seconds": 10.0,
            "byte_count": 0,
        },
        body=b"",
        warning_notes=[],
        limitation_notes=[],
    )
    monkeypatch.setattr(antiblock_runner, "fetch_anti_blocking_http_capture", lambda **_: result)

    exit_code, _message = antiblock_runner.run_source_capture_antiblock_http_packet(
        url="https://example.test/",
        source_family="web_page",
        source_surface="anti_blocking_http",
        decision_question="What did the source return?",
        output_directory=tmp_path / "packet",
        capture_context="test",
        operator_category="test_operator",
        capture_mode=CaptureModeCategory.STRUCTURED_ACCESS,
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
        timeout_seconds=10.0,
        max_bytes=1000,
    )

    assert exit_code == 0
    manifest = json.loads((tmp_path / "packet" / "manifest.json").read_text(encoding="utf-8"))
    assert "empty/whitespace-only body" in manifest["access_posture"]["value"]
    assert any("empty/whitespace-only body" in item for item in manifest["limitations"])
    assert any(
        "empty/whitespace-only body" in item
        for item in manifest["source_slices"][0]["limitations"]
    )


def test_antiblock_runner_surfaces_encoded_body_limitation(
    monkeypatch: pytest.MonkeyPatch, tmp_path
):
    result = AntiBlockingHttpCaptureSuccess(
        requested_url="https://example.test/",
        final_url="https://example.test/",
        status=200,
        reason="OK",
        impersonation_profile=DEFAULT_IMPERSONATION_PROFILE,
        method_category=ANTI_BLOCKING_HTTP_METHOD_CATEGORY,
        response_headers={"Content-Encoding": "gzip"},
        metadata={
            "requested_url": "https://example.test/",
            "final_url": "https://example.test/",
            "status": 200,
            "reason": "OK",
            "method_category": ANTI_BLOCKING_HTTP_METHOD_CATEGORY,
            "impersonation_profile": DEFAULT_IMPERSONATION_PROFILE,
            "content_type": None,
            "content_length": None,
            "content_encoding": "gzip",
            "date": None,
            "last_modified": None,
            "etag": None,
            "response_headers": {"Content-Encoding": "gzip"},
            "capture_timestamp": "2026-06-06T00:00:00Z",
            "timeout_seconds": 10.0,
            "byte_count": 7,
        },
        body=b"\x1f\x8bbytes",
        warning_notes=[],
        limitation_notes=[
            "encoded_response_body: anti_blocking_http requested identity encoding but server returned Content-Encoding gzip; preserved bytes are as served and body classification cannot certify decoded source content"
        ],
    )
    monkeypatch.setattr(antiblock_runner, "fetch_anti_blocking_http_capture", lambda **_: result)

    exit_code, _message = antiblock_runner.run_source_capture_antiblock_http_packet(
        url="https://example.test/",
        source_family="web_page",
        source_surface="anti_blocking_http",
        decision_question="What did the source return?",
        output_directory=tmp_path / "packet",
        capture_context="test",
        operator_category="test_operator",
        capture_mode=CaptureModeCategory.STRUCTURED_ACCESS,
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
        timeout_seconds=10.0,
        max_bytes=1000,
    )

    assert exit_code == 0
    manifest = json.loads((tmp_path / "packet" / "manifest.json").read_text(encoding="utf-8"))
    assert "encoded body preserved" in manifest["access_posture"]["value"]
    assert any("encoded_response_body" in item for item in manifest["limitations"])
    assert any("encoded body" in item for item in manifest["source_slices"][0]["limitations"])


def test_capture_response_size_cap_via_content_length():
    resp = _FakeResponse(
        status=200, body=b"x" * 100, headers={"Content-Length": "10000000"}
    )
    result = _capture_response(
        requested_url="https://example.test/",
        response=resp,
        timeout_seconds=10.0,
        max_bytes=1000,
        impersonation_profile=DEFAULT_IMPERSONATION_PROFILE,
    )
    assert isinstance(result, AntiBlockingHttpCaptureFailure)
    assert result.failure_kind is AntiBlockingHttpCaptureFailureKind.SIZE_CAP_EXCEEDED
