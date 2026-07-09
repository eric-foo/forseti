"""Orca Data Lake — physical foundation (filesystem-incumbent).

Foundation slice of the adopted Data Lake decision contracts: the external
data-root resolver, the per-root identity marker, the directory skeleton, and
the deterministic write-boundary guard. Selects no storage engine,
serialization, or queue.
"""
from __future__ import annotations

from data_lake.root import (
    DataLakeRoot,
    DataLakeRootError,
    LAKE_SUBDIRECTORIES,
    ROOT_MARKER_CONTRACT_VERSION,
    ROOT_MARKER_FILENAME,
)

__all__ = [
    "DataLakeRoot",
    "DataLakeRootError",
    "LAKE_SUBDIRECTORIES",
    "ROOT_MARKER_CONTRACT_VERSION",
    "ROOT_MARKER_FILENAME",
]
