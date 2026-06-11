"""Pure composer for the JSG-01-scoped EvidenceUnit binding (slice B).

``compose_jsg01_evidence_record`` is a pure function over its frozen inputs
(binding, packet, receipts, run judge family): no I/O, no mutation,
deterministic. File reads belong to the assembly runner (slice C), not here.

Behavior (ratified contract; do not relax):

- Key guards block, don't repair: a binding whose keys do not resolve against
  the packet raises ``Jsg01BindingError`` — a malformed binding is a visible
  block, never a residual, never silently re-keyed. A low-quality or
  non-clearing bound slice is still carried as the bound read; the composer
  never searches for, promotes, or repairs toward a better-clearing sibling.
- Posture reads carry the four built derivers' output verbatim (re-derive,
  never migrate); the full per-slice SP-2/SP-3 vectors ride along so failing
  siblings stay visible.
- The finalization read carries the validate-only consumer's verdict verbatim:
  a missing/invalid/ambiguous receipt set is the consumer's BLOCKED verdict —
  an honest named state, never an invention. ``judge_model_family`` flows in
  from the run context; the composer never supplies or defaults it.
- NO aggregate verdict is computed; the frozen JSG-01 conductor owns that.
"""
from __future__ import annotations

from ecr.deriver import (
    derive_identity_postures,
    derive_inspectability_postures,
    derive_source_visibility_postures,
    derive_timing_postures,
)
from evidence_binding.models import (
    Jsg01EvidenceBinding,
    Jsg01EvidenceRecord,
    Jsg01FinalizationRead,
)
from schemas.finalization_models import (
    FinalizationReceipt,
    evaluate_finalization_provenance,
)
from source_capture.models import SourceCapturePacket


class Jsg01BindingError(ValueError):
    """A malformed binding: a visible block — never a residual, never re-keyed."""


def compose_jsg01_evidence_record(
    *,
    binding: Jsg01EvidenceBinding,
    packet: SourceCapturePacket,
    receipts: list[FinalizationReceipt],
    judge_model_family: str,
) -> Jsg01EvidenceRecord:
    """Compose the five JSG-01 reads for one bound evidence unit, by key."""
    if packet.packet_id != binding.packet_id:
        raise Jsg01BindingError(
            f"binding packet_id {binding.packet_id!r} does not match the supplied "
            f"packet {packet.packet_id!r}; block-don't-repair."
        )
    slice_ids = [source_slice.slice_id for source_slice in packet.source_slices]
    matches = slice_ids.count(binding.evidence_slice_id)
    if matches == 0:
        raise Jsg01BindingError(
            f"evidence_slice_id {binding.evidence_slice_id!r} names no slice in "
            f"packet {packet.packet_id!r} (slices: {slice_ids}); block-don't-repair."
        )
    if matches > 1:
        raise Jsg01BindingError(
            f"evidence_slice_id {binding.evidence_slice_id!r} is ambiguous in "
            f"packet {packet.packet_id!r} ({matches} slices carry it); "
            f"block-don't-repair."
        )

    [identity] = derive_identity_postures(packet)
    [source_visibility] = derive_source_visibility_postures(packet)
    timing = derive_timing_postures(packet)
    inspectability = derive_inspectability_postures(packet)

    verdict = evaluate_finalization_provenance(
        evidence_id=binding.evidence_id,
        receipts=receipts,
        judge_model_family=judge_model_family,
    )
    finalization = Jsg01FinalizationRead(
        result=verdict.result,
        reason=verdict.reason,
        final_pre_decision_status=verdict.final_pre_decision_status,
        current_receipt_id=verdict.current_receipt_id,
    )

    return Jsg01EvidenceRecord(
        evidence_id=binding.evidence_id,
        packet_id=binding.packet_id,
        evidence_slice_id=binding.evidence_slice_id,
        identity=identity,
        source_visibility=source_visibility,
        timing=timing,
        inspectability=inspectability,
        finalization=finalization,
    )
