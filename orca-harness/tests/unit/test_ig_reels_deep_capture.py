"""Offline tests for the one-render deep-capture parser (media URL + combined).

No network/browser. Fixtures mirror the embedded shape: ``video_versions`` arrays
of ``{type,url}`` and ``XIGComment`` nodes, in a single DOM.
"""
from __future__ import annotations

import json

import pytest

from source_capture.ig_reels_deep_capture import (
    ReelDeepCapture,
    parse_reel_deep_capture_from_rendered_dom,
    parse_reel_media_urls_from_rendered_dom,
)

MEDIA_FIXTURE = r'''
<script>{"items":[{"pk":"m1","video_versions":[
{"type":101,"url":"https://instagram.fxx1-1.fna.fbcdn.net/o1/v/clip720.mp4?efg=abc"},
{"type":102,"url":"https:\/\/scontent.cdninstagram.com\/o1\/v\/clip480.mp4?x=1"},
{"type":103,"url":"https://evil.attacker.com/clip.mp4"},
{"type":104,"url":"https://x.fbcdn.net.attacker.com/spoof.mp4"}
],"__typename":"XIGMedia"}]}</script>
'''

BOTH_FIXTURE = r'''
<script>{"feed":[
{"node":{"pk":"c1","user":{"username":"zoe"},"text":"love this","created_at":1782400000,"comment_like_count":7,"id":"c1","__typename":"XIGComment"},"cursor":null}
],"media":{"video_versions":[{"type":101,"url":"https://scontent.cdninstagram.com/o1/v/clip.mp4?e=1"}],"__typename":"XIGMedia"}}</script>
'''


def _media_dom_for_url(url: str) -> str:
    return json.dumps({"video_versions": [{"type": 101, "url": url}]})


def test_extracts_only_ig_host_media_urls() -> None:
    urls = parse_reel_media_urls_from_rendered_dom(MEDIA_FIXTURE)
    # evil.attacker.com and the "x.fbcdn.net.attacker.com" suffix-spoof are rejected
    assert urls == [
        "https://instagram.fxx1-1.fna.fbcdn.net/o1/v/clip720.mp4?efg=abc",
        "https://scontent.cdninstagram.com/o1/v/clip480.mp4?x=1",
    ]


def test_no_video_versions_yields_empty() -> None:
    assert parse_reel_media_urls_from_rendered_dom("<html>no media</html>") == []


def test_malformed_video_versions_is_skipped_not_raised() -> None:
    dom = '<script>{"video_versions":[{"type":1,"url":"https://x.fbcdn.net/a.mp4"</script>'  # truncated
    assert parse_reel_media_urls_from_rendered_dom(dom) == []


def test_duplicate_media_urls_deduped() -> None:
    u = "https://scontent.cdninstagram.com/o1/v/dup.mp4"
    dom = f'{{"video_versions":[{{"type":1,"url":"{u}"}},{{"type":2,"url":"{u}"}}]}}'
    assert parse_reel_media_urls_from_rendered_dom(dom) == [u]


@pytest.mark.parametrize(
    "url",
    [
        "https://real.fbcdn.net@evil.com/x.mp4",
        "https://fbcdn.net.evil.com/x.mp4",
        "https://x.fbcdn.net.attacker.com/spoof.mp4",
        "data:text/plain,https://x.fbcdn.net/a.mp4",
        "blob:https://x.fbcdn.net/a.mp4",
        "https:///x.mp4",
        "https://fbcdn.net\u3002evil.com/x.mp4",
    ],
)
def test_rejects_media_url_host_bypasses(url: str) -> None:
    assert parse_reel_media_urls_from_rendered_dom(_media_dom_for_url(url)) == []


@pytest.mark.parametrize(
    "url",
    [
        "HTTPS://SCONTENT.CDNINSTAGRAM.COM/o1/v/clip.mp4",
        "https://scontent.cdninstagram.com./o1/v/clip.mp4",
        "https://scontent.cdninstagram.com:443/o1/v/clip.mp4",
        "https://fbcdn.net/o1/v/clip.mp4",
    ],
)
def test_accepts_legitimate_ig_cdn_host_forms(url: str) -> None:
    assert parse_reel_media_urls_from_rendered_dom(_media_dom_for_url(url)) == [url]


def test_unterminated_string_before_media_does_not_desync_scan() -> None:
    url = "https://scontent.cdninstagram.com/o1/v/recovered.mp4"
    dom = f'"unterminated user text <script>{_media_dom_for_url(url)}</script>'
    assert parse_reel_media_urls_from_rendered_dom(dom) == [url]


def test_video_versions_inside_comment_text_cannot_inject() -> None:
    # a comment whose TEXT embeds a video_versions literal must NOT yield a media URL
    dom = r'''<script>{"node":{"pk":"c","user":{"username":"mallory"},"text":"evil \"video_versions\":[{\"url\":\"https://real.fbcdn.net/inject.mp4\"}]","created_at":1782400000,"comment_like_count":1,"__typename":"XIGComment"}}</script>'''
    assert parse_reel_media_urls_from_rendered_dom(dom) == []


def test_one_dom_yields_both_voices() -> None:
    cap = parse_reel_deep_capture_from_rendered_dom(BOTH_FIXTURE, shortcode="ABC123")
    assert isinstance(cap, ReelDeepCapture)
    assert cap.reel_shortcode == "ABC123"
    assert len(cap.comments) == 1 and cap.comments[0].author_username == "zoe"
    assert cap.media_urls == ("https://scontent.cdninstagram.com/o1/v/clip.mp4?e=1",)
    assert cap.has_audio_handle is True


def test_deep_capture_blank_shortcode_rejected() -> None:
    with pytest.raises(ValueError):
        parse_reel_deep_capture_from_rendered_dom(BOTH_FIXTURE, shortcode="  ")
