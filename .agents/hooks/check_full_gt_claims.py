#!/usr/bin/env python3
"""Full-GT claim-inflation tripwire.

WHAT THIS DOES
  Checks ADDED lines of changed .md files for unballasted "full God Tier"
  claim language landing outside the claim-owning / record surfaces. This is
  the code substrate for the Erosion Guards ("claim inflation") named in
  forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_full_gt_declaration_v0.md
  -- referenced as rule authority, never restated here.

  A flagged line is allowed when ANY of these hold:
    - the file is in the allowlisted claim-owning/record path families below;
    - every claim-bearing sentence/clause carries bounding ballast (negation /
      boundary vocabulary such as "not", "pending", "excluded", "ceiling",
      "fixture", "claim tier");
    - the line carries the deliberate, review-visible ack token
      `full-gt-claim-ack`.

CHANGED-FILE SCOPE
  Committed net change `base...HEAD` (GITHUB_BASE_REF -> origin/main, or
  --base), .md files, added lines only (forward-looking; no backfill of
  historical docs). NO HEAD~1 fallback. If the base cannot be resolved or git
  fails, fail OPEN (exit 0, loud warning) -- the universal Forseti infra-gap
  stance; in CI the base is always present (fetch-depth: 0).

HARD BOUNDARY
  Read-only. Shape only: this checker enforces where and how full-GT claim
  language may land; it never grades whether any claim is true, and it creates
  no validation, readiness, or approval state. Code (.py) surfaces are out of
  scope -- those stay governed by tests and the declaration.

MODES
  check_full_gt_claims.py --changed [--strict] [--base REF]   diff-scoped scan
  check_full_gt_claims.py [--strict] PATH [...]               whole-file scan (all lines treated as added)
  check_full_gt_claims.py --hook                              PostToolUse advisory (stdin JSON; lines changed vs HEAD only, whole file for new/untracked files; emits additionalContext; always exit 0)
  check_full_gt_claims.py --selftest                          fixture cases; exit 0/1
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

RULE_AUTHORITY = (
    "forseti/product/spines/data_lake/authority/"
    "core_spine_v0_data_lake_bronze_full_gt_declaration_v0.md (Erosion Guards)"
)

ACK_TOKEN = "full-gt-claim-ack"

CLAIM_RE = re.compile(r"full[\s_-]*god[\s_-]*tier|\bfull[\s_-]*gt\b", re.IGNORECASE)
CLAUSE_SPLIT_RE = re.compile(r"[.;:!?]")
BALLAST_RE = re.compile(
    r"\b(?:not|never|no|pending|proposed|excluded|exclusion|exclusions|ceiling|"
    r"fixture|fixtures|residual|residuals|historical|superseded|toward|towards|"
    r"distance|before|until|bounded)\b"
    r"|claim[\s_-]*tier"
    r"|" + re.escape(ACK_TOKEN),
    re.IGNORECASE,
)

ALLOWLIST_EXACT = {
    "forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_full_gt_declaration_v0.md",
    "forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md",
    "forseti/product/spines/data_lake/README.md",
    "docs/workflows/forseti_repo_map_v0.md",
    "docs/workflows/orca_repo_map_v0.md",
    "docs/decisions/dcp_receipts_archive_v0.md",
}
ALLOWLIST_PREFIXES = (
    "forseti/product/spines/data_lake/workflows/",
    "docs/review-outputs/",
    "docs/prompts/",
    "docs/hygiene/",
)


def is_in_scope(relposix: str) -> bool:
    return relposix.endswith(".md")


def is_allowlisted(relposix: str) -> bool:
    if relposix in ALLOWLIST_EXACT:
        return True
    return relposix.startswith(ALLOWLIST_PREFIXES)


def has_bounding_ballast(line: str) -> bool:
    if ACK_TOKEN in line:
        return True
    claim_segments = [
        segment for segment in CLAUSE_SPLIT_RE.split(line) if CLAIM_RE.search(segment)
    ]
    return bool(claim_segments) and all(BALLAST_RE.search(segment) for segment in claim_segments)


def classify_added_line(relposix: str, line: str) -> str | None:
    """Return a finding message for an added line, or None when the line is clean.

    This is the single classification core; every mode routes through it.
    """
    if not is_in_scope(relposix):
        return None
    if not CLAIM_RE.search(line):
        return None
    if is_allowlisted(relposix):
        return None
    if has_bounding_ballast(line):
        return None
    return (
        "unballasted full-GT claim language outside the claim-owning surfaces. "
        "Bound the claim (negation/ceiling/fixture/claim-tier wording), move it "
        "to a claim-owning record, or mark a deliberate exception with "
        f"`{ACK_TOKEN}`. Rule authority: {RULE_AUTHORITY}."
    )


def _git(root: Path, args: list[str]) -> tuple[int, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True,
            encoding="utf-8", errors="replace",
        )
    except (FileNotFoundError, OSError):
        return 1, ""
    return result.returncode, result.stdout


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolve_base_ref(cli_base: str | None) -> str:
    if cli_base:
        return cli_base
    github_base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if github_base:
        return github_base if "/" in github_base else f"origin/{github_base}"
    return "origin/main"


def _parse_added_lines_by_file(diff_text: str) -> dict[str, list[tuple[int, str]]]:
    """Parse `git diff --unified=0` output into relpath -> [(new_lineno, added_line)].

    File headers (`+++ b/...`) are recognized STRUCTURALLY — only outside a
    hunk — so an added content line beginning `++` (which git renders as
    `+++...` inside a hunk) is kept as content instead of being dropped as a
    header and desynchronizing subsequent line numbers.
    """
    files: dict[str, list[tuple[int, str]]] = {}
    current: str | None = None
    in_hunk = False
    new_lineno = 0
    for raw in diff_text.splitlines():
        if raw.startswith("diff "):
            in_hunk = False
            current = None
        elif raw.startswith("@@"):
            in_hunk = True
            match = re.search(r"\+(\d+)", raw)
            new_lineno = int(match.group(1)) if match else 0
        elif not in_hunk and raw.startswith("+++ b/"):
            current = raw[6:].strip()
            files.setdefault(current, [])
        elif not in_hunk and raw.startswith("+++ "):
            current = None
        elif in_hunk and raw.startswith("+") and current is not None:
            files[current].append((new_lineno, raw[1:]))
            new_lineno += 1
    return files


def added_lines_by_file(root: Path, base_ref: str) -> dict[str, list[tuple[int, str]]] | None:
    """Map relpath -> [(new_lineno, added_line)] for changed .md files. None on infra gap."""
    for probe in ("HEAD", base_ref):
        if _git(root, ["rev-parse", "--verify", "--quiet", probe])[0] != 0:
            return None
    rc, out = _git(
        root,
        ["diff", "--diff-filter=ACMR", "--find-renames", "--unified=0",
         f"{base_ref}...HEAD", "--", "*.md"],
    )
    if rc != 0:
        return None
    return _parse_added_lines_by_file(out)


def scan_changed(root: Path, base_ref: str) -> list[str] | None:
    per_file = added_lines_by_file(root, base_ref)
    if per_file is None:
        return None
    findings: list[str] = []
    for relposix, lines in per_file.items():
        for lineno, line in lines:
            message = classify_added_line(relposix, line)
            if message:
                findings.append(f"{relposix}:{lineno}: {message}")
    return findings


def scan_whole_files(root: Path, paths: list[str]) -> list[str]:
    findings: list[str] = []
    for target in paths:
        path = Path(target)
        candidate = path if path.is_absolute() else root / path
        try:
            relposix = candidate.resolve().relative_to(root).as_posix()
        except (OSError, ValueError):
            relposix = Path(target).as_posix()
        try:
            text = candidate.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            message = classify_added_line(relposix, line)
            if message:
                findings.append(f"{relposix}:{lineno}: {message}")
    return findings


def _hook_relposix(target: str, root: Path) -> str | None:
    p = Path(target)
    if p.is_absolute():
        try:
            return p.resolve().relative_to(root).as_posix()
        except (ValueError, OSError):
            return None
    s = p.as_posix()
    s = s[2:] if s.startswith("./") else s
    if s.startswith("/"):
        # Rooted but not resolvable under the repo (e.g. POSIX-style "/docs/..."
        # payload on Windows): never treat as repo-relative (FIND-01 class).
        return None
    return s


def _uncommitted_added_lines(root: Path, relposix: str) -> list[tuple[int, str]]:
    """Added lines of the just-edited (uncommitted) file vs HEAD; new/untracked file -> all lines.

    The PostToolUse hook fires on an UNCOMMITTED edit, so scan_changed's committed
    base...HEAD diff would miss it -- and scanning the WHOLE file re-flags pre-existing
    (grandfathered) lines on every edit. This scopes to the lines the edit actually added.
    Diff parsing uses the shared structural parser so added content beginning `++`
    is kept as content (FIND-02).
    """
    rc, out = _git(root, ["diff", "--unified=0", "HEAD", "--", relposix])
    if rc != 0:
        return []
    if out.strip():
        parsed = _parse_added_lines_by_file(out)
        return [pair for pairs in parsed.values() for pair in pairs]
    if _git(root, ["ls-files", "--error-unmatch", "--", relposix])[0] == 0:
        return []
    try:
        text = (root / relposix).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    return list(enumerate(text.splitlines(), start=1))


def run_hook() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0
    # Type-check both payload layers: valid-but-wrong-shaped JSON (a list, or a
    # non-dict tool_input) must fail OPEN, not raise (FIND-03).
    if not isinstance(payload, dict):
        return 0
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return 0
    file_path = tool_input.get("file_path", "")
    # .md only -- code (.py) surfaces are out of scope (see CHANGED-FILE SCOPE).
    if not isinstance(file_path, str) or not file_path.endswith(".md"):
        return 0
    root = repo_root()
    relposix = _hook_relposix(file_path, root)
    if relposix is None:
        return 0
    findings = [
        f"{relposix}:{lineno}: {message}"
        for lineno, line in _uncommitted_added_lines(root, relposix)
        if (message := classify_added_line(relposix, line))
    ]
    if findings:
        msg = (
            "full-gt-claims (advisory): "
            + " | ".join(findings[:5])
            + "\nPlacement/shape only; not claim-truth, validation, or readiness "
            "(each finding above cites its rule authority)."
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
    failures: list[str] = []
    cases = 0

    def check(name: str, actual: object, expected: object) -> None:
        nonlocal cases
        cases += 1
        if actual != expected:
            failures.append(f"{name}: expected {expected!r}, got {actual!r}")

    plain = "Bronze is now full God Tier and production ready."
    check("unballasted claim in plain doc fires",
          classify_added_line("docs/decisions/some_new_note_v0.md", plain) is not None, True)
    check("ballasted line is clean",
          classify_added_line("docs/decisions/some_new_note_v0.md",
                              "Bronze is not full God Tier for production surfaces."), None)
    check("unrelated ballast sentence still fires",
          classify_added_line("docs/decisions/some_new_note_v0.md",
                              "This is not about production. Bronze is full God Tier.") is not None,
          True)
    check("one unballasted claim among clauses fires",
          classify_added_line("docs/decisions/some_new_note_v0.md",
                              "Bronze is not full God Tier; Silver is full God Tier.") is not None,
          True)
    check("same-clause pending ballast is clean",
          classify_added_line("docs/decisions/some_new_note_v0.md",
                              "Bronze full GT is pending an owner decision."), None)
    check("claim-tier ballast is clean",
          classify_added_line("docs/decisions/some_new_note_v0.md",
                              "Bronze's full-GT claim tier is owned by the declaration."), None)
    check("allowlisted path is clean",
          classify_added_line(
              "forseti/product/spines/data_lake/workflows/some_record_v0.md", plain), None)
    check("ack token is clean",
          classify_added_line("docs/decisions/some_new_note_v0.md",
                              plain + " full-gt-claim-ack: deliberate, reviewed."), None)
    check("non-md is out of scope",
          classify_added_line("forseti-harness/data_lake/catalog.py", plain), None)
    check("case-insensitive FULL GT fires",
          classify_added_line("docs/decisions/x.md", "We are FULL GT everywhere.") is not None,
          True)
    check("unrelated line is clean",
          classify_added_line("docs/decisions/x.md", "The catalog rebuilds byte-identically."),
          None)

    # FIND-02 red-green: an added content line beginning `++` renders as
    # `+++...` inside a hunk and must be parsed as CONTENT with correct
    # line numbers, not dropped as a file header.
    tricky_diff = (
        "diff --git a/docs/decisions/x.md b/docs/decisions/x.md\n"
        "index 1111111..2222222 100644\n"
        "--- a/docs/decisions/x.md\n"
        "+++ b/docs/decisions/x.md\n"
        "@@ -0,0 +1,2 @@\n"
        "+++ Bronze is full God Tier.\n"
        "+Second added line is full God Tier too.\n"
    )
    parsed = _parse_added_lines_by_file(tricky_diff)
    check("parser keeps the ++ content line",
          parsed.get("docs/decisions/x.md", [])[:1],
          [(1, "++ Bronze is full God Tier.")])
    check("parser keeps subsequent line numbering",
          parsed.get("docs/decisions/x.md", [])[1:],
          [(2, "Second added line is full God Tier too.")])
    check("parser still maps the real header to the file",
          list(parsed.keys()), ["docs/decisions/x.md"])

    # FIND-03: --hook must fail OPEN (exit 0) on valid-but-wrong-shaped JSON.
    import io
    real_stdin = sys.stdin
    try:
        for bad_payload in ("[]", '{"tool_input": "bad"}', '{"tool_input": {"file_path": 5}}', "not json"):
            sys.stdin = io.StringIO(bad_payload)
            check(f"hook fails open on payload {bad_payload!r}", run_hook(), 0)
    finally:
        sys.stdin = real_stdin

    real_git = _git
    real_read_text = Path.read_text
    try:
        def fake_git_tracked_clean(root: Path, args: list[str]) -> tuple[int, str]:
            if args[:3] == ["diff", "--unified=0", "HEAD"]:
                return 0, ""
            if args[:2] == ["ls-files", "--error-unmatch"]:
                return 0, "tracked.md"
            return 1, ""

        def fake_git_tracked_modified(root: Path, args: list[str]) -> tuple[int, str]:
            if args[:3] == ["diff", "--unified=0", "HEAD"]:
                return 0, ("diff --git a/tracked.md b/tracked.md\n--- a/tracked.md\n"
                           "+++ b/tracked.md\n@@ -1,0 +2 @@\n+New line is full GT.\n")
            return 1, ""

        def fake_git_untracked(root: Path, args: list[str]) -> tuple[int, str]:
            if args[:3] == ["diff", "--unified=0", "HEAD"]:
                return 0, ""
            if args[:2] == ["ls-files", "--error-unmatch"]:
                return 1, ""
            return 1, ""

        def fake_read_text(path: Path, *args: object, **kwargs: object) -> str:
            if path.as_posix().endswith("untracked.md"):
                return "New file is full GT.\n"
            if path.as_posix().endswith("tracked.md"):
                return "Grandfathered full GT line.\n"
            return real_read_text(path, *args, **kwargs)

        # Installed before the tracked cases so a whole-file-fallthrough
        # regression returns content and fails the [] checks.
        Path.read_text = fake_read_text
        globals()["_git"] = fake_git_tracked_clean
        check("tracked no-diff hook scan does not whole-file fallback",
              _uncommitted_added_lines(Path("."), "tracked.md"), [])
        globals()["_git"] = fake_git_tracked_modified
        check("tracked modified hook scan returns only added line",
              _uncommitted_added_lines(Path("."), "tracked.md"), [(2, "New line is full GT.")])
        globals()["_git"] = fake_git_untracked
        check("untracked hook scan treats whole file as added",
              _uncommitted_added_lines(Path("."), "untracked.md"), [(1, "New file is full GT.")])
    finally:
        globals()["_git"] = real_git
        Path.read_text = real_read_text

    if failures:
        for failure in failures:
            print(f"SELFTEST FAIL {failure}")
        return 1
    print(f"check_full_gt_claims --selftest: OK ({cases} cases)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check added .md lines for unballasted full-GT claim language."
    )
    parser.add_argument("paths", nargs="*", help="whole-file scan targets")
    parser.add_argument("--changed", action="store_true")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--base", default=None)
    parser.add_argument("--hook", action="store_true")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()

    if args.selftest:
        return selftest()
    if args.hook:
        # Advisory contract: --hook ALWAYS exits 0, including on internal errors.
        try:
            return run_hook()
        except Exception as exc:  # fail OPEN — never block the tool call
            print(f"check_full_gt_claims --hook: internal error ({exc!r}); failing open", file=sys.stderr)
            return 0

    root = repo_root()
    if args.changed:
        findings = scan_changed(root, resolve_base_ref(args.base))
        if findings is None:
            print(
                "check_full_gt_claims: WARNING infra gap (git/base unresolvable); "
                "failing open. In CI ensure fetch-depth: 0.",
            )
            return 0
    elif args.paths:
        findings = scan_whole_files(root, args.paths)
    else:
        parser.print_usage()
        return 0

    for finding in findings:
        print(("FAIL " if args.strict else "WARN ") + finding)
    if findings and args.strict:
        return 1
    if not findings:
        print("check_full_gt_claims: OK -- no unballasted full-GT claim language in scope")
    return 0


if __name__ == "__main__":
    sys.exit(main())
