from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot
from runners.run_tiktok_batch_coverage import main as tiktok_coverage_main
from source_capture.tiktok.batch_coverage import (
    TIKTOK_BATCH_COVERAGE_SCHEMA_VERSION,
    build_tiktok_batch_coverage_from_payload,
    build_tiktok_batch_coverage_from_packet_directory,
    tiktok_batch_coverage_json_text,
)
from source_capture.tiktok.batch_packet import write_tiktok_batch_packet
from test_tiktok_batch_admission import PROFILE_URL, _cadence_payload, _grid_payload


def test_tiktok_batch_coverage_from_packet_directory_excludes_raw_text(tmp_path: Path) -> None:
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

    coverage = build_tiktok_batch_coverage_from_packet_directory(packet_dir)
    coverage_text = tiktok_batch_coverage_json_text(coverage)

    assert coverage["coverage_schema_version"] == TIKTOK_BATCH_COVERAGE_SCHEMA_VERSION
    assert coverage["batch_summary"]["video_count"] == 2
    assert coverage["coverage_rollup"]["video_count"] == 2
    assert coverage["coverage_rollup"]["captured_comment_count"] == 2
    assert coverage["coverage_rollup"]["comment_envelope_total"] == 13
    assert coverage["coverage_rollup"]["videos_with_transcript_text"] == 1
    assert coverage["coverage_rollup"]["videos_with_disclosure_signal"] == 2
    assert coverage["loss_ledger"]["omitted_comment_text_row_count"] == 2
    assert coverage["loss_ledger"]["omitted_subtitle_cue_text_row_count"] == 2

    first = coverage["video_rows"][0]
    assert first["comments"]["captured_comment_count"] == 1
    assert first["comments"]["intent_term_counts"]["need"] == 1
    assert first["subtitles"]["subtitle_sources"] == ["ASR"]
    assert first["subtitles"]["has_transcript_text"] is True
    assert "#burberrypartner" in first["source_text_signals"]["disclosure_source_text_signals"]
    assert first["source_text_signals"]["description_sha256"]

    assert "I need to smell this" not in coverage_text
    assert "where can I buy it?" not in coverage_text
    assert "This fragrance" not in coverage_text
    assert "smells like tea" not in coverage_text
    assert "Burberry Goddess with" not in coverage_text
    assert "msToken" not in coverage_text
    assert "X-Bogus" not in coverage_text
    assert "tiktokcdn" not in coverage_text


def test_tiktok_batch_coverage_cli_reads_data_lake_packet_id(tmp_path: Path, capsys, monkeypatch) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
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
    output = tmp_path / "coverage.json"

    resolve_calls: list[object] = []

    def fake_resolve(cls, explicit=None):
        resolve_calls.append(explicit)
        return root

    monkeypatch.setattr(DataLakeRoot, "resolve", classmethod(fake_resolve))


    code = tiktok_coverage_main(
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
    coverage = json.loads(output.read_text(encoding="utf-8"))
    assert coverage["packet_id"] == packet_id
    assert coverage["raw_ref"]["packet_id"] == packet_id
    assert coverage["coverage_rollup"]["video_count"] == 2
    assert coverage["video_rows"][1]["subtitles"]["posture"] == "no_subtitleInfos_present"
    assert resolve_calls == [str(root.path)]


def test_tiktok_batch_coverage_cli_prints_stdout_without_raw_text(tmp_path: Path, capsys) -> None:
    packet_dir = tmp_path / "batch_packet"
    write_tiktok_batch_packet(
        creator_handle="funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=_grid_payload(),
        cadence_result_jsons=[_cadence_payload()],
        output_directory=packet_dir,
        decision_question="admit TikTok creator batch",
    )

    code = tiktok_coverage_main(["--packet", str(packet_dir)])

    captured = capsys.readouterr()
    assert code == 0
    coverage = json.loads(captured.out)
    assert coverage["coverage_rollup"]["comment_envelope_total"] == 13
    assert "I need to smell this" not in captured.out
    assert "This fragrance" not in captured.out


def test_tiktok_batch_coverage_rejects_non_tiktok_payload() -> None:
    with pytest.raises(ValueError, match="not a TikTok parsed-batch admission payload"):
        build_tiktok_batch_coverage_from_payload(
            {"platform": "instagram", "source_surface": "ig_reels_grid", "videos": []}
        )


def test_tiktok_batch_coverage_has_no_hidden_network_browser_or_proxy_imports() -> None:
    harness_root = Path(__file__).resolve().parents[2]
    checked_paths = [
        harness_root / "runners" / "run_tiktok_batch_coverage.py",
        harness_root / "source_capture" / "tiktok" / "batch_coverage.py",
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
