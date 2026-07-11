from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pytest

import source_capture.tiktok.creator_onboarding as onboarding
from runners import run_source_capture_tiktok_creator_onboarding as runner
from source_capture.adapters.browser_snapshot import (
    BrowserPageObservationSuccess,
    BrowserPageResponse,
)
from source_capture.auth_state import AuthenticatedSessionMode
from source_capture.session_profiles import (
    OWNER_HANDOFF_BEFORE_ACTION,
    SourceCaptureSessionProfile,
)
from source_capture.source_access_provenance import HarnessProxyProfilePosture
from source_capture.tiktok.creator_onboarding import (
    TIKTOK_ONBOARDING_RECEIPT_JSON_NAME,
    TIKTOK_ONBOARDING_SELECTION_JSON_NAME,
    TikTokCreatorOnboardingError,
    build_tiktok_grid_window,
    is_tiktok_profile_item_list_url,
    run_tiktok_creator_onboarding,
)


def _response(items: list[dict[str, object]]) -> BrowserPageResponse:
    return BrowserPageResponse(
        requested_url="https://www.tiktok.com/api/post/item_list/?cursor=0",
        final_url="https://www.tiktok.com/api/post/item_list/?cursor=0",
        status=200,
        ok=True,
        body_text=json.dumps({"itemList": items}),
        response_headers={"content-type": "application/json"},
    )


def _item(video_id: str, views: int, likes: int) -> dict[str, object]:
    return {
        "id": video_id,
        "author": {"uniqueId": "creator"},
        "stats": {"playCount": views, "diggCount": likes},
    }


def _capture(
    *,
    ordered_ids: list[str],
    items: list[dict[str, object]],
    suggested: list[dict[str, object]] | None = None,
) -> BrowserPageObservationSuccess:
    dom: dict[str, object]
    if suggested is not None:
        dom = {"suggested_accounts": suggested}
    else:
        dom = {
            "ordered_videos": [
                {
                    "video_id": video_id,
                    "video_url": f"https://www.tiktok.com/@creator/video/{video_id}",
                }
                for video_id in ordered_ids
            ],
            "hydration_json_text": None,
        }
    return BrowserPageObservationSuccess(
        requested_url="https://www.tiktok.com/@creator",
        final_url="https://www.tiktok.com/@creator",
        title="creator",
        visible_text="",
        dom_observation=dom,
        responses=[] if suggested is not None else [_response(items)],
        metadata={
            "post_load_pointer_actions": [],
            "human_challenge_handoff_attempts": [],
            "lazy_load_scroll_passes_executed": 2,
            "lazy_load_scroll_stop_reason": "response_target_reached",
            "lazy_load_response_stop_condition_configured": True,
        },
        warning_notes=[],
        limitation_notes=[],
    )


@dataclass
class _FakeEngine:
    outcomes: list[BrowserPageObservationSuccess]

    def __post_init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def capture_page_observation(self, **kwargs: object) -> BrowserPageObservationSuccess:
        self.calls.append(dict(kwargs))
        return self.outcomes.pop(0)


def _profile() -> SourceCaptureSessionProfile:
    return SourceCaptureSessionProfile(
        alias="chowdakr_sg_tiktok",
        platform="tiktok",
        state_label="chowdakr_sg_tiktok",
        session_mode=AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
        required_harness_proxy_profile_posture=(
            HarnessProxyProfilePosture.NO_PROXY_PROFILE_LOADED
        ),
        browser_backend="cloakbrowser",
        challenge_policy=OWNER_HANDOFF_BEFORE_ACTION,
    )


def test_runner_defaults_cold_agents_to_cookie_backed_session_alias(tmp_path: Path) -> None:
    args = runner.build_parser().parse_args(
        [
            "--creator-handle",
            "creator",
            "--output-dir",
            str(tmp_path),
        ]
    )

    assert args.session_profile == "chowdakr_sg_tiktok"

def test_profile_item_list_predicate_is_exact_and_local() -> None:
    assert is_tiktok_profile_item_list_url(
        "https://www.tiktok.com/api/post/item_list/?cursor=30"
    )
    assert not is_tiktok_profile_item_list_url(
        "https://www.tiktok.com/api/repost/item_list/?cursor=30"
    )
    assert not is_tiktok_profile_item_list_url(
        "https://example.com/api/post/item_list/?cursor=30"
    )


def test_grid_window_preserves_source_visible_order_and_complete_metrics() -> None:
    capture = _capture(
        ordered_ids=["3", "1", "2", "4"],
        items=[
            _item("1", 100, 10),
            _item("2", 200, 20),
            _item("3", 300, 30),
            _item("4", 400, 40),
        ],
    )

    window = build_tiktok_grid_window(
        creator_handle="creator",
        capture=capture,
        window_size=3,
    )

    assert [item["video_id"] for item in window["items"]] == ["3", "1", "2"]
    assert window["collection_receipt"]["scroll_stop_reason"] == "response_target_reached"


def test_grid_window_accepts_missing_author_with_exact_creator_url() -> None:
    capture = _capture(
        ordered_ids=["1"],
        items=[{"id": "1", "stats": {"playCount": 100, "diggCount": 10}}],
    )

    window = build_tiktok_grid_window(
        creator_handle="creator",
        capture=capture,
        window_size=1,
    )

    assert [item["video_id"] for item in window["items"]] == ["1"]


def test_grid_window_excludes_unrelated_handle_dom_url() -> None:
    capture = _capture(
        ordered_ids=["1"],
        items=[_item("1", 100, 10)],
    )
    capture.dom_observation["ordered_videos"][0]["video_url"] = (
        "https://www.tiktok.com/@unrelated/video/1"
    )

    with pytest.raises(TikTokCreatorOnboardingError, match="complete grid window"):
        build_tiktok_grid_window(
            creator_handle="creator",
            capture=capture,
            window_size=1,
        )


def test_grid_window_excludes_explicit_mismatched_payload_author() -> None:
    capture = _capture(
        ordered_ids=["1"],
        items=[
            {
                "id": "1",
                "author": {"uniqueId": "unrelated"},
                "stats": {"playCount": 100, "diggCount": 10},
            }
        ],
    )

    with pytest.raises(TikTokCreatorOnboardingError, match="complete grid window"):
        build_tiktok_grid_window(
            creator_handle="creator",
            capture=capture,
            window_size=1,
        )


def test_grid_window_does_not_count_nested_item_list_metric_node() -> None:
    creator_item = _item("1", 100, 10)
    creator_item["duetInfo"] = {
        "id": "999",
        "stats": {"playCount": 99999, "diggCount": 9999},
    }
    capture = _capture(
        ordered_ids=["1", "999"],
        items=[creator_item],
    )

    with pytest.raises(TikTokCreatorOnboardingError, match="complete grid window"):
        build_tiktok_grid_window(
            creator_handle="creator",
            capture=capture,
            window_size=2,
        )


def test_onboarding_writes_selection_before_same_engine_deep_capture(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state_path = tmp_path / "state.json"
    state_path.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(
        onboarding,
        "validate_auth_state_provenance_requirement",
        lambda *_args, **_kwargs: state_path,
    )
    suggested = _capture(
        ordered_ids=[],
        items=[],
        suggested=[
            {
                "handle": "adjacent",
                "profile_url": "https://www.tiktok.com/@adjacent",
                "display_text_or_none": "Adjacent",
            }
        ],
    )
    grid = _capture(
        ordered_ids=["1", "2", "3", "4"],
        items=[
            _item("1", 400, 20),
            _item("2", 300, 60),
            _item("3", 200, 10),
            _item("4", 100, 5),
        ],
    )
    engine = _FakeEngine([suggested, grid])
    deep_calls: list[dict[str, object]] = []

    def deep_capture(**kwargs: object) -> dict[str, object]:
        deep_calls.append(dict(kwargs))
        assert kwargs["engine"] is engine
        assert (tmp_path / TIKTOK_ONBOARDING_SELECTION_JSON_NAME).is_file()
        return {
            "grid_result": {"response_items": []},
            "cadence_result": {
                "requested_video_count": 2,
                "completed_count": 2,
                "results": [{}, {}],
                "failures": [],
            },
        }

    paths = run_tiktok_creator_onboarding(
        creator_handle="creator",
        session_profile=_profile(),
        output_dir=tmp_path,
        auth_state_root=tmp_path,
        window_size=4,
        selection_fraction=0.5,
        engine=engine,
        deep_capture_fn=deep_capture,
        cadence_min_gap_seconds=0,
        cadence_max_gap_seconds=0,
    )

    assert len(engine.calls) == 2
    assert engine.calls[1]["dom_extract_arg"] == {"creator_handle": "creator"}
    assert len(deep_calls) == 1
    assert deep_calls[0]["video_urls"] == [
        "https://www.tiktok.com/@creator/video/2",
        "https://www.tiktok.com/@creator/video/1",
    ]
    receipt = json.loads(paths.onboarding_receipt_json_path.read_text(encoding="utf-8"))
    assert receipt["status"] == "complete"
    assert receipt["session_profile"] == "chowdakr_sg_tiktok"
    assert receipt["window_size"] == 4
    assert receipt["selection_fraction"] == 0.5
    assert receipt["suggested_accounts_status_or_none"] == "captured"
    assert receipt["completed_deep_capture_count"] == 2


def test_incomplete_grid_fails_before_selection_or_deep_capture(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state_path = tmp_path / "state.json"
    state_path.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(
        onboarding,
        "validate_auth_state_provenance_requirement",
        lambda *_args, **_kwargs: state_path,
    )
    engine = _FakeEngine(
        [
            _capture(ordered_ids=[], items=[], suggested=[]),
            _capture(
                ordered_ids=["1", "2", "3", "4"],
                items=[
                    _item("1", 400, 20),
                    _item("2", 300, 30),
                    _item("3", 200, 20),
                ],
            ),
        ]
    )
    deep_called = False

    def deep_capture(**_kwargs: object) -> dict[str, object]:
        nonlocal deep_called
        deep_called = True
        return {}

    with pytest.raises(TikTokCreatorOnboardingError, match="complete grid window"):
        run_tiktok_creator_onboarding(
            creator_handle="creator",
            session_profile=_profile(),
            output_dir=tmp_path,
            auth_state_root=tmp_path,
            window_size=4,
            engine=engine,
            deep_capture_fn=deep_capture,
        )

    assert deep_called is False
    assert not (tmp_path / TIKTOK_ONBOARDING_SELECTION_JSON_NAME).exists()
    receipt = json.loads(
        (tmp_path / TIKTOK_ONBOARDING_RECEIPT_JSON_NAME).read_text(encoding="utf-8")
    )
    assert receipt["status"] == "failed"
    assert receipt["terminal_stage"] == "freeze_window"
    assert receipt["error_or_none"].startswith("TikTokCreatorOnboardingError:")


def test_onboarding_cli_defaults_to_nine_fourteen_second_range() -> None:
    args = runner.build_parser().parse_args(
        [
            "--creator-handle",
            "creator",
            "--output-dir",
            "out",
        ]
    )

    assert args.cadence_min_gap_seconds == 9.0
    assert args.cadence_max_gap_seconds == 14.0
    assert (args.cadence_min_gap_seconds + args.cadence_max_gap_seconds) / 2 == 11.5
