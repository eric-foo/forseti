"""Packet writer for the lean TikTok single-video admission slice."""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from source_capture.models import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map
from source_capture.tiktok.admission import (
    COMPLETE_LANE_NOTE,
    TIKTOK_COMMENT_LIST_ROUTE,
    assert_no_sensitive_tiktok_material,
    decoded_aweme_id_create_time_utc,
    extract_subtitle_infos,
    json_dumps_sanitized,
    parse_comment_list_bytes,
    parse_profile_list_items,
    parse_webvtt_cues,
)

TIKTOK_VIDEO_CAPTURE_SCHEMA_VERSION = "tiktok_video_capture_admission_v0"
TIKTOK_VIDEO_CAPTURE_SURFACE = "tiktok_video_comment_subtitle_admission"
TIKTOK_VIDEO_CAPTURE_JSON_NAME = "tiktok_video_capture.json"
_VIDEO_ID_RE = re.compile(r"\d{15,25}")

TIKTOK_VIDEO_NON_CLAIMS = [
    "not live browser automation",
    "not creator batch cadence capture",
    "not raw signed endpoint URL preservation",
    "not raw cookie/storage-state/session preservation",
    "not raw comment-list response-body preservation",
    "not raw subtitle URL preservation",
    "not raw media/video byte preservation",
    "not projection, extraction, or Judgment scoring",
]


def write_tiktok_video_packet(
    *,
    video_id: str,
    video_url: str,
    comment_list_json: bytes | None = None,
    video_item_json: bytes | None = None,
    profile_list_json: bytes | None = None,
    profile_list_source_surface: str = "/api/post/item_list/",
    subtitle_webvtt: bytes | None = None,
    output_directory: Path | None = None,
    data_root=None,
    decision_question: str,
    now_iso: str | None = None,
) -> tuple[int, str]:
    """Write a sanitized TikTok single-video admission packet.

    The runner admits already captured page-owned artifacts. It deliberately
    excludes raw signed URLs, cookies, storage-state contents, and raw response
    bodies from the preserved packet.
    """
    if (output_directory is None) == (data_root is None):
        raise ValueError("exactly one of output_directory or data_root is required")
    if not _VIDEO_ID_RE.fullmatch(video_id or ""):
        return 5, f"refusing to build packet: invalid TikTok video id {video_id!r}"
    if not video_url.startswith("https://www.tiktok.com/") or "?" in video_url:
        return 5, "refusing to build packet: video_url must be canonical TikTok https URL without query"
    if comment_list_json is None and video_item_json is None and profile_list_json is None and subtitle_webvtt is None:
        return 5, "refusing to build packet: at least one TikTok artifact is required"

    capture_ts = now_iso or _utc_now_z()
    try:
        payload = _build_payload(
            video_id=video_id,
            video_url=video_url,
            capture_ts=capture_ts,
            comment_list_json=comment_list_json,
            video_item_json=video_item_json,
            profile_list_json=profile_list_json,
            profile_list_source_surface=profile_list_source_surface,
            subtitle_webvtt=subtitle_webvtt,
        )
        assert_no_sensitive_tiktok_material(payload)
    except ValueError as exc:
        return 5, f"refusing to build packet: {exc}"

    staged_artifacts = [(TIKTOK_VIDEO_CAPTURE_JSON_NAME, json_dumps_sanitized(payload))]
    file_ids = staged_file_id_map(staged_artifacts)

    publication = _publication_fact(payload)
    timing = PacketTiming(
        source_publication_or_event=publication,
        source_edit_or_version=not_applicable("TikTok admission packet does not model source edit/version timing"),
        capture_time=known_fact(capture_ts),
        recapture_time=not_applicable("no prior TikTok video admission packet supplied"),
        cutoff_posture=not_applicable("cutoff posture does not apply to live/current TikTok admission"),
    )
    access = known_fact(
        "sanitized TikTok page-owned artifact admission; raw session/signed URL material excluded"
    )
    archive = not_attempted("TikTok admission packet does not query archive/history services")
    media = known_fact("sanitized comment/subtitle/profile-list fields preserved; no raw media bytes")
    recapture = not_applicable("no prior TikTok video admission packet supplied")

    source_slices = [
        SourceCaptureSlice(
            slice_id="tiktok_video_admission_01",
            locator=known_fact(video_url),
            timing=timing,
            access_posture=access,
            archive_history_posture=archive,
            media_modality_posture=media,
            re_capture_relationship=recapture,
            limitations=_limitations(payload),
            warning_notes=[],
            preserved_file_ids=[file_ids[TIKTOK_VIDEO_CAPTURE_JSON_NAME]],
        )
    ]

    result = stage_and_write_packet(
        output_directory=output_directory,
        data_root=data_root,
        staged_artifacts=staged_artifacts,
        source_slices=source_slices,
        source_family="tiktok",
        source_surface=TIKTOK_VIDEO_CAPTURE_SURFACE,
        source_locator=known_fact(video_url),
        decision_question=decision_question,
        capture_context=(
            "TikTok lean SCI admission from supplied page-owned artifacts; parser/sanitizer enforced; "
            "live browser and batch capture remain complete-lane work"
        ),
        actor_audience_context=not_applicable("public TikTok video capture; no actor/audience modeling at capture"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="tiktok_video_admission_cli_operator",
        session_identity=None,
        visible_mode_changes=[
            "tiktok_sci_admission:single_video_parser_sanitizer",
            COMPLETE_LANE_NOTE,
        ],
        source_publication_or_event=timing.source_publication_or_event,
        source_edit_or_version=timing.source_edit_or_version,
        cutoff_posture=timing.cutoff_posture,
        recapture_time=timing.recapture_time,
        access_posture=access,
        archive_history_posture=archive,
        media_modality_posture=media,
        re_capture_relationship=recapture,
        warnings=[],
        limitations=_limitations(payload),
        receipt_summary=(
            f"TikTok SCI admission packet for {video_id}: "
            f"comments={payload['comments']['posture']}, subtitles={payload['subtitles']['posture']}."
        ),
        receipt_non_claims=TIKTOK_VIDEO_NON_CLAIMS,
    )
    return 0, result.output_directory


def _build_payload(
    *,
    video_id: str,
    video_url: str,
    capture_ts: str,
    comment_list_json: bytes | None,
    video_item_json: bytes | None,
    profile_list_json: bytes | None,
    profile_list_source_surface: str,
    subtitle_webvtt: bytes | None,
) -> dict[str, Any]:
    profile_items: list[dict[str, Any]] = []
    if profile_list_json is not None:
        profile_payload = _loads_json_bytes(profile_list_json, label="profile-list JSON")
        profile_items = [
            item.to_dict()
            for item in parse_profile_list_items(profile_payload, source_surface=profile_list_source_surface)
            if item.video_id == video_id
        ]

    subtitle_infos: list[dict[str, Any]] = []
    if video_item_json is not None:
        video_item_payload = _loads_json_bytes(video_item_json, label="video item JSON")
        subtitle_infos = [item.to_dict() for item in extract_subtitle_infos(video_item_payload)]

    if comment_list_json is not None:
        comments = parse_comment_list_bytes(comment_list_json)
        comments_payload: dict[str, Any] = {"posture": "captured", **comments.to_dict()}
    else:
        comments_payload = {"posture": "not_attempted", "reason": "no comment-list JSON supplied"}

    if subtitle_webvtt is not None:
        cues = parse_webvtt_cues(subtitle_webvtt)
        transcript_text = "\n".join(cue.text for cue in cues)
        subtitles_payload: dict[str, Any] = {
            "posture": "source_native_webvtt_captured",
            "body_sha256": hashlib.sha256(subtitle_webvtt).hexdigest(),
            "body_size_bytes": len(subtitle_webvtt),
            "cue_count": len(cues),
            "transcript_text_sha256": hashlib.sha256(transcript_text.encode("utf-8")).hexdigest(),
            "cues": [cue.to_dict() for cue in cues],
        }
    elif subtitle_infos:
        subtitles_payload = {
            "posture": "subtitle_metadata_only",
            "reason": "subtitleInfos present but no WebVTT body supplied",
        }
    else:
        subtitles_payload = {"posture": "not_attempted", "reason": "no subtitle metadata/body supplied"}

    return {
        "capture_schema_version": TIKTOK_VIDEO_CAPTURE_SCHEMA_VERSION,
        "platform": "tiktok",
        "platform_video_id": video_id,
        "video_url": video_url,
        "capture_timestamp": capture_ts,
        "complete_lane_note": COMPLETE_LANE_NOTE,
        "derived_identity": {
            "decoded_aweme_id_create_time_utc": decoded_aweme_id_create_time_utc(video_id),
            "source_strength": "derived_from_video_id_not_tiktok_confirmed_createTime",
        },
        "profile_list_items": profile_items,
        "comments": comments_payload,
        "subtitle_infos": subtitle_infos,
        "subtitles": subtitles_payload,
        "non_claims": TIKTOK_VIDEO_NON_CLAIMS,
    }


def _publication_fact(payload: dict[str, Any]):
    for item in payload.get("profile_list_items", []):
        if not isinstance(item, dict):
            continue
        observed = item.get("create_time_utc")
        if isinstance(observed, str) and observed:
            return known_fact(observed)
    decoded = payload.get("derived_identity", {}).get("decoded_aweme_id_create_time_utc")
    if isinstance(decoded, str) and decoded:
        return unknown_with_reason(
            f"TikTok createTime not supplied; derived aweme-id timestamp candidate is {decoded}"
        )
    return unknown_with_reason("TikTok createTime was not supplied in admitted artifacts")


def _limitations(payload: dict[str, Any]) -> list[str]:
    limitations = [
        "raw_response_bodies_excluded:sanitized_admission_only",
        "raw_signed_urls_excluded:url_hashes_only",
    ]
    if payload["comments"]["posture"] != "captured":
        limitations.append(f"comments_posture:{payload['comments']['posture']}")
    if payload["subtitles"]["posture"] != "source_native_webvtt_captured":
        limitations.append(f"subtitles_posture:{payload['subtitles']['posture']}")
    if not payload.get("profile_list_items"):
        limitations.append("profile_list_item_absent_for_video")
    return limitations


def _loads_json_bytes(raw: bytes, *, label: str) -> object:
    if not raw:
        raise ValueError(f"empty {label}")
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError(f"invalid {label}: {exc}") from exc


def _utc_now_z() -> str:
    return _dt.datetime.utcnow().isoformat() + "Z"


__all__ = [
    "TIKTOK_VIDEO_CAPTURE_JSON_NAME",
    "TIKTOK_VIDEO_CAPTURE_SCHEMA_VERSION",
    "TIKTOK_VIDEO_CAPTURE_SURFACE",
    "TIKTOK_VIDEO_NON_CLAIMS",
    "write_tiktok_video_packet",
]
