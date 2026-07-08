from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from runners import run_source_capture_ig_daily_heartbeat as heartbeat


def _write_json(path: Path, payload: object) -> Path:
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_manifest(packet_dir: Path, *, packet_id: str = "packet_001") -> None:
    packet_dir.mkdir(parents=True, exist_ok=True)
    (packet_dir / "manifest.json").write_text(
        json.dumps(
            {
                "packet_id": packet_id,
                "source_surface": "ig_reels_grid_dom_passive_json",
                "source_slices": [
                    {"slice_id": "ig_reels_profile_00", "metric_observations": []},
                    {
                        "slice_id": "ig_reels_grid_01",
                        "metric_observations": [
                            {"metric": "view_count", "posture": "observed", "value": 1200},
                            {"metric": "like_count", "posture": "unknown", "value": None},
                        ],
                    },
                    {
                        "slice_id": "ig_reels_grid_02",
                        "metric_observations": [
                            {"metric": "view_count", "posture": "observed", "value": 900}
                        ],
                    },
                ],
                "warnings": ["packet_warning"],
                "limitations": ["packet_limitation"],
            }
        ),
        encoding="utf-8",
    )


def test_heartbeat_filters_active_roster_by_stable_lane_and_writes_receipts(tmp_path: Path) -> None:
    roster_path = _write_json(
        tmp_path / "roster.json",
        {
            "roster_snapshot_id": "ig_roster_snapshot_test",
            "creators": [
                {
                    "platform": "instagram",
                    "handle": "hyram",
                    "platform_account_id": "acct_hyram",
                    "status": "active",
                },
                {
                    "platform": "instagram",
                    "handle": "jeremyfragrance",
                    "ig_roster_record_id": "ig_roster_jeremy",
                    "status": "active",
                },
                {
                    "platform": "instagram",
                    "handle": "milanscents",
                    "platform_account_id": "acct_milan",
                    "status": "paused",
                },
                {
                    "platform": "youtube",
                    "handle": "not_ig",
                    "platform_account_id": "acct_yt",
                    "status": "active",
                },
            ],
        },
    )
    active_keys = {
        "hyram": "platform_account_id:acct_hyram",
        "jeremyfragrance": "ig_roster_record_id:ig_roster_jeremy",
    }
    lane_id = heartbeat.assign_lane_id(active_keys["hyram"], 2)
    expected_handles = [
        handle
        for handle, key in active_keys.items()
        if heartbeat.assign_lane_id(key, 2) == lane_id
    ]
    calls: list[dict[str, object]] = []

    def fake_grid_runner(**kwargs: object) -> tuple[int, str]:
        calls.append(dict(kwargs))
        packet_dir = Path(kwargs["output_directory"])
        _write_manifest(packet_dir, packet_id=f"packet_{len(calls):03d}")
        return 0, str(packet_dir)

    result = heartbeat.run_ig_daily_heartbeat(
        roster_path=roster_path,
        receipt_jsonl=tmp_path / "receipts.jsonl",
        lane_id=lane_id,
        lane_count=2,
        output_root=tmp_path / "packets",
        grid_runner=fake_grid_runner,
    )

    assert result.exit_code == 0
    assert [call["handle"] for call in calls] == expected_handles
    receipts = _read_jsonl(Path(result.message()))
    assert [receipt["creator"]["handle"] for receipt in receipts] == expected_handles
    for receipt in receipts:
        assert receipt["schema_version"] == "ig_daily_heartbeat_receipt_v0"
        assert receipt["status"] == "succeeded"
        assert receipt["grid_scope"] == "first_visible_grid_only"
        assert receipt["pagination_attempted"] is False
        assert receipt["scroll_expansion_attempted"] is False
        assert receipt["platform_write_actions_attempted"] is False
        assert receipt["deep_capture_selection"] == "no_candidate"
        assert receipt["asset_policy"] == "heavy_assets_blocked_bandwidth_mode"
        assert receipt["headless"] is True
        assert receipt["row_counts"] == {"grid_media_slices": 2}
        assert receipt["metric_observation_counts"] == {"view_count": 2}
        assert "like_count" not in receipt["metric_observation_counts"]

    assert all(call["data_root"] is None for call in calls)
    assert all(call["block_heavy_assets"] is True for call in calls)


def test_heartbeat_records_access_gap_without_fake_packet(tmp_path: Path) -> None:
    roster_path = _write_json(
        tmp_path / "roster.json",
        {
            "roster_snapshot_id": "ig_roster_snapshot_access_gap",
            "creators": [
                {
                    "platform": "instagram",
                    "handle": "hyram",
                    "platform_account_id": "acct_hyram",
                    "status": "active",
                }
            ],
        },
    )

    def fake_grid_runner(**_kwargs: object) -> tuple[int, str]:
        return 5, "profile access-blocked (challenge_route); no packet written"

    result = heartbeat.run_ig_daily_heartbeat(
        roster_path=roster_path,
        receipt_jsonl=tmp_path / "receipts.jsonl",
        lane_id="lane_1",
        lane_count=1,
        output_root=tmp_path / "packets",
        grid_runner=fake_grid_runner,
    )

    receipts = _read_jsonl(Path(result.message()))
    assert len(receipts) == 1
    receipt = receipts[0]
    assert receipt["status"] == "access_gap"
    assert receipt["packet_pointer"] is None
    assert receipt["access_gap_reason"] == "challenge_route"
    assert not (tmp_path / "packets").exists()


def test_heartbeat_validates_external_breakout_tags_only(tmp_path: Path) -> None:
    roster_path = _write_json(
        tmp_path / "roster.json",
        {
            "roster_snapshot_id": "ig_roster_snapshot_breakout",
            "creators": [
                {
                    "platform": "instagram",
                    "handle": "hyram",
                    "platform_account_id": "acct_hyram",
                    "status": "active",
                }
            ],
        },
    )
    bad_tags = _write_json(
        tmp_path / "bad_breakouts.json",
        [{"platform": "instagram", "handle": "hyram", "tag": "top_band", "shortcode": "ABC"}],
    )

    def should_not_run(**_kwargs: object) -> tuple[int, str]:
        raise AssertionError("grid runner should not run when breakout input is invalid")

    with pytest.raises(ValueError, match="unsupported tag"):
        heartbeat.run_ig_daily_heartbeat(
            roster_path=roster_path,
            receipt_jsonl=tmp_path / "bad_receipts.jsonl",
            lane_id="lane_1",
            lane_count=1,
            output_root=tmp_path / "packets",
            breakout_candidates_path=bad_tags,
            grid_runner=should_not_run,
        )

    good_tags = _write_json(
        tmp_path / "good_breakouts.json",
        [
            {
                "platform": "instagram",
                "handle": "hyram",
                "tag": "active_breakout_candidate",
                "shortcode": "ABC",
                "producer": "silver_monitoring_fixture",
            }
        ],
    )
    calls: list[dict[str, object]] = []

    def fake_grid_runner(**kwargs: object) -> tuple[int, str]:
        calls.append(dict(kwargs))
        packet_dir = Path(kwargs["output_directory"])
        _write_manifest(packet_dir)
        return 0, str(packet_dir)

    result = heartbeat.run_ig_daily_heartbeat(
        roster_path=roster_path,
        receipt_jsonl=tmp_path / "good_receipts.jsonl",
        lane_id="lane_1",
        lane_count=1,
        output_root=tmp_path / "packets",
        breakout_candidates_path=good_tags,
        grid_runner=fake_grid_runner,
    )

    receipts = _read_jsonl(Path(result.message()))
    assert len(calls) == 1
    assert receipts[0]["deep_capture_selection"] == "breakout_candidate_selected"
    assert receipts[0]["deep_capture_candidates"] == [
        {
            "platform_item_id": "ABC",
            "source": "silver_monitoring_fixture",
            "tag": "active_breakout_candidate",
        }
    ]


def test_registry_index_can_be_used_only_as_pilot_roster_with_limitations(tmp_path: Path) -> None:
    roster_path = _write_json(
        tmp_path / "creator_registry_index.json",
        {
            "creator_registry_index": {
                "index_id": "creator_registry_index_fixture",
                "platform_accounts": [
                    {
                        "platform": "instagram",
                        "public_handle": "hyram",
                        "platform_account_id": "acct_ig_hyram",
                    },
                    {
                        "platform": "tiktok",
                        "public_handle": "hyram",
                        "platform_account_id": "acct_tt_hyram",
                    },
                ],
            }
        },
    )

    def fake_grid_runner(**kwargs: object) -> tuple[int, str]:
        packet_dir = Path(kwargs["output_directory"])
        _write_manifest(packet_dir)
        return 0, str(packet_dir)

    result = heartbeat.run_ig_daily_heartbeat(
        roster_path=roster_path,
        receipt_jsonl=tmp_path / "receipts.jsonl",
        lane_id="lane_1",
        lane_count=1,
        output_root=tmp_path / "packets",
        grid_runner=fake_grid_runner,
    )

    receipts = _read_jsonl(Path(result.message()))
    assert len(receipts) == 1
    receipt = receipts[0]
    assert receipt["roster_source_kind"] == "creator_registry_index_pilot"
    assert receipt["creator"]["roster_status"] == "active_pilot_from_registry_known_account"
    assert "creator_registry_index_used_as_pilot_roster_no_active_monitoring_state" in receipt["limitations"]
    assert "no_active_roster_state_on_creator_registry_row" in receipt["limitations"]


def test_heartbeat_runner_has_no_direct_browser_network_or_platform_write_imports() -> None:
    path = Path(heartbeat.__file__)
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    forbidden_roots = {
        "aiohttp",
        "httpx",
        "playwright",
        "requests",
        "selenium",
        "socket",
        "webbrowser",
    }
    offenders: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            offenders |= {alias.name for alias in node.names if alias.name.split(".", 1)[0] in forbidden_roots}
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.module.split(".", 1)[0] in forbidden_roots:
                offenders.add(node.module)
    assert offenders == set()


def test_succeeded_receipt_never_carries_access_gap_reason_from_path_substring(tmp_path: Path) -> None:
    # On success the grid runner's message is the packet directory path. A handle or
    # output-root path that happens to contain an access-gap trigger substring
    # ("blocked", "login", "challenge", "captcha", "rate_limited") must NOT fabricate an
    # access_gap_reason on a succeeded run -- that would corrupt access-gap telemetry.
    roster_path = _write_json(
        tmp_path / "roster.json",
        {
            "roster_snapshot_id": "ig_roster_snapshot_substring",
            "creators": [
                {
                    "platform": "instagram",
                    "handle": "unblocked_beauty",
                    "platform_account_id": "acct_unblocked",
                    "status": "active",
                }
            ],
        },
    )

    def fake_grid_runner(**kwargs: object) -> tuple[int, str]:
        packet_dir = Path(kwargs["output_directory"])
        _write_manifest(packet_dir)
        return 0, str(packet_dir)

    result = heartbeat.run_ig_daily_heartbeat(
        roster_path=roster_path,
        receipt_jsonl=tmp_path / "receipts.jsonl",
        lane_id="lane_1",
        lane_count=1,
        output_root=tmp_path / "packets",
        grid_runner=fake_grid_runner,
    )

    receipts = _read_jsonl(Path(result.message()))
    assert len(receipts) == 1
    receipt = receipts[0]
    assert receipt["status"] == "succeeded"
    # The trigger substring really is present in the success path, so this asserts the
    # guard (not the absence of the substring) is what keeps the field clean.
    assert "blocked" in str(receipt["packet_pointer"]).lower()
    assert receipt["access_gap_reason"] is None
