"""Stitch existing Capture artifacts through ECR receipts into CleaningPacket."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Sequence

from pydantic import ValidationError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cleaning.models import (  # noqa: E402
    CleaningDerivedRecordRef,
    CleaningEcrRef,
    CleaningInputGrain,
    CleaningInputHandle,
    CleaningPacket,
    CleaningPreservationCheck,
    CleaningProjectionRef,
    CleaningRawAnchor,
    CleaningRuleScope,
    CleaningTransform,
    CleaningTransformClass,
    CleaningTransformLedgerEntry,
)
from cleaning.projection import cleaning_input_handles_from_projection_rows  # noqa: E402
from data_lake.root import DataLakeRoot  # noqa: E402
from ecr.deriver import (  # noqa: E402
    derive_identity_postures,
    derive_inspectability_postures,
    derive_source_visibility_postures,
    derive_timing_postures,
)
from ecr.models import (  # noqa: E402
    ECR_SOURCE_SIDE_RECEIPT_SCHEMA_VERSION,
    ECR_SOURCE_SIDE_REF_KIND,
    EcrSourceSideReceipt,
    EcrSourceSideReceiptArtifact,
)
from harness_utils import hash_file, utc_now_z  # noqa: E402
from source_capture.models import PreservedFile, SourceCapturePacket  # noqa: E402
from source_capture.ig_projection import IgCreatorMomentumProjectionPacket  # noqa: E402
from source_capture.reddit_consolidation import (  # noqa: E402
    REDDIT_THREAD_CONSOLIDATION_SCHEMA_VERSION,
)
from source_capture.retail_pdp_projection import RetailPdpProjectionPacket  # noqa: E402


ECR_OUTPUT_NAME = "ecr_source_side_receipts.json"
CLEANING_OUTPUT_NAME = "cleaning_packet.json"
SUMMARY_OUTPUT_NAME = "smoke_summary.json"

ECR_REF_KIND = ECR_SOURCE_SIDE_REF_KIND

NON_CLAIMS = [
    "not_capture_execution",
    "not_crawler",
    "not_production_acceptance",
    "not_proof_run_readiness",
    "not_judgment_scoring",
    "not_cleaning_semantic_transform",
    "not_capture_quality",
    "not_content_validity",
]

_ASR_LANE = "transcript_asr"
# Completion lane carrying the transcript record set's derivation-time content sha256 (see
# source_capture/transcript/asr_packet.py). A record written via the new append_record_set path has
# this marker; a legacy append_record record does not.
_ASR_COMPLETION_LANE = "transcript_asr__set"
# hash_basis tags: which integrity guarantee the anchor.sha256 carries.
_HASH_BASIS_MARKER = "derived_record_marker_sha256"  # derivation-time commitment (new records)
_HASH_BASIS_BYTES = "derived_record_bytes"  # stitch-time fallback (legacy markerless records, #405)

CAPTURE_VALIDITY_NOT_SUPPORTED_REASON = "capture_validity_not_supported"
INSTAGRAM_STRUCTURE_NOT_PRESERVED_REASON = "instagram_structure_not_preserved"
RETAIL_STRUCTURE_NOT_PRESERVED_REASON = "retail_structure_not_preserved"
SOURCE_STRUCTURE_NOT_PRESERVED_REASON = "source_structure_not_preserved"
INSTAGRAM_RAW_PULL_TRIGGER_PREFIX = "inspect_raw_before_instagram_use"
RETAIL_RAW_PULL_TRIGGER_PREFIX = "inspect_raw_before_retail_use"

_RETAIL_TRANSFORM_CONTEXT_ROW_KINDS = frozenset({"retail_pdp_product"})
_RETAIL_TRANSFORM_METADATA_FIELDS = frozenset(
    {
        "archive_history_posture",
        "capture_time",
        "currency_pin",
        "cutoff_posture",
        "locale_pin",
        "parse_status",
        "parsed_type",
        "retailer",
        "series_id",
        "slice_locator",
        "source_family",
        "source_locator",
        "source_surface",
        "script_index",
        "structured_json_kind",
        "variant_pin",
    }
)


def run_capture_ecr_cleaning_smoke(
    smoke_manifest_path: Path,
    output_dir: Path,
    *,
    include_cleaning_transform_smoke: bool = False,
    data_root: DataLakeRoot | None = None,
) -> dict[str, str]:
    """Build smoke outputs from already-captured packet/projection artifacts.

    ``data_root`` (injected, optional) supplies lake read access for lake-resident sources --
    ``youtube_asr`` audio packets and their derived transcript records. It is None for the
    packet-dir-only families (retail/reddit/instagram/youtube captions); a ``youtube_asr``
    entry with no ``data_root`` fails closed (no silent skip).
    """

    manifest_path = smoke_manifest_path.resolve()
    manifest = _load_json_object(manifest_path, "smoke manifest")
    manifest_dir = manifest_path.parent

    retail_entries = _entry_list(manifest, "retail")
    reddit_entries = _entry_list(manifest, "reddit")
    instagram_entries = _entry_list(manifest, "instagram")
    youtube_entries = _entry_list(manifest, "youtube")
    youtube_asr_entries = _entry_list(manifest, "youtube_asr")
    if (
        not retail_entries
        and not reddit_entries
        and not instagram_entries
        and not youtube_entries
        and not youtube_asr_entries
    ):
        raise ValueError(
            "smoke manifest must name at least one retail, reddit, instagram, youtube, "
            "or youtube_asr source"
        )
    if youtube_asr_entries and data_root is None:
        # Fail closed: a derived-record (ASR) source needs the lake to load the audio packet and
        # resolve the transcript record. Never silently skip a named source.
        raise ValueError(
            "smoke manifest names youtube_asr source(s) but no data_root was injected; "
            "a derived-record source requires lake read access (fail-closed)."
        )

    output_dir = output_dir.resolve()
    output_paths = {
        "ecr_source_side_receipts": output_dir / ECR_OUTPUT_NAME,
        "cleaning_packet": output_dir / CLEANING_OUTPUT_NAME,
        "smoke_summary": output_dir / SUMMARY_OUTPUT_NAME,
    }
    existing_outputs = [path for path in output_paths.values() if path.exists()]
    if existing_outputs:
        raise ValueError(
            "smoke output already exists: "
            + ", ".join(str(path) for path in existing_outputs)
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    generated_at = utc_now_z()
    handles: list[CleaningInputHandle] = []
    receipts: list[EcrSourceSideReceipt] = []
    source_summaries: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    transform_candidates: list[dict[str, str]] = []

    for index, entry in enumerate(retail_entries, start=1):
        result = _process_retail_entry(
            entry=entry,
            index=index,
            manifest_dir=manifest_dir,
            findings=findings,
        )
        handles.extend(result["handles"])
        transform_candidates.extend(result["transform_candidates"])
        receipts.append(result["ecr_receipt"])
        source_summaries.append(result["source_summary"])

    for index, entry in enumerate(reddit_entries, start=1):
        result = _process_reddit_entry(
            entry=entry,
            index=index,
            manifest_dir=manifest_dir,
            findings=findings,
        )
        handles.extend(result["handles"])
        receipts.append(result["ecr_receipt"])
        source_summaries.append(result["source_summary"])

    for index, entry in enumerate(instagram_entries, start=1):
        result = _process_instagram_entry(
            entry=entry,
            index=index,
            manifest_dir=manifest_dir,
            findings=findings,
        )
        handles.extend(result["handles"])
        receipts.append(result["ecr_receipt"])
        source_summaries.append(result["source_summary"])

    for index, entry in enumerate(youtube_entries, start=1):
        result = _process_youtube_entry(
            entry=entry,
            index=index,
            manifest_dir=manifest_dir,
            findings=findings,
        )
        handles.extend(result["handles"])
        receipts.append(result["ecr_receipt"])
        source_summaries.append(result["source_summary"])

    for index, entry in enumerate(youtube_asr_entries, start=1):
        result = _process_youtube_asr_entry(
            entry=entry,
            index=index,
            data_root=data_root,
            findings=findings,
        )
        handles.extend(result["handles"])
        receipts.append(result["ecr_receipt"])
        source_summaries.append(result["source_summary"])

    transform_ledger = (
        _cleaning_transform_smoke_entries(transform_candidates)
        if include_cleaning_transform_smoke
        else []
    )
    cleaning_packet = CleaningPacket(handles=handles, transform_ledger=transform_ledger)
    cleaning_payload = cleaning_packet.model_dump(mode="json")

    ecr_payload = EcrSourceSideReceiptArtifact(
        schema_version=ECR_SOURCE_SIDE_RECEIPT_SCHEMA_VERSION,
        generated_at=generated_at,
        receipts=receipts,
        non_claims=NON_CLAIMS,
    ).model_dump(mode="json")

    summary_payload = {
        "schema_version": "capture_ecr_cleaning_smoke_summary_v0",
        "generated_at": generated_at,
        "run_id": manifest.get("run_id"),
        "counts": {
            "retail_sources": len(retail_entries),
            "reddit_sources": len(reddit_entries),
            "instagram_sources": len(instagram_entries),
            "youtube_sources": len(youtube_entries),
            "youtube_asr_sources": len(youtube_asr_entries),
            "ecr_receipts": len(receipts),
            "cleaning_handles": len(cleaning_packet.handles),
            "cleaning_transform_entries": len(cleaning_packet.transform_ledger),
        },
        "cleaning_transform_smoke_enabled": include_cleaning_transform_smoke,
        "sources": source_summaries,
        "findings": findings,
        "output_paths": {key: str(path) for key, path in output_paths.items()},
        "non_claims": NON_CLAIMS,
    }

    _write_json(output_paths["ecr_source_side_receipts"], ecr_payload)
    _write_json(output_paths["cleaning_packet"], cleaning_payload)
    _write_json(output_paths["smoke_summary"], summary_payload)

    return {key: str(path) for key, path in output_paths.items()}


def _process_retail_entry(
    *,
    entry: dict[str, Any],
    index: int,
    manifest_dir: Path,
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    retailer = _optional_text(entry, "retailer") or f"retail_{index}"
    source_label = f"retail:{retailer}"
    packet_dir = _resolve_manifest_path(manifest_dir, entry, "packet_dir")
    projection_path = _resolve_manifest_path(manifest_dir, entry, "projection_json")

    packet = _load_packet(packet_dir)
    projection = RetailPdpProjectionPacket.model_validate(
        _load_json_object(projection_path, f"{source_label} projection")
    )
    if projection.packet_id != packet.packet_id:
        raise ValueError(
            f"{source_label} projection packet_id {projection.packet_id!r} "
            f"does not match packet {packet.packet_id!r}"
        )

    ecr_receipt, ecr_ref = _derive_ecr_receipt(
        packet=packet,
        packet_dir=packet_dir,
        source_label=source_label,
    )

    capture_validity_reasons = _retail_capture_validity_reasons(
        packet_dir=packet_dir,
        packet=packet,
        projection=projection,
    )
    capture_validity_supported = not capture_validity_reasons
    structure_preserved = bool(projection.loss_ledger.structure_preserved)
    handle_trace_notes = _retail_handle_trace_notes(
        capture_validity_reasons=capture_validity_reasons,
        structure_preserved=structure_preserved,
        projection_residuals=projection.residuals,
    )

    base_handles = cleaning_input_handles_from_projection_rows(
        source_family=packet.source_family,
        source_surface=packet.source_surface,
        projection_packet=projection,
        handle_id_prefix=f"retail:{_handle_token(retailer)}:{packet.packet_id}",
    )
    _verify_retail_projection_anchors(
        packet_dir=packet_dir,
        packet=packet,
        projection=projection,
        source_label=source_label,
        findings=findings,
    )
    handles: list[CleaningInputHandle] = []
    for handle in base_handles:
        handle_payload = handle.model_dump(mode="json")
        handles.append(
            CleaningInputHandle.model_validate(
                {
                    **handle_payload,
                    "ecr_ref": ecr_ref.model_dump(mode="json"),
                    "residuals": _dedupe_preserve_order(
                        [*handle_payload.get("residuals", []), *handle_trace_notes["residuals"]]
                    ),
                    "warnings": _dedupe_preserve_order(
                        [*handle_payload.get("warnings", []), *handle_trace_notes["warnings"]]
                    ),
                    "raw_pull_triggers": _dedupe_preserve_order(
                        [
                            *handle_payload.get("raw_pull_triggers", []),
                            *handle_trace_notes["raw_pull_triggers"],
                        ]
                    ),
                }
            )
        )
    if not capture_validity_supported:
        findings.append(
            {
                "code": "retail_capture_validity_not_supported",
                "source_label": source_label,
                "packet_id": packet.packet_id,
                "reasons": capture_validity_reasons,
            }
        )

    if not structure_preserved:
        findings.append(
            {
                "code": "retail_structure_not_preserved",
                "source_label": source_label,
                "packet_id": packet.packet_id,
                "residuals": projection.residuals,
            }
        )

    return {
        "handles": handles,
        "ecr_receipt": ecr_receipt,
        "source_summary": {
            "source_label": source_label,
            "packet_id": packet.packet_id,
            "packet_dir": str(packet_dir),
            "projection_json": str(projection_path),
            "handle_count": len(handles),
            "projection_method": projection.projection_method,
            "projection_version": projection.projection_version,
            "structure_preserved": structure_preserved,
            "capture_validity_supported": capture_validity_supported,
            "capture_validity_reasons": capture_validity_reasons,
        },
        "transform_candidates": _retail_transform_candidates(
            handles=handles,
            rows=projection.rows,
        ),
    }


def _process_reddit_entry(
    *,
    entry: dict[str, Any],
    index: int,
    manifest_dir: Path,
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    source_label = _optional_text(entry, "source_label") or f"reddit:{index}"
    packet_dir = _resolve_manifest_path(manifest_dir, entry, "packet_dir")
    consolidation_path = _resolve_manifest_path(manifest_dir, entry, "consolidation_json")

    packet = _load_packet(packet_dir)
    artifact = _load_json_object(consolidation_path, f"{source_label} consolidation")
    consolidation = artifact.get("reddit_thread_consolidation")
    if not isinstance(consolidation, dict):
        raise ValueError(f"{source_label} consolidation missing reddit_thread_consolidation")

    source_packet = consolidation.get("source_packet")
    if not isinstance(source_packet, dict):
        raise ValueError(f"{source_label} consolidation missing source_packet")
    if source_packet.get("packet_id") != packet.packet_id:
        raise ValueError(
            f"{source_label} consolidation packet_id {source_packet.get('packet_id')!r} "
            f"does not match packet {packet.packet_id!r}"
        )

    raw_file_id = _required_text(source_packet, "raw_html_file_id", source_label)
    expected_relative_path = _required_text(
        source_packet, "raw_html_relative_packet_path", source_label
    )
    expected_sha256 = _required_text(source_packet, "raw_html_sha256", source_label)
    raw_file, raw_path = _verified_preserved_file(
        packet_dir=packet_dir,
        packet=packet,
        file_id=raw_file_id,
        expected_relative_packet_path=expected_relative_path,
        expected_sha256=expected_sha256,
    )
    raw_html_bytes = raw_path.read_bytes()
    slice_id = _slice_id_for_file(packet, raw_file_id)

    ecr_receipt, ecr_ref = _derive_ecr_receipt(
        packet=packet,
        packet_dir=packet_dir,
        source_label=source_label,
    )

    handles: list[CleaningInputHandle] = []
    thread = consolidation.get("thread")
    post = consolidation.get("post")
    thread_id = _optional_text(thread if isinstance(thread, dict) else {}, "thread_id")
    if isinstance(post, dict):
        handles.append(
            _reddit_handle(
                packet=packet,
                source_label=source_label,
                row_id="post",
                row_kind="post",
                fullname_prefix="t3",
                fullname_id=thread_id,
                raw_file=raw_file,
                slice_id=slice_id,
                raw_html_bytes=raw_html_bytes,
                ecr_ref=ecr_ref,
                findings=findings,
            )
        )

    comments = consolidation.get("comments", [])
    if comments is None:
        comments = []
    if not isinstance(comments, list):
        raise ValueError(f"{source_label} consolidation comments must be a list")
    for comment_index, comment in enumerate(comments, start=1):
        if not isinstance(comment, dict):
            raise ValueError(
                f"{source_label} consolidation comment {comment_index} must be an object"
            )
        row_id = _optional_text(comment, "row_id") or f"comment_{comment_index:04d}"
        comment_id = _optional_text(comment, "comment_id")
        handles.append(
            _reddit_handle(
                packet=packet,
                source_label=source_label,
                row_id=row_id,
                row_kind="comment",
                fullname_prefix="t1",
                fullname_id=comment_id,
                raw_file=raw_file,
                slice_id=slice_id,
                raw_html_bytes=raw_html_bytes,
                ecr_ref=ecr_ref,
                findings=findings,
            )
        )

    return {
        "handles": handles,
        "ecr_receipt": ecr_receipt,
        "source_summary": {
            "source_label": source_label,
            "packet_id": packet.packet_id,
            "packet_dir": str(packet_dir),
            "consolidation_json": str(consolidation_path),
            "handle_count": len(handles),
            "comment_count": len(comments),
        },
    }


def _process_instagram_entry(
    *,
    entry: dict[str, Any],
    index: int,
    manifest_dir: Path,
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    handle = _optional_text(entry, "handle") or f"instagram_{index}"
    source_label = _optional_text(entry, "source_label") or f"instagram:{handle}"
    packet_dir = _resolve_manifest_path(manifest_dir, entry, "packet_dir")
    projection_path = _resolve_manifest_path(manifest_dir, entry, "projection_json")

    packet = _load_packet(packet_dir)
    projection = IgCreatorMomentumProjectionPacket.model_validate(
        _load_json_object(projection_path, f"{source_label} projection")
    )
    if projection.packet_id != packet.packet_id:
        raise ValueError(
            f"{source_label} projection packet_id {projection.packet_id!r} "
            f"does not match packet {packet.packet_id!r}"
        )

    ecr_receipt, ecr_ref = _derive_ecr_receipt(
        packet=packet,
        packet_dir=packet_dir,
        source_label=source_label,
    )

    structure_preserved = bool(projection.loss_ledger.structure_preserved)
    base_handles = cleaning_input_handles_from_projection_rows(
        source_family=packet.source_family,
        source_surface=packet.source_surface,
        projection_packet=projection,
        handle_id_prefix=f"instagram:{_handle_token(handle)}:{packet.packet_id}",
    )
    _verify_instagram_projection_anchors(
        packet_dir=packet_dir,
        packet=packet,
        projection=projection,
        source_label=source_label,
        findings=findings,
    )

    trace_notes = _instagram_handle_trace_notes(
        structure_preserved=structure_preserved,
        projection_residuals=projection.residuals,
    )
    handles: list[CleaningInputHandle] = []
    for raw_handle in base_handles:
        handle_payload = raw_handle.model_dump(mode="json")
        handles.append(
            CleaningInputHandle.model_validate(
                {
                    **handle_payload,
                    "ecr_ref": ecr_ref.model_dump(mode="json"),
                    "residuals": _dedupe_preserve_order(
                        [*handle_payload.get("residuals", []), *trace_notes["residuals"]]
                    ),
                    "warnings": _dedupe_preserve_order(
                        [*handle_payload.get("warnings", []), *trace_notes["warnings"]]
                    ),
                    "raw_pull_triggers": _dedupe_preserve_order(
                        [
                            *handle_payload.get("raw_pull_triggers", []),
                            *trace_notes["raw_pull_triggers"],
                        ]
                    ),
                }
            )
        )

    if not structure_preserved:
        findings.append(
            {
                "code": "instagram_structure_not_preserved",
                "source_label": source_label,
                "packet_id": packet.packet_id,
                "residuals": projection.residuals,
            }
        )

    return {
        "handles": handles,
        "ecr_receipt": ecr_receipt,
        "source_summary": {
            "source_label": source_label,
            "packet_id": packet.packet_id,
            "packet_dir": str(packet_dir),
            "projection_json": str(projection_path),
            "handle_count": len(handles),
            "projection_method": projection.projection_method,
            "projection_version": projection.projection_version,
            "structure_preserved": structure_preserved,
            "projection_residuals": projection.residuals,
            "row_count": len(projection.rows),
        },
    }


def _verify_instagram_projection_anchors(
    *,
    packet_dir: Path,
    packet: SourceCapturePacket,
    projection: IgCreatorMomentumProjectionPacket,
    source_label: str,
    findings: list[dict[str, Any]],
) -> None:
    packet_slice_files_by_id = {
        source_slice.slice_id: set(source_slice.preserved_file_ids)
        for source_slice in packet.source_slices
    }
    packet_file_ids = {preserved_file.file_id for preserved_file in packet.preserved_files}
    checked_json_payloads: dict[tuple[str, str, str], Any] = {}
    for row in projection.rows:
        if row.raw_ref.packet_id != packet.packet_id:
            raise ValueError(
                f"{source_label} projection row {row.row_id!r} raw_ref packet_id "
                f"{row.raw_ref.packet_id!r} does not match packet {packet.packet_id!r}"
            )
        if row.raw_ref.slice_id not in packet_slice_files_by_id:
            raise ValueError(
                f"{source_label} projection row {row.row_id!r} raw_ref slice_id "
                f"{row.raw_ref.slice_id!r} is absent from packet {packet.packet_id!r}"
            )
        if row.raw_anchor.file_id not in packet_file_ids:
            raise ValueError(
                f"{source_label} projection row {row.row_id!r} raw_anchor file_id "
                f"{row.raw_anchor.file_id!r} is absent from packet {packet.packet_id!r}"
            )
        key = (
            row.raw_anchor.file_id,
            row.raw_anchor.relative_packet_path,
            row.raw_anchor.sha256,
        )
        if key not in checked_json_payloads:
            _raw_file, raw_path = _verified_preserved_file(
                packet_dir=packet_dir,
                packet=packet,
                file_id=row.raw_anchor.file_id,
                expected_relative_packet_path=row.raw_anchor.relative_packet_path,
                expected_sha256=row.raw_anchor.sha256,
            )
            checked_json_payloads[key] = _load_json_bytes(
                raw_path.read_bytes(),
                findings=findings,
                finding_context={
                    "code": "instagram_row_anchor_unverified",
                    "source_label": source_label,
                    "packet_id": packet.packet_id,
                    "row_id": row.row_id,
                    "row_kind": row.row_kind,
                    "anchor_kind": "json_pointer",
                    "anchor_value": row.raw_anchor.json_pointer,
                },
            )

        if row.raw_anchor.json_pointer and not _json_pointer_exists(
            checked_json_payloads[key],
            row.raw_anchor.json_pointer,
        ):
            findings.append(
                {
                    "code": "instagram_row_anchor_unverified",
                    "source_label": source_label,
                    "packet_id": packet.packet_id,
                    "row_id": row.row_id,
                    "row_kind": row.row_kind,
                    "anchor_kind": "json_pointer",
                    "anchor_value": row.raw_anchor.json_pointer,
                    "reason": "json_pointer_absent_from_raw",
                }
            )


def _load_json_bytes(
    raw_bytes: bytes,
    *,
    findings: list[dict[str, Any]],
    finding_context: dict[str, Any],
) -> Any:
    try:
        return json.loads(raw_bytes)
    except json.JSONDecodeError:
        findings.append({**finding_context, "reason": "raw_json_malformed"})
        return None


def _json_pointer_exists(payload: Any, pointer: str) -> bool:
    if pointer == "":
        return True
    if not pointer.startswith("/"):
        return False
    current = payload
    for raw_token in pointer.split("/")[1:]:
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            if token not in current:
                return False
            current = current[token]
            continue
        if isinstance(current, list) and token.isdigit():
            index = int(token)
            if index >= len(current):
                return False
            current = current[index]
            continue
        return False
    return True


def _instagram_handle_trace_notes(
    *,
    structure_preserved: bool,
    projection_residuals: Sequence[str],
) -> dict[str, list[str]]:
    warnings: list[str] = []
    residuals: list[str] = []
    raw_pull_triggers: list[str] = []

    if not structure_preserved:
        warnings.append(INSTAGRAM_STRUCTURE_NOT_PRESERVED_REASON)
        residuals.extend(
            f"{INSTAGRAM_STRUCTURE_NOT_PRESERVED_REASON}:{residual}"
            for residual in projection_residuals
        )
        raw_pull_triggers.append(
            f"{INSTAGRAM_RAW_PULL_TRIGGER_PREFIX}:{INSTAGRAM_STRUCTURE_NOT_PRESERVED_REASON}"
        )

    return {
        "warnings": _dedupe_preserve_order(warnings),
        "residuals": _dedupe_preserve_order(residuals),
        "raw_pull_triggers": _dedupe_preserve_order(raw_pull_triggers),
    }

def _reddit_handle(
    *,
    packet: SourceCapturePacket,
    source_label: str,
    row_id: str,
    row_kind: str,
    fullname_prefix: str,
    fullname_id: str | None,
    raw_file: PreservedFile,
    slice_id: str,
    raw_html_bytes: bytes,
    ecr_ref: CleaningEcrRef,
    findings: list[dict[str, Any]],
) -> CleaningInputHandle:
    anchor_pattern = _old_reddit_anchor_pattern(
        raw_html_bytes, fullname_prefix, fullname_id
    )
    if anchor_pattern is None:
        anchor_kind = "file"
        anchor_value = None
        findings.append(
            {
                "code": "reddit_row_anchor_downgraded",
                "source_label": source_label,
                "packet_id": packet.packet_id,
                "row_id": row_id,
                "row_kind": row_kind,
                "reason": "raw_html_missing_matching_old_reddit_fullname_or_id_pattern",
            }
        )
    else:
        anchor_kind = "text_pattern"
        anchor_value = anchor_pattern

    return CleaningInputHandle(
        handle_id=f"{source_label}:{packet.packet_id}:{row_id}",
        source_family=packet.source_family,
        source_surface=packet.source_surface,
        raw_anchor=CleaningRawAnchor(
            packet_id=packet.packet_id,
            slice_id=slice_id,
            file_id=raw_file.file_id,
            relative_packet_path=raw_file.relative_packet_path,
            sha256=raw_file.sha256,
            hash_basis=raw_file.hash_basis,
            anchor_kind=anchor_kind,
            anchor_value=anchor_value,
        ),
        projection_ref=CleaningProjectionRef(
            projection_method="old_reddit_thread_consolidation_row_view",
            projection_version=REDDIT_THREAD_CONSOLIDATION_SCHEMA_VERSION,
            certification="view_only; not_cleaned; not_normalized; not_judgment_ready",
            packet_id=packet.packet_id,
            row_id=row_id,
            row_kind=row_kind,
        ),
        ecr_ref=ecr_ref,
    )


def _old_reddit_anchor_pattern(
    raw_html_bytes: bytes,
    fullname_prefix: str,
    fullname_id: str | None,
) -> str | None:
    fullnames = _old_reddit_fullname_candidates(fullname_prefix, fullname_id)
    candidates = tuple(
        candidate
        for fullname in fullnames
        for candidate in (
            f'data-fullname="{fullname}"',
            f"data-fullname='{fullname}'",
            f'id="thing_{fullname}"',
            f"id='thing_{fullname}'",
            f'id="{fullname}"',
            f"id='{fullname}'",
        )
    )
    return next(
        (
            candidate
            for candidate in candidates
            if candidate.encode("ascii") in raw_html_bytes
        ),
        None,
    )


def _old_reddit_fullname_candidates(
    fullname_prefix: str,
    fullname_id: str | None,
) -> tuple[str, ...]:
    if not fullname_id:
        return ()
    normalized = fullname_id.strip()
    if not normalized:
        return ()
    if normalized.startswith(("t1_", "t3_")):
        return (normalized,)
    return (f"{fullname_prefix}_{normalized}",)

def _process_youtube_entry(
    *,
    entry: dict[str, Any],
    index: int,
    manifest_dir: Path,
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    """Wire a YouTube caption packet through ECR into file-anchor cleaning handles."""
    source_label = _optional_text(entry, "source_label") or f"youtube:{index}"
    packet_dir = _resolve_manifest_path(manifest_dir, entry, "packet_dir")

    packet = _load_packet(packet_dir)
    if (packet.source_family, packet.source_surface) != ("youtube", "youtube_captions"):
        # No projection/consolidation cross-check exists for YouTube, so guard on identity:
        # refuse to route a non-YouTube packet through the caption branch (fail closed).
        raise ValueError(
            f"{source_label} packet {packet.packet_id} is not a YouTube caption packet "
            f"(source_family={packet.source_family!r}, source_surface={packet.source_surface!r})"
        )

    ecr_receipt, ecr_ref = _derive_ecr_receipt(
        packet=packet,
        packet_dir=packet_dir,
        source_label=source_label,
    )

    handles: list[CleaningInputHandle] = []
    files_by_id = {preserved.file_id: preserved for preserved in packet.preserved_files}
    for source_slice in packet.source_slices:
        for file_id in source_slice.preserved_file_ids:
            raw_file = files_by_id.get(file_id)
            if raw_file is None:
                raise ValueError(
                    f"{source_label} packet {packet.packet_id} slice {source_slice.slice_id!r} "
                    f"references absent preserved file {file_id!r}"
                )
            verified_file, _raw_path = _verified_preserved_file(
                packet_dir=packet_dir,
                packet=packet,
                file_id=raw_file.file_id,
                expected_relative_packet_path=raw_file.relative_packet_path,
                expected_sha256=raw_file.sha256,
            )
            handles.append(
                CleaningInputHandle(
                    handle_id=(
                        f"{source_label}:{packet.packet_id}:{source_slice.slice_id}:"
                        f"{verified_file.file_id}"
                    ),
                    source_family=packet.source_family,
                    source_surface=packet.source_surface,
                    raw_anchor=CleaningRawAnchor(
                        packet_id=packet.packet_id,
                        slice_id=source_slice.slice_id,
                        file_id=verified_file.file_id,
                        relative_packet_path=verified_file.relative_packet_path,
                        sha256=verified_file.sha256,
                        hash_basis=verified_file.hash_basis,
                        anchor_kind="file",
                    ),
                    # Projection-less / direct-artifact: no projection_ref.
                    ecr_ref=ecr_ref,
                )
            )

    return {
        "handles": handles,
        "ecr_receipt": ecr_receipt,
        "source_summary": {
            "source_label": source_label,
            "packet_id": packet.packet_id,
            "packet_dir": str(packet_dir),
            "source_surface": packet.source_surface,
            "slice_count": len(packet.source_slices),
            "preserved_file_count": len(packet.preserved_files),
            "handle_count": len(handles),
        },
    }


def _process_youtube_asr_entry(
    *,
    entry: dict[str, Any],
    index: int,
    data_root: DataLakeRoot | None,
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    """Wire a lake-resident YouTube AUDIO packet + its transcript_asr derived record into a
    single cleaning handle anchored by ``derived_record``.

    Unlike the caption ``youtube`` entry (a plain packet directory), the ASR artifact set lives
    entirely in the lake: the audio is a preserved file under ``raw/`` and the transcript is a
    DERIVED record under ``derived/<audio_packet_id>/transcript_asr/``. The cleaning input is the
    transcript record's bytes, which are not a preserved file, so the handle carries a
    ``derived_record`` anchor (re-verified against the record bytes by the periodic audit).
    """
    if data_root is None:
        # Defensive: the entry-point already fails closed, but never let this path silently no-op.
        raise ValueError("youtube_asr entry requires an injected data_root (fail-closed).")
    audio_packet_id = _required_text(entry, "audio_packet_id", f"youtube_asr[{index}]")
    source_label = _optional_text(entry, "source_label") or f"youtube_asr:{index}"

    loaded = data_root.load_raw_packet(audio_packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    if (packet.source_family, packet.source_surface) != ("youtube", "youtube_audio"):
        # No projection/consolidation cross-check exists for the ASR path, so guard on identity:
        # refuse to route a non-audio packet through the ASR branch (fail closed).
        raise ValueError(
            f"{source_label} packet {packet.packet_id} is not a YouTube audio packet "
            f"(source_family={packet.source_family!r}, source_surface={packet.source_surface!r})"
        )

    ecr_receipt, ecr_ref = _derive_ecr_receipt(
        packet=packet,
        packet_dir=loaded.container,
        source_label=source_label,
    )

    # Locate the transcript records in the lake. Derived records carry no by-key hash, so read
    # each record's bytes directly (mirrors run_transcript_product_extract._asr_records).
    lane_dir = data_root.lane_dir(
        subtree="derived", raw_anchor=audio_packet_id, lane=_ASR_LANE
    )
    transcribed: list[tuple[str, bytes]] = []
    if lane_dir.is_dir():
        # transcript_asr record ids carry no extension (asr_packet.py), so read every file.
        for record_file in sorted(lane_dir.iterdir()):
            if not record_file.is_file():
                continue
            record_bytes = record_file.read_bytes()
            try:
                record = json.loads(record_bytes.decode("utf-8"))
            except (ValueError, UnicodeDecodeError):
                continue
            if isinstance(record, dict) and record.get("posture") == "transcribed":
                transcribed.append((record_file.name, record_bytes))

    # Fail-closed selection (mirrors _process_youtube_entry's len(...) != 1 discipline): exactly
    # one transcribed record, else raise on zero or many (no silent coverage gap).
    if len(transcribed) != 1:
        raise ValueError(
            f"{source_label} audio packet {audio_packet_id} must have exactly one transcribed "
            f"transcript_asr record; found {len(transcribed)}"
        )
    record_id, record_bytes = transcribed[0]
    stitch_sha256 = hashlib.sha256(record_bytes).hexdigest()

    # Bind the anchor to the DERIVATION-TIME content sha committed in the record-set marker when
    # present (the stronger guarantee), else fall back to the stitch-time sha for a legacy markerless
    # record. read_record_set_member_sha256 returns None ONLY when the marker is ABSENT; a
    # present-but-corrupt marker RAISES DataLakeRootError, which we let PROPAGATE (fail closed) --
    # a new record whose marker is unreadable is corruption, never a silent stitch-time downgrade.
    marker_sha256 = data_root.read_record_set_member_sha256(
        subtree="derived",
        raw_anchor=audio_packet_id,
        record_id=record_id,
        completion_lane=_ASR_COMPLETION_LANE,
        member_lane=_ASR_LANE,
    )
    if marker_sha256 is not None:
        # Defensively re-check the derivation-time commitment against the bytes at stitch: a marker
        # sha that disagrees with the record bytes is corruption -- raise, never trust either side.
        if marker_sha256 != stitch_sha256:
            raise ValueError(
                f"{source_label} audio packet {audio_packet_id} transcript record {record_id!r} "
                f"marker sha256 {marker_sha256} disagrees with record bytes {stitch_sha256} "
                "(derivation-time/stitch-time mismatch; fail closed)"
            )
        anchor_sha256 = marker_sha256
        anchor_hash_basis = _HASH_BASIS_MARKER
    else:
        anchor_sha256 = stitch_sha256
        anchor_hash_basis = _HASH_BASIS_BYTES

    handle = CleaningInputHandle(
        handle_id=f"{source_label}:{audio_packet_id}:{record_id}",
        source_family=packet.source_family,
        source_surface=packet.source_surface,
        raw_anchor=CleaningRawAnchor(
            packet_id=audio_packet_id,
            sha256=anchor_sha256,
            hash_basis=anchor_hash_basis,
            anchor_kind="derived_record",
            derived_record_ref=CleaningDerivedRecordRef(
                lane=_ASR_LANE,
                record_id=record_id,
            ),
        ),
        # Derived record: no projection_ref (it is not a projection view of a preserved file).
        ecr_ref=ecr_ref,
    )

    return {
        "handles": [handle],
        "ecr_receipt": ecr_receipt,
        "source_summary": {
            "source_label": source_label,
            "packet_id": audio_packet_id,
            "handle_count": 1,
            "transcript_record_id": record_id,
            "transcript_lane": _ASR_LANE,
        },
    }


def _derive_ecr_receipt(
    *,
    packet: SourceCapturePacket,
    packet_dir: Path,
    source_label: str,
) -> tuple[EcrSourceSideReceipt, CleaningEcrRef]:
    identity = derive_identity_postures(packet)
    inspectability = derive_inspectability_postures(packet)
    timing = derive_timing_postures(packet)
    source_visibility = derive_source_visibility_postures(packet)
    ref_id = f"ecr:{packet.packet_id}:{ECR_REF_KIND}"

    receipt = EcrSourceSideReceipt(
        source_label=source_label,
        packet_id=packet.packet_id,
        packet_dir=str(packet_dir),
        ref_id=ref_id,
        postures={
            "identity": identity,
            "inspectability": inspectability,
            "timing": timing,
            "source_visibility": source_visibility,
        },
        clears={
            "identity": _all_clear(identity, "clears_identity"),
            "inspectability": _all_clear(inspectability, "clears_inspectable"),
            "timing": _all_clear(timing, "clears_pre_cutoff"),
            "source_visibility": _all_clear(
                source_visibility,
                "clears_source_visibility",
            ),
        },
    )

    return receipt, CleaningEcrRef(
        packet_id=packet.packet_id,
        ref_id=ref_id,
        posture_kind=ECR_REF_KIND,
    )


def _verify_retail_projection_anchors(
    *,
    packet_dir: Path,
    packet: SourceCapturePacket,
    projection: RetailPdpProjectionPacket,
    source_label: str,
    findings: list[dict[str, Any]],
) -> None:
    packet_slice_files_by_id = {
        source_slice.slice_id: set(source_slice.preserved_file_ids)
        for source_slice in packet.source_slices
    }
    checked_files: dict[tuple[str, str, str], bytes] = {}
    for row in projection.rows:
        if row.raw_ref.packet_id != packet.packet_id:
            raise ValueError(
                f"{source_label} projection row {row.row_id!r} raw_ref packet_id "
                f"{row.raw_ref.packet_id!r} does not match packet {packet.packet_id!r}"
            )
        if row.raw_ref.slice_id not in packet_slice_files_by_id:
            raise ValueError(
                f"{source_label} projection row {row.row_id!r} raw_ref slice_id "
                f"{row.raw_ref.slice_id!r} is absent from packet {packet.packet_id!r}"
            )
        if row.raw_anchor.file_id not in packet_slice_files_by_id[row.raw_ref.slice_id]:
            raise ValueError(
                f"{source_label} projection row {row.row_id!r} raw_ref slice_id "
                f"{row.raw_ref.slice_id!r} does not preserve file_id "
                f"{row.raw_anchor.file_id!r}"
            )
        key = (
            row.raw_anchor.file_id,
            row.raw_anchor.relative_packet_path,
            row.raw_anchor.sha256,
        )
        if key not in checked_files:
            _raw_file, raw_path = _verified_preserved_file(
                packet_dir=packet_dir,
                packet=packet,
                file_id=row.raw_anchor.file_id,
                expected_relative_packet_path=row.raw_anchor.relative_packet_path,
                expected_sha256=row.raw_anchor.sha256,
            )
            checked_files[key] = raw_path.read_bytes()

        reason = _retail_anchor_unverified_reason(
            anchor_kind=row.raw_anchor.anchor_kind,
            anchor_value=row.raw_anchor.anchor_value,
            raw_bytes=checked_files[key],
        )
        if reason is not None:
            findings.append(
                {
                    "code": "retail_row_anchor_unverified",
                    "source_label": source_label,
                    "packet_id": packet.packet_id,
                    "row_id": row.row_id,
                    "row_kind": row.row_kind,
                    "anchor_kind": row.raw_anchor.anchor_kind,
                    "anchor_value": row.raw_anchor.anchor_value,
                    "reason": reason,
                }
            )


def _retail_anchor_unverified_reason(
    *,
    anchor_kind: str,
    anchor_value: str | None,
    raw_bytes: bytes,
) -> str | None:
    if anchor_kind in {"file", "json_pointer"}:
        return None
    if not anchor_value or not anchor_value.strip():
        return "anchor_value_absent"
    if anchor_kind == "text_pattern":
        occurrence_count = raw_bytes.count(anchor_value.encode("utf-8"))
        if occurrence_count == 0:
            return "text_pattern_absent_from_raw"
        if occurrence_count > 1:
            return "text_pattern_ambiguous_in_raw"
        return None
    if anchor_kind == "script_index":
        return _script_anchor_unverified_reason(anchor_value=anchor_value, raw_bytes=raw_bytes)
    if anchor_kind == "html_selector":
        return _html_selector_unverified_reason(anchor_value=anchor_value, raw_bytes=raw_bytes)
    return "unsupported_anchor_kind"


def _script_anchor_unverified_reason(*, anchor_value: str, raw_bytes: bytes) -> str | None:
    raw_lower = raw_bytes.lower()
    anchor_lower = anchor_value.lower()
    probes: list[bytes] = []
    if "apollo" in anchor_lower:
        probes.append(b"window.__apollo_state__")
    if "ld_json" in anchor_lower or "ld-json" in anchor_lower or "json" in anchor_lower:
        probes.append(b"application/ld+json")
    if not probes:
        probes.append(anchor_value.encode("utf-8").lower())
    return None if any(probe in raw_lower for probe in probes) else "script_anchor_substrate_absent_from_raw"


def _html_selector_unverified_reason(*, anchor_value: str, raw_bytes: bytes) -> str | None:
    selector_ids = [match.group(1) for match in re.finditer(r"#([A-Za-z0-9_-]+)", anchor_value)]
    if not selector_ids:
        return None if anchor_value.encode("utf-8") in raw_bytes else "html_selector_literal_absent_from_raw"
    raw_lower = raw_bytes.lower()
    for selector_id in selector_ids:
        escaped = re.escape(selector_id).encode("ascii")
        pattern = rb"(?:id|name)\s*=\s*['\"]" + escaped + rb"['\"]"
        if re.search(pattern.lower(), raw_lower):
            return None
    return "html_selector_id_or_name_absent_from_raw"


def _retail_capture_validity_reasons(
    *,
    packet_dir: Path,
    packet: SourceCapturePacket,
    projection: RetailPdpProjectionPacket,
) -> list[str]:
    reasons: list[str] = []
    html_files = [
        preserved_file
        for preserved_file in packet.preserved_files
        if preserved_file.relative_packet_path.lower().endswith((".html", ".htm"))
    ]
    if not html_files:
        reasons.append("rendered_dom_absent")
    for preserved_file in html_files:
        _raw_file, raw_path = _verified_preserved_file(
            packet_dir=packet_dir,
            packet=packet,
            file_id=preserved_file.file_id,
            expected_relative_packet_path=preserved_file.relative_packet_path,
            expected_sha256=preserved_file.sha256,
        )
        raw_bytes = raw_path.read_bytes()
        raw_text = _decode_bytes(raw_bytes).lower()
        has_error_marker = any(marker in raw_text for marker in _RETAIL_ERROR_PAGE_MARKERS)
        if has_error_marker:
            reasons.append("rendered_dom_error_or_block_page_marker")
            if len(raw_bytes) < 5_000:
                reasons.append("tiny_rendered_dom_with_error_marker")
    if _projection_has_all_null_required_rows(projection):
        reasons.append("required_retail_rows_all_null")
    return _dedupe_preserve_order(reasons)


def _retail_handle_trace_notes(
    *,
    capture_validity_reasons: Sequence[str],
    structure_preserved: bool,
    projection_residuals: Sequence[str],
) -> dict[str, list[str]]:
    warnings: list[str] = []
    residuals: list[str] = []
    raw_pull_triggers: list[str] = []

    if capture_validity_reasons:
        warnings.extend(
            f"{CAPTURE_VALIDITY_NOT_SUPPORTED_REASON}:{reason}"
            for reason in capture_validity_reasons
        )
        raw_pull_triggers.append(
            f"{RETAIL_RAW_PULL_TRIGGER_PREFIX}:{CAPTURE_VALIDITY_NOT_SUPPORTED_REASON}"
        )

    if not structure_preserved:
        warnings.append(RETAIL_STRUCTURE_NOT_PRESERVED_REASON)
        residuals.extend(
            f"{RETAIL_STRUCTURE_NOT_PRESERVED_REASON}:{residual}"
            for residual in projection_residuals
        )
        raw_pull_triggers.append(
            f"{RETAIL_RAW_PULL_TRIGGER_PREFIX}:{RETAIL_STRUCTURE_NOT_PRESERVED_REASON}"
        )

    return {
        "warnings": _dedupe_preserve_order(warnings),
        "residuals": _dedupe_preserve_order(residuals),
        "raw_pull_triggers": _dedupe_preserve_order(raw_pull_triggers),
    }


def _projection_has_all_null_required_rows(projection: RetailPdpProjectionPacket) -> bool:
    for row in projection.rows:
        if row.row_kind == "retail_variant_offer" and not any(
            _source_value_present(row.source_visible_fields.get(field))
            for field in ("sku", "product_id", "variant_name", "price", "price_currency", "availability")
        ):
            return True
        if row.row_kind == "retail_review_substrate" and not any(
            _source_value_present(row.source_visible_fields.get(field))
            for field in ("rating", "review_count", "best_sellers_rank_text")
        ):
            return True
    return False


def _source_value_present(value: Any) -> bool:
    if value is None or value is False:
        return False
    if isinstance(value, str):
        return bool(value.strip()) and value.lower() not in {"absent", "none", "unknown"}
    return True


def _retail_transform_candidates(
    *,
    handles: Sequence[CleaningInputHandle],
    rows: Sequence[Any],
) -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    for handle, row in zip(handles, rows):
        if getattr(row, "row_kind", None) in _RETAIL_TRANSFORM_CONTEXT_ROW_KINDS:
            continue
        for field_name, value in row.source_visible_fields.items():
            if field_name in _RETAIL_TRANSFORM_METADATA_FIELDS:
                continue
            if isinstance(value, str) and value.strip():
                candidates.append(
                    {
                        "handle_id": handle.handle_id,
                        "field_name": field_name,
                        "original_value": value,
                    }
                )
                break
    return candidates


def _cleaning_transform_smoke_entries(
    candidates: Sequence[dict[str, str]],
) -> list[CleaningTransformLedgerEntry]:
    for candidate in candidates:
        original_value = candidate.get("original_value", "")
        transformed_value = _normalize_cleaning_smoke_value(original_value)
        if not transformed_value:
            continue
        return [
            CleaningTransformLedgerEntry(
                input_handle_id=candidate["handle_id"],
                transform=CleaningTransform(
                    transform_class=CleaningTransformClass.NORMALIZATION,
                    rule_scope=CleaningRuleScope.SOURCE_INVARIANT_CORE,
                    method_or_rule="unicode_nfkc_whitespace_collapse",
                    input_grain=CleaningInputGrain.ROW,
                    original_value=original_value,
                    transformed_value=transformed_value,
                ),
                preservation=CleaningPreservationCheck(
                    originals_addressable=True,
                    source_identity_preserved=True,
                    timing_preserved=True,
                    hierarchy_preserved=True,
                    semantic_binding_preserved=True,
                    counts_preserved=True,
                ),
            )
        ]
    raise ValueError("cleaning transform smoke requires a source-visible string value")


def _normalize_cleaning_smoke_value(value: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value)).strip()


def _decode_bytes(value: bytes) -> str:
    return value.decode("utf-8", errors="replace")


def _dedupe_preserve_order(values: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            deduped.append(value)
    return deduped


_RETAIL_ERROR_PAGE_MARKERS = (
    "page not found",
    "we couldn't find that page",
    "we can\u2019t load this page",
    "we can't load this page",
    "robot check",
    "enter the characters you see below",
    "access denied",
)


def _all_clear(postures: Sequence[Any], field_name: str) -> bool:
    return bool(postures) and all(bool(getattr(posture, field_name)) for posture in postures)


def _load_packet(packet_dir: Path) -> SourceCapturePacket:
    manifest_path = packet_dir / "manifest.json"
    if not manifest_path.is_file():
        raise ValueError(f"packet manifest not found: {manifest_path}")
    return SourceCapturePacket.model_validate(
        _load_json_object(manifest_path, f"packet manifest {manifest_path}")
    )


def _verified_preserved_file(
    *,
    packet_dir: Path,
    packet: SourceCapturePacket,
    file_id: str,
    expected_relative_packet_path: str,
    expected_sha256: str,
) -> tuple[PreservedFile, Path]:
    raw_file = next(
        (preserved for preserved in packet.preserved_files if preserved.file_id == file_id),
        None,
    )
    if raw_file is None:
        raise ValueError(f"packet {packet.packet_id} does not preserve file_id {file_id!r}")
    if raw_file.relative_packet_path != expected_relative_packet_path:
        raise ValueError(
            f"packet {packet.packet_id} file {file_id!r} path "
            f"{raw_file.relative_packet_path!r} does not match consolidation "
            f"{expected_relative_packet_path!r}"
        )
    raw_path = _contained_packet_path(packet_dir, raw_file.relative_packet_path)
    actual_sha256 = hash_file(raw_path)
    if actual_sha256 != raw_file.sha256:
        raise ValueError(
            f"packet {packet.packet_id} file {file_id!r} hash mismatch against manifest"
        )
    if actual_sha256 != expected_sha256:
        raise ValueError(
            f"packet {packet.packet_id} file {file_id!r} hash mismatch against consolidation"
        )
    return raw_file, raw_path


def _contained_packet_path(packet_dir: Path, relative_packet_path: str) -> Path:
    path = (packet_dir / relative_packet_path).resolve()
    packet_root = packet_dir.resolve()
    try:
        path.relative_to(packet_root)
    except ValueError as exc:
        raise ValueError(
            f"preserved file path escapes packet directory: {relative_packet_path}"
        ) from exc
    if not path.is_file():
        raise ValueError(f"preserved file not found: {path}")
    return path


def _slice_id_for_file(packet: SourceCapturePacket, file_id: str) -> str:
    for source_slice in packet.source_slices:
        if file_id in source_slice.preserved_file_ids:
            return source_slice.slice_id
    raise ValueError(f"packet {packet.packet_id} has no source slice for file {file_id!r}")


def _entry_list(manifest: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = manifest.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"smoke manifest field {key!r} must be a list")
    entries: list[dict[str, Any]] = []
    for index, entry in enumerate(value, start=1):
        if not isinstance(entry, dict):
            raise ValueError(f"smoke manifest {key}[{index}] must be an object")
        entries.append(entry)
    return entries


def _load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"{label} not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} is not valid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must be a JSON object: {path}")
    return payload


def _resolve_manifest_path(
    manifest_dir: Path,
    entry: dict[str, Any],
    field_name: str,
) -> Path:
    raw_value = _required_text(entry, field_name, "smoke manifest")
    path = Path(raw_value)
    if not path.is_absolute():
        path = manifest_dir / path
    return path.resolve()


def _required_text(mapping: dict[str, Any], field_name: str, label: str) -> str:
    value = mapping.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} field {field_name!r} must be a non-empty string")
    return value


def _optional_text(mapping: dict[str, Any], field_name: str) -> str | None:
    value = mapping.get(field_name)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"field {field_name!r} must be a string when provided")
    value = value.strip()
    return value or None


def _handle_token(value: str) -> str:
    token = "".join(character if character.isalnum() else "_" for character in value)
    return token.lower().strip("_") or "retail"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Stitch existing Capture packet/projection/consolidation artifacts into "
            "ECR source-side receipts and a CleaningPacket."
        )
    )
    parser.add_argument(
        "--smoke-manifest",
        required=True,
        type=Path,
        help="JSON manifest naming existing packet/projection/consolidation artifacts.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory where smoke output JSON files will be written.",
    )
    parser.add_argument(
        "--include-cleaning-transform-smoke",
        action="store_true",
        help="Also write one mechanical Cleaning transform ledger entry when source-visible text exists.",
    )
    args = parser.parse_args(argv)

    try:
        outputs = run_capture_ecr_cleaning_smoke(
            smoke_manifest_path=args.smoke_manifest,
            output_dir=args.output_dir,
            include_cleaning_transform_smoke=args.include_cleaning_transform_smoke,
        )
    except (ValueError, ValidationError) as exc:
        parser.exit(status=2, message=f"capture/ECR/Cleaning smoke failed: {exc}\n")

    print(json.dumps(outputs, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
