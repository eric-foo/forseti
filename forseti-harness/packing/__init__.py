"""Packing Spine: model-facing serialization of already-selected evidence sets.

Packing changes encoding only. It never selects, labels, scores, or repairs
evidence, and citation capability (aliases and their manifest binding) must
survive every packing round-trip exactly.
"""
from packing.columnar import (
    COLUMNAR_PACKING_VERSION,
    ColumnarPackingError,
    pack_table,
    unpack_table,
)
from packing.creator_audience_adapter import (
    CREATOR_AUDIENCE_VIEW_VERSION,
    EVIDENCE_TABLE_COLUMNS,
    pack_creator_audience_view,
    unpack_creator_audience_view,
)

__all__ = [
    "COLUMNAR_PACKING_VERSION",
    "CREATOR_AUDIENCE_VIEW_VERSION",
    "ColumnarPackingError",
    "EVIDENCE_TABLE_COLUMNS",
    "pack_creator_audience_view",
    "pack_table",
    "unpack_creator_audience_view",
    "unpack_table",
]
