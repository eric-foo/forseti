"""Mechanical projection of an ATS job-posting Source Capture Packet into
view-only derived rows (one row per posting).

Capture-only (ruling 2): this projection extracts verbatim source facts and
performs NO ranking, relevance filtering, role classification, scoring, dedupe,
or pain inference. The row schema is a FIXED set of source-fact fields — there is
no free-form field dict, so there is structurally nowhere for a Judgment/
credibility/relevance field to land (that fixed schema is the forbidden-field
guard here). The raw ATS JSON is preserved verbatim in ``raw/``; this projection
re-parses that raw through the one shared adapter parser, so a posting is never
parsed by two divergent code paths.

Not Cleaning, not ECR, not Judgment. Rows are ``view_only; not_cleaned;
not_normalized; not_judgment_ready``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Mapping

from pydantic import Field, model_validator

from harness_utils import generate_ulid
from schemas.case_models import StrictModel
from source_capture.adapters.ats_job_posting import AtsVendor, parse_board_postings
from source_capture.models import PreservedFile, SourceCapturePacket
from source_capture.projection_shared import read_packet_directory as _read_packet_directory

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


ATS_JOB_POSTING_SOURCE_FAMILY = "ats_job_posting"
ATS_JOB_POSTING_PROJECTION_METHOD = "ats_job_posting_mechanical_projection"
ATS_JOB_POSTING_PROJECTION_VERSION = "v1"
ATS_JOB_POSTING_PROJECTION_CERTIFICATION = (
    "view_only; not_cleaned; not_normalized; not_judgment_ready"
)
PROJECTION_ATS_JOB_POSTING_LANE = "projection_ats_job_posting"

RAW_BOARD_DOCUMENT_BASENAME = "ats_board_raw.json"
CAPTURE_METADATA_BASENAME = "ats_capture_metadata.json"


class AtsProjectionRawRef(StrictModel):
    packet_id: str
    slice_id: str


class AtsProjectionRawAnchor(StrictModel):
    file_id: str
    relative_packet_path: str
    sha256: str
    hash_basis: str


class AtsJobPostingRow(StrictModel):
    row_id: str
    row_kind: Literal["ats_job_posting"] = "ats_job_posting"
    ats_vendor: str
    company: str
    ats_job_id: str
    title: str | None = None
    description: str | None = None
    posted_date: str | None = None
    source_url: str | None = None
    location_raw: str | None = None
    location_country: str | None = None
    is_listed: bool | None = None
    captured_at: str
    source_order: int = Field(ge=0)
    raw_ref: AtsProjectionRawRef
    raw_anchor: AtsProjectionRawAnchor
    residuals: list[str] = Field(default_factory=list)


class AtsJobPostingLossLedger(StrictModel):
    preserved_posting_rows: int = Field(ge=0)
    certification: Literal[
        "mechanical_per_posting_projection; does_not_certify_board_completeness"
    ] = "mechanical_per_posting_projection; does_not_certify_board_completeness"


class AtsJobPostingProjectionPacket(StrictModel):
    projection_method: Literal["ats_job_posting_mechanical_projection"] = (
        ATS_JOB_POSTING_PROJECTION_METHOD
    )
    projection_version: Literal["v1"] = ATS_JOB_POSTING_PROJECTION_VERSION
    certification: Literal["view_only; not_cleaned; not_normalized; not_judgment_ready"] = (
        ATS_JOB_POSTING_PROJECTION_CERTIFICATION
    )
    packet_id: str
    ats_vendor: str
    company: str
    captured_at: str
    rows: list[AtsJobPostingRow] = Field(default_factory=list)
    loss_ledger: AtsJobPostingLossLedger
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_counts(self) -> "AtsJobPostingProjectionPacket":
        if self.loss_ledger.preserved_posting_rows != len(self.rows):
            raise ValueError("loss_ledger.preserved_posting_rows must match rows length")
        return self


def build_ats_job_posting_projection(
    *,
    packet: SourceCapturePacket,
    raw_file_bytes_by_file_id: Mapping[str, bytes],
) -> AtsJobPostingProjectionPacket:
    if packet.source_family != ATS_JOB_POSTING_SOURCE_FAMILY:
        raise ValueError(
            "ATS job-posting projection requires "
            f"source_family={ATS_JOB_POSTING_SOURCE_FAMILY!r}; got {packet.source_family!r}"
        )

    preserved_by_id = {item.file_id: item for item in packet.preserved_files}
    raw_file = _find_preserved(packet, RAW_BOARD_DOCUMENT_BASENAME)
    metadata_file = _find_preserved(packet, CAPTURE_METADATA_BASENAME)
    for preserved in (raw_file, metadata_file):
        if preserved.file_id not in raw_file_bytes_by_file_id:
            raise ValueError(f"raw bytes are required for preserved file id: {preserved.file_id}")

    metadata = json.loads(raw_file_bytes_by_file_id[metadata_file.file_id].decode("utf-8"))
    vendor_value = metadata.get("ats_vendor")
    company = metadata.get("company")
    captured_at = metadata.get("captured_at")
    if not isinstance(vendor_value, str) or not isinstance(company, str) or not isinstance(captured_at, str):
        raise ValueError(
            "ATS capture metadata must carry string ats_vendor, company, and captured_at"
        )
    vendor = AtsVendor(vendor_value)

    raw_anchor = AtsProjectionRawAnchor(
        file_id=raw_file.file_id,
        relative_packet_path=raw_file.relative_packet_path,
        sha256=raw_file.sha256,
        hash_basis=raw_file.hash_basis,
    )

    postings = parse_board_postings(vendor, raw_file_bytes_by_file_id[raw_file.file_id])
    raw_slice_ids = _slices_referencing(packet, raw_file.file_id)
    if postings and len(raw_slice_ids) != len(postings):
        raise ValueError(
            "ATS packet must carry exactly one raw-referencing source slice per posting; "
            f"found {len(raw_slice_ids)} slice(s) for {len(postings)} posting(s)"
        )
    rows: list[AtsJobPostingRow] = []
    for index, (posting, slice_id) in enumerate(
        zip(postings, raw_slice_ids if postings else [], strict=True), start=1
    ):
        residuals = [
            f"{name}_absent"
            for name, value in (
                ("title", posting.title),
                ("description", posting.description),
                ("posted_date", posting.posted_date),
                ("source_url", posting.source_url),
                ("location_raw", posting.location_raw),
                ("location_country", posting.location_country),
            )
            if value in (None, "")
        ]
        rows.append(
            AtsJobPostingRow(
                row_id=f"{packet.packet_id}:{vendor.value}:{index:04d}:{posting.ats_job_id}",
                ats_vendor=vendor.value,
                company=company,
                ats_job_id=posting.ats_job_id,
                title=posting.title,
                description=posting.description,
                posted_date=posting.posted_date,
                source_url=posting.source_url,
                location_raw=posting.location_raw,
                location_country=posting.location_country,
                is_listed=posting.is_listed,
                captured_at=captured_at,
                source_order=index,
                raw_ref=AtsProjectionRawRef(
                    packet_id=packet.packet_id, slice_id=slice_id
                ),
                raw_anchor=raw_anchor,
                residuals=residuals,
            )
        )

    board_residuals: list[str] = []
    if not rows:
        board_residuals.append("ats_board_zero_postings")

    return AtsJobPostingProjectionPacket(
        packet_id=packet.packet_id,
        ats_vendor=vendor.value,
        company=company,
        captured_at=captured_at,
        rows=rows,
        loss_ledger=AtsJobPostingLossLedger(preserved_posting_rows=len(rows)),
        residuals=board_residuals,
    )


def build_ats_job_posting_projection_from_packet_directory(
    *,
    packet_or_manifest_path: Path,
) -> AtsJobPostingProjectionPacket:
    packet, raw_file_bytes_by_file_id = _read_packet_directory(packet_or_manifest_path)
    return build_ats_job_posting_projection(
        packet=packet,
        raw_file_bytes_by_file_id=raw_file_bytes_by_file_id,
    )


def write_ats_job_posting_projection(
    *,
    packet_or_manifest_path: Path,
    output_path: Path,
    overwrite: bool = False,
) -> AtsJobPostingProjectionPacket:
    projection = build_ats_job_posting_projection_from_packet_directory(
        packet_or_manifest_path=packet_or_manifest_path,
    )
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_projection_json_text(projection), encoding="utf-8")
    return projection


def project_ats_job_posting_into_lake(
    *,
    data_root: "DataLakeRoot",
    packet_id: str,
    record_id: str | None = None,
) -> tuple[AtsJobPostingProjectionPacket, Path]:
    """Project a committed ATS raw packet into an append-only derived record."""
    loaded = data_root.load_raw_packet(packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    projection = build_ats_job_posting_projection(
        packet=packet,
        raw_file_bytes_by_file_id=loaded.bodies,
    )
    record = record_id if record_id is not None else generate_ulid()
    derived_path = data_root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=PROJECTION_ATS_JOB_POSTING_LANE,
        record_id=f"{record}.json",
        data=_projection_json_text(projection).encode("utf-8"),
    )
    return projection, derived_path


def _find_preserved(packet: SourceCapturePacket, basename: str) -> PreservedFile:
    for preserved in packet.preserved_files:
        if Path(preserved.relative_packet_path).name.endswith(basename):
            return preserved
    raise ValueError(
        f"ATS packet is missing the required preserved file '{basename}'; "
        "not an ats_job_posting capture packet"
    )


def _slices_referencing(packet: SourceCapturePacket, file_id: str) -> list[str]:
    slice_ids = [
        source_slice.slice_id
        for source_slice in packet.source_slices
        if file_id in source_slice.preserved_file_ids
    ]
    if not slice_ids:
        raise ValueError(
            f"no source slice references the raw board document file_id {file_id!r}"
        )
    return slice_ids


def _projection_json_text(projection: AtsJobPostingProjectionPacket) -> str:
    return f"{json.dumps(projection.model_dump(mode='json'), indent=2, sort_keys=True)}\n"


__all__ = [
    "ATS_JOB_POSTING_PROJECTION_CERTIFICATION",
    "ATS_JOB_POSTING_PROJECTION_METHOD",
    "ATS_JOB_POSTING_PROJECTION_VERSION",
    "ATS_JOB_POSTING_SOURCE_FAMILY",
    "CAPTURE_METADATA_BASENAME",
    "PROJECTION_ATS_JOB_POSTING_LANE",
    "RAW_BOARD_DOCUMENT_BASENAME",
    "AtsJobPostingLossLedger",
    "AtsJobPostingProjectionPacket",
    "AtsJobPostingRow",
    "AtsProjectionRawAnchor",
    "AtsProjectionRawRef",
    "build_ats_job_posting_projection",
    "build_ats_job_posting_projection_from_packet_directory",
    "project_ats_job_posting_into_lake",
    "write_ats_job_posting_projection",
]
