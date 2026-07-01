from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from runners import run_source_capture_tiktok_live_batch_probe as runner
from source_capture.adapters.browser_snapshot import (
    BrowserPageObservationSuccess,
    BrowserPageResponse,
)
from source_capture.auth_state import (
    AuthenticatedSessionMode,
    auth_state_path_for_label,
    write_auth_state_metadata,
)
from source_capture.tiktok.batch_packet import write_tiktok_batch_packet
from source_capture.tiktok.live_batch_probe import (
    is_tiktok_comment_list_url,
    write_tiktok_live_batch_probe_outputs,
)


@dataclass
class _FakeObservationEngine:
    outcomes: list[BrowserPageObservationSuccess]

    def __post_init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def capture_page_observation(
        self,
        *,
        url: str,
        timeout_seconds: float,
        wait_until: str,
        viewport_width: int,
        viewport_height: int,
        dom_extract_script: str,
        dom_extract_arg: object,
        response_url_predicate: Callable[[str], bool],
        post_load_action_script: str | None = None,
        post_load_action_arg: object = None,
        selector: str | None = None,
        selector_timeout_seconds: float = 5.0,
        max_response_bytes: int = 5_000_000,
        settle_seconds: float = 0.0,
        lazy_load_scroll_passes: int = 0,
        lazy_load_scroll_step_px: int = 0,
        block_resource_types: tuple[str, ...] = (),
        proxy_profile: object = None,
        storage_state_path: Path | None = None,
        headless: bool = True,
        browser_channel: str | None = None,
    ) -> BrowserPageObservationSuccess:
        self.calls.append(
            {
                "url": url,
                "headless": headless,
                "storage_state_path": storage_state_path,
                "post_load_action_script": post_load_action_script,
                "response_predicate_matches_comment_list": response_url_predicate(
                    "https://www.tiktok.com/api/comment/list/?aweme_id=7390000000000000001&cursor=0"
                ),
            }
        )
        return self.outcomes.pop(0)


def test_live_probe_writes_sanitized_staging_compatible_with_batch_admission(
    tmp_path: Path,
) -> None:
    auth_root = _auth_state(tmp_path)
    response_url = (
        "https://www.tiktok.com/api/comment/list/"
        "?aweme_id=7390000000000000001&cursor=0&count=20"
    )
    engine = _FakeObservationEngine(
        outcomes=[
            _success_observation(
                video_id="7390000000000000001",
                response=BrowserPageResponse(
                    requested_url=response_url,
                    final_url=response_url,
                    status=200,
                    ok=True,
                    body_text=json.dumps(
                        {
                            "cursor": 20,
                            "has_more": 1,
                            "total": 42,
                            "comments": [
                                {
                                    "cid": "7291",
                                    "text": "Love the breakdown",
                                    "create_time": 1710000000,
                                    "digg_count": 7,
                                    "reply_comment_total": 1,
                                    "user": {
                                        "uid": "u1",
                                        "unique_id": "viewer_one",
                                        "nickname": "Viewer One",
                                    },
                                }
                            ],
                        }
                    ),
                    response_headers={"content-type": "application/json"},
                ),
            )
        ]
    )

    paths = write_tiktok_live_batch_probe_outputs(
        creator_handle="funmi",
        creator_profile_url="https://www.tiktok.com/@funmi",
        video_urls=["https://www.tiktok.com/@funmi/video/7390000000000000001"],
        state_label="test-session",
        session_mode=AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
        auth_state_root=auth_root,
        output_dir=tmp_path / "out",
        cadence_min_gap_seconds=0,
        cadence_max_gap_seconds=0,
        random_seed=1,
        engine=engine,
        sleep_fn=lambda _seconds: None,
    )

    grid = json.loads(paths.grid_result_json_path.read_text(encoding="utf-8"))
    cadence = json.loads(paths.cadence_result_json_path.read_text(encoding="utf-8"))
    serialized = json.dumps({"grid": grid, "cadence": cadence}, sort_keys=True)

    assert cadence["attempted_count"] == 1
    assert cadence["completed_count"] == 1
    assert cadence["results"][0]["comment_responses"][0]["url_summary"]["query_key_count"] == 3
    assert "https://www.tiktok.com/api/comment/list/" not in serialized
    assert '"body_text"' not in serialized
    assert str(auth_root) not in serialized
    assert str(engine.calls[0]["storage_state_path"]) not in serialized
    assert engine.calls[0]["headless"] is False
    assert engine.calls[0]["post_load_action_script"]
    assert engine.calls[0]["response_predicate_matches_comment_list"] is True

    code, message = write_tiktok_batch_packet(
        creator_handle="funmi",
        creator_profile_url="https://www.tiktok.com/@funmi",
        batch_label="fake-live-probe",
        decision_question="offline fake-engine admission compatibility",
        grid_result_json=paths.grid_result_json_path.read_bytes(),
        cadence_result_jsons=[paths.cadence_result_json_path.read_bytes()],
        output_directory=tmp_path / "packet",
        source_file_receipts=[],
    )
    assert code == 0
    packet_payload = json.loads(
        (Path(message) / "raw" / "01_tiktok_batch_capture.json").read_text(encoding="utf-8")
    )
    assert packet_payload["batch_summary"]["video_count"] == 1
    assert packet_payload["batch_summary"]["captured_comment_count"] == 1
    assert packet_payload["batch_summary"]["subtitle_info_video_count"] == 1
    assert packet_payload["videos"][0]["subtitles"]["posture"] == "source_native_subtitle_not_captured"
    assert packet_payload["videos"][0]["subtitles"]["subtitle_infos"][0]["url_redacted"] is True


def test_live_probe_stops_on_platform_challenge(tmp_path: Path) -> None:
    auth_root = _auth_state(tmp_path)
    engine = _FakeObservationEngine(
        outcomes=[
            BrowserPageObservationSuccess(
                requested_url="https://www.tiktok.com/@funmi/video/7390000000000000001",
                final_url="https://www.tiktok.com/@funmi/video/7390000000000000001",
                title="Verify to continue",
                visible_text="Drag the slider to verify to continue",
                dom_observation={"hydration_json_text": None},
                responses=[],
                metadata={},
                warning_notes=[],
                limitation_notes=[],
            ),
            _success_observation(video_id="7390000000000000002"),
        ]
    )

    paths = write_tiktok_live_batch_probe_outputs(
        creator_handle="funmi",
        creator_profile_url="https://www.tiktok.com/@funmi",
        video_urls=[
            "https://www.tiktok.com/@funmi/video/7390000000000000001",
            "https://www.tiktok.com/@funmi/video/7390000000000000002",
        ],
        state_label="test-session",
        session_mode=AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
        auth_state_root=auth_root,
        output_dir=tmp_path / "out",
        cadence_min_gap_seconds=0,
        cadence_max_gap_seconds=0,
        random_seed=1,
        engine=engine,
        sleep_fn=lambda _seconds: None,
    )

    cadence = json.loads(paths.cadence_result_json_path.read_text(encoding="utf-8"))
    assert cadence["attempted_count"] == 1
    assert cadence["completed_count"] == 0
    assert cadence["challenge_count"] == 1
    assert cadence["failures"][0]["reason"] == "platform_challenge_observed"
    assert len(engine.calls) == 1


def test_live_probe_stops_on_missing_video_detail_hydration(tmp_path: Path) -> None:
    auth_root = _auth_state(tmp_path)
    engine = _FakeObservationEngine(
        outcomes=[
            BrowserPageObservationSuccess(
                requested_url="https://www.tiktok.com/@funmi/video/7390000000000000001",
                final_url="https://www.tiktok.com/@funmi/video/7390000000000000001",
                title="TikTok",
                visible_text="video loaded",
                dom_observation={"hydration_json_text": None},
                responses=[],
                metadata={},
                warning_notes=[],
                limitation_notes=[],
            ),
            _success_observation(video_id="7390000000000000002"),
        ]
    )

    paths = write_tiktok_live_batch_probe_outputs(
        creator_handle="funmi",
        creator_profile_url="https://www.tiktok.com/@funmi",
        video_urls=[
            "https://www.tiktok.com/@funmi/video/7390000000000000001",
            "https://www.tiktok.com/@funmi/video/7390000000000000002",
        ],
        state_label="test-session",
        session_mode=AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
        auth_state_root=auth_root,
        output_dir=tmp_path / "out",
        cadence_min_gap_seconds=0,
        cadence_max_gap_seconds=0,
        random_seed=1,
        engine=engine,
        sleep_fn=lambda _seconds: None,
    )

    cadence = json.loads(paths.cadence_result_json_path.read_text(encoding="utf-8"))
    assert cadence["attempted_count"] == 1
    assert cadence["completed_count"] == 0
    assert cadence["challenge_count"] == 1
    assert cadence["failures"][0]["reason"] == "missing_video_detail_hydration"
    assert len(engine.calls) == 1


def test_live_probe_runner_exposes_no_secret_or_storage_path_flags() -> None:
    forbidden_destinations = {"password", "username", "token", "cookie", "profile"}
    forbidden_options = {
        "--password",
        "--username",
        "--token",
        "--cookie",
        "--profile",
        "--profile-path",
        "--storage-state-path",
    }
    parser = runner.build_parser()
    destinations = {action.dest for action in parser._actions}
    options = {option for action in parser._actions for option in action.option_strings}
    assert destinations.isdisjoint(forbidden_destinations)
    assert options.isdisjoint(forbidden_options)


def test_comment_list_predicate_is_tiktok_path_only() -> None:
    assert is_tiktok_comment_list_url("https://www.tiktok.com/api/comment/list/?cursor=0")
    assert is_tiktok_comment_list_url("https://www.tiktok.com/api/comment/list/?signed=value")
    assert not is_tiktok_comment_list_url("https://www.tiktok.com/api/user/list/?cursor=0")
    assert not is_tiktok_comment_list_url("https://not-tiktok.example.com/api/comment/list/?cursor=0")
    assert not is_tiktok_comment_list_url("https://example.com/api/comment/list/?cursor=0")


def _auth_state(tmp_path: Path) -> Path:
    auth_root = tmp_path / "auth"
    path = auth_state_path_for_label("test-session", auth_state_root=auth_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"cookies": [], "origins": []}), encoding="utf-8")
    write_auth_state_metadata(
        "test-session",
        session_mode=AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
        auth_state_root=auth_root,
    )
    return auth_root


def _success_observation(
    *,
    video_id: str,
    response: BrowserPageResponse | None = None,
) -> BrowserPageObservationSuccess:
    return BrowserPageObservationSuccess(
        requested_url=f"https://www.tiktok.com/@funmi/video/{video_id}",
        final_url=f"https://www.tiktok.com/@funmi/video/{video_id}",
        title="TikTok",
        visible_text="video loaded",
        dom_observation={"hydration_json_text": json.dumps(_hydration(video_id))},
        responses=[response] if response is not None else [],
        metadata={},
        warning_notes=[],
        limitation_notes=[],
    )


def _hydration(video_id: str) -> dict[str, object]:
    return {
        "__DEFAULT_SCOPE__": {
            "webapp.video-detail": {
                "itemInfo": {
                    "itemStruct": {
                        "id": video_id,
                        "desc": "Testing #capture",
                        "createTime": 1710000000,
                        "stats": {
                            "playCount": 1000,
                            "diggCount": 50,
                            "commentCount": 42,
                            "shareCount": 3,
                            "collectCount": 2,
                        },
                        "author": {"uniqueId": "funmi", "nickname": "Funmi"},
                        "music": {"id": "m1", "title": "Original sound", "duration": 12},
                        "video": {
                            "subtitleInfos": [
                                {
                                    "Format": "webvtt",
                                    "LanguageCodeName": "eng-US",
                                    "LanguageID": "2",
                                    "Size": 123,
                                    "Source": "MT",
                                    "Version": "1",
                                    "Url": "https://subtitle.example.invalid/subtitle.webvtt",
                                }
                            ]
                        },
                    }
                }
            }
        }
    }
