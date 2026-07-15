"""Fail-closed validation for company-aggregate/org-motion observations."""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import fields
import re
from typing import Any

from capture_spine.company_aggregate_forward_signal.models import (
    COMPANY_AGGREGATE_OBSERVATION_SCHEMA_VERSION,
    CompanyAggregateObservation,
    CompanyAggregateObservationError,
    MeasurementPosture,
    TimePrecision,
)


_ALLOWED_KEYS = frozenset(field.name for field in fields(CompanyAggregateObservation))
_MEASUREMENT_FIELDS = ("headcount", "size_band", "follower_count", "open_role_count")
_MEASUREMENT_KEYS = frozenset(
    {"posture", "value", "unit", "source_field", "reason", "zero_basis"}
)
_TIME_KEYS = frozenset({"value", "precision", "unknown_reason"})
_PROVENANCE_KEYS = frozenset(
    {"packet_id", "source_locator", "sha256", "hash_basis", "source_span"}
)
_TOKEN = re.compile(r"^[a-z0-9][a-z0-9_.-]*$")
_SHA256 = re.compile(r"^(?:sha256:)?[0-9a-f]{64}$")


def validate_company_aggregate_observation(observation: Mapping[str, Any]) -> None:
    if not isinstance(observation, Mapping):
        _fail("invalid_observation", "company aggregate observation must be a mapping")
    _reject_unknown_keys(observation, _ALLOWED_KEYS, "observation")
    if observation.get("schema_version") != COMPANY_AGGREGATE_OBSERVATION_SCHEMA_VERSION:
        _fail("invalid_schema_version", "unexpected company aggregate schema_version")
    for field_name in (
        "observation_id",
        "entity_key",
        "raw_entity_name",
        "source_tag",
        "capture_posture",
        "signal_kind",
        "captured_at",
    ):
        _require_string(observation.get(field_name), field_name)
    for token_name in ("source_tag", "capture_posture", "signal_kind"):
        if _TOKEN.fullmatch(str(observation[token_name])) is None:
            _fail("invalid_token", f"{token_name} must be a lowercase stable token")

    known_source_times = 0
    for field_name in ("source_effective_time", "filing_time", "as_of_time"):
        if field_name not in observation:
            _fail("missing_time", f"{field_name} is required; use unknown-with-reason")
        if _validate_source_time(observation[field_name], field_name):
            known_source_times += 1
    if known_source_times == 0:
        _fail(
            "missing_source_time",
            "at least one source-effective, filing, or as-of time must be known",
        )

    provenance = observation.get("provenance")
    if not _is_list(provenance) or not provenance:
        _fail("missing_provenance", "at least one provenance reference is required")
    for index, ref in enumerate(provenance):
        _validate_provenance_ref(ref, index)

    limitations = observation.get("limitations")
    if not _is_list(limitations):
        _fail("missing_limitations", "limitations must be an explicit list")
    for limitation in limitations:
        _require_string(limitation, "limitation")

    supplied_measurements = 0
    for field_name in _MEASUREMENT_FIELDS:
        measurement = observation.get(field_name)
        if measurement is not None:
            supplied_measurements += 1
            _validate_measurement(measurement, field_name)
    if supplied_measurements == 0:
        _fail("missing_measurement", "at least one aggregate/org-motion measurement is required")

    details = observation.get("signal_details", [])
    if not _is_list(details):
        _fail("invalid_signal_details", "signal_details must be a list")
    for detail in details:
        _require_string(detail, "signal_detail")

    prior = observation.get("reobserves_observation_id")
    if prior is not None:
        _require_string(prior, "reobserves_observation_id")
        if prior == observation.get("observation_id"):
            _fail("self_reobservation", "a re-observation must append a new observation_id")


def _validate_source_time(value: Any, label: str) -> bool:
    if not isinstance(value, Mapping):
        _fail("invalid_time", f"{label} must be a mapping")
    _reject_unknown_keys(value, _TIME_KEYS, label)
    precision = value.get("precision")
    allowed = {item.value for item in TimePrecision}
    if precision not in allowed:
        _fail("invalid_time_precision", f"{label}.precision must be one of {sorted(allowed)}")
    timestamp = value.get("value")
    reason = value.get("unknown_reason")
    if precision == TimePrecision.UNKNOWN.value:
        if timestamp is not None:
            _fail("unknown_time_has_value", f"{label} unknown time must not carry a value")
        _require_string(reason, f"{label}.unknown_reason")
        return False
    _require_string(timestamp, f"{label}.value")
    if reason not in (None, ""):
        _fail("known_time_has_unknown_reason", f"{label} known time must not carry unknown_reason")
    return True


def _validate_measurement(value: Any, label: str) -> None:
    if not isinstance(value, Mapping):
        _fail("invalid_measurement", f"{label} must be a mapping")
    _reject_unknown_keys(value, _MEASUREMENT_KEYS, label)
    posture = value.get("posture")
    allowed = {item.value for item in MeasurementPosture}
    if posture not in allowed:
        _fail("invalid_measurement_posture", f"{label}.posture must be one of {sorted(allowed)}")
    _require_string(value.get("unit"), f"{label}.unit")
    _require_string(value.get("source_field"), f"{label}.source_field")
    measurement_value = value.get("value")
    reason = value.get("reason")
    if posture == MeasurementPosture.OBSERVED.value:
        if measurement_value is None:
            _fail("observed_without_value", f"observed {label} requires a value")
        if reason not in (None, ""):
            _fail("observed_with_absence_reason", f"observed {label} must not carry an absence reason")
        if type(measurement_value) not in (int, str):
            _fail(
                "invalid_measurement_value",
                f"{label} value must be exactly an integer or string",
            )
        if measurement_value == 0:
            _require_string(
                value.get("zero_basis"),
                f"{label}.zero_basis (required to prove an observed zero is not absence)",
            )
    else:
        if measurement_value is not None:
            _fail(
                "absence_as_value",
                f"non-observed {label} must not carry a value; absence must never be zero",
            )
        _require_string(reason, f"{label}.reason")
        if value.get("zero_basis") not in (None, ""):
            _fail("non_observed_zero_basis", f"non-observed {label} must not carry zero_basis")


def _validate_provenance_ref(value: Any, index: int) -> None:
    label = f"provenance[{index}]"
    if not isinstance(value, Mapping):
        _fail("invalid_provenance", f"{label} must be a mapping")
    _reject_unknown_keys(value, _PROVENANCE_KEYS, label)
    for field_name in ("packet_id", "source_locator", "sha256", "hash_basis"):
        _require_string(value.get(field_name), f"{label}.{field_name}")
    if _SHA256.fullmatch(str(value["sha256"])) is None:
        _fail("invalid_provenance_hash", f"{label}.sha256 must be lowercase sha256")
    if value.get("source_span") is not None:
        _require_string(value["source_span"], f"{label}.source_span")


def _reject_unknown_keys(value: Mapping[str, Any], allowed: frozenset[str], label: str) -> None:
    unknown = sorted(str(key) for key in value if str(key) not in allowed)
    if unknown:
        _fail("unknown_field", f"{label} contains unknown field(s): {unknown}")


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail("missing_required_field", f"{label} must be a non-empty string")
    return value


def _is_list(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _fail(code: str, message: str) -> None:
    raise CompanyAggregateObservationError(code, message)


__all__ = ["validate_company_aggregate_observation"]
