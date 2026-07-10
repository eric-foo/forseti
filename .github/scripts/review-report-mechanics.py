#!/usr/bin/env python3
"""Assemble and verify review reports without making review judgments."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import ModuleType
from typing import Sequence


DIFF_TOKEN = b"{{REVIEW_MECHANICS_UNIFIED_DIFF}}"
REVIEW_OUTPUT_ROOT = Path("docs/review-outputs")


class MechanicsFailure(RuntimeError):
    """A fail-visible mechanical gate failure."""

    def __init__(self, gate: str, exit_code: int, message: str) -> None:
        super().__init__(message)
        self.gate = gate
        self.exit_code = exit_code


class ReceiptParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise MechanicsFailure("input_contract", 2, message)


@dataclass
class Receipt:
    mode: str
    status: str = "GATE PASS"
    paths: dict[str, object] = field(default_factory=dict)
    hashes: dict[str, object] = field(default_factory=dict)
    gates: list[dict[str, object]] = field(default_factory=list)

    def record(self, name: str, bucket: str, exit_code: int) -> None:
        self.gates.append(
            {"name": name, "bucket": bucket, "exit_code": int(exit_code)}
        )
        if bucket == "GATE FAIL":
            self.status = "GATE FAIL"

    def emit(self) -> None:
        print(
            json.dumps(
                {
                    "mode": self.mode,
                    "status": self.status,
                    "paths": self.paths,
                    "hashes": self.hashes,
                    "gates": self.gates,
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def resolve_worktree(raw: str) -> Path:
    try:
        root = Path(raw).resolve(strict=True)
    except OSError as exc:
        raise MechanicsFailure("input_contract", 2, f"worktree is unreadable: {exc}") from exc
    if not root.is_dir():
        raise MechanicsFailure("input_contract", 2, "worktree is not a directory")
    return root


def resolve_inside(
    root: Path, raw: str, label: str, *, must_exist: bool
) -> tuple[Path, str]:
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = root / candidate
    try:
        resolved = candidate.resolve(strict=must_exist)
    except OSError as exc:
        raise MechanicsFailure("path_containment", 2, f"{label} is unavailable: {exc}") from exc
    try:
        relative = resolved.relative_to(root).as_posix()
    except ValueError as exc:
        raise MechanicsFailure("path_containment", 2, f"{label} is outside the worktree") from exc
    return resolved, relative


def run_git(
    root: Path,
    args: Sequence[str],
    *,
    allowed: tuple[int, ...] = (0,),
    gate: str,
) -> subprocess.CompletedProcess[bytes]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except (FileNotFoundError, OSError) as exc:
        raise MechanicsFailure(gate, -1, f"git could not run: {exc}") from exc
    if result.returncode not in allowed:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise MechanicsFailure(
            gate,
            result.returncode,
            f"git {' '.join(args)} exited {result.returncode}: {detail}",
        )
    return result


def validate_base(root: Path, base: str) -> None:
    if not base or base.startswith("-") or "\x00" in base:
        raise MechanicsFailure("base_ref", 2, "base ref is malformed")
    run_git(root, ["rev-parse", "--verify", f"{base}^{{commit}}"], gate="base_ref")


def classify_patch_path(root: Path, relative: str) -> str:
    tracked = run_git(
        root,
        ["ls-files", "--error-unmatch", "--", relative],
        allowed=(0, 1),
        gate="patch_selection",
    )
    if tracked.returncode == 0:
        return "tracked"
    ignored = run_git(
        root,
        ["check-ignore", "--quiet", "--", relative],
        allowed=(0, 1),
        gate="patch_selection",
    )
    if ignored.returncode == 1:
        return "untracked"
    raise MechanicsFailure("patch_selection", 2, f"patch path is ignored: {relative}")


def generate_diff(
    root: Path, base: str, patch_paths: list[tuple[Path, str]]
) -> tuple[bytes, list[str], list[str]]:
    tracked: list[str] = []
    untracked: list[str] = []
    blocks: list[bytes] = []
    for _absolute, relative in patch_paths:
        kind = classify_patch_path(root, relative)
        if kind == "tracked":
            tracked.append(relative)
            result = run_git(
                root,
                [
                    "diff",
                    "--no-color",
                    "--no-ext-diff",
                    "--unified=0",
                    base,
                    "--",
                    relative,
                ],
                gate="diff_generation",
            )
        else:
            untracked.append(relative)
            result = run_git(
                root,
                [
                    "diff",
                    "--no-index",
                    "--no-color",
                    "--no-ext-diff",
                    "--unified=0",
                    "--",
                    "/dev/null",
                    relative,
                ],
                allowed=(0, 1),
                gate="diff_generation",
            )
        if result.stdout:
            blocks.append(result.stdout)
    aggregate = b"".join(blocks)
    if not aggregate:
        raise MechanicsFailure("nonempty_diff", 1, "selected paths produced an empty aggregate diff")
    return aggregate, tracked, untracked


def run_tracked_diff_check(root: Path, base: str, tracked: list[str]) -> int:
    if not tracked:
        return 0
    result = run_git(
        root,
        ["diff", "--check", base, "--", *tracked],
        gate="tracked_diff_check",
    )
    return result.returncode


def verify_diff_occurrence(report_bytes: bytes, expected_diff: bytes) -> bool:
    return bool(expected_diff) and report_bytes.count(expected_diff) == 1


def verify_assembled_bytes(readback: bytes, expected: bytes) -> bool:
    return readback == expected


def atomic_write(path: Path, data: bytes) -> None:
    descriptor = -1
    temporary: Path | None = None
    try:
        descriptor, raw_temporary = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
        )
        temporary = Path(raw_temporary)
        with os.fdopen(descriptor, "wb") as handle:
            descriptor = -1
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    except OSError as exc:
        raise MechanicsFailure("atomic_write", -1, f"atomic report write failed: {exc}") from exc
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if temporary is not None:
            try:
                temporary.unlink()
            except OSError:
                pass


def load_checker(path: Path, module_name: str) -> ModuleType:
    try:
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise RuntimeError("module spec has no loader")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as exc:
        sys.modules.pop(module_name, None)
        raise MechanicsFailure("checker_load", -1, f"could not load {path}: {exc}") from exc


def run_checkers(root: Path, report_relative: str, receipt: Receipt) -> None:
    hooks = root / ".agents" / "hooks"
    provenance_path = hooks / "check_review_output_provenance.py"
    summary_path = hooks / "check_review_summary.py"
    for checker in (provenance_path, summary_path):
        if not checker.is_file():
            raise MechanicsFailure("checker_load", -1, f"checker is missing: {checker}")
    receipt.paths["checkers"] = [
        provenance_path.relative_to(root).as_posix(),
        summary_path.relative_to(root).as_posix(),
    ]
    receipt.hashes["checkers"] = {
        provenance_path.relative_to(root).as_posix(): sha256_bytes(provenance_path.read_bytes()),
        summary_path.relative_to(root).as_posix(): sha256_bytes(summary_path.read_bytes()),
    }

    provenance = load_checker(provenance_path, "review_report_mechanics_provenance")
    try:
        provenance_items = provenance.collect_findings([report_relative], root)
        provenance_exit = int(provenance.report(provenance_items, True))
    except Exception as exc:
        raise MechanicsFailure("provenance_shape", -1, f"provenance checker failed: {exc}") from exc
    receipt.record(
        "provenance_shape",
        "GATE PASS" if provenance_exit == 0 else "GATE FAIL",
        provenance_exit,
    )

    summary = load_checker(summary_path, "review_report_mechanics_summary")
    try:
        summary_items, enum_drift, _templates = summary.scan_files(root, [report_relative])
    except Exception as exc:
        raise MechanicsFailure("summary_shape", -1, f"summary checker failed: {exc}") from exc
    summary_exit = 1 if summary_items else 0
    if summary_items:
        for item in summary_items:
            print(
                f"review-summary-shape: {item.source}:{item.lineno}: {item.code}",
                file=sys.stderr,
            )
    receipt.record(
        "summary_shape",
        "GATE PASS" if summary_exit == 0 else "GATE FAIL",
        summary_exit,
    )
    if enum_drift:
        receipt.record("summary_enum_drift", "INFO", 0)


def prepare_inputs(args: argparse.Namespace, receipt: Receipt) -> tuple[
    Path, Path | None, Path, str, list[tuple[Path, str]]
]:
    root = resolve_worktree(args.worktree)
    receipt.paths["worktree"] = str(root)
    draft: Path | None = None
    if args.mode == "assemble":
        draft, draft_relative = resolve_inside(root, args.draft, "draft", must_exist=True)
        if not draft.is_file():
            raise MechanicsFailure("input_contract", 2, "draft is not a file")
        receipt.paths["draft"] = draft_relative

    report, report_relative = resolve_inside(root, args.report, "report", must_exist=False)
    review_root = (root / REVIEW_OUTPUT_ROOT).resolve(strict=True)
    try:
        report.relative_to(review_root)
    except ValueError as exc:
        raise MechanicsFailure("report_destination", 2, "report must be under docs/review-outputs") from exc
    if report == review_root or report.suffix.lower() != ".md":
        raise MechanicsFailure("report_destination", 2, "report must be a Markdown file below docs/review-outputs")
    if not report.parent.is_dir():
        raise MechanicsFailure("report_destination", 2, "report parent directory does not exist")
    receipt.paths["report"] = report_relative

    patch_paths: list[tuple[Path, str]] = []
    seen: set[str] = set()
    for raw in args.patch:
        absolute, relative = resolve_inside(root, raw, "patch path", must_exist=True)
        if not absolute.is_file():
            raise MechanicsFailure("patch_selection", 2, f"patch path is not a file: {relative}")
        if relative in seen:
            raise MechanicsFailure("patch_selection", 2, f"duplicate patch path: {relative}")
        seen.add(relative)
        patch_paths.append((absolute, relative))
    receipt.paths["patches"] = [relative for _absolute, relative in patch_paths]
    receipt.hashes["patches"] = {
        relative: sha256_bytes(absolute.read_bytes()) for absolute, relative in patch_paths
    }
    receipt.record("input_contract", "GATE PASS", 0)
    return root, draft, report, report_relative, patch_paths


def execute(args: argparse.Namespace, receipt: Receipt) -> int:
    root, draft, report, report_relative, patch_paths = prepare_inputs(args, receipt)
    validate_base(root, args.base)
    receipt.record("base_ref", "GATE PASS", 0)
    generated_diff, tracked, _untracked = generate_diff(root, args.base, patch_paths)
    receipt.hashes["generated_diff_sha256"] = sha256_bytes(generated_diff)
    receipt.record("diff_generation", "GATE PASS", 0)
    receipt.record("nonempty_diff", "GATE PASS", 0)
    run_tracked_diff_check(root, args.base, tracked)
    receipt.record(
        "tracked_diff_check" if tracked else "tracked_diff_check_not_applicable",
        "GATE PASS" if tracked else "INFO",
        0,
    )

    expected_report: bytes | None = None
    if args.mode == "assemble":
        assert draft is not None
        draft_bytes = draft.read_bytes()
        receipt.hashes["draft_sha256"] = sha256_bytes(draft_bytes)
        if draft_bytes.count(DIFF_TOKEN) != 1:
            raise MechanicsFailure("unique_diff_token", 2, "draft must contain exactly one diff token")
        receipt.record("unique_diff_token", "GATE PASS", 0)
        if report.exists() and not args.replace:
            raise MechanicsFailure("replace_guard", 2, "report exists; pass --replace to overwrite it")
        receipt.record("replace_guard", "GATE PASS", 0)
        expected_report = draft_bytes.replace(DIFF_TOKEN, generated_diff, 1)
        atomic_write(report, expected_report)
        receipt.record("atomic_write", "GATE PASS", 0)
    elif not report.is_file():
        raise MechanicsFailure("input_contract", 2, "report does not exist for verify mode")

    try:
        report_bytes = report.read_bytes()
    except OSError as exc:
        raise MechanicsFailure("readback", -1, f"report readback failed: {exc}") from exc
    receipt.hashes["report_sha256"] = sha256_bytes(report_bytes)
    if expected_report is not None and not verify_assembled_bytes(report_bytes, expected_report):
        raise MechanicsFailure("readback_exact", 1, "report readback does not match assembled bytes")
    receipt.record("readback_exact", "GATE PASS", 0)
    if not verify_diff_occurrence(report_bytes, generated_diff):
        raise MechanicsFailure("generated_diff_once", 1, "generated diff does not occur exactly once")
    receipt.record("generated_diff_once", "GATE PASS", 0)

    run_checkers(root, report_relative, receipt)
    return 0 if receipt.status == "GATE PASS" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = ReceiptParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="mode", required=True, parser_class=ReceiptParser)
    for mode in ("assemble", "verify"):
        subparser = subparsers.add_parser(mode)
        subparser.add_argument("--worktree", required=True)
        subparser.add_argument("--base", default="HEAD")
        subparser.add_argument("--report", required=True)
        subparser.add_argument("--patch", action="append", required=True)
        if mode == "assemble":
            subparser.add_argument("--draft", required=True)
            subparser.add_argument("--replace", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    raw_args = list(argv if argv is not None else sys.argv[1:])
    mode = raw_args[0] if raw_args and raw_args[0] in {"assemble", "verify"} else "unselected"
    receipt = Receipt(mode=mode)
    try:
        args = build_parser().parse_args(raw_args)
        return execute(args, receipt)
    except MechanicsFailure as exc:
        receipt.record(exc.gate, "GATE FAIL", exc.exit_code)
        print(f"review-report-mechanics: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        receipt.record("internal_error", "GATE FAIL", -1)
        print(f"review-report-mechanics: internal error: {exc}", file=sys.stderr)
        return 1
    finally:
        receipt.emit()


if __name__ == "__main__":
    sys.exit(main())
