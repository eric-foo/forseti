"""Unit tests for platform-aware creator-metric rollup discovery.

Discovery is platform-aware because the two merged producers anchor rollups
differently: Instagram rollups are packet-anchored (found via the availability
index -> ``list_available("instagram_creator")`` -> ``lane_dir``) and YouTube
rollups are account-anchored (found via per-account ``lane_dir``). Both shapes
are exercised against a temp lake (``DataLakeRoot.for_test``) using the real
producers and the real raw-commit writer; the committed view, the seeds, and CI
are untouched. The headline property is the fail-closed guard on the EXPECTED
account set -- a non-empty packet set that lacks a rollup for an expected
account still fails closed.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from capture_spine.creator_profile_current.silver_metric_producer import (
    derive_creator_metric_silver_records_from_projections,
)
from capture_spine.creator_profile_current.silver_metric_reader import (
    CreatorRollupDiscoveryError,
    discover_creator_metric_rollup_records,
)
from capture_spine.creator_profile_current.silver_subject_ref import (
    FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY,
    LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY,
    platform_account_id_from_subject_ref,
)
from capture_spine.creator_profile_current.youtube_silver_metric_producer import (
    DEFAULT_YOUTUBE_SEED_PATH,
    YOUTUBE_SEED_WRAPPER_KEY,
)
from data_lake.creator_metric_lineage import AUDIT_COMPATIBLE
from data_lake.root import DataLakeRoot, EPOCH_MARKER_FILENAME, raw_shard
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet
from tests.unit._creator_metric_silver_fixtures import (
    seed_preexisting_youtube_creator_metric_records,
)

IG_ACCOUNT = "acct_ig_reels_001"
IG_HANDLE = "hyram"


def _ledger(*entries: tuple[str, str]) -> dict:
    """Build a minimal discovery ledger from (platform_account_id, platform)
    pairs. Discovery reads only ``platform_account_id`` + ``platform``."""
    return {
        "platform_accounts": [
            {"platform_account_id": account_id, "platform": platform, "public_handle": account_id}
            for account_id, platform in entries
        ]
    }


def _account_of(record: dict) -> str:
    return platform_account_id_from_subject_ref(
        record["payload"]["observation"]["subject"]["ref"], what="rollup subject ref"
    )


# -- Instagram (packet-anchored) fixtures -----------------------------------

def _commit_ig_raw_packet(data_root: DataLakeRoot, tmp_path: Path, *, slot: str) -> str:
    """Commit a minimal ``instagram_creator`` raw packet (records availability)
    and return its packet id -- the anchor the IG rollup binds to."""
    raw = tmp_path / f"ig_raw_{slot}.json"
    # Content varies by slot: a byte-identical raw packet for the same
    # source_locator would collide with the Bronze write-gate's duplicate check
    # when a test commits more than one packet for the same account (see
    # test_returns_all_records_per_account_for_selection).
    raw.write_text(json.dumps({"reels_grid": "fixture bytes", "slot": slot}), encoding="utf-8")
    result = write_local_source_capture_packet(
        data_root=data_root,
        input_files=[raw],
        source_family="instagram_creator",
        source_surface="ig_reels_grid",
        source_locator=known_fact(f"https://www.instagram.com/{IG_HANDLE}/"),
        decision_question="creator metric discovery fixture",
        capture_context="creator metric silver discovery test",
    )
    return result.packet.packet_id


def _ig_projection_rows(
    packet_id: str, *, username: str, views: tuple[int, int], raw_anchor: dict
) -> list[dict]:
    capture = "2026-06-29T00:01:00Z"
    def _reel(shortcode: str, metric: str, value: int) -> dict:
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
            "capture_time": capture,
            "coverage_window": {"start": None, "end": capture},
            "raw_ref": {"packet_id": packet_id, "slice_id": "ig_reels_grid_01"},
            "raw_anchor": raw_anchor,
            "chosen_source_surface": "clips_user_json_metadata",
            "source_surface_count_candidates": [],
            "source_publication_or_event": capture,
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
            "capture_time": capture,
            "coverage_window": {"start": None, "end": capture},
            "raw_ref": {"packet_id": packet_id, "slice_id": "ig_reels_profile_00"},
            "raw_anchor": raw_anchor,
            "chosen_source_surface": "web_profile_info_json_metadata",
            "source_surface_count_candidates": [],
            "source_publication_or_event": None,
        }
    ]
    for shortcode, view, like, comment in (("AAA", views[0], 10, 5), ("BBB", views[1], 30, 15)):
        rows.append(_reel(shortcode, "view_count", view))
        rows.append(_reel(shortcode, "like_count", like))
        rows.append(_reel(shortcode, "comment_count", comment))
    return rows


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


def _write_ig_rollup(
    data_root: DataLakeRoot,
    tmp_path: Path,
    *,
    account_id: str = IG_ACCOUNT,
    handle: str = IG_HANDLE,
    slot: str = "a",
    views: tuple[int, int] = (100, 300),
) -> str:
    """Commit an IG raw packet and derive its rollup (anchored to that packet)
    for one account. Returns the packet id."""
    packet_id = _commit_ig_raw_packet(data_root, tmp_path, slot=slot)
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
                    packet_id, username=handle, views=views, raw_anchor=raw_anchor
                ),
            }
        ),
        encoding="utf-8",
    )
    derive_creator_metric_silver_records_from_projections(
        data_root=data_root,
        projection_paths=[projection],
        account_ledger=_ig_producer_ledger(account_id, handle),
        generated_at_utc="2026-06-30T00:02:00Z",
    )
    return packet_id


# -- YouTube (account-anchored) fixture -------------------------------------

def _write_yt_rollups(data_root: DataLakeRoot, tmp_path: Path) -> set[str]:
    """Seed pre-contract YT bytes for read-side audit classification only.

    Both call sites only ever consume a single account from the returned set
    (``sorted(...)[0]``), so materialize one committed-seed account instead of
    all 30.
    """
    seed_document = json.loads(DEFAULT_YOUTUBE_SEED_PATH.read_text(encoding="utf-8-sig"))
    result = seed_preexisting_youtube_creator_metric_records(
        data_root,
        seed_document,
        wrapper_key=YOUTUBE_SEED_WRAPPER_KEY,
        limit_to_platform_account_ids={"acct_yt_fragrance_001"},
    )
    archive = tmp_path / "youtube_seed_archive"
    archive.mkdir()
    (archive / ".orca-data-root").write_text(
        json.dumps(
            {
                "root_uuid": "01KWYTSEEDARCHIVEROOT00001",
                "label": "youtube-seed-test-archive",
                "contract_version": "v0",
            }
        ),
        encoding="utf-8",
    )
    for record in result.observation_records:
        packet_id = record["raw_anchor"]
        packet = archive / "raw" / raw_shard(packet_id) / packet_id
        body = packet / "raw" / "caption.json"
        body.parent.mkdir(parents=True, exist_ok=True)
        body.write_bytes(b"caption fixture; cited watch HTML intentionally absent")
        digest = hashlib.sha256(body.read_bytes()).hexdigest()
        (packet / "manifest.json").write_text(
            json.dumps(
                {
                    "packet_id": packet_id,
                    "preserved_files": [
                        {
                            "file_id": "file_01",
                            "relative_packet_path": "raw/caption.json",
                            "size_bytes": body.stat().st_size,
                            "sha256": digest,
                            "hash_basis": "raw_stored_bytes",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
    epoch_path = data_root.path / EPOCH_MARKER_FILENAME
    epoch = json.loads(epoch_path.read_text(encoding="utf-8"))
    epoch["legacy_roots"] = [str(archive)]
    epoch_path.write_text(json.dumps(epoch), encoding="utf-8")
    return {_account_of(record) for record in result.rollup_records}


# -- tests -------------------------------------------------------------------

def test_discovers_ig_rollup_via_availability_index(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path)

    found = discover_creator_metric_rollup_records(
        data_root, account_ledger=_ledger((IG_ACCOUNT, "instagram"))
    )

    assert set(found) == {IG_ACCOUNT}
    assert len(found[IG_ACCOUNT]) == 1
    record = found[IG_ACCOUNT][0]
    assert _account_of(record) == IG_ACCOUNT
    assert record["payload_kind"] == "MetricRollupObservation"


def test_discovers_legacy_orca_subject_ref_key(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id = _write_ig_rollup(data_root, tmp_path)
    lane_dir = data_root.lane_dir(
        subtree="derived", raw_anchor=packet_id, lane="creator_metric_rollup_silver"
    )
    record_path = next(lane_dir.glob("*.json"))
    record = json.loads(record_path.read_text(encoding="utf-8"))
    subject_ref = record["payload"]["observation"]["subject"]["ref"]
    subject_ref[LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY] = subject_ref.pop(
        FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY
    )
    record_path.write_text(json.dumps(record), encoding="utf-8")

    found = discover_creator_metric_rollup_records(
        data_root, account_ledger=_ledger((IG_ACCOUNT, "instagram"))
    )

    assert set(found) == {IG_ACCOUNT}
    assert _account_of(found[IG_ACCOUNT][0]) == IG_ACCOUNT


def test_discovers_historical_yt_rollup_only_through_audit_mode(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    covered = _write_yt_rollups(data_root, tmp_path)
    account_id = sorted(covered)[0]

    with pytest.raises(CreatorRollupDiscoveryError):
        discover_creator_metric_rollup_records(
            data_root, account_ledger=_ledger((account_id, "youtube"))
        )

    found = discover_creator_metric_rollup_records(
        data_root,
        account_ledger=_ledger((account_id, "youtube")),
        lineage_mode=AUDIT_COMPATIBLE,
    )

    assert set(found) == {account_id}
    assert found[account_id]
    assert all(_account_of(record) == account_id for record in found[account_id])


def test_discovers_mixed_ig_and_yt(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path)
    yt_account = sorted(_write_yt_rollups(data_root, tmp_path))[0]

    found = discover_creator_metric_rollup_records(
        data_root,
        account_ledger=_ledger((IG_ACCOUNT, "instagram"), (yt_account, "youtube")),
        lineage_mode=AUDIT_COMPATIBLE,
    )

    assert set(found) == {IG_ACCOUNT, yt_account}
    assert found[IG_ACCOUNT] and found[yt_account]


def test_fails_closed_on_missing_account_despite_nonempty_packets(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path)  # only IG_ACCOUNT present

    # A second expected IG account has no rollup. The instagram_creator packet
    # set is non-empty, but the guard checks the EXPECTED account -> fail closed.
    with pytest.raises(CreatorRollupDiscoveryError) as excinfo:
        discover_creator_metric_rollup_records(
            data_root,
            account_ledger=_ledger((IG_ACCOUNT, "instagram"), ("acct_ig_reels_999", "instagram")),
        )

    assert excinfo.value.reason == "missing_account_rollup"
    assert excinfo.value.account_id == "acct_ig_reels_999"


def test_fails_closed_when_expected_yt_account_absent(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path)  # IG present, no YT records at all

    with pytest.raises(CreatorRollupDiscoveryError) as excinfo:
        discover_creator_metric_rollup_records(
            data_root,
            account_ledger=_ledger((IG_ACCOUNT, "instagram"), ("acct_yt_fragrance_001", "youtube")),
        )

    assert excinfo.value.reason == "missing_account_rollup"
    assert excinfo.value.account_id == "acct_yt_fragrance_001"


def test_returns_all_records_per_account_for_selection(tmp_path: Path) -> None:
    # Two IG snapshot runs append two distinct rollup records for one account;
    # discovery returns BOTH (selecting the latest is a later step's job).
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_ig_rollup(data_root, tmp_path, slot="a", views=(100, 300))
    _write_ig_rollup(data_root, tmp_path, slot="b", views=(120, 320))

    found = discover_creator_metric_rollup_records(
        data_root, account_ledger=_ledger((IG_ACCOUNT, "instagram"))
    )

    assert set(found) == {IG_ACCOUNT}
    assert len(found[IG_ACCOUNT]) == 2
    # Two genuinely distinct records (different content), ready for latest-selection.
    assert len({record["content_hash"] for record in found[IG_ACCOUNT]}) == 2


def test_rejects_unsupported_platform(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    with pytest.raises(ValueError, match="unsupported"):
        discover_creator_metric_rollup_records(
            data_root, account_ledger=_ledger(("acct_th_001", "threads"))
        )
