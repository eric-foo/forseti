"""Explicit completed-run selection and union accounting; no economic inference."""
import math
from pathlib import Path

from harness_efficiency import TOKEN_FIELDS, aggregate_usage


def selection(value: dict, directory: Path) -> tuple[list[dict], list[dict]]:
    if not isinstance(value, dict) or set(value) - {"runs", "comparisons"}:
        raise ValueError("selection must contain runs and optional comparisons")
    runs = value.get("runs")
    if not isinstance(runs, list) or not runs:
        raise ValueError("selection requires a nonempty runs list")
    required = {"label", "thread_id", "turn_id", "workflow", "workload_id"}
    defaults = dict(configuration=None, revision=None, pair_id=None, quality_command=None, cwd=None, timeout_seconds=300)
    labels, identities, result = set(), set(), []
    for row in runs:
        if not isinstance(row, dict) or set(row) - required - set(defaults) or not required <= set(row):
            raise ValueError("each run requires label, thread_id, turn_id, workflow and workload_id; unsupported fields refused")
        if any(not isinstance(row[key], str) or not row[key].strip() for key in required):
            raise ValueError("run identifiers must be nonempty strings")
        identity = row["thread_id"], row["turn_id"]
        if row["label"] in labels or identity in identities:
            raise ValueError("duplicate run label or selected turn")
        labels.add(row["label"])
        identities.add(identity)
        item = {**defaults, **row}
        timeout = item["timeout_seconds"]
        if type(timeout) not in (int, float) or not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout_seconds must be finite and positive")
        for key in ("revision", "pair_id"):
            if item[key] is not None and (not isinstance(item[key], str) or not item[key]):
                raise ValueError(f"{key} must be a nonempty string")
        for key in ("configuration", "quality_command", "cwd"):
            if item[key] is not None:
                if not isinstance(item[key], str) or not item[key]:
                    raise ValueError(f"{key} must be a nonempty path string")
                item[key] = str((directory / item[key]).resolve())
        result.append(item)
    comparisons = value.get("comparisons", [])
    if not isinstance(comparisons, list):
        raise ValueError("comparisons must be a list")
    names = set()
    for row in comparisons:
        if not isinstance(row, dict) or set(row) != {"label", "baseline", "candidate"}:
            raise ValueError("comparison requires label, baseline and candidate")
        if not isinstance(row["label"], str) or not row["label"] or row["label"] in names:
            raise ValueError("comparison labels must be nonempty and unique")
        names.add(row["label"])
        for arm in ("baseline", "candidate"):
            if not isinstance(row[arm], list) or not row[arm] or any(not isinstance(label, str) or label not in labels for label in row[arm]):
                raise ValueError("comparison arms must name selected runs")
    return result, comparisons


def reconcile_runs(records: dict[str, dict], *, uncollected: list[str]) -> dict:
    unique, duplicates, conflicts, issues = {}, 0, [], []
    for label, record in records.items():
        if record["usage"]["coverage"] != "complete":
            issues.append(f"{label}:incomplete_usage")
        for index, attempt in enumerate(record["attempts"]):
            key = tuple(attempt.get(name) for name in ("thread_id", "turn_id", "response_id"))
            if any(not isinstance(part, str) or not part for part in key):
                issues.append(f"{label}:unidentified_response")
                key = (label, index, None)
            if key in unique:
                if unique[key] != attempt:
                    conflicts.append(list(key))
                else:
                    duplicates += 1
            else:
                unique[key] = attempt
    usage = aggregate_usage(list(unique.values()))
    if issues or uncollected or conflicts:
        usage.update(coverage="unknown", **dict.fromkeys(TOKEN_FIELDS))
        usage["issues"] += issues + [f"{label}:uncollected" for label in uncollected]
        if conflicts:
            usage["issues"].append("conflicting_duplicate_response")
            # Even an observed lower bound would depend on which conflicting
            # observation happened to be first. Keep both source records instead.
            usage["observed_totals"] = dict.fromkeys(TOKEN_FIELDS)
    threads = {}
    for attempt in unique.values():
        thread = attempt.get("thread_id")
        if isinstance(thread, str):
            threads.setdefault(thread, []).append(attempt)
    return {"scope": "union of explicitly selected completed runs and their discovered descendants",
            "usage": usage, "unique_model_responses": sum(key[2] is not None for key in unique),
            "duplicate_response_observations": duplicates, "conflicts": conflicts, "uncollected": uncollected,
            "threads": {thread: {"observed_usage": None if conflicts else aggregate_usage(attempts),
                                  "model_responses": sum(isinstance(a.get("response_id"), str) for a in attempts)}
                        for thread, attempts in threads.items()},
            "elapsed_scope": "per-run intervals retained; overlapping durations are not added"}
