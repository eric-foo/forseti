from __future__ import annotations

import json
from dataclasses import replace
from datetime import date

import pytest

import source_capture.fragrance_rendered_widget_companion as companion_module
from runners import run_fragrance_rendered_widget_companion as runner_module
from source_capture.adapters.browser_snapshot import BrowserPageObservationSuccess, BrowserPageResponse
from source_capture.fragrance_rendered_widget_companion import (
    FRAGRANCE_RENDERED_WIDGET_COMPANION_CERTIFICATION,
    FragranceRenderedWidgetCompanionInputError,
    build_fragrance_rendered_widget_companion_from_observation,
    capture_fragrance_rendered_widget_companion,
    fetch_fragrance_widget_fallback_responses,
    is_fragrance_widget_response_url,
)


PRODUCT_URL = "https://example.test/products/fragrance"
WIDGET_URL = "https://api.judge.me/reviews/reviews_for_widget?shop_domain=example.myshopify.com&platform=shopify&page=1"
WIDGET_URL_PAGE_2 = "https://api.judge.me/reviews/reviews_for_widget?shop_domain=example.myshopify.com&platform=shopify&page=2"
YOTPO_REVIEWS_URL = "https://api-cdn.yotpo.com/v3/storefront/store/key/product/123/reviews?page=1&perPage=10"


def _words(prefix: str, count: int) -> str:
    return " ".join(f"{prefix}{index}" for index in range(count))


def _observation(
    *,
    response_body: str | None,
    total_count: int = 2,
    provider_metadata: dict[str, object] | None = None,
) -> BrowserPageObservationSuccess:
    aggregate = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "Example Fragrance",
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": 4.5, "reviewCount": total_count},
    }
    responses = []
    if response_body is not None:
        responses.append(_widget_response(response_body, url=WIDGET_URL))
    dom_observation = {
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
    }
    if provider_metadata is not None:
        dom_observation["provider_metadata"] = provider_metadata

    return BrowserPageObservationSuccess(
        requested_url=PRODUCT_URL,
        final_url=PRODUCT_URL,
        title="Example Fragrance",
        visible_text="Example Fragrance 4.5 (2) $120 Add to Cart Customer Reviews",
        dom_observation=dom_observation,
        responses=responses,
        metadata={"viewport_width": 1365, "viewport_height": 900, "response_count": len(responses)},
        warning_notes=[],
        limitation_notes=[],
    )


def _widget_response(body: str, *, url: str, status: int = 200, ok: bool = True) -> BrowserPageResponse:
    return BrowserPageResponse(
        requested_url=url,
        final_url=url,
        status=status,
        ok=ok,
        body_text=body,
        response_headers={"content-type": "application/json"},
        limitation_notes=[],
    )


def _widget_body(*, total_count: int, review_count: int) -> str:
    reviews = _reviews(review_count)
    return json.dumps({"total_count": total_count, "reviews": reviews})


def _widget_body_without_total(*, review_count: int) -> str:
    return json.dumps({"reviews": _reviews(review_count)})


def _reviews(review_count: int) -> list[dict[str, object]]:
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
    return reviews


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


def test_combined_companion_marks_fallback_when_rows_have_no_widget_total() -> None:
    receipt = build_fragrance_rendered_widget_companion_from_observation(
        _observation(response_body=_widget_body_without_total(review_count=2), total_count=2),
        source_id="fragrance_retail_example",
        source_site="Example",
        product_url=PRODUCT_URL,
        as_of_date=date(2026, 6, 29),
    )

    assert receipt.focused_review_coverage is not None
    assert receipt.focused_review_coverage.coverage_summary.total_rows == 2
    assert receipt.focused_review_coverage.coverage_summary.widget_total_count is None
    assert receipt.fallback_needed is True
    assert "widget_total_count_absent_completeness_unverified" in receipt.residuals
    assert "widget_total_count_absent_completeness_unverified" in receipt.focused_review_coverage.residuals
    assert "bounded_direct_widget_fallback_needed_for_row_completion" in receipt.residuals


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


def test_capture_auto_derives_judgeme_fallback_from_dom_metadata() -> None:
    captured_urls: list[str] = []

    def fake_observation_fetcher(**_: object) -> BrowserPageObservationSuccess:
        return _observation(
            response_body=None,
            total_count=13,
            provider_metadata={
                "judge_me": {
                    "present": True,
                    "myshopify_domains": ["example.myshopify.com"],
                    "product_ids": ["1234567890123"],
                    "review_count": 13,
                }
            },
        )

    def fake_fallback_fetcher(**kwargs: object) -> list[BrowserPageResponse]:
        captured_urls.extend(kwargs["urls"])  # type: ignore[arg-type]
        return [_widget_response(_widget_body(total_count=2, review_count=2), url=captured_urls[0])]

    receipt = capture_fragrance_rendered_widget_companion(
        url=PRODUCT_URL,
        source_id="fragrance_retail_example",
        source_site="Example",
        as_of_date=date(2026, 6, 29),
        observation_fetcher=fake_observation_fetcher,
        fallback_fetcher=fake_fallback_fetcher,
    )

    assert len(captured_urls) == 2
    assert "shop_domain=example.myshopify.com" in captured_urls[0]
    assert "product_id=1234567890123" in captured_urls[0]
    assert "page=2" in captured_urls[1]
    assert receipt.widget_route["auto_judgeme_detected"] is True
    assert receipt.widget_route["auto_judgeme_page_count"] == 2
    assert [response.response_origin for response in receipt.widget_responses] == ["bounded_fallback"]
    assert receipt.focused_review_coverage is not None
    assert receipt.fallback_needed is False




def test_capture_auto_judgeme_multiple_page_candidates_are_residualized_without_fetch() -> None:
    def fake_observation_fetcher(**_: object) -> BrowserPageObservationSuccess:
        return _observation(
            response_body=None,
            total_count=2,
            provider_metadata={
                "judge_me": {
                    "present": True,
                    "myshopify_domains": ["example.myshopify.com", "other.myshopify.com"],
                    "product_ids": ["1234567890123", "9999999999999"],
                    "review_count": 2,
                }
            },
        )

    def fake_fallback_fetcher(**_: object) -> list[BrowserPageResponse]:
        raise AssertionError("ambiguous Judge.me route should not fetch fallback URLs")

    receipt = capture_fragrance_rendered_widget_companion(
        url=PRODUCT_URL,
        source_id="fragrance_retail_example",
        source_site="Example",
        as_of_date=date(2026, 6, 29),
        observation_fetcher=fake_observation_fetcher,
        fallback_fetcher=fake_fallback_fetcher,
    )

    assert receipt.fallback_needed is True
    assert receipt.widget_route["auto_judgeme_detected"] is True
    assert "auto_judgeme_multiple_shop_domain_candidates" in receipt.residuals
    assert "auto_judgeme_multiple_product_id_candidates" in receipt.residuals
    assert "auto_judgeme_fallback_underivable" in receipt.residuals
    assert "parseable_widget_review_responses_absent" in receipt.residuals


def test_capture_auto_judgeme_prefers_widget_scoped_product_id_over_page_candidates() -> None:
    captured_urls: list[str] = []

    def fake_observation_fetcher(**_: object) -> BrowserPageObservationSuccess:
        return _observation(
            response_body=None,
            total_count=2,
            provider_metadata={
                "judge_me": {
                    "present": True,
                    "myshopify_domains": ["example.myshopify.com", "other.myshopify.com"],
                    "widget_myshopify_domains": ["example.myshopify.com"],
                    "widget_product_ids": ["1234567890123"],
                    "product_ids": ["1234567890123", "9999999999999"],
                    "review_count": 2,
                }
            },
        )

    def fake_fallback_fetcher(**kwargs: object) -> list[BrowserPageResponse]:
        captured_urls.extend(kwargs["urls"])  # type: ignore[arg-type]
        return [_widget_response(_widget_body(total_count=1, review_count=1), url=captured_urls[0])]

    receipt = capture_fragrance_rendered_widget_companion(
        url=PRODUCT_URL,
        source_id="fragrance_retail_example",
        source_site="Example",
        as_of_date=date(2026, 6, 29),
        observation_fetcher=fake_observation_fetcher,
        fallback_fetcher=fake_fallback_fetcher,
    )

    assert len(captured_urls) == 1
    assert "shop_domain=example.myshopify.com" in captured_urls[0]
    assert "product_id=1234567890123" in captured_urls[0]
    assert "auto_judgeme_multiple_product_id_candidates" not in receipt.residuals
    assert receipt.fallback_needed is False


def test_capture_auto_judgeme_caps_pages_and_records_uncapped_page_count() -> None:
    captured_urls: list[str] = []

    def fake_observation_fetcher(**_: object) -> BrowserPageObservationSuccess:
        return _observation(
            response_body=None,
            total_count=57,
            provider_metadata={
                "judge_me": {
                    "present": True,
                    "myshopify_domains": ["example.myshopify.com"],
                    "product_ids": ["1234567890123"],
                    "review_count": 57,
                }
            },
        )

    def fake_fallback_fetcher(**kwargs: object) -> list[BrowserPageResponse]:
        captured_urls.extend(kwargs["urls"])  # type: ignore[arg-type]
        return [_widget_response(_widget_body(total_count=1, review_count=1), url=captured_urls[0])]

    receipt = capture_fragrance_rendered_widget_companion(
        url=PRODUCT_URL,
        source_id="fragrance_retail_example",
        source_site="Example",
        as_of_date=date(2026, 6, 29),
        observation_fetcher=fake_observation_fetcher,
        fallback_fetcher=fake_fallback_fetcher,
    )

    assert len(captured_urls) == 5
    assert receipt.widget_route["auto_judgeme_page_count"] == 5
    assert receipt.widget_route["auto_judgeme_page_count_capped"] == 6


def test_capture_auto_judgeme_prefers_operator_pinned_widget_route() -> None:
    captured_urls: list[str] = []

    def fake_observation_fetcher(**_: object) -> BrowserPageObservationSuccess:
        return _observation(
            response_body=None,
            total_count=2,
            provider_metadata={
                "judge_me": {
                    "present": True,
                    "myshopify_domains": ["wrong.myshopify.com"],
                    "product_ids": ["9999999999999"],
                    "review_count": 2,
                }
            },
        )

    def fake_fallback_fetcher(**kwargs: object) -> list[BrowserPageResponse]:
        captured_urls.extend(kwargs["urls"])  # type: ignore[arg-type]
        return [_widget_response(_widget_body(total_count=1, review_count=1), url=captured_urls[0])]

    receipt = capture_fragrance_rendered_widget_companion(
        url=PRODUCT_URL,
        source_id="fragrance_retail_example",
        source_site="Example",
        widget_route={"shop_domain": "pinned.myshopify.com", "product_id": "1234567890123"},
        as_of_date=date(2026, 6, 29),
        observation_fetcher=fake_observation_fetcher,
        fallback_fetcher=fake_fallback_fetcher,
    )

    assert "shop_domain=pinned.myshopify.com" in captured_urls[0]
    assert "product_id=1234567890123" in captured_urls[0]
    assert receipt.widget_route["auto_judgeme_source"] == "operator_widget_route"


def test_companion_surfaces_body_absence_and_nested_coverage_residuals() -> None:
    body_empty_widget = json.dumps(
        {
            "total_count": 1,
            "reviews": [{"id": "rating-only-four", "rating": 4, "created_at": "2026-06-01"}],
        }
    )
    receipt = build_fragrance_rendered_widget_companion_from_observation(
        _observation(response_body=body_empty_widget, total_count=2),
        source_id="fragrance_retail_example",
        source_site="Example",
        product_url=PRODUCT_URL,
        as_of_date=date(2026, 6, 29),
    )

    assert receipt.focused_review_coverage is not None
    summary = receipt.focused_review_coverage.coverage_summary
    assert summary.review_body_absent_count == 1
    assert summary.selected_review_body_absent_count == 1
    assert "review_body_absent_rows_present" in receipt.residuals
    assert "selected_review_body_absent_rows_present" in receipt.residuals
    assert "focused_review_coverage_residuals_present" in receipt.residuals
    assert "focused_review_coverage:review_body_absent_rows_present" in receipt.residuals
    assert "focused_review_coverage:aggregate_review_count_widget_total_count_mismatch" in receipt.residuals

def test_capture_threads_lazy_load_scroll_controls_to_observation_fetcher() -> None:
    captured_kwargs: dict[str, object] = {}

    def fake_observation_fetcher(**kwargs: object) -> BrowserPageObservationSuccess:
        captured_kwargs.update(kwargs)
        observation = _observation(response_body=_widget_body(total_count=2, review_count=2), total_count=2)
        return replace(
            observation,
            metadata={
                **observation.metadata,
                "lazy_load_scroll_passes": 2,
                "lazy_load_scroll_passes_executed": 1,
                "lazy_load_scroll_stop_reason": "page_end",
            },
        )

    receipt = capture_fragrance_rendered_widget_companion(
        url=PRODUCT_URL,
        source_id="fragrance_retail_example",
        source_site="Example",
        as_of_date=date(2026, 6, 29),
        observation_fetcher=fake_observation_fetcher,
        lazy_load_scroll_passes=2,
        lazy_load_scroll_step_px=650,
    )

    assert captured_kwargs["lazy_load_scroll_passes"] == 2
    assert captured_kwargs["lazy_load_scroll_step_px"] == 650
    assert "lazy_load_scroll_passes_requested:2" in receipt.route_health
    assert "lazy_load_scroll_passes_executed:1" in receipt.route_health
    assert "lazy_load_scroll_stop_reason:page_end" in receipt.route_health
    assert receipt.fallback_needed is False


def test_companion_omits_lazy_load_route_health_when_not_requested() -> None:
    receipt = build_fragrance_rendered_widget_companion_from_observation(
        _observation(response_body=_widget_body(total_count=2, review_count=2), total_count=2),
        source_id="fragrance_retail_example",
        source_site="Example",
        product_url=PRODUCT_URL,
        as_of_date=date(2026, 6, 29),
    )

    assert not any(item.startswith("lazy_load_scroll_") for item in receipt.route_health)


def test_runner_threads_lazy_load_scroll_controls(monkeypatch: pytest.MonkeyPatch, tmp_path: object) -> None:
    captured_kwargs: dict[str, object] = {}

    def fake_write_fragrance_rendered_widget_companion(**kwargs: object) -> object:
        captured_kwargs.update(kwargs)
        return object()

    monkeypatch.setattr(
        runner_module,
        "write_fragrance_rendered_widget_companion",
        fake_write_fragrance_rendered_widget_companion,
    )
    output_path = tmp_path / "receipt.json"  # type: ignore[operator]

    result = runner_module.run_fragrance_rendered_widget_companion(
        url=PRODUCT_URL,
        output_path=output_path,
        source_id="fragrance_retail_example",
        source_site="Example",
        lazy_load_scroll_passes=3,
        lazy_load_scroll_step_px=700,
    )

    assert result == output_path
    assert captured_kwargs["lazy_load_scroll_passes"] == 3
    assert captured_kwargs["lazy_load_scroll_step_px"] == 700

def test_companion_combines_passive_and_fallback_rows_without_flagging_complete_rows() -> None:
    receipt = build_fragrance_rendered_widget_companion_from_observation(
        _observation(response_body=_widget_body(total_count=3, review_count=1), total_count=3),
        source_id="fragrance_retail_example",
        source_site="Example",
        product_url=PRODUCT_URL,
        as_of_date=date(2026, 6, 29),
        fallback_responses=[_widget_response(_widget_body(total_count=3, review_count=3), url=WIDGET_URL_PAGE_2)],
    )

    assert [response.response_origin for response in receipt.widget_responses] == [
        "render_passive",
        "bounded_fallback",
    ]
    assert receipt.focused_review_coverage is not None
    assert receipt.focused_review_coverage.coverage_summary.total_rows == 3
    assert receipt.focused_review_coverage.coverage_summary.widget_total_count == 3
    assert receipt.fallback_needed is False


def test_yotpo_review_body_is_parsed_from_v3_response() -> None:
    yotpo_body = json.dumps(
        {
            "pagination": {"page": 1, "perPage": 5, "total": 1},
            "bottomline": {"totalReview": 1, "averageScore": 5.0},
            "reviews": [
                {
                    "id": "yotpo-1",
                    "score": 5,
                    "createdAt": "2026-06-01",
                    "content": _words("yotpo", 30),
                    "verifiedBuyer": True,
                }
            ],
        }
    )
    receipt = build_fragrance_rendered_widget_companion_from_observation(
        _observation(response_body=None, total_count=1),
        source_id="fragrance_retail_example",
        source_site="Example",
        product_url=PRODUCT_URL,
        as_of_date=date(2026, 6, 29),
        fallback_responses=[_widget_response(yotpo_body, url=YOTPO_REVIEWS_URL)],
    )

    assert receipt.widget_responses[0].response_kind == "yotpo_v3_reviews"
    assert receipt.widget_responses[0].body_sha256 is not None
    assert receipt.focused_review_coverage is not None
    assert receipt.focused_review_coverage.coverage_summary.total_rows == 1
    assert receipt.focused_review_coverage.aggregate_companion.rating_value == 4.5
    assert receipt.focused_review_coverage.rows[0].row_source == "yotpo_v3_review"
    assert receipt.fallback_needed is False
    assert "yotpo_v3_reviews_preserved_not_parsed" not in receipt.residuals
    assert "parseable_widget_review_responses_absent" not in receipt.residuals


def test_malformed_fallback_body_is_visible_and_keeps_fallback_needed() -> None:
    receipt = build_fragrance_rendered_widget_companion_from_observation(
        _observation(response_body=None, total_count=2),
        source_id="fragrance_retail_example",
        source_site="Example",
        product_url=PRODUCT_URL,
        as_of_date=date(2026, 6, 29),
        fallback_responses=[_widget_response("{", url=WIDGET_URL)],
    )

    assert receipt.focused_review_coverage is None
    assert receipt.fallback_needed is True
    assert any(residual.startswith("widget_review_coverage_parse_failed:") for residual in receipt.residuals)
    assert "bounded_direct_widget_fallback_needed_for_row_completion" in receipt.residuals


def test_invalid_fallback_url_fails_before_render() -> None:
    observation_called = False

    def fake_observation_fetcher(**_: object) -> BrowserPageObservationSuccess:
        nonlocal observation_called
        observation_called = True
        return _observation(response_body=None, total_count=2)

    with pytest.raises(FragranceRenderedWidgetCompanionInputError, match="not a supported fragrance widget endpoint"):
        capture_fragrance_rendered_widget_companion(
            url=PRODUCT_URL,
            source_id="fragrance_retail_example",
            source_site="Example",
            observation_fetcher=fake_observation_fetcher,
            fallback_widget_urls=["https://example.test/not-a-widget"],
        )

    assert observation_called is False


def test_fallback_url_validation_rejects_embedded_credentials() -> None:
    with pytest.raises(FragranceRenderedWidgetCompanionInputError, match="embedded credentials"):
        fetch_fragrance_widget_fallback_responses(
            urls=["https://user:pass@api.judge.me/reviews/reviews_for_widget?shop_domain=x"],
            timeout_seconds=3,
            max_response_bytes=100,
        )


class _FakeHeaders(dict[str, str]):
    def get_content_charset(self) -> str | None:
        return None


class _FakeUrlopenResponse:
    def __init__(self, *, body: bytes, headers: _FakeHeaders | None = None, url: str = WIDGET_URL, status: int = 200):
        self._body = body
        self.headers = headers or _FakeHeaders({"content-type": "application/json"})
        self._url = url
        self.status = status

    def __enter__(self) -> "_FakeUrlopenResponse":
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def getcode(self) -> int:
        return self.status

    def geturl(self) -> str:
        return self._url

    def read(self, size: int = -1) -> bytes:
        if size < 0:
            return self._body
        return self._body[:size]


def test_fallback_fetch_strips_cookie_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    headers = _FakeHeaders(
        {
            "content-type": "application/json",
            "set-cookie": "secret=1",
            "cookie": "secret=1",
        }
    )

    def fake_urlopen(request: object, timeout: float) -> _FakeUrlopenResponse:
        assert timeout == 7
        return _FakeUrlopenResponse(body=_widget_body(total_count=1, review_count=1).encode("utf-8"), headers=headers)

    monkeypatch.setattr(companion_module.urllib.request, "urlopen", fake_urlopen)

    responses = fetch_fragrance_widget_fallback_responses(
        urls=[WIDGET_URL],
        timeout_seconds=7,
        max_response_bytes=10_000,
    )

    assert responses[0].ok is True
    assert responses[0].body_text
    assert responses[0].response_headers == {"content-type": "application/json"}


def test_fallback_fetch_records_network_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_urlopen(request: object, timeout: float) -> None:
        raise OSError("network unavailable")

    monkeypatch.setattr(companion_module.urllib.request, "urlopen", fake_urlopen)

    responses = fetch_fragrance_widget_fallback_responses(
        urls=[WIDGET_URL],
        timeout_seconds=3,
        max_response_bytes=100,
    )

    assert responses[0].status == 0
    assert responses[0].ok is False
    assert responses[0].body_text == ""
    assert responses[0].limitation_notes == ["bounded_fallback_fetch_failed:OSError:network unavailable"]


def test_fallback_fetch_omits_over_cap_body(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_urlopen(request: object, timeout: float) -> _FakeUrlopenResponse:
        return _FakeUrlopenResponse(body=b"abcdef")

    monkeypatch.setattr(companion_module.urllib.request, "urlopen", fake_urlopen)

    responses = fetch_fragrance_widget_fallback_responses(
        urls=[WIDGET_URL],
        timeout_seconds=3,
        max_response_bytes=5,
    )

    assert responses[0].status == 200
    assert responses[0].body_text == ""
    assert responses[0].limitation_notes == ["bounded_fallback_response_body_exceeded_cap:6>5"]


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
