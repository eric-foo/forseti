from __future__ import annotations

import json
from pathlib import Path

from capture_spine.creator_profile_current.registry_match_preflight import (
    CANDIDATE_SCHEMA_VERSION,
    CANDIDATES_WRAPPER_KEY,
    RECEIPT_WRAPPER_KEY,
)
from runners.run_creator_registry_match_preflight import main as preflight_main


ROOT = Path(__file__).resolve().parents[3]
REGISTRY_PATH = (
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


def _write_candidates(tmp_path: Path, candidates: list[object]) -> Path:
    path = tmp_path / "creator_registry_match_candidates.json"
    path.write_text(
        json.dumps(
            {
                CANDIDATES_WRAPPER_KEY: {
                    "schema_version": CANDIDATE_SCHEMA_VERSION,
                    "candidates": candidates,
                }
            }
        ),
        encoding="utf-8",
    )
    return path


def _run_preflight(tmp_path: Path, candidates: list[object]) -> tuple[int, dict]:
    candidates_path = _write_candidates(tmp_path, candidates)
    output_path = tmp_path / "creator_registry_match_preflight_receipt.json"
    result = preflight_main(
        [
            "--candidates",
            str(candidates_path),
            "--registry",
            str(REGISTRY_PATH),
            "--output",
            str(output_path),
            "--generated-at-utc",
            "2026-07-04T00:00:00Z",
        ]
    )
    return result, json.loads(output_path.read_text(encoding="utf-8"))


def _result(receipt: dict, index: int = 0) -> dict:
    return receipt[RECEIPT_WRAPPER_KEY]["results"][index]


def test_new_capture_existing_handle_is_blocked(tmp_path: Path) -> None:
    result, receipt = _run_preflight(
        tmp_path,
        [
            {
                "candidate_id": "ig-hyram",
                "platform": "instagram",
                "handle_or_url": "@hyram",
                "intended_action": "new_capture",
            }
        ],
    )

    row = _result(receipt)
    assert result == 2
    assert row["decision"] == "existing_match"
    assert row["action_status"] == "blocked"
    assert row["can_start_new_capture"] is False
    assert row["matched_registry_profiles"][0]["profile_subject_id"] == "acct_ig_reels_001"
    assert row["matched_registry_profiles"][0]["match_reasons"] == ["same_platform_public_handle"]
    assert receipt[RECEIPT_WRAPPER_KEY]["summary"]["blocked_actions"] == 1


def test_new_capture_new_candidate_is_allowed(tmp_path: Path) -> None:
    result, receipt = _run_preflight(
        tmp_path,
        [
            {
                "candidate_id": "ig-new",
                "platform": "instagram",
                "handle_or_url": "@newfragrancecreator",
                "intended_action": "new_capture",
            }
        ],
    )

    row = _result(receipt)
    assert result == 0
    assert row["decision"] == "new_candidate"
    assert row["action_status"] == "allowed"
    assert row["can_start_new_capture"] is True
    assert row["allowed_next_actions"] == ["new_capture"]
    assert receipt[RECEIPT_WRAPPER_KEY]["summary"]["safe_to_capture_new"] == 1


def test_existing_profile_url_blocks_new_capture(tmp_path: Path) -> None:
    result, receipt = _run_preflight(
        tmp_path,
        [
            {
                "candidate_id": "yt-bowtie",
                "handle_or_url": "http://www.youtube.com/channel/UCVvzGrPSok_sf8hfDhvTg7w/",
                "intended_action": "new_capture",
            }
        ],
    )

    row = _result(receipt)
    assert result == 2
    assert row["decision"] == "existing_match"
    assert row["matched_registry_profiles"][0]["profile_subject_id"] == "acct_yt_fragrance_001"
    assert row["matched_registry_profiles"][0]["match_reasons"] == ["public_profile_url"]


def test_conflicting_exact_keys_fail_closed_as_ambiguous(tmp_path: Path) -> None:
    result, receipt = _run_preflight(
        tmp_path,
        [
            {
                "candidate_id": "yt-conflicting-keys",
                "platform": "youtube",
                "platform_account_id_or_none": "acct_yt_fragrance_001",
                "public_handle_or_none": "ChaosFragrances",
                "intended_action": "new_capture",
            }
        ],
    )

    row = _result(receipt)
    assert result == 2
    assert row["decision"] == "ambiguous_match"
    assert row["action_status"] == "blocked"
    assert sorted(match["profile_subject_id"] for match in row["matched_registry_profiles"]) == [
        "acct_yt_fragrance_001",
        "acct_yt_fragrance_002",
    ]
    assert row["allowed_next_actions"] == ["resolve_identity"]


def test_duplicate_candidates_are_invalid(tmp_path: Path) -> None:
    result, receipt = _run_preflight(
        tmp_path,
        [
            {
                "candidate_id": "ig-dup-a",
                "platform": "instagram",
                "handle_or_url": "@duplicatefragrance",
                "intended_action": "new_capture",
            },
            {
                "candidate_id": "ig-dup-b",
                "platform": "instagram",
                "handle_or_url": "duplicatefragrance",
                "intended_action": "new_capture",
            },
        ],
    )

    rows = receipt[RECEIPT_WRAPPER_KEY]["results"]
    assert result == 2
    assert [row["decision"] for row in rows] == ["invalid_candidate", "invalid_candidate"]
    assert {row["errors"][0]["code"] for row in rows} == {"duplicate_candidate_identity"}
    assert receipt[RECEIPT_WRAPPER_KEY]["summary"]["invalid_candidates"] == 2


def test_unsupported_platform_is_invalid(tmp_path: Path) -> None:
    result, receipt = _run_preflight(
        tmp_path,
        [
            {
                "candidate_id": "linkedin-candidate",
                "platform": "linkedin",
                "handle_or_url": "fragrance-person",
                "intended_action": "new_capture",
            }
        ],
    )

    row = _result(receipt)
    assert result == 2
    assert row["decision"] == "invalid_candidate"
    assert row["action_status"] == "blocked"
    assert {error["code"] for error in row["errors"]} == {"unsupported_platform"}


def test_unsupported_profile_url_host_is_invalid(tmp_path: Path) -> None:
    result, receipt = _run_preflight(
        tmp_path,
        [
            {
                "candidate_id": "unknown-host",
                "handle_or_url": "https://example.com/fragrance-person",
                "intended_action": "new_capture",
            }
        ],
    )

    row = _result(receipt)
    assert result == 2
    assert row["decision"] == "invalid_candidate"
    assert row["action_status"] == "blocked"
    assert {error["code"] for error in row["errors"]} == {"unsupported_profile_url_host"}


def test_instagram_post_permalink_does_not_derive_a_bogus_handle(tmp_path: Path) -> None:
    result, receipt = _run_preflight(
        tmp_path,
        [
            {
                "candidate_id": "ig-permalink-share",
                "platform": "instagram",
                "handle_or_url": "https://www.instagram.com/p/Cxxxxxxxxxx/",
                "intended_action": "new_capture",
            }
        ],
    )

    row = _result(receipt)
    assert result == 2
    assert row["decision"] == "invalid_candidate"
    assert row["action_status"] == "blocked"
    assert row["can_start_new_capture"] is False
    assert row["normalized_candidate"]["handles"] == []
    assert {error["code"] for error in row["errors"]} == {"unresolvable_profile_url"}


def test_tiktok_short_link_does_not_derive_a_bogus_handle(tmp_path: Path) -> None:
    result, receipt = _run_preflight(
        tmp_path,
        [
            {
                "candidate_id": "tiktok-shortlink-share",
                "handle_or_url": "https://vm.tiktok.com/ZMabcdEFGH/",
                "intended_action": "new_capture",
            }
        ],
    )

    row = _result(receipt)
    assert result == 2
    assert row["decision"] == "invalid_candidate"
    assert row["action_status"] == "blocked"
    assert row["can_start_new_capture"] is False
    assert row["normalized_candidate"]["handles"] == []
    assert {error["code"] for error in row["errors"]} == {"unresolvable_profile_url"}


def test_tiktok_profile_url_with_handle_still_matches(tmp_path: Path) -> None:
    result, receipt = _run_preflight(
        tmp_path,
        [
            {
                "candidate_id": "tiktok-real-profile",
                "handle_or_url": "https://www.tiktok.com/@brandnewfragrancecreator",
                "intended_action": "new_capture",
            }
        ],
    )

    row = _result(receipt)
    assert result == 0
    assert row["decision"] == "new_candidate"
    assert row["normalized_candidate"]["handles"] == ["brandnewfragrancecreator"]
    assert row["can_start_new_capture"] is True


def test_malformed_candidate_does_not_abort_batch_receipt(tmp_path: Path) -> None:
    result, receipt = _run_preflight(
        tmp_path,
        [
            {
                "candidate_id": "ig-new",
                "platform": "instagram",
                "handle_or_url": "@newfragrancecreator",
                "intended_action": "new_capture",
            },
            {
                "candidate_id": "bad-action",
                "platform": "instagram",
                "handle_or_url": "@anothernewfragrancecreator",
                "intended_action": "new_captur",
            },
        ],
    )

    rows = receipt[RECEIPT_WRAPPER_KEY]["results"]
    summary = receipt[RECEIPT_WRAPPER_KEY]["summary"]
    assert result == 2
    assert rows[0]["candidate_id"] == "ig-new"
    assert rows[0]["decision"] == "new_candidate"
    assert rows[0]["action_status"] == "allowed"
    assert rows[0]["can_start_new_capture"] is True
    assert rows[1]["candidate_id"] == "bad-action"
    assert rows[1]["decision"] == "invalid_candidate"
    assert rows[1]["action_status"] == "blocked"
    assert rows[1]["intended_action"] == "classify"
    assert rows[1]["errors"][0]["code"] == "invalid_candidate_shape"
    assert "candidate[1] 'bad-action'" in rows[1]["errors"][0]["message"]
    assert "new_captur" in rows[1]["errors"][0]["message"]
    assert summary == {
        "total_candidates": 2,
        "existing_matches": 0,
        "new_candidates": 1,
        "ambiguous_matches": 0,
        "invalid_candidates": 1,
        "blocked_actions": 1,
        "safe_to_capture_new": 1,
    }


def test_non_object_candidate_is_invalid_row_not_batch_abort(tmp_path: Path) -> None:
    result, receipt = _run_preflight(tmp_path, ["not-an-object"])

    row = _result(receipt)
    assert result == 2
    assert row["candidate_id"] == "candidate_index_0"
    assert row["decision"] == "invalid_candidate"
    assert row["action_status"] == "blocked"
    assert row["errors"] == [
        {
            "code": "invalid_candidate_shape",
            "message": "candidate[0] 'candidate_index_0': candidate must be an object",
        }
    ]
