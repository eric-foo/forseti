"""Mechanical projection over an IG `/reels/` grid Source Capture Packet.

Sibling to ``ig_projection.py`` (the legacy creator-momentum/calls surface). Both
project the SAME ``source_family="instagram_creator"`` capture family, so they
share the doctrine primitives (the forbidden-field guard, raw ref/anchor models,
the safe packet-directory reader), but they consume DIFFERENT capture shapes:

- ``ig_projection`` reads ``ig_profile_momentum.json`` / ``ig_call_*.json``.
- this module reads the reels-grid packet whose one preserved file is
  ``ig_reels_grid_capture.json`` (``joined_rows[].source_surface_candidates[]``).

The reels capture runner (`run_source_capture_ig_reels_grid_packet.py`) already
selects ONE preferred source surface per metric (`_preferred_candidate`) and
stores only that selected value on each slice's ``metric_observations`` -- which
have no ``source_surface`` field and therefore COLLAPSE the cross-surface
disagreement (e.g. DOM 2,984 vs web_profile_info 655 vs /clips/user 2,984). The
disagreement survives only in the preserved ``ig_reels_grid_capture.json``.

This projection re-unites the two: it carries the slice's selected value+posture
verbatim when JSON joined, promotes parseable DOM-grid counts only when JSON did
not join, and re-attaches every source surface's value for that metric from the
preserved capture file. It is mechanical and re-derivable: it carries raw facts
and anchors, computes ``chosen_source_surface`` from the chosen source, and
enforces the spec's static ``view_count = not_applicable`` rule. It is not
Cleaning, ECR, Judgment, a momentum/traction score, or a capture path.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Mapping
from urllib.parse import urlparse

from pydantic import Field, field_validator, model_validator

from harness_utils import generate_ulid
from schemas.case_models import StrictModel
from source_capture.ig_projection import (
    IgProjectionRawAnchor,
    IgProjectionRawRef,
    _is_forbidden_field_name,  # reused to single-source the doctrine forbidden-name invariant
    _read_packet_directory,  # reused to single-source the packet-relative path-traversal guard
)
from source_capture.ig_reels_grid import (
    CLIPS_USER_JSON_METADATA,
    DOM_GRID_ENGAGEMENT,
    MEDIA_KIND_POST,
    PROFILE_FEED_JSON_METADATA,
    WEB_PROFILE_INFO_JSON_METADATA,
    shortcode_from_path,
)
from source_capture.models import (
    CoverageWindow,
    MetricPosture,
    PreservedFile,
    SourceCapturePacket,
    SourceCaptureSlice,
    VisibleFactStatus,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


IG_REELS_PROJECTION_METHOD = "ig_reels_grid_mechanical_projection"
IG_REELS_PROJECTION_VERSION = "v0"
IG_REELS_PROJECTION_CERTIFICATION = "view_only; not_cleaned; not_normalized; not_judgment_ready"

# Append-only derived lane namespace for the IG reels-grid projection's Silver record.
PROJECTION_IG_REELS_GRID_LANE = "projection_ig_reels_grid"

_IG_SOURCE_FAMILY = "instagram_creator"
_CAPTURE_FILE_BASENAME = "ig_reels_grid_capture.json"

# Mirrors the capture runner's `_preferred_candidate` JSON-surface order. It is a
# mechanical, versioned policy (pinned by the capture file's selection_policy_version),
# used ONLY to pick a representative candidate for raw source-visible facts -- never to
# re-decide which numeric value is "right" (that selection already happened upstream and
# is carried verbatim from the slice's metric_observation).
_SURFACE_PREFERENCE = {
    CLIPS_USER_JSON_METADATA: 0,
    WEB_PROFILE_INFO_JSON_METADATA: 1,
    PROFILE_FEED_JSON_METADATA: 2,
}

_STATIC_VIEW_COUNT_NOT_APPLICABLE_REASON = "static_post_view_count_not_applicable"

# Which capture-file field carries each metric, per surface.
_DOM_TEXT_KEY_BY_METRIC = {
    "view_count": "views_text",
    "like_count": "likes_text",
    "comment_count": "comments_text",
}
_JSON_KEY_BY_METRIC = {
    "view_count": "video_or_play_count",
    "like_count": "like_count",
    "comment_count": "comment_count",
}


class IgReelsSurfaceCountCandidate(StrictModel):
    """One source surface's value for a single metric on one media row.

    Carries the per-surface disagreement that the slice's selected
    ``metric_observation`` collapses. ``value`` is the parsed integer when the
    surface exposed a count; ``raw_text`` preserves the unparsed DOM string for
    the DOM surface (None for JSON surfaces, which expose native integers).
    """

    source_surface: str
    value: int | None = None
    raw_text: str | None = None


class IgReelsGridProjectionRow(StrictModel):
    row_id: str
    row_kind: Literal["ig_creator_metric", "ig_media_metric"]
    raw_ref: IgProjectionRawRef
    raw_anchor: IgProjectionRawAnchor
    entity_namespace: Literal["instagram"] = "instagram"
    username: str | None = None
    content_shortcode: str | None = None
    content_url: str | None = None
    content_kind: Literal["profile", "post", "reel", "unknown"]
    metric: str
    # Carried verbatim from the capture slice's metric_observation (the selection the
    # runner already made). posture/value coupling mirrors models.MetricObservation.
    posture: MetricPosture
    value: int | None = None
    reason: str | None = None
    coverage_window: CoverageWindow | None = None
    # --- reels enrichment: source-surface provenance + disagreement + selection audit ---
    chosen_source_surface: str | None = None
    source_surface_count_candidates: list[IgReelsSurfaceCountCandidate] = Field(default_factory=list)
    join_status: Literal[
        "joined_by_shortcode", "missing_json", "missing_shortcode", "ambiguous", "not_applicable"
    ]
    selection_policy_version: str | None = None
    selection_limitations: list[str] = Field(default_factory=list)
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
                "IG reels projection source_visible_fields may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value

    @model_validator(mode="after")
    def validate_value_posture_coupling(self) -> "IgReelsGridProjectionRow":
        if self.posture == MetricPosture.OBSERVED:
            if self.value is None:
                raise ValueError("an observed IG reels projection row requires a value")
            if self.reason is not None:
                raise ValueError("an observed IG reels projection row must not carry a reason")
            return self
        if self.value is not None:
            raise ValueError("a non-observed IG reels projection row must not carry a value")
        if not self.reason:
            raise ValueError("a non-observed IG reels projection row requires a reason")
        return self


class IgReelsGridProjectionLossLedger(StrictModel):
    preserved_metric_rows: int = Field(ge=0)
    preserved_bindings: Literal[0] = 0
    source_surfaces_observed: list[str] = Field(default_factory=list)
    static_view_count_not_applicable_rows: int = Field(ge=0, default=0)
    structure_preserved: bool
    certification: Literal[
        "mechanical_source_surface_reconciliation_index; does_not_certify_traction"
    ] = "mechanical_source_surface_reconciliation_index; does_not_certify_traction"


class IgReelsGridProjectionPacket(StrictModel):
    projection_method: Literal["ig_reels_grid_mechanical_projection"] = IG_REELS_PROJECTION_METHOD
    projection_version: Literal["v0"] = IG_REELS_PROJECTION_VERSION
    certification: Literal["view_only; not_cleaned; not_normalized; not_judgment_ready"] = (
        IG_REELS_PROJECTION_CERTIFICATION
    )
    packet_id: str
    selection_policy_version: str | None = None
    rows: list[IgReelsGridProjectionRow] = Field(default_factory=list)
    binding_map: list[object] = Field(default_factory=list)
    loss_ledger: IgReelsGridProjectionLossLedger
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_counts(self) -> "IgReelsGridProjectionPacket":
        if self.loss_ledger.preserved_metric_rows != len(self.rows):
            raise ValueError("loss_ledger.preserved_metric_rows must match rows length")
        if self.binding_map:
            raise ValueError("IG reels projection v0 does not define bindings")
        return self


def build_ig_reels_grid_projection(
    *,
    packet: SourceCapturePacket,
    raw_file_bytes_by_file_id: Mapping[str, bytes],
) -> IgReelsGridProjectionPacket:
    """Project an IG reels-grid packet into mechanical, source-surface-preserving rows.

    Carries the selected metric value+posture from each slice and re-attaches every
    source surface's value for that metric from the preserved capture file, so the
    cross-surface disagreement is recoverable downstream. Adds no capture, fetch,
    Cleaning, ECR, or Judgment.
    """
    if packet.source_family != _IG_SOURCE_FAMILY:
        raise ValueError(
            f"IG reels projection requires source_family={_IG_SOURCE_FAMILY!r}; got {packet.source_family!r}"
        )

    preserved_files = {item.file_id: item for item in packet.preserved_files}
    for source_slice in packet.source_slices:
        for file_id in source_slice.preserved_file_ids:
            if file_id not in raw_file_bytes_by_file_id:
                raise ValueError(f"raw bytes are required for preserved file id: {file_id}")

    capture_file = _capture_preserved_file(packet.preserved_files)
    if capture_file is None:
        raise ValueError(
            f"IG reels projection requires a preserved {_CAPTURE_FILE_BASENAME}; "
            "this packet is not an IG reels-grid capture"
        )
    capture_payload = _load_capture_payload(capture_file, raw_file_bytes_by_file_id)
    selection_policy_version = _capture_selection_policy_version(capture_payload)
    joined_rows = capture_payload.get("joined_rows")
    joined_index_by_shortcode, duplicate_shortcodes = _joined_index_by_shortcode(joined_rows)
    snapshot = capture_payload.get("creator_profile_snapshot")
    username = snapshot.get("source_profile") if isinstance(snapshot, dict) else None

    rows: list[IgReelsGridProjectionRow] = []
    residuals: list[str] = []
    static_not_applicable_rows = 0
    surfaces_observed: set[str] = set()

    for source_slice in packet.source_slices:
        raw_ref = IgProjectionRawRef(packet_id=packet.packet_id, slice_id=source_slice.slice_id)
        is_profile = source_slice.slice_id.startswith("ig_reels_profile")
        if is_profile:
            for observation in source_slice.metric_observations:
                row = _project_profile_observation(
                    source_slice=source_slice,
                    observation=observation,
                    raw_ref=raw_ref,
                    capture_file=capture_file,
                    snapshot=snapshot if isinstance(snapshot, dict) else None,
                    username=_string_or_none(username),
                    selection_policy_version=selection_policy_version,
                )
                rows.append(row)
                for residual in row.residuals:
                    _append_residual_once(residuals, residual)
                _record_surfaces(surfaces_observed, row)
            continue

        shortcode = _shortcode_from_locator(source_slice.locator)
        joined_index = joined_index_by_shortcode.get(shortcode or "")
        join_status_override: Literal["missing_shortcode", "missing_json", "ambiguous"] | None = None
        row_residuals: list[str] = []
        if shortcode is None:
            residual = f"ig_reels_locator_shortcode_absent:{source_slice.slice_id}"
            _append_residual_once(residuals, residual)
            row_residuals.append(residual)
            join_status_override = "missing_shortcode"
        elif joined_index is None:
            residual = f"ig_reels_joined_row_absent:{shortcode}"
            _append_residual_once(residuals, residual)
            row_residuals.append(residual)
            join_status_override = "missing_json"
        elif shortcode in duplicate_shortcodes:
            residual = f"ig_reels_ambiguous_shortcode_join:{shortcode}"
            _append_residual_once(residuals, residual)
            row_residuals.append(residual)
            join_status_override = "ambiguous"
            joined_index = None
        joined_row = _joined_row_at(joined_rows, joined_index)
        content_kind = _media_content_kind(source_slice=source_slice, joined_row=joined_row)
        for observation in source_slice.metric_observations:
            row, forced_static = _project_media_observation(
                source_slice=source_slice,
                observation=observation,
                raw_ref=raw_ref,
                capture_file=capture_file,
                joined_row=joined_row,
                joined_index=joined_index,
                shortcode=shortcode,
                content_kind=content_kind,
                username=_string_or_none(username),
                selection_policy_version=selection_policy_version,
                join_status_override=join_status_override,
                row_residuals=row_residuals,
            )
            rows.append(row)
            _record_surfaces(surfaces_observed, row)
            if forced_static:
                static_not_applicable_rows += 1

    if not rows:
        residuals.append("ig_reels_metric_observations_absent")

    return IgReelsGridProjectionPacket(
        packet_id=packet.packet_id,
        selection_policy_version=selection_policy_version,
        rows=rows,
        loss_ledger=IgReelsGridProjectionLossLedger(
            preserved_metric_rows=len(rows),
            source_surfaces_observed=sorted(surfaces_observed),
            static_view_count_not_applicable_rows=static_not_applicable_rows,
            structure_preserved=not residuals,
        ),
        residuals=residuals,
    )


def build_ig_reels_grid_projection_from_packet_directory(
    *,
    packet_or_manifest_path: Path,
) -> IgReelsGridProjectionPacket:
    packet, raw_file_bytes_by_file_id = _read_packet_directory(packet_or_manifest_path)
    return build_ig_reels_grid_projection(
        packet=packet,
        raw_file_bytes_by_file_id=raw_file_bytes_by_file_id,
    )


def write_ig_reels_grid_projection(
    *,
    packet_or_manifest_path: Path,
    output_path: Path,
    overwrite: bool = False,
) -> IgReelsGridProjectionPacket:
    projection = build_ig_reels_grid_projection_from_packet_directory(
        packet_or_manifest_path=packet_or_manifest_path,
    )
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_projection_json_text(projection), encoding="utf-8")
    return projection


def project_ig_reels_grid_into_lake(
    *,
    data_root: "DataLakeRoot",
    packet_id: str,
    record_id: str | None = None,
) -> tuple[IgReelsGridProjectionPacket, Path]:
    """Project a committed raw IG reels-grid packet into an append-only derived record.

    The packet is read by key through ``DataLakeRoot.load_raw_packet``, so preserved
    files are re-hashed against the manifest before projection. The derived record
    is appended at ``derived/<shard>/<packet_id>/projection_ig_reels_grid/<record-id>.json``.
    This adds no capture, Cleaning, ECR, Judgment, or creator-profile rollup.
    """
    loaded = data_root.load_raw_packet(packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    projection = build_ig_reels_grid_projection(
        packet=packet,
        raw_file_bytes_by_file_id=loaded.bodies,
    )
    record = record_id if record_id is not None else generate_ulid()
    derived_path = data_root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=PROJECTION_IG_REELS_GRID_LANE,
        record_id=f"{record}.json",
        data=_projection_json_text(projection).encode("utf-8"),
    )
    return projection, derived_path

def _project_profile_observation(
    *,
    source_slice: SourceCaptureSlice,
    observation,
    raw_ref: IgProjectionRawRef,
    capture_file: PreservedFile,
    snapshot: dict[str, Any | None] | None,
    username: str | None,
    selection_policy_version: str | None,
) -> IgReelsGridProjectionRow:
    candidates: list[IgReelsSurfaceCountCandidate] = []
    if snapshot is not None and observation.metric == "follower_count":
        snapshot_value = _int_or_none(snapshot.get("follower_count"))
        if snapshot_value is not None:
            candidates.append(
                IgReelsSurfaceCountCandidate(
                    source_surface=WEB_PROFILE_INFO_JSON_METADATA, value=snapshot_value
                )
            )
    source_fields = _profile_source_visible_fields(snapshot)
    anchor_pointer, residuals = _profile_anchor_pointer(snapshot=snapshot, metric=observation.metric)
    return IgReelsGridProjectionRow(
        row_id=_row_id(packet_id=raw_ref.packet_id, slice_id=source_slice.slice_id, metric=observation.metric),
        row_kind="ig_creator_metric",
        raw_ref=raw_ref,
        raw_anchor=_anchor(capture_file, json_pointer=anchor_pointer),
        username=username,
        content_kind="profile",
        metric=observation.metric,
        posture=observation.posture,
        value=observation.value,
        reason=observation.reason,
        coverage_window=observation.coverage_window,
        chosen_source_surface=_chosen_surface(observation.value, candidates),
        source_surface_count_candidates=candidates,
        join_status="not_applicable",
        selection_policy_version=selection_policy_version,
        selection_limitations=list(source_slice.limitations),
        capture_time=_known_value(source_slice.timing.capture_time),
        source_publication_or_event=_known_value(source_slice.timing.source_publication_or_event),
        source_visible_fields=source_fields,
        residuals=residuals,
    )


def _project_media_observation(
    *,
    source_slice: SourceCaptureSlice,
    observation,
    raw_ref: IgProjectionRawRef,
    capture_file: PreservedFile,
    joined_row: dict[str, Any] | None,
    joined_index: int | None,
    shortcode: str | None,
    content_kind: Literal["profile", "post", "reel", "unknown"],
    username: str | None,
    selection_policy_version: str | None,
    join_status_override: Literal["missing_shortcode", "missing_json", "ambiguous"] | None = None,
    row_residuals: list[str] | None = None,
) -> tuple[IgReelsGridProjectionRow, bool]:
    dom_row = joined_row.get("dom_row") if isinstance(joined_row, dict) else None
    json_candidates = joined_row.get("source_surface_candidates") if isinstance(joined_row, dict) else None
    json_candidates = json_candidates if isinstance(json_candidates, list) else []
    candidates = _media_surface_candidates(
        metric=observation.metric,
        dom_row=dom_row if isinstance(dom_row, dict) else None,
        json_candidates=json_candidates,
    )
    join_status: Literal[
        "joined_by_shortcode", "missing_json", "missing_shortcode", "ambiguous", "not_applicable"
    ]
    if join_status_override is not None:
        join_status = join_status_override
    else:
        join_status = "joined_by_shortcode" if json_candidates else "missing_json"

    posture = observation.posture
    value = observation.value
    reason = observation.reason
    forced_static = False
    dom_grid_fallback = False
    row_residuals = list(row_residuals or [])
    selection_limitations = list(source_slice.limitations)
    # Static-post enforcement (spec: static view_count is not_applicable, never a number).
    # Belt-and-suspenders: the reels runner already filters /p/ rows out of the traction
    # series, so this normally never fires; it keeps a static row that slips through from
    # ever promoting a visible number into view_count downstream.
    if content_kind == MEDIA_KIND_POST and observation.metric == "view_count" and posture == MetricPosture.OBSERVED:
        posture = MetricPosture.NOT_APPLICABLE
        value = None
        reason = _STATIC_VIEW_COUNT_NOT_APPLICABLE_REASON
        forced_static = True
    elif posture == MetricPosture.UNAVAILABLE_WITH_REASON and content_kind == "reel":
        dom_value = _dom_grid_candidate_value(candidates)
        if dom_value is not None:
            posture = MetricPosture.OBSERVED
            value = dom_value
            reason = None
            dom_grid_fallback = True
            selection_limitations.append("metric_value_from_dom_grid_no_passive_json_join")
            row_residuals.append(f"ig_reels_dom_grid_metric_promoted:{observation.metric}")

    content_url = _known_value(source_slice.locator)
    pointer = f"/joined_rows/{joined_index}" if joined_index is not None else None
    row = IgReelsGridProjectionRow(
        row_id=_row_id(packet_id=raw_ref.packet_id, slice_id=source_slice.slice_id, metric=observation.metric),
        row_kind="ig_media_metric",
        raw_ref=raw_ref,
        raw_anchor=_anchor(capture_file, json_pointer=pointer),
        username=username,
        content_shortcode=shortcode,
        content_url=content_url,
        content_kind=content_kind,
        metric=observation.metric,
        posture=posture,
        value=value,
        reason=reason,
        coverage_window=observation.coverage_window,
        chosen_source_surface=DOM_GRID_ENGAGEMENT
        if dom_grid_fallback
        else _chosen_surface(value if posture == MetricPosture.OBSERVED else None, candidates),
        source_surface_count_candidates=candidates,
        join_status=join_status,
        selection_policy_version=selection_policy_version,
        selection_limitations=selection_limitations,
        capture_time=_known_value(source_slice.timing.capture_time),
        source_publication_or_event=_known_value(source_slice.timing.source_publication_or_event),
        source_visible_fields=_media_source_visible_fields(json_candidates),
        residuals=row_residuals,
    )
    return row, forced_static


def _media_surface_candidates(
    *,
    metric: str,
    dom_row: dict[str, Any] | None,
    json_candidates: list[Any],
) -> list[IgReelsSurfaceCountCandidate]:
    candidates: list[IgReelsSurfaceCountCandidate] = []
    dom_key = _DOM_TEXT_KEY_BY_METRIC.get(metric)
    if dom_row is not None and dom_key is not None:
        dom_text = _string_or_none(dom_row.get(dom_key))
        candidates.append(
            IgReelsSurfaceCountCandidate(
                source_surface=DOM_GRID_ENGAGEMENT,
                value=_int_or_none(dom_text),
                raw_text=dom_text,
            )
        )
    json_key = _JSON_KEY_BY_METRIC.get(metric)
    if json_key is not None:
        for candidate in json_candidates:
            if not isinstance(candidate, dict):
                continue
            # Carry every joined surface, even when its value for this metric is None:
            # "surface present for this shortcode but exposed no count" is itself part of
            # the cross-surface disagreement and must not be silently dropped.
            candidates.append(
                IgReelsSurfaceCountCandidate(
                    source_surface=_string_or_none(candidate.get("source_surface")) or "unknown",
                    value=_int_or_none(candidate.get(json_key)),
                )
            )
    return candidates


def _dom_grid_candidate_value(candidates: list[IgReelsSurfaceCountCandidate]) -> int | None:
    for candidate in candidates:
        if candidate.source_surface == DOM_GRID_ENGAGEMENT and candidate.value is not None:
            return candidate.value
    return None


def _chosen_surface(selected_value: int | None, candidates: list[IgReelsSurfaceCountCandidate]) -> str | None:
    """Attribute the carried (already-selected) value to the surface it matches.

    Decision-free: it does not re-rank or re-pick a value, only reports which
    surface holds the value the upstream selection already chose. None when the
    metric is non-observed or no surface matches.
    """
    if selected_value is None:
        return None
    # Attribute upstream JSON-selected values to the surface the runner would have used:
    # JSON surfaces in the capture's preference order first, DOM/unknown last. DOM-grid
    # fallback is handled explicitly before this helper.
    for candidate in sorted(
        candidates, key=lambda item: _SURFACE_PREFERENCE.get(item.source_surface, 99)
    ):
        # For an already-observed upstream value, DOM is carried for disagreement but is not
        # attributed as the JSON-selected source surface.
        if candidate.source_surface == DOM_GRID_ENGAGEMENT:
            continue
        if candidate.value == selected_value:
            return candidate.source_surface
    return None


def _media_source_visible_fields(json_candidates: list[Any]) -> dict[str, Any | None]:
    # Row-level raw metadata taken from the preferred (clips_user-first) joined candidate.
    # This is per-row metadata for the shortcode, independent of which surface produced the
    # carried numeric value (chosen_source_surface); both describe the same media row.
    preferred = _preferred_candidate(json_candidates)
    if preferred is None:
        return {}
    caption_text = _string_or_none(preferred.get("caption_text"))
    fields: dict[str, Any | None] = {
        "product_type": _string_or_none(preferred.get("product_type")),
        "typename": _string_or_none(preferred.get("typename")),
        "is_video": preferred.get("is_video") if isinstance(preferred.get("is_video"), bool) else None,
        "taken_at_utc": _string_or_none(preferred.get("taken_at_utc")),
        "caption_present": caption_text is not None,
        "caption_length": _int_or_none(preferred.get("caption_length")) or 0,
        # Raw source-visible ad-candidate facts, carried as candidates only (never an
        # ad/sponsorship CONCLUSION -- that stays Judgment-owned). Field names are
        # deliberately *_candidate so they read as raw facts, not classifications.
        "is_paid_partnership_candidate": preferred.get("is_paid_partnership")
        if isinstance(preferred.get("is_paid_partnership"), bool)
        else None,
        "is_affiliate_candidate": preferred.get("is_affiliate")
        if isinstance(preferred.get("is_affiliate"), bool)
        else None,
        "sponsor_user_candidate_count": _list_len(preferred.get("sponsor_users")),
        "ad_term_candidate_count": _list_len(preferred.get("ad_term_candidates")),
        "pinned_on_clips_tab": preferred.get("pinned_on_clips_tab")
        if isinstance(preferred.get("pinned_on_clips_tab"), bool)
        else None,
        "pinned_on_timeline": preferred.get("pinned_on_timeline")
        if isinstance(preferred.get("pinned_on_timeline"), bool)
        else None,
    }
    return {key: value for key, value in fields.items() if value is not None}


def _profile_source_visible_fields(snapshot: dict[str, Any | None] | None) -> dict[str, Any | None]:
    if snapshot is None:
        return {}
    fields: dict[str, Any | None] = {
        "numeric_id_present": snapshot.get("numeric_id") is not None,
        "category_name": _string_or_none(snapshot.get("category_name")),
        "is_verified": snapshot.get("is_verified") if isinstance(snapshot.get("is_verified"), bool) else None,
        "is_private": snapshot.get("is_private") if isinstance(snapshot.get("is_private"), bool) else None,
        "bio_links_count": _int_or_none(snapshot.get("bio_links_count")),
        "following_count": _int_or_none(snapshot.get("following_count")),
        "post_or_media_count": _int_or_none(snapshot.get("post_or_media_count")),
        "parse_status": _string_or_none(snapshot.get("parse_status")),
    }
    return {key: value for key, value in fields.items() if value is not None}


def _profile_anchor_pointer(
    *, snapshot: dict[str, Any | None] | None, metric: str
) -> tuple[str | None, list[str]]:
    if snapshot is None:
        return None, [f"ig_reels_profile_snapshot_absent:{metric}"]
    if metric in snapshot:
        return f"/creator_profile_snapshot/{_escape_json_pointer_token(metric)}", []
    return "/creator_profile_snapshot", [f"ig_reels_profile_metric_field_absent:{metric}"]


def _preferred_candidate(json_candidates: list[Any]) -> dict[str, Any] | None:
    usable = [candidate for candidate in json_candidates if isinstance(candidate, dict)]
    if not usable:
        return None
    return sorted(
        usable,
        key=lambda item: _SURFACE_PREFERENCE.get(_string_or_none(item.get("source_surface")) or "", 99),
    )[0]


def _capture_preserved_file(preserved_files: list[PreservedFile]) -> PreservedFile | None:
    for preserved_file in preserved_files:
        if preserved_file.relative_packet_path.replace("\\", "/").endswith(_CAPTURE_FILE_BASENAME):
            return preserved_file
    return None


def _load_capture_payload(
    capture_file: PreservedFile, raw_file_bytes_by_file_id: Mapping[str, bytes]
) -> dict[str, Any]:
    raw_bytes = raw_file_bytes_by_file_id[capture_file.file_id]
    try:
        payload = json.loads(raw_bytes)
    except json.JSONDecodeError as exc:
        raise ValueError(f"malformed {_CAPTURE_FILE_BASENAME}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"unexpected {_CAPTURE_FILE_BASENAME} shape: expected a JSON object")
    return payload


def _capture_selection_policy_version(capture_payload: dict[str, Any]) -> str | None:
    metadata = capture_payload.get("capture_metadata")
    if isinstance(metadata, dict):
        return _string_or_none(metadata.get("selection_policy_version"))
    return None


def _joined_index_by_shortcode(joined_rows: object) -> tuple[dict[str, int], set[str]]:
    index_by_shortcode: dict[str, int] = {}
    duplicate_shortcodes: set[str] = set()
    if not isinstance(joined_rows, list):
        return index_by_shortcode, duplicate_shortcodes
    for index, joined in enumerate(joined_rows):
        if not isinstance(joined, dict):
            continue
        dom_row = joined.get("dom_row")
        shortcode = _string_or_none(dom_row.get("shortcode")) if isinstance(dom_row, dict) else None
        if shortcode is None:
            continue
        if shortcode in index_by_shortcode:
            # A shortcode appearing in two joined rows makes a by-shortcode anchor ambiguous;
            # record it so the build loop residualizes rather than silently anchoring to the first.
            duplicate_shortcodes.add(shortcode)
        else:
            index_by_shortcode[shortcode] = index
    return index_by_shortcode, duplicate_shortcodes


def _joined_row_at(joined_rows: object, index: int | None) -> dict[str, Any] | None:
    if index is None or not isinstance(joined_rows, list) or index >= len(joined_rows):
        return None
    joined = joined_rows[index]
    return joined if isinstance(joined, dict) else None


def _media_content_kind(
    *, source_slice: SourceCaptureSlice, joined_row: dict[str, Any] | None
) -> Literal["profile", "post", "reel", "unknown"]:
    if isinstance(joined_row, dict):
        dom_row = joined_row.get("dom_row")
        kind = _string_or_none(dom_row.get("kind")) if isinstance(dom_row, dict) else None
        if kind in {"reel", "post"}:
            return kind  # type: ignore[return-value]
    content_url = _known_value(source_slice.locator)
    if content_url is None:
        return "unknown"
    path_parts = [part for part in urlparse(content_url).path.split("/") if part]
    if len(path_parts) >= 2 and path_parts[-2] == "reel":
        return "reel"
    if len(path_parts) >= 2 and path_parts[-2] == "p":
        return "post"
    return "unknown"


def _shortcode_from_locator(locator) -> str | None:
    content_url = _known_value(locator)
    if content_url is None:
        return None
    return shortcode_from_path(urlparse(content_url).path)


def _record_surfaces(surfaces_observed: set[str], row: IgReelsGridProjectionRow) -> None:
    for candidate in row.source_surface_count_candidates:
        surfaces_observed.add(candidate.source_surface)


def _append_residual_once(residuals: list[str], residual: str) -> None:
    if residual not in residuals:
        residuals.append(residual)


def _anchor(preserved_file: PreservedFile, *, json_pointer: str | None) -> IgProjectionRawAnchor:
    return IgProjectionRawAnchor(
        file_id=preserved_file.file_id,
        relative_packet_path=preserved_file.relative_packet_path,
        sha256=preserved_file.sha256,
        hash_basis=preserved_file.hash_basis,
        json_pointer=json_pointer,
    )


def _row_id(*, packet_id: str, slice_id: str, metric: str) -> str:
    return f"{packet_id}:{slice_id}:{metric}"


def _known_value(fact) -> str | None:
    return fact.value if fact.status == VisibleFactStatus.KNOWN else None


def _projection_json_text(projection: IgReelsGridProjectionPacket) -> str:
    return f"{json.dumps(projection.model_dump(mode='json'), indent=2, sort_keys=True)}\n"


def _escape_json_pointer_token(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _string_or_none(value: object) -> str | None:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    return None


def _int_or_none(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        stripped = value.replace(",", "").strip()
        if stripped.isdigit():
            return int(stripped)
        compact = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)([KkMm])", stripped)
        if compact:
            multiplier = 1000 if compact.group(2).lower() == "k" else 1000000
            return int(float(compact.group(1)) * multiplier)
    return None

def _list_len(value: object) -> int | None:
    if isinstance(value, (list, tuple)):
        return len(value)
    return None


__all__ = [
    "IG_REELS_PROJECTION_CERTIFICATION",
    "IG_REELS_PROJECTION_METHOD",
    "IG_REELS_PROJECTION_VERSION",
    "IgReelsGridProjectionLossLedger",
    "IgReelsGridProjectionPacket",
    "IgReelsGridProjectionRow",
    "IgReelsSurfaceCountCandidate",
    "PROJECTION_IG_REELS_GRID_LANE",
    "build_ig_reels_grid_projection",
    "build_ig_reels_grid_projection_from_packet_directory",
    "project_ig_reels_grid_into_lake",
    "write_ig_reels_grid_projection",
]
