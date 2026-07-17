from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from runners.run_parfumo_mgt_capture import (
    TARGETED_RENDERED_SLOT,
    TARGETED_RENDERED_SURFACE,
    run_parfumo_targeted_rendered_capture,
)
from runners.run_parfumo_parser_fit_check import (
    ParserFitCheckError,
    check_parfumo_parser_fit,
    run_parfumo_parser_fit_check,
)
from tests.unit.test_parfumo_projection import _LOCATOR, _TARGETED_HTML


def test_parfumo_parser_fit_matches_sample_packet(tmp_path: Path) -> None:
    packet_dir = _write_packet(tmp_path, mode="sample")

    row = check_parfumo_parser_fit(packet_or_manifest_path=packet_dir)
    exit_code, report = run_parfumo_parser_fit_check(packet_paths=[packet_dir])

    assert row["status"] == "match"
    assert exit_code == 0
    assert report["failure_count"] == 0


@pytest.mark.parametrize(
    ("mode", "error_code"),
    [
        ("content", "ineligible_capture_mode"),
        ("raw", "preserved_file_missing_or_ambiguous"),
    ],
)
def test_parfumo_parser_fit_rejects_non_sample_packets(
    tmp_path: Path,
    mode: str,
    error_code: str,
) -> None:
    packet_dir = _write_packet(tmp_path, mode=mode)

    with pytest.raises(ParserFitCheckError) as exc_info:
        check_parfumo_parser_fit(packet_or_manifest_path=packet_dir)

    assert exc_info.value.code == error_code


def test_parfumo_parser_fit_reports_drift(tmp_path: Path) -> None:
    packet_dir = _write_packet(tmp_path, mode="sample")

    def mutate(record):
        record["rows"][0]["source_visible_fields"]["page_title"] = "tampered title"
        return record

    _mutate_json_preserved_file(packet_dir, "content_record.json", mutate)
    row = check_parfumo_parser_fit(packet_or_manifest_path=packet_dir)

    assert row["status"] == "drift"
    assert row["diff_summary"]["changed_top_level_keys"] == ["rows"]


def test_parfumo_parser_fit_rejects_metadata_parser_version(tmp_path: Path) -> None:
    packet_dir = _write_packet(tmp_path, mode="sample")

    def mutate(metadata):
        metadata["parser_version"] = "parfumo_targeted_parser_v0"
        return metadata

    _mutate_json_preserved_file(packet_dir, "content_capture_metadata.json", mutate)
    with pytest.raises(ParserFitCheckError) as exc_info:
        check_parfumo_parser_fit(packet_or_manifest_path=packet_dir)

    assert exc_info.value.code == "parser_version_mismatch"


def test_parfumo_parser_fit_rejects_bad_projector_input_hash(tmp_path: Path) -> None:
    packet_dir = _write_packet(tmp_path, mode="sample")

    def mutate(metadata):
        rendered = next(item for item in metadata["inputs"] if item["role"] == "rendered_dom")
        rendered["sha256"] = "0" * 64
        return metadata

    _mutate_json_preserved_file(packet_dir, "content_capture_metadata.json", mutate)
    with pytest.raises(ParserFitCheckError) as exc_info:
        check_parfumo_parser_fit(packet_or_manifest_path=packet_dir)

    assert exc_info.value.code == "projector_input_hash_mismatch"


def test_parfumo_parser_fit_rejects_source_url_mismatch(tmp_path: Path) -> None:
    packet_dir = _write_packet(tmp_path, mode="sample")

    def mutate(record):
        record["source_url"] = "https://www.parfumo.com/Perfumes/Other/Other"
        return record

    _mutate_json_preserved_file(packet_dir, "content_record.json", mutate)
    with pytest.raises(ParserFitCheckError) as exc_info:
        check_parfumo_parser_fit(packet_or_manifest_path=packet_dir)

    assert exc_info.value.code == "source_url_mismatch"


def test_parfumo_parser_fit_rejects_malformed_content_record(tmp_path: Path) -> None:
    packet_dir = _write_packet(tmp_path, mode="sample")
    _replace_preserved_file(packet_dir, "content_record.json", b"[]\n")

    with pytest.raises(ParserFitCheckError) as exc_info:
        check_parfumo_parser_fit(packet_or_manifest_path=packet_dir)

    assert exc_info.value.code == "content_record_shape"


def _write_packet(tmp_path: Path, *, mode: str) -> Path:
    artifact_dir = tmp_path / "artifacts"
    artifact_dir.mkdir()
    rendered_dom = artifact_dir / "rendered_dom.html"
    visible_text = artifact_dir / "visible_text.txt"
    route_receipt = artifact_dir / "route_receipt.json"
    screenshot = artifact_dir / "viewport.png"
    rendered_dom.write_text(_TARGETED_HTML, encoding="utf-8")
    visible_text.write_text(
        "Baccarat Rouge 540 Eau de Parfum\nReviews 369\nStatements 1390\n",
        encoding="utf-8",
    )
    route_receipt.write_text(
        json.dumps(
            {
                "route": "chrome_extension_user_visible_rendered_session",
                "source_surface": TARGETED_RENDERED_SURFACE,
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    screenshot.write_bytes(b"png fixture bytes")

    exit_code, message = run_parfumo_targeted_rendered_capture(
        url=_LOCATOR,
        output_root=tmp_path / "out",
        rendered_dom_path=rendered_dom,
        visible_text_path=visible_text,
        route_receipt_path=route_receipt,
        screenshot_path=screenshot,
        capture_artifact_mode=mode,
    )
    assert exit_code == 0
    summary = json.loads(Path(message).read_text(encoding="utf-8"))
    return Path(summary["packet_roles"][TARGETED_RENDERED_SLOT]["packet_path"])


def _mutate_json_preserved_file(packet_dir: Path, suffix: str, mutator) -> None:
    path = _preserved_path(packet_dir, suffix)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    updated = mutator(loaded)
    _replace_preserved_file(
        packet_dir,
        suffix,
        (json.dumps(updated, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"),
    )


def _replace_preserved_file(packet_dir: Path, suffix: str, content: bytes) -> None:
    path = _preserved_path(packet_dir, suffix)
    path.write_bytes(content)
    manifest_path = packet_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    item = next(
        entry
        for entry in manifest["preserved_files"]
        if entry["relative_packet_path"].replace("\\", "/").endswith(suffix)
    )
    item["sha256"] = hashlib.sha256(content).hexdigest()
    item["size_bytes"] = len(content)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _preserved_path(packet_dir: Path, suffix: str) -> Path:
    manifest = json.loads((packet_dir / "manifest.json").read_text(encoding="utf-8"))
    item = next(
        entry
        for entry in manifest["preserved_files"]
        if entry["relative_packet_path"].replace("\\", "/").endswith(suffix)
    )
    return packet_dir / item["relative_packet_path"]
