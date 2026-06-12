#!/usr/bin/env python3
"""SessionStart hook — emit a compact lane-state capsule (advisory).

WHAT THIS DOES
  At session start (startup / resume / clear / compact), prints a short
  capsule of mechanical lane state so a new or re-oriented lane does not
  re-derive it turn by turn: repo root, branch, HEAD, last 3 commit subjects,
  dirty/untracked counts, config-surface dirt, and pointers to the two
  source-loading entry artifacts (repo map, overlay README). Replaces the
  repeated session-open recovery ritual with deterministic output
  (ratified config proposal P3, 2026-06-12).

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
from pathlib import Path

# Config-surface paths whose dirt matters to every lane (repo-relative POSIX).
CONFIG_SURFACE = ("CLAUDE.md", "AGENTS.md", ".claude", ".agents")

ENTRY_POINTERS = (
    "docs/workflows/orca_repo_map_v0.md",
    ".agents/workflow-overlay/README.md",
)


def repo_root() -> Path:
    """Repo root, derived from this file's location (.agents/hooks/<this>)."""
    return Path(__file__).resolve().parents[2]


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
    """Paths from config-surface-scoped porcelain output (pure function)."""
    out: list[str] = []
    for line in porcelain.splitlines():
        if len(line) < 4:
            continue
        path = line[3:]
        if " -> " in path:  # rename: take the destination
            path = path.split(" -> ", 1)[1]
        path = path.strip().strip('"')
        if path and path not in out:
            out.append(path)
    return out


def build_capsule(source: str, root: str, branch: str, head: str,
                  subjects: list[str], counts: tuple[int, int],
                  cfg_dirty: list[str]) -> str:
    """Render the capsule (pure function). Mechanical state only — no claims."""
    lines = [
        "[lane-state capsule | source=%s]" % (source or "unknown"),
        "repo: %s" % root,
        "branch: %s @ %s" % (branch or "UNKNOWN", head or "UNKNOWN"),
    ]
    if subjects:
        lines.append("recent: " + " | ".join(subjects[:3]))
    lines.append("tree: %d modified, %d untracked" % counts)
    lines.append("config-surface dirt (CLAUDE.md/AGENTS.md/.claude/.agents): "
                 + (", ".join(cfg_dirty) if cfg_dirty else "clean"))
    lines.append("source-loading entry points: " + " ; ".join(ENTRY_POINTERS)
                 + " (read overlay README before project work, per AGENTS.md)")
    lines.append("capsule is observed git state only -- not doctrine, "
                 "validation, readiness, or lane authority.")
    return "\n".join(lines)


def _git(root: Path, *args: str) -> str:
    """Run a git command with a short timeout; '' on any failure (fail open)."""
    try:
        res = subprocess.run(["git", "-C", str(root), *args],
                             capture_output=True, text=True, timeout=5)
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return ""
    return res.stdout if res.returncode == 0 else ""


def gather(root: Path, source: str) -> str:
    branch = _git(root, "rev-parse", "--abbrev-ref", "HEAD").strip()
    head = _git(root, "log", "-1", "--format=%h %s").strip()
    subjects = [s for s in _git(root, "log", "-3", "--format=%s").splitlines() if s]
    counts = tree_counts(_git(root, "status", "--porcelain"))
    cfg = config_dirt(_git(root, "status", "--porcelain", "--", *CONFIG_SURFACE))
    return build_capsule(source, str(root), branch, head, subjects, counts, cfg)


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
    capsule = build_capsule("startup", "/r", "main", "abc fix", ["s1", "s2"],
                            (1, 2), [])
    shape_ok = (
        capsule.startswith("[lane-state capsule | source=startup]")
        and "branch: main @ abc fix" in capsule
        and "tree: 1 modified, 2 untracked" in capsule
        and "clean" in capsule
        and len(capsule.splitlines()) <= 12
    )
    ok = cases_ok and shape_ok
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
