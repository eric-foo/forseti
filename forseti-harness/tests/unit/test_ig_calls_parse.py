from __future__ import annotations

from source_capture.ig_calls_parse import (
    extract_item_permalinks,
    extract_meta_content,
    parse_ig_og_description,
    parse_ig_profile_og,
)

# Real og:description values observed via the headless logged-out probe (2026-06-14), unescaped.
POST_OG = (
    '1,693 likes, 26 comments - hyram on August 1, 2024: "When at Target, I stock up on '
    "@selflessbyhyram \U0001f609\U0001fa75 Find the entire range in-store & online!\n\n"
    "shoutout to the Target employees who watched my bafoonery and let me be lol\n\n"
    '#target #skincare #selflessbyhyram". '
)
REEL_OG = (
    '1,047 likes, 43 comments - hyram on September 11, 2024: "#ad 2 in 1 exfoliating cleanser? '
    "Sign me up! Shop the new @youthtothepeople Superfruit Cleanser @sephora now! "
    '#youthtothepeople #cleanser #skincare #YTTPpartner". '
)
PROFILE_OG = "724K Followers, 2,339 Following, 321 Posts - See Instagram photos and videos from Hyram (@hyram)"
TRUNCATED_OG = (
    '500 likes, 10 comments - someone on March 3, 2024: "This is a very long caption that IG '
    "truncated mid-way and never closed the quote…"
)


def test_extract_meta_content_both_attribute_orders_and_unescaping() -> None:
    prop_first = (
        '<meta property="og:description" content="1,693 likes - hyram: &quot;Target &amp; more&quot;. " />'
    )
    content_first = (
        '<meta content="724K Followers, 2,339 Following, 321 Posts - See" property="og:description">'
    )
    assert extract_meta_content(prop_first, "og:description") == '1,693 likes - hyram: "Target & more". '
    assert extract_meta_content(content_first, "og:description") == "724K Followers, 2,339 Following, 321 Posts - See"
    assert extract_meta_content("<html>no meta here</html>", "og:description") is None


def test_extract_item_permalinks_dedupes_and_filters_non_items() -> None:
    grid = (
        '<a href="/p/CANON/">canonical post</a>'
        '<a href="/reel/CANONREEL/">canonical reel</a>'
        '<a href="/hyram/p/C-JRfLayO96/">a</a>'
        '<a href="/hyram/reel/C_yOnGJylAQ/">b</a>'
        '<a href="/hyram/p/C-JRfLayO96/">dup</a>'
        '<a href="/otheruser/p/SHOULD_SKIP/">other handle</a>'
        '<a href="/explore/">x</a>'
        '<a href="/hyram/">profile</a>'
    )
    assert extract_item_permalinks(grid) == [
        "https://www.instagram.com/p/CANON/",
        "https://www.instagram.com/reel/CANONREEL/",
        "https://www.instagram.com/hyram/p/C-JRfLayO96/",
        "https://www.instagram.com/hyram/reel/C_yOnGJylAQ/",
        "https://www.instagram.com/otheruser/p/SHOULD_SKIP/",
    ]
    assert extract_item_permalinks(grid, profile_handle="hyram") == [
        "https://www.instagram.com/p/CANON/",
        "https://www.instagram.com/reel/CANONREEL/",
        "https://www.instagram.com/hyram/p/C-JRfLayO96/",
        "https://www.instagram.com/hyram/reel/C_yOnGJylAQ/",
    ]


def test_parse_post_og_extracts_full_call_signal_not_ad() -> None:
    parsed = parse_ig_og_description(POST_OG)
    assert parsed.likes == 1693
    assert parsed.comments == 26
    assert parsed.date == "August 1, 2024"
    assert parsed.is_ad is False
    assert parsed.truncated is False
    assert parsed.caption is not None
    assert parsed.caption.startswith("When at Target, I stock up on @selflessbyhyram")
    assert parsed.caption.endswith("#selflessbyhyram")
    assert '"' not in parsed.caption[-1:]  # closing quote stripped


def test_parse_reel_og_flags_sponsorship_ad() -> None:
    parsed = parse_ig_og_description(REEL_OG)
    assert parsed.likes == 1047
    assert parsed.comments == 43
    assert parsed.date == "September 11, 2024"
    assert parsed.is_ad is True
    assert parsed.truncated is False
    assert parsed.caption is not None
    assert parsed.caption.endswith("#YTTPpartner")


def test_parse_truncated_caption_sets_truncated_flag() -> None:
    parsed = parse_ig_og_description(TRUNCATED_OG)
    assert parsed.likes == 500
    assert parsed.truncated is True
    assert parsed.caption is not None
    assert parsed.caption.endswith("…")  # ends mid-caption, no closing quote


def test_parse_og_handles_entity_encoded_input() -> None:
    raw = '500 likes, 2 comments - x on May 5, 2024: &quot;hi &amp; bye&quot;. '
    parsed = parse_ig_og_description(raw)
    assert parsed.caption == "hi & bye"
    assert parsed.likes == 500


def test_ad_word_boundary_does_not_false_match() -> None:
    raw = '1 likes, 0 comments - x on May 5, 2024: "my #address is hidden". '
    assert parse_ig_og_description(raw).is_ad is False


def test_parse_profile_og_extracts_stats() -> None:
    parsed = parse_ig_profile_og(PROFILE_OG)
    assert parsed is not None
    assert parsed.followers == "724K"
    assert parsed.following == "2,339"
    assert parsed.posts == "321"


def test_profile_parser_returns_none_on_post_og_and_vice_versa() -> None:
    assert parse_ig_profile_og(POST_OG) is None
    post_on_profile = parse_ig_og_description(PROFILE_OG)
    assert post_on_profile.caption is None
    assert post_on_profile.likes is None
    assert post_on_profile.is_ad is False
