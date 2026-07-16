from __future__ import annotations

import base64
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
CREATOR_REGISTRY_INDEX_PATH = (
    ROOT
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_registry"
    / "creator_registry_index_v0.json"
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
AK_AUDIENCE_SNAPSHOT_PATH = (
    ROOT
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_registry"
    / "ak_fragrances1_creator_audience_triangulation_snapshot_v1.json"
)
AK_AUDIENCE_OUTCOME_PATH = (
    ROOT
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_registry"
    / "ak_fragrances1_creator_audience_judgment_outcome_v1.json"
)


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


def _audience_snapshot(subject_id: str) -> dict:
    claim = {
        "claim_id": "claim-1",
        "axis": "presentation_style_resonance",
        "statement": "Comparison-led spectacle resonates across captured videos.",
        "commercial_implication": "Use direct comparisons to make products memorable.",
        "modality": "fused",
        "relation": "agreement",
        "support_scope": "mixed_multi_video",
        "representative_evidence_ids": ["ttte-1", "ttce-1"],
        "all_support_evidence_ids": ["ttte-1", "ttce-1"],
        "counterevidence_ids": [],
        "source_video_ids": ["v1", "v2"],
        "limitation": "Captured videos and top-level comments only.",
    }
    point = {"statement": "Makes products impossible to ignore and easy to recall.", "claim_ids": ["claim-1"]}
    return {
        "schema_version": "creator_audience_triangulation_snapshot_v0",
        "snapshot_id": "cats_fixture",
        "profile_subject_kind": "platform_account",
        "profile_subject_id": subject_id,
        "platform_account_id": subject_id,
        "creator_id": "tiktok:@fixture",
        "platform_scope": "tiktok",
        "generated_at": "2026-07-04T00:00:00Z",
        "evidence_cutoff": "2026-07-04T00:00:00Z",
        "input_bundle_id": "caeb_fixture",
        "input_bundle_hash": "sha256:" + "a" * 64,
        "judgment_claim_set": {
            "claims": [claim],
            "agreements": [],
            "contradictions": [],
            "missing_evidence": [],
        },
        "creator_signal_projection": {
            "hire_verdict": point,
            "product_advantage": point,
            "creator_specific_execution": point,
            "observed_audience_response": point,
            "strongest_campaign_jobs": [point],
            "briefing_instructions": [point],
            "wrong_hire_boundary": point,
            "robustness_stamp": None,
        },
        "limitations": ["Captured comments are not a platform census."],
        "non_claims": ["not guaranteed conversion"],
        "actual_audience_demographics": "not_estimated",
    }


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
        "profiles_total": 52,
        "platform_account_profiles": 52,
        "creator_record_profiles": 0,
        "profiles_with_metric_rollups": 33,
        "profiles_with_audience_triangulation": 1,
        "engagement_rate_observed_profiles": 31,
        "cross_platform_rollup_profiles": 0,
        "onboarded_profiles": 39,
        "not_onboarded_profiles": 13,
    }
    assert {profile["platform_accounts"][0]["platform"] for profile in view["profiles"]} == {"youtube", "instagram", "tiktok"}

    for profile in view["profiles"]:
        platform = profile["platform_accounts"][0]["platform"]
        assert profile["profile_subject_kind"] == "platform_account"
        assert profile["profile_subject_id"] == profile["platform_account_id_or_none"]
        assert profile["creator_record_id_or_none"] is None
        assert profile["identity_state"] == "single_platform_observed"
        assert profile["link_state_or_none"] is None
        assert profile["review_state_or_none"] is None
        if profile["profile_subject_id"] == "acct_tiktok_fragrance_007":
            audience = profile["audience_triangulation"]
            assert audience["snapshot_id"] == "cats_429711cc94298b9775b1"
            assert audience["actual_audience_demographics"] == "not_estimated"
            assert "not proof of a UK audience" in audience["non_claims"]
        else:
            assert profile["audience_triangulation"] is None
        assert profile["wind_calling_summary"] is None
        assert profile["onboarding"]["onboarding_state"] in {"not_onboarded", "onboarded"}
        if not profile["current_metric_rollups"]:
            assert profile["freshness"]["metrics_computed_at_or_none"] is None
            assert profile["source_drill_back"]["metric_rollup_pointer"] is None
            assert profile["source_drill_back"]["metric_snapshot_pointer"] is None
            assert profile["source_drill_back"]["source_metric_observation_ids"] == []
            assert any("No creator metric rollup is joined yet" in item for item in profile["limitations"])
            continue
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

    identity_only_ids = {
        "acct_tiktok_fragrance_001",
        "acct_tiktok_fragrance_002",
        "acct_tiktok_fragrance_003",
        "acct_tiktok_fragrance_004",
        "acct_ig_fragrance_005",
        "acct_tiktok_fragrance_005",
        "acct_ig_fragrance_006",
        "acct_tiktok_fragrance_006",
        "acct_tiktok_fragrance_007",
        "acct_yt_fragrance_032",
        "acct_yt_fragrance_033",
        "acct_yt_fragrance_034",
        "acct_yt_fragrance_035",
        "acct_yt_fragrance_036",
        "acct_yt_fragrance_037",
        "acct_yt_fragrance_038",
        "acct_yt_fragrance_039",
        "acct_yt_fragrance_040",
        "acct_yt_fragrance_041",
    }
    assert set(rollups_by_subject).issubset(set(accounts_by_id))
    assert set(accounts_by_id) - set(rollups_by_subject) == identity_only_ids
    assert set(accounts_by_id) == {
        profile["profile_subject_id"] for profile in view["profiles"]
    }

    for profile in view["profiles"]:
        subject_id = profile["profile_subject_id"]
        account = accounts_by_id[subject_id]
        assert profile["platform_accounts"] == [account]
        if subject_id not in rollups_by_subject:
            assert profile["current_metric_rollups"] == []
            assert profile["freshness"]["metrics_computed_at_or_none"] is None
            assert profile["source_drill_back"]["source_metric_observation_ids"] == []
            continue
        expected_rollup = rollups_by_subject[subject_id]
        actual_rollup = profile["current_metric_rollups"][0]

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
        creator_registry_index_path=CREATOR_REGISTRY_INDEX_PATH,
        metric_seed_paths=METRIC_SEED_PATHS,
        audience_triangulation_snapshot_paths=(AK_AUDIENCE_SNAPSHOT_PATH,),
        audience_judgment_outcome_paths=(AK_AUDIENCE_OUTCOME_PATH,),
        generated_at_utc=_view()["generated_at_utc"],
    )

    assert generated == _view_document()


def test_creator_profile_current_materializer_optionally_joins_audience_triangulation(tmp_path: Path) -> None:
    account = next(
        row for row in _account_ledger()["platform_accounts"] if row["platform"] == "tiktok"
    )
    snapshot = _audience_snapshot(account["platform_account_id"])
    snapshot_path = tmp_path / "creator_audience_triangulation_snapshot_v0.json"
    snapshot_text = (
        json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )
    snapshot_path.write_text(snapshot_text, encoding="utf-8", newline="\n")

    with pytest.raises(ValueError, match="requires one paired successful"):
        build_creator_profile_current_view_from_files(
            account_ledger_path=ACCOUNT_LEDGER_PATH,
            creator_registry_index_path=CREATOR_REGISTRY_INDEX_PATH,
            metric_seed_paths=METRIC_SEED_PATHS,
            audience_triangulation_snapshot_paths=(snapshot_path,),
            generated_at_utc=_view()["generated_at_utc"],
        )

    response_bytes = b"{}"
    outcome = {
        "schema_version": "creator_audience_judgment_outcome_v0",
        "record_id": "cajo_static_view_test",
        "raw_anchor": "static-view-test",
        "creator_id": snapshot["creator_id"],
        "profile_subject_id": snapshot["profile_subject_id"],
        "bundle_id": snapshot["input_bundle_id"],
        "bundle_hash": snapshot["input_bundle_hash"],
        "status": "validated",
        "response_sha256": f"sha256:{hashlib.sha256(response_bytes).hexdigest()}",
        "response_size_bytes": len(response_bytes),
        "response_bytes_b64": base64.b64encode(response_bytes).decode("ascii"),
        "validation_errors": [],
        "snapshot_id_or_none": snapshot["snapshot_id"],
        "snapshot_sha256_or_none": (
            f"sha256:{hashlib.sha256(snapshot_text.encode('utf-8')).hexdigest()}"
        ),
        "snapshot_or_none": snapshot,
        "model_api_calls": 0,
    }
    outcome_path = tmp_path / "creator_audience_judgment_outcome_v0.json"
    outcome_path.write_text(
        json.dumps(outcome, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    generated = build_creator_profile_current_view_from_files(
        account_ledger_path=ACCOUNT_LEDGER_PATH,
        creator_registry_index_path=CREATOR_REGISTRY_INDEX_PATH,
        metric_seed_paths=METRIC_SEED_PATHS,
        audience_triangulation_snapshot_paths=(snapshot_path,),
        audience_judgment_outcome_paths=(outcome_path,),
        generated_at_utc=_view()["generated_at_utc"],
    )
    view = generated["creator_profile_current_view"]
    joined = next(
        profile
        for profile in view["profiles"]
        if profile["profile_subject_id"] == account["platform_account_id"]
    )

    assert view["counts"]["profiles_with_audience_triangulation"] == 1
    assert joined["audience_triangulation"] == snapshot
    assert joined["freshness"]["audience_computed_at_or_none"] == snapshot["generated_at"]
    assert any("demographics remain not_estimated" in item for item in joined["limitations"])
def test_creator_profile_current_source_hashes_are_current() -> None:
    view = _view()
    inputs_by_pointer = {
        source_input["source_pointer"]: source_input
        for source_input in view["source_inputs"]
    }

    expected_paths = {
        "forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_v0.json": ACCOUNT_LEDGER_PATH,
        "forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_v0.json": CREATOR_REGISTRY_INDEX_PATH,
        "forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json": YOUTUBE_SNAPSHOT_PATH,
        "forseti/product/spines/capture/core/source_families/social_media/instagram/instagram_reels_creator_metric_rollup_snapshot_v0.json": INSTAGRAM_SNAPSHOT_PATH,
        "forseti/product/spines/capture/core/source_families/social_media/creator_registry/ak_fragrances1_creator_audience_triangulation_snapshot_v1.json": AK_AUDIENCE_SNAPSHOT_PATH,
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
        if not profile["current_metric_rollups"]:
            assert any("No creator metric rollup is joined yet" in item for item in profile["limitations"])
            continue
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


def test_creator_profile_identity_only_rejects_metric_pointer_without_rollup() -> None:
    document = _bad_view_document()
    profile = next(
        profile
        for profile in document["creator_profile_current_view"]["profiles"]
        if profile["platform_accounts"][0]["platform"] == "tiktok"
    )
    profile["source_drill_back"]["metric_rollup_pointer"] = "unexpected_metric_pointer"

    _assert_validation_code(document, "identity_only_source_drill_back_has_metric_pointer")


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


def test_creator_profile_validator_rejects_unknown_onboarding_state() -> None:
    document = _bad_view_document()
    document["creator_profile_current_view"]["profiles"][0]["onboarding"]["onboarding_state"] = "pending"

    _assert_validation_code(document, "invalid_onboarding_state")


def test_creator_profile_validator_rejects_not_onboarded_evidence() -> None:
    document = _bad_view_document()
    profile = next(
        profile
        for profile in document["creator_profile_current_view"]["profiles"]
        if profile["onboarding"]["onboarding_state"] == "not_onboarded"
    )
    profile["onboarding"]["evidence_packet_id_or_none"] = "fake_packet"

    _assert_validation_code(document, "not_onboarded_has_evidence")


def test_creator_profile_validator_rejects_malformed_audience_triangulation() -> None:
    document = _bad_view_document()
    document["creator_profile_current_view"]["profiles"][0]["audience_triangulation"] = {"freeform": "young buyers"}
    document["creator_profile_current_view"]["counts"]["profiles_with_audience_triangulation"] = 1

    _assert_validation_code(document, "invalid_audience_triangulation")


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
