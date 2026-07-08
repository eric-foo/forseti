"""Pure helpers for IG public `/reels/` grid capture normalization.

No network or browser launch lives here. The live runner supplies browser DOM row
observations and passive JSON response bodies; this module normalizes them into
shortcode-keyed, source-surface-preserving records.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Iterable
from urllib.parse import urljoin, urlparse

DOM_GRID_ENGAGEMENT = "dom_grid_engagement"
PASSIVE_PAGE_JSON_METADATA = "passive_page_json_metadata"
CLIPS_USER_JSON_METADATA = "clips_user_json_metadata"
WEB_PROFILE_INFO_JSON_METADATA = "web_profile_info_json_metadata"
PROFILE_FEED_JSON_METADATA = "profile_feed_json_metadata"
ITEM_PAGE_METADATA = "item_page_metadata"
UNKNOWN_SOURCE_SURFACE = "unknown"

PARSED_NO_HOVER_GRID_ENGAGEMENT = "parsed_no_hover_grid_engagement"
VIEWS_ONLY_NO_HIDDEN_ENGAGEMENT = "views_only_no_hidden_engagement"
HIDDEN_ENGAGEMENT_ONLY_NO_VISIBLE_VIEWS = "hidden_engagement_only_no_visible_views"
AMBIGUOUS_HIDDEN_NUMERIC = "ambiguous_hidden_numeric"
ROUTE_NOT_VERIFIED = "route_not_verified"
STATIC_POST_VIEW_COUNT_NOT_APPLICABLE = "static_post_view_count_not_applicable"
MEDIA_KIND_REEL = "reel"
MEDIA_KIND_POST = "post"
MEDIA_KIND_UNKNOWN = "unknown"

_NUMERIC_RE = re.compile(r"^\d[\d,.]*(?:[KMB])?$", re.IGNORECASE)
_AD_TERM_RE = re.compile(r"(#ad\b|#ads\b|#sponsored\b|paid partnership|partner(?:ship)?|gifted|affiliate)", re.IGNORECASE)


@dataclass(frozen=True)
class IgReelsGridDomRow:
    index: int
    path: str
    permalink_url: str
    shortcode: str | None
    kind: str
    visible_text: str | None
    visible_numeric_texts: tuple[str, ...]
    hidden_leaf_numeric_texts: tuple[str, ...]
    hidden_engagement_candidates: tuple[str, ...]
    views_text: str | None
    likes_text: str | None
    comments_text: str | None
    parse_status: str
    rect: dict[str, object] | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class IgReelsJsonCandidate:
    source_surface: str
    shortcode: str
    taken_at_timestamp: int | None = None
    taken_at_utc: str | None = None
    caption_text: str | None = None
    caption_length: int = 0
    product_type: str | None = None
    typename: str | None = None
    is_video: bool | None = None
    video_or_play_count: int | None = None
    video_or_play_count_key: str | None = None
    video_or_play_count_candidates: tuple[tuple[str, int], ...] = ()
    like_count: int | None = None
    comment_count: int | None = None
    is_paid_partnership: bool | None = None
    is_affiliate: bool | None = None
    sponsor_users: tuple[str, ...] = ()
    ad_term_candidates: tuple[str, ...] = ()
    # Pinned signal from passive JSON (probe-grounded 2026-06-25). Reels-tab pin =
    # clips_tab_pinned_user_ids non-empty; main-grid/timeline pin = pinned_for_users
    # or timeline_pinned_user_ids non-empty. None when the surface omits the field.
    pinned_on_clips_tab: bool | None = None
    pinned_on_timeline: bool | None = None
    raw_node_keys_sample: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class IgReelsJoinedRow:
    dom_row: IgReelsGridDomRow
    source_surface_candidates: tuple[IgReelsJsonCandidate, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "dom_row": self.dom_row.to_dict(),
            "source_surface_candidates": [item.to_dict() for item in self.source_surface_candidates],
        }


def source_surface_from_url_or_path(url_or_path: str) -> str:
    path = urlparse(url_or_path).path or url_or_path
    if path == "/api/v1/clips/user/" or path.endswith("/api/v1/clips/user/"):
        return CLIPS_USER_JSON_METADATA
    if path == "/api/v1/users/web_profile_info/" or path.endswith("/api/v1/users/web_profile_info/"):
        return WEB_PROFILE_INFO_JSON_METADATA
    if path in {"/graphql/query/", "/api/graphql"} or path.endswith("/graphql/query/"):
        return PROFILE_FEED_JSON_METADATA
    return PASSIVE_PAGE_JSON_METADATA


def shortcode_from_path(path: str) -> str | None:
    parts = [part for part in path.split("/") if part]
    for index, part in enumerate(parts):
        if part in {"p", "reel"} and index + 1 < len(parts):
            return parts[index + 1]
    return None


def normalize_dom_grid_rows(
    raw_rows: Iterable[dict[str, object]],
    *,
    final_url: str,
    profile_handle: str | None = None,
    max_rows: int | None = None,
    allowed_kinds: tuple[str, ...] | None = None,
) -> list[IgReelsGridDomRow]:
    normalized_handle = profile_handle.casefold() if profile_handle else None
    rows: list[IgReelsGridDomRow] = []
    seen: set[str] = set()
    for raw in raw_rows:
        path = _path_from_href(_string_or_none(raw.get("path"))) or _path_from_href(_string_or_none(raw.get("href")))
        if not path or ("/p/" not in path and "/reel/" not in path):
            continue
        if normalized_handle is not None and not _path_matches_handle(path, normalized_handle):
            continue
        kind = _media_kind_from_path(path)
        if allowed_kinds is not None and kind not in allowed_kinds:
            continue
        shortcode = shortcode_from_path(path)
        identity = _row_identity(path=path, shortcode=shortcode)
        if identity in seen:
            continue
        seen.add(identity)
        visible_nums = _numeric_text_tuple(raw.get("visible_numeric_texts") or raw.get("visibleNumericTexts"))
        leaf_nums = _leaf_numeric_texts(raw)
        explicit_hidden = raw.get("hidden_engagement_candidates") is not None
        hidden_candidates = _numeric_text_tuple(raw.get("hidden_engagement_candidates"))
        visible_found = True
        if not hidden_candidates:
            hidden_candidates, visible_found = _subtract_visible_numbers(leaf_nums, visible_nums)
        views_text = None if kind == MEDIA_KIND_POST else _string_or_none(raw.get("views_text")) or (visible_nums[0] if visible_nums else None)
        ambiguous_hidden = _ambiguous_hidden_numeric(
            leafs=leaf_nums,
            visible=visible_nums,
            hidden_candidates=hidden_candidates,
            explicit_hidden=explicit_hidden,
            visible_found=visible_found,
        )
        if ambiguous_hidden:
            likes_text = None
            comments_text = None
        else:
            likes_text = _string_or_none(raw.get("likes_text")) or (
                hidden_candidates[0] if len(hidden_candidates) == 2 else None
            )
            comments_text = _string_or_none(raw.get("comments_text")) or (
                hidden_candidates[1] if len(hidden_candidates) == 2 else None
            )
        parse_status = _dom_parse_status(
            media_kind=kind,
            views_text=views_text,
            hidden_candidates=hidden_candidates,
            ambiguous_hidden=ambiguous_hidden,
        )
        rows.append(
            IgReelsGridDomRow(
                index=len(rows),
                path=path,
                permalink_url=urljoin(final_url, path),
                shortcode=shortcode,
                kind=kind,
                visible_text=_string_or_none(raw.get("visible_text") or raw.get("visibleText")),
                visible_numeric_texts=visible_nums,
                hidden_leaf_numeric_texts=leaf_nums,
                hidden_engagement_candidates=hidden_candidates,
                views_text=views_text,
                likes_text=likes_text,
                comments_text=comments_text,
                parse_status=parse_status,
                rect=raw.get("rect") if isinstance(raw.get("rect"), dict) else None,
            )
        )
        if max_rows is not None and len(rows) >= max_rows:
            break
    return rows


def iter_json_media_candidates(payload: object, *, source_surface: str) -> list[IgReelsJsonCandidate]:
    candidates: list[IgReelsJsonCandidate] = []
    for node in _iter_media_nodes(payload):
        candidate = _candidate_from_node(node, source_surface=source_surface)
        if candidate is not None:
            candidates.append(candidate)
    return candidates


def candidates_by_shortcode(candidates: Iterable[IgReelsJsonCandidate]) -> dict[str, tuple[IgReelsJsonCandidate, ...]]:
    grouped: dict[str, list[IgReelsJsonCandidate]] = {}
    for candidate in candidates:
        grouped.setdefault(candidate.shortcode, []).append(candidate)
    return {shortcode: tuple(items) for shortcode, items in grouped.items()}


def join_dom_rows_with_json_candidates(
    dom_rows: Iterable[IgReelsGridDomRow],
    candidates: Iterable[IgReelsJsonCandidate],
) -> list[IgReelsJoinedRow]:
    grouped = candidates_by_shortcode(candidates)
    return [
        IgReelsJoinedRow(
            dom_row=row,
            source_surface_candidates=grouped.get(row.shortcode or "", ()),
        )
        for row in dom_rows
    ]


def _iter_media_nodes(value: object) -> Iterable[dict[str, object]]:
    if isinstance(value, dict):
        if _node_shortcode(value) is not None:
            yield value
            return
        for child in value.values():
            yield from _iter_media_nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_media_nodes(child)


def _candidate_from_node(node: dict[str, object], *, source_surface: str) -> IgReelsJsonCandidate | None:
    shortcode = _node_shortcode(node)
    if shortcode is None:
        return None
    caption = _caption_text(node)
    taken_at = _first_int(node, ("taken_at_timestamp", "taken_at"))
    video_count_key, video_count, video_count_candidates = _first_count_with_key(
        node,
        _video_count_keys(source_surface),
    )
    sponsors = tuple(sorted(set(_sponsor_users(node))))
    ad_terms = tuple(sorted(set(match.group(0) for match in _AD_TERM_RE.finditer(caption or ""))))
    return IgReelsJsonCandidate(
        source_surface=source_surface,
        shortcode=shortcode,
        taken_at_timestamp=taken_at,
        taken_at_utc=_timestamp_to_utc(taken_at),
        caption_text=caption,
        caption_length=len(caption) if caption else 0,
        product_type=_string_or_none(node.get("product_type")),
        typename=_string_or_none(node.get("__typename")),
        is_video=node.get("is_video") if isinstance(node.get("is_video"), bool) else None,
        video_or_play_count=video_count,
        video_or_play_count_key=video_count_key,
        video_or_play_count_candidates=video_count_candidates,
        like_count=_first_count(node, ("edge_liked_by", "edge_media_preview_like", "like_count")),
        comment_count=_first_count(node, ("edge_media_to_comment", "comment_count")),
        is_paid_partnership=node.get("is_paid_partnership")
        if isinstance(node.get("is_paid_partnership"), bool)
        else None,
        is_affiliate=node.get("is_affiliate") if isinstance(node.get("is_affiliate"), bool) else None,
        sponsor_users=sponsors,
        ad_term_candidates=ad_terms,
        pinned_on_clips_tab=_pinned_flag(node, "clips_tab_pinned_user_ids"),
        pinned_on_timeline=_pinned_flag(node, "timeline_pinned_user_ids", "pinned_for_users"),
        raw_node_keys_sample=tuple(sorted(str(key) for key in node.keys())[:80]),
    )


def _node_shortcode(node: dict[str, object]) -> str | None:
    return _shortcode_string_or_none(node.get("shortcode")) or _shortcode_string_or_none(node.get("code"))


def _pinned_flag(node: dict[str, object], *keys: str) -> bool | None:
    """Pinned posture from a media node's pinned-user-id list (first present key
    wins): a non-empty list means pinned (the creator's own id is listed), an empty
    list means not pinned, and None means the surface did not expose the field."""
    for key in keys:
        value = node.get(key)
        if isinstance(value, list):
            return len(value) > 0
    return None


def _caption_text(node: dict[str, object]) -> str | None:
    caption = node.get("caption")
    if isinstance(caption, dict):
        text = _string_or_none(caption.get("text"))
        if text is not None:
            return text
    if isinstance(caption, str):
        return caption.strip() or None
    edge_caption = node.get("edge_media_to_caption")
    if isinstance(edge_caption, dict):
        edges = edge_caption.get("edges")
        if isinstance(edges, list) and edges:
            first = edges[0]
            first_node = first.get("node") if isinstance(first, dict) else None
            if isinstance(first_node, dict):
                return _string_or_none(first_node.get("text"))
    return None


def _sponsor_users(node: dict[str, object]) -> list[str]:
    found: list[str] = []
    edge = node.get("edge_media_to_sponsor_user")
    if isinstance(edge, dict):
        edges = edge.get("edges")
        if isinstance(edges, list):
            for item in edges:
                sponsor = item.get("node") if isinstance(item, dict) else None
                if isinstance(sponsor, dict):
                    _append_sponsor(found, sponsor)
    for key in ("sponsor_tags", "sponsor_users", "branded_content_sponsor"):
        value = node.get(key)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    _append_sponsor(found, item)
        elif isinstance(value, dict):
            _append_sponsor(found, value)
    return found


def _append_sponsor(found: list[str], sponsor: dict[str, object]) -> None:
    value = sponsor.get("username") or sponsor.get("full_name") or sponsor.get("id")
    text = _string_or_none(value)
    if text is not None:
        found.append(text)


def _path_from_href(href: str | None) -> str | None:
    if href is None:
        return None
    try:
        return urlparse(href).path or href
    except ValueError:
        return href


def _row_identity(*, path: str, shortcode: str | None) -> str:
    if shortcode is not None:
        return f"shortcode:{shortcode}"
    return f"path:{_canonical_path(path)}"


def _canonical_path(path: str) -> str:
    parsed = urlparse(path)
    normalized = parsed.path or path
    return normalized.rstrip("/") or normalized

def _media_kind_from_path(path: str) -> str:
    if "/reel/" in path:
        return MEDIA_KIND_REEL
    if "/p/" in path:
        return MEDIA_KIND_POST
    return MEDIA_KIND_UNKNOWN


def _path_matches_handle(path: str, normalized_handle: str) -> bool:
    parts = [part for part in path.split("/") if part]
    if not parts:
        return False
    if parts[0] in {"p", "reel"}:
        return True
    return parts[0].casefold() == normalized_handle


def _leaf_numeric_texts(raw: dict[str, object]) -> tuple[str, ...]:
    explicit = raw.get("hidden_leaf_numeric_texts")
    if explicit is not None:
        return _numeric_text_tuple(explicit)
    leafs = raw.get("leafNumericTexts")
    if isinstance(leafs, list):
        out: list[str] = []
        for item in leafs:
            if isinstance(item, dict):
                text = _string_or_none(item.get("text"))
                if text is not None and _NUMERIC_RE.match(text):
                    out.append(text)
            else:
                text = _string_or_none(item)
                if text is not None and _NUMERIC_RE.match(text):
                    out.append(text)
        return tuple(out)
    return ()


def _subtract_visible_numbers(
    leafs: tuple[str, ...],
    visible: tuple[str, ...],
) -> tuple[tuple[str, ...], bool]:
    remaining_visible = list(visible)
    hidden: list[str] = []
    for text in leafs:
        try:
            index = remaining_visible.index(text)
        except ValueError:
            hidden.append(text)
        else:
            del remaining_visible[index]
    return tuple(hidden), not remaining_visible


def _ambiguous_hidden_numeric(
    *,
    leafs: tuple[str, ...],
    visible: tuple[str, ...],
    hidden_candidates: tuple[str, ...],
    explicit_hidden: bool,
    visible_found: bool,
) -> bool:
    if not visible or not hidden_candidates:
        return False
    if len(hidden_candidates) != 2:
        return True
    if not explicit_hidden and not visible_found:
        return True
    if explicit_hidden:
        return False
    return any(leafs.count(text) > visible.count(text) for text in visible)


def _dom_parse_status(
    *,
    media_kind: str,
    views_text: str | None,
    hidden_candidates: tuple[str, ...],
    ambiguous_hidden: bool,
) -> str:
    if media_kind == MEDIA_KIND_POST:
        return STATIC_POST_VIEW_COUNT_NOT_APPLICABLE
    if ambiguous_hidden:
        return AMBIGUOUS_HIDDEN_NUMERIC
    if views_text is not None and len(hidden_candidates) >= 2:
        return PARSED_NO_HOVER_GRID_ENGAGEMENT
    if views_text is not None:
        return VIEWS_ONLY_NO_HIDDEN_ENGAGEMENT
    if hidden_candidates:
        return HIDDEN_ENGAGEMENT_ONLY_NO_VISIBLE_VIEWS
    return ROUTE_NOT_VERIFIED


def _first_count(container: dict[str, object], keys: tuple[str, ...]) -> int | None:
    return _first_count_with_key(container, keys)[1]


def _first_count_with_key(
    container: dict[str, object],
    keys: tuple[str, ...],
) -> tuple[str | None, int | None, tuple[tuple[str, int], ...]]:
    candidates = _count_candidates(container, keys)
    selected_key = candidates[0][0] if candidates else None
    selected_value = candidates[0][1] if candidates else None
    return selected_key, selected_value, candidates


def _count_candidates(container: dict[str, object], keys: tuple[str, ...]) -> tuple[tuple[str, int], ...]:
    candidates: list[tuple[str, int]] = []
    for key in keys:
        if key not in container:
            continue
        value = container.get(key)
        parsed = _edge_count(value) if isinstance(value, dict) else _int_or_none(value)
        if parsed is not None:
            candidates.append((key, parsed))
    return tuple(candidates)


def _video_count_keys(source_surface: str) -> tuple[str, ...]:
    if source_surface == CLIPS_USER_JSON_METADATA:
        return ("ig_play_count", "play_count", "video_view_count", "view_count")
    return ("video_view_count", "play_count", "view_count", "ig_play_count")


def _first_int(container: dict[str, object], keys: tuple[str, ...]) -> int | None:
    for key in keys:
        if key in container:
            parsed = _int_or_none(container.get(key))
            if parsed is not None:
                return parsed
    return None


def _edge_count(value: object) -> int | None:
    if isinstance(value, dict):
        return _int_or_none(value.get("count"))
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


def _timestamp_to_utc(value: int | None) -> str | None:
    if value is None:
        return None
    try:
        return datetime.fromtimestamp(value, timezone.utc).isoformat().replace("+00:00", "Z")
    except (OSError, OverflowError, ValueError):
        return None


def _shortcode_string_or_none(value: object) -> str | None:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return None


def _string_or_none(value: object) -> str | None:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    if isinstance(value, int):
        return str(value)
    return None


def _text_tuple(value: object) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)):
        return ()
    out: list[str] = []
    for item in value:
        text = _string_or_none(item)
        if text is not None:
            out.append(text)
    return tuple(out)


def _numeric_text_tuple(value: object) -> tuple[str, ...]:
    return tuple(text for text in _text_tuple(value) if _NUMERIC_RE.match(text))
