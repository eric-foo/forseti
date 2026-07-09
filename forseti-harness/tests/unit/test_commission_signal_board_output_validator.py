from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import sys

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_PATH = REPO_ROOT / ".agents" / "hooks" / "check_commission_signal_board_output.py"
FIXTURE_DIR = REPO_ROOT / "forseti-harness" / "tests" / "fixtures" / "commission_signal_board_outputs"


def _load_validator():
    spec = importlib.util.spec_from_file_location("check_commission_signal_board_output", VALIDATOR_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = _load_validator()


@pytest.mark.parametrize(
    "fixture_name",
    [
        "valid_empty_backtest_output.txt",
        "valid_source_backed_backtest_output.txt",
        "valid_source_backed_forward_output.txt",
    ],
)
def test_valid_commission_signal_board_outputs_pass(fixture_name: str) -> None:
    findings = validator.validate_text((FIXTURE_DIR / fixture_name).read_text(encoding="utf-8"))
    assert findings == []


@pytest.mark.parametrize(
    ("fixture_name", "expected_code", "expected_row_id"),
    [
        ("bad_uncertain_cutoff_in_handoff_output.txt", "handoff_row_cutoff_invalid", "SBR-001"),
        ("bad_aeo_future_info_in_handoff_output.txt", "handoff_row_aeo_visibility", "SBR-001"),
        ("bad_to_retrieve_in_handoff_output.txt", "handoff_row_not_source_backed", "SBR-001"),
        ("bad_mixed_case_aeo_handoff_output.txt", "handoff_row_aeo_visibility", "SBR-001"),
        ("bad_missing_handoff_mode_backtest_output.txt", "missing_handoff_mode", ""),
        ("bad_surface_cutoff_uncertain_handoff_output.txt", "handoff_row_surface_cutoff_invalid", "SBR-001"),
        ("bad_forward_excluded_future_info_handoff_output.txt", "handoff_row_future_info", "SBR-001"),
    ],
)
def test_invalid_commission_signal_board_outputs_fail(
    fixture_name: str,
    expected_code: str,
    expected_row_id: str,
) -> None:
    findings = validator.validate_text((FIXTURE_DIR / fixture_name).read_text(encoding="utf-8"))
    assert findings
    assert (expected_code, expected_row_id) in {(finding.code, finding.row_id) for finding in findings}


def test_handoff_row_must_exist_in_signal_board_rows() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text, replacements = re.subn(r"(?m)^(\s*-\s*)SBR-001\s*$", r"\1SBR-999", text, count=1)
    assert replacements == 1

    findings = validator.validate_text(text)

    assert ("handoff_row_unknown", "SBR-999") in {(finding.code, finding.row_id) for finding in findings}


def test_handoff_validation_continues_with_malformed_unreferenced_row() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text = text.replace(
        "| SBR-001 | forums_community | Reddit | public thread | dated consumer question | consumer_language | signal_unit | node_candidate | medium | source_backed | URL and thread date supplied | existed_by_cutoff | in_window | Eligible for classifier handoff |",
        "| SBR-001 | forums_community | Reddit | public thread | dated consumer question | consumer_language | signal_unit | node_candidate | medium | source_backed | URL and thread date supplied | existed_by_cutoff | uncertain | Eligible for classifier handoff |",
        1,
    )
    text = text.replace(
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        "| SBR-BAD | malformed | row |",
        1,
    )

    findings = validator.validate_text(text)
    codes = {finding.code for finding in findings}

    assert "malformed_signal_board_row" in codes
    assert ("handoff_row_cutoff_invalid", "SBR-001") in {(finding.code, finding.row_id) for finding in findings}
