from __future__ import annotations

import json
import re
import statistics
from pathlib import Path

from capture_spine.creator_profile_current.instagram_metric_seed import (
    build_instagram_reels_creator_metric_seed_from_files,
)


ROOT = Path(__file__).resolve().parents[3]
SEED_PATH = (
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
ACCOUNT_LEDGER_PATH = (
    ROOT
    / "orca"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_registry"
    / "creator_public_handle_linkage_ledger_v0.json"
)
_SHA256_RE = re.compile(r"[0-9a-f]{64}")


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _seed() -> dict:
    return _json(SEED_PATH)["instagram_reels_creator_metric_seed"]


def _account_ledger() -> dict:
    return _json(ACCOUNT_LEDGER_PATH)["creator_public_handle_linkage_ledger"]


def _sample_support_label(observation_count: int) -> str:
    if observation_count <= 3:
        return "thin_n_1_to_3"
    if observation_count <= 7:
        return "limited_n_4_to_7"
    return "stronger_admitted_pool_n_8_plus"


def _surface_handling(observation_count: int) -> str:
    if observation_count <= 3:
        return "downgrade_or_withhold_summary_claim"
    return "show_only_with_visible_admitted_pool_limitation"


def test_instagram_reels_creator_metric_seed_counts_and_boundaries() -> None:
    seed = _seed()

    assert seed["schema_version"] == "instagram_reels_creator_metric_seed_v0"
    assert seed["seed_mode"] == "source_backed_static_metric_observation_and_rollup_seed"
    assert seed["counts"] == {
        "source_projection_files_supplied": 3,
        "source_projection_files_selected": 3,
        "metric_observations_total": 111,
        "content_metric_observations_total": 108,
        "profile_metric_observations_total": 3,
        "unique_content_items_observed": 36,
        "unique_platform_accounts_with_observations": 3,
        "metric_rollups_total": 3,
        "engagement_rate_rollups_observed": 3,
    }
    assert len(seed["metric_observations"]) == 111
    assert len(seed["metric_rollups"]) == 3
    assert all(_SHA256_RE.fullmatch(item["sha256"]) for item in seed["source_inputs"])
    assert all(item["source_pointer"].startswith("F:\\orca-data-lake\\derived\\") for item in seed["source_inputs"])
    assert seed["source_packet_pointer_posture"]["non_claim"] == (
        "absolute local lake paths are not required to resolve outside the capture host"
    )
    assert "not cross-platform identity linkage" in seed["non_claims"]

    accounts = {
        account["platform_account_id"]: account
        for account in _account_ledger()["platform_accounts"]
        if account["platform"] == "instagram"
    }
    assert set(accounts) == {"acct_ig_reels_001", "acct_ig_reels_002", "acct_ig_reels_004"}
    assert {observation["platform_account_id"] for observation in seed["metric_observations"]} == set(accounts)

    for observation in seed["metric_observations"]:
        assert observation["profile_subject_kind"] == "platform_account"
        assert observation["profile_subject_id"] == observation["platform_account_id"]
        assert observation["creator_record_id_or_none"] is None
        assert observation["platform"] == "instagram"
        assert observation["metric_unit"] == "count"
        assert observation["metric_posture"] == "observed"
        assert isinstance(observation["metric_value_or_none"], int)
        assert observation["metric_value_or_none"] >= 0


def test_instagram_reels_creator_metric_seed_rollups_recompute_from_observations() -> None:
    seed = _seed()
    observations_by_id = {
        observation["metric_observation_id"]: observation
        for observation in seed["metric_observations"]
    }

    for rollup in seed["metric_rollups"]:
        source_observations = [observations_by_id[item] for item in rollup["source_metric_observation_ids"]]
        by_content: dict[str, dict[str, dict]] = {}
        for observation in source_observations:
            by_content.setdefault(observation["content_id_or_none"], {})[observation["metric_name"]] = observation

        complete_reels = [
            metrics
            for metrics in by_content.values()
            if all(metric in metrics for metric in ("view_count", "like_count", "comment_count"))
        ]
        views = [item["view_count"]["metric_value_or_none"] for item in complete_reels]
        likes = [item["like_count"]["metric_value_or_none"] for item in complete_reels]
        comments = [item["comment_count"]["metric_value_or_none"] for item in complete_reels]
        observation_count = len(source_observations)

        assert len(complete_reels) == 12
        assert observation_count == 36
        assert rollup["profile_subject_kind"] == "platform_account"
        assert rollup["creator_record_id_or_none"] is None
        assert rollup["platform_scope"] == "instagram"
        assert rollup["platform_account_ids"] == [rollup["profile_subject_id"]]
        assert rollup["observation_count"] == observation_count
        assert rollup["sample_support"] == {
            "observation_count": observation_count,
            "sample_adequacy": _sample_support_label(observation_count),
            "representativeness_posture": "admitted_pool_only_not_representative_creator_average",
            "surface_handling": _surface_handling(observation_count),
        }
        assert rollup["view_count_min"] == min(views)
        assert rollup["view_count_max"] == max(views)
        assert rollup["metric_rollups"]["average_views"]["value_or_none"] == round(statistics.mean(views), 2)
        assert rollup["metric_rollups"]["median_views"]["value_or_none"] == round(statistics.median(views), 2)
        assert rollup["metric_rollups"]["average_like_count"]["value_or_none"] == round(statistics.mean(likes), 2)
        assert rollup["metric_rollups"]["average_comment_count"]["value_or_none"] == round(statistics.mean(comments), 2)
        assert rollup["metric_rollups"]["engagement_rate"]["value_or_none"] == round(
            (sum(likes) + sum(comments)) / sum(views), 6
        )
        assert rollup["freshness_state"] == "partial"
        assert any("not a representative creator average" in item for item in rollup["limitations"])
        assert any("selection can bias view averages" in item for item in rollup["limitations"])


def test_instagram_reels_creator_metric_seed_builder_dedupes_projection_by_observed_rows(tmp_path: Path) -> None:
    account_ledger = {
        "platform_accounts": [
            {
                "platform_account_id": "acct_ig_fixture_001",
                "platform": "instagram",
                "public_handle": "fixturecreator",
                "public_profile_url": "https://www.instagram.com/fixturecreator/",
                "handle_source_pointer": "fixture#/rows/0",
                "handle_observed_at": "2026-06-29T00:00:00Z",
            }
        ]
    }
    weak = tmp_path / "weak.json"
    strong = tmp_path / "strong.json"
    weak.write_text(json.dumps(_projection(rows=[_profile_row("fixturecreator", 10, "2026-06-29T00:00:00Z")])) , encoding="utf-8")
    strong.write_text(
        json.dumps(
            _projection(
                rows=[
                    _profile_row("fixturecreator", 20, "2026-06-29T00:01:00Z"),
                    _reel_row("fixturecreator", "ABC", "view_count", 100, "2026-06-29T00:01:00Z"),
                    _reel_row("fixturecreator", "ABC", "like_count", 10, "2026-06-29T00:01:00Z"),
                    _reel_row("fixturecreator", "ABC", "comment_count", 5, "2026-06-29T00:01:00Z"),
                ]
            )
        ),
        encoding="utf-8",
    )

    document = build_instagram_reels_creator_metric_seed_from_files(
        projection_paths=[weak, strong],
        account_ledger=account_ledger,
        generated_at_utc="2026-06-29T00:02:00Z",
    )
    seed = document["instagram_reels_creator_metric_seed"]

    assert seed["counts"]["source_projection_files_supplied"] == 2
    assert seed["counts"]["source_projection_files_selected"] == 1
    assert seed["source_inputs"][0]["source_pointer"] == str(strong)
    rollup = seed["metric_rollups"][0]
    assert rollup["observation_count"] == 3
    assert rollup["metric_rollups"]["average_views"]["value_or_none"] == 100
    assert rollup["metric_rollups"]["average_like_count"]["value_or_none"] == 10
    assert rollup["metric_rollups"]["average_comment_count"]["value_or_none"] == 5
    assert rollup["metric_rollups"]["engagement_rate"]["value_or_none"] == 0.15


def _projection(*, rows: list[dict]) -> dict:
    return {
        "packet_id": "packet_fixture",
        "rows": rows,
    }


def _profile_row(username: str, value: int, capture_time: str) -> dict:
    return {
        "row_id": f"packet_fixture:profile:follower_count:{value}",
        "row_kind": "ig_creator_metric",
        "username": username,
        "content_kind": "profile",
        "content_shortcode": None,
        "content_url": None,
        "metric": "follower_count",
        "posture": "observed",
        "value": value,
        "reason": None,
        "capture_time": capture_time,
        "coverage_window": {"start": None, "end": capture_time},
        "raw_ref": {"packet_id": "packet_fixture", "slice_id": "ig_reels_profile_00"},
        "raw_anchor": {"file_id": "file_01", "relative_packet_path": "raw/01.json", "sha256": "a" * 64, "hash_basis": "raw_stored_bytes"},
        "chosen_source_surface": "web_profile_info_json_metadata",
        "source_surface_count_candidates": [],
        "source_publication_or_event": None,
    }


def _reel_row(username: str, shortcode: str, metric: str, value: int, capture_time: str) -> dict:
    return {
        "row_id": f"packet_fixture:{shortcode}:{metric}",
        "row_kind": "ig_media_metric",
        "username": username,
        "content_kind": "reel",
        "content_shortcode": shortcode,
        "content_url": f"https://www.instagram.com/{username}/reel/{shortcode}/",
        "metric": metric,
        "posture": "observed",
        "value": value,
        "reason": None,
        "capture_time": capture_time,
        "coverage_window": {"start": None, "end": capture_time},
        "raw_ref": {"packet_id": "packet_fixture", "slice_id": "ig_reels_grid_01"},
        "raw_anchor": {"file_id": "file_01", "relative_packet_path": "raw/01.json", "sha256": "a" * 64, "hash_basis": "raw_stored_bytes"},
        "chosen_source_surface": "clips_user_json_metadata",
        "source_surface_count_candidates": [],
        "source_publication_or_event": capture_time,
    }
