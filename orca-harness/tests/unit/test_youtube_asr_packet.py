"""Unit tests for the ASR-fallback core (transcript spine v0).

Network-free + ASR-free: a canned audio blob + an injected fake transcriber exercise the
audio-capture packet + transcript_asr derived-record write, asserting contract validity,
raw-only preservation (no laundering), provenance, posture, and the video-id guard.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from data_lake.root import DataLakeRoot
from source_capture.models import SourceCapturePacket
from source_capture.transcript import write_asr_transcript

_AUDIO = b"FAKE-OPUS-AUDIO-BYTES"
_MODEL_INFO = {
    "tool": "faster-whisper",
    "tool_version": "1.2.1",
    "model": "small",
    "model_repo_id": "Systran/faster-whisper-small",
    "model_digest": None,
    "model_digest_basis": "not available from the faster-whisper runtime",
    "compute_type": "int8",
    "decode_params": {"beam_size": 1, "vad_filter": True},
    "speech_gate": "faster-whisper builtin Silero VAD (onnx)",
}


def _lake(tmp_path: Path) -> DataLakeRoot:
    return DataLakeRoot.for_test(tmp_path / "lake")


def _packet_id_from_msg(msg: str) -> str:
    # msg: "derived/<packet_id>/transcript_asr/<record_id> [posture, N cues]"
    return msg.split("/")[1]


def _load_derived(root: DataLakeRoot, msg: str) -> dict:
    rel = msg.split(" ")[0]  # derived/<pid>/transcript_asr/<rid>
    return json.loads((root.path / rel).read_text(encoding="utf-8"))


def test_transcribed_writes_audio_packet_and_derived_record(tmp_path):
    root = _lake(tmp_path)

    def fake_transcribe(_audio_path):
        return "transcribed", [{"start_ms": 0, "end_ms": 1500, "text": "hello world"}], _MODEL_INFO

    code, msg = write_asr_transcript(
        video_id="abcdefghijk", audio_bytes=_AUDIO, audio_ext="webm",
        transcribe_fn=fake_transcribe, data_root=root, now_iso="2026-06-20T00:00:00Z",
    )
    assert code == 0
    pid = _packet_id_from_msg(msg)

    # audio packet: contract-valid, raw-only, no transcript laundered in
    manifest = json.loads((root.path / "raw" / pid / "manifest.json").read_text(encoding="utf-8"))
    packet = SourceCapturePacket(**manifest)
    assert packet.source_surface == "youtube_audio"
    assert len(packet.preserved_files) == 2
    assert all(f.hash_basis == "raw_stored_bytes" for f in packet.preserved_files)
    assert not any("transcript" in f.original_path.lower() for f in packet.preserved_files)

    # derived transcript record: posture + cues + provenance
    rec = _load_derived(root, msg)
    assert rec["posture"] == "transcribed"
    assert rec["cue_count"] == 1
    assert rec["cues"][0]["text"] == "hello world"
    prov = rec["provenance"]
    assert prov["source_packet_id"] == pid
    assert prov["source_sha256"] == hashlib.sha256(_AUDIO).hexdigest()
    assert prov["model"] == "small"
    assert prov["speech_gate"].startswith("faster-whisper")
    # provenance honesty: model_digest is not a repo id wearing a digest's name
    assert prov["model_digest"] is None
    assert prov["model_repo_id"] == "Systran/faster-whisper-small"


def test_no_speech_records_posture_without_cues(tmp_path):
    root = _lake(tmp_path)

    def fake_transcribe(_audio_path):
        return "no_speech", [], _MODEL_INFO

    code, msg = write_asr_transcript(
        video_id="abcdefghijk", audio_bytes=_AUDIO, audio_ext="webm",
        transcribe_fn=fake_transcribe, data_root=root,
    )
    assert code == 0
    rec = _load_derived(root, msg)
    assert rec["posture"] == "no_speech"
    assert rec["cue_count"] == 0
    assert rec["cues"] == []
    # audio still captured
    pid = _packet_id_from_msg(msg)
    assert (root.path / "raw" / pid / "manifest.json").is_file()


def test_invalid_video_id_refused(tmp_path):
    root = _lake(tmp_path)
    code, msg = write_asr_transcript(
        video_id="../../evil", audio_bytes=_AUDIO, audio_ext="webm",
        transcribe_fn=lambda p: ("transcribed", [], _MODEL_INFO), data_root=root,
    )
    assert code == 5
    assert "invalid video id" in msg


def test_empty_audio_refused(tmp_path):
    root = _lake(tmp_path)
    code, msg = write_asr_transcript(
        video_id="abcdefghijk", audio_bytes=b"", audio_ext="webm",
        transcribe_fn=lambda p: ("transcribed", [], _MODEL_INFO), data_root=root,
    )
    assert code == 6
    assert "no audio" in msg


def test_transcriber_exception_records_failed_posture(tmp_path):
    # review F1: a transcriber raise must still produce a `failed` derived record, not just raw accumulation.
    root = _lake(tmp_path)

    def boom(_audio_path):
        raise RuntimeError("model load failed")

    code, msg = write_asr_transcript(
        video_id="abcdefghijk", audio_bytes=_AUDIO, audio_ext="webm",
        transcribe_fn=boom, data_root=root,
    )
    assert code == 0
    rec = _load_derived(root, msg)
    assert rec["posture"] == "failed"
    assert rec["cue_count"] == 0
    assert rec["cues"] == []
    assert "failure_message" in rec["provenance"]
    # the raw audio packet was still captured
    assert (root.path / "raw" / _packet_id_from_msg(msg) / "manifest.json").is_file()


def test_transcribed_without_cues_normalizes_to_no_speech(tmp_path):
    # posture/cue consistency: `transcribed` with no cues is not a valid record -> no_speech.
    root = _lake(tmp_path)
    code, msg = write_asr_transcript(
        video_id="abcdefghijk", audio_bytes=_AUDIO, audio_ext="webm",
        transcribe_fn=lambda p: ("transcribed", [], _MODEL_INFO), data_root=root,
    )
    assert code == 0
    assert _load_derived(root, msg)["posture"] == "no_speech"


def test_rerun_is_a_new_observation_not_an_overwrite(tmp_path):
    # honest rerun semantics (review F2): each run mints a new audio packet; no append-only refusal.
    root = _lake(tmp_path)

    def t(_audio_path):
        return "transcribed", [{"start_ms": 0, "end_ms": 1, "text": "x"}], _MODEL_INFO

    c1, _ = write_asr_transcript(video_id="abcdefghijk", audio_bytes=_AUDIO, audio_ext="webm", transcribe_fn=t, data_root=root)
    c2, _ = write_asr_transcript(video_id="abcdefghijk", audio_bytes=_AUDIO, audio_ext="webm", transcribe_fn=t, data_root=root)
    assert c1 == 0 and c2 == 0
    assert len(list((root.path / "raw").iterdir())) == 2  # two distinct audio packets, not a refusal


def test_download_audio_rejects_bad_id_pre_network():
    # review F4: id validated BEFORE building a URL / touching the network.
    from source_capture.transcript.audio_asr import download_audio

    assert download_audio("../etc/passwd") is None
