"""Run the existing finite command and its commissioned report once, without a model executor."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from reports.compact_return import write_verified
from reports.finite_closeout_judgment import judge, REASONING_EFFORTS


def argument_parser():
    parser = argparse.ArgumentParser(description=__doc__, epilog=(
        "For interrupted observation, wrap this command once with run_efficiency start --bind-codex; "
        "use its returned resume argv. Neither repeated start nor report-dir reuse relaunches work."))
    parser.add_argument("--report-dir", required=True, type=Path, help="New directory outside run/provider roots")
    parser.add_argument("--model", required=True)
    parser.add_argument("--reasoning-effort", required=True, choices=REASONING_EFFORTS)
    parser.add_argument("--timeout-seconds", required=True, type=float, help="Reporting attempt deadline only")
    parser.add_argument("finite_args", nargs=argparse.REMAINDER, help="-- followed by the existing finite execution arguments")
    return parser


def main(argv=None):
    args = argument_parser().parse_args(argv)
    finite_args = args.finite_args[1:] if args.finite_args[:1] == ["--"] else args.finite_args
    output = args.report_dir.resolve()
    try:
        from runners.run_finite_semantic_consolidation import argument_parser as finite_argument_parser
        finite = finite_argument_parser().parse_args(finite_args)
        if finite.replay_from:
            raise ValueError("run-and-report requires live execution; replay is not fresh report evidence")
        if any(output.is_relative_to(p.resolve()) for p in (finite.output_dir, finite.provider_root or finite.output_dir)):
            raise ValueError("report directory must be outside run/provider roots")
        from command_execution import positive
        positive(args.timeout_seconds)
        output.mkdir(parents=True, exist_ok=False)
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "FINITE_RUN_REPORT_REFUSED", "error": str(exc)}))
        return 1
    command = [sys.executable, "-m", "runners.run_finite_semantic_consolidation", *finite_args]
    result = {"status": "FINITE_RUN_REPORT_FAILED_OR_UNKNOWN", "command": command,
        "execution_exit_code": None, "reporting_status": "not_started", "judgment_result": None,
        "stdout_path": str(output / "execution.stdout"), "stderr_path": str(output / "execution.stderr")}
    try:
        write_verified({"command": command, "run_root": str(finite.output_dir.resolve())}, output / "execution-intent.json")
        with (output / "execution.stdout").open("xb") as stdout, (output / "execution.stderr").open("xb") as stderr:
            process = subprocess.run(command, cwd=Path(__file__).resolve().parents[1], stdout=stdout, stderr=stderr,
                check=False, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        result["execution_exit_code"] = process.returncode
        write_verified({"exit_code": process.returncode}, output / "execution.json")
        # Consume the actual finite entry's final record, never guess the newest
        # failure or turn an old result file into this invocation's success.
        lines = (output / "execution.stdout").read_text(encoding="utf-8").splitlines()
        terminal = json.loads(lines[-1])
        result["execution_terminal"] = terminal
        failure = terminal.get("failure") if process.returncode else None
        if process.returncode and not failure:
            raise ValueError("failed execution did not provide a saved failure record; inspect execution logs")
        if not process.returncode and terminal.get("result") != str(finite.output_dir / "result.json"):
            raise ValueError("execution did not provide its expected finite endpoint")
        result["reporting_status"] = "started"
        report = judge(finite.output_dir, None, output / "judgment", model=args.model,
            reasoning_effort=args.reasoning_effort, timeout_seconds=args.timeout_seconds, failure_record=failure,
            codex_executable=finite.codex_executable)
        result.update(reporting_status=report["status"], judgment_result=str(output / "judgment/result.json"),
                      report_path=report["report_path"], saved_status=report["saved_status"],
                      saved_answer_correction_status=report["saved_answer_correction_status"])
        if not process.returncode and report["status"] == "FINITE_CLOSEOUT_JUDGMENT_COMPLETE_REQUIRES_ADJUDICATION":
            result["status"] = "FINITE_RUN_REPORT_COMPLETE_REQUIRES_ADJUDICATION"
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        result.update(reporting_status="failed_or_unknown", error=str(exc))
    write_verified(result, output / "result.json")
    print(json.dumps(result, ensure_ascii=True))
    return result["execution_exit_code"] or (0 if result["status"] == "FINITE_RUN_REPORT_COMPLETE_REQUIRES_ADJUDICATION" else 1)
