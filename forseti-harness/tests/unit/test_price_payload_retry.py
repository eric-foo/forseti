"""Retry + loud-fail-evidence tests for the rung-1.5 runner (degraded-page handling).

A degraded server variant serves a thin module-preload list (the prices chunk
absent); the runner retries the page, and on all-K miss must loud-fail with
per-attempt evidence preserved -- never a silent empty feed.
"""
import json
import types

import runners.run_source_capture_price_payload_packet as runner


def test_retry_exhaustion_loud_fails_and_preserves_evidence(tmp_path, monkeypatch):
    # Every attempt yields a thin page (no module-preload chunks) -> all-K miss ->
    # exit 3, with per-attempt evidence written to rung15_capture_failure.json.
    fake = types.SimpleNamespace(
        body=b"<html>thin</html>", final_url="https://x/pricing/", status=200
    )
    monkeypatch.setattr(runner, "_rung1_fetch", lambda url, **k: (fake, None))
    monkeypatch.setattr(runner, "_chunk_urls", lambda html, base: [])

    code, _msg = runner.run_price_payload_capture(
        page_url="https://x/pricing/",
        announcement_url=None,
        currency="usd",
        output_directory=tmp_path,
        decision_question="q",
        capture_context="c",
        operator_category="o",
        session_id=None,
        timeout_seconds=5,
        max_chunks=20,
        chunk_byte_budget=1000,
        max_page_attempts=2,
        page_retry_backoff_seconds=0,
    )

    assert code == 3
    art = tmp_path / "rung15_capture_failure.json"
    assert art.exists(), "a loud failure must preserve per-attempt evidence"
    rec = json.loads(art.read_text(encoding="utf-8"))
    assert rec["outcome"] == "discovery_miss_all_attempts"
    assert len(rec["attempts"]) == 2
    assert all(a["failure_class"] == "parser_no_chunks" for a in rec["attempts"])


def test_full_page_anchor_miss_fails_immediately_without_retry(tmp_path, monkeypatch):
    # A FULL page (>= floor module-preload chunks) missing the prices anchor is a
    # likely vendor change, not a transient degraded page: fail loud on attempt 0,
    # do NOT retry to K (which would make a real break look like a transient cluster).
    fake = types.SimpleNamespace(
        body=b"<html>full</html>", final_url="https://x/pricing/", status=200
    )
    monkeypatch.setattr(runner, "_rung1_fetch", lambda url, **k: (fake, None))
    monkeypatch.setattr(runner, "_chunk_urls", lambda html, base: [f"u{i}" for i in range(20)])
    monkeypatch.setattr(
        runner, "_discover_prices_chunk",
        lambda urls, **k: (None, None, None, [], "anchor_not_found"),
    )

    code, _msg = runner.run_price_payload_capture(
        page_url="https://x/pricing/",
        announcement_url=None,
        currency="usd",
        output_directory=tmp_path,
        decision_question="q",
        capture_context="c",
        operator_category="o",
        session_id=None,
        timeout_seconds=5,
        max_chunks=20,
        chunk_byte_budget=1000,
        max_page_attempts=3,
        page_retry_backoff_seconds=0,
    )

    assert code == 3
    rec = json.loads((tmp_path / "rung15_capture_failure.json").read_text(encoding="utf-8"))
    assert len(rec["attempts"]) == 1  # failed immediately; did NOT retry to K=3
    assert rec["attempts"][0]["failure_class"] == "anchor_not_found_full_page"
