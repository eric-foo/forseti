from __future__ import annotations

import json
from pathlib import Path

from capture_spine.creator_public_handle_linkage.validation import assert_no_forbidden_output_fields


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


def _ledger_wrapper() -> dict:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))[
        "youtube_creator_observation_ledger"
    ]


def test_youtube_shorts_fragrance_creator_observation_ledger_counts_and_refs() -> None:
    wrapper = _ledger_wrapper()
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

    for observation in wrapper["creator_observations"]:
        assert observation["platform"] == "youtube"
        assert observation["platform_subject_key_type"] == "youtube_channel_id"
        assert observation["platform_subject_key"].startswith("UC")
        assert "not cross-platform identity linkage" in observation["non_claims"]
        assert "not metric rollup" in observation["non_claims"]
        assert "transcript_body" not in observation
        assert "transcript_text" not in observation
        assert "caption_text" not in observation
