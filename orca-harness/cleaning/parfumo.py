"""Parfumo-specific adapter into the Cleaning Spine v0 core."""
from __future__ import annotations

import json
import re
from typing import Any

from cleaning.models import (
    CleaningEcrRef,
    CleaningInputGrain,
    CleaningPacket,
    CleaningPreservationCheck,
    CleaningRuleScope,
    CleaningTransform,
    CleaningTransformClass,
    CleaningTransformLedgerEntry,
)
from cleaning.projection import cleaning_input_handles_from_projection_rows
from ecr.models import ECR_SOURCE_SIDE_REF_KIND
from source_capture.parfumo_projection import (
    PARFUMO_DIRECT_HTTP_SOURCE_SURFACE,
    PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE,
    ParfumoProjectionPacket,
    ParfumoProjectionRow,
)

PARFUMO_CLEANING_HANDLE_PREFIX = "cleaning:parfumo"
PARFUMO_RATING_CARRY_RULE = "parfumo_source_visible_rating_field_carry"

_PARFUMO_SOURCE_FAMILY = "fragrance_native_database"
_PARFUMO_SOURCE_SURFACES = (
    PARFUMO_DIRECT_HTTP_SOURCE_SURFACE,
    PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE,
)
_ECR_REF_STATUS_BY_CONVENTION = "by_convention_not_existence_checked"

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


def build_parfumo_cleaning_packet(
    projection: ParfumoProjectionPacket,
    *,
    attach_ecr_ref: bool = True,
    source_surface: str = PARFUMO_DIRECT_HTTP_SOURCE_SURFACE,
) -> CleaningPacket:
    """Build a CleaningPacket from a Parfumo projection packet."""
    if source_surface not in _PARFUMO_SOURCE_SURFACES:
        raise ValueError(
            "Parfumo Cleaning requires "
            f"source_surface in {_PARFUMO_SOURCE_SURFACES!r}; got {source_surface!r}"
        )
    handles = cleaning_input_handles_from_projection_rows(
        source_family=_PARFUMO_SOURCE_FAMILY,
        source_surface=source_surface,
        projection_packet=projection,
        handle_id_prefix=PARFUMO_CLEANING_HANDLE_PREFIX,
    )
    row_by_id = {row.row_id: row for row in projection.rows}
    ecr_ref = _ecr_ref(projection.packet_id) if attach_ecr_ref else None
    packet_residuals = sorted(set(projection.residuals))
    packet_raw_pull_triggers = _raw_pull_triggers_for_packet_residuals(packet_residuals)

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
    row: ParfumoProjectionRow,
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


def _normalization_entry(
    *,
    input_handle_id: str,
    method_or_rule: str,
    input_grain: CleaningInputGrain,
    original_value: str,
    transformed_value: str,
) -> CleaningTransformLedgerEntry:
    return CleaningTransformLedgerEntry(
        input_handle_id=input_handle_id,
        transform=CleaningTransform(
            transform_class=CleaningTransformClass.NORMALIZATION,
            rule_scope=CleaningRuleScope.SOURCE_FAMILY_ADAPTATION,
            method_or_rule=method_or_rule,
            input_grain=input_grain,
            original_value=original_value,
            transformed_value=transformed_value,
        ),
        preservation=_preservation(),
    )


def _preservation() -> CleaningPreservationCheck:
    return CleaningPreservationCheck(
        originals_addressable=True,
        source_identity_preserved=True,
        timing_preserved=True,
        hierarchy_preserved=True,
        semantic_binding_preserved=True,
        counts_preserved=True,
    )


def _row_text(fields: dict[str, Any | None]) -> str | None:
    return _non_empty_string_or_none(fields.get("review_text")) or _non_empty_string_or_none(
        fields.get("statement_text")
    )


def _normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _non_empty_string_or_none(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    return value if _normalize_space(value) else None


def _length_bin(length: int) -> str:
    if length < 200:
        return "chars_0000_0199"
    if length < 500:
        return "chars_0200_0499"
    if length < 1000:
        return "chars_0500_0999"
    return "chars_1000_plus"


def _ecr_ref(packet_id: str) -> CleaningEcrRef:
    return CleaningEcrRef(
        packet_id=packet_id,
        ref_id=f"ecr:{packet_id}:{ECR_SOURCE_SIDE_REF_KIND}",
        posture_kind=ECR_SOURCE_SIDE_REF_KIND,
        status=_ECR_REF_STATUS_BY_CONVENTION,
    )


def _raw_pull_triggers_for_packet_residuals(residuals: list[str]) -> list[str]:
    return sorted(
        trigger
        for residual, trigger in _PACKET_RAW_PULL_TRIGGERS_BY_RESIDUAL.items()
        if residual in residuals
    )


__all__ = [
    "PARFUMO_CLEANING_HANDLE_PREFIX",
    "PARFUMO_RATING_CARRY_RULE",
    "build_parfumo_cleaning_packet",
]
