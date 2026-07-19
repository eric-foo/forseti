"""Forseti Data Lake — physical foundation (filesystem-incumbent).

Foundation slice of the adopted Data Lake decision contracts: the external
data-root resolver, the per-root identity marker, the directory skeleton, and
the deterministic write-boundary guard. This package is the current
filesystem-incumbent foundation; engine/backend selection belongs to the Data
Lake Storage Contract physicalization boundary.
"""
from __future__ import annotations

from data_lake.root import (
    DataLakeRoot,
    DataLakeRootError,
    DataLakeRootUnavailableError,
    EPOCH_MARKER_FILENAME,
    FORSETI_DATA_ROOT_ENV,
    LAKE_EPOCH,
    LAKE_EPOCH_POLICY,
    LAKE_SUBDIRECTORIES,
    LEGACY_EPOCH_MARKER_FILENAME,
    LEGACY_ORCA_DATA_ROOT_ENV,
    LEGACY_ROOT_MARKER_FILENAME,
    ROOT_MARKER_CONTRACT_VERSION,
    ROOT_MARKER_DEFAULT_LABEL,
    ROOT_MARKER_FILENAME,
    anchor_shard,
    raw_shard,
)

__all__ = [
    "DataLakeRoot",
    "DataLakeRootError",
    "DataLakeRootUnavailableError",
    "EPOCH_MARKER_FILENAME",
    "FORSETI_DATA_ROOT_ENV",
    "LAKE_EPOCH",
    "LAKE_EPOCH_POLICY",
    "LAKE_SUBDIRECTORIES",
    "LEGACY_EPOCH_MARKER_FILENAME",
    "LEGACY_ORCA_DATA_ROOT_ENV",
    "LEGACY_ROOT_MARKER_FILENAME",
    "ROOT_MARKER_CONTRACT_VERSION",
    "ROOT_MARKER_DEFAULT_LABEL",
    "ROOT_MARKER_FILENAME",
    "anchor_shard",
    "raw_shard",
]
