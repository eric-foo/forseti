from __future__ import annotations

import copy
import json
import os
from pathlib import Path

import pytest

from capture_spine.creator_public_handle_linkage.validation import assert_no_forbidden_output_fields
from capture_spine.youtube_creator_observation import (
    YoutubeCreatorObservationLedgerError,
    load_youtube_creator_observation_ledger,
    validate_source_rebuild,
    validate_youtube_creator_observation_ledger,
    validate_youtube_creator_observation_ledger_against_live_lake,
)


LEDGER_PATH = (
    Path(__file__).resolve().parents[3]
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
SOURCE_CREATOR_LEDGER_PATH = (
    Path(__file__).resolve().parents[3]
    / "docs"
    / "review-inputs"
    / "youtube_shorts_fragrance_creator_ledger_v0.json"
)


def _ledger() -> dict:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def _ledger_wrapper(ledger: dict | None = None) -> dict:
    return (ledger or _ledger())["youtube_creator_observation_ledger"]


def _source_creator_ledger() -> dict:
    return json.loads(SOURCE_CREATOR_LEDGER_PATH.read_text(encoding="utf-8"))


def test_youtube_shorts_fragrance_creator_observation_ledger_counts_and_refs() -> None:
    wrapper = _ledger_wrapper()
    loaded = load_youtube_creator_observation_ledger(LEDGER_PATH)

    assert _ledger_wrapper(loaded) == wrapper
    assert wrapper["schema_version"] == "youtube_creator_observation_ledger_v0"
    assert wrapper["ledger_mode"] == "source_backed_static_fixture"

    observations = wrapper["creator_observations"]
    counts = wrapper["counts"]

    assert counts["creator_observations_total"] == len(observations) == 31
    assert counts["creator_or_channel_observed"] == 30
    assert counts["brand_or_platform_account_observed"] == 1
    assert sum(row["admitted_video_count"] for row in observations) == 200

    video_ids = [video_id for row in observations for video_id in row["video_ids"]]
    packet_refs = [ref for row in observations for ref in row["data_lake_packet_refs"]]
    packet_ids = [ref["packet_id"] for ref in packet_refs]

    assert len(video_ids) == len(set(video_ids)) == counts["unique_video_ids"] == 200
    assert len(packet_refs) == counts["data_lake_youtube_packets_matched"] == 200
    assert len(packet_ids) == len(set(packet_ids)) == 200
    assert counts["data_lake_youtube_caption_packets"] == 199
    assert counts["data_lake_youtube_audio_packets"] == 1
    assert counts["unique_youtube_channel_ids"] == 31
    assert (
        sum(1 for ref in packet_refs if ref["channel_id_or_none"] is None)
        == counts["video_channel_id_missing_in_lake_metadata"]
        == 1
    )


def test_youtube_shorts_fragrance_creator_observation_ledger_boundaries() -> None:
    wrapper = _ledger_wrapper()
    assert_no_forbidden_output_fields({"youtube_creator_observation_ledger": wrapper})

    assert wrapper["metric_rollup_policy"]["current_status"] == (
        "not_present_in_current_caption_audio_lake_packets"
    )
    assert wrapper["metric_rollup_policy"]["do_not_store_absence_as_zero"] is True
    assert "not cross-platform identity linkage" in wrapper["non_claims"]
    assert "not metric rollup" in wrapper["non_claims"]
    assert "not SQLite migration" in wrapper["non_claims"]
    assert "not runtime capture authorization" in wrapper["non_claims"]

    for forbidden_metric in ("average_views", "engagement_rate", "views", "likes"):
        assert forbidden_metric not in wrapper

    for observation in wrapper["creator_observations"]:
        assert observation["platform"] == "youtube"
        assert observation["platform_subject_key_type"] == "youtube_channel_id"
        assert observation["platform_subject_key"].startswith("UC")
        assert "not cross-platform identity linkage" in observation["non_claims"]
        assert "not metric rollup" in observation["non_claims"]
        assert "transcript_body" not in observation
        assert "transcript_text" not in observation
        assert "caption_text" not in observation


def test_youtube_shorts_fragrance_creator_observation_ledger_rebuilds_from_source() -> None:
    validate_source_rebuild(_ledger(), _source_creator_ledger())


def test_youtube_shorts_fragrance_creator_observation_ledger_live_lake_refs_when_available() -> None:
    data_root = os.environ.get("ORCA_DATA_ROOT")
    if not data_root:
        pytest.skip("ORCA_DATA_ROOT is not set; live lake reconciliation is an operator-local check")

    validate_youtube_creator_observation_ledger_against_live_lake(_ledger(), data_root)


def _raises_code(ledger: dict, expected_code: str) -> None:
    with pytest.raises(YoutubeCreatorObservationLedgerError) as exc_info:
        validate_youtube_creator_observation_ledger(ledger)
    assert exc_info.value.code == expected_code


def test_youtube_creator_observation_ledger_rejects_duplicate_video_ids() -> None:
    ledger = copy.deepcopy(_ledger())
    row = _ledger_wrapper(ledger)["creator_observations"][0]
    row["video_ids"][1] = row["video_ids"][0]
    row["data_lake_packet_refs"][1]["video_id"] = row["video_ids"][0]

    _raises_code(ledger, "duplicate_video_id_in_row")


def test_youtube_creator_observation_ledger_rejects_missing_packet_ref() -> None:
    ledger = copy.deepcopy(_ledger())
    row = _ledger_wrapper(ledger)["creator_observations"][0]
    row["data_lake_packet_refs"].pop()

    _raises_code(ledger, "packet_ref_count_mismatch")


def test_youtube_creator_observation_ledger_rejects_channel_mismatch() -> None:
    ledger = copy.deepcopy(_ledger())
    row = _ledger_wrapper(ledger)["creator_observations"][0]
    row["data_lake_packet_refs"][0]["channel_id_or_none"] = "UC_DIFFERENT_PUBLIC_CHANNEL"

    _raises_code(ledger, "packet_ref_channel_mismatch")


def test_youtube_creator_observation_ledger_rejects_metric_smuggling() -> None:
    ledger = copy.deepcopy(_ledger())
    _ledger_wrapper(ledger)["creator_observations"][0]["average_views"] = 12345

    _raises_code(ledger, "unknown_field")


def test_youtube_creator_observation_ledger_rejects_cross_platform_link_smuggling() -> None:
    ledger = copy.deepcopy(_ledger())
    _ledger_wrapper(ledger)["creator_observations"][0]["tiktok_public_handle"] = "samehandle"

    _raises_code(ledger, "unknown_field")


def test_youtube_creator_observation_ledger_rejects_transcript_body_smuggling() -> None:
    ledger = copy.deepcopy(_ledger())
    _ledger_wrapper(ledger)["creator_observations"][0]["transcript_body"] = "copied transcript text"

    _raises_code(ledger, "unknown_field")
