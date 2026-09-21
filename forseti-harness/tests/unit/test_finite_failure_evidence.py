"""Failure reporting preserves frozen evidence and never earns endpoint acceptance."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from harness_utils import hash_file
from reports import finite_closeout, finite_closeout_judgment as judgment
from reports.finite_failure_evidence import collect_failure
from runners import finite_run_report
from test_finite_closeout import saved_correction_run
from test_finite_closeout_judgment import controlled_response


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def failed_run(base):
    root = base / "run"
    inputs = {name: write(base / "inputs" / (name + ".json"), value) for name, value in {
        "source": {}, "bundle": {}, "verified": {}, "questions": {"questions": [], "worker_instructions": "scope"},
        "previous_answer": {"status": "unavailable"}}.items()}
    runtime = base / "runtime.py"
    runtime.write_text('def validate():\n    raise ValueError("unrelated precise fixture defect")\n', encoding="utf-8")
    write(root / "binding.json", {"inputs": {name: {"path": str(p), "sha256": hash_file(p)} for name, p in inputs.items()},
        "runtime": {str(runtime): hash_file(runtime)}, "replay_from": None})
    write(root / "coverage.json", {"attached_statements": 2, "residual_statements": 3,
        "missing_statements": 0, "packet_truncated": False})
    evidence = {str(p): hash_file(p) for p in root.rglob("*") if p.is_file()}
    failure = write(root / "failure-001.json", {"status": "FINITE_EXECUTION_FAILED_OR_UNKNOWN",
        "error_type": "ValueError", "error": "unrelated precise fixture defect", "evidence_files": evidence})
    return root, failure, inputs


def snapshot(base, destination):
    files = {}
    for source in base.rglob("*"):
        if source.is_file():
            relative = source.relative_to(base)
            copy = destination / relative
            copy.parent.mkdir(parents=True, exist_ok=True)
            copy.write_bytes(source.read_bytes())
            files[str(relative)] = {"sha256": hash_file(source), "original": str(source)}
    return write(destination / "manifest.json", {"files": files})


def test_snapshot_never_follows_later_live_endpoint_and_preserves_generic_guard(tmp_path):
    root, failure, inputs = failed_run(tmp_path / "original")
    manifest = snapshot(root.parent, tmp_path / "snapshot")
    write(root / "result.json", {"status": "later_recovery"})
    write(inputs["questions"], {"changed": "later live data must never enter the snapshot"})
    value = collect_failure(tmp_path / "snapshot/run", tmp_path / "snapshot/run/failure-001.json", snapshot_manifest=manifest)
    assert value["saved_result"]["error"] == "unrelated precise fixture defect"
    assert value["original_failure_guard_functions"][0]["function"] == "validate"
    assert value["input_scope"]["questions"]["worker_instructions"] == "scope"
    assert not value["execution_facts"]["endpoint_artifacts"]["result.json"]
    assert all(Path(p).is_relative_to(manifest.parent) for p in value["read_artifact_hashes"])
    with pytest.raises(ValueError, match="later endpoint"):
        collect_failure(root, failure)


@pytest.mark.parametrize("fault", ["changed_input", "missing_input", "changed_runtime", "changed_snapshot", "extra_snapshot"])
def test_missing_and_changed_sources_fail_before_reporting(tmp_path, monkeypatch, fault):
    root, failure, inputs = failed_run(tmp_path / "original")
    manifest = None
    if "snapshot" in fault:
        manifest = snapshot(root.parent, tmp_path / "snapshot")
        root, failure = manifest.parent / "run", manifest.parent / "run/failure-001.json"
        write(manifest.parent / ("extra.json" if fault == "extra_snapshot" else "inputs/questions.json"), {})
    elif fault == "missing_input":
        inputs["questions"].unlink()
    else:
        (inputs["questions"] if fault == "changed_input" else root.parent / "runtime.py").write_text("changed", encoding="utf-8")
    monkeypatch.setattr(judgment, "launch", lambda *a, **k: pytest.fail("wrong boundary: paid launch"))
    with pytest.raises((ValueError, OSError)):
        judgment.judge(root, None, tmp_path / "report", model="controlled", reasoning_effort="high", timeout_seconds=30,
            failure_record=failure, snapshot_manifest=manifest)
    assert not (tmp_path / "report").exists()


@pytest.mark.parametrize("details", [[], [{"missing_fact": "unknown guard cause", "source_locator": "runtime.py", "why_material": "cannot establish cause"}]])
def test_one_failure_judgment_rendered_with_counts_and_failure_even_if_prose_omits_them(tmp_path, monkeypatch, details):
    root, failure, _ = failed_run(tmp_path / "original")
    calls = []

    def launch(output, **kwargs):
        calls.append(output)
        response = write(output / "provider/attempts/test/response.json", {"report_markdown": "Concise explanation.", "details_required": details})
        assert "not a fresh semantic assessment" in (output / "prompt.md").read_text(encoding="utf-8")
        return {"attempt_dir": str(response.parent)}

    monkeypatch.setattr(judgment, "launch", launch)
    output = tmp_path / "report"
    report = judgment.judge(root, None, output, model="controlled", reasoning_effort="high", timeout_seconds=30, failure_record=failure)
    assert report["saved_status"] == "FINITE_EXECUTION_FAILED_OR_UNKNOWN"
    assert report["saved_failure"]["error"] == "unrelated precise fixture defect"
    assert report["status"] == ("FINITE_CLOSEOUT_DETAILS_REQUIRED" if details else "FINITE_CLOSEOUT_JUDGMENT_COMPLETE_REQUIRES_ADJUDICATION")
    text = (output / "report.md").read_text(encoding="utf-8")
    assert '"attached_statements": 2' in text and '"residual_statements": 3' in text
    assert '"packet_truncated": false' in text and '"total_including_startup": null' in text
    assert "unrelated precise fixture defect" in text
    prompt = (output / "prompt.md").read_text(encoding="utf-8")
    frozen = json.loads(failure.read_text())["evidence_files"]
    assert frozen and not any(digest in prompt for digest in frozen.values())
    assert '"frozen_failure_inventory_file_count":%d' % len(frozen) in prompt
    with pytest.raises(FileExistsError):
        judgment.judge(root, None, output, model="controlled", reasoning_effort="high", timeout_seconds=30, failure_record=failure)
    assert len(calls) == 1


def test_new_failure_inventory_rejects_changed_existing_record_and_later_work(tmp_path):
    root, failure, _ = failed_run(tmp_path / "original")
    before = (root / "coverage.json").read_bytes()
    write(root / "coverage.json", {"attached_statements": 999})
    with pytest.raises(ValueError, match="saved binding changed"):
        collect_failure(root, failure)
    (root / "coverage.json").write_bytes(before)
    write(root / "assessment-recheck/result.json", {"later": "partial work"})
    with pytest.raises(ValueError, match="interval inventory changed"):
        collect_failure(root, failure)


def test_legacy_failure_without_inventory_stays_details_required(tmp_path, monkeypatch):
    root, failure, _ = failed_run(tmp_path / "original")
    value = json.loads(failure.read_text())
    del value["evidence_files"]
    write(failure, value)

    def launch(output, **kwargs):
        path = write(output / "provider/attempts/test/response.json", {"report_markdown": "Omitted the evidence gap.", "details_required": []})
        return {"attempt_dir": str(path.parent)}

    monkeypatch.setattr(judgment, "launch", launch)
    report = judgment.judge(root, None, tmp_path / "report", model="controlled", reasoning_effort="high", timeout_seconds=30, failure_record=failure)
    assert report["status"] == "FINITE_CLOSEOUT_DETAILS_REQUIRED"
    assert report["evidence_gaps"][0]["missing_fact"] == "immutable inventory at the selected failure"


def test_failure_entry_freezes_inventory_and_original_error(tmp_path, monkeypatch):
    from runners import run_finite_semantic_consolidation as finite
    root, _, _ = failed_run(tmp_path / "original")

    class Failed:
        def __init__(self, args):
            pass

        def run(self):
            raise ValueError("original command error")

    monkeypatch.setattr(finite, "FiniteRun", Failed)
    assert finite.execute(SimpleNamespace(output_dir=root, provider_root=None)) == 1
    record = json.loads(sorted(root.glob("failure-*.json"))[-1].read_text())
    assert record["error"] == "original command error"
    assert record["evidence_files"][str(root / "coverage.json")] == hash_file(root / "coverage.json")


def test_completed_reader_accepts_composed_operation_without_mixing_reporting_costs(tmp_path):
    from reports.efficiency_codex import collect_provider_roots
    run, _ = saved_correction_run(tmp_path, "rejected")
    binding = json.loads((run.root / "binding.json").read_text())
    command = ["python", "-m", "runners.run_finite_semantic_consolidation", "run-and-report", "--report-dir", str(tmp_path / "report"), "--"]
    for name, record in binding["inputs"].items():
        command += ["--" + name.replace("_", "-"), record["path"]]
    command += ["--output-dir", str(run.root)]
    operation = tmp_path / "operation"
    reporting = tmp_path / "report/judgment/provider"
    reporting.mkdir(parents=True)
    roots = [str(run.root), str(reporting)]
    started = "2000-01-01T00:00:00Z"
    accounting = collect_provider_roots(roots, started_at=started)
    write(operation / "operation.json", {"operation_id": "test", "command": command, "provider_roots": roots, "created_at": started})
    write(operation / "accounting.json", accounting)
    write(operation / "closeout.json", {"operation_id": "test", "accounting": {k: v for k, v in accounting.items() if k != "attempts"}})
    value = finite_closeout.collect(run.root, operation)
    assert value["saved_result"]["answer_correction_status"] == "rejected"
    assert value["native_accounting"] == collect_provider_roots([str(run.root)], started_at=started)


@pytest.mark.parametrize("outcome", ["accepted", "rejected", "failed", "report_failed"])
def test_maintained_run_report_executes_once_and_preserves_underlying_failure(tmp_path, monkeypatch, outcome):
    if outcome in {"failed", "report_failed"}:
        root, failure, inputs = failed_run(tmp_path / "original")
        exit_code = 7
        terminal = {"status": "FINITE_EXECUTION_FAILED_OR_UNKNOWN", "failure": str(failure)}
    else:
        run, _ = saved_correction_run(tmp_path, outcome)
        root = run.root
        inputs = {k: Path(v["path"]) for k, v in json.loads((root / "binding.json").read_text())["inputs"].items()}
        exit_code = 0
        terminal = {"status": "FINITE_EXECUTION_COMPLETE_QUALITY_REQUIRES_ADJUDICATION", "result": str(root / "result.json")}
    execution_calls, report_calls = [], []

    def execute(command, **kwargs):
        execution_calls.append(command)
        kwargs["stdout"].write((json.dumps(terminal) + "\n").encode())
        return SimpleNamespace(returncode=exit_code)

    def launch(output, **kwargs):
        report_calls.append(output)
        assert kwargs["codex_executable"] == tmp_path / "explicit-native.exe"
        if outcome == "report_failed":
            raise ValueError("report transport failed")
        response = {"report_markdown": "Failure stays failed.", "details_required": []} if exit_code else controlled_response(finite_closeout.collect(root))
        path = write(output / "provider/attempts/test/response.json", response)
        return {"attempt_dir": str(path.parent)}

    monkeypatch.setattr(finite_run_report.subprocess, "run", execute)
    monkeypatch.setattr(judgment, "launch", launch)
    output = tmp_path / "report"
    argv = ["--report-dir", str(output), "--model", "controlled", "--reasoning-effort", "high", "--timeout-seconds", "30", "--"]
    for name, path in inputs.items():
        argv += ["--" + name.replace("_", "-"), str(path)]
    argv += ["--output-dir", str(root), "--codex-executable", str(tmp_path / "explicit-native.exe")]
    assert finite_run_report.main(argv) == exit_code
    result = json.loads((output / "result.json").read_text())
    assert result["execution_exit_code"] == exit_code
    if outcome == "rejected":
        assert result["saved_answer_correction_status"] == "rejected"
    if exit_code:
        assert result["status"] == "FINITE_RUN_REPORT_FAILED_OR_UNKNOWN"
    if outcome == "report_failed":
        assert result["reporting_status"] == "FINITE_CLOSEOUT_JUDGMENT_FAILED"
    assert finite_run_report.main(argv) == 1
    assert len(execution_calls) == len(report_calls) == 1
