#!/usr/bin/env python3
"""Retrieval-header boundary check (advisory, forward-only).

WHAT THIS ENFORCES
  Forseti's retrieval-header contract for durable human-authored workflow
  artifacts. The *rule* — which folders are in scope, the exclusions, the five
  core fields, and the controlled `authority_boundary: retrieval_only` value —
  is owned by:

      .agents/workflow-overlay/retrieval-metadata.md

  This script does NOT restate that rule. It is a thin structural tripwire that
  references the authority above. If the contract and this checker ever
  disagree, the contract wins and this checker is the stale party.

WHY THIS EXISTS (enforcement placement)
  The rule was previously carried only by instruction, so a capable agent could
  write a durable artifact with no retrieval header and nothing would notice at
  the moment the rule should fire. Per the Enforcement Placement principle in
      .agents/workflow-overlay/validation-gates.md  (-> "Enforcement Placement")
  a load-bearing rule that is mechanically checkable at a tool boundary is
  enforced at that boundary (a write-time hook + this portable checker), not
  left to actor memory. Judgment-based parts of the contract (is this really a
  "canonical" review input? is `scope` well written?) stay with the human/
  reviewer; this checker only trips on the deterministic shape.

SCOPE (forward-only, low false-positive by design)
  - Checks ONLY the paths handed to it. It never blind-scans the repository.
  - In scope: `*.md` under the durable folders the contract enumerates
    (.agents/workflow-overlay/, docs/decisions/, docs/product/, docs/prompts/,
    docs/review-inputs/, docs/review-outputs/, docs/workflows/, docs/migration/,
    docs/hygiene/).
  - Out of scope (silently skipped): everything else, plus directory README.md
    files, docs/_inbox/ scratch, skill copies (.agents/skills/, .claude/), and
    code (orca-harness/). These mirror the contract's own exclusions. Folders
    the contract does not enumerate (e.g. docs/research/, which carries embedded
    evidence units) are intentionally NOT in scope to keep false positives near
    zero; widen IN_SCOPE_PREFIXES if the contract's applicability list grows.
  - The structural check is deliberately shallow: it trips on a missing
    retrieval header, a non-`1` version, or an `authority_boundary` that is
    absent or not `retrieval_only`. It does not validate `artifact_role`,
    `scope`, or `use_when` wording — that is left to review (single-source).

MODES
  check_retrieval_header.py <path> [<path> ...]   advisory; warns, exit 0
  check_retrieval_header.py --strict <path> ...    exit 1 if any violation
  check_retrieval_header.py --staged [--strict]    check git-staged files
  check_retrieval_header.py --changed [--strict]   check changed + untracked
  check_retrieval_header.py --hook                 PostToolUse hook (reads
                                                   stdin JSON, always exit 0)
  check_retrieval_header.py --selftest             pure-function cases; exit 0/1

  Commit/CI gate (POSIX):   python3 .agents/hooks/check_retrieval_header.py --staged --strict
  Commit/CI gate (Windows): python  .agents/hooks/check_retrieval_header.py --staged --strict

This checker is advisory tooling, not validation, readiness, approval, or
source-of-truth promotion. A clean run does not prove an artifact is correct,
only that its retrieval header is structurally present.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# Authority this checker references (it does not restate the rule).
RULE_AUTHORITY = ".agents/workflow-overlay/retrieval-metadata.md"
PRINCIPLE = ".agents/workflow-overlay/validation-gates.md (Enforcement Placement)"

# Durable folders the contract enumerates under "Applicability". Forward slashes;
# matching is done on a POSIX-style repo-relative path.
IN_SCOPE_PREFIXES = (
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
EXCLUDED_PREFIXES = (
    "docs/_inbox/",
    ".agents/skills/",
    ".claude/",
    "orca-harness/",
)

HEAD_LINES = 80  # the header sits near the top, just after the H1 title

_VERSION_RE = re.compile(r"^\s*retrieval_header_version\s*:\s*(.+?)\s*$")
_BOUNDARY_RE = re.compile(r"^\s*authority_boundary\s*:\s*(.+?)\s*$")
_TOP_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:")

# Forbidden header keys (lifecycle / approval / validation STATUS leak). The
# retrieval header stays retrieval-only: it must not carry approval, validation,
# readiness, lifecycle, deployment, install, resolver, publication, or
# source-of-truth STATUS. Authority (not restated here):
#     .agents/workflow-overlay/retrieval-metadata.md  ("Forbidden Header Fields")
# Deliberately NOT included: edit_permission, review verdict, executor, status.
# Review-output and prompt frontmatter legitimately carry edit_permission /
# verdict / status under the review-lanes and prompt-orchestration conventions
# (verified against the corpus); this scan targets ONLY the status-leak keys,
# which no current in-scope header uses (born-green). Matching is exact-key,
# lowercased, against the header block's top-level keys -- never a body mention,
# a nested value, or a substring.
FORBIDDEN_HEADER_KEYS = frozenset({
    "approval", "approval_status", "approved",
    "validation", "validation_status", "validated", "proof_result",
    "readiness", "readiness_status",
    "lifecycle", "lifecycle_state", "lifecycle_status",
    "deployment", "deployment_status", "deployed",
    "install_status", "installed",
    "resolver", "resolver_status",
    "publication", "publication_status", "published",
    "source_of_truth", "source_of_truth_status", "sot_status",
})


def repo_root() -> Path:
    """Repo root, derived from this file's location (.agents/hooks/<this>)."""
    return Path(__file__).resolve().parents[2]


def to_relposix(target: str, root: Path) -> str | None:
    """Repo-relative POSIX path for a target, or None if outside the repo."""
    p = Path(target)
    if p.is_absolute():
        try:
            rel = p.resolve().relative_to(root)
        except (ValueError, OSError):
            return None
        return rel.as_posix()
    # Already relative -> assume relative to the repo root. Strip only a literal
    # leading "./" prefix; do NOT use lstrip("./"), which would also eat the
    # leading dot of paths like ".agents/..." (a character-set strip, not a
    # prefix strip) and silently drop overlay files out of scope.
    s = Path(target).as_posix()
    return s[2:] if s.startswith("./") else s


def scope_folder(relposix: str) -> str | None:
    """Return the in-scope folder prefix for a path, or None if out of scope."""
    if not relposix.endswith(".md"):
        return None
    if Path(relposix).name == "README.md":
        return None
    if any(relposix.startswith(x) for x in EXCLUDED_PREFIXES):
        return None
    for prefix in IN_SCOPE_PREFIXES:
        if relposix.startswith(prefix):
            return prefix
    return None


def _strip_value(raw: str) -> str:
    """Normalize a YAML scalar: drop a trailing comment and surrounding quotes."""
    val = raw.strip()
    if val and val[0] in "'\"":  # quoted scalar -> take inside the quotes
        q = val[0]
        end = val.find(q, 1)
        if end != -1:
            return val[1:end]
    val = val.split(" #", 1)[0].strip()  # inline comment on an unquoted scalar
    return val


def head_lines(path: Path) -> list[str] | None:
    """First HEAD_LINES lines of a file, or None if it can't be read."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    return text.splitlines()[:HEAD_LINES]


def header_block_top_keys(lines: list[str]) -> set[str]:
    """Top-level (column-0) keys, lowercased, inside the first ```yaml fence that
    contains `retrieval_header_version`. Empty set if there is no such header.

    Fence-scoped and column-0 only: a key nested under `use_when:`, a body
    heading, or a prose mention is never returned. Pure function (testable)."""
    in_yaml = False
    block: list[str] = []
    has_version = False
    for line in lines:
        s = line.strip()
        if s.startswith("```"):
            if not in_yaml and "yaml" in s.lower():
                in_yaml, block, has_version = True, [], False
                continue
            if in_yaml:
                if has_version:
                    break  # captured the header block
                in_yaml = False  # a different yaml block; keep looking
                continue
            continue
        if in_yaml:
            block.append(line)
            if line.strip().startswith("retrieval_header_version"):
                has_version = True
    if not has_version:
        return set()
    keys: set[str] = set()
    for line in block:
        if line[:1] not in (" ", "\t", "", "-", "#"):
            m = _TOP_KEY_RE.match(line)
            if m:
                keys.add(m.group(1).strip().lower())
    return keys


def header_problems_for_lines(lines: list[str]) -> list[str]:
    """Structural retrieval-header problems for already-read head lines (empty == ok).

    Scope-INDEPENDENT predicate: retrieval_header_version==1, authority_boundary==
    retrieval_only, and no forbidden status-leak key in the header block.
    check_relpath applies the scope gate then delegates here; the orca/ report path
    (header_index) applies this directly, so report-mode and strict share ONE
    predicate definition and cannot drift.
    """
    version_val = None
    boundary_val = None
    for line in lines:
        if version_val is None:
            m = _VERSION_RE.match(line)
            if m:
                version_val = _strip_value(m.group(1))
        if boundary_val is None:
            m = _BOUNDARY_RE.match(line)
            if m:
                boundary_val = _strip_value(m.group(1))

    problems: list[str] = []
    if version_val is None:
        problems.append("missing retrieval header (no `retrieval_header_version`)")
        return problems  # no header at all -> one primary signal, don't pile on
    if version_val != "1":
        problems.append(f"`retrieval_header_version` is `{version_val}`, expected `1`")
    if boundary_val is None:
        problems.append("header present but `authority_boundary` is missing")
    elif boundary_val != "retrieval_only":
        problems.append(
            f"`authority_boundary` is `{boundary_val}`, must be `retrieval_only`"
        )
    forbidden = sorted(FORBIDDEN_HEADER_KEYS & header_block_top_keys(lines))
    if forbidden:
        problems.append(
            "forbidden header field(s) %s -- the retrieval header stays "
            "retrieval-only (no approval/validation/readiness/lifecycle/deployment/"
            "install/resolver/publication/source-of-truth status; put such state in "
            "the artifact body, not the header)"
            % ", ".join("`%s`" % k for k in forbidden)
        )
    return problems


def check_relpath(relposix: str, root: Path) -> list[str]:
    """Return a list of structural problems for an in-scope file (empty == ok).

    Returns [] for out-of-scope or unreadable paths (advisory: never invent a
    problem we cannot see). Scope gate here; structural predicate delegated to
    header_problems_for_lines (shared with the orca/ report path).
    """
    folder = scope_folder(relposix)
    if folder is None:
        return []
    lines = head_lines(root / relposix)
    if lines is None:
        return []
    return header_problems_for_lines(lines)


def warning_for(relposix: str, problems: list[str]) -> str:
    detail = "; ".join(problems)
    return (
        f"{relposix}: {detail}. "
        f"Add the 5-field retrieval header per {RULE_AUTHORITY}. "
        f"If this artifact is excluded by that contract (scratch/_inbox, a "
        f"directory README, a skill copy, or code), no action is needed."
    )


def git_lines(root: Path, args: list[str]) -> list[str]:
    try:
        out = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, OSError):
        return []
    if out.returncode != 0:
        return []
    return [ln.strip() for ln in out.stdout.splitlines() if ln.strip()]


def staged_paths(root: Path) -> list[str]:
    return git_lines(root, ["diff", "--cached", "--name-only", "--diff-filter=ACMR"])


def changed_paths(root: Path) -> list[str]:
    seen: list[str] = []
    for args in (
        ["diff", "--name-only", "--diff-filter=ACMR"],
        ["diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        for p in git_lines(root, args):
            if p not in seen:
                seen.append(p)
    return seen


def collect_warnings(relpaths: list[str], root: Path) -> list[str]:
    warnings: list[str] = []
    for rel in relpaths:
        if rel is None:
            continue
        problems = check_relpath(rel, root)
        if problems:
            warnings.append(warning_for(rel, problems))
    return warnings


def run_hook(root: Path) -> int:
    """PostToolUse hook: read the touched file from stdin JSON, warn, exit 0."""
    try:
        data = json.loads(sys.stdin.read() or "{}")
        file_path = (data.get("tool_input") or {}).get("file_path")
    except (ValueError, AttributeError):
        return 0  # malformed payload -> stay silent, never block an edit
    if not file_path:
        return 0
    rel = to_relposix(file_path, root)
    if rel is None:
        return 0
    problems = check_relpath(rel, root)
    if not problems:
        return 0
    msg = (
        "Retrieval-header check (advisory, not blocking): "
        + warning_for(rel, problems)
        + f" Enforced at the write boundary per {PRINCIPLE}."
    )
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": msg,
                }
            }
        )
    )
    return 0


def selftest() -> int:
    """Pure-function cases for the shared header predicate. Exit 0 on pass, 1 on fail."""
    ok = True

    def check(label: str, got, exp):
        nonlocal ok
        status = "PASS" if got == exp else "FAIL"
        if got != exp:
            ok = False
        print("%s  %-52s got=%r" % (status, label, got))

    def hdr(*body: str) -> list[str]:
        return ["# Title", "", "```yaml", "retrieval_header_version: 1",
                *body, "authority_boundary: retrieval_only", "```"]

    # --- existing predicate still holds ---
    check("valid header passes",
          header_problems_for_lines(hdr("artifact_role: x", "scope: y", "use_when:", "  - a")), [])
    check("no header flagged",
          bool(header_problems_for_lines(["# T", "", "no yaml here"])), True)
    check("bad version flagged",
          any("version" in p for p in header_problems_for_lines(
              ["# T", "", "```yaml", "retrieval_header_version: 2",
               "authority_boundary: retrieval_only", "```"])), True)
    check("bad boundary flagged",
          any("authority_boundary" in p for p in header_problems_for_lines(
              ["# T", "", "```yaml", "retrieval_header_version: 1",
               "authority_boundary: open", "```"])), True)

    # --- new forbidden-status-key scan ---
    check("forbidden approval flagged",
          any("forbidden" in p for p in header_problems_for_lines(hdr("approval: granted"))), True)
    check("forbidden readiness flagged",
          any("forbidden" in p for p in header_problems_for_lines(hdr("readiness: ready"))), True)
    check("forbidden source_of_truth flagged",
          any("forbidden" in p for p in header_problems_for_lines(hdr("source_of_truth: yes"))), True)
    # legit review/prompt frontmatter keys are NOT forbidden (corpus reality)
    check("review/prompt keys not forbidden",
          header_problems_for_lines(hdr("artifact_role: x", "edit_permission: read-only",
                                        "reviewed_by: m", "status: done", "verdict: accept",
                                        "de_correlation_bar: cross_vendor_discovery")), [])
    # a forbidden WORD nested under use_when (not a top-level key) is NOT flagged
    check("nested mention not flagged",
          header_problems_for_lines(hdr("use_when:", "  - approval matters here")), [])

    # --- header_block_top_keys ---
    check("top key extracted", "approval" in header_block_top_keys(hdr("approval: x")), True)
    check("nested key not a top key",
          header_block_top_keys(hdr("use_when:", "  - approval matters")) & {"approval"}, set())
    check("no header -> empty keys", header_block_top_keys(["# T", "", "plain"]), set())

    print()
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    parser = argparse.ArgumentParser(
        description="Advisory, forward-only retrieval-header check. "
        f"Rule authority: {RULE_AUTHORITY}",
    )
    parser.add_argument("paths", nargs="*", help="explicit file paths to check")
    parser.add_argument("--staged", action="store_true", help="check git-staged files")
    parser.add_argument(
        "--changed", action="store_true", help="check changed + untracked files"
    )
    parser.add_argument(
        "--strict", action="store_true", help="exit 1 if any violation (CI/commit)"
    )
    parser.add_argument(
        "--hook", action="store_true", help="PostToolUse hook mode (stdin JSON)"
    )
    parser.add_argument(
        "--selftest", action="store_true", help="run pure-function self-tests"
    )
    args = parser.parse_args(argv)

    root = repo_root()

    if args.hook:
        return run_hook(root)  # always exit 0; --strict is ignored in hook mode

    relpaths: list[str] = []
    if args.staged:
        relpaths += staged_paths(root)
    if args.changed:
        relpaths += changed_paths(root)
    relpaths += [to_relposix(p, root) for p in args.paths]

    warnings = collect_warnings(relpaths, root)
    for w in warnings:
        print(f"retrieval-header: {w}", file=sys.stderr)
    if warnings and not args.strict:
        print(
            f"retrieval-header: {len(warnings)} advisory warning(s); "
            f"see {RULE_AUTHORITY} (advisory, exit 0).",
            file=sys.stderr,
        )
    if args.strict and warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
