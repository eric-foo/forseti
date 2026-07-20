from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from cleaning.legacy import cleaning_handles_from_legacy_rows
from data_lake.root import DataLakeRoot
from runners.run_tiktok_batch_projection import main as tiktok_projection_main
from source_capture.tiktok.batch_coverage import (
    build_tiktok_batch_coverage_from_packet_directory,
    build_tiktok_batch_coverage_from_payload,
)
from source_capture.tiktok.batch_packet import (
    TIKTOK_BATCH_CAPTURE_JSON_NAME,
    TIKTOK_BATCH_CAPTURE_SURFACE,
    write_tiktok_batch_packet,
)
from source_capture.tiktok.batch_projection import (
    TIKTOK_BATCH_PROJECTION_CERTIFICATION,
    TIKTOK_BATCH_PROJECTION_METHOD,
    build_tiktok_batch_projection_from_coverage,
    build_tiktok_batch_projection_from_packet_directory,
    tiktok_batch_projection_json_text,
)
from test_tiktok_batch_admission import PROFILE_URL, _cadence_payload, _grid_payload


def test_tiktok_batch_projection_from_packet_directory_anchors_rows_and_excludes_raw_text(
    tmp_path: Path,
) -> None:
    packet_dir = _write_fixture_packet(tmp_path)

    projection = build_tiktok_batch_projection_from_packet_directory(packet_dir)
    projection_text = tiktok_batch_projection_json_text(projection)

    assert projection.projection_method == TIKTOK_BATCH_PROJECTION_METHOD
    assert projection.certification == TIKTOK_BATCH_PROJECTION_CERTIFICATION
    assert projection.packet_id
    assert len(projection.rows) == 2
    assert projection.loss_ledger.preserved_video_rows == 2
    assert projection.loss_ledger.omitted_comment_text_row_count == 2
    assert projection.loss_ledger.omitted_subtitle_cue_text_row_count == 2
    assert projection.loss_ledger.row_residual_counts == {
        "comment_envelope_exceeds_captured_rows": 2,
        "source_native_webvtt_not_captured": 1,
        "transcript_text_not_available": 1,
    }

    first = projection.rows[0]
    assert first.row_id == f"{projection.packet_id}:videos/0"
    assert first.raw_ref.packet_id == projection.packet_id
    assert first.raw_ref.slice_id == "videos/0"
    assert first.raw_anchor.anchor_kind == "json_pointer"
    assert first.raw_anchor.json_pointer == "/videos/0"
    assert first.raw_anchor.relative_packet_path.endswith(TIKTOK_BATCH_CAPTURE_JSON_NAME)
    assert first.raw_video_index == 0
    assert first.captured_comment_count == 1
    assert first.comment_envelope_total == 10
    assert first.comment_intent_term_counts["need"] == 1
    assert first.subtitle_source_count == 1
    assert first.has_transcript_text is True
    assert first.has_disclosure_signal is True
    assert first.disclosure_signal_count == 1
    assert first.description_sha256

    assert "I need to smell this" not in projection_text
    assert "where can I buy it?" not in projection_text
    assert "This fragrance" not in projection_text
    assert "smells like tea" not in projection_text
    assert "Burberry Goddess with" not in projection_text
    assert "#burberrypartner" not in projection_text
    assert "msToken" not in projection_text
    assert "X-Bogus" not in projection_text
    assert "tiktokcdn" not in projection_text


def test_tiktok_batch_projection_pins_materially_different_raw_body_join_shape(
    tmp_path: Path,
) -> None:
    projection = build_tiktok_batch_projection_from_packet_directory(_write_fixture_packet(tmp_path))

    assert len(projection.rows) == 2
    assert {row.raw_ref.packet_id for row in projection.rows} == {projection.packet_id}
    assert [row.raw_ref.slice_id for row in projection.rows] == ["videos/0", "videos/1"]
    assert {row.raw_anchor.relative_packet_path for row in projection.rows} == {
        projection.rows[0].raw_anchor.relative_packet_path
    }
    assert [row.raw_anchor.json_pointer for row in projection.rows] == ["/videos/0", "/videos/1"]
    assert projection.binding_map == []
    assert "not_persisted_derived_projection_lane" in projection.non_claims

def test_tiktok_batch_projection_uses_raw_video_index_when_coverage_rows_have_gap(
    tmp_path: Path,
) -> None:
    packet_dir = _write_fixture_packet(tmp_path)
    payload_path = next(packet_dir.rglob(f"*{TIKTOK_BATCH_CAPTURE_JSON_NAME}"))
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    payload["videos"].insert(1, {})

    coverage = build_tiktok_batch_coverage_from_payload(
        payload,
        packet_id="packet_with_gap",
        raw_ref={
            "packet_id": "packet_with_gap",
            "file_id": "file_01",
            "relative_packet_path": "raw/01_tiktok_batch_capture.json",
            "sha256": "a" * 64,
            "hash_basis": "raw_stored_bytes",
        },
    )

    assert [row["raw_video_index"] for row in coverage["video_rows"]] == [0, 2]
    projection = build_tiktok_batch_projection_from_coverage(coverage)

    assert [row.raw_anchor.json_pointer for row in projection.rows] == ["/videos/0", "/videos/2"]
    assert [row.raw_ref.slice_id for row in projection.rows] == ["videos/0", "videos/2"]
    assert projection.loss_ledger.structure_preserved is False
    assert "raw_video_index_gap_or_reorder" in projection.residuals


def test_tiktok_batch_projection_rejects_coverage_without_raw_video_index(
    tmp_path: Path,
) -> None:
    coverage = build_tiktok_batch_coverage_from_packet_directory(_write_fixture_packet(tmp_path))
    del coverage["video_rows"][0]["raw_video_index"]

    with pytest.raises(ValueError, match="raw_video_index"):
        build_tiktok_batch_projection_from_coverage(coverage)


def test_tiktok_batch_projection_rejects_coverage_without_raw_ref(tmp_path: Path) -> None:
    coverage = build_tiktok_batch_coverage_from_packet_directory(_write_fixture_packet(tmp_path))
    coverage["raw_ref"] = {}

    with pytest.raises(ValueError, match="raw_ref.packet_id"):
        build_tiktok_batch_projection_from_coverage(coverage)


def test_tiktok_analytical_rows_adapt_to_cleaning_source_anchors(tmp_path: Path) -> None:
    projection = build_tiktok_batch_projection_from_packet_directory(_write_fixture_packet(tmp_path))

    handles = cleaning_handles_from_legacy_rows(
        source_family="tiktok",
        source_surface=TIKTOK_BATCH_CAPTURE_SURFACE,
        packet_id=projection.packet_id,
        rows=projection.rows,
        handle_id_prefix="tiktok_analytical",
    )

    assert len(handles) == len(projection.rows)
    first = handles[0]
    assert first.source_anchor.packet_id == projection.packet_id
    assert first.source_anchor.slice_id == "videos/0"
    assert first.source_anchor.anchor_kind == "json_pointer"
    assert first.source_anchor.json_pointer == "/videos/0"
    assert first.source_row_id == projection.rows[0].row_id


def test_tiktok_batch_projection_cli_reads_data_lake_packet_id(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _, message = write_tiktok_batch_packet(
        creator_handle="funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=_grid_payload(),
        cadence_result_jsons=[_cadence_payload()],
        data_root=root,
        decision_question="admit TikTok creator batch",
        batch_label="funmi_n2_fixture",
        capture_timestamp="2026-06-30T17:02:46Z",
    )
    packet_id = Path(message).name
    output = tmp_path / "projection.json"

    resolve_calls: list[object] = []

    def fake_resolve(cls, explicit=None):
        resolve_calls.append(explicit)
        return root

    monkeypatch.setattr(DataLakeRoot, "resolve", classmethod(fake_resolve))

    code = tiktok_projection_main(
        [
            "--packet-id",
            packet_id,
            "--data-root",
            str(root.path),
            "--output",
            str(output),
        ]
    )

    captured = capsys.readouterr()
    assert code == 0
    assert str(output) in captured.out
    projection = json.loads(output.read_text(encoding="utf-8"))
    assert projection["packet_id"] == packet_id
    assert projection["rows"][0]["raw_anchor"]["json_pointer"] == "/videos/0"
    assert projection["rows"][1]["subtitle_posture"] == "no_subtitleInfos_present"
    assert resolve_calls == [str(root.path)]


def test_tiktok_batch_projection_cli_prints_stdout_without_raw_text(
    tmp_path: Path,
    capsys,
) -> None:
    packet_dir = _write_fixture_packet(tmp_path)

    code = tiktok_projection_main(["--packet", str(packet_dir)])

    captured = capsys.readouterr()
    assert code == 0
    projection = json.loads(captured.out)
    assert projection["loss_ledger"]["preserved_video_rows"] == 2
    assert projection["rows"][0]["raw_anchor"]["json_pointer"] == "/videos/0"
    assert "I need to smell this" not in captured.out
    assert "This fragrance" not in captured.out
    assert "#burberrypartner" not in captured.out


def test_tiktok_batch_projection_has_no_hidden_network_browser_or_proxy_imports() -> None:
    harness_root = Path(__file__).resolve().parents[2]
    checked_paths = [
        harness_root / "runners" / "run_tiktok_batch_projection.py",
        harness_root / "source_capture" / "tiktok" / "batch_projection.py",
    ]
    forbidden = {
        "aiohttp",
        "anthropic",
        "browser_cookie3",
        "httpx",
        "langchain",
        "litellm",
        "openai",
        "patchright",
        "playwright",
        "requests",
        "scrapy",
        "selenium",
        "socket",
        "source_capture.proxy_profiles",
        "webbrowser",
    }
    bad_imports_by_path: dict[str, list[str]] = {}
    for path in checked_paths:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imported_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)
        bad_imports = sorted(
            module
            for module in imported_modules
            for forbidden_module in forbidden
            if module == forbidden_module or module.startswith(f"{forbidden_module}.")
        )
        if bad_imports:
            bad_imports_by_path[path.name] = bad_imports
    assert bad_imports_by_path == {}


def _write_fixture_packet(tmp_path: Path) -> Path:
    packet_dir = tmp_path / "batch_packet"
    write_tiktok_batch_packet(
        creator_handle="funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=_grid_payload(),
        cadence_result_jsons=[_cadence_payload()],
        output_directory=packet_dir,
        decision_question="admit TikTok creator batch",
        batch_label="funmi_n2_fixture",
        capture_timestamp="2026-06-30T17:02:46Z",
    )
    return packet_dir
