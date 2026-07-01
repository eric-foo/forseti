from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Callable, Sequence
from urllib.parse import parse_qsl, urlparse

from harness_utils import utc_now_z
from source_capture.adapters.browser_snapshot import (
    BrowserPageObservationEngine,
    BrowserPageObservationSuccess,
    BrowserPageResponse,
    BrowserSnapshotFailure,
    fetch_browser_page_observation_capture,
)
from source_capture.auth_state import AuthenticatedSessionMode, validate_auth_state_session_mode
from source_capture.cadence import build_cadence_plan
from source_capture.tiktok.admission import (
    assert_no_sensitive_tiktok_material,
    decoded_aweme_id_create_time_utc,
    json_dumps_sanitized,
)


TIKTOK_LIVE_BATCH_PROBE_SCHEMA_VERSION = "tiktok_live_batch_probe_v0"
TIKTOK_LIVE_BATCH_GRID_JSON_NAME = "tiktok_live_grid_result.json"
TIKTOK_LIVE_BATCH_CADENCE_JSON_NAME = "tiktok_live_cadence_result.json"

TIKTOK_VIDEO_DOM_EXTRACT_SCRIPT = r"""
() => {
  const hydration = document.querySelector('#__UNIVERSAL_DATA_FOR_REHYDRATION__');
  return {
    hydration_json_text: hydration ? hydration.textContent : null
  };
}
""".strip()

TIKTOK_OPEN_COMMENTS_POST_LOAD_SCRIPT = r"""
() => {
  const candidates = Array.from(document.querySelectorAll('button,[role="button"],a'));
  const target = candidates.find((node) => {
    const text = [
      node.getAttribute('aria-label'),
      node.getAttribute('title'),
      node.textContent
    ].filter(Boolean).join(' ').toLowerCase();
    return text.includes('comment') || text.includes('comments');
  });
  if (target && typeof target.click === 'function') {
    target.click();
    return { clicked: true };
  }
  return { clicked: false };
}
""".strip()

_TIKTOK_VIDEO_URL_RE = re.compile(r"^/@(?P<handle>[^/]+)/video/(?P<video_id>\d+)$")
_CHALLENGE_MARKERS = (
    "verify to continue",
    "drag the slider",
    "captcha",
    "security check",
    "too many attempts",
    "maximum number of attempts",
    "unusual traffic",
)


JsonObject = dict[str, Any]
SleepFn = Callable[[float], None]


@dataclass(frozen=True)
class TikTokLiveBatchProbeOutputPaths:
    grid_result_json_path: Path
    cadence_result_json_path: Path


def write_tiktok_live_batch_probe_outputs(
    *,
    creator_handle: str,
    creator_profile_url: str,
    video_urls: Sequence[str],
    state_label: str,
    session_mode: AuthenticatedSessionMode,
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
    cadence_min_gap_seconds: float = 75.0,
    cadence_max_gap_seconds: float = 120.0,
    cadence_window_seconds: float | None = None,
    random_seed: int | None = None,
    engine: BrowserPageObservationEngine | None = None,
    sleep_fn: SleepFn = time.sleep,
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
        auth_state_root=auth_state_root,
        timeout_seconds=timeout_seconds,
        wait_until=wait_until,
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        max_response_bytes=max_response_bytes,
        settle_seconds=settle_seconds,
        selector_timeout_seconds=selector_timeout_seconds,
        browser_channel=browser_channel,
        cadence_min_gap_seconds=cadence_min_gap_seconds,
        cadence_max_gap_seconds=cadence_max_gap_seconds,
        cadence_window_seconds=cadence_window_seconds,
        random_seed=random_seed,
        engine=engine,
        sleep_fn=sleep_fn,
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
    state_label: str,
    session_mode: AuthenticatedSessionMode,
    auth_state_root: Path | None = None,
    timeout_seconds: float = 30.0,
    wait_until: str = "domcontentloaded",
    viewport_width: int = 1280,
    viewport_height: int = 720,
    max_response_bytes: int = 5_000_000,
    settle_seconds: float = 2.0,
    selector_timeout_seconds: float = 5.0,
    browser_channel: str | None = None,
    cadence_min_gap_seconds: float = 75.0,
    cadence_max_gap_seconds: float = 120.0,
    cadence_window_seconds: float | None = None,
    random_seed: int | None = None,
    engine: BrowserPageObservationEngine | None = None,
    sleep_fn: SleepFn = time.sleep,
) -> JsonObject:
    normalized_handle = _normalize_handle(creator_handle)
    normalized_profile_url = _normalize_profile_url(creator_profile_url, normalized_handle)
    normalized_video_urls = [
        _normalize_video_url(url, expected_handle=normalized_handle) for url in video_urls
    ]
    if not normalized_video_urls:
        raise ValueError("at least one TikTok video URL is required")

    storage_state_path = validate_auth_state_session_mode(
        state_label,
        session_mode=session_mode,
        auth_state_root=auth_state_root,
    )
    cadence_plan = _build_probe_cadence_plan(
        video_count=len(normalized_video_urls),
        min_gap_seconds=cadence_min_gap_seconds,
        max_gap_seconds=cadence_max_gap_seconds,
        window_seconds=cadence_window_seconds,
        random_seed=random_seed,
    )

    attempts = 0
    challenge_count = 0
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
            post_load_action_script=TIKTOK_OPEN_COMMENTS_POST_LOAD_SCRIPT,
            post_load_action_arg=None,
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

        challenge_reason = detect_tiktok_challenge(capture_result)
        if challenge_reason is not None:
            challenge_count += 1
            failures.append(
                _failure_entry(
                    video_url=video_url,
                    video_id=video_id,
                    observed_utc=observed_utc,
                    reason=challenge_reason,
                    detail="TikTok challenge/auth-wall marker observed; probe stopped.",
                )
            )
            break

        item_struct = _extract_item_struct(capture_result.dom_observation)
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
        )
        assert_no_sensitive_tiktok_material(row)
        assert_no_sensitive_tiktok_material(grid_candidate)
        results.append(row)
        grid_items.append(grid_candidate)

    run_complete_utc = utc_now_z()
    grid_result = {
        "schema_version": TIKTOK_LIVE_BATCH_PROBE_SCHEMA_VERSION,
        "creator_handle": normalized_handle,
        "creator_profile_url": normalized_profile_url,
        "capture_contract": _capture_contract(session_mode=session_mode),
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
        "capture_contract": _capture_contract(session_mode=session_mode),
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
    final_url = capture_result.final_url.lower()
    title = (capture_result.title or "").lower()
    visible_text = capture_result.visible_text.lower()
    haystack = "\n".join((final_url, title, visible_text))
    if "/login" in final_url:
        return "login_or_auth_wall_observed"
    for marker in _CHALLENGE_MARKERS:
        if marker in haystack:
            return "platform_challenge_observed"
    return None


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
) -> JsonObject:
    subtitle_infos = _sanitize_subtitle_infos(_subtitle_infos_from_item_struct(item_struct))
    return {
        "video_id": video_id,
        "url_path": urlparse(video_url).path,
        "status": "completed",
        "creator_handle": creator_handle,
        "grid_candidate": grid_candidate,
        "comment_responses": [
            _comment_response_from_page_response(response, observed_utc=observed_utc)
            for response in capture_result.responses
            if is_tiktok_comment_list_url(response.final_url or response.requested_url)
        ],
        "hydration": {
            "subtitle_info_count": len(subtitle_infos),
            "subtitle_infos_sanitized": subtitle_infos,
        },
        "subtitle": {
            "attempted": False,
            "success": False,
            "reason": "subtitle_body_fetch_deferred_live_probe_v0",
        },
        "capture_receipt": {
            "page_url_sha256": _sha256_text(video_url),
            "final_url_sha256": _sha256_text(capture_result.final_url),
            "response_count": len(capture_result.responses),
            "matched_comment_response_count": sum(
                1
                for response in capture_result.responses
                if is_tiktok_comment_list_url(response.final_url or response.requested_url)
            ),
            "warning_count": len(capture_result.warning_notes),
            "limitation_count": len(capture_result.limitation_notes),
        },
    }


def _comment_response_from_page_response(
    response: BrowserPageResponse, *, observed_utc: str
) -> JsonObject:
    body_text = response.body_text or ""
    return {
        "observed_utc": observed_utc,
        "status": response.status,
        "ok": response.ok,
        "url_summary": _url_summary(response.final_url or response.requested_url),
        "body_assessment": _comment_body_assessment(body_text),
        "limitation_notes": list(response.limitation_notes),
    }


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
    assert_no_sensitive_tiktok_material(entry)
    return entry


def _capture_contract(*, session_mode: AuthenticatedSessionMode) -> JsonObject:
    return {
        "captcha_solving": False,
        "cookies_or_tokens_persisted": False,
        "direct_forged_api_calls": False,
        "page_owned_comment_list_response": True,
        "page_owned_video_navigation": True,
        "raw_comment_response_bodies_persisted": False,
        "raw_endpoint_urls_persisted": False,
        "raw_subtitle_bodies_persisted": False,
        "raw_subtitle_urls_persisted": False,
        "session_mode": session_mode.value,
        "staging_only": True,
        "stop_on_challenge": True,
        "subtitle_tier": "source_native_subtitle_metadata_only_live_probe_v0",
    }


def _non_claims() -> list[str]:
    return [
        "not_cross_creator_ceiling_evidence_until_real_owner_gated_runs_are_completed",
        "not_product_or_judgment_extraction",
        "not_bulk_scale_capture",
        "not_raw_comment_body_preservation",
        "not_subtitle_body_capture",
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
    "TIKTOK_OPEN_COMMENTS_POST_LOAD_SCRIPT",
    "TIKTOK_VIDEO_DOM_EXTRACT_SCRIPT",
    "TikTokLiveBatchProbeOutputPaths",
    "detect_tiktok_challenge",
    "is_tiktok_comment_list_url",
    "run_tiktok_live_batch_probe",
    "write_tiktok_live_batch_probe_outputs",
]
