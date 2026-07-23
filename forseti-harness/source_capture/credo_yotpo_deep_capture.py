"""Provider-bound, no-proxy Yotpo deep review capture for Credo PDPs."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from typing import Callable, Literal, Sequence
from urllib.parse import parse_qs, urlencode, urlparse

from pydantic import Field, model_validator

from schemas.case_models import StrictModel
from source_capture.adapters.browser_snapshot import BrowserPageResponse
from source_capture.credo_brand_grid import load_credo_shopify_init_data
from source_capture.fragrance_rendered_widget_companion import (
    fetch_fragrance_widget_fallback_responses,
)


CREDO_YOTPO_DEEP_VERSION = "credo_yotpo_deep_v1"
_STORE_RE = re.compile(
    r"cdn-widgetsrepository\.yotpo\.com/v1/loader/"
    r"(?P<store_id>[A-Za-z0-9_-]{20,80})\?languageCode=",
    re.IGNORECASE,
)
_PRODUCT_RE = re.compile(
    r'data-yotpo-product-id=["\'](?P<product_id>[0-9]{4,32})["\']',
    re.IGNORECASE,
)
_COUNT_RE = re.compile(
    r"<strong>\s*Overall rating:\s*</strong>\s*"
    r"[0-9.]+\s*/\s*5\s*from\s*(?P<count>[0-9]+)\s+reviews?\.",
    re.IGNORECASE,
)
_PER_PAGE = 10
_MAX_REVIEW_LIMIT = 100
YotpoFetcher = Callable[
    [Sequence[str], float, int], Sequence[BrowserPageResponse]
]


class CredoYotpoBinding(StrictModel):
    source_url: str
    handle: str
    store_id: str
    product_id: str
    declared_review_count: int
    qna_exposed: bool


class CredoYotpoResponseRecord(StrictModel):
    role: Literal["most_relevant", "most_recent"]
    sort: Literal["smart", "date"]
    page: int
    requested_url: str
    final_url: str
    status: int
    body_sha256: str
    body_text: str
    row_count: int
    declared_total: int


class CredoYotpoDeepCaptureReceipt(StrictModel):
    schema_version: Literal["credo_yotpo_deep_v1"] = CREDO_YOTPO_DEEP_VERSION
    source_url: str
    handle: str
    store_id: str
    product_id: str
    transport_posture: Literal["direct_no_proxy", "caller_supplied_unverified"]
    proxy_used: bool | None
    requested_limit_per_role: int
    declared_review_count: int
    most_relevant_review_ids: list[str] = Field(default_factory=list)
    most_recent_review_ids: list[str] = Field(default_factory=list)
    overlap_review_ids: list[str] = Field(default_factory=list)
    qna_posture: Literal["not_exposed", "exposed_not_captured"]
    responses: list[CredoYotpoResponseRecord] = Field(default_factory=list)
    status: Literal["complete", "partial"]
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_status(self) -> "CredoYotpoDeepCaptureReceipt":
        if self.status == "complete" and self.residuals:
            raise ValueError("complete Credo Yotpo receipt cannot carry residuals")
        if self.status == "partial" and not self.residuals:
            raise ValueError("partial Credo Yotpo receipt requires residuals")
        if self.transport_posture == "direct_no_proxy" and self.proxy_used is not False:
            raise ValueError("direct Credo Yotpo transport requires proxy_used=false")
        if self.transport_posture != "direct_no_proxy" and self.proxy_used is not None:
            raise ValueError("unverified Credo Yotpo transport cannot assert proxy usage")
        return self


def parse_credo_yotpo_binding(
    html: str,
    *,
    source_url: str,
) -> CredoYotpoBinding | None:
    parsed = urlparse(source_url)
    match = re.fullmatch(r"/products/(?P<handle>[a-z0-9][a-z0-9-]*)/?", parsed.path)
    if (
        parsed.scheme != "https"
        or (parsed.hostname or "").lower() != "credobeauty.com"
        or match is None
    ):
        raise ValueError("Credo Yotpo binding requires an exact Credo PDP URL")
    store_ids = tuple(dict.fromkeys(item.group("store_id") for item in _STORE_RE.finditer(html)))
    product_ids = tuple(dict.fromkeys(item.group("product_id") for item in _PRODUCT_RE.finditer(html)))
    counts = tuple(dict.fromkeys(int(item.group("count")) for item in _COUNT_RE.finditer(html)))
    if not store_ids and not product_ids and not counts:
        return None
    if len(store_ids) != 1 or len(product_ids) != 1 or len(counts) != 1:
        raise ValueError("Credo PDP Yotpo store/product/count binding is ambiguous")
    init_data = load_credo_shopify_init_data(html)
    products = init_data["products"]
    if not isinstance(products, list) or not all(isinstance(item, dict) for item in products):
        raise ValueError("Credo PDP Shopify products state is invalid")
    matching_products = [
        item
        for item in products
        if str(item.get("id") or "") == product_ids[0]
        and item.get("handle") == match.group("handle")
    ]
    if len(matching_products) != 1:
        raise ValueError("Credo PDP Yotpo product differs from Shopify page identity")
    return CredoYotpoBinding(
        source_url=f"https://credobeauty.com/products/{match.group('handle')}",
        handle=match.group("handle"),
        store_id=store_ids[0],
        product_id=product_ids[0],
        declared_review_count=counts[0],
        qna_exposed=bool(
            (qna_section := re.search(
                r'<section\b[^>]*id=["\']yotpo-reviews-qa["\'][^>]*>(.*?)</section>',
                html,
                re.IGNORECASE | re.DOTALL,
            ))
            and re.search(r"<(?:dt|dd)\b", qna_section.group(1), re.IGNORECASE)
        ),
    )


def capture_credo_yotpo_deep(
    *,
    binding: CredoYotpoBinding,
    review_limit: int = _MAX_REVIEW_LIMIT,
    timeout_seconds: float = 30.0,
    max_response_bytes: int = 5_000_000,
    fetcher: YotpoFetcher | None = None,
) -> CredoYotpoDeepCaptureReceipt:
    if not 1 <= review_limit <= _MAX_REVIEW_LIMIT:
        raise ValueError("review_limit must be between 1 and 100")
    desired = min(review_limit, binding.declared_review_count)
    transport = "direct_no_proxy" if fetcher is None else "caller_supplied_unverified"
    fetch_api = fetcher or _default_fetcher
    ids_by_role: dict[str, list[str]] = {}
    dates_by_role: dict[str, list[datetime]] = {}
    responses: list[CredoYotpoResponseRecord] = []
    residuals: list[str] = []
    for role, sort in (("most_relevant", "smart"), ("most_recent", "date")):
        role_ids: list[str] = []
        role_dates: list[datetime] = []
        for page in range(1, (desired + _PER_PAGE - 1) // _PER_PAGE + 1):
            url = _review_url(binding=binding, page=page, sort=sort)
            fetched = list(fetch_api([url], timeout_seconds, max_response_bytes))
            if len(fetched) != 1:
                raise ValueError(f"Credo Yotpo {role} page {page} returned {len(fetched)} responses")
            response = fetched[0]
            _validate_response_url(
                response.final_url,
                binding=binding,
                page=page,
                sort=sort,
            )
            if response.status != 200 or not response.ok:
                raise ValueError(f"Credo Yotpo {role} page {page} returned HTTP {response.status}")
            payload = json.loads(response.body_text)
            pagination = payload.get("pagination")
            reviews = payload.get("reviews")
            if not isinstance(pagination, dict) or not isinstance(reviews, list):
                raise ValueError(f"Credo Yotpo {role} page {page} lacks pagination/reviews")
            if (
                pagination.get("page") != page
                or pagination.get("perPage") != _PER_PAGE
                or pagination.get("total") != binding.declared_review_count
            ):
                raise ValueError(f"Credo Yotpo {role} page {page} pagination changed")
            for index, review in enumerate(reviews):
                if not isinstance(review, dict) or review.get("id") is None:
                    raise ValueError(f"Credo Yotpo {role} page {page} review {index} lacks id")
                review_id = str(review["id"])
                if review_id in role_ids:
                    raise ValueError(f"Credo Yotpo {role} duplicated review id {review_id}")
                role_ids.append(review_id)
                if role == "most_recent":
                    created = review.get("createdAt")
                    if not isinstance(created, str):
                        raise ValueError(f"Credo recent review {review_id} lacks createdAt")
                    role_dates.append(datetime.fromisoformat(created))
            responses.append(
                CredoYotpoResponseRecord(
                    role=role,  # type: ignore[arg-type]
                    sort=sort,  # type: ignore[arg-type]
                    page=page,
                    requested_url=url,
                    final_url=response.final_url,
                    status=response.status,
                    body_sha256=hashlib.sha256(response.body_text.encode("utf-8")).hexdigest(),
                    body_text=response.body_text,
                    row_count=len(reviews),
                    declared_total=binding.declared_review_count,
                )
            )
        ids_by_role[role] = role_ids[:desired]
        dates_by_role[role] = role_dates[:desired]
        if len(role_ids) < desired:
            residuals.append(
                f"credo_deep_{role}_shortfall:expected={desired}:observed={len(role_ids)}"
            )
    if any(
        left < right
        for left, right in zip(
            dates_by_role["most_recent"], dates_by_role["most_recent"][1:]
        )
    ):
        residuals.append("credo_deep_most_recent_not_descending")
    if binding.qna_exposed:
        residuals.append("credo_deep_qna_exposed_not_captured")
    relevant_ids = ids_by_role["most_relevant"]
    recent_ids = ids_by_role["most_recent"]
    return CredoYotpoDeepCaptureReceipt(
        source_url=binding.source_url,
        handle=binding.handle,
        store_id=binding.store_id,
        product_id=binding.product_id,
        transport_posture=transport,  # type: ignore[arg-type]
        proxy_used=False if fetcher is None else None,
        requested_limit_per_role=review_limit,
        declared_review_count=binding.declared_review_count,
        most_relevant_review_ids=relevant_ids,
        most_recent_review_ids=recent_ids,
        overlap_review_ids=sorted(set(relevant_ids) & set(recent_ids)),
        qna_posture="exposed_not_captured" if binding.qna_exposed else "not_exposed",
        responses=responses,
        status="partial" if residuals else "complete",
        residuals=residuals,
    )


def _review_url(*, binding: CredoYotpoBinding, page: int, sort: str) -> str:
    return (
        f"https://api-cdn.yotpo.com/v3/storefront/store/{binding.store_id}/"
        f"product/{binding.product_id}/reviews?"
        + urlencode({"page": page, "perPage": _PER_PAGE, "sort": sort})
    )


def _validate_response_url(
    value: str,
    *,
    binding: CredoYotpoBinding,
    page: int,
    sort: str,
) -> None:
    parsed = urlparse(value)
    expected_path = (
        f"/v3/storefront/store/{binding.store_id}/product/{binding.product_id}/reviews"
    )
    if (
        parsed.scheme != "https"
        or (parsed.hostname or "").lower() != "api-cdn.yotpo.com"
        or parsed.path != expected_path
        or parse_qs(parsed.query, keep_blank_values=True)
        != {"page": [str(page)], "perPage": [str(_PER_PAGE)], "sort": [sort]}
    ):
        raise ValueError("Credo Yotpo response URL does not bind store/product/sort/page")


def _default_fetcher(
    urls: Sequence[str],
    timeout_seconds: float,
    max_response_bytes: int,
) -> Sequence[BrowserPageResponse]:
    return fetch_fragrance_widget_fallback_responses(
        urls=urls,
        timeout_seconds=timeout_seconds,
        max_response_bytes=max_response_bytes,
        use_environment_proxies=False,
    )


__all__ = [
    "CREDO_YOTPO_DEEP_VERSION",
    "CredoYotpoBinding",
    "CredoYotpoDeepCaptureReceipt",
    "CredoYotpoResponseRecord",
    "capture_credo_yotpo_deep",
    "parse_credo_yotpo_binding",
]
