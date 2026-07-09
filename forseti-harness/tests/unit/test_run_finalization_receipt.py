from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

import runners.run_finalization_receipt as runner
from harness_utils import load_yaml_documents
from runners.run_finalization_receipt import (
    FinalizationActError,
    FinalizationPostWriteVerificationError,
    load_receipts,
    main,
    perform_finalization_act,
)
from schemas.case_models import PreDecisionStatus
from schemas.finalization_models import (
    FinalizationProvenanceResult,
    FinalizationVerdict,
    evaluate_finalization_provenance,
)

JUDGE = "family_alpha"
FINALIZER = "family_beta"


def _act(receipts_file: Path, **overrides):
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
    return perform_finalization_act(receipts_file, **kwargs)


# ---- the act: append + verify ----

def test_act_creates_stream_and_consumer_clears(tmp_path: Path) -> None:
    receipts_file = tmp_path / "receipts.yaml"
    receipt = _act(receipts_file)

    assert receipts_file.exists()
    persisted = load_receipts(receipts_file)
    assert [r.receipt_id for r in persisted] == [receipt.receipt_id]

    verdict = evaluate_finalization_provenance(
        evidence_id="ev-1", receipts=persisted, judge_model_family=JUDGE
    )
    assert verdict.result is FinalizationProvenanceResult.CLEARED
    assert verdict.current_receipt_id == receipt.receipt_id
    assert verdict.final_pre_decision_status is PreDecisionStatus.VERIFIED_PRE_DECISION


def test_correction_appends_and_retains_prior(tmp_path: Path) -> None:
    receipts_file = tmp_path / "receipts.yaml"
    original = _act(
        receipts_file, final_pre_decision_status=PreDecisionStatus.UNCERTAIN_TIMESTAMP
    )
    stream_after_original = receipts_file.read_text(encoding="utf-8")

    correction = _act(receipts_file, supersedes=original.receipt_id)

    # Append-only: the original receipt's serialized bytes are untouched.
    stream = receipts_file.read_text(encoding="utf-8")
    assert stream.startswith(stream_after_original)

    persisted = load_receipts(receipts_file)
    assert [r.receipt_id for r in persisted] == [original.receipt_id, correction.receipt_id]
    verdict = evaluate_finalization_provenance(
        evidence_id="ev-1", receipts=persisted, judge_model_family=JUDGE
    )
    assert verdict.result is FinalizationProvenanceResult.CLEARED
    assert verdict.current_receipt_id == correction.receipt_id
    assert verdict.final_pre_decision_status is PreDecisionStatus.VERIFIED_PRE_DECISION


def test_other_evidence_ids_do_not_gate_the_act(tmp_path: Path) -> None:
    receipts_file = tmp_path / "receipts.yaml"
    _act(receipts_file, evidence_id="ev-1")
    second = _act(receipts_file, evidence_id="ev-2")

    persisted = load_receipts(receipts_file)
    assert len(persisted) == 2
    verdict = evaluate_finalization_provenance(
        evidence_id="ev-2", receipts=persisted, judge_model_family=JUDGE
    )
    assert verdict.result is FinalizationProvenanceResult.CLEARED
    assert verdict.current_receipt_id == second.receipt_id


# ---- refusals: nothing written, nothing repaired ----

def _assert_unchanged(receipts_file: Path, before: str | None) -> None:
    if before is None:
        assert not receipts_file.exists()
    else:
        assert receipts_file.read_text(encoding="utf-8") == before


def test_second_receipt_without_supersedes_refused(tmp_path: Path) -> None:
    receipts_file = tmp_path / "receipts.yaml"
    original = _act(receipts_file)
    before = receipts_file.read_text(encoding="utf-8")

    with pytest.raises(FinalizationActError, match=original.receipt_id):
        _act(receipts_file)
    _assert_unchanged(receipts_file, before)


def test_supersedes_unknown_receipt_refused(tmp_path: Path) -> None:
    receipts_file = tmp_path / "receipts.yaml"
    _act(receipts_file)
    before = receipts_file.read_text(encoding="utf-8")

    with pytest.raises(FinalizationActError, match="does not name an existing receipt"):
        _act(receipts_file, supersedes="r-not-present")
    _assert_unchanged(receipts_file, before)


def test_supersedes_receipt_of_other_evidence_refused(tmp_path: Path) -> None:
    receipts_file = tmp_path / "receipts.yaml"
    other = _act(receipts_file, evidence_id="ev-other")
    before = receipts_file.read_text(encoding="utf-8")

    with pytest.raises(FinalizationActError, match="same evidence unit"):
        _act(receipts_file, evidence_id="ev-1", supersedes=other.receipt_id)
    _assert_unchanged(receipts_file, before)


def test_branching_correction_refused(tmp_path: Path) -> None:
    receipts_file = tmp_path / "receipts.yaml"
    original = _act(
        receipts_file, final_pre_decision_status=PreDecisionStatus.UNCERTAIN_TIMESTAMP
    )
    _act(receipts_file, supersedes=original.receipt_id)
    before = receipts_file.read_text(encoding="utf-8")

    with pytest.raises(FinalizationActError, match="already superseded"):
        _act(receipts_file, supersedes=original.receipt_id)
    _assert_unchanged(receipts_file, before)


def test_same_family_act_refused_and_not_written(tmp_path: Path) -> None:
    receipts_file = tmp_path / "receipts.yaml"
    with pytest.raises(FinalizationActError, match="nothing was written"):
        _act(receipts_file, finalizer_model_family=JUDGE)
    _assert_unchanged(receipts_file, None)


def test_blank_proposed_basis_refused(tmp_path: Path) -> None:
    receipts_file = tmp_path / "receipts.yaml"
    with pytest.raises(FinalizationActError, match="nothing was written"):
        _act(receipts_file, proposed_pre_decision_basis="   ")
    _assert_unchanged(receipts_file, None)


def test_malformed_existing_stream_blocks_and_is_not_repaired(tmp_path: Path) -> None:
    receipts_file = tmp_path / "receipts.yaml"
    receipts_file.write_text("---\nnot_a_receipt: true\n", encoding="utf-8")
    before = receipts_file.read_text(encoding="utf-8")

    with pytest.raises(FinalizationActError, match="block-don't-repair"):
        _act(receipts_file)
    _assert_unchanged(receipts_file, before)


def test_post_write_verification_failure_reports_recorded_not_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    receipts_file = tmp_path / "receipts.yaml"

    def blocked_verdict(**_kwargs) -> FinalizationVerdict:
        return FinalizationVerdict(
            result=FinalizationProvenanceResult.BLOCKED,
            reason="forced verification failure",
        )

    monkeypatch.setattr(runner, "evaluate_finalization_provenance", blocked_verdict)

    with pytest.raises(
        FinalizationPostWriteVerificationError, match="retained for audit"
    ):
        _act(receipts_file)

    documents = load_yaml_documents(receipts_file)
    assert len(documents) == 1
    assert documents[0]["evidence_id"] == "ev-1"


def test_post_write_load_failure_reports_recorded_not_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Adjudication extension of F-01: a fresh read that fails AFTER the append is
    # also a post-write failure and must not surface as refused/nothing-written.
    receipts_file = tmp_path / "receipts.yaml"
    real_load = runner.load_receipts
    calls = {"count": 0}

    def load_then_fail(path: Path):
        calls["count"] += 1
        if calls["count"] == 1:
            return real_load(path)
        raise FinalizationActError("simulated post-write read corruption")

    monkeypatch.setattr(runner, "load_receipts", load_then_fail)

    with pytest.raises(
        FinalizationPostWriteVerificationError, match="post-write fresh read failed"
    ):
        _act(receipts_file)

    documents = load_yaml_documents(receipts_file)
    assert len(documents) == 1
    assert documents[0]["evidence_id"] == "ev-1"


# ---- CLI ----

def _cli(receipts_file: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    project_root = Path(__file__).resolve().parents[2]
    argv = [
        sys.executable,
        "runners/run_finalization_receipt.py",
        "--receipts-file",
        str(receipts_file),
        "--evidence-id",
        "ev-cli",
        "--proposed-status",
        "uncertain_timestamp",
        "--proposed-basis",
        "packing proposed value pending finalization",
        "--final-status",
        "verified_pre_decision",
        "--finalizer-identity",
        "operator:band_labeler_1",
        "--judge-model-family",
        JUDGE,
        "--finalizer-model-family",
        FINALIZER,
        *extra,
    ]
    return subprocess.run(
        argv, cwd=project_root, check=False, capture_output=True, text=True
    )


def test_cli_records_receipt(tmp_path: Path) -> None:
    receipts_file = tmp_path / "receipts.yaml"
    result = _cli(receipts_file)

    assert result.returncode == 0, result.stderr
    assert "receipt_id:" in result.stdout
    documents = load_yaml_documents(receipts_file)
    assert len(documents) == 1
    assert documents[0]["evidence_id"] == "ev-cli"
    assert documents[0]["final_pre_decision_status"] == "verified_pre_decision"


def test_cli_refusal_exits_nonzero_with_visible_reason(tmp_path: Path) -> None:
    receipts_file = tmp_path / "receipts.yaml"
    first = _cli(receipts_file)
    assert first.returncode == 0, first.stderr

    second = _cli(receipts_file)
    assert second.returncode == 2
    assert "finalization act refused" in second.stderr
    assert len(load_yaml_documents(receipts_file)) == 1


def test_main_post_write_verification_failure_exits_distinct_status(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    receipts_file = tmp_path / "receipts.yaml"

    def blocked_verdict(**_kwargs) -> FinalizationVerdict:
        return FinalizationVerdict(
            result=FinalizationProvenanceResult.BLOCKED,
            reason="forced verification failure",
        )

    monkeypatch.setattr(runner, "evaluate_finalization_provenance", blocked_verdict)

    with pytest.raises(SystemExit) as exc_info:
        main(
            [
                "--receipts-file",
                str(receipts_file),
                "--evidence-id",
                "ev-main-failed",
                "--proposed-status",
                "uncertain_timestamp",
                "--proposed-basis",
                "packing proposed value pending finalization",
                "--final-status",
                "verified_pre_decision",
                "--finalizer-identity",
                "operator:band_labeler_1",
                "--judge-model-family",
                JUDGE,
                "--finalizer-model-family",
                FINALIZER,
            ]
        )

    captured = capsys.readouterr()
    assert exc_info.value.code == 3
    assert "recorded but not verified" in captured.err
    assert "refused" not in captured.err
    assert len(load_yaml_documents(receipts_file)) == 1


def test_main_returns_zero_in_process(tmp_path: Path) -> None:
    receipts_file = tmp_path / "receipts.yaml"
    exit_code = main(
        [
            "--receipts-file",
            str(receipts_file),
            "--evidence-id",
            "ev-main",
            "--proposed-status",
            "uncertain_timestamp",
            "--proposed-basis",
            "packing proposed value pending finalization",
            "--final-status",
            "excluded",
            "--finalizer-identity",
            "operator:band_labeler_1",
            "--judge-model-family",
            JUDGE,
            "--finalizer-model-family",
            FINALIZER,
        ]
    )
    assert exit_code == 0
    persisted = load_receipts(receipts_file)
    assert persisted[0].final_pre_decision_status is PreDecisionStatus.EXCLUDED
