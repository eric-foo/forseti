"""Consumption seam v0: shared derived-lane pickup/acknowledgement helper.

Contract: ``orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md``.
Every derived lane discovers committed Bronze work and acknowledges completion
the same tested way:

- **Pickup is by-key** over committed availability (storage contract
  authority); no queue, event, or ``indexes/derived_retrieval`` view is ever
  consulted (view-independence — the conformance suite enforces it).
- **Obligation fingerprint**: the consumer computes a cheap canonical-JSON
  snapshot of the inputs its processing depends on; its sha256 is the
  fingerprint. An anchor is picked up unless an ack with the CURRENT
  fingerprint exists, so obligation growth (a late-arriving input record)
  re-surfaces the anchor automatically.
- **Acks are lane-owned completion facts**: append-only create-only records
  under ``acknowledgements/`` written through ``DataLakeRoot.append_record``
  (write-boundary enforcement). The ack namespace MUST be a lane name already
  declared in ``lane_registry.LANE_ROLES`` for ACTIVE writers/consumers — the
  CI-guarded lane map is the single name authority; no second registry.
  (Historical acks under later-retired namespaces remain valid history; an
  active consumer using an unregistered namespace fails loudly here.)
- **Corrections are representable without overwrite**: a same-obligation
  evidence correction is an append-only RETRACTION fact
  (``unack_<fp>_<k>``, mandatory reason); a fingerprint is acknowledged iff
  its ack facts outnumber its retraction facts, so retracted work re-surfaces
  and can be truthfully re-acknowledged (``ack_<fp>_<k>``).
- **An empty pickup is a no-work claim only over a reconciled availability
  surface**: ``pickup`` reconciles by default (``rebuild_availability``,
  fail-loud); opting out is an explicit, visible parameter.
- **Fail toward re-verification, never fake-done**: an unreadable ack is
  treated as absent (the anchor re-surfaces); an ack is only written by the
  consumer with completion evidence in hand, meeting the contract's minimum
  obligation envelope and evidence shape.

This module sits in the base ``data_lake`` layer beside ``lane_registry`` and
imports no producer code. It adds NO behavior to ``DataLakeRoot``, the
catalog, or availability — it is lane-side infrastructure consuming public
surfaces only.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator

from data_lake.canonical_json import canonical_record_bytes
from data_lake.lane_registry import LANE_ROLES

ACK_SCHEMA_VERSION = 1
_ACK_SUBTREE = "acknowledgements"
# record_id budget: "ack_" + 24 hex chars stays far inside the lake's safe-segment limit.
_ACK_ID_HEX_LEN = 24


class ConsumptionSeamError(ValueError):
    """A seam-contract violation (bad namespace, malformed obligation, missing evidence)."""


def validate_ack_namespace(ack_namespace: str) -> str:
    """An ack namespace must be a lane name declared in ``lane_registry.LANE_ROLES``."""
    if ack_namespace not in LANE_ROLES:
        raise ConsumptionSeamError(
            f"ack namespace {ack_namespace!r} is not a lane declared in lane_registry.LANE_ROLES; "
            "register the lane there first (the lane map is the single name authority)"
        )
    return ack_namespace


def _validate_obligation(obligation: Any) -> None:
    """Minimum obligation envelope (seam contract): a mapping carrying at least
    ``obligation_schema`` and a non-empty ``consumer``. Input enumeration beyond
    the envelope is lane-owned."""
    if not isinstance(obligation, dict):
        raise ConsumptionSeamError(
            f"obligation must be a mapping carrying the minimum envelope, got {type(obligation).__name__}"
        )
    if "obligation_schema" not in obligation:
        raise ConsumptionSeamError("obligation envelope is missing 'obligation_schema'")
    consumer = obligation.get("consumer")
    if not isinstance(consumer, str) or not consumer.strip():
        raise ConsumptionSeamError("obligation envelope requires a non-empty 'consumer'")


def _validate_evidence(evidence: list[dict], *, raw_anchor: str, ack_namespace: str) -> None:
    """Minimum evidence shape (seam contract): non-empty list of mappings, each
    with a non-empty ``kind``. Sufficiency beyond the shape is lane-owned; a
    syntactically-present-but-empty evidence list never satisfies the ack."""
    if not evidence:
        raise ConsumptionSeamError(
            f"refusing ack for {raw_anchor!r}/{ack_namespace!r} without completion evidence"
        )
    for entry in evidence:
        if not isinstance(entry, dict) or not str(entry.get("kind") or "").strip():
            raise ConsumptionSeamError(
                f"evidence entries for {raw_anchor!r}/{ack_namespace!r} must be mappings "
                f"with a non-empty 'kind'; got {entry!r}"
            )


def obligation_fingerprint(obligation: Any) -> str:
    """sha256 over the obligation's canonical persisted bytes (key-sorted, so
    dict ordering never changes the fingerprint)."""
    try:
        return hashlib.sha256(canonical_record_bytes(obligation)).hexdigest()
    except (TypeError, ValueError) as exc:
        raise ConsumptionSeamError(f"obligation is not canonical-JSON serializable: {exc}") from exc


def ack_record_id(fingerprint: str, *, retraction_count: int = 0) -> str:
    """Deterministic ack record id for one obligation fingerprint. The first
    completion is ``ack_<fp>``; the k-th re-completion after retractions is
    ``ack_<fp>_<k>``. A colliding write hard-fails instead of overwriting."""
    base = f"ack_{fingerprint[:_ACK_ID_HEX_LEN]}"
    return base if retraction_count == 0 else f"{base}_{retraction_count}"


def retraction_record_id(fingerprint: str, *, ordinal: int) -> str:
    """Deterministic retraction record id: ``unack_<fp>_<ordinal>`` (1-based)."""
    return f"unack_{fingerprint[:_ACK_ID_HEX_LEN]}_{ordinal}"


def _parse_fact(path: Path) -> dict | None:
    """A well-formed ack or retraction record, or ``None``. Corrupt/unreadable
    facts are treated as ABSENT for pickup decisions — the safe direction is
    re-verification, never fake-done; integrity diagnosis belongs to the lake
    doctor."""
    try:
        data = json.loads(path.read_bytes().decode("utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    kind = data.get("record_kind")
    if kind == "acknowledgement":
        if not isinstance(data.get("obligation_fingerprint"), str):
            return None
        return data
    if kind == "acknowledgement_retraction":
        if not isinstance(data.get("retracts_fingerprint"), str):
            return None
        return data
    return None


def _lane_facts(root, *, raw_anchor: str, ack_namespace: str) -> list[dict]:
    """All well-formed ack + retraction facts for one anchor + namespace. The
    single lane-directory read the other fact readers share."""
    lane_dir = root.lane_dir(subtree=_ACK_SUBTREE, raw_anchor=raw_anchor, lane=ack_namespace)
    if not lane_dir.is_dir():
        return []
    facts: list[dict] = []
    for record_file in sorted(lane_dir.iterdir()):
        if not record_file.is_file():
            continue
        fact = _parse_fact(record_file)
        if fact is not None:
            facts.append(fact)
    return facts


def _fact_counts(facts: list[dict], fingerprint: str) -> tuple[int, int]:
    acks = sum(
        1
        for fact in facts
        if fact.get("record_kind") == "acknowledgement"
        and fact.get("obligation_fingerprint") == fingerprint
    )
    retractions = sum(
        1
        for fact in facts
        if fact.get("record_kind") == "acknowledgement_retraction"
        and fact.get("retracts_fingerprint") == fingerprint
    )
    return acks, retractions


def _append_fact(root, *, raw_anchor: str, ack_namespace: str, record_id: str, body: dict) -> Path:
    return root.append_record(
        subtree=_ACK_SUBTREE,
        raw_anchor=raw_anchor,
        lane=ack_namespace,
        record_id=record_id,
        data=canonical_record_bytes(body),
    )


def append_ack(
    root,
    *,
    raw_anchor: str,
    ack_namespace: str,
    obligation: Any,
    evidence: list[dict],
    generated_at: str | None = None,
) -> Path:
    """Append the lane-owned completion fact for ``obligation`` at ``raw_anchor``.

    ``evidence`` must carry the refs proving completion (record ids /
    completion markers / hashes) meeting the contract's minimum shape — the ack
    asserts the lane met its obligation, so it must say how that is checkable.
    Create-only: acknowledging an already-acknowledged obligation raises from
    the lake write boundary rather than overwriting history. After a
    retraction, the re-completion lands at the next deterministic id.
    """
    validate_ack_namespace(ack_namespace)
    _validate_obligation(obligation)
    _validate_evidence(evidence, raw_anchor=raw_anchor, ack_namespace=ack_namespace)
    fingerprint = obligation_fingerprint(obligation)
    facts = _lane_facts(root, raw_anchor=raw_anchor, ack_namespace=ack_namespace)
    _acks, retractions = _fact_counts(facts, fingerprint)
    body = {
        "ack_schema_version": ACK_SCHEMA_VERSION,
        "record_kind": "acknowledgement",
        "ack_namespace": ack_namespace,
        "raw_anchor": raw_anchor,
        "obligation_fingerprint": fingerprint,
        "obligation": obligation,
        "evidence": evidence,
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
    }
    return _append_fact(
        root,
        raw_anchor=raw_anchor,
        ack_namespace=ack_namespace,
        record_id=ack_record_id(fingerprint, retraction_count=retractions),
        body=body,
    )


def retract_ack(
    root,
    *,
    raw_anchor: str,
    ack_namespace: str,
    obligation: Any,
    reason: str,
    generated_at: str | None = None,
) -> Path:
    """Append-only correction for a same-obligation ack whose recorded evidence
    was wrong or insufficient. Requires a non-empty reason; refuses to retract
    an obligation that is not currently acknowledged. The anchor re-surfaces in
    pickup and may be truthfully re-acknowledged after re-verification."""
    validate_ack_namespace(ack_namespace)
    _validate_obligation(obligation)
    if not reason.strip():
        raise ConsumptionSeamError("retraction requires a non-empty reason")
    fingerprint = obligation_fingerprint(obligation)
    facts = _lane_facts(root, raw_anchor=raw_anchor, ack_namespace=ack_namespace)
    acks, retractions = _fact_counts(facts, fingerprint)
    if acks <= retractions:
        raise ConsumptionSeamError(
            f"nothing to retract for {raw_anchor!r}/{ack_namespace!r}: "
            f"fingerprint {fingerprint[:16]}… is not currently acknowledged"
        )
    body = {
        "ack_schema_version": ACK_SCHEMA_VERSION,
        "record_kind": "acknowledgement_retraction",
        "ack_namespace": ack_namespace,
        "raw_anchor": raw_anchor,
        "retracts_fingerprint": fingerprint,
        "reason": reason,
        "generated_at": generated_at or datetime.now(timezone.utc).isoformat(),
    }
    return _append_fact(
        root,
        raw_anchor=raw_anchor,
        ack_namespace=ack_namespace,
        record_id=retraction_record_id(fingerprint, ordinal=retractions + 1),
        body=body,
    )


def find_acks(root, *, raw_anchor: str, ack_namespace: str) -> list[dict]:
    """All well-formed ack records for one anchor + namespace (append-only
    history; retraction facts are not included — use ``find_retractions``).

    HISTORY READER — deliberately not registry-gated: ack facts written under a
    later-renamed or retired namespace remain valid, readable history across
    registry evolution (seam contract, namespace rule). Only ACTIVE
    writer/consumer paths (``append_ack``/``retract_ack``/``pickup``/
    ``is_acknowledged``) require current ``LANE_ROLES`` membership."""
    return [
        fact
        for fact in _lane_facts(root, raw_anchor=raw_anchor, ack_namespace=ack_namespace)
        if fact.get("record_kind") == "acknowledgement"
    ]


def find_retractions(root, *, raw_anchor: str, ack_namespace: str) -> list[dict]:
    """All well-formed retraction facts for one anchor + namespace. History
    reader — not registry-gated, same rule as ``find_acks``."""
    return [
        fact
        for fact in _lane_facts(root, raw_anchor=raw_anchor, ack_namespace=ack_namespace)
        if fact.get("record_kind") == "acknowledgement_retraction"
    ]


def is_acknowledged(root, *, raw_anchor: str, ack_namespace: str, obligation: Any) -> bool:
    """True iff this obligation fingerprint's well-formed ack facts outnumber its
    retraction facts. Bodies are parsed and fingerprint fields verified, so a
    truncated or tampered file never counts as done."""
    validate_ack_namespace(ack_namespace)
    _validate_obligation(obligation)
    fingerprint = obligation_fingerprint(obligation)
    facts = _lane_facts(root, raw_anchor=raw_anchor, ack_namespace=ack_namespace)
    acks, retractions = _fact_counts(facts, fingerprint)
    return acks > retractions


@dataclass(frozen=True)
class PickupItem:
    """One unit of undone work: the anchor, the obligation snapshot the consumer
    computed for it, and that snapshot's fingerprint (pass both to ``append_ack``
    after completing the work)."""

    raw_anchor: str
    obligation: Any
    fingerprint: str


def pickup(
    root,
    *,
    ack_namespace: str,
    obligation_fn: Callable[[str], Any],
    source_family: str | None = None,
    reconcile: bool = True,
) -> Iterator[PickupItem]:
    """Yield committed anchors whose current obligation is not yet acknowledged.

    ``obligation_fn(raw_anchor)`` must be CHEAP (no raw-body loading/re-hashing):
    it snapshots the inputs the consumer's processing depends on. Heavy packet
    loading belongs to the consumer's processing of the yielded items only.

    ``reconcile=True`` (default) rebuilds the availability index from committed
    raw before the scan, failing LOUD on error — an empty pickup is a "no
    committed work" claim, and the seam contract makes that claim valid only
    over a reconciled surface. Pass ``reconcile=False`` only when the caller
    reconciles itself first or visibly records its staleness tolerance.

    Always by-key: every committed anchor is enumerated and compared; there is
    no incremental shortcut that could silently miss late-arriving work, and no
    view is consulted.
    """
    validate_ack_namespace(ack_namespace)
    if reconcile:
        root.rebuild_availability()
    for raw_anchor in root.list_available(source_family=source_family):
        obligation = obligation_fn(raw_anchor)
        if is_acknowledged(
            root, raw_anchor=raw_anchor, ack_namespace=ack_namespace, obligation=obligation
        ):
            continue
        yield PickupItem(
            raw_anchor=raw_anchor,
            obligation=obligation,
            fingerprint=obligation_fingerprint(obligation),
        )


def iter_all_acks(root) -> Iterator[tuple[str, str, dict]]:
    """Walk the whole acknowledgements tree, yielding ``(raw_anchor, namespace,
    ack)`` for every well-formed ack record.

    Read-only walk of the contract-pinned grammar
    ``acknowledgements/<anchor_shard>/<raw-anchor>/<ack-namespace>/<ack-record-id>``
    (derived-layout contract); used by the rebuild runner to build the
    ``undone`` view. Corrupt records are skipped per the fail-toward-
    re-verification rule.
    """
    ack_root = root.path / _ACK_SUBTREE
    if not ack_root.is_dir():
        return
    for shard_dir in sorted(p for p in ack_root.iterdir() if p.is_dir()):
        for anchor_dir in sorted(p for p in shard_dir.iterdir() if p.is_dir()):
            for namespace_dir in sorted(p for p in anchor_dir.iterdir() if p.is_dir()):
                for record_file in sorted(p for p in namespace_dir.iterdir() if p.is_file()):
                    fact = _parse_fact(record_file)
                    if fact is not None and fact.get("record_kind") == "acknowledgement":
                        yield anchor_dir.name, namespace_dir.name, fact


__all__ = [
    "ACK_SCHEMA_VERSION",
    "ConsumptionSeamError",
    "PickupItem",
    "ack_record_id",
    "append_ack",
    "find_acks",
    "find_retractions",
    "is_acknowledged",
    "iter_all_acks",
    "obligation_fingerprint",
    "pickup",
    "retract_ack",
    "retraction_record_id",
    "validate_ack_namespace",
]
