"""Read a saved finite endpoint for bounded human/agent judgment; never run jobs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from jsonschema import ValidationError

from harness_utils import hash_file
from judgment.review_evidence import compact_evidence, expand_evidence, RENDERING_GUIDANCE
from reports.compact_return import bounded_json, output_budget, write_verified
from reports.efficiency_codex import collect_provider_roots


def failure_summary(run_root, provider_root):
    """Compact saved observations for a failed run, never endpoint validation.

    The exception remains owned by the caller. Missing, unreadable or changed
    diagnostics are explicit and cannot turn that exception into success.
    """
    from harness_efficiency import aggregate_usage
    from judgment.review_evidence import material_answer_findings
    root, providers = Path(run_root).resolve(), Path(provider_root).resolve()
    artifacts, issues = {}, []

    def optional(name):
        path = root / name
        if not path.exists():
            return None
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(value, dict):
                raise ValueError("expected object")
            artifacts[name] = {"path": str(path), "sha256": hash_file(path)}
            return value
        except (OSError, ValueError) as exc:
            issues.append(f"{name}: {exc}")
            return None

    counts = optional("coverage.json")
    for name in ("formation/compilation.json", "finish/compilation.json", "answer/freeze.json",
                 "answer-correction/composition.json", "assessment-recheck/result.json"):
        optional(name)
    assessment, repair_scope = None, None
    record = optional("assessment/result.json")
    if record is not None:
        try:
            path = Path(record["response"]).resolve(strict=True)
            if not path.is_relative_to(providers) or hash_file(path) != record["response_sha256"]:
                raise ValueError("assessment response is outside its provider scope or changed")
            value = json.loads(path.read_text(encoding="utf-8"))
            findings = value["material_findings"]
            affected = {ref.removeprefix("current_answer:") for finding in material_answer_findings(findings)
                        for ref in finding["artifact_refs"] if ref.startswith("current_answer:")}
            edited = {edit["question_id"] for edit in value.get("answer_repairs", {}).get("edits", [])}
            repair_scope = {"nominated_question_ids": sorted(affected), "edited_question_ids": sorted(edited),
                            "unedited_nominated_question_ids": sorted(affected - edited)}
            assessment = {"response": record, "semantic_status": "initial reviewer claims; not final acceptance",
                          "commissioned_checks": {key: check["status"] for key, check in value.get("commissioned_checks", {}).items()},
                          "material_findings": findings}
        except (OSError, ValueError, KeyError, TypeError) as exc:
            issues.append(f"assessment response: {exc}")
    accounting = collect_provider_roots([str(providers)])
    stages = {}
    for attempt in accounting["attempts"]:
        path = Path(attempt["receipt_path"]).resolve()
        stage = path.relative_to(providers).parts[0] if path.is_relative_to(providers) else "external_recovery"
        stages.setdefault(stage, []).append(attempt)
    usage_by_stage = {}
    for stage, attempts in stages.items():
        usage = aggregate_usage(attempts)
        usage_by_stage[stage] = {"attempts": len(attempts), "coverage": usage["coverage"],
            **{key: usage[key] for key in ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens")},
            "observed_total_tokens": usage["observed_totals"]["total_tokens"],
            "additional_observed_response_tokens": sum(a["additional_observed_response_tokens"] or 0 for a in attempts),
            "startup_observation_unknown_attempts": sum(a["additional_observed_response_tokens"] is None for a in attempts)}
    return {"schema_version": "finite_failure_diagnostics_v1",
            "scope": "saved diagnostic observations only; no complete endpoint, final selection or semantic acceptance",
            "run_root": str(root), "provider_root": str(providers), "coverage": counts,
            "saved_artifacts": artifacts, "initial_assessment": assessment, "repair_scope": repair_scope,
            "native_accounting": {k: v for k, v in accounting.items() if k != "attempts"},
            "usage_by_stage": usage_by_stage, "diagnostic_issues": issues}


def selected_answer_path(result, frozen_path, candidate_path, frozen, candidate, recheck, *, assessment=None, request=None):
    """Verify the saved selection through the same decision used by the live runner."""
    from judgment.review_evidence import correction_selection
    if result["answer_corrections"] not in (0, 1) or result["affected_rechecks"] not in (0, 1):
        raise ValueError("invalid finite correction/recheck counts")
    expected = Path(frozen_path).resolve()
    if result["affected_rechecks"]:
        if result["answer_corrections"] != 1 or recheck is None or candidate is None:
            raise ValueError("recheck lacks a correction candidate")
        decision = correction_selection(frozen, candidate, assessment or {"material_findings": []}, recheck, request)
        if any(result[key] != decision[key] for key in ("answer_correction_status", "answer_correction_failed_checks")):
            raise ValueError("saved correction acceptance differs from existing rules")
        if decision["answer_correction_status"] in {"accepted", "selected_requires_adjudication"}:
            expected = Path(candidate_path).resolve()
    if Path(result["final_answer"]).resolve() != expected:
        raise ValueError("selected answer is not authorized by saved selection")
    return expected


def check_material_status(result, assessment, recheck=None):
    from judgment.review_evidence import correction_material_status
    expected = correction_material_status(assessment, result.get("answer_correction_status"), recheck)
    if any(result[key] != value for key, value in expected.items()):
        raise ValueError("saved material status differs from reported findings and selection")


def composed_correction(composition, original, patch, questions, *, assessment=None, known_refs=None, unit_sources=None):
    """Recompose the saved candidate with the rule the runner used for this correction shape.

    A post-assessment proposal reports retained answers separately and the runner
    copies those from the original; only the pre-freeze repair response is itself
    the patch. Recomposing both shapes the same way would refuse a saved run whose
    correction legitimately retained an affected answer.
    """
    from runners import run_finite_semantic_consolidation as finite
    affected = composition["affected_question_ids"]
    if composition.get("method") in {"reviewer_exact_repairs_v1", "reviewer_exact_repairs_v2"}:
        if assessment is None or patch != assessment.get("answer_repairs"):
            raise ValueError("exact repairs differ from bound reviewer response")
        nominated = finite.material_answer_findings(assessment["material_findings"])
        reference_errors = {row["question_id"]: sorted(refs) for row in original["answers"]
            if (refs := finite.answer_source_references(row, known_refs) - known_refs)}
        expected = {r.removeprefix("current_answer:") for f in nominated for r in f["artifact_refs"]
                    if r.startswith("current_answer:")}
        expected.update(reference_errors)
        if set(affected) != expected:
            raise ValueError("exact repair composition scope differs")
        return finite.apply_exact_answer_repairs(original, patch, nominated, known_refs, reference_errors,
                                                 unit_sources=unit_sources,
                                                 allow_retained=composition["method"] == "reviewer_exact_repairs_v2")
    if patch.get("schema_version") == "finite_answer_correction_v1":
        scoped = [q for q in questions if q["id"] in set(affected)]
        patch = finite.answer_correction_patch(original, patch, scoped)
    return finite.compose_answer_patch(original, patch, affected)


def evidence_view(source, verified, view, questions):
    """Select by commissioned anchors, then retain every relation of touched findings.

    This is a bounded closeout, not another exhaustive inventory assessment. No
    ranking, excerpting, severity filtering, or semantic compression occurs.
    """
    checks = questions["assessment_only"]["checks"]
    if not checks or len({c["id"] for c in checks}) != len(checks):
        raise ValueError("closeout requires unique commissioned checks")
    rows = {r["evidence_id"]: r for r in source["captured_items"]}
    units = {u["semantic_unit_ref"]: u for u in verified["semantic_units"]}
    anchors = {r for c in checks for r in c["source_rows"]}
    if not anchors or anchors - rows.keys():
        raise ValueError("commissioned closeout source anchor missing")
    findings = [p for p in view["propositions"] if anchors & {
        units[r]["evidence_id"] for refs in p["semantic_relations"].values() for r in refs}]
    selected = anchors | {units[r]["evidence_id"] for p in findings
                          for refs in p["semantic_relations"].values() for r in refs}
    if selected - rows.keys():
        raise ValueError("closeout finding lineage lacks source rows")
    missing = sorted(r for r in selected if not rows[r].get("text"))
    locators = {rows[r]["source_artifact_id"] for r in selected}
    artifacts = [a for a in source["source_artifacts"] if a["artifact_id"] in locators]
    if {a["artifact_id"] for a in artifacts} != locators:
        raise ValueError("closeout source artifact locator missing")
    return {"commissioned_checks": checks,
            "selection": {"rule": "all check anchors plus all relations of findings touching an anchor; one hop",
                          "anchor_source_ids": sorted(anchors), "included_source_ids": sorted(selected),
                          "omitted_source_ids": sorted(rows.keys() - selected),
                          "missing_source_body_ids": missing,
                          "scope": "bounded commissioned checks; not an exhaustive inventory or every answer citation audit",
                          "wider_inspection_required_when": "a check needs evidence outside these rows, a body is missing, "
                          "or a question concerns another finding, residual, citation, or saved assessment nomination"},
            "source_context": {k: v for k, v in source.items() if k not in {"captured_items", "source_artifacts"}},
            "source_rows": [r for r in source["captured_items"] if r["evidence_id"] in selected],
            "source_artifacts": artifacts,
            "verified_units": [u for u in verified["semantic_units"] if u["evidence_id"] in selected],
            "evidence_dispositions": [d for d in verified["evidence_dispositions"] if d["evidence_id"] in selected],
            "findings": findings,
            "residuals": [u for u in view["unmerged_semantic_units"]
                          if units[u["semantic_unit_ref"]]["evidence_id"] in selected]}


def collect(run_root, operation_dir=None, *, failure_record=None, snapshot_manifest=None):
    if failure_record is not None:
        from reports.finite_failure_evidence import collect_failure
        return collect_failure(run_root, failure_record, operation_dir, snapshot_manifest)
    if snapshot_manifest is not None:
        raise ValueError("snapshot manifest requires an explicit failure record")
    # Import only read/validation routines; FiniteRun (and therefore job launch,
    # repair, resume, locks and persistence) is deliberately never instantiated.
    from runners import run_finite_semantic_consolidation as finite
    from provider_jobs import _check_attempt
    read = finite.read
    root = Path(run_root).resolve(strict=True)
    manifest = {}

    def load(path, expected=None):
        path = Path(path).resolve(strict=True)
        digest = hash_file(path)
        if expected is not None and digest != expected:
            raise ValueError(f"saved binding changed: {path}")
        value = read(path)
        manifest[str(path)] = digest
        return value

    def bound_response(record):
        return load(record["response"], record["response_sha256"])

    def bound_consumer_input(phase):
        request = load(root / phase / "input.json")
        policy = load(provider_root / phase / "provider/job/binding.json")
        prompt = Path(policy["binding"]["prompt_path"])
        packet = json.loads(prompt.read_text(encoding="utf-8").rstrip().rsplit("\n", 1)[-1])
        if (hash_file(prompt) != policy["binding"]["prompt_sha256"]
                or expand_evidence(packet) != request):
            raise ValueError(f"saved {phase} input differs from provider prompt")
        return request

    binding = load(root / "binding.json")
    if binding.get("replay_from"):
        raise ValueError("historical replay is not a live closeout; inspect its original saved run and replay result separately")
    inputs = {k: load(binding["inputs"][k]["path"], binding["inputs"][k]["sha256"])
              for k in ("source", "bundle", "verified", "questions", "previous_answer")}
    # These are the original runtime bindings, never today's checkout substituted
    # for a historical execution. Missing retired code is an explicit limitation.
    runtime_missing = []
    for path, digest in binding["runtime"].items():
        if not Path(path).is_file():
            runtime_missing.append(path)
        elif hash_file(Path(path)) != digest:
            raise ValueError(f"saved runtime changed: {path}")
    result = load(root / "result.json")
    if result["status"] not in {"FINITE_EXECUTION_COMPLETE_QUALITY_REQUIRES_ADJUDICATION",
                                "FINITE_EXECUTION_RECOVERED_QUALITY_REQUIRES_ADJUDICATION"}:
        raise ValueError("closeout requires a completed live finite endpoint; inspect saved failure artifacts")
    if Path(result["output_dir"]).resolve() != root:
        raise ValueError("result belongs to another run root")
    provider_root = Path(result["provider_root"]).resolve(strict=True)
    if "provider_root" in binding:
        origin = binding["provider_root"]
        original = load(Path(origin["path"]) / "binding.json", origin["binding_sha256"])
        if provider_root != Path(origin["path"]).resolve() or original["inputs"] != binding["inputs"]:
            raise ValueError("provider-root binding differs")
    elif provider_root != root:
        raise ValueError("unbound provider root")
    source, bundle, verified, questions = (inputs[k] for k in ("source", "bundle", "verified", "questions"))
    if "verified_row_selection" in verified:
        from judgment.verified_evidence_selection import validate_verified_selection
        if binding.get("verified_selection_original_inputs") != verified["verified_row_selection"]["original_inputs"]:
            raise ValueError("saved verified selection original binding differs")
        validate_verified_selection(bundle, verified, source=source, load=load)
    if finite.semantic.build_bundle(source, max_prompt_bytes=80000, max_evidence_per_work_unit=30,
                                   target_bundle_version=bundle["schema_version"]) != bundle:
        raise ValueError("source and bundle binding differ")
    view, packet = load(root / "view.json"), load(root / "packet-all.json")
    compilation = load(root / "finish/compilation.json")
    if finite.semantic.finalize_v3_view(bundle, verified, compilation) != view:
        raise ValueError("saved view differs from native finalization")
    if finite.semantic.project_evidence_packet(view, bundle, verified, compilation,
            include_claim_support=any("claim_support" in p for p in packet["propositions"]),
            proposition_ids=[p["proposition_id"] for p in view["propositions"]]) != packet:
        raise ValueError("saved packet differs from native projection")
    counts = finite.coverage(bundle, verified, view, packet)
    if counts != load(root / "coverage.json") or counts != result["coverage"]:
        raise ValueError("saved coverage differs")

    # Validate original provider outputs against their existing request bindings.
    # Keep every attempt (including failed/unused ones) in the accounting view.
    responses = {}
    for path in sorted(provider_root.rglob("job/binding.json")):
        policy = load(path)
        for receipt_path in sorted(Path(policy["attempt_root"]).glob("*/execution_receipt.json")):
            receipt = _check_attempt(receipt_path.parent, policy["binding"])
            load(receipt_path)
            if receipt["outcome"] == "PROCESS_COMPLETED":
                response = receipt_path.parent / "response.json"
                responses[str(response.resolve())] = load(response, receipt["response_sha256"])
    for recovery in result.get("provider_recoveries", []):
        path = Path(recovery["attempt_dir"]) / "execution_receipt.json"
        receipt = load(path)
        response = path.parent / "response.json"
        responses[str(response.resolve())] = load(response, receipt["response_sha256"])

    freeze = load(root / "answer/freeze.json")
    frozen = bound_response(freeze)
    load(root / "answer/input.json", freeze["input_sha256"])
    bound_consumer_input("answer")
    assessment_record = load(root / "assessment/result.json")
    assessment = bound_response(assessment_record)
    exact_repairs = assessment.get("schema_version") == "finite_source_assessment_keyed_v3"
    keyed_assessment = assessment.get("schema_version") in {"finite_source_assessment_keyed_v1", "finite_source_assessment_keyed_v3"}
    if Path(result["answer"]).resolve() != Path(freeze["response"]).resolve():
        raise ValueError("result answer differs from frozen answer")
    if Path(result["assessment"]).resolve() != Path(assessment_record["response"]).resolve():
        raise ValueError("result assessment differs from saved assessment")
    if str(Path(result["assessment"]).resolve()) not in responses:
        raise ValueError("assessment lacks a bound provider response")
    reference_errors = finite.answer_reference_errors(frozen, questions["questions"], bundle, verified)
    if reference_errors and not exact_repairs:
        raise ValueError("historical frozen answer contains unknown evidence references")
    assessment = finite.assessment_from_response(assessment, questions["assessment_only"]["checks"])
    if result["material_findings"] != assessment["material_findings"] or result["overall_usefulness"] != assessment["overall_usefulness"]:
        raise ValueError("result omits or changes assessment findings")
    assessment_input = load(root / "assessment/input.json")
    expected_source = {k: v for k, v in source.items() if k != "source_artifacts"}
    ids = {r["source_artifact_id"] for r in source["captured_items"]}
    expected_source["source_artifacts_for_bound_rows"] = [a for a in source["source_artifacts"] if a["artifact_id"] in ids]
    expected_source["unreferenced_locator_count_not_assessed"] = len(source["source_artifacts"]) - len(ids)
    expected = {"current_answer": frozen, "previously_completed_answer_for_comparison": inputs["previous_answer"],
                "answer_commission": {"questions": questions["questions"], "worker_instructions": questions["worker_instructions"]},
                "assessment_checks": questions["assessment_only"], "current_final_view": view,
                "complete_frozen_source": expected_source,
                "complete_frozen_verified_evidence": finite.provider_verified_evidence(verified),
                "scope": questions["coverage"]}
    if "citation_validation" in assessment_input:
        expected["citation_validation"] = {"unknown_references_by_question": reference_errors,
            "status": "invalid_draft" if reference_errors else "valid"}
    if assessment_input != expected:
        raise ValueError("assessment input differs from bound evidence")
    policy = load(provider_root / "assessment/provider/job/binding.json")
    prompt = Path(policy["binding"]["prompt_path"])
    if (hash_file(prompt) != policy["binding"]["prompt_sha256"]
            or prompt.read_text(encoding="utf-8") != finite.render_assessment(expected, keyed_checks=keyed_assessment, exact_repairs=exact_repairs)):
        raise ValueError("assessment prompt differs from bound evidence")

    answer_versions = {"frozen": {"path": freeze["response"], "value": frozen}}
    correction_records = {}
    candidate = composition = None
    corrected = root / "answer-correction/answers-corrected.json"
    if result["answer_corrections"]:
        composition = load(root / "answer-correction/composition.json")
        exact_method = composition.get("method") in {"reviewer_exact_repairs_v1", "reviewer_exact_repairs_v2"}
        if exact_method:
            if composition["assessment"] != assessment_record:
                raise ValueError("exact repairs lack bound source assessment")
            load(root / "answer-correction/input.json", composition["input_sha256"])
        else:
            bound_consumer_input("answer-correction")
        candidate = load(corrected, composition["corrected_sha256"])
        patch = load(composition["patch"], composition["patch_sha256"])
        if not exact_method and str(Path(composition["patch"]).resolve()) not in responses:
            raise ValueError("correction patch lacks a bound provider response")
        original_path = composition.get("original_response", freeze["response"])
        original = load(original_path, composition.get("original_response_sha256"))
        unit_sources = {u["semantic_unit_ref"]: u["evidence_id"] for u in verified["semantic_units"]}
        # Answer references resolve in the citable evidence namespace the runner
        # validated against. A captured row the bundle excluded is a real source
        # but never a citable answer reference; reading it as one would refuse
        # the saved repair scope the runner correctly froze.
        known_refs = {u["evidence_id"] for u in bundle["evidence_units"]} | set(unit_sources)
        if composed_correction(composition, original, patch, questions["questions"],
                               assessment=assessment, known_refs=known_refs, unit_sources=unit_sources) != candidate:
            raise ValueError("corrected answer composition differs")
        finite.check_answer(candidate, questions["questions"], bundle, verified)
        correction_records["composition"] = composition
        answer_versions["before_correction"] = {"path": str(original_path), "value": original}
        answer_versions["correction_candidate"] = {"path": str(corrected), "value": candidate}
    elif str(Path(freeze["response"]).resolve()) not in responses:
        raise ValueError("frozen answer lacks a bound provider response")
    recheck = None
    if result["affected_rechecks"]:
        record = load(root / "assessment-recheck/result.json")
        recheck = bound_response(record)
        if str(Path(record["response"]).resolve()) not in responses:
            raise ValueError("recheck lacks a bound provider response")
        if Path(result["affected_recheck"]).resolve() != Path(record["response"]).resolve():
            raise ValueError("recheck selection differs")
        request = bound_consumer_input("assessment-recheck")
        # Older saved requests omitted this context. New facts must match the
        # complete packet rederived above, not merely a hash-bound model input.
        if ("program_verified_inventory" in request
                and request["program_verified_inventory"] != finite.recheck_inventory_facts(packet)):
            raise ValueError("recheck inventory facts differ from native packet")
        if composition is not None and composition.get("method") == "reviewer_exact_repairs_v2":
            affected = set(composition["affected_question_ids"])
            scoped_questions = [q for q in questions["questions"] if q["id"] in affected]
            edited = {edit["question_id"] for edit in assessment["answer_repairs"]["edits"]}
            # Compare the retained records whole: their stated open-nomination reason is
            # what told the recheck to review that unchanged text, not decoration.
            if (request["affected_questions"] != scoped_questions
                    or request["corrected_affected_answers"] != [a for a in candidate["answers"] if a["question_id"] in affected]
                    or request["nominations_to_verify_against_sources"] != finite.material_answer_findings(assessment["material_findings"])
                    or request["exact_repairs"] != assessment["answer_repairs"]
                    or request["retained_answers"] != finite.retained_answer_records(scoped_questions, edited)):
                raise ValueError("exact repair recheck omits or changes affected answer scope")
        correction_records["recheck_input"] = request
        recheck = finite.assessment_from_response(recheck, request["frozen_relevant_checks"], scoped_checks=True)
        for key, field in (("affected_recheck_material_findings", "material_findings"),
                           ("affected_recheck_check_results", "check_results")):
            if result[key] != recheck[field]:
                raise ValueError("result recheck findings/statuses differ")
    final_path = selected_answer_path(result, freeze["response"], corrected, frozen, candidate, recheck,
                                      assessment=assessment, request=correction_records.get("recheck_input"))
    check_material_status(result, assessment, recheck)
    answer_versions["selected"] = {"path": str(final_path), "value": load(final_path)}
    finite.check_answer(answer_versions["selected"]["value"], questions["questions"], bundle, verified)
    # The raw initial provider answer stays distinct even after pre-freeze repair.
    answer_versions["initial_provider_responses"] = [
        {"path": p, "value": v} for p, v in responses.items()
        if Path(p).is_relative_to(provider_root / "answer/provider")]

    operation = None
    started_at = None
    if operation_dir is not None:
        operation_root = Path(operation_dir).resolve(strict=True)
        op = load(operation_root / "operation.json")
        command = op["command"]
        expected_roots = {provider_root}
        if "run-and-report" in command and command.count("--report-dir") == 1:
            expected_roots.add(Path(command[command.index("--report-dir") + 1]).resolve() / "judgment/provider")
        if (command.count("--output-dir") != 1 or Path(command[command.index("--output-dir") + 1]).resolve() != root
                or {Path(p).resolve() for p in op["provider_roots"]} != expected_roots):
            raise ValueError("operation does not bind this finite run/provider scope")
        for name, record in binding["inputs"].items():
            flag = "--" + name.replace("_", "-")
            if command.count(flag) != 1 or Path(command[command.index(flag) + 1]).resolve() != Path(record["path"]).resolve():
                raise ValueError("operation input binding differs")
        operation = load(operation_root / "closeout.json")
        if operation["operation_id"] != op["operation_id"]:
            raise ValueError("operation closeout identity differs")
        started_at = op["created_at"]
    accounting = collect_provider_roots([str(provider_root)], started_at=started_at)
    saved_receipts = {str(Path(p).resolve()) for p in result["provider_execution_receipts"]}
    observed_receipts = {str(Path(a["receipt_path"]).resolve()) for a in accounting["attempts"]
                         if Path(a["receipt_path"]).is_file()}
    if saved_receipts != observed_receipts:
        raise ValueError("saved provider receipt inventory differs from native scope")
    if operation is not None:
        saved_accounting = load(operation_root / "accounting.json")
        operation_accounting = (accounting if expected_roots == {provider_root} else
            collect_provider_roots(op["provider_roots"], started_at=started_at))
        if saved_accounting != operation_accounting or operation["accounting"] != {k: v for k, v in operation_accounting.items() if k != "attempts"}:
            raise ValueError("saved operation accounting differs from native receipts")
    payload = {"schema_version": "finite_closeout_v1", "semantic_verdict": "requires_human_or_agent_judgment",
               "saved_result": result, "mechanical_validation": {"coverage": counts,
                   "scope": "saved input/response bindings, native view/packet, answer/check shapes and saved selection; not meaning",
                   "original_runtime_missing": runtime_missing},
               "answer_commission": {"questions": questions["questions"], "worker_instructions": questions["worker_instructions"], "coverage": questions["coverage"]},
               "answers": answer_versions, "previous_answer_for_comparison": inputs["previous_answer"],
               "initial_assessment": assessment, "affected_recheck": recheck,
               "correction_records": correction_records, "operation_closeout": operation,
               "native_accounting": accounting,
               "cost_limits": "native receipts only; startup unknowns remain unknown; parent/executor and implementation/setup costs are outside this view; no savings inference",
               "judgment_evidence": evidence_view(source, verified, view, questions),
               "wider_sources": {"bound_inputs": binding["inputs"], "view": str(root / "view.json"), "packet": str(root / "packet-all.json"),
                                 "full_assessment_input": str(root / "assessment/input.json"),
                                 "original_additional_checks_not_recommissioned": questions["assessment_only"].get("additional_checks", [])}}
    from reports.finite_failure_evidence import execution_facts, stage_usage
    payload["execution_facts"] = execution_facts(root, load)
    payload["usage_by_stage"] = stage_usage(accounting, provider_root)
    for path, digest in manifest.items():
        if hash_file(Path(path)) != digest:
            raise ValueError(f"artifact changed during closeout read: {path}")
    payload["read_artifact_hashes"] = manifest
    return payload


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--operation-dir", type=Path, help="Existing run_efficiency operation; omitted means no operation claim")
    parser.add_argument("--failure-record", type=Path, help="Explicit saved failure instead of a completed endpoint")
    parser.add_argument("--snapshot-manifest", type=Path, help="Frozen file manifest with original locators and SHA256; no live-path fallback")
    parser.add_argument("--output", type=Path, help="New optional full consumer JSON outside the saved run; never overwritten")
    parser.add_argument("--max-output-bytes", type=output_budget, default=8192)
    args = parser.parse_args(argv)
    try:
        options = {"failure_record": args.failure_record, "snapshot_manifest": args.snapshot_manifest} if args.failure_record or args.snapshot_manifest else {}
        value = collect(args.run_root, args.operation_dir, **options)
        rendered = {"guidance": RENDERING_GUIDANCE, "evidence": compact_evidence(value)}
        if args.output:
            protected = [args.run_root.resolve(), Path(value["saved_result"]["provider_root"]).resolve()]
            if args.operation_dir:
                protected.append(args.operation_dir.resolve())
            if any(args.output.resolve().is_relative_to(p) for p in protected):
                raise ValueError("consumer output must be outside saved run/provider/operation roots")
            write_verified(rendered, args.output)
            text = bounded_json(rendered, record_path=args.output,
                facts={"semantic_verdict": value["semantic_verdict"], "saved_status": value["saved_result"]["status"],
                       "coverage": value["mechanical_validation"]["coverage"], "native_usage": value["native_accounting"]["usage"],
                       "missing_source_body_ids": value.get("judgment_evidence", {}).get("selection", {}).get("missing_source_body_ids")},
                budget=args.max_output_bytes)
            # Escape at the console boundary without changing the full UTF-8 file.
            print(json.dumps(json.loads(text), ensure_ascii=True, separators=(",", ":")))
        else:
            print(json.dumps(rendered, ensure_ascii=True, separators=(",", ":")))
    except (OSError, ValueError, KeyError, TypeError, IndexError, ValidationError) as exc:
        print(json.dumps({"status": "FINITE_CLOSEOUT_FAILED", "error": str(exc)}, ensure_ascii=True))
        return 1
    return 0
