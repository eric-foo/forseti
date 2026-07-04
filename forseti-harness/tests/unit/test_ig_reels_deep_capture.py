"""Offline tests for the one-render deep-capture parser (media URL + combined).

No network/browser. Fixtures mirror the embedded shape: ``video_versions`` arrays
of ``{type,url}`` and ``XIGComment`` nodes, in a single DOM.
"""
from __future__ import annotations

from email.message import Message
import io
import json
from pathlib import Path
from types import SimpleNamespace
from urllib.error import HTTPError

import pytest

from runners import run_source_capture_ig_reels_deep_capture as deep_capture_runner
from source_capture.adapters.browser_snapshot import (
    BrowserSnapshotFailure,
    BrowserSnapshotFailureKind,
)

from source_capture.ig_reels_deep_capture import (
    ReelDeepCapture,
    ReelDeepCaptureResult,
    parse_reel_deep_capture_from_rendered_dom,
    parse_reel_media_urls_from_rendered_dom,
    run_reel_deep_capture,
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


class _FakeMediaResponse:
    def __init__(self, url: str, body: bytes, headers: dict[str, str] | None = None):
        self._url = url
        self._body = io.BytesIO(body)
        self.headers = headers or {}

    def geturl(self) -> str:
        return self._url

    def read(self, size: int = -1) -> bytes:
        return self._body.read(size)

    def __enter__(self) -> "_FakeMediaResponse":
        return self

    def __exit__(self, *_exc: object) -> bool:
        return False


def _redirect_error(url: str, location: str) -> HTTPError:
    headers = Message()
    headers["Location"] = location
    return HTTPError(url, 302, "Found", headers, fp=None)


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


# --- live orchestration (offline: render/download/transcribe are injected fakes) ---


def test_run_reel_deep_capture_happy_path() -> None:
    seen: dict[str, str] = {}

    def render(code: str) -> str:
        seen["render"] = code
        return BOTH_FIXTURE

    def download(url: str) -> str:
        seen["download"] = url
        return "/tmp/fake.mp4"

    def transcribe(path: str):
        seen["transcribe"] = path
        return ("ok", [{"text": "hi", "start_ms": 0, "end_ms": 90}], {"model": "small"})

    res = run_reel_deep_capture("ABC123", render_fn=render, download_fn=download, transcribe_fn=transcribe)
    assert isinstance(res, ReelDeepCaptureResult)
    assert res.reel_shortcode == "ABC123"
    assert len(res.comments) == 1 and res.comments[0].author_username == "zoe"
    assert res.transcript_posture == "ok" and len(res.transcript_cues) == 1
    assert res.media_url_used == "https://scontent.cdninstagram.com/o1/v/clip.mp4?e=1"
    # downloaded exactly the extracted handle, then transcribed that file
    assert seen["download"] == res.media_url_used and seen["transcribe"] == "/tmp/fake.mp4"


def test_run_reel_deep_capture_render_unavailable_returns_no_comments() -> None:
    res = run_reel_deep_capture(
        "ABC",
        render_fn=lambda c: None,
        download_fn=lambda u: pytest.fail("must not download when render failed"),
        transcribe_fn=lambda p: pytest.fail("must not transcribe when render failed"),
    )
    assert res.transcript_posture == "render_unavailable"
    assert res.comments == () and res.media_url_used is None


def test_run_reel_deep_capture_no_audio_handle_still_returns_comments() -> None:
    dom = r'''<script>{"node":{"pk":"c1","user":{"username":"zoe"},"text":"hi","created_at":1,"comment_like_count":1,"id":"c1","__typename":"XIGComment"}}</script>'''
    res = run_reel_deep_capture(
        "ABC",
        render_fn=lambda c: dom,
        download_fn=lambda u: pytest.fail("must not download with no media handle"),
        transcribe_fn=lambda p: ("ok", [], {}),
    )
    assert res.transcript_posture == "no_audio_handle"
    assert len(res.comments) == 1 and res.media_url_used is None


def test_run_reel_deep_capture_download_failed_keeps_comments() -> None:
    res = run_reel_deep_capture(
        "ABC",
        render_fn=lambda c: BOTH_FIXTURE,
        download_fn=lambda u: None,
        transcribe_fn=lambda p: pytest.fail("must not transcribe when download failed"),
    )
    assert res.transcript_posture == "download_failed"
    assert res.media_url_used is not None and len(res.comments) == 1


def test_run_reel_deep_capture_blank_shortcode_rejected() -> None:
    with pytest.raises(ValueError):
        run_reel_deep_capture("  ", render_fn=lambda c: "", download_fn=lambda u: "", transcribe_fn=lambda p: ("ok", [], {}))


def test_deep_capture_downloader_follows_ig_cdn_redirect(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    requested = "https://scontent.cdninstagram.com/o1/v/clip.mp4"
    redirected = "https://instagram.fxx1-1.fna.fbcdn.net/o1/v/clip.mp4"
    opened: list[str] = []

    def fake_open(request, *, timeout_seconds: float):  # noqa: ANN001
        opened.append(request.full_url)
        if request.full_url == requested:
            raise _redirect_error(request.full_url, redirected)
        return _FakeMediaResponse(request.full_url, b"mp4data")

    monkeypatch.setattr(deep_capture_runner, "_open_media_url", fake_open)

    download = deep_capture_runner._make_downloader(str(tmp_path))
    path = download(requested)

    assert path is not None
    assert opened == [requested, redirected]
    assert Path(path).read_bytes() == b"mp4data"


def test_deep_capture_downloader_rejects_off_host_redirect_before_fetch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    requested = "https://scontent.cdninstagram.com/o1/v/clip.mp4"
    opened: list[str] = []

    def fake_open(request, *, timeout_seconds: float):  # noqa: ANN001
        opened.append(request.full_url)
        raise _redirect_error(request.full_url, "https://evil.example/clip.mp4")

    monkeypatch.setattr(deep_capture_runner, "_open_media_url", fake_open)

    download = deep_capture_runner._make_downloader(str(tmp_path))

    assert download(requested) is None
    assert opened == [requested]
    assert not (tmp_path / "reel_audio.mp4").exists()


def test_deep_capture_downloader_rejects_response_over_size_cap(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    requested = "https://scontent.cdninstagram.com/o1/v/clip.mp4"

    def fake_open(request, *, timeout_seconds: float):  # noqa: ANN001
        return _FakeMediaResponse(request.full_url, b"abcdef")

    monkeypatch.setattr(deep_capture_runner, "_open_media_url", fake_open)

    download = deep_capture_runner._make_downloader(str(tmp_path), max_bytes=5)

    assert download(requested) is None
    assert not (tmp_path / "reel_audio.mp4").exists()


def test_deep_capture_downloader_rejects_http_media_url_before_fetch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    opened: list[str] = []

    def fake_open(request, *, timeout_seconds: float):  # noqa: ANN001
        opened.append(request.full_url)
        return _FakeMediaResponse(request.full_url, b"mp4data")

    monkeypatch.setattr(deep_capture_runner, "_open_media_url", fake_open)

    download = deep_capture_runner._make_downloader(str(tmp_path))

    assert download("http://scontent.cdninstagram.com/o1/v/clip.mp4") is None
    assert opened == []
    assert not (tmp_path / "reel_audio.mp4").exists()


# --- _render retry/robustness (offline: the browser-snapshot capture is an injected fake) ---


def _snapshot_failure(kind: BrowserSnapshotFailureKind) -> BrowserSnapshotFailure:
    return BrowserSnapshotFailure(
        requested_url="https://www.instagram.com/reel/X/", failure_kind=kind, message="boom"
    )


def test_render_retries_transient_failure_then_succeeds() -> None:
    calls: list[dict] = []
    slept: list[float] = []
    outcomes = [
        _snapshot_failure(BrowserSnapshotFailureKind.TIMEOUT),
        _snapshot_failure(BrowserSnapshotFailureKind.EMPTY_RENDERED_DOM),
        SimpleNamespace(rendered_dom="<html>reel</html>"),
    ]

    def capture(**kwargs: object):
        calls.append(kwargs)
        return outcomes[len(calls) - 1]

    dom = deep_capture_runner._render("DaGUhsKsYL9", capture_fn=capture, sleep_fn=slept.append)

    assert dom == "<html>reel</html>"
    assert len(calls) == 3
    # the regression guard: deep-capture must wait on `load`, never the flaky `networkidle`
    assert all(call["wait_until"] == "load" for call in calls)
    assert slept == [2.0, 4.0]  # linear backoff between attempts, none after the success


def test_render_returns_none_after_exhausting_transient_retries() -> None:
    calls: list[dict] = []
    slept: list[float] = []

    def capture(**kwargs: object):
        calls.append(kwargs)
        return _snapshot_failure(BrowserSnapshotFailureKind.TIMEOUT)

    dom = deep_capture_runner._render("ABC", attempts=3, capture_fn=capture, sleep_fn=slept.append)

    assert dom is None
    assert len(calls) == 3 and slept == [2.0, 4.0]


def test_render_does_not_retry_permanent_failure() -> None:
    calls: list[dict] = []
    slept: list[float] = []

    def capture(**kwargs: object):
        calls.append(kwargs)
        return _snapshot_failure(BrowserSnapshotFailureKind.DEPENDENCY_UNAVAILABLE)

    dom = deep_capture_runner._render("ABC", capture_fn=capture, sleep_fn=slept.append)

    assert dom is None
    assert len(calls) == 1 and slept == []  # permanent failure: no retry, no backoff
