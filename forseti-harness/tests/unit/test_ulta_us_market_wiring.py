from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from runners import run_source_capture_cloakbrowser_packet as cloak_writer
from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess
from source_capture.adapters.ulta_us_market import (
    UltaUSMarketPlugin,
    confirm_ulta_us_market,
)
from source_capture.retail_capture_profiles import get_retail_capture_profile
from source_capture.retail_pdp_content import (
    ULTA_PDP_CONTENT_RECORD_KIND,
    build_ulta_pdp_aggregate_content_record,
)


_URL = (
    "https://www.ulta.com/p/night-shift-overnight-lip-mask-pimprod2046225"
    "?sku=2645443"
)
_SKU = "2645443"


def _dom(
    *,
    html_lang: str = "en-US",
    app_locale: str = "en-US",
    ulta_site: str = "en-us",
    placement_locale: str = "en_US",
    placement_currency: str = "USD",
    placement_amount: str = "12",
    product_sku: str = _SKU,
    offer_currency: str = "USD",
    offer_price: str = "12.00",
    apollo_modules: list[dict[str, Any]] | None = None,
    extra: str = "",
) -> str:
    product = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": "Night Shift Overnight Lip Mask - Watermelon",
        "productID": "pimprod2046225",
        "sku": product_sku,
        "offers": {
            "@type": "Offer",
            "availability": "https://schema.org/InStock",
            "price": offer_price,
            "priceCurrency": offer_currency,
            "url": _URL,
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": 4.3,
            "reviewCount": 671,
        },
    }
    apollo = {
        "ROOT_QUERY": {
            'Page({"moduleParams":{"sku":"2645443"}})': {
                "content": {
                    "modules": [
                        {
                            "skuId": "2645443",
                            "productId": "pimprod2046225",
                            "productName": "Night Shift Overnight Lip Mask",
                            "listPrice": "$12.00",
                            "availability": "InStock",
                            "rating": 4.3,
                            "reviewCount": 671,
                        }
                    ]
                    if apollo_modules is None
                    else apollo_modules
                }
            }
        }
    }
    return (
        f'<html lang="{html_lang}"><head>'
        f"<script>window.__APP_LOCALE__ = '{app_locale}';"
        "window.__GRAPHQL_URI__ = "
        f"'v1/client/dxl/graphql?ultasite={ulta_site}&User-Agent=gomez';"
        "</script>"
        '<script type="application/ld+json">'
        f"{json.dumps(product)}"
        "</script>"
        f"<script>window.__APOLLO_STATE__={json.dumps(apollo)}</script>"
        "</head><body>"
        '<square-placement data-page-type="product" '
        f'data-consumer-locale="{placement_locale}" '
        f'data-currency="{placement_currency}" data-amount="{placement_amount}">'
        "</square-placement>"
        f"{extra}</body></html>"
    )


_US_DOM = _dom()


def _fake_capture(
    *,
    dom: str = _US_DOM,
    final_url: str = _URL,
):
    def capture(**kwargs: Any) -> CloakBrowserSnapshotSuccess:
        pre_capture = kwargs["pre_capture"]
        assert isinstance(pre_capture, UltaUSMarketPlugin)
        confirmation = pre_capture.confirm(dom)
        return CloakBrowserSnapshotSuccess(
            requested_url=kwargs["url"],
            final_url=final_url,
            title="Night Shift Overnight Lip Mask",
            rendered_dom=dom,
            visible_text=(
                "ULTA Beauty Collection Night Shift Overnight Lip Mask "
                "Watermelon $12.00 671 Reviews In stock and ready to ship"
            ),
            screenshot_png=b"\x89PNG\r\n\x1a\n",
            metadata={
                "capture_timestamp": "2026-07-19T00:00:00Z",
                "requested_url": kwargs["url"],
                "final_url": final_url,
                "access_blocked": False,
                **pre_capture.describe(),
                "pin_confirmed": confirmation.confirmed,
            },
            warning_notes=[],
            limitation_notes=[],
        )

    return capture


def _run_kwargs(output: Path) -> dict[str, Any]:
    return {
        "url": _URL,
        "source_family": "retail_pdp",
        "source_surface": "cloakbrowser_snapshot",
        "decision_question": "Does the bound Ulta PDP confirm US/USD?",
        "output_directory": output,
        "capture_context": "offline test",
        "operator_category": "test",
        "capture_mode": cloak_writer.CaptureModeCategory.MULTIMODAL,
        "session_id": None,
        "proxy_profile": None,
        "actor_audience_context": cloak_writer.unknown_with_reason("not needed"),
        "visible_mode_changes": [],
        "source_publication_or_event": cloak_writer.unknown_with_reason("not needed"),
        "source_edit_or_version": cloak_writer.unknown_with_reason("not needed"),
        "cutoff_posture": cloak_writer.unknown_with_reason("not needed"),
        "recapture_time": cloak_writer.not_applicable("not needed"),
        "re_capture_relationship": cloak_writer.not_applicable("not needed"),
        "warnings": [],
        "limitations": [],
        "timeout_seconds": 30,
        "wait_until": "load",
        "viewport_width": 1920,
        "viewport_height": 1080,
        "max_artifact_bytes": 5_000_000,
        "block_heavy_assets": False,
        "ulta_market": "US",
    }


def test_confirmation_requires_bound_ulta_site_price_and_product_conjunction() -> None:
    confirmation = confirm_ulta_us_market(_US_DOM, expected_sku=_SKU)

    assert confirmation.confirmed is True
    assert "root/app/site state consistently bound en-US" in confirmation.detail
    assert f"SKU {_SKU}" in confirmation.detail


@pytest.mark.parametrize(
    "dom",
    [
        "<html><body>www.ulta.com US $12 USD 2645443</body></html>",
        _dom(html_lang="en-SG"),
        _dom(app_locale="en-SG"),
        _dom(ulta_site="en-sg"),
        _dom(extra="<script>window.__APP_LOCALE__='en-SG'</script>"),
        _dom(extra="<script>fetch('/graphql?ultasite=en-sg')</script>"),
        _dom(placement_locale="en_SG"),
        _dom(placement_currency="SGD"),
        _dom(placement_amount=""),
        _dom(product_sku="9999999"),
        _dom(offer_currency="SGD"),
        _dom(offer_price=""),
        (
            "<html lang='en-US'><script>window.__APP_LOCALE__='en-US';"
            "fetch('/graphql?ultasite=en-us')</script>"
            "<square-placement data-page-type='product' "
            "data-consumer-locale='en_US' data-currency='USD' data-amount='12'>"
            "</square-placement><script type='application/ld+json'>{broken}</script>"
            "</html>"
        ),
    ],
)
def test_confirmation_rejects_loose_split_conflicting_or_malformed_signals(
    dom: str,
) -> None:
    assert confirm_ulta_us_market(dom, expected_sku=_SKU).confirmed is False


def test_plugin_is_assertion_only_and_validates_exact_commissioned_url() -> None:
    plugin = UltaUSMarketPlugin(target_url=_URL, sku=_SKU)
    outcome = plugin.before(object(), setup_timeout_ms=1)

    assert outcome.attempted is True
    assert outcome.steps_completed is True
    assert plugin.humanize is False
    with pytest.raises(ValueError, match="matching the commissioned SKU"):
        UltaUSMarketPlugin(target_url=_URL, sku="9999999")
    with pytest.raises(ValueError, match="only US/USD"):
        UltaUSMarketPlugin(
            target_url=_URL,
            sku=_SKU,
            country_code="SG",
            currency_code="SGD",
        )


def test_writer_builds_ulta_plugin_and_accepts_confirmed_packet(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        cloak_writer,
        "fetch_cloakbrowser_snapshot_capture",
        _fake_capture(),
    )

    exit_code, output = cloak_writer.run_source_capture_cloakbrowser_packet(
        **_run_kwargs(tmp_path / "packet")
    )

    assert exit_code == 0
    assert output == str(tmp_path / "packet")
    metadata = json.loads(
        (tmp_path / "packet" / "raw" / "04_cloakbrowser_snapshot_metadata.json").read_text(
            encoding="utf-8"
        )
    )
    assert metadata["pin_confirmed"] is True
    assert metadata["product_sku_requested"] == _SKU


def test_ulta_aggregate_profile_defaults_to_lean_content(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        cloak_writer,
        "fetch_cloakbrowser_snapshot_capture",
        _fake_capture(),
    )
    kwargs = _run_kwargs(tmp_path / "content")
    kwargs["retail_capture_profile"] = get_retail_capture_profile(
        "ulta_pdp_aggregate"
    )

    exit_code, output = cloak_writer.run_source_capture_cloakbrowser_packet(
        **kwargs
    )

    assert exit_code == 0
    assert output == str(tmp_path / "content")
    manifest = json.loads((tmp_path / "content" / "manifest.json").read_text())
    names = {
        Path(item["relative_packet_path"]).name
        for item in manifest["preserved_files"]
    }
    assert any(name.endswith("content_record.json") for name in names)
    assert not any(name.endswith("rendered_dom.html") for name in names)
    assert not any(name.endswith("visible_text.txt") for name in names)
    record_path = next(
        tmp_path / "content" / item["relative_packet_path"]
        for item in manifest["preserved_files"]
        if item["relative_packet_path"].endswith("content_record.json")
    )
    record = json.loads(record_path.read_text(encoding="utf-8"))
    assert {
        row["row_kind"] for row in record["rows"]
    } >= {
        "retail_pdp_product",
        "retail_variant_offer",
        "retail_review_substrate",
    }
    assert all(
        row["row_kind"] != "retail_embedded_structured_json"
        for row in record["rows"]
    )


def test_ulta_content_is_deterministic_and_excludes_loader_baggage() -> None:
    reviews = [
        {
            "@type": "Review",
            "name": f"Review {index}",
            "reviewBody": f"Target review body {index}.",
            "datePublished": f"2026-07-0{index}",
            "author": {"@type": "Person", "name": f"Reviewer {index}"},
            "locationCreated": {
                "@type": "AdministrativeArea",
                "name": "New York, NY",
            },
            "reviewRating": {"@type": "Rating", "ratingValue": index + 3},
        }
        for index in (1, 2)
    ]
    target_product = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": "Night Shift Overnight Lip Mask - Watermelon",
        "description": "Target product description.",
        "brand": "ULTA Beauty Collection",
        "productID": "pimprod2046225",
        "sku": _SKU,
        "scent": "Watermelon",
        "offers": {
            "@type": "Offer",
            "availability": "https://schema.org/InStock",
            "price": "12.00",
            "priceCurrency": "USD",
            "url": _URL,
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": 4.3,
            "reviewCount": 671,
        },
        "review": reviews,
    }
    loader_padding = "not-valuable-loader-state-" * 5_000
    rendered_dom = _dom(
        extra=(
            '<script type="application/ld+json">'
            + json.dumps(target_product)
            + "</script><script>window.loaderPadding="
            + json.dumps(loader_padding)
            + "</script>"
            + "<section>Free standard shipping over $35.</section>"
            + "<section>Earn points with Rewards.</section>"
            + "<section>Make it a routine</section>"
        )
    ).encode()
    visible_text = (
        "Night Shift Overnight Lip Mask Watermelon $12.00 671 Reviews "
        "In stock and ready to ship"
    ).encode()

    first = build_ulta_pdp_aggregate_content_record(
        rendered_dom=rendered_dom,
        visible_text=visible_text,
        source_url=_URL,
    )
    second = build_ulta_pdp_aggregate_content_record(
        rendered_dom=rendered_dom,
        visible_text=visible_text,
        source_url=_URL,
    )

    assert first == second
    assert first["record_kind"] == ULTA_PDP_CONTENT_RECORD_KIND
    encoded = json.dumps(first, sort_keys=True)
    assert loader_padding not in encoded
    assert "raw_json_text" not in encoded
    assert "__APOLLO_STATE__" not in encoded
    review = next(
        row["source_visible_fields"]
        for row in first["rows"]
        if row["row_kind"] == "retail_review_substrate"
    )
    assert review["review_count"] == "671"
    assert review["displayed_review_body_count"] == 2
    assert [item["body"] for item in review["reviews"]] == [
        "Target review body 1.",
        "Target review body 2.",
    ]
    assert len(encoded.encode()) < len(rendered_dom)


def test_ulta_content_ignores_unrelated_recommendation_offer_and_reviews() -> None:
    recommendation = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": "Recommendation Product",
        "productID": "pimprod9999999",
        "sku": "9999999",
        "offers": {
            "@type": "Offer",
            "availability": "https://schema.org/InStock",
            "price": "99.00",
            "priceCurrency": "USD",
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": 1.0,
            "reviewCount": 9999,
        },
        "review": [
            {
                "@type": "Review",
                "name": "Unrelated",
                "reviewBody": "This review belongs to a recommendation.",
                "reviewRating": {"@type": "Rating", "ratingValue": 1},
            }
        ],
    }
    rendered_dom = _dom(
        apollo_modules=[
            {
                "skuId": "9999999",
                "productId": "pimprod9999999",
                "productName": "Recommendation Product",
                "listPrice": "$99.00",
                "availability": "InStock",
                "rating": 1.0,
                "reviewCount": 9999,
            },
            {
                "skuId": _SKU,
                "productId": "pimprod2046225",
                "productName": "Night Shift Overnight Lip Mask",
                "listPrice": "$12.00",
                "availability": "InStock",
                "rating": 4.3,
                "reviewCount": 671,
            },
        ],
        extra=(
            '<script type="application/ld+json">'
            + json.dumps(recommendation)
            + "</script>"
        ),
    ).encode()

    record = build_ulta_pdp_aggregate_content_record(
        rendered_dom=rendered_dom,
        visible_text=(
            b"Night Shift Overnight Lip Mask Watermelon $12.00 671 Reviews "
            b"In stock and ready to ship"
        ),
        source_url=_URL,
    )

    offer = next(
        row["source_visible_fields"]
        for row in record["rows"]
        if row["row_kind"] == "retail_variant_offer"
    )
    review = next(
        row["source_visible_fields"]
        for row in record["rows"]
        if row["row_kind"] == "retail_review_substrate"
    )
    assert offer["sku"] == _SKU
    assert offer["price"] == "12.00"
    assert review["review_count"] == "671"
    assert review["rating"] == "4.3"
    assert "Recommendation Product" not in json.dumps(record)
    assert "This review belongs to a recommendation." not in json.dumps(record)


def test_writer_preserves_typed_packet_and_exits_nonzero_when_pin_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        cloak_writer,
        "fetch_cloakbrowser_snapshot_capture",
        _fake_capture(dom="<html><body>www.ulta.com $12 USD</body></html>"),
    )

    kwargs = _run_kwargs(tmp_path / "failed")
    kwargs["retail_capture_profile"] = get_retail_capture_profile(
        "ulta_pdp_aggregate"
    )
    exit_code, message = cloak_writer.run_source_capture_cloakbrowser_packet(
        **kwargs
    )

    assert exit_code == cloak_writer.SOURCE_DETAIL_SUFFICIENCY_EXIT_CODE
    assert message.startswith("ulta_market_pin_failed: packet preserved")
    manifest = json.loads((tmp_path / "failed" / "manifest.json").read_text())
    assert "ulta_market_pin_failed" in manifest["visible_mode_changes"]
    assert any(
        "MUST NOT be admitted as Ulta US/USD storefront evidence" in limitation
        for limitation in manifest["limitations"]
    )
    names = {
        Path(item["relative_packet_path"]).name
        for item in manifest["preserved_files"]
    }
    assert any(name.endswith("rendered_dom.html") for name in names)
    assert any(name.endswith("visible_text.txt") for name in names)


def test_writer_rejects_final_host_drift_even_with_true_confirmation(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        cloak_writer,
        "fetch_cloakbrowser_snapshot_capture",
        _fake_capture(final_url="https://www.ulta.com.mx/p/example?sku=2645443"),
    )

    exit_code, message = cloak_writer.run_source_capture_cloakbrowser_packet(
        **_run_kwargs(tmp_path / "redirected")
    )

    assert exit_code == cloak_writer.SOURCE_DETAIL_SUFFICIENCY_EXIT_CODE
    assert "not ulta.com" in message


def test_writer_rejects_invalid_ulta_route_and_site_plugin_overlap(
    tmp_path: Path,
) -> None:
    kwargs = _run_kwargs(tmp_path / "invalid")
    kwargs["url"] = "https://www.ulta.com/p/example"
    with pytest.raises(ValueError, match="exactly one numeric sku"):
        cloak_writer.run_source_capture_cloakbrowser_packet(**kwargs)

    kwargs = _run_kwargs(tmp_path / "overlap")
    kwargs["sephora_market"] = "US"
    with pytest.raises(ValueError, match="only one site-specific pre-capture"):
        cloak_writer.run_source_capture_cloakbrowser_packet(**kwargs)
