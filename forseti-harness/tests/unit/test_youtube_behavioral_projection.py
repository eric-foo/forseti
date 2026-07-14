from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from data_lake.root import DataLakeRoot
from source_capture.youtube_watch_packet import (
    YoutubeWatchCommentPage,
    YoutubeWatchFetch,
    write_youtube_watch_packet,
)
from source_capture.transcript.asr_packet import write_asr_transcript
from source_capture.transcript.caption_packet import write_caption_packet
from source_capture.transcript.youtube_captions import CaptionFetch
from youtube_capture.behavioral_projection import (
    project_youtube_behavioral_item,
    project_youtube_behavioral_item_from_lake,
    transcript_sources_for_video,
)

_VIDEO_ID = "vid12345678"


def _json3_bytes() -> bytes:
    return json.dumps(
        {
            "events": [
                {"tStartMs": 1000, "dDurationMs": 1000, "segs": [{"utf8": "Dior Sauvage Elixir"}]},
                {"tStartMs": 2000, "dDurationMs": 1000, "segs": [{"utf8": "absolute beast"}]},
            ]
        }
    ).encode("utf-8")


def _metric_observed(value: int, path: str, artifact: str) -> dict[str, Any]:
    return {
        "posture": "observed",
        "value": value,
        "source_route": path.rsplit(".", 1)[0],
        "source_path": path,
        "artifact": artifact,
    }


def _metadata_packet(**overrides: Any) -> dict[str, Any]:
    packet = {
        "video_id": _VIDEO_ID,
        "surface_type": "watch",
        "watch_url": f"https://www.youtube.com/watch?v={_VIDEO_ID}",
        "channel": {"channel_id": "UC_fixture", "author": "Reviewer"},
        "metadata": {"title": "Fragrance review", "length_seconds": 42, "publish_date": "2026-06-20"},
        "engagement": {
            "view_count": 1200,
            "view_count_source_path": "player.microformat",
            "like_count": 34,
            "comment_sample_count": 1,
            "total_comment_count": 12,
        },
        "availability": {"video_state": "playable", "comments_state": "comments_sample_captured"},
        "metric_receipts": {
            "view_count": _metric_observed(1200, "ytInitialPlayerResponse.videoDetails.viewCount", "youtube_watch_capture.json"),
            "like_count": _metric_observed(
                34, "ytInitialPlayerResponse.microformat.playerMicroformatRenderer.likeCount", "youtube_watch_capture.json"
            ),
            "comment_sample_count": _metric_observed(
                1, "youtubei_next.commentEntityPayload", "youtube_watch_capture.json"
            ),
            "total_comment_count": _metric_observed(
                12, "youtubei_next.commentsHeaderRenderer.countText", "youtube_watch_capture.json"
            ),
        },
        "comments_posture": "comments_sample_captured",
        "comment_count_text": "12 comments",
        "comments": [
            {
                "comment_id": "comment-001",
                "author": "A",
                "text": "wear test?",
                "published_time": "1 day ago",
                "like_count": 2,
                "source_page_number": 1,
                "source_order_in_page": 1,
                "source_order_global": 1,
            }
        ],
        "comment_capture_coverage": {
            "requested_page_limit": 1,
            "pages_fetched": 1,
            "selected_comment_count": 1,
            "continuation_remaining_after_stop": False,
            "ordering_posture": "source_default_order_as_served",
        },
        "receipts": {"http_status": 200, "retrieval_time_utc": "2026-06-21T00:00:00Z"},
    }
    packet.update(overrides)
    return packet


def _commit_watch_metadata(
    data_root: DataLakeRoot,
    *,
    now_iso: str = "2026-06-21T00:00:00Z",
    title: str = "Fragrance review",
) -> str:
    packet = _metadata_packet()
    packet["metadata"] = {**packet["metadata"], "title": title}
    packet["receipts"] = {**packet["receipts"], "retrieval_time_utc": now_iso}
    code, output_dir = write_youtube_watch_packet(
        YoutubeWatchFetch(
            video_id=_VIDEO_ID,
            raw_watch_html=b"<html>ytInitialPlayerResponse</html>",
            packet=packet,
            comment_page_bodies=(
                YoutubeWatchCommentPage(filename="youtubei_next_page_01.json", raw_json_bytes=b"{}"),
            ),
        ),
        data_root=data_root,
        decision_question="capture YouTube watch metrics",
        now_iso=now_iso,
    )
    assert code == 0
    return Path(output_dir).name


def _rewrite_preserved_body(packet_dir: Path, suffix: str, body: bytes) -> None:
    manifest_path = packet_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for preserved in manifest["preserved_files"]:
        relative_path = preserved.get("relative_packet_path")
        if isinstance(relative_path, str) and relative_path.endswith(suffix):
            target = packet_dir.joinpath(*relative_path.split("/"))
            target.write_bytes(body)
            preserved["size_bytes"] = len(body)
            preserved["sha256"] = hashlib.sha256(body).hexdigest()
            manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            return
    raise AssertionError(f"preserved file ending with {suffix!r} not found")


def _watch_capture_manifest_entry(packet_dir: Path) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    manifest_path = packet_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for preserved in manifest["preserved_files"]:
        relative_path = preserved.get("relative_packet_path")
        if isinstance(relative_path, str) and relative_path.endswith("youtube_watch_capture.json"):
            return manifest_path, manifest, preserved
    raise AssertionError("youtube_watch_capture.json preserved file not found")


def _project_with_mutated_watch_capture(tmp_path, mutate):
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    watch_packet_id = _commit_watch_metadata(data_root)
    _commit_caption(data_root)
    watch_packet_dir = data_root.find_packet(watch_packet_id)
    assert watch_packet_dir is not None
    mutate(watch_packet_dir)
    sources = transcript_sources_for_video(data_root, _VIDEO_ID)

    projection = project_youtube_behavioral_item_from_lake(
        data_root=data_root,
        platform_video_id=_VIDEO_ID,
        extraction_results=_extracted_results_for_sources(sources),
    )
    return watch_packet_id, projection


def _assert_metadata_discovery_failure(projection: dict[str, Any], watch_packet_id: str, reason: str) -> None:
    residuals = projection["behavioral_completeness"]["residuals"]
    assert projection["metadata_capture"] is None
    assert f"youtube_metadata_packet_discovery_failed:{watch_packet_id}:{reason}" in residuals
    assert "youtube_metadata_packet_absent" in residuals
    assert projection["behavioral_completeness"]["complete"] is True


def _commit_caption(data_root: DataLakeRoot, *, video_id: str = _VIDEO_ID) -> str:
    cap = CaptionFetch(
        video_id=video_id,
        found=True,
        note="ok",
        lang="en",
        caption_kind="manual",
        original_language_assumed=False,
        json3_bytes=_json3_bytes(),
        flat_text="Dior Sauvage Elixir\nabsolute beast",
        cue_count=2,
        title="Fragrance review",
        channel_id="UC_fixture",
        publish_date_iso="2026-06-20",
        duration_s=42,
        tooling={"fixture": "youtube_behavioral_projection"},
    )
    code, output_dir = write_caption_packet(
        cap,
        data_root=data_root,
        decision_question="What products are mentioned?",
        now_iso="2026-06-21T00:00:00Z",
    )
    assert code == 0
    return Path(output_dir).name


def _commit_asr(data_root: DataLakeRoot, *, posture: str = "transcribed") -> None:
    def transcribe(_path):
        cues = [
            {"start_ms": 1000, "end_ms": 2000, "text": "Dior Sauvage Elixir"},
            {"start_ms": 2000, "end_ms": 3000, "text": "absolute beast"},
        ] if posture == "transcribed" else []
        return posture, cues, {"tool": "faster-whisper", "model": "tiny"}

    code, _ = write_asr_transcript(
        video_id=_VIDEO_ID,
        audio_bytes=f"fake-audio-{posture}".encode(),
        audio_ext="webm",
        transcribe_fn=transcribe,
        data_root=data_root,
        now_iso="2026-06-21T00:01:00Z",
    )
    assert code == 0


def _extracted_results_for_sources(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"anchor": source["transcript_anchor"], "video_id": _VIDEO_ID, "status": "extracted"}
        for source in sources
    ]


def _synthetic_source(*, anchor: str, source_kind: str, asr_record_id: str | None = None) -> dict[str, Any]:
    source = {
        "platform": "youtube",
        "platform_video_id": _VIDEO_ID,
        "transcript_anchor": anchor,
        "source_kind": source_kind,
        "source_route": "youtube_audio_asr" if source_kind == "asr" else "youtube_captions",
        "source_status": "complete",
        "posture": "transcribed" if source_kind == "asr" else "caption_ready",
        "cue_count": 2,
        "extraction_eligible": True,
        "non_eligible_reason": None,
        "capture_timestamp": "2026-06-21T00:00:00Z",
    }
    if asr_record_id is not None:
        source["asr_record_id"] = asr_record_id
        source["transcript_source_key"] = f"{anchor}:asr:{asr_record_id}"
    else:
        source["transcript_source_key"] = f"{anchor}:{source_kind}"
    return source


def test_projection_correlates_metadata_comments_transcripts_and_extraction_results(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_caption(data_root)
    _commit_asr(data_root)
    sources = transcript_sources_for_video(data_root, _VIDEO_ID)

    projection = project_youtube_behavioral_item_from_lake(
        data_root=data_root,
        platform_video_id=_VIDEO_ID,
        metadata_packet=_metadata_packet(),
        extraction_results=_extracted_results_for_sources(sources),
    )

    assert projection["platform_video_id"] == _VIDEO_ID
    assert projection["metadata_capture"]["comments"]["posture"] == "comments_sample_captured"
    assert projection["metadata_capture"]["comments"]["sample_count"] == 1
    assert projection["metadata_capture"]["availability"]["comments_state"] == "comments_sample_captured"
    assert projection["metadata_capture"]["engagement"]["like_count"] == 34
    assert projection["metadata_capture"]["metric_receipts"]["view_count"]["source_route"] == "ytInitialPlayerResponse.videoDetails"
    assert projection["transcript"]["source_count"] == 2
    assert projection["transcript"]["canonical_source"]["source_kind"] == "caption"
    assert projection["transcript"]["canonical_source"]["caption_kind"] == "manual"
    assert projection["transcript"]["extraction_rollup"]["status"] == "complete"
    assert projection["behavioral_completeness"]["complete"] is True
    assert {source["extraction_status"] for source in projection["transcript"]["sources"]} == {"extracted"}


def test_projection_from_lake_discovers_watch_metadata_packet_by_video_id(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    watch_packet_id = _commit_watch_metadata(data_root)
    _commit_caption(data_root)
    sources = transcript_sources_for_video(data_root, _VIDEO_ID)

    projection = project_youtube_behavioral_item_from_lake(
        data_root=data_root,
        platform_video_id=_VIDEO_ID,
        extraction_results=_extracted_results_for_sources(sources),
    )

    metadata = projection["metadata_capture"]
    assert metadata["capture_packet_id"] == watch_packet_id
    assert metadata["source_surface"] == "youtube_watch_metadata_comments"
    assert metadata["capture_schema_version"] == "youtube_watch_metadata_comments_capture_v1"
    assert metadata["metadata"]["title"] == "Fragrance review"
    assert metadata["comments"]["posture"] == "comments_sample_captured"
    assert metadata["comments"]["sample_count"] == 1
    assert metadata["engagement"]["total_comment_count"] == 12
    assert metadata["metric_receipts"]["total_comment_count"]["source_route"] == "youtubei_next.commentsHeaderRenderer"
    assert "youtube_metadata_packet_absent" not in projection["behavioral_completeness"]["residuals"]


def test_projection_from_lake_uses_latest_watch_metadata_packet_for_video(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_watch_metadata(data_root, now_iso="2026-06-21T00:00:00Z", title="Old title")
    latest_packet_id = _commit_watch_metadata(data_root, now_iso="2026-06-21T00:02:00Z", title="Latest title")

    projection = project_youtube_behavioral_item_from_lake(
        data_root=data_root,
        platform_video_id=_VIDEO_ID,
    )

    assert projection["metadata_capture"]["capture_packet_id"] == latest_packet_id
    assert projection["metadata_capture"]["metadata"]["title"] == "Latest title"


def test_projection_from_lake_residualizes_uninterpretable_watch_metadata_packet(tmp_path) -> None:
    watch_packet_id, projection = _project_with_mutated_watch_capture(
        tmp_path,
        lambda packet_dir: _rewrite_preserved_body(packet_dir, "youtube_watch_capture.json", b"{not-json"),
    )

    _assert_metadata_discovery_failure(projection, watch_packet_id, "invalid_capture_json")


def test_projection_from_lake_residualizes_non_object_watch_metadata_payload(tmp_path) -> None:
    watch_packet_id, projection = _project_with_mutated_watch_capture(
        tmp_path,
        lambda packet_dir: _rewrite_preserved_body(packet_dir, "youtube_watch_capture.json", b"[]"),
    )

    _assert_metadata_discovery_failure(projection, watch_packet_id, "capture_payload_not_object")


def test_projection_from_lake_residualizes_missing_watch_capture_json(tmp_path) -> None:
    def rename_capture_json(packet_dir: Path) -> None:
        manifest_path, manifest, preserved = _watch_capture_manifest_entry(packet_dir)
        relative_path = preserved["relative_packet_path"]
        replacement_path = relative_path.replace("youtube_watch_capture.json", "youtube_watch_capture_missing.json")
        packet_dir.joinpath(*relative_path.split("/")).rename(packet_dir.joinpath(*replacement_path.split("/")))
        preserved["relative_packet_path"] = replacement_path
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    watch_packet_id, projection = _project_with_mutated_watch_capture(tmp_path, rename_capture_json)

    _assert_metadata_discovery_failure(projection, watch_packet_id, "missing_capture_json")


def test_projection_from_lake_residualizes_watch_metadata_packet_missing_video_id(tmp_path) -> None:
    def remove_video_id(packet_dir: Path) -> None:
        _, _, preserved = _watch_capture_manifest_entry(packet_dir)
        target = packet_dir.joinpath(*preserved["relative_packet_path"].split("/"))
        payload = json.loads(target.read_text(encoding="utf-8"))
        payload.pop("platform_video_id", None)
        nested_packet = payload.get("packet")
        assert isinstance(nested_packet, dict)
        nested_packet.pop("platform_video_id", None)
        nested_packet.pop("video_id", None)
        _rewrite_preserved_body(
            packet_dir,
            "youtube_watch_capture.json",
            (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        )

    watch_packet_id, projection = _project_with_mutated_watch_capture(tmp_path, remove_video_id)

    _assert_metadata_discovery_failure(projection, watch_packet_id, "missing_platform_video_id")


def test_transcript_discovery_residualizes_corrupt_youtube_packet_without_aborting_healthy_video(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_caption(data_root)
    corrupt_packet_id = _commit_caption(data_root, video_id="other000000")
    corrupt_packet_dir = data_root.find_packet(corrupt_packet_id)
    assert corrupt_packet_dir is not None
    (corrupt_packet_dir / "manifest.json").write_text("{not-json", encoding="utf-8")

    sources = transcript_sources_for_video(data_root, _VIDEO_ID)

    caption_sources = [source for source in sources if source["source_kind"] == "caption"]
    assert len(caption_sources) == 1
    discovery_problem = next(
        source for source in sources if source["transcript_anchor"] == corrupt_packet_id
    )
    assert discovery_problem["source_kind"] == "discovery"
    assert discovery_problem["source_status"] == "discovery_failed"
    assert discovery_problem["posture"] == "discovery_failed"
    assert discovery_problem["extraction_eligible"] is False

    projection = project_youtube_behavioral_item_from_lake(
        data_root=data_root,
        platform_video_id=_VIDEO_ID,
        metadata_packet=_metadata_packet(),
        extraction_results=[
            {"anchor": caption_sources[0]["transcript_anchor"], "video_id": _VIDEO_ID, "status": "extracted"}
        ],
    )

    assert projection["transcript"]["extraction_rollup"]["status"] == "complete_with_residuals"
    assert projection["transcript"]["extraction_rollup"]["source_problem_count"] == 1
    assert any(
        residual.startswith(f"youtube_transcript_source_discovery_failed:{corrupt_packet_id}:discovery")
        for residual in projection["behavioral_completeness"]["residuals"]
    )


def test_transcript_discovery_residualizes_preserved_file_read_error_without_aborting_healthy_video(monkeypatch, tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_caption(data_root)
    unreadable_packet_id = _commit_caption(data_root, video_id="other000000")
    unreadable_packet_dir = data_root.find_packet(unreadable_packet_id)
    assert unreadable_packet_dir is not None
    original_read_bytes = Path.read_bytes

    def fail_only_unreadable_packet_body(path: Path) -> bytes:
        if path.name.endswith(".json3") and unreadable_packet_dir in path.parents:
            raise OSError("simulated body read failure")
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", fail_only_unreadable_packet_body)

    sources = transcript_sources_for_video(data_root, _VIDEO_ID)

    caption_sources = [source for source in sources if source["source_kind"] == "caption"]
    assert len(caption_sources) == 1
    discovery_problem = next(
        source for source in sources if source["transcript_anchor"] == unreadable_packet_id
    )
    assert discovery_problem["source_status"] == "discovery_failed"
    assert "unreadable preserved file" in discovery_problem["discovery_error"]

    projection = project_youtube_behavioral_item_from_lake(
        data_root=data_root,
        platform_video_id=_VIDEO_ID,
        metadata_packet=_metadata_packet(),
        extraction_results=[
            {"anchor": caption_sources[0]["transcript_anchor"], "video_id": _VIDEO_ID, "status": "extracted"}
        ],
    )

    assert projection["transcript"]["extraction_rollup"]["status"] == "complete_with_residuals"
    assert projection["transcript"]["extraction_rollup"]["source_problem_count"] == 1


def test_projection_does_not_mark_video_complete_when_observed_asr_is_unextracted(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_caption(data_root)
    _commit_asr(data_root)
    sources = transcript_sources_for_video(data_root, _VIDEO_ID)
    caption_anchor = next(source["transcript_anchor"] for source in sources if source["source_kind"] == "caption")

    projection = project_youtube_behavioral_item(
        metadata_packet=_metadata_packet(),
        transcript_sources=sources,
        extraction_results=[{"anchor": caption_anchor, "video_id": _VIDEO_ID, "status": "extracted"}],
    )

    assert projection["transcript"]["extraction_rollup"]["status"] == "partial"
    assert projection["behavioral_completeness"]["complete"] is False
    asr_source = next(source for source in projection["transcript"]["sources"] if source["source_kind"] == "asr")
    assert asr_source["extraction_status"] == "not_attempted"


def test_projection_rejects_anchor_only_result_for_duplicate_eligible_asr_sources() -> None:
    sources = [
        _synthetic_source(anchor="AUDIOPACKET00000000000000", source_kind="asr", asr_record_id="asr_model_a"),
        _synthetic_source(anchor="AUDIOPACKET00000000000000", source_kind="asr", asr_record_id="asr_model_b"),
    ]

    projection = project_youtube_behavioral_item(
        metadata_packet=_metadata_packet(),
        transcript_sources=sources,
        extraction_results=[{"anchor": "AUDIOPACKET00000000000000", "video_id": _VIDEO_ID, "status": "extracted"}],
    )

    assert projection["transcript"]["extraction_rollup"]["status"] == "failed"
    assert projection["behavioral_completeness"]["complete"] is False
    assert {source["extraction_status"] for source in projection["transcript"]["sources"]} == {
        "ambiguous_anchor_result"
    }


def test_projection_counts_failed_asr_posture_as_source_problem(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_caption(data_root)
    _commit_asr(data_root, posture="failed")
    sources = transcript_sources_for_video(data_root, _VIDEO_ID)
    caption_anchor = next(source["transcript_anchor"] for source in sources if source["source_kind"] == "caption")

    projection = project_youtube_behavioral_item(
        metadata_packet=_metadata_packet(),
        transcript_sources=sources,
        extraction_results=[{"anchor": caption_anchor, "video_id": _VIDEO_ID, "status": "extracted"}],
    )

    assert projection["transcript"]["extraction_rollup"]["status"] == "complete_with_residuals"
    assert projection["transcript"]["extraction_rollup"]["source_problem_count"] == 1
    assert projection["behavioral_completeness"]["complete"] is False
    assert any(
        residual.startswith("youtube_transcript_source_failed:")
        for residual in projection["behavioral_completeness"]["residuals"]
    )


def test_projection_residualizes_mismatched_metadata_packet() -> None:
    projection = project_youtube_behavioral_item(
        metadata_packet=_metadata_packet(video_id="other000000"),
        transcript_sources=[],
        platform_video_id=_VIDEO_ID,
    )

    assert projection["metadata_capture"] is None
    assert "youtube_metadata_packet_video_mismatch:other000000" in projection["behavioral_completeness"]["residuals"]


def test_projection_keeps_failed_extraction_visible_with_other_not_attempted_source() -> None:
    sources = [
        _synthetic_source(anchor="CAPTIONPACKET000000000000", source_kind="caption"),
        _synthetic_source(anchor="AUDIOPACKET00000000000000", source_kind="asr", asr_record_id="asr_model_a"),
    ]

    projection = project_youtube_behavioral_item(
        metadata_packet=_metadata_packet(),
        transcript_sources=sources,
        extraction_results=[{"anchor": "CAPTIONPACKET000000000000", "video_id": _VIDEO_ID, "status": "failed"}],
    )

    assert projection["transcript"]["extraction_rollup"]["status"] == "failed"
    assert projection["transcript"]["extraction_rollup"]["extraction_problem_count"] == 1
    assert projection["behavioral_completeness"]["complete"] is False
    assert any(
        residual.startswith("youtube_transcript_extraction_failed:")
        for residual in projection["behavioral_completeness"]["residuals"]
    )


def test_projection_preserves_metadata_only_comment_postures_without_claiming_transcript_completion() -> None:
    projection = project_youtube_behavioral_item(
        metadata_packet=_metadata_packet(comments_posture="disabled", comments=[]),
        platform_video_id=_VIDEO_ID,
    )

    assert projection["metadata_capture"]["comments"]["posture"] == "disabled"
    assert projection["metadata_capture"]["comments"]["sample_count"] == 0
    assert projection["transcript"]["source_count"] == 0
    assert projection["transcript"]["extraction_rollup"]["status"] == "no_extraction_eligible_sources"
    assert projection["behavioral_completeness"]["complete"] is False


def test_transcript_discovery_requires_explicit_availability_rebuild_for_stale_index(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_caption(data_root)
    availability_dir = data_root.path / "indexes" / "availability"
    for entry in availability_dir.glob("*.json"):
        entry.unlink()

    assert transcript_sources_for_video(data_root, _VIDEO_ID) == []

    rebuilt_sources = transcript_sources_for_video(data_root, _VIDEO_ID, rebuild_availability=True)

    assert [source["source_kind"] for source in rebuilt_sources] == ["caption"]
