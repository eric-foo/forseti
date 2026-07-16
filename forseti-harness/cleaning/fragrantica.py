"""Fragrantica-specific adapter into the Cleaning Spine v0 core.

This module consumes the mechanical Fragrantica projection packet and emits a
CleaningPacket with raw-keyed handles plus non-destructive review-card
normalization ledger entries. It does not write to the lake, decide sentiment,
dedupe near-matches, or make Judgment claims.
"""
from __future__ import annotations

import json

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
    CleaningInputGrain,
    CleaningPacket,
    CleaningRuleScope,
    CleaningTransform,
    CleaningTransformClass,
    CleaningTransformLedgerEntry,
)
from cleaning.projection import cleaning_input_handles_from_projection_rows
from source_capture.fragrantica_projection import FragranticaProjectionPacket, FragranticaProjectionRow

FRAGRANTICA_CLEANING_HANDLE_PREFIX = "cleaning:fragrantica"

_FRAGRANTICA_SOURCE_FAMILY = "fragrance_native_database"
_FRAGRANTICA_SOURCE_SURFACE = "fragrantica_product_page_direct_http"

_VOTE_FIELD_NAMES = (
    "rating",
    "longevity",
    "sillage",
    "gender",
    "relation",
    "season_winter",
    "season_spring",
    "season_summer",
    "season_autumn",
    "day",
    "night",
)

_PACKET_RAW_PULL_TRIGGERS_BY_RESIDUAL = {
    "full_review_archive_not_captured_login_prompt_present": (
        "inspect_raw_before_archive_completeness_claim"
    ),
    "search_review_rows_not_embedded_in_direct_http_body": (
        "inspect_raw_before_search_review_claim"
    ),
    "linked_media_assets_not_preserved_by_direct_http_packet": (
        "inspect_raw_before_media_dependent_claim"
    ),
    "review_attached_photo_proof_not_present": (
        "inspect_raw_before_review_photo_dependent_claim"
    ),
}


def build_fragrantica_cleaning_packet(
    projection: FragranticaProjectionPacket,
    *,
    attach_ecr_ref: bool = True,
) -> CleaningPacket:
    """Build a CleaningPacket from a Fragrantica projection packet.

    The packet contains one Cleaning input handle per projection row. Review-card
    rows receive source-family transform ledger entries for mechanical text,
    display-name, length-bin, and source-visible vote-field normalization/carry.
    Non-review rows remain addressable handles with no invented transforms.
    """
    handles = cleaning_input_handles_from_projection_rows(
        source_family=_FRAGRANTICA_SOURCE_FAMILY,
        source_surface=_FRAGRANTICA_SOURCE_SURFACE,
        projection_packet=projection,
        handle_id_prefix=FRAGRANTICA_CLEANING_HANDLE_PREFIX,
    )
    row_by_id = {row.row_id: row for row in projection.rows}
    ecr_ref = _ecr_ref(projection.packet_id) if attach_ecr_ref else None
    packet_residuals = sorted(set(projection.residuals))
    packet_raw_pull_triggers = _raw_pull_triggers_for_packet_residuals(
        packet_residuals, _PACKET_RAW_PULL_TRIGGERS_BY_RESIDUAL
    )

    enriched_handles = []
    handle_id_by_row_id: dict[str, str] = {}
    for handle in handles:
        row_id = handle.projection_ref.row_id if handle.projection_ref else None
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
    for row in projection.rows:
        if row.row_kind != "fragrance_review_card_current_window":
            continue
        transform_ledger.extend(
            _review_card_transform_entries(
                row,
                input_handle_id=handle_id_by_row_id[row.row_id],
            )
        )

    return CleaningPacket(handles=enriched_handles, transform_ledger=transform_ledger)


def _review_card_transform_entries(
    row: FragranticaProjectionRow,
    *,
    input_handle_id: str,
) -> list[CleaningTransformLedgerEntry]:
    fields = row.source_visible_fields
    entries: list[CleaningTransformLedgerEntry] = []

    review_text = _non_empty_string_or_none(fields.get("review_text"))
    if review_text is not None:
        entries.append(
            _normalization_entry(
                input_handle_id=input_handle_id,
                method_or_rule="fragrantica_review_text_whitespace_normalization",
                input_grain=CleaningInputGrain.ROW,
                original_value=review_text,
                transformed_value=_normalize_space(review_text),
            )
        )

    author_display_name = _non_empty_string_or_none(fields.get("author_display_name"))
    if author_display_name is not None:
        entries.append(
            _normalization_entry(
                input_handle_id=input_handle_id,
                method_or_rule="fragrantica_author_display_name_whitespace_normalization",
                input_grain=CleaningInputGrain.ROW,
                original_value=author_display_name,
                transformed_value=_normalize_space(author_display_name),
            )
        )

    review_length = fields.get("review_text_length_chars")
    if isinstance(review_length, int) and review_length >= 0:
        entries.append(
            _normalization_entry(
                input_handle_id=input_handle_id,
                method_or_rule="fragrantica_review_text_length_bin",
                input_grain=CleaningInputGrain.ROW,
                original_value=str(review_length),
                transformed_value=_length_bin(review_length),
            )
        )

    carried_votes = {
        key: fields.get(key)
        for key in _VOTE_FIELD_NAMES
        if fields.get(key) is not None
    }
    if carried_votes:
        vote_json = json.dumps(carried_votes, sort_keys=True, separators=(",", ":"))
        entries.append(
            CleaningTransformLedgerEntry(
                input_handle_id=input_handle_id,
                transform=CleaningTransform(
                    transform_class=CleaningTransformClass.PROPAGATION,
                    rule_scope=CleaningRuleScope.SOURCE_FAMILY_ADAPTATION,
                    method_or_rule="fragrantica_source_visible_vote_field_carry",
                    input_grain=CleaningInputGrain.ROW,
                    original_value=vote_json,
                    transformed_value=vote_json,
                ),
                preservation=_preservation(),
            )
        )

    return entries


__all__ = ["FRAGRANTICA_CLEANING_HANDLE_PREFIX", "build_fragrantica_cleaning_packet"]
