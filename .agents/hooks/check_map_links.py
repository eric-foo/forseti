#!/usr/bin/env python3
"""Bidirectional retrieval link-check: repo map <-> disk, open_next <-> disk, folder coverage.

WHAT THIS DOES
  Three mechanically-checkable invariants that keep the repo map and the
  retrieval headers honest without reading product-authority sources:

  C1  MAP->DISK: every repo-relative path mentioned in the repo map or any
      submap must exist on disk.  Exempt: lines whose surrounding text says
      "does not exist yet" or "created on first".

  C2  OPEN_NEXT->DISK: every path listed under open_next: in any .md file
      under docs/ or .agents/ (skipping _scratch/, _inbox/, node_modules)
      must exist on disk.

  C3  FOLDER COVERAGE: every directory under docs/ (recursive) that has >=3
      .md files directly must appear as a substring in the repo map (any of
      its files or the dir path itself) OR have a map line containing the
      phrase "not retrieval-indexed".  Exempt: docs/_inbox and any dir whose
      path contains "_scratch".

WHY (enforcement placement)
  The repo map and open_next headers are written by agents and humans.  Path
  rot happens silently: a file is renamed, a folder is added, a path is
  copy-pasted wrong.  A check run in CI and pre-commit catches the rot at the
  moment the diff lands, not after the next reader is confused.

HARD BOUNDARY
  Read-only.  No git calls.  No writes.  Fails OPEN on internal error
  (--strict: prints the error, exits 0 so the gate does not ghost-fail).
  --check always exits 0.  --strict exits 1 only when actual findings exist.

MODES
  check_map_links.py --strict     CI gate; print findings; exit 1 if any, else 0
  check_map_links.py --check      human-readable; always exit 0
  check_map_links.py --selftest   pure-function cases; exit per pass/fail

REGISTRATION (.github/workflows/ci.yml, after the test step)
  - name: retrieval link check
    run: python .agents/hooks/check_map_links.py --strict
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Repo root (this file lives at .agents/hooks/check_map_links.py)
# ---------------------------------------------------------------------------

def repo_root() -> Path:
    """Repo root derived from this file's location (parents[2])."""
    return Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# C1 helpers: path extraction from a markdown line
# ---------------------------------------------------------------------------

# Token pattern: starts with one of the known prefixes, contains no spaces,
# optionally backtick-quoted or bare.  We also strip trailing punctuation.
_PATH_PREFIXES = (
    "docs/", ".agents/", ".github/", "orca-harness/",
    "AGENTS.md", "CLAUDE.md",
)

_TOKEN_RE = re.compile(
    r"`([^`\s]+)`"           # backtick-quoted token
    r"|"
    r"(?<![`\w/])([\w.\-][^\s`\"'<>|,)]+)"  # bare word starting with word char or dot
)

_TRAILING_PUNCT = re.compile(r"[.,;:)\]>\"']+$")


def extract_paths_from_line(line: str) -> list[str]:
    """Extract repo-relative path tokens from one markdown line.

    Returns only tokens that begin with a known repo-relative prefix.
    Strips trailing punctuation.  Ignores tokens with spaces.
    Skips glob patterns (containing '*') and anchor-only suffixes ('#...').
    Strips fragment anchors ('#...') so 'source-loading.md#section' checks
    the base file only.

    Pure function (testable).
    """
    results: list[str] = []
    for m in _TOKEN_RE.finditer(line):
        raw = m.group(1) or m.group(2)
        if not raw:
            continue
        token = _TRAILING_PUNCT.sub("", raw)
        if not token:
            continue
        if not any(token.startswith(p) for p in _PATH_PREFIXES):
            continue
        # Skip glob patterns (contain '*' or '?')
        if "*" in token or "?" in token:
            continue
        # Strip fragment anchor (check base file only)
        if "#" in token:
            token = token.split("#")[0]
        if not token:
            continue
        results.append(token)
    return results


def is_exempt_line(line: str) -> bool:
    """True if the line contains an exemption marker for C1."""
    lower = line.lower()
    return "does not exist yet" in lower or "created on first" in lower


# ---------------------------------------------------------------------------
# C2 helpers: open_next parsing from header text
# ---------------------------------------------------------------------------

def parse_open_next(header_text: str) -> tuple[list[str], int]:
    """Parse path entries from the open_next: block of a YAML retrieval header.

    header_text is the first 40 lines of the file joined into a single string.
    Returns (entries, nonresolving_count) where:
      - entries: path-like entries that are NOT annotated with a "nonresolving:"
        trailing comment (contains "/" or ends with ".md").
      - nonresolving_count: number of path-like entries whose trailing comment
        (after " # ") starts with "nonresolving:" -- these are skipped from the
        existence check and counted as annotated debt.

    Strips surrounding quotes and reads trailing comments (after " # ").
    An entry with "# nonresolving: <reason>" is skipped but counted.
    An entry with "# <other comment>" is still checked.
    An entry with no comment is checked.

    Pure function (testable).
    """
    entries: list[str] = []
    nonresolving_count = 0
    in_open_next = False
    in_yaml_block = False

    for line in header_text.splitlines():
        stripped = line.strip()

        # Detect start/end of the YAML fenced block (``` yaml or ```)
        if stripped.startswith("```"):
            if not in_yaml_block and ("yaml" in stripped.lower() or stripped == "```"):
                in_yaml_block = True
                continue
            elif in_yaml_block:
                in_yaml_block = False
                in_open_next = False
                continue
            continue

        if not in_yaml_block:
            continue

        if stripped.startswith("open_next:"):
            in_open_next = True
            continue

        if in_open_next:
            # A new top-level key ends the open_next block
            if stripped and not stripped.startswith("-") and ":" in stripped and not stripped.startswith("#"):
                key = stripped.split(":")[0].strip()
                if not key.startswith("-"):
                    in_open_next = False
                    continue

            if stripped.startswith("- "):
                raw = stripped[2:].strip()
                # Extract trailing comment (after " # ")
                comment_pos = raw.find(" # ")
                comment = ""
                if comment_pos != -1:
                    comment = raw[comment_pos + 3:].strip()
                    raw = raw[:comment_pos].strip()
                # Strip surrounding quotes
                entry = raw.strip("\"'").strip()
                if not entry:
                    continue
                # Only handle path-like entries
                if not ("/" in entry or entry.endswith(".md")):
                    continue  # non-path entries like "owner decision" are skipped
                # Check for nonresolving annotation: skip existence check, count as debt
                if comment.startswith("nonresolving:"):
                    nonresolving_count += 1
                    continue
                entries.append(entry)

    return entries, nonresolving_count


# ---------------------------------------------------------------------------
# C3 helpers: folder coverage decision
# ---------------------------------------------------------------------------

def dir_is_covered(rel_dir: str, map_text: str) -> bool:
    """True if rel_dir (POSIX, e.g. "docs/prompts/reviews") appears as a
    substring of any line in map_text, or if map_text has a line containing
    "not retrieval-indexed".

    Pure function (testable).
    """
    for line in map_text.splitlines():
        if rel_dir in line:
            return True
        if "not retrieval-indexed" in line.lower():
            return True
    return False


def dir_is_exempt_coverage(rel_dir: str) -> bool:
    """True if this directory is exempt from C3 (docs/_inbox or contains _scratch)."""
    # Use forward-slash form for portability
    if rel_dir.startswith("docs/_inbox"):
        return True
    if "_scratch" in rel_dir:
        return True
    return False


# ---------------------------------------------------------------------------
# Finding type
# ---------------------------------------------------------------------------

class Finding(NamedTuple):
    check: str     # "C1", "C2", "C3"
    source: str    # which file reported the finding
    detail: str    # human-readable detail


# ---------------------------------------------------------------------------
# Main scanning logic
# ---------------------------------------------------------------------------

def collect_map_files(root: Path) -> list[Path]:
    """Return the repo map and any *submap*.md files under docs/workflows/."""
    candidates: list[Path] = []
    map_path = root / "docs" / "workflows" / "orca_repo_map_v0.md"
    if map_path.exists():
        candidates.append(map_path)
    workflows = root / "docs" / "workflows"
    if workflows.is_dir():
        for f in workflows.iterdir():
            if f.is_file() and "submap" in f.name.lower() and f.name.endswith(".md"):
                if f != map_path:
                    candidates.append(f)
    return candidates


def load_map_text(map_files: list[Path]) -> str:
    """Concatenate all map file content into one string for C3 coverage checks."""
    parts: list[str] = []
    for f in map_files:
        try:
            parts.append(f.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            pass
    return "\n".join(parts)


def run_c1(root: Path, map_files: list[Path]) -> list[Finding]:
    """C1: every path mentioned in map files must exist on disk."""
    findings: list[Finding] = []
    for map_file in map_files:
        try:
            text = map_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel_source = map_file.relative_to(root).as_posix()
        for line in text.splitlines():
            if is_exempt_line(line):
                continue
            for token in extract_paths_from_line(line):
                target = root / Path(token.replace("/", os.sep))
                if not target.exists():
                    findings.append(Finding(
                        check="C1",
                        source=rel_source,
                        detail="path in map does not exist on disk: %s" % token,
                    ))
    return findings


def run_c2(root: Path) -> tuple[list[Finding], int]:
    """C2: every open_next path in any .md file under docs/ and .agents/ must exist.

    Returns (findings, total_nonresolving) where total_nonresolving is the
    sum of all annotated nonresolving entries across all scanned files.
    """
    findings: list[Finding] = []
    total_nonresolving = 0
    search_roots = [root / "docs", root / ".agents"]

    for search_root in search_roots:
        if not search_root.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(search_root):
            # Prune excluded directories in-place
            dirnames[:] = [
                d for d in dirnames
                if d not in ("_scratch", "_inbox", "node_modules")
                and "_scratch" not in d
            ]
            for fname in filenames:
                if not fname.endswith(".md"):
                    continue
                fpath = Path(dirpath) / fname
                try:
                    # Only read the first 40 lines for the YAML header
                    with open(fpath, encoding="utf-8", errors="replace") as fh:
                        lines = []
                        for i, line in enumerate(fh):
                            if i >= 40:
                                break
                            lines.append(line.rstrip("\n"))
                    header_text = "\n".join(lines)
                except OSError:
                    continue

                entries, nonresolving = parse_open_next(header_text)
                total_nonresolving += nonresolving

                if not entries:
                    continue

                rel_source = fpath.relative_to(root).as_posix()
                for entry in entries:
                    target = root / Path(entry.replace("/", os.sep))
                    if not target.exists():
                        findings.append(Finding(
                            check="C2",
                            source=rel_source,
                            detail="open_next path does not exist on disk: %s" % entry,
                        ))
    return findings, total_nonresolving


def run_c3(root: Path, map_text: str) -> list[Finding]:
    """C3: every docs/ subdir with >=3 .md files directly must appear in the map."""
    findings: list[Finding] = []
    docs_root = root / "docs"
    if not docs_root.is_dir():
        return findings

    for dirpath, dirnames, filenames in os.walk(docs_root):
        # Prune _scratch from walk (don't descend, don't report)
        dirnames[:] = [d for d in dirnames if "_scratch" not in d]

        current = Path(dirpath)
        rel_dir = current.relative_to(root).as_posix()

        if dir_is_exempt_coverage(rel_dir):
            continue

        md_count = sum(1 for f in filenames if f.endswith(".md"))
        if md_count < 3:
            continue

        if not dir_is_covered(rel_dir, map_text):
            findings.append(Finding(
                check="C3",
                source=rel_dir,
                detail=(
                    "folder has %d .md files but no map entry: %s"
                    % (md_count, rel_dir)
                ),
            ))
    return findings


def run_all_checks(root: Path) -> tuple[list[Finding], int]:
    """Single-pass collection of all three checks.

    Returns (findings, total_nonresolving) where total_nonresolving is the
    count of annotated nonresolving open_next entries (debt, not failures).
    """
    map_files = collect_map_files(root)
    map_text = load_map_text(map_files)
    findings: list[Finding] = []
    findings.extend(run_c1(root, map_files))
    c2_findings, nonresolving = run_c2(root)
    findings.extend(c2_findings)
    findings.extend(run_c3(root, map_text))
    return findings, nonresolving


# ---------------------------------------------------------------------------
# Mode runners
# ---------------------------------------------------------------------------

def run_strict(root: Path) -> int:
    """--strict: CI gate.  Print findings; exit 1 if any, else 0."""
    findings, nonresolving = run_all_checks(root)
    if findings:
        print("check_map_links --strict: %d finding(s)" % len(findings))
        for f in findings:
            print("  [%s] %s  ::  %s" % (f.check, f.source, f.detail))
        print("annotated nonresolving: %d (debt, not failures)" % nonresolving)
        return 1
    print("check_map_links --strict: OK (0 findings)")
    print("annotated nonresolving: %d (debt, not failures)" % nonresolving)
    return 0


def run_check(root: Path) -> int:
    """--check: human-readable; always exit 0."""
    findings, nonresolving = run_all_checks(root)
    if not findings:
        print("check_map_links: OK -- all map paths, open_next paths, and folder coverage checks passed.")
        print("annotated nonresolving: %d (debt, not failures)" % nonresolving)
        return 0
    c1 = [f for f in findings if f.check == "C1"]
    c2 = [f for f in findings if f.check == "C2"]
    c3 = [f for f in findings if f.check == "C3"]
    print("check_map_links --check: %d finding(s)" % len(findings))
    print()
    if c1:
        print("C1  MAP->DISK  (%d)" % len(c1))
        for f in c1:
            print("  source: %s" % f.source)
            print("  detail: %s" % f.detail)
            print()
    if c2:
        print("C2  OPEN_NEXT->DISK  (%d)" % len(c2))
        for f in c2:
            print("  source: %s" % f.source)
            print("  detail: %s" % f.detail)
            print()
    if c3:
        print("C3  FOLDER COVERAGE  (%d)" % len(c3))
        for f in c3:
            print("  source: %s" % f.source)
            print("  detail: %s" % f.detail)
            print()
    print("annotated nonresolving: %d (debt, not failures)" % nonresolving)
    return 0


# ---------------------------------------------------------------------------
# Selftest
# ---------------------------------------------------------------------------

def selftest() -> int:
    """--selftest: pure-function cases.  Exit 0 on pass, 1 on fail."""
    ok = True

    # --- extract_paths_from_line cases ---
    epl_cases = [
        # (label, line, expected tokens)
        ("backtick path",
         "see `docs/workflows/orca_repo_map_v0.md` for details",
         ["docs/workflows/orca_repo_map_v0.md"]),
        ("bare path",
         "open docs/decisions/foo_v0.md before proceeding",
         ["docs/decisions/foo_v0.md"]),
        ("trailing comma",
         "see docs/product/core_spine/bar_v0.md, then decide",
         ["docs/product/core_spine/bar_v0.md"]),
        ("trailing paren",
         "see docs/product/core_spine/bar_v0.md) then decide",
         ["docs/product/core_spine/bar_v0.md"]),
        ("AGENTS.md bare",
         "see AGENTS.md for instructions",
         ["AGENTS.md"]),
        ("CLAUDE.md bare",
         "see CLAUDE.md for shim notes",
         ["CLAUDE.md"]),
        ("orca-harness path",
         "`orca-harness/ecr/__init__.py` is the entry",
         ["orca-harness/ecr/__init__.py"]),
        (".agents path",
         "open `.agents/workflow-overlay/source-of-truth.md`",
         [".agents/workflow-overlay/source-of-truth.md"]),
        (".github path",
         "see `.github/workflows/ci.yml`",
         [".github/workflows/ci.yml"]),
        ("non-path line (no match)",
         "owner decision: defer to next sprint",
         []),
        ("path with spaces not matched",
         "see my folder/with space/foo.md",
         []),
        ("glob pattern skipped",
         "see `docs/decisions/*` for all decisions",
         []),
        ("glob pattern bare skipped",
         "orca-harness/tests/unit/test_ecr_*",
         []),
        ("anchor stripped to base file",
         ".agents/workflow-overlay/source-loading.md#data-capture-spine-ca-read-pack",
         [".agents/workflow-overlay/source-loading.md"]),
        ("anchor in backtick stripped",
         "see `.agents/workflow-overlay/source-loading.md#section`",
         [".agents/workflow-overlay/source-loading.md"]),
    ]
    print("--- extract_paths_from_line ---")
    for label, line, expected in epl_cases:
        got = extract_paths_from_line(line)
        status = "PASS" if got == expected else "FAIL"
        if got != expected:
            ok = False
        print("%s  %-45s  expect=%s got=%s" % (status, label, expected, got))

    # --- is_exempt_line cases ---
    iel_cases = [
        ("exempt: does not exist yet", "see foo/bar.md -- does not exist yet", True),
        ("exempt: created on first", "foo/bar.md created on first run", True),
        ("not exempt: normal line", "see docs/product/bar_v0.md for details", False),
    ]
    print()
    print("--- is_exempt_line ---")
    for label, line, expected in iel_cases:
        got = is_exempt_line(line)
        status = "PASS" if got == expected else "FAIL"
        if got != expected:
            ok = False
        print("%s  %-42s  expect=%s got=%s" % (status, label, expected, got))

    # --- parse_open_next cases ---
    # Each case: (label, header_text, expected_entries, expected_nonresolving)
    def make_header(*entries: str) -> str:
        items = "".join("  - %s\n" % e for e in entries)
        return "# Title\n\n```yaml\nopen_next:\n%s```\n" % items

    pon_cases = [
        ("simple path entry",
         make_header("docs/foo/bar_v0.md"),
         ["docs/foo/bar_v0.md"], 0),
        ("backtick-quoted entry",
         make_header('"docs/foo/bar_v0.md"'),
         ["docs/foo/bar_v0.md"], 0),
        ("single-quoted entry",
         make_header("'docs/foo/bar_v0.md'"),
         ["docs/foo/bar_v0.md"], 0),
        ("entry with ordinary # comment (still checked)",
         make_header("docs/foo/bar_v0.md # load first"),
         ["docs/foo/bar_v0.md"], 0),
        ("nonresolving annotation (skipped, counted)",
         make_header("docs/foo/ephemeral_v0.md # nonresolving: ephemeral scratch"),
         [], 1),
        ("ordinary comment not confused with nonresolving",
         make_header("docs/foo/bar_v0.md # some other comment"),
         ["docs/foo/bar_v0.md"], 0),
        ("entry with no comment (checked)",
         make_header("docs/foo/nocomment_v0.md"),
         ["docs/foo/nocomment_v0.md"], 0),
        ("non-path entry (owner decision)",
         make_header("owner decision"),
         [], 0),
        ("non-path entry (plain word)",
         make_header("defer"),
         [], 0),
        ("mixed: path + non-path",
         make_header("docs/foo/bar_v0.md", "owner decision", ".agents/overlay/x.md"),
         ["docs/foo/bar_v0.md", ".agents/overlay/x.md"], 0),
        ("multiple path entries",
         make_header("docs/a/b_v0.md", "docs/c/d_v0.md"),
         ["docs/a/b_v0.md", "docs/c/d_v0.md"], 0),
        ("mixed nonresolving + normal",
         make_header(
             "docs/foo/real_v0.md",
             "docs/foo/gone_v0.md # nonresolving: operator workfile, never committed",
             "docs/foo/also_real_v0.md",
         ),
         ["docs/foo/real_v0.md", "docs/foo/also_real_v0.md"], 1),
        ("path in open_next stops at next yaml key",
         "```yaml\nopen_next:\n  - docs/a/b_v0.md\nstale_if:\n  - something\n```\n",
         ["docs/a/b_v0.md"], 0),
        ("no yaml block -> empty",
         "# Plain doc\n\nno yaml here\n",
         [], 0),
        ("yaml block no open_next -> empty",
         "```yaml\nscope: foo\n```\n",
         [], 0),
    ]
    print()
    print("--- parse_open_next ---")
    for label, header_text, exp_entries, exp_nr in pon_cases:
        got_entries, got_nr = parse_open_next(header_text)
        passed = (got_entries == exp_entries and got_nr == exp_nr)
        status = "PASS" if passed else "FAIL"
        if not passed:
            ok = False
        print("%s  %-52s  expect=(%s, nr=%d) got=(%s, nr=%d)" % (
            status, label, exp_entries, exp_nr, got_entries, got_nr))

    # --- dir_is_covered cases ---
    dic_cases = [
        ("dir appears in map",
         "docs/prompts/reviews",
         "| `docs/prompts/reviews/` | Review prompts. |",
         True),
        ("dir substring appears",
         "docs/review-outputs/adversarial-artifact-reviews",
         "see docs/review-outputs/adversarial-artifact-reviews/",
         True),
        ("not retrieval-indexed line",
         "docs/some/random/dir",
         "docs/unrelated/foo: not retrieval-indexed",
         True),
        ("dir NOT in map",
         "docs/prompts/architecture",
         "| `docs/prompts/reviews/` | Review prompts. |",
         False),
    ]
    print()
    print("--- dir_is_covered ---")
    for label, rel_dir, map_text, expected in dic_cases:
        got = dir_is_covered(rel_dir, map_text)
        status = "PASS" if got == expected else "FAIL"
        if got != expected:
            ok = False
        print("%s  %-52s  expect=%s got=%s" % (status, label, expected, got))

    # --- dir_is_exempt_coverage cases ---
    diec_cases = [
        ("docs/_inbox is exempt",          "docs/_inbox", True),
        ("docs/_inbox/subdir is exempt",   "docs/_inbox/subdir/foo", True),
        ("_scratch dir is exempt",         "docs/_scratch/foo", True),
        ("normal dir not exempt",          "docs/decisions", False),
        ("docs/hygiene not exempt",        "docs/hygiene", False),
        ("docs/prompts/reviews not exempt","docs/prompts/reviews", False),
    ]
    print()
    print("--- dir_is_exempt_coverage ---")
    for label, rel_dir, expected in diec_cases:
        got = dir_is_exempt_coverage(rel_dir)
        status = "PASS" if got == expected else "FAIL"
        if got != expected:
            ok = False
        print("%s  %-52s  expect=%s got=%s" % (status, label, expected, got))

    print()
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    try:
        root = repo_root()
    except Exception as exc:
        sys.stderr.write("check_map_links: could not determine repo root: %s\n" % exc)
        return 0  # fail open
    if "--check" in argv:
        return run_check(root)
    if "--strict" in argv:
        return run_strict(root)
    # Default: print usage
    print("Usage: check_map_links.py --strict | --check | --selftest")
    print("  --strict   CI gate: exit 1 if any finding")
    print("  --check    human-readable report, always exit 0")
    print("  --selftest pure-function self-check")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        sys.stderr.write("check_map_links: internal error, allowing: %s\n" % exc)
        sys.exit(0)  # fail open
