"""Mechanical projection rows for admitted TikTok creator-batch packets."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Literal, Mapping

from pydantic import Field, model_validator

from schemas.case_models import StrictModel
from source_capture.tiktok.admission import assert_no_sensitive_tiktok_material
from source_capture.tiktok.batch_coverage import (
    TIKTOK_BATCH_COVERAGE_METHOD,
    build_tiktok_batch_coverage_from_lake,
    build_tiktok_batch_coverage_from_packet_directory,
)
from source_capture.tiktok.batch_packet import TIKTOK_BATCH_CAPTURE_SURFACE

TIKTOK_BATCH_PROJECTION_METHOD = "tiktok_batch_coverage_mechanical_projection"
TIKTOK_BATCH_PROJECTION_VERSION = "v0"
TIKTOK_BATCH_PROJECTION_CERTIFICATION = (
    "view_only; not_cleaned; not_normalized; not_judgment_ready"
)

TIKTOK_BATCH_PROJECTION_NON_CLAIMS = (
    "not_live_tiktok_capture_or_browser_automation",
    "not_direct_forged_tiktok_api_call",
    "not_product_mention_extraction",
    "not_cleaning_transform",
    "not_ecr_record",
    "not_judgment_or_buyer_proof",
    "not_persisted_derived_projection_lane",
    "not_cross_creator_detection_ceiling",
    "raw_comment_text_omitted",
    "raw_transcript_text_omitted",
    "raw_subtitle_cue_text_omitted",
    "hashtags_and_source_mentions_omitted",
)


class TikTokBatchProjectionRawRef(StrictModel):
    packet_id: str
    slice_id: str


class TikTokBatchProjectionRawAnchor(StrictModel):
    file_id: str
    relative_packet_path: str
    sha256: str
    hash_basis: str
    anchor_kind: Literal["json_pointer"] = "json_pointer"
    json_pointer: str


class TikTokBatchProjectionRow(StrictModel):
    row_id: str
    row_kind: Literal["tiktok_batch_video_coverage"] = "tiktok_batch_video_coverage"
    raw_ref: TikTokBatchProjectionRawRef
    raw_anchor: TikTokBatchProjectionRawAnchor
    entity_namespace: Literal["tiktok"] = "tiktok"
    creator_handle: str | None = None
    video_id: str | None = None
    video_url: str | None = None
    raw_video_index: int
    source_index: int | None = None
    status: str | None = None
    create_time_utc: str | None = None
    decoded_aweme_id_create_time_utc: str | None = None
    stats: dict[str, int] = Field(default_factory=dict)
    comment_posture: str | None = None
    comment_response_status: int | None = None
    captured_comment_count: int = 0
    assessment_comment_count: int = 0
    comment_envelope_total: int = 0
    comment_envelope_has_more: bool | None = None
    comment_question_count: int = 0
    comment_intent_term_counts: dict[str, int] = Field(default_factory=dict)
    comment_body_sha256: str | None = None
    subtitle_posture: str | None = None
    subtitle_info_count: int = 0
    subtitle_source_count: int = 0
    subtitle_language_count: int = 0
    subtitle_format_count: int = 0
    subtitle_body_sha256: str | None = None
    subtitle_url_sha256: str | None = None
    subtitle_url_length: int | None = None
    subtitle_cue_count: int = 0
    transcript_char_count: int = 0
    transcript_text_sha256: str | None = None
    has_transcript_text: bool = False
    transcript_signal_term_count: int = 0
    has_description_text: bool = False
    description_char_count: int = 0
    description_sha256: str | None = None
    source_mention_count: int = 0
    disclosure_signal_count: int = 0
    has_disclosure_signal: bool = False
    has_profile_list_source_receipt: bool = False
    profile_list_source_response_url_sha256: str | None = None
    residuals: list[str] = Field(default_factory=list)


class TikTokBatchProjectionLossLedger(StrictModel):
    preserved_video_rows: int = Field(ge=0)
    preserved_bindings: Literal[0] = 0
    structure_preserved: bool
    omitted_comment_text_row_count: int = Field(ge=0)
    omitted_subtitle_cue_text_row_count: int = Field(ge=0)
    row_residual_counts: dict[str, int] = Field(default_factory=dict)
    certification: Literal[
        "mechanical_batch_coverage_projection; does_not_certify_cleaning_or_judgment"
    ] = "mechanical_batch_coverage_projection; does_not_certify_cleaning_or_judgment"


class TikTokBatchProjectionPacket(StrictModel):
    projection_method: Literal[
        "tiktok_batch_coverage_mechanical_projection"
    ] = TIKTOK_BATCH_PROJECTION_METHOD
    projection_version: Literal["v0"] = TIKTOK_BATCH_PROJECTION_VERSION
    certification: Literal[
        "view_only; not_cleaned; not_normalized; not_judgment_ready"
    ] = TIKTOK_BATCH_PROJECTION_CERTIFICATION
    source_family: Literal["tiktok"] = "tiktok"
    source_surface: Literal["tiktok_creator_profile_parsed_batch"] = TIKTOK_BATCH_CAPTURE_SURFACE
    packet_id: str
    coverage_method: Literal["tiktok_batch_coverage_view"] = TIKTOK_BATCH_COVERAGE_METHOD
    creator_handle: str | None = None
    batch_label: str | None = None
    capture_timestamp: str | None = None
    rows: list[TikTokBatchProjectionRow] = Field(default_factory=list)
    binding_map: list[object] = Field(default_factory=list)
    loss_ledger: TikTokBatchProjectionLossLedger
    residuals: list[str] = Field(default_factory=list)
    non_claims: list[str] = Field(default_factory=lambda: list(TIKTOK_BATCH_PROJECTION_NON_CLAIMS))

    @model_validator(mode="after")
    def validate_counts(self) -> "TikTokBatchProjectionPacket":
        if self.loss_ledger.preserved_video_rows != len(self.rows):
            raise ValueError("loss_ledger.preserved_video_rows must match rows length")
        if self.binding_map:
            raise ValueError("TikTok batch projection v0 does not define bindings")
        return self


def build_tiktok_batch_projection_from_coverage(
    coverage: Mapping[str, Any],
) -> TikTokBatchProjectionPacket:
    """Derive a text-free projection packet from a TikTok batch coverage view.

    The projection is keyed to the original preserved batch JSON, not to the
    coverage view. Coverage objects without file/hash raw refs are rejected.
    """

    _validate_coverage(coverage)
    packet_id = _required_str(coverage.get("packet_id"), "packet_id")
    raw_ref = _raw_ref_fields(coverage.get("raw_ref"), expected_packet_id=packet_id)
    rows_input = [_as_mapping(item) for item in _as_list(coverage.get("video_rows"))]
    raw_video_indexes: list[int] = []
    rows: list[TikTokBatchProjectionRow] = []
    for row_index, row in enumerate(rows_input):
        if not row:
            continue
        raw_video_index = _required_nonnegative_int(
            row.get("raw_video_index"), f"video_rows[{row_index}].raw_video_index"
        )
        raw_video_indexes.append(raw_video_index)
        rows.append(
            _project_video_row(
                row=row,
                raw_video_index=raw_video_index,
                packet_id=packet_id,
                creator_handle=_first_str(coverage.get("creator_handle")),
                raw_ref=raw_ref,
            )
        )
    coverage_loss = _as_mapping(coverage.get("loss_ledger"))
    row_residual_counts = Counter(residual for row in rows for residual in row.residuals)
    structure_preserved = _raw_video_index_sequence_preserved(raw_video_indexes)
    residuals = sorted(row_residual_counts)
    if not structure_preserved:
        residuals.append("raw_video_index_gap_or_reorder")
    projection = TikTokBatchProjectionPacket(
        packet_id=packet_id,
        creator_handle=_first_str(coverage.get("creator_handle")),
        batch_label=_first_str(coverage.get("batch_label")),
        capture_timestamp=_first_str(coverage.get("capture_timestamp")),
        rows=rows,
        loss_ledger=TikTokBatchProjectionLossLedger(
            preserved_video_rows=len(rows),
            structure_preserved=structure_preserved,
            omitted_comment_text_row_count=_first_int(
                coverage_loss.get("omitted_comment_text_row_count"), 0
            )
            or 0,
            omitted_subtitle_cue_text_row_count=_first_int(
                coverage_loss.get("omitted_subtitle_cue_text_row_count"), 0
            )
            or 0,
            row_residual_counts=dict(sorted(row_residual_counts.items())),
        ),
        residuals=residuals,
    )
    assert_no_sensitive_tiktok_material(projection.model_dump(mode="json"))
    return projection


def build_tiktok_batch_projection_from_packet_directory(
    packet_or_manifest_path: Path,
) -> TikTokBatchProjectionPacket:
    """Read an admitted TikTok batch packet directory and project its coverage rows."""

    coverage = build_tiktok_batch_coverage_from_packet_directory(packet_or_manifest_path)
    return build_tiktok_batch_projection_from_coverage(coverage)


def build_tiktok_batch_projection_from_lake(
    data_root: Any,
    packet_id: str,
) -> TikTokBatchProjectionPacket:
    """Read a raw packet by key through DataLakeRoot and project its coverage rows."""

    coverage = build_tiktok_batch_coverage_from_lake(data_root, packet_id)
    return build_tiktok_batch_projection_from_coverage(coverage)


def tiktok_batch_projection_json_text(
    projection: TikTokBatchProjectionPacket | Mapping[str, Any],
) -> str:
    """Render projection JSON deterministically."""

    data = (
        projection.model_dump(mode="json")
        if isinstance(projection, TikTokBatchProjectionPacket)
        else dict(projection)
    )
    assert_no_sensitive_tiktok_material(data)
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def write_tiktok_batch_projection(
    *,
    projection: TikTokBatchProjectionPacket | Mapping[str, Any],
    output_path: Path,
    overwrite: bool = False,
) -> Path:
    """Write projection JSON locally. This does not append a data-lake record."""

    if output_path.exists() and not overwrite:
        raise FileExistsError(f"projection output already exists: {output_path}")
    if output_path.exists() and output_path.is_dir():
        raise IsADirectoryError(f"projection output is a directory: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(tiktok_batch_projection_json_text(projection), encoding="utf-8")
    return output_path


def _validate_coverage(coverage: Mapping[str, Any]) -> None:
    if not isinstance(coverage, Mapping):
        raise ValueError("TikTok batch projection input must be a JSON object")
    if coverage.get("coverage_method") != TIKTOK_BATCH_COVERAGE_METHOD:
        raise ValueError("projection input is not a TikTok batch coverage view")
    if not isinstance(coverage.get("video_rows"), list):
        raise ValueError("TikTok batch projection input missing video_rows list")
    assert_no_sensitive_tiktok_material(coverage)


def _project_video_row(
    *,
    row: Mapping[str, Any],
    raw_video_index: int,
    packet_id: str,
    creator_handle: str | None,
    raw_ref: Mapping[str, str],
) -> TikTokBatchProjectionRow:
    comments = _as_mapping(row.get("comments"))
    subtitles = _as_mapping(row.get("subtitles"))
    source_text = _as_mapping(row.get("source_text_signals"))
    profile_receipt = _as_mapping(row.get("profile_list_source_receipt"))
    slice_id = f"videos/{raw_video_index}"
    return TikTokBatchProjectionRow(
        row_id=f"{packet_id}:{slice_id}",
        raw_ref=TikTokBatchProjectionRawRef(packet_id=packet_id, slice_id=slice_id),
        raw_anchor=TikTokBatchProjectionRawAnchor(
            file_id=raw_ref["file_id"],
            relative_packet_path=raw_ref["relative_packet_path"],
            sha256=raw_ref["sha256"],
            hash_basis=raw_ref["hash_basis"],
            json_pointer=f"/videos/{raw_video_index}",
        ),
        creator_handle=creator_handle,
        video_id=_first_str(row.get("video_id")),
        video_url=_first_str(row.get("video_url")),
        raw_video_index=raw_video_index,
        source_index=_first_int(row.get("source_index")),
        status=_first_str(row.get("status")),
        create_time_utc=_first_str(row.get("create_time_utc")),
        decoded_aweme_id_create_time_utc=_first_str(row.get("decoded_aweme_id_create_time_utc")),
        stats=_int_mapping(row.get("stats")),
        comment_posture=_first_str(comments.get("posture")),
        comment_response_status=_first_int(comments.get("response_status")),
        comment_body_sha256=_first_str(comments.get("body_sha256")),
        captured_comment_count=_first_int(comments.get("captured_comment_count"), 0) or 0,
        assessment_comment_count=_first_int(comments.get("assessment_comment_count"), 0) or 0,
        comment_envelope_total=_first_int(comments.get("envelope_total"), 0) or 0,
        comment_envelope_has_more=_as_bool(comments.get("envelope_has_more")),
        comment_question_count=_first_int(comments.get("question_comment_count"), 0) or 0,
        comment_intent_term_counts=_int_mapping(comments.get("intent_term_counts")),
        subtitle_posture=_first_str(subtitles.get("posture")),
        subtitle_info_count=_first_int(subtitles.get("subtitle_info_count"), 0) or 0,
        subtitle_source_count=len(_string_list(subtitles.get("subtitle_sources"))),
        subtitle_language_count=len(_string_list(subtitles.get("subtitle_language_code_names"))),
        subtitle_format_count=len(_string_list(subtitles.get("subtitle_formats"))),
        subtitle_body_sha256=_first_str(subtitles.get("body_sha256")),
        subtitle_url_sha256=_first_str(subtitles.get("subtitle_url_sha256")),
        subtitle_url_length=_first_int(subtitles.get("subtitle_url_length")),
        subtitle_cue_count=_first_int(subtitles.get("cue_count"), 0) or 0,
        transcript_char_count=_first_int(subtitles.get("transcript_char_count"), 0) or 0,
        transcript_text_sha256=_first_str(subtitles.get("transcript_text_sha256")),
        has_transcript_text=subtitles.get("has_transcript_text") is True,
        transcript_signal_term_count=len(_string_list(subtitles.get("transcript_signal_terms"))),
        has_description_text=source_text.get("has_description_text") is True,
        description_char_count=_first_int(source_text.get("description_char_count"), 0) or 0,
        description_sha256=_first_str(source_text.get("description_sha256")),
        source_mention_count=len(_string_list(source_text.get("source_mentions"))),
        disclosure_signal_count=len(_string_list(source_text.get("disclosure_source_text_signals"))),
        has_disclosure_signal=source_text.get("has_disclosure_signal") is True,
        has_profile_list_source_receipt=bool(profile_receipt),
        profile_list_source_response_url_sha256=_first_str(
            profile_receipt.get("source_response_url_sha256")
        ),
        residuals=_string_list(row.get("residuals")),
    )


def _raw_ref_fields(value: Any, *, expected_packet_id: str) -> dict[str, str]:
    raw_ref = _as_mapping(value)
    raw_packet_id = _required_str(raw_ref.get("packet_id"), "raw_ref.packet_id")
    if raw_packet_id != expected_packet_id:
        raise ValueError("coverage raw_ref.packet_id must match coverage packet_id")
    return {
        "packet_id": raw_packet_id,
        "file_id": _required_str(raw_ref.get("file_id"), "raw_ref.file_id"),
        "relative_packet_path": _required_str(
            raw_ref.get("relative_packet_path"), "raw_ref.relative_packet_path"
        ),
        "sha256": _required_str(raw_ref.get("sha256"), "raw_ref.sha256"),
        "hash_basis": _required_str(raw_ref.get("hash_basis"), "raw_ref.hash_basis"),
    }



def _raw_video_index_sequence_preserved(raw_video_indexes: list[int]) -> bool:
    return raw_video_indexes == list(range(len(raw_video_indexes)))


def _required_nonnegative_int(value: Any, label: str) -> int:
    parsed = _first_int(value)
    if parsed is None or parsed < 0:
        raise ValueError(f"TikTok batch projection requires non-negative {label}")
    return parsed


def _as_mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _first_str(*values: Any) -> str | None:
    for value in values:
        if value is None:
            continue
        text = value.strip() if isinstance(value, str) else str(value).strip()
        if text:
            return text
    return None


def _required_str(value: Any, label: str) -> str:
    parsed = _first_str(value)
    if parsed is None:
        raise ValueError(f"TikTok batch projection requires {label}")
    return parsed


def _first_int(*values: Any) -> int | None:
    for value in values:
        if value is None or isinstance(value, bool):
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return None


def _as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes"}:
            return True
        if lowered in {"false", "0", "no"}:
            return False
    return None


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value:
        text = _first_str(item)
        if text is not None:
            result.append(text)
    return result


def _int_mapping(value: Any) -> dict[str, int]:
    if not isinstance(value, Mapping):
        return {}
    result: dict[str, int] = {}
    for key, item in value.items():
        parsed = _first_int(item)
        if parsed is not None:
            result[str(key)] = parsed
    return dict(sorted(result.items()))


__all__ = [
    "TIKTOK_BATCH_PROJECTION_CERTIFICATION",
    "TIKTOK_BATCH_PROJECTION_METHOD",
    "TIKTOK_BATCH_PROJECTION_NON_CLAIMS",
    "TIKTOK_BATCH_PROJECTION_VERSION",
    "TikTokBatchProjectionLossLedger",
    "TikTokBatchProjectionPacket",
    "TikTokBatchProjectionRawAnchor",
    "TikTokBatchProjectionRawRef",
    "TikTokBatchProjectionRow",
    "build_tiktok_batch_projection_from_coverage",
    "build_tiktok_batch_projection_from_lake",
    "build_tiktok_batch_projection_from_packet_directory",
    "tiktok_batch_projection_json_text",
    "write_tiktok_batch_projection",
]
