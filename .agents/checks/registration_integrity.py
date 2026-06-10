#!/usr/bin/env python3
"""Registration-integrity check -- every artifact a shared registry names must exist.

WHAT THIS DOES (a CI-promoted, workspace-independent defect check)
  Verifies the checked-out tree's internal consistency: a shared registry/config
  names an artifact by path; that artifact must be present in the tree. A dangling
  reference breaks a fresh clone -- e.g. a hook registered in .claude/settings.json
  whose script file is missing errors on every matching tool call.

  This is the SINGLE workspace-independent, false-positive-free signal promoted to
  CI. The workspace-local health nudges (uncommitted pile-up, worktree sprawl,
  "present locally but not yet on main") are deliberately NOT run here -- a clean CI
  checkout has no local pile-up, and a PR's newly-added artifact legitimately is not
  on main yet, so those signals would false-positive in CI.

CHECKS (selectable with --checks; default = all)
  hook-registration   Every `.py` script referenced by a hook `command` in
                      .claude/settings.json must exist in the tree.

WHY THIS IS SAFE TO RUN IN CI
  - Decidable from the checked-out tree ALONE: reads .claude/settings.json and the
    filesystem. No base ref, no git history, no network -> a shallow CI checkout
    works and it cannot false-positive on "new in this PR, not yet on main".
  - Directional: a registry entry must have its file (entry -> file). It never flags
    a file that merely lacks a registry entry (READMEs and special-purpose files are
    legitimately unregistered) -- the reverse direction would false-positive.
  - Fails LOUD on misuse: an unknown or empty --checks, or an unreadable settings
    file, exits non-zero. It never silently runs nothing -- a silent no-op could
    mask the very defect it guards.

EXIT CODES
  0  every selected check passed (or there was genuinely nothing to verify)
  1  a selected check found a dangling reference (the defect)
  2  misuse or internal error (unknown/empty --checks, unreadable settings) --
     never a silent pass

ENFORCEMENT REACH (honesty)
  A non-zero exit fails the PR's check run. Without server-side required-status-
  checks (ORCA branch protection is 403-blocked on a private/free repo), that is a
  STRONG signal under merge-when-green / structure-B discipline, NOT a server-
  enforced merge gate. It does not, by itself, block a merge.

USAGE
  python .agents/checks/registration_integrity.py                      # all checks
  python .agents/checks/registration_integrity.py --checks hook-registration
  python .agents/checks/registration_integrity.py --list
  python .agents/checks/registration_integrity.py --selftest
"""
from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path


def repo_root() -> Path:
    """Repo root, derived from this file's location (.agents/checks/<this>)."""
    return Path(__file__).resolve().parents[2]


# ---- pure decision core (filesystem-free, unit-testable) --------------------

def _script_paths(command: str) -> list[str]:
    """Repo-relative `.py` paths referenced in a hook command string.

    A hook command looks like `python .agents/hooks/x.py --hook`. Tokenize
    (shlex handles quotes), then keep tokens ending in `.py`; args like `--hook`
    are ignored because only the script path is load-bearing."""
    try:
        toks = shlex.split(command, posix=True)
    except ValueError:
        toks = command.split()
    return [t for t in toks if t.endswith(".py")]


def _hook_commands(settings: dict):
    """Yield every hook `command` string in a settings dict, across all events."""
    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        return
    for event_entries in hooks.values():
        if not isinstance(event_entries, list):
            continue
        for entry in event_entries:
            if not isinstance(entry, dict):
                continue
            for hook in entry.get("hooks", []) or []:
                if isinstance(hook, dict) and isinstance(hook.get("command"), str):
                    yield hook["command"]


def missing_hook_scripts(settings: dict, exists) -> list:
    """Pure: return (command, script_path) pairs whose script does NOT exist.

    `exists` is a predicate (repo-relative path str -> bool), injected so this is
    testable without touching the filesystem."""
    missing = []
    for command in _hook_commands(settings):
        for path in _script_paths(command):
            if not exists(path):
                missing.append((command, path))
    return missing


# ---- IO wrappers ------------------------------------------------------------

def _load_settings(root: Path) -> dict:
    """Load the COMMITTED .claude/settings.json (the file a fresh clone has).

    settings.local.json is gitignored/machine-specific and is intentionally not
    consulted. An absent settings.json is a valid 'nothing to verify' state."""
    p = root / ".claude" / "settings.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def check_hook_registration(root: Path) -> list:
    """Return human-readable findings (empty list = pass)."""
    settings = _load_settings(root)
    missing = missing_hook_scripts(settings, lambda rel: (root / rel).exists())
    return ["hook registers a missing script: %s  (in command: %r)" % (path, cmd)
            for cmd, path in missing]


CHECKS = {
    "hook-registration": check_hook_registration,
}


# ---- runner -----------------------------------------------------------------

def run(selected: list, root: Path) -> int:
    findings = []
    for name in selected:
        findings.extend(CHECKS[name](root))
    if findings:
        print("FAIL registration-integrity (%d dangling reference(s)):" % len(findings))
        for f in findings:
            print("  - " + f)
        return 1
    print("OK registration-integrity [%s]: every named artifact exists"
          % ", ".join(selected))
    return 0


def _parse_checks(value: str) -> list:
    names = [n.strip() for n in value.split(",") if n.strip()]
    if not names:
        raise ValueError("empty --checks (never run nothing silently)")
    unknown = [n for n in names if n not in CHECKS]
    if unknown:
        raise ValueError("unknown check(s): %s (known: %s)"
                         % (", ".join(unknown), ", ".join(sorted(CHECKS))))
    return names


def selftest() -> int:
    ok = True

    def expect(label, cond):
        nonlocal ok
        ok = ok and cond
        print(("PASS " if cond else "FAIL ") + label)

    # _script_paths
    expect("extract bare script",
           _script_paths("python .agents/hooks/g.py") == [".agents/hooks/g.py"])
    expect("ignore trailing args",
           _script_paths("python .agents/hooks/g.py --hook") == [".agents/hooks/g.py"])
    expect("no .py token -> empty", _script_paths("echo hi") == [])

    # missing_hook_scripts (pure, injected exists predicate)
    settings = {"hooks": {
        "PreToolUse": [{"hooks": [{"command": "python .agents/hooks/present.py"}]}],
        "Stop": [{"hooks": [{"command": "python .agents/hooks/gone.py --hook"}]}],
    }}
    present = {".agents/hooks/present.py"}
    miss = [p for _, p in missing_hook_scripts(settings, lambda p: p in present)]
    expect("detects the missing script", miss == [".agents/hooks/gone.py"])
    expect("does not flag the present script", ".agents/hooks/present.py" not in miss)

    # robustness: empty / malformed settings -> no findings, no crash
    expect("no hooks key -> nothing to verify",
           missing_hook_scripts({}, lambda p: False) == [])
    expect("malformed hooks ignored",
           missing_hook_scripts({"hooks": []}, lambda p: False) == [])

    # _parse_checks fails LOUD on misuse
    try:
        _parse_checks("nope")
        expect("unknown check raises", False)
    except ValueError:
        expect("unknown check raises", True)
    try:
        _parse_checks("   ")
        expect("empty check raises", False)
    except ValueError:
        expect("empty check raises", True)

    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list) -> int:
    ap = argparse.ArgumentParser(
        description="Registration-integrity check (registry entry -> artifact exists).")
    ap.add_argument("--checks", default=",".join(sorted(CHECKS)),
                    help="comma-separated check names (default: all). Known: %s"
                         % ", ".join(sorted(CHECKS)))
    ap.add_argument("--list", action="store_true", help="list known checks and exit")
    ap.add_argument("--selftest", action="store_true",
                    help="run pure-decision selftests and exit")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.list:
        print("\n".join(sorted(CHECKS)))
        return 0
    try:
        selected = _parse_checks(args.checks)
    except ValueError as exc:
        sys.stderr.write("registration_integrity: misuse: %s\n" % exc)
        return 2
    try:
        return run(selected, repo_root())
    except Exception as exc:  # loud, never a silent pass
        sys.stderr.write("registration_integrity: internal error (failing loud): %s\n" % exc)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
