"""Silver Vault record envelope validation + the validating write front-door.

The no-blur invariant the Silver layer depends on -- a closed ``record_kind``, the
evidence-vs-fact split (a Silver observation is a FACT, never the Cleaning transform
ledger), and the MetricObservation posture coupling -- is enforced here as CODE, not
convention. ``append_silver_record`` is the validating front-door: a producer that
routes a Silver record through it cannot persist a blurred one, because validation
raises before any bytes are written.

Scope (v0): the record ENVELOPE invariants only (``record_kind`` / ``payload_kind`` /
no-ledger-in-observation / MetricObservation posture). The lineage-block shape
(``raw_refs``/``derived_refs`` vs the ``silver_lineage`` kit) is a separate, deferred
reconciliation -- this validator does not re-shape a producer's lineage. The generic
``data_lake.root.append_record`` stays payload-blind; this is a Silver-aware layer
ABOVE it, so the Cleaning audit pack (no ``record_kind``) and projection/ECR records
keep writing generically.

Not enforced in v0 (named residuals): the audit/projection/ECR negative constraints
(a non-Silver derived record must not carry ``record_kind``) and the universal
write-path guard (a producer that bypasses this front-door and writes a Silver lane
through the raw writer is not yet structurally blocked).
"""
from __future__ import annotations

import json
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

    from data_lake.root import DataLakeRoot

SILVER_VAULT_RECORD_SCHEMA_VERSION = "silver_vault_record_v0"
CLOSED_RECORD_KINDS = ("entity", "relationship", "observation")
# Keys that mark Cleaning processing evidence (the transform ledger). A Silver fact
# must never carry them -- that is the evidence-vs-fact half of the no-blur invariant.
_LEDGER_KEYS = ("cleaning_packet", "transform_ledger")


class SilverRecordError(ValueError):
    """A record violates the Silver Vault envelope contract (the no-blur invariant)."""


def validate_silver_vault_record(record: Mapping[str, Any]) -> None:
    """Raise ``SilverRecordError`` if ``record`` is not a well-formed Silver Vault
    record.

    Enforces the envelope invariants only: ``schema_version``; closed ``record_kind``;
    non-empty ``payload_kind``; no transform ledger in a fact; and the
    MetricObservation posture coupling. Lineage-block shape is out of scope in v0.
    """
    if not isinstance(record, Mapping):
        raise SilverRecordError("Silver record must be a mapping.")

    schema_version = record.get("schema_version")
    if schema_version != SILVER_VAULT_RECORD_SCHEMA_VERSION:
        raise SilverRecordError(
            f"Silver record schema_version must be {SILVER_VAULT_RECORD_SCHEMA_VERSION!r}; "
            f"got {schema_version!r}."
        )

    record_kind = record.get("record_kind")
    if record_kind not in CLOSED_RECORD_KINDS:
        raise SilverRecordError(
            f"Silver record_kind must be one of {CLOSED_RECORD_KINDS}; got {record_kind!r}."
        )

    payload_kind = record.get("payload_kind")
    if not isinstance(payload_kind, str) or not payload_kind.strip():
        raise SilverRecordError("Silver payload_kind must be a non-empty string.")

    payload = record.get("payload")
    if not isinstance(payload, Mapping):
        raise SilverRecordError("Silver record payload must be a mapping.")

    # Evidence-vs-fact: a Silver record must not carry the Cleaning transform ledger --
    # that belongs in the processing-audit sibling, not in a fact.
    _reject_ledger(payload, where="payload")

    if record_kind == "observation":
        observation = payload.get("observation")
        if not isinstance(observation, Mapping):
            raise SilverRecordError(
                "An observation record must carry a payload.observation object."
            )
        _reject_ledger(observation, where="observation")
        if payload_kind == "MetricObservation":
            _validate_metric_posture(observation)
        elif payload_kind == "TextObservation":
            _validate_text_observation(observation)


def _reject_ledger(container: Mapping[str, Any], *, where: str) -> None:
    for ledger_key in _LEDGER_KEYS:
        if ledger_key in container:
            raise SilverRecordError(
                f"A Silver fact must not carry a transform ledger (found {ledger_key!r} in "
                f"{where}); processing evidence belongs in the audit-pack sibling, not a fact."
            )


def _validate_metric_posture(observation: Mapping[str, Any]) -> None:
    """MetricObservation posture coupling, on the Silver-persisted field names:
    observed => value present + no reason; non-observed => value absent + a reason.
    Mirrors the live MetricObservation discipline without importing the capture model."""
    metric_name = observation.get("metric_name")
    if not isinstance(metric_name, str) or not metric_name.strip():
        raise SilverRecordError("MetricObservation requires a non-empty metric_name.")
    posture = observation.get("metric_posture")
    if not isinstance(posture, Mapping):
        raise SilverRecordError("MetricObservation requires a metric_posture object.")
    kind = posture.get("kind")
    value = observation.get("metric_value")
    reason = posture.get("reason_code")
    if kind == "observed":
        if value is None:
            raise SilverRecordError("An observed metric requires a metric_value.")
        if reason is not None:
            raise SilverRecordError("An observed metric must not carry a posture reason_code.")
    else:
        if value is not None:
            raise SilverRecordError(
                f"A non-observed metric (kind={kind!r}) must not carry a metric_value "
                "(absence must never be stored as an observed value)."
            )
        if reason is None:
            raise SilverRecordError(
                f"A non-observed metric (kind={kind!r}) requires a posture reason_code."
            )


def _validate_text_observation(observation: Mapping[str, Any]) -> None:
    if not isinstance(observation.get("text_value"), str):
        raise SilverRecordError("TextObservation requires a string text_value.")


def append_silver_record(
    data_root: "DataLakeRoot",
    *,
    raw_anchor: str,
    lane: str,
    record_id: str,
    record: Mapping[str, Any],
) -> "Path":
    """Validate a Silver record against the envelope contract, then append it.

    The single sanctioned write path for Silver Vault records: a blurred record raises
    ``SilverRecordError`` BEFORE any bytes are written. The generic ``append_record``
    stays payload-blind; the Silver semantics live here, above it.
    """
    validate_silver_vault_record(record)
    return data_root.append_record(
        subtree="derived",
        raw_anchor=raw_anchor,
        lane=lane,
        record_id=record_id,
        data=_canonical_record_bytes(record),
    )


def _canonical_record_bytes(record: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"
    ).encode("utf-8")


__all__ = [
    "CLOSED_RECORD_KINDS",
    "SILVER_VAULT_RECORD_SCHEMA_VERSION",
    "SilverRecordError",
    "append_silver_record",
    "validate_silver_vault_record",
]
