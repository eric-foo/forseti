"""Real subprocess identity, observer interruption and conservative closeout."""
from argparse import Namespace
import json
from pathlib import Path
import subprocess
import sys
import threading
import time

import pytest

import command_execution
from command_execution import launch, observe, resume, worker
from provider_jobs import _lock
from reports.efficiency_codex import collect_provider_roots


def reserve(monkeypatch, args):
    """Reserve one operation without spawning its real detached worker."""
    monkeypatch.setattr(command_execution.subprocess, "Popen", lambda *a, **k: Namespace(poll=lambda: 0))
    reserved = launch(args)
    monkeypatch.undo()
    return reserved


def options(tmp_path, body, checker=None):
    script = tmp_path / "command.py"
    script.write_text(body, encoding="utf-8")
    check_path = tmp_path / "checker.json"
    if checker:
        check_path.write_text(json.dumps([sys.executable, "-c", checker]), encoding="utf-8")
    return Namespace(command=[sys.executable, str(script)], cwd=str(tmp_path),
                     operation_dir=str(tmp_path / "operation"), bind_codex=False, quality_command=str(check_path) if checker else None,
                     timeout_seconds=None, validation_timeout_seconds=None, provider_root=[], stdin_file=None)


def test_real_interrupted_observer_resume_launches_exactly_once(tmp_path):
    args = options(tmp_path, "from pathlib import Path\nimport time\nPath('launch-count').open('x').write('one')\ntime.sleep(2)\nPath('answer').write_text('done')",
                   "from pathlib import Path; assert Path('answer').read_text() == 'done'; Path('validation-count').open('x').write('one')")
    first = launch(args)
    assert first["status"] == "running"
    observer = subprocess.Popen(first["resume_argv"], cwd=first["resume_cwd"], stdout=subprocess.PIPE)
    time.sleep(.2)
    observer.terminate()
    observer.wait(timeout=5)
    assert observe(Path(args.operation_dir))["operation_id"] == first["operation_id"]
    result = resume(args.operation_dir, 15)
    assert result["status"] == "completed"
    assert result["required_validation"]["status"] == "passed"
    assert result["operation_id"] == first["operation_id"]
    before = {p.name: p.read_bytes() for p in Path(args.operation_dir).iterdir() if p.suffix == ".json"}
    assert resume(args.operation_dir) == result
    with pytest.raises(FileExistsError):
        launch(args)
    with pytest.raises(FileExistsError):
        worker(args.operation_dir)
    assert before == {p.name: p.read_bytes() for p in Path(args.operation_dir).iterdir() if p.suffix == ".json"}
    assert (tmp_path / "launch-count").read_text() == (tmp_path / "validation-count").read_text() == "one"


@pytest.mark.parametrize("command,checker,status,validation", [
    ("import sys; print('before failure', flush=True); print('failure detail', file=sys.stderr, flush=True); raise SystemExit(7)",
     "raise SystemExit(0)", "failed", "not_run_execution_failed"),
    ("pass", "raise SystemExit(9)", "failed", "failed"),
    ("pass", None, "completed", "not_requested"),
])
def test_real_failure_and_absent_checker_are_not_acceptance(tmp_path, command, checker, status, validation):
    args = options(tmp_path, command, checker)
    launch(args)
    result = resume(args.operation_dir, 15)
    assert result["status"] == status
    assert result["required_validation"]["status"] == validation
    if validation == "not_run_execution_failed":
        assert result["execution"]["exit_code"] == 7
        assert Path(result["execution"]["stdout_path"]).read_text() == "before failure\n"
        assert Path(result["execution"]["stderr_path"]).read_text() == "failure detail\n"
    if validation == "failed":
        assert result["required_validation"]["exit_code"] == 9


def test_brief_observer_lock_hold_never_kills_the_worker(tmp_path, monkeypatch):
    args = options(tmp_path, "from pathlib import Path\nPath('ran').open('x').write('one')")
    assert reserve(monkeypatch, args)["status"] == "unknown"
    directory = Path(args.operation_dir)
    holding, release = threading.Event(), threading.Event()

    def hold():
        with _lock(directory / "worker.lock"):
            holding.set()
            release.wait(10)

    holder = threading.Thread(target=hold)
    holder.start()
    assert holding.wait(5)
    ran = threading.Thread(target=lambda: worker(directory))
    ran.start()
    time.sleep(.3)
    # Observation holds the same lock; it must delay the worker, never end it.
    assert not (directory / "closeout.json").exists()
    release.set()
    holder.join(10)
    ran.join(30)
    assert not ran.is_alive()
    assert observe(directory)["status"] == "completed"
    assert (tmp_path / "ran").read_text() == "one"


def test_peer_observation_does_not_report_a_dead_operation_as_running(tmp_path):
    directory = tmp_path / "dead"
    directory.mkdir()
    (directory / "operation.json").write_text(json.dumps({"operation_id": "dead"}))
    holding = threading.Event()

    def hold():
        with _lock(directory / "worker.lock"):
            holding.set()
            time.sleep(.05)

    holder = threading.Thread(target=hold)
    holder.start()
    assert holding.wait(5)
    assert observe(directory)["status"] == "unknown"
    holder.join(5)


def test_supplied_checker_is_never_closed_out_as_not_requested(tmp_path, monkeypatch):
    args = options(tmp_path, "pass", "raise SystemExit(0)")
    stdin_file = tmp_path / "stdin.txt"
    stdin_file.write_text("bound", encoding="utf-8")
    args.stdin_file = str(stdin_file)
    reserve(monkeypatch, args)
    stdin_file.write_text("changed", encoding="utf-8")
    worker(Path(args.operation_dir))
    result = observe(Path(args.operation_dir))
    assert result["status"] == "failed"
    assert result["required_validation"]["status"] == "not_run_execution_failed"
    assert any(i.startswith("execution_or_validation_incomplete") for i in result["issues"])
    # The compact closeout drops per-attempt rows but keeps the accounting scope split.
    assert result["accounting"]["usage_by_execution_scope"] == {}
    assert not (Path(args.operation_dir) / "command.stdout").exists()


def test_unknown_worker_never_relaunches(tmp_path):
    directory = tmp_path / "unknown"
    directory.mkdir()
    (directory / "operation.json").write_text(json.dumps({"operation_id": "original"}))
    result = resume(directory)
    assert result["status"] == "unknown"
    assert not (directory / "worker.json").exists()


def test_incomplete_observation_returns_carry_resume_recovery(tmp_path):
    """A caller that lost its observer recovers from the return alone, never by relaunching."""
    args = options(tmp_path, "import time; time.sleep(2)")
    running = launch(args)
    unknown = tmp_path / "unknown"
    unknown.mkdir()
    (unknown / "operation.json").write_text(json.dumps({"operation_id": "original"}))
    for result, state, directory in ((running, "running", Path(args.operation_dir)),
                                     (observe(unknown), "unknown", unknown)):
        assert result["status"] == state
        assert result["resume_argv"] == [sys.executable, "-m", "runners.run_efficiency", "resume",
                                         "--operation-dir", str(directory.resolve())]
        assert Path(result["resume_cwd"]) == Path(command_execution.__file__).resolve().parent
        assert "never start again" in result["wait_contract"]
    assert resume(args.operation_dir, 15)["status"] == "completed"


def test_real_deadline_preserves_timeout(tmp_path):
    args = options(tmp_path, "import time; time.sleep(10)")
    args.timeout_seconds = .1
    launch(args)
    result = resume(args.operation_dir, 15)
    assert result["status"] == "failed"
    assert result["execution"]["status"] == "timeout"
    assert "explicit_deadline_reached" in result["issues"]


def test_missing_receipt_and_launch_intent_are_unknown_usage(tmp_path):
    job = tmp_path / "job"
    job.mkdir()
    (job / "binding.json").write_text(json.dumps({"attempt_root": str(tmp_path / "attempts")}))
    (job / "launch-001.json").write_text(json.dumps({"attempt_id": "missing"}))
    result = collect_provider_roots([tmp_path])
    assert result["attempt_count"] == result["unknown_usage_attempts"] == 1
    assert result["usage"]["total_tokens"] is None
    assert "native_receipt_missing_invalid_or_changed" in result["issues"]


def test_changed_native_receipt_diagnostics_fail_closed(tmp_path):
    (tmp_path / "execution_receipt.json").write_text(json.dumps({
        "schema_version": "forseti_provider_execution_receipt_v1", "events_sha256": "wrong"}))
    (tmp_path / "events.jsonl").write_text('')
    result = collect_provider_roots([tmp_path])
    assert result["unknown_usage_attempts"] == 1
    assert result["usage"]["total_tokens"] is None


def test_native_accounting_subsets_startup_and_repeated_roots(tmp_path):
    from harness_utils import hash_file
    events = tmp_path / "events.jsonl"
    usage = {"input_tokens": 100, "cached_input_tokens": 40, "output_tokens": 20,
             "reasoning_output_tokens": 10}
    events.write_text("\n".join(json.dumps(e) for e in [
        {"type": "thread.started", "thread_id": "one"}, {"type": "turn.started"},
        {"type": "turn.completed", "usage": usage}]), encoding="utf-8")
    log = tmp_path / "stderr.log"
    log.write_text('INFO codex_otel.trace_safe: event.kind=response.completed input_token_count=7 output_token_count=0\n'
                   'INFO codex_otel.trace_safe: event.kind=response.completed input_token_count=100 output_token_count=20\n', encoding="utf-8")
    receipt = {"schema_version": "forseti_provider_execution_receipt_v1", "usage": usage,
               "events_sha256": hash_file(events), "stderr_sha256": hash_file(log),
               "outcome": "PROCESS_COMPLETED", "started_at": "2026-01-01T00:00:00Z", "observed_retry_events": 0}
    path = tmp_path / "execution_receipt.json"
    path.write_text(json.dumps(receipt), encoding="utf-8")
    result = collect_provider_roots([tmp_path, tmp_path], started_at="2026-02-01T00:00:00Z")
    assert result["attempt_count"] == 1
    assert result["usage"]["total_tokens"] == 120
    assert result["additional_observed_response_tokens"] == 7
    assert result["attempts"][0]["execution_scope"] == "preserved_prior_execution"
    assert result["usage_by_execution_scope"] == {"preserved_prior_execution": {
        "attempts": 1, "coverage": "complete", "total_tokens": 120, "observed_total_tokens": 120,
        "additional_observed_response_tokens": 7, "startup_observation_unknown_attempts": 0}}
    current = tmp_path / "current"
    current.mkdir()
    for source in (events, log):
        (current / source.name).write_bytes(source.read_bytes())
    (current / path.name).write_text(json.dumps({**receipt, "started_at": "2026-03-01T00:00:00Z"}), encoding="utf-8")
    mixed = collect_provider_roots([tmp_path, current], started_at="2026-02-01T00:00:00Z")
    assert mixed["attempt_count"] == 2
    assert mixed["usage"]["total_tokens"] == 240
    assert mixed["additional_observed_response_tokens"] == 14
    scopes = mixed["usage_by_execution_scope"]
    assert scopes["current_operation_interval"] == scopes["preserved_prior_execution"]
    assert scopes["current_operation_interval"]["total_tokens"] == 120
    # Perturb an already-admitted receipt, preserving valid diagnostic hashes.
    receipt["usage"]["input_tokens"] = 101
    path.write_text(json.dumps(receipt), encoding="utf-8")
    result = collect_provider_roots([tmp_path], started_at="2026-02-01T00:00:00Z")
    assert result["unknown_usage_attempts"] == 1
    assert result["usage"]["total_tokens"] is None
    scopes = result["usage_by_execution_scope"]
    assert scopes["preserved_prior_execution"]["total_tokens"] is None
    assert scopes["preserved_prior_execution"]["startup_observation_unknown_attempts"] == 1
    assert scopes["current_operation_interval"]["total_tokens"] == 120
    assert scopes["current_operation_interval"]["additional_observed_response_tokens"] == 7
    assert scopes["current_operation_interval"]["startup_observation_unknown_attempts"] == 0
