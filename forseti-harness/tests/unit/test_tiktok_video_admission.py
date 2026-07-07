from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, raw_shard
from runners.run_source_capture_tiktok_video_packet import main as tiktok_video_main, run_source_capture_tiktok_video_packet
from source_capture.models import SourceCapturePacket
from source_capture.tiktok import (
    COMPLETE_LANE_NOTE,
    assert_no_sensitive_tiktok_material,
    decoded_aweme_id_create_time_utc,
    extract_subtitle_infos,
    parse_comment_list_bytes,
    parse_profile_list_items,
    parse_webvtt_cues,
)
from source_capture.tiktok.video_packet import write_tiktok_video_packet

VIDEO_ID = "7629774409762442526"
VIDEO_URL = f"https://www.tiktok.com/@funmimonet/video/{VIDEO_ID}"


def _profile_payload() -> bytes:
    return json.dumps(
        {
            "itemList": [
                {
                    "id": VIDEO_ID,
                    "desc": "Burberry Goddess. #BurberryPartner #fragrance",
                    "createTime": 1761930827,
                    "stats": {
                        "playCount": 1000,
                        "diggCount": 45,
                        "commentCount": 12,
                        "shareCount": 3,
                        "collectCount": 7,
                    },
                    "textExtra": [{"hashtagName": "BurberryPartner"}, {"hashtagName": "fragrance"}],
                    "challenges": [{"title": "burberrypartner"}],
                    "music": {"title": "original sound", "authorName": "Funmi Monet"},
                    "isAd": True,
                    "adLabelVersion": 2,
                    "adAuthorization": {"x": 1},
                    "BAInfo": {"x": 1},
                }
            ]
        }
    ).encode("utf-8")


def _comment_payload() -> bytes:
    return json.dumps(
        {
            "cursor": 20,
            "has_more": 1,
            "total": 304,
            "comments": [
                {
                    "cid": "735",
                    "text": "I need to smell this",
                    "create_time": 1761930900,
                    "digg_count": 9,
                    "reply_comment_total": 1,
                    "user": {"uid": "42", "unique_id": "viewer", "nickname": "Viewer"},
                }
            ],
        }
    ).encode("utf-8")


def _video_item_payload() -> bytes:
    return json.dumps(
        {
            "itemInfo": {
                "itemStruct": {
                    "id": VIDEO_ID,
                    "video": {
                        "subtitleInfos": [
                            {
                                "Format": "webvtt",
                                "LanguageCodeName": "eng-US",
                                "LanguageID": 2,
                                "Source": "ASR",
                                "Size": 1106,
                                "Version": "1:whisper_lid",
                                "Url": "https://v16-webapp-prime.tiktokcdn-us.com/subtitle.vtt?X-Bogus=secret",
                            }
                        ]
                    },
                }
            }
        }
    ).encode("utf-8")


def _webvtt() -> bytes:
    return b"""WEBVTT

00:00:00.000 --> 00:00:01.200
First cue

00:00:01.200 --> 00:00:02.500
Second cue
"""


def test_profile_list_parser_extracts_stats_ad_and_dates() -> None:
    payload = json.loads(_profile_payload().decode("utf-8"))

    [item] = parse_profile_list_items(payload, source_surface="/api/post/item_list/")

    assert item.video_id == VIDEO_ID
    assert item.create_time_utc == "2025-10-31T17:13:47Z"
    assert item.decoded_aweme_id_create_time_utc == decoded_aweme_id_create_time_utc(VIDEO_ID)
    assert item.play_count == 1000
    assert item.digg_count == 45
    assert item.comment_count == 12
    assert item.share_count == 3
    assert item.collect_count == 7
    assert item.hashtags == ("BurberryPartner", "fragrance")
    assert item.challenge_titles == ("burberrypartner",)
    assert item.is_ad is True
    assert item.ad_label_version == 2
    assert item.ad_authorization_present is True
    assert item.ba_info_present is True


def test_comment_list_parser_requires_packet_grade_fields() -> None:
    admission = parse_comment_list_bytes(_comment_payload())

    assert admission.body_size_bytes == len(_comment_payload())
    assert admission.cursor == 20
    assert admission.has_more == 1
    assert admission.total == 304
    assert admission.comment_count == 1
    assert admission.comments[0].cid == "735"
    assert admission.comments[0].user_uid == "42"


def test_comment_list_parser_rejects_missing_uid() -> None:
    payload = json.loads(_comment_payload().decode("utf-8"))
    del payload["comments"][0]["user"]["uid"]

    with pytest.raises(ValueError, match="missing user.uid"):
        parse_comment_list_bytes(json.dumps(payload).encode("utf-8"))


def test_subtitle_infos_are_sanitized_to_url_hash_only_and_webvtt_parses() -> None:
    [info] = extract_subtitle_infos(json.loads(_video_item_payload().decode("utf-8")))
    cues = parse_webvtt_cues(_webvtt())

    assert info.format == "webvtt"
    assert info.language_code_name == "eng-US"
    assert info.source == "ASR"
    assert info.url_present is True
    assert info.url_sha256
    assert "Url" not in info.to_dict()
    assert [(cue.start_ms, cue.end_ms, cue.text) for cue in cues] == [
        (0, 1200, "First cue"),
        (1200, 2500, "Second cue"),
    ]


def test_sanitizer_rejects_raw_signed_or_session_material() -> None:
    with pytest.raises(ValueError, match="unsafe TikTok material"):
        assert_no_sensitive_tiktok_material(
            {"Url": "https://www.tiktok.com/api/comment/list?msToken=secret&X-Bogus=signed"}
        )
    with pytest.raises(ValueError, match="unsafe TikTok material"):
        assert_no_sensitive_tiktok_material({"Cookie": "ttwid=secret"})
    with pytest.raises(ValueError, match="unsafe TikTok material"):
        assert_no_sensitive_tiktok_material(
            {"hashtags": ("https://www.tiktok.com/api/comment/list?msToken=secret",)}
        )
    with pytest.raises(ValueError, match="unsafe TikTok material"):
        assert_no_sensitive_tiktok_material({"comment": "https://www.tiktok.com/@foo/video/123?lang=en"})
    with pytest.raises(ValueError, match="unsafe TikTok material"):
        assert_no_sensitive_tiktok_material({"subtitle": "https://v16-webapp-prime.tiktokcdn-us.com/subtitle.vtt"})
    with pytest.raises(ValueError, match="unsafe TikTok material"):
        assert_no_sensitive_tiktok_material(
            {"subtitle_url_sha256": "https://v9-default.byteoversea.com/tos-useast5-ve-0068c001-tx/subtitle.webvtt"}
        )


def test_write_tiktok_video_packet_preserves_sanitized_payload_only(tmp_path: Path) -> None:
    output = tmp_path / "tiktok_packet"

    code, message = write_tiktok_video_packet(
        video_id=VIDEO_ID,
        video_url=VIDEO_URL,
        comment_list_json=_comment_payload(),
        video_item_json=_video_item_payload(),
        profile_list_json=_profile_payload(),
        subtitle_webvtt=_webvtt(),
        output_directory=output,
        decision_question="admit TikTok behavioral packet",
        now_iso="2026-06-30T17:00:00Z",
    )

    assert code == 0
    assert Path(message) == output.resolve()
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    packet = SourceCapturePacket(**manifest)
    assert packet.source_family == "tiktok"
    assert packet.source_surface == "tiktok_video_comment_subtitle_admission"
    assert COMPLETE_LANE_NOTE in packet.visible_mode_changes
    assert [item.relative_packet_path for item in packet.preserved_files] == ["raw/01_tiktok_video_capture.json"]

    payload = json.loads((output / "raw" / "01_tiktok_video_capture.json").read_text(encoding="utf-8"))
    assert payload["complete_lane_note"] == COMPLETE_LANE_NOTE
    assert payload["comments"]["body_sha256"]
    assert payload["comments"]["comments"][0]["text"] == "I need to smell this"
    assert payload["subtitle_infos"][0]["url_sha256"]
    assert "Url" not in json.dumps(payload)
    assert "X-Bogus" not in json.dumps(payload)
    assert payload["subtitles"]["cue_count"] == 2


def test_write_tiktok_video_packet_rejects_identity_url_and_empty_artifacts(tmp_path: Path) -> None:
    output = tmp_path / "tiktok_packet"

    bad_id_code, bad_id_message = write_tiktok_video_packet(
        video_id="not-a-video-id",
        video_url=VIDEO_URL,
        comment_list_json=_comment_payload(),
        output_directory=output,
        decision_question="admit TikTok behavioral packet",
    )
    assert bad_id_code == 5
    assert "invalid TikTok video id" in bad_id_message

    bad_url_code, bad_url_message = write_tiktok_video_packet(
        video_id=VIDEO_ID,
        video_url=f"{VIDEO_URL}?lang=en",
        comment_list_json=_comment_payload(),
        output_directory=output,
        decision_question="admit TikTok behavioral packet",
    )
    assert bad_url_code == 5
    assert "without query" in bad_url_message

    empty_code, empty_message = write_tiktok_video_packet(
        video_id=VIDEO_ID,
        video_url=VIDEO_URL,
        output_directory=output,
        decision_question="admit TikTok behavioral packet",
    )
    assert empty_code == 5
    assert "at least one TikTok artifact" in empty_message


def test_webvtt_parser_rejects_empty_headerless_and_no_cue_bodies() -> None:
    for body, expected in [
        (b"", "empty WebVTT body"),
        (b"00:00:00.000 --> 00:00:01.000\nNo header", "missing WEBVTT header"),
        (b"WEBVTT\n\nNOTE no cues here\n", "no parseable cues"),
    ]:
        with pytest.raises(ValueError, match=expected):
            parse_webvtt_cues(body)


def test_tiktok_video_runner_can_commit_to_data_lake(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    comment_path = tmp_path / "comments.json"
    item_path = tmp_path / "item.json"
    profile_path = tmp_path / "profile.json"
    webvtt_path = tmp_path / "subtitle.vtt"
    comment_path.write_bytes(_comment_payload())
    item_path.write_bytes(_video_item_payload())
    profile_path.write_bytes(_profile_payload())
    webvtt_path.write_bytes(_webvtt())

    code, message = run_source_capture_tiktok_video_packet(
        video_id=VIDEO_ID,
        video_url=VIDEO_URL,
        data_root=root,
        decision_question="admit TikTok behavioral packet",
        comment_list_json_path=comment_path,
        video_item_json_path=item_path,
        profile_list_json_path=profile_path,
        subtitle_webvtt_path=webvtt_path,
    )

    assert code == 0
    packet_dir = Path(message)
    assert packet_dir.parent == root.path / "raw" / raw_shard(packet_dir.name)
    assert root.find_packet(packet_dir.name) is not None
    assert root.read_availability(packet_dir.name) is not None


def test_tiktok_video_cli_prints_complete_lane_note(tmp_path: Path, capsys) -> None:
    output = tmp_path / "packet"
    comment_path = tmp_path / "comments.json"
    item_path = tmp_path / "item.json"
    webvtt_path = tmp_path / "subtitle.vtt"
    comment_path.write_bytes(_comment_payload())
    item_path.write_bytes(_video_item_payload())
    webvtt_path.write_bytes(_webvtt())

    code = tiktok_video_main(
        [
            "--video-id",
            VIDEO_ID,
            "--video-url",
            VIDEO_URL,
            "--comment-list-json",
            str(comment_path),
            "--video-item-json",
            str(item_path),
            "--subtitle-webvtt",
            str(webvtt_path),
            "--output",
            str(output),
        ]
    )

    captured = capsys.readouterr()
    assert code == 0
    assert COMPLETE_LANE_NOTE in captured.out
    assert str(output.resolve()) in captured.out


def test_tiktok_video_cli_surfaces_failure_exit_code(tmp_path: Path, capsys) -> None:
    output = tmp_path / "packet"
    comment_path = tmp_path / "comments.json"
    comment_path.write_bytes(_comment_payload())

    with pytest.raises(SystemExit) as excinfo:
        tiktok_video_main(
            [
                "--video-id",
                VIDEO_ID,
                "--video-url",
                f"{VIDEO_URL}?lang=en",
                "--comment-list-json",
                str(comment_path),
                "--output",
                str(output),
            ]
        )

    captured = capsys.readouterr()
    assert excinfo.value.code == 5
    assert "without query" in captured.err
