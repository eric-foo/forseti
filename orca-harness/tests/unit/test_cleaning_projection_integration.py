from __future__ import annotations

import json

from cleaning import (
    CleaningPacket,
    cleaning_input_handles_from_projection_rows,
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
from source_capture.reddit_projection import (
    REDDIT_PROJECTION_CERTIFICATION,
    build_reddit_api_projection,
)
from source_capture.retail_pdp_projection import (
    RETAIL_PDP_PROJECTION_CERTIFICATION,
    build_retail_pdp_projection,
)


def test_reddit_projection_rows_become_raw_keyed_cleaning_handles() -> None:
    packet = _reddit_packet()
    projection = build_reddit_api_projection(
        packet=packet,
        raw_file_bytes_by_file_id={"file_01": _reddit_comments_bytes()},
    )

    handles = cleaning_input_handles_from_projection_rows(
        source_family=packet.source_family,
        source_surface=packet.source_surface,
        projection_packet=projection,
    )

    assert len(handles) == len(projection.rows) == 4
    CleaningPacket(handles=handles)

    first_row = projection.rows[0]
    first_handle = handles[0]
    assert first_handle.raw_anchor.packet_id == packet.packet_id
    assert first_handle.raw_anchor.slice_id == first_row.raw_ref.slice_id
    assert first_handle.raw_anchor.file_id == first_row.raw_anchor.file_id
    assert first_handle.raw_anchor.anchor_kind == "json_pointer"
    assert first_handle.raw_anchor.json_pointer == first_row.raw_anchor.json_pointer
    assert first_handle.projection_ref is not None
    assert first_handle.projection_ref.certification == REDDIT_PROJECTION_CERTIFICATION
    assert first_handle.projection_ref.row_id == first_row.row_id
    assert first_handle.projection_ref.row_kind == first_row.row_kind


def test_retail_projection_rows_keep_source_anchor_kind_in_cleaning_handles() -> None:
    packet = _retail_packet()
    projection = build_retail_pdp_projection(
        packet=packet,
        raw_file_bytes_by_file_id={
            "file_01": _retail_html().encode("utf-8"),
            "file_02": _retail_visible_text().encode("utf-8"),
        },
    )

    handles = cleaning_input_handles_from_projection_rows(
        source_family=packet.source_family,
        source_surface=packet.source_surface,
        projection_packet=projection,
    )

    assert len(handles) == len(projection.rows)
    CleaningPacket(handles=handles)

    review_row = _single_projection_row(projection.rows, "retail_review_substrate")
    review_handle = next(
        handle for handle in handles if handle.projection_ref and handle.projection_ref.row_id == review_row.row_id
    )
    assert review_handle.raw_anchor.packet_id == packet.packet_id
    assert review_handle.raw_anchor.anchor_kind == "html_selector"
    assert review_handle.raw_anchor.anchor_value == "#averageCustomerReviews/#acrCustomerReviewText"
    assert review_handle.projection_ref is not None
    assert review_handle.projection_ref.certification == RETAIL_PDP_PROJECTION_CERTIFICATION
    assert review_handle.projection_ref.row_kind == "retail_review_substrate"


def _timing() -> PacketTiming:
    return PacketTiming(
        source_publication_or_event=unknown_with_reason("fixture does not supply source event timing"),
        source_edit_or_version=unknown_with_reason("fixture does not supply edit timing"),
        capture_time=known_fact("2026-06-16T00:00:00Z"),
        recapture_time=not_applicable("first capture"),
        cutoff_posture=unknown_with_reason("test fixture has no decision cutoff"),
    )


def _reddit_packet() -> SourceCapturePacket:
    timing = _timing()
    return SourceCapturePacket(
        packet_id="01TESTREDDITCLEANING",
        manifest_version="source_capture_packet_manifest_v1",
        obligation_contract_version="core_spine_v0_data_capture_spine_obligation_contract_v0",
        source_family="reddit",
        source_surface="reddit_api_comments",
        source_locator=known_fact("https://www.reddit.com/comments/abc123"),
        requested_decision_context=known_fact("test projection to cleaning traceability"),
        capture_context=known_fact("unit test packet"),
        actor_audience_context=unknown_with_reason("not supplied by fixture"),
        capture_mode=CaptureModeCategory.STRUCTURED_ACCESS,
        operator_category="unit_test",
        session_identity="01TESTSESSION",
        timing=timing,
        access_posture=known_fact("reddit api fixture supplied"),
        archive_history_posture=not_attempted("archive not queried"),
        media_modality_posture=not_attempted("media not fetched"),
        re_capture_relationship=not_applicable("first capture"),
        source_slices=[
            SourceCaptureSlice(
                slice_id="reddit_post_01",
                locator=known_fact("https://www.reddit.com/comments/abc123"),
                timing=timing,
                access_posture=known_fact("reddit api fixture supplied"),
                archive_history_posture=not_attempted("archive not queried"),
                media_modality_posture=not_attempted("media not fetched"),
                re_capture_relationship=not_applicable("first capture"),
                limitations=[],
                warning_notes=[],
                preserved_file_ids=["file_01"],
            )
        ],
        preserved_files=[
            PreservedFile(
                file_id="file_01",
                original_path="reddit_comments.json",
                relative_packet_path="raw/01_reddit_comments.json",
                sha256="abc123sha",
                hash_basis="raw_stored_bytes",
                size_bytes=123,
            )
        ],
        receipt_metadata=ReceiptMetadata(
            title="Source Capture Packet Receipt",
            generated_at="2026-06-16T00:00:00Z",
            summary="unit test packet",
            non_claims=["not Cleaning", "not Judgment"],
        ),
    )


def _retail_packet() -> SourceCapturePacket:
    timing = _timing()
    return SourceCapturePacket(
        packet_id="01TESTRETAILCLEANING",
        manifest_version="source_capture_packet_manifest_v1",
        obligation_contract_version="core_spine_v0_data_capture_spine_obligation_contract_v0",
        source_family="web_page",
        source_surface="cloakbrowser_snapshot",
        source_locator=known_fact("https://www.amazon.com/Laneige-Sleeping-Berry/dp/B07XXPHQZK"),
        requested_decision_context=known_fact("test projection to cleaning traceability"),
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
        series_id="amazon_laneige_lipmask_berry_us_v0",
        intended_cadence={"mode": "fixed", "slot_count": 3},
        source_slices=[
            SourceCaptureSlice(
                slice_id="cloakbrowser_snapshot_01",
                locator=known_fact("https://www.amazon.com/Laneige-Sleeping-Berry/dp/B07XXPHQZK"),
                timing=timing,
                access_posture=known_fact("rendered DOM fixture supplied"),
                archive_history_posture=not_attempted("archive not queried"),
                media_modality_posture=not_attempted("screenshot not supplied"),
                re_capture_relationship=not_applicable("first capture"),
                locale_pin=known_fact("en-US"),
                currency_pin=known_fact("USD"),
                variant_pin=known_fact("Berry 2.5g (B07XXPHQZK)"),
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


def _reddit_comments_bytes() -> bytes:
    post_listing = {
        "kind": "Listing",
        "data": {
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "id": "abc123",
                        "name": "t3_abc123",
                        "title": "API pricing changed",
                        "selftext": "Original post body",
                        "author": "poster",
                        "created_utc": 1700000000.0,
                        "subreddit": "testsub",
                        "permalink": "/r/testsub/comments/abc123/api_pricing_changed/",
                        "score": 12,
                        "num_comments": 2,
                    },
                }
            ]
        },
    }
    comments_listing = {
        "kind": "Listing",
        "data": {
            "children": [
                {
                    "kind": "t1",
                    "data": {
                        "id": "c1",
                        "name": "t1_c1",
                        "parent_id": "t3_abc123",
                        "link_id": "t3_abc123",
                        "body": "first comment",
                        "author": "commenter",
                        "created_utc": 1700000001.0,
                        "score": 3,
                        "replies": {
                            "kind": "Listing",
                            "data": {
                                "children": [
                                    {
                                        "kind": "t1",
                                        "data": {
                                            "id": "c2",
                                            "name": "t1_c2",
                                            "parent_id": "t1_c1",
                                            "link_id": "t3_abc123",
                                            "body": "nested reply",
                                            "author": "replier",
                                            "created_utc": 1700000002.0,
                                            "score": 1,
                                        },
                                    }
                                ]
                            },
                        },
                    },
                },
                {"kind": "more", "data": {"id": "more1", "count": 5, "children": ["c3", "c4"]}},
            ]
        },
    }
    return json.dumps([post_listing, comments_listing]).encode("utf-8")


def _retail_html() -> str:
    return """
    <html><body>
      <input type="hidden" id="ASIN" name="ASIN" value="B07XXPHQZK">
      <input type="hidden" name="items[0.base][customerVisiblePrice][amount]" value="16.8">
      <div id="averageCustomerReviews"><span>4.6 out of 5 stars</span></div>
      <span id="acrCustomerReviewText">36,799 global ratings</span>
      <div id="imageBlock_feature_div">hero image chrome</div>
    </body></html>
    """


def _retail_visible_text() -> str:
    return """
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


def _single_projection_row(rows, row_kind: str):
    matching_rows = [row for row in rows if row.row_kind == row_kind]
    assert len(matching_rows) == 1
    return matching_rows[0]
