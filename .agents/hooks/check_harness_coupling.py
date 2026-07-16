#!/usr/bin/env python3
"""Run fast harness coupling contracts when the outgoing diff can affect them.

This is a thin, diff-scoped adapter around two existing pytest contract files.
It adds no test rule and makes no full-suite or readiness claim.

Rule authority: .agents/workflow-overlay/validation-gates.md
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _hooklib import repo_root  # noqa: E402  (sys.path pin must precede the import)


INVENTORY_PATH = "forseti-harness/data_lake/lake_touchpoint_inventory_v0.json"
CONTRACT_TESTS = (
    "tests/contract/test_data_lake_inventory_gate.py",
    "tests/contract/test_policy_module_version_pins.py",
)
TIMEOUT_SECONDS = 120


class GateInfrastructureError(RuntimeError):
    """The gate could not determine or execute its required scope."""


def resolve_base_ref(explicit_base: str | None = None) -> str:
    """Resolve the diff base using the repository-wide CI precedence."""
    event_base = os.environ.get("FORSETI_DIFF_BASE", "").strip()
    if event_base:
        return event_base
    github_base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if github_base:
        return f"origin/{github_base}"
    if explicit_base:
        return explicit_base
    return "origin/main"


def changed_paths_command(base_ref: str) -> list[str]:
    return [
        "git",
        "diff",
        "--name-only",
        "--diff-filter=ACMRTD",
        f"{base_ref}...HEAD",
    ]


def changed_paths(root: Path, base_ref: str) -> tuple[str, ...]:
    command = changed_paths_command(base_ref)
    try:
        result = subprocess.run(
            command,
            cwd=root,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired) as exc:
        raise GateInfrastructureError(f"could not resolve changed paths: {exc}") from exc
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "git diff failed").strip()
        raise GateInfrastructureError(
            f"could not resolve diff {base_ref}...HEAD (exit {result.returncode}): {detail}"
        )
    return tuple(
        line.strip().replace("\\", "/")
        for line in result.stdout.splitlines()
        if line.strip()
    )


def path_triggers_gate(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return normalized == INVENTORY_PATH or (
        normalized.startswith("forseti-harness/") and normalized.endswith(".py")
    )


def triggering_paths(paths: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(path for path in paths if path_triggers_gate(path))


def contract_command() -> list[str]:
    return [
        sys.executable,
        "-m",
        "pytest",
        "-p",
        "no:cacheprovider",
        "-q",
        *CONTRACT_TESTS,
    ]


def run_contracts(root: Path, runner=subprocess.run) -> int:
    harness_root = root / "forseti-harness"
    missing = [test for test in CONTRACT_TESTS if not (harness_root / test).is_file()]
    if missing:
        print(
            "GATE FAIL harness coupling contracts: missing test file(s): "
            + ", ".join(missing),
            file=sys.stderr,
        )
        return 2
    try:
        result = runner(
            contract_command(),
            cwd=harness_root,
            timeout=TIMEOUT_SECONDS,
        )
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired) as exc:
        print(f"GATE FAIL harness coupling contracts: could not run: {exc}", file=sys.stderr)
        return 2
    return result.returncode


def selftest() -> int:
    cases = (
        ("harness Python", "forseti-harness/src/forseti_harness/example.py", True),
        ("contract Python", "forseti-harness/tests/contract/test_example.py", True),
        ("generated inventory", INVENTORY_PATH, True),
        ("unrelated JSON", "forseti-harness/data_lake/other.json", False),
        ("documentation", "docs/decisions/example.md", False),
    )
    ok = True
    for name, path, expected in cases:
        observed = path_triggers_gate(path)
        passed = observed == expected
        ok = ok and passed
        print(
            f"{'PASS' if passed else 'FAIL'} {name} "
            f"expected_trigger={expected} observed_trigger={observed}"
        )

    expected_tail = ["-q", *CONTRACT_TESTS]
    command_ok = contract_command()[-len(expected_tail) :] == expected_tail
    ok = ok and command_ok
    print(f"{'PASS' if command_ok else 'FAIL'} existing contract test command")
    deletion_ok = "--diff-filter=ACMRTD" in changed_paths_command("base")
    ok = ok and deletion_ok
    print(f"{'PASS' if deletion_ok else 'FAIL'} deleted paths remain in gate scope")
    print("SELFTEST", "OK" if ok else "FAILED")

    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="explicit diff base (after CI/GitHub environment bases)")
    parser.add_argument("--strict", action="store_true", help="CI/pre-push gate mode")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    root = repo_root()
    base_ref = resolve_base_ref(args.base)
    try:
        paths = changed_paths(root, base_ref)
    except GateInfrastructureError as exc:
        print(f"GATE FAIL harness coupling contracts: {exc}", file=sys.stderr)
        return 2

    triggers = triggering_paths(paths)
    if not triggers:
        print(
            f"SKIP harness coupling contracts: no harness Python or generated inventory "
            f"change in {base_ref}...HEAD"
        )
        return 0

    print(
        "RUN harness coupling contracts: "
        f"{len(triggers)} triggering path(s) in {base_ref}...HEAD"
    )
    result = run_contracts(root)
    if result == 0:
        print("GATE PASS harness coupling contracts (coupling preflight only; not full validation)")
    else:
        print(
            f"GATE FAIL harness coupling contracts: pytest exited {result}",
            file=sys.stderr,
        )
    return result


if __name__ == "__main__":
    sys.exit(main())
