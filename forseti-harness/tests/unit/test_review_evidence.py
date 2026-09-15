"""Lossless transport cannot purchase economy by omitting inconvenient evidence."""
from copy import deepcopy
import json

import pytest

from judgment.review_evidence import compact_evidence, expand_evidence, compose_answer_patch, material_answer_findings
from runners import run_finite_semantic_consolidation as finite
from test_finite_semantic_consolidation import answer_fixture


def test_complete_roundtrip_retains_origins_conditions_opposition_and_literal_markers():
    text = "A repeated exact source quotation, kept once in transport, never counted as another origin. " * 3
    payload = {"sources": [
        {"id": "one", "origin": "actor-a", "text": text, "conditions": ["dry lips"], "relation": "supports"},
        {"id": "two", "origin": "actor-b", "text": text, "conditions": ["not drying"], "relation": "opposes"}],
        "heterogeneous": [{"nullable": None}, {}], "literal": [{"$text": text}, {"$text": text}],
        "distinct_types": [{"v": False}, {"v": 0}, {"v": 0.0}],
        "repeated_structure": {"one": {"text": text, "date": None}, "two": {"text": text, "date": None}},
        "scalars": [None, False, 0, "", [], {}, [1, 2]],
        "condition_lineage": [{"semantic_unit_ref": "one::u", "conditions": ["dry lips"]},
                              {"semantic_unit_ref": "two::u", "conditions": ["not drying"]}]}
    before = deepcopy(payload)
    compact = compact_evidence(payload)
    assert expand_evidence(json.loads(json.dumps(compact))) == payload == before
    assert json.dumps(expand_evidence(compact), sort_keys=True) == json.dumps(payload, sort_keys=True)
    assert list(compact["texts"].values()) == [text]
    assert compact["values"]  # Repeated literal source structures are transmitted once too.
    assert compact_evidence({"elsewhere": [text, text]})["texts"] == compact["texts"]
    # A cheaper-but-misleading renderer that drops the contrary row must fail equality.
    bad = deepcopy(compact)
    bad["data"]["sources"]["$table"]["rows"].pop()
    assert expand_evidence(bad) != payload


@pytest.mark.parametrize("severity,origin", [("minor", "current_answer"), ("major", "current_consolidation")])
def test_minor_or_inventory_only_finding_does_not_spend_answer_correction(tmp_path, severity, origin):
    run, answer = answer_fixture(tmp_path)
    path = run.root / "answer.json"
    finite.persist(path, answer)
    finite.persist(run.root / "answer/freeze.json", {"response": str(path)})
    finding = {"severity": severity, "status": "open", "introduced_at": origin,
               "artifact_refs": ["current_answer:one"]}
    assessment = {"material_findings": [finding]}
    before = deepcopy(assessment)
    run.job = lambda *a, **k: pytest.fail("nonmaterial answer finding launched correction")
    result = run.correct_and_recheck(answer, assessment, {})
    assert (result["answer_corrections"], result["affected_rechecks"]) == (0, 0)
    assert assessment == before
    if severity == "major":
        # A cross-reference to the answer does not move an inventory defect
        # into the answer; the reviewer's introduced_at judgment still owns it.
        assert result["remaining_material_answer_findings"] == []


@pytest.mark.parametrize("origin", ["uncertain", "historical_answer"])
def test_uncertain_origin_and_corrected_answer_major_remain_visible(origin):
    finding = {"severity": "major", "status": "open", "introduced_at": origin,
               "artifact_refs": ["corrected_answer:one"]}
    assert material_answer_findings([finding]) == []
    assert material_answer_findings([finding], for_correction=False) == [finding]


def test_patch_cannot_change_or_omit_unaffected_answer():
    original = {"answers": [{"question_id": "one", "answer": "bad"}, {"question_id": "two", "answer": "fixed"}]}
    patch = {"answers": [{"question_id": "one", "answer": "repaired"}]}
    assert compose_answer_patch(original, patch, {"one"})["answers"][1] == original["answers"][1]
    with pytest.raises(ValueError, match="exactly"):
        compose_answer_patch(original, {"answers": original["answers"]}, {"one"})


@pytest.mark.parametrize("missing_body", [False, True])
def test_repair_includes_opposition_and_recheck_all_named_source_bodies(tmp_path, missing_body):
    run, answer = answer_fixture(tmp_path)
    ids = ["known", "opposition", "check-only"]
    run.source = {"captured_items": [{"evidence_id": e, "text": e + " original source body"}
                                     for e in ids if not (missing_body and e == "check-only")]}
    run.bundle = {"evidence_units": [{"evidence_id": e} for e in ids]}
    run.verified = {"semantic_units": [{"semantic_unit_ref": e + "::u", "evidence_id": e} for e in ids]}
    run.questions["assessment_only"] = {"checks": [{"id": "contrast", "source_rows": ["known", "check-only"]}]}
    finding = {"severity": "major", "status": "open", "introduced_at": "current_answer",
               "artifact_refs": ["current_answer:one"], "source_refs": ["known"]}
    view = {"propositions": [{"semantic_relations": {"supports": ["known::u"], "opposes": ["opposition::u"]}}]}
    patch = {"schema_version": "finite_answer_v1", "answers": [{**answer["answers"][0], "answer": "corrected"}]}
    recheck = {"schema_version": "finite_source_assessment_v1", "inventory_coverage": "complete",
               "comparison": "fixture", "unassessed_material": "none", "overall_usefulness": "material issue remains",
               "check_results": [{"check_id": "contrast", "status": "fail", "source_refs": ids,
                                  "finding_refs": [], "explanation": "fixture"}],
               "material_findings": [{**finding, "defect": "still wrong", "effect": "misleads", "bounded_repair": "reject"}]}
    launches = []
    def job(name, prompt, schema):
        launches.append(name)
        packet = json.loads(prompt[prompt.index('{"format":'):])
        data = expand_evidence(packet)
        bodies = {r["evidence_id"] for r in data["complete_relevant_source_rows"]}
        assert {"known", "opposition"} <= bodies
        if "recheck" in name:
            assert set(ids) <= bodies
        path = run.root / (name + ".json")
        finite.persist(path, recheck if "recheck" in name else patch)
        return path
    run.job = job
    if missing_body:
        with pytest.raises(ValueError, match="check source bodies"):
            run.correct_and_recheck(answer, {"material_findings": [finding]}, view)
        assert launches == ["answer-correction/provider"]
    else:
        result = run.correct_and_recheck(answer, {"material_findings": [finding]}, view)
        assert result["answer_material_status"] == "material_defects_remain"
        assert len(launches) == 2
