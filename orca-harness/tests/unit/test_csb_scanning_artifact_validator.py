from __future__ import annotations

import importlib.util
from pathlib import Path
import re
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


def _codes(text: str) -> set[str]:
    return {finding.code for finding in validator.validate_text(text)}


def _code_list(text: str) -> list[str]:
    return [finding.code for finding in validator.validate_text(text)]


def test_valid_csb_first_scan_artifact_passes() -> None:
    assert validator.validate_text(_valid_text()) == []


def test_fixture_expected_fail_has_broad_scout_error() -> None:
    findings = validator.validate_text((FIXTURE_DIR / "bad_missing_broad_scout.md").read_text(encoding="utf-8"))

    assert [finding.code for finding in findings] == ["missing_broad_scout_accounting"]


@pytest.mark.parametrize(
    ("old", "new", "expected_code"),
    [
        ("exact_queries_used: 2", "", "missing_intake_fields"),
        ("max_exact_queries_total: 3", "", "missing_run_cap_fields"),
        ("screening_moves_used: 2", "screening_moves_used: 9", "screening_moves_exceed_cap"),
        ("closeout_state: no_candidate_after_discovery", "closeout_state: SCAN_COMPLETE", "invalid_closeout_state"),
        ("closeout_state: no_candidate_after_discovery", "closeout_state:", "invalid_closeout_state"),
        ("source_context_status: SOURCE_CONTEXT_READY", "", "missing_intake_fields"),
    ],
)
def test_intake_contract_failures(old: str, new: str, expected_code: str) -> None:
    assert expected_code in _codes(_valid_text().replace(old, new, 1))


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
    assert expected_code in _codes(_valid_text().replace(old, new, 1))


def test_broad_scout_return_token_without_section_does_not_count() -> None:
    assert "missing_broad_scout_accounting" in _codes(_valid_text().replace("## Broad Scout Return", "## Scout Notes", 1))


def test_broad_scout_section_requires_route_ledger_parts() -> None:
    text = _valid_text().replace("access notes, and current-state", "current-state", 1)

    assert "missing_broad_scout_detail" in _codes(text)


def test_empty_broad_scout_section_requires_detail() -> None:
    text = re.sub(r"## Broad Scout Return\n\n.*?\n\n## CSB Board Intake", "## Broad Scout Return\n\n## CSB Board Intake", _valid_text(), count=1, flags=re.DOTALL)

    assert "missing_broad_scout_detail" in _codes(text)


def test_broad_scout_deepening_vocab_allows_natural_phrase() -> None:
    text = _valid_text().replace("Recommended main deepening:", "Deepening recommendation:", 1)

    assert "missing_broad_scout_detail" not in _codes(text)


def test_csb_row_accounting_requires_sbr_ids() -> None:
    text = (
        _valid_text()
        .replace("SBR-001 through SBR-003", "three rows", 1)
        .replace("SBR-001", "row one")
        .replace("SBR-002", "row two")
    )

    assert "missing_csb_row_ids" in _codes(text)


@pytest.mark.parametrize(
    ("old", "new", "expected_code"),
    [
        ("screening_moves_used: 2", "screening_moves_used: 3", "screening_moves_count_mismatch"),
        ("exact_queries_used: 2", "exact_queries_used: 1", "exact_queries_count_mismatch"),
        ("hidden_venue_pointers: 1", "hidden_venue_pointers: 2", "hidden_venue_pointer_count_mismatch"),
        ("capture_requests: 1", "capture_requests: 2", "capture_request_count_mismatch"),
    ],
)
def test_declared_counts_match_recorded_ledgers(old: str, new: str, expected_code: str) -> None:
    assert expected_code in _codes(_valid_text().replace(old, new, 1))


def test_recency_overclaim_text_fails() -> None:
    text = _valid_text().replace(
        "It did not decide candidates.",
        "Recency proves demand and clears gate for this fixture.",
        1,
    )

    assert "recency_as_proof" in _codes(text)


def test_fixture_expected_fail_has_engagement_overclaim_errors() -> None:
    findings = validator.validate_text((FIXTURE_DIR / "bad_engagement_overclaim.md").read_text(encoding="utf-8"))
    codes = {finding.code for finding in findings}

    assert "engagement_as_proof" in codes
    assert "engagement_gate_clearance_shortcut" in codes
    assert "engagement_route_binding_shortcut" in codes
    assert "engagement_final_resonance_weight" in codes


def test_engagement_nonclaim_text_passes() -> None:
    text = _valid_text().replace(
        "It did not decide candidates.",
        "Engagement does not prove demand, clear gates, bind Capture routes, or set final resonance weight.",
        1,
    )

    assert validator.validate_text(text) == []



def test_engagement_overclaim_does_not_cross_sentence_boundary() -> None:
    text = _valid_text().replace(
        "It did not decide candidates.",
        "Engagement is high. Our research proves demand.",
        1,
    )

    assert "engagement_as_proof" not in _codes(text)

def test_engagement_nonclaim_sentence_does_not_mask_later_overclaim() -> None:
    text = _valid_text().replace(
        "It did not decide candidates.",
        "Engagement does not prove demand. High engagement proves demand.",
        1,
    )

    assert "engagement_as_proof" in _codes(text)


@pytest.mark.parametrize(
    ("phrase", "expected_code"),
    [
        ("High engagement proves demand", "engagement_as_proof"),
        ("Demand is proven by high engagement", "engagement_as_proof"),
        ("High engagement clears demand gate", "engagement_gate_clearance_shortcut"),
        ("Gate clearance is justified by high engagement", "engagement_gate_clearance_shortcut"),
        ("High engagement binds the Capture route", "engagement_route_binding_shortcut"),
        ("Capture route is selected by high engagement", "engagement_route_binding_shortcut"),
        ("High engagement sets graph weight", "engagement_graph_weight_shortcut"),
        ("Public reaction confirms credibility", "engagement_credibility_shortcut"),
        ("High engagement proves artificial amplification", "engagement_amplification_shortcut"),
        ("Reaction volume clears Action Ceiling", "engagement_action_ceiling_shortcut"),
        ("This scan assigns final resonance weight", "engagement_final_resonance_weight"),
    ],
)
def test_engagement_overclaim_text_fails(phrase: str, expected_code: str) -> None:
    text = _valid_text().replace("It did not decide candidates.", phrase, 1)

    assert expected_code in _codes(text)


def test_observation_record_required() -> None:
    assert "missing_observation_records" in _codes(_valid_text().replace("observation_id: OBS-001", "observation_note: OBS-001", 1))


def test_observation_required_fields_enforced() -> None:
    assert "missing_observation_fields" in _codes(_valid_text().replace("claim_it_might_support: preservation pressure only\n", "", 1))


@pytest.mark.parametrize(
    ("old", "new", "expected_code"),
    [
        ("retrieval_date: 2026-06-23", "retrieval_date: soon", "invalid_observation_retrieval_date"),
        ("signal_stage: access_note", "signal_stage: proof", "invalid_signal_stage"),
        ("gate_role: none", "gate_role: gate_proof", "invalid_gate_role"),
        ("url: https://example.test/fixture-product", "url: fixture-product", "invalid_observation_url"),
    ],
)
def test_observation_field_values_enforced(old: str, new: str, expected_code: str) -> None:
    assert expected_code in _codes(_valid_text().replace(old, new, 1))


def test_missing_observation_vocab_fields_do_not_emit_invalid_enum_codes() -> None:
    text = _valid_text().replace("signal_stage: access_note\n", "", 1).replace("gate_role: none\n", "", 1)
    codes = _codes(text)

    assert "missing_observation_fields" in codes
    assert "invalid_signal_stage" not in codes
    assert "invalid_gate_role" not in codes


def test_candidate_observation_schema_enforced_when_present() -> None:
    text = _valid_text() + """

```yaml
candidate_observation_id: COBS-001
candidate: Fixture Candidate
supporting_observations:
  - OBS-001
decision_window: fixture window
competing_or_defeating_observations: []
capture_needed: unknown
```
"""

    assert "missing_candidate_observation_fields" in _codes(text)


def test_candidate_ready_requires_candidate_observation() -> None:
    text = _valid_text().replace(
        "closeout_state: no_candidate_after_discovery", "closeout_state: candidate_ready_for_next_lane", 2
    ).replace("`no_candidate_after_discovery`", "`candidate_ready_for_next_lane`", 1)

    assert "candidate_ready_without_candidate_observation" in _codes(text)


def test_no_candidate_closeout_rejects_candidate_observation() -> None:
    text = _valid_text() + """

```yaml
candidate_observation_id: COBS-001
candidate: Fixture Candidate
supporting_observations:
  - OBS-001
why_promoted: fixture support
decision_window: fixture window
competing_or_defeating_observations: []
capture_needed: unknown
```
"""

    assert "no_candidate_with_candidate_observation" in _codes(text)


def test_candidate_decision_closeout_must_match_intake() -> None:
    text = _valid_text().replace(
        "candidate_decision:\n  closeout_state: no_candidate_after_discovery",
        "candidate_decision:\n  closeout_state: capture_preservation_only",
        1,
    )

    assert "candidate_decision_closeout_mismatch" in _codes(text)


def test_closeout_section_must_repeat_intake_closeout() -> None:
    text = _valid_text().replace("`no_candidate_after_discovery`", "`capture_preservation_only`", 1)

    assert "closeout_state_not_in_closeout_section" in _codes(text)


def test_closeout_section_accepts_natural_normalized_state_text() -> None:
    text = _valid_text().replace("`no_candidate_after_discovery`", "No candidate after discovery.", 1)

    assert "closeout_state_not_in_closeout_section" not in _codes(text)


def test_capture_preservation_only_requires_capture_request() -> None:
    text = (
        _valid_text()
        .replace("capture_requests: 1", "capture_requests: 0", 1)
        .replace("capture_request_id: CR-001", "capture_request_note: CR-001", 1)
        .replace("closeout_state: no_candidate_after_discovery", "closeout_state: capture_preservation_only", 2)
        .replace("`no_candidate_after_discovery`", "`capture_preservation_only`", 1)
    )

    assert "preservation_without_capture_request" in _codes(text)


def test_capture_request_accounting_missing_when_section_and_intake_count_absent() -> None:
    text = _valid_text().replace("capture_requests: 1\n", "", 1).replace("## Capture Triage", "## Preservation Notes", 1)

    assert "missing_capture_request_accounting" in _codes(text)


def test_positive_capture_request_count_requires_capture_section() -> None:
    assert "missing_capture_request_accounting" in _codes(_valid_text().replace("## Capture Triage", "## Preservation Notes", 1))


def test_zero_capture_request_count_can_account_without_capture_section() -> None:
    text = (
        _valid_text()
        .replace("capture_requests: 1", "capture_requests: 0", 1)
        .replace("capture_request_id: CR-001", "capture_request_note: CR-001", 1)
        .replace("## Capture Triage", "## Preservation Notes", 1)
    )

    assert "missing_capture_request_accounting" not in _codes(text)


def test_capture_request_required_fields_enforced() -> None:
    assert "missing_capture_request_fields" in _codes(_valid_text().replace("what_capture_should_verify: whether current PDP availability needs preservation\n", "", 1))


def test_capture_request_url_entries_must_be_structured() -> None:
    text = _valid_text().replace(
        "urls:\n  - url: https://example.test/fixture-product\n    venue: Official PDP\n    observation_supported: OBS-001\n    gate_role: none",
        "urls:\n  - https://example.test/fixture-product",
        1,
    )

    assert "invalid_capture_request_urls" in _codes(text)


def test_capture_request_not_requested_boundaries_required() -> None:
    assert "missing_capture_request_not_requested_boundaries" in _codes(_valid_text().replace("  - route expansion\n", "", 1))


@pytest.mark.parametrize("state", ["cited_current", "unknown", "blocked_outside_current_binding", "not_applicable"])
def test_mgt_route_binding_states_allowed(state: str) -> None:
    text = _valid_text().replace("route_binding_state: unknown", f"route_binding_state: {state}", 1)

    assert "invalid_capture_route_binding_state" not in _codes(text)


@pytest.mark.parametrize("state", ["bound_by_scanning", "not_bound", "capture_owned", ""])
def test_non_mgt_route_binding_states_fail(state: str) -> None:
    replacement = f"route_binding_state: {state}" if state else "route_binding_state:"
    text = _valid_text().replace("route_binding_state: unknown", replacement, 1)

    assert "invalid_capture_route_binding_state" in _codes(text)


def test_invalid_route_binding_state_emits_once_per_field() -> None:
    text = _valid_text().replace("route_binding_state: unknown", "route_binding_state: not_bound", 1)

    assert _code_list(text).count("invalid_capture_route_binding_state") == 1


def test_missing_scan_intake_receipt_without_yaml_fails() -> None:
    assert "missing_scan_intake_receipt" in _codes("# Missing Intake\n\nNo YAML receipt here.")


def test_invalid_yaml_fence_fails() -> None:
    text = _valid_text().replace("commission_id: fixture_csb_first_scan", "commission_id: [", 1)

    codes = _codes(text)
    assert "invalid_yaml_fence" in codes
    assert "missing_scan_intake_receipt" in codes
