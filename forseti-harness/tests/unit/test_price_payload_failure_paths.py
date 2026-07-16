"""Characterization pins for the rung-1.5 runner's four previously-untested
failure classes: page_fetch_failed, byte_budget_exceeded, max_chunks_exhausted,
anchor_not_found_thin_page.

These tests PIN CURRENT BEHAVIOR as observed on 2026-07-17 -- they are the
safety net for structural refactors, not a spec of ideal behavior. Rules for
future maintainers:

- DO NOT "fix" a behavior these tests pin as part of a refactor or cleanup. A
  deliberate behavior change must be its own authorized change that consciously
  updates the pin and says so.
- DO NOT make byte_budget_exceeded or max_chunks_exhausted retryable to
  "improve resilience": they are terminal BY DESIGN. Retrying them would mask a
  likely vendor change (or coverage limit) as a transient degraded-page
  cluster, defeating the loud-failure diagnosis contract in
  rung15_capture_failure.json.
- DO NOT reorder the anchor check after the byte-budget check in discovery: a
  chunk that exceeds the budget but CARRIES the prices anchor is a hit today.
- DO keep the retryable set exactly {page_fetch_failed, parser_no_chunks,
  anchor_not_found_thin_page}: transient classes that heal on re-fetch.
- DO keep failure-path evidence: every all-attempts miss in output-directory
  mode writes per-attempt records; data-lake mode writes nothing before a
  complete packet exists (asserted below).

Also pins the success-path packet wiring (previously untested end-to-end):
exit code 0/4 selection from the certification verdict, the staged artifact
set, and the certified-vs-uncertified limitation/mode-change surface handed
to stage_and_write_packet.
"""
import json
import types

import runners.run_source_capture_price_payload_packet as runner
from source_capture.adapters import AntiBlockingHttpCaptureFailure
from source_capture.adapters.anti_blocking_http import (
    AntiBlockingHttpCaptureFailureKind,
)


def _run(tmp_path, *, max_page_attempts=3, output_directory="dir", data_root=None):
    kwargs = dict(
        page_url="https://x/pricing/",
        announcement_url=None,
        currency="usd",
        decision_question="q",
        capture_context="c",
        operator_category="o",
        session_id=None,
        timeout_seconds=5,
        max_chunks=20,
        chunk_byte_budget=1000,
        max_page_attempts=max_page_attempts,
        page_retry_backoff_seconds=0,
    )
    if output_directory == "dir":
        kwargs["output_directory"] = tmp_path
    kwargs["data_root"] = data_root
    return runner.run_price_payload_capture(**kwargs)


def _fetch_failure(msg="connection refused"):
    return AntiBlockingHttpCaptureFailure(
        requested_url="https://x/pricing/",
        failure_kind=AntiBlockingHttpCaptureFailureKind.NETWORK_ERROR,
        message=msg,
        impersonation_profile="test_profile",
    )


def test_page_fetch_failed_retries_to_exhaustion_and_preserves_detail(
    tmp_path, monkeypatch
):
    # A page-level fetch failure is transient -> retried to all K attempts; the
    # attempt record carries only {attempt, failure_class, detail} (no status,
    # sha256, or byte_count -- there is no body to describe).
    monkeypatch.setattr(runner, "_rung1_fetch", lambda url, **k: (_fetch_failure(), None))

    code, msg = _run(tmp_path, max_page_attempts=2)

    assert code == 3
    assert "last failure_class=page_fetch_failed" in msg
    rec = json.loads((tmp_path / "rung15_capture_failure.json").read_text(encoding="utf-8"))
    assert rec["outcome"] == "discovery_miss_all_attempts"
    assert len(rec["attempts"]) == 2
    for i, attempt in enumerate(rec["attempts"]):
        assert attempt["attempt"] == i
        assert attempt["failure_class"] == "page_fetch_failed"
        assert attempt["detail"] == "connection refused"
        assert "status" not in attempt
        assert "body_sha256" not in attempt


def test_byte_budget_exceeded_is_terminal_and_preserves_scan_log(
    tmp_path, monkeypatch
):
    # A byte-budget stop is NOT transient: fail loud on attempt 0 (no retry to
    # K=3), and the per-chunk scan log survives into the attempt record.
    fake = types.SimpleNamespace(
        body=b"<html>full</html>", final_url="https://x/pricing/", status=200
    )
    scan_log = [{"url": "u0", "status": 200, "bytes": 2000,
                 "block_shell": None, "has_prices_anchor": False}]
    monkeypatch.setattr(runner, "_rung1_fetch", lambda url, **k: (fake, None))
    monkeypatch.setattr(runner, "_chunk_urls", lambda html, base: [f"u{i}" for i in range(20)])
    monkeypatch.setattr(
        runner, "_discover_prices_chunk",
        lambda urls, **k: (None, None, None, scan_log, "byte_budget_exceeded"),
    )

    code, msg = _run(tmp_path, max_page_attempts=3)

    assert code == 3
    assert "last failure_class=byte_budget_exceeded" in msg
    rec = json.loads((tmp_path / "rung15_capture_failure.json").read_text(encoding="utf-8"))
    assert len(rec["attempts"]) == 1  # terminal: did NOT retry
    assert rec["attempts"][0]["failure_class"] == "byte_budget_exceeded"
    assert rec["attempts"][0]["scan_log"] == scan_log
    assert rec["attempts"][0]["module_preload_count"] == 20


def test_max_chunks_exhausted_is_terminal_no_retry(tmp_path, monkeypatch):
    # Stopping at the max_chunks scan limit is a coverage limit, not a transient
    # miss: fail loud on attempt 0 without retrying.
    fake = types.SimpleNamespace(
        body=b"<html>full</html>", final_url="https://x/pricing/", status=200
    )
    monkeypatch.setattr(runner, "_rung1_fetch", lambda url, **k: (fake, None))
    monkeypatch.setattr(runner, "_chunk_urls", lambda html, base: [f"u{i}" for i in range(30)])
    monkeypatch.setattr(
        runner, "_discover_prices_chunk",
        lambda urls, **k: (None, None, None, [], "max_chunks_exhausted"),
    )

    code, msg = _run(tmp_path, max_page_attempts=3)

    assert code == 3
    assert "last failure_class=max_chunks_exhausted" in msg
    rec = json.loads((tmp_path / "rung15_capture_failure.json").read_text(encoding="utf-8"))
    assert len(rec["attempts"]) == 1
    assert rec["attempts"][0]["failure_class"] == "max_chunks_exhausted"


def test_thin_page_anchor_miss_retries_to_exhaustion(tmp_path, monkeypatch):
    # A page with a thin module-preload list (< the degraded floor of 15) whose
    # scan misses the anchor is the transient degraded variant -> retried to K.
    fake = types.SimpleNamespace(
        body=b"<html>thin</html>", final_url="https://x/pricing/", status=200
    )
    monkeypatch.setattr(runner, "_rung1_fetch", lambda url, **k: (fake, None))
    monkeypatch.setattr(runner, "_chunk_urls", lambda html, base: [f"u{i}" for i in range(4)])
    monkeypatch.setattr(
        runner, "_discover_prices_chunk",
        lambda urls, **k: (None, None, None, [], "anchor_not_found"),
    )

    code, msg = _run(tmp_path, max_page_attempts=3)

    assert code == 3
    assert "last failure_class=anchor_not_found_thin_page" in msg
    rec = json.loads((tmp_path / "rung15_capture_failure.json").read_text(encoding="utf-8"))
    assert len(rec["attempts"]) == 3  # transient class: retried all K attempts
    assert all(
        a["failure_class"] == "anchor_not_found_thin_page" for a in rec["attempts"]
    )
    assert all(a["module_preload_count"] == 4 for a in rec["attempts"])


def test_data_lake_mode_failure_writes_no_artifact(tmp_path, monkeypatch):
    # In data-lake mode there is no output directory: an all-attempts miss must
    # still exit 3 with the diagnosis in the message, and write NOTHING (no
    # partial packet before a complete packet exists).
    monkeypatch.setattr(runner, "_rung1_fetch", lambda url, **k: (_fetch_failure(), None))

    code, msg = _run(
        tmp_path, max_page_attempts=1, output_directory=None, data_root=object()
    )

    assert code == 3
    assert "no packet artifact written in data-lake mode" in msg
    assert list(tmp_path.iterdir()) == []


def test_discovery_byte_budget_stops_only_after_anchor_check(monkeypatch):
    # Discovery-internal pins: (1) the budget is checked AFTER the anchor test,
    # so an over-budget chunk that CARRIES the anchor is still a hit; (2) a
    # budget stop returns the honest classified miss with the scan log.
    bodies = {"u0": b"x" * 600, "u1": b'y' * 600, "u2": b"z" * 600}

    def fake_fetch(url, **k):
        return types.SimpleNamespace(body=bodies[url], status=200), None

    monkeypatch.setattr(runner, "_rung1_fetch", fake_fetch)
    monkeypatch.setattr(runner, "chunk_contains_prices", lambda text: False)
    url, res, cls, scanned, reason = runner._discover_prices_chunk(
        ["u0", "u1", "u2"], timeout=5, max_chunks=10, byte_budget=1000
    )
    assert (url, res, cls) == (None, None, None)
    assert reason == "byte_budget_exceeded"
    assert [s["url"] for s in scanned] == ["u0", "u1"]  # stopped mid-list

    # Same budget, but the over-budget chunk carries the anchor: still a hit.
    monkeypatch.setattr(
        runner, "chunk_contains_prices", lambda text: text.startswith("y")
    )
    url, res, cls, scanned, reason = runner._discover_prices_chunk(
        ["u0", "u1", "u2"], timeout=5, max_chunks=10, byte_budget=1000
    )
    assert reason is None
    assert url == "u1"


def test_discovery_distinguishes_scan_limit_from_full_scan_miss(monkeypatch):
    # max_chunks_exhausted = stopped at the scan cap before seeing the full
    # list; anchor_not_found = scanned the whole list and the anchor is absent.
    # A failed chunk fetch is logged as status="fetch_failed" and skipped.
    def fake_fetch(url, **k):
        if url == "u1":
            return _fetch_failure("chunk down"), None
        return types.SimpleNamespace(body=b"nope", status=200), None

    monkeypatch.setattr(runner, "_rung1_fetch", fake_fetch)
    monkeypatch.setattr(runner, "chunk_contains_prices", lambda text: False)

    *_, scanned, reason = runner._discover_prices_chunk(
        ["u0", "u1", "u2", "u3", "u4"], timeout=5, max_chunks=3, byte_budget=10**9
    )
    assert reason == "max_chunks_exhausted"
    assert len(scanned) == 3  # scanned exactly the cap
    assert scanned[1] == {"url": "u1", "status": "fetch_failed", "detail": "chunk down"}

    *_, scanned, reason = runner._discover_prices_chunk(
        ["u0", "u1", "u2"], timeout=5, max_chunks=3, byte_budget=10**9
    )
    assert reason == "anchor_not_found"
    assert len(scanned) == 3


def _fake_success(body=b"<html>page</html>"):
    return types.SimpleNamespace(
        body=body,
        final_url="https://x/pricing/",
        requested_url="https://x/pricing/",
        status=200,
        metadata={"capture_timestamp": "2026-07-17T00:00:00Z",
                  "content_type": "text/html"},
        response_headers={},
        warning_notes=[],
        impersonation_profile="test_profile",
    )


def _fake_classification():
    return types.SimpleNamespace(
        classification=types.SimpleNamespace(value="content_unverified"),
        signal=None,
    )


def _wire_success_path(monkeypatch, verdict):
    # Discovery succeeds with fakes; extraction/certification are stubbed so
    # the pin isolates the RUNNER's wiring, not the extraction library (which
    # has its own 12 certification tests).
    monkeypatch.setattr(
        runner, "_rung1_fetch",
        lambda url, **k: (_fake_success(), _fake_classification()),
    )
    monkeypatch.setattr(runner, "_chunk_urls", lambda html, base: ["https://x/c.js"])
    monkeypatch.setattr(runner, "chunk_contains_prices", lambda text: True)
    monkeypatch.setattr(runner, "decode_react_router_stream", lambda html: {})
    monkeypatch.setattr(runner, "extract_tier_structure", lambda root: [])
    monkeypatch.setattr(runner, "extract_prices_object", lambda text: {})
    monkeypatch.setattr(runner, "extract_token_list", lambda text: [])
    monkeypatch.setattr(
        runner, "join_tiers_with_amounts", lambda tiers, prices, currency: []
    )
    monkeypatch.setattr(runner, "certify_extraction", lambda **k: verdict)
    calls = {}

    def fake_write(**kwargs):
        calls.update(kwargs)
        return types.SimpleNamespace(output_directory="written_dir")

    monkeypatch.setattr(runner, "stage_and_write_packet", fake_write)
    return calls


def test_success_path_certified_wiring(tmp_path, monkeypatch):
    verdict = types.SimpleNamespace(
        certified=True, priced_tier_count=0, checks=[],
        as_dict=lambda: {"certified": True},
    )
    calls = _wire_success_path(monkeypatch, verdict)

    code, out = _run(tmp_path)

    assert (code, out) == (0, "written_dir")
    assert [name for name, _body in calls["staged_artifacts"]] == [
        "rung15_pricing_page_body.bin",
        "rung15_prices_payload_chunk.js",
        "rung15_price_extraction.json",
        "rung15_extraction_metadata.json",
        "rung15_certification.json",
    ]  # no announcement body when announcement_url is None
    assert len(calls["source_slices"]) == 2
    assert calls["limitations"] == []
    assert "content_certification:certified" in calls["visible_mode_changes"]
    assert "discriminator=certified" in calls["receipt_summary"]
    assert calls["source_surface"] == "openai_chatgpt_pricing_rung15"


def test_success_path_uncertified_wiring(tmp_path, monkeypatch):
    # An uncertified verdict still writes the packet (payloads preserved) but
    # exits 4 and surfaces the failed checks as an explicit limitation.
    verdict = types.SimpleNamespace(
        certified=False, priced_tier_count=0,
        checks=[types.SimpleNamespace(name="tiers_nonempty", passed=False)],
        as_dict=lambda: {"certified": False},
    )
    calls = _wire_success_path(monkeypatch, verdict)

    code, out = _run(tmp_path)

    assert (code, out) == (4, "written_dir")
    assert calls["limitations"] == [
        "content_certification_failed: rung15_price_payload_v0 checks ['tiers_nonempty']"
    ]
    assert "content_certification:uncertified" in calls["visible_mode_changes"]
    assert "discriminator=uncertified" in calls["receipt_summary"]
