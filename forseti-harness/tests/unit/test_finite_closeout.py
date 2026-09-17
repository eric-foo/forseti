"""Closeout must expose source meaning without claiming semantic acceptance."""
from copy import deepcopy
from argparse import Namespace
import io
import json
from pathlib import Path

import pytest

from harness_utils import hash_file
from judgment.review_evidence import compact_evidence, expand_evidence
from reports import finite_closeout as closeout
from runners import run_finite_semantic_consolidation as finite


def fixture():
    rows = [{"evidence_id": key, "text": text, "source_artifact_id": "raw",
             "parent_context": [{"text": "Before reformulation; personally sensitive."}],
             "engagement": {"value": None}, "independence_key": "same_person"}
            for key, text in (("s:a", "Not strongest hydration, but not drier. Sensitive lips. 🧴"),
                              ("s:b", "Drier after use; only in cold weather."),
                              ("s:c", "Expected a brush to help, not tested."),
                              ("s:d", "A separate minority report."))]
    units = [{"semantic_unit_ref": f"{r['evidence_id']}::u", "evidence_id": r["evidence_id"],
              "conditions": ["cold weather"] if r["evidence_id"] == "s:b" else [], "text": r["text"]}
             for r in rows]
    source = {"captured_items": rows, "source_artifacts": [{"artifact_id": "raw", "locator": "Zoë/源.json"}],
              "question": "What experiences and expectations are reported?"}
    verified = {"semantic_units": units, "evidence_dispositions": [{"evidence_id": "s:c", "status": "residual"}]}
    view = {"propositions": [{"proposition_id": "p1", "semantic_relations": {
                "supporting": ["s:a::u"], "opposing": ["s:b::u"], "adjacent": ["s:c::u"]},
                "conditions": ["cold weather"], "condition_lineage": {"s:b::u": ["cold weather"]}},
            {"proposition_id": "p2", "semantic_relations": {"supporting": ["s:d::u", "s:c::u"]}}],
            "unmerged_semantic_units": [{"semantic_unit_ref": "s:c::u", "reason": "expectation not observed"}]}
    questions = {"assessment_only": {"checks": [{"id": "contrast", "source_rows": ["s:a"], "expectation": "Preserve qualifications"}]}}
    return source, verified, view, questions


def test_anchor_selection_keeps_full_rows_all_relations_conditions_and_residuals():
    source, verified, view, questions = fixture()
    result = closeout.evidence_view(source, verified, view, questions)
    assert result["source_rows"] == source["captured_items"][:3]
    assert result["verified_units"] == verified["semantic_units"][:3]
    assert result["findings"] == view["propositions"][:1]
    assert result["residuals"] == view["unmerged_semantic_units"]
    assert result["selection"]["omitted_source_ids"] == ["s:d"]
    assert expand_evidence(compact_evidence(result)) == result
    # Changing an already-admitted source must survive; no vocabulary selector.
    source["captured_items"][0]["text"] = "I intended to buy; never completed the order. 旧版"
    assert closeout.evidence_view(source, verified, view, questions)["source_rows"][0] == source["captured_items"][0]


def test_missing_anchor_fails_and_missing_body_is_explicit():
    args = fixture()
    args[0]["captured_items"][0]["text"] = ""
    assert closeout.evidence_view(*args)["selection"]["missing_source_body_ids"] == ["s:a"]
    args[3]["assessment_only"]["checks"][0]["source_rows"].append("missing")
    with pytest.raises(ValueError, match="source anchor missing"):
        closeout.evidence_view(*args)


@pytest.mark.parametrize("check_status,scope,finding,status", [
    ("pass", "answer", None, "accepted"),
    ("partial", "answer", None, "accepted"),
    ("fail", "upstream_only", None, "accepted"),
    ("fail", "answer", None, "rejected"),
    ("uncertain", "unknown", None, "rejected"),
    ("pass", "answer", "major", "rejected"),
    ("pass", "answer", "minor", "accepted"),
])
def test_selection_preserves_rejected_candidate_and_upstream_status(tmp_path, check_status, scope, finding, status):
    frozen_path, candidate_path = tmp_path / "original", tmp_path / "candidate"
    check = {"status": check_status, "scope": scope}
    findings = [{"severity": finding, "status": "open", "introduced_at": "frozen_upstream",
                 "artifact_refs": ["current_answer:q"]}] if finding else []
    recheck = {"check_results": [check], "material_findings": findings}
    result = {"answer_corrections": 1, "affected_rechecks": 1, "answer_correction_status": status,
              "answer_correction_failed_checks": [check] if check_status in {"fail", "uncertain"} and scope != "upstream_only" else [],
              "final_answer": str(candidate_path if status == "accepted" else frozen_path)}
    before = deepcopy(recheck)
    assert closeout.selected_answer_path(result, frozen_path, candidate_path, {"answer": "old"}, {"answer": "new"}, recheck) == Path(result["final_answer"])
    assert recheck == before
    result["final_answer"] = str(tmp_path / "unrelated")
    with pytest.raises(ValueError, match="not authorized"):
        closeout.selected_answer_path(result, frozen_path, candidate_path, {}, {"new": True}, recheck)


def test_all_retained_and_no_correction_use_frozen_path(tmp_path):
    path = tmp_path / "frozen"
    result = {"answer_corrections": 0, "affected_rechecks": 0, "final_answer": str(path)}
    assert closeout.selected_answer_path(result, path, tmp_path / "candidate", {}, None, None) == path
    result.update(answer_corrections=1, affected_rechecks=1, answer_correction_status="original_retained", answer_correction_failed_checks=[])
    assert closeout.selected_answer_path(result, path, tmp_path / "candidate", {}, {}, {"material_findings": [], "check_results": []}) == path


def test_post_assessment_correction_recomposes_retained_answers():
    original = {"schema_version": "finite_answer_v1", "answers": [
        {"question_id": "q1", "answer": "kept"}, {"question_id": "q2", "answer": "old"}]}
    questions = [{"id": "q1"}, {"id": "q2"}]
    proposal = {"schema_version": "finite_answer_correction_v1",
                "answers": [{"question_id": "q2", "answer": "repaired"}],
                "retained_answers": [{"question_id": "q1", "reason": "nomination disproven"}]}
    composition = {"affected_question_ids": ["q1", "q2"]}
    # The runner's own two-step composition is the fidelity bar, not a copied literal.
    expected = finite.compose_answer_patch(original, finite.answer_correction_patch(original, proposal, questions),
                                           composition["affected_question_ids"])
    assert closeout.composed_correction(composition, original, proposal, questions) == expected
    assert expected["answers"] == [{"question_id": "q1", "answer": "kept"}, {"question_id": "q2", "answer": "repaired"}]
    # The pre-freeze unknown-evidence repair response is already the composed patch.
    repair = {"schema_version": "finite_answer_v1", "answers": [{"question_id": "q2", "answer": "cited"}]}
    assert closeout.composed_correction({"affected_question_ids": ["q2"]}, original, repair, questions)["answers"] == [
        {"question_id": "q1", "answer": "kept"}, {"question_id": "q2", "answer": "cited"}]
    # An affected question left unaccounted still fails loud in either shape.
    with pytest.raises(ValueError, match="replace or retain each affected question"):
        closeout.composed_correction(composition, original, {**proposal, "retained_answers": []}, questions)
    with pytest.raises(ValueError, match="replace exactly the affected questions"):
        closeout.composed_correction(composition, original, repair, questions)


def test_wrong_acceptance_status_fails_at_selection_boundary(tmp_path):
    result = {"answer_corrections": 1, "affected_rechecks": 1, "final_answer": str(tmp_path / "candidate"),
              "answer_correction_status": "accepted", "answer_correction_failed_checks": []}
    with pytest.raises(ValueError, match="acceptance differs"):
        closeout.selected_answer_path(result, tmp_path / "frozen", tmp_path / "candidate", {}, {"new": 1},
            {"material_findings": [], "check_results": [{"status": "uncertain", "scope": "answer"}]})


def test_material_status_cannot_erase_open_findings_or_rejected_selection():
    finding = {"severity": "major", "status": "open", "introduced_at": "current_answer", "artifact_refs": ["current_answer:q"]}
    assessment = {"material_findings": [finding]}
    result = {"remaining_material_answer_findings": [], "answer_material_status": "no_open_material_answer_defects_reported"}
    with pytest.raises(ValueError, match="saved material status differs"):
        closeout.check_material_status(result, assessment)
    result.update(remaining_material_answer_findings=[finding], answer_material_status="material_defects_remain")
    closeout.check_material_status(result, assessment)
    result["answer_correction_status"] = "rejected"
    with pytest.raises(ValueError, match="saved material status differs"):
        closeout.check_material_status(result, assessment)
    result["answer_material_status"] = "correction_rejected_original_requires_adjudication"
    closeout.check_material_status(result, assessment)


def test_stale_input_fails_before_native_validation(tmp_path, monkeypatch):
    source = tmp_path / "source.json"
    source.write_text('{"source":"before"}', encoding="utf-8")
    binding = {"inputs": {"source": {"path": str(source), "sha256": hash_file(source)}}}
    (tmp_path / "binding.json").write_text(json.dumps(binding), encoding="utf-8")
    source.write_text('{"source":"changed"}', encoding="utf-8")
    monkeypatch.setattr(finite.semantic, "build_bundle", lambda *a, **k: pytest.fail("wrong boundary"))
    with pytest.raises(ValueError, match="saved binding changed"):
        closeout.collect(tmp_path)
    source.unlink()
    with pytest.raises(FileNotFoundError):
        closeout.collect(tmp_path)


def test_replay_is_explicitly_outside_live_reader(tmp_path):
    (tmp_path / "binding.json").write_text('{"replay_from":"historical"}', encoding="utf-8")
    with pytest.raises(ValueError, match="historical replay is not a live closeout"):
        closeout.collect(tmp_path)


def test_complete_unicode_output_unknown_costs_and_no_overwrite(tmp_path, monkeypatch):
    run = tmp_path / "run"
    run.mkdir()
    value = {"saved_result": {"status": "requires_adjudication", "provider_root": str(run)},
             "semantic_verdict": "requires_human_or_agent_judgment", "mechanical_validation": {"coverage": {}},
             "native_accounting": {"usage": {"coverage": "unknown", "total_tokens": None}},
             "judgment_evidence": {"selection": {"missing_source_body_ids": ["missing"]}},
             "body": "敏感 🧴 does not imply dryness " * 500}
    monkeypatch.setattr(closeout, "collect", lambda *a: deepcopy(value))
    buffer = io.BytesIO()
    stream = io.TextIOWrapper(buffer, encoding="cp1252")
    monkeypatch.setattr(closeout, "print", lambda text: stream.write(text + "\n"), raising=False)
    assert closeout.main(["--run-root", str(run)]) == 0
    stream.flush()
    full = json.loads(buffer.getvalue().decode("cp1252"))
    assert expand_evidence(full["evidence"]) == value
    output = tmp_path / "consumer.json"
    assert closeout.main(["--run-root", str(run), "--output", str(output), "--max-output-bytes", "1024"]) == 0
    stream.flush()
    pointer = json.loads(buffer.getvalue().decode("cp1252").splitlines()[-1])
    assert pointer["return_view"] == "details_required"
    assert pointer["facts"]["native_usage"]["total_tokens"] is None
    assert expand_evidence(json.loads(output.read_text(encoding="utf-8"))["evidence"]) == value
    original = output.read_bytes()
    assert closeout.main(["--run-root", str(run), "--output", str(output)]) == 1
    assert output.read_bytes() == original
    assert closeout.main(["--run-root", str(run), "--output", str(run / "new.json")]) == 1
    assert not (run / "new.json").exists()


def test_existing_runner_dispatch_is_read_only(monkeypatch):
    monkeypatch.setattr(closeout, "main", lambda argv: 17 if argv == ["--help"] else 18)
    monkeypatch.setattr(finite, "FiniteRun", lambda *a: pytest.fail("closeout launched execution"))
    assert finite.main(["closeout", "--help"]) == 17


def saved_correction_run(tmp_path, outcome):
    """Actual runner-to-reader integration; only provider generation is controlled.

    These are synthetic test receipts, never model-quality or cost evidence.
    Prompts, schemas, compositions, final selections and saved inputs come from
    the production runner. The reader and its validators/accounting are unmocked.
    """
    from test_semantic_evidence_integration import (
        _source_v7, _v5_responses, _row_verification_responses, _finite_decision_response,
    )
    source = _source_v7(count=3)
    bundle = finite.semantic.build_bundle(source, max_prompt_bytes=80000, max_evidence_per_work_unit=30)
    compiled = finite.semantic.validate_batch_responses(bundle, _v5_responses(bundle, detailed_per_batch=3))
    verification, _ = finite.semantic.prepare_row_verification(bundle, compiled)
    verified = finite.semantic.apply_row_verification(bundle, compiled, verification,
                                                       _row_verification_responses(verification))
    ref = source["captured_items"][0]["evidence_id"]
    # Deliberately different from alphabetical order: retained/replaced answers
    # follow the commission, not the sorted composition affected-ID list.
    questions = {"questions": [{"id": "z"}, {"id": "a"}], "worker_instructions": "Answer both questions.",
                 "coverage": "Synthetic three-row integration fixture.",
                 "assessment_only": {"checks": [{"id": "contrast", "source_rows": [ref],
                                                "expectation": "Preserve source qualifications."}]}}
    answer = {"schema_version": "finite_answer_v1", "answers": [
        {"question_id": q["id"], "answer": "Original source-backed answer.", "evidence_refs": [ref], "limits": "Sample."}
        for q in questions["questions"]]}
    finding = {"severity": "major", "status": "open", "introduced_at": "current_answer",
               "source_refs": [ref], "artifact_refs": ["current_answer:z", "current_answer:a"],
               "defect": "Controlled nomination.", "effect": "Qualification lost.", "bounded_repair": "Check source."}
    assessment = {"schema_version": "finite_source_assessment_v1", "inventory_coverage": "Fixture.",
                  "comparison": "Fixture.", "unassessed_material": "None in fixture.", "overall_usefulness": "Bounded.",
                  "check_results": [{"check_id": "contrast", "status": "pass", "source_refs": [ref],
                                     "finding_refs": [], "explanation": "Controlled check."}],
                  "material_findings": [] if outcome == "pre_freeze" else [finding]}
    proposal = {"schema_version": "finite_answer_correction_v1",
                "answers": [{**answer["answers"][1], "answer": "Corrected source-backed answer."}],
                "retained_answers": [{"question_id": "z", "reason": "Original already preserves the distinction."}]}
    if outcome == "retained":
        proposal.update(answers=[], retained_answers=[{"question_id": q["id"], "reason": "No supported change."}
                                                      for q in questions["questions"]])
    recheck = {**deepcopy(assessment), "schema_version": "finite_source_assessment_v2", "material_findings": [],
               "check_results": [{**assessment["check_results"][0], "scope": "answer",
                                  "status": "fail" if outcome == "rejected" else "pass"}]}
    inputs = {"source": source, "bundle": bundle, "verified": verified, "questions": questions,
              "previous_answer": answer}
    paths = {name: tmp_path / "inputs" / (name + ".json") for name in inputs}
    for name, value in inputs.items():
        finite.persist(paths[name], value)
    run = finite.FiniteRun(Namespace(**paths, output_dir=tmp_path / "run", provider_root=None,
                                    replay_from=None, local_repair_successor=[], completed_recovery=[]))
    run.bind_executable = lambda: {"path": "synthetic-test-provider"}

    def fixture_job(name, prompt, schema, **kwargs):
        phase = name.split("/", 1)[0]
        if phase in {"formation", "finish"}:
            stage = finite.read(run.root / phase / "stage.json")
            response = _finite_decision_response(stage,
                [[(r, "support") for r in stage["batches"][0]["candidate_refs"]]], terminal=phase == "finish")
        elif phase == "answer":
            response = deepcopy(answer)
            if outcome == "pre_freeze":
                response["answers"][1]["evidence_refs"] = ["unknown-source"]
        elif phase == "assessment":
            response = assessment
        elif phase == "answer-correction":
            response = ({"schema_version": "finite_answer_v1", "answers": [answer["answers"][1]]}
                        if outcome == "pre_freeze" else proposal)
        else:
            assert phase == "assessment-recheck"
            response = recheck
        directory = run.root / name
        finite.persist_bytes(directory / "prompt.md", prompt.encode("utf-8"))
        finite.persist(directory / "response.schema.json", schema)
        attempt = directory / "attempts/job-attempt-001"
        finite.persist(attempt / "response.json", response)
        usage = {"input_tokens": 10, "cached_input_tokens": 0, "output_tokens": 2}
        events = [{"type": "thread.started", "thread_id": name}, {"type": "turn.started"},
                  {"type": "turn.completed", "usage": usage}]
        finite.persist_bytes(attempt / "events.jsonl", ("\n".join(json.dumps(e) for e in events) + "\n").encode())
        finite.persist_bytes(attempt / "stderr.log", b"")  # Startup remains unknown, never invented zero coverage.
        binding = {"codex_executable": "synthetic-test-provider", "model": "synthetic", "worktree": str(tmp_path),
                   "prompt_path": str(directory / "prompt.md"), "prompt_sha256": hash_file(directory / "prompt.md"),
                   "schema_sha256": hash_file(directory / "response.schema.json")}
        finite.persist(directory / "job/binding.json", {"binding": binding, "attempt_root": str(directory / "attempts")})
        finite.persist(attempt / "execution_receipt.json", {
            "schema_version": "forseti_provider_execution_receipt_v1", "outcome": "PROCESS_COMPLETED",
            "command": ["synthetic-test-provider", "--model", "synthetic", "-C", str(tmp_path)],
            "launch_metadata": {"authentication_observed": "chatgpt"}, "synthetic_test_fixture": True,
            "prompt_sha256": binding["prompt_sha256"], "response_schema_sha256": binding["schema_sha256"],
            "events_sha256": hash_file(attempt / "events.jsonl"), "stderr_sha256": hash_file(attempt / "stderr.log"),
            "response_sha256": hash_file(attempt / "response.json"), "usage": usage})
        return attempt / "response.json"

    run.job = fixture_job
    result = run.run()
    return run, result


@pytest.mark.parametrize("outcome,selected", [("mixed", "accepted"), ("retained", "original_retained"),
                                             ("rejected", "rejected"), ("pre_freeze", None)])
def test_saved_correction_runs_reach_complete_reader(tmp_path, outcome, selected):
    run, result = saved_correction_run(tmp_path, outcome)
    before = {p: hash_file(p) for p in tmp_path.rglob("*") if p.is_file()}
    view = closeout.collect(run.root)
    assert view["saved_result"] == result
    assert view["answers"]["selected"]["value"] == finite.read(result["final_answer"])
    assert view["answers"]["correction_candidate"]["value"] == finite.read(run.root / "answer-correction/answers-corrected.json")
    assert view["correction_records"]["composition"] == finite.read(run.root / "answer-correction/composition.json")
    assert result.get("answer_correction_status") == selected
    assert view["native_accounting"]["startup_observation_unknown_attempts"] > 0
    if outcome == "pre_freeze":
        assert view["affected_recheck"] is None
        assert view["answers"]["initial_provider_responses"][0]["value"] != view["answers"]["frozen"]["value"]
    else:
        assert view["correction_records"]["recheck_input"] == finite.read(run.root / "assessment-recheck/input.json")
        assert view["affected_recheck"]["check_results"][0]["scope"] == "answer"
        assert view["initial_assessment"]["material_findings"]
    if outcome == "rejected":
        assert view["answers"]["selected"]["value"] == view["answers"]["frozen"]["value"]
        assert view["answers"]["selected"]["value"] != view["answers"]["correction_candidate"]["value"]
    assert closeout.collect(run.root) == view
    assert {p: hash_file(p) for p in tmp_path.rglob("*") if p.is_file()} == before


@pytest.mark.parametrize("phase", ["answer-correction", "assessment-recheck"])
def test_saved_correction_input_tamper_is_refused(tmp_path, phase):
    run, _ = saved_correction_run(tmp_path, "mixed")
    path = run.root / phase / "input.json"
    value = finite.read(path)
    value["answer_commission"]["worker_instructions"] = "Changed after execution."
    path.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError, match="input differs from provider prompt"):
        closeout.collect(run.root)


def test_trailing_operation_flag_returns_structured_failure(tmp_path, capsys):
    run, _ = saved_correction_run(tmp_path, "mixed")
    operation = tmp_path / "operation"
    finite.persist(operation / "operation.json", {"command": ["--output-dir"], "provider_roots": [str(run.root)]})
    capsys.readouterr()
    assert closeout.main(["--run-root", str(run.root), "--operation-dir", str(operation)]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "FINITE_CLOSEOUT_FAILED"


def test_saved_recheck_schema_failure_returns_structured_failure(tmp_path, capsys):
    run, result = saved_correction_run(tmp_path, "mixed")
    response = Path(result["affected_recheck"])
    invalid = finite.read(response)
    del invalid["check_results"][0]["scope"]
    response.write_text(json.dumps(invalid), encoding="utf-8")
    # Preserve byte bindings deliberately: the reader must reach the actual
    # scoped schema validator, not merely reject an unrefreshed digest.
    for path in (response.parent / "execution_receipt.json", run.root / "assessment-recheck/result.json"):
        record = finite.read(path)
        record["response_sha256"] = hash_file(response)
        path.write_text(json.dumps(record), encoding="utf-8")
    capsys.readouterr()
    assert closeout.main(["--run-root", str(run.root)]) == 1
    failure = json.loads(capsys.readouterr().out)
    assert failure["status"] == "FINITE_CLOSEOUT_FAILED"
    assert "scope" in failure["error"]
