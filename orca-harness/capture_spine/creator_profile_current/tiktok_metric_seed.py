"""Build a TikTok creator-metric document from committed batch-admission lake
packets.

The TikTok half of the metric-parity capture->registry loop, mirroring the live
YouTube path (``youtube_watch_packet_metric_document.py``): committed
``tiktok_creator_batch_comment_subtitle_admission`` SourceCapturePackets ->
this builder -> the TikTok Silver producer
(``tiktok_silver_metric_producer.derive_tiktok_creator_metric_silver_records_from_seed``)
-> snapshot -> materialize. The preserved ``tiktok_batch_capture.json`` carries
per-video source-native ``stats`` integers (playCount, diggCount, commentCount,
shareCount, collectCount); this builder maps them to metric observations
(playCount -> ``view_count``, diggCount -> ``like_count``, commentCount ->
``total_comment_count``, shareCount -> ``share_count``, collectCount ->
``collect_count``) and derives one engagement rollup per creator account.

Posture rules (the load-bearing honesty contract of this layer):

- A stats key PRESENT with an integer value is an ``observed`` metric.
- A stats key ABSENT from a video's preserved stats object is a LOUD GAP: an
  ``unavailable_with_reason`` observation (null value + reason). Absent metrics
  are NEVER zero-filled -- the batch writer's ``_normalize_stats`` 0-default is
  a batch-summary-sum convention that must not leak into this seed layer.
- A stats value that is present but NOT an integer (a rounded display string
  like ``"1.2M"``, a float, a boolean) FAILS CLOSED: it is corrupted or
  non-source-native material, not a gap (mirrors the YouTube badge-route
  posture).
- ``engagement_rate = round((sum(like_count) + sum(total_comment_count)) /
  sum(view_count), 6)`` over videos with ALL THREE engagement inputs observed
  (the IG recipe shape); rollup math never mixes partial-input videos.

Identity stays fenced: this builder never derives accounts. Callers supply an
explicit ``account_id_by_handle`` map (from the linkage ledger's TikTok rows
and/or an operator-attested map); a captured creator handle with no mapping
fails closed rather than minting an identity.

Boundary: this module is PURE -- it reads verified lake packets and returns the
document; it writes nothing and never touches the linkage ledger. Appending
Silver records is the producer's job (via the operator runner).

Accepted residuals (named, not hidden):
- The batch writer zero-fills missing stats keys at packet-write time, so a
  source-absent stat in an already-written packet can arrive here as a literal
  0 that this layer cannot distinguish from a real zero. This layer treats
  absent KEYS as gaps and integer values as observed; retroactively un-zeroing
  upstream fill is out of scope (upgrade trigger: the batch writer preserves
  per-stat presence postures).
- shareCount/collectCount are preserved as observed metrics but are NOT rollup
  inputs; the engagement recipe uses the view/like/comment trio only.
"""
from __future__ import annotations

import json
import statistics
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Mapping

from data_lake.root import raw_shard
from source_capture.tiktok.batch_packet import (
    TIKTOK_BATCH_CAPTURE_JSON_NAME,
    TIKTOK_BATCH_CAPTURE_SURFACE,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot

TIKTOK_BATCH_CREATOR_METRIC_SEED_WRAPPER = "tiktok_batch_creator_metric_seed"
TIKTOK_BATCH_METRIC_DOCUMENT_SCHEMA_VERSION = "tiktok_batch_creator_metric_document_v0"
TIKTOK_BATCH_METRIC_DOCUMENT_ID = "tiktok_batch_creator_metric_document_v0"
TIKTOK_BATCH_METRIC_RECIPE_VERSION = "creator_metric_rollup_tiktok_profile_grid_engagement_v0"
TIKTOK_BATCH_METRIC_REGISTRY_VERSION = "creator_metric_tiktok_batch_admission_v0"

TIKTOK_BATCH_OPERATOR_CATEGORY = "tiktok_batch_admission_cli_operator"

_PLATFORM = "tiktok"
# Ordered metric-name -> preserved source-native stats key. The first three are
# the engagement trio the rollup recipe consumes; share/collect are preserved
# observations only.
_STATS_KEY_BY_METRIC = {
    "view_count": "playCount",
    "like_count": "diggCount",
    "total_comment_count": "commentCount",
    "share_count": "shareCount",
    "collect_count": "collectCount",
}
_ENGAGEMENT_METRIC_ORDER = ("view_count", "like_count", "total_comment_count")


class TiktokBatchMetricDocumentError(ValueError):
    """Raised when the TikTok metric document cannot be built trustworthily.
    Subclasses ``ValueError`` so existing fail-closed ``except ValueError``
    paths still catch it; ``reason`` is the machine-readable code and
    ``subject`` names the packet/handle/video it failed on (``""`` for a
    run-level failure)."""

    def __init__(self, reason: str, subject: str, detail: str) -> None:
        self.reason = reason
        self.subject = subject
        prefix = f"{reason} for {subject!r}" if subject else reason
        super().__init__(f"{prefix}: {detail}")


@dataclass(frozen=True)
class TiktokBatchCapture:
    """One verified batch-packet read for one creator: the selected packet id,
    its preserved capture payload (``tiktok_batch_capture.json``), the
    lake-relative pointer to that preserved file, and the manifest's
    hash-checkable provenance for it."""

    packet_id: str
    creator_handle: str
    capture_timestamp: str
    payload: Mapping[str, Any]
    capture_json_pointer: str
    capture_file_id: str
    capture_relative_packet_path: str
    capture_json_sha256: str
    capture_hash_basis: str


def discover_latest_tiktok_batch_captures(
    data_root: "DataLakeRoot",
) -> dict[str, TiktokBatchCapture]:
    """Resolve every captured TikTok creator handle to its latest committed
    batch-admission packet, via verified lake reads. Returns
    ``{casefolded_handle: capture}``.

    "Latest" is the packet with the newest ``capture_timestamp``; two DISTINCT
    packets tying on the timestamp for the same handle fail closed
    (``ambiguous_creator_packet``) rather than picking silently. A lake with no
    committed batch-admission packets fails closed (``no_tiktok_batch_packets``)
    -- an empty pool is a loud condition, not an empty success. The caller
    ensures the availability index is current (the operator runner rebuilds it
    first)."""
    candidates: dict[str, list[TiktokBatchCapture]] = {}
    for packet_id in data_root.list_available(source_family=_PLATFORM):
        entry = data_root.read_availability(packet_id)
        if not entry or entry.get("source_surface") != TIKTOK_BATCH_CAPTURE_SURFACE:
            continue
        capture = _load_batch_capture(data_root, packet_id)
        candidates.setdefault(capture.creator_handle.casefold(), []).append(capture)

    if not candidates:
        raise TiktokBatchMetricDocumentError(
            "no_tiktok_batch_packets",
            "",
            "no committed tiktok_creator_batch_comment_subtitle_admission packet is "
            "available in the lake; refusing to build an empty metric document",
        )
    return {
        handle: _select_latest_capture(handle, found) for handle, found in candidates.items()
    }


def build_tiktok_batch_creator_metric_seed_document(
    data_root: "DataLakeRoot",
    *,
    account_id_by_handle: Mapping[str, str],
    generated_at_utc: str,
) -> dict[str, Any]:
    """Build the seed-shaped TikTok metric document from committed batch packets.

    Consumable directly by
    ``derive_tiktok_creator_metric_silver_records_from_seed`` (same wrapper
    key). Fails closed on: no committed batch packet, an unreadable/invalid
    preserved capture, distinct packets tying on capture_timestamp for one
    handle, a video row without a ``video_id``, a non-integer stats value, a
    captured handle with no account mapping, and an account whose batch yields
    no complete engagement-input video."""
    accounts = _normalized_account_map(account_id_by_handle)
    captures = discover_latest_tiktok_batch_captures(data_root)

    observations: list[dict[str, Any]] = []
    rollups: list[dict[str, Any]] = []
    source_inputs: list[dict[str, Any]] = []
    for rollup_index, handle_key in enumerate(sorted(captures), start=1):
        capture = captures[handle_key]
        account_id = accounts.get(handle_key)
        if account_id is None:
            raise TiktokBatchMetricDocumentError(
                "missing_account_mapping",
                capture.creator_handle,
                f"captured TikTok creator handle @{capture.creator_handle} has no platform "
                "account mapping; identity additions are a separate owner-gated lane -- "
                "supply --account-map handle=account_id or add the tiktok account to the "
                "linkage ledger",
            )
        source_inputs.append(
            {
                "source_pointer": capture.capture_json_pointer,
                "sha256": capture.capture_json_sha256,
                "role": (
                    f"TikTok batch-admission capture for @{capture.creator_handle} "
                    "(verified lake read; sha256 is the preserved capture JSON)"
                ),
            }
        )
        video_rows = _video_metric_rows(capture)
        account_observations: list[dict[str, Any]] = []
        for row in video_rows:
            for metric_name in _STATS_KEY_BY_METRIC:
                account_observations.append(
                    _metric_observation(
                        capture=capture,
                        row=row,
                        metric_name=metric_name,
                        account_id=account_id,
                        sequence=len(observations) + len(account_observations) + 1,
                    )
                )
        observations.extend(account_observations)
        rollups.append(
            _rollup(
                capture=capture,
                account_id=account_id,
                video_rows=video_rows,
                account_observations=account_observations,
                generated_at_utc=generated_at_utc,
                rollup_index=rollup_index,
            )
        )

    complete_video_ids = {
        observation_id
        for rollup in rollups
        for observation_id in rollup["source_metric_observation_ids"]
    }
    document = {
        "schema_version": TIKTOK_BATCH_METRIC_DOCUMENT_SCHEMA_VERSION,
        "seed_id": TIKTOK_BATCH_METRIC_DOCUMENT_ID,
        "seed_mode": "tiktok_batch_admission_metric_document",
        "generated_at_utc": generated_at_utc,
        "source_policy_posture": (
            "Metric document generated from committed TikTok batch-admission "
            "SourceCapturePackets in the data lake (verified by-key reads). Rows are "
            "account-scoped capture-time observations for the creator's captured "
            "profile-grid batch, not full-account history, not cross-platform linkage, "
            "not SQLite/runtime storage, and not dashboard readiness."
        ),
        "authority_pointers": [
            "forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md",
            "forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md",
            "forseti/product/spines/capture/core/source_families/social_media/tiktok/tiktok_capture_lane_spec_v0.md",
        ],
        "source_inputs": source_inputs,
        "selection_policy": {
            "included": (
                "videos preserved in the latest committed batch-admission packet per "
                "captured creator handle"
            ),
            "packet_selection_rule": (
                "latest capture_timestamp per creator handle; distinct packets tying on "
                "the timestamp fail closed rather than being clock-trusted"
            ),
            "rollup_scope": "platform_account only; no creator_record or cross-platform rollups",
            "metric_value_rule": (
                "only source-native integer stats values are stored as observed; a stats "
                "key absent from a video is an unavailable_with_reason gap and absent "
                "metrics are never zero-filled; a non-integer stats value fails closed"
            ),
            "engagement_rate_recipe": (
                "(sum(like_count) + sum(total_comment_count)) / sum(view_count) over "
                "videos with all three inputs observed"
            ),
            "representativeness_rule": (
                "Average and median view rollups are directional profile-grid batch "
                "statistics only. They must carry sample_support and must not be "
                "presented as representative creator averages."
            ),
        },
        "counts": {
            "creator_batches_selected": len(captures),
            "metric_observations_total": len(observations),
            "observed_metric_observations_total": sum(
                1 for item in observations if item["metric_posture"] == "observed"
            ),
            "unavailable_metric_observations_total": sum(
                1 for item in observations if item["metric_posture"] != "observed"
            ),
            "unique_platform_accounts_with_observations": len(
                {item["platform_account_id"] for item in observations}
            ),
            "metric_rollups_total": len(rollups),
            "rollup_source_observations_total": len(complete_video_ids),
            "engagement_rate_rollups_observed": sum(
                1
                for rollup in rollups
                if rollup["metric_rollups"]["engagement_rate"]["posture"] == "observed"
            ),
        },
        "metric_observations": observations,
        "metric_rollups": rollups,
        "accepted_residuals": [
            "The rollups are profile-grid batch statistics, not full-account creator averages.",
            "Latest-packet-per-handle selection orders by capture_timestamp; distinct packets tying on the timestamp fail closed rather than being clock-trusted.",
            "shareCount/collectCount are preserved as observed metrics but are not rollup inputs.",
            "The batch writer zero-fills missing stats keys at packet-write time, so a source-absent stat in an already-written packet can arrive as a literal 0 this layer cannot distinguish from a real zero; absent KEYS remain loud gaps.",
        ],
        "non_claims": [
            "not full-account creator average",
            "not follower or audience graph",
            "not cross-platform identity linkage",
            "not creator_record rollup",
            "not buyer proof",
            "not validation or readiness",
            "not admission or identity-ledger change authorization",
            "not dashboard implementation",
        ],
    }
    return {TIKTOK_BATCH_CREATOR_METRIC_SEED_WRAPPER: document}


def _normalized_account_map(account_id_by_handle: Mapping[str, str]) -> dict[str, str]:
    """Casefold + strip the map's handle keys (dropping a leading ``@``), fail
    closed on blank entries or on two spellings colliding onto one handle."""
    normalized: dict[str, str] = {}
    for handle, account_id in account_id_by_handle.items():
        if not isinstance(handle, str) or not handle.strip():
            raise TiktokBatchMetricDocumentError(
                "invalid_account_map", str(handle), "account map handle must be a non-empty string"
            )
        if not isinstance(account_id, str) or not account_id.strip():
            raise TiktokBatchMetricDocumentError(
                "invalid_account_map", handle, "account map account_id must be a non-empty string"
            )
        key = handle.strip().lstrip("@").casefold()
        if key in normalized and normalized[key] != account_id.strip():
            raise TiktokBatchMetricDocumentError(
                "invalid_account_map",
                handle,
                f"handle maps to conflicting account ids: {normalized[key]!r} vs {account_id!r}",
            )
        normalized[key] = account_id.strip()
    return normalized


# -- packet reading -----------------------------------------------------------

def _load_batch_capture(data_root: "DataLakeRoot", packet_id: str) -> TiktokBatchCapture:
    loaded = data_root.load_raw_packet(packet_id)
    operator_category = loaded.manifest.get("operator_category")
    if operator_category != TIKTOK_BATCH_OPERATOR_CATEGORY:
        raise TiktokBatchMetricDocumentError(
            "operator_category_mismatch",
            packet_id,
            f"batch-admission surface packet carries operator_category "
            f"{operator_category!r}, expected {TIKTOK_BATCH_OPERATOR_CATEGORY!r}; "
            "refusing to treat a mismatched identity seam as admission",
        )
    # The packet writer preserves each staged artifact as "<NN>_<original_name>",
    # so match on the original filename after the index prefix.
    capture_entry: Mapping[str, Any] | None = None
    for entry in loaded.manifest.get("preserved_files", []):
        if not isinstance(entry, Mapping):
            continue
        basename = str(entry.get("relative_packet_path", "")).rsplit("/", 1)[-1]
        original_name = basename.split("_", 1)[1] if "_" in basename else basename
        if original_name == TIKTOK_BATCH_CAPTURE_JSON_NAME:
            capture_entry = entry
            break
    if capture_entry is None:
        raise TiktokBatchMetricDocumentError(
            "invalid_batch_packet",
            packet_id,
            f"packet does not preserve {TIKTOK_BATCH_CAPTURE_JSON_NAME!r}",
        )
    try:
        payload = json.loads(loaded.bodies[capture_entry["file_id"]].decode("utf-8"))
    except (KeyError, UnicodeDecodeError, ValueError) as exc:
        raise TiktokBatchMetricDocumentError(
            "invalid_batch_packet",
            packet_id,
            f"unreadable {TIKTOK_BATCH_CAPTURE_JSON_NAME}: {exc}",
        ) from exc
    creator_handle = payload.get("creator_handle")
    capture_timestamp = payload.get("capture_timestamp")
    if not isinstance(creator_handle, str) or not creator_handle.strip():
        raise TiktokBatchMetricDocumentError(
            "invalid_batch_packet", packet_id, "capture payload lacks creator_handle"
        )
    if not isinstance(capture_timestamp, str) or not capture_timestamp.strip():
        raise TiktokBatchMetricDocumentError(
            "invalid_batch_packet", packet_id, "capture payload lacks capture_timestamp"
        )
    return TiktokBatchCapture(
        packet_id=packet_id,
        creator_handle=creator_handle.strip(),
        capture_timestamp=capture_timestamp,
        payload=payload,
        capture_json_pointer=(
            f"raw/{raw_shard(packet_id)}/{packet_id}/{capture_entry['relative_packet_path']}"
        ),
        capture_file_id=str(capture_entry["file_id"]),
        capture_relative_packet_path=str(capture_entry["relative_packet_path"]),
        capture_json_sha256=str(capture_entry["sha256"]),
        capture_hash_basis=str(capture_entry.get("hash_basis") or "raw_stored_bytes"),
    )


def _select_latest_capture(handle: str, found: list[TiktokBatchCapture]) -> TiktokBatchCapture:
    ranked = sorted(found, key=lambda capture: _parse_instant(capture.capture_timestamp))
    latest = ranked[-1]
    ties = [
        capture
        for capture in ranked
        if capture.packet_id != latest.packet_id
        and _parse_instant(capture.capture_timestamp) == _parse_instant(latest.capture_timestamp)
    ]
    if ties:
        raise TiktokBatchMetricDocumentError(
            "ambiguous_creator_packet",
            handle,
            f"distinct packets tie on capture_timestamp {latest.capture_timestamp!r}: "
            f"{sorted([latest.packet_id, *(capture.packet_id for capture in ties)])}",
        )
    return latest


def _parse_instant(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


# -- per-video row extraction -------------------------------------------------

def _video_metric_rows(capture: TiktokBatchCapture) -> list[dict[str, Any]]:
    videos = capture.payload.get("videos")
    if not isinstance(videos, list) or not videos:
        raise TiktokBatchMetricDocumentError(
            "invalid_batch_packet",
            capture.packet_id,
            "capture payload carries no videos list",
        )
    rows: list[dict[str, Any]] = []
    seen_video_ids: set[str] = set()
    for video_index, video in enumerate(videos):
        video = video if isinstance(video, Mapping) else {}
        video_id = video.get("video_id")
        if not isinstance(video_id, str) or not video_id.strip():
            raise TiktokBatchMetricDocumentError(
                "invalid_batch_packet",
                capture.packet_id,
                f"videos[{video_index}] lacks a video_id; refusing to emit an "
                "unanchored observation",
            )
        if video_id in seen_video_ids:
            raise TiktokBatchMetricDocumentError(
                "invalid_batch_packet",
                capture.packet_id,
                f"videos[{video_index}] repeats video_id {video_id!r}; duplicate rows "
                "would blur rollup lineage",
            )
        seen_video_ids.add(video_id)
        stats = video.get("stats")
        stats = stats if isinstance(stats, Mapping) else {}
        metric_values: dict[str, int | None] = {}
        for metric_name, stats_key in _STATS_KEY_BY_METRIC.items():
            if stats_key not in stats:
                metric_values[metric_name] = None  # loud gap, never 0
                continue
            value = stats[stats_key]
            if isinstance(value, bool) or not isinstance(value, int):
                raise TiktokBatchMetricDocumentError(
                    "non_integer_stat",
                    video_id,
                    f"stats.{stats_key} carries a non-integer value {value!r}; a rounded "
                    "display string is not a source-native exact count",
                )
            metric_values[metric_name] = value
        rows.append(
            {
                "video_index": video_index,
                "video_id": video_id,
                "video_url": video.get("video_url"),
                "create_time_utc": video.get("create_time_utc"),
                "metric_values": metric_values,
            }
        )
    return rows


# -- observation / rollup construction ---------------------------------------

def _metric_observation(
    *,
    capture: TiktokBatchCapture,
    row: Mapping[str, Any],
    metric_name: str,
    account_id: str,
    sequence: int,
) -> dict[str, Any]:
    stats_key = _STATS_KEY_BY_METRIC[metric_name]
    value = row["metric_values"][metric_name]
    observed = value is not None
    json_pointer = f"/videos/{row['video_index']}/stats/{stats_key}"
    return {
        "metric_observation_id": f"tiktok_batch_metric_obs_v0_{sequence:03d}",
        "platform_account_id": account_id,
        "profile_subject_kind": "platform_account",
        "profile_subject_id": account_id,
        "creator_record_id_or_none": None,
        "platform": _PLATFORM,
        "platform_subject_key_type": "tiktok_public_handle",
        "platform_subject_key": capture.creator_handle,
        "creator_handle_query": capture.creator_handle,
        "content_id_or_none": row["video_id"],
        "content_url_or_none": row["video_url"],
        "content_kind": "video",
        "content_publication_or_event_time_or_none": row["create_time_utc"],
        "metric_name": metric_name,
        "metric_value_or_none": value,
        "metric_unit": "count",
        "metric_posture": "observed" if observed else "unavailable_with_reason",
        "posture_reason_or_none": (
            None
            if observed
            else (
                f"{stats_key} is absent from the preserved profile-grid stats for this "
                "video; absent metrics are never zero-filled"
            )
        ),
        "source_pointer": f"{capture.capture_json_pointer}#{json_pointer}",
        "source_field": json_pointer,
        "source_file": capture.capture_json_pointer,
        "source_row_id_or_none": f"{capture.packet_id}:{row['video_id']}:{metric_name}",
        "source_packet_id_or_none": capture.packet_id,
        "source_packet_pointer_or_none": None,
        "raw_anchor": {
            "file_id": capture.capture_file_id,
            "relative_packet_path": capture.capture_relative_packet_path,
            "json_pointer": json_pointer,
            "sha256": capture.capture_json_sha256,
            "hash_basis": capture.capture_hash_basis,
        },
        "observed_at": capture.capture_timestamp,
        "observed_at_source": "tiktok_batch_capture_timestamp",
        "capture_window_start_or_none": None,
        "capture_window_end_or_none": None,
        "metric_registry_version": TIKTOK_BATCH_METRIC_REGISTRY_VERSION,
        "limitation_notes": [
            "Metric is source-visible at batch-admission capture time and may change after capture.",
            "Observation belongs to the creator's captured profile-grid batch, not a full account crawl.",
        ],
    }


def _rollup(
    *,
    capture: TiktokBatchCapture,
    account_id: str,
    video_rows: list[dict[str, Any]],
    account_observations: list[dict[str, Any]],
    generated_at_utc: str,
    rollup_index: int,
) -> dict[str, Any]:
    complete = [
        row
        for row in video_rows
        if all(row["metric_values"][metric] is not None for metric in _ENGAGEMENT_METRIC_ORDER)
    ]
    if not complete:
        raise TiktokBatchMetricDocumentError(
            "no_complete_video_trios",
            account_id,
            "no captured video exposes view, like, and comment counts together for "
            f"@{capture.creator_handle}; refusing an input-free rollup",
        )
    views = [row["metric_values"]["view_count"] for row in complete]
    likes = [row["metric_values"]["like_count"] for row in complete]
    comments = [row["metric_values"]["total_comment_count"] for row in complete]
    denominator = sum(views)
    engagement_rate = (
        round((sum(likes) + sum(comments)) / denominator, 6) if denominator > 0 else None
    )

    observation_id_by_video_metric = {
        (observation["content_id_or_none"], observation["metric_name"]): observation[
            "metric_observation_id"
        ]
        for observation in account_observations
        if observation["metric_posture"] == "observed"
    }
    source_ids = [
        observation_id_by_video_metric[(row["video_id"], metric)]
        for row in complete
        for metric in _ENGAGEMENT_METRIC_ORDER
    ]
    observation_count = len(source_ids)
    sample_adequacy = _sample_support_label(observation_count)

    return {
        "metric_rollup_id": f"tiktok_batch_account_engagement_rollup_v0_{rollup_index:03d}",
        "profile_subject_kind": "platform_account",
        "profile_subject_id": account_id,
        "creator_record_id_or_none": None,
        "platform_scope": _PLATFORM,
        "platform_account_ids": [account_id],
        "platform_subject_key_type": "tiktok_public_handle",
        "platform_subject_key": capture.creator_handle,
        "public_handle": capture.creator_handle,
        "rollup_window": "custom",
        "rollup_window_description": (
            "latest_tiktok_batch_admission_profile_grid_v0; not a full-account history window"
        ),
        "content_kind_inclusion_rule": (
            "TikTok videos preserved in the creator's captured profile-grid batch "
            "admission only; shareCount/collectCount observations are excluded from "
            "rollup math"
        ),
        "metric_rollups": {
            "average_views": _observed_metric(round(statistics.mean(views), 2), "count"),
            "median_views": _observed_metric(round(statistics.median(views), 2), "count"),
            "engagement_rate": (
                _observed_metric(engagement_rate, "rate")
                if engagement_rate is not None
                else _unavailable_metric(
                    "view_count denominator was zero across the complete-input videos", "rate"
                )
            ),
            "average_like_count": _observed_metric(round(statistics.mean(likes), 2), "count"),
            "average_comment_count": _observed_metric(round(statistics.mean(comments), 2), "count"),
            "posting_cadence": _not_attempted_metric(
                "cadence recipe is out of scope for this TikTok metric document", "rate"
            ),
            "recent_velocity": _not_attempted_metric(
                "velocity recipe is out of scope for this TikTok metric document", "rate"
            ),
        },
        "source_metric_observation_ids": source_ids,
        "observation_count": observation_count,
        "view_count_min": min(views),
        "view_count_max": max(views),
        "calculation_recipe_version": TIKTOK_BATCH_METRIC_RECIPE_VERSION,
        "computed_at": generated_at_utc,
        "freshness_state": "partial",
        "limitations": [
            "Rollup covers the creator's captured profile-grid batch selection only; it is not a full-account average.",
            "View, like, comment, share, and collect counts are capture-time observations and may have changed since capture.",
            "Engagement metrics are computed over complete-input videos only (view, like, and comment counts all observed); partial-input videos are named gaps, never zero-filled.",
            (
                f"Engagement inputs are complete for {len(complete)} of {len(video_rows)} "
                "captured videos."
            ),
            "Cross-platform rollups are not authorized without promoted public-handle linkage evidence.",
            (
                f"Average/median views are computed over {len(complete)} complete-input videos "
                f"({observation_count} metric observations); sample adequacy is {sample_adequacy} "
                "and the value is not a representative creator average."
            ),
            "Profile-grid selection can bias view averages relative to the creator's full TikTok output.",
        ],
        "sample_support": {
            "observation_count": observation_count,
            "sample_adequacy": sample_adequacy,
            "representativeness_posture": "admitted_pool_only_not_representative_creator_average",
            "surface_handling": _surface_handling(observation_count),
        },
    }


def _observed_metric(value: int | float | None, unit: str) -> dict[str, Any]:
    if value is None:
        raise ValueError("observed metric value must not be None")
    return {"value_or_none": value, "posture": "observed", "metric_unit": unit}


def _unavailable_metric(reason: str, unit: str) -> dict[str, Any]:
    return {
        "value_or_none": None,
        "posture": "unavailable_with_reason",
        "posture_reason_or_none": reason,
        "metric_unit": unit,
    }


def _not_attempted_metric(reason: str, unit: str) -> dict[str, Any]:
    return {
        "value_or_none": None,
        "posture": "not_attempted",
        "posture_reason_or_none": reason,
        "metric_unit": unit,
    }


def _sample_support_label(observation_count: int) -> str:
    if observation_count <= 3:
        return "thin_n_1_to_3"
    if observation_count <= 7:
        return "limited_n_4_to_7"
    return "stronger_admitted_pool_n_8_plus"


def _surface_handling(observation_count: int) -> str:
    if observation_count <= 3:
        return "downgrade_or_withhold_summary_claim"
    return "show_only_with_visible_admitted_pool_limitation"


__all__ = [
    "TIKTOK_BATCH_CREATOR_METRIC_SEED_WRAPPER",
    "TIKTOK_BATCH_METRIC_DOCUMENT_SCHEMA_VERSION",
    "TIKTOK_BATCH_METRIC_RECIPE_VERSION",
    "TIKTOK_BATCH_METRIC_REGISTRY_VERSION",
    "TIKTOK_BATCH_OPERATOR_CATEGORY",
    "TiktokBatchCapture",
    "TiktokBatchMetricDocumentError",
    "build_tiktok_batch_creator_metric_seed_document",
    "discover_latest_tiktok_batch_captures",
]
