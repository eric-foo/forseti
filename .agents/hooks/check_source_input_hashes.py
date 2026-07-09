#!/usr/bin/env python3
"""Source-input hash freshness gate (EP-37).

Validates repo-local JSON ``source_inputs`` entries that record both a
``source_pointer`` and ``sha256``. In strict mode the gate is diff-scoped and
forward-only: it checks a record when either the JSON artifact itself changed
or the referenced source file changed in ``base...HEAD``.

Rule authority:
  .agents/workflow-overlay/validation-gates.md

Placement boundary:
  This is provenance shape/freshness only. A green run never proves the
  dependent artifact is semantically current, complete, validated, or ready.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PureWindowsPath
from typing import Any, NamedTuple


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            pass


_configure_stdio()

_URL_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")


class SourceInput(NamedTuple):
    artifact: str
    json_path: str
    source_pointer: str
    expected_sha256: str


class Finding(NamedTuple):
    artifact: str
    json_path: str
    source_pointer: str
    problem: str
    expected_sha256: str | None = None
    actual_sha256: str | None = None


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def normalize_relpath(value: str) -> str:
    normalized = value.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def is_repo_local_pointer(pointer: str) -> bool:
    if not pointer or _URL_RE.search(pointer):
        return False
    if pointer.startswith("#"):
        return False
    if Path(pointer).is_absolute():
        return False
    if PureWindowsPath(pointer).drive:
        return False
    if ".." in Path(pointer).parts:
        return False
    return True


def sha256_normalized(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def source_inputs_from_document(document: Any, artifact: str) -> list[SourceInput]:
    records: list[SourceInput] = []

    def walk(value: Any, pointer: str) -> None:
        if isinstance(value, dict):
            source_inputs = value.get("source_inputs")
            if isinstance(source_inputs, list):
                for index, item in enumerate(source_inputs):
                    if not isinstance(item, dict):
                        continue
                    source_pointer = item.get("source_pointer")
                    expected_sha = item.get("sha256")
                    if isinstance(source_pointer, str) and isinstance(expected_sha, str):
                        records.append(
                            SourceInput(
                                artifact=artifact,
                                json_path=f"{pointer}/source_inputs/{index}",
                                source_pointer=normalize_relpath(source_pointer),
                                expected_sha256=expected_sha,
                            )
                        )
            for key, item in value.items():
                walk(item, f"{pointer}/{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                walk(item, f"{pointer}/{index}")

    walk(document, "$")
    return records


def findings_for_records(root: Path, records: list[SourceInput]) -> list[Finding]:
    findings: list[Finding] = []
    for record in records:
        if not is_repo_local_pointer(record.source_pointer):
            continue
        source_path = root / Path(record.source_pointer)
        if not source_path.is_file():
            findings.append(
                Finding(
                    artifact=record.artifact,
                    json_path=record.json_path,
                    source_pointer=record.source_pointer,
                    problem="source_pointer_missing",
                    expected_sha256=record.expected_sha256,
                )
            )
            continue
        actual = sha256_normalized(source_path)
        if actual != record.expected_sha256:
            findings.append(
                Finding(
                    artifact=record.artifact,
                    json_path=record.json_path,
                    source_pointer=record.source_pointer,
                    problem="source_input_hash_mismatch",
                    expected_sha256=record.expected_sha256,
                    actual_sha256=actual,
                )
            )
    return findings


def parse_name_status(lines: list[str]) -> set[str]:
    changed: set[str] = set()
    for line in lines:
        parts = [part.strip() for part in line.split("\t")]
        if len(parts) < 2:
            continue
        status = parts[0]
        if status.startswith(("R", "C")) and len(parts) >= 3:
            changed.add(normalize_relpath(parts[1]))
            changed.add(normalize_relpath(parts[2]))
        else:
            changed.add(normalize_relpath(parts[1]))
    return changed


def relevant_records(records: list[SourceInput], changed_paths: set[str]) -> list[SourceInput]:
    return [
        record
        for record in records
        if normalize_relpath(record.artifact) in changed_paths
        or normalize_relpath(record.source_pointer) in changed_paths
    ]


def _git(root: Path, args: list[str], timeout: int = 20) -> tuple[int, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout
    except (FileNotFoundError, OSError, subprocess.TimeoutExpired):
        return -1, ""


def resolve_base_ref(cli_base: str | None) -> str:
    gh_base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if gh_base:
        return f"origin/{gh_base}"
    if cli_base:
        return cli_base
    return "origin/main"


def changed_paths_for_base(root: Path, base_ref: str) -> set[str] | None:
    if _git(root, ["rev-parse", "--verify", "--quiet", "HEAD"])[0] != 0:
        return None
    if _git(root, ["rev-parse", "--verify", "--quiet", base_ref])[0] != 0:
        return None
    code, output = _git(root, ["diff", "--name-status", f"{base_ref}...HEAD"])
    if code != 0:
        return None
    return parse_name_status(output.splitlines())


def tracked_json_files(root: Path) -> list[str] | None:
    code, output = _git(root, ["ls-files", "*.json"])
    if code != 0:
        return None
    return [normalize_relpath(line) for line in output.splitlines() if line.strip()]


def collect_records(root: Path, rel_paths: list[str]) -> tuple[list[SourceInput], list[str]]:
    records: list[SourceInput] = []
    problems: list[str] = []
    for rel in rel_paths:
        path = root / Path(rel)
        try:
            document = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as exc:
            problems.append(f"{rel}: cannot read JSON ({exc})")
            continue
        records.extend(source_inputs_from_document(document, rel))
    return records, problems


def format_findings(findings: list[Finding]) -> str:
    lines: list[str] = []
    for finding in findings:
        lines.append(
            f"{finding.artifact} {finding.json_path}: {finding.problem}: "
            f"{finding.source_pointer}"
        )
        if finding.expected_sha256 is not None:
            lines.append(f"  expected: {finding.expected_sha256}")
        if finding.actual_sha256 is not None:
            lines.append(f"  actual:   {finding.actual_sha256}")
    return "\n".join(lines)


def run_scan(root: Path, *, base_ref: str | None, strict: bool, audit: bool) -> int:
    json_files = tracked_json_files(root)
    if json_files is None:
        print("check_source_input_hashes: WARNING: git ls-files unavailable; fail-open")
        return 0
    records, read_problems = collect_records(root, json_files)
    if read_problems and (strict or audit):
        print("check_source_input_hashes: JSON read problem(s):")
        for problem in read_problems:
            print(f"  {problem}")
        return 1 if strict else 0

    if audit:
        scoped = records
        base_note = "audit"
    else:
        assert base_ref is not None
        changed = changed_paths_for_base(root, base_ref)
        if changed is None:
            print(
                "check_source_input_hashes --strict: WARNING: diff scope "
                f"unavailable for {base_ref}; fail-open"
            )
            return 0
        scoped = relevant_records(records, changed)
        base_note = f"base: {base_ref}"

    findings = findings_for_records(root, scoped)
    if findings:
        mode = "--strict" if strict else "--audit"
        print(f"check_source_input_hashes {mode}: {len(findings)} finding(s) ({base_note}):")
        print(format_findings(findings))
        return 1 if strict else 0
    print(
        f"check_source_input_hashes: OK ({base_note}; "
        f"checked {len(scoped)} of {len(records)} source-input hash record(s))"
    )
    return 0


def selftest() -> int:
    ok = True

    def check(label: str, got: object, expected: object) -> None:
        nonlocal ok
        passed = got == expected
        if not passed:
            ok = False
        print(f"{'PASS' if passed else 'FAIL'}  {label}  expect={expected!r} got={got!r}")

    document = {
        "wrapper": {
            "source_inputs": [
                {"source_pointer": "docs/a.json", "sha256": "a" * 64, "role": "input"},
                {"source_pointer": "https://example.com/x", "sha256": "b" * 64},
                {"source_pointer": "F:/outside/file.json", "sha256": "c" * 64},
            ],
        },
        "legacy": {"source_inputs": {"path": "docs/a.json", "sha256": "ignored"}},
    }
    records = source_inputs_from_document(document, "artifact.json")
    check("list-style records only", len(records), 3)
    check("dict source_inputs ignored", any(r.json_path.endswith("/legacy") for r in records), False)
    check("repo-local pointer", is_repo_local_pointer("docs/a.json"), True)
    check("url pointer skipped", is_repo_local_pointer("https://example.com/x"), False)
    check("windows absolute skipped", is_repo_local_pointer("F:/outside/file.json"), False)
    check("parent traversal skipped", is_repo_local_pointer("../outside.json"), False)
    check(
        "name-status includes rename source and destination",
        parse_name_status(["M\tdocs/a.json", "D\tdocs/b.json", "R100\tdocs/c.json\tdocs/d.json"]),
        {"docs/a.json", "docs/b.json", "docs/c.json", "docs/d.json"},
    )
    check(
        "relevant when artifact changes",
        [r.source_pointer for r in relevant_records(records, {"artifact.json"})],
        ["docs/a.json", "https://example.com/x", "F:/outside/file.json"],
    )
    check(
        "relevant when source changes",
        [r.source_pointer for r in relevant_records(records, {"docs/a.json"})],
        ["docs/a.json"],
    )

    root = repo_root()
    source_pointer = ".agents/hooks/check_source_input_hashes.py"
    source = root / source_pointer
    good = SourceInput("artifact.json", "$/source_inputs/0", source_pointer, sha256_normalized(source))
    bad = good._replace(expected_sha256="0" * 64)
    missing = good._replace(source_pointer="docs/missing.json")
    check("good hash has no findings", findings_for_records(root, [good]), [])
    check("bad hash mismatch", findings_for_records(root, [bad])[0].problem, "source_input_hash_mismatch")
    check("missing source", findings_for_records(root, [missing])[0].problem, "source_pointer_missing")

    saved = os.environ.pop("GITHUB_BASE_REF", None)
    try:
        check("default base", resolve_base_ref(None), "origin/main")
        check("cli base", resolve_base_ref("main"), "main")
        os.environ["GITHUB_BASE_REF"] = "develop"
        check("env base wins", resolve_base_ref("main"), "origin/develop")
    finally:
        if saved is not None:
            os.environ["GITHUB_BASE_REF"] = saved
        else:
            os.environ.pop("GITHUB_BASE_REF", None)

    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def _arg_value(argv: list[str], flag: str) -> str | None:
    if flag in argv:
        index = argv.index(flag)
        if index + 1 < len(argv):
            return argv[index + 1]
    return None


def main(argv: list[str]) -> int:
    if "--force-internal-error" in argv:
        raise RuntimeError("forced internal error (probe)")
    if "--selftest" in argv:
        return selftest()
    root = repo_root()
    if "--strict" in argv:
        return run_scan(
            root,
            base_ref=resolve_base_ref(_arg_value(argv, "--base")),
            strict=True,
            audit=False,
        )
    if "--check" in argv:
        return run_scan(
            root,
            base_ref=resolve_base_ref(_arg_value(argv, "--base")),
            strict=False,
            audit=False,
        )
    if "--audit" in argv:
        return run_scan(root, base_ref=None, strict=False, audit=True)
    print("Usage: check_source_input_hashes.py --strict [--base <ref>] | --check [--base <ref>] | --audit | --selftest")
    print("  --strict    CI/pre-push gate: fail on changed source-input hash drift")
    print("  --check     same diff-scoped scan, always exit 0 except internal errors")
    print("  --audit     whole-repo source-input hash scan, advisory")
    print("  --selftest  pure-function self-check")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        sys.stderr.write(f"check_source_input_hashes: internal error: {exc}\n")
        gating = "--strict" in sys.argv[1:] or "--selftest" in sys.argv[1:]
        sys.exit(1 if gating else 0)
