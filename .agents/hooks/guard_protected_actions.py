#!/usr/bin/env python3
"""Forseti protected-action guard — PreToolUse hook (EP-01 + EP-03).

Hard-blocks the few irreversible actions an autonomous (auto/bypass-mode) agent
must never take unattended:

  EP-01  writes/edits into protected external roots (jb, agent-workflow, and the
         user-level plugin/skill caches) — corrupting another repo/tooling.
  EP-03  irreversible / main-affecting git: blocks direct push to main,
         force-push, and bare/ambiguous push, plus `reset --hard` / `clean` — via
         Bash OR PowerShell. ALLOWS an explicit non-main, non-force lane push
         (`git push -u origin <lane>`) so lanes can prep PRs under the per-lane PR
         flow.
         Landing a PR to main (`gh pr merge <N>`) is CONDITIONALLY allowed: the
         guard queries the PR and allows the merge ONLY when it is mergeStateStatus
         == CLEAN, every CI check has completed green, it carries the opt-in
         `agent-automerge` label, AND the router did NOT flag it
         `risk/manual-review-required` / `risk/blocked-for-merge-policy` (so a
         governed deletion or protected-surface PR is never self-merged). Any other
         state, a missing/ambiguous PR number, the lower-level `gh api .../merge`
         form, or any lookup error/timeout FAILS CLOSED (blocks) — and the block
         message prints the repo-scoped manual `gh pr merge ... --repo` command a
         human can run from anywhere.

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
allow. On any internal error the NON-merge paths fail OPEN (exit 0) to avoid
bricking the agent. The merge-authorization path is the deliberate exception: it
fails CLOSED (block) on any lookup error, timeout, parse failure, or non-CLEAN
state, because an erroneous ALLOW there would land unattended code on main. Its
`gh` lookup is self-limited to GH_TIMEOUT (< the hook's own timeout) so the guard
returns its own block before any harness-level timeout-kill could fail open.
"""
import json
import os
import re
import subprocess
import sys

HOME = os.path.expanduser("~")
DEFAULT_REPO_SLUG = "eric-foo/orca"
_REPO_SLUG_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def _configured_repo_slug(env=None):
    env = os.environ if env is None else env
    candidate = (
        env.get("FORSETI_GITHUB_REPOSITORY")
        or env.get("GITHUB_REPOSITORY")
        or DEFAULT_REPO_SLUG
    )
    if not _REPO_SLUG_RE.fullmatch(candidate):
        return DEFAULT_REPO_SLUG
    return candidate


REPO_SLUG = _configured_repo_slug()

# Opt-in label a PR must carry before the guard will allow an agent self-merge.
# A PR without it never auto-merges (safe default). One-time repo setup to make
# the label applyable: `gh label create agent-automerge --repo <configured-repo>`.
AUTOMERGE_LABEL = "agent-automerge"
# Router risk labels meaning "a human must land this" (deletions, protected
# surfaces). The guard honors them so an in-session self-merge cannot override
# the router's routing -- the same labels the unattended auto-merge bot already
# respects. Closes the gap where a router-flagged PR (e.g. a governed deletion)
# could still self-merge on CLEAN + green + agent-automerge alone.
MANUAL_RISK_LABELS = ("risk/manual-review-required", "risk/blocked-for-merge-policy")
# Self-imposed ceiling on the PR-state `gh` call, kept below the hook's own
# settings.json timeout so we fail CLOSED in-script rather than relying on the
# harness's (unspecified) timeout-kill behavior.
GH_TIMEOUT = 6
# statusCheckRollup conclusions that count as "green" for a completed check.
_OK_CONCLUSIONS = {"SUCCESS", "NEUTRAL", "SKIPPED"}


def _norm(p):
    return os.path.abspath(p).replace("\\", "/").lower()


# --- EP-01: protected-path writes ------------------------------------------
# Home-level caches/skills that are never a Forseti write target. Exact-dir
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
_GH_PR_MERGE = re.compile(r"\bgh\s+pr\s+merge\b(.*)$", re.I)
_GH_API_MERGE = re.compile(r"\bgh\s+api\b.*?(?:pulls?/\d+/merge|/merges)\b", re.I)
# `--repo owner/name` / `-R owner/name` on a merge: the guard only ever queries
# REPO_SLUG, so a merge explicitly aimed at a different repo cannot be verified
# here and must fail closed (never auto-allowed on this guard's authority).
_REPO_FLAG = re.compile(r"(?:--repo|-R)[=\s]+(\S+)", re.I)
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


# --- EP-03: conditional `gh pr merge` (CLEAN self-merge) -------------------
def _parse_pr_ref(rest):
    """`rest` = text after `gh pr merge`. Return an explicit PR number string, or
    None. Accepts a bare integer or a `.../pull/<n>` URL; a branch name or no
    argument returns None — auto-merge requires an explicit number, so the guard
    never guesses which PR is being landed (and a no-arg merge fails closed)."""
    for t in (rest or "").split():
        if t.startswith("-"):
            continue
        if t.isdigit():
            return t
        m = re.search(r"/pull/(\d+)", t)
        if m:
            return m.group(1)
    return None


def _check_ok(c):
    """True iff a single statusCheckRollup entry is completed-green."""
    if not isinstance(c, dict):
        return False
    if c.get("conclusion") is not None or c.get("__typename") == "CheckRun":
        return (c.get("status") == "COMPLETED"
                and str(c.get("conclusion") or "").upper() in _OK_CONCLUSIONS)
    if c.get("state") is not None:  # legacy commit StatusContext
        return str(c.get("state")).upper() == "SUCCESS"
    return False


def _query_pr_state(pr):
    """Real PR-state lookup: ONE repo-scoped `gh` call, self-timed below the hook
    budget. Returns the parsed JSON dict, or None on any non-zero exit (the caller
    wraps this in try/except and treats every failure as a CLOSED block)."""
    out = subprocess.run(
        ["gh", "pr", "view", str(pr), "--repo", REPO_SLUG,
         "--json", "number,mergeStateStatus,statusCheckRollup,labels"],
        capture_output=True, text=True, timeout=GH_TIMEOUT,
    )
    if out.returncode != 0:
        return None
    return json.loads(out.stdout or "")


def _merge_decision(pr_ref, lookup):
    """Decide one `gh pr merge` segment. Return None to ALLOW, else a block reason.

    FAIL CLOSED: a missing/ambiguous PR number, any lookup error or timeout, a
    non-CLEAN mergeStateStatus, an empty/non-green check set, a router
    manual/blocked risk label, or a missing opt-in label all block. Only an
    explicit, CLEAN, all-checks-green, `agent-automerge`-labeled PR that the
    router did NOT flag for manual review is allowed to self-merge."""
    if not pr_ref:
        return ("EP-03 merge blocked - needs an explicit PR number "
                "(`gh pr merge <N>`); a no-arg / branch-name merge fails closed")
    try:
        state = lookup(pr_ref)
    except Exception:
        state = None
    if not state:
        return ("EP-03 merge blocked - PR %s mergeability lookup failed "
                "(fail-closed)" % pr_ref)
    mss = state.get("mergeStateStatus")
    if mss != "CLEAN":
        return ("EP-03 merge blocked - PR %s mergeStateStatus=%s, not CLEAN"
                % (pr_ref, mss or "?"))
    rollup = state.get("statusCheckRollup") or []
    if not rollup:
        return ("EP-03 merge blocked - PR %s reports no CI checks yet "
                "(fail-closed against the empty-checkset race)" % pr_ref)
    if not all(_check_ok(c) for c in rollup):
        return ("EP-03 merge blocked - PR %s has non-green or pending checks"
                % pr_ref)
    labels = {(l or {}).get("name") for l in (state.get("labels") or [])}
    blocking = sorted(labels & set(MANUAL_RISK_LABELS))
    if blocking:
        return ("EP-03 merge blocked - PR %s carries router label '%s'; it must be "
                "landed by a human (deletion / protected surface), not self-merged"
                % (pr_ref, blocking[0]))
    if AUTOMERGE_LABEL not in labels:
        return ("EP-03 merge blocked - PR %s missing opt-in label '%s'"
                % (pr_ref, AUTOMERGE_LABEL))
    return None  # CLEAN + green + opt-in label + no manual-risk label → allow self-merge


def _shell_block_reason(cmd, lookup=None):
    """Return an EP-03 block reason for a shell command, or None to allow.

    `lookup` is the PR-state fetcher (injected so --selftest stays offline);
    defaults to the real `gh` query."""
    if lookup is None:
        lookup = _query_pr_state
    cmd = _QUOTED.sub(" ", cmd or "")
    for seg in _SEP.split(cmd):
        seg = seg.strip()
        if not seg:
            continue
        if _GH_API_MERGE.search(seg):
            # The low-level API PUT bypasses gh's own pre-merge mergeability
            # re-check, so it is never auto-allowed — always human/manual.
            return ("EP-03 merge blocked - `gh api .../merge` form is always "
                    "manual: %s" % seg[:160])
        m = _GH_PR_MERGE.search(seg)
        if m:
            rest = m.group(1)
            rflag = _REPO_FLAG.search(rest)
            if rflag and rflag.group(1).lower() != REPO_SLUG.lower():
                return ("EP-03 merge blocked - targets a different repo (%s); "
                        "this guard only authorizes %s"
                        % (rflag.group(1), REPO_SLUG))
            why = _merge_decision(_parse_pr_ref(rest), lookup)
            if why:
                return why
            continue  # CLEAN+green+labeled self-merge — allow; scan other segs
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


def decide(tool_name, tool_input, lookup=None):
    """Decision. Returns (block: bool, reason: str). EP-01 (write paths) is pure;
    the EP-03 merge path may consult `lookup` (the PR-state fetcher, injected in
    tests, real `gh` query in production)."""
    tool_input = tool_input or {}
    if tool_name in WRITE_TOOLS:
        target = (tool_input.get("file_path")
                  or tool_input.get("notebook_path")
                  or tool_input.get("path"))
        hit = _protected_path(target)
        if hit:
            return True, "EP-01 protected-path write: %s (under %s)" % (target, hit)
    elif tool_name in SHELL_TOOLS:
        reason = _shell_block_reason(tool_input.get("command", "") or "", lookup)
        if reason:
            return True, reason
    return False, ""


_BLOCK_MSG = (
    "BLOCKED by Forseti protected-action guard (.agents/hooks/guard_protected_actions.py).\n"
    "Reason: %s\n"
    "%s"
    "Authority: .agents/workflow-overlay/safety-rules.md + dev-workflow doctrine "
    "(push-to-main / force-push / destructive-clean are blocked, and edits to "
    "jb/external/installed skills, unless explicitly authorized; `gh pr merge <N>` "
    "self-merge is allowed ONLY for a CLEAN + CI-green + '" + AUTOMERGE_LABEL +
    "'-labeled PR). Fires in all modes incl. auto.\n"
    "Authorized exception: a human lands the PR with the command above, or remove "
    "this hook. An explicit lane push `git push -u origin <lane>` is allowed."
)

# --- selftest ---------------------------------------------------------------
def _selftest():
    j = lambda *a: os.path.join(HOME, *a)

    # Fake PR-state lookups so the merge logic is tested deterministically and
    # OFFLINE (no `gh`, no network). Each case may pass its own lookup; cases
    # that omit one default to `_fake` (irrelevant for non-merge cases).
    _green = {"__typename": "CheckRun", "status": "COMPLETED", "conclusion": "SUCCESS"}
    _pending = {"__typename": "CheckRun", "status": "IN_PROGRESS", "conclusion": None}
    _FAKE = {
        "100": {"mergeStateStatus": "CLEAN", "statusCheckRollup": [_green],
                "labels": [{"name": AUTOMERGE_LABEL}]},              # the one ALLOW shape
        "101": {"mergeStateStatus": "CLEAN", "statusCheckRollup": [_green],
                "labels": []},                                       # CLEAN+green, no label
        "102": {"mergeStateStatus": "UNSTABLE", "statusCheckRollup": [_green],
                "labels": [{"name": AUTOMERGE_LABEL}]},              # not CLEAN
        "103": {"mergeStateStatus": "CLEAN", "statusCheckRollup": [_pending],
                "labels": [{"name": AUTOMERGE_LABEL}]},              # a check still pending
        "104": {"mergeStateStatus": "CLEAN", "statusCheckRollup": [],
                "labels": [{"name": AUTOMERGE_LABEL}]},              # empty-checkset race
        "105": {"mergeStateStatus": "BLOCKED", "statusCheckRollup": [_green],
                "labels": [{"name": AUTOMERGE_LABEL}]},              # review/required-check block
        "106": {"mergeStateStatus": "CLEAN", "statusCheckRollup": [_green],
                "labels": [{"name": AUTOMERGE_LABEL},
                           {"name": "risk/manual-review-required"}]},  # router-flagged -> human only
    }
    _fake = lambda pr: _FAKE.get(str(pr))            # unknown PR -> None -> fail closed

    def _raises(pr):                                 # lookup error -> fail closed
        raise RuntimeError("simulated gh/network failure")

    cases = [
        # EP-03 conditional merge — the new behavior (lookup injected):
        ("Bash", {"command": "gh pr merge 100 --squash"}, False, _fake),                 # CLEAN+green+label -> ALLOW
        ("PowerShell", {"command": "gh pr merge 100 --squash --delete-branch"}, False, _fake),
        ("Bash", {"command": f"gh pr merge https://github.com/{REPO_SLUG}/pull/100"}, False, _fake),  # URL form -> ALLOW
        ("Bash", {"command": "gh pr merge 101"}, True, _fake),                            # missing opt-in label
        ("Bash", {"command": "gh pr merge 102"}, True, _fake),                            # not CLEAN (UNSTABLE)
        ("Bash", {"command": "gh pr merge 103"}, True, _fake),                            # pending check
        ("Bash", {"command": "gh pr merge 104"}, True, _fake),                            # empty checkset
        ("Bash", {"command": "gh pr merge 105"}, True, _fake),                            # BLOCKED
        ("Bash", {"command": "gh pr merge 106"}, True, _fake),                            # router manual-review label -> human only
        ("Bash", {"command": "gh pr merge 999"}, True, _fake),                            # unknown PR -> lookup None
        ("Bash", {"command": "gh pr merge 100"}, True, _raises),                          # lookup raises -> fail closed
        ("PowerShell", {"command": "gh pr merge"}, True, _fake),                          # no explicit PR number
        ("Bash", {"command": "gh pr merge 9 --squash"}, True, _fake),                     # 9 not in fake -> fail closed
        ("Bash", {"command": f"gh api -X PUT repos/{REPO_SLUG}/pulls/9/merge"}, True, _fake),  # api form always manual
        ("Bash", {"command": f"gh pr merge 100 --repo {REPO_SLUG} --squash"}, False, _fake),  # explicit own-repo -> ALLOW
        ("Bash", {"command": "gh pr merge 100 --repo someone/else"}, True, _fake),        # foreign repo -> fail closed
        ("Bash", {"command": "gh pr merge 100 -R other/repo"}, True, _fake),              # foreign repo (-R) -> fail closed
        ("Bash", {"command": "gh pr merge 100 && git push origin main"}, True, _fake),    # merge ALLOWED, push-to-main still blocks
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
        # ALLOW: lane push (the per-lane PR flow)
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
    for i, (tn, ti, expect, *rest) in enumerate(cases, 1):
        lookup = rest[0] if rest else _fake
        got, reason = decide(tn, ti, lookup=lookup)
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
        if "EP-03 merge blocked" in reason:
            pr_m = re.search(r"PR (\d+)", reason)
            pr_ref = pr_m.group(1) if pr_m else "<PR#>"
            # Repo-scoped + absolute: a human can paste this in any PowerShell
            # window from any directory to land the PR.
            hint = (
                "  -> To land it manually (PowerShell, from any directory):\n"
                "    gh pr merge %s --squash --delete-branch --repo %s\n"
            ) % (pr_ref, REPO_SLUG)
        sys.stderr.write(_BLOCK_MSG % (reason, hint) + "\n")
        sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
