from __future__ import annotations

import json

import pytest

from source_capture.adapters.browser_session_probe import (
    DEFAULT_CDP_PROBE_PORTS,
    probe_local_cdp_endpoints,
)


def test_probe_reports_live_endpoint_with_browser_identity() -> None:
    def opener(url: str, timeout: float) -> str:
        assert url == "http://127.0.0.1:9223/json/version"
        return json.dumps({"Browser": "Chrome/126.0.0.0"})

    report = probe_local_cdp_endpoints((9223,), opener=opener)
    assert report["probe_kind"] == "local_cdp_endpoint_probe"
    assert report["browser_available"] is True
    assert report["live_endpoints"] == ["http://127.0.0.1:9223"]
    assert report["probed"][0]["live"] is True
    assert report["probed"][0]["browser_or_none"] == "Chrome/126.0.0.0"
    assert report["probed"][0]["error_or_none"] is None


def test_probe_reports_dead_endpoints_without_raising() -> None:
    def opener(url: str, timeout: float) -> str:
        raise OSError("connection refused")

    report = probe_local_cdp_endpoints((9222, 9223), opener=opener)
    assert report["browser_available"] is False
    assert report["live_endpoints"] == []
    assert report["ports_checked"] == [9222, 9223]
    for entry in report["probed"]:
        assert entry["live"] is False
        assert "connection refused" in entry["error_or_none"]


def test_probe_mixed_live_and_dead_endpoints() -> None:
    def opener(url: str, timeout: float) -> str:
        if ":9223/" in url:
            return "not-json"
        raise OSError("refused")

    report = probe_local_cdp_endpoints((9222, 9223), opener=opener)
    assert report["browser_available"] is True
    assert report["live_endpoints"] == ["http://127.0.0.1:9223"]
    live_entry = report["probed"][1]
    assert live_entry["live"] is True
    assert live_entry["browser_or_none"] is None  # reachable, identity unknown


def test_probe_rejects_non_local_host() -> None:
    with pytest.raises(ValueError):
        probe_local_cdp_endpoints((9222,), host="example.com")


def test_probe_requires_at_least_one_port() -> None:
    with pytest.raises(ValueError):
        probe_local_cdp_endpoints(())


def test_probe_rejects_out_of_range_or_non_int_ports() -> None:
    for bad_port in (0, 70000, -1, True, "9222"):
        with pytest.raises(ValueError):
            probe_local_cdp_endpoints((bad_port,), opener=lambda url, timeout: "{}")


def test_probe_rejects_non_positive_timeout() -> None:
    for bad_timeout in (0, -2.5, True):
        with pytest.raises(ValueError):
            probe_local_cdp_endpoints((9222,), timeout_seconds=bad_timeout, opener=lambda url, timeout: "{}")


def test_probe_brackets_ipv6_host_in_endpoint() -> None:
    seen: list[str] = []

    def opener(url: str, timeout: float) -> str:
        seen.append(url)
        return "{}"

    report = probe_local_cdp_endpoints((9223,), host="::1", opener=opener)
    assert seen == ["http://[::1]:9223/json/version"]
    assert report["live_endpoints"] == ["http://[::1]:9223"]


def test_default_ports_cover_the_cloakbrowser_endpoint() -> None:
    assert 9223 in DEFAULT_CDP_PROBE_PORTS
