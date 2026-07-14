"""Shared real-shape TikTok batch-packet fixtures for current consumer tests."""
from __future__ import annotations

import json
from pathlib import Path

from data_lake.root import DataLakeRoot
from source_capture.models import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
)
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map
from source_capture.tiktok.batch_packet import (
    TIKTOK_BATCH_CAPTURE_JSON_NAME,
    TIKTOK_BATCH_CAPTURE_SCHEMA_VERSION,
    TIKTOK_BATCH_CAPTURE_SURFACE,
    TIKTOK_BATCH_NON_CLAIMS,
)

HANDLE = "funmimonet"
CAPTURE_T1 = "2026-06-30T17:48:37Z"


def _stats(
    play: int, digg: int, comment: int, share: int = 29, collect: int = 163
) -> dict:
    return {
        "playCount": play,
        "diggCount": digg,
        "commentCount": comment,
        "shareCount": share,
        "collectCount": collect,
    }


def _video(
    video_id: str,
    *,
    stats: dict,
    handle: str = HANDLE,
    create_time_utc: str = "2026-06-25T03:00:41Z",
) -> dict:
    return {
        "source_index": 0,
        "video_id": video_id,
        "video_url": f"https://www.tiktok.com/@{handle}/video/{video_id}",
        "url_path": f"/@{handle}/video/{video_id}",
        "status": "completed",
        "create_time_utc": create_time_utc,
        "stats": stats,
        "source_text": {"desc": "fixture", "hashtags": [], "mentions": []},
        "comments": {
            "posture": "not_observed",
            "captured_comment_count": 0,
            "comments": [],
        },
        "subtitles": {
            "posture": "no_subtitleInfos_present",
            "cue_count": 0,
            "cues": [],
        },
        "limitations": list(TIKTOK_BATCH_NON_CLAIMS),
    }


def _commit_batch_packet(
    data_root: DataLakeRoot,
    *,
    videos: list[dict],
    handle: str = HANDLE,
    capture_timestamp: str = CAPTURE_T1,
    operator_category: str = "tiktok_batch_admission_cli_operator",
) -> str:
    profile_url = f"https://www.tiktok.com/@{handle}"
    payload = {
        "capture_schema_version": TIKTOK_BATCH_CAPTURE_SCHEMA_VERSION,
        "platform": "tiktok",
        "source_surface": TIKTOK_BATCH_CAPTURE_SURFACE,
        "creator_handle": handle,
        "creator_profile_url": profile_url,
        "batch_label": "fixture_batch",
        "capture_timestamp": capture_timestamp,
        "videos": videos,
        "non_claims": list(TIKTOK_BATCH_NON_CLAIMS),
    }
    staged = [
        (
            TIKTOK_BATCH_CAPTURE_JSON_NAME,
            json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        )
    ]
    file_ids = staged_file_id_map(staged)
    timing = PacketTiming(
        source_publication_or_event=known_fact("fixture creator batch window"),
        source_edit_or_version=not_applicable("fixture batch packet"),
        capture_time=known_fact(capture_timestamp),
        recapture_time=not_applicable("fixture batch packet"),
        cutoff_posture=not_applicable("fixture batch packet"),
    )
    access = known_fact("sanitized parsed TikTok staging admission (fixture)")
    archive = not_attempted("fixture batch packet does not query archive services")
    media = known_fact("parsed fields preserved; no raw media bytes (fixture)")
    recapture = not_applicable("fixture batch packet")
    limitations = list(TIKTOK_BATCH_NON_CLAIMS)
    result = stage_and_write_packet(
        data_root=data_root,
        staged_artifacts=staged,
        source_slices=[
            SourceCaptureSlice(
                slice_id="tiktok_batch_admission_01",
                locator=known_fact(profile_url),
                timing=timing,
                access_posture=access,
                archive_history_posture=archive,
                media_modality_posture=media,
                re_capture_relationship=recapture,
                limitations=limitations,
                warning_notes=[],
                preserved_file_ids=[file_ids[TIKTOK_BATCH_CAPTURE_JSON_NAME]],
            )
        ],
        source_family="tiktok",
        source_surface=TIKTOK_BATCH_CAPTURE_SURFACE,
        source_locator=known_fact(profile_url),
        decision_question="fixture: TikTok batch admission",
        capture_context="fixture TikTok parsed creator-batch admission",
        actor_audience_context=not_applicable("fixture batch packet"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category=operator_category,
        session_identity=None,
        visible_mode_changes=["tiktok_sci_admission:parsed_creator_batch"],
        source_publication_or_event=timing.source_publication_or_event,
        source_edit_or_version=timing.source_edit_or_version,
        cutoff_posture=timing.cutoff_posture,
        recapture_time=timing.recapture_time,
        access_posture=access,
        archive_history_posture=archive,
        media_modality_posture=media,
        re_capture_relationship=recapture,
        warnings=[],
        limitations=limitations,
        receipt_summary=f"fixture TikTok batch admission for @{handle}",
        receipt_non_claims=TIKTOK_BATCH_NON_CLAIMS,
    )
    data_root.rebuild_availability()
    return Path(result.output_directory).name
