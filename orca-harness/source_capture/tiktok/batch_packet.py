"""Network-free TikTok creator batch admission from sanitized staging results."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence
from urllib.parse import urlparse

from source_capture.models import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
)
from source_capture.packet_assembly import staged_file_id_map, stage_and_write_packet
from source_capture.tiktok.admission import (
    COMPLETE_LANE_NOTE,
    assert_no_sensitive_tiktok_material,
    decoded_aweme_id_create_time_utc,
    json_dumps_sanitized,
)

TIKTOK_BATCH_CAPTURE_SCHEMA_VERSION = "tiktok_batch_capture_admission_v0"
TIKTOK_BATCH_CAPTURE_SURFACE = "tiktok_creator_batch_comment_subtitle_admission"
TIKTOK_BATCH_CAPTURE_JSON_NAME = "tiktok_batch_capture.json"

TIKTOK_BATCH_NON_CLAIMS = (
    "not_live_tiktok_capture_or_browser_automation",
    "not_direct_forged_tiktok_api_call",
    "not_raw_signed_endpoint_url_capture",
    "not_raw_cookie_token_or_storage_capture",
    "not_raw_comment_response_body_capture",
    "not_raw_subtitle_url_capture",
    "not_raw_subtitle_body_capture",
    "not_raw_media_video_or_audio_capture",
    "not_full_comment_census",
    "not_reply_thread_expansion",
    "not_cross_creator_detection_ceiling",
    "not_final_product_or_judgment_extraction",
)

_DISCLOSURE_TERMS = ("#ad", "ad", "partner", "partnership", "sponsored", "gifted", "pr", "collab", "commission", "affiliate")
_COMMENT_INTENT_TERMS = ("where", "what", "which", "how much", "link", "buy", "need", "want", "try", "smell", "scent", "perfume", "fragrance", "worth", "last")
_TRANSCRIPT_SIGNAL_TERMS = ("smells like", "smell like", "lasts", "longevity", "sillage", "price", "available", "launch", "collection", "notes", "perfume", "fragrance")
_HANDLE_RE = re.compile(r"^[A-Za-z0-9._]{2,64}$")
_HASHTAG_RE = re.compile(r"(?<!\w)#([A-Za-z0-9_]{1,80})")

JsonObject = dict[str, Any]


def write_tiktok_batch_packet(
    *,
    creator_handle: str,
    creator_profile_url: str,
    grid_result_json: bytes,
    cadence_result_jsons: Sequence[bytes],
    output_directory: str | Path | None = None,
    data_root: str | Path | None = None,
    decision_question: str = "What product, disclosure, comment, and subtitle signals are present in this TikTok creator batch?",
    batch_label: str = "tiktok_creator_batch",
    source_file_receipts: Sequence[JsonObject] | None = None,
    capture_timestamp: str | None = None,
) -> tuple[int, str]:
    """Write a sanitized TikTok creator batch packet from parsed staging JSON."""

    handle = _normalize_creator_handle(creator_handle)
    profile_url = _canonical_creator_profile_url(creator_profile_url, handle)
    if not cadence_result_jsons:
        raise ValueError("At least one cadence result JSON input is required")

    payload = _build_payload(
        creator_handle=handle,
        creator_profile_url=profile_url,
        grid_result_json=grid_result_json,
        cadence_result_jsons=cadence_result_jsons,
        decision_question=decision_question,
        batch_label=batch_label,
        source_file_receipts=source_file_receipts or (),
        capture_timestamp=capture_timestamp,
    )

    payload_bytes = json_dumps_sanitized(payload)
    staged_artifacts = [(TIKTOK_BATCH_CAPTURE_JSON_NAME, payload_bytes)]
    file_ids = staged_file_id_map(staged_artifacts)
    summary = payload["batch_summary"]
    window = summary.get("create_time_utc_range") or "unknown create-time window"

    timing = PacketTiming(
        source_publication_or_event=known_fact(f"creator batch window UTC: {window}"),
        source_edit_or_version=not_applicable("TikTok batch admission packet does not model source edit/version timing"),
        capture_time=known_fact(payload["capture_timestamp"]),
        recapture_time=not_applicable("no prior TikTok batch admission packet supplied"),
        cutoff_posture=not_applicable("cutoff posture does not apply to parsed TikTok staging admission"),
    )
    access = known_fact(
        "sanitized parsed TikTok staging admission; raw session/signed URL material excluded"
    )
    archive = not_attempted("TikTok batch admission packet does not query archive/history services")
    media = known_fact("parsed comments/source-native WebVTT/profile-list fields preserved; no raw media bytes")
    recapture = not_applicable("no prior TikTok batch admission packet supplied")
    limitations = list(TIKTOK_BATCH_NON_CLAIMS)

    source_slices = [
        SourceCaptureSlice(
            slice_id="tiktok_batch_admission_01",
            locator=known_fact(profile_url),
            timing=timing,
            access_posture=access,
            archive_history_posture=archive,
            media_modality_posture=media,
            re_capture_relationship=recapture,
            limitations=limitations,
            warning_notes=[],
            preserved_file_ids=[file_ids[TIKTOK_BATCH_CAPTURE_JSON_NAME]],
        )
    ]

    result = stage_and_write_packet(
        output_directory=output_directory,
        data_root=data_root,
        staged_artifacts=staged_artifacts,
        source_slices=source_slices,
        source_family="tiktok",
        source_surface=TIKTOK_BATCH_CAPTURE_SURFACE,
        source_locator=known_fact(profile_url),
        decision_question=decision_question,
        capture_context=(
            "TikTok parsed creator-batch admission from supplied sanitized staging results; "
            "no live browser automation, endpoint replay, raw response bodies, or raw subtitle URLs"
        ),
        actor_audience_context=not_applicable("public TikTok creator batch capture; no actor/audience modeling at capture"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="tiktok_batch_admission_cli_operator",
        session_identity=None,
        visible_mode_changes=[
            "tiktok_sci_admission:parsed_creator_batch",
            COMPLETE_LANE_NOTE,
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
        limitations=limitations,
        receipt_summary=(
            f"TikTok batch admission for @{handle}: videos={summary['video_count']}, "
            f"comment_responses={summary['comment_response_success_count']}, "
            f"captured_comments={summary['captured_comment_count']}, "
            f"subtitle_success={summary['subtitle_success_count']}."
        ),
        receipt_non_claims=TIKTOK_BATCH_NON_CLAIMS,
    )
    return 0, result.output_directory


def _build_payload(
    *,
    creator_handle: str,
    creator_profile_url: str,
    grid_result_json: bytes,
    cadence_result_jsons: Sequence[bytes],
    decision_question: str,
    batch_label: str,
    source_file_receipts: Sequence[JsonObject],
    capture_timestamp: str | None,
) -> JsonObject:
    grid_payload = _loads_json_object(grid_result_json, "grid_result_json")
    cadence_payloads = [_loads_json_object(raw, f"cadence_result_json[{index}]") for index, raw in enumerate(cadence_result_jsons)]
    _validate_staging_contracts(grid_payload, cadence_payloads)

    run_results = _iter_cadence_results(cadence_payloads)
    if not run_results:
        raise ValueError("No cadence result rows were found")
    captured_ids = [str(row.get("video_id") or "") for row in run_results if row.get("video_id")]
    if not captured_ids:
        raise ValueError("No cadence result rows contained video_id")

    grid_by_video_id = _profile_items_by_video_id(grid_payload, captured_ids, creator_handle)
    videos = [
        _normalize_video_row(
            row=row,
            source_index=index,
            creator_handle=creator_handle,
            creator_profile_url=creator_profile_url,
            grid_item=grid_by_video_id.get(str(row.get("video_id") or "")),
        )
        for index, row in enumerate(run_results)
    ]
    videos = [video for video in videos if video is not None]
    if not videos:
        raise ValueError("No valid videos could be normalized from cadence results")

    summary = _summarize_batch(videos, cadence_payloads)
    timestamp = capture_timestamp or _latest_run_complete_utc(cadence_payloads) or _utc_now_iso()
    payload: JsonObject = {
        "capture_schema_version": TIKTOK_BATCH_CAPTURE_SCHEMA_VERSION,
        "platform": "tiktok",
        "source_surface": TIKTOK_BATCH_CAPTURE_SURFACE,
        "creator_handle": creator_handle,
        "creator_profile_url": creator_profile_url,
        "batch_label": batch_label,
        "capture_timestamp": timestamp,
        "decision_question": decision_question,
        "source_file_receipts": [_normalize_source_receipt(receipt) for receipt in source_file_receipts],
        "staging_contract_summary": _summarize_contracts(grid_payload, cadence_payloads),
        "batch_summary": summary,
        "videos": videos,
        "non_claims": list(TIKTOK_BATCH_NON_CLAIMS),
    }
    assert_no_sensitive_tiktok_material(payload)
    return payload


def _normalize_video_row(
    *,
    row: JsonObject,
    source_index: int,
    creator_handle: str,
    creator_profile_url: str,
    grid_item: JsonObject | None,
) -> JsonObject | None:
    video_id = str(row.get("video_id") or "").strip()
    if not video_id:
        return None

    grid_candidate = _as_dict(row.get("grid_candidate"))
    source_item = grid_item or grid_candidate
    source_stats = _as_dict(source_item.get("stats") if source_item else None) or _as_dict(grid_candidate.get("stats"))
    create_time = _first_int(source_item.get("createTime") if source_item else None, grid_candidate.get("createTime"))
    desc = _first_str(source_item.get("desc") if source_item else None, grid_candidate.get("desc"), "")
    hashtags = _dedupe_preserve_order(_HASHTAG_RE.findall(desc or ""))
    comments = _normalize_comments(row)
    subtitles = _normalize_subtitles(row)
    extraction_seed = _build_extraction_seed(desc or "", hashtags, _extract_mentions(desc or ""), comments, subtitles)

    video: JsonObject = {
        "source_index": source_index,
        "video_id": video_id,
        "video_url": f"{creator_profile_url.rstrip('/')}/video/{video_id}",
        "url_path": _first_str(row.get("url_path"), grid_candidate.get("url_path"), f"/@{creator_handle}/video/{video_id}"),
        "status": _first_str(row.get("status"), "unknown"),
        "create_time": create_time,
        "create_time_utc": _iso_from_unix(create_time),
        "decoded_aweme_id_create_time_utc": _first_str(
            source_item.get("decoded_aweme_id_create_time_utc") if source_item else None,
            grid_candidate.get("decoded_aweme_id_create_time_utc"),
            decoded_aweme_id_create_time_utc(video_id),
        ),
        "stats": _normalize_stats(source_stats),
        "source_text": {
            "desc": desc,
            "hashtags": hashtags,
            "mentions": extraction_seed["source_mentions"],
            "music": _normalize_music(_as_dict(source_item.get("music") if source_item else None) or _as_dict(grid_candidate.get("music"))),
        },
        "comments": comments,
        "subtitles": subtitles,
        "typed_extraction_seed": extraction_seed,
        "limitations": list(TIKTOK_BATCH_NON_CLAIMS),
    }
    if source_item:
        receipt = _profile_item_receipt(source_item)
        if receipt:
            video["profile_list_source_receipt"] = receipt
    assert_no_sensitive_tiktok_material(video)
    return video


def _normalize_comments(row: JsonObject) -> JsonObject:
    best = _best_comment_response(row)
    if best is None:
        return {
            "posture": "not_observed",
            "response_status": None,
            "body_sha256": None,
            "body_size_bytes": 0,
            "captured_comment_count": 0,
            "envelope": {},
            "field_coverage": {},
            "comments": [],
        }

    assessment = _as_dict(best.get("body_assessment"))
    parsed_comments = [_normalize_comment(comment, index) for index, comment in enumerate(_as_list(assessment.get("comments")))]
    parsed_comments = [comment for comment in parsed_comments if comment is not None]
    envelope = _normalize_comment_envelope(_as_dict(assessment.get("envelope")))
    url_summary = _as_dict(best.get("url_summary"))
    result: JsonObject = {
        "posture": "captured_page_owned_response",
        "observed_utc": _first_str(best.get("observed_utc")),
        "response_status": _first_int(best.get("status")),
        "body_sha256": _first_str(assessment.get("body_sha256")),
        "body_size_bytes": _first_int(assessment.get("body_byte_count"), 0),
        "captured_comment_count": len(parsed_comments),
        "assessment_comment_count": _first_int(assessment.get("comment_count"), len(parsed_comments)),
        "envelope": envelope,
        "field_coverage": _json_safe_scalar_map(_as_dict(assessment.get("field_coverage"))),
        "endpoint_receipt": {
            "path": _first_str(url_summary.get("path")),
            "url_sha256": _first_str(url_summary.get("url_sha256")),
            "query_key_count": _first_int(url_summary.get("query_key_count"), 0),
        },
        "comments": parsed_comments,
    }
    assert_no_sensitive_tiktok_material(result)
    return result


def _normalize_comment(comment: Any, source_order: int) -> JsonObject | None:
    item = _as_dict(comment)
    if not item:
        return None
    user = _as_dict(item.get("user"))
    result: JsonObject = {
        "source_order": source_order,
        "cid": _first_str(item.get("cid"), item.get("comment_id")),
        "text": _first_str(item.get("text"), ""),
        "create_time": _first_int(item.get("create_time"), item.get("createTime")),
        "create_time_utc": _iso_from_unix(_first_int(item.get("create_time"), item.get("createTime"))),
        "digg_count": _first_int(item.get("digg_count"), item.get("diggCount"), 0),
        "reply_comment_total": _first_int(item.get("reply_comment_total"), item.get("replyCommentTotal"), 0),
        "user": {
            "uid": _first_str(item.get("user_uid"), user.get("uid")),
            "unique_id": _first_str(item.get("user_unique_id"), user.get("unique_id"), user.get("uniqueId")),
            "nickname": _first_str(item.get("user_nickname"), user.get("nickname")),
        },
    }
    assert_no_sensitive_tiktok_material(result)
    return result


def _normalize_subtitles(row: JsonObject) -> JsonObject:
    hydration = _as_dict(row.get("hydration"))
    subtitle_info_count = _first_int(hydration.get("subtitle_info_count"), 0)
    subtitle_infos = _normalize_subtitle_infos(_as_list(hydration.get("subtitle_infos_sanitized")))
    subtitle = _as_dict(row.get("subtitle"))
    parsed = _as_dict(subtitle.get("parsed_webvtt"))

    if subtitle.get("success") is True and parsed:
        cues = [_normalize_cue(cue, index) for index, cue in enumerate(_as_list(parsed.get("cues")))]
        cues = [cue for cue in cues if cue is not None]
        transcript_text = _first_str(parsed.get("transcript_text"), "") or ""
        result: JsonObject = {
            "posture": "source_native_webvtt_captured",
            "subtitle_info_count": subtitle_info_count,
            "subtitle_infos": subtitle_infos,
            "body_sha256": _first_str(subtitle.get("body_sha256")),
            "body_size_bytes": _first_int(subtitle.get("body_byte_count"), 0),
            "subtitle_url_sha256": _first_str(subtitle.get("subtitle_url_sha256")),
            "subtitle_url_length": _first_int(subtitle.get("subtitle_url_length")),
            "cue_count": _first_int(parsed.get("cue_count"), len(cues)),
            "transcript_char_count": _first_int(parsed.get("transcript_char_count"), len(transcript_text)),
            "transcript_text_sha256": _first_str(parsed.get("transcript_text_sha256"), _sha256_text(transcript_text)),
            "transcript_text": transcript_text,
            "cues": cues,
        }
        assert_no_sensitive_tiktok_material(result)
        return result

    posture = "no_subtitleInfos_present" if subtitle_info_count == 0 else "source_native_subtitle_not_captured"
    result = {
        "posture": posture,
        "subtitle_info_count": subtitle_info_count,
        "subtitle_infos": subtitle_infos,
        "body_sha256": None,
        "body_size_bytes": 0,
        "subtitle_url_sha256": _first_str(subtitle.get("subtitle_url_sha256")),
        "cue_count": 0,
        "transcript_char_count": 0,
        "transcript_text_sha256": None,
        "transcript_text": "",
        "cues": [],
    }
    assert_no_sensitive_tiktok_material(result)
    return result


def _build_extraction_seed(desc: str, hashtags: Sequence[str], mentions: Sequence[str], comments: JsonObject, subtitles: JsonObject) -> JsonObject:
    desc_lower = (desc or "").lower()
    hashtag_lowers = [tag.lower() for tag in hashtags]
    disclosure_hits = _disclosure_hits(desc_lower, hashtag_lowers)
    comment_texts = [_first_str(_as_dict(comment).get("text"), "") or "" for comment in _as_list(comments.get("comments"))]
    question_comment_count = sum(1 for text in comment_texts if "?" in text)
    intent_counts = Counter()
    for text in comment_texts:
        lowered = text.lower()
        for term in _COMMENT_INTENT_TERMS:
            if term in lowered:
                intent_counts[term] += 1
    transcript_lower = (_first_str(subtitles.get("transcript_text"), "") or "").lower()
    seed = {
        "source_mentions": list(mentions),
        "hashtags": list(hashtags),
        "disclosure_source_text_signals": disclosure_hits,
        "has_disclosure_signal": bool(disclosure_hits),
        "comment_question_count": question_comment_count,
        "comment_intent_term_counts": dict(sorted(intent_counts.items())),
        "transcript_signal_terms": [term for term in _TRANSCRIPT_SIGNAL_TERMS if term in transcript_lower],
        "has_transcript_text": bool(transcript_lower.strip()),
    }
    assert_no_sensitive_tiktok_material(seed)
    return seed


def _summarize_batch(videos: Sequence[JsonObject], cadence_payloads: Sequence[JsonObject]) -> JsonObject:
    created = sorted(_first_str(video.get("create_time_utc")) for video in videos if video.get("create_time_utc"))
    attempted_count = sum(_first_int(payload.get("attempted_count"), 0) or 0 for payload in cadence_payloads)
    completed_count = sum(_first_int(payload.get("completed_count"), 0) or 0 for payload in cadence_payloads)
    challenge_count = sum(_first_int(payload.get("challenge_count"), 0) or 0 for payload in cadence_payloads)
    if completed_count != len(videos):
        raise ValueError(
            f"cadence completed_count={completed_count} does not match normalized video_count={len(videos)}"
        )
    if attempted_count < completed_count:
        raise ValueError(
            f"cadence attempted_count={attempted_count} is less than completed_count={completed_count}"
        )
    stats_sums = {
        key: sum(_first_int(_as_dict(video.get("stats")).get(key), 0) or 0 for video in videos)
        for key in ("playCount", "diggCount", "commentCount", "shareCount", "collectCount")
    }
    comment_success_count = sum(1 for video in videos if _as_dict(video.get("comments")).get("posture") == "captured_page_owned_response")
    captured_comment_count = sum(_first_int(_as_dict(video.get("comments")).get("captured_comment_count"), 0) or 0 for video in videos)
    envelope_total = sum(_first_int(_as_dict(_as_dict(video.get("comments")).get("envelope")).get("total"), 0) or 0 for video in videos)
    subtitle_success_count = sum(1 for video in videos if _as_dict(video.get("subtitles")).get("posture") == "source_native_webvtt_captured")
    subtitle_info_count = sum(1 for video in videos if (_first_int(_as_dict(video.get("subtitles")).get("subtitle_info_count"), 0) or 0) > 0)
    transcript_count = sum(1 for video in videos if _as_dict(video.get("typed_extraction_seed")).get("has_transcript_text") is True)
    cue_count = sum(_first_int(_as_dict(video.get("subtitles")).get("cue_count"), 0) or 0 for video in videos)
    disclosure_count = sum(1 for video in videos if _as_dict(video.get("typed_extraction_seed")).get("has_disclosure_signal") is True)

    return {
        "video_count": len(videos),
        "attempted_count": attempted_count,
        "completed_count": completed_count,
        "challenge_count": challenge_count,
        "comment_response_success_count": comment_success_count,
        "captured_comment_count": captured_comment_count,
        "comment_envelope_total_sum": envelope_total,
        "subtitle_info_video_count": subtitle_info_count,
        "subtitle_success_count": subtitle_success_count,
        "subtitle_cue_count": cue_count,
        "transcript_text_available_count": transcript_count,
        "source_text_disclosure_video_count": disclosure_count,
        "stats_sums": stats_sums,
        "create_time_utc_range": {"start": created[0], "end": created[-1]} if created else None,
    }


def _validate_staging_contracts(grid_payload: JsonObject, cadence_payloads: Sequence[JsonObject]) -> None:
    contracts = [_as_dict(grid_payload.get("capture_contract"))]
    contracts.extend(_as_dict(payload.get("capture_contract")) for payload in cadence_payloads)
    forbidden_true = (
        "direct_forged_api_calls",
        "cookies_or_tokens_persisted",
        "raw_endpoint_urls_persisted",
        "raw_comment_response_bodies_persisted",
        "raw_subtitle_urls_persisted",
        "raw_subtitle_bodies_persisted",
    )
    for index, contract in enumerate(contracts):
        for key in forbidden_true:
            if contract.get(key) is True:
                raise ValueError(f"capture_contract[{index}] indicates {key}=true")


def _summarize_contracts(grid_payload: JsonObject, cadence_payloads: Sequence[JsonObject]) -> JsonObject:
    contracts = [_as_dict(grid_payload.get("capture_contract")), *[_as_dict(payload.get("capture_contract")) for payload in cadence_payloads]]
    keys = (
        "captcha_solving",
        "cookies_or_tokens_persisted",
        "direct_forged_api_calls",
        "page_owned_comment_list_response",
        "page_owned_video_navigation",
        "raw_comment_response_bodies_persisted",
        "raw_endpoint_urls_persisted",
        "raw_subtitle_bodies_persisted",
        "raw_subtitle_urls_persisted",
        "staging_only",
        "stop_on_challenge",
        "subtitle_tier",
    )
    return {key: _unique_scalars(_json_safe_scalar(contract.get(key)) for contract in contracts if key in contract) for key in keys}


def _iter_cadence_results(cadence_payloads: Sequence[JsonObject]) -> list[JsonObject]:
    rows: list[JsonObject] = []
    for payload in cadence_payloads:
        rows.extend(_as_dict(row) for row in _as_list(payload.get("results")) if _as_dict(row))
    return rows


def _profile_items_by_video_id(grid_payload: JsonObject, video_ids: Sequence[str], creator_handle: str) -> dict[str, JsonObject]:
    wanted = set(video_ids)
    items_by_id: dict[str, JsonObject] = {}
    for raw in _as_list(grid_payload.get("response_items")):
        item = _as_dict(raw)
        video_id = str(item.get("id") or item.get("video_id") or "").strip()
        if video_id not in wanted:
            continue
        author = str(item.get("authorUniqueId") or item.get("author_unique_id") or "").strip().lstrip("@").lower()
        if author and author != creator_handle.lower():
            continue
        items_by_id.setdefault(video_id, item)
    return items_by_id


def _best_comment_response(row: JsonObject) -> JsonObject | None:
    candidates = []
    for raw in _as_list(row.get("comment_responses")):
        response = _as_dict(raw)
        assessment = _as_dict(response.get("body_assessment"))
        if not response:
            continue
        score = (2 if response.get("ok") is True else 0) + (2 if assessment.get("json_parse_ok") is True else 0) + (_first_int(assessment.get("comment_count"), 0) or 0)
        candidates.append((score, response))
    if not candidates:
        return None
    candidates.sort(key=lambda pair: pair[0], reverse=True)
    return candidates[0][1]


def _normalize_comment_envelope(envelope: JsonObject) -> JsonObject:
    return {"cursor": _first_str(envelope.get("cursor")), "has_more": _as_bool(envelope.get("has_more")), "total": _first_int(envelope.get("total"), 0)}


def _normalize_subtitle_infos(infos: Sequence[Any]) -> list[JsonObject]:
    safe_infos: list[JsonObject] = []
    for raw in infos:
        info = _as_dict(raw)
        if not info:
            continue
        safe = {
            "format": _first_str(info.get("Format"), info.get("format")),
            "language_code_name": _first_str(info.get("LanguageCodeName"), info.get("language_code_name")),
            "language_id": _first_str(info.get("LanguageID"), info.get("language_id")),
            "size": _first_int(info.get("Size"), info.get("size")),
            "source": _first_str(info.get("Source"), info.get("source")),
            "version": _first_str(info.get("Version"), info.get("version")),
        }
        if info.get("Url") or info.get("url") or _as_bool(info.get("url_present_but_redacted")):
            safe["url_redacted"] = True
        if info.get("UrlExpire") or info.get("url_expire"):
            safe["url_expire_redacted"] = True
        safe_infos.append(safe)
    return safe_infos


def _normalize_cue(cue: Any, source_order: int) -> JsonObject | None:
    item = _as_dict(cue)
    if not item:
        return None
    result = {
        "source_order": source_order,
        "identifier": _first_str(item.get("identifier"), item.get("id")),
        "start": _first_str(item.get("start"), item.get("start_time")),
        "end": _first_str(item.get("end"), item.get("end_time")),
        "text": _first_str(item.get("text"), ""),
    }
    assert_no_sensitive_tiktok_material(result)
    return result


def _normalize_stats(stats: JsonObject) -> JsonObject:
    return {
        "playCount": _first_int(stats.get("playCount"), stats.get("play_count"), 0),
        "diggCount": _first_int(stats.get("diggCount"), stats.get("digg_count"), 0),
        "commentCount": _first_int(stats.get("commentCount"), stats.get("comment_count"), 0),
        "shareCount": _first_int(stats.get("shareCount"), stats.get("share_count"), 0),
        "collectCount": _first_int(stats.get("collectCount"), stats.get("collect_count"), 0),
    }


def _normalize_music(music: JsonObject) -> JsonObject:
    return {
        "id": _first_str(music.get("id"), music.get("musicId")),
        "title": _first_str(music.get("title")),
        "author_name": _first_str(music.get("authorName"), music.get("author_name")),
        "original": _as_bool(music.get("original")),
    }


def _profile_item_receipt(item: JsonObject) -> JsonObject:
    receipt = {
        "source_response_path": _first_str(item.get("source_response_path")),
        "source_response_url_sha256": _first_str(item.get("source_response_url_sha256")),
    }
    return {key: value for key, value in receipt.items() if value not in (None, "")}


def _normalize_source_receipt(receipt: JsonObject) -> JsonObject:
    safe = {
        "role": _first_str(receipt.get("role"), "input"),
        "file_name": Path(str(receipt.get("file_name") or receipt.get("basename") or "input.json")).name,
        "sha256": _first_str(receipt.get("sha256")),
        "size_bytes": _first_int(receipt.get("size_bytes"), 0),
        "source_path_sha256": _first_str(receipt.get("source_path_sha256")),
        "path_redacted": True,
    }
    assert_no_sensitive_tiktok_material(safe)
    return safe


def _extract_mentions(text: str) -> list[str]:
    mentions: list[str] = []
    start = 0
    while True:
        idx = text.find("@", start)
        if idx == -1:
            break
        idx += 1
        chars: list[str] = []
        while idx < len(text) and len(chars) < 80:
            ch = text[idx]
            if ch in "\r\n\t#,:;!?()[]{}<>|/\\" or ch == "\u00a0":
                break
            chars.append(ch)
            idx += 1
        candidate = "".join(chars).strip()
        if candidate:
            mentions.append(candidate)
        start = idx + 1
    return _dedupe_preserve_order(mentions)


def _disclosure_hits(desc_lower: str, hashtag_lowers: Sequence[str]) -> list[str]:
    hits: list[str] = []
    for tag in hashtag_lowers:
        if tag in {"ad", "partner", "partnership", "sponsored", "gifted", "pr", "collab"}:
            hits.append(f"#{tag}")
        elif "partner" in tag or "sponsor" in tag or "gifted" in tag:
            hits.append(f"#{tag}")
    for term in _DISCLOSURE_TERMS:
        if term.startswith("#"):
            if term in desc_lower:
                hits.append(term)
        elif re.search(rf"\b{re.escape(term)}\b", desc_lower):
            hits.append(term)
    return _dedupe_preserve_order(hits)


def _loads_json_object(raw: bytes, label: str) -> JsonObject:
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise ValueError(f"{label} is not UTF-8 JSON") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"{label} is not valid JSON") from exc
    if not isinstance(parsed, dict):
        raise ValueError(f"{label} must contain a JSON object")
    return parsed


def _normalize_creator_handle(handle: str) -> str:
    value = str(handle or "").strip().lstrip("@")
    if not _HANDLE_RE.match(value):
        raise ValueError("creator_handle must be a TikTok handle without spaces or URL syntax")
    return value


def _canonical_creator_profile_url(url: str, handle: str) -> str:
    parsed = urlparse(str(url or "").strip())
    if parsed.scheme not in {"http", "https"} or parsed.netloc.lower() not in {"www.tiktok.com", "tiktok.com"}:
        raise ValueError("creator_profile_url must be a TikTok profile URL")
    if parsed.query or parsed.fragment:
        raise ValueError("creator_profile_url must not include query parameters or fragments")
    if parsed.path.rstrip("/").lower() != f"/@{handle}".lower():
        raise ValueError("creator_profile_url path must match creator_handle")
    return f"https://www.tiktok.com/@{handle}"


def _latest_run_complete_utc(cadence_payloads: Sequence[JsonObject]) -> str | None:
    values = sorted(_first_str(payload.get("run_complete_utc")) for payload in cadence_payloads if payload.get("run_complete_utc"))
    return values[-1] if values else None


def _parse_capture_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _iso_from_unix(value: int | None) -> str | None:
    if value is None:
        return None
    try:
        return datetime.fromtimestamp(int(value), tz=timezone.utc).isoformat().replace("+00:00", "Z")
    except (OSError, OverflowError, ValueError):
        return None


def _sha256_text(value: str) -> str | None:
    return hashlib.sha256(value.encode("utf-8")).hexdigest() if value else None


def _as_dict(value: Any) -> JsonObject:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _first_str(*values: Any) -> str | None:
    for value in values:
        if value is None:
            continue
        text = value.strip() if isinstance(value, str) else str(value).strip()
        if text:
            return text
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


def _as_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes"}:
            return True
        if lowered in {"false", "0", "no"}:
            return False
    return None


def _json_safe_scalar(value: Any) -> str | int | float | bool | None:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _json_safe_scalar_map(value: JsonObject) -> JsonObject:
    return {str(key): _json_safe_scalar(item) for key, item in value.items()}


def _unique_scalars(values: Iterable[Any]) -> list[Any]:
    result: list[Any] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def _dedupe_preserve_order(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        cleaned = str(value or "").strip()
        key = cleaned.lower()
        if cleaned and key not in seen:
            seen.add(key)
            result.append(cleaned)
    return result
