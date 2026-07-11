"""Supervised one-creator TikTok onboarding orchestration.

This module composes existing session-profile, page-observation, grid-selection,
and live-batch deep-capture substrate. It is deliberately bounded to one creator
and one caller-visible browser lease; it is not a scanner, scheduler, registry
writer, or CAPTCHA solver.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence
from urllib.parse import urlparse

from source_capture.adapters.browser_snapshot import (
    BrowserPageObservationEngine,
    BrowserPageObservationSuccess,
    BrowserPagePointerAction,
    BrowserPageResponse,
    BrowserSnapshotFailure,
    CloakBrowserPageObservationSessionEngine,
    fetch_browser_page_observation_capture,
)
from source_capture.auth_state import validate_auth_state_provenance_requirement
from source_capture.session_profiles import SourceCaptureSessionProfile
from source_capture.tiktok.admission import (
    assert_no_sensitive_tiktok_material,
    json_dumps_sanitized,
)
from source_capture.tiktok.grid_video_selection import build_tiktok_grid_video_selection
from source_capture.tiktok.live_batch_probe import (
    TIKTOK_BROWSER_BACKEND_CLOAKBROWSER,
    TIKTOK_SUPERVISED_DEFAULT_CADENCE_GAP_SECONDS,
    TIKTOK_CHALLENGE_TEXT_MARKERS,
    TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
    TIKTOK_LIVE_BATCH_CADENCE_JSON_NAME,
    TIKTOK_LIVE_BATCH_GRID_JSON_NAME,
    run_tiktok_live_batch_probe,
)


TIKTOK_CREATOR_ONBOARDING_SCHEMA_VERSION = "tiktok_creator_onboarding_v0"
TIKTOK_ONBOARDING_SUGGESTED_JSON_NAME = "tiktok_suggested_accounts_attempt.json"
TIKTOK_ONBOARDING_GRID_WINDOW_JSON_NAME = "tiktok_grid_window.json"
TIKTOK_ONBOARDING_SELECTION_JSON_NAME = "tiktok_grid_video_selection.json"
TIKTOK_ONBOARDING_RECEIPT_JSON_NAME = "tiktok_creator_onboarding_receipt.json"
DEFAULT_WINDOW_SIZE = 32
DEFAULT_SELECTION_FRACTION = 0.25
DEFAULT_MAX_GRID_SCROLL_PASSES = 40

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
    videos.push({video_id: match[2], video_url: href});
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
  const selectors = [
    '[data-e2e*="suggest"]',
    '[class*="Suggested"]',
    '[class*="suggested"]',
    '[class*="Recommend"]',
    '[class*="recommend"]',
    '[role="dialog"]'
  ];
  const roots = [];
  for (const selector of selectors) {
    for (const node of Array.from(document.querySelectorAll(selector))) {
      if (!roots.includes(node)) roots.push(node);
    }
  }
  const rows = [];
  const seen = new Set();
  for (const root of roots) {
    for (const anchor of Array.from(root.querySelectorAll('a[href^="/@"],a[href*="tiktok.com/@"]'))) {
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
  return {suggested_accounts: rows};
}
""".strip()

TIKTOK_SUGGESTED_VIEW_ALL_ACTION = BrowserPagePointerAction(
    action_name="tiktok_suggested_accounts_view_all_v0",
    candidate_selector="button,a,[role='button']",
    text_markers=("view all", "see all"),
    page_text_markers=("suggested",),
    wait_after_ms=2000,
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


def run_tiktok_creator_onboarding(
    *,
    creator_handle: str,
    session_profile: SourceCaptureSessionProfile,
    output_dir: Path,
    auth_state_root: Path | None = None,
    window_size: int = DEFAULT_WINDOW_SIZE,
    selection_fraction: float = DEFAULT_SELECTION_FRACTION,
    timeout_seconds: float = 30.0,
    settle_seconds: float = 2.0,
    max_grid_scroll_passes: int = DEFAULT_MAX_GRID_SCROLL_PASSES,
    cadence_min_gap_seconds: float = TIKTOK_SUPERVISED_DEFAULT_CADENCE_GAP_SECONDS,
    cadence_max_gap_seconds: float = TIKTOK_SUPERVISED_DEFAULT_CADENCE_GAP_SECONDS,
    cadence_window_seconds: float | None = None,
    random_seed: int | None = None,
    engine: BrowserPageObservationEngine | None = None,
    deep_capture_fn: DeepCaptureFn = run_tiktok_live_batch_probe,
) -> TikTokCreatorOnboardingOutputPaths:
    """Run suggested -> grid -> select -> deep-capture in one browser context."""

    normalized_handle = _normalize_handle(creator_handle)
    if session_profile.platform != "tiktok":
        raise TikTokCreatorOnboardingError("session profile platform must be tiktok")
    if session_profile.browser_backend != TIKTOK_BROWSER_BACKEND_CLOAKBROWSER:
        raise TikTokCreatorOnboardingError("TikTok onboarding requires CloakBrowser")
    if isinstance(window_size, bool) or not isinstance(window_size, int) or window_size <= 0:
        raise TikTokCreatorOnboardingError("window_size must be a positive integer")
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
    observation_engine = engine or CloakBrowserPageObservationSessionEngine(
        cloakbrowser_humanize=False,
        human_challenge_handoff_markers=TIKTOK_CHALLENGE_TEXT_MARKERS,
        human_challenge_handoff_timeout_seconds=180.0,
        human_challenge_handoff_prompt=TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
    )

    stage = "acquire_session"
    status = "failed"
    error: str | None = None
    close_error: str | None = None
    selected_video_ids: list[str] = []
    completed_count = 0
    suggested_status: str | None = None
    artifacts_written: list[str] = []
    try:
        stage = "collect_suggested_accounts"
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
        _write_json(paths.suggested_accounts_json_path, suggested_receipt)
        artifacts_written.append(paths.suggested_accounts_json_path.name)
        if suggested_status == "failed":
            raise TikTokCreatorOnboardingError("suggested-account observation failed")

        stage = "collect_grid"
        grid_capture = _capture_creator_grid(
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
        grid_window = build_tiktok_grid_window(
            creator_handle=normalized_handle,
            capture=grid_capture,
            window_size=window_size,
        )
        _write_json(paths.grid_window_json_path, grid_window)
        artifacts_written.append(paths.grid_window_json_path.name)

        stage = "select"
        selection = build_tiktok_grid_video_selection(
            grid_window["items"],
            expected_item_count=window_size,
            selection_fraction=selection_fraction,
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
        selected_urls = [
            str(window_by_id[video_id]["video_url"]) for video_id in selected_video_ids
        ]

        stage = "deep_capture"
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
        )
        _write_json(paths.live_grid_json_path, deep_capture["grid_result"])
        artifacts_written.append(paths.live_grid_json_path.name)
        _write_json(paths.live_cadence_json_path, deep_capture["cadence_result"])
        artifacts_written.append(paths.live_cadence_json_path.name)
        completed_count = int(deep_capture["cadence_result"]["completed_count"])
        status = (
            "complete"
            if completed_count == len(selected_video_ids)
            else "partial_failure"
        )
        if status != "complete":
            raise TikTokCreatorOnboardingError(
                "one or more selected video deep captures did not complete"
            )
        stage = "close"
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
            "window_size": window_size,
            "selection_fraction": selection_fraction,
            "suggested_accounts_status_or_none": suggested_status,
            "selected_video_ids_in_capture_order": selected_video_ids,
            "selected_count": len(selected_video_ids),
            "completed_deep_capture_count": completed_count,
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
    return fetch_browser_page_observation_capture(
        url=profile_url,
        dom_extract_script=TIKTOK_SUGGESTED_ACCOUNTS_DOM_EXTRACT_SCRIPT,
        dom_extract_arg={"creator_handle": creator_handle},
        response_url_predicate=lambda _: False,
        post_load_pointer_actions=(TIKTOK_SUGGESTED_VIEW_ALL_ACTION,),
        timeout_seconds=timeout_seconds,
        wait_until="domcontentloaded",
        settle_seconds=settle_seconds,
        storage_state_path=storage_state_path,
        headless=False,
        browser_backend=TIKTOK_BROWSER_BACKEND_CLOAKBROWSER,
        human_challenge_handoff_markers=TIKTOK_CHALLENGE_TEXT_MARKERS,
        human_challenge_handoff_timeout_seconds=180.0,
        human_challenge_handoff_prompt=TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
        engine=engine,
    )


def _capture_creator_grid(
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
        timeout_seconds=timeout_seconds,
        wait_until="domcontentloaded",
        settle_seconds=settle_seconds,
        lazy_load_scroll_passes=max_grid_scroll_passes,
        lazy_load_response_stop_condition=target_reached,
        dom_extract_after_lazy_load=True,
        storage_state_path=storage_state_path,
        headless=False,
        browser_backend=TIKTOK_BROWSER_BACKEND_CLOAKBROWSER,
        human_challenge_handoff_markers=TIKTOK_CHALLENGE_TEXT_MARKERS,
        human_challenge_handoff_timeout_seconds=180.0,
        human_challenge_handoff_prompt=TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
        engine=engine,
    )


def build_tiktok_grid_window(
    *,
    creator_handle: str,
    capture: BrowserPageObservationSuccess,
    window_size: int,
) -> dict[str, Any]:
    """Freeze the first complete N source-visible grid rows."""

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
        frozen.append({**by_id[video_id], "video_url": video_url})
        if len(frozen) == window_size:
            break

    if len(frozen) != window_size:
        raise TikTokCreatorOnboardingError(
            "complete grid window unavailable: "
            f"required {window_size}, found {len(frozen)} ordered rows with metrics"
        )
    receipt = {
        "schema_version": TIKTOK_CREATOR_ONBOARDING_SCHEMA_VERSION,
        "creator_handle": creator_handle,
        "window_size": window_size,
        "observed_ordered_video_count": len(ordered_videos),
        "observed_metric_video_count": len(metric_items),
        "complete": True,
        "items": frozen,
        "collection_receipt": {
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
            "failure_kind_or_none": capture.failure_kind.value,
            "non_claims": ["not an exhaustive suggested-account graph"],
        }
    rows: list[dict[str, Any]] = []
    if isinstance(capture.dom_observation, dict):
        candidate_rows = capture.dom_observation.get("suggested_accounts")
        if isinstance(candidate_rows, list):
            rows = [row for row in candidate_rows if isinstance(row, dict)]
    receipt = {
        "schema_version": TIKTOK_CREATOR_ONBOARDING_SCHEMA_VERSION,
        "creator_handle": creator_handle,
        "status": "captured" if rows else "blocked_or_empty",
        "suggested_accounts": rows,
        "attempt_receipt": {
            "view_all_action": capture.metadata.get("post_load_pointer_action"),
            "view_all_actions": capture.metadata.get("post_load_pointer_actions"),
            "challenge_handoff_attempts": capture.metadata.get(
                "human_challenge_handoff_attempts"
            ),
        },
        "non_claims": ["not an exhaustive suggested-account graph"],
    }
    assert_no_sensitive_tiktok_material(receipt)
    return receipt


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
        items.extend(_metric_items_from_payload(payload, creator_handle))
    return _dedupe_metric_items(items)


def _metric_items_from_payload(
    payload: object,
    creator_handle: str,
) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    normalized_handle = _normalize_handle(creator_handle)

    def consider(node: dict[str, Any]) -> None:
        stats = node.get("stats")
        raw_id = node.get("id")
        if not isinstance(stats, dict) or not isinstance(raw_id, (str, int)):
            return
        play_count = stats.get("playCount")
        digg_count = stats.get("diggCount")
        author = node.get("author")
        author_handle = (
            str(author.get("uniqueId") or "").lstrip("@").lower()
            if isinstance(author, dict)
            else ""
        )
        if (
            isinstance(play_count, int)
            and not isinstance(play_count, bool)
            and play_count > 0
            and isinstance(digg_count, int)
            and not isinstance(digg_count, bool)
            and 0 <= digg_count <= play_count
            and (not author_handle or author_handle == normalized_handle)
        ):
            found.append(
                {
                    "video_id": str(raw_id),
                    "playCount": play_count,
                    "diggCount": digg_count,
                }
            )

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
    "DEFAULT_SELECTION_FRACTION",
    "DEFAULT_WINDOW_SIZE",
    "TIKTOK_CREATOR_ONBOARDING_SCHEMA_VERSION",
    "TIKTOK_ONBOARDING_GRID_WINDOW_JSON_NAME",
    "TIKTOK_ONBOARDING_RECEIPT_JSON_NAME",
    "TIKTOK_ONBOARDING_SELECTION_JSON_NAME",
    "TIKTOK_ONBOARDING_SUGGESTED_JSON_NAME",
    "TikTokCreatorOnboardingError",
    "TikTokCreatorOnboardingOutputPaths",
    "build_tiktok_grid_window",
    "is_tiktok_profile_item_list_url",
    "run_tiktok_creator_onboarding",
]
