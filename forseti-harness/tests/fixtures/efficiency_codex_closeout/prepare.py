"""Prepare a synthetic completed-task comparison; never launch a model.

Use two intact Git checkouts. All six local checks must match the frozen
expectations before commands.json is published for a coordinator.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


CONTENT = ("saved start\n" + "x" * 7999 + "🙂Ω\nEND_SAVED_CONTENT\n").encode("utf-8")
EXPECTED = {
    "case-a": (0, "success", "passed", "complete", 36),
    "case-b": (0, "success", "passed", "unknown", 23),
    "case-c": (7, "failed", "failed", "complete", 36),
}
SCRIPT = Path(__file__).resolve()


def _digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _save(path, value):
    """Publish only complete, reread JSON; never overwrite an earlier observation."""
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=True, indent=2, allow_nan=False)
    if json.loads(temporary.read_text(encoding="utf-8")) != value:
        raise ValueError(f"saved JSON mismatch: {temporary}")
    temporary.rename(path)


def _git(root, *args):
    result = subprocess.run(["git", *args], cwd=root, capture_output=True,
                            encoding="utf-8", errors="replace", timeout=30)
    if result.returncode:
        raise ValueError(f"checkout inspection failed for {root}: {result.stderr.strip()}")
    return result.stdout


def _checkout(path):
    root = Path(path).resolve(strict=True)
    top = Path(_git(root, "rev-parse", "--show-toplevel").strip()).resolve()
    if top != root:
        raise ValueError(f"expected the complete checkout root, received {root}")
    if not (root / "forseti-harness/runners/run_efficiency.py").is_file():
        raise ValueError(f"measurement runner missing in {root}")
    return {"root": str(root), "revision": _git(root, "rev-parse", "HEAD").strip(),
            "harness_diff_sha256": _digest(_git(root, "diff", "--no-ext-diff", "HEAD",
                                                "--", "forseti-harness").encode("utf-8"))}


def _usage(inputs, responses=1):
    return {"input_tokens": inputs, "cached_input_tokens": 4 * responses,
            "cache_write_input_tokens": 0, "output_tokens": 3 * responses,
            "reasoning_output_tokens": responses, "total_tokens": inputs + 3 * responses}


def _examples(output):
    for case in EXPECTED:
        directory = output / "inputs" / case
        directory.mkdir(parents=True)
        rows = [
            {"type": "session_meta", "payload": {"id": case, "cli_version": "synthetic"}},
            {"type": "event_msg", "timestamp": "2026-09-12T00:00:00Z",
             "payload": {"type": "task_started", "turn_id": "turn"}},
            {"type": "turn_context", "payload": {"turn_id": "turn",
             "model": "synthetic-no-provider", "effort": "high"}},
            {"type": "token_usage_record", "payload": {"thread_id": case,
             "turn_id": "turn", "response_id": "response-1", "usage": _usage(10),
             "turn_token_usage": _usage(10)}},
            {"type": "token_usage_record", "payload": {"thread_id": case,
             "turn_id": "turn", "response_id": "response-2", "usage": _usage(20),
             "turn_token_usage": _usage(30, 2)}},
            {"type": "event_msg", "timestamp": "2026-09-12T00:00:02Z",
             "payload": {"type": "task_complete", "turn_id": "turn", "duration_ms": 2000}},
        ]
        if case == "case-b":
            del rows[3]
        (directory / "rollout.jsonl").write_text(
            "\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
        artifact = directory / "saved.txt"
        artifact.write_bytes(CONTENT if case != "case-c" else CONTENT.replace(b"xxx", b"", 1))
        _save(directory / "checker.json", [sys.executable, "-E", "-s", str(SCRIPT),
                                          "check", "--artifact", str(artifact)])


def _command(binding, arm, case, output, destination):
    directory = output / "inputs" / case
    return {"arm": arm, "case": case,
            "cwd": str(Path(binding["root"]) / "forseti-harness"),
            "argv": [sys.executable, "-E", "-s", "-m", "runners.run_efficiency", "import-codex",
                     "--sessions-dir", str(directory), "--thread-id", case, "--turn-id", "turn",
                     "--workflow", "synthetic-coordinator-closeout", "--workload-id", "saved-unicode-v1",
                     "--output-dir", str(output / destination / arm / case),
                     "--quality-command", str(directory / "checker.json"), "--cwd", str(directory),
                     "--timeout-seconds", "30"]}


def _exercise(command, output):
    """Run the actual module in its own checkout, with no cross-checkout imports."""
    process = subprocess.run(command["argv"], cwd=command["cwd"], capture_output=True,
                             encoding="utf-8", errors="replace", timeout=30)
    case, arm = command["case"], command["arm"]
    _save(output / f"{arm}-{case}-process.json",
          {"exit_code": process.returncode, "stdout": process.stdout, "stderr": process.stderr})
    try:
        returned = json.loads(process.stdout.strip().splitlines()[-1])
        record_path = Path(returned["record_path"])
        expected_dir = output / "preparation-records" / arm / case
        if record_path.resolve().parent != expected_dir.resolve():
            raise ValueError("runner returned a record outside its selected destination")
        record = json.loads(record_path.read_text(encoding="utf-8"))
        observed = (process.returncode, record["outcome"], record["quality"]["status"],
                    record["usage"]["coverage"], record["usage"]["total_tokens"])
        if observed != EXPECTED[case]:
            raise ValueError(f"expected {EXPECTED[case]}, observed {observed}")
        if (returned["outcome"], returned["quality"], returned["usage_coverage"]) != observed[1:4]:
            raise ValueError("command return disagrees with its saved record")
        if record["quality_return_code"] != (7 if case == "case-c" else 0):
            raise ValueError("wrong quality-check exit")
        if case == "case-b" and "turn_cumulative_reconciliation_failed" not in record["usage"]["issues"]:
            raise ValueError("missing usage failed for the wrong reason")
        if case == "case-c" and "saved_content_mismatch" not in process.stdout:
            raise ValueError("damaged content failed for the wrong reason")
        return {"arm": arm, "case": case, "exit_code": process.returncode,
                "record_path": str(record_path), "observed": list(observed)}
    except (ValueError, KeyError, IndexError, OSError) as exc:
        raise ValueError(f"{arm}/{case} preparation failed; inspect {arm}-{case}-process.json: {exc}") from exc


def prepare(baseline_root, candidate_root, output_dir):
    output = Path(output_dir).resolve()
    output.mkdir(parents=True, exist_ok=False)
    checks = []
    try:
        bindings = {"baseline": _checkout(baseline_root), "candidate": _checkout(candidate_root)}
        fixture_hash = _digest(SCRIPT.read_bytes())
        _examples(output)
        for arm, binding in bindings.items():
            for case in EXPECTED:
                checks.append(_exercise(_command(binding, arm, case, output, "preparation-records"), output))
        if bindings != {arm: _checkout(value["root"]) for arm, value in bindings.items()}:
            raise ValueError("checkout changed during preparation")
        if fixture_hash != _digest(SCRIPT.read_bytes()):
            raise ValueError("fixture changed during preparation")
        _save(output / "preparation.json", {"checks": checks, "synthetic": True})
        capsule = {"synthetic": True, "checkouts": bindings, "fixture_sha256": fixture_hash,
                   "instructions": "Execute these commands using each supplied cwd and argv. Preserve all exits. "
                   "Return the outcome, quality and accounting coverage for each case. These saved inputs "
                   "do not measure fresh model generation or subscription savings. Reuse only while the "
                   "fixture, inputs and relevant checkout state are unchanged. Use a new output directory "
                   "for a new observation; do not retry into existing record destinations.",
                   "commands": [_command(binding, arm, case, output, "worker-records")
                                for arm, binding in bindings.items() for case in EXPECTED]}
        _save(output / "commands.json", capsule)
        if json.loads((output / "commands.json").read_text(encoding="utf-8")) != capsule:
            raise ValueError("published command capsule differs from prepared commands")
        return {"status": "ready", "local_checks": len(checks), "model_calls": 0,
                "commands_path": str(output / "commands.json")}
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        _save(output / "failure.json", {"error": str(exc), "completed_checks": checks})
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    setup = sub.add_parser("prepare", help="Check both complete checkouts before publishing worker commands")
    setup.add_argument("--baseline-root", required=True)
    setup.add_argument("--candidate-root", required=True)
    setup.add_argument("--output-dir", required=True)
    check = sub.add_parser("check", help="Compare saved bytes with the frozen synthetic content")
    check.add_argument("--artifact", required=True)
    args = parser.parse_args(argv)
    try:
        if args.action == "check":
            if Path(args.artifact).read_bytes() != CONTENT:
                raise ValueError("saved_content_mismatch")
            print(json.dumps({"check": "saved_content", "status": "passed"}))
        else:
            print(json.dumps(prepare(args.baseline_root, args.candidate_root, args.output_dir)))
        return 0
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}))
        return 7 if args.action == "check" else 2


if __name__ == "__main__":
    raise SystemExit(main())
