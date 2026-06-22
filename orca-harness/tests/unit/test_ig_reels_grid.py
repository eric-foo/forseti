from __future__ import annotations

from source_capture.ig_reels_grid import (
    AMBIGUOUS_HIDDEN_NUMERIC,
    CLIPS_USER_JSON_METADATA,
    PARSED_NO_HOVER_GRID_ENGAGEMENT,
    STATIC_POST_VIEW_COUNT_NOT_APPLICABLE,
    MEDIA_KIND_REEL,
    WEB_PROFILE_INFO_JSON_METADATA,
    iter_json_media_candidates,
    join_dom_rows_with_json_candidates,
    normalize_dom_grid_rows,
    source_surface_from_url_or_path,
)


def test_normalize_dom_grid_rows_preserves_no_hover_hidden_engagement() -> None:
    rows = normalize_dom_grid_rows(
        [
            {
                "path": "/jeremyfragrance/reel/DZ4Stb5MVPB/",
                "visibleText": "2,984",
                "visibleNumericTexts": ["2,984"],
                "leafNumericTexts": [
                    {"text": "30"},
                    {"text": "4"},
                    {"text": "2,984"},
                ],
                "rect": {"x": 492, "y": 499, "width": 233, "height": 362},
            }
        ],
        final_url="https://www.instagram.com/jeremyfragrance/reels/",
        profile_handle="jeremyfragrance",
    )

    assert len(rows) == 1
    row = rows[0]
    assert row.shortcode == "DZ4Stb5MVPB"
    assert row.kind == "reel"
    assert row.views_text == "2,984"
    assert row.likes_text == "30"
    assert row.comments_text == "4"
    assert row.hidden_leaf_numeric_texts == ("30", "4", "2,984")
    assert row.hidden_engagement_candidates == ("30", "4")
    assert row.parse_status == PARSED_NO_HOVER_GRID_ENGAGEMENT




def test_static_profile_post_never_promotes_visible_number_to_view_count() -> None:
    rows = normalize_dom_grid_rows(
        [
            {
                "path": "/liv_cos/p/STATIC123/",
                "visibleNumericTexts": ["4,264"],
                "leafNumericTexts": [{"text": "4,264"}, {"text": "48"}],
            }
        ],
        final_url="https://www.instagram.com/liv_cos/",
        profile_handle="liv_cos",
    )

    assert len(rows) == 1
    row = rows[0]
    assert row.kind == "post"
    assert row.shortcode == "STATIC123"
    assert row.views_text is None
    assert row.parse_status == STATIC_POST_VIEW_COUNT_NOT_APPLICABLE


def test_normalize_dom_grid_rows_can_filter_to_reels_only() -> None:
    rows = normalize_dom_grid_rows(
        [
            {"path": "/liv_cos/reel/REEL123/", "visibleNumericTexts": ["1,234"]},
            {"path": "/liv_cos/p/STATIC123/", "visibleNumericTexts": ["4,264"]},
        ],
        final_url="https://www.instagram.com/liv_cos/reels/",
        profile_handle="liv_cos",
        allowed_kinds=(MEDIA_KIND_REEL,),
    )

    assert len(rows) == 1
    assert rows[0].shortcode == "REEL123"
    assert rows[0].kind == "reel"

def test_normalize_dom_grid_rows_marks_hidden_numeric_collision_ambiguous() -> None:
    rows = normalize_dom_grid_rows(
        [
            {
                "path": "/jeremyfragrance/reel/COLLISION/",
                "visibleNumericTexts": ["30"],
                "leafNumericTexts": [
                    {"text": "30"},
                    {"text": "4"},
                    {"text": "30"},
                ],
            }
        ],
        final_url="https://www.instagram.com/jeremyfragrance/reels/",
        profile_handle="jeremyfragrance",
    )

    assert len(rows) == 1
    row = rows[0]
    assert row.views_text == "30"
    assert row.likes_text is None
    assert row.comments_text is None
    assert row.hidden_engagement_candidates == ("4", "30")
    assert row.parse_status == AMBIGUOUS_HIDDEN_NUMERIC


def test_normalize_dom_grid_rows_dedupes_by_shortcode_across_path_variants() -> None:
    rows = normalize_dom_grid_rows(
        [
            {"path": "/jeremyfragrance/reel/DUPLICATE/", "visibleNumericTexts": ["1"]},
            {"href": "https://www.instagram.com/jeremyfragrance/reel/DUPLICATE/?utm=grid", "visibleNumericTexts": ["1"]},
            {"path": "/reel/DUPLICATE", "visibleNumericTexts": ["1"]},
        ],
        final_url="https://www.instagram.com/jeremyfragrance/reels/",
        profile_handle="jeremyfragrance",
    )

    assert len(rows) == 1
    assert rows[0].shortcode == "DUPLICATE"


def test_iter_json_media_candidates_parses_clips_user_shape() -> None:
    payload = {
        "items": [
            {
                "media": {
                    "code": "DZ4Stb5MVPB",
                    "taken_at": 1782112975,
                    "caption": {"text": "REFRESH By Game Of Spades. #fragrance"},
                    "product_type": "clips",
                    "ig_play_count": 2984,
                    "like_count": 30,
                    "comment_count": 4,
                    "is_paid_partnership": False,
                    "is_affiliate": False,
                    "edge_media_to_sponsor_user": {"edges": [{"node": {"username": "brand"}}]},
                }
            }
        ]
    }

    [candidate] = iter_json_media_candidates(payload, source_surface=CLIPS_USER_JSON_METADATA)

    assert candidate.source_surface == CLIPS_USER_JSON_METADATA
    assert candidate.shortcode == "DZ4Stb5MVPB"
    assert candidate.taken_at_utc == "2026-06-22T07:22:55Z"
    assert candidate.caption_text == "REFRESH By Game Of Spades. #fragrance"
    assert candidate.product_type == "clips"
    assert candidate.video_or_play_count == 2984
    assert candidate.video_or_play_count_key == "ig_play_count"
    assert candidate.video_or_play_count_candidates == (("ig_play_count", 2984),)
    assert candidate.like_count == 30
    assert candidate.comment_count == 4
    assert candidate.is_paid_partnership is False
    assert candidate.is_affiliate is False
    assert candidate.sponsor_users == ("brand",)


def test_iter_json_media_candidates_prefers_clips_ig_play_count_and_preserves_count_keys() -> None:
    payload = {
        "items": [
            {
                "media": {
                    "code": "COUNTKEYS",
                    "ig_play_count": 2984,
                    "play_count": 2000,
                    "video_view_count": 655,
                    "view_count": 650,
                }
            }
        ]
    }

    [candidate] = iter_json_media_candidates(payload, source_surface=CLIPS_USER_JSON_METADATA)

    assert candidate.video_or_play_count == 2984
    assert candidate.video_or_play_count_key == "ig_play_count"
    assert candidate.video_or_play_count_candidates == (
        ("ig_play_count", 2984),
        ("play_count", 2000),
        ("video_view_count", 655),
        ("view_count", 650),
    )


def test_iter_json_media_candidates_ignores_device_timestamp_and_guards_bad_epoch() -> None:
    payload = {
        "items": [
            {"media": {"code": "DEVICEONLY", "device_timestamp": 1782112975123456}},
            {"media": {"code": "BADTAKENAT", "taken_at": 1782112975123456}},
        ]
    }

    candidates = iter_json_media_candidates(payload, source_surface=CLIPS_USER_JSON_METADATA)

    assert [(candidate.shortcode, candidate.taken_at_timestamp, candidate.taken_at_utc) for candidate in candidates] == [
        ("DEVICEONLY", None, None),
        ("BADTAKENAT", 1782112975123456, None),
    ]


def test_iter_json_media_candidates_does_not_recurse_inside_matched_media_or_accept_int_code() -> None:
    payload = {
        "error": {"code": 400, "message": "not media"},
        "items": [
            {
                "media": {
                    "code": "PARENT",
                    "like_count": 5,
                    "nested": {"code": "CHILD", "like_count": 99},
                }
            }
        ],
    }

    candidates = iter_json_media_candidates(payload, source_surface=CLIPS_USER_JSON_METADATA)

    assert [(candidate.shortcode, candidate.like_count) for candidate in candidates] == [("PARENT", 5)]


def test_iter_json_media_candidates_parses_web_profile_info_shape() -> None:
    payload = {
        "data": {
            "user": {
                "edge_owner_to_timeline_media": {
                    "edges": [
                        {
                            "node": {
                                "shortcode": "DZ4SvBvs6PB",
                                "__typename": "GraphVideo",
                                "is_video": True,
                                "taken_at_timestamp": 1782112969,
                                "edge_media_to_caption": {
                                    "edges": [{"node": {"text": "SUPERZ Fragrances Budapest."}}]
                                },
                                "video_view_count": 653,
                                "edge_media_preview_like": {"count": 13},
                                "edge_media_to_comment": {"count": 0},
                            }
                        }
                    ],
                    "page_info": {"has_next_page": False},
                }
            }
        }
    }

    [candidate] = iter_json_media_candidates(payload, source_surface=WEB_PROFILE_INFO_JSON_METADATA)

    assert candidate.source_surface == WEB_PROFILE_INFO_JSON_METADATA
    assert candidate.shortcode == "DZ4SvBvs6PB"
    assert candidate.taken_at_utc == "2026-06-22T07:22:49Z"
    assert candidate.caption_text == "SUPERZ Fragrances Budapest."
    assert candidate.video_or_play_count == 653
    assert candidate.video_or_play_count_key == "video_view_count"
    assert candidate.video_or_play_count_candidates == (("video_view_count", 653),)
    assert candidate.like_count == 13
    assert candidate.comment_count == 0
    assert candidate.typename == "GraphVideo"
    assert candidate.is_video is True


def test_join_preserves_conflicting_source_surface_candidates_without_selection() -> None:
    [dom_row] = normalize_dom_grid_rows(
        [
            {
                "path": "/jeremyfragrance/reel/DZ4Stb5MVPB/",
                "visibleNumericTexts": ["2,984"],
                "leafNumericTexts": [{"text": "30"}, {"text": "4"}, {"text": "2,984"}],
            }
        ],
        final_url="https://www.instagram.com/jeremyfragrance/reels/",
    )
    [web_candidate] = iter_json_media_candidates(
        {"shortcode": "DZ4Stb5MVPB", "video_view_count": 655, "edge_media_preview_like": {"count": 30}},
        source_surface=WEB_PROFILE_INFO_JSON_METADATA,
    )
    [clips_candidate] = iter_json_media_candidates(
        {"code": "DZ4Stb5MVPB", "ig_play_count": 2984, "like_count": 30, "comment_count": 4},
        source_surface=CLIPS_USER_JSON_METADATA,
    )

    [joined] = join_dom_rows_with_json_candidates(dom_rows=[dom_row], candidates=[web_candidate, clips_candidate])

    assert joined.dom_row.views_text == "2,984"
    assert [(c.source_surface, c.video_or_play_count) for c in joined.source_surface_candidates] == [
        (WEB_PROFILE_INFO_JSON_METADATA, 655),
        (CLIPS_USER_JSON_METADATA, 2984),
    ]


def test_source_surface_from_url_or_path_labels_known_ig_surfaces() -> None:
    assert source_surface_from_url_or_path("https://www.instagram.com/api/v1/clips/user/?x=1") == CLIPS_USER_JSON_METADATA
    assert source_surface_from_url_or_path("/api/v1/users/web_profile_info/") == WEB_PROFILE_INFO_JSON_METADATA
    assert source_surface_from_url_or_path("/graphql/query/") == "profile_feed_json_metadata"
    assert source_surface_from_url_or_path("/some/other.json") == "passive_page_json_metadata"
