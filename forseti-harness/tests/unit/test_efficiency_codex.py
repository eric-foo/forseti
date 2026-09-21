"""Counterexamples for truthful Codex usage and task coverage."""
import json
import pytest

from reports.efficiency_codex import collect_codex_exec, collect_codex_rollouts, collect_desktop_task


def usage(n=10):
    return {"input_tokens": n, "cached_input_tokens": 4,
            "cache_write_input_tokens": 0, "output_tokens": 3,
            "reasoning_output_tokens": 1, "total_tokens": n + 3}


def write(tmp_path, rows, name="events.jsonl"):
    path = tmp_path / name
    path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
    return path


def exec_rows():
    return [{"type": "thread.started", "thread_id": "root"},
            {"type": "turn.started"},
            {"type": "turn.completed", "usage": usage()}]


def rollout(thread="root", complete=True):
    rows = [{"type": "session_meta", "payload": {"id": thread, "cli_version": "0.153.1"}},
            {"type": "event_msg", "timestamp": "2026-09-05T00:00:00Z",
             "payload": {"type": "task_started", "turn_id": "turn"}},
            {"type": "turn_context", "payload": {"turn_id": "turn", "model": "test-model"}},
            {"type": "token_usage_record", "payload": {
                "thread_id": thread, "turn_id": "turn", "response_id": "response-1",
                "usage": usage(), "turn_token_usage": usage(),
                "thread_token_usage": usage(9999)}}]
    if complete:
        rows.append({"type": "event_msg", "payload": {
            "type": "task_complete", "turn_id": "turn", "duration_ms": 1200}})
    return rows


def collect(path, **kwargs):
    return collect_codex_rollouts([path], selected_turns={"root": ["turn"]},
                                  root_thread_id="root", **kwargs)


def test_fresh_complete_exec_reports_usage(tmp_path):
    result = collect_codex_exec(write(tmp_path, exec_rows()), fresh_session=True)
    assert result["coverage"] == "complete"
    assert result["attempts"][0]["usage"]["total_tokens"] == 13


def test_exec_requires_fresh_boundary(tmp_path):
    result = collect_codex_exec(write(tmp_path, exec_rows()))
    assert result["coverage"] == "unknown"
    assert "fresh_session_not_established" in result["issues"]


def test_exec_duplicate_completion_does_not_double_count(tmp_path):
    rows = exec_rows()
    rows.append(rows[-1])
    result = collect_codex_exec(write(tmp_path, rows), fresh_session=True)
    assert len(result["attempts"]) == 1
    assert result["coverage"] == "unknown"


def test_exec_failure_and_truncation_remain_incomplete(tmp_path):
    for rows in [exec_rows()[:-1], exec_rows()[:-1] + [{"type": "turn.failed"}]]:
        result = collect_codex_exec(write(tmp_path, rows), fresh_session=True)
        assert result["coverage"] == "unknown"


def test_exec_missing_usage_never_zero(tmp_path):
    rows = exec_rows()
    rows[-1].pop("usage")
    result = collect_codex_exec(write(tmp_path, rows), fresh_session=True)
    assert result["coverage"] == "unknown"
    assert result["attempts"][0]["usage"]["input_tokens"] is None


def test_exec_child_usage_cannot_claim_cheaper_task(tmp_path):
    rows = exec_rows()
    rows.insert(2, {"type": "item.completed", "item": {
        "type": "collab_tool_call", "id": "tool1", "receiver_thread_ids": ["child"]}})
    result = collect_codex_exec(write(tmp_path, rows), fresh_session=True)
    assert result["coverage"] == "unknown"
    assert result["child_thread_ids"] == ["child"]


def test_exec_multiple_turns_are_not_assumed_additive(tmp_path):
    rows = exec_rows() + exec_rows()[1:]
    result = collect_codex_exec(write(tmp_path, rows), fresh_session=True)
    assert result["coverage"] == "unknown"
    assert "single_completed_turn_required" in result["issues"]


def test_desktop_uses_responses_not_cumulative_snapshots(tmp_path):
    rows = rollout()
    rows.insert(4, {"type": "event_msg", "payload": {
        "type": "token_count", "info": {"total_token_usage": usage(999999)}}})
    result = collect(write(tmp_path, rows), expected_child_ids=[])
    assert result["coverage"] == "complete"
    assert result["attempts"][0]["usage"]["input_tokens"] == 10


def test_desktop_exact_duplicate_response_is_deduplicated(tmp_path):
    rows = rollout()
    rows.insert(4, rows[3])
    result = collect(write(tmp_path, rows), expected_child_ids=[])
    assert result["coverage"] == "complete"
    assert len(result["attempts"]) == 1


def test_desktop_conflicting_duplicate_fails(tmp_path):
    rows = rollout()
    copy = json.loads(json.dumps(rows[3]))
    copy["payload"]["usage"] = usage(12)
    rows.insert(4, copy)
    result = collect(write(tmp_path, rows), expected_child_ids=[])
    assert result["coverage"] == "unknown"
    assert "conflicting_response_duplicate" in result["issues"]


def test_desktop_missing_request_detected_by_cumulative(tmp_path):
    rows = rollout()
    rows[3]["payload"]["turn_token_usage"] = usage(100)
    result = collect(write(tmp_path, rows), expected_child_ids=[])
    assert result["coverage"] == "unknown"
    assert "turn_cumulative_reconciliation_failed" in result["issues"]


def test_desktop_active_turn_and_unknown_children_fail(tmp_path):
    result = collect(write(tmp_path, rollout(complete=False)))
    assert result["coverage"] == "unknown"
    assert "child_inventory_unknown" in result["issues"]
    assert "turn_boundary_incomplete" in result["issues"]


def test_desktop_delegation_cannot_be_declared_child_free(tmp_path):
    rows = rollout()
    rows.insert(3, {"type": "response_item", "payload": {
        "type": "function_call", "name": "spawn_agent", "arguments": "SECRET"}})
    result = collect(write(tmp_path, rows), expected_child_ids=[])
    assert result["coverage"] == "unknown"
    assert "observed_delegation_missing_children" in result["issues"]
    assert "SECRET" not in json.dumps(result)


def test_desktop_child_must_have_source_and_parent_link(tmp_path):
    path = write(tmp_path, rollout())
    result = collect_codex_rollouts([path], selected_turns={"root": ["turn"], "child": ["turn"]},
                                    root_thread_id="root", expected_child_ids=["child"])
    assert result["coverage"] == "unknown"
    assert "thread_source_missing" in result["issues"]
    assert "child_parent_link_missing_or_invalid" in result["issues"]


def test_desktop_explicit_complete_child_inventory(tmp_path):
    root = write(tmp_path, rollout())
    child = write(tmp_path, rollout("child"), "child.jsonl")
    result = collect_codex_rollouts([root, child],
        selected_turns={"root": ["turn"], "child": ["turn"]}, root_thread_id="root",
        expected_child_ids=["child"], parent_links={"child": "root"})
    assert result["coverage"] == "complete"
    assert len(result["attempts"]) == 2


def test_desktop_abort_is_not_success_with_completion_marker(tmp_path):
    rows = rollout()
    rows.insert(4, {"type": "event_msg", "payload": {"type": "turn_aborted", "turn_id": "turn"}})
    result = collect(write(tmp_path, rows), expected_child_ids=[])
    assert result["coverage"] == "unknown"
    assert "selected_turn_failed_or_aborted" in result["issues"]


def test_malformed_source_fails_without_echoing_content(tmp_path):
    path = tmp_path / "invalid.jsonl"
    path.write_text("SECRET malformed", encoding="utf-8")
    result = collect_codex_exec(path, fresh_session=True)
    assert result["coverage"] == "unknown"
    assert "SECRET" not in json.dumps(result)


def auto_rows(thread="root", parent=None, root_turn="turn", agent_path=None):
    rows = rollout(thread)
    rows[0]["payload"].update(parent_thread_id=parent, agent_path=agent_path,
                              timestamp="2026-09-05T00:00:00Z")
    if parent:
        rows[0]["payload"]["source"] = {"subagent": {"thread_spawn": {
            "parent_thread_id": parent, "agent_path": agent_path}}}
    else:
        rows[0]["payload"]["source"] = "vscode"
    rows[3]["payload"]["root_turn_id"] = root_turn
    rows[-1]["timestamp"] = "2026-09-05T00:00:02Z"
    return rows


def test_auto_discovery_includes_guardian_and_ignores_unrelated_body(tmp_path):
    write(tmp_path, auto_rows())
    write(tmp_path, auto_rows("child", "root"), "child.jsonl")
    guardian = auto_rows("guardian", "child")
    guardian[0]["payload"]["source"] = {"subagent": {"other": "guardian"}}
    write(tmp_path, guardian, "guardian.jsonl")
    unrelated = write(tmp_path, auto_rows("unrelated"), "unrelated.jsonl")
    with unrelated.open("a", encoding="utf-8") as stream:
        stream.write("\nSECRET invalid body must never be read")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "complete"
    assert len(result["attempts"]) == 3
    assert result["child_thread_ids"] == ["child", "guardian"]
    assert result["source_kinds"]["guardian"] == "guardian"
    assert result["elapsed_seconds"] == 2
    assert "SECRET" not in json.dumps(result)


def test_auto_discovery_exact_root_turn_excludes_other_child_work(tmp_path):
    write(tmp_path, auto_rows())
    write(tmp_path, auto_rows("child", "root", root_turn="other-turn"), "child.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "complete"
    assert result["child_thread_ids"] == []
    assert len(result["attempts"]) == 1


def test_auto_discovery_missing_child_usage_is_not_zero(tmp_path):
    write(tmp_path, auto_rows())
    child = auto_rows("child", "root")
    child.pop(3)
    write(tmp_path, child, "child.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "unknown"
    assert "child_turn_root_attribution_missing" in result["issues"]
    assert "turn_usage_missing" in result["issues"]


def test_auto_discovery_missing_entire_child_detected_by_receipt(tmp_path):
    rows = auto_rows()
    rows[3:3] = [
        {"type": "response_item", "payload": {"type": "function_call",
            "name": "spawn_agent", "call_id": "spawn1"}},
        {"type": "response_item", "payload": {"type": "function_call_output",
            "call_id": "spawn1", "output": json.dumps({"task_name": "/root/missing"})}},
    ]
    write(tmp_path, rows)
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "unknown"
    assert "spawn_receipt_child_usage_missing_or_ambiguous" in result["issues"]


def test_auto_discovery_spawn_receipt_resolves_metadata_path(tmp_path):
    rows = auto_rows()
    rows[3:3] = [
        {"type": "response_item", "payload": {"type": "function_call",
            "name": "spawn_agent", "call_id": "spawn1"}},
        {"type": "response_item", "payload": {"type": "function_call_output",
            "call_id": "spawn1", "output": json.dumps({"task_name": "/root/worker"})}},
    ]
    write(tmp_path, rows)
    write(tmp_path, auto_rows("child", "root", agent_path="/root/worker"), "child.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "complete"
    assert result["child_thread_ids"] == ["child"]


def nested_rows(thread="root", parent="study", agent_path="/study/root", target=None):
    rows = auto_rows(thread, parent, root_turn="study-turn", agent_path=agent_path)
    if target:
        rows[3:3] = [
            {"type": "response_item", "payload": {"type": "function_call",
                "name": "spawn_agent", "call_id": "spawn1"}},
            {"type": "response_item", "payload": {"type": "function_call_output",
                "call_id": "spawn1", "output": json.dumps({"task_name": target})}},
        ]
    return rows


def test_nested_task_counts_receipt_bound_workers_with_ancestor_billing_turn(tmp_path):
    write(tmp_path, nested_rows(target="/study/root/worker"))
    write(tmp_path, nested_rows("child", "root", "/study/root/worker", "/study/root/worker/helper"), "child.jsonl")
    write(tmp_path, nested_rows("grandchild", "child", "/study/root/worker/helper"), "grandchild.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "complete", result["issues"]
    assert result["child_thread_ids"] == ["child", "grandchild"]
    assert sum(a["usage"]["total_tokens"] for a in result["attempts"]) == 39


def test_nested_task_shared_billing_alone_does_not_admit_child(tmp_path):
    write(tmp_path, nested_rows())
    write(tmp_path, nested_rows("child", "root", "/study/root/worker"), "child.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "unknown"
    assert "nested_child_launch_binding_missing" in result["issues"]


def test_nested_task_receipt_cannot_rebind_preexisting_child(tmp_path):
    write(tmp_path, nested_rows(target="/study/root/worker"))
    child = nested_rows("child", "root", "/study/root/worker")
    child[0]["payload"]["timestamp"] = "2026-09-04T00:00:00Z"
    write(tmp_path, child, "child.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "unknown"
    assert "nested_spawn_session_not_fresh" in result["issues"]


def test_nested_task_old_unlaunched_child_does_not_taint_selected_turn(tmp_path):
    write(tmp_path, nested_rows())
    child = nested_rows("child", "root", "/study/root/old-worker")
    child[0]["payload"]["timestamp"] = "2026-09-04T00:00:00Z"
    write(tmp_path, child, "child.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "complete", result["issues"]
    assert result["child_thread_ids"] == []


def test_nested_task_reused_child_turns_remain_ambiguous(tmp_path):
    write(tmp_path, nested_rows(target="/study/root/worker"))
    child = nested_rows("child", "root", "/study/root/worker")
    extra = json.loads(json.dumps(child[1:]))
    for row in extra:
        row["payload"]["turn_id"] = "later-turn"
        if row["type"] == "token_usage_record":
            row["payload"]["response_id"] = "response-2"
    write(tmp_path, child + extra, "child.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "unknown"
    assert "nested_child_turn_binding_ambiguous" in result["issues"]


def test_nested_task_conflicting_billing_does_not_disappear_from_usage(tmp_path):
    write(tmp_path, nested_rows(target="/study/root/worker"))
    child = nested_rows("child", "root", "/study/root/worker")
    child[3]["payload"]["root_turn_id"] = "foreign-turn"
    write(tmp_path, child, "child.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "unknown"
    assert "nested_child_root_attribution_conflict" in result["issues"]
    assert result["child_thread_ids"] == ["child"]
    assert sum(a["usage"]["total_tokens"] for a in result["attempts"]) == 26


def test_nested_task_fresh_metadata_cannot_rebind_old_turn(tmp_path):
    write(tmp_path, nested_rows(target="/study/root/worker"))
    child = nested_rows("child", "root", "/study/root/worker")
    child[1]["timestamp"] = "2026-09-04T00:00:00Z"
    write(tmp_path, child, "child.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "unknown"
    assert "nested_child_start_precedes_launch" in result["issues"]


def test_nested_task_child_of_unknown_creation_time_stays_unknown(tmp_path):
    write(tmp_path, nested_rows())
    child = nested_rows("child", "root", "/study/root/worker")
    del child[0]["payload"]["timestamp"]
    write(tmp_path, child, "child.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "unknown"
    assert "nested_child_launch_binding_missing" in result["issues"]


def test_nested_task_child_usage_without_started_turn_is_not_dropped(tmp_path):
    write(tmp_path, nested_rows(target="/study/root/worker"))
    child = nested_rows("child", "root", "/study/root/worker")
    extra = json.loads(json.dumps(child[3]))
    extra["payload"].update(turn_id="unstarted", response_id="response-x")
    child.insert(4, extra)
    write(tmp_path, child, "child.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "unknown"
    assert "nested_child_turn_binding_ambiguous" in result["issues"]
    assert sum(a["usage"]["total_tokens"] for a in result["attempts"]) == 39


@pytest.mark.parametrize("actor,orphan_turn", [("root", "unstarted"), ("root", None), ("child", None)])
def test_fresh_task_unbound_usage_cannot_claim_complete(tmp_path, actor, orphan_turn):
    rows = nested_rows(target="/study/root/worker" if actor == "child" else None)
    target = nested_rows("child", "root", "/study/root/worker") if actor == "child" else rows
    extra = json.loads(json.dumps(target[3]))
    extra["payload"].update(turn_id=orphan_turn, response_id="orphan-response")
    target.insert(4, extra)
    write(tmp_path, rows)
    if actor == "child":
        write(tmp_path, target, "child.jsonl")
    result = collect_desktop_task(tmp_path, agent_path="/study/root")
    assert result["coverage"] == "unknown"
    expected = "agent_turn_missing_or_ambiguous" if actor == "root" else "nested_child_usage_turn_missing"
    assert expected in result["issues"]


def test_explicit_turn_selection_keeps_missing_usage_identity_unknown(tmp_path):
    rows = nested_rows()
    extra = json.loads(json.dumps(rows[3]))
    extra["payload"].update(turn_id=None, response_id="orphan-response")
    rows.insert(4, extra)
    write(tmp_path, rows)
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "unknown"
    assert "usage_turn_missing" in result["issues"]


def test_nested_guardian_extends_completed_accounting_boundary(tmp_path):
    write(tmp_path, nested_rows())
    guardian = nested_rows("guardian", "root", "/study/root/guardian")
    guardian[0]["payload"]["source"] = {"subagent": {"other": "guardian"}}
    guardian[-1]["timestamp"] = "2026-09-05T00:00:04Z"
    write(tmp_path, guardian, "guardian.jsonl")
    result = collect_desktop_task(tmp_path, agent_path="/study/root")
    assert result["coverage"] == "complete", result["issues"]
    assert result["child_thread_ids"] == ["guardian"]
    assert result["elapsed_seconds"] == 4


@pytest.mark.parametrize("mutation,issue", [
    ("missing", "agent_path_missing_or_ambiguous"),
    ("duplicate", "agent_path_missing_or_ambiguous"),
    ("reused", "agent_turn_missing_or_ambiguous"),
    ("active", "turn_boundary_incomplete"),
])
def test_agent_path_selector_does_not_invent_a_complete_task(tmp_path, mutation, issue):
    rows = nested_rows()
    if mutation == "active":
        rows.pop()
    elif mutation == "reused":
        rows.append({"type": "event_msg", "payload": {"type": "task_started", "turn_id": "later"}})
    write(tmp_path, rows)
    if mutation == "duplicate":
        write(tmp_path, nested_rows("second"), "second.jsonl")
    result = collect_desktop_task(tmp_path, agent_path="/missing" if mutation == "missing" else "/study/root")
    assert result["coverage"] == "unknown"
    assert issue in result["issues"]


def test_auto_discovery_active_root_has_no_invented_duration(tmp_path):
    rows = auto_rows()[:-1]
    write(tmp_path, rows)
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "unknown"
    assert result["elapsed_seconds"] is None


def test_unrelated_duplicate_metadata_does_not_taint_selected_task(tmp_path):
    write(tmp_path, auto_rows())
    write(tmp_path, auto_rows("unrelated"), "unrelated-1.jsonl")
    write(tmp_path, auto_rows("unrelated"), "unrelated-2.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "complete"


def test_related_duplicate_metadata_fails_closed(tmp_path):
    write(tmp_path, auto_rows())
    write(tmp_path, auto_rows("child", "root"), "child-1.jsonl")
    write(tmp_path, auto_rows("child", "root"), "child-2.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "unknown"
    assert "duplicate_session_metadata" in result["issues"]


def paginated_rows(tmp_path, rows, split=3):
    """Desktop continuation binds an exact prefix, not the old file's tail."""
    import copy
    base = copy.deepcopy(rows[:split])
    base[0]["payload"]["history_mode"] = "paginated"
    prefix = ("\n".join(json.dumps(row) for row in base) + "\n").encode()
    first = tmp_path / "base.jsonl"
    first.write_bytes(prefix)
    meta = copy.deepcopy(base[0])
    meta["payload"].update(timestamp="2026-09-05T00:00:01Z", history_base={
        "thread_id": rows[0]["payload"]["id"], "end_ordinal_exclusive": len(base),
        "end_byte_offset": len(prefix)})
    second = write(tmp_path, [meta, *copy.deepcopy(rows[split:])], "continuation.jsonl")
    return first, second


def test_paginated_turn_and_child_count_once_and_ignore_unbound_tail(tmp_path):
    first, _ = paginated_rows(tmp_path, auto_rows())
    with first.open("a", encoding="utf-8") as stream:
        stream.write("NOT PART OF THE BOUND HISTORY\n")
    write(tmp_path, auto_rows("child", "root"), "child.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "complete", result["issues"]
    assert sum(a["usage"]["total_tokens"] for a in result["attempts"]) == 26
    assert result["child_thread_ids"] == ["child"]
    assert result["elapsed_seconds"] == 2


def test_paginated_completed_turn_in_base_remains_collectible(tmp_path):
    rows = auto_rows()
    paginated_rows(tmp_path, rows, len(rows))
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "complete", result["issues"]
    assert len(result["attempts"]) == 1


@pytest.mark.parametrize("mutation", ["offset", "ordinal", "foreign", "ancestry", "missing_base"])
def test_paginated_invalid_history_cannot_claim_complete(tmp_path, mutation):
    first, second = paginated_rows(tmp_path, auto_rows(), split=1)
    rows = [json.loads(line) for line in second.read_text().splitlines()]
    meta = rows[0]["payload"]
    if mutation == "offset":
        meta["history_base"]["end_byte_offset"] -= 1
    elif mutation == "ordinal":
        meta["history_base"]["end_ordinal_exclusive"] += 1
    elif mutation == "foreign":
        meta["history_base"]["thread_id"] = "other"
    elif mutation == "ancestry":
        meta["parent_thread_id"] = "other"
    else:
        first.unlink()
    write(tmp_path, rows, second.name)
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "unknown"
    assert any("paginated" in issue or "duplicate_session" in issue for issue in result["issues"])


def test_paginated_three_pages_preserve_turn_without_counting_headers(tmp_path):
    _, second = paginated_rows(tmp_path, auto_rows())
    rows = [json.loads(line) for line in second.read_text().splitlines()]
    prefix = ("\n".join(json.dumps(row) for row in rows[:2]) + "\n").encode()
    second.write_bytes(prefix)
    meta = json.loads(json.dumps(rows[0]))
    meta["payload"]["history_base"].update(end_ordinal_exclusive=5, end_byte_offset=len(prefix))
    write(tmp_path, [meta, rows[-1]], "third.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "complete", result["issues"]
    assert len(result["attempts"]) == 1


def test_paginated_competing_continuations_fail_closed(tmp_path):
    _, second = paginated_rows(tmp_path, auto_rows())
    (tmp_path / "competing.jsonl").write_bytes(second.read_bytes())
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "unknown"
    assert "duplicate_session_metadata" in result["issues"]


def test_unrelated_paginated_body_is_never_read(tmp_path):
    write(tmp_path, auto_rows())
    unrelated = tmp_path / "unrelated"
    unrelated.mkdir()
    first, second = paginated_rows(unrelated, auto_rows("other"))
    with second.open("a", encoding="utf-8") as stream:
        stream.write("\nPRIVATE UNRELATED BODY")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "complete"
    assert "PRIVATE" not in json.dumps(result)


def test_child_finishing_after_parent_extends_whole_task_elapsed(tmp_path):
    write(tmp_path, auto_rows())
    child = auto_rows("child", "root")
    child[-1]["timestamp"] = "2026-09-05T00:00:05Z"
    write(tmp_path, child, "child.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "complete"
    assert result["elapsed_seconds"] == 5


def test_active_child_does_not_inherit_parent_completed_duration(tmp_path):
    write(tmp_path, auto_rows())
    write(tmp_path, auto_rows("child", "root")[:-1], "child.jsonl")
    result = collect_desktop_task(tmp_path, "root", "turn")
    assert result["coverage"] == "unknown"
    assert result["elapsed_seconds"] is None


def test_desktop_output_observations_cover_both_native_shapes_without_claiming_intake(tmp_path):
    rows = rollout()
    rows[2]["payload"]["effort"] = "high"
    outputs = [
        ("function_call_output", "Discussion of truncation is not a warning."),
        ("custom_tool_call_output", [{"type": "input_text", "text": json.dumps({
            "wall_time_seconds": 0.1, "exit_code": 7,
            "output": "Warning: truncated output (original token count: 100)\nTotal output lines: 20"})}]),
        ("function_call_output", "Warning: truncated output (original token count: 300)\nOutput:"),
        ("custom_tool_call_output", {"future_shape": "unknown"}),
    ]
    rows[3:3] = [{"type": "response_item", "payload": {"type": kind, "output": output}}
                 for kind, output in outputs]
    result = collect(write(tmp_path, rows), expected_child_ids=[])
    assert result["tool_output_observations"] == {
        "output_events": 4, "truncation_marker_events": 2,
        "nonzero_command_exit_observations": 1, "unrecognized_output_events": 1}
    assert result["observed_settings"] == [{"model": "test-model", "effort": "high"}]
    # An observed tool failure may have been recovered; accounting stays separate.
    assert result["coverage"] == "complete"
    assert "intake_complete" not in result


def test_desktop_observations_exclude_unselected_turn_outputs(tmp_path):
    rows = rollout()
    rows += [{"type": "turn_context", "payload": {"turn_id": "other", "model": "other", "effort": "low"}},
             {"type": "response_item", "payload": {"type": "custom_tool_call_output",
              "output": "Warning: truncated output (original token count: 200)"}}]
    result = collect(write(tmp_path, rows), expected_child_ids=[])
    assert result["tool_output_observations"]["output_events"] == 0
    assert result["observed_settings"] == [{"model": "test-model", "effort": None}]
