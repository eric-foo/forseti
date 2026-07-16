#!/usr/bin/env python3
"""Smallest-Complete-Intervention reminder hook (advisory, never blocks).

WHY THIS EXISTS
  The Smallest Complete Intervention (SCI) rule lives in AGENTS.md, near the top
  of a large instruction surface. Over a long session -- and especially while
  authoring durable artifacts, where scope creep is most tempting -- SCI can drift
  out of active context. This hook re-injects the SCI rule at the COMMIT boundary,
  right before Claude commits durable artifacts, so the rule is top-of-mind at the
  moment scope is locked in -- the cheapest point to still amend if the change crept
  past "smallest complete."

  Placement note: this is a PreToolUse hook matched on the shell tools and gated to
  `git commit`, so it fires ONLY for commits Claude itself runs through the Bash /
  PowerShell tool. A human committing in their own terminal is not seen -- add a real
  git pre-commit hook if you need to cover that path too.

  The rule is OWNED by AGENTS.md (-> "Smallest Complete Intervention"). To spare a
  fetch round-trip, this hook carries the rule's text INLINE as a verbatim mirror:
  the full definition -- including the cleanup/speculation clause -- rides in the
  reminder. KEEP `_SCI_VERBATIM` IN SYNC with that AGENTS.md section; if the section
  changes, update the constant.

BOUNDARY
  Advisory only. Emits `additionalContext` and ALWAYS exits 0; it never blocks a
  commit and makes no validation/readiness claim. Forward-only and low-noise: it
  fires ONLY when a `git commit` has durable-artifact changes pending in the tree,
  and stays silent for code-only / scratch / config commits.

SCOPE (in: durable artifacts; out: code/scratch/config)
  In  : docs/{decisions,product,prompts,workflows,migration,hygiene,review-inputs,
        review-outputs}/, .agents/workflow-overlay/, forseti/product/
  Out : anything containing _scratch; docs/_inbox/; .agents/skills/; .claude/;
        forseti-harness/ (and any path not under an in-scope prefix, e.g. .agents/hooks/).
  Pending changes are read from `git status --porcelain` (staged, unstaged, or
  untracked), so the nudge fires whether files were staged in a separate step or in
  the same `git add -A && git commit` one-liner.

MODES
  remind_sci.py --hook       PreToolUse hook (reads stdin JSON): if the command is a
                             `git commit` touching durable artifacts, emit reminder; exit 0
  remind_sci.py --selftest   pure-function scope / commit-detect cases; exit 0/1
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hooklib import (  # noqa: E402  (sys.path pin must precede the import)
    EXCLUDED_DOC_PREFIXES,
    DURABLE_DOC_PREFIXES,
    GIT_PREFIX,
    porcelain_paths,
    repo_root,
    shell_segments,
    to_relposix,
)

# Durable artifact folders whose creation/edit warrants the SCI nudge: the
# shared durable-docs base plus forseti/product/ (product artifacts also lock
# scope in, but sit outside the retrieval-metadata applicability list).
IN_SCOPE_PREFIXES = DURABLE_DOC_PREFIXES + ("forseti/product/",)

# Subtrees excluded even under an in-scope prefix (scratch, skill copies, config, code).
EXCLUDED_PREFIXES = EXCLUDED_DOC_PREFIXES

# VERBATIM mirror of the "Smallest Complete Intervention" section of AGENTS.md,
# inlined (not a pointer) so the full rule rides in the reminder with no fetch.
# KEEP IN SYNC with AGENTS.md -- if that section changes, update this text.
_SCI_VERBATIM = """`Complete` is load-bearing. Do not underfix to minimize diff, ceremony, or
visible change; a slightly larger fix is correct when required for durable,
coherent, non-fragile completion.

Prefer the biggest COMPLETE move you can still fully verify and the owner
can still steer in one pass -- not a thin smoke-test slice that proves
plumbing and defers the real capability. Over-slicing is its own
compounding cost: the deferrals pile up and rot, and each slice burns a
full plan/review/steer cycle. Slice deliberately only when the move is
high-lock-in or irreversible (probe first) or you genuinely need real
output to design the rest (harvest before cook) -- never just to look safe.

`Smallest` is also load-bearing. Do not add unrelated cleanup, speculative
abstractions, broad rewrites, extra workflow ceremony, or nice-to-have
improvements.

Weigh subtraction equally with addition. Additive fixes feel safe --
nothing visibly breaks -- so unchecked drift runs additive and rules,
steps, and surface only grow. When choosing the intervention, give
removing or simplifying an existing rule, step, artifact, or special case
the same standing as adding a new one, and when both satisfy the request,
prefer the one that leaves the smaller total surface. This is a
solution-choice rule inside the bound request: it never authorizes
speculative cleanup beyond it, and removals keep their evidence gates.

Watch for ceremony debt: the recurring process cost a change installs when
it adds a required step, preflight, gate, receipt, field, checklist, sync
obligation, or review pass that every future work unit must pay. A change
that is small in diff can still carry a large recurring toll. That toll is
downstream lock-in under the rule below, not a free addition: prefer the
path that does not add it, and when the requested outcome genuinely needs
a recurring step, name what each future work unit pays and what real
defect class it catches so the owner can weigh the toll before it becomes
standing.

When two candidate paths both satisfy the current request under this rule,
prefer the one with materially lower downstream lock-in -- the durable data,
schema, interface, or workflow shape that would be irreversible, costly to
roll back, or costly to maintain. Take the higher-lock-in path only when a
benefit necessary to the current request outweighs that structural cost; if
so, pause and surface the tradeoff for a decision before proceeding. This
narrows the choice among already-complete paths only; it never authorizes
speculative cleanup, future-proofing, or broader scope.

Whenever the user or instructions say **"smallest complete X"** -- including
phrases like **smallest complete fix, patch, edit, rewrite, refactor, review,
or answer** -- interpret it as **X performed under the Smallest complete
intervention rule above.**"""

REMINDER = (
    "SCI reminder (advisory, not blocking) -- make this a smallest complete change. "
    "The Smallest Complete Intervention rule (verbatim from AGENTS.md):\n\n"
    + _SCI_VERBATIM
)

# --- git commit detection (shared segment parsing from _hooklib; the hard
# guard keeps its own copy deliberately -- see _hooklib's standalone exception) ---
# Self-imposed ceiling on the `git status` call, kept below the hook's settings.json
# timeout so a slow git never trips a harness-level kill.
GIT_TIMEOUT = 6
_COMMIT = re.compile(GIT_PREFIX + r"commit\b", re.I)


def in_scope(relposix: str) -> bool:
    """True if this path is a durable artifact whose write warrants the SCI nudge.

    Pure function (testable). Exclusions win over inclusions; a path under no
    in-scope prefix is out of scope (so code under .agents/hooks/ stays silent).
    """
    if not relposix:
        return False
    if "_scratch" in relposix:
        return False
    if any(relposix.startswith(x) for x in EXCLUDED_PREFIXES):
        return False
    return any(relposix.startswith(x) for x in IN_SCOPE_PREFIXES)


def _is_git_commit(command: str) -> bool:
    """True if any shell segment of `command` is a `git commit` invocation. Quoted
    args are dropped first so a commit message (or an `echo "git commit"`) cannot
    false-match; segments are split so `git add -A && git commit` is still seen."""
    return any(_COMMIT.search(seg) for seg in shell_segments(command))


def _durable_from_porcelain(porcelain: str, root: Path) -> list[str]:
    """Repo-relative durable-artifact paths parsed from `git status --porcelain`.
    Pure (testable): porcelain parsing is shared (_hooklib.porcelain_paths, which
    keeps a rename/copy's destination); the same in_scope filter the write
    boundary used is applied on top."""
    hits = []
    for path in porcelain_paths(porcelain):
        rel = to_relposix(path, root)
        if rel and in_scope(rel):
            hits.append(rel)
    return hits


def _changed_durable_artifacts(root: Path) -> list[str]:
    """Durable-artifact paths with changes pending in the worktree, via one
    `git status --porcelain` call. Empty on any git error/timeout -- this hook is
    advisory and must never block or crash a commit on its own failure."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain"],
            capture_output=True, text=True, timeout=GIT_TIMEOUT,
        )
    except Exception:
        return []
    if out.returncode != 0:
        return []
    return _durable_from_porcelain(out.stdout or "", root)


def run_hook(root: Path) -> int:
    """PreToolUse hook: read the about-to-run shell command from stdin JSON; if it is
    a `git commit` with durable-artifact changes pending, inject the SCI reminder as
    additionalContext BEFORE the commit runs. Always exit 0 (advisory; never blocks)."""
    try:
        data = json.loads(sys.stdin.read() or "{}")
        command = (data.get("tool_input") or {}).get("command")
    except (ValueError, AttributeError):
        return 0  # malformed payload -> stay silent, never block
    if not command or not _is_git_commit(command):
        return 0
    hits = sorted(set(_changed_durable_artifacts(root)))
    if not hits:
        return 0  # code-only / scratch / config commit -> stay silent
    listed = ", ".join(hits[:8])
    more = "" if len(hits) <= 8 else " (+%d more)" % (len(hits) - 8)
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": "%s\n\n(committing durable artifacts: %s%s)"
                    % (REMINDER, listed, more),
                }
            }
        )
    )
    return 0


def selftest() -> int:
    ok = True
    root = repo_root()

    # The reminder promises a verbatim mirror of the owning SCI section. Keep
    # that promise mechanically fail-capable when AGENTS.md changes again.
    try:
        agents_text = (root / "AGENTS.md").read_text(encoding="utf-8")
        sci_source = (
            agents_text.split("## Smallest Complete Intervention", 1)[1]
            .split("### Problem Integrity", 1)[0]
            .strip()
        )
        mirror_ok = _SCI_VERBATIM.strip() == sci_source
    except (OSError, IndexError):
        mirror_ok = False
    if not mirror_ok:
        ok = False
    print(("PASS" if mirror_ok else "FAIL") + "  sci-verbatim mirror")

    scope_cases = [
        ("decision doc in scope", "docs/decisions/foo_v0.md", True),
        ("product artifact in scope", "forseti/product/spines/x/y_v0.md", True),
        ("overlay in scope", ".agents/workflow-overlay/x.md", True),
        ("migration doc in scope", "docs/migration/plan_v0.md", True),
        ("harness code out of scope", "forseti-harness/schemas/case_models.py", False),
        ("hook code out of scope", ".agents/hooks/remind_sci.py", False),
        ("scratch excluded", "docs/decisions/_scratch/tmp.md", False),
        ("inbox excluded", "docs/_inbox/note.md", False),
        ("project config excluded", ".claude/settings.json", False),
        ("repo-root file out of scope", "README.md", False),
        ("empty path", "", False),
    ]
    for label, rel, exp in scope_cases:
        got = in_scope(rel)
        status = "PASS" if got == exp else "FAIL"
        if got != exp:
            ok = False
        print("%s  in_scope   %-30s got=%s" % (status, label, got))

    commit_cases = [
        ("plain commit", "git commit -m 'x'", True),
        ("add && commit one-liner", "git add -A && git commit -m \"msg\"", True),
        ("commit with -C / --amend", "git -C . commit --amend", True),
        ("staged; then commit", "git add docs/x.md; git commit -m 'y'", True),
        ("status is not a commit", "git status", False),
        ("log grep is not a commit", "git log --grep=commit", False),
        ("quoted mention only", "echo 'git commit'", False),
        ("push is not a commit", "git push origin my-lane", False),
    ]
    for label, cmd, exp in commit_cases:
        got = _is_git_commit(cmd)
        status = "PASS" if got == exp else "FAIL"
        if got != exp:
            ok = False
        print("%s  is_commit  %-30s got=%s" % (status, label, got))

    porcelain = (
        " M docs/decisions/foo_v0.md\n"
        "?? forseti/product/spines/x/y_v0.md\n"
        "A  .agents/hooks/remind_sci.py\n"
        "R  docs/decisions/old.md -> docs/decisions/new_v0.md\n"
        " M README.md\n"
        " M docs/_inbox/note.md\n"
    )
    expect = [
        "docs/decisions/foo_v0.md",
        "docs/decisions/new_v0.md",
        "forseti/product/spines/x/y_v0.md",
    ]
    got_paths = sorted(_durable_from_porcelain(porcelain, root))
    p_ok = got_paths == sorted(expect)
    if not p_ok:
        ok = False
    print("%s  porcelain  durable-only filter         got=%s"
          % ("PASS" if p_ok else "FAIL", got_paths))

    print()
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    if "--hook" in argv:
        return run_hook(repo_root())
    print("Usage: remind_sci.py --hook | --selftest")
    return 0  # advisory tool: unknown args -> exit 0, never block


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # never block a write on an internal error
        sys.stderr.write("remind_sci: internal error, allowing: %s\n" % exc)
        sys.exit(0)
