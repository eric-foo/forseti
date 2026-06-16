"""Tests for the operator-triggered demand-durability series runner (capture-spine step 3).

These exercise the runner end-to-end against a local stdlib HTTP server (the same fixture
shape as ``test_source_capture_direct_http.py``), so the step-2 durability writer is invoked
for real per slot and writes real ``SourceCapturePacket``s -- no live network, no real SKU.

Coverage maps to the step-3 brief:
- the declared cadence is honored (slots run per the plan's offsets/slot_count);
- a gap is recorded as ``un_observed`` -- NEVER "no change";
- the series is bounded to ``slot_count`` (a slot beyond it is rejected);
- INV-1: the runner records facts + limits, never a score/rank/weight/verdict.
"""

from __future__ import annotations

import json
import shutil
import threading
import uuid
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from runners.run_source_capture_durability_series import (
    SERIES_INDEX_FILENAME,
    SERIES_RUNNER_NON_CLAIMS,
    SLOT_OBSERVED,
    SLOT_PENDING,
    SLOT_UN_OBSERVED,
    build_series_index,
    main as series_main,
    run_slot,
    series_status,
)


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"durability_series_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


@dataclass(frozen=True)
class _RouteResponse:
    status: int
    body: bytes
    headers: dict[str, str]


@pytest.fixture
def http_server():
    routes = {
        "/sku": _RouteResponse(
            status=200,
            body=b"<html>price: $44.00 in_stock</html>\n",
            headers={"Content-Type": "text/html; charset=utf-8"},
        ),
    }

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            route = routes.get(self.path)
            if route is None:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"unexpected path")
                return
            self.send_response(route.status)
            for key, value in route.headers.items():
                self.send_header(key, value)
            self.end_headers()
            if route.body:
                self.wfile.write(route.body)

        def log_message(self, format: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def _init_series(
    *,
    series_dir: Path,
    url: str,
    slot_count: int = 3,
    delay_seconds: float = 86400.0,
    anchor_time: str = "2026-06-15T00:00:00Z",
) -> int:
    return series_main(
        [
            "init",
            "--series-dir",
            str(series_dir),
            "--series-id",
            "test_series_001",
            "--decision-frame-ref",
            "DF-test-001",
            "--decision-question",
            "Is demand for this SKU durable across the series window?",
            "--url",
            url,
            "--anchor-time",
            anchor_time,
            "--cadence-mode",
            "fixed",
            "--slot-count",
            str(slot_count),
            "--cadence-delay-seconds",
            str(delay_seconds),
            "--session-visibility-pin",
            "logged_out_public",
            "--locale-pin",
            "en-US",
            "--currency-pin",
            "USD",
            "--variant-pin-unknown-reason",
            "default on-page variant; not pinned to a specific SKU id",
            "--cold-start-at",
            anchor_time,
            "--pre-coverage-history-posture",
            "uncovered by construction; series began at first commissioned capture",
        ]
    )


def test_init_builds_bounded_series_with_declared_cadence(http_server: str, scratch_dir: Path) -> None:
    # The declared cadence is honored: the series index carries the canonical CadencePlan shape
    # and one slot per planned offset, bounded to slot_count. No score/verdict (INV-1).
    series_dir = scratch_dir / "series"
    assert _init_series(series_dir=series_dir, url=f"{http_server}/sku", slot_count=3) == 0

    index = json.loads((series_dir / SERIES_INDEX_FILENAME).read_text(encoding="utf-8"))
    assert index["series_id"] == "test_series_001"
    assert index["decision_frame_ref"] == "DF-test-001"
    assert index["slot_count"] == 3
    # Cadence is the canonical CadencePlan.to_dict() shape (reused primitive; no invented shape).
    assert index["intended_cadence"]["mode"] == "fixed"
    assert index["intended_cadence"]["slot_count"] == 3
    assert index["intended_cadence"]["planned_offsets_seconds"] == [0.0, 86400.0, 172800.0]
    # One slot per planned offset; intended slot times = anchor + offset; all pending at init.
    assert [slot["slot_index"] for slot in index["slots"]] == [0, 1, 2]
    assert [slot["intended_slot_time"] for slot in index["slots"]] == [
        "2026-06-15T00:00:00Z",
        "2026-06-16T00:00:00Z",
        "2026-06-17T00:00:00Z",
    ]
    assert all(slot["status"] == SLOT_PENDING for slot in index["slots"])
    # INV-1: the substantive index (spec + slots, excluding the non-claims disclaimer that
    # NAMES score/verdict only to deny them) carries no score/rank/weight/verdict -- it is
    # cadence + identity + slot bookkeeping only.
    substantive = {key: value for key, value in index.items() if key != "non_claims"}
    blob = json.dumps(substantive).lower()
    for forbidden in ("score", "rank", "weight", "verdict"):
        assert forbidden not in blob
    # The runner explicitly disclaims the gap != no-change confusion in its non-claims.
    assert "a gap is recorded as un-observed, never as no-change" in index["non_claims"]


def test_run_slot_observes_and_records_realized_capture_time(http_server: str, scratch_dir: Path) -> None:
    # Running a slot invokes the step-2 writer, writes a real packet, and records the realized
    # capture_time vs the intended slot time. The first observed slot is the cold start.
    series_dir = scratch_dir / "series"
    _init_series(series_dir=series_dir, url=f"{http_server}/sku", slot_count=3)

    status, slot = run_slot(series_dir=series_dir, slot_index=0, now_z="2026-06-15T00:00:05Z")
    assert status == SLOT_OBSERVED
    assert slot["was_cold_start"] is True
    observation = slot["observations"][0]
    # A real packet was written and its capture_time recorded as the realized timing.
    packet_dir = series_dir / observation["packet_dir"]
    manifest = json.loads((packet_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["series_id"] == "test_series_001"
    assert manifest["intended_cadence"]["slot_count"] == 3
    # Element-2 cold-start postures rode onto the FIRST observed slot only.
    assert manifest["cold_start_at"]["value"] == "2026-06-15T00:00:00Z"
    assert observation["realized_capture_time"] == manifest["timing"]["capture_time"]["value"]
    assert "lateness_seconds" in observation

    # The SECOND observed slot is NOT a cold start (postures do not repeat).
    status2, slot2 = run_slot(series_dir=series_dir, slot_index=1, now_z="2026-06-16T00:00:00Z")
    assert status2 == SLOT_OBSERVED
    assert slot2["was_cold_start"] is False
    packet_dir2 = series_dir / slot2["observations"][0]["packet_dir"]
    manifest2 = json.loads((packet_dir2 / "manifest.json").read_text(encoding="utf-8"))
    assert manifest2["cold_start_at"] is None


def test_mark_gap_records_un_observed_never_no_change(http_server: str, scratch_dir: Path) -> None:
    # The load-bearing invariant: a slot the operator did not sample is un_observed (a visible
    # limitation), NEVER "no change". The recorded fact must say un_observed and carry a reason.
    series_dir = scratch_dir / "series"
    _init_series(series_dir=series_dir, url=f"{http_server}/sku", slot_count=3)

    rc = series_main(
        [
            "mark-gap",
            "--series-dir",
            str(series_dir),
            "--slot",
            "1",
            "--reason",
            "operator unavailable for this slot",
        ]
    )
    assert rc == 0
    index = json.loads((series_dir / SERIES_INDEX_FILENAME).read_text(encoding="utf-8"))
    gap_slot = index["slots"][1]
    assert gap_slot["status"] == SLOT_UN_OBSERVED
    assert gap_slot["gap_kind"] == "skipped"
    assert gap_slot["gap_reason"] == "operator unavailable for this slot"
    # The gap is NEVER expressed as a no-change fact.
    assert "no_change" not in json.dumps(gap_slot).lower()
    assert "no change" not in json.dumps(gap_slot).lower()


def test_run_slot_failed_fetch_records_un_observed_gap_not_no_change(scratch_dir: Path) -> None:
    # A failed fetch (writer non-zero exit) is recorded as an un_observed GAP, never no-change.
    # Use a URL that cannot connect so the step-2 writer returns a non-zero exit for real.
    series_dir = scratch_dir / "series"
    # Port 9 (discard) refuses; the direct_http adapter returns a network failure -> writer exit 3.
    _init_series(series_dir=series_dir, url="http://127.0.0.1:9/unreachable", slot_count=2)

    status, slot = run_slot(series_dir=series_dir, slot_index=0, now_z="2026-06-15T00:00:00Z")
    assert status == SLOT_UN_OBSERVED
    assert slot["gap_kind"] == "fetch_failed"
    assert "writer exit" in slot["gap_reason"]
    assert "no_change" not in json.dumps(slot).lower()
    assert "no change" not in json.dumps(slot).lower()


def test_series_is_bounded_to_slot_count(http_server: str, scratch_dir: Path) -> None:
    # The series is a bounded commissioned unit (Ob.1), not an open crawler: a slot index at or
    # beyond slot_count is rejected -- the runner cannot run unbounded slots.
    series_dir = scratch_dir / "series"
    _init_series(series_dir=series_dir, url=f"{http_server}/sku", slot_count=3)

    # Slot 3 is out of bounds for a 3-slot series (valid: 0..2).
    with pytest.raises(ValueError, match="out of bounds"):
        run_slot(series_dir=series_dir, slot_index=3, now_z="2026-06-15T00:00:00Z")

    # Via the CLI the out-of-bounds attempt exits non-zero (SystemExit from parser.exit).
    with pytest.raises(SystemExit) as exc_info:
        series_main(["run-slot", "--series-dir", str(series_dir), "--slot", "3"])
    assert exc_info.value.code == 2


def test_status_summarizes_observed_un_observed_pending_as_facts(http_server: str, scratch_dir: Path) -> None:
    # status reports counts of observed / un_observed / pending only -- facts, no verdict (INV-1).
    series_dir = scratch_dir / "series"
    _init_series(series_dir=series_dir, url=f"{http_server}/sku", slot_count=3)

    run_slot(series_dir=series_dir, slot_index=0, now_z="2026-06-15T00:00:00Z")
    series_main(["mark-gap", "--series-dir", str(series_dir), "--slot", "1", "--reason", "skipped"])

    summary = series_status(series_dir)
    assert summary["slot_count"] == 3
    assert summary["observed"] == 1
    assert summary["un_observed"] == 1
    assert summary["pending"] == 1
    assert summary["complete"] is False
    # INV-1: the summary is counts + identity only; no score/rank/weight/verdict key.
    for forbidden in ("score", "rank", "weight", "verdict"):
        assert forbidden not in json.dumps(summary).lower()


def test_build_series_index_requires_at_least_one_url() -> None:
    with pytest.raises(ValueError, match="at least one source URL"):
        build_series_index(
            series_id="s",
            urls=[],
            decision_frame_ref="DF",
            decision_question="q",
            cadence_mode="fixed",
            slot_count=1,
            delay_seconds=0.0,
        )


def test_init_refuses_to_overwrite_existing_series(http_server: str, scratch_dir: Path) -> None:
    # Re-initializing an existing series dir is refused (the series state is durable across the
    # separate operator invocations; init must not clobber recorded slots).
    series_dir = scratch_dir / "series"
    assert _init_series(series_dir=series_dir, url=f"{http_server}/sku") == 0
    with pytest.raises(SystemExit) as exc_info:
        _init_series(series_dir=series_dir, url=f"{http_server}/sku")
    assert exc_info.value.code == 2


def test_runner_non_claims_assert_no_scheduler_no_crawler_no_diff() -> None:
    # The runner's non-claims pin option A (operator-triggered, not a scheduler/cron), the
    # commissioned-bounded model (not an open crawler), and the deferred series-diff.
    blob = " ".join(SERIES_RUNNER_NON_CLAIMS).lower()
    assert "not a scheduler" in blob
    assert "not an open crawler" in blob
    assert "not series-diff" in blob
    assert "not a demand verdict" in blob
