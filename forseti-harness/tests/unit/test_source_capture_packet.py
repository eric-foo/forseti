from __future__ import annotations

import json
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

import harness_utils
from harness_utils import hash_file
from runners import run_source_capture_packet as packet_runner
from source_capture import writer as packet_writer
from source_capture.models import (
    CaptureModeCategory,
    PacketTiming,
    SourceCapturePacket,
    SourceCaptureSlice,
    VisibleFact,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.writer import NON_CLAIMS, write_local_source_capture_packet


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"source_capture_packet_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def _minimal_packet_payload() -> dict[str, object]:
    return {
        "packet_id": "01TESTPACKET",
        "manifest_version": "source_capture_packet_manifest_v1",
        "obligation_contract_version": "core_spine_v0_data_capture_spine_obligation_contract_v0",
        "source_family": "docs_page",
        "source_surface": "local_file_artifact",
        "source_locator": {"status": "known", "value": "C:/source/input.txt"},
        "requested_decision_context": {"status": "known", "value": "What changed before cutoff?"},
        "capture_context": {"status": "known", "value": "local file packaging"},
        "actor_audience_context": {
            "status": "unknown_with_reason",
            "reason": "not supplied in local CLI mode",
        },
        "capture_mode": "agent-assisted",
        "operator_category": "local_cli_operator",
        "session_identity": "01SESSION",
        "visible_mode_changes": [],
        "timing": {
            "source_publication_or_event": {
                "status": "unknown_with_reason",
                "reason": "not supplied",
            },
            "source_edit_or_version": {
                "status": "unknown_with_reason",
                "reason": "not supplied",
            },
            "capture_time": {"status": "known", "value": "2026-06-02T00:00:00Z"},
            "recapture_time": {
                "status": "not_applicable",
                "reason": "no recapture supplied",
            },
            "cutoff_posture": {
                "status": "unknown_with_reason",
                "reason": "not supplied",
            },
        },
        "access_posture": {"status": "known", "value": "local_file_only"},
        "archive_history_posture": {
            "status": "not_attempted",
            "reason": "archive not queried",
        },
        "media_modality_posture": {
            "status": "not_attempted",
            "reason": "modality not assessed",
        },
        "re_capture_relationship": {
            "status": "not_applicable",
            "reason": "first capture only",
        },
        "source_slices": [
            {
                "slice_id": "slice_01",
                "locator": {"status": "known", "value": "C:/source/input.txt"},
                "timing": {
                    "source_publication_or_event": {
                        "status": "unknown_with_reason",
                        "reason": "not supplied",
                    },
                    "source_edit_or_version": {
                        "status": "unknown_with_reason",
                        "reason": "not supplied",
                    },
                    "capture_time": {"status": "known", "value": "2026-06-02T00:00:00Z"},
                    "recapture_time": {
                        "status": "not_applicable",
                        "reason": "no recapture supplied",
                    },
                    "cutoff_posture": {
                        "status": "unknown_with_reason",
                        "reason": "not supplied",
                    },
                },
                "access_posture": {"status": "known", "value": "local_file_only"},
                "archive_history_posture": {
                    "status": "not_attempted",
                    "reason": "archive not queried",
                },
                "media_modality_posture": {
                    "status": "not_attempted",
                    "reason": "modality not assessed",
                },
                "re_capture_relationship": {
                    "status": "not_applicable",
                    "reason": "first capture only",
                },
                "limitations": [],
                "warning_notes": [],
                "preserved_file_ids": ["file_01"],
            }
        ],
        "preserved_files": [
            {
                "file_id": "file_01",
                "original_path": "C:/source/input.txt",
                "relative_packet_path": "raw/01_input.txt",
                "sha256": "abc123",
                "hash_basis": "raw_stored_bytes",
                "size_bytes": 12,
            }
        ],
        "warnings": [],
        "limitations": [],
        "receipt_metadata": {
            "title": "Source Capture Packet Receipt",
            "generated_at": "2026-06-02T00:00:00Z",
            "summary": "Local-file-only packet for docs_page with 1 preserved file(s).",
            "non_claims": ["not source acquisition"],
        },
    }


def test_model_accepts_minimal_valid_local_packet_payload() -> None:
    packet = SourceCapturePacket.model_validate(_minimal_packet_payload())

    assert packet.capture_mode == CaptureModeCategory.AGENT_ASSISTED
    assert packet.source_family == "docs_page"
    assert packet.preserved_files[0].relative_packet_path == "raw/01_input.txt"


def test_packet_timing_archive_snapshot_time_is_optional_for_legacy_manifests() -> None:
    # Additive / forward-only: a manifest written before archive_snapshot_time existed (the
    # minimal payload omits it) still validates, and the field reads back as None on the packet
    # timing and every slice timing -- no manifest_version bump, no in-place upgrade required.
    payload = _minimal_packet_payload()
    assert "archive_snapshot_time" not in payload["timing"]  # type: ignore[operator]

    packet = SourceCapturePacket.model_validate(payload)

    assert packet.timing.archive_snapshot_time is None
    for source_slice in packet.source_slices:
        assert source_slice.timing.archive_snapshot_time is None


def test_packet_timing_accepts_explicit_archive_snapshot_time() -> None:
    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason("not supplied"),
        source_edit_or_version=unknown_with_reason("not supplied"),
        capture_time=known_fact("2026-06-11T00:00:00Z"),
        archive_snapshot_time=known_fact("2024-01-01T00:00:00Z"),
        recapture_time=not_applicable("first capture only"),
        cutoff_posture=unknown_with_reason("not supplied"),
    )

    assert timing.archive_snapshot_time is not None
    assert timing.archive_snapshot_time.value == "2024-01-01T00:00:00Z"
    # capture_time stays its own distinct fact.
    assert timing.capture_time.value == "2026-06-11T00:00:00Z"


def test_demand_durability_fields_optional_for_legacy_manifests() -> None:
    # Additive / forward-only (mirrors archive_snapshot_time): a manifest written before the
    # demand-durability fields existed (the minimal payload omits them) still validates, and the
    # new fields read back as None on the packet and every slice -- no manifest_version bump,
    # no in-place upgrade required.
    payload = _minimal_packet_payload()
    assert "series_id" not in payload
    assert "session_visibility_pin" not in payload["source_slices"][0]  # type: ignore[index]

    packet = SourceCapturePacket.model_validate(payload)

    assert packet.series_id is None
    assert packet.cold_start_at is None
    assert packet.pre_coverage_history_posture is None
    assert packet.intended_cadence is None
    for source_slice in packet.source_slices:
        assert source_slice.session_visibility_pin is None
        assert source_slice.locale_pin is None
        assert source_slice.currency_pin is None
        assert source_slice.variant_pin is None


def test_packet_accepts_explicit_demand_durability_fields() -> None:
    # A demand-durability observation populates Element 1 pins (per slice) and Element 2 & 4
    # series facts (per packet); they validate and round-trip. Pins are VisibleFacts (observed
    # facts, never weights -- INV-1); series-diff (Element 3) is intentionally not a field here.
    payload = _minimal_packet_payload()
    payload["series_id"] = "pilot_sdj_bumbum_001"
    payload["cold_start_at"] = {"status": "known", "value": "2026-06-14T17:45:09Z"}
    payload["pre_coverage_history_posture"] = {
        "status": "known",
        "value": "uncovered by construction; series began at first commissioned capture",
    }
    payload["intended_cadence"] = {"mode": "fixed", "slot_count": 14, "delay_seconds": 86400.0}
    slice0 = payload["source_slices"][0]  # type: ignore[index]
    slice0["session_visibility_pin"] = {"status": "known", "value": "logged_out_public"}
    slice0["locale_pin"] = {"status": "known", "value": "en-US"}
    slice0["currency_pin"] = {"status": "known", "value": "USD"}
    slice0["variant_pin"] = {
        "status": "unknown_with_reason",
        "reason": "default on-page variant; not pinned to a specific SKU id",
    }

    packet = SourceCapturePacket.model_validate(payload)

    assert packet.series_id == "pilot_sdj_bumbum_001"
    assert packet.cold_start_at is not None and packet.cold_start_at.value == "2026-06-14T17:45:09Z"
    assert packet.pre_coverage_history_posture is not None
    assert packet.intended_cadence == {"mode": "fixed", "slot_count": 14, "delay_seconds": 86400.0}
    observed = packet.source_slices[0]
    assert observed.session_visibility_pin is not None and observed.session_visibility_pin.value == "logged_out_public"
    assert observed.locale_pin is not None and observed.locale_pin.value == "en-US"
    assert observed.currency_pin is not None and observed.currency_pin.value == "USD"
    assert observed.variant_pin is not None and observed.variant_pin.status == "unknown_with_reason"


def test_model_rejects_missing_required_fields() -> None:
    payload = _minimal_packet_payload()
    del payload["source_family"]

    with pytest.raises(Exception):
        SourceCapturePacket.model_validate(payload)


def test_visible_fact_rejects_unknown_status_vocabulary() -> None:
    with pytest.raises(Exception):
        VisibleFact(status="partial", reason="belongs to obligation discharge vocabulary")


def test_visible_fact_rejects_known_without_value() -> None:
    with pytest.raises(Exception):
        VisibleFact(status="known")


def test_visible_fact_rejects_non_known_without_reason() -> None:
    with pytest.raises(Exception):
        VisibleFact(status="unknown_with_reason")


def test_model_rejects_slice_reference_to_unknown_preserved_file() -> None:
    payload = _minimal_packet_payload()
    payload["source_slices"][0]["preserved_file_ids"] = ["file_99"]  # type: ignore[index]

    with pytest.raises(Exception, match="unknown preserved file IDs"):
        SourceCapturePacket.model_validate(payload)


def test_model_rejects_unreferenced_preserved_file() -> None:
    payload = _minimal_packet_payload()
    payload["preserved_files"].append(  # type: ignore[union-attr]
        {
            "file_id": "file_02",
            "original_path": "C:/source/unused.txt",
            "relative_packet_path": "raw/02_unused.txt",
            "sha256": "def456",
            "hash_basis": "raw_stored_bytes",
            "size_bytes": 9,
        }
    )

    with pytest.raises(Exception, match="not referenced by any source slice"):
        SourceCapturePacket.model_validate(payload)


def test_writer_copies_files_records_sha256_and_writes_manifest_and_receipt(scratch_dir: Path) -> None:
    input_path = scratch_dir / "input.txt"
    output_dir = scratch_dir / "packet"
    input_path.write_text("hello source capture\n", encoding="utf-8")

    result = write_local_source_capture_packet(
        output_directory=output_dir,
        input_files=[input_path],
        source_family="docs_page",
        source_surface="local_file_artifact",
        source_locator=known_fact(str(input_path)),
        decision_question="What changed before the decision cutoff?",
        capture_context="local file packaging of already-local source artifacts",
        capture_mode=CaptureModeCategory.AGENT_ASSISTED,
        operator_category="local_cli_operator",
        warnings=["operator supplied only one local file"],
        limitations=["source publication time not supplied"],
    )

    manifest_path = Path(result.manifest_path)
    receipt_path = Path(result.receipt_path)
    copied_file = output_dir / "raw" / "01_input.txt"

    assert copied_file.exists()
    assert result.packet.preserved_files[0].sha256 == hash_file(copied_file)
    assert result.packet.preserved_files[0].relative_packet_path == "raw/01_input.txt"
    assert result.packet.preserved_files[0].hash_basis == "raw_stored_bytes"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["source_family"] == "docs_page"
    assert manifest["preserved_files"][0]["sha256"] == hash_file(copied_file)
    assert manifest["preserved_files"][0]["hash_basis"] == "raw_stored_bytes"

    receipt_text = receipt_path.read_text(encoding="utf-8")
    assert "# Source Capture Packet Receipt" in receipt_text
    assert "## Preserved Files" in receipt_text
    for non_claim in NON_CLAIMS:
        assert non_claim in receipt_text


def test_writer_preserves_explicit_empty_receipt_non_claims(scratch_dir: Path) -> None:
    input_path = scratch_dir / "input.txt"
    output_dir = scratch_dir / "packet"
    input_path.write_text("hello source capture\n", encoding="utf-8")

    result = write_local_source_capture_packet(
        output_directory=output_dir,
        input_files=[input_path],
        source_family="docs_page",
        source_surface="local_file_artifact",
        source_locator=known_fact(str(input_path)),
        decision_question="What changed before the decision cutoff?",
        capture_context="local file packaging of already-local source artifacts",
        receipt_non_claims=[],
    )

    assert result.packet.receipt_metadata.non_claims == []
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["receipt_metadata"]["non_claims"] == []
    receipt_text = (output_dir / "receipt.md").read_text(encoding="utf-8")
    assert "## Non-Claims\n\n- none" in receipt_text


def test_writer_rejects_empty_input_files(scratch_dir: Path) -> None:
    with pytest.raises(ValueError, match="at least one input file"):
        write_local_source_capture_packet(
            output_directory=scratch_dir / "packet",
            input_files=[],
            source_family="docs_page",
            source_surface="local_file_artifact",
            source_locator=known_fact("local input absent"),
            decision_question="What changed before the decision cutoff?",
            capture_context="local file packaging of already-local source artifacts",
        )


def test_writer_rejects_directory_as_input_file(scratch_dir: Path) -> None:
    input_dir = scratch_dir / "not_a_file"
    input_dir.mkdir()

    with pytest.raises(ValueError, match="input path is not a file"):
        write_local_source_capture_packet(
            output_directory=scratch_dir / "packet",
            input_files=[input_dir],
            source_family="docs_page",
            source_surface="local_file_artifact",
            source_locator=known_fact(str(input_dir)),
            decision_question="What changed before the decision cutoff?",
            capture_context="local file packaging of already-local source artifacts",
        )


def test_writer_handles_multiple_files_in_default_single_slice(scratch_dir: Path) -> None:
    first_input = scratch_dir / "first.txt"
    second_input = scratch_dir / "second.txt"
    output_dir = scratch_dir / "packet"
    first_input.write_text("first source\n", encoding="utf-8")
    second_input.write_text("second source\n", encoding="utf-8")

    result = write_local_source_capture_packet(
        output_directory=output_dir,
        input_files=[first_input, second_input],
        source_family="docs_page",
        source_surface="local_file_artifact",
        source_locator=known_fact("bounded local file set"),
        decision_question="What changed before the decision cutoff?",
        capture_context="local file packaging of already-local source artifacts",
    )

    assert [item.file_id for item in result.packet.preserved_files] == ["file_01", "file_02"]
    assert result.packet.source_slices[0].slice_id == "slice_01"
    assert result.packet.source_slices[0].preserved_file_ids == ["file_01", "file_02"]
    assert (output_dir / "raw" / "01_first.txt").exists()
    assert (output_dir / "raw" / "02_second.txt").exists()


@pytest.mark.parametrize(
    "failure_boundary",
    ["second_copy", "manifest_write", "receipt_write", "publish"],
)
def test_cli_atomic_packet_failure_leaves_no_final_set_and_retry_converges(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    failure_boundary: str,
) -> None:
    first_input = scratch_dir / "first.txt"
    second_input = scratch_dir / "second.txt"
    output_dir = scratch_dir / "packet"
    first_input.write_text("first source\n", encoding="utf-8")
    second_input.write_text("second source\n", encoding="utf-8")
    argv = [
        "--source-family",
        "docs_page",
        "--source-locator",
        "bounded local file set",
        "--decision-question",
        "What changed before the decision cutoff?",
        "--input-file",
        str(first_input),
        "--input-file",
        str(second_input),
        "--output",
        str(output_dir),
    ]

    if failure_boundary == "second_copy":
        original = packet_writer.shutil.copy2
        copy_calls = 0

        def fail_second_copy(*args: object, **kwargs: object) -> object:
            nonlocal copy_calls
            copy_calls += 1
            if copy_calls == 2:
                raise OSError("injected second body copy failure")
            return original(*args, **kwargs)

        monkeypatch.setattr(packet_writer.shutil, "copy2", fail_second_copy)
        restore = lambda: monkeypatch.setattr(packet_writer.shutil, "copy2", original)
        expected_diagnostic = "injected second body copy failure"
    elif failure_boundary in {"manifest_write", "receipt_write"}:
        original = Path.write_text
        failed_name = "manifest.json" if failure_boundary == "manifest_write" else "receipt.md"

        def fail_packet_text_write(
            path: Path, *args: object, **kwargs: object
        ) -> int:
            if path.name == failed_name:
                raise OSError(f"injected {failed_name} write failure")
            return original(path, *args, **kwargs)

        monkeypatch.setattr(Path, "write_text", fail_packet_text_write)
        restore = lambda: monkeypatch.setattr(Path, "write_text", original)
        expected_diagnostic = f"injected {failed_name} write failure"
    else:
        original = harness_utils.os.rename

        def fail_publish(*args: object, **kwargs: object) -> None:
            raise OSError("injected packet publish failure")

        monkeypatch.setattr(harness_utils.os, "rename", fail_publish)
        restore = lambda: monkeypatch.setattr(harness_utils.os, "rename", original)
        expected_diagnostic = "injected packet publish failure"

    with pytest.raises(SystemExit) as exc_info:
        packet_runner.main(argv)

    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert expected_diagnostic in captured.err
    assert captured.out == ""
    assert not output_dir.exists()
    assert list(scratch_dir.glob(".packet.staging-*")) == []

    restore()
    assert packet_runner.main(argv) == 0
    capsys.readouterr()

    assert sorted(
        path.relative_to(output_dir).as_posix()
        for path in output_dir.rglob("*")
        if path.is_file()
    ) == [
        "manifest.json",
        "raw/01_first.txt",
        "raw/02_second.txt",
        "receipt.md",
    ]
    packet = SourceCapturePacket.model_validate_json(
        (output_dir / "manifest.json").read_text(encoding="utf-8")
    )
    assert packet.preserved_files[0].sha256 == hash_file(output_dir / "raw" / "01_first.txt")
    assert packet.preserved_files[1].sha256 == hash_file(output_dir / "raw" / "02_second.txt")


def test_writer_accepts_explicit_multi_slice_path(scratch_dir: Path) -> None:
    first_input = scratch_dir / "first.txt"
    second_input = scratch_dir / "second.txt"
    output_dir = scratch_dir / "packet"
    first_input.write_text("first source\n", encoding="utf-8")
    second_input.write_text("second source\n", encoding="utf-8")
    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason("publication timing not supplied"),
        source_edit_or_version=unknown_with_reason("edit timing not supplied"),
        capture_time=known_fact("2026-06-02T00:00:00Z"),
        recapture_time=not_applicable("first local packetization"),
        cutoff_posture=unknown_with_reason("local-file packetization; cutoff posture not established"),
    )

    result = write_local_source_capture_packet(
        output_directory=output_dir,
        input_files=[first_input, second_input],
        source_family="docs_page",
        source_surface="local_file_artifact",
        source_locator=known_fact("bounded local file set"),
        decision_question="What changed before the decision cutoff?",
        capture_context="local file packaging of already-local source artifacts",
        source_slices=[
            SourceCaptureSlice(
                slice_id="slice_01",
                locator=known_fact(str(first_input)),
                timing=timing,
                access_posture=known_fact("local_file_only"),
                archive_history_posture=not_attempted("archive not queried"),
                media_modality_posture=not_attempted("media not queried"),
                re_capture_relationship=not_applicable("first local packetization"),
                preserved_file_ids=["file_01"],
            ),
            SourceCaptureSlice(
                slice_id="slice_02",
                locator=known_fact(str(second_input)),
                timing=timing,
                access_posture=known_fact("local_file_only"),
                archive_history_posture=not_attempted("archive not queried"),
                media_modality_posture=not_attempted("media not queried"),
                re_capture_relationship=not_applicable("first local packetization"),
                preserved_file_ids=["file_02"],
            ),
        ],
    )

    assert [source_slice.slice_id for source_slice in result.packet.source_slices] == [
        "slice_01",
        "slice_02",
    ]
    assert result.packet.source_slices[0].preserved_file_ids == ["file_01"]
    assert result.packet.source_slices[1].preserved_file_ids == ["file_02"]


def test_writer_rejects_non_empty_output_directory(scratch_dir: Path) -> None:
    input_path = scratch_dir / "input.txt"
    output_dir = scratch_dir / "packet"
    input_path.write_text("hello source capture\n", encoding="utf-8")
    output_dir.mkdir()
    (output_dir / "keep.txt").write_text("occupied\n", encoding="utf-8")

    with pytest.raises(ValueError, match="non-empty output directory"):
        write_local_source_capture_packet(
            output_directory=output_dir,
            input_files=[input_path],
            source_family="docs_page",
            source_surface="local_file_artifact",
            source_locator=known_fact(str(input_path)),
            decision_question="What changed before the decision cutoff?",
            capture_context="local file packaging of already-local source artifacts",
        )

    assert (output_dir / "keep.txt").read_text(encoding="utf-8") == "occupied\n"
    assert list(scratch_dir.glob(".packet.staging-*")) == []


def test_cli_writes_packet_from_local_input_file(scratch_dir: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    input_path = scratch_dir / "input.txt"
    output_dir = scratch_dir / "packet"
    input_path.write_text("hello source capture\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "runners/run_source_capture_packet.py",
            "--source-family",
            "docs_page",
            "--source-locator",
            str(input_path),
            "--decision-question",
            "What changed before the decision cutoff?",
            "--input-file",
            str(input_path),
            "--output",
            str(output_dir),
            "--actor-audience-context",
            "reddit financialcareers posters and commenters",
            "--source-publication-or-event",
            "source artifact contains Reddit post and comment timing from supplied JSON",
            "--source-edit-or-version-unknown-reason",
            "local markdown does not expose complete edit/version state",
            "--cutoff-posture-unknown-reason",
            "local JSON file state supplied for the pressure-test capture; cutoff posture not independently established by the local CLI",
            "--capture-time",
            "2026-06-01T12:34:56Z",
            "--recapture-time-not-applicable-reason",
            "dry-run packet is the first local packetization of this artifact",
            "--access-posture",
            "local_file_only",
            "--archive-history-not-attempted-reason",
            "dry-run did not query archives",
            "--media-modality-posture",
            "markdown artifact only; linked media not fetched by local CLI",
            "--recapture-relationship-not-applicable-reason",
            "no prior Source Capture Packet supplied",
            "--visible-mode-change",
            "none observed during local packetization",
            "--warning",
            "operator supplied only one local file",
            "--limitation",
            "source publication time not supplied",
        ],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert output_dir.exists()
    assert (output_dir / "manifest.json").exists()
    assert (output_dir / "receipt.md").exists()

    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["warnings"] == ["operator supplied only one local file"]
    assert manifest["limitations"] == ["source publication time not supplied"]
    assert manifest["receipt_metadata"]["non_claims"] == NON_CLAIMS
    assert manifest["actor_audience_context"]["value"] == "reddit financialcareers posters and commenters"
    assert (
        manifest["timing"]["source_publication_or_event"]["value"]
        == "source artifact contains Reddit post and comment timing from supplied JSON"
    )
    assert manifest["timing"]["source_edit_or_version"]["status"] == "unknown_with_reason"
    assert manifest["timing"]["cutoff_posture"]["status"] == "unknown_with_reason"
    assert manifest["timing"]["capture_time"]["status"] == "known"
    assert manifest["timing"]["capture_time"]["value"] == "2026-06-01T12:34:56Z"
    assert manifest["receipt_metadata"]["generated_at"] != "2026-06-01T12:34:56Z"
    assert manifest["access_posture"]["value"] == "local_file_only"
    assert manifest["archive_history_posture"]["status"] == "not_attempted"
    assert (
        manifest["media_modality_posture"]["value"]
        == "markdown artifact only; linked media not fetched by local CLI"
    )
    assert manifest["visible_mode_changes"] == ["none observed during local packetization"]

    receipt_text = (output_dir / "receipt.md").read_text(encoding="utf-8")
    assert "reddit financialcareers posters and commenters" in receipt_text
    assert "local JSON file state supplied for the pressure-test capture" in receipt_text
    assert "none observed during local packetization" in receipt_text


def test_cli_rejects_conflicting_metadata_value_and_reason(scratch_dir: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    input_path = scratch_dir / "input.txt"
    output_dir = scratch_dir / "packet"
    input_path.write_text("hello source capture\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "runners/run_source_capture_packet.py",
            "--source-family",
            "docs_page",
            "--source-locator",
            str(input_path),
            "--decision-question",
            "What changed before the decision cutoff?",
            "--input-file",
            str(input_path),
            "--output",
            str(output_dir),
            "--cutoff-posture",
            "known cutoff posture",
            "--cutoff-posture-unknown-reason",
            "conflicting unknown reason",
        ],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "cutoff posture accepts only one value/reason flag" in result.stderr
    assert not output_dir.exists()


def test_cli_rejects_empty_string_value_with_conflicting_reason(scratch_dir: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    input_path = scratch_dir / "input.txt"
    output_dir = scratch_dir / "packet"
    input_path.write_text("hello source capture\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "runners/run_source_capture_packet.py",
            "--source-family",
            "docs_page",
            "--source-locator",
            str(input_path),
            "--decision-question",
            "What changed before the decision cutoff?",
            "--input-file",
            str(input_path),
            "--output",
            str(output_dir),
            "--cutoff-posture",
            "",
            "--cutoff-posture-unknown-reason",
            "conflicting unknown reason",
        ],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "cutoff posture accepts only one value/reason flag" in result.stderr
    assert not output_dir.exists()


def test_cli_accepts_unknown_access_posture_reason(scratch_dir: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    input_path = scratch_dir / "input.txt"
    output_dir = scratch_dir / "packet"
    input_path.write_text("hello source capture\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "runners/run_source_capture_packet.py",
            "--source-family",
            "docs_page",
            "--source-locator",
            str(input_path),
            "--decision-question",
            "What changed before the decision cutoff?",
            "--input-file",
            str(input_path),
            "--output",
            str(output_dir),
            "--access-posture-unknown-reason",
            "operator did not classify local access posture",
        ],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["access_posture"] == {
        "reason": "operator did not classify local access posture",
        "status": "unknown_with_reason",
        "value": None,
    }


def test_missing_input_file_returns_failure(scratch_dir: Path) -> None:
    project_root = Path(__file__).resolve().parents[2]
    missing_input = scratch_dir / "missing.txt"
    output_dir = scratch_dir / "packet"

    result = subprocess.run(
        [
            sys.executable,
            "runners/run_source_capture_packet.py",
            "--source-family",
            "docs_page",
            "--source-locator-unknown-reason",
            "operator did not supply a live locator",
            "--decision-question",
            "What changed before the decision cutoff?",
            "--input-file",
            str(missing_input),
            "--output",
            str(output_dir),
        ],
        cwd=project_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "input file does not exist" in result.stderr
    assert not output_dir.exists()
