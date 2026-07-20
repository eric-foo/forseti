"""Network-only adapter for public, page-declared Bazaarvoice reads."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import ProxyHandler, Request, build_opener

from harness_utils import utc_now_z


BAZAARVOICE_API_HOST = "api.bazaarvoice.com"
_API_USER_AGENT = "ForsetiBazaarvoiceCapture/1.0 (raw-preserving structured read)"
_NO_PROXY_OPENER = build_opener(ProxyHandler({}))


class BazaarvoiceApiCaptureError(RuntimeError):
    """Secret-safe structured acquisition failure."""


@dataclass(frozen=True)
class BazaarvoiceReadConfig:
    host: str
    version: str
    token: str


@dataclass(frozen=True)
class ApiRequestSpec:
    artifact_name: str
    endpoint: str
    config_kind: str
    parameters: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class ApiResponse:
    status: int
    reason: str
    body: bytes
    content_type: str | None
    captured_at: str


ApiFetcher = Callable[
    [ApiRequestSpec, BazaarvoiceReadConfig, float, int],
    ApiResponse,
]


def fetch_bazaarvoice_api_response(
    spec: ApiRequestSpec,
    config: BazaarvoiceReadConfig,
    timeout_seconds: float,
    max_bytes: int,
) -> ApiResponse:
    query = urlencode(
        (("apiversion", config.version), ("passkey", config.token), *spec.parameters),
        doseq=True,
    )
    url = f"https://{config.host}/data/{spec.endpoint}?{query}"
    request = Request(
        url,
        headers={"Accept": "application/json", "User-Agent": _API_USER_AGENT},
        method="GET",
    )
    try:
        response = _NO_PROXY_OPENER.open(request, timeout=timeout_seconds)
    except HTTPError as exc:
        response = exc
    except (URLError, TimeoutError, OSError) as exc:
        raise BazaarvoiceApiCaptureError(
            f"{spec.artifact_name} network read failed"
        ) from exc
    with response:
        content_length = _optional_header_int(response.headers.get("Content-Length"))
        if content_length is not None and content_length > max_bytes:
            raise BazaarvoiceApiCaptureError(
                f"{spec.artifact_name} exceeds max_bytes before read"
            )
        body = response.read(max_bytes + 1)
        if len(body) > max_bytes:
            raise BazaarvoiceApiCaptureError(
                f"{spec.artifact_name} exceeds max_bytes during read"
            )
        if not body:
            raise BazaarvoiceApiCaptureError(
                f"{spec.artifact_name} returned an empty body"
            )
        return ApiResponse(
            status=int(response.getcode()),
            reason=str(getattr(response, "reason", "") or ""),
            body=body,
            content_type=response.headers.get("Content-Type"),
            captured_at=utc_now_z(),
        )


def _optional_header_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


__all__ = [
    "ApiFetcher",
    "ApiRequestSpec",
    "ApiResponse",
    "BAZAARVOICE_API_HOST",
    "BazaarvoiceApiCaptureError",
    "BazaarvoiceReadConfig",
    "fetch_bazaarvoice_api_response",
]
