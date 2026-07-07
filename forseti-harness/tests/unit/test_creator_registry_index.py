from __future__ import annotations

import hashlib
import json
from pathlib import Path


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
    / "creator_registry_index_v0.json"
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


_FORBIDDEN_REGISTRY_FIELDS = {
    "average_views",
    "median_views",
    "engagement_rate",
    "average_like_count",
    "average_comment_count",
    "follower_count",
    "subscriber_count",
    "ideal_audience_profile",
    "wind_calling_summary",
    "email",
    "phone",
    "contact",
}


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _registry() -> dict:
    return _json(REGISTRY_PATH)["creator_registry_index"]


def _account_ledger() -> dict:
    return _json(ACCOUNT_LEDGER_PATH)["creator_public_handle_linkage_ledger"]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _walk_keys(value: object) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.add(str(key))
            keys.update(_walk_keys(nested))
    elif isinstance(value, list):
        for item in value:
            keys.update(_walk_keys(item))
    return keys


def test_creator_registry_index_counts_and_contract() -> None:
    registry = _registry()

    assert registry["schema_version"] == "creator_registry_index_v0"
    assert registry["index_mode"] == "static_known_public_account_dedupe_index"
    assert registry["counts"] == {
        "platform_accounts_total": 38,
        "creator_records_total": 1,
        "known_account_rows_total": 38,
        "platform_accounts_by_platform": {"instagram": 4, "tiktok": 4, "youtube": 30},
    }
    assert [record["creator_record_id"] for record in registry["creator_records"]] == ["creator_fragranceknowledge_001"]
    creator_record = registry["creator_records"][0]
    assert creator_record["link_state"] == "candidate_public_account_link"
    assert creator_record["review_state"] == "candidate_needs_review"
    assert creator_record["platform_account_ids"] == [
        "acct_yt_fragrance_007",
        "acct_tiktok_fragrance_004",
        "acct_ig_fragrance_005",
    ]
    assert creator_record["evidence_ids"] == ["ev_linkhub_fragranceknowledge_20260707_001"]
    assert creator_record["routing_decision"] == "route_to_linkage_review_before_cross_platform_rollup_or_final_identity_use"
    assert "not metric authority" in registry["non_claims"]
    assert "not public person identity proof" in registry["non_claims"]


def test_creator_registry_index_mirrors_public_handle_ledger_accounts() -> None:
    registry = _registry()
    ledger = _account_ledger()
    registry_by_id = {
        account["platform_account_id"]: account
        for account in registry["platform_accounts"]
    }

    assert set(registry_by_id) == {
        account["platform_account_id"]
        for account in ledger["platform_accounts"]
    }

    linked_account_ids = {
        "acct_yt_fragrance_007",
        "acct_tiktok_fragrance_004",
        "acct_ig_fragrance_005",
    }
    profile_packet_account_ids = {
        "acct_ig_reels_001",
        "acct_ig_reels_002",
        "acct_ig_reels_004",
        "acct_tiktok_fragrance_001",
        "acct_tiktok_fragrance_002",
        "acct_tiktok_fragrance_003",
        "acct_tiktok_fragrance_004",
        "acct_ig_fragrance_005",
    }


    for source_account in ledger["platform_accounts"]:
        indexed = registry_by_id[source_account["platform_account_id"]]
        normalized_handle = source_account["public_handle"].lstrip("@").lower()
        assert indexed["platform"] == source_account["platform"]
        assert indexed["platform_public_account_id_or_none"] == source_account["platform_public_account_id_or_none"]
        assert indexed["public_handle"] == source_account["public_handle"]
        assert indexed["normalized_public_handle"] == normalized_handle
        assert indexed["public_profile_url"] == source_account["public_profile_url"]
        assert indexed["discovery_state"] == "known_account"

        if source_account["platform_account_id"] in linked_account_ids:
            assert indexed["creator_record_id_or_none"] == "creator_fragranceknowledge_001"
            assert indexed["identity_state"] == "candidate_public_account_link"
            assert indexed["linkage_state"] == "candidate_needs_review"
            assert indexed["routing_decision"] == "dedupe_exact_platform_account_then_route_linkage_review_before_cross_platform_use"
        else:
            assert indexed["creator_record_id_or_none"] is None
            assert indexed["identity_state"] == "single_platform_observed"
            assert indexed["linkage_state"] == "single_platform_observed"

        if source_account["platform_account_id"] in profile_packet_account_ids:
            assert indexed["capture_state"] == "identity_observed_profile_packet_available"
            assert indexed["freshness"]["metrics_freshness_state_or_none"] is None
        else:
            assert indexed["capture_state"] == "identity_observed_metric_seed_available"
        assert indexed["freshness"]["identity_observed_at"] == source_account["handle_observed_at"]
        assert f"platform:{source_account['platform']}:handle:{normalized_handle}" in indexed["lookup_keys"]
        if source_account["platform_public_account_id_or_none"] is not None:
            assert any(
                key.startswith(f"platform:{source_account['platform']}:public_account_id:")
                for key in indexed["lookup_keys"]
            )


def test_creator_registry_index_source_hash_matches_public_handle_ledger() -> None:
    registry = _registry()
    source = registry["source_inputs"][0]

    assert source["source_pointer"] == (
        "forseti/product/spines/capture/core/source_families/social_media/creator_registry/"
        "creator_public_handle_linkage_ledger_v0.json"
    )
    assert source["sha256"] == _sha256(ACCOUNT_LEDGER_PATH)


def test_creator_registry_index_does_not_carry_metric_or_contact_fields() -> None:
    keys = _walk_keys(_registry())

    assert not (_FORBIDDEN_REGISTRY_FIELDS & keys)
