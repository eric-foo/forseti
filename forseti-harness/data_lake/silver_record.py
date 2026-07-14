"""Silver Vault record envelope validation + the validating write front-door.

The no-blur invariant the Silver layer depends on -- a closed ``record_kind``, the
evidence-vs-fact split (a Silver observation is a FACT, never the Cleaning transform
ledger), and the MetricObservation posture coupling -- is enforced here as CODE, not
convention. ``append_silver_record`` is the validating front-door: a producer that
routes a Silver record through it cannot persist a blurred one, because validation
raises before any bytes are written.

Scope (v0): the common record header, integrity hash, source/derived-reference
lineage, no-ledger boundary, and payload-specific observation invariants.  The
generic ``data_lake.root.append_record`` stays payload-blind; this is a
Silver-aware layer ABOVE it, so Cleaning audit packs and projection/ECR records
keep writing generically.

Companions that close the v0 residuals: the write-path guard
``.agents/hooks/check_silver_lane_registry.py`` (a producer writing a Silver lane
through the raw writer instead of this front-door fails CI, save the named
FRONT_DOOR_PENDING lanes), and the no-blur NEGATIVE mirror
``data_lake.non_silver_record`` (a projection / cleaning-audit / ECR / signal-content
/ transcript record must not carry ``record_kind`` or this ``schema_version``, and
must carry its own role posture). Remaining residual: that negative mirror is enforced
by a conformance test, not yet wired into every producer's write path.
"""
from __future__ import annotations

from collections.abc import Mapping
import hashlib
import json
import re
from typing import TYPE_CHECKING, Any

from data_lake.canonical_json import canonical_record_bytes

if TYPE_CHECKING:
    from pathlib import Path

    from data_lake.root import DataLakeRoot

SILVER_VAULT_RECORD_SCHEMA_VERSION = "silver_vault_record_v0"
CLOSED_RECORD_KINDS = ("entity", "relationship", "observation")
# The closed metric-posture vocabulary -- the source-capture posture kinds a Silver
# MetricObservation may carry. Kept local here, exactly like CLOSED_RECORD_KINDS, so this
# base data_lake layer enforces the contract's "posture values must map to the live
# source-capture posture vocabulary" clause without importing the capture spine. Adding a
# kind is a deliberate edit here (mirroring a capture-spine vocabulary change).
METRIC_POSTURE_KINDS = ("observed", "unavailable_with_reason", "not_attempted")
METRIC_OBSERVATION_SET_PAYLOAD_KIND = "MetricObservationSet"
TEXT_OBSERVATION_SET_PAYLOAD_KIND = "TextObservationSet"
CONTENT_HASH_BASIS = "canonical_json_excluding_content_hash"
# Keys that mark Cleaning processing evidence (the transform ledger). A Silver fact
# must never carry them -- that is the evidence-vs-fact half of the no-blur invariant.
_LEDGER_KEYS = ("cleaning_packet", "transform_ledger")


class SilverRecordError(ValueError):
    """A record violates the Silver Vault envelope contract (the no-blur invariant)."""


def validate_silver_vault_record(record: Mapping[str, Any]) -> None:
    """Raise ``SilverRecordError`` if ``record`` is not a well-formed Silver Vault
    record.

    Enforces the common header, integrity, lineage, no-blur, and supported
    observation payload invariants.  Validation is deliberately fail-closed at
    the write boundary.
    """
    if not isinstance(record, Mapping):
        raise SilverRecordError("Silver record must be a mapping.")

    schema_version = record.get("schema_version")
    if schema_version != SILVER_VAULT_RECORD_SCHEMA_VERSION:
        raise SilverRecordError(
            f"Silver record schema_version must be {SILVER_VAULT_RECORD_SCHEMA_VERSION!r}; "
            f"got {schema_version!r}."
        )

    for field in (
        "record_id",
        "raw_anchor",
        "lane_namespace",
        "producer_id",
        "producer_schema_version",
        "producer_row_kind",
        "source_surface",
    ):
        _require_non_empty_string(record.get(field), f"Silver {field}")
    for field in ("observed_at", "captured_at"):
        if field not in record:
            raise SilverRecordError(f"Silver common header requires {field} (nullable when unknown).")
        value = record.get(field)
        if value is not None:
            _require_non_empty_string(value, f"Silver {field}")

    if record.get("content_hash_basis") != CONTENT_HASH_BASIS:
        raise SilverRecordError(
            f"Silver content_hash_basis must be {CONTENT_HASH_BASIS!r}."
        )
    content_hash = record.get("content_hash")
    if not isinstance(content_hash, str) or re.fullmatch(r"sha256:[0-9a-f]{64}", content_hash) is None:
        raise SilverRecordError("Silver content_hash must be sha256: followed by 64 lowercase hex characters.")
    _validate_lineage_refs(record)

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
        elif payload_kind == METRIC_OBSERVATION_SET_PAYLOAD_KIND:
            _validate_metric_observation_set(observation)
        elif payload_kind == "TextObservation":
            _validate_text_observation(observation)
        elif payload_kind == TEXT_OBSERVATION_SET_PAYLOAD_KIND:
            _validate_text_observation_set(observation)

    expected_hash = silver_content_hash(record)
    if content_hash != f"sha256:{expected_hash}":
        raise SilverRecordError("Silver content hash mismatch: content_hash does not match canonical record content.")


def _require_non_empty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SilverRecordError(f"{field} must be a non-empty string.")
    return value


def _validate_lineage_refs(record: Mapping[str, Any]) -> None:
    raw_refs = record.get("raw_refs")
    derived_refs = record.get("derived_refs")
    if not isinstance(raw_refs, list) or not isinstance(derived_refs, list):
        raise SilverRecordError("Silver raw_refs and derived_refs must both be lists.")
    if not raw_refs and not derived_refs:
        raise SilverRecordError("A Silver record requires at least one resolvable raw_ref or derived_ref.")
    for index, ref in enumerate(raw_refs):
        if not isinstance(ref, Mapping):
            raise SilverRecordError(f"Silver raw_refs[{index}] must be a mapping.")
        _require_non_empty_string(ref.get("packet_id"), f"Silver raw_refs[{index}].packet_id")
        sha = ref.get("sha256")
        basis = ref.get("hash_basis")
        if bool(sha) != bool(basis):
            raise SilverRecordError(
                f"Silver raw_refs[{index}] sha256 and hash_basis must travel together."
            )
        if ref.get("file_id") is not None and not sha:
            raise SilverRecordError(
                f"Silver raw_refs[{index}] names a file_id but is not hash-checkable."
            )
        if sha is not None:
            _require_non_empty_string(sha, f"Silver raw_refs[{index}].sha256")
            _require_non_empty_string(basis, f"Silver raw_refs[{index}].hash_basis")
    for index, ref in enumerate(derived_refs):
        if not isinstance(ref, Mapping):
            raise SilverRecordError(f"Silver derived_refs[{index}] must be a mapping.")
        lane = ref.get("lane_namespace", ref.get("lane"))
        record_id = ref.get("record_id")
        _require_non_empty_string(lane, f"Silver derived_refs[{index}].lane")
        _require_non_empty_string(record_id, f"Silver derived_refs[{index}].record_id")
        digest = ref.get("content_hash", ref.get("sha256"))
        basis = ref.get("content_hash_basis", ref.get("hash_basis"))
        if bool(digest) != bool(basis):
            raise SilverRecordError(
                f"Silver derived_refs[{index}] content hash and hash basis must travel together."
            )
        if digest is not None:
            _require_non_empty_string(digest, f"Silver derived_refs[{index}].content_hash")
            _require_non_empty_string(basis, f"Silver derived_refs[{index}].content_hash_basis")


def _reject_ledger(container: Mapping[str, Any], *, where: str) -> None:
    for ledger_key in _LEDGER_KEYS:
        if ledger_key in container:
            raise SilverRecordError(
                f"A Silver fact must not carry a transform ledger (found {ledger_key!r} in "
                f"{where}); processing evidence belongs in the audit-pack sibling, not a fact."
            )


def _validate_metric_posture(observation: Mapping[str, Any]) -> None:
    """MetricObservation posture coupling, per the Silver Vault contract's metric
    posture table: observed => value present and BOTH reason fields null; non-observed
    => value absent and A REASON present. The contract says "a reason is present" (not
    "a reason_code"), and the controlled signal is the posture ``kind`` (which maps to
    the source-capture posture vocabulary), so the reason may be carried in
    ``reason_code`` or the free-text ``reason_detail``. The posture ``kind`` itself must be
    one of the closed ``METRIC_POSTURE_KINDS`` (the source-capture posture vocabulary, kept
    local), so a looser free-text posture value cannot enter through the front-door."""
    metric_name = observation.get("metric_name")
    if not isinstance(metric_name, str) or not metric_name.strip():
        raise SilverRecordError("MetricObservation requires a non-empty metric_name.")
    posture = observation.get("metric_posture")
    if not isinstance(posture, Mapping):
        raise SilverRecordError("MetricObservation requires a metric_posture object.")
    kind = posture.get("kind")
    if kind not in METRIC_POSTURE_KINDS:
        raise SilverRecordError(
            f"MetricObservation metric_posture.kind must be one of {METRIC_POSTURE_KINDS}; "
            f"got {kind!r}. Posture values must map to the source-capture posture vocabulary."
        )
    value = observation.get("metric_value")
    has_reason = _has_posture_reason(posture)
    if kind == "observed":
        if value is None:
            raise SilverRecordError("An observed metric requires a metric_value.")
        if has_reason:
            raise SilverRecordError(
                "An observed metric must not carry a posture reason "
                "(reason_code and reason_detail must be null)."
            )
    else:
        if value is not None:
            raise SilverRecordError(
                f"A non-observed metric (kind={kind!r}) must not carry a metric_value "
                "(absence must never be stored as an observed value)."
            )
        if not has_reason:
            raise SilverRecordError(
                f"A non-observed metric (kind={kind!r}) requires a posture reason "
                "(reason_code or reason_detail)."
            )


def _validate_metric_observation_set(observation: Mapping[str, Any]) -> None:
    """Validate the packet-grain social metric observation-set envelope.

    The set is a physicalization optimization only: every nested metric retains
    the exact MetricObservation posture/value discipline.  Keeping this check in
    the Silver front door prevents a producer from gaining fewer files by
    weakening missing-vs-zero semantics or row identity.
    """
    platform = observation.get("platform")
    if not isinstance(platform, str) or not platform.strip():
        raise SilverRecordError("MetricObservationSet requires a non-empty platform.")
    policy_version = observation.get("policy_version")
    if not isinstance(policy_version, str) or not policy_version.strip():
        raise SilverRecordError("MetricObservationSet requires a non-empty policy_version.")
    fingerprint = observation.get("policy_fingerprint_sha256")
    if not isinstance(fingerprint, str) or re.fullmatch(r"[0-9a-f]{64}", fingerprint) is None:
        raise SilverRecordError(
            "MetricObservationSet requires a lowercase 64-hex policy_fingerprint_sha256."
        )
    rows = observation.get("rows")
    if not isinstance(rows, list) or not rows:
        raise SilverRecordError("MetricObservationSet requires a non-empty rows list.")
    row_count = observation.get("row_count")
    if isinstance(row_count, bool) or not isinstance(row_count, int) or row_count != len(rows):
        raise SilverRecordError(
            "MetricObservationSet row_count must exactly equal the rows-list length."
        )
    subject = observation.get("subject")
    subject_ref = subject.get("ref") if isinstance(subject, Mapping) else None
    if (
        not isinstance(subject, Mapping)
        or subject.get("ref_type") != "entity_key"
        or not isinstance(subject_ref, Mapping)
        or not all(
            isinstance(subject_ref.get(key), str) and str(subject_ref.get(key)).strip()
            for key in ("namespace", "kind", "native_id")
        )
    ):
        raise SilverRecordError(
            "MetricObservationSet requires an account-level entity_key subject."
        )
    if subject_ref.get("namespace") != platform:
        raise SilverRecordError(
            "MetricObservationSet subject namespace must equal platform."
        )
    if not isinstance(observation.get("observation_set_kind"), str) or not str(
        observation.get("observation_set_kind")
    ).strip():
        raise SilverRecordError(
            "MetricObservationSet requires a non-empty observation_set_kind."
        )
    seen_subjects: set[tuple[str, str, str]] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping):
            raise SilverRecordError(f"MetricObservationSet row {index} must be a mapping.")
        subject = row.get("subject")
        if not isinstance(subject, Mapping) or subject.get("ref_type") != "entity_key":
            raise SilverRecordError(
                f"MetricObservationSet row {index} requires an entity_key subject."
            )
        ref = subject.get("ref")
        if not isinstance(ref, Mapping):
            raise SilverRecordError(
                f"MetricObservationSet row {index} requires a subject.ref mapping."
            )
        identity = tuple(str(ref.get(key) or "").strip() for key in ("namespace", "kind", "native_id"))
        if any(not value for value in identity):
            raise SilverRecordError(
                f"MetricObservationSet row {index} requires namespace/kind/native_id identity."
            )
        if identity[0] != platform:
            raise SilverRecordError(
                f"MetricObservationSet row {index} subject namespace must equal platform."
            )
        if identity in seen_subjects:
            raise SilverRecordError(
                f"MetricObservationSet contains duplicate row subject {identity!r}."
            )
        seen_subjects.add(identity)
        metrics = row.get("metrics")
        if not isinstance(metrics, Mapping) or not metrics:
            raise SilverRecordError(
                f"MetricObservationSet row {index} requires a non-empty metrics mapping."
            )
        for metric_name, metric in metrics.items():
            if not isinstance(metric_name, str) or not metric_name.strip():
                raise SilverRecordError(
                    f"MetricObservationSet row {index} has a blank metric name."
                )
            if not isinstance(metric, Mapping):
                raise SilverRecordError(
                    f"MetricObservationSet row {index} metric {metric_name!r} must be a mapping."
                )
            if not isinstance(metric.get("unit"), str) or not str(metric.get("unit")).strip():
                raise SilverRecordError(
                    f"MetricObservationSet row {index} metric {metric_name!r} requires a unit."
                )
            if not isinstance(metric.get("source_field"), str) or not str(
                metric.get("source_field")
            ).strip():
                raise SilverRecordError(
                    f"MetricObservationSet row {index} metric {metric_name!r} requires a source_field."
                )
            _validate_metric_posture({**dict(metric), "metric_name": metric_name})


def _has_posture_reason(posture: Mapping[str, Any]) -> bool:
    """True if the posture carries a non-empty reason in either field. The Silver Vault
    contract requires 'a reason is present' for a non-observed metric without mandating
    which field carries it (the controlled signal is the posture ``kind``)."""
    for field in ("reason_code", "reason_detail"):
        value = posture.get(field)
        if isinstance(value, str) and value.strip():
            return True
    return False


def _validate_text_observation(observation: Mapping[str, Any]) -> None:
    text_value = observation.get("text_value")
    text_ref = observation.get("text_ref")
    posture = observation.get("text_posture")
    if not isinstance(posture, Mapping) or posture.get("kind") != "observed":
        raise SilverRecordError("TextObservation currently requires text_posture.kind='observed'.")
    if not (isinstance(text_value, str) and text_value) and not (
        isinstance(text_ref, str) and text_ref.strip()
    ):
        raise SilverRecordError("Observed TextObservation requires text_value or text_ref.")
    if isinstance(text_value, str) and text_value:
        text_hash = observation.get("text_hash")
        expected = "sha256:" + hashlib.sha256(text_value.encode("utf-8")).hexdigest()
        if text_hash != expected:
            raise SilverRecordError("Inline TextObservation text_hash does not match text_value.")


def _validate_text_observation_set(observation: Mapping[str, Any]) -> None:
    _validate_entity_key_subject(observation.get("subject"), "TextObservationSet")
    _require_non_empty_string(
        observation.get("observation_set_kind"), "TextObservationSet observation_set_kind"
    )
    _require_non_empty_string(observation.get("policy_version"), "TextObservationSet policy_version")
    fingerprint = observation.get("policy_fingerprint_sha256")
    if not isinstance(fingerprint, str) or re.fullmatch(r"[0-9a-f]{64}", fingerprint) is None:
        raise SilverRecordError(
            "TextObservationSet requires a lowercase 64-hex policy_fingerprint_sha256."
        )
    rows = observation.get("rows")
    if not isinstance(rows, list):
        raise SilverRecordError("TextObservationSet rows must be a list.")
    if observation.get("row_count") != len(rows):
        raise SilverRecordError("TextObservationSet row_count must equal rows-list length.")
    seen: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping):
            raise SilverRecordError(f"TextObservationSet row {index} must be a mapping.")
        row_id = _require_non_empty_string(row.get("row_id"), f"TextObservationSet row {index} row_id")
        if row_id in seen:
            raise SilverRecordError(f"TextObservationSet contains duplicate row_id {row_id!r}.")
        seen.add(row_id)
        _validate_text_observation(row)


def _validate_entity_key_subject(value: Any, context: str) -> None:
    ref = value.get("ref") if isinstance(value, Mapping) else None
    if not isinstance(value, Mapping) or value.get("ref_type") != "entity_key" or not isinstance(ref, Mapping):
        raise SilverRecordError(f"{context} requires an entity_key subject.")
    for field in ("namespace", "kind", "native_id"):
        _require_non_empty_string(ref.get(field), f"{context} subject.ref.{field}")


def silver_content_hash(record: Mapping[str, Any]) -> str:
    canonical = dict(record)
    canonical.pop("content_hash", None)
    encoded = json.dumps(
        canonical,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


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
    _validate_write_binding(record, raw_anchor=raw_anchor, lane=lane, record_id=record_id)
    return data_root.append_record(
        subtree="derived",
        raw_anchor=raw_anchor,
        lane=lane,
        record_id=record_id,
        data=canonical_record_bytes(record),
    )


def append_silver_record_set(
    data_root: "DataLakeRoot",
    *,
    raw_anchor: str,
    record_id: str,
    records: Mapping[str, Mapping[str, Any]],
    completion_lane: str,
) -> dict[str, "Path"]:
    """Validate every Silver member before publishing a detectable record set."""
    if not records:
        raise SilverRecordError("A Silver record set requires at least one member.")
    members: dict[str, bytes] = {}
    for lane, record in records.items():
        validate_silver_vault_record(record)
        _validate_write_binding(record, raw_anchor=raw_anchor, lane=lane, record_id=record_id)
        members[lane] = canonical_record_bytes(record)
    return data_root.append_record_set(
        subtree="derived",
        raw_anchor=raw_anchor,
        record_id=record_id,
        members=members,
        completion_lane=completion_lane,
    )


def _validate_write_binding(
    record: Mapping[str, Any], *, raw_anchor: str, lane: str, record_id: str
) -> None:
    expected = {
        "raw_anchor": raw_anchor,
        "lane_namespace": lane,
        "record_id": record_id,
    }
    for field, value in expected.items():
        if record.get(field) != value:
            raise SilverRecordError(
                f"Silver write binding mismatch: record {field}={record.get(field)!r}, "
                f"write target={value!r}."
            )


__all__ = [
    "CLOSED_RECORD_KINDS",
    "CONTENT_HASH_BASIS",
    "METRIC_POSTURE_KINDS",
    "METRIC_OBSERVATION_SET_PAYLOAD_KIND",
    "TEXT_OBSERVATION_SET_PAYLOAD_KIND",
    "SILVER_VAULT_RECORD_SCHEMA_VERSION",
    "SilverRecordError",
    "append_silver_record",
    "append_silver_record_set",
    "silver_content_hash",
    "validate_silver_vault_record",
]
