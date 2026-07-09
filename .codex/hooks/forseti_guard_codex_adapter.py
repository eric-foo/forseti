#!/usr/bin/env python3
"""Codex adapter for Forseti's protected-action guard.

Codex PreToolUse hooks can deny tool calls by returning a JSON
`permissionDecision: deny`. Forseti's portable guard predates that Codex-specific
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
WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
SHELL_TOOLS = {"Bash", "PowerShell"}
DURABLE_EXT = r"(?:md|py|ya?ml|json|toml|ps1)"
DURABLE_PATH = re.compile(r"[A-Za-z0-9_./\\:-]+\." + DURABLE_EXT + r"\b", re.I)
SHELL_WRITE_PRIMITIVE = re.compile(
    r"\[System\.IO\.File\]::(?:WriteAllText|WriteAllLines|AppendAllText|AppendAllLines)\b"
    r"|\b(?:Set-Content|Add-Content|Out-File)\b"
    r"|\b(?:write_text|write_bytes)\s*\("
    r"|\bopen\s*\([^)]*,\s*['\"][^'\"]*[wax+]"
    r"|\bopen\s*\([^)]*\bmode\s*=\s*['\"][^'\"]*[wax+]",
    re.I,
)
REDIRECT_DURABLE = re.compile(
    r"(?:^|[^>])>>?\s*['\"]?[^'\"\s|&;>]+\." + DURABLE_EXT + r"\b", re.I
)


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
    return proc.stderr.strip() or proc.stdout.strip() or "Blocked by Forseti protected-action guard."


def _path_for_guard(path_text):
    path = pathlib.Path(path_text.strip())
    if path.is_absolute():
        return str(path)
    return str(ROOT / path)


def _norm_path(path):
    try:
        resolved = pathlib.Path(path).resolve()
    except OSError:
        resolved = pathlib.Path(path).absolute()
    return str(resolved).replace("\\", "/").lower().rstrip("/")


def _contains_path(parent, child):
    parent = parent.rstrip("/")
    child = child.rstrip("/")
    return child == parent or child.startswith(parent + "/")


def _registered_worktree_roots():
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "worktree", "list", "--porcelain"],
            text=True,
            capture_output=True,
            timeout=4,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return []
    if out.returncode != 0:
        return []
    roots = []
    for line in out.stdout.splitlines():
        if line.startswith("worktree "):
            roots.append(_norm_path(line[len("worktree "):].strip()))
    return roots


def _nested_worktree_reason(path_text, roots=None):
    target = _norm_path(path_text)
    current = _norm_path(ROOT)
    roots = roots if roots is not None else _registered_worktree_roots()
    for root in roots:
        if root == current:
            continue
        if _contains_path(root, target):
            return (
                "Codex nested-worktree write blocked: target is under registered "
                "worktree %s while this hook is rooted at %s. Open/reroot Codex "
                "in the target worktree and rerun the lane-start writeability "
                "preflight before editing."
            ) % (root, current)
    return ""


def _check_direct_write_path(tool_input):
    target = (
        tool_input.get("file_path")
        or tool_input.get("notebook_path")
        or tool_input.get("path")
    )
    if not target:
        return ""
    return _nested_worktree_reason(_path_for_guard(target))


def _check_shell_durable_write(tool_input):
    command = tool_input.get("command") or ""
    if not command:
        return ""
    if not (REDIRECT_DURABLE.search(command) or SHELL_WRITE_PRIMITIVE.search(command)):
        return ""
    if not DURABLE_PATH.search(command):
        return ""
    return (
        "Codex raw shell durable-write blocked: use apply_patch from the active "
        "worktree. If apply_patch fails against a nested worktree, reroot Codex "
        "in that worktree instead of rewriting repo files through Bash/PowerShell."
    )


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
        reason = _nested_worktree_reason(_path_for_guard(path))
        if reason:
            return reason
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

    ps_write = subprocess.run(
        [sys.executable, str(pathlib.Path(__file__))],
        input=json.dumps(
            {
                "tool_name": "PowerShell",
                "tool_input": {
                    "command": "[System.IO.File]::WriteAllText('docs/x.md', 'bad')"
                },
            }
        ),
        text=True,
        capture_output=True,
    )
    try:
        denial = json.loads(ps_write.stdout)
        ok = ok and ps_write.returncode == 0
        ok = ok and denial["hookSpecificOutput"]["permissionDecision"] == "deny"
    except Exception:
        ok = False

    set_content = subprocess.run(
        [sys.executable, str(pathlib.Path(__file__))],
        input=json.dumps(
            {
                "tool_name": "PowerShell",
                "tool_input": {"command": "Set-Content docs/x.md 'bad'"},
            }
        ),
        text=True,
        capture_output=True,
    )
    try:
        denial = json.loads(set_content.stdout)
        ok = ok and set_content.returncode == 0
        ok = ok and denial["hookSpecificOutput"]["permissionDecision"] == "deny"
    except Exception:
        ok = False

    redirect = subprocess.run(
        [sys.executable, str(pathlib.Path(__file__))],
        input=json.dumps(
            {
                "tool_name": "Bash",
                "tool_input": {"command": "echo bad > docs/x.md"},
            }
        ),
        text=True,
        capture_output=True,
    )
    try:
        denial = json.loads(redirect.stdout)
        ok = ok and redirect.returncode == 0
        ok = ok and denial["hookSpecificOutput"]["permissionDecision"] == "deny"
    except Exception:
        ok = False

    redirect_no_space = subprocess.run(
        [sys.executable, str(pathlib.Path(__file__))],
        input=json.dumps(
            {
                "tool_name": "Bash",
                "tool_input": {"command": "echo bad>docs/x.md"},
            }
        ),
        text=True,
        capture_output=True,
    )
    try:
        denial = json.loads(redirect_no_space.stdout)
        ok = ok and redirect_no_space.returncode == 0
        ok = ok and denial["hookSpecificOutput"]["permissionDecision"] == "deny"
    except Exception:
        ok = False

    py_open_read = subprocess.run(
        [sys.executable, str(pathlib.Path(__file__))],
        input=json.dumps(
            {
                "tool_name": "Bash",
                "tool_input": {"command": "python -c \"open('docs/x.md').read()\""},
            }
        ),
        text=True,
        capture_output=True,
    )
    ok = ok and py_open_read.returncode == 0 and not py_open_read.stdout.strip()

    py_open_write = subprocess.run(
        [sys.executable, str(pathlib.Path(__file__))],
        input=json.dumps(
            {
                "tool_name": "Bash",
                "tool_input": {"command": "python -c \"open('docs/x.md', 'w').write('bad')\""},
            }
        ),
        text=True,
        capture_output=True,
    )
    try:
        denial = json.loads(py_open_write.stdout)
        ok = ok and py_open_write.returncode == 0
        ok = ok and denial["hookSpecificOutput"]["permissionDecision"] == "deny"
    except Exception:
        ok = False

    current_root = _norm_path(ROOT)
    fake_other = current_root + "/worktrees/other-lane"
    fake_roots = [
        current_root,
        fake_other,
        current_root + "/.codex/worktrees/another-lane",
    ]
    ok = ok and bool(
        _nested_worktree_reason(
            fake_other + "/docs/x.md",
            roots=fake_roots,
        )
    )
    ok = ok and not _nested_worktree_reason(current_root + "/docs/x.md", roots=fake_roots)

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
    elif event.get("tool_name") in WRITE_TOOLS:
        reason = _check_direct_write_path(event.get("tool_input") or {})
        if reason:
            return _deny(reason)
    elif event.get("tool_name") in SHELL_TOOLS:
        reason = _check_shell_durable_write(event.get("tool_input") or {})
        if reason:
            return _deny(reason)

    return _run_guard_event(event_text)


if __name__ == "__main__":
    sys.exit(main())
