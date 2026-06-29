#!/usr/bin/env python3
"""Enforce the Data Lake silver-lane write contract (the no-blur binding).

Reads the lane registry (``orca-harness/data_lake/lane_registry.py``) and scans
producer source for raw lake writes (``append_record`` / ``append_record_set``):

- **G1 (declared).** A ``silver``-named lane written by a producer must be
  declared in the registry. An undeclared silver lane fails -- a new silver lane
  has to be registered with a role, which is also how the next agent discovers
  the contract.
- **G2 (front-door).** A raw write to a ``silver_envelope`` lane must go through
  the validating front-door ``append_silver_record`` (``data_lake/silver_record``).
  A direct ``append_record`` to an envelope lane fails, unless the lane is listed
  in the registry's ``FRONT_DOOR_PENDING`` baseline (a named, justified migration
  target -- not a silent exception).

It does NOT validate record CONTENT (that is the front-door's job at write time);
it binds the WRITE PATH so the content validator cannot be silently bypassed.
Lane arguments it cannot statically resolve (a computed/parameterized lane) are
skipped and reported as a coverage note, never a silent pass.

Usage:
  python .agents/hooks/check_silver_lane_registry.py [--strict] [--selftest] [PATH ...]
"""
from __future__ import annotations

import argparse
import ast
import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

WRITE_METHODS = {"append_record", "append_record_set"}
LANE_KEYWORDS = {"lane", "completion_lane"}


@dataclass(frozen=True)
class Finding:
    code: str
    message: str


@dataclass(frozen=True)
class Unresolved:
    relposix: str
    lineno: int
    excerpt: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_registry(root: Path):
    path = root / "orca-harness" / "data_lake" / "lane_registry.py"
    spec = importlib.util.spec_from_file_location("orca_lane_registry", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load lane registry from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# --- static constant resolution -------------------------------------------

def _string_constants(tree: ast.Module) -> dict[str, str]:
    consts: dict[str, str] = {}
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    consts[target.id] = node.value.value
    return consts


def _alias_assignments(tree: ast.Module) -> dict[str, str]:
    out: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Name):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    out.setdefault(target.id, node.value.id)
    return out


def _build_global_consts(parsed: dict[Path, ast.Module]) -> dict[str, str]:
    """Repo-wide ``name -> str value`` from module-level literal assignments
    (resolving simple ``NAME = OTHER`` aliases). A name with conflicting literal
    values across files is dropped -- treated as unresolvable, never guessed."""
    literal: dict[str, set[str]] = {}
    aliases: dict[str, str] = {}
    for tree in parsed.values():
        for name, value in _string_constants(tree).items():
            literal.setdefault(name, set()).add(value)
        for name, src in _alias_assignments(tree).items():
            aliases.setdefault(name, src)
    consts = {name: next(iter(vals)) for name, vals in literal.items() if len(vals) == 1}
    for _ in range(3):  # resolve short alias chains
        for name, src in aliases.items():
            if name not in consts and src in consts:
                consts[name] = consts[src]
    return consts


def _resolve(node: ast.AST, consts: dict[str, str]) -> tuple[str | None, str]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value, repr(node.value)
    if isinstance(node, ast.Name):
        return consts.get(node.id), node.id
    if isinstance(node, ast.Attribute):
        return consts.get(node.attr), node.attr
    return None, type(node).__name__


def _lane_args(call: ast.Call, consts: dict[str, str]) -> list[tuple[str | None, str, int]]:
    out: list[tuple[str | None, str, int]] = []
    for kw in call.keywords:
        if kw.arg in LANE_KEYWORDS:
            value, excerpt = _resolve(kw.value, consts)
            out.append((value, excerpt, call.lineno))
        elif kw.arg == "members" and isinstance(kw.value, ast.Dict):
            for key in kw.value.keys:
                if key is None:
                    continue
                value, excerpt = _resolve(key, consts)
                out.append((value, excerpt, call.lineno))
    return out


def _iter_write_calls(tree: ast.Module) -> Iterable[ast.Call]:
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in WRITE_METHODS
        ):
            yield node


def _scan_tree(
    relposix: str, tree: ast.Module, consts: dict[str, str], registry, is_front_door: bool
) -> tuple[list[Finding], list[Unresolved]]:
    findings: list[Finding] = []
    unresolved: list[Unresolved] = []
    for call in _iter_write_calls(tree):
        for lane, excerpt, lineno in _lane_args(call, consts):
            if lane is None:
                # The front-door legitimately takes a lane parameter; only note an
                # unresolved lane elsewhere, where it is a real static-coverage gap.
                if not is_front_door:
                    unresolved.append(Unresolved(relposix, lineno, excerpt))
                continue
            if not registry.is_silver_named(lane):
                continue
            role = registry.role_of(lane)
            if role is None:
                findings.append(
                    Finding(
                        "undeclared_silver_lane",
                        f"{relposix}:{lineno} writes silver lane {lane!r}, which is not declared "
                        "in orca-harness/data_lake/lane_registry.py. Add it with a role.",
                    )
                )
                continue
            if role == registry.LaneRole.SILVER_ENVELOPE and not is_front_door:
                if lane in registry.FRONT_DOOR_PENDING:
                    continue
                findings.append(
                    Finding(
                        "envelope_lane_bypass",
                        f"{relposix}:{lineno} writes silver_envelope lane {lane!r} through a raw "
                        f"lake writer. Route it through {registry.SILVER_ENVELOPE_FRONT_DOOR_FUNC}() "
                        "(orca-harness/data_lake/silver_record.py). If migration is genuinely "
                        "pending, add the lane to FRONT_DOOR_PENDING with a reason.",
                    )
                )
    return findings, unresolved


# --- file discovery + drivers ---------------------------------------------

def _producer_files(root: Path) -> list[Path]:
    harness = root / "orca-harness"
    out: list[Path] = []
    for path in sorted(harness.rglob("*.py")):
        parts = set(path.parts)
        if "tests" in parts or "__pycache__" in parts:
            continue
        out.append(path)
    return out


def _parse(paths: Iterable[Path]) -> dict[Path, ast.Module]:
    parsed: dict[Path, ast.Module] = {}
    for path in paths:
        try:
            parsed[path] = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (SyntaxError, UnicodeDecodeError, OSError):
            continue
    return parsed


def scan(root: Path, paths: list[Path], registry) -> tuple[list[Finding], list[Unresolved]]:
    parsed = _parse(paths)
    consts = _build_global_consts(parsed)
    findings: list[Finding] = []
    unresolved: list[Unresolved] = []
    front_door = registry.SILVER_ENVELOPE_FRONT_DOOR_MODULE
    for path, tree in parsed.items():
        try:
            relposix = path.relative_to(root).as_posix()
        except ValueError:
            relposix = path.as_posix()
        f, u = _scan_tree(relposix, tree, consts, registry, is_front_door=(relposix == front_door))
        findings.extend(f)
        unresolved.extend(u)
    return findings, unresolved


def _print_report(findings: list[Finding], unresolved: list[Unresolved]) -> None:
    for finding in findings:
        print(f"FAIL {finding.code}: {finding.message}")
    if unresolved:
        # No silent caps: report what was skipped so coverage is visible.
        print(f"note: {len(unresolved)} lane argument(s) not statically resolved (skipped):")
        for item in unresolved[:8]:
            print(f"  - {item.relposix}:{item.lineno} ({item.excerpt})")
        if len(unresolved) > 8:
            print(f"  - ... and {len(unresolved) - 8} more")
    if not findings:
        print("check_silver_lane_registry: OK (no silver-lane write violations)")


def selftest(root: Path | None = None) -> int:
    root = root or repo_root()
    registry = _load_registry(root)
    fixture_dir = root / "orca-harness" / "tests" / "fixtures" / "silver_lane_guard"
    fixtures = sorted(fixture_dir.glob("*.py"))
    if not fixtures:
        print(f"SELFTEST FAILED: no fixtures at {fixture_dir}")
        return 1
    ok = True
    for path in fixtures:
        first_line = path.read_text(encoding="utf-8").splitlines()[0]
        expected = "fail" if "fixture_expected: fail" in first_line else "pass"
        findings, _ = scan(root, [path], registry)
        actual = "fail" if findings else "pass"
        if actual == expected:
            print(f"PASS {path.name} ({expected})")
        else:
            ok = False
            codes = ", ".join(sorted({f.code for f in findings})) or "<none>"
            print(f"FAIL {path.name}: expected {expected}, got {actual} ({codes})")
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Enforce the Data Lake silver-lane write contract.")
    parser.add_argument("paths", nargs="*", help="explicit files to scan (default: all producers)")
    parser.add_argument("--selftest", action="store_true", help="run the fixture selftest")
    parser.add_argument("--strict", action="store_true", help="accepted for CI readability; findings already exit 1")
    args = parser.parse_args(argv)

    root = repo_root()
    if args.selftest:
        return selftest(root)

    registry = _load_registry(root)
    paths = [Path(p) for p in args.paths] if args.paths else _producer_files(root)
    findings, unresolved = scan(root, paths, registry)
    _print_report(findings, unresolved)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
