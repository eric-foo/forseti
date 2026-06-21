from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from cleaning.models import CleaningPacket
from runners import run_capture_ecr_cleaning_smoke as smoke_runner
from runners.run_capture_ecr_cleaning_smoke import (
    _old_reddit_anchor_pattern,
    run_capture_ecr_cleaning_smoke,
)
from source_capture.models import (
    CaptureModeCategory,
    PacketTiming,
    PreservedFile,
    ReceiptMetadata,
    SourceCapturePacket,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.reddit_consolidation import consolidate_reddit_packet
from source_capture.retail_pdp_projection import write_retail_pdp_projection
from source_capture.writer import write_local_source_capture_packet


def test_runner_writes_ecr_receipts_and_cleaning_packet_for_retail_and_reddit(
    tmp_path: Path,
) -> None:
    retail_packet_dir = _write_retail_packet_dir(tmp_path)
    retail_projection_path = tmp_path / "retail_projection" / "retail_pdp_projection.json"
    retail_projection = write_retail_pdp_projection(
        packet_directory=retail_packet_dir,
        output_path=retail_projection_path,
    )
    reddit_packet_dir = _write_reddit_packet_dir(tmp_path, NORMAL_THREAD_HTML)
    reddit_consolidation = consolidate_reddit_packet(
        packet_or_manifest_path=reddit_packet_dir,
        output_directory=tmp_path / "reddit_consolidation",
    )
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        retail_packet_dir=retail_packet_dir,
        retail_projection_path=retail_projection_path,
        reddit_packet_dir=reddit_packet_dir,
        reddit_consolidation_path=Path(reddit_consolidation["json_path"]),
    )

    outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )

    ecr_receipts = _load_json(Path(outputs["ecr_source_side_receipts"]))
    cleaning_packet = CleaningPacket.model_validate(
        _load_json(Path(outputs["cleaning_packet"]))
    )
    summary = _load_json(Path(outputs["smoke_summary"]))

    assert summary["counts"] == {
        "retail_sources": 1,
        "reddit_sources": 1,
        "ecr_receipts": 2,
        "cleaning_handles": len(cleaning_packet.handles),
        "cleaning_transform_entries": 0,
    }
    assert summary["cleaning_transform_smoke_enabled"] is False
    assert {receipt["source_label"] for receipt in ecr_receipts["receipts"]} == {
        "retail:sephora",
        "reddit:1",
    }
    for receipt in ecr_receipts["receipts"]:
        assert receipt["ref_id"].endswith(":source_side_postures")
        assert set(receipt["postures"]) == {
            "identity",
            "inspectability",
            "timing",
            "source_visibility",
        }
        assert all(receipt["postures"][kind] for kind in receipt["postures"])

    retail_handles = [
        handle
        for handle in cleaning_packet.handles
        if handle.handle_id.startswith("retail:sephora:")
    ]
    reddit_handles = [
        handle
        for handle in cleaning_packet.handles
        if handle.handle_id.startswith("reddit:1:")
    ]
    assert len(retail_handles) == len(retail_projection.rows)
    assert len(reddit_handles) == 3
    assert all(handle.projection_ref is not None for handle in retail_handles)
    assert all(handle.projection_ref is None for handle in reddit_handles)
    assert all(handle.ecr_ref is not None for handle in cleaning_packet.handles)
    assert all(
        handle.ecr_ref.packet_id == handle.raw_anchor.packet_id
        for handle in cleaning_packet.handles
        if handle.ecr_ref is not None
    )
    assert all(
        handle.raw_anchor.anchor_kind == "text_pattern" for handle in reddit_handles
    )
    retail_source = next(
        source for source in summary["sources"] if source["source_label"] == "retail:sephora"
    )
    assert retail_source["structure_preserved"] is True
    assert retail_source["capture_validity_supported"] is True
    assert retail_source["capture_validity_reasons"] == []
    assert not any(
        finding["code"] in {"retail_capture_validity_not_supported", "retail_row_anchor_unverified"}
        for finding in summary["findings"]
    )
    assert "not_capture_execution" in summary["non_claims"]


def test_retail_capture_validity_flags_error_page_without_blocking(tmp_path: Path) -> None:
    retail_packet_dir = _write_retail_packet_dir(
        tmp_path,
        html="""
        <html><head><title>Page Not Found</title></head>
        <body>Sorry! We couldn't find that page.</body></html>
        """,
        visible_text="",
    )
    retail_projection_path = tmp_path / "retail_projection" / "retail_pdp_projection.json"
    write_retail_pdp_projection(
        packet_directory=retail_packet_dir,
        output_path=retail_projection_path,
    )
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        retail_packet_dir=retail_packet_dir,
        retail_projection_path=retail_projection_path,
    )

    outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )

    cleaning_packet = CleaningPacket.model_validate(
        _load_json(Path(outputs["cleaning_packet"]))
    )
    ecr_receipts = _load_json(Path(outputs["ecr_source_side_receipts"]))
    summary = _load_json(Path(outputs["smoke_summary"]))

    assert cleaning_packet.handles
    retail_source = next(source for source in summary["sources"] if source["source_label"] == "retail:sephora")
    assert retail_source["capture_validity_supported"] is False
    assert "rendered_dom_error_or_block_page_marker" in retail_source["capture_validity_reasons"]
    assert "tiny_rendered_dom_with_error_marker" in retail_source["capture_validity_reasons"]
    assert len(ecr_receipts["receipts"]) == 1
    assert ecr_receipts["receipts"][0]["packet_id"] == retail_source["packet_id"]
    failed_handles = [
        handle for handle in cleaning_packet.handles if handle.raw_anchor.packet_id == retail_source["packet_id"]
    ]
    assert failed_handles
    assert len(failed_handles) == retail_source["handle_count"]
    assert all(
        "capture_validity_not_supported:rendered_dom_error_or_block_page_marker" in handle.warnings
        for handle in failed_handles
    )
    assert all(
        "inspect_raw_before_retail_use:capture_validity_not_supported" in handle.raw_pull_triggers
        for handle in failed_handles
    )
    assert any(
        finding["code"] == "retail_capture_validity_not_supported"
        and "rendered_dom_error_or_block_page_marker" in finding["reasons"]
        for finding in summary["findings"]
    )


def test_retail_capture_validity_ignores_embedded_recaptcha_on_valid_pdp(
    tmp_path: Path,
) -> None:
    retail_packet_dir = _write_retail_packet_dir(
        tmp_path,
        html=_retail_html()
        + '<script src="https://www.google.com/recaptcha/api.js"></script>'
        + '<iframe title="recaptcha challenge expires in two minutes"></iframe>',
    )
    retail_projection_path = tmp_path / "retail_projection" / "retail_pdp_projection.json"
    write_retail_pdp_projection(
        packet_directory=retail_packet_dir,
        output_path=retail_projection_path,
    )
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        retail_packet_dir=retail_packet_dir,
        retail_projection_path=retail_projection_path,
    )

    outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )

    summary = _load_json(Path(outputs["smoke_summary"]))
    retail_source = next(source for source in summary["sources"] if source["source_label"] == "retail:sephora")
    assert retail_source["capture_validity_supported"] is True
    assert not any(
        finding["code"] == "retail_capture_validity_not_supported"
        for finding in summary["findings"]
    )

def test_retail_capture_validity_flags_all_null_required_rows(tmp_path: Path) -> None:
    retail_packet_dir = _write_retail_packet_dir(tmp_path)
    retail_projection_path = tmp_path / "retail_projection" / "retail_pdp_projection.json"
    write_retail_pdp_projection(
        packet_directory=retail_packet_dir,
        output_path=retail_projection_path,
    )
    projection = _load_json(retail_projection_path)
    for row in projection["rows"]:
        if row["row_kind"] in {"retail_variant_offer", "retail_review_substrate"}:
            row["source_visible_fields"] = {key: None for key in row["source_visible_fields"]}
    _write_json(retail_projection_path, projection)
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        retail_packet_dir=retail_packet_dir,
        retail_projection_path=retail_projection_path,
    )

    outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )

    summary = _load_json(Path(outputs["smoke_summary"]))
    assert any(
        finding["code"] == "retail_capture_validity_not_supported"
        and "required_retail_rows_all_null" in finding["reasons"]
        for finding in summary["findings"]
    )


def test_retail_missing_text_pattern_anchor_is_finding_not_failure(tmp_path: Path) -> None:
    retail_packet_dir = _write_retail_packet_dir(tmp_path)
    retail_projection_path = tmp_path / "retail_projection" / "retail_pdp_projection.json"
    write_retail_pdp_projection(
        packet_directory=retail_packet_dir,
        output_path=retail_projection_path,
    )
    projection = _load_json(retail_projection_path)
    for row in projection["rows"]:
        if row["row_kind"] == "retail_review_substrate":
            row["raw_anchor"]["anchor_kind"] = "text_pattern"
            row["raw_anchor"]["anchor_value"] = "not present in fixture raw"
    _write_json(retail_projection_path, projection)
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        retail_packet_dir=retail_packet_dir,
        retail_projection_path=retail_projection_path,
    )

    outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )

    cleaning_packet = CleaningPacket.model_validate(
        _load_json(Path(outputs["cleaning_packet"]))
    )
    summary = _load_json(Path(outputs["smoke_summary"]))
    assert cleaning_packet.handles
    assert any(
        finding["code"] == "retail_row_anchor_unverified"
        and finding["reason"] == "text_pattern_absent_from_raw"
        for finding in summary["findings"]
    )


def test_retail_missing_html_selector_anchor_is_finding_not_failure(tmp_path: Path) -> None:
    retail_packet_dir = _write_retail_packet_dir(tmp_path)
    retail_projection_path = tmp_path / "retail_projection" / "retail_pdp_projection.json"
    write_retail_pdp_projection(
        packet_directory=retail_packet_dir,
        output_path=retail_projection_path,
    )
    projection = _load_json(retail_projection_path)
    for row in projection["rows"]:
        if row["row_kind"] == "retail_variant_offer":
            row["raw_anchor"]["anchor_kind"] = "html_selector"
            row["raw_anchor"]["anchor_value"] = "#missingSelector"
    _write_json(retail_projection_path, projection)
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        retail_packet_dir=retail_packet_dir,
        retail_projection_path=retail_projection_path,
    )

    outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )

    summary = _load_json(Path(outputs["smoke_summary"]))
    assert any(
        finding["code"] == "retail_row_anchor_unverified"
        and finding["reason"] == "html_selector_id_or_name_absent_from_raw"
        for finding in summary["findings"]
    )


def test_runner_opt_in_cleaning_transform_smoke_writes_one_ledger_entry(tmp_path: Path) -> None:
    retail_packet_dir = _write_retail_packet_dir(tmp_path)
    retail_projection_path = tmp_path / "retail_projection" / "retail_pdp_projection.json"
    write_retail_pdp_projection(
        packet_directory=retail_packet_dir,
        output_path=retail_projection_path,
    )
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        retail_packet_dir=retail_packet_dir,
        retail_projection_path=retail_projection_path,
    )

    outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
        include_cleaning_transform_smoke=True,
    )

    cleaning_packet = CleaningPacket.model_validate(
        _load_json(Path(outputs["cleaning_packet"]))
    )
    summary = _load_json(Path(outputs["smoke_summary"]))

    assert len(cleaning_packet.transform_ledger) == 1
    entry = cleaning_packet.transform_ledger[0]
    assert entry.input_handle_id in {handle.handle_id for handle in cleaning_packet.handles}
    assert entry.transform.transform_class.value == "normalization"
    assert entry.transform.method_or_rule == "unicode_nfkc_whitespace_collapse"
    assert entry.transform.original_value is not None
    assert entry.transform.original_value != "2026-06-16T00:00:00Z"
    assert not entry.input_handle_id.endswith(":pdp")
    assert entry.transform.transformed_value is not None
    assert summary["cleaning_transform_smoke_enabled"] is True
    assert summary["counts"]["cleaning_transform_entries"] == 1


def test_transform_smoke_fails_without_source_visible_string(tmp_path: Path) -> None:
    retail_packet_dir = _write_retail_packet_dir(tmp_path)
    retail_projection_path = tmp_path / "retail_projection" / "retail_pdp_projection.json"
    write_retail_pdp_projection(
        packet_directory=retail_packet_dir,
        output_path=retail_projection_path,
    )
    projection = _load_json(retail_projection_path)
    for row in projection["rows"]:
        row["source_visible_fields"] = {}
    for binding in projection["binding_map"]:
        binding["source_visible_fields"] = {}
    _write_json(retail_projection_path, projection)
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        retail_packet_dir=retail_packet_dir,
        retail_projection_path=retail_projection_path,
    )

    with pytest.raises(ValueError, match="source-visible string value"):
        run_capture_ecr_cleaning_smoke(
            smoke_manifest_path=smoke_manifest_path,
            output_dir=tmp_path / "smoke_outputs",
            include_cleaning_transform_smoke=True,
        )


def test_old_reddit_anchor_pattern_accepts_bare_and_prefixed_ids_on_raw_bytes() -> None:
    comment_html = b'<div data-fullname="t1_c1">\xff</div>'
    post_html = b"<div id='thing_t3_abc'>\xfe</div>"

    assert (
        _old_reddit_anchor_pattern(comment_html, "t1", "c1")
        == 'data-fullname="t1_c1"'
    )
    assert (
        _old_reddit_anchor_pattern(comment_html, "t1", "t1_c1")
        == 'data-fullname="t1_c1"'
    )
    assert (
        _old_reddit_anchor_pattern(post_html, "t3", "abc")
        == "id='thing_t3_abc'"
    )
    assert (
        _old_reddit_anchor_pattern(post_html, "t3", "t3_abc")
        == "id='thing_t3_abc'"
    )


def test_reddit_missing_row_anchor_downgrades_to_file_anchor(tmp_path: Path) -> None:
    reddit_packet_dir = _write_reddit_packet_dir(tmp_path, NORMAL_THREAD_HTML)
    reddit_consolidation = consolidate_reddit_packet(
        packet_or_manifest_path=reddit_packet_dir,
        output_directory=tmp_path / "reddit_consolidation",
    )
    consolidation_path = Path(reddit_consolidation["json_path"])
    artifact = _load_json(consolidation_path)
    artifact["reddit_thread_consolidation"]["comments"][0]["comment_id"] = "missing"
    consolidation_path.write_text(
        json.dumps(artifact, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        reddit_packet_dir=reddit_packet_dir,
        reddit_consolidation_path=consolidation_path,
    )

    outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )

    cleaning_packet = CleaningPacket.model_validate(
        _load_json(Path(outputs["cleaning_packet"]))
    )
    summary = _load_json(Path(outputs["smoke_summary"]))

    assert any(
        finding["code"] == "reddit_row_anchor_downgraded"
        and finding["row_kind"] == "comment"
        for finding in summary["findings"]
    )
    assert any(
        handle.handle_id.startswith("reddit:1:")
        and handle.raw_anchor.anchor_kind == "file"
        for handle in cleaning_packet.handles
    )


def test_runner_refuses_empty_manifest_and_existing_outputs(tmp_path: Path) -> None:
    empty_manifest = tmp_path / "empty_smoke_manifest.json"
    empty_manifest.write_text(
        json.dumps({"run_id": "empty", "retail": [], "reddit": []}) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="at least one retail or reddit source"):
        run_capture_ecr_cleaning_smoke(
            smoke_manifest_path=empty_manifest,
            output_dir=tmp_path / "empty_outputs",
        )

    retail_packet_dir = _write_retail_packet_dir(tmp_path)
    retail_projection_path = tmp_path / "retail_projection" / "retail_pdp_projection.json"
    write_retail_pdp_projection(
        packet_directory=retail_packet_dir,
        output_path=retail_projection_path,
    )
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        retail_packet_dir=retail_packet_dir,
        retail_projection_path=retail_projection_path,
    )
    output_dir = tmp_path / "smoke_outputs"
    output_dir.mkdir()
    (output_dir / "cleaning_packet.json").write_text("{}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="smoke output already exists"):
        run_capture_ecr_cleaning_smoke(
            smoke_manifest_path=smoke_manifest_path,
            output_dir=output_dir,
        )


def test_retail_projection_slice_file_mismatch_refuses(tmp_path: Path) -> None:
    retail_packet_dir = _write_retail_packet_dir(tmp_path)
    retail_projection_path = tmp_path / "retail_projection" / "retail_pdp_projection.json"
    write_retail_pdp_projection(
        packet_directory=retail_packet_dir,
        output_path=retail_projection_path,
    )
    manifest = _load_json(retail_packet_dir / "manifest.json")
    wrong_slice = dict(manifest["source_slices"][0])
    wrong_slice["slice_id"] = "wrong_slice"
    wrong_slice["preserved_file_ids"] = []
    manifest["source_slices"].append(wrong_slice)
    _write_json(retail_packet_dir / "manifest.json", manifest)
    projection = _load_json(retail_projection_path)
    for row in projection["rows"]:
        row["raw_ref"]["slice_id"] = "wrong_slice"
    _write_json(retail_projection_path, projection)
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        retail_packet_dir=retail_packet_dir,
        retail_projection_path=retail_projection_path,
    )

    with pytest.raises(ValueError, match="does not preserve file_id"):
        run_capture_ecr_cleaning_smoke(
            smoke_manifest_path=smoke_manifest_path,
            output_dir=tmp_path / "smoke_outputs",
        )


def test_retail_projection_packet_id_mismatch_refuses(tmp_path: Path) -> None:
    retail_packet_dir = _write_retail_packet_dir(tmp_path)
    retail_projection_path = tmp_path / "retail_projection" / "retail_pdp_projection.json"
    write_retail_pdp_projection(
        packet_directory=retail_packet_dir,
        output_path=retail_projection_path,
    )
    projection = _load_json(retail_projection_path)
    projection["packet_id"] = "01DIFFERENTPACKET"
    _write_json(retail_projection_path, projection)
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        retail_packet_dir=retail_packet_dir,
        retail_projection_path=retail_projection_path,
    )

    with pytest.raises(ValueError, match="projection packet_id"):
        run_capture_ecr_cleaning_smoke(
            smoke_manifest_path=smoke_manifest_path,
            output_dir=tmp_path / "smoke_outputs",
        )


def test_preserved_file_hash_mismatch_refuses(tmp_path: Path) -> None:
    retail_packet_dir = _write_retail_packet_dir(tmp_path)
    retail_projection_path = tmp_path / "retail_projection" / "retail_pdp_projection.json"
    write_retail_pdp_projection(
        packet_directory=retail_packet_dir,
        output_path=retail_projection_path,
    )
    raw_path = retail_packet_dir / "raw" / "01_cloakbrowser_rendered_dom.html"
    raw_path.write_text("tampered", encoding="utf-8")
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        retail_packet_dir=retail_packet_dir,
        retail_projection_path=retail_projection_path,
    )

    with pytest.raises(ValueError, match="hash mismatch against manifest"):
        run_capture_ecr_cleaning_smoke(
            smoke_manifest_path=smoke_manifest_path,
            output_dir=tmp_path / "smoke_outputs",
        )


def test_preserved_file_path_escape_refuses(tmp_path: Path) -> None:
    retail_packet_dir = _write_retail_packet_dir(tmp_path)
    retail_projection_path = tmp_path / "retail_projection" / "retail_pdp_projection.json"
    write_retail_pdp_projection(
        packet_directory=retail_packet_dir,
        output_path=retail_projection_path,
    )
    manifest = _load_json(retail_packet_dir / "manifest.json")
    for preserved_file in manifest["preserved_files"]:
        if preserved_file["file_id"] == "file_01":
            preserved_file["relative_packet_path"] = "../escape.html"
    _write_json(retail_packet_dir / "manifest.json", manifest)
    projection = _load_json(retail_projection_path)
    for row in projection["rows"]:
        if row["raw_anchor"]["file_id"] == "file_01":
            row["raw_anchor"]["relative_packet_path"] = "../escape.html"
    _write_json(retail_projection_path, projection)
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        retail_packet_dir=retail_packet_dir,
        retail_projection_path=retail_projection_path,
    )

    with pytest.raises(ValueError, match="escapes packet directory"):
        run_capture_ecr_cleaning_smoke(
            smoke_manifest_path=smoke_manifest_path,
            output_dir=tmp_path / "smoke_outputs",
        )


def test_runner_main_maps_validation_errors_to_cli_failure(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    retail_packet_dir = _write_retail_packet_dir(tmp_path)
    retail_projection_path = tmp_path / "retail_projection" / "retail_pdp_projection.json"
    write_retail_pdp_projection(
        packet_directory=retail_packet_dir,
        output_path=retail_projection_path,
    )
    projection = _load_json(retail_projection_path)
    projection["rows"] = []
    projection["binding_map"] = []
    projection["loss_ledger"].update(
        {
            "collapsed": [],
            "preserved_evidence_rows": 0,
            "preserved_bindings": 0,
            "hierarchy_preserved": False,
            "structure_preserved": False,
        }
    )
    projection["residuals"] = ["fixture_zero_rows"]
    _write_json(retail_projection_path, projection)
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        retail_packet_dir=retail_packet_dir,
        retail_projection_path=retail_projection_path,
    )

    with pytest.raises(SystemExit) as exc_info:
        smoke_runner.main(
            [
                "--smoke-manifest",
                str(smoke_manifest_path),
                "--output-dir",
                str(tmp_path / "smoke_outputs"),
            ]
        )

    assert exc_info.value.code == 2
    assert "capture/ECR/Cleaning smoke failed:" in capsys.readouterr().err

def _write_smoke_manifest(
    tmp_path: Path,
    *,
    retail_packet_dir: Path | None = None,
    retail_projection_path: Path | None = None,
    reddit_packet_dir: Path | None = None,
    reddit_consolidation_path: Path | None = None,
) -> Path:
    manifest: dict[str, object] = {"run_id": "fixture_real_data_shape_smoke"}
    if retail_packet_dir is not None and retail_projection_path is not None:
        manifest["retail"] = [
            {
                "retailer": "sephora",
                "packet_dir": str(retail_packet_dir),
                "projection_json": str(retail_projection_path),
            }
        ]
    if reddit_packet_dir is not None and reddit_consolidation_path is not None:
        manifest["reddit"] = [
            {
                "packet_dir": str(reddit_packet_dir),
                "consolidation_json": str(reddit_consolidation_path),
            }
        ]
    path = tmp_path / f"smoke_manifest_{len(list(tmp_path.glob('smoke_manifest_*.json')))}.json"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _write_reddit_packet_dir(tmp_path: Path, html: str) -> Path:
    input_path = tmp_path / "thread.html"
    input_path.write_text(html, encoding="utf-8")
    output_dir = tmp_path / "reddit_packet"
    result = write_local_source_capture_packet(
        output_directory=output_dir,
        input_files=[input_path],
        source_family="reddit_thread",
        source_surface="old_reddit_html",
        source_locator=known_fact(
            "https://old.reddit.com/r/b2bmarketing/comments/abc/fragrance_marketing/"
        ),
        decision_question="What visible Reddit thread content is preserved in this packet?",
        capture_context="local test packet over already-preserved old-Reddit-like HTML",
        capture_mode=CaptureModeCategory.AGENT_ASSISTED,
        operator_category="capture_ecr_cleaning_smoke_test_operator",
    )
    return Path(result.output_directory)


def _write_retail_packet_dir(
    tmp_path: Path,
    *,
    html: str | None = None,
    visible_text: str | None = None,
) -> Path:
    packet = _retail_packet()
    raw_file_bytes_by_file_id = {
        "file_01": (html if html is not None else _retail_html()).encode("utf-8"),
        "file_02": (
            visible_text if visible_text is not None else _retail_visible_text()
        ).encode("utf-8"),
    }
    packet = packet.model_copy(
        update={
            "preserved_files": [
                preserved_file.model_copy(
                    update={
                        "sha256": hashlib.sha256(
                            raw_file_bytes_by_file_id[preserved_file.file_id]
                        ).hexdigest(),
                        "size_bytes": len(
                            raw_file_bytes_by_file_id[preserved_file.file_id]
                        ),
                    }
                )
                for preserved_file in packet.preserved_files
            ]
        }
    )
    packet_dir = tmp_path / "retail_packet"
    for preserved_file in packet.preserved_files:
        file_path = packet_dir / preserved_file.relative_packet_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(raw_file_bytes_by_file_id[preserved_file.file_id])
    (packet_dir / "manifest.json").write_text(
        json.dumps(packet.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return packet_dir


def _retail_packet() -> SourceCapturePacket:
    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason(
            "retail PDP fixture does not supply source event timing"
        ),
        source_edit_or_version=unknown_with_reason(
            "retail PDP fixture does not supply edit timing"
        ),
        capture_time=known_fact("2026-06-16T00:00:00Z"),
        recapture_time=not_applicable("first capture"),
        cutoff_posture=unknown_with_reason("test fixture has no decision cutoff"),
    )
    locator = "https://www.sephora.com/product/good-girl-jasmine-absolute-P123456"
    return SourceCapturePacket(
        packet_id="01TESTRETAILSMOKE",
        manifest_version="source_capture_packet_manifest_v1",
        obligation_contract_version="core_spine_v0_data_capture_spine_obligation_contract_v0",
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        source_locator=known_fact(locator),
        requested_decision_context=known_fact("Fragrance PDP smoke fixture."),
        capture_context=known_fact("unit test packet"),
        actor_audience_context=unknown_with_reason("not supplied by fixture"),
        capture_mode=CaptureModeCategory.MULTIMODAL,
        operator_category="unit_test",
        session_identity="01TESTSESSION",
        timing=timing,
        access_posture=known_fact("rendered DOM fixture supplied"),
        archive_history_posture=not_attempted("archive not queried"),
        media_modality_posture=not_attempted("screenshot not supplied"),
        re_capture_relationship=not_applicable("first capture"),
        series_id="sephora_good_girl_fragrance_us_v0",
        intended_cadence={"mode": "fixed", "slot_count": 1},
        source_slices=[
            SourceCaptureSlice(
                slice_id="cloakbrowser_snapshot_01",
                locator=known_fact(locator),
                timing=timing,
                access_posture=known_fact("rendered DOM fixture supplied"),
                archive_history_posture=not_attempted("archive not queried"),
                media_modality_posture=not_attempted("screenshot not supplied"),
                re_capture_relationship=not_applicable("first capture"),
                locale_pin=known_fact("en-US"),
                currency_pin=known_fact("USD"),
                variant_pin=known_fact("Jasmine Absolute Eau de Parfum"),
                limitations=[],
                warning_notes=[],
                preserved_file_ids=["file_01", "file_02"],
            )
        ],
        preserved_files=[
            PreservedFile(
                file_id="file_01",
                original_path="rendered_dom.html",
                relative_packet_path="raw/01_cloakbrowser_rendered_dom.html",
                sha256="htmlsha",
                hash_basis="raw_stored_bytes",
                size_bytes=123,
            ),
            PreservedFile(
                file_id="file_02",
                original_path="visible_text.txt",
                relative_packet_path="raw/02_cloakbrowser_visible_text.txt",
                sha256="textsha",
                hash_basis="raw_stored_bytes",
                size_bytes=123,
            ),
        ],
        receipt_metadata=ReceiptMetadata(
            title="Source Capture Packet Receipt",
            generated_at="2026-06-16T00:00:00Z",
            summary="unit test packet",
            non_claims=["not Cleaning", "not Judgment"],
        ),
    )


def _retail_html() -> str:
    ld_json = json.dumps(
        {
            "@context": "http://schema.org",
            "@type": "Product",
            "name": "Good Girl Jasmine Absolute Eau de Parfum",
            "productID": "P123456",
            "sku": "1234567",
            "offers": {
                "@type": "Offer",
                "price": "168.00",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
            },
            "aggregateRating": {
                "@type": "AggregateRating",
                "reviewCount": "245",
                "ratingValue": "4.5",
            },
        },
        separators=(",", ":"),
    )
    return f"""
    <html><head>
      <script type="application/ld+json">{ld_json}</script>
    </head><body>
      <div data-cnstrc-item-id="P123456" data-cnstrc-item-price="$168.00"
        data-cnstrc-item-variation-id="1234567" data-comp="ProductPage">
        <b>$168.00</b>
      </div>
      <section id="target-reviews">Ratings & Reviews (245)<span>245 Reviews*</span></section>
      <p>Get It Shipped</p>
      <p>Fragrance family: floral</p>
    </body></html>
    """


def _retail_visible_text() -> str:
    return """
    Good Girl Jasmine Absolute Eau de Parfum
    $168.00
    Get It Shipped
    Fragrance family: floral
    Ratings & Reviews (245)
    4.5
    245 Reviews*
    """


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _load_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


NORMAL_THREAD_HTML = """\
<!doctype html>
<html>
  <body class="old-reddit">
    <div id="siteTable">
      <div class="thing link" data-fullname="t3_abc" data-subreddit="b2bmarketing"
           data-author="poster" data-score="42"
           data-permalink="/r/b2bmarketing/comments/abc/fragrance_marketing/">
        <a class="title" href="/r/b2bmarketing/comments/abc/fragrance_marketing/">Fragrance marketing</a>
        <time datetime="2026-06-01T00:00:00Z">1 day ago</time>
        <div class="usertext-body"><div class="md"><p>Original post body</p></div></div>
      </div>
    </div>
    <div class="sitetable nestedlisting">
      <div class="thing comment" data-fullname="t1_c1" data-parent="t3_abc" data-depth="0"
           data-author="commenter_one" data-score="5">
        <time datetime="2026-06-01T01:00:00Z">1 hour ago</time>
        <div class="usertext-body"><div class="md"><p>First comment</p></div></div>
        <div class="child">
          <div class="sitetable">
            <div class="thing comment" data-fullname="t1_c2" data-parent="t1_c1" data-depth="1"
                 data-author="commenter_two">
              <span class="score unvoted">score hidden</span>
              <div class="usertext-body"><div class="md"><p>Nested reply</p></div></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
"""
