"""Instagram Reels behavioral projection over already-captured surfaces.

This module deliberately does not acquire, render, transcribe, extract, or write
anything. It centralizes existing IG grid/comment/transcript/extraction facts
into one shortcode-keyed behavior record so downstream code can inspect partials
and residuals without pretending IG uses YouTube's capture machinery.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence


IG_REELS_BEHAVIORAL_PROJECTION_METHOD = "ig_reels_behavioral_projection"
IG_REELS_BEHAVIORAL_PROJECTION_VERSION = "v0"

EXTRACTION_COMPLETE_STATUSES = {"extracted", "skipped_done"}
EXTRACTION_PROBLEM_STATUSES = {
    "failed",
    "partial_needs_cleanup",
    "discovery_failed",
    "ambiguous_anchor_result",
    "source_lineage_missing",
    "source_lineage_incomplete",
    "source_lineage_invalid",
}
SOURCE_COMPLETION_PROBLEMS = {
    "partial_needs_cleanup",
    "missing_derived_record",
    "discovery_failed",
}
SOURCE_POSTURE_PROBLEMS = {
    "failed",
    "render_unavailable",
    "no_audio_handle",
    "download_failed",
}
SOURCE_NON_ELIGIBLE_PROBLEMS = SOURCE_COMPLETION_PROBLEMS | SOURCE_POSTURE_PROBLEMS


def project_ig_reels_behavioral_item(
    *,
    platform_item_id: str,
    grid_rows: Sequence[Mapping[str, Any] | Any] = (),
    comment_sets: Sequence[Mapping[str, Any] | Any] = (),
    standalone_audio_transcript_records: Sequence[Mapping[str, Any] | Any] = (),
    deep_capture_transcript_records: Sequence[Mapping[str, Any] | Any] = (),
    extraction_results: Sequence[Mapping[str, Any] | Any] = (),
) -> dict[str, Any]:
    """Build a shortcode-level IG behavior record from already-captured inputs."""
    shortcode = _required_shortcode(platform_item_id)
    residuals: list[str] = []

    candidate = _candidate_projection(shortcode, grid_rows, residuals=residuals)
    comments = _comment_projection(
        shortcode,
        comment_sets,
        deep_capture_transcript_records,
        residuals=residuals,
    )
    transcript_sources = _transcript_sources(
        shortcode,
        standalone_audio_transcript_records,
        deep_capture_transcript_records,
        residuals=residuals,
    )
    exact_results, anchor_results = _extraction_result_indexes(extraction_results)
    duplicate_eligible_anchors = _duplicate_eligible_anchors(transcript_sources)
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
        for source in sorted(transcript_sources, key=_source_sort_key)
    ]
    rollup = _extraction_rollup(enriched_sources, residuals=residuals)
    canonical = _canonical_transcript_source(enriched_sources)
    correlation = _persistence_correlation(candidate, comments, enriched_sources)

    behavioral_status = _behavioral_status(rollup["status"], residuals)
    return {
        "projection_method": IG_REELS_BEHAVIORAL_PROJECTION_METHOD,
        "projection_version": IG_REELS_BEHAVIORAL_PROJECTION_VERSION,
        "platform": "instagram",
        "platform_item_id": shortcode,
        "platform_item_id_kind": "shortcode",
        "canonical_url": f"https://www.instagram.com/reel/{shortcode}/",
        "candidate": candidate,
        "comments": comments,
        "transcript": {
            "source_count": len(enriched_sources),
            "sources": enriched_sources,
            "canonical_source": canonical,
            "extraction_rollup": rollup,
        },
        "extraction": {
            "source_statuses": _source_extraction_statuses(enriched_sources),
            "rollup": rollup,
        },
        "persistence_correlation": correlation,
        "behavioral_completeness": {
            "status": behavioral_status,
            "complete": behavioral_status == "complete",
            "residuals": residuals,
        },
    }


def _behavioral_status(extraction_status: str, residuals: Sequence[str]) -> str:
    if extraction_status == "complete" and residuals:
        return "complete_with_residuals"
    return extraction_status


def _candidate_projection(
    shortcode: str,
    grid_rows: Sequence[Mapping[str, Any] | Any],
    *,
    residuals: list[str],
) -> dict[str, Any] | None:
    rows = [
        _as_mapping(row)
        for row in grid_rows
        if _string_or_none(_as_mapping(row).get("content_shortcode")) == shortcode
    ]
    if not rows:
        _append_residual_once(residuals, f"ig_grid_candidate_absent:{shortcode}")
        return None

    metric_observations: list[dict[str, Any]] = []
    limitations: list[str] = []
    row_ids: list[str] = []
    packet_ids: list[str] = []
    for row in rows:
        row_id = _string_or_none(row.get("row_id"))
        if row_id is not None:
            row_ids.append(row_id)
        raw_ref = _as_mapping(row.get("raw_ref"))
        packet_id = _string_or_none(raw_ref.get("packet_id"))
        if packet_id is not None and packet_id not in packet_ids:
            packet_ids.append(packet_id)
        for limitation in _strings(row.get("selection_limitations")):
            _append_residual_once(limitations, limitation)
        for row_residual in _strings(row.get("residuals")):
            _append_residual_once(residuals, row_residual)
        join_status = _string_or_none(row.get("join_status"))
        if join_status and join_status != "joined_by_shortcode":
            _append_residual_once(limitations, f"join_status:{join_status}")
        metric_observations.append(
            _compact_dict(
                {
                    "metric": _string_or_none(row.get("metric")),
                    "posture": _string_or_none(row.get("posture")),
                    "value": _int_or_none(row.get("value")),
                    "reason": _string_or_none(row.get("reason")),
                    "chosen_source_surface": _string_or_none(row.get("chosen_source_surface")),
                    "source_surface_count_candidates": _surface_candidates(
                        row.get("source_surface_count_candidates")
                    ),
                    "capture_time": _string_or_none(row.get("capture_time")),
                    "source_visible_fields": _mapping_or_none(row.get("source_visible_fields")),
                }
            )
        )

    return {
        "platform_item_id": shortcode,
        "ranking_basis": _ranking_basis(rows),
        "metric_observations": metric_observations,
        "limitations": limitations,
        "persistence_anchors": {
            "grid_packet_ids": packet_ids,
            "grid_row_ids": row_ids,
        },
    }


def _comment_projection(
    shortcode: str,
    comment_sets: Sequence[Mapping[str, Any] | Any],
    deep_capture_transcript_records: Sequence[Mapping[str, Any] | Any],
    *,
    residuals: list[str],
) -> dict[str, Any]:
    sets = [
        _as_mapping(item)
        for item in comment_sets
        if _string_or_none(_as_mapping(item).get("reel_shortcode")) == shortcode
    ]
    deep_postures = [
        _normalise_deep_posture(_string_or_none(_as_mapping(item).get("transcript_posture")))
        for item in deep_capture_transcript_records
        if _string_or_none(_as_mapping(item).get("reel_shortcode")) == shortcode
    ]
    if not sets:
        posture = "render_unavailable" if "render_unavailable" in deep_postures else "not_attempted"
        _append_residual_once(residuals, f"ig_comments_{posture}:{shortcode}")
        return {
            "posture": posture,
            "comment_count": 0,
            "sources": [],
        }

    total = sum(_int_or_none(item.get("comment_count")) or 0 for item in sets)
    if total > 0:
        posture = "captured"
    elif "render_unavailable" in deep_postures:
        posture = "render_unavailable"
    else:
        posture = "empty"
    if posture in {"render_unavailable", "parse_failed", "blocked"}:
        _append_residual_once(residuals, f"ig_comments_{posture}:{shortcode}")

    sources: list[dict[str, Any]] = []
    for item in sets:
        record_id = _string_or_none(item.get("record_id"))
        if record_id is None:
            _append_residual_once(residuals, f"ig_comment_record_id_absent:{shortcode}")
        sources.append(
            _compact_dict(
                {
                    "source_route": "deep_capture_render",
                    "record_id": record_id,
                    "generated_at": _string_or_none(item.get("generated_at")),
                    "comment_count": _int_or_none(item.get("comment_count")) or 0,
                    "media_provenance": _mapping_or_none(item.get("media_provenance")),
                }
            )
        )

    return {
        "posture": posture,
        "comment_count": total,
        "sources": sources,
    }


def _transcript_sources(
    shortcode: str,
    standalone_audio_transcript_records: Sequence[Mapping[str, Any] | Any],
    deep_capture_transcript_records: Sequence[Mapping[str, Any] | Any],
    *,
    residuals: list[str],
) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for record in standalone_audio_transcript_records:
        source = _standalone_audio_source(shortcode, _as_mapping(record), residuals=residuals)
        if source is not None:
            sources.append(source)
    for record in deep_capture_transcript_records:
        source = _deep_capture_source(shortcode, _as_mapping(record), residuals=residuals)
        if source is not None:
            sources.append(source)
    if not sources:
        _append_residual_once(residuals, f"ig_transcript_source_absent:{shortcode}")
    return sources


def _standalone_audio_source(
    shortcode: str,
    record: Mapping[str, Any],
    *,
    residuals: list[str],
) -> dict[str, Any] | None:
    record_shortcodes = [
        value
        for value in (
            _string_or_none(record.get("shortcode")),
            _string_or_none(record.get("video_id")),
        )
        if value is not None
    ]
    mismatches = sorted({value for value in record_shortcodes if value != shortcode})
    if mismatches:
        for value in mismatches:
            _append_residual_once(residuals, f"ig_transcript_source_shortcode_mismatch:{value}")
        return None
    if not record_shortcodes:
        _append_residual_once(residuals, "ig_transcript_source_shortcode_absent:standalone_audio_packet")
        return None
    provenance = _as_mapping(record.get("provenance"))
    transcript_anchor = (
        _string_or_none(record.get("transcript_anchor"))
        or _string_or_none(provenance.get("source_packet_id"))
        or "unknown_audio_packet"
    )
    asr_record_id = _string_or_none(record.get("record_id") or record.get("asr_record_id"))
    if asr_record_id is None:
        _append_residual_once(
            residuals,
            f"ig_transcript_source_record_id_absent:standalone_audio_packet:{transcript_anchor}",
        )
    source = _base_transcript_source(
        platform_item_id=shortcode,
        transcript_anchor=transcript_anchor,
        asr_record_id=asr_record_id,
        source_route="standalone_audio_packet",
        source_status=_string_or_none(record.get("source_status")) or "complete",
        posture=_string_or_none(record.get("posture")) or "unknown",
        cue_count=_int_or_none(record.get("cue_count")) or len(_list(record.get("cues"))),
        capture_timestamp=_string_or_none(record.get("retrieval_time_utc")),
        extraction_feed_eligible=True,
    )
    source["provenance"] = _compact_dict(dict(provenance))
    return source


def _deep_capture_source(
    shortcode: str,
    record: Mapping[str, Any],
    *,
    residuals: list[str],
) -> dict[str, Any] | None:
    record_shortcode = _string_or_none(record.get("reel_shortcode"))
    if record_shortcode is None:
        _append_residual_once(
            residuals,
            f"ig_transcript_source_shortcode_absent:deep_capture_render_audio:{shortcode}",
        )
        return None
    if record_shortcode and record_shortcode != shortcode:
        _append_residual_once(residuals, f"ig_transcript_source_shortcode_mismatch:{record_shortcode}")
        return None
    asr_record_id = _string_or_none(record.get("record_id") or record.get("asr_record_id"))
    if asr_record_id is None:
        _append_residual_once(
            residuals,
            f"ig_transcript_source_record_id_absent:deep_capture_render_audio:{shortcode}",
        )
    source = _base_transcript_source(
        platform_item_id=shortcode,
        transcript_anchor=(
            _string_or_none(record.get("transcript_anchor"))
            or _string_or_none(record.get("raw_anchor"))
            or shortcode
        ),
        asr_record_id=asr_record_id,
        source_route="deep_capture_render_audio",
        source_status=_string_or_none(record.get("source_status")) or "complete",
        posture=_normalise_deep_posture(_string_or_none(record.get("transcript_posture"))),
        cue_count=_int_or_none(record.get("cue_count")) or len(_list(record.get("cues"))),
        capture_timestamp=_string_or_none(record.get("generated_at")),
        extraction_feed_eligible=True,
    )
    source["media_provenance"] = _mapping_or_none(record.get("media_provenance")) or {}
    return source


def _base_transcript_source(
    *,
    platform_item_id: str,
    transcript_anchor: str,
    asr_record_id: str | None,
    source_route: str,
    source_status: str,
    posture: str,
    cue_count: int,
    capture_timestamp: str | None,
    extraction_feed_eligible: bool,
) -> dict[str, Any]:
    source = {
        "platform": "instagram",
        "platform_item_id": platform_item_id,
        "platform_item_id_kind": "shortcode",
        "transcript_anchor": transcript_anchor,
        "asr_record_id": asr_record_id,
        "source_kind": "asr",
        "source_route": source_route,
        "source_status": source_status,
        "posture": posture,
        "cue_count": cue_count,
        "capture_timestamp": capture_timestamp,
    }
    source["transcript_source_key"] = _source_key(source)
    eligible, reason = _eligibility(source, extraction_feed_eligible=extraction_feed_eligible)
    source["extraction_eligible"] = eligible
    source["non_eligible_reason"] = reason
    return source


def _eligibility(
    source: Mapping[str, Any],
    *,
    extraction_feed_eligible: bool,
) -> tuple[bool, str | None]:
    source_status = _string_or_none(source.get("source_status"))
    posture = _string_or_none(source.get("posture"))
    cue_count = _int_or_none(source.get("cue_count")) or 0
    if source_status != "complete":
        return False, source_status or "source_incomplete"
    if posture != "transcribed":
        return False, posture or "posture_unknown"
    if cue_count <= 0:
        return False, "zero_cues"
    if not extraction_feed_eligible:
        # Retained for future source kinds; current IG transcript sources are feed-eligible.
        return False, "source_not_in_extraction_feed"
    return True, None


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
        if "source_backed_status" in result:
            out["source_backed_status"] = result.get("source_backed_status")
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
            _append_residual_once(residuals, f"ig_transcript_source_{source_status}:{source_key}")
        if posture in SOURCE_POSTURE_PROBLEMS:
            _append_residual_once(residuals, f"ig_transcript_source_{posture}:{source_key}")

        if (
            source.get("extraction_eligible") is False
            and non_eligible_reason in SOURCE_NON_ELIGIBLE_PROBLEMS
        ):
            _append_residual_once(
                residuals,
                f"ig_transcript_source_not_extraction_eligible:{source_key}",
            )
        if extraction_status in EXTRACTION_PROBLEM_STATUSES:
            _append_residual_once(residuals, f"ig_transcript_extraction_{extraction_status}:{source_key}")

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
    usable = [
        source
        for source in sources
        if _string_or_none(source.get("posture")) == "transcribed"
        and (_int_or_none(source.get("cue_count")) or 0) > 0
    ]
    if not usable:
        return None
    selected = max(usable, key=_canonical_source_rank)
    return {
        "transcript_anchor": selected.get("transcript_anchor"),
        "transcript_source_key": _source_key(selected),
        "source_kind": selected.get("source_kind"),
        "source_route": selected.get("source_route"),
        "extraction_status": selected.get("extraction_status"),
        "selection_reason": (
            "same_render_comments_transcript"
            if selected.get("source_route") == "deep_capture_render_audio"
            else "latest_standalone_audio_asr"
        ),
    }


def _source_extraction_statuses(sources: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        _compact_dict(
            {
                "transcript_source_key": _source_key(source),
                "transcript_anchor": source.get("transcript_anchor"),
                "source_route": source.get("source_route"),
                "extraction_eligible": source.get("extraction_eligible"),
                "non_eligible_reason": source.get("non_eligible_reason"),
                "extraction_status": source.get("extraction_status"),
                "extraction_record_path": source.get("extraction_record_path"),
                "extraction_error": source.get("extraction_error"),
                "source_backed_status": source.get("source_backed_status"),
            }
        )
        for source in sources
    ]


def _persistence_correlation(
    candidate: Mapping[str, Any] | None,
    comments: Mapping[str, Any],
    sources: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    candidate_anchors = _as_mapping((candidate or {}).get("persistence_anchors"))
    extraction_paths = [
        str(path)
        for source in sources
        for path in [_string_or_none(source.get("extraction_record_path"))]
        if path is not None
    ]
    return {
        "grid_packet_ids": _strings(candidate_anchors.get("grid_packet_ids")),
        "grid_row_ids": _strings(candidate_anchors.get("grid_row_ids")),
        "deep_capture_record_ids": [
            record_id
            for source in sources
            if source.get("source_route") == "deep_capture_render_audio"
            for record_id in [_string_or_none(source.get("asr_record_id"))]
            if record_id is not None
        ],
        "comment_record_ids": [
            record_id
            for source in _list(comments.get("sources"))
            for record_id in [_string_or_none(_as_mapping(source).get("record_id"))]
            if record_id is not None
        ],
        "audio_packet_ids": [
            anchor
            for source in sources
            if source.get("source_route") == "standalone_audio_packet"
            for anchor in [_string_or_none(source.get("transcript_anchor"))]
            if anchor is not None
        ],
        "transcript_source_keys": [_source_key(source) for source in sources],
        "transcript_anchors": [
            anchor
            for source in sources
            for anchor in [_string_or_none(source.get("transcript_anchor"))]
            if anchor is not None
        ],
        "extraction_record_paths": extraction_paths,
    }


def _result_for_source(
    source: Mapping[str, Any],
    *,
    exact_results: Mapping[str, Mapping[str, Any]],
    anchor_results: Mapping[str, list[Mapping[str, Any]]],
    duplicate_eligible_anchors: set[str],
) -> Mapping[str, Any] | None:
    for key in (
        _source_key(source),
        _string_or_none(source.get("transcript_source_key")),
    ):
        if key is not None and key in exact_results:
            return exact_results[key]
    anchor = _string_or_none(source.get("transcript_anchor"))
    if anchor is None:
        return None
    results = anchor_results.get(anchor, [])
    if len(results) == 1 and anchor not in duplicate_eligible_anchors:
        return results[0]
    if results:
        return {"status": "ambiguous_anchor_result"}
    return None


def _extraction_result_indexes(
    extraction_results: Sequence[Mapping[str, Any] | Any],
) -> tuple[dict[str, Mapping[str, Any]], dict[str, list[Mapping[str, Any]]]]:
    exact: dict[str, Mapping[str, Any]] = {}
    by_anchor: dict[str, list[Mapping[str, Any]]] = {}
    for item in extraction_results:
        result = _as_mapping(item)
        for key_name in ("transcript_source_key",):
            key = _string_or_none(result.get(key_name))
            if key is not None:
                exact[key] = result
        anchor = _string_or_none(result.get("anchor") or result.get("packet_id"))
        if anchor is not None:
            by_anchor.setdefault(anchor, []).append(result)
    return exact, by_anchor


def _duplicate_eligible_anchors(sources: Sequence[Mapping[str, Any]]) -> set[str]:
    seen: set[str] = set()
    duplicate: set[str] = set()
    for source in sources:
        if source.get("extraction_eligible") is not True:
            continue
        anchor = _string_or_none(source.get("transcript_anchor"))
        if anchor is None:
            continue
        if anchor in seen:
            duplicate.add(anchor)
        seen.add(anchor)
    return duplicate


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


def _source_sort_key(source: Mapping[str, Any]) -> tuple[int, str, str]:
    route = _string_or_none(source.get("source_route"))
    route_rank = 0 if route == "deep_capture_render_audio" else 1 if route == "standalone_audio_packet" else 9
    timestamp = _string_or_none(source.get("capture_timestamp")) or ""
    key = _source_key(source)
    return (route_rank, timestamp, key)


def _canonical_source_rank(source: Mapping[str, Any]) -> tuple[int, str, str]:
    route = _string_or_none(source.get("source_route"))
    route_score = 2 if route == "deep_capture_render_audio" else 1 if route == "standalone_audio_packet" else 0
    timestamp = _string_or_none(source.get("capture_timestamp")) or ""
    return (route_score, timestamp, _source_key(source))


def _ranking_basis(rows: Sequence[Mapping[str, Any]]) -> str:
    observed = {
        _string_or_none(row.get("metric"))
        for row in rows
        if _string_or_none(row.get("posture")) == "observed" and row.get("value") is not None
    }
    if "view_count" in observed:
        return "views_then_engagement"
    if observed & {"like_count", "comment_count"}:
        return "engagement"
    return "unknown_or_weak"


def _normalise_deep_posture(posture: str | None) -> str:
    if posture == "ok":
        return "transcribed"
    return posture or "unknown"


def _surface_candidates(value: Any) -> list[dict[str, Any]]:
    return [
        _compact_dict(
            {
                "source_surface": _string_or_none(candidate.get("source_surface")),
                "value": _int_or_none(candidate.get("value")),
                "raw_text": _string_or_none(candidate.get("raw_text")),
            }
        )
        for candidate in (_as_mapping(item) for item in _list(value))
    ]


def _required_shortcode(value: str) -> str:
    shortcode = _string_or_none(value)
    if not shortcode:
        raise ValueError("platform_item_id is required")
    return shortcode


def _as_mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    model_dump = getattr(value, "model_dump", None)
    if callable(model_dump):
        dumped = model_dump(mode="json")
        if isinstance(dumped, Mapping):
            return dumped
    return {}


def _mapping_or_none(value: Any) -> dict[str, Any] | None:
    mapped = _as_mapping(value)
    return dict(mapped) if mapped else None


def _list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return []


def _strings(value: Any) -> list[str]:
    return [item for item in (_string_or_none(item) for item in _list(value)) if item is not None]


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _int_or_none(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        try:
            return int(value.replace(",", "").strip())
        except ValueError:
            return None
    return None


def _compact_dict(data: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in data.items() if value not in (None, {}, [], ())}


def _append_residual_once(residuals: list[str], residual: str) -> None:
    if residual not in residuals:
        residuals.append(residual)


__all__ = [
    "IG_REELS_BEHAVIORAL_PROJECTION_METHOD",
    "IG_REELS_BEHAVIORAL_PROJECTION_VERSION",
    "project_ig_reels_behavioral_item",
]
