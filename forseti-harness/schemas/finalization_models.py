"""SP-5 FinalizationReceipt model + validate-only consumer.

Implements the behavior spec at
docs/research/judgment-spine/sp5_finalization_receipt_spec_v0.md (reviewed).

This is the finalizer *half* of the bounded JSG-01 unfreeze. It does NOT unfreeze
JSG-01: the conductor also needs the EvidenceUnit binding and a real case packet
that carries a FinalizationReceipt. Product-learning grade; this module mints no
claim tier and authorizes no run.

Design (locked by the deep-think + spec/micro lock):
- binding_hash = canonical_yaml_hash over (evidence_id + finalized_over).
- current-designation = supersedes-via-ULID: every receipt carries a unique
  receipt_id; a correction is a NEW receipt that carries supersedes=<prior
  receipt_id>; the CURRENT receipt for an evidence_id is the single un-superseded
  one (zero or more-than-one => block). Receipts are immutable/append-only.
- The consumer is validate-only / block-don't-repair: it never authors, defaults,
  repairs, or infers a final value.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from pydantic import field_validator, model_validator

from harness_utils import canonical_yaml_hash, generate_ulid, utc_now_z
from schemas.case_models import PreDecisionStatus, StrictModel


class FinalizationProvenanceResult(StrEnum):
    CLEARED = "cleared"
    BLOCKED = "blocked"


class FinalizedOver(StrictModel):
    """The Packing-proposed inputs the finalization is recorded over."""

    proposed_pre_decision_status: PreDecisionStatus
    proposed_pre_decision_basis: str

    @field_validator("proposed_pre_decision_basis")
    @classmethod
    def reject_blank_basis(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("proposed_pre_decision_basis must be non-empty")
        return value


def compute_binding_hash(evidence_id: str, finalized_over: FinalizedOver) -> str:
    """Deterministic, reproducible hash over (evidence_id + the finalized-over proposed inputs).

    Uses the harness canonical YAML serialization (sorted keys, Enum -> value) so
    the same inputs always yield the same hash regardless of construction order.
    """
    return canonical_yaml_hash(
        {
            "evidence_id": evidence_id,
            "proposed_pre_decision_status": finalized_over.proposed_pre_decision_status,
            "proposed_pre_decision_basis": finalized_over.proposed_pre_decision_basis,
        }
    )


class FinalizationReceipt(StrictModel):
    """A separate, append-only record that finalizes one EvidenceUnit's pre_decision_status.

    evidence_id is the association/index, NOT a uniqueness key: several receipts may
    exist for one evidence_id over time (original + corrections), exactly one current.
    """

    receipt_id: str
    evidence_id: str
    finalized_over: FinalizedOver
    final_pre_decision_status: PreDecisionStatus
    finalizer_identity: str
    judge_model_family: str
    finalizer_model_family: str
    finalized_at: str
    binding_hash: str
    supersedes: str | None = None

    @field_validator(
        "receipt_id",
        "evidence_id",
        "finalizer_identity",
        "judge_model_family",
        "finalizer_model_family",
        "finalized_at",
        "binding_hash",
    )
    @classmethod
    def reject_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("required FinalizationReceipt string fields must be non-empty")
        return value

    @model_validator(mode="after")
    def validate_receipt(self) -> "FinalizationReceipt":
        if self.finalizer_model_family == self.judge_model_family:
            raise ValueError(
                "finalizer_model_family must differ from judge_model_family "
                "(distinct cross-family act; no same-family self-finalization)"
            )
        if self.supersedes is not None:
            if not self.supersedes.strip():
                raise ValueError("supersedes, when present, must be a non-empty prior receipt_id")
            if self.supersedes == self.receipt_id:
                raise ValueError("a receipt cannot supersede itself")
        expected = compute_binding_hash(self.evidence_id, self.finalized_over)
        if self.binding_hash != expected:
            raise ValueError(
                "binding_hash must be the deterministic hash over (evidence_id + finalized_over)"
            )
        return self


def build_finalization_receipt(
    *,
    evidence_id: str,
    proposed_pre_decision_status: PreDecisionStatus,
    proposed_pre_decision_basis: str,
    final_pre_decision_status: PreDecisionStatus,
    finalizer_identity: str,
    judge_model_family: str,
    finalizer_model_family: str,
    supersedes: str | None = None,
) -> FinalizationReceipt:
    """Assemble a receipt over operator-supplied values.

    This does NOT author/default the final value: the caller supplies
    final_pre_decision_status (the out-of-band finalization act). This helper only
    stamps the per-receipt identity, timestamp, and the deterministic binding hash.
    """
    finalized_over = FinalizedOver(
        proposed_pre_decision_status=proposed_pre_decision_status,
        proposed_pre_decision_basis=proposed_pre_decision_basis,
    )
    return FinalizationReceipt(
        receipt_id=generate_ulid(),
        evidence_id=evidence_id,
        finalized_over=finalized_over,
        final_pre_decision_status=final_pre_decision_status,
        finalizer_identity=finalizer_identity,
        judge_model_family=judge_model_family,
        finalizer_model_family=finalizer_model_family,
        finalized_at=utc_now_z(),
        binding_hash=compute_binding_hash(evidence_id, finalized_over),
        supersedes=supersedes,
    )


@dataclass(frozen=True)
class FinalizationVerdict:
    """Validate-only verdict for the JSG-01 finalization-provenance subpredicate.

    final_pre_decision_status is populated ONLY on CLEARED, and only ever copies the
    value present in a valid current receipt (block-don't-repair: never authored).
    """

    result: FinalizationProvenanceResult
    reason: str
    final_pre_decision_status: PreDecisionStatus | None = None
    current_receipt_id: str | None = None


def select_current_receipt(receipts: list[FinalizationReceipt]) -> FinalizationReceipt | None:
    """The single un-superseded current receipt, or None when the scoped set is malformed
    or ambiguous (the caller blocks on None).

    Callers should pass receipts already scoped to one evidence_id. Returns None when, for
    that set: it is empty; a receipt_id is duplicated (ambiguous identity); a non-null
    supersedes does not resolve to a present receipt_id (incomplete audit chain); the
    supersedes graph contains a cycle (contradictory history); or there is not exactly one
    un-superseded receipt (zero, or branching/multiple currents).
    """
    if not receipts:
        return None
    # Duplicate receipt_id => ambiguous identity; the scoped set is malformed.
    ids = [receipt.receipt_id for receipt in receipts]
    if len(set(ids)) != len(ids):
        return None
    by_id = {receipt.receipt_id: receipt for receipt in receipts}
    # Every non-null supersedes must reference a retained receipt in this scoped set,
    # otherwise the correction's audited prior is missing and the chain cannot be verified.
    for receipt in receipts:
        if receipt.supersedes is not None and receipt.supersedes not in by_id:
            return None
    # The supersedes graph must be acyclic; a cycle is contradictory append-only history.
    for receipt in receipts:
        seen: set[str] = set()
        node = receipt
        while node.supersedes is not None:
            if node.receipt_id in seen:
                return None
            seen.add(node.receipt_id)
            node = by_id[node.supersedes]
    # Exactly one un-superseded receipt is current.
    superseded = {receipt.supersedes for receipt in receipts if receipt.supersedes is not None}
    current = [receipt for receipt in receipts if receipt.receipt_id not in superseded]
    if len(current) != 1:
        return None
    return current[0]


def evaluate_finalization_provenance(
    *,
    evidence_id: str,
    receipts: list[FinalizationReceipt],
    judge_model_family: str,
) -> FinalizationVerdict:
    """Validate-only (block-don't-repair) resolver for the JSG-01 finalization-provenance subpredicate.

    Returns CLEARED only when a single current, cross-family, binding-consistent receipt
    exists for evidence_id; otherwise BLOCKED. Never authors, defaults, repairs, or infers.

    NOTE: this resolves the *provenance* subpredicate only. Whether the returned
    final_pre_decision_status is an allowed *cleared* value (vs excluded/uncertain) is a
    separate conductor-owned JSG-01 check; this consumer surfaces the value, it does not police it.
    """

    def blocked(reason: str) -> FinalizationVerdict:
        return FinalizationVerdict(result=FinalizationProvenanceResult.BLOCKED, reason=reason)

    if not judge_model_family.strip():
        return blocked("run judge_model_family was not provided to the consumer")

    scoped = [receipt for receipt in receipts if receipt.evidence_id == evidence_id]
    if not scoped:
        return blocked(f"no FinalizationReceipt found for evidence_id {evidence_id!r}")

    current = select_current_receipt(scoped)
    if current is None:
        return blocked("zero or more-than-one current (un-superseded) receipt for evidence_id")

    # Cross-family for THIS run: the receipt's recorded judge family must be the run's judge
    # family. Given that, finalizer != run judge follows from the model's finalizer != judge
    # invariant, so no separate finalizer-vs-run-judge check is needed.
    if current.judge_model_family != judge_model_family:
        return blocked("current receipt judge_model_family does not match the run's judge family")

    # Defense-in-depth: do not trust the model's finalizer != judge invariant alone — a
    # constructed receipt can be mutated after validation (or built via model_construct).
    # Re-check the cross-family constraint against the run's judge at the gate.
    if not current.finalizer_model_family.strip() or current.finalizer_model_family == judge_model_family:
        return blocked("current receipt finalizer is missing or same-family as the run judge")

    if current.binding_hash != compute_binding_hash(current.evidence_id, current.finalized_over):
        return blocked("current receipt binding_hash does not match its finalized_over inputs")

    return FinalizationVerdict(
        result=FinalizationProvenanceResult.CLEARED,
        reason="single current cross-family binding-consistent FinalizationReceipt",
        final_pre_decision_status=current.final_pre_decision_status,
        current_receipt_id=current.receipt_id,
    )
