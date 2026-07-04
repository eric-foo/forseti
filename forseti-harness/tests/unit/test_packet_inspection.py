from __future__ import annotations

import hashlib
import json
import shutil
import uuid
from pathlib import Path

import pytest

import source_capture.packet_inspection as inspection_module
from source_capture import known_fact, write_local_source_capture_packet
from source_capture.models import SOURCE_CAPTURE_MANIFEST_VERSION, SourceCapturePacket
from source_capture.packet_inspection import (
    NOT_AVAILABLE_WITHOUT_PER_VERSION_SCHEMA,
    PacketConformanceReport,
    inspect_packet_manifest,
    read_packet_leniently,
)


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"packet_inspection_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def _write_conforming_packet(root: Path) -> Path:
    source_file = root / "source.html"
    source_file.write_text("<html><body>conforming v1 body</body></html>", encoding="utf-8")
    packet_dir = root / "packet"
    write_local_source_capture_packet(
        output_directory=packet_dir,
        input_files=[source_file],
        source_family="web_page",
        source_surface="local_file",
        source_locator=known_fact("https://example.test/source"),
        decision_question="What source body was preserved?",
        capture_context="packet inspection unit test",
        cutoff_posture=known_fact("pre_cutoff"),
    )
    return packet_dir


def _manifest_dict(packet_dir: Path) -> dict:
    return json.loads((packet_dir / "manifest.json").read_text(encoding="utf-8"))


def test_conforming_v1_manifest_reports_conforming(scratch_dir: Path) -> None:
    manifest = _manifest_dict(_write_conforming_packet(scratch_dir))

    report = inspect_packet_manifest(manifest)

    assert isinstance(report, PacketConformanceReport)
    assert report.conforms_to_current_schema is True
    assert report.declared_manifest_version == SOURCE_CAPTURE_MANIFEST_VERSION
    assert report.declares_current_manifest_version is True
    assert report.current_schema_errors == []
    assert report.declared_version_shape_validation is None
    assert isinstance(report.packet, SourceCapturePacket)


def test_missing_hash_basis_reports_nonconforming_current_version(scratch_dir: Path) -> None:
    manifest = _manifest_dict(_write_conforming_packet(scratch_dir))
    del manifest["preserved_files"][0]["hash_basis"]

    report = inspect_packet_manifest(manifest)

    assert report.conforms_to_current_schema is False
    assert report.declares_current_manifest_version is True
    # Declares the current version but fails it -> a corruption signal, not off-version.
    assert report.declared_version_shape_validation is None
    assert report.packet is None
    assert any("hash_basis" in err.loc for err in report.current_schema_errors)


def test_off_version_nonconforming_marks_shape_validation_unavailable(scratch_dir: Path) -> None:
    manifest = _manifest_dict(_write_conforming_packet(scratch_dir))
    manifest["manifest_version"] = "source_capture_packet_manifest_v0"
    del manifest["preserved_files"][0]["hash_basis"]

    report = inspect_packet_manifest(manifest)

    assert report.conforms_to_current_schema is False
    assert report.declared_manifest_version == "source_capture_packet_manifest_v0"
    assert report.declares_current_manifest_version is False
    assert report.declared_version_shape_validation == NOT_AVAILABLE_WITHOUT_PER_VERSION_SCHEMA
    assert report.packet is None


def test_off_version_but_structurally_current_cannot_confirm_declared_shape(scratch_dir: Path) -> None:
    # Honest edge: satisfies the CURRENT schema but claims a non-current version.
    # We confirm current-schema conformance but cannot verify the v0 claim it makes.
    manifest = _manifest_dict(_write_conforming_packet(scratch_dir))
    manifest["manifest_version"] = "source_capture_packet_manifest_v0"

    report = inspect_packet_manifest(manifest)

    assert report.conforms_to_current_schema is True
    assert report.declares_current_manifest_version is False
    assert report.declared_version_shape_validation == NOT_AVAILABLE_WITHOUT_PER_VERSION_SCHEMA


def test_nonconforming_report_never_carries_a_packet(scratch_dir: Path) -> None:
    manifest = _manifest_dict(_write_conforming_packet(scratch_dir))
    del manifest["preserved_files"][0]["hash_basis"]

    report = inspect_packet_manifest(manifest)

    # The distinct-type guard: a non-conforming read must not hand back a usable packet.
    assert report.packet is None
    assert not isinstance(report, SourceCapturePacket)


def test_errors_drop_pydantic_input_so_siblings_do_not_leak(scratch_dir: Path) -> None:
    manifest = _manifest_dict(_write_conforming_packet(scratch_dir))
    sha = manifest["preserved_files"][0]["sha256"]
    del manifest["preserved_files"][0]["hash_basis"]  # missing-required error

    report = inspect_packet_manifest(manifest)

    assert report.conforms_to_current_schema is False
    # pydantic's raw `input` for a missing-field error is the whole parent object;
    # dropping it keeps unrelated sibling fields (e.g. the sha256) out of the report.
    dumped = json.dumps(report.model_dump(mode="json"))
    assert sha not in dumped
    for err in report.current_schema_errors:
        assert set(err.model_dump().keys()) == {"loc", "type", "msg"}


def test_non_validation_error_is_not_swallowed(scratch_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    manifest = _manifest_dict(_write_conforming_packet(scratch_dir))

    class _Boom:
        @staticmethod
        def model_validate(_data: object) -> object:
            raise RuntimeError("probe blew up")

    monkeypatch.setattr(inspection_module, "SourceCapturePacket", _Boom)

    # Only ValidationError is caught; a real bug must surface, not become "non-conforming".
    with pytest.raises(RuntimeError, match="probe blew up"):
        inspect_packet_manifest(manifest)


def test_read_packet_leniently_raises_on_invalid_json(scratch_dir: Path) -> None:
    bad = scratch_dir / "manifest.json"
    bad.write_text("{ not valid json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        read_packet_leniently(bad)


def test_lenient_read_does_not_mutate_the_packet(scratch_dir: Path) -> None:
    packet_dir = _write_conforming_packet(scratch_dir)

    def snapshot() -> dict[str, str]:
        return {
            str(p.relative_to(packet_dir)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(packet_dir.rglob("*"))
            if p.is_file()
        }

    before = snapshot()
    read_packet_leniently(packet_dir / "manifest.json")
    after = snapshot()

    assert before == after
