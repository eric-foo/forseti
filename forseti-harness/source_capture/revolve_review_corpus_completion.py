"""Bounded Most Recent acquisition for every distinct REVOLVE review corpus."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Sequence
from datetime import date, datetime
from typing import Literal
from urllib.parse import parse_qs, urlencode, urlparse

from pydantic import Field, model_validator

from schemas.case_models import StrictModel
from source_capture.adapters.browser_snapshot import BrowserPageResponse
from source_capture.fragrance_rendered_widget_companion import (
    fetch_fragrance_widget_fallback_responses,
)
from source_capture.retail_review_onboarding import (
    RETAIL_REVIEW_CONTEXT_TARGET,
    assess_retail_review_onboarding,
)
from source_capture.revolve_pdp_content import RevolvePdpAggregateContentRecord


REVOLVE_REVIEW_CORPUS_RECEIPT_VERSION = "revolve_review_corpus_recent_v1"
_PER_PAGE = 10
ReviewFetcher = Callable[
    [Sequence[str], float, int], Sequence[BrowserPageResponse]
]


class RevolveRecentReviewResponse(StrictModel):
    page: int
    requested_url: str
    final_url: str
    status: int
    body_sha256: str
    body_text: str
    response_headers: dict[str, str] = Field(default_factory=dict)
    row_count: int
    declared_total: int


class RevolveReviewCorpusReceipt(StrictModel):
    schema_version: Literal["revolve_review_corpus_recent_v1"] = (
        REVOLVE_REVIEW_CORPUS_RECEIPT_VERSION
    )
    retailer: Literal["revolve"] = "revolve"
    provider: Literal["yotpo"] = "yotpo"
    provider_tenant_store: str
    collection_context: str
    corpus_key: str
    source_product_ids: list[str] = Field(min_length=1)
    source_urls: list[str] = Field(min_length=1)
    requested_ordering: Literal["Most Recent"] = "Most Recent"
    actual_ordering: Literal["Most Recent"] = "Most Recent"
    requested_limit: int
    declared_review_count: int
    captured_review_ids: list[str] = Field(default_factory=list)
    responses: list[RevolveRecentReviewResponse] = Field(default_factory=list)
    onboarding_assessment: dict[str, object] | None = None
    transport_posture: Literal["direct_no_proxy", "caller_supplied_unverified"]
    proxy_used: bool | None
    status: Literal["complete", "partial"]
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_completion(self) -> "RevolveReviewCorpusReceipt":
        if self.status == "complete" and self.residuals:
            raise ValueError("complete review-corpus receipt cannot carry residuals")
        if self.status == "partial" and not self.residuals:
            raise ValueError("partial review-corpus receipt requires residuals")
        if self.transport_posture == "direct_no_proxy":
            if self.proxy_used is not False:
                raise ValueError("direct review-corpus transport requires proxy_used=false")
        elif self.proxy_used is not None:
            raise ValueError(
                "caller-supplied review-corpus transport cannot assert proxy use"
            )
        return self


def review_corpus_key(
    *, provider_tenant_store: str, collection_context: str
) -> str:
    basis = f"revolve|yotpo|{provider_tenant_store}|{collection_context}"
    return "review_corpus_" + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:24]


def group_revolve_review_corpora(
    records: Sequence[RevolvePdpAggregateContentRecord],
) -> list[list[RevolvePdpAggregateContentRecord]]:
    grouped: dict[
        tuple[str, str], list[RevolvePdpAggregateContentRecord]
    ] = {}
    for record in records:
        substrate = record.review_substrate
        store_id = substrate.get("store_id")
        product_id = substrate.get("product_id")
        if (
            not isinstance(store_id, str)
            or not store_id
            or not isinstance(product_id, str)
            or not product_id
        ):
            raise ValueError(
                f"REVOLVE PDP {record.style_id} lacks a review corpus identity"
            )
        grouped.setdefault((store_id, product_id), []).append(record)
    return [
        sorted(items, key=lambda item: (item.style_id, item.source_url))
        for _key, items in sorted(grouped.items())
    ]


def capture_revolve_recent_review_corpus(
    *,
    content_records: Sequence[RevolvePdpAggregateContentRecord],
    review_limit: int = RETAIL_REVIEW_CONTEXT_TARGET,
    reference_date: date | None = None,
    timeout_seconds: float = 30.0,
    max_response_bytes: int = 5_000_000,
    fetcher: ReviewFetcher | None = None,
) -> RevolveReviewCorpusReceipt:
    """Capture one distinct Yotpo corpus using only its Most Recent ordering."""
    records = list(content_records)
    if not records:
        raise ValueError("review corpus capture requires at least one PDP record")
    if not 1 <= review_limit <= RETAIL_REVIEW_CONTEXT_TARGET:
        raise ValueError(
            f"review_limit must be between 1 and {RETAIL_REVIEW_CONTEXT_TARGET}"
        )
    if timeout_seconds <= 0 or max_response_bytes <= 0:
        raise ValueError("timeout_seconds and max_response_bytes must be positive")

    groups = group_revolve_review_corpora(records)
    if len(groups) != 1:
        raise ValueError("review corpus capture requires exactly one corpus group")
    substrate = records[0].review_substrate
    store_id = str(substrate["store_id"])
    product_id = str(substrate["product_id"])
    declared_values = {record.review_substrate.get("review_count") for record in records}
    if len(declared_values) != 1:
        raise ValueError("review corpus records disagree on the declared total")
    declared_value = next(iter(declared_values))
    if declared_value is None:
        declared: int | None = None
    elif (
        isinstance(declared_value, int)
        and not isinstance(declared_value, bool)
        and declared_value >= 0
    ):
        declared = declared_value
    else:
        raise ValueError("review corpus records carry an invalid declared total")
    collection_context = f"product/{product_id}"
    corpus_key = review_corpus_key(
        provider_tenant_store=store_id,
        collection_context=collection_context,
    )
    transport_posture = (
        "direct_no_proxy" if fetcher is None else "caller_supplied_unverified"
    )
    proxy_used = False if fetcher is None else None

    if declared == 0:
        return RevolveReviewCorpusReceipt(
            provider_tenant_store=store_id,
            collection_context=collection_context,
            corpus_key=corpus_key,
            source_product_ids=sorted({record.style_id for record in records}),
            source_urls=sorted({record.source_url for record in records}),
            requested_limit=review_limit,
            declared_review_count=0,
            onboarding_assessment={
                "policy": "source_exhausted_zero_rows",
                "admitted": True,
                "status": "source_exhausted",
                "captured_review_count": 0,
                "review_scope_claim": "source_declared_zero_rows",
            },
            transport_posture=transport_posture,
            proxy_used=proxy_used,
            status="complete",
        )

    fetch_api = fetcher or _default_fetcher
    discovered_first_response: BrowserPageResponse | None = None
    if declared is None:
        first_url = _review_url(
            store_id=store_id,
            product_id=product_id,
            page=1,
        )
        discovery = list(
            fetch_api([first_url], timeout_seconds, max_response_bytes)
        )
        if len(discovery) != 1:
            raise ValueError(
                "REVOLVE Yotpo count discovery returned "
                f"{len(discovery)} responses"
            )
        discovered_first_response = discovery[0]
        _validate_response_binding(
            final_url=discovered_first_response.final_url,
            store_id=store_id,
            product_id=product_id,
            page=1,
        )
        if (
            discovered_first_response.status != 200
            or not discovered_first_response.ok
        ):
            raise ValueError(
                "REVOLVE Yotpo count discovery returned HTTP "
                f"{discovered_first_response.status}"
            )
        try:
            discovery_payload = json.loads(discovered_first_response.body_text)
        except json.JSONDecodeError as exc:
            raise ValueError("REVOLVE Yotpo count discovery was not JSON") from exc
        discovery_pagination = discovery_payload.get("pagination")
        discovered_total = (
            discovery_pagination.get("total")
            if isinstance(discovery_pagination, dict)
            else None
        )
        if (
            not isinstance(discovered_total, int)
            or isinstance(discovered_total, bool)
            or discovered_total < 0
        ):
            raise ValueError(
                "REVOLVE Yotpo count discovery lacks a valid pagination total"
            )
        declared = discovered_total

    assert declared is not None
    if declared == 0 and discovered_first_response is not None:
        payload = json.loads(discovered_first_response.body_text)
        reviews = payload.get("reviews")
        if not isinstance(reviews, list) or reviews:
            raise ValueError(
                "REVOLVE Yotpo zero-total discovery returned review rows"
            )
        return RevolveReviewCorpusReceipt(
            provider_tenant_store=store_id,
            collection_context=collection_context,
            corpus_key=corpus_key,
            source_product_ids=sorted({record.style_id for record in records}),
            source_urls=sorted({record.source_url for record in records}),
            requested_limit=review_limit,
            declared_review_count=0,
            responses=[
                RevolveRecentReviewResponse(
                    page=1,
                    requested_url=discovered_first_response.requested_url,
                    final_url=discovered_first_response.final_url,
                    status=discovered_first_response.status,
                    body_sha256=hashlib.sha256(
                        discovered_first_response.body_text.encode("utf-8")
                    ).hexdigest(),
                    body_text=discovered_first_response.body_text,
                    response_headers=discovered_first_response.response_headers,
                    row_count=0,
                    declared_total=0,
                )
            ],
            onboarding_assessment={
                "policy": "source_exhausted_zero_rows",
                "admitted": True,
                "status": "source_exhausted",
                "captured_review_count": 0,
                "review_scope_claim": "source_declared_zero_rows",
            },
            transport_posture=transport_posture,
            proxy_used=proxy_used,
            status="complete",
        )
    desired = min(review_limit, declared)
    urls = [
        _review_url(
            store_id=store_id,
            product_id=product_id,
            page=page,
        )
        for page in range(1, (desired + _PER_PAGE - 1) // _PER_PAGE + 1)
    ]
    if discovered_first_response is None:
        fetched = list(fetch_api(urls, timeout_seconds, max_response_bytes))
    else:
        remaining_urls = urls[1:]
        fetched = [
            discovered_first_response,
            *(
                list(
                    fetch_api(
                        remaining_urls,
                        timeout_seconds,
                        max_response_bytes,
                    )
                )
                if remaining_urls
                else []
            ),
        ]
    if len(fetched) != len(urls):
        raise ValueError(
            "REVOLVE Yotpo Most Recent capture returned "
            f"{len(fetched)} responses for {len(urls)} requests"
        )

    responses: list[RevolveRecentReviewResponse] = []
    review_ids: list[str] = []
    review_dates: list[date] = []
    residuals: list[str] = []
    for page, (requested_url, response) in enumerate(
        zip(urls, fetched, strict=True),
        start=1,
    ):
        _validate_response_binding(
            final_url=response.final_url,
            store_id=store_id,
            product_id=product_id,
            page=page,
        )
        if response.status != 200 or not response.ok:
            raise ValueError(
                f"REVOLVE Yotpo Most Recent page {page} returned HTTP "
                f"{response.status}"
            )
        try:
            payload = json.loads(response.body_text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"REVOLVE Yotpo Most Recent page {page} was not JSON"
            ) from exc
        pagination = payload.get("pagination")
        reviews = payload.get("reviews")
        if not isinstance(pagination, dict) or not isinstance(reviews, list):
            raise ValueError(
                f"REVOLVE Yotpo Most Recent page {page} lacks pagination/reviews"
            )
        if (
            pagination.get("page") != page
            or pagination.get("perPage") != _PER_PAGE
            or pagination.get("total") != declared
        ):
            raise ValueError(
                f"REVOLVE Yotpo Most Recent page {page} pagination changed"
            )
        for index, review in enumerate(reviews):
            if not isinstance(review, dict) or review.get("id") is None:
                raise ValueError(
                    f"REVOLVE Yotpo Most Recent page {page} review {index} lacks id"
                )
            review_id = str(review["id"])
            if review_id in review_ids:
                raise ValueError(
                    f"REVOLVE Yotpo Most Recent duplicated review id {review_id}"
                )
            created = review.get("createdAt")
            if not isinstance(created, str):
                raise ValueError(
                    f"REVOLVE Yotpo Most Recent review {review_id} lacks createdAt"
                )
            review_ids.append(review_id)
            review_dates.append(datetime.fromisoformat(created).date())
        responses.append(
            RevolveRecentReviewResponse(
                page=page,
                requested_url=requested_url,
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

    review_ids = review_ids[:desired]
    review_dates = review_dates[:desired]
    if len(review_ids) < desired:
        residuals.append(
            "revolve_review_corpus_recent_shortfall:"
            f"expected={desired}:observed={len(review_ids)}"
        )
    assessment = assess_retail_review_onboarding(
        review_dates,
        reference_date=reference_date or date.today(),
        continuation_available=declared > len(review_ids),
        source_exhausted=declared <= len(review_ids),
        structure_valid=not residuals,
    )
    if assessment["admitted"] is not True:
        residuals.append(
            "revolve_review_corpus_onboarding_not_admitted:"
            f"status={assessment['status']}"
        )
    return RevolveReviewCorpusReceipt(
        provider_tenant_store=store_id,
        collection_context=collection_context,
        corpus_key=corpus_key,
        source_product_ids=sorted({record.style_id for record in records}),
        source_urls=sorted({record.source_url for record in records}),
        requested_limit=review_limit,
        declared_review_count=declared,
        captured_review_ids=review_ids,
        responses=responses,
        onboarding_assessment=assessment,
        transport_posture=transport_posture,
        proxy_used=proxy_used,
        status="partial" if residuals else "complete",
        residuals=residuals,
    )


def _review_url(*, store_id: str, product_id: str, page: int) -> str:
    return (
        f"https://api-cdn.yotpo.com/v3/storefront/store/{store_id}/"
        f"product/{product_id}/reviews?"
        + urlencode(
            {
                "page": str(page),
                "perPage": str(_PER_PAGE),
                "sort": "date",
            }
        )
    )


def _validate_response_binding(
    *, final_url: str, store_id: str, product_id: str, page: int
) -> None:
    parsed = urlparse(final_url)
    expected_path = (
        f"/v3/storefront/store/{store_id}/product/{product_id}/reviews"
    )
    expected_query = {
        "page": [str(page)],
        "perPage": [str(_PER_PAGE)],
        "sort": ["date"],
    }
    if (
        parsed.scheme != "https"
        or (parsed.hostname or "").lower() != "api-cdn.yotpo.com"
        or parsed.path != expected_path
        or parse_qs(parsed.query, keep_blank_values=True) != expected_query
    ):
        raise ValueError(
            "REVOLVE Yotpo response URL does not bind the requested "
            f"store/product/date/page: {final_url}"
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


__all__ = [
    "REVOLVE_REVIEW_CORPUS_RECEIPT_VERSION",
    "RevolveReviewCorpusReceipt",
    "capture_revolve_recent_review_corpus",
    "group_revolve_review_corpora",
    "review_corpus_key",
]
