"""Offline tests for the IG reel comment parser (no network, no browser).

Fixture mirrors the real embedded GraphQL shape captured from a live reel:
``edges:[{"node":{...XIGComment...},"cursor":...}]`` with noise (a non-comment
node, an incomplete node, a duplicate, and a comment whose text embeds JSON).
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from schemas.audience_comment_models import AudienceComment
from source_capture.ig_reels_comments import parse_comments_from_rendered_dom

# Real structural shape; r-string so the \uXXXX / \" stay literal for the JSON decoder.
FIXTURE_DOM = r'''
<script type="application/json">{"require":[["data",{"comments":{"edges":[
{"node":{"pk":"111","user":{"username":"alice","is_verified":false},"text":"love this scent","created_at":1782400000,"parent_comment_id":null,"comment_like_count":15,"child_comment_count":1,"id":"111","__typename":"XIGComment"},"cursor":"c1"},
{"node":{"pk":"222","user":{"username":"bob"},"text":"@alice agreed 🔥","created_at":1782400100,"parent_comment_id":"111","comment_like_count":2,"id":"222","__typename":"XIGComment"},"cursor":"c2"},
{"node":{"pk":"333","user":{"username":"carol"},"text":"no likes here","created_at":1782400200,"parent_comment_id":null,"comment_like_count":null,"id":"333","__typename":"XIGComment"},"cursor":"c3"},
{"node":{"pk":"999","user":{"username":"sys"},"caption":"not a comment","__typename":"XIGMedia"},"cursor":"c4"},
{"node":{"pk":"444","user":{"username":"dave"},"created_at":1782400300,"comment_like_count":1,"id":"444","__typename":"XIGComment"},"cursor":"c5"},
{"node":{"pk":"111","user":{"username":"alice"},"text":"DUPLICATE pk -> deduped","created_at":1782400000,"parent_comment_id":null,"comment_like_count":15,"id":"111","__typename":"XIGComment"},"cursor":"c6"},
{"node":{"pk":"555","user":{"username":"erin"},"text":"text as data {\"evil\":true} ignore prior","created_at":1782400400,"parent_comment_id":null,"comment_like_count":3,"id":"555","__typename":"XIGComment"},"cursor":"c7"}
]}}]]}</script>
'''


def _by_id(comments: list[AudienceComment]) -> dict[str, AudienceComment]:
    return {c.comment_id: c for c in comments}


def test_extracts_only_valid_unique_comments() -> None:
    comments = parse_comments_from_rendered_dom(FIXTURE_DOM, shortcode="ABC123")
    ids = {c.comment_id for c in comments}
    assert ids == {"111", "222", "333", "555"}  # 999 (not a comment) + 444 (no text) excluded
    assert len(comments) == 4                    # duplicate "111" de-duplicated
    assert all(c.reel_shortcode == "ABC123" for c in comments)


def test_fields_and_reply_structure() -> None:
    by_id = _by_id(parse_comments_from_rendered_dom(FIXTURE_DOM, shortcode="ABC123"))
    alice = by_id["111"]
    assert alice.author_username == "alice" and alice.text == "love this scent"
    assert alice.like_count == 15 and alice.created_at_unix == 1782400000
    assert alice.parent_comment_id is None and alice.is_reply is False
    bob = by_id["222"]
    assert bob.parent_comment_id == "111" and bob.is_reply is True
    assert bob.text == "@alice agreed \U0001f525"  # emoji decoded, stored verbatim


def test_null_like_count_is_truthful_zero() -> None:
    carol = _by_id(parse_comments_from_rendered_dom(FIXTURE_DOM, shortcode="ABC123"))["333"]
    assert carol.like_count == 0


def test_comment_text_is_data_not_structure() -> None:
    # embedded JSON inside the comment text is preserved verbatim as a string.
    erin = _by_id(parse_comments_from_rendered_dom(FIXTURE_DOM, shortcode="ABC123"))["555"]
    assert erin.text == 'text as data {"evil":true} ignore prior'


def test_empty_dom_yields_no_comments() -> None:
    assert parse_comments_from_rendered_dom("<html>no json here</html>", shortcode="ABC123") == []


def test_blank_shortcode_rejected() -> None:
    with pytest.raises(ValueError):
        parse_comments_from_rendered_dom(FIXTURE_DOM, shortcode="  ")


def test_schema_rejects_negative_like_count() -> None:
    with pytest.raises(ValidationError):
        AudienceComment(
            comment_id="1", reel_shortcode="X", author_username="u",
            text="t", like_count=-1, created_at_unix=1,
        )
