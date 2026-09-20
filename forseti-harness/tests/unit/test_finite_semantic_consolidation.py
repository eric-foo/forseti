"""Native acceptance, frozen replay and explicit provider-boundary failures."""
from argparse import Namespace
from copy import deepcopy
from pathlib import Path
import json
import sys

import pytest
from jsonschema import Draft202012Validator, ValidationError

from runners import run_finite_semantic_consolidation as finite
from runners import run_codex_provider_job as job_runner
from runners import run_codex_provider_attempt as launcher
from test_semantic_evidence_integration import (
    _missing_definition_fixture, _local_repair_fixture,
    _finite_row_identity_fixture, _finite_decision_response,
)


@pytest.mark.skipif(sys.platform != "win32", reason="Windows PowerShell output encoding")
def test_desktop_ancestry_preserves_non_ascii_paths(monkeypatch):
    native_run = finite.subprocess.run
    expected = "C:/Users/Zo\u00eb/\u30c7\u30fc\u30bf/ChatGPT.exe"

    def with_process_fixture(command, **kwargs):
        # Exercise the real Windows PowerShell serialization and Python decoding.
        fixture = ("function Get-CimInstance { param($ClassName, $Filter) "
                   "[pscustomobject]@{ProcessId=1; ParentProcessId=0; "
                   "Name='ChatGPT.exe'; ExecutablePath='" + expected + "'} }\n")
        return native_run([*command[:-1], fixture + command[-1]], **kwargs)

    monkeypatch.setattr(finite.subprocess, "run", with_process_fixture)
    assert launcher.desktop_process_context()["ancestors"][0]["path"] == expected


@pytest.fixture
def installed_codex(tmp_path, monkeypatch):
    monkeypatch.setenv("CODEX_INTERNAL_ORIGINATOR_OVERRIDE", "Codex Desktop")
    calls = []
    context = {"ancestors": []}
    state = Namespace(calls=calls, context=context)
    def install(version):
        executable = tmp_path / "Codex/bin" / version / "codex.exe"
        executable.parent.mkdir(parents=True, exist_ok=True)
        executable.write_text(version)
        host = tmp_path / "WindowsApps" / ("OpenAI.Codex_" + version) / "app/ChatGPT.exe"
        context["ancestors"] = [
            {"pid": 1, "parent_pid": 2, "name": "python.exe", "path": str(Path(sys.executable))},
            {"pid": 2, "parent_pid": 3, "name": "codex.exe", "path": str(executable)},
            {"pid": 3, "parent_pid": 4, "name": "ChatGPT.exe", "path": str(host)}]
        monkeypatch.setenv("CODEX_VERSION", version)
        state.executable = executable
    def local(exe, args, env):
        calls.append((exe, args))
        return Namespace(returncode=0, stdout="codex-cli " + Path(exe).read_text(), stderr="")
    install("1.0.0")
    monkeypatch.setattr(launcher, "desktop_process_context", lambda: deepcopy(context))
    monkeypatch.setattr(launcher, "_local_codex_check", local)
    state.install = install
    return state


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
    bound_executable = Path(selected["path"])
    installed_codex.install("1.2.0")
    assert run.bind_executable() == selected  # New host cannot silently rebind this run.
    bound_executable.write_text("changed bound bytes")
    with pytest.raises(ValueError, match="bound Codex executable changed"):
        run.job("other-job", "prompt", {"type": "object"})
    assert len(commands) == 1


def test_finite_forwards_and_verifies_completed_recovery(tmp_path, monkeypatch):
    run = object.__new__(finite.FiniteRun)
    run.root, run.provider_root, run.replay = tmp_path / "successor", tmp_path / "original", None
    name = "finish/provider/reconcile-0002-0002"
    record = {"mode": "completed_same_request_recovery", "attempt_dir": str(tmp_path / "diagnostic")}
    run.completed_recoveries, run.consumed_recoveries = {name: record}, set()
    run.bind_executable = lambda: {"path": "fixture-codex"}
    finite.persist(Path(record["attempt_dir"]) / "response.json", {})
    def provider(command, **kwargs):
        assert command[command.index("--completed-recovery")+1] == record["attempt_dir"]
        finite.persist(Path(command[command.index("--result-out")+1]), {
            "status": "PROCESS_COMPLETED_NOT_VALIDATED", "attempt_dir": record["attempt_dir"], "recovery": record})
        return Namespace(returncode=0)
    monkeypatch.setattr(finite.subprocess, "run", provider)
    assert run.job(name, "fixture", {"type": "object"}) == Path(record["attempt_dir"]) / "response.json"
    assert run.consumed_recoveries == {name}


@pytest.mark.parametrize("case", ["missing", "ambiguous", "foreign", "version", "arbitrary", "origin", "missing_file"])
def test_unverified_installation_fails_before_native_or_paid_work(installed_codex, monkeypatch, case):
    ancestors = installed_codex.context["ancestors"]
    if case == "missing":
        ancestors.pop(1)
    elif case == "ambiguous":
        ancestors.append({**ancestors[1], "pid": 99})
    elif case == "foreign":
        ancestors[2]["name"] = "unrelated.exe"
    elif case == "origin":
        monkeypatch.setenv("CODEX_INTERNAL_ORIGINATOR_OVERRIDE", "unrelated")
    elif case == "missing_file":
        installed_codex.executable.unlink()
    elif case == "version":
        monkeypatch.setenv("CODEX_VERSION", "9.9.9")
    else:
        installed_codex.executable.write_text("not-codex")
    with pytest.raises(ValueError):
        finite.select_codex_executable()
    assert len(installed_codex.calls) == (1 if case in {"arbitrary", "version"} else 0)


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


def test_inherited_selection_rechecks_bytes_and_explicit_override_wins(tmp_path, installed_codex, monkeypatch):
    selected = launcher.select_codex_executable()
    binding = tmp_path / "selection.json"
    binding.write_text(json.dumps(selected), encoding="utf-8")
    monkeypatch.setenv("FORSETI_CODEX_SELECTION", str(binding))
    monkeypatch.setenv("FORSETI_CODEX_SELECTION_SHA256", finite.hash_file(binding))
    monkeypatch.setattr(launcher, "desktop_process_context", lambda: {"ancestors": []})
    assert launcher.select_codex_executable() == selected
    installed_codex.executable.write_text("changed")
    with pytest.raises(ValueError):
        launcher.select_codex_executable()
    override = tmp_path / "override.exe"
    override.write_text("3.0.0")
    assert launcher.select_codex_executable(override)["path"] == str(override.resolve())


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
    run.grouping_rejections = {}
    finite.persist(run.args.bundle, bundle)
    finite.persist(run.root / "formation/stage.json", stage)
    return run


def unsupported_finish_fixture():
    bundle, verified, formation = _finite_row_identity_fixture()
    formed_response = _finite_decision_response(formation,
        [[(ref, "support")] for ref in formation["batches"][0]["candidate_refs"]], terminal=False)
    formed = finite.semantic.validate_reconciliation_stage(bundle, formation, [formed_response])
    finish, _ = finite.semantic.prepare_reconciliation_stage(bundle, formed,
        completion_strategy=finite.semantic.FINITE_COMPLETION_STRATEGY, packing_strategy="group_aware_v1")
    by_row = {}
    for candidate in finish["candidates"]:
        row = candidate["leaf_relations"][0]["semantic_unit_ref"].rsplit("::", 1)[0]
        by_row.setdefault(row, []).append(candidate["candidate_ref"])
    shared = next(refs for refs in by_row.values() if len(refs) == 2)
    others = [ref for refs in by_row.values() for ref in refs if ref not in shared]
    response = _finite_decision_response(finish,
        [[(ref, "support") for ref in refs] for refs in (shared, others)], terminal=True)
    return bundle, verified, finish, response, shared


def test_unsupported_finish_group_retains_evidence_and_valid_group_without_model(tmp_path):
    bundle, verified, stage, failed, shared = unsupported_finish_fixture()
    run = bare_run(tmp_path, bundle, stage)
    run.verified = verified
    response = tmp_path / "original.json"
    finite.persist(response, failed)
    before = response.read_bytes()
    with pytest.raises(finite.semantic.UnsupportedFinishGroupings, match="lacks repeated source-row support"):
        finite.semantic.validate_reconciliation_stage(bundle, stage, [failed])
    run.job = lambda *a, **k: pytest.fail("declining a grouping must not invoke a model")
    successor = run.validate_or_repair("finish", stage, response, 0)
    restored = finite.read(successor)
    assert restored["semantic_nodes"] == failed["semantic_nodes"][1:]
    assert set(restored["decisions_by_candidate_ref"]) == set(failed["decisions_by_candidate_ref"])
    for ref, decision in restored["decisions_by_candidate_ref"].items():
        if ref in shared:
            assert decision["attachments"] == []
            assert "one distinct supporting source row" in decision["unmerged_reason"]
        else:
            assert decision == failed["decisions_by_candidate_ref"][ref]
    compiled = finite.semantic.validate_reconciliation_stage(bundle, stage, [restored])
    view = finite.semantic.finalize_v3_view(bundle, verified, compiled)
    packet = finite.semantic.project_evidence_packet(view, bundle, verified, compiled,
        proposition_ids=[p["proposition_id"] for p in view["propositions"]])
    counts = finite.coverage(bundle, verified, view, packet)
    assert counts == dict(source_rows=3, verified_statements=4, attached_statements=2,
                         residual_statements=2, findings=1, missing_statements=0, packet_truncated=False)
    assert {r["semantic_unit_ref"] for r in view["unmerged_semantic_units"]} == {
        leaf["semantic_unit_ref"] for c in stage["candidates"] if c["candidate_ref"] in shared
        for leaf in c["leaf_relations"]}
    assert run.validate_or_repair("finish", stage, response, 0) == successor
    assert response.read_bytes() == before
    assert not (run.root / "repair-budget").exists()
    rejection = finite.read(next(iter(run.grouping_rejections.values())))
    assert rejection["retained_candidate_refs"] == sorted(shared)
    assert rejection["original_response_sha256"] == finite.hash_file(response)
    assert rejection["successor_sha256"] == finite.hash_file(successor)
    assert rejection["model_api_calls"] == 0
    assert "lacks repeated" in finite.read(successor.parent.parent / "failure.json")["error"]
    successor.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="existing finite output differs"):
        run.validate_or_repair("finish", stage, response, 0)


@pytest.mark.parametrize("mutation, error", [
    ("missing_candidate", "candidate decisions"),
    ("duplicate_definition", "duplicate or empty node key"),
    ("bad_claim_kind", "lacks claim metadata"),
    ("other_node_bad_claim_kind", "lacks claim metadata"),
    ("zero_support", "lacks repeated source-row support"),
    ("multiple_attachments", "multiple attachments"),
])
def test_other_finish_defects_stop_without_retention_or_paid_repair(tmp_path, mutation, error):
    bundle, _, stage, failed, shared = unsupported_finish_fixture()
    if mutation == "missing_candidate":
        del failed["decisions_by_candidate_ref"][shared[0]]
    elif mutation == "duplicate_definition":
        failed["semantic_nodes"].append(deepcopy(failed["semantic_nodes"][0]))
    elif mutation == "bad_claim_kind":
        failed["semantic_nodes"][0]["claim_kind"] = "unknown"
    elif mutation == "other_node_bad_claim_kind":
        # A defect in a different, well-supported node must still stop the run
        # even though the single-row node deferred earlier in the same batch.
        failed["semantic_nodes"][1]["claim_kind"] = "unknown"
    elif mutation == "zero_support":
        for ref in shared:
            failed["decisions_by_candidate_ref"][ref]["attachments"][0]["relation"] = "counter"
    else:
        failed["decisions_by_candidate_ref"][shared[0]]["attachments"].append(
            {"semantic_node_key": failed["semantic_nodes"][1]["semantic_node_key"], "relation": "support"})
    run = bare_run(tmp_path, bundle, stage)
    response = tmp_path / "failed.json"
    finite.persist(response, failed)
    run.job = lambda *a, **k: pytest.fail("unrelated defects must not invoke repair")
    with pytest.raises(finite.semantic.SemanticIntegrationError, match=error) as caught:
        run.validate_or_repair("finish", stage, response, 0)
    assert type(caught.value) is finite.semantic.SemanticIntegrationError
    assert not run.grouping_rejections
    assert not (run.root / "finish/accepted").exists()


def test_valid_distinct_source_group_is_unchanged(tmp_path):
    bundle, _, stage, response, _ = unsupported_finish_fixture()
    refs = stage["batches"][0]["candidate_refs"]
    response = _finite_decision_response(stage, [[(ref, "support") for ref in refs]], terminal=True)
    run = bare_run(tmp_path, bundle, stage)
    path = tmp_path / "valid.json"
    finite.persist(path, response)
    assert run.validate_or_repair("finish", stage, path, 0) == path
    assert not run.grouping_rejections


@pytest.mark.parametrize("formation_terminal, error", [
    (True, "cannot unmerge required finding"),
    (False, "carries repeated source-row support"),
])
def test_rejection_cannot_retire_an_existing_repeated_finding(formation_terminal, error):
    bundle, _, formation = _finite_row_identity_fixture()
    by_row = {}
    for candidate in formation["candidates"]:
        ref = candidate["candidate_ref"]
        by_row.setdefault(ref.rsplit("::", 1)[0], []).append(ref)
    shared = next(refs for refs in by_row.values() if len(refs) == 2)
    others = [ref for refs in by_row.values() for ref in refs if ref not in shared]
    response = _finite_decision_response(formation, [
        [(shared[0], "support"), (others[0], "support")],
        [(shared[1], "support")], [(others[1], "support")]], terminal=formation_terminal)
    formed = finite.semantic.validate_reconciliation_stage(bundle, formation, [response])
    finish, _ = finite.semantic.prepare_reconciliation_stage(bundle, formed,
        completion_strategy=finite.semantic.FINITE_COMPLETION_STRATEGY, packing_strategy="group_aware_v1")
    repeated = next(c for c in finish["candidates"] if len(c["leaf_relations"]) == 2)
    single = next(c for c in finish["candidates"] if c != repeated)
    failed = _finite_decision_response(finish,
        [[(repeated["candidate_ref"], "counter"), (single["candidate_ref"], "support")]], terminal=True)
    with pytest.raises(finite.semantic.UnsupportedFinishGroupings):
        finite.semantic.validate_reconciliation_stage(bundle, finish, [failed])
    # The declined group's own support is single-row, but this counter-attached
    # child carries two distinct supporting rows of its own. Required-finding
    # retention names that case exactly when it applies; the grouping guard
    # refuses the rest instead of authoring an undeclared unmerge.
    with pytest.raises(finite.semantic.SemanticIntegrationError, match=error):
        finite.semantic.reject_unsupported_finish_groupings(bundle, finish, failed)


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


@pytest.mark.parametrize("excluded", [0, 6])
def test_coverage_is_input_derived_and_rejects_missing_or_overlapping_statement(excluded):
    bundle = {"evidence_units": [{"evidence_id": "one"}, {"evidence_id": "two"}],
        "coverage_denominator": {"captured_item_count": 2 + excluded,
            "accounting_disposition_counts": {"mechanically_excluded": excluded}}}
    verified = {"semantic_units": [{"semantic_unit_ref": "a"}, {"semantic_unit_ref": "b"}]}
    view = {"coverage": {"accounted_item_count": 2 + excluded, "captured_item_count": 2 + excluded,
        "semantically_assessed_item_count": 2, "mechanically_excluded_item_count": excluded,
        "blocked_item_count": 0, "complete": True},
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
    for field in ("accounted_item_count", "semantically_assessed_item_count", "mechanically_excluded_item_count"):
        changed = deepcopy(view)
        changed["coverage"][field] += 1
        with pytest.raises(ValueError, match="does not account for every source row"):
            finite.coverage(bundle, verified, changed, packet)


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


def test_generation_choices_reject_wrong_kind_without_changing_recovery(tmp_path):
    run, answer = answer_fixture(tmp_path)
    run.verified["semantic_units"] = [{"semantic_unit_ref": "known::u"}]
    schema = finite.answer_generation_schema(run.questions["questions"],
        run.bundle["evidence_units"], run.verified["semantic_units"])
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    for refs in (["known"], ["known::u"], ["known", "known::u"], []):
        answer["answers"][0]["evidence_refs"] = refs
        validator.validate(answer)
        finite.check_answer(answer, run.questions["questions"], run.bundle, run.verified)
    for ref in ("prop_supplied_finding", "unknown", ""):
        answer["answers"][0]["evidence_refs"] = [ref]
        # This is the historical failure: the old structural schema admits it.
        Draft202012Validator(finite.answer_schema(run.questions["questions"])).validate(answer)
        with pytest.raises(ValidationError) as failure:
            validator.validate(answer)
        assert failure.value.validator == "enum"
        assert list(failure.value.path) == ["answers", 0, "evidence_refs", 0]
        with pytest.raises(finite.UnknownAnswerEvidence):
            finite.check_answer(answer, run.questions["questions"], run.bundle, run.verified)


def test_generation_empty_evidence_and_invalid_identities_are_not_unrestricted(tmp_path):
    run, answer = answer_fixture(tmp_path)
    schema = finite.answer_generation_schema(run.questions["questions"], [], [])
    Draft202012Validator.check_schema(schema)
    for row in answer["answers"]:
        row.update(answer="No supplied evidence supports an answer.", evidence_refs=[], limits="No evidence supplied.")
    Draft202012Validator(schema).validate(answer)
    finite.check_answer(answer, run.questions["questions"], {"evidence_units": []}, {"semantic_units": []})
    answer["answers"][0]["evidence_refs"] = ["invented"]
    with pytest.raises(ValidationError) as failure:
        Draft202012Validator(schema).validate(answer)
    assert failure.value.validator == "maxItems"
    for bad in ("", " ", None, 42):
        for rows, units in (([{"evidence_id": bad}], []), ([], [{"semantic_unit_ref": bad}])):
            with pytest.raises(ValueError, match="nonempty source identities"):
                finite.answer_generation_schema(run.questions["questions"], rows, units)


@pytest.mark.parametrize("malformed", [False, True])
def test_initial_job_generation_schema_does_not_preempt_recovery(tmp_path, monkeypatch, malformed):
    run, answer = answer_fixture(tmp_path)
    answer["answers"][0]["evidence_refs"] = ["prop_supplied_finding"]
    if malformed:
        del answer["answers"][0]["limits"]
    structural = finite.answer_schema(run.questions["questions"])
    generation = finite.answer_generation_schema(run.questions["questions"], run.bundle["evidence_units"], [])
    run.bind_executable = lambda: {"path": "fixture-codex"}
    def provider(command, **kwargs):
        assert finite.read(Path(command[command.index("--output-schema") + 1])) == generation
        attempt = run.provider_root / "answer/provider/attempts/job-attempt-001"
        finite.persist(attempt / "response.json", answer)
        finite.persist(Path(command[command.index("--result-out") + 1]), {
            "status": "PROCESS_COMPLETED_NOT_VALIDATED", "attempt_dir": str(attempt)})
        return Namespace(returncode=0)
    monkeypatch.setattr(finite.subprocess, "run", provider)
    if malformed:
        with pytest.raises(ValidationError) as failure:
            run.job("answer/provider", "fixture", generation, validation_schema=structural)
        assert failure.value.validator == "required"
    else:
        response = run.job("answer/provider", "fixture", generation, validation_schema=structural)
        with pytest.raises(finite.UnknownAnswerEvidence):
            finite.check_answer(finite.read(response), run.questions["questions"], run.bundle, run.verified)


@pytest.mark.parametrize("replay", [False, True])
def test_initial_answer_call_uses_live_choices_but_retains_historical_schema(tmp_path, replay):
    run, answer = answer_fixture(tmp_path)
    run.questions.update(worker_instructions="fixture", coverage={})
    # Most real citations are unit refs, so the live vocabulary must carry them.
    run.verified.update(evidence_dispositions=[],
                        semantic_units=[{"evidence_id": "known", "semantic_unit_ref": "known::u"}])
    run.source = {"captured_items": [], "source_artifacts": []}
    run.args = Namespace(previous_answer=tmp_path / "prior.json")
    finite.persist(run.args.previous_answer, answer)
    response = tmp_path / "answer.json"
    finite.persist(response, answer)
    view = {"propositions": [], "unmerged_semantic_units": []}
    if replay:
        run.replay = tmp_path / "saved"
        # Build the exact consumer input through the same native entry below.
        run.check_saved_input = lambda *args: None
    class CapturedInitial(Exception):
        pass
    def job(name, prompt, schema, **kwargs):
        assert name == "answer/provider"
        expected = finite.answer_schema(run.questions["questions"]) if replay else finite.answer_generation_schema(
            run.questions["questions"], run.bundle["evidence_units"], run.verified["semantic_units"])
        assert schema == expected
        assert replay or "known::u" in schema["properties"]["answers"]["items"]["properties"]["evidence_refs"]["items"]["enum"]
        assert kwargs["validation_schema"] == finite.answer_schema(run.questions["questions"])
        assert kwargs["replay_response"] == (response if replay else None)
        raise CapturedInitial
    run.job = job
    if replay:
        # Persist intercept supplies historical fixture bytes before replay checks.
        original_persist = finite.persist
        def persist_input(path, value):
            original_persist(path, value)
            if Path(path) == run.root / "answer/input.json":
                original_persist(run.replay / "answer-v3/input.json", value)
                original_persist(run.replay / "answer-v3/freeze.json", {"response": str(response)})
            return value
        with pytest.MonkeyPatch.context() as patcher:
            patcher.setattr(finite, "persist", persist_input)
            with pytest.raises(CapturedInitial):
                run.answer_and_assess(view, {}, {})
    else:
        with pytest.raises(CapturedInitial):
            run.answer_and_assess(view, {}, {})


def test_assessment_receives_actual_answer_commission(tmp_path):
    run, answer = answer_fixture(tmp_path)
    run.questions.update(worker_instructions="Answer only the two supplied questions.", coverage="fixture")
    run.questions["questions"] = [{"id": "one", "question": "The first narrow question?"},
                                 {"id": "two", "question": "The second narrow question?"}]
    run.questions["assessment_only"] = {"checks": []}
    run.verified["evidence_dispositions"] = []
    run.source = {"question": "A much broader research question?", "captured_items": [], "source_artifacts": []}
    run.args = Namespace(previous_answer=tmp_path / "prior.json")
    finite.persist(run.args.previous_answer, answer)
    response = tmp_path / "answer.json"
    finite.persist(response, answer)

    class CapturedAssessment(Exception):
        pass

    def job(name, prompt, schema, **kwargs):
        if name == "answer/provider":
            assert "assessment_checks" not in prompt
            return response
        assert name == "assessment/provider"
        request = finite.read(run.root / "assessment/input.json")
        assert request["answer_commission"] == {
            "questions": run.questions["questions"], "worker_instructions": run.questions["worker_instructions"]}
        assert all(q["question"] in prompt for q in run.questions["questions"])
        assert run.questions["worker_instructions"] in prompt
        assert request["complete_frozen_source"]["question"] == run.source["question"]
        raise CapturedAssessment

    run.job = job
    with pytest.raises(CapturedAssessment):
        run.answer_and_assess({"propositions": [], "unmerged_semantic_units": []}, {}, [])


def _keyed_assessment(assessment, ids):
    """Model-output fixture; production deliberately has no legacy-to-wire converter."""
    value = deepcopy(assessment)
    rows = value.pop("check_results")
    value["schema_version"] = value["schema_version"].replace("_v", "_keyed_v")
    value["commissioned_checks"] = {r["check_id"]: {k: v for k, v in r.items() if k != "check_id"}
                                     for r in rows if r["check_id"] in ids}
    value["additional_checks"] = [r for r in rows if r["check_id"] not in ids]
    return value


@pytest.mark.parametrize("scoped", [False, True])
def test_assessment_generation_binds_names_and_preserves_all_judgments(scoped):
    checks = [{"id": "behavior_contrasts"}, {"id": "additional_check_1"}]
    result = {"schema_version": "finite_source_assessment_v2" if scoped else "finite_source_assessment_v1",
              "inventory_coverage": "Bounded", "comparison": "Not identical", "unassessed_material": "Outside rows",
              "overall_usefulness": "Material issue remains", "material_findings": [], "check_results": [
                  {"check_id": ref, "status": status, "source_refs": ["source"], "finding_refs": [],
                   "explanation": ref, **({"scope": "unknown"} if scoped else {})}
                  for ref, status in [("behavior_contrasts", "partial"), ("additional_check_1", "pass"),
                                      ("extra", "fail"), ("extra_two", "uncertain")]]}
    wire = _keyed_assessment(result, [c["id"] for c in checks])
    wire["commissioned_checks"] = dict(reversed(list(wire["commissioned_checks"].items())))
    original = deepcopy(wire)
    schema = finite.assessment_generation_schema(checks, scoped_checks=scoped)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(wire)
    assert finite.assessment_from_response(wire, checks, scoped_checks=scoped) == result
    assert wire == original
    assert finite.assessment_from_response(result, checks, scoped_checks=scoped) == result
    for perturbation in ("renamed", "missing", "extra_name", "model_supplied_id"):
        bad = deepcopy(wire)
        named = bad["commissioned_checks"]
        if perturbation == "renamed":
            named["frozen.behavior_contrasts"] = named.pop("behavior_contrasts")
        elif perturbation == "missing":
            named.pop("behavior_contrasts")
        elif perturbation == "extra_name":
            named["uncommissioned"] = deepcopy(named["behavior_contrasts"])
        else:
            named["behavior_contrasts"]["check_id"] = "frozen.behavior_contrasts"
        with pytest.raises(ValidationError):
            Draft202012Validator(schema).validate(bad)
        with pytest.raises(ValidationError):
            finite.assessment_from_response(bad, checks, scoped_checks=scoped)
    bad = deepcopy(wire)
    del bad["additional_checks"][0]["check_id"]
    with pytest.raises(ValidationError):
        finite.assessment_from_response(bad, checks, scoped_checks=scoped)
    for collision in ("behavior_contrasts", "extra_two"):
        bad = deepcopy(wire)
        bad["additional_checks"][0]["check_id"] = collision
        with pytest.raises(ValueError, match="omits or duplicates commissioned checks"):
            finite.assessment_from_response(bad, checks, scoped_checks=scoped)


@pytest.mark.parametrize("checks", [[{"id": "same"}, {"id": "same"}], [{"id": ""}], [{"id": None}],
                                    [{}], [None], [{"id": []}], [{"id": "  "}]])
def test_assessment_generation_refuses_ambiguous_commissions(checks):
    with pytest.raises(ValueError, match="unique nonempty identities"):
        finite.assessment_generation_schema(checks)


def test_assessment_generation_supports_no_commissioned_checks():
    result = {"schema_version": "finite_source_assessment_v1", "inventory_coverage": "Fixture",
              "comparison": "Fixture", "unassessed_material": "None", "overall_usefulness": "Bounded",
              "material_findings": [], "check_results": []}
    wire = _keyed_assessment(result, [])
    assert finite.assessment_from_response(wire, []) == result


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
    monkeypatch.setattr(job_runner, "select_codex_executable", lambda path: {
        "path": str(path.resolve()), "sha256": finite.hash_file(path), "version": "codex-cli 1.0.0"})
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
    run.questions = {"questions": [{"id": "one"}, {"id": "two"}], "worker_instructions": "Answer the supplied questions."}
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


@pytest.mark.parametrize("field", ["answer", "limits", "evidence_refs"])
def test_unknown_citation_exact_repair_keeps_valid_references_and_unrelated_text(tmp_path, field):
    run, original = answer_fixture(tmp_path)
    original["answers"][0][field] = ["unknown"] if field == "evidence_refs" else "Keep before [s:typo] keep after."
    unknown = "unknown" if field == "evidence_refs" else "s:typo"
    known = {"known", "s:correct"}
    errors = {"one": [unknown]}
    repair = {"answer_sha256": finite.answer_identity(original), "edits": [
        {"question_id": "one", "field": field, "before": unknown, "after": "s:correct", "source_refs": ["s:correct"]}]}
    corrected = finite.apply_exact_answer_repairs(original, repair, [], known, errors)
    assert corrected["answers"][1] == original["answers"][1]
    assert corrected["answers"][0][field] == (["s:correct"] if field == "evidence_refs" else "Keep before [s:correct] keep after.")
    assert original["answers"][0][field] != corrected["answers"][0][field]
    # Even an observed invalid index entry cannot be removed, guessed or used for unrelated prose.
    for replacement in ("", "invented", "s:correct plus invented meaning"):
        repair["edits"][0]["after"] = replacement
        with pytest.raises(ValueError, match="source scope"):
            finite.apply_exact_answer_repairs(original, repair, [], known, errors)


def test_other_answer_failures_do_not_enter_unknown_citation_recovery(tmp_path):
    run, answer = answer_fixture(tmp_path)
    answer["answers"].reverse()
    with pytest.raises(ValueError, match="identities/order differ") as failure:
        finite.check_answer(answer, run.questions["questions"], run.bundle, run.verified)
    assert not isinstance(failure.value, finite.UnknownAnswerEvidence)
    assert not (run.provider_root / "answer-correction/allowance.json").exists()


@pytest.mark.parametrize("outcome", ["minor", "partial", "unaddressed", "major", "reversed_comparator", "unknown_locator", "uncertain_origin",
                                         "failed_check", "uncertain_check", "upstream_only", "upstream_uncertain",
                                         "extra_answer_fail", "extra_answer_uncertain", "extra_unknown_fail",
                                         "extra_unknown_uncertain", "upstream_answer", "consolidation_answer",
                                         "upstream_commissioned", "missing_scope", "false_scope", "invalid_scope", "legacy_report"])
def test_post_assessment_correction_rechecks_before_adopting_candidate(tmp_path, outcome):
    run, answer = answer_fixture(tmp_path)
    if outcome == "reversed_comparator":
        answer["answers"][0]["answer"] = "Alpha has a reported advantage over Beta."
    run.questions["worker_instructions"] = "Answer both commissioned questions."
    original_path = run.root / "original.json"
    finite.persist(original_path, answer)
    finite.persist(run.root / "answer/freeze.json", {"response": str(original_path)})
    original_bytes = original_path.read_bytes()
    run.source = {"captured_items": [{"evidence_id": "known"}, {"evidence_id": "outside"}]}
    run.bundle["evidence_units"].append({"evidence_id": "outside"})
    run.verified["semantic_units"] = [{"evidence_id": ref, "semantic_unit_ref": ref + "::u"}
                                      for ref in ("known", "outside")]
    run.questions["assessment_only"] = {"checks": [{"id": "anchored", "source_rows": ["known"]}]}
    assessment = {"material_findings": [{"severity": "major", "status": "open", "introduced_at": "current_answer",
        "artifact_refs": ["current_answer:one"], "source_refs": ["known"]}]}
    patch = {"schema_version": "finite_answer_correction_v1", "retained_answers": [],
             "answers": [{**answer["answers"][0], "answer": "corrected"}]}
    assessment.update(schema_version="finite_source_assessment_v3", answer_repairs={
        "answer_sha256": finite.answer_identity(answer), "edits": [{"question_id": "one", "field": "answer",
        "before": "bounded", "after": "corrected", "source_refs": ["known"]}]})
    if outcome == "reversed_comparator":
        assessment["answer_repairs"]["edits"][0].update(
            before="Alpha has a reported advantage over Beta.", after="Beta has a reported advantage over Alpha.")
        patch["answers"][0]["answer"] = "Beta has a reported advantage over Alpha."
        run.source["captured_items"][0]["text"] = "I preferred Alpha over Beta in winter."
    finite.persist(run.root / "assessment/result.json", {"response": "fixture-review", "response_sha256": "fixture"})
    new_defect = {"severity": "minor", "introduced_at": "current_answer", "status": "open", "source_refs": ["known"],
        "artifact_refs": ["current_answer:one"], "defect": "fixture", "effect": "fixture", "bounded_repair": "fixture"}
    recheck = {"schema_version": "finite_source_assessment_v2", "inventory_coverage": "fixture", "comparison": "fixture",
        "unassessed_material": "fixture", "overall_usefulness": "fixture", "material_findings": [new_defect],
        "check_results": [{"check_id": "anchored", "scope": "answer", "status": "pass", "source_refs": ["known"], "finding_refs": [],
                           "explanation": "fixture"}]}
    if outcome in {"reversed_comparator", "major", "unknown_locator", "uncertain_origin"}:
        new_defect.update(severity="blocker", artifact_refs=["corrected_affected_answers:one"])
        if outcome == "reversed_comparator":
            new_defect.update(defect="Exact edit reversed Alpha and Beta despite the supplied source.",
                              effect="Applicability cannot establish semantic acceptance.")
        if outcome == "unknown_locator":
            new_defect["artifact_refs"] = ["unrecognized_input_label"]
        if outcome == "uncertain_origin":
            new_defect["introduced_at"] = "uncertain"
    elif outcome in {"failed_check", "uncertain_check", "partial"}:
        recheck["check_results"][0]["status"] = {"failed_check": "fail", "uncertain_check": "uncertain", "partial": "partial"}[outcome]
    elif outcome in {"upstream_only", "upstream_uncertain", "upstream_answer", "consolidation_answer"}:
        new_defect.update(severity="major", introduced_at="frozen_upstream", artifact_refs=["verified_units[known::u]"])
        recheck["check_results"].append({"check_id": "extra_inventory", "scope": "upstream_only",
            "status": "uncertain" if outcome == "upstream_uncertain" else "fail", "source_refs": ["known"],
            "finding_refs": ["material_findings[0]"], "explanation": "Frozen inventory remains defective; answer is repaired."})
        if outcome in {"upstream_answer", "consolidation_answer"}:
            # A contradictory scope label cannot hide a real answer finding.
            new_defect["artifact_refs"].append("corrected_affected_answers:one")
            if outcome == "consolidation_answer":
                new_defect["introduced_at"] = "current_consolidation"
    elif outcome.startswith("extra_"):
        _, scope, status = outcome.split("_")
        recheck["material_findings"] = []  # Checks independently veto adoption.
        recheck["check_results"].append({"check_id": "genuine_added_check", "scope": scope, "status": status,
            "source_refs": ["known"], "finding_refs": [], "explanation": "A new answer defect or unresolved scope."})
    elif outcome == "upstream_commissioned":
        new_defect.update(severity="major", introduced_at="current_consolidation", artifact_refs=["current_findings[0]"])
        recheck["check_results"][0].update(scope="upstream_only", status="fail")
    invalid_report = outcome in {"missing_scope", "false_scope", "invalid_scope", "legacy_report"}
    if invalid_report:
        recheck["material_findings"] = []
        recheck["check_results"][0]["status"] = "fail"
        if outcome in {"missing_scope", "legacy_report"}:
            recheck["check_results"][0].pop("scope")
        else:
            recheck["check_results"][0]["scope"] = False if outcome == "false_scope" else "not_answer"
        if outcome == "legacy_report":
            recheck["schema_version"] = "finite_source_assessment_v1"
            finite.check_assessment(recheck, run.questions)  # Still a valid historical/full assessment.
    if outcome == "unaddressed":
        assessment["material_findings"].append({"severity": "major", "status": "open", "introduced_at": "current_answer",
                                               "artifact_refs": ["unroutable_other_question"]})
    accepted = outcome in {"minor", "partial", "unaddressed", "upstream_only", "upstream_uncertain",
                           "upstream_commissioned"}
    responses = {"answer-correction/provider": run.provider_root / "patch.json",
                 "assessment-recheck/provider": run.provider_root / "recheck.json"}
    wire_recheck = recheck if outcome == "legacy_report" else _keyed_assessment(recheck, ["anchored"])
    finite.persist(responses["answer-correction/provider"], patch)
    finite.persist(responses["assessment-recheck/provider"], wire_recheck)
    frozen_inputs = deepcopy((run.questions, run.source, run.bundle, run.verified, assessment))
    launched = []
    def correction_job(name, prompt, schema):
        launched.append(name)
        request = finite.read(run.root / name.removesuffix("/provider") / "input.json")
        assert request["answer_commission"] == {
            "questions": run.questions["questions"], "worker_instructions": run.questions["worker_instructions"]}
        assert request["affected_questions"] == run.questions["questions"][:1]
        assert "questions" not in request and "worker_instructions" not in request
        assert name == "assessment-recheck/provider"  # No interpretation/rewrite call.
        if not invalid_report:
            Draft202012Validator(schema).validate(wire_recheck)
        assert request["exact_repairs"] == assessment["answer_repairs"]
        assert request["corrected_affected_answers"] == patch["answers"]
        return responses[name]
    run.job = correction_job
    if invalid_report:
        with pytest.raises(ValidationError) as failure:
            run.correct_and_recheck(answer, assessment, {"propositions": []})
        assert failure.value.validator == {
            "missing_scope": "required", "false_scope": "type", "invalid_scope": "enum", "legacy_report": "const"}[outcome]
        assert original_path.read_bytes() == original_bytes
        assert launched == ["assessment-recheck/provider"]
        return
    result = run.correct_and_recheck(answer, assessment, {"propositions": []})
    corrected = finite.read(result["final_answer"])
    if accepted and outcome != "retain":
        assert corrected["answers"] == [patch["answers"][0], answer["answers"][1]]
        assert result["answer_correction_status"] == "accepted"
    else:
        assert corrected == answer
        assert Path(result["final_answer"]) == original_path
        assert result["answer_correction_status"] == ("original_retained" if accepted else "rejected")
    assert original_path.read_bytes() == original_bytes
    assert finite.read(result["answer_correction_candidate"])["answers"] == (
        answer["answers"] if outcome == "retain" else [patch["answers"][0], answer["answers"][1]])
    assert result["answer_material_status"] == (
        "material_defects_remain" if outcome == "unaddressed" else "no_open_material_answer_defects_reported" if accepted
        else "correction_rejected_original_requires_adjudication")
    assert result["remaining_material_answer_findings"] == (
        assessment["material_findings"][1:] if outcome == "unaddressed" else [] if accepted else assessment["material_findings"])
    assert launched == ["assessment-recheck/provider"]
    assert (result["answer_corrections"], result["affected_rechecks"]) == (1, 1)
    assert result["affected_recheck_material_findings"] == recheck["material_findings"]
    assert result["affected_recheck_check_results"] == recheck["check_results"]
    assert result["answer_correction_failed_checks"] == [
        c for c in recheck["check_results"] if c["status"] in {"fail", "uncertain"} and c["scope"] != "upstream_only"]
    assert finite.read(run.root / "assessment-recheck/input.json")["frozen_relevant_checks"] == run.questions["assessment_only"]["checks"]
    assert finite.read(run.provider_root / "answer-correction/allowance.json")["kind"] == "post_assessment"
    # Repeating the consumer over the same saved responses preserves the exact result.
    assert run.correct_and_recheck(answer, assessment, {"propositions": []}) == result
    assert (run.questions, run.source, run.bundle, run.verified, assessment) == frozen_inputs


def test_saved_unscoped_recheck_keeps_historical_selection_without_live_acceptance(tmp_path):
    run, answer = answer_fixture(tmp_path)
    run.replay = tmp_path / "historical"
    run.source = {"captured_items": [{"evidence_id": "known"}]}
    run.verified = {"semantic_units": []}
    run.questions["assessment_only"] = {"checks": []}
    assessment = {"material_findings": [{"severity": "major", "status": "open", "introduced_at": "current_answer",
        "artifact_refs": ["current_answer:one"], "source_refs": ["known"]}]}
    corrected_row = {**answer["answers"][0], "answer": "historically selected correction"}
    patch_path = run.replay / "answer-correction/provider/attempts/job-attempt-001/response.json"
    recheck_path = run.replay / "assessment-recheck/provider/attempts/job-attempt-001/response.json"
    recheck = {"schema_version": "finite_source_assessment_v1", "inventory_coverage": "fixture", "comparison": "fixture",
        "unassessed_material": "fixture", "overall_usefulness": "fixture", "material_findings": [],
        "check_results": [{"check_id": "old_unscoped", "status": "fail", "source_refs": [],
                           "finding_refs": [], "explanation": "Historical response, not current acceptance."}]}
    finite.persist(patch_path, corrected_row)
    finite.persist(recheck_path, recheck)
    finite.persist(run.replay / "answer-correction/input.json", {
        "assessor_nominations_to_verify_against_sources": assessment["material_findings"],
        "original_answer_one": answer["answers"][0]})
    finite.persist(run.replay / "assessment-recheck/input.json", {"corrected_answer_one": corrected_row})
    finite.persist(run.replay / "assessment-recheck/response.schema.json", finite.assessment_schema())
    saved_bytes = (patch_path.read_bytes(), recheck_path.read_bytes())
    run.saved = {"fixture": [(patch_path, {}), (recheck_path, {})]}
    checked_inputs = []
    run.check_saved_input = lambda directory, tag: checked_inputs.append((directory, tag))
    run.job = lambda *a, **k: pytest.fail("historical replay launched a provider")
    result = run.correct_and_recheck(answer, assessment, {"propositions": []})
    assert finite.read(result["final_answer"])["answers"] == [corrected_row, answer["answers"][1]]
    assert "answer_correction_status" not in result and "answer_material_status" not in result
    assert result["affected_recheck"] == str(recheck_path)
    assert checked_inputs == [("answer-correction", "answer_correction_input_json"),
                              ("assessment-recheck", "affected_recheck_input_json")]
    assert (patch_path.read_bytes(), recheck_path.read_bytes()) == saved_bytes
    assert finite.read(run.root / "assessment-recheck/result.json")["saved_replay"] is True


@pytest.mark.parametrize("invalid", ["missing", "overlap", "duplicate_replacement", "duplicate_retention", "foreign", "order"])
def test_correction_must_partition_questions_without_dropping_or_reordering(tmp_path, invalid):
    run, answer = answer_fixture(tmp_path)
    proposal = {"schema_version": "finite_answer_correction_v1", "answers": [answer["answers"][0]],
                "retained_answers": [{"question_id": "two", "reason": "No defect."}]}
    if invalid == "missing":
        proposal["retained_answers"] = []
    elif invalid == "overlap":
        proposal["retained_answers"].append({"question_id": "one", "reason": "Conflicting action."})
    elif invalid == "duplicate_replacement":
        proposal["answers"] *= 2
    elif invalid == "duplicate_retention":
        proposal["retained_answers"] *= 2
    elif invalid == "foreign":
        proposal["retained_answers"][0]["question_id"] = "outside"
    else:
        proposal.update(answers=list(reversed(answer["answers"])), retained_answers=[])
    with pytest.raises(ValueError, match="exactly once|identities/order"):
        finite.answer_correction_patch(answer, proposal, run.questions["questions"])


def test_correction_can_mix_a_repair_with_verbatim_retention(tmp_path):
    run, answer = answer_fixture(tmp_path)
    proposal = {"schema_version": "finite_answer_correction_v1",
                "answers": [{**answer["answers"][1], "answer": "A supported repair."}],
                "retained_answers": [{"question_id": "one", "reason": "The original already answers its question."}]}
    schema = finite.answer_correction_schema(run.questions["questions"], run.bundle["evidence_units"], [])
    Draft202012Validator(schema).validate(proposal)
    result = finite.answer_correction_patch(answer, proposal, run.questions["questions"])
    assert result["answers"] == [answer["answers"][0], proposal["answers"][0]]
    finite.check_answer(result, run.questions["questions"], run.bundle, run.verified)


@pytest.mark.parametrize("kind", ["local-repair successor", "completed-recovery"])
def test_unused_local_repair_successor_fails_before_paid_consumers(tmp_path, monkeypatch, kind):
    run, _ = answer_fixture(tmp_path)
    run.provider_root, run.source, run.consumed_repairs = run.root, {}, set()
    run.bundle["schema_version"] = "fixture"
    args = {"provider_root": None, "codex_executable": Path(sys.executable),
            "local_repair_successor": [["formation:unmatched", "request", "patch", "successor"]]}
    for name in ("source", "bundle", "verified", "questions", "previous_answer"):
        args[name] = tmp_path / (name + ".json")
        finite.persist(args[name], {})
    run.args = Namespace(**args)
    if kind == "completed-recovery":
        run.args.local_repair_successor = []
        run.completed_recoveries, run.consumed_recoveries = {"finish/provider/unmatched": {}}, set()
    run.bind_executable = lambda: {"path": str(args["codex_executable"])}
    monkeypatch.setattr(finite.semantic, "build_bundle", lambda *a, **k: run.bundle)
    run.phase = lambda name, compilation: {}
    run.consumers = lambda *a: pytest.fail("stale repair binding must stop before answer and assessment jobs")
    with pytest.raises(ValueError, match="unused " + kind):
        run.run()
    assert not (run.root / "result.json").exists()


def test_unsupported_packet_metadata_stops_before_any_paid_phase(tmp_path, monkeypatch):
    run, _ = answer_fixture(tmp_path)
    run.provider_root, run.source, run.consumed_repairs = run.root, {}, set()
    run.bundle["schema_version"] = "fixture"
    run.bundle["evidence_units"][0]["engagement"] = {
        "posture": "not_interpreted", "material_positive": False, "unknown_field": "must not disappear",
    }
    args = {"provider_root": None, "codex_executable": Path(sys.executable), "local_repair_successor": []}
    for name in ("source", "bundle", "verified", "questions", "previous_answer"):
        args[name] = tmp_path / (name + ".json")
        finite.persist(args[name], {})
    run.args = Namespace(**args)
    run.bind_executable = lambda: {"path": str(args["codex_executable"])}
    monkeypatch.setattr(finite.semantic, "build_bundle", lambda *a, **k: run.bundle)
    run.phase = lambda *a: pytest.fail("unsupported source metadata must stop before generation")
    with pytest.raises(finite.semantic.SemanticIntegrationError, match="engagement shape"):
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


@pytest.mark.parametrize("case,message", [
    ("missing", "anchor is missing"), ("ambiguous", "anchor is missing"),
    ("overlap", "anchors overlap"), ("stale", "stale frozen"),
    ("question", "answer scope"), ("source", "source scope"),
    ("inline", "outside its source refs"), ("empty", "omit a nominated")])
def test_exact_repairs_reject_at_the_intended_boundary(tmp_path, case, message):
    run, answer = answer_fixture(tmp_path)
    answer["answers"][0]["answer"] = "Preserve preface. aaaabounded. Preserve tail."
    nominations = [{"severity": "major", "status": "open", "introduced_at": "current_answer",
        "artifact_refs": ["current_answer:one"], "source_refs": ["known"]}]
    edit = {"question_id": "one", "field": "answer", "before": "bounded", "after": "supported",
            "source_refs": ["known"]}
    repairs = {"answer_sha256": finite.answer_identity(answer), "edits": [edit]}
    if case == "missing": edit["before"] = "absent"
    if case == "ambiguous": edit["before"] = "aaa"  # Overlapping matches count too.
    if case == "overlap": repairs["edits"].append({**edit, "before": "aaaabounded"})
    if case == "stale": repairs["answer_sha256"] = "old"
    if case == "question": edit["question_id"] = "two"
    if case == "source": edit["source_refs"] = ["s:outside"]
    if case == "inline": edit["after"] = "supported [s:outside]"
    if case == "empty": repairs["edits"] = []
    before = deepcopy(answer)
    Draft202012Validator(finite.exact_repairs_schema()).validate(repairs)
    with pytest.raises(ValueError, match=message):
        finite.apply_exact_answer_repairs(answer, repairs, nominations, {"known", "s:outside"})
    assert answer == before


def test_exact_repairs_preserve_unrelated_bytes_additions_and_reject_reapplication(tmp_path):
    _, answer = answer_fixture(tmp_path)
    answer["answers"][0].update(answer="Prefix 🧴. Two users. Other claim.", limits="Keep limit.")
    nominations = [{"severity": "major", "status": "open", "introduced_at": "current_answer",
        "artifact_refs": ["current_answer:one"], "source_refs": ["known", "s:new"]}]
    repairs = {"answer_sha256": finite.answer_identity(answer), "edits": [
        {"question_id": "one", "field": "answer", "before": "Two users", "after": "One origin in two observations", "source_refs": ["known"]},
        {"question_id": "one", "field": "limits", "before": "Keep limit.", "after": "Keep limit. Split experience [s:new].", "source_refs": ["s:new"]}]}
    corrected = finite.apply_exact_answer_repairs(answer, repairs, nominations, {"known", "s:new"})
    assert corrected["answers"][0] == {**answer["answers"][0],
        "answer": "Prefix 🧴. One origin in two observations. Other claim.",
        "limits": "Keep limit. Split experience [s:new].", "evidence_refs": ["known", "s:new"]}
    assert corrected["answers"][1] == answer["answers"][1]
    with pytest.raises(ValueError, match="stale frozen"):
        finite.apply_exact_answer_repairs(corrected, repairs, nominations, {"known", "s:new"})
    target = tmp_path / "candidate.json"
    finite.persist(target, corrected)
    frozen_bytes = target.read_bytes()
    finite.persist(target, finite.apply_exact_answer_repairs(answer, repairs, nominations, {"known", "s:new"}))
    assert target.read_bytes() == frozen_bytes
    repairs["edits"][0]["after"] = "Another answer"
    with pytest.raises(ValueError, match="existing finite output differs"):
        finite.persist(target, finite.apply_exact_answer_repairs(answer, repairs, nominations, {"known", "s:new"}))


@pytest.mark.parametrize("case", ["inline_only", "wrong_question", "wrong_entry", "valid_inline", "valid_index"])
def test_reviewer_generation_offers_only_actual_invalid_index_entries(tmp_path, case):
    _, answer = answer_fixture(tmp_path)
    answer["answers"][0]["answer"] = "Inline [s:typo]."
    if case != "inline_only":
        answer["answers"][1]["evidence_refs"] = ["s:index-typo"]
    known = {"known", "s:correct"}
    edit = {"question_id": "two", "field": "evidence_refs", "before": "s:index-typo",
            "after": "s:correct", "source_refs": ["s:correct"]}
    if case in {"inline_only", "wrong_question"}: edit.update(question_id="one", before="s:typo")
    if case == "wrong_entry": edit["before"] = "s:typo"
    if case == "valid_inline": edit.update(question_id="one", field="answer", before="s:typo")
    repairs = {"answer_sha256": finite.answer_identity(answer), "edits": [edit]}
    bound = finite.assessment_generation_schema([], exact_repairs=True, answer=answer, known_refs=known)
    schema = bound["properties"]["answer_repairs"]
    Draft202012Validator.check_schema(bound)
    if case.startswith("valid"):
        Draft202012Validator(schema).validate(repairs)
    else:
        # Identical complete edit passes transport shape but fails the actual generation target binding.
        Draft202012Validator(finite.exact_repairs_schema()).validate(repairs)
        with pytest.raises(ValidationError) as failure:
            Draft202012Validator(schema).validate(repairs)
        assert failure.value.validator == ("enum" if case == "inline_only" else "anyOf")
