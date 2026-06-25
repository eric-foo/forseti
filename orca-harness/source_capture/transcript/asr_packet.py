"""Audio capture packet + transcript_asr derived record (network-free, ASR-free core).

Stages the RAW audio as a SourceCapturePacket (audio = raw_stored_bytes PreservedFile), then
writes the transcript as a DERIVED RECORD at derived/<audio-packet_id>/transcript_asr/<record_id>
via DataLakeRoot.append_record (append-only). Generated transcript bytes live ONLY under derived/
— never a capture PreservedFile (no laundering, no manifest change). The transcriber is INJECTED
(`transcribe_fn(audio_path)`), so this module needs no faster-whisper/yt-dlp import and is
unit-testable from canned audio bytes + a fake transcriber. Data-lake mode only (append_record
is a DataLakeRoot method).
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import tempfile
from typing import Callable

from source_capture import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
)
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map

_VIDEO_ID = re.compile(r"[A-Za-z0-9_-]{11}")

AUDIO_NON_CLAIMS = [
    "not Cleaning implementation (cue dedup/readable transform is downstream)",
    "not Judgment scoring (no sentiment, verdict, or commentary decision)",
    "the ASR transcript is a derived record, not source content; it is machine-generated text",
    "not browser automation, not proxy/session injection",
]

# transcribe_fn(audio_path) -> (posture, cues, model_info)
TranscribeFn = Callable[[str], "tuple[str, list[dict], dict]"]


def write_asr_transcript(
    *,
    video_id: str,
    audio_bytes: bytes,
    audio_ext: str,
    transcribe_fn: TranscribeFn,
    data_root,
    identity_extra: dict | None = None,
    now_iso: str | None = None,
) -> tuple[int, str]:
    """Capture the audio packet, run the injected transcriber, write the derived record."""
    if not _VIDEO_ID.fullmatch(video_id or ""):
        return 5, f"refusing: invalid video id {video_id!r}"
    if not audio_bytes:
        return 6, "refusing: no audio bytes"

    ts = now_iso or (datetime.datetime.utcnow().isoformat() + "Z")
    audio_sha = hashlib.sha256(audio_bytes).hexdigest()
    canonical = f"https://www.youtube.com/watch?v={video_id}"
    identity = {
        "platform": "youtube",
        "platform_video_id": video_id,
        "canonical_url": canonical,
        "capture_timestamp": ts,
        **(identity_extra or {}),
    }
    audio_name = f"{video_id}.audio.{audio_ext}"
    artifacts: list[tuple[str, bytes]] = [
        (audio_name, audio_bytes),
        ("capture_metadata.json", (json.dumps(identity, indent=2, sort_keys=True) + "\n").encode("utf-8")),
    ]
    file_ids = staged_file_id_map(artifacts)

    timing = PacketTiming(
        source_publication_or_event=not_attempted("publish timing not fetched in the audio/ASR path; available via the caption/RSS path"),
        source_edit_or_version=not_applicable("audio carries no source edit/version timing"),
        capture_time=known_fact(ts),
        recapture_time=not_applicable("no prior audio capture supplied"),
        cutoff_posture=not_applicable("cutoff posture does not apply to an audio capture"),
    )
    access = known_fact(f"bestaudio fetched ({len(audio_bytes)} bytes) via yt-dlp android_vr")
    media = known_fact("audio asset preserved (bestaudio)")
    archive = not_attempted("audio capture does not query archive/history services")
    recap = not_applicable("no prior audio capture packet supplied")

    result = stage_and_write_packet(
        data_root=data_root,
        staged_artifacts=artifacts,
        source_slices=[
            SourceCaptureSlice(
                slice_id="slice_01",
                locator=known_fact(canonical),
                timing=timing,
                access_posture=access,
                archive_history_posture=archive,
                media_modality_posture=media,
                re_capture_relationship=recap,
                preserved_file_ids=[file_ids[audio_name], file_ids["capture_metadata.json"]],
            )
        ],
        source_family="youtube",
        source_surface="youtube_audio",
        source_locator=known_fact(canonical),
        decision_question="Capture YouTube audio for an ASR transcript (transcript spine v0).",
        capture_context="YouTube bestaudio capture via yt-dlp (android_vr) for the ASR fallback",
        actor_audience_context=not_applicable("anonymous public audio capture; no actor/audience modeling"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="youtube_asr_cli_operator",
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
        limitations=[
            "the ASR transcript is a derived record (derived/<packet_id>/transcript_asr/), never a PreservedFile",
        ],
        receipt_summary=f"YouTube audio packet for {video_id}: {len(audio_bytes)} raw bytes (ASR source).",
        receipt_non_claims=AUDIO_NON_CLAIMS,
    )
    audio_packet_id = result.packet.packet_id

    # Run the injected transcriber on a temp file (Windows-safe: write, close, transcribe, unlink).
    fd, tmp_audio = tempfile.mkstemp(suffix=f".{audio_ext}", prefix="orca_asr_")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(audio_bytes)
        try:
            posture, cues, model_info = transcribe_fn(tmp_audio)
        except Exception as exc:  # noqa: BLE001 - an injected transcriber raise still records a `failed` posture
            posture, cues, model_info = "failed", [], {
                "tool": "faster-whisper",
                "model_digest": None,
                "model_digest_basis": "transcriber raised before producing provenance",
                "failure_type": type(exc).__name__,
                "failure_message": str(exc)[:200],
            }
    finally:
        try:
            os.unlink(tmp_audio)
        except OSError:
            pass

    # Posture/cue consistency + never-fabricate: only `transcribed` carries cues; unknown -> failed.
    if posture not in {"transcribed", "no_speech", "failed"}:
        posture = "failed"
    if posture == "transcribed" and not cues:
        posture = "no_speech"
    if posture != "transcribed":
        cues = []

    record = {
        "video_id": video_id,
        "platform": "youtube",
        "posture": posture,                      # transcribed | no_speech | failed
        "cue_count": len(cues),
        "cues": cues,                            # each: {start_ms, end_ms, text}; empty unless transcribed
        "provenance": {
            "source_packet_id": audio_packet_id,
            "source_file_id": file_ids[audio_name],
            "source_sha256": audio_sha,
            **model_info,                        # tool/version, model/digest, compute_type, decode_params, speech_gate
        },
        "retrieval_time_utc": ts,
    }
    # record_id is deterministic PER audio packet (model + audio sha). NOTE: each run mints a NEW
    # audio packet (fresh packet_id), so a normal rerun is a new observation, not an append-only
    # refusal; the refusal only fires when the SAME audio packet is re-derived with the same model.
    model_token = re.sub(r"[^A-Za-z0-9_-]", "-", str(model_info.get("model", "asr")))
    record_id = f"asr_{model_token}__{audio_sha[:16]}"
    written = data_root.append_record(
        subtree="derived",
        raw_anchor=audio_packet_id,
        lane="transcript_asr",
        record_id=record_id,
        data=(json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
    )
    rel = written.relative_to(data_root.path.resolve()).as_posix()
    return 0, f"{rel} [{posture}, {len(cues)} cues]"
