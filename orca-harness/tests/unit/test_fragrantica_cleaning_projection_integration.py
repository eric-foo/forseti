from __future__ import annotations

import json

from cleaning import CleaningPacket, cleaning_input_handles_from_projection_rows
from cleaning.fragrantica import (
    FRAGRANTICA_CLEANING_HANDLE_PREFIX,
    build_fragrantica_cleaning_packet,
)
from source_capture.fragrantica_projection import (
    FRAGRANTICA_PROJECTION_CERTIFICATION,
    build_fragrantica_projection,
)
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


def test_fragrantica_projection_rows_become_raw_keyed_cleaning_handles() -> None:
    packet = _packet()
    projection = build_fragrantica_projection(
        packet=packet,
        raw_file_bytes_by_file_id={
            "file_01": _html().encode("utf-8"),
            "file_02": b'{"status": 200}',
        },
    )

    handles = cleaning_input_handles_from_projection_rows(
        source_family=packet.source_family,
        source_surface=packet.source_surface,
        projection_packet=projection,
    )

    CleaningPacket(handles=handles)
    review_row = next(row for row in projection.rows if row.row_kind == "fragrance_review_card_current_window")
    review_handle = next(
        handle for handle in handles if handle.projection_ref and handle.projection_ref.row_id == review_row.row_id
    )
    assert review_handle.raw_anchor.packet_id == packet.packet_id
    assert review_handle.raw_anchor.anchor_kind == "html_selector"
    assert review_handle.raw_anchor.anchor_value == "#parent3090334"
    assert review_handle.projection_ref is not None
    assert review_handle.projection_ref.certification == FRAGRANTICA_PROJECTION_CERTIFICATION
    assert review_handle.projection_ref.row_kind == "fragrance_review_card_current_window"


def test_fragrantica_cleaning_packet_adds_review_card_transform_ledger() -> None:
    packet = _packet()
    projection = build_fragrantica_projection(
        packet=packet,
        raw_file_bytes_by_file_id={
            "file_01": _html().encode("utf-8"),
            "file_02": b'{"status": 200}',
        },
    )

    cleaning_packet = build_fragrantica_cleaning_packet(projection)

    assert len(cleaning_packet.handles) == len(projection.rows)
    assert all(handle.ecr_ref is not None for handle in cleaning_packet.handles)
    assert {
        handle.ecr_ref.status
        for handle in cleaning_packet.handles
        if handle.ecr_ref is not None
    } == {"by_convention_not_existence_checked"}
    review_row = next(row for row in projection.rows if row.row_kind == "fragrance_review_card_current_window")
    expected_handle_id = f"{FRAGRANTICA_CLEANING_HANDLE_PREFIX}:{review_row.row_id}"
    review_entries = [
        entry
        for entry in cleaning_packet.transform_ledger
        if entry.input_handle_id == expected_handle_id
    ]
    methods = {entry.transform.method_or_rule for entry in review_entries}
    assert methods == {
        "fragrantica_author_display_name_whitespace_normalization",
        "fragrantica_review_text_length_bin",
        "fragrantica_review_text_whitespace_normalization",
        "fragrantica_source_visible_vote_field_carry",
    }

    text_entry = _entry_by_method(
        review_entries, "fragrantica_review_text_whitespace_normalization"
    )
    assert text_entry.transform.original_value == "This perfume died young."
    assert text_entry.transform.transformed_value == "This perfume died young."

    length_entry = _entry_by_method(review_entries, "fragrantica_review_text_length_bin")
    assert length_entry.transform.original_value == "24"
    assert length_entry.transform.transformed_value == "chars_0000_0199"

    vote_entry = _entry_by_method(review_entries, "fragrantica_source_visible_vote_field_carry")
    carried_votes = json.loads(vote_entry.transform.transformed_value)
    assert carried_votes["rating"] == 5
    assert carried_votes["longevity"] == 3
    assert carried_votes["sillage"] == 2
    assert carried_votes["gender"] == "female_unisex"
    assert carried_votes["relation"] == "have"


def test_fragrantica_cleaning_packet_carries_projection_residuals_without_judgment_claims() -> None:
    packet = _packet()
    projection = build_fragrantica_projection(
        packet=packet,
        raw_file_bytes_by_file_id={
            "file_01": _html().encode("utf-8"),
            "file_02": b'{"status": 200}',
        },
    )

    cleaning_packet = build_fragrantica_cleaning_packet(projection)

    review_handle = next(
        handle
        for handle in cleaning_packet.handles
        if handle.projection_ref
        and handle.projection_ref.row_kind == "fragrance_review_card_current_window"
    )
    assert "linked_media_assets_not_preserved_by_direct_http_packet" in review_handle.residuals
    assert "review_attached_photo_proof_not_present" in review_handle.residuals
    assert "inspect_raw_before_media_dependent_claim" in review_handle.raw_pull_triggers
    assert "inspect_raw_before_review_photo_dependent_claim" in review_handle.raw_pull_triggers
    assert review_handle.ecr_ref is not None
    assert review_handle.ecr_ref.ref_id == f"ecr:{packet.packet_id}:source_side_postures"


def test_fragrantica_cleaning_packet_leaves_non_review_rows_untransformed() -> None:
    packet = _packet()
    projection = build_fragrantica_projection(
        packet=packet,
        raw_file_bytes_by_file_id={
            "file_01": _html().encode("utf-8"),
            "file_02": b'{"status": 200}',
        },
    )

    cleaning_packet = build_fragrantica_cleaning_packet(projection)
    review_row_ids = {
        row.row_id
        for row in projection.rows
        if row.row_kind == "fragrance_review_card_current_window"
    }
    transformed_row_ids = {
        entry.input_handle_id.removeprefix(f"{FRAGRANTICA_CLEANING_HANDLE_PREFIX}:")
        for entry in cleaning_packet.transform_ledger
    }

    assert transformed_row_ids == review_row_ids


def test_fragrantica_cleaning_normalization_preserves_pre_transform_string_values() -> None:
    projection = _projection_with_review_field_overrides(
        review_text="  This   perfume\n died young.  ",
        author_display_name="  Ri   mazy  ",
    )

    cleaning_packet = build_fragrantica_cleaning_packet(projection)
    review_row = next(row for row in projection.rows if row.row_kind == "fragrance_review_card_current_window")
    expected_handle_id = f"{FRAGRANTICA_CLEANING_HANDLE_PREFIX}:{review_row.row_id}"
    review_entries = [
        entry
        for entry in cleaning_packet.transform_ledger
        if entry.input_handle_id == expected_handle_id
    ]

    text_entry = _entry_by_method(
        review_entries, "fragrantica_review_text_whitespace_normalization"
    )
    assert text_entry.transform.original_value == "  This   perfume\n died young.  "
    assert text_entry.transform.transformed_value == "This perfume died young."

    author_entry = _entry_by_method(
        review_entries, "fragrantica_author_display_name_whitespace_normalization"
    )
    assert author_entry.transform.original_value == "  Ri   mazy  "
    assert author_entry.transform.transformed_value == "Ri mazy"


def test_fragrantica_cleaning_packet_can_omit_ecr_ref_when_not_present() -> None:
    packet = _packet()
    projection = build_fragrantica_projection(
        packet=packet,
        raw_file_bytes_by_file_id={
            "file_01": _html().encode("utf-8"),
            "file_02": b'{"status": 200}',
        },
    )

    cleaning_packet = build_fragrantica_cleaning_packet(projection, attach_ecr_ref=False)

    assert all(handle.ecr_ref is None for handle in cleaning_packet.handles)


def _projection_with_review_field_overrides(**overrides):
    packet = _packet()
    projection = build_fragrantica_projection(
        packet=packet,
        raw_file_bytes_by_file_id={
            "file_01": _html().encode("utf-8"),
            "file_02": b'{"status": 200}',
        },
    )
    rows = []
    for row in projection.rows:
        if row.row_kind == "fragrance_review_card_current_window":
            fields = {**row.source_visible_fields, **overrides}
            row = row.model_copy(update={"source_visible_fields": fields})
        rows.append(row)
    return projection.model_copy(update={"rows": rows})


def _packet() -> SourceCapturePacket:
    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason("fixture does not supply source event timing"),
        source_edit_or_version=unknown_with_reason("fixture does not supply edit timing"),
        capture_time=known_fact("2026-06-28T18:57:58Z"),
        recapture_time=not_applicable("first capture"),
        cutoff_posture=unknown_with_reason("test fixture has no decision cutoff"),
    )
    return SourceCapturePacket(
        packet_id="01TESTFRAGRANTICACLEANING",
        manifest_version="source_capture_packet_manifest_v1",
        obligation_contract_version="core_spine_v0_data_capture_spine_obligation_contract_v0",
        source_family="fragrance_native_database",
        source_surface="fragrantica_product_page_direct_http",
        source_locator=known_fact(
            "https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html"
        ),
        requested_decision_context=known_fact("test projection to cleaning traceability"),
        capture_context=known_fact("unit test packet"),
        actor_audience_context=unknown_with_reason("not supplied by fixture"),
        capture_mode=CaptureModeCategory.STRUCTURED_ACCESS,
        operator_category="unit_test",
        session_identity="",
        timing=timing,
        access_posture=known_fact("direct HTTP fixture supplied"),
        archive_history_posture=not_attempted("archive not queried"),
        media_modality_posture=not_attempted("linked media not fetched"),
        re_capture_relationship=not_applicable("first capture"),
        source_slices=[
            SourceCaptureSlice(
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
        ],
        preserved_files=[
            PreservedFile(
                file_id="file_01",
                original_path="http_response_body.bin",
                relative_packet_path="raw/01_http_response_body.bin",
                sha256="htmlsha",
                hash_basis="raw_stored_bytes",
                size_bytes=123,
            ),
            PreservedFile(
                file_id="file_02",
                original_path="http_response_metadata.json",
                relative_packet_path="raw/02_http_response_metadata.json",
                sha256="metasha",
                hash_basis="raw_stored_bytes",
                size_bytes=123,
            ),
        ],
        receipt_metadata=ReceiptMetadata(
            title="Source Capture Packet Receipt",
            generated_at="2026-06-28T18:57:59Z",
            summary="unit test packet",
            non_claims=["not Cleaning", "not Judgment"],
        ),
    )


def _html() -> str:
    return """
    <html><head>
      <link rel="canonical" href="https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html"/>
    </head><body>
      <div id="perfume-description-content" itemprop="description">
        <p><b>Baccarat Rouge 540</b> by <b>Maison Francis Kurkdjian</b> is a fragrance. Baccarat Rouge 540 was launched in 2015.</p>
      </div>
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
      </div>
    </body></html>
    """



def _entry_by_method(entries, method: str):
    return next(entry for entry in entries if entry.transform.method_or_rule == method)
