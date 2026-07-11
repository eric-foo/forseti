"""Derive generic Retail/PDP Silver records from one exact projection record.

The producer is intentionally retailer-generic. Amazon is the first proof
source, not a lane boundary. Inputs are caller-pinned projection record ids;
the producer never guesses which append-only sibling is current.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable

from data_lake.silver_lineage import (
    SilverAnchor,
    SilverDerivedRef,
    SilverLineage,
    SilverRawRef,
    SilverRowLocator,
    SilverSourceObject,
    is_silver_record_source_backed_complete,
)
from data_lake.silver_record import append_silver_record, validate_silver_vault_record
from harness_utils import generate_ulid
from source_capture.models import SourceCapturePacket, SourceCaptureSlice, VisibleFactStatus
from source_capture.retail_pdp_projection import (
    PROJECTION_RETAIL_PDP_LANE,
    RetailPdpProjectionPacket,
    RetailPdpProjectionRow,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


RETAIL_PDP_SILVER_LANE = "retail_pdp_silver"
RETAIL_PDP_SILVER_SCHEMA_VERSION = "silver_vault_record_v0"
RETAIL_PDP_SILVER_PRODUCER_SCHEMA_VERSION = "retail_pdp_silver_v0"

_CONTENT_HASH_BASIS = "canonical_json_excluding_content_hash"
_DERIVED_HASH_BASIS = "derived_record_bytes"
_PRODUCER_ID = (
    "forseti-harness.source_capture.retail_pdp_silver"
    ".derive_retail_pdp_silver_from_projection"
)
_SELECTED_ROW_KINDS = frozenset(
    {"retail_pdp_product", "retail_variant_offer", "retail_review_substrate"}
)
_NON_CLAIMS = (
    "not_cleaning",
    "not_complete_amazon_demand_projection",
    "not_exact_inventory_quantity",
    "not_exact_sold_units",
    "not_judgment",
    "not_sibling_selection_policy",
)


class RetailPdpSilverError(ValueError):
    """The pinned projection cannot produce truthful Retail/PDP Silver records."""


@dataclass(frozen=True)
class RetailPdpSilverResult:
    projection_record_id: str
    records: list[dict[str, Any]]
    paths: list[Path]


def derive_retail_pdp_silver_from_projection(
    *, data_root: "DataLakeRoot", packet_id: str, projection_record_id: str
) -> RetailPdpSilverResult:
    """Read one exact projection record and append its selected Silver semantics."""
    projection_path = data_root.record_path(
        subtree="derived",
        raw_anchor=packet_id,
        lane=PROJECTION_RETAIL_PDP_LANE,
        record_id=projection_record_id,
    )
    if not projection_path.is_file():
        raise RetailPdpSilverError(
            f"Retail/PDP projection record does not exist: {projection_record_id!r}"
        )
    try:
        projection_bytes = projection_path.read_bytes()
        projection = RetailPdpProjectionPacket.model_validate_json(projection_bytes)
    except (OSError, ValueError) as exc:
        raise RetailPdpSilverError(
            f"Retail/PDP projection record is unreadable or invalid: {projection_record_id!r}: {exc}"
        ) from exc
    if projection.packet_id != packet_id:
        raise RetailPdpSilverError(
            "Retail/PDP projection packet_id does not match the requested raw anchor: "
            f"{projection.packet_id!r} != {packet_id!r}"
        )

    loaded = data_root.load_raw_packet(packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    records = build_retail_pdp_silver_records(
        packet=packet,
        projection=projection,
        projection_record_id=projection_record_id,
        projection_sha256=hashlib.sha256(projection_bytes).hexdigest(),
    )
    # Validate the full batch before the first append; malformed input cannot
    # create a partial-success record prefix.
    for record in records:
        validate_silver_vault_record(record)
        if not is_silver_record_source_backed_complete(record):
            raise RetailPdpSilverError(
                f"Retail/PDP Silver record is not source-backed complete: {record['record_id']}"
            )

    paths = [
        append_silver_record(
            data_root,
            raw_anchor=packet_id,
            lane=RETAIL_PDP_SILVER_LANE,
            record_id=record["record_id"],
            record=record,
        )
        for record in records
    ]
    return RetailPdpSilverResult(projection_record_id, records, paths)


def build_retail_pdp_silver_records(
    *,
    packet: SourceCapturePacket,
    projection: RetailPdpProjectionPacket,
    projection_record_id: str,
    projection_sha256: str,
) -> list[dict[str, Any]]:
    """Build the selected entity/offer/review record set in memory."""
    if projection.packet_id != packet.packet_id:
        raise RetailPdpSilverError("projection and raw packet ids do not match")
    if not projection_sha256.strip():
        raise RetailPdpSilverError("projection derived-record hash must be non-empty")

    selected = [row for row in projection.rows if row.row_kind in _SELECTED_ROW_KINDS]
    _verify_selected_rows(packet, selected)
    products = _one_row_per_key(selected, "retail_pdp_product")
    variants = _one_row_per_key(selected, "retail_variant_offer")
    reviews = _one_row_per_key(selected, "retail_review_substrate")
    if not variants:
        raise RetailPdpSilverError(
            "projection has no retail_variant_offer row; refusing an empty Silver success"
        )

    records: list[dict[str, Any]] = []
    for key, variant in sorted(variants.items()):
        product = products.get(key)
        if product is None:
            raise RetailPdpSilverError(
                f"variant row {variant.row_id!r} has no matching retail_pdp_product context"
            )
        source_slice = _source_slice(packet, variant.raw_ref.slice_id)
        entity_key = _entity_key(variant)
        common = {
            "packet": packet,
            "source_slice": source_slice,
            "entity_key": entity_key,
            "projection_record_id": projection_record_id,
            "projection_sha256": projection_sha256,
        }
        records.append(_entity_record(product_row=product, variant_row=variant, **common))
        records.append(
            _observation_record(
                supporting_rows=(product, variant),
                observed_row=variant,
                payload_kind="RetailOfferObservation",
                observation_kind="retail_offer",
                **common,
            )
        )
        review = reviews.get(key)
        if review is not None:
            records.append(
                _observation_record(
                    supporting_rows=(product, variant, review),
                    observed_row=review,
                    payload_kind="RetailReviewAggregateObservation",
                    observation_kind="retail_review_aggregate",
                    **common,
                )
            )

    orphan_reviews = sorted(set(reviews) - set(variants))
    if orphan_reviews:
        raise RetailPdpSilverError(
            "review substrate row(s) have no matching retailer-local product identity: "
            + ", ".join(f"{slice_id}:{retailer}" for slice_id, retailer in orphan_reviews)
        )
    return records


def _entity_record(
    *,
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
    product_row: RetailPdpProjectionRow,
    variant_row: RetailPdpProjectionRow,
    entity_key: dict[str, str],
    projection_record_id: str,
    projection_sha256: str,
) -> dict[str, Any]:
    lineage = _lineage(
        packet,
        source_slice,
        (product_row, variant_row),
        entity_key,
        projection_record_id,
        projection_sha256,
    )
    record = _base_record(
        packet, source_slice, variant_row.row_kind, "ProductEntity", "entity", lineage
    )
    record["payload"] = {
        "entity": {
            "entity_type": "product",
            "entity_key": entity_key,
            "identity_source": {
                "raw_refs": record["raw_refs"],
                "derived_refs": record["derived_refs"],
            },
        }
    }
    return _finish_record(record)


def _observation_record(
    *,
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
    supporting_rows: tuple[RetailPdpProjectionRow, ...],
    observed_row: RetailPdpProjectionRow,
    entity_key: dict[str, str],
    payload_kind: str,
    observation_kind: str,
    projection_record_id: str,
    projection_sha256: str,
) -> dict[str, Any]:
    lineage = _lineage(
        packet,
        source_slice,
        supporting_rows,
        entity_key,
        projection_record_id,
        projection_sha256,
    )
    record = _base_record(
        packet, source_slice, observed_row.row_kind, payload_kind, "observation", lineage
    )
    residuals = sorted(set(observed_row.residuals))
    record["payload"] = {
        "observation": {
            "subject": {"ref_type": "entity_key", "ref": entity_key},
            "observation_kind": observation_kind,
            "source_visible_fields": observed_row.source_visible_fields,
            "residuals": residuals,
        }
    }
    record["residuals"] = residuals
    return _finish_record(record)


def _base_record(
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
    producer_row_kind: str,
    payload_kind: str,
    record_kind: str,
    lineage: SilverLineage,
) -> dict[str, Any]:
    capture_time = _known_capture_time(source_slice)
    return {
        "record_id": f"{generate_ulid()}.json",
        "raw_anchor": packet.packet_id,
        "lane_namespace": RETAIL_PDP_SILVER_LANE,
        "schema_version": RETAIL_PDP_SILVER_SCHEMA_VERSION,
        "content_hash": "",
        "content_hash_basis": _CONTENT_HASH_BASIS,
        "record_kind": record_kind,
        "payload_kind": payload_kind,
        "producer_row_kind": producer_row_kind,
        "source_family": packet.source_family,
        "observed_at": capture_time,
        "captured_at": capture_time,
        **lineage.to_record_fields(),
        "non_claims": list(_NON_CLAIMS),
    }


def _lineage(
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
    rows: Iterable[RetailPdpProjectionRow],
    entity_key: dict[str, str],
    projection_record_id: str,
    projection_sha256: str,
) -> SilverLineage:
    row_list = list(rows)
    source_url = _known_value(source_slice.locator) or _known_value(packet.source_locator)
    return SilverLineage(
        producer_id=_PRODUCER_ID,
        producer_schema_version=RETAIL_PDP_SILVER_PRODUCER_SCHEMA_VERSION,
        source_surface=packet.source_surface,
        source_object=SilverSourceObject(
            namespace=entity_key["namespace"],
            kind=entity_key["kind"],
            native_id=entity_key["native_id"],
            source_url=source_url,
        ),
        observed_at=_known_capture_time(source_slice),
        captured_at=_known_capture_time(source_slice),
        raw_refs=[_raw_ref(row) for row in row_list],
        derived_refs=[
            SilverDerivedRef(
                raw_anchor=packet.packet_id,
                lane=PROJECTION_RETAIL_PDP_LANE,
                record_id=projection_record_id,
                row_locator=SilverRowLocator(row_id=row.row_id, row_kind=row.row_kind),
                sha256=projection_sha256,
                hash_basis=_DERIVED_HASH_BASIS,
                relation="consumed",
            )
            for row in row_list
        ],
    )


def _raw_ref(row: RetailPdpProjectionRow) -> SilverRawRef:
    return SilverRawRef(
        packet_id=row.raw_ref.packet_id,
        slice_id=row.raw_ref.slice_id,
        file_id=row.raw_anchor.file_id,
        relative_packet_path=row.raw_anchor.relative_packet_path,
        sha256=row.raw_anchor.sha256,
        hash_basis=row.raw_anchor.hash_basis,
        anchor=SilverAnchor(
            kind=row.raw_anchor.anchor_kind, value=row.raw_anchor.anchor_value
        ),
        relation="observed_from",
    )


def _verify_selected_rows(
    packet: SourceCapturePacket, rows: Iterable[RetailPdpProjectionRow]
) -> None:
    files = {item.file_id: item for item in packet.preserved_files}
    slices = {item.slice_id: item for item in packet.source_slices}
    for row in rows:
        if row.raw_ref.packet_id != packet.packet_id:
            raise RetailPdpSilverError(f"projection row {row.row_id!r} points at another packet")
        source_slice = slices.get(row.raw_ref.slice_id)
        if source_slice is None:
            raise RetailPdpSilverError(
                f"projection row {row.row_id!r} points at unknown slice {row.raw_ref.slice_id!r}"
            )
        preserved = files.get(row.raw_anchor.file_id)
        if preserved is None or row.raw_anchor.file_id not in source_slice.preserved_file_ids:
            raise RetailPdpSilverError(f"projection row {row.row_id!r} points at an unbound raw file")
        expected = (preserved.relative_packet_path, preserved.sha256, preserved.hash_basis)
        actual = (
            row.raw_anchor.relative_packet_path,
            row.raw_anchor.sha256,
            row.raw_anchor.hash_basis,
        )
        if actual != expected:
            raise RetailPdpSilverError(
                f"projection row {row.row_id!r} raw ref does not match the committed packet"
            )


def _one_row_per_key(
    rows: Iterable[RetailPdpProjectionRow], row_kind: str
) -> dict[tuple[str, str], RetailPdpProjectionRow]:
    result: dict[tuple[str, str], RetailPdpProjectionRow] = {}
    for row in rows:
        if row.row_kind != row_kind:
            continue
        key = (row.raw_ref.slice_id, row.retailer)
        if key in result:
            raise RetailPdpSilverError(
                f"multiple {row_kind} rows for {key[0]}:{key[1]}; identity binding is ambiguous"
            )
        result[key] = row
    return result


def _entity_key(row: RetailPdpProjectionRow) -> dict[str, str]:
    if row.retailer == "unknown":
        raise RetailPdpSilverError(f"variant row {row.row_id!r} has unknown retailer identity")
    native_id = _non_empty(row.source_visible_fields.get("product_id")) or _non_empty(
        row.source_visible_fields.get("sku")
    )
    if native_id is None:
        raise RetailPdpSilverError(
            f"variant row {row.row_id!r} has no retailer-local product_id or sku"
        )
    return {
        "namespace": f"retail_pdp:{row.retailer}",
        "kind": "retailer_product",
        "native_id": native_id,
    }


def _source_slice(packet: SourceCapturePacket, slice_id: str) -> SourceCaptureSlice:
    match = next((item for item in packet.source_slices if item.slice_id == slice_id), None)
    if match is None:
        raise RetailPdpSilverError(f"source slice not found: {slice_id!r}")
    return match


def _known_capture_time(source_slice: SourceCaptureSlice) -> str:
    value = _known_value(source_slice.timing.capture_time)
    if value is None:
        raise RetailPdpSilverError(
            f"source slice {source_slice.slice_id!r} has no known capture time"
        )
    return value


def _known_value(fact: Any) -> str | None:
    if fact is None or fact.status != VisibleFactStatus.KNOWN:
        return None
    return _non_empty(fact.value)


def _non_empty(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    return value.strip() or None


def _finish_record(record: dict[str, Any]) -> dict[str, Any]:
    canonical = dict(record)
    canonical.pop("content_hash", None)
    encoded = json.dumps(
        canonical,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    record["content_hash"] = f"sha256:{hashlib.sha256(encoded).hexdigest()}"
    return record


__all__ = [
    "RETAIL_PDP_SILVER_LANE",
    "RETAIL_PDP_SILVER_PRODUCER_SCHEMA_VERSION",
    "RetailPdpSilverError",
    "RetailPdpSilverResult",
    "build_retail_pdp_silver_records",
    "derive_retail_pdp_silver_from_projection",
]
