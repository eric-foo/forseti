"""Pure parser: rendered IG reel-page DOM -> audience-comment evidence records.

No network, no browser, no LLM (this lives in the no-LLM capture zone; the live
runner renders a reel via the browser-snapshot adapter and hands the rendered DOM
here). It walks the page's embedded GraphQL JSON -- each comment is an
``XIGComment`` node ``{pk, user:{username}, text, created_at, parent_comment_id,
comment_like_count, ...}`` -- into validated ``AudienceComment`` records.

Total and honest: a node missing required fields (id, author, text, created_at)
is SKIPPED, never invented; comment text is parsed as DATA via the JSON decoder,
never executed. Records are de-duplicated by ``comment_id``.
"""
from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass

from pydantic import ValidationError

from schemas.audience_comment_models import AudienceComment

_COMMENT_TYPENAME = "XIGComment"
_TYPENAME_KEY_TOKEN = '"__typename"'
_COMMENT_TYPENAME_TOKEN = '"XIGComment"'
_MISSING = object()
_WS = " \t\r\n"


@dataclass
class _JsonFrame:
    kind: str
    start: int
    is_comment: bool = False


def _skip_ws(text: str, index: int) -> int:
    while index < len(text) and text[index] in _WS:
        index += 1
    return index


def _find_json_string_end(text: str, start: int) -> int | None:
    escaped = False
    index = start + 1
    while index < len(text):
        char = text[index]
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == '"':
            return index + 1
        index += 1
    return None


def _is_comment_typename_pair(text: str, key_start: int, key_end: int) -> bool:
    if text[key_start:key_end] != _TYPENAME_KEY_TOKEN:
        return False
    colon = _skip_ws(text, key_end)
    if colon >= len(text) or text[colon] != ":":
        return False
    value_start = _skip_ws(text, colon + 1)
    if value_start >= len(text) or text[value_start] != '"':
        return False
    value_end = _find_json_string_end(text, value_start)
    return value_end is not None and text[value_start:value_end] == _COMMENT_TYPENAME_TOKEN


def _iter_comment_node_sources(dom: str) -> Iterator[tuple[str, dict]]:
    """Yield each decoded ``XIGComment`` node dict from the embedded JSON.

    Scans JSON tokens once and decodes only complete objects that declare
    ``"__typename": "XIGComment"`` as an object field. String contents are
    skipped as data, so comment text cannot create parser structure.
    """
    n = len(dom)
    index = 0
    stack: list[_JsonFrame] = []
    while index < n:
        char = dom[index]
        if char == '"':
            end = _find_json_string_end(dom, index)
            if end is None:
                index += 1
                continue
            if stack and stack[-1].kind == "{" and _is_comment_typename_pair(dom, index, end):
                stack[-1].is_comment = True
            index = end
            continue
        if char in "{[":
            stack.append(_JsonFrame(kind=char, start=index))
            index += 1
            continue
        if char in "}]":
            expected = "{" if char == "}" else "["
            if stack and stack[-1].kind == expected:
                frame = stack.pop()
                if frame.kind == "{" and frame.is_comment:
                    try:
                        obj = json.loads(dom[frame.start : index + 1])
                    except json.JSONDecodeError:
                        pass
                    else:
                        if isinstance(obj, dict) and obj.get("__typename") == _COMMENT_TYPENAME:
                            yield dom[frame.start : index + 1], obj
            index += 1
            continue
        index += 1


def _iter_comment_nodes(dom: str) -> Iterator[dict]:
    for _source, node in _iter_comment_node_sources(dom):
        yield node


def extract_comment_substrate_from_rendered_dom(
    dom: str,
    *,
    shortcode: str,
    forbidden_strings: tuple[str, ...] = (),
) -> bytes:
    """Preserve the exact rendered-JSON objects that support admitted comments.

    The full rendered page also carries signed, expiring media handles and is not
    durable evidence.  This function therefore retains the source-exact
    ``XIGComment`` object substrings only.  A comment object containing a forbidden
    transient handle is excluded rather than rewritten; downstream parsing of the
    returned bytes consequently cannot admit text that the retained substrate does
    not prove.
    """
    if not shortcode or not shortcode.strip():
        raise ValueError("extract_comment_substrate_from_rendered_dom requires a non-empty shortcode")
    kept: list[str] = []
    seen: set[str] = set()
    for source, node in _iter_comment_node_sources(dom):
        if any(needle and needle in source for needle in forbidden_strings):
            continue
        parsed = parse_comments_from_rendered_dom(source, shortcode=shortcode)
        if len(parsed) != 1 or parsed[0].comment_id in seen:
            continue
        seen.add(parsed[0].comment_id)
        kept.append(source)
    return ("\n".join(kept) + ("\n" if kept else "")).encode("utf-8")


def parse_comments_from_rendered_dom(dom: str, *, shortcode: str) -> list[AudienceComment]:
    """Extract validated ``AudienceComment`` records from a rendered reel-page DOM.

    Deterministic and total: incomplete nodes are skipped (not faked) and records
    are de-duplicated by ``comment_id``. Only null/absent like counts are zero-filled.
    """
    if not shortcode or not shortcode.strip():
        raise ValueError("parse_comments_from_rendered_dom requires a non-empty shortcode")
    code = shortcode.strip()

    out: list[AudienceComment] = []
    seen: set[str] = set()
    for node in _iter_comment_nodes(dom):
        pk = node.get("pk") or node.get("id")
        user = node.get("user")
        username = user.get("username") if isinstance(user, dict) else None
        text = node.get("text")
        created = node.get("created_at")
        if not (
            pk
            and username
            and isinstance(text, str)
            and isinstance(created, int)
            and not isinstance(created, bool)
            and created >= 0
        ):
            continue  # incomplete node -> skip, never fake
        comment_id = str(pk)
        if comment_id in seen:
            continue
        seen.add(comment_id)

        likes_raw = node.get("comment_like_count", _MISSING)
        if likes_raw is _MISSING or likes_raw is None:
            like_count = 0
        elif isinstance(likes_raw, int) and not isinstance(likes_raw, bool) and likes_raw >= 0:
            like_count = likes_raw
        else:
            continue
        parent = node.get("parent_comment_id")
        try:
            out.append(
                AudienceComment(
                    comment_id=comment_id,
                    reel_shortcode=code,
                    author_username=str(username),
                    text=text,
                    like_count=like_count,
                    created_at_unix=int(created),
                    parent_comment_id=(str(parent) if parent else None),
                )
            )
        except ValidationError:
            continue
    return out
