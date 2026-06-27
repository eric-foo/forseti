from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from capture_spine.creator_public_handle_linkage import (
    CreatorPublicHandleLinkageError,
    load_creator_public_handle_linkage_ledger,
    validate_creator_public_handle_linkage_ledger,
)


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "creator_public_handle_linkage"
    / "valid_synthetic_ledger.json"
)


def _fixture() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _wrapper(ledger: dict) -> dict:
    return ledger["creator_public_handle_linkage_ledger"]


def _raises_code(ledger: dict, expected_code: str) -> None:
    with pytest.raises(CreatorPublicHandleLinkageError) as exc_info:
        validate_creator_public_handle_linkage_ledger(ledger)
    assert exc_info.value.code == expected_code


def test_valid_synthetic_fixture_loads_and_validates() -> None:
    loaded = load_creator_public_handle_linkage_ledger(FIXTURE_PATH)

    wrapper = _wrapper(loaded)
    assert wrapper["ledger_mode"] == "synthetic_fixture"
    assert {record["link_state"] for record in wrapper["creator_records"]} == {
        "declared_public_account_link",
        "probable_public_account_link",
        "rejected_public_account_link",
        "candidate_public_account_link",
    }


def test_unknown_top_level_sibling_key_raises() -> None:
    ledger = _fixture()
    ledger["ignored_payload"] = {"harmless": "ignored"}

    _raises_code(ledger, "unknown_field")


def test_forbidden_real_identity_field_raises() -> None:
    ledger = _fixture()
    _wrapper(ledger)["platform_accounts"][0]["legal_name"] = "Fixture Person"

    _raises_code(ledger, "forbidden_output_field")


def test_confirmed_link_label_is_rejected() -> None:
    ledger = _fixture()
    _wrapper(ledger)["creator_records"][0]["link_state"] = "confirmed_public_account_link"

    _raises_code(ledger, "confirmed_link_state_forbidden")


def test_declared_link_requires_strong_public_evidence() -> None:
    ledger = _fixture()
    evidence = _wrapper(ledger)["account_link_evidence"][0]
    evidence["evidence_type"] = "handle_similarity"
    evidence["evidence_strength"] = "weak"

    _raises_code(ledger, "declared_link_missing_strong_evidence")


def test_probable_link_requires_three_independent_weak_evidence_types() -> None:
    ledger = _fixture()
    for evidence in _wrapper(ledger)["account_link_evidence"]:
        if evidence["evidence_id"] in {"ev_barrier_bio_overlap", "ev_barrier_topic_overlap"}:
            evidence["evidence_type"] = "handle_similarity"
            evidence["source_field"] = "profile.public_handle"

    _raises_code(ledger, "probable_link_needs_three_independent_weak_evidence_types")


def test_disconfirming_evidence_blocks_probable_link() -> None:
    ledger = _fixture()
    barrier = next(
        record
        for record in _wrapper(ledger)["creator_records"]
        if record["creator_record_id"] == "cphl_synthetic_barrier_001"
    )
    barrier["evidence_ids"].append("ev_mist_conflicting_link_hub")
    barrier["platform_account_ids"].extend(["acct_synthetic_mist_ig", "acct_synthetic_mist_yt"])

    _raises_code(ledger, "disconfirming_evidence_blocks_final_link")


def test_llm_only_final_link_raises() -> None:
    ledger = _fixture()
    for evidence in _wrapper(ledger)["account_link_evidence"]:
        if evidence["evidence_id"].startswith("ev_barrier_"):
            evidence["llm_assisted"] = True
            evidence["review_actor"] = "llm_only"

    _raises_code(ledger, "llm_only_final_link")


def test_missing_display_name_source_fails() -> None:
    ledger = _fixture()
    _wrapper(ledger)["platform_accounts"][0]["display_name_source_pointer_or_none"] = None

    _raises_code(ledger, "missing_display_name_source_pointer_or_none")


def test_synthetic_fixture_rejects_real_looking_profile_url() -> None:
    ledger = _fixture()
    _wrapper(ledger)["platform_accounts"][0]["public_profile_url"] = (
        "https://instagram.com/synthetic_glow_lab_ig"
    )

    _raises_code(ledger, "synthetic_fixture_url_required")


def test_synthetic_fixture_rejects_real_looking_handle() -> None:
    ledger = _fixture()
    _wrapper(ledger)["platform_accounts"][0]["public_handle"] = "glowlab"

    _raises_code(ledger, "synthetic_fixture_handle_required")


def test_non_public_join_evidence_type_is_rejected() -> None:
    ledger = _fixture()
    _wrapper(ledger)["account_link_evidence"][0]["evidence_type"] = "email_match"

    _raises_code(ledger, "invalid_evidence_type")


def test_evidence_cannot_point_outside_creator_record_accounts() -> None:
    ledger = _fixture()
    declared = _wrapper(ledger)["creator_records"][0]
    declared["evidence_ids"].append("ev_barrier_handle_similarity")

    _raises_code(ledger, "evidence_points_outside_creator_record")


def test_single_platform_creator_record_raises() -> None:
    ledger = _fixture()
    declared = _wrapper(ledger)["creator_records"][0]
    declared["platform_account_ids"] = ["acct_synthetic_glow_ig", "acct_synthetic_barrier_ig"]
    declared["evidence_ids"] = []
    evidence = copy.deepcopy(_wrapper(ledger)["account_link_evidence"][0])
    evidence["evidence_id"] = "ev_ig_only_self_declared"
    evidence["account_ids"] = declared["platform_account_ids"]
    _wrapper(ledger)["account_link_evidence"].append(evidence)
    declared["evidence_ids"] = [evidence["evidence_id"]]

    _raises_code(ledger, "single_platform_creator_record")


def test_hollow_non_claims_raise() -> None:
    ledger = _fixture()
    _wrapper(ledger)["non_claims"] = ["not ready"]

    _raises_code(ledger, "missing_required_non_claim")


