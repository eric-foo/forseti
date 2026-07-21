"""Ulta-owned public PowerReviews display configuration and transport.

PowerReviews mechanics here are Ulta-specific: the configuration is the
page-declared ``POWERREVIEWS.display.render({...})`` block inside the
``PowerReviewsRender`` script of an admitted rendered Ulta PDP packet, and the
read route is the public ``display.powerreviews.com`` display API that block
drives. Nothing in this module is Bazaarvoice, and nothing is claimed portable
to another PowerReviews retailer until that retailer proves identical public
mechanics.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import ProxyHandler, Request, build_opener

from harness_utils import utc_now_z


POWERREVIEWS_DISPLAY_HOST = "display.powerreviews.com"
# The display route silently returns zero rows above this page size; the cap is
# an observed route boundary, not a preference.
POWERREVIEWS_DISPLAY_PAGE_SIZE_MAX = 25
_API_USER_AGENT = "ForsetiUltaPowerReviewsCapture/1.0 (raw-preserving structured read)"
_NO_PROXY_OPENER = build_opener(ProxyHandler({}))

_RENDER_SCRIPT = re.compile(
    r"""<script\b(?=[^>]*\bid\s*=\s*(?P<quote>["'])PowerReviewsRender(?P=quote))[^>]*>(?P<body>.*?)</script\s*>""",
    re.IGNORECASE | re.DOTALL,
)
_RENDER_BLOCK = re.compile(
    r"POWERREVIEWS\.display\.render\(\{(?P<body>.*?)\}\)",
    re.DOTALL,
)
_API_KEY = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)
_LOCALE = re.compile(r"^[a-z]{2}_[A-Z]{2}$")


class UltaPowerReviewsConfigError(RuntimeError):
    """Fail-closed, credential-safe page-declared configuration failure."""


class UltaPowerReviewsApiCaptureError(RuntimeError):
    """Secret-safe structured acquisition failure."""


@dataclass(frozen=True)
class PowerReviewsReadConfig:
    host: str
    merchant_id: str
    merchant_group_id: str
    page_id: str
    locale: str
    api_key: str


@dataclass(frozen=True)
class PowerReviewsRequestSpec:
    artifact_name: str
    resource: str
    parameters: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class PowerReviewsResponse:
    status: int
    reason: str
    body: bytes
    content_type: str | None
    captured_at: str


PowerReviewsFetcher = Callable[
    [PowerReviewsRequestSpec, PowerReviewsReadConfig, float, int],
    PowerReviewsResponse,
]


def resolve_ulta_powerreviews_config(dom_text: str) -> PowerReviewsReadConfig:
    """Resolve the page-declared public display configuration without persisting it.

    The api key is a page-declared public display credential; it is returned
    for in-flight use only and must never be written into manifests, summaries,
    or error text.
    """
    scripts = [match.group("body") for match in _RENDER_SCRIPT.finditer(dom_text)]
    if len(scripts) != 1:
        raise UltaPowerReviewsConfigError(
            "Ulta parent DOM must declare exactly one script#PowerReviewsRender"
        )
    blocks = _RENDER_BLOCK.findall(scripts[0])
    if len(blocks) != 1:
        raise UltaPowerReviewsConfigError(
            "script#PowerReviewsRender must contain exactly one "
            "POWERREVIEWS.display.render configuration block"
        )
    body = blocks[0]
    api_key = _declared_value(body, "api_key")
    merchant_id = _declared_value(body, "merchant_id")
    merchant_group_id = _declared_value(body, "merchant_group_id")
    page_id = _declared_value(body, "page_id")
    locale = _declared_value(body, "locale")
    if _API_KEY.fullmatch(api_key) is None:
        raise UltaPowerReviewsConfigError(
            "Ulta page-declared public display key has an invalid shape"
        )
    if not merchant_id.isdigit() or not merchant_group_id.isdigit():
        raise UltaPowerReviewsConfigError(
            "Ulta page-declared merchant identifiers must be numeric"
        )
    if _LOCALE.fullmatch(locale) is None:
        raise UltaPowerReviewsConfigError(
            "Ulta page-declared PowerReviews locale has an invalid shape"
        )
    if not page_id:
        raise UltaPowerReviewsConfigError(
            "Ulta page-declared PowerReviews page_id is empty"
        )
    return PowerReviewsReadConfig(
        host=POWERREVIEWS_DISPLAY_HOST,
        merchant_id=merchant_id,
        merchant_group_id=merchant_group_id,
        page_id=page_id,
        locale=locale,
        api_key=api_key,
    )


def fetch_powerreviews_display_response(
    spec: PowerReviewsRequestSpec,
    config: PowerReviewsReadConfig,
    timeout_seconds: float,
    max_bytes: int,
) -> PowerReviewsResponse:
    if spec.resource not in {"reviews", "questions"}:
        raise UltaPowerReviewsApiCaptureError(
            f"{spec.artifact_name} requests an unsupported display resource"
        )
    query = urlencode(
        (("apikey", config.api_key), *spec.parameters),
        doseq=True,
    )
    url = (
        f"https://{config.host}/m/{config.merchant_id}/l/{config.locale}"
        f"/product/{config.page_id}/{spec.resource}?{query}"
    )
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
        raise UltaPowerReviewsApiCaptureError(
            f"{spec.artifact_name} network read failed"
        ) from exc
    with response:
        content_length = _optional_header_int(response.headers.get("Content-Length"))
        if content_length is not None and content_length > max_bytes:
            raise UltaPowerReviewsApiCaptureError(
                f"{spec.artifact_name} exceeds max_bytes before read"
            )
        body = response.read(max_bytes + 1)
        if len(body) > max_bytes:
            raise UltaPowerReviewsApiCaptureError(
                f"{spec.artifact_name} exceeds max_bytes during read"
            )
        if not body:
            raise UltaPowerReviewsApiCaptureError(
                f"{spec.artifact_name} returned an empty body"
            )
        return PowerReviewsResponse(
            status=int(response.getcode()),
            reason=str(getattr(response, "reason", "") or ""),
            body=body,
            content_type=response.headers.get("Content-Type"),
            captured_at=utc_now_z(),
        )


def _declared_value(body: str, name: str) -> str:
    values = set(re.findall(rf"{name}:\s*'([^']*)'", body))
    if len(values) != 1:
        raise UltaPowerReviewsConfigError(
            f"Ulta render configuration must declare exactly one {name}"
        )
    return next(iter(values))


def _optional_header_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


__all__ = [
    "POWERREVIEWS_DISPLAY_HOST",
    "POWERREVIEWS_DISPLAY_PAGE_SIZE_MAX",
    "PowerReviewsFetcher",
    "PowerReviewsReadConfig",
    "PowerReviewsRequestSpec",
    "PowerReviewsResponse",
    "UltaPowerReviewsApiCaptureError",
    "UltaPowerReviewsConfigError",
    "fetch_powerreviews_display_response",
    "resolve_ulta_powerreviews_config",
]
