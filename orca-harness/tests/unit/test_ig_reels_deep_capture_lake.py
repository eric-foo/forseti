"""Offline tests for deep-capture persistence (silver record-set per reel)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, DataLakeRootError
from runners import run_source_capture_ig_reels_deep_capture as deep_capture_runner
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


def test_transient_signed_url_redacted_from_comment_and_cue_payloads(tmp_path: Path) -> None:
    root = _root(tmp_path)
    signed = "https://x.fbcdn.net/o1/v/clip.mp4?oh=SECRET_SIGNATURE_TOKEN&oe=DEADBEEF"
    comment = _comment().model_copy(update={"text": f"watch {signed} token SECRET_SIGNATURE_TOKEN"})
    result = ReelDeepCaptureResult(
        reel_shortcode="DaA8n7EhqTR",
        comments=(comment,),
        transcript_posture="transcribed",
        transcript_cues=(
            {"start_ms": 0, "end_ms": 90, "text": "heard DEADBEEF", "debug_media_url": signed},
        ),
        media_url_used=signed,
    )

    written = write_reel_deep_capture_into_lake(data_root=root, result=result, generated_at="t")

    raw = written[AUDIENCE_COMMENTS_LANE].read_bytes() + written[REEL_TRANSCRIPT_LANE].read_bytes()
    for forbidden in (signed, "SECRET_SIGNATURE_TOKEN", "DEADBEEF"):
        assert forbidden.encode("utf-8") not in raw
    comments_doc = json.loads(written[AUDIENCE_COMMENTS_LANE].read_text(encoding="utf-8"))
    transcript_doc = json.loads(written[REEL_TRANSCRIPT_LANE].read_text(encoding="utf-8"))
    assert "[redacted_transient_media_url]" in comments_doc["comments"][0]["text"]
    assert transcript_doc["cues"][0]["debug_media_url"] == "[redacted_transient_media_url]"
    assert "[redacted_transient_media_url]" in transcript_doc["cues"][0]["text"]
    assert comments_doc["media_provenance"] == {"audio_handle_used": True, "media_host": "x.fbcdn.net"}


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


def test_persist_helper_allows_env_resolution(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = _root(tmp_path)
    result = _result()
    seen: dict[str, object] = {}

    def resolve(*, explicit=None):  # noqa: ANN001
        seen["explicit"] = explicit
        return root

    monkeypatch.setattr(deep_capture_runner.DataLakeRoot, "resolve", staticmethod(resolve))

    status = deep_capture_runner._persist_deep_capture(result, data_root_arg=None)

    rid = deep_capture_record_id(result)
    assert seen == {"explicit": None}
    assert status.startswith("persisted:")
    assert root.is_record_set_complete(
        subtree="derived", raw_anchor="DaA8n7EhqTR", record_id=rid, completion_lane=DEEP_CAPTURE_SET_LANE
    )


def test_nc_ht_host_preserved_while_full_signed_url_redacted_from_payloads(tmp_path: Path) -> None:
    # Combined high-risk regression: an IG media URL carries the host in _nc_ht=<host> (which was
    # clobbering the media_host provenance field) AND the full signed URL is embedded in comment +
    # cue text. media_host must be PRESERVED (host is not a secret) while the full URL + signature
    # (oh/oe values) are redacted from BOTH lanes.
    root = _root(tmp_path)
    signed = (
        "https://scontent.cdninstagram.com/o1/v/clip.mp4"
        "?_nc_ht=scontent.cdninstagram.com&oh=SECRET_SIGNATURE_TOKEN&oe=DEADBEEF"
    )
    comment = _comment().model_copy(update={"text": f"source: {signed}"})
    result = ReelDeepCaptureResult(
        reel_shortcode="DaA8n7EhqTR",
        comments=(comment,),
        transcript_posture="transcribed",
        transcript_cues=({"start_ms": 0, "end_ms": 90, "text": "clip", "debug_media_url": signed},),
        media_url_used=signed,
    )
    written = write_reel_deep_capture_into_lake(data_root=root, result=result, generated_at="t")
    comments_doc = json.loads(written[AUDIENCE_COMMENTS_LANE].read_text(encoding="utf-8"))
    assert comments_doc["media_provenance"]["media_host"] == "scontent.cdninstagram.com"
    raw = written[AUDIENCE_COMMENTS_LANE].read_bytes() + written[REEL_TRANSCRIPT_LANE].read_bytes()
    for forbidden in (signed, "SECRET_SIGNATURE_TOKEN", "DEADBEEF"):
        assert forbidden.encode("utf-8") not in raw
