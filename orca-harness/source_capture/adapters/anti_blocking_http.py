from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from http.client import HTTPResponse
from typing import TypeAlias
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from harness_utils import utc_now_z


DEFAULT_TIMEOUT_SECONDS = 20.0
DEFAULT_MAX_BYTES = 5_000_000

ANTI_BLOCKING_HTTP_METHOD_CATEGORY = "anti_blocking_http"
DEFAULT_IMPERSONATION_PROFILE = "header_complete_stdlib"

_DEFAULT_CHROME_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


class AntiBlockingHttpCaptureFailureKind(StrEnum):
    NETWORK_ERROR = "network_error"
    TIMEOUT = "timeout"
    NO_BODY = "no_body"
    SIZE_CAP_EXCEEDED = "size_cap_exceeded"


@dataclass(frozen=True)
class AntiBlockingHttpCaptureSuccess:
    requested_url: str
    final_url: str
    status: int
    reason: str
    impersonation_profile: str
    method_category: str
    response_headers: dict[str, str]
    metadata: dict[str, object]
    body: bytes
    warning_notes: list[str]
    limitation_notes: list[str]


@dataclass(frozen=True)
class AntiBlockingHttpCaptureFailure:
    requested_url: str
    failure_kind: AntiBlockingHttpCaptureFailureKind
    message: str
    impersonation_profile: str
    final_url: str | None = None
    status: int | None = None
    reason: str | None = None


AntiBlockingHttpCaptureResult: TypeAlias = (
    AntiBlockingHttpCaptureSuccess | AntiBlockingHttpCaptureFailure
)


def header_complete_profile(user_agent: str = _DEFAULT_CHROME_USER_AGENT) -> dict[str, str]:
    """Full desktop-Chrome request header set for the ``header_complete_stdlib`` rung.

    ``Accept-Encoding: identity`` is deliberate: stdlib ``urllib`` does not
    transparently decompress ``gzip``/``br`` responses, so requesting an
    uncompressed body keeps the preserved bytes byte-identical to what the server
    served (hash-honest). Negotiating compression is a rung-2 (``curl_cffi``)
    concern, not this rung's.
    """
    return {
        "User-Agent": user_agent,
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,image/apng,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "identity",
        "Upgrade-Insecure-Requests": "1",
        "Sec-CH-UA": '"Chromium";v="126", "Google Chrome";v="126", "Not.A/Brand";v="24"',
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }


def fetch_anti_blocking_http_capture(
    *,
    url: str,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = DEFAULT_MAX_BYTES,
    user_agent: str = _DEFAULT_CHROME_USER_AGENT,
) -> AntiBlockingHttpCaptureResult:
    """Header/UA-complete stdlib HTTP fetch (rung-1 anti-blocking).

    Anti-blocking method category, distinct from the honest ``direct_http``
    baseline: it sends a full desktop-Chrome header profile to get past naive
    User-Agent / header sniffing. It does NOT impersonate the TLS/JA3 fingerprint
    (stdlib ``urllib`` carries Python's TLS signature) -- that is rung-2.

    The body is preserved verbatim; this adapter makes no claim that a returned
    body is real source content (a server may return a 200 challenge/block shell).
    Body-honesty classification belongs to the runner via ``block_shell``.
    """
    profile = DEFAULT_IMPERSONATION_PROFILE
    normalized_url = _validate_http_url(url)
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than zero")
    if max_bytes <= 0:
        raise ValueError("max_bytes must be greater than zero")

    request = Request(normalized_url, headers=header_complete_profile(user_agent), method="GET")

    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            return _capture_response(
                requested_url=normalized_url,
                response=response,
                timeout_seconds=timeout_seconds,
                max_bytes=max_bytes,
                impersonation_profile=profile,
            )
    except HTTPError as exc:
        return _capture_response(
            requested_url=normalized_url,
            response=exc,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
            impersonation_profile=profile,
        )
    except URLError as exc:
        return AntiBlockingHttpCaptureFailure(
            requested_url=normalized_url,
            failure_kind=_failure_kind_from_url_error(exc),
            message=f"anti_blocking_http request failed: {exc.reason}",
            impersonation_profile=profile,
        )


def _capture_response(
    *,
    requested_url: str,
    response: HTTPResponse | HTTPError,
    timeout_seconds: float,
    max_bytes: int,
    impersonation_profile: str,
) -> AntiBlockingHttpCaptureResult:
    status = int(response.getcode())
    reason = str(getattr(response, "reason", "") or "")
    final_url = response.geturl()
    headers = response.headers

    content_length = _parse_optional_int(headers.get("Content-Length"))
    if content_length is not None and content_length > max_bytes:
        return AntiBlockingHttpCaptureFailure(
            requested_url=requested_url,
            final_url=final_url,
            status=status,
            reason=reason,
            failure_kind=AntiBlockingHttpCaptureFailureKind.SIZE_CAP_EXCEEDED,
            message=(
                "anti_blocking_http response exceeded max-bytes cap before body read: "
                f"{content_length} bytes > {max_bytes} bytes"
            ),
            impersonation_profile=impersonation_profile,
        )

    try:
        body = _read_with_cap(response, max_bytes=max_bytes)
    except _BodyTooLargeError as exc:
        return AntiBlockingHttpCaptureFailure(
            requested_url=requested_url,
            final_url=final_url,
            status=status,
            reason=reason,
            failure_kind=AntiBlockingHttpCaptureFailureKind.SIZE_CAP_EXCEEDED,
            message=str(exc),
            impersonation_profile=impersonation_profile,
        )

    warning_notes: list[str] = []
    if final_url != requested_url:
        warning_notes.append(
            f"anti_blocking_http followed redirect from {requested_url} to {final_url}"
        )

    limitation_notes: list[str] = []
    content_encoding = headers.get("Content-Encoding")
    if content_encoding and content_encoding.strip().lower() not in {"identity", "none"}:
        limitation_notes.append(
            "encoded_response_body: anti_blocking_http requested identity encoding but "
            f"server returned Content-Encoding {content_encoding}; preserved bytes are as served "
            "and body classification cannot certify decoded source content"
        )

    response_headers = {str(key): str(value) for key, value in headers.items()}
    metadata: dict[str, object] = {
        "requested_url": requested_url,
        "final_url": final_url,
        "status": status,
        "reason": reason or None,
        "method_category": ANTI_BLOCKING_HTTP_METHOD_CATEGORY,
        "impersonation_profile": impersonation_profile,
        "content_type": headers.get("Content-Type"),
        "content_length": content_length,
        "content_encoding": headers.get("Content-Encoding"),
        "date": headers.get("Date"),
        "last_modified": headers.get("Last-Modified"),
        "etag": headers.get("ETag"),
        "response_headers": response_headers,
        "capture_timestamp": utc_now_z(),
        "timeout_seconds": timeout_seconds,
        "byte_count": len(body),
    }

    return AntiBlockingHttpCaptureSuccess(
        requested_url=requested_url,
        final_url=final_url,
        status=status,
        reason=reason,
        impersonation_profile=impersonation_profile,
        method_category=ANTI_BLOCKING_HTTP_METHOD_CATEGORY,
        response_headers=response_headers,
        metadata=metadata,
        body=body,
        warning_notes=warning_notes,
        limitation_notes=limitation_notes,
    )


def _validate_http_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("anti_blocking_http capture requires an absolute http:// or https:// URL")
    return parsed.geturl()


def _parse_optional_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _read_with_cap(response: HTTPResponse | HTTPError, *, max_bytes: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(min(65536, max_bytes - total + 1))
        if not chunk:
            return b"".join(chunks)
        total += len(chunk)
        if total > max_bytes:
            raise _BodyTooLargeError(
                "anti_blocking_http response exceeded max-bytes cap during body read: "
                f"{total} bytes > {max_bytes} bytes"
            )
        chunks.append(chunk)


def _failure_kind_from_url_error(error: URLError) -> AntiBlockingHttpCaptureFailureKind:
    reason_text = str(error.reason).lower()
    if "timed out" in reason_text or "timeout" in reason_text:
        return AntiBlockingHttpCaptureFailureKind.TIMEOUT
    return AntiBlockingHttpCaptureFailureKind.NETWORK_ERROR


class _BodyTooLargeError(ValueError):
    pass
