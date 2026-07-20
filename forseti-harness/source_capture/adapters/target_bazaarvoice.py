"""Target-owned public Bazaarvoice configuration resolution."""

from __future__ import annotations

import hashlib
import gzip
import re
import zlib
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlparse

from source_capture.adapters.bazaarvoice_api import (
    BAZAARVOICE_API_HOST,
    BazaarvoiceReadConfig,
)
from source_capture.adapters.direct_http import (
    DirectHttpCaptureFailure,
    DirectHttpCaptureResult,
    DirectHttpCaptureSuccess,
    fetch_direct_http_capture,
)


_DEPLOYMENT_HOST = "apps.bazaarvoice.com"
_LEGACY_HOST = "display.ugc.bazaarvoice.com"
_DEPLOYMENT_PATH = (
    "/deployments/targetcom/main_site/production/en_US/bv.js"
)
_LEGACY_PATH = "/static/targetcom/main_site/en_US/bvapi.js"
_PASSKEY = re.compile(r"[A-Za-z0-9_-]{20,100}")


class TargetBazaarvoiceConfigError(RuntimeError):
    """Fail-closed, credential-safe public configuration failure."""


ConfigFetcher = Callable[..., DirectHttpCaptureResult]


@dataclass(frozen=True)
class PublicConfigReceipt:
    endpoint: str
    status: int
    reason: str | None
    content_type: str | None
    byte_count: int
    sha256: str
    captured_at: str | None

    def as_dict(self) -> dict[str, object]:
        return {
            "endpoint": self.endpoint,
            "status": self.status,
            "reason": self.reason,
            "content_type": self.content_type,
            "byte_count": self.byte_count,
            "sha256": self.sha256,
            "captured_at": self.captured_at,
        }


@dataclass(frozen=True)
class TargetBazaarvoiceResolution:
    config: BazaarvoiceReadConfig
    deployment: str
    display_code: str
    deployment_url: str
    legacy_config_url: str
    config_receipts: tuple[PublicConfigReceipt, ...]


def validate_target_deployment_url(url: str) -> str:
    parsed = urlparse(url)
    if (
        parsed.scheme != "https"
        or (parsed.hostname or "").lower() != _DEPLOYMENT_HOST
        or parsed.path != _DEPLOYMENT_PATH
        or parsed.query
        or parsed.fragment
    ):
        raise TargetBazaarvoiceConfigError(
            "Target Bazaarvoice deployment must be the exact public "
            "targetcom/main_site/production/en_US bv.js route"
        )
    return url


def resolve_target_bazaarvoice_config(
    *,
    deployment_url: str,
    timeout_seconds: float,
    max_bytes: int,
    fetcher: ConfigFetcher | None = None,
) -> TargetBazaarvoiceResolution:
    """Resolve Target's public deployment chain without persisting its passkey."""
    validate_target_deployment_url(deployment_url)
    config_fetcher = fetcher or fetch_direct_http_capture
    deployment_response = _fetch_config(
        deployment_url,
        label="Target Bazaarvoice deployment",
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
        fetcher=config_fetcher,
    )
    deployment_text = _decode_config_body(
        deployment_response.body,
        label="Target Bazaarvoice deployment",
    )
    legacy_urls = set(
        re.findall(
            r'legacyScoutUrl\s*:\s*"(https://display\.ugc\.bazaarvoice\.com'
            r'/static/targetcom/main_site/en_US/bvapi\.js)"',
            deployment_text,
        )
    )
    if legacy_urls != {f"https://{_LEGACY_HOST}{_LEGACY_PATH}"}:
        raise TargetBazaarvoiceConfigError(
            "Target Bazaarvoice deployment did not expose exactly one admitted "
            "public legacy configuration route"
        )
    legacy_url = next(iter(legacy_urls))
    legacy_response = _fetch_config(
        legacy_url,
        label="Target Bazaarvoice legacy configuration",
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
        fetcher=config_fetcher,
    )
    legacy_text = _decode_config_body(
        legacy_response.body,
        label="Target Bazaarvoice legacy configuration",
    )
    if 'deploymentId:"targetcom/main_site/PRODUCTION/en_US"' not in legacy_text:
        raise TargetBazaarvoiceConfigError(
            "Target Bazaarvoice legacy configuration deployment identity is absent"
        )

    api_matches = re.findall(
        r'apiconfig:\{[^{}]*?passkey:"([^"]+)"[^{}]*?'
        r'baseUrl:"//api\.bazaarvoice\.com/data/"[^{}]*?'
        r'displaycode:"([^"]+)"',
        legacy_text,
    )
    if len(api_matches) != 1:
        raise TargetBazaarvoiceConfigError(
            "Target Bazaarvoice legacy configuration requires exactly one public "
            "read passkey/display-code tuple"
        )
    passkey, display_code = api_matches[0]
    if _PASSKEY.fullmatch(passkey) is None:
        raise TargetBazaarvoiceConfigError(
            "Target Bazaarvoice public read passkey has an invalid shape"
        )
    if display_code != "19988-en_us":
        raise TargetBazaarvoiceConfigError(
            "Target Bazaarvoice display code is not the admitted 19988-en_us value"
        )

    versions = set(re.findall(r"apiversion=([0-9]+(?:\.[0-9]+)+)", legacy_text))
    if len(versions) != 1:
        raise TargetBazaarvoiceConfigError(
            "Target Bazaarvoice legacy configuration requires one API version"
        )
    version = next(iter(versions))
    receipts = (
        _receipt(deployment_url, deployment_response),
        _receipt(legacy_url, legacy_response),
    )
    return TargetBazaarvoiceResolution(
        config=BazaarvoiceReadConfig(
            host=BAZAARVOICE_API_HOST,
            version=version,
            token=passkey,
        ),
        deployment="targetcom/main_site/production/en_US",
        display_code=display_code,
        deployment_url=deployment_url,
        legacy_config_url=legacy_url,
        config_receipts=receipts,
    )


def _fetch_config(
    url: str,
    *,
    label: str,
    timeout_seconds: float,
    max_bytes: int,
    fetcher: ConfigFetcher,
) -> DirectHttpCaptureSuccess:
    result = fetcher(
        url=url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
    )
    if isinstance(result, DirectHttpCaptureFailure):
        raise TargetBazaarvoiceConfigError(
            f"{label} read failed: {result.failure_kind.value}"
        )
    if not 200 <= result.status < 300:
        raise TargetBazaarvoiceConfigError(
            f"{label} returned HTTP {result.status}"
        )
    if result.final_url != url:
        raise TargetBazaarvoiceConfigError(f"{label} redirected outside its exact route")
    return result


def _receipt(
    endpoint: str,
    response: DirectHttpCaptureSuccess,
) -> PublicConfigReceipt:
    captured_at = response.metadata.get("capture_timestamp")
    return PublicConfigReceipt(
        endpoint=endpoint,
        status=response.status,
        reason=response.reason or None,
        content_type=(
            str(response.metadata["content_type"])
            if response.metadata.get("content_type") is not None
            else None
        ),
        byte_count=len(response.body),
        sha256=hashlib.sha256(response.body).hexdigest(),
        captured_at=str(captured_at) if captured_at is not None else None,
    )


def _decode_config_body(body: bytes, *, label: str) -> str:
    try:
        if body.startswith(b"\x1f\x8b"):
            decoded = gzip.decompress(body)
        elif len(body) >= 2 and body[0] == 0x78:
            decoded = zlib.decompress(body)
        else:
            decoded = body
        return decoded.decode("utf-8", errors="strict")
    except (OSError, UnicodeDecodeError, zlib.error) as exc:
        raise TargetBazaarvoiceConfigError(
            f"{label} could not be decoded as source-delivered JavaScript"
        ) from exc


__all__ = [
    "ConfigFetcher",
    "PublicConfigReceipt",
    "TargetBazaarvoiceConfigError",
    "TargetBazaarvoiceResolution",
    "resolve_target_bazaarvoice_config",
    "validate_target_deployment_url",
]
