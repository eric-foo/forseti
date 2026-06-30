"""Non-silver derived record role invariants -- the no-blur NEGATIVE mirror.

``silver_record.py`` says a Silver record MUST be a well-formed
``silver_vault_record_v0`` envelope. This module says the converse for the other
derived roles: a non-silver derived record (projection / cleaning audit / ECR /
signal-content / transcript) must NOT masquerade as a Silver fact, and must carry
its own honest role posture. Like ``silver_record.py`` this is a role-aware layer
ABOVE the payload-blind ``data_lake.root.append_record``; the generic writer stays
unchanged. Batch 2 enforces it through a conformance test rather than wiring it
into the (partly do-not-touch) producers -- the named residual below.

Scope: the record-CONTENT negatives the silver front-door listed as v0 residuals.

- #3 (every non-silver role): the record is not a Silver envelope -- no
  ``silver_vault_record_v0`` schema_version and no closed ``record_kind``. Checked
  on a Mapping record, or per member of a list record (ECR / signal-content write
  a JSON list of posture / SCR dicts).
- #4 (PROJECTION): carries a certification asserting ``not_cleaned`` and
  ``not_judgment_ready`` (a projection is a mechanical view, never a clean fact).
- #4 (CLEANING_AUDIT): carries ``record_family == "processing_audit"`` and its
  transform ledger (the processing evidence).
- #10 (CLEANING_AUDIT): asserts the ``not_judgment`` boundary and embeds no
  resolved Judgment record -- Cleaning references downstream layers, it never
  resolves them.

Not in scope (named residuals): wiring this validator into producer write paths;
a full reference-vs-resolved-ECR-posture check (the Judgment boundary is enforced;
the ECR link is checked at shape level only); and the ``silver_lineage`` grammar,
which is a Silver role validated by its own kit, not here.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from data_lake.lane_registry import LaneRole
from data_lake.silver_record import (
    CLOSED_RECORD_KINDS,
    SILVER_VAULT_RECORD_SCHEMA_VERSION,
)

# The non-silver derived roles this validator governs. The two Silver roles
# (SILVER_ENVELOPE, SILVER_LINEAGE) are legitimately Silver records and are out of
# scope here -- they have their own validators.
NON_SILVER_ROLES = frozenset(
    {
        LaneRole.CLEANING_AUDIT,
        LaneRole.PROJECTION,
        LaneRole.ECR,
        LaneRole.SIGNAL_CONTENT,
        LaneRole.TRANSCRIPT_CAPTURE,
    }
)

# Top-level keys whose presence means a Cleaning record is smuggling a resolved
# Judgment record (the out-of-scope boundary). Cleaning may reference downstream
# layers; it must not embed a resolved one.
_JUDGMENT_FIELD_NAMES = ("judgment", "judgement", "evidence_unit", "evidence_units")
_NOT_JUDGMENT_NON_CLAIM = "not_judgment"


class NonSilverRecordError(ValueError):
    """A non-silver derived record violates a no-blur role invariant."""


def validate_non_silver_record(role: LaneRole, record: Any) -> None:
    """Raise ``NonSilverRecordError`` if ``record`` blurs its non-silver role.

    ``role`` is the lane's declared role (from ``lane_registry.role_of``). ``record``
    is the derived record being (or just) persisted: a Mapping for the single-record
    lanes, or a Sequence of Mappings for the list lanes (ECR / signal-content).

    Passing a Silver role raises: a Silver record must use
    ``data_lake.silver_record.validate_silver_vault_record`` instead, and routing one
    here would silently skip its envelope contract.
    """
    if role not in NON_SILVER_ROLES:
        raise NonSilverRecordError(
            f"validate_non_silver_record governs non-silver roles only; got {role!r}. "
            "A Silver record must be validated by validate_silver_vault_record."
        )

    # #3 -- no member of this record may be (or pretend to be) a Silver envelope.
    for member in _record_members(record):
        _reject_silver_envelope(member, role=role)

    # #4 / #10 -- positive role posture, on the dict record only.
    if isinstance(record, Mapping):
        if role is LaneRole.PROJECTION:
            _require_projection_certification(record)
        elif role is LaneRole.CLEANING_AUDIT:
            _require_processing_audit_posture(record)
            _reject_smuggled_judgment(record)


def _record_members(record: Any):
    """Yield the dict members the #3 negative applies to: the record itself if it is
    a Mapping, else each Mapping in a Sequence record (ECR / signal-content persist a
    JSON list of posture / SCR dicts)."""
    if isinstance(record, Mapping):
        yield record
        return
    if isinstance(record, Sequence) and not isinstance(record, (str, bytes, bytearray)):
        for member in record:
            if isinstance(member, Mapping):
                yield member
        return
    raise NonSilverRecordError(
        "A non-silver derived record must be a mapping or a list of mappings; "
        f"got {type(record).__name__}."
    )


def _reject_silver_envelope(member: Mapping[str, Any], *, role: LaneRole) -> None:
    if member.get("schema_version") == SILVER_VAULT_RECORD_SCHEMA_VERSION:
        raise NonSilverRecordError(
            f"A {role.value} record must not carry schema_version="
            f"{SILVER_VAULT_RECORD_SCHEMA_VERSION!r} -- evidence / projection / posture "
            "cannot masquerade as a Silver fact."
        )
    record_kind = member.get("record_kind")
    if record_kind in CLOSED_RECORD_KINDS:
        raise NonSilverRecordError(
            f"A {role.value} record must not carry the closed Silver record_kind "
            f"{record_kind!r} -- record_kind is the Silver-fact discriminator."
        )


def _require_projection_certification(record: Mapping[str, Any]) -> None:
    cert = record.get("certification") or record.get("projection_certification")
    if (
        not isinstance(cert, str)
        or "not_cleaned" not in cert
        or "not_judgment_ready" not in cert
    ):
        raise NonSilverRecordError(
            "A projection record must declare its posture: a certification asserting "
            f"'not_cleaned' and 'not_judgment_ready' (got {cert!r})."
        )


def _require_processing_audit_posture(record: Mapping[str, Any]) -> None:
    record_family = record.get("record_family")
    if record_family != "processing_audit":
        raise NonSilverRecordError(
            "A cleaning-audit record must carry record_family='processing_audit' "
            f"(got {record_family!r})."
        )
    if not _has_transform_ledger(record):
        raise NonSilverRecordError(
            "A cleaning-audit record must carry its transform ledger (the processing "
            "evidence); none found in payload."
        )


def _has_transform_ledger(record: Mapping[str, Any]) -> bool:
    payload = record.get("payload")
    if not isinstance(payload, Mapping):
        return False
    cleaning_packet = payload.get("cleaning_packet")
    if isinstance(cleaning_packet, Mapping) and "transform_ledger" in cleaning_packet:
        return True
    # Tolerate a future audit shape that carries the ledger directly on payload.
    return "transform_ledger" in payload


def _reject_smuggled_judgment(record: Mapping[str, Any]) -> None:
    non_claims = record.get("non_claims")
    if not (isinstance(non_claims, (list, tuple)) and _NOT_JUDGMENT_NON_CLAIM in non_claims):
        raise NonSilverRecordError(
            "A cleaning record must assert the Judgment boundary (non_claims must "
            f"include {_NOT_JUDGMENT_NON_CLAIM!r}); Cleaning is not Judgment."
        )
    payload = record.get("payload")
    payload = payload if isinstance(payload, Mapping) else {}
    for field in _JUDGMENT_FIELD_NAMES:
        if field in record:
            raise NonSilverRecordError(
                "A cleaning record must not embed a resolved Judgment record (found "
                f"top-level {field!r}); reference Judgment, never resolve it."
            )
        if field in payload:
            raise NonSilverRecordError(
                "A cleaning record must not embed a resolved Judgment record (found "
                f"payload.{field!r}); reference Judgment, never resolve it."
            )


__all__ = [
    "NON_SILVER_ROLES",
    "NonSilverRecordError",
    "validate_non_silver_record",
]
