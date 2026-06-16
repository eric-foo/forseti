from __future__ import annotations

import json

from source_capture.adapters.browser_snapshot import (
    BrowserContextResponse,
    BrowserContextResponsesSuccess,
)
from source_capture.ig_momentum_harvest import (
    extract_ig_shortcode,
    fetch_ig_profile_momentum,
)
from source_capture.proxy_profiles import ProxyCategory, ProxyProfile


def _success(request_id: str, body: dict) -> BrowserContextResponsesSuccess:
    return BrowserContextResponsesSuccess(
        page_url="https://www.instagram.com/hyram/",
        final_page_url="https://www.instagram.com/hyram/",
        responses=[
            BrowserContextResponse(
                request_id=request_id,
                requested_url=f"https://www.instagram.com/{request_id}",
                final_url=f"https://www.instagram.com/{request_id}",
                status=200,
                ok=True,
                body_text=json.dumps(body),
                response_headers={"content-type": "application/json"},
            )
        ],
        metadata={},
        warning_notes=[],
        limitation_notes=[],
    )


def test_extract_ig_shortcode_from_post_and_reel_urls() -> None:
    assert extract_ig_shortcode("https://www.instagram.com/hyram/p/AAA/") == "AAA"
    assert extract_ig_shortcode("https://www.instagram.com/hyram/reel/BBB/") == "BBB"
    assert extract_ig_shortcode("https://www.instagram.com/explore/") is None


def test_fetch_ig_profile_momentum_parses_profile_and_grid_pages_without_faking_zero() -> None:
    sleeps: list[float] = []
    proxy = ProxyProfile(
        proxy_endpoint="http://proxy_user:proxy_pass@example.proxy.test:1234",
        proxy_category=ProxyCategory.RESIDENTIAL_ROTATING,
        geoip_enabled=False,
    )
    seen_proxy_profiles: list[ProxyProfile | None] = []

    def fake_fetcher(**kwargs):
        seen_proxy_profiles.append(kwargs.get("proxy_profile"))
        request_id = kwargs["requests"][0].request_id
        if request_id == "web_profile_info":
            return _success(
                request_id,
                {
                    "data": {
                        "user": {
                            "id": "5802114508",
                            "edge_followed_by": {"count": 723000},
                            "edge_owner_to_timeline_media": {
                                "edges": [
                                    {
                                        "node": {
                                            "shortcode": "AAA",
                                            "is_video": False,
                                            "edge_liked_by": {"count": 0},
                                            "edge_media_to_comment": {"count": 2},
                                        }
                                    }
                                ],
                                "page_info": {"has_next_page": True, "end_cursor": "CURSOR"},
                            },
                        }
                    }
                },
            )
        assert request_id == "graphql_grid_01"
        return _success(
            request_id,
            {
                "data": {
                    "user": {
                        "edge_owner_to_timeline_media": {
                            "edges": [
                                {
                                    "node": {
                                        "shortcode": "BBB",
                                        "is_video": True,
                                        "video_view_count": 0,
                                        "edge_liked_by": {"count": 3},
                                        "edge_media_to_comment": {"count": 4},
                                        "taken_at_timestamp": 1720000000,
                                    }
                                },
                                {
                                    "node": {
                                        "shortcode": "CCC",
                                        "is_video": True,
                                        "video_view_count": 9876,
                                    }
                                },
                            ],
                            "page_info": {"has_next_page": False, "end_cursor": None},
                        }
                    }
                }
            },
        )

    capture = fetch_ig_profile_momentum(
        profile_url="https://www.instagram.com/hyram/",
        max_media=3,
        max_graphql_pages=1,
        request_gap_seconds=3.0,
        proxy_profile=proxy,
        sleep_fn=sleeps.append,
        browser_fetcher=fake_fetcher,
    )

    assert sleeps == [3.0]
    assert seen_proxy_profiles == [proxy, proxy]
    assert capture.numeric_id == "5802114508"
    assert capture.follower_count == 723000
    assert capture.media_by_shortcode["AAA"].is_video is False
    assert capture.media_by_shortcode["AAA"].like_count == 0
    assert capture.media_by_shortcode["BBB"].video_view_count == 0
    assert capture.media_by_shortcode["CCC"].video_view_count == 9876
    assert [response.request_id for response in capture.raw_responses] == [
        "web_profile_info",
        "graphql_grid_01",
    ]


def test_fetch_ig_profile_momentum_turns_empty_success_responses_into_limitation() -> None:
    def fake_fetcher(**_kwargs):
        return BrowserContextResponsesSuccess(
            page_url="https://www.instagram.com/hyram/",
            final_page_url="https://www.instagram.com/hyram/",
            responses=[],
            metadata={},
            warning_notes=[],
            limitation_notes=[],
        )

    capture = fetch_ig_profile_momentum(
        profile_url="https://www.instagram.com/hyram/",
        max_media=1,
        browser_fetcher=fake_fetcher,
    )

    assert capture.raw_responses[0].request_id == "browser_context_empty_response"
    assert capture.raw_responses[0].status is None
    assert capture.raw_responses[0].failure_message == "browser context response capture returned no responses"
    assert capture.limitation_notes == [
        "web_profile_info_unavailable: status=None failure=browser context response capture returned no responses"
    ]
