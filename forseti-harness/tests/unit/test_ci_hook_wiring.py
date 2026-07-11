"""Keep CI and the local pre-push mirror mechanically aligned."""

from __future__ import annotations

import importlib
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
CI_PATH = REPO_ROOT / ".github" / "workflows" / "ci.yml"
PRE_PUSH_PATH = REPO_ROOT / ".agents" / "hooks" / "pre_push_guard.py"
HOOKS_DIR = REPO_ROOT / ".agents" / "hooks"
EVENT_BASE_SHA = "1" * 40
DIFF_BASE_RESOLVERS = (
    ("check_source_input_hashes.py", "resolve_base_ref", False),
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


def test_every_pre_push_gate_is_the_same_command_ci_runs() -> None:
    guard = _load_pre_push_guard()
    ci_commands = {
        command.replace('"$FORSETI_DIFF_BASE"', "origin/main")
        for command in _ci_python_commands()
    }
    mirrored = {
        "python " + " ".join((script, *args))
        for _name, (script, *args) in guard.DOC_GATES
    }
    assert mirrored <= ci_commands


def test_observed_fast_failure_classes_are_mirrored_pre_push() -> None:
    guard = _load_pre_push_guard()
    names = {name for name, _command in guard.DOC_GATES}
    assert {
        "prompt output-mode",
        "review-output provenance",
        "handoff-pointer resolution",
        "ontology tag validity",
    } <= names


def test_ci_derives_and_verifies_exact_event_base_sha() -> None:
    ci_text = CI_PATH.read_text(encoding="utf-8")
    assert "github.event.pull_request.base.sha" in ci_text
    assert "github.event.before" in ci_text
    assert '[[ "$FORSETI_DIFF_BASE" =~ ^0+$ ]]' in ci_text
    assert 'git cat-file -e "${FORSETI_DIFF_BASE}^{commit}"' in ci_text
    assert ci_text.count('--diff "$FORSETI_DIFF_BASE" --strict') == 2


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
