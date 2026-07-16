"""Shared cleaning-layer helpers (owning home per the Shared Helpers
convention in ``forseti-harness/README.md``).

Single source of truth for helpers that previously lived as byte-identical
private copies across the fragrantica/parfumo/basenotes cleaning adapters
(``cleaning.fragrantica`` / ``cleaning.parfumo`` / ``cleaning.basenotes``) and
their lake persistence modules (``cleaning.fragrantica_lake`` /
``cleaning.parfumo_lake`` / ``cleaning.basenotes_lake``). Per-source deltas --
silver subjects, coverage blocks, capture-time error messages, and the
residual->trigger tables -- stay in the source modules; only the shared
mechanism lives here.
"""
from __future__ import annotations

import json
import re
from typing import Any, Mapping

from cleaning.models import (
    CleaningEcrRef,
    CleaningInputGrain,
    CleaningInputHandle,
    CleaningPacket,
    CleaningPreservationCheck,
    CleaningRuleScope,
    CleaningTransform,
    CleaningTransformClass,
    CleaningTransformLedgerEntry,
)
from ecr.models import ECR_SOURCE_SIDE_REF_KIND

_ECR_REF_STATUS_BY_CONVENTION = "by_convention_not_existence_checked"


# --- adapter-side helpers (CleaningPacket construction) ---


def normalization_entry(
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
        preservation=preservation(),
    )


def preservation() -> CleaningPreservationCheck:
    return CleaningPreservationCheck(
        originals_addressable=True,
        source_identity_preserved=True,
        timing_preserved=True,
        hierarchy_preserved=True,
        semantic_binding_preserved=True,
        counts_preserved=True,
    )


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def non_empty_string_or_none(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    return value if normalize_space(value) else None


def length_bin(length: int) -> str:
    if length < 200:
        return "chars_0000_0199"
    if length < 500:
        return "chars_0200_0499"
    if length < 1000:
        return "chars_0500_0999"
    return "chars_1000_plus"


def ecr_ref(packet_id: str) -> CleaningEcrRef:
    return CleaningEcrRef(
        packet_id=packet_id,
        ref_id=f"ecr:{packet_id}:{ECR_SOURCE_SIDE_REF_KIND}",
        posture_kind=ECR_SOURCE_SIDE_REF_KIND,
        status=_ECR_REF_STATUS_BY_CONVENTION,
    )


def raw_pull_triggers_for_packet_residuals(
    residuals: list[str],
    triggers_by_residual: Mapping[str, str],
) -> list[str]:
    """Sorted triggers for the residuals present; the residual->trigger table is
    per-source and stays in the calling module."""
    return sorted(
        trigger
        for residual, trigger in triggers_by_residual.items()
        if residual in residuals
    )


# --- lake-side helpers (audit-pack / Silver record input refs) ---


def handle_raw_ref(handle: CleaningInputHandle) -> dict[str, str | None]:
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


def _none_first_ref_key(key: tuple[str | None, ...]) -> tuple[tuple[int, str], ...]:
    # None sorts before any string: a packet mixing a derived_record anchor
    # (None preserved-file fields) with a preserved-file anchor must order
    # deterministically instead of raising TypeError on None < str.
    return tuple((0, "") if part is None else (1, part) for part in key)


def raw_refs(cleaning_packet: CleaningPacket) -> list[dict[str, str | None]]:
    refs: dict[tuple[str | None, ...], dict[str, str | None]] = {}
    for handle in cleaning_packet.handles:
        ref = handle_raw_ref(handle)
        key = tuple(ref[field] for field in sorted(ref))
        refs[key] = ref
    return [refs[key] for key in sorted(refs, key=_none_first_ref_key)]


def projection_refs(cleaning_packet: CleaningPacket) -> list[dict[str, Any]]:
    return dedupe_refs(
        handle.projection_ref.model_dump(mode="json")
        for handle in cleaning_packet.handles
        if handle.projection_ref is not None
    )


def ecr_refs(cleaning_packet: CleaningPacket) -> list[dict[str, Any]]:
    return dedupe_refs(
        handle.ecr_ref.model_dump(mode="json")
        for handle in cleaning_packet.handles
        if handle.ecr_ref is not None
    )


def dedupe_refs(dumps: Any) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for ref in dumps:
        key = json.dumps(ref, sort_keys=True, separators=(",", ":"))
        if key not in seen:
            seen.add(key)
            out.append(ref)
    return out


__all__ = [
    "dedupe_refs",
    "ecr_ref",
    "ecr_refs",
    "handle_raw_ref",
    "length_bin",
    "non_empty_string_or_none",
    "normalization_entry",
    "normalize_space",
    "preservation",
    "projection_refs",
    "raw_pull_triggers_for_packet_residuals",
    "raw_refs",
]
