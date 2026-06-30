"""Unit tests for STEP-2b: the creator-metric rollup snapshot generator.

Covers the hardened-alpha ordering authority from the cross-vendor review:
bootstrap never clock-orders (>1 distinct record fails closed), steady-state
advance is double-gated (manifest run-order + STEP 1's computed_at regression),
the snapshot's consumed rollups carry no provenance keys, and the selection
manifest chains. YouTube (account-anchored, no availability index) is the
end-to-end + no-drift vehicle; IG (raw-commit + producer, controllable to >1
record per account) drives the fail-closed cases. Temp lake only.
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
    read_creator_metric_rollups_from_lake,
)
from capture_spine.creator_profile_current.silver_metric_snapshot import (
    MANIFEST_WRAPPER_KEY,
    SNAPSHOT_WRAPPER_KEY,
    SnapshotGenerationError,
    generate_creator_metric_rollup_snapshot,
    manifest_content_hash,
    validate_manifest,
    validate_snapshot,
)
from capture_spine.creator_profile_current.youtube_silver_metric_producer import (
    derive_youtube_creator_metric_silver_records_from_seed_file,
)
from data_lake.root import DataLakeRoot
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet

IG_ACCOUNT = "acct_ig_reels_001"
IG_HANDLE = "hyram"
LATE = "2026-06-30T00:02:00Z"
LATER = "2026-07-01T00:02:00Z"
EARLY = "2026-06-20T00:02:00Z"


def _account_of(record: dict) -> str:
    return record["payload"]["observation"]["subject"]["ref"]["orca_platform_account_id"]


def _ig_discovery_ledger(*account_ids: str) -> dict:
    return {
        "platform_accounts": [
            {"platform_account_id": a, "platform": "instagram", "public_handle": a} for a in account_ids
        ]
    }


def _yt_discovery_ledger(*account_ids: str) -> dict:
    return {
        "platform_accounts": [
            {"platform_account_id": a, "platform": "youtube", "public_handle": a} for a in account_ids
        ]
    }


# -- IG (packet-anchored) controllable fixtures ------------------------------

def _ig_producer_ledger(account_id: str, handle: str) -> dict:
    return {
        "platform_accounts": [
            {
                "platform_account_id": account_id,
                "platform": "instagram",
                "public_handle": handle,
                "public_profile_url": f"https://www.instagram.com/{handle}/",
                "handle_source_pointer": "fixture#/rows/0",
                "handle_observed_at": "2026-06-29T00:00:00Z",
            }
        ]
    }


def _ig_projection_rows(packet_id: str, username: str, views: tuple[int, int]) -> list[dict]:
    cap = "2026-06-29T00:01:00Z"
    raw_anchor = {"file_id": "f1", "relative_packet_path": "raw/01.json", "sha256": "a" * 64, "hash_basis": "raw_stored_bytes"}

    def reel(shortcode: str, metric: str, value: int) -> dict:
        return {
            "row_id": f"{packet_id}:{shortcode}:{metric}",
            "row_kind": "ig_media_metric",
            "username": username,
            "content_kind": "reel",
            "content_shortcode": shortcode,
            "content_url": f"https://www.instagram.com/{username}/reel/{shortcode}/",
            "metric": metric,
            "posture": "observed",
            "value": value,
            "reason": None,
            "capture_time": cap,
            "coverage_window": {"start": None, "end": cap},
            "raw_ref": {"packet_id": packet_id, "slice_id": "ig_reels_grid_01"},
            "raw_anchor": raw_anchor,
            "chosen_source_surface": "clips_user_json_metadata",
            "source_surface_count_candidates": [],
            "source_publication_or_event": cap,
        }

    rows = [
        {
            "row_id": f"{packet_id}:profile:follower_count",
            "row_kind": "ig_creator_metric",
            "username": username,
            "content_kind": "profile",
            "content_shortcode": None,
            "content_url": None,
            "metric": "follower_count",
            "posture": "observed",
            "value": 1000,
            "reason": None,
            "capture_time": cap,
            "coverage_window": {"start": None, "end": cap},
            "raw_ref": {"packet_id": packet_id, "slice_id": "ig_reels_profile_00"},
            "raw_anchor": raw_anchor,
            "chosen_source_surface": "web_profile_info_json_metadata",
            "source_surface_count_candidates": [],
            "source_publication_or_event": None,
        }
    ]
    for shortcode, view, like, comment in (("AAA", views[0], 10, 5), ("BBB", views[1], 30, 15)):
        rows.append(reel(shortcode, "view_count", view))
        rows.append(reel(shortcode, "like_count", like))
        rows.append(reel(shortcode, "comment_count", comment))
    return rows


def _write_ig_rollup(
    data_root: DataLakeRoot,
    tmp_path: Path,
    *,
    slot: str,
    generated_at: str,
    views: tuple[int, int] = (100, 300),
    account_id: str = IG_ACCOUNT,
    handle: str = IG_HANDLE,
) -> None:
    """Commit one IG grid packet + derive its rollup into the SHARED lake."""
    raw = tmp_path / f"ig_raw_{slot}.json"
    raw.write_text(json.dumps({"grid": slot}), encoding="utf-8")
    result = write_local_source_capture_packet(
        data_root=data_root,
        input_files=[raw],
        source_family="instagram_creator",
        source_surface="ig_reels_grid",
        source_locator=known_fact(f"https://www.instagram.com/{handle}/"),
        decision_question="snapshot fixture",
        capture_context="creator metric snapshot test",
    )
    packet_id = result.packet.packet_id
    projection = tmp_path / f"ig_projection_{slot}.json"
    projection.write_text(
        json.dumps({"packet_id": packet_id, "rows": _ig_projection_rows(packet_id, handle, views)}),
        encoding="utf-8",
    )
    derive_creator_metric_silver_records_from_projections(
        data_root=data_root,
        projection_paths=[projection],
        account_ledger=_ig_producer_ledger(account_id, handle),
        generated_at_utc=generated_at,
    )


def _ig_snapshot(data_root, generated_at, prior_manifest=None):
    return generate_creator_metric_rollup_snapshot(
        data_root,
        account_ledger=_ig_discovery_ledger(IG_ACCOUNT),
        platform="instagram",
        snapshot_generated_at=generated_at,
        prior_manifest=prior_manifest,
    )


# -- YouTube (account-anchored) end-to-end -----------------------------------

def test_bootstrap_account_anchored_snapshot_and_no_drift(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    result = derive_youtube_creator_metric_silver_records_from_seed_file(data_root=data_root)
    accounts = sorted({_account_of(r) for r in result.rollup_records})

    run = generate_creator_metric_rollup_snapshot(
        data_root,
        account_ledger=_yt_discovery_ledger(*accounts),
        platform="youtube",
        snapshot_generated_at=LATE,
    )

    body = run.snapshot[SNAPSHOT_WRAPPER_KEY]
    assert body["platform_scope"] == "youtube"
    assert validate_snapshot(run.snapshot) == []
    assert validate_manifest(run.manifest) == []
    # one chosen rollup per covered account, bootstrap run id 1, genesis chain
    prov = body["snapshot_provenance"]
    assert {e["profile_subject_id"] for e in prov["per_account"]} == set(accounts)
    assert all(e["selection_run_id"] == 1 for e in prov["per_account"])
    assert run.manifest[MANIFEST_WRAPPER_KEY]["parent_manifest_sha256"] is None

    # no-drift: each consumed rollup equals the reader's reconstruction of that
    # account's record (which the merged reader tests prove == the seed rollup).
    by_account = {e["profile_subject_id"]: r for e, r in zip(prov["per_account"], body["metric_rollups"])}
    sample = accounts[0]
    reconstructed = read_creator_metric_rollups_from_lake(data_root, raw_anchors=[sample])
    assert by_account[sample] == reconstructed[0]


def test_metric_rollups_carry_no_provenance_keys(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    result = derive_youtube_creator_metric_silver_records_from_seed_file(data_root=data_root)
    accounts = sorted({_account_of(r) for r in result.rollup_records})
    run = generate_creator_metric_rollup_snapshot(
        data_root, account_ledger=_yt_discovery_ledger(*accounts), platform="youtube", snapshot_generated_at=LATE
    )
    forbidden = {"source_record", "content_hash", "record_id", "raw_anchor", "lane_namespace"}
    for rollup in run.snapshot[SNAPSHOT_WRAPPER_KEY]["metric_rollups"]:
        assert forbidden.isdisjoint(rollup)


def test_platform_filter_excludes_other_platform(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path, slot="a", generated_at=LATE)
    yt = derive_youtube_creator_metric_silver_records_from_seed_file(data_root=data_root)
    yt_account = sorted({_account_of(r) for r in yt.rollup_records})[0]
    # ask for an instagram snapshot but pass a ledger holding BOTH platforms;
    # only the IG account is covered.
    ledger = {
        "platform_accounts": [
            {"platform_account_id": IG_ACCOUNT, "platform": "instagram", "public_handle": IG_HANDLE},
            {"platform_account_id": yt_account, "platform": "youtube", "public_handle": yt_account},
        ]
    }
    run = generate_creator_metric_rollup_snapshot(
        data_root, account_ledger=ledger, platform="instagram", snapshot_generated_at=LATE
    )
    subjects = {e["profile_subject_id"] for e in run.snapshot[SNAPSHOT_WRAPPER_KEY]["snapshot_provenance"]["per_account"]}
    assert subjects == {IG_ACCOUNT}


# -- fail-closed ordering (IG, controllable) ---------------------------------

def test_bootstrap_two_distinct_records_fails_closed(tmp_path: Path) -> None:
    # Two grid captures of one account before any snapshot: bootstrap must NOT
    # clock-order them -> STEP 1 raises ambiguous_latest_rollup.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path, slot="a", generated_at=LATE, views=(100, 300))
    _write_ig_rollup(data_root, tmp_path, slot="b", generated_at=LATER, views=(120, 320))

    with pytest.raises(LatestRollupSelectionError) as excinfo:
        _ig_snapshot(data_root, LATE)
    assert excinfo.value.reason == "ambiguous_latest_rollup"
    assert excinfo.value.account_id == IG_ACCOUNT


def test_advance_picks_new_record_and_chains_manifest(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path, slot="a", generated_at=LATE, views=(100, 300))
    run1 = _ig_snapshot(data_root, LATE)  # bootstrap, run id 1
    entry1 = run1.manifest[MANIFEST_WRAPPER_KEY]["entries"][0]

    # a later grid capture (newer computed_at, distinct content) lands
    _write_ig_rollup(data_root, tmp_path, slot="b", generated_at=LATER, views=(120, 320))
    run2 = _ig_snapshot(data_root, LATER, prior_manifest=run1.manifest)

    prov2 = run2.snapshot[SNAPSHOT_WRAPPER_KEY]["snapshot_provenance"]["per_account"][0]
    entry2 = run2.manifest[MANIFEST_WRAPPER_KEY]["entries"][0]
    # advanced to the new record at run id 2; mean(120,320)=220 confirms it's the new one
    assert prov2["selection_run_id"] == 2
    assert prov2["record_id"] != entry1["selected_record_id"]
    assert run2.snapshot[SNAPSHOT_WRAPPER_KEY]["metric_rollups"][0]["metric_rollups"]["average_views"]["value_or_none"] == 220
    # manifest chains and the seen-set now holds both records
    assert run2.manifest[MANIFEST_WRAPPER_KEY]["parent_manifest_sha256"] == manifest_content_hash(run1.manifest)
    assert len(entry2["seen_content_hashes"]) == 2


def test_advance_with_regressed_computed_at_fails_closed(tmp_path: Path) -> None:
    # The newer-arriving record carries an OLDER computed_at than the committed
    # selection -> double-gating: STEP 1 raises computed_at_regression.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path, slot="a", generated_at=LATE, views=(100, 300))
    run1 = _ig_snapshot(data_root, LATE)

    _write_ig_rollup(data_root, tmp_path, slot="b", generated_at=EARLY, views=(120, 320))
    with pytest.raises(LatestRollupSelectionError) as excinfo:
        _ig_snapshot(data_root, LATER, prior_manifest=run1.manifest)
    assert excinfo.value.reason == "computed_at_regression"


def test_no_change_keeps_selection_stable(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path, slot="a", generated_at=LATE)
    run1 = _ig_snapshot(data_root, LATE)
    run2 = _ig_snapshot(data_root, LATER, prior_manifest=run1.manifest)  # nothing new appended

    body1 = run1.snapshot[SNAPSHOT_WRAPPER_KEY]
    body2 = run2.snapshot[SNAPSHOT_WRAPPER_KEY]
    # the consumed view and the chosen record are identical across the no-op run
    assert body2["metric_rollups"] == body1["metric_rollups"]
    p1 = body1["snapshot_provenance"]["per_account"][0]
    p2 = body2["snapshot_provenance"]["per_account"][0]
    assert (p2["record_id"], p2["content_hash"], p2["selection_run_id"]) == (
        p1["record_id"], p1["content_hash"], p1["selection_run_id"]
    )


def test_manifest_selected_record_missing_fails_closed(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path, slot="a", generated_at=LATE)
    bogus_prior = {
        MANIFEST_WRAPPER_KEY: {
            "schema_version": "creator_metric_rollup_selection_manifest_v0",
            "platform_scope": "instagram",
            "selection_run_id": 1,
            "parent_manifest_sha256": None,
            "entries": [
                {
                    "profile_subject_id": IG_ACCOUNT,
                    "selected_record_id": "01NONEXISTENT.json",
                    "selected_content_hash": "sha256:dead",
                    "selection_run_id": 1,
                    "seen_content_hashes": ["sha256:dead"],
                }
            ],
        }
    }
    with pytest.raises(SnapshotGenerationError) as excinfo:
        _ig_snapshot(data_root, LATER, prior_manifest=bogus_prior)
    assert excinfo.value.reason == "manifest_selected_record_missing"
    assert excinfo.value.account_id == IG_ACCOUNT
