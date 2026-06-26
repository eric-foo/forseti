"""Offline ASR (youtube_audio -> transcript_asr) ECR + Cleaning smoke/audit integration (AO-2).

Network-free + ASR-free: a canned audio blob + an injected FAKE transcriber write a real audio
packet + transcribed transcript_asr record into a temp lake (DataLakeRoot.for_test). The smoke
runner stitches them into a derived_record-anchored cleaning handle; the periodic audit RESOLVES
that record from the lake and RE-HASHES it. The tamper tests prove the audit truly verifies (not
silently skips): mutating / removing the record, or withholding the lake, flips the audit.

Spec: cleaning_derived_record_anchor_contract_v0.md (acceptance criteria 1-7).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from cleaning.models import (
    CleaningEcrRef,
    CleaningInputHandle,
    CleaningPacket,
    CleaningRawAnchor,
    CleaningDerivedRecordRef,
)
from data_lake.root import DataLakeRoot
from runners.run_capture_ecr_cleaning_smoke import run_capture_ecr_cleaning_smoke
from runners.run_cleaning_spine_periodic_audit import run_cleaning_spine_periodic_audit
from source_capture.transcript import write_asr_transcript


_AUDIO = b"FAKE-OPUS-AUDIO-BYTES-FOR-ASR-SMOKE"
_MODEL_INFO = {
    "tool": "faster-whisper",
    "tool_version": "1.2.1",
    "model": "small",
    "model_repo_id": "Systran/faster-whisper-small",
    "model_digest": None,
    "model_digest_basis": "not available from the faster-whisper runtime",
    "compute_type": "int8",
    "decode_params": {"beam_size": 1, "vad_filter": True},
    "speech_gate": "faster-whisper builtin Silero VAD (onnx)",
}


def _transcribed(_audio_path):
    return (
        "transcribed",
        [{"start_ms": 0, "end_ms": 1500, "text": "I really love the CeraVe moisturizer"}],
        _MODEL_INFO,
    )


def _write_audio_packet_with_transcript(
    data_root: DataLakeRoot,
    *,
    transcribe_fn=_transcribed,
    video_id: str = "abcdefghijk",
) -> str:
    """Write the audio packet + transcript_asr record; return the audio packet_id."""
    code, msg = write_asr_transcript(
        video_id=video_id,
        audio_bytes=_AUDIO,
        audio_ext="webm",
        transcribe_fn=transcribe_fn,
        data_root=data_root,
        now_iso="2026-06-20T00:00:00Z",
    )
    assert code == 0, msg
    # msg: "derived/<shard>/<packet_id>/transcript_asr/<record_id> [posture, N cues]"
    return msg.split("/")[2]


def _record_dir(data_root: DataLakeRoot, audio_packet_id: str) -> Path:
    return data_root.lane_dir(
        subtree="derived", raw_anchor=audio_packet_id, lane="transcript_asr"
    )


def _write_smoke_manifest(tmp_path: Path, audio_packet_id: str) -> Path:
    manifest = {
        "run_id": "asr_smoke_fixture",
        "youtube_asr": [
            {"source_label": "youtube_asr:hyram", "audio_packet_id": audio_packet_id}
        ],
    }
    path = tmp_path / "asr_smoke_manifest.json"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _write_audit_manifest(tmp_path: Path, *, smoke_manifest_path: Path, smoke_outputs) -> Path:
    manifest = {
        "audit_id": "asr_cleaning_periodic_audit_fixture",
        "smoke_manifest": str(smoke_manifest_path),
        "lane_a_outputs": {
            "ecr_source_side_receipts": smoke_outputs["ecr_source_side_receipts"],
            "cleaning_packet": smoke_outputs["cleaning_packet"],
            "smoke_summary": smoke_outputs["smoke_summary"],
        },
    }
    path = tmp_path / "asr_audit_manifest.json"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# -- Smoke (acceptance 1 + 2) ------------------------------------------------


def test_asr_smoke_builds_receipt_clears_profile_and_derived_record_handle(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    audio_packet_id = _write_audio_packet_with_transcript(data_root)
    smoke_manifest_path = _write_smoke_manifest(tmp_path, audio_packet_id)

    outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
        data_root=data_root,
    )

    ecr_receipts = _load_json(Path(outputs["ecr_source_side_receipts"]))
    cleaning_packet = CleaningPacket.model_validate(_load_json(Path(outputs["cleaning_packet"])))
    summary = _load_json(Path(outputs["smoke_summary"]))

    assert summary["counts"]["youtube_asr_sources"] == 1
    assert summary["counts"]["ecr_receipts"] == 1
    assert summary["counts"]["cleaning_handles"] == 1
    assert summary["findings"] == []

    # The clears-profile mirrors the #401 caption profile: identity + inspectability clear; timing
    # + source_visibility are HONEST non-clearing residuals (audio has no cutoff class, no archive
    # comparison). Pinning the two False values is the anti-fake-success guard.
    assert len(ecr_receipts["receipts"]) == 1
    receipt = ecr_receipts["receipts"][0]
    assert receipt["source_label"] == "youtube_asr:hyram"
    assert receipt["clears"] == {
        "identity": True,
        "inspectability": True,
        "timing": False,
        "source_visibility": False,
    }

    # Exactly one derived_record-anchored handle keyed to the AUDIO packet, no projection_ref.
    assert len(cleaning_packet.handles) == 1
    handle = cleaning_packet.handles[0]
    assert handle.source_family == "youtube"
    assert handle.source_surface == "youtube_audio"
    assert handle.projection_ref is None
    assert handle.raw_anchor.anchor_kind == "derived_record"
    assert handle.raw_anchor.packet_id == audio_packet_id
    assert handle.raw_anchor.hash_basis == "derived_record_bytes"
    assert handle.raw_anchor.derived_record_ref is not None
    assert handle.raw_anchor.derived_record_ref.lane == "transcript_asr"
    assert handle.ecr_ref is not None
    assert handle.ecr_ref.packet_id == audio_packet_id

    # sha256 in the handle matches the actual lake record bytes (so the audit can re-verify).
    record_dir = _record_dir(data_root, audio_packet_id)
    record_file = next(record_dir.iterdir())
    assert handle.raw_anchor.sha256 == hashlib.sha256(record_file.read_bytes()).hexdigest()
    assert handle.raw_anchor.derived_record_ref.record_id == record_file.name


# -- Fail-closed selection (acceptance 6) ------------------------------------


def test_asr_smoke_raises_on_zero_transcribed_records(tmp_path: Path) -> None:
    # A no_speech record is NOT 'transcribed' -> zero selectable records -> fail closed.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    audio_packet_id = _write_audio_packet_with_transcript(
        data_root, transcribe_fn=lambda p: ("no_speech", [], _MODEL_INFO)
    )
    smoke_manifest_path = _write_smoke_manifest(tmp_path, audio_packet_id)

    with pytest.raises(ValueError, match="exactly one transcribed"):
        run_capture_ecr_cleaning_smoke(
            smoke_manifest_path=smoke_manifest_path,
            output_dir=tmp_path / "smoke_outputs",
            data_root=data_root,
        )


def test_asr_smoke_raises_on_multiple_transcribed_records(tmp_path: Path) -> None:
    # Two distinct transcribed records under the same audio packet -> ambiguous -> fail closed.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    audio_packet_id = _write_audio_packet_with_transcript(data_root)
    # Append a SECOND transcribed record by hand (distinct record_id, same lane).
    second = {
        "video_id": "abcdefghijk",
        "platform": "youtube",
        "posture": "transcribed",
        "cue_count": 1,
        "cues": [{"start_ms": 0, "end_ms": 10, "text": "second"}],
        "provenance": {"source_packet_id": audio_packet_id},
    }
    data_root.append_record(
        subtree="derived",
        raw_anchor=audio_packet_id,
        lane="transcript_asr",
        record_id="asr_small__secondrecord00",
        data=(json.dumps(second) + "\n").encode("utf-8"),
    )
    smoke_manifest_path = _write_smoke_manifest(tmp_path, audio_packet_id)

    with pytest.raises(ValueError, match="exactly one transcribed"):
        run_capture_ecr_cleaning_smoke(
            smoke_manifest_path=smoke_manifest_path,
            output_dir=tmp_path / "smoke_outputs",
            data_root=data_root,
        )


def test_asr_smoke_fails_closed_without_data_root(tmp_path: Path) -> None:
    # A youtube_asr entry with no injected lake must raise (no silent skip).
    smoke_manifest_path = _write_smoke_manifest(tmp_path, "01ASRAUDIOPACKET00000000AB")
    with pytest.raises(ValueError, match="requires lake read access"):
        run_capture_ecr_cleaning_smoke(
            smoke_manifest_path=smoke_manifest_path,
            output_dir=tmp_path / "smoke_outputs",
            data_root=None,
        )


def test_derived_record_anchor_clears_projection_less_youtube_coverage() -> None:
    # The projection-less youtube adapter accepts a derived_record anchor with no anchor_value and
    # no finding (the read-side integrity is checked separately by _verify_derived_record_anchor).
    from runners import run_cleaning_spine_periodic_audit as audit_runner

    audit_runner._validate_source_family_adapter_contract()
    findings: list[dict] = []
    audit_runner._verify_source_family_anchor_adapter_coverage(
        handle_id="youtube_asr:fixture",
        source_family="youtube",
        raw_anchor={"packet_id": "01ASRAUDIOPACKET00000000AB", "anchor_kind": "derived_record"},
        findings=findings,
        lane="lane_a_existing_package",
    )
    assert findings == []


# -- Full-path audit (acceptance 3) ------------------------------------------


def test_asr_audit_resolves_and_rehashes_to_pass(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    audio_packet_id = _write_audio_packet_with_transcript(data_root)
    smoke_manifest_path = _write_smoke_manifest(tmp_path, audio_packet_id)
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
        data_root=data_root,
    )
    audit_manifest_path = _write_audit_manifest(
        tmp_path, smoke_manifest_path=smoke_manifest_path, smoke_outputs=smoke_outputs
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
        data_root=data_root,
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "pass", report["findings"]
    assert report["counts"]["source_entries"] == 1
    assert report["lane_statuses"]["capture_preflight"] == "pass"
    assert report["lane_statuses"]["lane_a_existing_package"] == "pass"
    assert report["lane_statuses"]["lane_b_projection_breakpoint"] == "pass"
    assert report["lane_statuses"]["lane_b_cleaning_breakpoint"] == "pass"
    # No derived-record finding of any kind on a clean run.
    assert not any(
        finding["code"].startswith("cleaning_derived_record_anchor_")
        for finding in report["findings"]
    )


# -- Tamper (acceptance 4) — the proof the audit actually verifies ----------


def _run_audit(tmp_path: Path, data_root, *, audit_data_root) -> dict:
    audio_packet_id = _write_audio_packet_with_transcript(data_root)
    smoke_manifest_path = _write_smoke_manifest(tmp_path, audio_packet_id)
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
        data_root=data_root,
    )
    audit_manifest_path = _write_audit_manifest(
        tmp_path, smoke_manifest_path=smoke_manifest_path, smoke_outputs=smoke_outputs
    )
    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
        data_root=audit_data_root,
    )
    return _load_json(Path(audit_outputs["audit_report_json"]))


def test_asr_audit_flags_hash_mismatch_when_record_bytes_mutated(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    audio_packet_id = _write_audio_packet_with_transcript(data_root)
    smoke_manifest_path = _write_smoke_manifest(tmp_path, audio_packet_id)
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
        data_root=data_root,
    )
    # Tamper: mutate the ACTUAL transcript record bytes in the lake AFTER the handle is stitched.
    record_dir = _record_dir(data_root, audio_packet_id)
    record_file = next(record_dir.iterdir())
    record_file.write_text(
        record_file.read_text(encoding="utf-8") + "\n// tampered\n", encoding="utf-8"
    )
    audit_manifest_path = _write_audit_manifest(
        tmp_path, smoke_manifest_path=smoke_manifest_path, smoke_outputs=smoke_outputs
    )

    report = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
        data_root=data_root,
    )
    report = _load_json(Path(report["audit_report_json"]))

    assert report["overall_status"] == "fail"
    assert any(
        finding["code"] == "cleaning_derived_record_anchor_hash_mismatch"
        for finding in report["findings"]
    )


def test_asr_audit_flags_unresolved_when_record_removed(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    audio_packet_id = _write_audio_packet_with_transcript(data_root)
    smoke_manifest_path = _write_smoke_manifest(tmp_path, audio_packet_id)
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
        data_root=data_root,
    )
    # Tamper: remove the transcript record (a rename/delete) so the path no longer resolves.
    record_dir = _record_dir(data_root, audio_packet_id)
    next(record_dir.iterdir()).unlink()
    audit_manifest_path = _write_audit_manifest(
        tmp_path, smoke_manifest_path=smoke_manifest_path, smoke_outputs=smoke_outputs
    )

    report = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
        data_root=data_root,
    )
    report = _load_json(Path(report["audit_report_json"]))

    assert report["overall_status"] == "fail"
    assert any(
        finding["code"] == "cleaning_derived_record_anchor_unresolved"
        for finding in report["findings"]
    )


def test_asr_audit_flags_lake_unavailable_when_no_data_root(tmp_path: Path) -> None:
    # A CleaningPacket containing a derived_record handle, audited with data_root=None, must emit
    # the blocking lake-unavailable finding AND not pass (proves it is not silently skipped).
    audio_packet_id = "01ASRAUDIOPACKET00000000AB"
    handle = CleaningInputHandle(
        handle_id=f"youtube_asr:fixture:{audio_packet_id}:asr_rec",
        source_family="youtube",
        source_surface="youtube_audio",
        raw_anchor=CleaningRawAnchor(
            packet_id=audio_packet_id,
            sha256="0" * 64,
            hash_basis="derived_record_bytes",
            anchor_kind="derived_record",
            derived_record_ref=CleaningDerivedRecordRef(
                lane="transcript_asr", record_id="asr_small__deadbeefdeadbeef"
            ),
        ),
        ecr_ref=CleaningEcrRef(
            packet_id=audio_packet_id,
            ref_id=f"ecr:{audio_packet_id}:source_side_postures",
        ),
    )
    findings: list[dict] = []
    packet_index = {audio_packet_id: {"packet": None, "packet_dir": None}}
    from runners import run_cleaning_spine_periodic_audit as audit_runner

    audit_runner._verify_cleaning_raw_anchor(
        handle_id=handle.handle_id,
        raw_anchor=handle.raw_anchor.model_dump(mode="json"),
        packet_index=packet_index,
        findings=findings,
        lane="lane_a_existing_package",
        data_root=None,
    )

    lake_findings = [
        finding
        for finding in findings
        if finding["code"] == "cleaning_derived_record_anchor_lake_unavailable"
    ]
    assert len(lake_findings) == 1
    assert lake_findings[0]["severity"] == "blocker"
    # A blocking finding makes the lane (and overall status) fail, not pass.
    assert audit_runner._lane_status("lane_a_existing_package", findings) == "fail"


def test_asr_audit_malformed_segment_is_unreadable_finding_not_crash(tmp_path: Path) -> None:
    # A malformed lane/record_id (caught by the lake's segment grammar at resolution) must surface
    # as a fail-closed `..._unreadable` finding, never a mid-audit crash.
    from runners import run_cleaning_spine_periodic_audit as audit_runner

    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    audio_packet_id = _write_audio_packet_with_transcript(data_root)
    raw_anchor = {
        "packet_id": audio_packet_id,
        "slice_id": None,
        "file_id": None,
        "relative_packet_path": None,
        "sha256": "0" * 64,
        "hash_basis": "derived_record_bytes",
        "anchor_kind": "derived_record",
        "anchor_value": None,
        "json_pointer": None,
        "derived_record_ref": {
            "subtree": "derived",
            "lane": "transcript_asr",
            "record_id": "../escape",
        },
    }
    findings: list[dict] = []
    audit_runner._verify_cleaning_raw_anchor(
        handle_id="youtube_asr:fixture",
        raw_anchor=raw_anchor,
        packet_index={audio_packet_id: {"packet": None, "packet_dir": None}},
        findings=findings,
        lane="lane_a_existing_package",
        data_root=data_root,
    )
    assert any(
        finding["code"] == "cleaning_derived_record_anchor_unreadable" for finding in findings
    )
