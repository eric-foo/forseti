from __future__ import annotations

import json
from typing import Any, Literal, Mapping

from pydantic import Field, field_validator, model_validator

from schemas.case_models import StrictModel
from source_capture.models import PreservedFile, SourceCapturePacket, SourceCaptureSlice


REDDIT_PROJECTION_METHOD = "reddit_api_mechanical_projection"
REDDIT_PROJECTION_VERSION = "v0"
REDDIT_PROJECTION_CERTIFICATION = "view_only; not_cleaned; not_normalized; not_judgment_ready"

_FORBIDDEN_SOURCE_VISIBLE_FIELD_NAMES = frozenset(
    {
        "action_ceiling",
        "action_supporting",
        "credibility",
        "decision_strength",
        "demand",
        "discount",
        "exclude",
        "excluded",
        "inclusion",
        "integrity",
        "judgment",
        "signal_use",
        "strength",
        "strong",
        "weak",
    }
)


class ProjectionRawRef(StrictModel):
    packet_id: str
    slice_id: str


class ProjectionRawAnchor(StrictModel):
    file_id: str
    relative_packet_path: str
    sha256: str
    hash_basis: str
    json_pointer: str | None = None


class RedditProjectionRow(StrictModel):
    row_id: str
    row_kind: Literal["reddit_submission", "reddit_comment", "reddit_more_stub"]
    raw_ref: ProjectionRawRef
    raw_anchor: ProjectionRawAnchor
    parent_row_id: str | None = None
    reddit_kind: str | None = None
    reddit_id: str | None = None
    source_visible_fields: dict[str, Any | None] = Field(default_factory=dict)
    residuals: list[str] = Field(default_factory=list)

    @field_validator("source_visible_fields")
    @classmethod
    def reject_judgment_field_names(cls, value: dict[str, Any | None]) -> dict[str, Any | None]:
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "reddit projection source_visible_fields may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value


class RedditProjectionBinding(StrictModel):
    binding_type: Literal["reply_to_parent"]
    row_id: str
    parent_row_id: str
    raw_ref: ProjectionRawRef
    raw_anchor: ProjectionRawAnchor


class RedditProjectionLossEntry(StrictModel):
    category: Literal["REDDIT_LISTING_ENVELOPE"]
    count: int = Field(ge=0)
    raw_anchor: ProjectionRawAnchor
    reason: str


class RedditProjectionLossLedger(StrictModel):
    removed: list[RedditProjectionLossEntry] = Field(default_factory=list)
    preserved_evidence_rows: int = Field(ge=0)
    preserved_bindings: int = Field(ge=0)
    timing: Literal["separate_not_collapsed"] = "separate_not_collapsed"
    hierarchy_preserved: bool
    structure_preserved: bool
    certification: Literal["removes_source_envelope_only; does_not_certify_cleaning"] = (
        "removes_source_envelope_only; does_not_certify_cleaning"
    )


class RedditProjectionPacket(StrictModel):
    projection_method: Literal["reddit_api_mechanical_projection"] = REDDIT_PROJECTION_METHOD
    projection_version: Literal["v0"] = REDDIT_PROJECTION_VERSION
    certification: Literal["view_only; not_cleaned; not_normalized; not_judgment_ready"] = (
        REDDIT_PROJECTION_CERTIFICATION
    )
    packet_id: str
    rows: list[RedditProjectionRow] = Field(default_factory=list)
    binding_map: list[RedditProjectionBinding] = Field(default_factory=list)
    loss_ledger: RedditProjectionLossLedger
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_counts(self) -> "RedditProjectionPacket":
        if self.loss_ledger.preserved_evidence_rows != len(self.rows):
            raise ValueError("loss_ledger.preserved_evidence_rows must match rows length")
        if self.loss_ledger.preserved_bindings != len(self.binding_map):
            raise ValueError("loss_ledger.preserved_bindings must match binding_map length")
        return self


def build_reddit_api_projection(
    *,
    packet: SourceCapturePacket,
    raw_file_bytes_by_file_id: Mapping[str, bytes],
) -> RedditProjectionPacket:
    """Derive a traceable, mechanical Reddit row view from preserved packet bytes.

    This is not a parser authority, Cleaning transform, ECR schema, or Judgment
    read. It only projects the already-preserved Reddit API JSON into inspectable
    rows that carry packet/slice/file/hash anchors.
    """
    preserved_files = {item.file_id: item for item in packet.preserved_files}
    rows: list[RedditProjectionRow] = []
    bindings: list[RedditProjectionBinding] = []
    loss_entries: list[RedditProjectionLossEntry] = []
    residuals: list[str] = []

    for source_slice in packet.source_slices:
        for file_id in source_slice.preserved_file_ids:
            preserved_file = preserved_files[file_id]
            raw_anchor = _raw_anchor(preserved_file)
            raw_ref = ProjectionRawRef(packet_id=packet.packet_id, slice_id=source_slice.slice_id)
            body = raw_file_bytes_by_file_id.get(file_id)
            if body is None:
                raise ValueError(f"raw bytes are required for preserved file id: {file_id}")

            try:
                payload = json.loads(body)
            except json.JSONDecodeError:
                residuals.append(f"{source_slice.slice_id}:{file_id}:malformed_reddit_json")
                continue

            projected = _project_reddit_comments_payload(
                payload,
                raw_ref=raw_ref,
                raw_anchor=raw_anchor,
                source_slice=source_slice,
            )
            rows.extend(projected.rows)
            bindings.extend(projected.bindings)
            residuals.extend(projected.residuals)
            for envelope_json_pointer in projected.envelope_json_pointers:
                loss_entries.append(
                    RedditProjectionLossEntry(
                        category="REDDIT_LISTING_ENVELOPE",
                        count=1,
                        raw_anchor=_with_json_pointer(raw_anchor, envelope_json_pointer),
                        reason="reddit Listing wrapper flattened into anchored evidence rows",
                    )
                )

    return RedditProjectionPacket(
        packet_id=packet.packet_id,
        rows=rows,
        binding_map=bindings,
        loss_ledger=RedditProjectionLossLedger(
            removed=loss_entries,
            preserved_evidence_rows=len(rows),
            preserved_bindings=len(bindings),
            hierarchy_preserved=bool(rows)
            and all(row.parent_row_id is not None for row in rows if row.row_kind != "reddit_submission"),
            structure_preserved=not residuals,
        ),
        residuals=residuals,
    )


class _ProjectedPayload(StrictModel):
    rows: list[RedditProjectionRow] = Field(default_factory=list)
    bindings: list[RedditProjectionBinding] = Field(default_factory=list)
    residuals: list[str] = Field(default_factory=list)
    envelope_json_pointers: list[str] = Field(default_factory=list)


def _project_reddit_comments_payload(
    payload: object,
    *,
    raw_ref: ProjectionRawRef,
    raw_anchor: ProjectionRawAnchor,
    source_slice: SourceCaptureSlice,
) -> _ProjectedPayload:
    if not isinstance(payload, list) or len(payload) < 2:
        return _ProjectedPayload(
            residuals=[f"{source_slice.slice_id}:{raw_anchor.file_id}:unexpected_reddit_comments_shape"]
        )

    rows: list[RedditProjectionRow] = []
    bindings: list[RedditProjectionBinding] = []
    residuals: list[str] = []

    submission_data = _first_listing_child_data(payload[0])
    if submission_data is None:
        residuals.append(f"{source_slice.slice_id}:{raw_anchor.file_id}:submission_data_absent")
        submission_row_id: str | None = None
    else:
        submission_id = _string_or_none(submission_data.get("id"))
        submission_row_id = _row_id(source_slice.slice_id, "t3", submission_id)
        submission_residuals = []
        if submission_data.get("selftext") in {None, ""}:
            submission_residuals.append("submission_selftext_absent")
        rows.append(
            RedditProjectionRow(
                row_id=submission_row_id,
                row_kind="reddit_submission",
                reddit_kind="t3",
                reddit_id=submission_id,
                raw_ref=raw_ref,
                raw_anchor=_with_json_pointer(raw_anchor, "/0/data/children/0"),
                source_visible_fields=_source_visible_fields(
                    submission_data,
                    (
                        "id",
                        "name",
                        "title",
                        "selftext",
                        "author",
                        "created_utc",
                        "subreddit",
                        "permalink",
                        "score",
                        "num_comments",
                    ),
                ),
                residuals=submission_residuals,
            )
        )

    comments_listing = payload[1]
    comments_children = _listing_children(comments_listing)
    if comments_children is None:
        residuals.append(f"{source_slice.slice_id}:{raw_anchor.file_id}:comments_listing_absent")
    else:
        parent_for_top_level = submission_row_id
        for child_index, child in enumerate(comments_children):
            _project_comment_child(
                child,
                rows=rows,
                bindings=bindings,
                residuals=residuals,
                raw_ref=raw_ref,
                raw_anchor=raw_anchor,
                source_slice=source_slice,
                fallback_parent_row_id=parent_for_top_level,
                json_pointer=f"/1/data/children/{child_index}",
            )

    return _ProjectedPayload(
        rows=rows,
        bindings=bindings,
        residuals=residuals,
        envelope_json_pointers=["/0", "/1"],
    )


def _project_comment_child(
    child: object,
    *,
    rows: list[RedditProjectionRow],
    bindings: list[RedditProjectionBinding],
    residuals: list[str],
    raw_ref: ProjectionRawRef,
    raw_anchor: ProjectionRawAnchor,
    source_slice: SourceCaptureSlice,
    fallback_parent_row_id: str | None,
    json_pointer: str,
) -> None:
    if not isinstance(child, dict):
        residuals.append(f"{source_slice.slice_id}:{raw_anchor.file_id}:non_object_comment_child")
        return

    kind = _string_or_none(child.get("kind"))
    data = child.get("data")
    if not isinstance(data, dict):
        residuals.append(f"{source_slice.slice_id}:{raw_anchor.file_id}:{kind or 'unknown'}_data_absent")
        return

    if kind == "t1":
        comment_id = _string_or_none(data.get("id"))
        row_id = _row_id(source_slice.slice_id, "t1", comment_id)
        row_anchor = _with_json_pointer(raw_anchor, json_pointer)
        parent_row_id = _parent_row_id_from_raw(
            source_slice.slice_id,
            _string_or_none(data.get("parent_id")),
            fallback_parent_row_id=fallback_parent_row_id,
        )
        row_residuals = []
        if parent_row_id is None:
            row_residuals.append("comment_parent_missing")
        if data.get("body") in {None, ""}:
            row_residuals.append("comment_body_absent")
        rows.append(
            RedditProjectionRow(
                row_id=row_id,
                row_kind="reddit_comment",
                reddit_kind="t1",
                reddit_id=comment_id,
                parent_row_id=parent_row_id,
                raw_ref=raw_ref,
                raw_anchor=row_anchor,
                source_visible_fields=_source_visible_fields(
                    data,
                    ("id", "name", "parent_id", "link_id", "body", "author", "created_utc", "score", "permalink"),
                ),
                residuals=row_residuals,
            )
        )
        if parent_row_id is not None:
            bindings.append(
                RedditProjectionBinding(
                    binding_type="reply_to_parent",
                    row_id=row_id,
                    parent_row_id=parent_row_id,
                    raw_ref=raw_ref,
                    raw_anchor=row_anchor,
                )
            )
        replies = data.get("replies")
        if isinstance(replies, dict):
            nested_children = _listing_children(replies)
            if nested_children is None:
                residuals.append(f"{source_slice.slice_id}:{raw_anchor.file_id}:{row_id}:replies_listing_absent")
            else:
                for nested_index, nested_child in enumerate(nested_children):
                    _project_comment_child(
                        nested_child,
                        rows=rows,
                        bindings=bindings,
                        residuals=residuals,
                        raw_ref=raw_ref,
                        raw_anchor=raw_anchor,
                        source_slice=source_slice,
                        fallback_parent_row_id=row_id,
                        json_pointer=f"{json_pointer}/data/replies/data/children/{nested_index}",
                    )
        elif replies not in {None, ""}:
            residuals.append(f"{source_slice.slice_id}:{raw_anchor.file_id}:{row_id}:replies_unreadable")
        return

    if kind == "more":
        more_id = _string_or_none(data.get("id")) or _string_or_none(data.get("name"))
        row_id = _row_id(source_slice.slice_id, "more", more_id)
        row_anchor = _with_json_pointer(raw_anchor, json_pointer)
        parent_row_id = fallback_parent_row_id
        rows.append(
            RedditProjectionRow(
                row_id=row_id,
                row_kind="reddit_more_stub",
                reddit_kind="more",
                reddit_id=more_id,
                parent_row_id=parent_row_id,
                raw_ref=raw_ref,
                raw_anchor=row_anchor,
                source_visible_fields=_source_visible_fields(data, ("id", "name", "parent_id", "count", "children")),
                residuals=["more_stub_not_expanded"],
            )
        )
        if parent_row_id is not None:
            bindings.append(
                RedditProjectionBinding(
                    binding_type="reply_to_parent",
                    row_id=row_id,
                    parent_row_id=parent_row_id,
                    raw_ref=raw_ref,
                    raw_anchor=row_anchor,
                )
            )
        return

    residuals.append(f"{source_slice.slice_id}:{raw_anchor.file_id}:unsupported_reddit_kind:{kind or 'unknown'}")


def _raw_anchor(preserved_file: PreservedFile) -> ProjectionRawAnchor:
    return ProjectionRawAnchor(
        file_id=preserved_file.file_id,
        relative_packet_path=preserved_file.relative_packet_path,
        sha256=preserved_file.sha256,
        hash_basis=preserved_file.hash_basis,
    )


def _with_json_pointer(raw_anchor: ProjectionRawAnchor, json_pointer: str) -> ProjectionRawAnchor:
    return ProjectionRawAnchor(
        file_id=raw_anchor.file_id,
        relative_packet_path=raw_anchor.relative_packet_path,
        sha256=raw_anchor.sha256,
        hash_basis=raw_anchor.hash_basis,
        json_pointer=json_pointer,
    )


def _first_listing_child_data(listing: object) -> dict[str, Any] | None:
    children = _listing_children(listing)
    if not children:
        return None
    first = children[0]
    if not isinstance(first, dict):
        return None
    data = first.get("data")
    return data if isinstance(data, dict) else None


def _listing_children(listing: object) -> list[object] | None:
    if not isinstance(listing, dict):
        return None
    data = listing.get("data")
    if not isinstance(data, dict):
        return None
    children = data.get("children")
    return children if isinstance(children, list) else None


def _source_visible_fields(data: Mapping[str, object], keys: tuple[str, ...]) -> dict[str, Any | None]:
    return {key: data.get(key) for key in keys if key in data}


def _parent_row_id_from_raw(
    slice_id: str,
    parent_id: str | None,
    *,
    fallback_parent_row_id: str | None,
) -> str | None:
    if parent_id and "_" in parent_id:
        kind, reddit_id = parent_id.split("_", 1)
        if kind in {"t1", "t3"} and reddit_id:
            return _row_id(slice_id, kind, reddit_id)
    return fallback_parent_row_id


def _row_id(slice_id: str, reddit_kind: str, reddit_id: str | None) -> str:
    return f"{slice_id}:{reddit_kind}:{reddit_id or 'unknown'}"


def _string_or_none(value: object) -> str | None:
    # helper-delta: does not strip and is str-only, unlike harness_utils.string_or_none.
    return value if isinstance(value, str) and value else None


def _is_forbidden_field_name(key: str) -> bool:
    normalized = key.lower().replace("-", "_")
    parts = normalized.split("_")
    return any(
        token == normalized or token in parts or token in normalized
        for token in _FORBIDDEN_SOURCE_VISIBLE_FIELD_NAMES
    )


__all__ = [
    "REDDIT_PROJECTION_CERTIFICATION",
    "REDDIT_PROJECTION_METHOD",
    "REDDIT_PROJECTION_VERSION",
    "ProjectionRawAnchor",
    "ProjectionRawRef",
    "RedditProjectionBinding",
    "RedditProjectionLossEntry",
    "RedditProjectionLossLedger",
    "RedditProjectionPacket",
    "RedditProjectionRow",
    "build_reddit_api_projection",
]
