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
HOOK_ADOPTION_CANARY_ARG = "--live-adoption-probe"
HOOK_ADOPTION_ADOPTED = "FORSETI_CODEX_HOOK_ADOPTION=ADOPTED"
HOOK_ADOPTION_NOT_INTERCEPTED = "FORSETI_CODEX_HOOK_ADOPTION=NOT_INTERCEPTED"
HOOK_ADOPTION_CANARY_COMMAND = re.compile(
    r"\s*python(?:\.exe)?\s+['\"]?(?:\.\\|\./)?\.codex[\\/]hooks[\\/]"
    r"forseti_guard_codex_adapter\.py['\"]?\s+--live-adoption-probe\s*",
    re.I,
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


def _is_hook_adoption_canary(tool_input):
    command = tool_input.get("command") or ""
    return bool(HOOK_ADOPTION_CANARY_COMMAND.fullmatch(command))


def _not_intercepted():
    print(HOOK_ADOPTION_NOT_INTERCEPTED, file=sys.stderr)
    return 3


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


def _check_shell_durable_write(tool_input):
    command = tool_input.get("command") or ""
    if not command:
        return ""
    if not (REDIRECT_DURABLE.search(command) or SHELL_WRITE_PRIMITIVE.search(command)):
        return ""
    if not DURABLE_PATH.search(command):
        return ""
    return (
        "Codex raw shell durable-write blocked: use apply_patch so every edited "
        "path is checked by the Forseti protected-action guard."
    )


def _apply_patch_paths(patch_text):
    paths = []
    for line in patch_text.splitlines():
        match = PATCH_PATH.match(line) or PATCH_MOVE.match(line)
        if match:
            paths.append(_path_for_guard(match.group(1)))
    return paths


def _check_apply_patch_paths(tool_input):
    seen = set()
    for key in ("command", "patch", "input"):
        patch_text = tool_input.get(key)
        if not isinstance(patch_text, str) or not patch_text:
            continue
        for path in _apply_patch_paths(patch_text):
            if path in seen:
                continue
            seen.add(path)
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
    failures = []

    def _run_adapter(event):
        return subprocess.run(
            [sys.executable, str(pathlib.Path(__file__))],
            input=json.dumps(event),
            text=True,
            capture_output=True,
        )

    def _shell_event(tool_name, command):
        return {"tool_name": tool_name, "tool_input": {"command": command}}

    def _expect_denied(name, event, *, reason=None):
        # Fail-safe: an unexpected exception (no JSON, missing keys) records a
        # named failure instead of being silently swallowed.
        proc = _run_adapter(event)
        try:
            output = json.loads(proc.stdout)["hookSpecificOutput"]
            decision = output["permissionDecision"]
            got_reason = output["permissionDecisionReason"]
        except Exception as exc:
            failures.append(f"{name}: no denial JSON ({type(exc).__name__}: {exc})")
            return
        if proc.returncode != 0:
            failures.append(f"{name}: exit {proc.returncode}, expected 0")
        elif decision != "deny":
            failures.append(f"{name}: permissionDecision {decision!r}, expected 'deny'")
        elif reason is not None and got_reason != reason:
            failures.append(f"{name}: unexpected denial reason {got_reason!r}")

    def _expect_allowed(name, event):
        proc = _run_adapter(event)
        if proc.returncode != 0 or proc.stdout.strip():
            failures.append(
                f"{name}: expected silent allow "
                f"(exit {proc.returncode}, stdout {proc.stdout.strip()!r})"
            )

    guard = subprocess.run([sys.executable, str(GUARD), "--selftest"], text=True)
    if guard.returncode != 0:
        failures.append(f"guard --selftest: exit {guard.returncode}, expected 0")

    direct_canary = subprocess.run(
        [sys.executable, str(pathlib.Path(__file__)), HOOK_ADOPTION_CANARY_ARG],
        text=True,
        capture_output=True,
    )
    if direct_canary.returncode != 3:
        failures.append(f"direct canary: exit {direct_canary.returncode}, expected 3")
    if direct_canary.stderr.strip() != HOOK_ADOPTION_NOT_INTERCEPTED:
        failures.append("direct canary: NOT_INTERCEPTED marker missing on stderr")

    _expect_denied(
        "hooked canary",
        _shell_event(
            "PowerShell",
            "python .codex/hooks/forseti_guard_codex_adapter.py "
            f"{HOOK_ADOPTION_CANARY_ARG}",
        ),
        reason=HOOK_ADOPTION_ADOPTED,
    )

    _expect_allowed(
        "chained canary",
        _shell_event(
            "PowerShell",
            "python .codex/hooks/forseti_guard_codex_adapter.py "
            f"{HOOK_ADOPTION_CANARY_ARG}; git status --short",
        ),
    )

    _expect_denied("git clean", _shell_event("Bash", "git clean -n"))

    protected = pathlib.Path.home() / "Desktop" / "projects" / "jb" / "x.md"
    _expect_denied(
        "apply_patch protected path",
        {
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
        },
    )

    _expect_allowed("git status", _shell_event("Bash", "git status --short"))

    _expect_denied(
        "powershell WriteAllText",
        _shell_event("PowerShell", "[System.IO.File]::WriteAllText('docs/x.md', 'bad')"),
    )
    _expect_denied(
        "powershell Set-Content",
        _shell_event("PowerShell", "Set-Content docs/x.md 'bad'"),
    )
    _expect_denied("shell redirect", _shell_event("Bash", "echo bad > docs/x.md"))
    _expect_denied(
        "shell redirect no space", _shell_event("Bash", "echo bad>docs/x.md")
    )
    _expect_allowed(
        "python open read",
        _shell_event("Bash", "python -c \"open('docs/x.md').read()\""),
    )
    _expect_denied(
        "python open write",
        _shell_event("Bash", "python -c \"open('docs/x.md', 'w').write('bad')\""),
    )

    for failure in failures:
        print(f"SELFTEST FAILURE: {failure}", file=sys.stderr)
    ok = not failures
    print("CODEX ADAPTER SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main():
    if HOOK_ADOPTION_CANARY_ARG in sys.argv:
        return _not_intercepted()
    if "--selftest" in sys.argv:
        return _selftest()

    event_text = sys.stdin.read()
    try:
        event = json.loads(event_text)
    except Exception:
        return _run_guard_event(event_text)

    if event.get("tool_name") in SHELL_TOOLS and _is_hook_adoption_canary(
        event.get("tool_input") or {}
    ):
        return _deny(HOOK_ADOPTION_ADOPTED)
    if event.get("tool_name") == "apply_patch":
        reason = _check_apply_patch_paths(event.get("tool_input") or {})
        if reason:
            return _deny(reason)

    elif event.get("tool_name") in SHELL_TOOLS:
        reason = _check_shell_durable_write(event.get("tool_input") or {})
        if reason:
            return _deny(reason)

    return _run_guard_event(event_text)


if __name__ == "__main__":
    sys.exit(main())
