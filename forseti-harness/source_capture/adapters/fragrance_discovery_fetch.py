"""Network transport for fragrance review discovery (adapter layer).

Isolated here so ``source_capture/fragrance_review_discovery.py`` stays free of
runtime acquisition imports (the source-capture no-runtime-imports contract scans
the top-level package, not ``adapters/``). stdlib ``urllib`` only; verified TLS,
with certifi's CA bundle when available (never weakened).
"""
from __future__ import annotations

import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass


def _build_ssl_context() -> ssl.SSLContext:
    # Verified TLS. Prefer certifi's complete CA bundle when importable so hosts
    # with extra intermediate certs still validate; otherwise the env trust store.
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:  # noqa: BLE001 - certifi optional; default context is still verified
        return ssl.create_default_context()


_SSL_CONTEXT = _build_ssl_context()
_USER_AGENT = "Mozilla/5.0 (compatible; OrcaSourceCapture/0.1)"


@dataclass
class DiscoveryFetchResult:
    url: str
    status: int
    ok: bool
    text: str
    error: str | None = None


def fetch_discovery_url(
    url: str,
    *,
    accept: str = "application/json",
    timeout_seconds: float = 30.0,
    max_response_bytes: int = 5_000_000,
) -> DiscoveryFetchResult:
    request = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds, context=_SSL_CONTEXT) as response:
            raw = response.read(max_response_bytes + 1)
            status = int(response.getcode())
            if len(raw) > max_response_bytes:
                return DiscoveryFetchResult(url, status, False, "", f"response_body_exceeded_cap:{len(raw)}")
            charset = response.headers.get_content_charset() if response.headers else None
            return DiscoveryFetchResult(url, status, 200 <= status < 400, raw.decode(charset or "utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        return DiscoveryFetchResult(url, int(exc.code), False, "", f"http_error:{exc.code}")
    except Exception as exc:  # noqa: BLE001 - report transport failure to the caller, do not raise
        return DiscoveryFetchResult(url, 0, False, "", f"{type(exc).__name__}:{exc}")


__all__ = ["DiscoveryFetchResult", "fetch_discovery_url"]
