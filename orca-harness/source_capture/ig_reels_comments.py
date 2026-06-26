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
from json import JSONDecoder

from schemas.audience_comment_models import AudienceComment

_DECODER = JSONDecoder()
_COMMENT_TYPENAME = "XIGComment"
_COMMENT_MARKER = '"__typename":"XIGComment"'
_NODE_KEY = '"node":'
_WS = " \t\r\n"


def _iter_comment_nodes(dom: str):
    """Yield each decoded ``XIGComment`` node dict from the embedded JSON.

    Anchors on the comment marker, then JSON-decodes the enclosing ``"node":{..}``
    object (the JSON decoder, not regex, owns brace/quote/escape correctness).
    """
    n = len(dom)
    search_from = 0
    while True:
        marker = dom.find(_COMMENT_MARKER, search_from)
        if marker == -1:
            return
        search_from = marker + 1
        key = dom.rfind(_NODE_KEY, 0, marker)  # the "node": that opens this comment
        if key == -1:
            continue
        brace = key + len(_NODE_KEY)
        while brace < n and dom[brace] in _WS:
            brace += 1
        if brace >= n or dom[brace] != "{":
            continue
        try:
            obj, _ = _DECODER.raw_decode(dom, brace)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and obj.get("__typename") == _COMMENT_TYPENAME:
            yield obj


def parse_comments_from_rendered_dom(dom: str, *, shortcode: str) -> list[AudienceComment]:
    """Extract validated ``AudienceComment`` records from a rendered reel-page DOM.

    Deterministic and total: incomplete nodes are skipped (not faked) and records
    are de-duplicated by ``comment_id``. A null/absent like count is a truthful 0.
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
        if not (pk and username and isinstance(text, str) and isinstance(created, int)):
            continue  # incomplete node -> skip, never fake
        comment_id = str(pk)
        if comment_id in seen:
            continue
        seen.add(comment_id)

        likes_raw = node.get("comment_like_count")
        like_count = likes_raw if isinstance(likes_raw, int) and likes_raw >= 0 else 0
        parent = node.get("parent_comment_id")
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
    return out
