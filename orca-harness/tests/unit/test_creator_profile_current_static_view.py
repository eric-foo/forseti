from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from capture_spine.creator_profile_current.ideal_audience_snapshot import (
    build_creator_ideal_audience_profile_snapshot_from_evidence,
    build_creator_ideal_audience_snapshot_document,
    dump_creator_ideal_audience_snapshot_document,
)
from capture_spine.creator_profile_current.materialize import (
    build_creator_profile_current_view_from_files,
)
from capture_spine.creator_profile_current.validation import (
    CREATOR_PROFILE_CURRENT_VIEW_SCHEMA_VERSION,
    CreatorProfileCurrentError,
    load_creator_profile_current_view,
    validate_creator_profile_current_view,
)
from schemas.audience_inference_models import EvidenceRecord, ModalityFamily, OutputField


ROOT = Path(__file__).resolve().parents[3]
VIEW_PATH = (
    ROOT
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_registry"
    / "creator_profile_current_view_v0.json"
)
ACCOUNT_LEDGER_PATH = (
    ROOT
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_registry"
    / "creator_public_handle_linkage_ledger_v0.json"
)
YOUTUBE_METRIC_SEED_PATH = (
    ROOT
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "youtube"
    / "youtube_shorts_fragrance_creator_metric_seed_v0.json"
)
YOUTUBE_SNAPSHOT_PATH = (
    ROOT
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "youtube"
    / "youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json"
)
INSTAGRAM_METRIC_SEED_PATH = (
    ROOT
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "instagram"
    / "instagram_reels_creator_metric_seed_v0.json"
)
# Lake cut-over §5/§8: the view's YT and IG rollups come from the committed lake
# snapshots; each seed stays the no-drift value oracle (see _metric_seeds below).
INSTAGRAM_SNAPSHOT_PATH = (
    ROOT
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "instagram"
    / "instagram_reels_creator_metric_rollup_snapshot_v0.json"
)
METRIC_SEED_PATHS = (YOUTUBE_SNAPSHOT_PATH, INSTAGRAM_SNAPSHOT_PATH)


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


def _audience_snapshot(subject_id: str, platform: str) -> dict:
    evidence = [
        EvidenceRecord(
            evidence_id=f"{subject_id}:audience:e1",
            creator_id=subject_id,
            platform=platform,
            post_id="audience-post-1",
            signal_id="tier1-test",
            modality=ModalityFamily.TEXT,
            target_field=OutputField.SEGMENT,
            label="fragrance_discovery",
            vote=1.0,
            base_reliability=1.0,
            extractor_confidence=1.0,
            creator_authored=True,
            source_pointer="for beginners",
        )
    ]
    return build_creator_ideal_audience_profile_snapshot_from_evidence(
        evidence,
        profile_subject_kind="platform_account",
        profile_subject_id=subject_id,
        platform_scope=platform,
        observation_window_start="2026-07-01T00:00:00Z",
        observation_window_end="2026-07-04T00:00:00Z",
        computed_at="2026-07-04T00:00:00Z",
    )


def _rollups_by_subject() -> dict[str, dict]:
    # Reconstruct from the view's ACTUAL rollup sources: both YT and IG from their
    # committed lake snapshots (§5/§8). Each snapshot is value-equal to its seed
    # (the no-drift bridge, proven by the equivalence gate) but carries fresher
    # provenance (e.g. computed_at), so the view-vs-source check must compare
    # against the snapshots, not the seeds.
    rollup_lists = [
        _json(YOUTUBE_SNAPSHOT_PATH)["creator_metric_rollup_snapshot"]["metric_rollups"],
        _json(INSTAGRAM_SNAPSHOT_PATH)["creator_metric_rollup_snapshot"]["metric_rollups"],
    ]
    rollups: dict[str, dict] = {}
    for rollup_list in rollup_lists:
        for rollup in rollup_list:
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
        "engagement_rate_observed_profiles": 31,
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
        # Engagement rate is posture/value coupled on every platform: observed
        # carries a numeric value, anything else carries null plus a reason.
        # (YT flipped to observed at cycle 2 via the watch-packet badge route;
        # platform-frozen pins here broke on every honest data refresh.)
        engagement_rate = rollup["metric_rollups"]["engagement_rate"]
        assert engagement_rate["posture"] in {"observed", "unavailable_with_reason"}
        if engagement_rate["posture"] == "observed":
            assert isinstance(engagement_rate["value_or_none"], (int, float))
        else:
            assert engagement_rate["value_or_none"] is None
            assert engagement_rate["posture_reason_or_none"]
        if platform == "instagram":
            assert engagement_rate["posture"] == "observed"
            assert rollup["metric_rollups"]["average_like_count"]["posture"] == "observed"
            assert rollup["metric_rollups"]["average_comment_count"]["posture"] == "observed"


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


def test_creator_profile_current_materializer_optionally_joins_ideal_audience_snapshot(tmp_path: Path) -> None:
    account = _account_ledger()["platform_accounts"][0]
    snapshot = _audience_snapshot(account["platform_account_id"], account["platform"])
    snapshot_document = build_creator_ideal_audience_snapshot_document(
        [snapshot],
        generated_at_utc=snapshot["computed_at"],
    )
    snapshot_path = tmp_path / "creator_ideal_audience_profile_snapshot_v0.json"
    snapshot_path.write_text(
        dump_creator_ideal_audience_snapshot_document(snapshot_document),
        encoding="utf-8",
        newline="\n",
    )

    generated = build_creator_profile_current_view_from_files(
        account_ledger_path=ACCOUNT_LEDGER_PATH,
        metric_seed_paths=METRIC_SEED_PATHS,
        audience_profile_snapshot_paths=(snapshot_path,),
        generated_at_utc=_view()["generated_at_utc"],
    )
    view = generated["creator_profile_current_view"]
    joined = next(
        profile
        for profile in view["profiles"]
        if profile["profile_subject_id"] == account["platform_account_id"]
    )

    assert view["counts"]["profiles_with_ideal_audience_profiles"] == 1
    assert joined["ideal_audience_profile"] == snapshot
    assert joined["freshness"]["audience_computed_at_or_none"] == snapshot["computed_at"]
    assert any("actual_audience remains not_estimated" in item for item in joined["limitations"])


def test_creator_profile_current_source_hashes_are_current() -> None:
    view = _view()
    inputs_by_pointer = {
        source_input["source_pointer"]: source_input
        for source_input in view["source_inputs"]
    }

    expected_paths = {
        "forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json": ACCOUNT_LEDGER_PATH,
        "forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json": YOUTUBE_SNAPSHOT_PATH,
        "forseti/product/spines/capture/core/source_families/social_media/instagram/instagram_reels_creator_metric_rollup_snapshot_v0.json": INSTAGRAM_SNAPSHOT_PATH,
    }

    assert set(inputs_by_pointer) == set(expected_paths)
    for pointer, path in expected_paths.items():
        assert inputs_by_pointer[pointer]["sha256"] == _sha256(path)


def test_creator_profile_source_input_files_are_lf_repo_text() -> None:
    source_pointers = {source["source_pointer"] for source in _view()["source_inputs"]}
    for seed in _metric_seeds():
        for source in seed["source_inputs"]:
            source_pointer = source["source_pointer"]
            if source_pointer.startswith(("docs/", "forseti/")):
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
            # YouTube engagement coverage is per-account capture reality (live
            # watch packets expose like_count widely, total comments rarely) --
            # the forbidden-scope guarantee is posture/value coupling, never a
            # platform-frozen capability pin or a zero-filled value.
            for name in ("average_like_count", "average_comment_count", "engagement_rate"):
                metric = rollup["metric_rollups"][name]
                if metric["posture"] == "observed":
                    assert metric["value_or_none"] is not None
                else:
                    assert metric["value_or_none"] is None
                    assert metric["posture_reason_or_none"]


def test_creator_profile_validator_rejects_non_observed_metric_zero_fill() -> None:
    document = _bad_view_document()
    rollup = document["creator_profile_current_view"]["profiles"][0]["current_metric_rollups"][0]
    # posting_cadence is not_attempted by recipe construction on every rollup,
    # so this stays a non-observed target across honest data refreshes
    # (engagement_rate stopped being one when YT turned observed at cycle 2).
    assert rollup["metric_rollups"]["posting_cadence"]["posture"] != "observed"
    rollup["metric_rollups"]["posting_cadence"]["value_or_none"] = 0

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


def test_creator_profile_validator_rejects_malformed_ideal_audience_profile() -> None:
    document = _bad_view_document()
    document["creator_profile_current_view"]["profiles"][0]["ideal_audience_profile"] = {"freeform": "young buyers"}
    document["creator_profile_current_view"]["counts"]["profiles_with_ideal_audience_profiles"] = 1

    _assert_validation_code(document, "invalid_ideal_audience_profile")


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
