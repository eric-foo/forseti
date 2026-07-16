from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Mapping
from urllib.parse import urlparse

from pydantic import Field, field_validator, model_validator

from harness_utils import generate_ulid
from schemas.case_models import StrictModel
from source_capture.models import (
    CoverageWindow,
    MetricPosture,
    PreservedFile,
    SourceCapturePacket,
    SourceCaptureSlice,
    VisibleFactStatus,
)
from source_capture.projection_shared import (
    is_forbidden_field_token_match,
    read_packet_directory as _read_packet_directory,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


IG_PROJECTION_METHOD = "ig_creator_momentum_mechanical_projection"
IG_PROJECTION_VERSION = "v0"
IG_PROJECTION_CERTIFICATION = "view_only; not_cleaned; not_normalized; not_judgment_ready"

# Append-only derived lane namespace for the IG creator-momentum projection's Silver record.
PROJECTION_IG_LANE = "projection_ig"

_IG_SOURCE_FAMILY = "instagram_creator"
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


class IgProjectionRawRef(StrictModel):
    packet_id: str
    slice_id: str


class IgProjectionRawAnchor(StrictModel):
    file_id: str
    relative_packet_path: str
    sha256: str
    hash_basis: str
    json_pointer: str | None = None


class IgCreatorMomentumProjectionRow(StrictModel):
    row_id: str
    row_kind: Literal["ig_creator_metric", "ig_media_metric"]
    raw_ref: IgProjectionRawRef
    raw_anchor: IgProjectionRawAnchor
    entity_namespace: Literal["instagram"] = "instagram"
    entity_id: str | None = None
    username: str | None = None
    content_shortcode: str | None = None
    content_url: str | None = None
    content_kind: Literal["profile", "post", "reel", "unknown"]
    metric: str
    posture: MetricPosture
    value: int | None = None
    reason: str | None = None
    coverage_window: CoverageWindow | None = None
    capture_time: str | None = None
    source_publication_or_event: str | None = None
    source_visible_fields: dict[str, Any | None] = Field(default_factory=dict)
    residuals: list[str] = Field(default_factory=list)

    @field_validator("source_visible_fields")
    @classmethod
    def reject_judgment_field_names(cls, value: dict[str, Any | None]) -> dict[str, Any | None]:
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "IG projection source_visible_fields may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value

    @model_validator(mode="after")
    def validate_value_posture_coupling(self) -> "IgCreatorMomentumProjectionRow":
        if self.posture == MetricPosture.OBSERVED:
            if self.value is None:
                raise ValueError("an observed IG projection row requires a value")
            if self.reason is not None:
                raise ValueError("an observed IG projection row must not carry a reason")
            return self
        if self.value is not None:
            raise ValueError("a non-observed IG projection row must not carry a value")
        if not self.reason:
            raise ValueError("a non-observed IG projection row requires a reason")
        return self


class IgCreatorMomentumProjectionLossLedger(StrictModel):
    preserved_metric_rows: int = Field(ge=0)
    preserved_bindings: Literal[0] = 0
    identity_complete: bool
    structure_preserved: bool
    certification: Literal["mechanical_metric_observation_index; does_not_certify_momentum"] = (
        "mechanical_metric_observation_index; does_not_certify_momentum"
    )


class IgCreatorMomentumProjectionPacket(StrictModel):
    projection_method: Literal["ig_creator_momentum_mechanical_projection"] = IG_PROJECTION_METHOD
    projection_version: Literal["v0"] = IG_PROJECTION_VERSION
    certification: Literal["view_only; not_cleaned; not_normalized; not_judgment_ready"] = (
        IG_PROJECTION_CERTIFICATION
    )
    packet_id: str
    rows: list[IgCreatorMomentumProjectionRow] = Field(default_factory=list)
    binding_map: list[object] = Field(default_factory=list)
    loss_ledger: IgCreatorMomentumProjectionLossLedger
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_counts(self) -> "IgCreatorMomentumProjectionPacket":
        if self.loss_ledger.preserved_metric_rows != len(self.rows):
            raise ValueError("loss_ledger.preserved_metric_rows must match rows length")
        if self.binding_map:
            raise ValueError("IG projection v0 does not define bindings")
        return self


def build_ig_creator_momentum_projection(
    *,
    packet: SourceCapturePacket,
    raw_file_bytes_by_file_id: Mapping[str, bytes],
) -> IgCreatorMomentumProjectionPacket:
    """Derive a traceable, mechanical IG creator-momentum row view from a packet.

    This is not a scheduler, Cleaning transform, ECR schema, Judgment read, or
    momentum score. It only indexes typed metric observations already preserved
    on IG Source Capture Packet slices and carries packet/slice/file/hash anchors.
    """
    if packet.source_family != _IG_SOURCE_FAMILY:
        raise ValueError(
            f"IG projection requires source_family={_IG_SOURCE_FAMILY!r}; got {packet.source_family!r}"
        )

    preserved_files = {item.file_id: item for item in packet.preserved_files}
    for source_slice in packet.source_slices:
        for file_id in source_slice.preserved_file_ids:
            if file_id not in raw_file_bytes_by_file_id:
                raise ValueError(f"raw bytes are required for preserved file id: {file_id}")

    raw_context = _build_raw_context(
        packet=packet,
        preserved_files=preserved_files,
        raw_file_bytes_by_file_id=raw_file_bytes_by_file_id,
    )
    residuals = list(raw_context.residuals)
    if raw_context.numeric_id is None:
        residuals.append("ig_numeric_id_absent")

    rows: list[IgCreatorMomentumProjectionRow] = []
    for source_slice in packet.source_slices:
        raw_ref = IgProjectionRawRef(packet_id=packet.packet_id, slice_id=source_slice.slice_id)
        for metric_index, observation in enumerate(source_slice.metric_observations):
            row = _project_metric_observation(
                packet=packet,
                source_slice=source_slice,
                metric_index=metric_index,
                raw_ref=raw_ref,
                observation=observation,
                preserved_files=preserved_files,
                raw_context=raw_context,
            )
            rows.append(row)

    if not rows:
        residuals.append("ig_metric_observations_absent")

    return IgCreatorMomentumProjectionPacket(
        packet_id=packet.packet_id,
        rows=rows,
        loss_ledger=IgCreatorMomentumProjectionLossLedger(
            preserved_metric_rows=len(rows),
            identity_complete=raw_context.numeric_id is not None,
            structure_preserved=not residuals,
        ),
        residuals=residuals,
    )


def build_ig_creator_momentum_projection_from_packet_directory(
    *,
    packet_or_manifest_path: Path,
) -> IgCreatorMomentumProjectionPacket:
    packet, raw_file_bytes_by_file_id = _read_packet_directory(packet_or_manifest_path)
    return build_ig_creator_momentum_projection(
        packet=packet,
        raw_file_bytes_by_file_id=raw_file_bytes_by_file_id,
    )


def write_ig_creator_momentum_projection(
    *,
    packet_or_manifest_path: Path,
    output_path: Path,
    overwrite: bool = False,
) -> IgCreatorMomentumProjectionPacket:
    projection = build_ig_creator_momentum_projection_from_packet_directory(
        packet_or_manifest_path=packet_or_manifest_path,
    )
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_projection_json_text(projection), encoding="utf-8")
    return projection


def project_ig_creator_momentum_into_lake(
    *,
    data_root: "DataLakeRoot",
    packet_id: str,
    record_id: str | None = None,
) -> tuple[IgCreatorMomentumProjectionPacket, Path]:
    """Project a committed raw packet -- read by key from the lake and
    hash-verified -- into an IG creator-momentum projection, and append it as a
    derived record at ``derived/<packet_id>/projection_ig/<record_id>.json``
    (append-only; re-derive = new sibling).

    The verified read is the lake loader (``DataLakeRoot.load_raw_packet``), which
    closes the unverified-read gap of the directory path; the extraction is
    byte-identical to ``build_ig_creator_momentum_projection_from_packet_directory``.
    This adds no capture, fetch, Cleaning, ECR, or Judgment. Returns the
    projection and the derived record path.
    """
    loaded = data_root.load_raw_packet(packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    projection = build_ig_creator_momentum_projection(
        packet=packet,
        raw_file_bytes_by_file_id=loaded.bodies,
    )
    record = record_id if record_id is not None else generate_ulid()
    derived_path = data_root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=PROJECTION_IG_LANE,
        record_id=f"{record}.json",
        data=_projection_json_text(projection).encode("utf-8"),
    )
    return projection, derived_path




class _RawContext(StrictModel):
    username: str | None = None
    numeric_id: str | None = None
    metric_registry_version: str | None = None
    identity_conflict_policy_version: str | None = None
    profile_file_id: str | None = None
    momentum_file_id: str | None = None
    media_by_shortcode: dict[str, dict[str, Any | None]] = Field(default_factory=dict)
    raw_payload_by_file_id: dict[str, dict[str, Any | None]] = Field(default_factory=dict)
    residuals: list[str] = Field(default_factory=list)


def _build_raw_context(
    *,
    packet: SourceCapturePacket,
    preserved_files: Mapping[str, PreservedFile],
    raw_file_bytes_by_file_id: Mapping[str, bytes],
) -> _RawContext:
    context = _RawContext()
    for source_slice in packet.source_slices:
        for file_id in source_slice.preserved_file_ids:
            preserved_file = preserved_files[file_id]
            path = preserved_file.relative_packet_path.lower()
            if not path.endswith(".json"):
                continue
            try:
                payload = json.loads(raw_file_bytes_by_file_id[file_id])
            except json.JSONDecodeError:
                context.residuals.append(f"{source_slice.slice_id}:{file_id}:malformed_ig_json")
                continue
            if not isinstance(payload, dict):
                context.residuals.append(f"{source_slice.slice_id}:{file_id}:unexpected_ig_json_shape")
                continue
            context.raw_payload_by_file_id[file_id] = payload
            if path.endswith("ig_profile.json"):
                context.profile_file_id = file_id
            if path.endswith("ig_profile_momentum.json"):
                context.momentum_file_id = file_id
                context.username = _string_or_none(payload.get("username"))
                context.numeric_id = _string_or_none(payload.get("numeric_id"))
                context.metric_registry_version = _string_or_none(payload.get("metric_registry_version"))
                context.identity_conflict_policy_version = _string_or_none(
                    payload.get("identity_conflict_policy_version")
                )
                media = payload.get("media")
                if isinstance(media, dict):
                    context.media_by_shortcode = {
                        str(shortcode): item
                        for shortcode, item in media.items()
                        if isinstance(item, dict)
                    }
                else:
                    context.residuals.append(f"{source_slice.slice_id}:{file_id}:ig_media_map_absent")
    return context


def _project_metric_observation(
    *,
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
    metric_index: int,
    raw_ref: IgProjectionRawRef,
    observation,
    preserved_files: Mapping[str, PreservedFile],
    raw_context: _RawContext,
) -> IgCreatorMomentumProjectionRow:
    content_url = _known_value(source_slice.locator)
    content_kind = _content_kind(source_slice=source_slice, content_url=content_url)
    shortcode = _shortcode_from_url(content_url)
    media = raw_context.media_by_shortcode.get(shortcode or "") if shortcode is not None else None
    raw_anchor = _anchor_for_observation(
        observation_metric=observation.metric,
        source_slice=source_slice,
        metric_index=metric_index,
        preserved_files=preserved_files,
        raw_context=raw_context,
        shortcode=shortcode,
    )
    source_fields: dict[str, Any | None] = {
        "locator": content_url,
        "source_publication_or_event": _known_value(source_slice.timing.source_publication_or_event),
        "metric_registry_version": raw_context.metric_registry_version,
        "identity_conflict_policy_version": raw_context.identity_conflict_policy_version,
    }
    if media is not None:
        source_fields.update(
            {
                "is_video": media.get("is_video"),
                "taken_at_timestamp": media.get("taken_at_timestamp"),
            }
        )
    item_payload = _first_slice_payload(source_slice, raw_context=raw_context)
    if item_payload is not None:
        source_fields.update(
            {
                "status": item_payload.get("status"),
                "is_ad": item_payload.get("is_ad"),
                "caption_truncated": item_payload.get("caption_truncated"),
            }
        )

    row_kind: Literal["ig_creator_metric", "ig_media_metric"] = (
        "ig_creator_metric" if content_kind == "profile" else "ig_media_metric"
    )
    row_id = _row_id(packet_id=packet.packet_id, slice_id=source_slice.slice_id, metric=observation.metric)
    return IgCreatorMomentumProjectionRow(
        row_id=row_id,
        row_kind=row_kind,
        raw_ref=raw_ref,
        raw_anchor=raw_anchor,
        entity_id=raw_context.numeric_id,
        username=raw_context.username,
        content_shortcode=shortcode,
        content_url=content_url,
        content_kind=content_kind,
        metric=observation.metric,
        posture=observation.posture,
        value=observation.value,
        reason=observation.reason,
        coverage_window=observation.coverage_window,
        capture_time=_known_value(source_slice.timing.capture_time),
        source_publication_or_event=_known_value(source_slice.timing.source_publication_or_event),
        source_visible_fields={key: value for key, value in source_fields.items() if value is not None},
        residuals=[],
    )


def _anchor_for_observation(
    *,
    observation_metric: str,
    source_slice: SourceCaptureSlice,
    metric_index: int,
    preserved_files: Mapping[str, PreservedFile],
    raw_context: _RawContext,
    shortcode: str | None,
) -> IgProjectionRawAnchor:
    if observation_metric == "follower_count" and raw_context.momentum_file_id is not None:
        return _raw_anchor(preserved_files[raw_context.momentum_file_id], json_pointer="/follower_count")
    if observation_metric == "view_count" and shortcode and raw_context.momentum_file_id is not None:
        escaped_shortcode = _escape_json_pointer_token(shortcode)
        return _raw_anchor(
            preserved_files[raw_context.momentum_file_id],
            json_pointer=f"/media/{escaped_shortcode}/video_view_count",
        )
    item_file_id = _first_item_file_id(source_slice, preserved_files=preserved_files)
    if item_file_id is not None:
        pointer_by_metric = {
            "like_count": "/likes",
            "comment_count": "/comments",
        }
        return _raw_anchor(
            preserved_files[item_file_id],
            json_pointer=pointer_by_metric.get(observation_metric, f"/metric_observations/{metric_index}"),
        )
    fallback_file_id = source_slice.preserved_file_ids[0]
    return _raw_anchor(
        preserved_files[fallback_file_id],
        json_pointer=f"/metric_observations/{metric_index}",
    )


def _first_item_file_id(
    source_slice: SourceCaptureSlice, *, preserved_files: Mapping[str, PreservedFile]
) -> str | None:
    for file_id in source_slice.preserved_file_ids:
        if "ig_call_" in preserved_files[file_id].relative_packet_path.lower():
            return file_id
    return None


def _first_slice_payload(source_slice: SourceCaptureSlice, *, raw_context: _RawContext) -> dict[str, Any | None] | None:
    for file_id in source_slice.preserved_file_ids:
        payload = raw_context.raw_payload_by_file_id.get(file_id)
        if payload is not None:
            return payload
    return None


def _raw_anchor(preserved_file: PreservedFile, *, json_pointer: str | None = None) -> IgProjectionRawAnchor:
    return IgProjectionRawAnchor(
        file_id=preserved_file.file_id,
        relative_packet_path=preserved_file.relative_packet_path,
        sha256=preserved_file.sha256,
        hash_basis=preserved_file.hash_basis,
        json_pointer=json_pointer,
    )


def _known_value(fact) -> str | None:
    return fact.value if fact.status == VisibleFactStatus.KNOWN else None


def _content_kind(
    *, source_slice: SourceCaptureSlice, content_url: str | None
) -> Literal["profile", "post", "reel", "unknown"]:
    if source_slice.slice_id.startswith("ig_profile"):
        return "profile"
    if content_url is None:
        return "unknown"
    path_parts = [part for part in urlparse(content_url).path.split("/") if part]
    if len(path_parts) >= 2 and path_parts[-2] == "p":
        return "post"
    if len(path_parts) >= 2 and path_parts[-2] == "reel":
        return "reel"
    return "unknown"


def _shortcode_from_url(url: str | None) -> str | None:
    if url is None:
        return None
    path_parts = [part for part in urlparse(url).path.split("/") if part]
    if len(path_parts) >= 2 and path_parts[-2] in {"p", "reel"}:
        return path_parts[-1]
    return None


def _row_id(*, packet_id: str, slice_id: str, metric: str) -> str:
    return f"{packet_id}:{slice_id}:{metric}"


def _projection_json_text(projection: IgCreatorMomentumProjectionPacket) -> str:
    return f"{json.dumps(projection.model_dump(mode='json'), indent=2, sort_keys=True)}\n"


def _escape_json_pointer_token(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _string_or_none(value: object) -> str | None:
    # helper-delta: does not strip and is str-only, unlike harness_utils.string_or_none.
    return value if isinstance(value, str) and value else None


def _is_forbidden_field_name(key: str) -> bool:
    return is_forbidden_field_token_match(key, _FORBIDDEN_SOURCE_VISIBLE_FIELD_NAMES)


__all__ = [
    "IG_PROJECTION_CERTIFICATION",
    "IG_PROJECTION_METHOD",
    "IG_PROJECTION_VERSION",
    "PROJECTION_IG_LANE",
    "IgCreatorMomentumProjectionLossLedger",
    "IgCreatorMomentumProjectionPacket",
    "IgCreatorMomentumProjectionRow",
    "IgProjectionRawAnchor",
    "IgProjectionRawRef",
    "build_ig_creator_momentum_projection",
    "build_ig_creator_momentum_projection_from_packet_directory",
    "project_ig_creator_momentum_into_lake",
    "write_ig_creator_momentum_projection",
]
