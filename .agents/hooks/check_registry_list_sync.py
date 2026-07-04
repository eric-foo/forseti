#!/usr/bin/env python3
"""Registry/list synchronization checker for narrow Forseti vocabulary bindings.

WHAT THIS DOES
  Checks one explicit vocabulary binding:

    Information Production Foundation Allowed Signal Uses
    must be contained by Engagement Logic Registry Signal Use Classification.

RULE AUTHORITY
  forseti/product/shared/engagement_registry/engagement_logic_registry_v0.md
  forseti/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md

BOUNDARY
  Shape/list sync only. This checker does not decide whether a category should
  exist, does not auto-edit either source, does not build an ontology system,
  and does not prove validation, readiness, acceptance, or product correctness.

MODES
  check_registry_list_sync.py --live [--strict]      check the registered binding
  check_registry_list_sync.py --changed [--strict]   check only if binding files changed
  check_registry_list_sync.py --staged [--strict]    check only if binding files staged
  check_registry_list_sync.py <path> [...]           check if paths touch a binding
  check_registry_list_sync.py --selftest             pure-function cases
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys

ENGAGEMENT_REGISTRY = "forseti/product/shared/engagement_registry/engagement_logic_registry_v0.md"
FOUNDATION = "forseti/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md"

SECTION_HEADING_RE = re.compile(r"(?m)^(#{2,6})\s+(.+?)\s*$")
BULLET_RE = re.compile(r"^\s*-\s+(.+?)\s*$")


@dataclass(frozen=True)
class Binding:
    name: str
    source_path: str
    source_heading: str
    registry_path: str
    registry_heading: str


@dataclass(frozen=True)
class Finding:
    binding: str
    code: str
    message: str


SIGNAL_USE_BINDING = Binding(
    name="foundation_signal_use_to_engagement_registry",
    source_path=FOUNDATION,
    source_heading="Allowed Signal Uses",
    registry_path=ENGAGEMENT_REGISTRY,
    registry_heading="Signal Use Classification",
)
BINDINGS = (SIGNAL_USE_BINDING,)


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


def normalize_item(value: str) -> str:
    value = value.strip().strip("`*_ ")
    value = re.sub(r"[.;:,]+$", "", value.strip())
    value = re.sub(r"\s+", " ", value)
    return value.casefold()


def find_section_body(text: str, heading: str) -> str | None:
    matches = list(SECTION_HEADING_RE.finditer(text))
    target = normalize_item(heading)
    for index, match in enumerate(matches):
        if normalize_item(match.group(2)) != target:
            continue
        start = match.end()
        level = len(match.group(1))
        end = len(text)
        for next_match in matches[index + 1 :]:
            if len(next_match.group(1)) <= level:
                end = next_match.start()
                break
        return text[start:end]
    return None


def parse_bullet_list_under_heading(text: str, heading: str) -> tuple[list[str], str | None]:
    body = find_section_body(text, heading)
    if body is None:
        return [], f"Missing heading {heading!r}."

    items: list[str] = []
    for line in body.splitlines():
        match = BULLET_RE.match(line)
        if not match:
            continue
        item = normalize_item(match.group(1))
        if item and item not in items:
            items.append(item)
    if not items:
        return [], f"Heading {heading!r} contains no Markdown bullet items."
    return items, None


def read_text(root: Path, relpath: str) -> tuple[str, str | None]:
    path = root / relpath
    try:
        return path.read_text(encoding="utf-8"), None
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace"), None
    except OSError as exc:
        return "", f"Could not read {relpath}: {exc}"


def check_binding(binding: Binding, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    source_text, source_error = read_text(root, binding.source_path)
    registry_text, registry_error = read_text(root, binding.registry_path)
    if source_error:
        findings.append(Finding(binding.name, "source_unreadable", source_error))
        return findings
    if registry_error:
        findings.append(Finding(binding.name, "registry_unreadable", registry_error))
        return findings

    source_items, source_parse_error = parse_bullet_list_under_heading(
        source_text, binding.source_heading
    )
    registry_items, registry_parse_error = parse_bullet_list_under_heading(
        registry_text, binding.registry_heading
    )
    if source_parse_error:
        findings.append(Finding(binding.name, "source_list_missing", source_parse_error))
    if registry_parse_error:
        findings.append(Finding(binding.name, "registry_list_missing", registry_parse_error))
    if source_parse_error or registry_parse_error:
        return findings

    missing = [item for item in source_items if item not in registry_items]
    if missing:
        findings.append(
            Finding(
                binding.name,
                "registry_missing_signal_use_categories",
                "Engagement registry Signal Use Classification is missing "
                + ", ".join(missing)
                + f" from Foundation Allowed Signal Uses. Binding: {binding.source_path} -> {binding.registry_path}.",
            )
        )
    return findings


def bindings_touched(relpaths: list[str | None]) -> list[Binding]:
    touched = {path for path in relpaths if path}
    selected: list[Binding] = []
    for binding in BINDINGS:
        if binding.source_path in touched or binding.registry_path in touched:
            selected.append(binding)
    return selected


def collect_findings(bindings: list[Binding], root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for binding in bindings:
        findings.extend(check_binding(binding, root))
    return findings


def report(findings: list[Finding], strict: bool, checked_count: int) -> int:
    if not findings:
        print(f"registry-list-sync: OK ({checked_count} binding(s) checked)")
        return 0
    for finding in findings:
        print(
            f"registry-list-sync: {finding.binding}: {finding.code}: {finding.message}",
            file=sys.stderr,
        )
    if not strict:
        print(
            f"registry-list-sync: {len(findings)} advisory finding(s); shape/list sync only, exit 0.",
            file=sys.stderr,
        )
    return 1 if strict else 0


def selftest() -> int:
    foundation = """# Foundation

### Allowed Signal Uses

Use these categories:

- demand evidence;
- resonance-direction evidence;
- actor-strategy evidence.
"""
    registry_ok = """# Registry

## Signal Use Classification

Every engagement signal should be classified by decision use:

- demand evidence;
- resonance-direction evidence;
- actor-strategy evidence;
- extra registry-only evidence.
"""
    registry_missing = """# Registry

## Signal Use Classification

- demand evidence;
- resonance-direction evidence.
"""
    no_heading = "# Registry\n\n- demand evidence;\n"

    cases = [
        (
            "parse source list",
            parse_bullet_list_under_heading(foundation, "Allowed Signal Uses")[0],
            ["demand evidence", "resonance-direction evidence", "actor-strategy evidence"],
        ),
        (
            "parse registry list",
            parse_bullet_list_under_heading(registry_ok, "Signal Use Classification")[0],
            [
                "demand evidence",
                "resonance-direction evidence",
                "actor-strategy evidence",
                "extra registry-only evidence",
            ],
        ),
        (
            "missing category",
            [
                item
                for item in parse_bullet_list_under_heading(foundation, "Allowed Signal Uses")[0]
                if item
                not in parse_bullet_list_under_heading(registry_missing, "Signal Use Classification")[0]
            ],
            ["actor-strategy evidence"],
        ),
        (
            "missing heading error",
            parse_bullet_list_under_heading(no_heading, "Signal Use Classification")[1],
            "Missing heading 'Signal Use Classification'.",
        ),
        (
            "changed source selects binding",
            bindings_touched([FOUNDATION]),
            [SIGNAL_USE_BINDING],
        ),
        (
            "unrelated change selects nothing",
            bindings_touched([".agents/hooks/check_registry_list_sync.py"]),
            [],
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
        description="Check explicitly registered Forseti vocabulary list-sync bindings."
    )
    parser.add_argument("paths", nargs="*", help="explicit file paths to check for binding relevance")
    parser.add_argument("--live", action="store_true", help="check all registered bindings")
    parser.add_argument("--staged", action="store_true", help="check staged paths if they touch a binding")
    parser.add_argument("--changed", action="store_true", help="check changed + staged + untracked paths if they touch a binding")
    parser.add_argument("--strict", action="store_true", help="exit 1 if any selected binding has a finding")
    parser.add_argument("--selftest", action="store_true", help="run pure-function cases")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    root = repo_root()
    selected: list[Binding] = []
    relpaths: list[str | None] = []
    if args.live:
        selected = list(BINDINGS)
    else:
        if args.staged:
            relpaths.extend(staged_paths(root))
        if args.changed:
            relpaths.extend(changed_paths(root))
        relpaths.extend(to_relposix(path, root) for path in args.paths)
        selected = bindings_touched(relpaths)

    if not selected:
        if args.paths or args.changed or args.staged:
            print("registry-list-sync: no registered binding files selected -- OK")
            return 0
        parser.print_usage(sys.stderr)
        return 2

    return report(collect_findings(selected, root), args.strict, len(selected))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))