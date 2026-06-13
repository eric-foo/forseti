"""JSG-01-scoped EvidenceUnit binding models (slice B of the bounded unfreeze build).

Ratified architecture basis: the JSG-01-scoped EvidenceUnit binding contract,
owner-ratified 2026-06-12 at
``docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md``
(design basis:
``docs/product/ecr/ecr_consolidation_v0_jsg01_evidence_unit_binding_slice_plan_v0.md``).
``Jsg01`` working names mark the scope honestly; the canonical object name stays
owner-reserved — everything downstream of the keys re-derives, so a later rename
is cheap.

Design constraints (do not relax without explicit owner authorization):

- Reference-never-merge: the binding is three keys; no posture, content, or
  derived value is stored on it. The composed record carries each read as its
  own sub-record at its own grain, keyed back to its source.
- NO aggregate verdict: combining subpredicates into cleared/not-cleared is the
  FROZEN JSG-01 conductor's job. No field here carries a source-side verdict.
- Anti-laundering: ``evidence_slice_id`` is an assembly-authored assertion of
  which slice's preserved bytes carry the evidence unit's content — never a
  selector over the strongest posture. Bound-row selection is by exact key; a
  failing bound slice stays the bound read; failing siblings stay visible in the
  carried vectors.
- The ``EvidenceUnit`` schema (``schemas/case_models.py``) is UNCHANGED by this
  slice; the binding references it by ``evidence_id`` only.

JSG-01 stays FROZEN; nothing here evaluates, readies, or unfreezes it.
"""
from __future__ import annotations

from pydantic import field_validator, model_validator

from ecr.models import (
    EcrIdentityPosture,
    EcrInspectabilityPosture,
    EcrSourceVisibilityPosture,
    EcrTimingPosture,
)
from schemas.case_models import PreDecisionStatus, StrictModel
from schemas.finalization_models import FinalizationProvenanceResult


class Jsg01EvidenceBinding(StrictModel):
    """The durable binding declaration: three keys, reference-never-merge.

    An assembly-authored key assertion — the slice whose preserved bytes carry
    this evidence unit's content — never a selector over the strongest posture.
    """

    evidence_id: str
    packet_id: str
    evidence_slice_id: str

    @field_validator("evidence_id", "packet_id", "evidence_slice_id")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Jsg01EvidenceBinding keys must be non-empty")
        return value


class Jsg01FinalizationRead(StrictModel):
    """Verbatim carry of the SP-5 validate-only consumer's verdict.

    ``final_pre_decision_status`` / ``current_receipt_id`` are populated ONLY on
    a CLEARED read, and only ever copy the consumer-surfaced values
    (block-don't-repair: a BLOCKED read carries the named reason and nothing
    authored).
    """

    result: FinalizationProvenanceResult
    reason: str
    final_pre_decision_status: PreDecisionStatus | None = None
    current_receipt_id: str | None = None

    @model_validator(mode="after")
    def validate_read(self) -> "Jsg01FinalizationRead":
        if not self.reason.strip():
            raise ValueError("Jsg01FinalizationRead.reason must be non-empty")
        cleared = self.result is FinalizationProvenanceResult.CLEARED
        has_value = (
            self.final_pre_decision_status is not None
            or self.current_receipt_id is not None
        )
        if cleared and (
            self.final_pre_decision_status is None or self.current_receipt_id is None
        ):
            raise ValueError(
                "a CLEARED finalization read must carry the consumer-surfaced "
                "final_pre_decision_status and current_receipt_id"
            )
        if cleared and not self.current_receipt_id.strip():
            raise ValueError(
                "a CLEARED finalization read current_receipt_id must be non-empty"
            )
        if not cleared and has_value:
            raise ValueError(
                "a BLOCKED finalization read must carry no final status or "
                "receipt id (values are consumer-surfaced, never authored)"
            )
        return self


class Jsg01EvidenceRecord(StrictModel):
    """The composed five-read record for one bound evidence unit.

    One record per kind, composed by key, never merged: the per-packet SP-1 and
    SP-6 postures, the FULL per-slice SP-3/SP-2 vectors (the bound row selected
    by exact key via ``bound_timing()`` / ``bound_inspectability()``), and the
    finalization read. Deliberately carries NO aggregate verdict field —
    combining subpredicates is the frozen conductor's job
    (``tests/unit/test_ecr_source_side_composition.py`` discipline).
    """

    evidence_id: str
    packet_id: str
    evidence_slice_id: str
    identity: EcrIdentityPosture
    source_visibility: EcrSourceVisibilityPosture
    timing: list[EcrTimingPosture]
    inspectability: list[EcrInspectabilityPosture]
    finalization: Jsg01FinalizationRead

    @field_validator("evidence_id", "packet_id", "evidence_slice_id")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Jsg01EvidenceRecord keys must be non-empty")
        return value

    @model_validator(mode="after")
    def validate_key_coherence(self) -> "Jsg01EvidenceRecord":
        if self.identity.packet_id != self.packet_id:
            raise ValueError(
                "identity posture is keyed to a different packet_id than the record"
            )
        if self.source_visibility.packet_id != self.packet_id:
            raise ValueError(
                "source-visibility posture is keyed to a different packet_id "
                "than the record"
            )
        timing_ids = [posture.slice_id for posture in self.timing]
        inspect_ids = [posture.slice_id for posture in self.inspectability]
        if timing_ids != inspect_ids:
            raise ValueError(
                "timing and inspectability vectors must align 1:1 by slice_id "
                f"and order; got {timing_ids} vs {inspect_ids}"
            )
        if len(set(timing_ids)) != len(timing_ids):
            raise ValueError(
                "timing and inspectability vectors must not contain duplicate "
                f"slice_id rows; got {timing_ids}"
            )
        if timing_ids.count(self.evidence_slice_id) != 1:
            raise ValueError(
                f"evidence_slice_id {self.evidence_slice_id!r} must match exactly "
                f"one carried slice row; got {timing_ids}"
            )
        return self

    def bound_timing(self) -> EcrTimingPosture:
        """The JSG-01-relevant SP-3 row: selected by exact key, never by posture quality."""
        return next(
            posture
            for posture in self.timing
            if posture.slice_id == self.evidence_slice_id
        )

    def bound_inspectability(self) -> EcrInspectabilityPosture:
        """The JSG-01-relevant SP-2 row: selected by exact key, never by posture quality."""
        return next(
            posture
            for posture in self.inspectability
            if posture.slice_id == self.evidence_slice_id
        )


class Jsg01ClaimSupportAssertion(StrictModel):
    """An assembly-authored assertion that a verbatim span on ONE preserved page backs ONE claim.

    Reference-keyed: claim -> evidence -> packet -> slice -> preserved file. Unlike
    ``Jsg01EvidenceBinding`` (three keys, reference-never-merge), this assertion
    deliberately carries the verbatim ``quoted_span`` and the ``verified_sha256`` it was
    checked against, so the claim -> page -> span -> fingerprint chain is fully retrievable
    for audit. It is a SEPARATE record and does not relax the binding's no-content
    constraint. The span is confirmed against the hash-anchored body by
    ``evidence_binding.verifier.verify_claim_support`` (an I/O step), never by the pure
    composer. Atomic, quotable claims only; aggregate/derived claims assert no span.

    The verifier checks that ``quoted_span`` is PRESENT in the body (a necessary
    precondition); whether the span is specific enough to genuinely support ``claim_id``
    is the asserting author's judgment, not code-enforced.
    """

    claim_id: str
    evidence_id: str
    packet_id: str
    evidence_slice_id: str
    preserved_file_id: str
    quoted_span: str
    verified_sha256: str

    @field_validator(
        "claim_id",
        "evidence_id",
        "packet_id",
        "evidence_slice_id",
        "preserved_file_id",
        "quoted_span",
        "verified_sha256",
    )
    @classmethod
    def reject_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Jsg01ClaimSupportAssertion fields must be non-empty")
        return value
