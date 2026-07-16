from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from cleaning import CleaningPacket
from cleaning.basenotes_lake import (
    CLEANING_AUDIT_PACK_SCHEMA_VERSION,
    DISCRIMINATOR_LOCALITY_NON_CLAIM,
    BASENOTES_CLEANING_AUDIT_LANE,
    BASENOTES_CLEANING_SILVER_LANE,
    derive_basenotes_cleaning_into_lake,
)
from data_lake.root import DataLakeRoot, DataLakeRootError, raw_shard
from source_capture.models import known_fact
from source_capture.basenotes_projection import (
    BASENOTES_PROJECTION_CERTIFICATION,
    PROJECTION_BASENOTES_LANE,
    project_basenotes_into_lake,
)
from source_capture.writer import write_local_source_capture_packet


_LOCATOR = "https://basenotes.com/fragrances/mojave-ghost-by-byredo.26143979"
_SOURCE_SURFACE = "basenotes_product_page_user_cleared_persistent_chrome_current_window"
_REVIEW_TEXT = "Ectoplasmic. A wisp of something and then poof, it's gone. Spooky."
_FIXTURE = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "basenotes"
    / "mojave_ghost_product_page.html"
)


def _fixture_html() -> str:
    return _FIXTURE.read_text(encoding="utf-8")


def test_basenotes_projection_and_cleaning_persist_distinct_lake_layers(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    packet_id = _commit_packet(root, tmp_path)

    projection, projection_path = project_basenotes_into_lake(data_root=root, packet_id=packet_id)
    result = derive_basenotes_cleaning_into_lake(data_root=root, packet_id=packet_id)

    derived_root = root.path / "derived" / raw_shard(packet_id) / packet_id
    assert projection_path.parent == derived_root / PROJECTION_BASENOTES_LANE
    assert result.audit_path.parent == derived_root / BASENOTES_CLEANING_AUDIT_LANE
    assert result.silver_paths
    assert all(path.parent == derived_root / BASENOTES_CLEANING_SILVER_LANE for path in result.silver_paths)

    raw_html = _raw_html_body(root, packet_id)
    assert _REVIEW_TEXT in raw_html
    assert '"@type": "Review"' in raw_html

    projection_record = json.loads(projection_path.read_text(encoding="utf-8"))
    assert projection_record["certification"] == BASENOTES_PROJECTION_CERTIFICATION
    assert projection.loss_ledger.preserved_review_cards == 6
    assert projection.loss_ledger.preserved_statements == 0

    audit = json.loads(result.audit_path.read_text(encoding="utf-8"))
    assert audit["schema_version"] == CLEANING_AUDIT_PACK_SCHEMA_VERSION
    assert audit["record_family"] == "processing_audit"
    assert "record_kind" not in audit
    assert audit["raw_anchor"] == packet_id
    assert audit["lane_namespace"] == BASENOTES_CLEANING_AUDIT_LANE
    assert audit["content_hash"] == f"sha256:{_content_hash(audit)}"
    assert "not_silver_fact" in audit["non_claims"]
    assert DISCRIMINATOR_LOCALITY_NON_CLAIM in audit["non_claims"]
    assert "full_review_corpus_not_captured" in audit["coverage"]["residuals"]
    assert "basenotes_rating_metric_observations_deferred" in audit["coverage"]["residuals"]
    assert "inspect_raw_before_review_corpus_completeness_claim" in audit["coverage"]["raw_pull_triggers"]
    assert "cleaning_packet" in audit["payload"]

    round_tripped = CleaningPacket.model_validate(audit["payload"]["cleaning_packet"])
    assert len(round_tripped.transform_ledger) == len(result.cleaning_packet.transform_ledger)

    silver_records = [json.loads(path.read_text(encoding="utf-8")) for path in result.silver_paths]
    text_by_row_kind = {
        record["producer_row_kind"]: record
        for record in silver_records
        if record["payload_kind"] == "TextObservation"
    }
    # Basenotes has no statements surface; only review-body text observations are emitted.
    assert set(text_by_row_kind) == {"basenotes_review_body_text"}
    assert all(
        record["payload"]["observation"]["text_artifact_type"] == "review_body"
        for record in text_by_row_kind.values()
    )
    review_texts = {
        record["payload"]["observation"]["text_value"] for record in silver_records
    }
    assert _REVIEW_TEXT in review_texts
    # One Silver TextObservation per in-page review card (the 6-review JSON-LD subset).
    assert len(silver_records) == 6
    for record in silver_records:
        assert record["schema_version"] == "silver_vault_record_v0"
        assert record["record_kind"] == "observation"
        assert record["payload_kind"] == "TextObservation"
        assert "cleaning_packet" not in record["payload"]
        assert "transform_ledger" not in json.dumps(record)
        refs = [ref for ref in record["derived_refs"] if ref["record_id"] == audit["record_id"]]
        assert len(refs) == 1
        assert refs[0]["lane_namespace"] == BASENOTES_CLEANING_AUDIT_LANE
        assert refs[0]["content_hash"] == audit["content_hash"]


def test_basenotes_projection_rederive_appends_sibling_and_explicit_id_is_create_only(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    packet_id = _commit_packet(root, tmp_path)

    _, first = project_basenotes_into_lake(data_root=root, packet_id=packet_id)
    _, second = project_basenotes_into_lake(data_root=root, packet_id=packet_id)

    lane_dir = root.path / "derived" / raw_shard(packet_id) / packet_id / PROJECTION_BASENOTES_LANE
    assert first != second
    assert len(list(lane_dir.glob("*.json"))) == 2

    project_basenotes_into_lake(data_root=root, packet_id=packet_id, record_id="rec1")
    with pytest.raises(DataLakeRootError):
        project_basenotes_into_lake(data_root=root, packet_id=packet_id, record_id="rec1")


def test_basenotes_cleaning_audit_rederive_appends_sibling_and_explicit_id_is_create_only(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    packet_id = _commit_packet(root, tmp_path)

    first = derive_basenotes_cleaning_into_lake(data_root=root, packet_id=packet_id)
    second = derive_basenotes_cleaning_into_lake(data_root=root, packet_id=packet_id)

    audit_dir = root.path / "derived" / raw_shard(packet_id) / packet_id / BASENOTES_CLEANING_AUDIT_LANE
    assert first.audit_path != second.audit_path
    assert len(list(audit_dir.glob("*.json"))) == 2

    derive_basenotes_cleaning_into_lake(data_root=root, packet_id=packet_id, record_id="rec1")
    with pytest.raises(DataLakeRootError):
        derive_basenotes_cleaning_into_lake(data_root=root, packet_id=packet_id, record_id="rec1")


def _raw_html_body(root: DataLakeRoot, packet_id: str) -> str:
    loaded = root.load_raw_packet(packet_id)
    for body in loaded.bodies.values():
        decoded = body.decode("utf-8", errors="ignore")
        if '"@type": "Review"' in decoded:
            return decoded
    raise AssertionError("raw packet body with Basenotes JSON-LD review markup not found")


def _commit_packet(root: DataLakeRoot, tmp_path: Path) -> str:
    body_path = tmp_path / "browser_rendered_dom.html"
    body_path.write_text(_fixture_html(), encoding="utf-8")
    metadata_path = tmp_path / "browser_snapshot_metadata.json"
    metadata_path.write_text('{"capture_timestamp": "2026-06-30T00:00:00Z"}\n', encoding="utf-8")
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[body_path, metadata_path],
        source_family="fragrance_native_database",
        source_surface=_SOURCE_SURFACE,
        source_locator=known_fact(_LOCATOR),
        decision_question="test Basenotes native pipeline into lake",
        capture_context="basenotes native pipeline lake fixture",
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
