"""Unit tests for the TikTok batch-admission creator-metric seed builder.

Fixture packets are committed through the REAL packet-assembly writer
(``stage_and_write_packet``) into ``DataLakeRoot.for_test`` so the builder's
verified by-key reads (manifest sha256s, preserved-file ids) are exercised
end-to-end, while the preserved ``tiktok_batch_capture.json`` payload stays
under direct test control -- required because the batch writer's
``_normalize_stats`` zero-fills missing stats keys at write time, and the gap /
non-integer fail-closed cases need payloads the writer would never emit. The
happy-path video shape mirrors the real funmimonet lake packet
(videos[].video_id/stats with exact playCount/diggCount/commentCount/
shareCount/collectCount integers).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from capture_spine.creator_profile_current.tiktok_metric_seed import (
    TIKTOK_BATCH_CREATOR_METRIC_SEED_WRAPPER,
    TIKTOK_BATCH_METRIC_RECIPE_VERSION,
    TiktokBatchMetricDocumentError,
    build_tiktok_batch_creator_metric_seed_document,
    discover_latest_tiktok_batch_captures,
)
from data_lake.root import DataLakeRoot
from source_capture.models import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
)
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map
from source_capture.tiktok.batch_packet import (
    TIKTOK_BATCH_CAPTURE_JSON_NAME,
    TIKTOK_BATCH_CAPTURE_SCHEMA_VERSION,
    TIKTOK_BATCH_CAPTURE_SURFACE,
    TIKTOK_BATCH_NON_CLAIMS,
)

HANDLE = "funmimonet"
CAPTURE_T1 = "2026-06-30T17:48:37Z"
GENERATED_AT = "2026-07-01T12:00:00Z"
ACCOUNT_MAP = {"funmimonet": "acct_tt_funmimonet", "scentwithbee": "acct_tt_scentwithbee"}


def _stats(play: int, digg: int, comment: int, share: int = 29, collect: int = 163) -> dict:
    return {
        "playCount": play,
        "diggCount": digg,
        "commentCount": comment,
        "shareCount": share,
        "collectCount": collect,
    }


def _video(
    video_id: str,
    *,
    stats: dict,
    handle: str = HANDLE,
    create_time_utc: str = "2026-06-25T03:00:41Z",
) -> dict:
    """One preserved batch video row mirroring the real funmimonet packet shape
    (non-metric blocks trimmed to the fields the seed layer never reads)."""
    return {
        "source_index": 0,
        "video_id": video_id,
        "video_url": f"https://www.tiktok.com/@{handle}/video/{video_id}",
        "url_path": f"/@{handle}/video/{video_id}",
        "status": "completed",
        "create_time_utc": create_time_utc,
        "stats": stats,
        "source_text": {"desc": "fixture", "hashtags": [], "mentions": []},
        "comments": {"posture": "not_observed", "captured_comment_count": 0, "comments": []},
        "subtitles": {"posture": "no_subtitleInfos_present", "cue_count": 0, "cues": []},
        "limitations": list(TIKTOK_BATCH_NON_CLAIMS),
    }


def _commit_batch_packet(
    data_root: DataLakeRoot,
    *,
    videos: list[dict],
    handle: str = HANDLE,
    capture_timestamp: str = CAPTURE_T1,
    operator_category: str = "tiktok_batch_admission_cli_operator",
) -> str:
    """Commit a real-shape TikTok batch-admission packet with a test-controlled
    preserved payload; returns the packet id."""
    profile_url = f"https://www.tiktok.com/@{handle}"
    payload = {
        "capture_schema_version": TIKTOK_BATCH_CAPTURE_SCHEMA_VERSION,
        "platform": "tiktok",
        "source_surface": TIKTOK_BATCH_CAPTURE_SURFACE,
        "creator_handle": handle,
        "creator_profile_url": profile_url,
        "batch_label": "fixture_batch",
        "capture_timestamp": capture_timestamp,
        "videos": videos,
        "non_claims": list(TIKTOK_BATCH_NON_CLAIMS),
    }
    staged = [
        (TIKTOK_BATCH_CAPTURE_JSON_NAME, json.dumps(payload, ensure_ascii=False).encode("utf-8"))
    ]
    file_ids = staged_file_id_map(staged)
    timing = PacketTiming(
        source_publication_or_event=known_fact("fixture creator batch window"),
        source_edit_or_version=not_applicable("fixture batch packet"),
        capture_time=known_fact(capture_timestamp),
        recapture_time=not_applicable("fixture batch packet"),
        cutoff_posture=not_applicable("fixture batch packet"),
    )
    access = known_fact("sanitized parsed TikTok staging admission (fixture)")
    archive = not_attempted("fixture batch packet does not query archive services")
    media = known_fact("parsed fields preserved; no raw media bytes (fixture)")
    recapture = not_applicable("fixture batch packet")
    limitations = list(TIKTOK_BATCH_NON_CLAIMS)
    result = stage_and_write_packet(
        data_root=data_root,
        staged_artifacts=staged,
        source_slices=[
            SourceCaptureSlice(
                slice_id="tiktok_batch_admission_01",
                locator=known_fact(profile_url),
                timing=timing,
                access_posture=access,
                archive_history_posture=archive,
                media_modality_posture=media,
                re_capture_relationship=recapture,
                limitations=limitations,
                warning_notes=[],
                preserved_file_ids=[file_ids[TIKTOK_BATCH_CAPTURE_JSON_NAME]],
            )
        ],
        source_family="tiktok",
        source_surface=TIKTOK_BATCH_CAPTURE_SURFACE,
        source_locator=known_fact(profile_url),
        decision_question="fixture: TikTok batch metric admission",
        capture_context="fixture TikTok parsed creator-batch admission",
        actor_audience_context=not_applicable("fixture batch packet"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category=operator_category,
        session_identity=None,
        visible_mode_changes=["tiktok_sci_admission:parsed_creator_batch"],
        source_publication_or_event=timing.source_publication_or_event,
        source_edit_or_version=timing.source_edit_or_version,
        cutoff_posture=timing.cutoff_posture,
        recapture_time=timing.recapture_time,
        access_posture=access,
        archive_history_posture=archive,
        media_modality_posture=media,
        re_capture_relationship=recapture,
        warnings=[],
        limitations=limitations,
        receipt_summary=f"fixture TikTok batch admission for @{handle}",
        receipt_non_claims=TIKTOK_BATCH_NON_CLAIMS,
    )
    data_root.rebuild_availability()
    return Path(result.output_directory).name


def _two_video_lake(tmp_path: Path) -> tuple[DataLakeRoot, str]:
    """Two-complete-video funmimonet batch with the real lake packet's numbers."""
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id = _commit_batch_packet(
        data_root,
        videos=[
            _video("7655162561783975199", stats=_stats(10800, 1625, 96, share=29, collect=163)),
            _video("7655162561783975200", stats=_stats(43000, 5936, 228, share=175, collect=1492)),
        ],
    )
    return data_root, packet_id


def _seed(document: dict) -> dict:
    return document[TIKTOK_BATCH_CREATOR_METRIC_SEED_WRAPPER]


def _observations_by_video_metric(seed: dict) -> dict[tuple[str, str], dict]:
    return {
        (obs["content_id_or_none"], obs["metric_name"]): obs
        for obs in seed["metric_observations"]
    }


def test_document_maps_source_stats_to_metric_observations(tmp_path: Path) -> None:
    data_root, packet_id = _two_video_lake(tmp_path)
    document = build_tiktok_batch_creator_metric_seed_document(
        data_root, account_id_by_handle=ACCOUNT_MAP, generated_at_utc=GENERATED_AT
    )
    seed = _seed(document)

    # 2 videos x 5 named metrics, all observed (the packet carries exact ints).
    assert len(seed["metric_observations"]) == 10
    assert all(obs["metric_posture"] == "observed" for obs in seed["metric_observations"])
    by_key = _observations_by_video_metric(seed)
    first = "7655162561783975199"
    assert by_key[(first, "view_count")]["metric_value_or_none"] == 10800
    assert by_key[(first, "like_count")]["metric_value_or_none"] == 1625
    assert by_key[(first, "total_comment_count")]["metric_value_or_none"] == 96
    assert by_key[(first, "share_count")]["metric_value_or_none"] == 29
    assert by_key[(first, "collect_count")]["metric_value_or_none"] == 163

    view = by_key[(first, "view_count")]
    assert view["platform"] == "tiktok"
    assert view["platform_subject_key"] == HANDLE
    assert view["platform_account_id"] == "acct_tt_funmimonet"
    assert view["source_packet_id_or_none"] == packet_id
    assert view["source_field"] == "/videos/0/stats/playCount"
    assert view["source_pointer"].endswith("#/videos/0/stats/playCount")
    assert view["observed_at"] == CAPTURE_T1

    # The raw anchor is the manifest-backed provenance of the preserved capture.
    anchor = view["raw_anchor"]
    assert anchor["relative_packet_path"] == f"raw/01_{TIKTOK_BATCH_CAPTURE_JSON_NAME}"
    manifest = json.loads(
        (data_root.find_packet(packet_id) / "manifest.json").read_text(encoding="utf-8")
    )
    assert anchor["sha256"] == manifest["preserved_files"][0]["sha256"]
    assert anchor["file_id"] == manifest["preserved_files"][0]["file_id"]

    assert seed["counts"]["metric_observations_total"] == 10
    assert seed["counts"]["engagement_rate_rollups_observed"] == 1


def test_rollup_engagement_math_pinned_to_hand_computed_values(tmp_path: Path) -> None:
    data_root, _packet_id = _two_video_lake(tmp_path)
    document = build_tiktok_batch_creator_metric_seed_document(
        data_root, account_id_by_handle=ACCOUNT_MAP, generated_at_utc=GENERATED_AT
    )
    seed = _seed(document)
    assert len(seed["metric_rollups"]) == 1
    rollup = seed["metric_rollups"][0]
    metrics = rollup["metric_rollups"]

    # Hand-computed: (1625 + 5936 + 96 + 228) / (10800 + 43000) = 7885 / 53800.
    assert metrics["engagement_rate"]["value_or_none"] == 0.146561
    assert metrics["engagement_rate"]["posture"] == "observed"
    assert metrics["average_views"]["value_or_none"] == 26900.0
    assert metrics["median_views"]["value_or_none"] == 26900.0
    assert metrics["average_like_count"]["value_or_none"] == 3780.5
    assert metrics["average_comment_count"]["value_or_none"] == 162.0
    assert metrics["posting_cadence"]["posture"] == "not_attempted"
    assert metrics["recent_velocity"]["posture"] == "not_attempted"
    assert rollup["view_count_min"] == 10800
    assert rollup["view_count_max"] == 43000
    assert rollup["calculation_recipe_version"] == TIKTOK_BATCH_METRIC_RECIPE_VERSION

    # Rollup sources are the engagement trio only -- share/collect observations
    # are preserved but never rollup inputs.
    assert rollup["observation_count"] == 6
    assert len(rollup["source_metric_observation_ids"]) == 6
    trio_names = {"view_count", "like_count", "total_comment_count"}
    obs_by_id = {obs["metric_observation_id"]: obs for obs in seed["metric_observations"]}
    assert {
        obs_by_id[source_id]["metric_name"]
        for source_id in rollup["source_metric_observation_ids"]
    } == trio_names

    # The required rollup limitations are stated.
    joined = " ".join(rollup["limitations"])
    assert "profile-grid batch selection only" in joined
    assert "capture-time observations" in joined
    assert "not a representative creator average" in joined
    assert "complete-input videos only" in joined


def test_missing_stat_key_is_a_loud_gap_never_zero(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    gap_stats = _stats(5000, 250, 50)
    del gap_stats["diggCount"]
    _commit_batch_packet(
        data_root,
        videos=[
            _video("7655162561783975199", stats=_stats(10800, 1625, 96)),
            _video("7655162561783975201", stats=gap_stats),
        ],
    )
    document = build_tiktok_batch_creator_metric_seed_document(
        data_root, account_id_by_handle=ACCOUNT_MAP, generated_at_utc=GENERATED_AT
    )
    seed = _seed(document)

    gap = _observations_by_video_metric(seed)[("7655162561783975201", "like_count")]
    assert gap["metric_posture"] == "unavailable_with_reason"
    assert gap["metric_value_or_none"] is None
    assert "never zero-filled" in gap["posture_reason_or_none"]
    # No observation was zero-filled for the absent stat.
    assert not any(
        obs["metric_name"] == "like_count" and obs["metric_value_or_none"] == 0
        for obs in seed["metric_observations"]
    )

    # The partial-input video is excluded from ALL rollup math (complete trios only).
    rollup = seed["metric_rollups"][0]
    assert rollup["metric_rollups"]["average_views"]["value_or_none"] == 10800.0
    assert rollup["metric_rollups"]["engagement_rate"]["value_or_none"] == round(
        (1625 + 96) / 10800, 6
    )
    assert rollup["observation_count"] == 3
    assert "complete for 1 of 2 captured videos" in " ".join(rollup["limitations"])


def test_absent_stats_object_makes_every_metric_a_gap(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    no_stats = _video("7655162561783975201", stats={})
    del no_stats["stats"]
    _commit_batch_packet(
        data_root,
        videos=[_video("7655162561783975199", stats=_stats(10800, 1625, 96)), no_stats],
    )
    document = build_tiktok_batch_creator_metric_seed_document(
        data_root, account_id_by_handle=ACCOUNT_MAP, generated_at_utc=GENERATED_AT
    )
    seed = _seed(document)
    gap_rows = [
        obs
        for obs in seed["metric_observations"]
        if obs["content_id_or_none"] == "7655162561783975201"
    ]
    assert len(gap_rows) == 5
    assert all(obs["metric_posture"] == "unavailable_with_reason" for obs in gap_rows)
    assert all(obs["metric_value_or_none"] is None for obs in gap_rows)


@pytest.mark.parametrize("bad_value", ["1.2M", 1.5, True])
def test_non_integer_stat_fails_closed(tmp_path: Path, bad_value: object) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    stats = _stats(10800, 1625, 96)
    stats["playCount"] = bad_value
    _commit_batch_packet(data_root, videos=[_video("7655162561783975199", stats=stats)])
    with pytest.raises(TiktokBatchMetricDocumentError, match="non_integer_stat"):
        build_tiktok_batch_creator_metric_seed_document(
            data_root, account_id_by_handle=ACCOUNT_MAP, generated_at_utc=GENERATED_AT
        )


def test_video_without_video_id_fails_closed(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    video = _video("7655162561783975199", stats=_stats(10800, 1625, 96))
    del video["video_id"]
    _commit_batch_packet(data_root, videos=[video])
    with pytest.raises(TiktokBatchMetricDocumentError, match="lacks a video_id"):
        build_tiktok_batch_creator_metric_seed_document(
            data_root, account_id_by_handle=ACCOUNT_MAP, generated_at_utc=GENERATED_AT
        )


def test_duplicate_video_id_fails_closed(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_batch_packet(
        data_root,
        videos=[
            _video("7655162561783975199", stats=_stats(10800, 1625, 96)),
            _video("7655162561783975199", stats=_stats(43000, 5936, 228)),
        ],
    )
    with pytest.raises(TiktokBatchMetricDocumentError, match="repeats video_id"):
        build_tiktok_batch_creator_metric_seed_document(
            data_root, account_id_by_handle=ACCOUNT_MAP, generated_at_utc=GENERATED_AT
        )


def test_unmapped_creator_handle_fails_closed_with_clear_message(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_batch_packet(data_root, videos=[_video("7655162561783975199", stats=_stats(10800, 1625, 96))])
    with pytest.raises(TiktokBatchMetricDocumentError) as excinfo:
        build_tiktok_batch_creator_metric_seed_document(
            data_root,
            account_id_by_handle={"someoneelse": "acct_tt_other"},
            generated_at_utc=GENERATED_AT,
        )
    message = str(excinfo.value)
    assert "missing_account_mapping" in message
    assert "@funmimonet" in message
    assert "--account-map" in message


def test_empty_lake_fails_closed(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    with pytest.raises(TiktokBatchMetricDocumentError, match="no_tiktok_batch_packets"):
        build_tiktok_batch_creator_metric_seed_document(
            data_root, account_id_by_handle=ACCOUNT_MAP, generated_at_utc=GENERATED_AT
        )


def test_latest_packet_wins_and_timestamp_ties_fail_closed(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_batch_packet(
        data_root,
        videos=[_video("7655162561783975199", stats=_stats(100, 10, 1))],
        capture_timestamp="2026-06-29T00:00:00Z",
    )
    later = _commit_batch_packet(
        data_root,
        videos=[_video("7655162561783975199", stats=_stats(10800, 1625, 96))],
        capture_timestamp=CAPTURE_T1,
    )
    captures = discover_latest_tiktok_batch_captures(data_root)
    assert captures[HANDLE].packet_id == later

    _commit_batch_packet(
        data_root,
        videos=[_video("7655162561783975199", stats=_stats(200, 20, 2))],
        capture_timestamp=CAPTURE_T1,  # distinct packet, same timestamp
    )
    with pytest.raises(TiktokBatchMetricDocumentError, match="ambiguous_creator_packet"):
        discover_latest_tiktok_batch_captures(data_root)


def test_operator_category_mismatch_fails_closed(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_batch_packet(
        data_root,
        videos=[_video("7655162561783975199", stats=_stats(10800, 1625, 96))],
        operator_category="some_other_operator",
    )
    with pytest.raises(TiktokBatchMetricDocumentError, match="operator_category_mismatch"):
        discover_latest_tiktok_batch_captures(data_root)


def test_account_with_no_complete_trio_fails_closed(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    stats = _stats(10800, 1625, 96)
    del stats["commentCount"]
    _commit_batch_packet(data_root, videos=[_video("7655162561783975199", stats=stats)])
    with pytest.raises(TiktokBatchMetricDocumentError, match="no_complete_video_trios"):
        build_tiktok_batch_creator_metric_seed_document(
            data_root, account_id_by_handle=ACCOUNT_MAP, generated_at_utc=GENERATED_AT
        )


def test_zero_view_denominator_makes_engagement_unavailable(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_batch_packet(
        data_root,
        videos=[_video("7655162561783975199", stats=_stats(0, 5, 1, share=0, collect=0))],
    )
    document = build_tiktok_batch_creator_metric_seed_document(
        data_root, account_id_by_handle=ACCOUNT_MAP, generated_at_utc=GENERATED_AT
    )
    engagement = _seed(document)["metric_rollups"][0]["metric_rollups"]["engagement_rate"]
    assert engagement["posture"] == "unavailable_with_reason"
    assert engagement["value_or_none"] is None
