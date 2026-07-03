from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from runners import run_source_capture_tiktok_live_batch_probe as runner
from source_capture.adapters.browser_snapshot import (
    BrowserPageObservationSuccess,
    BrowserPagePointerAction,
    BrowserPageResponse,
)
from source_capture.auth_state import (
    AuthenticatedSessionMode,
    auth_state_path_for_label,
    write_auth_state_metadata,
)
from source_capture.tiktok.batch_packet import write_tiktok_batch_packet
from source_capture.tiktok.blocker_triage import (
    TIKTOK_BLOCKER_ACTION_CONTINUE,
    TIKTOK_BLOCKER_ACTION_RELOAD_ONCE_CANDIDATE,
    TIKTOK_BLOCKER_ACTION_STOP,
    TIKTOK_BLOCKER_CLASS_CHALLENGE_OR_SECURITY,
    TIKTOK_BLOCKER_CLASS_INFRASTRUCTURE_RELOAD,
    TIKTOK_BLOCKER_CLASS_NO_BLOCKER,
)
from source_capture.tiktok.live_batch_probe import (
    TIKTOK_CHALLENGE_AFTER_CLOSE_DIAGNOSTIC_REASON,
    TIKTOK_CHALLENGE_AFTER_CLOSE_FOLLOWTHROUGH_REASON,
    TIKTOK_CHALLENGE_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME,
    TIKTOK_CHALLENGE_CLOSE_DIAGNOSTIC_REASON,
    TIKTOK_CHALLENGE_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
    TIKTOK_CHALLENGE_X_CLOSE_NOT_ACCEPTED_REASON,
    TIKTOK_CHALLENGE_VISUAL_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME,
    TIKTOK_CHALLENGE_VISUAL_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
    TIKTOK_COMMENT_ROUTE_NO_RESPONSE_REASON,
    TIKTOK_COMMENT_SURFACE_TOGGLE_POINTER_SEQUENCE_NAME,
    TIKTOK_LOGGED_OUT_SESSION_MODE,
    TIKTOK_DISMISS_BENIGN_OVERLAY_POINTER_ACTION_NAME,
    TIKTOK_OPEN_COMMENTS_POINTER_ACTION_NAME,
    TIKTOK_OPEN_MORE_LIKE_THIS_POINTER_ACTION_NAME,
    TIKTOK_REOPEN_COMMENTS_POINTER_ACTION_NAME,
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
        post_load_pointer_action: BrowserPagePointerAction | None = None,
        post_load_pointer_actions: tuple[BrowserPagePointerAction, ...] = (),
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
                "post_load_pointer_action": post_load_pointer_action,
                "post_load_pointer_actions": post_load_pointer_actions,
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
                    request_method="GET",
                    resource_type="fetch",
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
    assert cadence["results"][0]["comment_responses"][0]["request_method"] == "GET"
    assert cadence["results"][0]["comment_responses"][0]["resource_type"] == "fetch"
    assert "https://www.tiktok.com/api/comment/list/" not in serialized
    assert '"body_text"' not in serialized
    assert str(auth_root) not in serialized
    assert str(engine.calls[0]["storage_state_path"]) not in serialized
    assert cadence["results"][0]["capture_receipt"]["blocker_triage"] == {
        "blocker_class": TIKTOK_BLOCKER_CLASS_NO_BLOCKER,
        "action": TIKTOK_BLOCKER_ACTION_CONTINUE,
        "reason": "no_blocker_markers_observed",
        "challenge_marker_seen": False,
        "dismiss_candidate_count": 0,
        "reload_candidate_count": 0,
        "hydration_present": True,
        "item_struct_present": True,
        "action_mode": "classification_only",
        "action_taken": False,
    }
    receipt = cadence["results"][0]["capture_receipt"]
    assert receipt["benign_overlay_action"] == _benign_overlay_action_receipt()
    assert receipt["comment_action"] == {
        "sequence_name": TIKTOK_COMMENT_SURFACE_TOGGLE_POINTER_SEQUENCE_NAME,
        "action_count": 3,
        "action_sequence": _pointer_action_sequence_receipt(),
        "clicked_all_targets": True,
    }
    assert engine.calls[0]["headless"] is False
    assert engine.calls[0]["post_load_action_script"] is None
    assert engine.calls[0]["post_load_pointer_action"] is None
    pointer_actions = engine.calls[0]["post_load_pointer_actions"]
    assert isinstance(pointer_actions, tuple)
    assert [action.action_name for action in pointer_actions] == [
        TIKTOK_DISMISS_BENIGN_OVERLAY_POINTER_ACTION_NAME,
        TIKTOK_OPEN_COMMENTS_POINTER_ACTION_NAME,
        TIKTOK_OPEN_MORE_LIKE_THIS_POINTER_ACTION_NAME,
        TIKTOK_REOPEN_COMMENTS_POINTER_ACTION_NAME,
    ]
    assert pointer_actions[0].text_markers == (
        "got it",
        "not now",
        "continue in browser",
        "maybe later",
    )
    assert "browse your feed" in pointer_actions[0].page_text_markers
    assert pointer_actions[1].candidate_selector == (
        '[data-e2e="comment-icon"],[data-e2e*="comment"],button,[role="button"],a'
    )
    assert pointer_actions[1].text_markers == ("comment", "comments")
    assert pointer_actions[1].move_steps_min == 6
    assert pointer_actions[1].move_steps_max == 12
    assert pointer_actions[2].text_markers == (
        "more like this",
        "more-like-this",
        "more_like_this",
    )
    assert pointer_actions[3].wait_after_ms == 3500
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


def test_live_probe_logged_out_mode_uses_no_storage_state_and_admits(
    tmp_path: Path,
) -> None:
    video_id = "7390000000000000001"
    engine = _FakeObservationEngine(
        outcomes=[
            _success_observation(
                video_id=video_id,
                responses=[
                    _comment_response(video_id=video_id, cid="7291"),
                    _comment_response(video_id=video_id, cid="7292"),
                ],
            )
        ]
    )

    paths = write_tiktok_live_batch_probe_outputs(
        creator_handle="funmi",
        creator_profile_url="https://www.tiktok.com/@funmi",
        video_urls=["https://www.tiktok.com/@funmi/video/7390000000000000001"],
        logged_out=True,
        output_dir=tmp_path / "out",
        cadence_min_gap_seconds=0,
        cadence_max_gap_seconds=0,
        random_seed=1,
        engine=engine,
        sleep_fn=lambda _seconds: None,
    )

    assert engine.calls[0]["storage_state_path"] is None
    grid = json.loads(paths.grid_result_json_path.read_text(encoding="utf-8"))
    cadence = json.loads(paths.cadence_result_json_path.read_text(encoding="utf-8"))
    assert cadence["completed_count"] == 1
    assert cadence["capture_contract"]["session_mode"] == TIKTOK_LOGGED_OUT_SESSION_MODE
    assert cadence["capture_contract"]["logged_out_public"] is True
    row = cadence["results"][0]
    assert row["capture_receipt"]["matched_comment_response_count"] == 2
    assert row["capture_receipt"]["admitted_comment_response_count"] == 1
    assert row["capture_receipt"]["comment_response_cap"] == 1
    assert len(row["comment_responses"]) == 1
    assert grid["capture_contract"]["logged_out_public"] is True

    code, message = write_tiktok_batch_packet(
        creator_handle="funmi",
        creator_profile_url="https://www.tiktok.com/@funmi",
        batch_label="fake-logged-out-probe",
        decision_question="offline fake-engine logged-out admission compatibility",
        grid_result_json=paths.grid_result_json_path.read_bytes(),
        cadence_result_jsons=[paths.cadence_result_json_path.read_bytes()],
        output_directory=tmp_path / "packet",
        source_file_receipts=[],
    )
    assert code == 0
    packet_payload = json.loads(
        (Path(message) / "raw" / "01_tiktok_batch_capture.json").read_text(encoding="utf-8")
    )
    assert packet_payload["batch_summary"]["captured_comment_count"] == 1


def test_live_probe_runner_rejects_logged_out_with_session_args(tmp_path: Path) -> None:
    try:
        runner.main(
            [
                "--creator-handle",
                "funmi",
                "--creator-profile-url",
                "https://www.tiktok.com/@funmi",
                "--video-url",
                "https://www.tiktok.com/@funmi/video/7390000000000000001",
                "--logged-out",
                "--state-label",
                "test-session",
                "--session-mode",
                AuthenticatedSessionMode.FREE_ACCOUNT_CREATED.value,
                "--output-dir",
                str(tmp_path / "out"),
            ]
        )
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("logged-out mode accepted sessioned auth arguments")


def test_live_probe_runner_rejects_diagnostic_and_followthrough_together(tmp_path: Path) -> None:
    try:
        runner.main(
            [
                "--creator-handle",
                "funmi",
                "--creator-profile-url",
                "https://www.tiktok.com/@funmi",
                "--video-url",
                "https://www.tiktok.com/@funmi/video/7390000000000000001",
                "--logged-out",
                "--allow-challenge-close-diagnostic",
                "--allow-challenge-close-followthrough",
                "--output-dir",
                str(tmp_path / "out"),
            ]
        )
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("diagnostic and followthrough modes were accepted together")

def test_live_probe_filters_non_get_comment_list_responses_when_method_available(
    tmp_path: Path,
) -> None:
    auth_root = _auth_state(tmp_path)
    response_url = (
        "https://www.tiktok.com/api/comment/list/"
        "?aweme_id=7390000000000000001&cursor=0&count=20"
    )
    get_body = json.dumps(
        {
            "cursor": 20,
            "has_more": 0,
            "total": 1,
            "comments": [
                {
                    "cid": "7291",
                    "text": "Real body",
                    "create_time": 1710000000,
                    "user": {"uid": "u1", "unique_id": "viewer_one"},
                }
            ],
        }
    )
    engine = _FakeObservationEngine(
        outcomes=[
            _success_observation(
                video_id="7390000000000000001",
                responses=[
                    BrowserPageResponse(
                        requested_url=response_url,
                        final_url=response_url,
                        status=200,
                        ok=True,
                        body_text="",
                        response_headers={"content-type": "application/json"},
                        request_method="OPTIONS",
                        resource_type="fetch",
                    ),
                    BrowserPageResponse(
                        requested_url=response_url,
                        final_url=response_url,
                        status=200,
                        ok=True,
                        body_text=get_body,
                        response_headers={"content-type": "application/json"},
                        request_method="GET",
                        resource_type="fetch",
                    ),
                ],
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

    cadence = json.loads(paths.cadence_result_json_path.read_text(encoding="utf-8"))
    row = cadence["results"][0]
    assert row["capture_receipt"]["response_count"] == 2
    assert row["capture_receipt"]["matched_comment_response_count"] == 1
    assert row["capture_receipt"]["admitted_comment_response_count"] == 1
    assert len(row["comment_responses"]) == 1
    assert row["comment_responses"][0]["request_method"] == "GET"
    assert row["comment_responses"][0]["body_assessment"]["json_parse_ok"] is True
    assert row["comment_responses"][0]["body_assessment"]["comment_count"] == 1

def test_live_probe_caps_admitted_comment_list_responses(tmp_path: Path) -> None:
    auth_root = _auth_state(tmp_path)
    response_url = (
        "https://www.tiktok.com/api/comment/list/"
        "?aweme_id=7390000000000000001&cursor=0&count=20"
    )
    responses = [
        BrowserPageResponse(
            requested_url=response_url,
            final_url=response_url,
            status=200,
            ok=True,
            body_text=json.dumps(
                {
                    "cursor": index * 20,
                    "has_more": 1,
                    "total": 3,
                    "comments": [
                        {
                            "cid": f"729{index}",
                            "text": f"Body {index}",
                            "create_time": 1710000000 + index,
                            "user": {"uid": f"u{index}", "unique_id": f"viewer_{index}"},
                        }
                    ],
                }
            ),
            response_headers={"content-type": "application/json"},
            request_method="GET",
            resource_type="fetch",
        )
        for index in range(3)
    ]
    engine = _FakeObservationEngine(
        outcomes=[_success_observation(video_id="7390000000000000001", responses=responses)]
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

    cadence = json.loads(paths.cadence_result_json_path.read_text(encoding="utf-8"))
    row = cadence["results"][0]
    assert row["capture_receipt"]["response_count"] == 3
    assert row["capture_receipt"]["matched_comment_response_count"] == 3
    assert row["capture_receipt"]["admitted_comment_response_count"] == 2
    assert row["capture_receipt"]["comment_response_cap"] == 2
    assert len(row["comment_responses"]) == 2
    assert [
        response["body_assessment"]["comments"][0]["cid"]
        for response in row["comment_responses"]
    ] == ["7290", "7291"]



def test_live_probe_challenge_close_diagnostic_flag_prepends_close_action(
    tmp_path: Path,
) -> None:
    auth_root = _auth_state(tmp_path)
    engine = _FakeObservationEngine(
        outcomes=[
            _success_observation(
                video_id="7390000000000000001",
                response=_comment_response(video_id="7390000000000000001"),
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
        allow_challenge_close_diagnostic=True,
        engine=engine,
        sleep_fn=lambda _seconds: None,
    )

    cadence = json.loads(paths.cadence_result_json_path.read_text(encoding="utf-8"))
    pointer_actions = engine.calls[0]["post_load_pointer_actions"]
    assert [action.action_name for action in pointer_actions] == [
        TIKTOK_DISMISS_BENIGN_OVERLAY_POINTER_ACTION_NAME,
        TIKTOK_CHALLENGE_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME,
        TIKTOK_OPEN_COMMENTS_POINTER_ACTION_NAME,
        TIKTOK_OPEN_MORE_LIKE_THIS_POINTER_ACTION_NAME,
        TIKTOK_REOPEN_COMMENTS_POINTER_ACTION_NAME,
        TIKTOK_CHALLENGE_VISUAL_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME,
    ]
    close_action = pointer_actions[1]
    assert close_action.page_text_markers == (
        "drag the slider",
        "verify to continue",
        "captcha",
        "security check",
    )
    assert close_action.exact_text_markers == ("x", "×")
    assert close_action.prefer_top_right is True
    assert close_action.visual_top_right_x_fallback is True
    visual_close_action = pointer_actions[5]
    assert visual_close_action.action_name == (
        TIKTOK_CHALLENGE_VISUAL_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME
    )
    assert visual_close_action.page_text_markers == (
        "drag the slider",
        "verify to continue",
        "captcha",
        "security check",
    )
    assert visual_close_action.visual_top_right_x_fallback is True
    assert cadence["capture_contract"]["challenge_close_diagnostic_allowed"] is True
    assert cadence["capture_contract"]["challenge_close_counts_as_success"] is False
    assert cadence["completed_count"] == 1
    receipt = cadence["results"][0]["capture_receipt"]
    assert receipt["benign_overlay_action"]["action_name"] == (
        TIKTOK_DISMISS_BENIGN_OVERLAY_POINTER_ACTION_NAME
    )
    assert receipt["comment_action"]["action_count"] == 3


def test_live_probe_challenge_close_followthrough_admits_post_close_comments(
    tmp_path: Path,
) -> None:
    auth_root = _auth_state(tmp_path)
    followthrough_close_receipt = _pointer_action_receipt(
        action_name=TIKTOK_CHALLENGE_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
        wait_ms=2000,
        selection_strategy="top_right_visual_x",
    )
    followthrough_close_receipt.update(
        {
            "target_kind": "visual_x",
            "visual_fallback_attempted": True,
            "visual_fallback_target_found": True,
            "visual_fallback_candidate_count": 1,
            "visual_fallback_confidence": 0.812,
            "visual_fallback_screenshot_sha256": "b" * 64,
            "visual_fallback_crop_box": {"x": 576, "y": 0, "width": 704, "height": 324},
            "target_box": {"x": 796.0, "y": 190.0, "width": 16.0, "height": 16.0},
            "click_point": {"x": 803.3, "y": 197.4},
            "post_click_absence_checked": True,
            "post_click_absence_marker_count": 4,
            "post_click_absence_verified": True,
            "post_click_visual_check_attempted": True,
            "post_click_visual_target_found": False,
            "post_click_visual_target_absent": True,
            "post_click_visual_candidate_count": 0,
            "post_click_visual_screenshot_sha256": "c" * 64,
        }
    )
    visual_followthrough_receipt = _pointer_action_receipt(
        action_name=TIKTOK_CHALLENGE_VISUAL_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
        wait_ms=2000,
        selection_strategy="top_right_visual_x",
    )
    visual_followthrough_receipt.update(
        {
            "candidate_count": 0,
            "matched_count": 0,
            "target_found": False,
            "clicked": False,
            "move_steps": None,
            "target_kind": "visual_x",
            "visual_fallback_attempted": True,
            "visual_fallback_target_found": False,
            "visual_fallback_candidate_count": 0,
        }
    )
    pointer_sequence = [
        _benign_overlay_action_receipt(),
        followthrough_close_receipt,
        visual_followthrough_receipt,
        *_pointer_action_sequence_receipt(),
    ]
    engine = _FakeObservationEngine(
        outcomes=[
            _success_observation(
                video_id="7390000000000000001",
                response=_comment_response(video_id="7390000000000000001"),
                pointer_sequence=pointer_sequence,
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
        allow_challenge_close_followthrough=True,
        engine=engine,
        sleep_fn=lambda _seconds: None,
    )

    pointer_actions = engine.calls[0]["post_load_pointer_actions"]
    assert [action.action_name for action in pointer_actions] == [
        TIKTOK_DISMISS_BENIGN_OVERLAY_POINTER_ACTION_NAME,
        TIKTOK_CHALLENGE_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
        TIKTOK_CHALLENGE_VISUAL_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
        TIKTOK_OPEN_COMMENTS_POINTER_ACTION_NAME,
        TIKTOK_OPEN_MORE_LIKE_THIS_POINTER_ACTION_NAME,
        TIKTOK_REOPEN_COMMENTS_POINTER_ACTION_NAME,
    ]
    assert pointer_actions[1].page_text_markers == (
        "drag the slider",
        "verify to continue",
        "captcha",
        "security check",
    )
    assert pointer_actions[2].page_text_markers == ()
    assert pointer_actions[2].visual_top_right_x_fallback is True
    assert pointer_actions[2].stop_sequence_on_failed_post_click_verification is True
    cadence = json.loads(paths.cadence_result_json_path.read_text(encoding="utf-8"))
    assert cadence["attempted_count"] == 1
    assert cadence["completed_count"] == 1
    assert cadence["challenge_count"] == 0
    assert cadence["challenge_close_followthrough_count"] == 1
    assert cadence["capture_contract"]["challenge_close_diagnostic_allowed"] is False
    assert cadence["capture_contract"]["challenge_close_followthrough_allowed"] is True
    row = cadence["results"][0]
    receipt = row["capture_receipt"]
    assert receipt["challenge_close_followthrough"] is True
    assert receipt["challenge_close_accepted"] is True
    assert receipt["challenge_close_action"]["action_name"] == (
        TIKTOK_CHALLENGE_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME
    )
    assert receipt["challenge_close_action"]["target_box"]["x"] == 796.0
    assert receipt["challenge_close_action"]["click_point"] == {"x": 803.3, "y": 197.4}
    assert receipt["admitted_comment_response_count"] == 1
    assert len(row["comment_responses"]) == 1

    code, message = write_tiktok_batch_packet(
        creator_handle="funmi",
        creator_profile_url="https://www.tiktok.com/@funmi",
        batch_label="fake-followthrough-probe",
        decision_question="offline fake-engine followthrough admission compatibility",
        grid_result_json=paths.grid_result_json_path.read_bytes(),
        cadence_result_jsons=[paths.cadence_result_json_path.read_bytes()],
        output_directory=tmp_path / "packet",
        source_file_receipts=[],
    )
    assert code == 0
    packet_payload = json.loads(
        (Path(message) / "raw" / "01_tiktok_batch_capture.json").read_text(encoding="utf-8")
    )
    assert packet_payload["batch_summary"]["challenge_close_followthrough_video_count"] == 1
    intervention = packet_payload["videos"][0]["source_access_intervention"]
    assert intervention["posture"] == "owner_authorized_challenge_x_close_followthrough"
    assert intervention["followthrough"] is True
    assert intervention["accepted"] is True
    assert intervention["clicked"] is True
    assert intervention["post_click_absence_verified"] is True
    assert intervention["post_click_visual_target_absent"] is True


def test_live_probe_challenge_close_followthrough_stops_if_close_not_accepted(
    tmp_path: Path,
) -> None:
    auth_root = _auth_state(tmp_path)
    followthrough_close_receipt = _pointer_action_receipt(
        action_name=TIKTOK_CHALLENGE_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
        wait_ms=2000,
        selection_strategy="center_modal_visual_x",
    )
    followthrough_close_receipt.update(
        {
            "target_kind": "visual_x",
            "post_click_absence_checked": True,
            "post_click_absence_marker_count": 4,
            "post_click_absence_verified": True,
            "post_click_visual_check_attempted": True,
            "post_click_visual_target_found": False,
            "post_click_visual_target_absent": False,
            "post_click_visual_candidate_count": 4,
            "post_click_visual_screenshot_sha256": "d" * 64,
        }
    )
    pointer_sequence = [
        _benign_overlay_action_receipt(),
        followthrough_close_receipt,
        *_pointer_action_sequence_receipt(),
    ]
    engine = _FakeObservationEngine(
        outcomes=[
            _success_observation(
                video_id="7390000000000000001",
                response=_comment_response(video_id="7390000000000000001"),
                pointer_sequence=pointer_sequence,
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
        allow_challenge_close_followthrough=True,
        engine=engine,
        sleep_fn=lambda _seconds: None,
    )

    cadence = json.loads(paths.cadence_result_json_path.read_text(encoding="utf-8"))
    assert cadence["attempted_count"] == 1
    assert cadence["completed_count"] == 0
    assert cadence["challenge_count"] == 1
    assert cadence["challenge_close_followthrough_count"] == 0
    assert cadence["results"] == []
    failure = cadence["failures"][0]
    assert failure["reason"] == TIKTOK_CHALLENGE_X_CLOSE_NOT_ACCEPTED_REASON
    triage = failure["blocker_triage"]
    assert triage["challenge_close_action"]["clicked"] is True
    assert triage["challenge_close_action"]["post_click_absence_verified"] is True
    assert triage["challenge_close_action"]["post_click_visual_candidate_count"] == 4
    assert triage["challenge_close_action"]["post_click_visual_target_absent"] is False
    assert triage["challenge_close_accepted"] is False
    assert triage["matched_comment_response_count"] == 1
    assert triage["admitted_comment_response_count"] == 0
    assert triage["dom_visible_comment_candidate_count"] == 0



def test_live_probe_failed_close_without_comment_actions_has_no_comment_action_label(
    tmp_path: Path,
) -> None:
    auth_root = _auth_state(tmp_path)
    followthrough_close_receipt = _pointer_action_receipt(
        action_name=TIKTOK_CHALLENGE_VISUAL_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
        wait_ms=2000,
        selection_strategy="center_modal_visual_x",
    )
    followthrough_close_receipt.update(
        {
            "target_kind": "visual_x",
            "post_click_absence_checked": True,
            "post_click_absence_marker_count": 4,
            "post_click_absence_verified": True,
            "post_click_visual_check_attempted": True,
            "post_click_visual_target_found": False,
            "post_click_visual_target_absent": False,
            "post_click_visual_candidate_count": 3,
        }
    )
    engine = _FakeObservationEngine(
        outcomes=[
            _success_observation(
                video_id="7390000000000000001",
                pointer_sequence=[_benign_overlay_action_receipt(), followthrough_close_receipt],
                dom_comment_candidates=[],
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
        allow_challenge_close_followthrough=True,
        engine=engine,
        sleep_fn=lambda _seconds: None,
    )

    cadence = json.loads(paths.cadence_result_json_path.read_text(encoding="utf-8"))
    assert cadence["attempted_count"] == 1
    assert cadence["completed_count"] == 0
    assert cadence["challenge_count"] == 1
    failure = cadence["failures"][0]
    assert failure["reason"] == TIKTOK_CHALLENGE_X_CLOSE_NOT_ACCEPTED_REASON
    triage = failure["blocker_triage"]
    assert triage["challenge_close_action"]["clicked"] is True
    assert triage["challenge_close_accepted"] is False
    assert "challenge_close_followthrough" not in triage
    assert "comment_action" not in triage
    assert triage["matched_comment_response_count"] == 0
    assert triage["admitted_comment_response_count"] == 0
    assert triage["dom_visible_comment_candidate_count"] == 0

def test_live_probe_challenge_close_followthrough_stops_if_challenge_remains(
    tmp_path: Path,
) -> None:
    auth_root = _auth_state(tmp_path)
    followthrough_close_receipt = _pointer_action_receipt(
        action_name=TIKTOK_CHALLENGE_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME,
        wait_ms=2000,
        selection_strategy="top_right_visual_x",
    )
    followthrough_close_receipt.update(
        {
            "post_click_absence_checked": True,
            "post_click_absence_marker_count": 4,
            "post_click_absence_verified": True,
            "post_click_visual_check_attempted": True,
            "post_click_visual_target_found": False,
            "post_click_visual_target_absent": False,
            "post_click_visual_candidate_count": 4,
        }
    )
    pointer_sequence = [
        _benign_overlay_action_receipt(),
        followthrough_close_receipt,
        *_pointer_action_sequence_receipt(),
    ]
    engine = _FakeObservationEngine(
        outcomes=[
            _success_observation(
                video_id="7390000000000000001",
                response=_comment_response(video_id="7390000000000000001"),
                pointer_sequence=pointer_sequence,
                visible_text="Drag the slider to fit the puzzle",
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
        allow_challenge_close_followthrough=True,
        engine=engine,
        sleep_fn=lambda _seconds: None,
    )

    cadence = json.loads(paths.cadence_result_json_path.read_text(encoding="utf-8"))
    assert cadence["attempted_count"] == 1
    assert cadence["completed_count"] == 0
    assert cadence["challenge_count"] == 1
    assert cadence["results"] == []
    failure = cadence["failures"][0]
    assert failure["reason"] == TIKTOK_CHALLENGE_AFTER_CLOSE_FOLLOWTHROUGH_REASON
    triage = failure["blocker_triage"]
    assert triage["challenge_close_action"]["action_name"] == (
        TIKTOK_CHALLENGE_CLOSE_FOLLOWTHROUGH_POINTER_ACTION_NAME
    )
    assert "challenge_close_followthrough" not in triage
    assert triage["challenge_close_accepted"] is False
    assert triage["comment_action"]["action_count"] == 3
    assert triage["matched_comment_response_count"] == 1
    assert triage["admitted_comment_response_count"] == 0
    assert triage["dom_visible_comment_candidate_count"] == 0
    assert "challenge_close_diagnostic" not in triage


def test_live_probe_challenge_close_diagnostic_is_not_completion(
    tmp_path: Path,
) -> None:
    auth_root = _auth_state(tmp_path)
    dom_close_receipt = _pointer_action_receipt(
        action_name=TIKTOK_CHALLENGE_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME,
        wait_ms=0,
        page_text_gate_matched=False,
        selection_strategy="top_right",
    )
    dom_close_receipt.update(
        {
            "candidate_count": 0,
            "matched_count": 0,
            "target_found": False,
            "clicked": False,
            "move_steps": None,
        }
    )
    visual_close_receipt = _pointer_action_receipt(
        action_name=TIKTOK_CHALLENGE_VISUAL_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME,
        wait_ms=2000,
        selection_strategy="top_right_visual_x",
    )
    visual_close_receipt.update(
        {
            "candidate_count": 0,
            "matched_count": 0,
            "target_kind": "visual_x",
            "visual_fallback_attempted": True,
            "visual_fallback_target_found": True,
            "visual_fallback_candidate_count": 1,
            "visual_fallback_confidence": 0.812,
            "visual_fallback_screenshot_sha256": "a" * 64,
            "visual_fallback_crop_box": {"x": 576, "y": 0, "width": 704, "height": 324},
        }
    )
    pointer_sequence = [
        _benign_overlay_action_receipt(),
        dom_close_receipt,
        *_pointer_action_sequence_receipt(),
        visual_close_receipt,
    ]
    engine = _FakeObservationEngine(
        outcomes=[
            _success_observation(
                video_id="7390000000000000001",
                response=_comment_response(video_id="7390000000000000001"),
                pointer_sequence=pointer_sequence,
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
        allow_challenge_close_diagnostic=True,
        engine=engine,
        sleep_fn=lambda _seconds: None,
    )

    cadence = json.loads(paths.cadence_result_json_path.read_text(encoding="utf-8"))
    serialized = json.dumps(cadence, sort_keys=True)
    assert cadence["attempted_count"] == 1
    assert cadence["completed_count"] == 0
    assert cadence["challenge_count"] == 1
    assert cadence["results"] == []
    assert "comment_responses" not in serialized
    failure = cadence["failures"][0]
    assert failure["reason"] == TIKTOK_CHALLENGE_CLOSE_DIAGNOSTIC_REASON
    triage = failure["blocker_triage"]
    assert triage["blocker_class"] == "challenge_close_diagnostic"
    assert triage["action"] == "stop"
    assert triage["action_taken"] is True
    assert triage["challenge_close_diagnostic"] == pointer_sequence[-1]
    assert triage["comment_action"]["action_count"] == 3
    assert triage["matched_comment_response_count"] == 1
    assert triage["admitted_comment_response_count"] == 0
    assert triage["dom_visible_comment_candidate_count"] == 0


def test_live_probe_challenge_after_close_diagnostic_keeps_challenge_stop(
    tmp_path: Path,
) -> None:
    auth_root = _auth_state(tmp_path)
    dom_close_receipt = _pointer_action_receipt(
        action_name=TIKTOK_CHALLENGE_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME,
        wait_ms=0,
        page_text_gate_matched=False,
        selection_strategy="top_right",
    )
    dom_close_receipt.update(
        {
            "candidate_count": 0,
            "matched_count": 0,
            "target_found": False,
            "clicked": False,
            "move_steps": None,
        }
    )
    visual_close_receipt = _pointer_action_receipt(
        action_name=TIKTOK_CHALLENGE_VISUAL_CLOSE_DIAGNOSTIC_POINTER_ACTION_NAME,
        wait_ms=2000,
        selection_strategy="top_right_visual_x",
    )
    visual_close_receipt.update(
        {
            "candidate_count": 0,
            "matched_count": 0,
            "target_kind": "visual_x",
            "visual_fallback_attempted": True,
            "visual_fallback_target_found": True,
            "visual_fallback_candidate_count": 1,
            "visual_fallback_confidence": 0.812,
            "visual_fallback_screenshot_sha256": "a" * 64,
            "visual_fallback_crop_box": {"x": 576, "y": 0, "width": 704, "height": 324},
        }
    )
    pointer_sequence = [
        _benign_overlay_action_receipt(),
        dom_close_receipt,
        *_pointer_action_sequence_receipt(),
        visual_close_receipt,
    ]
    engine = _FakeObservationEngine(
        outcomes=[
            _success_observation(
                video_id="7390000000000000001",
                response=_comment_response(video_id="7390000000000000001"),
                pointer_sequence=pointer_sequence,
                visible_text="Drag the slider.",
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
        allow_challenge_close_diagnostic=True,
        engine=engine,
        sleep_fn=lambda _seconds: None,
    )

    cadence = json.loads(paths.cadence_result_json_path.read_text(encoding="utf-8"))
    assert cadence["attempted_count"] == 1
    assert cadence["completed_count"] == 0
    assert cadence["challenge_count"] == 1
    failure = cadence["failures"][0]
    assert failure["reason"] == TIKTOK_CHALLENGE_AFTER_CLOSE_DIAGNOSTIC_REASON
    triage = failure["blocker_triage"]
    assert triage["reason"] == "platform_challenge_observed"
    assert triage["matched_marker"] == "drag the slider"
    assert triage["challenge_close_diagnostic"] == pointer_sequence[-1]
    assert triage["comment_action"]["action_count"] == 3
    assert triage["matched_comment_response_count"] == 1
    assert triage["admitted_comment_response_count"] == 0
    assert triage["dom_visible_comment_candidate_count"] == 0



def test_live_probe_stops_on_zero_comment_list_response(tmp_path: Path) -> None:
    auth_root = _auth_state(tmp_path)
    engine = _FakeObservationEngine(
        outcomes=[
            _success_observation(video_id="7390000000000000001", responses=[]),
            _success_observation(video_id="7390000000000000002", response=_comment_response()),
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
    assert cadence["challenge_count"] == 0
    assert cadence["results"] == []
    assert cadence["failures"][0]["reason"] == TIKTOK_COMMENT_ROUTE_NO_RESPONSE_REASON
    assert cadence["failures"][0]["blocker_triage"] == {
        "blocker_class": "comment_route_zero_yield",
        "action": "stop",
        "reason": TIKTOK_COMMENT_ROUTE_NO_RESPONSE_REASON,
        "action_mode": "diagnosis_only",
        "action_taken": False,
        "benign_overlay_action": _benign_overlay_action_receipt(),
        "comment_action": {
            "sequence_name": TIKTOK_COMMENT_SURFACE_TOGGLE_POINTER_SEQUENCE_NAME,
            "action_count": 3,
            "action_sequence": _pointer_action_sequence_receipt(),
            "clicked_all_targets": True,
        },
        "response_count": 0,
        "matched_comment_response_count": 0,
        "admitted_comment_response_count": 0,
        "dom_visible_comment_candidate_count": 0,
    }
    assert len(engine.calls) == 1


def test_live_probe_completes_with_dom_visible_comment_fallback(tmp_path: Path) -> None:
    auth_root = _auth_state(tmp_path)
    engine = _FakeObservationEngine(
        outcomes=[
            _success_observation(
                video_id="7390000000000000001",
                responses=[],
                dom_comment_candidates=[
                    {
                        "text": "What perfume is this?",
                        "selector": '[data-e2e*="comment"]',
                    }
                ],
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

    cadence = json.loads(paths.cadence_result_json_path.read_text(encoding="utf-8"))
    assert cadence["attempted_count"] == 1
    assert cadence["completed_count"] == 1
    assert cadence["challenge_count"] == 0
    assert cadence["failures"] == []
    row = cadence["results"][0]
    assert row["comment_responses"] == []
    assert row["dom_visible_comment_candidates"][0]["text"] == "What perfume is this?"
    receipt = row["capture_receipt"]
    assert receipt["admitted_comment_response_count"] == 0
    assert receipt["dom_visible_comment_candidate_count"] == 1
    assert receipt["comment_capture_fallback"] == "dom_visible_comment_candidates_v0"


def test_live_probe_rejects_dom_visible_count_badge_as_comment_fallback(
    tmp_path: Path,
) -> None:
    auth_root = _auth_state(tmp_path)
    engine = _FakeObservationEngine(
        outcomes=[
            _success_observation(
                video_id="7390000000000000001",
                responses=[],
                dom_comment_candidates=[
                    {
                        "text": "303",
                        "selector": '[data-e2e*="comment"]',
                    },
                    {
                        "text": "1.2K comments",
                        "selector": '[data-e2e*="comment"]',
                    },
                ],
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

    cadence = json.loads(paths.cadence_result_json_path.read_text(encoding="utf-8"))
    assert cadence["attempted_count"] == 1
    assert cadence["completed_count"] == 0
    assert cadence["challenge_count"] == 0
    assert cadence["results"] == []
    failure = cadence["failures"][0]
    assert failure["reason"] == TIKTOK_COMMENT_ROUTE_NO_RESPONSE_REASON
    triage = failure["blocker_triage"]
    assert triage["dom_visible_comment_candidate_count"] == 0
    assert triage["matched_comment_response_count"] == 0

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
                metadata={"post_load_pointer_action": _pointer_action_receipt()},
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
    assert cadence["failures"][0]["blocker_triage"]["blocker_class"] == (
        TIKTOK_BLOCKER_CLASS_CHALLENGE_OR_SECURITY
    )
    assert cadence["failures"][0]["blocker_triage"]["action"] == TIKTOK_BLOCKER_ACTION_STOP
    assert cadence["failures"][0]["blocker_triage"]["action_taken"] is False
    assert cadence["failures"][0]["blocker_triage"]["matched_marker"] == "verify to continue"
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
                metadata={"post_load_pointer_action": _pointer_action_receipt()},
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
    assert cadence["failures"][0]["blocker_triage"]["blocker_class"] == (
        TIKTOK_BLOCKER_CLASS_INFRASTRUCTURE_RELOAD
    )
    assert cadence["failures"][0]["blocker_triage"]["action"] == (
        TIKTOK_BLOCKER_ACTION_RELOAD_ONCE_CANDIDATE
    )
    assert cadence["failures"][0]["blocker_triage"]["action_taken"] is False
    assert len(engine.calls) == 1


def test_live_probe_does_not_stop_on_close_text_without_blocker_candidate(
    tmp_path: Path,
) -> None:
    auth_root = _auth_state(tmp_path)
    engine = _FakeObservationEngine(
        outcomes=[
            BrowserPageObservationSuccess(
                requested_url="https://www.tiktok.com/@funmi/video/7390000000000000001",
                final_url="https://www.tiktok.com/@funmi/video/7390000000000000001",
                title="TikTok",
                visible_text="Close",
                dom_observation={
                    "hydration_json_text": json.dumps(_hydration("7390000000000000001"))
                },
                responses=[_comment_response()],
                metadata={"post_load_pointer_action": _pointer_action_receipt()},
                warning_notes=[],
                limitation_notes=[],
            ),
            _success_observation(video_id="7390000000000000002", response=_comment_response()),
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
    assert cadence["attempted_count"] == 2
    assert cadence["completed_count"] == 2
    assert cadence["challenge_count"] == 0
    assert cadence["failures"] == []
    first_triage = cadence["results"][0]["capture_receipt"]["blocker_triage"]
    assert first_triage["blocker_class"] == TIKTOK_BLOCKER_CLASS_NO_BLOCKER
    assert first_triage["action"] == TIKTOK_BLOCKER_ACTION_CONTINUE
    assert "Close" not in json.dumps(cadence)
    assert len(engine.calls) == 2

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


def _comment_response(
    *,
    video_id: str = "7390000000000000001",
    cid: str = "7291",
) -> BrowserPageResponse:
    response_url = (
        "https://www.tiktok.com/api/comment/list/"
        f"?aweme_id={video_id}&cursor=0&count=20"
    )
    return BrowserPageResponse(
        requested_url=response_url,
        final_url=response_url,
        status=200,
        ok=True,
        body_text=json.dumps(
            {
                "cursor": 20,
                "has_more": 0,
                "total": 1,
                "comments": [
                    {
                        "cid": cid,
                        "text": "Route proof",
                        "create_time": 1710000000,
                        "digg_count": 1,
                        "reply_comment_total": 0,
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
        request_method="GET",
        resource_type="fetch",
    )

def _success_observation(
    *,
    video_id: str,
    response: BrowserPageResponse | None = None,
    responses: list[BrowserPageResponse] | None = None,
    pointer_sequence: list[dict[str, object]] | None = None,
    visible_text: str = "video loaded",
    dom_comment_candidates: list[dict[str, object]] | None = None,
) -> BrowserPageObservationSuccess:
    pointer_sequence = pointer_sequence or _live_pointer_action_sequence_receipt()
    dom_observation: dict[str, object] = {"hydration_json_text": json.dumps(_hydration(video_id))}
    if dom_comment_candidates is not None:
        dom_observation["visible_comment_candidates"] = dom_comment_candidates
    return BrowserPageObservationSuccess(
        requested_url=f"https://www.tiktok.com/@funmi/video/{video_id}",
        final_url=f"https://www.tiktok.com/@funmi/video/{video_id}",
        title="TikTok",
        visible_text=visible_text,
        dom_observation=dom_observation,
        responses=responses if responses is not None else ([response] if response is not None else []),
        metadata={
            "post_load_pointer_action": pointer_sequence[-1],
            "post_load_pointer_actions": pointer_sequence,
        },
        warning_notes=[],
        limitation_notes=[],
    )


def _live_pointer_action_sequence_receipt() -> list[dict[str, object]]:
    return [_benign_overlay_action_receipt(), *_pointer_action_sequence_receipt()]


def _benign_overlay_action_receipt() -> dict[str, object]:
    return _pointer_action_receipt(
        action_name=TIKTOK_DISMISS_BENIGN_OVERLAY_POINTER_ACTION_NAME,
        wait_ms=1500,
        page_text_gate_matched=True,
        selection_strategy="first_match",
    )


def _pointer_action_sequence_receipt() -> list[dict[str, object]]:
    return [
        _pointer_action_receipt(
            action_name=TIKTOK_OPEN_COMMENTS_POINTER_ACTION_NAME,
            wait_ms=2000,
        ),
        _pointer_action_receipt(
            action_name=TIKTOK_OPEN_MORE_LIKE_THIS_POINTER_ACTION_NAME,
            wait_ms=2000,
        ),
        _pointer_action_receipt(
            action_name=TIKTOK_REOPEN_COMMENTS_POINTER_ACTION_NAME,
            wait_ms=3500,
        ),
    ]


def _pointer_action_receipt(
    *,
    action_name: str = TIKTOK_OPEN_COMMENTS_POINTER_ACTION_NAME,
    wait_ms: int = 2500,
    page_text_gate_matched: bool | None = None,
    selection_strategy: str | None = None,
) -> dict[str, object]:
    receipt: dict[str, object | None] = {
        "action_name": action_name,
        "candidate_count": 5,
        "matched_count": 1,
        "target_found": True,
        "clicked": True,
        "move_steps": 7,
        "wait_ms": wait_ms,
        "target_kind": "button",
        "page_text_gate_matched": page_text_gate_matched,
        "selection_strategy": selection_strategy,
    }
    return {key: value for key, value in receipt.items() if value is not None}


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
