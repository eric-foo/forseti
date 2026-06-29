from __future__ import annotations

import pytest

from source_capture.ig_reels_behavioral_projection import (
    IG_REELS_BEHAVIORAL_PROJECTION_METHOD,
    project_ig_reels_behavioral_item,
)


_SHORTCODE = "DaA8n7EhqTR"


def _grid_row(**overrides):
    row = {
        "row_id": "grid-packet-1:ig_reels_grid_00:view_count",
        "raw_ref": {"packet_id": "grid-packet-1", "slice_id": "ig_reels_grid_00"},
        "content_shortcode": _SHORTCODE,
        "metric": "view_count",
        "posture": "observed",
        "value": 1200,
        "chosen_source_surface": "clips/user",
        "source_surface_count_candidates": [
            {"source_surface": "clips/user", "value": 1200},
            {"source_surface": "dom_grid_engagement", "value": 900, "raw_text": "900"},
        ],
        "join_status": "joined_by_shortcode",
        "selection_limitations": ["likes_hidden"],
        "capture_time": "2026-06-29T00:00:00Z",
        "source_visible_fields": {"media_product_type": "clips"},
        "residuals": [],
    }
    row.update(overrides)
    return row


def _comment_set(**overrides):
    row = {
        "reel_shortcode": _SHORTCODE,
        "record_id": "deepcap_1.json",
        "generated_at": "2026-06-29T00:01:00Z",
        "comment_count": 1,
        "comments": [{"comment_id": "c1", "author_username": "zoe", "text": "works"}],
        "media_provenance": {"audio_handle_used": True, "media_host": "x.fbcdn.net"},
    }
    row.update(overrides)
    return row


def _audio_transcript(**overrides):
    row = {
        "video_id": _SHORTCODE,
        "shortcode": _SHORTCODE,
        "record_id": "asr_small__abc123",
        "platform": "instagram",
        "posture": "transcribed",
        "cue_count": 1,
        "cues": [{"start_ms": 0, "end_ms": 90, "text": "hello"}],
        "provenance": {
            "source_packet_id": "audio-packet-1",
            "source_file_id": "audio-file-1",
            "source_sha256": "abc123",
        },
        "retrieval_time_utc": "2026-06-29T00:02:00Z",
    }
    row.update(overrides)
    return row


def _deep_transcript(**overrides):
    row = {
        "reel_shortcode": _SHORTCODE,
        "record_id": "deepcap_1.json",
        "generated_at": "2026-06-29T00:01:00Z",
        "transcript_posture": "ok",
        "cue_count": 1,
        "cues": [{"start_ms": 0, "end_ms": 90, "text": "hello"}],
        "media_provenance": {"audio_handle_used": True, "media_host": "x.fbcdn.net"},
    }
    row.update(overrides)
    return row


def _audio_source(anchor: str, record_id: str, **overrides):
    return _audio_transcript(
        record_id=record_id,
        provenance={"source_packet_id": anchor, "source_file_id": f"{anchor}-file"},
        **overrides,
    )


def test_projects_complete_audio_backed_ig_behavior_record() -> None:
    projection = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        grid_rows=[_grid_row()],
        comment_sets=[_comment_set()],
        standalone_audio_transcript_records=[_audio_transcript()],
        extraction_results=[
            {
                "anchor": "audio-packet-1",
                "video_id": _SHORTCODE,
                "status": "extracted",
                "path": "derived/audio-packet-1/product_mentions/r1",
            }
        ],
    )

    assert projection["projection_method"] == IG_REELS_BEHAVIORAL_PROJECTION_METHOD
    assert projection["platform_item_id"] == _SHORTCODE
    assert projection["candidate"]["ranking_basis"] == "views_then_engagement"
    assert projection["candidate"]["limitations"] == ["likes_hidden"]
    assert projection["comments"]["posture"] == "captured"
    assert projection["transcript"]["source_count"] == 1
    assert projection["transcript"]["sources"][0]["source_route"] == "standalone_audio_packet"
    assert projection["transcript"]["sources"][0]["extraction_status"] == "extracted"
    assert projection["transcript"]["canonical_source"]["source_route"] == "standalone_audio_packet"
    assert projection["behavioral_completeness"] == {
        "status": "complete",
        "complete": True,
        "residuals": [],
    }
    assert projection["persistence_correlation"]["grid_packet_ids"] == ["grid-packet-1"]
    assert projection["persistence_correlation"]["audio_packet_ids"] == ["audio-packet-1"]
    assert projection["persistence_correlation"]["extraction_record_paths"] == [
        "derived/audio-packet-1/product_mentions/r1"
    ]


def test_deep_capture_transcript_is_extraction_eligible_and_can_complete() -> None:
    projection = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        grid_rows=[_grid_row()],
        comment_sets=[_comment_set()],
        deep_capture_transcript_records=[_deep_transcript()],
        extraction_results=[
            {
                "anchor": _SHORTCODE,
                "video_id": _SHORTCODE,
                "status": "extracted",
                "path": f"derived/{_SHORTCODE}/product_mentions/r1",
            }
        ],
    )

    deep_source = [
        source
        for source in projection["transcript"]["sources"]
        if source["source_route"] == "deep_capture_render_audio"
    ][0]
    assert deep_source["posture"] == "transcribed"
    assert deep_source["extraction_eligible"] is True
    assert deep_source["non_eligible_reason"] is None
    assert deep_source["extraction_status"] == "extracted"
    assert projection["transcript"]["canonical_source"]["source_route"] == "deep_capture_render_audio"
    assert projection["behavioral_completeness"] == {
        "status": "complete",
        "complete": True,
        "residuals": [],
    }


def test_failed_extraction_stays_visible_and_blocks_complete_claim() -> None:
    projection = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        standalone_audio_transcript_records=[_audio_transcript()],
        extraction_results=[
            {
                "anchor": "audio-packet-1",
                "video_id": _SHORTCODE,
                "status": "failed",
                "error": "RuntimeError: bad extraction",
            }
        ],
    )

    assert projection["extraction"]["rollup"]["status"] == "failed"
    assert projection["behavioral_completeness"]["complete"] is False
    assert projection["extraction"]["source_statuses"][0]["extraction_error"] == "RuntimeError: bad extraction"
    assert (
        "ig_transcript_extraction_failed:audio-packet-1:asr:asr_small__abc123"
    ) in projection["behavioral_completeness"]["residuals"]
    assert f"ig_grid_candidate_absent:{_SHORTCODE}" in projection["behavioral_completeness"]["residuals"]
    assert f"ig_comments_not_attempted:{_SHORTCODE}" in projection["behavioral_completeness"]["residuals"]


def test_mismatched_transcript_source_is_residualized_and_ignored() -> None:
    projection = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        standalone_audio_transcript_records=[_audio_transcript(video_id="OtherShort")],
    )

    assert projection["transcript"]["source_count"] == 0
    assert projection["extraction"]["rollup"]["status"] == "no_extraction_eligible_sources"
    assert "ig_transcript_source_shortcode_mismatch:OtherShort" in projection["behavioral_completeness"]["residuals"]


def test_canonical_standalone_audio_prefers_latest_capture_time() -> None:
    projection = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        standalone_audio_transcript_records=[
            _audio_transcript(
                record_id="asr_old",
                retrieval_time_utc="2026-06-29T00:01:00Z",
                provenance={"source_packet_id": "audio-old"},
            ),
            _audio_transcript(
                record_id="asr_new",
                retrieval_time_utc="2026-06-29T00:03:00Z",
                provenance={"source_packet_id": "audio-new"},
            ),
        ],
        extraction_results=[
            {"anchor": "audio-old", "video_id": _SHORTCODE, "status": "extracted"},
            {"anchor": "audio-new", "video_id": _SHORTCODE, "status": "extracted"},
        ],
    )

    assert projection["transcript"]["canonical_source"]["transcript_anchor"] == "audio-new"
    assert projection["behavioral_completeness"]["status"] == "complete"


def test_real_shape_records_without_in_body_record_ids_are_residualized() -> None:
    audio = _audio_transcript()
    audio.pop("record_id")
    deep = _deep_transcript()
    deep.pop("record_id")
    comment = _comment_set()
    comment.pop("record_id")

    projection = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        comment_sets=[comment],
        standalone_audio_transcript_records=[audio],
        deep_capture_transcript_records=[deep],
        extraction_results=[{"anchor": "audio-packet-1", "video_id": _SHORTCODE, "status": "extracted"}],
    )

    residuals = projection["behavioral_completeness"]["residuals"]
    assert "ig_transcript_source_record_id_absent:standalone_audio_packet:audio-packet-1" in residuals
    assert f"ig_transcript_source_record_id_absent:deep_capture_render_audio:{_SHORTCODE}" in residuals
    assert f"ig_comment_record_id_absent:{_SHORTCODE}" in residuals
    standalone_source = [
        source
        for source in projection["transcript"]["sources"]
        if source["source_route"] == "standalone_audio_packet"
    ][0]
    assert standalone_source["transcript_source_key"] == "audio-packet-1:asr:unknown_record"
    assert projection["persistence_correlation"]["deep_capture_record_ids"] == []
    assert projection["persistence_correlation"]["comment_record_ids"] == []


def test_deep_capture_transcript_without_shortcode_is_residualized_and_ignored() -> None:
    deep = _deep_transcript()
    deep.pop("reel_shortcode")

    projection = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        deep_capture_transcript_records=[deep],
    )

    assert projection["transcript"]["source_count"] == 0
    assert (
        f"ig_transcript_source_shortcode_absent:deep_capture_render_audio:{_SHORTCODE}"
        in projection["behavioral_completeness"]["residuals"]
    )


def test_comment_posture_prefers_captured_when_successful_record_coexists_with_failed_render() -> None:
    projection = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        comment_sets=[_comment_set(comment_count=3)],
        deep_capture_transcript_records=[
            _deep_transcript(record_id="deepcap_failed.json", transcript_posture="render_unavailable"),
            _deep_transcript(record_id="deepcap_ok.json", transcript_posture="ok"),
        ],
    )

    assert projection["comments"]["posture"] == "captured"
    assert projection["comments"]["comment_count"] == 3


def test_comment_postures_cover_render_unavailable_and_empty() -> None:
    render_unavailable = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        deep_capture_transcript_records=[
            _deep_transcript(record_id="deepcap_render_unavailable.json", transcript_posture="render_unavailable")
        ],
    )
    empty = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        comment_sets=[_comment_set(record_id="deepcap_empty.json", comment_count=0, comments=[])],
    )

    assert render_unavailable["comments"]["posture"] == "render_unavailable"
    assert f"ig_comments_render_unavailable:{_SHORTCODE}" in render_unavailable["behavioral_completeness"]["residuals"]
    assert empty["comments"]["posture"] == "empty"


def test_extraction_rollup_covers_partial_failed_not_attempted_source_problem_and_ambiguous_anchor() -> None:
    partial = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        standalone_audio_transcript_records=[_audio_source("a1", "r1"), _audio_source("a2", "r2")],
        extraction_results=[{"anchor": "a1", "status": "extracted"}],
    )
    partial_failed = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        standalone_audio_transcript_records=[_audio_source("a1", "r1"), _audio_source("a2", "r2")],
        extraction_results=[{"anchor": "a1", "status": "extracted"}, {"anchor": "a2", "status": "failed"}],
    )
    not_attempted = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        standalone_audio_transcript_records=[_audio_source("a1", "r1")],
    )
    source_problem = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        standalone_audio_transcript_records=[_audio_source("a1", "r1")],
        deep_capture_transcript_records=[_deep_transcript(record_id="deep_failed", transcript_posture="failed")],
    )
    ambiguous = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        standalone_audio_transcript_records=[_audio_source("same-anchor", "r1"), _audio_source("same-anchor", "r2")],
        extraction_results=[{"anchor": "same-anchor", "status": "extracted"}],
    )

    assert partial["behavioral_completeness"]["status"] == "partial"
    assert partial_failed["behavioral_completeness"]["status"] == "partial_failed"
    assert not_attempted["behavioral_completeness"]["status"] == "not_attempted"
    assert source_problem["behavioral_completeness"]["status"] == "source_problem"
    assert ambiguous["behavioral_completeness"]["status"] == "failed"
    assert all(
        source["extraction_status"] == "ambiguous_anchor_result"
        for source in ambiguous["transcript"]["sources"]
    )


def test_ranking_basis_covers_engagement_and_unknown_or_weak() -> None:
    engagement = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        grid_rows=[_grid_row(metric="like_count")],
    )
    weak = project_ig_reels_behavioral_item(
        platform_item_id=_SHORTCODE,
        grid_rows=[_grid_row(metric="view_count", posture="estimated")],
    )

    assert engagement["candidate"]["ranking_basis"] == "engagement"
    assert weak["candidate"]["ranking_basis"] == "unknown_or_weak"


def test_requires_platform_item_id() -> None:
    with pytest.raises(ValueError, match="platform_item_id is required"):
        project_ig_reels_behavioral_item(platform_item_id=" ")
