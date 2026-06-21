from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Mapping, Sequence

from source_capture.models import (
    PacketWriteResult,
    SourceCaptureSlice,
    VisibleFact,
    VisibleFactStatus,
)
from source_capture.writer import write_local_source_capture_packet

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


_CAPTURE_POSTURE_AXES = (
    "access_posture",
    "archive_history_posture",
    "media_modality_posture",
    "re_capture_relationship",
)


def staged_file_id_map(staged_artifacts: Sequence[tuple[str, bytes]]) -> dict[str, str]:
    """Map each staged-artifact filename to the file_id the writer will assign.

    The writer assigns ``file_{index:02d}`` (1-based) in ``input_files`` order
    (see ``writer._copy_preserved_files``). Runners reference these IDs from
    slices via this map instead of hard-coding ``["file_01", "file_02"]``.
    """
    mapping: dict[str, str] = {}
    for index, (filename, _content) in enumerate(staged_artifacts, start=1):
        if filename in mapping:
            raise ValueError(f"duplicate staged artifact filename: {filename}")
        mapping[filename] = f"file_{index:02d}"
    return mapping


def validate_capture_posture_honesty(
    *,
    source_slices: Sequence[SourceCaptureSlice],
    capture_postures: Mapping[str, object],
    limitations: Sequence[str] | None,
) -> None:
    """Reject a clean capture-level rollup that hides a limited slice.

    A slice is "limited" if it carries any ``limitations`` OR if any of its four
    posture axes (``access_posture``, ``archive_history_posture``,
    ``media_modality_posture``, ``re_capture_relationship``) has status
    ``unknown_with_reason`` -- the "tried and could not establish" gap. (Posture
    fields are ``VisibleFact``; ``not_attempted`` / ``not_applicable`` are honest
    scope statements and do NOT count as limited, so an ordinary direct-HTTP
    packet whose archive/media axes are ``not_attempted`` stays valid.)

    A limited slice must be surfaced at the capture level: either the
    capture-level ``limitations`` is non-empty, or -- for an
    ``unknown_with_reason`` axis -- the capture-level posture on that same axis is
    also ``unknown_with_reason``. This enforces the contract's "no rollup hides a
    failed/limited slice" invariant before the packet is written; it does not
    weaken ``models.SourceCapturePacket.validate_preserved_file_references``.
    """
    capture_limited = bool(list(limitations or []))

    if any(source_slice.limitations for source_slice in source_slices) and not capture_limited:
        raise ValueError(
            "capture-level limitations must surface slice-level limitations; "
            "a clean rollup may not hide a limited slice"
        )

    if capture_limited:
        # A non-empty capture-level limitations list already flags the capture as
        # limited, which surfaces every slice-level gap.
        return

    for axis in _CAPTURE_POSTURE_AXES:
        slice_unknown = any(
            getattr(source_slice, axis).status == VisibleFactStatus.UNKNOWN_WITH_REASON
            for source_slice in source_slices
        )
        if not slice_unknown:
            continue
        capture_fact = capture_postures.get(axis)
        capture_surfaces_gap = (
            isinstance(capture_fact, VisibleFact)
            and capture_fact.status == VisibleFactStatus.UNKNOWN_WITH_REASON
        )
        if not capture_surfaces_gap:
            raise ValueError(
                f"capture-level rollup hides a slice gap on '{axis}': a slice reports "
                "unknown_with_reason while capture-level limitations is empty and the "
                "capture-level posture on this axis is not unknown_with_reason"
            )


def stage_and_write_packet(
    *,
    output_directory: Path | None = None,
    data_root: "DataLakeRoot | None" = None,
    staged_artifacts: Sequence[tuple[str, bytes]],
    source_slices: Sequence[SourceCaptureSlice],
    enforce_posture_honesty: bool = True,
    **writer_kwargs: object,
) -> PacketWriteResult:
    """Own the adapter-result -> packet last mile: stage, validate, write, clean up.

    ``staged_artifacts`` is an ordered sequence of ``(filename, content_bytes)``;
    the order defines the writer's ``file_{index:02d}`` assignment (pair with
    ``staged_file_id_map``). ``writer_kwargs`` are forwarded verbatim to
    ``write_local_source_capture_packet`` — do not pass ``input_files`` or
    ``source_slices`` there; this helper owns both.
    """
    if "input_files" in writer_kwargs or "source_slices" in writer_kwargs:
        raise ValueError("input_files and source_slices are owned by stage_and_write_packet")
    if not staged_artifacts:
        raise ValueError("at least one staged artifact is required")
    if (output_directory is None) == (data_root is None):
        raise ValueError("exactly one of output_directory or data_root is required")

    if data_root is not None:
        if enforce_posture_honesty:
            raw_limitations = writer_kwargs.get("limitations")
            limitations = raw_limitations if isinstance(raw_limitations, Sequence) else None
            capture_postures = {axis: writer_kwargs.get(axis) for axis in _CAPTURE_POSTURE_AXES}
            validate_capture_posture_honesty(
                source_slices=source_slices,
                capture_postures=capture_postures,
                limitations=limitations,
            )
        # Lake commit: stage input artifacts in an isolated temp scratch; the writer
        # copies them into <root>/raw/<packet_id>/ and we discard the scratch.
        with tempfile.TemporaryDirectory(prefix="orca_capture_stage_") as scratch:
            staged_paths = [Path(scratch) / filename for filename, _content in staged_artifacts]
            for staged_path, (_filename, content) in zip(staged_paths, staged_artifacts):
                staged_path.write_bytes(content)
            return write_local_source_capture_packet(
                data_root=data_root,
                input_files=staged_paths,
                source_slices=list(source_slices),
                **writer_kwargs,  # type: ignore[arg-type]
            )

    staging_parent = output_directory.parent
    staging_parent.mkdir(parents=True, exist_ok=True)
    staged_paths = [staging_parent / filename for filename, _content in staged_artifacts]

    existing = [str(staged_path) for staged_path in staged_paths if staged_path.exists()]
    if existing:
        raise ValueError(
            "source capture staging files already exist in the output parent; "
            f"clear them before rerunning: {', '.join(existing)}"
        )

    if enforce_posture_honesty:
        raw_limitations = writer_kwargs.get("limitations")
        limitations = raw_limitations if isinstance(raw_limitations, Sequence) else None
        capture_postures = {axis: writer_kwargs.get(axis) for axis in _CAPTURE_POSTURE_AXES}
        validate_capture_posture_honesty(
            source_slices=source_slices,
            capture_postures=capture_postures,
            limitations=limitations,
        )

    try:
        for staged_path, (_filename, content) in zip(staged_paths, staged_artifacts):
            staged_path.write_bytes(content)
        result = write_local_source_capture_packet(
            output_directory=output_directory,
            input_files=staged_paths,
            source_slices=list(source_slices),
            **writer_kwargs,  # type: ignore[arg-type]
        )
    finally:
        for staged_path in staged_paths:
            try:
                staged_path.unlink()
            except FileNotFoundError:
                pass
    return result


__all__ = [
    "staged_file_id_map",
    "validate_capture_posture_honesty",
    "stage_and_write_packet",
]
