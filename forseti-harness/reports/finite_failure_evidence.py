"""Assemble saved failure observations without executing or repairing a run."""
from __future__ import annotations

import ast
import json
from pathlib import Path

from harness_utils import hash_file
from harness_efficiency import aggregate_usage
from judgment.review_evidence import material_answer_findings
from reports.efficiency_codex import collect_provider_roots


class SavedEvidence:
    """An explicit frozen manifest relocates original paths without changing bytes."""

    def __init__(self, snapshot_manifest=None):
        self.hashes, self.mapping = {}, {}
        self.snapshot = Path(snapshot_manifest).resolve(strict=True) if snapshot_manifest else None
        if self.snapshot:
            manifest = self.load(self.snapshot)
            base = self.snapshot.parent
            for relative, record in manifest["files"].items():
                copy = (base / relative).resolve(strict=True)
                if not copy.is_relative_to(base) or copy == self.snapshot:
                    raise ValueError("snapshot file outside manifest root")
                self.check(copy, record["sha256"])
                original = Path(record["original"]).resolve()
                # Ancestors give missing-file and directory lookups the same
                # frozen scope. Conflicts cannot silently pick another copy.
                while copy != base and copy.is_relative_to(base):
                    if original in self.mapping and self.mapping[original] != copy:
                        raise ValueError("ambiguous snapshot path mapping")
                    self.mapping[original] = copy
                    original, copy = original.parent, copy.parent
            observed = {str(p.resolve()) for p in base.rglob("*") if p.is_file()}
            if observed != set(self.hashes):
                raise ValueError("snapshot inventory differs from manifest")

    def resolve(self, path):
        path = Path(path).resolve()
        if not self.snapshot or path.is_relative_to(self.snapshot.parent):
            return path
        for ancestor in (path, *path.parents):
            if ancestor in self.mapping:
                return self.mapping[ancestor] / path.relative_to(ancestor)
        raise ValueError(f"source locator absent from frozen snapshot: {path}")

    def check(self, path, expected=None):
        path = Path(path).resolve(strict=True)
        digest = hash_file(path)
        if expected is not None and digest != expected:
            raise ValueError(f"saved binding changed: {path}")
        if str(path) in self.hashes and self.hashes[str(path)] != digest:
            raise ValueError(f"saved artifact changed during read: {path}")
        self.hashes[str(path)] = digest
        return path

    def load(self, path, expected=None):
        return json.loads(self.text(path, expected))

    def text(self, path, expected=None):
        path = self.check(self.resolve(path), expected)
        return path.read_text(encoding="utf-8-sig")


def stage_usage(accounting, providers):
    stages = {}
    for attempt in accounting["attempts"]:
        path = Path(attempt["receipt_path"]).resolve()
        stage = path.relative_to(providers).parts[0] if path.is_relative_to(providers) else "external_recovery"
        stages.setdefault(stage, []).append(attempt)
    result = {}
    for stage, attempts in stages.items():
        usage = aggregate_usage(attempts)
        result[stage] = {"attempts": len(attempts), "usage": usage,
            "additional_observed_response_tokens": sum(a["additional_observed_response_tokens"] or 0 for a in attempts),
            "startup_observation_unknown_attempts": sum(a["additional_observed_response_tokens"] is None for a in attempts)}
    return result


def execution_facts(root, load):
    """Copy dimensions separately; absence does not claim a completed stage."""
    facts = {"stages": {}, "endpoint_artifacts": {}}
    for phase in ("formation", "finish"):
        for name in ("stage", "compilation"):
            path = root / phase / (name + ".json")
            if path.is_file():
                value = load(path)
                facts["stages"][f"{phase}/{name}"] = {
                    **{k: value[k] for k in ("completion_phase", "reconciliation_mode", "input_batch_count",
                       "input_candidate_count", "unmerged_candidate_count") if k in value},
                    **{k + "_count": len(value[k]) for k in ("batches", "candidates", "semantic_nodes",
                        "unmerged_semantic_units") if k in value}}
    for name in ("coverage.json", "view.json", "answer/input.json"):
        path = root / name
        if path.is_file():
            value = load(path)
            facts[name] = value if name == "coverage.json" else {
                **{k: value[k] for k in ("scope", "completion_scope", "completion_strategy", "corpus_profile",
                    "coverage", "source_row_resolution") if k in value},
                **{k + "_count": len(value[k]) for k in ("propositions", "unmerged_semantic_units",
                    "emerging_axis_candidates", "questions") if k in value}}
    for name in ("answer/freeze.json", "answer-correction/exact-repairs.json", "answer-correction/answers-corrected.json",
                 "answer-correction/composition.json", "assessment-recheck/result.json", "result.json"):
        facts["endpoint_artifacts"][name] = (root / name).is_file()
    return facts


def collect_failure(run_root, failure_record, operation_dir=None, snapshot_manifest=None):
    saved = SavedEvidence(snapshot_manifest)
    root = saved.resolve(run_root).resolve(strict=True)
    failure_path = saved.resolve(failure_record).resolve(strict=True)
    if failure_path.parent != root or not failure_path.name.startswith("failure-"):
        raise ValueError("failure record does not belong to the selected run")
    failure = saved.load(failure_path)
    if failure["status"] != "FINITE_EXECUTION_FAILED_OR_UNKNOWN":
        raise ValueError("not a finite failure record")
    binding = saved.load(root / "binding.json")
    if binding.get("replay_from"):
        raise ValueError("historical replay is not a live failure")
    # A historical failure needs a frozen snapshot if the run has since moved on.
    if (root / "result.json").exists():
        raise ValueError("selected failure has a later endpoint; use its frozen snapshot")
    failures = sorted(root.glob("failure-*.json"))
    if failures[-1] != failure_path:
        raise ValueError("selected failure is not latest; use its frozen snapshot")
    inputs = {k: saved.load(v["path"], v["sha256"]) for k, v in binding["inputs"].items()}
    providers = root
    if "provider_root" in binding:
        origin = binding["provider_root"]
        providers = saved.resolve(origin["path"]).resolve(strict=True)
        original = saved.load(providers / "binding.json", origin["binding_sha256"])
        if original["inputs"] != binding["inputs"]:
            raise ValueError("provider-root input binding differs")
    if failure.get("evidence_binding_error"):
        raise ValueError("failed run could not freeze its reporting evidence: " + failure["evidence_binding_error"])
    if "evidence_files" in failure:
        expected = {str(saved.resolve(p)): digest for p, digest in failure["evidence_files"].items()}
        observed = {str(p.resolve()) for directory in {root, providers} for p in directory.rglob("*")
                    if p.is_file() and p.suffix != ".lock" and p.resolve() != failure_path}
        if observed != set(expected):
            raise ValueError("failed interval inventory changed; use its frozen snapshot")
        for path, digest in expected.items():
            saved.check(path, digest)
    for record in failure.get("diagnostics", {}).get("saved_artifacts", {}).values():
        saved.check(saved.resolve(record["path"]), record["sha256"])
    runtime_missing, guards = [], []
    for original, digest in binding["runtime"].items():
        try:
            path = saved.resolve(original)
        except ValueError:
            runtime_missing.append(original)
            continue
        if not path.is_file():
            runtime_missing.append(original)
            continue
        code = saved.text(path, digest)
        if path.suffix != ".py":
            continue
        tree = ast.parse(code)
        # Historical failures predate traceback capture. Recover complete
        # governing functions by literal exception anchors, never known errors.
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and any(
                isinstance(child, ast.Raise) and any(isinstance(part, ast.Constant)
                and isinstance(part.value, str) and len(part.value) >= 12
                and part.value in failure["error"] for part in ast.walk(child)) for child in ast.walk(node)):
                guards.append({"path": original, "sha256": digest, "function": node.name,
                    "from_line": node.lineno, "to_line": node.end_lineno,
                    "text": "\n".join(code.splitlines()[node.lineno - 1:node.end_lineno])})
    records = {}
    for name in ("answer/input.json", "answer/freeze.json", "assessment/input.json", "assessment/result.json",
                 "answer-correction/input.json", "answer-correction/allowance.json", "answer-correction/exact-repairs.json",
                 "answer-correction/composition.json", "answer-correction/answers-corrected.json", "assessment-recheck/result.json"):
        if (root / name).is_file():
            record = saved.load(root / name)
            if name.endswith("input.json"):
                # Reporting a failed execution does not recommission source
                # semantics. Keep scope, exact nominations and affected text;
                # large inventories stay bound at their original locators.
                record = {**{k: record[k] for k in ("scope", "questions", "worker_instructions", "source_row_resolution",
                    "answer_commission", "assessment_checks", "citation_validation", "affected_questions", "reference_errors",
                    "nominations_to_verify_against_sources", "original_affected_answers") if k in record},
                    "supplied_inventory_counts": {k: len(record[k]) for k in ("complete_relevant_source_rows",
                        "verified_units", "current_findings") if k in record}}
            records[name] = record
    # Full assessment/answer response bytes and inputs remain prior observations;
    # reporting must not silently turn them into a fresh semantic assessment.
    for phase in ("answer", "assessment", "answer-correction", "assessment-recheck"):
        result_path = root / phase / "result.json"
        if result_path.is_file():
            record = saved.load(result_path)
            records[phase + "/response"] = saved.load(record["response"], record["response_sha256"])
    assessment = records.get("assessment/response")
    if "answer/freeze.json" in records:
        freeze = records["answer/freeze.json"]
        saved.check(root / "answer/input.json", freeze["input_sha256"])
        records["frozen_answer"] = saved.load(freeze["response"], freeze["response_sha256"])
    repair_scope = None
    if assessment:
        nominated = {ref.removeprefix("current_answer:") for f in material_answer_findings(assessment["material_findings"])
                     for ref in f["artifact_refs"] if ref.startswith("current_answer:")}
        edited = {e["question_id"] for e in assessment.get("answer_repairs", {}).get("edits", [])}
        repair_scope = {"nominated_question_ids": sorted(nominated), "edited_question_ids": sorted(edited),
                        "unedited_nominated_question_ids": sorted(nominated - edited)}
    operation, started_at = None, None
    if operation_dir:
        op_root = saved.resolve(operation_dir).resolve(strict=True)
        op = saved.load(op_root / "operation.json")
        command = op["command"]
        if command.count("--output-dir") != 1 or saved.resolve(command[command.index("--output-dir") + 1]) != root:
            raise ValueError("operation does not bind selected failed run")
        expected_roots = {providers}
        if "run-and-report" in command and command.count("--report-dir") == 1:
            expected_roots.add(saved.resolve(command[command.index("--report-dir") + 1]) / "judgment/provider")
        if {saved.resolve(p) for p in op["provider_roots"]} != expected_roots:
            raise ValueError("operation provider scope differs")
        operation = {name: saved.load(op_root / name) for name in ("closeout.json", "execution.json", "validation.json")}
        if operation["closeout.json"]["operation_id"] != op["operation_id"]:
            raise ValueError("operation closeout identity differs")
        if operation["execution.json"]["exit_code"] in (0, None):
            raise ValueError("operation does not establish failed execution")
        for name in ("command.stdout", "command.stderr"):
            operation[name] = saved.text(op_root / name)
        started_at = op["created_at"]
    accounting = collect_provider_roots([str(providers)], started_at=started_at, resolve_path=saved.resolve)
    # Hash every provider observation used by the accounting reader, not only
    # the receipt; preserve errors and unknown usage rather than certifying it.
    for attempt in accounting["attempts"]:
        for name in ("execution_receipt.json", "events.jsonl", "stderr.log", "response.json"):
            path = Path(attempt["receipt_path"]).parent / name
            if path.is_file():
                saved.check(path)
    facts = execution_facts(root, saved.load)
    facts["repair_scope"] = repair_scope
    value = {"schema_version": "finite_failure_closeout_v1", "semantic_verdict": "failed_execution_not_quality_acceptance",
        "saved_result": {**failure, "provider_root": str(providers)}, "failure_record": str(failure_path),
        "mechanical_validation": {"coverage": facts.get("coverage.json"), "original_runtime_missing": runtime_missing,
            "scope": "saved failure bindings and observations; not endpoint validation or semantic acceptance"},
        "execution_facts": facts, "saved_records": records, "original_failure_guard_functions": guards,
        "guard_evidence_limit": None if guards else "No matching original exception function was available; exact runtime cause may require details.",
        "input_scope": {k: inputs[k] for k in ("questions", "previous_answer")},
        "operation_closeout": operation, "native_accounting": accounting,
        "usage_by_stage": stage_usage(accounting, providers),
        "snapshot_manifest": str(saved.snapshot) if saved.snapshot else None,
        "evidence_gaps": ([] if saved.snapshot or "evidence_files" in failure else [{
            "missing_fact": "immutable inventory at the selected failure", "source_locator": str(failure_path),
            "why_material": "Legacy failure records do not exclude later partial work; supply an explicit frozen snapshot."}]),
        "reporting_scope": "Saved execution diagnosis only. Initial assessment claims remain provisional; no fresh answer/source semantic acceptance."}
    for path, digest in list(saved.hashes.items()):
        saved.check(path, digest)
    value["read_artifact_hashes"] = saved.hashes
    value["read_directory_inventories"] = {str(directory): sorted(str(p.resolve()) for p in directory.rglob("*")
        if p.is_file() and p.suffix != ".lock") for directory in ({saved.snapshot.parent} if saved.snapshot else {root, providers})}
    return value
