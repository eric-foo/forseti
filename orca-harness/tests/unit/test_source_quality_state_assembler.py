from __future__ import annotations

import json
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import pytest
import yaml

from source_capture import known_fact, write_local_source_capture_packet
from source_capture.source_quality import build_source_quality_state_census


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"source_quality_state_assembler_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_state_assembler_surfaces_existing_packet_skeleton_without_finalizing(scratch_dir: Path) -> None:
    packet_dir = _write_local_body_packet(scratch_dir)

    census = build_source_quality_state_census(
        rows=[
            {
                "source_id": "CW-PACKET",
                "case_or_slot": "Canoo/Walmart source-quality trial",
                "row_status": "packet_written_needs_report",
                "packet_path": str(packet_dir),
                "source_language_anchors": ["operator-visible headline"],
                "coverage_or_drift_note": "standardizes current body posture",
                "packet_lifecycle": "scratch",
            }
        ],
        base_path=Path.cwd(),
    )["source_quality_state_assembler"]

    row = census["rows"][0]
    assert row["source_id"] == "CW-PACKET"
    assert row["packet_state"] == "manifest_inspectable"
    assert row["helper_state"] == "skeleton_built"
    assert row["suggested_result_token"] == "mini_god_tier_with_visible_limitations"
    assert row["suggested_result_token"] != "mini_god_tier_met"
    assert row["result_token_finalization"] == "operator_review_required"
    assert row["mini_god_tier_source_quality_report_skeleton"]["source_language_anchors"] == [
        "operator-visible headline"
    ]
    assert census["census"]["row_status_counts"] == {"packet_written_needs_report": 1}
    assert census["census"]["packet_state_counts"] == {"manifest_inspectable": 1}
    assert "not runner dispatch" in census["non_claims"]


def test_missing_packet_path_is_visible_row_stop_without_dispatching(scratch_dir: Path) -> None:
    missing_packet = scratch_dir / "does_not_exist"

    census = build_source_quality_state_census(
        rows=[
            {
                "source_id": "CW-MISSING",
                "case_or_slot": "Canoo/Walmart source-quality trial",
                "row_status": "ready_for_tool_run",
                "packet_path": str(missing_packet),
                "packet_lifecycle": "scratch",
            }
        ],
        base_path=Path.cwd(),
    )["source_quality_state_assembler"]

    row = census["rows"][0]
    assert row["row_status"] == "ready_for_tool_run"
    assert row["packet_state"] == "manifest_missing"
    assert row["helper_state"] == "not_invoked"
    assert row["suggested_result_token"] == "none"
    assert any("manifest not found" in item for item in row["visible_stops"])
    assert census["census"]["visible_stop_count"] == 1


def test_invalid_manifest_is_row_failure_not_batch_verdict(scratch_dir: Path) -> None:
    packet_dir = scratch_dir / "invalid_packet"
    packet_dir.mkdir()
    (packet_dir / "manifest.json").write_text(json.dumps({"not": "a packet"}), encoding="utf-8")

    census = build_source_quality_state_census(
        rows=[
            {
                "source_id": "CW-BROKEN",
                "case_or_slot": "Canoo/Walmart source-quality trial",
                "row_status": "packet_written_needs_report",
                "packet_path": str(packet_dir),
                "packet_lifecycle": "scratch",
            }
        ],
        base_path=Path.cwd(),
    )["source_quality_state_assembler"]

    row = census["rows"][0]
    assert row["packet_state"] == "manifest_uninspectable"
    assert row["helper_state"] == "helper_failed"
    assert any("source-quality skeleton helper failed" in item for item in row["visible_stops"])
    assert census["census"]["helper_state_counts"] == {"helper_failed": 1}


def test_not_cited_packet_remains_visible_stop(scratch_dir: Path) -> None:
    census = build_source_quality_state_census(
        rows=[
            {
                "source_id": "CW-PLANNED",
                "case_or_slot": "Canoo/Walmart source-quality trial",
                "row_status": "planned",
            }
        ],
        base_path=scratch_dir,
    )["source_quality_state_assembler"]

    row = census["rows"][0]
    assert row["packet_state"] == "not_cited"
    assert row["helper_state"] == "not_invoked"
    assert any("assembler did not run Source Capture tools" in item for item in row["visible_stops"])


def test_empty_rows_are_rejected() -> None:
    with pytest.raises(ValueError, match="at least one source-quality row is required"):
        build_source_quality_state_census(rows=[])


def test_cli_writes_state_census_yaml(scratch_dir: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    packet_dir = _write_local_body_packet(scratch_dir)
    queue_path = scratch_dir / "queue.yaml"
    output_path = scratch_dir / "state_census.yaml"
    queue_path.write_text(
        yaml.safe_dump(
            {
                "rows": [
                    {
                        "source_id": "CW-CLI",
                        "case_or_slot": "Canoo/Walmart source-quality trial",
                        "row_status": "packet_written_needs_report",
                        "packet_path": str(packet_dir),
                        "source_language_anchors": ["operator-visible headline"],
                        "coverage_or_drift_note": "standardizes current body posture",
                        "packet_lifecycle": "scratch",
                    }
                ]
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "runners/run_source_quality_state_assembler.py",
            "--queue",
            str(queue_path),
            "--output",
            str(output_path),
        ],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    output = yaml.safe_load(output_path.read_text(encoding="utf-8"))
    census = output["source_quality_state_assembler"]
    assert census["row_count"] == 1
    assert census["rows"][0]["helper_state"] == "skeleton_built"
    assert census["rows"][0]["result_token_finalization"] == "operator_review_required"


def _write_local_body_packet(root: Path) -> Path:
    source_file = root / "source_body.html"
    source_file.write_text("<html><body>operator-visible headline</body></html>", encoding="utf-8")
    packet_dir = root / "local_packet"
    write_local_source_capture_packet(
        output_directory=packet_dir,
        input_files=[source_file],
        source_family="web_page",
        source_surface="local_file",
        source_locator=known_fact("https://example.test/source"),
        decision_question="What source body was preserved?",
        capture_context="unit test source-quality state assembler packet",
        cutoff_posture=known_fact("current local packet test cutoff"),
    )
    return packet_dir
