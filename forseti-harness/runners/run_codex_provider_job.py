#!/usr/bin/env python3
"""Resume one subscription-only provider job with a finite shared retry budget."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HARNESS_ROOT = Path(__file__).resolve().parents[1]
if str(HARNESS_ROOT) not in sys.path:
    sys.path.insert(0, str(HARNESS_ROOT))
from harness_utils import hash_file
from provider_jobs import _new, run_provider_job
from runners.run_codex_provider_attempt import REASONING_EFFORTS, preloaded_context, select_codex_executable


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("job-dir", "attempt-root", "retry-budget-dir", "prompt-file", "output-schema", "worktree"):
        parser.add_argument("--"+name, type=Path, required=True)
    parser.add_argument("--codex-executable", type=Path,
                        help="Explicit native override; default verifies Desktop ancestry once, then reuses the job binding")
    parser.add_argument("--model", required=True)
    parser.add_argument("--reasoning-effort", choices=REASONING_EFFORTS, required=True,
                        help="Explicit task-assessed effort supported by the selected model; no default")
    parser.add_argument("--timeout-seconds", type=float, required=True)
    parser.add_argument("--run-retry-limit", type=int, required=True)
    parser.add_argument("--max-retries", type=int, default=1)
    parser.add_argument("--retry-delay-seconds", type=float, default=10)
    parser.add_argument("--result-out", type=Path,
                        help="New JSON result file for callers; stdout also contains attempt receipts")
    parser.add_argument("--completed-recovery", type=Path,
                        help="Explicit completed identical repeat of a stopped read-only timeout; consumes one retry")
    parser.add_argument("--preload-context", type=Path, action="append", default=[],
                        help="Required context supplied verbatim with shell_tool disabled; repeat per file")
    args = parser.parse_args()
    if args.result_out is not None and args.result_out.exists():
        parser.error("refusing to replace provider result output")
    native = HARNESS_ROOT / "runners/run_codex_provider_attempt.py"
    try:
        saved_path = args.job_dir / "binding.json"
        saved = json.loads(saved_path.read_text(encoding="utf-8"))["binding"] if saved_path.exists() else None
        override = args.codex_executable
        if saved:
            if override is not None and str(override.resolve()) != saved["codex_executable"]:
                raise ValueError("explicit executable differs from the bound provider job")
            override = Path(saved["codex_executable"])
            if hash_file(override) != saved["codex_sha256"]:
                raise ValueError("bound Codex executable changed; no automatic rebind")
        selected = select_codex_executable(override)
        binding = dict(prompt_path=str(args.prompt_file.resolve(strict=True)), prompt_sha256=hash_file(args.prompt_file),
            schema_path=str(args.output_schema.resolve(strict=True)), schema_sha256=hash_file(args.output_schema),
            model=args.model, reasoning_effort=args.reasoning_effort, timeout_seconds=args.timeout_seconds,
            worktree=str(args.worktree.resolve(strict=True)), codex_executable=selected["path"],
            codex_sha256=selected["sha256"], runner_path=str(native),runner_sha256=hash_file(native))
        if saved is None or "codex_version" in saved:
            binding["codex_version"] = selected["version"]
        context, context_files = preloaded_context(args.preload_context)
        if context:
            binding["preloaded_context_sha256"] = hashlib.sha256(context.encode("utf-8")).hexdigest()
            binding["preloaded_context_files"] = context_files
        def launch(aid):
            command = [sys.executable, str(native), "--attempt-root", str(args.attempt_root), "--attempt-id", aid,
                "--prompt-file", binding["prompt_path"], "--output-schema", binding["schema_path"],
                "--worktree", binding["worktree"], "--codex-executable", binding["codex_executable"],
                "--model", args.model, "--reasoning-effort", binding["reasoning_effort"], "--require-chatgpt",
                "--timeout-seconds", str(args.timeout_seconds)]
            if context:
                command += ["--expected-context-sha256", binding["preloaded_context_sha256"]]
                for record in context_files:
                    command += ["--preload-context", record["path"]]
            subprocess.run(command, check=False)
        result = run_provider_job(job_dir=args.job_dir, attempt_root=args.attempt_root, binding=binding,
            launch=launch, retry_budget_dir=args.retry_budget_dir, run_retry_limit=args.run_retry_limit,
            max_retries=args.max_retries, retry_delay_seconds=args.retry_delay_seconds,
            completed_recovery=args.completed_recovery)
        if args.result_out is not None:
            _new(args.result_out, result)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    # Context can contain BOMs or text outside a Windows redirected console's
    # encoding. JSON escapes preserve it without failing after model completion.
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result["status"] == "PROCESS_COMPLETED_NOT_VALIDATED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
