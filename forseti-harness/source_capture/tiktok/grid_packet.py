"""Admit an already-captured TikTok creator grid window as a Bronze packet.

The packet is intentionally grid-only: it preserves the compact source-visible
rows used for daily metric monitoring and carries no comments, subtitles, media,
or deep-capture claim.  The supplied JSON bytes are preserved byte-for-byte.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlparse

from source_capture.models import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
)
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map

TIKTOK_GRID_PACKET_SOURCE_SURFACE = "tiktok_creator_grid_window"
TIKTOK_GRID_WINDOW_JSON_NAME = "tiktok_grid_window.json"
TIKTOK_GRID_PACKET_POLICY_VERSION = "tiktok_grid_packet_admission_v0"

TIKTOK_GRID_PACKET_NON_CLAIMS = (
    "not a deep capture or comment-body capture",
    "not transcript, subtitle, or media preservation",
    "not Creator Registry mutation or cross-platform identity",
    "not evidence that missing metrics are zero",
    "not a prediction of virality or creative causality",
)


def write_tiktok_grid_packet(
    *,
    grid_window_json: bytes,
    output_directory: Path | None = None,
    data_root: Any = None,
    observed_at_utc: str | None = None,
    decision_question: str = "What source-visible metrics are present on this TikTok creator grid?",
) -> tuple[int, str]:
    """Validate and preserve one grid-window artifact as a SourceCapturePacket."""
    grid = _load_grid(grid_window_json)
    creator_handle = _required_text(grid.get("creator_handle"), "creator_handle").lstrip("@")
    items = grid.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("TikTok grid window requires a non-empty items list")
    if grid.get("complete") is not True:
        raise ValueError("TikTok grid window must indicate complete=true")
    if grid.get("window_size") != len(items):
        raise ValueError("TikTok grid window window_size must equal items length")

    video_ids: list[str] = []
    for index, raw_item in enumerate(items):
        if not isinstance(raw_item, Mapping):
            raise ValueError(f"TikTok grid item {index} must be an object")
        video_id = _required_text(raw_item.get("video_id"), f"items[{index}].video_id")
        video_url = _required_text(raw_item.get("video_url"), f"items[{index}].video_url")
        parsed = urlparse(video_url)
        host = parsed.hostname.lower() if parsed.hostname else ""
        expected_path = f"/@{creator_handle}/video/{video_id}".lower()
        if (
            parsed.scheme not in {"http", "https"}
            or not (host == "tiktok.com" or host.endswith(".tiktok.com"))
            or parsed.path.rstrip("/").lower() != expected_path
        ):
            raise ValueError(
                f"TikTok grid item {index} URL does not bind creator_handle and video_id "
                "on a canonical TikTok host"
            )
        video_ids.append(video_id)
    if len(set(video_ids)) != len(video_ids):
        raise ValueError("TikTok grid window contains duplicate video_id values")

    receipt = grid.get("collection_receipt")
    receipt_time = receipt.get("capture_timestamp") if isinstance(receipt, Mapping) else None
    if receipt_time is not None:
        # The artifact's own collection receipt is the source-backed capture time;
        # an explicit observed_at_utc may only confirm it, never replace it.
        observed_at = _required_utc(receipt_time)
        if observed_at_utc and _required_utc(observed_at_utc) != observed_at:
            raise ValueError(
                "TikTok grid observed_at_utc conflicts with the artifact's "
                "collection_receipt capture_timestamp"
            )
    else:
        observed_at = _required_utc(observed_at_utc)
    profile_url = f"https://www.tiktok.com/@{creator_handle}"
    staged_artifacts = [(TIKTOK_GRID_WINDOW_JSON_NAME, grid_window_json)]
    file_ids = staged_file_id_map(staged_artifacts)
    timing = PacketTiming(
        source_publication_or_event=not_applicable(
            "a creator grid is a capture-time state, not one publication event"
        ),
        source_edit_or_version=not_applicable(
            "TikTok grid state exposes no source edit/version identifier"
        ),
        capture_time=known_fact(observed_at),
        recapture_time=not_applicable("no prior grid packet was supplied to this admission"),
        cutoff_posture=not_applicable("cutoff posture does not apply to current grid monitoring"),
    )
    access = known_fact(
        "sanitized creator grid-window rows captured from the source-visible profile surface"
    )
    archive = not_attempted("grid monitoring does not query archive/history services")
    media = not_attempted("grid monitoring preserves metrics and content identifiers only")
    recapture = not_applicable("no prior grid packet was supplied to this admission")
    result = stage_and_write_packet(
        output_directory=output_directory,
        data_root=data_root,
        staged_artifacts=staged_artifacts,
        source_slices=[
            SourceCaptureSlice(
                slice_id="tiktok_creator_grid_01",
                locator=known_fact(profile_url),
                timing=timing,
                access_posture=access,
                archive_history_posture=archive,
                media_modality_posture=media,
                re_capture_relationship=recapture,
                limitations=list(TIKTOK_GRID_PACKET_NON_CLAIMS),
                warning_notes=[],
                preserved_file_ids=[file_ids[TIKTOK_GRID_WINDOW_JSON_NAME]],
            )
        ],
        source_family="tiktok",
        source_surface=TIKTOK_GRID_PACKET_SOURCE_SURFACE,
        source_locator=known_fact(profile_url),
        decision_question=decision_question,
        capture_context=(
            "TikTok grid-only admission from a validated sanitized grid artifact; "
            "no browser launch or deep capture in this writer"
        ),
        actor_audience_context=not_applicable(
            "public creator/content object metrics only; no audience or person modeling"
        ),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="tiktok_grid_packet_cli_operator",
        session_identity=None,
        visible_mode_changes=[TIKTOK_GRID_PACKET_POLICY_VERSION],
        source_publication_or_event=timing.source_publication_or_event,
        source_edit_or_version=timing.source_edit_or_version,
        cutoff_posture=timing.cutoff_posture,
        recapture_time=timing.recapture_time,
        access_posture=access,
        archive_history_posture=archive,
        media_modality_posture=media,
        re_capture_relationship=recapture,
        warnings=[],
        limitations=list(TIKTOK_GRID_PACKET_NON_CLAIMS),
        receipt_summary=(
            f"TikTok grid packet for @{creator_handle}: rows={len(items)}, "
            f"observed_at={observed_at}."
        ),
        receipt_non_claims=list(TIKTOK_GRID_PACKET_NON_CLAIMS),
    )
    return 0, result.output_directory


def _load_grid(raw: bytes) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"TikTok grid window is not valid UTF-8 JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("TikTok grid window must be a JSON object")
    return value


def _required_text(value: object, field: str) -> str:
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        raise ValueError(f"TikTok grid window {field} is missing or invalid")
    text = str(value).strip()
    if not text:
        raise ValueError(f"TikTok grid window {field} is blank")
    return text


def _required_utc(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            "TikTok grid admission requires a source-backed UTC capture time "
            "(collection_receipt.capture_timestamp, or observed_at_utc when the receipt lacks one)"
        )
    text = value.strip()
    parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("TikTok grid observed_at_utc must include a UTC offset")
    if parsed.utcoffset().total_seconds() != 0:
        raise ValueError("TikTok grid observed_at_utc must be UTC")
    return parsed.isoformat().replace("+00:00", "Z")


__all__ = [
    "TIKTOK_GRID_PACKET_POLICY_VERSION",
    "TIKTOK_GRID_PACKET_SOURCE_SURFACE",
    "TIKTOK_GRID_WINDOW_JSON_NAME",
    "write_tiktok_grid_packet",
]
