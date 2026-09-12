"""Observe PR checks once; GitHub CLI owns polling. This command never merges."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
from uuid import uuid4

from reports.compact_return import bounded_json, output_budget, write_verified


def observe(*, repo: str, pr: int, head: str, output_dir: Path,
            timeout_seconds: float = 900, gh: str = "gh") -> tuple[dict, int]:
    if not re.fullmatch(r"[^/\s]+/[^/\s]+", repo) or pr <= 0:
        raise ValueError("supply an explicit OWNER/REPO and positive PR number")
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise ValueError("head must be the full expected commit SHA")
    if not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
        raise ValueError("timeout-seconds must be finite and positive")
    directory = output_dir.resolve() / str(uuid4())
    directory.mkdir(parents=True, exist_ok=False)
    result = {"repo": repo, "pr": pr, "expected_head": head, "status": "blocked",
              "issues": [], "commands": [], "checks": [], "counts": {}}

    def command(label: str, argv: list[str], timeout: float):
        out, err = directory / f"{label}.stdout", directory / f"{label}.stderr"
        observation = {"argv": [gh, *argv], "stdout_path": str(out), "stderr_path": str(err)}
        result["commands"].append(observation)
        with out.open("x", encoding="utf-8") as stdout, err.open("x", encoding="utf-8") as stderr:
            try:
                completed = subprocess.run([gh, *argv], stdout=stdout, stderr=stderr,
                                           timeout=timeout, check=False, shell=False)
                observation["exit_code"] = completed.returncode
            except subprocess.TimeoutExpired:
                observation["exit_code"] = 124
                observation["timed_out"] = True
            except OSError as exc:
                observation.update(exit_code=127, error=str(exc))
        return observation, out

    def snapshot(label: str, operation: str, fields: str):
        command_result, path = command(label, ["pr", operation, str(pr), "--repo", repo,
                                               "--json", fields], 30)
        try:
            value = json.loads(path.read_text(encoding="utf-8-sig"))
        except (ValueError, OSError):
            value = None
        return command_result["exit_code"], value

    rc, before = snapshot("before", "view", "headRefOid,state,url")
    result["before"] = before
    if rc or not isinstance(before, dict) or before.get("headRefOid") != head or before.get("state") != "OPEN":
        result["issues"].append("initial_open_pr_head_not_confirmed")
    else:
        watched, _ = command("watch", ["pr", "checks", str(pr), "--repo", repo,
                                      "--watch", "--fail-fast"], timeout_seconds)
        result["watch_exit_code"] = watched["exit_code"]
        rc, after = snapshot("after", "view", "headRefOid,state,url")
        result["after"] = after
        if rc or not isinstance(after, dict) or after.get("headRefOid") != head or after.get("state") != "OPEN":
            result["issues"].append("final_open_pr_head_not_confirmed")
        checks_rc, checks = snapshot("checks", "checks", "name,bucket,state,link,workflow")
        if checks_rc not in (0, 1, 8) or not isinstance(checks, list) or not checks:
            result["issues"].append("checks_not_observed")
        elif any(not isinstance(check, dict) or check.get("bucket") not in
                 {"pass", "fail", "pending", "skipping", "cancel"} for check in checks):
            result["issues"].append("unrecognized_check")
        else:
            result["checks"] = checks
            for check in checks:
                bucket = check["bucket"]
                result["counts"][bucket] = result["counts"].get(bucket, 0) + 1
        if watched.get("timed_out"):
            result["status"] = "timeout"
        elif result["counts"].get("fail") or result["counts"].get("cancel"):
            result["status"] = "failed"
        elif not result["issues"] and watched["exit_code"] == checks_rc == 0 and all(
                check["bucket"] == "pass" for check in result["checks"]):
            result["status"] = "passed"
        else:
            result["issues"].append("watch_or_checks_not_successful")
        # The identity check brackets the check snapshot as well as the watch.
        rc, final = snapshot("final", "view", "headRefOid,state,url")
        result["final"] = final
        if rc or not isinstance(final, dict) or final.get("headRefOid") != head or final.get("state") != "OPEN":
            result["issues"].append("check_snapshot_head_not_confirmed")
            result["status"] = "blocked"
    path = write_verified(result, directory / "observation.json")
    returned = {key: result[key] for key in ("repo", "pr", "expected_head", "status", "counts", "issues")}
    returned.update(record_path=str(path), record_readback_matched=True,
                    watch_exit_code=result.get("watch_exit_code"))
    return returned, 0 if result["status"] == "passed" else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr", required=True, type=int)
    parser.add_argument("--head", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--timeout-seconds", type=float, default=900)
    parser.add_argument("--max-output-bytes", type=output_budget, default=8192)
    args = parser.parse_args(argv)
    try:
        budget = args.max_output_bytes
        del args.max_output_bytes
        gh = shutil.which("gh")
        if gh is None:
            raise ValueError("GitHub CLI executable not found")
        result, code = observe(**vars(args), gh=gh)
        print(bounded_json(result, record_path=Path(result["record_path"]),
                           facts={"status": result["status"], "counts": result["counts"],
                                  "issue_count": len(result["issues"])}, budget=budget), end="")
        return code
    except (ValueError, OSError) as exc:
        print(f"CI observation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
