from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Sequence

from harness_utils import generate_ulid, hash_file, utc_now_z
from source_capture.models import (
    OBLIGATION_CONTRACT_VERSION,
    SOURCE_CAPTURE_MANIFEST_VERSION,
    CaptureModeCategory,
    PacketTiming,
    PacketWriteResult,
    PreservedFile,
    ReceiptMetadata,
    SourceCapturePacket,
    SourceCaptureSlice,
    VisibleFact,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


NON_CLAIMS = [
    "not source acquisition",
    "not direct HTTP fetch",
    "not archive retrieval",
    "not media preservation",
    "not browser automation",
    "not ECR design",
    "not Cleaning implementation",
    "not Judgment scoring",
    "not buyer proof",
    "not commercial-readiness logic",
]


def write_local_source_capture_packet(
    *,
    output_directory: Path | None = None,
    data_root: "DataLakeRoot | None" = None,
    input_files: Sequence[Path],
    source_family: str,
    source_surface: str,
    source_locator: VisibleFact,
    decision_question: str,
    capture_context: str,
    actor_audience_context: VisibleFact | None = None,
    capture_mode: CaptureModeCategory = CaptureModeCategory.AGENT_ASSISTED,
    operator_category: str = "local_cli_operator",
    session_identity: str | None = None,
    visible_mode_changes: Sequence[str] | None = None,
    source_publication_or_event: VisibleFact | None = None,
    source_edit_or_version: VisibleFact | None = None,
    cutoff_posture: VisibleFact | None = None,
    recapture_time: VisibleFact | None = None,
    archive_snapshot_time: VisibleFact | None = None,
    access_posture: VisibleFact | None = None,
    archive_history_posture: VisibleFact | None = None,
    media_modality_posture: VisibleFact | None = None,
    re_capture_relationship: VisibleFact | None = None,
    # Demand-durability series facts (Ob.17 Elements 2 & 4). Additive and optional so a
    # non-durability capture leaves them unset (None) and existing manifests stay valid under
    # extra="forbid" -- no SOURCE_CAPTURE_MANIFEST_VERSION bump. A demand-durability series sets
    # series_id on every observation; cold_start_at + pre_coverage_history_posture mark the series
    # origin (first / cold-start observation); intended_cadence carries the declared
    # CadencePlan.to_dict() shape. All are observed facts forwarded verbatim, never weights or a
    # durable-vs-hollow verdict (INV-1). Element 1 pins ride on each SourceCaptureSlice (the caller
    # builds the slices), so they are not parameters here.
    series_id: str | None = None,
    cold_start_at: VisibleFact | None = None,
    pre_coverage_history_posture: VisibleFact | None = None,
    intended_cadence: dict[str, object] | None = None,
    source_slices: Sequence[SourceCaptureSlice] | None = None,
    warnings: Sequence[str] | None = None,
    limitations: Sequence[str] | None = None,
    receipt_summary: str | None = None,
    receipt_non_claims: Sequence[str] | None = None,
) -> PacketWriteResult:
    if not input_files:
        raise ValueError("at least one input file is required")
    if (output_directory is None) == (data_root is None):
        raise ValueError("exactly one of output_directory or data_root is required")

    resolved_inputs = [path.resolve() for path in input_files]
    for path in resolved_inputs:
        if not path.exists():
            raise FileNotFoundError(f"input file does not exist: {path}")
        if not path.is_file():
            raise ValueError(f"input path is not a file: {path}")

    packet_id = generate_ulid()
    if data_root is not None:
        # Go-forward raw writes are staged off-tree, then atomically published to
        # <root>/raw/<packet_id>/ so a partial packet never appears under raw/
        # (write-once + atomic publish per the write-boundary enforcement contract).
        # output_directory stays available for legacy/test callers (incumbent path;
        # migration of existing output is deferred).
        output_directory = data_root.stage_raw_packet(packet_id)
    assert output_directory is not None  # guaranteed by the exactly-one-target check above

    _prepare_output_directory(output_directory)
    raw_directory = output_directory / "raw"
    raw_directory.mkdir(parents=True, exist_ok=True)

    session_id = session_identity or generate_ulid()
    captured_at = utc_now_z()
    preserved_files = _copy_preserved_files(raw_directory, resolved_inputs)
    packet_warnings = list(warnings or [])
    packet_limitations = list(limitations or [])

    timing = PacketTiming(
        source_publication_or_event=source_publication_or_event
        or unknown_with_reason("local-file CLI did not receive source publication or event timing"),
        source_edit_or_version=source_edit_or_version
        or unknown_with_reason("local-file CLI did not receive source edit or version timing"),
        capture_time=known_fact(captured_at),
        archive_snapshot_time=archive_snapshot_time,
        recapture_time=recapture_time
        or not_applicable("first checkpoint local-file packet does not model an earlier capture by default"),
        cutoff_posture=cutoff_posture
        or unknown_with_reason("local-file CLI did not receive cutoff posture metadata"),
    )
    access = access_posture or known_fact("local_file_only")
    archive = archive_history_posture or not_attempted(
        "local-file CLI packages existing artifacts only and does not query archive or history services"
    )
    media = media_modality_posture or not_attempted(
        "local-file CLI preserves supplied files but does not determine whether additional media capture was required"
    )
    recapture = re_capture_relationship or not_applicable(
        "no re-capture relationship was supplied for this local packet"
    )
    packet_slices = (
        list(source_slices)
        if source_slices is not None
        else [
            SourceCaptureSlice(
                slice_id="slice_01",
                locator=source_locator,
                timing=timing,
                access_posture=access,
                archive_history_posture=archive,
                media_modality_posture=media,
                re_capture_relationship=recapture,
                limitations=packet_limitations,
                warning_notes=packet_warnings,
                preserved_file_ids=[item.file_id for item in preserved_files],
            )
        ]
    )
    if not packet_slices:
        raise ValueError("at least one source slice is required")

    packet = SourceCapturePacket(
        packet_id=packet_id,
        manifest_version=SOURCE_CAPTURE_MANIFEST_VERSION,
        obligation_contract_version=OBLIGATION_CONTRACT_VERSION,
        source_family=source_family,
        source_surface=source_surface,
        source_locator=source_locator,
        requested_decision_context=known_fact(decision_question),
        capture_context=known_fact(capture_context),
        actor_audience_context=actor_audience_context
        or unknown_with_reason("actor or audience context was not supplied to the local-file CLI"),
        capture_mode=capture_mode,
        operator_category=operator_category,
        session_identity=session_id,
        visible_mode_changes=list(visible_mode_changes or []),
        timing=timing,
        access_posture=access,
        archive_history_posture=archive,
        media_modality_posture=media,
        re_capture_relationship=recapture,
        series_id=series_id,
        cold_start_at=cold_start_at,
        pre_coverage_history_posture=pre_coverage_history_posture,
        intended_cadence=intended_cadence,
        source_slices=packet_slices,
        preserved_files=preserved_files,
        warnings=packet_warnings,
        limitations=packet_limitations,
        receipt_metadata=ReceiptMetadata(
            title="Source Capture Packet Receipt",
            generated_at=captured_at,
            summary=receipt_summary
            or f"Local-file-only packet for {source_family} with {len(preserved_files)} preserved file(s).",
            non_claims=list(receipt_non_claims if receipt_non_claims is not None else NON_CLAIMS),
        ),
    )

    manifest_path = output_directory / "manifest.json"
    receipt_path = output_directory / "receipt.md"
    manifest_path.write_text(
        f"{json.dumps(packet.model_dump(mode='json'), indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )
    receipt_path.write_text(render_receipt(packet), encoding="utf-8", newline="\n")

    if data_root is not None:
        # Atomically publish the completed staging dir to raw/<packet_id>.
        output_directory = data_root.publish_raw_packet(output_directory, packet_id)
        manifest_path = output_directory / "manifest.json"
        receipt_path = output_directory / "receipt.md"

    return PacketWriteResult(
        output_directory=str(output_directory.resolve()),
        manifest_path=str(manifest_path.resolve()),
        receipt_path=str(receipt_path.resolve()),
        packet=packet,
    )


def render_receipt(packet: SourceCapturePacket) -> str:
    lines = [
        f"# {packet.receipt_metadata.title}",
        "",
        f"- Packet ID: `{packet.packet_id}`",
        f"- Manifest version: `{packet.manifest_version}`",
        f"- Obligation contract version: `{packet.obligation_contract_version}`",
        f"- Source family: `{packet.source_family}`",
        f"- Source surface: `{packet.source_surface}`",
        f"- Session identity: `{packet.session_identity}`",
        f"- Capture mode: `{packet.capture_mode.value}`",
        f"- Visible mode changes: {', '.join(packet.visible_mode_changes) if packet.visible_mode_changes else 'none'}",
        f"- Operator category: `{packet.operator_category}`",
        f"- Receipt generated at: `{packet.receipt_metadata.generated_at}`",
        "",
        "## Summary",
        "",
        packet.receipt_metadata.summary,
        "",
        "## Requested Context",
        "",
        f"- Decision question: {_format_fact(packet.requested_decision_context)}",
        f"- Capture context: {_format_fact(packet.capture_context)}",
        f"- Source locator: {_format_fact(packet.source_locator)}",
        f"- Actor/audience context: {_format_fact(packet.actor_audience_context)}",
        "",
        "## Timing",
        "",
        f"- Source publication or event timing: {_format_fact(packet.timing.source_publication_or_event)}",
        f"- Source edit or version timing: {_format_fact(packet.timing.source_edit_or_version)}",
        f"- Capture timing: {_format_fact(packet.timing.capture_time)}",
        f"- Re-capture timing: {_format_fact(packet.timing.recapture_time)}",
        f"- Cutoff posture: {_format_fact(packet.timing.cutoff_posture)}",
        "",
        "## Posture",
        "",
        f"- Access posture: {_format_fact(packet.access_posture)}",
        f"- Archive/history posture: {_format_fact(packet.archive_history_posture)}",
        f"- Media/modality posture: {_format_fact(packet.media_modality_posture)}",
        f"- Re-capture relationship: {_format_fact(packet.re_capture_relationship)}",
        "",
        "## Preserved Files",
        "",
    ]

    for preserved_file in packet.preserved_files:
        lines.append(
            "- "
            f"`{preserved_file.file_id}` -> `{preserved_file.relative_packet_path}` "
            f"(sha256 `{preserved_file.sha256}`, {preserved_file.size_bytes} bytes)"
        )

    lines.extend(
        [
            "",
            "## Warnings",
            "",
            *_format_list(packet.warnings),
            "",
            "## Limitations",
            "",
            *_format_list(packet.limitations),
            "",
            "## Non-Claims",
            "",
            *_format_list(packet.receipt_metadata.non_claims),
            "",
        ]
    )
    return "\n".join(lines)


def _copy_preserved_files(raw_directory: Path, input_files: Sequence[Path]) -> list[PreservedFile]:
    preserved_files: list[PreservedFile] = []
    for index, source_path in enumerate(input_files, start=1):
        destination_name = f"{index:02d}_{source_path.name}"
        destination_path = raw_directory / destination_name
        shutil.copy2(source_path, destination_path)
        preserved_files.append(
            PreservedFile(
                file_id=f"file_{index:02d}",
                original_path=str(source_path),
                relative_packet_path=str(destination_path.relative_to(raw_directory.parent)).replace("\\", "/"),
                sha256=hash_file(destination_path),
                # hash_file hashes the complete copied bytes at relative_packet_path; the
                # basis is therefore raw_stored_bytes (AR-04 recomputation-bound contract).
                hash_basis="raw_stored_bytes",
                size_bytes=destination_path.stat().st_size,
            )
        )
    return preserved_files


def _prepare_output_directory(output_directory: Path) -> None:
    if output_directory.exists():
        if not output_directory.is_dir():
            raise ValueError(f"output path is not a directory: {output_directory}")
        if any(output_directory.iterdir()):
            raise ValueError(f"refusing to overwrite non-empty output directory: {output_directory}")
        return
    output_directory.mkdir(parents=True, exist_ok=False)


def _format_fact(fact: VisibleFact) -> str:
    if fact.status == "known":
        return fact.value or ""
    return f"{fact.status} ({fact.reason})"


def _format_list(items: Sequence[str]) -> list[str]:
    if not items:
        return ["- none"]
    return [f"- {item}" for item in items]
