"""Cleaning Spine v0 source-invariant core.

The package is deliberately thin: it models Cleaning input handles,
non-destructive transform ledger entries, and exact-identity duplicate groups.
It does not acquire sources, project raw material, finalize ECR, bind Evidence
Units, or make Judgment claims.
"""

from cleaning.core import derive_exact_identity_duplicate_groups
from cleaning.models import (
    CLEANING_CORE_VERSION,
    REQUIRED_NON_CLAIMS,
    CleaningDedupeBasis,
    CleaningDedupeGroup,
    CleaningEcrRef,
    CleaningInputGrain,
    CleaningInputHandle,
    CleaningPacket,
    CleaningPreservationCheck,
    CleaningProjectionRef,
    CleaningRawAnchor,
    CleaningRelation,
    CleaningRuleScope,
    CleaningTransform,
    CleaningTransformClass,
    CleaningTransformLedgerEntry,
)
from cleaning.projection import (
    cleaning_input_handle_from_projection_row,
    cleaning_input_handles_from_projection_rows,
)

__all__ = [
    "CLEANING_CORE_VERSION",
    "REQUIRED_NON_CLAIMS",
    "CleaningDedupeBasis",
    "CleaningDedupeGroup",
    "CleaningEcrRef",
    "CleaningInputGrain",
    "CleaningInputHandle",
    "CleaningPacket",
    "CleaningPreservationCheck",
    "CleaningProjectionRef",
    "CleaningRawAnchor",
    "CleaningRelation",
    "CleaningRuleScope",
    "CleaningTransform",
    "CleaningTransformClass",
    "CleaningTransformLedgerEntry",
    "cleaning_input_handle_from_projection_row",
    "cleaning_input_handles_from_projection_rows",
    "derive_exact_identity_duplicate_groups",
]
