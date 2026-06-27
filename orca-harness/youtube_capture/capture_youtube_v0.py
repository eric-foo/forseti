#!/usr/bin/env python3
"""Bounded YouTube public-metadata capture v0 (tracked code; captured data gitignored).

Proven route (see source_families/social_media/youtube/youtube_capture_recon_v0.md):
  - metadata: embedded `ytInitialPlayerResponse` in served HTML (logged-out, no JS)
  - comments: `youtubei/v1/next` panel-scoped continuation (same route long-form + Shorts)

Persists one packet per video to ./packets/<video_id>/. Public read-only; no auth; no scheduler.
Tracked at orca-harness/youtube_capture/. Helpers here are reused by shorts_scroll_capture_v0.py.
"""
import re, json, os, hashlib, datetime, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packets")
COMMENT_PAGES = 2  # bounded
VIDEOS = ["dQw4w9WgXcQ", "-0FVExAgmps", "84id2dzpwU0", "__fmDj0ZJ1Q"]  # longform, short, comments-off, recent


from stealth_client import http_get, BACKEND  # Chrome-impersonating client (curl_cffi) + urllib fallback


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


def youtubei_next(api_key, ver, token):
    body = json.dumps({"context": {"client": {"clientName": "WEB", "clientVersion": ver, "hl": "en", "gl": "US"}},
                       "continuation": token}).encode()
    _, _, raw = http_get(f"https://www.youtube.com/youtubei/v1/next?key={api_key}&prettyPrint=false", data=body)
    return json.loads(raw)


def first(pattern, text, cast=str):
    m = re.search(pattern, text)
    return cast(m.group(1)) if m else None


def _integer(value):
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
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


def extract_view_count(html):
    count, source_path = player_view_count(ytplayer(html))
    if count is not None:
        return count, source_path
    count = first(r'"viewCount":"([0-9]+)"', html, int)
    return count, "served_html.regex.first_viewCount" if count is not None else None


def detect_surface(vid):
    try:
        _, final, _ = http_get(f"https://www.youtube.com/shorts/{vid}")
        return "shorts" if "/shorts/" in final else "long_form"
    except Exception:
        return "unknown"


def capture(vid):
    status, final_url, raw = http_get(f"https://www.youtube.com/watch?v={vid}")
    html = raw.decode("utf-8", "replace")
    view_count, view_count_source_path = extract_view_count(html)
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
            "like_count_text": first(r'"accessibilityText":"([0-9,.KMB]+ likes?)"', html),
        },
        "comments_posture": None,
        "comment_count_text": None,
        "comments": [],
        "receipts": {
            "source_url": final_url,
            "http_status": status,
            "retrieval_time_utc": datetime.datetime.utcnow().isoformat() + "Z",
            "byte_size": len(raw),
            "raw_body_sha256": hashlib.sha256(raw).hexdigest(),
            "extraction": "served_html:ytInitialPlayerResponse + youtubei/v1/next",
            "auth": "logged_out", "js_executed": False,
        },
    }
    api_key = first(r'"INNERTUBE_API_KEY":"([^"]+)"', html)
    ver = first(r'"INNERTUBE_CONTEXT_CLIENT_VERSION":"([^"]+)"', html)
    token = comment_panel_token(ytinit(html) or {})
    if not token:
        pkt["comments_posture"] = "disabled"
    elif api_key and ver:
        page, got = 0, []
        while token and page < COMMENT_PAGES:
            resp = youtubei_next(api_key, ver, token)
            hdr = collect(resp, "commentsHeaderRenderer")
            if hdr and pkt["comment_count_text"] is None:
                ct = collect(hdr[0], "countText")
                if ct:
                    pkt["comment_count_text"] = json.dumps(ct[0])[:120]
            for p in collect(resp, "commentEntityPayload"):
                props, auth, tb = p.get("properties", {}), p.get("author", {}), p.get("toolbar", {})
                got.append({"author": auth.get("displayName"), "author_channel_id": auth.get("channelId"),
                            "text": (props.get("content", {}) or {}).get("content", "")[:300],
                            "published_time": props.get("publishedTime"),
                            "like_count": tb.get("likeCountNotliked"), "reply_count": tb.get("replyCount")})
            page += 1
            token = next_token(resp)
        pkt["comments"] = got
        pkt["comments_posture"] = "captured" if got else "empty"
    d = os.path.join(OUT, vid)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "raw_watch.html"), "wb") as f:
        f.write(raw)
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
