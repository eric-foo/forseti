"""Unit tests for the IG Reels ASR-capture core (IG transcript spine v0).

Network-free + ASR-free: a canned audio blob + an injected fake transcriber exercise the
audio-capture packet + transcript_asr derived-record write, asserting IG identity
(source_family=instagram_creator, source_surface=ig_reels_audio), raw-only preservation (no
laundering), provenance, posture, and the shortcode guard. The yt-dlp fetch classifier,
URL->shortcode parse, and the pre-network shortcode guard are tested purely (no network).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from data_lake.root import DataLakeRoot
from source_capture.models import SourceCapturePacket
from source_capture.transcript.ig_reels_audio_packet import (
    classify_ig_fetch_failure,
    download_ig_reel_audio,
    ig_shortcode_from_url,
    write_ig_reels_asr_transcript,
)

_AUDIO = b"FAKE-IG-AUDIO-BYTES"
_SHORTCODE = "DZ69knlsDb1"
_MODEL_INFO = {
    "tool": "faster-whisper",
    "tool_version": "1.2.1",
    "model": "small",
    "model_repo_id": "Systran/faster-whisper-small",
    "model_digest": None,
    "compute_type": "int8",
    "decode_params": {"beam_size": 1, "vad_filter": True},
    "speech_gate": "faster-whisper builtin Silero VAD (onnx)",
}


def _lake(tmp_path: Path) -> DataLakeRoot:
    return DataLakeRoot.for_test(tmp_path / "lake")


def _packet_id_from_msg(msg: str) -> str:
    # flat: derived/<packet_id>/transcript_asr/<record_id>; sharded: derived/<shard>/<packet_id>/...
    return msg.split(" ")[0].split("/")[-3]


def _load_derived(root: DataLakeRoot, msg: str) -> dict:
    rel = msg.split(" ")[0]
    return json.loads((root.path / rel).read_text(encoding="utf-8"))


def _load_capture_metadata(root: DataLakeRoot, packet_id: str) -> dict:
    loaded = root.load_raw_packet(packet_id)
    file_paths = {
        pf.get("file_id", ""): pf.get("relative_packet_path", "")
        for pf in loaded.manifest.get("preserved_files", [])
        if isinstance(pf, dict)
    }
    metadata_file_id = next(fid for fid, path in file_paths.items() if path.endswith("capture_metadata.json"))
    return json.loads(loaded.bodies[metadata_file_id].decode("utf-8"))


def _manifest_path(root: DataLakeRoot, packet_id: str) -> Path:
    packet_dir = root.find_packet(packet_id)
    assert packet_dir is not None
    return packet_dir / "manifest.json"


def test_transcribed_writes_ig_audio_packet_and_derived_record(tmp_path):
    root = _lake(tmp_path)

    def fake_transcribe(_audio_path):
        return "transcribed", [{"start_ms": 0, "end_ms": 1500, "text": "Chanel is number one"}], _MODEL_INFO

    code, msg = write_ig_reels_asr_transcript(
        shortcode=_SHORTCODE, audio_bytes=_AUDIO, audio_ext="m4a",
        transcribe_fn=fake_transcribe, data_root=root, now_iso="2026-06-25T00:00:00Z",
    )
    assert code == 0
    pid = _packet_id_from_msg(msg)

    # audio packet: IG identity, contract-valid, raw-only, no transcript laundered in
    manifest = json.loads(_manifest_path(root, pid).read_text(encoding="utf-8"))
    packet = SourceCapturePacket(**manifest)
    assert packet.source_family == "instagram_creator"
    assert packet.source_surface == "ig_reels_audio"
    assert len(packet.preserved_files) == 2
    assert all(f.hash_basis == "raw_stored_bytes" for f in packet.preserved_files)
    assert not any("transcript" in f.original_path.lower() for f in packet.preserved_files)

    # derived transcript record: IG identity + posture + cues + provenance
    rec = _load_derived(root, msg)
    assert rec["platform"] == "instagram"
    assert rec["video_id"] == _SHORTCODE  # IG shortcode carried in the reused video_id field
    assert rec["shortcode"] == _SHORTCODE
    assert rec["posture"] == "transcribed"
    assert rec["cue_count"] == 1
    assert rec["cues"][0]["text"] == "Chanel is number one"
    prov = rec["provenance"]
    assert prov["source_packet_id"] == pid
    assert prov["source_sha256"] == hashlib.sha256(_AUDIO).hexdigest()
    assert prov["model"] == "small"


def test_identity_extra_cannot_override_core_ig_identity(tmp_path):
    root = _lake(tmp_path)
    code, msg = write_ig_reels_asr_transcript(
        shortcode=_SHORTCODE, audio_bytes=_AUDIO, audio_ext="m4a",
        transcribe_fn=lambda _path: ("no_speech", [], _MODEL_INFO),
        data_root=root,
        now_iso="2026-06-25T00:00:00Z",
        identity_extra={
            "platform": "youtube",
            "platform_shortcode": "wrong",
            "canonical_url": "https://www.youtube.com/watch?v=wrong",
            "capture_timestamp": "1999-01-01T00:00:00Z",
            "probe_label": "kept",
        },
    )

    assert code == 0
    meta = _load_capture_metadata(root, _packet_id_from_msg(msg))
    assert meta["platform"] == "instagram"
    assert meta["platform_shortcode"] == _SHORTCODE
    assert meta["canonical_url"] == f"https://www.instagram.com/reel/{_SHORTCODE}/"
    assert meta["capture_timestamp"] == "2026-06-25T00:00:00Z"
    assert meta["probe_label"] == "kept"


def test_model_info_cannot_override_source_provenance(tmp_path):
    root = _lake(tmp_path)
    model_info = {
        **_MODEL_INFO,
        "source_packet_id": "spoofed-packet",
        "source_file_id": "spoofed-file",
        "source_sha256": "spoofed-sha",
    }

    code, msg = write_ig_reels_asr_transcript(
        shortcode=_SHORTCODE, audio_bytes=_AUDIO, audio_ext="m4a",
        transcribe_fn=lambda _path: ("no_speech", [], model_info), data_root=root,
    )

    assert code == 0
    pid = _packet_id_from_msg(msg)
    prov = _load_derived(root, msg)["provenance"]
    assert prov["source_packet_id"] == pid
    assert prov["source_file_id"] == "file_01"
    assert prov["source_sha256"] == hashlib.sha256(_AUDIO).hexdigest()


def test_long_or_unsafe_model_name_keeps_record_id_segment_safe(tmp_path):
    root = _lake(tmp_path)
    long_model = "provider/" + ("x" * 200)
    model_info = {**_MODEL_INFO, "model": long_model}

    code, msg = write_ig_reels_asr_transcript(
        shortcode=_SHORTCODE, audio_bytes=_AUDIO, audio_ext="m4a",
        transcribe_fn=lambda _path: ("transcribed", [{"start_ms": 0, "end_ms": 1, "text": "x"}], model_info),
        data_root=root,
    )

    assert code == 0
    record_id = msg.split(" ")[0].split("/")[-1]
    assert len(record_id) <= 128
    assert "/" not in record_id
    assert _load_derived(root, msg)["provenance"]["model"] == long_model


def test_no_speech_records_posture_without_cues(tmp_path):
    root = _lake(tmp_path)

    def fake_transcribe(_audio_path):
        return "no_speech", [], _MODEL_INFO

    code, msg = write_ig_reels_asr_transcript(
        shortcode=_SHORTCODE, audio_bytes=_AUDIO, audio_ext="m4a",
        transcribe_fn=fake_transcribe, data_root=root,
    )
    assert code == 0
    rec = _load_derived(root, msg)
    assert rec["posture"] == "no_speech"
    assert rec["cue_count"] == 0
    assert rec["cues"] == []
    pid = _packet_id_from_msg(msg)
    assert _manifest_path(root, pid).is_file()


def test_invalid_shortcode_refused(tmp_path):
    root = _lake(tmp_path)
    code, msg = write_ig_reels_asr_transcript(
        shortcode="../../evil", audio_bytes=_AUDIO, audio_ext="m4a",
        transcribe_fn=lambda p: ("transcribed", [], _MODEL_INFO), data_root=root,
    )
    assert code == 5
    assert "invalid ig shortcode" in msg


def test_invalid_audio_extension_refused_before_write(tmp_path):
    root = _lake(tmp_path)
    code, msg = write_ig_reels_asr_transcript(
        shortcode=_SHORTCODE, audio_bytes=_AUDIO, audio_ext="../m4a",
        transcribe_fn=lambda p: ("transcribed", [], _MODEL_INFO), data_root=root,
    )
    assert code == 5
    assert "invalid audio extension" in msg
    assert list((root.path / "raw").iterdir()) == []


def test_empty_audio_refused(tmp_path):
    root = _lake(tmp_path)
    code, msg = write_ig_reels_asr_transcript(
        shortcode=_SHORTCODE, audio_bytes=b"", audio_ext="m4a",
        transcribe_fn=lambda p: ("transcribed", [], _MODEL_INFO), data_root=root,
    )
    assert code == 6
    assert "no audio" in msg


def test_transcriber_exception_records_failed_posture(tmp_path):
    root = _lake(tmp_path)

    def boom(_audio_path):
        raise RuntimeError("model load failed")

    code, msg = write_ig_reels_asr_transcript(
        shortcode=_SHORTCODE, audio_bytes=_AUDIO, audio_ext="m4a",
        transcribe_fn=boom, data_root=root,
    )
    assert code == 0
    rec = _load_derived(root, msg)
    assert rec["posture"] == "failed"
    assert rec["cue_count"] == 0
    assert rec["cues"] == []
    assert "failure_message" in rec["provenance"]
    assert _manifest_path(root, _packet_id_from_msg(msg)).is_file()


def test_transcribed_without_cues_normalizes_to_no_speech(tmp_path):
    root = _lake(tmp_path)
    code, msg = write_ig_reels_asr_transcript(
        shortcode=_SHORTCODE, audio_bytes=_AUDIO, audio_ext="m4a",
        transcribe_fn=lambda p: ("transcribed", [], _MODEL_INFO), data_root=root,
    )
    assert code == 0
    assert _load_derived(root, msg)["posture"] == "no_speech"


def test_rerun_is_a_new_observation_not_an_overwrite(tmp_path):
    root = _lake(tmp_path)

    def t(_audio_path):
        return "transcribed", [{"start_ms": 0, "end_ms": 1, "text": "x"}], _MODEL_INFO

    c1, _ = write_ig_reels_asr_transcript(shortcode=_SHORTCODE, audio_bytes=_AUDIO, audio_ext="m4a", transcribe_fn=t, data_root=root)
    c2, _ = write_ig_reels_asr_transcript(shortcode=_SHORTCODE, audio_bytes=_AUDIO, audio_ext="m4a", transcribe_fn=t, data_root=root)
    assert c1 == 0 and c2 == 0
    assert len(list((root.path / "raw").glob("**/manifest.json"))) == 2  # two distinct audio packets, not a refusal


# --- yt-dlp fetch classifier + URL parse + pre-network guard (no network) ------


def test_classify_audience_restricted_is_access_gated():
    err = "ERROR: [Instagram] DZWSHBTOjPa: This content isn't available to everyone: It can't be seen by certain audiences."
    assert classify_ig_fetch_failure(err) == "access_gated"


def test_classify_login_required_is_access_gated():
    assert classify_ig_fetch_failure("ERROR: Requested content requires login") == "access_gated"
    assert classify_ig_fetch_failure("This account is private") == "access_gated"
    assert classify_ig_fetch_failure("This video is private") == "access_gated"


def test_classify_private_network_error_is_unavailable():
    assert classify_ig_fetch_failure("ERROR: private network timeout while connecting") == "unavailable"


def test_classify_other_failure_is_unavailable():
    assert classify_ig_fetch_failure("ERROR: HTTP Error 404: Not Found") == "unavailable"
    assert classify_ig_fetch_failure("") == "unavailable"


def test_ig_shortcode_from_url_parses_permalink_forms():
    assert ig_shortcode_from_url("https://www.instagram.com/reel/DZ69knlsDb1/") == "DZ69knlsDb1"
    assert ig_shortcode_from_url("https://www.instagram.com/p/DaALKgOsWn0/") == "DaALKgOsWn0"
    assert ig_shortcode_from_url("https://www.instagram.com/tv/DZ69knlsDb1/") == "DZ69knlsDb1"
    assert ig_shortcode_from_url("https://www.instagram.com/reels/DYCkRNsAXrY/") == "DYCkRNsAXrY"  # /reels/ plural share form
    assert ig_shortcode_from_url("www.instagram.com/reel/DZ69knlsDb1/") == "DZ69knlsDb1"
    assert ig_shortcode_from_url("https://m.instagram.com/reel/DZ69knlsDb1/?utm_source=ig_web_copy_link") == "DZ69knlsDb1"
    assert ig_shortcode_from_url("DZ69knlsDb1") == "DZ69knlsDb1"  # bare shortcode passthrough
    assert ig_shortcode_from_url("not a url or code !!") is None


def test_ig_shortcode_from_url_rejects_url_smuggling_and_bad_segments():
    assert ig_shortcode_from_url("https://evil.example/?next=https://www.instagram.com/reel/DZ69knlsDb1/") is None
    assert ig_shortcode_from_url("https://instagram.com.evil.example/reel/DZ69knlsDb1/") is None
    assert ig_shortcode_from_url(f"https://www.instagram.com/reel/{'A' * 33}/") is None
    assert ig_shortcode_from_url("https://www.instagram.com/reel/DZ69knlsDb1/extra") is None
    assert ig_shortcode_from_url("https://www.instagram.com/reel/../../etc") is None


def test_download_rejects_bad_shortcode_pre_network():
    # the shortcode is validated BEFORE building a URL / touching the network.
    fetch = download_ig_reel_audio("../etc/passwd")
    assert fetch.status == "unavailable"
    assert fetch.audio_bytes is None
    assert "pre-network" in fetch.detail
