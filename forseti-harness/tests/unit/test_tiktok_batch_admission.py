from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, raw_shard
from runners.run_source_capture_tiktok_batch_packet import main as tiktok_batch_main, run_source_capture_tiktok_batch_packet
from source_capture.models import SourceCapturePacket
from source_capture.tiktok import COMPLETE_LANE_NOTE
from source_capture.tiktok.batch_packet import _normalize_stats, write_tiktok_batch_packet

VIDEO_1 = "7629774409762442526"
VIDEO_2 = "7629774409762442527"
VIDEO_3 = "7629774409762442528"
PROFILE_URL = "https://www.tiktok.com/@funmimonet"


def _contract() -> dict[str, object]:
    return {
        "captcha_solving": False,
        "cookies_or_tokens_persisted": False,
        "direct_forged_api_calls": False,
        "dom_visible_comment_fallback": True,
        "page_owned_comment_list_response": True,
        "page_owned_video_navigation": True,
        "raw_comment_response_bodies_persisted": False,
        "raw_endpoint_urls_persisted": False,
        "raw_subtitle_bodies_persisted": False,
        "raw_subtitle_urls_persisted": False,
        "staging_only": True,
        "stop_on_challenge": True,
        "subtitle_tier": "source_native_subtitle_webvtt_when_present",
    }


def _grid_payload() -> bytes:
    return json.dumps(
        {
            "capture_contract": _contract(),
            "response_items": [
                {
                    "id": VIDEO_1,
                    "authorUniqueId": "funmimonet",
                    "desc": "Burberry Goddess with @Burberry Beauty #BurberryPartner #fragrance",
                    "createTime": 1761930827,
                    "decoded_aweme_id_create_time_utc": "2025-10-31T17:13:47Z",
                    "stats": {"playCount": 1000, "diggCount": 45, "commentCount": 12, "shareCount": 3, "collectCount": 7},
                    "music": {"title": "original sound", "authorName": "Funmi Monet", "original": True},
                    "source_response_path": "/api/post/item_list/",
                    "source_response_url_sha256": "grid1sha",
                },
                {
                    "id": VIDEO_2,
                    "authorUniqueId": "funmimonet",
                    "desc": "Trying a travel spray #ad #perfume",
                    "createTime": 1761930927,
                    "stats": {"playCount": 2000, "diggCount": 90, "commentCount": 20, "shareCount": 4, "collectCount": 11},
                    "music": {"title": "sound two", "authorName": "Creator"},
                    "source_response_path": "/api/post/item_list/",
                    "source_response_url_sha256": "grid2sha",
                },
                {"id": "9999999999999999999", "authorUniqueId": "other", "desc": "not this creator"},
            ],
        }
    ).encode("utf-8")


def _cadence_payload() -> bytes:
    return json.dumps(
        {
            "attempted_count": 2,
            "completed_count": 2,
            "challenge_count": 0,
            "run_complete_utc": "2026-06-30T17:02:46Z",
            "capture_contract": _contract(),
            "results": [_result_row(VIDEO_1, 1761930827, subtitle=True), _result_row(VIDEO_2, 1761930927, subtitle=False)],
        }
    ).encode("utf-8")


def _onboarding_evidence_payloads() -> tuple[bytes, bytes]:
    grid = {
        "schema_version": "tiktok_creator_onboarding_v0",
        "creator_handle": "funmimonet",
        "window_size": 3,
        "window_cap": 30,
        "minimum_window_size": 2,
        "complete": True,
        "items": [
            {
                "video_id": VIDEO_1,
                "video_url": f"{PROFILE_URL}/video/{VIDEO_1}",
                "playCount": 1000,
                "diggCount": 45,
            },
            {
                "video_id": VIDEO_2,
                "video_url": f"{PROFILE_URL}/video/{VIDEO_2}",
                "playCount": 2000,
                "diggCount": 90,
            },
            {
                "video_id": VIDEO_3,
                "video_url": f"{PROFILE_URL}/video/{VIDEO_3}",
                "playCount": 500,
                "diggCount": 20,
            },
        ],
    }
    grid_bytes = (json.dumps(grid, indent=2, sort_keys=True) + "\n").encode("utf-8")
    selection = {
        "schema_version": "tiktok_grid_video_selection_v1",
        "coverage": {
            "complete": True,
            "expected_item_count": 3,
            "observed_item_count": 3,
        },
        "onboarding_binding": {
            "creator_handle": "funmimonet",
            "grid_window_file": "tiktok_grid_window.json",
            "grid_window_sha256": hashlib.sha256(grid_bytes).hexdigest(),
        },
        "ranked_items": [
            {"video_id": VIDEO_2, "selected": True},
            {"video_id": VIDEO_1, "selected": True},
            {"video_id": VIDEO_3, "selected": False},
        ],
        "selection_summary": {
            "selection_count": 2,
            "selected_video_ids_in_review_priority_order": [VIDEO_2, VIDEO_1],
        },
    }
    selection_bytes = (json.dumps(selection, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    return grid_bytes, selection_bytes


def _result_row(video_id: str, create_time: int, *, subtitle: bool) -> dict[str, object]:
    base = {
        "video_id": video_id,
        "url_path": f"/@funmimonet/video/{video_id}",
        "status": "completed",
        "grid_candidate": {
            "video_id": video_id,
            "url_path": f"/@funmimonet/video/{video_id}",
            "createTime": create_time,
            "stats": {"playCount": 1, "diggCount": 2, "commentCount": 3, "shareCount": 4, "collectCount": 5},
        },
        "comment_responses": [
            {
                "ok": True,
                "status": 200,
                "observed_utc": "2026-06-30T17:00:00Z",
                "url_summary": {"path": "/api/comment/list", "query_key_count": 12, "url_sha256": f"{video_id}urlsha"},
                "body_assessment": {
                    "body_present": True,
                    "body_byte_count": 1234,
                    "body_sha256": f"{video_id}bodysha",
                    "comment_count": 1,
                    "json_parse_ok": True,
                    "envelope": {"cursor": 20, "has_more": 1, "total": 10 if subtitle else 3},
                    "field_coverage": {"cid": True, "uid": True},
                    "comments": [
                        {
                            "cid": f"cid-{video_id[-3:]}",
                            "text": "I need to smell this" if subtitle else "where can I buy it?",
                            "create_time": 1761931000,
                            "digg_count": 9,
                            "reply_comment_total": 1,
                            "user": {"uid": "42", "unique_id": "viewer", "nickname": "Viewer"},
                        }
                    ],
                },
            }
        ],
    }
    if subtitle:
        base["hydration"] = {"subtitle_info_count": 1, "subtitle_infos_sanitized": [{"Format": "webvtt", "LanguageCodeName": "eng-US", "Source": "ASR", "Size": 99}]}
        base["subtitle"] = {
            "success": True,
            "body_byte_count": 456,
            "body_sha256": "subtitlebodysha",
            "subtitle_url_sha256": "subtitleurlsha",
            "subtitle_url_length": 180,
            "parsed_webvtt": {
                "cue_count": 2,
                "transcript_char_count": 29,
                "transcript_text_sha256": "transcriptsha",
                "transcript_text": "This fragrance smells like tea",
                "cues": [
                    {"start": "00:00:00.000", "end": "00:00:01.000", "text": "This fragrance"},
                    {"start": "00:00:01.000", "end": "00:00:02.000", "text": "smells like tea"},
                ],
            },
        }
    else:
        base["hydration"] = {"subtitle_info_count": 0, "subtitle_infos_sanitized": []}
        base["subtitle"] = {"attempted": False, "success": False}
    return base


def test_normalize_stats_omits_absent_and_never_zero_fills() -> None:
    # absent stats are OMITTED, not synthesized as 0 (the no-zero-fill invariant):
    # the metric seed can only emit a loud gap if the key is genuinely absent.
    assert _normalize_stats({"playCount": 1000, "commentCount": 12}) == {
        "playCount": 1000,
        "commentCount": 12,
    }
    assert _normalize_stats({}) == {}
    # a digit-string exact count is coerced to int (the seed requires ints)
    assert _normalize_stats({"playCount": "10800", "diggCount": 5}) == {
        "playCount": 10800,
        "diggCount": 5,
    }
    # a present but non-exact value (rounded display string) is preserved RAW so
    # the seed's non-integer guard fails closed on it -- never coerced to a number
    # and never dropped to a silent gap.
    assert _normalize_stats({"playCount": 1000, "diggCount": "1.2M"}) == {
        "playCount": 1000,
        "diggCount": "1.2M",
    }
    # a null value is treated as absent -> omitted
    assert _normalize_stats({"playCount": 1000, "shareCount": None}) == {"playCount": 1000}


def _grid_payload_missing_digg() -> bytes:
    grid = json.loads(_grid_payload())
    del grid["response_items"][0]["stats"]["diggCount"]
    return json.dumps(grid).encode("utf-8")


def _cadence_payload_missing_digg() -> bytes:
    # drop the grid_candidate fallback stat too, so the writer cannot backfill
    cadence = json.loads(_cadence_payload())
    del cadence["results"][0]["grid_candidate"]["stats"]["diggCount"]
    return json.dumps(cadence).encode("utf-8")


def test_write_omits_a_missing_stat_end_to_end_no_zero_fill(tmp_path: Path) -> None:
    # End-to-end through the real writer (not a handcrafted payload): a source
    # grid item missing diggCount must produce a preserved video whose stats
    # OMITS diggCount, so the downstream metric seed emits a like_count gap
    # rather than a fabricated observed 0.
    output = tmp_path / "batch_packet"
    code, message = write_tiktok_batch_packet(
        creator_handle="@funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=_grid_payload_missing_digg(),
        cadence_result_jsons=[_cadence_payload_missing_digg()],
        output_directory=output,
        capture_timestamp="2026-06-30T17:02:46Z",
    )
    assert code == 0
    payload = json.loads((output / "raw" / "01_tiktok_batch_capture.json").read_text(encoding="utf-8"))
    first = next(v for v in payload["videos"] if v["video_id"] == VIDEO_1)
    assert "diggCount" not in first["stats"]  # absent -> omitted, NOT 0
    assert first["stats"]["playCount"] == 1000  # present stats still preserved
    assert first["stats"]["commentCount"] == 12
    # the second video keeps its complete stats
    second = next(v for v in payload["videos"] if v["video_id"] == VIDEO_2)
    assert second["stats"]["diggCount"] == 90
    # A partial aggregate would silently treat the missing value as zero, so the
    # incomplete metric is omitted while complete metrics remain available.
    assert "diggCount" not in payload["batch_summary"]["stats_sums"]
    assert payload["batch_summary"]["stats_sums"]["playCount"] == 3000


def test_write_tiktok_batch_packet_preserves_suggested_accounts_as_bronze(
    tmp_path: Path,
) -> None:
    output = tmp_path / "batch_packet"
    grid_window, selection = _onboarding_evidence_payloads()
    suggested = json.dumps(
        {
            "schema_version": "tiktok_creator_onboarding_v0",
            "creator_handle": "funmimonet",
            "status": "captured",
            "suggested_accounts": [
                {
                    "handle": "freshfrag",
                    "profile_url": "https://www.tiktok.com/@freshfrag",
                    "display_text_or_none": "Fresh Frag",
                }
            ],
            "profile_external_links": [],
        }
    ).encode("utf-8")

    code, _message = write_tiktok_batch_packet(
        creator_handle="@funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=_grid_payload(),
        cadence_result_jsons=[_cadence_payload()],
        grid_window_json=grid_window,
        selection_result_json=selection,
        suggested_accounts_json=suggested,
        output_directory=output,
        capture_timestamp="2026-06-30T17:02:46Z",
    )

    assert code == 0
    manifest = SourceCapturePacket(
        **json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    )
    assert [item.relative_packet_path for item in manifest.preserved_files] == [
        "raw/01_tiktok_batch_capture.json",
        "raw/02_tiktok_grid_window.json",
        "raw/03_tiktok_grid_video_selection.json",
        "raw/04_tiktok_suggested_accounts_attempt.json",
    ]
    assert json.loads(
        (output / "raw/04_tiktok_suggested_accounts_attempt.json").read_text(
            encoding="utf-8"
        )
    )["suggested_accounts"][0]["handle"] == "freshfrag"


def test_historical_recapture_is_written_as_a_separate_bronze_supplement(
    tmp_path: Path,
) -> None:
    output = tmp_path / "supplement_packet"
    prior = "bronze/tiktok/prior-packet"

    code, _message = write_tiktok_batch_packet(
        creator_handle="@funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=_grid_payload(),
        cadence_result_jsons=[_cadence_payload()],
        output_directory=output,
        capture_timestamp="2026-06-30T17:02:46Z",
        prior_capture_pointer=prior,
    )

    assert code == 0
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["re_capture_relationship"]["status"] == "known"
    assert manifest["re_capture_relationship"]["value"] == "supplement"
    payload = json.loads(
        (output / "raw" / "01_tiktok_batch_capture.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["historical_recapture"] == {
        "re_capture_relationship": "supplement",
        "prior_capture_pointer": prior,
        "prior_provenance_mutated": False,
    }


def _overlay_contract() -> dict[str, object]:
    return {
        **_contract(),
        "video_navigation_mode": "grid_tile_overlay_sequence",
        "grid_tile_overlay_navigation": True,
        "return_to_grid_between_videos": True,
        "direct_video_navigation": False,
        "item_struct_required": False,
    }


def test_write_tiktok_batch_packet_preserves_sanitized_batch_payload(tmp_path: Path) -> None:
    output = tmp_path / "batch_packet"

    code, message = write_tiktok_batch_packet(
        creator_handle="@funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=_grid_payload(),
        cadence_result_jsons=[_cadence_payload()],
        output_directory=output,
        decision_question="admit TikTok creator batch",
        batch_label="funmi_n2_fixture",
        source_file_receipts=[{"role": "grid", "file_name": "grid.json", "sha256": "gridsha", "size_bytes": 10, "source_path_sha256": "pathsha"}],
        capture_timestamp="2026-06-30T17:02:46Z",
    )

    assert code == 0
    assert Path(message) == output.resolve()
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    packet = SourceCapturePacket(**manifest)
    assert packet.source_family == "tiktok"
    assert packet.source_surface == "tiktok_creator_batch_comment_subtitle_admission"
    assert COMPLETE_LANE_NOTE in packet.visible_mode_changes
    assert [item.relative_packet_path for item in packet.preserved_files] == ["raw/01_tiktok_batch_capture.json"]

    payload_text = (output / "raw" / "01_tiktok_batch_capture.json").read_text(encoding="utf-8")
    payload = json.loads(payload_text)
    assert payload["batch_summary"]["video_count"] == 2
    assert payload["batch_summary"]["comment_response_success_count"] == 2
    assert payload["batch_summary"]["captured_comment_count"] == 2
    assert payload["batch_summary"]["comment_envelope_total_sum"] == 13
    assert payload["batch_summary"]["subtitle_success_count"] == 1
    assert payload["batch_summary"]["transcript_text_available_count"] == 1
    assert payload["batch_summary"]["source_text_disclosure_video_count"] == 2
    assert payload["batch_summary"]["stats_sums"]["playCount"] == 3000
    assert payload["source_file_receipts"][0]["path_redacted"] is True

    first = payload["videos"][0]
    assert first["source_text"]["mentions"] == ["Burberry Beauty"]
    assert first["source_text"]["hashtags"] == ["BurberryPartner", "fragrance"]
    assert first["comments"]["comments"][0]["cid"] == "cid-526"
    assert first["comments"]["envelope"] == {"cursor": "20", "has_more": True, "total": 10}
    assert first["subtitles"]["posture"] == "source_native_webvtt_captured"
    assert first["subtitles"]["cue_count"] == 2
    assert "smells like" in first["typed_extraction_seed"]["transcript_signal_terms"]
    assert "#burberrypartner" in first["typed_extraction_seed"]["disclosure_source_text_signals"]

    second = payload["videos"][1]
    assert second["subtitles"]["posture"] == "no_subtitleInfos_present"
    assert second["typed_extraction_seed"]["comment_question_count"] == 1
    assert second["typed_extraction_seed"]["comment_intent_term_counts"]["buy"] == 1
    assert "X-Bogus" not in payload_text
    assert "msToken" not in payload_text
    assert "tiktokcdn" not in payload_text


def test_write_tiktok_batch_packet_preserves_complete_onboarding_evidence(
    tmp_path: Path,
) -> None:
    output = tmp_path / "batch_packet"
    grid_window, selection = _onboarding_evidence_payloads()

    code, message = write_tiktok_batch_packet(
        creator_handle="funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=_grid_payload(),
        cadence_result_jsons=[_cadence_payload()],
        grid_window_json=grid_window,
        selection_result_json=selection,
        output_directory=output,
        capture_timestamp="2026-06-30T17:02:46Z",
    )

    assert code == 0
    assert Path(message) == output.resolve()
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    packet = SourceCapturePacket(**manifest)
    assert [item.relative_packet_path for item in packet.preserved_files] == [
        "raw/01_tiktok_batch_capture.json",
        "raw/02_tiktok_grid_window.json",
        "raw/03_tiktok_grid_video_selection.json",
    ]
    assert (output / "raw" / "02_tiktok_grid_window.json").read_bytes() == grid_window
    assert (
        output / "raw" / "03_tiktok_grid_video_selection.json"
    ).read_bytes() == selection
    payload = json.loads(
        (output / "raw" / "01_tiktok_batch_capture.json").read_text(
            encoding="utf-8"
        )
    )
    assert payload["capture_schema_version"] == "tiktok_batch_capture_admission_v2"
    assert payload["onboarding_evidence"] == {
        "grid_window_file": "tiktok_grid_window.json",
        "grid_window_sha256": hashlib.sha256(grid_window).hexdigest(),
        "grid_window_schema_version": "tiktok_creator_onboarding_v0",
        "grid_window_item_count": 3,
        "selection_file": "tiktok_grid_video_selection.json",
        "selection_sha256": hashlib.sha256(selection).hexdigest(),
        "selection_schema_version": "tiktok_grid_video_selection_v1",
        "selected_video_count": 2,
        "selection_grid_window_binding_verified": True,
        "selected_deep_capture_coverage_verified": True,
    }


def test_batch_admission_embeds_oldest_observation_without_new_raw_artifact(
    tmp_path: Path,
) -> None:
    grid_bytes, selection_bytes = _onboarding_evidence_payloads()
    grid = json.loads(grid_bytes)
    grid["schema_version"] = "tiktok_creator_onboarding_v1"
    grid["earliest_public_post_observation"] = {
        "status": "observed",
        "published_at_utc": "2021-04-03T12:34:56Z",
        "source_video_id": VIDEO_3,
        "source_video_url": f"{PROFILE_URL}/video/{VIDEO_3}",
        "observed_at_utc": "2026-07-21T10:00:00Z",
        "selection_method": "tiktok_profile_oldest_sort_first_batch_min_exact_create_time_v1",
        "timestamp_precision": "exact_source_create_time",
        "limitations": [
            "not_account_creation_time",
            "deleted_or_private_earlier_posts_not_observable",
        ],
    }
    grid_bytes = (json.dumps(grid, indent=2, sort_keys=True) + "\n").encode("utf-8")
    selection = json.loads(selection_bytes)
    selection["onboarding_binding"]["grid_window_sha256"] = hashlib.sha256(
        grid_bytes
    ).hexdigest()
    selection_bytes = (json.dumps(selection, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    output = tmp_path / "packet"

    write_tiktok_batch_packet(
        creator_handle="funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=_grid_payload(),
        cadence_result_jsons=[_cadence_payload()],
        grid_window_json=grid_bytes,
        selection_result_json=selection_bytes,
        output_directory=output,
        capture_timestamp="2026-06-30T17:02:46Z",
    )

    manifest = SourceCapturePacket(
        **json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    )
    assert [item.relative_packet_path for item in manifest.preserved_files] == [
        "raw/01_tiktok_batch_capture.json",
        "raw/02_tiktok_grid_window.json",
        "raw/03_tiktok_grid_video_selection.json",
    ]
    payload = json.loads(
        (output / "raw" / "01_tiktok_batch_capture.json").read_text(encoding="utf-8")
    )
    assert payload["earliest_public_post_observation"] == (
        grid["earliest_public_post_observation"]
    )


def test_write_tiktok_batch_packet_requires_onboarding_evidence_pair(
    tmp_path: Path,
) -> None:
    output = tmp_path / "batch_packet"
    grid_window, _selection = _onboarding_evidence_payloads()

    with pytest.raises(
        ValueError,
        match="grid_window_json and selection_result_json must be supplied together",
    ):
        write_tiktok_batch_packet(
            creator_handle="funmimonet",
            creator_profile_url=PROFILE_URL,
            grid_result_json=_grid_payload(),
            cadence_result_jsons=[_cadence_payload()],
            grid_window_json=grid_window,
            output_directory=output,
        )

    assert not output.exists()


def test_write_tiktok_batch_packet_rejects_stale_grid_selection_binding(
    tmp_path: Path,
) -> None:
    output = tmp_path / "batch_packet"
    grid_window, selection = _onboarding_evidence_payloads()
    selection_payload = json.loads(selection)
    selection_payload["onboarding_binding"]["grid_window_sha256"] = "0" * 64

    with pytest.raises(ValueError, match="grid_window_sha256 does not match"):
        write_tiktok_batch_packet(
            creator_handle="funmimonet",
            creator_profile_url=PROFILE_URL,
            grid_result_json=_grid_payload(),
            cadence_result_jsons=[_cadence_payload()],
            grid_window_json=grid_window,
            selection_result_json=json.dumps(selection_payload).encode("utf-8"),
            output_directory=output,
        )

    assert not output.exists()


def test_write_tiktok_batch_packet_rejects_selection_not_matching_deep_captures(
    tmp_path: Path,
) -> None:
    output = tmp_path / "batch_packet"
    grid_window, selection = _onboarding_evidence_payloads()
    selection_payload = json.loads(selection)
    selection_payload["ranked_items"][0]["selected"] = False
    selection_payload["selection_summary"] = {
        "selection_count": 1,
        "selected_video_ids_in_review_priority_order": [VIDEO_1],
    }

    with pytest.raises(ValueError, match="selected ids do not match admitted cadence"):
        write_tiktok_batch_packet(
            creator_handle="funmimonet",
            creator_profile_url=PROFILE_URL,
            grid_result_json=_grid_payload(),
            cadence_result_jsons=[_cadence_payload()],
            grid_window_json=grid_window,
            selection_result_json=json.dumps(selection_payload).encode("utf-8"),
            output_directory=output,
        )

    assert not output.exists()


def test_write_tiktok_batch_packet_accepts_scraped_video_url_variants(
    tmp_path: Path,
) -> None:
    output = tmp_path / "batch_packet"
    grid_bytes, selection_bytes = _onboarding_evidence_payloads()
    grid_payload = json.loads(grid_bytes)
    grid_payload["items"][0]["video_url"] = (
        f"http://m.tiktok.com/@funmimonet/video/{VIDEO_1}/"
    )
    grid_bytes = (json.dumps(grid_payload, indent=2, sort_keys=True) + "\n").encode(
        "utf-8"
    )
    selection_payload = json.loads(selection_bytes)
    selection_payload["onboarding_binding"]["grid_window_sha256"] = hashlib.sha256(
        grid_bytes
    ).hexdigest()
    selection_bytes = (
        json.dumps(selection_payload, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")

    code, message = write_tiktok_batch_packet(
        creator_handle="funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=_grid_payload(),
        cadence_result_jsons=[_cadence_payload()],
        grid_window_json=grid_bytes,
        selection_result_json=selection_bytes,
        output_directory=output,
        capture_timestamp="2026-06-30T17:02:46Z",
    )

    assert code == 0
    assert Path(message) == output.resolve()


def test_write_tiktok_batch_packet_rejects_grid_video_url_for_wrong_creator(
    tmp_path: Path,
) -> None:
    output = tmp_path / "batch_packet"
    grid_window, selection = _onboarding_evidence_payloads()
    grid_payload = json.loads(grid_window)
    grid_payload["items"][0]["video_url"] = f"https://www.tiktok.com/@someoneelse/video/{VIDEO_1}"
    grid_window = (json.dumps(grid_payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    selection_payload = json.loads(selection)
    selection_payload["onboarding_binding"]["grid_window_sha256"] = hashlib.sha256(
        grid_window
    ).hexdigest()
    selection = (json.dumps(selection_payload, indent=2, sort_keys=True) + "\n").encode("utf-8")

    with pytest.raises(ValueError, match="video_url does not match creator/video_id"):
        write_tiktok_batch_packet(
            creator_handle="funmimonet",
            creator_profile_url=PROFILE_URL,
            grid_result_json=_grid_payload(),
            cadence_result_jsons=[_cadence_payload()],
            grid_window_json=grid_window,
            selection_result_json=selection,
            output_directory=output,
        )

    assert not output.exists()


def test_write_tiktok_batch_packet_preserves_dom_visible_comment_fallback(tmp_path: Path) -> None:
    output = tmp_path / "batch_packet"
    row = _result_row(VIDEO_1, 1761930827, subtitle=False)
    row["comment_responses"] = []
    row["dom_visible_comment_candidates"] = [
        {
            "source_order": 0,
            "text": "What perfume is this?",
            "text_sha256": "domtextsha",
            "text_char_count": 21,
            "capture_posture": "visible_dom_after_comment_route",
        }
    ]
    cadence = json.dumps(
        {
            "attempted_count": 1,
            "completed_count": 1,
            "challenge_count": 0,
            "run_complete_utc": "2026-06-30T17:02:46Z",
            "capture_contract": _contract(),
            "results": [row],
        }
    ).encode("utf-8")

    code, message = write_tiktok_batch_packet(
        creator_handle="@funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=_grid_payload(),
        cadence_result_jsons=[cadence],
        output_directory=output,
        decision_question="admit TikTok DOM-visible comments",
        batch_label="funmi_dom_fixture",
        capture_timestamp="2026-06-30T17:02:46Z",
    )

    assert code == 0
    assert Path(message) == output.resolve()
    payload = json.loads((output / "raw" / "01_tiktok_batch_capture.json").read_text(encoding="utf-8"))
    assert payload["batch_summary"]["comment_response_success_count"] == 0
    assert payload["batch_summary"]["dom_visible_comment_video_count"] == 1
    assert payload["batch_summary"]["captured_comment_count"] == 1
    comments = payload["videos"][0]["comments"]
    assert comments["posture"] == "captured_visible_dom"
    assert comments["comments"][0]["text"] == "What perfume is this?"
    assert comments["limitations"] == [
        "dom_visible_comment_candidates_no_api_envelope",
        "dom_visible_comment_candidates_no_reply_expansion",
    ]


def test_write_tiktok_batch_packet_preserves_subtitle_non_capture_reason(tmp_path: Path) -> None:
    output = tmp_path / "batch_packet"
    row = _result_row(VIDEO_1, 1761930827, subtitle=False)
    row["hydration"] = {
        "subtitle_info_count": 1,
        "subtitle_infos_sanitized": [
            {
                "Format": "webvtt",
                "LanguageCodeName": "eng-US",
                "Source": "ASR",
                "Size": 99,
                "url_present_but_redacted": True,
            }
        ],
    }
    row["subtitle"] = {
        "attempted": False,
        "success": False,
        "reason": "unsupported_subtitle_url_host_live_probe_v0",
        "subtitle_url_sha256": "subtitleurlsha",
        "subtitle_url_length": 180,
    }
    cadence = json.dumps(
        {
            "attempted_count": 1,
            "completed_count": 1,
            "challenge_count": 0,
            "run_complete_utc": "2026-06-30T17:02:46Z",
            "capture_contract": _contract(),
            "results": [row],
        }
    ).encode("utf-8")

    code, message = write_tiktok_batch_packet(
        creator_handle="@funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=_grid_payload(),
        cadence_result_jsons=[cadence],
        output_directory=output,
        decision_question="admit TikTok subtitle non-capture reason",
        batch_label="funmi_subtitle_reason_fixture",
        capture_timestamp="2026-06-30T17:02:46Z",
    )

    assert code == 0
    payload_text = (Path(message) / "raw" / "01_tiktok_batch_capture.json").read_text(
        encoding="utf-8"
    )
    payload = json.loads(payload_text)
    subtitles = payload["videos"][0]["subtitles"]
    assert subtitles["posture"] == "source_native_subtitle_not_captured"
    assert subtitles["non_capture_reason"] == "unsupported_subtitle_url_host_live_probe_v0"
    assert subtitles["subtitle_url_sha256"] == "subtitleurlsha"
    assert subtitles["subtitle_url_length"] == 180
    assert "tiktokcdn" not in payload_text
    assert "subtitle.webvtt" not in payload_text


def test_write_tiktok_batch_packet_labels_human_handoff_as_intervention(tmp_path: Path) -> None:
    output = tmp_path / "batch_packet"
    row = _result_row(VIDEO_1, 1761930827, subtitle=False)
    row["capture_receipt"] = {
        "challenge_close_followthrough": True,
        "challenge_close_accepted": True,
        "challenge_close_action": {
            "action_name": "tiktok_challenge_modal_close_followthrough_pointer_v0",
            "clicked": True,
            "target_kind": "visual_x",
            "selection_strategy": "center_modal_visual_x",
            "post_click_absence_verified": True,
            "post_click_visual_target_absent": True,
        },
        "human_challenge_handoff": True,
        "human_challenge_handoff_attempts": [
            {
                "action_name": "human_challenge_handoff_v0",
                "action_mode": "source_access_intervention",
                "action_taken": True,
                "captcha_solving_by_agent": False,
                "prompted": True,
                "prompt_surface": "test_prompt",
                "matched_marker": "drag the slider",
                "marker_count": 1,
                "timeout_seconds": 1,
                "cleared": True,
                "wait_ms": 0,
                "after_action_name": "tiktok_challenge_modal_close_followthrough_pointer_v0",
            }
        ],
    }
    cadence = json.dumps(
        {
            "attempted_count": 1,
            "completed_count": 1,
            "challenge_count": 0,
            "run_complete_utc": "2026-06-30T17:02:46Z",
            "capture_contract": _contract(),
            "results": [row],
        }
    ).encode("utf-8")

    code, message = write_tiktok_batch_packet(
        creator_handle="@funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=_grid_payload(),
        cadence_result_jsons=[cadence],
        output_directory=output,
        decision_question="admit TikTok human handoff intervention",
        batch_label="funmi_human_handoff_fixture",
        capture_timestamp="2026-06-30T17:02:46Z",
    )

    assert code == 0
    payload = json.loads(
        (Path(message) / "raw" / "01_tiktok_batch_capture.json").read_text(
            encoding="utf-8"
        )
    )
    intervention = payload["videos"][0]["source_access_intervention"]
    assert intervention["posture"] == (
        "owner_manual_challenge_handoff_after_challenge_close_followthrough"
    )
    assert intervention["human_challenge_handoff"] is True
    assert intervention["human_challenge_handoff_attempt_count"] == 1
    assert intervention["human_challenge_handoff_cleared"] is True
    assert intervention["human_challenge_handoff_prompt_surfaces"] == ["test_prompt"]
    assert intervention["human_challenge_handoff_matched_markers"] == ["drag the slider"]
    assert intervention["agent_may_solve_challenge"] is False
    assert intervention["counts_as_clean_capture"] is False


def test_tiktok_batch_rejects_agent_challenge_solving_receipt(tmp_path: Path) -> None:
    output = tmp_path / "packet"
    cadence = json.loads(_cadence_payload().decode("utf-8"))
    cadence["results"][0]["capture_receipt"] = {"agent_may_solve_challenge": True}

    with pytest.raises(ValueError, match="permits agent challenge solving"):
        write_tiktok_batch_packet(
            creator_handle="funmimonet",
            creator_profile_url=PROFILE_URL,
            grid_result_json=_grid_payload(),
            cadence_result_jsons=[json.dumps(cadence).encode("utf-8")],
            output_directory=output,
            decision_question="reject agent challenge solving",
        )


def test_tiktok_batch_rejects_owner_attention_clean_capture_claim(tmp_path: Path) -> None:
    output = tmp_path / "packet"
    cadence = json.loads(_cadence_payload().decode("utf-8"))
    cadence["results"][0]["capture_receipt"] = {
        "owner_attention_required": True,
        "manual_challenge_attention_required": True,
        "owner_attention_counts_as_clean_capture": True,
    }

    with pytest.raises(ValueError, match="counts owner attention as clean capture"):
        write_tiktok_batch_packet(
            creator_handle="funmimonet",
            creator_profile_url=PROFILE_URL,
            grid_result_json=_grid_payload(),
            cadence_result_jsons=[json.dumps(cadence).encode("utf-8")],
            output_directory=output,
            decision_question="reject owner attention clean claim",
        )

def test_tiktok_batch_runner_can_commit_to_data_lake(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    grid_path = tmp_path / "grid.json"
    cadence_path = tmp_path / "cadence.json"
    grid_path.write_bytes(_grid_payload())
    cadence_path.write_bytes(_cadence_payload())

    code, message = run_source_capture_tiktok_batch_packet(
        creator_handle="funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json_path=grid_path,
        cadence_result_json_paths=[cadence_path],
        data_root=root,
        decision_question="admit TikTok creator batch",
        batch_label="funmi_fixture",
    )

    assert code == 0
    packet_dir = Path(message)
    assert packet_dir.parent == root.path / "raw" / raw_shard(packet_dir.name)
    assert root.find_packet(packet_dir.name) is not None
    assert root.read_availability(packet_dir.name) is not None
    payload = json.loads((packet_dir / "raw" / "01_tiktok_batch_capture.json").read_text(encoding="utf-8"))
    assert payload["source_file_receipts"][0]["file_name"] == "grid.json"
    assert payload["source_file_receipts"][0]["source_path_sha256"]


def test_tiktok_batch_runner_can_re_admit_complete_onboarding_staging(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    grid_path = tmp_path / "grid.json"
    cadence_path = tmp_path / "cadence.json"
    grid_window_path = tmp_path / "tiktok_grid_window.json"
    selection_path = tmp_path / "tiktok_grid_video_selection.json"
    grid_window, selection = _onboarding_evidence_payloads()
    grid_path.write_bytes(_grid_payload())
    cadence_path.write_bytes(_cadence_payload())
    grid_window_path.write_bytes(grid_window)
    selection_path.write_bytes(selection)

    code, message = run_source_capture_tiktok_batch_packet(
        creator_handle="funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json_path=grid_path,
        cadence_result_json_paths=[cadence_path],
        grid_window_json_path=grid_window_path,
        selection_result_json_path=selection_path,
        data_root=root,
        decision_question="admit complete TikTok onboarding evidence",
    )

    assert code == 0
    packet_dir = Path(message)
    manifest = json.loads((packet_dir / "manifest.json").read_text(encoding="utf-8"))
    assert [row["relative_packet_path"] for row in manifest["preserved_files"]] == [
        "raw/01_tiktok_batch_capture.json",
        "raw/02_tiktok_grid_window.json",
        "raw/03_tiktok_grid_video_selection.json",
    ]
    payload = json.loads(
        (packet_dir / "raw" / "01_tiktok_batch_capture.json").read_text(
            encoding="utf-8"
        )
    )
    assert [row["role"] for row in payload["source_file_receipts"]][-2:] == [
        "grid_window_json",
        "selection_result_json",
    ]


def test_tiktok_batch_cli_prints_complete_lane_note(tmp_path: Path, capsys) -> None:
    output = tmp_path / "packet"
    grid_path = tmp_path / "grid.json"
    cadence_path = tmp_path / "cadence.json"
    grid_path.write_bytes(_grid_payload())
    cadence_path.write_bytes(_cadence_payload())

    code = tiktok_batch_main(
        [
            "--creator-handle",
            "funmimonet",
            "--creator-profile-url",
            PROFILE_URL,
            "--grid-result-json",
            str(grid_path),
            "--cadence-result-json",
            str(cadence_path),
            "--output",
            str(output),
        ]
    )

    captured = capsys.readouterr()
    assert code == 0
    assert COMPLETE_LANE_NOTE in captured.out
    assert str(output.resolve()) in captured.out


def test_tiktok_batch_rejects_forbidden_staging_contract(tmp_path: Path) -> None:
    output = tmp_path / "packet"
    grid = json.loads(_grid_payload().decode("utf-8"))
    grid["capture_contract"]["direct_forged_api_calls"] = True

    with pytest.raises(ValueError, match="direct_forged_api_calls=true"):
        write_tiktok_batch_packet(
            creator_handle="funmimonet",
            creator_profile_url=PROFILE_URL,
            grid_result_json=json.dumps(grid).encode("utf-8"),
            cadence_result_jsons=[_cadence_payload()],
            output_directory=output,
            decision_question="admit TikTok creator batch",
        )


def test_tiktok_batch_accepts_grid_overlay_contract_without_item_struct_requirement(
    tmp_path: Path,
) -> None:
    grid = json.loads(_grid_payload().decode("utf-8"))
    cadence = json.loads(_cadence_payload().decode("utf-8"))
    grid["capture_contract"] = _overlay_contract()
    cadence["capture_contract"] = _overlay_contract()

    code, _message = write_tiktok_batch_packet(
        creator_handle="funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=json.dumps(grid).encode("utf-8"),
        cadence_result_jsons=[json.dumps(cadence).encode("utf-8")],
        output_directory=tmp_path / "overlay_packet",
    )

    assert code == 0


def test_tiktok_batch_rejects_overlay_contract_with_direct_navigation(
    tmp_path: Path,
) -> None:
    grid = json.loads(_grid_payload().decode("utf-8"))
    grid["capture_contract"] = {
        **_overlay_contract(),
        "direct_video_navigation": True,
    }

    with pytest.raises(ValueError, match="direct_video_navigation=false"):
        write_tiktok_batch_packet(
            creator_handle="funmimonet",
            creator_profile_url=PROFILE_URL,
            grid_result_json=json.dumps(grid).encode("utf-8"),
            cadence_result_jsons=[_cadence_payload()],
            output_directory=tmp_path / "invalid_overlay_packet",
        )


def test_tiktok_batch_rejects_challenge_cadence_for_admission(tmp_path: Path) -> None:
    output = tmp_path / "packet"
    cadence = json.loads(_cadence_payload().decode("utf-8"))
    cadence["challenge_count"] = 1

    with pytest.raises(ValueError, match="challenge_count=1 cannot be admitted"):
        write_tiktok_batch_packet(
            creator_handle="funmimonet",
            creator_profile_url=PROFILE_URL,
            grid_result_json=_grid_payload(),
            cadence_result_jsons=[json.dumps(cadence).encode("utf-8")],
            output_directory=output,
            decision_question="admit TikTok creator batch",
        )


def test_tiktok_batch_rejects_failed_cadence_for_admission(tmp_path: Path) -> None:
    output = tmp_path / "packet"
    cadence = json.loads(_cadence_payload().decode("utf-8"))
    cadence["failures"] = [{"reason": "challenge_close_diagnostic_only"}]

    with pytest.raises(ValueError, match="contains 1 failure entries"):
        write_tiktok_batch_packet(
            creator_handle="funmimonet",
            creator_profile_url=PROFILE_URL,
            grid_result_json=_grid_payload(),
            cadence_result_jsons=[json.dumps(cadence).encode("utf-8")],
            output_directory=output,
            decision_question="admit TikTok creator batch",
        )


def test_tiktok_batch_admits_failure_superseded_by_later_completed_receipt(
    tmp_path: Path,
) -> None:
    output = tmp_path / "packet"
    failed = json.loads(_cadence_payload().decode("utf-8"))
    failed["attempted_count"] = 2
    failed["completed_count"] = 1
    failed["run_complete_utc"] = "2026-06-30T17:02:46Z"
    failed["results"] = [failed["results"][0]]
    failed["failures"] = [
        {
            "video_id": VIDEO_2,
            "reason": "comment_list_response_absent",
            "observed_utc": "2026-06-30T17:02:30Z",
        }
    ]

    recovered = json.loads(_cadence_payload().decode("utf-8"))
    recovered["attempted_count"] = 1
    recovered["completed_count"] = 1
    recovered["run_complete_utc"] = "2026-06-30T17:05:00Z"
    recovered["results"] = [recovered["results"][1]]

    code, _message = write_tiktok_batch_packet(
        creator_handle="funmimonet",
        creator_profile_url=PROFILE_URL,
        grid_result_json=_grid_payload(),
        cadence_result_jsons=[
            json.dumps(failed).encode("utf-8"),
            json.dumps(recovered).encode("utf-8"),
        ],
        output_directory=output,
        decision_question="admit a later-completed recovery without hiding the earlier failure",
    )

    assert code == 0
    payload = json.loads(
        (output / "raw" / "01_tiktok_batch_capture.json").read_text(encoding="utf-8")
    )
    assert [video["video_id"] for video in payload["videos"]] == [VIDEO_1, VIDEO_2]
    assert payload["staging_contract_summary"]["superseded_failures"] == [
        {
            "video_id": VIDEO_2,
            "failure_reason": "comment_list_response_absent",
            "failure_observed_utc": "2026-06-30T17:02:30Z",
            "failed_run_complete_utc": "2026-06-30T17:02:46Z",
            "superseding_run_complete_utc": "2026-06-30T17:05:00Z",
            "superseding_result_status": "completed",
        }
    ]


def test_tiktok_batch_rejects_failure_when_completion_is_not_later(tmp_path: Path) -> None:
    output = tmp_path / "packet"
    failed = json.loads(_cadence_payload().decode("utf-8"))
    failed["attempted_count"] = 1
    failed["completed_count"] = 0
    failed["run_complete_utc"] = "2026-06-30T17:05:00Z"
    failed["results"] = []
    failed["failures"] = [{"video_id": VIDEO_1, "reason": "comment_list_response_absent"}]

    older_completion = json.loads(_cadence_payload().decode("utf-8"))
    older_completion["attempted_count"] = 1
    older_completion["completed_count"] = 1
    older_completion["run_complete_utc"] = "2026-06-30T17:02:46Z"
    older_completion["results"] = [older_completion["results"][0]]

    with pytest.raises(ValueError, match="1 unsuperseded"):
        write_tiktok_batch_packet(
            creator_handle="funmimonet",
            creator_profile_url=PROFILE_URL,
            grid_result_json=_grid_payload(),
            cadence_result_jsons=[
                json.dumps(failed).encode("utf-8"),
                json.dumps(older_completion).encode("utf-8"),
            ],
            output_directory=output,
            decision_question="reject a failure without a strictly later completion",
        )


def test_tiktok_batch_rejects_diagnostic_mode_contract(tmp_path: Path) -> None:
    output = tmp_path / "packet"
    cadence = json.loads(_cadence_payload().decode("utf-8"))
    cadence["capture_contract"]["challenge_close_diagnostic_allowed"] = True

    with pytest.raises(ValueError, match="challenge_close_diagnostic_allowed=true"):
        write_tiktok_batch_packet(
            creator_handle="funmimonet",
            creator_profile_url=PROFILE_URL,
            grid_result_json=_grid_payload(),
            cadence_result_jsons=[json.dumps(cadence).encode("utf-8")],
            output_directory=output,
            decision_question="admit TikTok creator batch",
        )


def test_tiktok_batch_rejects_human_handoff_clean_capture_contract(tmp_path: Path) -> None:
    output = tmp_path / "packet"
    cadence = json.loads(_cadence_payload().decode("utf-8"))
    cadence["capture_contract"]["human_challenge_handoff_counts_as_clean_capture"] = True

    with pytest.raises(
        ValueError,
        match="human_challenge_handoff_counts_as_clean_capture=true",
    ):
        write_tiktok_batch_packet(
            creator_handle="funmimonet",
            creator_profile_url=PROFILE_URL,
            grid_result_json=_grid_payload(),
            cadence_result_jsons=[json.dumps(cadence).encode("utf-8")],
            output_directory=output,
            decision_question="reject human handoff clean capture contract",
        )

def test_tiktok_batch_rejects_mismatched_completed_count(tmp_path: Path) -> None:
    output = tmp_path / "packet"
    cadence = json.loads(_cadence_payload().decode("utf-8"))
    cadence["completed_count"] = 30

    with pytest.raises(ValueError, match="completed_count=30 does not match normalized video_count=2"):
        write_tiktok_batch_packet(
            creator_handle="funmimonet",
            creator_profile_url=PROFILE_URL,
            grid_result_json=_grid_payload(),
            cadence_result_jsons=[json.dumps(cadence).encode("utf-8")],
            output_directory=output,
            decision_question="admit TikTok creator batch",
        )


def test_tiktok_batch_runner_has_no_hidden_network_browser_or_proxy_imports() -> None:
    runner_path = Path(__file__).resolve().parents[2] / "runners" / "run_source_capture_tiktok_batch_packet.py"
    tree = ast.parse(runner_path.read_text(encoding="utf-8"))
    imported_modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.add(node.module)

    forbidden = {
        "aiohttp",
        "browser_cookie3",
        "httpx",
        "patchright",
        "playwright",
        "requests",
        "scrapy",
        "selenium",
        "socket",
        "source_capture.proxy_profiles",
        "webbrowser",
    }
    bad_imports = sorted(
        module
        for module in imported_modules
        for forbidden_module in forbidden
        if module == forbidden_module or module.startswith(f"{forbidden_module}.")
    )
    assert bad_imports == []
