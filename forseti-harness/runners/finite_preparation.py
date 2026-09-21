"""Offline validation and explicit planning estimates for a fresh finite run."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import time
from unittest.mock import patch

from harness_utils import hash_file
from runners import run_finite_semantic_consolidation as finite
from runners.finite_run_report import argument_parser as report_parser
from runners.run_codex_provider_attempt import preloaded_context


class CapacityUnknown(ValueError):
    """A missing planning input or local tokenizer is never evidence of fit."""


class OutputRefused(ValueError):
    """Even a refusal record must not be written into an execution root."""


def offline_tokenizer(encoding):
    try:
        import tiktoken
        import tiktoken.load
        if not callable(getattr(tiktoken, "get_encoding", None)):
            raise ImportError("tiktoken package is not readable")
    except ImportError as exc:
        raise CapacityUnknown("preparation requires the optional preparation dependency tiktoken and a cached encoding") from exc

    def cached_only(url, expected_hash=None):
        # Match tiktoken's cache naming, but never fetch, delete, or rewrite it.
        cache = os.environ.get("TIKTOKEN_CACHE_DIR", os.environ.get("DATA_GYM_CACHE_DIR",
            str(Path(tempfile.gettempdir()) / "data-gym-cache")))
        if not cache:
            raise CapacityUnknown("offline tokenizer requires an enabled local encoding cache")
        path = Path(cache) / hashlib.sha1(url.encode()).hexdigest()
        try:
            data = path.read_bytes()
        except OSError as exc:
            raise CapacityUnknown(f"offline tokenizer cache unavailable: {path}") from exc
        if expected_hash is None or hashlib.sha256(data).hexdigest() != expected_hash:
            raise CapacityUnknown(f"offline tokenizer cache hash unavailable or mismatched: {path}")
        return data

    try:
        # Constructors load vocabularies through this boundary. Cache misses
        # must remain offline even when tiktoken would ordinarily download.
        with patch.object(tiktoken.load, "read_file_cached", cached_only):
            tokenizer = tiktoken.get_encoding(encoding)
        return tokenizer, tiktoken.__version__
    except (OSError, ValueError, AttributeError) as exc:
        raise CapacityUnknown(f"offline tokenizer unavailable: {exc}") from exc


def launch_arguments(argv):
    """Parse through the execution owners; normalize paths, preserve settings."""
    argv = list(argv[1:] if argv[:1] == ["--"] else argv)
    report = None
    if argv[:1] == ["run-and-report"]:
        report = report_parser().parse_args(argv[1:])
        argv = report.finite_args
        argv = argv[1:] if argv[:1] == ["--"] else argv
        from command_execution import positive
        positive(report.timeout_seconds)
        report.report_dir = report.report_dir.resolve()
    args = finite.argument_parser().parse_args(argv)
    if args.replay_from or args.provider_root or args.local_repair_successor or args.completed_recovery:
        raise ValueError("prepare requires a fresh run, without replay, provider reuse, or recovery arguments")
    normalized = []
    for name in ("source", "bundle", "verified", "questions", "previous_answer", "output_dir", "codex_executable"):
        path = getattr(args, name)
        if path is not None:
            path = path.resolve()
            setattr(args, name, path)
            normalized.extend(["--" + name.replace("_", "-"), str(path)])
    if report:
        normalized = ["run-and-report", "--report-dir", str(report.report_dir),
            "--model", report.model, "--reasoning-effort", report.reasoning_effort,
            "--timeout-seconds", str(report.timeout_seconds), "--", *normalized]
    return args, report, [sys.executable, "-X", "utf8", "-m", "runners.run_finite_semantic_consolidation", *normalized]


def fresh_outputs(result_path, args, report, input_paths):
    outputs = [result_path, args.output_dir]
    if report:
        outputs.append(report.report_dir)
    for path in outputs:
        if path.exists():
            raise ValueError(f"preparation requires a fresh output path: {path}")
        if any(path != other and (path.is_relative_to(other) or other.is_relative_to(path))
               for other in outputs) or len(set(outputs)) != len(outputs):
            raise OutputRefused("preparation result, run and report outputs must be separate, non-overlapping paths")
        if any(p == path or p.is_relative_to(path) for p in input_paths):
            raise OutputRefused(f"output overlaps an input or original proof dependency: {path}")


def commission(questions, bundle):
    """Validate supplied anchors; an absent check commission remains pending."""
    items = questions.get("questions")
    if not isinstance(items, list) or not items:
        raise ValueError("questions must be a nonempty list")
    for item in items:
        if not isinstance(item, dict) or any(not isinstance(item.get(k), str) or not item[k].strip()
                                             for k in ("id", "question")):
            raise ValueError("each question requires nonempty id and question text")
    finite.answer_schema(items)
    if not isinstance(questions.get("worker_instructions"), str) or not questions["worker_instructions"].strip():
        raise ValueError("worker_instructions must be nonempty text")
    if "coverage" not in questions or questions["coverage"] is None:
        raise ValueError("questions require explicit coverage")
    assessment = questions.get("assessment_only")
    if assessment is None and "assessment_only" not in questions:
        return False
    if not isinstance(assessment, dict):
        raise ValueError("assessment_only must be an object")
    if "checks" not in assessment:
        return False
    checks = assessment["checks"]
    if not isinstance(checks, list):
        raise ValueError("assessment_only.checks must be a list")
    finite.assessment_generation_schema(checks)
    known = {r["evidence_id"] for r in bundle["evidence_units"]}
    for check in checks:
        refs = check.get("source_rows")
        if (not isinstance(refs, list) or not refs or
                any(not isinstance(ref, str) or not ref.strip() for ref in refs)):
            raise ValueError(f"check {check['id']} requires nonempty source_rows references")
        missing = set(refs) - known
        if missing:
            raise ValueError(f"check {check['id']} references absent source rows: {sorted(missing)}")
        if not isinstance(check.get("expectation"), str) or not check["expectation"].strip():
            raise ValueError(f"check {check['id']} requires nonempty expectation text")
    return True


def estimate(settings, source, bundle, verified, questions, previous, prompts):
    fields = ("encoding", "effective_context_tokens", "generated_content_reserve_tokens",
              "output_reserve_tokens", "other_overhead_reserve_tokens")
    missing = [name for name in fields if getattr(settings, name) is None]
    if missing:
        raise CapacityUnknown("missing explicit capacity inputs: " + ", ".join(missing))
    for name in fields[1:]:
        if getattr(settings, name) < (1 if name == "effective_context_tokens" else 0):
            raise ValueError(f"invalid capacity input: {name}")
    tokenizer, version = offline_tokenizer(settings.encoding)
    count = lambda text: len(tokenizer.encode(text, disallowed_special=()))
    context, manifest = preloaded_context(finite.CONTEXT)

    def measure(prompt, schema, reserve):
        envelope = json.dumps({"required_context": context, "task_prompt": prompt}, ensure_ascii=False)
        envelope_tokens = count(envelope)
        schema_tokens = count(json.dumps(schema, ensure_ascii=False))
        total = envelope_tokens + schema_tokens
        return {"envelope_tokens": envelope_tokens, "schema_tokens": schema_tokens,
                "total_tokens": total, "margin_after_reserves_tokens": settings.effective_context_tokens - total - reserve}

    probe_questions = deepcopy(questions)
    probe_questions.setdefault("assessment_only", {}).setdefault("checks", [])
    empty_answer = {"schema_version": "finite_answer_v1", "answers": [
        {"question_id": q["id"], "answer": "", "evidence_refs": [], "limits": ""} for q in questions["questions"]]}
    assessment = finite.assessment_input(source, verified, probe_questions, previous, empty_answer, {}, {})
    probe_view = {"propositions": [], "unmerged_semantic_units": [
        {"semantic_unit_ref": u["semantic_unit_ref"],
         "reason": "capacity probe only: all verified units represented as residuals; no judgment asserted"}
        for u in verified["semantic_units"]]}
    answer = finite.answer_input(bundle, verified, questions, probe_view, {}, [])
    known = {r["evidence_id"] for r in bundle["evidence_units"]} | {u["semantic_unit_ref"] for u in verified["semantic_units"]}
    reserves = {name: getattr(settings, name) for name in fields[2:]}
    total_reserve = sum(reserves.values())
    measurements = {
        "assessment_fixed": measure(finite.render_assessment(assessment, keyed_checks=True, exact_repairs=True),
            finite.assessment_generation_schema(probe_questions["assessment_only"]["checks"], exact_repairs=True,
                answer=empty_answer, known_refs=known), total_reserve),
        "answer_all_residual_probe": measure(finite.render_answer(answer),
            finite.answer_generation_schema(questions["questions"], bundle["evidence_units"], verified["semantic_units"]), total_reserve),
    }
    formation = [measure(row["prompt"] + "\n", row["response_schema"],
        settings.output_reserve_tokens + settings.other_overhead_reserve_tokens) for row in prompts]
    measurements["largest_formation_request"] = max(formation, key=lambda row: row["total_tokens"])
    return {"encoding": settings.encoding, "tiktoken_version": version,
        "effective_context_tokens": settings.effective_context_tokens, "reserves": reserves,
        "assumptions_source": "explicit caller planning settings; no universal model context limit",
        "serialization_basis": "json.dumps envelope and schema with ensure_ascii=False and default separators; CLI framing and native schema transport are not attested",
        "context_inputs": manifest, "measurements": measurements,
        "fits_planning_allowances": all(row["margin_after_reserves_tokens"] >= 0 for row in measurements.values()),
        "limitations": ["Tokenizer equivalence to the execution model is not attested.",
            "Generated view, packet, axes, answer, finish and correction requests are unknown; reserves are planning allowances, not upper bounds.",
            "The all-residual answer probe is not the eventual answer request or a bound on its size.",
            "Final report capacity is not estimated. Provider overhead and output policy are not measured.",
            "Estimated fit neither guarantees execution fit nor establishes intelligence quality or launch authorization."]}


def prepare(settings, result):
    args, report, argv = launch_arguments(settings.execution_args)
    paths = [getattr(args, name) for name in ("source", "bundle", "verified", "questions", "previous_answer")]
    fresh_outputs(settings.result_out, args, report, paths)
    values = [finite.read(path) for path in paths]
    source, bundle, verified, questions, previous = values
    dependencies = verified.get("verified_row_selection", {}).get("original_inputs", {})
    fresh_outputs(settings.result_out, args, report, paths + [Path(v["path"]).resolve() for v in dependencies.values()])
    result["inputs"] = {name: {"path": str(path), "sha256": hash_file(path)}
                        for name, path in zip(("source", "bundle", "verified", "questions", "previous_answer"), paths)}
    if dependencies:
        finite.validate_verified_selection(bundle, verified, source=source)
        result["verified_selection_original_inputs"] = dependencies
    finite.validate_finite_bundle(source, bundle)
    complete = commission(questions, bundle)
    # Use the same formation owner as execution: checks all native prerequisites
    # and prompt bounds without persisting a stage or invoking a worker.
    stage, prompts = finite.semantic.prepare_reconciliation_stage(bundle, verified, **finite.POLICY, packing_strategy="input_order")
    if stage["completion_phase"] != "formation" or stage["max_prompt_bytes"] != 80000:
        raise ValueError("finite phase or prompt ceiling differs")
    # Validate locator prerequisites even if capacity settings/tokenizer are absent.
    sizing_questions = deepcopy(questions)
    sizing_questions.setdefault("assessment_only", {}).setdefault("checks", [])
    finite.assessment_input(source, verified, sizing_questions, previous, {}, {}, {})
    units = {u["evidence_id"] for u in verified["semantic_units"]}
    result.update(validation="passed", commissioned_checks="supplied" if complete else "pending",
        counts={"source_rows": len(bundle["evidence_units"]), "semantic_units": len(verified["semantic_units"]),
                "no_unit_rows": len({r["evidence_id"] for r in bundle["evidence_units"]} - units),
                "containers": len({r["container_id"] for r in source["captured_items"]}), "formation_batches": len(prompts)},
        finite_policy=finite.POLICY,
        execution_settings={"model": "gpt-5.6-sol", "reasoning_effort": "high", "timeout_seconds": 1800},
        runtime_prerequisites="Native executable, authentication and provider availability remain execution-time checks; no executable launched.")
    result["capacity"] = estimate(settings, source, bundle, verified, questions, previous, prompts)
    # A race changing selected inputs cannot leave a launchable result.
    for record in result["inputs"].values():
        if hash_file(Path(record["path"])) != record["sha256"]:
            raise ValueError(f"input changed during preparation: {record['path']}")
    for record in dependencies.values():
        if hash_file(Path(record["path"])) != record["sha256"]:
            raise ValueError(f"original proof changed during preparation: {record['path']}")
    if not result["capacity"]["fits_planning_allowances"]:
        result["status"] = "FINITE_PREPARATION_CAPACITY_EXCEEDED"
    elif not complete:
        result["status"] = "FINITE_PREPARATION_CHECKS_PENDING"
    else:
        fresh_outputs(settings.result_out, args, report, paths)
        result.update(status="FINITE_PREPARATION_ESTIMATED_FIT", launch={"cwd": str(finite.HARNESS), "argv": argv})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, epilog="After -- supply ordinary finite arguments or run-and-report and its arguments. Never launches jobs.")
    parser.add_argument("--result-out", required=True, type=Path, help="New compact JSON file outside fresh run/report output roots")
    parser.add_argument("--encoding", help="Explicit locally cached tiktoken encoding")
    for name in ("effective-context-tokens", "generated-content-reserve-tokens", "output-reserve-tokens", "other-overhead-reserve-tokens"):
        parser.add_argument("--" + name, type=int)
    parser.add_argument("execution_args", nargs=argparse.REMAINDER)
    settings = parser.parse_args(argv)
    settings.result_out = settings.result_out.resolve()
    start = time.perf_counter()
    result = {"status": "FINITE_PREPARATION_REFUSED", "provider_calls": 0, "preparation_invocations": 1,
              "validation": "not_completed", "launch": None,
              "planning_inputs": {name: getattr(settings, name) for name in (
                  "encoding", "effective_context_tokens", "generated_content_reserve_tokens",
                  "output_reserve_tokens", "other_overhead_reserve_tokens")}}
    try:
        # Only the result file is written; never create execution outputs.
        if settings.result_out.exists():
            raise FileExistsError(f"preparation result already exists: {settings.result_out}")
        prepare(settings, result)
    except OutputRefused as exc:
        print(json.dumps({"status": "FINITE_PREPARATION_REFUSED", "error": str(exc), "provider_calls": 0}))
        return 1
    except CapacityUnknown as exc:
        result.update(status="FINITE_PREPARATION_CAPACITY_UNKNOWN", error=str(exc))
    except Exception as exc:
        result.update(status="FINITE_PREPARATION_REFUSED", error_type=type(exc).__name__, error=str(exc))
    result["elapsed_seconds"] = round(time.perf_counter() - start, 6)
    try:
        settings.result_out.parent.mkdir(parents=True, exist_ok=True)
        with settings.result_out.open("x", encoding="utf-8", newline="\n") as out:
            out.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        if finite.read(settings.result_out) != result:
            raise ValueError("preparation result readback differs")
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "FINITE_PREPARATION_REFUSED", "error": str(exc), "provider_calls": 0}))
        return 1
    print(json.dumps({"status": result["status"], "result": str(settings.result_out),
        "elapsed_seconds": result["elapsed_seconds"], "output_bytes": settings.result_out.stat().st_size, "provider_calls": 0}))
    return 0 if result["status"] == "FINITE_PREPARATION_ESTIMATED_FIT" else 1
