"""Instagram Reels audio capture + transcript_asr derived record (IG source_family).

The IG analogue of the YouTube `asr_packet` path. IG Reels expose NO caption API, so ASR is
the ONLY transcript route: download the Reel's bestaudio anonymously (yt-dlp, no login / no
proxy), stage it as a SourceCapturePacket (audio = raw_stored_bytes PreservedFile), then write
the transcript as a DERIVED RECORD at derived/<audio-packet_id>/transcript_asr/<record_id> via
DataLakeRoot.append_record (append-only). Generated transcript bytes live ONLY under derived/.

This MIRRORS the YouTube pattern by composition — it reuses the source-family-agnostic primitives
(`stage_and_write_packet`, `staged_file_id_map`, `SourceCaptureSlice`, `DataLakeRoot.append_record`,
and the agnostic `audio_asr.transcribe_audio` as the injected transcriber). It does NOT import or
edit any YouTube-lane module: `asr_packet.write_asr_transcript` is YouTube-coupled (11-char id
regex, youtube.com canonical URL, platform/source_family=youtube), so IG gets its own writer.

The transcriber is INJECTED (`transcribe_fn(audio_path)`), so this module needs no
faster-whisper import and the writer is unit-testable from canned audio bytes + a fake
transcriber. yt-dlp is invoked as a subprocess (`python -m yt_dlp`), never imported, so the
module stays import-light. Data-lake mode only. Public data only, anonymous.

Capture posture (proven by the 2026-06-25 audio-acquisition probe): a publicly-viewable Reel's
bestaudio is fetchable anonymously; an audience-restricted Reel ("can't be seen by certain
audiences") is a TYPED SKIP, never a hard failure.

Spec: forseti/product/spines/capture/core/source_families/social_media/instagram/
ig_reels_transcript_product_extraction_spec_v0.md (IG delta over the YouTube CE1-CE10).
"""
from __future__ import annotations

import datetime
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlparse

from source_capture import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
)
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map

# IG shortcodes are base64url handles (the probe targets were 11 chars: DZ69knlsDb1, DaALKgOsWn0).
# Bounded + URL/path-safe; NOT the YouTube 11-char-exact regex.
_IG_SHORTCODE = re.compile(r"[A-Za-z0-9_-]{5,32}")
_IG_PATH_KINDS = {"reel", "reels", "p", "tv"}  # "reels" = the plural share-URL form IG hands out
_AUDIO_EXT = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,15}")
_MAX_MODEL_TOKEN = 96

# transcribe_fn(audio_path) -> (posture, cues, model_info)
TranscribeFn = Callable[[str], "tuple[str, list[dict], dict]"]

IG_REELS_AUDIO_NON_CLAIMS = [
    "not Cleaning implementation (cue dedup/readable transform is downstream)",
    "not Judgment scoring (no sentiment, verdict, or commentary decision)",
    "the ASR transcript is a derived record, not source content; it is machine-generated text",
    "not login/session capture, not proxy/anti-detect; anonymous public capture only",
    "not media/video preservation beyond the audio asset needed for ASR",
]


@dataclass(frozen=True)
class IgAudioFetch:
    """Result of an anonymous Reel-audio fetch. `status` is a TYPED posture so the runner can
    skip an access-gated Reel honestly instead of treating it as a generic failure.

    status:
      - "ok"           -> audio_bytes/audio_ext present
      - "access_gated" -> audience-restricted / login-walled (out of anonymous scope; typed skip)
      - "unavailable"  -> not found / not a video / transient fetch failure
    """

    status: str
    audio_bytes: bytes | None
    audio_ext: str | None
    detail: str


def ig_shortcode_from_url(url_or_shortcode: str) -> str | None:
    """Extract the IG shortcode from a /reel/, /reels/, /p/, or /tv/ URL, or pass through a bare shortcode."""
    target = (url_or_shortcode or "").strip()
    if not target:
        return None
    if _IG_SHORTCODE.fullmatch(target):
        return target

    parse_target = target
    if "://" not in parse_target and parse_target.lower().startswith(
        ("instagram.com/", "www.instagram.com/", "m.instagram.com/")
    ):
        parse_target = f"https://{parse_target}"
    parsed = urlparse(parse_target)
    host = (parsed.hostname or "").lower()
    if host != "instagram.com" and not host.endswith(".instagram.com"):
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) != 2 or parts[0] not in _IG_PATH_KINDS:
        return None
    shortcode = parts[1]
    return shortcode if _IG_SHORTCODE.fullmatch(shortcode) else None


def _safe_audio_ext(audio_ext: str | None) -> str | None:
    ext = (audio_ext or "").lstrip(".")
    return ext if _AUDIO_EXT.fullmatch(ext) else None


def _bounded_model_token(model: object) -> str:
    token = re.sub(r"[^A-Za-z0-9_-]", "-", str(model or "asr"))
    return (token or "asr")[:_MAX_MODEL_TOKEN]


def classify_ig_fetch_failure(stderr: str) -> str:
    """Map yt-dlp stderr to a typed fetch status. Audience-restricted / login-walled -> a typed
    skip (`access_gated`); everything else -> `unavailable`. Pure (offline-testable)."""
    low = (stderr or "").lower()
    gated_markers = (
        "isn't available to everyone",
        "not available to everyone",
        "certain audiences",              # "can't be seen by certain audiences"
        "login required",
        "requires login",
        "log in",
        "sign in",
        "this account is private",
        "this video is private",
        "content is private",
        "media is private",
        "you need to log in",
    )
    if any(marker in low for marker in gated_markers):
        return "access_gated"
    return "unavailable"


def download_ig_reel_audio(shortcode: str) -> IgAudioFetch:
    """Download a public Reel's bestaudio ANONYMOUSLY via yt-dlp (no login, no proxy). Returns a
    typed `IgAudioFetch`. Validates the shortcode BEFORE building any URL / touching the network
    (pre-network guard, matching the YouTube audio path)."""
    if not _IG_SHORTCODE.fullmatch(shortcode or ""):
        return IgAudioFetch("unavailable", None, None, "invalid shortcode (pre-network guard)")
    url = f"https://www.instagram.com/reel/{shortcode}/"
    with tempfile.TemporaryDirectory(prefix="orca_ig_audio_") as tmp:
        out_tmpl = os.path.join(tmp, "%(id)s.%(ext)s")
        # bestaudio/best, anonymous (no cookies, no proxy) — the route the 2026-06-25 probe proved.
        proc = subprocess.run(
            [sys.executable, "-m", "yt_dlp", "-f", "ba/b", "-o", out_tmpl, url],
            capture_output=True, text=True,
        )
        files = [hit for hit in glob.glob(os.path.join(tmp, "*")) if os.path.isfile(hit)]
        if proc.returncode != 0 or not files:
            return IgAudioFetch(
                classify_ig_fetch_failure(proc.stderr), None, None, (proc.stderr or "").strip()[:200]
            )
        path = max(files, key=os.path.getsize)
        ext = _safe_audio_ext(os.path.splitext(path)[1].lstrip(".") or "bin")
        if ext is None:
            return IgAudioFetch("unavailable", None, None, "invalid audio extension from yt-dlp")
        with open(path, "rb") as handle:
            return IgAudioFetch("ok", handle.read(), ext, "ok")


def write_ig_reels_asr_transcript(
    *,
    shortcode: str,
    audio_bytes: bytes,
    audio_ext: str,
    transcribe_fn: TranscribeFn,
    data_root,
    identity_extra: dict | None = None,
    now_iso: str | None = None,
) -> tuple[int, str]:
    """Capture the Reel-audio packet (source_family=instagram_creator, source_surface=ig_reels_audio),
    run the injected transcriber, and write the transcript_asr derived record. IG identity only;
    no YouTube coupling."""
    if not _IG_SHORTCODE.fullmatch(shortcode or ""):
        return 5, f"refusing: invalid ig shortcode {shortcode!r}"
    safe_ext = _safe_audio_ext(audio_ext)
    if safe_ext is None:
        return 5, f"refusing: invalid audio extension {audio_ext!r}"
    if not audio_bytes:
        return 6, "refusing: no audio bytes"

    ts = now_iso or (datetime.datetime.utcnow().isoformat() + "Z")
    audio_sha = hashlib.sha256(audio_bytes).hexdigest()
    canonical = f"https://www.instagram.com/reel/{shortcode}/"
    identity = {
        **(identity_extra or {}),
        "platform": "instagram",
        "platform_shortcode": shortcode,
        "canonical_url": canonical,
        "capture_timestamp": ts,
    }
    audio_name = f"{shortcode}.audio.{safe_ext}"
    artifacts: list[tuple[str, bytes]] = [
        (audio_name, audio_bytes),
        ("capture_metadata.json", (json.dumps(identity, indent=2, sort_keys=True) + "\n").encode("utf-8")),
    ]
    file_ids = staged_file_id_map(artifacts)

    timing = PacketTiming(
        source_publication_or_event=not_attempted("publish timing not fetched in the IG audio/ASR path"),
        source_edit_or_version=not_applicable("audio carries no source edit/version timing"),
        capture_time=known_fact(ts),
        recapture_time=not_applicable("no prior audio capture supplied"),
        cutoff_posture=not_applicable("cutoff posture does not apply to an audio capture"),
    )
    access = known_fact(f"bestaudio fetched ({len(audio_bytes)} bytes) via yt-dlp (anonymous, no login/proxy)")
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
        source_family="instagram_creator",
        source_surface="ig_reels_audio",
        source_locator=known_fact(canonical),
        decision_question="Capture Instagram Reel audio for an ASR transcript (IG transcript spine v0).",
        capture_context="Instagram Reel bestaudio capture via yt-dlp (anonymous) for the ASR transcript path",
        actor_audience_context=not_applicable("anonymous public audio capture; no actor/audience modeling"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="ig_reels_asr_cli_operator",
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
        receipt_summary=f"Instagram Reel audio packet for {shortcode}: {len(audio_bytes)} raw bytes (ASR source).",
        receipt_non_claims=IG_REELS_AUDIO_NON_CLAIMS,
    )
    audio_packet_id = result.packet.packet_id

    # Run the injected transcriber on a temp file (Windows-safe: write, close, transcribe, unlink).
    fd, tmp_audio = tempfile.mkstemp(suffix=f".{safe_ext}", prefix="orca_ig_asr_")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(audio_bytes)
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
        "video_id": shortcode,            # IG shortcode carried in video_id (reused field; the
        "shortcode": shortcode,           # extractor/runner key on video_id, the schema is agnostic)
        "platform": "instagram",
        "posture": posture,               # transcribed | no_speech | failed
        "cue_count": len(cues),
        "cues": cues,                     # each: {start_ms, end_ms, text}; empty unless transcribed
        "provenance": {
            **model_info,
            "source_packet_id": audio_packet_id,
            "source_file_id": file_ids[audio_name],
            "source_sha256": audio_sha,
        },
        "retrieval_time_utc": ts,
    }
    model_token = _bounded_model_token(model_info.get("model", "asr"))
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
