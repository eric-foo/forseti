"""Structural trajectories, not a semantic-quality oracle or model-cost proof."""
from copy import deepcopy
import json

import pytest

from judgment import lean_evidence_consolidation as lean
from judgment.semantic_evidence_integration import _sha256


def count(text):
    return len(text.encode("utf-8"))


def fixture(size=4):
    context = {"text": "I received it as a gift and intend to finish to avoid waste, despite disliking the scent.",
               "source_artifact_id": "raw", "source_ref": "post/1", "context_type": "post_text"}
    rows = []
    for i in range(size):
        text, role = [("Comfortable in winter; I used it again.", "community_post"),
                      ("The scent gave me a headache; I stopped using it.", "customer_review"),
                      ("Our product promises brighter-looking skin.", "owned_claim"),
                      ("Unrelated greeting.", "community_post")][i % 4]
        rows.append({"evidence_id": "original-" + str(i), "text": text, "source_artifact_id": "raw",
                     "source_ref": "source/" + str(i), "source_role": role, "source_family": role,
                     "independence_key": "actor-" + str(i), "independence_posture": "credited",
                     "accounting_disposition": "assess", "product_candidates": [],
                     "product_context": [deepcopy(context)] if i in (0, 1) else []})
    source = {"schema_version": "semantic_evidence_source_v3", "captured_items": rows,
              "source_artifacts": [{"artifact_id": "raw", "locator": "fixture.json", "sha256": "a" * 64}]}
    source["source_sha256"] = _sha256(source)
    commission = {"questions": [{"id": "q", "question": "Why do consumers continue or avoid this product, versus brand positioning?"}],
                  "assessment_only": {"checks": [{"id": "opposition", "source_rows": ["original-1"],
                                                     "expectation": "Preserve stopped use and the scent condition."}]}}
    capacity = {"encoding": "fixture_bytes", "effective_context_tokens": 100000,
                "output_reserve_tokens": 20000, "other_overhead_reserve_tokens": 1000, "max_rows_per_slice": 1}
    return source, commission, capacity


def finding(refs, statement, *, inputs=None):
    value = {"question_ids": ["q"], "statement": statement, "supporting_refs": refs,
             "opposing_refs": [], "context_refs": [], "conditions": "Source-specific conditions remain.",
             "limits": "Reported experience or attributed positioning only; no market causation."}
    if inputs is not None:
        value["input_refs"] = inputs
    return value


def respond(request):
    p, phase = request["payload"], request["phase"]
    response = {"input_sha256": lean.digest(p)}
    if phase == "lean_read":
        observations = {o["ref"]: o for o in p["observations"]}
        findings, unused = [], []
        for row in p["records"]:
            body = observations[row["body_ref"]]
            if body["text"] == "Unrelated greeting.":
                unused.append({"row_id": row["row_id"], "reason": "Greeting has no relevance to the questions."})
            else:
                value = finding([row["body_ref"]], body["text"])
                value["context_refs"] = row["context_refs"]
                findings.append(value)
        response.update(findings=findings, unused_rows=unused)
    elif phase == "lean_synthesis":
        refs = sorted({r for f in p["inputs"] for role in lean.RELATIONS for r in f[role]})
        findings = [finding(refs, "Consumer experience is conditional and mixed; stated brand promises are positioning.",
                            inputs=[f["input_ref"] for f in p["inputs"]])] if p["inputs"] else []
        response.update(findings=findings, unused_inputs=[])
        if p["final"]:
            response["answers"] = [{"question_id": "q", "answer": "Continued use and avoidance coexist under different conditions. Brand promises do not demonstrate consumer outcomes.",
                                     "evidence_refs": refs, "limits": "Capture and identity limits remain; no causal conclusion."}]
    elif phase == "lean_repair":
        response.update(replacements=[{"finding_id": fid, "finding": finding(p["allowed_refs"], "Corrected source-bounded finding.")}
                                      for fid in p["target_findings"]], remove_finding_ids=[], new_findings=[],
                        answers=[{"question_id": q, "answer": "Corrected answer preserves the material source qualification.",
                                  "evidence_refs": p["allowed_refs"], "limits": "No causal or prevalence claim."} for q in p["target_questions"]])
    else:
        response.update(reviewed_claim_ids=p["claim_ids"], reviewed_rows=[r["row_id"] for r in p["records"]],
                        reviewed_checks=[c["id"] for c in p["checks"]], exceptions=[])
    return response


def publish(info, response, tmp_path):
    path = tmp_path / "candidate.json"
    path.write_text(json.dumps(response), encoding="utf-8")
    return lean.submit(info["job_path"], info["job_sha256"], path, count)


def complete(args, root, tmp_path, responder=respond):
    seen = []
    for _ in range(30):
        state = lean.advance(*args, root, count=count)
        if not state["judgment_requests"]:
            return state, seen
        for info in state["judgment_requests"]:
            request = lean.read(info["job_path"])
            seen.append(request)
            publish(info, responder(request), tmp_path)
    raise AssertionError("lean route did not terminate")


def test_mixed_source_multibatch_consumer_and_immutable_restart(tmp_path):
    args = fixture()
    state, seen = complete(args, tmp_path / "run", tmp_path)
    assert state["status"] == "LEAN_EVIDENCE_CONSOLIDATION_CHECKED", state
    assert len([r for r in seen if r["phase"] == "lean_read"]) == 4
    synthesis = next(r for r in seen if r["phase"] == "lean_synthesis")
    assert "stopped using" in lean.compact(synthesis["payload"]["inputs"])
    assert "promises" in lean.compact(synthesis["payload"]["inputs"])
    reviews = [r for r in seen if r["phase"] == "lean_review"]
    assert len(reviews) == 4
    assert any("Unrelated greeting" in lean.compact(r["payload"]["observations"]) for r in reviews)
    assert len({r["payload"]["answer_sha256"] for r in reviews}) == 1
    assert sum(bool(r["payload"]["checks"]) for r in reviews) == 1
    packet = lean.validate_packet(lean.read(state["packet_path"]))
    assert packet["source"] == args[0]
    shared = [r for r, m in packet["registry"].items() if m["kind"] == "post_text"]
    assert len(shared) == 1
    assert packet["registry"][shared[0]]["origin_ref"] is None
    assert len(packet["registry"][shared[0]]["locations"]) == 2
    assert "avoid waste" in lean.resolve_refs(packet, shared)[0]["text"]
    assert packet["review"]["all_originals_checked"] is True
    assert packet["review"]["exhaustive_recall_claim"] is False
    assert packet["findings"][0]["accounting"]["supporting_refs"]["known_origin_count"] == 3
    before = {str(p.relative_to(tmp_path / "run")): p.read_bytes() for p in (tmp_path / "run").rglob("*") if p.is_file()}
    repeated, calls = complete(args, tmp_path / "run", tmp_path)
    assert repeated == state and calls == []
    assert before == {str(p.relative_to(tmp_path / "run")): p.read_bytes() for p in (tmp_path / "run").rglob("*") if p.is_file()}


def test_whole_original_may_support_and_oppose_a_conditional_finding(tmp_path):
    source, commission, capacity = fixture(1)
    source["captured_items"][0]["text"] = "I like Vanilla, but Iced Coffee sometimes overpowers me."
    source.pop("source_sha256")
    source["source_sha256"] = _sha256(source)
    commission.pop("assessment_only")

    def mixed(request):
        response = respond(request)
        if request["phase"] in {"lean_read", "lean_synthesis"}:
            response["findings"][0]["opposing_refs"] = ["e0"]
            response["findings"][0]["statement"] = "Variant preference is mixed: Vanilla is liked; Iced Coffee can overpower."
        return response

    state, requests = complete((source, commission, capacity), tmp_path / "run", tmp_path, mixed)
    assert state["status"] == "LEAN_EVIDENCE_CONSOLIDATION_CHECKED", state
    review = next(r for r in requests if r["phase"] == "lean_review")
    assert review["payload"]["findings"][0]["opposing_refs"] == ["e0"]
    packet = lean.validate_packet(lean.read(state["packet_path"]))
    accounting = packet["findings"][0]["accounting"]
    # Relation totals overlap: a consumer's overall origin count is their union.
    origins = {origin for relation in accounting.values() for origin in relation["known_origin_refs"]}
    assert origins == {"o0"}
    assert accounting["supporting_refs"]["known_origin_count"] == accounting["opposing_refs"]["known_origin_count"] == 1


def test_shared_context_does_not_turn_an_excluded_body_into_double_accounting(tmp_path):
    source, commission, capacity = fixture(2)
    source["captured_items"][1]["text"] = "Unrelated greeting."
    source.pop("source_sha256")
    source["source_sha256"] = _sha256(source)
    capacity["max_rows_per_slice"] = 4
    state, requests = complete((source, commission, capacity), tmp_path / "run", tmp_path)
    assert state["status"] == "LEAN_EVIDENCE_CONSOLIDATION_CHECKED", state
    request = next(r for r in requests if r["phase"] == "lean_read")
    response = respond(request)
    assert response["unused_rows"][0]["row_id"] == "r1"
    assert request["payload"]["records"][1]["context_refs"] == response["findings"][0]["context_refs"]
    response["findings"][0]["supporting_refs"].append(request["payload"]["records"][1]["body_ref"])
    lean.validate_response(request, response, count)
    response["unused_rows"].append(deepcopy(response["unused_rows"][0]))
    with pytest.raises(ValueError, match="read row coverage differs"):
        lean.validate_response(request, response, count)


def test_redundant_unused_label_cannot_hide_omission_or_mint_origin_credit(tmp_path):
    source, commission, capacity = fixture()
    capacity["max_rows_per_slice"] = 4
    state = lean.advance(source, commission, capacity, tmp_path / "run", count=count)
    request = lean.read(state["judgment_requests"][0]["job_path"])
    response = respond(request)
    before = lean._compile_findings(response["findings"], lean._source_inventory(source)["registry"])
    response["unused_rows"].append({"row_id": "r0", "reason": "Already covered; no additional independent contribution."})
    lean.validate_response(request, response, count)
    assert lean._compile_findings(response["findings"], lean._source_inventory(source)["registry"]) == before
    response["findings"].pop()  # The owned-source row has no shared context to cover it.
    with pytest.raises(ValueError, match="read row coverage differs"):
        lean.validate_response(request, response, count)


def test_known_prose_citation_is_compiled_before_exact_answer_review(tmp_path):
    def omitted_flat_ref(request):
        response = respond(request)
        if request["phase"] == "lean_synthesis" and request["payload"]["final"]:
            answer = response["answers"][0]
            ref = answer["evidence_refs"].pop()
            answer["limits"] = "The observation [" + ref + "] cannot establish efficacy."
        return response

    state, requests = complete(fixture(), tmp_path / "run", tmp_path, omitted_flat_ref)
    assert state["status"] == "LEAN_EVIDENCE_CONSOLIDATION_CHECKED", state
    packet = lean.validate_packet(lean.read(state["packet_path"]))
    answer = packet["answers"][0]
    ref = answer["limits"].split("[")[1].split("]")[0]
    assert ref in answer["evidence_refs"]
    assert all(r["payload"]["answers"] == packet["answers"] for r in requests if r["phase"] == "lean_review")
    synthesis = next(r for r in requests if r["phase"] == "lean_synthesis")
    invalid = omitted_flat_ref(synthesis)
    invalid["answers"][0]["limits"] = "Foreign observation [e999999]."
    with pytest.raises(ValueError, match="foreign lean citation"):
        lean.validate_response(synthesis, invalid, count)


@pytest.mark.parametrize("disposition", ["blocked", "mechanically_excluded"])
def test_captured_blockers_stop_before_launch_but_excluded_originals_stay_visible(tmp_path, disposition):
    source, commission, capacity = fixture()
    source["captured_items"][0].update(accounting_disposition=disposition, accounting_reason="Captured original has this explicit intake disposition.")
    source.pop("source_sha256")
    source["source_sha256"] = _sha256(source)
    state = lean.advance(source, commission, capacity, tmp_path / "run", count=count)
    if disposition == "blocked":
        assert state["status"] == "SEMANTIC_ADVANCE_BLOCKED"
        assert "blocked captured rows: original-0" in state["error"]
        assert not list((tmp_path / "run").glob("requests/*"))
    else:
        assert state["status"] == "SEMANTIC_JUDGMENT_REQUIRED"
        request = lean.read(state["judgment_requests"][0]["job_path"])
        assert request["payload"]["records"][0]["accounting_disposition"] == disposition
        assert any("Comfortable in winter" in o["text"] for o in request["payload"]["observations"])


@pytest.mark.parametrize("mutation", ["body", "context", "commission", "capacity"])
def test_changed_bound_inputs_block_even_when_source_rehashed(tmp_path, mutation):
    args = fixture()
    first = lean.advance(*args, tmp_path / "run", count=count)
    assert first["status"] == "SEMANTIC_JUDGMENT_REQUIRED"
    changed = deepcopy(args)
    if mutation == "body":
        changed[0]["captured_items"][0]["text"] += " changed"
    elif mutation == "context":
        changed[0]["captured_items"][0]["product_context"][0]["text"] += " changed"
    elif mutation == "commission":
        changed[1]["questions"][0]["question"] += " changed"
    else:
        changed[2]["max_rows_per_slice"] = 2
    changed[0]["source_sha256"] = _sha256({k: v for k, v in changed[0].items() if k != "source_sha256"})
    state = lean.advance(*changed, tmp_path / "run", count=count)
    assert state["status"] == "SEMANTIC_ADVANCE_BLOCKED"
    assert "differs" in state["error"] or "immutable" in state["error"]
    assert not state["judgment_requests"]


@pytest.mark.parametrize("mutation", ["foreign", "prose", "omitted", "stale"])
def test_read_response_rejects_real_violation_before_persistence(tmp_path, mutation):
    state = lean.advance(*fixture(), tmp_path / "run", count=count)
    info = state["judgment_requests"][0]
    request = lean.read(info["job_path"])
    response = respond(request)
    if mutation == "foreign":
        response["findings"][0]["supporting_refs"] = ["e999"]
    elif mutation == "prose":
        response["findings"][0]["statement"] += " [e999]"
    elif mutation == "omitted":
        response["findings"] = []
    else:
        response["input_sha256"] = "wrong"
    with pytest.raises(Exception, match="foreign|coverage|expected"):
        publish(info, response, tmp_path)
    assert not (lean.Path(info["job_path"]).parent / "response.json").exists()


def test_accepted_missing_or_unaccepted_output_cannot_silently_rejudge(tmp_path):
    args = fixture()
    state = lean.advance(*args, tmp_path / "run", count=count)
    info = state["judgment_requests"][0]
    request = lean.read(info["job_path"])
    response = respond(request)
    target = lean.Path(info["job_path"]).with_name("response.json")
    target.write_bytes((lean.compact(response) + "\n").encode("utf-8"))
    blocked = lean.advance(*args, tmp_path / "run", count=count)
    assert blocked["status"] == "SEMANTIC_ADVANCE_BLOCKED"
    assert "unaccepted" in blocked["error"]
    publish(info, response, tmp_path)  # explicit validated submission recovers this exact staging
    target.unlink()
    blocked = lean.advance(*args, tmp_path / "run", count=count)
    assert blocked["status"] == "SEMANTIC_ADVANCE_BLOCKED"
    assert not blocked["judgment_requests"]


@pytest.mark.parametrize("field", ["reviewed_claim_ids", "reviewed_rows", "reviewed_checks"])
def test_empty_exceptions_cannot_hide_omitted_review_obligation(tmp_path, field):
    args = fixture()
    root = tmp_path / "run"
    for _ in range(5):
        state = lean.advance(*args, root, count=count)
        if state.get("phase") == "lean_review":
            break
        for info in state["judgment_requests"]:
            publish(info, respond(lean.read(info["job_path"])), tmp_path)
    info = next(i for i in state["judgment_requests"] if lean.read(i["job_path"])["payload"]["checks"])
    request = lean.read(info["job_path"])
    response = respond(request)
    response[field] = []
    with pytest.raises(ValueError, match="review .*coverage"):
        publish(info, response, tmp_path)
    assert lean.advance(*args, root, count=count)["status"] != "LEAN_EVIDENCE_CONSOLIDATION_CHECKED"


def test_material_review_requires_targeted_repair_and_exact_candidate_recheck(tmp_path):
    args = fixture()

    def material(request):
        response = respond(request)
        if request["phase"] == "lean_review" and request["payload"]["findings"]:
            response["exceptions"] = [{"severity": "material", "question_ids": ["q"], "finding_ids": ["f0"],
                                       "source_refs": request["payload"]["allowed_refs"], "reason": "Missing important condition."}]
        return response

    state, seen = complete(args, tmp_path / "run", tmp_path, material)
    assert state["status"] == "LEAN_EVIDENCE_CONSOLIDATION_CHECKED", state
    assert [r["phase"] for r in seen].count("lean_repair") == 1
    original = next(r["payload"]["answers"] for r in seen if r["phase"] == "lean_review")
    final = lean.read(state["packet_path"])["answers"]
    assert original != final
    assert all(r["payload"]["answers"] == final for r in seen if r["phase"] == "lean_recheck")


def test_answer_claim_exception_repairs_that_answer_without_inventing_finding_targets(tmp_path):
    args = fixture()
    args[2]["max_rows_per_slice"] = 4

    def answer_defect(request):
        response = respond(request)
        if request["phase"] == "lean_review":
            response["exceptions"] = [{"severity": "material", "question_ids": ["q"], "finding_ids": ["answer:q"],
                                       "source_refs": [request["payload"]["allowed_refs"][0]],
                                       "reason": "The answer assigns a reason the source does not state."}]
        return response

    state, seen = complete(args, tmp_path / "run", tmp_path, answer_defect)
    assert state["status"] == "LEAN_EVIDENCE_CONSOLIDATION_CHECKED", state
    repair = next(r for r in seen if r["phase"] == "lean_repair")
    assert repair["payload"]["target_findings"] == []
    assert repair["payload"]["target_questions"] == ["q"]
    assert repair["payload"]["exceptions"][0]["finding_ids"] == ["answer:q"]
    packet = lean.validate_packet(lean.read(state["packet_path"]))
    original = next(r["payload"] for r in seen if r["phase"] == "lean_review")
    assert packet["findings"] == original["findings"]
    assert packet["answers"] != original["answers"]
    assert all(r["payload"]["answers"] == packet["answers"] for r in seen if r["phase"] == "lean_recheck")


@pytest.mark.parametrize("mutation", ["foreign_answer", "foreign_finding", "mismatched_question"])
def test_review_exception_cannot_target_foreign_claim_or_wrong_answer_question(tmp_path, mutation):
    args = fixture()
    args[1]["questions"].append({"id": "other", "question": "What remains uncertain?"})
    root = tmp_path / "run"
    for _ in range(5):
        state = lean.advance(*args, root, count=count)
        if state.get("phase") == "lean_review":
            break
        for info in state["judgment_requests"]:
            request = lean.read(info["job_path"])
            response = respond(request)
            if "answers" in response:
                response["answers"].append({"question_id": "other", "answer": "No additional conclusion.", "evidence_refs": [], "limits": "Evidence is bounded."})
            publish(info, response, tmp_path)
    info = state["judgment_requests"][0]
    request = lean.read(info["job_path"])
    response = respond(request)
    response["exceptions"] = [{"severity": "material", "question_ids": ["other" if mutation == "mismatched_question" else "q"],
                               "finding_ids": [{"foreign_answer": "answer:absent", "foreign_finding": "f999", "mismatched_question": "answer:q"}[mutation]],
                               "source_refs": [request["payload"]["allowed_refs"][0]], "reason": "Claim needs correction."}]
    expected = "question route" if mutation == "mismatched_question" else "foreign or missing evidence"
    with pytest.raises(ValueError, match=expected):
        publish(info, response, tmp_path)
    assert not lean.Path(info["job_path"]).with_name("response.receipt.json").exists()


@pytest.mark.parametrize("commissioned", [False, True])
def test_supplementary_review_labels_are_preserved_without_commissioned_credit(tmp_path, commissioned):
    args = fixture()
    if not commissioned:
        args[1].pop("assessment_only")

    def annotated(request):
        response = respond(request)
        if request["phase"] == "lean_review":
            response["reviewed_checks"].append("General source attribution and context audit")
        return response

    state, seen = complete(args, tmp_path / "run", tmp_path, annotated)
    assert state["status"] == "LEAN_EVIDENCE_CONSOLIDATION_CHECKED", state
    packet = lean.validate_packet(lean.read(state["packet_path"]))
    assert all("General source attribution and context audit" in p["response"]["reviewed_checks"] for p in packet["review"]["responses"])
    assert packet["commission"].get("assessment_only", {}).get("checks", []) == args[1].get("assessment_only", {}).get("checks", [])
    review = next(r for r in seen if r["phase"] == "lean_review" and (r["payload"]["checks"] or not commissioned))
    response = annotated(review)
    response["reviewed_checks"] = ["General source attribution and context audit"]
    if commissioned:
        with pytest.raises(ValueError, match="review check coverage differs"):
            lean.validate_response(review, response, count)
    else:
        lean.validate_response(review, response, count)
    response = annotated(review)
    response["reviewed_checks"].append("General source attribution and context audit")
    with pytest.raises(ValueError, match="review check coverage differs"):
        lean.validate_response(review, response, count)


def test_recheck_material_failure_is_revision_not_success_or_retry(tmp_path):
    def failing(request):
        response = respond(request)
        if request["phase"] in {"lean_review", "lean_recheck"} and request["payload"]["findings"]:
            response["exceptions"] = [{"severity": "material", "question_ids": ["q"], "finding_ids": ["f0"],
                                       "source_refs": request["payload"]["allowed_refs"], "reason": "Still unsupported."}]
        return response

    state, seen = complete(fixture(), tmp_path / "run", tmp_path, failing)
    assert state["status"] == "LEAN_EVIDENCE_CONSOLIDATION_REQUIRES_REVISION", state
    assert [r["phase"] for r in seen].count("lean_repair") == 1


def test_large_sample_is_source_independent_and_discloses_actual_coverage(tmp_path):
    source, commission, capacity = fixture(60)
    commission["review"] = {"omission_mode": "sample", "sample_size": 7, "seed": "bound"}
    inventory = lean._source_inventory(source)
    normalized = lean._commission(commission)
    selected = lean._omission_rows(inventory, normalized)
    assert len(selected) == 7
    assert len({r["source_role"] for r in inventory["records"] if r["row_id"] in selected}) == 3
    assert selected == lean._omission_rows(inventory, normalized)
    capacity["max_rows_per_slice"] = 8
    # Isolate review planning: deliberately cite only one observation, so omitted
    # originals cannot enter only as a side effect of broad generated citations.
    findings = lean._compile_findings([finding(["e0"], "One bounded report.")], inventory["registry"])
    answers = [{"question_id": "q", "answer": "One report.", "evidence_refs": ["e0"], "limits": "Selected evidence only."}]
    requests, coverage = lean._review_requests(inventory, normalized, capacity, findings, answers, count)
    assert coverage["mode"] == "sample" and not coverage["all_originals_checked"]
    assert set(selected) <= set(coverage["reviewed_row_ids"])
    assert any(r["payload"]["omission_row_ids"] for r in requests)
    assert all(r["payload"]["answers"] == answers for r in requests)
    normalized["review"]["omission_mode"] = "all"
    _, full = lean._review_requests(inventory, normalized, capacity, findings, answers, count)
    assert full["all_originals_checked"] and len(full["omission_row_ids"]) == 60


def test_indivisible_source_capacity_failure_preserves_all_original_bytes(tmp_path):
    source, commission, capacity = fixture()
    source["captured_items"][0]["text"] = "Unabridged source. " * 10000
    source["source_sha256"] = _sha256({k: v for k, v in source.items() if k != "source_sha256"})
    state = lean.advance(source, commission, capacity, tmp_path / "run", count=count)
    assert state["status"] == "SEMANTIC_ADVANCE_BLOCKED"
    assert "capacity" in state["error"] and not state["judgment_requests"]
    assert not (tmp_path / "run" / "requests").exists()


def test_coherently_rehashed_fabricated_provenance_and_counts_fail(tmp_path):
    state, _ = complete(fixture(), tmp_path / "run", tmp_path)
    packet = lean.read(state["packet_path"])
    changed = deepcopy(packet)
    changed["registry"]["e0"]["source_role"] = "owned_claim"
    changed["packet_sha256"] = lean.digest({k: v for k, v in changed.items() if k != "packet_sha256"})
    with pytest.raises(ValueError, match="provenance"):
        lean.validate_packet(changed)
    changed = deepcopy(packet)
    changed["findings"][0]["accounting"]["supporting_refs"]["known_origin_count"] = 1000
    changed["packet_sha256"] = lean.digest({k: v for k, v in changed.items() if k != "packet_sha256"})
    with pytest.raises(ValueError, match="accounting"):
        lean.validate_packet(changed)


@pytest.mark.parametrize("mutation", ["finding", "slice", "claims", "coverage", "exceptions", "answer"])
def test_packet_review_binds_exact_output_and_complete_actual_slices(tmp_path, mutation):
    state, _ = complete(fixture(), tmp_path / "run", tmp_path)
    packet = lean.read(state["packet_path"])
    if mutation == "finding":
        packet["findings"][0]["statement"] = "A new unsupported conclusion."
        packet["review"]["findings_sha256"] = lean.digest(packet["findings"])
    elif mutation == "slice":
        packet["review"]["responses"].pop()
    elif mutation == "claims":
        packet["review"]["checked_claim_ids"] = []
    elif mutation == "coverage":
        packet["review"]["all_originals_checked"] = False
    elif mutation == "answer":
        packet["answers"][0]["answer"] = "Different final answer."
        packet["review"]["answer_sha256"] = lean.digest(packet["answers"])
    else:
        packet["review"]["exceptions"] = [{"severity": "material"}]
    packet["packet_sha256"] = lean.digest({k: v for k, v in packet.items() if k != "packet_sha256"})
    with pytest.raises(ValueError, match="review|coverage|exceptions|proof"):
        lean.validate_packet(packet)


def test_progressive_synthesis_folds_new_batches_without_repeating_a_ledger(tmp_path):
    args = list(fixture(14))
    args[2]["effective_context_tokens"] = 16000
    args[2]["output_reserve_tokens"] = 3000
    args[2]["other_overhead_reserve_tokens"] = 100

    def verbose_notes(request):
        response = respond(request)
        if request["phase"] == "lean_read":
            for value in response["findings"]:
                value["statement"] += " A retained material condition and qualification." * 25
        return response

    state, seen = complete(args, tmp_path / "run", tmp_path, verbose_notes)
    assert state["status"] == "LEAN_EVIDENCE_CONSOLIDATION_CHECKED", state
    folds = [r for r in seen if r["phase"] == "lean_synthesis"]
    assert len(folds) > 1
    assert sum(r["payload"]["final"] for r in folds) == 1
    assert all("answers" not in r["schema"]["properties"] for r in folds[:-1])
    new_inputs = [f["input_ref"] for r in folds for f in r["payload"]["inputs"] if f["input_ref"].startswith("n")]
    assert len(new_inputs) == len(set(new_inputs)) == 11
    assert all(r["measurement"]["total_reserved_tokens"] <= args[2]["effective_context_tokens"] for r in seen)


def test_valid_schema_tampered_accepted_response_fails_receipt_binding(tmp_path):
    args = fixture()
    state = lean.advance(*args, tmp_path / "run", count=count)
    info = state["judgment_requests"][0]
    request = lean.read(info["job_path"])
    response = respond(request)
    publish(info, response, tmp_path)
    response["findings"][0]["statement"] += " Altered after acceptance."
    lean.validate_response(request, response, count)  # prove schema/coverage still pass
    lean.Path(info["job_path"]).with_name("response.json").write_text(lean.compact(response) + "\n", encoding="utf-8")
    blocked = lean.advance(*args, tmp_path / "run", count=count)
    assert blocked["status"] == "SEMANTIC_ADVANCE_BLOCKED"
    assert "receipt mismatch" in blocked["error"]


def test_fresh_capture_table_is_lossless_and_materially_smaller(tmp_path):
    source, commission, capacity = fixture(8)
    source["containers"] = [{"container_id": "thread", "capture_boundary": "All archived text; live completeness unknown. " * 120,
                             "completeness": "partial", "captured_leaf_count": 8, "source_visible_total": "unavailable"}]
    for row in source["captured_items"]:
        row["container_id"] = "thread"
    source.pop("source_sha256")
    source["source_sha256"] = _sha256(source)
    capacity["max_rows_per_slice"] = 8
    inventory = lean._source_inventory(source)
    original = lean._originals(inventory, inventory["records"])
    packed = lean._originals(inventory, inventory["records"], delivery_layout=lean.DELIVERY_LAYOUT)
    expanded = deepcopy(packed)
    expanded.pop("delivery_layout")
    captures = expanded.pop("captures")
    for row in expanded["records"]:
        row["capture"] = captures[row.pop("capture_ref")]
    assert expanded == original
    assert len(captures) == 1 and count(lean.compact(packed)) < count(lean.compact(original)) * 0.6
    state = lean.advance(source, commission, capacity, tmp_path / "run", count=count)
    assert state["status"] == "SEMANTIC_JUDGMENT_REQUIRED", state
    assert len(state["judgment_requests"]) == 1
    request = lean.read(state["judgment_requests"][0]["job_path"])
    assert lean.read(tmp_path / "run" / "start.json")["delivery_layout"] == lean.DELIVERY_LAYOUT
    assert request["payload"]["captures"] == captures
    assert request["payload"]["observations"] == original["observations"]
    assert all("capture" not in row for row in request["payload"]["records"])


def test_pre_layout_start_and_default_capacity_packet_replay_without_restamping(tmp_path):
    source, commission, _ = fixture()
    root = tmp_path / "run"
    # Historical starts did not carry a layout field, including default-capacity runs.
    lean.retain(root / "start.json", {"method_version": lean.METHOD_VERSION, "source_sha256": source["source_sha256"],
        "source_object_sha256": lean.digest(source), "commission_sha256": lean.digest(lean._commission(commission)),
        "capacity_sha256": lean.digest(lean.DEFAULT_CAPACITY)})
    args = (source, commission, None)
    state, requests = complete(args, root, tmp_path)
    assert state["status"] == "LEAN_EVIDENCE_CONSOLIDATION_CHECKED", state
    assert all("delivery_layout" not in request["payload"] for request in requests)
    assert all("capture" in row for request in requests for row in request["payload"].get("records", []))
    packet = lean.validate_packet(lean.read(state["packet_path"]))
    assert "delivery_layout" not in packet
    before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}
    repeated, calls = complete(args, root, tmp_path)
    assert repeated == state and not calls
    assert before == {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}


@pytest.mark.parametrize("mutation", ["remove", "legacy", "unknown"])
def test_changed_layout_pin_cannot_silently_rejudge_saved_requests(tmp_path, mutation):
    args, root = fixture(), tmp_path / "run"
    state = lean.advance(*args, root, count=count)
    request_paths = set((root / "requests").glob("*/request.json"))
    start = lean.read(root / "start.json")
    if mutation == "remove":
        start.pop("delivery_layout")
    else:
        start["delivery_layout"] = lean.LEGACY_DELIVERY_LAYOUT if mutation == "legacy" else "unknown_layout"
    (root / "start.json").write_text(lean.compact(start), encoding="utf-8")
    blocked = lean.advance(*args, root, count=count)
    assert state["status"] == "SEMANTIC_JUDGMENT_REQUIRED"
    assert blocked["status"] == "SEMANTIC_ADVANCE_BLOCKED" and "delivery layout" in blocked["error"]
    assert not blocked["judgment_requests"] and set((root / "requests").glob("*/request.json")) == request_paths


def test_new_review_and_recheck_assign_remote_originals_without_asserting_support(tmp_path):
    source, commission, capacity = fixture(60)
    commission["review"] = {"omission_mode": "sample", "sample_size": 3, "seed": "bounded-slices"}
    commission = lean._commission(commission)
    capacity["max_rows_per_slice"] = 2
    inventory = lean._source_inventory(source)
    refs = [inventory["records"][index]["body_ref"] for index in (0, 59)]
    findings = lean._compile_findings([finding(refs, "A conditional finding with premises in different source slices.")], inventory["registry"])
    answers = [{"question_id": "q", "answer": "The source accounts differ by condition.", "evidence_refs": refs, "limits": "No prevalence or causal conclusion."}]
    requests, coverage = lean._review_requests(inventory, commission, capacity, findings, answers, count,
                                               delivery_layout=lean.DELIVERY_LAYOUT)
    assert len(requests) > 1
    for request in requests:
        p = request["payload"]
        assert p["answers"] == answers and all(f in findings for f in p["findings"])
        scope = p["review_scope"]
        other_text = {o["ref"] for other in requests if other != request for o in other["payload"]["observations"]}
        assert set(scope["elsewhere_source_refs"]) == set(refs) - set(scope["local_source_refs"])
        assert set(scope["elsewhere_source_refs"]) <= other_text
        assert "absence HERE is intentional, never a defect" in request["prompt"]
        lean.validate_response(request, respond(request), count)
    prior_row = next(r for r in inventory["records"] if r["row_id"] not in coverage["reviewed_row_ids"])
    prior = [{"severity": "material", "question_ids": ["q"], "finding_ids": [], "source_refs": [prior_row["body_ref"]],
              "reason": "An original qualification was previously omitted."}]
    rechecks, corrected = lean._review_requests(inventory, commission, capacity, findings, answers, count,
        phase="lean_recheck", prior_exceptions=prior, delivery_layout=lean.DELIVERY_LAYOUT)
    assert prior_row["row_id"] in corrected["reviewed_row_ids"]
    assert any(prior_row["body_ref"] in r["payload"]["review_scope"]["local_source_refs"] for r in rechecks)
    assert all(prior_row["body_ref"] in (r["payload"]["review_scope"]["local_source_refs"] +
                                      r["payload"]["review_scope"]["elsewhere_source_refs"]) for r in rechecks)
    assert all("assigned to OTHER slices" in r["prompt"] for r in rechecks)
    request = next(r for r in requests if r["payload"]["review_scope"]["elsewhere_source_refs"])
    missing_assignment = deepcopy(request["payload"])
    missing_assignment["review_scope"]["elsewhere_source_refs"].pop()
    with pytest.raises(ValueError, match="source assignment coverage differs"):
        lean.build_request("lean_review", missing_assignment, capacity, count)
    missing_original = deepcopy(request["payload"])
    missing_original["observations"].pop()
    with pytest.raises(ValueError, match="delivered original coverage differs"):
        lean.build_request("lean_review", missing_original, capacity, count)


def test_reviewed_compact_layout_cannot_be_downgraded_in_rehashed_packet(tmp_path):
    state, _ = complete(fixture(), tmp_path / "run", tmp_path)
    packet = lean.validate_packet(lean.read(state["packet_path"]))
    assert packet["delivery_layout"] == lean.DELIVERY_LAYOUT
    packet.pop("delivery_layout")
    packet["packet_sha256"] = lean.digest({k: v for k, v in packet.items() if k != "packet_sha256"})
    with pytest.raises(ValueError, match="review proof differs"):
        lean.validate_packet(packet)


def test_unclassified_known_prose_original_reaches_review_and_repair_without_support_credit(tmp_path):
    source, commission, capacity = fixture(2)
    for row in source["captured_items"]:
        row["product_context"] = []
    source["captured_items"][0]["text"] = "I use foundation only on my nose."
    source["captured_items"][1].update(text="Full face foundation feels uncomfortable, despite good coverage.", source_role="retailer_review")
    source.pop("source_sha256")
    source["source_sha256"] = _sha256(source)

    def conditional(request):
        response = respond(request)
        p, phase = request["payload"], request["phase"]
        if phase == "lean_read" and p["records"][0]["row_id"] == "r1":
            response["findings"] = [finding([], "Full-face coverage can feel unwelcome [e1].")]
        elif phase == "lean_synthesis":
            response["findings"] = [finding(["e0"], "Coverage preference differs; full-face feel can be unwelcome [e1].",
                                             inputs=[f["input_ref"] for f in p["inputs"]])]
            if p["final"]:
                response["answers"] = [{"question_id": "q", "answer": "Preferences differ by application.",
                                          "evidence_refs": ["e0"], "limits": "Captured accounts only."}]
        elif phase == "lean_review" and p["records"][0]["row_id"] == "r0":
            response["exceptions"] = [{"severity": "material", "question_ids": ["q"], "finding_ids": ["f0"],
                                       "source_refs": ["e0"], "reason": "Preserve the application qualification."}]
        elif phase == "lean_repair":
            response["replacements"] = [{"finding_id": "f0", "finding": finding(["e0"],
                "Application is conditional; full-face feel can be unwelcome [e1].")}]
            response["answers"][0]["evidence_refs"] = ["e0"]
        return response

    state, requests = complete((source, commission, capacity), tmp_path / "run", tmp_path, conditional)
    assert state["status"] == "LEAN_EVIDENCE_CONSOLIDATION_CHECKED", state
    synthesis = next(r for r in requests if r["phase"] == "lean_synthesis")
    assert "e1" in synthesis["payload"]["allowed_refs"]
    raw_read = next(r for r in requests if r["phase"] == "lean_read" and r["payload"]["records"][0]["row_id"] == "r1")
    accepted = lean.read(lean.Path(tmp_path / "run" / "requests" / raw_read["request_sha256"] / "response.json"))
    assert all(accepted["findings"][0][relation] == [] for relation in lean.RELATIONS)
    remote_review = next(r for r in requests if r["phase"] == "lean_review" and r["payload"]["records"][0]["row_id"] == "r1")
    assert remote_review["payload"]["findings"][0]["finding_id"] == "f0"
    assert "e1" in remote_review["payload"]["review_scope"]["local_source_refs"]
    repair = next(r for r in requests if r["phase"] == "lean_repair")
    assert "e1" in repair["payload"]["allowed_refs"]  # Neither exception nor answer cites it.
    packet = lean.validate_packet(lean.read(state["packet_path"]))
    result = packet["findings"][0]
    assert lean.finding_refs(result) == {"e0", "e1"}
    assert lean.resolve_refs(packet, ["e1"])[0]["text"] == source["captured_items"][1]["text"]
    assert result["accounting"]["supporting_refs"]["known_origin_refs"] == ["o0"]
    assert all("o1" not in row["known_origin_refs"] for row in result["accounting"].values())
    bad = conditional(raw_read)
    bad["findings"][0]["statement"] += " Foreign original [e999]."
    with pytest.raises(ValueError, match="foreign or missing source citation"):
        lean.validate_response(raw_read, bad, count)

    # A reachable prose original is not a second credited support for comparison.
    packet["commission"]["comparison_scope"] = {"q": {"axis_ids": ["comfort"], "subject_product_ids": ["subject"], "comparator_product_ids": ["competitor"]}}
    packet["answers"][0]["evidence_refs"] = ["e0", "e1"]
    packet["answers"][0]["comparison_verdicts"] = [{"axis_id": "comfort", "choice_posture": "subject_advantage",
        "claim_kind": "customer_experience", "support_posture": "independently_repeated", "conflict_posture": "none_observed",
        "why": "Another detail is reachable [e1].", "supporting_refs": ["e0"], "opposing_refs": [], "context_refs": [],
        "conditions": [], "limits": "Captured accounts only."}]
    packet["packet_sha256"] = lean.digest({k: v for k, v in packet.items() if k != "packet_sha256"})
    with pytest.raises(ValueError, match="lacks two credited origins"):
        lean.validate_packet(packet)
