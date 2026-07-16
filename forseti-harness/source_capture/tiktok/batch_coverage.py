"""Deterministic coverage view for admitted TikTok creator-batch packets."""

from __future__ import annotations

import json
from collections import Counter
from hashlib import sha256
from pathlib import Path
from typing import Any, Mapping

from source_capture.models import PreservedFile, SourceCapturePacket
from source_capture.projection_shared import resolve_preserved_file_path
from source_capture.tiktok.admission import assert_no_sensitive_tiktok_material
from source_capture.tiktok.batch_packet import (
    TIKTOK_BATCH_CAPTURE_JSON_NAME,
    TIKTOK_BATCH_CAPTURE_SURFACE,
)

TIKTOK_BATCH_COVERAGE_METHOD = "tiktok_batch_coverage_view"
TIKTOK_BATCH_COVERAGE_SCHEMA_VERSION = "tiktok_batch_coverage_view_v0"

TIKTOK_BATCH_COVERAGE_NON_CLAIMS = (
    "not_live_tiktok_capture_or_browser_automation",
    "not_direct_forged_tiktok_api_call",
    "not_product_mention_extraction",
    "not_cleaning_transform",
    "not_ecr_record",
    "not_judgment_or_buyer_proof",
    "not_persisted_derived_projection_lane",
    "not_cross_creator_detection_ceiling",
    "raw_comment_text_omitted",
    "raw_transcript_text_omitted",
    "raw_subtitle_cue_text_omitted",
)


def build_tiktok_batch_coverage_from_payload(
    payload: Mapping[str, Any],
    *,
    packet_id: str | None = None,
    raw_ref: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a text-free coverage view from a sanitized TikTok batch payload."""

    _validate_batch_payload(payload)
    videos = [_as_mapping(video) for video in _as_list(payload.get("videos"))]
    rows = [
        _coverage_row(video, raw_video_index=raw_video_index)
        for raw_video_index, video in enumerate(videos)
        if video
    ]
    batch_summary = _batch_summary(payload.get("batch_summary"), rows)
    rollup = _coverage_rollup(rows, batch_summary)
    coverage: dict[str, Any] = {
        "coverage_schema_version": TIKTOK_BATCH_COVERAGE_SCHEMA_VERSION,
        "coverage_method": TIKTOK_BATCH_COVERAGE_METHOD,
        "source_family": "tiktok",
        "source_surface": TIKTOK_BATCH_CAPTURE_SURFACE,
        "packet_id": packet_id,
        "raw_ref": dict(raw_ref or {}),
        "creator_handle": _first_str(payload.get("creator_handle")),
        "creator_profile_url": _first_str(payload.get("creator_profile_url")),
        "batch_label": _first_str(payload.get("batch_label")),
        "capture_timestamp": _first_str(payload.get("capture_timestamp")),
        "batch_summary": batch_summary,
        "coverage_rollup": rollup,
        "video_rows": rows,
        "loss_ledger": _loss_ledger(rows),
        "certification": "view_only; not_cleaned; not_normalized; not_judgment_ready; not_product_extraction",
        "non_claims": list(TIKTOK_BATCH_COVERAGE_NON_CLAIMS),
    }
    assert_no_sensitive_tiktok_material(coverage)
    return coverage


def build_tiktok_batch_coverage_from_packet_directory(packet_or_manifest_path: Path) -> dict[str, Any]:
    """Read an admitted TikTok batch packet directory and build its coverage view."""

    packet, raw_file_bytes_by_file_id, packet_dir = _read_packet_directory(packet_or_manifest_path)
    preserved = _tiktok_batch_capture_preserved_file(packet)
    raw_bytes = raw_file_bytes_by_file_id[preserved.file_id]
    payload = _loads_json_object(raw_bytes, f"{preserved.relative_packet_path}")
    return build_tiktok_batch_coverage_from_payload(
        payload,
        packet_id=packet.packet_id,
        raw_ref={
            "packet_id": packet.packet_id,
            "packet_directory_name": packet_dir.name,
            "file_id": preserved.file_id,
            "relative_packet_path": preserved.relative_packet_path,
            "sha256": preserved.sha256,
            "hash_basis": preserved.hash_basis,
        },
    )


def build_tiktok_batch_coverage_from_lake(data_root: Any, packet_id: str) -> dict[str, Any]:
    """Read a committed raw packet by key through a verified DataLakeRoot."""

    loaded = data_root.load_raw_packet(packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    preserved = _tiktok_batch_capture_preserved_file(packet)
    raw_bytes = loaded.bodies[preserved.file_id]
    payload = _loads_json_object(raw_bytes, f"{packet_id}:{preserved.relative_packet_path}")
    return build_tiktok_batch_coverage_from_payload(
        payload,
        packet_id=packet.packet_id,
        raw_ref={
            "packet_id": packet.packet_id,
            "file_id": preserved.file_id,
            "relative_packet_path": preserved.relative_packet_path,
            "sha256": preserved.sha256,
            "hash_basis": preserved.hash_basis,
        },
    )


def tiktok_batch_coverage_json_text(coverage: Mapping[str, Any]) -> str:
    """Render coverage JSON deterministically."""

    assert_no_sensitive_tiktok_material(coverage)
    return json.dumps(coverage, indent=2, sort_keys=True) + "\n"


def write_tiktok_batch_coverage(
    *,
    coverage: Mapping[str, Any],
    output_path: Path,
    overwrite: bool = False,
) -> Path:
    """Write coverage JSON to a local file. This does not append a data-lake record."""

    if output_path.exists() and not overwrite:
        raise FileExistsError(f"coverage output already exists: {output_path}")
    if output_path.exists() and output_path.is_dir():
        raise IsADirectoryError(f"coverage output is a directory: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(tiktok_batch_coverage_json_text(coverage), encoding="utf-8")
    return output_path


def _validate_batch_payload(payload: Mapping[str, Any]) -> None:
    if not isinstance(payload, Mapping):
        raise ValueError("TikTok batch coverage input must be a JSON object")
    if payload.get("platform") != "tiktok" or payload.get("source_surface") != TIKTOK_BATCH_CAPTURE_SURFACE:
        raise ValueError("coverage input is not a TikTok parsed-batch admission payload")
    if not isinstance(payload.get("videos"), list):
        raise ValueError("TikTok batch coverage input missing videos list")
    assert_no_sensitive_tiktok_material(payload)


def _coverage_row(video: Mapping[str, Any], *, raw_video_index: int) -> dict[str, Any]:
    comments = _as_mapping(video.get("comments"))
    subtitles = _as_mapping(video.get("subtitles"))
    source_text = _as_mapping(video.get("source_text"))
    seed = _as_mapping(video.get("typed_extraction_seed"))
    stats = _normalize_stats(video.get("stats"))
    desc = _first_str(source_text.get("desc")) or ""
    row: dict[str, Any] = {
        "row_kind": "tiktok_batch_video_coverage",
        "raw_video_index": raw_video_index,
        "source_index": _first_int(video.get("source_index")),
        "video_id": _first_str(video.get("video_id")),
        "video_url": _first_str(video.get("video_url")),
        "status": _first_str(video.get("status"), "unknown"),
        "create_time_utc": _first_str(video.get("create_time_utc")),
        "decoded_aweme_id_create_time_utc": _first_str(video.get("decoded_aweme_id_create_time_utc")),
        "stats": stats,
        "comments": _comment_coverage(comments, seed),
        "subtitles": _subtitle_coverage(subtitles, seed),
        "source_text_signals": _source_text_signals(source_text, seed, desc),
        "profile_list_source_receipt": _profile_list_source_receipt(video.get("profile_list_source_receipt")),
        "residuals": [],
        "limitations": list(TIKTOK_BATCH_COVERAGE_NON_CLAIMS),
    }
    row["residuals"] = _row_residuals(row)
    assert_no_sensitive_tiktok_material(row)
    return row


def _comment_coverage(comments: Mapping[str, Any], seed: Mapping[str, Any]) -> dict[str, Any]:
    envelope = _as_mapping(comments.get("envelope"))
    endpoint = _as_mapping(comments.get("endpoint_receipt"))
    return {
        "posture": _first_str(comments.get("posture"), "unknown"),
        "response_status": _first_int(comments.get("response_status")),
        "body_sha256": _first_str(comments.get("body_sha256")),
        "body_size_bytes": _first_int(comments.get("body_size_bytes"), 0),
        "captured_comment_count": _first_int(comments.get("captured_comment_count"), 0),
        "assessment_comment_count": _first_int(comments.get("assessment_comment_count"), 0),
        "envelope_total": _first_int(envelope.get("total"), 0),
        "envelope_has_more": _as_bool(envelope.get("has_more")),
        "field_coverage_keys": sorted(str(key) for key in _as_mapping(comments.get("field_coverage")).keys()),
        "endpoint_receipt": {
            "path": _first_str(endpoint.get("path")),
            "url_sha256": _first_str(endpoint.get("url_sha256")),
            "query_key_count": _first_int(endpoint.get("query_key_count"), 0),
        },
        "question_comment_count": _first_int(seed.get("comment_question_count"), 0),
        "intent_term_counts": _int_mapping(seed.get("comment_intent_term_counts")),
    }


def _subtitle_coverage(subtitles: Mapping[str, Any], seed: Mapping[str, Any]) -> dict[str, Any]:
    infos = [_as_mapping(item) for item in _as_list(subtitles.get("subtitle_infos"))]
    sources = _unique_strings(info.get("source") for info in infos)
    languages = _unique_strings(info.get("language_code_name") for info in infos)
    formats = _unique_strings(info.get("format") for info in infos)
    return {
        "posture": _first_str(subtitles.get("posture"), "unknown"),
        "subtitle_info_count": _first_int(subtitles.get("subtitle_info_count"), 0),
        "subtitle_sources": sources,
        "subtitle_language_code_names": languages,
        "subtitle_formats": formats,
        "body_sha256": _first_str(subtitles.get("body_sha256")),
        "body_size_bytes": _first_int(subtitles.get("body_size_bytes"), 0),
        "subtitle_url_sha256": _first_str(subtitles.get("subtitle_url_sha256")),
        "subtitle_url_length": _first_int(subtitles.get("subtitle_url_length")),
        "cue_count": _first_int(subtitles.get("cue_count"), 0),
        "transcript_char_count": _first_int(subtitles.get("transcript_char_count"), 0),
        "transcript_text_sha256": _first_str(subtitles.get("transcript_text_sha256")),
        "has_transcript_text": seed.get("has_transcript_text") is True,
        "transcript_signal_terms": _string_list(seed.get("transcript_signal_terms")),
    }


def _source_text_signals(
    source_text: Mapping[str, Any], seed: Mapping[str, Any], desc: str
) -> dict[str, Any]:
    return {
        "has_description_text": bool(desc.strip()),
        "description_char_count": len(desc),
        "description_sha256": sha256(desc.encode("utf-8")).hexdigest() if desc else None,
        "hashtags": _string_list(source_text.get("hashtags")),
        "source_mentions": _string_list(seed.get("source_mentions")),
        "disclosure_source_text_signals": _string_list(seed.get("disclosure_source_text_signals")),
        "has_disclosure_signal": seed.get("has_disclosure_signal") is True,
    }


def _profile_list_source_receipt(value: Any) -> dict[str, Any]:
    receipt = _as_mapping(value)
    if not receipt:
        return {}
    return {
        "source_response_path": _first_str(receipt.get("source_response_path")),
        "source_response_url_sha256": _first_str(receipt.get("source_response_url_sha256")),
    }


def _row_residuals(row: Mapping[str, Any]) -> list[str]:
    residuals: list[str] = []
    comments = _as_mapping(row.get("comments"))
    subtitles = _as_mapping(row.get("subtitles"))
    captured_comments = _first_int(comments.get("captured_comment_count"), 0) or 0
    envelope_total = _first_int(comments.get("envelope_total"), 0) or 0
    if captured_comments == 0:
        residuals.append("no_captured_comment_rows")
    if envelope_total > captured_comments:
        residuals.append("comment_envelope_exceeds_captured_rows")
    if subtitles.get("posture") != "source_native_webvtt_captured":
        residuals.append("source_native_webvtt_not_captured")
    if subtitles.get("has_transcript_text") is not True:
        residuals.append("transcript_text_not_available")
    return residuals


def _batch_summary(value: Any, rows: list[dict[str, Any]]) -> dict[str, Any]:
    summary = _as_mapping(value)
    return {
        "video_count": _first_int(summary.get("video_count"), len(rows)),
        "attempted_count": _first_int(summary.get("attempted_count"), 0),
        "completed_count": _first_int(summary.get("completed_count"), 0),
        "challenge_count": _first_int(summary.get("challenge_count"), 0),
        "comment_response_success_count": _first_int(summary.get("comment_response_success_count"), 0),
        "captured_comment_count": _first_int(summary.get("captured_comment_count"), 0),
        "comment_envelope_total_sum": _first_int(summary.get("comment_envelope_total_sum"), 0),
        "subtitle_info_video_count": _first_int(summary.get("subtitle_info_video_count"), 0),
        "subtitle_success_count": _first_int(summary.get("subtitle_success_count"), 0),
        "subtitle_cue_count": _first_int(summary.get("subtitle_cue_count"), 0),
        "transcript_text_available_count": _first_int(summary.get("transcript_text_available_count"), 0),
        "source_text_disclosure_video_count": _first_int(summary.get("source_text_disclosure_video_count"), 0),
        "stats_sums": _normalize_stats(summary.get("stats_sums")),
        "create_time_utc_range": summary.get("create_time_utc_range"),
    }


def _coverage_rollup(rows: list[dict[str, Any]], batch_summary: Mapping[str, Any]) -> dict[str, Any]:
    comment_postures = Counter(_first_str(_as_mapping(row.get("comments")).get("posture"), "unknown") for row in rows)
    subtitle_postures = Counter(_first_str(_as_mapping(row.get("subtitles")).get("posture"), "unknown") for row in rows)
    statuses = Counter(_first_str(row.get("status"), "unknown") for row in rows)
    captured_comment_count = sum(_first_int(_as_mapping(row.get("comments")).get("captured_comment_count"), 0) or 0 for row in rows)
    comment_envelope_total = sum(_first_int(_as_mapping(row.get("comments")).get("envelope_total"), 0) or 0 for row in rows)
    subtitle_cue_count = sum(_first_int(_as_mapping(row.get("subtitles")).get("cue_count"), 0) or 0 for row in rows)
    return {
        "video_count": len(rows),
        "attempted_count": _first_int(batch_summary.get("attempted_count"), 0),
        "completed_count": _first_int(batch_summary.get("completed_count"), 0),
        "challenge_count": _first_int(batch_summary.get("challenge_count"), 0),
        "captured_comment_count": captured_comment_count,
        "comment_envelope_total": comment_envelope_total,
        "subtitle_cue_count": subtitle_cue_count,
        "videos_with_comment_response": sum(1 for row in rows if _as_mapping(row.get("comments")).get("posture") == "captured_page_owned_response"),
        "videos_with_transcript_text": sum(1 for row in rows if _as_mapping(row.get("subtitles")).get("has_transcript_text") is True),
        "videos_with_disclosure_signal": sum(1 for row in rows if _as_mapping(row.get("source_text_signals")).get("has_disclosure_signal") is True),
        "videos_with_profile_list_receipt": sum(1 for row in rows if _as_mapping(row.get("profile_list_source_receipt"))),
        "videos_by_status": dict(sorted(statuses.items())),
        "comment_postures": dict(sorted(comment_postures.items())),
        "subtitle_postures": dict(sorted(subtitle_postures.items())),
    }


def _loss_ledger(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "raw_text_omissions": [
            {
                "source_path": "videos[].source_text.desc",
                "retained": "description_sha256, description_char_count, hashtags, source_mentions, disclosure_source_text_signals",
            },
            {
                "source_path": "videos[].comments.comments[].text",
                "retained": "captured_comment_count, envelope_total, question_comment_count, intent_term_counts",
            },
            {
                "source_path": "videos[].subtitles.transcript_text",
                "retained": "transcript_text_sha256, transcript_char_count, transcript_signal_terms",
            },
            {
                "source_path": "videos[].subtitles.cues[].text",
                "retained": "cue_count and subtitle timing/hash metadata only",
            },
        ],
        "omitted_comment_text_row_count": sum(_first_int(_as_mapping(row.get("comments")).get("captured_comment_count"), 0) or 0 for row in rows),
        "omitted_subtitle_cue_text_row_count": sum(_first_int(_as_mapping(row.get("subtitles")).get("cue_count"), 0) or 0 for row in rows),
        "certification": "omits_raw_text_fields; coverage_counts_and_hashes_retained",
    }


def _tiktok_batch_capture_preserved_file(packet: SourceCapturePacket) -> PreservedFile:
    if packet.source_family != "tiktok" or packet.source_surface != TIKTOK_BATCH_CAPTURE_SURFACE:
        raise ValueError(
            f"packet is not a TikTok parsed-batch admission packet: {packet.source_family}/{packet.source_surface}"
        )
    matches = [
        preserved
        for preserved in packet.preserved_files
        if preserved.relative_packet_path.replace("\\", "/").endswith(TIKTOK_BATCH_CAPTURE_JSON_NAME)
    ]
    if len(matches) != 1:
        raise ValueError(
            f"expected exactly one preserved {TIKTOK_BATCH_CAPTURE_JSON_NAME}, found {len(matches)}"
        )
    return matches[0]


def _read_packet_directory(packet_or_manifest_path: Path) -> tuple[SourceCapturePacket, dict[str, bytes], Path]:
    manifest_path = packet_or_manifest_path / "manifest.json" if packet_or_manifest_path.is_dir() else packet_or_manifest_path
    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest not found: {manifest_path}")
    packet_dir = manifest_path.parent
    packet = SourceCapturePacket.model_validate(json.loads(manifest_path.read_text(encoding="utf-8")))
    raw_file_bytes_by_file_id: dict[str, bytes] = {}
    for preserved_file in packet.preserved_files:
        # helper-delta: this reader returns a 3-tuple (adds packet_dir) so it
        # cannot BE projection_shared.read_packet_directory, but it adopts the
        # same path-containment guard so preserved-file reads cannot escape.
        raw_path = resolve_preserved_file_path(
            packet_dir, preserved_file.file_id, preserved_file.relative_packet_path
        )
        raw_file_bytes_by_file_id[preserved_file.file_id] = raw_path.read_bytes()
    return packet, raw_file_bytes_by_file_id, packet_dir


def _loads_json_object(raw: bytes, label: str) -> dict[str, Any]:
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label} is not UTF-8 JSON") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} is not valid JSON") from exc
    if not isinstance(parsed, dict):
        raise ValueError(f"{label} must contain a JSON object")
    return parsed


def _normalize_stats(value: Any) -> dict[str, Any]:
    stats = _as_mapping(value)
    normalized: dict[str, Any] = {}
    for key in (
        "playCount",
        "diggCount",
        "commentCount",
        "shareCount",
        "collectCount",
    ):
        raw = stats.get(key)
        if raw is None:
            continue
        parsed = _first_int(raw)
        normalized[key] = parsed if parsed is not None else raw
    return normalized


def _as_mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _first_str(*values: Any) -> str | None:
    for value in values:
        if value is None:
            continue
        text = value.strip() if isinstance(value, str) else str(value).strip()
        if text:
            return text
    return None


def _first_int(*values: Any) -> int | None:
    for value in values:
        if value is None or isinstance(value, bool):
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return None


def _as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes"}:
            return True
        if lowered in {"false", "0", "no"}:
            return False
    return None


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        text = _first_str(item)
        if text is not None:
            result.append(text)
    return result


def _unique_strings(values: Any) -> list[str]:
    result: list[str] = []
    for item in values:
        text = _first_str(item)
        if text is not None and text not in result:
            result.append(text)
    return result


def _int_mapping(value: Any) -> dict[str, int]:
    if not isinstance(value, Mapping):
        return {}
    result: dict[str, int] = {}
    for key, item in value.items():
        parsed = _first_int(item)
        if parsed is not None:
            result[str(key)] = parsed
    return dict(sorted(result.items()))
