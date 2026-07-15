"""Unit tests for the creator-metric rollup PRODUCER runner -- the lake-population
step that deposits the records the snapshot runner consumes.

The core (``run_producer``) is exercised against a temp lake (real raw-commit +
real producer). There is intentionally NO real-lake ``main`` test: the producer
is append-only, so running it against the live lake would deposit durable records
-- not something a test may do. ``main``'s only extra surface over the tested core
is ``DataLakeRoot.resolve`` (covered by the lake's own tests) and ledger loading
(covered here).
"""
from __future__ import annotations

import json
from pathlib import Path

from capture_spine.creator_profile_current.silver_metric_reader import (
    discover_creator_metric_rollup_records,
)
from data_lake.root import DataLakeRoot
from runners.run_creator_metric_rollup_producer import _load_account_ledger, run_producer
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet

IG_ACCOUNT = "acct_ig_reels_001"
IG_HANDLE = "hyram"
TS = "2026-06-30T00:02:00Z"


def _ledger() -> dict:
    return {
        "platform_accounts": [
            {
                "platform_account_id": IG_ACCOUNT,
                "platform": "instagram",
                "public_handle": IG_HANDLE,
                "public_profile_url": f"https://www.instagram.com/{IG_HANDLE}/",
                "handle_source_pointer": "fixture#/rows/0",
                "handle_observed_at": "2026-06-29T00:00:00Z",
            }
        ]
    }


def _projection_rows(packet_id: str, raw_anchor: dict) -> list[dict]:
    cap = "2026-06-29T00:01:00Z"

    def reel(sc: str, metric: str, val: int) -> dict:
        return {
            "row_id": f"{packet_id}:{sc}:{metric}", "row_kind": "ig_media_metric", "username": IG_HANDLE,
            "content_kind": "reel", "content_shortcode": sc, "content_url": f"https://www.instagram.com/{IG_HANDLE}/reel/{sc}/",
            "metric": metric, "posture": "observed", "value": val, "reason": None, "capture_time": cap,
            "coverage_window": {"start": None, "end": cap}, "raw_ref": {"packet_id": packet_id, "slice_id": "ig_reels_grid_01"},
            "raw_anchor": raw_anchor, "chosen_source_surface": "clips_user_json_metadata",
            "source_surface_count_candidates": [], "source_publication_or_event": cap,
        }

    rows = [{
        "row_id": f"{packet_id}:profile:follower_count", "row_kind": "ig_creator_metric", "username": IG_HANDLE,
        "content_kind": "profile", "content_shortcode": None, "content_url": None, "metric": "follower_count",
        "posture": "observed", "value": 1000, "reason": None, "capture_time": cap,
        "coverage_window": {"start": None, "end": cap}, "raw_ref": {"packet_id": packet_id, "slice_id": "ig_reels_profile_00"},
        "raw_anchor": raw_anchor, "chosen_source_surface": "web_profile_info_json_metadata",
        "source_surface_count_candidates": [], "source_publication_or_event": None,
    }]
    for sc, v, l, c in (("AAA", 100, 10, 5), ("BBB", 300, 30, 15)):
        rows += [reel(sc, "view_count", v), reel(sc, "like_count", l), reel(sc, "comment_count", c)]
    return rows


def _raw_projection(data_root: DataLakeRoot, tmp_path: Path) -> Path:
    raw = tmp_path / "ig_raw.json"
    raw.write_text(json.dumps({"grid": "x"}), encoding="utf-8")
    capture = write_local_source_capture_packet(
        data_root=data_root,
        input_files=[raw],
        source_family="instagram_creator",
        source_surface="ig_reels_grid",
        source_locator=known_fact(f"https://www.instagram.com/{IG_HANDLE}/"),
        decision_question="producer runner",
        capture_context="producer runner test",
    )
    packet_id = capture.packet.packet_id
    preserved = data_root.load_raw_packet(packet_id).manifest["preserved_files"][0]
    raw_anchor = {
        key: preserved[key]
        for key in ("file_id", "relative_packet_path", "sha256", "hash_basis")
    }
    projection = tmp_path / "ig_projection.json"
    projection.write_text(
        json.dumps(
            {
                "packet_id": packet_id,
                "rows": _projection_rows(packet_id, raw_anchor),
            }
        ),
        encoding="utf-8",
    )
    return projection


def test_run_producer_appends_discoverable_rollup(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    projection = _raw_projection(data_root, tmp_path)

    result = run_producer(
        data_root, projection_paths=[projection], account_ledger=_ledger(), generated_at_utc=TS
    )

    assert len(result.rollup_records) == 1
    assert result.rollup_paths and result.rollup_paths[0].is_file()
    # the deposited rollup is exactly what the snapshot runner's discovery finds
    found = discover_creator_metric_rollup_records(
        data_root,
        account_ledger={"platform_accounts": [{"platform_account_id": IG_ACCOUNT, "platform": "instagram", "public_handle": IG_ACCOUNT}]},
    )
    assert set(found) == {IG_ACCOUNT}
    assert len(found[IG_ACCOUNT]) == 1


def test_load_account_ledger_unwraps_committed_shape(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.json"
    ledger.write_text(
        json.dumps({"creator_public_handle_linkage_ledger": {"platform_accounts": [{"platform_account_id": "x"}]}}),
        encoding="utf-8",
    )
    assert _load_account_ledger(ledger) == {"platform_accounts": [{"platform_account_id": "x"}]}
