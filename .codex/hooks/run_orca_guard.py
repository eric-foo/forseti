#!/usr/bin/env python3
"""Run Orca's current protected-action guard from origin/main.

This local Codex hook wrapper avoids coupling guard behavior to a stale or dirty
worktree branch. It reads the Codex hook event from stdin, loads the guard script
from the local origin/main ref, and translates guard denials into Codex's
PreToolUse JSON deny shape.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
GUARD_PATH = ".agents/hooks/guard_protected_actions.py"


def _load_guard_source():
    shown = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"origin/main:{GUARD_PATH}"],
        capture_output=True,
        text=True,
        timeout=5,
    )
    if shown.returncode == 0 and shown.stdout:
        return shown.stdout
    fallback = ROOT / GUARD_PATH
    return fallback.read_text(encoding="utf-8")


def _deny(reason):
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
    )
    sys.stdout.write("\n")
    return 0


def main():
    try:
        guard_source = _load_guard_source()
    except Exception as exc:
        return _deny(f"run_orca_guard: could not load guard: {exc}")

    event = sys.stdin.read()
    proc = subprocess.run(
        [sys.executable, "-c", guard_source, *sys.argv[1:]],
        input=event,
        text=True,
        capture_output=True,
    )
    if proc.returncode == 2:
        reason = proc.stderr.strip() or proc.stdout.strip() or "Blocked by Orca protected-action guard."
        return _deny(reason)
    if proc.stdout:
        sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
