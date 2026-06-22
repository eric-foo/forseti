from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from runners import run_retail_pdp_projection as retail_projection_runner
from source_capture.models import (
    CaptureModeCategory,
    PacketTiming,
    PreservedFile,
    ReceiptMetadata,
    SourceCapturePacket,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.retail_pdp_projection import (
    RETAIL_PDP_PROJECTION_CERTIFICATION,
    RetailPdpProjectionInputError,
    RetailPdpProjectionRow,
    RetailProjectionRawAnchor,
    RetailProjectionRawRef,
    build_retail_pdp_projection,
    build_retail_pdp_projection_from_packet_directory,
    write_retail_pdp_projection,
)


def _timing() -> PacketTiming:
    return PacketTiming(
        source_publication_or_event=unknown_with_reason("retail PDP fixture does not supply source event timing"),
        source_edit_or_version=unknown_with_reason("retail PDP fixture does not supply edit timing"),
        capture_time=known_fact("2026-06-16T00:00:00Z"),
        recapture_time=not_applicable("first capture"),
        cutoff_posture=unknown_with_reason("test fixture has no decision cutoff"),
    )


def _packet(
    *,
    retailer: str,
    locator: str,
    series_id: str,
    variant_pin: str | None = None,
) -> SourceCapturePacket:
    timing = _timing()
    return SourceCapturePacket(
        packet_id=f"01TESTRETAIL{retailer.upper()}",
        manifest_version="source_capture_packet_manifest_v1",
        obligation_contract_version="core_spine_v0_data_capture_spine_obligation_contract_v0",
        source_family="web_page",
        source_surface="cloakbrowser_snapshot",
        source_locator=known_fact(locator),
        requested_decision_context=known_fact(f"Demand-durability series slot 0: {retailer} US PDP."),
        capture_context=known_fact("unit test packet"),
        actor_audience_context=unknown_with_reason("not supplied by fixture"),
        capture_mode=CaptureModeCategory.MULTIMODAL,
        operator_category="unit_test",
        session_identity="01TESTSESSION",
        timing=timing,
        access_posture=known_fact("rendered DOM fixture supplied"),
        archive_history_posture=not_attempted("archive not queried"),
        media_modality_posture=not_attempted("screenshot not supplied"),
        re_capture_relationship=not_applicable("first capture"),
        series_id=series_id,
        intended_cadence={"mode": "fixed", "slot_count": 3},
        source_slices=[
            SourceCaptureSlice(
                slice_id="cloakbrowser_snapshot_01",
                locator=known_fact(locator),
                timing=timing,
                access_posture=known_fact("rendered DOM fixture supplied"),
                archive_history_posture=not_attempted("archive not queried"),
                media_modality_posture=not_attempted("screenshot not supplied"),
                re_capture_relationship=not_applicable("first capture"),
                locale_pin=known_fact("en-US"),
                currency_pin=known_fact("USD"),
                variant_pin=known_fact(variant_pin) if variant_pin else None,
                limitations=[],
                warning_notes=[],
                preserved_file_ids=["file_01", "file_02"],
            )
        ],
        preserved_files=[
            PreservedFile(
                file_id="file_01",
                original_path="rendered_dom.html",
                relative_packet_path="raw/01_cloakbrowser_rendered_dom.html",
                sha256="htmlsha",
                hash_basis="raw_stored_bytes",
                size_bytes=123,
            ),
            PreservedFile(
                file_id="file_02",
                original_path="visible_text.txt",
                relative_packet_path="raw/02_cloakbrowser_visible_text.txt",
                sha256="textsha",
                hash_basis="raw_stored_bytes",
                size_bytes=123,
            ),
        ],
        receipt_metadata=ReceiptMetadata(
            title="Source Capture Packet Receipt",
            generated_at="2026-06-16T00:00:00Z",
            summary="unit test packet",
            non_claims=["not Cleaning", "not Judgment"],
        ),
    )


def _projection(
    *,
    packet: SourceCapturePacket,
    html: str,
    visible_text: str,
):
    return build_retail_pdp_projection(
        packet=packet,
        raw_file_bytes_by_file_id={"file_01": html.encode("utf-8"), "file_02": visible_text.encode("utf-8")},
    )


def _packet_with_file_bytes(
    packet: SourceCapturePacket,
    raw_file_bytes_by_file_id: dict[str, bytes],
) -> SourceCapturePacket:
    return packet.model_copy(
        update={
            "preserved_files": [
                preserved_file.model_copy(
                    update={
                        "sha256": hashlib.sha256(raw_file_bytes_by_file_id[preserved_file.file_id]).hexdigest(),
                        "size_bytes": len(raw_file_bytes_by_file_id[preserved_file.file_id]),
                    }
                )
                for preserved_file in packet.preserved_files
            ]
        }
    )


def _write_packet_directory(
    tmp_path: Path,
    packet: SourceCapturePacket,
    raw_file_bytes_by_file_id: dict[str, bytes],
) -> tuple[Path, SourceCapturePacket]:
    packet = _packet_with_file_bytes(packet, raw_file_bytes_by_file_id)
    packet_dir = tmp_path / "packet"
    for preserved_file in packet.preserved_files:
        file_path = packet_dir / preserved_file.relative_packet_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(raw_file_bytes_by_file_id[preserved_file.file_id])
    (packet_dir / "manifest.json").write_text(
        f"{json.dumps(packet.model_dump(mode='json'), indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )
    return packet_dir, packet


def _sephora_projection_packet_dir(tmp_path: Path) -> tuple[Path, SourceCapturePacket]:
    packet = _packet(
        retailer="sephora",
        locator="https://www.sephora.com/product/lip-sleeping-mask-in-berry-2-5g-P446304",
        series_id="sephora_laneige_lipmask_berry_us_v0",
    )
    ld_json = json.dumps(
        {
            "@context": "http://schema.org",
            "@type": "ProductGroup",
            "productGroupID": "P446304",
            "hasVariant": [
                {
                    "@type": "Product",
                    "sku": "2240844",
                    "color": "Lip Sleeping Mask in Berry - 2.5g",
                    "offers": {
                        "@type": "Offer",
                        "price": "0.01",
                        "priceCurrency": "USD",
                        "availability": "https://schema.org/OutOfStock",
                    },
                }
            ],
            "aggregateRating": {"@type": "AggregateRating", "reviewCount": "3", "ratingValue": "3.7"},
        },
        separators=(",", ":"),
    )
    html = f"""
    <html><head>
      <script type="application/ld+json">{ld_json}</script>
    </head><body>
      <section id="target-reviews">Ratings & Reviews (3)</section>
      <p>OUT OF STOCK</p>
    </body></html>
    """
    visible_text = "OUT OF STOCK\nRatings & Reviews (3)\nSummary\n5\n4\n3\n2\n1\n3.7\n3 Reviews*"
    return _write_packet_directory(
        tmp_path,
        packet,
        {"file_01": html.encode("utf-8"), "file_02": visible_text.encode("utf-8")},
    )


def _single_row(projection, row_kind: str) -> RetailPdpProjectionRow:
    rows = [row for row in projection.rows if row.row_kind == row_kind]
    assert len(rows) == 1
    return rows[0]


def test_amazon_projection_pins_dom_js_review_and_asin_without_ld_json() -> None:
    packet = _packet(
        retailer="amazon",
        locator="https://www.amazon.com/Laneige-Sleeping-Berry/dp/B07XXPHQZK",
        series_id="amazon_laneige_lipmask_berry_us_v0",
        variant_pin="Berry 2.5g (B07XXPHQZK)",
    )
    html = """
    <html><body>
      <input type="hidden" id="ASIN" name="ASIN" value="B07XXPHQZK">
      <input type="hidden" name="items[0.base][customerVisiblePrice][amount]" value="16.8">
      <div id="averageCustomerReviews"><span>4.6 out of 5 stars</span></div>
      <span id="acrCustomerReviewText">36,799 global ratings</span>
      <div id="imageBlock_feature_div">hero image chrome</div>
    </body></html>
    """
    visible_text = """
    LANEIGE Lip Sleeping Mask
    Style: Berry
    $16.80
    FREE delivery Sunday, June 21 on orders shipped by Amazon over $35
    In Stock
    Customer reviews
    4.6 out of 5 stars
    36,799 global ratings
    Best Sellers Rank: #249 in Beauty & Personal Care
    Get a $10 Amazon Store Card instantly upon approval
    LANEIGE products customers bought together
    """

    projection = _projection(packet=packet, html=html, visible_text=visible_text)

    assert projection.certification == RETAIL_PDP_PROJECTION_CERTIFICATION
    assert [row for row in projection.rows if row.row_kind == "retail_embedded_structured_json"] == []
    variant = _single_row(projection, "retail_variant_offer")
    assert variant.source_visible_fields["sku"] == "B07XXPHQZK"
    assert variant.source_visible_fields["price"] == "16.8"
    assert variant.source_visible_fields["availability"] == "In Stock"
    assert variant.source_visible_fields["variant_binding_source"] == "amazon_dom_js"

    review = _single_row(projection, "retail_review_substrate")
    assert review.source_visible_fields["review_substrate_source"] == "amazon_dom_js"
    assert review.source_visible_fields["ld_json_present"] is False
    assert review.source_visible_fields["review_count"] == "36,799"
    assert "Best Sellers Rank" in review.source_visible_fields["best_sellers_rank_text"]
    assert review.raw_anchor.anchor_value == "#averageCustomerReviews/#acrCustomerReviewText"

    carried_modules = {
        row.source_visible_fields["module_type"]: row
        for row in projection.rows
        if row.row_kind == "retail_carried_module"
    }
    assert set(carried_modules) == {"shipping", "loyalty", "recommendations"}
    shipping = carried_modules["shipping"]
    assert shipping.source_visible_fields["anchor_source"] == "visible_text"
    assert "$35" in shipping.source_visible_fields["text_excerpt"]
    assert shipping.raw_anchor.file_id == "file_02"
    assert shipping.raw_anchor.anchor_value is not None
    assert "$35" in shipping.raw_anchor.anchor_value
    binding_types = {binding.binding_type for binding in projection.binding_map}
    assert {"sku_variant_price", "variant_availability", "series_locale_currency"} <= binding_types
    assert projection.loss_ledger.collapsed[0].category == "RETAIL_HERO_IMAGERY_COLLAPSED"


def test_amazon_projection_does_not_preserve_structure_for_404_page() -> None:
    packet = _packet(
        retailer="amazon",
        locator="https://www.amazon.com/Carolina-Herrera-Good-Girl-Parfum/dp/B01FIOLI2G",
        series_id="amazon_good_girl_404_capture_us_v0",
    )
    html = """
    <html><head><title>Page Not Found</title></head>
    <body>Sorry! We couldn't find that page. Dogs of Amazon</body></html>
    """

    projection = _projection(packet=packet, html=html, visible_text="")

    assert [row for row in projection.rows if row.row_kind == "retail_variant_offer"] == []
    assert [row for row in projection.rows if row.row_kind == "retail_review_substrate"] == []
    assert projection.loss_ledger.structure_preserved is False
    assert "cloakbrowser_snapshot_01:amazon:variant_offer_absent" in projection.residuals
    assert "cloakbrowser_snapshot_01:amazon:review_substrate_absent" in projection.residuals


def test_carried_module_text_pattern_prefers_exact_html_occurrence() -> None:
    packet = _packet(
        retailer="amazon",
        locator="https://www.amazon.com/Laneige-Sleeping-Berry/dp/B07XXPHQZK",
        series_id="amazon_laneige_lipmask_berry_us_v0",
        variant_pin="Berry 2.5g (B07XXPHQZK)",
    )
    html = """
    <html><body>
      <input type="hidden" id="ASIN" name="ASIN" value="B07XXPHQZK">
      <input type="hidden" name="items[0.base][customerVisiblePrice][amount]" value="24.00">
      <p>Enjoy fast, free delivery, exclusive deals, and award-winning movies & TV shows.</p>
      <div id="deliveryBlock">FREE delivery Sunday, June 21 on orders shipped by Amazon over $35</div>
    </body></html>
    """
    visible_text = """
    LANEIGE Lip Sleeping Mask
    Style: Berry
    $24.00
    In Stock
    """

    projection = _projection(packet=packet, html=html, visible_text=visible_text)

    shipping_modules = [
        row
        for row in projection.rows
        if row.row_kind == "retail_carried_module" and row.source_visible_fields["module_type"] == "shipping"
    ]
    assert len(shipping_modules) == 1
    shipping = shipping_modules[0]
    assert shipping.source_visible_fields["anchor_source"] == "rendered_dom"
    assert "$35" in shipping.source_visible_fields["text_excerpt"]
    assert "award-winning" not in shipping.source_visible_fields["text_excerpt"]
    assert shipping.raw_anchor.file_id == "file_01"
    assert shipping.raw_anchor.anchor_value is not None
    assert "$35" in shipping.raw_anchor.anchor_value


def test_ulta_projection_residualizes_present_offer_substrate_when_not_extracted() -> None:
    packet = _packet(
        retailer="ulta",
        locator="https://www.ulta.com/p/good-girl-eau-de-parfum-pimprod2022701?sku=2573274",
        series_id="ulta_good_girl_offer_substrate_us_v0",
    )
    apollo = json.dumps(
        {
            "ROOT_QUERY": {
                'Page({"moduleParams":{"sku":"2573274"},"url":{"path":"/p/good-girl-eau-de-parfum-pimprod2022701"}})': {
                    "content": {
                        "modules": [
                            {
                                "skuId": "2573274",
                                "productId": "pimprod2022701",
                                "salePrice": "$145.00",
                            }
                        ]
                    }
                }
            }
        },
        separators=(",", ":"),
    )
    html = f"<script>window.__APOLLO_STATE__ = {apollo}</script>"

    projection = _projection(packet=packet, html=html, visible_text="Good Girl Eau de Parfum")

    structured = _single_row(projection, "retail_embedded_structured_json")
    assert structured.source_visible_fields["parse_status"] == "parsed"
    assert [row for row in projection.rows if row.row_kind == "retail_variant_offer"] == []
    assert "cloakbrowser_snapshot_01:ulta:variant_offer_absent" in projection.residuals
    assert "cloakbrowser_snapshot_01:ulta:variant_offer_substrate_present_but_unextracted" in projection.residuals
    assert projection.loss_ledger.structure_preserved is False


def test_sephora_projection_uses_target_review_widget_not_recommendation_noise() -> None:
    packet = _packet(
        retailer="sephora",
        locator="https://www.sephora.com/product/lip-sleeping-mask-in-berry-2-5g-P446304",
        series_id="sephora_laneige_lipmask_berry_us_v0",
    )
    ld_json = json.dumps(
        {
            "@context": "http://schema.org",
            "@type": "ProductGroup",
            "name": "Lip Sleeping Mask in Berry - 2.5g",
            "productGroupID": "P446304",
            "hasVariant": [
                {
                    "@type": "Product",
                    "sku": "2240844",
                    "color": "Lip Sleeping Mask in Berry - 2.5g",
                    "offers": {"@type": "Offer", "price": "0.01", "priceCurrency": "USD", "availability": "https://schema.org/OutOfStock"},
                }
            ],
            "aggregateRating": {"@type": "AggregateRating", "reviewCount": "3", "ratingValue": "3.6666666666666665"},
        },
        separators=(",", ":"),
    )
    html = f"""
    <html><head>
      <script>Sephora.configurationSettings = {{"bvApi_rwdRating_desktop_read":{{"host":"api.bazaarvoice.com"}}}};</script>
      <script type="application/ld+json">{ld_json}</script>
    </head><body>
      <section id="target-reviews">Ratings & Reviews (3)<span>3 Reviews*</span></section>
      <a data-cnstrc-item="recommendation" data-cnstrc-item-name="Alpha Beta">
        <span data-at="product_list_price">$99.00</span>
        <span data-at="review_count" aria-label="7.8K reviews">7.8K</span>
      </a>
      <p>Sign in for FREE standard shipping.</p>
      <p>OUT OF STOCK</p>
    </body></html>
    """
    visible_text = """
    LANEIGE
    Lip Sleeping Mask in Berry - 2.5g
    OUT OF STOCK
    Sign in for FREE standard shipping.
    Questions & Answers (0)
    Ratings & Reviews (3)
    Write a review
    Summary
    5
    4
    3
    2
    1
    3.7
    3 Reviews*
    """

    projection = _projection(packet=packet, html=html, visible_text=visible_text)

    structured = _single_row(projection, "retail_embedded_structured_json")
    assert structured.source_visible_fields["raw_json_text"] == ld_json
    variant = _single_row(projection, "retail_variant_offer")
    assert variant.source_visible_fields["sku"] == "2240844"
    assert variant.source_visible_fields["price"] == "0.01"
    assert variant.source_visible_fields["price_isolation"] == "structured_json_offer"
    assert variant.source_visible_fields["price_binding_source"] == "ld_json"
    assert variant.source_visible_fields["availability"] == "https://schema.org/OutOfStock"

    review = _single_row(projection, "retail_review_substrate")
    assert review.source_visible_fields["review_substrate_source"] == "sephora_target_dom"
    assert review.source_visible_fields["bazaarvoice_api_config_present"] is True
    assert review.source_visible_fields["review_count"] == "3"
    assert review.source_visible_fields["ld_json_review_count"] == "3"
    assert review.source_visible_fields["recommendation_review_count_examples"] == ["7.8K reviews"]
    assert review.source_visible_fields["recommendation_counts_are_not_target_substrate"] is True
    assert "sephora_price_from_structured_json_without_target_dom_price" in projection.residuals
    assert "sephora_ld_json_review_count_differs_from_target_dom" not in projection.residuals


def test_sephora_projection_uses_target_dom_price_when_product_page_anchor_exists() -> None:
    packet = _packet(
        retailer="sephora",
        locator="https://www.sephora.com/product/lip-sleeping-mask-P420652",
        series_id="sephora_laneige_lipmask_visible_price_recapture_v0",
    )
    ld_json = json.dumps(
        {
            "@context": "http://schema.org",
            "@type": "Product",
            "name": "Lip Sleeping Mask",
            "productID": "P420652",
            "sku": "1966258",
            "scent": "Berry",
            "offers": {"@type": "Offer", "price": "24.00", "priceCurrency": "USD", "availability": "https://schema.org/InStock"},
            "aggregateRating": {"@type": "AggregateRating", "reviewCount": "22240", "ratingValue": "4.3158273381294965"},
        },
        separators=(",", ":"),
    )
    html = f"""
    <html><head><script type="application/ld+json">{ld_json}</script></head>
    <body>
      <div data-cnstrc-item-id="P420652" data-cnstrc-item-price="$24.00"
        data-cnstrc-item-variation-id="1966258" data-comp="ProductPage ProductPage BaseComponent">
        <b>$24.00</b>
      </div>
      <a data-cnstrc-item="recommendation" data-cnstrc-item-name="Alpha Beta">
        <span data-at="product_list_price">$99.00</span>
      </a>
      <section>Ratings & Reviews (22K)</section>
    </body></html>
    """

    projection = _projection(packet=packet, html=html, visible_text="Ratings & Reviews (22K)\nAdd to Basket")

    variant = _single_row(projection, "retail_variant_offer")
    assert variant.source_visible_fields["sku"] == "1966258"
    assert variant.source_visible_fields["price"] == "24.00"
    assert variant.source_visible_fields["dom_price"] == "24.00"
    assert variant.source_visible_fields["dom_product_id"] == "P420652"
    assert variant.source_visible_fields["dom_sku"] == "1966258"
    assert variant.source_visible_fields["price_isolation"] == "sephora_dom_product_page"
    assert variant.source_visible_fields["price_binding_source"] == "rendered_dom_product_page"
    assert "sephora_price_from_structured_json_without_target_dom_price" not in projection.residuals


def test_sephora_projection_residualizes_ld_json_review_count_trap_when_dom_differs() -> None:
    packet = _packet(
        retailer="sephora",
        locator="https://www.sephora.com/product/lip-sleeping-mask-in-berry-2-5g-P446304",
        series_id="sephora_laneige_lipmask_berry_us_v0",
    )
    ld_json = json.dumps(
        {
            "@context": "http://schema.org",
            "@type": "ProductGroup",
            "productGroupID": "P446304",
            "hasVariant": [{"@type": "Product", "sku": "2240844", "offers": {"price": "0.01", "priceCurrency": "USD"}}],
            "aggregateRating": {"@type": "AggregateRating", "reviewCount": "3", "ratingValue": "3.7"},
        },
        separators=(",", ":"),
    )
    html = f'<script type="application/ld+json">{ld_json}</script><div id="bv-reviews">Ratings & Reviews (7.8K)</div>'
    visible_text = "Ratings & Reviews (7.8K)\nSummary\n5\n4\n3\n2\n1\n4.6\n7.8K Reviews*"

    projection = _projection(packet=packet, html=html, visible_text=visible_text)

    review = _single_row(projection, "retail_review_substrate")
    assert review.source_visible_fields["review_count"] == "7.8K"
    assert review.source_visible_fields["ld_json_review_count"] == "3"
    assert "sephora_ld_json_review_count_differs_from_target_dom" in review.residuals
    assert "sephora_ld_json_review_count_differs_from_target_dom" in projection.residuals


def test_ulta_projection_preserves_ld_json_and_apollo_verbatim_and_binds_rendered_sku() -> None:
    packet = _packet(
        retailer="ulta",
        locator="https://www.ulta.com/p/night-shift-overnight-lip-mask-pimprod2046225?sku=2620759",
        series_id="ulta_nightshift_overnight_lipmask_us_v0",
    )
    ld_json = json.dumps(
        {
            "@context": "https://schema.org/",
            "@type": "Product",
            "name": "Night Shift Overnight Lip Mask - Watermelon",
            "productID": "pimprod2046225",
            "sku": "2645443",
            "offers": {"@type": "Offer", "availability": "https://schema.org/InStock", "price": "12.00", "priceCurrency": "USD"},
            "scent": "Watermelon",
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": 4.3, "reviewCount": 671},
        },
        separators=(",", ":"),
    )
    apollo = json.dumps(
        {
            "ROOT_QUERY": {
                'Page({"moduleParams":{"sku":"2620759"},"url":{"path":"/p/night-shift-overnight-lip-mask-pimprod2046225"}})': {
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
                    }
                }
            }
        },
        separators=(",", ":"),
    )
    html = f"""
    <html><head><script type="application/ld+json">{ld_json}</script></head>
    <body>
      <script>window.__APOLLO_STATE__ = {apollo}</script>
      <div>Night Shift Overnight Lip Mask</div>
      <div>4.3</div><div>671 Reviews</div><div>In stock and ready to ship</div>
      <div>Free standard shipping over $35.</div><div>Earn points on this purchase.</div>
      <div>Make it a routine</div>
    </body></html>
    """
    visible_text = "Night Shift Overnight Lip Mask\n4.3\n671 Reviews\n$12.00\nIn stock and ready to ship\nFree standard shipping over $35.\nEarn points on this purchase.\nMake it a routine"

    projection = _projection(packet=packet, html=html, visible_text=visible_text)

    structured_rows = [row for row in projection.rows if row.row_kind == "retail_embedded_structured_json"]
    assert [row.source_visible_fields["structured_json_kind"] for row in structured_rows] == ["ld_json", "apollo_state"]
    assert structured_rows[0].source_visible_fields["raw_json_text"] == ld_json
    assert structured_rows[1].source_visible_fields["raw_json_text"] == apollo

    variant = _single_row(projection, "retail_variant_offer")
    assert variant.source_visible_fields["sku"] == "2645443"
    assert variant.source_visible_fields["apollo_sku"] == "2645443"
    assert variant.source_visible_fields["apollo_requested_sku"] == "2620759"
    assert variant.source_visible_fields["price"] == "12.00"
    assert variant.source_visible_fields["availability"] == "https://schema.org/InStock"
    assert "ulta_ld_json_apollo_sku_mismatch" not in projection.residuals
    assert "ulta_requested_sku_rendered_sku_mismatch" in projection.residuals

    review = _single_row(projection, "retail_review_substrate")
    assert review.source_visible_fields["review_substrate_source"] == "ulta_ld_json_and_apollo_state"
    assert review.source_visible_fields["review_count"] == "671"
    assert review.source_visible_fields["ld_json_review_count"] == "671"
    assert review.source_visible_fields["apollo_review_count"] == "671"


def test_ulta_projection_does_not_residualize_matching_requested_sku() -> None:
    packet = _packet(
        retailer="ulta",
        locator="https://www.ulta.com/p/night-shift-overnight-lip-mask-pimprod2046225?sku=2645443",
        series_id="ulta_nightshift_overnight_lipmask_us_v0",
    )
    ld_json = json.dumps(
        {
            "@context": "https://schema.org/",
            "@type": "Product",
            "name": "Night Shift Overnight Lip Mask - Watermelon",
            "productID": "pimprod2046225",
            "sku": "2645443",
            "offers": {"@type": "Offer", "availability": "https://schema.org/InStock", "price": "12.00", "priceCurrency": "USD"},
            "scent": "Watermelon",
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": 4.3, "reviewCount": 671},
        },
        separators=(",", ":"),
    )
    apollo = json.dumps(
        {
            "ROOT_QUERY": {
                'Page({"moduleParams":{"sku":"2645443"},"url":{"path":"/p/night-shift-overnight-lip-mask-pimprod2046225"}})': {
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
                    }
                }
            }
        },
        separators=(",", ":"),
    )
    html = f'<script type="application/ld+json">{ld_json}</script><script>window.__APOLLO_STATE__ = {apollo}</script>'

    projection = _projection(packet=packet, html=html, visible_text="Night Shift Overnight Lip Mask\n671 Reviews\n$12.00")

    variant = _single_row(projection, "retail_variant_offer")
    assert variant.source_visible_fields["sku"] == "2645443"
    assert variant.source_visible_fields["apollo_requested_sku"] == "2645443"
    assert "ulta_requested_sku_rendered_sku_mismatch" not in projection.residuals


def test_retail_projection_requires_raw_bytes_for_each_preserved_file() -> None:
    packet = _packet(
        retailer="ulta",
        locator="https://www.ulta.com/p/night-shift-overnight-lip-mask-pimprod2046225",
        series_id="ulta_nightshift_overnight_lipmask_us_v0",
    )

    with pytest.raises(ValueError, match="raw bytes are required"):
        build_retail_pdp_projection(packet=packet, raw_file_bytes_by_file_id={"file_01": b"<html></html>"})


def test_retail_projection_rejects_judgment_smuggling_field_names() -> None:
    raw_ref = RetailProjectionRawRef(packet_id="p1", slice_id="s1")
    raw_anchor = RetailProjectionRawAnchor(
        file_id="file_01",
        relative_packet_path="raw/body.html",
        sha256="sha",
        hash_basis="raw_stored_bytes",
        anchor_kind="file",
    )

    with pytest.raises(ValidationError, match="forbidden Judgment field"):
        RetailPdpProjectionRow(
            row_id="s1:retail:review",
            row_kind="retail_review_substrate",
            retailer="sephora",
            raw_ref=raw_ref,
            raw_anchor=raw_anchor,
            source_visible_fields={"credibility_label": "high"},
        )


def test_ulta_projection_residualizes_requested_sku_when_only_apollo_differs() -> None:
    packet = _packet(
        retailer="ulta",
        locator="https://www.ulta.com/p/night-shift-overnight-lip-mask-pimprod2046225?sku=2620759",
        series_id="ulta_nightshift_overnight_lipmask_us_v0",
    )
    apollo = json.dumps(
        {
            "ROOT_QUERY": {
                'Page({"moduleParams":{"sku":"2620759"},"url":{"path":"/p/night-shift-overnight-lip-mask-pimprod2046225"}})': {
                    "content": {
                        "modules": [
                            {
                                "skuId": "2645443",
                                "productId": "pimprod2046225",
                                "productName": "Night Shift Overnight Lip Mask",
                                "listPrice": "$12.00",
                            }
                        ]
                    }
                }
            }
        },
        separators=(",", ":"),
    )
    html = f"<script>window.__APOLLO_STATE__ = {apollo}</script>"
    visible_text = "Night Shift Overnight Lip Mask\n$12.00"

    projection = _projection(packet=packet, html=html, visible_text=visible_text)

    variant = _single_row(projection, "retail_variant_offer")
    assert variant.source_visible_fields["sku"] == "2645443"
    assert variant.source_visible_fields["apollo_requested_sku"] == "2620759"
    assert "ulta_requested_sku_rendered_sku_mismatch" in projection.residuals


def test_ulta_projection_residualizes_variant_pin_sku_when_apollo_request_is_absent() -> None:
    packet = _packet(
        retailer="ulta",
        locator="https://www.ulta.com/p/night-shift-overnight-lip-mask-pimprod2046225?sku=2620759",
        series_id="ulta_nightshift_overnight_lipmask_us_v0",
        variant_pin="sku=2620759",
    )
    ld_json = json.dumps(
        {
            "@context": "https://schema.org/",
            "@type": "Product",
            "sku": "2645443",
            "name": "Night Shift Overnight Lip Mask",
            "offers": {
                "@type": "Offer",
                "price": "12.00",
                "availability": "https://schema.org/InStock",
            },
        }
    )
    html = f'<script type="application/ld+json">{ld_json}</script>'

    projection = _projection(packet=packet, html=html, visible_text="Night Shift Overnight Lip Mask\n$12.00")

    variant = _single_row(projection, "retail_variant_offer")
    assert variant.source_visible_fields["sku"] == "2645443"
    assert "apollo_requested_sku" not in variant.source_visible_fields
    assert "ulta_requested_sku_rendered_sku_mismatch" in projection.residuals


def test_amazon_price_unanchored_visible_text_fallback_is_residualized() -> None:
    # With no target-anchored DOM price input, the only $N in visible text is a "$10 store card"
    # offer. It must be carried-but-flagged, never silently trusted as the target price.
    packet = _packet(
        retailer="amazon",
        locator="https://www.amazon.com/Some-Product/dp/B000000000",
        series_id="amazon_test_us_v0",
    )
    html = '<html><body><input type="hidden" id="ASIN" name="ASIN" value="B000000000"></body></html>'
    visible_text = (
        "Get a $10 Amazon Store Card instantly upon approval\n"
        "In Stock\n"
        "Customer reviews 4.6 out of 5 stars\n"
        "36,799 global ratings\n"
    )

    projection = _projection(packet=packet, html=html, visible_text=visible_text)

    variant = _single_row(projection, "retail_variant_offer")
    assert variant.source_visible_fields["price"] == "10"
    assert variant.source_visible_fields["price_isolation"] == "unanchored_visible_text_fallback"
    assert "amazon_price_from_unanchored_visible_text_fallback" in projection.residuals
    assert projection.loss_ledger.structure_preserved is True


def test_sephora_review_count_unanchored_fallback_is_residualized() -> None:
    # With no parenthesized "Ratings & Reviews (N)" target widget, the only "<token> Reviews" in
    # visible text is a recommendation count; it must be flagged as unanchored, not trusted as target.
    packet = _packet(
        retailer="sephora",
        locator="https://www.sephora.com/product/some-thing-P000001",
        series_id="sephora_test_us_v0",
    )
    html = "<html><body><span>nothing structured</span></body></html>"
    visible_text = "Bestsellers you may like\n7.8K Reviews\nMore picks\n"

    projection = _projection(packet=packet, html=html, visible_text=visible_text)

    review = _single_row(projection, "retail_review_substrate")
    assert review.source_visible_fields["review_count"] == "7.8K"
    assert review.source_visible_fields["review_count_isolation"] == "unanchored_fallback"
    assert "sephora_review_count_from_unanchored_fallback" in projection.residuals


def test_structure_preserved_is_false_when_required_retail_bindings_are_absent() -> None:
    # A residual is not itself structure loss, but a structured-json binding alone does not preserve
    # the retail PDP binding structure.
    packet = _packet(
        retailer="sephora",
        locator="https://www.sephora.com/product/some-thing-P000002",
        series_id="sephora_test_us_v0",
    )
    ld_json = json.dumps(
        {"@context": "http://schema.org", "@type": "WebPage", "name": "not a product"},
        separators=(",", ":"),
    )
    html = f'<html><head><script type="application/ld+json">{ld_json}</script></head><body>x</body></html>'
    visible_text = "x"

    projection = _projection(packet=packet, html=html, visible_text=visible_text)

    assert projection.residuals  # at least the variant_offer_absent residual
    assert projection.loss_ledger.preserved_bindings >= 1  # the structured_json_for_product binding
    assert projection.loss_ledger.structure_preserved is False


def test_packet_directory_writer_emits_hash_verified_projection_json(tmp_path: Path) -> None:
    packet_dir, packet = _sephora_projection_packet_dir(tmp_path)
    output_path = tmp_path / "projection" / "retail_pdp_projection.json"

    projection = write_retail_pdp_projection(packet_directory=packet_dir, output_path=output_path)
    written = json.loads(output_path.read_text(encoding="utf-8"))

    assert written["packet_id"] == packet.packet_id
    assert written["certification"] == RETAIL_PDP_PROJECTION_CERTIFICATION
    assert projection.loss_ledger.structure_preserved is True
    assert {row["row_kind"] for row in written["rows"]} >= {
        "retail_pdp_product",
        "retail_variant_offer",
        "retail_review_substrate",
        "retail_embedded_structured_json",
    }
    product_row = next(row for row in written["rows"] if row["row_kind"] == "retail_pdp_product")
    assert product_row["raw_anchor"]["sha256"] == packet.preserved_files[0].sha256
    assert product_row["source_visible_fields"]["retailer"] == "sephora"


def test_retail_pdp_projection_runner_writes_projection_json(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    packet_dir, _packet = _sephora_projection_packet_dir(tmp_path)
    output_path = tmp_path / "runner_projection.json"

    assert retail_projection_runner.main(["--packet-dir", str(packet_dir), "--output", str(output_path)]) == 0

    assert capsys.readouterr().out.strip() == str(output_path)
    written = json.loads(output_path.read_text(encoding="utf-8"))
    assert written["projection_method"] == "retail_pdp_mechanical_projection"
    assert written["loss_ledger"]["structure_preserved"] is True


def test_packet_directory_projection_blocks_missing_preserved_file(tmp_path: Path) -> None:
    packet_dir, _packet = _sephora_projection_packet_dir(tmp_path)
    (packet_dir / "raw" / "01_cloakbrowser_rendered_dom.html").unlink()

    with pytest.raises(RetailPdpProjectionInputError, match="not found"):
        build_retail_pdp_projection_from_packet_directory(packet_directory=packet_dir)


def test_packet_directory_projection_blocks_sha_mismatch(tmp_path: Path) -> None:
    packet_dir, _packet = _sephora_projection_packet_dir(tmp_path)
    html_path = packet_dir / "raw" / "01_cloakbrowser_rendered_dom.html"
    body = html_path.read_bytes()
    html_path.write_bytes((b"X" if body[:1] != b"X" else b"Y") + body[1:])

    with pytest.raises(RetailPdpProjectionInputError, match="sha256 mismatch"):
        build_retail_pdp_projection_from_packet_directory(packet_directory=packet_dir)


def test_packet_directory_projection_blocks_preserved_path_escape(tmp_path: Path) -> None:
    packet_dir, packet = _sephora_projection_packet_dir(tmp_path)
    escaped_files = [
        preserved_file.model_copy(update={"relative_packet_path": "../escape.html"})
        if preserved_file.file_id == "file_01"
        else preserved_file
        for preserved_file in packet.preserved_files
    ]
    packet = packet.model_copy(update={"preserved_files": escaped_files})
    (packet_dir / "manifest.json").write_text(
        f"{json.dumps(packet.model_dump(mode='json'), indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )

    with pytest.raises(RetailPdpProjectionInputError, match="resolves outside the packet dir"):
        build_retail_pdp_projection_from_packet_directory(packet_directory=packet_dir)
