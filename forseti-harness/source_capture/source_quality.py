from __future__ import annotations

import json
import mimetypes
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from source_capture.models import (
    SourceCapturePacket,
    SourceCaptureSlice,
    VisibleFact,
    VisibleFactStatus,
)
from source_capture.packet_inspection import PacketConformanceReport, read_packet_leniently


SOURCE_QUALITY_REPORT_SKELETON_VERSION = "mini_god_tier_source_quality_report_skeleton_v0"
SOURCE_QUALITY_STATE_ASSEMBLER_VERSION = "source_quality_state_assembler_v0"

MINI_GOD_TIER_MET = "mini_god_tier_met"
MINI_GOD_TIER_WITH_VISIBLE_LIMITATIONS = "mini_god_tier_with_visible_limitations"
CURRENT_BODY_STANDARDIZED_ONLY = "current_body_standardized_only"
ARCHIVE_BODY_NOT_PRESERVED = "archive_body_not_preserved"
BODY_POSSESSION_NOT_PROVEN = "body_possession_not_proven"
NEEDS_SEPARATE_FIXTURE_ADMISSION_DECISION = "needs_separate_fixture_admission_decision"
VISIBLE_STOP = "visible_stop"

LIFECYCLE_STATES = {
    "scratch",
    "candidate_evidence",
    "recommended_fixture_admission",
    "separately_admitted",
}

ROW_STATUSES = {
    "planned",
    "ready_for_tool_run",
    "blocked_missing_input",
    "packet_written_needs_report",
    "reported",
}

RESULT_TOKENS = {
    MINI_GOD_TIER_MET,
    MINI_GOD_TIER_WITH_VISIBLE_LIMITATIONS,
    CURRENT_BODY_STANDARDIZED_ONLY,
    ARCHIVE_BODY_NOT_PRESERVED,
    BODY_POSSESSION_NOT_PROVEN,
    NEEDS_SEPARATE_FIXTURE_ADMISSION_DECISION,
    VISIBLE_STOP,
}

SKELETON_NON_CLAIMS = [
    "not validation",
    "not source completeness proof",
    "not fixture admission unless separately decided",
    "not Judgment scoring",
]

STATE_ASSEMBLER_NON_CLAIMS = [
    "not validation",
    "not source completeness proof",
    "not fixture admission",
    "not source discovery",
    "not runner dispatch",
    "not source acquisition",
    "not source-quality scoring",
    "not Judgment scoring",
]


def resolve_manifest_path(packet_or_manifest_path: Path) -> Path:
    if packet_or_manifest_path.is_dir():
        return packet_or_manifest_path / "manifest.json"
    return packet_or_manifest_path


def _nonconformance_stop(report: PacketConformanceReport) -> str:
    error_count = len(report.current_schema_errors)
    if report.declares_current_manifest_version:
        return (
            f"manifest declares the current schema version "
            f"({report.declared_manifest_version!r}) but does not conform to it: "
            f"{error_count} schema error(s) — possible corruption of a current-version packet"
        )
    if report.declared_manifest_version is None:
        return (
            "manifest does not declare a string manifest_version; "
            f"inspected leniently against the current schema and found {error_count} "
            "non-conformance(s) — malformed or unknown-version packet, not off-version evidence"
        )
    return (
        f"manifest declares a non-current schema version "
        f"({report.declared_manifest_version!r}); inspected leniently against the current "
        f"schema and found {error_count} non-conformance(s) — off-version evidence, not corruption"
    )


def build_source_quality_report_skeleton(
    *,
    packet_or_manifest_path: Path,
    source_id: str,
    source_language_anchors: Sequence[str] = (),
    coverage_or_drift_note: str | None = None,
    lifecycle_state: str = "scratch",
    lifecycle_decision_reference: str | None = None,
) -> dict[str, Any]:
    if lifecycle_state not in LIFECYCLE_STATES:
        allowed = ", ".join(sorted(LIFECYCLE_STATES))
        raise ValueError(f"lifecycle_state must be one of: {allowed}")
    if lifecycle_state == "separately_admitted" and _missing_lifecycle_decision_reference(lifecycle_decision_reference):
        raise ValueError("separately_admitted requires lifecycle_decision_reference")

    manifest_path = resolve_manifest_path(packet_or_manifest_path)
    if not manifest_path.exists():
        raise ValueError(f"manifest not found: {manifest_path}")

    packet_dir = manifest_path.parent
    packet = SourceCapturePacket.model_validate(json.loads(manifest_path.read_text(encoding="utf-8")))
    metadata_files = _read_metadata_files(packet_dir, packet)
    body = _detect_best_body(packet, metadata_files)
    provenance = _build_provenance(packet, body, metadata_files)
    visible_limitations = _build_visible_limitations(packet, body, metadata_files)
    suggested_token, suggested_reason = _suggest_result_token(packet, body)
    operator_completion_required = _operator_completion_required(
        source_language_anchors=source_language_anchors,
        coverage_or_drift_note=coverage_or_drift_note,
    )

    return {
        "mini_god_tier_source_quality_report_skeleton": {
            "skeleton_version": SOURCE_QUALITY_REPORT_SKELETON_VERSION,
            "source_id": source_id,
            "packet_path": str(packet_dir),
            "suggested_result_token": suggested_token,
            "suggested_result_token_reason": suggested_reason,
            "result_token_finalization": "operator_review_required",
            "best_in_bound_body": body["report"],
            "provenance": provenance,
            "source_language_anchors": (
                list(source_language_anchors)
                if source_language_anchors
                else ["operator_fill_required: helper did not infer source-language anchors from raw body"]
            ),
            "coverage_or_drift_note": coverage_or_drift_note
            or "operator_fill_required: helper did not infer coverage or drift relationship",
            "visible_limitations": visible_limitations
            or ["none_observed_in_manifest; operator_review_required still applies"],
            "operator_completion_required": operator_completion_required,
            "lifecycle_state": lifecycle_state,
            "lifecycle_decision_reference": lifecycle_decision_reference or "none",
            "non_claims": SKELETON_NON_CLAIMS,
        }
    }


def build_source_quality_state_census(
    *,
    rows: Sequence[Mapping[str, Any]],
    base_path: Path | None = None,
) -> dict[str, Any]:
    if not rows:
        raise ValueError("at least one source-quality row is required")

    assembled_rows = [
        _assemble_source_quality_row(row=row, row_index=index, base_path=base_path)
        for index, row in enumerate(rows, start=1)
    ]
    return {
        "source_quality_state_assembler": {
            "assembler_version": SOURCE_QUALITY_STATE_ASSEMBLER_VERSION,
            "row_count": len(assembled_rows),
            "rows": assembled_rows,
            "census": _build_state_census(assembled_rows),
            "non_claims": STATE_ASSEMBLER_NON_CLAIMS,
        }
    }


def _detect_best_body(
    packet: SourceCapturePacket,
    metadata_files: dict[str, Any],
) -> dict[str, Any]:
    preserved_by_id = {item.file_id: item for item in packet.preserved_files}
    snapshot_slice = _find_slice(packet, "archive_snapshot_body")
    if snapshot_slice is not None:
        body_file = _first_non_metadata_file(snapshot_slice, preserved_by_id)
        if body_file is not None:
            snapshot_time = _selected_snapshot_field(metadata_files, "timestamp") or _source_time(snapshot_slice)
            return {
                "kind": "preserved",
                "source_slice": snapshot_slice,
                "preserved_file": body_file,
                "report": {
                    "posture": "preserved",
                    "preserved_body_path": body_file.relative_packet_path,
                    "sha256": body_file.sha256,
                    "byte_count": body_file.size_bytes,
                    "source_or_snapshot_time": snapshot_time,
                },
            }

    generic_body_slice, generic_body_file = _first_body_file(packet, preserved_by_id)
    if generic_body_slice is not None and generic_body_file is not None:
        return {
            "kind": "preserved",
            "source_slice": generic_body_slice,
            "preserved_file": generic_body_file,
            "report": {
                "posture": "preserved",
                "preserved_body_path": generic_body_file.relative_packet_path,
                "sha256": generic_body_file.sha256,
                "byte_count": generic_body_file.size_bytes,
                "source_or_snapshot_time": _source_time(generic_body_slice),
            },
        }

    if packet.source_surface == "archive_org_wayback" and _has_archive_availability_metadata(packet):
        return {
            "kind": "metadata_only",
            "source_slice": _find_slice(packet, "archive_availability"),
            "preserved_file": None,
            "report": {
                "posture": "metadata_only",
                "preserved_body_path": "none",
                "sha256": "none",
                "byte_count": "none",
                "source_or_snapshot_time": _archive_metadata_time_summary(metadata_files),
            },
        }

    return {
        "kind": "not_preserved",
        "source_slice": None,
        "preserved_file": None,
        "report": {
            "posture": "not_preserved",
            "preserved_body_path": "none",
            "sha256": "none",
            "byte_count": "none",
            "source_or_snapshot_time": "unknown_with_reason: no preserved body file identified",
        },
    }


def _missing_lifecycle_decision_reference(value: str | None) -> bool:
    if value is None:
        return True
    normalized = value.strip()
    return not normalized or normalized.lower() == "none"


def _build_provenance(
    packet: SourceCapturePacket,
    body: dict[str, Any],
    metadata_files: dict[str, Any],
) -> dict[str, str]:
    body_slice = body.get("source_slice")
    final_locator = _fact_value(body_slice.locator) if body_slice is not None else "none"
    http_metadata = _best_http_metadata(metadata_files, prefer_snapshot=body["kind"] == "preserved")

    return {
        "original_locator": _fact_value(packet.source_locator),
        "final_or_snapshot_locator": http_metadata.get("final_url") or final_locator,
        "access_status": _fact_value(packet.access_posture),
        "content_type": http_metadata.get("content_type")
        or _content_type_from_preserved_body(body)
        or "unknown_with_reason: content type not present in manifest metadata or inferable file extension",
        "capture_time": http_metadata.get("capture_timestamp") or _fact_value(packet.timing.capture_time),
    }


def _build_visible_limitations(
    packet: SourceCapturePacket,
    body: dict[str, Any],
    metadata_files: dict[str, Any],
) -> list[str]:
    limitations: list[str] = []
    limitations.extend(packet.limitations)
    limitations.extend(f"warning: {item}" for item in packet.warnings)
    for source_slice in packet.source_slices:
        limitations.extend(source_slice.limitations)
        limitations.extend(f"slice warning ({source_slice.slice_id}): {item}" for item in source_slice.warning_notes)

    if body["kind"] == "metadata_only":
        limitations.append("Archive availability metadata was preserved, but no archive snapshot body is referenced by source_slices.")
        selected_snapshot = _availability_field(metadata_files, "selected_snapshot")
        if selected_snapshot is None:
            limitations.append("Archive availability metadata selected_snapshot is null.")
        snapshot_count = _availability_field(metadata_files, "snapshot_count")
        if snapshot_count is not None:
            limitations.append(f"Archive availability metadata snapshot_count is {snapshot_count}; this is not archive completeness proof.")

    if packet.source_surface == "archive_org_wayback":
        limitations.append("Archive.org snapshot_count, when present, reflects collapse=digest availability rows, not archive completeness proof.")

    for label, fact in (
        ("archive_history_posture", packet.archive_history_posture),
        ("media_modality_posture", packet.media_modality_posture),
    ):
        if fact.status == VisibleFactStatus.NOT_ATTEMPTED:
            limitations.append(f"{label}: not_attempted - {fact.reason}")
        elif fact.status == VisibleFactStatus.UNKNOWN_WITH_REASON:
            limitations.append(f"{label}: unknown_with_reason - {fact.reason}")

    return _dedupe(limitations)


def _suggest_result_token(packet: SourceCapturePacket, body: dict[str, Any]) -> tuple[str, str]:
    if body["kind"] == "metadata_only":
        return (
            ARCHIVE_BODY_NOT_PRESERVED,
            "Archive availability exists, but the packet does not preserve an inspectable archive body.",
        )
    if body["kind"] != "preserved":
        return (
            BODY_POSSESSION_NOT_PROVEN,
            "The packet manifest does not identify a preserved source body or body-equivalent.",
        )
    return (
        MINI_GOD_TIER_WITH_VISIBLE_LIMITATIONS,
        "A source body is preserved, but manifest-only evidence cannot finalize all Mini God-Tier criteria or auto-claim mini_god_tier_met.",
    )


def _operator_completion_required(
    *,
    source_language_anchors: Sequence[str],
    coverage_or_drift_note: str | None,
) -> list[str]:
    required: list[str] = ["review suggested_result_token against the Mini God-Tier profile"]
    if not source_language_anchors:
        required.append("supply bounded source-language anchors or not_applicable_with_reason")
    if not coverage_or_drift_note:
        required.append("supply coverage_or_drift_note")
    return required


def _find_slice(packet: SourceCapturePacket, slice_id: str) -> SourceCaptureSlice | None:
    for source_slice in packet.source_slices:
        if source_slice.slice_id == slice_id:
            return source_slice
    return None


def _first_body_file(
    packet: SourceCapturePacket,
    preserved_by_id: dict[str, Any],
) -> tuple[SourceCaptureSlice | None, Any | None]:
    for source_slice in packet.source_slices:
        body_file = _first_non_metadata_file(source_slice, preserved_by_id)
        if body_file is not None:
            return source_slice, body_file
    return None, None


def _first_non_metadata_file(
    source_slice: SourceCaptureSlice,
    preserved_by_id: dict[str, Any],
) -> Any | None:
    for file_id in source_slice.preserved_file_ids:
        preserved_file = preserved_by_id[file_id]
        relative_path = preserved_file.relative_packet_path.lower()
        if not _is_metadata_path(relative_path):
            return preserved_file
    return None


def _is_metadata_path(relative_path: str) -> bool:
    return relative_path.endswith("_metadata.json") or relative_path.endswith("metadata.json")


def _has_archive_availability_metadata(packet: SourceCapturePacket) -> bool:
    availability_slice = _find_slice(packet, "archive_availability")
    if availability_slice is None:
        return False
    return bool(availability_slice.preserved_file_ids)


def _read_metadata_files(packet_dir: Path, packet: SourceCapturePacket) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    for preserved_file in packet.preserved_files:
        relative_path = preserved_file.relative_packet_path
        if not _is_metadata_path(relative_path.lower()):
            continue
        path = packet_dir / relative_path
        if not path.exists():
            continue
        try:
            metadata[relative_path] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            metadata[relative_path] = {"parse_error": f"could not parse {relative_path}"}
    return metadata


def _best_http_metadata(metadata_files: dict[str, Any], *, prefer_snapshot: bool) -> dict[str, Any]:
    if prefer_snapshot:
        for data in metadata_files.values():
            nested = data.get("snapshot_body_http_metadata") if isinstance(data, dict) else None
            if isinstance(nested, dict):
                return nested
    for data in metadata_files.values():
        if not isinstance(data, dict):
            continue
        if "content_type" in data or "final_url" in data:
            return data
        nested = data.get("availability_http_metadata")
        if isinstance(nested, dict):
            return nested
    return {}


def _content_type_from_preserved_body(body: dict[str, Any]) -> str | None:
    preserved_file = body.get("preserved_file")
    relative_path = getattr(preserved_file, "relative_packet_path", None)
    if not relative_path:
        return None

    guessed_type, _ = mimetypes.guess_type(relative_path)
    if guessed_type is None:
        return None
    return f"inferred_from_extension: {guessed_type}"


def _selected_snapshot_field(metadata_files: dict[str, Any], field: str) -> str | None:
    for data in metadata_files.values():
        if not isinstance(data, dict):
            continue
        snapshot = data.get("selected_snapshot")
        if isinstance(snapshot, dict) and snapshot.get(field) is not None:
            return str(snapshot[field])
    return None


def _availability_field(metadata_files: dict[str, Any], field: str) -> Any | None:
    for data in metadata_files.values():
        if isinstance(data, dict) and field in data:
            return data[field]
    return None


def _archive_metadata_time_summary(metadata_files: dict[str, Any]) -> str:
    selected_snapshot = _availability_field(metadata_files, "selected_snapshot")
    if selected_snapshot:
        return f"selected snapshot {selected_snapshot}"
    snapshots = _availability_field(metadata_files, "snapshots")
    if isinstance(snapshots, list) and snapshots:
        timestamps = [item.get("timestamp") for item in snapshots if isinstance(item, dict) and item.get("timestamp")]
        if timestamps:
            return f"earliest observed availability timestamp {min(timestamps)}; no selected snapshot"
    return "unknown_with_reason: no archive snapshot selected"


def _source_time(source_slice: SourceCaptureSlice) -> str:
    # AR-03: source/snapshot time must NOT be derived from cutoff_posture -- a
    # posture is not a time. Once cutoff_posture is a closed vocabulary
    # ({pre_cutoff, post_cutoff, mixed, unknown}), reading it here would surface a
    # posture value as a timestamp (e.g. source_or_snapshot_time: "pre_cutoff").
    # Re-source from real timing fields only; otherwise explicit unknown.
    for fact in (
        source_slice.timing.source_edit_or_version,
        source_slice.timing.source_publication_or_event,
    ):
        if fact.status == VisibleFactStatus.KNOWN and fact.value:
            return fact.value
    return "unknown_with_reason: packet did not carry source or snapshot timing as a known fact"


def _fact_value(fact: VisibleFact) -> str:
    if fact.status == VisibleFactStatus.KNOWN and fact.value:
        return fact.value
    return f"{fact.status.value}: {fact.reason}"


def _assemble_source_quality_row(
    *,
    row: Mapping[str, Any],
    row_index: int,
    base_path: Path | None,
) -> dict[str, Any]:
    source_id = _row_text(row, "source_id", default=f"row_{row_index}_missing_source_id")
    row_status = _row_text(row, "row_status", default="missing")
    result_token = _row_text(row, "result_token", default="none")
    lifecycle_state = _row_text(row, "packet_lifecycle", default=_row_text(row, "lifecycle_state", default="scratch"))
    visible_stops = _validate_row_state(
        row_status=row_status,
        result_token=result_token,
        lifecycle_state=lifecycle_state,
    )
    packet_reference = _row_text(row, "packet_path", default=_row_text(row, "manifest_path", default="none"))

    assembled = {
        "row_index": row_index,
        "source_id": source_id,
        "case_or_slot": _row_text(row, "case_or_slot", default="unknown_with_reason: not supplied"),
        "row_status": row_status,
        "row_status_valid": row_status in ROW_STATUSES,
        "operator_reported_result_token": result_token,
        "operator_reported_result_token_valid": result_token == "none" or result_token in RESULT_TOKENS,
        "packet_lifecycle": lifecycle_state,
        "packet_lifecycle_valid": lifecycle_state in LIFECYCLE_STATES,
        "packet_reference": packet_reference,
        "manifest_path": "none",
        "packet_state": "not_cited",
        "helper_state": "not_invoked",
        "suggested_result_token": "none",
        "result_token_finalization": "operator_review_required",
        "operator_completion_required": [
            "supply existing packet path before assembler can inspect packet state"
        ],
        "visible_limitations": [],
        "visible_stops": visible_stops,
        "mini_god_tier_source_quality_report_skeleton": None,
    }

    if packet_reference == "none":
        assembled["visible_stops"].append(
            "no packet_path or manifest_path cited; assembler did not run Source Capture tools"
        )
        return assembled

    manifest_path = resolve_manifest_path(_resolve_input_path(packet_reference, base_path=base_path))
    assembled["manifest_path"] = str(manifest_path)
    if not manifest_path.exists():
        assembled["packet_state"] = "manifest_missing"
        assembled["visible_stops"].append(f"manifest not found: {manifest_path}")
        return assembled

    # Lenient inspection pre-check (Phase-1 schema-evolution slice). Distinguish a
    # parseable-but-off-schema manifest (an honest older version, or a current-version
    # corruption) from a genuinely unreadable one. Reuses the strict model as the single
    # source of truth (M2) and returns a distinct report — never a packet.
    try:
        conformance = read_packet_leniently(manifest_path)
    except Exception as exc:
        assembled["packet_state"] = "manifest_uninspectable"
        assembled["helper_state"] = "helper_failed"
        assembled["visible_stops"].append(f"manifest could not be read: {exc}")
        assembled["operator_completion_required"] = [
            "repair packet reference, manifest, or lifecycle fields before operator review"
        ]
        return assembled

    if not conformance.conforms_to_current_schema:
        assembled["packet_state"] = "manifest_nonconforming"
        assembled["helper_state"] = "not_invoked"
        assembled["packet_conformance"] = conformance.model_dump(mode="json")
        assembled["visible_stops"].append(_nonconformance_stop(conformance))
        assembled["operator_completion_required"] = [
            "packet does not conform to the current Source Capture schema; re-capture under "
            "the current schema or review as off-version evidence before operator review"
        ]
        return assembled

    try:
        skeleton_wrapper = build_source_quality_report_skeleton(
            packet_or_manifest_path=manifest_path,
            source_id=source_id,
            source_language_anchors=_row_string_list(row, "source_language_anchors"),
            coverage_or_drift_note=_row_optional_text(row, "coverage_or_drift_note"),
            lifecycle_state=lifecycle_state,
            lifecycle_decision_reference=_row_optional_text(row, "lifecycle_decision_reference"),
        )
    except Exception as exc:
        assembled["packet_state"] = "manifest_uninspectable"
        assembled["helper_state"] = "helper_failed"
        assembled["visible_stops"].append(f"source-quality skeleton helper failed: {exc}")
        assembled["operator_completion_required"] = [
            "repair packet reference, manifest, or lifecycle fields before operator review"
        ]
        return assembled

    skeleton = skeleton_wrapper["mini_god_tier_source_quality_report_skeleton"]
    assembled["packet_state"] = "manifest_inspectable"
    assembled["helper_state"] = "skeleton_built"
    assembled["suggested_result_token"] = skeleton["suggested_result_token"]
    assembled["result_token_finalization"] = skeleton["result_token_finalization"]
    assembled["operator_completion_required"] = list(skeleton["operator_completion_required"])
    assembled["visible_limitations"] = list(skeleton["visible_limitations"])
    assembled["mini_god_tier_source_quality_report_skeleton"] = skeleton
    return assembled


def _validate_row_state(
    *,
    row_status: str,
    result_token: str,
    lifecycle_state: str,
) -> list[str]:
    visible_stops: list[str] = []
    if row_status not in ROW_STATUSES:
        visible_stops.append(f"row_status not recognized by queue template: {row_status}")
    if result_token != "none" and result_token not in RESULT_TOKENS:
        visible_stops.append(f"result_token not recognized by Mini God-Tier profile: {result_token}")
    if lifecycle_state not in LIFECYCLE_STATES:
        visible_stops.append(f"packet_lifecycle not recognized by Mini God-Tier profile: {lifecycle_state}")
    return visible_stops


def _build_state_census(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    suggested_tokens = [
        row["suggested_result_token"]
        for row in rows
        if row["suggested_result_token"] != "none"
    ]
    return {
        "row_status_counts": dict(Counter(row["row_status"] for row in rows)),
        "packet_state_counts": dict(Counter(row["packet_state"] for row in rows)),
        "helper_state_counts": dict(Counter(row["helper_state"] for row in rows)),
        "suggested_result_token_counts": dict(Counter(suggested_tokens)),
        "operator_finalization_required_count": sum(
            1 for row in rows if row["result_token_finalization"] == "operator_review_required"
        ),
        "visible_stop_count": sum(1 for row in rows if row["visible_stops"]),
        "rows_with_visible_limitations_count": sum(1 for row in rows if row["visible_limitations"]),
    }


def _resolve_input_path(value: str, *, base_path: Path | None) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    if base_path is not None:
        return base_path / path
    return path


def _row_text(row: Mapping[str, Any], key: str, *, default: str) -> str:
    value = row.get(key)
    if value is None:
        return default
    text = str(value).strip()
    return text or default


def _row_optional_text(row: Mapping[str, Any], key: str) -> str | None:
    value = row.get(key)
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _row_string_list(row: Mapping[str, Any], key: str) -> list[str]:
    value = row.get(key)
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return [str(item).strip() for item in value if str(item).strip()]
    raise ValueError(f"{key} must be a string or list of strings")


def _dedupe(items: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped
