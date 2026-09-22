"""Offline execution-boundary and unchanged-work reuse tests; no model calls."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from harness_utils import hash_file
from judgment import semantic_evidence_integration as semantic
from judgment import extracted_evidence_selection as selection
from provider_jobs import run_provider_job
from runners import run_semantic_evidence_integration as native
from runners import semantic_execution as execution
from runners.run_codex_provider_attempt import preloaded_context, DIRECT_JUDGMENT_INSTRUCTION
from test_semantic_evidence_integration import (
    _source_v10, _keyed_responses, _claim_row, _row_verification_responses, _keyed_row_review_response)


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False) + "\n", encoding="utf-8")


@pytest.fixture
def corpus(tmp_path):
    source = _source_v10(count=6)
    source["semantic_method_version"] = semantic.METHOD_VERSION_V13
    source = semantic.materialize_source_v3(source)
    bundle = semantic.build_bundle(source, max_prompt_bytes=80000, max_evidence_per_work_unit=2)
    responses = _keyed_responses(bundle)
    for response in responses:
        eid = next(iter(response["decisions_by_evidence_id"]))
        row = _claim_row(eid)
        row.pop("evidence_id")
        row["semantic_units"][0]["subject_product_ids"] = ["summer-fridays-lip-butter-balm"]
        response["decisions_by_evidence_id"][eid] = row
    paths = {name: tmp_path / "original" / (name + ".json") for name in ("source", "bundle")}
    write(paths["source"], source)
    write(paths["bundle"], bundle)
    paths["responses"] = []
    for response in responses:
        path = tmp_path / "original" / (response["batch_id"] + ".json")
        write(path, response)
        paths["responses"].append(path)
    return source, bundle, responses, paths


def selected_start(corpus, tmp_path):
    _, _, _, paths = corpus
    out = tmp_path / "selection"
    result = selection.prepare(source_path=paths["source"], bundle_path=paths["bundle"],
        response_paths=paths["responses"][:1], output_dir=out)
    return result, dict(source_path=out / "source.json", bundle_path=out / "bundle.json",
        extracted_selection_path=out / "selection.json", run_dir=tmp_path / "continued")


def test_selected_completed_batch_enters_verification_without_new_extraction(corpus, tmp_path):
    source, bundle, responses, paths = corpus
    originals = {p: p.read_bytes() for p in [paths["source"], paths["bundle"], *paths["responses"]]}
    result, kwargs = selected_start(corpus, tmp_path)
    assert result["status"] == "EXTRACTED_SELECTION_REQUIRES_VERIFICATION"
    assert result["selected_row_count"] == len(bundle["batches"][0]["evidence_ids"])
    assert result["excluded_row_count"] == len(source["captured_items"]) - result["selected_row_count"]
    state = native.advance_semantic_run(**kwargs)
    assert state["status"] == "SEMANTIC_JUDGMENT_REQUIRED", state.get("error")
    assert state["phase"] == "verification"
    assert state["judgment_requests"] and all(r["phase"] == "verification" for r in state["judgment_requests"])
    assert all("worker_prompt" not in r and r["execution"]["transport"] == "direct_provider_v1" for r in state["judgment_requests"])
    compilation = native._load_object(kwargs["run_dir"] / "extraction/compilation.json")
    assert "row_verification_manifest" not in compilation
    original = semantic.validate_batch_responses(bundle, responses)
    def meanings(c):
        return {r["evidence_id"]: semantic._proposed_result_from_compilation(c, r) for r in c["evidence_dispositions"]}
    selected_ids = set(bundle["batches"][0]["evidence_ids"])
    assert meanings(compilation) == {k: v for k, v in meanings(original).items() if k in selected_ids}
    stage = native._load_object(kwargs["run_dir"] / "verification/stage.json")
    verification = {r["batch_id"]: _keyed_row_review_response(r) for r in _row_verification_responses(stage)}
    for request in state["judgment_requests"]:
        raw = tmp_path / (request["batch_id"] + ".json")
        write(raw, verification[request["batch_id"]])
        native.submit_judgment_job(job_path=Path(request["job_path"]), expected_sha256=request["job_sha256"], response_path=raw)
    next_state = native.advance_semantic_run(**kwargs)
    assert next_state["phase"] == "reconciliation", next_state.get("error")
    assert all(r["phase"] == "reconciliation" for r in next_state["judgment_requests"])
    assert {p: p.read_bytes() for p in originals} == originals
    assert native.advance_semantic_run(**kwargs)["judgment_requests"] == next_state["judgment_requests"]


@pytest.mark.parametrize("changed", ["source", "response", "derived", "selection"])
def test_selection_tampering_blocks_before_new_judgments(corpus, tmp_path, changed):
    _, kwargs = selected_start(corpus, tmp_path)
    paths = corpus[-1]
    if changed == "source":
        path = paths["source"]
    elif changed == "response":
        path = paths["responses"][0]
    elif changed == "derived":
        path = next((kwargs["source_path"].parent / "responses").glob("*.json"))
    else:
        path = kwargs["extracted_selection_path"]
    value = native._load_object(path)
    value["injected_mutation"] = "must not be accepted even with a fresh outer hash"
    if changed == "selection":
        value.pop("selection_sha256")
        value["selection_sha256"] = semantic._sha256(value)
    write(path, value)
    state = native.advance_semantic_run(**kwargs)
    assert state["status"] == "SEMANTIC_ADVANCE_BLOCKED" and not state["judgment_requests"]
    assert any(word in state["error"] for word in ("changed", "differs")), state["error"]
    assert not kwargs["run_dir"].exists()


def simulated_provider(monkeypatch, tmp_path, responses, calls, *, before_launch=None):
    """Use the real job state machine with an explicitly simulated model boundary."""
    codex = tmp_path / "simulated-codex"
    codex.write_text("offline simulation", encoding="utf-8")
    def invoke(command, **kwargs):
        assert "run_codex_provider_job.py" in command[1]
        assert "--direct-judgment" in command
        def arg(name):
            return command[command.index(name) + 1]
        contexts = [Path(command[i+1]) for i, x in enumerate(command[:-1]) if x == "--preload-context"]
        context, context_files = preloaded_context(contexts)
        prompt, schema = Path(arg("--prompt-file")), Path(arg("--output-schema"))
        binding = {"prompt_path": str(prompt), "prompt_sha256": hash_file(prompt),
            "schema_path": str(schema), "schema_sha256": hash_file(schema),
            "codex_executable": str(codex), "codex_sha256": hash_file(codex),
            "runner_path": command[1], "runner_sha256": hash_file(Path(command[1])),
            "model": arg("--model"), "reasoning_effort": arg("--reasoning-effort"),
            "worktree": arg("--worktree"), "direct_judgment": True}
        if context:
            binding.update(preloaded_context_sha256=hashlib.sha256(context.encode()).hexdigest(), preloaded_context_files=context_files)
        def launch(aid):
            if before_launch is not None:
                before_launch()
            calls.append({"prompt": prompt.read_bytes(), "schema": native._load_object(schema), "command": command})
            attempt = Path(arg("--attempt-root")) / aid
            attempt.mkdir(parents=True)
            write(attempt / "response.json", responses.pop(0))
            (attempt / "events.jsonl").write_text('{"type":"turn.completed"}\n', encoding="utf-8")
            (attempt / "stderr.log").write_text("", encoding="utf-8")
            from runners.run_codex_provider_attempt import DIRECT_JUDGMENT_CONFIG, DIRECT_JUDGMENT_DISABLED_FEATURES
            launch_command = [str(codex), "exec", "--model", binding["model"], "-C", binding["worktree"],
                *[part for feature in DIRECT_JUDGMENT_DISABLED_FEATURES for part in ("--disable", feature)],
                *[part for value in DIRECT_JUDGMENT_CONFIG for part in ("--config", value)],
                "--config", f'model_reasoning_effort="{binding["reasoning_effort"]}"',
                "--config", "developer_instructions=" + json.dumps(context or DIRECT_JUDGMENT_INSTRUCTION)]
            metadata = {"authentication_observed": "chatgpt", "direct_judgment": True}
            if context:
                metadata["preloaded_context_sha256"] = binding["preloaded_context_sha256"]
            receipt = {"outcome": "PROCESS_COMPLETED", "command": launch_command,
                "prompt_sha256": binding["prompt_sha256"], "response_schema_sha256": binding["schema_sha256"],
                "response_sha256": hash_file(attempt / "response.json"),
                "events_sha256": hash_file(attempt / "events.jsonl"), "stderr_sha256": hash_file(attempt / "stderr.log"),
                "launch_metadata": metadata, "usage": None}
            write(attempt / "execution_receipt.json", receipt)
        result = run_provider_job(job_dir=Path(arg("--job-dir")), attempt_root=Path(arg("--attempt-root")),
            binding=binding, launch=launch, retry_budget_dir=Path(arg("--retry-budget-dir")),
            run_retry_limit=int(arg("--run-retry-limit")), max_retries=int(arg("--max-retries")))
        write(Path(arg("--result-out")), result)
        return SimpleNamespace(returncode=0)
    monkeypatch.setattr(execution.subprocess, "run", invoke)
    return invoke


def test_direct_adapter_delivers_exact_input_and_restart_never_generates_again(corpus, tmp_path, monkeypatch):
    _, _, responses, paths = corpus
    state = native.advance_semantic_run(source_path=paths["source"], run_dir=tmp_path / "run",
        max_prompt_bytes=80000, max_evidence_per_work_unit=2)
    request = state["judgment_requests"][0]
    calls = []
    simulated_provider(monkeypatch, tmp_path, [responses[0]], calls)
    kwargs = dict(job_path=Path(request["job_path"]), job_sha256=request["job_sha256"], provider_root=tmp_path / "provider",
        model="offline-model", reasoning_effort="high", timeout_seconds=60)
    result = execution.execute_judgment_job(**kwargs)
    assert result["status"] == "SEMANTIC_JUDGMENT_SUBMITTED"
    assert len(calls) == 1
    assert calls[0]["prompt"] == Path(request["prompt_path"]).read_bytes()
    assert calls[0]["schema"] == native._load_object(Path(request["response_schema_path"]))
    assert execution.execute_judgment_job(**kwargs)["disposition"] == "reused"
    assert len(calls) == 1


def test_normal_execute_stops_at_explicit_bound_then_resumes_without_reextraction(corpus, tmp_path, monkeypatch):
    _, _, responses, paths = corpus
    calls = []
    simulated_provider(monkeypatch, tmp_path, deepcopy(responses), calls)
    kwargs = dict(advance_kwargs=dict(source_path=paths["source"], run_dir=tmp_path / "run",
        max_prompt_bytes=80000, max_evidence_per_work_unit=2), model="offline-model", reasoning_effort="high",
        timeout_seconds=60, max_jobs=1)
    first = execution.execute_semantic_run(**kwargs)
    assert first["status"] == "SEMANTIC_EXECUTION_LIMIT_REACHED", first.get("error")
    assert len(calls) == 1 and first["executed_job_count"] == 1
    assert "model_api_calls" not in first
    second = execution.execute_semantic_run(**kwargs)
    assert second["status"] == "SEMANTIC_EXECUTION_LIMIT_REACHED" and len(calls) == 2
    assert calls[0]["prompt"] != calls[1]["prompt"]


def test_invalid_answer_stops_with_preserved_failure_and_no_semantic_retry(corpus, tmp_path, monkeypatch):
    _, _, responses, paths = corpus
    bad = deepcopy(responses[0])
    bad["batch_id"] = "foreign-batch"
    calls = []
    simulated_provider(monkeypatch, tmp_path, [bad], calls)
    kwargs = dict(advance_kwargs=dict(source_path=paths["source"], run_dir=tmp_path / "run",
        max_prompt_bytes=80000, max_evidence_per_work_unit=2), model="offline-model", reasoning_effort="high",
        timeout_seconds=60, max_jobs=2)
    result = execution.execute_semantic_run(**kwargs)
    assert result["status"] == "SEMANTIC_EXECUTION_BLOCKED" and "batch identity" in result["error"]
    assert len(calls) == 1 and result["executed_job_count"] == 1  # a rejected answer still ran
    assert list((tmp_path / "run/extraction/responses").glob("*.tmp"))
    again = execution.execute_semantic_run(**kwargs)
    assert again["status"] == "SEMANTIC_ADVANCE_BLOCKED" and len(calls) == 1


def test_missing_execution_bound_fails_before_preparation_or_provider(tmp_path):
    with pytest.raises(ValueError, match="max-jobs"):
        execution.execute_semantic_run(advance_kwargs={"run_dir": tmp_path / "run"}, model="test",
            reasoning_effort="high", timeout_seconds=60, max_jobs=None)
    assert not (tmp_path / "run").exists()


def test_completion_before_submission_recovers_without_another_generation(corpus, tmp_path, monkeypatch):
    _, _, responses, paths = corpus
    state = native.advance_semantic_run(source_path=paths["source"], run_dir=tmp_path / "run",
        max_prompt_bytes=80000, max_evidence_per_work_unit=2)
    request = state["judgment_requests"][0]
    calls = []
    invoke = simulated_provider(monkeypatch, tmp_path, [responses[0]], calls)
    def interrupted(command, **kwargs):
        invoke(command, **kwargs)
        # Simulate interruption after the durable attempt but before delivery of
        # its result to the outer runner. Only this test's temporary file changes.
        Path(command[command.index("--result-out") + 1]).unlink()
        raise OSError("simulated interrupted observer")
    monkeypatch.setattr(execution.subprocess, "run", interrupted)
    kwargs = dict(job_path=Path(request["job_path"]), job_sha256=request["job_sha256"], provider_root=tmp_path / "provider",
        model="offline-model", reasoning_effort="high", timeout_seconds=60)
    with pytest.raises(OSError, match="interrupted observer"):
        execution.execute_judgment_job(**kwargs)
    monkeypatch.setattr(execution.subprocess, "run", invoke)
    assert execution.execute_judgment_job(**kwargs)["status"] == "SEMANTIC_JUDGMENT_SUBMITTED"
    assert len(calls) == 1


def test_complete_case_uses_same_direct_adapter_and_existing_consumer_validation(tmp_path, monkeypatch):
    from judgment import complete_case_consumer as consumer
    from runners import finite_preparation
    from test_complete_case_consumer import fixture, respond, count
    args = fixture()
    state = consumer.advance(*args, tmp_path / "consumer", context="", count=count)
    request = state["judgment_requests"][0]
    job = consumer.read(request["job_path"])
    monkeypatch.setattr(finite_preparation, "offline_tokenizer",
        lambda encoding: (SimpleNamespace(encode=lambda text, **kw: list(text.encode("utf-8"))), {}))
    calls = []
    simulated_provider(monkeypatch, tmp_path, [respond(job)], calls)
    kwargs = dict(job_path=Path(request["job_path"]), job_sha256=request["job_sha256"], provider_root=tmp_path / "provider",
        model="offline-model", reasoning_effort="high", timeout_seconds=60)
    result = execution.execute_judgment_job(**kwargs)
    assert result["status"] == "CONSUMER_RESPONSE_ACCEPTED"
    assert calls[0]["prompt"].decode() == job["prompt"]
    assert "--preload-context" not in calls[0]["command"]  # already in the measured consumer prompt
    assert "model_api_calls" not in result
    assert execution.execute_judgment_job(**kwargs)["status"] == "CONSUMER_RESPONSE_ACCEPTED"
    assert len(calls) == 1


def test_cli_execution_returns_compact_bound_result(corpus, tmp_path, monkeypatch, capsys):
    _, _, responses, paths = corpus
    calls = []
    simulated_provider(monkeypatch, tmp_path, [responses[0]], calls)
    assert native.main(["advance", "--source", str(paths["source"]), "--run-dir", str(tmp_path / "run"),
        "--max-prompt-bytes", "80000", "--max-evidence-per-work-unit", "2", "--execute",
        "--model", "offline-model", "--reasoning-effort", "high", "--timeout-seconds", "60", "--max-jobs", "1"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "SEMANTIC_EXECUTION_LIMIT_REACHED" and result["pending_job_count"] == len(responses) - 1
    assert "judgment_requests" not in result and "worker_prompt" not in result
    assert len(calls) == 1


@pytest.mark.parametrize("event, after_turn, accepted", [
    ({"type": "item.completed", "item": {"type": "error", "message":
      "Code Mode is unavailable because code-mode host is disabled. Code mode will fail closed; "
      "enable `features.code_mode_host` and install `codex-code-mode-host`."}}, False, True),
    ({"type": "item.completed", "item": {"type": "error", "message":
      "Code Mode is unavailable because code-mode host is disabled. Code mode will fail closed; "
      "enable `features.code_mode_host` and install `codex-code-mode-host`."}}, True, False),
    ({"type": "item.completed", "item": {"type": "error", "message":
      "Codex is ignoring 1 unrecognized configuration setting. Check for typos or deprecated settings.\n"
      "  session-flags: `tools.view_image` is ignored."}}, False, False),
    ({"type": "item.completed", "item": {"type": "error", "message": "unexpected provider failure"}}, False, False),
    ({"type": "item.completed", "item": {"type": "command_execution"}}, True, False),
    ({"type": "item.completed", "item": {"type": "mcp_tool_call"}}, True, False),
    ({"type": "turn.failed", "error": {"message": "generation failed"}}, True, False),
    ({"type": "error", "message": "generation failed"}, False, False),
])
def test_startup_notice_and_failures_at_role_boundary(corpus, tmp_path, monkeypatch, event, after_turn, accepted):
    _, _, responses, paths = corpus
    request = native.advance_semantic_run(source_path=paths["source"], run_dir=tmp_path / "run",
        max_prompt_bytes=80000, max_evidence_per_work_unit=2)["judgment_requests"][0]
    calls = []
    invoke = simulated_provider(monkeypatch, tmp_path, [responses[0]], calls)
    def escaped(command, **kwargs):
        result = invoke(command, **kwargs)
        path = Path(command[command.index("--result-out") + 1])
        saved = native._load_object(path)
        attempt = Path(saved["attempt_dir"])
        events = [{"type": "thread.started", "thread_id": "offline"}]
        if after_turn:
            events.append({"type": "turn.started"})
        events.append(event)
        if not after_turn:
            events.append({"type": "turn.started"})
        events.append({"type": "turn.completed"})
        (attempt / "events.jsonl").write_text("\n".join(json.dumps(row) for row in events) + "\n", encoding="utf-8")
        saved["execution_receipt"]["events_sha256"] = hash_file(attempt / "events.jsonl")
        write(attempt / "execution_receipt.json", saved["execution_receipt"])
        write(path, saved)
        return result
    monkeypatch.setattr(execution.subprocess, "run", escaped)
    kwargs = dict(job_path=Path(request["job_path"]), job_sha256=request["job_sha256"],
        provider_root=tmp_path / "provider", model="offline-model", reasoning_effort="high", timeout_seconds=60)
    if accepted:
        assert execution.execute_judgment_job(**kwargs)["status"] == "SEMANTIC_JUDGMENT_SUBMITTED"
        assert native._load_object(Path(request["response_path"])) == responses[0]
        assert execution.execute_judgment_job(**kwargs)["disposition"] == "reused"
    else:
        with pytest.raises(ValueError, match="direct judgment"):
            execution.execute_judgment_job(**kwargs)
        assert not Path(request["response_path"]).exists()
    assert len(calls) == 1


def test_job_count_reports_provider_attempts_not_reuse(corpus, tmp_path, monkeypatch):
    _, _, responses, paths = corpus
    calls = []
    invoke = simulated_provider(monkeypatch, tmp_path, [responses[0]], calls)
    def interrupted(command, **kwargs):
        invoke(command, **kwargs)
        Path(command[command.index("--result-out") + 1]).unlink()
        raise OSError("simulated interrupted observer")
    monkeypatch.setattr(execution.subprocess, "run", interrupted)
    kwargs = dict(advance_kwargs=dict(source_path=paths["source"], run_dir=tmp_path / "run",
        max_prompt_bytes=80000, max_evidence_per_work_unit=2), model="offline-model", reasoning_effort="high",
        timeout_seconds=60, max_jobs=1)
    blocked = execution.execute_semantic_run(**kwargs)
    assert blocked["status"] == "SEMANTIC_EXECUTION_BLOCKED" and len(calls) == 1
    assert blocked["executed_job_count"] == 1
    monkeypatch.setattr(execution.subprocess, "run", invoke)
    resumed = execution.execute_semantic_run(**kwargs)
    assert resumed["status"] == "SEMANTIC_EXECUTION_LIMIT_REACHED" and len(calls) == 1
    assert resumed["executed_job_count"] == 0  # submitting the saved attempt launched nothing


def test_cli_blocked_resume_names_preserved_artifacts(corpus, tmp_path, monkeypatch, capsys):
    _, _, responses, paths = corpus
    bad = deepcopy(responses[0])
    bad["batch_id"] = "foreign-batch"
    calls = []
    simulated_provider(monkeypatch, tmp_path, [bad], calls)
    argv = ["advance", "--source", str(paths["source"]), "--run-dir", str(tmp_path / "run"),
        "--max-prompt-bytes", "80000", "--max-evidence-per-work-unit", "2", "--execute",
        "--model", "offline-model", "--reasoning-effort", "high", "--timeout-seconds", "60", "--max-jobs", "2"]
    assert native.main(argv) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "SEMANTIC_EXECUTION_BLOCKED"
    assert native.main(argv) == 2
    again = json.loads(capsys.readouterr().out)
    staged = next((tmp_path / "run/extraction/responses").glob("*.tmp"))
    assert again["status"] == "SEMANTIC_ADVANCE_BLOCKED" and len(calls) == 1
    assert [Path(row["path"]).resolve() for row in again["problems"]] == [staged.resolve()]


def test_launch_intent_without_attempt_is_counted_as_unknown_not_free(corpus, tmp_path, monkeypatch):
    _, _, responses, paths = corpus
    calls = []
    def interrupted():
        raise OSError("observer interrupted before attempt reservation")
    simulated_provider(monkeypatch, tmp_path, [responses[0]], calls, before_launch=interrupted)
    kwargs = dict(advance_kwargs=dict(source_path=paths["source"], run_dir=tmp_path / "run",
        max_prompt_bytes=80000, max_evidence_per_work_unit=2), model="offline-model", reasoning_effort="high",
        timeout_seconds=60, max_jobs=1)
    blocked = execution.execute_semantic_run(**kwargs)
    assert blocked["status"] == "SEMANTIC_EXECUTION_BLOCKED"
    assert blocked["executed_job_count"] == 1 and not calls
    assert list((tmp_path / "run/provider").glob("*/job/launch-001.json"))
    assert not list((tmp_path / "run/provider").glob("*/attempts/job-attempt-001"))
    again = execution.execute_semantic_run(**kwargs)
    assert again["status"] == "SEMANTIC_EXECUTION_BLOCKED" and "execution is unconfirmed" in again["error"]
    assert again["executed_job_count"] == 0 and not calls


@pytest.mark.parametrize("mutation", ["missing_feature", "enabled_feature", "missing_context_cap", "duplicate_context_cap", "feature_config", "tools_config"])
def test_saved_direct_attempt_cannot_weaken_launch_restrictions(corpus, tmp_path, monkeypatch, mutation):
    _, _, responses, paths = corpus
    request = native.advance_semantic_run(source_path=paths["source"], run_dir=tmp_path / "run",
        max_prompt_bytes=80000, max_evidence_per_work_unit=2)["judgment_requests"][0]
    calls = []
    invoke = simulated_provider(monkeypatch, tmp_path, [responses[0]], calls)
    def weakened(command, **kwargs):
        result = invoke(command, **kwargs)
        path = Path(command[command.index("--result-out") + 1])
        saved = native._load_object(path)
        launch_command = saved["execution_receipt"]["command"]
        if mutation in {"missing_feature", "missing_context_cap"}:
            value = "multi_agent" if mutation == "missing_feature" else "project_doc_max_bytes=0"
            index = launch_command.index(value)
            del launch_command[index-1:index+1]
        elif mutation == "enabled_feature":
            launch_command += ["--enable", "multi_agent"]
        else:
            setting = {"duplicate_context_cap": "project_doc_max_bytes=32000",
                       "feature_config": "features.multi_agent=true",
                       "tools_config": "tools={view_image=true}"}[mutation]
            launch_command += ["--config", setting]
        write(Path(saved["attempt_dir"]) / "execution_receipt.json", saved["execution_receipt"])
        write(path, saved)
        return result
    monkeypatch.setattr(execution.subprocess, "run", weakened)
    with pytest.raises(ValueError, match="direct judgment restriction changed"):
        execution.execute_judgment_job(job_path=Path(request["job_path"]), job_sha256=request["job_sha256"],
            provider_root=tmp_path / "provider", model="offline-model", reasoning_effort="high", timeout_seconds=60)
    assert len(calls) == 1 and not Path(request["response_path"]).exists()
