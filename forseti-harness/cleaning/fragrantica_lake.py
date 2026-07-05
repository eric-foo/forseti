"""Persist Fragrantica Cleaning output into the Data Lake.

The verified read half lives on ``DataLakeRoot``. This adapter reads a committed
Fragrantica raw packet by key, rebuilds the mechanical Fragrantica projection,
builds the source-family Cleaning packet, and appends two kinds of derived
record:

1. one raw-anchored **Cleaning audit pack** (``schema_version`` =
   ``cleaning_audit_pack_v0``, ``record_family`` = ``processing_audit``) under
   lane ``cleaning_fragrantica_audit`` carrying the full transform ledger; and
2. zero or more **post-cleaned Silver** ``TextObservation`` records under lane
   ``cleaning_fragrantica_silver`` (one per review-card handle) that carry only
   the cleaned review text plus a one-way provenance pointer back to the audit
   pack.

Boundary: the full transform ledger is processing evidence, not a Silver fact
record (Silver ``record_kind`` stays closed to entity/relationship/observation).
The audit pack's ``record_family``/``audit_kind`` are local descriptive fields of
``cleaning_audit_pack_v0`` only and carry no Data-Lake-wide dispatch authority
unless a generic derived-record envelope is separately ratified. This adapter
does not write lake core fields, change raw, decide sentiment, infer demand, bind
Evidence Units, or make Judgment claims.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cleaning.fragrantica import build_fragrantica_cleaning_packet
from cleaning.models import (
    CLEANING_CORE_VERSION,
    REQUIRED_NON_CLAIMS,
    CleaningInputHandle,
    CleaningPacket,
)
from harness_utils import generate_ulid
from source_capture.fragrantica_projection import (
    FRAGRANTICA_PROJECTION_CERTIFICATION,
    FRAGRANTICA_PROJECTION_METHOD,
    FRAGRANTICA_PROJECTION_VERSION,
    build_fragrantica_projection,
)
from source_capture.models import SourceCapturePacket, VisibleFactStatus
from data_lake.silver_record import append_silver_record
from data_lake.canonical_json import canonical_record_bytes as _json_bytes

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


FRAGRANTICA_CLEANING_AUDIT_LANE = "cleaning_fragrantica_audit"
FRAGRANTICA_CLEANING_SILVER_LANE = "cleaning_fragrantica_silver"
CLEANING_AUDIT_PACK_SCHEMA_VERSION = "cleaning_audit_pack_v0"
SILVER_VAULT_RECORD_SCHEMA_VERSION = "silver_vault_record_v0"
FRAGRANTICA_AUDIT_PACK_PRODUCER_SCHEMA_VERSION = "fragrantica_cleaning_audit_pack_v1"
FRAGRANTICA_SILVER_PRODUCER_SCHEMA_VERSION = "fragrantica_cleaning_silver_textobservation_v1"
FRAGRANTICA_CLEANING_METHOD_ID = "fragrantica_cleaning_method_v0"
REVIEW_TEXT_NORMALIZATION_RULE = "fragrantica_review_text_whitespace_normalization"
REVIEW_VOTE_CARRY_RULE = "fragrantica_source_visible_vote_field_carry"
FRAGRANTICA_SILVER_METRIC_PRODUCER_SCHEMA_VERSION = (
    "fragrantica_cleaning_silver_metricobservation_v1"
)

# Review-vote metrics emitted as post-cleaned Silver MetricObservations:
# (vote_field, metric_name, unit). Non-numeric votes (gender/relation) and the
# season/day/night votes are deferred as named residuals.
_REVIEW_VOTE_METRIC_SPECS: tuple[tuple[str, str, str], ...] = (
    ("rating", "review_rating", "fragrantica_rating"),
    ("longevity", "review_longevity_vote", "fragrantica_vote_ordinal"),
    ("sillage", "review_sillage_vote", "fragrantica_vote_ordinal"),
)

# Reviewer-driven anti-lock-in guard (FCR-04 closure): the audit pack's
# discriminator fields are local to cleaning_audit_pack_v0 and confer no lake-wide
# dispatch authority until a generic derived-record envelope is ratified.
DISCRIMINATOR_LOCALITY_NON_CLAIM = (
    "record_family_and_audit_kind_local_to_cleaning_audit_pack_v0_no_lake_wide_dispatch"
)

_CONTENT_HASH_BASIS = "canonical_json_excluding_content_hash"
_AUDIT_PRODUCER_ID = (
    "forseti-harness.cleaning.fragrantica_lake.derive_fragrantica_cleaning_into_lake#audit"
)
_SILVER_PRODUCER_ID = (
    "forseti-harness.cleaning.fragrantica_lake.derive_fragrantica_cleaning_into_lake#silver"
)


@dataclass(frozen=True)
class FragranticaCleaningLakeResult:
    """Outputs of one Fragrantica Cleaning derivation into the lake."""

    cleaning_packet: CleaningPacket
    audit_record: dict[str, Any]
    audit_path: Path
    silver_records: list[dict[str, Any]]
    silver_paths: list[Path]


def derive_fragrantica_cleaning_into_lake(
    *,
    data_root: "DataLakeRoot",
    packet_id: str,
    record_id: str | None = None,
) -> FragranticaCleaningLakeResult:
    """Build and append the Fragrantica Cleaning audit pack + post-cleaned Silver.

    Re-derive = a fresh audit-pack sibling. A caller-supplied ``record_id`` names
    the audit pack and is still create-only through ``DataLakeRoot.append_record``;
    post-cleaned Silver records always use fresh ids. The audit pack is appended
    first so its content hash can be threaded into each Silver provenance pointer.
    """
    loaded = data_root.load_raw_packet(packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    projection = build_fragrantica_projection(
        packet=packet,
        raw_file_bytes_by_file_id=loaded.bodies,
    )
    cleaning_packet = build_fragrantica_cleaning_packet(projection)

    audit_seed = record_id if record_id is not None else generate_ulid()
    audit_record_name = f"{audit_seed}.json"
    audit_record = fragrantica_cleaning_audit_pack_payload(
        packet=packet,
        cleaning_packet=cleaning_packet,
        record_id=audit_record_name,
    )
    audit_path = data_root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=FRAGRANTICA_CLEANING_AUDIT_LANE,
        record_id=audit_record_name,
        data=_json_bytes(audit_record),
    )

    silver_records = fragrantica_post_cleaned_silver_records(
        packet=packet,
        cleaning_packet=cleaning_packet,
        audit_lane=FRAGRANTICA_CLEANING_AUDIT_LANE,
        audit_record_id=audit_record_name,
        audit_content_hash=audit_record["content_hash"],
    )
    # Text observations first, then per-review vote MetricObservations, so callers
    # and tests can rely on a TextObservation leading the list.
    silver_records.extend(
        fragrantica_post_cleaned_silver_metric_records(
            packet=packet,
            cleaning_packet=cleaning_packet,
            audit_lane=FRAGRANTICA_CLEANING_AUDIT_LANE,
            audit_record_id=audit_record_name,
            audit_content_hash=audit_record["content_hash"],
        )
    )
    silver_paths: list[Path] = []
    for silver_record in silver_records:
        # Route every Silver record through the validating front-door: a blurred
        # record (bad record_kind, a ledger inside a fact, broken metric posture)
        # raises before any bytes are written. The audit pack above stays on the
        # generic writer because it is intentionally NOT a Silver record.
        silver_paths.append(
            append_silver_record(
                data_root,
                raw_anchor=packet_id,
                lane=FRAGRANTICA_CLEANING_SILVER_LANE,
                record_id=silver_record["record_id"],
                record=silver_record,
            )
        )

    return FragranticaCleaningLakeResult(
        cleaning_packet=cleaning_packet,
        audit_record=audit_record,
        audit_path=audit_path,
        silver_records=silver_records,
        silver_paths=silver_paths,
    )


def fragrantica_cleaning_audit_pack_payload(
    *,
    packet: SourceCapturePacket,
    cleaning_packet: CleaningPacket,
    record_id: str,
) -> dict[str, Any]:
    """Return the Cleaning audit-pack record payload before lake append.

    This is a derived processing-audit sibling, not a Silver fact record: it
    carries no ``record_kind`` and is never a Silver Vault envelope.
    """
    capture_time = _known_capture_time(packet)
    record: dict[str, Any] = {
        "schema_version": CLEANING_AUDIT_PACK_SCHEMA_VERSION,
        "record_family": "processing_audit",
        "audit_kind": "cleaning_transform_audit",
        "record_id": record_id,
        "raw_anchor": packet.packet_id,
        "lane_namespace": FRAGRANTICA_CLEANING_AUDIT_LANE,
        "producer_id": _AUDIT_PRODUCER_ID,
        "producer_schema_version": FRAGRANTICA_AUDIT_PACK_PRODUCER_SCHEMA_VERSION,
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
            "projection_method": FRAGRANTICA_PROJECTION_METHOD,
            "projection_version": FRAGRANTICA_PROJECTION_VERSION,
            "projection_certification": FRAGRANTICA_PROJECTION_CERTIFICATION,
            "handle_count": len(cleaning_packet.handles),
            "transform_entry_count": len(cleaning_packet.transform_ledger),
            "cleaning_packet": cleaning_packet.model_dump(mode="json"),
        },
        "non_claims": sorted(
            {
                *REQUIRED_NON_CLAIMS,
                "not_archive_completeness",
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


def fragrantica_post_cleaned_silver_records(
    *,
    packet: SourceCapturePacket,
    cleaning_packet: CleaningPacket,
    audit_lane: str,
    audit_record_id: str,
    audit_content_hash: str,
) -> list[dict[str, Any]]:
    """Return one post-cleaned Silver ``TextObservation`` per review-card handle.

    The cleaned review text is the whitespace-normalized ``transformed_value`` of
    the review-text normalization ledger entry. Each record links back to the
    audit pack by lane namespace, record id, and content hash.
    """
    capture_time = _known_capture_time(packet)
    handle_by_id = {handle.handle_id: handle for handle in cleaning_packet.handles}
    records: list[dict[str, Any]] = []
    for entry in cleaning_packet.transform_ledger:
        if entry.transform.method_or_rule != REVIEW_TEXT_NORMALIZATION_RULE:
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


def fragrantica_post_cleaned_silver_metric_records(
    *,
    packet: SourceCapturePacket,
    cleaning_packet: CleaningPacket,
    audit_lane: str,
    audit_record_id: str,
    audit_content_hash: str,
) -> list[dict[str, Any]]:
    """Return post-cleaned Silver ``MetricObservation`` records for review votes.

    One record per numeric review vote carried through Cleaning (rating,
    longevity, sillage), read from the source-visible vote-carry ledger entry so
    each metric is a post-cleaned fact linking back to the same audit pack as its
    review's text observation. Non-numeric votes (gender/relation), the
    season/day/night votes, and the product-level aggregate rating (not carried
    through Cleaning) are deferred as named residuals.
    """
    capture_time = _known_capture_time(packet)
    handle_by_id = {handle.handle_id: handle for handle in cleaning_packet.handles}
    records: list[dict[str, Any]] = []
    for entry in cleaning_packet.transform_ledger:
        if entry.transform.method_or_rule != REVIEW_VOTE_CARRY_RULE:
            continue
        handle = handle_by_id.get(entry.input_handle_id)
        carried = entry.transform.transformed_value
        if handle is None or carried is None:
            continue
        try:
            votes = json.loads(carried)
        except (TypeError, ValueError):
            continue
        if not isinstance(votes, dict):
            continue
        for vote_field, metric_name, unit in _REVIEW_VOTE_METRIC_SPECS:
            value = votes.get(vote_field)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            records.append(
                _post_cleaned_metric_record(
                    packet=packet,
                    handle=handle,
                    metric_name=metric_name,
                    metric_value=value,
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
    record: dict[str, Any] = {
        "record_id": record_id,
        "raw_anchor": packet.packet_id,
        "lane_namespace": FRAGRANTICA_CLEANING_SILVER_LANE,
        "producer_id": _SILVER_PRODUCER_ID,
        "schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
        "producer_schema_version": FRAGRANTICA_SILVER_PRODUCER_SCHEMA_VERSION,
        "content_hash": "",
        "content_hash_basis": _CONTENT_HASH_BASIS,
        "record_kind": "observation",
        "payload_kind": "TextObservation",
        "producer_row_kind": "fragrantica_review_body_text",
        "source_family": packet.source_family,
        "source_surface": packet.source_surface,
        "observed_at": capture_time,
        "captured_at": capture_time,
        "raw_refs": [_handle_raw_ref(handle)],
        # Standard Silver-header lineage: this record is generated from a prior
        # derived record (the audit pack), so the link lives here, not a sidecar.
        "derived_refs": [
            {
                "edge_type": "derived_from_record",
                "lane_namespace": audit_lane,
                "record_id": audit_record_id,
                "content_hash": audit_content_hash,
                "content_hash_basis": _CONTENT_HASH_BASIS,
            }
        ],
        "payload": {
            "observation": {
                "subject": _silver_subject(handle),
                "text_artifact_type": "review_body",
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
            "cleaning_method_id": FRAGRANTICA_CLEANING_METHOD_ID,
        },
        "non_claims": sorted(
            {
                "not_archive_completeness",
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
        "lane_namespace": FRAGRANTICA_CLEANING_SILVER_LANE,
        "producer_id": _SILVER_PRODUCER_ID,
        "schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
        "producer_schema_version": FRAGRANTICA_SILVER_METRIC_PRODUCER_SCHEMA_VERSION,
        "content_hash": "",
        "content_hash_basis": _CONTENT_HASH_BASIS,
        "record_kind": "observation",
        "payload_kind": "MetricObservation",
        "producer_row_kind": "fragrantica_review_vote",
        "source_family": packet.source_family,
        "source_surface": packet.source_surface,
        "observed_at": capture_time,
        "captured_at": capture_time,
        "raw_refs": [_handle_raw_ref(handle)],
        # Same standard-header lineage as the TextObservation: generated from the
        # audit pack, so the link lives in derived_refs.
        "derived_refs": [
            {
                "edge_type": "derived_from_record",
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
            "cleaning_method_id": FRAGRANTICA_CLEANING_METHOD_ID,
        },
        "non_claims": sorted(
            {
                "not_archive_completeness",
                "not_demand_signal",
                "not_judgment",
                "not_sentiment_analysis",
            }
        ),
    }
    record["content_hash"] = f"sha256:{_content_hash(record)}"
    return record


def _silver_subject(handle: CleaningInputHandle) -> dict[str, Any]:
    """Minimal source-visible subject; omit fields that are not present."""
    subject: dict[str, Any] = {
        "review_handle_id": handle.handle_id,
        "source_surface": handle.source_surface,
    }
    if handle.projection_ref is not None:
        subject["review_row_id"] = handle.projection_ref.row_id
    return subject


def _known_capture_time(packet: SourceCapturePacket) -> str:
    if packet.timing.capture_time.status != VisibleFactStatus.KNOWN or not packet.timing.capture_time.value:
        raise ValueError(
            "Fragrantica Cleaning lake records require a known capture_time "
            "for observed_at and captured_at."
        )
    return packet.timing.capture_time.value


def _coverage(cleaning_packet: CleaningPacket) -> dict[str, Any]:
    residuals = sorted(
        {
            residual
            for handle in cleaning_packet.handles
            for residual in handle.residuals
        }
    )
    return {
        "basis": "fragrantica_current_window_cleaning_packet",
        "current_window_only": True,
        "full_archive_captured": False,
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
    "FRAGRANTICA_CLEANING_AUDIT_LANE",
    "FRAGRANTICA_CLEANING_METHOD_ID",
    "FRAGRANTICA_CLEANING_SILVER_LANE",
    "FragranticaCleaningLakeResult",
    "derive_fragrantica_cleaning_into_lake",
    "fragrantica_cleaning_audit_pack_payload",
    "fragrantica_post_cleaned_silver_records",
    "fragrantica_post_cleaned_silver_metric_records",
]
