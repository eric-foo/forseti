"""Bounded, content-free Codex telemetry collection (no model calls).

Exec JSON is accepted only for one declared fresh invocation. Desktop rollout
records use response usage, never sums of cumulative token_count snapshots.
Desktop schema was probed on Codex Desktop 0.153.1; exec schema reference:
https://github.com/openai/codex/blob/main/codex-rs/exec/src/exec_events.rs
Unknown child coverage is deliberately different from an empty child set.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from harness_efficiency import normalize_usage, aggregate_usage

TOKEN_KEYS = ("input_tokens", "cached_input_tokens", "cache_write_input_tokens",
              "output_tokens", "reasoning_output_tokens", "total_tokens")
CHILD_TOOLS = {"spawn_agent", "followup_task", "send_input", "create_thread",
               "send_message_to_thread", "fork_thread"}


def collect_provider_roots(roots, *, started_at=None, resolve_path=Path):
    """Account selected immutable native attempts, including incomplete launches.

    Existing receipts may be reused by a resumed command. Their costs are
    preserved history, not fresh generation or model-supervision savings.
    Only trace_safe numeric counters are inspected; log_only is never copied.
    """
    from harness_utils import hash_file
    directories, intents, retries, issues = set(), set(), set(), []
    for raw in roots:
        root = Path(raw).resolve()
        if not root.is_dir():
            issues.append(f"provider_root_missing:{root}")
            continue
        directories.update(p.parent for p in root.rglob("execution_started.json"))
        directories.update(p.parent for p in root.rglob("execution_receipt.json"))
        for path in root.rglob("launch-*.json"):
            intents.add(path)
            if path.name != "launch-001.json":
                retries.add(path)
        for path in root.rglob("recovery-*.json"):
            retries.add(path)
            try:
                directories.add(resolve_path(json.loads(path.read_text(encoding="utf-8"))["attempt_dir"]).resolve())
            except (ValueError, OSError, KeyError):
                issues.append(f"invalid_recovery_record:{path}")
    for intent in intents:
        try:
            policy = json.loads((intent.parent / "binding.json").read_text(encoding="utf-8"))
            aid = json.loads(intent.read_text(encoding="utf-8"))["attempt_id"]
            directories.add(resolve_path(Path(policy["attempt_root"]) / aid).resolve())
        except (ValueError, OSError, KeyError):
            issues.append(f"unresolved_launch_intent:{intent}")
    attempts, additional = [], 0
    diagnostic_unknown = 0
    for directory in sorted(directories):
        path = directory / "execution_receipt.json"
        entry = {"receipt_path": str(path), "outcome": "unknown", "usage": normalize_usage("codex_exec", None),
                 "issues": [], "execution_scope": "unknown", "additional_observed_response_tokens": None}
        try:
            receipt = json.loads(path.read_text(encoding="utf-8"))
            if receipt.get("schema_version") != "forseti_provider_execution_receipt_v1":
                raise ValueError("unknown receipt schema")
            for filename, field in (("events.jsonl", "events_sha256"), ("stderr.log", "stderr_sha256")):
                if hash_file(directory / filename) != receipt[field]:
                    raise ValueError("diagnostic hash mismatch")
            if receipt.get("response_sha256") and hash_file(directory / "response.json") != receipt["response_sha256"]:
                raise ValueError("response hash mismatch")
            summary = collect_codex_exec(directory / "events.jsonl", fresh_session=True)
            entry.update(outcome=receipt["outcome"], receipt_sha256=hash_file(path),
                         usage=normalize_usage("codex_exec", _raw(receipt.get("usage"))),
                         observed_retry_events=receipt.get("observed_retry_events"),
                         execution_scope="preserved_prior_execution" if started_at and receipt["started_at"] < started_at else
                                         "current_operation_interval" if started_at else "selected_receipt_history")
            event_usage = aggregate_usage(summary["attempts"])
            if (entry["usage"]["total_tokens"] != event_usage["total_tokens"] or summary["coverage"] != "complete"):
                entry["usage"]["coverage"] = "unknown"
                entry["usage"]["issues"].append("native_event_usage_incomplete_or_mismatch")
            observations = []
            with (directory / "stderr.log").open(encoding="utf-8", errors="replace") as stream:
                for line in stream:
                    if "codex_otel.trace_safe:" not in line or "event.kind=response.completed " not in line:
                        continue
                    fields = dict(re.findall(r"\b(input_token_count|output_token_count)=(\d+)\b", line))
                    if len(fields) == 2:
                        observations.append((int(fields["input_token_count"]), int(fields["output_token_count"])))
            pair = (entry["usage"]["input_tokens"], entry["usage"]["output_tokens"])
            # Admit extra startup only with one exactly overlapping completed-turn
            # response and preceding zero-output responses. Other shapes stay unknown.
            if (observations and observations[-1] == pair and observations.count(pair) == 1
                    and all(output == 0 for _, output in observations[:-1])):
                entry["additional_observed_response_tokens"] = sum(inp for inp, _ in observations[:-1])
            if receipt["outcome"] != "PROCESS_COMPLETED":
                entry["issues"].append("provider_attempt_not_completed")
        except (OSError, ValueError, KeyError, TypeError):
            entry["issues"].append("native_receipt_missing_invalid_or_changed")
        if entry["additional_observed_response_tokens"] is None:
            diagnostic_unknown += 1
        else:
            additional += entry["additional_observed_response_tokens"]
        attempts.append(entry)
    usage = aggregate_usage(attempts)
    unknown = sum(a["usage"]["coverage"] != "complete" for a in attempts)
    issues.extend(issue for a in attempts for issue in a["issues"])
    if roots and not attempts:
        issues.append("selected_provider_scope_has_no_attempts")
    # The compact closeout keeps this summary but drops the per-attempt rows, so
    # the scope split has to survive here; otherwise the one merged total above
    # reads as the current operation's cost even when it carries replayed
    # receipts. Unknown coverage stays unknown per scope, as in the merged total.
    scopes = {}
    for scope in sorted({a["execution_scope"] for a in attempts}):
        selected = [a for a in attempts if a["execution_scope"] == scope]
        aggregate = aggregate_usage(selected)
        scopes[scope] = {"attempts": len(selected), "coverage": aggregate["coverage"],
                         "total_tokens": aggregate["total_tokens"],
                         "observed_total_tokens": aggregate["observed_totals"]["total_tokens"],
                         "additional_observed_response_tokens": sum(
                             a["additional_observed_response_tokens"] or 0 for a in selected),
                         "startup_observation_unknown_attempts": sum(
                             a["additional_observed_response_tokens"] is None for a in selected)}
    return {"attempts": attempts, "attempt_count": len(attempts), "usage": usage,
            "usage_by_execution_scope": scopes,
            "unknown_usage_attempts": unknown, "retry_claims_observed": len(retries),
            "observed_retry_events": sum(a.get("observed_retry_events") or 0 for a in attempts),
            "additional_observed_response_tokens": additional,
            "startup_observation_unknown_attempts": diagnostic_unknown,
            "issues": sorted(set(issues)),
            "scope": "selected native receipts only; cached input/reasoning output are subsets; additional observed startup is separate; hidden requests and parent active-turn costs are not closed"}


def _stamp(value: Any) -> datetime | None:
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return result if result.tzinfo is not None else None
    except (AttributeError, TypeError, ValueError):
        return None


def _events(path: str | Path) -> tuple[list[dict], list[str]]:
    """Read only caller-selected files; never discover unrelated histories."""
    rows, issues = [], []
    try:
        with Path(path).open(encoding="utf-8-sig") as stream:
            for index, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                    if not isinstance(row, dict):
                        raise ValueError("not an object")
                    rows.append(row)
                except (ValueError, TypeError):
                    issues.append(f"invalid_json_row:{index}")
    except OSError:
        issues.append("source_unreadable")
    return rows, issues


def _raw(usage: Any) -> dict:
    if not isinstance(usage, dict):
        return {}
    return {key: usage[key] for key in TOKEN_KEYS if key in usage}


def _attempt(usage: Any, *, model: str | None = None, outcome: str = "success",
             provider: str = "codex_exec",
             **metadata: Any) -> dict:
    return {"provider": provider, "model": model, "elapsed_seconds": None,
            "outcome": outcome, "usage": normalize_usage(provider, _raw(usage)),
            **metadata}


def _summary(attempts: list[dict], issues: list[str], **metadata: Any) -> dict:
    if not attempts:
        issues.append("usage_missing")
    if any(item["usage"].get("coverage") != "complete" for item in attempts):
        issues.append("attempt_usage_incomplete")
    return {"attempts": attempts, "coverage": "unknown" if issues else "complete",
            "issues": sorted(set(issues)), **metadata}


def collect_codex_exec(path: str | Path, *, fresh_session: bool = False,
                       model: str | None = None) -> dict:
    """Collect a single fresh exec JSON stream, excluding prompt/output content.

    More than one turn, resume, failure, truncation, or observed delegation leaves
    whole-task coverage unknown. A CLI turn has no per-provider-request count;
    its attempt is explicitly a turn aggregate.
    """
    rows, issues = _events(path)
    attempts, threads, children = [], set(), set()
    tools: Counter[str] = Counter()
    item_ids: dict[str, dict] = {}
    starts = completions = 0
    active = False
    if not fresh_session:
        issues.append("fresh_session_not_established")
    for row in rows:
        kind = row.get("type")
        if kind == "thread.started":
            if isinstance(row.get("thread_id"), str):
                threads.add(row["thread_id"])
            else:
                issues.append("thread_id_missing")
        elif kind == "turn.started":
            if active:
                issues.append("overlapping_turns")
            starts += 1
            active = True
        elif kind == "turn.completed":
            if not active:
                issues.append("duplicate_or_unstarted_completion")
                continue
            active = False
            completions += 1
            attempts.append(_attempt(row.get("usage"), model=model,
                                     accounting_unit="exec_turn"))
        elif kind in {"turn.failed", "error"}:
            issues.append("execution_failed")
            if kind == "turn.failed":
                active = False
                attempts.append(_attempt(None, model=model, outcome="failed",
                                         accounting_unit="exec_turn"))
        elif kind in {"item.started", "item.updated", "item.completed"}:
            item = row.get("item")
            if not isinstance(item, dict):
                issues.append("invalid_item")
                continue
            item_type = item.get("type")
            if item_type == "collab_tool_call":
                issues.append("child_usage_not_in_exec_stream")
                children.update(x for x in item.get("receiver_thread_ids", [])
                                if isinstance(x, str))
            if kind == "item.completed":
                item_id = item.get("id")
                if not isinstance(item_id, str):
                    issues.append("item_id_missing")
                    continue
                # Compare safe metadata only: content never enters the report.
                safe = {"type": item_type, "status": item.get("status"),
                        "exit_code": item.get("exit_code")}
                if item_id in item_ids:
                    if item_ids[item_id] != safe:
                        issues.append("conflicting_item_duplicate")
                    continue
                item_ids[item_id] = safe
                if item_type in {"command_execution", "mcp_tool_call", "web_search",
                                 "collab_tool_call", "file_change"}:
                    tools[str(item_type)] += 1
    if starts != 1 or completions != 1 or active:
        issues.append("single_completed_turn_required")
    if len(threads) != 1:
        issues.append("single_thread_required")
    return _summary(attempts, issues, source_kind="codex_exec_json",
                    thread_ids=sorted(threads), child_thread_ids=sorted(children),
                    tools=dict(tools), child_coverage="unknown" if children or
                    "child_usage_not_in_exec_stream" in issues else "no_collab_events_observed",
                    model_source="caller_configuration" if model else "unavailable")


def _observe_tool_output(output: Any, counts: Counter) -> None:
    """Content-free observations, never a claim that model intake was complete.

    Desktop retains both plain output strings and lists of text fragments.
    Exact wrapper markers can also be quoted by a tool: they nominate inspection,
    while the workload's checker owns complete/exact intake validation.
    """
    counts["output_events"] += 1
    if isinstance(output, str):
        parts = [output]
    elif isinstance(output, list) and all(isinstance(p, dict) and
            p.get("type") in {"input_text", "text"} and isinstance(p.get("text"), str)
            for p in output):
        parts = [p["text"] for p in output]
    else:
        counts["unrecognized_output_events"] += 1
        return
    marker = False
    for part in parts:
        marker |= bool(re.search(r"(?:^|\n)Warning: truncated output \(original token count: [0-9]+\)", part))
        try:
            envelope = json.loads(part)
        except (ValueError, TypeError):
            continue
        # Read only the known command-result envelope, not arbitrary JSON data.
        if (isinstance(envelope, dict) and
                {"wall_time_seconds", "exit_code", "output"} <= envelope.keys()):
            code = envelope["exit_code"]
            if type(code) is int and code != 0:
                counts["nonzero_command_exit_observations"] += 1
            body = envelope["output"]
            if isinstance(body, str):
                marker |= body.startswith("Warning: truncated output (original token count: ")
    counts["truncation_marker_events"] += int(marker)


def collect_codex_rollouts(paths: Iterable[str | Path], *,
                           selected_turns: dict[str, list[str]],
                           root_thread_id: str,
                           expected_child_ids: list[str] | None = None,
                           parent_links: dict[str, str] | None = None,
                           _snapshots: dict | None = None) -> dict:
    """Collect explicitly selected complete Desktop turns and explicit children.

    ``expected_child_ids=None`` means the child inventory is unknown; [] is an
    explicit no-children boundary. Parent links are caller-supplied provenance,
    never inferred from tokens. Delegation with an empty inventory fails closed.
    Every child's selected turns must independently satisfy the same gates.
    Files are read once, giving a fixed collection snapshot. For an in-progress
    turn take a new snapshot after completion; partial snapshots cannot pass.
    """
    issues, attempts = [], []
    tools: Counter[str] = Counter()
    diagnostics = Counter(output_events=0, truncation_marker_events=0,
                          nonzero_command_exit_observations=0, unrecognized_output_events=0)
    settings = set()
    sources: dict[str, list[dict]] = {}
    versions = set()
    delegation_seen = False
    if expected_child_ids is None:
        issues.append("child_inventory_unknown")
    expected = set(expected_child_ids or [])
    links = parent_links or {}
    expected_threads = expected | {root_thread_id}
    if set(selected_turns) != expected_threads:
        issues.append("selected_threads_do_not_match_child_inventory")
    for child in expected:
        seen = {child}
        parent = links.get(child)
        while parent in expected and parent not in seen:
            seen.add(parent)
            parent = links.get(parent)
        if parent != root_thread_id:
            issues.append("child_parent_link_missing_or_invalid")
    for path in paths:
        rows, read_issues = (_snapshots[str(path)] if _snapshots is not None else _events(path))
        issues.extend(read_issues)
        meta = [row.get("payload", {}) for row in rows if row.get("type") == "session_meta"]
        if len(meta) != 1 or not isinstance(meta[0], dict) or not meta[0].get("id"):
            issues.append("session_metadata_missing_or_ambiguous")
            continue
        thread = meta[0]["id"]
        if thread not in expected_threads:
            issues.append("unexpected_thread_source")
            continue
        if thread in sources:
            issues.append("duplicate_thread_source")
            continue
        sources[thread] = rows
        if isinstance(meta[0].get("cli_version"), str):
            versions.add(meta[0]["cli_version"])
    if set(sources) != expected_threads:
        issues.append("thread_source_missing")
    for thread, rows in sources.items():
        wanted = set(selected_turns.get(thread, []))
        if not wanted:
            issues.append("selected_turns_missing")
            continue
        records: dict[str, dict[str, dict]] = {turn: {} for turn in wanted}
        totals: dict[str, dict] = {}
        starts, ends, contexts = {}, {}, {}
        current = None
        for row in rows:
            payload = row.get("payload", {})
            if not isinstance(payload, dict):
                issues.append("invalid_payload")
                continue
            kind = row.get("type")
            turn = payload.get("turn_id")
            if kind == "turn_context":
                current = turn
                if turn in wanted:
                    contexts[turn] = payload.get("model")
                    model, effort = payload.get("model"), payload.get("effort")
                    settings.add((model if isinstance(model, str) else None,
                                  effort if isinstance(effort, str) else None))
            elif kind == "event_msg" and payload.get("type") == "task_started":
                current = turn
                if turn in wanted:
                    starts[turn] = row.get("timestamp")
            elif kind == "event_msg" and payload.get("type") == "task_complete":
                if turn in wanted:
                    ends[turn] = payload.get("duration_ms")
            elif kind == "event_msg" and payload.get("type") in {"turn_aborted", "error"}:
                if (turn or current) in wanted:
                    issues.append("selected_turn_failed_or_aborted")
            elif kind == "response_item" and current in wanted:
                if payload.get("type") in {"function_call", "custom_tool_call"}:
                    name = payload.get("name")
                    if isinstance(name, str):
                        tools[name] += 1
                        short_name = name.split(".")[-1].strip("_")
                        delegation_seen |= short_name in CHILD_TOOLS
                elif payload.get("type") in {"function_call_output", "custom_tool_call_output"}:
                    _observe_tool_output(payload.get("output"), diagnostics)
            elif kind == "token_usage_record" and (not isinstance(turn, str) or not turn):
                if current is None or current in wanted:
                    issues.append("usage_turn_missing")
            elif kind == "token_usage_record" and turn in wanted:
                if payload.get("thread_id") != thread:
                    issues.append("usage_thread_mismatch")
                    continue
                response = payload.get("response_id")
                raw = _raw(payload.get("usage"))
                if not isinstance(response, str) or not response:
                    issues.append("response_id_missing")
                    continue
                if response in records[turn]:
                    if records[turn][response] != raw:
                        issues.append("conflicting_response_duplicate")
                    continue
                records[turn][response] = raw
                cumulative = _raw(payload.get("turn_token_usage"))
                previous = totals.get(turn, {})
                for key in TOKEN_KEYS:
                    values = [usage.get(key) for usage in records[turn].values()]
                    if all(type(value) is int and value >= 0 for value in values):
                        if cumulative.get(key) != sum(values):
                            issues.append("turn_cumulative_reconciliation_failed")
                        if (type(previous.get(key)) is int and
                                type(cumulative.get(key)) is int and
                                cumulative[key] < previous[key]):
                            issues.append("cumulative_counter_regressed")
                    else:
                        issues.append("response_usage_field_missing_or_invalid")
                totals[turn] = cumulative
        for turn in sorted(wanted):
            if turn not in starts or turn not in ends:
                issues.append("turn_boundary_incomplete")
            if not records[turn]:
                issues.append("turn_usage_missing")
                attempts.append(_attempt(None, model=contexts.get(turn),
                                         provider="codex_rollout",
                                         thread_id=thread, turn_id=turn,
                                         accounting_unit="desktop_response"))
            for response, raw in records[turn].items():
                attempts.append(_attempt(raw, model=contexts.get(turn),
                                         provider="codex_rollout",
                                         thread_id=thread, turn_id=turn,
                                         response_id=response,
                                         accounting_unit="desktop_response"))
    if delegation_seen and not expected:
        issues.append("observed_delegation_missing_children")
    return _summary(attempts, issues, source_kind="codex_desktop_rollout",
                    thread_ids=sorted(sources), child_thread_ids=sorted(expected),
                    tools=dict(tools), cli_versions=sorted(versions),
                    observed_settings=[{"model": model, "effort": effort}
                                       for model, effort in sorted(settings, key=repr)],
                    tool_output_observations=dict(diagnostics),
                    child_coverage="caller_manifest" if expected_child_ids is not None
                    else "unknown", parent_links=links)


def discover_desktop_sessions(session_root: str | Path, root_thread_id: str | None,
                              *, agent_path: str | None = None) -> dict:
    """Inventory first-row metadata only, recursively inside an explicit folder.

    Only matched root/descendant paths are returned. No unrelated conversation
    bodies are read. The caller supplies the date folder(s) covering the task;
    missing parent source or invalid metadata makes discovery incomplete.
    """
    metas, issues, duplicates = {}, [], []
    root = Path(session_root)
    if not root.is_dir():
        return {"sessions": {}, "issues": ["session_directory_missing"]}
    for path in sorted(root.rglob("*.jsonl")):
        try:
            with path.open(encoding="utf-8-sig") as stream:
                row = json.loads(stream.readline())
            payload = row.get("payload", {})
            if row.get("type") != "session_meta" or not isinstance(payload, dict):
                raise ValueError("metadata missing")
            ident = payload.get("id")
            if not isinstance(ident, str) or not ident:
                raise ValueError("metadata identifier missing")
            source = payload.get("source")
            subagent = source.get("subagent", {}) if isinstance(source, dict) else {}
            spawn = subagent.get("thread_spawn", {}) if isinstance(subagent, dict) else {}
            if not isinstance(spawn, dict):
                spawn = {}
            parent = payload.get("parent_thread_id") or spawn.get("parent_thread_id")
            if ident in metas:
                duplicates.append((ident, parent))
                continue
            metas[ident] = {"path": str(path), "parent_thread_id": parent,
                            "agent_path": payload.get("agent_path") or spawn.get("agent_path"),
                            "timestamp": payload.get("timestamp"),
                            "source_kind": subagent.get("other", "thread_spawn")
                            if isinstance(source, dict) and isinstance(subagent, dict) else source}
        except (OSError, ValueError, AttributeError):
            issues.append("session_metadata_unreadable")
    if agent_path is not None:
        matches = [ident for ident, meta in metas.items() if meta.get("agent_path") == agent_path]
        if len(matches) != 1:
            return {"sessions": {}, "issues": sorted(set(issues + ["agent_path_missing_or_ambiguous"]))}
        root_thread_id = matches[0]
    linked = {root_thread_id}
    while True:
        more = {ident for ident, meta in metas.items() if meta["parent_thread_id"] in linked}
        more.update(ident for ident, parent in duplicates if parent in linked)
        if more <= linked:
            break
        linked.update(more)
    if root_thread_id not in metas:
        issues.append("root_session_missing")
    if any(ident in linked for ident, _ in duplicates):
        issues.append("duplicate_session_metadata")
    return {"sessions": {ident: metas[ident] for ident in sorted(linked) if ident in metas},
            "issues": sorted(set(issues)), "root_thread_id": root_thread_id}


def _nested_task_selection(sessions: dict, snapshots: dict, root: str, turn: str,
                           billing_roots: set[str]) -> tuple[dict, list[str]]:
    """Bind fresh child turns to selected launches, not a shared ancestor's bill.

    Reused children require a more precise turn binding than Desktop currently
    exposes in protected follow-up arguments. Keep those cases unknown rather
    than guessing from overlapping timestamps or silently dropping requests.
    """
    selected, issues, visited = {root: [turn]}, [], set()
    if len(billing_roots) != 1:
        issues.append("nested_root_attribution_ambiguous")
    bounds = {}
    for thread, meta in sessions.items():
        starts, ends = {}, {}
        for row in snapshots[meta["path"]][0]:
            p = row.get("payload", {})
            if row.get("type") == "event_msg" and isinstance(p, dict):
                if p.get("type") == "task_started":
                    starts[p.get("turn_id")] = _stamp(row.get("timestamp"))
                elif p.get("type") == "task_complete":
                    ends[p.get("turn_id")] = _stamp(row.get("timestamp"))
        bounds[thread] = {key: (began, ends.get(key)) for key, began in starts.items()
                          if isinstance(key, str)}

    def created_in(parent, parent_turn, child):
        began, ended = bounds[parent].get(parent_turn, (None, None))
        created = _stamp(sessions[child].get("timestamp"))
        return (began is not None and created is not None and created >= began
                and (ended is None or created <= ended))

    while set(selected) - visited:
        parent = sorted(set(selected) - visited)[0]
        visited.add(parent)
        current, pending, launched = None, {}, {}
        for row in snapshots[sessions[parent]["path"]][0]:
            p = row.get("payload", {})
            if not isinstance(p, dict):
                continue
            if row.get("type") == "turn_context" or (row.get("type") == "event_msg"
                    and p.get("type") == "task_started"):
                current = p.get("turn_id")
            if row.get("type") != "response_item":
                continue
            name = p.get("name", "").split(".")[-1]
            if current in selected[parent] and p.get("type") == "function_call":
                if name == "spawn_agent":
                    pending[p.get("call_id")] = current
                elif name in CHILD_TOOLS:
                    issues.append("nested_followup_turn_binding_unavailable")
            elif p.get("type") == "function_call_output" and p.get("call_id") in pending:
                owner_turn = pending.pop(p["call_id"])
                try:
                    receipt = json.loads(p.get("output", ""))
                except (TypeError, ValueError):
                    receipt = {}
                task_name = receipt.get("task_name") if isinstance(receipt, dict) else None
                matches = [key for key, meta in sessions.items() if isinstance(task_name, str)
                           and meta.get("agent_path") == task_name and meta.get("parent_thread_id") == parent]
                if len(matches) != 1:
                    issues.append("spawn_receipt_child_usage_missing_or_ambiguous")
                else:
                    launched[matches[0]] = owner_turn
        if pending:
            issues.append("spawn_receipt_missing")
        # Runtime-owned guardians have source metadata rather than model launch calls.
        for child, meta in sessions.items():
            owners = [t for t in selected[parent] if meta.get("parent_thread_id") == parent
                      and meta.get("source_kind") == "guardian" and created_in(parent, t, child)]
            if len(owners) == 1:
                launched[child] = owners[0]
        for child, owner_turn in launched.items():
            if not created_in(parent, owner_turn, child):
                issues.append("nested_spawn_session_not_fresh")
                continue
            # Usage rows without a started turn must not vanish from the selection.
            usage_rows = [row["payload"] for row in snapshots[sessions[child]["path"]][0]
                          if row.get("type") == "token_usage_record" and isinstance(row.get("payload"), dict)]
            if any(not isinstance(p.get("turn_id"), str) or not p["turn_id"] for p in usage_rows):
                issues.append("nested_child_usage_turn_missing")
            turns = sorted(set(bounds[child]) | {p["turn_id"] for p in usage_rows
                                                if isinstance(p.get("turn_id"), str) and p["turn_id"]})
            if len(turns) != 1:
                issues.append("nested_child_turn_binding_ambiguous")
            created = _stamp(sessions[child].get("timestamp"))
            if any(bounds[child].get(t, (None,))[0] is None or bounds[child][t][0] < created
                   for t in turns):
                issues.append("nested_child_start_precedes_launch")
            selected[child] = turns
            attributed = {p.get("root_turn_id") for row in snapshots[sessions[child]["path"]][0]
                          if row.get("type") == "token_usage_record"
                          and isinstance(p := row.get("payload"), dict) and p.get("turn_id") in turns}
            if not attributed or None in attributed:
                issues.append("child_turn_root_attribution_missing")
            elif attributed != billing_roots:
                issues.append("nested_child_root_attribution_conflict")
    for child, meta in sessions.items():
        parent = meta.get("parent_thread_id")
        # Unknown creation time cannot prove a child predates the selected turn.
        if child not in selected and parent in selected and (
                _stamp(meta.get("timestamp")) is None
                or any(created_in(parent, t, child) for t in selected[parent])):
            issues.append("nested_child_launch_binding_missing")
    return selected, issues


def collect_desktop_task(session_root: str | Path, root_thread_id: str | None = None,
                         turn_id: str | None = None, *, agent_path: str | None = None) -> dict:
    """Collect one Desktop root turn plus automatically linked child/guardian work.

    Root-turn attribution comes from observed token_usage_record.root_turn_id.
    A nested selected task shares its ancestor's billing turn, so its fresh
    workers additionally require observed launch/ancestry and turn bindings.
    Unattributed child turns overlapping the root interval remain unknown. The
    same snapshots feed selection and counting, so a growing rollout cannot
    silently change which requests are included between the two operations.
    """
    if agent_path is not None and (root_thread_id is not None or turn_id is not None):
        raise ValueError("select an agent path or explicit thread and turn, not both")
    if agent_path is None and (root_thread_id is None or turn_id is None):
        raise ValueError("supply an agent path or both thread and turn")
    inventory = discover_desktop_sessions(session_root, root_thread_id, agent_path=agent_path)
    root_thread_id = inventory.get("root_thread_id", root_thread_id)
    sessions = inventory["sessions"]
    issues = list(inventory["issues"])
    snapshots = {meta["path"]: _events(meta["path"]) for meta in sessions.values()}
    root_meta = sessions.get(root_thread_id)
    if root_meta is None:
        return _summary([], issues, source_kind="codex_desktop_rollout", thread_ids=[],
                        child_thread_ids=[], child_coverage="unknown", tools={})
    root_rows = snapshots[root_meta["path"]][0]
    if agent_path is not None:
        turns = {p.get("turn_id") for row in root_rows if isinstance(p := row.get("payload"), dict)
                 and (row.get("type") == "token_usage_record" or
                      (row.get("type") == "event_msg" and p.get("type") == "task_started"))}
        if len(turns) != 1 or not all(isinstance(t, str) and t for t in turns):
            return _summary([], issues + ["agent_turn_missing_or_ambiguous"],
                source_kind="codex_desktop_rollout", thread_ids=[root_thread_id],
                child_thread_ids=[], child_coverage="unknown", tools={})
        turn_id = next(iter(turns))
    start = end = None
    for row in root_rows:
        p = row.get("payload", {})
        if row.get("type") == "event_msg" and p.get("turn_id") == turn_id:
            if p.get("type") == "task_started":
                start = row.get("timestamp")
            elif p.get("type") == "task_complete":
                end = row.get("timestamp")
    selected = {root_thread_id: [turn_id]}
    start_time, end_time = _stamp(start), _stamp(end)
    billing_roots = {p["root_turn_id"] for row in root_rows
                     if row.get("type") == "token_usage_record"
                     and isinstance(p := row.get("payload"), dict) and p.get("turn_id") == turn_id
                     and isinstance(p.get("root_turn_id"), str)}
    nested = bool(root_meta.get("parent_thread_id")) and billing_roots != {turn_id}
    for thread, meta in sessions.items():
        if thread == root_thread_id or nested:
            continue
        rows, read_issues = snapshots[meta["path"]]
        # Descendants created after a finished root turn cannot belong to it.
        created_time = _stamp(meta.get("timestamp"))
        if end_time and created_time and created_time > end_time:
            continue
        attributed: dict[str, set[str]] = {}
        starts: dict[str, str | None] = {}
        for row in rows:
            p = row.get("payload", {})
            if not isinstance(p, dict):
                continue
            child_turn = p.get("turn_id")
            if not isinstance(child_turn, str):
                continue
            if row.get("type") == "token_usage_record":
                roots = attributed.setdefault(child_turn, set())
                if isinstance(p.get("root_turn_id"), str):
                    roots.add(p["root_turn_id"])
            elif row.get("type") == "event_msg" and p.get("type") == "task_started":
                starts[child_turn] = row.get("timestamp")
        wanted = {child_turn for child_turn, roots in attributed.items() if turn_id in roots}
        if any(len(attributed[child_turn]) != 1 for child_turn in wanted):
            issues.append("child_turn_has_ambiguous_root_attribution")
        for child_turn, began in starts.items():
            if attributed.get(child_turn):
                continue
            began_time = _stamp(began)
            if start_time is None or began_time is None or (began_time >= start_time and
                    (end_time is None or began_time <= end_time)):
                wanted.add(child_turn)
                issues.append("child_turn_root_attribution_missing")
        if read_issues or (not starts and not attributed):
            if start_time is None or created_time is None or created_time >= start_time:
                selected[thread] = []
                issues.append("child_usage_or_boundary_missing")
        if wanted:
            selected[thread] = sorted(wanted)
    if nested:
        selected, nested_issues = _nested_task_selection(
            sessions, snapshots, root_thread_id, turn_id, billing_roots)
        issues.extend(nested_issues)
    # Preserve ancestry even if an intermediate thread has no selected requests.
    for thread in list(selected):
        parent = sessions[thread].get("parent_thread_id")
        seen = {thread}
        while parent in sessions and parent != root_thread_id and parent not in seen:
            seen.add(parent)
            if parent not in selected:
                selected[parent] = []
                issues.append("intermediate_parent_usage_unattributed")
            parent = sessions[parent].get("parent_thread_id")
    paths = [sessions[thread]["path"] for thread in selected]
    # Actual Desktop spawn receipts contain a task_name rather than a UUID.
    # Match that name to observed session_meta.agent_path; never replace missing
    # child evidence with a launch-count heuristic (followups can reuse agents).
    for thread, turns in selected.items():
        current = None
        pending = set()
        for row in snapshots[sessions[thread]["path"]][0]:
            payload = row.get("payload", {})
            if not isinstance(payload, dict):
                continue
            if row.get("type") == "turn_context" or (row.get("type") == "event_msg" and
                    payload.get("type") == "task_started"):
                current = payload.get("turn_id")
            if row.get("type") != "response_item":
                continue
            if (current in turns and payload.get("type") == "function_call" and
                    payload.get("name", "").split(".")[-1] == "spawn_agent"):
                pending.add(payload.get("call_id"))
            elif payload.get("type") == "function_call_output" and payload.get("call_id") in pending:
                pending.remove(payload.get("call_id"))
                try:
                    receipt = json.loads(payload.get("output", ""))
                except (ValueError, TypeError):
                    receipt = {}
                task_name = receipt.get("task_name") if isinstance(receipt, dict) else None
                matches = [ident for ident, meta in sessions.items()
                           if meta.get("agent_path") == task_name and meta.get("parent_thread_id") == thread]
                if not isinstance(task_name, str) or len(matches) != 1 or matches[0] not in selected:
                    issues.append("spawn_receipt_child_usage_missing_or_ambiguous")
        if pending:
            issues.append("spawn_receipt_missing")
    links = {thread: sessions[thread]["parent_thread_id"] for thread in selected
             if thread != root_thread_id}
    result = collect_codex_rollouts(paths, selected_turns=selected,
        root_thread_id=root_thread_id, expected_child_ids=sorted(links),
        parent_links=links, _snapshots=snapshots)
    result["issues"] = sorted(set(result["issues"] + issues))
    result["coverage"] = "unknown" if result["issues"] else "complete"
    result["child_coverage"] = ("session_metadata_launch_receipts_and_turn_attribution" if nested
                                else "session_metadata_and_root_turn_attribution")
    result["selected_turns"] = selected
    result["source_kinds"] = {thread: sessions[thread]["source_kind"] for thread in selected}
    result["root_started_at"] = start
    result["root_completed_at"] = end
    completed_times = []
    selected_count = sum(len(turns) for turns in selected.values())
    for thread, turns in selected.items():
        completed = {}
        for row in snapshots[sessions[thread]["path"]][0]:
            payload = row.get("payload", {})
            if (row.get("type") == "event_msg" and isinstance(payload, dict) and
                    payload.get("type") == "task_complete" and payload.get("turn_id") in turns):
                completed[payload["turn_id"]] = _stamp(row.get("timestamp"))
        completed_times.extend(value for value in completed.values() if value is not None)
    workunit_end = max(completed_times) if len(completed_times) == selected_count else None
    result["workunit_completed_at"] = workunit_end.isoformat() if workunit_end else None
    result["elapsed_seconds"] = ((workunit_end - start_time).total_seconds()
                                 if start_time and end_time and workunit_end and
                                 workunit_end >= start_time else None)
    if result["elapsed_seconds"] is None:
        result["coverage"] = "unknown"
        result["issues"] = sorted(set(result["issues"] + ["root_elapsed_boundary_incomplete"]))
    result["observed_models"] = sorted({a["model"] for a in result["attempts"]
                                        if isinstance(a.get("model"), str)})
    return result
