from __future__ import annotations

from pathlib import Path

from harness_utils import NON_CLAIM_NOTICE, load_yaml_file, write_yaml_file, canonical_yaml_hash
from reports.case_report import build_case_report_path
from runners.run_case import run_fixed_case


def test_run_case_green_path(copied_project: Path) -> None:
    case_dir = copied_project / "cases" / "plumbing" / "tr_casetext_2023_v0_14"
    artifacts = run_fixed_case(case_dir)

    score_doc = load_yaml_file(artifacts.score_path)
    report_doc = load_yaml_file(artifacts.report_path)

    assert score_doc["action_band_result"]["action_floor"] == 6
    assert score_doc["action_band_result"]["action_ceiling"] == 6
    assert score_doc["action_band_result"]["band_status"] == "conflict_escalate"
    assert score_doc["recommended_level"] == 6
    assert score_doc["in_band"] is True
    assert score_doc["memorization_probe_result"] == "not_run"
    assert report_doc["non_claim_notice"] == NON_CLAIM_NOTICE
    assert artifacts.report_path == build_case_report_path(copied_project, "plumbing", "tr_casetext_2023_v0_14")
    assert len(report_doc["contestant_results"]) == 1


def test_runner_reads_blind_judgement_from_disk(copied_project: Path) -> None:
    case_dir = copied_project / "cases" / "plumbing" / "tr_casetext_2023_v0_14"
    judgement_path = case_dir / "runs" / "fixed_contestant" / "run_tr_casetext_fixed" / "blind_judgement.yaml"
    judgement_doc = load_yaml_file(judgement_path)
    judgement_doc["judgement_class"] = "recommend"
    judgement_doc["recommended_action"]["ladder_level"] = 5
    judgement_doc["recommended_action"]["action_label"] = "phase"
    write_yaml_file(judgement_path, judgement_doc)

    artifacts = run_fixed_case(case_dir)
    score_doc = load_yaml_file(artifacts.score_path)
    assert score_doc["under_band"] is True
    assert score_doc["recommended_level"] == 5


def test_knife_edge_option_value_mutation(copied_project: Path) -> None:
    case_dir = copied_project / "cases" / "plumbing" / "tr_casetext_2023_v0_14"
    ledger_path = case_dir / "facilitator_ledger.yaml"
    ledger_doc = load_yaml_file(ledger_path)
    ledger_doc["frozen_band_inputs"]["option_value"] = "moderate"
    ledger_without_hash = dict(ledger_doc)
    ledger_without_hash.pop("ledger_freeze_hash", None)
    ledger_doc["ledger_freeze_hash"] = canonical_yaml_hash(ledger_without_hash)
    write_yaml_file(ledger_path, ledger_doc)

    artifacts = run_fixed_case(case_dir)
    score_doc = load_yaml_file(artifacts.score_path)
    assert score_doc["action_band_result"]["action_floor"] == 3
    assert score_doc["action_band_result"]["action_ceiling"] == 3
    assert score_doc["action_band_result"]["band_status"] == "normal"


def test_case_report_aggregates_multiple_scores_for_same_run_when_rescore_allowed(copied_project: Path) -> None:
    case_dir = copied_project / "cases" / "plumbing" / "tr_casetext_2023_v0_14"
    first = run_fixed_case(case_dir)
    second = run_fixed_case(case_dir, allow_duplicate_score=True)

    report_doc = load_yaml_file(second.report_path)
    assert len(report_doc["contestant_results"]) == 2
    assert {entry["scoring_result_id"] for entry in report_doc["contestant_results"]} == {
        first.scoring_bundle.scoring_result.scoring_result_id,
        second.scoring_bundle.scoring_result.scoring_result_id,
    }
