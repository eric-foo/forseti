"""One command operation, independently resumable observation, no automatic retry.

run_efficiency owns the public entry. The detached worker owns execution and
the supplied checker; observers only read its immutable result and lock state.
"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
from uuid import uuid4

from harness_efficiency import utc_now
from harness_utils import hash_file
from provider_jobs import _lock
from reports.compact_return import bounded_json, output_budget, write_verified


# An observer holds the worker lock only long enough to read one record, so lock
# contention alone identifies neither a second worker nor a live one. The worker
# outwaits peer holds instead of dying; single execution stays owned by the
# exclusive `worker.json` create below. An observer outwaits a peer observer so a
# dead operation is not reported as running; a live worker holds the lock for its
# whole lifetime and is still observed as running after this bounded wait.
WORKER_LOCK_WAIT_SECONDS = 30
OBSERVER_LOCK_WAIT_SECONDS = 0.25


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def positive(value):
    if value is not None and (not math.isfinite(value) or value <= 0):
        raise ValueError("deadline/wait must be finite and positive when supplied")
    return value


def launch(args):
    from runners.run_efficiency import _argv, _checker_identity
    command = _argv(args.command[1:] if args.command[:1] == ["--"] else args.command, "command")
    cwd = Path(args.cwd or os.getcwd()).resolve(strict=True)
    if not cwd.is_dir():
        raise ValueError("cwd must be a directory")
    selection = None
    if args.bind_codex:
        # Resolve before detachment; arbitrary non-provider commands need no Codex.
        from runners.run_codex_provider_attempt import select_codex_executable
        selection = select_codex_executable()
    checker = _argv(read(Path(args.quality_command)), "quality command") if args.quality_command else None
    directory = Path(args.operation_dir).resolve()
    manifest = {"operation_id": str(uuid4()), "created_at": utc_now(), "cwd": str(cwd),
                "command": command, "command_identity": _checker_identity(command, cwd),
                "codex_selection": selection,
                "checker": checker, "checker_identity": _checker_identity(checker, cwd) if checker else None,
                "timeout_seconds": positive(args.timeout_seconds),
                "validation_timeout_seconds": positive(args.validation_timeout_seconds),
                "provider_roots": [str(Path(p).resolve()) for p in args.provider_root],
                "stdin_file": str(Path(args.stdin_file).resolve(strict=True)) if args.stdin_file else None,
                "stdin_sha256": hash_file(Path(args.stdin_file)) if args.stdin_file else None}
    # Atomic operation reservation is also the concurrency/idempotency boundary.
    # An uncertain launch stays reserved. Neither start nor resume retries it.
    directory.mkdir(parents=True, exist_ok=False)
    write_verified(manifest, directory / "operation.json")
    (directory / "worker.lock").touch(exist_ok=False)
    environment = dict(os.environ)
    if selection:
        selected_path = write_verified(selection, directory / "codex-selection.json")
        environment["FORSETI_CODEX_SELECTION"] = str(selected_path)
        environment["FORSETI_CODEX_SELECTION_SHA256"] = hash_file(selected_path)
    worker = [sys.executable, "-m", "runners.run_efficiency", "_operation-worker",
              "--operation-dir", str(directory)]
    creation = {"creationflags": subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP |
                subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {"start_new_session": True}
    with (directory / "worker.stdout").open("xb") as out, (directory / "worker.stderr").open("xb") as err:
        process = subprocess.Popen(worker, cwd=Path(__file__).resolve().parent, stdin=subprocess.DEVNULL,
                                   stdout=out, stderr=err, env=environment, close_fds=True, **creation)
    # Launch return waits only for worker acknowledgement, never command completion.
    deadline = time.monotonic() + 10
    while not (directory / "worker.json").exists() and process.poll() is None and time.monotonic() < deadline:
        time.sleep(0.05)
    return observe(directory)


def _run(command, directory, label, cwd, timeout, identity, stdin_file=None):
    from runners.run_efficiency import _checker_identity, _stop_tree
    started = time.monotonic()
    result = {"exit_code": None, "status": "unknown", "issues": [],
              "stdout_path": str(directory / f"{label}.stdout"),
              "stderr_path": str(directory / f"{label}.stderr")}
    if _checker_identity(command, cwd) != identity:
        result.update(status="refused", issues=[f"{label}_binding_changed"])
        return result
    with (directory / f"{label}.stdout").open("xb") as out, (directory / f"{label}.stderr").open("xb") as err:
        source = Path(stdin_file).open("rb") if stdin_file else None
        try:
            creation = {"creationflags": subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
            process = subprocess.Popen(command, cwd=cwd, stdin=source or subprocess.DEVNULL,
                                       stdout=out, stderr=err, shell=False, **creation)
            write_verified({"pid": process.pid, "started_at": utc_now()}, directory / f"{label}-started.json")
            try:
                result["exit_code"] = process.wait(timeout=timeout)
                result["status"] = "passed" if result["exit_code"] == 0 else "failed"
            except subprocess.TimeoutExpired:
                result["status"] = "timeout"
                result["issues"] = ["explicit_deadline_reached", *_stop_tree(process)]
                result["exit_code"] = process.returncode
        except OSError as exc:
            result.update(status="launch_failed", issues=[type(exc).__name__])
        finally:
            if source:
                source.close()
    result["elapsed_seconds"] = time.monotonic() - started
    return result


def worker(directory):
    from reports.efficiency_codex import collect_provider_roots
    directory = Path(directory).resolve(strict=True)
    with _lock(directory / "worker.lock", wait_seconds=WORKER_LOCK_WAIT_SECONDS):
        # Re-entering the private worker is not a recovery mechanism.
        write_verified({"pid": os.getpid(), "started_at": utc_now()}, directory / "worker.json")
        manifest = read(directory / "operation.json")
        started = time.monotonic()
        cwd = Path(manifest["cwd"])
        # A supplied checker never closes out as "not_requested", including when
        # the run aborts before validation could be reached.
        validation = {"status": "not_run_execution_failed" if manifest["checker"] else "not_requested",
                      "exit_code": None, "issues": []}
        issues = []
        try:
            if manifest["stdin_file"] and hash_file(Path(manifest["stdin_file"])) != manifest["stdin_sha256"]:
                raise ValueError("stdin_binding_changed")
            execution = _run(manifest["command"], directory, "command", cwd, manifest["timeout_seconds"],
                             manifest["command_identity"], manifest["stdin_file"])
            write_verified(execution, directory / "execution.json")
            if manifest["checker"] and execution["status"] == "passed":
                validation = _run(manifest["checker"], directory, "validation", cwd,
                                  manifest["validation_timeout_seconds"], manifest["checker_identity"])
            write_verified(validation, directory / "validation.json")
        except (ValueError, OSError, subprocess.SubprocessError) as exc:
            execution = read(directory / "execution.json") if (directory / "execution.json").exists() else {
                "status": "unknown", "exit_code": None, "issues": [type(exc).__name__]}
            issues.append(f"execution_or_validation_incomplete:{type(exc).__name__}")
        accounting = collect_provider_roots(manifest["provider_roots"], started_at=manifest["created_at"])
        write_verified(accounting, directory / "accounting.json")
        issues.extend(execution["issues"] + validation["issues"] + accounting["issues"])
        passed = execution["status"] == "passed" and validation["status"] in {"passed", "not_requested"}
        status = "completed" if passed and not any(i.startswith("execution_or_validation_incomplete") for i in issues) else "failed"
        result = {"operation_id": manifest["operation_id"], "status": status,
                  "execution": execution, "required_validation": validation,
                  "validation_scope": "supplied checker only; no semantic quality or owner acceptance inferred",
                  "accounting": {k: v for k, v in accounting.items() if k != "attempts"},
                  "issues": sorted(set(issues)), "elapsed_seconds": time.monotonic() - started,
                  "completed_at": utc_now(), "record_path": str(directory / "closeout.json"),
                  "accounting_path": str(directory / "accounting.json"),
                  "operation_path": str(directory / "operation.json"),
                  "observer_cost_scope": "parent active-turn costs remain open; use report-codex after that turn completes"}
        write_verified(result, directory / "closeout.json")


def observe(directory):
    directory = Path(directory).resolve(strict=True)
    manifest = read(directory / "operation.json")
    try:
        with _lock(directory / "worker.lock", wait_seconds=OBSERVER_LOCK_WAIT_SECONDS):
            if (directory / "closeout.json").exists():
                result = read(directory / "closeout.json")
                if result["operation_id"] != manifest["operation_id"]:
                    raise ValueError("closeout operation identity mismatch")
                return {**result, "record_readback_matched": True, "return_view": "summary",
                        "accounting_view": "summary_without_attempts"}
    except ValueError as exc:
        if str(exc) != "provider job or retry budget is already in use":
            raise
        state = "running"
    else:
        state = "unknown"
    return {"operation_id": manifest["operation_id"], "status": state,
            "operation_path": str(directory / "operation.json"),
            "worker_stdout_path": str(directory / "worker.stdout"),
            "worker_stderr_path": str(directory / "worker.stderr"),
            "issues": [] if state == "running" else ["worker_not_observed_and_no_closeout; do not relaunch"],
            "resume_argv": [sys.executable, "-m", "runners.run_efficiency", "resume", "--operation-dir", str(directory)],
            "resume_cwd": str(Path(__file__).resolve().parent),
            "wait_contract": (
                "resume only observes this operation; interrupting it leaves execution running. "
                "Await exec_command and write_stdin continuations inside one functions.exec: "
                "the `// @exec` header sets the outer yield (1500000 ms = one 25-minute review); "
                "inner waits stay <=60s. "
                "Completion returns early; a review interval never kills or relaunches work. "
                "On an outer yield review once, retain its cell and use functions.wait with "
                "yield_time_ms=1500000 if continuing, not one-minute model polling. "
                "If interrupted, invoke this same resume_argv; never start again. "
                "A host yielding earlier is a limitation to report, not proof of quiet waiting. "
                "Policy owner: .agents/workflow-overlay/decision-routing.md -> Task-Local Tool-Stall Circuit.")}


def resume(directory, wait_seconds=None):
    positive(wait_seconds)
    deadline = time.monotonic() + wait_seconds if wait_seconds is not None else None
    while True:
        result = observe(directory)
        if result["status"] != "running" or deadline is not None and time.monotonic() >= deadline:
            return result
        time.sleep(0.2)


def main(args):
    if args.subcommand == "_operation-worker":
        worker(args.operation_dir)
        return 0
    result = launch(args) if args.subcommand == "start" else (
        resume(args.operation_dir, args.wait_seconds) if args.subcommand == "resume" else observe(args.operation_dir))
    print(bounded_json(result, record_path=Path(result.get("record_path", result["operation_path"])),
                       facts={"operation_id": result["operation_id"], "status": result["status"],
                              "issue_count": len(result["issues"])}, budget=args.max_output_bytes), end="")
    return 0 if result["status"] == "completed" else 3 if result["status"] == "running" else 1


def add_commands(commands):
    for name in ("start", "status", "resume", "_operation-worker"):
        parser = commands.add_parser(name, help={"start": "Launch once with durable identity and closeout",
            "status": "Observe an existing operation once", "resume": "Wait mechanically for the same operation",
            "_operation-worker": "Internal worker; never use to recover/retry"}[name])
        parser.add_argument("--operation-dir", required=True)
        parser.add_argument("--max-output-bytes", type=output_budget, default=8192)
        parser.set_defaults(handler=main)
        if name == "resume":
            parser.add_argument("--wait-seconds", type=float, help="Optional observer return interval; never kills work")
        if name == "start":
            parser.add_argument("--cwd")
            parser.add_argument("--bind-codex", action="store_true", help="Bind the shared native selector before detachment for provider commands")
            parser.add_argument("--quality-command", help="JSON argv for required validation; run once after exit zero")
            parser.add_argument("--timeout-seconds", type=float, help="Explicit command hard deadline; omitted has no kill timer")
            parser.add_argument("--validation-timeout-seconds", type=float, help="Separate explicit checker deadline")
            parser.add_argument("--stdin-file")
            parser.add_argument("--provider-root", action="append", default=[], help="Exact run/attempt scope for native accounting, repeatable")
            parser.add_argument("command", nargs="...")
