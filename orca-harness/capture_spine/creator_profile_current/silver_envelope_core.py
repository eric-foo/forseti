"""Shared Silver-envelope core for the creator-metric Silver producers.

Extraction of the envelope helpers that were previously duplicated verbatim
between ``silver_metric_producer.py`` (Instagram) and
``youtube_silver_metric_producer.py`` (YouTube) -- the named upgrade trigger in
the YouTube producer's docstring ("a clean shared silver-envelope core is
extracted and both producers import it") has fired. This is an EXTRACTION, not
a redesign: every function and constant here is byte-for-byte the behavior the
producers carried locally, so the produced record bytes are unchanged (proven
by both producers' unmodified test suites, which re-implement the content hash
independently).

Scope: only the genuinely duplicated envelope pieces live here -- the canonical
JSON/content-hash discipline, the posture/value coupling assert, the shared
lane/payload constants, and the small fail-closed field helpers both producers
restated identically. Platform-specific pieces (subjects, raw_refs, rollup raw
anchors, Bronze Attachment Record joins, non-claim conditionality) stay in the
producers: they genuinely differ and folding them here would be a redesign.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

SILVER_VAULT_RECORD_SCHEMA_VERSION = "silver_vault_record_v0"

# Platform-agnostic creator-metric Silver lanes shared by every producer: the
# lane names carry no platform token (records are distinguished by
# source_family/source_surface/producer_id/subject namespace), keeping creator
# metrics in one unified Silver lane across platforms.
METRIC_OBSERVATION_LANE = "creator_metric_silver"
METRIC_ROLLUP_LANE = "creator_metric_rollup_silver"
METRIC_OBSERVATION_PAYLOAD_KIND = "MetricObservation"
METRIC_ROLLUP_PAYLOAD_KIND = "MetricRollupObservation"

CONTENT_HASH_BASIS = "canonical_json_excluding_content_hash"
SOURCE_FAMILY = "social_media"

# Non-claims attached to every emitted creator-metric record. The
# registry/profile boundaries already in the codebase are the source of truth
# for these tokens; the producers restate them so a record is never mistaken
# for representative or buyer truth.
BASE_NON_CLAIMS = (
    "not a representative creator average",
    "not channel-wide creator influence",
    "not cross-platform identity linkage",
    "not a follower graph or audience estimate",
    "not buyer proof",
)


def assert_posture_value_coupling(*, posture: str, value: Any, reason: Any, what: str) -> None:
    """Enforce the Silver posture/value coupling: observed <=> numeric value and
    no reason; non-observed <=> null value and a reason. Booleans are not numbers.
    Fails loud rather than emitting a fake-shaped record."""
    if posture == "observed":
        if value is None or isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{what}: observed posture requires a numeric metric value, got {value!r}")
        if reason:
            raise ValueError(f"{what}: observed posture must not carry a posture reason")
    else:
        if value is not None:
            raise ValueError(f"{what}: non-observed posture must carry a null value, got {value!r}")
        if not reason:
            raise ValueError(f"{what}: non-observed posture requires a posture reason")


def metric_posture(kind: str, reason: str | None) -> dict[str, Any]:
    return {"kind": kind, "reason_code": None, "reason_detail": reason}


def rollup_metric(metric: Mapping[str, Any], *, what: str) -> dict[str, Any]:
    posture = metric["posture"]
    value = metric.get("value_or_none")
    reason = metric.get("posture_reason_or_none")
    assert_posture_value_coupling(posture=posture, value=value, reason=reason, what=what)
    return {
        "metric_value": value,
        "metric_posture": metric_posture(posture, reason),
        "unit": metric["metric_unit"],
    }


def required_subject_native_id(value: Any, *, what: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{what} requires a non-empty entity_key native_id")
    return value


def require_source_packet_id(seed_observation: Mapping[str, Any]) -> str:
    packet_id = seed_observation.get("source_packet_id_or_none")
    if not packet_id:
        raise ValueError(
            f"metric observation {seed_observation.get('metric_observation_id')!r} lacks a "
            "source packet id; cannot anchor a source-backed Silver record."
        )
    return packet_id


def content_hash(record: dict[str, Any]) -> str:
    canonical = dict(record)
    canonical.pop("content_hash", None)
    return hashlib.sha256(canonical_json_bytes(canonical)).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


__all__ = [
    "BASE_NON_CLAIMS",
    "CONTENT_HASH_BASIS",
    "METRIC_OBSERVATION_LANE",
    "METRIC_OBSERVATION_PAYLOAD_KIND",
    "METRIC_ROLLUP_LANE",
    "METRIC_ROLLUP_PAYLOAD_KIND",
    "SILVER_VAULT_RECORD_SCHEMA_VERSION",
    "SOURCE_FAMILY",
    "assert_posture_value_coupling",
    "canonical_json_bytes",
    "content_hash",
    "metric_posture",
    "require_source_packet_id",
    "required_subject_native_id",
    "rollup_metric",
]
