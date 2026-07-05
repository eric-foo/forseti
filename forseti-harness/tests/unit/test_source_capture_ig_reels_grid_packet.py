from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, raw_shard
import runners.run_source_capture_ig_reels_grid_packet as reels_grid_runner
from runners.run_source_capture_ig_reels_grid_packet import _bio_links
from runners.run_source_capture_ig_reels_grid_packet import _detect_ig_block
from runners.run_source_capture_ig_reels_grid_packet import main as reels_grid_main
from runners.run_source_capture_ig_reels_grid_packet import run_source_capture_ig_reels_grid_packet
from source_capture.ig_reels_grid_capture import (
    IgReelsGridCaptureFailure,
    IgReelsGridCaptureSuccess,
    IgReelsGridPassiveResponse,
)


def _fake_capture(**_kwargs):
    web_profile = {
        "data": {
            "user": {
                "id": "5802114508",
                "full_name": "Hyram",
                "biography": "Just your average skin care addict",
                "external_url": "https://example.test/video",
                "bio_links": [{"title": "Video", "url": "https://example.test/video"}],
                "profile_pic_url": "https://example.test/pic.jpg",
                "is_verified": True,
                "is_private": False,
                "category_name": "Reel creator",
                "edge_followed_by": {"count": 722810},
                "edge_follow": {"count": 2339},
                "edge_owner_to_timeline_media": {
                    "count": 321,
                    "edges": [
                        {
                            "node": {
                                "shortcode": "REEL123",
                                "__typename": "GraphVideo",
                                "is_video": True,
                                "taken_at_timestamp": 1750797556,
                                "edge_media_to_caption": {
                                    "edges": [{"node": {"text": "Web profile caption"}}]
                                },
                                "video_view_count": 1200,
                                "edge_media_preview_like": {"count": 55},
                                "edge_media_to_comment": {"count": 6},
                            }
                        }
                    ],
                },
            }
        }
    }
    clips = {
        "items": [
            {
                "media": {
                    "code": "REEL123",
                    "taken_at": 1750797556,
                    "caption": {"text": "Clips caption #ad"},
                    "product_type": "clips",
                    "ig_play_count": 1234,
                    "like_count": 56,
                    "comment_count": 7,
                    "is_paid_partnership": False,
                    "is_affiliate": False,
                }
            }
        ]
    }
    return IgReelsGridCaptureSuccess(
        requested_url="https://www.instagram.com/hyram/reels/",
        final_url="https://www.instagram.com/hyram/reels/",
        title="Hyram reels",
        visible_text="Hyram\n723K followers\n321 posts",
        dom_rows=[
            {
                "path": "/hyram/reel/REEL123/",
                "visibleText": "1,234",
                "visibleNumericTexts": ["1,234"],
                "leafNumericTexts": [{"text": "56"}, {"text": "7"}, {"text": "1,234"}],
                "rect": {"x": 0, "y": 0, "width": 200, "height": 300},
            }
        ],
        passive_json_responses=[
            IgReelsGridPassiveResponse(
                source_surface="web_profile_info_json_metadata",
                requested_url="https://www.instagram.com/api/v1/users/web_profile_info/?username=hyram",
                final_url="https://www.instagram.com/api/v1/users/web_profile_info/?username=hyram",
                status=200,
                ok=True,
                body_text=json.dumps(web_profile),
                response_headers={"content-type": "application/json"},
            ),
            IgReelsGridPassiveResponse(
                source_surface="clips_user_json_metadata",
                requested_url="https://www.instagram.com/api/v1/clips/user/?target_user_id=5802114508",
                final_url="https://www.instagram.com/api/v1/clips/user/?target_user_id=5802114508",
                status=200,
                ok=True,
                body_text=json.dumps(clips),
                response_headers={"content-type": "application/json"},
            ),
        ],
        metadata={
            "requested_url": "https://www.instagram.com/hyram/reels/",
            "final_url": "https://www.instagram.com/hyram/reels/",
            "capture_timestamp": "2026-06-22T10:00:00Z",
            "proxy_used": False,
            "proxy_endpoint_recorded": False,
            "proxy_exit_ip_recorded": False,
            "block_heavy_assets": True,
            "viewport_width": 1080,
            "viewport_height": 1920,
        },
    )


def test_reels_grid_runner_writes_packet_without_item_page_fanout(tmp_path: Path) -> None:
    output = tmp_path / "ig_reels_packet"

    exit_code, message = run_source_capture_ig_reels_grid_packet(
        handle="hyram",
        output_directory=output,
        decision_question="capture hyram reels grid",
        capture_fetcher=_fake_capture,
    )

    assert exit_code == 0
    assert Path(message) == output.resolve()
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["source_surface"] == "ig_reels_grid_dom_passive_json"
    assert "ig_reels_grid_no_item_fanout:rows=1:json_candidates=2:passive_json=2" in manifest["visible_mode_changes"]
    assert manifest["source_slices"][0]["metric_observations"][0]["metric"] == "follower_count"
    assert manifest["source_slices"][0]["metric_observations"][0]["value"] == 722810
    item_metrics = manifest["source_slices"][1]["metric_observations"]
    assert {item["metric"]: item["value"] for item in item_metrics if item["posture"] == "observed"} == {
        "view_count": 1234,
        "like_count": 56,
        "comment_count": 7,
    }
    payload = json.loads((output / "raw" / "01_ig_reels_grid_capture.json").read_text(encoding="utf-8"))
    assert payload["creator_profile_snapshot"]["bio"] == "Just your average skin care addict"
    assert payload["creator_profile_snapshot"]["bio_links"] == [
        {"title": "Video", "url": "https://example.test/video"}
    ]
    assert payload["joined_rows"][0]["dom_row"]["shortcode"] == "REEL123"
    captions = {item["caption_text"] for item in payload["joined_rows"][0]["source_surface_candidates"]}
    assert "Clips caption #ad" in captions
    assert "Web profile caption" in captions




def _fake_capture_with_pinned_reel(**_kwargs):
    result = _fake_capture(**_kwargs)
    web_response = result.passive_json_responses[0]
    clips = {
        "items": [
            {
                "media": {
                    "code": "PINOLD",
                    "taken_at": 1000,
                    "ig_play_count": 10,
                    "clips_tab_pinned_user_ids": [5802114508],
                    "timeline_pinned_user_ids": [],
                }
            },
            {"media": {"code": "NEWEST", "taken_at": 9000, "ig_play_count": 20}},
            {"media": {"code": "OLDER", "taken_at": 8000, "ig_play_count": 30}},
        ]
    }
    clips_response = IgReelsGridPassiveResponse(
        source_surface="clips_user_json_metadata",
        requested_url="https://www.instagram.com/api/v1/clips/user/?target_user_id=5802114508",
        final_url="https://www.instagram.com/api/v1/clips/user/?target_user_id=5802114508",
        status=200,
        ok=True,
        body_text=json.dumps(clips),
        response_headers={"content-type": "application/json"},
    )
    return replace(
        result,
        dom_rows=[
            {
                "path": f"/hyram/reel/{code}/",
                "visibleNumericTexts": ["10"],
                "rect": {"x": 0, "y": 0, "width": 200, "height": 300},
            }
            for code in ("PINOLD", "NEWEST", "OLDER")
        ],
        passive_json_responses=[web_response, clips_response],
    )


def test_reels_grid_runner_emits_pinned_inference_cross_check(tmp_path: Path) -> None:
    output = tmp_path / "ig_reels_pinned_packet"

    exit_code, message = run_source_capture_ig_reels_grid_packet(
        handle="hyram",
        output_directory=output,
        decision_question="capture hyram reels grid",
        capture_fetcher=_fake_capture_with_pinned_reel,
    )

    assert exit_code == 0
    payload = json.loads((output / "raw" / "01_ig_reels_grid_capture.json").read_text(encoding="utf-8"))
    inference = payload["pinned_inference"]
    # In grid order the pinned reel is older yet sits above newer reels -> recency
    # inversion flags it, and it independently agrees with the explicit clips_tab flag.
    assert inference["reels_tab_inferred_pinned_by_recency"] == ["PINOLD"]
    assert inference["reels_tab_explicit_pinned_shortcodes"] == ["PINOLD"]
    assert inference["recency_matches_explicit"] is True


def _fake_capture_with_static_post_row(**_kwargs):
    result = _fake_capture(**_kwargs)
    return replace(
        result,
        dom_rows=[
            *result.dom_rows,
            {
                "path": "/hyram/p/STATIC123/",
                "visibleText": "4,264",
                "visibleNumericTexts": ["4,264"],
                "leafNumericTexts": [{"text": "99"}, {"text": "8"}, {"text": "4,264"}],
                "rect": {"x": 210, "y": 0, "width": 200, "height": 300},
            },
        ],
    )



def test_reels_grid_runner_filters_static_post_rows_from_reels_series(tmp_path: Path) -> None:
    output = tmp_path / "ig_reels_static_filtered_packet"

    exit_code, message = run_source_capture_ig_reels_grid_packet(
        handle="hyram",
        output_directory=output,
        decision_question="capture hyram reels grid",
        capture_fetcher=_fake_capture_with_static_post_row,
    )

    assert exit_code == 0
    assert Path(message) == output.resolve()
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert any("static_profile_grid_rows_filtered: 1" in item for item in manifest["limitations"])
    grid_slices = [item for item in manifest["source_slices"] if item["slice_id"].startswith("ig_reels_grid_")]
    assert len(grid_slices) == 1

    payload = json.loads((output / "raw" / "01_ig_reels_grid_capture.json").read_text(encoding="utf-8"))
    assert [row["shortcode"] for row in payload["dom_rows"]] == ["REEL123"]

def test_reels_grid_runner_can_commit_to_data_lake(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")

    exit_code, message = run_source_capture_ig_reels_grid_packet(
        handle="@hyram",
        data_root=root,
        decision_question="capture hyram reels grid",
        capture_fetcher=_fake_capture,
    )

    assert exit_code == 0
    packet_dir = Path(message)
    assert packet_dir.parent == root.path / "raw" / raw_shard(packet_dir.name)
    assert root.find_packet(packet_dir.name) is not None
    assert root.read_availability(packet_dir.name) is not None



def _fake_views_only_capture(**_kwargs):
    result = _fake_capture(**_kwargs)
    metadata = dict(result.metadata)
    metadata["block_heavy_assets"] = False
    return IgReelsGridCaptureSuccess(
        requested_url=result.requested_url,
        final_url=result.final_url,
        title=result.title,
        visible_text=result.visible_text,
        dom_rows=[
            {
                "path": "/hyram/reel/REEL123/",
                "visibleText": "1,234",
                "visibleNumericTexts": ["1,234"],
                "leafNumericTexts": [{"text": "1,234"}],
                "rect": {"x": 0, "y": 0, "width": 200, "height": 300},
            }
        ],
        passive_json_responses=result.passive_json_responses,
        metadata=metadata,
    )


def _fake_capture_without_timestamp(**_kwargs):
    result = _fake_capture(**_kwargs)
    metadata = {key: value for key, value in result.metadata.items() if key != "capture_timestamp"}
    return IgReelsGridCaptureSuccess(
        requested_url=result.requested_url,
        final_url=result.final_url,
        title=result.title,
        visible_text=result.visible_text,
        dom_rows=result.dom_rows,
        passive_json_responses=result.passive_json_responses,
        metadata=metadata,
    )


def test_reels_grid_runner_allows_heavy_assets_with_row_limitations(tmp_path: Path) -> None:
    output = tmp_path / "ig_reels_views_only_packet"

    exit_code, message = run_source_capture_ig_reels_grid_packet(
        handle="hyram",
        output_directory=output,
        decision_question="capture hyram reels grid",
        block_heavy_assets=False,
        capture_fetcher=_fake_views_only_capture,
    )

    assert exit_code == 0
    assert Path(message) == output.resolve()
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert any("media_slice_limitations_present: 1" in item for item in manifest["limitations"])
    assert "heavy_asset_blocking_enabled" not in "\n".join(manifest["limitations"])
    assert manifest["source_slices"][1]["limitations"] == [
        "dom_parse_status=views_only_no_hidden_engagement"
    ]


def test_reels_grid_runner_missing_capture_timestamp_is_unknown_not_known(tmp_path: Path) -> None:
    output = tmp_path / "ig_reels_missing_timestamp_packet"

    exit_code, message = run_source_capture_ig_reels_grid_packet(
        handle="hyram",
        output_directory=output,
        decision_question="capture hyram reels grid",
        capture_fetcher=_fake_capture_without_timestamp,
    )

    assert exit_code == 0
    assert Path(message) == output.resolve()
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["source_slices"][1]["timing"]["capture_time"] == {
        "reason": "capture timestamp missing from browser capture metadata",
        "status": "unknown_with_reason",
        "value": None,
    }
    observed_metric = manifest["source_slices"][1]["metric_observations"][0]
    assert observed_metric["posture"] == "observed"
    assert observed_metric["coverage_window"] is None


def test_reels_grid_main_prefers_explicit_output_over_forseti_data_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    output = tmp_path / "scratch-output"
    captured: dict[str, object] = {}

    def fake_run_source_capture_ig_reels_grid_packet(**kwargs):
        captured.update(kwargs)
        return 0, str(output.resolve())

    monkeypatch.setenv("FORSETI_DATA_ROOT", str(root.path))
    monkeypatch.setattr(
        reels_grid_runner,
        "run_source_capture_ig_reels_grid_packet",
        fake_run_source_capture_ig_reels_grid_packet,
    )

    assert reels_grid_main(
        [
            "--handle",
            "hyram",
            "--decision-question",
            "capture hyram reels grid",
            "--output",
            str(output),
        ]
    ) == 0

    assert captured["output_directory"] == output
    assert captured["data_root"] is None


def test_bio_links_captures_title_and_url_with_lynx_fallback() -> None:
    assert _bio_links(
        [
            {"title": "Shop", "url": "https://example.test/shop"},
            {"title": "Linktree", "lynx_url": "https://lynx.test/abc"},
            {"title": None, "url": None},
            "not-a-dict",
        ]
    ) == [
        {"title": "Shop", "url": "https://example.test/shop"},
        {"title": "Linktree", "url": "https://lynx.test/abc"},
    ]
    assert _bio_links(None) is None
    assert _bio_links([]) == []


# --- Exit-code contract (the typed signals the durability wrapper branches on) ---


def _fake_capture_blocked(**_kwargs):
    result = _fake_capture(**_kwargs)
    return replace(result, visible_text="Please wait a few minutes before you try again.")


def test_run_returns_exit_5_and_writes_no_packet_on_access_block(tmp_path: Path) -> None:
    output = tmp_path / "ig_reels_blocked_packet"

    exit_code, message = run_source_capture_ig_reels_grid_packet(
        handle="hyram",
        output_directory=output,
        decision_question="capture hyram reels grid",
        capture_fetcher=_fake_capture_blocked,
    )

    # Durability contract: a detected access block fails closed with exit 5 and NO packet.
    assert exit_code == 5
    assert "access-blocked" in message
    assert not (output / "manifest.json").exists()


def _fake_capture_failure(**_kwargs):
    return IgReelsGridCaptureFailure(
        requested_url="https://www.instagram.com/hyram/reels/",
        failure_kind="capture_failed",
        message="browser page observation capture failed",
        final_url="https://www.instagram.com/hyram/reels/",
    )


def test_run_returns_exit_3_and_writes_no_packet_on_capture_failure(tmp_path: Path) -> None:
    output = tmp_path / "ig_reels_capture_failed_packet"

    exit_code, message = run_source_capture_ig_reels_grid_packet(
        handle="hyram",
        output_directory=output,
        decision_question="capture hyram reels grid",
        capture_fetcher=_fake_capture_failure,
    )

    # Durability contract: a capture failure is the bounded-retry signal, exit 3 (not a block).
    assert exit_code == 3
    assert "capture failed" in message.lower()
    assert not (output / "manifest.json").exists()


def test_detect_ig_block_covers_each_access_block_reason() -> None:
    # The exit-5 contract the durability doctrine depends on: every block reason maps,
    # including network_security_block (the de-correlated review's catch). A clean page is None.
    assert (
        _detect_ig_block(
            final_url="https://www.instagram.com/accounts/login/", title=None, visible_text=""
        )
        == "redirected_to_login"
    )
    assert (
        _detect_ig_block(
            final_url="https://www.instagram.com/hyram/reels/",
            title=None,
            visible_text="Please wait a few minutes before you try again.",
        )
        == "rate_limited_429_interstitial"
    )
    assert (
        _detect_ig_block(
            final_url="https://www.instagram.com/hyram/reels/",
            title="Instagram",
            visible_text="You've been blocked from accessing this content.",
        )
        == "network_security_block"
    )
    assert (
        _detect_ig_block(
            final_url="https://www.instagram.com/challenge/action/", title=None, visible_text=""
        )
        == "challenge_route"
    )
    assert (
        _detect_ig_block(
            final_url="https://www.instagram.com/hyram/reels/", title="Hyram", visible_text="reels"
        )
        is None
    )


# --- Reels-tab scoping of pinned_inference (main-grid/timeline pins stay out) ---


def _fake_capture_with_timeline_pin(**_kwargs):
    result = _fake_capture(**_kwargs)
    web_response = result.passive_json_responses[0]
    clips = {
        "items": [
            {"media": {"code": "RECENT1", "taken_at": 9000, "ig_play_count": 10, "clips_tab_pinned_user_ids": []}},
            {"media": {"code": "RECENT2", "taken_at": 8000, "ig_play_count": 20, "clips_tab_pinned_user_ids": []}},
            {
                "media": {
                    "code": "GRIDPIN",
                    "taken_at": 100,
                    "ig_play_count": 30,
                    "clips_tab_pinned_user_ids": [],
                    "timeline_pinned_user_ids": [5802114508],
                }
            },
        ]
    }
    clips_response = IgReelsGridPassiveResponse(
        source_surface="clips_user_json_metadata",
        requested_url="https://www.instagram.com/api/v1/clips/user/?target_user_id=5802114508",
        final_url="https://www.instagram.com/api/v1/clips/user/?target_user_id=5802114508",
        status=200,
        ok=True,
        body_text=json.dumps(clips),
        response_headers={"content-type": "application/json"},
    )
    return replace(
        result,
        dom_rows=[
            {
                "path": f"/hyram/reel/{code}/",
                "visibleNumericTexts": ["10"],
                "rect": {"x": 0, "y": 0, "width": 200, "height": 300},
            }
            for code in ("RECENT1", "RECENT2", "GRIDPIN")
        ],
        passive_json_responses=[web_response, clips_response],
    )


def test_pinned_inference_excludes_main_grid_timeline_pins(tmp_path: Path) -> None:
    output = tmp_path / "ig_reels_timeline_pin_packet"

    exit_code, message = run_source_capture_ig_reels_grid_packet(
        handle="hyram",
        output_directory=output,
        decision_question="capture hyram reels grid",
        capture_fetcher=_fake_capture_with_timeline_pin,
    )

    assert exit_code == 0
    payload = json.loads((output / "raw" / "01_ig_reels_grid_capture.json").read_text(encoding="utf-8"))
    inference = payload["pinned_inference"]
    # A main-grid/timeline pin (pinned_on_timeline) is NOT a reels-tab pin: it stays out of the
    # reels summary's explicit and inferred sets, while remaining visible per-candidate.
    assert inference["reels_tab_explicit_pinned_shortcodes"] == []
    assert inference["reels_tab_inferred_pinned_by_recency"] == []
    gridpin = next(
        candidate
        for joined in payload["joined_rows"]
        for candidate in joined["source_surface_candidates"]
        if candidate["shortcode"] == "GRIDPIN"
    )
    assert gridpin["pinned_on_timeline"] is True
