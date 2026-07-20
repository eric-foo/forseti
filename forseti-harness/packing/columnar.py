"""Payload-agnostic columnar packing core for the Packing Spine.

A dense table declares its columns once and carries each row as a value list
in that column order. Packing requires every row to match the declared column
set exactly, and rehydration fails loud on any version, column, or shape
drift, so the deep-equal round-trip contract can never silently degrade.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

COLUMNAR_PACKING_VERSION = "packing_columnar_view_v0"


class ColumnarPackingError(ValueError):
    """Raised when a table cannot be packed or rehydrated losslessly."""


def _validated_columns(columns: Sequence[str]) -> list[str]:
    ordered = list(columns)
    if not ordered or not all(
        isinstance(column, str) and column for column in ordered
    ):
        raise ColumnarPackingError(
            "table columns must be a non-empty sequence of non-blank strings"
        )
    if len(set(ordered)) != len(ordered):
        raise ColumnarPackingError(f"table columns must be unique: {ordered!r}")
    return ordered


def pack_table(
    rows: Sequence[Mapping[str, Any]], columns: Sequence[str]
) -> dict[str, Any]:
    ordered = _validated_columns(columns)
    expected = set(ordered)
    packed_rows: list[list[Any]] = []
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping):
            raise ColumnarPackingError(f"table row {index} is not a mapping")
        observed = set(row)
        if observed != expected:
            missing = sorted(expected - observed)
            unexpected = sorted(observed - expected)
            raise ColumnarPackingError(
                f"table row {index} does not match the declared columns "
                f"(missing={missing!r}, unexpected={unexpected!r})"
            )
        packed_rows.append([row[column] for column in ordered])
    return {"columns": ordered, "rows": packed_rows}


def unpack_table(
    table: Any, *, expected_columns: Sequence[str] | None = None
) -> list[dict[str, Any]]:
    if not isinstance(table, Mapping) or set(table) != {"columns", "rows"}:
        raise ColumnarPackingError(
            "packed table must be a mapping with exactly 'columns' and 'rows'"
        )
    columns = table["columns"]
    if not isinstance(columns, Sequence) or isinstance(columns, str):
        raise ColumnarPackingError("packed table columns must be a sequence")
    ordered = _validated_columns(columns)
    if expected_columns is not None and ordered != list(expected_columns):
        raise ColumnarPackingError(
            f"packed table columns drifted: expected {list(expected_columns)!r}, "
            f"observed {ordered!r}"
        )
    rows = table["rows"]
    if not isinstance(rows, Sequence) or isinstance(rows, str):
        raise ColumnarPackingError("packed table rows must be a sequence")
    unpacked: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        if (
            not isinstance(row, Sequence)
            or isinstance(row, str)
            or len(row) != len(ordered)
        ):
            raise ColumnarPackingError(
                f"packed table row {index} does not match the declared "
                f"column count ({len(ordered)})"
            )
        unpacked.append(dict(zip(ordered, row, strict=True)))
    return unpacked
