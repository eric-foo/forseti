"""Canonical JSON byte encoder for Data Lake records.

One home for the byte format a lake JSON record is persisted in, so producers
cannot drift the serialization (``indent``/``sort_keys``/``ensure_ascii``/
``allow_nan``) by keeping private copies. Four byte-identical copies of this
function previously lived in ``data_lake.silver_record``,
``cleaning.fragrantica_lake``,
``capture_spine.creator_profile_current.silver_metric_producer`` and
``capture_spine.creator_profile_current.youtube_silver_metric_producer``; this is
their single source of truth.

It sits in the base ``data_lake`` layer and imports nothing from
``cleaning``/``capture_spine``/``source_capture``, so every adopter depends
downward only (no layer inversion).
"""
from __future__ import annotations

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


__all__ = ["canonical_record_bytes"]
