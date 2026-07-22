from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from data_lake.canonical_json import canonical_record_bytes
from data_lake.creator_registry import (
    ADMISSION_LANE,
    CANDIDATE_ADMISSION_LANE,
    CANDIDATE_RETRACTION_LANE,
    CreatorRegistryLakeError,
    admit_tiktok_creator_account,
    admit_tiktok_creator_candidate,
    deterministic_platform_account_id,
    load_current_creator_profiles,
    load_current_creator_registry,
    load_current_registry_preflight_view,
    migrate_legacy_registry,
    monitoring_eligible_accounts,
    publish_creator_registry_generation,
    retract_tiktok_creator_candidate,
)
from data_lake.root import DataLakeRoot, DataLakeRootError, raw_shard
from source_capture.tiktok.grid_packet import write_tiktok_grid_packet
from capture_spine.tiktok_creator_discovery_frontier.register_lake_writer import (
    load_creator_frontier_dispositions,
    write_creator_frontier_dispositions,
)
from runners import run_source_capture_tiktok_creator_onboarding as onboarding_runner
from runners.run_creator_registry_lake import main as registry_main


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


def _candidate_admit(root: DataLakeRoot, packet_id: str) -> dict:
    written = write_creator_frontier_dispositions(
        data_root=root,
        actions=[
            {
                "platform": "tiktok",
                "handle": "new.fragrance",
                "status": "eligible",
                "priority": "high",
                "reason_code": "owner_choice",
            }
        ],
        recorded_at="2026-07-21T12:01:00Z",
    )
    disposition = written["current"]["creator_frontier_disposition_current"][
        "dispositions"
    ][0]
    return admit_tiktok_creator_candidate(
        data_root=root,
        packet_id=packet_id,
        frontier_disposition_id=disposition["disposition_id"],
    )


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


def test_existing_v1_generation_does_not_collide_with_v3_rebuild(tmp_path: Path) -> None:
    root = _root(tmp_path)
    migrated = _migrate(root)
    registry_root = root.path / "indexes" / "derived_retrieval" / "creator_registry"
    v3_generation = Path(migrated["generation_root"])
    v3_manifest = json.loads(
        (v3_generation / "manifests" / "creator_registry_generation_v3.json").read_text(
            encoding="utf-8"
        )
    )
    legacy_generation_id = "crg_" + v3_manifest["authority_inventory_sha256"][:24]
    assert legacy_generation_id != migrated["generation_id"]

    legacy_generation = registry_root / "generations" / legacy_generation_id
    (legacy_generation / "query_tables").mkdir(parents=True)
    (legacy_generation / "profiles").mkdir()
    (legacy_generation / "manifests").mkdir()
    (legacy_generation / "query_tables" / "creator_registry_index_v1.json").write_bytes(
        (v3_generation / "query_tables" / "creator_registry_index_v1.json").read_bytes()
    )
    (legacy_generation / "profiles" / "creator_profile_public_v1.json").write_bytes(
        (v3_generation / "profiles" / "creator_profile_public_v1.json").read_bytes()
    )
    (legacy_generation / "manifests" / "creator_registry_generation_v1.json").write_bytes(
        canonical_record_bytes(
            {
                "schema_version": "creator_registry_generation_v1",
                "generation_id": legacy_generation_id,
                "authority_inventory_sha256": v3_manifest[
                    "authority_inventory_sha256"
                ],
            }
        )
    )
    legacy_before = {
        path.relative_to(legacy_generation).as_posix(): path.read_bytes()
        for path in legacy_generation.rglob("*")
        if path.is_file()
    }
    (registry_root / "CURRENT").write_bytes(
        canonical_record_bytes(
            {"pointer_schema_version": 1, "generation_id": legacy_generation_id}
        )
    )
    shutil.rmtree(v3_generation)

    dry = publish_creator_registry_generation(root, dry_run=True)
    assert dry["generation_id"] == migrated["generation_id"]
    assert dry["would_write_generation"] is True
    assert dry["would_update_pointer"] is True
    assert not v3_generation.exists()

    rebuilt = publish_creator_registry_generation(root)
    assert rebuilt["generation_id"] == migrated["generation_id"]
    assert v3_generation.is_dir()
    pointer = json.loads((registry_root / "CURRENT").read_text(encoding="utf-8"))
    assert pointer == {
        "pointer_schema_version": 3,
        "generation_id": migrated["generation_id"],
    }
    assert legacy_before == {
        path.relative_to(legacy_generation).as_posix(): path.read_bytes()
        for path in legacy_generation.rglob("*")
        if path.is_file()
    }
    assert load_current_creator_registry(root)["creator_registry_index"][
        "counts"
    ]["platform_accounts_total"] == migrated["platform_accounts_total"]


def test_generation_and_existing_baseline_dry_runs_are_read_only(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _root(tmp_path)
    _migrate(root)
    # repo_root=None keeps the readonly resolve usable on a `for_test` root, which
    # may legitimately live inside the working tree (see DataLakeRoot.for_test).
    readonly = DataLakeRoot.resolve_readonly(explicit=root.path, repo_root=None)
    assert readonly.readonly is True

    def snapshot() -> dict[str, tuple[bytes, int] | None]:
        # Directories are included so a dry run that only creates an empty
        # directory is caught too, not just one that writes bytes.
        return {
            path.relative_to(root.path).as_posix(): (
                (path.read_bytes(), path.stat().st_mtime_ns) if path.is_file() else None
            )
            for path in root.path.rglob("*")
        }

    before = snapshot()
    dry = publish_creator_registry_generation(readonly, dry_run=True)
    assert dry["would_write_generation"] is False
    assert dry["would_update_pointer"] is False
    migrated = migrate_legacy_registry(
        data_root=readonly,
        account_ledger_path=LEGACY_ROOT / "creator_public_handle_linkage_ledger_v0.json",
        registry_index_path=LEGACY_ROOT / "creator_registry_index_v0.json",
        profile_current_path=LEGACY_ROOT / "creator_profile_current_view_v0.json",
        dry_run=True,
    )
    assert migrated["status"] == "dry_run_passed"
    assert migrated["would_write_authority"] is False
    assert snapshot() == before

    assert registry_main(
        ["rebuild", "--data-root", str(root.path), "--dry-run"]
    ) == 0
    cli = json.loads(capsys.readouterr().out)
    assert cli["status"] == "dry_run_passed"
    assert cli["would_write_generation"] is False
    assert cli["would_update_pointer"] is False
    assert snapshot() == before

    with pytest.raises(SystemExit):
        registry_main(["rebuild", "--data-root", str(root.path)])
    with pytest.raises(DataLakeRootError, match="read-only"):
        publish_creator_registry_generation(readonly)


def test_validated_tiktok_admission_is_idempotent_and_client_safe(tmp_path: Path) -> None:
    root = _root(tmp_path)
    _migrate(root)
    packet_id, outcome_path, account_id = _packet_and_outcome(root)
    candidate = _candidate_admit(root, packet_id)
    assert candidate["status"] == "admitted"

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
    assert rows[0]["onboarding"]["onboarding_state"] == "onboarded"
    assert rows[0]["capture_state"] == "identity_observed_content_packet_available"
    assert (
        rows[0]["routing_decision"]
        == "dedupe_exact_platform_account_then_attach_new_discovery_evidence"
    )
    assert rows[0]["source_pointers"] == [
        outcome_path.resolve().relative_to(root.path.resolve()).as_posix()
    ]
    assert not [
        claim
        for claim in rows[0]["non_claims"]
        if claim in {"not onboarded", "not monitoring eligible", "not public profile admission"}
    ]
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
    candidates = list((root.path / "derived").glob(f"*/*/{CANDIDATE_ADMISSION_LANE}/*"))
    assert len(candidates) == 1


def test_validated_admission_content_id_and_native_identity_fail_closed(
    tmp_path: Path,
) -> None:
    root = _root(tmp_path)
    _migrate(root)
    packet_id, outcome_path, _account_id = _packet_and_outcome(root)
    _candidate_admit(root, packet_id)
    admit_tiktok_creator_account(
        data_root=root,
        packet_id=packet_id,
        judgment_outcome_path=outcome_path,
    )

    admission_path = next((root.path / "derived").glob(f"*/*/{ADMISSION_LANE}/*"))
    admission = json.loads(admission_path.read_text(encoding="utf-8"))
    admission["platform_account"]["platform_public_account_id_or_none"] = "112233445566"
    admission_path.write_bytes(canonical_record_bytes(admission))
    with pytest.raises(CreatorRegistryLakeError, match="content id mismatch"):
        load_current_creator_registry(root)

    payload = {key: value for key, value in admission.items() if key != "record_id"}
    admission["record_id"] = (
        "cra_" + hashlib.sha256(canonical_record_bytes(payload)).hexdigest()[:24]
    )
    rebound_path = admission_path.with_name(admission["record_id"])
    admission_path.rename(rebound_path)
    rebound_path.write_bytes(canonical_record_bytes(admission))
    with pytest.raises(CreatorRegistryLakeError, match="identity differs from its grid packet"):
        load_current_creator_registry(root)


def test_cold_rebuild_is_byte_identical_and_stale_current_fails_closed(tmp_path: Path) -> None:
    root = _root(tmp_path)
    _migrate(root)
    packet_id, outcome_path, _account_id = _packet_and_outcome(root)
    _candidate_admit(root, packet_id)
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


def test_candidate_admission_is_internal_unmonitored_and_non_public(tmp_path: Path) -> None:
    root = _root(tmp_path)
    _migrate(root)
    packet_id, _outcome_path, account_id = _packet_and_outcome(root)

    first = _candidate_admit(root, packet_id)
    second = _candidate_admit(root, packet_id)

    assert first["status"] == "admitted"
    assert second["status"] == "already_current"
    rows = [
        row
        for row in load_current_creator_registry(root)["creator_registry_index"][
            "platform_accounts"
        ]
        if row["platform_account_id"] == account_id
    ]
    assert len(rows) == 1
    assert rows[0]["onboarding"]["onboarding_state"] == "not_onboarded"
    assert rows[0]["monitoring_eligibility"]["eligible"] is False
    assert all(
        row["profile_subject_id"] != account_id
        for row in load_current_creator_profiles(root)["creator_profile_public"]["profiles"]
    )


def test_candidate_retraction_removes_current_registry_and_is_idempotent(
    tmp_path: Path,
) -> None:
    root = _root(tmp_path)
    _migrate(root)
    packet_id, _outcome_path, account_id = _packet_and_outcome(root)
    _candidate_admit(root, packet_id)
    write_creator_frontier_dispositions(
        data_root=root,
        actions=[
            {
                "platform": "tiktok",
                "handle": "new.fragrance",
                "status": "deferred",
                "reason_code": "owner_choice",
                "reconsideration": "owner_reopen",
            }
        ],
        recorded_at="2026-07-21T12:02:00Z",
    )

    first = retract_tiktok_creator_candidate(
        data_root=root, public_handle="@New.Fragrance"
    )
    second = retract_tiktok_creator_candidate(
        data_root=root, public_handle="new.fragrance"
    )

    assert first["status"] == "retracted"
    assert second["status"] == "already_current"
    assert second["record_id"] == first["record_id"]
    assert second["generation_id"] == first["generation_id"]
    assert not any(
        row["platform_account_id"] == account_id
        for row in load_current_creator_registry(root)["creator_registry_index"][
            "platform_accounts"
        ]
    )
    assert not any(
        row["profile_subject_id"] == account_id
        for row in load_current_creator_profiles(root)["creator_profile_public"][
            "profiles"
        ]
    )
    assert not onboarding_runner.eligible_creator_onboarding_candidates(
        load_current_registry_preflight_view(root), platform="tiktok"
    )
    assert len(list((root.path / "derived").glob(f"*/*/{CANDIDATE_RETRACTION_LANE}/*"))) == 1
    manifest = json.loads(
        (
            Path(first["generation_root"])
            / "manifests"
            / "creator_registry_generation_v3.json"
        ).read_text(encoding="utf-8")
    )
    assert any(
        f"/{CANDIDATE_RETRACTION_LANE}/" in row["record_ref"]
        for row in manifest["authority_refs"]
    )


def test_candidate_retraction_requires_current_block_and_rejects_validated(
    tmp_path: Path,
) -> None:
    root = _root(tmp_path)
    _migrate(root)
    packet_id, outcome_path, _account_id = _packet_and_outcome(root)
    _candidate_admit(root, packet_id)

    with pytest.raises(CreatorRegistryLakeError, match="current deferred or rejected"):
        retract_tiktok_creator_candidate(
            data_root=root, public_handle="new.fragrance"
        )
    assert not list(
        (root.path / "derived").glob(f"*/*/{CANDIDATE_RETRACTION_LANE}/*")
    )

    admit_tiktok_creator_account(
        data_root=root,
        packet_id=packet_id,
        judgment_outcome_path=outcome_path,
    )
    write_creator_frontier_dispositions(
        data_root=root,
        actions=[
            {
                "platform": "tiktok",
                "handle": "new.fragrance",
                "status": "deferred",
                "reason_code": "owner_choice",
                "reconsideration": "owner_reopen",
            }
        ],
        recorded_at="2026-07-21T12:02:00Z",
    )
    with pytest.raises(CreatorRegistryLakeError, match="validated or onboarded"):
        retract_tiktok_creator_candidate(
            data_root=root, public_handle="new.fragrance"
        )


def test_candidate_retraction_missing_target_fails_closed(tmp_path: Path) -> None:
    root = _root(tmp_path)
    _migrate(root)
    packet_id, _outcome_path, _account_id = _packet_and_outcome(root)
    _candidate_admit(root, packet_id)
    written = write_creator_frontier_dispositions(
        data_root=root,
        actions=[
            {
                "platform": "tiktok",
                "handle": "new.fragrance",
                "status": "deferred",
                "reason_code": "owner_choice",
                "reconsideration": "owner_reopen",
            }
        ],
        recorded_at="2026-07-21T12:02:00Z",
    )
    disposition = written["current"]["creator_frontier_disposition_current"][
        "dispositions"
    ][0]
    payload = {
        "schema_version": "creator_registry_candidate_retraction_v1",
        "raw_anchor": packet_id,
        "retracted_at": disposition["recorded_at"],
        "platform_account_id": "acct_tiktok_missing",
        "public_handle": "new.fragrance",
        "candidate_admission": {
            "record_id": "crc_missing",
            "record_ref": "derived/000/missing/creator_registry_candidate_admission/crc_missing",
            "record_sha256": "0" * 64,
        },
        "frontier_disposition": {
            "disposition_id": disposition["disposition_id"],
            "candidate_key": disposition["candidate_key"],
            "record_ref": disposition["authority_record_ref"],
            "record_sha256": disposition["authority_record_sha256"],
        },
    }
    record_id = "crr_" + hashlib.sha256(canonical_record_bytes(payload)).hexdigest()[:24]
    root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=CANDIDATE_RETRACTION_LANE,
        record_id=record_id,
        data=canonical_record_bytes({"record_id": record_id, **payload}),
    )
    with pytest.raises(CreatorRegistryLakeError, match="missing or changed"):
        load_current_creator_registry(root)


def test_validated_admission_requires_registry_candidate_and_current_route(tmp_path: Path) -> None:
    root = _root(tmp_path)
    _migrate(root)
    packet_id, outcome_path, _account_id = _packet_and_outcome(root)

    with pytest.raises(CreatorRegistryLakeError, match="Registry not_onboarded"):
        admit_tiktok_creator_account(
            data_root=root,
            packet_id=packet_id,
            judgment_outcome_path=outcome_path,
        )

    _candidate_admit(root, packet_id)
    write_creator_frontier_dispositions(
        data_root=root,
        actions=[
            {
                "platform": "tiktok",
                "handle": "new.fragrance",
                "status": "deferred",
                "reason_code": "owner_choice",
                "reconsideration": "owner_reopen",
            }
        ],
        recorded_at="2026-07-21T12:02:00Z",
    )
    with pytest.raises(CreatorRegistryLakeError, match="blocked by the current Frontier"):
        admit_tiktok_creator_account(
            data_root=root,
            packet_id=packet_id,
            judgment_outcome_path=outcome_path,
        )


def test_browser_free_temporary_lake_candidate_dogfood(tmp_path: Path) -> None:
    root = _root(tmp_path)
    _migrate(root)
    packet_id, _outcome_path, account_id = _packet_and_outcome(root)
    _candidate_admit(root, packet_id)

    internal = load_current_creator_registry(root)["creator_registry_index"]
    candidate = next(
        row for row in internal["platform_accounts"] if row["platform_account_id"] == account_id
    )
    public = load_current_creator_profiles(root)["creator_profile_public"]
    assert candidate["onboarding"]["onboarding_state"] == "not_onboarded"
    assert candidate["monitoring_eligibility"]["eligible"] is False
    assert not any(row["profile_subject_id"] == account_id for row in public["profiles"])

    preflight = load_current_registry_preflight_view(root)
    handle, selected = onboarding_runner._resolve_creator_handle(
        creator_handle=None,
        creator_intent="new_onboarding",
        registry_document=preflight,
        frontier_dispositions=load_creator_frontier_dispositions(root),
    )
    assert handle == "new.fragrance"
    assert selected["platform_account_id"] == account_id

    write_creator_frontier_dispositions(
        data_root=root,
        actions=[
            {
                "platform": "tiktok",
                "handle": "new.fragrance",
                "status": "deferred",
                "reason_code": "owner_choice",
                "reconsideration": "owner_reopen",
            }
        ],
        recorded_at="2026-07-21T12:02:00Z",
    )
    with pytest.raises(ValueError, match="no actionable not_onboarded"):
        onboarding_runner._resolve_creator_handle(
            creator_handle=None,
            creator_intent="new_onboarding",
            registry_document=load_current_registry_preflight_view(root),
            frontier_dispositions=load_creator_frontier_dispositions(root),
        )
