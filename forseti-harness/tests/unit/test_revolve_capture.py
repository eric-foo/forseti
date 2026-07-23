from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import parse_qs, urlparse

import pytest

from runners import run_revolve_brand_corpus as corpus_runner
from runners.run_revolve_brand_corpus import run_revolve_brand_corpus
from runners.run_source_capture_cloakbrowser_packet import (
    _revolve_content_extraction_spec,
)
from source_capture.adapters import cloakbrowser_snapshot as cloak_snapshot
from source_capture.adapters import fragrance_widget_fallback as widget_fallback
from source_capture.adapters.browser_snapshot import BrowserPageResponse
from source_capture.adapters.cloakbrowser_snapshot import (
    ReusableCloakBrowserSnapshotEngine,
)
from source_capture.adapters.revolve_us_market import (
    RevolveUSMarketPlugin,
    confirm_revolve_us_market,
)
from source_capture.models import VisibleFactStatus
from source_capture.retail_capture_profiles import get_retail_capture_profile
from source_capture.retail_grid_projection import (
    RetailGridCaptureEvent,
    RetailGridCompletenessReconciliation,
    RetailGridProjectionLossLedger,
    RetailGridProjectionPacket,
    RetailGridProjectionPlacement,
    RetailGridProjectionRow,
)
from source_capture.revolve_brand_grid import (
    RevolveBrandGridCard,
    build_revolve_brand_grid_content_record,
    load_revolve_brand_grid_state,
)
from source_capture.revolve_corpus import verify_revolve_corpus
from source_capture.revolve_pdp_content import (
    RevolvePdpAggregateContentRecord,
    build_revolve_pdp_aggregate_content_record,
)
from source_capture.revolve_yotpo_deep_capture import (
    capture_revolve_yotpo_deep,
    capture_revolve_yotpo_deep_from_content,
    select_revolve_deep_candidate,
)
from source_capture.source_detail_sufficiency import (
    evaluate_source_detail_sufficiency,
)


_STYLE_ID = "SUMR-WU76"
_PDP_URL = (
    "https://www.revolve.com/summer-fridays-lip-butter-balm-in-pink-guava/"
    f"dp/{_STYLE_ID}/"
)
_STORE_ID = "b4k4hvSXVzfPzX41MmcY1NO4yJyOAtVxDGEh4bxA"


def _pdp_url(style_id: str, *, slug: str | None = None) -> str:
    return (
        "https://www.revolve.com/"
        f"{slug or 'summer-fridays-' + style_id.lower()}/dp/{style_id}/"
    )


def _product(*, style_id: str = _STYLE_ID, currency: str = "USD", count: int = 12):
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "sku": style_id,
        "name": "Lip Butter Balm in Pink Guava",
        "description": "A hydrating lip balm.",
        "brand": {"@type": "Brand", "name": "Summer Fridays"},
        "offers": {
            "@type": "Offer",
            "price": "24.00",
            "priceCurrency": currency,
            "availability": "https://schema.org/InStock",
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": count,
        },
    }


def _pdp_dom(
    *,
    product_style_id: str = _STYLE_ID,
    yotpo_style_id: str = _STYLE_ID,
    offer_currency: str = "USD",
    yotpo_currency: str = "USD",
    review_count: int = 12,
) -> bytes:
    product = _product(
        style_id=product_style_id,
        currency=offer_currency,
        count=review_count,
    )
    return (
        "<html><head>"
        f'<script type="application/ld+json">{json.dumps(product)}</script>'
        f'<script src="https://cdn-widgetsrepository.yotpo.com/v1/loader/{_STORE_ID}">'
        "</script></head>"
        '<body class="checkout US">'
        '<button aria-label="Country Preference: US | EN | $USD"></button>'
        '<a href="/shipping?countryCode=US">Shipping</a>'
        f'<div data-yotpo-product-id="{yotpo_style_id}" '
        f'data-yotpo-currency="{yotpo_currency}" '
        'data-yotpo-instance-id="849475" '
        'data-yotpo-description="Observed Yotpo description"></div>'
        '<input type="radio" aria-label="color: Pink Guava" checked>'
        '<input type="radio" aria-label="color: Vanilla Beige">'
        f'<img src="https://is4.revolveassets.com/images/p4/n/z/{_STYLE_ID.lower()}_v1.jpg">'
        '<button aria-label="Most relevant">Most relevant</button>'
        '<button aria-label="Most recent">Most recent</button>'
        "</body></html>"
    ).encode()


def _grid_dom() -> str:
    return """
    <html>
      <body class="US">
        <button><div>Country Preference: US</div>
          <span>| <span>EN</span> | <span>$USD</span></span></button>
        <a href="/shipping?countryCode=US">Shipping</a>
        <h1>Summer Fridays</h1>
        <span>2 Items</span>
        <button>View 100</button><button>View 500</button>
        <ul>
          <li class="plp__product" id="SUMR-WU76">
            <a class="product-link"
               href="/summer-fridays-lip-butter-balm/dp/SUMR-WU76/">
              <span class="js-plp-brand">Summer Fridays</span>
              <span class="js-plp-name">Lip Butter Balm</span>
            </a>
            <div class="js-plp-prices-div">$24</div>
            <button aria-label="4.9 out of 5 stars rating in total 2,278 reviews"></button>
            <button data-oos="false">Quick view</button>
            <input type="radio" aria-label="color: Pink Guava" checked>
            <img src="https://is4.revolveassets.com/images/p4/n/z/sumr-wu76_v1.jpg">
          </li>
          <li class="plp__product" id="SUMR-WU75">
            <a class="product-link"
               href="/summer-fridays-cloud-dew/dp/SUMR-WU75/">
              <span class="js-plp-brand">Summer Fridays</span>
              <span class="js-plp-name">Cloud Dew</span>
            </a>
            <div class="js-plp-prices-div">$45</div>
            <button aria-label="4.7 out of 5 stars rating in total 103 reviews"></button>
            <button data-oos="true">Quick view</button>
          </li>
        </ul>
      </body>
    </html>
    """


def _response(url: str, reviews: list[dict[str, object]], *, total: int) -> BrowserPageResponse:
    page = int(parse_qs(urlparse(url).query)["page"][0])
    body = json.dumps(
        {
            "pagination": {"page": page, "perPage": 10, "total": total},
            "reviews": reviews,
        },
        separators=(",", ":"),
    )
    return BrowserPageResponse(
        requested_url=url,
        final_url=url,
        status=200,
        ok=True,
        body_text=body,
        response_headers={"content-type": "application/json"},
    )


def _review_rows(prefix: str, start: int, count: int) -> list[dict[str, object]]:
    return [
        {
            "id": f"{prefix}-{index}",
            "createdAt": f"2026-07-{31 - index:02d}T12:00:00+00:00",
        }
        for index in range(start, start + count)
    ]


def _bound_content_record(
    *,
    style_id: str = _STYLE_ID,
    review_count: int = 12,
    source_url: str | None = None,
) -> RevolvePdpAggregateContentRecord:
    return build_revolve_pdp_aggregate_content_record(
        rendered_dom=_pdp_dom(
            product_style_id=style_id,
            yotpo_style_id=style_id,
            review_count=review_count,
        ),
        visible_text=(
            f"Summer Fridays {style_id} Manufacturer Style No. {style_id} 0.5 oz"
        ).encode(),
        source_url=source_url or _pdp_url(style_id),
    )


def _successful_fetcher(total: int):
    def fetcher(urls, _timeout_seconds, _max_response_bytes):
        url = urls[0]
        query = parse_qs(urlparse(url).query)
        page = int(query["page"][0])
        sort = query["sort"][0]
        prefix = "relevant" if sort == "smart" else "recent"
        start = (page - 1) * 10 + 1
        count = min(10, max(0, total - start + 1))
        return [_response(url, _review_rows(prefix, start, count), total=total)]

    return fetcher


def _corpus_projection() -> RetailGridProjectionPacket:
    rows = [
        RetailGridProjectionRow(
            row_id="grid:SUMR-WU76",
            retailer="revolve",
            placements=[RetailGridProjectionPlacement(grid_position=1)],
            source_visible_fields={
                "source_product_id": "SUMR-WU76",
                "style_id": "SUMR-WU76",
                "product_url": _pdp_url("SUMR-WU76"),
                "name": "Lip Butter Balm",
                "review_count": 12,
                "grid_position": 1,
            },
        ),
        RetailGridProjectionRow(
            row_id="grid:SUMR-WU75",
            retailer="revolve",
            placements=[RetailGridProjectionPlacement(grid_position=2)],
            source_visible_fields={
                "source_product_id": "SUMR-WU75",
                "style_id": "SUMR-WU75",
                "product_url": _pdp_url("SUMR-WU75"),
                "name": "Cloud Dew",
                "review_count": 5,
                "grid_position": 2,
            },
        ),
    ]
    return RetailGridProjectionPacket(
        projection_version="v1",
        capture_event=RetailGridCaptureEvent(
            capture_event_id="revolve-grid-test",
            captured_at="2026-07-23T00:00:00Z",
            requested_url="https://www.revolve.com/summer-fridays/br/95db2c/",
            final_url="https://www.revolve.com/summer-fridays/br/95db2c/",
            capture_profile="revolve_grid_aggregate",
            parser_version="test",
        ),
        rows=rows,
        source_visible_grid_facts={"retailer": "revolve"},
        completeness=RetailGridCompletenessReconciliation(
            status="complete",
            page_declared_result_count=2,
            extracted_unique_parent_count=2,
            extracted_placement_count=2,
            duplicate_placement_count=0,
            subject_binding_confirmed=True,
            termination="retailer_visible_count_reconciled",
        ),
        loss_ledger=RetailGridProjectionLossLedger(
            preserved_evidence_rows=2,
            structure_preserved=True,
        ),
    )


def test_us_market_confirmation_requires_conjoined_identity_and_currency() -> None:
    confirmed = confirm_revolve_us_market(
        _pdp_dom().decode(),
        expected_style_id=_STYLE_ID,
    )
    assert confirmed.confirmed is True

    contradictory = confirm_revolve_us_market(
        _pdp_dom(offer_currency="CAD", yotpo_currency="USD").decode(),
        expected_style_id=_STYLE_ID,
    )
    assert contradictory.confirmed is False
    assert "Product JSON-LD" in contradictory.detail
    assert "contradictory explicit currency" in contradictory.detail

    mismatched = confirm_revolve_us_market(
        _pdp_dom().decode(),
        expected_style_id="SUMR-WU75",
    )
    assert mismatched.confirmed is False
    assert "SUMR-WU75" in mismatched.detail


def test_grid_compact_record_preserves_complete_visible_inventory_state() -> None:
    market = confirm_revolve_us_market(
        _grid_dom(),
        expected_style_id=None,
        page_kind="grid",
    )
    assert market.confirmed is True

    record = build_revolve_brand_grid_content_record(
        rendered_dom=_grid_dom(),
        final_url="https://www.revolve.com/summer-fridays/br/95db2c/",
    )

    assert record["brand_slug"] == "summer-fridays"
    assert record["brand_id"] == "95db2c"
    assert record["declared_count"] == 2
    assert record["view_limit"] == 500
    assert record["continuation_control_present"] is False
    assert record["country_code"] == "US"
    assert record["currency_code"] == "USD"
    cards = record["cards"]
    assert isinstance(cards, list)
    assert [card["style_id"] for card in cards] == ["SUMR-WU76", "SUMR-WU75"]
    assert cards[0]["review_count"] == 2278

    replayed = load_revolve_brand_grid_state(json.dumps(record))
    assert replayed is not None
    assert replayed.brand_slug == "summer-fridays"
    assert replayed.brand_id == "95db2c"
    assert len(replayed.cards) == replayed.declared_count


def test_pdp_content_binds_exact_url_product_yotpo_and_usd() -> None:
    dom = _pdp_dom()
    visible = (
        b"Lip Butter Balm Manufacturer Style No. SUMR-WU76 0.5 oz "
        b"Most relevant Most recent"
    )
    record = build_revolve_pdp_aggregate_content_record(
        rendered_dom=dom,
        visible_text=visible,
        source_url=_PDP_URL,
    )

    assert record.style_id == _STYLE_ID
    assert record.product["sku"] == _STYLE_ID
    assert record.offer["priceCurrency"] == "USD"
    assert record.review_substrate["store_id"] == _STORE_ID
    assert record.review_substrate["product_id"] == _STYLE_ID
    assert record.review_substrate["source_native_depth_orders"] == [
        "Most relevant",
        "Most recent",
    ]
    assert record.input_hashes == {
        "rendered_dom_sha256": hashlib.sha256(dom).hexdigest(),
        "visible_text_sha256": hashlib.sha256(visible).hexdigest(),
    }

    with pytest.raises(ValueError, match="Yotpo route is ambiguous"):
        build_revolve_pdp_aggregate_content_record(
            rendered_dom=_pdp_dom(yotpo_style_id="SUMR-WU75"),
            visible_text=visible,
            source_url=_PDP_URL,
        )

    with pytest.raises(ValueError, match="exactly one target-bound Product"):
        build_revolve_pdp_aggregate_content_record(
            rendered_dom=_pdp_dom(product_style_id="SUMR-WU75"),
            visible_text=visible,
            source_url=_PDP_URL,
        )


def test_deep_capture_paginates_native_sorts_preserves_raw_and_bounds_count() -> None:
    calls: list[str] = []

    def fetcher(urls, _timeout_seconds, _max_response_bytes):
        assert len(urls) == 1
        url = urls[0]
        calls.append(url)
        query = parse_qs(urlparse(url).query)
        page = int(query["page"][0])
        sort = query["sort"][0]
        prefix = "relevant" if sort == "smart" else "recent"
        start = (page - 1) * 10 + 1
        count = 10 if page == 1 else 1
        return [_response(url, _review_rows(prefix, start, count), total=12)]

    receipt = capture_revolve_yotpo_deep(
        rendered_dom=_pdp_dom(review_count=12),
        source_url=_PDP_URL,
        review_limit=11,
        fetcher=fetcher,
    )

    assert receipt.status == "complete"
    assert len(receipt.most_relevant_review_ids) == 11
    assert len(receipt.most_recent_review_ids) == 11
    assert len(receipt.responses) == 4
    assert {parse_qs(urlparse(url).query)["sort"][0] for url in calls} == {
        "smart",
        "date",
    }
    for response in receipt.responses:
        assert response.body_sha256 == hashlib.sha256(
            response.body_text.encode()
        ).hexdigest()

    with pytest.raises(ValueError, match="between 1 and 100"):
        capture_revolve_yotpo_deep(
            rendered_dom=_pdp_dom(),
            source_url=_PDP_URL,
            review_limit=101,
            fetcher=fetcher,
        )


def test_deep_capture_marks_shortfall_and_order_failure_partial() -> None:
    def fetcher(urls, _timeout_seconds, _max_response_bytes):
        url = urls[0]
        query = parse_qs(urlparse(url).query)
        page = int(query["page"][0])
        sort = query["sort"][0]
        if page == 2:
            return [_response(url, [], total=12)]
        if sort == "smart":
            rows = _review_rows("relevant", 1, 10)
        else:
            rows = [
                {"id": "recent-1", "createdAt": "2026-07-01T12:00:00+00:00"},
                {"id": "recent-2", "createdAt": "2026-07-02T12:00:00+00:00"},
            ]
        return [_response(url, rows, total=12)]

    receipt = capture_revolve_yotpo_deep(
        rendered_dom=_pdp_dom(review_count=12),
        source_url=_PDP_URL,
        review_limit=12,
        fetcher=fetcher,
    )

    assert receipt.status == "partial"
    assert any("most_relevant_shortfall" in item for item in receipt.residuals)
    assert any("most_recent_shortfall" in item for item in receipt.residuals)
    assert "revolve_deep_most_recent_not_descending" in receipt.residuals


def test_deep_capture_rejects_duplicate_ids() -> None:
    def fetcher(urls, _timeout_seconds, _max_response_bytes):
        url = urls[0]
        query = parse_qs(urlparse(url).query)
        page = int(query["page"][0])
        sort = query["sort"][0]
        prefix = "relevant" if sort == "smart" else "recent"
        if page == 1:
            rows = _review_rows(prefix, 1, 10)
        else:
            rows = _review_rows(prefix, 10, 2)
        return [_response(url, rows, total=12)]

    with pytest.raises(ValueError, match="duplicated review id"):
        capture_revolve_yotpo_deep(
            rendered_dom=_pdp_dom(review_count=12),
            source_url=_PDP_URL,
            review_limit=12,
            fetcher=fetcher,
        )


def test_deep_candidate_is_highest_review_then_earliest_grid_position() -> None:
    def card(style_id: str, position: int, reviews: int) -> RevolveBrandGridCard:
        return RevolveBrandGridCard(
            grid_position=position,
            style_id=style_id,
            product_url=f"https://www.revolve.com/example/dp/{style_id}/",
            brand_name="Summer Fridays",
            name=style_id,
            price_display="$24",
            average_rating="4.9",
            review_count=reviews,
            color_names=(),
            selected_color=None,
            badges=(),
            out_of_stock=False,
            image_urls=(),
        )

    selected = select_revolve_deep_candidate(
        [
            card("SUMR-WU75", 4, 2278),
            card("SUMR-WU76", 2, 2278),
            card("SUMR-WU77", 1, 100),
        ]
    )
    assert selected.style_id == "SUMR-WU76"


def test_deep_capture_from_retained_content_is_equivalent_and_bound() -> None:
    record = _bound_content_record(review_count=12, source_url=_PDP_URL)
    fetcher = _successful_fetcher(12)

    from_dom = capture_revolve_yotpo_deep(
        rendered_dom=_pdp_dom(review_count=12),
        source_url=_PDP_URL,
        review_limit=12,
        fetcher=fetcher,
    )
    from_content = capture_revolve_yotpo_deep_from_content(
        content_record=record,
        review_limit=12,
        fetcher=fetcher,
    )

    assert from_content.model_dump(mode="json") == from_dom.model_dump(mode="json")

    invalid = record.model_copy(
        update={
            "review_substrate": {
                **record.review_substrate,
                "product_id": "SUMR-WU75",
            }
        }
    )
    with pytest.raises(ValueError, match="exact Yotpo product/count/Q&A binding"):
        capture_revolve_yotpo_deep_from_content(
            content_record=invalid,
            review_limit=12,
            fetcher=fetcher,
        )


def test_corpus_verification_completes_only_with_every_bound_pdp_and_deep() -> None:
    projection = _corpus_projection()
    pdps = [
        _bound_content_record(style_id="SUMR-WU76", review_count=12),
        _bound_content_record(style_id="SUMR-WU75", review_count=5),
    ]
    deep = capture_revolve_yotpo_deep_from_content(
        content_record=pdps[0],
        review_limit=12,
        fetcher=_successful_fetcher(12),
    )

    receipt = verify_revolve_corpus(
        grid_projection=projection,
        pdp_records=pdps,
        deep_receipt=deep,
    )

    assert receipt.status == "complete"
    assert receipt.grid_style_count == 2
    assert receipt.pdp_record_count == 2
    assert receipt.verified_style_ids == ["SUMR-WU75", "SUMR-WU76"]
    assert receipt.deep_candidate_style_id == "SUMR-WU76"
    assert receipt.residuals == []


def test_corpus_verification_fails_closed_for_missing_and_mismatched_pdp() -> None:
    projection = _corpus_projection()
    candidate = _bound_content_record(style_id="SUMR-WU76", review_count=12)
    deep = capture_revolve_yotpo_deep_from_content(
        content_record=candidate,
        review_limit=12,
        fetcher=_successful_fetcher(12),
    )

    missing = verify_revolve_corpus(
        grid_projection=projection,
        pdp_records=[candidate],
        deep_receipt=deep,
    )
    assert missing.status == "partial"
    assert missing.missing_style_ids == ["SUMR-WU75"]
    assert "revolve_corpus_missing_pdp:SUMR-WU75" in missing.residuals

    wrong_url = _bound_content_record(
        style_id="SUMR-WU75",
        review_count=5,
        source_url=_pdp_url("SUMR-WU75", slug="wrong-product"),
    )
    mismatched = verify_revolve_corpus(
        grid_projection=projection,
        pdp_records=[candidate, wrong_url],
        deep_receipt=deep,
    )
    assert mismatched.status == "partial"
    assert [item.style_id for item in mismatched.pdp_url_mismatches] == [
        "SUMR-WU75"
    ]
    assert any(
        item.startswith("revolve_corpus_pdp_url_mismatch:SUMR-WU75")
        for item in mismatched.residuals
    )


def test_corpus_verification_rejects_partial_deep_receipt() -> None:
    projection = _corpus_projection()
    pdps = [
        _bound_content_record(style_id="SUMR-WU76", review_count=12),
        _bound_content_record(style_id="SUMR-WU75", review_count=5),
    ]

    def short_fetcher(urls, _timeout_seconds, _max_response_bytes):
        url = urls[0]
        return [_response(url, [], total=12)]

    deep = capture_revolve_yotpo_deep_from_content(
        content_record=pdps[0],
        review_limit=12,
        fetcher=short_fetcher,
    )
    assert deep.status == "partial"

    receipt = verify_revolve_corpus(
        grid_projection=projection,
        pdp_records=pdps,
        deep_receipt=deep,
    )

    assert receipt.status == "partial"
    assert "status:expected=complete:observed=partial" in receipt.deep_binding_mismatches
    assert any(
        "revolve_corpus_deep_binding_mismatch:status:expected=complete"
        in item
        for item in receipt.residuals
    )


def test_brand_corpus_grid_failure_writes_receipt_without_proxy_or_profile(
    tmp_path,
) -> None:
    calls: list[list[str]] = []

    def capture_main(args):
        assert args is not None
        calls.append(list(args))
        return 7

    output_root = tmp_path / "revolve-corpus"
    exit_code, receipt = run_revolve_brand_corpus(
        brand_url="https://www.revolve.com/summer-fridays/br/95db2c/",
        output_root=output_root,
        capture_main=capture_main,
    )

    assert exit_code == 7
    assert receipt.status == "partial"
    assert receipt.failure == "revolve_grid_capture_failed:exit=7"
    assert len(calls) == 1
    args = calls[0]
    assert "--proxy" not in args
    assert "--profile" not in args
    assert "--profile-dir" not in args
    assert "--user-data-dir" not in args
    capture_context = args[args.index("--capture-context") + 1]
    assert "no VPN, proxy, stored browser profile" in capture_context
    persisted = json.loads((output_root / "run-receipt.json").read_text())
    assert persisted["failure"] == "revolve_grid_capture_failed:exit=7"


class _PreferenceLocator:
    def __init__(self, page, selector: str) -> None:
        self.page = page
        self.selector = selector

    def count(self) -> int:
        if self.selector.startswith('button[data-url='):
            return int(self.page.trigger_ready)
        return int(self.page.dialog_ready)

    def click(self, **_kwargs) -> None:
        if self.selector.startswith('button[data-url='):
            self.page.dialog_requested = True

    def select_option(self, **_kwargs) -> None:
        assert self.page.dialog_ready


class _DelayedPreferencePage:
    def __init__(self) -> None:
        self.url = "https://www.revolve.com/summer-fridays/br/95db2c/"
        self.trigger_ready = False
        self.dialog_requested = False
        self.dialog_ready = False
        self.waited: list[str] = []

    def goto(self, *_args, **_kwargs) -> None:
        return None

    def wait_for_timeout(self, _milliseconds: int) -> None:
        return None

    def content(self) -> str:
        return '<body class="SG"></body>'

    def wait_for_selector(self, selector: str, **_kwargs) -> None:
        self.waited.append(selector)
        if selector.startswith('button[data-url='):
            self.trigger_ready = True
        else:
            assert self.dialog_requested
            self.dialog_ready = True

    def locator(self, selector: str) -> _PreferenceLocator:
        return _PreferenceLocator(self, selector)


def test_market_plugin_waits_for_delayed_trigger_and_dialog_controls() -> None:
    page = _DelayedPreferencePage()
    plugin = RevolveUSMarketPlugin(
        target_url="https://www.revolve.com/summer-fridays/br/95db2c/",
        page_kind="grid",
    )

    outcome = plugin.before(page, setup_timeout_ms=10_000)

    assert outcome.steps_completed is True
    assert page.waited[0].startswith('button[data-url=')
    assert page.waited[1:] == [
        "#preferences-shipTo",
        "#preferences-currency",
        'button:has-text("Update Preferences")',
    ]


def test_deep_capture_rejects_redirected_or_cross_product_response() -> None:
    def redirected_fetcher(urls, _timeout_seconds, _max_response_bytes):
        exact = _response(urls[0], _review_rows("relevant", 1, 1), total=1)
        return [
            replace(
                exact,
                final_url=exact.final_url.replace("SUMR-WU76", "SUMR-WU75"),
            )
        ]

    with pytest.raises(ValueError, match="response URL does not bind"):
        capture_revolve_yotpo_deep(
            rendered_dom=_pdp_dom(review_count=1),
            source_url=_PDP_URL,
            review_limit=1,
            fetcher=redirected_fetcher,
        )


def test_brand_corpus_deep_failure_persists_partial_receipt(
    tmp_path, monkeypatch
) -> None:
    projection = _corpus_projection()

    def capture_main(args):
        assert args is not None
        values = list(args)
        if "--retail-grid-projection-output" in values:
            path = values[values.index("--retail-grid-projection-output") + 1]
            Path(path).write_text(projection.model_dump_json(), encoding="utf-8")
        return 0

    def load_record(packet_directory):
        style_id = packet_directory.name
        return _bound_content_record(
            style_id=style_id,
            review_count=12 if style_id == "SUMR-WU76" else 5,
        )

    def fail_deep(**_kwargs):
        raise RuntimeError("injected Yotpo transport failure")

    monkeypatch.setattr(corpus_runner, "_load_revolve_pdp_record", load_record)
    output_root = tmp_path / "revolve-deep-failure"
    exit_code, receipt = run_revolve_brand_corpus(
        brand_url="https://www.revolve.com/summer-fridays/br/95db2c/",
        output_root=output_root,
        capture_main=capture_main,
        deep_capture=fail_deep,
    )

    assert exit_code == 3
    assert receipt.status == "partial"
    assert receipt.captured_pdp_count == 2
    assert receipt.failure == (
        "revolve_deep_capture_failed:RuntimeError:"
        "injected Yotpo transport failure"
    )
    persisted = json.loads((output_root / "run-receipt.json").read_text())
    assert persisted["status"] == "partial"
    assert persisted["captured_pdp_count"] == 2
    assert persisted["failure"] == receipt.failure


def test_raw_grid_canonical_subject_and_split_footer_usd_are_preserved() -> None:
    raw_dom = _grid_dom().replace(
        "<html>",
        (
            "<html><head>"
            '<link rel="canonical" '
            'href="https://www.revolve.com/summer-fridays/br/95db2c/?src=nav">'
            "</head>"
        ),
    ).replace(
        '<button aria-label="Country Preference: US | EN | $USD"></button>',
        (
            "<footer><span>Country Preference: US</span>"
            "<span>| EN |</span><span>$USD</span></footer>"
        ),
    )

    state = load_revolve_brand_grid_state(raw_dom)

    assert state is not None
    assert state.brand_slug == "summer-fridays"
    assert state.brand_id == "95db2c"
    assert state.country_code == "US"
    assert state.currency_code == "USD"


def test_market_plugin_normalizes_mixed_case_pdp_path_identity() -> None:
    plugin = RevolveUSMarketPlugin(
        target_url=(
            "https://www.revolve.com/Summer-Fridays-Jet-Lag-Mask/"
            "dp/sumr-wu118/"
        ),
        style_id="SUMR-WU118",
    )
    assert plugin.style_id == "SUMR-WU118"

    with pytest.raises(ValueError, match="matching the requested URL"):
        RevolveUSMarketPlugin(
            target_url=(
                "https://www.revolve.com/Summer-Fridays-Jet-Lag-Mask/"
                "dp/sumr-wu118/"
            ),
            style_id="SUMR-WU117",
        )


def test_brand_corpus_resume_replay_skips_grid_and_uses_canonical_pdp_url(
    tmp_path, monkeypatch
) -> None:
    projection = _corpus_projection()
    first = projection.rows[0]
    canonical_url = _pdp_url("SUMR-WU76")
    tracked_url = canonical_url + "?source=brand-grid&utm_campaign=summer"
    first = first.model_copy(
        update={
            "source_visible_fields": {
                **first.source_visible_fields,
                "product_url": tracked_url,
                "canonical_product_url": canonical_url,
            }
        }
    )
    projection = projection.model_copy(
        update={"rows": [first, *projection.rows[1:]]}
    )
    replay_calls: list[tuple[Path, str, Path]] = []

    def replay(*, packet_directory, brand_url, projection_path):
        replay_calls.append((packet_directory, brand_url, projection_path))
        Path(projection_path).write_text(
            projection.model_dump_json(),
            encoding="utf-8",
        )
        return projection

    capture_calls: list[list[str]] = []

    def capture_main(args):
        assert args is not None
        values = list(args)
        capture_calls.append(values)
        return 8

    monkeypatch.setattr(corpus_runner, "_replay_verified_grid_packet", replay)
    resume_packet = tmp_path / "verified-grid-packet"
    resume_packet.mkdir()
    output_root = tmp_path / "resumed-corpus"
    exit_code, receipt = run_revolve_brand_corpus(
        brand_url="https://www.revolve.com/summer-fridays/br/95db2c/",
        output_root=output_root,
        resume_grid_packet=resume_packet,
        capture_main=capture_main,
    )

    assert exit_code == 8
    assert len(replay_calls) == 1
    assert replay_calls[0][0] == resume_packet.resolve()
    assert len(capture_calls) == 1
    first_capture = capture_calls[0]
    assert "--retail-grid-projection-output" not in first_capture
    assert first_capture[first_capture.index("--retail-capture-profile") + 1] == (
        "revolve_pdp_aggregate"
    )
    assert first_capture[first_capture.index("--url") + 1] == canonical_url
    assert "?" not in first_capture[first_capture.index("--url") + 1]
    assert receipt.status == "partial"
    assert receipt.grid_input_mode == "verified_raw_replay"
    assert receipt.failure == "revolve_pdp_capture_failed:SUMR-WU76:exit=8"
    persisted = json.loads((output_root / "run-receipt.json").read_text())
    assert persisted["grid_input_mode"] == "verified_raw_replay"
    assert persisted["failure"] == receipt.failure


def test_exact_grid_replay_rejects_requested_brand_url_mismatch(
    tmp_path, monkeypatch
) -> None:
    packet = SimpleNamespace(
        source_family="retail_pdp",
        source_locator=SimpleNamespace(
            status=VisibleFactStatus.KNOWN,
            value="https://www.revolve.com/summer-fridays/br/95db2c/",
        ),
    )
    monkeypatch.setattr(
        corpus_runner,
        "load_verified_source_capture_packet_directory",
        lambda _packet_directory: (packet, {}),
    )

    with pytest.raises(
        ValueError,
        match="does not bind the requested REVOLVE brand URL",
    ):
        corpus_runner._replay_verified_grid_packet(
            packet_directory=tmp_path / "verified-grid-packet",
            brand_url="https://www.revolve.com/rare-beauty/br/abcdef/",
            projection_path=tmp_path / "projection.json",
        )


def test_revolve_content_extraction_spec_serializes_strict_record_to_json_dict() -> None:
    spec = _revolve_content_extraction_spec("content")

    extracted = spec.extractor(
        _pdp_dom(review_count=0),
        b"Revolve Style No. SUMR-WU76 $24",
        _PDP_URL,
    )

    assert isinstance(extracted, dict)
    assert extracted["record_kind"] == "retail_pdp_revolve_aggregate_content"
    assert extracted["style_id"] == "SUMR-WU76"
    assert extracted["review_substrate"]["review_count"] == 0


def test_revolve_zero_review_pdp_satisfies_identity_price_market_and_yotpo() -> None:
    profile = get_retail_capture_profile("revolve_pdp_aggregate")
    visible_text = "Revolve Style No. SUMR-WU76 Lip Butter Balm $24"
    rendered_dom = _pdp_dom(review_count=0).decode()

    result = evaluate_source_detail_sufficiency(
        requirements=profile.requirements,
        access_block_reason=None,
        visible_text=visible_text,
        rendered_dom=rendered_dom,
    )

    assert result.passed is True
    assert "Ratings & Reviews" not in profile.requirements.visible_text_contains
    assert not any(
        "Based on" in pattern
        for pattern in profile.requirements.visible_text_regexes
    )


def test_reusable_cloakbrowser_engine_reuses_context_with_fresh_pages_and_closes(
    monkeypatch,
) -> None:
    class BodyLocator:
        def inner_text(self, **_kwargs):
            return "fresh page body"

    class Page:
        def __init__(self, index: int) -> None:
            self.index = index
            self.url = "about:blank"
            self.closed = False
            self.viewport = None

        def set_viewport_size(self, viewport) -> None:
            self.viewport = viewport

        def goto(self, url, **_kwargs) -> None:
            self.url = url

        def content(self) -> str:
            return f"<html><body>page {self.index}</body></html>"

        def locator(self, selector: str):
            assert selector == "body"
            return BodyLocator()

        def screenshot(self, **_kwargs) -> bytes:
            return f"png-{self.index}".encode()

        def title(self) -> str:
            return f"Page {self.index}"

        def close(self) -> None:
            self.closed = True

    class Context:
        def __init__(self) -> None:
            self.pages: list[Page] = []
            self.closed = False

        def new_page(self) -> Page:
            page = Page(len(self.pages) + 1)
            self.pages.append(page)
            return page

        def close(self) -> None:
            self.closed = True

    class Browser:
        def __init__(self) -> None:
            self.context = Context()
            self.context_calls: list[dict[str, object]] = []
            self.closed = False

        def new_context(self, **kwargs):
            self.context_calls.append(kwargs)
            return self.context

        def close(self) -> None:
            self.closed = True

    browser = Browser()
    launch_calls: list[dict[str, object]] = []
    persistent_launch_calls: list[object] = []

    def launch(**kwargs):
        launch_calls.append(kwargs)
        return browser

    def launch_persistent_context(*args, **kwargs):
        persistent_launch_calls.append((args, kwargs))
        raise AssertionError("reusable engine must not load a stored profile")

    fake_cloakbrowser = SimpleNamespace(
        launch=launch,
        launch_persistent_context=launch_persistent_context,
    )
    monkeypatch.setattr(
        cloak_snapshot,
        "import_module",
        lambda name: fake_cloakbrowser if name == "cloakbrowser" else None,
    )
    engine = ReusableCloakBrowserSnapshotEngine()
    capture_args = {
        "timeout_seconds": 5.0,
        "wait_until": "domcontentloaded",
        "viewport_width": 1280,
        "viewport_height": 720,
        "proxy_profile": None,
        "block_heavy_assets": False,
        "user_data_dir": None,
    }

    first = engine.capture(url="https://www.revolve.com/first", **capture_args)
    second = engine.capture(url="https://www.revolve.com/second", **capture_args)

    assert len(launch_calls) == 1
    assert launch_calls[0]["proxy"] is None
    assert persistent_launch_calls == []
    assert len(browser.context_calls) == 1
    assert browser.context_calls[0] == {
        "viewport": {"width": 1280, "height": 720}
    }
    assert len(browser.context.pages) == 2
    assert browser.context.pages[0] is not browser.context.pages[1]
    assert all(page.closed for page in browser.context.pages)
    assert first.browser_context_scope == "run_scoped_in_memory"
    assert first.browser_context_reused is False
    assert second.browser_context_reused is True
    assert browser.context.closed is False
    assert browser.closed is False

    engine.close()

    assert browser.context.closed is True
    assert browser.closed is True


def test_default_yotpo_fetch_disables_ambient_proxy_and_receipts_direct_posture(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Headers(dict[str, str]):
        def get_content_charset(self) -> str | None:
            return None

    class Response:
        def __init__(self, url: str, body: bytes) -> None:
            self._url = url
            self._body = body
            self.headers = Headers({"content-type": "application/json"})

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        def getcode(self) -> int:
            return 200

        def geturl(self) -> str:
            return self._url

        def read(self, size: int = -1) -> bytes:
            return self._body if size < 0 else self._body[:size]

    class DirectOpener:
        def open(self, request, *, timeout: float):
            assert timeout == 30.0
            url = request.full_url
            query = parse_qs(urlparse(url).query)
            sort = query["sort"][0]
            body = json.dumps(
                {
                    "pagination": {"page": 1, "perPage": 10, "total": 1},
                    "reviews": [
                        {
                            "id": f"direct-{sort}",
                            "createdAt": "2026-07-23T00:00:00",
                        }
                    ],
                },
                separators=(",", ":"),
            ).encode()
            return Response(url, body)

    proxy_handlers: list[object] = []

    def build_opener(*handlers):
        assert len(handlers) == 1
        proxy_handlers.extend(handlers)
        assert isinstance(handlers[0], widget_fallback.urllib.request.ProxyHandler)
        assert handlers[0].proxies == {}
        return DirectOpener()

    def default_urlopen_must_not_run(*_args, **_kwargs):
        raise AssertionError("default urlopen could inherit ambient proxies")

    monkeypatch.setenv("HTTPS_PROXY", "http://ambient-proxy.invalid:8080")
    monkeypatch.setattr(widget_fallback.urllib.request, "build_opener", build_opener)
    monkeypatch.setattr(
        widget_fallback.urllib.request,
        "urlopen",
        default_urlopen_must_not_run,
    )

    receipt = capture_revolve_yotpo_deep(
        rendered_dom=_pdp_dom(review_count=1),
        source_url=_PDP_URL,
        review_limit=1,
    )

    assert len(proxy_handlers) == 2
    assert receipt.schema_version == "revolve_yotpo_deep_v2"
    assert receipt.transport_posture == "direct_no_proxy"
    assert receipt.proxy_used is False
    assert receipt.status == "complete"


def test_injected_yotpo_fetcher_receipts_unverified_transport() -> None:
    receipt = capture_revolve_yotpo_deep(
        rendered_dom=_pdp_dom(review_count=1),
        source_url=_PDP_URL,
        review_limit=1,
        fetcher=_successful_fetcher(1),
    )

    assert receipt.transport_posture == "caller_supplied_unverified"
    assert receipt.proxy_used is None
