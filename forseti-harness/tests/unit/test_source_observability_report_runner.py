from __future__ import annotations

import json
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import pytest
import yaml

from runners.run_source_observability_report import (
    build_source_observability_report,
    load_operator_records,
    write_source_observability_report,
)
from source_observability.models import ObservablePosture, SourceObservabilityRecord


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"source_observability_report_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def _record_payload(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "record_id": "R01",
        "source_ref": "slot3://reddit/R01",
        "source_family": "forum_thread",
        "source_language_posture": "preserved",
        "source_structure_posture": "preserved",
        "archive_body_posture": "not_applicable",
        "media_posture": "not_applicable",
        "access_posture": "preserved",
        "locator_visible": True,
        "cutoff_visible": True,
        "source_language_anchor_count": 2,
        "source_language_anchor_required": False,
        "source_structure_required": False,
        "media_required": False,
        "archive_body_expected": False,
        "limitation_notes": [],
    }
    values.update(overrides)
    return values


def test_load_operator_records_accepts_top_level_records_mapping(scratch_dir: Path) -> None:
    input_path = scratch_dir / "records.yaml"
    input_path.write_text(
        yaml.safe_dump({"records": [_record_payload(record_id="R02")]}),
        encoding="utf-8",
    )

    records = load_operator_records(input_path)

    assert len(records) == 1
    assert records[0].record_id == "R02"
    assert records[0].source_language_posture == ObservablePosture.PRESERVED


def test_load_operator_records_accepts_top_level_list(scratch_dir: Path) -> None:
    input_path = scratch_dir / "records.yaml"
    input_path.write_text(yaml.safe_dump([_record_payload()]), encoding="utf-8")

    records = load_operator_records(input_path)

    assert [record.record_id for record in records] == ["R01"]


def test_load_operator_records_rejects_missing_records_list(scratch_dir: Path) -> None:
    input_path = scratch_dir / "records.yaml"
    input_path.write_text(yaml.safe_dump({"not_records": []}), encoding="utf-8")

    with pytest.raises(ValueError, match="records list"):
        load_operator_records(input_path)


def test_build_report_exposes_counts_limitations_and_non_claims() -> None:
    record = SourceObservabilityRecord.model_validate(
        _record_payload(
            source_language_posture="pointer_only",
            source_language_anchor_count=0,
            source_language_anchor_required=True,
        )
    )

    report = build_source_observability_report([record])

    assert report["report_type"] == "source_observability_limitations_report"
    assert report["record_count"] == 1
    assert report["limitation_count"] == 1
    assert report["has_visible_limitations"] is True
    assert report["record_summaries"] == [
        {
            "record_id": "R01",
            "source_ref": "slot3://reddit/R01",
            "source_family": "forum_thread",
            "source_language_posture": "pointer_only",
            "source_structure_posture": "preserved",
            "archive_body_posture": "not_applicable",
            "media_posture": "not_applicable",
            "access_posture": "preserved",
            "locator_visible": True,
            "cutoff_visible": True,
            "source_language_anchor_count": 0,
            "source_language_anchor_required": True,
            "source_structure_required": False,
            "media_required": False,
            "archive_body_expected": False,
            "limitation_notes": [],
        }
    ]
    assert report["limitations"] == [
        {
            "record_id": "R01",
            "source_ref": "slot3://reddit/R01",
            "limitation_type": "source_language_anchor_missing",
            "posture": "pointer_only",
            "detail": "Source-language anchors are required but not visibly preserved.",
        }
    ]
    assert "not capture validation" in report["non_claims"]
    assert "not source acquisition" in report["non_claims"]
    assert "not source-access handling" in report["non_claims"]
    assert "not media capture" in report["non_claims"]


def test_write_report_writes_json_file(scratch_dir: Path) -> None:
    input_path = scratch_dir / "records.yaml"
    output_path = scratch_dir / "report.json"
    input_path.write_text(yaml.safe_dump({"records": [_record_payload()]}), encoding="utf-8")

    report = write_source_observability_report(input_path, output_path)
    persisted = json.loads(output_path.read_text(encoding="utf-8"))

    assert persisted == report
    assert persisted["record_count"] == 1
    assert persisted["limitation_count"] == 0


def test_script_style_runner_entrypoint_writes_report(scratch_dir: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    input_path = scratch_dir / "records.yaml"
    output_path = scratch_dir / "report.json"
    input_path.write_text(
        yaml.safe_dump(
            {
                "records": [
                    _record_payload(
                        source_language_posture="pointer_only",
                        source_language_anchor_count=0,
                        source_language_anchor_required=True,
                    )
                ]
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "runners/run_source_observability_report.py",
            str(input_path),
            "--output",
            str(output_path),
        ],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    persisted = json.loads(output_path.read_text(encoding="utf-8"))
    assert persisted["record_count"] == 1
    assert persisted["limitation_count"] == 1
    assert persisted["record_summaries"][0]["source_language_posture"] == "pointer_only"
    assert persisted["record_summaries"][0]["limitation_notes"] == []
    assert persisted["limitations"][0]["limitation_type"] == "source_language_anchor_missing"
