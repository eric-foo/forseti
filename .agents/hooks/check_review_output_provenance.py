#!/usr/bin/env python3
"""Review-output provenance and use-boundary checker.

WHAT THIS DOES
  Checks new or materially changed Forseti review outputs for the mechanical
  fields and artifact integrity needed by later adjudication:

    - retrieval header shape;
    - reviewed_by and authored_by provenance fields;
    - review-use boundary text that frames findings as decision input and not
      approval, validation, mandatory remediation, or patch authority;
    - balanced, well-formed Markdown fences;
    - embedded git diffs kept inside proper ```diff fences;
    - no collapsed one-line diffs from unsafe report assembly;
    - no future-tense provenance/check placeholders after final write;
    - no trailing whitespace.

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
  check_review_output_provenance.py --diff BASE [--strict]
                                                      check committed BASE...HEAD paths
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
NEGATION_RE = re.compile(r"\b(?:not|no|never)\b", re.IGNORECASE)
# Complete required non-claim set per .agents/workflow-overlay/review-lanes.md:
# "not approval, validation, mandatory remediation, or executor-ready patch
# authority" -- all four concepts must be present, not just one.
REQUIRED_NON_CLAIM_TERMS = {
    "approval": re.compile(r"\bapproval\b", re.IGNORECASE),
    "validation": re.compile(r"\bvalidation\b", re.IGNORECASE),
    "mandatory_remediation": re.compile(r"\bmandatory\s+remediation\b", re.IGNORECASE),
    "patch_authority": re.compile(
        r"\b(?:executor[- ]ready(?:\s+patch\s+authority)?|patch\s+authority)\b",
        re.IGNORECASE,
    ),
}
NON_CLAIM_WINDOW_CHARS = 400
FINDINGS_RE = re.compile(r"\bfindings?\b", re.IGNORECASE)
REVIEW_USE_BOUNDARY_FIELD_RE = re.compile(
    r"(?mis)^\s*review_use_boundary\s*:\s*(?:>\s*)?(?P<value>.*?)(?=^\S|\Z)"
)
FENCE_RE = re.compile(r"^```(?P<info>.*)$")
FENCE_INFO_RE = re.compile(r"^[A-Za-z0-9_-]+$")
# A future-tense provenance/check placeholder is a promise to check, verify,
# confirm, or record a result at some point after the report is finalized,
# rather than recording an observed result now. Match the semantic class
# (future modal + checking verb, tied to a report-completion trigger), not
# only the exact wordings the checker happened to be authored against.
_FUTURE_MODAL = r"(?:will|must|should|shall|is\s+to|are\s+to)\s+be\s+(?:checked|verified|confirmed|recorded|reran|rerun|run)"
_COMPLETION_TRIGGER = (
    r"(?:after|once|when|upon)\s+(?:this\s+)?(?:report(?:\s+is)?\s+)?"
    r"(?:written|saved|merged|committed|finalized|closed[- ]out|post[- ]write)"
)
FUTURE_CHECK_RE = re.compile(
    r"(?:"
    rf"{_FUTURE_MODAL}.{{0,100}}?{_COMPLETION_TRIGGER}|"
    rf"{_COMPLETION_TRIGGER}.{{0,100}}?{_FUTURE_MODAL}|"
    r"final\s+chat\s+closeout\s+records\s+the\s+observed\s+result|"
    r"report\s+provenance\s+command\s+runs\s+after\s+durable\s+write"
    r")",
    re.IGNORECASE,
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


class GitSelectionError(RuntimeError):
    """Raised when a git path-selection command could not be evaluated.

    This is distinct from a git command that ran and legitimately selected
    zero paths; callers must not treat the two as equivalent.
    """


def git_lines(root: Path, args: list[str]) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, OSError) as exc:
        raise GitSelectionError(f"git {' '.join(args)} could not run: {exc}") from exc
    if result.returncode != 0:
        stderr = result.stderr.strip()
        detail = f": {stderr}" if stderr else ""
        raise GitSelectionError(f"git {' '.join(args)} exited {result.returncode}{detail}")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def staged_paths(root: Path) -> list[str]:
    return git_lines(root, ["diff", "--cached", "--name-only", "--diff-filter=ACMR"])


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


def diff_paths(root: Path, base: str) -> list[str]:
    """Added/modified relpaths in `base...HEAD` for CI-scoped committed diffs."""
    return git_lines(root, ["diff", "--diff-filter=ACMR", "--find-renames", "--name-only", f"{base}...HEAD"])

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


def _has_complete_non_claim_set(candidate: str) -> bool:
    negation_match = NEGATION_RE.search(candidate)
    if negation_match is None:
        return False
    window = candidate[negation_match.start() : negation_match.start() + NON_CLAIM_WINDOW_CHARS]
    return all(pattern.search(window) is not None for pattern in REQUIRED_NON_CLAIM_TERMS.values())


def _has_review_use_boundary(text: str) -> bool:
    for candidate in _review_use_boundary_candidates(text):
        if DECISION_INPUT_RE.search(candidate) is not None and _has_complete_non_claim_set(candidate):
            return True
    return False


def _fence_findings(relposix: str, lines: list[str]) -> list[Finding]:
    findings: list[Finding] = []
    fence_count = 0
    active_info: str | None = None
    inside_diff = False

    for index, line in enumerate(lines, 1):
        match = FENCE_RE.match(line)
        if match:
            fence_count += 1
            raw_info = match.group("info")
            normalized = raw_info.strip()
            if raw_info != normalized or (normalized and FENCE_INFO_RE.fullmatch(normalized) is None):
                findings.append(
                    Finding(
                        relposix,
                        "malformed_code_fence",
                        f"Line {index} has malformed fenced-code marker `{line}`; use bare ``` or a single language token.",
                    )
                )

            if active_info is None:
                active_info = normalized or ""
                inside_diff = active_info == "diff"
            else:
                active_info = None
                inside_diff = False
            continue

        if line.startswith("diff --git ") and not inside_diff:
            findings.append(
                Finding(
                    relposix,
                    "diff_line_outside_diff_fence",
                    f"Line {index} starts with `diff --git` outside a ```diff fence.",
                )
            )

        if inside_diff and line.startswith("diff --git ") and any(
            token in line for token in (" index ", " --- ", " +++ ", " @@ ")
        ):
            findings.append(
                Finding(
                    relposix,
                    "collapsed_diff_block",
                    f"Line {index} looks like multiple git-diff lines collapsed into one line.",
                )
            )

    if fence_count % 2:
        findings.append(
            Finding(
                relposix,
                "unbalanced_code_fences",
                "Review output has an odd number of fenced-code markers.",
            )
        )
    return findings


def _integrity_findings(relposix: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = text.splitlines()
    findings.extend(_fence_findings(relposix, lines))

    for index, line in enumerate(lines, 1):
        if line.rstrip(" \t") != line:
            findings.append(
                Finding(
                    relposix,
                    "trailing_whitespace",
                    f"Line {index} has trailing whitespace.",
                )
            )
        if FUTURE_CHECK_RE.search(line):
            findings.append(
                Finding(
                    relposix,
                    "future_tense_review_output_check",
                    f"Line {index} contains a future-tense provenance/check placeholder; record observed results only.",
                )
            )
    return findings


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

    findings.extend(_integrity_findings(relposix, text))

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
            "shape/integrity only, exit 0.",
            file=sys.stderr,
        )
    return 1 if strict and findings else 0


FIXTURE_EXPECTED_RE = re.compile(r"fixture_expected:\s*(pass|fail)")
FIXTURE_EXPECTED_CODES_RE = re.compile(r"fixture_expected_codes:\s*([^>]+?)\s*-->")


def _fixture_metadata(text: str) -> tuple[str, set[str] | None]:
    header = "\n".join(text.splitlines()[:5])
    expected_match = FIXTURE_EXPECTED_RE.search(header)
    expected = expected_match.group(1) if expected_match else ""
    codes_match = FIXTURE_EXPECTED_CODES_RE.search(header)
    if codes_match is None:
        return expected, None
    codes = {code.strip() for code in codes_match.group(1).split(",") if code.strip()}
    return expected, codes


def selftest() -> int:
    root = repo_root()
    fixture_dir = root / "forseti-harness" / "tests" / "fixtures" / "review_outputs"
    fixture_paths = sorted(fixture_dir.glob("*.md"))
    if not fixture_paths:
        print(f"SELFTEST FAILED: no fixtures found at {fixture_dir}")
        return 1

    ok = True
    for path in fixture_paths:
        text = path.read_text(encoding="utf-8")
        expected, expected_codes = _fixture_metadata(text)
        relpath = "docs/review-outputs/adversarial-artifact-reviews/" + path.name
        findings = check_text(relpath, text)
        found_codes = {f.code for f in findings}
        passed = not findings
        if expected == "pass" and passed:
            print(f"PASS {path.name}")
        elif expected == "fail" and not passed:
            if expected_codes is not None and not expected_codes.issubset(found_codes):
                ok = False
                missing = sorted(expected_codes - found_codes)
                print(f"FAIL {path.name} missing expected codes {missing}; found={sorted(found_codes)}")
            else:
                print(f"PASS {path.name} expected fail: {', '.join(sorted(found_codes))}")
        else:
            ok = False
            print(f"FAIL {path.name} expected={expected or '<missing>'} findings={findings}")
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Check changed Forseti review outputs for provenance, use-boundary, and integrity shape."
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
    try:
        if args.staged:
            relpaths.extend(staged_paths(root))
        if args.changed:
            relpaths.extend(changed_paths(root))
        if args.diff:
            relpaths.extend(diff_paths(root, args.diff))
    except GitSelectionError as exc:
        print(f"review-output-provenance: selection could not be evaluated: {exc}", file=sys.stderr)
        return 2
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
