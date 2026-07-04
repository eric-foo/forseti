"""Seam catch-up tests for the fragrance-review projection lane.

Mirrors the adjudicated cleaning catch-up suite shape (discovery finds its own
backlog; second run is a no-op; policy bump re-surfaces; failures are loud,
isolated, and never acked; unknown surfaces are visible, never acked; reconcile
failures are per-packet statuses) plus this lane's two unit-specific behaviors:
capture-date-pinned determinism and the loud missing-capture-time failure.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

import pytest

import runners.run_fragrance_review_projection_catchup as catchup
from data_lake.consumption import find_acks
from data_lake.root import DataLakeRoot, raw_shard
from harness_utils import generate_ulid
from source_capture.fragrance_rendered_widget_companion import FragranceWidgetResponseCapture
from source_capture.fragrance_review_lake import (
    PROJECTION_FRAGRANCE_REVIEW_LANE,
    capture_as_of_date,
    project_fragrance_review_into_lake,
    write_fragrance_review_capture_packet,
)

_PRODUCT_URL = "https://examplefragrance.example/products/synthetic-eau"

# Fully synthetic Yotpo-v3-shaped widget response (no captured PII on-tree),
# mirroring the lake pilot fixture.
_WIDGET_BODY = json.dumps(
    {
        "reviews": [
            {
                "id": 90001,
                "content": "Synthetic test review body for the projection catch-up fixture.",
                "score": 5,
                "created_at": "2026-05-01T00:00:00Z",
                "verified_buyer": True,
            }
        ],
        "bottomline": {"totalReview": 1, "averageScore": 5.0},
        "pagination": {"page": 1, "perPage": 10, "total": 1},
    },
    sort_keys=True,
)


def _synthetic_widget_response() -> FragranceWidgetResponseCapture:
    body = _WIDGET_BODY
    return FragranceWidgetResponseCapture(
        response_index=1,
        response_origin="render_passive",
        response_kind="yotpo_v3_reviews",
        requested_url="https://api-cdn.yotpo.com/v3/storefront/store/SYN/product/SYN/reviews",
        final_url="https://api-cdn.yotpo.com/v3/storefront/store/SYN/product/SYN/reviews",
        status=200,
        ok=True,
        body_sha256=hashlib.sha256(body.encode("utf-8")).hexdigest(),
        body_byte_count=len(body.encode("utf-8")),
        body_text=body,
    )


def _commit_packet(root: DataLakeRoot, *, source_surface: str | None = None) -> str:
    kwargs = {} if source_surface is None else {"source_surface": source_surface}
    result = write_fragrance_review_capture_packet(
        data_root=root,
        widget_responses=[_synthetic_widget_response()],
        product_url=_PRODUCT_URL,
        **kwargs,
    )
    return result.packet.packet_id


def _manifest_path(root: DataLakeRoot, packet_id: str) -> Path:
    return root.path / "raw" / raw_shard(packet_id) / packet_id / "manifest.json"


def _derived_lane_dir(root: DataLakeRoot, packet_id: str) -> Path:
    return root.lane_dir(
        subtree="derived", raw_anchor=packet_id, lane=PROJECTION_FRAGRANCE_REVIEW_LANE
    )


def _acks(root: DataLakeRoot, packet_id: str) -> list[dict]:
    return find_acks(
        root, raw_anchor=packet_id, ack_namespace=PROJECTION_FRAGRANCE_REVIEW_LANE
    )


def test_catchup_discovers_derives_and_acks(tmp_path: Path) -> None:
    # S1: the lane finds its own backlog — a committed packet nobody pointed at
    # gets its derived coverage record plus a lane-owned ack citing it.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root)

    results = catchup.run_catchup(data_root=root)

    assert [entry["status"] for entry in results] == ["derived"]
    assert results[0]["packet_id"] == pid
    derived_files = list(_derived_lane_dir(root, pid).iterdir())
    assert len(derived_files) == 1
    acks = _acks(root, pid)
    assert len(acks) == 1
    assert acks[0]["obligation"]["consumer"] == "fragrance_review_projection_catchup"


def test_second_run_is_a_no_op(tmp_path: Path) -> None:
    # S2: acked-and-unchanged packets emit no statuses and gain no new siblings.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root)
    catchup.run_catchup(data_root=root)

    second = catchup.run_catchup(data_root=root)

    assert second == []
    assert len(list(_derived_lane_dir(root, pid).iterdir())) == 1
    assert len(_acks(root, pid)) == 1


def test_policy_bump_re_surfaces_and_re_derives(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # S3: changing an enumerated policy constant changes the obligation
    # fingerprint, so an already-acked packet re-surfaces and re-derives.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root)
    catchup.run_catchup(data_root=root)

    monkeypatch.setattr(catchup, "FRAGRANCE_REVIEW_SELECTION_RECENT_MONTHS", 6)
    results = catchup.run_catchup(data_root=root)

    assert [entry["status"] for entry in results] == ["derived"]
    assert len(_acks(root, pid)) == 2
    assert len(list(_derived_lane_dir(root, pid).iterdir())) == 2


def test_check_mode_counts_pending_without_writing(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root)

    assert catchup.pending_packets(data_root=root) == [pid]
    assert not _derived_lane_dir(root, pid).is_dir()

    catchup.run_catchup(data_root=root)
    assert catchup.pending_packets(data_root=root) == []


def test_derive_failure_is_loud_isolated_and_never_acked(tmp_path: Path) -> None:
    # S4+S5: a packet whose preserved body no longer matches its manifest hash
    # fails its verified read; the failure is a visible status, the packet stays
    # unacknowledged (re-surfaces), and a healthy packet still derives.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    bad_pid = _commit_packet(root)
    good_pid = _commit_packet(root)
    container = _manifest_path(root, bad_pid).parent
    manifest = json.loads(_manifest_path(root, bad_pid).read_text(encoding="utf-8"))
    preserved_relpath = manifest["preserved_files"][0]["relative_packet_path"]
    (container / preserved_relpath).write_bytes(b"{} tampered")

    results = catchup.run_catchup(data_root=root)

    by_pid = {entry["packet_id"]: entry for entry in results}
    assert by_pid[bad_pid]["status"] == "derive_failed"
    assert by_pid[good_pid]["status"] == "derived"
    assert _acks(root, bad_pid) == []
    # still re-surfaces on the next run
    rerun = {entry["packet_id"]: entry["status"] for entry in catchup.run_catchup(data_root=root)}
    assert rerun == {bad_pid: "derive_failed"}


def test_unsupported_surface_is_visible_and_never_acked(tmp_path: Path) -> None:
    # F-FRAG-002 shape for a single-surface family: any unknown surface is a
    # visible unsupported_surface status every run — no open-world ack.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root, source_surface="mystery_future_surface")

    first = catchup.run_catchup(data_root=root)
    second = catchup.run_catchup(data_root=root)

    for results in (first, second):
        assert [entry["status"] for entry in results] == ["unsupported_surface"]
        assert results[0]["source_surface"] == "mystery_future_surface"
    assert _acks(root, pid) == []
    assert not _derived_lane_dir(root, pid).is_dir()


def test_reconcile_failure_is_per_packet_and_healthy_packets_proceed(tmp_path: Path) -> None:
    # F-ECR-001 shape: one corrupt manifest is a visible per-packet
    # availability_reconcile_failed status; healthy packets still index+derive.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    good_pid = _commit_packet(root)
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


def test_as_of_is_pinned_to_capture_date_and_recorded_in_evidence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The lane's determinism rule: as_of = the packet's own capture date,
    # resolved from the committed manifest and recorded in the ack evidence
    # (the coverage receipt does not carry it).
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root)
    manifest_path = _manifest_path(root, pid)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["source_slices"][0]["timing"]["capture_time"]["value"] = "2024-01-15T12:34:56Z"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    capture_value = manifest["source_slices"][0]["timing"]["capture_time"]["value"]
    expected_as_of = datetime.fromisoformat(capture_value.replace("Z", "+00:00")).date()

    assert capture_as_of_date(manifest) == expected_as_of

    projected_as_of_dates = []
    real_project = catchup.project_fragrance_review_into_lake

    def recording_project(*, data_root, packet_id, as_of_date=None):
        projected_as_of_dates.append(as_of_date)
        return real_project(data_root=data_root, packet_id=packet_id, as_of_date=as_of_date)

    monkeypatch.setattr(catchup, "project_fragrance_review_into_lake", recording_project)

    results = catchup.run_catchup(data_root=root)
    assert results[0]["as_of_date"] == expected_as_of.isoformat()
    assert projected_as_of_dates == [expected_as_of]

    (ack,) = _acks(root, pid)
    evidence = {entry["kind"]: entry for entry in ack["evidence"]}
    assert evidence["as_of_resolution"]["as_of_policy"] == "packet_capture_date"
    assert evidence["as_of_resolution"]["as_of_date"] == expected_as_of.isoformat()
    derived_file = _derived_lane_dir(root, pid) / evidence["derived_record"]["record_id"]
    assert (
        hashlib.sha256(derived_file.read_bytes()).hexdigest()
        == evidence["derived_record"]["content_sha256"]
    )
    assert ack["obligation"]["as_of_policy"] == "packet_capture_date"


def test_capture_pinned_derivation_is_byte_deterministic(tmp_path: Path) -> None:
    # Two derivations under the pinned as_of produce byte-identical derived
    # records (fresh sibling ids, same content) — the catch-up's output is a
    # pure function of (immutable raw, policy).
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root)
    catchup.run_catchup(data_root=root)
    (first_file,) = _derived_lane_dir(root, pid).iterdir()

    manifest = json.loads(_manifest_path(root, pid).read_text(encoding="utf-8"))
    _, second_path = project_fragrance_review_into_lake(
        data_root=root, packet_id=pid, as_of_date=capture_as_of_date(manifest)
    )

    assert second_path.name != first_file.name
    assert second_path.read_bytes() == first_file.read_bytes()


def test_missing_capture_time_is_a_loud_derive_failure(tmp_path: Path) -> None:
    # Block-don't-fake: a family packet whose capture_time is not a known fact
    # must fail loudly per-packet — never silently fall back to date.today().
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_packet(root)
    manifest_path = _manifest_path(root, pid)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["source_slices"][0]["timing"]["capture_time"] = {
        "status": "unknown_with_reason",
        "reason": "synthetic: capture time stripped for the loud-failure test",
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    results = catchup.run_catchup(data_root=root)

    assert [entry["status"] for entry in results] == ["derive_failed"]
    assert "capture" in results[0]["error"]
    assert _acks(root, pid) == []


def test_cli_requires_exactly_one_mode() -> None:
    with pytest.raises(SystemExit) as excinfo:
        catchup.main([])
    assert excinfo.value.code == 2
