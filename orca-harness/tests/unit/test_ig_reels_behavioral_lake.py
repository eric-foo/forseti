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
from source_capture.transcript.ig_reels_audio_packet import write_ig_reels_asr_transcript

_SHORTCODE = "DaA8n7EhqTR"
_CUES = [{"start_ms": 0, "end_ms": 90, "text": "hello from a real lake record"}]


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
