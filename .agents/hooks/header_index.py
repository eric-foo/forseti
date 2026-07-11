#!/usr/bin/env python3
"""Retrieval-header index and forward-only CI gate.

WHAT THIS DOES
  Provides four modes over the retrieval-header contract:

  --index    Full retrieval view: for each durable, header-bearing .md in the
             repo, print one row: path | artifact_role | scope | use_when
             (joined) | stale_if (joined) | open_next.  Human-readable, exit 0.

  --health   Whole-repo advisory. Counts (and with --verbose lists) two classes:
               MISSING-HEADER  durable, non-exempt .md files with no header
               ORPHAN          header-bearing .md whose CONTAINING FOLDER is not
                               map-covered per C3 semantics (dir appears as a
                               substring in any map/submap line, or any map line
                               says "not retrieval-indexed") AND the folder is
                               not C3-exempt (_inbox/_scratch).  A file whose
                               folder IS map-covered is NOT an orphan even if
                               the individual file path is not named in the map.
             Exit 0 always (advisory, not a gate).

  --health --oneline
             Single capsule line for the session context capsule:
               "retrieval health: N missing headers, M orphans"
             or "retrieval health: ok" when both are zero.  Exit 0.

  --strict   CI GATE — diff-scoped / forward-only.  Resolves changed .md files
             vs a base ref (priority: $FORSETI_DIFF_BASE exact CI event SHA;
             then $GITHUB_BASE_REF -> origin/<ref>; then --base <ref>; then
             default origin/main).  Computes
             the changed set via `git diff --name-only <base>...HEAD`.  For
             ONLY those changed files: fails (exit 1) if a changed durable
             non-exempt doc is MISSING-HEADER or is an ORPHAN.  Prints each
             finding.  Exit 0 if none.  If diff-scoping genuinely cannot be
             resolved (e.g. no origin), prints a loud message and exits 0
             (fail-open) — a whole-repo strict would red-main on the existing
             backlog.

  --selftest Pure-function cases; exit 0 on pass, 1 on fail.

WHY THIS EXISTS (enforcement placement)
  The retrieval-header check (check_retrieval_header.py) already enforces header
  presence at the write-time boundary for individual files.  This companion adds:
    (a) a whole-repo index so a CA can see all durable retrieval artifacts at a
        glance without blind-walking the tree;
    (b) a whole-repo health advisory so the existing missing-header and orphan
        backlog is surfaced non-blockingly via the session capsule;
    (c) a forward-only CI gate so every NEW or CHANGED durable doc is gated on
        both header presence AND map reachability, without red-lining main on
        the pre-existing backlog.
  Enforcement placement principle:
    .agents/workflow-overlay/validation-gates.md -> "Enforcement Placement"

HARD BOUNDARY
  Read-only.  No writes.  An unexpected internal exception (including a
  broken/missing check_retrieval_header.py sibling) is the GATE FAIL bucket
  in gating modes (validation-gates.md; EP-35 FIND-02 class sweep):
  --strict/--selftest exit 1 on internal error; advisory modes (--index,
  --health, --report-orca) print the error and exit 0 so a broken index
  never stalls a session.  Infra-gap fail-opens (unresolvable repo root or
  base ref) are unchanged.  --strict is diff-scoped only; it NEVER falls
  back to whole-repo strict.

MODES (summary)
  header_index.py --index
  header_index.py --health [--verbose]
  header_index.py --health --oneline
  header_index.py --strict [--base <ref>]
  header_index.py --selftest

REUSE
  Imports scope_folder, check_relpath, IN_SCOPE_PREFIXES, EXCLUDED_PREFIXES,
  and head_lines directly from check_retrieval_header.py (same .agents/hooks/
  directory).  check_retrieval_header.py is the canonical source for "which
  .md paths are durable/in-scope" and "does a file have a valid header";
  this file does NOT redefine those decisions.

REGISTRATION
  CI:  .github/workflows/ci.yml (retrieval-header index step, after link-check)
  Capsule: session_context_capsule.py calls --health --oneline with a 5s timeout
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path


def _configure_stdio() -> None:
    """Keep report modes printable when repo text contains non-ASCII."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            pass


_configure_stdio()

# ---------------------------------------------------------------------------
# Import shared decisions from check_retrieval_header (canonical source)
# ---------------------------------------------------------------------------

def _import_check_retrieval_header():
    """Import check_retrieval_header from the same hooks directory."""
    import importlib.util
    hooks_dir = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location(
        "check_retrieval_header",
        hooks_dir / "check_retrieval_header.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


try:
    _crh = _import_check_retrieval_header()
    scope_folder = _crh.scope_folder
    check_relpath = _crh.check_relpath
    head_lines = _crh.head_lines
    header_problems_for_lines = _crh.header_problems_for_lines
    IN_SCOPE_PREFIXES = _crh.IN_SCOPE_PREFIXES
    EXCLUDED_PREFIXES = _crh.EXCLUDED_PREFIXES
    _CRH_AVAILABLE = True
except Exception as _crh_err:
    _CRH_AVAILABLE = False
    _CRH_ERR = _crh_err


def _import_check_map_links():
    """Import check_map_links from the same hooks directory (for C3 folder-coverage)."""
    import importlib.util
    hooks_dir = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location(
        "check_map_links",
        hooks_dir / "check_map_links.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


try:
    _cml = _import_check_map_links()
    _dir_is_covered = _cml.dir_is_covered
    _dir_is_exempt_coverage = _cml.dir_is_exempt_coverage
    _collect_map_files = _cml.collect_map_files
    _load_map_text_cml = _cml.load_map_text
    _CML_AVAILABLE = True
except Exception as _cml_err:
    _CML_AVAILABLE = False
    _CML_ERR = _cml_err


# ---------------------------------------------------------------------------
# Repo root (same pattern as other hooks)
# ---------------------------------------------------------------------------

def repo_root() -> Path:
    """Repo root derived from this file's location (.agents/hooks/<this>)."""
    return Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# YAML header field extraction
# ---------------------------------------------------------------------------

_FIELD_RE = re.compile(r"^\s*(\w[\w_]*)\s*:\s*(.*)$")
_LIST_ITEM_RE = re.compile(r"^\s+-\s+(.+)$")


def _extract_header_fields(lines: list[str]) -> dict:
    """Extract YAML retrieval header fields from the first HEAD_LINES of a file.

    Returns a dict with keys: artifact_role, scope, use_when (list), stale_if
    (list), open_next (list).  Missing fields are empty strings / empty lists.

    Pure function (testable).
    """
    fields: dict = {
        "artifact_role": "",
        "scope": "",
        "use_when": [],
        "stale_if": [],
        "open_next": [],
    }

    in_yaml = False
    current_list_key: str | None = None
    list_keys = {"use_when", "stale_if", "open_next"}

    for line in lines:
        stripped = line.strip()

        # Detect yaml fence
        if stripped.startswith("```"):
            if not in_yaml and ("yaml" in stripped.lower() or stripped == "```"):
                in_yaml = True
                continue
            elif in_yaml:
                in_yaml = False
                current_list_key = None
                continue
            continue

        if not in_yaml:
            continue

        # List continuation
        if current_list_key is not None:
            m = _LIST_ITEM_RE.match(line)
            if m:
                val = m.group(1).strip().strip("\"'")
                fields[current_list_key].append(val)
                continue
            # Any non-list line ends the current list
            current_list_key = None

        # Key-value line
        m = _FIELD_RE.match(line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip().strip("\"'")
            if key in ("artifact_role", "scope"):
                fields[key] = val
            elif key in list_keys:
                # Inline value or start of a list
                if val:
                    fields[key].append(val)
                else:
                    current_list_key = key

    return fields


# ---------------------------------------------------------------------------
# Repo walk: enumerate all in-scope .md files
# ---------------------------------------------------------------------------

def walk_durable_mds(root: Path) -> list[str]:
    """Return all in-scope durable .md relpaths (POSIX) under the repo root.

    Pure walk — does not check for header presence. Walks only the
    IN_SCOPE_PREFIXES roots: scope_folder() accepts nothing outside them, so
    the result set is identical to a whole-repo walk while out-of-scope
    subtrees (product spines, harness, nested worktrees in a main checkout)
    cost no I/O.
    """
    results: list[str] = []
    for prefix in IN_SCOPE_PREFIXES:
        base = root / prefix
        if not base.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            # Prune hidden/large non-relevant dirs
            dirnames[:] = [
                d for d in dirnames
                if not (d.startswith(".git") or d == "node_modules" or d == "__pycache__")
            ]
            for fname in filenames:
                if not fname.endswith(".md"):
                    continue
                fpath = Path(dirpath) / fname
                relposix = fpath.relative_to(root).as_posix()
                if scope_folder(relposix) is not None:
                    results.append(relposix)
    return sorted(results)


def has_retrieval_header(relposix: str, root: Path) -> bool:
    """True if the file has a structurally valid retrieval header (no problems)."""
    return len(check_relpath(relposix, root)) == 0


# ---------------------------------------------------------------------------
# Repo map / submap loading (delegates to check_map_links canonical source)
# ---------------------------------------------------------------------------

def load_map_text(root: Path) -> str:
    """Concatenate repo map + any submap text.

    Delegates to check_map_links.collect_map_files + check_map_links.load_map_text
    when available (canonical C3 source), otherwise falls back to local logic.
    """
    if _CML_AVAILABLE:
        map_files = _collect_map_files(root)
        return _load_map_text_cml(map_files)
    # Fallback: local logic (used only when check_map_links import failed)
    parts: list[str] = []
    map_path = root / "docs" / "workflows" / "forseti_repo_map_v0.md"
    if map_path.exists():
        try:
            parts.append(map_path.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            pass
    workflows = root / "docs" / "workflows"
    if workflows.is_dir():
        for f in workflows.iterdir():
            if (
                f.is_file()
                and "submap" in f.name.lower()
                and f.name.endswith(".md")
                and f != map_path
            ):
                try:
                    parts.append(f.read_text(encoding="utf-8", errors="replace"))
                except OSError:
                    pass
    return "\n".join(parts)


def is_folder_orphan(relposix: str, map_text: str) -> bool:
    """True if relposix's containing folder is NOT map-covered per C3 semantics.

    A file is a folder-orphan when ALL of these hold:
      1. Its containing folder is not C3-exempt (_inbox / _scratch).
      2. Its containing folder does NOT appear as a substring in any map line,
         AND no map line contains "not retrieval-indexed".

    This aligns with check_map_links C3: coverage is FOLDER-LEVEL, not
    individual-file-level.  A file whose folder IS map-covered is NOT an
    orphan even if its exact path is not named in the map.

    Delegates to check_map_links.dir_is_covered / dir_is_exempt_coverage when
    available; falls back to inline logic when the import failed.

    Pure function (testable).
    """
    # Derive containing folder (POSIX)
    parts = relposix.rsplit("/", 1)
    folder = parts[0] if len(parts) == 2 else ""

    # Check C3 exemption
    if _CML_AVAILABLE:
        if _dir_is_exempt_coverage(folder):
            return False
        if not map_text:
            return True
        return not _dir_is_covered(folder, map_text)
    else:
        # Inline fallback (should rarely trigger)
        if folder.startswith("docs/_inbox") or "_scratch" in folder:
            return False
        if not map_text:
            return True
        for line in map_text.splitlines():
            if folder and folder in line:
                return False
            if "not retrieval-indexed" in line.lower():
                return False
        return True


# ---------------------------------------------------------------------------
# Health scan (whole-repo advisory)
# ---------------------------------------------------------------------------

def health_scan(root: Path) -> tuple[list[str], list[str]]:
    """Return (missing_headers, orphans) lists of relpaths.

    missing_headers: durable in-scope .md files with no valid retrieval header.
    orphans: durable in-scope .md files WITH a valid header whose CONTAINING
             FOLDER is not map-covered per C3 semantics (and not C3-exempt).
    """
    map_text = load_map_text(root)
    all_mds = walk_durable_mds(root)
    missing: list[str] = []
    orphans: list[str] = []
    for relposix in all_mds:
        problems = check_relpath(relposix, root)
        if problems:
            missing.append(relposix)
        else:
            # Has a valid header — check folder-level map coverage (C3 semantics)
            if is_folder_orphan(relposix, map_text):
                orphans.append(relposix)
    return missing, orphans


# ---------------------------------------------------------------------------
# Mode: --index
# ---------------------------------------------------------------------------

def run_index(root: Path) -> int:
    """Print a full retrieval view of all header-bearing durable .md files."""
    all_mds = walk_durable_mds(root)
    rows = []
    for relposix in all_mds:
        problems = check_relpath(relposix, root)
        if problems:
            continue  # skip files without a valid header
        lines = head_lines(root / relposix)
        if lines is None:
            continue
        f = _extract_header_fields(lines)
        rows.append((relposix, f))

    if not rows:
        print("header_index --index: no header-bearing durable .md files found")
        return 0

    print("header_index --index: %d indexed file(s)\n" % len(rows))
    for relposix, f in rows:
        use_when = " | ".join(f["use_when"]) if f["use_when"] else "(none)"
        stale_if = " | ".join(f["stale_if"]) if f["stale_if"] else "(none)"
        open_next = " | ".join(f["open_next"]) if f["open_next"] else "(none)"
        print("  path:        %s" % relposix)
        print("  role:        %s" % (f["artifact_role"] or "(missing)"))
        print("  scope:       %s" % (f["scope"] or "(missing)"))
        print("  use_when:    %s" % use_when)
        print("  stale_if:    %s" % stale_if)
        print("  open_next:   %s" % open_next)
        print()
    return 0


# ---------------------------------------------------------------------------
# Mode: --health [--verbose] [--oneline]
# ---------------------------------------------------------------------------

def run_health(root: Path, verbose: bool = False, oneline: bool = False) -> int:
    """Advisory whole-repo health check. Always exit 0."""
    missing, orphans = health_scan(root)
    if oneline:
        if not missing and not orphans:
            print("retrieval health: ok")
        else:
            print(
                "retrieval health: %d missing header%s, %d orphan%s"
                % (
                    len(missing), "s" if len(missing) != 1 else "",
                    len(orphans),  "s" if len(orphans)  != 1 else "",
                )
            )
        return 0

    # Full health report
    print("header_index --health (whole-repo advisory, exit 0)")
    print("  MISSING-HEADER: %d  (durable in-scope .md with no valid header)" % len(missing))
    print("  ORPHAN:         %d  (header-bearing .md in folder not map-covered per C3)" % len(orphans))
    print()
    if verbose:
        if missing:
            print("MISSING-HEADER files:")
            for p in missing:
                print("  %s" % p)
            print()
        if orphans:
            print("ORPHAN files:")
            for p in orphans:
                print("  %s" % p)
            print()
    if not missing and not orphans:
        print("health: ok")
    else:
        print(
            "health: advisory backlog present (%d missing header, %d orphan) "
            "-- not a gate; fix via the retrieval-metadata contract; "
            "new/changed docs gated forward-only via --strict."
            % (len(missing), len(orphans))
        )
    return 0


# ---------------------------------------------------------------------------
# Mode: --strict (CI gate, diff-scoped)
# ---------------------------------------------------------------------------

def _git(root: Path, *args: str, timeout: int = 15) -> tuple[int, str]:
    """Run git; return (returncode, stdout). Never raises."""
    try:
        res = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True, text=True, timeout=timeout,
        )
        return res.returncode, res.stdout
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired) as e:
        return -1, ""


def resolve_base_ref(root: Path, cli_base: str | None) -> str | None:
    """Resolve the base ref for diff-scoping.

    Priority:
    1. $FORSETI_DIFF_BASE exact CI event SHA
    2. $GITHUB_BASE_REF env var  -> "origin/<value>"
    3. --base <ref> CLI arg
    4. default: "origin/main"

    Returns a ref string, or None if none could be resolved.
    """
    ci_base = os.environ.get("FORSETI_DIFF_BASE", "").strip()
    if ci_base:
        return ci_base
    gh_base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if gh_base:
        return "origin/%s" % gh_base
    if cli_base:
        return cli_base
    return "origin/main"


def changed_mds_vs_base(root: Path, base_ref: str) -> list[str] | None:
    """Return list of changed .md relpaths vs base_ref, or None on failure.

    Uses `git diff --name-only <base>...HEAD` (three-dot: merge-base diff).
    Returns None if the diff cannot be computed.
    """
    rc, out = _git(root, "diff", "--name-only", "%s...HEAD" % base_ref)
    if rc != 0:
        # Try two-dot as fallback
        rc2, out2 = _git(root, "diff", "--name-only", base_ref, "HEAD")
        if rc2 != 0:
            return None
        out = out2
    return [line.strip() for line in out.splitlines() if line.strip().endswith(".md")]


def run_strict(root: Path, cli_base: str | None = None) -> int:
    """--strict CI gate: diff-scoped, forward-only.  Exit 1 on findings."""
    base_ref = resolve_base_ref(root, cli_base)

    changed = changed_mds_vs_base(root, base_ref)
    if changed is None:
        # Cannot diff-scope — MUST fail open (whole-repo strict would red-main)
        print(
            "header_index --strict: WARNING: diff-scoping unavailable "
            "(base ref '%s' could not be resolved or git diff failed). "
            "Failing OPEN (exit 0) to avoid red-main on backlog. "
            "Check that origin is configured and the base ref exists."
            % base_ref,
            file=sys.stderr,
        )
        return 0

    if not changed:
        print("header_index --strict: no changed .md files in this diff -- OK (exit 0)")
        return 0

    map_text = load_map_text(root)
    findings: list[str] = []

    for relposix in changed:
        if scope_folder(relposix) is None:
            continue  # out of scope (not a durable doc)
        problems = check_relpath(relposix, root)
        if problems:
            findings.append(
                "MISSING-HEADER: %s -- %s" % (relposix, "; ".join(problems))
            )
        else:
            # Header present — check folder-level map coverage (C3 semantics)
            if is_folder_orphan(relposix, map_text):
                folder = relposix.rsplit("/", 1)[0] if "/" in relposix else ""
                findings.append(
                    "ORPHAN: %s -- header present but containing folder (%s) "
                    "is not map-covered per C3 semantics. "
                    "Add a map entry for folder %s in "
                    "docs/workflows/forseti_repo_map_v0.md or a submap."
                    % (relposix, folder, folder)
                )

    if findings:
        print(
            "header_index --strict: %d finding(s) on changed durable .md files "
            "(base: %s):" % (len(findings), base_ref)
        )
        for f in findings:
            print("  %s" % f)
        return 1

    print(
        "header_index --strict: OK -- %d changed durable .md file(s) all have "
        "headers and are map-reachable (base: %s)"
        % (sum(1 for r in changed if scope_folder(r) is not None), base_ref)
    )
    return 0


# ---------------------------------------------------------------------------
# Mode: --selftest
# ---------------------------------------------------------------------------

def selftest() -> int:
    """Pure-function self-test cases. Exit 0 on pass, 1 on fail."""
    ok = True

    # --- _extract_header_fields ---
    def make_header(**kw) -> list[str]:
        lines = ["# Title", "", "```yaml", "retrieval_header_version: 1"]
        for k, v in kw.items():
            if isinstance(v, list):
                lines.append("%s:" % k)
                for item in v:
                    lines.append("  - %s" % item)
            else:
                lines.append("%s: %s" % (k, v))
        lines.append("authority_boundary: retrieval_only")
        lines.append("```")
        return lines

    print("--- _extract_header_fields ---")
    h1 = make_header(
        artifact_role="Test role",
        scope="Test scope",
        use_when=["when A", "when B"],
        stale_if=["if X"],
        open_next=["docs/foo/bar_v0.md"],
    )
    f1 = _extract_header_fields(h1)
    cases_ehf = [
        ("artifact_role", f1["artifact_role"] == "Test role"),
        ("scope",         f1["scope"] == "Test scope"),
        ("use_when len",  len(f1["use_when"]) == 2),
        ("use_when[0]",   f1["use_when"][0] == "when A"),
        ("stale_if",      f1["stale_if"] == ["if X"]),
        ("open_next",     f1["open_next"] == ["docs/foo/bar_v0.md"]),
    ]
    for label, passed in cases_ehf:
        status = "PASS" if passed else "FAIL"
        if not passed:
            ok = False
        print("%s  %s" % (status, label))

    # Empty header (no yaml block)
    h_empty = ["# Title", "", "No yaml here."]
    f_empty = _extract_header_fields(h_empty)
    cases_empty = [
        ("empty artifact_role", f_empty["artifact_role"] == ""),
        ("empty use_when",      f_empty["use_when"] == []),
    ]
    for label, passed in cases_empty:
        status = "PASS" if passed else "FAIL"
        if not passed:
            ok = False
        print("%s  %s" % (status, label))

    # --- is_folder_orphan (C3 folder-coverage semantics) ---
    # map_text contains folder-level entries; individual file paths need not appear.
    print()
    print("--- is_folder_orphan ---")
    # Map text mentions 'docs/decisions' and 'docs/workflows' as folder-level entries
    map_text_sample = (
        "| `docs/decisions/` | Decision records. |\n"
        "| `docs/workflows/` | Workflow overlays. |\n"
    )
    # Map text with 'not retrieval-indexed' exemption line
    map_text_nri = "docs/some/unmapped/folder: not retrieval-indexed\n"
    # Map text that does NOT cover docs/prompts/reviews
    map_text_no_pr = "| `docs/decisions/` | Decision records. |\n"
    orphan_cases = [
        # Folder 'docs/decisions' IS in map -> not orphan (even if file path not named)
        ("folder covered, file not named",
         "docs/decisions/baz_v0.md", map_text_sample, False),
        # Folder 'docs/decisions' IS in map -> not orphan
        ("folder covered, file also present",
         "docs/decisions/foo_v0.md", map_text_sample, False),
        # Folder 'docs/prompts/reviews' NOT in map -> orphan
        ("folder not covered",
         "docs/prompts/reviews/bar_v0.md", map_text_no_pr, True),
        # Empty map text -> orphan
        ("empty map text",
         "docs/decisions/foo_v0.md", "", True),
        # 'not retrieval-indexed' prose no longer auto-covers (F2 fix): an
        # uncovered folder is an orphan even if such a line exists in the map.
        ("not-retrieval-indexed prose no longer covers",
         "docs/some/unmapped/folder/file_v0.md", map_text_nri, True),
        # docs/_inbox is C3-exempt -> not orphan
        ("_inbox exempt",
         "docs/_inbox/foo.md", map_text_no_pr, False),
        # _scratch is C3-exempt -> not orphan
        ("_scratch exempt",
         "docs/_scratch/foo.md", map_text_no_pr, False),
        # docs/workflows IS in map -> not orphan
        ("docs/workflows covered",
         "docs/workflows/forseti_repo_map_v0.md", map_text_sample, False),
    ]
    for label, relposix, mt, expected in orphan_cases:
        got = is_folder_orphan(relposix, mt)
        status = "PASS" if got == expected else "FAIL"
        if got != expected:
            ok = False
        print("%s  %-52s  expect=%s got=%s" % (status, label, expected, got))

    # --- resolve_base_ref ---
    print()
    print("--- resolve_base_ref ---")
    import pathlib
    fake_root = pathlib.Path(".")
    # Clear CI and GitHub base variables for deterministic testing
    saved_ci_base = os.environ.pop("FORSETI_DIFF_BASE", None)
    env_saved = os.environ.pop("GITHUB_BASE_REF", None)
    try:
        r1 = resolve_base_ref(fake_root, None)
        r2 = resolve_base_ref(fake_root, "some-branch")
        os.environ["GITHUB_BASE_REF"] = "develop"
        r3 = resolve_base_ref(fake_root, None)
        os.environ["GITHUB_BASE_REF"] = "develop"
        r4 = resolve_base_ref(fake_root, "ignored")  # env takes priority
    finally:
        if env_saved is not None:
            os.environ["GITHUB_BASE_REF"] = env_saved
        else:
            os.environ.pop("GITHUB_BASE_REF", None)
        if saved_ci_base is not None:
            os.environ["FORSETI_DIFF_BASE"] = saved_ci_base
        else:
            os.environ.pop("FORSETI_DIFF_BASE", None)
    base_cases = [
        ("default -> origin/main",  r1, "origin/main"),
        ("cli base",                r2, "some-branch"),
        ("env GITHUB_BASE_REF",     r3, "origin/develop"),
        ("env beats cli",           r4, "origin/develop"),
    ]
    for label, got, expected in base_cases:
        status = "PASS" if got == expected else "FAIL"
        if got != expected:
            ok = False
        print("%s  %-30s  expect=%s got=%s" % (status, label, expected, got))

    print()
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_report_orca(root: Path) -> int:
    """--report-orca: REPORT MODE over forseti/product/spines/**. ALWAYS exits 0.

    Measures retrieval-header PRESENCE/validity using the SAME structural predicate
    as the live header gate (header_problems_for_lines), applied directly so the
    forseti/ corpus is not masked by the live IN_SCOPE_PREFIXES scope (check_relpath
    returns [] for out-of-scope paths). Frozen predicate = strict-minus-exit-0; the
    Phase-3 flip changes the exit only, not the predicate.

    Orphan / folder-coverage over forseti/ is intentionally NOT reported here: it
    depends on check_map_links.dir_is_covered, which is currently vacuous (F2), so
    any count would falsely imply coverage. Coverage is the W-map / coverage-gate piece.
    """
    spines_root = root / "forseti" / "product" / "spines"
    if not spines_root.is_dir():
        print("header_index --report-orca: no forseti/product/spines/ tree; nothing to report")
        return 0

    missing: list[str] = []
    total = 0
    for dirpath, dirnames, filenames in os.walk(spines_root):
        dirnames[:] = [
            d for d in dirnames
            if not (d.startswith(".git") or d == "node_modules"
                    or d == "__pycache__" or "_scratch" in d)
        ]
        for fname in filenames:
            if not fname.endswith(".md"):
                continue
            relposix = (Path(dirpath) / fname).relative_to(root).as_posix()
            lines = head_lines(root / relposix)
            if lines is None:
                continue
            total += 1
            if header_problems_for_lines(lines):
                missing.append(relposix)

    print("header_index --report-orca (REPORT MODE, exit 0; not a gate):")
    print("  scope: forseti/product/spines/**  |  predicate shared with the live header gate")
    print("  durable .md scanned:             %d" % total)
    print("  MISSING / invalid header (debt): %d" % len(missing))
    print("  orphan / coverage:               deferred to W-map (dir_is_covered vacuous, F2)")
    for m in sorted(missing):
        print("    MISSING-HEADER: %s" % m)
    return 0


def main(argv: list[str]) -> int:
    # Forced-exception probe: proves the __main__ gating handler
    # (forseti-harness/tests/unit/test_hook_internal_error_gating.py).
    if "--force-internal-error" in argv:
        raise RuntimeError("forced internal error (probe)")
    if not _CRH_AVAILABLE:
        print(
            "header_index: ERROR: could not import check_retrieval_header.py: %s" % _CRH_ERR,
            file=sys.stderr,
        )
        print(
            "header_index: ensure check_retrieval_header.py is in the same "
            "directory as this script (.agents/hooks/).",
            file=sys.stderr,
        )
        # A broken/missing sibling checker is an internal defect, not an infra
        # gap: GATE FAIL in gating modes (EP-35 FIND-02 class sweep); advisory
        # modes stay fail-open so a broken import never stalls a session.
        return 1 if ("--strict" in argv or "--selftest" in argv) else 0

    if "--selftest" in argv:
        return selftest()

    try:
        root = repo_root()
    except Exception as exc:
        print("header_index: could not determine repo root: %s" % exc, file=sys.stderr)
        return 0  # fail open

    if "--index" in argv:
        return run_index(root)

    if "--health" in argv:
        oneline = "--oneline" in argv
        verbose = "--verbose" in argv
        return run_health(root, verbose=verbose, oneline=oneline)

    if "--strict" in argv:
        cli_base: str | None = None
        if "--base" in argv:
            idx = argv.index("--base")
            if idx + 1 < len(argv):
                cli_base = argv[idx + 1]
        return run_strict(root, cli_base=cli_base)

    if "--report-orca" in argv:
        return run_report_orca(root)

    print("Usage: header_index.py --index | --health [--verbose] [--oneline] | --strict [--base <ref>] | --report-orca | --selftest")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        # GATE FAIL bucket in gating modes (validation-gates.md; EP-35
        # delegated review FIND-02 class sweep): an internal checker bug must
        # not read as a green gate. Advisory modes fail open so a bug never
        # bricks the agent.
        sys.stderr.write("header_index: internal error: %s\n" % exc)
        gating = "--strict" in sys.argv[1:] or "--selftest" in sys.argv[1:]
        sys.exit(1 if gating else 0)
