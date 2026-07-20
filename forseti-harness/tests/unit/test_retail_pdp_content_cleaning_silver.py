from __future__ import annotations

import json
from pathlib import Path

from data_lake.root import DataLakeRoot
from source_capture.models import known_fact
from source_capture.retail_pdp_projection import LUCKYSCENT_PDP_PARSER_VERSION
from source_capture.retail_pdp_silver import derive_retail_pdp_silver
from source_capture.writer import write_local_source_capture_packet


_URL = "https://www.luckyscent.com/products/bread-and-roses-by-pearfat-parfum"


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
