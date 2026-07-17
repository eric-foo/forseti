#!/usr/bin/env python3
"""Registration-integrity check -- every artifact a shared registry names must exist.

WHAT THIS DOES (a CI-promoted, workspace-independent defect check)
  Verifies the checked-out tree's internal consistency: a shared registry/config
  names an artifact by path; that artifact must be present in the tree. A dangling
  reference breaks a fresh clone -- e.g. a hook registered in .claude/settings.json
  whose script file is missing errors on every matching tool call.

  This is the SINGLE workspace-independent, false-positive-free signal promoted to
  CI. The workspace-local health nudges (uncommitted pile-up, worktree sprawl,
  "present locally but not yet on main") are deliberately NOT run here.

CHECKS (selectable with --checks; default = all)
  hook-registration   For every hook `command` in .claude/settings.json, verify the
                      registered Python script exists as an in-tree regular file.

SCOPE (narrowed after the GPT-5.5 cross-vendor review, findings F1-F4)
  This check covers the `python[3] <script>.py [args]` hook-command form -- which is
  the only form Forseti uses. A hook command it cannot verify in that form (a non-python
  interpreter, `python -c`/`-m`, or a first positional that is not a `.py` script) is
  reported as `unverifiable` and FAILS the check (never silently passed) -- extend the
  check or convert the hook. It does not (yet) verify `.sh`/`.js`/extensionless hook
  artifacts; that would be a deliberate, separate broadening, not assumed here.

WHY THIS IS SAFE TO RUN IN CI
  - Decidable from the checked-out tree ALONE: reads .claude/settings.json and the
    filesystem. No base ref, no git history, no network -> a shallow CI checkout
    works and it cannot false-positive on "new in this PR, not yet on main".
  - Directional: a registry entry must have its file (entry -> file). It never flags
    a file that merely lacks a registry entry.
  - In-tree regular file only (F1): a registered script counts as present only when it
    resolves to a regular file INSIDE the checkout -- a same-named directory, a symlink
    to a directory, or an absolute / `..`-escaping path does NOT satisfy it.
  - Precise script extraction (F2): the script is the first positional token after the
    `python` interpreter, per `;`/`&&`/`||`/`|`-separated segment -- so a compound
    command is not missed and an option value like `--config x.py` is not mistaken for
    the script.
  - Fails LOUD: an unknown/empty --checks, an unreadable settings file, an unverifiable
    hook command, or an internal error all exit non-zero. It never silently runs nothing
    -- a silent no-op could mask the very defect it guards.

EXIT CODES
  0  every selected check passed (or there was genuinely nothing to verify)
  1  a selected check found a dangling reference or an unverifiable hook command
  2  misuse or internal error (unknown/empty --checks, unreadable settings)

ENFORCEMENT REACH (honesty)
  A non-zero exit fails the PR's check run, and active branch protection requires the
  strict forseti-harness-tests context before main can merge. This checker proves only
  registration integrity inside that required job; it is not validation or readiness by itself.

USAGE
  python .agents/checks/registration_integrity.py                      # all checks
  python .agents/checks/registration_integrity.py --checks hook-registration
  python .agents/checks/registration_integrity.py --list
  python .agents/checks/registration_integrity.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import sys
from pathlib import Path, PurePosixPath

# Split a hook command into independently-run segments (compound shell commands).
_SEGMENT_SEP = re.compile(r"&&|\|\||[;|]")
# The hook interpreters this check verifies (Forseti hooks are python).
_PY_INTERPRETERS = ("python", "python3")


# ---- pure decision core (unit-testable) -------------------------------------

def _segments(command: str) -> list:
    return [s.strip() for s in _SEGMENT_SEP.split(command) if s.strip()]


def classify_segment(segment: str):
    """Classify one command segment.

    Returns ('script', path) for a supported `python[3] <path>.py [args]` form
    (path = the registered script), ('unsupported', segment) for a hook command
    this python-script check cannot verify, or None for empty. Only the FIRST
    positional (non-option) token after a python interpreter is the script, and it
    must end in `.py`; option flags and their `=value`s are skipped, so
    `--config x.py` / `--flag="x.py"` are never mistaken for the script (F2)."""
    try:
        toks = shlex.split(segment, posix=True)
    except ValueError:
        toks = segment.split()
    if not toks:
        return None
    if PurePosixPath(toks[0]).name not in _PY_INTERPRETERS:
        return ("unsupported", segment)                  # non-python interpreter / direct exec
    for tok in toks[1:]:
        if tok.startswith("-c") or tok.startswith("-m"):
            return ("unsupported", segment)              # inline code / module: no script file
        if tok.startswith("-"):
            continue                                     # other option flag: skip
        return ("script", tok) if tok.endswith(".py") else ("unsupported", segment)
    return ("unsupported", segment)                      # python with no script positional


def scan_command(command: str):
    """Return (scripts, unsupported_segments) across all segments of a hook command."""
    scripts, unsupported = [], []
    for seg in _segments(command):
        classified = classify_segment(seg)
        if not classified:
            continue
        kind, value = classified
        (scripts if kind == "script" else unsupported).append(value)
    return scripts, unsupported


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


def _registered_script_path(path: str) -> str:
    """Map Claude's canonical project-root token to a repo-relative path."""
    normalized = path.replace("\\", "/")
    for prefix in ("$CLAUDE_PROJECT_DIR/", "${CLAUDE_PROJECT_DIR}/"):
        if normalized.startswith(prefix):
            return normalized[len(prefix):]
    return normalized


def hook_findings(settings: dict, is_intree_file) -> list:
    """Pure: list of (category, detail) findings (empty = pass).

    `is_intree_file` is a predicate (repo-relative path str -> bool), injected so
    this is testable without the filesystem. Categories:
      'dangling'      a python-script hook whose script is not an in-tree regular file
      'unverifiable'  a hook command this python-script check cannot verify (fail loud)"""
    findings = []
    for command in _hook_commands(settings):
        scripts, unsupported = scan_command(command)
        for path in scripts:
            resolved_path = _registered_script_path(path)
            if not is_intree_file(resolved_path):
                findings.append(("dangling", "%s  (in command: %r)" % (path, command)))
        for seg in unsupported:
            findings.append(("unverifiable", "%r  (segment of: %r)" % (seg, command)))
    return findings


# ---- IO wrappers ------------------------------------------------------------

def _load_settings(root: Path) -> dict:
    """Load the COMMITTED .claude/settings.json (the file a fresh clone has).

    settings.local.json is gitignored/machine-specific and intentionally not read.
    An absent settings.json is a valid 'nothing to verify' state."""
    p = root / ".claude" / "settings.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _intree_regular_file(root: Path, rel: str) -> bool:
    """True only if `rel` resolves to a regular file INSIDE the checkout (F1).

    Rejects directories, absolute paths, and `..`-escapes -- so a same-named
    directory or an out-of-tree path cannot mask a missing hook script."""
    try:
        root_resolved = root.resolve()
        target = (root / rel).resolve()
    except OSError:
        return False
    try:
        target.relative_to(root_resolved)
    except ValueError:
        return False                       # absolute, or escaped the checkout
    return target.is_file()                # not a directory / missing


def check_hook_registration(root: Path) -> list:
    """Return human-readable findings (empty list = pass)."""
    settings = _load_settings(root)
    out = []
    for category, detail in hook_findings(settings, lambda rel: _intree_regular_file(root, rel)):
        if category == "dangling":
            out.append("dangling hook script (registry names a missing in-tree file): " + detail)
        else:
            out.append("unverifiable hook command (not a python-script form this check "
                       "covers; convert the hook or extend the check): " + detail)
    return out


CHECKS = {
    "hook-registration": check_hook_registration,
}


# ---- runner -----------------------------------------------------------------

def run(selected: list, root: Path) -> int:
    findings = []
    for name in selected:
        findings.extend(CHECKS[name](root))
    if findings:
        print("FAIL registration-integrity (%d finding(s)):" % len(findings))
        for f in findings:
            print("  - " + f)
        return 1
    print("OK registration-integrity [%s]: every registered script is an in-tree file "
          "and every hook command is verifiable" % ", ".join(selected))
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
    import tempfile
    ok = True

    def expect(label, cond):
        nonlocal ok
        ok = ok and cond
        print(("PASS " if cond else "FAIL ") + label)

    # classify_segment -- precise script extraction (F2)
    expect("bare python script",
           classify_segment("python .agents/hooks/g.py") == ("script", ".agents/hooks/g.py"))
    expect("trailing arg ignored",
           classify_segment("python .agents/hooks/g.py --hook") == ("script", ".agents/hooks/g.py"))
    expect("Claude project-root token resolves inside checkout",
           _registered_script_path("$CLAUDE_PROJECT_DIR/.agents/hooks/g.py")
           == ".agents/hooks/g.py")
    expect("braced Claude project-root token resolves inside checkout",
           _registered_script_path("${CLAUDE_PROJECT_DIR}/.agents/hooks/g.py")
           == ".agents/hooks/g.py")
    expect("option value .py is not the script (F2)",
           classify_segment("python .agents/hooks/g.py --config config.py") == ("script", ".agents/hooks/g.py"))
    expect("flag=value .py is not the script (F2)",
           classify_segment('python .agents/hooks/g.py --flag="b.py"') == ("script", ".agents/hooks/g.py"))
    expect("python -c is unverifiable (F2/F3)", classify_segment('python -c "import x"')[0] == "unsupported")
    expect("python -m is unverifiable (F3)", classify_segment("python -m pkg.mod")[0] == "unsupported")
    expect("non-python interpreter is unverifiable (F3)",
           classify_segment("node .agents/hooks/g.js")[0] == "unsupported")
    expect("non-.py positional is unverifiable (F3)",
           classify_segment("python .agents/hooks/g")[0] == "unsupported")

    # scan_command -- compound command is split, not missed (F2 case 1)
    scripts, _ = scan_command("python .agents/hooks/a.py; python .agents/hooks/b.py")
    expect("compound command -> both scripts (F2)",
           scripts == [".agents/hooks/a.py", ".agents/hooks/b.py"])

    # hook_findings -- dangling vs unverifiable (pure, injected predicate)
    settings = {"hooks": {
        "PreToolUse": [{"hooks": [{"command": "python .agents/hooks/present.py"}]}],
        "Stop": [{"hooks": [{"command": "python .agents/hooks/gone.py --hook"}]}],
        "PostToolUse": [{"hooks": [{"command": "node .agents/hooks/x.js"}]}],
    }}
    present = {".agents/hooks/present.py"}
    found = hook_findings(settings, lambda p: p in present)
    expect("flags the dangling python script",
           any(c == "dangling" and "gone.py" in d for c, d in found))
    expect("does not flag the present script", not any("present.py" in d for _, d in found))
    expect("surfaces the non-python hook, no silent pass (F3)",
           any(c == "unverifiable" for c, _ in found))

    # robustness: empty / malformed settings structure -> no crash (F4 boundary)
    expect("no hooks key -> nothing to verify", hook_findings({}, lambda p: False) == [])
    expect("malformed hooks shape ignored, no crash", hook_findings({"hooks": []}, lambda p: False) == [])

    # _intree_regular_file -- in-tree regular file only (F1)
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "real.py").write_text("x", encoding="utf-8")
        (root / "adir.py").mkdir()
        expect("in-tree regular file accepted (F1)", _intree_regular_file(root, "real.py") is True)
        expect("directory rejected (F1)", _intree_regular_file(root, "adir.py") is False)
        expect("missing rejected", _intree_regular_file(root, "nope.py") is False)
        expect("parent-escape rejected (F1)", _intree_regular_file(root, "../outside.py") is False)

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
        description="Registration-integrity check (registry entry -> in-tree artifact).")
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


def repo_root() -> Path:
    """Repo root, derived from this file's location (.agents/checks/<this>)."""
    return Path(__file__).resolve().parents[2]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
