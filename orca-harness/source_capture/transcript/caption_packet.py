"""Build a SourceCapturePacket from a fetched caption (Capture layer; network-free).

Takes a CaptionFetch (produced by a per-platform fetcher) and stages the RAW caption
bytes + capture metadata into a contract-compliant SourceCapturePacket via the shared
assembly helper. The readable transcript is a downstream Cleaning transform; the
NON-AUTHORITATIVE flat-text view is written BESIDE the packet (output-dir mode only),
never as a PreservedFile. No ASR-derived bytes here (gated on the FileDerivation
manifest extension). This module performs no network I/O — it is unit-testable from a
canned CaptionFetch.
"""
from __future__ import annotations

import datetime
import json
import re
from pathlib import Path

from source_capture import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map
from source_capture.transcript.youtube_captions import CaptionFetch

CAPTION_NON_CLAIMS = [
    "not a clean or readable transcript (raw caption json3 only)",
    "not ASR (no model-generated text; captions are YouTube-provided)",
    "not Cleaning implementation (cue dedup/normalization is downstream)",
    "not Judgment scoring (no sentiment, verdict, or commentary decision)",
    "the flat-text view beside the packet is NON-AUTHORITATIVE and regenerable",
    "not media preservation, not browser automation, not proxy/session injection",
]


def write_caption_packet(
    cap: CaptionFetch,
    *,
    output_directory: Path | None = None,
    data_root=None,
    decision_question: str,
    now_iso: str | None = None,
) -> tuple[int, str]:
    """Stage a found CaptionFetch into a SourceCapturePacket. Returns (exit_code, message)."""
    if not cap.found:
        return 4, f"no caption for {cap.video_id}: {cap.note} (ASR fallback required)"
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", cap.video_id or ""):
        # Belt-and-suspenders: the fetcher already validates, but never build filenames/paths
        # from an unvalidated id (path-traversal guard for the side-file write).
        return 5, f"refusing to build packet: invalid video id {cap.video_id!r}"

    capture_ts = now_iso or (datetime.datetime.utcnow().isoformat() + "Z")
    canonical_url = f"https://www.youtube.com/watch?v={cap.video_id}"
    identity = {
        "platform": "youtube",
        "platform_video_id": cap.video_id,
        "canonical_url": canonical_url,
        "title": cap.title,
        "channel_id": cap.channel_id,
        "publish_date_iso": cap.publish_date_iso,
        "duration_s": cap.duration_s,
        "caption_lang": cap.lang,
        "caption_kind": cap.caption_kind,
        "original_language_assumed": cap.original_language_assumed,
        "cue_count": cap.cue_count,
        "tooling": cap.tooling,
        "capture_timestamp": capture_ts,
    }
    captions_name = f"{cap.video_id}.captions.{cap.lang}.json3"
    artifacts: list[tuple[str, bytes]] = [
        (captions_name, cap.json3_bytes),
        ("capture_metadata.json", (json.dumps(identity, indent=2, sort_keys=True) + "\n").encode("utf-8")),
    ]
    file_ids = staged_file_id_map(artifacts)

    pub = known_fact(cap.publish_date_iso) if cap.publish_date_iso else unknown_with_reason(
        "yt-dlp did not expose an upload date for this video"
    )
    timing = PacketTiming(
        source_publication_or_event=pub,
        source_edit_or_version=not_applicable("captions carry no source edit/version timing"),
        capture_time=known_fact(capture_ts),
        recapture_time=not_applicable("no prior caption capture was supplied"),
        cutoff_posture=not_applicable("cutoff posture does not apply to a caption capture"),
    )
    access_posture = known_fact(
        f"caption track fetched: lang={cap.lang} kind={cap.caption_kind} cues={cap.cue_count}"
    )
    archive_posture = not_attempted("caption capture does not query archive/history services")
    media_posture = not_attempted("caption capture preserves caption text only; no media assets fetched")
    recapture_posture = not_applicable("no prior caption capture packet supplied")

    result = stage_and_write_packet(
        output_directory=output_directory,
        data_root=data_root,
        staged_artifacts=artifacts,
        source_slices=[
            SourceCaptureSlice(
                slice_id="slice_01",
                locator=known_fact(canonical_url),
                timing=timing,
                access_posture=access_posture,
                archive_history_posture=archive_posture,
                media_modality_posture=media_posture,
                re_capture_relationship=recapture_posture,
                preserved_file_ids=[file_ids[captions_name], file_ids["capture_metadata.json"]],
            )
        ],
        source_family="youtube",
        source_surface="youtube_captions",
        source_locator=known_fact(canonical_url),
        decision_question=decision_question,
        capture_context="YouTube public caption capture via yt-dlp (default token-free client) for the transcript spine",
        actor_audience_context=not_applicable("anonymous public caption capture; no actor/audience modeling"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="youtube_caption_cli_operator",
        session_identity=None,
        visible_mode_changes=[],
        source_publication_or_event=timing.source_publication_or_event,
        source_edit_or_version=timing.source_edit_or_version,
        cutoff_posture=timing.cutoff_posture,
        recapture_time=timing.recapture_time,
        access_posture=access_posture,
        archive_history_posture=archive_posture,
        media_modality_posture=media_posture,
        re_capture_relationship=recapture_posture,
        warnings=[],
        limitations=[
            "video media not preserved (caption text only)",
            "flat-text view beside the packet is non-authoritative; cue/span ids in the preserved json3 are the evidence anchor (downstream Cleaning)",
        ],
        receipt_summary=(
            f"YouTube caption packet for {cap.video_id}: {cap.lang}/{cap.caption_kind}, "
            f"{cap.cue_count} cues, {len(cap.json3_bytes)} raw json3 bytes preserved."
        ),
        receipt_non_claims=CAPTION_NON_CLAIMS,
    )

    if output_directory is not None and cap.flat_text:
        view = Path(result.output_directory).parent / f"{cap.video_id}_transcript_view_NONAUTHORITATIVE.txt"
        view.write_text(cap.flat_text, encoding="utf-8")

    return 0, result.output_directory
