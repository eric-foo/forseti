#!/usr/bin/env python3
"""Review-output provenance and use-boundary checker.

WHAT THIS DOES
  Checks new or materially changed Orca review outputs for the mechanical
  fields needed by later adjudication:

    - retrieval header shape;
    - reviewed_by and authored_by provenance fields;
    - review-use boundary text that frames findings as decision input and not
      approval, validation, mandatory remediation, or patch authority.

RULE AUTHORITY
  .agents/workflow-overlay/review-lanes.md
  .agents/workflow-overlay/retrieval-metadata.md

BOUNDARY
  Shape only. This checker does not verify reviewer identity, decide
  de-correlation truth, grade findings, validate review quality, approve
  remediation, or backfill historical review outputs.

MODES
  check_review_output_provenance.py <path> [...]        advisory; warns, exit 0
  check_review_output_provenance.py --strict <path>     exit 1 if any finding
  check_review_output_provenance.py --staged [--strict] check git-staged paths
  check_review_output_provenance.py --changed [--strict] check changed + untracked
  check_review_output_provenance.py --diff BASE [--strict] check committed BASE...HEAD (CI mode; --changed sees only the working tree, which is clean in CI)
  check_review_output_provenance.py --selftest          fixture/selftest cases
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import importlib.util
from pathlib import Path
import re
import subprocess
import sys

REVIEW_LANES_AUTHORITY = ".agents/workflow-overlay/review-lanes.md"
RETRIEVAL_METADATA_AUTHORITY = ".agents/workflow-overlay/retrieval-metadata.md"
REVIEW_OUTPUT_PREFIX = "docs/review-outputs/"

FIELD_RE_TEMPLATE = r"(?mi)^\s*{field}\s*:\s*(?P<value>.*?)\s*$"
REVIEWED_BY_RE = re.compile(FIELD_RE_TEMPLATE.format(field="reviewed_by"))
AUTHORED_BY_RE = re.compile(FIELD_RE_TEMPLATE.format(field="authored_by"))
DECISION_INPUT_RE = re.compile(r"\bdecision\s+input\b", re.IGNORECASE)
NON_APPROVAL_RE = re.compile(
    r"\b(?:not|no|never)\b.{0,240}\b(?:approval|validation|mandatory\s+remediation|"
    r"executor[- ]ready|patch\s+authority|readiness)\b",
    re.IGNORECASE | re.DOTALL,
)
FINDINGS_RE = re.compile(r"\bfindings?\b", re.IGNORECASE)
REVIEW_USE_BOUNDARY_FIELD_RE = re.compile(
    r"(?mis)^\s*review_use_boundary\s*:\s*(?:>\s*)?(?P<value>.*?)(?=^\S|\Z)"
)


@dataclass(frozen=True)
class Finding:
    relpath: str
    code: str
    message: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def to_relposix(target: str, root: Path) -> str | None:
    path = Path(target)
    if path.is_absolute():
        try:
            return path.resolve().relative_to(root).as_posix()
        except (OSError, ValueError):
            return None
    value = path.as_posix()
    return value[2:] if value.startswith("./") else value


def git_lines(root: Path, args: list[str]) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, OSError):
        return []
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def staged_paths(root: Path) -> list[str]:
    return git_lines(root, ["diff", "--cached", "--name-only", "--diff-filter=ACMR"])


def diff_paths(root: Path, base_ref: str) -> list[str] | None:
    """Added/modified relpaths in `base_ref...HEAD` (committed net change).

    Returns None on a git infra gap (no HEAD, unresolvable base) so the caller
    can fail OPEN loudly -- the universal Orca infra-gap stance; in CI the base
    is always present (fetch-depth: 0). This is the CI-scoped mode: --changed
    scans the working tree, which is always clean in a CI checkout.
    """
    try:
        for probe in ("HEAD", base_ref):
            result = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "--verify", "--quiet", probe],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                return None
    except (FileNotFoundError, OSError):
        return None
    return git_lines(
        root,
        ["diff", "--diff-filter=ACMR", "--find-renames", "--name-only",
         f"{base_ref}...HEAD"],
    )


def changed_paths(root: Path) -> list[str]:
    paths: list[str] = []
    for args in (
        ["diff", "--name-only", "--diff-filter=ACMR"],
        ["diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        for path in git_lines(root, args):
            if path not in paths:
                paths.append(path)
    return paths


def _load_retrieval_header_checker():
    hooks_dir = Path(__file__).resolve().parent
    module_path = hooks_dir / "check_retrieval_header.py"
    spec = importlib.util.spec_from_file_location("check_retrieval_header", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def is_review_output_scope(relposix: str) -> bool:
    if not relposix.startswith(REVIEW_OUTPUT_PREFIX) or not relposix.endswith(".md"):
        return False
    return Path(relposix).name != "README.md"


def _field_value(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    if not match:
        return None
    return match.group("value").strip().strip("'\"")


def _review_use_boundary_candidates(text: str) -> list[str]:
    candidates = [match.group("value") for match in REVIEW_USE_BOUNDARY_FIELD_RE.finditer(text)]
    candidates.extend(block for block in re.split(r"\n\s*\n", text) if FINDINGS_RE.search(block))
    return candidates


def _has_review_use_boundary(text: str) -> bool:
    for candidate in _review_use_boundary_candidates(text):
        if DECISION_INPUT_RE.search(candidate) is not None and NON_APPROVAL_RE.search(candidate) is not None:
            return True
    return False


def check_text(relposix: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    if not is_review_output_scope(relposix):
        return findings

    header_checker = _load_retrieval_header_checker()
    header_problems = header_checker.header_problems_for_lines(text.splitlines()[: header_checker.HEAD_LINES])
    for problem in header_problems:
        findings.append(
            Finding(
                relposix,
                "review_output_retrieval_header_invalid",
                f"{problem}. See {RETRIEVAL_METADATA_AUTHORITY}.",
            )
        )

    for field, pattern in (("reviewed_by", REVIEWED_BY_RE), ("authored_by", AUTHORED_BY_RE)):
        value = _field_value(pattern, text)
        if value is None:
            findings.append(
                Finding(
                    relposix,
                    f"missing_{field}",
                    f"Review outputs require `{field}` per {REVIEW_LANES_AUTHORITY}; use `unrecorded` if not supplied.",
                )
            )
        elif not value:
            findings.append(
                Finding(
                    relposix,
                    f"blank_{field}",
                    f"`{field}` is present but blank; use `unrecorded` if the identity was not supplied.",
                )
            )

    if not _has_review_use_boundary(text):
        findings.append(
            Finding(
                relposix,
                "missing_review_use_boundary",
                "Review output must say findings are decision input and not approval, validation, "
                f"mandatory remediation, or patch authority per {REVIEW_LANES_AUTHORITY}.",
            )
        )

    return findings


def check_relpath(relposix: str, root: Path) -> list[Finding]:
    if not is_review_output_scope(relposix):
        return []
    path = root / relposix
    if not path.exists() or not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return [
            Finding(
                relposix,
                "unreadable_review_output",
                f"Could not read review-output candidate: {exc}.",
            )
        ]
    return check_text(relposix, text)


def collect_findings(relpaths: list[str | None], root: Path) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[str] = set()
    for rel in relpaths:
        if rel is None or rel in seen:
            continue
        seen.add(rel)
        findings.extend(check_relpath(rel, root))
    return findings


def report(findings: list[Finding], strict: bool) -> int:
    for finding in findings:
        print(
            f"review-output-provenance: {finding.relpath}: {finding.code}: {finding.message}",
            file=sys.stderr,
        )
    if findings and not strict:
        print(
            f"review-output-provenance: {len(findings)} advisory finding(s); "
            "shape only, exit 0.",
            file=sys.stderr,
        )
    return 1 if strict and findings else 0


def selftest() -> int:
    root = repo_root()
    fixture_dir = root / "orca-harness" / "tests" / "fixtures" / "review_outputs"
    fixture_paths = sorted(fixture_dir.glob("*.md"))
    if not fixture_paths:
        print(f"SELFTEST FAILED: no fixtures found at {fixture_dir}")
        return 1

    ok = True
    for path in fixture_paths:
        first_line = path.read_text(encoding="utf-8").splitlines()[0]
        match = re.search(r"fixture_expected:\s*(pass|fail)", first_line)
        expected = match.group(1) if match else ""
        relpath = "docs/review-outputs/adversarial-artifact-reviews/" + path.name
        findings = check_text(relpath, path.read_text(encoding="utf-8"))
        passed = not findings
        if expected == "pass" and passed:
            print(f"PASS {path.name}")
        elif expected == "fail" and not passed:
            print(f"PASS {path.name} expected fail: {', '.join(sorted({f.code for f in findings}))}")
        else:
            ok = False
            print(f"FAIL {path.name} expected={expected or '<missing>'} findings={findings}")
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Check changed Orca review outputs for provenance and review-use boundary shape."
    )
    parser.add_argument("paths", nargs="*", help="explicit review-output files to check")
    parser.add_argument("--staged", action="store_true", help="check git-staged paths")
    parser.add_argument("--changed", action="store_true", help="check changed + staged + untracked paths")
    parser.add_argument("--diff", metavar="BASE_REF", default=None,
                        help="check committed net change BASE_REF...HEAD (CI mode)")
    parser.add_argument("--strict", action="store_true", help="exit 1 if any finding exists")
    parser.add_argument("--selftest", action="store_true", help="run fixture/selftest cases")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    root = repo_root()
    relpaths: list[str | None] = []
    if args.staged:
        relpaths.extend(staged_paths(root))
    if args.changed:
        relpaths.extend(changed_paths(root))
    if args.diff:
        diffed = diff_paths(root, args.diff)
        if diffed is None:
            print(
                "review-output-provenance: WARNING infra gap (git or base ref "
                f"{args.diff!r} unresolvable); failing open. In CI ensure fetch-depth: 0.",
                file=sys.stderr,
            )
            return 0
        relpaths.extend(diffed)
    relpaths.extend(to_relposix(path, root) for path in args.paths)

    selection_requested = bool(args.paths or args.staged or args.changed or args.diff)
    if not relpaths and selection_requested:
        print("review-output-provenance: no review-output files selected -- OK")
        return 0
    if not relpaths:
        parser.print_usage(sys.stderr)
        return 2

    return report(collect_findings(relpaths, root), args.strict)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
