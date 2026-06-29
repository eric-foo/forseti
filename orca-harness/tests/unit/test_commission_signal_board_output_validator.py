from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import sys

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_PATH = REPO_ROOT / ".agents" / "hooks" / "check_commission_signal_board_output.py"
FIXTURE_DIR = REPO_ROOT / "orca-harness" / "tests" / "fixtures" / "commission_signal_board_outputs"


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
        "valid_adjacent_research_proof_output.txt",
    ],
)
def test_valid_commission_signal_board_outputs_pass(fixture_name: str) -> None:
    findings = validator.validate_text((FIXTURE_DIR / fixture_name).read_text(encoding="utf-8"))
    assert findings == []



def test_signal_board_nonclaim_sentence_does_not_mask_later_overclaim() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text = text.replace(
        "Eligible for classifier handoff",
        "Engagement does not prove demand. High engagement proves demand.",
        1,
    )

    findings = validator.validate_text(text)

    assert "engagement_as_proof" in {finding.code for finding in findings}


def test_signal_board_engagement_overclaim_does_not_cross_sentence_boundary() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text = text.replace("Eligible for classifier handoff", "Engagement is high. Our research proves demand.", 1)

    findings = validator.validate_text(text)

    assert findings == []


def test_signal_board_zero_row_board_still_checks_engagement_overclaim() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text, replacements = re.subn(r"(\| Row ID .*?\n\| --- .*?\n)(?:\| SBR-.*?\n)+", r"\1", text, count=1)
    assert replacements == 1
    text = text.replace("relation utility only; graph weight is not signal strength", "High engagement proves demand", 1)

    findings = validator.validate_text(text)

    assert "engagement_as_proof" in {finding.code for finding in findings}

def test_signal_board_allows_engagement_nonclaim_boundary() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text = text.replace(
        "Eligible for classifier handoff",
        "Engagement does not prove demand, graph weight, or Commit/Scale support; eligible for classifier handoff",
        1,
    )

    findings = validator.validate_text(text)

    assert findings == []


@pytest.mark.parametrize(
    ("phrase", "expected_code"),
    [
        ("High engagement proves demand", "engagement_as_proof"),
        ("Demand is proven by high engagement", "engagement_as_proof"),
        ("High engagement sets graph weight", "engagement_graph_weight_shortcut"),
        ("Graph weight is high because of high engagement", "engagement_graph_weight_shortcut"),
        ("High engagement clears Commit/Scale support", "engagement_commit_scale_shortcut"),
        ("Public reaction confirms credibility", "engagement_credibility_shortcut"),
        ("Reaction volume clears Action Ceiling", "engagement_action_ceiling_shortcut"),
        ("This row assigns final resonance weight", "engagement_final_resonance_weight"),
    ],
)
def test_signal_board_flags_engagement_overclaim_classes(phrase: str, expected_code: str) -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text = text.replace("Eligible for classifier handoff", phrase, 1)

    findings = validator.validate_text(text)

    assert expected_code in {finding.code for finding in findings}


@pytest.mark.parametrize(
    ("fixture_name", "expected_code", "expected_row_id"),
    [
        ("bad_engagement_overclaim_output.txt", "engagement_as_proof", ""),
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


def test_signal_board_requires_recency_columns() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text = text.replace(" | Recency status | Recency attention |", " |", 1)

    findings = validator.validate_text(text)

    assert "missing_required_row_columns" in {finding.code for finding in findings}


def test_signal_board_validates_recency_vocab() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text, replacements = re.subn(
        r"(\| SBR-001 \| forums_community \| Reddit \| public thread \| dated consumer question \| consumer_language \| signal_unit \| )recent \| high( \| node_candidate \|)",
        r"\1too_new | proof\2",
        text,
        count=1,
    )
    assert replacements == 1

    findings = validator.validate_text(text)

    assert ("invalid_recency_status", "SBR-001") in {(finding.code, finding.row_id) for finding in findings}
    assert ("invalid_recency_attention", "SBR-001") in {(finding.code, finding.row_id) for finding in findings}


@pytest.mark.parametrize(
    "header_fragment",
    [" | Row purpose |", " | Graph role |", " | Graph weight hint |"],
)
def test_signal_board_requires_non_recency_shape_columns(header_fragment: str) -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text = text.replace(header_fragment, " |", 1)

    findings = validator.validate_text(text)

    assert "missing_required_row_columns" in {finding.code for finding in findings}


@pytest.mark.parametrize(
    ("valid_fragment", "invalid_fragment", "expected_code"),
    [
        (
            "| consumer_language | signal_unit | recent | high |",
            "| consumer_language | proof_unit | recent | high |",
            "invalid_row_purpose",
        ),
        (
            "| recent | high | node_candidate | medium |",
            "| recent | high | proof_node | medium |",
            "invalid_graph_role",
        ),
        (
            "| high | node_candidate | medium | source_backed |",
            "| high | node_candidate | proof | source_backed |",
            "invalid_graph_weight_hint",
        ),
    ],
)
def test_signal_board_validates_non_recency_vocab(
    valid_fragment: str,
    invalid_fragment: str,
    expected_code: str,
) -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text = text.replace(valid_fragment, invalid_fragment, 1)

    findings = validator.validate_text(text)

    assert (expected_code, "SBR-001") in {(finding.code, finding.row_id) for finding in findings}

def test_unknown_handoff_mode_is_rejected_before_cutoff_bypass() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text, mode_replacements = re.subn(r"(?m)^(\s{2})mode: backtest\s*$", r"\1mode: unknown", text, count=1)
    assert mode_replacements == 1
    text = text.replace(
        "| SBR-001 | forums_community | Reddit | public thread | dated consumer question | consumer_language | signal_unit | recent | high | node_candidate | medium | source_backed | URL and thread date supplied | existed_by_cutoff | in_window | Eligible for classifier handoff |",
        "| SBR-001 | forums_community | Reddit | public thread | dated consumer question | consumer_language | signal_unit | recent | high | node_candidate | medium | source_backed | URL and thread date supplied | existed_by_cutoff | uncertain | Eligible for classifier handoff |",
        1,
    )

    findings = validator.validate_text(text)

    assert "invalid_handoff_mode" in {finding.code for finding in findings}


def test_handoff_row_must_exist_in_signal_board_rows() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text, replacements = re.subn(r"(?m)^(\s*-\s*)SBR-001\s*$", r"\1SBR-999", text, count=1)
    assert replacements == 1

    findings = validator.validate_text(text)

    assert ("handoff_row_unknown", "SBR-999") in {(finding.code, finding.row_id) for finding in findings}


def test_handoff_validation_continues_with_malformed_unreferenced_row() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text = text.replace(
        "| SBR-001 | forums_community | Reddit | public thread | dated consumer question | consumer_language | signal_unit | recent | high | node_candidate | medium | source_backed | URL and thread date supplied | existed_by_cutoff | in_window | Eligible for classifier handoff |",
        "| SBR-001 | forums_community | Reddit | public thread | dated consumer question | consumer_language | signal_unit | recent | high | node_candidate | medium | source_backed | URL and thread date supplied | existed_by_cutoff | uncertain | Eligible for classifier handoff |",
        1,
    )
    text = text.replace(
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        "| SBR-BAD | malformed | row |",
        1,
    )

    findings = validator.validate_text(text)
    codes = {finding.code for finding in findings}

    assert "malformed_signal_board_row" in codes
    assert ("handoff_row_cutoff_invalid", "SBR-001") in {(finding.code, finding.row_id) for finding in findings}


def test_full_board_requires_sections_one_through_ten_in_order() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text, replacements = re.subn(
        r"(?ms)^### 9\. Visible Limitations\s+.*?(?=^### 10\.)",
        "",
        text,
        count=1,
    )
    assert replacements == 1

    findings = validator.validate_text(text)

    assert "invalid_section_contract" in {finding.code for finding in findings}


def test_row_ids_must_use_sbr_format() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text = text.replace("| SBR-001 | forums_community |", "| ROW-001 | forums_community |", 1)

    findings = validator.validate_text(text)

    assert ("invalid_row_id_format", "ROW-001") in {(finding.code, finding.row_id) for finding in findings}


def test_row_ids_must_be_monotonic() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text = text.replace("| SBR-002 | reviews |", "| SBR-004 | reviews |", 1)

    findings = validator.validate_text(text)

    assert ("non_monotonic_row_id", "SBR-004") in {(finding.code, finding.row_id) for finding in findings}


def test_row_vocab_must_use_prompt_values() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text = text.replace("| SBR-001 | forums_community |", "| SBR-001 | forum-ish |", 1)

    findings = validator.validate_text(text)

    assert ("invalid_source_family", "SBR-001") in {(finding.code, finding.row_id) for finding in findings}


def test_handoff_packet_requires_shape_fields() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text = text.replace("  classifier_mapping_status: classifier_owned\n", "", 1)

    findings = validator.validate_text(text)

    assert "missing_handoff_packet_fields" in {finding.code for finding in findings}
    assert "invalid_classifier_mapping_status" in {finding.code for finding in findings}


def test_board_status_values_are_constrained() -> None:
    text = (FIXTURE_DIR / "valid_source_backed_backtest_output.txt").read_text(encoding="utf-8")
    text = text.replace("board_status: READY_FOR_RETRIEVAL_HANDOFF", "board_status: READY_FOR_DEMAND_VERDICT", 1)
    text = text.replace("run_boundary: CHAT_ONLY_BOARD_COMPLETE", "run_boundary: RAN_CLASSIFIER", 1)

    findings = validator.validate_text(text)
    codes = {finding.code for finding in findings}

    assert "invalid_board_status" in codes
    assert "invalid_run_boundary" in codes
