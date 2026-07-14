"""Supervised one-creator TikTok onboarding orchestration.

This module composes existing session-profile, page-observation, grid-selection,
and live-batch deep-capture substrate. It is deliberately bounded to one creator
and one caller-visible browser lease; it is not a scanner, scheduler, registry
writer, or CAPTCHA solver.
"""
from __future__ import annotations

import json
import random
import re
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from typing import Any, Callable, Sequence
from urllib.parse import urlparse

from source_capture.adapters.browser_snapshot import (
    BrowserPageObservationEngine,
    BrowserPageObservationSuccess,
    BrowserPagePointerAction,
    BrowserPageResponse,
    BrowserPageWheelAction,
    BrowserSnapshotFailure,
    ChromeCdpPageObservationSessionEngine,
    fetch_browser_page_observation_capture,
)
from source_capture.auth_state import validate_auth_state_provenance_requirement
from source_capture.browser_user_data import browser_user_data_path_for_label
from source_capture.session_profiles import SourceCaptureSessionProfile
from source_capture.tiktok.admission import (
    assert_no_sensitive_tiktok_material,
    json_dumps_sanitized,
)
from source_capture.tiktok.grid_video_selection import build_tiktok_grid_video_selection
from source_capture.tiktok.live_batch_probe import (
    TIKTOK_ACCOUNT_SAFETY_STOP_MARKERS,
    TIKTOK_BROWSER_BACKEND_CHROME_CDP,
    TIKTOK_SUPERVISED_DEFAULT_CADENCE_MAX_GAP_SECONDS,
    TIKTOK_SUPERVISED_DEFAULT_CADENCE_MIN_GAP_SECONDS,
    TIKTOK_CHALLENGE_TEXT_MARKERS,
    TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
    TIKTOK_LIVE_BATCH_CADENCE_JSON_NAME,
    TIKTOK_LIVE_BATCH_GRID_JSON_NAME,
    TIKTOK_VIDEO_DOM_EXTRACT_SCRIPT,
    is_tiktok_comment_list_url,
    run_tiktok_live_batch_probe,
)


TIKTOK_CREATOR_ONBOARDING_SCHEMA_VERSION = "tiktok_creator_onboarding_v0"
TIKTOK_ONBOARDING_SUGGESTED_JSON_NAME = "tiktok_suggested_accounts_attempt.json"
TIKTOK_ONBOARDING_GRID_WINDOW_JSON_NAME = "tiktok_grid_window.json"
TIKTOK_ONBOARDING_SELECTION_JSON_NAME = "tiktok_grid_video_selection.json"
TIKTOK_ONBOARDING_RECEIPT_JSON_NAME = "tiktok_creator_onboarding_receipt.json"
DEFAULT_WINDOW_SIZE = 30
DEFAULT_SELECTION_COUNT = 8
DEFAULT_MAX_GRID_SCROLL_PASSES = 40
INITIAL_DEEP_CAPTURE_WAIT_MIN_SECONDS = 8.0
INITIAL_DEEP_CAPTURE_WAIT_MAX_SECONDS = 13.0
GRID_ENTRY_RETRY_WAIT_SECONDS = 60.0

SleepFn = Callable[[float], None]
MonotonicFn = Callable[[], float]
UtcNowFn = Callable[[], datetime]

TIKTOK_PROFILE_GRID_DOM_EXTRACT_SCRIPT = r"""
(arg) => {
  const creator = String((arg && arg.creator_handle) || '')
    .trim()
    .replace(/^@/, '')
    .toLowerCase();
  const seen = new Set();
  const videos = [];
  for (const anchor of Array.from(document.querySelectorAll('a[href*="/video/"]'))) {
    const href = String(anchor.href || anchor.getAttribute('href') || '');
    const match = href.match(/\/@([^/]+)\/video\/(\d+)/);
    if (
      !creator ||
      !match ||
      match[1].toLowerCase() !== creator ||
      seen.has(match[2])
    ) continue;
    seen.add(match[2]);
    let container = anchor;
    let pinnedVisible = false;
    for (let depth = 0; container && depth < 5; depth += 1) {
      const text = String(container.innerText || container.textContent || '').toLowerCase();
      if (text.includes('pinned') || container.querySelector('[data-e2e*="pinned"]')) {
        pinnedVisible = true;
        break;
      }
      container = container.parentElement;
    }
    const style = window.getComputedStyle(anchor);
    const box = anchor.getBoundingClientRect();
    const intersectsViewport = box.bottom > 0 && box.right > 0 &&
      box.top < window.innerHeight && box.left < window.innerWidth;
    const visibleInViewport = style.visibility !== 'hidden' && style.display !== 'none' &&
      box.width > 0 && box.height > 0 && intersectsViewport;
    videos.push({
      video_id: match[2],
      video_url: href,
      pinned_visible: pinnedVisible,
      visible_in_viewport: visibleInViewport,
      grid_position: videos.length + 1
    });
  }
  const hydration = document.querySelector('#__UNIVERSAL_DATA_FOR_REHYDRATION__');
  return {
    ordered_videos: videos,
    hydration_json_text: hydration ? hydration.textContent : null
  };
}
""".strip()

TIKTOK_SUGGESTED_ACCOUNTS_DOM_EXTRACT_SCRIPT = r"""
(arg) => {
  const creator = String((arg && arg.creator_handle) || '').toLowerCase();
  const visible = (node) => {
    if (!node) return false;
    const style = window.getComputedStyle(node);
    const box = node.getBoundingClientRect();
    return style.visibility !== 'hidden' && style.display !== 'none' && box.width > 0 && box.height > 0;
  };
  const profileAnchors = (root) => Array.from(
    root.querySelectorAll('a[href^="/@"],a[href*="tiktok.com/@"]')
  );
  const exactSuggestedNodes = Array.from(document.querySelectorAll('body *')).filter((node) =>
    visible(node) && String(node.innerText || node.textContent || '').trim().toLowerCase() === 'suggested'
  );
  let dialog = null;
  let suggestedTab = null;
  for (const node of exactSuggestedNodes) {
    let current = node;
    while (current && current !== document.body) {
      const text = String(current.innerText || current.textContent || '').toLowerCase();
      if (text.includes('following') && text.includes('followers') && text.includes('suggested') && profileAnchors(current).length > 0) {
        dialog = current;
        suggestedTab = node;
        break;
      }
      current = current.parentElement;
    }
    if (dialog) break;
  }
  const rows = [];
  const seen = new Set();
  let suggestedProfileAnchorCount = dialog ? profileAnchors(dialog).length : 0;
  if (dialog) {
    const anchors = profileAnchors(dialog);
    for (const anchor of anchors) {
      const href = String(anchor.href || anchor.getAttribute('href') || '');
      const match = href.match(/\/@([^/?#]+)/);
      if (!match) continue;
      const handle = match[1].toLowerCase();
      if (!handle || handle === creator || seen.has(handle)) continue;
      seen.add(handle);
      rows.push({
        handle,
        profile_url: 'https://www.tiktok.com/@' + handle,
        display_text_or_none: String(anchor.innerText || anchor.textContent || '').trim() || null
      });
    }
  }
  const externalLinks = [];
  const seenExternal = new Set();
  for (const anchor of Array.from(document.querySelectorAll('a[href]'))) {
    try {
      const url = new URL(String(anchor.href || anchor.getAttribute('href') || ''), location.href);
      const host = String(url.hostname || '').toLowerCase();
      if (!['http:', 'https:'].includes(url.protocol) || !host || host === 'tiktok.com' || host.endsWith('.tiktok.com')) continue;
      const cleanUrl = url.origin + url.pathname;
      if (seenExternal.has(cleanUrl)) continue;
      seenExternal.add(cleanUrl);
      externalLinks.push({
        url: cleanUrl,
        host,
        display_text_or_none: String(anchor.innerText || anchor.textContent || '').trim() || null
      });
    } catch (_error) {
      continue;
    }
  }
  return {
    suggested_accounts: rows,
    profile_external_links: externalLinks,
    suggested_surface_detected: Boolean(dialog && suggestedTab),
    suggested_surface_root_count: dialog && suggestedTab ? 1 : 0,
    suggested_profile_anchor_count: suggestedProfileAnchorCount,
    relationship_dialog_detected: Boolean(dialog),
    suggested_tab_detected: Boolean(suggestedTab),
    suggested_route: 'followers_dialog_suggested_tab'
  };
}
""".strip()

TIKTOK_VISIBLE_SELECTED_GRID_TILES_DOM_EXTRACT_SCRIPT = r"""
(arg) => {
  const creator = String((arg && arg.creator_handle) || '').trim().replace(/^@/, '').toLowerCase();
  const selected = new Set(Array.isArray(arg && arg.selected_video_ids)
    ? arg.selected_video_ids.map((value) => String(value))
    : []);
  const seen = new Set();
  const rows = [];
  const visibleGridPositions = [];
  let gridPosition = 0;
  for (const anchor of Array.from(document.querySelectorAll('a[href*="/video/"]'))) {
    const href = String(anchor.href || anchor.getAttribute('href') || '');
    const match = href.match(/\/@([^/]+)\/video\/(\d+)/);
    if (!match || match[1].toLowerCase() !== creator || seen.has(match[2])) continue;
    seen.add(match[2]);
    gridPosition += 1;
    const style = window.getComputedStyle(anchor);
    const box = anchor.getBoundingClientRect();
    const intersectsViewport = box.bottom > 0 && box.right > 0 &&
      box.top < window.innerHeight && box.left < window.innerWidth;
    const visible = style.visibility !== 'hidden' && style.display !== 'none' &&
      box.width > 0 && box.height > 0 && intersectsViewport;
    if (!visible) continue;
    visibleGridPositions.push(gridPosition);
    if (!selected.has(match[2])) continue;
    rows.push({
      video_id: match[2],
      video_url: href,
      grid_position: gridPosition,
      bounding_box: {x: box.x, y: box.y, width: box.width, height: box.height}
    });
  }
  return {
    visible_selected_tiles: rows,
    selected_video_count: selected.size,
    tile_scroll_performed: false,
    visible_grid_position_min_or_none: visibleGridPositions.length
      ? Math.min(...visibleGridPositions) : null,
    visible_grid_position_max_or_none: visibleGridPositions.length
      ? Math.max(...visibleGridPositions) : null,
    scroll_y: Math.max(0, Math.round(window.scrollY || 0)),
    viewport_height: Math.max(0, Math.round(window.innerHeight || 0)),
    document_height: Math.max(0, Math.round(document.documentElement.scrollHeight || 0))
  };
}
""".strip()

TIKTOK_FOLLOWERS_ACTION = BrowserPagePointerAction(
    action_name="tiktok_creator_followers_count_v0",
    candidate_selector=(
        "[data-e2e*='followers'],a[href*='/followers'],button,[role='button'],"
        "[role='link']"
    ),
    text_markers=("followers",),
    wait_after_ms=1500,
    prefer_smallest_match=True,
)

TIKTOK_RELATIONSHIP_SUGGESTED_TAB_ACTION = BrowserPagePointerAction(
    action_name="tiktok_relationship_dialog_suggested_tab_v0",
    candidate_selector="[role='dialog'] *,[aria-modal='true'] *",
    text_markers=(),
    exact_text_markers=("suggested",),
    wait_after_ms=2000,
    prefer_smallest_match=True,
)

TIKTOK_SUGGESTED_ACCOUNTS_FALLBACK_DOM_EXTRACT_SCRIPT = r"""
(arg) => {
  const creator = String((arg && arg.creator_handle) || '').toLowerCase();
  const profileAnchors = (root) => Array.from(
    root.querySelectorAll('a[href^="/@"],a[href*="tiktok.com/@"]')
  );
  const roots = [];
  const addSuggestedRoot = (node) => {
    let current = node;
    while (current && current !== document.body) {
      if (
        String(current.innerText || current.textContent || '').toLowerCase().includes('suggested accounts') &&
        profileAnchors(current).length > 0
      ) {
        if (!roots.includes(current)) roots.push(current);
        return;
      }
      current = current.parentElement;
    }
  };
  for (const node of Array.from(document.querySelectorAll('body *'))) {
    if (String(node.innerText || node.textContent || '').trim().toLowerCase() === 'suggested accounts') addSuggestedRoot(node);
  }
  for (const node of Array.from(document.querySelectorAll('[data-e2e*="suggest"]'))) addSuggestedRoot(node);
  const rows = [];
  const seen = new Set();
  let suggestedProfileAnchorCount = 0;
  for (const root of roots) {
    const anchors = profileAnchors(root);
    suggestedProfileAnchorCount += anchors.length;
    for (const anchor of anchors) {
      const href = String(anchor.href || anchor.getAttribute('href') || '');
      const match = href.match(/\/@([^/?#]+)/);
      if (!match) continue;
      const handle = match[1].toLowerCase();
      if (!handle || handle === creator || seen.has(handle)) continue;
      seen.add(handle);
      rows.push({
        handle,
        profile_url: 'https://www.tiktok.com/@' + handle,
        display_text_or_none: String(anchor.innerText || anchor.textContent || '').trim() || null
      });
    }
  }
  return {
    suggested_accounts: rows,
    profile_external_links: [],
    suggested_surface_detected: roots.length > 0,
    suggested_surface_root_count: roots.length,
    suggested_profile_anchor_count: suggestedProfileAnchorCount,
    relationship_dialog_detected: false,
    suggested_tab_detected: false,
    suggested_route: 'profile_suggested_accounts_view_all_fallback'
  };
}
""".strip()

TIKTOK_SUGGESTED_VIEW_ALL_ACTION = BrowserPagePointerAction(
    action_name="tiktok_suggested_accounts_view_all_v0",
    candidate_selector="[aria-label='View All'],button,[role='button'],a",
    text_markers=("view all",),
    exact_text_markers=("view all",),
    page_text_markers=("suggested accounts",),
    wait_after_ms=2000,
    prefer_smallest_match=True,
)

TIKTOK_RELATIONSHIP_DIALOG_CLOSE_ACTION = BrowserPagePointerAction(
    action_name="tiktok_relationship_dialog_close_v0",
    candidate_selector=(
        "[role='dialog'] button,[role='dialog'] [role='button'],"
        "[role='dialog'] svg"
    ),
    text_markers=(),
    exact_text_markers=("close", "x", "×"),
    page_text_markers=("followers", "suggested"),
    wait_after_ms=1500,
    prefer_top_right=True,
    visual_top_right_x_fallback=True,
    visual_x_target_zone="center_modal",
    visual_x_geometric_fallback=False,
)

TIKTOK_VIDEO_OVERLAY_CLOSE_ACTION = BrowserPagePointerAction(
    action_name="tiktok_grid_video_overlay_close_v0",
    candidate_selector=(
        "button[aria-label*='close' i],[role='button'][aria-label*='close' i],"
        "[data-e2e*='close'],button,[role='button']"
    ),
    text_markers=(),
    exact_text_markers=("close", "x", "×"),
    page_text_markers=("comments", "creator videos"),
    wait_after_ms=1500,
    prefer_smallest_match=True,
)


class TikTokCreatorOnboardingError(RuntimeError):
    """Raised when supervised onboarding cannot produce trustworthy completion."""


@dataclass(frozen=True)
class TikTokCreatorOnboardingOutputPaths:
    suggested_accounts_json_path: Path
    grid_window_json_path: Path
    selection_json_path: Path
    live_grid_json_path: Path
    live_cadence_json_path: Path
    onboarding_receipt_json_path: Path


DeepCaptureFn = Callable[..., dict[str, Any]]
ProgressFn = Callable[[str, dict[str, object]], None]


def _utc_now() -> datetime:
    return datetime.now(UTC)


def run_tiktok_creator_onboarding(
    *,
    creator_handle: str,
    session_profile: SourceCaptureSessionProfile,
    output_dir: Path,
    auth_state_root: Path | None = None,
    browser_user_data_root: Path | None = None,
    window_size: int = DEFAULT_WINDOW_SIZE,
    selection_count: int = DEFAULT_SELECTION_COUNT,
    timeout_seconds: float = 30.0,
    settle_seconds: float = 2.0,
    max_grid_scroll_passes: int = DEFAULT_MAX_GRID_SCROLL_PASSES,
    cadence_min_gap_seconds: float = TIKTOK_SUPERVISED_DEFAULT_CADENCE_MIN_GAP_SECONDS,
    cadence_max_gap_seconds: float = TIKTOK_SUPERVISED_DEFAULT_CADENCE_MAX_GAP_SECONDS,
    cadence_window_seconds: float | None = None,
    random_seed: int | None = None,
    engine: BrowserPageObservationEngine | None = None,
    progress_fn: ProgressFn | None = None,
    deep_capture_fn: DeepCaptureFn = run_tiktok_live_batch_probe,
    sleep_fn: SleepFn = time.sleep,
    monotonic_fn: MonotonicFn = time.monotonic,
    utc_now_fn: UtcNowFn = _utc_now,
) -> TikTokCreatorOnboardingOutputPaths:
    """Run suggested -> grid -> select -> deep-capture in one browser context."""

    normalized_handle = _normalize_handle(creator_handle)
    run_started_monotonic = monotonic_fn()
    phase_chronology = [
        _phase_chronology_row(
            "onboarding_started",
            run_started_monotonic=run_started_monotonic,
            monotonic_fn=monotonic_fn,
            utc_now_fn=utc_now_fn,
        )
    ]
    if session_profile.platform != "tiktok":
        raise TikTokCreatorOnboardingError("session profile platform must be tiktok")
    if session_profile.browser_backend != TIKTOK_BROWSER_BACKEND_CHROME_CDP:
        raise TikTokCreatorOnboardingError("TikTok onboarding requires Chrome CDP")
    if isinstance(window_size, bool) or not isinstance(window_size, int) or window_size <= 0:
        raise TikTokCreatorOnboardingError("window_size must be a positive integer")
    if (
        isinstance(selection_count, bool)
        or not isinstance(selection_count, int)
        or selection_count <= 0
        or selection_count > window_size
    ):
        raise TikTokCreatorOnboardingError("selection_count must be between 1 and window_size")
    if (
        isinstance(max_grid_scroll_passes, bool)
        or not isinstance(max_grid_scroll_passes, int)
        or max_grid_scroll_passes <= 0
    ):
        raise TikTokCreatorOnboardingError(
            "max_grid_scroll_passes must be a positive integer"
        )

    storage_state_path = validate_auth_state_provenance_requirement(
        session_profile.state_label,
        session_mode=session_profile.session_mode,
        required_harness_proxy_profile_posture=(
            session_profile.required_harness_proxy_profile_posture
        ),
        auth_state_root=auth_state_root,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = _output_paths(output_dir)
    profile_url = f"https://www.tiktok.com/@{normalized_handle}"
    owned_engine = engine is None
    if engine is None:
        if session_profile.browser_user_data_label is None:
            raise TikTokCreatorOnboardingError(
                "TikTok onboarding requires a retained browser_user_data_label"
            )
        user_data_dir = browser_user_data_path_for_label(
            session_profile.browser_user_data_label,
            user_data_root=browser_user_data_root,
        )
        if not user_data_dir.is_dir() or not any(user_data_dir.iterdir()):
            raise TikTokCreatorOnboardingError(
                "retained browser profile is missing or empty; bootstrap it manually before onboarding"
            )
        observation_engine = ChromeCdpPageObservationSessionEngine(
            pre_action_stop_markers=TIKTOK_ACCOUNT_SAFETY_STOP_MARKERS,
            human_challenge_handoff_markers=TIKTOK_CHALLENGE_TEXT_MARKERS,
            human_challenge_handoff_timeout_seconds=180.0,
            human_challenge_handoff_prompt=TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
        )
    else:
        observation_engine = engine

    stage = "acquire_session"
    status = "failed"
    error: str | None = None
    close_error: str | None = None
    selected_video_ids: list[str] = []
    challenge_count = 0
    human_challenge_handoff_count = 0
    completed_count = 0
    account_safety_stop = False
    suggested_status: str | None = None
    suggested_outer_ui_route: str | None = None
    initial_deep_capture_wait: dict[str, object] | None = None
    grid_deep_entry: dict[str, object] | None = None
    artifacts_written: list[str] = []
    try:
        stage = "collect_suggested_accounts"
        _notify_progress(progress_fn, stage)
        suggested_capture = _capture_suggested_accounts(
            profile_url=profile_url,
            creator_handle=normalized_handle,
            storage_state_path=storage_state_path,
            timeout_seconds=timeout_seconds,
            settle_seconds=settle_seconds,
            engine=observation_engine,
        )
        suggested_receipt = _build_suggested_accounts_receipt(
            creator_handle=normalized_handle,
            capture=suggested_capture,
        )
        suggested_status = str(suggested_receipt["status"])
        suggested_outer_ui_route = str(suggested_receipt["outer_ui_route"])
        _write_json(paths.suggested_accounts_json_path, suggested_receipt)
        artifacts_written.append(paths.suggested_accounts_json_path.name)
        if suggested_status == "failed":
            raise TikTokCreatorOnboardingError("suggested-account observation failed")

        stage = "collect_grid"
        _notify_progress(progress_fn, stage)
        grid_capture = capture_tiktok_creator_grid(
            profile_url=profile_url,
            creator_handle=normalized_handle,
            storage_state_path=storage_state_path,
            window_size=window_size,
            timeout_seconds=timeout_seconds,
            settle_seconds=settle_seconds,
            max_grid_scroll_passes=max_grid_scroll_passes,
            engine=observation_engine,
        )
        if isinstance(grid_capture, BrowserSnapshotFailure):
            raise TikTokCreatorOnboardingError(
                f"grid capture failed: {grid_capture.failure_kind.value}"
            )

        stage = "freeze_window"
        _notify_progress(progress_fn, stage)
        grid_window = build_tiktok_grid_window(
            creator_handle=normalized_handle,
            capture=grid_capture,
            window_size=window_size,
            minimum_window_size=selection_count,
        )
        _write_json(paths.grid_window_json_path, grid_window)
        artifacts_written.append(paths.grid_window_json_path.name)

        stage = "select"
        _notify_progress(progress_fn, stage)
        selection = build_tiktok_grid_video_selection(
            grid_window["items"],
            expected_item_count=len(grid_window["items"]),
            selection_count=selection_count,
        )
        selection["onboarding_binding"] = {
            "creator_handle": normalized_handle,
            "grid_window_file": paths.grid_window_json_path.name,
            "grid_window_sha256": _sha256_path(paths.grid_window_json_path),
        }
        _write_json(paths.selection_json_path, selection)
        artifacts_written.append(paths.selection_json_path.name)

        window_by_id = {
            str(item["video_id"]): item for item in grid_window["items"]
        }
        selected_video_ids = list(
            selection["selection_summary"][
                "selected_video_ids_in_review_priority_order"
            ]
        )
        phase_chronology.append(
            _phase_chronology_row(
                "grid_and_selection_complete",
                run_started_monotonic=run_started_monotonic,
                monotonic_fn=monotonic_fn,
                utc_now_fn=utc_now_fn,
            )
        )
        run_rng = (
            random.Random(random_seed)
            if random_seed is not None
            else random.SystemRandom()
        )
        planned_wait_seconds = run_rng.uniform(
            INITIAL_DEEP_CAPTURE_WAIT_MIN_SECONDS,
            INITIAL_DEEP_CAPTURE_WAIT_MAX_SECONDS,
        )
        wait_observed_at_utc = _utc_iso(utc_now_fn())
        wait_started_monotonic = monotonic_fn()
        sleep_fn(planned_wait_seconds)
        wait_finished_monotonic = monotonic_fn()
        initial_deep_capture_wait = {
            "policy": "randomized_wait_after_grid_before_first_deep_capture",
            "minimum_seconds": INITIAL_DEEP_CAPTURE_WAIT_MIN_SECONDS,
            "maximum_seconds": INITIAL_DEEP_CAPTURE_WAIT_MAX_SECONDS,
            "planned_seconds": round(planned_wait_seconds, 6),
            "actual_seconds": round(
                max(0.0, wait_finished_monotonic - wait_started_monotonic), 6
            ),
            "observed_at_utc": wait_observed_at_utc,
        }
        phase_chronology.append(
            _phase_chronology_row(
                "first_deep_capture_released",
                run_started_monotonic=run_started_monotonic,
                monotonic_fn=monotonic_fn,
                utc_now_fn=utc_now_fn,
            )
        )

        stage = "enter_grid_overlay_capture_sequence"
        _notify_progress(progress_fn, stage, selected_count=len(selected_video_ids))
        grid_deep_entry = {
            "policy": "all_selected_via_visible_grid_tile_overlay_with_bounded_pagination",
            "deep_capture_route": "grid_tile_overlay",
            "direct_video_navigation_count": 0,
            "targeted_tile_scroll_performed": False,
            "grid_pagination_allowed": True,
            "grid_pagination_input_method": "mouse_wheel_burst",
            "logical_grid_positions_remembered": True,
            "absolute_pixel_positions_cached": False,
            "thumbnail_click_safe_inset_fraction": 0.15,
            "grid_pagination_pass_cap_per_lookup": max_grid_scroll_passes,
            "grid_pagination_total_pass_cap": (
                max_grid_scroll_passes * len(selected_video_ids)
            ),
            "grid_pagination_passes_executed": 0,
            "grid_pagination_passes": [],
            "attempts": [],
            "retry_waits": [],
            "status": "in_progress",
        }
        selected_urls = [
            str(window_by_id[video_id]["video_url"])
            for video_id in selected_video_ids
        ]
        overlay_capture_sequence = _GridOverlayCaptureSequence(
            profile_url=profile_url,
            creator_handle=normalized_handle,
            selected_video_ids=selected_video_ids,
            window_by_id=window_by_id,
            storage_state_path=storage_state_path,
            timeout_seconds=timeout_seconds,
            settle_seconds=settle_seconds,
            pagination_pass_cap=max_grid_scroll_passes,
            engine=observation_engine,
            rng=run_rng,
            sleep_fn=sleep_fn,
            monotonic_fn=monotonic_fn,
            utc_now_fn=utc_now_fn,
            receipt=grid_deep_entry,
        )

        stage = "deep_capture"
        _notify_progress(progress_fn, stage, selected_count=len(selected_video_ids))
        deep_capture = deep_capture_fn(
            creator_handle=normalized_handle,
            creator_profile_url=profile_url,
            video_urls=selected_urls,
            state_label=session_profile.state_label,
            session_mode=session_profile.session_mode,
            logged_out=False,
            auth_state_root=auth_state_root,
            timeout_seconds=timeout_seconds,
            settle_seconds=settle_seconds,
            browser_backend=session_profile.browser_backend,
            required_harness_proxy_profile_posture=(
                session_profile.required_harness_proxy_profile_posture
            ),
            human_challenge_handoff=True,
            cadence_min_gap_seconds=cadence_min_gap_seconds,
            cadence_max_gap_seconds=cadence_max_gap_seconds,
            cadence_window_seconds=cadence_window_seconds,
            random_seed=random_seed,
            engine=observation_engine,
            capture_route="grid_tile_overlay",
            page_capture_sequence_fn=overlay_capture_sequence,
            grid_candidates_by_video_id=window_by_id,
        )
        captured_video_ids = [
            str(row["video_id"])
            for row in deep_capture["cadence_result"].get("results", [])
            if isinstance(row, dict) and row.get("video_id")
        ]
        if grid_deep_entry.get("status") == "complete":
            phase_chronology.append(
                _phase_chronology_row(
                    "grid_overlay_deep_capture_sequence_completed",
                    run_started_monotonic=run_started_monotonic,
                    monotonic_fn=monotonic_fn,
                    utc_now_fn=utc_now_fn,
                )
            )
        _write_json(paths.live_grid_json_path, deep_capture["grid_result"])
        artifacts_written.append(paths.live_grid_json_path.name)
        _write_json(paths.live_cadence_json_path, deep_capture["cadence_result"])
        artifacts_written.append(paths.live_cadence_json_path.name)
        challenge_count = int(
            deep_capture["cadence_result"].get("challenge_count", 0)
        )
        human_challenge_handoff_count = int(
            deep_capture["cadence_result"].get(
                "human_challenge_handoff_count", 0
            )
        )
        completed_count = int(deep_capture["cadence_result"]["completed_count"])
        account_safety_stop = _has_account_safety_stop(
            deep_capture["cadence_result"]
        )
        status = (
            "complete"
            if completed_count == len(selected_video_ids)
            else "partial_failure"
        )
        if status != "complete":
            if account_safety_stop:
                raise TikTokCreatorOnboardingError("account_safety_stop")
            raise TikTokCreatorOnboardingError(
                "one or more selected video deep captures did not complete"
            )
        phase_chronology.append(
            _phase_chronology_row(
                "deep_capture_completed",
                run_started_monotonic=run_started_monotonic,
                monotonic_fn=monotonic_fn,
                utc_now_fn=utc_now_fn,
            )
        )
        stage = "close"
        _notify_progress(progress_fn, stage, completed_count=completed_count)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        if owned_engine:
            close = getattr(observation_engine, "close", None)
            if callable(close):
                try:
                    close()
                except Exception as exc:
                    close_error = f"{type(exc).__name__}: {exc}"
                    error = f"{error}; close failed: {close_error}" if error else f"close failed: {close_error}"
                    status = "failed"
                    stage = "close"
        lifecycle_receipt = getattr(observation_engine, "lifecycle_receipt", None)
        receipt = {
            "schema_version": TIKTOK_CREATOR_ONBOARDING_SCHEMA_VERSION,
            "status": status,
            "terminal_stage": stage,
            "creator_handle": normalized_handle,
            "session_profile": session_profile.alias,
            "window_size": len(grid_window["items"]) if "grid_window" in locals() else 0,
            "window_cap": window_size,
            "selection_count": selection_count,
            "suggested_accounts_status_or_none": suggested_status,
            "suggested_outer_ui_route_or_none": suggested_outer_ui_route,
            "candidate_profiles_opened": 0,
            "account_mutations_taken": 0,
            "selected_video_ids_in_capture_order": (
                captured_video_ids
                if "captured_video_ids" in locals()
                else selected_video_ids
            ),
            "selected_count": len(selected_video_ids),
            "challenge_count": challenge_count,
            "human_challenge_handoff_count": human_challenge_handoff_count,
            "account_safety_stop": account_safety_stop,
            "completed_deep_capture_count": completed_count,
            "initial_deep_capture_wait_or_none": initial_deep_capture_wait,
            "grid_deep_entry_or_none": grid_deep_entry,
            "phase_chronology": phase_chronology,
            "artifacts_written": artifacts_written,
            "browser_lifecycle": (
                lifecycle_receipt
                if isinstance(lifecycle_receipt, dict)
                else {
                    "engine": type(observation_engine).__name__,
                    "owned_by_onboarding_runner": owned_engine,
                    "closed_or_none": True if owned_engine else None,
                }
            ),
            "error_or_none": error,
            "non_claims": [
                "not a standing scanner or crawler",
                "not Creator Registry mutation",
                "not an exhaustive suggested-account graph",
                "not paid or organic distribution classification",
            ],
        }
        _write_json(paths.onboarding_receipt_json_path, receipt)

    if close_error is not None:
        raise TikTokCreatorOnboardingError(f"browser session close failed: {close_error}")
    return paths


def _capture_suggested_accounts(
    *,
    profile_url: str,
    creator_handle: str,
    storage_state_path: Path,
    timeout_seconds: float,
    settle_seconds: float,
    engine: BrowserPageObservationEngine,
) -> BrowserPageObservationSuccess | BrowserSnapshotFailure:
    primary = fetch_browser_page_observation_capture(
        url=profile_url,
        dom_extract_script=TIKTOK_SUGGESTED_ACCOUNTS_DOM_EXTRACT_SCRIPT,
        dom_extract_arg={"creator_handle": creator_handle},
        response_url_predicate=lambda _: False,
        post_load_pointer_actions=(
            TIKTOK_FOLLOWERS_ACTION,
            TIKTOK_RELATIONSHIP_SUGGESTED_TAB_ACTION,
        ),
        timeout_seconds=timeout_seconds,
        wait_until="domcontentloaded",
        settle_seconds=settle_seconds,
        storage_state_path=storage_state_path,
        headless=False,
        browser_backend=TIKTOK_BROWSER_BACKEND_CHROME_CDP,
        human_challenge_handoff_markers=TIKTOK_CHALLENGE_TEXT_MARKERS,
        human_challenge_handoff_timeout_seconds=180.0,
        human_challenge_handoff_prompt=TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
        engine=engine,
    )
    if isinstance(primary, BrowserSnapshotFailure):
        return primary
    primary_dom = primary.dom_observation
    if (
        isinstance(primary_dom, dict)
        and primary_dom.get("relationship_dialog_detected") is True
        and primary_dom.get("suggested_tab_detected") is True
    ):
        primary.metadata["suggested_outer_ui_route"] = (
            "followers_dialog_suggested_tab_primary"
        )
        primary.metadata["suggested_primary_pointer_actions"] = primary.metadata.get(
            "post_load_pointer_actions"
        )
        primary.metadata["suggested_fallback_pointer_actions"] = []
        return primary

    fallback = fetch_browser_page_observation_capture(
        url=profile_url,
        dom_extract_script=TIKTOK_SUGGESTED_ACCOUNTS_FALLBACK_DOM_EXTRACT_SCRIPT,
        dom_extract_arg={"creator_handle": creator_handle},
        response_url_predicate=lambda _: False,
        post_load_pointer_actions=(
            TIKTOK_RELATIONSHIP_DIALOG_CLOSE_ACTION,
            TIKTOK_SUGGESTED_VIEW_ALL_ACTION,
        ),
        timeout_seconds=timeout_seconds,
        wait_until="domcontentloaded",
        settle_seconds=settle_seconds,
        storage_state_path=storage_state_path,
        headless=False,
        browser_backend=TIKTOK_BROWSER_BACKEND_CHROME_CDP,
        human_challenge_handoff_markers=TIKTOK_CHALLENGE_TEXT_MARKERS,
        human_challenge_handoff_timeout_seconds=180.0,
        human_challenge_handoff_prompt=TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
        engine=engine,
    )
    if isinstance(fallback, BrowserPageObservationSuccess):
        if isinstance(fallback.dom_observation, dict) and isinstance(
            primary.dom_observation, dict
        ):
            fallback.dom_observation["profile_external_links"] = (
                primary.dom_observation.get("profile_external_links", [])
            )
        fallback.metadata["suggested_outer_ui_route"] = (
            "profile_suggested_accounts_view_all_fallback"
        )
        fallback.metadata["suggested_primary_pointer_actions"] = primary.metadata.get(
            "post_load_pointer_actions"
        )
        fallback.metadata["suggested_fallback_pointer_actions"] = fallback.metadata.get(
            "post_load_pointer_actions"
        )
    return fallback


class _GridOverlayCaptureSequence:
    """Choose every deep capture from visible selected tiles on one grid page."""

    def __init__(
        self,
        *,
        profile_url: str,
        creator_handle: str,
        selected_video_ids: Sequence[str],
        window_by_id: dict[str, dict[str, Any]],
        storage_state_path: Path,
        timeout_seconds: float,
        settle_seconds: float,
        pagination_pass_cap: int,
        engine: BrowserPageObservationEngine,
        rng: Any,
        sleep_fn: SleepFn,
        monotonic_fn: MonotonicFn,
        utc_now_fn: UtcNowFn,
        receipt: dict[str, object],
    ) -> None:
        self.profile_url = profile_url
        self.creator_handle = creator_handle
        self.selected_video_ids = tuple(selected_video_ids)
        self.window_by_id = window_by_id
        self.storage_state_path = storage_state_path
        self.timeout_seconds = timeout_seconds
        self.settle_seconds = settle_seconds
        self.pagination_pass_cap = pagination_pass_cap
        self.engine = engine
        self.rng = rng
        self.sleep_fn = sleep_fn
        self.monotonic_fn = monotonic_fn
        self.utc_now_fn = utc_now_fn
        self.receipt = receipt
        self.current_overlay_url: str | None = None
        self.capture_order: list[str] = []
        self.last_grid_view: dict[str, object] = {}

    def __call__(
        self, index: int, pending_video_urls: Sequence[str]
    ) -> tuple[str, BrowserPageObservationSuccess | BrowserSnapshotFailure]:
        pending_by_id = {
            _video_id_from_url(url): url for url in pending_video_urls
        }
        if not pending_by_id or not set(pending_by_id).issubset(self.selected_video_ids):
            raise TikTokCreatorOnboardingError(
                "overlay capture sequence received an invalid pending selection"
            )
        if self.current_overlay_url is not None:
            self._close_current_overlay(tuple(pending_by_id))

        visible_rows = self._visible_rows(tuple(pending_by_id))
        if not visible_rows:
            visible_rows = self._paginate_until_visible(tuple(pending_by_id))
        if not visible_rows:
            self.receipt["status"] = "failed"
            raise TikTokCreatorOnboardingError(
                "bounded grid pagination exhausted before a selected tile became visible"
            )

        for retry_number in (0, 1):
            if not visible_rows:
                break
            chosen = self.rng.choice(visible_rows)
            chosen_video_id = str(chosen["video_id"])
            chosen_url = pending_by_id[chosen_video_id]
            click_capture = _click_visible_selected_grid_tile(
                profile_url=self.profile_url,
                creator_handle=self.creator_handle,
                selected_video_ids=tuple(pending_by_id),
                chosen_video_id=chosen_video_id,
                storage_state_path=self.storage_state_path,
                timeout_seconds=self.timeout_seconds,
                settle_seconds=self.settle_seconds,
                engine=self.engine,
            )
            attempt_receipt = self._click_attempt_receipt(
                index=index,
                retry_number=retry_number,
                chosen=chosen,
                visible_rows=visible_rows,
                capture=click_capture,
            )
            attempts = self.receipt["attempts"]
            assert isinstance(attempts, list)
            attempts.append(attempt_receipt)
            if (
                isinstance(click_capture, BrowserPageObservationSuccess)
                and attempt_receipt["outcome"] == "overlay_ready"
            ):
                self.current_overlay_url = click_capture.final_url
                self.capture_order.append(chosen_video_id)
                self.receipt["capture_order_policy"] = (
                    "random_among_visible_selected_then_bounded_grid_pagination"
                )
                self.receipt["selected_video_ids_in_capture_order"] = list(
                    self.capture_order
                )
                self.receipt["status"] = (
                    "complete"
                    if len(self.capture_order) == len(self.selected_video_ids)
                    else "in_progress"
                )
                return chosen_url, click_capture

            if retry_number == 0:
                retry_started = self.monotonic_fn()
                observed_at = _utc_iso(self.utc_now_fn())
                self.sleep_fn(GRID_ENTRY_RETRY_WAIT_SECONDS)
                retry_waits = self.receipt["retry_waits"]
                assert isinstance(retry_waits, list)
                retry_waits.append(
                    {
                        "video_attempt_index": index,
                        "planned_seconds": GRID_ENTRY_RETRY_WAIT_SECONDS,
                        "actual_seconds": round(
                            max(0.0, self.monotonic_fn() - retry_started), 6
                        ),
                        "observed_at_utc": observed_at,
                    }
                )
                if (
                    isinstance(click_capture, BrowserPageObservationSuccess)
                    and _is_any_creator_video_url(
                        click_capture.final_url, self.creator_handle
                    )
                ):
                    self.current_overlay_url = click_capture.final_url
                    self._close_current_overlay(tuple(pending_by_id))
                visible_rows = self._visible_rows(tuple(pending_by_id))
                if not visible_rows:
                    visible_rows = self._paginate_until_visible(
                        tuple(pending_by_id)
                    )

        self.receipt["status"] = "failed"
        raise TikTokCreatorOnboardingError(
            "grid tile did not materialize a matching overlay after one 60-second retry"
        )

    def _visible_rows(self, pending_video_ids: Sequence[str]) -> list[dict[str, Any]]:
        capture = _capture_visible_selected_grid_tiles(
            profile_url=self.profile_url,
            creator_handle=self.creator_handle,
            selected_video_ids=pending_video_ids,
            storage_state_path=self.storage_state_path,
            timeout_seconds=self.timeout_seconds,
            settle_seconds=self.settle_seconds,
            engine=self.engine,
        )
        if isinstance(capture, BrowserSnapshotFailure):
            return []
        self._remember_grid_view(capture)
        return _visible_grid_rows_from_capture(capture)

    def _paginate_until_visible(
        self, pending_video_ids: Sequence[str]
    ) -> list[dict[str, Any]]:
        for lookup_pass_number in range(1, self.pagination_pass_cap + 1):
            total_pass_number = int(
                self.receipt["grid_pagination_passes_executed"]
            ) + 1
            direction = self._pagination_direction(pending_video_ids)
            capture = _capture_visible_selected_grid_tiles(
                profile_url=self.profile_url,
                creator_handle=self.creator_handle,
                selected_video_ids=pending_video_ids,
                storage_state_path=self.storage_state_path,
                timeout_seconds=self.timeout_seconds,
                settle_seconds=self.settle_seconds,
                engine=self.engine,
                pagination_direction=direction,
            )
            self.receipt["grid_pagination_passes_executed"] = total_pass_number
            pagination_passes = self.receipt["grid_pagination_passes"]
            assert isinstance(pagination_passes, list)
            pass_receipt: dict[str, object] = {
                "lookup_pass_number": lookup_pass_number,
                "total_pass_number": total_pass_number,
                "direction": direction,
                "wheel_action_or_none": None,
            }
            if isinstance(capture, BrowserSnapshotFailure):
                pass_receipt["outcome"] = f"capture_failed:{capture.failure_kind.value}"
                pagination_passes.append(pass_receipt)
                continue
            self._remember_grid_view(capture)
            pass_receipt["wheel_action_or_none"] = capture.metadata.get(
                "post_load_wheel_action"
            )
            pass_receipt["visible_grid_position_min_or_none"] = (
                self.last_grid_view.get("visible_grid_position_min_or_none")
            )
            pass_receipt["visible_grid_position_max_or_none"] = (
                self.last_grid_view.get("visible_grid_position_max_or_none")
            )
            rows = _visible_grid_rows_from_capture(capture)
            pass_receipt["outcome"] = (
                "selected_tile_visible" if rows else "no_selected_tile_visible"
            )
            pagination_passes.append(pass_receipt)
            if rows:
                return rows
        return []

    def _remember_grid_view(self, capture: BrowserPageObservationSuccess) -> None:
        observation = capture.dom_observation
        self.last_grid_view = {
            "visible_grid_position_min_or_none": observation.get(
                "visible_grid_position_min_or_none"
            ),
            "visible_grid_position_max_or_none": observation.get(
                "visible_grid_position_max_or_none"
            ),
            "scroll_y": observation.get("scroll_y"),
        }

    def _pagination_direction(self, pending_video_ids: Sequence[str]) -> str:
        pending_positions = [
            int(self.window_by_id[video_id]["grid_position"])
            for video_id in pending_video_ids
            if video_id in self.window_by_id
            and self.window_by_id[video_id].get("grid_position") is not None
        ]
        visible_min = self.last_grid_view.get("visible_grid_position_min_or_none")
        visible_max = self.last_grid_view.get("visible_grid_position_max_or_none")
        if pending_positions and isinstance(visible_min, (int, float)) and isinstance(
            visible_max, (int, float)
        ):
            above = [position for position in pending_positions if position < visible_min]
            below = [position for position in pending_positions if position > visible_max]
            if above and below:
                up_gap = visible_min - max(above)
                down_gap = min(below) - visible_max
                return "up" if up_gap <= down_gap else "down"
            if above:
                return "up"
            if below:
                return "down"
        return "up" if float(self.last_grid_view.get("scroll_y") or 0) > 0 else "down"

    def _close_current_overlay(self, pending_video_ids: Sequence[str]) -> None:
        assert self.current_overlay_url is not None
        capture = fetch_browser_page_observation_capture(
            url=self.current_overlay_url,
            dom_extract_script=TIKTOK_VISIBLE_SELECTED_GRID_TILES_DOM_EXTRACT_SCRIPT,
            dom_extract_arg={
                "creator_handle": self.creator_handle,
                "selected_video_ids": list(pending_video_ids),
            },
            response_url_predicate=lambda _: False,
            post_load_pointer_actions=(TIKTOK_VIDEO_OVERLAY_CLOSE_ACTION,),
            timeout_seconds=self.timeout_seconds,
            wait_until="domcontentloaded",
            settle_seconds=self.settle_seconds,
            storage_state_path=self.storage_state_path,
            headless=False,
            browser_backend=TIKTOK_BROWSER_BACKEND_CHROME_CDP,
            human_challenge_handoff_markers=TIKTOK_CHALLENGE_TEXT_MARKERS,
            human_challenge_handoff_timeout_seconds=180.0,
            human_challenge_handoff_prompt=TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
            engine=self.engine,
        )
        action = _first_pointer_action_receipt(capture)
        if (
            isinstance(capture, BrowserSnapshotFailure)
            or not isinstance(action, dict)
            or action.get("clicked") is not True
            or not _is_creator_profile_url(capture.final_url, self.creator_handle)
        ):
            self.receipt["status"] = "failed"
            raise TikTokCreatorOnboardingError(
                "video overlay close did not return to the creator grid"
            )
        self.current_overlay_url = None

    def _click_attempt_receipt(
        self,
        *,
        index: int,
        retry_number: int,
        chosen: dict[str, Any],
        visible_rows: Sequence[dict[str, Any]],
        capture: BrowserPageObservationSuccess | BrowserSnapshotFailure,
    ) -> dict[str, object]:
        chosen_video_id = str(chosen["video_id"])
        action = _first_pointer_action_receipt(capture)
        overlay_ready = (
            isinstance(capture, BrowserPageObservationSuccess)
            and isinstance(action, dict)
            and action.get("clicked") is True
            and _overlay_capture_ready(
                capture,
                creator_handle=self.creator_handle,
                video_id=chosen_video_id,
            )
        )
        return {
            "video_attempt_index": index,
            "retry_number": retry_number,
            "observed_at_utc": _utc_iso(self.utc_now_fn()),
            "visible_selected_video_ids": [
                str(row["video_id"]) for row in visible_rows
            ],
            "chosen_video_id": chosen_video_id,
            "chosen_grid_position": chosen.get("grid_position"),
            "click_action_or_none": action,
            "final_url_or_none": (
                capture.final_url
                if isinstance(capture, BrowserPageObservationSuccess)
                else None
            ),
            "overlay_ready": overlay_ready,
            "item_struct_required": False,
            "outcome": (
                "overlay_ready"
                if overlay_ready
                else f"click_capture_failed:{capture.failure_kind.value}"
                if isinstance(capture, BrowserSnapshotFailure)
                else "overlay_not_ready_or_identity_mismatch"
            ),
        }


def _capture_visible_selected_grid_tiles(
    *,
    profile_url: str,
    creator_handle: str,
    selected_video_ids: Sequence[str],
    storage_state_path: Path,
    timeout_seconds: float,
    settle_seconds: float,
    engine: BrowserPageObservationEngine,
    pagination_direction: str | None = None,
) -> BrowserPageObservationSuccess | BrowserSnapshotFailure:
    if pagination_direction not in {None, "up", "down"}:
        raise ValueError("pagination_direction must be up, down, or None")
    return fetch_browser_page_observation_capture(
        url=profile_url,
        dom_extract_script=TIKTOK_VISIBLE_SELECTED_GRID_TILES_DOM_EXTRACT_SCRIPT,
        dom_extract_arg={
            "creator_handle": creator_handle,
            "selected_video_ids": list(selected_video_ids),
        },
        response_url_predicate=lambda _: False,
        post_load_wheel_action=(
            BrowserPageWheelAction(
                action_name="tiktok_grid_mouse_wheel_pagination_v0",
                direction=pagination_direction,
            )
            if pagination_direction is not None
            else None
        ),
        timeout_seconds=timeout_seconds,
        wait_until="domcontentloaded",
        settle_seconds=settle_seconds,
        storage_state_path=storage_state_path,
        headless=False,
        browser_backend=TIKTOK_BROWSER_BACKEND_CHROME_CDP,
        human_challenge_handoff_markers=TIKTOK_CHALLENGE_TEXT_MARKERS,
        human_challenge_handoff_timeout_seconds=180.0,
        human_challenge_handoff_prompt=TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
        engine=engine,
    )


def _click_visible_selected_grid_tile(
    *,
    profile_url: str,
    creator_handle: str,
    selected_video_ids: Sequence[str],
    chosen_video_id: str,
    storage_state_path: Path,
    timeout_seconds: float,
    settle_seconds: float,
    engine: BrowserPageObservationEngine,
) -> BrowserPageObservationSuccess | BrowserSnapshotFailure:
    action = BrowserPagePointerAction(
        action_name="tiktok_visible_selected_grid_video_v0",
        candidate_selector=f"a[href*='/video/{chosen_video_id}']",
        text_markers=(chosen_video_id,),
        wait_after_ms=2500,
        prefer_smallest_match=True,
        target_fraction_min=0.15,
        target_fraction_max=0.85,
    )
    return fetch_browser_page_observation_capture(
        url=profile_url,
        dom_extract_script=TIKTOK_VIDEO_DOM_EXTRACT_SCRIPT,
        dom_extract_arg=None,
        response_url_predicate=is_tiktok_comment_list_url,
        post_load_pointer_actions=(action,),
        timeout_seconds=timeout_seconds,
        wait_until="domcontentloaded",
        settle_seconds=settle_seconds,
        storage_state_path=storage_state_path,
        headless=False,
        browser_backend=TIKTOK_BROWSER_BACKEND_CHROME_CDP,
        human_challenge_handoff_markers=TIKTOK_CHALLENGE_TEXT_MARKERS,
        human_challenge_handoff_timeout_seconds=180.0,
        human_challenge_handoff_prompt=TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
        engine=engine,
    )


def _first_pointer_action_receipt(
    capture: BrowserPageObservationSuccess | BrowserSnapshotFailure,
) -> dict[str, Any] | None:
    if isinstance(capture, BrowserSnapshotFailure):
        return None
    actions = capture.metadata.get("post_load_pointer_actions")
    if not isinstance(actions, list) or not actions or not isinstance(actions[0], dict):
        return None
    return actions[0]


def _overlay_capture_ready(
    capture: BrowserPageObservationSuccess,
    *,
    creator_handle: str,
    video_id: str,
) -> bool:
    dom = capture.dom_observation
    if not isinstance(dom, dict):
        return False
    observed_creator = str(dom.get("overlay_creator_handle_or_none") or "").lstrip("@").lower()
    return bool(
        dom.get("video_overlay_detected") is True
        and _non_negative_int_or_zero(dom.get("visible_video_element_count")) > 0
        and str(dom.get("overlay_video_id_or_none") or "") == video_id
        and (not observed_creator or observed_creator == creator_handle.lower())
        and _is_creator_video_url(
            video_url=capture.final_url,
            creator_handle=creator_handle,
            video_id=video_id,
        )
    )


def _video_id_from_url(video_url: str) -> str:
    match = re.match(r"^/@[^/]+/video/(\d+)$", urlparse(video_url).path.rstrip("/"))
    if match is None:
        raise TikTokCreatorOnboardingError("selected video URL has invalid TikTok path")
    return match.group(1)


def _is_any_creator_video_url(video_url: str, creator_handle: str) -> bool:
    try:
        video_id = _video_id_from_url(video_url)
    except TikTokCreatorOnboardingError:
        return False
    return _is_creator_video_url(
        video_url=video_url,
        creator_handle=creator_handle,
        video_id=video_id,
    )


def _is_creator_profile_url(profile_url: str, creator_handle: str) -> bool:
    parsed = urlparse(profile_url)
    host = parsed.hostname.lower() if parsed.hostname else ""
    return bool(
        parsed.scheme in {"http", "https"}
        and (host == "tiktok.com" or host.endswith(".tiktok.com"))
        and parsed.path.rstrip("/").lower()
        == f"/@{_normalize_handle(creator_handle)}".lower()
    )


def _visible_grid_rows_from_capture(
    capture: BrowserPageObservationSuccess,
) -> list[dict[str, Any]]:
    dom = capture.dom_observation
    if not isinstance(dom, dict):
        return []
    rows = dom.get("visible_selected_tiles")
    if not isinstance(rows, list):
        return []
    return [
        row
        for row in rows
        if isinstance(row, dict)
        and isinstance(row.get("video_id"), str)
        and isinstance(row.get("video_url"), str)
    ]


def capture_tiktok_creator_grid(
    *,
    profile_url: str,
    creator_handle: str,
    storage_state_path: Path,
    window_size: int,
    timeout_seconds: float,
    settle_seconds: float,
    max_grid_scroll_passes: int,
    engine: BrowserPageObservationEngine,
) -> BrowserPageObservationSuccess | BrowserSnapshotFailure:
    def target_reached(responses: Sequence[BrowserPageResponse]) -> bool:
        return len(_metric_items_from_responses(responses, creator_handle)) >= window_size

    return fetch_browser_page_observation_capture(
        url=profile_url,
        dom_extract_script=TIKTOK_PROFILE_GRID_DOM_EXTRACT_SCRIPT,
        dom_extract_arg={"creator_handle": creator_handle},
        response_url_predicate=is_tiktok_profile_item_list_url,
        post_load_pointer_actions=(TIKTOK_RELATIONSHIP_DIALOG_CLOSE_ACTION,),
        timeout_seconds=timeout_seconds,
        wait_until="domcontentloaded",
        settle_seconds=settle_seconds,
        lazy_load_scroll_passes=max_grid_scroll_passes,
        lazy_load_response_stop_condition=target_reached,
        dom_extract_after_lazy_load=True,
        storage_state_path=storage_state_path,
        headless=False,
        browser_backend=TIKTOK_BROWSER_BACKEND_CHROME_CDP,
        human_challenge_handoff_markers=TIKTOK_CHALLENGE_TEXT_MARKERS,
        human_challenge_handoff_timeout_seconds=180.0,
        human_challenge_handoff_prompt=TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
        engine=engine,
    )


# Compatibility alias for tests and callers that used the pre-public seam.
_capture_creator_grid = capture_tiktok_creator_grid


def build_tiktok_grid_window(
    *,
    creator_handle: str,
    capture: BrowserPageObservationSuccess,
    window_size: int,
    minimum_window_size: int | None = None,
) -> dict[str, Any]:
    """Freeze up to the cap while requiring enough rows for selection."""

    required_minimum = window_size if minimum_window_size is None else minimum_window_size
    if (
        isinstance(required_minimum, bool)
        or not isinstance(required_minimum, int)
        or required_minimum <= 0
        or required_minimum > window_size
    ):
        raise TikTokCreatorOnboardingError("minimum_window_size must be between 1 and window_size")
    dom = capture.dom_observation
    if not isinstance(dom, dict):
        raise TikTokCreatorOnboardingError("grid DOM observation is not an object")
    ordered_videos = dom.get("ordered_videos")
    if not isinstance(ordered_videos, list):
        raise TikTokCreatorOnboardingError("grid DOM observation lacks ordered_videos")

    metric_items = _metric_items_from_capture(capture, creator_handle)
    by_id = {str(item["video_id"]): item for item in metric_items}
    frozen: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in ordered_videos:
        if not isinstance(row, dict):
            continue
        video_id = str(row.get("video_id") or "").strip()
        video_url = str(row.get("video_url") or "").strip()
        if (
            not video_id
            or video_id in seen
            or video_id not in by_id
            or not _is_creator_video_url(
                video_url=video_url,
                creator_handle=creator_handle,
                video_id=video_id,
            )
        ):
            continue
        seen.add(video_id)
        frozen.append(
            {
                **by_id[video_id],
                "video_url": video_url,
                "pinned_visible": row.get("pinned_visible") is True,
                "visible_in_viewport": row.get("visible_in_viewport") is True,
                "grid_position": _non_negative_int_or_zero(
                    row.get("grid_position")
                ),
            }
        )
        if len(frozen) == window_size:
            break

    if len(frozen) < required_minimum:
        raise TikTokCreatorOnboardingError(
            "usable grid window unavailable: "
            f"required at least {required_minimum}, found {len(frozen)} ordered rows with metrics"
        )
    receipt = {
        "schema_version": TIKTOK_CREATOR_ONBOARDING_SCHEMA_VERSION,
        "creator_handle": creator_handle,
        "window_size": len(frozen),
        "window_cap": window_size,
        "minimum_window_size": required_minimum,
        "observed_ordered_video_count": len(ordered_videos),
        "observed_metric_video_count": len(metric_items),
        "complete": True,
        "items": frozen,
        "collection_receipt": {
            "capture_timestamp": capture.metadata.get("capture_timestamp"),
            "response_count": len(capture.responses),
            "scroll_passes_executed": capture.metadata.get(
                "lazy_load_scroll_passes_executed"
            ),
            "scroll_stop_reason": capture.metadata.get(
                "lazy_load_scroll_stop_reason"
            ),
            "response_target_stop_configured": capture.metadata.get(
                "lazy_load_response_stop_condition_configured"
            ),
        },
    }
    assert_no_sensitive_tiktok_material(receipt)
    return receipt


def _build_suggested_accounts_receipt(
    *,
    creator_handle: str,
    capture: BrowserPageObservationSuccess | BrowserSnapshotFailure,
) -> dict[str, Any]:
    if isinstance(capture, BrowserSnapshotFailure):
        return {
            "schema_version": TIKTOK_CREATOR_ONBOARDING_SCHEMA_VERSION,
            "creator_handle": creator_handle,
            "status": "failed",
            "suggested_accounts": [],
            "suggested_surface_detected": False,
            "suggested_surface_root_count": 0,
            "suggested_profile_anchor_count": 0,
            "profile_external_links": [],
            "profile_external_links_status": "failed",
            "failure_kind_or_none": capture.failure_kind.value,
            "outer_ui_route": "unresolved_capture_failure",
            "candidate_profiles_opened": 0,
            "account_mutations_taken": 0,
            "non_claims": ["not an exhaustive suggested-account graph"],
        }
    rows: list[dict[str, Any]] = []
    profile_external_links: list[dict[str, Any]] = []
    suggested_surface_detected = False
    suggested_surface_root_count = 0
    suggested_profile_anchor_count = 0
    relationship_dialog_detected = False
    suggested_tab_detected = False
    dom_route: str | None = None
    if isinstance(capture.dom_observation, dict):
        candidate_rows = capture.dom_observation.get("suggested_accounts")
        if isinstance(candidate_rows, list):
            rows = [row for row in candidate_rows if isinstance(row, dict)]
        external_rows = capture.dom_observation.get("profile_external_links")
        if isinstance(external_rows, list):
            profile_external_links = [
                row for row in external_rows if isinstance(row, dict)
            ]
        suggested_surface_detected = (
            capture.dom_observation.get("suggested_surface_detected") is True
        )
        suggested_surface_root_count = _non_negative_int_or_zero(
            capture.dom_observation.get("suggested_surface_root_count")
        )
        suggested_profile_anchor_count = _non_negative_int_or_zero(
            capture.dom_observation.get("suggested_profile_anchor_count")
        )
        relationship_dialog_detected = (
            capture.dom_observation.get("relationship_dialog_detected") is True
        )
        suggested_tab_detected = (
            capture.dom_observation.get("suggested_tab_detected") is True
        )
        raw_dom_route = capture.dom_observation.get("suggested_route")
        if isinstance(raw_dom_route, str) and raw_dom_route:
            dom_route = raw_dom_route
    status = (
        "captured"
        if rows
        else "visible_empty"
        if suggested_surface_detected
        else "not_visible"
    )
    receipt = {
        "schema_version": TIKTOK_CREATOR_ONBOARDING_SCHEMA_VERSION,
        "creator_handle": creator_handle,
        "status": status,
        "suggested_accounts": rows,
        "suggested_surface_detected": suggested_surface_detected,
        "suggested_surface_root_count": suggested_surface_root_count,
        "suggested_profile_anchor_count": suggested_profile_anchor_count,
        "relationship_dialog_detected": relationship_dialog_detected,
        "suggested_tab_detected": suggested_tab_detected,
        "outer_ui_route": (
            capture.metadata.get("suggested_outer_ui_route")
            or dom_route
            or "not_visible_after_primary_and_fallback"
        ),
        "candidate_profiles_opened": 0,
        "account_mutations_taken": 0,
        "profile_external_links": profile_external_links,
        "profile_external_links_status": "captured" if profile_external_links else "none_visible",
        "attempt_receipt": {
            "primary_followers_and_suggested_actions": capture.metadata.get(
                "suggested_primary_pointer_actions",
                capture.metadata.get("post_load_pointer_actions"),
            ),
            "fallback_view_all_actions": capture.metadata.get(
                "suggested_fallback_pointer_actions", []
            ),
            "outer_ui_route": capture.metadata.get("suggested_outer_ui_route"),
            "humanized_pointer_layer": capture.metadata.get(
                "humanized_pointer_layer",
                "cloakbrowser.patch_context(resolve_config('careful'))",
            ),
            "outer_move_steps_semantics": capture.metadata.get(
                "outer_move_steps_semantics",
                "BrowserPagePointerAction routing input; not the internal "
                "CloakBrowser humanized pointer path",
            ),
            "challenge_handoff_attempts": capture.metadata.get(
                "human_challenge_handoff_attempts"
            ),
            "capture_timestamp": capture.metadata.get("capture_timestamp"),
        },
        "non_claims": ["not an exhaustive suggested-account graph"],
    }
    assert_no_sensitive_tiktok_material(receipt)
    return receipt


def _non_negative_int_or_zero(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return 0
    return value


def is_tiktok_profile_item_list_url(url: str) -> bool:
    parsed = urlparse(url)
    host = parsed.hostname.lower() if parsed.hostname else ""
    return (
        parsed.scheme in {"http", "https"}
        and (host == "tiktok.com" or host.endswith(".tiktok.com"))
        and parsed.path.rstrip("/") == "/api/post/item_list"
    )


def _metric_items_from_capture(
    capture: BrowserPageObservationSuccess,
    creator_handle: str,
) -> list[dict[str, Any]]:
    items = _metric_items_from_responses(capture.responses, creator_handle)
    dom = capture.dom_observation
    if isinstance(dom, dict):
        hydration = dom.get("hydration_json_text")
        if isinstance(hydration, str) and hydration.strip():
            try:
                payload = json.loads(hydration)
            except json.JSONDecodeError:
                pass
            else:
                items = _dedupe_metric_items(
                    [*items, *_metric_items_from_payload(payload, creator_handle)]
                )
    return items


def _metric_items_from_responses(
    responses: Sequence[BrowserPageResponse],
    creator_handle: str,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for response in responses:
        if not response.body_text:
            continue
        try:
            payload = json.loads(response.body_text)
        except json.JSONDecodeError:
            continue
        items.extend(
            _metric_items_from_payload(
                payload,
                creator_handle,
                source_response_url=response.final_url or response.requested_url,
            )
        )
    return _dedupe_metric_items(items)


def _metric_items_from_payload(
    payload: object,
    creator_handle: str,
    *,
    source_response_url: str | None = None,
) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    normalized_handle = _normalize_handle(creator_handle)

    def consider(node: dict[str, Any]) -> None:
        stats = node.get("stats")
        raw_id = node.get("id")
        if not isinstance(stats, dict) or not isinstance(raw_id, (str, int)):
            return
        author = node.get("author")
        author_handle = (
            str(author.get("uniqueId") or "").lstrip("@").lower()
            if isinstance(author, dict)
            else ""
        )
        if author_handle and author_handle != normalized_handle:
            return

        # Bronze-facing grid evidence preserves every source-present stat and
        # every source-owned row, including a real zero-play row or a row whose
        # ranking metrics are incomplete. Selection eligibility is a separate
        # concern handled by grid_video_selection; dropping the row here would
        # make later longitudinal reconstruction impossible.
        item: dict[str, Any] = {
            "video_id": str(raw_id),
            "stats": dict(stats),
        }
        desc = node.get("desc")
        if isinstance(desc, str):
            item["desc"] = desc
        create_time = node.get("createTime", node.get("create_time"))
        if isinstance(create_time, int) and not isinstance(create_time, bool):
            item["createTime"] = create_time
        if isinstance(author, dict):
            item["author"] = {
                key: author[key]
                for key in ("id", "uid", "uniqueId", "nickname")
                if author.get(key) not in (None, "")
            }
            if author_handle:
                item["authorUniqueId"] = author_handle
        music = node.get("music")
        if isinstance(music, dict):
            item["music"] = {
                key: music[key]
                for key in ("id", "title", "authorName", "duration", "original")
                if music.get(key) is not None
            }
        challenges = node.get("challenges")
        if isinstance(challenges, list):
            item["challenges"] = [
                {
                    key: challenge[key]
                    for key in ("id", "title", "desc")
                    if challenge.get(key) not in (None, "")
                }
                for challenge in challenges
                if isinstance(challenge, dict)
            ]
        if source_response_url:
            parsed_source = urlparse(source_response_url)
            item["source_response_path"] = parsed_source.path
            item["source_response_url_sha256"] = sha256(
                source_response_url.encode("utf-8")
            ).hexdigest()
        item["field_provenance"] = {
            "video_id": "profile_grid_item_response",
            "stats": "profile_grid_item_response_exact_source_values",
            "author": "profile_grid_item_response_when_present",
            "desc": "profile_grid_item_response_when_present",
            "create_time": "profile_grid_item_response_when_present",
            "music": "profile_grid_item_response_when_present",
        }
        # Keep the two incumbent flat fields as compatibility mirrors while the
        # exact source-native stats object is the fidelity-preserving home.
        for key in ("playCount", "diggCount"):
            if key in stats:
                item[key] = stats[key]
        found.append(item)

    def visit(node: object) -> None:
        if isinstance(node, list):
            for value in node:
                visit(value)
            return
        if not isinstance(node, dict):
            return
        item_list = node.get("itemList")
        if isinstance(item_list, list):
            for item in item_list:
                if isinstance(item, dict):
                    consider(item)
            for key, value in node.items():
                if key != "itemList":
                    visit(value)
            return
        consider(node)
        for value in node.values():
            visit(value)

    visit(payload)
    return found


def _notify_progress(
    progress_fn: ProgressFn | None,
    event: str,
    **fields: object,
) -> None:
    if progress_fn is not None:
        progress_fn(event, dict(fields))


def _has_account_safety_stop(cadence_result: object) -> bool:
    if not isinstance(cadence_result, dict):
        return False
    failures = cadence_result.get("failures")
    if not isinstance(failures, list):
        return False
    for failure in failures:
        if not isinstance(failure, dict):
            continue
        triage = failure.get("blocker_triage")
        if isinstance(triage, dict) and triage.get("account_safety_stop") is True:
            return True
    return False


def _dedupe_metric_items(items: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in items:
        video_id = str(item["video_id"])
        if video_id in seen:
            continue
        seen.add(video_id)
        deduped.append(item)
    return deduped


def _is_creator_video_url(
    *,
    video_url: str,
    creator_handle: str,
    video_id: str,
) -> bool:
    parsed = urlparse(video_url)
    host = parsed.hostname.lower() if parsed.hostname else ""
    expected_path = f"/@{_normalize_handle(creator_handle)}/video/{video_id}"
    return (
        parsed.scheme in {"http", "https"}
        and (host == "tiktok.com" or host.endswith(".tiktok.com"))
        and parsed.path.rstrip("/").lower() == expected_path.lower()
    )


def _utc_iso(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _phase_chronology_row(
    phase: str,
    *,
    run_started_monotonic: float,
    monotonic_fn: MonotonicFn,
    utc_now_fn: UtcNowFn,
) -> dict[str, object]:
    return {
        "phase": phase,
        "observed_at_utc": _utc_iso(utc_now_fn()),
        "elapsed_seconds": round(
            max(0.0, monotonic_fn() - run_started_monotonic), 6
        ),
    }


def _output_paths(output_dir: Path) -> TikTokCreatorOnboardingOutputPaths:
    return TikTokCreatorOnboardingOutputPaths(
        suggested_accounts_json_path=output_dir / TIKTOK_ONBOARDING_SUGGESTED_JSON_NAME,
        grid_window_json_path=output_dir / TIKTOK_ONBOARDING_GRID_WINDOW_JSON_NAME,
        selection_json_path=output_dir / TIKTOK_ONBOARDING_SELECTION_JSON_NAME,
        live_grid_json_path=output_dir / TIKTOK_LIVE_BATCH_GRID_JSON_NAME,
        live_cadence_json_path=output_dir / TIKTOK_LIVE_BATCH_CADENCE_JSON_NAME,
        onboarding_receipt_json_path=output_dir / TIKTOK_ONBOARDING_RECEIPT_JSON_NAME,
    )


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    assert_no_sensitive_tiktok_material(payload)
    path.write_bytes(json_dumps_sanitized(payload))


def _sha256_path(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def _normalize_handle(handle: str) -> str:
    normalized = handle.strip().lstrip("@")
    if not normalized or "/" in normalized or "\\" in normalized:
        raise TikTokCreatorOnboardingError(
            "creator_handle must be a non-empty TikTok handle"
        )
    return normalized.lower()


__all__ = [
    "DEFAULT_MAX_GRID_SCROLL_PASSES",
    "DEFAULT_SELECTION_COUNT",
    "DEFAULT_WINDOW_SIZE",
    "TIKTOK_CREATOR_ONBOARDING_SCHEMA_VERSION",
    "TIKTOK_ONBOARDING_GRID_WINDOW_JSON_NAME",
    "TIKTOK_ONBOARDING_RECEIPT_JSON_NAME",
    "TIKTOK_ONBOARDING_SELECTION_JSON_NAME",
    "TIKTOK_ONBOARDING_SUGGESTED_JSON_NAME",
    "TikTokCreatorOnboardingError",
    "TikTokCreatorOnboardingOutputPaths",
    "build_tiktok_grid_window",
    "capture_tiktok_creator_grid",
    "is_tiktok_profile_item_list_url",
    "run_tiktok_creator_onboarding",
]
