from __future__ import annotations

import json

from source_capture.fragrance_review_discovery import (
    THROTTLE,
    ProductRef,
    RateLimiterPolicy,
    discover_judgeme_by_probe,
    discover_yotpo_shop_feed,
    extract_judgeme_product_id,
    judgeme_count_from_response,
    parse_shopify_products_json,
    parse_sitemap_locs,
    parse_yotpo_shop_feed_page,
    select_product_refs_from_sitemap,
    select_product_sitemap_locs,
)


# --- enumeration -----------------------------------------------------------
def test_parse_shopify_products_json_builds_refs() -> None:
    text = json.dumps({"products": [{"handle": "a", "id": 123456, "title": "A"}, {"handle": "b", "id": 789012}]})
    refs = parse_shopify_products_json(text, store_domain="shop.com")
    assert refs[0].product_url == "https://shop.com/products/a"
    assert refs[0].shopify_product_id == "123456"
    assert refs[0].title == "A"
    assert refs[1].title is None


def test_parse_shopify_products_json_empty_when_no_products() -> None:
    assert parse_shopify_products_json(json.dumps({"foo": 1}), store_domain="shop.com") == []


def test_sitemap_locs_and_product_refs() -> None:
    xml = (
        '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        "<url><loc>https://s.com/products/foo</loc></url>"
        "<url><loc>https://s.com/collections/all</loc></url>"
        "<url><loc>https://s.com/products/bar?variant=1</loc></url></urlset>"
    )
    refs = select_product_refs_from_sitemap(parse_sitemap_locs(xml))
    assert {ref.handle for ref in refs} == {"foo", "bar"}
    assert all(ref.shopify_product_id is None for ref in refs)


def test_select_product_sitemap_locs_filters_index() -> None:
    locs = ["https://s.com/sitemap/products_1.xml", "https://s.com/sitemap/pages_1.xml"]
    assert select_product_sitemap_locs(locs) == ["https://s.com/sitemap/products_1.xml"]


# --- Judge.me count + id extraction ---------------------------------------
def test_judgeme_count_multifield() -> None:
    assert judgeme_count_from_response({"total_count": 7}) == 7
    assert judgeme_count_from_response({"number_of_reviews": 4}) == 4
    assert judgeme_count_from_response({"pagination": {"total": 9}}) == 9
    assert judgeme_count_from_response({"bottomline": {"totalReviews": 2}}) == 2
    assert judgeme_count_from_response({"html": "<div/>"}) is None


def test_extract_judgeme_product_id_patterns() -> None:
    assert extract_judgeme_product_id('<div data-product-id="1243179588">') == "1243179588"
    assert extract_judgeme_product_id("gid://shopify/Product/451146516") == "451146516"
    assert extract_judgeme_product_id('"product_id": 8675663642945') == "8675663642945"
    assert extract_judgeme_product_id("no id here") is None


# --- Yotpo shop feed -------------------------------------------------------
def test_parse_yotpo_shop_feed_page_maps_ids_and_counts() -> None:
    page = parse_yotpo_shop_feed_page(
        {
            "products": [{"id": 1, "domainKey": "100", "name": "A"}, {"id": 2, "domainKey": "200", "name": "B"}],
            "reviews": [{"product_id": 1}, {"product_id": 1}, {"product_id": 2}],
            "pagination": {"page": 1, "perPage": 10, "total": 3},
        }
    )
    assert page.total_reviews == 3
    assert page.product_review_counts == {"100": 2, "200": 1}
    assert page.product_names == {"100": "A", "200": "B"}


def test_discover_yotpo_shop_feed_resolves_and_ranks() -> None:
    page1 = {
        "products": [{"id": 1, "domainKey": "100", "name": "A"}, {"id": 2, "domainKey": "200", "name": "B"}],
        "reviews": [{"product_id": 1}, {"product_id": 1}, {"product_id": 2}],
        "pagination": {"page": 1, "perPage": 10, "total": 3},
    }
    receipt = discover_yotpo_shop_feed(
        source_id="zgo",
        fetch_feed_page=lambda page: page1 if page == 1 else None,
        shopify_id_to_url={"100": "https://s/products/a", "200": "https://s/products/b"},
        max_pages=3,
        find_target=2,
    )
    assert [c.product_id for c in receipt.candidates] == ["100", "200"]  # 2 reviews before 1
    assert receipt.candidates[0].review_count == 2
    assert receipt.feed_total_reviews == 3
    assert receipt.vendor == "yotpo"


def test_discover_yotpo_shop_feed_unresolved_residual() -> None:
    page1 = {"products": [{"id": 1, "domainKey": "999", "name": "Z"}], "reviews": [{"product_id": 1}], "pagination": {"total": 1}}
    receipt = discover_yotpo_shop_feed(
        source_id="zgo",
        fetch_feed_page=lambda page: page1 if page == 1 else None,
        shopify_id_to_url={},
        max_pages=2,
        find_target=2,
    )
    assert receipt.candidates == []
    assert any("unresolved" in residual for residual in receipt.residuals)


# --- rate limiter ----------------------------------------------------------
def test_rate_limiter_policy_backoff_and_reset() -> None:
    policy = RateLimiterPolicy(min_interval_s=6.0, backoff_factor=2.0, max_interval_s=20.0)
    assert policy.interval_s == 6.0
    assert policy.on_throttle() == 12.0
    assert policy.on_throttle() == 20.0  # capped, not 24
    assert policy.on_ok() == 6.0


# --- Judge.me probe orchestration -----------------------------------------
def test_discover_judgeme_by_probe_finds_ranks_and_stops() -> None:
    refs = [
        ProductRef(product_url="u1", handle="h1", shopify_product_id="111111"),
        ProductRef(product_url="u2", handle="h2", shopify_product_id="222222"),
        ProductRef(product_url="u3", handle="excluded", shopify_product_id="333333"),
        ProductRef(product_url="u4", handle="h4", shopify_product_id="444444"),
    ]
    counts = {"111111": 0, "222222": 5, "444444": 3}
    receipt = discover_judgeme_by_probe(
        source_id="s",
        shop_domain="shop",
        product_refs=refs,
        fetch_count=lambda shop, pid: counts.get(pid, 0),
        sleeper=lambda _seconds: None,
        find_target=2,
        exclude_handles=["excluded"],
    )
    assert [c.product_id for c in receipt.candidates] == ["222222", "444444"]
    assert receipt.zero_count == 1
    assert receipt.probed == 3  # 111111, 222222, 444444 (excluded h3 skipped)


def test_discover_judgeme_by_probe_backs_off_on_throttle() -> None:
    refs = [ProductRef(product_url="u1", handle="h1", shopify_product_id="111111")]
    intervals: list[float] = []
    receipt = discover_judgeme_by_probe(
        source_id="s",
        shop_domain="shop",
        product_refs=refs,
        fetch_count=lambda shop, pid: THROTTLE,
        sleeper=intervals.append,
        policy=RateLimiterPolicy(min_interval_s=6.0, backoff_factor=2.0, max_interval_s=60.0),
        find_target=1,
    )
    assert receipt.throttled == 1
    assert receipt.candidates == []
    assert intervals == [12.0]
    assert "judgeme_probe_throttled_no_candidate" in receipt.residuals


def test_discover_judgeme_by_probe_resolves_missing_id() -> None:
    refs = [ProductRef(product_url="https://s/products/x", handle="x")]  # no shopify id (sitemap-only)
    receipt = discover_judgeme_by_probe(
        source_id="s",
        shop_domain="shop",
        product_refs=refs,
        fetch_count=lambda shop, pid: 4 if pid == "987654" else 0,
        sleeper=lambda _seconds: None,
        find_target=1,
        resolve_product_id=lambda ref: "987654",
    )
    assert [c.product_id for c in receipt.candidates] == ["987654"]
    assert receipt.missing_product_id == 0
