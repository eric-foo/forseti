"""Mechanical projection of one old Reddit subreddit listing (grid) page.

One grid page carries both radar layers at once:

- the venue envelope (titlebox subscriber / active-user counts when the
  subreddit's markup exposes them), and
- the thread grid (one row per listing ``thing`` with visible engagement:
  score and comment count).

The projection is read-only and mechanical: source-visible values are
carried as strings, absence is carried as ``None`` plus an absent reason,
and nothing here ranks, scores quality, or claims demand.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from html.parser import HTMLParser

from source_capture.projection_shared import canonical_old_reddit_thread_url

# Bump on ANY behavior change to this projection so content packets written
# under the old behavior stay distinguishable from re-projections under the
# new one (parser-fit drift checks compare records only within one version).
GRID_PROJECTION_PARSER_VERSION = "1"

GRID_CONTENT_RECORD_KIND = "reddit_subreddit_grid_view_v0"


class RedditGridProjectionError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class GridThreadRow:
    thread_url: str
    subreddit: str
    visible_title_or_none: str | None
    visible_score_or_none: str | None
    visible_comment_count_or_none: str | None
    promoted: bool


@dataclass(frozen=True)
class GridView:
    subreddit: str
    listing_url: str
    visible_subscriber_count_or_none: str | None
    visible_active_user_count_or_none: str | None
    visible_volume_signal_absent_reason_or_none: str | None
    thread_rows: tuple[GridThreadRow, ...] = field(default_factory=tuple)


def project_old_reddit_grid_html(
    *,
    html_text: str,
    subreddit: str,
    listing_url: str,
    max_thread_rows: int = 100,
) -> GridView:
    """Project one old Reddit listing page into a grid view.

    ``subreddit`` is the declared capture target; rows whose ``thing`` markup
    names another subreddit (cross-posted link entries) keep their true home
    subreddit, which is honest provenance, not traversal.
    """
    if not subreddit.isascii() or not subreddit.replace("_", "").isalnum():
        raise RedditGridProjectionError("invalid_subreddit", f"invalid subreddit name: {subreddit!r}")
    if max_thread_rows <= 0:
        raise RedditGridProjectionError("invalid_cap", "max_thread_rows must be greater than zero")

    parser = _OldRedditGridParser(declared_subreddit=subreddit)
    parser.feed(html_text)

    rows: list[GridThreadRow] = []
    seen: set[str] = set()
    for row in parser.thread_rows:
        if row.thread_url in seen:
            continue
        rows.append(row)
        seen.add(row.thread_url)
        if len(rows) >= max_thread_rows:
            break

    absent_reason = None
    if parser.visible_subscriber_count is None and parser.visible_active_user_count is None:
        absent_reason = "visible_volume_not_present_on_declared_surface"

    return GridView(
        subreddit=subreddit,
        listing_url=listing_url,
        visible_subscriber_count_or_none=parser.visible_subscriber_count,
        visible_active_user_count_or_none=parser.visible_active_user_count,
        visible_volume_signal_absent_reason_or_none=absent_reason,
        thread_rows=tuple(rows),
    )


def build_grid_content_record(
    *,
    html_text: str,
    subreddit: str,
    listing_url: str,
) -> dict:
    """Project one grid page into the deterministic content-packet record.

    Pure function of its inputs (no timestamps, no environment reads) so a
    parser-fit check can re-project sampled raw bytes and compare the result
    byte-for-byte against the stored record.
    """
    view = project_old_reddit_grid_html(
        html_text=html_text,
        subreddit=subreddit,
        listing_url=listing_url,
    )
    return {
        "record_kind": GRID_CONTENT_RECORD_KIND,
        "parser_version": GRID_PROJECTION_PARSER_VERSION,
        "grid_view": grid_view_to_dict(view),
    }


def grid_view_to_dict(view: GridView) -> dict:
    payload = asdict(view)
    payload["thread_rows"] = list(payload["thread_rows"])
    return payload


def grid_view_from_record(record: dict) -> GridView:
    """Rebuild a GridView from a content-packet record (materializer read path)."""
    if not isinstance(record, dict) or record.get("record_kind") != GRID_CONTENT_RECORD_KIND:
        raise RedditGridProjectionError(
            "record_kind_mismatch",
            f"expected a {GRID_CONTENT_RECORD_KIND!r} record, got {record.get('record_kind') if isinstance(record, dict) else type(record).__name__!r}",
        )
    payload = record.get("grid_view")
    if not isinstance(payload, dict):
        raise RedditGridProjectionError("record_shape", "content record carries no grid_view object")
    try:
        rows = tuple(GridThreadRow(**row) for row in payload.get("thread_rows", []))
        return GridView(
            subreddit=payload["subreddit"],
            listing_url=payload["listing_url"],
            visible_subscriber_count_or_none=payload["visible_subscriber_count_or_none"],
            visible_active_user_count_or_none=payload["visible_active_user_count_or_none"],
            visible_volume_signal_absent_reason_or_none=payload["visible_volume_signal_absent_reason_or_none"],
            thread_rows=rows,
        )
    except (KeyError, TypeError) as exc:
        raise RedditGridProjectionError(
            "record_shape",
            f"content record grid_view does not match the GridView shape: {exc}",
        ) from exc


class _OldRedditGridParser(HTMLParser):
    """Single pass over a grid page: titlebox numbers + listing things.

    Thing rows prefer old Reddit's own machine attributes
    (``data-permalink`` / ``data-score`` / ``data-comments-count`` on
    ``div.thing``) and fall back to the title anchor plus visible score /
    comments text when an attribute is absent.
    """

    _VOID_TAGS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr",
    }

    def __init__(self, *, declared_subreddit: str) -> None:
        super().__init__(convert_charrefs=True)
        self.declared_subreddit = declared_subreddit
        self.thread_rows: list[GridThreadRow] = []
        self.visible_subscriber_count: str | None = None
        self.visible_active_user_count: str | None = None
        self._titlebox_depth = 0
        self._users_online_depth = 0
        self._capturing_number_for: str | None = None
        self._capturing_number_depth: int | None = None
        self._thing_depth = 0
        self._current: dict[str, str | bool | None] | None = None
        self._capturing_title_depth: int | None = None
        self._capturing_score_depth: int | None = None
        self._capturing_comments_depth: int | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key: value or "" for key, value in attrs}
        class_tokens = set(attr_map.get("class", "").split())

        self._advance_titlebox(tag, class_tokens)
        if "users-online" in class_tokens:
            self._users_online_depth += 1
        elif self._users_online_depth and tag not in self._VOID_TAGS:
            self._users_online_depth += 1
        if tag == "span" and "number" in class_tokens and self._titlebox_depth:
            target = "active_users" if self._users_online_depth else "subscribers"
            already_captured = (
                self.visible_active_user_count if target == "active_users" else self.visible_subscriber_count
            )
            # First complete span wins per field: a later same-class span must
            # not append onto an already-captured value; fragments within one
            # span still accumulate while the capture stays open.
            if already_captured is None:
                self._capturing_number_for = target
                self._capturing_number_depth = self._titlebox_depth

        if "thing" in class_tokens and not self._thing_depth:
            self._open_thing(attr_map, class_tokens)
            self._thing_depth = 1
            return
        if self._thing_depth and tag not in self._VOID_TAGS:
            self._thing_depth += 1

        if self._current is None:
            return
        if tag == "a" and _is_title_anchor(class_tokens):
            href = attr_map.get("href", "")
            if self._current.get("thread_url") is None:
                self._current["thread_url"] = canonical_old_reddit_thread_url(href)
            if self._current.get("title") is None:
                self._capturing_title_depth = self._thing_depth
        elif "score" in class_tokens and "unvoted" in class_tokens:
            if self._current.get("score") is None:
                self._capturing_score_depth = self._thing_depth
        elif tag == "a" and "comments" in class_tokens:
            if self._current.get("comments") is None:
                self._capturing_comments_depth = self._thing_depth

    def handle_data(self, data: str) -> None:
        value = " ".join(data.split())
        if self._capturing_number_for is not None and value:
            if self._capturing_number_for == "active_users":
                self.visible_active_user_count = _append_fragment(
                    self.visible_active_user_count,
                    value,
                    separator="",
                )
            else:
                self.visible_subscriber_count = _append_fragment(
                    self.visible_subscriber_count,
                    value,
                    separator="",
                )
        if self._current is None or not value:
            return
        if self._capturing_title_depth is not None:
            self._current["title"] = _append_fragment(
                _str_or_none(self._current.get("title")),
                value,
                separator=" ",
            )
        elif self._capturing_score_depth is not None:
            self._current["score"] = _append_fragment(
                _str_or_none(self._current.get("score")),
                value,
                separator="",
            )
        elif self._capturing_comments_depth is not None:
            self._current["comments"] = _append_fragment(
                _str_or_none(self._current.get("comments")),
                value,
                separator=" ",
            )

    def handle_endtag(self, tag: str) -> None:
        if (
            tag == "span"
            and self._capturing_number_depth is not None
            and self._capturing_number_depth == self._titlebox_depth
        ):
            self._capturing_number_for = None
            self._capturing_number_depth = None
        if tag not in self._VOID_TAGS:
            if self._capturing_title_depth == self._thing_depth:
                self._capturing_title_depth = None
            if self._capturing_score_depth == self._thing_depth:
                self._capturing_score_depth = None
            if self._capturing_comments_depth == self._thing_depth:
                self._capturing_comments_depth = None
            if self._titlebox_depth:
                self._titlebox_depth -= 1
            if self._users_online_depth:
                self._users_online_depth -= 1
            if self._thing_depth:
                self._thing_depth -= 1
                if not self._thing_depth:
                    self._close_thing()

    def _advance_titlebox(self, tag: str, class_tokens: set[str]) -> None:
        if "titlebox" in class_tokens:
            self._titlebox_depth += 1
        elif self._titlebox_depth and tag not in self._VOID_TAGS:
            self._titlebox_depth += 1

    def _open_thing(self, attr_map: dict[str, str], class_tokens: set[str]) -> None:
        permalink = attr_map.get("data-permalink", "")
        self._current = {
            "thread_url": canonical_old_reddit_thread_url(permalink) if permalink else None,
            "subreddit": attr_map.get("data-subreddit", "") or self.declared_subreddit,
            "title": None,
            "score": attr_map.get("data-score") or None,
            "comments": attr_map.get("data-comments-count") or None,
            "promoted": "promoted" in class_tokens or attr_map.get("data-promoted", "") == "true",
        }

    def _close_thing(self) -> None:
        current = self._current
        self._current = None
        self._capturing_title_depth = None
        self._capturing_score_depth = None
        self._capturing_comments_depth = None
        if current is None:
            return
        thread_url = current.get("thread_url")
        if not isinstance(thread_url, str) or thread_url is None:
            return
        self.thread_rows.append(
            GridThreadRow(
                thread_url=thread_url,
                subreddit=str(current.get("subreddit") or self.declared_subreddit),
                visible_title_or_none=_str_or_none(current.get("title")),
                visible_score_or_none=_str_or_none(current.get("score")),
                visible_comment_count_or_none=_extract_leading_count(current.get("comments")),
                promoted=bool(current.get("promoted")),
            )
        )


def _is_title_anchor(class_tokens: set[str]) -> bool:
    return "title" in class_tokens


def _str_or_none(value: object) -> str | None:
    # helper-delta: str-only vs harness_utils.string_or_none, which also
    # int-coerces; this copy returns None for a non-str (no coercion).
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _append_fragment(existing: str | None, value: str, *, separator: str) -> str:
    if existing is None:
        return value
    return f"{existing}{separator}{value}"


def _extract_leading_count(value: object) -> str | None:
    """``"128 comments"`` -> ``"128"``; ``"comment"`` -> None; passthrough digits."""
    text = _str_or_none(value)
    if text is None:
        return None
    match = re.match(r"^\s*(\d[\d,\s]*)", text)
    if match is not None:
        digits = match.group(1).replace(",", "").replace(" ", "")
        if digits.isdigit():
            return digits
    return None
