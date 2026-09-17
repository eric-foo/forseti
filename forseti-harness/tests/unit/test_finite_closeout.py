"""Closeout must expose source meaning without claiming semantic acceptance."""
from copy import deepcopy
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
