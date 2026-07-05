"""Audio capture packet + transcript_asr derived record (network-free, ASR-free core).

Stages the RAW audio as a SourceCapturePacket (audio = raw_stored_bytes PreservedFile), then
writes the transcript as a DERIVED RECORD at derived/<audio-packet_id>/transcript_asr/<record_id>
via DataLakeRoot.append_record_set (append-only, with a completion marker in transcript_asr__set
that commits the transcript's derivation-time content sha256). Generated transcript bytes live ONLY
under derived/ — never a capture PreservedFile (no laundering, no manifest change). The transcriber
is INJECTED (`transcribe_fn(audio_path)`), so this module needs no faster-whisper/yt-dlp import and
is unit-testable from canned audio bytes + a fake transcriber. Data-lake mode only
(append_record_set is a DataLakeRoot method).
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

# Record-SHAPE schema token for transcript_asr derived records (V4: vault-versioned;
# closes the weak-envelope residual). Shared by the YT writer here and the IG writer
# in ig_reels_audio_packet.py (same lane, same record family). Added additively:
# earlier committed records lack the field and read as pre-token vintage; no
# derivation-policy token was bumped, so no committed packet re-surfaces on cadence.
TRANSCRIPT_ASR_RECORD_SCHEMA_VERSION = "transcript_asr_record_v0"

AUDIO_NON_CLAIMS = [
    "not Cleaning implementation (cue dedup/readable transform is downstream)",
    "not Judgment scoring (no sentiment, verdict, or commentary decision)",
    "the ASR transcript is a derived record, not source content; it is machine-generated text",
    "not browser automation, not proxy/session injection",
]

# transcribe_fn(audio_path) -> (posture, cues, model_info)
TranscribeFn = Callable[[str], "tuple[str, list[dict], dict]"]


def asr_record_id(model: object, audio_sha256: str) -> str:
    """Deterministic transcript record id for one audio packet + ASR model policy.
    The model token embeds the policy in the id, so a policy change never collides
    with an existing record (append-only refusal fires only for the SAME packet
    re-derived under the SAME model)."""
    model_token = re.sub(r"[^A-Za-z0-9_-]", "-", str(model or "asr"))
    return f"asr_{model_token}__{audio_sha256[:16]}"


def _run_transcriber(
    audio_bytes: bytes, audio_ext: str, transcribe_fn: TranscribeFn
) -> tuple[str, list[dict], dict]:
    """Run the injected transcriber on a temp file (Windows-safe: write, close,
    transcribe, unlink) and normalize the posture/cue coupling (never-fabricate:
    only `transcribed` carries cues; unknown postures collapse to `failed`)."""
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

    if posture not in {"transcribed", "no_speech", "failed"}:
        posture = "failed"
    if posture == "transcribed" and not cues:
        posture = "no_speech"
    if posture != "transcribed":
        cues = []
    return posture, cues, model_info


def _append_transcript_record(
    data_root,
    *,
    audio_packet_id: str,
    video_id: str,
    audio_file_id: str,
    audio_sha: str,
    posture: str,
    cues: list[dict],
    model_info: dict,
    ts: str,
) -> tuple[str, str]:
    """Append the transcript_asr derived record SET on the audio anchor and return
    (record_id, record relpath). The completion marker in ``transcript_asr__set``
    commits the derivation-time content sha256."""
    record = {
        "record_schema_version": TRANSCRIPT_ASR_RECORD_SCHEMA_VERSION,
        "video_id": video_id,
        "platform": "youtube",
        "posture": posture,                      # transcribed | no_speech | failed
        "cue_count": len(cues),
        "cues": cues,                            # each: {start_ms, end_ms, text}; empty unless transcribed
        "provenance": {
            "source_packet_id": audio_packet_id,
            "source_file_id": audio_file_id,
            "source_sha256": audio_sha,
            **model_info,                        # tool/version, model/digest, compute_type, decode_params, speech_gate
        },
        "retrieval_time_utc": ts,
    }
    record_id = asr_record_id(model_info.get("model", "asr"), audio_sha)
    record_bytes = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    written = data_root.append_record_set(
        subtree="derived",
        raw_anchor=audio_packet_id,
        record_id=record_id,
        members={"transcript_asr": record_bytes},
        completion_lane="transcript_asr__set",
    )
    rel = written["transcript_asr"].relative_to(data_root.path.resolve()).as_posix()
    return record_id, rel


def _policy_model_mismatch(expected_model: object | None, actual_model: object, audio_sha: str) -> str | None:
    if expected_model is None:
        return None
    expected_record_id = asr_record_id(expected_model, audio_sha)
    actual_record_id = asr_record_id(actual_model, audio_sha)
    if actual_record_id == expected_record_id:
        return None
    return (
        "transcriber model mismatch: "
        f"policy model {expected_model!r} would write {expected_record_id}, "
        f"but transcriber reported {actual_model!r} ({actual_record_id})"
    )


def transcribe_committed_audio_packet(
    data_root,
    *,
    packet_id: str,
    transcribe_fn: TranscribeFn,
    expected_model: object | None = None,
    now_iso: str | None = None,
) -> dict:
    """Derive the transcript_asr record for an ALREADY COMMITTED YouTube audio packet
    (the catch-up half: no capture, no network — verified by-key read of the audio
    bytes, injected transcriber, derived record on the EXISTING anchor).

    Block-don't-burn (deliberate divergence from the capture fusion, which records
    ``failed`` postures safely because every capture run mints a fresh packet): a
    failed transcription here writes NO record — the deterministic model+audio
    record id is append-only, and committing an environment failure would
    permanently block retry under the same policy. The caller surfaces the failure
    and the packet re-surfaces. Raises on a packet that is not a YouTube audio
    packet shape (missing audio / capture_metadata / video id).
    """
    loaded = data_root.load_raw_packet(packet_id)
    preserved = loaded.manifest.get("preserved_files") or []
    audio_entry = next(
        (pf for pf in preserved if ".audio." in str(pf.get("relative_packet_path", ""))), None
    )
    meta_entry = next(
        (
            pf
            for pf in preserved
            if str(pf.get("relative_packet_path", "")).endswith("capture_metadata.json")
        ),
        None,
    )
    if audio_entry is None or meta_entry is None:
        raise ValueError(
            f"committed packet {packet_id} is not an audio+metadata capture; refusing to transcribe"
        )
    identity = json.loads(loaded.bodies[meta_entry["file_id"]].decode("utf-8"))
    video_id = identity.get("platform_video_id")
    if not isinstance(video_id, str) or not _VIDEO_ID.fullmatch(video_id):
        raise ValueError(f"committed packet {packet_id} carries no valid platform_video_id")
    audio_bytes = loaded.bodies[audio_entry["file_id"]]
    audio_ext = str(audio_entry["relative_packet_path"]).rsplit(".", 1)[-1] or "bin"
    ts = now_iso or (datetime.datetime.utcnow().isoformat() + "Z")

    posture, cues, model_info = _run_transcriber(audio_bytes, audio_ext, transcribe_fn)
    if posture == "failed":
        return {
            "posture": "failed",
            "failure": str(model_info.get("failure_message") or "transcriber failed")[:200],
        }
    mismatch = _policy_model_mismatch(expected_model, model_info.get("model", "asr"), audio_entry["sha256"])
    if mismatch:
        return {"posture": "failed", "failure": mismatch[:200]}
    record_id, rel = _append_transcript_record(
        data_root,
        audio_packet_id=packet_id,
        video_id=video_id,
        audio_file_id=audio_entry["file_id"],
        audio_sha=audio_entry["sha256"],
        posture=posture,
        cues=cues,
        model_info=model_info,
        ts=ts,
    )
    return {
        "posture": posture,
        "record_id": record_id,
        "record_relpath": rel,
        "cue_count": len(cues),
    }


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

    # Capture fusion keeps recording `failed` postures: each run mints a NEW audio
    # packet, so a failed record never blocks a retry (unlike the committed-packet
    # catch-up path, which must not burn the deterministic record id — see
    # ``transcribe_committed_audio_packet``).
    posture, cues, model_info = _run_transcriber(audio_bytes, audio_ext, transcribe_fn)
    _record_id, rel = _append_transcript_record(
        data_root,
        audio_packet_id=audio_packet_id,
        video_id=video_id,
        audio_file_id=file_ids[audio_name],
        audio_sha=audio_sha,
        posture=posture,
        cues=cues,
        model_info=model_info,
        ts=ts,
    )
    return 0, f"{rel} [{posture}, {len(cues)} cues]"
