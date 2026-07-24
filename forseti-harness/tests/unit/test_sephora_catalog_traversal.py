from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from source_capture.adapters.sephora_catalog_traversal import (
    SephoraCatalogTraversalPlugin,
)


_URL = (
    "https://www.sephora.com/shop/makeup-cosmetics?country_switch=us"
    "&lang=en&currentPage=1&sortBy=BEST_SELLING"
)


def test_catalog_traversal_collects_two_complete_consecutive_pages() -> None:
    page = MagicMock()
    _configure_no_country_dialog(page)
    page.url = _URL
    page.content.side_effect = [_page_dom(1), _page_dom(2)]
    plugin = SephoraCatalogTraversalPlugin(
        target_url=_URL, page_count=2, traversal_timeout_seconds=10
    )

    outcome = plugin.before_snapshot(page, setup_timeout_ms=1_000)

    assert outcome.steps_completed is True
    assert len(plugin.grid_page_doms) == 2
    assert plugin.grid_observation["capturedPageCount"] == 2
    assert plugin.grid_observation["extractedUniqueParentCount"] == 120
    assert plugin.grid_observation["termination"] == (
        "requested_page_window_reconciled"
    )
    page.goto.assert_called_once()
    assert "currentPage=2" in page.goto.call_args.args[0]
    assert plugin.confirm("").confirmed is True


def test_catalog_traversal_fails_before_retaining_duplicate_second_page() -> None:
    page = MagicMock()
    _configure_no_country_dialog(page)
    page.url = _URL
    page.content.side_effect = [_page_dom(1), _page_dom(2, duplicate_first=60)]
    plugin = SephoraCatalogTraversalPlugin(
        target_url=_URL, page_count=2, traversal_timeout_seconds=10
    )

    outcome = plugin.before_snapshot(page, setup_timeout_ms=1_000)

    assert outcome.steps_completed is False
    assert outcome.reason is not None
    assert "duplicate product identities" in outcome.reason
    assert len(plugin.grid_page_doms) == 1
    assert plugin.grid_observation["termination"] == "unproven"


def test_catalog_traversal_collects_twelve_complete_consecutive_pages() -> None:
    page = MagicMock()
    _configure_no_country_dialog(page)
    page.url = _URL
    page.content.side_effect = [_page_dom(page_number) for page_number in range(1, 13)]
    plugin = SephoraCatalogTraversalPlugin(
        target_url=_URL, page_count=12, traversal_timeout_seconds=30
    )

    outcome = plugin.before_snapshot(page, setup_timeout_ms=1_000)

    assert outcome.steps_completed is True
    assert len(plugin.grid_page_doms) == 12
    assert plugin.grid_observation["capturedPageCount"] == 12
    assert plugin.grid_observation["extractedUniqueParentCount"] == 720
    assert page.goto.call_count == 11
    assert "currentPage=12" in page.goto.call_args.args[0]


def test_catalog_traversal_rejects_more_than_twelve_pages() -> None:
    with pytest.raises(ValueError, match=r"must be in \[1,12\]"):
        SephoraCatalogTraversalPlugin(target_url=_URL, page_count=13)


def test_catalog_traversal_reuses_established_market_preflight() -> None:
    page = MagicMock()
    plugin = SephoraCatalogTraversalPlugin(target_url=_URL, page_count=1)
    expected = MagicMock()

    with patch(
        "source_capture.adapters.sephora_catalog_traversal.SephoraUSMarketPlugin"
    ) as market_plugin:
        market_plugin.return_value.before.return_value = expected
        outcome = plugin.before(page, setup_timeout_ms=60_000)

    assert outcome is expected
    market_plugin.assert_called_once_with(target_url=_URL, page_kind="grid")
    market_plugin.return_value.before.assert_called_once_with(
        page, setup_timeout_ms=30_000
    )


def test_catalog_traversal_fails_if_geo_dialog_reappears_after_preflight() -> None:
    page = MagicMock()
    page.url = _URL
    dialog = page.locator.return_value.filter.return_value
    dialog.count.return_value = 1
    dialog.is_visible.return_value = True
    plugin = SephoraCatalogTraversalPlugin(
        target_url=_URL, page_count=1, traversal_timeout_seconds=10
    )

    outcome = plugin.before_snapshot(page, setup_timeout_ms=1_000)

    assert outcome.steps_completed is False
    assert outcome.reason == (
        "Sephora geo dialog reappeared after country-continuation preflight"
    )
    page.content.assert_not_called()
    assert plugin.grid_observation["geoShippingDialogObserved"] is True
    assert plugin.grid_observation["capturedPageCount"] == 0


def _configure_no_country_dialog(page: MagicMock) -> None:
    page.locator.return_value.filter.return_value.count.return_value = 0


def _page_dom(page: int, *, duplicate_first: int | None = None) -> str:
    start = ((page - 1) * 60) + 1
    products = []
    for page_position in range(1, 61):
        number = start + page_position - 1
        if page_position == 1 and duplicate_first is not None:
            number = duplicate_first
        products.append(
            {
                "productId": f"P{number:06d}",
                "displayName": f"Product {number}",
                "targetUrl": f"/product/product-{number}-P{number:06d}",
                "brandName": f"Brand {number}",
                "currentSku": {
                    "skuId": str(number),
                    "listPrice": f"${number}.00",
                },
                "rating": "4.5",
                "reviews": str(number),
            }
        )
    link_store = json.dumps(
        {
            "page": {
                "nthCategory": {
                    "categoryId": "cat140006",
                    "displayName": "Makeup",
                    "currentPage": page,
                    "pageSize": 60,
                    "totalProducts": 2391,
                    "resultId": f"result-{page}",
                    "targetUrl": "/shop/makeup-cosmetics",
                    "sortOptionCode": "BEST_SELLING",
                    "products": products,
                }
            }
        },
        separators=(",", ":"),
    )
    render_query = json.dumps(
        {
            "country": "US",
            "urlPath": "/shop/makeup-cosmetics",
            "cachedQueryParams": (
                f"currentPage={page}&sortBy=BEST_SELLING"
            ),
        },
        separators=(",", ":"),
    )
    return (
        f"<script>Sephora.renderQueryParams = {render_query};</script>"
        f'<script id="linkStore" type="text/json">{link_store}</script>'
    )
