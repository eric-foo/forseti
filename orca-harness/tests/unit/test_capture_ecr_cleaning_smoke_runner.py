from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from cleaning.models import CleaningPacket
from runners import run_capture_ecr_cleaning_smoke as smoke_runner
from runners import run_cleaning_spine_periodic_audit as audit_runner
from runners.run_capture_ecr_cleaning_smoke import (
    _old_reddit_anchor_pattern,
    run_capture_ecr_cleaning_smoke,
)
from runners.run_cleaning_spine_periodic_audit import run_cleaning_spine_periodic_audit
from source_capture.models import (
    CaptureModeCategory,
    CoverageWindow,
    MetricObservation,
    MetricPosture,
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
from source_capture.ig_projection import write_ig_creator_momentum_projection
from source_capture.reddit_consolidation import consolidate_reddit_packet
from source_capture.retail_pdp_projection import write_retail_pdp_projection
from source_capture.transcript.caption_packet import write_caption_packet
from source_capture.transcript.youtube_captions import CaptionFetch
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
        "instagram_sources": 0,
        "youtube_sources": 0,
        "youtube_asr_sources": 0,
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
    assert all(handle.projection_ref is not None for handle in reddit_handles)
    assert {
        handle.projection_ref.row_id
        for handle in reddit_handles
        if handle.projection_ref is not None
    } == {"post", "comment_0001", "comment_0002"}
    assert {
        handle.projection_ref.row_kind
        for handle in reddit_handles
        if handle.projection_ref is not None
    } == {"post", "comment"}
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


def test_runner_writes_ecr_receipts_and_cleaning_packet_for_instagram(
    tmp_path: Path,
) -> None:
    instagram_packet_dir = _write_instagram_packet_dir(tmp_path)
    instagram_projection_path = tmp_path / "instagram_projection" / "ig_projection.json"
    instagram_projection = write_ig_creator_momentum_projection(
        packet_or_manifest_path=instagram_packet_dir,
        output_path=instagram_projection_path,
    )
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        instagram_handle="hyram",
        instagram_packet_dir=instagram_packet_dir,
        instagram_projection_path=instagram_projection_path,
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
        "retail_sources": 0,
        "reddit_sources": 0,
        "instagram_sources": 1,
        "youtube_sources": 0,
        "youtube_asr_sources": 0,
        "ecr_receipts": 1,
        "cleaning_handles": len(instagram_projection.rows),
        "cleaning_transform_entries": 0,
    }
    assert len(ecr_receipts["receipts"]) == 1
    assert ecr_receipts["receipts"][0]["source_label"] == "instagram:hyram"
    assert set(ecr_receipts["receipts"][0]["postures"]) == {
        "identity",
        "inspectability",
        "timing",
        "source_visibility",
    }
    assert len(cleaning_packet.handles) == len(instagram_projection.rows)
    assert all(handle.projection_ref is not None for handle in cleaning_packet.handles)
    assert all(handle.ecr_ref is not None for handle in cleaning_packet.handles)
    assert all(
        handle.ecr_ref.packet_id == handle.raw_anchor.packet_id
        for handle in cleaning_packet.handles
        if handle.ecr_ref is not None
    )
    assert all(handle.raw_anchor.anchor_kind == "json_pointer" for handle in cleaning_packet.handles)
    follower_handle = next(
        handle
        for handle in cleaning_packet.handles
        if handle.projection_ref and handle.projection_ref.row_kind == "ig_creator_metric"
    )
    assert follower_handle.raw_anchor.json_pointer == "/follower_count"
    instagram_source = next(
        source for source in summary["sources"] if source["source_label"] == "instagram:hyram"
    )
    assert instagram_source["handle_count"] == len(instagram_projection.rows)
    assert instagram_source["row_count"] == len(instagram_projection.rows)
    assert instagram_source["structure_preserved"] is True
    assert summary["findings"] == []

def test_runner_writes_ecr_receipts_and_cleaning_packet_for_youtube(tmp_path: Path) -> None:
    youtube_packet_dir = _write_youtube_packet_dir(tmp_path)
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        youtube_packet_dir=youtube_packet_dir,
        youtube_source_label="youtube:hyram",
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
        "retail_sources": 0,
        "reddit_sources": 0,
        "instagram_sources": 0,
        "youtube_sources": 1,
        "youtube_asr_sources": 0,
        "ecr_receipts": 1,
        "cleaning_handles": 2,
        "cleaning_transform_entries": 0,
    }

    # The clears-profile is the whole point: identity + inspectability clear, while timing
    # and source_visibility are HONEST non-clearing residuals (a caption has no cutoff class
    # and no archive comparison). Pinning the two False values is the anti-fake-success guard
    # -- "a receipt was emitted" must never pass on its own.
    assert len(ecr_receipts["receipts"]) == 1
    receipt = ecr_receipts["receipts"][0]
    assert receipt["source_label"] == "youtube:hyram"
    assert receipt["clears"] == {
        "identity": True,
        "inspectability": True,
        "timing": False,
        "source_visibility": False,
    }
    assert any(
        (posture.get("residual") or {}).get("status") == "not_applicable"
        for posture in receipt["postures"]["timing"]
    )
    assert any(
        posture.get("value") == "current_capture_only"
        for posture in receipt["postures"]["source_visibility"]
    )

    youtube_handles = [
        handle
        for handle in cleaning_packet.handles
        if handle.handle_id.startswith("youtube:hyram:")
    ]
    assert len(youtube_handles) == 2
    assert all(handle.source_family == "youtube" for handle in youtube_handles)
    assert all(handle.source_surface == "youtube_captions" for handle in youtube_handles)
    assert all(handle.projection_ref is None for handle in youtube_handles)
    assert all(handle.raw_anchor.anchor_kind == "file" for handle in youtube_handles)
    assert all(handle.ecr_ref is not None for handle in youtube_handles)
    assert all(
        handle.ecr_ref.packet_id == handle.raw_anchor.packet_id
        for handle in youtube_handles
        if handle.ecr_ref is not None
    )
    assert any(
        handle.raw_anchor.relative_packet_path.endswith(".json3")
        for handle in youtube_handles
    )
    youtube_source = next(
        source for source in summary["sources"] if source["source_label"] == "youtube:hyram"
    )
    assert youtube_source["source_surface"] == "youtube_captions"
    assert youtube_source["slice_count"] == 1
    assert youtube_source["preserved_file_count"] == 2
    assert youtube_source["handle_count"] == 2
    assert summary["findings"] == []


def test_youtube_entry_refuses_non_youtube_packet(tmp_path: Path) -> None:
    # The YouTube entry has no projection/consolidation cross-check, so a manifest that routes a
    # NON-YouTube packet through the YouTube branch must fail closed on the identity guard.
    non_youtube_packet_dir = _write_instagram_packet_dir(tmp_path)
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        youtube_packet_dir=non_youtube_packet_dir,
        youtube_source_label="youtube:spoofed",
    )
    with pytest.raises(ValueError, match="not a YouTube caption packet"):
        run_capture_ecr_cleaning_smoke(
            smoke_manifest_path=smoke_manifest_path,
            output_dir=tmp_path / "smoke_outputs",
        )


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


def test_retail_ambiguous_text_pattern_anchor_is_finding_not_failure(tmp_path: Path) -> None:
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
            row["raw_anchor"]["anchor_value"] = "Reviews"
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
        and finding["reason"] == "text_pattern_ambiguous_in_raw"
        and finding["anchor_value"] == "Reviews"
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


def test_periodic_audit_accepts_transform_original_value_from_projection(tmp_path: Path) -> None:
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
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
        include_cleaning_transform_smoke=True,
    )
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "pass"
    assert not any(
        finding["code"] == "cleaning_transform_original_value_unresolved"
        for finding in report["findings"]
    )


def test_periodic_audit_flags_transform_original_value_not_from_projection_or_raw(
    tmp_path: Path,
) -> None:
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
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
        include_cleaning_transform_smoke=True,
    )
    cleaning_path = Path(smoke_outputs["cleaning_packet"])
    cleaning_payload = _load_json(cleaning_path)
    cleaning_payload["transform_ledger"][0]["transform"]["original_value"] = (
        "invented original text absent from raw and projection"
    )
    _write_json(cleaning_path, cleaning_payload)
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "fail"
    assert any(
        finding["lane"] == "lane_a_existing_package"
        and finding["code"] == "cleaning_transform_original_value_unresolved"
        and finding["owner_candidate"] == "cleaning"
        and finding["details"]["original_value"]
        == "invented original text absent from raw and projection"
        for finding in report["findings"]
    )

def test_transform_original_value_raw_anchor_accepts_text_pattern_value(tmp_path: Path) -> None:
    anchored_value = "RAW_ANCHORED_VALUE"
    retail_packet_dir = _write_retail_packet_dir(
        tmp_path,
        html=_retail_html() + f"\n<!-- {anchored_value} -->",
    )
    packet = SourceCapturePacket.model_validate(
        _load_json(retail_packet_dir / "manifest.json")
    )
    preserved_file = next(
        item for item in packet.preserved_files if item.file_id == "file_01"
    )
    raw_anchor = {
        "packet_id": packet.packet_id,
        "slice_id": packet.source_slices[0].slice_id,
        "file_id": preserved_file.file_id,
        "relative_packet_path": preserved_file.relative_packet_path,
        "sha256": preserved_file.sha256,
        "anchor_kind": "text_pattern",
        "anchor_value": anchored_value,
    }

    assert audit_runner._transform_original_value_in_raw(
        original_value=anchored_value,
        raw_anchor=raw_anchor,
        packet_index={
            packet.packet_id: {"packet": packet, "packet_dir": retail_packet_dir}
        },
    )


def test_transform_original_value_raw_anchor_rejects_unanchored_raw_substring(
    tmp_path: Path,
) -> None:
    anchor_value = "REAL_ANCHOR_VALUE"
    coincidental_value = "COINCIDENTAL_RAW_ONLY_VALUE"
    retail_packet_dir = _write_retail_packet_dir(
        tmp_path,
        html=(
            _retail_html()
            + f"\n<!-- {anchor_value} -->"
            + f"\n<!-- {coincidental_value} -->"
        ),
    )
    packet = SourceCapturePacket.model_validate(
        _load_json(retail_packet_dir / "manifest.json")
    )
    preserved_file = next(
        item for item in packet.preserved_files if item.file_id == "file_01"
    )
    raw_anchor = {
        "packet_id": packet.packet_id,
        "slice_id": packet.source_slices[0].slice_id,
        "file_id": preserved_file.file_id,
        "relative_packet_path": preserved_file.relative_packet_path,
        "sha256": preserved_file.sha256,
        "anchor_kind": "text_pattern",
        "anchor_value": anchor_value,
    }

    assert not audit_runner._transform_original_value_in_raw(
        original_value=coincidental_value,
        raw_anchor=raw_anchor,
        packet_index={
            packet.packet_id: {"packet": packet, "packet_dir": retail_packet_dir}
        },
    )

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

    with pytest.raises(
        ValueError,
        match="at least one retail, reddit, instagram, youtube, or youtube_asr source",
    ):
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


def test_periodic_audit_passes_for_fixture_capture_projection_cleaning(
    tmp_path: Path,
) -> None:
    retail_packet_dir = _write_retail_packet_dir(tmp_path)
    retail_projection_path = tmp_path / "retail_projection" / "retail_pdp_projection.json"
    write_retail_pdp_projection(
        packet_directory=retail_packet_dir,
        output_path=retail_projection_path,
    )
    reddit_packet_dir = _write_reddit_packet_dir(tmp_path, NORMAL_THREAD_HTML)
    reddit_consolidation = consolidate_reddit_packet(
        packet_or_manifest_path=reddit_packet_dir,
        output_directory=tmp_path / "reddit_consolidation",
    )
    instagram_packet_dir = _write_instagram_packet_dir(tmp_path)
    instagram_projection_path = tmp_path / "instagram_projection" / "ig_projection.json"
    write_ig_creator_momentum_projection(
        packet_or_manifest_path=instagram_packet_dir,
        output_path=instagram_projection_path,
    )
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        retail_packet_dir=retail_packet_dir,
        retail_projection_path=retail_projection_path,
        reddit_packet_dir=reddit_packet_dir,
        reddit_consolidation_path=Path(reddit_consolidation["json_path"]),
        instagram_handle="hyram",
        instagram_packet_dir=instagram_packet_dir,
        instagram_projection_path=instagram_projection_path,
    )
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "pass"
    assert report["lane_statuses"] == {
        "capture_preflight": "pass",
        "lane_a_existing_package": "pass",
        "lane_b_projection_breakpoint": "pass",
        "lane_b_cleaning_breakpoint": "pass",
    }
    assert report["counts"]["source_entries"] == 3
    assert report["lane_b_cleaning_breakpoint"]["cleaning_signature_match"] is True
    assert report["lane_b_cleaning_breakpoint"]["ecr_signature_match"] is True
    assert "not_live_capture" in report["non_claims"]


def test_periodic_audit_passes_for_projection_less_youtube_capture(tmp_path: Path) -> None:
    # The projection-less YouTube handle flows through the FULL audit clean: its packet enters
    # packet_index (so the raw anchor resolves), adapter-coverage accepts the file anchor, and
    # lane-B records it as not-applicable instead of failing a projection rebuild.
    youtube_packet_dir = _write_youtube_packet_dir(tmp_path)
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        youtube_packet_dir=youtube_packet_dir,
        youtube_source_label="youtube:hyram",
    )
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "pass"
    assert report["counts"]["source_entries"] == 1
    assert report["lane_statuses"]["lane_a_existing_package"] == "pass"
    assert report["lane_statuses"]["lane_b_projection_breakpoint"] == "pass"


def test_periodic_audit_supported_source_families_have_adapter_coverage() -> None:
    audit_runner._validate_source_family_adapter_contract()
    assert audit_runner.SUPPORTED_SOURCE_FAMILIES == ("retail", "reddit", "instagram")
    for source_family in audit_runner.SUPPORTED_SOURCE_FAMILIES:
        adapter = audit_runner._SOURCE_FAMILY_AUDIT_ADAPTERS[source_family]
        assert adapter["row_kinds"]
        assert adapter["anchor_kinds"]


def test_periodic_audit_accepts_projection_less_youtube_file_anchor() -> None:
    # The projection-less set is well-formed and disjoint from the projection-backed mapping
    # (otherwise this raises). YouTube allows the direct-artifact "file" anchor (captions) and the
    # "derived_record" anchor (ASR transcript record).
    audit_runner._validate_source_family_adapter_contract()
    assert audit_runner._PROJECTION_LESS_SOURCE_FAMILIES["youtube"] == frozenset(
        {"file", "derived_record"}
    )

    # A projection-less YouTube file-anchor handle clears coverage with no finding.
    ok_findings: list[dict[str, object]] = []
    audit_runner._verify_source_family_anchor_adapter_coverage(
        handle_id="youtube:fixture:file_01",
        source_family="youtube",
        raw_anchor={"packet_id": "pkt_yt", "anchor_kind": "file"},
        findings=ok_findings,
        lane="lane_a_existing_package",
    )
    assert ok_findings == []

    # A non-file anchor for a projection-less source is flagged (fail closed on unsupported kind).
    bad_findings: list[dict[str, object]] = []
    audit_runner._verify_source_family_anchor_adapter_coverage(
        handle_id="youtube:fixture:file_01",
        source_family="youtube",
        raw_anchor={"packet_id": "pkt_yt", "anchor_kind": "text_pattern"},
        findings=bad_findings,
        lane="lane_a_existing_package",
    )
    assert any(
        finding["code"] == "cleaning_anchor_kind_unsupported_for_source_family"
        for finding in bad_findings
    )


def test_periodic_audit_flags_projection_row_kind_outside_source_family_adapter() -> None:
    findings: list[dict[str, object]] = []

    row_index = audit_runner._projection_rows_by_id(
        packet_id="packet_001",
        source_label="retail:fixture",
        source_type="retail",
        rows=[
            ("row_1", "retail_pdp_product", {"product_name": "Fixture"}),
            ("row_2", "ig_creator_metric", {"followers": "724K"}),
        ],
        findings=findings,
        lane="lane_a_existing_package",
    )

    assert row_index["row_2"]["row_kind"] == "ig_creator_metric"
    assert any(
        finding["code"] == "projection_row_kind_unsupported_for_source_family"
        and finding["owner_candidate"] == "projection_or_audit_adapter"
        and finding["details"] == {
            "source_type": "retail",
            "unsupported_row_kinds": ["ig_creator_metric"],
            "allowed_row_kinds": sorted(
                audit_runner._SOURCE_FAMILY_AUDIT_ADAPTERS["retail"]["row_kinds"]
            ),
        }
        for finding in findings
    )


def test_periodic_audit_flags_anchor_kind_outside_source_family_adapter(
    tmp_path: Path,
) -> None:
    instagram_packet_dir = _write_instagram_packet_dir(tmp_path)
    instagram_projection_path = tmp_path / "instagram_projection" / "ig_projection.json"
    write_ig_creator_momentum_projection(
        packet_or_manifest_path=instagram_packet_dir,
        output_path=instagram_projection_path,
    )
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        instagram_handle="hyram",
        instagram_packet_dir=instagram_packet_dir,
        instagram_projection_path=instagram_projection_path,
    )
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    cleaning_path = Path(smoke_outputs["cleaning_packet"])
    cleaning_payload = _load_json(cleaning_path)
    cleaning_payload["handles"][0]["raw_anchor"]["anchor_kind"] = "text_pattern"
    cleaning_payload["handles"][0]["raw_anchor"]["anchor_value"] = "724K"
    _write_json(cleaning_path, cleaning_payload)
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "fail"
    assert any(
        finding["lane"] == "lane_a_existing_package"
        and finding["code"] == "cleaning_anchor_kind_unsupported_for_source_family"
        and finding["owner_candidate"] == "cleaning_or_audit_adapter"
        and finding["details"] == {
            "source_family": "instagram_creator",
            "source_type": "instagram",
            "anchor_kind": "text_pattern",
            "allowed_anchor_kinds": ["json_pointer"],
        }
        for finding in report["findings"]
    )


def test_periodic_audit_execution_does_not_open_network_socket(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
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
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    import socket

    def fail_socket(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("periodic audit attempted to open a network socket")

    monkeypatch.setattr(socket, "socket", fail_socket)
    monkeypatch.setattr(socket, "create_connection", fail_socket)

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "pass"

def test_periodic_audit_flags_projection_breakpoint_drift(tmp_path: Path) -> None:
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
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    projection = _load_json(retail_projection_path)
    projection["residuals"].append("fixture_projection_drift")
    _write_json(retail_projection_path, projection)
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "fail"
    assert any(
        finding["lane"] == "lane_b_projection_breakpoint"
        and finding["code"] == "projection_rebuild_signature_mismatch"
        and finding["owner_candidate"] == "projection_or_consolidation"
        for finding in report["findings"]
    )

def test_periodic_audit_flags_projection_source_visible_field_drift(tmp_path: Path) -> None:
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
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    projection = _load_json(retail_projection_path)
    projection["rows"][0]["source_visible_fields"]["product_name"] = "Fixture Corrupted Name"
    _write_json(retail_projection_path, projection)
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "fail"
    assert any(
        finding["lane"] == "lane_b_projection_breakpoint"
        and finding["code"] == "projection_rebuild_signature_mismatch"
        for finding in report["findings"]
    )


def test_periodic_audit_flags_cleaning_projection_ref_row_unresolved(tmp_path: Path) -> None:
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
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    cleaning_path = Path(smoke_outputs["cleaning_packet"])
    cleaning_payload = _load_json(cleaning_path)
    cleaning_payload["handles"][0]["projection_ref"]["row_id"] = "missing_fixture_row"
    _write_json(cleaning_path, cleaning_payload)
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "fail"
    assert any(
        finding["lane"] == "lane_a_existing_package"
        and finding["code"] == "cleaning_projection_ref_row_unresolved"
        and finding["owner_candidate"] == "cleaning_or_projection"
        and finding["details"] == {"row_id": "missing_fixture_row"}
        for finding in report["findings"]
    )

def test_periodic_audit_flags_reddit_cleaning_projection_ref_row_unresolved(
    tmp_path: Path,
) -> None:
    reddit_packet_dir = _write_reddit_packet_dir(tmp_path, NORMAL_THREAD_HTML)
    reddit_consolidation = consolidate_reddit_packet(
        packet_or_manifest_path=reddit_packet_dir,
        output_directory=tmp_path / "reddit_consolidation",
    )
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        reddit_packet_dir=reddit_packet_dir,
        reddit_consolidation_path=Path(reddit_consolidation["json_path"]),
    )
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    cleaning_path = Path(smoke_outputs["cleaning_packet"])
    cleaning_payload = _load_json(cleaning_path)
    for handle in cleaning_payload["handles"]:
        if handle["handle_id"].endswith(":comment_0001"):
            handle["projection_ref"]["row_id"] = "missing_reddit_row"
            break
    else:
        pytest.fail("expected reddit comment handle")
    _write_json(cleaning_path, cleaning_payload)
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "fail"
    assert any(
        finding["lane"] == "lane_a_existing_package"
        and finding["code"] == "cleaning_projection_ref_row_unresolved"
        and finding["details"] == {"row_id": "missing_reddit_row"}
        for finding in report["findings"]
    )


def test_periodic_audit_flags_instagram_cleaning_projection_ref_row_unresolved(
    tmp_path: Path,
) -> None:
    instagram_packet_dir = _write_instagram_packet_dir(tmp_path)
    instagram_projection_path = tmp_path / "instagram_projection" / "ig_projection.json"
    write_ig_creator_momentum_projection(
        packet_or_manifest_path=instagram_packet_dir,
        output_path=instagram_projection_path,
    )
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        instagram_handle="hyram",
        instagram_packet_dir=instagram_packet_dir,
        instagram_projection_path=instagram_projection_path,
    )
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    cleaning_path = Path(smoke_outputs["cleaning_packet"])
    cleaning_payload = _load_json(cleaning_path)
    cleaning_payload["handles"][0]["projection_ref"]["row_id"] = "missing_ig_row"
    _write_json(cleaning_path, cleaning_payload)
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "fail"
    assert any(
        finding["lane"] == "lane_a_existing_package"
        and finding["code"] == "cleaning_projection_ref_row_unresolved"
        and finding["details"] == {"row_id": "missing_ig_row"}
        for finding in report["findings"]
    )


def test_periodic_audit_flags_duplicate_projection_row_ids(tmp_path: Path) -> None:
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
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    projection = _load_json(retail_projection_path)
    duplicate_row_id = projection["rows"][0]["row_id"]
    projection["rows"][1]["row_id"] = duplicate_row_id
    _write_json(retail_projection_path, projection)
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "fail"
    assert any(
        finding["lane"] == "lane_a_existing_package"
        and finding["code"] == "projection_row_index_ambiguous"
        and finding["details"] == {"duplicate_row_ids": [duplicate_row_id]}
        for finding in report["findings"]
    )

def test_periodic_audit_flags_cleaning_text_pattern_anchor_ambiguity(tmp_path: Path) -> None:
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
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    cleaning_path = Path(smoke_outputs["cleaning_packet"])
    cleaning_payload = _load_json(cleaning_path)
    cleaning_payload["handles"][0]["raw_anchor"]["anchor_kind"] = "text_pattern"
    cleaning_payload["handles"][0]["raw_anchor"]["anchor_value"] = "Reviews"
    _write_json(cleaning_path, cleaning_payload)
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert any(
        finding["lane"] == "lane_a_existing_package"
        and finding["severity"] == "minor"
        and finding["code"] == "cleaning_text_pattern_anchor_ambiguous"
        and finding["details"] == {
            "anchor_kind": "text_pattern",
            "anchor_value": "Reviews",
            "occurrence_count": 2,
        }
        for finding in report["findings"]
    )
def test_periodic_audit_promotes_lane_a_smoke_findings_to_status(tmp_path: Path) -> None:
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
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "fail"
    assert report["lane_statuses"]["lane_a_existing_package"] == "fail"
    assert any(
        finding["lane"] == "lane_a_existing_package"
        and finding["code"] == "lane_a_smoke_summary_finding"
        and finding["smoke_finding_code"] == "retail_capture_validity_not_supported"
        for finding in report["findings"]
    )


def test_periodic_audit_flags_failed_capture_handle_missing_raw_pull_trigger(tmp_path: Path) -> None:
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
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    cleaning_path = Path(smoke_outputs["cleaning_packet"])
    cleaning_payload = _load_json(cleaning_path)
    stripped_handle_count = 0
    for handle in cleaning_payload["handles"]:
        if any(
            reason.startswith("capture_validity_not_supported:")
            for reason in handle["warnings"]
        ):
            handle["raw_pull_triggers"] = []
            stripped_handle_count += 1
    assert stripped_handle_count
    _write_json(cleaning_path, cleaning_payload)
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "fail"
    assert any(
        finding["lane"] == "lane_a_existing_package"
        and finding["code"] == "cleaning_failed_capture_handle_raw_pull_trigger_missing"
        and finding["owner_candidate"] == "cleaning"
        and "capture_validity_not_supported:rendered_dom_error_or_block_page_marker"
        in finding["details"]["triggering_reasons"]
        for finding in report["findings"]
    )


def test_periodic_audit_accepts_failed_capture_handle_with_raw_pull_trigger(
    tmp_path: Path,
) -> None:
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
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert not any(
        finding["lane"] == "lane_a_existing_package"
        and finding["code"] == "cleaning_failed_capture_handle_raw_pull_trigger_missing"
        for finding in report["findings"]
    )


def test_periodic_audit_refuses_stale_rebuild_subdirectories(tmp_path: Path) -> None:
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
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )
    output_dir = tmp_path / "audit_outputs"
    (output_dir / "lane_b_projection_rebuild").mkdir(parents=True)

    with pytest.raises(ValueError, match="audit output already exists"):
        run_cleaning_spine_periodic_audit(
            audit_manifest_path=audit_manifest_path,
            output_dir=output_dir,
        )


def test_periodic_audit_main_returns_nonzero_for_warn_status(tmp_path: Path) -> None:
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
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    summary_path = Path(smoke_outputs["smoke_summary"])
    summary = _load_json(summary_path)
    summary["findings"] = [
        {
            "code": "retail_capture_validity_not_supported",
            "source_label": "retail:sephora",
            "packet_id": "01TESTRETAILSMOKE",
            "reasons": ["fixture_warn_only"],
        }
    ]
    _write_json(summary_path, summary)
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    exit_code = audit_runner.main(
        [
            "--audit-manifest",
            str(audit_manifest_path),
            "--output-dir",
            str(tmp_path / "audit_outputs"),
        ]
    )

    report = _load_json(
        tmp_path
        / "audit_outputs"
        / "cleaning_spine_periodic_audit_report.json"
    )
    assert report["overall_status"] == "warn"
    assert exit_code == 3
    assert any(
        finding["code"] == "lane_a_smoke_summary_finding"
        and finding["smoke_finding_code"] == "retail_capture_validity_not_supported"
        for finding in report["findings"]
    )


def test_periodic_audit_rejects_invalid_ecr_receipt_schema(tmp_path: Path) -> None:
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
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    ecr_path = Path(smoke_outputs["ecr_source_side_receipts"])
    ecr_payload = _load_json(ecr_path)
    del ecr_payload["receipts"][0]["postures"]["source_visibility"]
    _write_json(ecr_path, ecr_payload)
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "fail"
    assert any(
        finding["lane"] == "lane_a_existing_package"
        and finding["code"] == "lane_a_ecr_receipts_invalid"
        and "source_visibility" in finding["message"]
        for finding in report["findings"]
    )

def test_periodic_audit_flags_ecr_posture_content_drift(tmp_path: Path) -> None:
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
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    ecr_path = Path(smoke_outputs["ecr_source_side_receipts"])
    ecr_payload = _load_json(ecr_path)
    ecr_payload["receipts"][0]["postures"]["identity"][0]["fixture_extra_detail"] = (
        "ecr posture content drift"
    )
    _write_json(ecr_path, ecr_payload)
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "fail"
    assert any(
        finding["lane"] == "lane_b_cleaning_breakpoint"
        and finding["code"] == "ecr_rebuild_signature_mismatch"
        and finding["owner_candidate"] == "ecr"
        for finding in report["findings"]
    )


def test_periodic_audit_flags_cleaning_package_drift(tmp_path: Path) -> None:
    instagram_packet_dir = _write_instagram_packet_dir(tmp_path)
    instagram_projection_path = tmp_path / "instagram_projection" / "ig_projection.json"
    write_ig_creator_momentum_projection(
        packet_or_manifest_path=instagram_packet_dir,
        output_path=instagram_projection_path,
    )
    smoke_manifest_path = _write_smoke_manifest(
        tmp_path,
        instagram_handle="hyram",
        instagram_packet_dir=instagram_packet_dir,
        instagram_projection_path=instagram_projection_path,
    )
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    cleaning_path = Path(smoke_outputs["cleaning_packet"])
    cleaning_payload = _load_json(cleaning_path)
    cleaning_payload["handles"][0]["ecr_ref"]["ref_id"] = "ecr:wrong:source_side_postures"
    _write_json(cleaning_path, cleaning_payload)
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "fail"
    assert any(
        finding["lane"] == "lane_a_existing_package"
        and finding["code"] == "cleaning_handle_ecr_ref_unresolved"
        for finding in report["findings"]
    )
    assert any(
        finding["lane"] == "lane_b_cleaning_breakpoint"
        and finding["code"] == "cleaning_rebuild_signature_mismatch"
        and finding["owner_candidate"] == "cleaning"
        for finding in report["findings"]
    )


def test_periodic_audit_flags_capture_packet_hash_mismatch(tmp_path: Path) -> None:
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
    smoke_outputs = run_capture_ecr_cleaning_smoke(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=tmp_path / "smoke_outputs",
    )
    (retail_packet_dir / "raw" / "01_cloakbrowser_rendered_dom.html").write_text(
        "tampered after Lane A package creation",
        encoding="utf-8",
    )
    audit_manifest_path = _write_audit_manifest(
        tmp_path,
        smoke_manifest_path=smoke_manifest_path,
        smoke_outputs=smoke_outputs,
    )

    audit_outputs = run_cleaning_spine_periodic_audit(
        audit_manifest_path=audit_manifest_path,
        output_dir=tmp_path / "audit_outputs",
    )

    report = _load_json(Path(audit_outputs["audit_report_json"]))
    assert report["overall_status"] == "fail"
    assert any(
        finding["lane"] == "capture_preflight"
        and finding["code"] == "preserved_file_hash_mismatch"
        for finding in report["findings"]
    )


def _write_youtube_packet_dir(
    tmp_path: Path,
    *,
    video_id: str = "dQw4w9WgXcQ",
    lang: str = "en",
) -> Path:
    cues = [
        {"tStartMs": 1000, "dDurationMs": 2000, "segs": [{"utf8": "I really love the CeraVe moisturizer"}]},
        {"tStartMs": 3000, "dDurationMs": 2000, "segs": [{"utf8": "and the Paula's Choice BHA exfoliant"}]},
    ]
    json3_bytes = (json.dumps({"events": cues}, sort_keys=True) + "\n").encode("utf-8")
    cap = CaptionFetch(
        video_id=video_id,
        found=True,
        note="ok",
        lang=lang,
        caption_kind="manual",
        original_language_assumed=False,
        json3_bytes=json3_bytes,
        flat_text=(
            "CeraVe Hydrating Cleanser\n"
            "and the Paula's Choice BHA exfoliant"
        ),
        cue_count=len(cues),
        title="Skincare routine fixture",
        channel_id="UCfixturechannel",
        publish_date_iso="2024-08-01",
        duration_s=120,
        tooling={"fixture": "youtube_smoke"},
    )
    code, packet_dir = write_caption_packet(
        cap,
        output_directory=tmp_path / "youtube_packet",
        decision_question="What products does this creator mention?",
        now_iso="2026-06-16T20:32:17Z",
    )
    assert code == 0, packet_dir
    return Path(packet_dir)


def _write_smoke_manifest(
    tmp_path: Path,
    *,
    retail_packet_dir: Path | None = None,
    retail_projection_path: Path | None = None,
    reddit_packet_dir: Path | None = None,
    reddit_consolidation_path: Path | None = None,
    instagram_handle: str | None = None,
    instagram_packet_dir: Path | None = None,
    instagram_projection_path: Path | None = None,
    youtube_packet_dir: Path | None = None,
    youtube_source_label: str | None = None,
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
    if instagram_packet_dir is not None and instagram_projection_path is not None:
        manifest["instagram"] = [
            {
                "handle": instagram_handle or "instagram_fixture",
                "packet_dir": str(instagram_packet_dir),
                "projection_json": str(instagram_projection_path),
            }
        ]
    if youtube_packet_dir is not None:
        manifest["youtube"] = [
            {
                "source_label": youtube_source_label or "youtube:fixture",
                "packet_dir": str(youtube_packet_dir),
            }
        ]
    path = tmp_path / f"smoke_manifest_{len(list(tmp_path.glob('smoke_manifest_*.json')))}.json"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _write_audit_manifest(
    tmp_path: Path,
    *,
    smoke_manifest_path: Path,
    smoke_outputs: dict[str, str],
) -> Path:
    manifest = {
        "audit_id": "fixture_cleaning_periodic_audit",
        "smoke_manifest": str(smoke_manifest_path),
        "lane_a_outputs": {
            "ecr_source_side_receipts": smoke_outputs["ecr_source_side_receipts"],
            "cleaning_packet": smoke_outputs["cleaning_packet"],
            "smoke_summary": smoke_outputs["smoke_summary"],
        },
    }
    path = tmp_path / f"audit_manifest_{len(list(tmp_path.glob('audit_manifest_*.json')))}.json"
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _write_instagram_packet_dir(tmp_path: Path) -> Path:
    capture_time = "2026-06-16T20:32:17Z"
    profile_raw = {
        "profile_url": "https://www.instagram.com/hyram/",
        "stats": {"followers": "724K", "following": "2,339", "posts": "321"},
    }
    momentum_raw = {
        "username": "hyram",
        "numeric_id": "5802114508",
        "follower_count": 724000,
        "metric_registry_version": "ig_creator_momentum_metrics_v0",
        "identity_conflict_policy_version": "ig_numeric_id_username_policy_v0",
        "media": {
            "AAA": {
                "shortcode": "AAA",
                "is_video": False,
                "video_view_count": None,
                "like_count": 1693,
                "comment_count": 26,
                "caption": "caption omitted from projection rows",
                "taken_at_timestamp": 1722470400,
            }
        },
    }
    call_raw = {
        "url": "https://www.instagram.com/hyram/p/AAA/",
        "status": "captured",
        "likes": 1693,
        "comments": 26,
        "date": "August 1, 2024",
        "is_ad": False,
        "caption_truncated": False,
    }
    raw_file_bytes_by_file_id = {
        "file_01": json.dumps(profile_raw, sort_keys=True).encode("utf-8"),
        "file_02": json.dumps(momentum_raw, sort_keys=True).encode("utf-8"),
        "file_03": json.dumps(call_raw, sort_keys=True).encode("utf-8"),
    }
    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason(
            "profile slice is the enumeration source"
        ),
        source_edit_or_version=unknown_with_reason("not inferred"),
        capture_time=known_fact(capture_time),
        recapture_time=not_applicable("no prior capture"),
        cutoff_posture=unknown_with_reason("not supplied"),
    )
    call_timing = timing.model_copy(
        update={"source_publication_or_event": known_fact("August 1, 2024")}
    )
    packet = SourceCapturePacket(
        packet_id="01TESTIGSMOKE",
        manifest_version="source_capture_packet_manifest_v1",
        obligation_contract_version="core_spine_v0_data_capture_spine_obligation_contract_v0",
        source_family="instagram_creator",
        source_surface="ig_calls_browser_snapshot",
        source_locator=known_fact("https://www.instagram.com/hyram/"),
        requested_decision_context=known_fact("IG Cleaning smoke fixture."),
        capture_context=known_fact("logged-out IG wind-caller calls capture fixture"),
        actor_audience_context=known_fact("public creator fixture"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="capture_ecr_cleaning_smoke_test_operator",
        session_identity="01TESTIGSESSION",
        timing=timing,
        access_posture=known_fact("ig_logged_out_browser_snapshot"),
        archive_history_posture=not_attempted(
            "IG calls runner does not query archive or history services"
        ),
        media_modality_posture=known_fact("og:description and profile-feed JSON checked"),
        re_capture_relationship=not_applicable("no prior packet"),
        source_slices=[
            SourceCaptureSlice(
                slice_id="ig_profile_00",
                locator=known_fact("https://www.instagram.com/hyram/"),
                timing=timing,
                access_posture=known_fact("ig_logged_out_browser_snapshot"),
                archive_history_posture=not_attempted(
                    "IG calls runner does not query archive or history services"
                ),
                media_modality_posture=known_fact("og:description and profile-feed JSON checked"),
                re_capture_relationship=not_applicable("no prior packet"),
                preserved_file_ids=["file_01", "file_02"],
                metric_observations=[
                    MetricObservation(
                        metric="follower_count",
                        posture=MetricPosture.OBSERVED,
                        value=724000,
                        coverage_window=CoverageWindow(end=capture_time),
                    )
                ],
            ),
            SourceCaptureSlice(
                slice_id="ig_call_01",
                locator=known_fact("https://www.instagram.com/hyram/p/AAA/"),
                timing=call_timing,
                access_posture=known_fact("ig_logged_out_browser_snapshot"),
                archive_history_posture=not_attempted(
                    "IG calls runner does not query archive or history services"
                ),
                media_modality_posture=known_fact("og:description and profile-feed JSON checked"),
                re_capture_relationship=not_applicable("no prior packet"),
                preserved_file_ids=["file_03"],
                metric_observations=[
                    MetricObservation(
                        metric="like_count",
                        posture=MetricPosture.OBSERVED,
                        value=1693,
                        coverage_window=CoverageWindow(end=capture_time),
                    ),
                    MetricObservation(
                        metric="comment_count",
                        posture=MetricPosture.OBSERVED,
                        value=26,
                        coverage_window=CoverageWindow(end=capture_time),
                    ),
                    MetricObservation(
                        metric="view_count",
                        posture=MetricPosture.NOT_APPLICABLE,
                        reason="IG profile-feed JSON marks this media as non-video",
                        coverage_window=CoverageWindow(end=capture_time),
                    ),
                ],
            ),
        ],
        preserved_files=[
            _preserved_file(
                "file_01",
                "raw/01_ig_profile.json",
                raw_file_bytes_by_file_id["file_01"],
            ),
            _preserved_file(
                "file_02",
                "raw/02_ig_profile_momentum.json",
                raw_file_bytes_by_file_id["file_02"],
            ),
            _preserved_file(
                "file_03",
                "raw/03_ig_call_01.json",
                raw_file_bytes_by_file_id["file_03"],
            ),
        ],
        receipt_metadata=ReceiptMetadata(
            title="Source Capture Packet Receipt",
            generated_at="2026-06-16T20:33:46Z",
            summary="unit test IG source capture packet",
            non_claims=["not Cleaning", "not Judgment"],
        ),
    )
    packet_dir = tmp_path / "instagram_packet"
    for preserved_file in packet.preserved_files:
        file_path = packet_dir / preserved_file.relative_packet_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(raw_file_bytes_by_file_id[preserved_file.file_id])
    (packet_dir / "manifest.json").write_text(
        json.dumps(packet.model_dump(mode="json"), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return packet_dir


def _preserved_file(file_id: str, relative_path: str, body: bytes) -> PreservedFile:
    return PreservedFile(
        file_id=file_id,
        original_path=relative_path,
        relative_packet_path=relative_path,
        sha256=hashlib.sha256(body).hexdigest(),
        hash_basis="raw_stored_bytes",
        size_bytes=len(body),
    )


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
