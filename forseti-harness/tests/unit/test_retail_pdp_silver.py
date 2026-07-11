from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from data_lake.lane_registry import LaneRole, role_of
from data_lake.root import DataLakeRoot
from data_lake.silver_lineage import is_silver_record_source_backed_complete
from source_capture.models import known_fact
from source_capture.retail_pdp_projection import (
    PROJECTION_RETAIL_PDP_LANE,
    project_retail_pdp_into_lake,
)
from source_capture.retail_pdp_silver import (
    RETAIL_PDP_SILVER_LANE,
    RetailPdpSilverError,
    derive_retail_pdp_silver_from_projection,
)
from source_capture.writer import write_local_source_capture_packet


_AMAZON_HTML = """<!doctype html>
<html><body>
<input id="ASIN" value="B012345678">
<input name="items[0.base][customerVisiblePrice][amount]" value="24.99">
<div id="availability">In Stock</div>
<div id="averageCustomerReviews">
  <span>4.6 out of 5 stars</span>
  <span id="acrCustomerReviewText">36,799 global ratings</span>
</div>
<p>Best Sellers Rank: #12 in Beauty</p>
</body></html>
"""


def _capture_and_project(root: DataLakeRoot, tmp_path: Path) -> tuple[str, Path]:
    source = tmp_path / "amazon.html"
    visible_text = tmp_path / "amazon.txt"
    source.write_text(_AMAZON_HTML, encoding="utf-8")
    visible_text.write_text(
        "In Stock\n4.6 out of 5 stars\n36,799 global ratings\nBest Sellers Rank: #12 in Beauty\n",
        encoding="utf-8",
    )
    written = write_local_source_capture_packet(
        data_root=root,
        input_files=[source, visible_text],
        source_family="retail_pdp",
        source_surface="amazon_product_detail",
        source_locator=known_fact("https://www.amazon.com/dp/B012345678"),
        decision_question="source-visible offer and review state?",
        capture_context="Retail/PDP Silver unit proof",
    )
    _, projection_path = project_retail_pdp_into_lake(
        data_root=root, packet_id=written.packet.packet_id
    )
    return written.packet.packet_id, projection_path


def _computed_content_hash(record: dict) -> str:
    body = dict(record)
    body.pop("content_hash")
    encoded = json.dumps(
        body,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def test_amazon_projection_emits_generic_source_backed_silver(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    packet_id, projection_path = _capture_and_project(root, tmp_path)

    result = derive_retail_pdp_silver_from_projection(
        data_root=root,
        packet_id=packet_id,
        projection_record_id=projection_path.name,
    )

    assert role_of(RETAIL_PDP_SILVER_LANE) is LaneRole.SILVER_ENVELOPE
    assert [record["payload_kind"] for record in result.records] == [
        "ProductEntity",
        "RetailOfferObservation",
        "RetailReviewAggregateObservation",
    ]
    assert len(result.paths) == 3
    assert all(path.parent.name == RETAIL_PDP_SILVER_LANE for path in result.paths)
    assert all(is_silver_record_source_backed_complete(record) for record in result.records)
    assert all(record["content_hash"] == _computed_content_hash(record) for record in result.records)

    entity = result.records[0]["payload"]["entity"]
    assert entity["entity_key"] == {
        "namespace": "retail_pdp:amazon",
        "kind": "retailer_product",
        "native_id": "B012345678",
    }
    offer_fields = result.records[1]["payload"]["observation"]["source_visible_fields"]
    assert offer_fields["price"] == "24.99"
    assert offer_fields["availability"] == "In Stock"
    assert "exact_inventory_quantity" not in offer_fields
    assert "sold_units" not in offer_fields
    review_fields = result.records[2]["payload"]["observation"]["source_visible_fields"]
    assert review_fields["review_count"] == "36,799"
    assert "Best Sellers Rank" in review_fields["best_sellers_rank_text"]

    projection_sha256 = hashlib.sha256(projection_path.read_bytes()).hexdigest()
    for record in result.records:
        assert record["lane_namespace"] == RETAIL_PDP_SILVER_LANE
        assert record["schema_version"] == "silver_vault_record_v0"
        assert record["non_claims"] == [
            "not_cleaning",
            "not_complete_amazon_demand_projection",
            "not_exact_inventory_quantity",
            "not_exact_sold_units",
            "not_judgment",
            "not_sibling_selection_policy",
        ]
        for ref in record["derived_refs"]:
            assert ref["lane"] == PROJECTION_RETAIL_PDP_LANE
            assert ref["record_id"] == projection_path.name
            assert ref["sha256"] == projection_sha256
            assert ref["hash_basis"] == "derived_record_bytes"
            assert ref["row_locator"]["row_kind"] in {
                "retail_pdp_product",
                "retail_variant_offer",
                "retail_review_substrate",
            }


def test_missing_exact_projection_fails_without_silver_write(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    packet_id, _ = _capture_and_project(root, tmp_path)

    with pytest.raises(RetailPdpSilverError, match="does not exist"):
        derive_retail_pdp_silver_from_projection(
            data_root=root,
            packet_id=packet_id,
            projection_record_id="missing.json",
        )

    assert not root.lane_dir(
        subtree="derived", raw_anchor=packet_id, lane=RETAIL_PDP_SILVER_LANE
    ).exists()


def test_raw_ref_drift_fails_before_any_silver_write(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    packet_id, projection_path = _capture_and_project(root, tmp_path)
    projection = json.loads(projection_path.read_text(encoding="utf-8"))
    projection["rows"][0]["raw_anchor"]["sha256"] = "0" * 64
    corrupted = root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=PROJECTION_RETAIL_PDP_LANE,
        record_id="corrupted.json",
        data=(json.dumps(projection, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )

    with pytest.raises(RetailPdpSilverError, match="does not match the committed packet"):
        derive_retail_pdp_silver_from_projection(
            data_root=root,
            packet_id=packet_id,
            projection_record_id=corrupted.name,
        )

    assert not root.lane_dir(
        subtree="derived", raw_anchor=packet_id, lane=RETAIL_PDP_SILVER_LANE
    ).exists()


def test_projection_without_variant_refuses_empty_success(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    packet_id, projection_path = _capture_and_project(root, tmp_path)
    projection = json.loads(projection_path.read_text(encoding="utf-8"))
    projection["rows"] = [
        row for row in projection["rows"] if row["row_kind"] != "retail_variant_offer"
    ]
    projection["loss_ledger"]["preserved_evidence_rows"] = len(projection["rows"])
    no_variant = root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=PROJECTION_RETAIL_PDP_LANE,
        record_id="no-variant.json",
        data=(json.dumps(projection, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )

    with pytest.raises(RetailPdpSilverError, match="refusing an empty Silver success"):
        derive_retail_pdp_silver_from_projection(
            data_root=root,
            packet_id=packet_id,
            projection_record_id=no_variant.name,
        )

    assert not root.lane_dir(
        subtree="derived", raw_anchor=packet_id, lane=RETAIL_PDP_SILVER_LANE
    ).exists()
