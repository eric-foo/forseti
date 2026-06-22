#!/usr/bin/env python3
"""Enrich captured YouTube packets with Return-YouTube-Dislike ESTIMATE dislikes.

Adds a clearly-labeled `dislikes_estimate` block to each packet (NOT YouTube ground truth).
Per integrity guidance: carry rawLikes/rawDislikes, retrieval time, and video era; treat the
estimate as low-weight, never a hard authenticity threshold. Tracked code; captured data gitignored.
"""
import os, json, datetime, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packets")
CUTOFF = "2021-11-10"  # YouTube public-dislike hiding began


def ryd(vid):
    req = urllib.request.Request(f"https://returnyoutubedislikeapi.com/votes?videoId={vid}", headers={"User-Agent": UA})
    return json.loads(urllib.request.urlopen(req, timeout=20).read())


def era(publish_date):
    if not publish_date:
        return "unknown"
    return "pre_cutoff_archived (~±1-2%)" if publish_date[:10] < CUTOFF else "post_cutoff_extrapolated (~±15-25%; <24h unreliable)"


for vid in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, vid, "packet.json")
    pkt = json.load(open(p, encoding="utf-8"))
    try:
        v = ryd(vid)
        pkt["dislikes_estimate"] = {
            "source": "return_youtube_dislike (THIRD-PARTY ESTIMATE — not YouTube ground truth)",
            "is_ground_truth": False,
            "estimated_dislikes": v.get("dislikes"),
            "ryd_likes": v.get("likes"),
            "raw_dislikes_sample": v.get("rawDislikes"),
            "raw_likes_sample": v.get("rawLikes"),
            "rating": v.get("rating"),
            "view_count_ryd": v.get("viewCount"),
            "video_era": era(pkt.get("metadata", {}).get("publish_date")),
            "retrieval_time_utc": datetime.datetime.utcnow().isoformat() + "Z",
            "use_note": "low-weight labeled estimate; never a hard bot/authenticity threshold",
        }
        json.dump(pkt, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        de = pkt["dislikes_estimate"]
        print(f"{vid:12} est_dislikes={de['estimated_dislikes']} raw(l/d)={de['raw_likes_sample']}/{de['raw_dislikes_sample']} "
              f"rating={de['rating']} era={de['video_era']}")
    except Exception as ex:
        print(f"{vid:12} RYD_ERR {type(ex).__name__}: {ex}")
