"""End-to-end no-blur proof: capture -> projection -> Cleaning audit -> Silver.

This is the first test that walks the whole Fragrantica path in a single run and
asserts the layer-separation invariant the long-term goal names: the raw
capture, the mechanical projection, the Cleaning audit pack (processing
evidence), and the post-cleaned Silver fact each stay a DISTINCT persisted
representation with its own declared role, while one raw anchor threads the
lineage end to end.

Scope fence: this proof stays inside the capture / projection / Cleaning / Silver
lanes. The ECR reference is asserted only as the by-convention reference the
Cleaning layer already emits; it reads and requires no physical ECR record and
no Judgment (JSG-01) gate state.
"""
from __future__ import annotations

import json
from pathlib import Path

from cleaning.fragrantica_lake import (
    FRAGRANTICA_CLEANING_AUDIT_LANE,
    FRAGRANTICA_CLEANING_SILVER_LANE,
    derive_fragrantica_cleaning_into_lake,
)
from data_lake.root import DataLakeRoot, raw_shard
from source_capture.fragrantica_projection import (
    FRAGRANTICA_PROJECTION_CERTIFICATION,
    PROJECTION_FRAGRANTICA_LANE,
    project_fragrantica_into_lake,
)
from source_capture.models import (
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.writer import write_local_source_capture_packet


_CAPTURE_TIME = "2026-06-28T18:57:58Z"
_REVIEW_TEXT = "This perfume died young."


def test_capture_to_silver_persists_four_distinct_layers(tmp_path: Path) -> None:
    """raw, projection, Cleaning audit, and Silver coexist as distinct records.

    Each layer carries the same review content in its own representation and
    declares its own role; none impersonates another.
    """
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_fragrantica_packet(root, tmp_path)

    projection, projection_path = project_fragrantica_into_lake(
        data_root=root, packet_id=packet_id
    )
    result = derive_fragrantica_cleaning_into_lake(data_root=root, packet_id=packet_id)

    derived_root = root.path / "derived" / raw_shard(packet_id) / packet_id

    # Four distinct persisted homes under one raw anchor.
    assert projection_path.parent == derived_root / PROJECTION_FRAGRANTICA_LANE
    assert result.audit_path.parent == derived_root / FRAGRANTICA_CLEANING_AUDIT_LANE
    assert result.silver_paths
    assert (
        result.silver_paths[0].parent
        == derived_root / FRAGRANTICA_CLEANING_SILVER_LANE
    )

    # RAW: HTML bytes that still carry markup and the surrounding page.
    raw_html = _raw_html_body(root, packet_id)
    assert f"<p>{_REVIEW_TEXT}</p>" in raw_html
    assert "tw-review-card" in raw_html

    # PROJECTION: a structured, explicitly NOT-cleaned view-only record.
    projection_record = json.loads(projection_path.read_text(encoding="utf-8"))
    assert projection_record["certification"] == FRAGRANTICA_PROJECTION_CERTIFICATION
    assert "not_cleaned" in projection_record["certification"]
    assert "not_judgment_ready" in projection_record["certification"]
    review_row = next(
        row
        for row in projection.rows
        if row.row_kind == "fragrance_review_card_current_window"
    )
    projected_text = review_row.source_visible_fields["review_text"]

    # CLEANING audit pack: processing evidence, NOT a Silver fact.
    audit = json.loads(result.audit_path.read_text(encoding="utf-8"))
    assert "record_kind" not in audit
    assert audit["record_family"] == "processing_audit"
    assert "not_silver_fact" in audit["non_claims"]
    assert "cleaning_packet" in audit["payload"]  # carries the transform ledger

    # SILVER: a fact record, NOT evidence. Find the review-body TextObservation
    # (the lane now also emits vote MetricObservations).
    silver_records = [
        json.loads(p.read_text(encoding="utf-8")) for p in result.silver_paths
    ]
    silver = next(r for r in silver_records if r["payload_kind"] == "TextObservation")
    assert silver["record_kind"] == "observation"
    assert silver["payload_kind"] == "TextObservation"
    assert "cleaning_packet" not in silver["payload"]
    assert "transform_ledger" not in json.dumps(silver)
    cleaned_text = silver["payload"]["observation"]["text_value"]

    # No blurring: one review content, distinct representations + roles.
    #  - raw keeps HTML markup; the Silver fact carries none.
    #  - projection holds the text as one field of a not_cleaned row.
    #  - the value itself is carried faithfully end to end.
    assert "<" not in cleaned_text
    assert projected_text == cleaned_text == _REVIEW_TEXT


def test_capture_to_silver_threads_one_lineage_end_to_end(tmp_path: Path) -> None:
    """One raw anchor threads raw -> projection -> audit -> Silver, no break."""
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_fragrantica_packet(root, tmp_path)

    projection, _ = project_fragrantica_into_lake(data_root=root, packet_id=packet_id)
    result = derive_fragrantica_cleaning_into_lake(data_root=root, packet_id=packet_id)

    audit = json.loads(result.audit_path.read_text(encoding="utf-8"))
    silver_records = [
        json.loads(p.read_text(encoding="utf-8")) for p in result.silver_paths
    ]
    silver = next(r for r in silver_records if r["payload_kind"] == "TextObservation")

    # The same raw anchor appears at every layer.
    assert projection.packet_id == packet_id
    assert audit["raw_anchor"] == packet_id
    assert silver["raw_anchor"] == packet_id
    assert silver["raw_refs"][0]["packet_id"] == packet_id
    assert audit["input_refs"]["raw_refs"][0]["packet_id"] == packet_id

    # Silver -> audit pack via the standard derived_refs header edge.
    pointer = next(
        ref for ref in silver["derived_refs"] if ref["record_id"] == audit["record_id"]
    )
    assert pointer["edge_type"] == "derived_from_record"
    assert pointer["lane_namespace"] == FRAGRANTICA_CLEANING_AUDIT_LANE
    assert pointer["content_hash"] == audit["content_hash"]

    # Projection -> audit: the review row that became the Silver fact is recorded
    # in the audit pack's projection lineage.
    review_row = next(
        row
        for row in projection.rows
        if row.row_kind == "fragrance_review_card_current_window"
    )
    audit_projection_row_ids = {
        ref["row_id"] for ref in audit["input_refs"]["projection_refs"]
    }
    assert review_row.row_id in audit_projection_row_ids

    # ECR stays a by-convention REFERENCE only (Judgment / JSG-01 out of scope):
    # the chain references ECR without resolving or existence-checking a record.
    ecr_refs = audit["input_refs"]["ecr_refs"]
    assert ecr_refs
    assert all(
        ref["status"] == "by_convention_not_existence_checked" for ref in ecr_refs
    )


def _raw_html_body(root: DataLakeRoot, packet_id: str) -> str:
    loaded = root.load_raw_packet(packet_id)
    for body in loaded.bodies.values():
        decoded = body.decode("utf-8", errors="ignore")
        if "tw-review-card" in decoded:
            return decoded
    raise AssertionError("raw packet body with review markup not found")


def _commit_fragrantica_packet(root: DataLakeRoot, tmp_path: Path) -> str:
    body_path = tmp_path / "http_response_body.bin"
    body_path.write_text(_html(), encoding="utf-8")
    metadata_path = tmp_path / "http_response_metadata.json"
    metadata_path.write_text('{"status": 200}\n', encoding="utf-8")

    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason(
            "fixture does not supply source event timing"
        ),
        source_edit_or_version=unknown_with_reason(
            "fixture does not supply edit timing"
        ),
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
        decision_question="capture-to-Silver e2e no-blur proof",
        capture_context="fragrantica capture to silver e2e",
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
