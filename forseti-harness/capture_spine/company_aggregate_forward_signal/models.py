"""Source-agnostic company-aggregate/org-motion observation schema.

The schema is deliberately capture-owned and append-only.  It carries an
already-supplied Company Surface ``entity_key`` without minting identity, keeps
source time separate from capture time, and makes missing measurements explicit
instead of encoding absence as numeric zero.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


COMPANY_AGGREGATE_OBSERVATION_SCHEMA_VERSION = "company_aggregate_observation_v0"


class CompanyAggregateObservationError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class MeasurementPosture(StrEnum):
    OBSERVED = "observed"
    UNAVAILABLE_WITH_REASON = "unavailable_with_reason"
    NOT_ATTEMPTED = "not_attempted"


class TimePrecision(StrEnum):
    EXACT = "exact"
    DAY = "day"
    MONTH = "month"
    YEAR = "year"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class SourceTime:
    value: str | None
    precision: TimePrecision
    unknown_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class Measurement:
    posture: MeasurementPosture
    value: int | str | None
    unit: str
    source_field: str
    reason: str | None = None
    zero_basis: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class ProvenanceRef:
    packet_id: str
    source_locator: str
    sha256: str
    hash_basis: str
    source_span: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


@dataclass(frozen=True)
class CompanyAggregateObservation:
    observation_id: str
    entity_key: str
    raw_entity_name: str
    source_tag: str
    capture_posture: str
    signal_kind: str
    source_effective_time: SourceTime
    filing_time: SourceTime
    as_of_time: SourceTime
    captured_at: str
    provenance: tuple[ProvenanceRef, ...]
    limitations: tuple[str, ...]
    schema_version: str = COMPANY_AGGREGATE_OBSERVATION_SCHEMA_VERSION
    headcount: Measurement | None = None
    size_band: Measurement | None = None
    follower_count: Measurement | None = None
    open_role_count: Measurement | None = None
    signal_details: tuple[str, ...] = ()
    reobserves_observation_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return _enum_values(asdict(self))


def _enum_values(value: Any) -> Any:
    if isinstance(value, StrEnum):
        return value.value
    if isinstance(value, tuple):
        return [_enum_values(item) for item in value]
    if isinstance(value, list):
        return [_enum_values(item) for item in value]
    if isinstance(value, dict):
        return {key: _enum_values(item) for key, item in value.items()}
    return value


__all__ = [
    "COMPANY_AGGREGATE_OBSERVATION_SCHEMA_VERSION",
    "CompanyAggregateObservation",
    "CompanyAggregateObservationError",
    "Measurement",
    "MeasurementPosture",
    "ProvenanceRef",
    "SourceTime",
    "TimePrecision",
]
