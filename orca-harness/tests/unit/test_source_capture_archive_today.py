from __future__ import annotations

import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

import pytest

from source_capture.adapters import archive_today
from source_capture.adapters.archive_today import (
    ArchiveTodayBodyVerification,
    ArchiveTodayCaptureFailure,
    ArchiveTodayCaptureSuccess,
    fetch_archive_today_capture,
    parse_timemap_mementos,
    select_memento,
    verify_archive_today_body,
)
from source_capture.adapters.direct_http import (
    DirectHttpCaptureFailure,
    DirectHttpCaptureFailureKind,
    DirectHttpCaptureSuccess,
)

_CHALLENGE_BODY = (
    b"<html><head><title>Just a moment...</title></head>"
    b"<body>Checking your browser before accessing. challenge-platform</body></html>"
)
_CAPTCHA_CHALLENGE_BODY = b"<html><body>Please complete the captcha to verify you are human.</body></html>"
_CAPTCHA_ARTICLE_BODY = b"<html><body>This archived article discusses captcha usability.</body></html>"
_ARCHIVED_BODY = b"<html>archived archive.today body</html>"


def _timemap_body(*, base: str, original: str, mementos: list[tuple[str, str | None]]) -> bytes:
    # Build an application/link-format TimeMap whose memento URLs point at the fake server `base`.
    lines = [
        f"<{original}>; rel=\"original\"",
        f"<{base}/timegate/{original}>; rel=\"timegate\"",
    ]
    for index, (timestamp, datetime_value) in enumerate(mementos):
        rel = "first memento" if index == 0 else "memento"
        entry = f"<{base}/{timestamp}/{original}>; rel=\"{rel}\""
        if datetime_value is not None:
            entry += f"; datetime=\"{datetime_value}\""
        lines.append(entry)
    return (",\n".join(lines) + "\n").encode("utf-8")


@pytest.fixture
def archive_today_server():
    timemap_mementos: dict[str, list[tuple[str, str | None]]] = {
        "https://example.com/with-body": [
            ("20230101000000", "Sun, 01 Jan 2023 00:00:00 GMT"),
            ("20240101000000", "Mon, 01 Jan 2024 00:00:00 GMT"),
        ],
        "https://example.com/no-memento": [
            ("20250101000000", "Wed, 01 Jan 2025 00:00:00 GMT"),
        ],
        "https://example.com/served-leak": [
            ("20240101000000", "Mon, 01 Jan 2024 00:00:00 GMT"),
        ],
        "https://example.com/challenge-body": [
            ("20240101000000", "Mon, 01 Jan 2024 00:00:00 GMT"),
        ],
        "https://example.com/captcha-challenge-body": [
            ("20240101000000", "Mon, 01 Jan 2024 00:00:00 GMT"),
        ],
        "https://example.com/captcha-article": [
            ("20240101000000", "Mon, 01 Jan 2024 00:00:00 GMT"),
        ],
        "https://example.com/rate-limited-body": [
            ("20240101000000", "Mon, 01 Jan 2024 00:00:00 GMT"),
        ],
    }
    # A pre-cutoff memento whose body 302s to a POST-cutoff capture (the served-time leak).
    body_redirects: dict[tuple[str, str], tuple[str, str]] = {
        ("20240101000000", "https://example.com/served-leak"): (
            "20250101000000",
            "https://example.com/served-leak",
        ),
    }

    base_holder: dict[str, str] = {}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args) -> None:  # silence test server logging
            return

        def do_GET(self) -> None:  # noqa: N802
            base = base_holder["base"]
            path = self.path
            if path.startswith("/timemap/"):
                original = path[len("/timemap/"):]
                if original.endswith("challenge-timemap"):
                    self._send(200, _CHALLENGE_BODY, "text/html")
                    return
                if original.endswith("rate-limited"):
                    self._send(429, b"<html><title>archive.ph rate limited</title></html>", "text/html")
                    return
                mementos = timemap_mementos.get(original)
                if mementos is None:
                    self._send(500, b"unexpected timemap url", "text/plain")
                    return
                self._send(
                    200,
                    _timemap_body(base=base, original=original, mementos=mementos),
                    "application/link-format",
                )
                return

            segments = path.lstrip("/").split("/", 1)
            if len(segments) == 2 and segments[0].isdigit() and len(segments[0]) == 14:
                timestamp, original = segments
                redirect = body_redirects.get((timestamp, original))
                if redirect is not None:
                    redirect_ts, redirect_original = redirect
                    self.send_response(302)
                    self.send_header("Location", f"{base}/{redirect_ts}/{redirect_original}")
                    self.end_headers()
                    return
                if original.endswith("challenge-body"):
                    self._send(200, _CHALLENGE_BODY, "text/html")
                    return
                if original.endswith("captcha-challenge-body"):
                    self._send(200, _CAPTCHA_CHALLENGE_BODY, "text/html")
                    return
                if original.endswith("captcha-article"):
                    self._send(200, _CAPTCHA_ARTICLE_BODY, "text/html")
                    return
                if original.endswith("rate-limited-body"):
                    self._send(429, b"<html><title>archive.ph rate limited</title></html>", "text/html")
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
            "timemap_base_url": f"{base}/timemap",
            "hosts": frozenset({f"127.0.0.1:{port}"}),
        }
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def _fetch(server: dict[str, object], *, url: str, cutoff: str | None, max_attempts: int = 4):
    return fetch_archive_today_capture(
        original_url=url,
        cutoff_timestamp=cutoff,
        timemap_base_url=server["timemap_base_url"],  # type: ignore[arg-type]
        archive_today_hosts=server["hosts"],  # type: ignore[arg-type]
        timeout_seconds=5,
        max_bytes=65536,
        max_attempts=max_attempts,
    )


# --------------------------------------------------------------------------------------------------
# End-to-end (fake server)
# --------------------------------------------------------------------------------------------------


def test_selects_latest_pre_cutoff_memento_with_verified_body(archive_today_server) -> None:
    result = _fetch(archive_today_server, url="https://example.com/with-body", cutoff="20240601000000")
    assert isinstance(result, ArchiveTodayCaptureSuccess)
    assert result.selected_memento is not None
    assert result.selected_memento.timestamp == "20240101000000"  # latest <= cutoff, not the 2023 one
    assert isinstance(result.body_result, DirectHttpCaptureSuccess)
    assert result.body_result.body == _ARCHIVED_BODY
    assert result.body_verification is not None and result.body_verification.ok
    assert result.body_verification.served_timestamp == "20240101000000"
    assert result.gate_defeat_stop is None


def test_no_pre_cutoff_memento_is_honest_no_go(archive_today_server) -> None:
    result = _fetch(archive_today_server, url="https://example.com/no-memento", cutoff="20240601000000")
    assert isinstance(result, ArchiveTodayCaptureSuccess)
    assert result.mementos  # a memento exists, it is just post-cutoff
    assert result.selected_memento is None  # NO-GO: none <= cutoff
    assert result.body_result is None
    assert result.body_verification is None


def test_served_time_leak_redirect_is_flagged_not_silently_passed(archive_today_server) -> None:
    result = _fetch(archive_today_server, url="https://example.com/served-leak", cutoff="20240601000000")
    assert isinstance(result, ArchiveTodayCaptureSuccess)
    assert result.selected_memento is not None
    assert result.selected_memento.timestamp == "20240101000000"  # selected pre-cutoff
    assert result.body_verification is not None
    assert not result.body_verification.ok
    assert "served_time_leak" in (result.body_verification.reason or "")
    assert result.body_verification.served_timestamp == "20250101000000"  # the leaked served capture


def test_challenge_on_timemap_stops_at_gate_defeat_line(archive_today_server) -> None:
    result = _fetch(archive_today_server, url="https://example.com/challenge-timemap", cutoff="20240601000000")
    assert isinstance(result, ArchiveTodayCaptureFailure)
    assert result.gate_defeat_stop is not None
    assert "challenge_detected" in result.gate_defeat_stop
    assert any("gate_defeat_stop" in note for note in result.limitation_notes)


def test_challenge_on_body_stops_and_does_not_preserve_body(archive_today_server) -> None:
    result = _fetch(archive_today_server, url="https://example.com/challenge-body", cutoff="20240601000000")
    assert isinstance(result, ArchiveTodayCaptureSuccess)
    assert result.selected_memento is not None
    assert result.gate_defeat_stop is not None
    assert "challenge_detected" in result.gate_defeat_stop
    assert result.body_result is None  # a challenge body is not preserved or trusted
    assert result.body_verification is None


def test_captcha_challenge_context_stops_and_does_not_preserve_body(archive_today_server) -> None:
    result = _fetch(
        archive_today_server, url="https://example.com/captcha-challenge-body", cutoff="20240601000000"
    )
    assert isinstance(result, ArchiveTodayCaptureSuccess)
    assert result.gate_defeat_stop is not None
    assert "challenge_detected" in result.gate_defeat_stop
    assert result.body_result is None
    assert result.body_verification is None


def test_plain_captcha_text_in_archived_body_is_not_gate_defeat(archive_today_server) -> None:
    result = _fetch(archive_today_server, url="https://example.com/captcha-article", cutoff="20240601000000")
    assert isinstance(result, ArchiveTodayCaptureSuccess)
    assert result.gate_defeat_stop is None
    assert isinstance(result.body_result, DirectHttpCaptureSuccess)
    assert result.body_result.body == _CAPTCHA_ARTICLE_BODY
    assert result.body_verification is not None and result.body_verification.ok


def test_persistent_rate_limit_body_is_partial_not_verified_body(archive_today_server) -> None:
    result = _fetch(
        archive_today_server, url="https://example.com/rate-limited-body", cutoff="20240601000000", max_attempts=1
    )
    assert isinstance(result, ArchiveTodayCaptureSuccess)
    assert result.gate_defeat_stop is None
    assert isinstance(result.body_result, DirectHttpCaptureSuccess)
    assert result.body_result.status == 429
    assert result.body_verification is not None
    assert not result.body_verification.ok
    assert "body_http_status_not_usable" in (result.body_verification.reason or "")


def test_persistent_rate_limit_timemap_is_access_failed_not_challenge(archive_today_server) -> None:
    result = _fetch(
        archive_today_server, url="https://example.com/rate-limited", cutoff="20240601000000", max_attempts=1
    )
    assert isinstance(result, ArchiveTodayCaptureFailure)
    assert result.gate_defeat_stop is None  # 429 rate limit is NOT a gate defeat
    assert any("access_failed" in note and "429" in note for note in result.limitation_notes)


def test_timemap_transport_failure_is_capture_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_fetch(*, url: str, timeout_seconds: float, max_bytes: int):
        return DirectHttpCaptureFailure(
            requested_url=url,
            failure_kind=DirectHttpCaptureFailureKind.NETWORK_ERROR,
            message="boom",
        )

    monkeypatch.setattr(archive_today, "fetch_direct_http_capture", fake_fetch)
    result = fetch_archive_today_capture(
        original_url="https://example.com/x", cutoff_timestamp="20240601000000", max_attempts=1
    )
    assert isinstance(result, ArchiveTodayCaptureFailure)
    assert isinstance(result.timemap_result, DirectHttpCaptureFailure)
    assert any("access_failed" in note for note in result.limitation_notes)


def test_fetch_with_retry_recovers_after_transient_rate_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []
    calls = {"n": 0}

    def fake_fetch(*, url: str, timeout_seconds: float, max_bytes: int):
        calls["n"] += 1
        if calls["n"] < 3:
            return DirectHttpCaptureFailure(
                requested_url=url,
                failure_kind=DirectHttpCaptureFailureKind.NO_BODY,
                message="HTTP 429 empty body",
                status=429,
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

    monkeypatch.setattr(archive_today, "fetch_direct_http_capture", fake_fetch)
    monkeypatch.setattr(archive_today.time, "sleep", lambda seconds: sleeps.append(seconds))

    result = archive_today._fetch_with_retry(
        url="https://archive.ph/timemap/https://example.com/",
        timeout_seconds=5,
        max_bytes=1024,
        max_attempts=4,
        retry_backoff_seconds=2.0,
    )
    assert isinstance(result, DirectHttpCaptureSuccess)
    assert calls["n"] == 3
    assert sleeps == [2.0, 4.0]


def test_fetch_with_retry_recovers_after_transient_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    # A read-phase timeout (surfaced by direct_http as a TIMEOUT failure, not a crash) is transient:
    # the retry wrapper backs off and recovers instead of failing the rung on a momentarily slow
    # archive.today TimeMap/memento fetch.
    sleeps: list[float] = []
    calls = {"n": 0}

    def fake_fetch(*, url: str, timeout_seconds: float, max_bytes: int):
        calls["n"] += 1
        if calls["n"] < 3:
            return DirectHttpCaptureFailure(
                requested_url=url,
                failure_kind=DirectHttpCaptureFailureKind.TIMEOUT,
                message="Direct HTTP request timed out during response read",
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

    monkeypatch.setattr(archive_today, "fetch_direct_http_capture", fake_fetch)
    monkeypatch.setattr(archive_today.time, "sleep", lambda seconds: sleeps.append(seconds))

    result = archive_today._fetch_with_retry(
        url="https://archive.ph/timemap/https://example.com/",
        timeout_seconds=5,
        max_bytes=1024,
        max_attempts=4,
        retry_backoff_seconds=2.0,
    )
    assert isinstance(result, DirectHttpCaptureSuccess)
    assert calls["n"] == 3  # two timeout retries, then success
    assert sleeps == [2.0, 4.0]


# --------------------------------------------------------------------------------------------------
# parse_timemap_mementos
# --------------------------------------------------------------------------------------------------


def test_parse_timemap_keeps_mementos_skips_original_and_timegate_and_foreign_host() -> None:
    body = (
        b'<https://example.com/>; rel="original",\n'
        b'<http://archive.md/timegate/https://example.com/>; rel="timegate",\n'
        b'<http://archive.md/19941231150000/https://example.com/>; rel="first memento"; '
        b'datetime="Sat, 31 Dec 1994 15:00:00 GMT",\n'
        b'<http://archive.md/20240101000000/https://example.com/>; rel="memento"; '
        b'datetime="Mon, 01 Jan 2024 00:00:00 GMT",\n'
        b'<http://evil.example.net/20240101000000/https://example.com/>; rel="memento"\n'
    )
    mementos = parse_timemap_mementos(body, requested_original_url="https://example.com/")
    # original + timegate skipped; the foreign-host memento skipped; two archive.md mementos kept.
    assert [m.timestamp for m in mementos] == ["19941231150000", "20240101000000"]
    assert mementos[1].datetime_header == "Mon, 01 Jan 2024 00:00:00 GMT"  # comma-in-datetime parsed
    assert all(m.original_url == "https://example.com/" for m in mementos)


def test_select_memento_picks_latest_pre_cutoff() -> None:
    body = (
        b'<http://archive.md/20230101000000/https://example.com/>; rel="memento",\n'
        b'<http://archive.md/20240101000000/https://example.com/>; rel="memento",\n'
        b'<http://archive.md/20250101000000/https://example.com/>; rel="memento"\n'
    )
    mementos = parse_timemap_mementos(body, requested_original_url="https://example.com/")
    selected = select_memento(mementos, cutoff_timestamp="20240601000000")
    assert selected is not None and selected.timestamp == "20240101000000"
    assert select_memento(mementos, cutoff_timestamp="20220101000000") is None  # all post-cutoff
    assert select_memento(mementos, cutoff_timestamp=None).timestamp == "20250101000000"  # newest


# --------------------------------------------------------------------------------------------------
# verify_archive_today_body (direct unit -- off-host / identity / unparseable cannot use a real
# redirect to a foreign host without hitting the network)
# --------------------------------------------------------------------------------------------------


def _body(final_url: str) -> DirectHttpCaptureSuccess:
    return DirectHttpCaptureSuccess(
        requested_url=final_url,
        final_url=final_url,
        status=200,
        reason="OK",
        metadata={},
        body=b"<html>x</html>",
        warning_notes=[],
        limitation_notes=[],
    )


def test_verify_passes_clean_pre_cutoff_family_body() -> None:
    verdict = verify_archive_today_body(
        body_result=_body("https://archive.md/20240101000000/https://example.com/page"),
        requested_original_url="https://example.com/page",
        cutoff_timestamp="20240601000000",
    )
    assert verdict is not None and verdict.ok and verdict.served_timestamp == "20240101000000"


def test_verify_flags_off_family_host() -> None:
    verdict = verify_archive_today_body(
        body_result=_body("https://evil.example.net/20240101000000/https://example.com/page"),
        requested_original_url="https://example.com/page",
        cutoff_timestamp="20240601000000",
    )
    assert verdict is not None and not verdict.ok
    assert "served_off_archive_host" in (verdict.reason or "")


def test_verify_flags_identity_mismatch() -> None:
    verdict = verify_archive_today_body(
        body_result=_body("https://archive.md/20240101000000/https://example.com/OTHER"),
        requested_original_url="https://example.com/page",
        cutoff_timestamp="20240601000000",
    )
    assert verdict is not None and not verdict.ok
    assert "served_url_identity_mismatch" in (verdict.reason or "")


def test_verify_flags_served_time_leak() -> None:
    verdict = verify_archive_today_body(
        body_result=_body("https://archive.md/20250101000000/https://example.com/page"),
        requested_original_url="https://example.com/page",
        cutoff_timestamp="20240601000000",
    )
    assert verdict is not None and not verdict.ok
    assert "served_time_leak" in (verdict.reason or "")


def test_verify_unparseable_served_time_with_cutoff_is_failure() -> None:
    # A short canonical archive.today URL (family host, no 14-digit path) cannot prove served time.
    verdict = verify_archive_today_body(
        body_result=_body("https://archive.ph/abc12"),
        requested_original_url="https://example.com/page",
        cutoff_timestamp="20240601000000",
    )
    assert verdict is not None and not verdict.ok
    assert "served_time_unverifiable" in (verdict.reason or "")


def test_verify_unparseable_served_time_without_cutoff_passes_on_family_host() -> None:
    verdict = verify_archive_today_body(
        body_result=_body("https://archive.ph/abc12"),
        requested_original_url="https://example.com/page",
        cutoff_timestamp=None,
    )
    assert verdict is not None and verdict.ok and verdict.served_timestamp is None


def test_verify_returns_none_for_non_success_body() -> None:
    assert (
        verify_archive_today_body(
            body_result=DirectHttpCaptureFailure(
                requested_url="https://archive.md/x",
                failure_kind=DirectHttpCaptureFailureKind.NO_BODY,
                message="empty",
            ),
            requested_original_url="https://example.com/page",
            cutoff_timestamp="20240601000000",
        )
        is None
    )
