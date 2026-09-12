"""Measure complete commands and compare explicit sets of operational records.

Run with ``python -m runners.run_efficiency`` from the harness directory.
No shell interpolation, provider calls, or quality assertions are added here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from uuid import NAMESPACE_URL, uuid4, uuid5

from harness_efficiency import aggregate_usage, current_revision, make_record, utc_now, write_record
from reports.efficiency_codex import collect_codex_exec, collect_desktop_task
from reports.efficiency_compare import compare_runs
from reports.compact_return import bounded_json, output_budget, write_verified


def _json(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def _argv(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or not value or any(not isinstance(arg, str) for arg in value):
        raise ValueError(f"{label} must be a nonempty JSON array of strings")
    if not value[0]:
        raise ValueError(f"{label} executable must be nonempty")
    if os.name == "nt":
        resolved = shutil.which(value[0]) or value[0]
        if Path(resolved).suffix.lower() in {".cmd", ".bat"}:
            raise ValueError("Windows shell wrappers are unsupported; use the native executable with shell=False")
    return value


def _checker_identity(argv: list[str], cwd: Path) -> str:
    # Bind the checker argv and any referenced local files, including scripts.
    # A changed script must not silently remain the same acceptance oracle.
    files = {}
    for index, argument in enumerate(argv):
        path = Path(shutil.which(argument) or argument) if index == 0 else Path(argument)
        path = path if path.is_absolute() else cwd / path
        if path.is_file():
            files[str(index)] = hashlib.sha256(path.read_bytes()).hexdigest()
    body = json.dumps({"argv": argv, "files": files}, sort_keys=True).encode()
    return "sha256:" + hashlib.sha256(body).hexdigest()


def _stop_tree(process: subprocess.Popen) -> list[str]:
    issues = []
    try:
        if os.name == "nt":
            result = subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                    timeout=5, shell=False)
            if result.returncode:
                issues.append("descendant_timeout_cleanup_unconfirmed")
        else:
            os.killpg(process.pid, signal.SIGKILL)
    except (OSError, subprocess.SubprocessError):
        issues.append("descendant_timeout_cleanup_unconfirmed")
    if process.poll() is None:
        process.kill()
    process.wait(timeout=5)
    return issues


def _execute(argv: list[str], *, cwd: Path, timeout: float, stdin=None, stdout=None,
             stderr=None) -> tuple[int, list[str]]:
    try:
        process = subprocess.Popen(argv, cwd=cwd, stdin=stdin, stdout=stdout, stderr=stderr,
                                   shell=False, start_new_session=os.name != "nt")
    except OSError as exc:
        return 127, [f"command_launch_failed:{type(exc).__name__}"]
    try:
        return process.wait(timeout=timeout), []
    except subprocess.TimeoutExpired:
        return 124, ["command_timeout", *_stop_tree(process)]


def _last_message(path: Path) -> str | None:
    last = None
    with path.open(encoding="utf-8-sig", errors="replace") as handle:
        for line in handle:
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if isinstance(row, dict) and row.get("type") == "item.completed":
                item = row.get("item")
                if isinstance(item, dict) and item.get("type") == "agent_message" and isinstance(item.get("text"), str):
                    last = item["text"]
    return last


def _measure(args: argparse.Namespace) -> int:
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    command = _argv(command, "command")
    if not math.isfinite(args.timeout_seconds) or args.timeout_seconds <= 0:
        raise ValueError("timeout-seconds must be finite and positive")
    cwd = Path(args.cwd or os.getcwd()).resolve(strict=True)
    if not cwd.is_dir():
        raise ValueError("cwd must be a directory")
    configuration = _json(args.configuration) if args.configuration else {}
    if not isinstance(configuration, dict):
        raise ValueError("configuration must be a JSON object")
    json.dumps(configuration, allow_nan=False)
    checker = _argv(_json(args.quality_command), "quality command") if args.quality_command else None
    oracle = _checker_identity(checker, cwd) if checker else None
    if args.codex_json:
        if (Path(command[0]).name.lower() not in {"codex", "codex.exe", "codex.cmd"}
                or len(command) < 2 or command[1] != "exec" or "--json" not in command
                or "resume" in command[2:]):
            raise ValueError("--codex-json requires a fresh codex exec --json command (no resume)")
    quality = {"status": "unmeasured", "oracle": oracle, "output_fingerprint": None}
    summary = {"attempts": [], "coverage": "unknown", "issues": ["no_observed_model_usage"]}
    started_at = utc_now()
    started = time.perf_counter()
    stdin = Path(args.stdin_file).open("rb") if args.stdin_file else None
    try:
        if args.codex_json:
            # The exact raw file is invocation-owned and deleted after collection.
            # Prompts/tool output never become permanent measurement artifacts.
            descriptor, raw_name = tempfile.mkstemp(prefix="forseti-efficiency-", suffix=".jsonl")
            raw_path = Path(raw_name)
            try:
                with os.fdopen(descriptor, "wb") as raw:
                    return_code, issues = _execute(command, cwd=cwd, timeout=args.timeout_seconds,
                                                  stdin=stdin, stdout=raw)
                summary = collect_codex_exec(raw_path, fresh_session=True,
                                             model=configuration.get("model"))
                message = _last_message(raw_path)
                if message is not None:
                    print(message)
            finally:
                raw_path.unlink()
        else:
            return_code, issues = _execute(command, cwd=cwd, timeout=args.timeout_seconds, stdin=stdin)
    finally:
        if stdin is not None:
            stdin.close()
    checker_exit = None
    if checker and return_code == 0:
        checker_exit, checker_issues = _execute(checker, cwd=cwd, timeout=args.timeout_seconds)
        issues.extend(f"quality:{issue}" for issue in checker_issues)
        quality["status"] = "passed" if checker_exit == 0 else "failed"
        if checker_exit:
            return_code = checker_exit
    elapsed = time.perf_counter() - started
    record = make_record(
        workflow=args.workflow, workload_id=args.workload_id, configuration=configuration,
        revision=current_revision(), elapsed_seconds=elapsed,
        outcome="success" if return_code == 0 else "failed", quality=quality,
        attempts=summary["attempts"], started_at=started_at, ended_at=utc_now(),
        return_code=return_code, quality_return_code=checker_exit, measurement_errors=issues,
        **({"pair_id": args.pair_id} if args.pair_id else {}),
    )
    # Collector completeness includes missing children/truncation, not merely
    # the usage-bearing attempts that happened to arrive.
    if summary["coverage"] != "complete" or issues:
        record["usage"]["coverage"] = "unknown"
        record["usage"]["issues"] = sorted(set(record["usage"]["issues"] + summary["issues"] + issues))
    record["collection"] = {key: value for key, value in summary.items() if key != "attempts"}
    path = write_record(record, Path(args.output_dir))
    print(json.dumps({"record_path": str(path.resolve()), "outcome": record["outcome"],
                      "quality": quality["status"], "usage_coverage": record["usage"]["coverage"]}))
    return return_code if 0 <= return_code <= 255 else 1


def _compare(args: argparse.Namespace) -> int:
    report = compare_runs([_json(path) for path in args.baseline], [_json(path) for path in args.candidate],
                          minimum_pairs=args.minimum_pairs, relative_threshold=args.threshold)
    path = Path(args.output) if args.output else Path(os.environ.get(
        "FORSETI_EFFICIENCY_DIR", "memory/logs/efficiency")) / f"comparison-{uuid4()}.json"
    path = write_verified(report, path)
    returned = {**report, "record_path": str(path), "record_readback_matched": True}
    print(bounded_json(returned, record_path=path, facts={"overall": report["overall"]},
                       budget=getattr(args, "max_output_bytes", 8192)), end="")
    return 0


def _desktop_return(record: dict, path: Path) -> dict:
    """Return the collected decision facts without rereading the detailed record."""
    collection = record["collection"]
    by_thread = {}
    for attempt in record["attempts"]:
        thread = attempt.get("thread_id")
        if isinstance(thread, str):
            by_thread.setdefault(thread, []).append(attempt)
    return {
        "record_path": str(path.resolve()), "outcome": record["outcome"],
        "quality": record["quality"]["status"],
        "quality_return_code": record["quality_return_code"],
        "usage_coverage": record["usage"]["coverage"], "usage": record["usage"],
        "model_responses": sum(isinstance(a.get("response_id"), str) for a in record["attempts"]),
        "threads": {thread: {"model_responses": sum(isinstance(a.get("response_id"), str) for a in attempts),
                             "usage": aggregate_usage(attempts)}
                    for thread, attempts in by_thread.items()},
        "tool_call_events": collection.get("tools", {}),
        "tool_output_observations": collection.get("tool_output_observations"),
        "observed_settings": collection.get("observed_settings"),
        "collection_issues": collection.get("issues", []),
        "child_coverage": collection.get("child_coverage"),
        "selected_turns": collection.get("selected_turns"),
        "started_at": record.get("started_at"), "ended_at": record.get("ended_at"),
        "elapsed_seconds": record["elapsed_seconds"],
        "validation_elapsed_seconds": record["validation_elapsed_seconds"],
        "validation_issues": record["validation_issues"],
    }


class IncompleteDesktopTurn(ValueError):
    def __init__(self, observation: dict):
        super().__init__("selected Desktop turn has no complete observed elapsed interval")
        self.observation = observation


def _collect_codex(args: argparse.Namespace) -> tuple[dict, dict, int]:
    configuration = _json(args.configuration) if args.configuration else {}
    if not isinstance(configuration, dict):
        raise ValueError("configuration must be a JSON object")
    json.dumps(configuration, allow_nan=False)
    if not math.isfinite(args.timeout_seconds) or args.timeout_seconds <= 0:
        raise ValueError("timeout-seconds must be finite and positive")
    cwd = Path(args.cwd or os.getcwd()).resolve(strict=True)
    if not cwd.is_dir():
        raise ValueError("cwd must be a directory")
    checker = _argv(_json(args.quality_command), "quality command") if args.quality_command else None
    oracle = _checker_identity(checker, cwd) if checker else None
    summary = collect_desktop_task(args.sessions_dir, args.thread_id, args.turn_id)
    observed_models = summary.get("observed_models", [])
    if not isinstance(observed_models, list) or any(not isinstance(model, str) for model in observed_models):
        raise ValueError("collector observed_models must be a list of model names")
    observed_models = sorted(set(observed_models))
    if "observed_models" in configuration and configuration["observed_models"] != observed_models:
        raise ValueError("configuration cannot overwrite source observed_models")
    configuration = {**configuration, "observed_models": observed_models}
    elapsed = summary.get("elapsed_seconds")
    if isinstance(elapsed, bool) or not isinstance(elapsed, (int, float)) or not math.isfinite(elapsed) or elapsed < 0:
        # Preserve the collector's explanation, without manufacturing a completed
        # run interval from file times or the import operation's own duration.
        path = write_verified(summary, Path(args.output_dir) / "diagnostics" / f"incomplete-{uuid4()}.json")
        raise IncompleteDesktopTurn({**summary, "record_path": str(path)})
    quality = {"status": "unmeasured", "oracle": oracle, "output_fingerprint": None}
    checker_exit = None
    validation_elapsed = None
    validation_issues = []
    if checker:
        validation_started = time.perf_counter()
        logs = Path(args.output_dir).resolve() / f"validation-{uuid4()}"
        logs.mkdir(parents=True, exist_ok=False)
        with (logs / "stdout.txt").open("x", encoding="utf-8") as stdout, (logs / "stderr.txt").open("x", encoding="utf-8") as stderr:
            checker_exit, validation_issues = _execute(checker, cwd=cwd, timeout=args.timeout_seconds,
                                                       stdout=stdout, stderr=stderr)
        validation_elapsed = time.perf_counter() - validation_started
        quality["status"] = "passed" if checker_exit == 0 else "failed"
    # A recovered request does not fail the whole run. An explicitly failed or
    # aborted selected turn remains a failure even if a later checker passes.
    failed = quality["status"] == "failed" or "selected_turn_failed_or_aborted" in summary["issues"]
    result = make_record(
        workflow=args.workflow, workload_id=args.workload_id, configuration=configuration,
        revision=args.revision, elapsed_seconds=elapsed,
        run_id=str(uuid5(NAMESPACE_URL, json.dumps(["forseti-codex-desktop", args.thread_id, args.turn_id]))),
        outcome="failed" if failed else "success",
        quality=quality,
        attempts=summary["attempts"], started_at=summary.get("root_started_at"),
        ended_at=summary.get("workunit_completed_at") or summary.get("root_completed_at"),
        validation_elapsed_seconds=validation_elapsed, quality_return_code=checker_exit,
        validation_issues=validation_issues,
        **({"pair_id": args.pair_id} if args.pair_id else {}),
    )
    if summary["coverage"] != "complete":
        result["usage"]["coverage"] = "unknown"
        result["usage"]["issues"] = sorted(set(result["usage"]["issues"] + summary["issues"]))
    result["collection"] = {key: value for key, value in summary.items() if key != "attempts"}
    if checker:
        result["validation_logs"] = {"stdout": str(logs / "stdout.txt"), "stderr": str(logs / "stderr.txt")}
    path = write_record(result, Path(args.output_dir))
    persisted = _json(path)
    if persisted != result:
        raise ValueError("saved Desktop measurement differs from collected record")
    returned = _desktop_return(persisted, path)
    returned["record_readback_matched"] = True
    if checker:
        returned["validation_logs"] = persisted["validation_logs"]
    code = (checker_exit if checker_exit is not None and 0 < checker_exit <= 255 else 1) if failed else 0
    return returned, persisted, code


def _import_codex(args: argparse.Namespace) -> int:
    try:
        returned, _, code = _collect_codex(args)
    except IncompleteDesktopTurn as exc:
        print(bounded_json(exc.observation, record_path=Path(exc.observation["record_path"]),
                           facts={"coverage": "unknown", "completion": "incomplete"},
                           budget=args.max_output_bytes), end="")
        raise
    path = Path(returned["record_path"])
    print(bounded_json(returned, record_path=path,
                       facts={"outcome": returned["outcome"], "quality": returned["quality"],
                              "quality_return_code": returned["quality_return_code"], "usage_coverage": returned["usage_coverage"],
                              "collection_issue_count": len(returned["collection_issues"])},
                       budget=getattr(args, "max_output_bytes", 8192)), end="")
    return code


def _report_codex(args: argparse.Namespace) -> int:
    from reports.efficiency_batch import reconcile_runs, selection

    manifest_path = Path(args.selection).resolve(strict=True)
    runs, comparisons = selection(_json(manifest_path), manifest_path.parent)
    destination = Path(args.output_dir).resolve() / f"batch-{uuid4()}"
    records, rows = {}, []
    for index, run in enumerate(runs):
        label = run.pop("label")
        options = argparse.Namespace(sessions_dir=args.sessions_dir, output_dir=str(destination / str(index)), **run)
        try:
            returned, record, code = _collect_codex(options)
            records[label] = record
            rows.append({"label": label, "exit_code": code, **returned})
        except (ValueError, OSError, subprocess.SubprocessError) as exc:
            row = {"label": label, "exit_code": 2, "outcome": "uncollected", "error": str(exc)}
            if isinstance(exc, IncompleteDesktopTurn):
                row["diagnostic_path"] = exc.observation["record_path"]
            rows.append(row)
    accounting = reconcile_runs(records, uncollected=[row["label"] for row in rows if row["outcome"] == "uncollected"])
    compared = []
    for requested in comparisons:
        try:
            report = compare_runs([records[label] for label in requested["baseline"]],
                                  [records[label] for label in requested["candidate"]])
        except (KeyError, ValueError) as exc:
            report = {"overall": "inconclusive", "reasons": [f"comparison unavailable: {exc}"]}
        compared.append({"label": requested["label"], **report})
    code = next((row["exit_code"] for row in rows if row["exit_code"]), 0)
    if accounting["conflicts"]:
        code = 2
    result = {"status": "failed" if code else "observed", "runs": rows,
              "accounting": accounting, "comparisons": compared}
    path = write_verified(result, destination / "report.json")
    returned = {"status": result["status"], "record_path": str(path), "record_readback_matched": True,
                "accounting": accounting,
                "runs": [{key: row[key] for key in ("label", "exit_code", "outcome", "quality", "usage_coverage",
                         "model_responses", "elapsed_seconds", "record_path", "diagnostic_path", "error") if key in row}
                         for row in rows],
                "comparisons": [{"label": row["label"], "overall": row["overall"], "reasons": row["reasons"]}
                                for row in compared]}
    print(bounded_json(returned, record_path=path,
                       facts={"status": result["status"], "selected_runs": len(rows),
                              "failed_or_uncollected_runs": sum(row["exit_code"] != 0 for row in rows),
                              "usage_coverage": accounting["usage"]["coverage"],
                              "unique_model_responses": accounting["unique_model_responses"]},
                       budget=args.max_output_bytes), end="")
    return code


def _repo_size(args: argparse.Namespace) -> int:
    from reports.efficiency_repository import repository_size

    current = repository_size(Path(args.repo), args.revision)
    result = {"snapshot": current}
    if args.base:
        baseline = repository_size(Path(args.repo), args.base)
        result["baseline"] = baseline
        fields = ("tracked_bytes", "tracked_file_count", "instruction_source_bytes",
                  "instruction_source_file_count")
        result["delta"] = {field: current[field] - baseline[field] for field in fields}
        result["delta_scope"] = "logical tracked content; current physical measurement logs are not historical deltas"
    print(json.dumps(result, allow_nan=False, sort_keys=True, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="subcommand", required=True)
    compare = commands.add_parser("compare", help="Compare explicit ordered run files; verdict is descriptive")
    compare.add_argument("--baseline", nargs="+", required=True)
    compare.add_argument("--candidate", nargs="+", required=True)
    compare.add_argument("--minimum-pairs", type=int, default=3)
    compare.add_argument("--threshold", type=float, default=0.05)
    compare.add_argument("--output", help="Optional new report file (exclusive creation)")
    compare.add_argument("--max-output-bytes", type=output_budget, default=8192)
    compare.set_defaults(handler=_compare)
    measure = commands.add_parser("measure", help="Measure a complete command plus optional independent checker")
    measure.add_argument("--workflow", required=True)
    measure.add_argument("--workload-id", required=True, help="Fixture content identity, not just a case label")
    measure.add_argument("--configuration", help="JSON file containing comparable model/settings/environment")
    measure.add_argument("--output-dir", required=True)
    measure.add_argument("--cwd")
    measure.add_argument("--timeout-seconds", type=float, default=300)
    measure.add_argument("--quality-command", help="JSON argv array for an independent output checker")
    measure.add_argument("--pair-id")
    measure.add_argument("--codex-json", action="store_true")
    measure.add_argument("--stdin-file", help="Supply exact command stdin, e.g. a Codex prompt")
    measure.add_argument("command", nargs=argparse.REMAINDER)
    measure.set_defaults(handler=_measure)
    imported = commands.add_parser("import-codex", help="Import one observed Desktop turn with linked child usage")
    imported.add_argument("--sessions-dir", required=True, help="Explicit session folder covering the selected work")
    imported.add_argument("--thread-id", required=True)
    imported.add_argument("--turn-id", required=True)
    imported.add_argument("--workflow", required=True)
    imported.add_argument("--workload-id", required=True)
    imported.add_argument("--configuration")
    imported.add_argument("--revision", help="Observed run revision; omitted remains unknown")
    imported.add_argument("--output-dir", required=True)
    imported.add_argument("--pair-id")
    imported.add_argument("--quality-command", help="JSON argv for an independent post-hoc output checker")
    imported.add_argument("--cwd", help="Post-hoc checker working directory")
    imported.add_argument("--timeout-seconds", type=float, default=300)
    imported.add_argument("--max-output-bytes", type=output_budget, default=8192)
    imported.set_defaults(handler=_import_codex)
    batch = commands.add_parser("report-codex", help="Collect explicit completed tasks and reconcile their shared usage once")
    batch.add_argument("--sessions-dir", required=True)
    batch.add_argument("--selection", required=True, help="JSON runs and optional named baseline/candidate label lists")
    batch.add_argument("--output-dir", required=True)
    batch.add_argument("--max-output-bytes", type=output_budget, default=8192)
    batch.set_defaults(handler=_report_codex)
    size = commands.add_parser("repo-size", help="Observe tracked logical content and current measurement log size")
    size.add_argument("--repo", required=True)
    size.add_argument("--revision", default="HEAD")
    size.add_argument("--base", help="Optional historical revision for logical tracked-content delta")
    size.set_defaults(handler=_repo_size)
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f"efficiency command failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
