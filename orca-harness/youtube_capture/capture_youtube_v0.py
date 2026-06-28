#!/usr/bin/env python3
"""Bounded YouTube public-metadata capture v0 (tracked code; captured data gitignored).

Proven route (see source_families/social_media/youtube/youtube_capture_recon_v0.md):
  - metadata: embedded `ytInitialPlayerResponse` in served HTML (logged-out, no JS)
  - comments: `youtubei/v1/next` panel-scoped continuation (same route long-form + Shorts)

Persists one packet per video to ./packets/<video_id>/. Public read-only; no auth; no scheduler.
Tracked at orca-harness/youtube_capture/. Helpers here are reused by shorts_scroll_capture_v0.py.
"""
import re, json, os, hashlib, datetime, urllib.request
from dataclasses import dataclass, field

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packets")
COMMENT_PAGES = 2  # bounded
VIDEOS = ["dQw4w9WgXcQ", "-0FVExAgmps", "84id2dzpwU0", "__fmDj0ZJ1Q"]  # longform, short, comments-off, recent


try:
    from .stealth_client import http_get, BACKEND  # type: ignore[import-not-found]
except ImportError:  # script-mode compatibility
    from stealth_client import http_get, BACKEND  # Chrome-impersonating client (curl_cffi) + urllib fallback


VIDEO_AVAILABILITY_STATES = {
    "playable",
    "removed_by_uploader",
    "private",
    "age_restricted",
    "login_required",
    "region_blocked",
    "unknown",
}
COMMENT_AVAILABILITY_STATES = {
    "comments_disabled",
    "comments_not_exposed",
    "comments_sample_captured",
}


@dataclass(frozen=True)
class YoutubeCommentPageBody:
    filename: str
    raw_json_bytes: bytes
    http_status: int
    final_url: str


@dataclass(frozen=True)
class YoutubeWatchFetchResult:
    packet: dict
    raw_watch_html: bytes
    comment_page_bodies: tuple[YoutubeCommentPageBody, ...] = field(default_factory=tuple)


def ytinit(html):
    return embedded_json(html, "ytInitialData")


def ytplayer(html):
    return embedded_json(html, "ytInitialPlayerResponse")


def embedded_json(html, marker):
    idx = html.find(marker)
    if idx < 0:
        return None
    start = html.find("{", idx)
    if start < 0:
        return None
    depth = 0
    in_string = False
    escape = False
    for i, c in enumerate(html[start:], start=start):
        if in_string:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == '"':
                in_string = False
        else:
            if c == '"':
                in_string = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(html[start : i + 1])
                    except Exception:
                        return None
    return None


def _rec(x, pred, out):
    if isinstance(x, dict):
        if pred(x):
            out.append(x)
        for v in x.values():
            _rec(v, pred, out)
    elif isinstance(x, list):
        for v in x:
            _rec(v, pred, out)


def comment_panel_token(data):
    out = []
    _rec(data, lambda d: "engagementPanelSectionListRenderer" in d
         and "comment" in json.dumps(d["engagementPanelSectionListRenderer"])[:400].lower(), out)
    if not out:
        return None
    toks = []
    _rec(out[0], lambda d: isinstance(d.get("continuationCommand"), dict) and d["continuationCommand"].get("token"), toks)
    return toks[0]["continuationCommand"]["token"] if toks else None


def next_token(obj):
    toks = []
    _rec(obj, lambda d: isinstance(d.get("continuationCommand"), dict) and d["continuationCommand"].get("token"), toks)
    return toks[-1]["continuationCommand"]["token"] if toks else None


def collect(obj, key):
    out = []
    _rec(obj, lambda d: key in d, out)
    return [d[key] for d in out]


def youtubei_next_raw(api_key, ver, token):
    body = json.dumps({"context": {"client": {"clientName": "WEB", "clientVersion": ver, "hl": "en", "gl": "US"}},
                       "continuation": token}).encode()
    status, final_url, raw = http_get(
        f"https://www.youtube.com/youtubei/v1/next?key={api_key}&prettyPrint=false", data=body
    )
    return status, final_url, raw, json.loads(raw)


def youtubei_next(api_key, ver, token):
    return youtubei_next_raw(api_key, ver, token)[3]


def first(pattern, text, cast=str):
    m = re.search(pattern, text)
    return cast(m.group(1)) if m else None


def _integer(value):
    if isinstance(value, bool):
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


def player_view_count(player):
    video_details = (player or {}).get("videoDetails") or {}
    count = _integer(video_details.get("viewCount"))
    if count is not None:
        return count, "ytInitialPlayerResponse.videoDetails.viewCount"

    microformat = ((player or {}).get("microformat") or {}).get("playerMicroformatRenderer") or {}
    count = _integer(microformat.get("viewCount"))
    if count is not None:
        return count, "ytInitialPlayerResponse.microformat.playerMicroformatRenderer.viewCount"

    return None, None


def player_like_count(player):
    microformat = ((player or {}).get("microformat") or {}).get("playerMicroformatRenderer") or {}
    count = _integer(microformat.get("likeCount"))
    if count is not None:
        return count, "ytInitialPlayerResponse.microformat.playerMicroformatRenderer.likeCount"
    return None, None


def extract_view_count(html):
    count, source_path = player_view_count(ytplayer(html))
    if count is not None:
        return count, source_path
    count = first(r'"viewCount":"([0-9]+)"', html, int)
    return count, "served_html.regex.first_viewCount" if count is not None else None


def extract_like_count(html):
    count, source_path = player_like_count(ytplayer(html))
    if count is not None:
        return count, source_path
    return None, None


def _route_from_source_path(source_path):
    if not source_path:
        return None
    if source_path.startswith("ytInitialPlayerResponse.microformat"):
        return "ytInitialPlayerResponse.microformat"
    if source_path.startswith("ytInitialPlayerResponse.videoDetails"):
        return "ytInitialPlayerResponse.videoDetails"
    if source_path.startswith("served_html.regex"):
        return "served_html.regex"
    if source_path.startswith("youtubei_next"):
        return "youtubei_next"
    return source_path.split(".")[0]


def _metric_observed(value, source_path, *, artifact):
    return {
        "posture": "observed",
        "value": value,
        "source_route": _route_from_source_path(source_path),
        "source_path": source_path,
        "artifact": artifact,
    }


def _metric_unavailable(reason, *, routes_checked):
    return {
        "posture": "unavailable_with_reason",
        "reason": reason,
        "routes_checked": list(routes_checked),
    }


def _text_from_youtube_runs(value):
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, dict):
        simple = value.get("simpleText")
        if isinstance(simple, str):
            return simple.strip() or None
        runs = value.get("runs")
        if isinstance(runs, list):
            text = "".join(str(run.get("text") or "") for run in runs if isinstance(run, dict))
            return text.strip() or None
    return None


def parse_exact_count_text(text):
    if not isinstance(text, str):
        return None
    stripped = text.strip()
    if not stripped:
        return None
    if re.search(r"(?<!\d)\d[\d,]*\.\d+\s*[kmb]?\b", stripped, re.IGNORECASE):
        return None
    if re.search(r"(?<!\d)\d[\d,]*\s*[kmb]\b", stripped, re.IGNORECASE):
        return None
    match = re.search(
        r"(?<![\d.])(\d{1,3}(?:,\d{3})+|\d+)\s*(?:comments?|likes?|views?)?\b",
        stripped,
        re.IGNORECASE,
    )
    if not match:
        return None
    return _integer(match.group(1))


def _playability_reason(player):
    status = ((player or {}).get("playabilityStatus") or {})
    return " ".join(
        str(part or "")
        for part in [
            status.get("status"),
            status.get("reason"),
            _text_from_youtube_runs(status.get("messages")),
        ]
    ).strip()


def detect_video_state(*, status, final_url, html, player):
    final_low = (final_url or "").lower()
    playability_probe = _playability_reason(player).lower()
    served_probe = (html or "")[:200000].lower()
    probe = f"{playability_probe}\n{served_probe}"
    play_status = (((player or {}).get("playabilityStatus") or {}).get("status") or "").upper()
    if play_status == "OK":
        return "playable", "ytInitialPlayerResponse.playabilityStatus.status=OK"
    if "removed by the uploader" in probe or "video has been removed" in probe:
        return "removed_by_uploader", "playability or served HTML reports removed by uploader"
    if "private video" in probe or "this video is private" in probe:
        return "private", "playability or served HTML reports private video"
    if "age-restricted" in probe or "confirm your age" in probe:
        return "age_restricted", "playability or served HTML reports age restriction"
    if (
        "not available in your country" in probe
        or "not available in this country" in probe
        or "blocked in your country" in probe
        or "unavailable in your location" in probe
        or "not available in your region" in probe
    ):
        return "region_blocked", "playability or served HTML reports region restriction"
    if (
        play_status == "LOGIN_REQUIRED"
        or "sign in" in playability_probe
        or "login" in playability_probe
        or "consent.youtube.com" in final_low
    ):
        return "login_required", "served route requires sign-in/consent before metadata is exposed"
    if status == 200 and player:
        return "playable", "ytInitialPlayerResponse present; no blocking playability reason found"
    return "unknown", "could not classify video availability from served route"


def comments_disabled_signal(html, initial_data):
    probe = (html[:200000] + "\n" + json.dumps(initial_data or {})[:200000]).lower()
    return "comments are turned off" in probe or "comments are disabled" in probe


def detect_surface(vid):
    try:
        _, final, _ = http_get(f"https://www.youtube.com/shorts/{vid}")
        return "shorts" if "/shorts/" in final else "long_form"
    except Exception:
        return "unknown"


def fetch_youtube_watch(vid, *, comment_pages=COMMENT_PAGES):
    status, final_url, raw = http_get(f"https://www.youtube.com/watch?v={vid}")
    html = raw.decode("utf-8", "replace")
    initial_data = ytinit(html) or {}
    player = ytplayer(html) or {}
    video_state, video_state_reason = detect_video_state(
        status=status, final_url=final_url, html=html, player=player
    )
    view_count, view_count_source_path = extract_view_count(html)
    like_count, like_count_source_path = extract_like_count(html)
    capture_time = datetime.datetime.utcnow().isoformat() + "Z"
    pkt = {
        "video_id": vid,
        "surface_type": detect_surface(vid),
        "watch_url": f"https://www.youtube.com/watch?v={vid}",
        "canonical_url": first(r'<link rel="canonical" href="([^"]+)"', html),
        "channel": {"channel_id": first(r'"channelId":"([A-Za-z0-9_-]+)"', html),
                    "author": first(r'"author":"([^"]*)"', html)},
        "metadata": {
            "title": first(r'<meta property="og:title" content="([^"]*)"', html),
            "length_seconds": first(r'"lengthSeconds":"([0-9]+)"', html, int),
            "publish_date": first(r'"publishDate":"([^"]*)"', html),
            "short_description": (first(r'"shortDescription":"((?:[^"\\]|\\.)*)"', html) or "")[:500],
        },
        "engagement": {
            "view_count": view_count,
            "view_count_source_path": view_count_source_path,
            "like_count": like_count,
            "like_count_source_path": like_count_source_path,
            "like_count_text": first(r'"accessibilityText":"([0-9,.KMB]+ likes?)"', html),
            "comment_sample_count": None,
            "total_comment_count": None,
            "total_comment_count_source_path": None,
        },
        "availability": {
            "video_state": video_state,
            "video_state_reason": video_state_reason,
            "comments_state": None,
            "comments_state_reason": None,
        },
        "metric_receipts": {
            "view_count": _metric_observed(view_count, view_count_source_path, artifact="raw_watch.html")
            if view_count is not None
            else _metric_unavailable(
                "view count was not exposed in ytInitialPlayerResponse or served HTML regex fallback",
                routes_checked=[
                    "ytInitialPlayerResponse.videoDetails.viewCount",
                    "ytInitialPlayerResponse.microformat.playerMicroformatRenderer.viewCount",
                    "served_html.regex.first_viewCount",
                ],
            ),
            "like_count": _metric_observed(like_count, like_count_source_path, artifact="raw_watch.html")
            if like_count is not None
            else _metric_unavailable(
                "microformat.likeCount was not exposed; abbreviated accessibility text is preserved separately when present",
                routes_checked=["ytInitialPlayerResponse.microformat.playerMicroformatRenderer.likeCount"],
            ),
        },
        "comments_posture": None,
        "comment_count_text": None,
        "comments": [],
        "receipts": {
            "source_url": final_url,
            "http_status": status,
            "retrieval_time_utc": capture_time,
            "byte_size": len(raw),
            "raw_body_sha256": hashlib.sha256(raw).hexdigest(),
            "extraction": "served_html:ytInitialPlayerResponse + youtubei/v1/next",
            "auth": "logged_out", "js_executed": False,
        },
    }
    api_key = first(r'"INNERTUBE_API_KEY":"([^"]+)"', html)
    ver = first(r'"INNERTUBE_CONTEXT_CLIENT_VERSION":"([^"]+)"', html)
    token = comment_panel_token(initial_data)
    comment_page_bodies = []
    if not token:
        if comments_disabled_signal(html, initial_data):
            comments_state = "comments_disabled"
            comments_reason = "served watch route reports comments are turned off"
        else:
            comments_state = "comments_not_exposed"
            comments_reason = "served watch route did not expose a comments continuation token"
        pkt["comments_posture"] = comments_state
        pkt["availability"]["comments_state"] = comments_state
        pkt["availability"]["comments_state_reason"] = comments_reason
        pkt["engagement"]["comment_sample_count"] = None
        pkt["metric_receipts"]["comment_sample_count"] = _metric_unavailable(
            comments_reason,
            routes_checked=["ytInitialData.engagementPanelSectionListRenderer.continuationCommand.token"],
        )
        pkt["metric_receipts"]["total_comment_count"] = _metric_unavailable(
            comments_reason,
            routes_checked=["youtubei_next.commentsHeaderRenderer.countText"],
        )
    elif api_key and ver:
        page, got = 0, []
        while token and page < comment_pages:
            resp_status, resp_final_url, resp_raw, resp = youtubei_next_raw(api_key, ver, token)
            page_name = f"youtubei_next_page_{page + 1:02d}.json"
            comment_page_bodies.append(
                YoutubeCommentPageBody(
                    filename=page_name,
                    raw_json_bytes=resp_raw,
                    http_status=resp_status,
                    final_url=resp_final_url,
                )
            )
            hdr = collect(resp, "commentsHeaderRenderer")
            if hdr and pkt["comment_count_text"] is None:
                ct = collect(hdr[0], "countText")
                if ct:
                    count_text = _text_from_youtube_runs(ct[0]) or json.dumps(ct[0])[:120]
                    pkt["comment_count_text"] = count_text
                    exact_count = parse_exact_count_text(count_text)
                    if exact_count is not None:
                        pkt["engagement"]["total_comment_count"] = exact_count
                        pkt["engagement"]["total_comment_count_source_path"] = (
                            "youtubei_next.commentsHeaderRenderer.countText"
                        )
            for p in collect(resp, "commentEntityPayload"):
                props, auth, tb = p.get("properties", {}), p.get("author", {}), p.get("toolbar", {})
                got.append({"author": auth.get("displayName"), "author_channel_id": auth.get("channelId"),
                            "text": (props.get("content", {}) or {}).get("content", "")[:300],
                            "published_time": props.get("publishedTime"),
                            "like_count": tb.get("likeCountNotliked"), "reply_count": tb.get("replyCount")})
            page += 1
            token = next_token(resp)
        pkt["comments"] = got
        pkt["engagement"]["comment_sample_count"] = len(got)
        comments_state = "comments_sample_captured" if got else "comments_not_exposed"
        comments_reason = (
            f"captured {len(got)} sampled comments via youtubei_next"
            if got
            else "comments continuation was reachable but did not expose comment sample rows in this bounded run"
        )
        pkt["comments_posture"] = comments_state
        pkt["availability"]["comments_state"] = comments_state
        pkt["availability"]["comments_state_reason"] = comments_reason
        pkt["metric_receipts"]["comment_sample_count"] = _metric_observed(
            len(got),
            "youtubei_next.commentEntityPayload",
            artifact="youtubei_next_page_*.json",
        )
        if pkt["engagement"]["total_comment_count"] is not None:
            pkt["metric_receipts"]["total_comment_count"] = _metric_observed(
                pkt["engagement"]["total_comment_count"],
                pkt["engagement"]["total_comment_count_source_path"],
                artifact="youtubei_next_page_01.json",
            )
        else:
            pkt["metric_receipts"]["total_comment_count"] = _metric_unavailable(
                "source-native total comment count was not exposed as an exact count in commentsHeaderRenderer.countText",
                routes_checked=["youtubei_next.commentsHeaderRenderer.countText"],
            )
    else:
        comments_state = "comments_not_exposed"
        comments_reason = "comments continuation token was present but INNERTUBE_API_KEY/clientVersion was not exposed"
        pkt["comments_posture"] = comments_state
        pkt["availability"]["comments_state"] = comments_state
        pkt["availability"]["comments_state_reason"] = comments_reason
        pkt["metric_receipts"]["comment_sample_count"] = _metric_unavailable(
            comments_reason,
            routes_checked=["ytInitialData comment token", "served_html.INNERTUBE_API_KEY"],
        )
        pkt["metric_receipts"]["total_comment_count"] = _metric_unavailable(
            comments_reason,
            routes_checked=["youtubei_next.commentsHeaderRenderer.countText"],
        )
    pkt["comment_page_receipts"] = [
        {
            "filename": page.filename,
            "http_status": page.http_status,
            "final_url": page.final_url,
            "byte_size": len(page.raw_json_bytes),
            "raw_body_sha256": hashlib.sha256(page.raw_json_bytes).hexdigest(),
        }
        for page in comment_page_bodies
    ]
    return YoutubeWatchFetchResult(
        packet=pkt,
        raw_watch_html=raw,
        comment_page_bodies=tuple(comment_page_bodies),
    )


def capture(vid):
    result = fetch_youtube_watch(vid)
    pkt = result.packet
    d = os.path.join(OUT, vid)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "raw_watch.html"), "wb") as f:
        f.write(result.raw_watch_html)
    for page in result.comment_page_bodies:
        with open(os.path.join(d, page.filename), "wb") as f:
            f.write(page.raw_json_bytes)
    with open(os.path.join(d, "packet.json"), "w", encoding="utf-8") as f:
        json.dump(pkt, f, ensure_ascii=False, indent=2)
    return pkt


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"[stealth backend: {BACKEND}]")
    for vid in VIDEOS:
        try:
            p = capture(vid)
            m, e = p["metadata"], p["engagement"]
            print(f"OK  {vid:12} {p['surface_type']:9} view={e['view_count']} dur={m['length_seconds']} "
                  f"comments={p['comments_posture']}({len(p['comments'])})")
        except Exception as ex:
            print(f"ERR {vid}: {type(ex).__name__}: {ex}")
