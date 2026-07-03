from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, raw_shard
from runners.run_source_capture_tiktok_batch_packet import main as tiktok_batch_main, run_source_capture_tiktok_batch_packet
from source_capture.models import SourceCapturePacket
from source_capture.tiktok import COMPLETE_LANE_NOTE
from source_capture.tiktok.batch_packet import write_tiktok_batch_packet

VIDEO_1 = "7629774409762442526"
VIDEO_2 = "7629774409762442527"
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


def test_tiktok_batch_runner_can_commit_to_data_lake(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
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
