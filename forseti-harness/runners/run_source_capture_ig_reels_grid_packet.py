"""Optimized IG `/reels/` grid capture -> Source Capture Packet.

This supersedes the older IG calls runner as the default public creator-monitoring
path. It loads one public ``/<handle>/reels/`` grid, extracts no-hover DOM media
anchor engagement, preserves passive page-load JSON responses, joins metadata by
shortcode, and writes a Source Capture Packet. It does not visit item pages.

The older ``run_source_capture_ig_calls_packet.py`` remains a legacy calibration
or fallback route when item-page OG metadata is explicitly needed.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Sequence
from urllib.parse import urljoin, urlparse

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
)
from source_capture.ig_reels_grid import (
    IgReelsJoinedRow,
    IgReelsJsonCandidate,
    MEDIA_KIND_REEL,
    infer_pinned_shortcodes_by_recency,
    iter_json_media_candidates,
    join_dom_rows_with_json_candidates,
    normalize_dom_grid_rows,
)
from source_capture.ig_reels_grid_capture import (
    DEFAULT_IG_REELS_MAX_RESPONSE_BYTES,
    DEFAULT_IG_REELS_SETTLE_SECONDS,
    DEFAULT_IG_REELS_TIMEOUT_SECONDS,
    DEFAULT_IG_REELS_VIEWPORT_HEIGHT,
    DEFAULT_IG_REELS_VIEWPORT_WIDTH,
    IgReelsGridCaptureFailure,
    IgReelsGridCaptureResult,
    IgReelsGridCaptureSuccess,
    fetch_ig_reels_grid_capture,
)
from source_capture.models import CoverageWindow, MetricObservation, MetricPosture
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map
from source_capture.proxy_profiles import (
    ProxyCategory,
    ProxyProfile,
    load_proxy_profile,
    load_proxy_profile_by_label,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


IG_REELS_GRID_NON_CLAIMS = [
    "not content sufficiency proof",
    "not login or session capture",
    "not stored profile or cookie use",
    "not anti-detect behavior",
    "not proxy endpoint or credential disclosure",
    "not proxy exit IP disclosure",
    "not CAPTCHA solving",
    "not crawler or scheduled monitoring",
    "not item-page fan-out",
    "not comment text capture",
    "not full-history backfill",
    "not static/main-grid comparison capture",
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

DEFAULT_MAX_ROWS = 12
SOURCE_SURFACE = "ig_reels_grid_dom_passive_json"
SELECTION_POLICY_VERSION = "ig_reels_grid_capture_selection_v0"


def run_source_capture_ig_reels_grid_packet(
    *,
    handle: str | None = None,
    profile_url: str | None = None,
    output_directory: Path | None = None,
    data_root: object | None = None,
    decision_question: str,
    max_rows: int = DEFAULT_MAX_ROWS,
    timeout_seconds: float = DEFAULT_IG_REELS_TIMEOUT_SECONDS,
    settle_seconds: float = DEFAULT_IG_REELS_SETTLE_SECONDS,
    viewport_width: int = DEFAULT_IG_REELS_VIEWPORT_WIDTH,
    viewport_height: int = DEFAULT_IG_REELS_VIEWPORT_HEIGHT,
    max_response_bytes: int = DEFAULT_IG_REELS_MAX_RESPONSE_BYTES,
    block_heavy_assets: bool = True,
    proxy_profile: ProxyProfile | None = None,
    session_id: str | None = None,
    warnings: Sequence[str] = (),
    limitations: Sequence[str] = (),
    capture_fetcher: Callable[..., IgReelsGridCaptureResult] = fetch_ig_reels_grid_capture,
) -> tuple[int, str]:
    if (output_directory is None) == (data_root is None):
        raise ValueError("exactly one of output_directory or data_root is required")
    profile_handle, reels_url = _resolve_profile_input(handle=handle, profile_url=profile_url)

    capture = capture_fetcher(
        reels_url=reels_url,
        profile_handle=profile_handle,
        timeout_seconds=timeout_seconds,
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        settle_seconds=settle_seconds,
        max_response_bytes=max_response_bytes,
        max_rows=max_rows,
        block_heavy_assets=block_heavy_assets,
        proxy_profile=proxy_profile,
        storage_state_path=None,
        headless=True,
        browser_channel=None,
    )
    if isinstance(capture, IgReelsGridCaptureFailure):
        return 3, capture.message

    block_reason = _detect_ig_block(final_url=capture.final_url, title=capture.title, visible_text=capture.visible_text)
    if block_reason is not None:
        return 5, f"profile access-blocked ({block_reason}); no packet written"

    dom_rows = normalize_dom_grid_rows(
        capture.dom_rows,
        final_url=capture.final_url,
        profile_handle=profile_handle,
        max_rows=max_rows,
        allowed_kinds=(MEDIA_KIND_REEL,),
    )
    static_input_count = _static_post_row_count(capture.dom_rows)
    candidates, json_limitations = _json_candidates_from_passive_responses(capture)
    joined_rows = join_dom_rows_with_json_candidates(dom_rows, candidates)
    profile_snapshot = _profile_snapshot_from_passive_responses(
        capture=capture,
        profile_handle=profile_handle,
        reels_url=reels_url,
    )
    served_username = _string_or_none(profile_snapshot.get("served_username"))
    if served_username is None:
        return 5, (
            "subject_identity_unavailable: web_profile_info did not expose a served "
            "Instagram username; no packet written"
        )
    try:
        normalized_served_username = _normalize_handle(served_username)
    except ValueError:
        return 5, (
            "subject_identity_unavailable: web_profile_info exposed an invalid served "
            "Instagram username; no packet written"
        )
    if normalized_served_username.casefold() != profile_handle.casefold():
        return 5, (
            "subject_identity_mismatch: requested Instagram handle "
            f"{profile_handle!r} but web_profile_info served {served_username!r}; "
            "no packet written"
        )

    capture_timestamp = _string_or_none(capture.metadata.get("capture_timestamp"))
    capture_time_fact = (
        known_fact(capture_timestamp)
        if capture_timestamp is not None
        else unknown_with_reason("capture timestamp missing from browser capture metadata")
    )
    payload = {
        "capture_metadata": {
            **capture.metadata,
            "source_surface": SOURCE_SURFACE,
            "selection_policy_version": SELECTION_POLICY_VERSION,
        },
        "creator_profile_snapshot": profile_snapshot,
        "dom_rows": [row.to_dict() for row in dom_rows],
        "json_candidates": [candidate.to_dict() for candidate in candidates],
        "joined_rows": [row.to_dict() for row in joined_rows],
        "pinned_inference": _pinned_inference(joined_rows),
        "passive_json_responses": [response.to_dict() for response in capture.passive_json_responses],
        "warning_notes": list(capture.warning_notes),
        "limitation_notes": list(capture.limitation_notes) + json_limitations,
    }
    payload_bytes = f"{json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)}\n".encode("utf-8")
    staged_artifacts = [("ig_reels_grid_capture.json", payload_bytes)]
    file_ids = staged_file_id_map(staged_artifacts)
    preserved_file_ids = [file_ids["ig_reels_grid_capture.json"]]

    access = known_fact("ig_logged_out_reels_grid_browser_capture; public DOM and passive page-load JSON")
    archive = not_attempted("IG reels-grid runner does not query archive or history services")
    media = known_fact(
        "DOM media-anchor text and passive JSON metadata preserved; raw media bytes are out of scope"
    )
    recapture = not_applicable("no prior source capture packet was supplied for this IG reels-grid capture")

    def timing(publication_fact) -> PacketTiming:
        return PacketTiming(
            source_publication_or_event=publication_fact,
            source_edit_or_version=unknown_with_reason("IG reels-grid runner did not infer source edit/version timing"),
            capture_time=capture_time_fact,
            recapture_time=not_applicable("IG reels-grid packet does not model an earlier capture by default"),
            cutoff_posture=unknown_with_reason("IG reels-grid runner did not receive cutoff posture metadata"),
        )

    profile_timing = timing(unknown_with_reason("profile grid slice is the enumeration source, not a dated post"))
    source_slices: list[SourceCaptureSlice] = [
        SourceCaptureSlice(
            slice_id="ig_reels_profile_00",
            locator=known_fact(capture.final_url),
            timing=profile_timing,
            access_posture=access,
            archive_history_posture=archive,
            media_modality_posture=media,
            re_capture_relationship=recapture,
            limitations=[],
            warning_notes=[],
            preserved_file_ids=preserved_file_ids,
            metric_observations=_profile_metric_observations(
                profile_snapshot=profile_snapshot,
                capture_timestamp=capture_timestamp,
            ),
        )
    ]
    for index, joined in enumerate(joined_rows, start=1):
        best = _preferred_candidate(joined.source_surface_candidates)
        publication = (
            known_fact(best.taken_at_utc)
            if best is not None and best.taken_at_utc is not None
            else unknown_with_reason("no joined passive JSON timestamp for this grid row")
        )
        row_limitations: list[str] = []
        if not joined.source_surface_candidates:
            row_limitations.append("no_passive_json_join_for_shortcode")
        if joined.dom_row.parse_status != "parsed_no_hover_grid_engagement":
            row_limitations.append(f"dom_parse_status={joined.dom_row.parse_status}")
        source_slices.append(
            SourceCaptureSlice(
                slice_id=f"ig_reels_grid_{index:02d}",
                locator=known_fact(joined.dom_row.permalink_url),
                timing=timing(publication),
                access_posture=access,
                archive_history_posture=archive,
                media_modality_posture=media,
                re_capture_relationship=recapture,
                limitations=row_limitations,
                warning_notes=[],
                preserved_file_ids=preserved_file_ids,
                metric_observations=_media_metric_observations(
                    candidate=best,
                    capture_timestamp=capture_timestamp,
                ),
            )
        )

    run_warnings = list(warnings) + capture.warning_notes
    run_limitations = list(limitations) + capture.limitation_notes + json_limitations
    limited_media_slice_count = sum(
        1
        for source_slice in source_slices
        if source_slice.slice_id.startswith("ig_reels_grid_") and source_slice.limitations
    )
    if limited_media_slice_count:
        run_limitations.append(
            "media_slice_limitations_present: "
            f"{limited_media_slice_count} grid row(s) carried row-level limitations; "
            "inspect source_slices[].limitations"
        )
    if static_input_count:
        run_limitations.append(
            "static_profile_grid_rows_filtered: "
            f"{static_input_count} /p/ row(s) omitted from the reels traction series; "
            "use a separate static comparison source surface; static view_count is not_applicable"
        )
    if proxy_profile is not None:
        run_limitations.append(
            "proxy_profile_used: category="
            f"{proxy_profile.proxy_category.value}; endpoint, credentials, exit IP, and store path not recorded"
        )
    if block_heavy_assets:
        run_limitations.append(
            "heavy_asset_blocking_enabled: image/media/font requests aborted to reduce bandwidth; "
            "scripts and JSON/XHR left intact; content sufficiency not asserted"
        )
    if not dom_rows:
        run_limitations.append("zero_anchor_route_variant: no media anchors parsed from rendered reels grid")

    view_count_observed = _observed_metric_count(source_slices, "view_count")
    like_count_observed = _observed_metric_count(source_slices, "like_count")
    comment_count_observed = _observed_metric_count(source_slices, "comment_count")
    visible_mode_changes = [
        (
            "ig_reels_grid_no_item_fanout:"
            f"rows={len(dom_rows)}:json_candidates={len(candidates)}:passive_json={len(capture.passive_json_responses)}"
        ),
        (
            "ig_reels_grid_metrics:"
            f"views={view_count_observed}:likes={like_count_observed}:comments={comment_count_observed}"
        ),
    ]
    if block_heavy_assets:
        visible_mode_changes.append("ig_reels_grid_bandwidth_mode:block_heavy_assets")

    result = stage_and_write_packet(
        output_directory=output_directory,
        data_root=data_root,  # type: ignore[arg-type]
        staged_artifacts=staged_artifacts,
        source_slices=source_slices,
        source_family="instagram_creator",
        source_surface=SOURCE_SURFACE,
        source_locator=known_fact(reels_url),
        decision_question=decision_question,
        capture_context=(
            "logged-out IG public /reels/ grid capture; one page load; no hover/click/item-page fan-out; "
            "passive page-load JSON preserved when observed"
        ),
        actor_audience_context=known_fact(
            "public creator profile; logged-out capture; internal creator-monitoring calibration"
        ),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="ig_reels_grid_cli_operator",
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
        warnings=run_warnings,
        limitations=run_limitations,
        receipt_summary=(
            f"IG reels-grid packet for {reels_url}: {len(dom_rows)} DOM row(s), "
            f"{len(candidates)} passive JSON media candidate(s), "
            f"{view_count_observed} observed view_count metric(s); no item pages visited."
        ),
        receipt_non_claims=IG_REELS_GRID_NON_CLAIMS,
    )
    return 0, result.output_directory


def _resolve_profile_input(*, handle: str | None, profile_url: str | None) -> tuple[str, str]:
    if bool(handle) == bool(profile_url):
        raise ValueError("supply exactly one of --handle or --profile-url")
    if handle:
        normalized = _normalize_handle(handle)
        return normalized, f"https://www.instagram.com/{normalized}/reels/"

    assert profile_url is not None
    parsed = urlparse(profile_url)
    if parsed.scheme not in {"http", "https"} or parsed.netloc.lower() not in {
        "www.instagram.com",
        "instagram.com",
    }:
        raise ValueError("--profile-url must be an absolute instagram.com /<handle>/reels/ URL")
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2 or parts[1] != "reels":
        raise ValueError("--profile-url must point at /<handle>/reels/ for the optimized route")
    normalized = _normalize_handle(parts[0])
    return normalized, urljoin(f"https://www.instagram.com/{normalized}/", "reels/")


def _normalize_handle(handle: str) -> str:
    normalized = handle.strip().lstrip("@")
    if not normalized or "/" in normalized or "\\" in normalized:
        raise ValueError("IG handle must be a non-empty handle, not a path")
    return normalized


def _static_post_row_count(raw_rows: Sequence[dict[str, object]]) -> int:
    count = 0
    for raw in raw_rows:
        raw_path = _string_or_none(raw.get("path")) or _string_or_none(raw.get("href"))
        if raw_path is None:
            continue
        path = urlparse(raw_path).path or raw_path
        if "/p/" in path:
            count += 1
    return count

def _detect_ig_block(*, final_url: str, title: str | None, visible_text: str) -> str | None:
    final_low = final_url.lower()
    if "/accounts/login" in final_low:
        return "redirected_to_login"
    probe = f"{title or ''}\n{visible_text[:3000]}".lower()
    if "please wait a few minutes before you try again" in probe:
        return "rate_limited_429_interstitial"
    if "you've been blocked" in probe or "you have been blocked" in probe:
        return "network_security_block"
    if "challenge" in final_low or "/challenge/" in final_low:
        return "challenge_route"
    return None


def _json_candidates_from_passive_responses(
    capture: IgReelsGridCaptureSuccess,
) -> tuple[list[IgReelsJsonCandidate], list[str]]:
    candidates: list[IgReelsJsonCandidate] = []
    limitations: list[str] = []
    for response in capture.passive_json_responses:
        if not response.body_text:
            continue
        try:
            payload = json.loads(response.body_text)
        except json.JSONDecodeError as exc:
            limitations.append(f"{response.source_surface}_invalid_json: {exc}")
            continue
        candidates.extend(iter_json_media_candidates(payload, source_surface=response.source_surface))
    return candidates, limitations


def _profile_snapshot_from_passive_responses(
    *,
    capture: IgReelsGridCaptureSuccess,
    profile_handle: str,
    reels_url: str,
) -> dict[str, object]:
    snapshot: dict[str, object] = {
        "platform": "instagram",
        "source_profile": profile_handle,
        "served_username": None,
        "numeric_id": None,
        "capture_timestamp_utc": capture.metadata.get("capture_timestamp"),
        "capture_context_label": SOURCE_SURFACE,
        "profile_grid_url": reels_url,
        "final_url": capture.final_url,
        "display_name": None,
        "bio": None,
        "external_url": None,
        "bio_links_count": None,
        "bio_links": None,
        "profile_pic_url_present": None,
        "is_verified": None,
        "is_private": None,
        "category_name": None,
        "follower_count": None,
        "following_count": None,
        "post_or_media_count": None,
        "raw_profile_text_excerpt": capture.visible_text[:1000],
        "source_surfaces": sorted({response.source_surface for response in capture.passive_json_responses}),
        "parse_status": "raw_profile_visible_text_only",
        "limitations": [],
    }
    for response in capture.passive_json_responses:
        if response.source_surface != "web_profile_info_json_metadata" or not response.body_text:
            continue
        try:
            payload = json.loads(response.body_text)
        except json.JSONDecodeError:
            continue
        user = _profile_user(payload)
        if not isinstance(user, dict):
            continue
        snapshot.update(
            {
                "served_username": _string_or_none(user.get("username")),
                "numeric_id": _string_or_none(user.get("id")),
                "display_name": _string_or_none(user.get("full_name")),
                "bio": _string_or_none(user.get("biography")),
                "external_url": _string_or_none(user.get("external_url")),
                "bio_links_count": _list_count(user.get("bio_links")),
                "bio_links": _bio_links(user.get("bio_links")),
                "profile_pic_url_present": bool(user.get("profile_pic_url")),
                "is_verified": user.get("is_verified") if isinstance(user.get("is_verified"), bool) else None,
                "is_private": user.get("is_private") if isinstance(user.get("is_private"), bool) else None,
                "category_name": _string_or_none(user.get("category_name")),
                "follower_count": _edge_count(user.get("edge_followed_by")) or _int_or_none(user.get("follower_count")),
                "following_count": _edge_count(user.get("edge_follow")) or _int_or_none(user.get("following_count")),
                "post_or_media_count": _edge_count(user.get("edge_owner_to_timeline_media")),
                "parse_status": "parsed_web_profile_info_json_metadata",
            }
        )
        break
    return snapshot


def _profile_user(payload: object) -> dict[str, object] | None:
    if not isinstance(payload, dict):
        return None
    data = payload.get("data")
    if isinstance(data, dict) and isinstance(data.get("user"), dict):
        return data["user"]
    if isinstance(payload.get("user"), dict):
        return payload["user"]
    return None


def _bio_links(value: object) -> list[dict[str, object]] | None:
    """Capture the public link-in-bio destinations (title + url), not just a count.

    IG ``web_profile_info`` exposes ``bio_links`` as a list of public link objects;
    we preserve each link's title and destination URL (``url`` or ``lynx_url``).
    These are public profile fields -- no redaction. Returns None when the source
    did not expose a ``bio_links`` list at all (distinct from an empty list).
    """
    if not isinstance(value, list):
        return None
    links: list[dict[str, object]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        url = _string_or_none(item.get("url")) or _string_or_none(item.get("lynx_url"))
        title = _string_or_none(item.get("title"))
        if url is None and title is None:
            continue
        links.append({"title": title, "url": url})
    return links


def _profile_metric_observations(
    *,
    profile_snapshot: dict[str, object],
    capture_timestamp: str | None,
) -> list[MetricObservation]:
    observations: list[MetricObservation] = []
    follower_count = _int_or_none(profile_snapshot.get("follower_count"))
    if follower_count is not None:
        observations.append(_observed_metric("follower_count", follower_count, capture_timestamp=capture_timestamp))
    else:
        observations.append(
            _gap_metric(
                "follower_count",
                MetricPosture.UNAVAILABLE_WITH_REASON,
                "web_profile_info passive JSON did not yield exact follower_count",
                capture_timestamp=capture_timestamp,
            )
        )
    return observations


def _media_metric_observations(
    *,
    candidate: IgReelsJsonCandidate | None,
    capture_timestamp: str | None,
) -> list[MetricObservation]:
    observations: list[MetricObservation] = []
    if candidate is None:
        return [
            _gap_metric(
                "view_count",
                MetricPosture.UNAVAILABLE_WITH_REASON,
                "no joined passive JSON candidate for this shortcode",
                capture_timestamp=capture_timestamp,
            ),
            _gap_metric(
                "like_count",
                MetricPosture.UNAVAILABLE_WITH_REASON,
                "no joined passive JSON candidate for this shortcode",
                capture_timestamp=capture_timestamp,
            ),
            _gap_metric(
                "comment_count",
                MetricPosture.UNAVAILABLE_WITH_REASON,
                "no joined passive JSON candidate for this shortcode",
                capture_timestamp=capture_timestamp,
            ),
        ]
    if candidate.video_or_play_count is not None:
        observations.append(_observed_metric("view_count", candidate.video_or_play_count, capture_timestamp=capture_timestamp))
    elif candidate.is_video is False:
        observations.append(
            _gap_metric(
                "view_count",
                MetricPosture.NOT_APPLICABLE,
                "joined passive JSON marks this media as non-video/static",
                capture_timestamp=capture_timestamp,
            )
        )
    else:
        observations.append(
            _gap_metric(
                "view_count",
                MetricPosture.UNAVAILABLE_WITH_REASON,
                "joined passive JSON did not yield a video/play count",
                capture_timestamp=capture_timestamp,
            )
        )
    if candidate.like_count is not None:
        observations.append(_observed_metric("like_count", candidate.like_count, capture_timestamp=capture_timestamp))
    else:
        observations.append(
            _gap_metric(
                "like_count",
                MetricPosture.UNAVAILABLE_WITH_REASON,
                "joined passive JSON did not yield like_count",
                capture_timestamp=capture_timestamp,
            )
        )
    if candidate.comment_count is not None:
        observations.append(_observed_metric("comment_count", candidate.comment_count, capture_timestamp=capture_timestamp))
    else:
        observations.append(
            _gap_metric(
                "comment_count",
                MetricPosture.UNAVAILABLE_WITH_REASON,
                "joined passive JSON did not yield comment_count",
                capture_timestamp=capture_timestamp,
            )
        )
    return observations


def _preferred_candidate(candidates: Sequence[IgReelsJsonCandidate]) -> IgReelsJsonCandidate | None:
    if not candidates:
        return None
    preference = {
        "clips_user_json_metadata": 0,
        "web_profile_info_json_metadata": 1,
        "profile_feed_json_metadata": 2,
    }
    return sorted(candidates, key=lambda item: preference.get(item.source_surface, 99))[0]


def _pinned_inference(joined_rows: Sequence[IgReelsJoinedRow]) -> dict[str, object]:
    """Two independent reels-tab pinned signals over the reels grid, surfaced for
    cross-check rather than as a correctness assertion: the explicit
    ``pinned_on_clips_tab`` JSON flag vs the grid-order recency-inversion
    heuristic. Both are scoped to the reels grid only -- main-grid/timeline pins
    (``pinned_on_timeline``, which leak in via ``web_profile_info``) are a
    different surface and stay out of this summary, visible per-candidate instead.
    The two can legitimately differ: inversion is blind to a pinned *newest* reel,
    so ``recency_matches_explicit`` only reports whether they agreed this capture;
    downstream decides which to trust."""
    grid_rows: list[tuple[str, int | None]] = []
    explicit: set[str] = set()
    for joined in joined_rows:
        shortcode = joined.dom_row.shortcode or ""
        taken_at = next(
            (
                candidate.taken_at_timestamp
                for candidate in joined.source_surface_candidates
                if candidate.taken_at_timestamp is not None
            ),
            None,
        )
        grid_rows.append((shortcode, taken_at))
        if any(candidate.pinned_on_clips_tab for candidate in joined.source_surface_candidates):
            explicit.add(shortcode)
    inferred = list(infer_pinned_shortcodes_by_recency(grid_rows))
    explicit_sorted = sorted(explicit)
    return {
        "reels_tab_inferred_pinned_by_recency": inferred,
        "reels_tab_explicit_pinned_shortcodes": explicit_sorted,
        "recency_matches_explicit": sorted(inferred) == explicit_sorted,
    }


def _observed_metric(metric: str, value: int, *, capture_timestamp: str | None) -> MetricObservation:
    return MetricObservation(
        metric=metric,
        posture=MetricPosture.OBSERVED,
        value=value,
        coverage_window=_metric_coverage_window(capture_timestamp),
    )


def _gap_metric(
    metric: str,
    posture: MetricPosture,
    reason: str,
    *,
    capture_timestamp: str | None,
) -> MetricObservation:
    return MetricObservation(
        metric=metric,
        posture=posture,
        reason=reason,
        coverage_window=_metric_coverage_window(capture_timestamp),
    )


def _metric_coverage_window(capture_timestamp: str | None) -> CoverageWindow | None:
    if capture_timestamp is None:
        return None
    return CoverageWindow(end=capture_timestamp)


def _observed_metric_count(slices: Sequence[SourceCaptureSlice], metric: str) -> int:
    return sum(
        1
        for source_slice in slices
        for observation in source_slice.metric_observations
        if observation.metric == metric and observation.posture == MetricPosture.OBSERVED
    )


def _edge_count(value: object) -> int | None:
    if isinstance(value, dict):
        return _int_or_none(value.get("count"))
    return None


def _list_count(value: object) -> int | None:
    if isinstance(value, list):
        return len(value)
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
        return int(stripped) if stripped.isdigit() else None
    return None


def _string_or_none(value: object) -> str | None:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    if isinstance(value, int):
        return str(value)
    return None


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Capture one IG creator's public /reels/ grid into a Source Capture Packet "
            "(optimized default: no hover/click/item-page fan-out)."
        )
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--handle", default=None, help="IG handle, with or without @.")
    input_group.add_argument("--profile-url", default=None, help="Absolute instagram.com/<handle>/reels/ URL.")
    parser.add_argument("--decision-question", required=True)
    target_group = parser.add_mutually_exclusive_group(required=False)
    target_group.add_argument("--output", type=Path, default=None)
    target_group.add_argument(
        "--data-root",
        default=None,
        help="Commit into the Forseti data lake at this root; explicit --data-root is mutually exclusive with --output. FORSETI_DATA_ROOT is used only when --output is omitted; legacy ORCA_DATA_ROOT is also accepted.",
    )
    parser.add_argument("--max-rows", type=int, default=DEFAULT_MAX_ROWS)
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_IG_REELS_TIMEOUT_SECONDS)
    parser.add_argument("--settle-seconds", type=float, default=DEFAULT_IG_REELS_SETTLE_SECONDS)
    parser.add_argument("--viewport-width", type=int, default=DEFAULT_IG_REELS_VIEWPORT_WIDTH)
    parser.add_argument("--viewport-height", type=int, default=DEFAULT_IG_REELS_VIEWPORT_HEIGHT)
    parser.add_argument("--max-response-bytes", type=int, default=DEFAULT_IG_REELS_MAX_RESPONSE_BYTES)
    parser.add_argument(
        "--allow-heavy-assets",
        action="store_true",
        help="Do not abort image/media/font requests. Default blocks them to reduce bandwidth.",
    )
    proxy_group = parser.add_argument_group(
        "proxy profile",
        "Optional label-indirected proxy use. Endpoint and credentials stay in the local secret store; packets record category-only provenance.",
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
        data_root = None
        data_root_requested = args.data_root is not None or (args.output is None and (os.environ.get("FORSETI_DATA_ROOT") or os.environ.get("ORCA_DATA_ROOT")))
        if args.output is not None and args.data_root is not None:
            parser.exit(
                status=2,
                message=(
                    "source capture ig reels-grid failed: exactly one of --output or "
                    "--data-root/FORSETI_DATA_ROOT/ORCA_DATA_ROOT is required\n"
                ),
            )
        if args.output is None and not data_root_requested:
            parser.exit(
                status=2,
                message=(
                    "source capture ig reels-grid failed: exactly one of --output or "
                    "--data-root/FORSETI_DATA_ROOT/ORCA_DATA_ROOT is required\n"
                ),
            )
        if data_root_requested:
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)
        exit_code, message = run_source_capture_ig_reels_grid_packet(
            handle=args.handle,
            profile_url=args.profile_url,
            output_directory=args.output if data_root is None else None,
            data_root=data_root,
            decision_question=args.decision_question,
            max_rows=args.max_rows,
            timeout_seconds=args.timeout_seconds,
            settle_seconds=args.settle_seconds,
            viewport_width=args.viewport_width,
            viewport_height=args.viewport_height,
            max_response_bytes=args.max_response_bytes,
            block_heavy_assets=not args.allow_heavy_assets,
            proxy_profile=proxy_profile,
            session_id=args.session_id,
            warnings=args.warning,
            limitations=args.limitation,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"source capture ig reels-grid failed: {exc}\n")
    except Exception as exc:  # noqa: BLE001 - surface any failure visibly with a nonzero exit
        parser.exit(status=3, message=f"source capture ig reels-grid failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0
    parser.exit(status=exit_code, message=f"source capture ig reels-grid failed: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
