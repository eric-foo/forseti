"""Opt-in finite formation/finish execution over already verified evidence.

No extraction, third round, semantic acceptance shortcut, or model supervisor.
The existing provider jobs own transport retry, receipt reuse and unknown states.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import datetime, timezone
import json
import os
import re
from pathlib import Path
import subprocess
import sys

from jsonschema import Draft202012Validator

from harness_utils import hash_file
from provider_jobs import _check_attempt, _lock, completed_recovery_record
from runners import run_semantic_evidence_integration as native
from runners.run_codex_provider_attempt import select_codex_executable
from judgment import semantic_evidence_integration as semantic
from judgment.review_evidence import (render_evidence, material_answer_findings, compose_answer_patch,
                                     answer_source_references, answer_identity, apply_exact_answer_repairs)

HARNESS = Path(__file__).resolve().parents[1]
REPO = HARNESS.parent
CONTEXT = [REPO / path for path in (
    "AGENTS.md", ".agents/workflow-overlay/README.md",
    "docs/prompts/templates/shared/forseti_preflight_defaults_v0.md",
    "forseti/product/spines/judgment/claim_support/forseti_intelligence_claim_support_contract_v0.md",
)]
POLICY = dict(completion_strategy="finite_formation_finish_v1",
              authoring_revision="finite_formation_retention_v1",
              reconciliation_policy_version="semantic_evidence_reconciliation_policy_v2",
              response_version="semantic_evidence_reconciliation_response_v3")
ASSESSMENT_MATERIALITY = (
    "Judge roughly comparable supported usefulness, not matching vocabulary or finding counts. "
    "Report minor imperfections too, using the existing severity/effect judgment: blocker or major means a material "
    "source-supported meaning or usefulness defect; minor means a nonmaterial imperfection. An answer correction "
    "does not require identical wording or maximal detail. Material defects include unsupported claims, changed meaning, "
    "missing important conditions and materially untraceable claims. A more precise possible citation or "
    "other nonmaterial imperfection alone does not require correction or rejection. Apply this standard to "
    "check_results about the answer: a failed or uncertain answer check must reflect a material defect or unresolved "
    "material support, and a nonmaterial imperfection is reported as a minor finding instead. Inventory and upstream "
    "check results keep their observed status. "
)
ASSESSMENT_CHECK_FIELDS = (
    "Fill every named field in commissioned_checks with its source-backed judgment. "
    "Those field names are fixed check identities; do not rename them or add check_id inside those judgments. "
    "Put extra judgments in additional_checks, each with a descriptive check_id distinct from all other checks. "
)


class UnknownAnswerEvidence(ValueError):
    """A schema-valid answer cites evidence absent from its admitted input."""


def read(path):
    return native._load_object(Path(path))


def persist(path, value):
    """No replacement; every resume rederives the expected durable bytes."""
    data = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    persist_bytes(path, data)
    return value


def persist_bytes(path, data):
    path = Path(path)
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError(f"existing finite output differs: {path}")
    else:
        native._write_new(path, data)
    if path.read_bytes() != data:
        raise ValueError(f"finite output readback differs: {path}")


def bound_provider_harness(origin):
    """Keep the original native launch paths when continuing in another checkout."""
    paths = [Path(p) for p in origin["runtime"] if Path(p).name == "run_codex_provider_job.py"]
    if len(paths) != 1:
        raise ValueError("provider root lacks one bound job runner")
    harness = paths[0].resolve().parents[1]
    if harness != HARNESS:
        for path, digest in origin["runtime"].items():
            if hash_file(Path(path)) != digest:
                raise ValueError(f"original provider runtime changed: {path}")
    return harness


def answer_schema(questions):
    ids = [q["id"] for q in questions]
    if not ids or len(set(ids)) != len(ids):
        raise ValueError("questions require unique nonempty identities")
    item = {"type": "object", "additionalProperties": False,
            "required": ["question_id", "answer", "evidence_refs", "limits"],
            "properties": {"question_id": {"type": "string", "enum": ids},
                           "answer": {"type": "string"}, "limits": {"type": "string"},
                           "evidence_refs": {"type": "array", "items": {"type": "string"}}}}
    return {"type": "object", "additionalProperties": False,
            "required": ["schema_version", "answers"], "properties": {
                "schema_version": {"type": "string", "const": "finite_answer_v1"},
                "answers": {"type": "array", "minItems": len(ids), "maxItems": len(ids), "items": item}}}


def answer_generation_schema(questions, source_rows, semantic_units):
    """Constrain generation to the evidence supplied to this answer call.

    Keep the structural schema separate for historical replay and the initial
    answer's explicit unknown-reference validation. Choices establish identity,
    never semantic support for an assertion.
    """
    refs = [r["evidence_id"] for r in source_rows]
    refs.extend(u["semantic_unit_ref"] for u in semantic_units)
    if any(not isinstance(ref, str) or not ref.strip() for ref in refs):
        raise ValueError("answer citation choices require nonempty source identities")
    schema = answer_schema(questions)
    citations = schema["properties"]["answers"]["items"]["properties"]["evidence_refs"]
    if refs:
        citations["items"]["enum"] = sorted(set(refs))
    else:
        # Empty evidence is not an unrestricted vocabulary or a fake sentinel.
        citations["maxItems"] = 0
    return schema


def answer_correction_schema(questions, source_rows, semantic_units):
    """A rejected nomination has a disposition, never replacement answer prose."""
    schema = answer_generation_schema(questions, source_rows, semantic_units)
    schema["properties"]["schema_version"]["const"] = "finite_answer_correction_v1"
    schema["properties"]["answers"]["minItems"] = 0
    schema["required"].append("retained_answers")
    schema["properties"]["retained_answers"] = {
        "type": "array", "maxItems": len(questions), "items": {
            "type": "object", "additionalProperties": False, "required": ["question_id", "reason"],
            "properties": {"question_id": {"type": "string", "enum": [q["id"] for q in questions]},
                           "reason": {"type": "string", "minLength": 1}}}}
    return schema


def answer_correction_patch(original, proposal, questions):
    replaced = [a["question_id"] for a in proposal["answers"]]
    retained = [a["question_id"] for a in proposal["retained_answers"]]
    ids = [q["id"] for q in questions]
    if (len(replaced + retained) != len(set(replaced + retained))
            or set(replaced + retained) != set(ids)):
        raise ValueError("correction must replace or retain each affected question exactly once")
    if replaced != [q for q in ids if q in replaced] or retained != [q for q in ids if q in retained]:
        raise ValueError("correction question identities/order differ")
    replacements = {a["question_id"]: a for a in proposal["answers"]}
    originals = {a["question_id"]: a for a in original["answers"]}
    return {"schema_version": "finite_answer_v1",
            "answers": [replacements.get(q, originals[q]) for q in ids]}


def exact_repairs_schema(answer=None, known_refs=None):
    text = {"type": "string"}
    props = {"question_id": text, "field": {"type": "string", "enum": ["answer", "limits", "evidence_refs"]},
             "before": {"type": "string", "minLength": 1}, "after": text,
             "source_refs": {"type": "array", "minItems": 1, "items": text}}
    edit = {"type": "object", "additionalProperties": False, "required": list(props), "properties": props}
    if answer is not None:
        if known_refs is None:
            raise ValueError("bound repair schema requires supplied reference identities")
        props["question_id"] = {"type": "string", "enum": [a["question_id"] for a in answer["answers"]]}
        props["field"] = {"type": "string", "enum": ["answer", "limits"]}
        choices = [edit]
        for row in answer["answers"]:
            invalid_entries = sorted({r for r in row["evidence_refs"]
                                      if r not in known_refs and row["evidence_refs"].count(r) == 1})
            if invalid_entries and known_refs:
                index_edit = deepcopy(edit)
                index_edit["properties"].update(
                    question_id={"type": "string", "const": row["question_id"]},
                    field={"type": "string", "const": "evidence_refs"},
                    before={"type": "string", "enum": invalid_entries},
                    after={"type": "string", "enum": sorted(known_refs)},
                    source_refs={"type": "array", "minItems": 1, "maxItems": 1,
                                 "items": {"type": "string", "enum": sorted(known_refs)}})
                choices.append(index_edit)
        edit = {"anyOf": choices} if len(choices) > 1 else edit
    return {"type": "object", "additionalProperties": False, "required": ["answer_sha256", "edits"],
            "properties": {"answer_sha256": text, "edits": {"type": "array", "items": edit}}}


def assessment_schema(*, scoped_checks=False, exact_repairs=False, answer=None, known_refs=None):
    text = {"type": "string"}
    refs = {"type": "array", "items": text}
    def obj(props):
        return {"type": "object", "additionalProperties": False,
                "required": list(props), "properties": props}
    check = obj({"check_id": text,
        "status": {"type": "string", "enum": ["pass", "partial", "fail", "uncertain"]},
        "source_refs": refs, "finding_refs": refs, "explanation": text})
    if scoped_checks:
        check["required"].append("scope")
        check["properties"]["scope"] = {"type": "string", "enum": ["answer", "upstream_only", "unknown"]}
    return obj({"schema_version": {"type": "string", "const": (
        "finite_source_assessment_v3" if exact_repairs else "finite_source_assessment_v2" if scoped_checks else "finite_source_assessment_v1")},
        **({"answer_repairs": exact_repairs_schema(answer, known_refs)} if exact_repairs else {}),
        "inventory_coverage": text, "comparison": text, "unassessed_material": text,
        "overall_usefulness": text,
        "check_results": {"type": "array", "items": check},
        "material_findings": {"type": "array", "items": obj({
            "severity": {"type": "string", "enum": ["blocker", "major", "minor"]},
            "introduced_at": {"type": "string", "enum": ["frozen_upstream", "current_consolidation", "current_answer", "historical_answer", "uncertain"]},
            "status": {"type": "string", "enum": ["open", "repaired", "not_a_defect"]},
            "source_refs": refs, "artifact_refs": refs, "defect": text, "effect": text, "bounded_repair": text})}})


def assessment_generation_schema(checks, *, scoped_checks=False, exact_repairs=False, answer=None, known_refs=None):
    """Bind commissioned identities in provider output, before paid generation."""
    ids = [c.get("id") if isinstance(c, dict) else None for c in checks]
    if any(not isinstance(ref, str) or not ref.strip() for ref in ids) or len(ids) != len(set(ids)):
        raise ValueError("assessment checks require unique nonempty identities")
    schema = assessment_schema(scoped_checks=scoped_checks, exact_repairs=exact_repairs, answer=answer, known_refs=known_refs)
    props = schema["properties"]
    if exact_repairs and answer is not None:
        # This call proposes edits; only the later recheck can discharge them.
        # Unbound historical decoding preserves the statuses actually returned.
        props["material_findings"]["items"]["properties"]["status"]["enum"] = ["open", "not_a_defect"]
    additional = props.pop("check_results")["items"]
    check = {**additional,
             "properties": {k: v for k, v in additional["properties"].items() if k != "check_id"},
             "required": [k for k in additional["required"] if k != "check_id"]}
    props["schema_version"]["const"] = props["schema_version"]["const"].replace("_v", "_keyed_v")
    props["commissioned_checks"] = {"type": "object", "additionalProperties": False,
                                    "properties": {ref: check for ref in ids}, "required": ids}
    props["additional_checks"] = {"type": "array", "items": additional}
    schema["required"] = list(props)
    return schema


def assessment_from_response(value, checks, *, scoped_checks=False):
    """Project new provider transport; keep historical assessments unchanged."""
    exact_repairs = value.get("schema_version") in {"finite_source_assessment_keyed_v3", "finite_source_assessment_v3"}
    if value.get("schema_version") in {"finite_source_assessment_keyed_v1", "finite_source_assessment_keyed_v2", "finite_source_assessment_keyed_v3"}:
        Draft202012Validator(assessment_generation_schema(checks, scoped_checks=scoped_checks, exact_repairs=exact_repairs)).validate(value)
        value = dict(value)
        required = value.pop("commissioned_checks")
        additional = value.pop("additional_checks")
        rows = [{"check_id": c["id"], **required[c["id"]]} for c in checks]
        rows.extend(dict(check) for check in additional)
        value["schema_version"] = "finite_source_assessment_v3" if exact_repairs else "finite_source_assessment_v2" if scoped_checks else "finite_source_assessment_v1"
        value["check_results"] = rows
    check_assessment(value, {"assessment_only": {"checks": checks}}, scoped_checks=scoped_checks)
    return value


def answer_reference_errors(answer, questions, bundle, verified):
    Draft202012Validator(answer_schema(questions)).validate(answer)
    if [a["question_id"] for a in answer["answers"]] != [q["id"] for q in questions]:
        raise ValueError("answer question identities/order differ")
    known = {u["evidence_id"] for u in bundle["evidence_units"]}
    known.update(u["semantic_unit_ref"] for u in verified["semantic_units"])
    return {row["question_id"]: sorted(refs) for row in answer["answers"]
            if (refs := answer_source_references(row, known) - known)}


def check_answer(answer, questions, bundle, verified):
    if answer_reference_errors(answer, questions, bundle, verified):
        raise UnknownAnswerEvidence("answer contains unknown evidence references")


def check_assessment(value, questions, *, scoped_checks=False):
    Draft202012Validator(assessment_schema(scoped_checks=scoped_checks,
        exact_repairs=value.get("schema_version") == "finite_source_assessment_v3")).validate(value)
    ids = [x["check_id"] for x in value["check_results"]]
    required = {x["id"] for x in questions["assessment_only"]["checks"]}
    if len(ids) != len(set(ids)) or not required.issubset(ids):
        raise ValueError("source assessment omits or duplicates commissioned checks")


def coverage(bundle, verified, view, packet):
    original = {x["semantic_unit_ref"] for x in verified["semantic_units"]}
    attached = {ref for p in view["propositions"] for refs in p["semantic_relations"].values() for ref in refs}
    residual_rows = [x["semantic_unit_ref"] for x in view["unmerged_semantic_units"]]
    residual = set(residual_rows)
    if (attached | residual != original or attached & residual
            or len(residual) != len(residual_rows)):
        raise ValueError("finding/residual coverage does not partition verified statements")
    selected = packet["selection_coverage"]
    if (selected["truncated"] or selected["selected_proposition_count"] != len(view["propositions"])
            or selected["corpus_unmerged_semantic_unit_count"] != len(residual)):
        raise ValueError("consumer packet coverage differs")
    denominator = bundle["coverage_denominator"]
    expected = {
        "captured_item_count": denominator["captured_item_count"],
        "semantically_assessed_item_count": len(bundle["evidence_units"]),
        "mechanically_excluded_item_count": denominator["accounting_disposition_counts"]["mechanically_excluded"],
        "blocked_item_count": 0,
        "accounted_item_count": denominator["captured_item_count"],
        "complete": True,
    }
    if (any(view["coverage"].get(k) != value for k, value in expected.items())
            or expected["semantically_assessed_item_count"] + expected["mechanically_excluded_item_count"]
            != expected["captured_item_count"]):
        raise ValueError("native view does not account for every source row")
    return dict(source_rows=len(bundle["evidence_units"]), verified_statements=len(original),
                attached_statements=len(attached), residual_statements=len(residual),
                findings=len(view["propositions"]), missing_statements=0, packet_truncated=False)


class FiniteRun:
    policy = POLICY
    def __init__(self, args):
        self.args = args
        self.root = args.output_dir.resolve()
        self.provider_root = args.provider_root.resolve(strict=True) if args.provider_root else self.root
        self.bundle, self.verified, self.source, self.questions = (
            read(getattr(args, name)) for name in ("bundle", "verified", "source", "questions"))
        self.replay = args.replay_from.resolve() if args.replay_from else None
        self.policy = {**POLICY, **({"authoring_revision": "exact_identity_namespaces_v5"} if self.replay else {})}
        self.saved = {}
        self.consumed_repairs = set()
        self.completed_recoveries = {}
        self.consumed_recoveries = set()
        self.grouping_rejections = {}
        for name, supplied in getattr(args, "completed_recovery", []):
            if (self.replay or name in self.completed_recoveries
                    or not re.fullmatch(r"(?:formation|finish)/provider/reconcile-\d{4}-\d{4}", name)):
                raise ValueError("completed recovery must name one distinct live formation/finish job")
            directory = self.provider_root / name
            policy = read(directory / "job/binding.json")
            failed = Path(policy["attempt_root"]) / "job-attempt-001"
            record, _ = completed_recovery_record(failed, Path(supplied).resolve(strict=True), policy["binding"])
            self.completed_recoveries[name] = record
        if self.replay:
            frozen = read(self.replay / "manifest.json")
            for name, filename in (("source", "source.json"), ("bundle", "bundle.json"),
                                   ("verified", "verified.json"), ("questions", "evaluation-questions.json")):
                record = frozen["inputs"][filename]
                if hash_file(Path(record["path"])) != record["sha256"] or hash_file(getattr(args, name)) != record["sha256"]:
                    raise ValueError(f"historical replay input bytes differ: {name}")
            prior = frozen["reference"]["answers-final.json"]
            if hash_file(args.previous_answer) != prior["sha256"]:
                raise ValueError("historical replay comparison answer differs")
            # Original job bindings and receipts are preserved, never restamped.
            for binding_path in self.replay.rglob("job/binding.json"):
                policy = read(binding_path)
                for receipt_path in Path(policy["attempt_root"]).glob("*/execution_receipt.json"):
                    receipt = _check_attempt(receipt_path.parent, policy["binding"])
                    if receipt["outcome"] == "PROCESS_COMPLETED":
                        self.saved.setdefault(policy["binding"]["prompt_sha256"], []).append(
                            (receipt_path.parent / "response.json", policy["binding"]))

    def job(self, name, prompt, schema, *, replay_response=None, validation_schema=None):
        directory = self.provider_root / name
        prompt_path, schema_path = directory / "prompt.md", directory / "response.schema.json"
        persist_bytes(prompt_path, prompt.encode("utf-8"))
        persist(schema_path, schema)
        Draft202012Validator.check_schema(schema)
        if self.replay:
            if replay_response is None:
                matches = self.saved.get(hash_file(prompt_path), [])
                matches = [(p, b) for p, b in matches if read(b["schema_path"]) == schema]
                if len(matches) != 1:
                    raise ValueError(f"replay requires one original prompt/schema-bound response: {name}")
                response = matches[0][0]
            else:
                response = replay_response
                if not any(response == p for records in self.saved.values() for p, _ in records):
                    raise ValueError("replay consumer response lacks verified original provider receipt")
            persist(directory / "replay.json", {"mode": "saved_response_replay_not_fresh_generation",
                "original_response": str(response), "original_response_sha256": hash_file(response),
                "current_prompt_sha256": hash_file(prompt_path),
                "prompt_identical": replay_response is None})
        else:
            selection = self.bind_executable()
            provider_harness = getattr(self, "provider_harness", HARNESS)
            command = [sys.executable, str(provider_harness / "runners/run_codex_provider_job.py"),
                "--job-dir", str(directory / "job"), "--attempt-root", str(directory / "attempts"),
                "--retry-budget-dir", str(self.provider_root / "retry-budget"), "--run-retry-limit", "2",
                "--max-retries", "1", "--prompt-file", str(prompt_path), "--output-schema", str(schema_path),
                "--worktree", str(provider_harness.parent), "--codex-executable", selection["path"],
                "--model", "gpt-5.6-sol", "--reasoning-effort", "high", "--timeout-seconds", "1800"]
            for path in CONTEXT:
                command += ["--preload-context", str(provider_harness.parent / path.relative_to(REPO))]
            recovery = getattr(self, "completed_recoveries", {}).get(name)
            if recovery:
                command += ["--completed-recovery", recovery["attempt_dir"]]
            # Logs for each invocation remain separate, including failed resumes.
            index = len(list(directory.glob("invoke-*.stdout"))) + 1
            out, err = directory / f"invoke-{index:03d}.stdout", directory / f"invoke-{index:03d}.stderr"
            result_path = directory / f"invoke-{index:03d}-result.json"
            command += ["--result-out", str(result_path)]
            with out.open("xb") as stdout, err.open("xb") as stderr:
                process = subprocess.run(command, cwd=provider_harness, stdin=subprocess.DEVNULL,
                    stdout=stdout, stderr=stderr, check=False,
                    env=dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1"),
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            persist(directory / f"invoke-{index:03d}.json", dict(command=command, exit_code=process.returncode,
                stdout=str(out), stderr=str(err)))
            if process.returncode:
                raise ValueError(f"provider job failed or unknown; preserve job/attempt state: {directory}")
            result = read(result_path)
            if result["status"] != "PROCESS_COMPLETED_NOT_VALIDATED":
                raise ValueError("provider did not complete")
            if recovery:
                if result.get("recovery") != recovery:
                    raise ValueError("provider did not consume the bound completed recovery")
                self.consumed_recoveries.add(name)
            response = Path(result["attempt_dir"]) / "response.json"
        Draft202012Validator(schema if validation_schema is None else validation_schema).validate(read(response))
        return response

    def bind_executable(self):
        path = self.provider_root / "codex-selection.json"
        if path.exists():
            selected = read(path)
            binding_path = self.provider_root / "binding.json"
            if binding_path.exists() and read(binding_path).get("codex_selection") != selected:
                raise ValueError("Codex selection differs from the immutable run binding")
            if (self.args.codex_executable is not None
                    and str(self.args.codex_executable.resolve()) != selected["path"]):
                raise ValueError("explicit Codex selection differs from the bound run")
            if hash_file(Path(selected["path"])) != selected["sha256"]:
                raise ValueError("bound Codex executable changed; no automatic rebind")
            return selected
        if (self.provider_root / "binding.json").exists():
            raise ValueError("bound run has no Codex selection; refusing an automatic rebind")
        selected = select_codex_executable(self.args.codex_executable)
        persist(path, selected)
        return read(path)

    def phase(self, name, compilation):
        print(json.dumps({"phase": name, "state": "preparing"}), flush=True)
        stage, prompts = semantic.prepare_reconciliation_stage(self.bundle, compilation, **self.policy,
            packing_strategy="input_order" if name == "formation" else "group_aware_v1")
        if stage["completion_phase"] != name or stage["max_prompt_bytes"] != 80000:
            raise ValueError("finite phase or prompt ceiling differs")
        stage_path = self.root / name / "stage.json"
        persist(stage_path, stage)
        def execute(row):
            return self.job(f"{name}/provider/{row['batch_id']}", row["prompt"] + "\n", row["response_schema"])
        # Validate the first actual installation/context result before expansion.
        responses = [execute(prompts[0])]
        self.validate_or_repair(name, stage, responses[0], 0)
        with ThreadPoolExecutor(max_workers=3) as pool:
            responses += list(pool.map(execute, prompts[1:]))
        accepted = [self.validate_or_repair(name, stage, path, index)
                    for index, path in enumerate(responses)]
        compiled = semantic.validate_reconciliation_stage(self.bundle, stage, [read(p) for p in accepted])
        persist(self.root / name / "compilation.json", compiled)
        # Validate the bytes actually consumed by the next phase.
        if read(self.root / name / "compilation.json") != compiled:
            raise ValueError("durable compilation differs")
        print(json.dumps({"phase": name, "state": "native_validated", "batches": len(prompts)}), flush=True)
        return read(self.root / name / "compilation.json")

    def validate_or_repair(self, phase, stage, response, index):
        try:
            receipt = native.validate_one_reconciliation_response(self.bundle, stage, read(response))
        except semantic.SemanticIntegrationError as exc:
            base = self.root / phase / "repair" / stage["batches"][index]["batch_id"]
            persist(base / "failure.json", {"response": str(response), "sha256": hash_file(response), "error": str(exc)})
            key = f"{phase}:{stage['batches'][index]['batch_id']}"
            supplied = [r for r in self.args.local_repair_successor if r[0] == key]
            if len(supplied) > 1:
                raise ValueError("duplicate local-repair successor binding")
            if supplied:
                _, request_path, patch_path, successor_dir = supplied[0]
                successor_dir = Path(successor_dir).resolve(strict=True)
                # Reuse only a previously accepted native successor, with original
                # response/request/patch and complete durable revalidation.
                if not (successor_dir / "receipt.json").is_file():
                    raise ValueError("supplied local repair has no native acceptance receipt")
                native.submit_reconciliation_local_repair(bundle_path=self.args.bundle,
                    stage_path=self.root / phase / "stage.json", failed_response_path=response,
                    request_path=Path(request_path), patch_path=Path(patch_path), output_dir=successor_dir)
                self.claim_repair(f"{phase}-{index:04d}-local", {
                    "response_sha256": hash_file(response), "request": str(Path(request_path).resolve()),
                    "patch": str(Path(patch_path).resolve()), "patch_sha256": hash_file(Path(patch_path)),
                    "successor": str(successor_dir), "external_provider_usage": "must be included; not inferred from patch"})
                self.consumed_repairs.add(key)
                response = successor_dir / "response.json"
                receipt = native.validate_one_reconciliation_response(self.bundle, stage, read(response))
                persist(self.root / phase / "accepted" / f"{index:04d}.json",
                    {"response": str(response), "response_sha256": hash_file(response), "validation": receipt})
                return response
            if isinstance(exc, semantic.UnsupportedFinishGroupings):
                successor, rejection = semantic.reject_unsupported_finish_groupings(self.bundle, stage, read(response))
                original = response
                response = base / "retained/response.json"
                persist(response, successor)
                receipt = native.validate_one_reconciliation_response(self.bundle, stage, read(response))
                record_path = base / "retained/rejection.json"
                persist(record_path, {**rejection, "original_response": str(original),
                    "original_response_sha256": hash_file(original), "successor": str(response),
                    "successor_sha256": hash_file(response)})
                self.grouping_rejections[key] = str(record_path)
                persist(self.root / phase / "accepted" / f"{index:04d}.json",
                    {"response": str(response), "response_sha256": hash_file(response),
                     "validation": receipt, "grouping_rejection": str(record_path)})
                return response
            request = semantic.prepare_reconciliation_definition_recovery(self.bundle, stage, read(response))
            # Existing native definition recovery admits only exact frozen assignments.
            # Other semantic/graph failures remain diagnosed failures, never generic rerolls.
            self.claim_repair(f"{phase}-{index:04d}", {"response_sha256": hash_file(response)})
            record = {"request": request, "input_sha256": {"bundle": hash_file(self.args.bundle),
                "stage": hash_file(self.root / phase / "stage.json"), "failed_response": hash_file(response)}}
            persist(base / "request.json", record)
            patch = self.job(f"{phase}/repair/{stage['batches'][index]['batch_id']}/provider-definition",
                             request["prompt"] + "\n", request["response_schema"])
            native.submit_reconciliation_definitions(bundle_path=self.args.bundle,
                stage_path=self.root / phase / "stage.json", failed_response_path=response,
                request_path=base / "request.json", patch_path=patch, output_dir=base / "successor")
            response = base / "successor/response.json"
            receipt = native.validate_one_reconciliation_response(self.bundle, stage, read(response))
        persist(self.root / phase / "accepted" / f"{index:04d}.json",
                {"response": str(response), "response_sha256": hash_file(response), "validation": receipt})
        return response

    def claim_repair(self, name, record):
        claim = self.provider_root / "repair-budget" / f"{name}.json"
        with _lock(claim.parent / "budget.lock", wait_seconds=5):
            if not claim.exists() and len(list(claim.parent.glob("*.json"))) >= 4:
                raise ValueError("finite consolidation repair budget exhausted")
            persist(claim, record)

    def consumers(self, compilation):
        print(json.dumps({"phase": "consumer_finalization", "state": "running"}), flush=True)
        view = semantic.finalize_v3_view(self.bundle, self.verified, compilation)
        persist(self.root / "view.json", view)
        view = read(self.root / "view.json")
        packet = semantic.project_evidence_packet(read(self.root / "view.json"), self.bundle,
            self.verified, compilation, include_claim_support=not self.replay, proposition_ids=[p["proposition_id"] for p in view["propositions"]])
        persist(self.root / "packet-all.json", packet)
        counts = coverage(self.bundle, self.verified, read(self.root / "view.json"), read(self.root / "packet-all.json"))
        persist(self.root / "coverage.json", counts)
        axis_rows = []
        for axis in self.source["axes"]:
            selection = semantic.project_evidence_packet(view, self.bundle, self.verified, compilation, include_claim_support=not self.replay, axis_ids=[axis["axis_id"]])
            path = self.root / "packets-axis" / f"{axis['axis_id']}.json"
            persist(path, selection)
            axis_rows.append({"axis_id": axis["axis_id"], "label": axis["label"], "packet_sha256": hash_file(path),
                "selected_proposition_ids": [p["proposition_id"] for p in selection["propositions"]],
                "unmerged_axis_semantic_unit_refs": [u["semantic_unit_ref"] for u in selection["unmerged_axis_candidates"]],
                "unresolved_axis_evidence_ids": [u["evidence_id"] for u in selection["unresolved_axis_candidates"]]})
        # Consumer replay goes through the same validators and serializer again.
        replay_view = semantic.finalize_v3_view(self.bundle, self.verified, read(self.root / "finish/compilation.json"))
        replay_packet = semantic.project_evidence_packet(replay_view, self.bundle, self.verified, compilation,
            include_claim_support=not self.replay, proposition_ids=[p["proposition_id"] for p in replay_view["propositions"]])
        persist(self.root / "view.json", replay_view)
        persist(self.root / "packet-all.json", replay_packet)
        return view, packet, axis_rows, counts

    def answer_and_assess(self, view, packet, axes):
        print(json.dumps({"phase": "answer", "state": "preparing"}), flush=True)
        units = {u["semantic_unit_ref"]: u for u in self.verified["semantic_units"]}
        attached = {r for p in view["propositions"] for refs in p["semantic_relations"].values() for r in refs}
        represented_ids = {units[r]["evidence_id"] for r in attached}
        evidence = {u["evidence_id"]: u for u in self.bundle["evidence_units"]}
        unit_ids = {u["evidence_id"] for u in units.values()}
        request = {"schema_version": "finite_answer_input_v1", "worker_instructions": self.questions["worker_instructions"],
            "questions": self.questions["questions"], "current_native_packet": packet, "native_axis_selections": axes,
            "retrievable_residual_statements": [{"semantic_unit_ref": u["semantic_unit_ref"], "reason": u["reason"],
                "verified_statement": units[u["semantic_unit_ref"]]} for u in view["unmerged_semantic_units"]],
            "additional_source_rows_for_retrieval": [evidence[e] for e in sorted(set(evidence) - represented_ids)],
            "nonclaim_source_dispositions": [d for d in self.verified["evidence_dispositions"] if d["evidence_id"] not in unit_ids],
            "source_row_resolution": {"native_packet_source_rows": len(represented_ids),
                "additional_retrievable_source_rows": len(set(evidence) - represented_ids), "total_unique_source_rows": len(evidence)},
            "scope": self.questions["coverage"]}
        persist(self.root / "answer/input.json", request)
        original_answer = None
        if self.replay:
            if read(self.replay / "answer-v3/input.json") != request:
                raise ValueError("saved answer evidence/input differs from replay consumer")
            self.check_saved_input("answer-v3", "current_answer_input_json")
            original_answer = Path(read(self.replay / "answer-v3/freeze.json")["response"])
        structural_schema = answer_schema(self.questions["questions"])
        generation_schema = structural_schema if self.replay else answer_generation_schema(
            self.questions["questions"], self.bundle["evidence_units"], self.verified["semantic_units"])
        # Citation-invalid drafts reach the same source reviewer; malformed
        # structures and question identities still stop before that call.
        answer_path = self.job("answer/provider", render_answer(request), generation_schema,
                               replay_response=original_answer, validation_schema=structural_schema)
        answer = read(answer_path)
        reference_errors = answer_reference_errors(answer, self.questions["questions"], self.bundle, self.verified)
        if self.replay and reference_errors:
            raise UnknownAnswerEvidence("historical frozen answer contains unknown evidence references")
        persist(self.root / "answer/freeze.json", {"response": str(answer_path), "response_sha256": hash_file(answer_path),
            "input_sha256": hash_file(self.root / "answer/input.json"), "historical_answer_access_before_freeze": False})
        # Historical answer and hidden checks first enter a provider request AFTER freeze.
        reachable = {r["source_artifact_id"] for r in self.source["captured_items"]}
        assessment_source = {k: v for k, v in self.source.items() if k != "source_artifacts"}
        assessment_source["source_artifacts_for_bound_rows"] = [a for a in self.source["source_artifacts"] if a["artifact_id"] in reachable]
        if {a["artifact_id"] for a in assessment_source["source_artifacts_for_bound_rows"]} != reachable:
            raise ValueError("source assessment lacks bound source-artifact locators")
        assessment_source["unreferenced_locator_count_not_assessed"] = len(self.source["source_artifacts"]) - len(reachable)
        assessment_input = {"current_answer": answer, "previously_completed_answer_for_comparison": read(self.args.previous_answer),
            "answer_commission": {"questions": self.questions["questions"],
                                  "worker_instructions": self.questions["worker_instructions"]},
            "assessment_checks": self.questions["assessment_only"], "current_final_view": view,
            "complete_frozen_source": assessment_source, "complete_frozen_verified_evidence": self.verified,
            "scope": self.questions["coverage"]}
        if not self.replay:
            assessment_input["citation_validation"] = {"unknown_references_by_question": reference_errors,
                "status": "invalid_draft" if reference_errors else "valid"}
        persist(self.root / "assessment/input.json", assessment_input)
        original_assessment = None
        if self.replay:
            self.check_saved_input("assessment", "source_assessment_input_json")
            old = read(self.replay / "assessment/input.json")
            for key, expected in (("current_answer", answer), ("previously_completed_answer_for_comparison", read(self.args.previous_answer)),
                    ("assessment_checks", self.questions["assessment_only"]),
                    ("current_final_view_all_findings_relations_conditions_and_residuals", view),
                    ("complete_frozen_verified_evidence_and_dispositions", self.verified)):
                if old[key] != expected:
                    raise ValueError(f"saved source assessment binding differs: {key}")
            original_assessment = Path(read(self.replay / "assessment/completion.json")["response"])
        checks = self.questions["assessment_only"]["checks"]
        known_refs = {r["evidence_id"] for r in self.bundle["evidence_units"]} | set(units)
        schema = assessment_schema() if self.replay else assessment_generation_schema(
            checks, exact_repairs=True, answer=answer, known_refs=known_refs)
        assessment_path = self.job("assessment/provider", render_assessment(assessment_input, keyed_checks=not self.replay, exact_repairs=not self.replay), schema,
                                    replay_response=original_assessment)
        assessment = assessment_from_response(read(assessment_path), checks)
        persist(self.root / "assessment/result.json", {"response": str(assessment_path), "response_sha256": hash_file(assessment_path)})
        correction = self.correct_and_recheck(answer, assessment, view)
        check_answer(read(correction["final_answer"]), self.questions["questions"], self.bundle, self.verified)
        return {"answer": str(answer_path), "assessment": str(assessment_path), **correction,
                "material_findings": assessment["material_findings"], "overall_usefulness": assessment["overall_usefulness"]}

    def correct_and_recheck(self, answer, assessment, view):
        nominations = material_answer_findings(assessment["material_findings"])
        reference_errors = answer_reference_errors(answer, self.questions["questions"], self.bundle, self.verified)
        if not nominations and not reference_errors:
            if assessment.get("answer_repairs", {}).get("edits"):
                raise ValueError("exact repairs have no material answer nomination")
            remaining = material_answer_findings(assessment["material_findings"], for_correction=False)
            return {"final_answer": read(self.root / "answer/freeze.json")["response"],
                    "answer_corrections": 0, "affected_rechecks": 0,
                    "answer_material_status": "material_defects_remain" if remaining else "no_open_material_answer_defects_reported",
                    "remaining_material_answer_findings": remaining}
        affected = {r.removeprefix("current_answer:") for f in nominations for r in f["artifact_refs"]
                    if r.startswith("current_answer:")}
        affected.update(reference_errors)
        questions = [q for q in self.questions["questions"] if q["id"] in affected]
        if {q["id"] for q in questions} != affected:
            raise ValueError("assessment correction scope contains unknown question identity")
        persist(self.provider_root / "answer-correction/allowance.json", {
            "kind": "post_assessment", "original_answer": answer, "affected_question_ids": sorted(affected)})
        if not self.replay:
            original_path = Path(read(self.root / "answer/freeze.json")["response"])
            if read(original_path) != answer:
                raise ValueError("frozen original answer differs before correction")
        refs = {r for f in nominations for r in f["source_refs"]}
        known_units = {u["semantic_unit_ref"]: u["evidence_id"] for u in self.verified["semantic_units"]}
        known_ids = {r["evidence_id"] for r in self.source["captured_items"]}
        citable_refs = {r["evidence_id"] for r in self.bundle["evidence_units"]} | set(known_units)
        refs.update(r for a in answer["answers"] if a["question_id"] in affected
                    for r in answer_source_references(a, known_ids | set(known_units)) if r in known_ids or r in known_units)
        if not self.replay:
            refs.update(r for edit in assessment.get("answer_repairs", {}).get("edits", []) for r in edit["source_refs"])
        if refs - known_ids - set(known_units):
            raise ValueError("correction nomination/citation contains unknown source reference")
        ids = {known_units.get(r, r) for r in refs}
        # Include all support/opposition behind related findings, not just the
        # assessor's cited side. Hidden checks enter only the later recheck.
        related = [p for p in view["propositions"]
                   if ids & {known_units[r] for rs in p["semantic_relations"].values() for r in rs}]
        ids.update(known_units[r] for p in related for rs in p["semantic_relations"].values() for r in rs)
        if ids - known_ids:
            raise ValueError("correction lacks required source bodies")
        request = {"questions": questions, "worker_instructions": self.questions["worker_instructions"],
            "original_affected_answers": [a for a in answer["answers"] if a["question_id"] in affected],
            "nominations_to_verify_against_sources": nominations,
            "complete_relevant_source_rows": [r for r in self.source["captured_items"] if r["evidence_id"] in ids],
            "verified_units": [u for u in self.verified["semantic_units"] if u["evidence_id"] in ids],
            "current_findings": related}
        if not self.replay:
            request["reference_errors"] = reference_errors
            request["answer_commission"] = {"questions": self.questions["questions"],
                "worker_instructions": request.pop("worker_instructions")}
            request["affected_questions"] = request.pop("questions")
        persist(self.root / "answer-correction/input.json", request)
        if self.replay:
            self.check_saved_input("answer-correction", "answer_correction_input_json")
            old = read(self.replay / "answer-correction/input.json")
            if (old["assessor_nominations_to_verify_against_sources"] != nominations
                    or old["original_answer_one"] not in request["original_affected_answers"]):
                raise ValueError("saved correction nomination or original answer differs")
            patch_path = self.replay / "answer-correction/provider/attempts/job-attempt-001/response.json"
            if not any(patch_path == p for records in self.saved.values() for p, _ in records):
                raise ValueError("saved correction lacks original provider receipt")
            patch = {"schema_version": "finite_answer_v1", "answers": [read(patch_path)]}
        else:
            if assessment.get("schema_version") != "finite_source_assessment_v3":
                raise ValueError("live correction requires reviewer-authored exact repairs")
            proposal = assessment["answer_repairs"]
            Draft202012Validator(exact_repairs_schema()).validate(proposal)
            # Repair references become answer citations, so they resolve in the
            # citable namespace the answer itself is validated against, not the
            # wider assessed source rows a nomination may cite.
            corrected = apply_exact_answer_repairs(answer, proposal, nominations, citable_refs,
                                                   reference_errors, unit_sources=known_units, allow_retained=True)
            patch = {"schema_version": "finite_answer_v1",
                     "answers": [a for a in corrected["answers"] if a["question_id"] in affected]}
            patch_path = self.root / "answer-correction/exact-repairs.json"
            persist(patch_path, proposal)
        check_answer(patch, questions, self.bundle, self.verified)
        corrected = compose_answer_patch(answer, patch, affected)
        check_answer(corrected, self.questions["questions"], self.bundle, self.verified)
        persist(self.root / "answer-correction/answers-corrected.json", corrected)
        persist(self.root / "answer-correction/composition.json", {
            **({"method": "reviewer_exact_repairs_v2", "assessment": read(self.root / "assessment/result.json"),
                "input_sha256": hash_file(self.root / "answer-correction/input.json")} if not self.replay else {}),
            "patch": str(patch_path), "patch_sha256": hash_file(patch_path),
            "affected_question_ids": sorted(affected), "unaffected_answers_unchanged": True,
            "corrected_sha256": hash_file(self.root / "answer-correction/answers-corrected.json")})
        corrected_refs = {r for a in patch["answers"] for r in answer_source_references(a, known_ids | set(known_units))}
        ids.update(known_units.get(r, r) for r in corrected_refs)
        checks = [c for c in self.questions["assessment_only"]["checks"] if ids & set(c["source_rows"])]
        ids.update(r for c in checks for r in c["source_rows"])
        recheck_findings = [p for p in view["propositions"]
            if ids & {known_units[r] for rs in p["semantic_relations"].values() for r in rs}]
        ids.update(known_units[r] for p in recheck_findings for rs in p["semantic_relations"].values() for r in rs)
        if ids - known_ids:
            raise ValueError("affected recheck lacks commissioned check source bodies")
        recheck_request = {**request, "corrected_affected_answers": patch["answers"], "frozen_relevant_checks": checks,
            "current_findings": recheck_findings,
            "complete_relevant_source_rows": [r for r in self.source["captured_items"] if r["evidence_id"] in ids],
            "verified_units": [u for u in self.verified["semantic_units"] if u["evidence_id"] in ids]}
        if not self.replay:
            recheck_request["exact_repairs"] = proposal
            edited = {edit["question_id"] for edit in proposal["edits"]}
            recheck_request["retained_answers"] = [
                {"question_id": q["id"], "reason": "No exact edit supplied; the original text remains under its open nomination for this recheck."}
                for q in questions if q["id"] not in edited]
        persist(self.root / "assessment-recheck/input.json", recheck_request)
        if self.replay:
            self.check_saved_input("assessment-recheck", "affected_recheck_input_json")
            old = read(self.replay / "assessment-recheck/input.json")
            if old["corrected_answer_one"] not in patch["answers"]:
                raise ValueError("saved affected recheck corrected answer differs")
            recheck_path = self.replay / "assessment-recheck/provider/attempts/job-attempt-001/response.json"
            if not any(recheck_path == p for records in self.saved.values() for p, _ in records):
                raise ValueError("saved recheck lacks original provider receipt")
            Draft202012Validator(read(self.replay / "assessment-recheck/response.schema.json")).validate(read(recheck_path))
        else:
            prompt = ("Output mode: chat-only. Edit permission: read-only. Perform one source-backed affected-scope recheck "
                "of the corrected answers and original nominations. Check every material changed assertion and citation. "
                "answer_commission describes the original full assignment; review only affected_questions. Other answers "
                "are preserved unchanged by the runner and deliberately absent here, not missing from the full answer. "
                "Full-assignment counts and length do not apply to this subset. Verify retained_answers reasons against "
                "the affected questions and original answer requirements; retained answer text "
                "is copied from the original. A rejected nomination is not answer prose. Mark disproven nominations not_a_defect; "
                "report any unresolved material defect in the candidate answers as open. "
                + ASSESSMENT_MATERIALITY + ASSESSMENT_CHECK_FIELDS +
                "Run the supplied relevant frozen checks. Identify new defects from correction. Preserve upstream and "
                "consolidation inventory limits separately in material_findings; correcting prose does not repair the inventory. "
                "For every check, including added checks, set scope to answer if it concerns the corrected answer "
                "or an upstream defect still affects that answer; use upstream_only only for inventory defects with no "
                "remaining effect on the corrected answer. A check covering both is answer; unresolved scope is unknown. "
                "Explain that scope against the supplied sources and candidate. Scope describes remaining effect, not defect origin. "
                "Keep internal review and inventory diagnostics out of answer and limits; preserve source-supported limitations "
                "that matter to the user's question. "
                "Use the supplied assessment schema; comparison means corrected versus original affected answers.\n\n"
                + render_evidence(recheck_request))
            recheck_path = self.job("assessment-recheck/provider", prompt,
                                   assessment_generation_schema(checks, scoped_checks=True))
            recheck = assessment_from_response(read(recheck_path), checks, scoped_checks=True)
        persist(self.root / "assessment-recheck/result.json", {"response": str(recheck_path),
            "response_sha256": hash_file(recheck_path), "saved_replay": bool(self.replay)})
        result = {"final_answer": str(self.root / "answer-correction/answers-corrected.json"),
                  "affected_recheck": str(recheck_path), "answer_corrections": 1, "affected_rechecks": 1}
        if not self.replay:
            # Preserve the candidate even when it cannot replace the frozen original.
            remaining = material_answer_findings(recheck["material_findings"], for_correction=False)
            failed_checks = [c for c in recheck["check_results"]
                             if c["status"] in {"fail", "uncertain"} and c["scope"] != "upstream_only"]
            accepted = not remaining and not failed_checks
            unchanged = corrected == answer
            result["answer_correction_candidate"] = result["final_answer"]
            result["answer_correction_status"] = (
                "rejected" if not accepted else "original_retained" if unchanged else "accepted")
            result["answer_correction_failed_checks"] = failed_checks
            if not accepted or unchanged:
                result["final_answer"] = str(original_path)
            result["affected_recheck_material_findings"] = recheck["material_findings"]
            result["affected_recheck_check_results"] = recheck["check_results"]
            # A rejected candidate's findings stay above; retaining the original
            # does not discharge its original nominations or declare it successful.
            original_remaining = material_answer_findings(assessment["material_findings"], for_correction=False)
            result["remaining_material_answer_findings"] = (
                [f for f in original_remaining if f not in nominations] if accepted else original_remaining)
            result["answer_material_status"] = (
                "correction_rejected_original_requires_adjudication" if not accepted
                else "material_defects_remain" if result["remaining_material_answer_findings"]
                else "no_open_material_answer_defects_reported")
        return result

    def check_saved_input(self, directory, tag):
        """Tie saved consumer input back to the original hash-bound provider prompt."""
        path = self.replay / directory / "prompt.md"
        binding = read(self.replay / directory / "provider/job/binding.json")["binding"]
        if hash_file(path) != binding["prompt_sha256"]:
            raise ValueError("saved consumer prompt bytes changed")
        text = path.read_text(encoding="utf-8")
        opening, closing = f"<{tag}>", f"</{tag}>"
        if text.count(opening) != 1 or text.count(closing) != 1:
            raise ValueError("saved consumer input boundary differs")
        payload = json.loads(text.split(opening, 1)[1].split(closing, 1)[0], object_pairs_hook=native.unique_json_object)
        if payload != read(self.replay / directory / "input.json"):
            raise ValueError("saved consumer input differs from original provider prompt")

    def run(self):
        inputs = {name: {"path": str(getattr(self.args, name).resolve()), "sha256": hash_file(getattr(self.args, name))}
                  for name in ("bundle", "verified", "source", "questions", "previous_answer")}
        runtime = [Path(__file__), HARNESS / "judgment/semantic_evidence_integration.py",
            HARNESS / "judgment/review_evidence.py",
            HARNESS / "reports/finite_closeout.py",
            HARNESS / "runners/run_semantic_evidence_integration.py", HARNESS / "provider_jobs.py",
            HARNESS / "provider_execution.py",
            HARNESS / "runners/run_codex_provider_job.py", HARNESS / "runners/run_codex_provider_attempt.py", *CONTEXT]
        binding = {"inputs": inputs, "policy": self.policy, "replay_from": str(self.replay) if self.replay else None,
            "runtime": {str(p.resolve()): hash_file(p) for p in runtime}}
        if getattr(self, "completed_recoveries", {}):
            binding["completed_recoveries"] = self.completed_recoveries
        with _lock(self.provider_root / "run.lock"):
            if self.args.provider_root:
                if self.replay:
                    raise ValueError("provider-root reuse and historical replay are separate modes")
                origin_path = self.provider_root / "binding.json"
                origin = read(origin_path)
                if "provider_root" in origin:
                    # A successor root holds no provider jobs or budgets; chaining would reset them.
                    raise ValueError("provider root must be the original live run root, not a successor")
                if origin["inputs"] != inputs or origin["policy"] != self.policy or origin.get("replay_from") is not None:
                    raise ValueError("provider-root inputs or finite policy differ")
                self.provider_harness = bound_provider_harness(origin)
                binding["provider_root"] = {"path": str(self.provider_root), "binding_sha256": hash_file(origin_path)}
            if not self.replay:
                binding["codex_selection"] = self.bind_executable()
            persist(self.root / "binding.json", binding)
            rederived = semantic.build_bundle(self.source, max_prompt_bytes=80000,
                max_evidence_per_work_unit=30, target_bundle_version=self.bundle["schema_version"])
            if rederived != self.bundle:
                raise ValueError("source and bundle bytes/packing differ under the finite input boundary")
            # Packet compatibility depends only on frozen source metadata;
            # reject it before paying for formation and finish.
            for row in self.bundle["evidence_units"]:
                semantic._packet_v2_engagement_observation(row)
            formation = self.phase("formation", self.verified)
            finish = self.phase("finish", formation)
            # Repairs are consumed only by the two phases; reject a stale binding before paid consumers.
            if {r[0] for r in self.args.local_repair_successor} != self.consumed_repairs:
                raise ValueError("unused local-repair successor binding")
            if set(getattr(self, "completed_recoveries", {})) != getattr(self, "consumed_recoveries", set()):
                raise ValueError("unused completed-recovery binding")
            view, packet, axes, counts = self.consumers(finish)
            result = self.answer_and_assess(view, packet, axes)
            # Include external completed repeats once, alongside every preserved
            # original attempt. A timeout's missing usage remains unknown.
            receipts = {str(p.resolve()) for p in self.provider_root.rglob("attempts/*/execution_receipt.json")}
            recoveries = [read(p) for p in sorted(self.provider_root.rglob("job/recovery-002.json"))]
            receipts.update(str(Path(r["attempt_dir"]) / "execution_receipt.json") for r in recoveries)
            rejections = list(getattr(self, "grouping_rejections", {}).values())
            recovered = bool(recoveries or rejections) or any(read(Path(p))["outcome"] != "PROCESS_COMPLETED" for p in receipts)
            result.update(status="SAVED_REPLAY_COMPLETE" if self.replay else (
                              "FINITE_EXECUTION_RECOVERED_QUALITY_REQUIRES_ADJUDICATION" if recovered
                              else "FINITE_EXECUTION_COMPLETE_QUALITY_REQUIRES_ADJUDICATION"),
                          coverage=counts, output_dir=str(self.root), provider_root=str(self.provider_root),
                          provider_recoveries=recoveries, provider_execution_receipts=sorted(receipts),
                          grouping_rejections=rejections,
                          provider_usage="listed original and recovery receipts; unknown remains unknown; completed-turn usage may omit startup warmup and hidden requests")
            persist(self.root / "result.json", result)
            return result


def render_answer(request):
    return ("Output mode: chat-only. Edit permission: read-only. The input below is run-authoritative. "
            "Answer only the frozen questions from current finalized evidence and retrievable residuals. "
            "Inspect residuals where they materially qualify an answer. The packet uses positional catalogue rows "
            "under named columns/defaults; interpret those exactly. Residuals are retrievable evidence, not findings. "
            "Per-finding evidence_item_counts count preserved source items, not people; claim_support.independent_origin_count "
            "is the already-credited origin count, not proven unique persons. Missing or uncredited identity remains uncertain. "
            "Cite source evidence IDs or semantic unit refs. Preserve conditions, opposition, uncertainty and intent versus action. "
            "Return the supplied JSON schema in question order. Follow worker_instructions for length and scope.\n\n"
            + render_evidence(request))


def render_assessment(request, *, keyed_checks=False, exact_repairs=False):
    rows = request["complete_frozen_source"]["captured_items"]
    missing = [r["evidence_id"] for r in rows if not r.get("text")]
    body_coverage = (f"Input availability: {len(rows) - len(missing)} of {len(rows)} captured rows have source-native "
        f"bodies in complete_frozen_source.captured_items.text; missing body IDs: {json.dumps(missing)}. "
        "Resolve transport references to read these bodies. Original artifact locators are not substitutes for "
        "the supplied bodies, and unreferenced locators are a separate scope. Availability does not certify inspection; "
        "name exact row IDs and affected checks if any included body cannot be inspected. ")
    return ("Output mode: chat-only. Edit permission: read-only. The input below is run-authoritative. "
            "Perform the commissioned source-backed assessment of every current finding meaning, condition, assignment "
            "and residual disposition, plus the frozen checks and additional inventory checks. Prior answers are comparison, "
            "not truth. Judge answer coverage against answer_commission.questions and worker_instructions. The broader "
            "complete_frozen_source.question defines research inventory scope; it does not expand the commissioned answers. "
            "Distinguish frozen upstream, current consolidation, current answer and historical answer defects. "
            + ASSESSMENT_MATERIALITY + (ASSESSMENT_CHECK_FIELDS if keyed_checks else "") + "Cite exact source "
            "and artifact refs. Use current_answer:QUESTION_ID for affected answer references. State unassessed material honestly. "
            + (("Supply answer_repairs bound to answer_sha256=" + answer_identity(request["current_answer"]) + ". "
                "For every open major/blocker nomination referencing current_answer:QUESTION_ID, author the exact supported "
                "text edits now. Findings describe the unchanged frozen answer: keep defects open even when supplying "
                "their proposed fixes. Do not include edits for minor or not_a_defect findings. "
                + (("citation_validation lists observed invalid draft references; repair those too even when "
                "the typo is nonmaterial, without promoting minor findings. They are not source evidence. For an exact "
                "citation repair, before must be the observed invalid reference, after a supported supplied reference, "
                "and source_refs exactly [after]. For invalid evidence_refs entries, field=evidence_refs replaces that "
                "one exact entry; no list rewriting, deletion or guessed substitutions. Unrepairable references remain "
                "a visible failure. Other edits select answer or limits, a nonempty before substring occurring exactly once in "
) if "citation_validation" in request else
                   "Each edit selects answer or limits, a nonempty before substring occurring exactly once in ") +
                "that frozen field and the exact after replacement. Each non-citation edit's source_refs must include "
                "a source from that question's open major/blocker nominations; any other refs must already be cited "
                "in that frozen answer and support retained context. "
                "For additions replace a unique existing anchor with itself plus the addition. Use disjoint anchors; "
                "preserve all unrelated prose verbatim, direction, scope, attribution and uncertainty. No rewrite call follows: "
                "these exact edits will be applied mechanically, then separately source-rechecked. Do not put internal "
                "review/inventory diagnostics into user-facing text. Cite source IDs or semantic unit refs, never finding IDs. "
                + ("If neither material answer repairs nor citation-validation repairs are needed, return an empty edits list. Applicability does not "
                   if "citation_validation" in request else
                   "If no material answer repair is warranted, return an empty edits list. A repair's applicability does not ") +
                "prove meaning; a source-supported repair must satisfy the original answer commission. ") if exact_repairs else "")
            + "Return the supplied JSON schema.\n\n"
            + body_coverage + render_evidence(request))


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "judge-closeout":
        from reports.finite_closeout_judgment import main as judge_closeout
        return judge_closeout(argv[1:])
    if argv and argv[0] == "closeout":
        from reports.finite_closeout import main as closeout
        return closeout(argv[1:])
    parser = argparse.ArgumentParser(description=__doc__,
        epilog="Read a saved endpoint without provider calls: closeout --run-root RUN_ROOT [--operation-dir OPERATION] [--output NEW_JSON]")
    for name in ("bundle", "verified", "source", "questions", "previous-answer", "output-dir"):
        parser.add_argument("--" + name, type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--codex-executable", type=Path, help="Explicit native override; default selects the verified native ancestor hosting this Windows Desktop task")
    mode.add_argument("--replay-from", type=Path)
    parser.add_argument("--provider-root", type=Path,
        help="Explicit prior live run root: reuse native jobs, shared lock and all budgets in place")
    parser.add_argument("--local-repair-successor", nargs=4, action="append", default=[],
        metavar=("PHASE:BATCH", "REQUEST", "PATCH", "SUCCESSOR_DIR"),
        help="Resume with an explicitly nominated, already accepted native local repair")
    parser.add_argument("--completed-recovery", nargs=2, action="append", default=[],
        metavar=("PHASE/provider/BATCH", "ATTEMPT_DIR"),
        help="Adopt a completed identical repeat of an existing stopped timeout; preserves failure and consumes one shared retry")
    args = parser.parse_args(argv)
    try:
        result = FiniteRun(args).run()
    except Exception as exc:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        failure = args.output_dir / ("failure-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f") + ".json")
        record = {"status": "FINITE_EXECUTION_FAILED_OR_UNKNOWN", "error_type": type(exc).__name__, "error": str(exc)}
        try:
            from reports.finite_closeout import failure_summary
            record["diagnostics"] = failure_summary(args.output_dir, args.provider_root or args.output_dir)
        except Exception as diagnostic_error:
            record["diagnostic_error"] = str(diagnostic_error)
        persist(failure, record)
        print(json.dumps({"status": "FINITE_EXECUTION_FAILED_OR_UNKNOWN", "failure": str(failure), "error": str(exc)}))
        return 1
    print(json.dumps({"status": result["status"], "coverage": result["coverage"], "result": str(args.output_dir / "result.json")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
