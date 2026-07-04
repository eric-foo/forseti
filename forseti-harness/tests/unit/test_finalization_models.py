from __future__ import annotations

import pytest
from pydantic import ValidationError

from schemas.case_models import PreDecisionStatus
from schemas.finalization_models import (
    FinalizationProvenanceResult,
    FinalizationReceipt,
    FinalizedOver,
    build_finalization_receipt,
    compute_binding_hash,
    evaluate_finalization_provenance,
    select_current_receipt,
)

JUDGE = "family_alpha"
FINALIZER = "family_beta"


def _receipt(**overrides) -> FinalizationReceipt:
    kwargs = dict(
        evidence_id="ev-1",
        proposed_pre_decision_status=PreDecisionStatus.UNCERTAIN_TIMESTAMP,
        proposed_pre_decision_basis="packing proposed value pending finalization",
        final_pre_decision_status=PreDecisionStatus.VERIFIED_PRE_DECISION,
        finalizer_identity="operator:band_labeler_1",
        judge_model_family=JUDGE,
        finalizer_model_family=FINALIZER,
    )
    kwargs.update(overrides)
    return build_finalization_receipt(**kwargs)


def _raw_fields(**overrides) -> dict:
    fo = FinalizedOver(
        proposed_pre_decision_status=PreDecisionStatus.UNCERTAIN_TIMESTAMP,
        proposed_pre_decision_basis="packing proposed value pending finalization",
    )
    fields = dict(
        receipt_id="r-original",
        evidence_id="ev-1",
        finalized_over=fo,
        final_pre_decision_status=PreDecisionStatus.VERIFIED_PRE_DECISION,
        finalizer_identity="operator:band_labeler_1",
        judge_model_family=JUDGE,
        finalizer_model_family=FINALIZER,
        finalized_at="2026-06-10T00:00:00Z",
        binding_hash=compute_binding_hash("ev-1", fo),
    )
    fields.update(overrides)
    return fields


# ---- model construction + invariants ----

def test_valid_receipt_builds_and_validates():
    receipt = _receipt()
    assert receipt.receipt_id
    assert receipt.supersedes is None
    assert receipt.binding_hash == compute_binding_hash(receipt.evidence_id, receipt.finalized_over)


def test_binding_hash_is_deterministic():
    fo = FinalizedOver(
        proposed_pre_decision_status=PreDecisionStatus.UNCERTAIN_TIMESTAMP,
        proposed_pre_decision_basis="same inputs",
    )
    assert compute_binding_hash("ev-9", fo) == compute_binding_hash("ev-9", fo)
    other = FinalizedOver(
        proposed_pre_decision_status=PreDecisionStatus.UNCERTAIN_TIMESTAMP,
        proposed_pre_decision_basis="different inputs",
    )
    assert compute_binding_hash("ev-9", fo) != compute_binding_hash("ev-9", other)


def test_same_family_self_finalization_rejected():
    with pytest.raises(ValidationError):
        FinalizationReceipt(**_raw_fields(finalizer_model_family=JUDGE))


def test_binding_hash_tamper_rejected():
    with pytest.raises(ValidationError):
        FinalizationReceipt(**_raw_fields(binding_hash="0" * 64))


def test_self_supersede_rejected():
    with pytest.raises(ValidationError):
        FinalizationReceipt(**_raw_fields(receipt_id="r-x", supersedes="r-x"))


def test_blank_required_field_rejected():
    with pytest.raises(ValidationError):
        FinalizationReceipt(**_raw_fields(finalizer_identity="   "))


# ---- current-designation (supersedes-via-ULID) ----

def test_select_current_single_original():
    receipt = _receipt()
    assert select_current_receipt([receipt]) is receipt


def test_select_current_follows_supersede_chain():
    original = _receipt()
    correction = _receipt(supersedes=original.receipt_id)
    assert select_current_receipt([original, correction]) is correction


def test_select_current_two_unsuperseded_is_none():
    assert select_current_receipt([_receipt(), _receipt()]) is None


def test_select_current_empty_is_none():
    assert select_current_receipt([]) is None


# ---- consumer: validate-only, block-don't-repair ----

def test_evaluate_valid_clears_and_surfaces_status():
    receipt = _receipt()
    verdict = evaluate_finalization_provenance(
        evidence_id="ev-1", receipts=[receipt], judge_model_family=JUDGE
    )
    assert verdict.result is FinalizationProvenanceResult.CLEARED
    assert verdict.final_pre_decision_status is PreDecisionStatus.VERIFIED_PRE_DECISION
    assert verdict.current_receipt_id == receipt.receipt_id


def test_evaluate_correction_clears_on_current_value():
    original = _receipt(final_pre_decision_status=PreDecisionStatus.UNCERTAIN_TIMESTAMP)
    correction = _receipt(
        supersedes=original.receipt_id,
        final_pre_decision_status=PreDecisionStatus.VERIFIED_PRE_DECISION,
    )
    verdict = evaluate_finalization_provenance(
        evidence_id="ev-1", receipts=[original, correction], judge_model_family=JUDGE
    )
    assert verdict.result is FinalizationProvenanceResult.CLEARED
    assert verdict.final_pre_decision_status is PreDecisionStatus.VERIFIED_PRE_DECISION
    assert verdict.current_receipt_id == correction.receipt_id


def test_evaluate_missing_blocks_and_authors_nothing():
    verdict = evaluate_finalization_provenance(
        evidence_id="ev-missing", receipts=[_receipt()], judge_model_family=JUDGE
    )
    assert verdict.result is FinalizationProvenanceResult.BLOCKED
    assert verdict.final_pre_decision_status is None
    assert verdict.current_receipt_id is None


def test_evaluate_two_currents_blocks():
    verdict = evaluate_finalization_provenance(
        evidence_id="ev-1", receipts=[_receipt(), _receipt()], judge_model_family=JUDGE
    )
    assert verdict.result is FinalizationProvenanceResult.BLOCKED
    assert verdict.final_pre_decision_status is None


def test_evaluate_judge_family_mismatch_blocks():
    verdict = evaluate_finalization_provenance(
        evidence_id="ev-1", receipts=[_receipt()], judge_model_family="family_gamma"
    )
    assert verdict.result is FinalizationProvenanceResult.BLOCKED


def test_evaluate_excluded_final_status_still_surfaces_for_conductor_value_gate():
    # The consumer owns provenance, not value-clearedness: an EXCLUDED final value still
    # clears PROVENANCE and is surfaced for the conductor's separate value check.
    receipt = _receipt(final_pre_decision_status=PreDecisionStatus.EXCLUDED)
    verdict = evaluate_finalization_provenance(
        evidence_id="ev-1", receipts=[receipt], judge_model_family=JUDGE
    )
    assert verdict.result is FinalizationProvenanceResult.CLEARED
    assert verdict.final_pre_decision_status is PreDecisionStatus.EXCLUDED


def test_evaluate_blank_run_judge_blocks():
    verdict = evaluate_finalization_provenance(
        evidence_id="ev-1", receipts=[_receipt()], judge_model_family="   "
    )
    assert verdict.result is FinalizationProvenanceResult.BLOCKED


# ---- review-hardening: malformed scoped sets block (F1 dangling, F2 dup-id, F3 cycle, F4 mutation) ----

def _raw_receipt(**overrides) -> FinalizationReceipt:
    return FinalizationReceipt(**_raw_fields(**overrides))


def test_dangling_supersedes_blocks():
    receipt = _raw_receipt(receipt_id="r-correction", supersedes="r-not-present")
    assert select_current_receipt([receipt]) is None
    verdict = evaluate_finalization_provenance(
        evidence_id="ev-1", receipts=[receipt], judge_model_family=JUDGE
    )
    assert verdict.result is FinalizationProvenanceResult.BLOCKED
    assert verdict.final_pre_decision_status is None


def test_duplicate_receipt_id_blocks():
    a = _raw_receipt(receipt_id="dup")
    b = _raw_receipt(receipt_id="dup")
    assert select_current_receipt([a, b]) is None


def test_supersedes_cycle_blocks():
    a = _raw_receipt(receipt_id="A", supersedes="B")
    b = _raw_receipt(receipt_id="B", supersedes="A")
    c = _raw_receipt(receipt_id="C", supersedes="A")
    assert select_current_receipt([a, b, c]) is None


def test_mutated_same_family_finalizer_blocks():
    # The model rejects finalizer == judge at construction; a post-construction mutation
    # bypasses that validator, so the consumer must re-check the cross-family constraint.
    receipt = _receipt()
    receipt.finalizer_model_family = JUDGE
    verdict = evaluate_finalization_provenance(
        evidence_id="ev-1", receipts=[receipt], judge_model_family=JUDGE
    )
    assert verdict.result is FinalizationProvenanceResult.BLOCKED
    assert verdict.final_pre_decision_status is None
