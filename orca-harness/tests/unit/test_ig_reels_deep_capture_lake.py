"""Offline tests for deep-capture persistence (silver record-set per reel)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, DataLakeRootError
from schemas.audience_comment_models import AudienceComment
from source_capture.ig_reels_deep_capture import ReelDeepCaptureResult
from source_capture.ig_reels_deep_capture_lake import (
    AUDIENCE_COMMENTS_LANE,
    DEEP_CAPTURE_SET_LANE,
    REEL_TRANSCRIPT_LANE,
    deep_capture_record_id,
    write_reel_deep_capture_into_lake,
)


def _root(tmp_path: Path) -> DataLakeRoot:
    return DataLakeRoot.for_test(tmp_path / "orca-data")


def _comment(cid: str = "c1", *, likes: int = 9) -> AudienceComment:
    return AudienceComment(
        comment_id=cid, reel_shortcode="DaA8n7EhqTR", author_username="zoe",
        text="love this", like_count=likes, created_at_unix=1782400000,
    )


def _result(*, media_url: str | None = "https://x.fbcdn.net/o1/v/clip.mp4") -> ReelDeepCaptureResult:
    return ReelDeepCaptureResult(
        reel_shortcode="DaA8n7EhqTR",
        comments=(_comment(),),
        transcript_posture="transcribed",
        transcript_cues=({"start_ms": 0, "end_ms": 90, "text": "hi there"},),
        media_url_used=media_url,
    )


def test_writes_both_voices_and_marks_complete(tmp_path: Path) -> None:
    root = _root(tmp_path)
    result = _result()
    written = write_reel_deep_capture_into_lake(data_root=root, result=result, generated_at="2026-06-27T00:00:00Z")
    assert set(written) == {AUDIENCE_COMMENTS_LANE, REEL_TRANSCRIPT_LANE}
    rid = deep_capture_record_id(result)
    assert root.is_record_set_complete(
        subtree="derived", raw_anchor="DaA8n7EhqTR", record_id=rid, completion_lane=DEEP_CAPTURE_SET_LANE
    )
    comments_doc = json.loads(written[AUDIENCE_COMMENTS_LANE].read_text(encoding="utf-8"))
    assert comments_doc["comment_count"] == 1
    assert comments_doc["comments"][0]["author_username"] == "zoe"
    transcript_doc = json.loads(written[REEL_TRANSCRIPT_LANE].read_text(encoding="utf-8"))
    assert transcript_doc["transcript_posture"] == "transcribed" and transcript_doc["cue_count"] == 1
    assert transcript_doc["cues"][0]["text"] == "hi there"


def test_transient_signed_url_is_never_persisted(tmp_path: Path) -> None:
    root = _root(tmp_path)
    signed = "https://x.fbcdn.net/o1/v/clip.mp4?oh=SECRET_SIGNATURE_TOKEN&oe=DEADBEEF"
    written = write_reel_deep_capture_into_lake(
        data_root=root, result=_result(media_url=signed), generated_at="t"
    )
    raw = written[AUDIENCE_COMMENTS_LANE].read_bytes() + written[REEL_TRANSCRIPT_LANE].read_bytes()
    assert b"SECRET_SIGNATURE_TOKEN" not in raw and b"DEADBEEF" not in raw
    doc = json.loads(written[AUDIENCE_COMMENTS_LANE].read_text(encoding="utf-8"))
    assert doc["media_provenance"] == {"audio_handle_used": True, "media_host": "x.fbcdn.net"}


def test_no_audio_handle_provenance(tmp_path: Path) -> None:
    root = _root(tmp_path)
    result = ReelDeepCaptureResult("DaA8n7EhqTR", (_comment(),), "no_audio_handle", (), None)
    written = write_reel_deep_capture_into_lake(data_root=root, result=result, generated_at="t")
    doc = json.loads(written[AUDIENCE_COMMENTS_LANE].read_text(encoding="utf-8"))
    assert doc["media_provenance"] == {"audio_handle_used": False, "media_host": None}


def test_rewrite_same_record_is_refused_write_once(tmp_path: Path) -> None:
    root = _root(tmp_path)
    result = _result()
    write_reel_deep_capture_into_lake(data_root=root, result=result, generated_at="t")
    with pytest.raises(DataLakeRootError):
        write_reel_deep_capture_into_lake(data_root=root, result=result, generated_at="t")
