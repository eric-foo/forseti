"""Bounded, logged-out IG wind-caller CALLS capture -> Source Capture Packet.

Composes existing primitives (no new auth/session path, no secrets):
- browser_snapshot (headless, LOGGED-OUT; scroll to enumerate the profile grid),
- ig_calls_parse (og:description -> caption/likes/comments/date/#ad; permalinks),
- browser-context XHR (web_profile_info + bounded grid pagination -> view counts),
- cadence.bounded_jitter (human-mimicking variable gaps between item visits),
- writer.write_local_source_capture_packet (one packet: profile slice + N call slices).

Substrate basis: the recon + 2026-06-14 headless probe found IG serves the call
signal (caption + engagement) in the post/reel page og:description to a browser,
LOGGED-OUT. The reel view-count path is browser-context profile-feed JSON, also
logged-out. This runner therefore needs no session.

Bounded by the wind-caller carve-out: attended, human-mimicking cadence, no
standing/scheduled crawler, per-run item cap. This is one bounded capture unit
(one named account's recent calls), launched by an operator; there is no
scheduler entrypoint.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import sys
import time
from pathlib import Path
from typing import Callable, Sequence
from urllib.parse import urlparse

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
    write_local_source_capture_packet,
)
from source_capture.adapters import BrowserSnapshotFailure, fetch_browser_snapshot_capture
from source_capture.adapters.browser_snapshot import (
    DEFAULT_MAX_ARTIFACT_BYTES,
    DEFAULT_TIMEOUT_SECONDS,
    BrowserSnapshotFailureKind,
)
from source_capture.cadence import build_cadence_plan
from source_capture.ig_momentum_harvest import (
    IG_ID_CONFLICT_POLICY_VERSION,
    IG_METRIC_REGISTRY_VERSION,
    IgMediaMetricRecord,
    IgProfileMomentumCapture,
    extract_ig_shortcode,
    fetch_ig_profile_momentum,
)
from source_capture.ig_calls_parse import (
    extract_item_permalinks,
    extract_meta_content,
    parse_ig_og_description,
    parse_ig_profile_og,
)
from source_capture.models import CoverageWindow, MetricObservation, MetricPosture
from source_capture.proxy_profiles import (
    ProxyCategory,
    ProxyProfile,
    load_proxy_profile,
    load_proxy_profile_by_label,
)

IG_CALLS_NON_CLAIMS = [
    "not content sufficiency proof",
    "not login or session capture",
    "not stored profile or cookie use",
    "not anti-detect behavior",
    "not proxy endpoint or credential disclosure",
    "not per-request proxy rotation",
    "not CAPTCHA solving",
    "not crawler or scheduled monitoring",
    "not full-history backfill",
    "not full momentum curve",
    "not projection fold",
    "not media byte preservation",
    "not API SDK use",
    "not ECR design",
    "not Cleaning implementation",
    "not Judgment scoring",
    "not buyer proof",
    "not commercial-readiness logic",
]

DEFAULT_MAX_ITEMS = 12
DEFAULT_PROFILE_SCROLL_PASSES = 3
DEFAULT_CADENCE_WINDOW_SECONDS = 900.0
DEFAULT_CADENCE_MIN_GAP_SECONDS = 8.0
DEFAULT_CADENCE_MAX_GAP_SECONDS = 45.0
DEFAULT_XHR_REQUEST_GAP_SECONDS = 3.0
DEFAULT_VIEW_COUNT_MAX_GRAPHQL_PAGES = 1
DEFAULT_IG_PROFILE_VIEWPORT_WIDTH = 768
DEFAULT_IG_PROFILE_VIEWPORT_HEIGHT = 1024
DEFAULT_PROFILE_SETTLE_SECONDS = 3.0
DEFAULT_PROFILE_LINK_RETRIES = 1
DEFAULT_PROFILE_LINK_RETRY_BACKOFF_SECONDS = 2.5
_CAPTURED_ITEM_STATUSES = frozenset({"captured", "captured_with_profile_feed_json"})


def _detect_ig_block(*, final_url: str, title: str | None, visible_text: str, rendered_dom: str) -> str | None:
    """Return a block reason if the page is an access/anti-bot wall, else None.

    Logged-out IG shows "Log in"/"Sign up" while still serving the og:description,
    so those alone are NOT a block. Only a login redirect, a 429 interstitial, or
    an explicit network-security block count.
    """
    final_low = final_url.lower()
    if "/accounts/login" in final_low:
        return "redirected_to_login"
    probe = f"{title or ''}\n{visible_text[:3000]}\n{rendered_dom[:3000]}".lower()
    if "please wait a few minutes before you try again" in probe:
        return "rate_limited_429_interstitial"
    if "you've been blocked" in probe or "you have been blocked" in probe:
        return "network_security_block"
    return None


DEFAULT_CAPTURE_RETRY_BACKOFF_SECONDS = 2.5

# Transient capture failures worth retrying. A successful-but-BLOCKED page (login
# redirect / 429) is NOT a BrowserSnapshotFailure -- it is handled by the caller's
# _detect_ig_block and is deliberately never retried here (retrying a wall only
# deepens the throttle).
_RETRYABLE_CAPTURE_FAILURES = frozenset({
    BrowserSnapshotFailureKind.TIMEOUT,
    BrowserSnapshotFailureKind.CAPTURE_FAILED,
})


def _capture_one(url: str, *, scroll_passes: int, timeout_seconds: float, viewport_width: int,
                 viewport_height: int, max_artifact_bytes: int,
                 proxy_profile: ProxyProfile | None = None,
                 max_attempts: int = 1, retry_backoff_seconds: float = 0.0,
                 settle_seconds: float = 0.0,
                 sleep_fn: Callable[[float], None] = time.sleep):
    attempt = 0
    while True:
        attempt += 1
        result = fetch_browser_snapshot_capture(
            url=url,
            timeout_seconds=timeout_seconds,
            wait_until="load",
            viewport_width=viewport_width,
            viewport_height=viewport_height,
            max_artifact_bytes=max_artifact_bytes,
            proxy_profile=proxy_profile,
            scroll_passes=scroll_passes,
            settle_seconds=settle_seconds,
        )
        if not isinstance(result, BrowserSnapshotFailure):
            return result
        if result.failure_kind not in _RETRYABLE_CAPTURE_FAILURES or attempt >= max_attempts:
            return result
        if retry_backoff_seconds > 0:
            sleep_fn(retry_backoff_seconds * attempt)  # linear backoff


def _profile_handle_from_url(profile_url: str) -> str | None:
    path_parts = [part for part in urlparse(profile_url).path.split("/") if part]
    return path_parts[0] if path_parts else None


def _timestamp_iso(timestamp: int | None) -> str | None:
    if timestamp is None:
        return None
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def _caption_has_ad_disclosure(caption: str | None) -> bool:
    if not caption:
        return False
    lowered = caption.casefold()
    return "#ad" in lowered or "paid partnership" in lowered


def _media_permalink_url(*, profile_url: str, media: IgMediaMetricRecord) -> str:
    handle = _profile_handle_from_url(profile_url)
    route = "p"
    if media.product_type == "clips" or (media.product_type is None and media.is_video is True):
        route = "reel"
    if handle:
        return f"https://www.instagram.com/{handle}/{route}/{media.shortcode}/"
    return f"https://www.instagram.com/{route}/{media.shortcode}/"


def _permalink_by_shortcode(permalinks: Sequence[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for permalink in permalinks:
        shortcode = extract_ig_shortcode(permalink)
        if shortcode and shortcode not in out:
            out[shortcode] = permalink
    return out


def _select_item_permalinks(
    *,
    profile_url: str,
    dom_permalinks: Sequence[str],
    momentum_capture: IgProfileMomentumCapture | None,
    max_items: int,
) -> tuple[list[str], str, int]:
    if dom_permalinks:
        source = "profile_dom_grid"
        if momentum_capture is not None and momentum_capture.media_by_shortcode:
            source = "profile_dom_grid_with_profile_feed_json_metrics"
        return list(dom_permalinks[:max_items]), source, 0

    if momentum_capture is not None and momentum_capture.media_by_shortcode:
        media_records = sorted(
            momentum_capture.media_by_shortcode.values(),
            key=lambda item: item.taken_at_timestamp if item.taken_at_timestamp is not None else -1,
            reverse=True,
        )
        urls = [
            _media_permalink_url(profile_url=profile_url, media=media)
            for media in media_records[:max_items]
        ]
        if urls:
            return urls, "profile_feed_json_timestamp_desc", len(urls)
    return [], "none", 0


def _capture_profile_with_permalink_retry(
    *,
    profile_url: str,
    profile_scroll_passes: int,
    timeout_seconds: float,
    viewport_width: int,
    viewport_height: int,
    max_artifact_bytes: int,
    proxy_profile: ProxyProfile | None,
    capture_retries: int,
    capture_retry_backoff_seconds: float,
    profile_settle_seconds: float,
    profile_link_retries: int,
    profile_link_retry_backoff_seconds: float,
    sleep_fn: Callable[[float], None],
):
    last_profile = None
    last_permalinks: list[str] = []
    for attempt in range(profile_link_retries + 1):
        profile = _capture_one(
            profile_url,
            scroll_passes=profile_scroll_passes,
            timeout_seconds=timeout_seconds,
            viewport_width=viewport_width,
            viewport_height=viewport_height,
            max_artifact_bytes=max_artifact_bytes,
            proxy_profile=proxy_profile,
            max_attempts=capture_retries + 1,
            retry_backoff_seconds=capture_retry_backoff_seconds,
            settle_seconds=profile_settle_seconds,
            sleep_fn=sleep_fn,
        )
        if isinstance(profile, BrowserSnapshotFailure):
            return profile, []
        last_profile = profile
        block = _detect_ig_block(
            final_url=profile.final_url,
            title=profile.title,
            visible_text=profile.visible_text,
            rendered_dom=profile.rendered_dom,
        )
        if block is not None:
            return profile, []
        last_permalinks = extract_item_permalinks(
            profile.rendered_dom,
            profile_handle=_profile_handle_from_url(profile.final_url or profile.requested_url),
        )
        if last_permalinks:
            return profile, last_permalinks
        if attempt < profile_link_retries and profile_link_retry_backoff_seconds > 0:
            sleep_fn(profile_link_retry_backoff_seconds)
    return last_profile, last_permalinks


def _media_for_item_url(
    *,
    url: str,
    momentum_capture: IgProfileMomentumCapture | None,
) -> IgMediaMetricRecord | None:
    shortcode = extract_ig_shortcode(url)
    if momentum_capture is None or shortcode is None:
        return None
    return momentum_capture.media_by_shortcode.get(shortcode)


def _has_usable_call_signal(record: dict) -> bool:
    return bool(
        record.get("caption")
        and (record.get("date") or record.get("source_timestamp"))
        and (record.get("likes") is not None or record.get("comments") is not None)
    )


def _build_item_record(
    *,
    url: str,
    item_page_status: str,
    parsed,
    media: IgMediaMetricRecord | None,
    item_page_message: str | None = None,
    block_reason: str | None = None,
) -> dict:
    sources: dict[str, str] = {}
    caption = parsed.caption if parsed and parsed.caption else None
    if caption is not None:
        sources["caption"] = "og_description"
    elif media is not None and media.caption:
        caption = media.caption
        sources["caption"] = "profile_feed_json"

    likes = parsed.likes if parsed and parsed.likes is not None else None
    if likes is not None:
        sources["likes"] = "og_description"
    elif media is not None and media.like_count is not None:
        likes = media.like_count
        sources["likes"] = "profile_feed_json"

    comments = parsed.comments if parsed and parsed.comments is not None else None
    if comments is not None:
        sources["comments"] = "og_description"
    elif media is not None and media.comment_count is not None:
        comments = media.comment_count
        sources["comments"] = "profile_feed_json"

    date = parsed.date if parsed and parsed.date else None
    if date is not None:
        sources["date"] = "og_description"

    source_timestamp = media.taken_at_timestamp if media is not None else None
    source_timestamp_iso = _timestamp_iso(source_timestamp)
    if source_timestamp is not None:
        sources["source_timestamp"] = "profile_feed_json"

    status = item_page_status
    if caption and (date or source_timestamp) and (likes is not None or comments is not None):
        status = "captured" if parsed is not None and _has_captured_call_signal(parsed) else "captured_with_profile_feed_json"
    elif parsed is not None or caption or date or source_timestamp is not None or likes is not None or comments is not None:
        status = "partial_signal"

    if status == "captured_with_profile_feed_json":
        message = "item page signal incomplete; profile-feed JSON supplied the minimum call signal"
    elif status == "partial_signal":
        message = (
            "logged-out item/profile-feed signals did not contain the minimum call signal "
            "(caption, date/timestamp, and at least one engagement count)"
        )
    elif status == "no_signal":
        message = item_page_message or "no og:description on item page and no usable profile-feed JSON fallback"
    else:
        message = item_page_message

    record = {
        "url": url,
        "status": status,
        "item_page_status": item_page_status,
        "message": message,
        "caption": caption,
        "likes": likes,
        "comments": comments,
        "date": date,
        "source_timestamp": source_timestamp,
        "source_timestamp_iso": source_timestamp_iso,
        "is_ad": bool((parsed and parsed.is_ad) or _caption_has_ad_disclosure(caption)),
        "caption_truncated": bool(parsed and parsed.truncated),
        "raw_og": parsed.raw_og if parsed else None,
        "signal_sources": sources,
    }
    if block_reason is not None:
        record["block_reason"] = block_reason
    if media is not None:
        record.update(
            {
                "media_shortcode": media.shortcode,
                "media_is_video": media.is_video,
                "media_typename": media.typename,
                "media_product_type": media.product_type,
            }
        )
    return record


def _has_captured_call_signal(parsed) -> bool:
    return bool(
        parsed.caption
        and parsed.date
        and (parsed.likes is not None or parsed.comments is not None)
    )


def _observed_metric(metric: str, value: int, *, capture_timestamp: str) -> MetricObservation:
    return MetricObservation(
        metric=metric,
        posture=MetricPosture.OBSERVED,
        value=value,
        coverage_window=CoverageWindow(end=capture_timestamp),
    )


def _gap_metric(
    metric: str,
    posture: MetricPosture,
    reason: str,
    *,
    capture_timestamp: str,
) -> MetricObservation:
    return MetricObservation(
        metric=metric,
        posture=posture,
        reason=reason,
        coverage_window=CoverageWindow(end=capture_timestamp),
    )


def _profile_metric_observations(
    *,
    momentum_capture: IgProfileMomentumCapture | None,
    capture_timestamp: str,
    capture_view_counts: bool,
) -> list[MetricObservation]:
    if not capture_view_counts:
        return [
            _gap_metric(
                "follower_count",
                MetricPosture.NOT_ATTEMPTED,
                "browser-context web_profile_info capture was disabled for this run",
                capture_timestamp=capture_timestamp,
            )
        ]
    if momentum_capture is not None and momentum_capture.follower_count is not None:
        return [
            _observed_metric(
                "follower_count",
                momentum_capture.follower_count,
                capture_timestamp=capture_timestamp,
            )
        ]
    reason = "browser-context web_profile_info did not yield an exact follower_count"
    if momentum_capture is not None and momentum_capture.limitation_notes:
        reason = "; ".join(momentum_capture.limitation_notes)
    return [
        _gap_metric(
            "follower_count",
            MetricPosture.UNAVAILABLE_WITH_REASON,
            reason,
            capture_timestamp=capture_timestamp,
        )
    ]


def _item_metric_observations(
    *,
    record: dict,
    momentum_capture: IgProfileMomentumCapture | None,
    capture_timestamp: str,
    capture_view_counts: bool,
) -> list[MetricObservation]:
    observations: list[MetricObservation] = []
    likes = record.get("likes")
    comments = record.get("comments")
    if isinstance(likes, int):
        observations.append(_observed_metric("like_count", likes, capture_timestamp=capture_timestamp))
    elif record.get("status") in _CAPTURED_ITEM_STATUSES:
        observations.append(
            _gap_metric(
                "like_count",
                MetricPosture.UNAVAILABLE_WITH_REASON,
                "og:description call signal did not include like count",
                capture_timestamp=capture_timestamp,
            )
        )
    if isinstance(comments, int):
        observations.append(_observed_metric("comment_count", comments, capture_timestamp=capture_timestamp))
    elif record.get("status") in _CAPTURED_ITEM_STATUSES:
        observations.append(
            _gap_metric(
                "comment_count",
                MetricPosture.UNAVAILABLE_WITH_REASON,
                "og:description call signal did not include comment count",
                capture_timestamp=capture_timestamp,
            )
        )

    if not capture_view_counts:
        observations.append(
            _gap_metric(
                "view_count",
                MetricPosture.NOT_ATTEMPTED,
                "browser-context profile-feed JSON capture was disabled for this run",
                capture_timestamp=capture_timestamp,
            )
        )
        return observations

    shortcode = extract_ig_shortcode(str(record.get("url", "")))
    media = momentum_capture.media_by_shortcode.get(shortcode) if momentum_capture and shortcode else None
    if media is None:
        reason = "browser-context profile-feed JSON did not include this shortcode"
        status = str(record.get("status", "unknown"))
        if status not in _CAPTURED_ITEM_STATUSES:
            reason = f"{reason}; item status={status}"
        if momentum_capture is not None and momentum_capture.limitation_notes:
            reason = "; ".join(momentum_capture.limitation_notes)
        observations.append(
            _gap_metric(
                "view_count",
                MetricPosture.UNAVAILABLE_WITH_REASON,
                reason,
                capture_timestamp=capture_timestamp,
            )
        )
        return observations

    if media.video_view_count is not None:
        observations.append(_observed_metric("view_count", media.video_view_count, capture_timestamp=capture_timestamp))
    elif media.is_video is False:
        observations.append(
            _gap_metric(
                "view_count",
                MetricPosture.NOT_APPLICABLE,
                "IG profile-feed JSON marks this media as non-video",
                capture_timestamp=capture_timestamp,
            )
        )
    else:
        observations.append(
            _gap_metric(
                "view_count",
                MetricPosture.UNAVAILABLE_WITH_REASON,
                "IG profile-feed JSON did not include video_view_count for this media",
                capture_timestamp=capture_timestamp,
            )
        )
    return observations


def run_source_capture_ig_calls_packet(
    *,
    profile_url: str,
    output_directory: Path,
    decision_question: str,
    max_items: int = DEFAULT_MAX_ITEMS,
    profile_scroll_passes: int = DEFAULT_PROFILE_SCROLL_PASSES,
    cadence_window_seconds: float = DEFAULT_CADENCE_WINDOW_SECONDS,
    cadence_min_gap_seconds: float = DEFAULT_CADENCE_MIN_GAP_SECONDS,
    cadence_max_gap_seconds: float = DEFAULT_CADENCE_MAX_GAP_SECONDS,
    cadence_random_seed: int | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    viewport_width: int = DEFAULT_IG_PROFILE_VIEWPORT_WIDTH,
    viewport_height: int = DEFAULT_IG_PROFILE_VIEWPORT_HEIGHT,
    max_artifact_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
    capture_view_counts: bool = True,
    view_count_max_graphql_pages: int = DEFAULT_VIEW_COUNT_MAX_GRAPHQL_PAGES,
    xhr_request_gap_seconds: float = DEFAULT_XHR_REQUEST_GAP_SECONDS,
    capture_retries: int = 0,
    capture_retry_backoff_seconds: float = DEFAULT_CAPTURE_RETRY_BACKOFF_SECONDS,
    profile_settle_seconds: float = DEFAULT_PROFILE_SETTLE_SECONDS,
    profile_link_retries: int = DEFAULT_PROFILE_LINK_RETRIES,
    profile_link_retry_backoff_seconds: float = DEFAULT_PROFILE_LINK_RETRY_BACKOFF_SECONDS,
    proxy_profile: ProxyProfile | None = None,
    capture_context: str = "logged-out IG wind-caller calls capture (no session); one bounded account, recent calls",
    operator_category: str = "ig_calls_browser_snapshot_cli_operator",
    session_id: str | None = None,
    warnings: Sequence[str] = (),
    limitations: Sequence[str] = (),
    sleep_fn: Callable[[float], None] = time.sleep,
) -> tuple[int, str]:
    if max_items <= 0:
        raise ValueError("max_items must be greater than zero")
    if max_items > DEFAULT_MAX_ITEMS:
        raise ValueError(f"max_items must be no greater than {DEFAULT_MAX_ITEMS} for this bounded runner")
    if xhr_request_gap_seconds < 2.5:
        raise ValueError("xhr_request_gap_seconds must be at least 2.5 seconds")
    if profile_settle_seconds < 0:
        raise ValueError("profile_settle_seconds must be zero or greater")
    if profile_link_retries < 0:
        raise ValueError("profile_link_retries must be zero or greater")
    if profile_link_retry_backoff_seconds < 0:
        raise ValueError("profile_link_retry_backoff_seconds must be zero or greater")

    profile, dom_permalinks = _capture_profile_with_permalink_retry(
        profile_url=profile_url,
        profile_scroll_passes=profile_scroll_passes,
        timeout_seconds=timeout_seconds,
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        max_artifact_bytes=max_artifact_bytes,
        proxy_profile=proxy_profile,
        capture_retries=capture_retries,
        capture_retry_backoff_seconds=capture_retry_backoff_seconds,
        profile_settle_seconds=profile_settle_seconds,
        profile_link_retries=profile_link_retries,
        profile_link_retry_backoff_seconds=profile_link_retry_backoff_seconds,
        sleep_fn=sleep_fn,
    )
    if isinstance(profile, BrowserSnapshotFailure):
        return 3, f"profile capture failed: {profile.message}"
    block = _detect_ig_block(
        final_url=profile.final_url, title=profile.title,
        visible_text=profile.visible_text, rendered_dom=profile.rendered_dom,
    )
    if block is not None:
        return 3, f"profile access-blocked ({block}); recorded NO-GO, no packet written"

    profile_og = extract_meta_content(profile.rendered_dom, "og:description")
    profile_stats = parse_ig_profile_og(profile_og) if profile_og else None
    capture_timestamp = str(profile.metadata["capture_timestamp"])
    momentum_capture: IgProfileMomentumCapture | None = None
    if capture_view_counts:
        sleep_fn(xhr_request_gap_seconds)
        momentum_capture = fetch_ig_profile_momentum(
            profile_url=profile.final_url or profile.requested_url,
            max_media=max_items,
            max_graphql_pages=view_count_max_graphql_pages,
            request_gap_seconds=xhr_request_gap_seconds,
            timeout_seconds=timeout_seconds,
            max_response_bytes=max_artifact_bytes,
            proxy_profile=proxy_profile,
            sleep_fn=sleep_fn,
        )

    permalinks, enumeration_source, generated_permalink_count = _select_item_permalinks(
        profile_url=profile.final_url or profile.requested_url,
        dom_permalinks=dom_permalinks,
        momentum_capture=momentum_capture,
        max_items=max_items,
    )
    if not permalinks:
        return 3, "no /p/ or /reel/ permalinks enumerated from profile DOM or profile-feed JSON"
    if capture_view_counts:
        sleep_fn(xhr_request_gap_seconds)

    # Human-mimicking gaps between the per-item visits (auditable, deterministic per seed).
    cadence = build_cadence_plan(
        slot_count=len(permalinks),
        mode="bounded_jitter",
        delay_seconds=0.0,
        window_seconds=cadence_window_seconds,
        min_gap_seconds=cadence_min_gap_seconds,
        max_gap_seconds=cadence_max_gap_seconds,
        random_seed=cadence_random_seed,
    )

    item_records: list[dict] = []
    for index, url in enumerate(permalinks):
        if index > 0:
            sleep_fn(cadence.planned_waits_seconds[index - 1])
        media = _media_for_item_url(url=url, momentum_capture=momentum_capture)
        item = _capture_one(
            url, scroll_passes=0, timeout_seconds=timeout_seconds, viewport_width=viewport_width,
            viewport_height=viewport_height, max_artifact_bytes=max_artifact_bytes,
            proxy_profile=proxy_profile,
            max_attempts=capture_retries + 1, retry_backoff_seconds=capture_retry_backoff_seconds, sleep_fn=sleep_fn,
        )
        if isinstance(item, BrowserSnapshotFailure):
            item_records.append(
                _build_item_record(
                    url=url,
                    item_page_status="capture_failed",
                    parsed=None,
                    media=media,
                    item_page_message=item.message,
                )
            )
            continue
        item_block = _detect_ig_block(
            final_url=item.final_url, title=item.title,
            visible_text=item.visible_text, rendered_dom=item.rendered_dom,
        )
        if item_block is not None:
            item_records.append(
                _build_item_record(
                    url=item.final_url,
                    item_page_status="access_blocked",
                    parsed=None,
                    media=media,
                    block_reason=item_block,
                    item_page_message=f"item access-blocked ({item_block})",
                )
            )
            continue
        og = extract_meta_content(item.rendered_dom, "og:description")
        parsed = parse_ig_og_description(og) if og else None
        item_records.append(
            _build_item_record(
                url=item.final_url,
                item_page_status="captured" if parsed is not None else "no_signal",
                parsed=parsed,
                media=media,
                item_page_message=None if og else "no og:description on item page",
            )
        )

    return _write_packet(
        profile_url=profile.requested_url,
        profile_final_url=profile.final_url,
        profile_stats=profile_stats,
        permalink_count=len(permalinks),
        dom_permalink_count=len(dom_permalinks),
        profile_feed_media_count=len(momentum_capture.media_by_shortcode) if momentum_capture is not None else 0,
        enumeration_source=enumeration_source,
        generated_permalink_count=generated_permalink_count,
        capture_timestamp=capture_timestamp,
        cadence_summary=cadence.to_dict(),
        item_records=item_records,
        output_directory=output_directory,
        decision_question=decision_question,
        capture_context=capture_context,
        operator_category=operator_category,
        session_id=session_id,
        warnings=list(warnings),
        limitations=list(limitations),
        momentum_capture=momentum_capture,
        capture_view_counts=capture_view_counts,
        profile_capture_metadata=profile.metadata,
        proxy_profile=proxy_profile,
    )


def _slice_postures():
    access = known_fact(
        "ig_logged_out_browser_snapshot; public og:description; content sufficiency not asserted"
    )
    archive = not_attempted("IG calls runner does not query archive or history services")
    media = known_fact(
        "og:description caption + engagement text preserved; browser-context profile-feed JSON checked for view counts; media bytes are out of scope"
    )
    recapture = not_applicable("no prior source capture packet was supplied for this IG calls capture")
    return access, archive, media, recapture


def _write_packet(
    *,
    profile_url: str,
    profile_final_url: str,
    profile_stats,
    permalink_count: int,
    dom_permalink_count: int,
    profile_feed_media_count: int,
    enumeration_source: str,
    generated_permalink_count: int,
    capture_timestamp: str,
    cadence_summary: dict,
    item_records: list[dict],
    output_directory: Path,
    decision_question: str,
    capture_context: str,
    operator_category: str,
    session_id: str | None,
    warnings: list[str],
    limitations: list[str],
    momentum_capture: IgProfileMomentumCapture | None,
    capture_view_counts: bool,
    profile_capture_metadata: dict[str, object],
    proxy_profile: ProxyProfile | None,
) -> tuple[int, str]:
    access, archive, media, recapture = _slice_postures()
    staging_parent = output_directory.parent
    staging_parent.mkdir(parents=True, exist_ok=True)

    captured_count = sum(1 for r in item_records if _has_usable_call_signal(r))
    stats_dict = (
        {"followers": profile_stats.followers, "following": profile_stats.following, "posts": profile_stats.posts}
        if profile_stats is not None
        else None
    )
    profile_payload = {
        "profile_url": profile_final_url,
        "stats": stats_dict,
        "permalinks_enumerated": permalink_count,
        "dom_permalinks_detected": dom_permalink_count,
        "profile_feed_media_detected": profile_feed_media_count,
        "enumeration_source": enumeration_source,
        "generated_permalink_count": generated_permalink_count,
        "cadence_plan": cadence_summary,
        "capture_metadata": {
            "viewport_width": profile_capture_metadata.get("viewport_width"),
            "viewport_height": profile_capture_metadata.get("viewport_height"),
            "proxy_used": proxy_profile is not None or profile_capture_metadata.get("proxy_used", False),
            "proxy_category": (
                proxy_profile.proxy_category.value
                if proxy_profile is not None
                else profile_capture_metadata.get("proxy_category")
            ),
            "proxy_disclosure": (
                "category_only"
                if proxy_profile is not None
                else profile_capture_metadata.get("proxy_disclosure", "none")
            ),
            "proxy_endpoint_recorded": False,
            "proxy_exit_ip_recorded": False,
        },
    }

    # One staged file per slice: file_01 = profile, file_02.. = each item.
    staged: list[tuple[Path, dict]] = [(staging_parent / "ig_profile.json", profile_payload)]
    profile_file_ids = ["file_01"]
    if capture_view_counts:
        momentum_payload = (
            momentum_capture.to_staged_payload()
            if momentum_capture is not None
            else {
                "status": "not_attempted",
                "reason": "browser-context profile-feed JSON capture did not run",
            }
        )
        profile_file_ids.append(f"file_{len(staged) + 1:02d}")
        staged.append((staging_parent / "ig_profile_momentum.json", momentum_payload))
    item_file_ids: list[str] = []
    for i, record in enumerate(item_records, start=1):
        item_file_ids.append(f"file_{len(staged) + 1:02d}")
        staged.append((staging_parent / f"ig_call_{i:02d}.json", record))

    if any(path.exists() for path, _ in staged):
        raise ValueError("IG calls staging files already exist in the output parent; clear them before rerunning")

    written: list[Path] = []
    try:
        for path, payload in staged:
            written.append(path)
            path.write_text(
                json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                encoding="utf-8",
                newline="\n",
            )

        def _timing(publication) -> PacketTiming:
            return PacketTiming(
                source_publication_or_event=publication,
                source_edit_or_version=unknown_with_reason("IG calls runner did not infer source edit/version timing"),
                capture_time=known_fact(capture_timestamp),
                recapture_time=not_applicable("IG calls packet does not model an earlier capture by default"),
                cutoff_posture=unknown_with_reason("IG calls runner did not receive cutoff posture metadata"),
            )

        profile_timing = _timing(
            unknown_with_reason("profile slice is the enumeration source, not a dated post")
        )
        slices = [
            SourceCaptureSlice(
                slice_id="ig_profile_00",
                locator=known_fact(profile_final_url),
                timing=profile_timing,
                access_posture=access,
                archive_history_posture=archive,
                media_modality_posture=media,
                re_capture_relationship=recapture,
                limitations=[],
                warning_notes=[],
                preserved_file_ids=profile_file_ids,
                metric_observations=_profile_metric_observations(
                    momentum_capture=momentum_capture,
                    capture_timestamp=capture_timestamp,
                    capture_view_counts=capture_view_counts,
                ),
            )
        ]
        for i, record in enumerate(item_records, start=1):
            date = record.get("date")
            source_timestamp_iso = record.get("source_timestamp_iso")
            publication_value = date or source_timestamp_iso
            publication = known_fact(str(publication_value)) if publication_value else unknown_with_reason(
                f"item {record['status']}: no post date/timestamp parsed"
            )
            slice_limitations: list[str] = []
            if not _has_usable_call_signal(record):
                slice_limitations.append(f"item_not_captured: {record['status']}")
            elif record["status"] != "captured":
                slice_limitations.append(f"item_page_signal_fallback: {record['status']}")
            if record.get("item_page_status") not in {None, "captured"}:
                slice_limitations.append(f"item_page_status: {record['item_page_status']}")
            if record.get("caption_truncated"):
                slice_limitations.append(
                    "caption_truncated_in_og: long caption may be cut at IG's og cap; profile-feed JSON fallback checked when available"
                )
            slices.append(
                SourceCaptureSlice(
                    slice_id=f"ig_call_{i:02d}",
                    locator=known_fact(record["url"]),
                    timing=_timing(publication),
                    access_posture=access,
                    archive_history_posture=archive,
                    media_modality_posture=media,
                    re_capture_relationship=recapture,
                    limitations=slice_limitations,
                    warning_notes=[],
                    preserved_file_ids=[item_file_ids[i - 1]],
                    metric_observations=_item_metric_observations(
                        record=record,
                        momentum_capture=momentum_capture,
                        capture_timestamp=capture_timestamp,
                        capture_view_counts=capture_view_counts,
                    ),
                )
            )

        run_limitations = list(limitations)
        run_warnings = list(warnings)
        if momentum_capture is not None:
            run_limitations.extend(momentum_capture.limitation_notes)
            run_warnings.extend(momentum_capture.warning_notes)
            if momentum_capture.numeric_id is None:
                run_limitations.append("ig_numeric_id_unavailable_from_profile_feed_json")
            run_limitations.append(
                f"ig_metric_registry_version={IG_METRIC_REGISTRY_VERSION}; "
                f"ig_identity_conflict_policy_version={IG_ID_CONFLICT_POLICY_VERSION}"
            )
        run_limitations.append(f"item_enumeration_source={enumeration_source}")
        if dom_permalink_count == 0 and profile_feed_media_count > 0:
            run_limitations.append("profile_dom_grid_permalinks_empty; profile_feed_json_used_for_enumeration")
        if generated_permalink_count > 0:
            run_limitations.append(
                f"profile_feed_json_generated_item_locators={generated_permalink_count}; "
                "DOM did not supply exact permalink for every shortcode"
            )
        if captured_count < len(item_records):
            run_limitations.append(
                f"partial_capture: {captured_count}/{len(item_records)} items yielded a usable call record"
            )
        if proxy_profile is not None:
            run_limitations.append(
                "proxy_profile_used: category="
                f"{proxy_profile.proxy_category.value}; endpoint, credentials, exit IP, and store path not recorded"
            )
        view_count_observed = sum(
            1
            for source_slice in slices
            for observation in source_slice.metric_observations
            if observation.metric == "view_count" and observation.posture == MetricPosture.OBSERVED
        )
        visible_mode_changes = [
            f"ig_calls_logged_out_capture:items={len(item_records)}:captured={captured_count}",
            f"ig_item_enumeration_source:{enumeration_source}",
            f"ig_browser_context_view_count_capture:items_observed={view_count_observed}",
        ]
        if not capture_view_counts:
            visible_mode_changes.append("ig_browser_context_view_count_capture:not_attempted")

        result = write_local_source_capture_packet(
            output_directory=output_directory,
            input_files=written,
            source_family="instagram_creator",
            source_surface="ig_calls_browser_snapshot",
            source_locator=known_fact(profile_url),
            decision_question=decision_question,
            capture_context=capture_context,
            actor_audience_context=known_fact(
                "public-figure creator public profile; logged-out capture; internal wind-caller calibration"
            ),
            capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
            operator_category=operator_category,
            session_identity=session_id,
            visible_mode_changes=visible_mode_changes,
            source_publication_or_event=profile_timing.source_publication_or_event,
            source_edit_or_version=profile_timing.source_edit_or_version,
            cutoff_posture=profile_timing.cutoff_posture,
            recapture_time=profile_timing.recapture_time,
            access_posture=access,
            archive_history_posture=archive,
            media_modality_posture=media,
            re_capture_relationship=recapture,
            source_slices=slices,
            warnings=run_warnings,
            limitations=run_limitations,
            receipt_summary=(
                f"IG calls packet for {profile_final_url}: {captured_count} of {len(item_records)} "
                "enumerated items yielded a usable logged-out call record; "
                f"{view_count_observed} item(s) yielded observed IG video_view_count metric values."
            ),
            receipt_non_claims=IG_CALLS_NON_CLAIMS,
        )
    finally:
        for path in written:
            try:
                path.unlink()
            except FileNotFoundError:
                pass
    return 0, result.output_directory


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Capture one IG creator's recent CALLS (logged-out) into a Source Capture Packet."
    )
    parser.add_argument("--profile-url", required=True)
    parser.add_argument("--decision-question", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-items", type=int, default=DEFAULT_MAX_ITEMS)
    parser.add_argument("--profile-scroll-passes", type=int, default=DEFAULT_PROFILE_SCROLL_PASSES)
    parser.add_argument("--cadence-window-seconds", type=float, default=DEFAULT_CADENCE_WINDOW_SECONDS)
    parser.add_argument("--cadence-min-gap-seconds", type=float, default=DEFAULT_CADENCE_MIN_GAP_SECONDS)
    parser.add_argument("--cadence-max-gap-seconds", type=float, default=DEFAULT_CADENCE_MAX_GAP_SECONDS)
    parser.add_argument("--cadence-random-seed", type=int, default=None)
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--max-artifact-bytes", type=int, default=DEFAULT_MAX_ARTIFACT_BYTES)
    parser.add_argument("--skip-view-counts", action="store_true")
    parser.add_argument("--view-count-max-graphql-pages", type=int, default=DEFAULT_VIEW_COUNT_MAX_GRAPHQL_PAGES)
    parser.add_argument("--xhr-request-gap-seconds", type=float, default=DEFAULT_XHR_REQUEST_GAP_SECONDS)
    parser.add_argument("--capture-retries", type=int, default=0,
                        help="extra retries for a TRANSIENT capture failure (timeout/capture_failed); never retries a block")
    parser.add_argument("--capture-retry-backoff-seconds", type=float, default=DEFAULT_CAPTURE_RETRY_BACKOFF_SECONDS)
    parser.add_argument("--profile-settle-seconds", type=float, default=DEFAULT_PROFILE_SETTLE_SECONDS)
    parser.add_argument("--profile-link-retries", type=int, default=DEFAULT_PROFILE_LINK_RETRIES)
    parser.add_argument(
        "--profile-link-retry-backoff-seconds",
        type=float,
        default=DEFAULT_PROFILE_LINK_RETRY_BACKOFF_SECONDS,
    )
    proxy_group = parser.add_argument_group(
        "proxy profile",
        "Optional label-indirected proxy use. The endpoint and credentials stay in the local secret store; "
        "packets record category-only provenance.",
    )
    proxy_group.add_argument(
        "--proxy-label",
        "--proxy-profile-label",
        dest="proxy_profile_label",
        default=None,
        help="Registered proxy profile label. If --proxy-category is omitted, the runner uses the sidecar category.",
    )
    proxy_group.add_argument(
        "--proxy-category",
        "--proxy-profile-category",
        dest="proxy_profile_category",
        choices=[item.value for item in ProxyCategory],
        default=None,
        help="Optional category assertion for the selected label; rejects the run if it disagrees with the sidecar.",
    )
    proxy_group.add_argument(
        "--proxy-root",
        "--proxy-profile-root",
        dest="proxy_profile_root",
        type=Path,
        default=None,
        help="Optional local proxy profile store root. Never recorded in packet output.",
    )
    parser.add_argument("--session-id", default=None)
    parser.add_argument("--warning", action="append", default=[])
    parser.add_argument("--limitation", action="append", default=[])
    return parser


def _load_optional_proxy_profile(
    *,
    label: str | None,
    category: str | None,
    profile_root: Path | None,
) -> ProxyProfile | None:
    if not label and not category:
        return None
    if not label:
        raise ValueError("proxy capture requires --proxy-label when --proxy-category is supplied")
    if not category:
        return load_proxy_profile_by_label(label=label, profile_root=profile_root)
    return load_proxy_profile(
        label=label,
        proxy_category=ProxyCategory(category),
        profile_root=profile_root,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        proxy_profile = _load_optional_proxy_profile(
            label=args.proxy_profile_label,
            category=args.proxy_profile_category,
            profile_root=args.proxy_profile_root,
        )
        exit_code, message = run_source_capture_ig_calls_packet(
            profile_url=args.profile_url,
            output_directory=args.output,
            decision_question=args.decision_question,
            max_items=args.max_items,
            profile_scroll_passes=args.profile_scroll_passes,
            cadence_window_seconds=args.cadence_window_seconds,
            cadence_min_gap_seconds=args.cadence_min_gap_seconds,
            cadence_max_gap_seconds=args.cadence_max_gap_seconds,
            cadence_random_seed=args.cadence_random_seed,
            timeout_seconds=args.timeout_seconds,
            max_artifact_bytes=args.max_artifact_bytes,
            capture_view_counts=not args.skip_view_counts,
            view_count_max_graphql_pages=args.view_count_max_graphql_pages,
            xhr_request_gap_seconds=args.xhr_request_gap_seconds,
            capture_retries=args.capture_retries,
            capture_retry_backoff_seconds=args.capture_retry_backoff_seconds,
            profile_settle_seconds=args.profile_settle_seconds,
            profile_link_retries=args.profile_link_retries,
            profile_link_retry_backoff_seconds=args.profile_link_retry_backoff_seconds,
            proxy_profile=proxy_profile,
            session_id=args.session_id,
            warnings=args.warning,
            limitations=args.limitation,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"source capture ig calls failed: {exc}\n")
    except Exception as exc:  # noqa: BLE001 - surface any failure visibly with a nonzero exit
        parser.exit(status=3, message=f"source capture ig calls failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0
    parser.exit(status=exit_code, message=f"source capture ig calls failed: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
