from __future__ import annotations

import json

import pytest

from data_lake.root import DataLakeRoot, DataLakeRootError
from source_capture.ig_reels_grid_projection import (
    IG_REELS_PROJECTION_CERTIFICATION,
    IG_REELS_PROJECTION_METHOD,
    PROJECTION_IG_REELS_GRID_LANE,
    IgProjectionRawAnchor,
    IgProjectionRawRef,
    IgReelsGridProjectionRow,
    build_ig_reels_grid_projection,
    build_ig_reels_grid_projection_from_packet_directory,
    project_ig_reels_grid_into_lake,
)
from source_capture.models import (
    CaptureModeCategory,
    CoverageWindow,
    MetricObservation,
    MetricPosture,
    PacketTiming,
    PreservedFile,
    ReceiptMetadata,
    SourceCapturePacket,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.writer import write_local_source_capture_packet

CAPTURE_TIME = "2026-06-22T20:48:29Z"
SELECTION_POLICY_VERSION = "ig_reels_grid_capture_selection_v0"
HANDLE = "jeremyfragrance"
FINAL_URL = f"https://www.instagram.com/{HANDLE}/reels/"
CAPTURE_FILE = "raw/ig_reels_grid_capture.json"


def test_projection_carries_source_surface_disagreement() -> None:
    packet, raw = _reels_packet()

    projection = build_ig_reels_grid_projection(packet=packet, raw_file_bytes_by_file_id=raw)

    view = _row(projection, "ig_reels_grid_01", "view_count")
    # The slice collapsed the surfaces to one number (2984); the projection re-attaches all.
    assert view.value == 2984
    assert view.posture is MetricPosture.OBSERVED
    assert view.row_kind == "ig_media_metric"
    assert view.content_kind == "reel"
    assert view.content_shortcode == "DZ4Stb5MVPB"
    assert view.join_status == "joined_by_shortcode"
    assert view.selection_policy_version == SELECTION_POLICY_VERSION
    # DOM (2984) ties /clips/user (2984) but the value was sourced from the preferred JSON
    # surface, not DOM -- attribution must resolve to /clips/user, never DOM.
    assert view.chosen_source_surface == "clips_user_json_metadata"
    disagreement = {c.source_surface: c.value for c in view.source_surface_count_candidates}
    assert disagreement == {
        "dom_grid_engagement": 2984,
        "clips_user_json_metadata": 2984,
        "web_profile_info_json_metadata": 655,
    }
    dom_candidate = next(c for c in view.source_surface_count_candidates if c.source_surface == "dom_grid_engagement")
    assert dom_candidate.raw_text == "2,984"
    # Anchored back into the preserved capture file by json_pointer.
    assert view.raw_anchor.json_pointer == "/joined_rows/0"
    assert view.raw_anchor.file_id == packet.preserved_files[0].file_id
    # Mechanical raw ad-candidate fact carried as a candidate, never a conclusion.
    assert view.source_visible_fields["is_paid_partnership_candidate"] is True
    assert "clips_user_json_metadata" in projection.loss_ledger.source_surfaces_observed


def test_projection_missing_json_join_promotes_parseable_dom_grid_metric() -> None:
    packet, raw = _reels_packet()

    projection = build_ig_reels_grid_projection(packet=packet, raw_file_bytes_by_file_id=raw)

    view = _row(projection, "ig_reels_grid_02", "view_count")
    assert view.join_status == "missing_json"
    assert view.posture is MetricPosture.OBSERVED
    assert view.value == 1630
    assert view.reason is None
    assert view.chosen_source_surface == "dom_grid_engagement"
    assert "metric_value_from_dom_grid_no_passive_json_join" in view.selection_limitations
    assert "ig_reels_dom_grid_metric_promoted:view_count" in view.residuals
    assert [(c.source_surface, c.value, c.raw_text) for c in view.source_surface_count_candidates] == [
        ("dom_grid_engagement", 1630, "1,630")
    ]

    like = _row(projection, "ig_reels_grid_02", "like_count")
    comment = _row(projection, "ig_reels_grid_02", "comment_count")
    assert like.value == 9
    assert like.chosen_source_surface == "dom_grid_engagement"
    assert comment.value == 0
    assert comment.chosen_source_surface == "dom_grid_engagement"

def test_projection_forces_static_post_view_count_not_applicable() -> None:
    packet, raw = _reels_packet()

    projection = build_ig_reels_grid_projection(packet=packet, raw_file_bytes_by_file_id=raw)

    view = _row(projection, "ig_reels_grid_03", "view_count")
    assert view.content_kind == "post"
    # The slice carried an (erroneous) observed view_count=9999; the projection forces it.
    assert view.posture is MetricPosture.NOT_APPLICABLE
    assert view.value is None
    assert view.reason == "static_post_view_count_not_applicable"
    assert projection.loss_ledger.static_view_count_not_applicable_rows == 1


def test_projection_carries_creator_follower_metric() -> None:
    packet, raw = _reels_packet()

    projection = build_ig_reels_grid_projection(packet=packet, raw_file_bytes_by_file_id=raw)

    follower = _row(projection, "ig_reels_profile_00", "follower_count")
    assert follower.row_kind == "ig_creator_metric"
    assert follower.content_kind == "profile"
    assert follower.value == 123456
    assert follower.join_status == "not_applicable"
    assert follower.chosen_source_surface == "web_profile_info_json_metadata"
    assert follower.raw_anchor.json_pointer == "/creator_profile_snapshot/follower_count"
    assert follower.username == HANDLE


def test_projection_rejects_non_ig_packet() -> None:
    packet, raw = _reels_packet(source_family="reddit")

    with pytest.raises(ValueError, match="source_family='instagram_creator'"):
        build_ig_reels_grid_projection(packet=packet, raw_file_bytes_by_file_id=raw)


def test_projection_requires_reels_capture_file() -> None:
    packet, raw = _reels_packet(capture_relative_path="raw/ig_profile_momentum.json")

    with pytest.raises(ValueError, match="ig_reels_grid_capture.json"):
        build_ig_reels_grid_projection(packet=packet, raw_file_bytes_by_file_id=raw)


def test_projection_row_rejects_judgment_field_name() -> None:
    with pytest.raises(ValueError, match="forbidden Judgment field"):
        IgReelsGridProjectionRow(
            row_id="r",
            row_kind="ig_media_metric",
            raw_ref=IgProjectionRawRef(packet_id="p", slice_id="s"),
            raw_anchor=IgProjectionRawAnchor(
                file_id="file_01",
                relative_packet_path=CAPTURE_FILE,
                sha256="a" * 64,
                hash_basis="raw_stored_bytes",
            ),
            content_kind="reel",
            metric="view_count",
            posture=MetricPosture.NOT_APPLICABLE,
            reason="static",
            join_status="joined_by_shortcode",
            source_visible_fields={"credibility_score": 1},
        )


def test_projection_from_directory_certifies_view_only(tmp_path) -> None:
    packet, raw = _reels_packet()
    packet_dir = _write_packet_dir(tmp_path, packet=packet, raw=raw)

    projection = build_ig_reels_grid_projection_from_packet_directory(packet_or_manifest_path=packet_dir)

    assert projection.projection_method == IG_REELS_PROJECTION_METHOD
    assert projection.certification == IG_REELS_PROJECTION_CERTIFICATION
    assert projection.selection_policy_version == SELECTION_POLICY_VERSION
    assert projection.loss_ledger.preserved_metric_rows == len(projection.rows)




def test_project_reels_grid_into_lake_appends_verified_projection(tmp_path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_reels_packet(root, tmp_path)

    projection, derived_path = project_ig_reels_grid_into_lake(
        data_root=root,
        packet_id=packet_id,
        record_id="rec1",
    )

    assert derived_path == root.path / "derived" / packet_id / PROJECTION_IG_REELS_GRID_LANE / "rec1.json"
    assert derived_path.is_file()
    assert projection.packet_id == packet_id

    container = root.find_packet(packet_id)
    assert container is not None
    expected = build_ig_reels_grid_projection_from_packet_directory(packet_or_manifest_path=container)
    expected_bytes = (
        f"{json.dumps(expected.model_dump(mode='json'), indent=2, sort_keys=True)}\n"
    ).encode("utf-8")
    assert derived_path.read_bytes() == expected_bytes

    assert root.load_raw_packet(packet_id).manifest["packet_id"] == packet_id


def test_project_reels_grid_rederive_appends_sibling_not_overwrite(tmp_path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_reels_packet(root, tmp_path)

    _, first = project_ig_reels_grid_into_lake(data_root=root, packet_id=packet_id)
    _, second = project_ig_reels_grid_into_lake(data_root=root, packet_id=packet_id)

    lane_dir = root.path / "derived" / packet_id / PROJECTION_IG_REELS_GRID_LANE
    assert first != second
    assert len(list(lane_dir.glob("*.json"))) == 2


def test_project_reels_grid_explicit_record_id_is_create_only(tmp_path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_reels_packet(root, tmp_path)

    project_ig_reels_grid_into_lake(data_root=root, packet_id=packet_id, record_id="rec1")
    with pytest.raises(DataLakeRootError):
        project_ig_reels_grid_into_lake(data_root=root, packet_id=packet_id, record_id="rec1")


def test_projection_carries_present_but_null_json_surface() -> None:
    # web_profile_info joined the shortcode but exposed no video/play count for THIS row;
    # it must still be carried as a candidate with value=None, not silently dropped.
    joined = [
        {
            "dom_row": _dom_row(0, "DZnull00000", "reel", "2,984", "30", "4"),
            "source_surface_candidates": [
                _json_candidate("clips_user_json_metadata", "DZnull00000", 2984, 30, 4),
                {
                    "source_surface": "web_profile_info_json_metadata",
                    "shortcode": "DZnull00000",
                    "video_or_play_count": None,
                    "like_count": 30,
                    "comment_count": 4,
                    "is_video": True,
                },
            ],
        }
    ]
    slices = [
        _slice("ig_reels_grid_01", f"https://www.instagram.com/{HANDLE}/reel/DZnull00000/", [_observed("view_count", 2984)])
    ]
    packet, raw = _packet_with(joined_rows=joined, slices=slices)

    projection = build_ig_reels_grid_projection(packet=packet, raw_file_bytes_by_file_id=raw)

    view = _row(projection, "ig_reels_grid_01", "view_count")
    by_surface = {c.source_surface: c.value for c in view.source_surface_count_candidates}
    assert by_surface["web_profile_info_json_metadata"] is None  # present surface, null count -> carried
    assert by_surface["clips_user_json_metadata"] == 2984
    assert view.chosen_source_surface == "clips_user_json_metadata"


def test_projection_carries_dom_surface_when_metric_text_absent() -> None:
    # The DOM row is present but exposes no comment count. The absent DOM value is
    # still part of the source-surface disagreement and must be carried as None.
    joined = [
        {
            "dom_row": _dom_row(0, "DZdomnull00", "reel", "2,984", "30", None),
            "source_surface_candidates": [
                _json_candidate("clips_user_json_metadata", "DZdomnull00", 2984, 30, 7),
            ],
        }
    ]
    slices = [
        _slice(
            "ig_reels_grid_01",
            f"https://www.instagram.com/{HANDLE}/reel/DZdomnull00/",
            [_observed("comment_count", 7)],
        )
    ]
    packet, raw = _packet_with(joined_rows=joined, slices=slices)

    projection = build_ig_reels_grid_projection(packet=packet, raw_file_bytes_by_file_id=raw)

    comment = _row(projection, "ig_reels_grid_01", "comment_count")
    by_surface = {c.source_surface: c.value for c in comment.source_surface_count_candidates}
    assert by_surface == {"dom_grid_engagement": None, "clips_user_json_metadata": 7}
    dom_candidate = next(
        c for c in comment.source_surface_count_candidates if c.source_surface == "dom_grid_engagement"
    )
    assert dom_candidate.raw_text is None


def test_projection_duplicate_shortcode_does_not_anchor_first_joined_row() -> None:
    shortcode = "DZdupe0000"
    residual = f"ig_reels_ambiguous_shortcode_join:{shortcode}"
    joined = [
        {
            "dom_row": _dom_row(0, shortcode, "reel", "111", "10", "1"),
            "source_surface_candidates": [_json_candidate("clips_user_json_metadata", shortcode, 111, 10, 1)],
        },
        {
            "dom_row": _dom_row(1, shortcode, "reel", "222", "20", "2"),
            "source_surface_candidates": [_json_candidate("web_profile_info_json_metadata", shortcode, 222, 20, 2)],
        },
    ]
    slices = [
        _slice(
            "ig_reels_grid_01",
            f"https://www.instagram.com/{HANDLE}/reel/{shortcode}/",
            [_observed("view_count", 111)],
        )
    ]
    packet, raw = _packet_with(joined_rows=joined, slices=slices)

    projection = build_ig_reels_grid_projection(packet=packet, raw_file_bytes_by_file_id=raw)

    view = _row(projection, "ig_reels_grid_01", "view_count")
    assert view.value == 111  # selected slice value is still carried verbatim
    assert view.join_status == "ambiguous"
    assert view.raw_anchor.json_pointer is None
    assert view.source_surface_count_candidates == []
    assert view.chosen_source_surface is None
    assert residual in view.residuals
    assert residual in projection.residuals
    assert projection.loss_ledger.structure_preserved is False


def test_projection_profile_missing_metric_field_anchors_snapshot_object() -> None:
    residual = "ig_reels_profile_metric_field_absent:follower_count"
    slices = [
        _slice(
            "ig_reels_profile_00",
            FINAL_URL,
            [
                MetricObservation(
                    metric="follower_count",
                    posture=MetricPosture.UNAVAILABLE_WITH_REASON,
                    reason="web_profile_info passive JSON did not yield exact follower_count",
                    coverage_window=CoverageWindow(end=CAPTURE_TIME),
                )
            ],
        )
    ]
    packet, raw = _packet_with(
        joined_rows=[],
        slices=slices,
        snapshot={"source_profile": HANDLE, "parse_status": "parsed_web_profile_info_json_metadata"},
    )

    projection = build_ig_reels_grid_projection(packet=packet, raw_file_bytes_by_file_id=raw)

    follower = _row(projection, "ig_reels_profile_00", "follower_count")
    assert follower.raw_anchor.json_pointer == "/creator_profile_snapshot"
    assert residual in follower.residuals
    assert residual in projection.residuals
    assert projection.loss_ledger.structure_preserved is False


def test_projection_does_not_reattribute_json_selected_value_to_dom() -> None:
    # This is already an observed upstream value, so projection does not infer DOM source
    # provenance merely because the number matches only DOM. DOM fallback is only for
    # unavailable metrics where JSON did not join.
    joined = [
        {
            "dom_row": _dom_row(0, "DZdomonly00", "reel", "655", "9", "0"),
            "source_surface_candidates": [_json_candidate("clips_user_json_metadata", "DZdomonly00", 999, 9, 0)],
        }
    ]
    slices = [
        _slice("ig_reels_grid_01", f"https://www.instagram.com/{HANDLE}/reel/DZdomonly00/", [_observed("view_count", 655)])
    ]
    packet, raw = _packet_with(joined_rows=joined, slices=slices)

    projection = build_ig_reels_grid_projection(packet=packet, raw_file_bytes_by_file_id=raw)

    view = _row(projection, "ig_reels_grid_01", "view_count")
    assert view.chosen_source_surface is None
    assert {c.source_surface: c.value for c in view.source_surface_count_candidates} == {
        "dom_grid_engagement": 655,
        "clips_user_json_metadata": 999,
    }


def test_projection_dom_grid_fallback_parses_compact_k_m_counts() -> None:
    joined = [
        {
            "dom_row": _dom_row(0, "DZcompact00", "reel", "1.4M", "73.5K", "536"),
            "source_surface_candidates": [],
        }
    ]
    slices = [
        _slice(
            "ig_reels_grid_01",
            f"https://www.instagram.com/{HANDLE}/reel/DZcompact00/",
            [_gap("view_count"), _gap("like_count"), _gap("comment_count")],
            limitations=["no_passive_json_join_for_shortcode"],
        )
    ]
    packet, raw = _packet_with(joined_rows=joined, slices=slices)

    projection = build_ig_reels_grid_projection(packet=packet, raw_file_bytes_by_file_id=raw)

    view = _row(projection, "ig_reels_grid_01", "view_count")
    like = _row(projection, "ig_reels_grid_01", "like_count")
    comment = _row(projection, "ig_reels_grid_01", "comment_count")
    assert view.value == 1400000
    assert like.value == 73500
    assert comment.value == 536
    assert {view.chosen_source_surface, like.chosen_source_surface, comment.chosen_source_surface} == {
        "dom_grid_engagement"
    }

def test_projection_static_already_not_applicable_is_preserved() -> None:
    # A static /p/ row whose view_count is ALREADY not_applicable passes through unchanged
    # and is not counted as a forced override.
    joined = [{"dom_row": _dom_row(0, "DZstatic000", "post", None, "5", "1"), "source_surface_candidates": []}]
    slices = [
        _slice(
            "ig_reels_grid_03",
            f"https://www.instagram.com/{HANDLE}/p/DZstatic000/",
            [
                MetricObservation(
                    metric="view_count",
                    posture=MetricPosture.NOT_APPLICABLE,
                    reason="joined passive JSON marks this media as non-video/static",
                    coverage_window=CoverageWindow(end=CAPTURE_TIME),
                )
            ],
        )
    ]
    packet, raw = _packet_with(joined_rows=joined, slices=slices)

    projection = build_ig_reels_grid_projection(packet=packet, raw_file_bytes_by_file_id=raw)

    view = _row(projection, "ig_reels_grid_03", "view_count")
    assert view.content_kind == "post"
    assert view.posture is MetricPosture.NOT_APPLICABLE
    assert view.value is None
    assert projection.loss_ledger.static_view_count_not_applicable_rows == 0


def _packet_with(*, joined_rows, slices, snapshot=None) -> tuple[SourceCapturePacket, dict[str, bytes]]:
    default_snapshot = {"source_profile": HANDLE, "follower_count": 123456}
    cap = {
        "capture_metadata": {
            "source_surface": "ig_reels_grid_dom_passive_json",
            "selection_policy_version": SELECTION_POLICY_VERSION,
        },
        "creator_profile_snapshot": default_snapshot if snapshot is None else snapshot,
        "joined_rows": joined_rows,
    }
    raw = {"file_01": _json_bytes(cap)}
    packet = SourceCapturePacket(
        packet_id="pkt-ig-reels",
        manifest_version="source_capture_packet_manifest_v1",
        obligation_contract_version="core_spine_v0_data_capture_spine_obligation_contract_v0",
        source_family="instagram_creator",
        source_surface="ig_reels_grid_dom_passive_json",
        source_locator=known_fact(FINAL_URL),
        requested_decision_context=known_fact("creator monitoring"),
        capture_context=known_fact("logged-out IG public /reels/ grid capture"),
        actor_audience_context=known_fact("public creator profile"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="ig_reels_grid_cli_operator",
        session_identity="",
        timing=_timing(unknown_with_reason("profile grid slice is the enumeration source")),
        access_posture=known_fact("ig_logged_out_reels_grid_browser_capture"),
        archive_history_posture=not_attempted("IG reels-grid runner does not query archive services"),
        media_modality_posture=known_fact("DOM media-anchor text and passive JSON preserved"),
        re_capture_relationship=not_applicable("no prior source capture packet"),
        source_slices=slices,
        preserved_files=[_preserved_file("file_01", CAPTURE_FILE, raw["file_01"])],
        receipt_metadata=ReceiptMetadata(
            title="Source Capture Packet Receipt",
            generated_at=CAPTURE_TIME,
            summary="summary",
            non_claims=["not projection"],
        ),
    )
    return packet, raw


# --- construction helpers -------------------------------------------------


def _capture_payload() -> dict[str, object]:
    return {
        "capture_metadata": {
            "source_surface": "ig_reels_grid_dom_passive_json",
            "selection_policy_version": SELECTION_POLICY_VERSION,
        },
        "creator_profile_snapshot": {
            "platform": "instagram",
            "source_profile": HANDLE,
            "numeric_id": "42",
            "follower_count": 123456,
            "following_count": 10,
            "post_or_media_count": 500,
            "bio_links_count": 2,
            "category_name": "Public figure",
            "is_verified": True,
            "is_private": False,
            "parse_status": "parsed_web_profile_info_json_metadata",
        },
        "joined_rows": [
            {
                "dom_row": _dom_row(0, "DZ4Stb5MVPB", "reel", "2,984", "30", "4"),
                "source_surface_candidates": [
                    _json_candidate("clips_user_json_metadata", "DZ4Stb5MVPB", 2984, 30, 4, is_paid_partnership=True),
                    _json_candidate("web_profile_info_json_metadata", "DZ4Stb5MVPB", 655, 30, 4),
                ],
            },
            {
                "dom_row": _dom_row(1, "DZ4SnoJSON", "reel", "1,630", "9", "0"),
                "source_surface_candidates": [],
            },
            {
                "dom_row": _dom_row(2, "DZ4Static0", "post", None, "5", "1"),
                "source_surface_candidates": [
                    _json_candidate("clips_user_json_metadata", "DZ4Static0", 9999, 5, 1, is_video=False),
                ],
            },
        ],
    }


def _dom_row(index, shortcode, kind, views_text, likes_text, comments_text) -> dict[str, object]:
    leaf = [t for t in (views_text, likes_text, comments_text) if t is not None]
    permalink = f"https://www.instagram.com/{HANDLE}/{kind}/{shortcode}/"
    return {
        "index": index,
        "path": f"/{HANDLE}/{kind}/{shortcode}/",
        "permalink_url": permalink,
        "shortcode": shortcode,
        "kind": kind,
        "visible_text": views_text,
        "visible_numeric_texts": [views_text] if views_text else [],
        "hidden_leaf_numeric_texts": leaf,
        "hidden_engagement_candidates": [likes_text, comments_text],
        "views_text": views_text,
        "likes_text": likes_text,
        "comments_text": comments_text,
        "parse_status": "parsed_no_hover_grid_engagement" if kind == "reel" else "static_post_view_count_not_applicable",
        "rect": None,
    }


def _json_candidate(
    source_surface, shortcode, video_or_play_count, like_count, comment_count, *, is_paid_partnership=None, is_video=True
) -> dict[str, object]:
    return {
        "source_surface": source_surface,
        "shortcode": shortcode,
        "taken_at_timestamp": 1750000000,
        "taken_at_utc": "2026-06-15T00:00:00Z",
        "caption_text": "new drop #ad" if is_paid_partnership else "daily reel",
        "caption_length": 12,
        "product_type": "clips",
        "typename": "GraphVideo",
        "is_video": is_video,
        "video_or_play_count": video_or_play_count,
        "video_or_play_count_key": "ig_play_count",
        "video_or_play_count_candidates": [["ig_play_count", video_or_play_count]],
        "like_count": like_count,
        "comment_count": comment_count,
        "is_paid_partnership": is_paid_partnership,
        "is_affiliate": None,
        "sponsor_users": ["acme"] if is_paid_partnership else [],
        "ad_term_candidates": ["#ad"] if is_paid_partnership else [],
        "pinned_on_clips_tab": False,
        "pinned_on_timeline": None,
        "raw_node_keys_sample": ["shortcode", "video_view_count"],
    }




def _commit_reels_packet(root: DataLakeRoot, tmp_path) -> str:
    packet, _raw = _reels_packet()
    capture_path = tmp_path / "ig_reels_grid_capture.json"
    capture_path.write_bytes(_json_bytes(_capture_payload()))
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[capture_path],
        source_family="instagram_creator",
        source_surface="ig_reels_grid_dom_passive_json",
        source_locator=known_fact(FINAL_URL),
        decision_question="creator monitoring",
        capture_context="logged-out IG public /reels/ grid capture",
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="ig_reels_grid_cli_operator",
        source_slices=packet.source_slices,
        access_posture=known_fact("ig_logged_out_reels_grid_browser_capture"),
        archive_history_posture=not_attempted("IG reels-grid runner does not query archive services"),
        media_modality_posture=known_fact("DOM media-anchor text and passive JSON preserved"),
        re_capture_relationship=not_applicable("no prior source capture packet"),
        limitations=packet.limitations,
        receipt_non_claims=["not projection"],
    )
    return result.packet.packet_id


def _reels_packet(
    *,
    source_family: str = "instagram_creator",
    capture_relative_path: str = CAPTURE_FILE,
) -> tuple[SourceCapturePacket, dict[str, bytes]]:
    raw = {"file_01": _json_bytes(_capture_payload())}
    slices = [
        _slice(
            "ig_reels_profile_00",
            FINAL_URL,
            [_observed("follower_count", 123456)],
        ),
        _slice(
            "ig_reels_grid_01",
            f"https://www.instagram.com/{HANDLE}/reel/DZ4Stb5MVPB/",
            [_observed("view_count", 2984), _observed("like_count", 30), _observed("comment_count", 4)],
        ),
        _slice(
            "ig_reels_grid_02",
            f"https://www.instagram.com/{HANDLE}/reel/DZ4SnoJSON/",
            [_gap("view_count"), _gap("like_count"), _gap("comment_count")],
            limitations=["no_passive_json_join_for_shortcode"],
        ),
        _slice(
            "ig_reels_grid_03",
            f"https://www.instagram.com/{HANDLE}/p/DZ4Static0/",
            [_observed("view_count", 9999), _observed("like_count", 5), _observed("comment_count", 1)],
        ),
    ]
    packet = SourceCapturePacket(
        packet_id="pkt-ig-reels",
        manifest_version="source_capture_packet_manifest_v1",
        obligation_contract_version="core_spine_v0_data_capture_spine_obligation_contract_v0",
        source_family=source_family,
        source_surface="ig_reels_grid_dom_passive_json",
        source_locator=known_fact(FINAL_URL),
        requested_decision_context=known_fact("creator monitoring"),
        capture_context=known_fact("logged-out IG public /reels/ grid capture"),
        actor_audience_context=known_fact("public creator profile"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="ig_reels_grid_cli_operator",
        session_identity="",
        timing=_timing(unknown_with_reason("profile grid slice is the enumeration source")),
        access_posture=known_fact("ig_logged_out_reels_grid_browser_capture"),
        archive_history_posture=not_attempted("IG reels-grid runner does not query archive services"),
        media_modality_posture=known_fact("DOM media-anchor text and passive JSON preserved"),
        re_capture_relationship=not_applicable("no prior source capture packet"),
        source_slices=slices,
        preserved_files=[_preserved_file("file_01", capture_relative_path, raw["file_01"])],
        limitations=["media_slice_limitations_present: 1 grid row(s) carried row-level limitations"],
        receipt_metadata=ReceiptMetadata(
            title="Source Capture Packet Receipt",
            generated_at=CAPTURE_TIME,
            summary="summary",
            non_claims=["not projection"],
        ),
    )
    return packet, raw


def _slice(slice_id, locator, metric_observations, *, limitations=None) -> SourceCaptureSlice:
    return SourceCaptureSlice(
        slice_id=slice_id,
        locator=known_fact(locator),
        timing=_timing(unknown_with_reason("reels grid slice")),
        access_posture=known_fact("ig_logged_out_reels_grid_browser_capture"),
        archive_history_posture=not_attempted("IG reels-grid runner does not query archive services"),
        media_modality_posture=known_fact("DOM media-anchor text and passive JSON preserved"),
        re_capture_relationship=not_applicable("no prior source capture packet"),
        preserved_file_ids=["file_01"],
        limitations=list(limitations or []),
        metric_observations=metric_observations,
    )


def _observed(metric: str, value: int) -> MetricObservation:
    return MetricObservation(
        metric=metric,
        posture=MetricPosture.OBSERVED,
        value=value,
        coverage_window=CoverageWindow(end=CAPTURE_TIME),
    )


def _gap(metric: str) -> MetricObservation:
    return MetricObservation(
        metric=metric,
        posture=MetricPosture.UNAVAILABLE_WITH_REASON,
        reason="no joined passive JSON candidate for this shortcode",
        coverage_window=CoverageWindow(end=CAPTURE_TIME),
    )


def _timing(publication) -> PacketTiming:
    return PacketTiming(
        source_publication_or_event=publication,
        source_edit_or_version=unknown_with_reason("not inferred"),
        capture_time=known_fact(CAPTURE_TIME),
        recapture_time=not_applicable("no prior capture"),
        cutoff_posture=unknown_with_reason("not supplied"),
    )


def _preserved_file(file_id: str, relative_path: str, body: bytes) -> PreservedFile:
    return PreservedFile(
        file_id=file_id,
        original_path=relative_path,
        relative_packet_path=relative_path,
        sha256="a" * 64,
        hash_basis="raw_stored_bytes",
        size_bytes=len(body),
    )


def _write_packet_dir(tmp_path, *, packet: SourceCapturePacket, raw: dict[str, bytes]):
    packet_dir = tmp_path / "packet"
    for preserved_file in packet.preserved_files:
        raw_path = packet_dir / preserved_file.relative_packet_path
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_bytes(raw[preserved_file.file_id])
    (packet_dir / "manifest.json").write_text(
        f"{json.dumps(packet.model_dump(mode='json'), indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )
    return packet_dir


def _row(projection, slice_id: str, metric: str) -> IgReelsGridProjectionRow:
    return next(
        row
        for row in projection.rows
        if row.raw_ref.slice_id == slice_id and row.metric == metric
    )


def _json_bytes(payload: dict[str, object]) -> bytes:
    return json.dumps(payload, sort_keys=True).encode("utf-8")
