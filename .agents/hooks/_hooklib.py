#!/usr/bin/env python3
"""_hooklib -- shared helpers for the .agents/hooks checkers.

WHY THIS EXISTS
  The wired hook scripts each carried private copies of the same helpers:
  repo-root derivation, repo-relative POSIX path normalization, tool-event
  parsing (including Codex apply_patch headers), the git subprocess wrapper,
  `git status --porcelain` parsing, shell-segment splitting, and the durable-
  docs scope vocabulary. The copies had already diverged -- rooted-path
  handling differed between checkers (the FIND-01 class), and the scope lists
  differed by accident as well as by design. One definition here removes the
  accidental drift; deliberate per-checker scope deltas stay in each checker,
  expressed against the shared base so the divergence is visible.

DELIBERATE EXCEPTION -- guard_protected_actions.py stays import-free.
  The hard EP-03/EP-01 blocker keeps its own copies of these helpers by
  design: an ImportError in an advisory checker costs one advisory, but in
  the guard it would disable the only hard gate at whole-script level
  (including its fail-CLOSED merge-authorization path). Do not "fix" the
  guard's duplication by importing this module.

IMPORT PATTERN (works when the sibling script runs as a file from any cwd
and when it is loaded via importlib.util.spec_from_file_location):

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import _hooklib

BOUNDARY
  Helpers only. This module owns no rule; each checker names its own rule
  authority. Nothing here is validation, readiness, or source-of-truth
  promotion.

MODES
  _hooklib.py --selftest   pure-function cases; exit 0/1
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# --- scope vocabulary ---------------------------------------------------------

# Durable folders the retrieval-metadata contract enumerates under
# "Applicability" (.agents/workflow-overlay/retrieval-metadata.md). This is the
# BASE durable-docs vocabulary; a checker with a deliberately different scope
# derives from it (or declares its own list with a comment pointing here) so
# the delta is visible instead of accidental.
DURABLE_DOC_PREFIXES = (
    ".agents/workflow-overlay/",
    "docs/decisions/",
    "docs/product/",
    "docs/prompts/",
    "docs/review-inputs/",
    "docs/review-outputs/",
    "docs/workflows/",
    "docs/migration/",
    "docs/hygiene/",
)

# Subtrees excluded even when nested under an in-scope prefix (mirrors the
# contract's own exclusions: scratch, skill copies, project config, code).
EXCLUDED_DOC_PREFIXES = (
    "docs/_inbox/",
    ".agents/skills/",
    ".claude/",
    "forseti-harness/",
)


# --- paths ----------------------------------------------------------------------

def repo_root() -> Path:
    """Repo root, derived from this file's location (.agents/hooks/<this>)."""
    return Path(__file__).resolve().parents[2]


def to_relposix(target: str, root: Path) -> str | None:
    """Repo-relative POSIX path for a target, or None if it cannot be tied to
    the repo.

    - Absolute paths resolve against `root`; outside the repo -> None.
    - Relative paths are assumed repo-relative. Strip only a LITERAL leading
      "./" prefix; NOT lstrip("./"), which is a character-set strip that would
      also eat the leading dot of ".agents/..." paths (silently dropping
      overlay files out of scope).
    - A rooted-but-not-absolute path ("/docs/..." on Windows, where it carries
      no drive) is never treated as repo-relative -> None (FIND-01 class).
    """
    if not target:
        return None
    p = Path(target)
    if p.is_absolute():
        try:
            return p.resolve().relative_to(root).as_posix()
        except (ValueError, OSError):
            return None
    s = p.as_posix()
    s = s[2:] if s.startswith("./") else s
    if s.startswith("/"):
        return None
    return s


# --- tool-event parsing ---------------------------------------------------------

# Codex apply_patch headers (Codex reports patch edits as tool_name
# "apply_patch" with the patch text in tool_input, not Claude-style Write/Edit).
_PATCH_FILE_RE = re.compile(
    r"^\*\*\* (?:Add|Update|Delete) File: (.+)$|^\*\*\* Move to: (.+)$",
    re.MULTILINE,
)


def read_event() -> dict:
    """Tool event parsed from stdin JSON; {} on malformed or non-dict payload."""
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except (ValueError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def patch_paths(text: str) -> list[str]:
    """Write-target paths named by Codex apply_patch headers in `text`."""
    out: list[str] = []
    for match in _PATCH_FILE_RE.finditer(text or ""):
        candidate = match.group(1) or match.group(2)
        if candidate:
            out.append(candidate.strip())
    return out


def candidate_paths(data: dict) -> list[str]:
    """Write-target paths from a Claude/Codex-like tool event, deduped in order.

    Claude-style Write/Edit/NotebookEdit payloads carry tool_input.file_path /
    .path / .notebook_path; Codex apply_patch payloads carry the patch text in
    tool_input.command / .patch / .input.
    """
    tool_input = data.get("tool_input") if isinstance(data, dict) else None
    if not isinstance(tool_input, dict):
        return []
    out: list[str] = []
    for key in ("file_path", "path", "notebook_path"):
        value = tool_input.get(key)
        if isinstance(value, str) and value:
            out.append(value)
    for key in ("command", "patch", "input"):
        value = tool_input.get(key)
        if isinstance(value, str) and value:
            out.extend(patch_paths(value))
    deduped: list[str] = []
    for path in out:
        if path not in deduped:
            deduped.append(path)
    return deduped


# --- git plumbing ---------------------------------------------------------------

def git_out(root: Path, args: list[str], timeout: int | None = None) -> tuple[int, str]:
    """Run git in `root`; (returncode, stdout). (1, "") on launch failure/timeout."""
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=timeout,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return 1, ""
    return result.returncode, result.stdout


def git_lines(root: Path, args: list[str], timeout: int | None = None) -> list[str]:
    """Non-empty stripped stdout lines from git; [] on any failure."""
    rc, out = git_out(root, args, timeout=timeout)
    if rc != 0:
        return []
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def resolve_base_ref(cli_base: str | None) -> str:
    """Diff-base ref for the forward-only gates, in contract priority order:
    $FORSETI_DIFF_BASE (exact CI event SHA) -> $GITHUB_BASE_REF as
    "origin/<ref>" -> explicit CLI base -> "origin/main". No HEAD~1 fallback --
    that would see only the last commit of a multi-commit lane.

    Shared home for the copies the diff-scoped checkers carried; a checker
    with a deliberately different precedence (e.g. bare GITHUB_BASE_REF
    handling) keeps its own copy with a comment naming the delta."""
    ci_base = os.environ.get("FORSETI_DIFF_BASE", "").strip()
    if ci_base:
        return ci_base
    gh_base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if gh_base:
        return "origin/%s" % gh_base
    if cli_base:
        return cli_base
    return "origin/main"


def parse_name_status(lines: list[str]) -> list[str]:
    """Present-in-tree changed paths from `git diff --name-status` output:
    added, modified, and rename/copy DESTINATIONS (sources may be gone).
    D rows are skipped -- nothing left in the tree to scan.

    Pure function (testable)."""
    present: list[str] = []
    for ln in lines:
        parts = [p.strip() for p in ln.split("\t")]
        if len(parts) < 2:
            continue
        status = parts[0]
        if status.startswith(("R", "C")) and len(parts) >= 3:
            present.append(parts[2])
        elif status.startswith(("A", "M")):
            present.append(parts[1])
    return present


def porcelain_paths(porcelain: str) -> list[str]:
    """Paths from `git status --porcelain` v1 output, deduped in order.

    2-char status, a space, then the path; a rename/copy is shown as
    'old -> new' and the committed path is the DESTINATION. Quotes stripped."""
    out: list[str] = []
    for line in (porcelain or "").splitlines():
        if len(line) < 4:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        path = path.strip().strip('"')
        if path and path not in out:
            out.append(path)
    return out


# --- shell-command parsing ------------------------------------------------------

# `git` invocation allowing -C <path> / -c k=v / global flags before the
# subcommand. (guard_protected_actions.py keeps its own copy deliberately --
# see the module docstring's standalone exception.)
GIT_PREFIX = r"\bgit\b(?:\s+-C\s+\S+|\s+-c\s+\S+|\s+--?\S+)*\s+"
_SEP = re.compile(r"&&|\|\||[;\n|]")
_QUOTED = re.compile(r"\"[^\"]*\"|'[^']*'")


def shell_segments(command: str) -> list[str]:
    """Shell segments of `command` with quoted args dropped first (so a commit
    MESSAGE or an `echo "git commit"` is never mistaken for the command itself),
    then split on separators (so `git add -A && git commit` is still seen)."""
    return _SEP.split(_QUOTED.sub(" ", command or ""))


# --- once-per-session state -----------------------------------------------------

def _session_state_path(name: str, session_id: str) -> str:
    key = hashlib.sha1(
        ("%s|%s" % (name, session_id or "nosession")).encode("utf-8")
    ).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "forseti_hookonce_%s.json" % key)


def mark_session_once(name: str, session_id: str) -> bool:
    """True the FIRST time (name, session_id) is marked this session; False after.

    Tempdir marker file (same pattern as check_token_burn's rung state). Fails
    OPEN: on any I/O error it returns True, so a state bug degrades to the
    pre-dedupe behavior (remind every time), never to silence."""
    path = _session_state_path(name, session_id)
    try:
        if os.path.exists(path):
            return False
        with open(path, "w", encoding="utf-8") as handle:
            json.dump({"name": name}, handle)
        return True
    except OSError:
        return True


# --- selftest -------------------------------------------------------------------

def selftest() -> int:
    ok = True

    def check(label: str, got, expect) -> None:
        nonlocal ok
        passed = got == expect
        if not passed:
            ok = False
        print("%s  %-58s got=%r" % ("PASS" if passed else "FAIL", label, got))

    root = repo_root()

    # to_relposix
    check("absolute under root", to_relposix(str(root / "docs" / "x.md"), root), "docs/x.md")
    check("absolute outside root", to_relposix(str(root.parent / "elsewhere_x.md"), root), None)
    check("relative passthrough", to_relposix("docs/decisions/x.md", root), "docs/decisions/x.md")
    check("literal ./ stripped", to_relposix("./docs/x.md", root), "docs/x.md")
    check("leading dot kept (no lstrip corruption)",
          to_relposix(".agents/workflow-overlay/x.md", root), ".agents/workflow-overlay/x.md")
    check("rooted non-absolute -> None (FIND-01)", to_relposix("/docs/decisions/x.md", root), None)
    check("empty -> None", to_relposix("", root), None)
    check("backslashes normalized", to_relposix("docs\\decisions\\x.md", root),
          "docs/decisions/x.md")

    # candidate_paths / patch_paths
    check("file_path picked",
          candidate_paths({"tool_input": {"file_path": "a.md"}}), ["a.md"])
    check("notebook_path picked",
          candidate_paths({"tool_input": {"notebook_path": "n.ipynb"}}), ["n.ipynb"])
    check("patch headers parsed",
          candidate_paths({"tool_input": {"command":
              "*** Begin Patch\n*** Update File: docs/a.md\n@@\n-x\n+y\n"
              "*** Move to: docs/b.md\n*** End Patch\n"}}),
          ["docs/a.md", "docs/b.md"])
    check("file_path + patch deduped",
          candidate_paths({"tool_input": {"file_path": "docs/a.md",
                                          "patch": "*** Add File: docs/a.md\n"}}),
          ["docs/a.md"])
    check("empty tool_input", candidate_paths({"tool_input": {}}), [])
    check("non-dict tool_input", candidate_paths({"tool_input": "bad"}), [])
    check("non-dict event", candidate_paths([]), [])

    # resolve_base_ref
    saved_ci = os.environ.pop("FORSETI_DIFF_BASE", None)
    saved_gh = os.environ.pop("GITHUB_BASE_REF", None)
    try:
        check("base default", resolve_base_ref(None), "origin/main")
        check("base cli", resolve_base_ref("some-branch"), "some-branch")
        os.environ["GITHUB_BASE_REF"] = "develop"
        check("base GITHUB_BASE_REF wins over cli", resolve_base_ref("ignored"),
              "origin/develop")
        os.environ["FORSETI_DIFF_BASE"] = "abc123"
        check("base FORSETI_DIFF_BASE wins over all", resolve_base_ref("ignored"),
              "abc123")
    finally:
        for key, saved in (("FORSETI_DIFF_BASE", saved_ci),
                           ("GITHUB_BASE_REF", saved_gh)):
            if saved is not None:
                os.environ[key] = saved
            else:
                os.environ.pop(key, None)

    # parse_name_status
    check(
        "name-status: A/M kept, D dropped, R keeps destination",
        parse_name_status([
            "A\tdocs/new.md",
            "M\tdocs/mod.md",
            "D\tdocs/gone.md",
            "R100\tdocs/from.md\tdocs/to.md",
            "noise",
        ]),
        ["docs/new.md", "docs/mod.md", "docs/to.md"],
    )

    # porcelain_paths
    check("porcelain basic", porcelain_paths(" M docs/a.md\n?? docs/b.md\n"),
          ["docs/a.md", "docs/b.md"])
    check("porcelain rename destination",
          porcelain_paths("R  docs/old.md -> docs/new.md\n"), ["docs/new.md"])
    check("porcelain junk line skipped", porcelain_paths("xx\n"), [])
    check("porcelain quoted path", porcelain_paths(' M "docs/a b.md"\n'), ["docs/a b.md"])

    # shell_segments
    segs = shell_segments("git add -A && git commit -m 'git push'")
    check("segments split", len(segs), 2)
    check("quoted dropped", any("push" in s for s in segs), False)
    commit_re = re.compile(GIT_PREFIX + r"commit\b", re.I)
    check("commit seen in second segment", bool(commit_re.search(segs[1])), True)
    check("echo-quoted commit not seen",
          any(commit_re.search(s) for s in shell_segments("echo 'git commit'")), False)

    # mark_session_once
    sid = "hooklib-selftest-%d" % os.getpid()
    path = _session_state_path("selftest", sid)
    if os.path.exists(path):
        os.unlink(path)
    try:
        check("first mark -> True", mark_session_once("selftest", sid), True)
        check("second mark -> False", mark_session_once("selftest", sid), False)
    finally:
        if os.path.exists(path):
            os.unlink(path)

    print()
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    print("Usage: _hooklib.py --selftest  (shared helper module; not a hook)")
    sys.exit(0)
