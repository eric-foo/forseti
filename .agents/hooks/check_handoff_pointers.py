#!/usr/bin/env python3
"""Handoff-pointer resolution gate (EP-36): handoff-packet paths referenced in
changed durable docs must resolve in the same tree, or the pointer line must
carry an explicit resolution pin or exemption marker.

RULE AUTHORITY
  .agents/workflow-overlay/validation-gates.md -> "Current Gates" ->
  Handoff-pointer resolution gate. This checker references that rule and never
  restates it. EP handle: EP-36 in
  docs/decisions/overlay_enforcement_placement_classification_v0.md.

WHAT THIS ENFORCES (shape only)
  A handoff packet is a cold-lane required read. Twice-observed failure class:
  a packet authored on an unmerged lane branch (e.g.
  docs/workflows/yt_shorts_grid_tier_assessment_handoff_v0.md, reachable only
  on its authoring branch) was referenced by filed prompts that landed on
  main, so receiving agents and delegated reviewers starting cold from main
  could not resolve it. The mechanically checkable shell: in every CHANGED
  durable `.md` file (diff base...HEAD), each referenced handoff-packet path

    docs/workflows/*handoff*.md        (basename contains "handoff")
    docs/prompts/handoffs/*.md         (the handoff prompt family)

  must exist in the same tree, UNLESS the pointer line carries
    - an explicit resolution pin: the word "branch", "PR #<n>", or an
      "origin/<ref>" token (a cold reader gets a fetch handle), or
    - an exemption marker: "does not exist yet", "created on first",
      "not retrieval-indexed", "nonresolving:", or superseded/removed/deleted
      wording (historical references to retired packets).
  Pinned/exempt pointers are counted as annotated debt, never failures.

  Because the gate runs on the landing PR's tree, the practical consequence is
  the doctrine rule: a handoff packet merges no later than the first
  main-bound artifact that points at it (same PR is fine), or the pointer pins
  the authoring branch explicitly.

WHAT THIS DOES NOT DO (PLACEMENT IS NOT AUTHORITY)
  - It never proves a resolved packet's content is current, that a pinned
    branch still exists, or that the packet was the right source to cite.
  - It cannot see couriers that never land in the repo (chat bodies, PR
    comments, ignored docs/_inbox/ scratch) -- those stay resident judgment
    under prompt-orchestration.md.
  - A write-time PostToolUse advisory is intentionally NOT built: the defect
    is a merge-topology property (packet lives on a different unmerged
    branch), invisible at the write boundary where the packet usually exists
    in the author's own tree.

DETECTION CONTRACT (mirrors check_review_routing.py / check_dcp_receipt.py)
  base ref priority: $FORSETI_DIFF_BASE (exact CI event SHA); else
  $GITHUB_BASE_REF -> origin/<ref>; else --base <ref>; else origin/main.
  Diff is three-dot `base...HEAD`, name-status; scanned files are
  the added/modified/rename-or-copy-destination `.md` paths still present in
  the tree, excluding `_scratch`, `docs/_inbox/`, and `node_modules`. NO
  HEAD~1 fallback. If the base cannot be resolved or git fails, fail OPEN
  (exit 0, loud warning) -- the universal Forseti infra-gap stance; in CI the
  base is always present (fetch-depth: 0). Fail-open is for INFRASTRUCTURE
  GAPS ONLY: in --strict and --selftest an unexpected internal exception exits
  1 (the GATE FAIL bucket, validation-gates.md); advisory modes fail open on
  internal error. Forward-only by construction: only the current diff is
  gated, never historical backlog (see --audit for that view).

MODES
  check_handoff_pointers.py --strict [--base <ref>]  CI gate; exit 1 on findings
  check_handoff_pointers.py --check  [--base <ref>]  same scan, human-readable, exit 0
  check_handoff_pointers.py --audit                  whole-corpus backlog view, exit 0 (never a gate)
  check_handoff_pointers.py --selftest               pure-function cases; exit per pass/fail

REGISTRATION (.github/workflows/ci.yml, after the review-routing step)
  - name: handoff-pointer resolution (packets resolve where referenced)
    run: python .agents/hooks/check_handoff_pointers.py --strict
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Callable, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hooklib import (  # noqa: E402  (sys.path pin must precede the import)
    git_out,
    repo_root,
)


# ---------------------------------------------------------------------------
# Pure decision core (testable)
# ---------------------------------------------------------------------------

# Handoff-packet path tokens, forward- or backslash-separated, backticked or
# bare (the regex does not care about surrounding markup). Two canonical
# homes only; hygiene/scratch handoff files are deliberately out of scope.
_HANDOFF_TOKEN_RE = re.compile(
    r"(?:docs[/\\]workflows[/\\][\w.\-/\\]*handoff[\w.\-]*\.md"
    r"|docs[/\\]prompts[/\\]handoffs[/\\][\w.\-/\\]+\.md)"
)

# Resolution pins: vocabulary that hands a cold reader a fetch handle.
_PIN_RE = re.compile(
    r"\bbranch\b|\bPR\s*#\d+|\borigin/[\w./\-]+", re.IGNORECASE
)

# Exemption markers: established house vocabulary plus retired-packet wording.
_EXEMPT_MARKERS = (
    "does not exist yet",
    "created on first",
    "not retrieval-indexed",
    "nonresolving:",
    "supersed",   # supersedes / superseded
    "removed",
    "deleted",
)


def extract_handoff_pointers(line: str) -> list[str]:
    """Handoff-packet path tokens on one line, normalized to forward slashes.

    Pure function (testable).
    """
    return [m.group(0).replace("\\", "/") for m in _HANDOFF_TOKEN_RE.finditer(line)]


def line_is_exempt(line: str) -> bool:
    """True if the pointer line carries a resolution pin or exemption marker.

    Shape only: the pin's truth (the branch still exists, the PR is the right
    one) stays resident judgment. Pure function (testable).
    """
    lower = line.lower()
    if any(marker in lower for marker in _EXEMPT_MARKERS):
        return True
    return _PIN_RE.search(line) is not None


class Finding(NamedTuple):
    source: str   # referencing file (repo-relative, forward slashes)
    lineno: int
    token: str    # the unresolved handoff-packet path


def evaluate_lines(
    rel_source: str,
    lines: list[str],
    path_exists: Callable[[str], bool],
) -> tuple[list[Finding], int]:
    """Scan one file's lines. Returns (findings, exempt_count).

    path_exists is injected so the core stays pure (testable).
    """
    findings: list[Finding] = []
    exempt = 0
    for i, line in enumerate(lines, 1):
        tokens = extract_handoff_pointers(line)
        if not tokens:
            continue
        if line_is_exempt(line):
            exempt += sum(1 for t in tokens if not path_exists(t))
            continue
        for tok in tokens:
            if not path_exists(tok):
                findings.append(Finding(rel_source, i, tok))
    return findings, exempt


def is_scanned_file(rel_path: str) -> bool:
    """True if a changed file is in the gate's scanned set.

    Pure function (testable).
    """
    p = rel_path.replace("\\", "/")
    if not p.endswith(".md"):
        return False
    if "_scratch" in p or "node_modules" in p:
        return False
    if p.startswith("docs/_inbox/") or "/_inbox/" in p:
        return False
    return True


def parse_name_status(lines: list[str]) -> list[str]:
    """Present-in-tree changed paths from `git diff --name-status` output:
    added, modified, and rename/copy DESTINATIONS (sources may be gone).

    Pure function (testable).
    """
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
        # D rows: skip -- nothing left in the tree to scan
    return present


# ---------------------------------------------------------------------------
# Git plumbing (infra-gap fail-open)
# ---------------------------------------------------------------------------

def _git(root: Path, args: list[str], timeout: int = 15) -> tuple[int, str]:
    """Run a git command; return (returncode, stdout). Never raises.

    Thin adapter over the shared _hooklib.git_out (keeps this file's 15s
    default). git_out returns (1, "") on launch failure/timeout instead of
    (-1, ""); callers here only test rc != 0, so the distinction is inert."""
    return git_out(root, args, timeout=timeout)


def resolve_base_ref(cli_base: str | None) -> str:
    ci_base = os.environ.get("FORSETI_DIFF_BASE", "").strip()
    if ci_base:
        return ci_base
    gh_base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if gh_base:
        return "origin/%s" % gh_base
    if cli_base:
        return cli_base
    return "origin/main"


def changed_scanned_files(root: Path, base_ref: str) -> list[str] | None:
    """Repo-relative scanned .md paths changed in base...HEAD. None = infra gap."""
    if _git(root, ["rev-parse", "--verify", "--quiet", "HEAD"])[0] != 0:
        return None
    if _git(root, ["rev-parse", "--verify", "--quiet", base_ref])[0] != 0:
        return None
    code, out = _git(root, ["diff", "--name-status", "%s...HEAD" % base_ref])
    if code != 0:
        return None
    return [p for p in parse_name_status(out.splitlines()) if is_scanned_file(p)]


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------

def _disk_exists(root: Path) -> Callable[[str], bool]:
    def exists(token: str) -> bool:
        return (root / Path(token.replace("/", os.sep))).exists()
    return exists


def scan_files(root: Path, rel_paths: list[str]) -> tuple[list[Finding], int]:
    findings: list[Finding] = []
    exempt = 0
    exists = _disk_exists(root)
    for rel in rel_paths:
        fpath = root / Path(rel.replace("/", os.sep))
        try:
            lines = fpath.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        f, e = evaluate_lines(rel.replace("\\", "/"), lines, exists)
        findings.extend(f)
        exempt += e
    return findings, exempt


def corpus_files(root: Path) -> list[str]:
    """All scanned-set .md files in the tree (for --audit)."""
    out: list[str] = []
    skip_dirs = {".git", "node_modules", "__pycache__", "_inbox"}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if d not in skip_dirs and "_scratch" not in d
        ]
        for fname in filenames:
            if not fname.endswith(".md"):
                continue
            rel = (Path(dirpath) / fname).relative_to(root).as_posix()
            if is_scanned_file(rel):
                out.append(rel)
    return sorted(out)


# ---------------------------------------------------------------------------
# Mode runners
# ---------------------------------------------------------------------------

def _print_findings(findings: list[Finding], exempt: int) -> None:
    for f in findings:
        print("  %s:%d  ->  unresolved handoff-packet pointer: %s"
              % (f.source, f.lineno, f.token))
    print("pinned/exempt handoff pointers: %d (annotated debt, not failures)" % exempt)


def run_strict(root: Path, cli_base: str | None) -> int:
    base_ref = resolve_base_ref(cli_base)
    rel_paths = changed_scanned_files(root, base_ref)
    if rel_paths is None:
        sys.stderr.write(
            "check_handoff_pointers --strict: WARNING git diff vs %s unavailable; "
            "failing OPEN (infra gap, not a pass)\n" % base_ref
        )
        return 0
    findings, exempt = scan_files(root, rel_paths)
    if findings:
        print("check_handoff_pointers --strict: %d finding(s) vs %s"
              % (len(findings), base_ref))
        _print_findings(findings, exempt)
        print(
            "rule: a handoff packet must resolve in the tree where the pointer lands\n"
            "      (merge the packet first or in the same PR), or the pointer line\n"
            "      must pin the source explicitly (branch/PR #/origin/<ref>) or carry\n"
            "      an exemption marker. Authority: .agents/workflow-overlay/"
            "validation-gates.md -> Handoff-pointer resolution gate."
        )
        return 1
    print("check_handoff_pointers --strict: OK (0 findings in %d changed file(s) vs %s)"
          % (len(rel_paths), base_ref))
    print("pinned/exempt handoff pointers: %d (annotated debt, not failures)" % exempt)
    return 0


def run_check(root: Path, cli_base: str | None) -> int:
    base_ref = resolve_base_ref(cli_base)
    rel_paths = changed_scanned_files(root, base_ref)
    if rel_paths is None:
        print("check_handoff_pointers --check: git diff vs %s unavailable; nothing scanned"
              % base_ref)
        return 0
    findings, exempt = scan_files(root, rel_paths)
    print("check_handoff_pointers --check (advisory, exit 0): %d finding(s) in %d "
          "changed file(s) vs %s" % (len(findings), len(rel_paths), base_ref))
    _print_findings(findings, exempt)
    return 0


def run_audit(root: Path) -> int:
    rel_paths = corpus_files(root)
    findings, exempt = scan_files(root, rel_paths)
    print("check_handoff_pointers --audit (whole-corpus backlog view, exit 0; "
          "never a gate):")
    print("  scanned .md files: %d" % len(rel_paths))
    print("  unresolved handoff-packet pointers: %d" % len(findings))
    _print_findings(findings, exempt)
    return 0


# ---------------------------------------------------------------------------
# Selftest
# ---------------------------------------------------------------------------

def selftest() -> int:
    ok = True

    def check(label: str, got: object, expected: object) -> None:
        nonlocal ok
        status = "PASS" if got == expected else "FAIL"
        if got != expected:
            ok = False
        print("%s  %-58s  expect=%r got=%r" % (status, label, expected, got))

    # --- extract_handoff_pointers ---
    print("--- extract_handoff_pointers ---")
    check("backtick workflows handoff",
          extract_handoff_pointers(
              "read `docs/workflows/yt_shorts_grid_tier_assessment_handoff_v0.md`."),
          ["docs/workflows/yt_shorts_grid_tier_assessment_handoff_v0.md"])
    check("bare workflows handoff, trailing period stripped by regex",
          extract_handoff_pointers(
              "Commissioned by docs/workflows/x_handoff_v0.md."),
          ["docs/workflows/x_handoff_v0.md"])
    check("prompts/handoffs family (no 'handoff' needed in basename)",
          extract_handoff_pointers(
              "- `docs/prompts/handoffs/consume_capture_corpus_v0.md`"),
          ["docs/prompts/handoffs/consume_capture_corpus_v0.md"])
    check("non-handoff workflows file not matched",
          extract_handoff_pointers("see docs/workflows/forseti_repo_map_v0.md"),
          [])
    check("hygiene handoff out of scope",
          extract_handoff_pointers("docs/hygiene/foo_handoff_v0.md"),
          [])
    check("directory reference without .md not matched",
          extract_handoff_pointers("file it under docs/prompts/handoffs/"),
          [])
    check("anchor suffix stops at .md",
          extract_handoff_pointers("docs/workflows/a_handoff_v0.md#section"),
          ["docs/workflows/a_handoff_v0.md"])
    check("backslash separators normalized",
          extract_handoff_pointers(r"docs\workflows\a_handoff_v0.md"),
          ["docs/workflows/a_handoff_v0.md"])
    check("two pointers on one line",
          extract_handoff_pointers(
              "docs/workflows/a_handoff_v0.md and docs/prompts/handoffs/b_v0.md"),
          ["docs/workflows/a_handoff_v0.md", "docs/prompts/handoffs/b_v0.md"])
    check("hash-pin suffix after .md ignored",
          extract_handoff_pointers("docs/workflows/a_handoff_v0.md@abc123"),
          ["docs/workflows/a_handoff_v0.md"])

    # --- line_is_exempt ---
    print()
    print("--- line_is_exempt ---")
    check("branch pin",
          line_is_exempt("- packet on branch claude/yt-grid (unmerged)"), True)
    check("PR pin",
          line_is_exempt("decided in docs/prompts/handoffs/x_v0.md (on PR #66)"), True)
    check("origin ref pin",
          line_is_exempt("reachable only on origin/claude/yt-grid-tier-assessment-handoff"), True)
    check("does not exist yet",
          line_is_exempt("docs/workflows/a_handoff_v0.md -- does not exist yet"), True)
    check("nonresolving annotation",
          line_is_exempt("docs/workflows/a_handoff_v0.md # nonresolving: retired"), True)
    check("superseded wording",
          line_is_exempt("supersedes: docs/prompts/handoffs/old_v0.md"), True)
    check("removed wording",
          line_is_exempt("prior version, removed in the defork pass"), True)
    check("plain pointer line not exempt",
          line_is_exempt("read `docs/workflows/a_handoff_v0.md` before starting"), False)
    check("the word 'branching' does not pin (word boundary)",
          line_is_exempt("branching logic reads docs/workflows/a_handoff_v0.md"), False)

    # --- evaluate_lines ---
    print()
    print("--- evaluate_lines ---")
    exists_none = lambda _t: False  # noqa: E731
    exists_all = lambda _t: True    # noqa: E731
    f, e = evaluate_lines("docs/prompts/reviews/p_v0.md",
                          ["read docs/workflows/a_handoff_v0.md now"], exists_none)
    check("missing packet -> finding",
          (len(f), f[0].token if f else None, e),
          (1, "docs/workflows/a_handoff_v0.md", 0))
    f, e = evaluate_lines("docs/prompts/reviews/p_v0.md",
                          ["read docs/workflows/a_handoff_v0.md now"], exists_all)
    check("resolving packet -> no finding", (len(f), e), (0, 0))
    f, e = evaluate_lines("docs/prompts/reviews/p_v0.md",
                          ["packet docs/workflows/a_handoff_v0.md on branch lane-x"],
                          exists_none)
    check("missing but pinned -> exempt count, no finding", (len(f), e), (0, 1))
    f, e = evaluate_lines("docs/prompts/reviews/p_v0.md",
                          ["no pointers on this line"], exists_none)
    check("no pointers -> nothing", (len(f), e), (0, 0))

    # --- is_scanned_file ---
    print()
    print("--- is_scanned_file ---")
    check("durable doc md", is_scanned_file("docs/prompts/reviews/p_v0.md"), True)
    check("product corpus md", is_scanned_file("forseti/product/spines/x/y_v0.md"), True)
    check("root AGENTS.md", is_scanned_file("AGENTS.md"), True)
    check("python file", is_scanned_file(".agents/hooks/check_handoff_pointers.py"), False)
    check("inbox scratch excluded", is_scanned_file("docs/_inbox/tmp_v0.md"), False)
    check("_scratch excluded", is_scanned_file("docs/_scratch/x.md"), False)

    # --- parse_name_status ---
    print()
    print("--- parse_name_status ---")
    check("A/M kept, D dropped, R keeps destination",
          parse_name_status([
              "A\tdocs/prompts/reviews/new_v0.md",
              "M\tdocs/workflows/a_handoff_v0.md",
              "D\tdocs/old_v0.md",
              "R100\tdocs/from_v0.md\tdocs/to_v0.md",
              "noise",
          ]),
          ["docs/prompts/reviews/new_v0.md", "docs/workflows/a_handoff_v0.md",
           "docs/to_v0.md"])

    # --- resolve_base_ref ---
    print()
    print("--- resolve_base_ref ---")
    saved_ci_base = os.environ.pop("FORSETI_DIFF_BASE", None)
    saved = os.environ.pop("GITHUB_BASE_REF", None)
    try:
        check("base default", resolve_base_ref(None), "origin/main")
        check("base cli", resolve_base_ref("some-branch"), "some-branch")
        os.environ["GITHUB_BASE_REF"] = "develop"
        check("base env wins", resolve_base_ref("ignored"), "origin/develop")
    finally:
        if saved is not None:
            os.environ["GITHUB_BASE_REF"] = saved
        else:
            os.environ.pop("GITHUB_BASE_REF", None)
        if saved_ci_base is not None:
            os.environ["FORSETI_DIFF_BASE"] = saved_ci_base
        else:
            os.environ.pop("FORSETI_DIFF_BASE", None)

    print()
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _arg_value(argv: list[str], flag: str) -> str | None:
    if flag in argv:
        idx = argv.index(flag)
        if idx + 1 < len(argv):
            return argv[idx + 1]
    return None


def main(argv: list[str]) -> int:
    # Forced-exception probe: proves the __main__ gating handler
    # (forseti-harness/tests/unit/test_hook_internal_error_gating.py).
    if "--force-internal-error" in argv:
        raise RuntimeError("forced internal error (probe)")
    if "--selftest" in argv:
        return selftest()
    root = repo_root()
    cli_base = _arg_value(argv, "--base")
    if "--strict" in argv:
        return run_strict(root, cli_base)
    if "--check" in argv:
        return run_check(root, cli_base)
    if "--audit" in argv:
        return run_audit(root)
    print("Usage: check_handoff_pointers.py --strict [--base <ref>] | --check [--base <ref>] | --audit | --selftest")
    print("  --strict    CI gate: exit 1 if a changed durable doc references an")
    print("              unresolved, unpinned handoff-packet path")
    print("  --check     same scan, human-readable, always exit 0")
    print("  --audit     whole-corpus backlog view, always exit 0 (never a gate)")
    print("  --selftest  pure-function self-check")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        # GATE FAIL bucket in gating modes (validation-gates.md): an internal
        # checker bug must not read as a green gate. Advisory modes fail open
        # so a bug never bricks the agent.
        sys.stderr.write("check_handoff_pointers: internal error: %s\n" % exc)
        gating = "--strict" in sys.argv[1:] or "--selftest" in sys.argv[1:]
        sys.exit(1 if gating else 0)
