"""Pure parser for YouTube public channel RSS/Atom feeds.

Network-free by contract (mirroring the ``ig_reels_grid`` parser/capture
split): callers own acquisition; this module only turns served feed XML into
typed per-entry records for the tier-1 daily monitor. Honesty rules: an absent
or unparseable field is ``None`` plus a limitation note -- never zero-filled,
never inferred. The feed's ``media:starRating count`` is surfaced under its own
name; interpreting it as a like count (and that interpretation's provenance)
belongs to the caller.

Observed surface quirk (2026-07-02 probe, N=4 roster feeds): the feed-level
``yt:channelId`` is served WITHOUT the ``UC`` prefix while entry-level
``yt:channelId`` carries the full id. Both are preserved as served.
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import TypeAlias

ATOM_NS = "{http://www.w3.org/2005/Atom}"
YT_NS = "{http://www.youtube.com/xml/schemas/2015}"
MEDIA_NS = "{http://search.yahoo.com/mrss/}"

FAILURE_KIND_INVALID_XML = "invalid_xml"
FAILURE_KIND_NOT_AN_ATOM_FEED = "not_an_atom_feed"


@dataclass(frozen=True)
class YoutubeChannelFeedEntry:
    video_id: str
    title: str | None
    published: str | None
    updated: str | None
    view_count: int | None
    star_rating_count: int | None


@dataclass(frozen=True)
class YoutubeChannelFeedParse:
    feed_channel_id_as_served: str | None
    feed_title: str | None
    entry_channel_ids: tuple[str, ...]
    entries: tuple[YoutubeChannelFeedEntry, ...]
    limitation_notes: tuple[str, ...]


@dataclass(frozen=True)
class YoutubeChannelFeedParseFailure:
    failure_kind: str
    message: str


YoutubeChannelFeedParseResult: TypeAlias = YoutubeChannelFeedParse | YoutubeChannelFeedParseFailure


def parse_youtube_channel_feed(xml_text: str) -> YoutubeChannelFeedParseResult:
    """Parse one served channel feed document into typed entries."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        return YoutubeChannelFeedParseFailure(
            failure_kind=FAILURE_KIND_INVALID_XML, message=str(exc)
        )
    if root.tag != f"{ATOM_NS}feed":
        return YoutubeChannelFeedParseFailure(
            failure_kind=FAILURE_KIND_NOT_AN_ATOM_FEED,
            message=f"document root is {root.tag!r}, not an Atom feed",
        )

    notes: list[str] = []
    entries: list[YoutubeChannelFeedEntry] = []
    entry_channel_ids: list[str] = []
    for index, entry in enumerate(root.findall(f"{ATOM_NS}entry")):
        video_id = _element_text(entry, f"{YT_NS}videoId")
        if video_id is None:
            notes.append(f"entry[{index}] missing yt:videoId; entry skipped")
            continue
        entry_channel_id = _element_text(entry, f"{YT_NS}channelId")
        if entry_channel_id is not None and entry_channel_id not in entry_channel_ids:
            entry_channel_ids.append(entry_channel_id)

        view_count: int | None = None
        star_rating_count: int | None = None
        community = entry.find(f"{MEDIA_NS}group/{MEDIA_NS}community")
        if community is None:
            notes.append(
                f"entry[{index}] ({video_id}) missing media:community; "
                "views and starRating unavailable"
            )
        else:
            statistics = community.find(f"{MEDIA_NS}statistics")
            if statistics is None:
                notes.append(f"entry[{index}] ({video_id}) missing media:statistics")
            else:
                view_count = _strict_int(statistics.get("views"))
                if view_count is None:
                    notes.append(
                        f"entry[{index}] ({video_id}) media:statistics views not a "
                        f"plain integer: {statistics.get('views')!r}"
                    )
            star_rating = community.find(f"{MEDIA_NS}starRating")
            if star_rating is None:
                notes.append(f"entry[{index}] ({video_id}) missing media:starRating")
            else:
                star_rating_count = _strict_int(star_rating.get("count"))
                if star_rating_count is None:
                    notes.append(
                        f"entry[{index}] ({video_id}) media:starRating count not a "
                        f"plain integer: {star_rating.get('count')!r}"
                    )

        entries.append(
            YoutubeChannelFeedEntry(
                video_id=video_id,
                title=_element_text(entry, f"{ATOM_NS}title")
                or _element_text(entry, f"{MEDIA_NS}group/{MEDIA_NS}title"),
                published=_element_text(entry, f"{ATOM_NS}published"),
                updated=_element_text(entry, f"{ATOM_NS}updated"),
                view_count=view_count,
                star_rating_count=star_rating_count,
            )
        )

    return YoutubeChannelFeedParse(
        feed_channel_id_as_served=_element_text(root, f"{YT_NS}channelId"),
        feed_title=_element_text(root, f"{ATOM_NS}title"),
        entry_channel_ids=tuple(entry_channel_ids),
        entries=tuple(entries),
        limitation_notes=tuple(notes),
    )


def _element_text(parent: ET.Element, path: str) -> str | None:
    element = parent.find(path)
    if element is None or element.text is None:
        return None
    stripped = element.text.strip()
    return stripped or None


def _strict_int(value: str | None) -> int | None:
    if value is None:
        return None
    stripped = value.strip()
    return int(stripped) if stripped.isdigit() else None


__all__ = [
    "FAILURE_KIND_INVALID_XML",
    "FAILURE_KIND_NOT_AN_ATOM_FEED",
    "YoutubeChannelFeedEntry",
    "YoutubeChannelFeedParse",
    "YoutubeChannelFeedParseFailure",
    "YoutubeChannelFeedParseResult",
    "parse_youtube_channel_feed",
]
