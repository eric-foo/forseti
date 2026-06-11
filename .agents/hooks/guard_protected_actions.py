#!/usr/bin/env python3
"""Orca protected-action guard — PreToolUse hook (EP-01 + EP-03).

Hard-blocks the few irreversible actions an autonomous (auto/bypass-mode) agent
must never take unattended:

  EP-01  writes/edits into protected external roots (jb, agent-workflow, and the
         user-level plugin/skill caches) — corrupting another repo/tooling.
  EP-03  irreversible / main-affecting git: blocks landing a PR to main
         (`gh pr merge`), direct push to main, force-push, and bare/ambiguous
         push, plus `reset --hard` / `clean` — via Bash OR PowerShell. ALLOWS an
         explicit non-main, non-force lane push (`git push -u origin <lane>`) so
         lanes can prep PRs under the per-lane PR flow; a human / explicitly
         authorized action lands the PR to main.

This fires in ALL permission modes, including auto-accept / bypassPermissions,
which is the point: `ask`/`deny` permission rules need a human and go inert in
auto mode; a PreToolUse hook does not. It references rule authority rather than
restating it.

Authority (the rules):     .agents/workflow-overlay/safety-rules.md
Dev-workflow doctrine:     docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
                           (on main: per-lane PR flow; the server-side merge gate
                           is 403-blocked on this private/free repo, so this hook
                           is the local stand-in against unattended land-to-main)
Placement principle:       .agents/workflow-overlay/validation-gates.md -> "Enforcement Placement"
Per-rule classification:   docs/decisions/overlay_enforcement_placement_classification_v0.md

Scope (deliberately narrow): `git commit` and an explicit lane-branch push are
NOT blocked (reversible; required by the per-lane PR flow); generic file deletion
is NOT blocked. Only the irreversible / main-affecting few are blocked.
Authorized exceptions: run the action yourself, or temporarily remove this hook.

Contract: reads the PreToolUse JSON on stdin; exit 2 + stderr = BLOCK; exit 0 =
allow. On any internal error it fails OPEN (exit 0) to avoid bricking the agent.
"""
import json
import os
import re
import sys

HOME = os.path.expanduser("~")
REPO_SLUG = "eric-foo/orca"


def _norm(p):
    return os.path.abspath(p).replace("\\", "/").lower()


# --- EP-01: protected-path writes ------------------------------------------
# Home-level caches/skills that are never an Orca write target. Exact-dir
# boundary so the in-repo project `.claude/skills/` (a different absolute path)
# is NOT caught.
_DOTFOLDER_PROTECTED = [
    _norm(os.path.join(HOME, ".codex", "plugins")),
    _norm(os.path.join(HOME, ".codex", "skills")),
    _norm(os.path.join(HOME, ".claude", "plugins")),
    _norm(os.path.join(HOME, ".claude", "skills")),
    _norm(os.path.join(HOME, ".agents", "skills")),
]
# Sibling projects under ~/Desktop/projects matched by first-segment prefix, so
# `jb` and `jb nonrepo` are both caught and `orca` never is.
_PROJECTS = _norm(os.path.join(HOME, "Desktop", "projects"))
_PROTECTED_PROJECT_PREFIXES = ("agent-workflow", "jb")

WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
SHELL_TOOLS = {"Bash", "PowerShell"}


def _protected_path(target):
    """Return the matched protected root, or None."""
    if not target:
        return None
    p = _norm(target)
    for d in _DOTFOLDER_PROTECTED:
        if p == d or p.startswith(d + "/"):
            return d
    if p == _PROJECTS or p.startswith(_PROJECTS + "/"):
        rest = p[len(_PROJECTS):].lstrip("/")
        first = rest.split("/", 1)[0] if rest else ""
        for pref in _PROTECTED_PROJECT_PREFIXES:
            if first.startswith(pref):
                return _PROJECTS + "/" + first
    return None


# --- EP-03: irreversible / main-affecting git ------------------------------
# git invocation allowing -C <path> / -c k=v / global flags before the
# subcommand; matched per shell segment (we split on separators first) so
# `cd x && git push` is caught.
_GIT_PREFIX = r"\bgit\b(?:\s+-C\s+\S+|\s+-c\s+\S+|\s+--?\S+)*\s+"
_RESET_HARD = re.compile(_GIT_PREFIX + r"reset\b[^&|;]*--hard\b", re.I)
_CLEAN = re.compile(_GIT_PREFIX + r"clean\b", re.I)
_PUSH = re.compile(_GIT_PREFIX + r"push\b(.*)$", re.I)
_GH_PR_MERGE = re.compile(r"\bgh\s+pr\s+merge\b", re.I)
_GH_API_MERGE = re.compile(r"\bgh\s+api\b.*?(?:pulls?/\d+/merge|/merges)\b", re.I)
_FORCE = re.compile(r"--force(?:-with-lease)?\b|(?:^|\s)-[A-Za-z]*f[A-Za-z]*\b", re.I)
_SEP = re.compile(r"&&|\|\||[;\n|]")
# Drop quoted args before matching, so a *mention* of a dangerous command inside
# a string/echo (e.g. `echo "gh pr merge"`, or a commit message) is not treated
# as the command itself. Trade-off: a command hidden inside `bash -c "..."` is
# not seen — an accepted gap (this guards accidents, not deliberate evasion).
_QUOTED = re.compile(r"\"[^\"]*\"|'[^']*'")


def _push_block_reason(rest):
    """`rest` = text after `git ... push`. Return a reason, or None to ALLOW.

    Allows an explicit `<remote> <non-main-branch>` push without force; blocks
    force-push, pushes that target `main`, a bare `HEAD` (whose branch could be
    main), and bare/ambiguous pushes."""
    if _FORCE.search(rest):
        return "force-push"
    positionals = [t for t in rest.split() if t and not t.startswith("-")]
    for t in positionals:
        if "main" in t.split(":"):
            return "push to main"
    if "HEAD" in positionals:
        return "ambiguous push (bare HEAD could be main)"
    if len(positionals) < 2:
        return "bare/ambiguous push (could target main)"
    return None


def _shell_block_reason(cmd):
    """Return an EP-03 block reason for a shell command, or None to allow."""
    cmd = _QUOTED.sub(" ", cmd or "")
    for seg in _SEP.split(cmd):
        seg = seg.strip()
        if not seg:
            continue
        if _GH_PR_MERGE.search(seg) or _GH_API_MERGE.search(seg):
            return "EP-03 land-to-main (PR merge): %s" % seg[:160]
        if _RESET_HARD.search(seg):
            return "EP-03 destructive (git reset --hard): %s" % seg[:160]
        if _CLEAN.search(seg):
            return "EP-03 destructive (git clean): %s" % seg[:160]
        m = _PUSH.search(seg)
        if m:
            why = _push_block_reason(m.group(1))
            if why:
                return "EP-03 %s: %s" % (why, seg[:160])
    return None


def decide(tool_name, tool_input):
    """Pure decision. Returns (block: bool, reason: str)."""
    tool_input = tool_input or {}
    if tool_name in WRITE_TOOLS:
        target = (tool_input.get("file_path")
                  or tool_input.get("notebook_path")
                  or tool_input.get("path"))
        hit = _protected_path(target)
        if hit:
            return True, "EP-01 protected-path write: %s (under %s)" % (target, hit)
    elif tool_name in SHELL_TOOLS:
        reason = _shell_block_reason(tool_input.get("command", "") or "")
        if reason:
            return True, reason
    return False, ""


_BLOCK_MSG = (
    "BLOCKED by Orca protected-action guard (.agents/hooks/guard_protected_actions.py).\n"
    "Reason: %s\n"
    "%s"
    "Authority: .agents/workflow-overlay/safety-rules.md + dev-workflow doctrine "
    "(no unattended land-to-main / push-to-main / force-push / destructive-clean, "
    "and no edits to jb/external/installed skills, unless explicitly authorized). "
    "Fires in all modes incl. auto.\n"
    "Authorized exception: run it yourself (e.g. a human lands the PR), or remove "
    "this hook. An explicit lane push `git push -u origin <lane>` is allowed."
)

# --- selftest ---------------------------------------------------------------
def _selftest():
    j = lambda *a: os.path.join(HOME, *a)
    cases = [
        # EP-03 block: land-to-main
        ("Bash", {"command": "gh pr merge 9 --squash"}, True),
        ("PowerShell", {"command": "gh pr merge"}, True),
        ("Bash", {"command": "gh api -X PUT repos/eric-foo/orca/pulls/9/merge"}, True),
        # EP-03 block: push to main / force / bare / HEAD
        ("Bash", {"command": "git push origin main"}, True),
        ("Bash", {"command": "git push origin HEAD:main"}, True),
        ("Bash", {"command": "git add -A && git push origin main"}, True),
        ("PowerShell", {"command": "cd repo; git push --force"}, True),
        ("Bash", {"command": "git push -f origin my-lane"}, True),
        ("Bash", {"command": "git push"}, True),
        ("Bash", {"command": "git push origin HEAD"}, True),
        # EP-03 block: destructive
        ("Bash", {"command": "git -C . reset --hard HEAD~1"}, True),
        ("PowerShell", {"command": "git clean -fd"}, True),
        ("Bash", {"command": "git reset HEAD~1 --hard"}, True),
        # EP-01 block: protected paths
        ("Write", {"file_path": j("Desktop", "projects", "jb", "x.md")}, True),
        ("Write", {"file_path": j("Desktop", "projects", "jb nonrepo", "x.md")}, True),
        ("Edit", {"file_path": j("Desktop", "projects", "agent-workflow", "p.md")}, True),
        ("Write", {"file_path": j(".claude", "skills", "evil", "SKILL.md")}, True),
        # ALLOW: lane push (the per-lane PR flow) — the key new behavior
        ("Bash", {"command": "git push -u origin ecr-sp3-timing-deriver-slice1"}, False),
        ("Bash", {"command": "git push origin my-lane"}, False),
        ("Bash", {"command": "git push origin HEAD:my-lane"}, False),
        ("Bash", {"command": "git push origin feature/main-helper"}, False),
        ("Bash", {"command": "git add docs/x.md && git push -u origin my-lane"}, False),
        # ALLOW: benign
        ("Bash", {"command": "gh pr checks 9"}, False),
        ("Bash", {"command": "echo \"=== gh pr merge test ===\""}, False),
        ("Bash", {"command": "echo 'git push origin main'"}, False),
        ("Bash", {"command": "git commit -m \"note: git push to main is gated\""}, False),
        ("Bash", {"command": "git status"}, False),
        ("Bash", {"command": "git commit -m 'x'"}, False),
        ("Bash", {"command": "git log --grep=push"}, False),
        ("Write", {"file_path": j("Desktop", "projects", "orca", "docs", "x.md")}, False),
        ("Edit", {"file_path": j("Desktop", "projects", "orca", ".claude", "skills", "orca-product-lead", "SKILL.md")}, False),
        ("Read", {"file_path": j("Desktop", "projects", "jb", "x.md")}, False),
    ]
    ok = True
    for i, (tn, ti, expect) in enumerate(cases, 1):
        got, reason = decide(tn, ti)
        status = "PASS" if got == expect else "FAIL"
        if got != expect:
            ok = False
        print("%s case %02d  %-12s expect_block=%-5s got=%-5s  %s"
              % (status, i, tn, expect, got, reason or ""))
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main():
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    try:
        ev = json.load(sys.stdin)
        block, reason = decide(ev.get("tool_name", ""), ev.get("tool_input", {}))
    except Exception as exc:  # fail OPEN: never brick the agent on a guard bug
        sys.stderr.write("guard_protected_actions: internal error, allowing: %s\n" % exc)
        sys.exit(0)
    if block:
        hint = ""
        if "land-to-main (PR merge)" in reason:
            pr_m = re.search(r"\bpr\s+merge\s+(\d+)", reason, re.I)
            pr_ref = pr_m.group(1) if pr_m else "<PR#>"
            hint = (
                "  → Merge manually (PowerShell / terminal):\n"
                "    gh pr merge %s --squash --delete-branch --repo %s\n"
            ) % (pr_ref, REPO_SLUG)
        sys.stderr.write(_BLOCK_MSG % (reason, hint) + "\n")
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
