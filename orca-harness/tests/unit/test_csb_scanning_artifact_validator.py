from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_PATH = REPO_ROOT / ".agents" / "hooks" / "check_csb_scanning_artifact.py"
FIXTURE_DIR = REPO_ROOT / "orca-harness" / "tests" / "fixtures" / "csb_scanning_artifacts"


def _load_validator():
    spec = importlib.util.spec_from_file_location("check_csb_scanning_artifact", VALIDATOR_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = _load_validator()


def _valid_text() -> str:
    return (FIXTURE_DIR / "valid_csb_first_scan.md").read_text(encoding="utf-8")


def test_valid_csb_first_scan_artifact_passes() -> None:
    findings = validator.validate_text(_valid_text())
    assert findings == []


def test_fixture_expected_fail_has_broad_scout_error() -> None:
    findings = validator.validate_text((FIXTURE_DIR / "bad_missing_broad_scout.md").read_text(encoding="utf-8"))

    assert ("missing_broad_scout_accounting",) in {(finding.code,) for finding in findings}


@pytest.mark.parametrize(
    ("old", "new", "expected_code"),
    [
        ("exact_queries_used: 2", "", "missing_intake_fields"),
        ("max_exact_queries_total: 3", "", "missing_run_cap_fields"),
        ("screening_moves_used: 4", "screening_moves_used: 9", "screening_moves_exceed_cap"),
        ("closeout_state: no_candidate_after_discovery", "closeout_state: SCAN_COMPLETE", "invalid_closeout_state"),
        ("closeout_state: no_candidate_after_discovery", "closeout_state:", "invalid_closeout_state"),
        ("source_context_status: SOURCE_CONTEXT_READY", "", "missing_intake_fields"),
    ],
)
def test_intake_contract_failures(old: str, new: str, expected_code: str) -> None:
    text = _valid_text().replace(old, new, 1)

    findings = validator.validate_text(text)

    assert expected_code in {finding.code for finding in findings}


@pytest.mark.parametrize(
    ("old", "new", "expected_code"),
    [
        ("Rows consumed as route map: SBR-001 through SBR-003.", "Rows were reviewed.", "missing_csb_row_accounting"),
        ("## Exact Query Discovery Ledger", "## Query Notes", "missing_exact_query_accounting"),
        ("## Venue Evaluation Move Log", "## Move Log", "missing_venue_evaluation"),
        ("## Hidden Venue Pointers", "## Pointer Notes", "missing_hidden_venue_accounting"),
        ("## Negatives And Access Notes", "## Notes", "missing_negatives_access_notes"),
        ("## Observations", "## Move Notes", "missing_observations"),
        ("## Candidate Decision", "## Decision Notes", "missing_candidate_decision"),
        ("## Closeout", "## Final Note", "missing_closeout"),
    ],
)
def test_required_receipt_parts(old: str, new: str, expected_code: str) -> None:
    text = _valid_text().replace(old, new, 1)

    findings = validator.validate_text(text)

    assert expected_code in {finding.code for finding in findings}


def test_recency_overclaim_text_fails() -> None:
    text = _valid_text().replace(
        "It did not decide candidates.",
        "Recency proves demand and clears gate for this fixture.",
        1,
    )

    findings = validator.validate_text(text)

    assert "recency_as_proof" in {finding.code for finding in findings}


def test_capture_route_binding_yaml_fails() -> None:
    text = _valid_text().replace("route_binding_state: unknown", "route_binding_state: bound_by_scanning", 1)

    findings = validator.validate_text(text)

    assert "invalid_capture_route_binding_state" in {finding.code for finding in findings}


def test_broad_scout_return_token_without_section_does_not_count() -> None:
    text = _valid_text().replace("## Broad Scout Return", "## Scout Notes", 1)

    findings = validator.validate_text(text)

    assert "missing_broad_scout_accounting" in {finding.code for finding in findings}


def test_capture_request_accounting_missing_when_section_and_intake_count_absent() -> None:
    text = _valid_text().replace("capture_requests: 1\n", "", 1).replace("## Capture Triage", "## Preservation Notes", 1)

    findings = validator.validate_text(text)

    assert "missing_capture_request_accounting" in {finding.code for finding in findings}


def test_positive_capture_request_count_requires_capture_section() -> None:
    text = _valid_text().replace("## Capture Triage", "## Preservation Notes", 1)

    findings = validator.validate_text(text)

    assert "missing_capture_request_accounting" in {finding.code for finding in findings}


def test_zero_capture_request_count_can_account_without_capture_section() -> None:
    text = _valid_text().replace("capture_requests: 1", "capture_requests: 0", 1).replace(
        "## Capture Triage", "## Preservation Notes", 1
    )

    findings = validator.validate_text(text)

    assert "missing_capture_request_accounting" not in {finding.code for finding in findings}


def test_missing_scan_intake_receipt_without_yaml_fails() -> None:
    findings = validator.validate_text("# Missing Intake\n\nNo YAML receipt here.")

    assert "missing_scan_intake_receipt" in {finding.code for finding in findings}


def test_invalid_yaml_fence_fails() -> None:
    text = _valid_text().replace("commission_id: fixture_csb_first_scan", "commission_id: [", 1)

    findings = validator.validate_text(text)

    codes = {finding.code for finding in findings}
    assert "invalid_yaml_fence" in codes
    assert "missing_scan_intake_receipt" in codes


def test_capture_owned_route_binding_state_fails() -> None:
    text = _valid_text().replace("route_binding_state: unknown", "route_binding_state: capture_owned", 1)

    findings = validator.validate_text(text)

    assert "invalid_capture_route_binding_state" in {finding.code for finding in findings}
