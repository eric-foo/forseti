#!/usr/bin/env python3
"""Validate and count Batch 0 review-economics completion receipts."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

DEFAULT_RECEIPTS = Path("docs/workflows/process_improvement_batch0/review_receipts")
DEFAULT_THRESHOLD = 10
CLOSURE_STATES = {"closed", "partially_closed", "open", "deferred", "no_action"}


def _nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_pointer(repo_root: Path, pointer: object) -> bool:
    if not _nonempty_string(pointer):
        return False
    path = Path(str(pointer))
    return not path.is_absolute() and (repo_root / path).is_file()


def validate_receipt(path: Path, repo_root: Path) -> tuple[dict | None, list[str]]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"{path}: unreadable JSON: {exc}"]
    if not isinstance(data, dict):
        return None, [f"{path}: receipt root must be an object"]

    for field in (
        "review_id", "review_report_path", "status", "reviewed_by", "authored_by",
        "ca_adjudication_status", "ca_adjudicator", "decision_changed",
        "closure_state", "completed_at",
    ):
        if not _nonempty_string(data.get(field)):
            errors.append(f"{path}: {field} must be a non-empty string")

    if data.get("schema_version") != 1:
        errors.append(f"{path}: schema_version must equal 1")
    if data.get("status") != "completed":
        errors.append(f"{path}: status must equal completed")
    if data.get("material_review") is not True:
        errors.append(f"{path}: material_review must be true")
    if data.get("ca_adjudication_status") != "completed":
        errors.append(f"{path}: ca_adjudication_status must equal completed")
    if data.get("decision_changed") not in {"yes", "no"}:
        errors.append(f"{path}: decision_changed must be yes or no")
    if data.get("closure_state") not in CLOSURE_STATES:
        errors.append(f"{path}: closure_state is not recognized")

    findings = data.get("accepted_net_new_material_findings")
    if isinstance(findings, bool) or not isinstance(findings, int) or findings < 0:
        errors.append(f"{path}: accepted_net_new_material_findings must be an integer >= 0")
    report_lines = data.get("report_lines")
    if isinstance(report_lines, bool) or not isinstance(report_lines, int) or report_lines < 1:
        errors.append(f"{path}: report_lines must be an integer >= 1")
    turn_count = data.get("turn_count")
    if turn_count != "unknown" and (
        isinstance(turn_count, bool) or not isinstance(turn_count, int) or turn_count < 1
    ):
        errors.append(f"{path}: turn_count must be unknown or an integer >= 1")

    try:
        date.fromisoformat(str(data.get("completed_at", "")))
    except ValueError:
        errors.append(f"{path}: completed_at must be an ISO date")

    report_path = data.get("review_report_path")
    if _nonempty_string(report_path) and not _validate_pointer(repo_root, report_path):
        errors.append(f"{path}: review_report_path must point to an existing repository file")
    pointers = data.get("evidence_pointers")
    if not isinstance(pointers, list) or not pointers:
        errors.append(f"{path}: evidence_pointers must be a non-empty list")
    else:
        for pointer in pointers:
            if not _validate_pointer(repo_root, pointer):
                errors.append(f"{path}: invalid or missing evidence pointer: {pointer!r}")
    return data, errors


def inspect_receipts(
    receipts_dir: Path, repo_root: Path, threshold: int, pattern: str = "*.json"
) -> dict:
    errors: list[str] = []
    receipts: list[dict] = []
    seen_ids: dict[str, Path] = {}
    seen_paths: dict[str, Path] = {}
    if not receipts_dir.is_dir():
        errors.append(f"receipt directory does not exist: {receipts_dir}")
    else:
        for path in sorted(receipts_dir.glob(pattern)):
            if path.name.startswith("_"):
                continue
            data, receipt_errors = validate_receipt(path, repo_root)
            errors.extend(receipt_errors)
            if data is None or receipt_errors:
                continue
            review_id = data["review_id"]
            report_path = data["review_report_path"]
            if review_id in seen_ids:
                errors.append(
                    f"{path}: duplicate review_id {review_id!r}; first seen in {seen_ids[review_id]}"
                )
            else:
                seen_ids[review_id] = path
            if report_path in seen_paths:
                errors.append(
                    f"{path}: duplicate review_report_path {report_path!r}; "
                    f"first seen in {seen_paths[report_path]}"
                )
            else:
                seen_paths[report_path] = path
            receipts.append(data)

    count = len(receipts) if not errors else 0
    return {
        "schema_version": 1,
        "valid": not errors,
        "completed_count": count,
        "threshold": threshold,
        "notification_eligible": not errors and count >= threshold,
        "errors": errors,
    }


def _fixture(index: int, report_path: str) -> dict:
    return {
        "schema_version": 1,
        "review_id": f"review-{index:02d}",
        "review_report_path": report_path,
        "status": "completed",
        "material_review": True,
        "reviewed_by": "unrecorded",
        "authored_by": "unrecorded",
        "ca_adjudication_status": "completed",
        "ca_adjudicator": "selftest",
        "accepted_net_new_material_findings": 0,
        "decision_changed": "no",
        "closure_state": "no_action",
        "report_lines": 10,
        "turn_count": "unknown",
        "evidence_pointers": [report_path],
        "completed_at": "2026-07-11",
    }


def run_selftest() -> int:
    failures: list[str] = []
    root = Path.cwd()
    receipts = root / DEFAULT_RECEIPTS
    report_paths = [
        "AGENTS.md", "CLAUDE.md", "README.md",
        ".agents/workflow-overlay/README.md",
        ".agents/workflow-overlay/source-of-truth.md",
        ".agents/workflow-overlay/source-loading.md",
        ".agents/workflow-overlay/decision-routing.md",
        ".agents/workflow-overlay/review-lanes.md",
        ".agents/workflow-overlay/validation-gates.md",
        ".github/workflows/ci.yml",
        ".github/workflows/batch0-owner-notify.yml",
    ]

    def reset(count: int) -> None:
        for item in receipts.glob("selftest-*.json"):
            item.unlink()
        for index in range(count):
            payload = _fixture(index, report_paths[index])
            (receipts / f"selftest-{index:02d}.json").write_text(
                json.dumps(payload), encoding="utf-8"
            )

    try:
        for count, eligible in ((0, False), (9, False), (10, True), (11, True)):
            reset(count)
            result = inspect_receipts(receipts, root, DEFAULT_THRESHOLD, "selftest-*.json")
            if (
                not result["valid"]
                or result["completed_count"] != count
                or result["notification_eligible"] is not eligible
            ):
                failures.append(f"threshold case {count} failed: {result}")

        reset(1)
        first = receipts / "selftest-00.json"
        malformed = json.loads(first.read_text(encoding="utf-8"))
        malformed.pop("ca_adjudicator")
        first.write_text(json.dumps(malformed), encoding="utf-8")
        result = inspect_receipts(receipts, root, DEFAULT_THRESHOLD, "selftest-*.json")
        if result["valid"] or result["completed_count"] != 0:
            failures.append(f"malformed case failed: {result}")

        reset(2)
        second = receipts / "selftest-01.json"
        duplicate = json.loads(second.read_text(encoding="utf-8"))
        duplicate["review_id"] = "review-00"
        second.write_text(json.dumps(duplicate), encoding="utf-8")
        result = inspect_receipts(receipts, root, DEFAULT_THRESHOLD, "selftest-*.json")
        if result["valid"] or result["completed_count"] != 0:
            failures.append(f"duplicate case failed: {result}")

        # A single malformed receipt zeroes the whole directory's count, even
        # when nine other receipts in the same directory are otherwise valid.
        # This is deliberate fail-closed behavior (a corrupted receipt must
        # never let the sample silently under-report as "9 valid" instead of
        # surfacing the error), not a partial-exclusion count.
        reset(10)
        mixed = receipts / "selftest-05.json"
        mixed_payload = json.loads(mixed.read_text(encoding="utf-8"))
        mixed_payload.pop("ca_adjudicator")
        mixed.write_text(json.dumps(mixed_payload), encoding="utf-8")
        result = inspect_receipts(receipts, root, DEFAULT_THRESHOLD, "selftest-*.json")
        if result["valid"] or result["completed_count"] != 0:
            failures.append(f"mixed valid+malformed case failed: {result}")
    finally:
        for item in receipts.glob("selftest-*.json"):
            item.unlink()

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("SELFTEST OK: 0/9/10/11, malformed, duplicate, and mixed valid+malformed cases")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipts", type=Path, default=DEFAULT_RECEIPTS)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--github-output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return run_selftest()
    if args.threshold < 1:
        print("threshold must be >= 1", file=sys.stderr)
        return 2

    repo_root = args.repo_root.resolve()
    receipts = args.receipts if args.receipts.is_absolute() else repo_root / args.receipts
    result = inspect_receipts(receipts, repo_root, args.threshold)
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as handle:
            handle.write(f"completed_count={result['completed_count']}\n")
            handle.write(f"notification_eligible={str(result['notification_eligible']).lower()}\n")
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            f"valid={result['valid']} completed={result['completed_count']} "
            f"threshold={result['threshold']} eligible={result['notification_eligible']}"
        )
        for error in result["errors"]:
            print(f"ERROR: {error}", file=sys.stderr)
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
