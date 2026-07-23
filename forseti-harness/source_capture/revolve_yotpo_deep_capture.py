"""Bounded, raw-preserving REVOLVE Yotpo deep-PDP capture."""

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
from source_capture.fragrance_rendered_widget_companion import (
    fetch_fragrance_widget_fallback_responses,
)
from source_capture.revolve_brand_grid import RevolveBrandGridCard
from source_capture.revolve_pdp_content import (
    RevolvePdpAggregateContentRecord,
    extract_revolve_style_id_from_url,
)


REVOLVE_YOTPO_DEEP_VERSION = "revolve_yotpo_deep_v2"
_STORE_RE = re.compile(
    r"cdn-widgetsrepository\.yotpo\.com/v1/loader/"
    r"(?P<store_id>[A-Za-z0-9_-]{20,80})",
    re.IGNORECASE,
)
_PRODUCT_RE = re.compile(
    r'data-yotpo-product-id=["\'](?P<product_id>[A-Za-z0-9_-]{2,64})["\']',
    re.IGNORECASE,
)
_QNA_MARKER = "Questions & Answers"
_PER_PAGE = 10
_MAX_REVIEW_LIMIT = 100
YotpoFetcher = Callable[
    [Sequence[str], float, int], Sequence[BrowserPageResponse]
]


class RevolveYotpoResponseRecord(StrictModel):
    role: Literal["most_relevant", "most_recent"]
    sort: Literal["smart", "date"]
    page: int
    requested_url: str
    final_url: str
    status: int
    body_sha256: str
    body_text: str
    response_headers: dict[str, str] = Field(default_factory=dict)
    row_count: int
    declared_total: int


class RevolveYotpoDeepCaptureReceipt(StrictModel):
    schema_version: Literal["revolve_yotpo_deep_v2"] = REVOLVE_YOTPO_DEEP_VERSION
    source_url: str
    style_id: str
    store_id: str
    transport_posture: Literal[
        "direct_no_proxy",
        "caller_supplied_unverified",
        "not_used_no_reviews",
    ]
    proxy_used: bool | None
    requested_limit_per_role: int
    declared_review_count: int
    most_relevant_review_ids: list[str] = Field(default_factory=list)
    most_recent_review_ids: list[str] = Field(default_factory=list)
    overlap_review_ids: list[str] = Field(default_factory=list)
    qna_posture: Literal["not_exposed", "exposed_not_captured"]
    responses: list[RevolveYotpoResponseRecord] = Field(default_factory=list)
    status: Literal["complete", "partial"]
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_status(self) -> "RevolveYotpoDeepCaptureReceipt":
        if self.status == "complete" and self.residuals:
            raise ValueError("complete REVOLVE Yotpo receipt cannot carry residuals")
        if self.status == "partial" and not self.residuals:
            raise ValueError("partial REVOLVE Yotpo receipt requires residuals")
        if self.transport_posture == "direct_no_proxy":
            if self.proxy_used is not False:
                raise ValueError("direct REVOLVE Yotpo transport requires proxy_used=false")
        elif self.proxy_used is not None:
            raise ValueError(
                "non-direct REVOLVE Yotpo transport cannot assert a proxy-used fact"
            )
        return self


def capture_revolve_yotpo_deep(
    *,
    rendered_dom: bytes,
    source_url: str,
    review_limit: int = _MAX_REVIEW_LIMIT,
    timeout_seconds: float = 30.0,
    max_response_bytes: int = 5_000_000,
    fetcher: YotpoFetcher | None = None,
) -> RevolveYotpoDeepCaptureReceipt:
    """Capture REVOLVE's source-native Most Relevant and Most Recent windows."""
    if not 1 <= review_limit <= _MAX_REVIEW_LIMIT:
        raise ValueError("review_limit must be between 1 and 100")
    if timeout_seconds <= 0 or max_response_bytes <= 0:
        raise ValueError("timeout_seconds and max_response_bytes must be positive")
    style_id = extract_revolve_style_id_from_url(source_url)
    if style_id is None:
        raise ValueError("REVOLVE deep capture requires an exact PDP source URL")
    dom = rendered_dom.decode("utf-8", errors="replace")
    store_ids = list(
        dict.fromkeys(match.group("store_id") for match in _STORE_RE.finditer(dom))
    )
    product_ids = list(
        dict.fromkeys(match.group("product_id").upper() for match in _PRODUCT_RE.finditer(dom))
    )
    if len(store_ids) != 1 or product_ids != [style_id]:
        raise ValueError(
            "REVOLVE deep capture requires one Yotpo store and target-bound product id"
        )
    declared = _declared_review_count(dom, style_id=style_id)
    if declared is None:
        raise ValueError("REVOLVE deep capture lacks a target-bound review count")
    qna_exposed = _QNA_MARKER in dom
    return _capture_bound_yotpo_reviews(
        source_url=source_url,
        style_id=style_id,
        store_id=store_ids[0],
        declared=declared,
        qna_exposed=qna_exposed,
        review_limit=review_limit,
        timeout_seconds=timeout_seconds,
        max_response_bytes=max_response_bytes,
        fetcher=fetcher,
    )


def capture_revolve_yotpo_deep_from_content(
    *,
    content_record: RevolvePdpAggregateContentRecord,
    review_limit: int = _MAX_REVIEW_LIMIT,
    timeout_seconds: float = 30.0,
    max_response_bytes: int = 5_000_000,
    fetcher: YotpoFetcher | None = None,
) -> RevolveYotpoDeepCaptureReceipt:
    """Capture the bounded Yotpo windows from a verified retained PDP record."""
    substrate = content_record.review_substrate
    store_id = substrate.get("store_id")
    product_id = substrate.get("product_id")
    declared = substrate.get("review_count")
    qna_exposed = substrate.get("qna_exposed")
    if (
        not isinstance(store_id, str)
        or not store_id
        or product_id != content_record.style_id
        or not isinstance(declared, int)
        or isinstance(declared, bool)
        or declared < 0
        or not isinstance(qna_exposed, bool)
    ):
        raise ValueError(
            "REVOLVE retained PDP record lacks an exact Yotpo product/count/Q&A binding"
        )
    return _capture_bound_yotpo_reviews(
        source_url=content_record.source_url,
        style_id=content_record.style_id,
        store_id=store_id,
        declared=declared,
        qna_exposed=qna_exposed,
        review_limit=review_limit,
        timeout_seconds=timeout_seconds,
        max_response_bytes=max_response_bytes,
        fetcher=fetcher,
    )


def _capture_bound_yotpo_reviews(
    *,
    source_url: str,
    style_id: str,
    store_id: str,
    declared: int,
    qna_exposed: bool,
    review_limit: int,
    timeout_seconds: float,
    max_response_bytes: int,
    fetcher: YotpoFetcher | None,
) -> RevolveYotpoDeepCaptureReceipt:
    if not 1 <= review_limit <= _MAX_REVIEW_LIMIT:
        raise ValueError("review_limit must be between 1 and 100")
    if timeout_seconds <= 0 or max_response_bytes <= 0:
        raise ValueError("timeout_seconds and max_response_bytes must be positive")
    transport_posture = (
        "direct_no_proxy" if fetcher is None else "caller_supplied_unverified"
    )
    proxy_used = False if fetcher is None else None
    if declared == 0:
        residuals = (
            ["revolve_deep_qna_exposed_not_captured"] if qna_exposed else []
        )
        return RevolveYotpoDeepCaptureReceipt(
            source_url=source_url,
            style_id=style_id,
            store_id=store_id,
            transport_posture="not_used_no_reviews",
            proxy_used=None,
            requested_limit_per_role=review_limit,
            declared_review_count=0,
            qna_posture="exposed_not_captured" if qna_exposed else "not_exposed",
            status="partial" if residuals else "complete",
            residuals=residuals,
        )

    fetch_api = fetcher or _default_fetcher
    desired = min(review_limit, declared)
    responses: list[RevolveYotpoResponseRecord] = []
    ids_by_role: dict[str, list[str]] = {}
    dates_by_role: dict[str, list[datetime]] = {}
    residuals: list[str] = []
    for role, sort in (("most_relevant", "smart"), ("most_recent", "date")):
        role_ids: list[str] = []
        role_dates: list[datetime] = []
        pages = (desired + _PER_PAGE - 1) // _PER_PAGE
        for page in range(1, pages + 1):
            url = _review_url(
                store_id=store_id,
                product_id=style_id,
                page=page,
                sort=sort,
            )
            fetched = list(fetch_api([url], timeout_seconds, max_response_bytes))
            if len(fetched) != 1:
                raise ValueError(
                    f"REVOLVE Yotpo {role} page {page} returned {len(fetched)} responses"
                )
            response = fetched[0]
            _validate_response_binding(
                final_url=response.final_url,
                store_id=store_id,
                product_id=style_id,
                page=page,
                sort=sort,
            )
            if response.status != 200 or not response.ok:
                raise ValueError(
                    f"REVOLVE Yotpo {role} page {page} returned HTTP {response.status}"
                )
            try:
                payload = json.loads(response.body_text)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"REVOLVE Yotpo {role} page {page} was not JSON"
                ) from exc
            pagination = payload.get("pagination")
            reviews = payload.get("reviews")
            if not isinstance(pagination, dict) or not isinstance(reviews, list):
                raise ValueError(
                    f"REVOLVE Yotpo {role} page {page} lacks pagination/reviews"
                )
            if (
                pagination.get("page") != page
                or pagination.get("perPage") != _PER_PAGE
                or pagination.get("total") != declared
            ):
                raise ValueError(
                    f"REVOLVE Yotpo {role} page {page} pagination changed"
                )
            for index, review in enumerate(reviews):
                if not isinstance(review, dict) or review.get("id") is None:
                    raise ValueError(
                        f"REVOLVE Yotpo {role} page {page} review {index} lacks id"
                    )
                review_id = str(review["id"])
                if review_id in role_ids:
                    raise ValueError(
                        f"REVOLVE Yotpo {role} duplicated review id {review_id}"
                    )
                role_ids.append(review_id)
                if role == "most_recent":
                    created = review.get("createdAt")
                    if not isinstance(created, str):
                        raise ValueError(
                            f"REVOLVE Yotpo recent review {review_id} lacks createdAt"
                        )
                    role_dates.append(datetime.fromisoformat(created))
            responses.append(
                RevolveYotpoResponseRecord(
                    role=role,  # type: ignore[arg-type]
                    sort=sort,  # type: ignore[arg-type]
                    page=page,
                    requested_url=url,
                    final_url=response.final_url,
                    status=response.status,
                    body_sha256=hashlib.sha256(
                        response.body_text.encode("utf-8")
                    ).hexdigest(),
                    body_text=response.body_text,
                    response_headers=response.response_headers,
                    row_count=len(reviews),
                    declared_total=declared,
                )
            )
        ids_by_role[role] = role_ids[:desired]
        dates_by_role[role] = role_dates[:desired]
        if len(role_ids) < desired:
            residuals.append(
                f"revolve_deep_{role}_shortfall:expected={desired}:observed={len(role_ids)}"
            )
    recent_dates = dates_by_role["most_recent"]
    if any(left < right for left, right in zip(recent_dates, recent_dates[1:])):
        residuals.append("revolve_deep_most_recent_not_descending")
    if qna_exposed:
        residuals.append("revolve_deep_qna_exposed_not_captured")
    relevant_ids = ids_by_role["most_relevant"]
    recent_ids = ids_by_role["most_recent"]
    return RevolveYotpoDeepCaptureReceipt(
        source_url=source_url,
        style_id=style_id,
        store_id=store_id,
        transport_posture=transport_posture,  # type: ignore[arg-type]
        proxy_used=proxy_used,
        requested_limit_per_role=review_limit,
        declared_review_count=declared,
        most_relevant_review_ids=relevant_ids,
        most_recent_review_ids=recent_ids,
        overlap_review_ids=sorted(set(relevant_ids) & set(recent_ids)),
        qna_posture="exposed_not_captured" if qna_exposed else "not_exposed",
        responses=responses,
        status="partial" if residuals else "complete",
        residuals=residuals,
    )


def select_revolve_deep_candidate(
    cards: Sequence[RevolveBrandGridCard],
) -> RevolveBrandGridCard:
    if not cards:
        raise ValueError("REVOLVE deep candidate selection requires grid cards")
    return min(
        cards,
        key=lambda card: (
            -card.review_count,
            card.grid_position,
            card.style_id,
        ),
    )


def _validate_response_binding(
    *, final_url: str, store_id: str, product_id: str, page: int, sort: str
) -> None:
    parsed = urlparse(final_url)
    expected_path = (
        f"/v3/storefront/store/{store_id}/product/{product_id}/reviews"
    )
    query = parse_qs(parsed.query, keep_blank_values=True)
    expected_query = {
        "page": [str(page)],
        "perPage": [str(_PER_PAGE)],
        "sort": [sort],
    }
    if (
        parsed.scheme != "https"
        or (parsed.hostname or "").lower() != "api-cdn.yotpo.com"
        or parsed.path != expected_path
        or query != expected_query
    ):
        raise ValueError(
            "REVOLVE Yotpo response URL does not bind the requested "
            f"store/product/sort/page: {final_url}"
        )


def _review_url(
    *, store_id: str, product_id: str, page: int, sort: str
) -> str:
    return (
        f"https://api-cdn.yotpo.com/v3/storefront/store/{store_id}/"
        f"product/{product_id}/reviews?"
        + urlencode(
            {
                "page": str(page),
                "perPage": str(_PER_PAGE),
                "sort": sort,
            }
        )
    )


def _default_fetcher(
    urls: Sequence[str], timeout_seconds: float, max_response_bytes: int
) -> Sequence[BrowserPageResponse]:
    return fetch_fragrance_widget_fallback_responses(
        urls=urls,
        timeout_seconds=timeout_seconds,
        max_response_bytes=max_response_bytes,
        use_environment_proxies=False,
    )


def _declared_review_count(dom: str, *, style_id: str) -> int | None:
    for match in re.finditer(
        r"<script\b[^>]*type=[\"']application/ld\+json[\"'][^>]*>"
        r"(?P<body>.*?)</script>",
        dom,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        try:
            value = json.loads(match.group("body"))
        except json.JSONDecodeError:
            continue
        for candidate in _walk(value):
            if (
                candidate.get("@type") == "Product"
                and str(candidate.get("sku", "")).upper() == style_id
                and isinstance(candidate.get("aggregateRating"), dict)
            ):
                count = candidate["aggregateRating"].get("reviewCount")
                if isinstance(count, int) and not isinstance(count, bool) and count >= 0:
                    return count
    return None


def _walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


__all__ = [
    "REVOLVE_YOTPO_DEEP_VERSION",
    "RevolveYotpoDeepCaptureReceipt",
    "RevolveYotpoResponseRecord",
    "capture_revolve_yotpo_deep",
    "capture_revolve_yotpo_deep_from_content",
    "select_revolve_deep_candidate",
]
