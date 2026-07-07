from __future__ import annotations

import hashlib
import json
import re
import statistics
from pathlib import Path

import pytest

from capture_spine.creator_profile_current.instagram_metric_seed import (
    build_instagram_reels_creator_metric_seed_from_files,
    discover_instagram_reels_projection_paths_from_lake,
)
from data_lake.root import DataLakeRoot, raw_shard
from source_capture.ig_reels_grid_projection import PROJECTION_IG_REELS_GRID_LANE
import runners.run_instagram_reels_creator_metric_seed_materialize as metric_seed_runner


ROOT = Path(__file__).resolve().parents[3]
SEED_PATH = (
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
        "source_projection_files_supplied": 7,
        "source_projection_files_selected": 3,
        "metric_observations_total": 84,
        "content_metric_observations_total": 81,
        "profile_metric_observations_total": 3,
        "unique_content_items_observed": 27,
        "unique_platform_accounts_with_observations": 3,
        "metric_rollups_total": 3,
        "engagement_rate_rollups_observed": 3,
    }
    assert len(seed["metric_observations"]) == 84
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
    observed_account_ids = {"acct_ig_reels_001", "acct_ig_reels_002", "acct_ig_reels_004"}
    assert observed_account_ids.issubset(set(accounts))
    assert {observation["platform_account_id"] for observation in seed["metric_observations"]} == observed_account_ids

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

        # Per-account, from the committed artifact: recency-primary selection means a
        # newest-but-sparser capture legitimately carries fewer observations (the seed's
        # selection_residuals name the bypassed fuller sibling).
        expected_shape = {
            "acct_ig_reels_001": (9, 3),
            "acct_ig_reels_002": (36, 12),
            "acct_ig_reels_004": (36, 12),
        }[rollup["profile_subject_id"]]
        assert (observation_count, len(complete_reels)) == expected_shape
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


def test_instagram_reels_creator_metric_seed_builder_selects_newest_capture_per_username(tmp_path: Path) -> None:
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
    older = tmp_path / "older.json"
    newer = tmp_path / "newer.json"
    older.write_text(
        json.dumps(
            _projection(
                packet_id="packet_older",
                rows=[_profile_row("fixturecreator", 10, "2026-06-29T00:00:00Z", packet_id="packet_older")],
            )
        ),
        encoding="utf-8",
    )
    newer.write_text(
        json.dumps(
            _projection(
                packet_id="packet_newer",
                rows=[
                    _profile_row("fixturecreator", 20, "2026-06-29T00:01:00Z", packet_id="packet_newer"),
                    _reel_row("fixturecreator", "ABC", "view_count", 100, "2026-06-29T00:01:00Z", packet_id="packet_newer"),
                    _reel_row("fixturecreator", "ABC", "like_count", 10, "2026-06-29T00:01:00Z", packet_id="packet_newer"),
                    _reel_row("fixturecreator", "ABC", "comment_count", 5, "2026-06-29T00:01:00Z", packet_id="packet_newer"),
                ],
            )
        ),
        encoding="utf-8",
    )

    document = build_instagram_reels_creator_metric_seed_from_files(
        projection_paths=[older, newer],
        account_ledger=account_ledger,
        generated_at_utc="2026-06-29T00:02:00Z",
    )
    seed = document["instagram_reels_creator_metric_seed"]

    assert seed["counts"]["source_projection_files_supplied"] == 2
    assert seed["counts"]["source_projection_files_selected"] == 1
    assert seed["source_inputs"][0]["source_pointer"] == str(newer)
    # The newest capture also carries the most observed rows here, so no residual.
    assert seed["selection_residuals"] == []
    rollup = seed["metric_rollups"][0]
    assert rollup["observation_count"] == 3
    assert rollup["metric_rollups"]["average_views"]["value_or_none"] == 100
    assert rollup["metric_rollups"]["average_like_count"]["value_or_none"] == 10
    assert rollup["metric_rollups"]["average_comment_count"]["value_or_none"] == 5
    assert rollup["metric_rollups"]["engagement_rate"]["value_or_none"] == 0.15


def test_instagram_reels_creator_metric_seed_newest_capture_with_fewer_rows_wins_and_surfaces_residual(
    tmp_path: Path,
) -> None:
    # The F-IGRC-001 fix contract: recency decides -- a fuller-but-staler projection
    # must NOT outrank a newer one -- and the bypassed fuller sibling is surfaced as
    # a named residual instead of silently absorbed.
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
    fuller_older = tmp_path / "fuller_older.json"
    thinner_newer = tmp_path / "thinner_newer.json"
    fuller_older.write_text(
        json.dumps(
            _projection(
                packet_id="packet_older",
                rows=[
                    _profile_row("fixturecreator", 10, "2026-06-29T00:00:00Z", packet_id="packet_older"),
                    _reel_row("fixturecreator", "ABC", "view_count", 90, "2026-06-29T00:00:00Z", packet_id="packet_older"),
                    _reel_row("fixturecreator", "ABC", "like_count", 9, "2026-06-29T00:00:00Z", packet_id="packet_older"),
                    _reel_row("fixturecreator", "ABC", "comment_count", 4, "2026-06-29T00:00:00Z", packet_id="packet_older"),
                    _reel_row("fixturecreator", "DEF", "view_count", 80, "2026-06-29T00:00:00Z", packet_id="packet_older"),
                    _reel_row("fixturecreator", "DEF", "like_count", 8, "2026-06-29T00:00:00Z", packet_id="packet_older"),
                    _reel_row("fixturecreator", "DEF", "comment_count", 3, "2026-06-29T00:00:00Z", packet_id="packet_older"),
                ],
            )
        ),
        encoding="utf-8",
    )
    thinner_newer.write_text(
        json.dumps(
            _projection(
                packet_id="packet_newer",
                rows=[
                    _profile_row("fixturecreator", 20, "2026-06-29T00:05:00Z", packet_id="packet_newer"),
                    _reel_row("fixturecreator", "ABC", "view_count", 100, "2026-06-29T00:05:00Z", packet_id="packet_newer"),
                    _reel_row("fixturecreator", "ABC", "like_count", 10, "2026-06-29T00:05:00Z", packet_id="packet_newer"),
                    _reel_row("fixturecreator", "ABC", "comment_count", 5, "2026-06-29T00:05:00Z", packet_id="packet_newer"),
                ],
            )
        ),
        encoding="utf-8",
    )

    document = build_instagram_reels_creator_metric_seed_from_files(
        projection_paths=[fuller_older, thinner_newer],
        account_ledger=account_ledger,
        generated_at_utc="2026-06-29T00:06:00Z",
    )
    seed = document["instagram_reels_creator_metric_seed"]

    assert seed["source_inputs"][0]["source_pointer"] == str(thinner_newer)
    (residual,) = seed["selection_residuals"]
    assert residual == {
        "username": "fixturecreator",
        "reason": "newer_capture_fewer_observed_rows",
        "selected_projection": str(thinner_newer),
        "selected_observed_count": 4,
        "bypassed_projection": str(fuller_older),
        "bypassed_observed_count": 7,
    }


def test_instagram_reels_creator_metric_seed_orders_capture_times_by_parsed_instant(
    tmp_path: Path,
) -> None:
    # Raw ISO strings can sort differently from their actual instants when offsets
    # differ. The seed must feed the sibling selector a parsed instant, not the
    # lexically largest row timestamp from a projection. The decisive fixture is
    # MIXED offsets WITHIN one projection: the lexically greatest row string
    # (decoy, 2026-07-02T...+03:00 = 2026-07-01T21:15Z) is an OLDER instant than
    # the true newest row (2026-07-01T...-02:00 = 2026-07-02T01:30Z), so a
    # string-max summary understates the projection's recency and loses to
    # true_older; the parsed-instant summary wins.
    account_ledger = {
        "platform_accounts": [
            {
                "platform_account_id": "acct_ig_fixture_001",
                "platform": "instagram",
                "public_handle": "fixturecreator",
                "public_profile_url": "https://www.instagram.com/fixturecreator/",
                "handle_source_pointer": "fixture#/rows/0",
                "handle_observed_at": "2026-07-02T00:00:00Z",
            }
        ]
    }
    true_newer = tmp_path / "true_newer_offset.json"
    true_older = tmp_path / "true_older_utc.json"
    true_newer_capture = "2026-07-01T23:30:00-02:00"  # 2026-07-02T01:30:00Z (true max instant)
    decoy_lexical_capture = "2026-07-02T00:15:00+03:00"  # 2026-07-01T21:15:00Z (lexical max, older instant)
    true_older_capture = "2026-07-02T00:30:00+00:00"
    true_newer.write_text(
        json.dumps(
            _projection(
                packet_id="packet_true_newer",
                rows=[
                    _profile_row("fixturecreator", 20, decoy_lexical_capture, packet_id="packet_true_newer"),
                    _reel_row("fixturecreator", "ABC", "view_count", 100, true_newer_capture, packet_id="packet_true_newer"),
                    _reel_row("fixturecreator", "ABC", "like_count", 10, true_newer_capture, packet_id="packet_true_newer"),
                    _reel_row("fixturecreator", "ABC", "comment_count", 5, true_newer_capture, packet_id="packet_true_newer"),
                ],
            )
        ),
        encoding="utf-8",
    )
    true_older.write_text(
        json.dumps(
            _projection(
                packet_id="packet_true_older",
                rows=[
                    _profile_row("fixturecreator", 10, true_older_capture, packet_id="packet_true_older"),
                    _reel_row("fixturecreator", "ABC", "view_count", 90, true_older_capture, packet_id="packet_true_older"),
                    _reel_row("fixturecreator", "ABC", "like_count", 9, true_older_capture, packet_id="packet_true_older"),
                    _reel_row("fixturecreator", "ABC", "comment_count", 4, true_older_capture, packet_id="packet_true_older"),
                ],
            )
        ),
        encoding="utf-8",
    )

    document = build_instagram_reels_creator_metric_seed_from_files(
        projection_paths=[true_newer, true_older],
        account_ledger=account_ledger,
        generated_at_utc="2026-07-02T02:00:00Z",
    )
    seed = document["instagram_reels_creator_metric_seed"]

    assert seed["source_inputs"][0]["source_pointer"] == str(true_newer)
    assert seed["metric_rollups"][0]["metric_rollups"]["average_views"]["value_or_none"] == 100


def test_instagram_reels_metric_seed_dedupe_keeps_catchup_rank_for_identical_content(
    tmp_path: Path,
) -> None:
    # Observed on the live lake (2026-07-05): one packet carried three distinct
    # ULID derivations PLUS a rank-1 catch-up byte-identical to the newest one.
    # Discovery's content dedupe must keep the CATCH-UP path as the representative
    # of the identical pair -- else its supersession rank is lost before selection
    # and the three ULIDs tie ambiguous instead of being superseded.
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    packet_id = "01KWBMNTESWZVSVD3YASDAXK0A"
    newest_body = json.dumps(
        _projection(
            packet_id=packet_id,
            rows=[
                _profile_row("fixturecreator", 30, "2026-06-29T13:48:30Z", packet_id=packet_id),
                _reel_row("fixturecreator", "ABC", "view_count", 100, "2026-06-29T13:48:30Z", packet_id=packet_id),
                _reel_row("fixturecreator", "ABC", "like_count", 10, "2026-06-29T13:48:30Z", packet_id=packet_id),
                _reel_row("fixturecreator", "ABC", "comment_count", 5, "2026-06-29T13:48:30Z", packet_id=packet_id),
            ],
        ),
        sort_keys=True,
    ).encode("utf-8")
    for record_id, body in (
        ("01_old_a.json", json.dumps(_projection(packet_id=packet_id, rows=[_profile_row("fixturecreator", 10, "2026-06-29T13:48:30Z", packet_id=packet_id)]), sort_keys=True).encode("utf-8")),
        ("01_old_b.json", json.dumps(_projection(packet_id=packet_id, rows=[_profile_row("fixturecreator", 20, "2026-06-29T13:48:30Z", packet_id=packet_id)]), sort_keys=True).encode("utf-8")),
        ("01_newest.json", newest_body),
        ("zz_ig_reels_grid_projection_catchup_v0_twin.json", newest_body),
    ):
        root.append_record(
            subtree="derived",
            raw_anchor=packet_id,
            lane=PROJECTION_IG_REELS_GRID_LANE,
            record_id=record_id,
            data=body,
        )

    paths = discover_instagram_reels_projection_paths_from_lake(root)
    assert sum(1 for path in paths if path.name.startswith("zz_")) == 1
    assert not any(path.name == "01_newest.json" for path in paths)

    document = build_instagram_reels_creator_metric_seed_from_files(
        projection_paths=paths,
        account_ledger={
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
        },
        generated_at_utc="2026-06-29T14:00:00Z",
    )
    seed = document["instagram_reels_creator_metric_seed"]
    assert seed["source_inputs"][0]["source_pointer"].endswith(
        "zz_ig_reels_grid_projection_catchup_v0_twin.json"
    )
    assert seed["metric_rollups"][0]["metric_rollups"]["average_views"]["value_or_none"] == 100


def test_instagram_reels_metric_seed_discovers_lake_projections_and_dedupes_exact_duplicates(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    packet_id = "01KWBMNTESWZVSVD3YASDAXK0A"
    strong_packet_id = "01KWBMNTESWZVSVD3YASDAXK0B"
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
    weak_body = json.dumps(
        _projection(
            packet_id=packet_id,
            rows=[_profile_row("fixturecreator", 10, "2026-06-29T00:00:00Z", packet_id=packet_id)],
        ),
        sort_keys=True,
    ).encode("utf-8")
    strong_body = json.dumps(
        _projection(
            packet_id=strong_packet_id,
            rows=[
                _profile_row("fixturecreator", 20, "2026-06-29T00:01:00Z", packet_id=strong_packet_id),
                _reel_row("fixturecreator", "ABC", "view_count", 100, "2026-06-29T00:01:00Z", packet_id=strong_packet_id),
                _reel_row("fixturecreator", "ABC", "like_count", 10, "2026-06-29T00:01:00Z", packet_id=strong_packet_id),
                _reel_row("fixturecreator", "ABC", "comment_count", 5, "2026-06-29T00:01:00Z", packet_id=strong_packet_id),
            ],
        ),
        sort_keys=True,
    ).encode("utf-8")

    sharded_weak = root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=PROJECTION_IG_REELS_GRID_LANE,
        record_id="weak.json",
        data=weak_body,
    )
    strong = root.append_record(
        subtree="derived",
        raw_anchor="projection_anchor_fixture",
        lane=PROJECTION_IG_REELS_GRID_LANE,
        record_id="strong.json",
        data=strong_body,
    )
    legacy_weak = root.path / "derived" / packet_id / PROJECTION_IG_REELS_GRID_LANE / "legacy_weak.json"
    legacy_weak.parent.mkdir(parents=True)
    legacy_weak.write_bytes(weak_body)

    paths = discover_instagram_reels_projection_paths_from_lake(root)

    weak_digest = hashlib.sha256(weak_body).hexdigest()
    assert len(paths) == 2
    assert strong in paths
    assert sum(1 for path in paths if hashlib.sha256(path.read_bytes()).hexdigest() == weak_digest) == 1
    assert not ({sharded_weak, legacy_weak} <= set(paths))

    document = build_instagram_reels_creator_metric_seed_from_files(
        projection_paths=paths,
        account_ledger=account_ledger,
        generated_at_utc="2026-06-29T00:02:00Z",
    )
    seed = document["instagram_reels_creator_metric_seed"]

    assert seed["counts"]["source_projection_files_supplied"] == 2
    assert seed["counts"]["source_projection_files_selected"] == 1
    assert seed["source_inputs"][0]["source_pointer"] == str(strong)
    assert seed["metric_observations"][0]["source_packet_pointer_or_none"] == str(
        root.path / "raw" / raw_shard(strong_packet_id) / strong_packet_id
    )


def test_instagram_reels_metric_seed_legacy_flat_projection_uses_flat_raw_pointer(
    tmp_path: Path,
) -> None:
    packet_id = "01KWBMNTESWZVSVD3YASDAXK0A"
    lake_root = tmp_path / "legacy-lake"
    legacy = lake_root / "derived" / packet_id / PROJECTION_IG_REELS_GRID_LANE / "legacy.json"
    legacy.parent.mkdir(parents=True)
    legacy.write_text(
        json.dumps(
            _projection(
                packet_id=packet_id,
                rows=[
                    _profile_row("fixturecreator", 20, "2026-06-29T00:01:00Z", packet_id=packet_id),
                    _reel_row("fixturecreator", "ABC", "view_count", 100, "2026-06-29T00:01:00Z", packet_id=packet_id),
                    _reel_row("fixturecreator", "ABC", "like_count", 10, "2026-06-29T00:01:00Z", packet_id=packet_id),
                    _reel_row("fixturecreator", "ABC", "comment_count", 5, "2026-06-29T00:01:00Z", packet_id=packet_id),
                ],
            ),
            sort_keys=True,
        ),
        encoding="utf-8",
    )
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

    document = build_instagram_reels_creator_metric_seed_from_files(
        projection_paths=[legacy],
        account_ledger=account_ledger,
        generated_at_utc="2026-06-29T00:02:00Z",
    )
    seed = document["instagram_reels_creator_metric_seed"]

    assert seed["source_inputs"][0]["source_pointer"] == str(legacy)
    assert seed["metric_observations"][0]["source_packet_pointer_or_none"] == str(
        lake_root / "raw" / packet_id
    )


@pytest.mark.parametrize(
    ("argv", "message"),
    [
        (
            ["--check", "--from-lake", "--projection", "fixture.json"],
            "--from-lake cannot be combined with explicit --projection files",
        ),
        (["--check", "--data-root", "C:\\tmp\\lake"], "--data-root requires --from-lake"),
        (["--check"], "provide at least one --projection or use --from-lake"),
    ],
)
def test_instagram_reels_metric_seed_runner_rejects_invalid_source_modes(
    argv: list[str], message: str, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit) as exc_info:
        metric_seed_runner.main(argv)

    assert exc_info.value.code == 2
    assert message in capsys.readouterr().err


def test_instagram_reels_metric_seed_runner_uses_explicit_projection_without_lake(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    projection = tmp_path / "projection.json"
    output = tmp_path / "seed.json"
    ledger = tmp_path / "ledger.json"
    calls: dict[str, object] = {}

    class ResolveFails:
        @staticmethod
        def resolve(*, explicit: Path | None = None) -> object:
            raise AssertionError("DataLakeRoot.resolve should not run for explicit projection mode")

    monkeypatch.setattr(metric_seed_runner, "DataLakeRoot", ResolveFails)
    monkeypatch.setattr(
        metric_seed_runner,
        "discover_instagram_reels_projection_paths_from_lake",
        lambda data_root: (_ for _ in ()).throw(AssertionError("discovery should not run")),
    )
    monkeypatch.setattr(
        metric_seed_runner,
        "load_json",
        lambda path: {"creator_public_handle_linkage_ledger": {"platform_accounts": []}},
    )

    def fake_build(*, projection_paths, account_ledger, generated_at_utc):
        calls["projection_paths"] = projection_paths
        calls["account_ledger"] = account_ledger
        calls["generated_at_utc"] = generated_at_utc
        return {"seed": True}

    monkeypatch.setattr(metric_seed_runner, "build_instagram_reels_creator_metric_seed_from_files", fake_build)
    monkeypatch.setattr(metric_seed_runner, "dump_instagram_reels_creator_metric_seed", lambda document: "rendered\n")

    result = metric_seed_runner.main(
        [
            "--write",
            "--projection",
            str(projection),
            "--account-ledger",
            str(ledger),
            "--output",
            str(output),
            "--generated-at-utc",
            "2026-06-30T00:00:00Z",
        ]
    )

    assert result == 0
    assert calls == {
        "projection_paths": [projection],
        "account_ledger": {"platform_accounts": []},
        "generated_at_utc": "2026-06-30T00:00:00Z",
    }
    assert output.read_text(encoding="utf-8") == "rendered\n"
    assert str(output) in capsys.readouterr().out


def test_instagram_reels_metric_seed_runner_from_lake_uses_discovered_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    projection = tmp_path / "projection.json"
    data_root_path = tmp_path / "lake"
    output = tmp_path / "seed.json"
    ledger = tmp_path / "ledger.json"
    resolved_root = object()
    calls: dict[str, object] = {}

    class FakeDataLakeRoot:
        @staticmethod
        def resolve(*, explicit: Path | None = None) -> object:
            calls["explicit"] = explicit
            return resolved_root

    monkeypatch.setattr(metric_seed_runner, "DataLakeRoot", FakeDataLakeRoot)

    def fake_discover(data_root: object) -> list[Path]:
        calls["data_root"] = data_root
        return [projection]

    monkeypatch.setattr(metric_seed_runner, "discover_instagram_reels_projection_paths_from_lake", fake_discover)
    monkeypatch.setattr(
        metric_seed_runner,
        "load_json",
        lambda path: {"creator_public_handle_linkage_ledger": {"platform_accounts": []}},
    )

    def fake_build(*, projection_paths, account_ledger, generated_at_utc):
        calls["projection_paths"] = projection_paths
        calls["account_ledger"] = account_ledger
        calls["generated_at_utc"] = generated_at_utc
        return {"seed": True}

    monkeypatch.setattr(metric_seed_runner, "build_instagram_reels_creator_metric_seed_from_files", fake_build)
    monkeypatch.setattr(metric_seed_runner, "dump_instagram_reels_creator_metric_seed", lambda document: "rendered\n")

    result = metric_seed_runner.main(
        [
            "--write",
            "--from-lake",
            "--data-root",
            str(data_root_path),
            "--account-ledger",
            str(ledger),
            "--output",
            str(output),
            "--generated-at-utc",
            "2026-06-30T00:00:00Z",
        ]
    )

    assert result == 0
    assert calls == {
        "explicit": data_root_path,
        "data_root": resolved_root,
        "projection_paths": [projection],
        "account_ledger": {"platform_accounts": []},
        "generated_at_utc": "2026-06-30T00:00:00Z",
    }
    assert output.read_text(encoding="utf-8") == "rendered\n"
    assert str(output) in capsys.readouterr().out


def _projection(*, rows: list[dict], packet_id: str = "packet_fixture") -> dict:
    return {
        "packet_id": packet_id,
        "rows": rows,
    }


def _profile_row(username: str, value: int, capture_time: str, *, packet_id: str = "packet_fixture") -> dict:
    return {
        "row_id": f"{packet_id}:profile:follower_count:{value}",
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
        "raw_ref": {"packet_id": packet_id, "slice_id": "ig_reels_profile_00"},
        "raw_anchor": {"file_id": "file_01", "relative_packet_path": "raw/01.json", "sha256": "a" * 64, "hash_basis": "raw_stored_bytes"},
        "chosen_source_surface": "web_profile_info_json_metadata",
        "source_surface_count_candidates": [],
        "source_publication_or_event": None,
    }


def _reel_row(
    username: str,
    shortcode: str,
    metric: str,
    value: int,
    capture_time: str,
    *,
    packet_id: str = "packet_fixture",
) -> dict:
    return {
        "row_id": f"{packet_id}:{shortcode}:{metric}",
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
        "raw_ref": {"packet_id": packet_id, "slice_id": "ig_reels_grid_01"},
        "raw_anchor": {"file_id": "file_01", "relative_packet_path": "raw/01.json", "sha256": "a" * 64, "hash_basis": "raw_stored_bytes"},
        "chosen_source_surface": "clips_user_json_metadata",
        "source_surface_count_candidates": [],
        "source_publication_or_event": capture_time,
    }
