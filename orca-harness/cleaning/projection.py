"""Adapters from mechanical projection rows into Cleaning input handles."""
from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Literal

from cleaning.models import CleaningInputHandle, CleaningProjectionRef, CleaningRawAnchor

# Preserved-file anchor kinds ONLY. Deliberately excludes "derived_record": projection rows are
# views over preserved files, so a derived_record anchor must never originate from a projection
# (a derived record has no preserved-file substrate). Pinned by
# test_projection_never_emits_derived_record_anchor.
_CLEANING_ANCHOR_KINDS = frozenset(
    {"file", "json_pointer", "html_selector", "script_index", "text_pattern"}
)


def cleaning_input_handle_from_projection_row(
    *,
    handle_id: str,
    source_family: str,
    source_surface: str,
    projection_packet: Any,
    projection_row: Any,
) -> CleaningInputHandle:
    """Build a raw-keyed Cleaning handle from one projection row.

    Projection rows are working views. The returned handle is keyed to the
    row's raw packet/slice/file/hash anchor and carries the projection row only
    as secondary traceability.
    """
    raw_ref = _required_object(projection_row, "raw_ref", owner="projection row")
    projection_raw_anchor = _required_object(projection_row, "raw_anchor", owner="projection row")
    packet_id = _required_str(raw_ref, "packet_id", owner="projection row raw_ref")
    projection_packet_id = _required_str(projection_packet, "packet_id", owner="projection packet")
    if projection_packet_id != packet_id:
        raise ValueError("projection packet id must match projection row raw_ref.packet_id")

    return CleaningInputHandle(
        handle_id=handle_id,
        source_family=source_family,
        source_surface=source_surface,
        raw_anchor=_cleaning_raw_anchor(
            packet_id=packet_id,
            slice_id=_required_str(raw_ref, "slice_id", owner="projection row raw_ref"),
            projection_raw_anchor=projection_raw_anchor,
        ),
        projection_ref=CleaningProjectionRef(
            projection_method=_required_str(
                projection_packet, "projection_method", owner="projection packet"
            ),
            projection_version=_required_str(
                projection_packet, "projection_version", owner="projection packet"
            ),
            certification=_required_str(projection_packet, "certification", owner="projection packet"),
            packet_id=projection_packet_id,
            row_id=getattr(projection_row, "row_id", None),
            row_kind=getattr(projection_row, "row_kind", None),
        ),
    )


def cleaning_input_handles_from_projection_rows(
    *,
    source_family: str,
    source_surface: str,
    projection_packet: Any,
    rows: Iterable[Any] | None = None,
    handle_id_prefix: str = "cleaning",
) -> list[CleaningInputHandle]:
    """Build Cleaning handles for projection rows without source-family coupling."""
    projection_rows = getattr(projection_packet, "rows", None) if rows is None else rows
    if projection_rows is None:
        raise ValueError("projection rows are required")

    return [
        cleaning_input_handle_from_projection_row(
            handle_id=f"{handle_id_prefix}:{_required_str(row, 'row_id', owner='projection row')}",
            source_family=source_family,
            source_surface=source_surface,
            projection_packet=projection_packet,
            projection_row=row,
        )
        for row in projection_rows
    ]


def _cleaning_raw_anchor(
    *,
    packet_id: str,
    slice_id: str,
    projection_raw_anchor: Any,
) -> CleaningRawAnchor:
    anchor_kind = _projection_anchor_kind(projection_raw_anchor)
    anchor_value = getattr(projection_raw_anchor, "anchor_value", None)
    json_pointer = getattr(projection_raw_anchor, "json_pointer", None)

    base = {
        "packet_id": packet_id,
        "slice_id": slice_id,
        "file_id": _required_str(projection_raw_anchor, "file_id", owner="projection row raw_anchor"),
        "relative_packet_path": _required_str(
            projection_raw_anchor, "relative_packet_path", owner="projection row raw_anchor"
        ),
        "sha256": _required_str(projection_raw_anchor, "sha256", owner="projection row raw_anchor"),
        "hash_basis": _required_str(
            projection_raw_anchor, "hash_basis", owner="projection row raw_anchor"
        ),
    }

    if anchor_kind == "json_pointer":
        return CleaningRawAnchor(
            **base,
            anchor_kind=anchor_kind,
            json_pointer=_non_empty_anchor_value(
                json_pointer or anchor_value,
                owner="projection row raw_anchor",
                field="json_pointer",
            ),
        )

    if anchor_kind == "file":
        return CleaningRawAnchor(**base, anchor_kind=anchor_kind)

    return CleaningRawAnchor(
        **base,
        anchor_kind=anchor_kind,
        anchor_value=_non_empty_anchor_value(
            anchor_value,
            owner="projection row raw_anchor",
            field="anchor_value",
        ),
    )


def _projection_anchor_kind(
    projection_raw_anchor: Any,
) -> Literal["file", "json_pointer", "html_selector", "script_index", "text_pattern"]:
    anchor_kind = getattr(projection_raw_anchor, "anchor_kind", None)
    if anchor_kind is None:
        return "json_pointer" if getattr(projection_raw_anchor, "json_pointer", None) else "file"

    if not isinstance(anchor_kind, str) or not anchor_kind.strip():
        raise ValueError("projection row raw_anchor.anchor_kind must be a non-empty string")
    normalized = anchor_kind.strip()
    if normalized not in _CLEANING_ANCHOR_KINDS:
        allowed = ", ".join(sorted(_CLEANING_ANCHOR_KINDS))
        raise ValueError(f"unsupported projection raw anchor kind {normalized!r}; expected one of {allowed}")
    return normalized  # type: ignore[return-value]


def _required_object(value: Any, field: str, *, owner: str) -> Any:
    item = getattr(value, field, None)
    if item is None:
        raise ValueError(f"{owner}.{field} is required")
    return item


def _required_str(value: Any, field: str, *, owner: str) -> str:
    item = getattr(value, field, None)
    return _non_empty_anchor_value(item, owner=owner, field=field)


def _non_empty_anchor_value(value: Any, *, owner: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{owner}.{field} must be a non-empty string")
    return value
