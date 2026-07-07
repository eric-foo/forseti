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

import pytest

from capture_spine.creator_profile_current.silver_metric_producer import (
    derive_creator_metric_silver_records_from_projections,
)
from capture_spine.creator_profile_current.silver_metric_reader import (
    LatestRollupSelectionError,
    RollupRunCandidate,
    read_creator_metric_rollups_from_lake,
    select_latest_rollup_per_account,
)
from capture_spine.creator_profile_current.silver_subject_ref import (
    FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY,
    LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY,
)
from data_lake.root import DataLakeRoot

PACKET_ID = "packet_fixture"
GENERATED_AT = "2026-06-30T00:02:00Z"
SEED_WRAPPER = "instagram_reels_creator_metric_seed"


def _ledger_entry(account_id: str, handle: str) -> dict:
    return {
        "platform_account_id": account_id,
        "platform": "instagram",
        "public_handle": handle,
        "public_profile_url": f"https://www.instagram.com/{handle}/",
        "handle_source_pointer": "fixture#/rows/0",
        "handle_observed_at": "2026-06-29T00:00:00Z",
    }


def _account_ledger() -> dict:
    return {"platform_accounts": [_ledger_entry("acct_ig_fixture_001", "fixturecreator")]}


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


def _projection_rows(username: str = "fixturecreator", views: tuple[int, int] = (100, 300)) -> list[dict]:
    rows = [_profile_row(username, 1000, "2026-06-29T00:01:00Z")]
    for shortcode, view, like, comment in (("AAA", views[0], 10, 5), ("BBB", views[1], 30, 15)):
        rows.append(_reel_row(username, shortcode, "view_count", view, "2026-06-29T00:01:00Z"))
        rows.append(_reel_row(username, shortcode, "like_count", like, "2026-06-29T00:01:00Z"))
        rows.append(_reel_row(username, shortcode, "comment_count", comment, "2026-06-29T00:01:00Z"))
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


def test_reader_accepts_legacy_orca_subject_ref_key(tmp_path: Path) -> None:
    data_root, result = _run(tmp_path)
    record_path = result.rollup_paths[0]
    record = json.loads(record_path.read_text(encoding="utf-8"))
    subject_ref = record["payload"]["observation"]["subject"]["ref"]
    subject_ref[LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY] = subject_ref.pop(
        FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY
    )
    record_path.write_text(json.dumps(record), encoding="utf-8")

    reconstructed = read_creator_metric_rollups_from_lake(data_root, raw_anchors=[PACKET_ID])

    assert reconstructed[0]["profile_subject_id"] == "acct_ig_fixture_001"


def test_reader_skips_unknown_anchor(tmp_path: Path) -> None:
    data_root, _result = _run(tmp_path)
    assert read_creator_metric_rollups_from_lake(data_root, raw_anchors=["nosuchpacket"]) == []


# --- select_latest_rollup_per_account (latest-per-account selection rule) -------

ACCOUNT = "acct_ig_fixture_001"


def _rollup_record(
    tmp_path: Path,
    *,
    slot: str,
    generated_at: str,
    username: str = "fixturecreator",
    account_id: str = ACCOUNT,
    views: tuple[int, int] = (100, 300),
) -> dict:
    """Run the producer into an isolated temp lake and return the single on-disk
    rollup record. Distinct ``views`` / ``generated_at`` yield genuinely distinct
    records (different ``content_hash``); identical args reproduce identical
    content. Each slot is its own lake, so records never collide on append.
    """
    base = tmp_path / slot
    base.mkdir(parents=True, exist_ok=True)
    projection = base / "projection.json"
    projection.write_text(
        json.dumps({"packet_id": PACKET_ID, "rows": _projection_rows(username, views)}),
        encoding="utf-8",
    )
    data_root = DataLakeRoot.for_test(base / "lake")
    result = derive_creator_metric_silver_records_from_projections(
        data_root=data_root,
        projection_paths=[projection],
        account_ledger={"platform_accounts": [_ledger_entry(account_id, username)]},
        generated_at_utc=generated_at,
    )
    return json.loads(result.rollup_paths[0].read_text(encoding="utf-8"))


def test_select_latest_picks_newest_run_not_list_order(tmp_path: Path) -> None:
    early = _rollup_record(tmp_path, slot="early", generated_at="2026-06-29T00:02:00Z")
    late = _rollup_record(
        tmp_path, slot="late", generated_at="2026-06-30T00:02:00Z", views=(120, 320)
    )

    # Pass the newer run first to prove run order -- not list order -- governs.
    selected = select_latest_rollup_per_account(
        [
            RollupRunCandidate(selection_run_id=2, record=late),
            RollupRunCandidate(selection_run_id=1, record=early),
        ]
    )

    assert set(selected) == {ACCOUNT}
    chosen = selected[ACCOUNT]
    assert chosen.selection_run_id == 2
    assert chosen.record_id == late["record_id"]
    assert chosen.content_hash == late["content_hash"]
    # The returned rollup is the seed-shaped reconstruction of the chosen record:
    # mean(120, 320) == 220, distinct from the earlier run's mean(100, 300) == 200.
    assert chosen.rollup["metric_rollups"]["average_views"]["value_or_none"] == 220
    assert chosen.rollup["computed_at"] == "2026-06-30T00:02:00Z"


def test_select_collapses_identical_content_across_runs(tmp_path: Path) -> None:
    record = _rollup_record(tmp_path, slot="r", generated_at=GENERATED_AT)

    # The same unchanged rollup re-selected by runs 1 and 3 -> one entry, newest run.
    selected = select_latest_rollup_per_account(
        [
            RollupRunCandidate(selection_run_id=1, record=record),
            RollupRunCandidate(selection_run_id=3, record=record),
        ]
    )

    assert set(selected) == {ACCOUNT}
    chosen = selected[ACCOUNT]
    assert chosen.content_hash == record["content_hash"]
    assert chosen.selection_run_id == 3


def test_select_fails_closed_on_computed_at_regression(tmp_path: Path) -> None:
    newer_time = _rollup_record(tmp_path, slot="late", generated_at="2026-06-30T00:02:00Z")
    older_time = _rollup_record(
        tmp_path, slot="early", generated_at="2026-06-20T00:02:00Z", views=(120, 320)
    )

    # Run 2 (the newer run) carries the OLDER computed_at -> regression, fail closed.
    with pytest.raises(LatestRollupSelectionError) as excinfo:
        select_latest_rollup_per_account(
            [
                RollupRunCandidate(selection_run_id=1, record=newer_time),
                RollupRunCandidate(selection_run_id=2, record=older_time),
            ]
        )

    assert excinfo.value.reason == "computed_at_regression"
    assert excinfo.value.account_id == ACCOUNT


def test_select_fails_closed_on_same_run_distinct_content(tmp_path: Path) -> None:
    one = _rollup_record(tmp_path, slot="one", generated_at=GENERATED_AT, views=(100, 300))
    two = _rollup_record(tmp_path, slot="two", generated_at=GENERATED_AT, views=(140, 340))

    # Two distinct rollups tie on the same selection_run_id -> unorderable.
    with pytest.raises(LatestRollupSelectionError) as excinfo:
        select_latest_rollup_per_account(
            [
                RollupRunCandidate(selection_run_id=5, record=one),
                RollupRunCandidate(selection_run_id=5, record=two),
            ]
        )

    assert excinfo.value.reason == "ambiguous_latest_rollup"
    assert excinfo.value.account_id == ACCOUNT


def test_select_fails_closed_on_reused_computed_at_across_runs(tmp_path: Path) -> None:
    one = _rollup_record(tmp_path, slot="one", generated_at=GENERATED_AT, views=(100, 300))
    two = _rollup_record(tmp_path, slot="two", generated_at=GENERATED_AT, views=(140, 340))

    # Newer run reuses the earlier run's exact computed_at with different content
    # -> the timestamp cannot break the tie, fail closed rather than guess.
    with pytest.raises(LatestRollupSelectionError) as excinfo:
        select_latest_rollup_per_account(
            [
                RollupRunCandidate(selection_run_id=1, record=one),
                RollupRunCandidate(selection_run_id=2, record=two),
            ]
        )

    assert excinfo.value.reason == "ambiguous_latest_rollup"


def test_select_groups_accounts_independently(tmp_path: Path) -> None:
    acct1_early = _rollup_record(tmp_path, slot="a1e", generated_at="2026-06-29T00:02:00Z")
    acct1_late = _rollup_record(
        tmp_path, slot="a1l", generated_at="2026-06-30T00:02:00Z", views=(120, 320)
    )
    acct2 = _rollup_record(
        tmp_path,
        slot="a2",
        generated_at="2026-06-28T00:02:00Z",
        username="othercreator",
        account_id="acct_ig_fixture_002",
    )

    selected = select_latest_rollup_per_account(
        [
            RollupRunCandidate(selection_run_id=1, record=acct1_early),
            RollupRunCandidate(selection_run_id=2, record=acct1_late),
            RollupRunCandidate(selection_run_id=2, record=acct2),
        ]
    )

    assert set(selected) == {ACCOUNT, "acct_ig_fixture_002"}
    # Account 1 advances to its newest run; account 2's lone rollup is untouched
    # by account 1's run history (no cross-account leakage).
    assert selected[ACCOUNT].record_id == acct1_late["record_id"]
    assert selected["acct_ig_fixture_002"].record_id == acct2["record_id"]
    assert selected["acct_ig_fixture_002"].selection_run_id == 2


def test_select_returns_empty_for_no_candidates() -> None:
    # The selection rule does not fail closed on an empty input -- enforcing the
    # expected account set ("every ledger account must resolve to one rollup")
    # belongs to discovery, not to this pure rule.
    assert select_latest_rollup_per_account([]) == {}
