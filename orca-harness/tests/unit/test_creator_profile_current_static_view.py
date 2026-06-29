from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from capture_spine.creator_profile_current.materialize import (
    build_creator_profile_current_view_from_files,
)
from capture_spine.creator_profile_current.validation import (
    CREATOR_PROFILE_CURRENT_VIEW_SCHEMA_VERSION,
    CreatorProfileCurrentError,
    load_creator_profile_current_view,
    validate_creator_profile_current_view,
)


ROOT = Path(__file__).resolve().parents[3]
VIEW_PATH = (
    ROOT
    / "orca"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_profile_current_view_v0.json"
)
ACCOUNT_LEDGER_PATH = (
    ROOT
    / "orca"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_public_handle_linkage_ledger_v0.json"
)
YOUTUBE_METRIC_SEED_PATH = (
    ROOT
    / "orca"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "youtube"
    / "youtube_shorts_fragrance_creator_metric_seed_v0.json"
)
INSTAGRAM_METRIC_SEED_PATH = (
    ROOT
    / "orca"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "instagram"
    / "instagram_reels_creator_metric_seed_v0.json"
)
METRIC_SEED_PATHS = (YOUTUBE_METRIC_SEED_PATH, INSTAGRAM_METRIC_SEED_PATH)


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _view_document() -> dict:
    return _json(VIEW_PATH)


def _view() -> dict:
    return _view_document()["creator_profile_current_view"]


def _account_ledger() -> dict:
    return _json(ACCOUNT_LEDGER_PATH)["creator_public_handle_linkage_ledger"]


def _metric_seeds() -> list[dict]:
    return [
        _json(YOUTUBE_METRIC_SEED_PATH)["youtube_shorts_fragrance_creator_metric_seed"],
        _json(INSTAGRAM_METRIC_SEED_PATH)["instagram_reels_creator_metric_seed"],
    ]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _git_check_attr(path: Path, attr: str) -> str:
    relpath = path.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ["git", "-C", str(ROOT), "check-attr", attr, "--", relpath],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip().rsplit(": ", 1)[-1]


def _bad_view_document() -> dict:
    return deepcopy(_view_document())


def _assert_validation_code(document: dict, code: str) -> None:
    with pytest.raises(CreatorProfileCurrentError) as exc_info:
        validate_creator_profile_current_view(document)
    assert exc_info.value.code == code


def _rollups_by_subject() -> dict[str, dict]:
    rollups: dict[str, dict] = {}
    for seed in _metric_seeds():
        for rollup in seed["metric_rollups"]:
            rollups[rollup["profile_subject_id"]] = rollup
    return rollups


def test_creator_profile_current_reusable_validator_accepts_current_fixture() -> None:
    document = load_creator_profile_current_view(VIEW_PATH)
    assert document["creator_profile_current_view"]["schema_version"] == CREATOR_PROFILE_CURRENT_VIEW_SCHEMA_VERSION


def test_creator_profile_current_counts_and_boundaries() -> None:
    view = _view()
    validate_creator_profile_current_view(_view_document())

    assert view["schema_version"] == "creator_profile_current_view_v0"
    assert view["counts"] == {
        "profiles_total": 33,
        "platform_account_profiles": 33,
        "creator_record_profiles": 0,
        "profiles_with_metric_rollups": 33,
        "profiles_with_ideal_audience_profiles": 0,
        "engagement_rate_observed_profiles": 3,
        "cross_platform_rollup_profiles": 0,
    }
    assert {profile["platform_accounts"][0]["platform"] for profile in view["profiles"]} == {"youtube", "instagram"}

    for profile in view["profiles"]:
        platform = profile["platform_accounts"][0]["platform"]
        assert profile["profile_subject_kind"] == "platform_account"
        assert profile["profile_subject_id"] == profile["platform_account_id_or_none"]
        assert profile["creator_record_id_or_none"] is None
        assert profile["identity_state"] == "single_platform_observed"
        assert profile["link_state_or_none"] is None
        assert profile["review_state_or_none"] is None
        assert profile["ideal_audience_profile"] is None
        assert profile["wind_calling_summary"] is None
        assert len(profile["current_metric_rollups"]) == 1

        rollup = profile["current_metric_rollups"][0]
        assert rollup["platform_scope"] == platform
        assert rollup["freshness_state"] == "partial"
        assert rollup["metric_rollups"]["average_views"]["posture"] == "observed"
        assert rollup["metric_rollups"]["median_views"]["posture"] == "observed"
        assert rollup["sample_support"]["representativeness_posture"] == "admitted_pool_only_not_representative_creator_average"
        assert any("not a representative creator average" in item for item in rollup["limitations"])
        if platform == "instagram":
            assert rollup["metric_rollups"]["engagement_rate"]["posture"] == "observed"
            assert rollup["metric_rollups"]["average_like_count"]["posture"] == "observed"
            assert rollup["metric_rollups"]["average_comment_count"]["posture"] == "observed"
        else:
            assert rollup["metric_rollups"]["engagement_rate"]["posture"] == "unavailable_with_reason"


def test_creator_profile_current_rebuilds_from_identity_and_metric_seeds() -> None:
    view = _view()
    account_ledger = _account_ledger()
    rollups_by_subject = _rollups_by_subject()

    accounts_by_id = {
        account["platform_account_id"]: account
        for account in account_ledger["platform_accounts"]
    }

    assert set(accounts_by_id) == set(rollups_by_subject)
    assert set(accounts_by_id) == {
        profile["profile_subject_id"] for profile in view["profiles"]
    }

    for profile in view["profiles"]:
        subject_id = profile["profile_subject_id"]
        account = accounts_by_id[subject_id]
        expected_rollup = rollups_by_subject[subject_id]
        actual_rollup = profile["current_metric_rollups"][0]

        assert profile["platform_accounts"] == [account]
        assert actual_rollup["metric_rollup_id"] == expected_rollup["metric_rollup_id"]
        assert actual_rollup["platform_account_ids"] == expected_rollup["platform_account_ids"]
        assert actual_rollup["rollup_window"] == expected_rollup["rollup_window"]
        assert actual_rollup["rollup_window_description"] == expected_rollup["rollup_window_description"]
        assert actual_rollup["metric_rollups"] == expected_rollup["metric_rollups"]
        assert actual_rollup["source_metric_observation_ids"] == expected_rollup["source_metric_observation_ids"]
        assert actual_rollup["sample_support"] == expected_rollup["sample_support"]
        assert actual_rollup["limitations"] == expected_rollup["limitations"]
        assert actual_rollup["observation_count"] == expected_rollup["observation_count"]
        assert actual_rollup["computed_at"] == expected_rollup["computed_at"]
        assert profile["freshness"]["identity_updated_at"] == account["handle_observed_at"]
        assert profile["freshness"]["metrics_computed_at_or_none"] == expected_rollup["computed_at"]


def test_creator_profile_current_materializer_matches_checked_in_view() -> None:
    generated = build_creator_profile_current_view_from_files(
        account_ledger_path=ACCOUNT_LEDGER_PATH,
        metric_seed_paths=METRIC_SEED_PATHS,
        generated_at_utc=_view()["generated_at_utc"],
    )

    assert generated == _view_document()


def test_creator_profile_current_source_hashes_are_current() -> None:
    view = _view()
    inputs_by_pointer = {
        source_input["source_pointer"]: source_input
        for source_input in view["source_inputs"]
    }

    expected_paths = {
        "orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_v0.json": ACCOUNT_LEDGER_PATH,
        "orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_seed_v0.json": YOUTUBE_METRIC_SEED_PATH,
        "orca/product/spines/capture/core/source_families/social_media/instagram/instagram_reels_creator_metric_seed_v0.json": INSTAGRAM_METRIC_SEED_PATH,
    }

    assert set(inputs_by_pointer) == set(expected_paths)
    for pointer, path in expected_paths.items():
        assert inputs_by_pointer[pointer]["sha256"] == _sha256(path)


def test_creator_profile_source_input_files_are_lf_repo_text() -> None:
    source_pointers = {source["source_pointer"] for source in _view()["source_inputs"]}
    for seed in _metric_seeds():
        for source in seed["source_inputs"]:
            source_pointer = source["source_pointer"]
            if source_pointer.startswith(("docs/", "orca/")):
                source_pointers.add(source_pointer)

    for source_pointer in sorted(source_pointers):
        source_path = ROOT / source_pointer.split("#", 1)[0]
        assert source_path.is_file()
        assert _git_check_attr(source_path, "text") == "set"
        assert _git_check_attr(source_path, "eol") == "lf"


def test_creator_profile_current_does_not_smuggle_forbidden_scope() -> None:
    view = _view()
    forbidden_claim_fragments = (
        "channel-wide creator influence",
        "engagement rate",
        "buyer proof",
        "cross-platform rollup",
    )

    for profile in view["profiles"]:
        platform = profile["platform_accounts"][0]["platform"]
        non_claims = " ".join(profile["non_claims"])
        for fragment in forbidden_claim_fragments:
            assert fragment in non_claims

        assert "not SQLite or data-lake physicalization" in profile["non_claims"]
        assert any("sample_support" in item for item in profile["limitations"])
        rollup = profile["current_metric_rollups"][0]
        if platform == "instagram":
            assert rollup["metric_rollups"]["average_like_count"]["value_or_none"] is not None
            assert rollup["metric_rollups"]["average_comment_count"]["value_or_none"] is not None
            assert rollup["metric_rollups"]["engagement_rate"]["value_or_none"] is not None
        else:
            assert rollup["metric_rollups"]["average_like_count"]["value_or_none"] is None
            assert rollup["metric_rollups"]["average_comment_count"]["value_or_none"] is None
            assert rollup["metric_rollups"]["engagement_rate"]["value_or_none"] is None


def test_creator_profile_validator_rejects_non_observed_metric_zero_fill() -> None:
    document = _bad_view_document()
    rollup = document["creator_profile_current_view"]["profiles"][0]["current_metric_rollups"][0]
    rollup["metric_rollups"]["engagement_rate"]["value_or_none"] = 0

    _assert_validation_code(document, "metric_value_for_non_observed_posture")


def test_creator_profile_validator_rejects_missing_sample_support() -> None:
    document = _bad_view_document()
    rollup = document["creator_profile_current_view"]["profiles"][0]["current_metric_rollups"][0]
    del rollup["sample_support"]

    _assert_validation_code(document, "missing_sample_support")


def test_creator_profile_validator_rejects_metric_smuggling_into_identity_account() -> None:
    document = _bad_view_document()
    account = document["creator_profile_current_view"]["profiles"][0]["platform_accounts"][0]
    account["average_views"] = 123

    _assert_validation_code(document, "unknown_field")


def test_creator_profile_validator_rejects_metric_smuggling_into_source_drill_back() -> None:
    document = _bad_view_document()
    drill_back = document["creator_profile_current_view"]["profiles"][0]["source_drill_back"]
    drill_back["average_views"] = 123

    _assert_validation_code(document, "unknown_field")


def test_creator_profile_validator_rejects_metric_smuggling_into_identity_evidence_summary() -> None:
    document = _bad_view_document()
    identity_summary = document["creator_profile_current_view"]["profiles"][0]["identity_evidence_summary"]
    identity_summary["engagement_rate"] = 0.42

    _assert_validation_code(document, "unknown_field")


def test_creator_profile_validator_rejects_unjoined_ideal_audience_profile() -> None:
    document = _bad_view_document()
    document["creator_profile_current_view"]["profiles"][0]["ideal_audience_profile"] = {"freeform": "young buyers"}
    document["creator_profile_current_view"]["counts"]["profiles_with_ideal_audience_profiles"] = 1

    _assert_validation_code(document, "unsupported_ideal_audience_profile")


def test_creator_profile_validator_rejects_unjoined_wind_calling_summary() -> None:
    document = _bad_view_document()
    document["creator_profile_current_view"]["profiles"][0]["wind_calling_summary"] = {"summary": "high"}

    _assert_validation_code(document, "unsupported_wind_calling_summary")


def test_creator_profile_validator_rejects_source_drill_back_observation_id_drift() -> None:
    document = _bad_view_document()
    drill_back = document["creator_profile_current_view"]["profiles"][0]["source_drill_back"]
    drill_back["source_metric_observation_ids"] = ["unrelated_observation_id"]

    _assert_validation_code(document, "source_drill_back_observation_ids_mismatch")


def test_creator_profile_validator_rejects_bool_observed_metric_value() -> None:
    document = _bad_view_document()
    rollup = document["creator_profile_current_view"]["profiles"][0]["current_metric_rollups"][0]
    rollup["metric_rollups"]["average_views"]["value_or_none"] = True

    _assert_validation_code(document, "observed_metric_missing_value")


def test_creator_profile_validator_requires_full_profile_non_claim_set() -> None:
    document = _bad_view_document()
    profile = document["creator_profile_current_view"]["profiles"][0]
    profile["non_claims"] = [
        non_claim
        for non_claim in profile["non_claims"]
        if non_claim != "not SQLite or data-lake physicalization"
    ]

    _assert_validation_code(document, "missing_required_non_claim")


def test_creator_profile_validator_rejects_cross_platform_rollup_without_promoted_linkage() -> None:
    document = _bad_view_document()
    rollup = document["creator_profile_current_view"]["profiles"][0]["current_metric_rollups"][0]
    rollup["platform_scope"] = "cross_platform"

    _assert_validation_code(document, "cross_platform_rollup_without_promoted_linkage")
