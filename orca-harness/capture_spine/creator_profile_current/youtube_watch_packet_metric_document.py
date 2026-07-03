"""Build a YouTube creator-metric document from LIVE lake watch packets.

The live half of the YouTube capture->registry loop. The genesis path
(``youtube_metric_seed.py``) rebuilds the committed seed from a FIXED set of
checked-in review-input capture files and cannot ingest a fresh capture; this
module builds the same seed-shaped document the Silver producer
(``youtube_silver_metric_producer.derive_youtube_creator_metric_silver_records_from_seed``)
consumes, but from committed ``youtube_watch_metadata_comments`` SourceCapturePackets
in the data lake -- so a live recapture run (watch packets -> this builder ->
Silver producer -> snapshot -> materialize) is repeatable without touching the
genesis artifacts, and the longitudinal time-series can accrue.

The admitted pool stays ledger-governed: the YouTube creator observation ledger
names the admitted video ids; this builder never derives identity or admits new
videos (identity stays fenced in the linkage ledger, admission stays a governed
ledger change). Every expected creator video must resolve to a committed watch
packet or the build fails closed -- silent pool shrinkage is a fake-success path.

Engagement: live watch packets carry posture-backed receipts for ``view_count``,
``like_count`` and ``total_comment_count`` (the genesis 200-row artifacts exposed
view_count only), so per-account engagement metrics become computable here,
mirroring the Instagram recipe semantics:

- ``average_views`` / ``median_views``: over videos with an observed view_count
  (round 2), with ``view_count_min``/``view_count_max`` over the same set.
- ``average_like_count`` / ``average_comment_count``: per-metric observed
  subsets (round 2); unavailable-with-reason when no video exposes the input.
- ``engagement_rate``: ``(sum(like_count) + sum(total_comment_count)) /
  sum(view_count)`` over COMPLETE videos only (all three observed), round 6 --
  the IG recipe shape. Never computed over mixed subsets; never zero-filled.
- ``comment_sample_count`` is a bounded capture sample, NEVER a platform metric
  input.

Boundary: this module is PURE -- it reads verified lake packets and returns the
document; it writes nothing and never touches the committed genesis seed, the
identity ledger, or the observation ledger. Appending Silver records is the
producer's job (via the operator runner); the committed genesis artifacts remain
the no-drift oracle for the genesis path.
"""
from __future__ import annotations

import json
import statistics
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, Iterable, Mapping

from capture_spine.creator_profile_current.youtube_metric_seed import (
    YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_SEED_WRAPPER,
    _ledger_video_rows,
    _not_attempted_metric,
    _observed_metric,
    _pool_index,
    _sample_support_label,
    _surface_handling,
    _unavailable_metric,
    _unwrap_creator_ledger,
    _youtube_accounts_by_channel,
)
from data_lake.root import raw_shard
from source_capture.youtube_watch_packet import (
    CAPTURE_JSON_NAME,
    SOURCE_SURFACE as YOUTUBE_WATCH_SOURCE_SURFACE,
    WATCH_HTML_NAME,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot

YOUTUBE_WATCH_PACKET_METRIC_DOCUMENT_SCHEMA_VERSION = (
    "youtube_shorts_fragrance_creator_metric_document_live_v0"
)
YOUTUBE_WATCH_PACKET_METRIC_DOCUMENT_ID = (
    "youtube_shorts_fragrance_creator_metric_document_live_v0"
)
YOUTUBE_WATCH_PACKET_METRIC_RECIPE_VERSION = (
    "creator_metric_rollup_admitted_youtube_shorts_watch_packet_engagement_v0"
)
YOUTUBE_WATCH_PACKET_METRIC_REGISTRY_VERSION = "creator_metric_youtube_watch_packet_v0"

_PLATFORM = "youtube"
_CREATOR_CLASSIFICATION_INCLUDED = "creator_or_channel_observed"
_ENGAGEMENT_METRIC_ORDER = ("view_count", "like_count", "total_comment_count")


class WatchPacketMetricDocumentError(ValueError):
    """Raised when the live document cannot be built trustworthily. Subclasses
    ``ValueError`` so existing fail-closed ``except ValueError`` paths still
    catch it; ``reason`` is the machine-readable code and ``subject`` names the
    video/account it failed on (``""`` for a run-level failure)."""

    def __init__(self, reason: str, subject: str, detail: str) -> None:
        self.reason = reason
        self.subject = subject
        prefix = f"{reason} for {subject!r}" if subject else reason
        super().__init__(f"{prefix}: {detail}")


@dataclass(frozen=True)
class WatchCapture:
    """One verified watch-packet read for one admitted video: the selected
    packet id, its capture payload (``youtube_watch_capture.json``), the
    lake-relative pointer to that preserved payload file, and the
    hash-checkable watch-HTML provenance from the packet manifest."""

    packet_id: str
    video_id: str
    capture_timestamp: str
    payload: Mapping[str, Any]
    capture_json_pointer: str
    watch_html_sha256: str
    watch_byte_size: int


def discover_latest_watch_captures(
    data_root: "DataLakeRoot", *, expected_video_ids: Iterable[str]
) -> dict[str, WatchCapture]:
    """Resolve every expected admitted video id to its latest committed
    ``youtube_watch_metadata_comments`` packet, via verified lake reads.

    "Latest" is the packet with the newest ``capture_timestamp``; two DISTINCT
    packets tying on the timestamp for the same video fail closed
    (``ambiguous_video_packet``) rather than picking silently. Every expected
    video must resolve to at least one packet, else ``missing_video_packet``
    (silent pool shrinkage is a fake-success path). Packets for videos outside
    the expected set are ignored. The caller ensures the availability index is
    current (the operator runner rebuilds it first)."""
    expected = set(expected_video_ids)
    candidates: dict[str, list[WatchCapture]] = {video_id: [] for video_id in expected}
    for packet_id in data_root.list_available(source_family=_PLATFORM):
        entry = data_root.read_availability(packet_id)
        if not entry or entry.get("source_surface") != YOUTUBE_WATCH_SOURCE_SURFACE:
            continue
        capture = _load_watch_capture(data_root, packet_id)
        if capture.video_id in candidates:
            candidates[capture.video_id].append(capture)

    missing = sorted(video_id for video_id, found in candidates.items() if not found)
    if missing:
        raise WatchPacketMetricDocumentError(
            "missing_video_packet",
            missing[0],
            f"{len(missing)} expected admitted video(s) have no committed watch packet: {missing}",
        )
    return {
        video_id: _select_latest_capture(video_id, found)
        for video_id, found in candidates.items()
    }


def build_youtube_watch_packet_metric_document(
    data_root: "DataLakeRoot",
    *,
    creator_ledger: Mapping[str, Any],
    account_ledger: Mapping[str, Any],
    generated_at_utc: str,
    excluded_video_ids: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Build the seed-shaped live metric document from committed watch packets.

    Consumable directly by
    ``derive_youtube_creator_metric_silver_records_from_seed`` (same wrapper
    key). Fails closed on: a missing/ambiguous watch packet for an expected
    video, a packet whose captured channel id diverges from the ledger, an
    account with zero observed view counts, or an account row missing from the
    linkage ledger.

    ``excluded_video_ids`` is the explicit operator-exclusion mechanism for
    observably-dead admitted videos (``{video_id: reason}``, every reason
    non-empty): excluded ids leave the expected set BEFORE discovery, and the
    exclusion is recorded loudly in the document counts, an
    ``operator_exclusions`` block, and every affected account's rollup
    limitations. It is never a silent fallback: an id not in the admitted
    creator pool fails ``unknown_excluded_video``, and an exclusion set that
    eliminates ALL of an account's videos fails ``account_fully_excluded`` (a
    roster decision the operator must take to the owner, not a quiet shrink)."""
    ledger_video_rows = _ledger_video_rows(_unwrap_creator_ledger(dict(creator_ledger)))
    accounts_by_channel = _youtube_accounts_by_channel(account_ledger)

    creator_video_rows = {
        video_id: row
        for video_id, row in ledger_video_rows.items()
        if row["creator"].get("creator_classification") == _CREATOR_CLASSIFICATION_INCLUDED
    }
    excluded_video_count = len(ledger_video_rows) - len(creator_video_rows)
    if not creator_video_rows:
        raise WatchPacketMetricDocumentError(
            "empty_admitted_pool", "", "creator observation ledger has no creator-classified videos"
        )

    exclusions = _validated_exclusions(excluded_video_ids, creator_video_rows)
    excluded_by_channel: dict[str, list[str]] = {}
    for video_id in exclusions:
        channel = creator_video_rows[video_id]["creator"]["platform_subject_key"]
        excluded_by_channel.setdefault(channel, []).append(video_id)
        del creator_video_rows[video_id]
    fully_excluded = sorted(
        channel
        for channel in excluded_by_channel
        if not any(
            row["creator"]["platform_subject_key"] == channel
            for row in creator_video_rows.values()
        )
    )
    if fully_excluded:
        raise WatchPacketMetricDocumentError(
            "account_fully_excluded",
            fully_excluded[0],
            "operator exclusions eliminate every admitted video for channel(s) "
            f"{fully_excluded}; that is a roster decision, not an exclusion",
        )

    captures = discover_latest_watch_captures(
        data_root, expected_video_ids=creator_video_rows
    )

    observations: list[dict[str, Any]] = []
    rows_by_account: dict[str, list[dict[str, Any]]] = {}
    ordered_video_ids = sorted(
        creator_video_rows, key=lambda video_id: _pool_index(creator_video_rows[video_id]["pool_id"])
    )
    for video_id in ordered_video_ids:
        ledger_row = creator_video_rows[video_id]
        capture = captures[video_id]
        row = _video_metric_row(
            capture=capture, ledger_row=ledger_row, accounts_by_channel=accounts_by_channel
        )
        for metric in _ENGAGEMENT_METRIC_ORDER:
            value = row["metric_values"][metric]
            if value is None:
                continue
            observations.append(
                _metric_observation(
                    row=row,
                    metric=metric,
                    value=value,
                    sequence=len(observations) + 1,
                )
            )
            observations[-1]["_video_id"] = video_id
        rows_by_account.setdefault(row["platform_account_id"], []).append(row)

    observation_ids_by_account_video: dict[tuple[str, str], list[str]] = {}
    for observation in observations:
        key = (observation["platform_account_id"], observation.pop("_video_id"))
        observation_ids_by_account_video.setdefault(key, []).append(
            observation["metric_observation_id"]
        )

    rollups = [
        _rollup(
            account=accounts_by_channel[rows[0]["channel_id"]],
            rows=rows,
            observation_ids_by_account_video=observation_ids_by_account_video,
            generated_at_utc=generated_at_utc,
            rollup_index=index,
            excluded_videos={
                video_id: exclusions[video_id]
                for video_id in excluded_by_channel.get(rows[0]["channel_id"], [])
            },
        )
        for index, (account_id, rows) in enumerate(
            sorted(rows_by_account.items(), key=lambda item: item[0]), start=1
        )
    ]

    document = {
        "schema_version": YOUTUBE_WATCH_PACKET_METRIC_DOCUMENT_SCHEMA_VERSION,
        "seed_id": YOUTUBE_WATCH_PACKET_METRIC_DOCUMENT_ID,
        "seed_mode": "live_watch_packet_metric_document",
        "generated_at_utc": generated_at_utc,
        "source_policy_posture": (
            "Live metric document generated from committed YouTube watch-page "
            "SourceCapturePackets in the data lake (verified by-key reads). Rows are "
            "account-scoped capture-time observations for the ledger-admitted fragrance "
            "Shorts pool, not channel-wide creator averages, not cross-platform linkage, "
            "not SQLite/runtime storage, and not live dashboard readiness. Engagement "
            "metrics exist only where the live packets expose the source-native inputs."
        ),
        "authority_pointers": [
            "orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md",
            "orca/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md",
            "orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md",
            "orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md",
        ],
        "source_inputs": [
            {
                "source_pointer": captures[video_id].capture_json_pointer,
                "sha256": captures[video_id].watch_html_sha256,
                "role": "live YouTube watch packet (verified lake read; sha256 is the preserved watch HTML)",
            }
            for video_id in ordered_video_ids
        ],
        "selection_policy": {
            "included": (
                "creator_or_channel_observed rows from the YouTube Shorts fragrance creator "
                "observation ledger, recaptured from committed live watch packets"
            ),
            "excluded": (
                "brand_or_platform_account_observed ledger rows are skipped entirely; "
                "comment_sample_count is a bounded capture sample and never a metric input"
            ),
            "rollup_scope": "platform_account only; no creator_record or cross-platform rollups",
            "metric_value_rule": (
                "only observed source-visible numeric receipt values are stored; absent "
                "metrics are not zero-filled"
            ),
            "engagement_rate_recipe": (
                "(sum(like_count) + sum(total_comment_count)) / sum(view_count) over videos "
                "with all three inputs observed"
            ),
            "representativeness_rule": (
                "Average and median view rollups are directional admitted-pool statistics "
                "only. They must carry sample_support and must not be presented as "
                "representative creator or channel averages."
            ),
        },
        "counts": {
            "admitted_creator_videos": len(creator_video_rows),
            "brand_or_platform_excluded_ledger_rows": excluded_video_count,
            "operator_excluded_admitted_videos": len(exclusions),
            "metric_observations_total": len(observations),
            "unique_platform_accounts_with_observations": len(rows_by_account),
            "metric_rollups_total": len(rollups),
            "engagement_rate_rollups_observed": sum(
                1
                for rollup in rollups
                if rollup["metric_rollups"]["engagement_rate"]["posture"] == "observed"
            ),
        },
        "operator_exclusions": [
            {"video_id": video_id, "reason": exclusions[video_id]}
            for video_id in sorted(exclusions)
        ],
        "metric_observations": observations,
        "metric_rollups": rollups,
        "accepted_residuals": [
            "The rollups are admitted-pool statistics, not full-channel creator averages.",
            "Latest-packet-per-video selection orders by capture_timestamp; distinct packets tying on the timestamp fail closed rather than being clock-trusted.",
            "Engagement metrics cover only the videos whose live packets expose the source-native inputs; coverage is named per rollup, never zero-filled.",
            "comment_sample_count is preserved in the packets but never used as a metric input.",
        ],
        "non_claims": [
            "not channel-wide creator average",
            "not subscriber count",
            "not cross-platform identity linkage",
            "not creator_record rollup",
            "not buyer proof",
            "not validation or readiness",
            "not admission or identity-ledger change authorization",
            "not dashboard implementation",
        ],
    }
    return {YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_SEED_WRAPPER: document}


def _validated_exclusions(
    excluded_video_ids: Mapping[str, str] | None,
    creator_video_rows: Mapping[str, Any],
) -> dict[str, str]:
    """Validate the operator-exclusion map: every id must be an admitted creator
    video and every reason non-empty. Exclusion is operator-attested and loud,
    never inferred -- a bad id or blank reason fails closed."""
    if not excluded_video_ids:
        return {}
    out: dict[str, str] = {}
    for video_id, reason in excluded_video_ids.items():
        if video_id not in creator_video_rows:
            raise WatchPacketMetricDocumentError(
                "unknown_excluded_video",
                video_id,
                "excluded video is not an admitted creator-classified ledger video",
            )
        if not isinstance(reason, str) or not reason.strip():
            raise WatchPacketMetricDocumentError(
                "missing_exclusion_reason",
                video_id,
                "operator exclusion requires a non-empty reason",
            )
        out[video_id] = reason.strip()
    return out


# -- packet reading -----------------------------------------------------------

def _load_watch_capture(data_root: "DataLakeRoot", packet_id: str) -> WatchCapture:
    loaded = data_root.load_raw_packet(packet_id)
    # The packet writer preserves each staged artifact as "<NN>_<original_name>",
    # so match on the original filename after the index prefix.
    preserved_by_name: dict[str, Mapping[str, Any]] = {}
    for entry in loaded.manifest.get("preserved_files", []):
        if not isinstance(entry, Mapping):
            continue
        basename = str(entry.get("relative_packet_path", "")).rsplit("/", 1)[-1]
        original_name = basename.split("_", 1)[1] if "_" in basename else basename
        preserved_by_name.setdefault(original_name, entry)
    capture_entry = preserved_by_name.get(CAPTURE_JSON_NAME)
    watch_entry = preserved_by_name.get(WATCH_HTML_NAME)
    if capture_entry is None or watch_entry is None:
        raise WatchPacketMetricDocumentError(
            "invalid_watch_packet",
            packet_id,
            f"packet does not preserve both {CAPTURE_JSON_NAME!r} and {WATCH_HTML_NAME!r}",
        )
    try:
        payload = json.loads(loaded.bodies[capture_entry["file_id"]].decode("utf-8"))
    except (KeyError, UnicodeDecodeError, ValueError) as exc:
        raise WatchPacketMetricDocumentError(
            "invalid_watch_packet", packet_id, f"unreadable {CAPTURE_JSON_NAME}: {exc}"
        ) from exc
    video_id = payload.get("platform_video_id")
    capture_timestamp = payload.get("capture_timestamp")
    if not isinstance(video_id, str) or not video_id.strip():
        raise WatchPacketMetricDocumentError(
            "invalid_watch_packet", packet_id, "capture payload lacks platform_video_id"
        )
    if not isinstance(capture_timestamp, str) or not capture_timestamp.strip():
        raise WatchPacketMetricDocumentError(
            "invalid_watch_packet", packet_id, "capture payload lacks capture_timestamp"
        )
    return WatchCapture(
        packet_id=packet_id,
        video_id=video_id,
        capture_timestamp=capture_timestamp,
        payload=payload,
        capture_json_pointer=(
            f"raw/{raw_shard(packet_id)}/{packet_id}/{capture_entry['relative_packet_path']}"
        ),
        watch_html_sha256=str(watch_entry["sha256"]),
        watch_byte_size=int(watch_entry["size_bytes"]),
    )


def _select_latest_capture(video_id: str, found: list[WatchCapture]) -> WatchCapture:
    ranked = sorted(found, key=lambda capture: _parse_instant(capture.capture_timestamp))
    latest = ranked[-1]
    ties = [
        capture
        for capture in ranked
        if capture.packet_id != latest.packet_id
        and _parse_instant(capture.capture_timestamp) == _parse_instant(latest.capture_timestamp)
    ]
    if ties:
        raise WatchPacketMetricDocumentError(
            "ambiguous_video_packet",
            video_id,
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

def _video_metric_row(
    *,
    capture: WatchCapture,
    ledger_row: Mapping[str, Any],
    accounts_by_channel: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    creator = ledger_row["creator"]
    expected_channel = creator["platform_subject_key"]
    packet_dict = capture.payload.get("packet")
    packet_dict = packet_dict if isinstance(packet_dict, Mapping) else {}
    channel = packet_dict.get("channel")
    channel = channel if isinstance(channel, Mapping) else {}
    captured_channel = channel.get("channel_id")
    if not isinstance(captured_channel, str) or not captured_channel.strip():
        raise WatchPacketMetricDocumentError(
            "invalid_watch_packet",
            capture.packet_id,
            f"capture payload for video {capture.video_id!r} lacks packet.channel.channel_id",
        )
    if captured_channel != expected_channel:
        raise WatchPacketMetricDocumentError(
            "channel_mismatch",
            capture.video_id,
            f"captured channel {captured_channel!r} does not match ledger channel "
            f"{expected_channel!r}; refusing to attribute the observation",
        )
    account = accounts_by_channel.get(captured_channel)
    if account is None:
        raise WatchPacketMetricDocumentError(
            "missing_account_row",
            captured_channel,
            f"YouTube channel for video {capture.video_id!r} has no platform account row",
        )
    metadata = packet_dict.get("metadata")
    metadata = metadata if isinstance(metadata, Mapping) else {}
    return {
        "video_id": capture.video_id,
        "packet_id": capture.packet_id,
        "capture_json_pointer": capture.capture_json_pointer,
        "channel_id": captured_channel,
        "platform_account_id": account["platform_account_id"],
        "account": account,
        "creator": creator,
        "pool_id": ledger_row["pool_id"],
        "title": metadata.get("title"),
        "publish_date": metadata.get("publish_date"),
        "watch_url": capture.payload.get("watch_url"),
        "observed_at": capture.capture_timestamp,
        "watch_html_sha256": capture.watch_html_sha256,
        "watch_byte_size": capture.watch_byte_size,
        "metric_values": {
            metric: _observed_receipt_value(capture, metric)
            for metric in _ENGAGEMENT_METRIC_ORDER
        },
    }


def _observed_receipt_value(capture: WatchCapture, metric: str) -> int | None:
    receipts = capture.payload.get("metric_receipts")
    receipts = receipts if isinstance(receipts, Mapping) else {}
    receipt = receipts.get(metric)
    receipt = receipt if isinstance(receipt, Mapping) else {}
    if receipt.get("posture") != "observed":
        return None
    value = receipt.get("value")
    if isinstance(value, bool) or not isinstance(value, int):
        raise WatchPacketMetricDocumentError(
            "invalid_watch_packet",
            capture.packet_id,
            f"observed metric receipt for {metric!r} carries a non-integer value: {value!r}",
        )
    return value


# -- observation / rollup construction ---------------------------------------

def _metric_observation(
    *, row: Mapping[str, Any], metric: str, value: int, sequence: int
) -> dict[str, Any]:
    creator = row["creator"]
    source_file = row["capture_json_pointer"]
    return {
        "metric_observation_id": f"yt_watch_metric_obs_v0_{sequence:03d}",
        "platform_account_id": row["platform_account_id"],
        "profile_subject_kind": "platform_account",
        "profile_subject_id": row["platform_account_id"],
        "creator_record_id_or_none": None,
        "youtube_creator_observation_id": creator["creator_observation_id"],
        "platform": _PLATFORM,
        "platform_subject_key_type": "youtube_channel_id",
        "platform_subject_key": row["channel_id"],
        "creator_handle_query": creator["creator_handle_query"],
        "source_pool_row_id": row["pool_id"],
        "content_id_or_none": row["video_id"],
        "content_url_or_none": f"https://www.youtube.com/shorts/{row['video_id']}",
        "watch_url_or_none": row["watch_url"],
        "content_kind": "short",
        "content_title_or_none": row["title"],
        "content_publication_or_event_time_or_none": row["publish_date"],
        "metric_name": metric,
        "metric_value_or_none": value,
        "metric_unit": "count",
        "metric_posture": "observed",
        "posture_reason_or_none": None,
        "source_pointer": f"{source_file}#/metric_receipts/{metric}",
        "source_field": f"/metric_receipts/{metric}/value",
        "source_file": source_file,
        "source_row_id_or_none": f"{row['packet_id']}:{metric}",
        "source_watch_html_sha256_or_none": row["watch_html_sha256"],
        "source_shorts_html_sha256_or_none": None,
        "source_watch_byte_size_or_none": row["watch_byte_size"],
        "source_shorts_byte_size_or_none": None,
        "source_packet_id_or_none": row["packet_id"],
        "source_packet_pointer_or_none": None,
        "transcript_route_or_none": None,
        "observed_at": row["observed_at"],
        "observed_at_source": "watch_packet_capture_timestamp",
        "capture_window_start_or_none": None,
        "capture_window_end_or_none": None,
        "metric_registry_version": YOUTUBE_WATCH_PACKET_METRIC_REGISTRY_VERSION,
        "limitation_notes": [
            "Metric is source-visible at watch-packet capture time and may change after capture.",
            "Observation belongs to the admitted fragrance Shorts pool, not a full channel crawl.",
        ],
    }


def _rollup(
    *,
    account: Mapping[str, Any],
    rows: list[dict[str, Any]],
    observation_ids_by_account_video: Mapping[tuple[str, str], list[str]],
    generated_at_utc: str,
    rollup_index: int,
    excluded_videos: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    account_id = account["platform_account_id"]
    views = [row["metric_values"]["view_count"] for row in rows if row["metric_values"]["view_count"] is not None]
    likes = [row["metric_values"]["like_count"] for row in rows if row["metric_values"]["like_count"] is not None]
    comments = [
        row["metric_values"]["total_comment_count"]
        for row in rows
        if row["metric_values"]["total_comment_count"] is not None
    ]
    complete = [row for row in rows if all(row["metric_values"][m] is not None for m in _ENGAGEMENT_METRIC_ORDER)]
    if not views:
        raise WatchPacketMetricDocumentError(
            "no_observed_views_for_account",
            account_id,
            "no admitted video exposed an observed view_count in the live watch packets: "
            f"{sorted(row['video_id'] for row in rows)}",
        )

    source_ids = [
        observation_id
        for row in rows
        for observation_id in observation_ids_by_account_video.get((account_id, row["video_id"]), [])
    ]
    observation_count = len(source_ids)
    sample_adequacy = _sample_support_label(observation_count)

    engagement_metric = _engagement_rate_metric(complete)
    metric_rollups = {
        "average_views": _observed_metric(round(statistics.mean(views), 2), "count"),
        "median_views": _observed_metric(round(statistics.median(views), 2), "count"),
        "engagement_rate": engagement_metric,
        "average_like_count": (
            _observed_metric(round(statistics.mean(likes), 2), "count")
            if likes
            else _unavailable_metric(
                "no admitted Short exposed a source-visible like_count in the live watch packets",
                "count",
            )
        ),
        "average_comment_count": (
            _observed_metric(round(statistics.mean(comments), 2), "count")
            if comments
            else _unavailable_metric(
                "no admitted Short exposed a source-visible total_comment_count in the live watch packets",
                "count",
            )
        ),
        "posting_cadence": _not_attempted_metric(
            "cadence recipe is out of scope for this live metric document", "rate"
        ),
        "recent_velocity": _not_attempted_metric(
            "velocity recipe is out of scope for this live metric document", "rate"
        ),
    }

    engagement_limitation = (
        (
            f"Engagement inputs (like_count and total_comment_count) are exposed for "
            f"{len(complete)} of {len(rows)} admitted Shorts; engagement metrics cover that "
            "subset only and are never zero-filled."
        )
        if engagement_metric["posture"] == "observed"
        else (
            "Engagement rate is unavailable because no admitted Short exposed view, like, "
            "and total-comment counts together in the live watch packets."
        )
    )
    exclusion_limitations = (
        [
            (
                f"{len(excluded_videos)} admitted Short(s) excluded from this rollup by "
                "explicit operator exclusion: "
                + "; ".join(
                    f"{video_id} ({excluded_videos[video_id]})"
                    for video_id in sorted(excluded_videos)
                )
                + ". Metrics cover the remaining admitted pool only."
            )
        ]
        if excluded_videos
        else []
    )
    return {
        "metric_rollup_id": f"yt_watch_account_metric_rollup_v0_{rollup_index:03d}",
        "profile_subject_kind": "platform_account",
        "profile_subject_id": account_id,
        "creator_record_id_or_none": None,
        "platform_scope": _PLATFORM,
        "platform_account_ids": [account_id],
        "platform_subject_key_type": "youtube_channel_id",
        "platform_subject_key": account["platform_public_account_id_or_none"],
        "public_handle": account["public_handle"],
        "rollup_window": "custom",
        "rollup_window_description": (
            "admitted_fragrance_shorts_pool200_v0 recaptured from live watch packets; "
            "not a full creator-channel window"
        ),
        "content_kind_inclusion_rule": (
            "youtube Shorts admitted into the fragrance transcript-bearing source pool only"
        ),
        "metric_rollups": metric_rollups,
        "source_metric_observation_ids": source_ids,
        "observation_count": observation_count,
        "view_count_min": min(views),
        "view_count_max": max(views),
        "calculation_recipe_version": YOUTUBE_WATCH_PACKET_METRIC_RECIPE_VERSION,
        "computed_at": generated_at_utc,
        "freshness_state": "partial",
        "limitations": [
            "Rollup covers the admitted fragrance Shorts pool only; it is not a channel-wide average.",
            "Metrics are recaptured from live YouTube watch packets and are capture-time observations that may change after capture.",
            *exclusion_limitations,
            engagement_limitation,
            "Cross-platform rollups are not authorized without promoted public-handle linkage evidence.",
            (
                f"Average/median views are computed over {len(views)} admitted Shorts "
                f"({observation_count} metric observations in total); sample adequacy is "
                f"{sample_adequacy} and the value is not a representative creator average."
            ),
            (
                "The admitted pool is fragrance and transcript-bearing, so selection can bias "
                "view averages relative to the creator's full Shorts or channel output."
            ),
        ],
        "sample_support": {
            "observation_count": observation_count,
            "sample_adequacy": sample_adequacy,
            "representativeness_posture": "admitted_pool_only_not_representative_creator_average",
            "surface_handling": _surface_handling(observation_count),
        },
    }


def _engagement_rate_metric(complete: list[dict[str, Any]]) -> dict[str, Any]:
    if not complete:
        return _unavailable_metric(
            "no admitted Short exposed view, like, and total-comment counts together in the "
            "live watch packets",
            "rate",
        )
    denominator = sum(row["metric_values"]["view_count"] for row in complete)
    if denominator <= 0:
        return _unavailable_metric(
            "engagement denominator is zero: the complete-input Shorts carry no views",
            "rate",
        )
    numerator = sum(
        row["metric_values"]["like_count"] + row["metric_values"]["total_comment_count"]
        for row in complete
    )
    return _observed_metric(round(numerator / denominator, 6), "rate")


__all__ = [
    "WatchCapture",
    "WatchPacketMetricDocumentError",
    "YOUTUBE_WATCH_PACKET_METRIC_DOCUMENT_SCHEMA_VERSION",
    "YOUTUBE_WATCH_PACKET_METRIC_RECIPE_VERSION",
    "YOUTUBE_WATCH_PACKET_METRIC_REGISTRY_VERSION",
    "build_youtube_watch_packet_metric_document",
    "discover_latest_watch_captures",
]
