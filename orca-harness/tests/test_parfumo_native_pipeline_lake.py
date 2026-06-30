from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from cleaning import CleaningPacket
from cleaning.parfumo_lake import (
    CLEANING_AUDIT_PACK_SCHEMA_VERSION,
    DISCRIMINATOR_LOCALITY_NON_CLAIM,
    PARFUMO_CLEANING_AUDIT_LANE,
    PARFUMO_CLEANING_SILVER_LANE,
    derive_parfumo_cleaning_into_lake,
)
from data_lake.root import DataLakeRoot, DataLakeRootError, raw_shard
from source_capture.models import known_fact
from source_capture.parfumo_projection import (
    PARFUMO_PROJECTION_CERTIFICATION,
    PROJECTION_PARFUMO_LANE,
    project_parfumo_into_lake,
)
from source_capture.writer import write_local_source_capture_packet


_LOCATOR = "https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum"
_REVIEW_TEXT = "This perfume died young."
_STATEMENT_TEXT = "Airy amber trail."


def test_parfumo_projection_and_cleaning_persist_distinct_lake_layers(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_packet(root, tmp_path)

    projection, projection_path = project_parfumo_into_lake(data_root=root, packet_id=packet_id)
    result = derive_parfumo_cleaning_into_lake(data_root=root, packet_id=packet_id)

    derived_root = root.path / "derived" / raw_shard(packet_id) / packet_id
    assert projection_path.parent == derived_root / PROJECTION_PARFUMO_LANE
    assert result.audit_path.parent == derived_root / PARFUMO_CLEANING_AUDIT_LANE
    assert result.silver_paths
    assert all(path.parent == derived_root / PARFUMO_CLEANING_SILVER_LANE for path in result.silver_paths)

    raw_html = _raw_html_body(root, packet_id)
    assert f"<p data-role=\"review-text\">{_REVIEW_TEXT}</p>" in raw_html
    assert f"<p data-role=\"statement-text\">{_STATEMENT_TEXT}</p>" in raw_html

    projection_record = json.loads(projection_path.read_text(encoding="utf-8"))
    assert projection_record["certification"] == PARFUMO_PROJECTION_CERTIFICATION
    assert projection.loss_ledger.preserved_review_cards == 1
    assert projection.loss_ledger.preserved_statements == 1

    audit = json.loads(result.audit_path.read_text(encoding="utf-8"))
    assert audit["schema_version"] == CLEANING_AUDIT_PACK_SCHEMA_VERSION
    assert audit["record_family"] == "processing_audit"
    assert "record_kind" not in audit
    assert audit["raw_anchor"] == packet_id
    assert audit["lane_namespace"] == PARFUMO_CLEANING_AUDIT_LANE
    assert audit["content_hash"] == f"sha256:{_content_hash(audit)}"
    assert "not_silver_fact" in audit["non_claims"]
    assert DISCRIMINATOR_LOCALITY_NON_CLAIM in audit["non_claims"]
    assert "full_review_corpus_not_captured_ajax_pagination_present" in audit["coverage"]["residuals"]
    assert "inspect_raw_before_review_corpus_completeness_claim" in audit["coverage"]["raw_pull_triggers"]
    assert "cleaning_packet" in audit["payload"]

    round_tripped = CleaningPacket.model_validate(audit["payload"]["cleaning_packet"])
    assert len(round_tripped.transform_ledger) == len(result.cleaning_packet.transform_ledger)

    silver_records = [json.loads(path.read_text(encoding="utf-8")) for path in result.silver_paths]
    text_by_type = {
        record["payload"]["observation"]["text_artifact_type"]: record
        for record in silver_records
        if record["payload_kind"] == "TextObservation"
    }
    assert set(text_by_type) == {"review_body", "statement_body"}
    assert text_by_type["review_body"]["payload"]["observation"]["text_value"] == _REVIEW_TEXT
    assert text_by_type["statement_body"]["payload"]["observation"]["text_value"] == _STATEMENT_TEXT
    for record in silver_records:
        assert record["schema_version"] == "silver_vault_record_v0"
        assert record["record_kind"] == "observation"
        assert record["payload_kind"] == "TextObservation"
        assert "cleaning_packet" not in record["payload"]
        assert "transform_ledger" not in json.dumps(record)
        refs = [ref for ref in record["derived_refs"] if ref["record_id"] == audit["record_id"]]
        assert len(refs) == 1
        assert refs[0]["lane_namespace"] == PARFUMO_CLEANING_AUDIT_LANE
        assert refs[0]["content_hash"] == audit["content_hash"]


def test_parfumo_projection_rederive_appends_sibling_and_explicit_id_is_create_only(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_packet(root, tmp_path)

    _, first = project_parfumo_into_lake(data_root=root, packet_id=packet_id)
    _, second = project_parfumo_into_lake(data_root=root, packet_id=packet_id)

    lane_dir = root.path / "derived" / raw_shard(packet_id) / packet_id / PROJECTION_PARFUMO_LANE
    assert first != second
    assert len(list(lane_dir.glob("*.json"))) == 2

    project_parfumo_into_lake(data_root=root, packet_id=packet_id, record_id="rec1")
    with pytest.raises(DataLakeRootError):
        project_parfumo_into_lake(data_root=root, packet_id=packet_id, record_id="rec1")


def test_parfumo_cleaning_audit_rederive_appends_sibling_and_explicit_id_is_create_only(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_packet(root, tmp_path)

    first = derive_parfumo_cleaning_into_lake(data_root=root, packet_id=packet_id)
    second = derive_parfumo_cleaning_into_lake(data_root=root, packet_id=packet_id)

    audit_dir = root.path / "derived" / raw_shard(packet_id) / packet_id / PARFUMO_CLEANING_AUDIT_LANE
    assert first.audit_path != second.audit_path
    assert len(list(audit_dir.glob("*.json"))) == 2

    derive_parfumo_cleaning_into_lake(data_root=root, packet_id=packet_id, record_id="rec1")
    with pytest.raises(DataLakeRootError):
        derive_parfumo_cleaning_into_lake(data_root=root, packet_id=packet_id, record_id="rec1")


def _raw_html_body(root: DataLakeRoot, packet_id: str) -> str:
    loaded = root.load_raw_packet(packet_id)
    for body in loaded.bodies.values():
        decoded = body.decode("utf-8", errors="ignore")
        if "data-review-id" in decoded:
            return decoded
    raise AssertionError("raw packet body with Parfumo text markup not found")


def _commit_packet(root: DataLakeRoot, tmp_path: Path) -> str:
    body_path = tmp_path / "http_response_body.bin"
    body_path.write_text(_HTML, encoding="utf-8")
    metadata_path = tmp_path / "http_response_metadata.json"
    metadata_path.write_text('{"status": 200}\n', encoding="utf-8")
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[body_path, metadata_path],
        source_family="fragrance_native_database",
        source_surface="parfumo_product_page_direct_http",
        source_locator=known_fact(_LOCATOR),
        decision_question="test Parfumo native pipeline into lake",
        capture_context="parfumo native pipeline lake fixture",
    )
    return result.packet.packet_id


def _content_hash(record: dict[str, object]) -> str:
    canonical = dict(record)
    canonical.pop("content_hash", None)
    return hashlib.sha256(
        json.dumps(
            canonical,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


_HTML = f"""
<html><head>
  <link rel="canonical" href="{_LOCATOR}"/>
  <meta name="description" content="Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian"/>
  <title>Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian (Eau de Parfum) & Perfume Facts</title>
</head><body>
  <main data-perfume-id="67720" data-rating-count="5176" data-review-count="369"
        data-statement-count="1390" data-scent-rating="7.7" data-longevity-rating="8.7"
        data-sillage-rating="8.5">
    <button data-tab="reviews" data-active="true">Reviews <span>369</span></button>
    <button data-tab="statements">Statements <span>1390</span></button>
    <input type="hidden" name="h" value="7536fa6f9c01a6637a935e7717b53101">
    <script>const routes = {{reviews: "/action/perfume/get_reviews.php", statements: "/action/perfume/get_statements.php", p_id: 67720}};</script>
    <article data-review-id="900001" data-author="Rimazy" data-rating="8.0">
      <time datetime="2026-06-25">06/25/26</time>
      <p data-role="review-text">{_REVIEW_TEXT}</p>
      <a href="/Users/rimazy">Read review</a>
    </article>
    <article data-statement-id="st7001" data-author="Lyra">
      <time datetime="2026-06-24">06/24/26</time>
      <p data-role="statement-text">{_STATEMENT_TEXT}</p>
    </article>
  </main>
</body></html>
"""
