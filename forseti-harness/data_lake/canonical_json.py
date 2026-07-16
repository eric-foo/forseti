"""Canonical JSON byte encoders for Data Lake records.

One home for the byte formats a lake JSON record is serialized in, so producers
cannot drift the serialization (``indent``/``sort_keys``/``ensure_ascii``/
``allow_nan``) by keeping private copies. Four byte-identical copies of the
persisted-form function previously lived in ``data_lake.silver_record``,
``cleaning.fragrantica_lake``,
``capture_spine.creator_profile_current.silver_metric_producer`` and
``capture_spine.creator_profile_current.youtube_silver_metric_producer``; this is
their single source of truth. The compact content-hash form
(``canonical_compact_json_bytes`` / ``record_content_hash``) previously lived as
byte-identical private copies in ``cleaning.fragrantica_lake``,
``cleaning.parfumo_lake`` and ``cleaning.basenotes_lake``; it is consolidated
here for the same reason.

It sits in the base ``data_lake`` layer and imports nothing from
``cleaning``/``capture_spine``/``source_capture``, so every adopter depends
downward only (no layer inversion).
"""
from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_record_bytes(record: Any) -> bytes:
    """Canonical persisted bytes for a Data Lake JSON record: pretty-printed
    (``indent=2``), key-sorted, UTF-8, trailing newline, NaN/Infinity rejected.

    This is the exact format the validating Silver front-door re-encodes with, so
    a record routed through ``append_silver_record`` is byte-identical to one a
    conforming producer serialized directly."""
    return (
        json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")


def canonical_compact_json_bytes(value: Any) -> bytes:
    """Compact canonical JSON bytes: key-sorted, minimal separators, UTF-8,
    NaN/Infinity rejected. This is the hashing form (no indent, no trailing
    newline), not the persisted-record form above."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def record_content_hash(record: dict[str, Any]) -> str:
    """Hex sha256 of the record's compact canonical JSON with ``content_hash``
    excluded -- the ``canonical_json_excluding_content_hash`` hash basis."""
    canonical = dict(record)
    canonical.pop("content_hash", None)
    return hashlib.sha256(canonical_compact_json_bytes(canonical)).hexdigest()


__all__ = [
    "canonical_compact_json_bytes",
    "canonical_record_bytes",
    "record_content_hash",
]
