"""Unit tests for the YouTube caption acquisition core (transcript spine v0).

Network-free: exercises the rolling-cue flattener and the packet builder from a
canned CaptionFetch, asserting the produced SourceCapturePacket is contract-valid,
preserves only raw bytes, records identity, and writes the NON-AUTHORITATIVE view.
"""
from __future__ import annotations

import json
from pathlib import Path

from source_capture.models import SourceCapturePacket
from source_capture.transcript import CaptionFetch, flatten_json3, write_caption_packet


def test_flatten_json3_dedups_rolling_cues_and_counts_seg_events():
    raw = json.dumps(
        {
            "events": [
                {"segs": [{"utf8": "line one"}]},
                {"segs": [{"utf8": "line one"}]},  # rolling duplicate -> collapsed
                {"segs": [{"utf8": "line two"}]},
                {"segs": []},  # no segs -> skipped, not counted
                {"tStartMs": 9},  # no segs key -> skipped
            ]
        }
    ).encode("utf-8")
    text, cues = flatten_json3(raw)
    assert text == "line one\nline two"  # consecutive duplicate removed
    assert cues == 3  # three events carried segs


def _found_cap() -> CaptionFetch:
    json3 = json.dumps({"events": [{"tStartMs": 0, "segs": [{"utf8": "hello world"}]}]}).encode("utf-8")
    return CaptionFetch(
        video_id="vid12345678",
        found=True,
        note="ok",
        lang="en",
        caption_kind="auto",
        json3_bytes=json3,
        flat_text="hello world",
        cue_count=1,
        title="A Title",
        channel_id="UC_test_channel",
        publish_date_iso="2026-06-20",
        duration_s=42,
        tooling={"tool": "yt-dlp", "tool_version": "x", "client": "yt-dlp-default"},
    )


def test_write_caption_packet_produces_contract_valid_packet(tmp_path):
    out = tmp_path / "pkt"
    code, msg = write_caption_packet(
        _found_cap(), output_directory=out, decision_question="Q", now_iso="2026-06-20T00:00:00Z"
    )
    assert code == 0

    packet_dir = Path(msg)
    manifest = json.loads((packet_dir / "manifest.json").read_text(encoding="utf-8"))
    packet = SourceCapturePacket(**manifest)  # raises if contract-invalid

    assert packet.source_family == "youtube"
    assert packet.source_surface == "youtube_captions"
    assert len(packet.preserved_files) == 2
    assert all(f.hash_basis == "raw_stored_bytes" for f in packet.preserved_files)  # no laundering

    meta_path = next((packet_dir / "raw").glob("*capture_metadata.json"))
    ident = json.loads(meta_path.read_text(encoding="utf-8"))
    assert ident["platform"] == "youtube"
    assert ident["platform_video_id"] == "vid12345678"
    assert ident["caption_kind"] == "auto"
    assert ident["publish_date_iso"] == "2026-06-20"

    view = packet_dir.parent / "vid12345678_transcript_view_NONAUTHORITATIVE.txt"
    assert view.exists()
    assert "hello world" in view.read_text(encoding="utf-8")


def test_write_caption_packet_no_caption_returns_asr_required(tmp_path):
    cap = CaptionFetch(video_id="novid000000", found=False, note="no caption track")
    code, msg = write_caption_packet(cap, output_directory=tmp_path / "x", decision_question="Q")
    assert code == 4
    assert "ASR" in msg


def test_fetch_rejects_malformed_video_id():
    # path-traversal / bad id rejected before any network call (review F5).
    from source_capture.transcript import youtube_captions as yc

    cap = yc.fetch_youtube_caption_artifacts("../etc/passwd")
    assert cap.found is False
    assert "invalid" in cap.note.lower()


def test_fetch_rejects_translated_en_as_original(monkeypatch):
    # Spanish-original video exposing ONLY auto-translated English must NOT be accepted as
    # original-language captions (review F2). The yt-dlp seam is mocked -> no yt-dlp/network needed.
    from source_capture.transcript import youtube_captions as yc

    monkeypatch.setattr(yc, "_ytdlp_version", lambda: "test")
    monkeypatch.setattr(yc, "_extract_info", lambda url: {
        "language": "es",
        "subtitles": {},
        "automatic_captions": {"en": [{"ext": "json3", "url": "x"}]},
        "title": "T",
        "channel_id": "UC",
        "upload_date": "20260101",
        "duration": 30,
    })
    cap = yc.fetch_youtube_caption_artifacts("abcdefghijk")
    assert cap.found is False
    assert "original-language" in cap.note


def test_write_caption_packet_rejects_bad_video_id(tmp_path):
    # builder must not build filenames/paths from an unvalidated id (review F5).
    bad = CaptionFetch(
        video_id="../../evil", found=True, note="ok", lang="en", caption_kind="auto",
        json3_bytes=b"{}", flat_text="x", cue_count=1,
    )
    code, msg = write_caption_packet(bad, output_directory=tmp_path / "p", decision_question="Q")
    assert code == 5
    assert "invalid video id" in msg


def test_assumed_original_language_flag_recorded(tmp_path):
    cap = _found_cap()
    cap.original_language_assumed = True
    code, msg = write_caption_packet(
        cap, output_directory=tmp_path / "p", decision_question="Q", now_iso="2026-06-20T00:00:00Z"
    )
    assert code == 0
    meta = next((Path(msg) / "raw").glob("*capture_metadata.json"))
    ident = json.loads(meta.read_text(encoding="utf-8"))
    assert ident["original_language_assumed"] is True
