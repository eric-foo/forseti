#!/usr/bin/env python3
"""Stop hook — warn when a commit-once-whole shared file is left dirty (advisory).

WHAT THIS DOES
  At the end of a turn (a Stop event), warns if any of the three shared,
  interleaved "commit once, whole" files is left uncommitted. Those files are
  edited by every lane, so a dirty one blocks others from cleanly committing
  their own one-line edit (committing it would sweep the dirty pile into an
  unrelated commit). This is the turn-end backstop to the per-edit PostToolUse
  repo-map commit interrupt in check_repo_map_freshness.py.

  The three shared files:
    - docs/workflows/orca_repo_map_v0.md
    - .claude/settings.json
    - .agents/workflow-overlay/source-of-truth.md

WHY (enforcement placement)
  "Commit the shared file immediately" was carried only by instruction. This is
  the substrate backstop, per the Enforcement Placement principle in
  .agents/workflow-overlay/validation-gates.md. Complementary to the per-edit
  PostToolUse interrupt (map-specific) — this one is turn-end and covers all
  three.

HARD BOUNDARY — warn only, never block, never auto-commit.
  Exit 0 always. It returns a reminder via `additionalContext`; it does NOT
  exit 2 (which would block the Stop and force the agent to continue), and it
  does NOT commit anything (auto-commit on a shared branch is unsafe). It guards
  `stop_hook_active` to avoid any stop-loop, and fails OPEN on internal error.

MODES
  check_shared_files_dirty.py --hook       Stop hook (stdin JSON, exit 0)
  check_shared_files_dirty.py --check       human-readable check of the live tree
  check_shared_files_dirty.py --selftest    pure-decision cases

REGISTRATION (.claude/settings.json; Stop takes NO matcher)
  "Stop": [ { "hooks": [ { "type": "command",
              "command": "python .agents/hooks/check_shared_files_dirty.py --hook",
              "timeout": 10 } ] } ]
  Hooks load at session start; restart the session after editing settings.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

# The three commit-once-whole shared files (repo-relative POSIX).
SHARED = (
    "docs/workflows/orca_repo_map_v0.md",
    ".claude/settings.json",
    ".agents/workflow-overlay/source-of-truth.md",
)


def repo_root() -> Path:
    """Repo root, derived from this file's location (.agents/hooks/<this>)."""
    return Path(__file__).resolve().parents[2]


def dirty_shared(porcelain: str) -> list[str]:
    """Given `git status --porcelain` output, return which SHARED files are dirty.

    Pure function (testable). Porcelain v1: 2-char status, a space, then the path
    (rename shown as 'old -> new'). Paths use forward slashes, matching SHARED."""
    out: list[str] = []
    for line in porcelain.splitlines():
        if len(line) < 4:
            continue
        path = line[3:]
        if " -> " in path:  # rename: take the destination
            path = path.split(" -> ", 1)[1]
        path = path.strip().strip('"')
        if path in SHARED and path not in out:
            out.append(path)
    return out


def git_porcelain(root: Path) -> str:
    """`git status --porcelain` scoped to the three shared files ('' on failure)."""
    try:
        res = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain", "--", *SHARED],
            capture_output=True, text=True)
    except (FileNotFoundError, OSError):
        return ""
    return res.stdout if res.returncode == 0 else ""


def reminder_text(dirty: list[str]) -> str:
    return (
        "Commit-once-whole shared file(s) left dirty at end of turn: "
        + ", ".join(dirty)
        + ". Each interleaves every lane's edits, so leaving one dirty blocks "
        "other lanes from cleanly committing their own edit. Commit each one now, "
        "explicit-path, e.g. `git commit --only -- " + dirty[0] + "`. "
        "Advisory only - not blocking, and never auto-committed on a shared branch."
    )


def run_stop_hook(root: Path) -> int:
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        data = {}
    if isinstance(data, dict) and data.get("stop_hook_active") is True:
        return 0  # already in a stop-hook iteration; never loop
    dirty = dirty_shared(git_porcelain(root))
    if dirty:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "Stop", "additionalContext": reminder_text(dirty)}}))
    return 0


def run_check(root: Path) -> int:
    dirty = dirty_shared(git_porcelain(root))
    if dirty:
        print("DIRTY shared files: " + ", ".join(dirty))
        print(reminder_text(dirty))
    else:
        print("clean: no commit-once-whole shared file is dirty")
    return 0


def selftest() -> int:
    rm = "docs/workflows/orca_repo_map_v0.md"
    st = ".agents/workflow-overlay/source-of-truth.md"
    sj = ".claude/settings.json"
    cases = [
        ("", []),
        (" M %s\n" % rm, [rm]),
        ("?? %s\n M docs/other.md\n" % sj, [sj]),
        (" M %s\n M %s\n" % (st, rm), [st, rm]),
        (" M docs/decisions/x_v0.md\n", []),            # non-shared dirty -> silent
        ("R  old.md -> %s\n" % rm, [rm]),               # rename destination
        ("xx\n", []),                                   # junk line ignored
    ]
    ok = True
    for i, (porc, expect) in enumerate(cases, 1):
        got = dirty_shared(porc)
        status = "PASS" if got == expect else "FAIL"
        if got != expect:
            ok = False
        print("%s case %02d  expect=%s got=%s" % (status, i, expect, got))
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    root = repo_root()
    if "--check" in argv:
        return run_check(root)
    return run_stop_hook(root)  # default / --hook: Stop hook mode


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # fail OPEN: a reminder bug must never block a stop
        sys.stderr.write("check_shared_files_dirty: internal error, allowing: %s\n" % exc)
        sys.exit(0)
