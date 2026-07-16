#!/usr/bin/env python3
"""Engagement stale-doctrine phrase sweep.

WHAT THIS DOES
  Finds a small curated set of superseded engagement/resonance doctrine phrases
  when they appear in live Forseti doctrine surfaces.

RULE AUTHORITY
  docs/hygiene/engagement_resonance_enforcement_goal_handoff_v0.md
  forseti/product/shared/engagement_registry/engagement_logic_registry_v0.md

BOUNDARY
  Leakage detection only. This checker does not prove doctrine coherence,
  validation, readiness, proof, buyer proof, acceptance, or resonance judgment.
  It does not score engagement and does not rewrite stale text.

MODES
  check_engagement_stale_phrases.py --live [--strict]      check live doctrine
  check_engagement_stale_phrases.py --changed [--strict]   check changed live docs
  check_engagement_stale_phrases.py --staged [--strict]    check staged live docs
  check_engagement_stale_phrases.py <path> [...]           check selected paths
  check_engagement_stale_phrases.py --include-excluded ... include historical paths
  check_engagement_stale_phrases.py --selftest             pure-function cases
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hooklib import (  # noqa: E402  (sys.path pin must precede the import)
    git_lines,
    repo_root,
)

HANDOFF_AUTHORITY = "docs/hygiene/engagement_resonance_enforcement_goal_handoff_v0.md"
REGISTRY_AUTHORITY = "forseti/product/shared/engagement_registry/engagement_logic_registry_v0.md"

LIVE_PREFIXES = (
    "forseti/product/",
    "docs/decisions/",
)
EXCLUDED_PREFIXES = (
    "docs/prompts/",
    "docs/review-inputs/",
    "docs/review-outputs/",
    "docs/hygiene/",
    "docs/migration/",
    "docs/_inbox/",
)
EXCLUDED_EXACT = {
    "docs/decisions/dcp_receipts_archive_v0.md",
}

FENCE_RE = re.compile(r"(?ms)^```[A-Za-z0-9_-]*\s*\n.*?^```", re.MULTILINE)


@dataclass(frozen=True)
class PhraseRule:
    code: str
    pattern: re.Pattern[str]
    label: str


PHRASE_RULES = (
    PhraseRule(
        "stale_score_boost_phrase",
        re.compile(
            r"\b(?:engagement context is not a score boost|"
            r"not a score boost;\s*it remains attention-priority|"
            r"engagement[- ]score[- ]boost)\b",
            re.IGNORECASE,
        ),
        "old score-boost shorthand",
    ),
    PhraseRule(
        "stale_attention_routing_phrase",
        re.compile(r"\battention and routing cue\b", re.IGNORECASE),
        "old attention-routing shorthand",
    ),
    PhraseRule(
        "stale_attention_only_phrase",
        re.compile(
            r"\b(?:weak/attention-only|attention-only (?:input|evidence)|"
            r"engagement-only (?:evidence|signal)|"
            r"attention/engagement volume (?:alone|standing alone))\b",
            re.IGNORECASE,
        ),
        "old attention-only shorthand",
    ),
    PhraseRule(
        "stale_engagement_only_cap_phrase",
        re.compile(
            r"\b(?:engagement-only (?:cap|caps|memo|cannot)|"
            r"engagement volume alone|convergence asserted on engagement volume)\b",
            re.IGNORECASE,
        ),
        "old engagement-only cap shorthand",
    ),
    PhraseRule(
        "stale_engagement_proof_phrase",
        re.compile(r"\bengagement-proof\b", re.IGNORECASE),
        "old engagement-proof shorthand",
    ),
)


@dataclass(frozen=True)
class Finding:
    relpath: str
    line: int
    code: str
    message: str
    scope: str = "live"


@dataclass(frozen=True)
class IgnoredMatch:
    relpath: str
    line: int
    code: str
    reason: str


@dataclass(frozen=True)
class ScanResult:
    findings: list[Finding]
    ignored: list[IgnoredMatch]
    checked_files: int
    skipped_files: int


# Kept local: drifted from _hooklib.to_relposix (no empty/rooted-path -> None handling; FIND-01 class).
def to_relposix(target: str, root: Path) -> str | None:
    path = Path(target)
    if path.is_absolute():
        try:
            return path.resolve().relative_to(root).as_posix()
        except (OSError, ValueError):
            return None
    value = path.as_posix()
    return value[2:] if value.startswith("./") else value


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


def scope_for(relposix: str) -> str:
    if not relposix.endswith(".md"):
        return "out_of_scope"
    if relposix in EXCLUDED_EXACT:
        return "excluded"
    if any(relposix.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return "excluded"
    if any(relposix.startswith(prefix) for prefix in LIVE_PREFIXES):
        return "live"
    return "out_of_scope"


def iter_md_under(relposix: str, root: Path) -> list[str]:
    path = root / relposix
    if path.is_file():
        return [relposix]
    if not path.is_dir():
        return [relposix]
    rels: list[str] = []
    for child in sorted(path.rglob("*.md")):
        try:
            rels.append(child.relative_to(root).as_posix())
        except ValueError:
            continue
    return rels


def live_paths(root: Path) -> list[str]:
    rels: list[str] = []
    for prefix in LIVE_PREFIXES:
        path = root / prefix
        if not path.exists():
            continue
        for child in sorted(path.rglob("*.md")):
            try:
                rel = child.relative_to(root).as_posix()
            except ValueError:
                continue
            if scope_for(rel) == "live":
                rels.append(rel)
    return rels


def self_reference_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    for match in FENCE_RE.finditer(text):
        body = match.group(0)
        if "direction_change_propagation" in body or "stale_language_search" in body:
            ranges.append((match.start(), match.end()))
    return ranges


def inside_ranges(offset: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start <= offset < end for start, end in ranges)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def excerpt(value: str, limit: int = 120) -> str:
    compact = " ".join(value.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def check_text(relposix: str, text: str, include_excluded: bool = False) -> tuple[list[Finding], list[IgnoredMatch]]:
    scope = scope_for(relposix)
    if scope == "out_of_scope" or (scope == "excluded" and not include_excluded):
        return [], []

    ignored_ranges = self_reference_ranges(text)
    findings: list[Finding] = []
    ignored: list[IgnoredMatch] = []
    for rule in PHRASE_RULES:
        for match in rule.pattern.finditer(text):
            line = line_number(text, match.start())
            if inside_ranges(match.start(), ignored_ranges):
                ignored.append(
                    IgnoredMatch(
                        relposix,
                        line,
                        rule.code,
                        "self-reference or DCP receipt text",
                    )
                )
                continue
            findings.append(
                Finding(
                    relposix,
                    line,
                    rule.code,
                    f"{rule.label}: {excerpt(match.group(0))!r}. "
                    f"See {HANDOFF_AUTHORITY} and {REGISTRY_AUTHORITY}.",
                    scope,
                )
            )
    return findings, ignored


def check_relpath(relposix: str, root: Path, include_excluded: bool) -> ScanResult:
    expanded = iter_md_under(relposix, root)
    findings: list[Finding] = []
    ignored: list[IgnoredMatch] = []
    checked_files = 0
    skipped_files = 0

    for rel in expanded:
        scope = scope_for(rel)
        if scope == "out_of_scope" or (scope == "excluded" and not include_excluded):
            skipped_files += 1
            continue
        path = root / rel
        if not path.exists() or not path.is_file():
            skipped_files += 1
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            findings.append(
                Finding(
                    rel,
                    0,
                    "unreadable_stale_phrase_candidate",
                    f"Could not read stale-phrase candidate: {exc}.",
                    scope,
                )
            )
            continue
        checked_files += 1
        file_findings, file_ignored = check_text(rel, text, include_excluded)
        findings.extend(file_findings)
        ignored.extend(file_ignored)

    return ScanResult(findings, ignored, checked_files, skipped_files)


def collect_findings(relpaths: list[str | None], root: Path, include_excluded: bool) -> ScanResult:
    findings: list[Finding] = []
    ignored: list[IgnoredMatch] = []
    checked_files = 0
    skipped_files = 0
    seen: set[str] = set()
    for rel in relpaths:
        if rel is None or rel in seen:
            continue
        seen.add(rel)
        result = check_relpath(rel, root, include_excluded)
        findings.extend(result.findings)
        ignored.extend(result.ignored)
        checked_files += result.checked_files
        skipped_files += result.skipped_files
    return ScanResult(findings, ignored, checked_files, skipped_files)


def report(result: ScanResult, strict: bool) -> int:
    for finding in result.findings:
        line = f":{finding.line}" if finding.line else ""
        print(
            f"engagement-stale-phrases: {finding.relpath}{line}: "
            f"{finding.code}: {finding.message}",
            file=sys.stderr,
        )
    if result.ignored:
        print(
            f"engagement-stale-phrases: ignored {len(result.ignored)} "
            "self-reference/DCP match(es); live findings are reported separately.",
            file=sys.stderr,
        )
    if result.findings:
        if not strict:
            print(
                f"engagement-stale-phrases: {len(result.findings)} advisory finding(s); "
                "leakage detection only, exit 0.",
                file=sys.stderr,
            )
        return 1 if strict else 0
    print(
        f"engagement-stale-phrases: OK ({result.checked_files} file(s) checked, "
        f"{result.skipped_files} skipped)"
    )
    return 0


def selftest() -> int:
    def codes(relpath: str, text: str, include_excluded: bool = False) -> tuple[list[str], int]:
        findings, ignored = check_text(relpath, text, include_excluded)
        return sorted(finding.code for finding in findings), len(ignored)

    dcp_self_ref = """# Registry

## Direction Change Propagation

```yaml
direction_change_propagation:
  stale_language_search: >
    rg -n "attention and routing cue"
```
"""
    current_non_claims = (
        "Engagement context is not proof or a numeric score boost.\n"
        "Do not interpret whether engagement proves demand.\n"
        "Forbidden contents include any ranking that treats engagement as proof.\n"
    )
    cases = [
        (
            "live stale phrase",
            codes("forseti/product/x.md", "This says attention and routing cue."),
            (["stale_attention_routing_phrase"], 0),
        ),
        (
            "live engagement-proof phrase",
            codes("docs/decisions/x.md", "This old engagement-proof shortcut returned."),
            (["stale_engagement_proof_phrase"], 0),
        ),
        (
            "current non-claim boundary not stale",
            codes("forseti/product/x.md", current_non_claims),
            ([], 0),
        ),
        (
            "DCP self-reference ignored",
            codes("forseti/product/shared/engagement_registry/x.md", dcp_self_ref),
            ([], 1),
        ),
        (
            "historical prompt excluded by default",
            codes("docs/prompts/reviews/x.md", "attention-only evidence"),
            ([], 0),
        ),
        (
            "historical prompt explicit include",
            codes("docs/prompts/reviews/x.md", "attention-only evidence", include_excluded=True),
            (["stale_attention_only_phrase"], 0),
        ),
        (
            "DCP archive excluded by default",
            codes("docs/decisions/dcp_receipts_archive_v0.md", "engagement volume alone"),
            ([], 0),
        ),
    ]

    ok = True
    for index, (label, got, expected) in enumerate(cases, start=1):
        passed = got == expected
        if not passed:
            ok = False
        status = "PASS" if passed else "FAIL"
        print(f"{status} case {index:02d} {label}: expect={expected!r} got={got!r}")
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Check stale engagement/resonance doctrine phrase leaks."
    )
    parser.add_argument("paths", nargs="*", help="explicit files or directories to check")
    parser.add_argument("--live", action="store_true", help="check live doctrine roots")
    parser.add_argument("--staged", action="store_true", help="check staged paths")
    parser.add_argument("--changed", action="store_true", help="check changed + staged + untracked paths")
    parser.add_argument("--strict", action="store_true", help="exit 1 if live stale phrase findings exist")
    parser.add_argument(
        "--include-excluded",
        action="store_true",
        help="include historical prompts, review outputs, hygiene notes, and archives",
    )
    parser.add_argument("--selftest", action="store_true", help="run pure-function cases")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    root = repo_root()
    relpaths: list[str | None] = []
    if args.live:
        relpaths.extend(live_paths(root))
    if args.staged:
        relpaths.extend(staged_paths(root))
    if args.changed:
        relpaths.extend(changed_paths(root))
    relpaths.extend(to_relposix(path, root) for path in args.paths)

    selection_requested = bool(args.paths or args.live or args.staged or args.changed)
    if not relpaths and selection_requested:
        print("engagement-stale-phrases: no live doctrine files selected -- OK")
        return 0
    if not relpaths:
        parser.print_usage(sys.stderr)
        return 2

    return report(collect_findings(relpaths, root, args.include_excluded), args.strict)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
