"""TikTok parser/admission helpers for the lean behavioral capture slice.

This module is deliberately network-free. Live browser/session acquisition stays
outside this layer; callers supply page-owned response bodies or hydrated item
JSON that have already been captured under the TikTok lane guardrails.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping, Sequence

TIKTOK_COMMENT_LIST_ROUTE = "/api/comment/list"
TIKTOK_PROFILE_LIST_SURFACES = ("/api/post/item_list/", "/api/repost/item_list/")

COMPLETE_LANE_NOTE = (
    "Complete TikTok lane still requires the live browser/profile-grid runner, "
    "projection bridge, cross-creator ceiling, and recon/playbook update. "
    "This SCI layer enforces sanitized single-video and parsed-batch admission only."
)

_VIDEO_ID_RE = re.compile(r"\d{15,25}")
_TIMESTAMP_RE = re.compile(
    r"(?P<start>(?:\d{2}:)?\d{2}:\d{2}[.,]\d{3})\s*-->\s*"
    r"(?P<end>(?:\d{2}:)?\d{2}:\d{2}[.,]\d{3})"
)
_SENSITIVE_QUERY_RE = re.compile(
    r"(?i)(?:msToken|X-Bogus|verifyFp|ttwid|sessionid|sid_guard|odin_tt|"
    r"passport_csrf_token|s_v_web_id)="
)
_RAW_TIKTOK_URL_RE = re.compile(r"(?i)^https?://[^ \n\r\t]*(?:tiktok|tiktokcdn|ttwstatic)[^ \n\r\t]*\?.+")
_RAW_SUBTITLE_URL_RE = re.compile(r"(?i)^https?://[^ \n\r\t]*(?:v16|tos-|tiktokcdn|byteoversea)[^ \n\r\t]*")
_SENSITIVE_KEYS = {
    "authorization",
    "cookie",
    "cookies",
    "set-cookie",
    "mstoken",
    "x-bogus",
    "verifyfp",
    "ttwid",
    "sessionid",
    "sid_guard",
    "odin_tt",
    "passport_csrf_token",
    "storage_state",
}


@dataclass(frozen=True)
class TiktokProfileListItem:
    source_surface: str
    video_id: str
    create_time: int | None
    create_time_utc: str | None
    decoded_aweme_id_create_time_utc: str | None
    desc: str | None
    play_count: int | None
    digg_count: int | None
    comment_count: int | None
    share_count: int | None
    collect_count: int | None
    hashtags: tuple[str, ...]
    challenge_titles: tuple[str, ...]
    music_title: str | None
    music_author: str | None
    is_ad: bool | None
    ad_label_version: int | None
    ad_authorization_present: bool
    ba_info_present: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TiktokComment:
    cid: str
    text: str
    create_time: int
    digg_count: int
    reply_comment_total: int
    user_uid: str
    user_unique_id: str
    user_nickname: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TiktokCommentListAdmission:
    body_sha256: str
    body_size_bytes: int
    cursor: int | str | None
    has_more: int | bool | None
    total: int | None
    comment_count: int
    comments: tuple[TiktokComment, ...]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["comments"] = [comment.to_dict() for comment in self.comments]
        return payload


@dataclass(frozen=True)
class TiktokSubtitleInfo:
    format: str | None
    language_code_name: str | None
    language_id: str | int | None
    source: str | None
    size: int | None
    version: str | None
    url_sha256: str | None
    url_present: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TiktokWebVttCue:
    start_ms: int
    end_ms: int
    text: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def decoded_aweme_id_create_time_utc(video_id: str) -> str | None:
    """Decode the high-bit timestamp candidate from a TikTok Snowflake-like id."""
    if not _VIDEO_ID_RE.fullmatch(video_id or ""):
        return None
    try:
        timestamp = int(video_id) >> 32
    except ValueError:
        return None
    # TikTok launched after 2016; keep a broad future guard so malformed ids do
    # not become plausible dates.
    if timestamp < 1_451_606_400 or timestamp > 4_102_444_800:
        return None
    return _unix_to_utc(timestamp)


def parse_profile_list_items(payload: object, *, source_surface: str) -> list[TiktokProfileListItem]:
    """Extract TikTok item candidates from page-owned profile/list JSON."""
    out: list[TiktokProfileListItem] = []
    seen: set[tuple[str, str]] = set()
    for node in _iter_dicts(payload):
        item = _profile_item_from_node(node, source_surface=source_surface)
        if item is None:
            continue
        key = (item.source_surface, item.video_id)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def parse_comment_list_bytes(raw_body: bytes) -> TiktokCommentListAdmission:
    """Parse a page-owned TikTok comment-list body into packet-grade fields."""
    if not raw_body:
        raise ValueError("empty TikTok comment-list body")
    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError(f"invalid TikTok comment-list JSON: {exc}") from exc
    if not isinstance(payload, Mapping):
        raise ValueError("TikTok comment-list body must be a JSON object")
    comments_raw = payload.get("comments")
    if not isinstance(comments_raw, list):
        raise ValueError("TikTok comment-list body missing comments list")

    comments = tuple(_comment_from_node(comment, index=index) for index, comment in enumerate(comments_raw))
    return TiktokCommentListAdmission(
        body_sha256=hashlib.sha256(raw_body).hexdigest(),
        body_size_bytes=len(raw_body),
        cursor=_int_or_string_or_none(payload.get("cursor")),
        has_more=_bool_int_or_none(payload.get("has_more")),
        total=_int_or_none(payload.get("total")),
        comment_count=len(comments),
        comments=comments,
    )


def extract_subtitle_infos(video_item: object) -> list[TiktokSubtitleInfo]:
    """Extract sanitized TikTok subtitleInfos records, keeping only URL hashes."""
    out: list[TiktokSubtitleInfo] = []
    for node in _iter_dicts(video_item):
        infos = node.get("subtitleInfos")
        if not isinstance(infos, list):
            continue
        for info in infos:
            if not isinstance(info, Mapping):
                continue
            raw_url = _string_or_none(info.get("Url")) or _string_or_none(info.get("url"))
            out.append(
                TiktokSubtitleInfo(
                    format=_string_or_none(info.get("Format")) or _string_or_none(info.get("format")),
                    language_code_name=_string_or_none(info.get("LanguageCodeName"))
                    or _string_or_none(info.get("languageCodeName")),
                    language_id=_int_or_string_or_none(info.get("LanguageID") or info.get("languageID")),
                    source=_string_or_none(info.get("Source")) or _string_or_none(info.get("source")),
                    size=_int_or_none(info.get("Size") or info.get("size")),
                    version=_string_or_none(info.get("Version")) or _string_or_none(info.get("version")),
                    url_sha256=hashlib.sha256(raw_url.encode("utf-8")).hexdigest() if raw_url else None,
                    url_present=raw_url is not None,
                )
            )
    return out


def parse_webvtt_cues(raw_body: bytes) -> list[TiktokWebVttCue]:
    """Parse WebVTT cue text/timing from bytes. Content-Type is intentionally ignored."""
    if not raw_body:
        raise ValueError("empty WebVTT body")
    try:
        text = raw_body.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError(f"invalid WebVTT UTF-8: {exc}") from exc
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if "WEBVTT" not in normalized[:80]:
        raise ValueError("WebVTT body missing WEBVTT header")
    cues: list[TiktokWebVttCue] = []
    for block in re.split(r"\n{2,}", normalized):
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if not lines or lines[0].startswith("WEBVTT"):
            continue
        timing_index = 0 if "-->" in lines[0] else 1 if len(lines) > 1 and "-->" in lines[1] else -1
        if timing_index < 0:
            continue
        match = _TIMESTAMP_RE.search(lines[timing_index])
        if match is None:
            continue
        cue_text = "\n".join(lines[timing_index + 1 :]).strip()
        if not cue_text:
            continue
        cues.append(
            TiktokWebVttCue(
                start_ms=_timestamp_to_ms(match.group("start")),
                end_ms=_timestamp_to_ms(match.group("end")),
                text=cue_text,
            )
        )
    if not cues:
        raise ValueError("WebVTT body contained no parseable cues")
    return cues


def find_sensitive_tiktok_material(value: object) -> list[str]:
    """Return paths that appear to contain raw TikTok/session-sensitive material."""
    findings: list[str] = []
    _collect_sensitive(value, "$", findings)
    return findings


def assert_no_sensitive_tiktok_material(value: object) -> None:
    findings = find_sensitive_tiktok_material(value)
    if findings:
        preview = "; ".join(findings[:5])
        raise ValueError(f"refusing to persist unsafe TikTok material: {preview}")


def _profile_item_from_node(node: Mapping[str, Any], *, source_surface: str) -> TiktokProfileListItem | None:
    video_id = _string_or_none(node.get("id")) or _string_or_none(node.get("aweme_id"))
    if video_id is None or not _VIDEO_ID_RE.fullmatch(video_id):
        return None
    if not _looks_like_profile_item(node):
        return None

    stats = node.get("stats") if isinstance(node.get("stats"), Mapping) else {}
    stats_v2 = node.get("statsV2") if isinstance(node.get("statsV2"), Mapping) else {}
    create_time = _first_int(node, stats, keys=("createTime", "create_time", "create_time_sec"))
    hashtags = _hashtags_from_text_extra(node.get("textExtra"))
    challenge_titles = _challenge_titles(node.get("challenges"))
    music = node.get("music") if isinstance(node.get("music"), Mapping) else {}
    return TiktokProfileListItem(
        source_surface=source_surface,
        video_id=video_id,
        create_time=create_time,
        create_time_utc=_unix_to_utc(create_time) if create_time is not None else None,
        decoded_aweme_id_create_time_utc=decoded_aweme_id_create_time_utc(video_id),
        desc=_string_or_none(node.get("desc")),
        play_count=_first_int(node, stats, stats_v2, keys=("playCount", "play_count", "play")),
        digg_count=_first_int(node, stats, stats_v2, keys=("diggCount", "digg_count", "digg")),
        comment_count=_first_int(node, stats, stats_v2, keys=("commentCount", "comment_count", "comment")),
        share_count=_first_int(node, stats, stats_v2, keys=("shareCount", "share_count", "share")),
        collect_count=_first_int(node, stats, stats_v2, keys=("collectCount", "collect_count", "collect")),
        hashtags=hashtags,
        challenge_titles=challenge_titles,
        music_title=_string_or_none(music.get("title")),
        music_author=_string_or_none(music.get("authorName")) or _string_or_none(music.get("author")),
        is_ad=_bool_or_none(node.get("isAd")),
        ad_label_version=_int_or_none(node.get("adLabelVersion")),
        ad_authorization_present=isinstance(node.get("adAuthorization"), Mapping),
        ba_info_present=isinstance(node.get("BAInfo"), Mapping),
    )


def _comment_from_node(comment: object, *, index: int) -> TiktokComment:
    if not isinstance(comment, Mapping):
        raise ValueError(f"comment[{index}] must be an object")
    user = comment.get("user")
    if not isinstance(user, Mapping):
        raise ValueError(f"comment[{index}] missing user object")
    return TiktokComment(
        cid=_required_string(comment, "cid", index=index),
        text=_required_string(comment, "text", index=index, allow_empty=True),
        create_time=_required_int(comment, "create_time", index=index),
        digg_count=_required_int(comment, "digg_count", index=index),
        reply_comment_total=_required_int(comment, "reply_comment_total", index=index),
        user_uid=_required_string(user, "uid", index=index, prefix="user"),
        user_unique_id=_required_string(user, "unique_id", index=index, prefix="user"),
        user_nickname=_required_string(user, "nickname", index=index, prefix="user"),
    )


def _looks_like_profile_item(node: Mapping[str, Any]) -> bool:
    if any(key in node for key in ("stats", "statsV2", "createTime", "desc", "textExtra", "challenges", "music")):
        return True
    return any(key in node for key in ("isAd", "adLabelVersion", "adAuthorization", "BAInfo"))


def _hashtags_from_text_extra(value: object) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    found: list[str] = []
    for item in value:
        if not isinstance(item, Mapping):
            continue
        hashtag = _string_or_none(item.get("hashtagName")) or _string_or_none(item.get("hashtag_name"))
        if hashtag is not None and hashtag not in found:
            found.append(hashtag)
    return tuple(found)


def _challenge_titles(value: object) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    found: list[str] = []
    for item in value:
        if not isinstance(item, Mapping):
            continue
        title = _string_or_none(item.get("title"))
        if title is not None and title not in found:
            found.append(title)
    return tuple(found)


def _iter_dicts(value: object) -> Iterable[Mapping[str, Any]]:
    if isinstance(value, Mapping):
        yield value
        for child in value.values():
            yield from _iter_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_dicts(child)


def _collect_sensitive(value: object, path: str, findings: list[str]) -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            key_text = str(key)
            key_norm = key_text.strip().lower()
            child_path = f"{path}.{key_text}"
            if key_norm in _SENSITIVE_KEYS:
                findings.append(f"{child_path}: sensitive key")
            _collect_sensitive(child, child_path, findings)
        return
    if isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            _collect_sensitive(child, f"{path}[{index}]", findings)
        return
    if not isinstance(value, str):
        return
    if _SENSITIVE_QUERY_RE.search(value):
        findings.append(f"{path}: signed/session query material")
    elif _RAW_TIKTOK_URL_RE.match(value):
        findings.append(f"{path}: raw TikTok URL with query string")
    elif _RAW_SUBTITLE_URL_RE.match(value):
        findings.append(f"{path}: raw TikTok media/subtitle URL")


def _required_string(
    value: Mapping[str, Any],
    key: str,
    *,
    index: int,
    prefix: str = "comment",
    allow_empty: bool = False,
) -> str:
    parsed = _string_or_none(value.get(key), allow_empty=allow_empty)
    if parsed is None:
        raise ValueError(f"comment[{index}] missing {prefix}.{key}")
    return parsed


def _required_int(value: Mapping[str, Any], key: str, *, index: int) -> int:
    parsed = _int_or_none(value.get(key))
    if parsed is None:
        raise ValueError(f"comment[{index}] missing integer {key}")
    return parsed


def _first_int(*containers: Mapping[str, Any], keys: Sequence[str]) -> int | None:
    for container in containers:
        for key in keys:
            parsed = _int_or_none(container.get(key))
            if parsed is not None:
                return parsed
    return None


def _int_or_none(value: object) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        stripped = value.replace(",", "").strip()
        if stripped.isdigit():
            return int(stripped)
    return None


def _int_or_string_or_none(value: object) -> int | str | None:
    parsed_int = _int_or_none(value)
    if parsed_int is not None:
        return parsed_int
    return _string_or_none(value)


def _bool_int_or_none(value: object) -> int | bool | None:
    if isinstance(value, bool):
        return value
    return _int_or_none(value)


def _bool_or_none(value: object) -> bool | None:
    if isinstance(value, bool):
        return value
    return None


def _string_or_none(value: object, *, allow_empty: bool = False) -> str | None:
    if isinstance(value, str):
        stripped = value.strip()
        if stripped or allow_empty:
            return stripped
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    return None


def _unix_to_utc(value: int) -> str:
    return _dt.datetime.fromtimestamp(value, _dt.timezone.utc).isoformat().replace("+00:00", "Z")


def _timestamp_to_ms(value: str) -> int:
    parts = value.replace(",", ".").split(":")
    if len(parts) == 2:
        hours = 0
        minutes = int(parts[0])
        seconds_text = parts[1]
    elif len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds_text = parts[2]
    else:
        raise ValueError(f"invalid WebVTT timestamp: {value!r}")
    seconds, milliseconds = seconds_text.split(".", 1)
    return ((hours * 3600 + minutes * 60 + int(seconds)) * 1000) + int(milliseconds[:3])


def json_dumps_sanitized(payload: object) -> bytes:
    assert_no_sensitive_tiktok_material(payload)
    return (json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
