from __future__ import annotations

from pathlib import Path
import subprocess
import sys

import pytest

from harness_utils import canonical_yaml_hash, load_yaml_documents, load_yaml_file, write_yaml_file
from reports.case_report import build_case_report_path
from runners.run_case import DuplicateScoreError, run_fixed_case
from scoring.band_scorer import MappingVersionMismatchError


def test_report_path_is_deterministic(copied_project: Path) -> None:
    expected = copied_project / "reports" / "plumbing" / "tr_casetext_2023_v0_14" / "case_report.yaml"
    actual = build_case_report_path(copied_project, "plumbing", "tr_casetext_2023_v0_14")
    assert actual == expected


def test_mapping_version_mismatch_blocks_runner_without_allow_mapping_version_mismatch(copied_project: Path) -> None:
    case_dir = copied_project / "cases" / "plumbing" / "tr_casetext_2023_v0_14"
    ledger_path = case_dir / "facilitator_ledger.yaml"
    ledger_doc = load_yaml_file(ledger_path)
    ledger_doc["mapping_table_version_pin"] = "v0_13_old"
    ledger_without_hash = dict(ledger_doc)
    ledger_without_hash.pop("ledger_freeze_hash", None)
    ledger_doc["ledger_freeze_hash"] = canonical_yaml_hash(ledger_without_hash)
    write_yaml_file(ledger_path, ledger_doc)

    with pytest.raises(MappingVersionMismatchError):
        run_fixed_case(case_dir)

    failure_events = load_yaml_documents(copied_project / "memory" / "logs" / "failure_events.yaml")
    assert len(failure_events) == 1
    assert failure_events[0]["failure_type"] == "mapping_version_mismatch"
    assert failure_events[0]["severity"] == "blocking"
    assert failure_events[0]["scoring_result_ref"] is None
    assert failure_events[0]["scoring_result_hash"] is None

    artifacts = run_fixed_case(case_dir, allow_mapping_version_mismatch=True)
    score_doc = load_yaml_file(artifacts.score_path)
    assert score_doc["action_band_result"]["band_status"] == "conflict_escalate"


def test_duplicate_override_does_not_allow_mapping_version_mismatch(copied_project: Path) -> None:
    case_dir = copied_project / "cases" / "plumbing" / "tr_casetext_2023_v0_14"
    ledger_path = case_dir / "facilitator_ledger.yaml"
    ledger_doc = load_yaml_file(ledger_path)
    ledger_doc["mapping_table_version_pin"] = "v0_13_old"
    ledger_without_hash = dict(ledger_doc)
    ledger_without_hash.pop("ledger_freeze_hash", None)
    ledger_doc["ledger_freeze_hash"] = canonical_yaml_hash(ledger_without_hash)
    write_yaml_file(ledger_path, ledger_doc)

    with pytest.raises(MappingVersionMismatchError):
        run_fixed_case(case_dir, allow_duplicate_score=True)


def test_runner_blocks_duplicate_score_without_duplicate_override(copied_project: Path) -> None:
    case_dir = copied_project / "cases" / "plumbing" / "tr_casetext_2023_v0_14"
    run_fixed_case(case_dir)

    with pytest.raises(DuplicateScoreError):
        run_fixed_case(case_dir)


def test_runner_allows_duplicate_score_and_aggregates_case_report(copied_project: Path) -> None:
    case_dir = copied_project / "cases" / "plumbing" / "tr_casetext_2023_v0_14"
    first = run_fixed_case(case_dir)
    second = run_fixed_case(case_dir, allow_duplicate_score=True)

    report_doc = load_yaml_file(second.report_path)
    assert [entry["scoring_result_id"] for entry in report_doc["contestant_results"]] == [
        first.scoring_bundle.scoring_result.scoring_result_id,
        second.scoring_bundle.scoring_result.scoring_result_id,
    ]
    assert report_doc["failure_event_summary"]["total"] == 0


def test_archived_duplicate_warns_without_contaminating_active_report(copied_project: Path) -> None:
    case_dir = copied_project / "cases" / "plumbing" / "tr_casetext_2023_v0_14"
    first = run_fixed_case(case_dir)
    archive_dir = case_dir / "scores" / "archive"
    archive_dir.mkdir(exist_ok=True)
    archived_path = archive_dir / first.score_path.name
    first.score_path.replace(archived_path)

    second = run_fixed_case(case_dir)

    assert len(second.warnings) == 1
    assert first.scoring_bundle.scoring_result.scoring_result_id in second.warnings[0]
    report_doc = load_yaml_file(second.report_path)
    assert [entry["scoring_result_id"] for entry in report_doc["contestant_results"]] == [
        second.scoring_bundle.scoring_result.scoring_result_id
    ]
    assert archived_path.exists()


def test_runner_validates_explicit_project_root(copied_project: Path) -> None:
    case_dir = copied_project / "cases" / "plumbing" / "tr_casetext_2023_v0_14"
    artifacts = run_fixed_case(case_dir, project_root=copied_project)
    assert artifacts.report_path == build_case_report_path(copied_project, "plumbing", "tr_casetext_2023_v0_14")


def test_runner_rejects_wrong_explicit_project_root(copied_project: Path) -> None:
    case_dir = copied_project / "cases" / "plumbing" / "tr_casetext_2023_v0_14"
    with pytest.raises(ValueError, match="not under expected cases root"):
        run_fixed_case(case_dir, project_root=copied_project / "cases")


def test_script_style_runner_entrypoint(copied_project: Path) -> None:
    completed = subprocess.run(
        [sys.executable, "runners/run_case.py", "cases/plumbing/tr_casetext_2023_v0_14"],
        cwd=copied_project,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr
    assert "cases" in completed.stdout
    assert "reports" in completed.stdout
