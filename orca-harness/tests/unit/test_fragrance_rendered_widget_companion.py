from __future__ import annotations

import json
from datetime import date

from source_capture.adapters.browser_snapshot import BrowserPageObservationSuccess, BrowserPageResponse
from source_capture.fragrance_rendered_widget_companion import (
    FRAGRANCE_RENDERED_WIDGET_COMPANION_CERTIFICATION,
    build_fragrance_rendered_widget_companion_from_observation,
    capture_fragrance_rendered_widget_companion,
    is_fragrance_widget_response_url,
)


PRODUCT_URL = "https://example.test/products/fragrance"
WIDGET_URL = "https://api.judge.me/reviews/reviews_for_widget?shop_domain=example.myshopify.com&platform=shopify&page=1"


def _words(prefix: str, count: int) -> str:
    return " ".join(f"{prefix}{index}" for index in range(count))


def _observation(*, response_body: str | None, total_count: int = 2) -> BrowserPageObservationSuccess:
    aggregate = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "Example Fragrance",
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": 4.5, "reviewCount": total_count},
    }
    responses = []
    if response_body is not None:
        responses.append(_widget_response(response_body, url=WIDGET_URL))
    return BrowserPageObservationSuccess(
        requested_url=PRODUCT_URL,
        final_url=PRODUCT_URL,
        title="Example Fragrance",
        visible_text="Example Fragrance 4.5 (2) $120 Add to Cart Customer Reviews",
        dom_observation={
            "viewport": {"width": 1365, "height": 900},
            "items": [
                {"tag": "h1", "text": "Example Fragrance", "top": 100, "left": 600, "width": 500, "height": 40},
                {"tag": "div", "text": "4.5 (2)", "top": 150, "left": 600, "width": 120, "height": 20},
                {"tag": "div", "text": "$120", "top": 190, "left": 600, "width": 80, "height": 20},
                {"tag": "button", "text": "Add to Cart", "top": 240, "left": 600, "width": 180, "height": 45},
                {"tag": "div", "text": "Size 50ml 2ml Sample", "top": 300, "left": 600, "width": 300, "height": 30},
                {"tag": "div", "text": "Customer Reviews", "top": 760, "left": 600, "width": 220, "height": 30},
            ],
            "json_ld_texts": [json.dumps(aggregate)],
        },
        responses=responses,
        metadata={"viewport_width": 1365, "viewport_height": 900, "response_count": len(responses)},
        warning_notes=[],
        limitation_notes=[],
    )


def _widget_response(body: str, *, url: str) -> BrowserPageResponse:
    return BrowserPageResponse(
        requested_url=url,
        final_url=url,
        status=200,
        ok=True,
        body_text=body,
        response_headers={"content-type": "application/json"},
        limitation_notes=[],
    )


def _widget_body(*, total_count: int, review_count: int) -> str:
    reviews = []
    for index in range(review_count):
        reviews.append(
            {
                "id": f"json-{index}",
                "rating": 4 if index == 0 else 5,
                "created_at": "2026-06-01",
                "body": _words(f"body{index}", 42),
                "verified_buyer": index == 0,
            }
        )
    return json.dumps({"total_count": total_count, "reviews": reviews})


def test_combined_companion_builds_rendered_signals_and_widget_review_coverage() -> None:
    receipt = build_fragrance_rendered_widget_companion_from_observation(
        _observation(response_body=_widget_body(total_count=2, review_count=2), total_count=2),
        source_id="fragrance_retail_example",
        source_site="Example",
        product_url=PRODUCT_URL,
        widget_route={"shop_domain": "example.myshopify.com"},
        as_of_date=date(2026, 6, 29),
    )

    assert receipt.certification == FRAGRANCE_RENDERED_WIDGET_COMPANION_CERTIFICATION
    assert receipt.rendered_companion.rating_or_review_count_visible is True
    assert receipt.rendered_companion.price_visible is True
    assert receipt.rendered_companion.cta_visible is True
    assert receipt.rendered_companion.review_section_visible is True
    assert receipt.rendered_companion.size_or_variant_visible is True
    assert receipt.widget_responses[0].response_kind == "judgeme_reviews_for_widget"
    assert receipt.widget_responses[0].response_origin == "render_passive"
    assert receipt.widget_responses[0].body_sha256 is not None
    assert receipt.focused_review_coverage is not None
    assert receipt.focused_review_coverage.coverage_summary.total_rows == 2
    assert receipt.focused_review_coverage.aggregate_companion.rating_value == 4.5
    assert receipt.fallback_needed is False
    assert "bounded_direct_widget_fallback_needed_for_row_completion" not in receipt.residuals


def test_combined_companion_marks_fallback_when_widget_page_is_incomplete() -> None:
    receipt = build_fragrance_rendered_widget_companion_from_observation(
        _observation(response_body=_widget_body(total_count=3, review_count=1), total_count=3),
        source_id="fragrance_retail_example",
        source_site="Example",
        product_url=PRODUCT_URL,
        as_of_date=date(2026, 6, 29),
    )

    assert receipt.focused_review_coverage is not None
    assert receipt.focused_review_coverage.coverage_summary.total_rows == 1
    assert receipt.focused_review_coverage.coverage_summary.widget_total_count == 3
    assert receipt.fallback_needed is True
    assert "bounded_direct_widget_fallback_needed_for_row_completion" in receipt.residuals
    assert "widget_total_count_deduped_row_count_mismatch" in receipt.focused_review_coverage.residuals


def test_capture_uses_bounded_fallback_when_render_does_not_expose_widget_rows() -> None:
    def fake_observation_fetcher(**_: object) -> BrowserPageObservationSuccess:
        return _observation(response_body=None, total_count=2)

    def fake_fallback_fetcher(**_: object) -> list[BrowserPageResponse]:
        return [_widget_response(_widget_body(total_count=2, review_count=2), url=WIDGET_URL)]

    receipt = capture_fragrance_rendered_widget_companion(
        url=PRODUCT_URL,
        source_id="fragrance_retail_example",
        source_site="Example",
        as_of_date=date(2026, 6, 29),
        observation_fetcher=fake_observation_fetcher,
        fallback_fetcher=fake_fallback_fetcher,
        fallback_widget_urls=[WIDGET_URL],
    )

    assert receipt.rendered_companion.item_count == 6
    assert [response.response_origin for response in receipt.widget_responses] == ["bounded_fallback"]
    assert receipt.focused_review_coverage is not None
    assert receipt.focused_review_coverage.coverage_summary.total_rows == 2
    assert receipt.fallback_needed is False
    assert "passive_widget_not_observed_during_render" in receipt.residuals
    assert "bounded_fallback_widget_response_count:1" in receipt.route_health


def test_widget_response_url_filter_covers_judgeme_and_yotpo_v3() -> None:
    assert is_fragrance_widget_response_url("https://api.judge.me/reviews/reviews_for_widget?shop_domain=x") is True
    assert (
        is_fragrance_widget_response_url(
            "https://api-cdn.yotpo.com/v3/storefront/store/key/product/123/reviews?page=1&perPage=10"
        )
        is True
    )
    assert (
        is_fragrance_widget_response_url(
            "https://api-cdn.yotpo.com/v3/storefront/stores/key/products/123/reviewsMedia?page=1&perPage=10"
        )
        is True
    )
    assert is_fragrance_widget_response_url("https://example.test/assets/app.js") is False