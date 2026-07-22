from __future__ import annotations

import json

import pytest

import source_capture.retail_pdp_projection as retail_pdp_projection
from data_lake.root import DataLakeRoot
from runners.run_source_capture_cloakbrowser_packet import (
    _sephora_content_extraction_spec,
)
from source_capture.content_extraction import RenderedContentExtractionSpec
from source_capture.models import SourceCapturePacket, known_fact
from source_capture.retail_pdp_content import load_retail_pdp_content_record
from source_capture.retail_pdp_projection import (
    SEPHORA_PDP_CONTENT_SCHEMA_VERSION,
    SEPHORA_PDP_PARSER_VERSION,
    build_sephora_pdp_aggregate_content_record,
)
from source_capture.writer import write_local_source_capture_packet


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


def _synthetic_sephora_html(product: dict | None = None) -> bytes:
    product = _synthetic_product() if product is None else product
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


def test_sephora_v4_deduplicates_without_losing_source_fields() -> None:
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


@pytest.mark.parametrize("absent_field", ["regularChildSkus", "reviewImages"])
def test_sephora_v4_preserves_absent_canonical_field_semantics(
    absent_field: str,
) -> None:
    product = _synthetic_product()
    product.pop(absent_field)

    record = build_sephora_pdp_aggregate_content_record(
        rendered_dom=_synthetic_sephora_html(product),
        visible_text=b"Lip Sleeping Mask\nBerry\n$24.00\nFive stars.",
        source_url=SOURCE_URL,
    )

    product_source = _row(
        record,
        structured="sephora_link_store_product",
    )["source_visible_fields"]
    assert absent_field not in product_source["deduplicated_canonical_fields"]


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


@pytest.mark.parametrize(
    ("broken_row_kind", "broken_field", "expected_error"),
    (
        (
            "retail_variant_offer",
            "product_details_state",
            "cannot reconstruct linkStore.page.product.productDetails",
        ),
        (
            "retail_review_substrate",
            "displayed_review_rows",
            "does not reconstruct rendered interactions",
        ),
    ),
)
def test_sephora_v4_fails_loud_when_canonical_rows_cannot_reconstruct(
    monkeypatch: pytest.MonkeyPatch,
    broken_row_kind: str,
    broken_field: str,
    expected_error: str,
) -> None:
    project_retail_html = retail_pdp_projection._project_retail_html

    def project_with_broken_canonical_row(*args, **kwargs):
        projected = project_retail_html(*args, **kwargs)
        rows = []
        for row in projected.rows:
            if row.row_kind != broken_row_kind:
                rows.append(row)
                continue
            fields = dict(row.source_visible_fields)
            if broken_field == "displayed_review_rows":
                fields[broken_field] = []
            else:
                fields.pop(broken_field)
            rows.append(row.model_copy(update={"source_visible_fields": fields}))
        return projected.model_copy(update={"rows": rows})

    monkeypatch.setattr(
        retail_pdp_projection,
        "_project_retail_html",
        project_with_broken_canonical_row,
    )

    with pytest.raises(ValueError, match=expected_error):
        build_sephora_pdp_aggregate_content_record(
            rendered_dom=_synthetic_sephora_html(),
            visible_text=b"Lip Sleeping Mask\nBerry\n$24.00\nFive stars.",
            source_url=SOURCE_URL,
        )


def test_historical_sephora_v3_content_remains_loader_readable(tmp_path) -> None:
    record = build_sephora_pdp_aggregate_content_record(
        rendered_dom=_synthetic_sephora_html(),
        visible_text=b"Lip Sleeping Mask\nBerry\n$24.00\nFive stars.",
        source_url=SOURCE_URL,
    )
    record["schema_version"] = "retail_pdp_sephora_aggregate_content_v3"
    record["parser_version"] = "retail_pdp_sephora_aggregate_parser_v3"
    extraction_metadata = {
        "extractor_version": record["parser_version"],
        "extraction_status": "succeeded",
        "retention_outcome": "content",
    }
    browser_metadata = {
        "retail_capture_profile": {"name": "sephora_pdp_aggregate"},
        "pin_confirmed": True,
        "pre_capture_attempted": True,
    }

    def write_json(name: str, value: object):
        path = tmp_path / name
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    root = DataLakeRoot.for_test(tmp_path / "lake")
    written = write_local_source_capture_packet(
        data_root=root,
        input_files=[
            write_json("content_record.json", record),
            write_json("content_extraction_metadata.json", extraction_metadata),
            write_json("cloakbrowser_snapshot_metadata.json", browser_metadata),
        ],
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        source_locator=known_fact(SOURCE_URL),
        decision_question="Can historical Sephora content still load?",
        capture_context="historical Sephora v3 loader regression",
    )
    loaded = root.load_raw_packet(written.packet.packet_id)

    content_file, loaded_record = load_retail_pdp_content_record(
        packet=SourceCapturePacket.model_validate(loaded.manifest),
        file_bytes_by_file_id=loaded.bodies,
    )
    assert content_file.original_path.endswith("content_record.json")
    assert loaded_record.parser_version == "retail_pdp_sephora_aggregate_parser_v3"
