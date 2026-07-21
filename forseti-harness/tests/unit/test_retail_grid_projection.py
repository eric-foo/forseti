from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from runners import run_retail_grid_projection as grid_projection_runner
from runners.run_capture_ecr_cleaning_smoke import run_capture_ecr_cleaning_smoke
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
from source_capture.retail_grid_projection import (
    RetailGridProjectionInputError,
    build_retail_grid_projection,
    build_retail_grid_projection_from_packet_directory,
    write_retail_grid_projection,
)


def test_walmart_next_data_projection_preserves_one_row_per_product_tile() -> None:
    next_data = {
        "props": {
            "pageProps": {
                "initialData": {
                    "searchResult": {
                        "itemStacks": [
                            {
                                "items": [
                                    _walmart_item(item_type="REGULAR", selected_variant=None),
                                    {"__typename": "SearchPlaceholder"},
                                    _walmart_item(item_type="VARIANT", selected_variant="Single"),
                                ]
                            }
                        ]
                    }
                }
            }
        }
    }
    body = _walmart_html(next_data)
    packet = _packet(
        retailer="walmart",
        locator="https://www.walmart.com/search?q=lip%20mask",
        relative_path="raw/01_http_response_body.bin",
        body=body,
        surface="direct_http",
    )

    projection = build_retail_grid_projection(
        packet=packet, raw_file_bytes_by_file_id={"file_01": body}
    )

    assert len(projection.rows) == 2
    assert projection.loss_ledger.structure_preserved is True
    assert [row.raw_anchor.anchor_value for row in projection.rows] == [
        "/props/pageProps/initialData/searchResult/itemStacks/0/items/0",
        "/props/pageProps/initialData/searchResult/itemStacks/0/items/2",
    ]
    first, second = projection.rows
    assert first.source_visible_fields["source_product_id"] == "2150828728"
    assert first.source_visible_fields["product_url"].startswith("https://www.walmart.com/ip/")
    assert first.source_visible_fields["price"] == "2.97"
    assert first.source_visible_fields["average_rating"] == 4.4
    assert first.source_visible_fields["rating_count"] == 180
    assert first.source_visible_fields["written_review_count"] is None
    assert first.source_visible_fields["availability_summary"] == "In stock"
    assert first.source_visible_fields["pickup_availability"] == "Pickup as soon as 12pm"
    assert first.source_visible_fields["delivery_availability"] == "Delivery as soon as 13 mins"
    assert first.source_visible_fields["location_ids"] == ["3081"]
    assert first.source_visible_fields["seller"] == "Walmart.com"
    assert first.source_visible_fields["exact_inventory_quantity_posture"] == "not_observed"
    assert first.source_visible_fields["sold_units_posture"] == "not_observed"
    assert second.source_visible_fields["selected_variant"] == "Single"
    assert "walmart_grid_exact_inventory_quantity_not_observed" in first.residuals
    assert "walmart_grid_sold_units_not_observed" in first.residuals


def test_walmart_grid_skips_incomplete_tile_and_preserves_valid_rows() -> None:
    valid = _walmart_item(item_type="REGULAR", selected_variant=None)
    incomplete = {
        "__typename": "Product",
        "usItemId": "9999999999",
        "name": "Incomplete product tile",
        "canonicalUrl": None,
    }
    next_data = {
        "props": {
            "pageProps": {
                "initialData": {
                    "searchResult": {
                        "itemStacks": [{"items": [valid, incomplete]}]
                    }
                }
            }
        }
    }
    body = _walmart_html(next_data)
    packet = _packet(
        retailer="walmart",
        locator="https://www.walmart.com/search?q=lip%20mask",
        relative_path="raw/01_http_response_body.bin",
        body=body,
        surface="direct_http",
    )

    projection = build_retail_grid_projection(
        packet=packet, raw_file_bytes_by_file_id={"file_01": body}
    )

    assert [
        row.source_visible_fields["source_product_id"] for row in projection.rows
    ] == ["2150828728"]
    assert (
        "walmart_grid_01:walmart:grid_tile_identity_incomplete:0:1"
        in projection.residuals
    )
    assert projection.loss_ledger.structure_preserved is True


def test_target_rendered_projection_preserves_product_cards_and_channel_availability() -> None:
    body = _target_html().encode("utf-8")
    packet = _packet(
        retailer="target",
        locator="https://www.target.com/s?searchTerm=lip%20mask",
        relative_path="raw/01_cloakbrowser_rendered_dom.html",
        body=body,
        surface="cloakbrowser_snapshot",
    )

    projection = build_retail_grid_projection(
        packet=packet, raw_file_bytes_by_file_id={"file_01": body}
    )

    assert len(projection.rows) == 2
    row = projection.rows[0]
    assert row.source_visible_fields["source_product_id"] == "94631382"
    assert row.source_visible_fields["product_url"] == (
        "https://www.target.com/p/byoma-liptide-lip-mask-0-2-fl-oz/-/A-94631382#lnk=sametab"
    )
    assert row.source_visible_fields["name"].startswith("BYOMA Liptide Lip Mask")
    assert row.source_visible_fields["price"] == "10.99"
    assert row.source_visible_fields["average_rating"] == "3.8"
    assert row.source_visible_fields["rating_count"] == "145"
    assert row.source_visible_fields["written_review_count"] is None
    assert row.source_visible_fields["availability_summary"] == "In stock"
    assert row.source_visible_fields["pickup_availability"] == "ready by July 10"
    assert row.source_visible_fields["delivery_availability"] == "as soon as 2am"
    assert row.source_visible_fields["shipping_availability"] == "arrives Tue, Jul 14"
    assert row.raw_anchor.anchor_kind == "html_selector"
    assert row.raw_anchor.anchor_value == (
        ':nth-match([data-focusid="94631382_product_card"], 1)'
    )
    assert row.source_visible_fields["exact_inventory_quantity_posture"] == "not_observed"
    assert row.source_visible_fields["sold_units_posture"] == "not_observed"
    assert "target_grid_location_pin_not_observed" in row.residuals


def test_target_duplicate_product_placements_receive_ordinal_anchors() -> None:
    rendered_html = _target_html().replace(
        'data-focusid="91234567_product_card"',
        'data-focusid="94631382_product_card"',
    ).replace("preselect=91234567", "preselect=94631382")
    body = rendered_html.encode("utf-8")
    packet = _packet(
        retailer="target",
        locator="https://www.target.com/s?searchTerm=lip%20mask",
        relative_path="raw/01_cloakbrowser_rendered_dom.html",
        body=body,
        surface="cloakbrowser_snapshot",
    )

    projection = build_retail_grid_projection(
        packet=packet, raw_file_bytes_by_file_id={"file_01": body}
    )
    duplicate_anchors = [
        row.raw_anchor.anchor_value
        for row in projection.rows
        if row.source_visible_fields["source_product_id"] == "94631382"
    ]

    assert duplicate_anchors == [
        ':nth-match([data-focusid="94631382_product_card"], 1)',
        ':nth-match([data-focusid="94631382_product_card"], 2)',
    ]


def test_sephora_linkstore_projection_deduplicates_parent_products_and_reconciles_count() -> None:
    products = [
        _sephora_product(product_id="P455936", name="Lip Butter Balm"),
        _sephora_product(product_id="P455936", name="Lip Butter Balm"),
        _sephora_product(
            product_id="P429952",
            name="Jet Lag Mask",
            list_price="$26.00 - $49.00",
        ),
    ]
    body = _sephora_grid_html(
        products=products,
        total_products=2,
        currency_code="USD",
    )
    packet = _packet(
        retailer="sephora",
        locator="https://www.sephora.com/brand/summer-fridays?country_switch=us",
        relative_path="raw/01_cloakbrowser_rendered_dom.html",
        body=body,
        surface="cloakbrowser_snapshot",
    )

    projection = build_retail_grid_projection(
        packet=packet, raw_file_bytes_by_file_id={"file_01": body}
    )

    assert [row.source_visible_fields["source_product_id"] for row in projection.rows] == [
        "P455936",
        "P429952",
    ]
    first = projection.rows[0]
    assert first.source_visible_fields["canonical_product_url"] == (
        "https://www.sephora.com/product/lip-butter-balm-P455936"
    )
    assert first.source_visible_fields["price"] == "24.00"
    assert first.source_visible_fields["price_currency"] == "USD"
    assert first.source_visible_fields["average_rating"] == 4.29
    assert first.source_visible_fields["review_count"] == 17635
    assert first.source_visible_fields["visible_variant_count"] == 11
    assert first.source_visible_fields["badges"] == ["isBestseller", "isNew"]
    assert [placement.grid_position for placement in first.placements] == [1, 2]
    assert [placement.raw_anchor.anchor_value for placement in first.placements] == [
        "/page/nthBrand/products/0",
        "/page/nthBrand/products/1",
    ]
    assert projection.completeness.status == "complete"
    assert projection.completeness.page_declared_result_count == 2
    assert projection.completeness.extracted_unique_parent_count == 2
    assert projection.completeness.extracted_placement_count == 3
    assert projection.completeness.duplicate_placement_count == 1
    assert projection.completeness.termination == (
        "retailer_serialized_count_reconciled"
    )
    assert projection.source_visible_grid_facts["subject_binding_confirmed"] is True
    ranged = projection.rows[1]
    assert ranged.source_visible_fields["price"] is None
    assert ranged.source_visible_fields["price_display"] == "$26.00 - $49.00"
    assert ranged.source_visible_fields["price_range"] == {
        "minimum": "26.00",
        "maximum": "49.00",
    }


def test_sephora_projection_preserves_partial_tile_and_fails_count_reconciliation() -> None:
    incomplete = _sephora_product(product_id="P000002", name="Missing URL")
    incomplete["targetUrl"] = None
    body = _sephora_grid_html(
        products=[
            _sephora_product(product_id="P000001", name="Complete Product"),
            incomplete,
        ],
        total_products=2,
        currency_code="USD",
    )
    packet = _packet(
        retailer="sephora",
        locator="https://www.sephora.com/brand/summer-fridays?country_switch=us",
        relative_path="raw/01_cloakbrowser_rendered_dom.html",
        body=body,
        surface="cloakbrowser_snapshot",
    )

    projection = build_retail_grid_projection(
        packet=packet, raw_file_bytes_by_file_id={"file_01": body}
    )

    assert len(projection.rows) == 1
    assert projection.completeness.status == "incomplete"
    assert projection.completeness.termination == "unproven"
    assert any(
        "declared_unique_parent_count_mismatch" in residual
        for residual in projection.completeness.residuals
    )
    assert "sephora_grid_incomplete_product_identity_present" in (
        projection.completeness.residuals
    )
    assert any("grid_tile_identity_incomplete:1" in item for item in projection.residuals)


def test_grid_projection_runner_writes_hash_verified_sidecar(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    packet_dir = _write_walmart_packet(tmp_path)
    output = tmp_path / "projection" / "retail_grid_projection.json"

    assert grid_projection_runner.main(
        ["--packet-dir", str(packet_dir), "--output", str(output)]
    ) == 0

    assert capsys.readouterr().out.strip() == str(output)
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["projection_method"] == "retail_grid_mechanical_projection"
    assert payload["loss_ledger"]["structure_preserved"] is True
    assert payload["rows"][0]["raw_anchor"]["sha256"] == hashlib.sha256(
        (packet_dir / "raw/01_http_response_body.bin").read_bytes()
    ).hexdigest()


def test_grid_projection_packet_directory_blocks_hash_mismatch(tmp_path: Path) -> None:
    packet_dir = _write_walmart_packet(tmp_path)
    raw_path = packet_dir / "raw/01_http_response_body.bin"
    raw_path.write_bytes(raw_path.read_bytes() + b"tampered")

    with pytest.raises(RetailGridProjectionInputError, match="size mismatch"):
        build_retail_grid_projection_from_packet_directory(packet_directory=packet_dir)


def test_grid_projection_packet_directory_blocks_missing_raw_file(tmp_path: Path) -> None:
    packet_dir = _write_walmart_packet(tmp_path)
    (packet_dir / "raw/01_http_response_body.bin").unlink()

    with pytest.raises(RetailGridProjectionInputError, match="not found"):
        build_retail_grid_projection_from_packet_directory(packet_directory=packet_dir)


def test_smoke_accepts_grid_projection_and_preserves_anchors_residuals_and_lineage(
    tmp_path: Path,
) -> None:
    packet_dir = _write_walmart_packet(tmp_path)
    projection_path = tmp_path / "projection" / "retail_grid_projection.json"
    projection = write_retail_grid_projection(
        packet_directory=packet_dir, output_path=projection_path
    )
    manifest_path = _write_smoke_manifest(
        tmp_path, packet_dir=packet_dir, projection_path=projection_path
    )

    outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=manifest_path,
        output_dir=tmp_path / "smoke_outputs",
        include_cleaning_transform_smoke=True,
    )

    receipts = _load_json(Path(outputs["ecr_source_side_receipts"]))
    cleaning = _load_json(Path(outputs["cleaning_packet"]))
    summary = _load_json(Path(outputs["smoke_summary"]))
    assert len(receipts["receipts"]) == 1
    assert len(cleaning["handles"]) == len(projection.rows) == 1
    assert len(cleaning["transform_ledger"]) == 1
    handle = cleaning["handles"][0]
    assert handle["source_row_kind"] == "retail_grid_product"
    assert handle["source_anchor"]["anchor_kind"] == "json_pointer"
    assert handle["source_anchor"]["json_pointer"].endswith("/itemStacks/0/items/0")
    assert "walmart_grid_written_review_count_not_observed" in handle["residuals"]
    assert "walmart_grid_exact_inventory_quantity_not_observed" in handle["residuals"]
    assert summary["sources"][0]["page_kind"] == "grid"
    assert summary["sources"][0]["capture_validity_supported"] is True
    assert not any(
        finding["code"] == "retail_row_anchor_unverified"
        for finding in summary["findings"]
    )


def test_smoke_fails_visibly_when_required_grid_identity_is_missing(tmp_path: Path) -> None:
    packet_dir = _write_walmart_packet(tmp_path)
    projection_path = tmp_path / "projection" / "retail_grid_projection.json"
    write_retail_grid_projection(packet_directory=packet_dir, output_path=projection_path)
    payload = _load_json(projection_path)
    payload["rows"][0]["source_visible_fields"]["name"] = None
    projection_path.write_text(json.dumps(payload), encoding="utf-8")
    manifest_path = _write_smoke_manifest(
        tmp_path, packet_dir=packet_dir, projection_path=projection_path
    )

    with pytest.raises(ValidationError, match="source identity fields: name"):
        run_capture_ecr_cleaning_smoke(
            smoke_manifest_path=manifest_path, output_dir=tmp_path / "smoke_outputs"
        )


def test_smoke_reports_unverified_grid_json_pointer(tmp_path: Path) -> None:
    packet_dir = _write_walmart_packet(tmp_path)
    projection_path = tmp_path / "projection" / "retail_grid_projection.json"
    write_retail_grid_projection(packet_directory=packet_dir, output_path=projection_path)
    payload = _load_json(projection_path)
    payload["rows"][0]["raw_anchor"]["anchor_value"] = (
        "/props/pageProps/initialData/searchResult/itemStacks/0/items/99"
    )
    projection_path.write_text(json.dumps(payload), encoding="utf-8")
    manifest_path = _write_smoke_manifest(
        tmp_path, packet_dir=packet_dir, projection_path=projection_path
    )

    outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=manifest_path, output_dir=tmp_path / "smoke_outputs"
    )
    summary = _load_json(Path(outputs["smoke_summary"]))
    assert any(
        finding["code"] == "retail_row_anchor_unverified"
        and finding["reason"] == "json_pointer_absent_from_raw"
        for finding in summary["findings"]
    )


def _walmart_item(*, item_type: str, selected_variant: str | None) -> dict[str, object]:
    item: dict[str, object] = {
        "__typename": "Product",
        "usItemId": "2150828728",
        "name": "Vitamasques Cherry Vegan Collagen Lip Mask, Moisturize & Plump, One Patch",
        "type": item_type,
        "canonicalUrl": "/ip/Vitamasques-Lip-Mask/2150828728?classType=REGULAR",
        "price": 2.97,
        "priceInfo": {"linePriceDisplay": "$2.97"},
        "averageRating": 4.4,
        "numberOfReviews": 180,
        "availabilityStatusV2": {"display": "In stock", "value": "IN_STOCK"},
        "sellerName": "Walmart.com",
        "fulfillmentBadgeGroups": [
            {"key": "FF_DELIVERY", "text": "Delivery as soon as ", "slaText": "13 mins"},
            {"key": "FF_PICKUP", "text": "Pickup as soon as ", "slaText": "12pm"},
        ],
        "fulfillmentSummary": [{"fulfillment": "PICKUP", "storeId": "3081"}],
        "variantList": [],
    }
    if selected_variant:
        item["variantList"] = [
            {"usItemId": "2150828728", "displayName": selected_variant, "name": "1"}
        ]
    return item


def _walmart_html(next_data: dict[str, object]) -> bytes:
    return (
        '<html><body><script id="__NEXT_DATA__" type="application/json">'
        + json.dumps(next_data, separators=(",", ":"))
        + "</script></body></html>"
    ).encode("utf-8")


def _target_html() -> str:
    return """
    <html><body><div data-test="product-grid">
      <div data-focusid="94631382_product_card" data-test="@web/site-top-of-funnel/ProductCardWrapper">
        <a href="/p/byoma-liptide-lip-mask-0-2-fl-oz/-/A-94631382#lnk=sametab">image</a>
        <span data-test="current-price"><span>$10.99</span></span>
        <a aria-label="BYOMA Liptide Lip Mask - 0.2 fl oz: Moisturizing &amp; Vegan"
           data-test="@web/ProductCard/title">BYOMA Liptide Lip Mask</a>
        <div aria-label="3.8 stars with 145 ratings"></div>
        <div data-test="lowStockMessaging"><span>In stock</span></div>
        <span>Pickup </span><span>ready by July 10</span>
        <span>Delivery </span><span>as soon as 2am</span>
        <span>Shipping </span><span>arrives Tue, Jul 14</span>
      </div>
      <div data-focusid="91234567_product_card" data-test="@web/site-top-of-funnel/ProductCardWrapper">
        <a href="/p/second-mask/-/A-90000000?preselect=91234567#lnk=sametab">image</a>
        <span data-test="current-price"><span>$8.00</span></span>
        <a aria-label="Second Lip Mask" data-test="@web/ProductCard/title">Second Lip Mask</a>
        <div aria-label="4.2 stars with 12 ratings"></div>
      </div>
    </div></body></html>
    """


def _sephora_product(
    *, product_id: str, name: str, list_price: str = "$24.00"
) -> dict[str, object]:
    return {
        "brandName": "Summer Fridays",
        "currentSku": {
            "isBestseller": True,
            "isNew": True,
            "listPrice": list_price,
            "skuId": f"SKU-{product_id}",
        },
        "displayName": name,
        "moreColors": 11,
        "pickupEligible": False,
        "productId": product_id,
        "rating": 4.29,
        "reviews": 17635,
        "sameDayEligible": False,
        "targetUrl": f"/product/{name.lower().replace(' ', '-')}-{product_id}?skuId=1",
    }


def _sephora_grid_html(
    *,
    products: list[dict[str, object]],
    total_products: int,
    currency_code: str | None,
) -> bytes:
    nth_brand: dict[str, object] = {
        "brandId": "6247",
        "displayName": "Summer Fridays",
        "shortName": "Summer Fridays",
        "resultId": "test-result",
        "targetUrl": "/brand/summer-fridays",
        "seoCanonicalUrl": "/brand/summer-fridays",
        "pageSize": 60,
        "totalProducts": total_products,
        "products": products,
    }
    if currency_code is not None:
        nth_brand["currencyCode"] = currency_code
    payload = {"page": {"nthBrand": nth_brand}}
    return (
        '<html><body><script id="linkStore" type="text/json">'
        + json.dumps(payload, separators=(",", ":"))
        + "</script></body></html>"
    ).encode("utf-8")


def _packet(
    *, retailer: str, locator: str, relative_path: str, body: bytes, surface: str
) -> SourceCapturePacket:
    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason("grid has no source event time"),
        source_edit_or_version=unknown_with_reason("grid has no source edit time"),
        capture_time=known_fact("2026-07-11T00:00:00Z"),
        recapture_time=not_applicable("first capture"),
        cutoff_posture=unknown_with_reason("test fixture has no cutoff"),
    )
    preserved_file = PreservedFile(
        file_id="file_01",
        original_path=Path(relative_path).name,
        relative_packet_path=relative_path,
        sha256=hashlib.sha256(body).hexdigest(),
        hash_basis="raw_stored_bytes",
        size_bytes=len(body),
    )
    return SourceCapturePacket(
        packet_id=f"01TESTGRID{retailer.upper()}",
        manifest_version="source_capture_packet_manifest_v1",
        obligation_contract_version="core_spine_v0_data_capture_spine_obligation_contract_v0",
        source_family="retail_grid",
        source_surface=surface,
        source_locator=known_fact(locator),
        requested_decision_context=known_fact(f"{retailer} grid projection fixture"),
        capture_context=known_fact("unit test packet"),
        actor_audience_context=unknown_with_reason("not supplied"),
        capture_mode=(
            CaptureModeCategory.STRUCTURED_ACCESS
            if retailer == "walmart"
            else CaptureModeCategory.MULTIMODAL
        ),
        operator_category="unit_test",
        session_identity="01TESTGRIDSESSION",
        timing=timing,
        access_posture=known_fact("fixture supplied"),
        archive_history_posture=not_attempted("archive not queried"),
        media_modality_posture=not_attempted("screenshot not supplied"),
        re_capture_relationship=not_applicable("first capture"),
        series_id=f"{retailer}_lip_mask_grid_us_v0",
        source_slices=[
            SourceCaptureSlice(
                slice_id=f"{retailer}_grid_01",
                locator=known_fact(locator),
                timing=timing,
                access_posture=known_fact("fixture supplied"),
                archive_history_posture=not_attempted("archive not queried"),
                media_modality_posture=not_attempted("screenshot not supplied"),
                re_capture_relationship=not_applicable("first capture"),
                locale_pin=known_fact("en-US"),
                currency_pin=known_fact("USD"),
                preserved_file_ids=["file_01"],
            )
        ],
        preserved_files=[preserved_file],
        receipt_metadata=ReceiptMetadata(
            title="Retail grid fixture",
            generated_at="2026-07-11T00:00:00Z",
            summary="unit test packet",
            non_claims=["not Cleaning", "not Judgment"],
        ),
    )


def _write_walmart_packet(tmp_path: Path) -> Path:
    next_data = {
        "props": {
            "pageProps": {
                "initialData": {
                    "searchResult": {
                        "itemStacks": [{"items": [_walmart_item(item_type="REGULAR", selected_variant=None)]}]
                    }
                }
            }
        }
    }
    body = _walmart_html(next_data)
    packet = _packet(
        retailer="walmart",
        locator="https://www.walmart.com/search?q=lip%20mask",
        relative_path="raw/01_http_response_body.bin",
        body=body,
        surface="direct_http",
    )
    packet_dir = tmp_path / "walmart_packet"
    raw_path = packet_dir / packet.preserved_files[0].relative_packet_path
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_bytes(body)
    (packet_dir / "manifest.json").write_text(
        f"{json.dumps(packet.model_dump(mode='json'), indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )
    return packet_dir


def _write_smoke_manifest(
    tmp_path: Path, *, packet_dir: Path, projection_path: Path
) -> Path:
    path = tmp_path / "smoke_manifest.json"
    path.write_text(
        json.dumps(
            {
                "run_id": "retail_grid_fixture_smoke",
                "retail": [
                    {
                        "retailer": "walmart",
                        "packet_dir": str(packet_dir),
                        "projection_json": str(projection_path),
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_ulta_grid_projection_reconciles_visible_placements_and_duplicates() -> None:
    body = _ulta_grid_html().encode()
    packet = _packet(
        retailer="ulta",
        locator="https://www.ulta.com/brand/clinique",
        relative_path="raw/01_cloakbrowser_rendered_dom.html",
        body=body,
        surface="cloakbrowser_snapshot",
    )

    projection = build_retail_grid_projection(
        packet=packet, raw_file_bytes_by_file_id={"file_01": body}
    )

    assert projection.completeness.status == "complete"
    assert projection.completeness.termination == "retailer_visible_count_reconciled"
    assert projection.completeness.extracted_unique_parent_count == 2
    assert projection.completeness.extracted_placement_count == 3
    assert projection.completeness.duplicate_placement_count == 1
    first = next(
        row
        for row in projection.rows
        if row.source_visible_fields["source_product_id"] == "pimprod2056072"
    )
    assert len(first.placements) == 2
    assert first.source_visible_fields["selected_sku_id"] == "2639131"
    assert first.source_visible_fields["price_range"] == {
        "minimum": "18.00",
        "maximum": "89.00",
    }
    assert first.source_visible_fields["average_rating"] == "4.6"
    assert first.source_visible_fields["review_count"] == 4253
    assert first.source_visible_fields["price_currency"] is None


def test_ulta_grid_projection_fails_closed_while_load_more_remains() -> None:
    body = _ulta_grid_html(viewed=2, load_more=True).encode()
    packet = _packet(
        retailer="ulta",
        locator="https://www.ulta.com/brand/clinique",
        relative_path="raw/01_cloakbrowser_rendered_dom.html",
        body=body,
        surface="cloakbrowser_snapshot",
    )

    projection = build_retail_grid_projection(
        packet=packet, raw_file_bytes_by_file_id={"file_01": body}
    )

    assert projection.completeness.status == "incomplete"
    assert projection.completeness.termination == "unproven"
    assert "ulta_grid_load_more_control_still_present" in projection.completeness.residuals
    assert any("viewed_count_stale" in value for value in projection.residuals)


def _ulta_grid_html(*, viewed: int = 3, load_more: bool = False) -> str:
    def card(
        *, sku: str, href: str, name: str, price: str, rating: str, variant: str
    ) -> str:
        return (
            f'<li data-test="products-list-item" data-sku-id="{sku}">'
            f'<a href="{href}">'
            '<span class="pal-c-ProductCardBody--brandName">Clinique</span>'
            f'<span class="pal-c-ProductCardBody--title">{name}</span></a>'
            f'<span class="pal-c-ProductCardBody--price">{price}</span>'
            f'<span class="pal-c-Ratings"><span class="sr-only">{rating}</span></span>'
            f'<span class="pal-c-ProductCardHeader__variant">{variant}</span>'
            "<button>Add to bag</button></li>"
        )

    cards = [
        card(
            sku="2639131",
            href="/p/moisture-surge-100h-auto-replenishing-hydrator-pimprod2056072?sku=2639131",
            name="Moisture Surge 100H Auto-Replenishing Hydrator",
            price="$18.00 - $89.00",
            rating="4.6 out of 5 stars ; 4,253 reviews",
            variant="5 sizes",
        ),
        card(
            sku="2253011",
            href="https://www.ulta.com/p/almost-lipstick-VP11111?sku=2253011",
            name="Almost Lipstick",
            price="$25.00",
            rating="4.5 out of 5 stars ; 2,100 reviews",
            variant="2 colors",
        ),
        card(
            sku="2639131",
            href="/p/moisture-surge-100h-auto-replenishing-hydrator-pimprod2056072?sku=2639131",
            name="Moisture Surge 100H Auto-Replenishing Hydrator",
            price="$18.00 - $89.00",
            rating="4.6 out of 5 stars ; 4,253 reviews",
            variant="5 sizes",
        ),
    ]
    button = '<button class="LoadContent__button">Load More</button>' if load_more else ""
    return (
        '<html lang="en-US"><head><script>window.__APP_LOCALE__="en-US";'
        'fetch("/graphql?ultasite=en-us")</script></head><body>'
        '<h1>Clinique</h1><ul data-test="products-list">'
        + "".join(cards)
        + "</ul>"
        + f"<p>You have viewed {viewed} of 3</p>{button}</body></html>"
    )
