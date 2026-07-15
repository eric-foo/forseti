"""Persist Basenotes Cleaning output into the Data Lake."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cleaning.models import CLEANING_CORE_VERSION, REQUIRED_NON_CLAIMS, CleaningInputHandle, CleaningPacket
from cleaning.basenotes import build_basenotes_cleaning_packet
from data_lake.canonical_json import canonical_record_bytes as _json_bytes
from data_lake.silver_record import append_silver_record
from harness_utils import generate_ulid
from source_capture.models import SourceCapturePacket, VisibleFactStatus
from source_capture.basenotes_projection import (
    BASENOTES_PROJECTION_CERTIFICATION,
    BASENOTES_PROJECTION_METHOD,
    BASENOTES_PROJECTION_VERSION,
    build_basenotes_projection,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


BASENOTES_CLEANING_AUDIT_LANE = "cleaning_basenotes_audit"
BASENOTES_CLEANING_SILVER_LANE = "cleaning_basenotes_silver"
CLEANING_AUDIT_PACK_SCHEMA_VERSION = "cleaning_audit_pack_v0"
SILVER_VAULT_RECORD_SCHEMA_VERSION = "silver_vault_record_v0"
BASENOTES_AUDIT_PACK_PRODUCER_SCHEMA_VERSION = "basenotes_cleaning_audit_pack_v1"
BASENOTES_SILVER_PRODUCER_SCHEMA_VERSION = "basenotes_cleaning_silver_textobservation_v2"
BASENOTES_CLEANING_METHOD_ID = "basenotes_cleaning_method_v1"
TEXT_NORMALIZATION_RULE = "basenotes_text_whitespace_normalization"
BASENOTES_RATING_METRIC_RESIDUAL = "basenotes_rating_metric_observations_deferred"

DISCRIMINATOR_LOCALITY_NON_CLAIM = (
    "record_family_and_audit_kind_local_to_cleaning_audit_pack_v0_no_lake_wide_dispatch"
)

_CONTENT_HASH_BASIS = "canonical_json_excluding_content_hash"
_AUDIT_PRODUCER_ID = "forseti-harness.cleaning.basenotes_lake.derive_basenotes_cleaning_into_lake#audit"
_SILVER_PRODUCER_ID = "forseti-harness.cleaning.basenotes_lake.derive_basenotes_cleaning_into_lake#silver"


@dataclass(frozen=True)
class BasenotesCleaningLakeResult:
    """Outputs of one Basenotes Cleaning derivation into the lake."""

    cleaning_packet: CleaningPacket
    audit_record: dict[str, Any]
    audit_path: Path
    silver_records: list[dict[str, Any]]
    silver_paths: list[Path]


def derive_basenotes_cleaning_into_lake(
    *,
    data_root: "DataLakeRoot",
    packet_id: str,
    record_id: str | None = None,
) -> BasenotesCleaningLakeResult:
    """Build and append the Basenotes Cleaning audit pack plus post-cleaned Silver."""
    loaded = data_root.load_raw_packet(packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    projection = build_basenotes_projection(
        packet=packet,
        raw_file_bytes_by_file_id=loaded.bodies,
    )
    cleaning_packet = build_basenotes_cleaning_packet(projection)

    audit_seed = record_id if record_id is not None else generate_ulid()
    audit_record_name = f"{audit_seed}.json"
    audit_record = basenotes_cleaning_audit_pack_payload(
        packet=packet,
        cleaning_packet=cleaning_packet,
        record_id=audit_record_name,
    )
    audit_path = data_root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=BASENOTES_CLEANING_AUDIT_LANE,
        record_id=audit_record_name,
        data=_json_bytes(audit_record),
    )

    silver_records = basenotes_post_cleaned_silver_records(
        packet=packet,
        cleaning_packet=cleaning_packet,
        audit_lane=BASENOTES_CLEANING_AUDIT_LANE,
        audit_record_id=audit_record_name,
        audit_content_hash=audit_record["content_hash"],
    )
    silver_paths: list[Path] = []
    for silver_record in silver_records:
        silver_paths.append(
            append_silver_record(
                data_root,
                raw_anchor=packet_id,
                lane=BASENOTES_CLEANING_SILVER_LANE,
                record_id=silver_record["record_id"],
                record=silver_record,
            )
        )

    return BasenotesCleaningLakeResult(
        cleaning_packet=cleaning_packet,
        audit_record=audit_record,
        audit_path=audit_path,
        silver_records=silver_records,
        silver_paths=silver_paths,
    )


def basenotes_cleaning_audit_pack_payload(
    *,
    packet: SourceCapturePacket,
    cleaning_packet: CleaningPacket,
    record_id: str,
) -> dict[str, Any]:
    """Return the Cleaning audit-pack record payload before lake append."""
    capture_time = _known_capture_time(packet)
    record: dict[str, Any] = {
        "schema_version": CLEANING_AUDIT_PACK_SCHEMA_VERSION,
        "record_family": "processing_audit",
        "audit_kind": "cleaning_transform_audit",
        "record_id": record_id,
        "raw_anchor": packet.packet_id,
        "lane_namespace": BASENOTES_CLEANING_AUDIT_LANE,
        "producer_id": _AUDIT_PRODUCER_ID,
        "producer_schema_version": BASENOTES_AUDIT_PACK_PRODUCER_SCHEMA_VERSION,
        "content_hash": "",
        "content_hash_basis": _CONTENT_HASH_BASIS,
        "source_family": packet.source_family,
        "source_surface": packet.source_surface,
        "captured_at": capture_time,
        "input_refs": {
            "raw_refs": _raw_refs(cleaning_packet),
            "projection_refs": _projection_refs(cleaning_packet),
            "ecr_refs": _ecr_refs(cleaning_packet),
        },
        "coverage": _coverage(cleaning_packet),
        "payload": {
            "cleaning_core_version": CLEANING_CORE_VERSION,
            "projection_method": BASENOTES_PROJECTION_METHOD,
            "projection_version": BASENOTES_PROJECTION_VERSION,
            "projection_certification": BASENOTES_PROJECTION_CERTIFICATION,
            "handle_count": len(cleaning_packet.handles),
            "transform_entry_count": len(cleaning_packet.transform_ledger),
            "cleaning_packet": cleaning_packet.model_dump(mode="json"),
        },
        "non_claims": sorted(
            {
                *REQUIRED_NON_CLAIMS,
                "not_corpus_completeness",
                "not_demand_signal",
                "not_evidence_unit_binding",
                "not_judgment",
                "not_metric_observation_promotion",
                "not_sentiment_analysis",
                "not_silver_fact",
                DISCRIMINATOR_LOCALITY_NON_CLAIM,
            }
        ),
    }
    record["content_hash"] = f"sha256:{_content_hash(record)}"
    return record


def basenotes_post_cleaned_silver_records(
    *,
    packet: SourceCapturePacket,
    cleaning_packet: CleaningPacket,
    audit_lane: str,
    audit_record_id: str,
    audit_content_hash: str,
) -> list[dict[str, Any]]:
    """Return one post-cleaned Silver TextObservation per Basenotes text-row handle."""
    capture_time = _known_capture_time(packet)
    handle_by_id = {handle.handle_id: handle for handle in cleaning_packet.handles}
    records: list[dict[str, Any]] = []
    for entry in cleaning_packet.transform_ledger:
        if entry.transform.method_or_rule != TEXT_NORMALIZATION_RULE:
            continue
        cleaned_text = entry.transform.transformed_value
        handle = handle_by_id.get(entry.input_handle_id)
        if cleaned_text is None or handle is None:
            continue
        records.append(
            _post_cleaned_silver_record(
                packet=packet,
                handle=handle,
                cleaned_text=cleaned_text,
                record_id=f"{generate_ulid()}.json",
                capture_time=capture_time,
                audit_lane=audit_lane,
                audit_record_id=audit_record_id,
                audit_content_hash=audit_content_hash,
            )
        )
    return records


def _post_cleaned_silver_record(
    *,
    packet: SourceCapturePacket,
    handle: CleaningInputHandle,
    cleaned_text: str,
    record_id: str,
    capture_time: str,
    audit_lane: str,
    audit_record_id: str,
    audit_content_hash: str,
) -> dict[str, Any]:
    is_statement = bool(
        handle.projection_ref and handle.projection_ref.row_kind == "fragrance_statement_current_window"
    )
    text_artifact_type = "review_body"
    producer_row_kind = "basenotes_statement_body_text" if is_statement else "basenotes_review_body_text"
    record: dict[str, Any] = {
        "record_id": record_id,
        "raw_anchor": packet.packet_id,
        "lane_namespace": BASENOTES_CLEANING_SILVER_LANE,
        "producer_id": _SILVER_PRODUCER_ID,
        "schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
        "producer_schema_version": BASENOTES_SILVER_PRODUCER_SCHEMA_VERSION,
        "content_hash": "",
        "content_hash_basis": _CONTENT_HASH_BASIS,
        "record_kind": "observation",
        "payload_kind": "TextObservation",
        "producer_row_kind": producer_row_kind,
        "source_family": packet.source_family,
        "source_surface": packet.source_surface,
        "observed_at": capture_time,
        "captured_at": capture_time,
        "raw_refs": [_handle_raw_ref(handle)],
        "derived_refs": [
            {
                "edge_type": "derived_from_record",
                "raw_anchor": packet.packet_id,
                "lane_namespace": audit_lane,
                "record_id": audit_record_id,
                "content_hash": audit_content_hash,
                "content_hash_basis": _CONTENT_HASH_BASIS,
            }
        ],
        "payload": {
            "observation": {
                "subject": _silver_subject(handle),
                "text_artifact_type": text_artifact_type,
                "text_value": cleaned_text,
                "text_hash": f"sha256:{hashlib.sha256(cleaned_text.encode('utf-8')).hexdigest()}",
                "text_posture": {
                    "kind": "observed",
                    "reason_code": None,
                    "reason_detail": None,
                },
                "coverage_window": {"start": None, "end": None},
            }
        },
        "provenance": {
            "cleaning_method_id": BASENOTES_CLEANING_METHOD_ID,
        },
        "non_claims": sorted(
            {
                "not_corpus_completeness",
                "not_demand_signal",
                "not_judgment",
                "not_metric_observation_promotion",
                "not_sentiment_analysis",
            }
        ),
    }
    record["content_hash"] = f"sha256:{_content_hash(record)}"
    return record


def _silver_subject(handle: CleaningInputHandle) -> dict[str, Any]:
    subject: dict[str, Any] = {
        "text_handle_id": handle.handle_id,
        "source_surface": handle.source_surface,
    }
    if handle.projection_ref is not None:
        subject["projection_row_id"] = handle.projection_ref.row_id
        subject["projection_row_kind"] = handle.projection_ref.row_kind
    return subject


def _known_capture_time(packet: SourceCapturePacket) -> str:
    if packet.timing.capture_time.status != VisibleFactStatus.KNOWN or not packet.timing.capture_time.value:
        raise ValueError(
            "Basenotes Cleaning lake records require a known capture_time "
            "for observed_at and captured_at."
        )
    return packet.timing.capture_time.value


def _coverage(cleaning_packet: CleaningPacket) -> dict[str, Any]:
    residual_set = {BASENOTES_RATING_METRIC_RESIDUAL}
    residual_set.update(
        residual
        for handle in cleaning_packet.handles
        for residual in handle.residuals
    )
    residuals = sorted(residual_set)
    return {
        "basis": "basenotes_current_window_cleaning_packet",
        "current_window_only": True,
        "full_review_corpus_captured": False,
        "full_statement_corpus_captured": False,
        "handle_count": len(cleaning_packet.handles),
        "transform_entry_count": len(cleaning_packet.transform_ledger),
        "residuals": residuals,
        "raw_pull_triggers": sorted(
            {
                trigger
                for handle in cleaning_packet.handles
                for trigger in handle.raw_pull_triggers
            }
        ),
    }


def _handle_raw_ref(handle: CleaningInputHandle) -> dict[str, str | None]:
    anchor = handle.raw_anchor
    return {
        "ref_type": "raw_packet",
        "packet_id": anchor.packet_id,
        "slice_id": anchor.slice_id,
        "file_id": anchor.file_id,
        "relative_packet_path": anchor.relative_packet_path,
        "sha256": anchor.sha256,
        "hash_basis": anchor.hash_basis,
    }


def _raw_refs(cleaning_packet: CleaningPacket) -> list[dict[str, str | None]]:
    refs: dict[tuple[str | None, ...], dict[str, str | None]] = {}
    for handle in cleaning_packet.handles:
        ref = _handle_raw_ref(handle)
        key = tuple(ref[field] for field in sorted(ref))
        refs[key] = ref
    return [refs[key] for key in sorted(refs)]


def _projection_refs(cleaning_packet: CleaningPacket) -> list[dict[str, Any]]:
    return _dedupe_refs(
        handle.projection_ref.model_dump(mode="json")
        for handle in cleaning_packet.handles
        if handle.projection_ref is not None
    )


def _ecr_refs(cleaning_packet: CleaningPacket) -> list[dict[str, Any]]:
    return _dedupe_refs(
        handle.ecr_ref.model_dump(mode="json")
        for handle in cleaning_packet.handles
        if handle.ecr_ref is not None
    )


def _dedupe_refs(dumps: Any) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for ref in dumps:
        key = json.dumps(ref, sort_keys=True, separators=(",", ":"))
        if key not in seen:
            seen.add(key)
            out.append(ref)
    return out


def _content_hash(record: dict[str, Any]) -> str:
    canonical = dict(record)
    canonical.pop("content_hash", None)
    return hashlib.sha256(_canonical_json_bytes(canonical)).hexdigest()


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


__all__ = [
    "CLEANING_AUDIT_PACK_SCHEMA_VERSION",
    "DISCRIMINATOR_LOCALITY_NON_CLAIM",
    "BASENOTES_CLEANING_AUDIT_LANE",
    "BASENOTES_CLEANING_METHOD_ID",
    "BASENOTES_CLEANING_SILVER_LANE",
    "BasenotesCleaningLakeResult",
    "derive_basenotes_cleaning_into_lake",
    "basenotes_cleaning_audit_pack_payload",
    "basenotes_post_cleaned_silver_records",
]
