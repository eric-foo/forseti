"""Unit tests for the creator-metric Silver reader -- prove the lake path is
no-drift.

These run the producer into a temp lake (``DataLakeRoot.for_test``, no external
lake), then read the rollup records back OFF DISK and assert the reconstructed
seed-shaped rollups equal the seed rollups the producer wrapped. That proves the
capture -> Silver record -> reader path reproduces the registry's metric numbers
exactly, so ``creator_profile_current`` can be sourced from the lake without
drift. The committed view, the seeds, and CI are untouched.
"""
from __future__ import annotations

import json
from pathlib import Path

from capture_spine.creator_profile_current.silver_metric_producer import (
    derive_creator_metric_silver_records_from_projections,
)
from capture_spine.creator_profile_current.silver_metric_reader import (
    read_creator_metric_rollups_from_lake,
)
from data_lake.root import DataLakeRoot

PACKET_ID = "packet_fixture"
GENERATED_AT = "2026-06-30T00:02:00Z"
SEED_WRAPPER = "instagram_reels_creator_metric_seed"


def _account_ledger() -> dict:
    return {
        "platform_accounts": [
            {
                "platform_account_id": "acct_ig_fixture_001",
                "platform": "instagram",
                "public_handle": "fixturecreator",
                "public_profile_url": "https://www.instagram.com/fixturecreator/",
                "handle_source_pointer": "fixture#/rows/0",
                "handle_observed_at": "2026-06-29T00:00:00Z",
            }
        ]
    }


def _profile_row(username: str, value: int, capture_time: str) -> dict:
    return {
        "row_id": f"{PACKET_ID}:profile:follower_count",
        "row_kind": "ig_creator_metric",
        "username": username,
        "content_kind": "profile",
        "content_shortcode": None,
        "content_url": None,
        "metric": "follower_count",
        "posture": "observed",
        "value": value,
        "reason": None,
        "capture_time": capture_time,
        "coverage_window": {"start": None, "end": capture_time},
        "raw_ref": {"packet_id": PACKET_ID, "slice_id": "ig_reels_profile_00"},
        "raw_anchor": {
            "file_id": "file_01",
            "relative_packet_path": "raw/01.json",
            "sha256": "a" * 64,
            "hash_basis": "raw_stored_bytes",
        },
        "chosen_source_surface": "web_profile_info_json_metadata",
        "source_surface_count_candidates": [],
        "source_publication_or_event": None,
    }


def _reel_row(username: str, shortcode: str, metric: str, value: int, capture_time: str) -> dict:
    return {
        "row_id": f"{PACKET_ID}:{shortcode}:{metric}",
        "row_kind": "ig_media_metric",
        "username": username,
        "content_kind": "reel",
        "content_shortcode": shortcode,
        "content_url": f"https://www.instagram.com/{username}/reel/{shortcode}/",
        "metric": metric,
        "posture": "observed",
        "value": value,
        "reason": None,
        "capture_time": capture_time,
        "coverage_window": {"start": None, "end": capture_time},
        "raw_ref": {"packet_id": PACKET_ID, "slice_id": "ig_reels_grid_01"},
        "raw_anchor": {
            "file_id": "file_01",
            "relative_packet_path": "raw/01.json",
            "sha256": "a" * 64,
            "hash_basis": "raw_stored_bytes",
        },
        "chosen_source_surface": "clips_user_json_metadata",
        "source_surface_count_candidates": [],
        "source_publication_or_event": capture_time,
    }


def _projection_rows() -> list[dict]:
    rows = [_profile_row("fixturecreator", 1000, "2026-06-29T00:01:00Z")]
    for shortcode, view, like, comment in (("AAA", 100, 10, 5), ("BBB", 300, 30, 15)):
        rows.append(_reel_row("fixturecreator", shortcode, "view_count", view, "2026-06-29T00:01:00Z"))
        rows.append(_reel_row("fixturecreator", shortcode, "like_count", like, "2026-06-29T00:01:00Z"))
        rows.append(_reel_row("fixturecreator", shortcode, "comment_count", comment, "2026-06-29T00:01:00Z"))
    return rows


def _run(tmp_path: Path):
    projection = tmp_path / "projection.json"
    projection.write_text(json.dumps({"packet_id": PACKET_ID, "rows": _projection_rows()}), encoding="utf-8")
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    result = derive_creator_metric_silver_records_from_projections(
        data_root=data_root,
        projection_paths=[projection],
        account_ledger=_account_ledger(),
        generated_at_utc=GENERATED_AT,
    )
    return data_root, result


def _seed_rollups(result) -> list[dict]:
    return result.seed_document[SEED_WRAPPER]["metric_rollups"]


def test_reader_reconstructs_seed_rollups_with_no_drift(tmp_path: Path) -> None:
    data_root, result = _run(tmp_path)
    seed_rollups = _seed_rollups(result)

    reconstructed = read_creator_metric_rollups_from_lake(data_root, raw_anchors=[PACKET_ID])

    assert len(reconstructed) == len(seed_rollups) == 1
    # Full structural equality: a rollup read back from the lake equals the seed
    # rollup the producer wrapped -- the lake path introduces no drift.
    assert reconstructed[0] == seed_rollups[0]


def test_reader_round_trips_metric_numbers_and_posture(tmp_path: Path) -> None:
    data_root, result = _run(tmp_path)
    rollup = read_creator_metric_rollups_from_lake(data_root, raw_anchors=[PACKET_ID])[0]
    metrics = rollup["metric_rollups"]

    # observed metrics: numeric value, no reason key (matches the seed shape).
    assert metrics["average_views"] == {"value_or_none": 200, "posture": "observed", "metric_unit": "count"}
    assert metrics["median_views"]["value_or_none"] == 200
    assert metrics["engagement_rate"]["posture"] == "observed"
    assert metrics["engagement_rate"]["value_or_none"] == 0.15
    assert "posture_reason_or_none" not in metrics["average_views"]

    # non-observed metrics: null value, carry a posture reason (missing != zero).
    cadence = metrics["posting_cadence"]
    assert cadence["posture"] == "not_attempted"
    assert cadence["value_or_none"] is None
    assert cadence["posture_reason_or_none"]


def test_reader_reads_on_disk_records_not_memory(tmp_path: Path) -> None:
    data_root, result = _run(tmp_path)
    # the records the reader sees are the real on-disk lake files.
    assert result.rollup_paths and all(path.exists() for path in result.rollup_paths)

    reconstructed = read_creator_metric_rollups_from_lake(data_root, raw_anchors=[PACKET_ID])
    seed_rollup = _seed_rollups(result)[0]
    assert reconstructed[0]["metric_rollup_id"] == seed_rollup["metric_rollup_id"]
    assert reconstructed[0]["source_metric_observation_ids"] == seed_rollup["source_metric_observation_ids"]


def test_reader_skips_unknown_anchor(tmp_path: Path) -> None:
    data_root, _result = _run(tmp_path)
    assert read_creator_metric_rollups_from_lake(data_root, raw_anchors=["nosuchpacket"]) == []
