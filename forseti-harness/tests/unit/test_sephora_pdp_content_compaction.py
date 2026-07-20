from __future__ import annotations

import json

import pytest

from runners.run_source_capture_cloakbrowser_packet import (
    _sephora_content_extraction_spec,
)
from source_capture.content_extraction import RenderedContentExtractionSpec
from source_capture.retail_pdp_projection import (
    SEPHORA_PDP_CONTENT_SCHEMA_VERSION,
    SEPHORA_PDP_PARSER_VERSION,
    build_sephora_pdp_aggregate_content_record,
)


SOURCE_URL = (
    "https://www.sephora.com/product/lip-sleeping-mask-P420652"
    "?country_switch=us&lang=en"
)


def _synthetic_product() -> dict:
    current_sku = {
        "skuId": "2961324",
        "variationValue": "Berry",
        "isOutOfStock": False,
        "futureSkuFact": {"sourceValue": "kept"},
    }
    return {
        "productId": "P420652",
        "currentSku": current_sku,
        "regularChildSkus": [
            current_sku,
            {
                "skuId": "2961325",
                "variationValue": "Mango",
                "isOutOfStock": True,
                "isLimitedEdition": True,
            },
        ],
        "productDetails": {"longDescription": "Overnight lip care."},
        "reviewFilters": [{"id": "skinType", "values": ["Dry"]}],
        "sentiments": [{"label": "Softness", "count": 7, "polarity": "positive"}],
        "reviewImages": [{"id": "image-1", "url": "https://example.test/review.jpg"}],
        "futureRootFact": {
            "nested": ["this must survive a Sephora page-shape change"]
        },
    }


def _synthetic_sephora_html() -> bytes:
    product = _synthetic_product()
    product_ld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "productID": "P420652",
        "sku": "2961324",
        "name": "Lip Sleeping Mask",
        "offers": {
            "@type": "Offer",
            "price": "24.00",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
        },
    }
    return (
        "<html><body>"
        f'<script type="application/ld+json">{json.dumps(product_ld)}</script>'
        f'<script id="linkStore">{json.dumps({"page": {"product": product}})}</script>'
        '<div data-comp="ProductPage " data-cnstrc-item-id="P420652" '
        'data-cnstrc-item-variation-id="2961324" '
        'data-cnstrc-item-price="$24.00"></div>'
        '<div data-comp="Review ">Five stars. Soft and comfortable.</div>'
        '<div data-comp="Question ">Can I use this nightly?</div>'
        '<div data-comp="Answer ">Yes, apply before bed.</div>'
        "</body></html>"
    ).encode("utf-8")


def _row(record: dict, *, kind: str | None = None, structured: str | None = None) -> dict:
    return next(
        row
        for row in record["rows"]
        if (kind is None or row["row_kind"] == kind)
        and (
            structured is None
            or row["source_visible_fields"].get("structured_json_kind")
            == structured
        )
    )


def test_sephora_v3_deduplicates_without_losing_source_fields() -> None:
    record = build_sephora_pdp_aggregate_content_record(
        rendered_dom=_synthetic_sephora_html(),
        visible_text=b"Lip Sleeping Mask\nBerry\n$24.00\nFive stars.",
        source_url=SOURCE_URL,
    )

    assert record["schema_version"] == SEPHORA_PDP_CONTENT_SCHEMA_VERSION
    assert record["parser_version"] == SEPHORA_PDP_PARSER_VERSION

    product_source = _row(
        record,
        structured="sephora_link_store_product",
    )["source_visible_fields"]
    variant = _row(record, kind="retail_variant_offer")["source_visible_fields"]
    reviews = _row(record, kind="retail_review_substrate")["source_visible_fields"]
    interactions = _row(
        record,
        structured="sephora_rendered_interactions",
    )["source_visible_fields"]

    assert "raw_json_text" not in product_source
    assert "raw_json_text" not in interactions
    assert product_source["additional_source_fields"]["futureRootFact"] == {
        "nested": ["this must survive a Sephora page-shape change"]
    }
    assert variant["selected_variant_state"]["futureSkuFact"] == {
        "sourceValue": "kept"
    }
    assert variant["variant_count"] == 2
    assert reviews["displayed_review_rows"][0]["visible_text"] == (
        "Five stars. Soft and comfortable."
    )
    assert interactions["displayed_questions"][0]["visible_text"] == (
        "Can I use this nightly?"
    )
    assert interactions["displayed_answers"][0]["visible_text"] == (
        "Yes, apply before bed."
    )
    assert "displayed_reviews" not in interactions

    reconstructed = dict(product_source["additional_source_fields"])
    reconstructed.update(
        {
            "currentSku": variant["selected_variant_state"],
            "regularChildSkus": variant["all_variant_states"],
            "productDetails": variant["product_details_state"],
            "reviewFilters": reviews["review_filters"],
            "sentiments": reviews["review_sentiments"],
            "reviewImages": reviews["review_images"],
        }
    )
    assert reconstructed == _synthetic_product()


def test_sephora_content_route_writes_compact_json_only_for_sephora() -> None:
    spec = _sephora_content_extraction_spec("content")
    assert spec.json_indent is None

    ordinary = RenderedContentExtractionSpec(
        requested_retention_mode="content",
        extractor_version="test",
        extractor=lambda _dom, _text, _url: {},
    )
    assert ordinary.json_indent == 2

    with pytest.raises(ValueError, match="json_indent"):
        RenderedContentExtractionSpec(
            requested_retention_mode="content",
            extractor_version="test",
            extractor=lambda _dom, _text, _url: {},
            json_indent=-1,
        )
