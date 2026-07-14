"""Build a compact SourceCapturePacket from a YouTube watch/comments result.

Network-free packet writer. The live fetcher owns YouTube-specific acquisition; this
module validates the acquisition-time watch/comment response bodies, then stages only
the selected source-visible metadata and bounded comment rows. The enclosing served
HTML and ``youtubei/v1/next`` response bodies are intentionally not persisted.

Metric observations in the manifest carry the typed value/absence posture. The
platform-specific route receipts (``ytInitialPlayerResponse``, ``microformat``,
``youtubei_next``) stay in the preserved ``youtube_watch_capture.json`` payload so
we do not force a shared schema before IG/YT core architecture is settled.
"""
from __future__ import annotations

import datetime
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from source_capture.models import (
    CaptureModeCategory,
    CoverageWindow,
    MetricObservation,
    MetricPosture,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map

SOURCE_SURFACE = "youtube_watch_metadata_comments"
LEGACY_CAPTURE_SCHEMA_VERSION = "youtube_watch_metadata_comments_capture_v0"
CAPTURE_SCHEMA_VERSION = "youtube_watch_metadata_comments_capture_v1"
WATCH_HTML_NAME = "raw_watch.html"
CAPTURE_JSON_NAME = "youtube_watch_capture.json"
SELECTIVE_CAPTURE_POLICY_VERSION = "youtube_watch_selected_observables_v1"
SELECTIVE_RETENTION_POSTURE = "not_persisted_after_validated_extraction"
YOUTUBE_WATCH_METRIC_NAMES = ("view_count", "like_count", "comment_sample_count", "total_comment_count")

YOUTUBE_WATCH_NON_CLAIMS = [
    "not video media byte preservation",
    "not YouTube Data API use",
    "not login or account-entitled capture",
    "not browser-rendered JS execution",
    "not complete comment graph capture",
    "not total comment count unless source-native exact count is exposed",
    "not full served watch HTML or youtubei response-body preservation",
    "not future-field replay from discarded source-response envelopes",
    "not zero-filled missing engagement metrics",
    "not ECR design",
    "not Cleaning implementation",
    "not Judgment scoring",
    "not buyer proof",
]


@dataclass(frozen=True)
class YoutubeWatchCommentPage:
    filename: str
    raw_json_bytes: bytes


@dataclass(frozen=True)
class YoutubeWatchFetch:
    video_id: str
    raw_watch_html: bytes
    packet: Mapping[str, Any]
    comment_page_bodies: Sequence[YoutubeWatchCommentPage] = ()


def write_youtube_watch_packet(
    fetch: YoutubeWatchFetch,
    *,
    output_directory: Path | None = None,
    data_root=None,
    decision_question: str,
    now_iso: str | None = None,
) -> tuple[int, str]:
    """Stage a fetched YouTube watch capture into SourceCapturePacket form."""
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", fetch.video_id or ""):
        return 5, f"refusing to build packet: invalid video id {fetch.video_id!r}"
    if not fetch.raw_watch_html:
        return 5, "refusing to build packet: empty raw_watch_html"

    packet = _json_safe_dict(fetch.packet)
    receipts = packet.get("receipts") if isinstance(packet.get("receipts"), Mapping) else {}
    metadata = packet.get("metadata") if isinstance(packet.get("metadata"), Mapping) else {}
    engagement = packet.get("engagement") if isinstance(packet.get("engagement"), Mapping) else {}
    availability = packet.get("availability") if isinstance(packet.get("availability"), Mapping) else {}

    capture_ts = now_iso or _string_or_none(receipts.get("retrieval_time_utc")) or _utc_now_z()
    watch_url = _string_or_none(packet.get("watch_url")) or f"https://www.youtube.com/watch?v={fetch.video_id}"
    video_state = _string_or_none(availability.get("video_state")) or "unknown"
    comments_state = _string_or_none(availability.get("comments_state")) or _string_or_none(
        packet.get("comments_posture")
    ) or "comments_not_exposed"
    try:
        metric_observations = _metric_observations(packet, capture_timestamp=capture_ts)
    except ValueError as exc:
        return 5, f"refusing to build packet: {exc}"
    metric_receipts = packet.get("metric_receipts") if isinstance(packet.get("metric_receipts"), Mapping) else {}

    for page in fetch.comment_page_bodies:
        try:
            _validate_comment_page(page)
        except ValueError as exc:
            return 5, f"refusing to build packet: {exc}"
    try:
        _validate_selected_comments(packet, received_page_count=len(fetch.comment_page_bodies))
    except ValueError as exc:
        return 5, f"refusing to build packet: {exc}"

    payload = {
        "capture_schema_version": CAPTURE_SCHEMA_VERSION,
        "platform": "youtube",
        "platform_video_id": fetch.video_id,
        "watch_url": watch_url,
        "capture_timestamp": capture_ts,
        "availability": availability,
        "metric_receipts": metric_receipts,
        "packet": packet,
        "selected_observable_policy_version": SELECTIVE_CAPTURE_POLICY_VERSION,
        "source_response_retention": {
            "watch_html": {
                "posture": SELECTIVE_RETENTION_POSTURE,
                "received_byte_size": len(fetch.raw_watch_html),
            },
            "comment_pages": {
                "posture": SELECTIVE_RETENTION_POSTURE,
                "received_page_count": len(fetch.comment_page_bodies),
                "received_byte_size": sum(len(page.raw_json_bytes) for page in fetch.comment_page_bodies),
            },
        },
    }
    staged_artifacts: list[tuple[str, bytes]] = [
        (CAPTURE_JSON_NAME, (json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")),
    ]
    file_ids = staged_file_id_map(staged_artifacts)

    publication = _string_or_none(metadata.get("publish_date"))
    timing = PacketTiming(
        source_publication_or_event=known_fact(publication)
        if publication
        else unknown_with_reason("YouTube watch capture did not expose publishDate"),
        source_edit_or_version=not_applicable("YouTube watch metadata capture did not model source edit/version timing"),
        capture_time=known_fact(capture_ts),
        recapture_time=not_applicable("no prior YouTube watch metadata/comments packet supplied"),
        cutoff_posture=not_applicable("cutoff posture does not apply to live YouTube watch capture"),
    )
    access = known_fact(
        f"youtube_watch_video_state:{video_state}; comments_state:{comments_state}; auth=logged_out"
    )
    archive = not_attempted("YouTube watch metadata/comments runner does not query archive/history services")
    media = known_fact(
        "selected source-visible watch metadata and bounded comment rows preserved; "
        "enclosing watch HTML/youtubei bodies and video media bytes are not persisted"
    )
    recapture = not_applicable("no prior YouTube watch packet supplied")

    metadata_metrics = [metric_observations["view_count"], metric_observations["like_count"]]
    comments_metrics = [metric_observations["comment_sample_count"], metric_observations["total_comment_count"]]
    comments_file_ids = [file_ids[CAPTURE_JSON_NAME]]

    slice_limitations = _slice_limitations(packet, metric_observations)
    comments_limitations = _comments_limitations(packet, metric_observations)
    retention_limitations = [
        "full_watch_html_not_persisted:selected_observables_are_canonical",
        "raw_youtubei_comment_pages_not_persisted:selected_comment_rows_are_canonical",
    ]
    run_limitations = slice_limitations + comments_limitations + retention_limitations

    source_slices = [
        SourceCaptureSlice(
            slice_id="youtube_watch_metadata_01",
            locator=known_fact(watch_url),
            timing=timing,
            access_posture=access,
            archive_history_posture=archive,
            media_modality_posture=media,
            re_capture_relationship=recapture,
            limitations=slice_limitations + [retention_limitations[0]],
            warning_notes=[],
            preserved_file_ids=[file_ids[CAPTURE_JSON_NAME]],
            metric_observations=metadata_metrics,
        ),
        SourceCaptureSlice(
            slice_id="youtube_watch_comments_01",
            locator=known_fact("youtubei/v1/next continuation route for the watch page"),
            timing=timing,
            access_posture=access,
            archive_history_posture=archive,
            media_modality_posture=media,
            re_capture_relationship=recapture,
            limitations=comments_limitations + [retention_limitations[1]],
            warning_notes=[],
            preserved_file_ids=comments_file_ids,
            metric_observations=comments_metrics,
        ),
    ]

    result = stage_and_write_packet(
        output_directory=output_directory,
        data_root=data_root,
        staged_artifacts=staged_artifacts,
        source_slices=source_slices,
        source_family="youtube",
        source_surface=SOURCE_SURFACE,
        source_locator=known_fact(watch_url),
        decision_question=decision_question,
        capture_context=(
            "YouTube logged-out selected-observable watch metadata/comments capture; transient served HTML "
            "for player/microformat extraction plus bounded youtubei_next comment rows when exposed"
        ),
        actor_audience_context=not_applicable("public video capture; no actor/audience modeling at capture"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="youtube_watch_cli_operator",
        session_identity=None,
        visible_mode_changes=[
            (
                "youtube_watch_routes:metadata=ytInitialPlayerResponse/microformat;comments=youtubei_next;"
                f"comment_pages={len(fetch.comment_page_bodies)};retention=selected_observables_only"
            ),
            f"youtube_watch_states:video={video_state};comments={comments_state}",
            f"youtube_watch_metric_postures:{_metric_posture_summary(metric_observations)}",
        ],
        source_publication_or_event=timing.source_publication_or_event,
        source_edit_or_version=timing.source_edit_or_version,
        cutoff_posture=timing.cutoff_posture,
        recapture_time=timing.recapture_time,
        access_posture=access,
        archive_history_posture=archive,
        media_modality_posture=media,
        re_capture_relationship=recapture,
        warnings=[],
        limitations=run_limitations,
        receipt_summary=(
            f"YouTube watch metadata/comments packet for {fetch.video_id}: video_state={video_state}, "
            f"comments_state={comments_state}, comment_pages={len(fetch.comment_page_bodies)}, "
            "retention=selected_observables_only."
        ),
        receipt_non_claims=YOUTUBE_WATCH_NON_CLAIMS,
    )
    return 0, result.output_directory


def _metric_observations(packet: Mapping[str, Any], *, capture_timestamp: str) -> dict[str, MetricObservation]:
    return {
        metric: _metric_observation(packet, metric, capture_timestamp=capture_timestamp)
        for metric in YOUTUBE_WATCH_METRIC_NAMES
    }


def _metric_observation(packet: Mapping[str, Any], metric: str, *, capture_timestamp: str) -> MetricObservation:
    receipts = packet.get("metric_receipts") if isinstance(packet.get("metric_receipts"), Mapping) else {}
    receipt = receipts.get(metric) if isinstance(receipts.get(metric), Mapping) else None
    if receipt is None:
        raise ValueError(f"missing metric receipt for {metric}")

    engagement = packet.get("engagement") if isinstance(packet.get("engagement"), Mapping) else {}
    engagement_value = _int_or_none(engagement.get(metric))
    posture = _string_or_none(receipt.get("posture"))

    if posture == "observed":
        value = _int_or_none(receipt.get("value"))
        if value is None:
            raise ValueError(f"observed metric receipt for {metric} requires an integer value")
        source_route = _string_or_none(receipt.get("source_route"))
        source_path = _string_or_none(receipt.get("source_path"))
        artifact = _string_or_none(receipt.get("artifact"))
        missing = [
            name
            for name, field_value in (
                ("source_route", source_route),
                ("source_path", source_path),
                ("artifact", artifact),
            )
            if field_value is None
        ]
        if missing:
            raise ValueError(f"observed metric receipt for {metric} missing {', '.join(missing)}")
        if engagement_value is not None and engagement_value != value:
            raise ValueError(
                f"metric receipt for {metric} value {value} does not match engagement value {engagement_value}"
            )
        return _observed_metric(metric, value, capture_timestamp=capture_timestamp)

    if engagement_value is not None:
        raise ValueError(
            f"{metric} has engagement value {engagement_value} but metric receipt posture is {posture!r}"
        )
    if posture != "unavailable_with_reason":
        raise ValueError(f"metric receipt for {metric} has unsupported posture {posture!r}")

    reason = _string_or_none(receipt.get("reason"))
    if reason is None:
        raise ValueError(f"unavailable metric receipt for {metric} requires a reason")
    routes_checked = receipt.get("routes_checked")
    if not _nonempty_string_sequence(routes_checked):
        raise ValueError(f"unavailable metric receipt for {metric} requires non-empty routes_checked")
    return MetricObservation(
        metric=metric,
        posture=MetricPosture.UNAVAILABLE_WITH_REASON,
        reason=reason,
        coverage_window=_coverage_window(capture_timestamp),
    )

def _observed_metric(metric: str, value: int, *, capture_timestamp: str) -> MetricObservation:
    return MetricObservation(
        metric=metric,
        posture=MetricPosture.OBSERVED,
        value=value,
        coverage_window=_coverage_window(capture_timestamp),
    )


def _coverage_window(capture_timestamp: str) -> CoverageWindow:
    return CoverageWindow(end=capture_timestamp)


def _slice_limitations(packet: Mapping[str, Any], metric_observations: Mapping[str, MetricObservation]) -> list[str]:
    availability = packet.get("availability") if isinstance(packet.get("availability"), Mapping) else {}
    state = _string_or_none(availability.get("video_state")) or "unknown"
    limitations: list[str] = []
    if state != "playable":
        limitations.append(f"video_availability_state:{state}")
    for metric in ("view_count", "like_count"):
        obs = metric_observations[metric]
        if obs.posture != MetricPosture.OBSERVED:
            limitations.append(f"{metric}_not_exposed:no_zero_fill")
    return limitations


def _comments_limitations(packet: Mapping[str, Any], metric_observations: Mapping[str, MetricObservation]) -> list[str]:
    availability = packet.get("availability") if isinstance(packet.get("availability"), Mapping) else {}
    state = _string_or_none(availability.get("comments_state")) or _string_or_none(packet.get("comments_posture"))
    limitations: list[str] = []
    if state != "comments_sample_captured":
        limitations.append(f"comments_state:{state or 'comments_not_exposed'}")
    for metric in ("comment_sample_count", "total_comment_count"):
        obs = metric_observations[metric]
        if obs.posture != MetricPosture.OBSERVED:
            limitations.append(f"{metric}_not_exposed:no_zero_fill")
    return limitations


def _metric_posture_summary(metric_observations: Mapping[str, MetricObservation]) -> str:
    return ";".join(
        f"{metric}={metric_observations[metric].posture.value}" for metric in YOUTUBE_WATCH_METRIC_NAMES
    )


def _validate_comment_page(page: YoutubeWatchCommentPage) -> None:
    if not re.fullmatch(r"youtubei_next_page_\d{2}\.json", page.filename):
        raise ValueError(f"unsafe YouTube comment page filename: {page.filename!r}")
    if not page.raw_json_bytes:
        raise ValueError(f"empty YouTube comment page body: {page.filename}")


def _validate_selected_comments(packet: Mapping[str, Any], *, received_page_count: int) -> None:
    comments = packet.get("comments")
    if not isinstance(comments, list):
        raise ValueError("selected comments must be a list")
    engagement = packet.get("engagement") if isinstance(packet.get("engagement"), Mapping) else {}
    expected = _int_or_none(engagement.get("comment_sample_count"))
    if expected is not None and expected != len(comments):
        raise ValueError(
            f"comment_sample_count {expected} does not match selected comment row count {len(comments)}"
        )
    for index, comment in enumerate(comments, start=1):
        if not isinstance(comment, Mapping):
            raise ValueError(f"selected comment row {index} is not an object")
        comment_id = _string_or_none(comment.get("comment_id"))
        text = comment.get("text")
        page_number = _int_or_none(comment.get("source_page_number"))
        order_in_page = _int_or_none(comment.get("source_order_in_page"))
        order_global = _int_or_none(comment.get("source_order_global"))
        if comment_id is None:
            raise ValueError(f"selected comment row {index} lacks comment_id")
        if not isinstance(text, str):
            raise ValueError(f"selected comment row {index} lacks verbatim text")
        if page_number is None or page_number < 1:
            raise ValueError(f"selected comment row {index} lacks source_page_number")
        if order_in_page is None or order_in_page < 1:
            raise ValueError(f"selected comment row {index} lacks source_order_in_page")
        if order_global != index:
            raise ValueError(
                f"selected comment row {index} has non-contiguous source_order_global {order_global!r}"
            )
    coverage = packet.get("comment_capture_coverage")
    if not isinstance(coverage, Mapping):
        raise ValueError("selected capture lacks comment_capture_coverage")
    pages_fetched = _int_or_none(coverage.get("pages_fetched"))
    selected_count = _int_or_none(coverage.get("selected_comment_count"))
    requested_limit = _int_or_none(coverage.get("requested_page_limit"))
    ordering_posture = _string_or_none(coverage.get("ordering_posture"))
    if pages_fetched != received_page_count:
        raise ValueError(
            f"comment coverage pages_fetched {pages_fetched!r} does not match received page count "
            f"{received_page_count}"
        )
    if selected_count != len(comments):
        raise ValueError(
            f"comment coverage selected_comment_count {selected_count!r} does not match row count "
            f"{len(comments)}"
        )
    if requested_limit is None or requested_limit < pages_fetched:
        raise ValueError("comment coverage requested_page_limit is missing or below pages_fetched")
    if ordering_posture != "source_default_order_as_served":
        raise ValueError(f"unsupported comment ordering_posture {ordering_posture!r}")


def _json_safe_dict(value: Mapping[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(dict(value), ensure_ascii=False))


def _nonempty_string_sequence(value: object) -> bool:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        return False
    return any(_string_or_none(item) is not None for item in value)


def _int_or_none(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        stripped = value.replace(",", "").strip()
        return int(stripped) if stripped.isdigit() else None
    return None


def _string_or_none(value: object) -> str | None:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    return None


def _utc_now_z() -> str:
    return datetime.datetime.utcnow().isoformat() + "Z"


__all__ = [
    "CAPTURE_JSON_NAME",
    "CAPTURE_SCHEMA_VERSION",
    "LEGACY_CAPTURE_SCHEMA_VERSION",
    "SELECTIVE_CAPTURE_POLICY_VERSION",
    "SELECTIVE_RETENTION_POSTURE",
    "SOURCE_SURFACE",
    "WATCH_HTML_NAME",
    "YOUTUBE_WATCH_METRIC_NAMES",
    "YOUTUBE_WATCH_NON_CLAIMS",
    "YoutubeWatchCommentPage",
    "YoutubeWatchFetch",
    "write_youtube_watch_packet",
]
