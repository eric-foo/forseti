"""Probe local CDP endpoints before declaring a controllable browser unavailable.

Probe-and-report only: this module never attaches, navigates, captures, or
mutates browser state. It exists because a prior TikTok scan lane declared
"no controllable browser session" while a CloakBrowser CDP endpoint was
listening on 127.0.0.1:9223 -- an unavailability claim must now be backed by
a probe report naming the endpoints actually checked.

Local-only posture mirrors the LinkedIn lane's CDP attach rules: loopback
hosts only, no embedded credentials, no remote relays.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any, Callable, Sequence

DEFAULT_CDP_PROBE_PORTS: tuple[int, ...] = (9222, 9223)
_LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})
_DEFAULT_TIMEOUT_SECONDS = 2.0


def probe_local_cdp_endpoints(
    ports: Sequence[int] = DEFAULT_CDP_PROBE_PORTS,
    *,
    host: str = "127.0.0.1",
    timeout_seconds: float = _DEFAULT_TIMEOUT_SECONDS,
    opener: Callable[[str, float], str] | None = None,
) -> dict[str, Any]:
    """Return a probe report over ``http://<host>:<port>/json/version`` checks.

    ``opener`` is injectable for tests: it receives (url, timeout_seconds) and
    returns the response body text, raising on failure. The report is data,
    not authorization: a live endpoint proves reachability only.
    """
    if host not in _LOCAL_HOSTS:
        raise ValueError(
            f"probe host must be local ({sorted(_LOCAL_HOSTS)}); refusing {host!r}"
        )
    if not ports:
        raise ValueError("probe requires at least one port")
    for port in ports:
        if not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535:
            raise ValueError(f"probe port must be an integer in 1..65535; got {port!r}")
    if not isinstance(timeout_seconds, (int, float)) or isinstance(timeout_seconds, bool) or timeout_seconds <= 0:
        raise ValueError(f"probe timeout_seconds must be positive; got {timeout_seconds!r}")
    # IPv6 literals need brackets in URLs (http://[::1]:9223).
    host_for_url = f"[{host}]" if ":" in host else host
    read = opener or _http_get
    probed: list[dict[str, Any]] = []
    live_endpoints: list[str] = []
    for port in ports:
        endpoint = f"http://{host_for_url}:{int(port)}"
        url = f"{endpoint}/json/version"
        entry: dict[str, Any] = {
            "endpoint": endpoint,
            "live": False,
            "browser_or_none": None,
            "error_or_none": None,
        }
        try:
            body = read(url, timeout_seconds)
            entry["live"] = True
            try:
                version = json.loads(body)
                if isinstance(version, dict):
                    browser = version.get("Browser")
                    if isinstance(browser, str) and browser.strip():
                        entry["browser_or_none"] = browser
            except ValueError:
                pass  # live but non-JSON body: reachability stands, identity unknown
            live_endpoints.append(endpoint)
        except Exception as exc:  # noqa: BLE001 - each endpoint reports its own failure
            entry["error_or_none"] = f"{type(exc).__name__}: {exc}"
        probed.append(entry)
    return {
        "probe_kind": "local_cdp_endpoint_probe",
        "host": host,
        "ports_checked": [int(port) for port in ports],
        "probed": probed,
        "live_endpoints": live_endpoints,
        "browser_available": bool(live_endpoints),
    }


def _http_get(url: str, timeout_seconds: float) -> str:
    request = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310 - loopback-only by construction
        return response.read().decode("utf-8", errors="replace")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Probe local CDP endpoints and print a JSON probe report. Report-only: "
            "never attaches to or mutates a browser."
        )
    )
    parser.add_argument(
        "--port",
        action="append",
        type=int,
        dest="ports",
        help=f"Port to probe on 127.0.0.1. Repeatable. Defaults to {DEFAULT_CDP_PROBE_PORTS}.",
    )
    parser.add_argument("--timeout-seconds", type=float, default=_DEFAULT_TIMEOUT_SECONDS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    report = probe_local_cdp_endpoints(
        tuple(args.ports) if args.ports else DEFAULT_CDP_PROBE_PORTS,
        timeout_seconds=args.timeout_seconds,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
