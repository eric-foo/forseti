"""Parfumo-specific adapter into the Cleaning Spine v0 core."""
from __future__ import annotations

import json
from typing import Any, Mapping

from cleaning._shared import (
    ecr_ref as _ecr_ref,
    length_bin as _length_bin,
    non_empty_string_or_none as _non_empty_string_or_none,
    normalization_entry as _normalization_entry,
    normalize_space as _normalize_space,
    preservation as _preservation,
    raw_pull_triggers_for_packet_residuals as _raw_pull_triggers_for_packet_residuals,
)
from cleaning.models import (
    CleaningInputHandle,
    CleaningInputGrain,
    CleaningPacket,
    CleaningRuleScope,
    CleaningTransform,
    CleaningTransformClass,
    CleaningTransformLedgerEntry,
)
from cleaning.content import (
    cleaning_input_handles_from_content_rows,
    load_validated_content_record,
)
from cleaning.legacy import cleaning_handles_from_legacy_rows, decode_parfumo_raw
from source_capture.parfumo_projection import (
    PARFUMO_DIRECT_HTTP_SOURCE_SURFACE,
    PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE,
    ParfumoTargetedContentRecord,
)
from source_capture.models import SourceCapturePacket

PARFUMO_CLEANING_HANDLE_PREFIX = "cleaning:parfumo"
PARFUMO_RATING_CARRY_RULE = "parfumo_source_visible_rating_field_carry"

_PARFUMO_SOURCE_FAMILY = "fragrance_native_database"
_PARFUMO_SOURCE_SURFACES = (
    PARFUMO_DIRECT_HTTP_SOURCE_SURFACE,
    PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE,
)

_TEXT_ROW_KINDS = {
    "fragrance_review_card_current_window",
    "fragrance_statement_current_window",
}

_PACKET_RAW_PULL_TRIGGERS_BY_RESIDUAL = {
    "full_review_corpus_not_captured_ajax_pagination_present": (
        "inspect_raw_before_review_corpus_completeness_claim"
    ),
    "full_statement_corpus_not_captured_ajax_pagination_present": (
        "inspect_raw_before_statement_corpus_completeness_claim"
    ),
    "linked_media_assets_not_preserved_by_direct_http_packet": (
        "inspect_raw_before_media_dependent_claim"
    ),
    "linked_media_assets_not_preserved_by_targeted_rendered_packet": (
        "inspect_raw_before_media_dependent_claim"
    ),
    "review_attached_photo_proof_not_present": (
        "inspect_raw_before_photo_dependent_claim"
    ),
}


def _build_parfumo_cleaning_packet_from_legacy(
    decoded: Any, *, attach_ecr_ref: bool, source_surface: str
) -> CleaningPacket:
    if source_surface not in _PARFUMO_SOURCE_SURFACES:
        raise ValueError(
            "Parfumo Cleaning requires "
            f"source_surface in {_PARFUMO_SOURCE_SURFACES!r}; got {source_surface!r}"
        )
    handles = cleaning_handles_from_legacy_rows(
        source_family=_PARFUMO_SOURCE_FAMILY,
        source_surface=source_surface,
        packet_id=decoded.packet_id,
        rows=decoded.rows,
        handle_id_prefix=PARFUMO_CLEANING_HANDLE_PREFIX,
    )
    return _build_parfumo_cleaning_packet(
        rows=decoded.rows,
        handles=handles,
        packet_id=decoded.packet_id,
        packet_residuals=decoded.residuals,
        attach_ecr_ref=attach_ecr_ref,
    )


def build_parfumo_cleaning_packet_from_source(
    *,
    packet: SourceCapturePacket,
    file_bytes_by_file_id: Mapping[str, bytes],
    attach_ecr_ref: bool = True,
) -> CleaningPacket:
    """Adapt canonical content directly; decode raw only for historical packets."""
    loaded = load_validated_content_record(
        packet=packet,
        file_bytes_by_file_id=file_bytes_by_file_id,
        record_model=ParfumoTargetedContentRecord,
        family_label="Parfumo",
    )
    if loaded is None:
        legacy = decode_parfumo_raw(
            packet=packet, file_bytes_by_file_id=file_bytes_by_file_id
        )
        return _build_parfumo_cleaning_packet_from_legacy(
            legacy,
            attach_ecr_ref=attach_ecr_ref,
            source_surface=packet.source_surface,
        )
    if packet.source_surface != PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE:
        raise ValueError("Parfumo content records require the targeted rendered surface")
    content_file, record = loaded
    handles = cleaning_input_handles_from_content_rows(
        packet=packet,
        content_file=content_file,
        source_family=_PARFUMO_SOURCE_FAMILY,
        source_surface=packet.source_surface,
        rows=record.rows,
        handle_id_prefix=PARFUMO_CLEANING_HANDLE_PREFIX,
    )
    return _build_parfumo_cleaning_packet(
        rows=record.rows,
        handles=handles,
        packet_id=packet.packet_id,
        packet_residuals=record.residuals,
        attach_ecr_ref=attach_ecr_ref,
    )


def _build_parfumo_cleaning_packet(
    *,
    rows: list[Any],
    handles: list[CleaningInputHandle],
    packet_id: str,
    packet_residuals: list[str],
    attach_ecr_ref: bool,
) -> CleaningPacket:
    row_by_id = {row.row_id: row for row in rows}
    ecr_ref = _ecr_ref(packet_id) if attach_ecr_ref else None
    packet_residuals = sorted(set(packet_residuals))
    packet_raw_pull_triggers = _raw_pull_triggers_for_packet_residuals(
        packet_residuals, _PACKET_RAW_PULL_TRIGGERS_BY_RESIDUAL
    )

    enriched_handles = []
    handle_id_by_row_id: dict[str, str] = {}
    for handle in handles:
        row_id = handle.source_row_id
        if row_id is None:
            enriched_handles.append(handle)
            continue
        row = row_by_id[row_id]
        residuals = sorted(set([*handle.residuals, *row.residuals, *packet_residuals]))
        enriched = handle.model_copy(
            update={
                "ecr_ref": ecr_ref,
                "residuals": residuals,
                "raw_pull_triggers": sorted(
                    set([*handle.raw_pull_triggers, *packet_raw_pull_triggers])
                ),
            }
        )
        enriched_handles.append(enriched)
        handle_id_by_row_id[row_id] = enriched.handle_id

    transform_ledger: list[CleaningTransformLedgerEntry] = []
    for row in rows:
        if row.row_kind not in _TEXT_ROW_KINDS:
            continue
        transform_ledger.extend(
            _text_row_transform_entries(
                row,
                input_handle_id=handle_id_by_row_id[row.row_id],
            )
        )

    return CleaningPacket(handles=enriched_handles, transform_ledger=transform_ledger)


def _text_row_transform_entries(
    row: Any,
    *,
    input_handle_id: str,
) -> list[CleaningTransformLedgerEntry]:
    fields = row.source_visible_fields
    entries: list[CleaningTransformLedgerEntry] = []

    text_value = _row_text(fields)
    if text_value is not None:
        entries.append(
            _normalization_entry(
                input_handle_id=input_handle_id,
                method_or_rule="parfumo_text_whitespace_normalization",
                input_grain=CleaningInputGrain.ROW,
                original_value=text_value,
                transformed_value=_normalize_space(text_value),
            )
        )

    author_display_name = _non_empty_string_or_none(fields.get("author_display_name"))
    if author_display_name is not None:
        entries.append(
            _normalization_entry(
                input_handle_id=input_handle_id,
                method_or_rule="parfumo_author_display_name_whitespace_normalization",
                input_grain=CleaningInputGrain.ROW,
                original_value=author_display_name,
                transformed_value=_normalize_space(author_display_name),
            )
        )

    text_length = fields.get("review_text_length_chars")
    if text_length is None:
        text_length = fields.get("statement_text_length_chars")
    if isinstance(text_length, int) and text_length >= 0:
        entries.append(
            _normalization_entry(
                input_handle_id=input_handle_id,
                method_or_rule="parfumo_text_length_bin",
                input_grain=CleaningInputGrain.ROW,
                original_value=str(text_length),
                transformed_value=_length_bin(text_length),
            )
        )

    rating = fields.get("rating")
    if (
        row.row_kind == "fragrance_review_card_current_window"
        and isinstance(rating, (int, float))
        and not isinstance(rating, bool)
    ):
        rating_json = json.dumps({"rating": float(rating)}, sort_keys=True, separators=(",", ":"))
        entries.append(
            CleaningTransformLedgerEntry(
                input_handle_id=input_handle_id,
                transform=CleaningTransform(
                    transform_class=CleaningTransformClass.PROPAGATION,
                    rule_scope=CleaningRuleScope.SOURCE_FAMILY_ADAPTATION,
                    method_or_rule=PARFUMO_RATING_CARRY_RULE,
                    input_grain=CleaningInputGrain.ROW,
                    original_value=rating_json,
                    transformed_value=rating_json,
                ),
                preservation=_preservation(),
            )
        )

    return entries


def _row_text(fields: dict[str, Any | None]) -> str | None:
    return _non_empty_string_or_none(fields.get("review_text")) or _non_empty_string_or_none(
        fields.get("statement_text")
    )


__all__ = [
    "PARFUMO_CLEANING_HANDLE_PREFIX",
    "PARFUMO_RATING_CARRY_RULE",
    "build_parfumo_cleaning_packet_from_source",
]
