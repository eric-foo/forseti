"""Keep CI and the local pre-push mirror mechanically aligned."""

from __future__ import annotations

import importlib
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
CI_PATH = REPO_ROOT / ".github" / "workflows" / "ci.yml"
PRE_PUSH_PATH = REPO_ROOT / ".agents" / "hooks" / "pre_push_guard.py"
HOOKS_DIR = REPO_ROOT / ".agents" / "hooks"
HARNESS_COUPLING_PATH = HOOKS_DIR / "check_harness_coupling.py"
CODEX_HOOKS_PATH = REPO_ROOT / ".codex" / "hooks.json"
CODEX_ADAPTER_PATH = REPO_ROOT / ".codex" / "hooks" / "forseti_guard_codex_adapter.py"
DECISION_ROUTING_PATH = REPO_ROOT / ".agents" / "workflow-overlay" / "decision-routing.md"
PROMPT_ORCHESTRATION_PATH = (
    REPO_ROOT / ".agents" / "workflow-overlay" / "prompt-orchestration.md"
)
PROMPT_GATE_PATH = REPO_ROOT / ".agents" / "hooks" / "check_prompt_output_mode.py"
HOOK_README_PATH = REPO_ROOT / ".agents" / "hooks" / "README.md"
HOOK_ADOPTION_ADOPTED = "FORSETI_CODEX_HOOK_ADOPTION=ADOPTED"
HOOK_ADOPTION_NOT_INTERCEPTED = "FORSETI_CODEX_HOOK_ADOPTION=NOT_INTERCEPTED"
EVENT_BASE_SHA = "1" * 40
DIFF_BASE_RESOLVERS = (
    ("check_source_input_hashes.py", "resolve_base_ref", False),
    ("check_harness_coupling.py", "resolve_base_ref", False),
    ("header_index.py", "resolve_base_ref", True),
    ("check_search_surface_google_route.py", "resolve_base", False),
    ("check_csb_scanning_artifact.py", "resolve_base_ref", False),
    ("check_ontology_tag_validity.py", "resolve_base_ref", False),
    ("check_deletion_evidence.py", "resolve_base_ref", False),
    ("check_dcp_receipt.py", "resolve_base_ref", False),
    ("check_review_routing.py", "resolve_base_ref", False),
    ("check_handoff_pointers.py", "resolve_base_ref", False),
    ("check_prompt_output_mode.py", "resolve_base_ref", False),
    ("check_review_summary.py", "resolve_base_ref", False),
    ("check_hash_pin_freshness.py", "resolve_base_ref", False),
    ("check_full_gt_claims.py", "resolve_base_ref", False),
)


def _load_pre_push_guard():
    spec = importlib.util.spec_from_file_location("pre_push_guard", PRE_PUSH_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_harness_coupling():
    spec = importlib.util.spec_from_file_location("check_harness_coupling", HARNESS_COUPLING_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_prompt_gate():
    spec = importlib.util.spec_from_file_location("check_prompt_output_mode", PROMPT_GATE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _ci_python_commands() -> list[str]:
    commands: list[str] = []
    for raw in CI_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("run: python "):
            commands.append(line.removeprefix("run: "))
        elif line.startswith("python "):
            commands.append(line)
    return commands


def test_ci_has_no_duplicate_python_commands() -> None:
    commands = _ci_python_commands()
    duplicates = sorted(command for command, count in Counter(commands).items() if count > 1)
    assert duplicates == []


def test_codex_live_hook_adoption_probe_fails_closed() -> None:
    config = json.loads(CODEX_HOOKS_PATH.read_text(encoding="utf-8"))
    pre_tool = config["hooks"]["PreToolUse"]
    matching_entries = [
        entry
        for entry in pre_tool
        if {"Bash", "PowerShell"} <= set(entry["matcher"].split("|"))
    ]
    assert len(matching_entries) == 1
    configured_hook = matching_entries[0]["hooks"][0]
    assert "forseti_guard_codex_adapter.py" in configured_hook["commandWindows"]

    direct = subprocess.run(
        [sys.executable, str(CODEX_ADAPTER_PATH), "--live-adoption-probe"],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=10,
    )
    assert direct.returncode == 3
    assert direct.stderr.strip() == HOOK_ADOPTION_NOT_INTERCEPTED

    event = {
        "tool_name": "PowerShell",
        "tool_input": {
            "command": (
                "python .codex/hooks/forseti_guard_codex_adapter.py "
                "--live-adoption-probe"
            )
        },
    }
    intercepted = subprocess.run(
        [sys.executable, str(CODEX_ADAPTER_PATH)],
        cwd=REPO_ROOT,
        input=json.dumps(event),
        text=True,
        capture_output=True,
        timeout=10,
    )
    denial = json.loads(intercepted.stdout)
    assert intercepted.returncode == 0
    assert denial["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert (
        denial["hookSpecificOutput"]["permissionDecisionReason"]
        == HOOK_ADOPTION_ADOPTED
    )


def test_one_time_binding_preserves_guard_and_limits_canary() -> None:
    routing = DECISION_ROUTING_PATH.read_text(encoding="utf-8")
    hook_readme = HOOK_README_PATH.read_text(encoding="utf-8")
    adapter = CODEX_ADAPTER_PATH.read_text(encoding="utf-8")
    probe_command = (
        "python .codex/hooks/forseti_guard_codex_adapter.py "
        "--live-adoption-probe"
    )

    assert "## One-Time Writable-Root Binding" in routing
    assert "revision_mode: exact | ancestor" in routing
    assert "`HEAD` equals `required_revision`" in routing
    assert "git merge-base --is-ancestor <required_revision> HEAD" in routing
    assert "sole writable root" in routing
    assert "synthetic file-write or Git-index probes" in routing
    assert "while that binding remains valid" in routing
    assert "ordinary work does not run that canary" in routing
    assert probe_command in hook_readme
    assert "only when hook adoption testing is itself" in hook_readme
    assert "lane-start writeability" not in adapter
    assert "already-authorized capable worktree-backed" in adapter


def test_implementation_commission_authorizes_one_immediate_managed_reroot() -> None:
    routing = DECISION_ROUTING_PATH.read_text(encoding="utf-8")
    prompt_contract = PROMPT_ORCHESTRATION_PATH.read_text(encoding="utf-8")

    for required in (
        "receiver_creation_authorization:",
        "authorization: create_exactly_one_fresh_codex_managed_worktree_task",
        "condition: current_task_not_receiver_verified",
        "initial_prompt: this_frozen_commission_verbatim",
        "dispatch: immediate_same_turn",
        "current_turn_authorization: read_only_scoping_only",
    ):
        assert required in prompt_contract

    assert "already-authorized capable worktree-backed task" in routing
    assert "read-only/scoping-only/review-only" in routing
    assert "Creating a user-visible Codex task still requires explicit product/user" in routing
    assert "do not create that authority" in routing


def test_managed_receiver_commission_gate_rejects_contradictions() -> None:
    gate = _load_prompt_gate()
    receiver = [
        "output_mode: paste-ready-chat",
        "edit_permission: implementation-authorized",
        "receiver_binding:",
        "  receiver_class: codex_managed_worktree",
        "  binding_state: receiver_to_verify",
        "  managed_starting_ref: origin/main",
        "  required_revision: 8cb44d080334453c384e39bc88fce510cbccfcde",
        "  revision_mode: ancestor",
    ]
    corrected_authorization = [
        "receiver_creation_authorization:",
        "  authorization: create_exactly_one_fresh_codex_managed_worktree_task",
        "  condition: current_task_not_receiver_verified",
        "  managed_starting_ref: origin/main",
        "  required_revision: 8cb44d080334453c384e39bc88fce510cbccfcde",
        "  revision_mode: ancestor",
        "  initial_prompt: this_frozen_commission_verbatim",
        "  dispatch: immediate_same_turn",
    ]

    defective = receiver + [
        "If this current task is not the receiver, stop; do not create another worktree.",
        "If the controlling prompt contract cannot be freshly loaded, fall back to project-owned prompt rules.",
    ]
    defective_findings = gate.evaluate_managed_receiver_lines("defective.md", defective)
    defective_kinds = {finding.kind for finding in defective_findings}
    assert "managed_receiver_creation_authorization_count" in defective_kinds
    assert "source_context_failure_not_typed" in defective_kinds
    assert "stale_source_fallback" in defective_kinds
    assert any("wrong-task stop" in finding.detail for finding in defective_findings)

    corrected = receiver + corrected_authorization + [
        "If a controlling source cannot be freshly loaded, declare SOURCE_CONTEXT_INCOMPLETE and stop.",
        "Do not manually create, discover, or target a Git worktree.",
        "Do not create a second receiver.",
    ]
    assert gate.evaluate_managed_receiver_lines("corrected.md", corrected) == []

    read_only = [line.replace("implementation-authorized", "read-only") for line in receiver]
    assert gate.evaluate_managed_receiver_lines("read_only.md", read_only) == []
    assert any(
        finding.kind == "receiver_creation_authority_on_read_only_commission"
        for finding in gate.evaluate_managed_receiver_lines(
            "read_only_bad.md", read_only + corrected_authorization
        )
    )

    manual = corrected + ["Run `git worktree add ../receiver origin/main` and continue there."]
    assert any(
        finding.kind == "manual_git_worktree_substitution"
        for finding in gate.evaluate_managed_receiver_lines("manual.md", manual)
    )

    mixed_clause_manual = corrected + [
        "Do not pause; run `git worktree add ../receiver origin/main` and continue there."
    ]
    assert any(
        finding.kind == "manual_git_worktree_substitution"
        for finding in gate.evaluate_managed_receiver_lines(
            "mixed_clause_manual.md", mixed_clause_manual
        )
    )

    mixed_clause_repeat = corrected + [
        "Do not wait; create another managed receiver task."
    ]
    assert any(
        finding.kind == "repeat_receiver_creation_authority"
        for finding in gate.evaluate_managed_receiver_lines(
            "mixed_clause_repeat.md", mixed_clause_repeat
        )
    )

    orphan_authorization = [
        "output_mode: paste-ready-chat",
        "edit_permission: implementation-authorized",
        *corrected_authorization,
    ]
    assert any(
        finding.kind == "managed_receiver_binding_count"
        for finding in gate.evaluate_managed_receiver_lines(
            "orphan_authorization.md", orphan_authorization
        )
    )

    conflicting_binding = corrected + [
        "receiver_binding:",
        "  receiver_class: codex_managed_worktree",
        "  binding_state: receiver_to_verify",
        "  managed_starting_ref: other/ref",
        "  required_revision: deadbeef",
        "  revision_mode: exact",
    ]
    assert any(
        finding.kind == "managed_receiver_binding_count"
        for finding in gate.evaluate_managed_receiver_lines(
            "conflicting_binding.md", conflicting_binding
        )
    )

    preparation_only_state = [
        line.replace("receiver_to_verify", "receiver_to_bind")
        for line in corrected
    ]
    assert any(
        finding.kind == "managed_receiver_binding_state"
        for finding in gate.evaluate_managed_receiver_lines(
            "preparation_only_state.md", preparation_only_state
        )
    )

    duplicate_authorization = corrected.copy()
    duplicate_authorization.insert(
        duplicate_authorization.index(
            "  authorization: create_exactly_one_fresh_codex_managed_worktree_task"
        ),
        "  authorization: create_many_tasks",
    )
    assert any(
        finding.kind == "managed_receiver_duplicate_field"
        for finding in gate.evaluate_managed_receiver_lines(
            "duplicate_authorization.md", duplicate_authorization
        )
    )

    broadened_authorization = corrected.copy()
    broadened_authorization.insert(
        broadened_authorization.index("  dispatch: immediate_same_turn") + 1,
        "  allow_repeat: true",
    )
    assert any(
        finding.kind == "managed_receiver_authorization_field"
        for finding in gate.evaluate_managed_receiver_lines(
            "broadened_authorization.md", broadened_authorization
        )
    )

    multiline_stale = corrected + [
        "If the controlling prompt contract cannot be freshly loaded,",
        "continue from remembered rules.",
    ]
    assert any(
        finding.kind == "stale_source_fallback"
        for finding in gate.evaluate_managed_receiver_lines(
            "multiline_stale.md", multiline_stale
        )
    )


def test_delegated_patch_gate_requires_cross_vendor_repo_courier() -> None:
    gate = _load_prompt_gate()
    couriered = [
        "output_mode: paste-ready-chat",
        "edit_permission: implementation-authorized",
        "target_kind: delegated_code_review_and_patch",
        "author_vendor: OpenAI",
        "delegate_vendor: operator_to_fill",
        "delegate_eligibility: different_vendor_lineage_with_direct_repo_access",
        "access: repo",
        "delivery: operator_courier_only",
        "receiver_binding:",
        "  receiver_class: receiver_to_bind",
        "  binding_state: receiver_to_bind",
    ]
    assert gate.evaluate_delegated_patch_lines("couriered.md", couriered) == []

    same_vendor = [
        line.replace("delegate_vendor: operator_to_fill", "delegate_vendor: OpenAI")
        for line in couriered
    ] + ["review_claim_boundary: same_vendor_sanity_only"]
    assert any(
        finding.kind == "delegated_patch_same_vendor"
        for finding in gate.evaluate_delegated_patch_lines("same_vendor.md", same_vendor)
    )

    managed_fallback = couriered + [
        "receiver_creation_authorization:",
        "  authorization: create_exactly_one_fresh_codex_managed_worktree_task",
    ]
    assert any(
        finding.kind == "delegated_patch_task_creation"
        for finding in gate.evaluate_delegated_patch_lines(
            "managed_fallback.md", managed_fallback
        )
    )

    no_repo = [line.replace("access: repo", "access: no_repo") for line in couriered]
    assert any(
        finding.kind == "delegated_patch_access"
        for finding in gate.evaluate_delegated_patch_lines("no_repo.md", no_repo)
    )

    missing_receiver = couriered[:-3]
    assert any(
        finding.kind == "delegated_patch_receiver_count"
        for finding in gate.evaluate_delegated_patch_lines(
            "missing_receiver.md", missing_receiver
        )
    )

    commented_trigger = [
        line.replace(
            "target_kind: delegated_code_review_and_patch",
            'target_kind: "delegated_code_review_and_patch" # courier target',
        ).replace("delegate_vendor: operator_to_fill", "delegate_vendor: OpenAI")
        for line in couriered
    ]
    assert any(
        finding.kind == "delegated_patch_same_vendor"
        for finding in gate.evaluate_delegated_patch_lines(
            "commented_trigger.md", commented_trigger
        )
    )

    cased_trigger = [
        line.replace(
            "target_kind: delegated_code_review_and_patch",
            "target_kind: Delegated_Code_Review_And_Patch",
        ).replace("access: repo", "access: no_repo")
        for line in couriered
    ]
    assert any(
        finding.kind == "delegated_patch_access"
        for finding in gate.evaluate_delegated_patch_lines(
            "cased_trigger.md", cased_trigger
        )
    )

    cased_placeholder = [
        line.replace(
            "delegate_vendor: operator_to_fill", "delegate_vendor: Operator_To_Fill"
        ).replace("receiver_class: receiver_to_bind", "receiver_class: external_direct_write")
        for line in couriered
    ]
    cased_findings = gate.evaluate_delegated_patch_lines(
        "cased_placeholder.md", cased_placeholder
    )
    assert any(
        finding.kind == "delegated_patch_delegate_vendor"
        for finding in cased_findings
    )
    assert any(
        finding.kind == "delegated_patch_receiver_class"
        for finding in cased_findings
    )


def test_every_pre_push_gate_is_the_same_command_ci_runs() -> None:
    guard = _load_pre_push_guard()
    ci_commands = {
        command.replace('"$FORSETI_DIFF_BASE"', "origin/main")
        for command in _ci_python_commands()
    }
    mirrored = {
        "python " + " ".join((script, *args))
        for _name, (script, *args) in guard.SELECTED_GATES
    }
    assert mirrored <= ci_commands


def test_observed_fast_failure_classes_are_mirrored_pre_push() -> None:
    guard = _load_pre_push_guard()
    names = {name for name, _command in guard.SELECTED_GATES}
    assert {
        "prompt contract shape",
        "review-output provenance",
        "handoff-pointer resolution",
        "ontology tag validity",
        "harness coupling contracts",
    } <= names


def test_ci_derives_and_verifies_exact_event_base_sha() -> None:
    ci_text = CI_PATH.read_text(encoding="utf-8")
    assert "github.event.pull_request.base.sha" in ci_text
    assert "github.event.before" in ci_text
    assert '[[ "$FORSETI_DIFF_BASE" =~ ^0+$ ]]' in ci_text
    assert 'git cat-file -e "${FORSETI_DIFF_BASE}^{commit}"' in ci_text
    assert ci_text.count('--diff "$FORSETI_DIFF_BASE" --strict') == 2


def test_ci_uses_public_runner_cpu_capacity_without_splitting_test_files() -> None:
    ci_text = CI_PATH.read_text(encoding="utf-8")
    assert '"pytest-xdist==3.8.0"' in ci_text
    assert (
        "python -m pytest --durations=50 --durations-min=0.25 "
        "-n 4 --dist=loadfile"
    ) in ci_text


def test_harness_coupling_trigger_scope() -> None:
    coupling = _load_harness_coupling()
    assert coupling.path_triggers_gate("forseti-harness/src/forseti_harness/example.py")
    assert coupling.path_triggers_gate(
        "forseti-harness/data_lake/lake_touchpoint_inventory_v0.json"
    )
    assert not coupling.path_triggers_gate("forseti-harness/data_lake/other.json")
    assert not coupling.path_triggers_gate("docs/decisions/example.md")


def test_harness_coupling_preserves_pytest_failure() -> None:
    coupling = _load_harness_coupling()

    class FailedResult:
        returncode = 7

    def failed_runner(_command, *, cwd, timeout):
        assert cwd == REPO_ROOT / "forseti-harness"
        assert timeout == coupling.TIMEOUT_SECONDS
        return FailedResult()

    assert coupling.run_contracts(REPO_ROOT, runner=failed_runner) == 7


def test_harness_coupling_fails_closed_on_unresolvable_diff_base(
    monkeypatch, capsys
) -> None:
    coupling = _load_harness_coupling()
    zero_sha = "0" * 40
    monkeypatch.setattr(coupling, "resolve_base_ref", lambda _base=None: zero_sha)

    assert coupling.main(["--strict"]) == 2
    captured = capsys.readouterr()
    assert "GATE FAIL harness coupling contracts" in captured.err
    assert f"{zero_sha}...HEAD" in captured.err


def test_event_base_sha_precedes_github_branch_and_cli(
    monkeypatch,
) -> None:
    monkeypatch.syspath_prepend(str(HOOKS_DIR))
    monkeypatch.setenv("FORSETI_DIFF_BASE", EVENT_BASE_SHA)
    monkeypatch.setenv("GITHUB_BASE_REF", "main")

    for filename, function_name, needs_root in DIFF_BASE_RESOLVERS:
        module = importlib.import_module(Path(filename).stem)
        resolver = getattr(module, function_name)
        args = (REPO_ROOT, "cli-base") if needs_root else ("cli-base",)
        assert resolver(*args) == EVENT_BASE_SHA, filename


def test_github_pr_base_precedes_cli_when_event_sha_absent(
    monkeypatch,
) -> None:
    monkeypatch.syspath_prepend(str(HOOKS_DIR))
    monkeypatch.delenv("FORSETI_DIFF_BASE", raising=False)
    monkeypatch.setenv("GITHUB_BASE_REF", "develop")

    for filename, function_name, needs_root in DIFF_BASE_RESOLVERS:
        module = importlib.import_module(Path(filename).stem)
        resolver = getattr(module, function_name)
        args = (REPO_ROOT, "cli-base") if needs_root else ("cli-base",)
        assert resolver(*args) == "origin/develop", filename


def test_external_actions_are_sha_pinned_and_renovate_managed() -> None:
    ci_text = CI_PATH.read_text(encoding="utf-8")
    uses = re.findall(r"^\s*- uses: (.+)$", ci_text, flags=re.MULTILINE)
    assert uses
    for use in uses:
        assert re.fullmatch(r"[^@]+@[0-9a-f]{40}\s+#\s+v\d+(?:\.\d+){0,2}", use), use

    renovate = json.loads((REPO_ROOT / "renovate.json").read_text(encoding="utf-8"))
    assert "github-actions" in renovate.get("enabledManagers", [])

    # A blanket wildcard packageRule can silently re-disable every manager it
    # does not carve back out; assert a later rule actually re-enables the
    # github-actions manager instead of just declaring it in enabledManagers.
    rules = renovate.get("packageRules", [])
    reenabled_at = None
    for index, rule in enumerate(rules):
        if rule.get("enabled") is True and "github-actions" in rule.get("matchManagers", []):
            reenabled_at = index
    assert reenabled_at is not None, "no packageRule re-enables the github-actions manager"

    disabled_wildcard_indexes = [
        index
        for index, rule in enumerate(rules)
        if rule.get("enabled") is False and rule.get("matchPackageNames") == ["*"]
    ]
    assert disabled_wildcard_indexes, "expected the blanket wildcard disable rule to still exist"
    assert reenabled_at > max(disabled_wildcard_indexes), (
        "github-actions re-enable rule must come after the blanket wildcard disable "
        "(Renovate packageRules merge in array order; an earlier re-enable would be "
        "overridden by the later blanket disable)"
    )
