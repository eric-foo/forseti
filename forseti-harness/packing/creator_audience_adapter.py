"""Creator-audience adapter over the payload-agnostic columnar packing core.

Encoding-only: the `creator_audience_compact_judgment_view_v3` evidence list
becomes dense tables per evidence kind and multiplicity class under a
`packing_columnar_view_v0` envelope, and rehydrates deep-equal. Aliases and
field values pass through exactly; durable evidence IDs never enter this
surface because the input view never carries them.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from packing.columnar import (
    COLUMNAR_PACKING_VERSION,
    ColumnarPackingError,
    pack_table,
    unpack_table,
)

CREATOR_AUDIENCE_VIEW_VERSION = "creator_audience_compact_judgment_view_v3"

_SHARED_COLUMNS = ("alias", "source_item_id", "source_item_ids", "text")
EVIDENCE_TABLE_COLUMNS: dict[str, tuple[str, ...]] = {
    "creator_content": (*_SHARED_COLUMNS, "start_ms", "end_ms"),
    "creator_content_duplicates": (
        *_SHARED_COLUMNS,
        "start_ms",
        "end_ms",
        "duplicate_multiplicity",
        "member_locations",
    ),
    "observed_comment": (
        *_SHARED_COLUMNS,
        "engagement_salience_eligible",
        "comment_likes",
        "comment_like_rank_within_captured",
    ),
    "observed_comment_duplicates": (
        *_SHARED_COLUMNS,
        "engagement_salience_eligible",
        "duplicate_multiplicity",
        "comment_mechanics",
    ),
}
_VIEW_KEYS = (
    "view_version",
    "identity",
    "question",
    "evidence_cutoff",
    "capture_scope",
    "evidence",
    "engagement_salience_rule",
)
_PACKED_KEYS = (
    "packing_version",
    "view_version",
    "identity",
    "question",
    "evidence_cutoff",
    "capture_scope",
    "evidence_tables",
    "engagement_salience_rule",
)


def _require_exact_keys(
    mapping: Mapping[str, Any], expected: tuple[str, ...], label: str
) -> None:
    observed = set(mapping)
    if observed != set(expected):
        missing = sorted(set(expected) - observed)
        unexpected = sorted(observed - set(expected))
        raise ColumnarPackingError(
            f"{label} keys drifted (missing={missing!r}, unexpected={unexpected!r})"
        )


def _evidence_table_name(row: Mapping[str, Any]) -> str:
    kind = row.get("kind")
    if kind not in ("creator_content", "observed_comment"):
        raise ColumnarPackingError(f"unsupported evidence kind: {kind!r}")
    return f"{kind}_duplicates" if "duplicate_multiplicity" in row else str(kind)


def pack_creator_audience_view(view: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(view, Mapping):
        raise ColumnarPackingError("compact judgment view must be a mapping")
    if view.get("view_version") != CREATOR_AUDIENCE_VIEW_VERSION:
        raise ColumnarPackingError(
            f"unsupported view_version: {view.get('view_version')!r}"
        )
    _require_exact_keys(view, _VIEW_KEYS, "compact judgment view")
    rows_by_table: dict[str, list[dict[str, Any]]] = {
        name: [] for name in EVIDENCE_TABLE_COLUMNS
    }
    for row in view["evidence"]:
        if not isinstance(row, Mapping):
            raise ColumnarPackingError("evidence rows must be mappings")
        rows_by_table[_evidence_table_name(row)].append(
            {key: value for key, value in row.items() if key != "kind"}
        )
    return {
        "packing_version": COLUMNAR_PACKING_VERSION,
        "view_version": CREATOR_AUDIENCE_VIEW_VERSION,
        "identity": view["identity"],
        "question": view["question"],
        "evidence_cutoff": view["evidence_cutoff"],
        "capture_scope": view["capture_scope"],
        "evidence_tables": {
            name: pack_table(rows, EVIDENCE_TABLE_COLUMNS[name])
            for name, rows in rows_by_table.items()
            if rows
        },
        "engagement_salience_rule": view["engagement_salience_rule"],
    }


def _alias_order_key(row: Mapping[str, Any]) -> tuple[int, str]:
    # Aliases are zero-padded within a width (e0001...), so (length, text)
    # ordering equals assignment order without parsing the digits.
    alias = str(row["alias"])
    return (len(alias), alias)


def unpack_creator_audience_view(packed: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(packed, Mapping):
        raise ColumnarPackingError("packed view must be a mapping")
    if packed.get("packing_version") != COLUMNAR_PACKING_VERSION:
        raise ColumnarPackingError(
            f"unsupported packing_version: {packed.get('packing_version')!r}"
        )
    if packed.get("view_version") != CREATOR_AUDIENCE_VIEW_VERSION:
        raise ColumnarPackingError(
            f"unsupported view_version: {packed.get('view_version')!r}"
        )
    _require_exact_keys(packed, _PACKED_KEYS, "packed view")
    tables = packed["evidence_tables"]
    if not isinstance(tables, Mapping):
        raise ColumnarPackingError("evidence_tables must be a mapping")
    unknown = sorted(set(tables) - set(EVIDENCE_TABLE_COLUMNS))
    if unknown:
        raise ColumnarPackingError(f"unknown evidence tables: {unknown!r}")
    evidence: list[dict[str, Any]] = []
    for name, columns in EVIDENCE_TABLE_COLUMNS.items():
        if name not in tables:
            continue
        kind = name.removesuffix("_duplicates")
        for stripped in unpack_table(tables[name], expected_columns=columns):
            row: dict[str, Any] = {"alias": stripped["alias"], "kind": kind}
            for column in columns:
                if column != "alias":
                    row[column] = stripped[column]
            evidence.append(row)
    evidence.sort(key=_alias_order_key)
    return {
        "view_version": CREATOR_AUDIENCE_VIEW_VERSION,
        "identity": packed["identity"],
        "question": packed["question"],
        "evidence_cutoff": packed["evidence_cutoff"],
        "capture_scope": packed["capture_scope"],
        "evidence": evidence,
        "engagement_salience_rule": packed["engagement_salience_rule"],
    }
