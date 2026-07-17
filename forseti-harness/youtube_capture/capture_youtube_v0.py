#!/usr/bin/env python3
"""Bounded YouTube public-metadata capture (tracked code; captured data gitignored).

Proven route (see source_families/social_media/youtube/youtube_capture_recon_v0.md):
  - metadata: embedded `ytInitialPlayerResponse` in served HTML (logged-out, no JS)
  - comments: `youtubei/v1/next` panel-scoped continuation (same route long-form + Shorts)

Persists one selected-observable packet per video to ./packets/<video_id>/. The
served watch/comment response bodies are acquisition-time inputs only and are not
written by this module. Public read-only; no auth; no scheduler.
Tracked at forseti-harness/youtube_capture/. Helpers here are reused by shorts_scroll_capture_v0.py.
"""
import re, json, os, datetime, urllib.request
from dataclasses import dataclass, field

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packets")
COMMENT_PAGES = 1  # bounded top/default-order comment page
VIDEOS = ["dQw4w9WgXcQ", "-0FVExAgmps", "84id2dzpwU0", "__fmDj0ZJ1Q"]  # longform, short, comments-off, recent


try:
    from .stealth_client import http_get, BACKEND  # type: ignore[import-not-found]
except ImportError:  # script-mode compatibility
    from stealth_client import http_get, BACKEND  # Chrome-impersonating client (curl_cffi) + urllib fallback

try:
    from harness_utils import int_or_none as _integer
except ImportError:  # script-mode compatibility: harness root not on sys.path
    import sys as _sys
    _sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from harness_utils import int_or_none as _integer


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


COMMENTS_PANEL_BADGE_SOURCE_PATH = (
    "ytInitialData.engagementPanels.engagementPanelTitleHeaderRenderer.contextualInfo"
)


def extract_comments_panel_count(initial_data):
    """Total comment count from the Comments engagement-panel badge in the served
    watch HTML. Returns ``(exact_count_or_none, badge_text_or_none)``; a rounded
    K/M badge yields ``(None, text)`` so callers stay fail-closed on non-exact text.
    YouTube renders this badge as an exact integer below 1,000 and rounds above."""
    for hdr in collect(initial_data or {}, "engagementPanelTitleHeaderRenderer"):
        if not isinstance(hdr, dict):
            continue
        if _text_from_youtube_runs(hdr.get("title")) != "Comments":
            continue
        badge = _text_from_youtube_runs(hdr.get("contextualInfo"))
        if badge is None:
            continue
        return parse_exact_count_text(badge), badge
    return None, None


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
    if play_status and play_status != "OK":
        return (
            "unknown",
            f"ytInitialPlayerResponse.playabilityStatus.status={play_status} blocks playback; "
            "no specific availability classification matched",
        )
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


def _comment_thread_metadata(response):
    """Return source-visible thread display facts keyed by comment id."""
    metadata = {}
    for thread in collect(response, "commentThreadRenderer"):
        if not isinstance(thread, dict):
            continue
        outer = thread.get("commentViewModel") or {}
        view = outer.get("commentViewModel") if isinstance(outer, dict) else {}
        if not isinstance(view, dict):
            continue
        comment_id = view.get("commentId")
        if not isinstance(comment_id, str) or not comment_id:
            continue
        pinned_text = view.get("pinnedText")
        rendering_priority = thread.get("renderingPriority")
        metadata[comment_id] = {
            "pinned_text": pinned_text if isinstance(pinned_text, str) else None,
            "rendering_priority": (
                rendering_priority if isinstance(rendering_priority, str) else None
            ),
        }
    return metadata


def _comment_heart_states(response):
    """Return source-native creator-heart states keyed by toolbar-state key."""
    states = {}
    for state in collect(response, "engagementToolbarStateEntityPayload"):
        if not isinstance(state, dict):
            continue
        key = state.get("key")
        heart_state = state.get("heartState")
        if isinstance(key, str) and key and isinstance(heart_state, str):
            states[key] = heart_state
    return states


def _content_attachment_labels(content):
    """Preserve compact public labels for emoji/sticker-style comment attachments."""
    if not isinstance(content, dict):
        return []
    labels = []
    for run in content.get("attachmentRuns") or []:
        if not isinstance(run, dict):
            continue
        element = run.get("element")
        properties = element.get("properties") if isinstance(element, dict) else None
        accessibility = (
            properties.get("accessibilityProperties") if isinstance(properties, dict) else None
        )
        label = accessibility.get("label") if isinstance(accessibility, dict) else None
        if isinstance(label, str) and label:
            labels.append(label)
    return labels


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
    panel_comment_count, panel_comment_count_text = extract_comments_panel_count(initial_data)
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
            "total_comment_count": panel_comment_count,
            "total_comment_count_source_path": (
                COMMENTS_PANEL_BADGE_SOURCE_PATH if panel_comment_count is not None else None
            ),
        },
        "availability": {
            "video_state": video_state,
            "video_state_reason": video_state_reason,
            "comments_state": None,
            "comments_state_reason": None,
        },
        "metric_receipts": {
            "view_count": _metric_observed(
                view_count, view_count_source_path, artifact="youtube_watch_capture.json"
            )
            if view_count is not None
            else _metric_unavailable(
                "view count was not exposed in ytInitialPlayerResponse or served HTML regex fallback",
                routes_checked=[
                    "ytInitialPlayerResponse.videoDetails.viewCount",
                    "ytInitialPlayerResponse.microformat.playerMicroformatRenderer.viewCount",
                    "served_html.regex.first_viewCount",
                ],
            ),
            "like_count": _metric_observed(
                like_count, like_count_source_path, artifact="youtube_watch_capture.json"
            )
            if like_count is not None
            else _metric_unavailable(
                "microformat.likeCount was not exposed; abbreviated accessibility text is preserved separately when present",
                routes_checked=["ytInitialPlayerResponse.microformat.playerMicroformatRenderer.likeCount"],
            ),
        },
        "comments_posture": None,
        "comment_count_text": None,
        "comments_panel_count_text": panel_comment_count_text,
        "comments": [],
        "receipts": {
            "source_url": final_url,
            "http_status": status,
            "retrieval_time_utc": capture_time,
            "source_response_byte_size": len(raw),
            "extraction": (
                "selected source-visible fields from served_html:ytInitialPlayerResponse "
                "+ youtubei/v1/next; enclosing response bodies are not persistence inputs"
            ),
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
    elif api_key and ver:
        page, got = 0, []
        page_receipts = []
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
                    if exact_count is not None and pkt["engagement"]["total_comment_count"] is None:
                        pkt["engagement"]["total_comment_count"] = exact_count
                        pkt["engagement"]["total_comment_count_source_path"] = (
                            "youtubei_next.commentsHeaderRenderer.countText"
                        )
            thread_metadata = _comment_thread_metadata(resp)
            heart_states = _comment_heart_states(resp)
            page_rows = []
            for source_order_in_page, p in enumerate(collect(resp, "commentEntityPayload"), start=1):
                props, auth, tb = p.get("properties", {}), p.get("author", {}), p.get("toolbar", {})
                content = props.get("content", {}) or {}
                comment_id = props.get("commentId")
                thread = thread_metadata.get(comment_id, {})
                heart_state = heart_states.get(props.get("toolbarStateKey"))
                row = {
                    "comment_id": comment_id,
                    "author": auth.get("displayName"),
                    "author_channel_id": auth.get("channelId"),
                    "author_is_creator": auth.get("isCreator"),
                    "author_is_verified": auth.get("isVerified"),
                    "text": content.get("content", ""),
                    "content_attachment_labels": _content_attachment_labels(content),
                    "published_time": props.get("publishedTime"),
                    "reply_level": props.get("replyLevel"),
                    "like_count": tb.get("likeCountNotliked"),
                    "reply_count": tb.get("replyCount"),
                    "pinned_text": thread.get("pinned_text"),
                    "rendering_priority": thread.get("rendering_priority"),
                    "heart_state": heart_state,
                    "source_page_number": page + 1,
                    "source_order_in_page": source_order_in_page,
                    "source_order_global": len(got) + len(page_rows) + 1,
                }
                page_rows.append(row)
            got.extend(page_rows)
            page_receipts.append(
                {
                    "page_number": page + 1,
                    "http_status": resp_status,
                    "final_url": resp_final_url,
                    "source_response_byte_size": len(resp_raw),
                    "selected_comment_count": len(page_rows),
                }
            )
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
            artifact="youtube_watch_capture.json",
        )
        pkt["comment_page_receipts"] = page_receipts
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
    total_comment_routes = [COMMENTS_PANEL_BADGE_SOURCE_PATH]
    if comment_page_bodies:
        total_comment_routes.append("youtubei_next.commentsHeaderRenderer.countText")
    if pkt["engagement"]["total_comment_count"] is not None:
        total_source_path = pkt["engagement"]["total_comment_count_source_path"]
        pkt["metric_receipts"]["total_comment_count"] = _metric_observed(
            pkt["engagement"]["total_comment_count"],
            total_source_path,
            artifact="youtube_watch_capture.json",
        )
    elif panel_comment_count_text is not None:
        pkt["metric_receipts"]["total_comment_count"] = _metric_unavailable(
            f"Comments panel badge text {panel_comment_count_text!r} is not an exact integer "
            "count (rounded or non-numeric); exact totals are never derived from rounded text",
            routes_checked=total_comment_routes,
        )
    elif comment_page_bodies:
        pkt["metric_receipts"]["total_comment_count"] = _metric_unavailable(
            "source-native total comment count was not exposed as an exact count in the "
            "Comments panel badge or commentsHeaderRenderer.countText",
            routes_checked=total_comment_routes,
        )
    else:
        pkt["metric_receipts"]["total_comment_count"] = _metric_unavailable(
            f"{comments_reason}; the Comments panel badge in served HTML also did not expose a count",
            routes_checked=total_comment_routes,
        )
    pkt.setdefault("comment_page_receipts", [])
    pkt["comment_capture_coverage"] = {
        "requested_page_limit": comment_pages,
        "pages_fetched": len(comment_page_bodies),
        "selected_comment_count": len(pkt["comments"]),
        "continuation_remaining_after_stop": bool(token),
        "ordering_posture": "source_default_order_as_served",
    }
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
