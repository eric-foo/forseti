#!/usr/bin/env python3
"""Shorts-scroll VOLUME capture (tracked code; captured data gitignored).

Captures Shorts end-to-end (metadata + a comments page) at ~CADENCE s each for ~DURATION s.
Doubles as a load/stress test of the raw route at realistic volume: stops on the FIRST wall and
records where it broke (the route-health signal at volume — no separate canary needed).

Lean packets (fields + comment sample + receipts incl. raw-body sha256; raw HTML NOT persisted).
Public read-only, logged-out. Tracked at orca-harness/youtube_capture/. Env overrides: SHORTS_DURATION, SHORTS_CADENCE.
"""
import re, json, os, time, random, hashlib, datetime, urllib.error
from collections import Counter
from capture_youtube_v0 import http_get, ytinit, comment_panel_token, collect, youtubei_next, first, extract_view_count

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "shorts_scroll_runs")
CHANNELS = ["MrBeast", "khaby00", "NBA", "NFL", "ZachKing", "WWE", "brentrivera", "DudePerfect"]
CADENCE = int(os.environ.get("SHORTS_CADENCE", "10"))     # seconds per short
DURATION = int(os.environ.get("SHORTS_DURATION", "1800"))  # 30 min


def enumerate_shorts(handles):
    pool = []
    for h in handles:
        try:
            _, _, raw = http_get(f"https://www.youtube.com/@{h}/shorts")
            ids = re.findall(r"/shorts/([A-Za-z0-9_-]{11})", raw.decode("utf-8", "replace"))
            pool += ids
            print(f"enum @{h}: {len(set(ids))} shorts", flush=True)
        except Exception as e:
            print(f"enum @{h}: {type(e).__name__}", flush=True)
    pool = list(dict.fromkeys(pool))
    random.shuffle(pool)
    return pool


def capture_short(vid):
    status, final_url, raw = http_get(f"https://www.youtube.com/watch?v={vid}")
    html = raw.decode("utf-8", "replace")
    wall = (status != 200) or ("consent.youtube.com" in final_url) or ("Sign in to confirm you" in html)
    view_count, view_count_source_path = extract_view_count(html)
    pkt = {"video_id": vid, "surface_type": "shorts", "http_status": status,
           "channel_id": first(r'"channelId":"([A-Za-z0-9_-]+)"', html),
           "author": first(r'"author":"([^"]*)"', html),
           "title": first(r'<meta property="og:title" content="([^"]*)"', html),
           "view_count": view_count,
           "view_count_source_path": view_count_source_path,
           "length_seconds": first(r'"lengthSeconds":"([0-9]+)"', html, int),
           "publish_date": first(r'"publishDate":"([^"]*)"', html),
           "retrieval_time_utc": datetime.datetime.utcnow().isoformat() + "Z",
           "raw_body_sha256": hashlib.sha256(raw).hexdigest(), "byte_size": len(raw),
           "comments_posture": None, "comments": []}
    if not wall:
        key = first(r'"INNERTUBE_API_KEY":"([^"]+)"', html)
        ver = first(r'"INNERTUBE_CONTEXT_CLIENT_VERSION":"([^"]+)"', html)
        token = comment_panel_token(ytinit(html) or {})
        if not token:
            pkt["comments_posture"] = "disabled"
        elif key and ver:
            got = []
            for p in collect(youtubei_next(key, ver, token), "commentEntityPayload"):
                props, auth, tb = p.get("properties", {}), p.get("author", {}), p.get("toolbar", {})
                got.append({"author": auth.get("displayName"),
                            "text": (props.get("content", {}) or {}).get("content", "")[:200],
                            "published_time": props.get("publishedTime"), "like_count": tb.get("likeCountNotliked")})
            pkt["comments"] = got
            pkt["comments_posture"] = "captured" if got else "empty"
    return pkt, wall


def main():
    os.makedirs(OUT, exist_ok=True)
    start_iso = datetime.datetime.utcnow().isoformat() + "Z"
    pool = enumerate_shorts(CHANNELS)
    print(f"POOL shorts={len(pool)} cadence={CADENCE}s duration={DURATION}s", flush=True)
    start = time.time()
    rows, wall_hit = [], None
    for idx, vid in enumerate(pool):
        if time.time() - start > DURATION:
            break
        t0 = time.time()
        try:
            pkt, wall = capture_short(vid)
            json.dump(pkt, open(os.path.join(OUT, vid + ".json"), "w", encoding="utf-8"), ensure_ascii=False)
            rows.append({"i": idx, "vid": vid, "status": pkt["http_status"],
                         "posture": pkt["comments_posture"], "comments": len(pkt["comments"]),
                         "view": pkt["view_count"], "wall": wall})
            if wall:
                wall_hit = {"at": idx, "vid": vid, "reason": f"wall_marker/status={pkt['http_status']}"}
                print(f"WALL at idx={idx} vid={vid} status={pkt['http_status']}", flush=True)
                break
        except urllib.error.HTTPError as he:
            wall_hit = {"at": idx, "vid": vid, "reason": f"HTTPError {he.code}"}
            rows.append({"i": idx, "vid": vid, "error": f"HTTP {he.code}", "wall": True})
            print(f"WALL(HTTP {he.code}) at idx={idx} vid={vid}", flush=True)
            break
        except Exception as e:
            rows.append({"i": idx, "vid": vid, "error": f"{type(e).__name__}: {e}"})
        if idx % 25 == 0:
            print(f"  ...{idx} done, {round(time.time()-start)}s elapsed", flush=True)
        dt = time.time() - t0
        if dt < CADENCE and (time.time() - start) < DURATION:
            time.sleep(CADENCE - dt)
    postures = Counter(r.get("posture") for r in rows if "posture" in r)
    errors = sum(1 for r in rows if "error" in r)
    summ = {"start_utc": start_iso, "elapsed_s": round(time.time() - start), "attempted": len(rows),
            "pool_size": len(pool), "cadence_s": CADENCE, "wall_hit": wall_hit,
            "posture_counts": dict(postures), "errors": errors,
            "captured_with_comments": postures.get("captured", 0),
            "approx_requests": len(rows) * 2 + len(CHANNELS)}
    path = os.path.join(OUT, "_summary_" + start_iso.replace(":", "-") + ".json")
    json.dump({**summ, "rows": rows}, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"SHORTS_SCROLL_DONE attempted={summ['attempted']} elapsed={summ['elapsed_s']}s "
          f"postures={dict(postures)} errors={errors} wall={wall_hit} approx_req={summ['approx_requests']} "
          f"summary={os.path.basename(path)}", flush=True)


if __name__ == "__main__":
    main()
