"""Pure parser: ONE rendered IG reel-page DOM -> BOTH voices in a single render.

Proves "one visit gets both": the live runner renders a reel ONCE via the
browser-snapshot adapter and hands the rendered DOM here, which composes
- the audience-comment parser (``ig_reels_comments``), and
- a media-URL parser over ``video_versions`` (the audio handle),
so a single render yields the creator-voice audio handle AND the audience-voice
comments without the second fetch the yt-dlp audio path would cost.

No network, no browser, no LLM. Media URLs are TRANSIENT: Instagram signs them
and they expire, so they are returned for IMMEDIATE download and are NEVER
persisted as durable evidence (unlike ``AudienceComment``). They are host-validated
to Instagram CDNs so a ``video_versions`` literal embedded inside comment text
cannot inject an arbitrary URL.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.parse import urlparse

from schemas.audience_comment_models import AudienceComment
from source_capture.ig_reels_comments import parse_comments_from_rendered_dom

_VIDEO_VERSIONS_KEY = '"video_versions"'
_WS = " \t\r\n"
_DECODER = json.JSONDecoder()
# Instagram media CDNs. Matched on the parsed host's registrable suffix (endswith),
# never a bare substring, so "x.fbcdn.net.attacker.com" does NOT pass.
_MEDIA_HOST_SUFFIXES = (".fbcdn.net", ".cdninstagram.com")
_MEDIA_HOSTS_EXACT = ("fbcdn.net", "cdninstagram.com")


def _skip_ws(text: str, index: int) -> int:
    while index < len(text) and text[index] in _WS:
        index += 1
    return index


def _is_ig_media_url(url: str) -> bool:
    if not isinstance(url, str) or not url.startswith(("http://", "https://")):
        return False
    try:
        host = (urlparse(url).hostname or "").lower()
    except ValueError:
        return False
    return host in _MEDIA_HOSTS_EXACT or host.endswith(_MEDIA_HOST_SUFFIXES)


def _find_json_string_end(text: str, start: int) -> int | None:
    """Index just past the closing quote of the JSON string opening at ``start``."""
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


def parse_reel_media_urls_from_rendered_dom(dom: str) -> list[str]:
    """Extract the progressive (audio-bearing) media URLs from ``video_versions``.

    TRANSIENT handles -- signed + expiring; download immediately, never persist.
    Returns IG-CDN-host-validated URLs in document order, de-duplicated.

    String-aware: the scan skips over JSON string CONTENTS, so a ``video_versions``
    literal embedded inside comment text is never parsed as structure -- it cannot
    inject a media URL.
    """
    urls: list[str] = []
    seen: set[str] = set()
    n = len(dom)
    index = 0
    while index < n:
        if dom[index] != '"':
            index += 1
            continue
        end = _find_json_string_end(dom, index)
        if end is None:
            break
        if dom[index:end] == _VIDEO_VERSIONS_KEY:
            colon = _skip_ws(dom, end)
            if colon < n and dom[colon] == ":":
                bracket = _skip_ws(dom, colon + 1)
                if bracket < n and dom[bracket] == "[":
                    try:
                        versions, _ = _DECODER.raw_decode(dom, bracket)
                    except json.JSONDecodeError:
                        versions = None
                    if isinstance(versions, list):
                        for item in versions:
                            if not isinstance(item, dict):
                                continue
                            url = item.get("url")
                            if _is_ig_media_url(url) and url not in seen:
                                seen.add(url)
                                urls.append(url)
        index = end  # advance past the whole string (its contents are never re-scanned)
    return urls


@dataclass(frozen=True)
class ReelDeepCapture:
    """Both signals harvested from ONE reel render.

    ``comments`` are durable evidence; ``media_urls`` are TRANSIENT (signed +
    expiring) audio handles for immediate download, never persisted.
    """

    reel_shortcode: str
    comments: tuple[AudienceComment, ...]
    media_urls: tuple[str, ...]

    @property
    def has_audio_handle(self) -> bool:
        return bool(self.media_urls)


def parse_reel_deep_capture_from_rendered_dom(dom: str, *, shortcode: str) -> ReelDeepCapture:
    """Compose the comment parser and the media-URL parser over ONE rendered DOM."""
    if not shortcode or not shortcode.strip():
        raise ValueError("parse_reel_deep_capture_from_rendered_dom requires a non-empty shortcode")
    comments = parse_comments_from_rendered_dom(dom, shortcode=shortcode)
    media_urls = parse_reel_media_urls_from_rendered_dom(dom)
    return ReelDeepCapture(
        reel_shortcode=shortcode.strip(),
        comments=tuple(comments),
        media_urls=tuple(media_urls),
    )
