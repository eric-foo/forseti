#!/usr/bin/env python3
"""SessionStart hook — emit a compact lane-state capsule (advisory).

WHAT THIS DOES
  At session start (startup / resume / clear / compact), prints a short
  capsule of mechanical lane state so a new or re-oriented lane does not
  re-derive it turn by turn: repo root, branch, HEAD, last 3 commit subjects,
  dirty/untracked counts, config-surface dirt, doctrine state relative to
  last-fetched origin/main, and pointers to the two source-loading entry
  artifacts (repo map, overlay README). Replaces the repeated session-open
  recovery ritual with deterministic output (ratified config proposal P3,
  2026-06-12).

  doctrine state field: compares AGENTS.md and .agents/ against origin/main
  using `git diff --name-only origin/main -- AGENTS.md .agents`. Reports
  DIFFERS (with up to 3 filenames) when non-empty, matches when empty, or
  omits the line entirely on git failure (fail open).

WHY (enforcement placement)
  Mechanical state recovery belongs in a deterministic substrate, not in model
  attention (.agents/workflow-overlay/validation-gates.md -> Enforcement
  Placement). The capsule reports observed git state only: it loads no
  doctrine, judges no lane fit, and asserts nothing beyond git output.

HARD BOUNDARY — report only, never block. Exit 0 always; fails OPEN.
  Output is capped by construction (single short capsule). Every git call has
  a short timeout so a wedged git can never stall session start.

MODES
  session_context_capsule.py --hook      SessionStart hook (stdin JSON, exit 0)
  session_context_capsule.py --check     human-readable run against live tree
  session_context_capsule.py --selftest  pure-decision cases

REGISTRATION (.claude/settings.json; SessionStart takes NO matcher)
  "SessionStart": [ { "hooks": [ { "type": "command",
      "command": "python \"$CLAUDE_PROJECT_DIR/.agents/hooks/session_context_capsule.py\" --hook",
      "timeout": 10 } ] } ]
  Hooks load at session start; restart the session after editing settings.
"""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hooklib import (  # noqa: E402  (sys.path pin must precede the import)
    porcelain_paths,
    repo_root,
)

# Config-surface paths whose dirt matters to every lane (repo-relative POSIX).
CONFIG_SURFACE = ("CLAUDE.md", "AGENTS.md", ".claude", ".agents")

ENTRY_POINTERS = (
    "docs/workflows/forseti_repo_map_v0.md",
    ".agents/workflow-overlay/README.md",
)


def tree_counts(porcelain: str) -> tuple[int, int]:
    """(modified_or_staged, untracked) counts from `git status --porcelain`.

    Pure function (testable). Untracked lines start with '??'; everything else
    non-empty counts as modified/staged."""
    modified = untracked = 0
    for line in porcelain.splitlines():
        if len(line) < 4:
            continue
        if line.startswith("??"):
            untracked += 1
        else:
            modified += 1
    return modified, untracked


def config_dirt(porcelain: str) -> list[str]:
    """Paths from config-surface-scoped porcelain output (pure function).

    Parsing is shared (_hooklib.porcelain_paths, which keeps a rename's
    destination)."""
    return porcelain_paths(porcelain)


def doctrine_lag_line(diff_output: str | None) -> str | None:
    """Return the doctrine-state capsule line (pure function).

    diff_output: stdout of `git diff --name-only origin/main -- AGENTS.md
    .agents`, or None to signal git failure (fail open -> omit line).
    Returns a single ASCII line, or None when git failed.
    """
    if diff_output is None:
        return None  # fail open: omit the line
    names = [n for n in diff_output.splitlines() if n.strip()]
    if not names:
        return "doctrine state: matches last-fetched origin/main"
    preview = ", ".join(names[:3])
    return "doctrine state: DIFFERS from last-fetched origin/main (%d file%s: %s)" % (
        len(names), "s" if len(names) != 1 else "", preview)


def build_capsule(source: str, root: str, branch: str, head: str,
                  subjects: list[str], counts: tuple[int, int],
                  cfg_dirty: list[str],
                  doctrine: str | None = None,
                  retrieval_health: str | None = None,
                  ontology_expansion: str | None = None) -> str:
    """Render the capsule (pure function). Mechanical state only — no claims."""
    lines = [
        "[lane-state capsule | source=%s]" % (source or "unknown"),
        "repo: %s" % root,
        "branch: %s @ %s" % (branch or "UNKNOWN", head or "UNKNOWN"),
    ]
    if branch and branch != "main":
        lines.append(
            "not on main (on '%s') -- verify on-main state via "
            "`git show origin/main:<path>` or `git ls-tree origin/main`, "
            "not a working-tree/file search" % branch)
    if subjects:
        lines.append("recent: " + " | ".join(subjects[:3]))
    lines.append("tree: %d modified, %d untracked" % counts)
    lines.append("config-surface dirt (CLAUDE.md/AGENTS.md/.claude/.agents): "
                 + (", ".join(cfg_dirty) if cfg_dirty else "clean"))
    if doctrine is not None:
        lines.append(doctrine)
    if retrieval_health is not None:
        lines.append(retrieval_health)
    if ontology_expansion is not None:
        lines.append(ontology_expansion)
    lines.append("source-loading entry points: " + " ; ".join(ENTRY_POINTERS)
                 + " (read overlay README before project work, per AGENTS.md)")
    lines.append("capsule is observed git state only -- not doctrine, "
                 "validation, readiness, or lane authority.")
    return "\n".join(lines)


# Kept local: deliberate delta from _hooklib.git_out (--no-optional-locks, 5s timeout, stdout-str-or-'' contract).
def _git(root: Path, *args: str) -> str:
    """Run a git command with a short timeout; '' on any failure (fail open).

    --no-optional-locks: gather() runs these read-only calls concurrently, and
    without it a `git status` may take index.lock for an opportunistic refresh
    and make a sibling call fail (which would silently misreport tree state).
    """
    try:
        res = subprocess.run(["git", "--no-optional-locks", "-C", str(root), *args],
                             capture_output=True, text=True, timeout=5)
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return ""
    return res.stdout if res.returncode == 0 else ""


def retrieval_health_line(root: Path) -> str | None:
    """Call header_index.py --health --oneline; return the output line, or None on error.

    Uses a 5-second timeout. Fails open (returns None) on any error so a broken
    index never stalls session start.  Never inlines a second os.walk here —
    delegates entirely to the hook.

    Pure subprocess call (testable by mocking subprocess.run; not a pure
    function since it shells out, but it is the single authoritative call site).
    """
    hook = root / ".agents" / "hooks" / "header_index.py"
    try:
        res = subprocess.run(
            ["python", str(hook), "--health", "--oneline"],
            capture_output=True, text=True, timeout=5,
        )
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
        return None
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return None


def ontology_expansion_line(root: Path) -> str | None:
    """Call check_ontology_expansion.py --health --oneline; return the line, or None.

    Returns None when nothing is due, the backlog is absent, or any error occurs
    (fail-open) so the capsule simply omits the line. 5-second timeout; never
    inlines the backlog logic here -- delegates entirely to the hook (the single
    authoritative call site), same pattern as retrieval_health_line above.
    """
    hook = root / ".agents" / "hooks" / "check_ontology_expansion.py"
    try:
        res = subprocess.run(
            ["python", str(hook), "--health", "--oneline"],
            capture_output=True, text=True, timeout=5,
        )
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
        return None
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return None


def gather(root: Path, source: str) -> str:
    # All eight child calls are independent reads; run them concurrently so
    # session start waits for the slowest child, not the serial sum. Each
    # child keeps its own timeout and fail-open contract unchanged.
    with ThreadPoolExecutor(max_workers=8) as pool:
        f_branch = pool.submit(_git, root, "rev-parse", "--abbrev-ref", "HEAD")
        f_head = pool.submit(_git, root, "log", "-1", "--format=%h %s")
        f_subjects = pool.submit(_git, root, "log", "-3", "--format=%s")
        f_status = pool.submit(_git, root, "status", "--porcelain")
        f_cfg = pool.submit(_git, root, "status", "--porcelain", "--", *CONFIG_SURFACE)
        f_diff = pool.submit(_git, root, "diff", "--name-only", "origin/main",
                             "--", "AGENTS.md", ".agents")
        f_health = pool.submit(retrieval_health_line, root)
        f_expansion = pool.submit(ontology_expansion_line, root)
    branch = f_branch.result().strip()
    head = f_head.result().strip()
    subjects = [s for s in f_subjects.result().splitlines() if s]
    counts = tree_counts(f_status.result())
    cfg = config_dirt(f_cfg.result())
    raw_diff = f_diff.result()
    # _git returns "" on failure; use None sentinel only when git itself errors
    # (we cannot distinguish "" output from error via _git's current contract,
    # so treat the empty-string-on-error case as fail-open: an empty diff output
    # means "matches", which is the safe/non-alarming default).
    doctrine = doctrine_lag_line(raw_diff)
    health = f_health.result()
    expansion = f_expansion.result()
    return build_capsule(source, str(root), branch, head, subjects, counts, cfg,
                         doctrine=doctrine, retrieval_health=health,
                         ontology_expansion=expansion)


def run_hook(root: Path) -> int:
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        data = {}
    source = data.get("source", "") if isinstance(data, dict) else ""
    print(gather(root, source))
    return 0


def selftest() -> int:
    porc = " M a.md\n?? b.md\n?? c.md\nxx\n"
    cases_ok = (
        tree_counts(porc) == (1, 2)
        and tree_counts("") == (0, 0)
        and config_dirt("?? .agents/hooks/x.py\n") == [".agents/hooks/x.py"]
        and config_dirt("R  old.md -> AGENTS.md\n") == ["AGENTS.md"]
        and config_dirt("") == []
    )
    # doctrine_lag_line: non-empty diff (3 files)
    dl_nonempty = doctrine_lag_line("AGENTS.md\n.agents/hooks/x.py\n.agents/other.py\n")
    # doctrine_lag_line: empty diff (matches)
    dl_empty = doctrine_lag_line("")
    # doctrine_lag_line: git failure (None -> omit)
    dl_fail = doctrine_lag_line(None)
    doctrine_ok = (
        dl_nonempty is not None
        and "DIFFERS" in dl_nonempty
        and "3 files" in dl_nonempty
        and "AGENTS.md" in dl_nonempty
        and dl_empty == "doctrine state: matches last-fetched origin/main"
        and dl_fail is None
    )
    # capsule with doctrine line present (non-empty diff case)
    capsule_with = build_capsule("startup", "/r", "main", "abc fix", ["s1", "s2"],
                                 (1, 2), [], doctrine=dl_nonempty)
    # capsule with doctrine omitted (git-failure case)
    capsule_without = build_capsule("startup", "/r", "main", "abc fix", ["s1", "s2"],
                                    (1, 2), [], doctrine=None)
    # capsule with retrieval_health line
    capsule_with_health = build_capsule("startup", "/r", "main", "abc fix", ["s1"],
                                        (0, 0), [],
                                        doctrine=None,
                                        retrieval_health="retrieval health: 3 missing headers, 1 orphan")
    # capsule without retrieval_health line (None)
    capsule_no_health = build_capsule("startup", "/r", "main", "abc fix", ["s1"],
                                      (0, 0), [],
                                      doctrine=None,
                                      retrieval_health=None)
    # capsule with ontology_expansion line
    capsule_with_expansion = build_capsule(
        "startup", "/r", "main", "abc fix", ["s1"], (0, 0), [],
        doctrine=None, retrieval_health=None,
        ontology_expansion="ontology expansion: 4 types due (Observation, TrendVector, Call, Reading)")
    # capsule without ontology_expansion line (None)
    capsule_no_expansion = build_capsule(
        "startup", "/r", "main", "abc fix", ["s1"], (0, 0), [],
        doctrine=None, retrieval_health=None, ontology_expansion=None)
    # capsule on a non-main branch (caution fires)
    capsule_off_main = build_capsule("startup", "/r", "feature-x", "abc fix", ["s1"],
                                     (0, 0), [])
    # capsule with empty branch (git failure -> caution suppressed, fail-open)
    capsule_empty_branch = build_capsule("startup", "/r", "", "abc fix", ["s1"],
                                         (0, 0), [])
    shape_ok = (
        capsule_with.startswith("[lane-state capsule | source=startup]")
        and "branch: main @ abc fix" in capsule_with
        and "tree: 1 modified, 2 untracked" in capsule_with
        and "clean" in capsule_with
        and "DIFFERS" in capsule_with
        and len(capsule_with.splitlines()) <= 15
        and "DIFFERS" not in capsule_without
        and len(capsule_without.splitlines()) <= 14
        and "retrieval health: 3 missing headers" in capsule_with_health
        and "retrieval health" not in capsule_no_health
        and "ontology expansion: 4 types due" in capsule_with_expansion
        and "ontology expansion" not in capsule_no_expansion
        and "not on main" in capsule_off_main
        and "feature-x" in capsule_off_main
        and "not on main" not in capsule_with
        and "not on main" not in capsule_empty_branch
    )
    ok = cases_ok and doctrine_ok and shape_ok
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    root = repo_root()
    if "--check" in argv:
        print(gather(root, "check"))
        return 0
    return run_hook(root)  # default / --hook: SessionStart hook mode


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:  # fail OPEN: a capsule bug must never stall a session
        sys.stderr.write("session_context_capsule: internal error, allowing: %s\n" % exc)
        sys.exit(0)
