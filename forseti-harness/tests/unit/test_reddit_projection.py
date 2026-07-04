from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

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
    ProjectionRawAnchor,
    ProjectionRawRef,
    RedditProjectionRow,
    build_reddit_api_projection,
)


def _timing() -> PacketTiming:
    return PacketTiming(
        source_publication_or_event=unknown_with_reason(
            "reddit API test fixture does not supply source event timing"
        ),
        source_edit_or_version=unknown_with_reason("reddit API test fixture does not supply edit timing"),
        capture_time=known_fact("2026-06-16T00:00:00Z"),
        recapture_time=not_applicable("first capture"),
        cutoff_posture=unknown_with_reason("test fixture has no decision cutoff"),
    )


def _packet() -> SourceCapturePacket:
    timing = _timing()
    return SourceCapturePacket(
        packet_id="01TESTREDDITPROJECTION",
        manifest_version="source_capture_packet_manifest_v1",
        obligation_contract_version="core_spine_v0_data_capture_spine_obligation_contract_v0",
        source_family="reddit",
        source_surface="reddit_api_comments",
        source_locator=known_fact("https://www.reddit.com/comments/abc123"),
        requested_decision_context=known_fact("test projection traceability"),
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


def test_reddit_projection_rows_are_raw_anchored_and_view_only() -> None:
    packet = _packet()

    projection = build_reddit_api_projection(
        packet=packet,
        raw_file_bytes_by_file_id={"file_01": _reddit_comments_bytes()},
    )

    assert projection.packet_id == packet.packet_id
    assert projection.certification == REDDIT_PROJECTION_CERTIFICATION
    assert projection.loss_ledger.certification == "removes_source_envelope_only; does_not_certify_cleaning"
    assert projection.loss_ledger.removed[0].category == "REDDIT_LISTING_ENVELOPE"
    assert projection.loss_ledger.removed[0].raw_anchor.sha256 == "abc123sha"
    assert [entry.raw_anchor.json_pointer for entry in projection.loss_ledger.removed] == ["/0", "/1"]

    assert [row.row_kind for row in projection.rows] == [
        "reddit_submission",
        "reddit_comment",
        "reddit_comment",
        "reddit_more_stub",
    ]
    assert [row.raw_anchor.json_pointer for row in projection.rows] == [
        "/0/data/children/0",
        "/1/data/children/0",
        "/1/data/children/0/data/replies/data/children/0",
        "/1/data/children/1",
    ]
    for row in projection.rows:
        assert row.raw_ref.packet_id == "01TESTREDDITPROJECTION"
        assert row.raw_ref.slice_id == "reddit_post_01"
        assert row.raw_anchor.file_id == "file_01"
        assert row.raw_anchor.relative_packet_path == "raw/01_reddit_comments.json"
        assert row.raw_anchor.sha256 == "abc123sha"
        assert row.raw_anchor.hash_basis == "raw_stored_bytes"

    first_comment = projection.rows[1]
    nested_reply = projection.rows[2]
    more_stub = projection.rows[3]
    assert first_comment.parent_row_id == "reddit_post_01:t3:abc123"
    assert nested_reply.parent_row_id == "reddit_post_01:t1:c1"
    assert more_stub.parent_row_id == "reddit_post_01:t3:abc123"
    assert len(projection.binding_map) == 3
    assert projection.loss_ledger.preserved_evidence_rows == len(projection.rows)
    assert projection.loss_ledger.preserved_bindings == len(projection.binding_map)
    assert nested_reply.source_visible_fields["score"] == 1
    assert "more_stub_not_expanded" in more_stub.residuals


def test_reddit_projection_requires_raw_bytes_for_each_preserved_file() -> None:
    with pytest.raises(ValueError, match="raw bytes are required"):
        build_reddit_api_projection(packet=_packet(), raw_file_bytes_by_file_id={})


def test_reddit_projection_residualizes_malformed_json_without_inventing_rows() -> None:
    projection = build_reddit_api_projection(
        packet=_packet(),
        raw_file_bytes_by_file_id={"file_01": b"not-json"},
    )

    assert projection.rows == []
    assert projection.loss_ledger.preserved_evidence_rows == 0
    assert projection.loss_ledger.structure_preserved is False
    assert projection.residuals == ["reddit_post_01:file_01:malformed_reddit_json"]


def test_reddit_projection_rejects_judgment_smuggling_field_names() -> None:
    raw_ref = ProjectionRawRef(packet_id="p1", slice_id="s1")
    raw_anchor = ProjectionRawAnchor(
        file_id="file_01",
        relative_packet_path="raw/body.json",
        sha256="sha",
        hash_basis="raw_stored_bytes",
    )

    with pytest.raises(ValidationError, match="forbidden Judgment field"):
        RedditProjectionRow(
            row_id="s1:t1:c1",
            row_kind="reddit_comment",
            raw_ref=raw_ref,
            raw_anchor=raw_anchor,
            source_visible_fields={"credibility_label": "high"},
        )
