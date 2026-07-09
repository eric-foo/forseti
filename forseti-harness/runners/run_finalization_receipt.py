"""SP-5 finalization acting half: operator-driven FinalizationReceipt producer.

Performs the *recording* of one out-of-band finalization act against the
existing ``schemas.finalization_models`` contract (committed ``a37f896``): the
operator -- the AR-01 finalizer (distinct cross-family act, operator-for-now) --
supplies the Packing-proposed inputs, the final ``pre_decision_status``, and the
actor/family provenance; this runner stamps identity / time / binding
(per-receipt ULID, UTC ``finalized_at``, deterministic ``binding_hash``) and
appends the receipt to an append-only YAML document stream.

Boundary (do not relax):

- The act itself happens out-of-band. This tool records it; it never authors,
  defaults, repairs, or infers a final value (block-don't-repair, both sides:
  a malformed existing receipt set blocks the act; nothing is rewritten).
- Family values are operator attestations (spec A3; product-learning grade) --
  recorded, never verified against a live provider. No live LLM calls.
- Receipts are append-only: a correction is a NEW receipt carrying
  ``supersedes=<prior receipt_id>``; priors are retained for audit. This runner
  refuses any act that would not leave exactly one current receipt for the
  evidence_id (it never auto-supersedes on the operator's behalf).
- Recording a receipt does NOT unfreeze JSG-01, clear any case, or mint any
  claim tier; the validate-only consumer + the frozen conductor own reads.
"""
from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from pydantic import ValidationError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness_utils import append_yaml_document, load_yaml_documents
from schemas.case_models import PreDecisionStatus
from schemas.finalization_models import (
    FinalizationProvenanceResult,
    FinalizationReceipt,
    build_finalization_receipt,
    evaluate_finalization_provenance,
    select_current_receipt,
)


class FinalizationActError(ValueError):
    """A visible block: the finalization act was refused and nothing was written."""


class FinalizationPostWriteVerificationError(RuntimeError):
    """The receipt was appended, but the fresh-read consumer did not verify it."""


def load_receipts(receipts_file: Path) -> list[FinalizationReceipt]:
    """Strictly load every receipt document from the append-only stream.

    Any unreadable or schema-invalid document blocks (block-don't-repair): the
    error names the failing document; nothing is skipped, defaulted, or repaired.
    """
    try:
        documents = load_yaml_documents(receipts_file)
    except ValueError as exc:
        raise FinalizationActError(str(exc)) from exc
    receipts: list[FinalizationReceipt] = []
    for index, document in enumerate(documents, start=1):
        try:
            receipts.append(FinalizationReceipt.model_validate(document))
        except ValidationError as exc:
            raise FinalizationActError(
                f"receipts file {receipts_file} document {index} is not a valid "
                f"FinalizationReceipt; refusing to act over a malformed receipt "
                f"set (block-don't-repair): {exc}"
            ) from exc
    return receipts


def perform_finalization_act(
    receipts_file: Path,
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
    """Record one finalization act as a new appended receipt, or refuse visibly.

    Guards (all checked BEFORE anything is written; on failure the stream is
    untouched):

    1. The existing receipt stream must load and validate strictly.
    2. The new receipt must construct validly (the model enforces cross-family,
       non-empty provenance fields, and the binding hash).
    3. The act must leave exactly one current receipt for ``evidence_id``:
       an existing current receipt requires an explicit ``supersedes`` naming
       it; ``supersedes`` must name a receipt of the SAME evidence_id that is
       not already superseded. The post-append scoped set is simulated and the
       new receipt must be its single current (backstop over the same
       ``select_current_receipt`` rules the consumer blocks on).

    After the append, the stream is re-read fresh and the validate-only consumer
    must return CLEARED with the new receipt as current; any mismatch raises.
    """
    existing = load_receipts(receipts_file)

    try:
        receipt = build_finalization_receipt(
            evidence_id=evidence_id,
            proposed_pre_decision_status=proposed_pre_decision_status,
            proposed_pre_decision_basis=proposed_pre_decision_basis,
            final_pre_decision_status=final_pre_decision_status,
            finalizer_identity=finalizer_identity,
            judge_model_family=judge_model_family,
            finalizer_model_family=finalizer_model_family,
            supersedes=supersedes,
        )
    except ValidationError as exc:
        raise FinalizationActError(
            f"finalization receipt is invalid; nothing was written: {exc}"
        ) from exc

    scoped_existing = [r for r in existing if r.evidence_id == evidence_id]
    scoped_by_id = {r.receipt_id: r for r in scoped_existing}

    if supersedes is None:
        current = select_current_receipt(scoped_existing) if scoped_existing else None
        if scoped_existing:
            if current is not None:
                raise FinalizationActError(
                    f"evidence_id {evidence_id!r} already has a current receipt "
                    f"({current.receipt_id}); a correction must explicitly pass "
                    f"--supersedes {current.receipt_id} (this tool never "
                    f"auto-supersedes)."
                )
            raise FinalizationActError(
                f"evidence_id {evidence_id!r} has existing receipts but no single "
                f"current one (malformed or ambiguous chain); refusing to append "
                f"over it (block-don't-repair)."
            )
    else:
        if supersedes not in scoped_by_id:
            raise FinalizationActError(
                f"--supersedes {supersedes!r} does not name an existing receipt "
                f"for evidence_id {evidence_id!r}; a correction must supersede a "
                f"receipt of the same evidence unit."
            )
        already_superseded = {
            r.supersedes for r in scoped_existing if r.supersedes is not None
        }
        if supersedes in already_superseded:
            raise FinalizationActError(
                f"receipt {supersedes!r} is already superseded; correcting it "
                f"again would branch the chain. Supersede the CURRENT receipt "
                f"instead."
            )

    simulated = scoped_existing + [receipt]
    if select_current_receipt(simulated) is not receipt:
        raise FinalizationActError(
            f"appending this receipt would not leave it as the single current "
            f"receipt for evidence_id {evidence_id!r}; refusing the act "
            f"(zero or more-than-one current => the consumer blocks)."
        )

    append_yaml_document(receipts_file, receipt.model_dump())

    # Post-write verification: fresh read; the validate-only consumer must clear
    # on exactly the receipt just recorded. Fail visibly on any mismatch. A fresh
    # read that fails AFTER the append is a post-write failure too: it must not
    # surface through the refused/nothing-written path (F-01 closure).
    try:
        persisted = load_receipts(receipts_file)
    except FinalizationActError as exc:
        raise FinalizationPostWriteVerificationError(
            f"post-write fresh read failed after appending receipt "
            f"{receipt.receipt_id}: {exc}; the appended receipt was retained "
            f"for audit but the act is NOT verified."
        ) from exc
    verdict = evaluate_finalization_provenance(
        evidence_id=evidence_id,
        receipts=persisted,
        judge_model_family=judge_model_family,
    )
    if (
        verdict.result is not FinalizationProvenanceResult.CLEARED
        or verdict.current_receipt_id != receipt.receipt_id
    ):
        raise FinalizationPostWriteVerificationError(
            f"post-write verification failed for receipt {receipt.receipt_id} "
            f"({verdict.result.value}: {verdict.reason}); the appended receipt "
            f"was retained for audit but the act is NOT verified."
        )
    return receipt


def _build_parser() -> argparse.ArgumentParser:
    status_values = sorted(status.value for status in PreDecisionStatus)
    parser = argparse.ArgumentParser(
        description=(
            "Record one out-of-band SP-5 finalization act as an appended "
            "FinalizationReceipt (operator-driven; block-don't-repair; no live "
            "LLM calls; does not unfreeze JSG-01)."
        )
    )
    parser.add_argument(
        "--receipts-file",
        type=Path,
        required=True,
        help="Append-only YAML document stream the receipt is appended to (created if missing).",
    )
    parser.add_argument("--evidence-id", required=True, help="The EvidenceUnit being finalized (association/index, not unique).")
    parser.add_argument(
        "--proposed-status",
        required=True,
        choices=status_values,
        help="The Packing-proposed pre_decision_status being finalized over.",
    )
    parser.add_argument(
        "--proposed-basis",
        required=True,
        help="The Packing-proposed pre_decision_basis being finalized over (non-empty).",
    )
    parser.add_argument(
        "--final-status",
        required=True,
        choices=status_values,
        help="The finalizer's out-of-band final pre_decision_status (may confirm or change the proposed value).",
    )
    parser.add_argument(
        "--finalizer-identity",
        required=True,
        help="Decision-B provenance: who performed the act (e.g. operator:band_labeler_1).",
    )
    parser.add_argument(
        "--judge-model-family",
        required=True,
        help="Operator-recorded judge model family (attestation, spec A3).",
    )
    parser.add_argument(
        "--finalizer-model-family",
        required=True,
        help="Operator-recorded finalizer model family; must differ from the judge family (no testee-tester).",
    )
    parser.add_argument(
        "--supersedes",
        default=None,
        help="Prior receipt_id this correction supersedes (append-only correction; required when a current receipt exists).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        receipt = perform_finalization_act(
            args.receipts_file,
            evidence_id=args.evidence_id,
            proposed_pre_decision_status=PreDecisionStatus(args.proposed_status),
            proposed_pre_decision_basis=args.proposed_basis,
            final_pre_decision_status=PreDecisionStatus(args.final_status),
            finalizer_identity=args.finalizer_identity,
            judge_model_family=args.judge_model_family,
            finalizer_model_family=args.finalizer_model_family,
            supersedes=args.supersedes,
        )
    except FinalizationActError as exc:
        parser.exit(status=2, message=f"finalization act refused: {exc}\n")
    except FinalizationPostWriteVerificationError as exc:
        parser.exit(
            status=3,
            message=f"finalization act recorded but not verified: {exc}\n",
        )

    print(f"receipt_id: {receipt.receipt_id}")
    print(f"evidence_id: {receipt.evidence_id}")
    print(f"final_pre_decision_status: {receipt.final_pre_decision_status.value}")
    print(f"finalizer_model_family: {receipt.finalizer_model_family}")
    print(f"judge_model_family: {receipt.judge_model_family}")
    print(f"supersedes: {receipt.supersedes or 'none'}")
    print(f"receipts_file: {args.receipts_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
