#!/usr/bin/env python3
"""Smallest-Complete-Intervention reminder hook (advisory, never blocks).

WHY THIS EXISTS
  The Smallest Complete Intervention (SCI) rule lives in AGENTS.md, near the top
  of a large instruction surface. Over a long session -- and especially while
  authoring durable artifacts, where scope creep is most tempting -- SCI can drift
  out of active context. This hook re-injects the SCI rule at the write boundary,
  RIGHT BEFORE a durable artifact is created or edited (PreToolUse), so the rule is
  top-of-mind exactly when the change is being made.

  The rule is OWNED by AGENTS.md (-> "Smallest Complete Intervention"). To spare a
  fetch round-trip, this hook carries the rule's text INLINE as a verbatim mirror:
  the full definition -- including the cleanup/speculation clause -- rides in the
  reminder. KEEP `_SCI_VERBATIM` IN SYNC with that AGENTS.md section; if the section
  changes, update the constant.

BOUNDARY
  Advisory only. Emits `additionalContext` and ALWAYS exits 0; it never blocks a
  write and makes no validation/readiness claim. Forward-only and low-noise: it
  fires ONLY for writes under the durable artifact folders and stays silent for
  code, scratch, skill copies, and project config.

SCOPE (in: durable artifacts; out: code/scratch/config)
  In  : docs/{decisions,product,prompts,workflows,migration,hygiene,review-inputs,
        review-outputs}/, .agents/workflow-overlay/, orca/product/
  Out : anything containing _scratch; docs/_inbox/; .agents/skills/; .claude/;
        orca-harness/ (and any path not under an in-scope prefix, e.g. .agents/hooks/).

MODES
  remind_sci.py --hook       PreToolUse hook (reads stdin JSON); emit reminder; exit 0
  remind_sci.py --selftest   pure-function scope cases; exit 0/1
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Durable artifact folders whose creation/edit warrants the SCI nudge.
IN_SCOPE_PREFIXES = (
    "docs/decisions/",
    "docs/product/",
    "docs/prompts/",
    "docs/workflows/",
    "docs/migration/",
    "docs/hygiene/",
    "docs/review-inputs/",
    "docs/review-outputs/",
    ".agents/workflow-overlay/",
    "orca/product/",
)

# Subtrees excluded even under an in-scope prefix (scratch, skill copies, config, code).
EXCLUDED_PREFIXES = (
    "docs/_inbox/",
    ".agents/skills/",
    ".claude/",
    "orca-harness/",
)

# VERBATIM mirror of the "Smallest Complete Intervention" section of AGENTS.md,
# inlined (not a pointer) so the full rule rides in the reminder with no fetch.
# KEEP IN SYNC with AGENTS.md -- if that section changes, update this text.
_SCI_VERBATIM = """`Complete` is load-bearing. Do not underfix to minimize diff, ceremony, or
visible change; a slightly larger fix is correct when required for durable,
coherent, non-fragile completion.

`Smallest` is also load-bearing. Do not add unrelated cleanup, speculative
abstractions, broad rewrites, extra workflow ceremony, or nice-to-have
improvements.

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


def repo_root() -> Path:
    """Repo root, derived from this file's location (.agents/hooks/<this>)."""
    return Path(__file__).resolve().parents[2]


def to_relposix(target: str, root: Path) -> str | None:
    """Repo-relative POSIX path for a target, or None if outside the repo."""
    p = Path(target)
    if p.is_absolute():
        try:
            return p.resolve().relative_to(root).as_posix()
        except (ValueError, OSError):
            return None
    s = Path(target).as_posix()
    return s[2:] if s.startswith("./") else s  # strip a literal leading "./"


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


def run_hook(root: Path) -> int:
    """PreToolUse hook: read the about-to-be-written file from stdin JSON; if it is
    a durable artifact, inject the SCI reminder as additionalContext BEFORE the
    write proceeds. Always exit 0 (advisory; never blocks the write)."""
    try:
        data = json.loads(sys.stdin.read() or "{}")
        file_path = (data.get("tool_input") or {}).get("file_path")
    except (ValueError, AttributeError):
        return 0  # malformed payload -> stay silent, never block
    if not file_path:
        return 0
    rel = to_relposix(file_path, root)
    if rel is None or not in_scope(rel):
        return 0
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "additionalContext": "%s\n\n(artifact: %s)" % (REMINDER, rel),
                }
            }
        )
    )
    return 0


def selftest() -> int:
    ok = True
    cases = [
        ("decision doc in scope", "docs/decisions/foo_v0.md", True),
        ("product artifact in scope", "orca/product/spines/x/y_v0.md", True),
        ("overlay in scope", ".agents/workflow-overlay/x.md", True),
        ("migration doc in scope", "docs/migration/plan_v0.md", True),
        ("harness code out of scope", "orca-harness/schemas/case_models.py", False),
        ("hook code out of scope", ".agents/hooks/remind_sci.py", False),
        ("scratch excluded", "docs/decisions/_scratch/tmp.md", False),
        ("inbox excluded", "docs/_inbox/note.md", False),
        ("project config excluded", ".claude/settings.json", False),
        ("repo-root file out of scope", "README.md", False),
        ("empty path", "", False),
    ]
    for label, rel, exp in cases:
        got = in_scope(rel)
        status = "PASS" if got == exp else "FAIL"
        if got != exp:
            ok = False
        print("%s  %-34s got=%s" % (status, label, got))
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
