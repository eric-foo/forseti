"""Basenotes-specific adapter into the Cleaning Spine v0 core."""
from __future__ import annotations

from typing import Any, Mapping

from cleaning._shared import (
    ecr_ref as _ecr_ref,
    length_bin as _length_bin,
    non_empty_string_or_none as _non_empty_string_or_none,
    normalization_entry as _normalization_entry,
    normalize_space as _normalize_space,
    raw_pull_triggers_for_packet_residuals as _raw_pull_triggers_for_packet_residuals,
)
from cleaning.models import (
    CleaningInputHandle,
    CleaningInputGrain,
    CleaningPacket,
    CleaningTransformLedgerEntry,
)
from cleaning.content import (
    cleaning_input_handles_from_content_rows,
    load_validated_content_record,
)
from cleaning.legacy import cleaning_handles_from_legacy_rows, decode_basenotes_raw
from source_capture.basenotes_projection import (
    BasenotesContentRecord,
)
from source_capture.models import SourceCapturePacket

BASENOTES_CLEANING_HANDLE_PREFIX = "cleaning:basenotes"

_BASENOTES_SOURCE_FAMILY = "fragrance_native_database"
_BASENOTES_SOURCE_SURFACE = (
    "basenotes_product_page_user_cleared_persistent_chrome_current_window"
)

_TEXT_ROW_KINDS = {
    "fragrance_review_card_current_window",
    "fragrance_statement_current_window",
}

_PACKET_RAW_PULL_TRIGGERS_BY_RESIDUAL = {
    "full_review_corpus_not_captured": (
        "inspect_raw_before_review_corpus_completeness_claim"
    ),
    "linked_media_assets_not_preserved_by_cloakbrowser_snapshot": (
        "inspect_raw_before_media_dependent_claim"
    ),
    "review_attached_photo_proof_not_present": (
        "inspect_raw_before_photo_dependent_claim"
    ),
}


def _build_basenotes_cleaning_packet_from_legacy(
    decoded: Any, *, attach_ecr_ref: bool
) -> CleaningPacket:
    handles = cleaning_handles_from_legacy_rows(
        source_family=_BASENOTES_SOURCE_FAMILY,
        source_surface=_BASENOTES_SOURCE_SURFACE,
        packet_id=decoded.packet_id,
        rows=decoded.rows,
        handle_id_prefix=BASENOTES_CLEANING_HANDLE_PREFIX,
    )
    return _build_basenotes_cleaning_packet(
        rows=decoded.rows,
        handles=handles,
        packet_id=decoded.packet_id,
        packet_residuals=decoded.residuals,
        attach_ecr_ref=attach_ecr_ref,
    )


def build_basenotes_cleaning_packet_from_source(
    *,
    packet: SourceCapturePacket,
    file_bytes_by_file_id: Mapping[str, bytes],
    attach_ecr_ref: bool = True,
) -> CleaningPacket:
    """Adapt canonical content directly; decode raw only for historical packets."""
    loaded = load_validated_content_record(
        packet=packet,
        file_bytes_by_file_id=file_bytes_by_file_id,
        record_model=BasenotesContentRecord,
        family_label="Basenotes",
    )
    if loaded is None:
        legacy = decode_basenotes_raw(
            packet=packet, file_bytes_by_file_id=file_bytes_by_file_id
        )
        return _build_basenotes_cleaning_packet_from_legacy(
            legacy, attach_ecr_ref=attach_ecr_ref
        )
    content_file, record = loaded
    handles = cleaning_input_handles_from_content_rows(
        packet=packet,
        content_file=content_file,
        source_family=_BASENOTES_SOURCE_FAMILY,
        source_surface=_BASENOTES_SOURCE_SURFACE,
        rows=record.rows,
        handle_id_prefix=BASENOTES_CLEANING_HANDLE_PREFIX,
    )
    return _build_basenotes_cleaning_packet(
        rows=record.rows,
        handles=handles,
        packet_id=packet.packet_id,
        packet_residuals=record.residuals,
        attach_ecr_ref=attach_ecr_ref,
    )


def _build_basenotes_cleaning_packet(
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
                method_or_rule="basenotes_text_whitespace_normalization",
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
                method_or_rule="basenotes_author_display_name_whitespace_normalization",
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
                method_or_rule="basenotes_text_length_bin",
                input_grain=CleaningInputGrain.ROW,
                original_value=str(text_length),
                transformed_value=_length_bin(text_length),
            )
        )

    return entries


def _row_text(fields: dict[str, Any | None]) -> str | None:
    return _non_empty_string_or_none(fields.get("review_text")) or _non_empty_string_or_none(
        fields.get("statement_text")
    )


__all__ = [
    "BASENOTES_CLEANING_HANDLE_PREFIX",
    "build_basenotes_cleaning_packet_from_source",
]
