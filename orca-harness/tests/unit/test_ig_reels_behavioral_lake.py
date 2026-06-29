from __future__ import annotations

import json
from pathlib import Path

from cleaning.transcript_product_lake import PRODUCT_MENTIONS_LANE, PRODUCT_MENTIONS_SET_LANE
from data_lake.root import DataLakeRoot
from schemas.audience_comment_models import AudienceComment
from source_capture.ig_reels_behavioral_lake import (
    IG_REELS_BEHAVIORAL_LAKE_ADAPTER_METHOD,
    project_ig_reels_behavioral_index_from_lake,
    project_ig_reels_behavioral_item_from_lake,
)
from source_capture.ig_reels_deep_capture import ReelDeepCaptureResult
from source_capture.ig_reels_deep_capture_lake import (
    deep_capture_record_id,
    write_reel_deep_capture_into_lake,
)
from source_capture.models import (
    CaptureModeCategory,
    CoverageWindow,
    MetricObservation,
    MetricPosture,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.packet_assembly import staged_file_id_map, stage_and_write_packet
from source_capture.transcript.ig_reels_audio_packet import write_ig_reels_asr_transcript

_SHORTCODE = "DaA8n7EhqTR"
_HANDLE = "creatorhandle"
_CAPTURE_TIME = "2026-06-29T00:03:00Z"
_CUES = [{"start_ms": 0, "end_ms": 90, "text": "hello from a real lake record"}]
_CORRUPT_PRODUCT_RECORD_ID = "mentions_bad__0000000000000000.json"


def test_lake_adapter_injects_durable_record_ids_from_real_lake_paths(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    audio_packet_id, asr_record_id = _write_audio_transcript(root)
    deep_record_id = _write_deep_capture(root)
    _write_product_mentions(root, raw_anchor=audio_packet_id)

    projection = project_ig_reels_behavioral_item_from_lake(
        data_root=root,
        platform_item_id=_SHORTCODE,
    )

    assert projection["lake_adapter"]["adapter_method"] == IG_REELS_BEHAVIORAL_LAKE_ADAPTER_METHOD
    assert projection["persistence_correlation"]["audio_packet_ids"] == [audio_packet_id]
    assert projection["persistence_correlation"]["deep_capture_record_ids"] == [deep_record_id]
    assert projection["persistence_correlation"]["comment_record_ids"] == [deep_record_id]
    assert projection["persistence_correlation"]["extraction_record_paths"]

    sources_by_route = {
        source["source_route"]: source
        for source in projection["transcript"]["sources"]
    }
    assert sources_by_route["standalone_audio_packet"]["asr_record_id"] == asr_record_id
    assert sources_by_route["standalone_audio_packet"]["transcript_source_key"] == (
        f"{audio_packet_id}:asr:{asr_record_id}"
    )
    assert sources_by_route["deep_capture_render_audio"]["asr_record_id"] == deep_record_id
    assert projection["comments"]["sources"][0]["record_id"] == deep_record_id

    residuals = projection["behavioral_completeness"]["residuals"]
    assert "unknown_record" not in json.dumps(projection, sort_keys=True)
    assert not any("record_id_absent" in residual for residual in residuals)
    assert projection["behavioral_completeness"]["status"] == "complete_with_residuals"
    assert projection["behavioral_completeness"]["complete"] is False


def test_lake_adapter_projects_requested_missing_item_without_hidden_success(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")

    index = project_ig_reels_behavioral_index_from_lake(
        data_root=root,
        platform_item_ids=[_SHORTCODE],
    )

    projection = index[_SHORTCODE]
    assert projection["behavioral_completeness"]["status"] == "no_extraction_eligible_sources"
    assert projection["behavioral_completeness"]["complete"] is False
    assert f"ig_grid_candidate_absent:{_SHORTCODE}" in projection["behavioral_completeness"]["residuals"]
    assert f"ig_transcript_source_absent:{_SHORTCODE}" in projection["behavioral_completeness"]["residuals"]


def test_lake_adapter_projects_real_grid_packet_rows(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    grid_packet_id = _write_grid_packet(root)

    projection = project_ig_reels_behavioral_item_from_lake(
        data_root=root,
        platform_item_id=_SHORTCODE,
    )

    assert projection["candidate"] is not None
    assert projection["candidate"]["ranking_basis"] == "views_then_engagement"
    assert projection["candidate"]["persistence_anchors"]["grid_packet_ids"] == [grid_packet_id]
    assert projection["persistence_correlation"]["grid_packet_ids"] == [grid_packet_id]
    residuals = projection["behavioral_completeness"]["residuals"]
    assert f"ig_grid_candidate_absent:{_SHORTCODE}" not in residuals


def test_lake_adapter_surfaces_unreadable_raw_packet_for_requested_item(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    audio_packet_id, _asr_record_id = _write_audio_transcript(root)
    packet_dir = root.find_packet(audio_packet_id)
    assert packet_dir is not None
    (packet_dir / "manifest.json").write_text("{not-json", encoding="utf-8")

    projection = project_ig_reels_behavioral_item_from_lake(
        data_root=root,
        platform_item_id=_SHORTCODE,
    )

    assert (
        f"ig_lake_raw_packet_discovery_failed:{audio_packet_id}"
        in projection["behavioral_completeness"]["residuals"]
    )
    assert projection["behavioral_completeness"]["complete"] is False


def test_lake_adapter_surfaces_grid_projection_failure_for_requested_item(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    grid_packet_id = _write_grid_packet(root, body=b"{not-json")

    projection = project_ig_reels_behavioral_item_from_lake(
        data_root=root,
        platform_item_id=_SHORTCODE,
    )

    residuals = projection["behavioral_completeness"]["residuals"]
    assert f"ig_lake_grid_projection_failed:{grid_packet_id}" in residuals
    assert f"ig_grid_candidate_absent:{_SHORTCODE}" in residuals
    assert projection["behavioral_completeness"]["complete"] is False


def test_lake_adapter_surfaces_unreadable_asr_record(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    audio_packet_id, asr_record_id = _write_audio_transcript(root)
    asr_path = root.record_path(
        subtree="derived",
        raw_anchor=audio_packet_id,
        lane="transcript_asr",
        record_id=asr_record_id,
    )
    asr_path.write_text("{not-json", encoding="utf-8")

    projection = project_ig_reels_behavioral_item_from_lake(
        data_root=root,
        platform_item_id=_SHORTCODE,
    )

    assert (
        f"ig_lake_asr_record_unreadable:{audio_packet_id}:{asr_record_id}"
        in projection["behavioral_completeness"]["residuals"]
    )
    assert projection["behavioral_completeness"]["complete"] is False


def test_lake_adapter_surfaces_unreadable_product_record(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    audio_packet_id, _asr_record_id = _write_audio_transcript(root)
    _write_corrupt_product_mentions(root, raw_anchor=audio_packet_id)

    projection = project_ig_reels_behavioral_item_from_lake(
        data_root=root,
        platform_item_id=_SHORTCODE,
    )

    residual = (
        f"ig_lake_product_mentions_record_unreadable:{audio_packet_id}:"
        f"{_CORRUPT_PRODUCT_RECORD_ID}"
    )
    assert residual in projection["behavioral_completeness"]["residuals"]
    assert projection["behavioral_completeness"]["complete"] is False


def _write_grid_packet(root: DataLakeRoot, *, body: bytes | None = None) -> str:
    payload = body
    if payload is None:
        payload = (json.dumps(_grid_capture_payload(), sort_keys=True) + "\n").encode("utf-8")
    artifacts = [("ig_reels_grid_capture.json", payload)]
    file_ids = staged_file_id_map(artifacts)
    locator = known_fact(f"https://www.instagram.com/{_HANDLE}/reels/")
    timing = _packet_timing(unknown_with_reason("profile grid slice is the enumeration source"))
    access = known_fact("ig_logged_out_reels_grid_browser_capture")
    archive = not_attempted("IG reels-grid test fixture does not query archive services")
    media = known_fact("DOM media-anchor text and passive JSON preserved")
    recap = not_applicable("no prior source capture packet")
    result = stage_and_write_packet(
        data_root=root,
        staged_artifacts=artifacts,
        source_slices=[
            SourceCaptureSlice(
                slice_id="ig_reels_grid_01",
                locator=known_fact(f"https://www.instagram.com/{_HANDLE}/reel/{_SHORTCODE}/"),
                timing=timing,
                access_posture=access,
                archive_history_posture=archive,
                media_modality_posture=media,
                re_capture_relationship=recap,
                preserved_file_ids=[file_ids["ig_reels_grid_capture.json"]],
                metric_observations=[
                    _observed("view_count", 1200),
                    _observed("like_count", 99),
                    _observed("comment_count", 4),
                ],
            )
        ],
        source_family="instagram_creator",
        source_surface="ig_reels_grid_dom_passive_json",
        source_locator=locator,
        decision_question="Project persisted IG Reels grid behavior in the lake adapter test.",
        capture_context="logged-out IG public /reels/ grid capture test fixture",
        actor_audience_context=known_fact("public creator profile"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="ig_reels_grid_test_operator",
        session_identity=None,
        visible_mode_changes=[],
        source_publication_or_event=timing.source_publication_or_event,
        source_edit_or_version=timing.source_edit_or_version,
        cutoff_posture=timing.cutoff_posture,
        recapture_time=timing.recapture_time,
        access_posture=access,
        archive_history_posture=archive,
        media_modality_posture=media,
        re_capture_relationship=recap,
        warnings=[],
        limitations=[],
        receipt_summary="IG Reels grid packet test fixture.",
        receipt_non_claims=["test fixture"],
    )
    return result.packet.packet_id


def _grid_capture_payload() -> dict[str, object]:
    return {
        "capture_metadata": {
            "source_surface": "ig_reels_grid_dom_passive_json",
            "selection_policy_version": "ig_reels_grid_capture_selection_v0",
        },
        "creator_profile_snapshot": {
            "platform": "instagram",
            "source_profile": _HANDLE,
            "numeric_id": "42",
            "follower_count": 123456,
            "parse_status": "parsed_web_profile_info_json_metadata",
        },
        "joined_rows": [
            {
                "dom_row": _dom_row(0, _SHORTCODE, "reel", "1,200", "99", "4"),
                "source_surface_candidates": [
                    _json_candidate("clips_user_json_metadata", _SHORTCODE, 1200, 99, 4),
                ],
            }
        ],
    }


def _dom_row(
    index: int,
    shortcode: str,
    kind: str,
    views_text: str | None,
    likes_text: str | None,
    comments_text: str | None,
) -> dict[str, object]:
    leaf = [text for text in (views_text, likes_text, comments_text) if text is not None]
    permalink = f"https://www.instagram.com/{_HANDLE}/{kind}/{shortcode}/"
    return {
        "index": index,
        "path": f"/{_HANDLE}/{kind}/{shortcode}/",
        "permalink_url": permalink,
        "shortcode": shortcode,
        "kind": kind,
        "visible_text": views_text,
        "visible_numeric_texts": [views_text] if views_text else [],
        "hidden_leaf_numeric_texts": leaf,
        "hidden_engagement_candidates": [likes_text, comments_text],
        "views_text": views_text,
        "likes_text": likes_text,
        "comments_text": comments_text,
        "parse_status": "parsed_no_hover_grid_engagement",
        "rect": None,
    }


def _json_candidate(
    source_surface: str,
    shortcode: str,
    video_or_play_count: int,
    like_count: int,
    comment_count: int,
) -> dict[str, object]:
    return {
        "source_surface": source_surface,
        "shortcode": shortcode,
        "taken_at_timestamp": 1750000000,
        "taken_at_utc": "2026-06-15T00:00:00Z",
        "caption_text": "daily reel",
        "caption_length": 10,
        "product_type": "clips",
        "typename": "GraphVideo",
        "is_video": True,
        "video_or_play_count": video_or_play_count,
        "video_or_play_count_key": "ig_play_count",
        "video_or_play_count_candidates": [["ig_play_count", video_or_play_count]],
        "like_count": like_count,
        "comment_count": comment_count,
        "is_paid_partnership": None,
        "is_affiliate": None,
        "sponsor_users": [],
        "ad_term_candidates": [],
        "pinned_on_clips_tab": False,
        "pinned_on_timeline": None,
        "raw_node_keys_sample": ["shortcode", "video_view_count"],
    }


def _observed(metric: str, value: int) -> MetricObservation:
    return MetricObservation(
        metric=metric,
        posture=MetricPosture.OBSERVED,
        value=value,
        coverage_window=CoverageWindow(end=_CAPTURE_TIME),
    )


def _packet_timing(publication) -> PacketTiming:  # noqa: ANN001
    return PacketTiming(
        source_publication_or_event=publication,
        source_edit_or_version=unknown_with_reason("not inferred"),
        capture_time=known_fact(_CAPTURE_TIME),
        recapture_time=not_applicable("no prior capture"),
        cutoff_posture=unknown_with_reason("not supplied"),
    )


def _write_audio_transcript(root: DataLakeRoot) -> tuple[str, str]:
    code, msg = write_ig_reels_asr_transcript(
        shortcode=_SHORTCODE,
        audio_bytes=b"fake audio bytes",
        audio_ext="m4a",
        transcribe_fn=lambda _path: (
            "transcribed",
            list(_CUES),
            {"tool": "faster-whisper", "model": "small"},
        ),
        data_root=root,
        now_iso="2026-06-29T00:02:00Z",
    )
    assert code == 0
    rel_path = Path(msg.split(" ")[0])
    return rel_path.parts[-3], rel_path.name


def _write_deep_capture(root: DataLakeRoot) -> str:
    result = ReelDeepCaptureResult(
        reel_shortcode=_SHORTCODE,
        comments=(
            AudienceComment(
                comment_id="c1",
                reel_shortcode=_SHORTCODE,
                author_username="zoe",
                text="works",
                like_count=1,
                created_at_unix=1782400000,
            ),
        ),
        transcript_posture="transcribed",
        transcript_cues=tuple(_CUES),
        media_url_used="https://x.fbcdn.net/o1/v/clip.mp4",
    )
    write_reel_deep_capture_into_lake(
        data_root=root,
        result=result,
        generated_at="2026-06-29T00:01:00Z",
    )
    return deep_capture_record_id(result)


def _write_corrupt_product_mentions(root: DataLakeRoot, *, raw_anchor: str) -> None:
    root.append_record_set(
        subtree="derived",
        raw_anchor=raw_anchor,
        record_id=_CORRUPT_PRODUCT_RECORD_ID,
        members={PRODUCT_MENTIONS_LANE: b"{not-json"},
        completion_lane=PRODUCT_MENTIONS_SET_LANE,
    )


def _write_product_mentions(root: DataLakeRoot, *, raw_anchor: str) -> None:
    payload = {
        "video_id": _SHORTCODE,
        "transcript_anchor": raw_anchor,
        "transcript_source": "asr",
        "model": "test",
        "rubric_version": "test",
        "mention_count": 0,
        "rejected_count": 0,
        "mentions": [],
        "rejected": [],
    }
    root.append_record_set(
        subtree="derived",
        raw_anchor=raw_anchor,
        record_id="mentions_test__0000000000000000.json",
        members={
            PRODUCT_MENTIONS_LANE: (
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
            ).encode("utf-8")
        },
        completion_lane=PRODUCT_MENTIONS_SET_LANE,
    )
