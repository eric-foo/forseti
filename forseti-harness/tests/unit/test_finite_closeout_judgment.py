"""Exercise the ordinary delivery route; controlled jobs are not quality/cost proof."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from judgment.review_evidence import expand_evidence
from reports import finite_closeout_judgment as judgment
from runners import run_finite_semantic_consolidation as finite
from test_finite_closeout import saved_correction_run


def controlled_response(value):
    return {"conclusion": "Controlled judgment.", "check_results": {
        c["id"]: {"outcome": "preserved", "source_refs": c["source_rows"], "evidence": "Fixture."}
        for c in value["judgment_evidence"]["commissioned_checks"]},
        "material_findings": [], "unassessed_and_limits": "Controlled test, not model evidence."}


@pytest.mark.parametrize("outcome", ["accepted", "retained", "rejected"])
def test_real_saved_run_keeps_commissioned_evidence_and_repeat_cannot_relaunch(tmp_path, monkeypatch, outcome):
    run, _ = saved_correction_run(tmp_path, outcome)
    value = judgment.collect(run.root)
    calls = []

    def job(output, **kwargs):
        packet = json.loads((output / "prompt.md").read_text(encoding="utf-8").split("Consumer view:\n", 1)[1])
        supplied = expand_evidence(packet["evidence"])
        # Complete semantic evidence, answer versions and earlier judgments survive;
        # these assertions do not use the implementation's projection as the oracle.
        for key in ("judgment_evidence", "answers", "answer_commission", "previous_answer_for_comparison",
                    "initial_assessment", "affected_recheck", "wider_sources"):
            assert supplied[key] == value[key]
        native_packet = json.loads((run.root / "packet-all.json").read_text(encoding="utf-8"))
        assert supplied["program_verified_inventory"] == finite.recheck_inventory_facts(native_packet)
        for key in ("status", "answer_material_status", "answer_correction_status"):
            assert supplied["saved_result"][key] == value["saved_result"][key]
        assert supplied["correction_records"]["composition"] == value["correction_records"]["composition"]
        assert "recheck_input" not in supplied["correction_records"]
        for key in ("read_artifact_hashes", "native_accounting", "execution_facts", "usage_by_stage"):
            assert key not in supplied
        bindings = json.loads((output / "evidence-bindings.json").read_text(encoding="utf-8"))
        assert bindings["read_artifact_hashes"] == value["read_artifact_hashes"]
        assert json.loads((output / "consumer.json").read_text(encoding="utf-8")) == packet
        calls.append(kwargs)
        attempt = output / "provider/attempts/controlled"
        attempt.mkdir(parents=True)
        (attempt / "response.json").write_text(json.dumps(controlled_response(value)), encoding="utf-8")
        return {"attempt_dir": str(attempt)}

    monkeypatch.setattr(judgment, "launch", job)
    output = tmp_path / "review"
    result = judgment.judge(run.root, None, output, model="controlled", reasoning_effort="high", timeout_seconds=30)
    assert result["status"] == "FINITE_CLOSEOUT_JUDGMENT_COMPLETE_REQUIRES_ADJUDICATION"
    assert result["selected_answer"] == value["answers"]["selected"]["path"]
    assert judgment.collect(run.root) == value
    assert len(calls) == 1
    assert json.loads((output / "result.json").read_text()) == result
    assert judgment.main(["--run-root", str(run.root), "--output-dir", str(output),
        "--model", "controlled", "--reasoning-effort", "high", "--timeout-seconds", "30"]) == 1
    assert len(calls) == 1


@pytest.mark.parametrize("fault", ["missing_check", "unknown_source", "empty_refs", "artifact_changed", "omitted_input_changed", "provider_failed"])
def test_failed_or_invalid_judgment_is_visible_without_another_job(tmp_path, monkeypatch, fault):
    run, _ = saved_correction_run(tmp_path, "accepted")
    value = judgment.collect(run.root)
    calls = []

    def job(output, **kwargs):
        calls.append(output)
        if fault == "provider_failed":
            raise ValueError("preserved provider failure")
        response = controlled_response(value)
        if fault == "missing_check":
            response["check_results"] = {}
        if fault == "unknown_source":
            response["check_results"]["contrast"]["source_refs"] = ["invented"]
        if fault == "empty_refs":
            response["check_results"]["contrast"]["source_refs"] = []
        if fault == "artifact_changed":
            selected = Path(value["answers"]["selected"]["path"])
            selected.write_text(selected.read_text() + "\n", encoding="utf-8")
        if fault == "omitted_input_changed":
            omitted = run.root / "assessment-recheck/input.json"
            omitted.write_text(omitted.read_text() + "\n", encoding="utf-8")
        attempt = output / "provider/attempts/controlled"
        attempt.mkdir(parents=True)
        (attempt / "response.json").write_text(json.dumps(response), encoding="utf-8")
        return {"attempt_dir": str(attempt)}

    monkeypatch.setattr(judgment, "launch", job)
    output = tmp_path / "review"
    result = judgment.judge(run.root, None, output, model="controlled", reasoning_effort="high", timeout_seconds=30)
    assert result["status"] == "FINITE_CLOSEOUT_JUDGMENT_FAILED"
    assert result["judgment"] is None
    assert result["error"]
    assert "review_accounting" in result
    assert len(calls) == 1
    assert json.loads((output / "result.json").read_text()) == result


def test_missing_review_evidence_remains_details_required_without_retry(tmp_path, monkeypatch):
    run, _ = saved_correction_run(tmp_path, "accepted")
    value = judgment.collect(run.root)
    calls = []

    def job(output, **kwargs):
        calls.append(output)
        response = controlled_response(value)
        response["check_results"]["contrast"] = {
            "outcome": "details_required", "source_refs": [],
            "evidence": "The commissioned check needs evidence outside the supplied selection."}
        attempt = output / "provider/attempts/controlled"
        attempt.mkdir(parents=True)
        (attempt / "response.json").write_text(json.dumps(response), encoding="utf-8")
        return {"attempt_dir": str(attempt)}

    monkeypatch.setattr(judgment, "launch", job)
    result = judgment.judge(run.root, None, tmp_path / "review", model="controlled", reasoning_effort="high", timeout_seconds=30)
    assert result["status"] == "FINITE_CLOSEOUT_DETAILS_REQUIRED"
    assert result["judgment"]["check_results"]["contrast"]["outcome"] == "details_required"
    assert len(calls) == 1


def test_protected_output_and_changed_binding_refused_before_job(tmp_path, monkeypatch):
    run, _ = saved_correction_run(tmp_path, "accepted")
    monkeypatch.setattr(judgment, "launch", lambda *a, **kw: pytest.fail("must fail before launch"))
    with pytest.raises(ValueError, match="outside saved"):
        judgment.judge(run.root, None, run.root / "review", model="controlled", reasoning_effort="high", timeout_seconds=30)
    assert not (run.root / "review").exists()
    path = run.root / "coverage.json"
    path.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="saved coverage differs"):
        judgment.judge(run.root, None, tmp_path / "review", model="controlled", reasoning_effort="high", timeout_seconds=30)
    assert not (tmp_path / "review").exists()


def test_existing_launcher_is_no_tools_no_retry_and_keeps_logs(tmp_path, monkeypatch):
    calls = []

    def subprocess_run(command, **kwargs):
        calls.append(command)
        assert kwargs["cwd"] == judgment.WORKTREE / "forseti-harness"
        kwargs["stdout"].write("retained provider output")
        output = Path(command[command.index("--result-out") + 1])
        output.parent.mkdir(parents=True)
        output.write_text(json.dumps({"status": "PROCESS_COMPLETED_NOT_VALIDATED", "attempt_dir": "fixture"}))
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(judgment.subprocess, "run", subprocess_run)
    assert judgment.launch(tmp_path, model="controlled", reasoning_effort="high", timeout_seconds=30)["attempt_dir"] == "fixture"
    command, = calls
    assert command[command.index("--max-retries") + 1] == "0"
    assert command[command.index("--run-retry-limit") + 1] == "0"
    assert [command[i + 1] for i, arg in enumerate(command) if arg == "--preload-context"] == [
        str(judgment.WORKTREE / p) for p in judgment.CONTEXT_FILES]
    assert (tmp_path / "provider.stdout.log").read_text() == "retained provider output"


@pytest.mark.parametrize("budget", [1024, 32768])
@pytest.mark.parametrize("coverage", ["complete", "unknown"])
def test_oversized_failure_diagnostic_keeps_the_record_locator_and_paid_usage(tmp_path, monkeypatch, capsys, budget, coverage):
    """Controlled counters and diagnostics test the return, not fresh model cost."""
    run, _ = saved_correction_run(tmp_path, "accepted")
    detail = "invalid \U0001f9f4 schema and instance \u6e90 " * 6000
    accounting = {"usage": {"coverage": coverage,
        "total_tokens": 199367 if coverage == "complete" else None,
        "observed_totals": {"total_tokens": 199367}, "issues": ["diagnostic " * 4000]},
        "additional_observed_response_tokens": 11117,
        "unknown_usage_attempts": 0 if coverage == "complete" else 1,
        "startup_observation_unknown_attempts": 0 if coverage == "complete" else 1}

    def job(output, **kwargs):
        raise ValueError(detail)

    monkeypatch.setattr(judgment, "launch", job)
    monkeypatch.setattr(judgment, "collect_provider_roots", lambda roots: accounting)
    output = tmp_path / "review"
    capsys.readouterr()  # Drop the runner's own progress lines from the fixture.
    assert judgment.main(["--run-root", str(run.root), "--output-dir", str(output),
        "--model", "controlled", "--reasoning-effort", "high", "--timeout-seconds", "30",
        "--max-output-bytes", str(budget)]) == 1
    console = capsys.readouterr().out
    assert len(console.encode("utf-8")) <= budget
    printed = json.loads(console)
    assert printed["return_view"] == "details_required"
    assert printed["record_path"] == str((output / "result.json").resolve())
    assert printed["facts"]["status"] == "FINITE_CLOSEOUT_JUDGMENT_FAILED"
    usage = printed["facts"]["review_usage"]
    assert usage == {"coverage": coverage, "completed_turn_tokens": accounting["usage"]["total_tokens"],
        "observed_completed_turn_tokens": 199367, "observed_startup_tokens": 11117,
        "unknown_usage_attempts": accounting["unknown_usage_attempts"],
        "unknown_startup_attempts": accounting["startup_observation_unknown_attempts"]}
    assert printed["facts"]["error"] == "Full failure diagnostic in record_path."
    # The bounded console fact never replaces the complete saved diagnostic.
    saved = json.loads((output / "result.json").read_text(encoding="utf-8"))
    assert saved["error"] == detail
    assert saved["review_accounting"] == accounting


def test_collector_index_failure_stays_an_explicit_failure_return(tmp_path, monkeypatch, capsys):
    """A saved operation command truncated after a flag raises IndexError."""
    run, _ = saved_correction_run(tmp_path, "accepted")
    operation = tmp_path / "operation"
    operation.mkdir()
    (operation / "operation.json").write_text(json.dumps({"command": ["--output-dir"]}), encoding="utf-8")
    monkeypatch.setattr(judgment, "launch", lambda *a, **kw: pytest.fail("must fail before launch"))
    capsys.readouterr()
    assert judgment.main(["--run-root", str(run.root), "--operation-dir", str(operation),
        "--output-dir", str(tmp_path / "review"),
        "--model", "controlled", "--reasoning-effort", "high", "--timeout-seconds", "30"]) == 1
    assert json.loads(capsys.readouterr().out) == {
        "status": "FINITE_CLOSEOUT_JUDGMENT_FAILED", "error": "list index out of range"}
    assert not (tmp_path / "review").exists()


def test_existing_runner_routes_to_judgment_without_restarting_consolidation(monkeypatch):
    monkeypatch.setattr(judgment, "main", lambda argv: 17 if argv == ["--help"] else 18)
    monkeypatch.setattr(finite, "FiniteRun", lambda *a: pytest.fail("restarted consolidation"))
    assert finite.main(["judge-closeout", "--help"]) == 17
