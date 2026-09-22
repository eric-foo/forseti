"""Structural boundaries; deterministic responders are not semantic-quality proof."""
from copy import deepcopy
import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from judgment import complete_case_consumer as consumer


def count(text):
    return len(text.encode("utf-8"))


def fixture():
    source = {"question": "reported experience", "captured_items": [
        {"evidence_id": key, "source_artifact_id": "raw", "text": text, "accounting_disposition": "assess"}
        for key, text in [("a", "Comfortable; bought another."), ("b", "Fragrance headache; stopped using."),
                          ("c", "New cap has not leaked; bought another."), ("d", "Unrelated greeting.")]],
        "source_artifacts": [{"artifact_id": "raw", "locator": "fixture"}]}
    units = [{"semantic_unit_ref": key + "::u", "evidence_id": key, "statement": row["text"]}
             for key, row in zip("abc", source["captured_items"])]
    verified = {"semantic_units": units, "evidence_dispositions": [
        {"evidence_id": key, "disposition": "claim_bearing" if key != "d" else "out_of_scope",
         "disposition_reason": "Preserved meaning" if key != "d" else "Greeting has no product assertion."} for key in "abcd"]}
    view = {"propositions": [{"proposition_id": "p", "bounded_proposition": "Mixed experience",
        "semantic_relations": {"support": ["a::u"], "counter": ["b::u"]},
        "condition_lineage": [{"semantic_unit_ref": "b::u", "conditions": ["fragrance"]}]}],
        "unmerged_semantic_units": [{"semantic_unit_ref": "c::u", "reason": "Singleton mitigation"}]}
    commission = {"questions": [{"id": "q", "question": "What action is justified?"}],
        "worker_instructions": "Preserve conditions.", "coverage": "All fixture sources",
        "assessment_only": {"checks": [{"id": "check", "source_rows": ["b"], "expectation": "Preserve stopping."}]}}
    capacity = {"encoding": "fixture_bytes", "effective_context_tokens": 100000,
        "output_reserve_tokens": 15000, "other_overhead_reserve_tokens": 1000, "max_rows_per_slice": 1}
    return source, verified, view, commission, capacity


def respond(request):
    payload = request["payload"]
    if request["phase"] in {"source_review", "reopen"}:
        findings = []
        for group in payload["source_groups"]:
            refs = group["unit_ids"]
            counter = group["source_row"]["evidence_id"] == "b"
            findings.append({"statement": group["source_row"]["text"], "question_ids": ["q"],
                "supporting_refs": [] if counter else refs, "opposing_refs": refs if counter else [],
                "context_refs": [], "limits": "One source; condition-specific."})
        return {"findings": findings, "unused": []}
    if request["phase"] == "assembly":
        records = payload["checked_findings_and_unused"]
        if isinstance(records, dict):
            records = [r for group in records.values() for r in group]
        return {"answers": [{"question_id": "q", "answer": "Mixed experience; mitigation limits need for intervention.",
            "evidence_refs": [r["handle"] for r in records if "statement" in r],
            "limits": "Separate actors; no prevalence or universal resolution."}]}
    response = {"answers": [{"question_id": "q", "status": "pass", "reason": "Fixture review."}],
        "checks": [{"check_id": c["id"], "status": "pass", "reason": "Fixture check."} for c in payload["checks"]],
        "material_findings": [], "reopen_refs": []}
    if payload.get("correction_policy"):
        from judgment.review_evidence import answer_identity
        response.update(answer_repairs={"answer_sha256": answer_identity(payload["answer"]), "edits": []})
        for check in response["checks"]:
            check["scope"] = "answer"
    return response


def publish(request_info, response, tmp_path):
    raw = tmp_path / "raw.json"
    raw.write_text(json.dumps(response), encoding="utf-8")
    return consumer.submit(request_info["job_path"], request_info["job_sha256"], raw, count)


def complete(args, root, tmp_path):
    seen = []
    for _ in range(10):
        state = consumer.advance(*args, root, context="claim support fixture", count=count)
        for info in state["judgment_requests"]:
            request = consumer.read(info["job_path"])
            seen.append(request)
            publish(info, respond(request), tmp_path)
        if not state["judgment_requests"]:
            return state, seen
    raise AssertionError("did not complete")


def test_complete_split_opposition_residual_and_nonclaim_reuse(tmp_path):
    args = fixture()
    state, seen = complete(args, tmp_path / "consumer", tmp_path)
    assert state["status"] == "COMPLETE_CASE_ANSWER_CHECKED"
    source_jobs = [r for r in seen if r["phase"] == "source_review"]
    assert len(source_jobs) == 3  # no raw re-review of verified no-claim row d
    assert source_jobs[0]["payload"]["unit_ids"] == ["a::u"]
    assert source_jobs[1]["payload"]["source_groups"][0]["native_findings"][0]["semantic_relations"]["counter"] == ["b::u"]
    assembly = next(r for r in seen if r["phase"] == "assembly")
    text = consumer.compact(assembly["payload"])
    assert "stopped using" in text and "New cap" in text and "Greeting has no product" in text
    result = consumer.read(state["answer_path"])
    assert result["coverage"]["reused_nonclaim_rows"] == 1
    assert result["answer"]["answers"][0]["evidence_refs"] == ["a::u", "b::u", "c::u"]
    repeated, new = complete(args, tmp_path / "consumer", tmp_path)
    assert repeated == state and new == []


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "foreign"])
def test_exact_coverage_failure_is_not_schema_only(tmp_path, mutation):
    args = fixture()
    state = consumer.advance(*args, tmp_path / "consumer", context="", count=count)
    info = state["judgment_requests"][0]
    request = consumer.read(info["job_path"])
    response = respond(request)
    if mutation == "missing":
        response["findings"] = []
    elif mutation == "duplicate":
        response["findings"] *= 2
    else:
        response["findings"][0]["supporting_refs"] = ["foreign"]
    if mutation != "foreign":
        consumer.Draft202012Validator(request["schema"]).validate(response)
    with pytest.raises((ValueError, ValidationError), match="coverage|not one of"):
        publish(info, response, tmp_path)
    assert not Path(info["response_path"]).exists()


def test_provider_schema_uses_supported_subset_and_local_identity_enforcement(tmp_path):
    state = consumer.advance(*fixture(), tmp_path / "consumer", context="", count=count)
    request = consumer.read(state["judgment_requests"][0]["job_path"])
    schema = consumer.compact(request["schema"])
    assert "uniqueItems" not in schema and "minLength" not in schema
    response = respond(request)
    response["findings"][0]["question_ids"] = ["foreign-question"]
    consumer.Draft202012Validator(request["schema"]).validate(response)
    with pytest.raises(ValueError, match="foreign question"):
        consumer.validate_response(request, response, count)


def test_compiled_membership_seeded_omission_rejected(tmp_path, monkeypatch):
    args = fixture()
    root = tmp_path / "consumer"
    state = consumer.advance(*args, root, context="", count=count)
    for info in state["judgment_requests"]:
        publish(info, respond(consumer.read(info["job_path"])), tmp_path)
    original = consumer.checked_projection
    def drop_counter(results):
        records, membership = original(results)
        key = next(k for k, refs in membership.items() if refs == ["b::u"])
        del membership[key]
        return [r for r in records if r["handle"] != key], membership
    monkeypatch.setattr(consumer, "checked_projection", drop_counter)
    with pytest.raises(ValueError, match="consumer compiled membership"):
        consumer.advance(*args, root, context="", count=count)


def test_repeated_citations_allowed_but_duplicate_unused_and_true_results_rejected(tmp_path):
    state = consumer.advance(*fixture(), tmp_path / "consumer", context="", count=count)
    request = consumer.read(state["judgment_requests"][0]["job_path"])
    response = respond(request)
    response["findings"][0]["context_refs"] = response["findings"][0]["supporting_refs"][:]
    consumer.validate_response(request, response, count)
    response = {"findings": [], "unused": [{"unit_ref": "a::u", "reason": "No effect."}] * 2}
    with pytest.raises(ValueError, match="coverage"):
        consumer.validate_response(request, response, count)


def test_origin_identity_across_jobs_and_lossless_shape_partition(tmp_path):
    args = fixture()
    for row, identity in zip(args[0]["captured_items"], ("same-person", "same-person", "other-person", None)):
        row.update(independence_key=identity, source_role="customer_experience", independence_posture="credited")
    state, seen = complete(args, tmp_path / "consumer", tmp_path)
    assembly = next(r for r in seen if r["phase"] == "assembly")
    attribution = assembly["payload"]["source_origin_attribution"]
    origins = attribution[0]["origins"]
    assert len(origins) == 2
    assert origins[0]["supporting_finding_indices"] == [0] and origins[0]["opposing_finding_indices"] == [1]
    assert origins[1]["supporting_finding_indices"] == [2]
    manifest = consumer.read(tmp_path / "consumer/membership" / (assembly["payload"]["membership_sha256"] + ".json"))
    assert manifest["original_origin_identities"] == {"0": "same-person", "1": "other-person"}
    records = [{"handle": "f0", "statement": "Opposition remains", "limits": "Only in winter"},
               {"handle": "u1", "unused_reason": "Greeting only"},
               {"handle": "n0", "verified_dispositions": [{"reason": "No product assertion"}]}]
    partitioned = consumer.partition_checked_records(records)
    from judgment.review_evidence import compact_evidence, expand_evidence
    decoded = expand_evidence(compact_evidence(partitioned))
    assert [r for group in decoded.values() for r in group] == records
    assert len(consumer.compact(decoded)) > 0


def test_public_delivery_is_exact_measured_envelope_and_unknown_identity_is_not_minted(tmp_path):
    state = consumer.advance(*fixture(), tmp_path / "consumer", context="context", count=count)
    info = state["judgment_requests"][0]
    request = consumer.read(info["job_path"])
    actor_path = Path(info["job_path"]).with_name("actor-input.json")
    actor = consumer.read(actor_path)
    assert set(actor) == {"prompt", "response_schema"}
    assert count(consumer.compact(actor)) == request["measurement"]["input_and_schema_tokens"]
    assert info["measurement"]["handoff_instruction_tokens"] > 0
    assert info["measurement"]["total_reserved_tokens"] > request["measurement"]["total_reserved_tokens"]
    response = respond(request)
    records, membership = consumer.checked_projection([(request, response)])
    attribution, identities = consumer.origin_projection([(request, response)], membership)
    assert not identities and attribution[0]["origins"][0]["origin"] == "unknown"


def test_worker_handoff_capacity_blocks_before_dispatch(tmp_path):
    args = fixture()
    first = consumer.advance(*args, tmp_path / "sizing", context="", count=count)
    request = consumer.read(first["judgment_requests"][0]["job_path"])
    args[4]["effective_context_tokens"] = request["measurement"]["total_reserved_tokens"] + 100
    with pytest.raises(ValueError, match="worker handoff"):
        consumer.advance(*args, tmp_path / "bounded", context="", count=count)


def test_model_fitting_oversized_intake_automatically_uses_bounded_transport(tmp_path):
    import subprocess
    import sys
    args = fixture()
    args[0]["captured_items"][0]["text"] = "bounded evidence " * 20000
    args[4]["effective_context_tokens"] = 1000000
    root = tmp_path / "consumer"
    state = consumer.advance(*args, root, context="", count=count)
    info = state["judgment_requests"][0]
    assert info["measurement"]["intake_transport_mode"] == "bounded_sections_v1"
    assert "--delivery-manifest" in info["worker_prompt"]
    path = Path(info["job_path"])
    request = consumer.read(path)
    assert request["measurement"]["total_reserved_tokens"] < args[4]["effective_context_tokens"]
    result = subprocess.run([sys.executable, "-m", "runners.run_semantic_evidence_integration",
        "intake-judgment-job", "--job", str(path), "--job-sha256", request["request_sha256"]],
        cwd=Path(__file__).parents[2], capture_output=True, check=True)
    # Real CLI serialization, not an inferred prompt-only size.
    assert len(result.stdout) > 60000
    assert json.loads(result.stdout)["intake_end"] == request["request_sha256"]
    assert not list(root.glob("requests/*/response.json"))


@pytest.mark.parametrize("fault", ["none", "truncated", "missing", "changed_job", "corrupt_content"])
def test_generated_chunk_delivery_validates_actual_envelope_hashes_and_refuses_faults(tmp_path, fault):
    import hashlib
    import subprocess
    from runners.run_semantic_evidence_integration import intake_judgment_job, _chunked_judgment_delivery_script
    args = fixture()
    args[0]["captured_items"][0]["text"] = "Unicode \U0001f600 source " * 5000
    args[4]["effective_context_tokens"] = 1000000
    state = consumer.advance(*args, tmp_path / "consumer", context="", count=count)
    info = state["judgment_requests"][0]
    path, key = Path(info["job_path"]), info["job_sha256"]
    complete = intake_judgment_job(job_path=path, expected_sha256=key)
    manifest = intake_judgment_job(job_path=path, expected_sha256=key, delivery_manifest=True)
    chunks = {}
    for section, total in manifest["content_bytes"].items():
        offset = 0
        while offset < total:
            chunk = intake_judgment_job(job_path=path, expected_sha256=key,
                delivery_section=section, delivery_offset=offset)
            assert len(chunk["content"].encode()) <= 8000
            assert hashlib.sha256(chunk["content"].encode()).hexdigest() == chunk["chunk_sha256"]
            chunks[f"{section}:{offset}"] = chunk
            offset = chunk["to_byte"]
    script = _chunked_judgment_delivery_script({"cmd": "intake", "max_output_tokens": 60000}, "intake", key)
    script_path = tmp_path / "delivery.js"
    script_path.write_text(script, encoding="utf-8")
    harness = r'''
const fs=require('fs'), crypto=require('crypto');
const fixture=JSON.parse(fs.readFileSync(0,'utf8'));
const script=fs.readFileSync(process.argv[1],'utf8');
const messages=[];let stored=null;
const tools={exec_command:async execution=>{
 if(execution.cmd.endsWith('--delivery-manifest'))return {exit_code:0,output:JSON.stringify(fixture.manifest)};
 const match=execution.cmd.match(/--delivery-section '([^']+)' --delivery-offset (\d+)$/);
 const chunk=structuredClone(fixture.chunks[match[1]+':'+match[2]]);
 if(fixture.fault==='truncated')return {exit_code:0,original_token_count:60001,output:JSON.stringify(chunk)};
 if(fixture.fault==='missing')return {exit_code:0,output:'{}'};
 if(fixture.fault==='changed_job')return {exit_code:2,output:'job hash mismatch'};
 if(fixture.fault==='corrupt_content')chunk.content='X'+chunk.content.slice(1);
 return {exit_code:0,output:JSON.stringify(chunk)};
}};
const run=new (Object.getPrototypeOf(async function(){}).constructor)('tools','notify','store','text','exit',script);
run(tools,x=>messages.push(x),(k,v)=>stored=v,x=>messages.push(x),()=>{throw Error('delivery stopped');})
.catch(error=>{if(error.message!=='delivery stopped')throw error;})
.then(()=>console.log(JSON.stringify({
 completed:messages.some(x=>typeof x==='object'&&x.intake_end),
 failure:messages.some(x=>typeof x==='object'&&x.status==='INCOMPLETE_INTAKE'),
 hashes:stored?Object.fromEntries(Object.entries(stored.content).map(([k,v])=>[k,crypto.createHash('sha256').update(v).digest('hex')])):{}
})));
'''
    result = subprocess.run(["node", "-e", harness, str(script_path)],
        input=json.dumps({"manifest": manifest, "chunks": chunks, "fault": fault}),
        text=True, capture_output=True, check=True)
    delivered = json.loads(result.stdout)
    if fault == "none":
        assert delivered["completed"] and not delivered["failure"]
        assert delivered["hashes"] == {k: hashlib.sha256(v.encode()).hexdigest() for k, v in complete["content"].items()}
    else:
        assert delivered["failure"] and not delivered["completed"] and not delivered["hashes"]


def test_chunk_intake_revalidates_changed_job_and_refuses_mid_codepoint_offset(tmp_path):
    from runners.run_semantic_evidence_integration import intake_judgment_job
    args = fixture()
    state = consumer.advance(*args, tmp_path / "consumer", context="\U0001f600", count=count)
    info = state["judgment_requests"][0]
    path, key = Path(info["job_path"]), info["job_sha256"]
    intake_judgment_job(job_path=path, expected_sha256=key, delivery_manifest=True)
    with pytest.raises(UnicodeDecodeError):
        intake_judgment_job(job_path=path, expected_sha256=key, delivery_section="prompt", delivery_offset=1)
    request = consumer.read(path)
    request["prompt"] += " changed"
    path.write_text(json.dumps(request))
    with pytest.raises(ValueError, match="identity mismatch"):
        intake_judgment_job(job_path=path, expected_sha256=key, delivery_section="prompt", delivery_offset=0)


def test_missing_accepted_response_blocks_instead_of_reissuing_judgment(tmp_path):
    args = fixture()
    root = tmp_path / "consumer"
    state = consumer.advance(*args, root, context="", count=count)
    info = state["judgment_requests"][0]
    publish(info, respond(consumer.read(info["job_path"])), tmp_path)
    Path(info["response_path"]).unlink()
    with pytest.raises(ValueError, match="restore its bound bytes"):
        consumer.advance(*args, root, context="", count=count)


def test_local_reuse_check_evidence_and_answer_dependencies(tmp_path):
    args = fixture()
    root = tmp_path / "consumer"
    state, _ = complete(args, root, tmp_path)
    args[3]["assessment_only"]["checks"][0]["expectation"] = "Preserve actual stopping, not intent."
    state2, seen = complete(args, root, tmp_path)
    assert [r["phase"] for r in seen] == ["answer_review"]
    args[0]["captured_items"][0]["text"] += " Only in winter."
    state3, seen = complete(args, root, tmp_path)
    assert [r["phase"] for r in seen] == ["source_review", "assembly", "answer_review"]
    assert Path(state["answer_path"]).exists() and Path(state2["answer_path"]).exists()
    review = seen[-1]
    changed = deepcopy(review["payload"])
    changed["answer"]["answers"][0]["answer"] = "Different conclusion."
    successor = consumer.build_request("answer_review", changed, args[4], "claim support fixture", count)
    assert successor["request_sha256"] != review["request_sha256"]


def test_indivisible_and_aggregate_capacity_and_output(tmp_path):
    args = fixture()
    args[0]["captured_items"][0]["text"] = "x" * 100000
    with pytest.raises(ValueError, match="capacity exceeded at source_review"):
        consumer.advance(*args, tmp_path / "consumer", context="", count=count)
    args = fixture()
    state = consumer.advance(*args, tmp_path / "small", context="", count=count)
    for info in state["judgment_requests"]:
        request = consumer.read(info["job_path"])
        response = respond(request)
        response["findings"][0]["statement"] = "z" * 13000
        publish(info, response, tmp_path)
    args[4]["effective_context_tokens"] = 30000
    # Capacity is part of request identity; same accepted source results cannot
    # silently use different budgets. Direct aggregate builder isolates failure.
    payload = {"commission": args[3], "unit_ids": ["f"], "checked_findings_and_unused": ["z" * 20000]}
    with pytest.raises(ValueError, match="capacity exceeded at assembly"):
        consumer.build_request("assembly", payload, args[4], "context" * 100, count)
    args[4]["effective_context_tokens"] = 100000
    request = consumer.build_request("assembly", payload, args[4], "", count)
    response = {"answers": [{"question_id": "q", "answer": "z" * 16000, "evidence_refs": [], "limits": "None."}]}
    with pytest.raises(ValueError, match="output exceeds"):
        consumer.validate_response(request, response, count)


def test_original_reopening_and_failed_review_are_visible(tmp_path):
    args = fixture()
    root = tmp_path / "consumer"
    for _ in range(5):
        state = consumer.advance(*args, root, context="", count=count)
        for info in state["judgment_requests"]:
            request = consumer.read(info["job_path"])
            response = respond(request)
            if request["phase"] == "answer_review":
                response["answers"][0].update(status="unresolved", reason="Need original mitigation context.")
                response["reopen_refs"] = [request["payload"]["unit_ids"][2]]
            elif request["phase"] == "reopen":
                assert "New cap" in request["prompt"]
            elif request["phase"] == "answer_review_after_reopen":
                response["answers"][0].update(status="defect", reason="Current universal claim is unsupported.")
            publish(info, response, tmp_path)
    state = consumer.advance(*args, root, context="", count=count)
    assert state["status"] == "COMPLETE_CASE_ANSWER_REQUIRES_REVISION"


def test_public_normal_advance_reaches_consumer_end_to_end(tmp_path, capsys, monkeypatch):
    import test_semantic_evidence_integration as native
    from runners.run_semantic_evidence_integration import main
    import runners.finite_preparation as preparation

    class Tokenizer:
        def encode(self, text, **_):
            return text.encode("utf-8")
    monkeypatch.setattr(preparation, "offline_tokenizer", lambda _: (Tokenizer(), "fixture"))
    source, replay, expected = native._advance_replay_fixture(tmp_path)
    from runners.run_semantic_evidence_integration import advance_semantic_run
    saved = tmp_path / "saved"
    for phase, responses in replay.items():
        native._publish_advance_replay(saved, phase, responses)
    assert advance_semantic_run(source_path=source, run_dir=saved, max_prompt_bytes=30000,
        max_evidence_per_work_unit=2)["status"] == "SEMANTIC_EVIDENCE_INTEGRATION_COMPLETE"
    run = tmp_path / "run"
    for phase, responses in replay.items():
        if phase.startswith("reconciliation"):
            native._publish_advance_replay(run, phase, responses)
    args = fixture()
    args[3]["assessment_only"]["checks"] = []
    commission, capacity = tmp_path / "commission.json", tmp_path / "capacity.json"
    commission.write_text(json.dumps(args[3]), encoding="utf-8")
    capacity.write_text(json.dumps(args[4]), encoding="utf-8")
    command = ["advance", "--source", str(source), "--run-dir", str(run),
        "--bundle", str(saved / "bundle.json"), "--verified", str(saved / "verification/compilation.json"), "--max-prompt-bytes", "30000",
        "--max-evidence-per-work-unit", "2", "--answer-commission", str(commission), "--answer-capacity", str(capacity)]
    phases = []
    for _ in range(5):
        assert main(command) == 0
        state = json.loads(capsys.readouterr().out)
        for info in state["judgment_requests"]:
            assert main(["intake-judgment-job", "--job", info["job_path"], "--job-sha256", info["job_sha256"]]) == 0
            intake = json.loads(capsys.readouterr().out)
            assert set(intake["content"]) == {"prompt", "response_schema"}
            assert intake["intake_end"] == info["job_sha256"]
            request = consumer.read(info["job_path"])
            assert intake["content"]["prompt"] == request["prompt"]
            phases.append(request["phase"])
            response = respond(request)
            if request["phase"] == "answer_review":
                nominate_exact_repair(request, response)
            raw = tmp_path / "response.json"
            raw.write_text(json.dumps(response), encoding="utf-8")
            assert main(["submit-judgment-job", "--job", info["job_path"], "--job-sha256",
                info["job_sha256"], "--response", str(raw)]) == 0
            capsys.readouterr()
    assert state["status"] == "COMPLETE_CASE_ANSWER_CHECKED"
    assert consumer.read(run / "view.json") == expected
    assert consumer.read(state["answer_path"])["coverage"]["source_rows"] > 0

    assert "extraction" not in phases and "verification" not in phases
    assert phases[-3:] == ["assembly", "answer_review", "correction_recheck"]
    assert not (run / "extraction").exists()
    assert main(command) == 0
    resumed = json.loads(capsys.readouterr().out)
    assert resumed["judgment_requests"] == [] and resumed["answer_sha256"] == state["answer_sha256"]

    # Real preload headers carry checkout paths. Moving unchanged authority must
    # preserve every accepted request and the final corrected answer byte-for-byte.
    from runners import run_finite_semantic_consolidation as finite
    moved = tmp_path / "another-checkout"
    copied_context = []
    for path in finite.CONTEXT:
        copy = moved / path.relative_to(finite.REPO)
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_bytes(path.read_bytes())
        copied_context.append(copy)
    before = {str(p): p.read_bytes() for p in (run / "consumer").rglob("*.json")}
    monkeypatch.setattr(finite, "CONTEXT", copied_context)
    monkeypatch.setattr(finite, "REPO", moved)
    assert main(command) == 0
    relocated = json.loads(capsys.readouterr().out)
    assert relocated == resumed
    assert before == {str(p): p.read_bytes() for p in (run / "consumer").rglob("*.json")}

    for bad in ({k: v for k, v in args[4].items() if k != "encoding"},
                {**args[4], "encoding": " "}, {**args[4], "encoding": None}):
        capacity.write_text(json.dumps(bad), encoding="utf-8")
        assert main(command) == 2
        blocked = json.loads(capsys.readouterr().out)
        assert blocked["status"] == "SEMANTIC_ADVANCE_BLOCKED"
        assert "encoding" in blocked["error"]
        assert blocked["judgment_requests"] == []
    assert before == {str(p): p.read_bytes() for p in (run / "consumer").rglob("*.json")}


def nominate_exact_repair(request, response):
    from judgment.review_evidence import answer_identity
    answer = request["payload"]["answer"]
    response["answers"][0].update(status="defect", reason="Exact bounded answer defect.")
    response["material_findings"] = [{"severity": "major", "introduced_at": "current_answer", "status": "open",
        "source_refs": ["f0"], "artifact_refs": ["current_answer:q"], "defect": "Overbroad text.",
        "effect": "Wrong scope.", "bounded_repair": "Replace the single scoped phrase."}]
    response["answer_repairs"] = {"answer_sha256": answer_identity(answer), "edits": [
        {"question_id": "q", "field": "answer", "before": "Mixed experience", "after": "Conditional mixed experience",
         "source_refs": ["f0"]}]}
    return response


@pytest.mark.parametrize("recheck_passes", [True, False])
def test_exact_correction_recheck_reuses_sources_and_retains_original(tmp_path, recheck_passes):
    args = fixture()
    args[3]["questions"].append({"id": "q2", "question": "What is the unchanged limitation?"})
    root = tmp_path / "consumer"
    phases, originals, candidate, source_bytes = [], None, None, {}
    for _ in range(7):
        state = consumer.advance(*args, root, context="", count=count)
        for info in state["judgment_requests"]:
            request = consumer.read(info["job_path"])
            phases.append(request["phase"])
            response = respond(request)
            if request["phase"] == "assembly":
                response["answers"].append({"question_id": "q2", "answer": "Unchanged bounded text.", "limits": "Unchanged limits.", "evidence_refs": ["f1"]})
                originals = deepcopy(response)
            elif request["phase"] not in {"source_review", "reopen"}:
                response["answers"].append({"question_id": "q2", "status": "pass", "reason": "Unchanged."})
            if request["phase"] == "answer_review":
                nominate_exact_repair(request, response)
            if request["phase"] == "correction_recheck":
                assert "source_groups" not in request["payload"]
                candidate = request["payload"]["answer"]
                assert candidate["answers"][1] == originals["answers"][1]
                if not recheck_passes:
                    response["answers"][0].update(status="defect", reason="Repair failed independent check.")
            publish(info, response, tmp_path)
            if request["phase"] == "source_review":
                source_bytes[info["response_path"]] = Path(info["response_path"]).read_bytes()
        if not state["judgment_requests"]:
            break
    assert phases == ["source_review"] * 3 + ["assembly", "answer_review", "correction_recheck"]
    result = consumer.read(state["answer_path"])
    assert result["correction"]["original_answer"] == originals
    assert result["correction"]["candidate_answer"] == candidate
    assert result["correction"]["status"] == ("accepted" if recheck_passes else "rejected")
    assert result["answer"]["answers"][0]["answer"] == (candidate if recheck_passes else originals)["answers"][0]["answer"]
    assert state["status"] == ("COMPLETE_CASE_ANSWER_CHECKED" if recheck_passes else "COMPLETE_CASE_ANSWER_REQUIRES_REVISION")
    assert consumer.advance(*args, root, context="", count=count) == state
    assert all(Path(path).read_bytes() == raw for path, raw in source_bytes.items())


def test_response_published_before_receipt_recovers_without_new_judgment(tmp_path, monkeypatch):
    args = fixture()
    root = tmp_path / "consumer"
    state = consumer.advance(*args, root, context="", count=count)
    info = state["judgment_requests"][0]
    real = consumer.retain
    def interrupted(path, value):
        if Path(path).name == "response.receipt.json":
            raise OSError("injected interruption after response publication")
        return real(path, value)
    with monkeypatch.context() as scoped:
        scoped.setattr(consumer, "retain", interrupted)
        with pytest.raises(OSError, match="injected interruption"):
            publish(info, respond(consumer.read(info["job_path"])), tmp_path)
    accepted = Path(info["response_path"]).read_bytes()
    resumed = consumer.advance(*args, root, context="", count=count)
    assert info["job_sha256"] not in {r["job_sha256"] for r in resumed["judgment_requests"]}
    assert Path(info["response_path"]).read_bytes() == accepted
    assert Path(info["response_path"]).with_name("response.receipt.json").exists()


def test_lost_accepted_response_is_never_replaced_by_a_later_submission(tmp_path):
    args = fixture()
    state = consumer.advance(*args, tmp_path / "consumer", context="", count=count)
    info = state["judgment_requests"][0]
    publish(info, respond(consumer.read(info["job_path"])), tmp_path)
    target = Path(info["response_path"])
    target.unlink()
    later = respond(consumer.read(info["job_path"]))
    later["findings"][0]["limits"] = "A different, later judgment."
    with pytest.raises(ValueError, match="restore its bound bytes"):
        publish(info, later, tmp_path)
    assert not target.exists()


def test_public_submit_reports_schema_invalid_consumer_response_without_publishing(tmp_path, capsys, monkeypatch):
    from runners.run_semantic_evidence_integration import main
    import runners.finite_preparation as preparation

    class Tokenizer:
        def encode(self, text, **_):
            return text.encode("utf-8")
    monkeypatch.setattr(preparation, "offline_tokenizer", lambda _: (Tokenizer(), "fixture"))
    state = consumer.advance(*fixture(), tmp_path / "consumer", context="", count=count)
    info = state["judgment_requests"][0]
    raw = tmp_path / "raw.json"
    raw.write_text(json.dumps({"findings": "not an array", "unused": []}), encoding="utf-8")
    assert main(["submit-judgment-job", "--job", info["job_path"], "--job-sha256", info["job_sha256"],
                 "--response", str(raw)]) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "error"
    assert not Path(info["response_path"]).exists()


def test_staged_partial_response_never_reissued_or_accepted(tmp_path):
    args = fixture()
    root = tmp_path / "consumer"
    state = consumer.advance(*args, root, context="", count=count)
    target = Path(state["judgment_requests"][0]["response_path"])
    target.with_name("response.json.tmp").write_text('{"findings":', encoding="utf-8")
    with pytest.raises(ValueError, match="staged consumer response"):
        consumer.advance(*args, root, context="", count=count)
    assert not target.exists()


@pytest.mark.parametrize("scope", ["uncertain", "current_consolidation", "legacy"])
def test_unclassified_and_upstream_only_defects_never_gain_answer_repair_authority(tmp_path, scope):
    args = fixture()
    root = tmp_path / "consumer"
    for _ in range(5):
        state = consumer.advance(*args, root, context="", count=count)
        for info in state["judgment_requests"]:
            request = consumer.read(info["job_path"])
            response = respond(request)
            if request["phase"] == "answer_review":
                if scope == "legacy":
                    payload = {k: v for k, v in request["payload"].items() if k != "correction_policy"}
                    legacy = consumer.build_request("answer_review", payload, args[4], "", count)
                    directory = root / "requests" / legacy["request_sha256"]
                    consumer.retain(directory / "request.json", legacy)
                    info = {"job_path": str(directory / "request.json"), "job_sha256": legacy["request_sha256"]}
                    response = respond(legacy)
                    response["answers"][0].update(status="defect", reason="Old schema does not classify repair scope.")
                else:
                    nominate_exact_repair(request, response)
                    response["material_findings"][0]["introduced_at"] = scope
            assert request["phase"] != "correction_recheck"
            publish(info, response, tmp_path)
        if not state["judgment_requests"]:
            break
    assert state["status"] == "COMPLETE_CASE_ANSWER_REQUIRES_REVISION"
    assert consumer.advance(*args, root, context="", count=count) == state


def test_consumer_request_identity_stable_across_real_hash_seed_processes(tmp_path):
    import os
    import subprocess
    import sys
    script = '''
from judgment.complete_case_consumer import build_request
payload = {k: v for k, v in {("z", 3), ("a", 1), ("b", 2)}}
payload.update(commission={"questions": [{"id": "q", "question": "Bound question"}]}, unit_ids=["u"])
capacity = {"effective_context_tokens": 100000, "output_reserve_tokens": 1000, "other_overhead_reserve_tokens": 1000}
print(build_request("source_review", payload, capacity, "context", len)["request_sha256"])
'''
    outputs = [subprocess.run([sys.executable, "-c", script], cwd=Path(__file__).parents[2],
        env={**os.environ, "PYTHONHASHSEED": str(seed)}, capture_output=True, text=True, check=True).stdout
        for seed in (1, 2, 3)]
    assert len(set(outputs)) == 1


def test_legacy_ordered_transport_reuse_and_conflicting_judgments_fail(tmp_path):
    from judgment.review_evidence import RENDERING_GUIDANCE, expand_evidence, render_evidence
    args = fixture()
    root = tmp_path / "consumer"
    state = consumer.advance(*args, root, context="", count=count)
    current = consumer.read(state["judgment_requests"][0]["job_path"])
    marker = RENDERING_GUIDANCE + "\n\n"
    prefix, envelope = current["prompt"].rsplit(marker, 1)
    payload = expand_evidence(json.loads(envelope))
    legacy = deepcopy(current)
    legacy["prompt"] = prefix + render_evidence(dict(reversed(list(payload.items()))))
    measured = count(consumer.compact({"prompt": legacy["prompt"], "response_schema": legacy["schema"]}))
    legacy["measurement"].update(input_and_schema_tokens=measured,
        total_reserved_tokens=measured + args[4]["output_reserve_tokens"] + args[4]["other_overhead_reserve_tokens"])
    legacy.pop("request_sha256")
    legacy["request_sha256"] = consumer.digest(legacy)
    assert legacy["request_sha256"] != current["request_sha256"]
    directory = root / "requests" / legacy["request_sha256"]
    consumer.retain(directory / "request.json", legacy)
    info = {"job_path": str(directory / "request.json"), "job_sha256": legacy["request_sha256"]}
    publish(info, respond(legacy), tmp_path)
    resumed = consumer.advance(*args, root, context="", count=count)
    assert len(resumed["judgment_requests"]) == 2  # old accepted source not rejudged
    different = respond(current)
    different["findings"][0]["limits"] = "A different accepted judgment."
    publish(state["judgment_requests"][0], different, tmp_path)
    with pytest.raises(ValueError, match="conflicting saved judgments"):
        consumer.advance(*args, root, context="", count=count)


@pytest.mark.parametrize("changed", ["contents", "logical_path", "forged_hash", "conflicting_judgment"])
def test_checkout_context_reuse_preserves_exact_authority_and_conflicts(tmp_path, changed):
    from runners.run_codex_provider_attempt import preloaded_context
    args = fixture()
    root = tmp_path / "consumer"
    old = tmp_path / "old" / "AGENTS.md"
    new = tmp_path / "new" / "AGENTS.md"
    for p in (old, new):
        p.parent.mkdir()
        p.write_bytes(b"Preserve all evidence.\nEND SOURCE\nThis is still source content.\n")
    context, _ = preloaded_context([old])
    first = consumer.advance(*args, root, context=context, count=count)
    info = first["judgment_requests"][0]
    request = consumer.read(info["job_path"])
    publish(info, respond(request), tmp_path)
    current_context, _ = preloaded_context([new])
    reused = consumer.advance(*args, root, context=current_context, count=count)
    assert [r["job_sha256"] for r in reused["judgment_requests"]] == [
        r["job_sha256"] for r in first["judgment_requests"][1:]]

    if changed == "conflicting_judgment":
        alternate = consumer.build_request("source_review", request["payload"], args[4], current_context, count)
        path = root / "requests" / alternate["request_sha256"] / "request.json"
        consumer.retain(path, alternate)
        response = respond(alternate)
        response["findings"][0]["limits"] = "A different accepted judgment."
        publish({"job_path": str(path), "job_sha256": alternate["request_sha256"]}, response, tmp_path)
        with pytest.raises(ValueError, match="conflicting saved judgments"):
            consumer.advance(*args, root, context=current_context, count=count)
        return
    if changed == "logical_path":
        renamed = new.with_name("DIFFERENT.md")
        renamed.write_bytes(new.read_bytes())
        current_context, _ = preloaded_context([renamed])
    else:
        changed_context = current_context.replace("Preserve all evidence.", "Discard contrary evidence.")
        if changed == "forged_hash":
            with pytest.raises(ValueError, match="context.*hash"):
                consumer.advance(*args, root, context=changed_context, count=count)
            return
        new.write_text("Discard contrary evidence.", encoding="utf-8")
        current_context, _ = preloaded_context([new])
    changed_state = consumer.advance(*args, root, context=current_context, count=count)
    assert len(changed_state["judgment_requests"]) == len(first["judgment_requests"])
    assert not {r["job_sha256"] for r in first["judgment_requests"]} & {
        r["job_sha256"] for r in changed_state["judgment_requests"]}


@pytest.mark.parametrize("command", ["submit-judgment-job", "submit-consumer-response"])
def test_public_submit_rejects_missing_encoding_before_tokenization(tmp_path, capsys, monkeypatch, command):
    from runners.run_semantic_evidence_integration import main
    import runners.finite_preparation as preparation
    def no_tokenizer(_):
        pytest.fail("malformed capacity must fail before tokenizer lookup")
    monkeypatch.setattr(preparation, "offline_tokenizer", no_tokenizer)
    state = consumer.advance(*fixture(), tmp_path / "consumer", context="", count=count)
    request = consumer.read(state["judgment_requests"][0]["job_path"])
    del request["capacity"]["encoding"]
    request.pop("request_sha256")
    request["request_sha256"] = consumer.digest(request)
    path = tmp_path / "malformed" / "request.json"
    consumer.retain(path, request)
    raw = tmp_path / "raw.json"
    raw.write_text(json.dumps(respond(request)), encoding="utf-8")
    assert main([command, "--job", str(path), "--job-sha256", request["request_sha256"],
                 "--response", str(raw)]) == 2
    assert "encoding" in json.loads(capsys.readouterr().out)["error"]
    assert not path.with_name("response.json").exists()
