from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot
from source_capture.models import known_fact
from source_capture.retail_pdp_projection import (
    AMAZON_PDP_PARSER_VERSION,
    LUCKYSCENT_PDP_PARSER_VERSION,
    TARGET_PDP_PARSER_VERSION,
    ULTA_PDP_PARSER_VERSION,
    build_luckyscent_pdp_aggregate_content_record,
)
from source_capture.retail_pdp_silver import derive_retail_pdp_silver
from source_capture.writer import write_local_source_capture_packet


_URL = "https://www.luckyscent.com/products/bread-and-roses-by-pearfat-parfum"
_ULTA_URL = (
    "https://www.ulta.com/p/night-shift-overnight-lip-mask-pimprod2046225"
    "?sku=2645443"
)
_TARGET_URL = "https://www.target.com/p/-/A-80184023"
_AMAZON_URL = "https://www.amazon.com/Laneige-Sleeping-Berry/dp/B07XXPHQZK"


def _json_file(path: Path, value: object) -> Path:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def test_current_content_flows_directly_through_cleaning_to_retail_silver(
    tmp_path: Path,
) -> None:
    content = {
        "record_kind": "retail_pdp_luckyscent_aggregate_content",
        "schema_version": "retail_pdp_luckyscent_aggregate_content_v1",
        "parser_version": LUCKYSCENT_PDP_PARSER_VERSION,
        "capture_profile": "luckyscent_pdp_aggregate",
        "source_url": _URL,
        "rows": [
            {
                "slice_id": "slice_01",
                "row_id": "product",
                "row_kind": "retail_pdp_product",
                "retailer": "luckyscent",
                "source_visible_fields": {"name": "Bread and Roses"},
                "residuals": [],
                "source_anchor_kind": "file",
            },
            {
                "slice_id": "slice_01",
                "row_id": "offer",
                "row_kind": "retail_variant_offer",
                "retailer": "luckyscent",
                "source_visible_fields": {
                    "product_id": "shopify_ZZ_9980138127681",
                    "price": "120.0",
                    "price_currency": "USD",
                    "availability": "InStock",
                    "seller": "Luckyscent",
                },
                "residuals": [],
                "source_anchor_kind": "file",
            },
            {
                "slice_id": "slice_01",
                "row_id": "reviews",
                "row_kind": "retail_review_substrate",
                "retailer": "luckyscent",
                "source_visible_fields": {
                    "review_count": "8",
                    "displayed_rating": "3.8",
                    "structured_rating": "3.75",
                },
                "residuals": [],
                "source_anchor_kind": "file",
            },
        ],
        "binding_map": [],
        "loss_ledger": {
            "collapsed": [],
            "preserved_evidence_rows": 3,
            "preserved_bindings": 0,
            "hierarchy_preserved": True,
            "structure_preserved": True,
        },
        "residuals": [],
    }
    extraction_metadata = {
        "extractor_version": LUCKYSCENT_PDP_PARSER_VERSION,
        "extraction_status": "succeeded",
        "retention_outcome": "content",
    }
    browser_metadata = {
        "retail_capture_profile": {"name": "luckyscent_pdp_aggregate"},
        "pin_confirmed": True,
    }
    inputs = [
        _json_file(tmp_path / "content_record.json", content),
        _json_file(
            tmp_path / "content_extraction_metadata.json", extraction_metadata
        ),
        _json_file(
            tmp_path / "cloakbrowser_snapshot_metadata.json", browser_metadata
        ),
    ]
    root = DataLakeRoot.for_test(tmp_path / "lake")
    written = write_local_source_capture_packet(
        data_root=root,
        input_files=inputs,
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        source_locator=known_fact(_URL),
        decision_question="What source-visible product facts are present?",
        capture_context="Direct content-to-Cleaning Retail Silver unit proof",
    )

    result = derive_retail_pdp_silver(
        data_root=root,
        packet_id=written.packet.packet_id,
    )

    assert result.cleaning_basis == "content_record"
    assert [record["payload_kind"] for record in result.records] == [
        "ProductEntity",
        "RetailOfferObservation",
        "RetailReviewAggregateObservation",
    ]
    for record in result.records:
        for source_ref in record["raw_refs"]:
            assert source_ref["anchor"]["kind"] == "json_pointer"
            assert source_ref["anchor"]["value"].startswith("/rows/")
            assert source_ref["relative_packet_path"].endswith(
                "content_record.json"
            )
        assert record["derived_refs"] == []


def test_luckyscent_content_accepts_current_single_product_group_shape() -> None:
    variants = [
        {
            "@type": "Product",
            "name": f"Bread and Roses - {size}",
            "size": size,
            "sku": sku,
            "url": f"{_URL}?variant={index}",
            "offers": {
                "@type": "Offer",
                "price": price,
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
                "seller": {"@type": "Organization", "name": "Luckyscent"},
            },
        }
        for index, (size, sku, price) in enumerate(
            (
                ("50ml", "1016005", "120.0"),
                ("15ml", "1016005_R", "45.0"),
                ("1ml spray", "1016005_S", "5.0"),
            ),
            start=1,
        )
    ]
    product_group = {
        "@context": "https://schema.org",
        "@type": "ProductGroup",
        "productGroupID": "shopify_ZZ_9980138127681",
        "name": "Bread and Roses",
        "description": "Fresh baguette, warm spice, and red rose petals.",
        "url": _URL,
        "brand": {"@type": "Brand", "name": "Pearfat Parfum"},
        "hasVariant": variants,
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": 3.75,
            "reviewCount": 8,
        },
    }
    histogram = "".join(
        '<div class="jdgm-histogram__row" '
        f'data-rating="{stars}" data-frequency="{count}" '
        f'data-percentage="{percent}"></div>'
        for stars, count, percent in (
            (5, 4, 50),
            (4, 1, 13),
            (3, 0, 0),
            (2, 3, 38),
            (1, 0, 0),
        )
    )
    reviews = "".join(
        '<div class="jdgm-rev jdgm-divider-top jdgm--done-setup" '
        'data-verified-buyer="true" '
        f'data-review-id="review-{index}" '
        'data-product-title="Bread and Roses" '
        'data-product-url="/products/bread-and-roses-by-pearfat-parfum">'
        f'<span class="jdgm-rev__rating" data-score="{5 if index < 5 else 2}"></span>'
        f'<span class="jdgm-rev__timestamp" data-content="2026-07-{index:02d} '
        f'00:00:00 UTC">07/{index:02d}/2026</span>'
        f'<span class="jdgm-rev__author">Reviewer {index}</span>'
        f'<div class="jdgm-rev__body"><p>Target review body {index}.</p></div>'
        "</div>"
        for index in range(1, 9)
    )
    rendered_dom = (
        "<html><head><script type=\"application/ld+json\">"
        + json.dumps(product_group, separators=(",", ":"))
        + "</script></head><body>"
        + histogram
        + reviews
        + '<div class="jdgm-paginate"></div></body></html>'
    ).encode()
    visible_text = b"""
Bread and Roses
Pearfat Parfum
3.8
(8)
$120
Size: 50ml
50ml
15ml
1ml Spray Sample
Add to Cart
Fragrance Notes
Fresh Baguette, Sweet Orange, Familiar Warmth, Red Rose Petals
Fragrance Style
Floral, Gourmand, Spicy
Customer Reviews
3.75 out of 5
"""

    record = build_luckyscent_pdp_aggregate_content_record(
        rendered_dom=rendered_dom,
        visible_text=visible_text,
        source_url=_URL,
    )

    structured_rows = [
        row
        for row in record["rows"]
        if row["row_kind"] == "retail_embedded_structured_json"
    ]
    assert len(structured_rows) == 1
    offer = next(
        row
        for row in record["rows"]
        if row["row_kind"] == "retail_variant_offer"
    )["source_visible_fields"]
    assert [variant["price"] for variant in offer["variants"]] == [
        "120.0",
        "45.0",
        "5.0",
    ]
    review = next(
        row
        for row in record["rows"]
        if row["row_kind"] == "retail_review_substrate"
    )["source_visible_fields"]
    assert review["structured_rating"] == "3.75"
    assert len(review["reviews"]) == 8


def test_ulta_content_flows_directly_through_cleaning_to_retail_silver(
    tmp_path: Path,
) -> None:
    content = {
        "record_kind": "retail_pdp_ulta_aggregate_content",
        "schema_version": "retail_pdp_ulta_aggregate_content_v2",
        "parser_version": ULTA_PDP_PARSER_VERSION,
        "capture_profile": "ulta_pdp_aggregate",
        "source_url": _ULTA_URL,
        "variant_module_state": "not_exposed",
        "rows": [
            {
                "slice_id": "slice_01",
                "row_id": "ulta_product_module_subtree",
                "row_kind": "retail_product_module_subtree",
                "retailer": "ulta",
                "source_visible_fields": {
                    "module_subtree": [
                        {
                            "skuId": "2645443",
                            "productId": "pimprod2046225",
                            "listPrice": "$12.00",
                        }
                    ],
                    "module_inventory": [
                        {
                            "source_order": 0,
                            "module_name": None,
                            "retained": True,
                            "byte_size": 64,
                            "contains_target_binding": True,
                            "exclusion_reason": None,
                        }
                    ],
                    "retained_module_names": [],
                    "page_data_capture": None,
                    "seo": None,
                    "redactions": {"count": 0, "paths": [], "marker": "[REDACTED_PAGE_DECLARED_PUBLIC_DISPLAY_KEY]"},
                    "retention_rule": "target-bound Apollo product modules retained verbatim",
                },
                "residuals": [],
                "source_anchor_kind": "script_index",
                "source_anchor_value": "apollo_state Page.content.modules",
            },
            {
                "slice_id": "slice_01",
                "row_id": "product",
                "row_kind": "retail_pdp_product",
                "retailer": "ulta",
                "source_visible_fields": {
                    "product_id": "pimprod2046225",
                    "sku": "2645443",
                    "product_name": "Night Shift Overnight Lip Mask - Watermelon",
                    "brand": "ULTA Beauty Collection",
                },
                "residuals": [],
                "source_anchor_kind": "script_index",
                "source_anchor_value": "ld_json Product sku=2645443",
            },
            {
                "slice_id": "slice_01",
                "row_id": "offer",
                "row_kind": "retail_variant_offer",
                "retailer": "ulta",
                "source_visible_fields": {
                    "product_id": "pimprod2046225",
                    "sku": "2645443",
                    "price": "12.00",
                    "price_currency": "USD",
                    "availability": "InStock",
                },
                "residuals": [],
                "source_anchor_kind": "script_index",
                "source_anchor_value": "apollo_state",
            },
            {
                "slice_id": "slice_01",
                "row_id": "reviews",
                "row_kind": "retail_review_substrate",
                "retailer": "ulta",
                "source_visible_fields": {
                    "review_count": "671",
                    "rating": "4.3",
                    "displayed_review_body_count": 1,
                    "reviews": [
                        {
                            "title": "Hydrating",
                            "body": "Target-bound review body.",
                            "rating": "5",
                        }
                    ],
                },
                "residuals": [],
                "source_anchor_kind": "script_index",
                "source_anchor_value": "ld_json/apollo_state review modules",
            },
        ],
        "residuals": [],
    }
    extraction_metadata = {
        "extractor_version": ULTA_PDP_PARSER_VERSION,
        "extraction_status": "succeeded",
        "retention_outcome": "content",
    }
    browser_metadata = {
        "retail_capture_profile": {"name": "ulta_pdp_aggregate"},
        "pin_confirmed": True,
    }
    inputs = [
        _json_file(tmp_path / "content_record.json", content),
        _json_file(
            tmp_path / "content_extraction_metadata.json", extraction_metadata
        ),
        _json_file(
            tmp_path / "cloakbrowser_snapshot_metadata.json", browser_metadata
        ),
    ]
    root = DataLakeRoot.for_test(tmp_path / "lake")
    written = write_local_source_capture_packet(
        data_root=root,
        input_files=inputs,
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        source_locator=known_fact(_ULTA_URL),
        decision_question="What source-visible Ulta product facts are present?",
        capture_context="Direct Ulta content-to-Cleaning Retail Silver proof",
    )

    result = derive_retail_pdp_silver(
        data_root=root,
        packet_id=written.packet.packet_id,
    )

    assert result.cleaning_basis == "content_record"
    assert [record["payload_kind"] for record in result.records] == [
        "ProductEntity",
        "RetailOfferObservation",
        "RetailReviewAggregateObservation",
    ]
    for record in result.records:
        for source_ref in record["raw_refs"]:
            assert source_ref["anchor"]["kind"] == "json_pointer"
            assert source_ref["anchor"]["value"].startswith("/rows/")
            assert source_ref["relative_packet_path"].endswith(
                "content_record.json"
            )


@pytest.mark.parametrize(
    ("pin_confirmed", "pre_capture_attempted"),
    ((True, True), (None, False)),
)
def test_target_content_flows_directly_through_cleaning_to_retail_silver(
    tmp_path: Path,
    pin_confirmed: bool | None,
    pre_capture_attempted: bool,
) -> None:
    content = {
        "record_kind": "retail_pdp_target_aggregate_content",
        "schema_version": "retail_pdp_target_aggregate_content_v1",
        "parser_version": TARGET_PDP_PARSER_VERSION,
        "capture_profile": "target_pdp_aggregate",
        "source_url": _TARGET_URL,
        "tcin": "80184023",
        "offer_module_state": "hydrated_in_rendered_dom",
        "variant_module_state": "not_exposed",
        "rows": [
            {
                "slice_id": "slice_01",
                "row_id": "product",
                "row_kind": "retail_pdp_product",
                "retailer": "target",
                "source_visible_fields": {
                    "product_id": "80184023",
                    "tcin": "80184023",
                    "dpci": "037-14-0466",
                    "product_name": "Naturium Vitamin C Complex Serum- 1 fl oz",
                    "brand_name": "Naturium",
                },
                "residuals": [],
                "source_anchor_kind": "script_index",
                "source_anchor_value": "__NEXT_DATA__ CDUI core tcin=80184023",
            },
            {
                "slice_id": "slice_01",
                "row_id": "offer",
                "row_kind": "retail_variant_offer",
                "retailer": "target",
                "source_visible_fields": {
                    "product_id": "80184023",
                    "sku": "80184023",
                    "price": "14.69",
                    "price_currency": "USD",
                    "availability": "pickup=Ready within 2 hours",
                    "seller": "Target",
                },
                "residuals": [],
                "source_anchor_kind": "html_selector",
                "source_anchor_value": "rendered PDP price/fulfillment region",
            },
            {
                "slice_id": "slice_01",
                "row_id": "reviews",
                "row_kind": "retail_review_substrate",
                "retailer": "target",
                "source_visible_fields": {
                    "rating": "4.45",
                    "rating_count": "1771",
                    "review_count": "758",
                    "structured_review_count": "758",
                    "filtered_review_count": "757",
                    "review_body_retention": (
                        "bodies_not_retained; owned by "
                        "target_bazaarvoice_onboarding companion"
                    ),
                },
                "residuals": [],
                "source_anchor_kind": "html_selector",
                "source_anchor_value": "rendered review widget + page state",
            },
            {
                "slice_id": "slice_01",
                "row_id": "target_product_module_subtree",
                "row_kind": "retail_product_module_subtree",
                "retailer": "target",
                "source_visible_fields": {
                    "ingredients": "Water (Aqua), Glycerin",
                    "alternate_image_count": 11,
                },
                "residuals": [],
                "source_anchor_kind": "script_index",
                "source_anchor_value": "__NEXT_DATA__ CDUI core product.item",
            },
            {
                "slice_id": "slice_01",
                "row_id": "target_review_identity_000",
                "row_kind": "retail_review_identity",
                "retailer": "target",
                "source_visible_fields": {
                    "target_native_review_id": "2e6c916e-2add-4efb-b36c-3cdac72a276b",
                    "body_present": True,
                    "body_retained_here": False,
                },
                "residuals": [],
                "source_anchor_kind": "script_index",
                "source_anchor_value": "__NEXT_DATA__ ratings_and_reviews.most_recent[0]",
            },
        ],
        "residuals": ["target_review_bodies_not_retained_companion_owns_them"],
    }
    extraction_metadata = {
        "extractor_version": TARGET_PDP_PARSER_VERSION,
        "extraction_status": "succeeded",
        "retention_outcome": "content",
    }
    browser_metadata = {
        "retail_capture_profile": {"name": "target_pdp_aggregate"},
        "pin_confirmed": pin_confirmed,
        "pre_capture_attempted": pre_capture_attempted,
    }
    inputs = [
        _json_file(tmp_path / "content_record.json", content),
        _json_file(
            tmp_path / "content_extraction_metadata.json", extraction_metadata
        ),
        _json_file(
            tmp_path / "cloakbrowser_snapshot_metadata.json", browser_metadata
        ),
    ]
    root = DataLakeRoot.for_test(tmp_path / "lake")
    written = write_local_source_capture_packet(
        data_root=root,
        input_files=inputs,
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        source_locator=known_fact(_TARGET_URL),
        decision_question="What source-visible Target product facts are present?",
        capture_context="Direct Target content-to-Cleaning Retail Silver proof",
    )

    result = derive_retail_pdp_silver(
        data_root=root,
        packet_id=written.packet.packet_id,
    )

    assert result.cleaning_basis == "content_record"
    assert [record["payload_kind"] for record in result.records] == [
        "ProductEntity",
        "RetailOfferObservation",
        "RetailReviewAggregateObservation",
    ]
    for record in result.records:
        for source_ref in record["raw_refs"]:
            assert source_ref["anchor"]["kind"] == "json_pointer"
            assert source_ref["anchor"]["value"].startswith("/rows/")
            assert source_ref["relative_packet_path"].endswith(
                "content_record.json"
            )


@pytest.mark.parametrize(
    ("pin_confirmed", "pre_capture_attempted"),
    ((True, True), (None, False)),
)
def test_amazon_content_flows_directly_through_cleaning_to_retail_silver(
    tmp_path: Path,
    pin_confirmed: bool | None,
    pre_capture_attempted: bool,
) -> None:
    content = {
        "record_kind": "retail_pdp_amazon_aggregate_content",
        "schema_version": "retail_pdp_amazon_aggregate_content_v1",
        "parser_version": AMAZON_PDP_PARSER_VERSION,
        "capture_profile": "amazon_pdp_aggregate",
        "review_provider": "amazon_native_rendered_pdp",
        "review_body_retention": "exact_bodies_retained_in_this_record",
        "source_url": _AMAZON_URL,
        "asin": "B07XXPHQZK",
        "offer_module_state": "hydrated_in_rendered_dom",
        "variant_module_state": "observed",
        "ai_review_summary_state": "not_exposed_on_target_pdp",
        "customer_q_and_a_state": "not_exposed_on_target_pdp",
        "rows": [
            {
                "slice_id": "slice_01",
                "row_id": "product",
                "row_kind": "retail_pdp_product",
                "retailer": "amazon",
                "source_visible_fields": {
                    "product_id": "B07XXPHQZK",
                    "asin": "B07XXPHQZK",
                    "product_name": "LANEIGE Lip Sleeping Mask",
                    "brand_logo_title": "LANEIGE",
                },
                "residuals": [],
                "source_anchor_kind": "html_selector",
                "source_anchor_value": "#productTitle data-csa-c-asin=B07XXPHQZK",
            },
            {
                "slice_id": "slice_01",
                "row_id": "offer",
                "row_kind": "retail_variant_offer",
                "retailer": "amazon",
                "source_visible_fields": {
                    "product_id": "B07XXPHQZK",
                    "sku": "B07XXPHQZK",
                    "price": "24.00",
                    "price_currency": "USD",
                    "availability": "In Stock",
                    "seller": "Amazon.com",
                    "bought_in_past_month": "70K+ bought in past month",
                },
                "residuals": [],
                "source_anchor_kind": "html_selector",
                "source_anchor_value": "target-ASIN-bound corePrice module",
            },
            {
                "slice_id": "slice_01",
                "row_id": "reviews",
                "row_kind": "retail_review_substrate",
                "retailer": "amazon",
                "source_visible_fields": {
                    "rating": "4.6",
                    "rating_count": "37,045",
                    "captured_review_rows": 13,
                    "review_body_retention": "exact_bodies_retained_in_this_record",
                },
                "residuals": [],
                "source_anchor_kind": "html_selector",
                "source_anchor_value": "#averageCustomerReviews + #histogramTable",
            },
            {
                "slice_id": "slice_01",
                "row_id": "amazon_product_module_subtree",
                "row_kind": "retail_product_module_subtree",
                "retailer": "amazon",
                "source_visible_fields": {
                    "feature_bullet_count": 4,
                    "image_reference_count": 30,
                },
                "residuals": [],
                "source_anchor_kind": "html_selector",
                "source_anchor_value": "#feature-bullets + #detailBullets_feature_div",
            },
            {
                "slice_id": "slice_01",
                "row_id": "amazon_review_row_000",
                "row_kind": "retail_review_row",
                "retailer": "amazon",
                "source_visible_fields": {
                    "review_id": "R1S7HOZY4X45ZI",
                    "body": "Thick, nourishing, and it lasts a long time.",
                    "body_retained_here": True,
                    "author": "HonesTee",
                },
                "residuals": [],
                "source_anchor_kind": "html_selector",
                "source_anchor_value": '#R1S7HOZY4X45ZI[data-hook="review"]',
            },
        ],
        "residuals": [
            "amazon_route_is_amazon_native_rendered_pdp_and_is_not_bazaarvoice"
        ],
    }
    extraction_metadata = {
        "extractor_version": AMAZON_PDP_PARSER_VERSION,
        "extraction_status": "succeeded",
        "retention_outcome": "content",
    }
    browser_metadata = {
        "retail_capture_profile": {"name": "amazon_pdp_aggregate"},
        "pin_confirmed": pin_confirmed,
        "pre_capture_attempted": pre_capture_attempted,
    }
    inputs = [
        _json_file(tmp_path / "content_record.json", content),
        _json_file(
            tmp_path / "content_extraction_metadata.json", extraction_metadata
        ),
        _json_file(
            tmp_path / "cloakbrowser_snapshot_metadata.json", browser_metadata
        ),
    ]
    root = DataLakeRoot.for_test(tmp_path / "lake")
    written = write_local_source_capture_packet(
        data_root=root,
        input_files=inputs,
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        source_locator=known_fact(_AMAZON_URL),
        decision_question="What source-visible Amazon product facts are present?",
        capture_context="Direct Amazon content-to-Cleaning Retail Silver proof",
    )

    result = derive_retail_pdp_silver(
        data_root=root,
        packet_id=written.packet.packet_id,
    )

    assert result.cleaning_basis == "content_record"
    assert [record["payload_kind"] for record in result.records] == [
        "ProductEntity",
        "RetailOfferObservation",
        "RetailReviewAggregateObservation",
    ]
    for record in result.records:
        for source_ref in record["raw_refs"]:
            assert source_ref["anchor"]["kind"] == "json_pointer"
            assert source_ref["anchor"]["value"].startswith("/rows/")
            assert source_ref["relative_packet_path"].endswith(
                "content_record.json"
            )
