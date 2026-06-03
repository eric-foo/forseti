from __future__ import annotations

import json
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import pytest
import yaml

from source_capture.source_quality import build_source_quality_report_skeleton


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"source_quality_skeleton_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_archive_metadata_only_suggests_archive_body_not_preserved(scratch_dir: Path) -> None:
    packet_dir = _write_archive_metadata_only_packet(scratch_dir)

    skeleton = build_source_quality_report_skeleton(
        packet_or_manifest_path=packet_dir,
        source_id="CW-P1",
    )["mini_god_tier_source_quality_report_skeleton"]

    assert skeleton["suggested_result_token"] == "archive_body_not_preserved"
    assert skeleton["result_token_finalization"] == "operator_review_required"
    assert skeleton["best_in_bound_body"] == {
        "posture": "metadata_only",
        "preserved_body_path": "none",
        "sha256": "none",
        "byte_count": "none",
        "source_or_snapshot_time": "earliest observed availability timestamp 20230920050729; no selected snapshot",
    }
    assert "Archive availability metadata selected_snapshot is null." in skeleton["visible_limitations"]
    assert "none_observed_in_manifest" not in skeleton["visible_limitations"]


def test_archive_snapshot_body_is_preserved_but_not_auto_met(scratch_dir: Path) -> None:
    packet_dir = _write_archive_snapshot_body_packet(scratch_dir)

    skeleton = build_source_quality_report_skeleton(
        packet_or_manifest_path=packet_dir,
        source_id="CW-P4",
        source_language_anchors=["operator supplied title anchor"],
        coverage_or_drift_note="improves prior posture",
    )["mini_god_tier_source_quality_report_skeleton"]

    assert skeleton["suggested_result_token"] == "mini_god_tier_with_visible_limitations"
    assert skeleton["suggested_result_token"] != "mini_god_tier_met"
    assert skeleton["best_in_bound_body"]["posture"] == "preserved"
    assert skeleton["best_in_bound_body"]["preserved_body_path"] == "raw/02_archive_snapshot_body.bin"
    assert skeleton["best_in_bound_body"]["source_or_snapshot_time"] == "20220511053411"
    assert skeleton["provenance"]["content_type"] == "text/html; charset=UTF-8"
    assert skeleton["source_language_anchors"] == ["operator supplied title anchor"]
    assert skeleton["operator_completion_required"] == [
        "review suggested_result_token against the Mini God-Tier profile"
    ]


def test_direct_http_body_carries_archive_not_attempted_limitation(scratch_dir: Path) -> None:
    packet_dir = _write_direct_http_packet(scratch_dir)

    skeleton = build_source_quality_report_skeleton(
        packet_or_manifest_path=packet_dir / "manifest.json",
        source_id="CW-P6",
    )["mini_god_tier_source_quality_report_skeleton"]

    assert skeleton["suggested_result_token"] == "mini_god_tier_with_visible_limitations"
    assert skeleton["best_in_bound_body"]["posture"] == "preserved"
    assert skeleton["best_in_bound_body"]["preserved_body_path"] == "raw/01_http_response_body.bin"
    assert skeleton["provenance"]["content_type"] == "text/html"
    assert (
        "archive_history_posture: not_attempted - direct HTTP adapter does not query archive or history services"
        in skeleton["visible_limitations"]
    )


def test_separately_admitted_requires_lifecycle_decision_reference(scratch_dir: Path) -> None:
    packet_dir = _write_direct_http_packet(scratch_dir)

    missing_references = [None, "", "   ", "none", " NONE "]
    for missing_reference in missing_references:
        with pytest.raises(ValueError, match="separately_admitted requires lifecycle_decision_reference"):
            build_source_quality_report_skeleton(
                packet_or_manifest_path=packet_dir,
                source_id="CW-P6",
                lifecycle_state="separately_admitted",
                lifecycle_decision_reference=missing_reference,
            )


def test_metadata_only_non_archive_packet_reports_body_possession_not_proven(scratch_dir: Path) -> None:
    packet_dir = _write_direct_http_metadata_only_packet(scratch_dir)

    skeleton = build_source_quality_report_skeleton(
        packet_or_manifest_path=packet_dir,
        source_id="CW-METADATA-ONLY",
    )["mini_god_tier_source_quality_report_skeleton"]

    assert skeleton["suggested_result_token"] == "body_possession_not_proven"
    assert skeleton["best_in_bound_body"] == {
        "posture": "not_preserved",
        "preserved_body_path": "none",
        "sha256": "none",
        "byte_count": "none",
        "source_or_snapshot_time": "unknown_with_reason: no preserved body file identified",
    }


def test_cli_reports_manifest_validation_failures_separately(scratch_dir: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    packet_dir = scratch_dir / "invalid_packet"
    packet_dir.mkdir()
    (packet_dir / "manifest.json").write_text(json.dumps({"not": "a source capture packet"}), encoding="utf-8")
    output_path = scratch_dir / "skeleton.yaml"

    result = subprocess.run(
        [
            sys.executable,
            "runners/run_source_quality_report_skeleton.py",
            "--packet",
            str(packet_dir),
            "--source-id",
            "BROKEN",
            "--output",
            str(output_path),
        ],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "manifest validation failed" in result.stderr
    assert not output_path.exists()


def test_separately_admitted_accepts_real_lifecycle_reference(scratch_dir: Path) -> None:
    packet_dir = _write_direct_http_packet(scratch_dir)

    skeleton = build_source_quality_report_skeleton(
        packet_or_manifest_path=packet_dir,
        source_id="CW-P6",
        lifecycle_state="separately_admitted",
        lifecycle_decision_reference="docs/decisions/source_unit_fixture_admission_v0.md",
    )["mini_god_tier_source_quality_report_skeleton"]

    assert skeleton["lifecycle_state"] == "separately_admitted"
    assert skeleton["lifecycle_decision_reference"] == "docs/decisions/source_unit_fixture_admission_v0.md"


def test_clean_manifest_limitation_sentinel_preserves_operator_review_guard(scratch_dir: Path) -> None:
    packet_dir = _write_clean_direct_http_packet(scratch_dir)

    skeleton = build_source_quality_report_skeleton(
        packet_or_manifest_path=packet_dir,
        source_id="CW-CLEAN-MANIFEST",
        source_language_anchors=["operator-visible title"],
        coverage_or_drift_note="single current source body",
    )["mini_god_tier_source_quality_report_skeleton"]

    assert skeleton["visible_limitations"] == [
        "none_observed_in_manifest; operator_review_required still applies"
    ]
    assert skeleton["result_token_finalization"] == "operator_review_required"


def test_package_public_api_does_not_export_manifest_path_helper() -> None:
    import source_capture

    assert "resolve_manifest_path" not in source_capture.__all__


def test_separately_admitted_requires_lifecycle_decision_reference_from_cli(scratch_dir: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    packet_dir = _write_direct_http_packet(scratch_dir)
    output_path = scratch_dir / "skeleton.yaml"

    result = subprocess.run(
        [
            sys.executable,
            "runners/run_source_quality_report_skeleton.py",
            "--packet",
            str(packet_dir),
            "--source-id",
            "CW-P6",
            "--output",
            str(output_path),
            "--lifecycle-state",
            "separately_admitted",
            "--lifecycle-decision-reference",
            "none",
        ],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "separately_admitted requires lifecycle_decision_reference" in result.stderr
    assert not output_path.exists()


def test_separately_admitted_requires_lifecycle_decision_reference_when_defaulted(scratch_dir: Path) -> None:
    packet_dir = _write_direct_http_packet(scratch_dir)

    with pytest.raises(ValueError, match="separately_admitted requires lifecycle_decision_reference"):
        build_source_quality_report_skeleton(
            packet_or_manifest_path=packet_dir,
            source_id="CW-P6",
            lifecycle_state="separately_admitted",
        )


def test_cli_writes_yaml_report_skeleton(scratch_dir: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    packet_dir = _write_archive_metadata_only_packet(scratch_dir)
    output_path = scratch_dir / "skeleton.yaml"

    result = subprocess.run(
        [
            sys.executable,
            "runners/run_source_quality_report_skeleton.py",
            "--packet",
            str(packet_dir),
            "--source-id",
            "CW-P1",
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
    skeleton = output["mini_god_tier_source_quality_report_skeleton"]
    assert skeleton["source_id"] == "CW-P1"
    assert skeleton["suggested_result_token"] == "archive_body_not_preserved"
    assert skeleton["non_claims"] == [
        "not validation",
        "not source completeness proof",
        "not fixture admission unless separately decided",
        "not Judgment scoring",
    ]


def _write_archive_metadata_only_packet(root: Path) -> Path:
    packet_dir = root / "archive_metadata_only"
    raw_dir = packet_dir / "raw"
    raw_dir.mkdir(parents=True)
    metadata = {
        "availability_http_metadata": {
            "capture_timestamp": "2026-06-03T07:35:51Z",
            "content_type": "application/json",
            "final_url": "https://web.archive.org/cdx/search/cdx?url=https%3A%2F%2Fexample.com&output=json",
            "status": 200,
        },
        "original_url": "https://example.com/source",
        "selected_snapshot": None,
        "snapshot_count": 2,
        "snapshots": [
            {"timestamp": "20230920050729"},
            {"timestamp": "20240211045656"},
        ],
    }
    (raw_dir / "01_archive_availability_metadata.json").write_text(
        json.dumps(metadata),
        encoding="utf-8",
    )
    _write_manifest(
        packet_dir,
        source_surface="archive_org_wayback",
        capture_mode="archive/history",
        access_posture=_known("archive_org availability metadata preserved; no eligible snapshot body requested"),
        archive_history_posture=_known("archive_org availability metadata preserved; no eligible snapshot selected"),
        media_modality_posture=_not_applicable("archive runner does not retrieve linked media assets"),
        preserved_files=[
            _preserved_file("file_01", "raw/01_archive_availability_metadata.json", 2500),
        ],
        source_slices=[
            _source_slice(
                "archive_availability",
                preserved_file_ids=["file_01"],
                locator="https://web.archive.org/cdx/search/cdx?url=https%3A%2F%2Fexample.com&output=json",
                access_posture=_known("archive_org availability direct_http succeeded with HTTP 200 OK"),
                archive_history_posture=_known("archive_org availability metadata preserved; no eligible snapshot selected"),
                media_modality_posture=_not_applicable("archive availability metadata is not a media asset"),
            )
        ],
    )
    return packet_dir


def _write_archive_snapshot_body_packet(root: Path) -> Path:
    packet_dir = root / "archive_snapshot_body"
    raw_dir = packet_dir / "raw"
    raw_dir.mkdir(parents=True)
    (raw_dir / "01_archive_availability_metadata.json").write_text(
        json.dumps({"selected_snapshot": {"timestamp": "20220511053411"}}),
        encoding="utf-8",
    )
    (raw_dir / "02_archive_snapshot_body.bin").write_text("archived body", encoding="utf-8")
    (raw_dir / "03_archive_snapshot_body_metadata.json").write_text(
        json.dumps(
            {
                "selected_snapshot": {
                    "snapshot_url": "https://web.archive.org/web/20220511053411/https://example.com/source",
                    "timestamp": "20220511053411",
                },
                "snapshot_body_http_metadata": {
                    "capture_timestamp": "2026-06-02T21:31:03Z",
                    "content_type": "text/html; charset=UTF-8",
                    "final_url": "https://web.archive.org/web/20220511053411/https://example.com/source",
                    "status": 200,
                },
            }
        ),
        encoding="utf-8",
    )
    _write_manifest(
        packet_dir,
        source_surface="archive_org_wayback",
        capture_mode="archive/history",
        access_posture=_known("archive_org availability metadata and selected snapshot body preserved"),
        archive_history_posture=_known("archive_org availability metadata preserved; snapshot body preserved for 20220511053411"),
        media_modality_posture=_not_applicable("archive runner does not retrieve linked media assets"),
        preserved_files=[
            _preserved_file("file_01", "raw/01_archive_availability_metadata.json", 100),
            _preserved_file("file_02", "raw/02_archive_snapshot_body.bin", 13),
            _preserved_file("file_03", "raw/03_archive_snapshot_body_metadata.json", 300),
        ],
        source_slices=[
            _source_slice(
                "archive_availability",
                preserved_file_ids=["file_01"],
                locator="https://web.archive.org/cdx/search/cdx?url=https%3A%2F%2Fexample.com&output=json",
                access_posture=_known("archive_org availability direct_http succeeded with HTTP 200 OK"),
                archive_history_posture=_known("archive_org availability metadata preserved; snapshot body preserved for 20220511053411"),
                media_modality_posture=_not_applicable("archive availability metadata is not a media asset"),
            ),
            _source_slice(
                "archive_snapshot_body",
                preserved_file_ids=["file_02", "file_03"],
                locator="https://web.archive.org/web/20220511053411/https://example.com/source",
                access_posture=_known("archive_org snapshot body direct_http succeeded with HTTP 200 OK"),
                archive_history_posture=_known("archive_org snapshot body preserved for 20220511053411"),
                media_modality_posture=_not_applicable("archive snapshot body is preserved as raw response body"),
                source_edit_or_version=_known("Archive.org snapshot timestamp 20220511053411"),
            ),
        ],
    )
    return packet_dir


def _write_direct_http_packet(root: Path) -> Path:
    packet_dir = root / "direct_http"
    raw_dir = packet_dir / "raw"
    raw_dir.mkdir(parents=True)
    (raw_dir / "01_http_response_body.bin").write_text("direct body", encoding="utf-8")
    (raw_dir / "02_http_response_metadata.json").write_text(
        json.dumps(
            {
                "capture_timestamp": "2026-06-03T07:36:14Z",
                "content_type": "text/html",
                "final_url": "https://www.sec.gov/example.htm",
                "status": 200,
            }
        ),
        encoding="utf-8",
    )
    _write_manifest(
        packet_dir,
        source_surface="direct_http",
        capture_mode="structured access",
        access_posture=_known("direct_http succeeded with HTTP 200 OK"),
        archive_history_posture=_not_attempted("direct HTTP adapter does not query archive or history services"),
        media_modality_posture=_not_attempted("direct HTTP adapter preserves the response body only and does not fetch linked media assets"),
        preserved_files=[
            _preserved_file("file_01", "raw/01_http_response_body.bin", 11),
            _preserved_file("file_02", "raw/02_http_response_metadata.json", 120),
        ],
        source_slices=[
            _source_slice(
                "slice_01",
                preserved_file_ids=["file_01", "file_02"],
                locator="https://www.sec.gov/example.htm",
                access_posture=_known("direct_http succeeded with HTTP 200 OK"),
                archive_history_posture=_not_attempted("direct HTTP adapter does not query archive or history services"),
                media_modality_posture=_not_attempted("direct HTTP adapter preserves the response body only and does not fetch linked media assets"),
                cutoff_posture=_known("current retrieval of stable SEC Archives URL"),
            )
        ],
    )
    return packet_dir


def _write_direct_http_metadata_only_packet(root: Path) -> Path:
    packet_dir = root / "direct_http_metadata_only"
    raw_dir = packet_dir / "raw"
    raw_dir.mkdir(parents=True)
    (raw_dir / "01_http_response_metadata.json").write_text(
        json.dumps(
            {
                "capture_timestamp": "2026-06-03T07:36:14Z",
                "content_type": "application/json",
                "final_url": "https://www.sec.gov/example.htm",
                "status": 200,
            }
        ),
        encoding="utf-8",
    )
    _write_manifest(
        packet_dir,
        source_surface="direct_http",
        capture_mode="structured access",
        access_posture=_known("direct_http metadata preserved without inspectable source body"),
        archive_history_posture=_not_attempted("direct HTTP adapter does not query archive or history services"),
        media_modality_posture=_not_attempted("direct HTTP adapter preserves the response body only and does not fetch linked media assets"),
        preserved_files=[
            _preserved_file("file_01", "raw/01_http_response_metadata.json", 120),
        ],
        source_slices=[
            _source_slice(
                "slice_01",
                preserved_file_ids=["file_01"],
                locator="https://www.sec.gov/example.htm",
                access_posture=_known("direct_http metadata preserved without inspectable source body"),
                archive_history_posture=_not_attempted("direct HTTP adapter does not query archive or history services"),
                media_modality_posture=_not_attempted("direct HTTP adapter preserves the response body only and does not fetch linked media assets"),
                cutoff_posture=_known("current retrieval of stable SEC Archives URL"),
            )
        ],
    )
    return packet_dir


def _write_clean_direct_http_packet(root: Path) -> Path:
    packet_dir = root / "clean_direct_http"
    raw_dir = packet_dir / "raw"
    raw_dir.mkdir(parents=True)
    (raw_dir / "01_http_response_body.bin").write_text("direct body", encoding="utf-8")
    (raw_dir / "02_http_response_metadata.json").write_text(
        json.dumps(
            {
                "capture_timestamp": "2026-06-03T07:36:14Z",
                "content_type": "text/html",
                "final_url": "https://www.sec.gov/example.htm",
                "status": 200,
            }
        ),
        encoding="utf-8",
    )
    _write_manifest(
        packet_dir,
        source_surface="direct_http",
        capture_mode="structured access",
        access_posture=_known("direct_http succeeded with HTTP 200 OK"),
        archive_history_posture=_known("archive body relationship already handled by selected packet"),
        media_modality_posture=_not_applicable("no linked media in this source unit"),
        preserved_files=[
            _preserved_file("file_01", "raw/01_http_response_body.bin", 11),
            _preserved_file("file_02", "raw/02_http_response_metadata.json", 120),
        ],
        source_slices=[
            _source_slice(
                "slice_01",
                preserved_file_ids=["file_01", "file_02"],
                locator="https://www.sec.gov/example.htm",
                access_posture=_known("direct_http succeeded with HTTP 200 OK"),
                archive_history_posture=_known("archive body relationship already handled by selected packet"),
                media_modality_posture=_not_applicable("no linked media in this source unit"),
                cutoff_posture=_known("current retrieval of stable SEC Archives URL"),
            )
        ],
    )
    return packet_dir


def _write_manifest(
    packet_dir: Path,
    *,
    source_surface: str,
    capture_mode: str,
    access_posture: dict[str, object],
    archive_history_posture: dict[str, object],
    media_modality_posture: dict[str, object],
    preserved_files: list[dict[str, object]],
    source_slices: list[dict[str, object]],
) -> None:
    manifest = {
        "packet_id": "01TESTPACKET",
        "manifest_version": "source_capture_packet_manifest_v0",
        "obligation_contract_version": "core_spine_v0_data_capture_spine_obligation_contract_v0",
        "source_family": "web_page",
        "source_surface": source_surface,
        "source_locator": _known("https://example.com/source"),
        "requested_decision_context": _known("What source state was visible before cutoff?"),
        "capture_context": _known("test packet"),
        "actor_audience_context": _unknown("not supplied"),
        "capture_mode": capture_mode,
        "operator_category": "test_operator",
        "session_identity": "01SESSION",
        "visible_mode_changes": [],
        "timing": _timing(),
        "access_posture": access_posture,
        "archive_history_posture": archive_history_posture,
        "media_modality_posture": media_modality_posture,
        "re_capture_relationship": _not_applicable("first capture"),
        "source_slices": source_slices,
        "preserved_files": preserved_files,
        "warnings": [],
        "limitations": [],
        "receipt_metadata": {
            "title": "Source Capture Packet Receipt",
            "generated_at": "2026-06-03T00:00:00Z",
            "summary": "test packet",
            "non_claims": ["not Judgment scoring"],
        },
    }
    (packet_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")


def _source_slice(
    slice_id: str,
    *,
    preserved_file_ids: list[str],
    locator: str,
    access_posture: dict[str, object],
    archive_history_posture: dict[str, object],
    media_modality_posture: dict[str, object],
    source_edit_or_version: dict[str, object] | None = None,
    cutoff_posture: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "slice_id": slice_id,
        "locator": _known(locator),
        "timing": _timing(
            source_edit_or_version=source_edit_or_version,
            cutoff_posture=cutoff_posture,
        ),
        "access_posture": access_posture,
        "archive_history_posture": archive_history_posture,
        "media_modality_posture": media_modality_posture,
        "re_capture_relationship": _not_applicable("first capture"),
        "limitations": [],
        "warning_notes": [],
        "preserved_file_ids": preserved_file_ids,
    }


def _timing(
    *,
    source_edit_or_version: dict[str, object] | None = None,
    cutoff_posture: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "source_publication_or_event": _unknown("not supplied"),
        "source_edit_or_version": source_edit_or_version or _unknown("not supplied"),
        "capture_time": _known("2026-06-03T00:00:00Z"),
        "recapture_time": _not_applicable("first capture"),
        "cutoff_posture": cutoff_posture or _known("test cutoff posture"),
    }


def _preserved_file(file_id: str, relative_packet_path: str, size_bytes: int) -> dict[str, object]:
    return {
        "file_id": file_id,
        "original_path": f"C:/tmp/{relative_packet_path}",
        "relative_packet_path": relative_packet_path,
        "sha256": f"sha-{file_id}",
        "size_bytes": size_bytes,
    }


def _known(value: str) -> dict[str, object]:
    return {"status": "known", "value": value}


def _unknown(reason: str) -> dict[str, object]:
    return {"status": "unknown_with_reason", "reason": reason}


def _not_attempted(reason: str) -> dict[str, object]:
    return {"status": "not_attempted", "reason": reason}


def _not_applicable(reason: str) -> dict[str, object]:
    return {"status": "not_applicable", "reason": reason}
