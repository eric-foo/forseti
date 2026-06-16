"""Bounded IG wind-caller CALLS capture -> Source Capture Packet.

Composes existing primitives (no login automation, no secrets):
- browser_snapshot (headless; scroll to enumerate the profile grid),
- ig_calls_parse (og:description -> caption/likes/comments/date/#ad; permalinks),
- browser-context XHR (web_profile_info + bounded grid pagination -> view counts),
- cadence.bounded_jitter (human-mimicking variable gaps between item visits),
- writer.write_local_source_capture_packet (one packet: profile slice + N call slices).

Substrate basis: the recon + 2026-06-14 headless probe found IG serves the call
signal (caption + engagement) in the post/reel page og:description to a browser,
logged-out. The runner can optionally load an operator-supplied browser
storage-state JSON for the bounded live assumption gate; it never performs
login or credential capture itself.

Bounded by the wind-caller carve-out: attended, human-mimicking cadence, no
standing/scheduled crawler, per-run item cap. This is one bounded capture unit
(one named account's recent calls), launched by an operator; there is no
scheduler entrypoint.
"""
from __future__ import annotations

import argparse
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
    DEFAULT_VIEWPORT_HEIGHT,
    DEFAULT_VIEWPORT_WIDTH,
)
from source_capture.cadence import build_cadence_plan
from source_capture.ig_momentum_harvest import (
    IG_ID_CONFLICT_POLICY_VERSION,
    IG_METRIC_REGISTRY_VERSION,
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

IG_CALLS_NON_CLAIMS = [
    "not content sufficiency proof",
    "not login automation or credential capture",
    "not storage-state generation or credential persistence",
    "not anti-detect behavior",
    "not proxy or session injection",
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


def _capture_one(url: str, *, scroll_passes: int, timeout_seconds: float, viewport_width: int,
                 viewport_height: int, max_artifact_bytes: int, storage_state_path: Path | None):
    return fetch_browser_snapshot_capture(
        url=url,
        timeout_seconds=timeout_seconds,
        wait_until="load",
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        max_artifact_bytes=max_artifact_bytes,
        scroll_passes=scroll_passes,
        storage_state_path=storage_state_path,
    )


def _profile_handle_from_url(profile_url: str) -> str | None:
    path_parts = [part for part in urlparse(profile_url).path.split("/") if part]
    return path_parts[0] if path_parts else None


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
    elif record.get("status") == "captured":
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
    elif record.get("status") == "captured":
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

    status = str(record.get("status", "unknown"))
    if status != "captured":
        observations.append(
            _gap_metric(
                "view_count",
                MetricPosture.UNAVAILABLE_WITH_REASON,
                f"item status={status}; view_count not attributed because the item did not produce a captured call signal",
                capture_timestamp=capture_timestamp,
            )
        )
        return observations

    shortcode = extract_ig_shortcode(str(record.get("url", "")))
    media = momentum_capture.media_by_shortcode.get(shortcode) if momentum_capture and shortcode else None
    if media is None:
        reason = "browser-context profile-feed JSON did not include this shortcode"
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
    viewport_width: int = DEFAULT_VIEWPORT_WIDTH,
    viewport_height: int = DEFAULT_VIEWPORT_HEIGHT,
    max_artifact_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
    capture_view_counts: bool = True,
    view_count_max_graphql_pages: int = DEFAULT_VIEW_COUNT_MAX_GRAPHQL_PAGES,
    xhr_request_gap_seconds: float = DEFAULT_XHR_REQUEST_GAP_SECONDS,
    storage_state_path: Path | None = None,
    capture_context: str = (
        "IG wind-caller calls capture; logged-out by default with optional operator-supplied browser storage state; "
        "one bounded account, recent calls"
    ),
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
    if storage_state_path is not None and not storage_state_path.is_file():
        raise ValueError("browser storage state file does not exist")

    profile = _capture_one(
        profile_url, scroll_passes=profile_scroll_passes, timeout_seconds=timeout_seconds,
        viewport_width=viewport_width, viewport_height=viewport_height, max_artifact_bytes=max_artifact_bytes,
        storage_state_path=storage_state_path,
    )
    if isinstance(profile, BrowserSnapshotFailure):
        return 3, f"profile capture failed: {profile.message}"
    block = _detect_ig_block(
        final_url=profile.final_url, title=profile.title,
        visible_text=profile.visible_text, rendered_dom=profile.rendered_dom,
    )
    if block is not None:
        return 3, f"profile access-blocked ({block}); recorded NO-GO, no packet written"

    permalinks = extract_item_permalinks(
        profile.rendered_dom,
        profile_handle=_profile_handle_from_url(profile.final_url or profile.requested_url),
    )[:max_items]
    if not permalinks:
        return 3, "no /p/ or /reel/ permalinks enumerated from the profile grid"

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
            storage_state_path=storage_state_path,
            sleep_fn=sleep_fn,
        )
        if permalinks:
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
        item = _capture_one(
            url, scroll_passes=0, timeout_seconds=timeout_seconds, viewport_width=viewport_width,
            viewport_height=viewport_height, max_artifact_bytes=max_artifact_bytes,
            storage_state_path=storage_state_path,
        )
        if isinstance(item, BrowserSnapshotFailure):
            item_records.append({"url": url, "status": "capture_failed", "message": item.message})
            continue
        item_block = _detect_ig_block(
            final_url=item.final_url, title=item.title,
            visible_text=item.visible_text, rendered_dom=item.rendered_dom,
        )
        if item_block is not None:
            item_records.append({"url": item.final_url, "status": "access_blocked", "block_reason": item_block})
            continue
        og = extract_meta_content(item.rendered_dom, "og:description")
        if not og:
            item_records.append({"url": item.final_url, "status": "no_signal",
                                 "message": "no og:description on item page"})
            continue
        parsed = parse_ig_og_description(og)
        if not _has_captured_call_signal(parsed):
            item_records.append({
                "url": item.final_url,
                "status": "partial_signal",
                "message": (
                    "og:description did not contain the minimum call signal "
                    "(caption, date, and at least one engagement count)"
                ),
                "caption": parsed.caption,
                "likes": parsed.likes,
                "comments": parsed.comments,
                "date": parsed.date,
                "is_ad": parsed.is_ad,
                "caption_truncated": parsed.truncated,
                "raw_og": parsed.raw_og,
            })
            continue
        item_records.append({
            "url": item.final_url,
            "status": "captured",
            "caption": parsed.caption,
            "likes": parsed.likes,
            "comments": parsed.comments,
            "date": parsed.date,
            "is_ad": parsed.is_ad,
            "caption_truncated": parsed.truncated,
            "raw_og": parsed.raw_og,
        })

    return _write_packet(
        profile_url=profile.requested_url,
        profile_final_url=profile.final_url,
        profile_stats=profile_stats,
        permalink_count=len(permalinks),
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
        storage_state_loaded=storage_state_path is not None,
    )


def _slice_postures():
    access = known_fact(
        "ig_browser_snapshot; public og:description; optional operator-supplied browser storage state; content sufficiency not asserted"
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
    storage_state_loaded: bool,
) -> tuple[int, str]:
    access, archive, media, recapture = _slice_postures()
    staging_parent = output_directory.parent
    staging_parent.mkdir(parents=True, exist_ok=True)

    captured_count = sum(1 for r in item_records if r["status"] == "captured")
    stats_dict = (
        {"followers": profile_stats.followers, "following": profile_stats.following, "posts": profile_stats.posts}
        if profile_stats is not None
        else None
    )
    profile_payload = {
        "profile_url": profile_final_url,
        "stats": stats_dict,
        "permalinks_enumerated": permalink_count,
        "cadence_plan": cadence_summary,
        "browser_storage_state_loaded": storage_state_loaded,
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
            publication = known_fact(date) if date else unknown_with_reason(
                f"item {record['status']}: no post date parsed"
            )
            slice_limitations: list[str] = []
            if record["status"] != "captured":
                slice_limitations.append(f"item_not_captured: {record['status']}")
            elif record.get("caption_truncated"):
                slice_limitations.append(
                    "caption_truncated_in_og: long caption may be cut at IG's og cap; rendered caption DOM not yet captured"
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
        if captured_count < len(item_records):
            run_limitations.append(
                f"partial_capture: {captured_count}/{len(item_records)} items yielded a call signal"
            )
        view_count_observed = sum(
            1
            for source_slice in slices
            for observation in source_slice.metric_observations
            if observation.metric == "view_count" and observation.posture == MetricPosture.OBSERVED
        )
        capture_mode_token = (
            "ig_calls_operator_storage_state_capture" if storage_state_loaded else "ig_calls_logged_out_capture"
        )
        visible_mode_changes = [
            f"{capture_mode_token}:items={len(item_records)}:captured={captured_count}",
            f"ig_browser_context_view_count_capture:observed={view_count_observed}",
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
                "public-figure creator public profile; logged-out by default or operator-supplied browser storage state; internal wind-caller calibration"
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
                "enumerated items yielded a browser-visible call signal (caption + engagement); "
                f"{view_count_observed} item(s) yielded observed view_count."
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
        description=(
            "Capture one IG creator's recent CALLS into a Source Capture Packet "
            "(logged-out by default; optional operator-supplied browser storage state)."
        )
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
    parser.add_argument("--browser-storage-state", type=Path, default=None)
    parser.add_argument("--session-id", default=None)
    parser.add_argument("--warning", action="append", default=[])
    parser.add_argument("--limitation", action="append", default=[])
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
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
            storage_state_path=args.browser_storage_state,
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
