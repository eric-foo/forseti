"""Unit tests for the YouTube channel RSS/Atom feed parser.

Fixtures mirror the real served nesting observed on the 2026-07-02 probe
(entry-level ``yt:videoId``/``yt:channelId``, ``media:group/media:community``
with ``media:starRating`` and ``media:statistics``). The honesty paths are the
point: absent or unparseable fields must come back ``None`` with a limitation
note -- never zero -- and a non-feed body must be a typed failure, not an
exception or fake entries.
"""
from __future__ import annotations

from source_capture.youtube_channel_rss import (
    FAILURE_KIND_INVALID_XML,
    FAILURE_KIND_NOT_AN_ATOM_FEED,
    YoutubeChannelFeedParse,
    YoutubeChannelFeedParseFailure,
    parse_youtube_channel_feed,
)


def _entry_xml(
    *,
    video_id: str | None = "vidAlpha0001",
    channel_id: str = "UCalphaAlphaAlphaAlpha01",
    title: str = "Alpha Video",
    published: str | None = "2026-07-02T09:00:05+00:00",
    updated: str = "2026-07-02T16:06:10+00:00",
    views: str | None = "1718",
    stars: str | None = "42",
    include_community: bool = True,
) -> str:
    video_id_xml = f"<yt:videoId>{video_id}</yt:videoId>" if video_id is not None else ""
    published_xml = f"<published>{published}</published>" if published is not None else ""
    statistics_xml = f'<media:statistics views="{views}"/>' if views is not None else ""
    star_xml = (
        f'<media:starRating count="{stars}" average="5.00" min="1" max="5"/>'
        if stars is not None
        else ""
    )
    community_xml = (
        f"<media:community>{star_xml}{statistics_xml}</media:community>"
        if include_community
        else ""
    )
    return (
        "<entry>"
        f"<id>yt:video:{video_id or 'missing'}</id>"
        f"{video_id_xml}"
        f"<yt:channelId>{channel_id}</yt:channelId>"
        f"<title>{title}</title>"
        f"{published_xml}"
        f"<updated>{updated}</updated>"
        f"<media:group><media:title>{title}</media:title>{community_xml}</media:group>"
        "</entry>"
    )


def _feed_xml(entries: str = "", *, feed_channel_id: str = "alphaAlphaAlphaAlpha01") -> str:
    # The real surface serves the feed-level yt:channelId WITHOUT the UC prefix.
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" '
        'xmlns:media="http://search.yahoo.com/mrss/" '
        'xmlns="http://www.w3.org/2005/Atom">'
        f"<yt:channelId>{feed_channel_id}</yt:channelId>"
        "<title>Alpha Channel</title>"
        f"{entries}"
        "</feed>"
    )


def test_parses_entries_with_exact_fields() -> None:
    xml = _feed_xml(
        _entry_xml()
        + _entry_xml(video_id="vidBeta00002", title="Beta Video", views="906213", stars="0")
    )
    parsed = parse_youtube_channel_feed(xml)
    assert isinstance(parsed, YoutubeChannelFeedParse)
    assert parsed.feed_channel_id_as_served == "alphaAlphaAlphaAlpha01"
    assert parsed.feed_title == "Alpha Channel"
    assert parsed.entry_channel_ids == ("UCalphaAlphaAlphaAlpha01",)
    assert len(parsed.entries) == 2
    first, second = parsed.entries
    assert first.video_id == "vidAlpha0001"
    assert first.title == "Alpha Video"
    assert first.published == "2026-07-02T09:00:05+00:00"
    assert first.updated == "2026-07-02T16:06:10+00:00"
    assert first.view_count == 1718
    assert first.star_rating_count == 42
    # A served zero is an honest observed zero, distinct from absence.
    assert second.view_count == 906213
    assert second.star_rating_count == 0
    assert parsed.limitation_notes == ()


def test_missing_community_yields_none_with_note() -> None:
    parsed = parse_youtube_channel_feed(_feed_xml(_entry_xml(include_community=False)))
    assert isinstance(parsed, YoutubeChannelFeedParse)
    (entry,) = parsed.entries
    assert entry.view_count is None
    assert entry.star_rating_count is None
    assert any("missing media:community" in note for note in parsed.limitation_notes)


def test_non_integer_views_yields_none_with_note() -> None:
    parsed = parse_youtube_channel_feed(_feed_xml(_entry_xml(views="1.2K")))
    assert isinstance(parsed, YoutubeChannelFeedParse)
    (entry,) = parsed.entries
    assert entry.view_count is None
    assert entry.star_rating_count == 42
    assert any("views not a plain integer" in note for note in parsed.limitation_notes)


def test_missing_published_is_none_not_invented() -> None:
    parsed = parse_youtube_channel_feed(_feed_xml(_entry_xml(published=None)))
    assert isinstance(parsed, YoutubeChannelFeedParse)
    (entry,) = parsed.entries
    assert entry.published is None


def test_missing_video_id_skips_entry_with_note() -> None:
    parsed = parse_youtube_channel_feed(
        _feed_xml(_entry_xml(video_id=None) + _entry_xml(video_id="vidKept00001"))
    )
    assert isinstance(parsed, YoutubeChannelFeedParse)
    assert [entry.video_id for entry in parsed.entries] == ["vidKept00001"]
    assert any("missing yt:videoId" in note for note in parsed.limitation_notes)


def test_empty_feed_parses_with_no_entries() -> None:
    parsed = parse_youtube_channel_feed(_feed_xml())
    assert isinstance(parsed, YoutubeChannelFeedParse)
    assert parsed.entries == ()


def test_invalid_xml_is_typed_failure() -> None:
    result = parse_youtube_channel_feed("<html><body>rate limited")
    assert isinstance(result, YoutubeChannelFeedParseFailure)
    assert result.failure_kind == FAILURE_KIND_INVALID_XML


def test_non_feed_document_is_typed_failure() -> None:
    result = parse_youtube_channel_feed("<html><body>consent wall</body></html>")
    assert isinstance(result, YoutubeChannelFeedParseFailure)
    assert result.failure_kind == FAILURE_KIND_NOT_AN_ATOM_FEED
