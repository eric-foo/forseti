"""Seam catch-up tests for the IG reels-grid projection lane.

Mirrors the adjudicated catch-up suite shape (discovery finds its own backlog;
second run is a no-op; policy bump re-surfaces; failures are loud, isolated,
and never acked; known other-lane surfaces are acked out-of-scope; unknown
surfaces are visible, never acked; reconcile failures are per-packet statuses)
plus this lane's specifics: dereferenceable ack evidence and byte-deterministic
re-derivation (the projection is a pure function of raw bytes + policy).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from capture_spine.creator_profile_current.instagram_metric_seed import (
    build_instagram_reels_creator_metric_seed_from_files,
    discover_instagram_reels_projection_paths_from_lake,
)
import runners.run_ig_reels_grid_projection_catchup as catchup
from data_lake.consumption import find_acks
from data_lake.root import DataLakeRoot, raw_shard
from harness_utils import generate_ulid
from source_capture.ig_reels_grid_projection import (
    PROJECTION_IG_REELS_GRID_LANE,
    project_ig_reels_grid_into_lake,
)
from source_capture.models import (
    CaptureModeCategory,
    CoverageWindow,
    MetricObservation,
    MetricPosture,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.writer import write_local_source_capture_packet

CAPTURE_TIME = "2026-06-22T20:48:29Z"
HANDLE = "syntheticcreator"
FINAL_URL = f"https://www.instagram.com/{HANDLE}/reels/"
SHORTCODE = "DZsynth0001"


def _account_ledger() -> dict[str, object]:
    return {
        "platform_accounts": [
            {
                "platform_account_id": "acct_ig_synthetic_001",
                "platform": "instagram",
                "public_handle": HANDLE,
                "public_profile_url": f"https://www.instagram.com/{HANDLE}/",
            }
        ]
    }


def _capture_payload() -> dict[str, object]:
    return {
        "capture_metadata": {
            "source_surface": "ig_reels_grid_dom_passive_json",
            "selection_policy_version": "ig_reels_grid_capture_selection_v0",
        },
        "creator_profile_snapshot": {"source_profile": HANDLE, "follower_count": 4321},
        "joined_rows": [
            {
                "dom_row": {
                    "index": 0,
                    "path": f"/{HANDLE}/reel/{SHORTCODE}/",
                    "permalink_url": f"https://www.instagram.com/{HANDLE}/reel/{SHORTCODE}/",
                    "shortcode": SHORTCODE,
                    "kind": "reel",
                    "views_text": "1,200",
                    "likes_text": "34",
                    "comments_text": "5",
                },
                "source_surface_candidates": [
                    {
                        "source_surface": "clips_user_json_metadata",
                        "shortcode": SHORTCODE,
                        "video_or_play_count": 1200,
                        "like_count": 34,
                        "comment_count": 5,
                        "is_video": True,
                    }
                ],
            }
        ],
    }


def _timing() -> PacketTiming:
    return PacketTiming(
        source_publication_or_event=unknown_with_reason("grid slice is the enumeration source"),
        source_edit_or_version=unknown_with_reason("not inferred"),
        capture_time=known_fact(CAPTURE_TIME),
        recapture_time=not_applicable("no prior capture"),
        cutoff_posture=unknown_with_reason("not supplied"),
    )


def _slices() -> list[SourceCaptureSlice]:
    def make(slice_id: str, locator: str, observations: list[MetricObservation]) -> SourceCaptureSlice:
        return SourceCaptureSlice(
            slice_id=slice_id,
            locator=known_fact(locator),
            timing=_timing(),
            access_posture=known_fact("ig_logged_out_reels_grid_browser_capture"),
            archive_history_posture=not_attempted("grid capture does not query archive services"),
            media_modality_posture=known_fact("DOM media-anchor text and passive JSON preserved"),
            re_capture_relationship=not_applicable("no prior source capture packet"),
            preserved_file_ids=["file_01"],
            limitations=[],
            metric_observations=observations,
        )

    def observed(metric: str, value: int) -> MetricObservation:
        return MetricObservation(
            metric=metric,
            posture=MetricPosture.OBSERVED,
            value=value,
            coverage_window=CoverageWindow(end=CAPTURE_TIME),
        )

    return [
        make("ig_reels_profile_00", FINAL_URL, [observed("follower_count", 4321)]),
        make(
            "ig_reels_grid_01",
            f"https://www.instagram.com/{HANDLE}/reel/{SHORTCODE}/",
            [observed("view_count", 1200), observed("like_count", 34), observed("comment_count", 5)],
        ),
    ]


def _commit_packet(root: DataLakeRoot, tmp_path: Path, *, source_surface: str | None = None) -> str:
    capture_path = tmp_path / f"capture_{generate_ulid()}" / "ig_reels_grid_capture.json"
    capture_path.parent.mkdir(parents=True)
    capture_path.write_bytes(json.dumps(_capture_payload(), sort_keys=True).encode("utf-8"))
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[capture_path],
        source_family="instagram_creator",
        source_surface=source_surface or "ig_reels_grid_dom_passive_json",
        source_locator=known_fact(FINAL_URL),
        decision_question="creator monitoring",
        capture_context="logged-out IG public /reels/ grid capture",
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="ig_reels_grid_cli_operator",
        source_slices=_slices(),
        access_posture=known_fact("ig_logged_out_reels_grid_browser_capture"),
        archive_history_posture=not_attempted("grid capture does not query archive services"),
        media_modality_posture=known_fact("DOM media-anchor text and passive JSON preserved"),
        re_capture_relationship=not_applicable("no prior source capture packet"),
        receipt_non_claims=["not projection"],
    )
    return result.packet.packet_id


def _derived_lane_dir(root: DataLakeRoot, packet_id: str) -> Path:
    return root.lane_dir(
        subtree="derived", raw_anchor=packet_id, lane=PROJECTION_IG_REELS_GRID_LANE
    )


def _acks(root: DataLakeRoot, packet_id: str) -> list[dict]:
    return find_acks(root, raw_anchor=packet_id, ack_namespace=PROJECTION_IG_REELS_GRID_LANE)


def test_catchup_discovers_derives_and_acks(tmp_path: Path) -> None:
    # S1: the lane finds its own backlog — a committed grid packet nobody pointed
    # at gets its derived projection record plus a lane-owned ack citing it.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root, tmp_path)

    results = catchup.run_catchup(data_root=root)

    assert [entry["status"] for entry in results] == ["derived"]
    assert results[0]["packet_id"] == pid
    assert results[0]["row_count"] > 0
    assert len(list(_derived_lane_dir(root, pid).iterdir())) == 1
    acks = _acks(root, pid)
    assert len(acks) == 1
    assert acks[0]["obligation"]["consumer"] == "ig_reels_grid_projection_catchup"


def test_second_run_is_a_no_op(tmp_path: Path) -> None:
    # S2: acked-and-unchanged packets emit no statuses and gain no new siblings.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root, tmp_path)
    catchup.run_catchup(data_root=root)

    second = catchup.run_catchup(data_root=root)

    assert second == []
    assert len(list(_derived_lane_dir(root, pid).iterdir())) == 1
    assert len(_acks(root, pid)) == 1


def test_policy_bump_re_surfaces_and_re_derives(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # S3: changing an enumerated policy constant changes the obligation
    # fingerprint, so an already-acked packet re-surfaces and re-derives.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root, tmp_path)
    catchup.run_catchup(data_root=root)

    monkeypatch.setattr(catchup, "IG_REELS_PROJECTION_VERSION", "v0-test-bump")
    results = catchup.run_catchup(data_root=root)

    assert [entry["status"] for entry in results] == ["derived"]
    assert len(_acks(root, pid)) == 2
    assert len(list(_derived_lane_dir(root, pid).iterdir())) == 2


def test_check_mode_counts_pending_without_writing(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root, tmp_path)

    assert catchup.pending_packets(data_root=root) == [pid]
    assert not _derived_lane_dir(root, pid).is_dir()

    catchup.run_catchup(data_root=root)
    assert catchup.pending_packets(data_root=root) == []


def test_catchup_record_wins_consumer_tie_break_against_stale_catalog_sibling(
    tmp_path: Path,
) -> None:
    # The real creator-metric seed selects via the lane's DECLARED record-id
    # derivation rank (catch-up supersedes earlier siblings of the same anchor).
    # A stale bronze_catalog sibling must not beat the catch-up record the seam
    # just wrote -- regardless of lexical order (F-IGRC-001).
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root, tmp_path)
    (result,) = catchup.run_catchup(data_root=root)
    catchup_path = _derived_lane_dir(root, pid) / result["derived_record_id"]
    assert catchup_path.name.startswith(catchup._CATCHUP_RECORD_ID_PREFIX)

    stale_projection = json.loads(catchup_path.read_text(encoding="utf-8"))
    for row in stale_projection["rows"]:
        if row.get("content_shortcode") == SHORTCODE and row.get("metric") == "view_count":
            row["value"] = 9999
            break
    else:  # pragma: no cover - fixture guard
        raise AssertionError("fixture projection did not contain the reel view_count row")
    stale_path = root.append_record(
        subtree="derived",
        raw_anchor=pid,
        lane=PROJECTION_IG_REELS_GRID_LANE,
        record_id="bronze_catalog_ig_reels_grid_v0_stale.json",
        data=(json.dumps(stale_projection, indent=2, sort_keys=True) + "\n").encode("utf-8"),
    )

    paths = discover_instagram_reels_projection_paths_from_lake(root)
    assert catchup_path in paths
    assert stale_path in paths
    document = build_instagram_reels_creator_metric_seed_from_files(
        projection_paths=paths,
        account_ledger=_account_ledger(),
        generated_at_utc="2026-06-22T21:00:00Z",
    )
    seed = document["instagram_reels_creator_metric_seed"]

    assert seed["source_inputs"][0]["source_pointer"] == str(catchup_path)
    view_rows = [
        item
        for item in seed["metric_observations"]
        if item["content_id_or_none"] == SHORTCODE and item["metric_name"] == "view_count"
    ]
    assert [item["metric_value_or_none"] for item in view_rows] == [1200]


def test_derive_failure_is_loud_isolated_and_never_acked(tmp_path: Path) -> None:
    # S4+S5: a packet whose preserved capture file no longer matches its manifest
    # hash fails its verified read; the failure is a visible status, the packet
    # stays unacknowledged (re-surfaces), and a healthy packet still derives.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    bad_pid = _commit_packet(root, tmp_path)
    good_pid = _commit_packet(root, tmp_path)
    container = root.path / "raw" / raw_shard(bad_pid) / bad_pid
    manifest = json.loads((container / "manifest.json").read_text(encoding="utf-8"))
    preserved_relpath = manifest["preserved_files"][0]["relative_packet_path"]
    (container / preserved_relpath).write_bytes(b"{} tampered")

    results = catchup.run_catchup(data_root=root)

    by_pid = {entry["packet_id"]: entry for entry in results}
    assert by_pid[bad_pid]["status"] == "derive_failed"
    assert by_pid[good_pid]["status"] == "derived"
    assert _acks(root, bad_pid) == []
    rerun = {entry["packet_id"]: entry["status"] for entry in catchup.run_catchup(data_root=root)}
    assert rerun == {bad_pid: "derive_failed"}


def test_known_other_lane_surface_is_acked_out_of_scope(tmp_path: Path) -> None:
    # F-FRAG-002 shape for a shared family: a packet owned by the ASR lane has no
    # grid-projectable content; the discovery outcome is the completion evidence.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root, tmp_path, source_surface="ig_reels_audio")

    results = catchup.run_catchup(data_root=root)

    assert [entry["status"] for entry in results] == ["acked_no_projectable_content"]
    assert results[0]["source_surface"] == "ig_reels_audio"
    assert not _derived_lane_dir(root, pid).is_dir()
    (ack,) = _acks(root, pid)
    assert ack["evidence"][0]["kind"] == "no_grid_projectable_content_for_surface"
    # leaves the backlog: second run is a no-op
    assert catchup.run_catchup(data_root=root) == []


def test_unsupported_surface_is_visible_and_never_acked(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root, tmp_path, source_surface="mystery_future_surface")

    first = catchup.run_catchup(data_root=root)
    second = catchup.run_catchup(data_root=root)

    for results in (first, second):
        assert [entry["status"] for entry in results] == ["unsupported_surface"]
        assert results[0]["source_surface"] == "mystery_future_surface"
    assert _acks(root, pid) == []


def test_out_of_scope_surface_policy_change_re_surfaces_previous_ack(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root, tmp_path, source_surface="ig_reels_audio")
    assert [entry["status"] for entry in catchup.run_catchup(data_root=root)] == [
        "acked_no_projectable_content"
    ]

    monkeypatch.setattr(catchup, "_KNOWN_OUT_OF_SCOPE_SURFACES", frozenset())
    second = catchup.run_catchup(data_root=root)

    assert [entry["status"] for entry in second] == ["unsupported_surface"]
    assert second[0]["source_surface"] == "ig_reels_audio"
    assert len(_acks(root, pid)) == 1


def test_reconcile_failure_is_per_packet_and_healthy_packets_proceed(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    good_pid = _commit_packet(root, tmp_path)
    corrupt_pid = generate_ulid()
    corrupt_dir = root.path / "raw" / raw_shard(corrupt_pid) / corrupt_pid
    corrupt_dir.mkdir(parents=True)
    (corrupt_dir / "manifest.json").write_text("{not json", encoding="utf-8")

    results = catchup.run_catchup(data_root=root)

    by_pid = {entry["packet_id"]: entry for entry in results}
    assert by_pid[corrupt_pid]["status"] == "availability_reconcile_failed"
    assert by_pid[good_pid]["status"] == "derived"


def test_pending_check_fails_loud_on_reconcile_failure(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    corrupt_pid = generate_ulid()
    corrupt_dir = root.path / "raw" / raw_shard(corrupt_pid) / corrupt_pid
    corrupt_dir.mkdir(parents=True)
    (corrupt_dir / "manifest.json").write_text("{not json", encoding="utf-8")

    with pytest.raises(Exception, match="availability reconcile failed"):
        catchup.pending_packets(data_root=root)


def test_ack_evidence_is_dereferenceable(tmp_path: Path) -> None:
    # The ack must say how completion is checkable: the cited derived record
    # exists and its read-back hash matches the recorded content_sha256.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root, tmp_path)
    catchup.run_catchup(data_root=root)

    (ack,) = _acks(root, pid)
    evidence = {entry["kind"]: entry for entry in ack["evidence"]}
    derived_file = _derived_lane_dir(root, pid) / evidence["derived_record"]["record_id"]
    body = derived_file.read_bytes()
    assert hashlib.sha256(body).hexdigest() == evidence["derived_record"]["content_sha256"]
    assert evidence["derived_record"]["byte_count"] == len(body)
    projection = json.loads(body.decode("utf-8"))
    assert evidence["projection_counts"]["row_count"] == len(projection["rows"])


def test_catchup_derivation_is_byte_deterministic(tmp_path: Path) -> None:
    # The projection is a pure function of (immutable raw, policy): a manual
    # re-derivation of the same packet produces byte-identical content under a
    # fresh sibling id.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root, tmp_path)
    catchup.run_catchup(data_root=root)
    (first_file,) = _derived_lane_dir(root, pid).iterdir()

    _, second_path = project_ig_reels_grid_into_lake(data_root=root, packet_id=pid)

    assert second_path.name != first_file.name
    assert second_path.read_bytes() == first_file.read_bytes()


def test_cli_requires_exactly_one_mode() -> None:
    with pytest.raises(SystemExit) as excinfo:
        catchup.main([])
    assert excinfo.value.code == 2
