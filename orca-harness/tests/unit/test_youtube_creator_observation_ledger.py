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


def test_youtube_shorts_fragrance_creator_observation_ledger_archived_lake_refs_when_available() -> None:
    # Explicit operator opt-in only; ambient ORCA_DATA_ROOT must never pull a
    # production lake into the suite (it is deleted per-test in conftest).
    # This ledger is a static historical fixture bound to the RETIRED lake root
    # (orca-canonical / v0), preserved as an archive outside the live lake, so it
    # takes its own opt-in variable: pointing it at the live (v4.1+) lake fails
    # closed at live_lake_root_uuid_mismatch by design. See
    # docs/decisions/youtube_creator_observation_ledger_lake_identity_drift_owner_decision_packet_v0.md.
    data_root = os.environ.get("ORCA_ARCHIVED_LAKE_TEST_ROOT")
    if not data_root:
        pytest.skip("ORCA_ARCHIVED_LAKE_TEST_ROOT is not set; archived-evidence reconciliation is an explicit operator opt-in")

    validate_youtube_creator_observation_ledger_against_live_lake(_ledger(), data_root)


def _raises_code(ledger: dict, expected_code: str) -> None:
    with pytest.raises(YoutubeCreatorObservationLedgerError) as exc_info:
        validate_youtube_creator_observation_ledger(ledger)
    assert exc_info.value.code == expected_code


def _raises_rebuild_code(ledger: dict, expected_code: str) -> None:
    with pytest.raises(YoutubeCreatorObservationLedgerError) as exc_info:
        validate_source_rebuild(ledger, _source_creator_ledger())
    assert exc_info.value.code == expected_code


def _single_ref_live_lake_ledger() -> dict:
    ledger = copy.deepcopy(_ledger())
    wrapper = _ledger_wrapper(ledger)
    # the trimmed single-video pool no longer contains the retired videos
    wrapper.pop("operator_video_retirements", None)
    row = copy.deepcopy(wrapper["creator_observations"][0])
    ref = row["data_lake_packet_refs"][0]
    row["video_ids"] = [row["video_ids"][0]]
    row["data_lake_packet_refs"] = [ref]
    row["pool_ids"] = [row["pool_ids"][0]]
    row["admitted_video_count"] = 1
    if ref["channel_id_or_none"] is None:
        row["resolved_lake_channel_ids"] = []
        row["lake_channel_id_missing_video_count"] = 1
    else:
        row["resolved_lake_channel_ids"] = [{"channel_id": ref["channel_id_or_none"], "count": 1}]
        row["lake_channel_id_missing_video_count"] = 0
    wrapper["creator_observations"] = [row]
    wrapper["counts"] = {
        **wrapper["counts"],
        "creator_observations_total": 1,
        "creator_or_channel_observed": 1 if row["creator_classification"] == "creator_or_channel_observed" else 0,
        "brand_or_platform_account_observed": 1 if row["creator_classification"] == "brand_or_platform_account_observed" else 0,
        "source_pool_rows_total": 1,
        "unique_video_ids": 1,
        "data_lake_youtube_packets_matched": 1,
        "data_lake_youtube_caption_packets": 1 if ref["source_surface"] == "youtube_captions" else 0,
        "data_lake_youtube_audio_packets": 1 if ref["source_surface"] == "youtube_audio" else 0,
        "unique_youtube_channel_ids": 1,
        "video_channel_id_missing_in_lake_metadata": row["lake_channel_id_missing_video_count"],
    }
    return ledger


def _write_live_lake_ref(root: Path, ledger: dict, *, platform_video_id: str | None = None) -> None:
    wrapper = _ledger_wrapper(ledger)
    root_uuid = next(item["root_uuid"] for item in wrapper["source_inputs"] if "root_uuid" in item)
    ref = wrapper["creator_observations"][0]["data_lake_packet_refs"][0]
    (root / ".orca-data-root").write_text(json.dumps({"root_uuid": root_uuid}), encoding="utf-8")
    packet_dir = root / ref["packet_relpath"]
    packet_dir.mkdir(parents=True)
    (packet_dir / "manifest.json").write_text(
        json.dumps(
            {
                "packet_id": ref["packet_id"],
                "source_family": "youtube",
                "source_surface": ref["source_surface"],
            }
        ),
        encoding="utf-8",
    )
    metadata_path = root / ref["metadata_relpath"]
    metadata_path.parent.mkdir(parents=True)
    metadata_path.write_text(
        json.dumps(
            {
                "platform_video_id": platform_video_id or ref["video_id"],
                "channel_id": ref["channel_id_or_none"],
            }
        ),
        encoding="utf-8",
    )


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

    _raises_code(ledger, "forbidden_youtube_observation_field")


def test_youtube_creator_observation_ledger_rejects_cross_platform_link_smuggling() -> None:
    ledger = copy.deepcopy(_ledger())
    _ledger_wrapper(ledger)["creator_observations"][0]["tiktok_public_handle"] = "samehandle"

    _raises_code(ledger, "forbidden_youtube_observation_field")


def test_youtube_creator_observation_ledger_rejects_transcript_body_smuggling() -> None:
    ledger = copy.deepcopy(_ledger())
    _ledger_wrapper(ledger)["creator_observations"][0]["transcript_body"] = "copied transcript text"

    _raises_code(ledger, "forbidden_youtube_observation_field")


def test_youtube_creator_observation_ledger_rejects_duplicate_observation_ids() -> None:
    ledger = copy.deepcopy(_ledger())
    observations = _ledger_wrapper(ledger)["creator_observations"]
    observations[1]["creator_observation_id"] = observations[0]["creator_observation_id"]

    _raises_code(ledger, "duplicate_creator_observation_id")


def test_youtube_creator_observation_ledger_rejects_duplicate_video_ids_across_rows() -> None:
    ledger = copy.deepcopy(_ledger())
    observations = _ledger_wrapper(ledger)["creator_observations"]
    observations[1]["video_ids"][0] = observations[0]["video_ids"][0]
    observations[1]["data_lake_packet_refs"][0]["video_id"] = observations[0]["video_ids"][0]

    _raises_code(ledger, "duplicate_video_id_across_ledger")


def test_youtube_creator_observation_ledger_rejects_duplicate_packet_ids_across_rows() -> None:
    ledger = copy.deepcopy(_ledger())
    observations = _ledger_wrapper(ledger)["creator_observations"]
    observations[1]["data_lake_packet_refs"][0]["packet_id"] = observations[0]["data_lake_packet_refs"][0]["packet_id"]
    observations[1]["data_lake_packet_refs"][0]["packet_relpath"] = observations[0]["data_lake_packet_refs"][0]["packet_relpath"]
    observations[1]["data_lake_packet_refs"][0]["metadata_relpath"] = observations[0]["data_lake_packet_refs"][0]["metadata_relpath"]

    _raises_code(ledger, "duplicate_packet_id_across_ledger")


def test_youtube_creator_observation_ledger_rejects_packet_video_misalignment() -> None:
    ledger = copy.deepcopy(_ledger())
    _ledger_wrapper(ledger)["creator_observations"][0]["data_lake_packet_refs"][0]["video_id"] = "DIFFERENT_VIDEO"

    _raises_code(ledger, "source_rebuild_mismatch")


def test_youtube_creator_observation_ledger_rejects_invalid_metadata_relpath() -> None:
    ledger = copy.deepcopy(_ledger())
    _ledger_wrapper(ledger)["creator_observations"][0]["data_lake_packet_refs"][0]["metadata_relpath"] = "../metadata.json"

    _raises_code(ledger, "invalid_metadata_relpath")


def test_youtube_creator_observation_ledger_rejects_invalid_metric_policy_status() -> None:
    ledger = copy.deepcopy(_ledger())
    _ledger_wrapper(ledger)["metric_rollup_policy"]["current_status"] = "present"

    _raises_code(ledger, "invalid_metric_rollup_status")


def test_youtube_creator_observation_ledger_rejects_metric_absence_as_zero() -> None:
    ledger = copy.deepcopy(_ledger())
    _ledger_wrapper(ledger)["metric_rollup_policy"]["do_not_store_absence_as_zero"] = False

    _raises_code(ledger, "metric_absence_zero_forbidden")


@pytest.mark.parametrize(
    ("field", "value", "container"),
    [
        ("tiktok_public_handle", "samehandle", "identity_boundary"),
        ("instagram_url", "https://www.instagram.com/samehandle/", "identity_boundary"),
        ("transcript_body", "copied transcript", "niche_scope"),
        ("average_views", 12345, "identity_boundary"),
        ("engagement_rate", 0.07, "niche_scope"),
    ],
)
def test_youtube_creator_observation_ledger_rejects_nested_boundary_smuggling(
    field: str, value: object, container: str
) -> None:
    ledger = copy.deepcopy(_ledger())
    _ledger_wrapper(ledger)["creator_observations"][0][container] = {field: value}

    _raises_code(ledger, "forbidden_youtube_observation_field")


def test_youtube_creator_observation_ledger_wraps_shared_forbidden_field_errors() -> None:
    ledger = copy.deepcopy(_ledger())
    _ledger_wrapper(ledger)["creator_observations"][0]["identity_boundary"] = {"email": "x@example.com"}

    _raises_code(ledger, "forbidden_output_field")


def test_youtube_creator_observation_ledger_rejects_non_string_boundary_fields() -> None:
    ledger = copy.deepcopy(_ledger())
    _ledger_wrapper(ledger)["creator_observations"][0]["identity_boundary"] = {"label": "youtube-only"}

    _raises_code(ledger, "invalid_identity_boundary")


def test_youtube_creator_observation_ledger_rebuild_rejects_source_field_drift() -> None:
    ledger = copy.deepcopy(_ledger())
    _ledger_wrapper(ledger)["creator_observations"][0]["creator_handle_query"] = "DRIFTED"

    _raises_rebuild_code(ledger, "source_rebuild_mismatch")


def test_youtube_creator_observation_ledger_rebuild_rejects_unobserved_subject_key() -> None:
    ledger = copy.deepcopy(_ledger())
    row = _ledger_wrapper(ledger)["creator_observations"][0]
    fake_channel_id = "UC00000000000000000000FAKE"
    row["platform_subject_key"] = fake_channel_id
    row["public_profile_url"] = f"https://www.youtube.com/channel/{fake_channel_id}"
    for ref in row["data_lake_packet_refs"]:
        if ref["channel_id_or_none"] is not None:
            ref["channel_id_or_none"] = fake_channel_id
    row["resolved_lake_channel_ids"] = [{"channel_id": fake_channel_id, "count": row["admitted_video_count"]}]

    _raises_rebuild_code(ledger, "source_platform_subject_key_mismatch")


def test_youtube_creator_observation_ledger_rebuild_rejects_source_input_hash_drift() -> None:
    ledger = copy.deepcopy(_ledger())
    _ledger_wrapper(ledger)["source_inputs"][0]["sha256"] = "0" * 64

    _raises_rebuild_code(ledger, "source_input_hash_mismatch")


def test_youtube_creator_observation_ledger_live_lake_mismatch_uses_live_error_code(tmp_path: Path) -> None:
    ledger = _single_ref_live_lake_ledger()
    _write_live_lake_ref(tmp_path, ledger, platform_video_id="WRONG_VIDEO")

    with pytest.raises(YoutubeCreatorObservationLedgerError) as exc_info:
        validate_youtube_creator_observation_ledger_against_live_lake(ledger, tmp_path)
    assert exc_info.value.code == "live_lake_metadata_mismatch"


# -- operator_video_retirements (additive-optional dead-video retirement block) --

_DEAD_VIDEO_IDS = (
    "DUafgG-TLms",
    "JcwT5rvhXIc",
    "ZRxgla8xoM8",
    "as7hye0qgYc",
    "doNVRDk0X_Y",
    "syjxpoKWbRM",
)


def _retirements(ledger: dict) -> list[dict]:
    return _ledger_wrapper(ledger)["operator_video_retirements"]


def test_committed_ledger_carries_dead_video_retirements() -> None:
    ledger = _ledger()
    validate_youtube_creator_observation_ledger(ledger)

    entries = _retirements(ledger)
    assert sorted(entry["video_id"] for entry in entries) == sorted(_DEAD_VIDEO_IDS)
    for entry in entries:
        assert "playabilityStatus ERROR" in entry["reason"]
        assert len(entry["evidence_packet_ids"]) >= 3


def test_retirement_block_is_optional() -> None:
    ledger = copy.deepcopy(_ledger())
    del _ledger_wrapper(ledger)["operator_video_retirements"]

    validate_youtube_creator_observation_ledger(ledger)


def test_retirement_unknown_field_rejected() -> None:
    ledger = copy.deepcopy(_ledger())
    _retirements(ledger)[0]["became_playable_again"] = True

    _raises_code(ledger, "unknown_field")


def test_retirement_missing_field_rejected() -> None:
    ledger = copy.deepcopy(_ledger())
    del _retirements(ledger)[0]["reason"]

    _raises_code(ledger, "missing_reason")


def test_retirement_outside_pool_rejected() -> None:
    ledger = copy.deepcopy(_ledger())
    _retirements(ledger)[0]["video_id"] = "AAAAAAAAAAA"

    _raises_code(ledger, "retirement_video_not_in_pool")


def test_retirement_duplicate_rejected() -> None:
    ledger = copy.deepcopy(_ledger())
    entries = _retirements(ledger)
    entries.append(copy.deepcopy(entries[0]))

    _raises_code(ledger, "duplicate_retirement_video_id")


def test_retirement_empty_reason_rejected() -> None:
    ledger = copy.deepcopy(_ledger())
    _retirements(ledger)[0]["reason"] = "  "

    _raises_code(ledger, "invalid_retirement_reason")


def test_retirement_bad_timestamp_rejected() -> None:
    ledger = copy.deepcopy(_ledger())
    _retirements(ledger)[0]["retired_at_utc"] = "2026-07-03"

    _raises_code(ledger, "invalid_retirement_timestamp")


def test_retirement_bad_or_empty_evidence_rejected() -> None:
    ledger = copy.deepcopy(_ledger())
    _retirements(ledger)[0]["evidence_packet_ids"] = ["not-a-ulid"]
    _raises_code(ledger, "invalid_retirement_evidence")

    ledger = copy.deepcopy(_ledger())
    _retirements(ledger)[0]["evidence_packet_ids"] = []
    _raises_code(ledger, "invalid_retirement_evidence")


def test_retirement_empty_block_rejected() -> None:
    ledger = copy.deepcopy(_ledger())
    _ledger_wrapper(ledger)["operator_video_retirements"] = []

    _raises_code(ledger, "invalid_operator_video_retirements")
