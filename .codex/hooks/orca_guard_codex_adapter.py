#!/usr/bin/env python3
"""Codex adapter for Orca's protected-action guard.

Codex PreToolUse hooks can deny tool calls by returning a JSON
`permissionDecision: deny`. Orca's portable guard predates that Codex-specific
shape and uses `exit 2` plus stderr. This adapter preserves the existing guard
logic while translating blocked decisions into Codex's native denial response.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
GUARD = ROOT / ".agents" / "hooks" / "guard_protected_actions.py"
PATCH_PATH = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$")
PATCH_MOVE = re.compile(r"^\*\*\* Move to: (.+)$")


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


def _run_guard(event):
    return subprocess.run(
        [sys.executable, str(GUARD)],
        input=event,
        text=True,
        capture_output=True,
        timeout=8,
    )


def _reason_from(proc):
    return proc.stderr.strip() or proc.stdout.strip() or "Blocked by Orca protected-action guard."


def _path_for_guard(path_text):
    path = pathlib.Path(path_text.strip())
    if path.is_absolute():
        return str(path)
    return str(ROOT / path)


def _apply_patch_paths(patch_text):
    paths = []
    for line in patch_text.splitlines():
        match = PATCH_PATH.match(line) or PATCH_MOVE.match(line)
        if match:
            paths.append(_path_for_guard(match.group(1)))
    return paths


def _check_apply_patch_paths(tool_input):
    patch_text = tool_input.get("command") or ""
    for path in _apply_patch_paths(patch_text):
        event = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": path}})
        proc = _run_guard(event)
        if proc.returncode == 2:
            return _reason_from(proc)
        if proc.returncode != 0:
            return _reason_from(proc)
    return ""


def _run_guard_event(event_text):
    proc = _run_guard(event_text)
    if proc.returncode == 2:
        return _deny(_reason_from(proc))
    if proc.returncode != 0:
        return _deny(_reason_from(proc))
    if proc.stdout:
        sys.stdout.write(proc.stdout)
    if proc.stderr:
        sys.stderr.write(proc.stderr)
    return 0


def _selftest():
    ok = True
    guard = subprocess.run([sys.executable, str(GUARD), "--selftest"], text=True)
    ok = ok and guard.returncode == 0

    blocked = subprocess.run(
        [sys.executable, str(pathlib.Path(__file__))],
        input=json.dumps({"tool_name": "Bash", "tool_input": {"command": "git clean -n"}}),
        text=True,
        capture_output=True,
    )
    try:
        denial = json.loads(blocked.stdout)
        ok = ok and blocked.returncode == 0
        ok = ok and denial["hookSpecificOutput"]["permissionDecision"] == "deny"
    except Exception:
        ok = False

    protected = pathlib.Path.home() / "Desktop" / "projects" / "jb" / "x.md"
    patch_event = {
        "tool_name": "apply_patch",
        "tool_input": {
            "command": (
                "*** Begin Patch\n"
                f"*** Update File: {protected}\n"
                "@@\n"
                "-old\n"
                "+new\n"
                "*** End Patch\n"
            )
        },
    }
    patch = subprocess.run(
        [sys.executable, str(pathlib.Path(__file__))],
        input=json.dumps(patch_event),
        text=True,
        capture_output=True,
    )
    try:
        denial = json.loads(patch.stdout)
        ok = ok and patch.returncode == 0
        ok = ok and denial["hookSpecificOutput"]["permissionDecision"] == "deny"
    except Exception:
        ok = False

    allowed = subprocess.run(
        [sys.executable, str(pathlib.Path(__file__))],
        input=json.dumps({"tool_name": "Bash", "tool_input": {"command": "git status --short"}}),
        text=True,
        capture_output=True,
    )
    ok = ok and allowed.returncode == 0 and not allowed.stdout.strip()

    print("CODEX ADAPTER SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main():
    if "--selftest" in sys.argv:
        return _selftest()

    event_text = sys.stdin.read()
    try:
        event = json.loads(event_text)
    except Exception:
        return _run_guard_event(event_text)

    if event.get("tool_name") == "apply_patch":
        reason = _check_apply_patch_paths(event.get("tool_input") or {})
        if reason:
            return _deny(reason)

    return _run_guard_event(event_text)


if __name__ == "__main__":
    sys.exit(main())
