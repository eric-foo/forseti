#!/usr/bin/env python3
"""SessionStart hook: emit one honest, low-latency lane-state read.

The capsule runs exactly one read-only Git child process:

    git --no-optional-locks status --porcelain=v2 --branch

It reports only the repository root, branch, and modified/untracked counts.
Git failure or timeout is represented as UNKNOWN, never as a clean tree.
The hook is advisory and always fails open; the host registration supplies the
5-second hard cap and this child process has a 2-second internal timeout.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hooklib import repo_root  # noqa: E402

GIT_TIMEOUT_SECONDS = 2


def parse_status(output: str) -> tuple[str, int, int]:
    """Parse porcelain-v2 branch status into branch/modified/untracked."""
    branch = "UNKNOWN"
    modified = untracked = 0
    for line in output.splitlines():
        if line.startswith("# branch.head "):
            value = line.removeprefix("# branch.head ").strip()
            branch = "DETACHED" if value == "(detached)" else (value or "UNKNOWN")
        elif line.startswith("? "):
            untracked += 1
        elif line.startswith(("1 ", "2 ", "u ")):
            modified += 1
    return branch, modified, untracked


def read_status(root: Path) -> str | None:
    """Run the capsule's only child process; return None on any Git failure."""
    command = [
        "git",
        "--no-optional-locks",
        "-C",
        str(root),
        "status",
        "--porcelain=v2",
        "--branch",
    ]
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT_SECONDS,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout if result.returncode == 0 else None


def build_capsule(root: Path, status_output: str | None) -> str:
    lines = [f"repo: {root}"]
    if status_output is None:
        lines.extend(("branch: UNKNOWN", "tree: UNKNOWN"))
    else:
        branch, modified, untracked = parse_status(status_output)
        lines.extend(
            (f"branch: {branch}", f"tree: {modified} modified, {untracked} untracked")
        )
    return "\n".join(lines)


def gather(root: Path) -> str:
    return build_capsule(root, read_status(root))


def selftest() -> int:
    sample = "\n".join(
        (
            "# branch.oid 0123456789abcdef",
            "# branch.head feature-x",
            "1 .M N... 100644 100644 100644 abc def tracked.md",
            "2 R. N... 100644 100644 100644 abc def R100 renamed.md\told.md",
            "u UU N... 100644 100644 100644 100644 abc def ghi conflict.md",
            "? new.md",
        )
    )
    success = build_capsule(Path("repo"), sample)
    failure = build_capsule(Path("repo"), None)
    ok = (
        parse_status(sample) == ("feature-x", 3, 1)
        and success.splitlines()
        == ["repo: repo", "branch: feature-x", "tree: 3 modified, 1 untracked"]
        and failure.splitlines()
        == ["repo: repo", "branch: UNKNOWN", "tree: UNKNOWN"]
        and "0 modified" not in failure
    )
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    print(gather(repo_root()))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # fail open: a capsule bug must not block session start
        sys.stderr.write(f"session_context_capsule: internal error, allowing: {exc}\n")
        sys.exit(0)
