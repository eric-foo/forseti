"""YouTube behavioral projection over existing metadata/comment + transcript artifacts.

This module deliberately does not acquire anything. It projects the incumbent YouTube
metadata/comment packets and transcript packet anchors into one inspectable, video-keyed
behavioral item so downstream code can reason over "what we know for this video" without
pretending that every capture lane uses the same machinery.
"""
from __future__ import annotations

import json
from typing import Any, Iterable, Mapping, Sequence

from data_lake.root import DataLakeRootError


YOUTUBE_BEHAVIORAL_PROJECTION_METHOD = "youtube_behavioral_projection"
YOUTUBE_BEHAVIORAL_PROJECTION_VERSION = "v0"

CAPTION_SURFACE = "youtube_captions"
AUDIO_SURFACE = "youtube_audio"
WATCH_METADATA_SURFACE = "youtube_watch_metadata_comments"
WATCH_CAPTURE_JSON_NAME = "youtube_watch_capture.json"
ASR_LANE = "transcript_asr"
ASR_SET_LANE = "transcript_asr__set"

EXTRACTION_COMPLETE_STATUSES = {"extracted", "skipped_done"}
EXTRACTION_PROBLEM_STATUSES = {
    "failed",
    "partial_needs_cleanup",
    "discovery_failed",
    "ambiguous_anchor_result",
}
SOURCE_COMPLETION_PROBLEMS = {
    "partial_needs_cleanup",
    "missing_derived_record",
    "discovery_failed",
}
SOURCE_POSTURE_PROBLEMS = {"failed"}
SOURCE_NON_ELIGIBLE_PROBLEMS = SOURCE_COMPLETION_PROBLEMS | SOURCE_POSTURE_PROBLEMS


def normalize_youtube_metadata_packet(
    packet: Mapping[str, Any] | None,
    *,
    comment_sample_limit: int = 5,
) -> dict[str, Any] | None:
    """Normalize legacy YouTube metadata/comment packet shapes without rewriting them."""
    if packet is None:
        return None
    video_id = _string_or_none(packet.get("platform_video_id") or packet.get("video_id"))
    if video_id is None:
        return None

    channel = packet.get("channel")
    if not isinstance(channel, Mapping):
        channel = {
            "channel_id": _string_or_none(packet.get("channel_id")),
            "author": _string_or_none(packet.get("author")),
        }
    metadata = packet.get("metadata")
    if not isinstance(metadata, Mapping):
        metadata = {
            "title": _string_or_none(packet.get("title")),
            "length_seconds": _int_or_none(packet.get("length_seconds")),
            "publish_date": _string_or_none(packet.get("publish_date")),
        }
    engagement = packet.get("engagement")
    if not isinstance(engagement, Mapping):
        engagement = {
            "view_count": _int_or_none(packet.get("view_count")),
            "view_count_source_path": _string_or_none(packet.get("view_count_source_path")),
            "like_count_text": _string_or_none(packet.get("like_count_text")),
        }
    comments = packet.get("comments")
    comment_rows = comments if isinstance(comments, list) else []
    availability = packet.get("availability")
    if not isinstance(availability, Mapping):
        availability = {}
    metric_receipts = packet.get("metric_receipts")
    if not isinstance(metric_receipts, Mapping):
        metric_receipts = {}
    receipts = packet.get("receipts")
    if not isinstance(receipts, Mapping):
        receipts = {
            "http_status": _int_or_none(packet.get("http_status")),
            "retrieval_time_utc": _string_or_none(packet.get("retrieval_time_utc")),
            "raw_body_sha256": _string_or_none(packet.get("raw_body_sha256")),
            "byte_size": _int_or_none(packet.get("byte_size")),
        }

    return {
        "platform": "youtube",
        "platform_video_id": video_id,
        "capture_packet_id": _string_or_none(packet.get("capture_packet_id")),
        "source_surface": _string_or_none(packet.get("source_surface")),
        "capture_schema_version": _string_or_none(packet.get("capture_schema_version")),
        "capture_timestamp": _string_or_none(packet.get("capture_timestamp")),
        "surface_type": _string_or_none(packet.get("surface_type")),
        "watch_url": _string_or_none(packet.get("watch_url")) or f"https://www.youtube.com/watch?v={video_id}",
        "canonical_url": _string_or_none(packet.get("canonical_url"))
        or _string_or_none(packet.get("watch_url"))
        or f"https://www.youtube.com/watch?v={video_id}",
        "channel": _compact_dict(dict(channel)),
        "metadata": _compact_dict(dict(metadata)),
        "engagement": _compact_dict(dict(engagement)),
        "availability": _compact_dict(dict(availability)),
        "metric_receipts": _compact_dict(dict(metric_receipts)),
        "comments": {
            "posture": _string_or_none(packet.get("comments_posture")) or "unknown",
            "comment_count_text": _string_or_none(packet.get("comment_count_text")),
            "sample_count": len(comment_rows),
            "sample": comment_rows[: max(0, comment_sample_limit)],
        },
        "receipts": _compact_dict(dict(receipts)),
    }


def metadata_packet_for_video(
    data_root,
    platform_video_id: str,
    *,
    rebuild_availability: bool = False,
) -> dict[str, Any] | None:
    """Discover the latest committed YouTube watch metadata/comment packet for one video."""
    if rebuild_availability:
        data_root.rebuild_availability()

    candidates: list[dict[str, Any]] = []
    for packet_id in data_root.list_available(source_family="youtube"):
        try:
            loaded = data_root.load_raw_packet(packet_id)
        except DataLakeRootError:
            continue
        if loaded.manifest.get("source_surface") != WATCH_METADATA_SURFACE:
            continue
        files = _file_paths(loaded.manifest)
        packet = _watch_metadata_packet(packet_id=packet_id, loaded=loaded, files=files)
        if packet is None:
            continue
        packet_video_id = _string_or_none(packet.get("platform_video_id") or packet.get("video_id"))
        if packet_video_id != platform_video_id:
            continue
        candidates.append(packet)
    if not candidates:
        return None
    return max(
        candidates,
        key=lambda packet: (
            _string_or_none(packet.get("capture_timestamp")) or "",
            _string_or_none(packet.get("capture_packet_id")) or "",
        ),
    )


def transcript_sources_for_video(
    data_root,
    platform_video_id: str,
    *,
    rebuild_availability: bool = False,
) -> list[dict[str, Any]]:
    """Discover committed YouTube transcript sources for one video from the local lake.

    ``rebuild_availability`` is opt-in because rebuilding the index is a write; callers that need
    raw-derived discovery can request it explicitly.
    """
    if rebuild_availability:
        data_root.rebuild_availability()

    sources: list[dict[str, Any]] = []
    for packet_id in data_root.list_available(source_family="youtube"):
        try:
            loaded = data_root.load_raw_packet(packet_id)
        except DataLakeRootError as exc:
            sources.append(
                _discovery_failure_source(
                    platform_video_id=platform_video_id,
                    packet_id=packet_id,
                    error=str(exc),
                )
            )
            continue
        surface = loaded.manifest.get("source_surface")
        files = _file_paths(loaded.manifest)
        meta = _capture_metadata(loaded, files)
        meta_video_id = _string_or_none(meta.get("platform_video_id"))
        if meta_video_id != platform_video_id:
            continue
        if surface == CAPTION_SURFACE:
            source = _caption_source(packet_id=packet_id, loaded=loaded, files=files, meta=meta)
            if source is not None:
                sources.append(source)
        elif surface == AUDIO_SURFACE:
            records = _asr_records(data_root, packet_id)
            if not records:
                sources.append(
                    _base_transcript_source(
                        platform_video_id=platform_video_id,
                        transcript_anchor=packet_id,
                        source_kind="asr",
                        source_route="youtube_audio_asr",
                        source_status="missing_derived_record",
                        posture="missing_derived_record",
                        cue_count=0,
                        capture_timestamp=_string_or_none(meta.get("capture_timestamp")),
                    )
                )
                continue
            for record_id, record, source_status in records:
                video_id = _string_or_none(record.get("video_id")) or meta_video_id
                if video_id != platform_video_id:
                    continue
                sources.append(
                    _asr_source(
                        packet_id=packet_id,
                        record_id=record_id,
                        record=record,
                        source_status=source_status,
                        meta=meta,
                    )
                )
    return sorted(sources, key=_source_sort_key)


def _discovery_failure_source(*, platform_video_id: str, packet_id: str, error: str) -> dict[str, Any]:
    return _base_transcript_source(
        platform_video_id=platform_video_id,
        transcript_anchor=packet_id,
        source_kind="discovery",
        source_route="youtube_packet_discovery",
        source_status="discovery_failed",
        posture="discovery_failed",
        cue_count=0,
        capture_timestamp=None,
        discovery_error=error,
    )


def project_youtube_behavioral_item(
    *,
    metadata_packet: Mapping[str, Any] | None = None,
    transcript_sources: Sequence[Mapping[str, Any]] = (),
    extraction_results: Sequence[Mapping[str, Any]] = (),
    platform_video_id: str | None = None,
    comment_sample_limit: int = 5,
) -> dict[str, Any]:
    """Build a video-level behavioral projection from already-captured inputs."""
    metadata = normalize_youtube_metadata_packet(
        metadata_packet, comment_sample_limit=comment_sample_limit
    )
    metadata_video_id = _string_or_none((metadata or {}).get("platform_video_id"))
    video_id = (
        _string_or_none(platform_video_id)
        or metadata_video_id
        or _single_video_id(transcript_sources)
    )
    if not video_id:
        raise ValueError("platform_video_id is required when metadata and sources do not supply one")

    residuals: list[str] = []
    if metadata is None:
        _append_residual_once(residuals, "youtube_metadata_packet_absent")
    elif metadata_video_id != video_id:
        _append_residual_once(residuals, f"youtube_metadata_packet_video_mismatch:{metadata_video_id}")
        metadata = None

    filtered_sources: list[dict[str, Any]] = []
    for source in transcript_sources:
        source_video_id = _string_or_none(source.get("platform_video_id"))
        if source_video_id and source_video_id != video_id:
            _append_residual_once(residuals, f"youtube_transcript_source_video_mismatch:{source_video_id}")
            continue
        filtered_sources.append(dict(source))

    exact_results, anchor_results = _extraction_result_indexes(extraction_results)
    duplicate_eligible_anchors = _duplicate_eligible_anchors(filtered_sources)
    enriched_sources = [
        _attach_extraction_status(
            source,
            _result_for_source(
                source,
                exact_results=exact_results,
                anchor_results=anchor_results,
                duplicate_eligible_anchors=duplicate_eligible_anchors,
            ),
        )
        for source in sorted(filtered_sources, key=_source_sort_key)
    ]
    rollup = _extraction_rollup(enriched_sources, residuals=residuals)
    canonical = _canonical_transcript_source(enriched_sources)

    return {
        "projection_method": YOUTUBE_BEHAVIORAL_PROJECTION_METHOD,
        "projection_version": YOUTUBE_BEHAVIORAL_PROJECTION_VERSION,
        "platform": "youtube",
        "platform_video_id": video_id,
        "metadata_capture": metadata,
        "transcript": {
            "source_count": len(enriched_sources),
            "sources": enriched_sources,
            "canonical_source": canonical,
            "extraction_rollup": rollup,
        },
        "behavioral_completeness": {
            "status": rollup["status"],
            "complete": rollup["status"] == "complete",
            "residuals": residuals,
        },
    }


def project_youtube_behavioral_item_from_lake(
    *,
    data_root,
    platform_video_id: str,
    metadata_packet: Mapping[str, Any] | None = None,
    extraction_results: Sequence[Mapping[str, Any]] = (),
    rebuild_availability: bool = False,
    comment_sample_limit: int = 5,
) -> dict[str, Any]:
    """Convenience wrapper for the common "video id + local capture lake" case."""
    if rebuild_availability:
        data_root.rebuild_availability()
    discovered_metadata = metadata_packet
    if discovered_metadata is None:
        discovered_metadata = metadata_packet_for_video(
            data_root, platform_video_id, rebuild_availability=False
        )
    return project_youtube_behavioral_item(
        metadata_packet=discovered_metadata,
        transcript_sources=transcript_sources_for_video(
            data_root, platform_video_id, rebuild_availability=False
        ),
        extraction_results=extraction_results,
        platform_video_id=platform_video_id,
        comment_sample_limit=comment_sample_limit,
    )


def _base_transcript_source(
    *,
    platform_video_id: str,
    transcript_anchor: str,
    source_kind: str,
    source_route: str,
    source_status: str,
    posture: str,
    cue_count: int,
    capture_timestamp: str | None,
    **extra: Any,
) -> dict[str, Any]:
    extraction_eligible = (
        source_status == "complete"
        and cue_count > 0
        and posture in {"caption_ready", "transcribed"}
    )
    reason = None
    if not extraction_eligible:
        if source_status != "complete":
            reason = source_status
        elif posture in SOURCE_POSTURE_PROBLEMS:
            reason = posture
        elif cue_count <= 0:
            reason = "zero_cues"
        else:
            reason = posture
    source = {
        "platform": "youtube",
        "platform_video_id": platform_video_id,
        "transcript_anchor": transcript_anchor,
        "transcript_source_key": _transcript_source_key(
            transcript_anchor=transcript_anchor,
            source_kind=source_kind,
            asr_record_id=_string_or_none(extra.get("asr_record_id")),
        ),
        "source_kind": source_kind,
        "source_route": source_route,
        "source_status": source_status,
        "posture": posture,
        "cue_count": cue_count,
        "extraction_eligible": extraction_eligible,
        "non_eligible_reason": reason,
        "capture_timestamp": capture_timestamp,
    }
    source.update(_compact_dict(extra))
    return source


def _caption_source(*, packet_id: str, loaded, files: Mapping[str, str], meta: Mapping[str, Any]) -> dict[str, Any] | None:
    video_id = _string_or_none(meta.get("platform_video_id"))
    if video_id is None:
        return None
    json3 = _body_ending_with(loaded, files, ".json3")
    cue_count = _int_or_none(meta.get("cue_count"))
    if cue_count is None and json3 is not None:
        cue_count = _count_json3_cues(json3)
    cue_count = cue_count or 0
    return _base_transcript_source(
        platform_video_id=video_id,
        transcript_anchor=packet_id,
        source_kind="caption",
        source_route=CAPTION_SURFACE,
        source_status="complete",
        posture="caption_ready" if cue_count > 0 else "caption_empty",
        cue_count=cue_count,
        capture_timestamp=_string_or_none(meta.get("capture_timestamp")),
        caption_kind=_string_or_none(meta.get("caption_kind")),
        language=_string_or_none(meta.get("caption_lang")),
        original_language_assumed=meta.get("original_language_assumed")
        if isinstance(meta.get("original_language_assumed"), bool)
        else None,
        title=_string_or_none(meta.get("title")),
        channel_id=_string_or_none(meta.get("channel_id")),
    )


def _asr_source(
    *,
    packet_id: str,
    record_id: str,
    record: Mapping[str, Any],
    source_status: str,
    meta: Mapping[str, Any],
) -> dict[str, Any]:
    cues = record.get("cues")
    cue_count = _int_or_none(record.get("cue_count"))
    if cue_count is None and isinstance(cues, list):
        cue_count = len(cues)
    provenance = record.get("provenance")
    return _base_transcript_source(
        platform_video_id=_string_or_none(record.get("video_id") or meta.get("platform_video_id")) or "",
        transcript_anchor=packet_id,
        source_kind="asr",
        source_route="youtube_audio_asr",
        source_status=source_status,
        posture=_string_or_none(record.get("posture")) or "unknown",
        cue_count=cue_count or 0,
        capture_timestamp=_string_or_none(record.get("retrieval_time_utc") or meta.get("capture_timestamp")),
        asr_record_id=record_id,
        provenance=provenance if isinstance(provenance, Mapping) else None,
    )


def _attach_extraction_status(
    source: Mapping[str, Any],
    result: Mapping[str, Any] | None,
) -> dict[str, Any]:
    out = dict(source)
    out.setdefault("transcript_source_key", _source_key(out))
    if not out.get("extraction_eligible"):
        out["extraction_status"] = "not_extraction_eligible"
        return out
    status = _string_or_none((result or {}).get("status")) or "not_attempted"
    out["extraction_status"] = status
    if result:
        if "path" in result:
            out["extraction_record_path"] = result.get("path")
        if "error" in result:
            out["extraction_error"] = result.get("error")
    return out


def _extraction_rollup(
    sources: Sequence[Mapping[str, Any]],
    *,
    residuals: list[str],
) -> dict[str, Any]:
    eligible = [source for source in sources if source.get("extraction_eligible") is True]
    complete = [
        source
        for source in eligible
        if _string_or_none(source.get("extraction_status")) in EXTRACTION_COMPLETE_STATUSES
    ]
    incomplete = [
        source
        for source in eligible
        if _string_or_none(source.get("extraction_status")) not in EXTRACTION_COMPLETE_STATUSES
    ]
    extraction_problem_count = sum(
        1
        for source in eligible
        if _string_or_none(source.get("extraction_status")) in EXTRACTION_PROBLEM_STATUSES
    )
    source_problem_count = sum(1 for source in sources if _source_has_problem(source))

    for source in sources:
        source_key = _source_key(source)
        source_status = _string_or_none(source.get("source_status"))
        posture = _string_or_none(source.get("posture"))
        non_eligible_reason = _string_or_none(source.get("non_eligible_reason"))
        extraction_status = _string_or_none(source.get("extraction_status"))

        if source_status in SOURCE_COMPLETION_PROBLEMS:
            _append_residual_once(residuals, f"youtube_transcript_source_{source_status}:{source_key}")
        if posture in SOURCE_POSTURE_PROBLEMS:
            _append_residual_once(residuals, f"youtube_transcript_source_{posture}:{source_key}")
        if source.get("extraction_eligible") is False and non_eligible_reason in SOURCE_NON_ELIGIBLE_PROBLEMS:
            _append_residual_once(
                residuals,
                f"youtube_transcript_source_not_extraction_eligible:{source_key}",
            )
        if extraction_status in EXTRACTION_PROBLEM_STATUSES:
            _append_residual_once(residuals, f"youtube_transcript_extraction_{extraction_status}:{source_key}")

    if not eligible:
        status = "no_extraction_eligible_sources"
    elif not incomplete and source_problem_count == 0:
        status = "complete"
    elif not incomplete:
        status = "complete_with_residuals"
    elif complete and extraction_problem_count:
        status = "partial_failed"
    elif complete and incomplete:
        status = "partial"
    elif extraction_problem_count:
        status = "failed"
    elif source_problem_count:
        status = "source_problem"
    else:
        status = "not_attempted"

    return {
        "status": status,
        "eligible_source_count": len(eligible),
        "complete_source_count": len(complete),
        "incomplete_source_count": len(incomplete),
        "source_problem_count": source_problem_count,
        "extraction_problem_count": extraction_problem_count,
    }


def _canonical_transcript_source(sources: Sequence[Mapping[str, Any]]) -> dict[str, Any] | None:
    eligible = [source for source in sources if source.get("extraction_eligible") is True]
    if not eligible:
        return None
    best_rank = min(_source_rank(source) for source in eligible)
    chosen = max(
        (source for source in eligible if _source_rank(source) == best_rank),
        key=lambda source: (
            str(source.get("capture_timestamp") or ""),
            str(source.get("transcript_anchor") or ""),
        ),
    )
    return {
        "transcript_anchor": chosen.get("transcript_anchor"),
        "source_kind": chosen.get("source_kind"),
        "source_route": chosen.get("source_route"),
        "caption_kind": chosen.get("caption_kind"),
        "extraction_status": chosen.get("extraction_status"),
    }


def _result_for_source(
    source: Mapping[str, Any],
    *,
    exact_results: Mapping[str, Mapping[str, Any]],
    anchor_results: Mapping[str, Sequence[Mapping[str, Any]]],
    duplicate_eligible_anchors: set[str],
) -> Mapping[str, Any] | None:
    source_key = _source_key(source)
    if source_key in exact_results:
        return exact_results[source_key]

    anchor = _string_or_none(source.get("transcript_anchor"))
    if anchor is None:
        return None
    anchor_level = anchor_results.get(anchor, [])
    if not anchor_level:
        return None
    if anchor in duplicate_eligible_anchors:
        return {
            "status": "ambiguous_anchor_result",
            "error": "anchor-level extraction result cannot be assigned to duplicate eligible transcript sources",
        }
    if len(anchor_level) == 1:
        return anchor_level[0]
    return {
        "status": "ambiguous_anchor_result",
        "error": "multiple anchor-level extraction results cannot be assigned to one transcript source",
    }


def _extraction_result_indexes(
    results: Iterable[Mapping[str, Any]],
) -> tuple[dict[str, Mapping[str, Any]], dict[str, list[Mapping[str, Any]]]]:
    exact: dict[str, Mapping[str, Any]] = {}
    by_anchor: dict[str, list[Mapping[str, Any]]] = {}
    for result in results:
        explicit_key = _string_or_none(result.get("transcript_source_key") or result.get("source_key"))
        if explicit_key is not None:
            exact[explicit_key] = result
            continue
        anchor = _string_or_none(result.get("anchor") or result.get("packet_id"))
        if anchor is None:
            continue
        source_kind = _string_or_none(result.get("source_kind"))
        asr_record_id = _string_or_none(result.get("asr_record_id"))
        if source_kind is not None or asr_record_id is not None:
            exact[
                _transcript_source_key(
                    transcript_anchor=anchor,
                    source_kind=source_kind or "asr",
                    asr_record_id=asr_record_id,
                )
            ] = result
        else:
            by_anchor.setdefault(anchor, []).append(result)
    return exact, by_anchor


def _duplicate_eligible_anchors(sources: Sequence[Mapping[str, Any]]) -> set[str]:
    counts: dict[str, int] = {}
    for source in sources:
        if source.get("extraction_eligible") is not True:
            continue
        anchor = _string_or_none(source.get("transcript_anchor"))
        if anchor is not None:
            counts[anchor] = counts.get(anchor, 0) + 1
    return {anchor for anchor, count in counts.items() if count > 1}


def _asr_records(data_root, audio_packet_id: str) -> list[tuple[str, dict[str, Any], str]]:
    lane_dir = data_root.lane_dir(subtree="derived", raw_anchor=audio_packet_id, lane=ASR_LANE)
    if not lane_dir.is_dir():
        return []
    records: list[tuple[str, dict[str, Any], str]] = []
    for record_file in sorted(lane_dir.iterdir()):
        if not record_file.is_file():
            continue
        try:
            data = json.loads(record_file.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(data, dict):
            continue
        complete = data_root.is_record_set_complete(
            subtree="derived",
            raw_anchor=audio_packet_id,
            record_id=record_file.name,
            completion_lane=ASR_SET_LANE,
        )
        records.append((record_file.name, data, "complete" if complete else "partial_needs_cleanup"))
    return records


def _source_has_problem(source: Mapping[str, Any]) -> bool:
    return (
        _string_or_none(source.get("source_status")) in SOURCE_COMPLETION_PROBLEMS
        or _string_or_none(source.get("posture")) in SOURCE_POSTURE_PROBLEMS
        or _string_or_none(source.get("non_eligible_reason")) in SOURCE_NON_ELIGIBLE_PROBLEMS
    )


def _source_key(source: Mapping[str, Any]) -> str:
    existing = _string_or_none(source.get("transcript_source_key"))
    if existing is not None:
        return existing
    return _transcript_source_key(
        transcript_anchor=_string_or_none(source.get("transcript_anchor")) or "unknown_anchor",
        source_kind=_string_or_none(source.get("source_kind")) or "unknown",
        asr_record_id=_string_or_none(source.get("asr_record_id")),
    )


def _transcript_source_key(
    *,
    transcript_anchor: str,
    source_kind: str,
    asr_record_id: str | None = None,
) -> str:
    if source_kind == "asr":
        return f"{transcript_anchor}:asr:{asr_record_id or 'unknown_record'}"
    return f"{transcript_anchor}:{source_kind}"


def _append_residual_once(residuals: list[str], residual: str) -> None:
    if residual not in residuals:
        residuals.append(residual)


def _file_paths(manifest: Mapping[str, Any]) -> dict[str, str]:
    return {
        str(preserved.get("file_id")): str(preserved.get("relative_packet_path"))
        for preserved in manifest.get("preserved_files", [])
        if isinstance(preserved, Mapping)
        and isinstance(preserved.get("file_id"), str)
        and isinstance(preserved.get("relative_packet_path"), str)
    }


def _body_ending_with(loaded, files: Mapping[str, str], suffix: str) -> bytes | None:
    for file_id, path in files.items():
        if path.endswith(suffix):
            return loaded.bodies.get(file_id)
    return None


def _watch_metadata_packet(*, packet_id: str, loaded, files: Mapping[str, str]) -> dict[str, Any] | None:
    body = _body_ending_with(loaded, files, WATCH_CAPTURE_JSON_NAME)
    if body is None:
        return None
    try:
        payload = json.loads(body.decode("utf-8"))
    except ValueError:
        return None
    if not isinstance(payload, Mapping):
        return None
    nested_packet = payload.get("packet")
    packet = dict(nested_packet) if isinstance(nested_packet, Mapping) else {}

    platform_video_id = _string_or_none(payload.get("platform_video_id"))
    if platform_video_id is not None:
        packet.setdefault("platform_video_id", platform_video_id)
        packet.setdefault("video_id", platform_video_id)
    for field in ("watch_url", "capture_timestamp", "capture_schema_version"):
        value = _string_or_none(payload.get(field))
        if value is not None:
            packet.setdefault(field, value)
    for field in ("availability", "metric_receipts"):
        value = payload.get(field)
        if isinstance(value, Mapping):
            packet.setdefault(field, value)
    packet["capture_packet_id"] = packet_id
    packet["source_surface"] = _string_or_none(loaded.manifest.get("source_surface")) or WATCH_METADATA_SURFACE
    return packet


def _capture_metadata(loaded, files: Mapping[str, str]) -> dict[str, Any]:
    body = _body_ending_with(loaded, files, "capture_metadata.json")
    if body is None:
        return {}
    try:
        data = json.loads(body.decode("utf-8"))
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


def _count_json3_cues(raw: bytes) -> int:
    try:
        data = json.loads(raw.decode("utf-8"))
    except ValueError:
        return 0
    events = data.get("events") if isinstance(data, Mapping) else None
    if not isinstance(events, list):
        return 0
    count = 0
    for event in events:
        if not isinstance(event, Mapping):
            continue
        segs = event.get("segs")
        if not isinstance(segs, list):
            continue
        text = "".join(str(seg.get("utf8") or "") for seg in segs if isinstance(seg, Mapping)).strip()
        if text:
            count += 1
    return count


def _single_video_id(sources: Sequence[Mapping[str, Any]]) -> str | None:
    ids = {
        source.get("platform_video_id")
        for source in sources
        if isinstance(source.get("platform_video_id"), str) and source.get("platform_video_id")
    }
    if len(ids) == 1:
        return str(next(iter(ids)))
    if len(ids) > 1:
        raise ValueError("transcript sources span multiple platform_video_id values")
    return None


def _source_sort_key(source: Mapping[str, Any]) -> tuple[int, str, str]:
    return (
        _source_rank(source),
        str(source.get("capture_timestamp") or ""),
        str(source.get("transcript_anchor") or ""),
    )


def _source_rank(source: Mapping[str, Any]) -> int:
    kind = _string_or_none(source.get("source_kind"))
    caption_kind = _string_or_none(source.get("caption_kind"))
    return 0 if kind == "caption" and caption_kind == "manual" else 1 if kind == "caption" else 2


def _compact_dict(data: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in data.items() if value is not None}


def _string_or_none(value: Any) -> str | None:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    return None


def _int_or_none(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        stripped = value.replace(",", "").strip()
        return int(stripped) if stripped.isdigit() else None
    return None


__all__ = [
    "AUDIO_SURFACE",
    "CAPTION_SURFACE",
    "WATCH_METADATA_SURFACE",
    "YOUTUBE_BEHAVIORAL_PROJECTION_METHOD",
    "YOUTUBE_BEHAVIORAL_PROJECTION_VERSION",
    "metadata_packet_for_video",
    "normalize_youtube_metadata_packet",
    "project_youtube_behavioral_item",
    "project_youtube_behavioral_item_from_lake",
    "transcript_sources_for_video",
]
