"""Offline tests for packet-first, source-backed deep-capture persistence."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot
from data_lake.silver_lineage import SOURCE_BACKED_COMPLETE_STATUS, silver_record_source_backed_status
from data_lake.silver_record import silver_content_hash
from runners import run_source_capture_ig_reels_deep_capture as deep_capture_runner
from schemas.audience_comment_models import AudienceComment
from source_capture.ig_reels_deep_capture import ReelDeepCaptureResult
from source_capture.ig_reels_deep_capture_lake import (
    AUDIENCE_COMMENTS_LANE,
    DEEP_CAPTURE_SET_LANE,
    REEL_TRANSCRIPT_LANE,
    current_deep_capture_record,
    deep_capture_record_id,
    write_reel_deep_capture_into_lake,
)


def _root(tmp_path: Path) -> DataLakeRoot:
    return DataLakeRoot.for_test(tmp_path / "forseti-data")


def _comment(cid: str = "c1", *, text: str = "love this") -> AudienceComment:
    return AudienceComment(
        comment_id=cid,
        reel_shortcode="DaA8n7EhqTR",
        author_username="zoe",
        text=text,
        like_count=9,
        created_at_unix=1782400000,
    )


def _substrate(comment: AudienceComment) -> bytes:
    body = {
        "pk": comment.comment_id,
        "user": {"username": comment.author_username},
        "text": comment.text,
        "created_at": comment.created_at_unix,
        "comment_like_count": comment.like_count,
        "__typename": "XIGComment",
    }
    return (json.dumps(body, separators=(",", ":")) + "\n").encode("utf-8")


def _result(
    *,
    media_url: str | None = "https://x.fbcdn.net/o1/v/clip.mp4",
    audio: bytes | None = b"mp4data",
    posture: str = "transcribed",
) -> ReelDeepCaptureResult:
    comment = _comment()
    return ReelDeepCaptureResult(
        reel_shortcode="DaA8n7EhqTR",
        comments=(comment,),
        transcript_posture=posture,
        transcript_cues=({"start_ms": 0, "end_ms": 90, "text": "hi there"},) if posture == "transcribed" else (),
        media_url_used=media_url,
        comment_substrate=_substrate(comment),
        audio_bytes=audio,
        audio_ext="mp4",
    )


def test_writes_packet_backed_envelopes_and_marks_complete(tmp_path: Path) -> None:
    root = _root(tmp_path)
    result = _result()
    written = write_reel_deep_capture_into_lake(
        data_root=root,
        result=result,
        generated_at="2026-06-27T00:00:00Z",
    )
    assert set(written) == {AUDIENCE_COMMENTS_LANE, REEL_TRANSCRIPT_LANE}
    assert root.is_record_set_complete(
        subtree="derived",
        raw_anchor=written.packet_id,
        record_id=written.record_id,
        completion_lane=DEEP_CAPTURE_SET_LANE,
    )
    loaded = root.load_raw_packet(written.packet_id)
    paths = {item["relative_packet_path"] for item in loaded.manifest["preserved_files"]}
    assert all(
        any(path.endswith(name) for path in paths)
        for name in ("rendered_comment_substrate.jsonl", "reel_audio.mp4", "capture_metadata.json")
    )

    for lane in (AUDIENCE_COMMENTS_LANE, REEL_TRANSCRIPT_LANE):
        record = json.loads(written[lane].read_text(encoding="utf-8"))
        assert record["schema_version"] == "silver_vault_record_v0"
        assert record["raw_anchor"] == written.packet_id
        assert silver_record_source_backed_status(record) == SOURCE_BACKED_COMPLETE_STATUS
        assert current_deep_capture_record(
            root,
            record=record,
            raw_anchor=written.packet_id,
            lane=lane,
            record_id=written.record_id,
        )


def test_current_record_uses_physical_gate_without_legacy_lineage_version(tmp_path: Path) -> None:
    root = _root(tmp_path)
    written = write_reel_deep_capture_into_lake(
        data_root=root,
        result=_result(),
        generated_at="2026-06-27T00:00:00Z",
    )
    record = json.loads(written[AUDIENCE_COMMENTS_LANE].read_text(encoding="utf-8"))
    record.pop("lineage_schema_version")
    record["content_hash"] = f"sha256:{silver_content_hash(record)}"

    assert current_deep_capture_record(
        root,
        record=record,
        raw_anchor=written.packet_id,
        lane=AUDIENCE_COMMENTS_LANE,
        record_id=written.record_id,
    )


def test_current_record_rejects_altered_preserved_packet_bytes(tmp_path: Path) -> None:
    root = _root(tmp_path)
    written = write_reel_deep_capture_into_lake(
        data_root=root,
        result=_result(),
        generated_at="2026-06-27T00:00:00Z",
    )
    record = json.loads(written[AUDIENCE_COMMENTS_LANE].read_text(encoding="utf-8"))
    packet_dir = root.find_packet(written.packet_id)
    assert packet_dir is not None
    source_path = packet_dir / record["raw_refs"][0]["relative_packet_path"]
    assert source_path.is_file()
    source_path.write_bytes(b"tampered\n")

    assert not current_deep_capture_record(
        root,
        record=record,
        raw_anchor=written.packet_id,
        lane=AUDIENCE_COMMENTS_LANE,
        record_id=written.record_id,
    )


def test_signed_media_url_is_never_persisted(tmp_path: Path) -> None:
    root = _root(tmp_path)
    signed = "https://x.fbcdn.net/o1/v/clip.mp4?oh=SECRET_SIGNATURE_TOKEN&oe=DEADBEEF"
    written = write_reel_deep_capture_into_lake(
        data_root=root,
        result=_result(media_url=signed),
        generated_at="2026-06-27T00:00:00Z",
    )
    packet_dir = root.find_packet(written.packet_id)
    assert packet_dir is not None
    raw = b"".join(path.read_bytes() for path in packet_dir.rglob("*") if path.is_file())
    raw += b"".join(path.read_bytes() for path in written.values())
    assert signed.encode() not in raw
    assert b"SECRET_SIGNATURE_TOKEN" not in raw
    assert b"DEADBEEF" not in raw
    transcript = json.loads(written[REEL_TRANSCRIPT_LANE].read_text(encoding="utf-8"))
    assert transcript["provenance"]["media_provenance"] == {
        "audio_handle_used": True,
        "media_host": "x.fbcdn.net",
    }


def test_comment_must_match_exact_retained_substrate(tmp_path: Path) -> None:
    root = _root(tmp_path)
    result = _result()
    forged = result.comments[0].model_copy(update={"text": "different"})
    with pytest.raises(ValueError, match="do not match"):
        write_reel_deep_capture_into_lake(
            data_root=root,
            result=result.__class__(
                **{**result.__dict__, "comments": (forged,)},
            ),
            generated_at="2026-06-27T00:00:00Z",
        )


def test_failed_audio_leg_writes_comments_only(tmp_path: Path) -> None:
    root = _root(tmp_path)
    written = write_reel_deep_capture_into_lake(
        data_root=root,
        result=_result(audio=None, posture="download_failed"),
        generated_at="2026-06-27T00:00:00Z",
    )
    assert set(written) == {AUDIENCE_COMMENTS_LANE}
    assert any(item.startswith("transcript_not_admitted:download_failed") for item in written.excluded_legs)
    marker = root.record_path(
        subtree="derived",
        raw_anchor=written.packet_id,
        lane=DEEP_CAPTURE_SET_LANE,
        record_id=written.record_id,
    )
    assert json.loads(marker.read_text(encoding="utf-8"))["member_lanes"] == [AUDIENCE_COMMENTS_LANE]


def test_transcript_without_audio_bytes_is_never_admitted(tmp_path: Path) -> None:
    root = _root(tmp_path)
    written = write_reel_deep_capture_into_lake(
        data_root=root,
        result=_result(audio=None),
        generated_at="2026-06-27T00:00:00Z",
    )
    assert REEL_TRANSCRIPT_LANE not in written


def test_no_source_backed_leg_refuses_without_packet_or_silver(tmp_path: Path) -> None:
    root = _root(tmp_path)
    result = ReelDeepCaptureResult("DaA8n7EhqTR", (), "download_failed", (), None)
    with pytest.raises(ValueError, match="no source-backed"):
        write_reel_deep_capture_into_lake(data_root=root, result=result, generated_at="t")
    assert root.list_available(source_family="instagram_creator") == []


def test_each_capture_mints_a_new_packet_without_rewriting_history(tmp_path: Path) -> None:
    root = _root(tmp_path)
    first = write_reel_deep_capture_into_lake(data_root=root, result=_result(), generated_at="t")
    second = write_reel_deep_capture_into_lake(data_root=root, result=_result(), generated_at="t")
    assert first.record_id == second.record_id == deep_capture_record_id(_result())
    assert first.packet_id != second.packet_id


def test_persist_helper_reports_packet_anchor(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    root = _root(tmp_path)
    seen: dict[str, object] = {}

    def resolve(*, explicit=None):  # noqa: ANN001
        seen["explicit"] = explicit
        return root

    monkeypatch.setattr(deep_capture_runner.DataLakeRoot, "resolve", staticmethod(resolve))
    status = deep_capture_runner._persist_deep_capture(_result(), data_root_arg=None)
    assert seen == {"explicit": None}
    assert status.startswith("persisted: packet=")
    packet_id = status.split("packet=", 1)[1].split()[0]
    assert root.find_packet(packet_id) is not None
