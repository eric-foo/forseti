#!/usr/bin/env python3
"""Validate minimum receipt shape for CSB-first scanning artifacts.

This is a local/manual checker. It does not run retrieval, grade signal
quality, validate candidates, bind Capture routes, or prove a scan is good. It
only checks that a CSB-first scan artifact preserves the mechanical receipt
shape needed for review: source context, caps, broad-scout accounting,
CSB-row accountability, exact-query accounting, venue/hidden-venue accounting,
observations, negatives/access notes, capture-request accounting, and a bounded
candidate closeout.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import sys
from typing import Any

import yaml

YAML_FENCE_RE = re.compile(r"```yaml\s*(?P<body>.*?)\s*```", re.IGNORECASE | re.DOTALL)

REQUIRED_INTAKE_FIELDS = {
    "commission_id",
    "scan_date",
    "mode",
    "subject",
    "source_context_status",
    "run_caps",
    "screening_moves_used",
    "exact_queries_used",
    "closeout_state",
}
REQUIRED_RUN_CAPS = {"max_screening_moves_total", "max_exact_queries_total"}
VALID_CLOSEOUT_STATES = {
    "candidate_ready_for_next_lane",
    "capture_preservation_only",
    "no_candidate_after_discovery",
}
VALID_SOURCE_CONTEXT_STATUS = "SOURCE_CONTEXT_READY"

SECTION_PATTERNS = {
    "broad_scout_accounting": re.compile(r"^##\s+Broad Scout\b", re.IGNORECASE | re.MULTILINE),
    "csb_row_accounting": re.compile(
        r"(csb_rows_consumed|Rows consumed as route map:)",
        re.IGNORECASE | re.MULTILINE,
    ),
    "exact_query_accounting": re.compile(
        r"^##\s+Exact Query Discovery Ledger\b",
        re.IGNORECASE | re.MULTILINE,
    ),
    "venue_evaluation": re.compile(r"^##\s+Venue Evaluation\b", re.IGNORECASE | re.MULTILINE),
    "hidden_venue_accounting": re.compile(
        r"^##\s+Hidden Venue Pointers\b",
        re.IGNORECASE | re.MULTILINE,
    ),
    "observations": re.compile(r"^##\s+(Screen-Light Observations|Observations)\b", re.IGNORECASE | re.MULTILINE),
    "negatives_access_notes": re.compile(r"^##\s+Negatives And Access Notes\b", re.IGNORECASE | re.MULTILINE),
    "capture_request_accounting": re.compile(
        r"^##\s+(Capture Requests|Capture Triage)\b",
        re.IGNORECASE | re.MULTILINE,
    ),
    "candidate_decision": re.compile(
        r"^##\s+(Candidate Decision|Candidate Observation Decision)\b",
        re.IGNORECASE | re.MULTILINE,
    ),
    "closeout": re.compile(r"^##\s+Closeout\b", re.IGNORECASE | re.MULTILINE),
}

FORBIDDEN_TEXT_PATTERNS = {
    "recency_as_proof": re.compile(
        r"\b(recency|recent|currentness|current-state|current state)\b.{0,60}\b(proves|proof|gate clearance|clears? gate|demand verdict)\b",
        re.IGNORECASE,
    ),
    "scanning_binds_capture": re.compile(
        r"\b(scan|scanning)\b.{0,60}\b(bind|binds|sets|selects)\b.{0,40}\bCapture\b.{0,40}\b(route|method)\b",
        re.IGNORECASE,
    ),
    "capture_authorized_by_scan": re.compile(
        r"\bCapture\b.{0,40}\b(authorized|route-bound|route bound)\b.{0,40}\b(scan|scanning)\b",
        re.IGNORECASE,
    ),
}


@dataclass(frozen=True)
class Finding:
    code: str
    message: str


def _normalize_vocab(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def _yaml_blocks(text: str) -> tuple[list[Any], list[Finding]]:
    blocks: list[Any] = []
    findings: list[Finding] = []
    for index, match in enumerate(YAML_FENCE_RE.finditer(text), start=1):
        try:
            blocks.append(yaml.safe_load(match.group("body")) or {})
        except yaml.YAMLError as exc:
            findings.append(Finding("invalid_yaml_fence", f"YAML fence {index} is invalid: {exc}"))
    return blocks, findings


def _find_intake(blocks: list[Any]) -> dict[str, Any] | None:
    for block in blocks:
        if not isinstance(block, dict):
            continue
        if "commission_id" in block:
            return block
    return None


def _as_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and re.fullmatch(r"\d+", value.strip()):
        return int(value.strip())
    return None


def _validate_intake(intake: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []

    missing = sorted(REQUIRED_INTAKE_FIELDS - set(intake))
    if missing:
        findings.append(
            Finding("missing_intake_fields", "Scan intake receipt is missing fields: " + ", ".join(missing))
        )

    status = intake.get("source_context_status")
    if status != VALID_SOURCE_CONTEXT_STATUS:
        findings.append(
            Finding(
                "source_context_not_ready",
                f"source_context_status must be {VALID_SOURCE_CONTEXT_STATUS}, got {status or '<blank>'}.",
            )
        )

    closeout = _normalize_vocab(intake.get("closeout_state"))
    if closeout not in VALID_CLOSEOUT_STATES:
        findings.append(
            Finding(
                "invalid_closeout_state",
                "closeout_state must be one of "
                + ", ".join(sorted(VALID_CLOSEOUT_STATES))
                + f", got {intake.get('closeout_state')}.",
            )
        )

    run_caps = intake.get("run_caps")
    if not isinstance(run_caps, dict):
        findings.append(Finding("missing_run_caps", "run_caps must be a mapping."))
        return findings

    missing_caps = sorted(REQUIRED_RUN_CAPS - set(run_caps))
    if missing_caps:
        findings.append(Finding("missing_run_cap_fields", "run_caps is missing fields: " + ", ".join(missing_caps)))

    _validate_used_within_cap(
        findings,
        intake,
        run_caps,
        "screening_moves_used",
        "max_screening_moves_total",
        "screening_moves_exceed_cap",
    )
    _validate_used_within_cap(
        findings,
        intake,
        run_caps,
        "exact_queries_used",
        "max_exact_queries_total",
        "exact_queries_exceed_cap",
    )

    return findings


def _validate_used_within_cap(
    findings: list[Finding],
    intake: dict[str, Any],
    run_caps: dict[str, Any],
    used_field: str,
    cap_field: str,
    code: str,
) -> None:
    used = _as_int(intake.get(used_field))
    cap = _as_int(run_caps.get(cap_field))
    if used is None or cap is None:
        return
    if used > cap:
        findings.append(Finding(code, f"{used_field}={used} exceeds {cap_field}={cap}."))


def _validate_required_receipt_parts(text: str, intake: dict[str, Any] | None = None) -> list[Finding]:
    findings: list[Finding] = []
    for name, pattern in SECTION_PATTERNS.items():
        if pattern.search(text):
            continue
        if name == "capture_request_accounting" and isinstance(intake, dict):
            if _as_int(intake.get("capture_requests")) == 0:
                continue
        findings.append(Finding(f"missing_{name}", f"Missing required CSB-first scan receipt part: {name}."))
    return findings


def _iter_yaml_items(value: Any, path: str = ""):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            yield child_path, key, child
            yield from _iter_yaml_items(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = f"{path}[{index}]"
            yield child_path, index, child
            yield from _iter_yaml_items(child, child_path)


def _validate_yaml_overclaims(blocks: list[Any]) -> list[Finding]:
    findings: list[Finding] = []
    for block in blocks:
        for path, key, value in _iter_yaml_items(block):
            key_norm = _normalize_vocab(key)
            value_norm = _normalize_vocab(value)
            if key_norm in {"recency_status", "recency_attention", "signal_stage"} and value_norm in {
                "proof",
                "demand_proof",
                "gate_clearance",
                "candidate_authorization",
            }:
                findings.append(Finding("invalid_signal_stage_overclaim", f"{path} must not use {value!r}."))
            if key_norm == "route_binding_state" and value_norm not in {"", "unknown", "not_bound"}:
                findings.append(
                    Finding(
                        "invalid_capture_route_binding_state",
                        f"{path} must stay unknown/not_bound, got {value!r}.",
                    )
                )
    return findings


def _validate_forbidden_text(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for code, pattern in FORBIDDEN_TEXT_PATTERNS.items():
        match = pattern.search(text)
        if match:
            excerpt = " ".join(match.group(0).split())
            findings.append(Finding(code, f"Forbidden overclaim language found: {excerpt!r}."))
    return findings


def validate_text(text: str) -> list[Finding]:
    blocks, yaml_findings = _yaml_blocks(text)
    findings = [*yaml_findings]
    intake = _find_intake(blocks)
    if intake is None:
        findings.append(
            Finding(
                "missing_scan_intake_receipt",
                "No YAML scan intake receipt with commission_id and source_context_status found.",
            )
        )
    else:
        findings.extend(_validate_intake(intake))

    findings.extend(_validate_required_receipt_parts(text, intake))
    findings.extend(_validate_yaml_overclaims(blocks))
    findings.extend(_validate_forbidden_text(text))
    return findings


def _expected_from_fixture(path: Path) -> str:
    first_line = path.read_text(encoding="utf-8").splitlines()[0]
    match = re.search(r"fixture_expected:\s*(pass|fail)", first_line)
    if not match:
        return ""
    return match.group(1)


def selftest() -> int:
    root = Path(__file__).resolve().parents[2]
    fixture_dir = root / "orca-harness" / "tests" / "fixtures" / "csb_scanning_artifacts"
    fixture_paths = sorted(fixture_dir.glob("*.md"))
    if not fixture_paths:
        print(f"SELFTEST FAILED: no fixtures found at {fixture_dir}")
        return 1

    ok = True
    for path in fixture_paths:
        expected = _expected_from_fixture(path)
        findings = validate_text(path.read_text(encoding="utf-8"))
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
    if "--selftest" in argv:
        return selftest()
    paths = [Path(arg) for arg in argv if not arg.startswith("-")]
    if not paths:
        print("usage: check_csb_scanning_artifact.py [--selftest] <scan-artifact> [...]", file=sys.stderr)
        return 2

    exit_code = 0
    for path in paths:
        findings = validate_text(path.read_text(encoding="utf-8"))
        if findings:
            exit_code = 1
            print(f"FAIL {path}")
            for finding in findings:
                print(f"  {finding.code}: {finding.message}")
        else:
            print(f"PASS {path}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
