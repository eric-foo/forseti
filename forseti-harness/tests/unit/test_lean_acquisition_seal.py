"""Exercise the actual seal consumer with checked lean packets, not fake units."""
from copy import deepcopy
import json

import pytest
import yaml

from judgment import lean_evidence_consolidation as lean
from judgment.semantic_evidence_integration import _sha256
from runners import run_phase_acquisition_seal_validation as seal_runner
from test_lean_evidence_consolidation import complete, fixture, respond
from test_phase_acquisition_seal_validation import (
    _artifact, _artifact_hash, _blocked_seal, _consumer_depth_ledger,
    _make_passing, _validate,
)


def _run(tmp_path, *, scoped=True, change_source=None, change_verdict=None, defect=False):
    source, commission, capacity = fixture()
    source.update(cycle_id="summer_fridays_confirmation", corpus_profile="phase_a_final_acquisition",
                  containers=[{"container_id": "capture", "source_artifact_id": "raw", "container_type": "published_object",
                               "captured_at": "2026-09-25", "captured_leaf_count": 4, "source_visible_total": "unavailable",
                               "completeness": "partial", "capture_boundary": "Only these four captured records; live total unknown."}])
    for row in source["captured_items"]:
        row.update(container_id="capture", accounting_reason="Captured original retained.", source_role="owned_source", source_family="owned_source")
    source["captured_items"][0]["text"] = "Summer Fridays balm costs USD24 at this US cutoff."
    source["captured_items"][1]["text"] = "e.l.f. balm costs USD10 at this US cutoff."
    if change_source:
        change_source(source)
    source.pop("source_sha256")
    source["source_sha256"] = _sha256(source)
    commission["questions"][0]["question"] = "Compare the captured sticker prices of these named products; do not infer customer preference."
    if scoped:
        commission["comparison_scope"] = {"q": {"axis_ids": ["price"], "subject_product_ids": ["sf-lbb"],
                                                  "comparator_product_ids": ["elf-glow-reviver"]}}
    capacity["max_rows_per_slice"] = 4
    inventory = lean._source_inventory(source)
    refs = [row["body_ref"] for row in inventory["records"][:2]]

    def semantic(request):
        response = respond(request)
        if "answers" in response and scoped:
            for answer in response["answers"]:
                verdict = {"axis_id": "price", "choice_posture": "competitor_advantage", "claim_kind": "observable_fact",
                           "support_posture": "directly_observed", "conflict_posture": "none_observed",
                           "why": "The captured e.l.f. sticker price is lower at this cutoff.",
                           "supporting_refs": refs, "opposing_refs": [], "context_refs": [],
                           "conditions": ["Captured US sticker prices only."], "limits": "Sizes are not normalized; no preference or efficacy conclusion."}
                if change_verdict:
                    change_verdict(verdict)
                answer.update(answer=verdict["why"], comparison_verdicts=[verdict])
        if defect and request["phase"] in {"lean_review", "lean_recheck"}:
            response["exceptions"] = [{"severity": "material", "question_ids": ["q"], "finding_ids": [],
                                        "source_refs": [refs[0]], "reason": "The price qualification remains incorrect."}]
        return response

    return complete((source, commission, capacity), tmp_path / "run", tmp_path, semantic)


def _packet(tmp_path, **kwargs):
    state, requests = _run(tmp_path, **kwargs)
    assert state["status"] in {"LEAN_EVIDENCE_CONSOLIDATION_CHECKED", "LEAN_EVIDENCE_CONSOLIDATION_REQUIRES_REVISION"}, state
    return lean.read(state["packet_path"]), requests


def _integration(tmp_path, packet, *, corpus=None, route="1.7.1"):
    ref = _artifact(tmp_path, "lean-packet.json", json.dumps(packet))
    value = {"status": "completed", "view": ref, "corpus_sha256": corpus or packet["source_sha256"],
             "unresolved_material_evidence_ids": []}
    findings = []
    index = seal_runner._validate_semantic_evidence_integration(
        value, seal={"cycle_id": "summer_fridays_confirmation"}, repo_root=tmp_path,
        valid_pass=True, route_version=route, findings=findings)
    return value, index, findings


def _explanation(packet):
    verdict = packet["answers"][0]["comparison_verdicts"][0]
    refs = sorted({ref for relation in lean.RELATIONS for ref in verdict[relation]})
    return {"status": "observed", "summary": packet["answers"][0]["answer"],
            "final_comparator_role": "value_substitute", "role_rationale": "The commissioned price comparison is source bounded.",
            "role_evidence_refs": refs,
            "axis_findings": [{**{key: verdict[key] for key in ("axis_id", "choice_posture", "why", "conditions", "limits")},
                               "evidence_refs": refs, "answer_refs": ["answer:q"]}]}


def _choice(explanation, index, *, subject="sf-lbb", competitor="elf-glow-reviver"):
    findings = []
    seal_runner._validate_comparator_choice_explanation(
        explanation, candidate_id="cand-elf", shared_axis_ids=["price"], promoted=True,
        subject_product_id=subject, competitor_product_id=competitor,
        proposition_index=index, findings=findings)
    return findings


def _bind_final_review(tmp_path, seal, packet):
    ref = seal["evidence_depth_ledger"]
    review = {"schema_version": "acquisition_final_semantic_source_review_v1", "reviewed_ledger_sha256": ref["sha256"],
              "reviewed_view_sha256": seal["understanding_route"]["semantic_evidence_integration"]["view"]["sha256"],
              "corpus_sha256": packet["source_sha256"], "review_status": "complete", "adjudication_status": "accepted",
              "unresolved_material_findings": []}
    ref["final_source_review"] = _artifact(tmp_path, "lean-final-source-review.md", "```yaml\n" +
                                         yaml.safe_dump({"final_semantic_source_review": review}) + "```\n")


def _full_seal(tmp_path, packet):
    seal = _blocked_seal(tmp_path)
    seal["evidence_depth_ledger"] = _consumer_depth_ledger(tmp_path)
    integration, _, findings = _integration(tmp_path, packet)
    assert not findings
    seal["understanding_route"]["semantic_evidence_integration"] = integration
    candidate = seal["understanding_route"]["comparator_closure"]["candidates"][0]
    candidate["competitive_choice_explanation"] = _explanation(packet)
    route = next(row for row in seal["route_job_accounting"] if row["route_id"] == "semantic_evidence_integration")
    route.update(terminal_artifact_locator=integration["view"]["locator"], terminal_artifact_sha256=integration["view"]["sha256"])
    _bind_final_review(tmp_path, seal, packet)
    return _make_passing(seal)


def test_checked_scoped_answer_reaches_full_seal_without_atomic_fictions(tmp_path):
    packet, requests = _packet(tmp_path)
    review = next(r for r in requests if r["phase"] == "lean_review")
    assert review["payload"]["answers"] == packet["answers"]
    assert "comparison_verdicts" in review["prompt"]
    assert any(o["text"] == "Unrelated greeting." for o in review["payload"]["observations"])
    _, index, findings = _integration(tmp_path, packet)
    assert findings == [] and set(index) == {"answer:q"}
    assert "proposition_id" not in index["answer:q"]
    assert _choice(_explanation(packet), index) == []
    assert _validate(tmp_path, _full_seal(tmp_path, packet)) == []


@pytest.mark.parametrize("mutation,expected", [
    ("missing_ledger_review", "final_semantic_source_review_missing_binding"),
    ("collection_frontier", "serp_source_frontier"),
])
def test_checked_packet_does_not_replace_ledger_review_or_collection_guards(tmp_path, mutation, expected):
    packet, _ = _packet(tmp_path)
    seal = _full_seal(tmp_path, packet)
    if mutation == "missing_ledger_review":
        seal["evidence_depth_ledger"].pop("final_source_review")
    else:
        ref = seal["evidence_depth_ledger"]
        path = tmp_path / ref["locator"]
        ledger = json.loads(path.read_text(encoding="utf-8"))
        ledger["serp_source_frontier"]["row_classifications"] = []
        path.write_text(json.dumps(ledger), encoding="utf-8")
        ref["sha256"] = _artifact_hash(path)
        _bind_final_review(tmp_path, seal, packet)
    assert any(expected in finding for finding in _validate(tmp_path, seal))


@pytest.mark.parametrize("mutation,expected", [
    ("corpus", "semantic_integration_corpus_hash_mismatch"),
    ("profile", "invalid_semantic_integration_corpus_profile"),
    ("capture_count", "semantic_integration_capture_envelope_leaf_mismatch"),
    ("historical_route", "lean_semantic_integration_requires_current_route"),
    ("review_defect", "lean_semantic_integration_requires_checked_output"),
])
def test_lean_seal_rejects_wrong_binding_capture_or_review_state(tmp_path, mutation, expected):
    def source_change(source):
        if mutation == "profile":
            source["corpus_profile"] = "bounded_regression_slice"
        if mutation == "capture_count":
            source["containers"][0]["captured_leaf_count"] += 1
    packet, _ = _packet(tmp_path, change_source=source_change, defect=mutation == "review_defect")
    _, _, findings = _integration(tmp_path, packet, corpus="0" * 64 if mutation == "corpus" else None,
                                 route="1.7" if mutation == "historical_route" else "1.7.1")
    assert expected in findings


@pytest.mark.parametrize("mutation,expected", [
    ("direction", "reviewed_verdict_mismatch"), ("conditions", "reviewed_verdict_mismatch"),
    ("evidence", "reviewed_evidence_mismatch"), ("pair", "commission_scope_mismatch"),
    ("axis", "commission_scope_mismatch"), ("fake_atomic", "cannot_claim_atomic_proposition_authority"),
])
def test_comparator_cannot_reinterpret_the_exact_reviewed_verdict(tmp_path, mutation, expected):
    packet, _ = _packet(tmp_path)
    _, index, findings = _integration(tmp_path, packet)
    assert findings == []
    explanation = _explanation(packet)
    row = explanation["axis_findings"][0]
    if mutation == "direction":
        row["choice_posture"] = "subject_advantage"
    elif mutation == "conditions":
        row["conditions"] = []
    elif mutation == "evidence":
        row["evidence_refs"] = ["e999"]
    elif mutation == "axis":
        row["axis_id"] = "hydration"
    elif mutation == "fake_atomic":
        row["proposition_refs"] = ["fake-verified-unit"]
    failures = _choice(explanation, index, competitor="another-product" if mutation == "pair" else "elf-glow-reviver")
    assert any(expected in finding for finding in failures)


def test_generic_checked_answer_is_not_comparison_authority(tmp_path):
    packet, _ = _packet(tmp_path, scoped=False)
    _, index, findings = _integration(tmp_path, packet)
    assert findings == []
    explanation = {"status": "observed", "summary": "Invented advantage.", "final_comparator_role": "direct_peer",
                   "role_rationale": "Claimed role.", "role_evidence_refs": ["e0"],
                   "axis_findings": [{"axis_id": "price", "choice_posture": "subject_advantage", "why": "Claimed direction.",
                                      "conditions": [], "limits": "Claimed limit.", "evidence_refs": ["e0"], "answer_refs": ["answer:q"]}]}
    assert any("commission_scope_mismatch" in finding for finding in _choice(explanation, index))


@pytest.mark.parametrize("mutation,expected", [
    ("unknown", "lacks attributed support"), ("same_origin", "lacks two credited origins"),
    ("role", "exceeds source-role competence"),
])
def test_comparison_source_competence_and_independence_are_not_actor_authored(tmp_path, mutation, expected):
    def source_change(source):
        if mutation == "unknown":
            for row in source["captured_items"][:2]:
                row.pop("independence_key")
                row["independence_posture"] = "unavailable"
        elif mutation == "same_origin":
            source["captured_items"][1]["independence_key"] = source["captured_items"][0]["independence_key"]
    def verdict_change(verdict):
        if mutation == "same_origin":
            verdict["support_posture"] = "independently_repeated"
        elif mutation == "role":
            verdict.update(claim_kind="customer_experience", support_posture="independently_repeated")
    state, requests = _run(tmp_path, change_source=source_change, change_verdict=verdict_change)
    assert state["status"] == "SEMANTIC_ADVANCE_BLOCKED" and expected in state["error"]
    assert [request["phase"] for request in requests] == ["lean_read", "lean_synthesis", "lean_repair"]


def test_compiler_comparison_failure_repairs_before_paid_review_and_still_rechecks(tmp_path):
    authored = []

    def once(verdict):
        if not authored:
            verdict.update(claim_kind="customer_experience", support_posture="independently_repeated")
        authored.append(deepcopy(verdict))

    state, requests = _run(tmp_path, change_verdict=once)
    assert state["status"] == "LEAN_EVIDENCE_CONSOLIDATION_CHECKED", state
    phases = [r["phase"] for r in requests]
    assert phases == ["lean_read", "lean_synthesis", "lean_repair", "lean_recheck"]
    repair = next(r for r in requests if r["phase"] == "lean_repair")
    assert repair["payload"]["target_questions"] == ["q"]
    assert "source-role competence" in repair["payload"]["exceptions"][0]["reason"]
    packet = lean.validate_packet(lean.read(state["packet_path"]))
    assert packet["answers"][0]["comparison_verdicts"][0]["claim_kind"] == "observable_fact"
    assert packet["review"]["responses"][0]["phase"] == "lean_recheck"


@pytest.mark.parametrize("mutation", ["isolated", "insufficient", "unchecked", "mixed", "wrong_axis"])
def test_unsupported_or_misqualified_direction_fails_before_acceptance(tmp_path, mutation):
    def change(verdict):
        if mutation in {"isolated", "insufficient"}:
            verdict["support_posture"] = mutation
        elif mutation == "unchecked":
            verdict["conflict_posture"] = "not_checked"
        elif mutation == "mixed":
            verdict["conflict_posture"] = "mixed"
        else:
            verdict["axis_id"] = "hydration"
    with pytest.raises(ValueError, match="comparison"):
        _run(tmp_path, change_verdict=change)
