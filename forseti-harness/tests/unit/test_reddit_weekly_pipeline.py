from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
from pathlib import Path

import pytest

from runners import run_reddit_weekly_pipeline as pipe
from runners.run_reddit_weekly_finalizer import finalize_reddit_weekly_run


def _candidate(tid: str, sub: str = "skincareaddiction", comments: int = 40) -> dict:
    return {
        "thread_url": f"https://www.reddit.com/r/{sub}/comments/{tid}/title/",
        "subreddit": sub, "comments": comments, "score": 10, "title_or_none": f"title {tid}",
        "flair_or_none": None, "listing_post_type_or_none": "text", "selection_reason": "comment_floor_cleared",
        "subreddit_rank_by_comments": 1, "timestamp_utc_ms_or_none": "1790000000000",
    }


def _reader(tmp_path: Path, ids: list[str]) -> Path:
    path = tmp_path / "reader.json"
    path.write_text(json.dumps({"run_name": "Reddit Top100 2026-09-23", "candidates": [_candidate(t) for t in ids]}), encoding="utf-8")
    return path


def test_adjudicate_repairs_incomplete_chunk_and_builds_best_sort_batches(tmp_path: Path) -> None:
    calls: list[str] = []

    def fake(prompt: str, schema: dict) -> dict:
        calls.append(prompt)
        ids = re.findall(r"^(t\w+)\t", prompt, flags=re.M)
        codes = {"t1": "yF", "t2": "bo", "t3": "na"}
        decisions = [{"thread_id": t, "code": codes[t]} for t in ids]
        if len(calls) == 1:
            decisions = decisions[:-1]  # first answer drops a row
        return {"output": {"decisions": decisions}, "usage": {"input_tokens": 1, "output_tokens": 1}}

    run = tmp_path / "run"
    result = pipe.adjudicate(run, _reader(tmp_path, ["t1", "t2", "t3"]), fake, chunk_rows=150, workers=1)

    assert len(calls) == 2 and "previous answer was rejected" in calls[1]
    assert result["counts"] == {"yes": 1, "borderline": 1, "no": 1}
    manifest = json.loads((run / "deep_dive_manifest_v1.json").read_text(encoding="utf-8"))
    assert [r["capture_wave"] for r in manifest["pending"]] == ["high_priority", "borderline_resolution"]
    batch = json.loads((run / "capture-batches" / "batch_001.json").read_text(encoding="utf-8"))
    assert all(s["url"].endswith("?sort=confidence") for s in batch)


def test_adjudicate_fails_loudly_when_repair_still_incomplete(tmp_path: Path) -> None:
    def fake(prompt: str, schema: dict) -> dict:
        return {"output": {"decisions": [{"thread_id": "t1", "code": "yf"}]}, "usage": {}}

    with pytest.raises(pipe.PipelineError, match="still invalid"):
        pipe.adjudicate(tmp_path / "run", _reader(tmp_path, ["t1", "t2"]), fake, chunk_rows=150, workers=1)


def _summary(results: list[dict], tripped: bool = False) -> dict:
    return {"results": results, "circuit_breaker": {"tripped": tripped}, "access_diagnostic_failure_count": 0}


def test_capture_retries_failed_slots_once_and_merges_index(tmp_path: Path) -> None:
    run = tmp_path / "run"
    (run / "capture-batches").mkdir(parents=True)
    slots = [{"slot_id": "deep_0001", "url": "u1"}, {"slot_id": "deep_0002", "url": "u2"}]
    (run / "capture-batches" / "batch_001.json").write_text(json.dumps(slots), encoding="utf-8")
    runs: list[Path] = []

    def fake_run(url_list: Path, output_root: Path, resume: bool) -> None:
        runs.append(output_root)
        output_root.mkdir(parents=True, exist_ok=True)
        wanted = json.loads(url_list.read_text(encoding="utf-8"))
        results = []
        for s in wanted:
            ok = not (s["slot_id"] == "deep_0002" and output_root.name.endswith("surface"))
            results.append({"slot_id": s["slot_id"], "capture_exit": 0 if ok else 2,
                            "content_record_preserved": ok, "packet_dir": f"P/{s['slot_id']}" if ok else None})
        (output_root / "batch_summary.json").write_text(json.dumps(_summary(results)), encoding="utf-8")

    pipe.capture(run, fake_run, first=None, last=None)

    assert [p.name for p in runs] == ["batch_001_surface", "batch_001_retry"]
    index = json.loads((run / "captures" / "batch_001_index.json").read_text(encoding="utf-8"))
    assert index == {"deep_0001": "P/deep_0001", "deep_0002": "P/deep_0002"}


def test_capture_records_deleted_post_as_unavailable_without_retry(tmp_path: Path) -> None:
    run = tmp_path / "run"
    (run / "capture-batches").mkdir(parents=True)
    slots = [{"slot_id": "deep_0001", "url": "u1"}, {"slot_id": "deep_0002", "url": "u2"}]
    (run / "capture-batches" / "batch_001.json").write_text(json.dumps(slots), encoding="utf-8")
    gone_packet = tmp_path / "P" / "deep_0002"
    (gone_packet / "raw").mkdir(parents=True)
    (gone_packet / "raw" / "02_02_realchrome_visible_text.txt").write_text(
        "r/FancyFollicles\n[deleted]\nSorry, this post was deleted by the person who originally posted it.\nShare", encoding="utf-8")
    runs: list[Path] = []

    def fake_run(url_list: Path, output_root: Path, resume: bool) -> None:
        runs.append(output_root)
        output_root.mkdir(parents=True, exist_ok=True)
        results = [{"slot_id": "deep_0001", "url": "u1", "capture_exit": 0, "content_record_preserved": True, "packet_dir": "P/deep_0001"},
                   {"slot_id": "deep_0002", "url": "u2", "capture_exit": 4, "content_record_preserved": False, "packet_dir": str(gone_packet)}]
        (output_root / "batch_summary.json").write_text(json.dumps(_summary(results)), encoding="utf-8")

    pipe.capture(run, fake_run, first=None, last=None)

    assert [p.name for p in runs] == ["batch_001_surface"]  # no retry for a post Reddit says is gone
    assert json.loads((run / "captures" / "batch_001_index.json").read_text(encoding="utf-8")) == {"deep_0001": "P/deep_0001"}
    [gone] = json.loads((run / "captures" / "unavailable_slots.json").read_text(encoding="utf-8"))
    assert gone["slot_id"] == "deep_0002" and gone["batch"] == "001" and gone["status"] == "source_deleted_or_removed"
    assert gone["evidence"] == "Sorry, this post was deleted by the person who originally posted it"


def test_capture_records_deleted_post_discovered_on_retry(tmp_path: Path) -> None:
    run = tmp_path / "run"
    (run / "capture-batches").mkdir(parents=True)
    (run / "capture-batches" / "batch_001.json").write_text(
        json.dumps([{"slot_id": "deep_0001", "url": "u1"}]), encoding="utf-8")
    gone_packet = tmp_path / "deleted_packet"
    (gone_packet / "raw").mkdir(parents=True)
    (gone_packet / "raw" / "visible_text.txt").write_text(
        "Sorry, this post was deleted by the person who originally posted it.", encoding="utf-8")
    calls = []

    def fake_run(url_list: Path, output_root: Path, resume: bool) -> None:
        calls.append(output_root)
        output_root.mkdir(parents=True)
        result = {"slot_id": "deep_0001", "url": "u1", "capture_exit": 2}
        if len(calls) == 2:
            result["packet_dir"] = str(gone_packet)
        (output_root / "batch_summary.json").write_text(json.dumps(_summary([result])), encoding="utf-8")

    pipe.capture(run, fake_run, first=None, last=None)
    assert len(calls) == 2
    assert json.loads((run / "captures" / "unavailable_slots.json").read_text(encoding="utf-8"))[0]["slot_id"] == "deep_0001"


def test_scope_drops_unavailable_slots_and_records_them(tmp_path: Path) -> None:
    run = tmp_path / "run"
    (run / "capture-batches").mkdir(parents=True)
    (run / "captures").mkdir()
    (run / "capture-batches" / "batch_001.json").write_text(
        json.dumps([{"slot_id": "deep_0001", "url": "u1"}, {"slot_id": "deep_0002", "url": "u2"}]), encoding="utf-8")
    pending = [{"deep_dive_order": i, "thread_id": f"t{i}"} for i in (1, 2, 3)]
    manifest = {"coverage": {"admitted": 3}, "pending": pending}
    (run / "deep_dive_manifest_v1.json").write_text(json.dumps(manifest), encoding="utf-8")
    (run / "batch_001_extracts_v1.jsonl").write_text("{}\n", encoding="utf-8")
    (run / "captures" / "unavailable_slots.json").write_text(json.dumps([
        {"slot_id": "deep_0002", "url": "u2", "status": "source_deleted_or_removed", "evidence": "Sorry, this post was deleted", "batch": "001"}]),
        encoding="utf-8")

    result = pipe.scope(run, 1)

    narrowed = json.loads((Path(result["finalize_dir"]) / "deep_dive_manifest_v1.json").read_text(encoding="utf-8"))
    assert [r["thread_id"] for r in narrowed["pending"]] == ["t1"]
    assert narrowed["coverage"]["admitted"] == 1
    assert narrowed["coverage"]["source_unavailable_at_capture"] == [
        {"slot_id": "deep_0002", "url": "u2", "status": "source_deleted_or_removed", "evidence": "Sorry, this post was deleted"}]


def test_capture_stops_on_refusal_without_retrying(tmp_path: Path) -> None:
    run = tmp_path / "run"
    (run / "capture-batches").mkdir(parents=True)
    (run / "capture-batches" / "batch_001.json").write_text(json.dumps([{"slot_id": "deep_0001", "url": "u"}]), encoding="utf-8")

    def fake_run(url_list: Path, output_root: Path, resume: bool) -> None:
        output_root.mkdir(parents=True, exist_ok=True)
        (output_root / "batch_summary.json").write_text(json.dumps(_summary([], tripped=True)), encoding="utf-8")

    with pytest.raises(pipe.PipelineError, match="refused"):
        pipe.capture(run, fake_run, first=None, last=None)


@pytest.mark.parametrize("field,value", [
    ("access_diagnostic_count", 1),
    ("access_diagnostic_failure_count", 1),
    ("navigation_http_status", 403),
])
def test_capture_refusal_signals_stop_before_retry(tmp_path: Path, field: str, value: int) -> None:
    run = tmp_path / "run"
    (run / "capture-batches").mkdir(parents=True)
    (run / "capture-batches" / "batch_001.json").write_text(
        json.dumps([{"slot_id": "deep_0001", "url": "u"}]), encoding="utf-8")
    calls = []

    def fake_run(url_list: Path, output_root: Path, resume: bool) -> None:
        calls.append(output_root)
        output_root.mkdir(parents=True)
        summary = _summary([{"slot_id": "deep_0001", "capture_exit": 2}])
        if field == "navigation_http_status":
            summary["results"][0][field] = value
        else:
            summary[field] = value
        (output_root / "batch_summary.json").write_text(json.dumps(summary), encoding="utf-8")

    with pytest.raises(pipe.PipelineError, match="refused"):
        pipe.capture(run, fake_run, first=None, last=None)
    assert len(calls) == 1


def _read_fixture(tmp_path: Path) -> Path:
    run = tmp_path / "run"
    packet = tmp_path / "packet"
    (packet / "raw").mkdir(parents=True)
    record = {
        "thread": {"thread_id": "t1", "title": "Foundation turns orange"},
        "post": {"author_state": "op_user", "body_text": "Every foundation oxidizes.", "score_state": "40"},
        "comment_completeness": {"comments_captured": 3, "declared_total_comments": 30},
        "comments": [
            {"comment_id": "c1", "author_state": "alice", "body_text": "Same, mine turned orange in an hour.", "score_state": "9", "depth": 0, "comment_posture": "present"},
            {"comment_id": "c2", "author_state": "bob", "body_text": "Mine oxidizes too, every brand.", "score_state": "5", "depth": 0, "comment_posture": "present"},
            {"comment_id": "c3", "author_state": "carol", "body_text": "Try a different primer.", "score_state": "2", "depth": 0, "comment_posture": "present"},
        ],
    }
    (packet / "raw" / "01_content_record.json").write_text(json.dumps(record), encoding="utf-8")
    pending = [{"deep_dive_order": 1, "thread_id": "t1", "thread_url": "https://www.reddit.com/r/palemua/comments/t1/x/",
                "subreddit": "palemua", "admission": "yes", "priority_band": "high", "capture_wave": "high_priority",
                "title_or_none": "Foundation turns orange", "listing_snapshot": {"score": 40, "comments": 30}}]
    manifest = {"schema": "forseti.reddit.weekly_deep_dive_manifest.v1", "methodology_id": pipe.METHODOLOGY_ID,
                "decision_frame": pipe.DECISION_FRAME, "read_policy_id": pipe.READ_POLICY_ID,
                "coverage": {"admitted": 1}, "existing_admitted_captures": [], "pending": pending}
    (run / "captures").mkdir(parents=True)
    (run / "deep_dive_manifest_v1.json").write_text(json.dumps(manifest), encoding="utf-8")
    (run / "capture-batches").mkdir()
    (run / "capture-batches" / "batch_001.json").write_text(json.dumps([{"slot_id": "deep_0001", "url": "u"}]), encoding="utf-8")
    (run / "captures" / "batch_001_index.json").write_text(json.dumps({"deep_0001": str(packet)}), encoding="utf-8")
    return run


def _judgment(support: list[str]) -> dict:
    return {
        "thread_id": "t1", "admission": "yes", "core_problem": "Foundations oxidize orange on fair skin.",
        "commercial_signal": "A fair-shade line that stays neutral could win switchers.", "evidence_strength": "medium",
        "contribution_class": "material_addition", "caveats": [], "named_brands": [],
        "where_customers_go": [], "workarounds_or_substitutions": [], "quote_comment_ids": ["c1", "c2"],
        "reason_codes": ["shade_oxidation"], "priority": "high", "comments_reviewed": 3,
        "stop_reason": "corpus_exhausted", "consecutive_no_value_batches": 0,
        "claims": [{"claim_id": "oxidation", "statement": "Users report foundations turning orange.",
                    "evidence_kind": "recurrence", "corroboration_status": "emerging",
                    "support_comment_ids": support, "counter_comment_ids": []}],
    }


def test_read_repairs_invalid_thread_fills_fields_and_finalizes(tmp_path: Path) -> None:
    run = _read_fixture(tmp_path)
    prompts: list[str] = []

    def fake(prompt: str, schema: dict) -> dict:
        prompts.append(prompt)
        support = ["c1", "zz"] if len(prompts) == 1 else ["c1", "c2"]  # first answer cites a missing comment
        return {"output": {"threads": [_judgment(support)]}, "usage": {"input_tokens": 100, "output_tokens": 50}}

    result = pipe.read(run, fake, first=None, last=None, workers=1)

    assert result == {"batches_read": 1, "yes": 1, "no": 0, "repaired_threads": 1}
    assert "--- COHORT" in prompts[0] and "rejected" in prompts[1]
    extract = json.loads((run / "batch_001_extracts_v1.jsonl").read_text(encoding="utf-8").strip())
    assert extract["quotes"][0] == {"comment_id": "c1", "text": "Same, mine turned orange in an hour."}
    assert extract["caveats"][-1] == "surface capture: 3 of 30 comments"
    assert "independent_reporters" not in extract and "read_policy_id" not in extract
    usage = [json.loads(line) for line in (run / "model_usage_log.jsonl").read_text(encoding="utf-8").splitlines()]
    assert [u["unit"] for u in usage] == ["batch_001", "batch_001_repair"]
    pipe.read(run, fake, first=None, last=None, workers=1)  # finished batch: no new calls, no new usage rows
    assert len((run / "model_usage_log.jsonl").read_text(encoding="utf-8").splitlines()) == 2

    finalized = finalize_reddit_weekly_run(deep_dive_dir=run, output_dir=run / "out", as_of=dt.date(2026, 9, 23))
    assert finalized["threads"] == 1 and finalized["yes"] == 1


def test_read_skips_batches_that_already_have_extracts(tmp_path: Path) -> None:
    run = _read_fixture(tmp_path)
    (run / "batch_001_extracts_v1.jsonl").write_text("{}\n", encoding="utf-8")

    def fake(prompt: str, schema: dict) -> dict:  # pragma: no cover - must not be called
        raise AssertionError("model must not be called for a finished batch")

    assert pipe.read(run, fake, first=None, last=None, workers=1)["batches_read"] == 0


def test_read_repairs_duplicate_judgments_instead_of_accepting_last(tmp_path: Path) -> None:
    run = _read_fixture(tmp_path)
    calls = []

    def fake(prompt: str, schema: dict) -> dict:
        calls.append(prompt)
        threads = [_judgment(["c1", "c2"])]
        if len(calls) == 1:
            threads.append(_judgment(["c1", "c2"]))
        return {"output": {"threads": threads}, "usage": {}}

    assert pipe.read(run, fake, first=None, last=None, workers=1)["repaired_threads"] == 1
    assert len(calls) == 2


def test_read_empty_capture_batch_writes_empty_extract_without_model(tmp_path: Path) -> None:
    run = _read_fixture(tmp_path)
    (run / "captures" / "batch_001_index.json").write_text("{}", encoding="utf-8")

    def fake(prompt: str, schema: dict) -> dict:
        raise AssertionError("no captured threads to read")

    assert pipe.read(run, fake, first=None, last=None, workers=1)["batches_read"] == 1
    assert (run / "batch_001_extracts_v1.jsonl").read_text(encoding="utf-8") == ""


def test_reused_receipt_recovers_missing_usage_without_duplicate(tmp_path: Path) -> None:
    calls = []

    def fake(prompt: str, schema: dict) -> dict:
        calls.append(prompt)
        return {"output": {"decisions": []}, "usage": {"input_tokens": 5}}

    fake.receipt_identity = {"model": "one"}
    path = tmp_path / "calls" / "one.json"
    receipt = pipe.receipted_call(fake, path, "prompt", pipe.ADJUDICATE_SCHEMA)
    assert not (tmp_path / "model_usage_log.jsonl").exists()
    reused = pipe.receipted_call(fake, path, "prompt", pipe.ADJUDICATE_SCHEMA)
    row = {"stage": "adjudicate", "unit": "chunk_001", "prompt_sha256": reused["prompt_sha256"], **reused["usage"]}
    pipe._append_usage(tmp_path, row)
    pipe._append_usage(tmp_path, row)
    assert len((tmp_path / "model_usage_log.jsonl").read_text(encoding="utf-8").splitlines()) == 1
    fake.receipt_identity = {"model": "two"}
    changed = pipe.receipted_call(fake, path, "prompt", pipe.ADJUDICATE_SCHEMA)
    assert changed["prompt_sha256"] != receipt["prompt_sha256"]
    assert len(calls) == 2


def test_fresh_call_with_same_prompt_is_still_logged(tmp_path: Path) -> None:
    row = {"stage": "read", "unit": "batch_001_repair", "prompt_sha256": "abc", "output_tokens": 10, "duration_ms": 5}
    pipe._append_usage(tmp_path, row)
    pipe._append_usage(tmp_path, {**row, "output_tokens": 12, "duration_ms": 7})  # discarded receipt, re-called
    assert len((tmp_path / "model_usage_log.jsonl").read_text(encoding="utf-8").splitlines()) == 2


def test_model_nonzero_exit_rejects_structured_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(args, 1, stdout=json.dumps({
            "structured_output": {"decisions": []}, "usage": {}, "result": "CLI failed"
        }), stderr="")

    monkeypatch.setattr(pipe.subprocess, "run", fake_run)
    call = pipe.claude_structured_call_factory(
        model="sonnet", effort="medium", timeout=1, executable="claude", bare=False, cwd=tmp_path)
    with pytest.raises(pipe.PipelineError, match="model call failed"):
        call("prompt", pipe.ADJUDICATE_SCHEMA)
