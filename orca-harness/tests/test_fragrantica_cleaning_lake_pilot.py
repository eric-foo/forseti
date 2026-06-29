from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from cleaning import CleaningPacket
from cleaning.fragrantica import build_fragrantica_cleaning_packet
from cleaning.fragrantica_lake import (
    CLEANING_AUDIT_PACK_SCHEMA_VERSION,
    DISCRIMINATOR_LOCALITY_NON_CLAIM,
    FRAGRANTICA_CLEANING_AUDIT_LANE,
    FRAGRANTICA_CLEANING_SILVER_LANE,
    derive_fragrantica_cleaning_into_lake,
    fragrantica_cleaning_audit_pack_payload,
)
from data_lake.root import DataLakeRoot, DataLakeRootError, raw_shard
from source_capture.fragrantica_projection import build_fragrantica_projection
from source_capture.models import (
    PacketTiming,
    SourceCapturePacket,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.writer import write_local_source_capture_packet


_CAPTURE_TIME = "2026-06-28T18:57:58Z"


def test_derives_fragrantica_cleaning_into_audit_pack_and_silver(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_fragrantica_packet(root, tmp_path)

    result = derive_fragrantica_cleaning_into_lake(data_root=root, packet_id=packet_id)

    # --- Audit pack: a derived processing-audit sibling, NOT a Silver fact ---
    audit_path = result.audit_path
    assert audit_path.parent == (
        root.path / "derived" / raw_shard(packet_id) / packet_id / FRAGRANTICA_CLEANING_AUDIT_LANE
    )
    assert audit_path.suffix == ".json"
    assert audit_path.is_file()

    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    assert audit["schema_version"] == CLEANING_AUDIT_PACK_SCHEMA_VERSION
    assert audit["record_family"] == "processing_audit"
    assert audit["audit_kind"] == "cleaning_transform_audit"
    assert "record_kind" not in audit, "audit pack is not a Silver fact record"
    assert audit["raw_anchor"] == packet_id
    assert audit["lane_namespace"] == FRAGRANTICA_CLEANING_AUDIT_LANE
    assert audit["content_hash"] == f"sha256:{_content_hash(audit)}"
    assert audit["content_hash_basis"] == "canonical_json_excluding_content_hash"
    assert audit["source_family"] == "fragrance_native_database"
    assert audit["source_surface"] == "fragrantica_product_page_direct_http"

    # Full transform ledger round-trips inside the audit pack.
    round_tripped = CleaningPacket.model_validate(audit["payload"]["cleaning_packet"])
    assert len(round_tripped.handles) == len(result.cleaning_packet.handles)
    assert len(round_tripped.transform_ledger) == len(result.cleaning_packet.transform_ledger)
    assert audit["payload"]["transform_entry_count"] == len(result.cleaning_packet.transform_ledger)

    # Anti-lock-in guard: discriminator locality is asserted explicitly.
    assert DISCRIMINATOR_LOCALITY_NON_CLAIM in audit["non_claims"]
    assert "not_silver_fact" in audit["non_claims"]

    # --- Post-cleaned Silver: TextObservation linking back to the audit pack ---
    assert result.silver_paths, "expected at least one post-cleaned Silver record"
    for silver_path in result.silver_paths:
        assert silver_path.parent == (
            root.path / "derived" / raw_shard(packet_id) / packet_id / FRAGRANTICA_CLEANING_SILVER_LANE
        )

    silver = json.loads(result.silver_paths[0].read_text(encoding="utf-8"))
    assert silver["schema_version"] == "silver_vault_record_v0"
    assert silver["record_kind"] == "observation"
    assert silver["payload_kind"] == "TextObservation"
    assert silver["lane_namespace"] == FRAGRANTICA_CLEANING_SILVER_LANE
    assert silver["content_hash"] == f"sha256:{_content_hash(silver)}"

    observation = silver["payload"]["observation"]
    assert observation["text_artifact_type"] == "review_body"
    assert observation["text_value"] == "This perfume died young."
    assert observation["text_hash"] == (
        "sha256:" + hashlib.sha256(observation["text_value"].encode("utf-8")).hexdigest()
    )
    assert observation["text_posture"]["kind"] == "observed"

    # Real linkage in the STANDARD header field (derived_refs), not a sidecar:
    # the Silver record is generated from the audit pack, so derived_refs must
    # carry the same audit record id + content hash.
    audit_refs = [r for r in silver["derived_refs"] if r["record_id"] == audit["record_id"]]
    assert len(audit_refs) == 1, "Silver record must reference the audit pack in derived_refs"
    pointer = audit_refs[0]
    assert pointer["edge_type"] == "derived_from_record"
    assert pointer["lane_namespace"] == FRAGRANTICA_CLEANING_AUDIT_LANE
    assert pointer["content_hash"] == audit["content_hash"]
    assert silver["provenance"]["cleaning_method_id"] == "fragrantica_cleaning_method_v0"


def test_fragrantica_cleaning_emits_no_silver_wrapped_full_packet(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_fragrantica_packet(root, tmp_path)

    derive_fragrantica_cleaning_into_lake(data_root=root, packet_id=packet_id)

    # No derived record anywhere wraps the full CleaningPacket as a Silver record.
    for path in (root.path / "derived").rglob("*.json"):
        record = json.loads(path.read_text(encoding="utf-8"))
        assert record.get("payload_kind") != "FragranticaCleaningPacket"
        if record.get("schema_version") == "silver_vault_record_v0":
            assert record["payload_kind"] == "TextObservation"
            assert "cleaning_packet" not in record.get("payload", {})


def test_fragrantica_cleaning_audit_pack_rejects_unknown_capture_time(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_fragrantica_packet(root, tmp_path)
    loaded = root.load_raw_packet(packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    packet = packet.model_copy(
        update={
            "timing": packet.timing.model_copy(
                update={"capture_time": unknown_with_reason("fixture hides capture time")}
            )
        }
    )
    projection = build_fragrantica_projection(
        packet=packet,
        raw_file_bytes_by_file_id=loaded.bodies,
    )
    cleaning_packet = build_fragrantica_cleaning_packet(projection)

    with pytest.raises(ValueError, match="known capture_time"):
        fragrantica_cleaning_audit_pack_payload(
            packet=packet,
            cleaning_packet=cleaning_packet,
            record_id="rec.json",
        )


def test_fragrantica_cleaning_audit_pack_preserves_current_window_residuals(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_fragrantica_packet(root, tmp_path)

    result = derive_fragrantica_cleaning_into_lake(data_root=root, packet_id=packet_id)

    audit = json.loads(result.audit_path.read_text(encoding="utf-8"))
    coverage = audit["coverage"]
    assert coverage["current_window_only"] is True
    assert coverage["full_archive_captured"] is False
    assert "full_review_archive_not_captured_login_prompt_present" in coverage["residuals"]
    assert "inspect_raw_before_archive_completeness_claim" in coverage["raw_pull_triggers"]
    assert "not_judgment" in audit["non_claims"]
    assert "not_demand_signal" in audit["non_claims"]
    assert "not_sentiment_analysis" in audit["non_claims"]


def test_fragrantica_cleaning_re_derive_appends_audit_sibling_not_overwrite(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_fragrantica_packet(root, tmp_path)

    first = derive_fragrantica_cleaning_into_lake(data_root=root, packet_id=packet_id)
    second = derive_fragrantica_cleaning_into_lake(data_root=root, packet_id=packet_id)

    audit_dir = root.path / "derived" / raw_shard(packet_id) / packet_id / FRAGRANTICA_CLEANING_AUDIT_LANE
    assert first.audit_path != second.audit_path
    assert len(list(audit_dir.glob("*.json"))) == 2


def test_fragrantica_cleaning_explicit_audit_record_id_is_create_only(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_fragrantica_packet(root, tmp_path)

    first = derive_fragrantica_cleaning_into_lake(
        data_root=root,
        packet_id=packet_id,
        record_id="rec1",
    )
    with pytest.raises(DataLakeRootError):
        derive_fragrantica_cleaning_into_lake(
            data_root=root,
            packet_id=packet_id,
            record_id="rec1",
        )
    assert first.audit_path.read_text(encoding="utf-8")


def test_fragrantica_cleaning_emits_one_silver_per_review_card(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_fragrantica_packet(root, tmp_path, html=_html_two_reviews())

    result = derive_fragrantica_cleaning_into_lake(data_root=root, packet_id=packet_id)

    # One post-cleaned Silver TextObservation per review-card handle (here: 2),
    # each linking to the SAME single audit pack.
    assert len(result.silver_paths) == 2
    audit = json.loads(result.audit_path.read_text(encoding="utf-8"))
    texts: set[str] = set()
    for silver_path in result.silver_paths:
        record = json.loads(silver_path.read_text(encoding="utf-8"))
        assert record["payload_kind"] == "TextObservation"
        texts.add(record["payload"]["observation"]["text_value"])
        refs = [r for r in record["derived_refs"] if r["record_id"] == audit["record_id"]]
        assert len(refs) == 1
        assert refs[0]["content_hash"] == audit["content_hash"]
    assert texts == {"This perfume died young.", "Smells like heaven all day."}


def _commit_fragrantica_packet(root: DataLakeRoot, tmp_path: Path, html: str | None = None) -> str:
    body_path = tmp_path / "http_response_body.bin"
    body_path.write_text(html if html is not None else _html(), encoding="utf-8")
    metadata_path = tmp_path / "http_response_metadata.json"
    metadata_path.write_text('{"status": 200}\n', encoding="utf-8")

    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason("fixture does not supply source event timing"),
        source_edit_or_version=unknown_with_reason("fixture does not supply edit timing"),
        capture_time=known_fact(_CAPTURE_TIME),
        recapture_time=not_applicable("first capture"),
        cutoff_posture=unknown_with_reason("test fixture has no decision cutoff"),
    )
    source_slice = SourceCaptureSlice(
        slice_id="slice_01",
        locator=known_fact(
            "https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html"
        ),
        timing=timing,
        access_posture=known_fact("direct HTTP fixture supplied"),
        archive_history_posture=not_attempted("archive not queried"),
        media_modality_posture=not_attempted("linked media not fetched"),
        re_capture_relationship=not_applicable("first capture"),
        limitations=[],
        warning_notes=[],
        preserved_file_ids=["file_01", "file_02"],
    )
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[body_path, metadata_path],
        source_family="fragrance_native_database",
        source_surface="fragrantica_product_page_direct_http",
        source_locator=known_fact(
            "https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html"
        ),
        decision_question="test Fragrantica Cleaning into lake",
        capture_context="fragrantica cleaning lake pilot",
        source_slices=[source_slice],
    )
    return result.packet.packet_id


def _html() -> str:
    return """
    <html><head>
      <link rel="canonical" href="https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html"/>
      <title>Baccarat Rouge 540 Maison Francis Kurkdjian perfume</title>
    </head><body>
      <div id="perfume-description-content" itemprop="description">
        <p><b>Baccarat Rouge 540</b> by <b>Maison Francis Kurkdjian</b> is a fragrance. Baccarat Rouge 540 was launched in 2015.</p>
      </div>
      <p itemprop="aggregateRating"><span itemprop="ratingValue">3.76</span><span itemprop="bestRating">5</span><span itemprop="ratingCount" content="28808">28,808</span></p>
      <span>Reviews (<span>3.9K</span>)</span>
      <button data-tab="all-reviews" data-active="true">All reviews by date</button>
      <div class="review-tab-panel" id="all-reviews">
        <div id="parent3090334" class="cell tw-review-card tw-gradient-rose" itemprop="review" itemscope>
          <user-perfume-votes-new :perfume-votes="{&quot;rating&quot;:5,&quot;winter&quot;:0,&quot;spring&quot;:0,&quot;summer&quot;:0,&quot;autumn&quot;:0,&quot;day&quot;:0,&quot;night&quot;:0,&quot;longevity&quot;:3,&quot;sillage&quot;:2,&quot;gender&quot;:&quot;female_unisex&quot;,&quot;relation&quot;:&quot;have&quot;}"></user-perfume-votes-new>
          <meta itemprop="name" content="Rimazy"/>
          <span itemprop="datePublished" content="2026-06-25">06/25/26 18:41</span>
          <div id="review_3090334"><p>This perfume died young.</p></div>
          <vote-buttons-new initial-status="neutral" item-id="33519" comment-id="3090334" vote-for="perfumeReview"></vote-buttons-new>
          <share-new path="/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html?ccid=3090334#focus-zone"></share-new>
        </div>
        <reviews-infinity-new :perfume-id="33519" sentiment="all" :is-logged="false" login-url="/board/login.php"
          :lang-strings="{&quot;loginPromptMessage&quot;:&quot;Sign in to access the full review archive&quot;}">
        </reviews-infinity-new>
      </div>
    </body></html>
    """


def _html_two_reviews() -> str:
    second_card = """
        <div id="parent3090335" class="cell tw-review-card tw-gradient-rose" itemprop="review" itemscope>
          <user-perfume-votes-new :perfume-votes="{&quot;rating&quot;:4,&quot;longevity&quot;:4,&quot;sillage&quot;:3,&quot;gender&quot;:&quot;unisex&quot;,&quot;relation&quot;:&quot;had&quot;}"></user-perfume-votes-new>
          <meta itemprop="name" content="Lyra"/>
          <span itemprop="datePublished" content="2026-06-24">06/24/26 09:12</span>
          <div id="review_3090335"><p>Smells like heaven all day.</p></div>
          <vote-buttons-new initial-status="neutral" item-id="33519" comment-id="3090335" vote-for="perfumeReview"></vote-buttons-new>
          <share-new path="/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html?ccid=3090335#focus-zone"></share-new>
        </div>
"""
    return _html().replace(
        "        <reviews-infinity-new",
        second_card + "        <reviews-infinity-new",
    )


def _content_hash(record: dict[str, Any]) -> str:
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
