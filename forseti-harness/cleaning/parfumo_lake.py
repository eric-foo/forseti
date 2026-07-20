"""Persist Parfumo Cleaning output into the Data Lake."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cleaning._shared import (
    ecr_refs as _ecr_refs,
    handle_source_ref as _handle_source_ref,
    source_refs as _source_refs,
)
from cleaning.models import CLEANING_CORE_VERSION, REQUIRED_NON_CLAIMS, CleaningInputHandle, CleaningPacket
from cleaning.parfumo import (
    PARFUMO_RATING_CARRY_RULE,
    build_parfumo_cleaning_packet_from_source,
)
from data_lake.canonical_json import (
    canonical_record_bytes as _json_bytes,
    record_content_hash as _content_hash,
)
from data_lake.silver_record import append_silver_record
from harness_utils import generate_ulid
from source_capture.models import SourceCapturePacket, VisibleFactStatus
from source_capture.parfumo_projection import (
    PARFUMO_TARGETED_CONTENT_SCHEMA_VERSION,
    PARFUMO_TARGETED_PARSER_VERSION,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


PARFUMO_CLEANING_AUDIT_LANE = "cleaning_parfumo_audit"
PARFUMO_CLEANING_SILVER_LANE = "cleaning_parfumo_silver"
CLEANING_AUDIT_PACK_SCHEMA_VERSION = "cleaning_audit_pack_v0"
SILVER_VAULT_RECORD_SCHEMA_VERSION = "silver_vault_record_v0"
PARFUMO_AUDIT_PACK_PRODUCER_SCHEMA_VERSION = "parfumo_cleaning_audit_pack_v2"
PARFUMO_SILVER_PRODUCER_SCHEMA_VERSION = "parfumo_cleaning_silver_textobservation_v3"
PARFUMO_SILVER_METRIC_PRODUCER_SCHEMA_VERSION = "parfumo_cleaning_silver_metricobservation_v3"
PARFUMO_CLEANING_METHOD_ID = "parfumo_cleaning_method_v1"
TEXT_NORMALIZATION_RULE = "parfumo_text_whitespace_normalization"
PARFUMO_RATING_METRIC_ABSENT_RESIDUAL = (
    "parfumo_review_rating_metric_absent_no_source_visible_numeric_rating"
)
_REVIEW_RATING_METRIC_SPECS: tuple[tuple[str, str, str], ...] = (
    ("rating", "review_rating", "parfumo_rating_0_10"),
)

DISCRIMINATOR_LOCALITY_NON_CLAIM = (
    "record_family_and_audit_kind_local_to_cleaning_audit_pack_v0_no_lake_wide_dispatch"
)

_CONTENT_HASH_BASIS = "canonical_json_excluding_content_hash"
_AUDIT_PRODUCER_ID = "forseti-harness.cleaning.parfumo_lake.derive_parfumo_cleaning_into_lake#audit"
_SILVER_PRODUCER_ID = "forseti-harness.cleaning.parfumo_lake.derive_parfumo_cleaning_into_lake#silver"


@dataclass(frozen=True)
class ParfumoCleaningLakeResult:
    """Outputs of one Parfumo Cleaning derivation into the lake."""

    cleaning_packet: CleaningPacket
    audit_record: dict[str, Any]
    audit_path: Path
    silver_records: list[dict[str, Any]]
    silver_paths: list[Path]


def derive_parfumo_cleaning_into_lake(
    *,
    data_root: "DataLakeRoot",
    packet_id: str,
    record_id: str | None = None,
) -> ParfumoCleaningLakeResult:
    """Build and append the Parfumo Cleaning audit pack plus post-cleaned Silver."""
    loaded = data_root.load_raw_packet(packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    cleaning_packet = build_parfumo_cleaning_packet_from_source(
        packet=packet,
        file_bytes_by_file_id=loaded.bodies,
    )

    audit_seed = record_id if record_id is not None else generate_ulid()
    audit_record_name = f"{audit_seed}.json"
    audit_record = parfumo_cleaning_audit_pack_payload(
        packet=packet,
        cleaning_packet=cleaning_packet,
        record_id=audit_record_name,
    )
    audit_path = data_root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=PARFUMO_CLEANING_AUDIT_LANE,
        record_id=audit_record_name,
        data=_json_bytes(audit_record),
    )

    silver_records = parfumo_post_cleaned_silver_records(
        packet=packet,
        cleaning_packet=cleaning_packet,
        audit_lane=PARFUMO_CLEANING_AUDIT_LANE,
        audit_record_id=audit_record_name,
        audit_content_hash=audit_record["content_hash"],
    )
    silver_records.extend(
        parfumo_post_cleaned_silver_metric_records(
            packet=packet,
            cleaning_packet=cleaning_packet,
            audit_lane=PARFUMO_CLEANING_AUDIT_LANE,
            audit_record_id=audit_record_name,
            audit_content_hash=audit_record["content_hash"],
        )
    )
    silver_paths: list[Path] = []
    for silver_record in silver_records:
        silver_paths.append(
            append_silver_record(
                data_root,
                raw_anchor=packet_id,
                lane=PARFUMO_CLEANING_SILVER_LANE,
                record_id=silver_record["record_id"],
                record=silver_record,
            )
        )

    return ParfumoCleaningLakeResult(
        cleaning_packet=cleaning_packet,
        audit_record=audit_record,
        audit_path=audit_path,
        silver_records=silver_records,
        silver_paths=silver_paths,
    )


def parfumo_cleaning_audit_pack_payload(
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
        "lane_namespace": PARFUMO_CLEANING_AUDIT_LANE,
        "producer_id": _AUDIT_PRODUCER_ID,
        "producer_schema_version": PARFUMO_AUDIT_PACK_PRODUCER_SCHEMA_VERSION,
        "content_hash": "",
        "content_hash_basis": _CONTENT_HASH_BASIS,
        "source_family": packet.source_family,
        "source_surface": packet.source_surface,
        "captured_at": capture_time,
        "input_refs": {
            "source_refs": _source_refs(cleaning_packet),
            "ecr_refs": _ecr_refs(cleaning_packet),
        },
        "coverage": _coverage(cleaning_packet),
        "payload": {
            "cleaning_core_version": CLEANING_CORE_VERSION,
            "content_schema_version": PARFUMO_TARGETED_CONTENT_SCHEMA_VERSION,
            "extractor_version": PARFUMO_TARGETED_PARSER_VERSION,
            "legacy_raw_decoder_supported": True,
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
                "not_sentiment_analysis",
                "not_silver_fact",
                DISCRIMINATOR_LOCALITY_NON_CLAIM,
            }
        ),
    }
    record["content_hash"] = f"sha256:{_content_hash(record)}"
    return record


def parfumo_post_cleaned_silver_records(
    *,
    packet: SourceCapturePacket,
    cleaning_packet: CleaningPacket,
    audit_lane: str,
    audit_record_id: str,
    audit_content_hash: str,
) -> list[dict[str, Any]]:
    """Return one post-cleaned Silver TextObservation per Parfumo text-row handle."""
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


def parfumo_post_cleaned_silver_metric_records(
    *,
    packet: SourceCapturePacket,
    cleaning_packet: CleaningPacket,
    audit_lane: str,
    audit_record_id: str,
    audit_content_hash: str,
) -> list[dict[str, Any]]:
    """Return observed Silver MetricObservations for source-visible Parfumo review ratings."""
    capture_time = _known_capture_time(packet)
    handle_by_id = {handle.handle_id: handle for handle in cleaning_packet.handles}
    records: list[dict[str, Any]] = []
    for entry in cleaning_packet.transform_ledger:
        if entry.transform.method_or_rule != PARFUMO_RATING_CARRY_RULE:
            continue
        handle = handle_by_id.get(entry.input_handle_id)
        carried = entry.transform.transformed_value
        if handle is None or carried is None:
            continue
        try:
            rating_fields = json.loads(carried)
        except (TypeError, ValueError):
            continue
        if not isinstance(rating_fields, dict):
            continue
        for rating_field, metric_name, unit in _REVIEW_RATING_METRIC_SPECS:
            value = rating_fields.get(rating_field)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            records.append(
                _post_cleaned_metric_record(
                    packet=packet,
                    handle=handle,
                    metric_name=metric_name,
                    metric_value=float(value),
                    unit=unit,
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
        handle.source_row_kind == "fragrance_statement_current_window"
    )
    text_artifact_type = "review_body"
    producer_row_kind = "parfumo_statement_body_text" if is_statement else "parfumo_review_body_text"
    record: dict[str, Any] = {
        "record_id": record_id,
        "raw_anchor": packet.packet_id,
        "lane_namespace": PARFUMO_CLEANING_SILVER_LANE,
        "producer_id": _SILVER_PRODUCER_ID,
        "schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
        "producer_schema_version": PARFUMO_SILVER_PRODUCER_SCHEMA_VERSION,
        "content_hash": "",
        "content_hash_basis": _CONTENT_HASH_BASIS,
        "record_kind": "observation",
        "payload_kind": "TextObservation",
        "producer_row_kind": producer_row_kind,
        "source_family": packet.source_family,
        "source_surface": packet.source_surface,
        "observed_at": capture_time,
        "captured_at": capture_time,
        "raw_refs": [_handle_source_ref(handle)],
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
            "cleaning_method_id": PARFUMO_CLEANING_METHOD_ID,
        },
        "non_claims": sorted(
            {
                "not_corpus_completeness",
                "not_demand_signal",
                "not_judgment",
                "not_sentiment_analysis",
            }
        ),
    }
    record["content_hash"] = f"sha256:{_content_hash(record)}"
    return record


def _post_cleaned_metric_record(
    *,
    packet: SourceCapturePacket,
    handle: CleaningInputHandle,
    metric_name: str,
    metric_value: float,
    unit: str,
    record_id: str,
    capture_time: str,
    audit_lane: str,
    audit_record_id: str,
    audit_content_hash: str,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "record_id": record_id,
        "raw_anchor": packet.packet_id,
        "lane_namespace": PARFUMO_CLEANING_SILVER_LANE,
        "producer_id": _SILVER_PRODUCER_ID,
        "schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
        "producer_schema_version": PARFUMO_SILVER_METRIC_PRODUCER_SCHEMA_VERSION,
        "content_hash": "",
        "content_hash_basis": _CONTENT_HASH_BASIS,
        "record_kind": "observation",
        "payload_kind": "MetricObservation",
        "producer_row_kind": "parfumo_review_rating",
        "source_family": packet.source_family,
        "source_surface": packet.source_surface,
        "observed_at": capture_time,
        "captured_at": capture_time,
        "raw_refs": [_handle_source_ref(handle)],
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
                "metric_name": metric_name,
                "metric_value": metric_value,
                "metric_posture": {
                    "kind": "observed",
                    "reason_code": None,
                    "reason_detail": None,
                },
                "coverage_window": {"start": None, "end": None},
                "source_surface": packet.source_surface,
                "source_publication_or_event": None,
                "source_surface_count_candidates": [],
                "unit": unit,
            }
        },
        "provenance": {
            "cleaning_method_id": PARFUMO_CLEANING_METHOD_ID,
        },
        "non_claims": sorted(
            {
                "not_corpus_completeness",
                "not_demand_signal",
                "not_judgment",
                "not_sentiment_analysis",
            }
        ),
    }
    record["content_hash"] = f"sha256:{_content_hash(record)}"
    return record


# helper-delta: text-keyed subject (text_handle_id/source_row_id/
# source_row_kind), unlike fragrantica_lake's review-keyed subject -- stays local.
def _silver_subject(handle: CleaningInputHandle) -> dict[str, Any]:
    subject: dict[str, Any] = {
        "text_handle_id": handle.handle_id,
        "source_surface": handle.source_surface,
    }
    if handle.source_row_id is not None:
        subject["source_row_id"] = handle.source_row_id
        subject["source_row_kind"] = handle.source_row_kind
    return subject


# helper-delta: error message names Parfumo; otherwise matches the local copies
# in fragrantica_lake/basenotes_lake -- stays local.
def _known_capture_time(packet: SourceCapturePacket) -> str:
    if packet.timing.capture_time.status != VisibleFactStatus.KNOWN or not packet.timing.capture_time.value:
        raise ValueError(
            "Parfumo Cleaning lake records require a known capture_time "
            "for observed_at and captured_at."
        )
    return packet.timing.capture_time.value


def _coverage(cleaning_packet: CleaningPacket) -> dict[str, Any]:
    residual_set = {
        residual
        for handle in cleaning_packet.handles
        for residual in handle.residuals
    }
    if not _has_source_visible_rating_metric(cleaning_packet):
        residual_set.add(PARFUMO_RATING_METRIC_ABSENT_RESIDUAL)
    residuals = sorted(residual_set)
    return {
        "basis": "parfumo_current_window_cleaning_packet",
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


def _has_source_visible_rating_metric(cleaning_packet: CleaningPacket) -> bool:
    return any(
        entry.transform.method_or_rule == PARFUMO_RATING_CARRY_RULE
        for entry in cleaning_packet.transform_ledger
    )


__all__ = [
    "CLEANING_AUDIT_PACK_SCHEMA_VERSION",
    "DISCRIMINATOR_LOCALITY_NON_CLAIM",
    "PARFUMO_CLEANING_AUDIT_LANE",
    "PARFUMO_CLEANING_METHOD_ID",
    "PARFUMO_CLEANING_SILVER_LANE",
    "ParfumoCleaningLakeResult",
    "derive_parfumo_cleaning_into_lake",
    "parfumo_cleaning_audit_pack_payload",
    "parfumo_post_cleaned_silver_metric_records",
    "parfumo_post_cleaned_silver_records",
]
