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


def saved_correction_run(tmp_path, outcome, *, selected=False):
    """Actual runner-to-reader integration; only provider generation is controlled.

    These are synthetic test receipts, never model-quality or cost evidence.
    Prompts, schemas, compositions, final selections and saved inputs come from
    the production runner. The reader and its validators/accounting are unmocked.
    """
    from test_semantic_evidence_integration import (
        _source_v7, _v5_responses, _row_verification_responses, _finite_decision_response,
    )
    from test_finite_semantic_consolidation import _keyed_assessment
    source = _source_v7(count=5 if selected else 3)
    excluded_row = "reddit:t1:excluded"
    if outcome.startswith("excluded_row"):
        # A mechanically excluded capture stays an assessable source row but
        # never becomes a citable evidence unit.
        kept = source["captured_items"][0]
        source["captured_items"].append({
            "evidence_id": excluded_row, "accounting_disposition": "mechanically_excluded",
            "accounting_reason": "native body unavailable in fixture",
            **{k: kept[k] for k in ("container_id", "source_artifact_id", "source_ref")}})
        source["containers"][0]["captured_leaf_count"] += 1
    bundle = finite.semantic.build_bundle(source, max_prompt_bytes=80000, max_evidence_per_work_unit=30)
    compiled = finite.semantic.validate_batch_responses(bundle, _v5_responses(bundle, detailed_per_batch=3))
    verification, _ = finite.semantic.prepare_row_verification(bundle, compiled)
    verified = finite.semantic.apply_row_verification(bundle, compiled, verification,
                                                       _row_verification_responses(verification))
    if selected:
        from judgment.verified_evidence_selection import derive_verified_selection
        dependencies = {}
        for name, value in (("source", source), ("bundle", bundle), ("verified", verified)):
            path = tmp_path / "original-proof" / (name + ".json")
            finite.persist(path, value)
            dependencies[name] = {"path": str(path.resolve()), "sha256": hash_file(path)}
        source, bundle, verified = derive_verified_selection(dependencies,
            [r["evidence_id"] for r in bundle["evidence_units"][:3]])
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
    if outcome.startswith("inventory_counts_"):
        answer["answers"][1]["answer"] += " Inventory contains " + ("30" if outcome.endswith("wrong") else "3") + " rows."
    if outcome.startswith("invalid_draft"):
        answer["answers"][1]["evidence_refs"] = ["unknown-source"]
        answer["answers"][1]["answer"] += " [" + ref.split(":")[0] + ":typo]"
    if outcome == "excluded_row_draft":
        answer["answers"][1]["answer"] += " [" + excluded_row + "]"
    draft = outcome.startswith("invalid_draft") or outcome == "excluded_row_draft"
    finding = {"severity": "major", "status": "open", "introduced_at": "current_answer",
               "source_refs": [ref], "artifact_refs": ["current_answer:a"],
               "defect": "Controlled nomination.", "effect": "Qualification lost.", "bounded_repair": "Check source."}
    if outcome.startswith("partial_"):
        finding["artifact_refs"].append("current_answer:z")
    assessment = {"schema_version": "finite_source_assessment_v1", "inventory_coverage": "Fixture.",
                  "comparison": "Fixture.", "unassessed_material": "None in fixture.", "overall_usefulness": "Bounded.",
                  "check_results": [{"check_id": "contrast", "status": "pass", "source_refs": [ref],
                                     "finding_refs": [], "explanation": "Controlled check."}],
                  "material_findings": [] if draft else [finding]}
    assessment["check_results"].append({"check_id": "additional.source_traceability", "status": "pass",
        "source_refs": [ref], "finding_refs": [], "explanation": "Extra source-backed check."})
    repairs = {"answer_sha256": finite.answer_identity(answer), "edits": [] if draft else [
        {"question_id": "a", "field": "answer", "before": "Original", "after": "Corrected", "source_refs": [ref]}]}
    if outcome.startswith("invalid_draft"):
        repairs["edits"] = [
            {"question_id": "a", "field": "evidence_refs", "before": "unknown-source", "after": ref, "source_refs": [ref]},
            {"question_id": "a", "field": "answer", "before": ref.split(":")[0] + ":typo", "after": ref, "source_refs": [ref]}]
    if outcome == "excluded_row_draft":
        repairs["edits"] = [{"question_id": "a", "field": "answer", "before": excluded_row,
                             "after": ref, "source_refs": [ref]}]
    if outcome == "excluded_row_repair":
        finding["source_refs"] = [excluded_row]
        repairs["edits"][0]["source_refs"] = [excluded_row]
    if outcome == "invalid_draft_unrepaired":
        repairs["edits"] = []
    recheck = {**deepcopy(assessment), "schema_version": "finite_source_assessment_v2", "material_findings": [],
               "check_results": [{**check, "scope": "answer"} for check in assessment["check_results"]]}
    assessment.update(schema_version="finite_source_assessment_v3", answer_repairs=repairs)
    if outcome in {"rejected", "invalid_draft_rejected", "partial_rejected"}:
        recheck["check_results"][-1]["status"] = "fail"
    if outcome == "improvement":
        recheck["material_findings"] = [{**finding, "defect": "Unchanged residual citation gap", "introduced_at": "historical_answer"}]
        recheck["check_results"][-1]["status"] = "fail"
    if outcome == "partial_rejected":
        recheck["material_findings"] = [{**finding, "artifact_refs": ["current_answer:z"],
                                        "defect": "The unedited answer still loses the qualification."}]
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
            if outcome.startswith("invalid_draft"):
                response["answers"][1]["evidence_refs"] = ["unknown-source"]
        elif phase == "assessment":
            response = assessment
        elif phase == "answer-correction":
            response = ({"schema_version": "finite_answer_v1", "answers": [answer["answers"][1]]}
                        if outcome.startswith("invalid_draft") else pytest.fail("unexpected paid rewrite"))
        else:
            assert phase == "assessment-recheck"
            if outcome.startswith("partial_"):
                request = finite.read(run.root / "assessment-recheck/input.json")
                assert [q["id"] for q in request["affected_questions"]] == ["z", "a"]
                assert request["corrected_affected_answers"][0] == answer["answers"][0]
                assert [r["question_id"] for r in request["retained_answers"]] == ["z"]
            response = {**recheck, "schema_version": "finite_source_assessment_v4", "answer_comparison": None}
            if outcome.startswith("inventory_counts_"):
                request = finite.read(run.root / "assessment-recheck/input.json")
                packet = finite.read(run.root / "packet-all.json")
                assert request["program_verified_inventory"] == finite.recheck_inventory_facts(packet)
                assert "only for inventory accounting" in prompt
                assert "Do not demand source-row quotations" in prompt
                expected_count = request["program_verified_inventory"]["corpus_coverage"]["captured_item_count"]
                candidate = finite.read(run.root / "answer-correction/answers-corrected.json")
                matches = f"Inventory contains {expected_count} rows." in candidate["answers"][1]["answer"]
                response["material_findings"] = [{**finding, "source_refs": [], "introduced_at": "historical_answer",
                    "defect": "Inventory count compared with native accounting", "status": "not_a_defect" if matches else "open"}]
                response["check_results"][-1].update(status="pass" if matches else "uncertain", source_refs=[])
            if outcome == "improvement":
                from test_review_evidence import comparison_for_test
                request = finite.read(run.root / "assessment-recheck/input.json")
                candidate = finite.read(run.root / "answer-correction/answers-corrected.json")
                response["answer_comparison"] = comparison_for_test(answer, candidate, assessment, response, request,
                                                                   {0: ("a", "source-backed answer.")})
        if phase in {"assessment", "assessment-recheck"}:
            response = _keyed_assessment(response, ["contrast"])
            finite.Draft202012Validator(schema).validate(response)
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


@pytest.mark.parametrize("outcome,status", [("partial_accepted", "accepted"), ("partial_rejected", "rejected")])
def test_partial_exact_repair_keeps_unedited_questions_in_recheck_and_saved_validation(tmp_path, outcome, status):
    run, result = saved_correction_run(tmp_path, outcome)
    payload = closeout.collect(run.root)
    original = payload["answers"]["frozen"]["value"]
    candidate = payload["answers"]["correction_candidate"]["value"]
    assert result["answer_correction_status"] == status
    assert candidate["answers"][0] == original["answers"][0]
    assert candidate["answers"][1] != original["answers"][1]
    assert payload["answers"]["selected"]["value"] == (candidate if status == "accepted" else original)
    assert payload["correction_records"]["composition"]["affected_question_ids"] == ["a", "z"]
    if status == "rejected":
        assert result["remaining_material_answer_findings"]
        assert result["affected_recheck_material_findings"][0]["artifact_refs"] == ["current_answer:z"]
    # Historical v1 records retain the old all-edited requirement.
    composition = {**payload["correction_records"]["composition"], "method": "reviewer_exact_repairs_v1"}
    assessment = payload["initial_assessment"]
    known = {r["evidence_id"] for r in run.bundle["evidence_units"]}
    with pytest.raises(ValueError, match="omit a nominated answer"):
        closeout.composed_correction(composition, original, assessment["answer_repairs"],
                                    run.questions["questions"], assessment=assessment, known_refs=known)


@pytest.mark.parametrize("field,mutate", [
    ("affected_questions", lambda value: value[1:]),
    ("corrected_affected_answers", lambda value: value[1:]),
    ("nominations_to_verify_against_sources", lambda value: value[1:]),
    ("retained_answers", lambda value: value[1:]),
    # Keeping the question but retracting its open-nomination reason is also lost scope.
    ("retained_answers", lambda value: [{**value[0], "reason": "Already resolved; no recheck needed."}])])
def test_saved_partial_recheck_cannot_drop_unchanged_nominated_scope(tmp_path, field, mutate):
    run, _ = saved_correction_run(tmp_path, "partial_accepted")
    path = run.root / "assessment-recheck/input.json"
    request = finite.read(path)
    request[field] = mutate(request[field])
    path.write_text(json.dumps(request), encoding="utf-8")
    # Deliberately bind the reduced request as if it were what the provider saw:
    # reject lost review scope, not just a stale digest.
    binding_path = run.root / "assessment-recheck/provider/job/binding.json"
    binding = finite.read(binding_path)
    prompt = Path(binding["binding"]["prompt_path"])
    prefix = prompt.read_text(encoding="utf-8").rstrip().rsplit("\n", 1)[0]
    packet = finite.render_evidence(request).rstrip().rsplit("\n", 1)[-1]
    prompt.write_text(prefix + "\n" + packet + "\n", encoding="utf-8")
    binding["binding"]["prompt_sha256"] = hash_file(prompt)
    binding_path.write_text(json.dumps(binding), encoding="utf-8")
    receipt_path = run.root / "assessment-recheck/provider/attempts/job-attempt-001/execution_receipt.json"
    receipt = finite.read(receipt_path)
    receipt["prompt_sha256"] = hash_file(prompt)
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
    with pytest.raises(ValueError, match="recheck omits or changes affected answer scope"):
        closeout.collect(run.root)


def test_saved_recheck_without_a_correction_reports_the_missing_candidate(tmp_path):
    run, _ = saved_correction_run(tmp_path, "partial_accepted")
    path = run.root / "result.json"
    result = finite.read(path)
    result["answer_corrections"] = 0
    path.write_text(json.dumps(result), encoding="utf-8")
    with pytest.raises(ValueError, match="recheck lacks a correction candidate"):
        closeout.collect(run.root)


def test_failed_runner_emits_one_compact_diagnostic_without_changing_saved_work(tmp_path, monkeypatch, capsys):
    with pytest.raises(ValueError, match="outside nominated source scope") as observed:
        saved_correction_run(tmp_path, "excluded_row_repair")
    root = tmp_path / "run"
    before = {p: hash_file(p) for p in tmp_path.rglob("*") if p.is_file()}
    def fail():
        raise observed.value
    monkeypatch.setattr(finite, "FiniteRun", lambda args: type("FailedRun", (), {"run": staticmethod(fail)})())
    argv = [arg for name in ("source", "bundle", "verified", "questions", "previous-answer")
            for arg in ("--" + name, str(tmp_path / "inputs" / (name.replace("-", "_") + ".json")))]
    capsys.readouterr()
    assert finite.main([*argv, "--output-dir", str(root)]) == 1
    terminal = json.loads(capsys.readouterr().out)
    record = finite.read(terminal["failure"])
    assert record["error"] == str(observed.value)
    assert record["status"] == "FINITE_EXECUTION_FAILED_OR_UNKNOWN"
    diagnostic = record["diagnostics"]
    assert diagnostic["diagnostic_issues"] == []
    assert diagnostic["coverage"]["missing_statements"] == 0
    assert diagnostic["repair_scope"] == {"nominated_question_ids": ["a"], "edited_question_ids": ["a"],
                                          "unedited_nominated_question_ids": []}
    assert diagnostic["initial_assessment"]["commissioned_checks"] == {"contrast": "pass"}
    assert diagnostic["initial_assessment"]["material_findings"][0]["status"] == "open"
    assert set(diagnostic["usage_by_stage"]) == {"formation", "finish", "answer", "assessment"}
    assert diagnostic["native_accounting"]["usage"]["total_tokens"] == 48  # Synthetic, not model-cost proof.
    assert diagnostic["native_accounting"]["startup_observation_unknown_attempts"] == 4
    assert {p: hash_file(p) for p in before} == before
    assert not (root / "answer-correction/answers-corrected.json").exists()
    assert not (root / "assessment-recheck").exists()


def test_failure_diagnostics_keep_changed_evidence_and_unknown_usage_explicit(tmp_path):
    with pytest.raises(ValueError):
        saved_correction_run(tmp_path, "excluded_row_repair")
    root = tmp_path / "run"
    response = root / "assessment/provider/attempts/job-attempt-001/response.json"
    response.write_text("{}", encoding="utf-8")
    diagnostic = closeout.failure_summary(root, root)
    assert diagnostic["initial_assessment"] is None
    assert any("changed" in issue for issue in diagnostic["diagnostic_issues"])
    assert diagnostic["native_accounting"]["unknown_usage_attempts"] == 1
    assert diagnostic["native_accounting"]["usage"]["total_tokens"] is None
    assert diagnostic["usage_by_stage"]["assessment"]["total_tokens"] is None


def test_broken_diagnostic_cannot_replace_original_execution_failure(tmp_path, monkeypatch, capsys):
    def fail():
        raise ValueError("original execution failure")
    def broken_diagnostic(*args):
        raise OSError("diagnostic unavailable")
    monkeypatch.setattr(finite, "FiniteRun", lambda args: type("FailedRun", (), {"run": staticmethod(fail)})())
    monkeypatch.setattr(closeout, "failure_summary", broken_diagnostic)
    argv = [arg for name in ("source", "bundle", "verified", "questions", "previous-answer")
            for arg in ("--" + name, str(tmp_path / name))]
    assert finite.main([*argv, "--output-dir", str(tmp_path / "run")]) == 1
    record = finite.read(json.loads(capsys.readouterr().out)["failure"])
    assert record["error"] == "original execution failure"
    assert record["diagnostic_error"] == "diagnostic unavailable"


@pytest.mark.parametrize("outcome,selected", [("mixed", "accepted"),
                                              ("rejected", "rejected"), ("invalid_draft", "accepted")])
def test_saved_correction_runs_reach_complete_reader(tmp_path, outcome, selected):
    run, result = saved_correction_run(tmp_path, outcome)
    before = {p: hash_file(p) for p in tmp_path.rglob("*") if p.is_file()}
    view = closeout.collect(run.root)
    assert view["saved_result"] == result
    assert view["initial_assessment"]["check_results"][-1]["check_id"] == "additional.source_traceability"
    assert view["answers"]["selected"]["value"] == finite.read(result["final_answer"])
    assert view["answers"]["correction_candidate"]["value"] == finite.read(run.root / "answer-correction/answers-corrected.json")
    assert view["correction_records"]["composition"] == finite.read(run.root / "answer-correction/composition.json")
    assert result.get("answer_correction_status") == selected
    assert view["native_accounting"]["startup_observation_unknown_attempts"] > 0
    assert view["correction_records"]["recheck_input"] == finite.read(run.root / "assessment-recheck/input.json")
    assert view["affected_recheck"]["check_results"][0]["scope"] == "answer"
    assert view["affected_recheck"]["check_results"] == result["affected_recheck_check_results"]
    assert view["affected_recheck"]["check_results"][-1]["check_id"] == "additional.source_traceability"
    if outcome == "invalid_draft":
        assert view["initial_assessment"]["material_findings"] == []  # Citation validity does not inflate materiality.
        assert finite.read(run.root / "assessment/input.json")["citation_validation"]["status"] == "invalid_draft"
        assert not (run.root / "answer-correction/provider").exists()
        assert len(result["provider_execution_receipts"]) == 5  # Two synthetic consolidation, answer, reviewer, recheck.
    else:
        assert view["initial_assessment"]["material_findings"]
    if outcome == "rejected":
        assert [c["check_id"] for c in result["answer_correction_failed_checks"]] == ["additional.source_traceability"]
        assert view["answers"]["selected"]["value"] == view["answers"]["frozen"]["value"]
        assert view["answers"]["selected"]["value"] != view["answers"]["correction_candidate"]["value"]
    assert run.run() == result  # Same frozen draft/repairs rederive identical durable bytes.
    assert closeout.collect(run.root) == view
    assert {p: hash_file(p) for p in tmp_path.rglob("*") if p.is_file()} == before


@pytest.mark.parametrize("phase", ["answer-correction", "assessment-recheck"])
def test_saved_correction_input_tamper_is_refused(tmp_path, phase):
    run, _ = saved_correction_run(tmp_path, "mixed")
    path = run.root / phase / "input.json"
    value = finite.read(path)
    value["answer_commission"]["worker_instructions"] = "Changed after execution."
    path.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError, match="saved binding changed|input differs from provider prompt"):
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
    del invalid["commissioned_checks"]["contrast"]["scope"]
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


@pytest.mark.parametrize("outcome,error", [("invalid_draft_rejected", finite.UnknownAnswerEvidence),
                                         ("invalid_draft_unrepaired", ValueError)])
def test_invalid_frozen_answer_cannot_be_selected_after_failed_exact_repair(tmp_path, outcome, error):
    with pytest.raises(error):
        saved_correction_run(tmp_path, outcome)
    root = tmp_path / "run"
    assert not (root / "result.json").exists()
    frozen = finite.read(finite.read(root / "answer/freeze.json")["response"])
    assert frozen["answers"][1]["evidence_refs"] == ["unknown-source"]
    assert not (root / "answer-correction/provider").exists()
    if outcome == "invalid_draft_rejected":
        assert (root / "answer-correction/answers-corrected.json").is_file()
        assert (root / "assessment-recheck/result.json").is_file()


def test_excluded_capture_is_not_a_citable_answer_reference_for_the_reader(tmp_path):
    """The reader resolves answer references the way the runner validated them.

    A captured row the bundle excluded is assessable source but not a citable
    answer reference, so the frozen draft's inline use of it is a real
    reference error and its saved exact repair is in the recorded scope.
    """
    run, result = saved_correction_run(tmp_path, "excluded_row_draft")
    source, bundle = finite.read(run.args.source), finite.read(run.args.bundle)
    assert ({r["evidence_id"] for r in source["captured_items"]}
            - {u["evidence_id"] for u in bundle["evidence_units"]}) == {"reddit:t1:excluded"}
    assert finite.read(run.root / "assessment/input.json")["citation_validation"] == {
        "status": "invalid_draft", "unknown_references_by_question": {"a": ["reddit:t1:excluded"]}}
    assert result["answer_correction_status"] == "accepted"
    view = closeout.collect(run.root)
    selected = view["answers"]["selected"]["value"]
    assert selected == finite.read(result["final_answer"])
    assert "reddit:t1:excluded" not in selected["answers"][1]["answer"]


def test_excluded_capture_repair_reference_fails_before_recheck(tmp_path):
    with pytest.raises(ValueError, match="exact repair sources are outside nominated source scope"):
        saved_correction_run(tmp_path, "excluded_row_repair")
    assert not (tmp_path / "run/answer-correction/answers-corrected.json").exists()
    assert not (tmp_path / "run/assessment-recheck").exists()


def test_saved_improvement_selected_with_visible_residual_and_no_extra_job(tmp_path):
    run, result = saved_correction_run(tmp_path, "improvement")
    view = closeout.collect(run.root)
    assert result["answer_correction_status"] == "selected_requires_adjudication"
    assert result["answer_material_status"] == "selected_answer_requires_adjudication"
    assert result["remaining_material_answer_findings"][0]["defect"] == "Unchanged residual citation gap"
    assert Path(result["final_answer"]) == run.root / "answer-correction/answers-corrected.json"
    assert len(result["provider_execution_receipts"]) == 5
    assert result["answer_corrections"] == result["affected_rechecks"] == 1
    assert view["saved_result"]["remaining_material_answer_findings"] == result["remaining_material_answer_findings"]
    frozen = finite.read(run.root / "answer/freeze.json")
    assert finite.read(frozen["response"])["answers"][0] == finite.read(result["final_answer"])["answers"][0]
    result_path = run.root / "result.json"
    saved = finite.read(result_path)
    saved["answer_material_status"] = "no_open_material_answer_defects_reported"
    result_path.write_text(json.dumps(saved), encoding="utf-8")
    with pytest.raises(ValueError, match="saved material status differs"):
        closeout.collect(run.root)


@pytest.mark.parametrize("outcome,expected", [("inventory_counts_valid", "accepted"), ("inventory_counts_wrong", "rejected")])
def test_saved_recheck_uses_native_totals_without_approving_wrong_counts(tmp_path, outcome, expected):
    run, result = saved_correction_run(tmp_path, outcome)
    payload = closeout.collect(run.root)
    request = payload["correction_records"]["recheck_input"]
    assert request["program_verified_inventory"]["corpus_coverage"]["captured_item_count"] == 3
    assert result["answer_correction_status"] == expected
    assert len(result["provider_execution_receipts"]) == 5
    assert result["answer_corrections"] == result["affected_rechecks"] == 1
    if expected == "rejected":
        assert result["answer_material_status"] == "correction_rejected_original_requires_adjudication"
        assert result["affected_recheck_material_findings"][0]["status"] == "open"


def test_closeout_rederives_recheck_program_facts_even_with_rebound_prompt(tmp_path):
    run, _ = saved_correction_run(tmp_path, "inventory_counts_valid")
    path = run.root / "assessment-recheck/input.json"
    request = finite.read(path)
    request["program_verified_inventory"]["corpus_coverage"]["captured_item_count"] = 30
    path.write_text(json.dumps(request), encoding="utf-8")
    binding_path = run.root / "assessment-recheck/provider/job/binding.json"
    binding = finite.read(binding_path)
    prompt = Path(binding["binding"]["prompt_path"])
    prefix = prompt.read_text(encoding="utf-8").rstrip().rsplit("\n", 1)[0]
    prompt.write_text(prefix + "\n" + finite.render_evidence(request).rstrip().rsplit("\n", 1)[-1] + "\n", encoding="utf-8")
    binding["binding"]["prompt_sha256"] = hash_file(prompt)
    binding_path.write_text(json.dumps(binding), encoding="utf-8")
    receipt_path = run.root / "assessment-recheck/provider/attempts/job-attempt-001/execution_receipt.json"
    receipt = finite.read(receipt_path)
    receipt["prompt_sha256"] = hash_file(prompt)
    receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
    with pytest.raises(ValueError, match="recheck inventory facts differ from native packet"):
        closeout.collect(run.root)
