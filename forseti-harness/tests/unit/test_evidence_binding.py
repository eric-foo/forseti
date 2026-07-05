from __future__ import annotations

import pytest
from _ecr_builders import build_packet, varied_packet
from pydantic import ValidationError

from ecr.deriver import (
    derive_identity_postures,
    derive_inspectability_postures,
    derive_source_visibility_postures,
    derive_timing_postures,
)
from evidence_binding import (
    Jsg01BindingError,
    Jsg01EvidenceBinding,
    Jsg01EvidenceRecord,
    Jsg01FinalizationRead,
    compose_jsg01_evidence_record,
)
from schemas.case_models import PreDecisionStatus
from schemas.finalization_models import (
    FinalizationProvenanceResult,
    build_finalization_receipt,
    evaluate_finalization_provenance,
)

JUDGE = "family_alpha"
FINALIZER = "family_beta"


def _binding(**overrides) -> Jsg01EvidenceBinding:
    kwargs = dict(evidence_id="E1", packet_id="pkt-test", evidence_slice_id="s_clean")
    kwargs.update(overrides)
    return Jsg01EvidenceBinding(**kwargs)


def _receipt(evidence_id: str = "E1", **overrides):
    kwargs = dict(
        evidence_id=evidence_id,
        proposed_pre_decision_status=PreDecisionStatus.UNCERTAIN_TIMESTAMP,
        proposed_pre_decision_basis="packing proposed value pending finalization",
        final_pre_decision_status=PreDecisionStatus.VERIFIED_PRE_DECISION,
        finalizer_identity="operator:band_labeler_1",
        judge_model_family=JUDGE,
        finalizer_model_family=FINALIZER,
    )
    kwargs.update(overrides)
    return build_finalization_receipt(**kwargs)


def _compose(packet=None, binding=None, receipts=None, judge_model_family=JUDGE):
    return compose_jsg01_evidence_record(
        binding=binding if binding is not None else _binding(),
        packet=packet if packet is not None else varied_packet(),
        receipts=receipts if receipts is not None else [],
        judge_model_family=judge_model_family,
    )


# ---- key guards: block, don't repair ----

def test_packet_id_mismatch_blocks():
    with pytest.raises(Jsg01BindingError, match="does not match the supplied packet"):
        _compose(binding=_binding(packet_id="pkt-other"))


def test_unknown_evidence_slice_blocks():
    with pytest.raises(Jsg01BindingError, match="names no slice"):
        _compose(binding=_binding(evidence_slice_id="s_not_there"))


# ---- grain + key coherence ----

def test_grain_and_key_coherence():
    packet = varied_packet()
    record = _compose(packet=packet)

    assert record.identity.packet_id == packet.packet_id
    assert record.source_visibility.packet_id == packet.packet_id

    slice_ids = [s.slice_id for s in packet.source_slices]
    assert [p.slice_id for p in record.timing] == slice_ids
    assert [p.slice_id for p in record.inspectability] == slice_ids

    assert record.bound_timing().slice_id == "s_clean"
    assert record.bound_inspectability().slice_id == "s_clean"


# ---- anti-laundering: both directions ----

def test_failing_bound_slice_stays_bound_when_sibling_clears():
    # Bind the FAILING slice while a sibling clears: the bound read stays the
    # failing row (no promotion), and the clearing sibling is merely visible.
    record = _compose(binding=_binding(evidence_slice_id="s_placeholder"))

    assert record.bound_timing().clears_pre_cutoff is False
    assert record.bound_timing().carried_cutoff_posture == "post_cutoff"
    assert record.bound_inspectability().clears_inspectable is False

    sibling_timing = {p.slice_id: p for p in record.timing}["s_clean"]
    assert sibling_timing.clears_pre_cutoff is True  # visible, not promoted


def test_clearing_bound_slice_does_not_hide_failing_siblings():
    # Bind the CLEARING slice: failing siblings stay visible in the carried
    # vectors (the no-hide audit surface).
    record = _compose(binding=_binding(evidence_slice_id="s_clean"))

    assert record.bound_timing().clears_pre_cutoff is True
    assert record.bound_inspectability().clears_inspectable is True

    timing_by_slice = {p.slice_id: p for p in record.timing}
    inspect_by_slice = {p.slice_id: p for p in record.inspectability}
    assert timing_by_slice["s_placeholder"].clears_pre_cutoff is False
    assert inspect_by_slice["s_placeholder"].clears_inspectable is False
    assert timing_by_slice["s_dark"].clears_pre_cutoff is False


# ---- verbatim carry ----

def test_postures_equal_the_derivers_direct_output():
    packet = varied_packet()
    record = _compose(packet=packet)

    assert [record.identity] == derive_identity_postures(packet)
    assert [record.source_visibility] == derive_source_visibility_postures(packet)
    assert record.timing == derive_timing_postures(packet)
    assert record.inspectability == derive_inspectability_postures(packet)


def test_finalization_read_equals_the_consumer_verdict():
    receipts = [_receipt()]
    record = _compose(receipts=receipts)
    verdict = evaluate_finalization_provenance(
        evidence_id="E1", receipts=receipts, judge_model_family=JUDGE
    )

    assert record.finalization.result is verdict.result
    assert record.finalization.reason == verdict.reason
    assert record.finalization.final_pre_decision_status is verdict.final_pre_decision_status
    assert record.finalization.current_receipt_id == verdict.current_receipt_id


# ---- finalization read: cleared and blocked carries ----

def test_cleared_finalization_surfaces_consumer_values():
    receipt = _receipt()
    record = _compose(receipts=[receipt])

    assert record.finalization.result is FinalizationProvenanceResult.CLEARED
    assert (
        record.finalization.final_pre_decision_status
        is PreDecisionStatus.VERIFIED_PRE_DECISION
    )
    assert record.finalization.current_receipt_id == receipt.receipt_id


def test_blocked_carry_without_receipts_authors_nothing():
    record = _compose(receipts=[])

    assert record.finalization.result is FinalizationProvenanceResult.BLOCKED
    assert record.finalization.reason.strip()
    assert record.finalization.final_pre_decision_status is None
    assert record.finalization.current_receipt_id is None
    # the rest of the record still composes (postures present at full grain)
    assert len(record.timing) == 4


def test_blocked_carry_on_judge_family_mismatch():
    record = _compose(receipts=[_receipt()], judge_model_family="family_gamma")

    assert record.finalization.result is FinalizationProvenanceResult.BLOCKED
    assert record.finalization.final_pre_decision_status is None


# ---- purity / determinism / round-trip ----

def test_purity_and_determinism():
    packet = varied_packet()
    receipts = [_receipt()]
    before = packet.model_dump()

    first = _compose(packet=packet, receipts=receipts)
    second = _compose(packet=packet, receipts=receipts)

    assert packet.model_dump() == before
    assert first == second


def test_binding_and_record_round_trip():
    binding = _binding()
    assert Jsg01EvidenceBinding.model_validate(binding.model_dump()) == binding

    record = _compose(receipts=[_receipt()])
    assert Jsg01EvidenceRecord.model_validate(record.model_dump()) == record


# ---- the contract's negative space ----

def test_no_aggregate_verdict_field_exists():
    # Combining subpredicates is the FROZEN conductor's job: the record carries
    # exactly the three keys + five reads, and no clears_*/verdict field.
    assert set(Jsg01EvidenceRecord.model_fields) == {
        "evidence_id",
        "packet_id",
        "evidence_slice_id",
        "identity",
        "source_visibility",
        "timing",
        "inspectability",
        "finalization",
    }
    assert not any(
        "clears" in name or "verdict" in name for name in Jsg01EvidenceRecord.model_fields
    )


def test_finalization_read_populated_only_on_cleared():
    with pytest.raises(ValidationError, match="must carry no final status"):
        Jsg01FinalizationRead(
            result=FinalizationProvenanceResult.BLOCKED,
            reason="blocked but smuggling a value",
            final_pre_decision_status=PreDecisionStatus.VERIFIED_PRE_DECISION,
        )
    with pytest.raises(ValidationError, match="must carry the consumer-surfaced"):
        Jsg01FinalizationRead(
            result=FinalizationProvenanceResult.CLEARED,
            reason="cleared without the surfaced values",
        )
    with pytest.raises(ValidationError, match="current_receipt_id must be non-empty"):
        Jsg01FinalizationRead(
            result=FinalizationProvenanceResult.CLEARED,
            reason="cleared with a blank receipt id",
            final_pre_decision_status=PreDecisionStatus.VERIFIED_PRE_DECISION,
            current_receipt_id="   ",
        )


def test_blank_binding_keys_rejected():
    with pytest.raises(ValidationError):
        _binding(evidence_id="   ")
    with pytest.raises(ValidationError):
        _binding(evidence_slice_id="")


def test_record_key_coherence_validators_reject_mismatches():
    record = _compose(receipts=[_receipt()])

    rekeyed = record.model_dump()
    rekeyed["packet_id"] = "pkt-other"
    with pytest.raises(ValidationError, match="different packet_id"):
        Jsg01EvidenceRecord.model_validate(rekeyed)

    unbound = record.model_dump()
    unbound["evidence_slice_id"] = "s_not_carried"
    with pytest.raises(ValidationError, match="exactly one carried slice row"):
        Jsg01EvidenceRecord.model_validate(unbound)

    duplicate_non_bound = record.model_dump()
    duplicate_non_bound["timing"][2]["slice_id"] = "s_placeholder"
    duplicate_non_bound["inspectability"][2]["slice_id"] = "s_placeholder"
    with pytest.raises(ValidationError, match="must not contain duplicate slice_id"):
        Jsg01EvidenceRecord.model_validate(duplicate_non_bound)


def test_single_slice_packet_composes():
    packet = build_packet(
        [
            {
                "id": "archive_snapshot_body",
                "files": [("f0", "a" * 64)],
                "locator_known": True,
                "cutoff": "pre_cutoff",
            }
        ]
    )
    binding = _binding(evidence_slice_id="archive_snapshot_body")
    record = _compose(packet=packet, binding=binding, receipts=[_receipt()])

    assert record.bound_timing().clears_pre_cutoff is True
    assert record.bound_inspectability().clears_inspectable is True
    assert record.finalization.result is FinalizationProvenanceResult.CLEARED
