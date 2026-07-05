from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Callable, Sequence
from urllib.parse import parse_qsl, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from harness_utils import utc_now_z
from source_capture.adapters.browser_snapshot import (
    BrowserPageObservationEngine,
    BrowserPageObservationSuccess,
    BrowserPagePointerAction,
    BrowserPageResponse,
    BrowserSnapshotFailure,
    fetch_browser_page_observation_capture,
)
from source_capture.auth_state import (
    AuthenticatedSessionMode,
    validate_auth_state_provenance_requirement,
    validate_auth_state_session_mode,
)
from source_capture.source_access_provenance import HarnessProxyProfilePosture
from source_capture.cadence import build_cadence_plan
from source_capture.tiktok.admission import (
    assert_no_sensitive_tiktok_material,
    decoded_aweme_id_create_time_utc,
    json_dumps_sanitized,
    parse_webvtt_cues,
)
from source_capture.tiktok.blocker_triage import (
    TIKTOK_BLOCKER_ACTION_STOP,
    TIKTOK_BLOCKER_CLASS_CHALLENGE_OR_SECURITY,
    TikTokBlockerTriage,
    classify_tiktok_capture,
)


TIKTOK_LIVE_BATCH_PROBE_SCHEMA_VERSION = "tiktok_live_batch_probe_v0"
TIKTOK_LIVE_BATCH_GRID_JSON_NAME = "tiktok_live_grid_result.json"
TIKTOK_LIVE_BATCH_CADENCE_JSON_NAME = "tiktok_live_cadence_result.json"

TIKTOK_VIDEO_DOM_EXTRACT_SCRIPT = r"""
() => {
  const hydration = document.querySelector('#__UNIVERSAL_DATA_FOR_REHYDRATION__');
  const normalizeText = (value) => String(value || '').replace(/\s+/g, ' ').trim();
  const candidateSelectors = [
    '[data-e2e="comment-item"]',
    '[data-e2e*="comment-level"]',
    '[data-e2e*="comment"]',
    '[class*="CommentItem"]',
    '[class*="comment-item"]'
  ];
  const hardSkipMarkers = [
    'drag the slider',
    'verify to continue',
    'captcha',
    'log in to comment'
  ];
  const exactSkipMarkers = [
    'comments',
    'you may like'
  ];
  const candidates = [];
  const seen = new Set();
  for (const selector of candidateSelectors) {
    for (const node of Array.from(document.querySelectorAll(selector))) {
      const rect = node.getBoundingClientRect();
      if (!rect || rect.width <= 0 || rect.height <= 0) {
        continue;
      }
      const text = normalizeText(node.innerText || node.textContent || '');
      const lowered = text.toLowerCase();
      if (text.length < 2 || text.length > 600 || exactSkipMarkers.includes(lowered)) {
        continue;
      }
      if (hardSkipMarkers.some((marker) => lowered.includes(marker))) {
        continue;
      }
      if (seen.has(text)) {
        continue;
      }
      seen.add(text);
      candidates.push({
        text,
        selector,
        text_char_count: text.length
      });
      if (candidates.length >= 12) {
        break;
      }
    }
    if (candidates.length >= 12) {
      break;
    }
  }
  return {
    hydration_json_text: hydration ? hydration.textContent : null,
    visible_comment_candidates: candidates
  };
}
""".strip()

TIKTOK_OPEN_COMMENTS_POINTER_ACTION_NAME = "tiktok_open_comments_pointer_v0"
TIKTOK_OPEN_MORE_LIKE_THIS_POINTER_ACTION_NAME = "tiktok_open_more_like_this_pointer_v0"
TIKTOK_REOPEN_COMMENTS_POINTER_ACTION_NAME = "tiktok_reopen_comments_pointer_v0"
TIKTOK_DISMISS_BENIGN_OVERLAY_POINTER_ACTION_NAME = "tiktok_dismiss_benign_overlay_pointer_v0"
TIKTOK_RETRY_VISIBLE_ERROR_POINTER_ACTION_NAME = "tiktok_retry_visible_error_pointer_v0"
TIKTOK_CHALLENGE_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME = (
    "tiktok_challenge_modal_close_diagnostic_pointer_v0"
)
TIKTOK_CHALLENGE_VISUAL_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME = (
    "tiktok_challenge_modal_visual_close_diagnostic_pointer_v0"
)
TIKTOK_CHALLENGE_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME = (
    "tiktok_challenge_modal_close_followthrough_pointer_v0"
)
TIKTOK_CHALLENGE_VISUAL_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME = (
    "tiktok_challenge_modal_visual_close_followthrough_pointer_v0"
)
TIKTOK_COMMENT_SURFACE_TOGGLE_POINTER_SEQUENCE_NAME = (
    "comment_surface_toggle_pointer_sequence_v0"
)
TIKTOK_CHALLENGE_CLOSE_DIAGNOSTIC_REASON = "challenge_close_diagnostic_only"
TIKTOK_CHALLENGE_AFTER_CLOSE_DIAGNOSTIC_REASON = (
    "platform_challenge_observed_after_close_diagnostic"
)
TIKTOK_CHALLENGE_AFTER_CLOSE_FOLLOWTHROUGH_REASON = (
    "platform_challenge_observed_after_close_followthrough"
)
TIKTOK_CHALLENGE_X_CLOSE_NOT_ACCEPTED_REASON = (
    "challenge_x_click_attempted_close_not_accepted"
)
TIKTOK_CHALLENGE_TEXT_MARKERS = (
    "drag the slider",
    "verify to continue",
    "captcha",
    "security check",
)
TIKTOK_BROWSER_BACKEND_DEFAULT = "play" + "wright"
TIKTOK_BROWSER_BACKEND_CLOAKBROWSER = "cloakbrowser"
TIKTOK_HUMAN_CHALLENGE_HANDOFF_TIMEOUT_SECONDS = 180.0
TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT = (
    "TikTok slider/captcha/security text remained after the scripted X/Close "
    "path. If authorized for this run, solve it manually in the open browser, "
    "then click OK here. The receipt will mark human_challenge_handoff; the "
    "agent does not drag or solve the puzzle."
)
TIKTOK_COMMENT_LIST_RESPONSE_CAP = 2
TIKTOK_COMMENT_ROUTE_NO_RESPONSE_REASON = "comment_list_response_absent"
TIKTOK_LOGGED_OUT_SESSION_MODE = "public_logged_out"
TIKTOK_DOM_VISIBLE_COMMENT_CANDIDATE_CAP = 12
TIKTOK_DOM_VISIBLE_COMMENT_TEXT_MAX_CHARS = 500
TIKTOK_SUBTITLE_WEBVTT_MAX_BYTES = 1_000_000
TIKTOK_SUBTITLE_FETCH_TIMEOUT_SECONDS = 5.0
TIKTOK_SUBTITLE_ALLOWED_HOST_SUFFIXES = (
    "tiktokcdn.com",
    "tiktokcdn-us.com",
    "tiktokcdn-eu.com",
    "byteoversea.com",
)
_URL_IN_TEXT_RE = re.compile(r"https?://\S+")
# DOM fallback must capture comment-body-like text, not visible count badges.
_COUNT_ONLY_TEXT_RE = re.compile(r"^[\d\s,._+-]+[kmb]?(?:\s+comments?)?$", re.IGNORECASE)

_TIKTOK_VIDEO_URL_RE = re.compile(r"^/@(?P<handle>[^/]+)/video/(?P<video_id>\d+)$")

JsonObject = dict[str, Any]
SleepFn = Callable[[float], None]
SubtitleFetchFn = Callable[[str], bytes]


@dataclass(frozen=True)
class TikTokLiveBatchProbeOutputPaths:
    grid_result_json_path: Path
    cadence_result_json_path: Path


def write_tiktok_live_batch_probe_outputs(
    *,
    creator_handle: str,
    creator_profile_url: str,
    video_urls: Sequence[str],
    state_label: str | None = None,
    session_mode: AuthenticatedSessionMode | None = None,
    logged_out: bool = False,
    output_dir: Path,
    auth_state_root: Path | None = None,
    timeout_seconds: float = 30.0,
    wait_until: str = "domcontentloaded",
    viewport_width: int = 1280,
    viewport_height: int = 720,
    max_response_bytes: int = 5_000_000,
    settle_seconds: float = 2.0,
    selector_timeout_seconds: float = 5.0,
    browser_channel: str | None = None,
    browser_backend: str = TIKTOK_BROWSER_BACKEND_DEFAULT,
    required_harness_proxy_profile_posture: str | HarnessProxyProfilePosture | None = None,
    cloakbrowser_humanize: bool = False,
    human_challenge_handoff: bool = False,
    human_challenge_handoff_timeout_seconds: float = TIKTOK_HUMAN_CHALLENGE_HANDOFF_TIMEOUT_SECONDS,
    cadence_min_gap_seconds: float = 75.0,
    cadence_max_gap_seconds: float = 120.0,
    cadence_window_seconds: float | None = None,
    random_seed: int | None = None,
    allow_challenge_close_diagnostic: bool = False,
    allow_challenge_close_followthrough: bool = False,
    engine: BrowserPageObservationEngine | None = None,
    sleep_fn: SleepFn = time.sleep,
    subtitle_fetcher: SubtitleFetchFn | None = None,
) -> TikTokLiveBatchProbeOutputPaths:
    """Capture sanitized TikTok live staging JSON for one creator.

    The output is intentionally not a SourceCapturePacket. It is local staging
    shaped for the existing TikTok batch admission gate, which performs the
    durable packet sanitization and lake write.
    """
    result = run_tiktok_live_batch_probe(
        creator_handle=creator_handle,
        creator_profile_url=creator_profile_url,
        video_urls=video_urls,
        state_label=state_label,
        session_mode=session_mode,
        logged_out=logged_out,
        auth_state_root=auth_state_root,
        timeout_seconds=timeout_seconds,
        wait_until=wait_until,
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        max_response_bytes=max_response_bytes,
        settle_seconds=settle_seconds,
        selector_timeout_seconds=selector_timeout_seconds,
        browser_channel=browser_channel,
        browser_backend=browser_backend,
        required_harness_proxy_profile_posture=required_harness_proxy_profile_posture,
        cloakbrowser_humanize=cloakbrowser_humanize,
        human_challenge_handoff=human_challenge_handoff,
        human_challenge_handoff_timeout_seconds=human_challenge_handoff_timeout_seconds,
        cadence_min_gap_seconds=cadence_min_gap_seconds,
        cadence_max_gap_seconds=cadence_max_gap_seconds,
        cadence_window_seconds=cadence_window_seconds,
        random_seed=random_seed,
        allow_challenge_close_diagnostic=allow_challenge_close_diagnostic,
        allow_challenge_close_followthrough=allow_challenge_close_followthrough,
        engine=engine,
        sleep_fn=sleep_fn,
        subtitle_fetcher=subtitle_fetcher,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    grid_path = output_dir / TIKTOK_LIVE_BATCH_GRID_JSON_NAME
    cadence_path = output_dir / TIKTOK_LIVE_BATCH_CADENCE_JSON_NAME
    grid_path.write_bytes(json_dumps_sanitized(result["grid_result"]))
    cadence_path.write_bytes(json_dumps_sanitized(result["cadence_result"]))
    return TikTokLiveBatchProbeOutputPaths(
        grid_result_json_path=grid_path,
        cadence_result_json_path=cadence_path,
    )


def run_tiktok_live_batch_probe(
    *,
    creator_handle: str,
    creator_profile_url: str,
    video_urls: Sequence[str],
    state_label: str | None = None,
    session_mode: AuthenticatedSessionMode | None = None,
    logged_out: bool = False,
    auth_state_root: Path | None = None,
    timeout_seconds: float = 30.0,
    wait_until: str = "domcontentloaded",
    viewport_width: int = 1280,
    viewport_height: int = 720,
    max_response_bytes: int = 5_000_000,
    settle_seconds: float = 2.0,
    selector_timeout_seconds: float = 5.0,
    browser_channel: str | None = None,
    browser_backend: str = TIKTOK_BROWSER_BACKEND_DEFAULT,
    required_harness_proxy_profile_posture: str | HarnessProxyProfilePosture | None = None,
    cloakbrowser_humanize: bool = False,
    human_challenge_handoff: bool = False,
    human_challenge_handoff_timeout_seconds: float = TIKTOK_HUMAN_CHALLENGE_HANDOFF_TIMEOUT_SECONDS,
    cadence_min_gap_seconds: float = 75.0,
    cadence_max_gap_seconds: float = 120.0,
    cadence_window_seconds: float | None = None,
    random_seed: int | None = None,
    allow_challenge_close_diagnostic: bool = False,
    allow_challenge_close_followthrough: bool = False,
    engine: BrowserPageObservationEngine | None = None,
    sleep_fn: SleepFn = time.sleep,
    subtitle_fetcher: SubtitleFetchFn | None = None,
) -> JsonObject:
    normalized_handle = _normalize_handle(creator_handle)
    normalized_profile_url = _normalize_profile_url(creator_profile_url, normalized_handle)
    normalized_video_urls = [
        _normalize_video_url(url, expected_handle=normalized_handle) for url in video_urls
    ]
    if not normalized_video_urls:
        raise ValueError("at least one TikTok video URL is required")
    subtitle_fetcher = subtitle_fetcher or _fetch_subtitle_webvtt
    browser_backend = browser_backend.strip().lower()
    if browser_backend not in (
        TIKTOK_BROWSER_BACKEND_DEFAULT,
        TIKTOK_BROWSER_BACKEND_CLOAKBROWSER,
    ):
        raise ValueError("browser_backend must be one of: cloakbrowser, " + TIKTOK_BROWSER_BACKEND_DEFAULT)

    if allow_challenge_close_diagnostic and allow_challenge_close_followthrough:
        raise ValueError(
            "challenge-close diagnostic and followthrough modes are mutually exclusive"
        )
    if human_challenge_handoff and not allow_challenge_close_followthrough:
        raise ValueError("human_challenge_handoff requires challenge-close followthrough mode")
    if (
        browser_backend != TIKTOK_BROWSER_BACKEND_CLOAKBROWSER
        and cloakbrowser_humanize
    ):
        raise ValueError("cloakbrowser_humanize requires browser_backend='cloakbrowser'")

    if logged_out:
        if state_label is not None or session_mode is not None:
            raise ValueError("logged_out mode must not receive state_label or session_mode")
        if required_harness_proxy_profile_posture is not None:
            raise ValueError("required_harness_proxy_profile_posture requires sessioned mode")
        storage_state_path: Path | None = None
        comment_response_cap = 1
    else:
        if state_label is None or session_mode is None:
            raise ValueError("sessioned TikTok capture requires state_label and session_mode")
        if required_harness_proxy_profile_posture is not None:
            storage_state_path = validate_auth_state_provenance_requirement(
                state_label,
                session_mode=session_mode,
                required_harness_proxy_profile_posture=required_harness_proxy_profile_posture,
                auth_state_root=auth_state_root,
            )
        else:
            storage_state_path = validate_auth_state_session_mode(
                state_label,
                session_mode=session_mode,
                auth_state_root=auth_state_root,
            )
        comment_response_cap = TIKTOK_COMMENT_LIST_RESPONSE_CAP
    cadence_plan = _build_probe_cadence_plan(
        video_count=len(normalized_video_urls),
        min_gap_seconds=cadence_min_gap_seconds,
        max_gap_seconds=cadence_max_gap_seconds,
        window_seconds=cadence_window_seconds,
        random_seed=random_seed,
    )

    attempts = 0
    challenge_count = 0
    challenge_close_followthrough_count = 0
    failures: list[JsonObject] = []
    results: list[JsonObject] = []
    grid_items: list[JsonObject] = []

    for index, video_url in enumerate(normalized_video_urls):
        if index > 0:
            sleep_fn(cadence_plan.planned_waits_seconds[index - 1])

        attempts += 1
        video_id = _video_id_from_tiktok_url(video_url)
        observed_utc = utc_now_z()
        capture_result = fetch_browser_page_observation_capture(
            url=video_url,
            dom_extract_script=TIKTOK_VIDEO_DOM_EXTRACT_SCRIPT,
            dom_extract_arg=None,
            response_url_predicate=is_tiktok_comment_list_url,
            post_load_pointer_actions=_tiktok_live_pointer_actions(
                video_id=video_id,
                random_seed=random_seed,
                allow_challenge_close_diagnostic=allow_challenge_close_diagnostic,
                allow_challenge_close_followthrough=allow_challenge_close_followthrough,
            ),
            timeout_seconds=timeout_seconds,
            wait_until=wait_until,
            viewport_width=viewport_width,
            viewport_height=viewport_height,
            max_response_bytes=max_response_bytes,
            settle_seconds=settle_seconds,
            selector_timeout_seconds=selector_timeout_seconds,
            storage_state_path=storage_state_path,
            headless=False,
            browser_channel=browser_channel,
            browser_backend=browser_backend,
            cloakbrowser_humanize=cloakbrowser_humanize,
            human_challenge_handoff_markers=(
                TIKTOK_CHALLENGE_TEXT_MARKERS if human_challenge_handoff else ()
            ),
            human_challenge_handoff_after_action_names=(
                _tiktok_human_challenge_handoff_after_action_names()
                if human_challenge_handoff
                else ()
            ),
            human_challenge_handoff_timeout_seconds=human_challenge_handoff_timeout_seconds,
            human_challenge_handoff_prompt=TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
            engine=engine,
        )

        if isinstance(capture_result, BrowserSnapshotFailure):
            failures.append(
                _failure_entry(
                    video_url=video_url,
                    video_id=video_id,
                    observed_utc=observed_utc,
                    reason=f"capture_failed:{capture_result.failure_kind.value}",
                    detail=capture_result.message,
                )
            )
            continue

        challenge_close_action = _challenge_close_action_summary(capture_result)
        challenge_close_clicked = _first_bool(challenge_close_action.get("clicked")) is True
        challenge_close_accepted = _challenge_close_accepted(challenge_close_action)
        blocker_triage = classify_tiktok_capture(capture_result)
        challenge_reason = _challenge_reason_from_triage(blocker_triage)
        if challenge_reason is not None:
            close_followthrough_attempted = (
                allow_challenge_close_followthrough and challenge_close_clicked
            )
            challenge_count += 1
            failures.append(
                _failure_entry(
                    video_url=video_url,
                    video_id=video_id,
                    observed_utc=observed_utc,
                    reason=(
                        TIKTOK_CHALLENGE_AFTER_CLOSE_FOLLOWTHROUGH_REASON
                        if close_followthrough_attempted
                        else TIKTOK_CHALLENGE_AFTER_CLOSE_DIAGNOSTIC_REASON
                        if challenge_close_clicked
                        else challenge_reason
                    ),
                    detail=(
                        "TikTok challenge/auth-wall marker remained visible after the "
                        "owner-authorized challenge-close followthrough pointer path; "
                        "probe stopped."
                        if close_followthrough_attempted
                        else "TikTok challenge/auth-wall marker observed after the "
                        "challenge-close diagnostic pointer path; probe stopped."
                        if challenge_close_clicked
                        else "TikTok challenge/auth-wall marker observed; probe stopped."
                    ),
                    blocker_triage=_with_comment_route_observation(
                        _with_challenge_close_action(
                            _blocker_triage_receipt(blocker_triage),
                            challenge_close_action,
                            challenge_close_followthrough=False,
                            challenge_close_diagnostic=(
                                challenge_close_clicked and not close_followthrough_attempted
                            ),
                            challenge_close_accepted=(
                                False
                                if close_followthrough_attempted
                                else challenge_close_accepted
                            ),
                        ),
                        capture_result,
                        comment_response_cap=comment_response_cap,
                        admit_comment_responses=False,
                    ),
                )
            )
            break

        if challenge_close_clicked and not allow_challenge_close_followthrough:
            challenge_count += 1
            failures.append(
                _failure_entry(
                    video_url=video_url,
                    video_id=video_id,
                    observed_utc=observed_utc,
                    reason=TIKTOK_CHALLENGE_CLOSE_DIAGNOSTIC_REASON,
                    detail=(
                        "Challenge-close diagnostic pointer clicked before comment capture; "
                        "post-dismissal observations are diagnostic only and cannot satisfy "
                        "the clean microbatch/admission gate."
                    ),
                    blocker_triage=_challenge_close_diagnostic_blocker_receipt(
                        capture_result,
                        challenge_close_diagnostic=challenge_close_action,
                        comment_response_cap=comment_response_cap,
                    ),
                )
            )
            break
        if (
            challenge_close_clicked
            and allow_challenge_close_followthrough
            and not challenge_close_accepted
        ):
            challenge_count += 1
            failures.append(
                _failure_entry(
                    video_url=video_url,
                    video_id=video_id,
                    observed_utc=observed_utc,
                    reason=TIKTOK_CHALLENGE_X_CLOSE_NOT_ACCEPTED_REASON,
                    detail=(
                        "TikTok challenge X/Close received a pointer click, but the "
                        "post-click verification did not prove the slider modal cleared; "
                        "probe stopped before comment admission."
                    ),
                    blocker_triage=_with_comment_route_observation(
                        _with_challenge_close_action(
                            _challenge_close_not_accepted_blocker_receipt(
                                challenge_close_action
                            ),
                            challenge_close_action,
                            challenge_close_followthrough=False,
                            challenge_close_accepted=False,
                        ),
                        capture_result,
                        comment_response_cap=comment_response_cap,
                        admit_comment_responses=False,
                    ),
                )
            )
            break
        if challenge_close_accepted:
            challenge_close_followthrough_count += 1

        item_struct = _extract_item_struct(capture_result.dom_observation)
        blocker_triage = classify_tiktok_capture(
            capture_result,
            item_struct_present=item_struct is not None,
        )
        if item_struct is None:
            # C6 names an empty/stripped shell as a genuine-block symptom alongside
            # captcha text and 403 HTML; stop like a detected challenge instead of
            # hammering the remaining cadence-planned videos.
            challenge_count += 1
            failures.append(
                _failure_entry(
                    video_url=video_url,
                    video_id=video_id,
                    observed_utc=observed_utc,
                    reason="missing_video_detail_hydration",
                    detail=(
                        "No video itemStruct found in TikTok hydration blob; treated as a "
                        "possible empty/stripped-shell block signal (C6) and the probe stopped."
                    ),
                    blocker_triage=_blocker_triage_receipt(blocker_triage),
                )
            )
            break

        if blocker_triage.action == TIKTOK_BLOCKER_ACTION_STOP:
            # itemStruct can be present alongside an unresolved ambiguous-stop
            # marker (e.g. an unclassified dismiss control); the triage's own
            # stop verdict must be honored even though hydration loaded, or C6's
            # "do not hammer on an unresolved block signal" invariant is silently
            # defeated.
            challenge_count += 1
            failures.append(
                _failure_entry(
                    video_url=video_url,
                    video_id=video_id,
                    observed_utc=observed_utc,
                    reason=blocker_triage.reason,
                    detail=(
                        "TikTok blocker triage returned a stop action despite present "
                        "hydration/itemStruct; probe stopped."
                    ),
                    blocker_triage=_blocker_triage_receipt(blocker_triage),
                )
            )
            break

        item_video_id = str(item_struct.get("id") or "").strip()
        if item_video_id and item_video_id != video_id:
            failures.append(
                _failure_entry(
                    video_url=video_url,
                    video_id=video_id,
                    observed_utc=observed_utc,
                    reason="hydration_video_id_mismatch",
                    detail=f"Hydration item id {item_video_id!r} did not match URL video id.",
                )
            )
            continue

        grid_candidate = _grid_candidate_from_item_struct(
            item_struct,
            creator_handle=normalized_handle,
            video_url=video_url,
        )
        row = _cadence_row_from_capture(
            item_struct=item_struct,
            creator_handle=normalized_handle,
            video_url=video_url,
            video_id=video_id,
            capture_result=capture_result,
            observed_utc=observed_utc,
            grid_candidate=grid_candidate,
            blocker_triage=blocker_triage,
            comment_response_cap=comment_response_cap,
            challenge_close_action=challenge_close_action,
            challenge_close_followthrough_allowed=allow_challenge_close_followthrough,
            subtitle_fetcher=subtitle_fetcher,
        )
        assert_no_sensitive_tiktok_material(row)
        assert_no_sensitive_tiktok_material(grid_candidate)

        comment_receipt = _as_dict(row.get("capture_receipt"))
        if (
            _first_int(comment_receipt.get("admitted_comment_response_count"), 0) == 0
            and _first_int(comment_receipt.get("dom_visible_comment_candidate_count"), 0) == 0
        ):
            failures.append(
                _failure_entry(
                    video_url=video_url,
                    video_id=video_id,
                    observed_utc=observed_utc,
                    reason=TIKTOK_COMMENT_ROUTE_NO_RESPONSE_REASON,
                    detail=(
                        "No page-owned TikTok /api/comment/list response was observed after "
                        "the bounded comments/more-like-this/comments route-opening action, "
                        "and no DOM-visible comment candidates were found; probe stopped before "
                        "treating this as a completed comment-capture row."
                    ),
                    blocker_triage=_comment_route_zero_yield_blocker_triage(
                        comment_receipt,
                        challenge_close_action=(
                            challenge_close_action if challenge_close_accepted else None
                        ),
                        challenge_close_followthrough=(
                            allow_challenge_close_followthrough and challenge_close_accepted
                        ),
                        challenge_close_accepted=(
                            challenge_close_accepted if challenge_close_accepted else None
                        ),
                    ),
                )
            )
            break

        results.append(row)
        grid_items.append(grid_candidate)

    run_complete_utc = utc_now_z()
    grid_result = {
        "schema_version": TIKTOK_LIVE_BATCH_PROBE_SCHEMA_VERSION,
        "creator_handle": normalized_handle,
        "creator_profile_url": normalized_profile_url,
        "capture_contract": _capture_contract(
            session_mode=session_mode,
            logged_out=logged_out,
            browser_backend=browser_backend,
            required_harness_proxy_profile_posture=required_harness_proxy_profile_posture,
            cloakbrowser_humanize=cloakbrowser_humanize,
            human_challenge_handoff=human_challenge_handoff,
            human_challenge_handoff_timeout_seconds=human_challenge_handoff_timeout_seconds,
            allow_challenge_close_diagnostic=allow_challenge_close_diagnostic,
            allow_challenge_close_followthrough=allow_challenge_close_followthrough,
        ),
        "response_items": grid_items,
        "run_complete_utc": run_complete_utc,
        "non_claims": _non_claims(),
    }
    cadence_result = {
        "schema_version": TIKTOK_LIVE_BATCH_PROBE_SCHEMA_VERSION,
        "creator_handle": normalized_handle,
        "creator_profile_url": normalized_profile_url,
        "requested_video_count": len(normalized_video_urls),
        "attempted_count": attempts,
        "completed_count": len(results),
        "challenge_count": challenge_count,
        "challenge_close_followthrough_count": challenge_close_followthrough_count,
        "capture_contract": _capture_contract(
            session_mode=session_mode,
            logged_out=logged_out,
            browser_backend=browser_backend,
            required_harness_proxy_profile_posture=required_harness_proxy_profile_posture,
            cloakbrowser_humanize=cloakbrowser_humanize,
            human_challenge_handoff=human_challenge_handoff,
            human_challenge_handoff_timeout_seconds=human_challenge_handoff_timeout_seconds,
            allow_challenge_close_diagnostic=allow_challenge_close_diagnostic,
            allow_challenge_close_followthrough=allow_challenge_close_followthrough,
        ),
        "cadence_plan": cadence_plan.to_dict(),
        "results": results,
        "failures": failures,
        "run_complete_utc": run_complete_utc,
        "non_claims": _non_claims(),
    }
    payload = {"grid_result": grid_result, "cadence_result": cadence_result}
    assert_no_sensitive_tiktok_material(payload)
    return payload


def is_tiktok_comment_list_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False
    host = parsed.hostname.lower() if parsed.hostname else ""
    if host != "tiktok.com" and not host.endswith(".tiktok.com"):
        return False
    return parsed.path.rstrip("/") == "/api/comment/list"


def detect_tiktok_challenge(capture_result: BrowserPageObservationSuccess) -> str | None:
    return _challenge_reason_from_triage(classify_tiktok_capture(capture_result))


def _challenge_reason_from_triage(triage: TikTokBlockerTriage) -> str | None:
    if triage.blocker_class == TIKTOK_BLOCKER_CLASS_CHALLENGE_OR_SECURITY:
        return triage.reason
    return None


def _blocker_triage_receipt(triage: TikTokBlockerTriage) -> JsonObject:
    receipt = triage.to_receipt()
    receipt["action_mode"] = "classification_only"
    receipt["action_taken"] = False
    return receipt


def _comment_route_zero_yield_blocker_triage(
    comment_receipt: JsonObject,
    *,
    challenge_close_action: JsonObject | None = None,
    challenge_close_followthrough: bool = False,
    challenge_close_accepted: bool | None = None,
) -> JsonObject:
    receipt = {
        "blocker_class": "comment_route_zero_yield",
        "action": "stop",
        "reason": TIKTOK_COMMENT_ROUTE_NO_RESPONSE_REASON,
        "action_mode": "diagnosis_only",
        "action_taken": False,
        "benign_overlay_action": _as_dict(
            comment_receipt.get("benign_overlay_action")
        ),
        "comment_action": (
            _as_dict(comment_receipt.get("comment_action"))
            or _missing_comment_route_action_summary()
        ),
        "response_count": _first_int(comment_receipt.get("response_count"), 0),
        "matched_comment_response_count": _first_int(
            comment_receipt.get("matched_comment_response_count"), 0
        ),
        "admitted_comment_response_count": 0,
        "dom_visible_comment_candidate_count": _first_int(
            comment_receipt.get("dom_visible_comment_candidate_count"), 0
        ),
    }
    challenge_close_action = _as_dict(challenge_close_action)
    if challenge_close_action:
        receipt["challenge_close_action"] = challenge_close_action
    if challenge_close_followthrough:
        receipt["challenge_close_followthrough"] = True
    if challenge_close_accepted is not None:
        receipt["challenge_close_accepted"] = challenge_close_accepted
    return receipt


def _missing_comment_route_action_summary() -> JsonObject:
    return {
        "sequence_name": TIKTOK_COMMENT_SURFACE_TOGGLE_POINTER_SEQUENCE_NAME,
        "action_count": 0,
        "action_sequence": [],
        "clicked_all_targets": False,
    }

def _with_challenge_close_action(
    receipt: JsonObject,
    challenge_close_action: JsonObject,
    *,
    challenge_close_followthrough: bool = False,
    challenge_close_diagnostic: bool = False,
    challenge_close_accepted: bool | None = None,
) -> JsonObject:
    if challenge_close_action:
        receipt["challenge_close_action"] = challenge_close_action
        if challenge_close_followthrough:
            receipt["challenge_close_followthrough"] = True
        if challenge_close_accepted is not None:
            receipt["challenge_close_accepted"] = challenge_close_accepted
        if challenge_close_diagnostic:
            receipt["challenge_close_diagnostic"] = challenge_close_action
    return receipt


def _challenge_close_not_accepted_blocker_receipt(
    challenge_close_action: JsonObject,
) -> JsonObject:
    matched_marker = _first_str(challenge_close_action.get("page_text_matched_marker"))
    return _drop_none(
        {
            "blocker_class": "challenge_close_not_accepted",
            "action": "stop",
            "reason": TIKTOK_CHALLENGE_X_CLOSE_NOT_ACCEPTED_REASON,
            "action_mode": "source_access_intervention",
            "action_taken": True,
            "marker_family": "challenge_or_security" if matched_marker else None,
            "matched_marker": matched_marker,
            "challenge_kind": _challenge_kind_from_close_action(challenge_close_action),
        }
    )


def _challenge_kind_from_close_action(challenge_close_action: JsonObject) -> str | None:
    matched_marker = _first_str(challenge_close_action.get("page_text_matched_marker"))
    if matched_marker:
        return _challenge_kind_from_marker(matched_marker)
    if _first_bool(challenge_close_action.get("page_text_gate_matched")) is True:
        return "closeable_challenge_modal"
    if _first_bool(challenge_close_action.get("post_click_visual_target_absent")) is False:
        return "visual_challenge_target_remaining"
    return None


def _challenge_kind_from_marker(marker: str) -> str:
    if marker == "drag the slider":
        return "slider"
    if marker == "captcha":
        return "captcha"
    if marker == "security check":
        return "security_check"
    if marker == "verify to continue":
        return "verification_gate"
    return "unknown_platform_challenge"

def _challenge_close_accepted(challenge_close_action: JsonObject) -> bool:
    if _first_bool(challenge_close_action.get("clicked")) is not True:
        return False
    verification_values = [
        value
        for value in (
            _first_bool(challenge_close_action.get("post_click_absence_verified")),
            _first_bool(challenge_close_action.get("post_click_visual_target_absent")),
        )
        if value is not None
    ]
    return bool(verification_values) and all(verification_values)


def _with_comment_route_observation(
    receipt: JsonObject,
    capture_result: BrowserPageObservationSuccess,
    *,
    comment_response_cap: int,
    admit_comment_responses: bool = True,
) -> JsonObject:
    comment_list_responses = _page_owned_comment_list_responses(
        capture_result,
        response_cap=comment_response_cap,
    )
    receipt["benign_overlay_action"] = _benign_overlay_action_summary(capture_result)
    comment_action = _comment_action_summary(capture_result)
    if comment_action:
        receipt["comment_action"] = comment_action
    receipt["response_count"] = len(capture_result.responses)
    receipt["matched_comment_response_count"] = sum(
        1
        for response in capture_result.responses
        if _is_page_owned_comment_list_response(response)
    )
    receipt["admitted_comment_response_count"] = (
        len(comment_list_responses) if admit_comment_responses else 0
    )
    receipt["dom_visible_comment_candidate_count"] = len(
        _dom_visible_comment_candidates(capture_result)
    )
    pointer_chronology = _pointer_action_chronology(capture_result)
    if pointer_chronology:
        receipt["pointer_action_chronology"] = pointer_chronology
    challenge_close_attempts = _challenge_close_attempts(capture_result)
    if challenge_close_attempts:
        receipt["challenge_close_attempts"] = challenge_close_attempts
    human_handoff_attempts = _human_challenge_handoff_attempts(capture_result)
    if human_handoff_attempts:
        receipt["human_challenge_handoff_attempts"] = human_handoff_attempts
        receipt["human_challenge_handoff"] = True
    return receipt


def _challenge_close_diagnostic_blocker_receipt(
    capture_result: BrowserPageObservationSuccess,
    *,
    challenge_close_diagnostic: JsonObject,
    comment_response_cap: int,
) -> JsonObject:
    receipt = _with_comment_route_observation(
        _drop_none(
            {
                "blocker_class": "challenge_close_diagnostic",
                "action": "stop",
                "reason": TIKTOK_CHALLENGE_CLOSE_DIAGNOSTIC_REASON,
                "action_mode": "diagnosis_only",
                "action_taken": True,
                "challenge_close_diagnostic": challenge_close_diagnostic,
            }
        ),
        capture_result,
        comment_response_cap=comment_response_cap,
        admit_comment_responses=False,
    )
    return _drop_none(receipt)


def _tiktok_live_pointer_actions(
    *,
    video_id: str,
    random_seed: int | None,
    allow_challenge_close_diagnostic: bool,
    allow_challenge_close_followthrough: bool,
) -> tuple[BrowserPagePointerAction, ...]:
    retry_action = _tiktok_retry_visible_error_pointer_action(
        video_id=video_id,
        random_seed=random_seed,
    )
    benign_overlay_action = _tiktok_dismiss_benign_overlay_pointer_action(
        video_id=video_id,
        random_seed=random_seed,
    )
    comment_actions = _tiktok_comment_route_pointer_actions(
        video_id=video_id,
        random_seed=random_seed,
    )
    if allow_challenge_close_followthrough:
        return (
            retry_action,
            benign_overlay_action,
            _tiktok_challenge_close_followthrough_pointer_action(
                video_id=video_id,
                random_seed=random_seed,
            ),
            _tiktok_challenge_visual_close_followthrough_pointer_action(
                video_id=video_id,
                random_seed=random_seed,
            ),
            *_interleave_challenge_followthrough_actions(
                comment_actions,
                video_id=video_id,
                random_seed=random_seed,
            ),
        )
    if not allow_challenge_close_diagnostic:
        return (retry_action, benign_overlay_action, *comment_actions)
    return (
        retry_action,
        benign_overlay_action,
        _tiktok_challenge_close_diagnostic_pointer_action(
            video_id=video_id,
            random_seed=random_seed,
        ),
        *_interleave_challenge_diagnostic_actions(
            comment_actions,
            video_id=video_id,
            random_seed=random_seed,
        ),
    )


def _interleave_challenge_followthrough_actions(
    comment_actions: Sequence[BrowserPagePointerAction],
    *,
    video_id: str,
    random_seed: int | None,
) -> tuple[BrowserPagePointerAction, ...]:
    interleaved: list[BrowserPagePointerAction] = []
    for action in comment_actions:
        interleaved.append(action)
        interleaved.append(
            _tiktok_challenge_close_followthrough_pointer_action(
                video_id=video_id,
                random_seed=random_seed,
            )
        )
        interleaved.append(
            _tiktok_challenge_visual_close_followthrough_pointer_action(
                video_id=video_id,
                random_seed=random_seed,
            )
        )
    return tuple(interleaved)


def _interleave_challenge_diagnostic_actions(
    comment_actions: Sequence[BrowserPagePointerAction],
    *,
    video_id: str,
    random_seed: int | None,
) -> tuple[BrowserPagePointerAction, ...]:
    interleaved: list[BrowserPagePointerAction] = []
    for action in comment_actions:
        interleaved.append(action)
        interleaved.append(
            _tiktok_challenge_visual_close_diagnostic_pointer_action(
                video_id=video_id,
                random_seed=random_seed,
            )
        )
    return tuple(interleaved)

def _tiktok_human_challenge_handoff_after_action_names() -> tuple[str, ...]:
    return (
        TIKTOK_CHALLENGE_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
        TIKTOK_CHALLENGE_VISUAL_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
    )


def _tiktok_comment_route_pointer_actions(
    *,
    video_id: str,
    random_seed: int | None,
) -> tuple[BrowserPagePointerAction, ...]:
    route_once = (
        _tiktok_open_comments_pointer_action(
            video_id=video_id,
            random_seed=random_seed,
            action_name=TIKTOK_OPEN_COMMENTS_POINTER_ACTION_NAME,
            wait_after_ms=2000,
        ),
        _tiktok_open_more_like_this_pointer_action(
            video_id=video_id,
            random_seed=random_seed,
        ),
        _tiktok_open_comments_pointer_action(
            video_id=video_id,
            random_seed=random_seed,
            action_name=TIKTOK_REOPEN_COMMENTS_POINTER_ACTION_NAME,
            wait_after_ms=3500,
        ),
    )
    return (*route_once, *route_once)


def _tiktok_dismiss_benign_overlay_pointer_action(
    *,
    video_id: str,
    random_seed: int | None,
) -> BrowserPagePointerAction:
    return BrowserPagePointerAction(
        action_name=TIKTOK_DISMISS_BENIGN_OVERLAY_POINTER_ACTION_NAME,
        candidate_selector=(
            'button,[role="button"],[aria-label],[title],[data-e2e],'
            '[data-testid],[data-test-id]'
        ),
        text_markers=("got it", "not now", "continue in browser", "maybe later"),
        page_text_markers=(
            "scroll, use the",
            "browse your feed",
            "got it",
            "press ok",
            "tap ok",
            "okay",
            "continue in browser",
            "open app",
        ),
        exact_text_markers=("ok", "okay"),
        wait_after_ms=1500,
        move_steps_min=6,
        move_steps_max=12,
        target_fraction_min=0.35,
        target_fraction_max=0.65,
        prefer_top_right=False,
        random_seed=_stable_pointer_seed(
            video_id=video_id,
            random_seed=random_seed,
            action_name=TIKTOK_DISMISS_BENIGN_OVERLAY_POINTER_ACTION_NAME,
        ),
    )


def _tiktok_retry_visible_error_pointer_action(
    *,
    video_id: str,
    random_seed: int | None,
) -> BrowserPagePointerAction:
    return BrowserPagePointerAction(
        action_name=TIKTOK_RETRY_VISIBLE_ERROR_POINTER_ACTION_NAME,
        candidate_selector=(
            'button,[role="button"],[aria-label],[title],[data-e2e],'
            '[data-testid],[data-test-id],a'
        ),
        text_markers=("retry", "retry again", "try again", "reload"),
        page_text_markers=(
            "retry",
            "retry again",
            "try again",
            "something went wrong",
            "couldn't load",
            "could not load",
            "failed to load",
        ),
        wait_after_ms=2500,
        move_steps_min=6,
        move_steps_max=12,
        target_fraction_min=0.35,
        target_fraction_max=0.65,
        random_seed=_stable_pointer_seed(
            video_id=video_id,
            random_seed=random_seed,
            action_name=TIKTOK_RETRY_VISIBLE_ERROR_POINTER_ACTION_NAME,
        ),
    )


def _tiktok_challenge_close_diagnostic_pointer_action(
    *,
    video_id: str,
    random_seed: int | None,
) -> BrowserPagePointerAction:
    return _tiktok_challenge_close_pointer_action(
        video_id=video_id,
        random_seed=random_seed,
        action_name=TIKTOK_CHALLENGE_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME,
    )


def _tiktok_challenge_close_followthrough_pointer_action(
    *,
    video_id: str,
    random_seed: int | None,
) -> BrowserPagePointerAction:
    return _tiktok_challenge_close_pointer_action(
        video_id=video_id,
        random_seed=random_seed,
        action_name=TIKTOK_CHALLENGE_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
    )


def _tiktok_challenge_close_pointer_action(
    *,
    video_id: str,
    random_seed: int | None,
    action_name: str,
) -> BrowserPagePointerAction:
    return BrowserPagePointerAction(
        action_name=action_name,
        candidate_selector=(
            "button,[role=\"button\"],[aria-label],[title],[data-e2e],"
            "[data-testid],[data-test-id],[class]"
        ),
        text_markers=("close", "dismiss"),
        page_text_markers=TIKTOK_CHALLENGE_TEXT_MARKERS,
        exact_text_markers=("x", "×"),
        wait_after_ms=2000,
        move_steps_min=6,
        move_steps_max=12,
        target_fraction_min=0.35,
        target_fraction_max=0.65,
        prefer_top_right=True,
        visual_top_right_x_fallback=True,
        visual_x_target_zone="center_modal",
        # Geometric fallback caused false X-click claims on TikTok challenge modals.
        visual_x_geometric_fallback=False,
        post_click_absent_text_markers=TIKTOK_CHALLENGE_TEXT_MARKERS,
        post_click_visual_target_absence_check=True,
        random_seed=_stable_pointer_seed(
            video_id=video_id,
            random_seed=random_seed,
            action_name=action_name,
        ),
    )


def _tiktok_challenge_visual_close_diagnostic_pointer_action(
    *,
    video_id: str,
    random_seed: int | None,
) -> BrowserPagePointerAction:
    return _tiktok_challenge_visual_close_pointer_action(
        video_id=video_id,
        random_seed=random_seed,
        action_name=TIKTOK_CHALLENGE_VISUAL_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME,
    )


def _tiktok_challenge_visual_close_followthrough_pointer_action(
    *,
    video_id: str,
    random_seed: int | None,
) -> BrowserPagePointerAction:
    return _tiktok_challenge_visual_close_pointer_action(
        video_id=video_id,
        random_seed=random_seed,
        action_name=TIKTOK_CHALLENGE_VISUAL_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
        stop_sequence_on_failed_post_click_verification=True,
    )


def _tiktok_challenge_visual_close_pointer_action(
    *,
    video_id: str,
    random_seed: int | None,
    action_name: str,
    require_visible_challenge_text: bool = True,
    stop_sequence_on_failed_post_click_verification: bool = False,
) -> BrowserPagePointerAction:
    return BrowserPagePointerAction(
        action_name=action_name,
        candidate_selector=(
            "button,[role=\"button\"],[aria-label],[title],[data-e2e],"
            "[data-testid],[data-test-id],[class]"
        ),
        text_markers=("__tiktok_visual_close_diagnostic_never_dom_match__",),
        page_text_markers=(
            TIKTOK_CHALLENGE_TEXT_MARKERS if require_visible_challenge_text else ()
        ),
        exact_text_markers=("__tiktok_visual_close_diagnostic_never_dom_match__",),
        wait_after_ms=2000,
        move_steps_min=6,
        move_steps_max=12,
        target_fraction_min=0.35,
        target_fraction_max=0.65,
        prefer_top_right=True,
        visual_top_right_x_fallback=True,
        visual_x_target_zone="center_modal",
        # Geometric fallback caused false X-click claims on TikTok challenge modals.
        visual_x_geometric_fallback=False,
        post_click_absent_text_markers=TIKTOK_CHALLENGE_TEXT_MARKERS,
        post_click_visual_target_absence_check=True,
        stop_sequence_on_failed_post_click_verification=(
            stop_sequence_on_failed_post_click_verification
        ),
        random_seed=_stable_pointer_seed(
            video_id=video_id,
            random_seed=random_seed,
            action_name=action_name,
        ),
    )

def _tiktok_open_comments_pointer_action(
    *,
    video_id: str,
    random_seed: int | None,
    action_name: str,
    wait_after_ms: int,
) -> BrowserPagePointerAction:
    return BrowserPagePointerAction(
        action_name=action_name,
        candidate_selector=(
            '[data-e2e="comment-icon"],[data-e2e*="comment"],button,[role="button"],a'
        ),
        text_markers=("comment", "comments"),
        wait_after_ms=wait_after_ms,
        move_steps_min=6,
        move_steps_max=12,
        target_fraction_min=0.35,
        target_fraction_max=0.65,
        stop_wait_on_observed_response=True,
        observed_response_wait_poll_ms=100,
        random_seed=_stable_pointer_seed(
            video_id=video_id,
            random_seed=random_seed,
            action_name=action_name,
        ),
    )


def _tiktok_open_more_like_this_pointer_action(
    *,
    video_id: str,
    random_seed: int | None,
) -> BrowserPagePointerAction:
    return BrowserPagePointerAction(
        action_name=TIKTOK_OPEN_MORE_LIKE_THIS_POINTER_ACTION_NAME,
        candidate_selector=(
            '[role="tab"],[aria-selected],button,[role="button"],a,'
            '[data-e2e*="more-like"],[data-e2e*="more_like"],'
            '[data-e2e*="you-may-like"],[data-e2e*="you_may_like"],'
            '[data-testid*="more-like"],[data-testid*="you-may-like"],'
            '[data-test-id*="more-like"],[data-test-id*="you-may-like"],'
            'div,span,p'
        ),
        text_markers=(
            "more like this",
            "more-like-this",
            "more_like_this",
            "you may like",
            "you-may-like",
            "you_may_like",
        ),
        exact_text_markers=("more like this", "you may like"),
        wait_after_ms=2000,
        move_steps_min=6,
        move_steps_max=12,
        target_fraction_min=0.35,
        target_fraction_max=0.65,
        prefer_smallest_match=True,
        random_seed=_stable_pointer_seed(
            video_id=video_id,
            random_seed=random_seed,
            action_name=TIKTOK_OPEN_MORE_LIKE_THIS_POINTER_ACTION_NAME,
        ),
    )


def _stable_pointer_seed(*, video_id: str, random_seed: int | None, action_name: str) -> int:
    base_seed = random_seed if random_seed is not None else 0
    material = f"{base_seed}:{video_id}:{action_name}"
    return int(sha256(material.encode("utf-8")).hexdigest()[:16], 16)


def _build_probe_cadence_plan(
    *,
    video_count: int,
    min_gap_seconds: float,
    max_gap_seconds: float,
    window_seconds: float | None,
    random_seed: int | None,
):
    if window_seconds is None:
        window_seconds = max_gap_seconds * max(0, video_count - 1)
    return build_cadence_plan(
        slot_count=video_count,
        mode="bounded_jitter",
        delay_seconds=0.0,
        window_seconds=window_seconds,
        min_gap_seconds=min_gap_seconds,
        max_gap_seconds=max_gap_seconds,
        random_seed=random_seed,
    )


def _cadence_row_from_capture(
    *,
    item_struct: JsonObject,
    creator_handle: str,
    video_url: str,
    video_id: str,
    capture_result: BrowserPageObservationSuccess,
    observed_utc: str,
    grid_candidate: JsonObject,
    blocker_triage: TikTokBlockerTriage,
    comment_response_cap: int = TIKTOK_COMMENT_LIST_RESPONSE_CAP,
    challenge_close_action: JsonObject | None = None,
    challenge_close_followthrough_allowed: bool = False,
    subtitle_fetcher: SubtitleFetchFn | None = None,
) -> JsonObject:
    subtitle_infos = _sanitize_subtitle_infos(_subtitle_infos_from_item_struct(item_struct))
    subtitle_capture = _subtitle_capture_from_item_struct(
        item_struct,
        subtitle_fetcher=subtitle_fetcher or _fetch_subtitle_webvtt,
    )
    matched_comment_response_count = sum(
        1
        for response in capture_result.responses
        if _is_page_owned_comment_list_response(response)
    )
    comment_list_responses = _page_owned_comment_list_responses(
        capture_result,
        response_cap=comment_response_cap,
    )
    dom_visible_comments = _dom_visible_comment_candidates(capture_result)
    challenge_close_action = _as_dict(challenge_close_action)
    challenge_close_clicked = _first_bool(challenge_close_action.get("clicked")) is True
    challenge_close_accepted = _challenge_close_accepted(challenge_close_action)
    capture_receipt = {
        "page_url_sha256": _sha256_text(video_url),
        "final_url_sha256": _sha256_text(capture_result.final_url),
        "response_count": len(capture_result.responses),
        "blocker_triage": _blocker_triage_receipt(blocker_triage),
        "benign_overlay_action": _benign_overlay_action_summary(capture_result),
        "comment_action": _comment_action_summary(capture_result),
        "matched_comment_response_count": matched_comment_response_count,
        "admitted_comment_response_count": len(comment_list_responses),
        "comment_response_cap": comment_response_cap,
        "dom_visible_comment_candidate_count": len(dom_visible_comments),
        "warning_count": len(capture_result.warning_notes),
        "limitation_count": len(capture_result.limitation_notes),
    }
    pointer_chronology = _pointer_action_chronology(capture_result)
    if pointer_chronology:
        capture_receipt["pointer_action_chronology"] = pointer_chronology
    challenge_close_attempts = _challenge_close_attempts(capture_result)
    if challenge_close_attempts:
        capture_receipt["challenge_close_attempts"] = challenge_close_attempts
    human_handoff_attempts = _human_challenge_handoff_attempts(capture_result)
    if human_handoff_attempts:
        capture_receipt["human_challenge_handoff_attempts"] = human_handoff_attempts
        capture_receipt["human_challenge_handoff"] = True
    if dom_visible_comments and not comment_list_responses:
        capture_receipt["comment_capture_fallback"] = "dom_visible_comment_candidates_v0"
    if challenge_close_action:
        capture_receipt["challenge_close_action"] = challenge_close_action
        if challenge_close_clicked:
            capture_receipt["challenge_close_accepted"] = challenge_close_accepted
    if challenge_close_followthrough_allowed and challenge_close_accepted:
        capture_receipt["challenge_close_followthrough"] = True
    return {
        "video_id": video_id,
        "url_path": urlparse(video_url).path,
        "status": "completed",
        "creator_handle": creator_handle,
        "grid_candidate": grid_candidate,
        "comment_responses": [
            _comment_response_from_page_response(response, observed_utc=observed_utc)
            for response in comment_list_responses
        ],
        "dom_visible_comment_candidates": dom_visible_comments,
        "hydration": {
            "subtitle_info_count": len(subtitle_infos),
            "subtitle_infos_sanitized": subtitle_infos,
        },
        "subtitle": subtitle_capture,
        "capture_receipt": capture_receipt,
    }


def _page_owned_comment_list_responses(
    capture_result: BrowserPageObservationSuccess,
    *,
    response_cap: int = TIKTOK_COMMENT_LIST_RESPONSE_CAP,
) -> list[BrowserPageResponse]:
    responses: list[BrowserPageResponse] = []
    for response in capture_result.responses:
        if not _is_page_owned_comment_list_response(response):
            continue
        responses.append(response)
        if len(responses) >= response_cap:
            break
    return responses


def _dom_visible_comment_candidates(
    capture_result: BrowserPageObservationSuccess,
) -> list[JsonObject]:
    observation = _as_dict(capture_result.dom_observation)
    candidates: list[JsonObject] = []
    seen: set[str] = set()
    for raw in _as_list(observation.get("visible_comment_candidates")):
        item = _as_dict(raw)
        text = _clean_dom_comment_text(_first_str(item.get("text"), ""))
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        candidate = {
            "source_order": len(candidates),
            "text": text,
            "text_sha256": _sha256_text(text),
            "text_char_count": len(text),
            "selector": _first_str(item.get("selector")),
            "capture_posture": "visible_dom_after_comment_route",
        }
        assert_no_sensitive_tiktok_material(candidate)
        candidates.append(_drop_none(candidate))
        if len(candidates) >= TIKTOK_DOM_VISIBLE_COMMENT_CANDIDATE_CAP:
            break
    return candidates


def _clean_dom_comment_text(value: str | None) -> str:
    text = re.sub(r"\s+", " ", value or "").strip()
    if not text:
        return ""
    lowered = text.lower()
    if lowered in {"comments", "you may like", "log in to comment"}:
        return ""
    if _COUNT_ONLY_TEXT_RE.fullmatch(lowered):
        return ""
    if any(marker in lowered for marker in ("drag the slider", "verify to continue", "captcha")):
        return ""
    text = _URL_IN_TEXT_RE.sub("[url redacted]", text)
    if len(text) > TIKTOK_DOM_VISIBLE_COMMENT_TEXT_MAX_CHARS:
        text = text[:TIKTOK_DOM_VISIBLE_COMMENT_TEXT_MAX_CHARS].rstrip()
    return text


def _comment_action_summary(capture_result: BrowserPageObservationSuccess) -> JsonObject:
    metadata = _as_dict(capture_result.metadata)
    action_sequence: list[JsonObject] = []
    for action in _as_list(metadata.get("post_load_pointer_actions")):
        summary = _pointer_action_summary(_as_dict(action))
        if not summary:
            continue
        if summary.get("action_name") in {
            TIKTOK_CHALLENGE_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME,
            TIKTOK_CHALLENGE_VISUAL_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME,
            TIKTOK_CHALLENGE_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
            TIKTOK_CHALLENGE_VISUAL_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
            TIKTOK_DISMISS_BENIGN_OVERLAY_POINTER_ACTION_NAME,
            TIKTOK_RETRY_VISIBLE_ERROR_POINTER_ACTION_NAME,
        }:
            continue
        action_sequence.append(summary)
    if len(action_sequence) > 1:
        return {
            "sequence_name": TIKTOK_COMMENT_SURFACE_TOGGLE_POINTER_SEQUENCE_NAME,
            "action_count": len(action_sequence),
            "action_sequence": action_sequence,
            "clicked_all_targets": all(
                action.get("target_found") is True and action.get("clicked") is True
                for action in action_sequence
            ),
        }
    if len(action_sequence) == 1:
        return action_sequence[0]
    if _as_list(metadata.get("post_load_pointer_actions")):
        return {}

    action = _as_dict(metadata.get("post_load_pointer_action"))
    if action:
        return _pointer_action_summary(action)

    legacy_action = _as_dict(_as_dict(capture_result.dom_observation).get("comment_action"))
    if not legacy_action:
        return {}
    return _drop_none(
        {
            "candidate_count": _first_int(legacy_action.get("candidate_count")),
            "clicked": _first_bool(legacy_action.get("clicked")),
        }
    )


def _pointer_action_chronology(
    capture_result: BrowserPageObservationSuccess,
) -> list[JsonObject]:
    metadata = _as_dict(capture_result.metadata)
    actions: list[JsonObject] = []
    for action in _as_list(metadata.get("post_load_pointer_actions")):
        summary = _pointer_action_summary(_as_dict(action))
        if summary:
            actions.append(summary)
    if actions:
        return actions
    action = _as_dict(metadata.get("post_load_pointer_action"))
    summary = _pointer_action_summary(action) if action else {}
    return [summary] if summary else []


def _human_challenge_handoff_attempts(
    capture_result: BrowserPageObservationSuccess,
) -> list[JsonObject]:
    metadata = _as_dict(capture_result.metadata)
    return [
        _as_dict(attempt)
        for attempt in _as_list(metadata.get("human_challenge_handoff_attempts"))
        if _as_dict(attempt)
    ]


def _challenge_close_attempts(
    capture_result: BrowserPageObservationSuccess,
) -> list[JsonObject]:
    challenge_action_names = {
        TIKTOK_CHALLENGE_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME,
        TIKTOK_CHALLENGE_VISUAL_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME,
        TIKTOK_CHALLENGE_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
        TIKTOK_CHALLENGE_VISUAL_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
    }
    return [
        action
        for action in _pointer_action_chronology(capture_result)
        if action.get("action_name") in challenge_action_names
    ]

def _benign_overlay_action_summary(
    capture_result: BrowserPageObservationSuccess,
) -> JsonObject:
    metadata = _as_dict(capture_result.metadata)
    for action in _as_list(metadata.get("post_load_pointer_actions")):
        summary = _pointer_action_summary(_as_dict(action))
        if summary.get("action_name") == TIKTOK_DISMISS_BENIGN_OVERLAY_POINTER_ACTION_NAME:
            return summary
    return {}


def _challenge_close_action_summary(
    capture_result: BrowserPageObservationSuccess,
) -> JsonObject:
    metadata = _as_dict(capture_result.metadata)
    diagnostic_summaries: list[JsonObject] = []
    diagnostic_names = {
        TIKTOK_CHALLENGE_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME,
        TIKTOK_CHALLENGE_VISUAL_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME,
        TIKTOK_CHALLENGE_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
        TIKTOK_CHALLENGE_VISUAL_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
    }
    for action in _as_list(metadata.get("post_load_pointer_actions")):
        summary = _pointer_action_summary(_as_dict(action))
        if summary.get("action_name") in diagnostic_names:
            diagnostic_summaries.append(summary)
    for summary in diagnostic_summaries:
        if _challenge_close_accepted(summary):
            return summary
    for summary in reversed(diagnostic_summaries):
        if _first_bool(summary.get("clicked")) is True:
            return summary
    for summary in diagnostic_summaries:
        if summary.get("action_name") == TIKTOK_CHALLENGE_VISUAL_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME:
            return summary
    return diagnostic_summaries[0] if diagnostic_summaries else {}


def _pointer_action_summary(action: JsonObject) -> JsonObject:
    return _drop_none(
        {
            "action_name": _first_str(action.get("action_name")),
            "candidate_count": _first_int(action.get("candidate_count")),
            "matched_count": _first_int(action.get("matched_count")),
            "target_found": _first_bool(action.get("target_found")),
            "clicked": _first_bool(action.get("clicked")),
            "move_steps": _first_int(action.get("move_steps")),
            "wait_ms": _first_int(action.get("wait_ms")),
            "observed_response_count_before": _first_int(
                action.get("observed_response_count_before")
            ),
            "observed_response_count_after": _first_int(
                action.get("observed_response_count_after")
            ),
            "observed_response_delta": _first_int(action.get("observed_response_delta")),
            "observed_response_seen": _first_bool(action.get("observed_response_seen")),
            "target_kind": _first_str(action.get("target_kind")),
            "page_text_gate_matched": _first_bool(action.get("page_text_gate_matched")),
            "page_text_matched_marker": _first_str(
                action.get("page_text_matched_marker")
            ),
            "selection_strategy": _first_str(action.get("selection_strategy")),
            "failure": _first_str(action.get("failure")),
            "target_box": _as_dict(action.get("target_box")) or None,
            "click_point": _as_dict(action.get("click_point")) or None,
            "visual_fallback_attempted": _first_bool(
                action.get("visual_fallback_attempted")
            ),
            "visual_fallback_target_found": _first_bool(
                action.get("visual_fallback_target_found")
            ),
            "visual_fallback_candidate_count": _first_int(
                action.get("visual_fallback_candidate_count")
            ),
            "visual_fallback_zone_candidate_count": _first_int(
                action.get("visual_fallback_zone_candidate_count")
            ),
            "visual_fallback_confidence": _first_float(
                action.get("visual_fallback_confidence")
            ),
            "visual_fallback_screenshot_sha256": _first_str(
                action.get("visual_fallback_screenshot_sha256")
            ),
            "visual_fallback_crop_box": _as_dict(
                action.get("visual_fallback_crop_box")
            ) or None,
            "visual_fallback_target_zone": _first_str(
                action.get("visual_fallback_target_zone")
            ),
            "visual_fallback_geometric_target": _first_bool(
                action.get("visual_fallback_geometric_target")
            ),
            "visual_fallback_failure": _first_str(
                action.get("visual_fallback_failure")
            ),
            "post_click_absence_checked": _first_bool(
                action.get("post_click_absence_checked")
            ),
            "post_click_absence_marker_count": _first_int(
                action.get("post_click_absence_marker_count")
            ),
            "post_click_absence_verified": _first_bool(
                action.get("post_click_absence_verified")
            ),
            "post_click_absence_matched_marker": _first_str(
                action.get("post_click_absence_matched_marker")
            ),
            "post_click_absence_failure": _first_str(
                action.get("post_click_absence_failure")
            ),
            "post_click_visual_check_attempted": _first_bool(
                action.get("post_click_visual_check_attempted")
            ),
            "post_click_visual_target_found": _first_bool(
                action.get("post_click_visual_target_found")
            ),
            "post_click_visual_target_absent": _first_bool(
                action.get("post_click_visual_target_absent")
            ),
            "post_click_visual_candidate_count": _first_int(
                action.get("post_click_visual_candidate_count")
            ),
            "post_click_visual_zone_candidate_count": _first_int(
                action.get("post_click_visual_zone_candidate_count")
            ),
            "post_click_visual_confidence": _first_float(
                action.get("post_click_visual_confidence")
            ),
            "post_click_visual_screenshot_sha256": _first_str(
                action.get("post_click_visual_screenshot_sha256")
            ),
            "post_click_visual_crop_box": _as_dict(
                action.get("post_click_visual_crop_box")
            ) or None,
            "post_click_visual_target_box": _as_dict(
                action.get("post_click_visual_target_box")
            ) or None,
            "post_click_visual_failure": _first_str(
                action.get("post_click_visual_failure")
            ),
        }
    )


def _is_page_owned_comment_list_response(response: BrowserPageResponse) -> bool:
    if not is_tiktok_comment_list_url(response.final_url or response.requested_url):
        return False
    method = (response.request_method or "").upper()
    if method and method != "GET":
        return False
    resource_type = (response.resource_type or "").lower()
    if resource_type and resource_type not in {"fetch", "xhr"}:
        return False
    return True

def _comment_response_from_page_response(
    response: BrowserPageResponse, *, observed_utc: str
) -> JsonObject:
    body_text = response.body_text or ""
    result: JsonObject = {
        "observed_utc": observed_utc,
        "status": response.status,
        "ok": response.ok,
        "url_summary": _url_summary(response.final_url or response.requested_url),
        "body_assessment": _comment_body_assessment(body_text),
        "limitation_notes": list(response.limitation_notes),
    }
    if response.request_method is not None:
        result["request_method"] = response.request_method
    if response.resource_type is not None:
        result["resource_type"] = response.resource_type
    return result


def _comment_body_assessment(body_text: str) -> JsonObject:
    body_bytes = body_text.encode("utf-8")
    assessment: JsonObject = {
        "body_sha256": sha256(body_bytes).hexdigest() if body_text else None,
        "body_byte_count": len(body_bytes),
        "json_parse_ok": False,
        "comment_count": 0,
        "envelope": {},
        "field_coverage": {},
        "comments": [],
    }
    if not body_text:
        return assessment

    try:
        payload = json.loads(body_text)
    except json.JSONDecodeError:
        assessment["parse_error"] = "json_decode_error"
        return assessment
    if not isinstance(payload, dict):
        assessment["parse_error"] = "json_root_not_object"
        return assessment

    comments = [_normalize_comment_item(item) for item in _as_list(payload.get("comments"))]
    comments = [comment for comment in comments if comment]
    envelope = {
        "cursor": _first_int(payload.get("cursor")),
        "has_more": _first_bool(payload.get("has_more")),
        "total": _first_int(payload.get("total")),
        "status_code": _first_int(payload.get("status_code")),
    }
    assessment.update(
        {
            "json_parse_ok": True,
            "comment_count": len(comments),
            "envelope": {key: value for key, value in envelope.items() if value is not None},
            "field_coverage": _comment_field_coverage(comments),
            "comments": comments,
        }
    )
    return assessment


def _normalize_comment_item(item: Any) -> JsonObject | None:
    if not isinstance(item, dict):
        return None
    user = item.get("user") if isinstance(item.get("user"), dict) else {}
    comment = {
        "cid": _first_str(item.get("cid"), item.get("comment_id")),
        "text": _first_str(item.get("text"), ""),
        "create_time": _first_int(item.get("create_time"), item.get("createTime")),
        "digg_count": _first_int(item.get("digg_count"), item.get("diggCount")),
        "reply_comment_total": _first_int(
            item.get("reply_comment_total"),
            item.get("replyCommentTotal"),
        ),
        "user": {
            "uid": _first_str(user.get("uid")),
            "unique_id": _first_str(user.get("unique_id"), user.get("uniqueId")),
            "nickname": _first_str(user.get("nickname")),
        },
    }
    return _drop_none(comment)


def _comment_field_coverage(comments: Sequence[JsonObject]) -> JsonObject:
    return {
        "cid": any(comment.get("cid") for comment in comments),
        "text": any(comment.get("text") for comment in comments),
        "create_time": any(comment.get("create_time") is not None for comment in comments),
        "digg_count": any(comment.get("digg_count") is not None for comment in comments),
        "reply_comment_total": any(
            comment.get("reply_comment_total") is not None for comment in comments
        ),
        "user.uid": any(_as_dict(comment.get("user")).get("uid") for comment in comments),
        "user.unique_id": any(
            _as_dict(comment.get("user")).get("unique_id") for comment in comments
        ),
        "user.nickname": any(
            _as_dict(comment.get("user")).get("nickname") for comment in comments
        ),
    }


def _grid_candidate_from_item_struct(
    item_struct: JsonObject,
    *,
    creator_handle: str,
    video_url: str,
) -> JsonObject:
    video_id = _first_str(item_struct.get("id"), _video_id_from_tiktok_url(video_url)) or ""
    create_time = _first_int(item_struct.get("createTime"), item_struct.get("create_time"))
    item = {
        "id": video_id,
        "desc": _first_str(item_struct.get("desc"), ""),
        "createTime": create_time,
        "stats": _normalize_stats(_as_dict(item_struct.get("stats"))),
        "author": _normalize_author(_as_dict(item_struct.get("author")), creator_handle),
        "music": _normalize_music(_as_dict(item_struct.get("music"))),
        "url_path": urlparse(video_url).path,
        "source_response_path": urlparse(video_url).path,
        "source_response_url_sha256": _sha256_text(video_url),
        "decoded_aweme_id_create_time_utc": decoded_aweme_id_create_time_utc(video_id),
    }
    return _drop_none(item)


def _normalize_stats(stats: JsonObject) -> JsonObject:
    return {
        "playCount": _first_int(stats.get("playCount"), stats.get("play_count"), 0),
        "diggCount": _first_int(stats.get("diggCount"), stats.get("digg_count"), 0),
        "commentCount": _first_int(stats.get("commentCount"), stats.get("comment_count"), 0),
        "shareCount": _first_int(stats.get("shareCount"), stats.get("share_count"), 0),
        "collectCount": _first_int(stats.get("collectCount"), stats.get("collect_count"), 0),
    }


def _normalize_author(author: JsonObject, creator_handle: str) -> JsonObject:
    return _drop_none(
        {
            "id": _first_str(author.get("id"), author.get("uid")),
            "uniqueId": _first_str(author.get("uniqueId"), author.get("unique_id"), creator_handle),
            "nickname": _first_str(author.get("nickname")),
        }
    )


def _normalize_music(music: JsonObject) -> JsonObject:
    return _drop_none(
        {
            "id": _first_str(music.get("id")),
            "title": _first_str(music.get("title")),
            "authorName": _first_str(music.get("authorName"), music.get("author_name")),
            "duration": _first_int(music.get("duration")),
        }
    )


def _sanitize_subtitle_infos(infos: Sequence[Any]) -> list[JsonObject]:
    sanitized: list[JsonObject] = []
    for info in infos:
        if not isinstance(info, dict):
            continue
        sanitized.append(
            _drop_none(
                {
                    "Format": _first_str(info.get("Format"), info.get("format")),
                    "LanguageCodeName": _first_str(
                        info.get("LanguageCodeName"),
                        info.get("languageCodeName"),
                        info.get("language_code_name"),
                    ),
                    "LanguageID": _first_str(
                        info.get("LanguageID"),
                        info.get("languageID"),
                        info.get("language_id"),
                    ),
                    "Size": _first_int(info.get("Size"), info.get("size")),
                    "Source": _first_str(info.get("Source"), info.get("source")),
                    "Version": _first_str(info.get("Version"), info.get("version")),
                    "url_present_but_redacted": bool(
                        info.get("Url") or info.get("url") or info.get("URL")
                    ),
                }
            )
        )
    return sanitized


def _subtitle_infos_from_item_struct(item_struct: JsonObject) -> Sequence[Any]:
    video = item_struct.get("video") if isinstance(item_struct.get("video"), dict) else {}
    for candidate in (
        video.get("subtitleInfos"),
        video.get("subtitle_infos"),
        item_struct.get("subtitleInfos"),
        item_struct.get("subtitle_infos"),
    ):
        if isinstance(candidate, list):
            return candidate
    return []


def _subtitle_capture_from_item_struct(
    item_struct: JsonObject,
    *,
    subtitle_fetcher: SubtitleFetchFn,
) -> JsonObject:
    subtitle_url = _subtitle_url_from_item_struct(item_struct)
    if subtitle_url is None:
        return {
            "attempted": False,
            "success": False,
            "reason": "no_subtitle_url_in_hydration_v0",
        }
    url_sha256 = _sha256_text(subtitle_url)
    base: JsonObject = {
        "attempted": False,
        "success": False,
        "subtitle_url_sha256": url_sha256,
        "subtitle_url_length": len(subtitle_url),
    }
    if not _is_supported_subtitle_url(subtitle_url):
        base["reason"] = "unsupported_subtitle_url_host_live_probe_v0"
        assert_no_sensitive_tiktok_material(base)
        return base

    base["attempted"] = True
    try:
        body = subtitle_fetcher(subtitle_url)
    except Exception:
        base["reason"] = "subtitle_body_fetch_failed_live_probe_v0"
        assert_no_sensitive_tiktok_material(base)
        return base

    body = body[: TIKTOK_SUBTITLE_WEBVTT_MAX_BYTES + 1]
    base["body_sha256"] = sha256(body).hexdigest()
    base["body_byte_count"] = len(body)
    if len(body) > TIKTOK_SUBTITLE_WEBVTT_MAX_BYTES:
        base["reason"] = "subtitle_body_size_cap_exceeded_live_probe_v0"
        assert_no_sensitive_tiktok_material(base)
        return base

    try:
        cues = parse_webvtt_cues(body)
    except ValueError:
        base["reason"] = "subtitle_body_parse_failed_live_probe_v0"
        assert_no_sensitive_tiktok_material(base)
        return base

    transcript_text = "\n".join(cue.text for cue in cues)
    result = {
        **base,
        "success": True,
        "reason": "source_native_webvtt_captured_live_probe_v0",
        "parsed_webvtt": {
            "cue_count": len(cues),
            "transcript_char_count": len(transcript_text),
            "transcript_text_sha256": _sha256_text(transcript_text),
            "transcript_text": transcript_text,
            "cues": [
                {
                    "start_ms": cue.start_ms,
                    "end_ms": cue.end_ms,
                    "start": _format_webvtt_timestamp_ms(cue.start_ms),
                    "end": _format_webvtt_timestamp_ms(cue.end_ms),
                    "text": cue.text,
                }
                for cue in cues
            ],
        },
    }
    assert_no_sensitive_tiktok_material(result)
    return result


def _subtitle_url_from_item_struct(item_struct: JsonObject) -> str | None:
    for info in _subtitle_infos_from_item_struct(item_struct):
        if not isinstance(info, dict):
            continue
        url = _first_str(info.get("Url"), info.get("url"), info.get("URL"))
        if url:
            return url
    return None


def _is_supported_subtitle_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False
    host = (parsed.hostname or "").lower()
    if not host:
        return False
    return any(
        _host_matches_suffix(host, suffix)
        for suffix in TIKTOK_SUBTITLE_ALLOWED_HOST_SUFFIXES
    )


def _host_matches_suffix(host: str, suffix: str) -> bool:
    normalized_host = host.lower().rstrip(".")
    normalized_suffix = suffix.lower().rstrip(".")
    return normalized_host == normalized_suffix or normalized_host.endswith(
        f".{normalized_suffix}"
    )


class _TikTokSubtitleRedirectHandler(HTTPRedirectHandler):
    def redirect_request(
        self,
        req: object,
        fp: object,
        code: int,
        msg: str,
        headers: object,
        newurl: str,
    ) -> object:
        if not _is_supported_subtitle_url(newurl):
            raise ValueError("unsupported subtitle redirect host")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _fetch_subtitle_webvtt(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    opener = build_opener(_TikTokSubtitleRedirectHandler)
    with opener.open(request, timeout=TIKTOK_SUBTITLE_FETCH_TIMEOUT_SECONDS) as response:
        final_url = ""
        try:
            final_url = str(response.geturl())
        except Exception:
            final_url = ""
        if final_url and not _is_supported_subtitle_url(final_url):
            raise ValueError("unsupported subtitle final host")
        return response.read(TIKTOK_SUBTITLE_WEBVTT_MAX_BYTES + 1)


def _format_webvtt_timestamp_ms(value: int) -> str:
    hours, remainder = divmod(max(0, int(value)), 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, millis = divmod(remainder, 1_000)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{millis:03}"

def _extract_item_struct(dom_observation: object) -> JsonObject | None:
    observation = _as_dict(dom_observation)
    hydration_text = _first_str(observation.get("hydration_json_text"))
    if not hydration_text:
        return None
    try:
        payload = json.loads(hydration_text)
    except json.JSONDecodeError:
        return None
    found = _find_first_item_struct(payload)
    return found if isinstance(found, dict) else None


def _find_first_item_struct(value: Any) -> JsonObject | None:
    if isinstance(value, dict):
        item_info = value.get("itemInfo")
        if isinstance(item_info, dict) and isinstance(item_info.get("itemStruct"), dict):
            return item_info["itemStruct"]
        item_struct = value.get("itemStruct")
        if isinstance(item_struct, dict):
            return item_struct
        for child in value.values():
            found = _find_first_item_struct(child)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _find_first_item_struct(child)
            if found is not None:
                return found
    return None


def _failure_entry(
    *,
    video_url: str,
    video_id: str,
    observed_utc: str,
    reason: str,
    detail: str,
    blocker_triage: JsonObject | None = None,
) -> JsonObject:
    safe_detail = detail
    if reason.startswith("capture_failed:"):
        safe_detail = "capture failure detail redacted; hash retained"
    entry = {
        "video_id": video_id,
        "url_path": urlparse(video_url).path,
        "observed_utc": observed_utc,
        "reason": reason,
        "detail": safe_detail,
        "detail_sha256": _sha256_text(detail),
        "detail_length": len(detail),
        "page_url_sha256": _sha256_text(video_url),
    }
    if blocker_triage is not None:
        entry["blocker_triage"] = blocker_triage
    assert_no_sensitive_tiktok_material(entry)
    return entry


def _capture_contract(
    *,
    session_mode: AuthenticatedSessionMode | None,
    logged_out: bool = False,
    browser_backend: str = TIKTOK_BROWSER_BACKEND_DEFAULT,
    required_harness_proxy_profile_posture: str | HarnessProxyProfilePosture | None = None,
    cloakbrowser_humanize: bool = False,
    human_challenge_handoff: bool = False,
    human_challenge_handoff_timeout_seconds: float = TIKTOK_HUMAN_CHALLENGE_HANDOFF_TIMEOUT_SECONDS,
    allow_challenge_close_diagnostic: bool = False,
    allow_challenge_close_followthrough: bool = False,
) -> JsonObject:
    session_mode_value = (
        TIKTOK_LOGGED_OUT_SESSION_MODE
        if logged_out
        else session_mode.value if session_mode is not None else None
    )
    if session_mode_value is None:
        raise ValueError("session_mode is required unless logged_out is true")
    return {
        "browser_backend": browser_backend,
        "required_harness_proxy_profile_posture": (
            required_harness_proxy_profile_posture.value
            if isinstance(required_harness_proxy_profile_posture, HarnessProxyProfilePosture)
            else required_harness_proxy_profile_posture
        ),
        "cloakbrowser_humanize": cloakbrowser_humanize,
        "captcha_solving": False,
        "human_challenge_handoff_allowed": human_challenge_handoff,
        "human_challenge_handoff_counts_as_clean_capture": False,
        "human_challenge_handoff_timeout_seconds": human_challenge_handoff_timeout_seconds,
        "challenge_close_diagnostic_allowed": allow_challenge_close_diagnostic,
        "challenge_close_followthrough_allowed": allow_challenge_close_followthrough,
        "challenge_close_counts_as_success": False,
        "cookies_or_tokens_persisted": False,
        "direct_forged_api_calls": False,
        "dom_visible_comment_fallback": True,
        "page_owned_comment_list_response": True,
        "page_owned_video_navigation": True,
        "raw_comment_response_bodies_persisted": False,
        "raw_endpoint_urls_persisted": False,
        "raw_subtitle_bodies_persisted": False,
        "raw_subtitle_urls_persisted": False,
        "session_mode": session_mode_value,
        "logged_out_public": logged_out,
        "staging_only": True,
        "stop_on_challenge": True,
        "subtitle_tier": "source_native_webvtt_transcript_live_probe_v0",
    }


def _non_claims() -> list[str]:
    return [
        "not_cross_creator_ceiling_evidence_until_real_owner_gated_runs_are_completed",
        "not_product_or_judgment_extraction",
        "not_bulk_scale_capture",
        "not_raw_comment_body_preservation",
        "not_raw_subtitle_body_preservation",
    ]


def _url_summary(url: str) -> JsonObject:
    parsed = urlparse(url)
    query_keys = {key for key, _value in parse_qsl(parsed.query, keep_blank_values=True)}
    return {
        "path": parsed.path,
        "query_key_count": len(query_keys),
        "url_sha256": _sha256_text(url),
    }


def _normalize_profile_url(creator_profile_url: str, creator_handle: str) -> str:
    parsed = urlparse(creator_profile_url.strip())
    if parsed.scheme not in {"https", "http"}:
        raise ValueError("creator_profile_url must be an HTTP(S) URL")
    if parsed.netloc.lower() not in {"www.tiktok.com", "tiktok.com"}:
        raise ValueError("creator_profile_url must be a TikTok profile URL")
    path = parsed.path.rstrip("/")
    if path != f"/@{creator_handle}":
        raise ValueError("creator_profile_url path must match creator_handle")
    if parsed.query or parsed.fragment:
        raise ValueError("creator_profile_url must not include query or fragment")
    return f"https://www.tiktok.com/@{creator_handle}"


def _normalize_video_url(video_url: str, *, expected_handle: str) -> str:
    parsed = urlparse(video_url.strip())
    if parsed.scheme not in {"https", "http"}:
        raise ValueError("video_url must be an HTTP(S) URL")
    if parsed.netloc.lower() not in {"www.tiktok.com", "tiktok.com"}:
        raise ValueError("video_url must be a TikTok URL")
    if parsed.query or parsed.fragment:
        raise ValueError("video_url must not include query or fragment")
    match = _TIKTOK_VIDEO_URL_RE.match(parsed.path.rstrip("/"))
    if match is None:
        raise ValueError("video_url must have /@handle/video/<id> path")
    handle = _normalize_handle(match.group("handle"))
    if handle != expected_handle:
        raise ValueError("video_url handle must match creator_handle")
    return f"https://www.tiktok.com/{parsed.path.strip('/')}"


def _normalize_handle(handle: str) -> str:
    normalized = handle.strip().removeprefix("@")
    if not re.fullmatch(r"[A-Za-z0-9._]{2,64}", normalized):
        raise ValueError("creator_handle must be a TikTok handle, without URL syntax")
    return normalized


def _video_id_from_tiktok_url(video_url: str) -> str:
    path = urlparse(video_url).path.rstrip("/")
    match = _TIKTOK_VIDEO_URL_RE.match(path)
    if match is None:
        raise ValueError("video_url must have /@handle/video/<id> path")
    return match.group("video_id")


def _sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


def _as_dict(value: Any) -> JsonObject:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _first_str(*values: Any) -> str | None:
    for value in values:
        if value is None:
            continue
        if isinstance(value, str):
            stripped = value.strip()
            if stripped:
                return stripped
        elif isinstance(value, (int, float, bool)):
            return str(value)
    return None


def _first_int(*values: Any) -> int | None:
    for value in values:
        if value is None or isinstance(value, bool):
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return None


def _first_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if value in (0, 1):
        return bool(value)
    return None


def _first_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def _drop_none(value: JsonObject) -> JsonObject:
    result: JsonObject = {}
    for key, item in value.items():
        if item is None:
            continue
        if isinstance(item, dict):
            result[key] = _drop_none(item)
        else:
            result[key] = item
    return result


__all__ = [
    "TIKTOK_LIVE_BATCH_CADENCE_JSON_NAME",
    "TIKTOK_LIVE_BATCH_GRID_JSON_NAME",
    "TIKTOK_LIVE_BATCH_PROBE_SCHEMA_VERSION",
    "TIKTOK_CHALLENGE_AFTER_CLOSE_DIAGNOSTIC_REASON",
    "TIKTOK_CHALLENGE_AFTER_CLOSE_FOLLOWTHROUGH_REASON",
    "TIKTOK_CHALLENGE_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME",
    "TIKTOK_CHALLENGE_VISUAL_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME",
    "TIKTOK_CHALLENGE_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME",
    "TIKTOK_CHALLENGE_X_CLOSE_NOT_ACCEPTED_REASON",
    "TIKTOK_CHALLENGE_VISUAL_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME",
    "TIKTOK_CHALLENGE_CLOSE_DIAGNOSTIC_REASON",
    "TIKTOK_COMMENT_ROUTE_NO_RESPONSE_REASON",
    "TIKTOK_DISMISS_BENIGN_OVERLAY_POINTER_ACTION_NAME",
    "TIKTOK_COMMENT_SURFACE_TOGGLE_POINTER_SEQUENCE_NAME",
    "TIKTOK_VIDEO_DOM_EXTRACT_SCRIPT",
    "TikTokLiveBatchProbeOutputPaths",
    "detect_tiktok_challenge",
    "is_tiktok_comment_list_url",
    "run_tiktok_live_batch_probe",
    "write_tiktok_live_batch_probe_outputs",
]
