#!/usr/bin/env python3
"""Full-GT claim-inflation tripwire.

WHAT THIS DOES
  Checks ADDED lines of changed .md files for unballasted "full God Tier"
  claim language landing outside the claim-owning / record surfaces. This is
  the code substrate for the Erosion Guards ("claim inflation") named in
  orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_full_gt_declaration_v0.md
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
  check_full_gt_claims.py --hook                              PostToolUse advisory (stdin JSON; always exit 0)
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
    "orca/product/spines/data_lake/authority/"
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
    "orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_full_gt_declaration_v0.md",
    "orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md",
    "orca/product/spines/data_lake/README.md",
    "docs/workflows/orca_repo_map_v0.md",
    "docs/decisions/dcp_receipts_archive_v0.md",
}
ALLOWLIST_PREFIXES = (
    "orca/product/spines/data_lake/workflows/",
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
    files: dict[str, list[tuple[int, str]]] = {}
    current: str | None = None
    new_lineno = 0
    for raw in out.splitlines():
        if raw.startswith("+++ b/"):
            current = raw[6:].strip()
            files.setdefault(current, [])
        elif raw.startswith("@@"):
            match = re.search(r"\+(\d+)", raw)
            new_lineno = int(match.group(1)) if match else 0
        elif raw.startswith("+") and not raw.startswith("+++") and current is not None:
            files[current].append((new_lineno, raw[1:]))
            new_lineno += 1
    return files


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


def run_hook() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0
    file_path = (payload.get("tool_input") or {}).get("file_path", "")
    if not file_path:
        return 0
    root = repo_root()
    findings = scan_whole_files(root, [file_path])
    if findings:
        print(
            "full-gt-claims (advisory): " + " | ".join(findings[:5]),
            file=sys.stderr,
        )
    return 0


def selftest() -> int:
    failures: list[str] = []

    def check(name: str, actual: object, expected: object) -> None:
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
              "orca/product/spines/data_lake/workflows/some_record_v0.md", plain), None)
    check("ack token is clean",
          classify_added_line("docs/decisions/some_new_note_v0.md",
                              plain + " full-gt-claim-ack: deliberate, reviewed."), None)
    check("non-md is out of scope",
          classify_added_line("orca-harness/data_lake/catalog.py", plain), None)
    check("case-insensitive FULL GT fires",
          classify_added_line("docs/decisions/x.md", "We are FULL GT everywhere.") is not None,
          True)
    check("unrelated line is clean",
          classify_added_line("docs/decisions/x.md", "The catalog rebuilds byte-identically."),
          None)

    if failures:
        for failure in failures:
            print(f"SELFTEST FAIL {failure}")
        return 1
    print("check_full_gt_claims --selftest: OK (11 cases)")
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
        return run_hook()

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
