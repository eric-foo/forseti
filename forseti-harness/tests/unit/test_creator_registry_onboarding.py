from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from capture_spine.creator_profile_current.creator_registry_onboarding import (
    CreatorRegistryOnboardingError,
    ONBOARDING_POLICY_VERSION,
    derive_onboarding_by_account,
    refresh_creator_registry_index_document,
)
from data_lake.root import DataLakeRoot
from data_lake.silver_record import append_raw_packet_tombstone
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet
from runners import run_creator_registry_onboarding_refresh as refresh_runner


def _account(
    account_id: str,
    *,
    platform: str,
    handle: str,
    native_id: str | None = None,
) -> dict:
    return {
        "platform_account_id": account_id,
        "platform": platform,
        "platform_public_account_id_or_none": native_id,
        "public_handle": handle,
        "public_profile_url": f"https://www.{platform}.com/@{handle}",
        "handle_source_pointer": "fixture.json#/handle",
        "handle_observed_at": "2026-07-15T00:00:00Z",
        "public_display_name_or_none": handle,
        "display_name_source_pointer_or_none": "fixture.json#/display_name",
        "display_name_source_field_or_none": "display_name",
    }


def _write_packet(
    tmp_path: Path,
    lake: DataLakeRoot,
    *,
    family: str,
    surface: str,
    filename: str,
    payload: dict,
):
    packet_input = tmp_path / filename
    packet_input.write_text(json.dumps(payload), encoding="utf-8")
    return write_local_source_capture_packet(
        data_root=lake,
        input_files=[packet_input],
        source_family=family,
        source_surface=surface,
        source_locator=known_fact("https://example.invalid/source"),
        decision_question="fixture onboarding evidence",
        capture_context="creator registry onboarding unit fixture",
        session_identity="fixture-session",
    )


def _youtube_payload(channel_id: str | None, *, schema: str = "youtube_watch_metadata_comments_capture_v1") -> dict:
    return {
        "capture_schema_version": schema,
        "platform": "youtube",
        "platform_video_id": "vid12345678",
        "packet": {"channel": {"channel_id": channel_id}},
    }


def test_rss_and_staging_do_not_onboard_but_committed_watch_packet_does(tmp_path: Path) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    account = _account(
        "acct_yt_new",
        platform="youtube",
        handle="fragrancecreator",
        native_id="UCexact",
    )

    # A staged packet-shaped directory is not committed Bronze and must be invisible.
    staged = tmp_path / "staging"
    staged.mkdir()
    (staged / "youtube_watch_capture.json").write_text(
        json.dumps(_youtube_payload("UCexact")), encoding="utf-8"
    )
    _write_packet(
        tmp_path,
        lake,
        family="youtube",
        surface="youtube_channel_rss_feed",
        filename="youtube_rss_feed.json",
        payload={"channel_id": "UCexact"},
    )

    before = derive_onboarding_by_account(data_root=lake, platform_accounts=[account])
    assert before["acct_yt_new"] == {
        "onboarding_state": "not_onboarded",
        "onboarded_at_or_none": None,
        "evidence_packet_id_or_none": None,
        "evidence_source_family_or_none": None,
        "evidence_source_surface_or_none": None,
        "earliest_public_post_at_or_none": None,
        "earliest_public_post_evidence_packet_id_or_none": None,
        "policy_version": ONBOARDING_POLICY_VERSION,
    }

    result = _write_packet(
        tmp_path,
        lake,
        family="youtube",
        surface="youtube_watch_metadata_comments",
        filename="youtube_watch_capture.json",
        payload=_youtube_payload("UCexact"),
    )
    after = derive_onboarding_by_account(data_root=lake, platform_accounts=[account])
    state = after["acct_yt_new"]
    assert state["onboarding_state"] == "onboarded"
    assert state["evidence_packet_id_or_none"] == result.packet.packet_id
    assert state["evidence_source_surface_or_none"] == "youtube_watch_metadata_comments"
    assert state["onboarded_at_or_none"]


def test_tiktok_grid_matches_exact_same_platform_handle(tmp_path: Path) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    account = _account("acct_tt", platform="tiktok", handle="TopFrag.Official")
    result = _write_packet(
        tmp_path,
        lake,
        family="tiktok",
        surface="tiktok_creator_grid_window",
        filename="tiktok_grid_window.json",
        payload={"creator_handle": "topfrag.official"},
    )

    state = derive_onboarding_by_account(data_root=lake, platform_accounts=[account])["acct_tt"]
    assert state["onboarding_state"] == "onboarded"
    assert state["evidence_packet_id_or_none"] == result.packet.packet_id


def test_tiktok_batch_projects_earliest_public_post_with_exact_packet_lineage(
    tmp_path: Path,
) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    account = _account("acct_tt", platform="tiktok", handle="fragrancecreator")
    result = _write_packet(
        tmp_path,
        lake,
        family="tiktok",
        surface="tiktok_creator_batch_comment_subtitle_admission",
        filename="tiktok_batch_capture.json",
        payload={
            "capture_schema_version": "tiktok_batch_capture_admission_v2",
            "creator_handle": "fragrancecreator",
            "earliest_public_post_observation": {
                "status": "observed",
                "published_at_utc": "2021-04-03T12:34:56Z",
            },
        },
    )

    state = derive_onboarding_by_account(
        data_root=lake, platform_accounts=[account]
    )["acct_tt"]

    assert state["earliest_public_post_at_or_none"] == "2021-04-03T12:34:56Z"
    assert (
        state["earliest_public_post_evidence_packet_id_or_none"]
        == result.packet.packet_id
    )


def test_tombstoned_packet_is_excluded_from_onboarding_evidence(tmp_path: Path) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    account = _account("acct_tt", platform="tiktok", handle="ak.fragrances1")
    old = _write_packet(
        tmp_path,
        lake,
        family="tiktok",
        surface="tiktok_creator_grid_window",
        filename="old_tiktok_grid_window.json",
        payload={"creator_handle": "ak.fragrances1", "capture_marker": "old"},
    )
    retained = _write_packet(
        tmp_path,
        lake,
        family="tiktok",
        surface="tiktok_creator_grid_window",
        filename="latest_tiktok_grid_window.json",
        payload={"creator_handle": "ak.fragrances1", "capture_marker": "retained"},
    )
    append_raw_packet_tombstone(
        lake,
        retained_packet_id=retained.packet.packet_id,
        tombstoned_packet_id=old.packet.packet_id,
        captured_at="2026-07-16T18:42:39Z",
        reason="owner-directed cleanup of superseded testing history",
    )

    state = derive_onboarding_by_account(data_root=lake, platform_accounts=[account])["acct_tt"]

    assert state["onboarding_state"] == "onboarded"
    assert state["evidence_packet_id_or_none"] == retained.packet.packet_id


def test_ambiguous_registry_handle_fails_before_derivation(tmp_path: Path) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    accounts = [
        _account("acct_one", platform="tiktok", handle="same"),
        _account("acct_two", platform="tiktok", handle="SAME"),
    ]

    with pytest.raises(CreatorRegistryOnboardingError, match="ambiguous same-platform"):
        derive_onboarding_by_account(data_root=lake, platform_accounts=accounts)


def test_unsupported_qualifying_packet_schema_fails_loud(tmp_path: Path) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    account = _account("acct_yt", platform="youtube", handle="creator", native_id="UCexact")
    _write_packet(
        tmp_path,
        lake,
        family="youtube",
        surface="youtube_watch_metadata_comments",
        filename="youtube_watch_capture.json",
        payload=_youtube_payload("UCexact", schema="youtube_watch_capture_v99"),
    )

    with pytest.raises(CreatorRegistryOnboardingError, match="unsupported YouTube"):
        derive_onboarding_by_account(data_root=lake, platform_accounts=[account])


def test_unattributable_legacy_youtube_packet_does_not_fake_onboarding(tmp_path: Path) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    account = _account("acct_yt", platform="youtube", handle="creator", native_id="UCexact")
    _write_packet(
        tmp_path,
        lake,
        family="youtube",
        surface="youtube_watch_metadata_comments",
        filename="youtube_watch_capture.json",
        payload=_youtube_payload(None, schema="youtube_watch_metadata_comments_capture_v0"),
    )

    state = derive_onboarding_by_account(data_root=lake, platform_accounts=[account])["acct_yt"]
    assert state["onboarding_state"] == "not_onboarded"


def test_registry_refresh_appends_new_account_and_keeps_onboarding_separate_from_freshness() -> None:
    account = _account(
        "acct_yt_new",
        platform="youtube",
        handle="creator",
        native_id="UCexact",
    )
    current = {
        "creator_registry_index": {
            "schema_version": "creator_registry_index_v0",
            "index_id": "creator_registry_index_v0",
            "index_mode": "static_known_public_account_dedupe_index",
            "generated_at_utc": "2026-07-01T00:00:00Z",
            "source_policy_posture": "fixture",
            "authority_pointers": [],
            "source_inputs": [],
            "lookup_policy": {},
            "counts": {},
            "platform_accounts": [],
            "creator_records": [],
            "accepted_residuals": [],
            "non_claims": [],
        }
    }
    ledger = {"platform_accounts": [account], "creator_records": []}
    not_onboarded = {
        "acct_yt_new": {
            "onboarding_state": "not_onboarded",
            "onboarded_at_or_none": None,
            "evidence_packet_id_or_none": None,
            "evidence_source_family_or_none": None,
            "evidence_source_surface_or_none": None,
            "policy_version": ONBOARDING_POLICY_VERSION,
        }
    }

    refreshed = refresh_creator_registry_index_document(
        current_document=current,
        account_ledger=ledger,
        onboarding_by_account=not_onboarded,
        generated_at_utc="2026-07-15T00:00:00Z",
        data_root_uuid="root-fixture",
        account_ledger_sha256="0" * 64,
    )["creator_registry_index"]

    row = refreshed["platform_accounts"][0]
    assert row["capture_state"] == "never_captured"
    assert row["freshness"]["last_capture_observed_at_or_none"] is None
    assert row["onboarding"]["onboarding_state"] == "not_onboarded"
    assert refreshed["counts"]["platform_accounts_by_onboarding_state"] == {
        "not_onboarded": 1,
        "onboarded": 0,
    }


def test_projection_refresh_updates_registry_and_profile_without_erasing_audience(
    tmp_path: Path,
) -> None:
    lake = DataLakeRoot.for_test(tmp_path / "lake")
    index_path = tmp_path / "creator_registry_index_v0.json"
    ledger_path = tmp_path / "creator_public_handle_linkage_ledger_v0.json"
    profile_path = tmp_path / "creator_profile_current_view_v0.json"
    shutil.copy2(refresh_runner.DEFAULT_INDEX, index_path)
    shutil.copy2(refresh_runner.DEFAULT_LEDGER, ledger_path)
    shutil.copy2(refresh_runner.DEFAULT_PROFILE_VIEW, profile_path)

    before = json.loads(profile_path.read_text(encoding="utf-8"))[
        "creator_profile_current_view"
    ]
    before_audience_joins = sum(
        1 for profile in before["profiles"] if profile["audience_triangulation"]
    )

    result = refresh_runner.refresh_creator_registry_projections(
        data_root=lake,
        index_path=index_path,
        account_ledger_path=ledger_path,
        profile_view_path=profile_path,
    )

    refreshed_index = json.loads(index_path.read_text(encoding="utf-8"))[
        "creator_registry_index"
    ]
    refreshed_profile = json.loads(profile_path.read_text(encoding="utf-8"))[
        "creator_profile_current_view"
    ]
    assert refreshed_index["counts"]["platform_accounts_by_onboarding_state"] == {
        "not_onboarded": len(refreshed_index["platform_accounts"]),
        "onboarded": 0,
    }
    assert refreshed_profile["counts"]["not_onboarded_profiles"] == len(
        refreshed_profile["profiles"]
    )
    assert refreshed_profile["counts"]["onboarded_profiles"] == 0
    assert refreshed_profile["counts"]["profiles_with_audience_triangulation"] == (
        before_audience_joins
    )
    assert result["retained_audience_join_count"] == before_audience_joins
