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
from typing import Callable
from urllib.parse import urlparse

from schemas.audience_comment_models import AudienceComment
from source_capture.ig_reels_comments import parse_comments_from_rendered_dom

_VIDEO_VERSIONS_KEY = '"video_versions"'
_WS = " \t\r\n"
_DECODER = json.JSONDecoder()
# Instagram media CDNs. Matched on the normalized parsed host's registrable
# suffix, never a bare substring, so "x.fbcdn.net.attacker.com" does NOT pass.
_MEDIA_HOST_SUFFIXES = (".fbcdn.net", ".cdninstagram.com")
_MEDIA_HOSTS_EXACT = ("fbcdn.net", "cdninstagram.com")
_MEDIA_SCHEMES = {"http", "https"}


def _skip_ws(text: str, index: int) -> int:
    while index < len(text) and text[index] in _WS:
        index += 1
    return index


def _previous_non_ws(text: str, index: int) -> str | None:
    index -= 1
    while index >= 0 and text[index] in _WS:
        index -= 1
    return text[index] if index >= 0 else None


def _quote_is_escaped(text: str, index: int) -> bool:
    slash_count = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        slash_count += 1
        index -= 1
    return slash_count % 2 == 1


def _normalised_media_host(hostname: str | None) -> str | None:
    if not hostname:
        return None
    host = hostname.rstrip(".").lower()
    if not host:
        return None
    try:
        host.encode("ascii")
    except UnicodeEncodeError:
        return None
    return host


def _is_ig_media_url(url: str) -> bool:
    if not isinstance(url, str):
        return False
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    if parsed.scheme.lower() not in _MEDIA_SCHEMES:
        return False
    host = _normalised_media_host(parsed.hostname)
    if host is None:
        return False
    return host in _MEDIA_HOSTS_EXACT or host.endswith(_MEDIA_HOST_SUFFIXES)


def parse_reel_media_urls_from_rendered_dom(dom: str) -> list[str]:
    """Extract the progressive (audio-bearing) media URLs from ``video_versions``.

    TRANSIENT handles -- signed + expiring; download immediately, never persist.
    Returns IG-CDN-host-validated URLs in document order, de-duplicated.

    String-data-safe: the scan only accepts unescaped ``"video_versions"`` object
    keys after ``{`` or ``,`` and before a JSON array. A literal embedded inside
    JSON string data is escaped and is not parsed as structure, so comment text
    cannot inject a media URL. Malformed earlier strings do not desync the scan.
    """
    urls: list[str] = []
    seen: set[str] = set()
    n = len(dom)
    search = 0
    while search < n:
        key_start = dom.find(_VIDEO_VERSIONS_KEY, search)
        if key_start == -1:
            break
        key_end = key_start + len(_VIDEO_VERSIONS_KEY)
        search = key_end
        if _quote_is_escaped(dom, key_start):
            continue
        if _previous_non_ws(dom, key_start) not in {"{", ","}:
            continue
        colon = _skip_ws(dom, key_end)
        if colon >= n or dom[colon] != ":":
            continue
        bracket = _skip_ws(dom, colon + 1)
        if bracket >= n or dom[bracket] != "[":
            continue
        try:
            versions, array_end = _DECODER.raw_decode(dom, bracket)
        except json.JSONDecodeError:
            continue
        if not isinstance(versions, list):
            continue
        search = max(search, array_end)
        for item in versions:
            if not isinstance(item, dict):
                continue
            url = item.get("url")
            if _is_ig_media_url(url) and url not in seen:
                seen.add(url)
                urls.append(url)
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


# --- live orchestration (PURE: all network/CPU I/O is injected, so offline-testable) ---

RenderFn = Callable[[str], "str | None"]                        # shortcode -> rendered DOM (None on fail/gate)
DownloadFn = Callable[[str], "str | None"]                      # media url -> local audio path (None on fail)
TranscribeFn = Callable[[str], "tuple[str, list[dict], dict]"]  # audio path -> (posture, cues, model_info)


@dataclass(frozen=True)
class ReelDeepCaptureResult:
    """The payoff of ONE render: the audience comments AND the creator transcript.

    ``media_url_used`` is the transient handle that was downloaded (never persisted).
    ``transcript_posture`` is the transcriber's 'ok'/'no_speech'/'failed', or a runner
    status ('render_unavailable' / 'no_audio_handle' / 'download_failed') when an
    earlier step did not yield audio. Comments are still returned whenever the render
    succeeded, even if the audio leg failed.
    """

    reel_shortcode: str
    comments: tuple[AudienceComment, ...]
    transcript_posture: str
    transcript_cues: tuple[dict, ...]
    media_url_used: str | None
    notes: tuple[str, ...] = ()


def run_reel_deep_capture(
    shortcode: str,
    *,
    render_fn: RenderFn,
    download_fn: DownloadFn,
    transcribe_fn: TranscribeFn,
) -> ReelDeepCaptureResult:
    """Render ONCE, then derive BOTH voices from that single render: the audience
    comments (parsed from the DOM) and the creator transcript (by downloading and
    transcribing the same render's audio handle) -- no second fetch.

    Every side-effecting step is injected, so the control flow is deterministic and
    offline-testable; the runner CLI supplies the real render/download/transcribe.
    """
    if not shortcode or not shortcode.strip():
        raise ValueError("run_reel_deep_capture requires a non-empty shortcode")
    code = shortcode.strip()

    dom = render_fn(code)
    if not dom:
        return ReelDeepCaptureResult(code, (), "render_unavailable", (), None, ("render returned no DOM",))

    capture = parse_reel_deep_capture_from_rendered_dom(dom, shortcode=code)
    if not capture.media_urls:
        return ReelDeepCaptureResult(
            code, capture.comments, "no_audio_handle", (), None, ("no media handle in the rendered DOM",)
        )

    media_url = capture.media_urls[0]
    audio_path = download_fn(media_url)
    if not audio_path:
        return ReelDeepCaptureResult(
            code, capture.comments, "download_failed", (), media_url, ("audio handle did not download",)
        )

    posture, cues, _model_info = transcribe_fn(audio_path)
    return ReelDeepCaptureResult(code, capture.comments, posture, tuple(cues), media_url)
