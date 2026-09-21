"""A failed attempt and its successful retry are different costs, counted once."""
from harness_efficiency import normalize_usage
from reports.finite_failure_evidence import cost_breakdown


def attempt(root, relative, *, outcome="PROCESS_COMPLETED", startup=2, unknown=False):
    usage = None if unknown else {"input_tokens": 10, "cached_input_tokens": 4,
        "cache_write_input_tokens": 0, "output_tokens": 3, "reasoning_output_tokens": 1, "total_tokens": 13}
    return {"receipt_path": str(root / relative / "execution_receipt.json"), "outcome": outcome,
        "usage": normalize_usage("codex_exec", usage), "additional_observed_response_tokens": startup}


def test_costs_partition_success_repairs_failed_retry_and_report(tmp_path):
    native = {"attempts": [attempt(tmp_path, "formation/provider/attempt-1", outcome="PROCESS_FAILED"),
        attempt(tmp_path, "formation/provider/attempt-2"), attempt(tmp_path, "assessment/provider/a"),
        attempt(tmp_path, "finish/repair/definition/a"), attempt(tmp_path, "assessment-recheck/provider/a")], "issues": []}
    report = {"attempts": [attempt(tmp_path.parent, "report/provider/a")], "issues": []}
    value = cost_breakdown(native, tmp_path, report)
    assert value["coverage"] == "complete"
    assert value["complete_tokens_including_startup"] == 90
    assert {k: v["complete_tokens_including_startup"] for k, v in value["groups"].items()} == {
        "actual_process": 30, "semantic_repairs_and_rechecks": 30,
        "reporting": 15, "technical_failures_or_unknown_attempts": 15}
    assert sum(g["cached_input_tokens"] for g in value["groups"].values()) == 24
    assert sum(g["attempts"] for g in value["groups"].values()) == 6


def test_missing_attempt_cost_and_startup_are_not_zero(tmp_path):
    value = cost_breakdown({"attempts": [attempt(tmp_path, "answer/provider/a", unknown=True, startup=None)],
        "issues": []}, tmp_path)
    assert value["coverage"] == "unknown"
    assert value["complete_tokens_including_startup"] is None
    group = value["groups"]["actual_process"]
    assert group["unknown_usage_attempts"] == group["unknown_startup_attempts"] == 1
    assert group["complete_tokens_including_startup"] is None


def test_duplicate_receipt_never_inflates_total_or_claims_complete(tmp_path):
    source = {"attempts": [attempt(tmp_path, "answer/provider/a")], "issues": []}
    value = cost_breakdown(source, tmp_path, source)
    assert value["observed_tokens_including_startup"] == 15
    assert value["complete_tokens_including_startup"] is None
    assert value["issues"] == ["receipt_accounted_more_than_once"]


def test_missing_provider_scope_prevents_complete_bill(tmp_path):
    value = cost_breakdown({"attempts": [attempt(tmp_path, "answer/provider/a")],
        "issues": ["provider_root_missing:lost"]}, tmp_path)
    assert value["observed_tokens_including_startup"] == 15
    assert value["complete_tokens_including_startup"] is None
    assert value["groups"]["reporting"]["complete_tokens_including_startup"] is None
