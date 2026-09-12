import copy
import json
from pathlib import Path
import sys

import pytest

from reports.efficiency_batch import reconcile_runs, selection
from runners import run_efficiency as cli


def native(folder, thread, tokens=10, parent=None, complete=True):
    usage = {"input_tokens": tokens, "output_tokens": 3, "total_tokens": tokens + 3,
             "cached_input_tokens": 0, "cache_write_input_tokens": 0, "reasoning_output_tokens": 0}
    meta = {"id": thread, "parent_thread_id": parent, "timestamp": "2026-09-05T00:00:00Z",
            "source": {"subagent": {"thread_spawn": {"parent_thread_id": parent}}} if parent else "vscode"}
    rows = [{"type": "session_meta", "payload": meta},
            {"type": "event_msg", "timestamp": "2026-09-05T00:00:00Z", "payload": {"type": "task_started", "turn_id": "turn"}},
            {"type": "turn_context", "payload": {"turn_id": "turn", "model": "fixture"}},
            {"type": "token_usage_record", "payload": {"thread_id": thread, "turn_id": "turn", "root_turn_id": "turn",
             "response_id": "response", "usage": usage, "turn_token_usage": usage}}]
    if complete:
        rows.append({"type": "event_msg", "timestamp": "2026-09-05T00:00:02Z",
                     "payload": {"type": "task_complete", "turn_id": "turn"}})
    folder.mkdir(exist_ok=True)
    (folder / f"{thread}.jsonl").write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")


def row(label):
    return {"label": label, "thread_id": label, "turn_id": "turn", "workflow": "sample", "workload_id": "same-fixture"}


def run_report(tmp_path, selections, capsys, budget=8192):
    manifest = tmp_path / "selection.json"
    manifest.write_text(json.dumps(selections), encoding="utf-8")
    code = cli.main(["report-codex", "--sessions-dir", str(tmp_path / "sessions"), "--selection", str(manifest),
                     "--output-dir", str(tmp_path / "records"), "--max-output-bytes", str(budget)])
    captured = capsys.readouterr()
    assert len(captured.out.encode("utf-8")) <= budget
    returned = json.loads(captured.out)
    persisted = json.loads(Path(returned["record_path"]).read_text(encoding="utf-8"))
    return code, returned, persisted


def test_real_native_parent_child_union_preserves_failed_selected_run(tmp_path, capsys):
    native(tmp_path / "sessions", "root")
    native(tmp_path / "sessions", "child", 20, parent="root")
    native(tmp_path / "sessions", "failed", 30)
    (tmp_path / "fail.json").write_text(json.dumps([sys.executable, "-c", "print('failure'); raise SystemExit(7)"]))
    selected = {"runs": [row("root"), row("child"), {**row("failed"), "quality_command": "fail.json"}],
                "comparisons": [{"label": "one pair", "baseline": ["root"], "candidate": ["failed"]}]}
    code, returned, saved = run_report(tmp_path, selected, capsys)
    assert code == 7 and saved["status"] == "failed"
    accounting = saved["accounting"]
    assert accounting["usage"]["coverage"] == "complete", [r["collection_issues"] for r in saved["runs"]]
    assert accounting["usage"]["total_tokens"] == 69  # 13 + 23 + 33, never 92.
    assert accounting["unique_model_responses"] == 3
    assert accounting["duplicate_response_observations"] == 1
    assert saved["runs"][2]["quality"] == "failed"
    assert saved["comparisons"][0]["overall"] == "inconclusive"
    assert returned["record_readback_matched"] is True


def test_incomplete_turn_remains_uncollected_and_later_completed_turn_recovers(tmp_path, capsys):
    native(tmp_path / "sessions", "root", complete=False)
    native(tmp_path / "sessions", "other", 20)
    selected = {"runs": [row("root"), row("other")]}
    code, _, saved = run_report(tmp_path, selected, capsys)
    assert code == 2 and saved["accounting"]["usage"]["coverage"] == "unknown"
    assert saved["accounting"]["usage"]["total_tokens"] is None
    assert saved["accounting"]["uncollected"] == ["root"]
    assert saved["runs"][0]["diagnostic_path"]
    native(tmp_path / "sessions", "root")
    code, _, recovered = run_report(tmp_path, selected, capsys)
    assert code == 0 and recovered["accounting"]["usage"]["total_tokens"] == 36
    assert saved["accounting"]["uncollected"] == ["root"]


def test_combined_batch_overflow_retains_all_failed_rows(tmp_path, capsys):
    for index in range(12):
        native(tmp_path / "sessions", str(index))
    selected = {"runs": [row(str(index)) for index in range(12)]}
    (tmp_path / "fail.json").write_text(json.dumps([sys.executable, "-c", "raise SystemExit(7)"]))
    selected["runs"][-1]["quality_command"] = "fail.json"
    code, returned, saved = run_report(tmp_path, selected, capsys, budget=1024)
    assert code == 7 and returned["return_view"] == "details_required"
    assert returned["facts"]["failed_or_uncollected_runs"] == 1
    assert saved["runs"][-1]["quality"] == "failed"
    assert returned["facts"]["selected_runs"] == len(saved["runs"]) == 12
    assert saved["accounting"]["usage"]["total_tokens"] == 156


def test_conflicting_duplicate_cannot_choose_a_convenient_total():
    attempt = {"thread_id": "child", "turn_id": "turn", "response_id": "response",
               "usage": {"coverage": "complete", "input_tokens": 10, "output_tokens": 3, "total_tokens": 13}}
    record = {"usage": {"coverage": "complete"}, "attempts": [attempt]}
    changed = copy.deepcopy(record)
    changed["attempts"][0]["usage"]["total_tokens"] = 99
    result = reconcile_runs({"parent": record, "child": changed}, uncollected=[])
    assert result["conflicts"] == [["child", "turn", "response"]]
    assert result["usage"]["total_tokens"] is result["usage"]["observed_totals"]["total_tokens"] is None
    assert result["threads"]["child"]["observed_usage"] is None


@pytest.mark.parametrize("bad", [
    {"runs": [row("a"), row("a")]},
    {"runs": [{**row("a"), "timeout_seconds": "forever"}]},
    {"runs": [row("a")], "comparisons": [{"label": "x", "baseline": ["a"], "candidate": ["missing"]}]},
    {"runs": [{**row("a"), "invented_option": True}]},
])
def test_selection_refuses_ambiguous_or_invalid_inputs(tmp_path, bad):
    with pytest.raises(ValueError):
        selection(bad, tmp_path)
