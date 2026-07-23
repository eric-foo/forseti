from __future__ import annotations

import json

import pytest

from source_capture.adapters.browser_snapshot import BrowserPageResponse
from source_capture.credo_brand_grid import load_credo_brand_grid_state
from source_capture.credo_yotpo_deep_capture import (
    capture_credo_yotpo_deep,
    parse_credo_yotpo_binding,
)


_GRID_URL = "https://credobeauty.com/collections/tower-28"
_PDP_URL = "https://credobeauty.com/products/alpha"
_STORE = "IPBTxGSyrV0qCW60sUC8XFGMBu6XKaki377yDdZ3"


def _init_data(*, products, page_type="collection", resource_type="collection"):
    return {
        "shop": {
            "name": "Credo",
            "paymentSettings": {"currencyCode": "USD"},
            "countryCode": "US",
            "storefrontUrl": "https://credobeauty.com",
        },
        "products": products,
        "page": {
            "pageType": page_type,
            "resourceType": resource_type,
            "resourceId": 42,
        },
    }


def _grid_html() -> str:
    state = _init_data(
        products=[
            {"id": "1000", "handle": "alpha"},
            {"id": "2000", "handle": "beta"},
        ]
    )
    return f"""
    <script>collection.title = "Tower 28 Beauty";</script>
    <script>manager({{initData: {json.dumps(state)}, other: true}});</script>
    <ul id="product-grid">
      <li><a href="/products/alpha">Alpha</a>
          <div class="caption newVendor">Tower 28</div></li>
      <li><a href="/products/beta">Beta</a>
          <div class="caption newVendor">Tower 28</div></li>
    </ul>
    """


def _pdp_html() -> str:
    state = _init_data(
        products=[
            {"id": "1000", "handle": "alpha"},
            {"id": "9000", "handle": "free-gift"},
        ],
        page_type="product",
        resource_type="product",
    )
    return f"""
    <script>manager({{initData: {json.dumps(state)}, other: true}});</script>
    <script src="https://cdn-widgetsrepository.yotpo.com/v1/loader/{_STORE}?languageCode=en"></script>
    <div data-yotpo-product-id="1000"></div>
    <div id="yotpo-reviews-section-data">
      <p><strong>Overall rating:</strong> 4.5 / 5 from 12 reviews.</p>
    </div>
    <section id="yotpo-reviews-qa"><dl></dl></section>
    """


def _review_rows(prefix: str, start: int, count: int):
    return [
        {
            "id": f"{prefix}{index}",
            "createdAt": f"2026-07-{20-index:02d}T00:00:00",
        }
        for index in range(start, start + count)
    ]


def test_grid_requires_exact_dom_shopify_identity_and_no_pagination() -> None:
    state = load_credo_brand_grid_state(_grid_html(), requested_url=_GRID_URL)
    assert [card.handle for card in state.cards] == ["alpha", "beta"]
    assert [card.product_id for card in state.cards] == ["1000", "2000"]
    assert state.pagination_next_url is None

    with pytest.raises(ValueError, match="do not reconcile"):
        load_credo_brand_grid_state(
            _grid_html().replace("/products/beta", "/products/gamma"),
            requested_url=_GRID_URL,
        )
    with pytest.raises(ValueError, match="next-page"):
        load_credo_brand_grid_state(
            _grid_html() + '<link rel="next" href="?page=2">',
            requested_url=_GRID_URL,
        )


def test_credo_yotpo_binding_and_deep_orders_are_exact() -> None:
    binding = parse_credo_yotpo_binding(_pdp_html(), source_url=_PDP_URL)
    assert binding is not None
    assert binding.product_id == "1000"
    assert binding.declared_review_count == 12
    assert binding.qna_exposed is False

    def fetcher(urls, _timeout, _max_bytes):
        url = urls[0]
        query = url.split("?", 1)[1]
        params = dict(item.split("=") for item in query.split("&"))
        page = int(params["page"])
        sort = params["sort"]
        rows = _review_rows(sort, (page - 1) * 10, 10 if page == 1 else 2)
        return [
            BrowserPageResponse(
                requested_url=url,
                final_url=url,
                status=200,
                ok=True,
                response_headers={},
                body_text=json.dumps(
                    {
                        "pagination": {"page": page, "perPage": 10, "total": 12},
                        "reviews": rows,
                    }
                ),
            )
        ]

    receipt = capture_credo_yotpo_deep(
        binding=binding,
        review_limit=12,
        fetcher=fetcher,
    )
    assert receipt.status == "complete"
    assert len(receipt.most_relevant_review_ids) == 12
    assert len(receipt.most_recent_review_ids) == 12
    assert len(receipt.responses) == 4


def test_wrong_cause_mutations_reject_provider_and_product_before_fetch() -> None:
    with pytest.raises(ValueError, match="ambiguous"):
        parse_credo_yotpo_binding(
            _pdp_html().replace("?languageCode=en", ""),
            source_url=_PDP_URL,
        )
    with pytest.raises(ValueError, match="differs"):
        parse_credo_yotpo_binding(
            _pdp_html().replace('data-yotpo-product-id="1000"', 'data-yotpo-product-id="9999"'),
            source_url=_PDP_URL,
        )
