"""Native acceptance, frozen replay and explicit provider-boundary failures."""
from argparse import Namespace
from copy import deepcopy
from pathlib import Path
import json
import sys

import pytest

from runners import run_finite_semantic_consolidation as finite
from runners import run_codex_provider_job as job_runner
from test_semantic_evidence_integration import _missing_definition_fixture, _local_repair_fixture


@pytest.fixture
def installed_codex(tmp_path, monkeypatch):
    monkeypatch.setenv("APPDATA", str(tmp_path))
    monkeypatch.setattr(finite.sys, "platform", "win32")
    monkeypatch.setattr(finite.platform, "machine", lambda: "AMD64")
    modules = tmp_path / "npm/node_modules"
    package = modules / "@openai/codex"
    native = package / "node_modules/@openai/codex-win32-x64"
    executable = native / "vendor/x86_64-pc-windows-msvc/bin/codex.exe"
    calls = []
    def install(version):
        package.mkdir(parents=True, exist_ok=True)
        native.mkdir(parents=True, exist_ok=True)
        (package / "package.json").write_text(json.dumps({"name": "@openai/codex", "version": version,
            "bin": {"codex": "bin/codex.js"}, "optionalDependencies": {
                "@openai/codex-win32-x64": f"npm:@openai/codex@{version}-win32-x64"}}))
        (native / "package.json").write_text(json.dumps({"name": "@openai/codex", "version": version + "-win32-x64",
            "os": ["win32"], "cpu": ["x64"]}))
        executable.parent.mkdir(parents=True, exist_ok=True)
        executable.write_text(version)
    def local(exe, args, env):
        calls.append((exe, args))
        return Namespace(returncode=0, stdout="codex-cli " + Path(exe).read_text(), stderr="")
    install("1.0.0")
    monkeypatch.setattr(finite, "_local_codex_check", local)
    return Namespace(install=install, executable=executable, native=native, modules=modules, calls=calls)


def test_installation_update_is_selected_at_actual_finite_job_launch(tmp_path, monkeypatch, installed_codex):
    run = object.__new__(finite.FiniteRun)
    run.root = run.provider_root = tmp_path / "run"
    run.replay = None
    run.args = Namespace(codex_executable=None)
    installed_codex.install("1.1.0")  # Update after runner construction, before first paid job.
    commands = []
    def job(command, **kwargs):
        commands.append(command)
        response_dir = run.root / "job/attempts/job-attempt-001"
        finite.persist(response_dir / "response.json", {})
        result = Path(command[command.index("--result-out") + 1])
        finite.persist(result, {"status": "PROCESS_COMPLETED_NOT_VALIDATED", "attempt_dir": str(response_dir)})
        return Namespace(returncode=0)
    monkeypatch.setattr(finite.subprocess, "run", job)
    run.job("job", "prompt", {"type": "object"})
    selected = finite.read(run.root / "codex-selection.json")
    assert selected["version"] == "codex-cli 1.1.0"
    assert selected["sha256"] == finite.hash_file(installed_codex.executable)
    assert commands[0][commands[0].index("--codex-executable") + 1] == selected["path"]
    assert installed_codex.calls == [(selected["path"], ["--version"])]
    assert run.bind_executable() == selected
    installed_codex.install("1.2.0")
    with pytest.raises(ValueError, match="bound Codex executable changed"):
        run.job("other-job", "prompt", {"type": "object"})
    assert len(commands) == 1


@pytest.mark.parametrize("case", ["missing", "ambiguous", "foreign", "version", "arbitrary"])
def test_unverified_installation_fails_before_native_or_paid_work(installed_codex, case):
    package = installed_codex.native / "package.json"
    if case == "missing":
        package.unlink()
    elif case == "ambiguous":
        other = installed_codex.modules / "@openai/codex-win32-x64/package.json"
        other.parent.mkdir(parents=True)
        other.write_bytes(package.read_bytes())
    elif case in {"foreign", "version"}:
        value = json.loads(package.read_text())
        value["name" if case == "foreign" else "version"] = "wrong"
        package.write_text(json.dumps(value))
    else:
        installed_codex.executable.write_text("not-codex")
    with pytest.raises(ValueError):
        finite.select_codex_executable()
    assert len(installed_codex.calls) == (1 if case == "arbitrary" else 0)


def test_explicit_override_is_verified_and_never_falls_back(tmp_path, installed_codex):
    override = tmp_path / "explicit.exe"
    override.write_text("2.0.0")
    selected = finite.select_codex_executable(override)
    assert selected["path"] == str(override.resolve())
    assert selected["selection"] == "explicit_native_override"
    assert selected["version"] == "codex-cli 2.0.0"
    with pytest.raises(ValueError, match="existing absolute native"):
        finite.select_codex_executable(tmp_path / "missing.exe")
    assert len(installed_codex.calls) == 1


def test_run_selection_cannot_be_rebound_or_removed(tmp_path, installed_codex):
    run = object.__new__(finite.FiniteRun)
    run.root = run.provider_root = tmp_path / "run"
    run.args = Namespace(codex_executable=None)
    selected = run.bind_executable()
    finite.persist(run.root / "binding.json", {"codex_selection": selected})
    run.args.codex_executable = tmp_path / "another.exe"
    with pytest.raises(ValueError, match="explicit Codex selection differs"):
        run.bind_executable()
    run.args.codex_executable = None
    (run.root / "codex-selection.json").unlink()
    with pytest.raises(ValueError, match="no Codex selection"):
        run.bind_executable()


def bare_run(tmp_path, bundle, stage):
    run = object.__new__(finite.FiniteRun)
    run.root = tmp_path / "run"
    run.provider_root = run.root
    run.bundle = bundle
    run.args = Namespace(bundle=tmp_path / "bundle.json", local_repair_successor=[])
    run.consumed_repairs = set()
    finite.persist(run.args.bundle, bundle)
    finite.persist(run.root / "formation/stage.json", stage)
    return run


def test_native_definition_recovery_preserves_original_and_reuses_successor(tmp_path):
    bundle, stage, original, failed, request, patch = _missing_definition_fixture()
    run = bare_run(tmp_path, bundle, stage)
    response, patch_path = tmp_path / "original-response.json", tmp_path / "patch.json"
    finite.persist(response, failed)
    finite.persist(patch_path, patch)
    before = response.read_bytes()
    with pytest.raises(finite.semantic.MissingReconciliationDefinitions):
        finite.native.validate_one_reconciliation_response(bundle, stage, failed)
    run.job = lambda *args, **kwargs: patch_path  # Saved fixture, zero model calls.
    successor = run.validate_or_repair("formation", stage, response, 0)
    restored = finite.read(successor)
    assert restored["decisions_by_candidate_ref"] == original["decisions_by_candidate_ref"]
    assert {n["semantic_node_key"]: n for n in restored["semantic_nodes"]} == {
        n["semantic_node_key"]: n for n in original["semantic_nodes"]}
    assert run.validate_or_repair("formation", stage, response, 0) == successor
    assert response.read_bytes() == before
    assert len(list((run.root / "repair-budget").glob("*.json"))) == 1
    assert finite.read(successor.parent / "receipt.json")["unchanged_existing_decisions_and_definitions"]


def test_missing_candidate_fails_native_boundary_without_paid_repair(tmp_path):
    bundle, stage, _, failed, _, _ = _missing_definition_fixture()
    del failed["decisions_by_candidate_ref"][next(iter(failed["decisions_by_candidate_ref"]))]
    run = bare_run(tmp_path, bundle, stage)
    response = tmp_path / "missing-candidate.json"
    finite.persist(response, failed)
    run.job = lambda *a, **k: pytest.fail("incomplete evidence must not launch a repair")
    with pytest.raises(finite.semantic.SemanticIntegrationError):
        run.validate_or_repair("formation", stage, response, 0)
    assert not (run.root / "formation/accepted/0000.json").exists()
    failure = next((run.root / "formation/repair").glob("*/failure.json"))
    assert "candidate" in finite.read(failure)["error"]


def test_repair_budget_fails_after_native_missing_definition_guard(tmp_path):
    bundle, stage, _, failed, _, _ = _missing_definition_fixture()
    run = bare_run(tmp_path, bundle, stage)
    response = tmp_path / "failed.json"
    finite.persist(response, failed)
    for i in range(4):
        finite.persist(run.root / "repair-budget" / f"prior-{i}.json", {"retained": True})
    run.job = lambda *a, **k: pytest.fail("exhausted budget must not launch")
    with pytest.raises(ValueError, match="repair budget exhausted"):
        run.validate_or_repair("formation", stage, response, 0)
    assert len(list((run.root / "repair-budget").glob("*.json"))) == 4


def test_explicit_native_local_successor_resumes_without_generation(tmp_path):
    bundle, stage, failed, _, patch = _local_repair_fixture()
    failed["semantic_nodes"].append(deepcopy(failed["semantic_nodes"][0]))
    run = bare_run(tmp_path, bundle, stage)
    original = tmp_path / "original.json"
    finite.persist(original, failed)
    request = finite.semantic.prepare_reconciliation_repair(bundle, stage, failed,
        node_keys=["affected"], reason="Explicit fixture nomination of duplicate definition")
    patch["request_sha256"] = request["request_sha256"]
    request_path, patch_path, successor = tmp_path / "request.json", tmp_path / "patch.json", tmp_path / "successor"
    finite.persist(request_path, {"request": request, "input_sha256": {
        "bundle": finite.hash_file(run.args.bundle), "stage": finite.hash_file(run.root / "formation/stage.json"),
        "failed_response": finite.hash_file(original)}})
    finite.persist(patch_path, patch)
    finite.native.submit_reconciliation_local_repair(bundle_path=run.args.bundle,
        stage_path=run.root / "formation/stage.json", failed_response_path=original,
        request_path=request_path, patch_path=patch_path, output_dir=successor)
    key = f"formation:{stage['batches'][0]['batch_id']}"
    run.args.local_repair_successor = [[key, str(request_path), str(patch_path), str(successor)]]
    run.job = lambda *a, **k: pytest.fail("accepted successor must not repeat a paid job")
    assert run.validate_or_repair("formation", stage, original, 0) == successor / "response.json"
    assert run.validate_or_repair("formation", stage, original, 0) == successor / "response.json"
    assert run.consumed_repairs == {key}
    before = original.read_bytes()
    (successor / "response.json").write_bytes(b"{}")
    with pytest.raises(ValueError, match="existing successor differs"):
        run.validate_or_repair("formation", stage, original, 0)
    assert original.read_bytes() == before


def test_coverage_is_input_derived_and_rejects_missing_or_overlapping_statement():
    bundle = {"evidence_units": [{"evidence_id": "one"}, {"evidence_id": "two"}]}
    verified = {"semantic_units": [{"semantic_unit_ref": "a"}, {"semantic_unit_ref": "b"}]}
    view = {"coverage": {"accounted_item_count": 2},
        "propositions": [{"semantic_relations": {"support": ["a"]}}],
        "unmerged_semantic_units": [{"semantic_unit_ref": "b"}]}
    packet = {"selection_coverage": {"truncated": False, "selected_proposition_count": 1,
                                     "corpus_unmerged_semantic_unit_count": 1}}
    assert finite.coverage(bundle, verified, view, packet)["verified_statements"] == 2
    for mutation in ([], [{"semantic_unit_ref": "a"}], [{"semantic_unit_ref": "unknown"}]):
        changed = {**view, "unmerged_semantic_units": mutation}
        with pytest.raises(ValueError, match="partition verified statements"):
            finite.coverage(bundle, verified, changed, packet)
    with pytest.raises(ValueError, match="packet coverage differs"):
        finite.coverage(bundle, verified, view, {"selection_coverage": {**packet["selection_coverage"], "truncated": True}})


def test_answer_schema_order_and_citations_are_native_input_bound():
    questions = [{"id": "a"}, {"id": "b"}]
    bundle = {"evidence_units": [{"evidence_id": "e"}]}
    verified = {"semantic_units": [{"semantic_unit_ref": "e::u"}]}
    answer = {"schema_version": "finite_answer_v1", "answers": [
        {"question_id": q["id"], "answer": "bounded", "evidence_refs": ["e::u"], "limits": "sample"} for q in questions]}
    finite.check_answer(answer, questions, bundle, verified)
    duplicate = deepcopy(answer)
    duplicate["answers"][1]["question_id"] = "a"
    with pytest.raises(ValueError, match="identities/order differ"):
        finite.check_answer(duplicate, questions, bundle, verified)
    answer["answers"][0]["evidence_refs"] = ["unknown"]
    with pytest.raises(ValueError, match="unknown evidence"):
        finite.check_answer(answer, questions, bundle, verified)


def test_assessment_allows_extra_checks_but_not_missing_frozen_checks():
    questions = {"assessment_only": {"checks": [{"id": "one"}, {"id": "two"}]}}
    result = {"schema_version": "finite_source_assessment_v1", "inventory_coverage": "fixture",
              "comparison": "fixture", "unassessed_material": "fixture", "overall_usefulness": "fixture",
              "material_findings": [], "check_results": [
                  {"check_id": x, "status": "pass", "source_refs": [], "finding_refs": [], "explanation": "fixture"}
                  for x in ("one", "two", "additional_inventory")]}
    finite.check_assessment(result, questions)
    result["check_results"].pop(0)
    with pytest.raises(ValueError, match="omits or duplicates"):
        finite.check_assessment(result, questions)


def test_provider_result_file_is_separate_from_attempt_stdout_and_no_replace(tmp_path, monkeypatch, capsys):
    for name in ("prompt", "schema", "codex"):
        (tmp_path / name).write_text("{}", encoding="utf-8")
    output = tmp_path / "result.json"
    argv = ["job", "--job-dir", str(tmp_path / "job"), "--attempt-root", str(tmp_path / "attempts"),
        "--retry-budget-dir", str(tmp_path / "budget"), "--run-retry-limit", "2", "--prompt-file", str(tmp_path / "prompt"),
        "--output-schema", str(tmp_path / "schema"), "--worktree", str(tmp_path), "--codex-executable", str(tmp_path / "codex"),
        "--model", "fixture", "--reasoning-effort", "high", "--timeout-seconds", "1", "--result-out", str(output)]
    result = {"status": "PROCESS_COMPLETED_NOT_VALIDATED", "simulated": True}
    calls = []
    def simulated_job(**kwargs):
        calls.append(kwargs)
        print('{"attempt_receipt":"separate"}')
        return result
    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setattr(job_runner, "run_provider_job", simulated_job)
    assert job_runner.main() == 0
    assert finite.read(output) == result
    assert "attempt_receipt" in capsys.readouterr().out
    with pytest.raises(SystemExit):
        job_runner.main()
    assert len(calls) == 1


def test_finite_provider_failure_stops_before_response_consumption(tmp_path, monkeypatch):
    run = object.__new__(finite.FiniteRun)
    run.root, run.replay = tmp_path, None
    run.provider_root = run.root
    run.args = Namespace(codex_executable=tmp_path / "codex")
    run.bind_executable = lambda: {"path": str(run.args.codex_executable)}
    def failed(command, **kwargs):
        kwargs["stderr"].write(b"provider launch outcome unknown\n")
        return Namespace(returncode=1)
    monkeypatch.setattr(finite.subprocess, "run", failed)
    with pytest.raises(ValueError, match="failed or unknown"):
        run.job("formation/provider/batch", "fixture", {"type": "object"})
    assert finite.read(tmp_path / "formation/provider/batch/invoke-001.json")["exit_code"] == 1
    assert not (tmp_path / "result.json").exists()


def answer_fixture(tmp_path):
    run = object.__new__(finite.FiniteRun)
    run.root, run.provider_root, run.replay = tmp_path / "successor", tmp_path / "original", None
    run.questions = {"questions": [{"id": "one"}, {"id": "two"}]}
    run.bundle = {"evidence_units": [{"evidence_id": "known"}]}
    run.verified = {"semantic_units": []}
    answer = {"schema_version": "finite_answer_v1", "answers": [
        {"question_id": q["id"], "answer": "bounded", "evidence_refs": ["known"], "limits": "sample"}
        for q in run.questions["questions"]]}
    return run, answer


def test_no_correction_final_answer_is_consumable_answer_object(tmp_path):
    run, answer = answer_fixture(tmp_path)
    response = run.provider_root / "answer/response.json"
    finite.persist(response, answer)
    finite.persist(run.root / "answer/freeze.json", {"response": str(response), "response_sha256": finite.hash_file(response)})
    result = run.correct_and_recheck(answer, {"material_findings": []}, {})
    finite.check_answer(finite.read(result["final_answer"]), run.questions["questions"], run.bundle, run.verified)
    assert result["answer_corrections"] == 0


def test_unknown_citation_correction_preserves_original_unaffected_and_shared_allowance(tmp_path):
    run, original = answer_fixture(tmp_path)
    original["answers"][0]["evidence_refs"] = ["invented"]
    response = run.provider_root / "answer/response.json"
    finite.persist(response, original)
    before = response.read_bytes()
    with pytest.raises(finite.UnknownAnswerEvidence):
        finite.check_answer(original, run.questions["questions"], run.bundle, run.verified)
    patch = {"schema_version": "finite_answer_v1", "answers": [
        {**original["answers"][0], "evidence_refs": ["known"]}]}
    patch_path = run.provider_root / "answer-correction/response.json"
    finite.persist(patch_path, patch)
    run.job = lambda *a, **k: patch_path
    corrected = finite.read(run.correct_invalid_answer(response, {"questions": run.questions["questions"]}))
    assert corrected["answers"][1] == original["answers"][1]
    assert response.read_bytes() == before
    assert finite.read(run.provider_root / "answer-correction/allowance.json")["kind"] == "pre_freeze_unknown_evidence"
    # A different successor cannot obtain a second correction by changing its output root.
    run.root = tmp_path / "another-successor"
    run.job = lambda *a, **k: pytest.fail("shared allowance must reject a second correction before launch")
    assessment = {"material_findings": [{"status": "open", "introduced_at": "current_answer",
        "artifact_refs": ["current_answer:one"]}]}
    with pytest.raises(ValueError, match="existing finite output differs"):
        run.correct_and_recheck(corrected, assessment, {})


def test_other_answer_failures_do_not_enter_unknown_citation_recovery(tmp_path):
    run, answer = answer_fixture(tmp_path)
    answer["answers"].reverse()
    with pytest.raises(ValueError, match="identities/order differ") as failure:
        finite.check_answer(answer, run.questions["questions"], run.bundle, run.verified)
    assert not isinstance(failure.value, finite.UnknownAnswerEvidence)
    assert not (run.provider_root / "answer-correction/allowance.json").exists()


def test_post_assessment_correction_rechecks_affected_scope_and_reports_recheck_findings(tmp_path):
    run, answer = answer_fixture(tmp_path)
    run.source = {"captured_items": [{"evidence_id": "known"}]}
    run.questions["assessment_only"] = {"checks": [{"id": "anchored", "source_rows": ["known"]}]}
    assessment = {"material_findings": [{"status": "open", "introduced_at": "current_answer",
        "artifact_refs": ["current_answer:one"], "source_refs": ["known"]}]}
    patch = {"schema_version": "finite_answer_v1", "answers": [{**answer["answers"][0], "answer": "corrected"}]}
    new_defect = {"severity": "minor", "introduced_at": "current_answer", "status": "open", "source_refs": ["known"],
        "artifact_refs": ["current_answer:one"], "defect": "fixture", "effect": "fixture", "bounded_repair": "fixture"}
    recheck = {"schema_version": "finite_source_assessment_v1", "inventory_coverage": "fixture", "comparison": "fixture",
        "unassessed_material": "fixture", "overall_usefulness": "fixture", "material_findings": [new_defect],
        "check_results": [{"check_id": "anchored", "status": "pass", "source_refs": ["known"], "finding_refs": [],
                           "explanation": "fixture"}]}
    responses = {"answer-correction/provider": run.provider_root / "patch.json",
                 "assessment-recheck/provider": run.provider_root / "recheck.json"}
    finite.persist(responses["answer-correction/provider"], patch)
    finite.persist(responses["assessment-recheck/provider"], recheck)
    launched = []
    run.job = lambda name, *a, **k: launched.append(name) or responses[name]
    result = run.correct_and_recheck(answer, assessment, {"propositions": []})
    corrected = finite.read(result["final_answer"])
    assert corrected["answers"] == [patch["answers"][0], answer["answers"][1]]
    assert launched == ["answer-correction/provider", "assessment-recheck/provider"]
    assert (result["answer_corrections"], result["affected_rechecks"]) == (1, 1)
    assert result["affected_recheck_material_findings"] == [new_defect]
    assert finite.read(run.root / "assessment-recheck/input.json")["frozen_relevant_checks"] == run.questions["assessment_only"]["checks"]
    assert finite.read(run.provider_root / "answer-correction/allowance.json")["kind"] == "post_assessment"


def test_unused_local_repair_successor_fails_before_paid_consumers(tmp_path, monkeypatch):
    run, _ = answer_fixture(tmp_path)
    run.provider_root, run.source, run.consumed_repairs = run.root, {}, set()
    run.bundle["schema_version"] = "fixture"
    args = {"provider_root": None, "codex_executable": Path(sys.executable),
            "local_repair_successor": [["formation:unmatched", "request", "patch", "successor"]]}
    for name in ("source", "bundle", "verified", "questions", "previous_answer"):
        args[name] = tmp_path / (name + ".json")
        finite.persist(args[name], {})
    run.args = Namespace(**args)
    run.bind_executable = lambda: {"path": str(args["codex_executable"])}
    monkeypatch.setattr(finite.semantic, "build_bundle", lambda *a, **k: run.bundle)
    run.phase = lambda name, compilation: {}
    run.consumers = lambda *a: pytest.fail("stale repair binding must stop before answer and assessment jobs")
    with pytest.raises(ValueError, match="unused local-repair successor"):
        run.run()
    assert not (run.root / "result.json").exists()


@pytest.mark.parametrize("mutation", ["inputs", "policy", "missing", "locked", "chained"])
def test_provider_root_binding_and_ownership_fail_before_consumers(tmp_path, mutation):
    run, _ = answer_fixture(tmp_path)
    inputs = {}
    args = {"provider_root": run.provider_root, "codex_executable": Path(sys.executable)}
    for name in ("source", "bundle", "verified", "questions", "previous_answer"):
        path = tmp_path / (name + ".json")
        finite.persist(path, {})
        args[name] = path
        inputs[name] = {"path": str(path.resolve()), "sha256": finite.hash_file(path)}
    run.args = Namespace(**args)
    run.phase = lambda *a: pytest.fail("unbound or concurrent origin must not reach consumers")
    origin = {"inputs": inputs, "policy": finite.POLICY, "replay_from": None}
    if mutation == "inputs":
        origin["inputs"] = {}
    elif mutation == "policy":
        origin["policy"] = {}
    elif mutation == "chained":
        # A successor root has matching inputs/policy but owns no provider jobs or budgets.
        origin["provider_root"] = {"path": str(tmp_path / "earlier"), "binding_sha256": "0" * 64}
    if mutation != "missing":
        finite.persist(run.provider_root / "binding.json", origin)
    if mutation == "locked":
        with finite._lock(run.provider_root / "run.lock"):
            with pytest.raises(ValueError, match="already in use"):
                run.run()
    else:
        with pytest.raises((ValueError, FileNotFoundError)):
            run.run()
    assert not (run.root / "binding.json").exists()


def test_successor_repair_budget_uses_original_root(tmp_path):
    bundle, stage, _, failed, _, _ = _missing_definition_fixture()
    run = bare_run(tmp_path, bundle, stage)
    run.provider_root = tmp_path / "original"
    for index in range(4):
        finite.persist(run.provider_root / "repair-budget" / f"prior-{index}.json", {"retained": True})
    response = tmp_path / "failed.json"
    finite.persist(response, failed)
    run.job = lambda *a, **k: pytest.fail("successor must not reset repair calls")
    with pytest.raises(ValueError, match="repair budget exhausted"):
        run.validate_or_repair("formation", stage, response, 0)
