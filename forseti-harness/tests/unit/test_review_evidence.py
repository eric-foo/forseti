"""Lossless transport cannot purchase economy by omitting inconvenient evidence."""
from copy import deepcopy
import json

import pytest

from judgment.review_evidence import compact_evidence, expand_evidence, compose_answer_patch, material_answer_findings
from runners import run_finite_semantic_consolidation as finite
from test_finite_semantic_consolidation import answer_fixture, _keyed_assessment


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
def test_minor_or_consolidation_origin_finding_does_not_spend_answer_correction(tmp_path, severity, origin):
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
        # Origin does not discharge an explicitly answer-relevant open defect.
        assert result["remaining_material_answer_findings"] == [finding]
        assert result["answer_material_status"] == "material_defects_remain"


@pytest.mark.parametrize("origin", ["uncertain", "historical_answer"])
def test_uncertain_origin_and_corrected_answer_major_remain_visible(origin):
    finding = {"severity": "major", "status": "open", "introduced_at": origin,
               "artifact_refs": ["corrected_answer:one"]}
    assert material_answer_findings([finding]) == []
    assert material_answer_findings([finding], for_correction=False) == [finding]


@pytest.mark.parametrize("reference", [
    "corrected_affected_answers:one", "corrected_affected_answers.evidence_refs", "unrecognized_label", "",
])
def test_current_answer_defect_cannot_disappear_through_reference_spelling(reference):
    # The real recheck used its input field name, not the filter's corrected_answer prefix.
    finding = {"severity": "blocker", "status": "open", "introduced_at": "current_answer",
               "artifact_refs": [reference]}
    assert material_answer_findings([finding], for_correction=False) == [finding]
    assert material_answer_findings([finding]) == []  # Unknown routing never guesses a question.


def test_patch_cannot_change_or_omit_unaffected_answer():
    original = {"answers": [{"question_id": "one", "answer": "bad"}, {"question_id": "two", "answer": "fixed"}]}
    patch = {"answers": [{"question_id": "one", "answer": "repaired"}]}
    assert compose_answer_patch(original, patch, {"one"})["answers"][1] == original["answers"][1]
    with pytest.raises(ValueError, match="exactly"):
        compose_answer_patch(original, {"answers": original["answers"]}, {"one"})


def test_unknown_inline_citation_uses_mandatory_repair_and_preserves_other_answers(tmp_path):
    run, original = answer_fixture(tmp_path)
    run.bundle = {"evidence_units": [{"evidence_id": "source:one"}]}
    run.verified = {"semantic_units": [{"semantic_unit_ref": "source:one::purchase-despite-price",
                                       "evidence_id": "source:one"}]}
    run.source = {"captured_items": [{"evidence_id": "source:one", "text": "Bought despite price."}]}
    run.questions["assessment_only"] = {"checks": []}
    for row in original["answers"]:
        row["evidence_refs"] = ["source:one"]
    original["answers"][0]["answer"] = "A report (source:one::purchase_despite_price)."
    with pytest.raises(finite.UnknownAnswerEvidence):
        finite.check_answer(original, run.questions["questions"], run.bundle, run.verified)
    path = run.root / "original.json"
    finite.persist(path, original)
    finite.persist(run.root / "answer/freeze.json", {"response": str(path)})
    finite.persist(run.root / "assessment/result.json", {"response": "fixture-review", "response_sha256": "fixture"})
    assessment = {"schema_version": "finite_source_assessment_v3", "material_findings": [],
        "answer_repairs": {"answer_sha256": finite.answer_identity(original), "edits": [
            {"question_id": "one", "field": "answer", "before": "source:one::purchase_despite_price",
             "after": "source:one::purchase-despite-price", "source_refs": ["source:one::purchase-despite-price"]}]}}
    recheck = _keyed_assessment({"schema_version": "finite_source_assessment_v4", "answer_comparison": None,
        "inventory_coverage": "fixture", "comparison": "fixture", "unassessed_material": "none",
        "overall_usefulness": "supported", "material_findings": [], "check_results": []}, [])
    launches = []
    def job(name, prompt, schema):
        launches.append(name)
        assert name == "assessment-recheck/provider"
        assert 'source:one::purchase_despite_price' in prompt
        response = run.root / "recheck.json"
        finite.Draft202012Validator(schema).validate(recheck)
        finite.persist(response, recheck)
        return response
    run.job = job
    result = run.correct_and_recheck(original, assessment, {"propositions": []})
    assert result["answer_correction_status"] == "accepted"
    corrected = finite.read(result["final_answer"])
    assert corrected["answers"][0]["answer"] == "A report (source:one::purchase-despite-price)."
    assert corrected["answers"][1] == original["answers"][1]
    assert finite.read(path) == original
    assert launches == ["assessment-recheck/provider"]
    finite.check_answer(corrected, run.questions["questions"], run.bundle, run.verified)


@pytest.mark.parametrize("missing_body", [False, True])
def test_repair_includes_opposition_and_recheck_all_named_source_bodies(tmp_path, missing_body):
    run, answer = answer_fixture(tmp_path)
    original_path = run.root / "original.json"
    finite.persist(original_path, answer)
    finite.persist(run.root / "answer/freeze.json", {"response": str(original_path)})
    ids = ["known", "opposition", "check-only"]
    run.source = {"captured_items": [{"evidence_id": e, "text": e + " original source body"}
                                     for e in ids if not (missing_body and e == "check-only")]}
    run.bundle = {"evidence_units": [{"evidence_id": e} for e in ids]}
    run.verified = {"semantic_units": [{"semantic_unit_ref": e + "::u", "evidence_id": e} for e in ids]}
    run.questions["assessment_only"] = {"checks": [{"id": "contrast", "source_rows": ["known", "check-only"]}]}
    finding = {"severity": "major", "status": "open", "introduced_at": "current_answer",
               "artifact_refs": ["current_answer:one"], "source_refs": ["known"]}
    view = {"propositions": [{"semantic_relations": {"supports": ["known::u"], "opposes": ["opposition::u"]}}]}
    assessment = {"schema_version": "finite_source_assessment_v3", "material_findings": [finding],
        "answer_repairs": {"answer_sha256": finite.answer_identity(answer), "edits": [
            {"question_id": "one", "field": "answer", "before": "bounded", "after": "corrected",
             "source_refs": ["known"]}]}}
    finite.persist(run.root / "assessment/result.json", {"response": "fixture-review", "response_sha256": "fixture"})
    recheck = {"schema_version": "finite_source_assessment_v4", "answer_comparison": None, "inventory_coverage": "complete",
               "comparison": "fixture", "unassessed_material": "none", "overall_usefulness": "material issue remains",
               "check_results": [{"check_id": "contrast", "scope": "answer", "status": "fail", "source_refs": ids,
                                  "finding_refs": [], "explanation": "fixture"}],
               "material_findings": [{**finding, "defect": "still wrong", "effect": "misleads", "bounded_repair": "reject"}]}
    launches = []
    def job(name, prompt, schema):
        launches.append(name)
        assert name == "assessment-recheck/provider"
        packet = json.loads(prompt[prompt.index('{"format":'):])
        data = expand_evidence(packet)
        bodies = {r["evidence_id"] for r in data["complete_relevant_source_rows"]}
        assert {"known", "opposition"} <= bodies
        assert set(ids) <= bodies
        path = run.root / (name + ".json")
        wire_recheck = _keyed_assessment(recheck, ["contrast"])
        finite.Draft202012Validator(schema).validate(wire_recheck)
        finite.persist(path, wire_recheck)
        return path
    run.job = job
    if missing_body:
        with pytest.raises(ValueError, match="check source bodies"):
            run.correct_and_recheck(answer, assessment, view)
        assert launches == []
    else:
        result = run.correct_and_recheck(answer, assessment, view)
        assert result["answer_material_status"] == "correction_rejected_original_requires_adjudication"
        assert finite.read(result["final_answer"]) == answer
        assert result["affected_recheck_material_findings"] == recheck["material_findings"]
        assert launches == ["assessment-recheck/provider"]


def comparison_for_test(original, candidate, assessment, recheck, request, excerpts):
    """Synthetic source-comparison input, never a historical model judgment."""
    from judgment.review_evidence import answer_identity, material_answer_findings
    sources = {r["evidence_id"]: r for r in request["complete_relevant_source_rows"]}
    units = {u["semantic_unit_ref"]: u["evidence_id"] for u in request["verified_units"]}
    def support(refs):
        return {"source_refs": refs, "explanation": "Synthetic source-checked comparison for the controlled test.",
                "source_observations": [{"source_ref": r, "excerpt": sources[units.get(r, r)]["text"]} for r in refs]}
    residuals = material_answer_findings(recheck["material_findings"], for_correction=False)
    indices = [i for i, f in enumerate(recheck["material_findings"]) if f in residuals]
    return {"original_answer_sha256": answer_identity(original), "candidate_answer_sha256": answer_identity(candidate),
        "affected_question_ids": [q["id"] for q in request["affected_questions"]],
        "changed_claims_verdict": "no_new_or_worsened_material_defect",
        "repair_checks": [{"edit_index": i, "verdict": "verified", **support(e["source_refs"])}
                          for i, e in enumerate(assessment["answer_repairs"]["edits"])],
        "nomination_checks": [{"nomination_index": i, "disposition": "repaired", "remaining_finding_indices": [],
                               **support(f["source_refs"])} for i, f in enumerate(material_answer_findings(assessment["material_findings"]))],
        "residual_checks": [{"finding_index": i, "question_id": excerpts[i][0], "field": "answer",
            "original_excerpt": excerpts[i][1], "candidate_excerpt": excerpts[i][1], "verdict": "unchanged_preexisting",
            **support(recheck["material_findings"][i]["source_refs"])} for i in indices],
        "failed_check_links": [{"check_id": c["check_id"], "finding_indices": indices} for c in recheck["check_results"]
                               if c["status"] in {"fail", "uncertain"} and c["scope"] != "upstream_only"]}


def improvement_fixture():
    from judgment.review_evidence import answer_identity
    original = {"answers": [{"question_id": "a", "answer": "Beta beats Alpha. Residual old claim.", "limits": "", "evidence_refs": ["source"]},
                            {"question_id": "b", "answer": "Untouched.", "limits": "", "evidence_refs": ["source"]}]}
    candidate = deepcopy(original)
    candidate["answers"][0]["answer"] = "Alpha beats Beta. Residual old claim."
    finding = {"severity": "major", "status": "open", "introduced_at": "current_answer", "artifact_refs": ["current_answer:a"],
               "source_refs": ["source"], "defect": "Comparator reversed", "effect": "Wrong meaning", "bounded_repair": "Fix comparator"}
    assessment = {"material_findings": [finding, {**finding, "artifact_refs": ["unroutable_outside"], "defect": "Outside scope"}],
                  "answer_repairs": {"answer_sha256": answer_identity(original), "edits": [
                      {"question_id": "a", "field": "answer", "before": "Beta beats Alpha", "after": "Alpha beats Beta", "source_refs": ["source"]}]}}
    recheck = {"schema_version": "finite_source_assessment_v4", "material_findings": [{**finding, "defect": "Residual traceability", "introduced_at": "historical_answer"}],
               "check_results": [{"check_id": "trace", "status": "fail", "scope": "answer", "source_refs": ["source"], "finding_refs": [], "explanation": "Old gap"}]}
    request = {"affected_questions": [{"id": "a"}], "original_affected_answers": original["answers"][:1],
               "corrected_affected_answers": candidate["answers"][:1], "nominations_to_verify_against_sources": [finding],
               "exact_repairs": assessment["answer_repairs"], "complete_relevant_source_rows": [{"evidence_id": "source", "text": "Alpha beats Beta. Old claim is observed."}], "verified_units": []}
    recheck["answer_comparison"] = comparison_for_test(original, candidate, assessment, recheck, request, {0: ("a", "Residual old claim.")})
    return original, candidate, assessment, recheck, request


def test_verified_improvement_keeps_residual_and_outside_scope_visible():
    from judgment.review_evidence import correction_selection
    args = improvement_fixture()
    before = deepcopy(args)
    result = correction_selection(*args)
    assert result["answer_correction_status"] == "selected_requires_adjudication"
    assert result["answer_material_status"] == "selected_answer_requires_adjudication"
    assert result["remaining_material_answer_findings"] == [args[2]["material_findings"][1], args[3]["material_findings"][0]]
    assert args == before


@pytest.mark.parametrize("defect", ["reversed_comparator", "unverified_repair", "stale", "missing", "legacy", "uncertain", "changed_excerpt", "invented_source",
                                   "omitted_residual", "omitted_nomination", "uncertain_scope", "uncertain_check", "omitted_check", "untouched_changed", "citation_removed"])
def test_partial_selection_refuses_missing_or_regressing_comparison(defect):
    from judgment.review_evidence import correction_selection
    original, candidate, assessment, recheck, request = improvement_fixture()
    comparison = recheck["answer_comparison"]
    if defect == "reversed_comparator":
        comparison["changed_claims_verdict"] = "new_or_worsened_material_defect"
    elif defect == "unverified_repair":
        comparison["repair_checks"][0]["verdict"] = "unverified"
    elif defect == "stale":
        comparison["candidate_answer_sha256"] = "stale"
    elif defect == "missing":
        recheck["answer_comparison"] = None
    elif defect == "legacy":
        recheck["schema_version"] = "finite_source_assessment_v2"
        recheck.pop("answer_comparison")
    elif defect == "uncertain":
        comparison["residual_checks"][0]["verdict"] = "uncertain"
    elif defect == "changed_excerpt":
        comparison["residual_checks"][0]["candidate_excerpt"] = "Different meaning"
    elif defect == "invented_source":
        comparison["repair_checks"][0]["source_observations"][0]["excerpt"] = "Beta beats Alpha"
    elif defect == "omitted_residual":
        comparison["residual_checks"] = []
    elif defect == "omitted_nomination":
        comparison["nomination_checks"] = []
    elif defect == "uncertain_scope":
        recheck["check_results"][0]["scope"] = "unknown"
    elif defect == "uncertain_check":
        recheck["check_results"][0]["status"] = "uncertain"
    elif defect == "omitted_check":
        comparison["failed_check_links"] = []
    elif defect == "untouched_changed":
        candidate["answers"][1]["answer"] = "Changed without authority"
    elif defect == "citation_removed":
        candidate["answers"][0]["evidence_refs"] = []
        from judgment.review_evidence import answer_identity
        comparison["candidate_answer_sha256"] = answer_identity(candidate)
    result = correction_selection(original, candidate, assessment, recheck, request)
    assert result["answer_correction_status"] == "rejected"
    assert result["remaining_material_answer_findings"] == assessment["material_findings"]
