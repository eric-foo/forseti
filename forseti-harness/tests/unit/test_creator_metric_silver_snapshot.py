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
import os
from pathlib import Path

import pytest

from capture_spine.creator_profile_current.instagram_metric_seed import (
    build_instagram_reels_creator_metric_seed_from_files,
)
from capture_spine.creator_profile_current.live_lake_freshness_gate import (
    SNAPSHOT_BEHIND_LAKE,
    check_live_lake_freshness,
)
from capture_spine.creator_profile_current.silver_metric_producer import (
    derive_creator_metric_silver_records_from_projections,
)
from capture_spine.creator_profile_current.silver_metric_reader import (
    LatestRollupSelectionError,
)
from capture_spine.creator_profile_current.silver_subject_ref import (
    platform_account_id_from_subject_ref,
)
from capture_spine.creator_profile_current.silver_metric_snapshot import (
    MANIFEST_WRAPPER_KEY,
    SNAPSHOT_WRAPPER_KEY,
    SnapshotGenerationError,
    SnapshotRun,
    generate_creator_metric_rollup_snapshot,
    manifest_content_hash,
    validate_manifest,
    validate_snapshot,
)
from capture_spine.creator_profile_current.youtube_silver_metric_producer import (
    DEFAULT_YOUTUBE_SEED_PATH,
    YOUTUBE_SEED_WRAPPER_KEY,
)
from data_lake.creator_metric_lineage import CreatorMetricLineageError
from data_lake.root import DataLakeRoot
from runners.run_creator_metric_rollup_snapshot import (
    RECEIPT_WRAPPER_KEY,
    SnapshotRunError,
    main as run_snapshot_main,
    run_snapshot,
)
from runners.run_live_lake_freshness_gate import main as run_freshness_gate_main
from runners.run_youtube_creator_metric_rollup_producer import (
    DEFAULT_ACCOUNT_LEDGER as _YT_ACCOUNT_LEDGER,
    _load_account_ledger as _load_youtube_account_ledger,
    default_generated_at_utc as _committed_youtube_generated_at_utc,
    default_source_files as _committed_youtube_source_files,
)
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet
from tests.unit._creator_metric_silver_fixtures import (
    seed_preexisting_youtube_creator_metric_records,
)

IG_ACCOUNT = "acct_ig_reels_001"
IG_HANDLE = "hyram"
LATE = "2026-06-30T00:02:00Z"
LATER = "2026-07-01T00:02:00Z"
EARLY = "2026-06-20T00:02:00Z"
FORSETI_LIVE_LAKE_TEST_ROOT_ENV = "FORSETI_LIVE_LAKE_TEST_ROOT"
LEGACY_ORCA_LIVE_LAKE_TEST_ROOT_ENV = "ORCA_LIVE_LAKE_TEST_ROOT"


def _live_lake_test_root() -> str | None:
    return os.environ.get(FORSETI_LIVE_LAKE_TEST_ROOT_ENV) or os.environ.get(
        LEGACY_ORCA_LIVE_LAKE_TEST_ROOT_ENV
    )


def test_live_lake_test_root_env_prefers_forseti(monkeypatch) -> None:
    monkeypatch.setenv(FORSETI_LIVE_LAKE_TEST_ROOT_ENV, "forseti-live-root")
    monkeypatch.setenv(LEGACY_ORCA_LIVE_LAKE_TEST_ROOT_ENV, "orca-live-root")
    assert _live_lake_test_root() == "forseti-live-root"
    monkeypatch.delenv(FORSETI_LIVE_LAKE_TEST_ROOT_ENV)
    assert _live_lake_test_root() == "orca-live-root"


def _account_of(record: dict) -> str:
    return platform_account_id_from_subject_ref(
        record["payload"]["observation"]["subject"]["ref"], what="rollup subject ref"
    )


def _seed_preexisting_youtube_records(
    data_root: DataLakeRoot,
    *,
    limit_to_platform_account_ids: frozenset[str] | set[str] | None = None,
):
    """Seed synthetic pre-contract bytes for read-side classification only."""
    seed_document = json.loads(DEFAULT_YOUTUBE_SEED_PATH.read_text(encoding="utf-8-sig"))
    return seed_preexisting_youtube_creator_metric_records(
        data_root,
        seed_document,
        wrapper_key=YOUTUBE_SEED_WRAPPER_KEY,
        limit_to_platform_account_ids=limit_to_platform_account_ids,
    )


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


def _ig_projection_rows(
    packet_id: str, username: str, views: tuple[int, int], *, raw_anchor: dict
) -> list[dict]:
    cap = "2026-06-29T00:01:00Z"

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
    preserved = data_root.load_raw_packet(packet_id).manifest["preserved_files"][0]
    raw_anchor = {
        key: preserved[key]
        for key in ("file_id", "relative_packet_path", "sha256", "hash_basis")
    }
    projection = tmp_path / f"ig_projection_{slot}.json"
    projection.write_text(
        json.dumps(
            {
                "packet_id": packet_id,
                "rows": _ig_projection_rows(
                    packet_id, handle, views, raw_anchor=raw_anchor
                ),
            }
        ),
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

def test_committed_seed_cannot_bootstrap_current_snapshot_without_cited_bytes(
    tmp_path: Path,
) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    result = _seed_preexisting_youtube_records(data_root)
    accounts = sorted({_account_of(r) for r in result.rollup_records})

    with pytest.raises(CreatorMetricLineageError, match="depends_on_excluded_observation"):
        generate_creator_metric_rollup_snapshot(
            data_root,
            account_ledger=_yt_discovery_ledger(*accounts),
            platform="youtube",
            snapshot_generated_at=LATE,
        )


def test_seed_rollup_payloads_carry_no_lake_provenance_keys(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    result = _seed_preexisting_youtube_records(data_root)
    forbidden = {"source_record", "content_hash", "record_id", "raw_anchor", "lane_namespace"}
    for rollup in result.seed_document["youtube_shorts_fragrance_creator_metric_seed"]["metric_rollups"]:
        assert forbidden.isdisjoint(rollup)


def test_platform_filter_excludes_other_platform(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path, slot="a", generated_at=LATE)
    # Only one YouTube account is needed to prove platform-filter exclusion,
    # so materialize a single committed-seed account rather than all 30.
    yt = _seed_preexisting_youtube_records(
        data_root, limit_to_platform_account_ids={"acct_yt_fragrance_001"}
    )
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


# -- STEP-3 operator runner (run_creator_metric_rollup_snapshot) -------------
# The runner wraps the pure generator with the file I/O the generator omits:
# loading the prior committed manifest from DISK, the manifest-chain co-presence
# block, the write-time freshness gate, and the freshness receipt. These cases
# exercise paths the in-memory generator tests above do NOT cover.

def _run_ig(data_root, *, generated_at, write, snap: Path, man: Path, rec: Path):
    return run_snapshot(
        data_root,
        account_ledger=_ig_discovery_ledger(IG_ACCOUNT),
        platform="instagram",
        snapshot_generated_at=generated_at,
        reconciled_at=generated_at,
        snapshot_path=snap,
        manifest_path=man,
        receipt_path=rec,
        write=write,
    )


def test_runner_genesis_write_emits_snapshot_manifest_receipt(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path, slot="a", generated_at=LATE)
    snap, man, rec = (tmp_path / "snapshot.json", tmp_path / "manifest.json", tmp_path / "receipt.json")

    summary = _run_ig(data_root, generated_at=LATE, write=True, snap=snap, man=man, rec=rec)

    assert summary["wrote"] is True and summary["selection_run_id"] == 1
    assert snap.exists() and man.exists() and rec.exists()
    written_snap = json.loads(snap.read_text(encoding="utf-8"))
    assert validate_snapshot(written_snap) == []
    assert validate_manifest(json.loads(man.read_text(encoding="utf-8"))) == []
    receipt = json.loads(rec.read_text(encoding="utf-8"))[RECEIPT_WRAPPER_KEY]
    prov = written_snap[SNAPSHOT_WRAPPER_KEY]["snapshot_provenance"]
    # the receipt records the SAME content-set watermark the snapshot carries
    assert receipt["lake_high_watermark"] == prov["lake_high_watermark"]
    assert receipt["selection_run_id"] == 1
    assert {e["profile_subject_id"]: e["content_hash"] for e in receipt["per_account"]} == {
        e["profile_subject_id"]: e["content_hash"] for e in prov["per_account"]
    }


def test_runner_advance_chains_via_disk_round_trip(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    snap, man, rec = (tmp_path / "snapshot.json", tmp_path / "manifest.json", tmp_path / "receipt.json")
    _write_ig_rollup(data_root, tmp_path, slot="a", generated_at=LATE, views=(100, 300))
    run1 = _run_ig(data_root, generated_at=LATE, write=True, snap=snap, man=man, rec=rec)

    # a genuinely newer record appended; the second run loads the prior manifest
    # from DISK (not an in-memory handoff) and advances the run-order chain.
    _write_ig_rollup(data_root, tmp_path, slot="b", generated_at=LATER, views=(120, 320))
    run2 = _run_ig(data_root, generated_at=LATER, write=True, snap=snap, man=man, rec=rec)

    assert run1["selection_run_id"] == 1 and run2["selection_run_id"] == 2
    assert run2["lake_high_watermark"] != run1["lake_high_watermark"]
    chained = json.loads(man.read_text(encoding="utf-8"))[MANIFEST_WRAPPER_KEY]
    assert chained["parent_manifest_sha256"] == manifest_content_hash(run1["manifest"])


def test_runner_dry_run_writes_nothing_but_still_gates(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path, slot="a", generated_at=LATE)
    snap, man, rec = (tmp_path / "snapshot.json", tmp_path / "manifest.json", tmp_path / "receipt.json")

    summary = _run_ig(data_root, generated_at=LATE, write=False, snap=snap, man=man, rec=rec)

    assert summary["wrote"] is False
    assert summary["lake_high_watermark"].startswith("sha256:")  # the gate ran
    assert not snap.exists() and not man.exists() and not rec.exists()


def test_runner_blocks_when_snapshot_present_but_manifest_missing(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path, slot="a", generated_at=LATE)
    snap, man, rec = (tmp_path / "snapshot.json", tmp_path / "manifest.json", tmp_path / "receipt.json")
    snap.write_text("{}", encoding="utf-8")  # committed snapshot but NO companion manifest

    with pytest.raises(SnapshotRunError) as excinfo:
        _run_ig(data_root, generated_at=LATER, write=True, snap=snap, man=man, rec=rec)
    assert excinfo.value.reason == "manifest_chain_broken"
    assert not man.exists()  # never reset the chain by writing a fresh run-id-1 manifest


def test_runner_blocks_when_committed_manifest_invalid(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path, slot="a", generated_at=LATE)
    snap, man, rec = (tmp_path / "snapshot.json", tmp_path / "manifest.json", tmp_path / "receipt.json")
    snap.write_text("{}", encoding="utf-8")
    man.write_text("{}", encoding="utf-8")  # present but fails the manifest validator

    with pytest.raises(SnapshotRunError) as excinfo:
        _run_ig(data_root, generated_at=LATER, write=True, snap=snap, man=man, rec=rec)
    assert excinfo.value.reason == "manifest_chain_broken"


def test_runner_main_against_live_lake_when_available(monkeypatch) -> None:
    # main()/resolve is the only real-lake-bound path; explicit operator opt-in
    # only (ambient FORSETI_DATA_ROOT/ORCA_DATA_ROOT are deleted per-test in conftest).
    live_root = _live_lake_test_root()
    if not live_root:
        pytest.skip(
            "FORSETI_LIVE_LAKE_TEST_ROOT is not set; legacy ORCA_LIVE_LAKE_TEST_ROOT "
            "is also accepted for this explicit opt-in live-lake check"
        )
    monkeypatch.setenv("FORSETI_DATA_ROOT", live_root)
    try:
        code = run_snapshot_main(["--platform", "instagram"])  # dry-run
    except SystemExit as exc:
        code = exc.code
    # success, or a clean fail-closed (e.g. the producer is unwired -> zero
    # rollups -> missing_account_rollup) -- never an uncaught crash.
    assert code in (0, 2)


def _fake_snapshot_run(watermark: str) -> SnapshotRun:
    # Minimal stand-in carrying only what the write-time gate inspects.
    snapshot = {
        SNAPSHOT_WRAPPER_KEY: {
            "snapshot_provenance": {
                "lake_high_watermark": watermark,
                "per_account": [{"profile_subject_id": IG_ACCOUNT, "content_hash": watermark}],
            }
        }
    }
    return SnapshotRun(snapshot=snapshot, manifest={})


def test_runner_freshness_gate_fires_when_lake_moves(tmp_path: Path, monkeypatch) -> None:
    # Negative test for the write-time gate: the two generator reads return
    # different watermarks (as a concurrent capture would), so the gate must fail
    # closed and write nothing. Without this, deleting the gate's raise would go
    # uncaught by the suite.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    snap, man, rec = (tmp_path / "snapshot.json", tmp_path / "manifest.json", tmp_path / "receipt.json")
    runs = iter([_fake_snapshot_run("sha256:aaa"), _fake_snapshot_run("sha256:bbb")])
    monkeypatch.setattr(
        "runners.run_creator_metric_rollup_snapshot.generate_creator_metric_rollup_snapshot",
        lambda *a, **k: next(runs),
    )
    with pytest.raises(SnapshotRunError) as excinfo:
        _run_ig(data_root, generated_at=LATE, write=True, snap=snap, man=man, rec=rec)
    assert excinfo.value.reason == "lake_moved_during_snapshot"
    assert not snap.exists() and not man.exists() and not rec.exists()


def test_runner_blocks_when_committed_manifest_type_corrupt(tmp_path: Path) -> None:
    # A committed manifest that passes key-presence but has a type-wrong
    # seen_content_hashes (a bare string) must fail closed, not silently advance
    # the run-order chain by reading the string as a per-character set.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path, slot="a", generated_at=LATE)
    snap, man, rec = (tmp_path / "snapshot.json", tmp_path / "manifest.json", tmp_path / "receipt.json")
    _run_ig(data_root, generated_at=LATE, write=True, snap=snap, man=man, rec=rec)
    doc = json.loads(man.read_text(encoding="utf-8"))
    doc[MANIFEST_WRAPPER_KEY]["entries"][0]["seen_content_hashes"] = "sha256:not-a-list"
    man.write_text(json.dumps(doc), encoding="utf-8")
    with pytest.raises(SnapshotRunError) as excinfo:
        _run_ig(data_root, generated_at=LATER, write=True, snap=snap, man=man, rec=rec)
    assert excinfo.value.reason == "manifest_chain_broken"


def test_runner_blocks_when_committed_snapshot_invalid(tmp_path: Path) -> None:
    # The co-presence block advertises "both present-and-valid": a corrupt prior
    # snapshot (manifest still valid) must fail closed too.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path, slot="a", generated_at=LATE)
    snap, man, rec = (tmp_path / "snapshot.json", tmp_path / "manifest.json", tmp_path / "receipt.json")
    _run_ig(data_root, generated_at=LATE, write=True, snap=snap, man=man, rec=rec)
    snap.write_text("{}", encoding="utf-8")  # present but schema-invalid
    with pytest.raises(SnapshotRunError) as excinfo:
        _run_ig(data_root, generated_at=LATER, write=True, snap=snap, man=man, rec=rec)
    assert excinfo.value.reason == "manifest_chain_broken"


# -- adapter-equivalence (no-drift) gate -------------------------------------
# The load-bearing proof that re-pointing materialize from the seed onto the
# lake-derived snapshot is a no-op on the numbers: given identical projections,
# the two independent adapters must produce value-equal metric_rollups.

def test_ig_lake_path_rollups_equal_seed_builder_no_drift(tmp_path: Path) -> None:
    """Adapter-equivalence gate (CI, lake-free). Given identical IG projections,
    the lake-fed path (producer -> lake -> reader -> snapshot) yields
    metric_rollups VALUE-equal to the independent seed-builder path -- exactly
    what makes re-pointing materialize a no-op on the registry's numbers. The
    committed seed's source projections are not in the repo, so this proves the
    two ADAPTERS agree on shared input; the "== committed seed" check is the
    later real-lake inspection diff (a stale seed legitimately differs)."""
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    raw = tmp_path / "ig_raw.json"
    raw.write_text(json.dumps({"grid": "x"}), encoding="utf-8")
    packet_id = write_local_source_capture_packet(
        data_root=data_root,
        input_files=[raw],
        source_family="instagram_creator",
        source_surface="ig_reels_grid",
        source_locator=known_fact(f"https://www.instagram.com/{IG_HANDLE}/"),
        decision_question="equivalence",
        capture_context="no-drift equivalence gate",
    ).packet.packet_id
    preserved = data_root.load_raw_packet(packet_id).manifest["preserved_files"][0]
    raw_anchor = {
        key: preserved[key]
        for key in ("file_id", "relative_packet_path", "sha256", "hash_basis")
    }
    projection = tmp_path / "ig_projection.json"
    projection.write_text(
        json.dumps(
            {
                "packet_id": packet_id,
                "rows": _ig_projection_rows(
                    packet_id, IG_HANDLE, (100, 300), raw_anchor=raw_anchor
                ),
            }
        ),
        encoding="utf-8",
    )

    # lake-fed adapter: producer -> lake -> snapshot
    derive_creator_metric_silver_records_from_projections(
        data_root=data_root,
        projection_paths=[projection],
        account_ledger=_ig_producer_ledger(IG_ACCOUNT, IG_HANDLE),
        generated_at_utc=LATE,
    )
    snapshot = generate_creator_metric_rollup_snapshot(
        data_root,
        account_ledger=_ig_discovery_ledger(IG_ACCOUNT),
        platform="instagram",
        snapshot_generated_at=LATE,
    )
    snapshot_rollups = snapshot.snapshot[SNAPSHOT_WRAPPER_KEY]["metric_rollups"]

    # independent seed-builder adapter: SAME projection + timestamp
    seed = build_instagram_reels_creator_metric_seed_from_files(
        projection_paths=[projection],
        account_ledger=_ig_producer_ledger(IG_ACCOUNT, IG_HANDLE),
        generated_at_utc=LATE,
    )
    seed_rollups = seed["instagram_reels_creator_metric_seed"]["metric_rollups"]

    assert snapshot_rollups == seed_rollups


def test_youtube_review_json_assertions_do_not_count_as_captured_bytes(tmp_path: Path) -> None:
    """The seed builder can reproduce numbers, but its review JSON inputs assert
    watch hashes; they are not the cited watch HTML bytes and cannot bootstrap a
    current source-backed snapshot."""
    data_root = DataLakeRoot.for_test(tmp_path / "lake")

    result = _seed_preexisting_youtube_records(data_root)
    accounts = sorted({_account_of(r) for r in result.rollup_records})

    with pytest.raises(CreatorMetricLineageError, match="depends_on_excluded_observation"):
        generate_creator_metric_rollup_snapshot(
            data_root,
            account_ledger=_yt_discovery_ledger(*accounts),
            platform="youtube",
            snapshot_generated_at=LATE,
        )


# -- live-lake freshness gate (AR-02, §6) ------------------------------------

def test_live_lake_freshness_gate_is_fresh_when_snapshot_matches_lake(tmp_path: Path) -> None:
    # The committed snapshot was generated from this exact lake state, so the gate
    # re-runs selection against the live lake and finds the same content-addressed
    # watermark -> FRESH, no drift.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path, slot="a", generated_at=LATE)
    run = _ig_snapshot(data_root, generated_at=LATE)

    result = check_live_lake_freshness(
        data_root,
        account_ledger=_ig_discovery_ledger(IG_ACCOUNT),
        platform="instagram",
        committed_snapshot=run.snapshot,
        committed_manifest=run.manifest,
    )
    assert result.is_fresh
    assert result.reason is None
    assert result.committed_watermark == result.live_watermark
    assert result.drifted_accounts == ()


def test_live_lake_freshness_gate_fires_when_lake_advances(tmp_path: Path) -> None:
    # A newer rollup appended after the snapshot (a fresh capture the operator did
    # not regen into the registry) is the silent-drift case: the gate must catch it
    # as snapshot_behind_lake and name the drifted account.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path, slot="a", generated_at=LATE, views=(100, 300))
    run = _ig_snapshot(data_root, generated_at=LATE)

    _write_ig_rollup(data_root, tmp_path, slot="b", generated_at=LATER, views=(999, 1500))

    result = check_live_lake_freshness(
        data_root,
        account_ledger=_ig_discovery_ledger(IG_ACCOUNT),
        platform="instagram",
        committed_snapshot=run.snapshot,
        committed_manifest=run.manifest,
    )
    assert not result.is_fresh
    assert result.reason == SNAPSHOT_BEHIND_LAKE
    assert result.committed_watermark != result.live_watermark
    assert IG_ACCOUNT in result.drifted_accounts


def test_live_lake_freshness_gate_main_against_live_lake_when_available(monkeypatch) -> None:
    # main()/resolve is the only real-lake-bound path; explicit operator opt-in
    # only (ambient FORSETI_DATA_ROOT/ORCA_DATA_ROOT are deleted per-test in conftest).
    live_root = _live_lake_test_root()
    if not live_root:
        pytest.skip(
            "FORSETI_LIVE_LAKE_TEST_ROOT is not set; legacy ORCA_LIVE_LAKE_TEST_ROOT "
            "is also accepted for this explicit opt-in live-lake check"
        )
    monkeypatch.setenv("FORSETI_DATA_ROOT", live_root)
    try:
        code = run_freshness_gate_main(["--platform", "instagram"])
    except SystemExit as exc:
        code = exc.code
    # FRESH (0), drift or a clean fail-closed (2) -- never an uncaught crash.
    assert code in (0, 2)
