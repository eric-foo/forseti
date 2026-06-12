"""Company-aggregate forward signal -- Layer 2 (derivation) for company headcount.

Slice 1: the Layer-2a immutable observation shape (``observation.py``). Layer-2b
(the derived, resolution-mapped entity projection) and the EDGAR adapter/runner/
extraction are later slices.
"""
from source_capture.company_aggregate.observation import (
    EDGAR_HEADCOUNT_OBSERVATION_SCHEMA_VERSION,
    EDGAR_SOURCE,
    MEASUREMENT_BASIS_VALUES,
    SPAN_LOCATOR_KIND_VALUES,
    VALUE_QUALITY_VALUES,
    EdgarHeadcountObservation,
    EdgarObservationKey,
    ExtractionProvenance,
    ExtractionSpan,
    HeadcountSupersession,
    ObservationRef,
)

__all__ = [
    "EDGAR_HEADCOUNT_OBSERVATION_SCHEMA_VERSION",
    "EDGAR_SOURCE",
    "MEASUREMENT_BASIS_VALUES",
    "SPAN_LOCATOR_KIND_VALUES",
    "VALUE_QUALITY_VALUES",
    "EdgarHeadcountObservation",
    "EdgarObservationKey",
    "ExtractionProvenance",
    "ExtractionSpan",
    "HeadcountSupersession",
    "ObservationRef",
]
