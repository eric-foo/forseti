"""Adversarial boundary fixtures, not evidence of model semantic quality."""
from copy import deepcopy
import json

import pytest

from judgment import complete_case_consumer as c
from judgment import semantic_evidence_integration as s
from test_semantic_evidence_integration import _source_v10, _keyed_responses


def fixture(count=2):
    source = _source_v10(count=count)
    source["semantic_method_version"] = s.METHOD_VERSION_V13
    source["captured_items"][0]["text"] = "The explicitly pink shade suits me; vanilla smells nice."
    source["captured_items"][1]["text"] = "Burned my skin; never buying again."
    source["source_sha256"] = s._sha256(source)
    commission = {"experimental_method": c.PROVISIONAL_METHOD,
        "questions": [{"id": "q", "question": "What do these sources support?"}]}
    capacity = {"encoding": "fixture", "effective_context_tokens": 2000000,
        "output_reserve_tokens": 24000, "other_overhead_reserve_tokens": 4000,
        "max_rows_per_slice": 12}
    return source, commission, capacity


def advance(args, root):
    return c.advance_provisional(*args, root, context="fixture authority", count=len)


def publish(state, response, tmp_path):
    info = state["judgment_requests"][0]
    raw = tmp_path / "raw.json"
    raw.write_text(json.dumps(response), encoding="utf-8")
    return c.submit(info["job_path"], info["job_sha256"], raw, len)


def request(state):
    return c.read(state["judgment_requests"][0]["job_path"])


def extraction(state):
    rows = request(state)["payload"]["original_source"]["captured_items"]
    return {"findings": [finding(rows[0])], "unused": [
        {"unit_ref": r["evidence_id"], "reason": "Misclassified as irrelevant to this question."}
        for r in rows[1:]]}


def finding(row):
    return {"statement": row["text"], "question_ids": ["q"],
        "supporting_refs": [row["evidence_id"]], "opposing_refs": [],
        "context_refs": [], "limits": "Attributed to this source; no independent corroboration."}


def reach_review(args, root, tmp_path):
    state = advance(args, root)
    publish(state, extraction(state), tmp_path)
    state = advance(args, root)
    assert request(state)["payload"]["original_source"]["captured_items"] == args[0]["captured_items"]
    # Simulate extraction omitting an important negative row: it still reaches
    # the real writer and reviewer as an original, not a reused verified nonclaim.
    publish(state, {"answers": [{"question_id": "q", "answer": "Only positive experiences.",
        "evidence_refs": [args[0]["captured_items"][0]["evidence_id"]], "limits": "Selected rows."}]}, tmp_path)
    return advance(args, root)


def review(status):
    return {"answers": [{"question_id": "q", "status": status,
        "reason": "Uncited original contradicts the positive-only answer."}],
        "checks": [], "material_findings": [], "reopen_refs": []}


def test_omitted_negative_reaches_exact_answer_review_and_blocks_delivery(tmp_path):
    args = fixture()
    root = tmp_path / "run"
    state = reach_review(args, root, tmp_path)
    payload = request(state)["payload"]
    assert payload["original_source"]["captured_items"] == args[0]["captured_items"]
    assert payload["source_sha256"] == args[0]["source_sha256"]
    assert payload["answer"]["answers"][0]["answer"] == "Only positive experiences."
    assert payload["provisional_notes"]["status"] == "PROVISIONAL_UNVERIFIED"
    publish(state, review("defect"), tmp_path)
    result = advance(args, root)
    assert result["status"] == "EXPERIMENTAL_ANSWER_BLOCKED"
    assert not result["normal_semantic_completion"]
    assert not result["extraction_recall_proven"]
    assert advance(args, root) == result
    assert len(list((root / "requests").glob("*/request.json"))) == 3


def test_clean_review_is_only_experimental_and_restart_reuses_exact_result(tmp_path):
    args = fixture()
    state = reach_review(args, tmp_path / "run", tmp_path)
    publish(state, review("pass"), tmp_path)
    result = advance(args, tmp_path / "run")
    assert result["status"] == "EXPERIMENTAL_ANSWER_SOURCE_CHECKED"
    assert result["row_verification"] == "not_performed"
    assert advance(args, tmp_path / "run") == result
    notes = c.read(tmp_path / "run/provisional-notes.json")
    bundle = c.read(tmp_path / "run/bundle.json")
    with pytest.raises(s.SemanticIntegrationError, match="compilation_sha256"):
        s.validate_row_verified_compilation(bundle, notes, notes)


@pytest.mark.parametrize("mutation", ["missing", "foreign", "duplicate_unused", "used_and_unused", "foreign_question", "empty_refs", "fake_product_field"])
def test_extraction_identity_rejected_at_submission(tmp_path, mutation):
    state = advance(fixture(), tmp_path / "run")
    response = extraction(state)
    if mutation == "missing":
        response["unused"] = []
    elif mutation == "foreign":
        response["unused"][0]["unit_ref"] = "foreign"
    elif mutation == "duplicate_unused":
        response["unused"] *= 2
    elif mutation == "used_and_unused":
        response["unused"][0]["unit_ref"] = response["findings"][0]["supporting_refs"][0]
    elif mutation == "foreign_question":
        response["findings"][0]["question_ids"] = ["foreign"]
    elif mutation == "empty_refs":
        response["findings"][0]["supporting_refs"] = []
    elif mutation == "fake_product_field":
        response["findings"][0]["subject_product_ids"] = ["invented-brand-product"]
    with pytest.raises(ValueError):
        publish(state, response, tmp_path)
    assert not list((tmp_path / "run").glob("requests/*/response.receipt.json"))


def test_duplicate_raw_key_is_rejected_before_last_key_wins(tmp_path):
    state = advance(fixture(), tmp_path / "run")
    raw = tmp_path / "duplicate.json"
    text = json.dumps(extraction(state))
    raw.write_text(text[:-1] + ', "unused": []}', encoding="utf-8")
    info = state["judgment_requests"][0]
    with pytest.raises(ValueError, match="duplicate JSON key"):
        c.submit(info["job_path"], info["job_sha256"], raw, len)


def test_source_tampering_and_rehashed_restart_drift_fail_at_distinct_boundaries(tmp_path):
    args = fixture()
    first = advance(args, tmp_path / "run")
    before = request(first)
    changed = deepcopy(args)
    changed[0]["captured_items"][1]["text"] = "Everything was fine."
    with pytest.raises(ValueError, match="source_sha256"):
        advance(changed, tmp_path / "run")
    changed[0].pop("source_sha256")
    changed[0]["source_sha256"] = s._sha256(changed[0])
    with pytest.raises(ValueError, match="overwrite|differ"):
        advance(changed, tmp_path / "run")
    assert request(first) == before


def test_missing_accepted_response_never_rejudges(tmp_path):
    args = fixture()
    state = advance(args, tmp_path / "run")
    publish(state, extraction(state), tmp_path)
    from pathlib import Path
    Path(state["judgment_requests"][0]["response_path"]).unlink()
    with pytest.raises(ValueError, match="requires recovery"):
        advance(args, tmp_path / "run")


def test_explicit_opt_in_and_duplicate_source_rows(tmp_path):
    args = fixture()
    args[1].pop("experimental_method")
    with pytest.raises(ValueError, match="explicit"):
        advance(args, tmp_path / "run")
    args[1]["experimental_method"] = c.LEGACY_PROVISIONAL_METHOD
    with pytest.raises(ValueError, match="explicit"):
        advance(args, tmp_path / "run")
    args = fixture()
    args[0]["captured_items"].append(deepcopy(args[0]["captured_items"][0]))
    args[0].pop("source_sha256")
    args[0]["source_sha256"] = s._sha256(args[0])
    with pytest.raises(ValueError, match="duplicate"):
        advance(args, tmp_path / "run")


def test_v13_method_and_verifier_text_unchanged_by_experiment(tmp_path):
    args = fixture()
    before = s.build_bundle(args[0], max_prompt_bytes=400000, max_evidence_per_work_unit=12)
    prompts = s.build_batch_prompts(before)
    verification = s._verification_method(before)
    advance(args, tmp_path / "run")
    after = s.build_bundle(args[0], max_prompt_bytes=400000, max_evidence_per_work_unit=12)
    assert before == after
    assert s.build_batch_prompts(after) == prompts
    assert s._verification_method(after) == verification


def test_broad_meanings_and_commission_reach_every_actor_without_product_coercion(tmp_path):
    source, commission, capacity = fixture(count=4)
    meanings = [
        "I like the founders but avoid the brand because I think they are already wealthy.",
        "I have not tried this brand. An uncataloged competitor's Moon Mask is my favorite moisturizer.",
        "The founder describes a lifestyle strategy rather than clinical claims; an editorial report cites a 2025 US retailer ranking.",
        "It burned after use on my sensitive skin; sequence does not establish causality.",
    ]
    for row, meaning in zip(source["captured_items"], meanings):
        row["text"] = meaning
    source.pop("source_sha256")
    source["source_sha256"] = s._sha256(source)
    commission["questions"][0]["question"] = "What do the sources support about product experience, limits and brand positioning?"
    args = source, commission, capacity
    root = tmp_path / "run"
    state = advance(args, root)
    notes = {"findings": [finding(row) for row in source["captured_items"]], "unused": []}
    for phase in ("provisional_extraction", "assembly", "answer_review"):
        current = request(state)
        assert current["phase"] == phase
        assert current["payload"]["commission"] == commission
        assert commission["questions"][0]["question"] in current["prompt"]
        assert "Every semantic unit requires" not in current["prompt"]
        assert current["payload"]["original_source"]["captured_items"] == source["captured_items"]
        for meaning in meanings:
            assert meaning in current["prompt"]
        from pathlib import Path
        actor = c.read(Path(state["judgment_requests"][0]["job_path"]).with_name("actor-input.json"))
        assert actor == {"prompt": current["prompt"], "response_schema": current["schema"]}
        if phase == "provisional_extraction":
            publish(state, notes, tmp_path)
        else:
            assert current["payload"]["provisional_notes"]["findings"] == notes["findings"]
            if phase == "assembly":
                publish(state, {"answers": [{"question_id": "q", "answer": " ".join(meanings),
                    "evidence_refs": [r["evidence_id"] for r in source["captured_items"]],
                    "limits": "These selected sources do not establish prevalence."}]}, tmp_path)
            else:
                publish(state, review("pass"), tmp_path)
        state = advance(args, root)
    assert state["status"] == "EXPERIMENTAL_ANSWER_SOURCE_CHECKED"
    assert state["answer"]["answers"][0]["answer"] == " ".join(meanings)


def test_saved_v1_native_response_still_validates_without_reinterpreting_it():
    source, commission, capacity = fixture()
    commission["experimental_method"] = c.LEGACY_PROVISIONAL_METHOD
    bundle = s.build_bundle(source, max_prompt_bytes=400000, max_evidence_per_work_unit=12)
    payload = {"experimental_method": c.LEGACY_PROVISIONAL_METHOD, "bundle": bundle}
    saved_request = {"phase": "provisional_extraction", "payload": payload,
        "capacity": capacity, "schema": c.response_schema("provisional_extraction", payload)}
    c.validate_response(saved_request, _keyed_responses(bundle)[0], len)


def test_context_only_finding_and_unused_envelope_reach_exact_review(tmp_path):
    source, commission, capacity = fixture(count=3)
    rows = source["captured_items"]
    context = {"context_type": "post_text", "source_artifact_id": rows[0]["source_artifact_id"],
        "source_ref": "fixture://thread/post",
        "text": "Is A or B closer to the original formula? I want that texture."}
    for row, body in zip(rows, ("Automated posting-rules notice.", "Thanks!", "Please follow forum rules.")):
        row["text"] = body
        row["parent_context"] = []
    rows[0]["product_context"] = [deepcopy(context)]
    rows[1]["product_context"] = [deepcopy(context)]
    rows[2]["product_context"] = [{**context, "context_type": "thread_title",
        "source_ref": "fixture://rules", "text": "Community rules"}]
    source.pop("source_sha256")
    source["source_sha256"] = s._sha256(source)
    args = source, commission, capacity
    root = tmp_path / "run"
    state = advance(args, root)
    note = {"statement": "The unidentified thread author seeks original-formula texture when comparing A and B.",
        "question_ids": ["q"], "supporting_refs": [row["evidence_id"] for row in rows[:2]],
        "opposing_refs": [], "context_refs": [],
        "limits": "One shared post, not two independent observations or either reply author's preference. Question only; no trial or equivalence established."}
    notes = {"findings": [note], "unused": [{"unit_ref": rows[2]["evidence_id"],
        "reason": "Both body and attached title concern forum rules, with no product-choice meaning."}]}
    publish(state, notes, tmp_path)
    state = advance(args, root)
    assert request(state)["payload"]["provisional_notes"]["findings"] == [note]
    assert request(state)["payload"]["provisional_notes"]["unused"] == notes["unused"]
    publish(state, {"answers": [{"question_id": "q", "answer": "No choice criterion is supplied.",
        "evidence_refs": [], "limits": "Selected rows."}]}, tmp_path)
    state = advance(args, root)
    payload = request(state)["payload"]
    assert payload["original_source"]["captured_items"] == rows
    assert payload["provisional_notes"]["findings"] == [note]
    assert payload["answer"]["answers"][0]["answer"] == "No choice criterion is supplied."
    defect = review("defect")
    defect["material_findings"] = [{"question_ids": ["q"], "evidence_refs": [rows[0]["evidence_id"]],
        "reason": "The answer omits the thread author's context-supported comparison criterion."}]
    defect["reopen_refs"] = [rows[0]["evidence_id"]]
    publish(state, defect, tmp_path)
    assert advance(args, root)["status"] == "EXPERIMENTAL_ANSWER_BLOCKED"


def test_instruction_change_requires_fresh_root_but_saved_response_still_validates(tmp_path, monkeypatch):
    args = fixture()
    root = tmp_path / "run"
    state = advance(args, root)
    saved_request = request(state)
    saved_response = extraction(state)
    publish(state, saved_response, tmp_path)
    monkeypatch.setattr(c, "PROVISIONAL_INSTRUCTIONS", c.PROVISIONAL_INSTRUCTIONS + "\nChanged interpretation.")
    with pytest.raises(ValueError, match="overwrite|differ"):
        advance(args, root)
    assert request(state) == saved_request
    c.validate_response(saved_request, saved_response, len)
    assert not (root / "result.json").exists()


def test_source_delivery_keeps_all_rows_but_omits_unreferenced_artifact_inventory(tmp_path):
    args = fixture()
    args[0]["source_artifacts"].append({"artifact_id": "unrelated", "locator": "unused.json", "sha256": "a" * 64})
    args[0].pop("source_sha256")
    args[0]["source_sha256"] = s._sha256(args[0])
    state = reach_review(args, tmp_path / "run", tmp_path)
    payload = request(state)["payload"]
    assert state["status"] == "SEMANTIC_JUDGMENT_REQUIRED"
    assert state["phase"] == "answer_review"
    assert payload["original_source"]["captured_items"] == args[0]["captured_items"]
    assert "unrelated" not in {a["artifact_id"] for a in payload["original_source"]["source_artifacts"]}
    assert c.read(tmp_path / "run/binding.json")["source"] == args[0]


@pytest.mark.parametrize(("status", "outcome", "code"), [
    ("defect", "EXPERIMENTAL_ANSWER_BLOCKED", 2), ("pass", "EXPERIMENTAL_ANSWER_SOURCE_CHECKED", 0)])
def test_cli_exit_status_reports_failed_answer_review(tmp_path, monkeypatch, capsys, status, outcome, code):
    from runners import finite_preparation
    from runners import run_semantic_evidence_integration as cli

    class Characters:
        def encode(self, value, disallowed_special=()):
            return value
    # Same length counter as the API fixtures; no tokenizer download.
    monkeypatch.setattr(finite_preparation, "offline_tokenizer", lambda encoding: (Characters(), None))
    argv = ["advance-provisional-experiment", "--run-dir", str(tmp_path / "run")]
    for name, value in zip(("source", "commission", "capacity"), fixture()):
        (tmp_path / f"{name}.json").write_text(json.dumps(value), encoding="utf-8")
        argv += ["--" + name, str(tmp_path / f"{name}.json")]

    def step(expected):
        assert cli.main(argv) == expected
        return json.loads(capsys.readouterr().out)
    state = step(0)
    publish(state, extraction(state), tmp_path)
    state = step(0)
    publish(state, {"answers": [{"question_id": "q", "answer": "Only positive experiences.",
        "evidence_refs": [], "limits": "Selected rows."}]}, tmp_path)
    state = step(0)
    assert state["phase"] == "answer_review"
    publish(state, review(status), tmp_path)
    assert step(code)["status"] == outcome


def test_stale_accepted_answer_cannot_reuse_passed_review(tmp_path):
    args = fixture()
    state = reach_review(args, tmp_path / "run", tmp_path)
    publish(state, review("pass"), tmp_path)
    root = tmp_path / "run"
    for path in (root / "requests").glob("*/request.json"):
        if c.read(path)["phase"] == "assembly":
            target = path.with_name("response.json")
            changed = c.read(target)
            changed["answers"][0]["answer"] = "Forged answer after the review."
            target.write_text(json.dumps(changed), encoding="utf-8")
            break
    else:
        raise AssertionError("missing actual assembly response")
    with pytest.raises(ValueError, match="response binding changed"):
        advance(args, root)
    assert not (root / "result.json").exists()
