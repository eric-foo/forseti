from __future__ import annotations

import ast
import json
import shutil
import uuid
from pathlib import Path

import pytest

from runners import run_reddit_old_http_batch as batch_runner
from runners.run_reddit_old_http_batch import BatchSlot, load_slots, run_reddit_old_http_batch


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"reddit_old_http_batch_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_load_slots_accepts_only_exact_old_reddit_thread_urls(scratch_dir: Path) -> None:
    path = scratch_dir / "urls.json"
    path.write_text(
        json.dumps(
            [
                {
                    "slot_id": "b2b_001",
                    "url": "https://old.reddit.com/r/SaaS/comments/abc/example/",
                },
                "https://old.reddit.com/r/SEO/comments/def/example/",
            ]
        ),
        encoding="utf-8",
    )

    slots = load_slots(path)

    assert slots == [
        BatchSlot(slot_id="b2b_001", url="https://old.reddit.com/r/SaaS/comments/abc/example/"),
        BatchSlot(slot_id="slot_002", url="https://old.reddit.com/r/SEO/comments/def/example/"),
    ]


def test_load_slots_rejects_new_reddit_and_non_thread_urls(scratch_dir: Path) -> None:
    path = scratch_dir / "urls.json"
    path.write_text(
        json.dumps(["https://www.reddit.com/r/SaaS/comments/abc/example/"]),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="old.reddit.com"):
        load_slots(path)

    path.write_text(json.dumps(["https://old.reddit.com/r/SaaS/"]), encoding="utf-8")
    with pytest.raises(ValueError, match="/comments/"):
        load_slots(path)


def test_batch_runner_captures_consolidates_and_sleeps_between_exact_urls(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, object]] = []

    def fake_capture(**kwargs: object) -> tuple[int, str]:
        calls.append(("capture", kwargs))
        Path(kwargs["output_directory"]).mkdir(parents=True)
        return 0, str(kwargs["output_directory"])

    def fake_consolidate(**kwargs: object) -> dict[str, str]:
        calls.append(("consolidate", kwargs))
        Path(kwargs["output_directory"]).mkdir(parents=True)
        return {
            "json_path": str(Path(kwargs["output_directory"]) / "reddit_thread_consolidation.json"),
            "receipt_path": str(Path(kwargs["output_directory"]) / "reddit_thread_consolidation_receipt.md"),
            "comment_count": "2",
            "observable_comment_node_count": "2",
        }

    def fake_sleep(seconds: float) -> None:
        calls.append(("sleep", seconds))

    monkeypatch.setattr(batch_runner, "run_source_capture_http_packet", fake_capture)
    monkeypatch.setattr(batch_runner, "consolidate_reddit_packet", fake_consolidate)
    monkeypatch.setattr(batch_runner.time, "sleep", fake_sleep)

    exit_code, message = run_reddit_old_http_batch(
        slots=[
            BatchSlot("slot_a", "https://old.reddit.com/r/SaaS/comments/abc/example/"),
            BatchSlot("slot_b", "https://old.reddit.com/r/SEO/comments/def/example/"),
        ],
        output_root=scratch_dir / "batch",
        decision_question="Can exact old Reddit URLs batch cleanly?",
        delay_seconds=0.25,
        max_urls=2,
        timeout_seconds=7,
        max_bytes=1234,
    )

    assert exit_code == 0
    summary_path = Path(message)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["url_count"] == 2
    assert summary["capture_success_count"] == 2
    assert summary["consolidation_success_count"] == 2
    assert summary["delay_seconds"] == 0.25
    assert summary["cadence"] == {
        "mode": "fixed",
        "slot_count": 2,
        "planned_offsets_seconds": [0.0, 0.25],
        "planned_waits_seconds": [0.25],
        "delay_seconds": 0.25,
        "window_seconds": None,
        "min_gap_seconds": None,
        "max_gap_seconds": None,
        "random_seed": None,
    }
    assert summary["non_claims"] == [
        "not crawler",
        "not source discovery",
        "not monitoring",
        "not proxy use",
        "not browser automation",
        "not retry escalation",
        "not broad Reddit crawl",
    ]
    assert [call[0] for call in calls] == [
        "capture",
        "consolidate",
        "sleep",
        "capture",
        "consolidate",
    ]
    first_capture = calls[0][1]
    assert isinstance(first_capture, dict)
    assert first_capture["source_surface"] == "old_reddit_direct_http"
    assert first_capture["timeout_seconds"] == 7
    assert first_capture["max_bytes"] == 1234
    assert summary["results"][0]["planned_start_offset_seconds"] == 0.0
    assert summary["results"][0]["planned_wait_after_seconds"] == 0.25
    assert summary["results"][0]["capture_started_at"].endswith("Z")
    assert summary["results"][0]["capture_finished_at"].endswith("Z")
    assert "no proxy, browser, crawler, retry, or link following" in first_capture[
        "capture_context"
    ]


def test_batch_runner_bounded_jitter_records_budgeted_cadence(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, object]] = []

    def fake_capture(**kwargs: object) -> tuple[int, str]:
        calls.append(("capture", kwargs))
        Path(kwargs["output_directory"]).mkdir(parents=True)
        return 0, str(kwargs["output_directory"])

    def fake_consolidate(**kwargs: object) -> dict[str, str]:
        calls.append(("consolidate", kwargs))
        Path(kwargs["output_directory"]).mkdir(parents=True)
        return {
            "json_path": str(Path(kwargs["output_directory"]) / "reddit_thread_consolidation.json"),
            "receipt_path": str(Path(kwargs["output_directory"]) / "reddit_thread_consolidation_receipt.md"),
            "comment_count": "2",
            "observable_comment_node_count": "2",
        }

    def fake_sleep(seconds: float) -> None:
        calls.append(("sleep", seconds))

    monkeypatch.setattr(batch_runner, "run_source_capture_http_packet", fake_capture)
    monkeypatch.setattr(batch_runner, "consolidate_reddit_packet", fake_consolidate)
    monkeypatch.setattr(batch_runner.time, "sleep", fake_sleep)

    _, message = run_reddit_old_http_batch(
        slots=[
            BatchSlot("slot_a", "https://old.reddit.com/r/SaaS/comments/abc/example/"),
            BatchSlot("slot_b", "https://old.reddit.com/r/SEO/comments/def/example/"),
            BatchSlot("slot_c", "https://old.reddit.com/r/founder/comments/ghi/example/"),
        ],
        output_root=scratch_dir / "batch",
        decision_question="Can exact old Reddit URLs batch with bounded jitter?",
        delay_seconds=999,
        max_urls=3,
        cadence_mode="bounded_jitter",
        cadence_window_seconds=9,
        cadence_min_gap_seconds=1,
        cadence_max_gap_seconds=4,
        cadence_random_seed=1234,
    )

    summary = json.loads(Path(message).read_text(encoding="utf-8"))
    assert summary["delay_seconds"] is None
    cadence = summary["cadence"]
    assert cadence["mode"] == "bounded_jitter"
    assert cadence["slot_count"] == 3
    assert cadence["window_seconds"] == 9
    assert cadence["min_gap_seconds"] == 1
    assert cadence["max_gap_seconds"] == 4
    assert cadence["random_seed"] == 1234
    assert cadence["delay_seconds"] is None
    waits = cadence["planned_waits_seconds"]
    assert len(waits) == 2
    assert all(1 <= wait <= 4 for wait in waits)
    assert sum(waits) <= 9
    assert [call for call in calls if call[0] == "sleep"] == [
        ("sleep", waits[0]),
        ("sleep", waits[1]),
    ]
    assert summary["results"][1]["planned_start_offset_seconds"] == waits[0]
    assert summary["results"][2]["planned_start_offset_seconds"] == round(sum(waits), 3)
    assert summary["results"][2]["planned_wait_after_seconds"] is None


def test_batch_runner_records_failures_without_retry_or_consolidation(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []

    def fake_capture(**kwargs: object) -> tuple[int, str]:
        calls.append("capture")
        return 3, "direct HTTP failed visibly"

    def fake_consolidate(**kwargs: object) -> dict[str, str]:
        calls.append("consolidate")
        return {}

    monkeypatch.setattr(batch_runner, "run_source_capture_http_packet", fake_capture)
    monkeypatch.setattr(batch_runner, "consolidate_reddit_packet", fake_consolidate)

    _, message = run_reddit_old_http_batch(
        slots=[BatchSlot("slot_a", "https://old.reddit.com/r/SaaS/comments/abc/example/")],
        output_root=scratch_dir / "batch",
        decision_question="Can failures stay loud?",
        delay_seconds=0,
    )

    summary = json.loads(Path(message).read_text(encoding="utf-8"))
    assert calls == ["capture"]
    assert summary["capture_success_count"] == 0
    assert summary["consolidation_success_count"] == 0
    assert summary["results"][0]["capture_exit"] == 3
    assert summary["results"][0]["consolidation_exit"] is None
    assert summary["results"][0]["retry_count"] == 0


def test_batch_runner_enforces_max_urls(scratch_dir: Path) -> None:
    with pytest.raises(ValueError, match="above max_urls=1"):
        run_reddit_old_http_batch(
            slots=[
                BatchSlot("slot_a", "https://old.reddit.com/r/SaaS/comments/abc/example/"),
                BatchSlot("slot_b", "https://old.reddit.com/r/SEO/comments/def/example/"),
            ],
            output_root=scratch_dir / "batch",
            decision_question="Can max URL cap stop the batch?",
            max_urls=1,
        )


def test_batch_runner_rejects_impossible_bounded_jitter_before_output(
    scratch_dir: Path,
) -> None:
    output_root = scratch_dir / "batch"
    with pytest.raises(ValueError, match="cadence window cannot fit"):
        run_reddit_old_http_batch(
            slots=[
                BatchSlot("slot_a", "https://old.reddit.com/r/SaaS/comments/abc/example/"),
                BatchSlot("slot_b", "https://old.reddit.com/r/SEO/comments/def/example/"),
                BatchSlot("slot_c", "https://old.reddit.com/r/founder/comments/ghi/example/"),
            ],
            output_root=output_root,
            decision_question="Does impossible cadence fail before output?",
            cadence_mode="bounded_jitter",
            cadence_window_seconds=5,
            cadence_min_gap_seconds=3,
            cadence_max_gap_seconds=4,
        )

    assert not output_root.exists()


def test_batch_runner_enforces_old_reddit_host_bound_for_directly_built_slots(
    scratch_dir: Path,
) -> None:
    # The host bound must hold at the runner boundary, not only in load_slots:
    # a caller that builds BatchSlot directly must not reach capture with a
    # non-old.reddit.com URL. Validation must fail before any output is written.
    output_root = scratch_dir / "batch"
    with pytest.raises(ValueError, match="old.reddit.com"):
        run_reddit_old_http_batch(
            slots=[BatchSlot("slot_a", "https://www.reddit.com/r/SaaS/comments/abc/example/")],
            output_root=output_root,
            decision_question="Does the runner enforce the host bound itself?",
            delay_seconds=0,
        )

    assert not output_root.exists()


def test_batch_runner_rejects_path_traversal_slot_id_for_directly_built_slots(
    scratch_dir: Path,
) -> None:
    # slot_id is interpolated into per-slot directory names; a path-traversal
    # slot_id must be rejected at the runner boundary before any directory is
    # created or any capture is attempted.
    output_root = scratch_dir / "batch"
    with pytest.raises(ValueError, match="slot_id"):
        run_reddit_old_http_batch(
            slots=[
                BatchSlot("../escape", "https://old.reddit.com/r/SaaS/comments/abc/example/")
            ],
            output_root=output_root,
            decision_question="Does the runner reject path-traversal slot ids?",
            delay_seconds=0,
        )

    assert not output_root.exists()


NETWORK_BROWSER_PROXY_ROOTS = {
    "aiohttp",
    "archivebox",
    "cloakbrowser",
    "httpx",
    "patchright",
    "playwright",
    "praw",
    "requests",
    "scrapy",
    "selenium",
    "socket",
    "webbrowser",
}


def _classify_forbidden_import(dotted: str) -> set[str]:
    parts = dotted.split(".")
    if parts[0] in NETWORK_BROWSER_PROXY_ROOTS:
        return {dotted}
    # urllib.parse is pure URL parsing and is allowed; any other urllib
    # submodule (request, error, ...) is network-capable and forbidden here,
    # because the batch runner must delegate all fetching to the bounded
    # direct-HTTP runner rather than open connections itself.
    if parts[0] == "urllib" and parts[:2] != ["urllib", "parse"]:
        return {dotted}
    return set()


def _batch_runner_forbidden_imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    offenders: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                offenders |= _classify_forbidden_import(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            offenders |= _classify_forbidden_import(node.module)
    return offenders


def test_batch_runner_has_no_hidden_network_browser_or_proxy_imports() -> None:
    runner_path = Path(batch_runner.__file__)
    assert _batch_runner_forbidden_imports(runner_path) == set()
