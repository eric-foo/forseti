from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from data_lake.canonical_json import canonical_record_bytes
from data_lake.creator_registry import (
    ADMISSION_LANE,
    CreatorRegistryLakeError,
    admit_tiktok_creator_account,
    deterministic_platform_account_id,
    load_current_creator_profiles,
    load_current_creator_registry,
    migrate_legacy_registry,
    monitoring_eligible_accounts,
    publish_creator_registry_generation,
)
from data_lake.root import DataLakeRoot, raw_shard
from source_capture.tiktok.grid_packet import write_tiktok_grid_packet


REPO_ROOT = Path(__file__).resolve().parents[3]
LEGACY_ROOT = (
    REPO_ROOT
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_registry"
)


def _root(tmp_path: Path) -> DataLakeRoot:
    return DataLakeRoot.for_test(tmp_path / "forseti-data")


def _migrate(root: DataLakeRoot, *, dry_run: bool = False) -> dict:
    return migrate_legacy_registry(
        data_root=root,
        account_ledger_path=LEGACY_ROOT / "creator_public_handle_linkage_ledger_v0.json",
        registry_index_path=LEGACY_ROOT / "creator_registry_index_v0.json",
        profile_current_path=LEGACY_ROOT / "creator_profile_current_view_v0.json",
        dry_run=dry_run,
    )


def _grid_bytes(handle: str = "new.fragrance", native_id: str = "998877665544") -> bytes:
    payload = {
        "schema_version": "tiktok_creator_grid_window_v1",
        "creator_handle": handle,
        "complete": True,
        "window_size": 1,
        "window_cap": 30,
        "minimum_window_size": 1,
        "items": [
            {
                "video_id": "7777777777777777777",
                "video_url": f"https://www.tiktok.com/@{handle}/video/7777777777777777777",
                "author": {
                    "id": native_id,
                    "uniqueId": handle,
                    "nickname": "New Fragrance",
                },
            }
        ],
        "collection_receipt": {"capture_timestamp": "2026-07-21T12:00:00Z"},
    }
    return canonical_record_bytes(payload)


def _packet_and_outcome(root: DataLakeRoot) -> tuple[str, Path, str]:
    _exit, output = write_tiktok_grid_packet(
        grid_window_json=_grid_bytes(),
        data_root=root,
        observed_at_utc="2026-07-21T12:00:00Z",
    )
    packet_id = Path(output).name
    account_id = deterministic_platform_account_id("tiktok", "998877665544")
    snapshot = {
        "schema_version": "creator_audience_triangulation_snapshot_v1",
        "snapshot_id": "cats_test_new_fragrance",
        "profile_subject_kind": "platform_account",
        "profile_subject_id": account_id,
        "platform_account_id": account_id,
        "creator_id": "tiktok:@new.fragrance",
        "platform_scope": "tiktok",
        "generated_at": "2026-07-21T12:05:00Z",
        "evidence_cutoff": "2026-07-21T12:00:00Z",
        "input_bundle_id": "caeb_test_new_fragrance",
        "input_bundle_hash": "sha256:" + "1" * 64,
        "judgment_claim_set": {"claims": [], "agreements": [], "contradictions": [], "missing_evidence": []},
        "creator_signal_projection": {},
        "actual_audience_demographics": "not_estimated",
        "limitations": ["test evidence window"],
        "non_claims": ["not campaign performance"],
    }
    outcome = {
        "schema_version": "creator_audience_judgment_outcome_v1",
        "record_id": "cajo_test_new_fragrance",
        "raw_anchor": packet_id,
        "status": "validated",
        "creator_id": "tiktok:@new.fragrance",
        "profile_subject_id": account_id,
        "bundle_id": snapshot["input_bundle_id"],
        "bundle_hash": snapshot["input_bundle_hash"],
        "snapshot_id_or_none": snapshot["snapshot_id"],
        "snapshot_or_none": snapshot,
    }
    path = root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane="creator_audience_judgment_outcome",
        record_id=outcome["record_id"],
        data=canonical_record_bytes(outcome),
    )
    return packet_id, path, account_id


def test_migration_dry_run_does_not_write_and_write_preserves_account_set(tmp_path: Path) -> None:
    root = _root(tmp_path)
    dry = _migrate(root, dry_run=True)
    assert dry["status"] == "dry_run_passed"
    assert dry["parity"]["account_id_sets_equal"] is True
    assert not (root.path / "indexes" / "derived_retrieval" / "creator_registry" / "CURRENT").exists()

    migrated = _migrate(root)
    assert migrated["status"] == "migrated"
    index = load_current_creator_registry(root)["creator_registry_index"]
    public = load_current_creator_profiles(root)["creator_profile_public"]
    assert len(index["platform_accounts"]) == dry["parity"]["platform_accounts_total"]
    assert len(public["profiles"]) == dry["parity"]["profiles_total"]


def test_validated_tiktok_admission_is_idempotent_and_client_safe(tmp_path: Path) -> None:
    root = _root(tmp_path)
    _migrate(root)
    packet_id, outcome_path, account_id = _packet_and_outcome(root)

    first = admit_tiktok_creator_account(
        data_root=root,
        packet_id=packet_id,
        judgment_outcome_path=outcome_path,
    )
    second = admit_tiktok_creator_account(
        data_root=root,
        packet_id=packet_id,
        judgment_outcome_path=outcome_path,
    )
    assert first["status"] == "admitted"
    assert second["status"] == "already_current"

    index = load_current_creator_registry(root)["creator_registry_index"]
    rows = [row for row in index["platform_accounts"] if row["platform_account_id"] == account_id]
    assert len(rows) == 1
    assert rows[0]["monitoring_eligibility"] == {
        "eligible": True,
        "reason": "validated_onboarding_admission",
        "scheduled": False,
    }
    eligible = monitoring_eligible_accounts(root, platform="tiktok")
    assert sum(row["platform_account_id"] == account_id for row in eligible) == 1

    public = load_current_creator_profiles(root)
    profiles = [
        row
        for row in public["creator_profile_public"]["profiles"]
        if row["profile_subject_id"] == account_id
    ]
    assert len(profiles) == 1
    assert profiles[0]["audience_triangulation"]["snapshot_id"] == "cats_test_new_fragrance"
    rendered = json.dumps(public)
    assert "onboarding" not in rendered
    assert "monitoring_eligibility" not in rendered
    assert "response_bytes_b64" not in rendered
    assert "F:\\" not in rendered

    admissions = list((root.path / "derived").glob(f"*/*/{ADMISSION_LANE}/*"))
    assert len(admissions) == 1


def test_cold_rebuild_is_byte_identical_and_stale_current_fails_closed(tmp_path: Path) -> None:
    root = _root(tmp_path)
    _migrate(root)
    packet_id, outcome_path, _account_id = _packet_and_outcome(root)
    admitted = admit_tiktok_creator_account(
        data_root=root,
        packet_id=packet_id,
        judgment_outcome_path=outcome_path,
    )
    generation = Path(admitted["generation_root"])
    before = {path.relative_to(generation).as_posix(): path.read_bytes() for path in generation.rglob("*") if path.is_file()}
    rebuilt = publish_creator_registry_generation(root)
    assert rebuilt["generation_id"] == admitted["generation_id"]
    after = {path.relative_to(generation).as_posix(): path.read_bytes() for path in generation.rglob("*") if path.is_file()}
    assert after == before

    outcome = json.loads(outcome_path.read_text(encoding="utf-8"))
    extra = {
        "schema_version": "creator_registry_account_admission_v1",
        "record_id": "cra_unpublished_test",
        "raw_anchor": packet_id,
        "admitted_at": "2026-07-21T12:05:00Z",
        "platform_account": {
            "platform_account_id": "acct_tiktok_unpublished",
            "platform": "tiktok",
            "platform_public_account_id_or_none": "111111111111",
            "public_handle": "unpublished.fragrance",
            "public_profile_url": "https://www.tiktok.com/@unpublished.fragrance",
            "handle_source_pointer": "raw/test",
            "handle_observed_at": "2026-07-21T12:00:00Z",
            "public_display_name_or_none": "Unpublished Fragrance",
            "display_name_source_pointer_or_none": "raw/test",
            "display_name_source_field_or_none": "items[0].author.nickname",
        },
        "onboarding": {"onboarding_state": "onboarded"},
        "judgment": {
            "record_id": outcome["record_id"],
            "record_ref": outcome_path.relative_to(root.path).as_posix(),
            "record_sha256": hashlib.sha256(outcome_path.read_bytes()).hexdigest(),
        },
        "snapshot": outcome["snapshot_or_none"],
        "monitoring_eligible": True,
    }
    root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=ADMISSION_LANE,
        record_id=extra["record_id"],
        data=canonical_record_bytes(extra),
    )
    with pytest.raises(CreatorRegistryLakeError):
        load_current_creator_registry(root)
