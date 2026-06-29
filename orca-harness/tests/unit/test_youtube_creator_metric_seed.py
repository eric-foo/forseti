from __future__ import annotations

import hashlib
import json
import statistics
from pathlib import Path


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
    / "youtube"
    / "youtube_shorts_fragrance_creator_metric_seed_v0.json"
)
CREATOR_LEDGER_PATH = (
    ROOT
    / "orca"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "youtube"
    / "youtube_shorts_fragrance_creator_observation_ledger_v0.json"
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
SOURCE_FILES = (
    "docs/review-inputs/youtube_shorts_fragrance_retained_recapture_v0.json",
    "docs/review-inputs/youtube_shorts_fragrance_replacement_capture_v0.json",
    "docs/review-inputs/youtube_shorts_fragrance_tone_expansion30_capture_v0.json",
    "docs/review-inputs/youtube_shorts_fragrance_tone_expansion100_capture_v0.json",
    "docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.json",
)


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _seed() -> dict:
    return _json(SEED_PATH)["youtube_shorts_fragrance_creator_metric_seed"]


def _creator_ledger() -> dict:
    return _json(CREATOR_LEDGER_PATH)["youtube_creator_observation_ledger"]


def _account_ledger() -> dict:
    return _json(ACCOUNT_LEDGER_PATH)["creator_public_handle_linkage_ledger"]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _pool_index(pool_id: str) -> int:
    return int(pool_id.rsplit("-", 1)[-1])


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


def _source_metric_rows() -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for relpath in SOURCE_FILES:
        data = _json(ROOT / relpath)
        if "recaptured_rows" in data:
            for index, row in enumerate(data["recaptured_rows"]):
                rows[row["video_id"]] = {
                    "source_pointer": f"{relpath}#/recaptured_rows/{index}",
                    "source_field": f"/recaptured_rows/{index}/metadata/view_count",
                    "view_count": row["metadata"]["view_count"],
                    "channel_id": row["metadata"]["channel_id"],
                }
        elif "selected_replacements" in data:
            for index, row in enumerate(data["selected_replacements"]):
                rows[row["video_id"]] = {
                    "source_pointer": f"{relpath}#/selected_replacements/{index}",
                    "source_field": f"/selected_replacements/{index}/metadata/view_count",
                    "view_count": row["metadata"]["view_count"],
                    "channel_id": row["metadata"]["channel_id"],
                }
        else:
            for index, row in enumerate(data["attempts"]):
                if row.get("admission_status") != "admitted":
                    continue
                rows[row["video_id"]] = {
                    "source_pointer": f"{relpath}#/attempts/{index}",
                    "source_field": f"/attempts/{index}/view_count",
                    "view_count": row["view_count"],
                    "channel_id": row["channel_id"],
                }
    return rows


def _ledger_video_rows() -> dict[str, dict]:
    videos: dict[str, dict] = {}
    for row in _creator_ledger()["creator_observations"]:
        for pool_id, video_id in zip(row["pool_ids"], row["video_ids"], strict=True):
            videos[video_id] = {"pool_id": pool_id, "creator": row}
    return videos


def test_youtube_creator_metric_seed_counts_and_boundaries() -> None:
    seed = _seed()
    observations = seed["metric_observations"]
    rollups = seed["metric_rollups"]
    counts = seed["counts"]

    assert seed["schema_version"] == "youtube_shorts_fragrance_creator_metric_seed_v0"
    assert seed["seed_mode"] == "source_backed_static_metric_observation_and_rollup_seed"
    assert counts == {
        "source_metric_rows_total": 200,
        "metric_observations_total": 196,
        "brand_or_platform_excluded_rows": 4,
        "unique_video_ids_source": 200,
        "unique_video_ids_observed_creator_rows": 196,
        "unique_platform_accounts_with_observations": 30,
        "metric_rollups_total": 30,
        "engagement_rate_rollups_observed": 0,
    }
    assert len(observations) == 196
    assert len(rollups) == 30
    assert len(seed["brand_or_platform_exclusions"]) == 4
    assert "not channel-wide creator average" in seed["non_claims"]
    assert "not engagement rate" in seed["non_claims"]
    assert "not cross-platform identity linkage" in seed["non_claims"]
    assert "representative creator or channel averages" in seed["selection_policy"]["representativeness_rule"]
    assert any("sample_support names thin rows" in residual for residual in seed["accepted_residuals"])
    assert any("admission-filter selection" in residual for residual in seed["accepted_residuals"])
    assert seed["source_packet_pointer_posture"] == {
        "source_packet_pointer_or_none": "optional local-only drill-back pointer copied from the capture environment; not portable provenance",
        "portable_provenance_fields": [
            "source_pointer",
            "source_field",
            "source_file",
            "source_packet_id_or_none",
        ],
        "non_claim": "absolute local lake paths are not required to resolve outside the capture host",
    }

    for observation in observations:
        assert observation["profile_subject_kind"] == "platform_account"
        assert observation["profile_subject_id"] == observation["platform_account_id"]
        assert observation["creator_record_id_or_none"] is None
        assert observation["platform"] == "youtube"
        assert observation["content_kind"] == "short"
        assert observation["metric_name"] == "view_count"
        assert observation["metric_unit"] == "count"
        assert observation["metric_posture"] == "observed"
        assert isinstance(observation["metric_value_or_none"], int)
        assert observation["metric_value_or_none"] >= 0


def test_youtube_creator_metric_seed_rebuilds_from_source_rows() -> None:
    seed = _seed()
    source_rows = _source_metric_rows()
    ledger_video_rows = _ledger_video_rows()
    account_by_channel = {
        account["platform_public_account_id_or_none"]: account["platform_account_id"]
        for account in _account_ledger()["platform_accounts"]
        if account["platform"] == "youtube"
    }

    assert len(source_rows) == 200
    assert set(source_rows) == set(ledger_video_rows)

    observations_by_video = {
        observation["content_id_or_none"]: observation
        for observation in seed["metric_observations"]
    }
    excluded_videos = {
        exclusion["video_id"]
        for exclusion in seed["brand_or_platform_exclusions"]
    }

    for video_id, source in source_rows.items():
        ledger_row = ledger_video_rows[video_id]["creator"]
        if ledger_row["creator_classification"] == "brand_or_platform_account_observed":
            assert video_id in excluded_videos
            continue

        observation = observations_by_video[video_id]
        assert observation["metric_value_or_none"] == source["view_count"]
        assert observation["source_pointer"] == source["source_pointer"]
        assert observation["source_field"] == source["source_field"]
        assert observation["platform_subject_key"] == ledger_row["platform_subject_key"]
        assert observation["platform_account_id"] == account_by_channel[source["channel_id"]]
        assert observation["source_pool_row_id"] == ledger_video_rows[video_id]["pool_id"]


def test_youtube_creator_metric_seed_rollups_recompute_from_observations() -> None:
    seed = _seed()
    by_account: dict[str, list[dict]] = {}
    for observation in seed["metric_observations"]:
        by_account.setdefault(observation["platform_account_id"], []).append(observation)

    for rollup in seed["metric_rollups"]:
        observations = sorted(
            by_account[rollup["profile_subject_id"]],
            key=lambda item: _pool_index(item["source_pool_row_id"]),
        )
        values = [observation["metric_value_or_none"] for observation in observations]

        assert rollup["profile_subject_kind"] == "platform_account"
        assert rollup["creator_record_id_or_none"] is None
        assert rollup["platform_scope"] == "youtube"
        assert rollup["platform_account_ids"] == [rollup["profile_subject_id"]]
        assert rollup["source_metric_observation_ids"] == [
            observation["metric_observation_id"] for observation in observations
        ]
        assert rollup["observation_count"] == len(observations)
        assert rollup["sample_support"] == {
            "observation_count": len(observations),
            "sample_adequacy": _sample_support_label(len(observations)),
            "representativeness_posture": "admitted_pool_only_not_representative_creator_average",
            "surface_handling": _surface_handling(len(observations)),
        }
        assert any("not a representative creator average" in item for item in rollup["limitations"])
        assert any("selection can bias view averages" in item for item in rollup["limitations"])
        assert rollup["view_count_min"] == min(values)
        assert rollup["view_count_max"] == max(values)
        assert rollup["metric_rollups"]["average_views"]["value_or_none"] == round(
            statistics.mean(values), 2
        )
        assert rollup["metric_rollups"]["median_views"]["value_or_none"] == round(
            statistics.median(values), 2
        )
        assert rollup["metric_rollups"]["engagement_rate"]["value_or_none"] is None
        assert rollup["metric_rollups"]["engagement_rate"]["posture"] == "unavailable_with_reason"
        assert rollup["freshness_state"] == "partial"


def test_youtube_creator_metric_seed_source_hashes_match_current_files() -> None:
    seed = _seed()
    for source in seed["source_inputs"]:
        path = ROOT / source["source_pointer"]
        assert path.is_file(), source["source_pointer"]
        assert source["sha256"] == _sha256(path)
