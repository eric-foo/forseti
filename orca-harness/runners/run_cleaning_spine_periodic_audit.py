"""No-network periodic audit for the Cleaning spine smoke boundary.

The audit consumes frozen Source Capture packet, projection/consolidation, ECR,
and Cleaning artifacts. It does not run live capture, schedule itself, persist
to a data lake, or make Judgment/readiness claims.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable, Sequence

from pydantic import ValidationError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cleaning.models import CleaningPacket  # noqa: E402
from harness_utils import hash_file, utc_now_z  # noqa: E402
from runners.run_capture_ecr_cleaning_smoke import (  # noqa: E402
    CLEANING_OUTPUT_NAME,
    ECR_OUTPUT_NAME,
    SUMMARY_OUTPUT_NAME,
    run_capture_ecr_cleaning_smoke,
)
from source_capture.ig_projection import (  # noqa: E402
    IgCreatorMomentumProjectionPacket,
    write_ig_creator_momentum_projection,
)
from source_capture.models import SourceCapturePacket  # noqa: E402
from source_capture.reddit_consolidation import consolidate_reddit_packet  # noqa: E402
from source_capture.retail_pdp_projection import (  # noqa: E402
    RetailPdpProjectionPacket,
    write_retail_pdp_projection,
)


AUDIT_JSON_NAME = "cleaning_spine_periodic_audit_report.json"
AUDIT_MD_NAME = "cleaning_spine_periodic_audit_report.md"
LANE_B_PROJECTION_DIR = "lane_b_projection_rebuild"
LANE_B_CLEANING_DIR = "lane_b_cleaning_rebuild"

SCHEMA_VERSION = "cleaning_spine_periodic_audit_v0"
BLOCKING_SEVERITIES = frozenset({"blocker", "major"})
SUPPORTED_SOURCE_FAMILIES = ("retail", "reddit", "instagram")

NON_CLAIMS = [
    "not_live_capture",
    "not_capture_scheduler",
    "not_data_lake_storage",
    "not_dashboard",
    "not_product_proof",
    "not_judgment_readiness",
    "not_live_e2e_readiness",
]

_JUDGMENT_REASON_TOKENS = frozenset(
    {
        "action_ceiling",
        "action_supporting",
        "artificial_amplification",
        "credible",
        "credibility",
        "decision_strength",
        "demand",
        "discount",
        "discounted",
        "discounting",
        "excluded",
        "independent",
        "integrity",
        "salience",
        "signal_integrity",
        "signal_use",
        "strong",
        "supporting",
        "weak",
    }
)


def run_cleaning_spine_periodic_audit(
    audit_manifest_path: Path,
    output_dir: Path,
) -> dict[str, str]:
    """Run the bounded no-network Cleaning periodic audit."""

    manifest_path = audit_manifest_path.resolve()
    manifest = _load_json_object(manifest_path, "audit manifest")
    manifest_dir = manifest_path.parent
    smoke_manifest_path = _resolve_manifest_path(
        manifest_dir,
        manifest,
        "smoke_manifest",
        label="audit manifest",
    )
    smoke_manifest = _load_json_object(smoke_manifest_path, "smoke manifest")
    smoke_manifest_dir = smoke_manifest_path.parent

    output_dir = output_dir.resolve()
    output_paths = {
        "audit_report_json": output_dir / AUDIT_JSON_NAME,
        "audit_report_markdown": output_dir / AUDIT_MD_NAME,
    }
    generated_paths = [
        *output_paths.values(),
        output_dir / LANE_B_PROJECTION_DIR,
        output_dir / LANE_B_CLEANING_DIR,
    ]
    existing_outputs = [path for path in generated_paths if path.exists()]
    if existing_outputs:
        raise ValueError(
            "audit output already exists: "
            + ", ".join(str(path) for path in existing_outputs)
        )
    output_dir.mkdir(parents=True, exist_ok=True)

    generated_at = utc_now_z()
    findings: list[dict[str, Any]] = []
    packet_index: dict[str, dict[str, Any]] = {}

    source_entries = _source_entries(smoke_manifest, smoke_manifest_dir)
    if not source_entries:
        raise ValueError("smoke manifest must name at least one supported source entry")

    capture_preflight = _run_capture_preflight(
        source_entries=source_entries,
        packet_index=packet_index,
        findings=findings,
    )

    lane_a_outputs = _resolve_lane_a_outputs(
        manifest=manifest,
        manifest_dir=manifest_dir,
    )
    lane_a = _run_lane_a_existing_package_checks(
        lane_a_outputs=lane_a_outputs,
        packet_index=packet_index,
        source_entries=source_entries,
        findings=findings,
    )

    lane_b_projection = _run_lane_b_projection_breakpoint(
        source_entries=source_entries,
        output_dir=output_dir / LANE_B_PROJECTION_DIR,
        findings=findings,
    )

    lane_b_cleaning = _run_lane_b_cleaning_breakpoint(
        smoke_manifest_path=smoke_manifest_path,
        output_dir=output_dir / LANE_B_CLEANING_DIR,
        baseline_cleaning=lane_a.get("cleaning_packet"),
        baseline_ecr_receipts=lane_a.get("ecr_receipts"),
        findings=findings,
    )

    lane_statuses = {
        "capture_preflight": _lane_status("capture_preflight", findings),
        "lane_a_existing_package": _lane_status("lane_a_existing_package", findings),
        "lane_b_projection_breakpoint": _lane_status("lane_b_projection_breakpoint", findings),
        "lane_b_cleaning_breakpoint": _lane_status("lane_b_cleaning_breakpoint", findings),
    }
    overall_status = (
        "fail"
        if any(status == "fail" for status in lane_statuses.values())
        else "warn"
        if any(status == "warn" for status in lane_statuses.values())
        else "pass"
    )

    report = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "audit_id": manifest.get("audit_id"),
        "overall_status": overall_status,
        "lane_statuses": lane_statuses,
        "inputs": {
            "audit_manifest": str(manifest_path),
            "smoke_manifest": str(smoke_manifest_path),
            "lane_a_outputs": {key: str(path) for key, path in lane_a_outputs.items()},
        },
        "counts": {
            "source_entries": len(source_entries),
            "capture_packets_checked": capture_preflight["packets_checked"],
            "lane_a_cleaning_handles": lane_a.get("cleaning_handle_count", 0),
            "lane_b_projection_entries": lane_b_projection["entries_checked"],
            "lane_b_cleaning_handles": lane_b_cleaning.get("cleaning_handle_count", 0),
            "findings": len(findings),
            "blocking_findings": sum(
                1 for finding in findings if finding["severity"] in BLOCKING_SEVERITIES
            ),
        },
        "capture_preflight": capture_preflight,
        "lane_a_existing_package": _summary_without_objects(lane_a),
        "lane_b_projection_breakpoint": lane_b_projection,
        "lane_b_cleaning_breakpoint": lane_b_cleaning,
        "findings": findings,
        "non_claims": NON_CLAIMS,
    }

    _write_json(output_paths["audit_report_json"], report)
    output_paths["audit_report_markdown"].write_text(
        _render_markdown_report(report),
        encoding="utf-8",
        newline="\n",
    )

    return {key: str(path) for key, path in output_paths.items()}


def _run_capture_preflight(
    *,
    source_entries: Sequence[dict[str, Any]],
    packet_index: dict[str, dict[str, Any]],
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    packets_checked = 0
    packet_summaries: list[dict[str, Any]] = []
    for entry in source_entries:
        source_label = entry["source_label"]
        packet_dir = entry["packet_dir"]
        try:
            packet = _load_packet(packet_dir)
            packets_checked += 1
            _verify_packet_preserved_files(
                source_label=source_label,
                packet_dir=packet_dir,
                packet=packet,
                findings=findings,
            )
            packet_index[packet.packet_id] = {
                "packet": packet,
                "packet_dir": packet_dir,
                "source_label": source_label,
            }
            packet_summaries.append(
                {
                    "source_label": source_label,
                    "packet_id": packet.packet_id,
                    "packet_dir": str(packet_dir),
                    "source_family": packet.source_family,
                    "source_surface": packet.source_surface,
                    "source_slices": len(packet.source_slices),
                    "preserved_files": len(packet.preserved_files),
                }
            )
        except Exception as exc:
            _finding(
                findings,
                lane="capture_preflight",
                severity="blocker",
                code="capture_packet_preflight_failed",
                owner_candidate="capture_or_fixture",
                source_label=source_label,
                message=str(exc),
            )
    return {
        "packets_checked": packets_checked,
        "packet_summaries": packet_summaries,
    }


def _run_lane_a_existing_package_checks(
    *,
    lane_a_outputs: dict[str, Path],
    packet_index: dict[str, dict[str, Any]],
    source_entries: Sequence[dict[str, Any]],
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    try:
        ecr_receipts = _load_json_object(
            lane_a_outputs["ecr_source_side_receipts"],
            "Lane A ECR receipts",
        )
        result["ecr_receipts"] = ecr_receipts
        receipts = ecr_receipts.get("receipts")
        if not isinstance(receipts, list) or not receipts:
            raise ValueError("ECR receipts must contain a non-empty receipts list")
        result["ecr_receipt_count"] = len(receipts)
    except Exception as exc:
        _finding(
            findings,
            lane="lane_a_existing_package",
            severity="blocker",
            code="lane_a_ecr_receipts_invalid",
            owner_candidate="ecr_or_fixture",
            message=str(exc),
        )
        ecr_receipts = {"receipts": []}
        result["ecr_receipts"] = ecr_receipts

    try:
        cleaning_packet = CleaningPacket.model_validate(
            _load_json_object(lane_a_outputs["cleaning_packet"], "Lane A CleaningPacket")
        )
        result["cleaning_packet"] = cleaning_packet
        result["cleaning_handle_count"] = len(cleaning_packet.handles)
        projection_ref_packet_ids = {
            handle.projection_ref.packet_id
            for handle in cleaning_packet.handles
            if handle.projection_ref is not None
        }
        projection_row_index = _build_projection_row_index(
            source_entries=source_entries,
            packet_index=packet_index,
            needed_packet_ids=projection_ref_packet_ids,
            findings=findings,
            lane="lane_a_existing_package",
        )
        result["projection_ref_packets_checked"] = len(projection_row_index)
        _verify_cleaning_packet_traceability(
            cleaning_packet=cleaning_packet,
            ecr_receipts=ecr_receipts,
            packet_index=packet_index,
            projection_row_index=projection_row_index,
            findings=findings,
            lane="lane_a_existing_package",
        )
    except Exception as exc:
        _finding(
            findings,
            lane="lane_a_existing_package",
            severity="blocker",
            code="lane_a_cleaning_packet_invalid",
            owner_candidate="cleaning",
            message=str(exc),
        )

    summary_path = lane_a_outputs.get("smoke_summary")
    if summary_path is not None:
        try:
            summary = _load_json_object(summary_path, "Lane A smoke summary")
            result["smoke_summary_counts"] = summary.get("counts", {})
            summary_findings = summary.get("findings", [])
            if not isinstance(summary_findings, list):
                _finding(
                    findings,
                    lane="lane_a_existing_package",
                    severity="minor",
                    code="lane_a_smoke_summary_invalid",
                    owner_candidate="audit_fixture",
                    message="Lane A smoke summary findings field is not a list.",
                )
                result["smoke_summary_finding_count"] = 0
            else:
                result["smoke_summary_finding_count"] = len(summary_findings)
                _promote_smoke_summary_findings(
                    summary_findings=summary_findings,
                    findings=findings,
                )
        except Exception as exc:
            _finding(
                findings,
                lane="lane_a_existing_package",
                severity="minor",
                code="lane_a_smoke_summary_invalid",
                owner_candidate="audit_fixture",
                message=str(exc),
            )

    pairs_path = lane_a_outputs.get("raw_cleaned_pairs")
    if pairs_path is not None:
        _verify_raw_cleaned_pairs(pairs_path=pairs_path, findings=findings)

    return result


def _run_lane_b_projection_breakpoint(
    *,
    source_entries: Sequence[dict[str, Any]],
    output_dir: Path,
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    entries: list[dict[str, Any]] = []
    for index, entry in enumerate(source_entries, start=1):
        source_type = entry["source_type"]
        source_label = entry["source_label"]
        try:
            if source_type == "retail":
                original = RetailPdpProjectionPacket.model_validate(
                    _load_json_object(entry["projection_json"], f"{source_label} projection")
                )
                rebuilt_path = output_dir / f"{index:02d}_retail_projection.json"
                rebuilt = write_retail_pdp_projection(
                    packet_directory=entry["packet_dir"],
                    output_path=rebuilt_path,
                )
                original_signature = _projection_signature(original)
                rebuilt_signature = _projection_signature(rebuilt)
            elif source_type == "instagram":
                original = IgCreatorMomentumProjectionPacket.model_validate(
                    _load_json_object(entry["projection_json"], f"{source_label} projection")
                )
                rebuilt_path = output_dir / f"{index:02d}_instagram_projection.json"
                rebuilt = write_ig_creator_momentum_projection(
                    packet_or_manifest_path=entry["packet_dir"],
                    output_path=rebuilt_path,
                )
                original_signature = _projection_signature(original)
                rebuilt_signature = _projection_signature(rebuilt)
            elif source_type == "reddit":
                rebuilt_dir = output_dir / f"{index:02d}_reddit_consolidation"
                rebuilt_result = consolidate_reddit_packet(
                    packet_or_manifest_path=entry["packet_dir"],
                    output_directory=rebuilt_dir,
                )
                rebuilt_path = Path(rebuilt_result["json_path"])
                original_signature = _reddit_consolidation_signature(
                    _load_json_object(
                        entry["consolidation_json"],
                        f"{source_label} consolidation",
                    )
                )
                rebuilt_signature = _reddit_consolidation_signature(
                    _load_json_object(rebuilt_path, f"{source_label} rebuilt consolidation")
                )
            else:
                raise ValueError(f"unsupported source type: {source_type}")

            match = original_signature == rebuilt_signature
            if not match:
                _finding(
                    findings,
                    lane="lane_b_projection_breakpoint",
                    severity="major",
                    code="projection_rebuild_signature_mismatch",
                    owner_candidate="projection_or_consolidation",
                    source_label=source_label,
                    message="Regenerated projection/consolidation signature differs from frozen artifact.",
                    details={
                        "original_signature": original_signature,
                        "rebuilt_signature": rebuilt_signature,
                    },
                )
            entries.append(
                {
                    "source_label": source_label,
                    "source_type": source_type,
                    "rebuilt_path": str(rebuilt_path),
                    "signature_match": match,
                }
            )
        except Exception as exc:
            _finding(
                findings,
                lane="lane_b_projection_breakpoint",
                severity="major",
                code="projection_rebuild_failed",
                owner_candidate="projection_or_consolidation",
                source_label=source_label,
                message=str(exc),
            )
    return {
        "entries_checked": len(entries),
        "entries": entries,
        "output_dir": str(output_dir),
    }


def _run_lane_b_cleaning_breakpoint(
    *,
    smoke_manifest_path: Path,
    output_dir: Path,
    baseline_cleaning: Any,
    baseline_ecr_receipts: Any,
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    try:
        outputs = run_capture_ecr_cleaning_smoke(
            smoke_manifest_path=smoke_manifest_path,
            output_dir=output_dir,
        )
        rebuilt_cleaning = CleaningPacket.model_validate(
            _load_json_object(Path(outputs["cleaning_packet"]), "rebuilt CleaningPacket")
        )
        rebuilt_ecr = _load_json_object(Path(outputs["ecr_source_side_receipts"]), "rebuilt ECR receipts")
        result: dict[str, Any] = {
            "output_dir": str(output_dir),
            "outputs": outputs,
            "cleaning_handle_count": len(rebuilt_cleaning.handles),
        }
        if isinstance(baseline_cleaning, CleaningPacket):
            match = _cleaning_signature(baseline_cleaning) == _cleaning_signature(rebuilt_cleaning)
            result["cleaning_signature_match"] = match
            if not match:
                _finding(
                    findings,
                    lane="lane_b_cleaning_breakpoint",
                    severity="major",
                    code="cleaning_rebuild_signature_mismatch",
                    owner_candidate="cleaning",
                    message="Rebuilt CleaningPacket stable handle signature differs from Lane A artifact.",
                )
        if isinstance(baseline_ecr_receipts, dict):
            ecr_match = _ecr_signature(baseline_ecr_receipts) == _ecr_signature(rebuilt_ecr)
            result["ecr_signature_match"] = ecr_match
            if not ecr_match:
                _finding(
                    findings,
                    lane="lane_b_cleaning_breakpoint",
                    severity="major",
                    code="ecr_rebuild_signature_mismatch",
                    owner_candidate="ecr",
                    message="Rebuilt ECR receipt signature differs from Lane A artifact.",
                )
        return result
    except Exception as exc:
        _finding(
            findings,
            lane="lane_b_cleaning_breakpoint",
            severity="major",
            code="cleaning_rebuild_failed",
            owner_candidate="cleaning",
            message=str(exc),
        )
        return {
            "output_dir": str(output_dir),
            "cleaning_handle_count": 0,
        }


def _verify_packet_preserved_files(
    *,
    source_label: str,
    packet_dir: Path,
    packet: SourceCapturePacket,
    findings: list[dict[str, Any]],
) -> None:
    preserved_by_id = {item.file_id: item for item in packet.preserved_files}
    for source_slice in packet.source_slices:
        for file_id in source_slice.preserved_file_ids:
            if file_id not in preserved_by_id:
                _finding(
                    findings,
                    lane="capture_preflight",
                    severity="blocker",
                    code="slice_preserved_file_missing_from_manifest",
                    owner_candidate="capture_or_fixture",
                    source_label=source_label,
                    packet_id=packet.packet_id,
                    slice_id=source_slice.slice_id,
                    file_id=file_id,
                    message="Source slice references a file_id absent from preserved_files.",
                )
    for preserved_file in packet.preserved_files:
        try:
            raw_path = _contained_packet_path(packet_dir, preserved_file.relative_packet_path)
            actual_sha256 = hash_file(raw_path)
            if actual_sha256 != preserved_file.sha256:
                _finding(
                    findings,
                    lane="capture_preflight",
                    severity="blocker",
                    code="preserved_file_hash_mismatch",
                    owner_candidate="capture_or_fixture",
                    source_label=source_label,
                    packet_id=packet.packet_id,
                    file_id=preserved_file.file_id,
                    message="Preserved file bytes do not match packet manifest sha256.",
                    details={
                        "expected_sha256": preserved_file.sha256,
                        "actual_sha256": actual_sha256,
                    },
                )
        except Exception as exc:
            _finding(
                findings,
                lane="capture_preflight",
                severity="blocker",
                code="preserved_file_unreadable",
                owner_candidate="capture_or_fixture",
                source_label=source_label,
                packet_id=packet.packet_id,
                file_id=preserved_file.file_id,
                message=str(exc),
            )



def _build_projection_row_index(
    *,
    source_entries: Sequence[dict[str, Any]],
    packet_index: dict[str, dict[str, Any]],
    needed_packet_ids: set[str],
    findings: list[dict[str, Any]],
    lane: str,
) -> dict[str, dict[str, str]]:
    row_index: dict[str, dict[str, str]] = {}
    if not needed_packet_ids:
        return row_index
    source_label_packet_ids = {
        str(record.get("source_label")): packet_id
        for packet_id, record in packet_index.items()
    }
    for entry in source_entries:
        packet_id = source_label_packet_ids.get(entry["source_label"])
        if packet_id not in needed_packet_ids:
            continue
        try:
            if entry["source_type"] == "retail":
                projection = RetailPdpProjectionPacket.model_validate(
                    _load_json_object(entry["projection_json"], f"{entry['source_label']} projection")
                )
                if projection.packet_id != packet_id:
                    raise ValueError(
                        f"projection packet_id {projection.packet_id!r} does not match "
                        f"packet {packet_id!r}"
                    )
                row_index[packet_id] = {
                    row.row_id: str(row.row_kind)
                    for row in projection.rows
                }
            elif entry["source_type"] == "instagram":
                projection = IgCreatorMomentumProjectionPacket.model_validate(
                    _load_json_object(entry["projection_json"], f"{entry['source_label']} projection")
                )
                if projection.packet_id != packet_id:
                    raise ValueError(
                        f"projection packet_id {projection.packet_id!r} does not match "
                        f"packet {packet_id!r}"
                    )
                row_index[packet_id] = {
                    row.row_id: str(row.row_kind)
                    for row in projection.rows
                }
            elif entry["source_type"] == "reddit":
                artifact = _load_json_object(
                    entry["consolidation_json"],
                    f"{entry['source_label']} consolidation",
                )
                consolidation = artifact.get("reddit_thread_consolidation")
                if not isinstance(consolidation, dict):
                    raise ValueError("reddit consolidation missing reddit_thread_consolidation")
                source_packet = consolidation.get("source_packet")
                if not isinstance(source_packet, dict) or source_packet.get("packet_id") != packet_id:
                    raise ValueError("reddit consolidation packet_id does not match packet")
                rows: dict[str, str] = {}
                if isinstance(consolidation.get("post"), dict):
                    rows["post"] = "post"
                comments = consolidation.get("comments", [])
                if comments is None:
                    comments = []
                if not isinstance(comments, list):
                    raise ValueError("reddit consolidation comments must be a list")
                for comment_index, comment in enumerate(comments, start=1):
                    if not isinstance(comment, dict):
                        raise ValueError("reddit consolidation comment must be an object")
                    row_id = comment.get("row_id")
                    if not isinstance(row_id, str) or not row_id.strip():
                        row_id = f"comment_{comment_index:04d}"
                    rows[row_id] = "comment"
                row_index[packet_id] = rows
            else:
                raise ValueError(f"unsupported source type: {entry['source_type']}")
        except Exception as exc:
            _finding(
                findings,
                lane=lane,
                severity="major",
                code="projection_row_index_unavailable",
                owner_candidate="projection_or_fixture",
                source_label=entry["source_label"],
                packet_id=packet_id,
                message=str(exc),
            )
    return row_index


def _verify_cleaning_projection_ref(
    *,
    handle_id: str,
    projection_ref: dict[str, Any] | None,
    projection_row_index: dict[str, dict[str, str]],
    findings: list[dict[str, Any]],
    lane: str,
) -> None:
    if projection_ref is None:
        return
    packet_id = projection_ref["packet_id"]
    row_id = projection_ref.get("row_id")
    if not isinstance(row_id, str) or not row_id.strip():
        _finding(
            findings,
            lane=lane,
            severity="major",
            code="cleaning_projection_ref_row_missing",
            owner_candidate="cleaning",
            packet_id=packet_id,
            handle_id=handle_id,
            message="Cleaning projection_ref is missing row_id.",
        )
        return
    packet_rows = projection_row_index.get(packet_id)
    if packet_rows is None:
        _finding(
            findings,
            lane=lane,
            severity="major",
            code="cleaning_projection_ref_packet_unresolved",
            owner_candidate="cleaning_or_projection",
            packet_id=packet_id,
            handle_id=handle_id,
            message="Cleaning projection_ref packet_id has no indexed projection artifact.",
        )
        return
    actual_row_kind = packet_rows.get(row_id)
    if actual_row_kind is None:
        _finding(
            findings,
            lane=lane,
            severity="major",
            code="cleaning_projection_ref_row_unresolved",
            owner_candidate="cleaning_or_projection",
            packet_id=packet_id,
            handle_id=handle_id,
            message="Cleaning projection_ref row_id is absent from the indexed projection artifact.",
            details={"row_id": row_id},
        )
        return
    expected_row_kind = projection_ref.get("row_kind")
    if isinstance(expected_row_kind, str) and expected_row_kind and expected_row_kind != actual_row_kind:
        _finding(
            findings,
            lane=lane,
            severity="major",
            code="cleaning_projection_ref_row_kind_mismatch",
            owner_candidate="cleaning_or_projection",
            packet_id=packet_id,
            handle_id=handle_id,
            message="Cleaning projection_ref row_kind differs from indexed projection artifact.",
            details={
                "row_id": row_id,
                "projection_ref_row_kind": expected_row_kind,
                "indexed_row_kind": actual_row_kind,
            },
        )


def _verify_cleaning_packet_traceability(
    *,
    cleaning_packet: CleaningPacket,
    ecr_receipts: dict[str, Any],
    packet_index: dict[str, dict[str, Any]],
    projection_row_index: dict[str, dict[str, str]],
    findings: list[dict[str, Any]],
    lane: str,
) -> None:
    receipt_keys = {
        (receipt.get("packet_id"), receipt.get("ref_id"))
        for receipt in ecr_receipts.get("receipts", [])
        if isinstance(receipt, dict)
    }
    for handle in cleaning_packet.handles:
        if handle.relation.value != "keyed_siblings_over_raw":
            _finding(
                findings,
                lane=lane,
                severity="major",
                code="cleaning_handle_relation_drift",
                owner_candidate="cleaning",
                packet_id=handle.raw_anchor.packet_id,
                handle_id=handle.handle_id,
                message="Cleaning handle relation is not keyed_siblings_over_raw.",
            )
        if handle.ecr_ref is None:
            _finding(
                findings,
                lane=lane,
                severity="major",
                code="cleaning_handle_ecr_ref_missing",
                owner_candidate="cleaning",
                packet_id=handle.raw_anchor.packet_id,
                handle_id=handle.handle_id,
                message="Cleaning handle has no ECR ref.",
            )
        elif (handle.ecr_ref.packet_id, handle.ecr_ref.ref_id) not in receipt_keys:
            _finding(
                findings,
                lane=lane,
                severity="major",
                code="cleaning_handle_ecr_ref_unresolved",
                owner_candidate="cleaning_or_ecr",
                packet_id=handle.raw_anchor.packet_id,
                handle_id=handle.handle_id,
                message="Cleaning handle ECR ref does not resolve to Lane A receipt.",
            )
        _verify_cleaning_projection_ref(
            handle_id=handle.handle_id,
            projection_ref=(
                handle.projection_ref.model_dump(mode="json")
                if handle.projection_ref is not None
                else None
            ),
            projection_row_index=projection_row_index,
            findings=findings,
            lane=lane,
        )
        _verify_cleaning_raw_anchor(
            handle_id=handle.handle_id,
            raw_anchor=handle.raw_anchor.model_dump(mode="json"),
            packet_index=packet_index,
            findings=findings,
            lane=lane,
        )
        _verify_no_judgment_reason_tokens(
            handle_id=handle.handle_id,
            values=[
                *handle.residuals,
                *handle.warnings,
                *handle.raw_pull_triggers,
            ],
            findings=findings,
            lane=lane,
        )


def _verify_cleaning_raw_anchor(
    *,
    handle_id: str,
    raw_anchor: dict[str, Any],
    packet_index: dict[str, dict[str, Any]],
    findings: list[dict[str, Any]],
    lane: str,
) -> None:
    packet_id = raw_anchor["packet_id"]
    packet_record = packet_index.get(packet_id)
    if packet_record is None:
        _finding(
            findings,
            lane=lane,
            severity="major",
            code="cleaning_raw_anchor_packet_unresolved",
            owner_candidate="cleaning_or_fixture",
            packet_id=packet_id,
            handle_id=handle_id,
            message="Cleaning raw anchor packet_id is absent from audit packet index.",
        )
        return

    packet: SourceCapturePacket = packet_record["packet"]
    packet_dir: Path = packet_record["packet_dir"]
    preserved_by_id = {item.file_id: item for item in packet.preserved_files}
    slice_by_id = {source_slice.slice_id: source_slice for source_slice in packet.source_slices}
    source_slice = slice_by_id.get(raw_anchor["slice_id"])
    if source_slice is None:
        _finding(
            findings,
            lane=lane,
            severity="major",
            code="cleaning_raw_anchor_slice_unresolved",
            owner_candidate="cleaning_or_fixture",
            packet_id=packet_id,
            handle_id=handle_id,
            slice_id=raw_anchor["slice_id"],
            message="Cleaning raw anchor slice_id is absent from packet.",
        )
        return
    preserved_file = preserved_by_id.get(raw_anchor["file_id"])
    if preserved_file is None:
        _finding(
            findings,
            lane=lane,
            severity="major",
            code="cleaning_raw_anchor_file_unresolved",
            owner_candidate="cleaning_or_fixture",
            packet_id=packet_id,
            handle_id=handle_id,
            file_id=raw_anchor["file_id"],
            message="Cleaning raw anchor file_id is absent from packet preserved_files.",
        )
        return
    if preserved_file.relative_packet_path != raw_anchor["relative_packet_path"]:
        _finding(
            findings,
            lane=lane,
            severity="major",
            code="cleaning_raw_anchor_path_mismatch",
            owner_candidate="cleaning_or_fixture",
            packet_id=packet_id,
            handle_id=handle_id,
            file_id=preserved_file.file_id,
            message="Cleaning raw anchor relative path differs from packet manifest.",
        )
    try:
        raw_path = _contained_packet_path(packet_dir, preserved_file.relative_packet_path)
        actual_sha256 = hash_file(raw_path)
        if actual_sha256 != raw_anchor["sha256"]:
            _finding(
                findings,
                lane=lane,
                severity="major",
                code="cleaning_raw_anchor_hash_mismatch",
                owner_candidate="cleaning_or_fixture",
                packet_id=packet_id,
                handle_id=handle_id,
                file_id=preserved_file.file_id,
                message="Cleaning raw anchor sha256 differs from preserved bytes.",
            )
        _verify_anchor_specificity(
            handle_id=handle_id,
            raw_anchor=raw_anchor,
            raw_path=raw_path,
            findings=findings,
            lane=lane,
        )
    except Exception as exc:
        _finding(
            findings,
            lane=lane,
            severity="major",
            code="cleaning_raw_anchor_file_unreadable",
            owner_candidate="cleaning_or_fixture",
            packet_id=packet_id,
            handle_id=handle_id,
            file_id=preserved_file.file_id,
            message=str(exc),
        )


def _verify_anchor_specificity(
    *,
    handle_id: str,
    raw_anchor: dict[str, Any],
    raw_path: Path,
    findings: list[dict[str, Any]],
    lane: str,
) -> None:
    anchor_kind = raw_anchor["anchor_kind"]
    if anchor_kind == "file":
        return
    if anchor_kind == "json_pointer":
        pointer = raw_anchor.get("json_pointer")
        try:
            payload = json.loads(raw_path.read_text(encoding="utf-8"))
            _resolve_json_pointer(payload, pointer)
        except Exception as exc:
            _finding(
                findings,
                lane=lane,
                severity="major",
                code="cleaning_json_pointer_anchor_unresolved",
                owner_candidate="cleaning_or_projection",
                packet_id=raw_anchor["packet_id"],
                handle_id=handle_id,
                message=str(exc),
            )
        return
    anchor_value = raw_anchor.get("anchor_value")
    if not isinstance(anchor_value, str) or not anchor_value.strip():
        _finding(
            findings,
            lane=lane,
            severity="major",
            code="cleaning_specific_anchor_value_missing",
            owner_candidate="cleaning_or_projection",
            packet_id=raw_anchor["packet_id"],
            handle_id=handle_id,
            message=f"{anchor_kind} anchor has no anchor_value.",
        )
        return
    raw_bytes = raw_path.read_bytes()
    issue = _specific_anchor_issue(
        anchor_kind=anchor_kind,
        anchor_value=anchor_value,
        raw_bytes=raw_bytes,
    )
    if issue is not None:
        details = {
            "anchor_kind": anchor_kind,
            "anchor_value": anchor_value,
            **issue.get("details", {}),
        }
        _finding(
            findings,
            lane=lane,
            severity=issue["severity"],
            code=issue["code"],
            owner_candidate="cleaning_or_projection",
            packet_id=raw_anchor["packet_id"],
            handle_id=handle_id,
            message=issue["message"],
            details=details,
        )


def _specific_anchor_issue(
    *,
    anchor_kind: str,
    anchor_value: str,
    raw_bytes: bytes,
) -> dict[str, Any] | None:
    if anchor_kind == "text_pattern":
        occurrence_count = raw_bytes.count(anchor_value.encode("utf-8"))
        if occurrence_count == 0:
            return {
                "severity": "major",
                "code": "cleaning_specific_anchor_unresolved",
                "message": "text_pattern_absent_from_raw",
            }
        if occurrence_count > 1:
            return {
                "severity": "minor",
                "code": "cleaning_text_pattern_anchor_ambiguous",
                "message": "text_pattern_ambiguous_in_raw",
                "details": {"occurrence_count": occurrence_count},
            }
        return None
    if anchor_kind == "html_selector":
        selector_ids = [match.group(1) for match in re.finditer(r"#([A-Za-z0-9_-]+)", anchor_value)]
        raw_lower = raw_bytes.lower()
        if selector_ids:
            for selector_id in selector_ids:
                escaped = re.escape(selector_id).encode("ascii")
                pattern = rb"(?:id|name)\s*=\s*['\"]" + escaped + rb"['\"]"
                if re.search(pattern.lower(), raw_lower):
                    return None
            return {
                "severity": "major",
                "code": "cleaning_specific_anchor_unresolved",
                "message": "html_selector_id_or_name_absent_from_raw",
            }
        if anchor_value.encode("utf-8") in raw_bytes:
            return None
        return {
            "severity": "major",
            "code": "cleaning_specific_anchor_unresolved",
            "message": "html_selector_literal_absent_from_raw",
        }
    if anchor_kind == "script_index":
        raw_lower = raw_bytes.lower()
        anchor_lower = anchor_value.lower()
        probes: list[bytes] = []
        if "apollo" in anchor_lower:
            probes.append(b"window.__apollo_state__")
        if "ld_json" in anchor_lower or "ld-json" in anchor_lower or "json" in anchor_lower:
            probes.append(b"application/ld+json")
        if not probes:
            probes.append(anchor_value.encode("utf-8").lower())
        if any(probe in raw_lower for probe in probes):
            return None
        return {
            "severity": "major",
            "code": "cleaning_specific_anchor_unresolved",
            "message": "script_anchor_substrate_absent_from_raw",
        }
    return {
        "severity": "major",
        "code": "cleaning_specific_anchor_unresolved",
        "message": "unsupported_specific_anchor_kind",
    }


def _promote_smoke_summary_findings(
    *,
    summary_findings: Sequence[Any],
    findings: list[dict[str, Any]],
) -> None:
    for index, summary_finding in enumerate(summary_findings, start=1):
        if not isinstance(summary_finding, dict):
            _finding(
                findings,
                lane="lane_a_existing_package",
                severity="minor",
                code="lane_a_smoke_summary_invalid",
                owner_candidate="audit_fixture",
                message=f"Lane A smoke summary finding {index} is not an object.",
            )
            continue
        smoke_code = summary_finding.get("code")
        source_label = summary_finding.get("source_label")
        packet_id = summary_finding.get("packet_id")
        message_code = smoke_code if isinstance(smoke_code, str) and smoke_code else "unknown_smoke_finding"
        _finding(
            findings,
            lane="lane_a_existing_package",
            severity="minor",
            code="lane_a_smoke_summary_finding",
            owner_candidate=_smoke_finding_owner_candidate(message_code),
            source_label=source_label,
            packet_id=packet_id,
            message=(
                f"Lane A smoke summary reported {message_code}; "
                "periodic audit cannot report a clean pass."
            ),
            smoke_finding_code=message_code,
            details={"smoke_finding": _stable_signature_payload(summary_finding)},
        )


def _smoke_finding_owner_candidate(smoke_code: str) -> str:
    if smoke_code.endswith("capture_validity_not_supported"):
        return "capture_or_fixture"
    if "row_anchor" in smoke_code or "anchor" in smoke_code:
        return "projection_or_capture"
    if "structure_not_preserved" in smoke_code:
        return "projection"
    return "capture_projection_cleaning_or_fixture"


def _verify_raw_cleaned_pairs(
    *,
    pairs_path: Path,
    findings: list[dict[str, Any]],
) -> None:
    try:
        payload = json.loads(pairs_path.read_text(encoding="utf-8"))
    except Exception as exc:
        _finding(
            findings,
            lane="lane_a_existing_package",
            severity="major",
            code="raw_cleaned_pairs_unreadable",
            owner_candidate="review_wrapper",
            message=str(exc),
        )
        return
    pairs = payload.get("pairs") if isinstance(payload, dict) else payload
    if not isinstance(pairs, list):
        _finding(
            findings,
            lane="lane_a_existing_package",
            severity="major",
            code="raw_cleaned_pairs_shape_invalid",
            owner_candidate="review_wrapper",
            message="raw_cleaned_pairs must be a list or an object with a pairs list.",
        )
        return
    missing_relation = 0
    for pair in pairs:
        if not isinstance(pair, dict):
            continue
        relation = pair.get("relation")
        cleaned = pair.get("cleaned")
        if relation is None and isinstance(cleaned, dict):
            relation = cleaned.get("relation")
        if relation != "keyed_siblings_over_raw":
            missing_relation += 1
    if missing_relation:
        _finding(
            findings,
            lane="lane_a_existing_package",
            severity="major",
            code="raw_cleaned_pairs_relation_missing",
            owner_candidate="review_wrapper",
            message="raw_cleaned_pairs entries are missing keyed_siblings_over_raw relation.",
            details={"missing_relation_count": missing_relation},
        )


def _verify_no_judgment_reason_tokens(
    *,
    handle_id: str,
    values: Iterable[str],
    findings: list[dict[str, Any]],
    lane: str,
) -> None:
    for value in values:
        tokens = _judgment_reason_tokens(value)
        if tokens:
            _finding(
                findings,
                lane=lane,
                severity="major",
                code="judgment_vocabulary_in_cleaning_reason",
                owner_candidate="cleaning",
                handle_id=handle_id,
                message="Cleaning reason field contains Judgment-owned vocabulary.",
                details={"value": value, "tokens": tokens},
            )


def _judgment_reason_tokens(value: str) -> list[str]:
    normalized = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    padded = f"_{normalized}_"
    return sorted(token for token in _JUDGMENT_REASON_TOKENS if f"_{token}_" in padded)


def _projection_signature(projection: Any) -> dict[str, Any]:
    return _stable_signature_payload(projection.model_dump(mode="json"))


def _reddit_consolidation_signature(artifact: dict[str, Any]) -> dict[str, Any]:
    consolidation = artifact.get("reddit_thread_consolidation")
    if not isinstance(consolidation, dict):
        raise ValueError("reddit consolidation missing reddit_thread_consolidation")
    return _stable_signature_payload(consolidation)


_VOLATILE_SIGNATURE_KEYS = frozenset(
    {
        "generated_at",
        "operator_supplied_packet_path",
        "manifest_path",
        "packet_path",
        "packet_dir",
    }
)


def _stable_signature_payload(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    if isinstance(value, dict):
        return {
            key: _stable_signature_payload(item)
            for key, item in sorted(value.items())
            if key not in _VOLATILE_SIGNATURE_KEYS
        }
    if isinstance(value, list):
        return [_stable_signature_payload(item) for item in value]
    if isinstance(value, tuple):
        return [_stable_signature_payload(item) for item in value]
    return value


def _cleaning_signature(cleaning_packet: CleaningPacket) -> list[dict[str, Any]]:
    signature: list[dict[str, Any]] = []
    for handle in cleaning_packet.handles:
        signature.append(
            {
                "handle_id": handle.handle_id,
                "raw_anchor": handle.raw_anchor.model_dump(mode="json"),
                "projection_ref": (
                    handle.projection_ref.model_dump(mode="json")
                    if handle.projection_ref is not None
                    else None
                ),
                "ecr_ref": (
                    handle.ecr_ref.model_dump(mode="json")
                    if handle.ecr_ref is not None
                    else None
                ),
                "relation": handle.relation.value,
                "residuals": handle.residuals,
                "warnings": handle.warnings,
                "raw_pull_triggers": handle.raw_pull_triggers,
            }
        )
    return sorted(signature, key=lambda item: item["handle_id"])


def _ecr_signature(ecr_receipts: dict[str, Any]) -> list[dict[str, Any]]:
    signature: list[dict[str, Any]] = []
    for receipt in ecr_receipts.get("receipts", []):
        if not isinstance(receipt, dict):
            continue
        signature.append(_stable_signature_payload(receipt))
    return sorted(
        signature,
        key=lambda item: (
            str(item.get("packet_id")),
            str(item.get("ref_id")),
            str(item.get("source_label")),
        ),
    )


def _source_entries(
    smoke_manifest: dict[str, Any],
    smoke_manifest_dir: Path,
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for source_type in SUPPORTED_SOURCE_FAMILIES:
        raw_entries = smoke_manifest.get(source_type, [])
        if raw_entries is None:
            continue
        if not isinstance(raw_entries, list):
            raise ValueError(f"smoke manifest field {source_type!r} must be a list")
        for index, entry in enumerate(raw_entries, start=1):
            if not isinstance(entry, dict):
                raise ValueError(f"smoke manifest {source_type}[{index}] must be an object")
            packet_dir = _resolve_manifest_path(
                smoke_manifest_dir,
                entry,
                "packet_dir",
                label=f"{source_type}[{index}]",
            )
            source_label = _source_label(source_type=source_type, entry=entry, index=index)
            normalized = {
                "source_type": source_type,
                "source_label": source_label,
                "packet_dir": packet_dir,
            }
            if source_type in {"retail", "instagram"}:
                normalized["projection_json"] = _resolve_manifest_path(
                    smoke_manifest_dir,
                    entry,
                    "projection_json",
                    label=f"{source_type}[{index}]",
                )
            if source_type == "reddit":
                normalized["consolidation_json"] = _resolve_manifest_path(
                    smoke_manifest_dir,
                    entry,
                    "consolidation_json",
                    label=f"{source_type}[{index}]",
                )
            entries.append(normalized)
    return entries


def _source_label(*, source_type: str, entry: dict[str, Any], index: int) -> str:
    value = entry.get("source_label")
    if isinstance(value, str) and value.strip():
        return value.strip()
    if source_type == "retail":
        retailer = entry.get("retailer")
        return f"retail:{retailer.strip()}" if isinstance(retailer, str) and retailer.strip() else f"retail:{index}"
    if source_type == "instagram":
        handle = entry.get("handle")
        return f"instagram:{handle.strip()}" if isinstance(handle, str) and handle.strip() else f"instagram:{index}"
    return f"reddit:{index}"


def _resolve_lane_a_outputs(
    *,
    manifest: dict[str, Any],
    manifest_dir: Path,
) -> dict[str, Path]:
    if "lane_a_outputs" in manifest:
        outputs = manifest["lane_a_outputs"]
        if not isinstance(outputs, dict):
            raise ValueError("audit manifest lane_a_outputs must be an object")
        resolved = {
            "ecr_source_side_receipts": _resolve_manifest_path(
                manifest_dir,
                outputs,
                "ecr_source_side_receipts",
                label="lane_a_outputs",
            ),
            "cleaning_packet": _resolve_manifest_path(
                manifest_dir,
                outputs,
                "cleaning_packet",
                label="lane_a_outputs",
            ),
        }
        if "smoke_summary" in outputs:
            resolved["smoke_summary"] = _resolve_manifest_path(
                manifest_dir,
                outputs,
                "smoke_summary",
                label="lane_a_outputs",
            )
        if "raw_cleaned_pairs" in outputs:
            resolved["raw_cleaned_pairs"] = _resolve_manifest_path(
                manifest_dir,
                outputs,
                "raw_cleaned_pairs",
                label="lane_a_outputs",
            )
        return resolved

    smoke_output_dir = _resolve_manifest_path(
        manifest_dir,
        manifest,
        "smoke_output_dir",
        label="audit manifest",
    )
    return {
        "ecr_source_side_receipts": smoke_output_dir / ECR_OUTPUT_NAME,
        "cleaning_packet": smoke_output_dir / CLEANING_OUTPUT_NAME,
        "smoke_summary": smoke_output_dir / SUMMARY_OUTPUT_NAME,
    }


def _resolve_json_pointer(payload: Any, pointer: str | None) -> Any:
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError(f"invalid JSON pointer: {pointer!r}")
    current = payload
    for raw_part in pointer.lstrip("/").split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            if part not in current:
                raise ValueError(f"JSON pointer segment {part!r} not found")
            current = current[part]
        elif isinstance(current, list):
            try:
                current = current[int(part)]
            except (ValueError, IndexError) as exc:
                raise ValueError(f"JSON pointer list segment {part!r} not found") from exc
        else:
            raise ValueError(f"JSON pointer segment {part!r} cannot resolve through scalar")
    return current


def _load_packet(packet_dir: Path) -> SourceCapturePacket:
    manifest_path = packet_dir / "manifest.json"
    if not manifest_path.is_file():
        raise ValueError(f"packet manifest not found: {manifest_path}")
    return SourceCapturePacket.model_validate(
        _load_json_object(manifest_path, f"packet manifest {manifest_path}")
    )


def _contained_packet_path(packet_dir: Path, relative_packet_path: str) -> Path:
    path = (packet_dir / relative_packet_path).resolve()
    packet_root = packet_dir.resolve()
    try:
        path.relative_to(packet_root)
    except ValueError as exc:
        raise ValueError(
            f"preserved file path escapes packet directory: {relative_packet_path}"
        ) from exc
    if not path.is_file():
        raise ValueError(f"preserved file not found: {path}")
    return path


def _resolve_manifest_path(
    manifest_dir: Path,
    entry: dict[str, Any],
    field_name: str,
    *,
    label: str,
) -> Path:
    value = entry.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} field {field_name!r} must be a non-empty string")
    path = Path(value)
    if not path.is_absolute():
        path = manifest_dir / path
    return path.resolve()


def _load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"{label} not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} is not valid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must be a JSON object: {path}")
    return payload


def _summary_without_objects(value: dict[str, Any]) -> dict[str, Any]:
    return {
        key: item
        for key, item in value.items()
        if key not in {"cleaning_packet", "ecr_receipts"}
    }


def _lane_status(lane: str, findings: Sequence[dict[str, Any]]) -> str:
    lane_findings = [finding for finding in findings if finding["lane"] == lane]
    if any(finding["severity"] in BLOCKING_SEVERITIES for finding in lane_findings):
        return "fail"
    if lane_findings:
        return "warn"
    return "pass"


def _finding(
    findings: list[dict[str, Any]],
    *,
    lane: str,
    severity: str,
    code: str,
    owner_candidate: str,
    message: str,
    **extra: Any,
) -> None:
    finding = {
        "lane": lane,
        "severity": severity,
        "code": code,
        "owner_candidate": owner_candidate,
        "message": message,
    }
    finding.update({key: value for key, value in extra.items() if value is not None})
    findings.append(finding)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _render_markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Cleaning Spine Periodic Audit Report",
        "",
        f"- Schema: `{report['schema_version']}`",
        f"- Generated at: `{report['generated_at']}`",
        f"- Overall status: `{report['overall_status']}`",
        "",
        "## Lane Statuses",
    ]
    for lane, status in report["lane_statuses"].items():
        lines.append(f"- `{lane}`: `{status}`")
    lines.extend(
        [
            "",
            "## Counts",
        ]
    )
    for key, value in report["counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Findings"])
    if report["findings"]:
        for finding in report["findings"]:
            lines.append(
                f"- `{finding['severity']}` `{finding['lane']}` `{finding['code']}`: "
                f"{finding['message']}"
            )
    else:
        lines.append("- none")
    lines.extend(["", "## Non-Claims"])
    lines.extend(f"- `{item}`" for item in report["non_claims"])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run the no-network Cleaning spine periodic audit over frozen "
            "packet/projection/ECR/Cleaning artifacts."
        )
    )
    parser.add_argument(
        "--audit-manifest",
        required=True,
        type=Path,
        help="JSON manifest naming a smoke manifest and Lane A output artifacts.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory where audit reports and Lane B rebuild outputs will be written.",
    )
    args = parser.parse_args(argv)

    try:
        outputs = run_cleaning_spine_periodic_audit(
            audit_manifest_path=args.audit_manifest,
            output_dir=args.output_dir,
        )
        report = _load_json_object(Path(outputs["audit_report_json"]), "audit report")
    except (ValueError, ValidationError) as exc:
        parser.exit(status=2, message=f"cleaning periodic audit failed: {exc}\n")

    print(json.dumps(outputs, indent=2, sort_keys=True))
    status = report.get("overall_status")
    if status == "fail":
        return 1
    if status == "warn":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
