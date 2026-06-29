#!/usr/bin/env python3
"""Direction-change-propagation receipt hygiene checker.

WHAT THIS DOES
  Checks deterministic storage shape for Orca direction_change_propagation
  receipts in changed durable docs:

    - at most two inline direction_change_propagation receipts;
    - an archive pointer line after inline receipts;
    - no unauthorized standalone DCP receipt files.

RULE AUTHORITY
  .agents/workflow-overlay/source-of-truth.md

BOUNDARY
  Shape only. This checker does not decide whether a receipt is truthful,
  whether a doctrine change needed a receipt, whether downstream surfaces were
  actually checked, or whether a file is validated, ready, accepted, or proof.

MODES
  check_dcp_receipt_hygiene.py <path> [...]        advisory; warns, exit 0
  check_dcp_receipt_hygiene.py --strict <path>     exit 1 if any finding
  check_dcp_receipt_hygiene.py --staged [--strict] check git-staged paths
  check_dcp_receipt_hygiene.py --changed [--strict] check changed + untracked
  check_dcp_receipt_hygiene.py --selftest          pure-function cases
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys

RULE_AUTHORITY = ".agents/workflow-overlay/source-of-truth.md"
ARCHIVE_PATH = "docs/decisions/dcp_receipts_archive_v0.md"
MAX_INLINE_RECEIPTS = 2

SCOPE_PREFIXES = (
    ".agents/workflow-overlay/",
    "docs/",
    "orca/product/",
)
EXCLUDED_PREFIXES = (
    "docs/_inbox/",
    "docs/review-inputs/",
    "docs/review-outputs/",
)
TOP_LEVEL_SCOPE = {"AGENTS.md", "CLAUDE.md"}

RECEIPT_RE = re.compile(r"(?m)^\s*direction_change_propagation\s*:")
DCP_HEADING_RE = re.compile(
    r"(?im)^#{2,6}\s+direction[_ -]change[_ -]propagation\b"
)
ARCHIVE_POINTER_LINE_RE = re.compile(
    r"(?i)\b(older receipts?|archived)\b.*docs/decisions/dcp_receipts_archive_v0\.md"
)
STANDALONE_DCP_RECEIPT_PATH_RE = re.compile(
    r"(?i)(^|[/_-])(direction_change_propagation_receipts?|dcp_receipts?)([/_.-]|$)"
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


def is_authorized_archive(relposix: str) -> bool:
    return relposix == ARCHIVE_PATH


def is_dcp_scope(relposix: str) -> bool:
    if not relposix.endswith(".md"):
        return False
    if is_authorized_archive(relposix):
        return False
    if relposix in TOP_LEVEL_SCOPE:
        return True
    if any(relposix.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return False
    return any(relposix.startswith(prefix) for prefix in SCOPE_PREFIXES)


def looks_like_unauthorized_standalone_receipt(relposix: str) -> bool:
    if is_authorized_archive(relposix):
        return False
    if not relposix.endswith(".md"):
        return False
    filename = relposix.rsplit("/", 1)[-1]
    return STANDALONE_DCP_RECEIPT_PATH_RE.search(filename) is not None


def dcp_scan_region(text: str) -> tuple[int, str]:
    """Return the region where inline DCP receipts should be counted.

    If a Direction Change Propagation heading exists, count from the first such
    heading forward. This avoids treating earlier schema examples as active
    inline receipts while still catching multiple DCP subsections in one file.
    """
    match = DCP_HEADING_RE.search(text)
    if not match:
        return 0, text
    return match.end(), text[match.end():]


def receipt_offsets(text: str) -> list[int]:
    start, region = dcp_scan_region(text)
    return [start + match.start() for match in RECEIPT_RE.finditer(region)]


def has_archive_pointer_after(text: str, offset: int) -> bool:
    for line in text[offset:].splitlines():
        if ARCHIVE_POINTER_LINE_RE.search(line):
            return True
    return False


def check_text(relposix: str, text: str) -> list[Finding]:
    findings: list[Finding] = []

    if looks_like_unauthorized_standalone_receipt(relposix):
        findings.append(
            Finding(
                relposix,
                "unauthorized_standalone_dcp_receipt_file",
                f"Only {ARCHIVE_PATH} is authorized as a standalone DCP receipt archive; "
                f"store DCP receipts inline or move older receipts to the archive per {RULE_AUTHORITY}.",
            )
        )

    if is_authorized_archive(relposix) or not is_dcp_scope(relposix):
        return findings

    offsets = receipt_offsets(text)
    if len(offsets) > MAX_INLINE_RECEIPTS:
        findings.append(
            Finding(
                relposix,
                "too_many_inline_dcp_receipts",
                f"Found {len(offsets)} inline direction_change_propagation receipts; "
                f"{RULE_AUTHORITY} allows at most {MAX_INLINE_RECEIPTS} before older receipts "
                f"move to {ARCHIVE_PATH}.",
            )
        )

    if offsets and not has_archive_pointer_after(text, offsets[-1]):
        findings.append(
            Finding(
                relposix,
                "missing_dcp_archive_pointer",
                "Inline direction_change_propagation receipts require an "
                f"Older receipts archive pointer line to {ARCHIVE_PATH} after the last receipt "
                f"per {RULE_AUTHORITY}.",
            )
        )

    return findings


def check_relpath(relposix: str, root: Path) -> list[Finding]:
    findings: list[Finding] = []

    if looks_like_unauthorized_standalone_receipt(relposix):
        findings.extend(check_text(relposix, ""))
        return findings

    if not is_dcp_scope(relposix):
        return findings

    path = root / relposix
    if not path.exists():
        return findings
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        findings.append(
            Finding(
                relposix,
                "unreadable_dcp_candidate",
                f"Could not read candidate DCP receipt file: {exc}.",
            )
        )
        return findings
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
            f"dcp-receipt-hygiene: {finding.relpath}: {finding.code}: {finding.message}",
            file=sys.stderr,
        )
    if findings and not strict:
        print(
            f"dcp-receipt-hygiene: {len(findings)} advisory finding(s); "
            f"see {RULE_AUTHORITY} (advisory, exit 0).",
            file=sys.stderr,
        )
    return 1 if strict and findings else 0


def selftest() -> int:
    def codes(relpath: str, text: str) -> list[str]:
        return sorted(finding.code for finding in check_text(relpath, text))

    one_receipt_with_pointer = """# X

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "x"
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
"""

    two_receipts_with_pointer = """# X

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "x"
```

```yaml
direction_change_propagation:
  doctrine_changed: "y"
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
"""

    three_receipts_with_pointer = """# X

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "x"
```

```yaml
direction_change_propagation:
  doctrine_changed: "y"
```

```yaml
direction_change_propagation:
  doctrine_changed: "z"
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
"""

    example_then_real = """# X

Use this receipt shape:

```yaml
direction_change_propagation:
  doctrine_changed: "<one sentence>"
```

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "actual"
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
"""

    blocker_only = """# X

## Direction Change Propagation

```yaml
direction_change_propagation_blocker:
  doctrine_changed: "x"
```
"""

    cases = [
        ("no receipt", "docs/decisions/x_v0.md", "# X\n", []),
        ("one receipt ok", "docs/decisions/x_v0.md", one_receipt_with_pointer, []),
        ("two receipts ok", "docs/decisions/x_v0.md", two_receipts_with_pointer, []),
        (
            "three receipts fail",
            "docs/decisions/x_v0.md",
            three_receipts_with_pointer,
            ["too_many_inline_dcp_receipts"],
        ),
        (
            "missing pointer fail",
            "docs/decisions/x_v0.md",
            "## Direction Change Propagation\n\ndirection_change_propagation:\n  doctrine_changed: x\n",
            ["missing_dcp_archive_pointer"],
        ),
        ("schema example ignored", "docs/decisions/x_v0.md", example_then_real, []),
        (
            "authorized archive ignored",
            ARCHIVE_PATH,
            three_receipts_with_pointer,
            [],
        ),
        (
            "unauthorized standalone dcp receipt file",
            "docs/decisions/new_dcp_receipt_v0.md",
            "# X\n",
            ["unauthorized_standalone_dcp_receipt_file"],
        ),
        (
            "doctrine-change decision path not standalone receipt",
            "docs/decisions/doctrine_change_propagation_restatement_integrity_decision_v0.md",
            "# X\n",
            [],
        ),
        (
            "checker script name is not a standalone receipt artifact",
            ".agents/hooks/check_dcp_receipt_hygiene.py",
            "# code\n",
            [],
        ),
        ("blocker only", "docs/decisions/x_v0.md", blocker_only, []),
    ]

    ok = True
    for index, (label, relpath, text, expected) in enumerate(cases, start=1):
        got = codes(relpath, text)
        passed = got == expected
        if not passed:
            ok = False
        status = "PASS" if passed else "FAIL"
        print(
            f"{status} case {index:02d} {label}: expect={expected} got={got}"
        )
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Check DCP receipt storage shape. "
        f"Rule authority: {RULE_AUTHORITY}"
    )
    parser.add_argument("paths", nargs="*", help="explicit file paths to check")
    parser.add_argument("--staged", action="store_true", help="check git-staged paths")
    parser.add_argument(
        "--changed",
        action="store_true",
        help="check changed + staged + untracked paths",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 if any DCP receipt hygiene finding exists",
    )
    parser.add_argument("--selftest", action="store_true", help="run pure-function cases")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    root = repo_root()
    relpaths: list[str | None] = []
    if args.staged:
        relpaths.extend(staged_paths(root))
    if args.changed:
        relpaths.extend(changed_paths(root))
    relpaths.extend(to_relposix(path, root) for path in args.paths)

    selection_requested = bool(args.paths or args.staged or args.changed)
    if not relpaths and selection_requested:
        print("dcp-receipt-hygiene: no DCP receipt candidate files selected -- OK")
        return 0
    if not relpaths:
        parser.print_usage(sys.stderr)
        return 2

    return report(collect_findings(relpaths, root), args.strict)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
