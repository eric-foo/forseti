"""Fail-closed profile checks; all credentials and native replies are simulated."""
import copy
import io
import json
from pathlib import Path

import pytest

from harness_utils import hash_file
from runners import codex_judgment_profile as profile


@pytest.fixture
def prepared(tmp_path, monkeypatch):
    executable = tmp_path / "fake-native.exe"
    executable.write_bytes(b"explicit offline fixture")
    monkeypatch.setattr(profile, "NATIVE_SHA256", hash_file(executable))
    monkeypatch.setattr(profile, "program_data_path", lambda: tmp_path / "system")
    monkeypatch.setattr(profile, "personal_account", lambda *args: {"type": "chatgpt", "plan": "pro"})
    source = {"slug": "fixture-model", "supported_reasoning_levels": [{"effort": "high"}],
        "model_messages": {"instructions_template": "Preserve this exact instruction"},
        "context_window": 272000, "use_responses_lite": True,
        "experimental_supported_tools": ["clock", "send_user_message_async"],
        "apply_patch_tool_type": "freeform", "tool_mode": "code_mode_only"}
    monkeypatch.setattr(profile, "read_catalog", lambda *args: {"models": [copy.deepcopy(source)]})
    selection = {"path": str(executable), "version": profile.NATIVE_VERSION, "sha256": hash_file(executable)}
    env = {"CODEX_HOME": str(tmp_path / "home")}
    result, original, catalog = profile.prepare(selection, env, tmp_path, "fixture-model", "high")
    catalog_setting = profile.retain(tmp_path, result, original, catalog)
    command = [str(executable), "exec", "--strict-config", "--ephemeral", "--ignore-user-config", "--ignore-rules",
        "--json", "--sandbox", "read-only", "--model", "fixture-model", "-C", str(tmp_path),
        *profile.profile_arguments(), "--config", catalog_setting]
    receipt = {"command": command, "launch_metadata": {
        "codex_selection": selection, "judgment_tool_profile": result}}
    return tmp_path, selection, env, result, source, catalog, receipt


def test_projection_preserves_every_non_tool_field_and_receipt(prepared):
    path, selection, env, result, source, catalog, receipt = prepared
    expected = copy.deepcopy(source)
    expected.update(profile.TOOL_PROJECTION)
    assert catalog == {"models": [expected]}
    assert source["tool_mode"] == "code_mode_only"
    assert env["CODEX_EXEC_SERVER_URL"] == "none"
    profile.recheck(selection, env, path, result, path)
    assert profile.verify_receipt(path, receipt) == result


@pytest.mark.parametrize("mutation", ["native_bytes", "native_version", "system", "requirements", "project",
    "environment", "noise", "remote", "user_config", "catalog"])
def test_changes_fail_before_launch(prepared, mutation):
    path, selection, env, result, _, _, _ = prepared
    if mutation == "native_bytes":
        Path(selection["path"]).write_bytes(b"changed")
    elif mutation == "native_version":
        selection["version"] = "codex-cli 0.156.2"
    elif mutation in {"system", "requirements", "project", "environment"}:
        index = {"system": 0, "requirements": 1, "project": 2, "environment": 3}[mutation]
        target = Path(result["absent_configuration"][index])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# even empty inherited files are unsupported")
    elif mutation == "noise":
        env[profile.NOISE_ENV[2]] = "secret-that-must-not-be-printed"
    elif mutation == "remote":
        env["CODEX_EXEC_SERVER_URL"] = "http://remote.invalid"
    elif mutation == "user_config":
        target = Path(env["CODEX_HOME"]) / "config.toml"
        target.parent.mkdir(parents=True)
        target.write_text('model="unrelated-change"')
    elif mutation == "catalog":
        (path / "judgment-model-catalog.json").write_text('{}')
    with pytest.raises(ValueError) as failure:
        profile.recheck(selection, env, path, result, path)
    assert "secret-that-must-not-be-printed" not in str(failure.value)


@pytest.mark.parametrize("key", ["model_catalog_json", "openai_base_url", "chatgpt_base_url"])
@pytest.mark.parametrize("active_profile", [False, True])
def test_diagnostic_config_rejects_effective_route_changes(tmp_path, key, active_profile):
    body = f'{key}="do-not-disclose-value"\n'
    if active_profile:
        body = 'profile="active"\n[profiles.active]\n' + body
    (tmp_path / "config.toml").write_text(body)
    with pytest.raises(ValueError, match=key) as failure:
        profile.diagnostic_config({"CODEX_HOME": str(tmp_path)})
    assert "do-not-disclose-value" not in str(failure.value)


def test_diagnostic_config_allows_irrelevant_and_inactive_settings(tmp_path):
    (tmp_path / "config.toml").write_text('model="other"\n[profiles.inactive]\nopenai_base_url="unused"\n')
    observed = profile.diagnostic_config({"CODEX_HOME": str(tmp_path)})
    assert observed["sha256"] == hash_file(tmp_path / "config.toml")


@pytest.mark.parametrize("mutation", ["missing_profile", "different_native", "environment", "plan", "catalog_bytes",
    "catalog_rehashed", "extra_setting", "missing_setting", "non_tool_metadata", "remote_argument", "sandbox",
    "attached_enable", "attached_config", "missing_absent", "missing_diagnostic", "absent_path",
    "diagnostic_path", "diagnostic_hash"])
def test_saved_receipt_cannot_assert_away_restrictions(prepared, mutation):
    path, _, _, result, _, _, receipt = prepared
    if mutation == "missing_profile":
        receipt["launch_metadata"].pop("judgment_tool_profile")
    elif mutation == "different_native":
        receipt["launch_metadata"]["codex_selection"]["sha256"] = "0" * 64
    elif mutation == "environment":
        result["executor_environment"] = {}
    elif mutation == "plan":
        result["account"]["plan"] = "business"
    elif mutation in {"catalog_bytes", "catalog_rehashed", "non_tool_metadata"}:
        target = path / "judgment-model-catalog.json"
        value = json.loads(target.read_text())
        if mutation == "non_tool_metadata":
            value["models"][0]["context_window"] = 1
        else:
            value["models"][0]["experimental_supported_tools"] = ["clock"]
        target.write_text(json.dumps(value))
        if mutation != "catalog_bytes":
            result["judgment-model-catalog.json"]["sha256"] = hash_file(target)
    elif mutation == "extra_setting":
        receipt["command"] += ["--config", 'openai_base_url="http://other.invalid"']
    elif mutation == "missing_setting":
        index = receipt["command"].index("agents.enabled=false")
        del receipt["command"][index - 1:index + 1]
    elif mutation == "remote_argument":
        receipt["command"] += ["--remote", "http://other.invalid"]
    elif mutation == "sandbox":
        receipt["command"][receipt["command"].index("--sandbox") + 1] = "danger-full-access"
    elif mutation == "attached_enable":
        receipt["command"] += ["--enable=send_message_to_user_async"]
    elif mutation == "attached_config":
        receipt["command"] += ["--config=tools.experimental_request_user_input.enabled=true"]
    elif mutation == "missing_absent":
        result.pop("absent_configuration")
    elif mutation == "missing_diagnostic":
        result.pop("diagnostic_config")
    elif mutation == "absent_path":
        result["absent_configuration"][2] = str(path / "wrong" / "config.toml")
    elif mutation == "diagnostic_path":
        result["diagnostic_config"]["path"] = "config.toml"
    elif mutation == "diagnostic_hash":
        result["diagnostic_config"]["sha256"] = "not-a-hash"
    with pytest.raises(ValueError):
        profile.verify_receipt(path, receipt)


@pytest.mark.parametrize("account", [None, {"type": "apiKey"}, {"type": "chatgpt", "planType": "unknown"},
    {"type": "chatgpt", "planType": "business"}, {"type": "chatgpt", "planType": "pro"}])
def test_account_protocol_projects_only_personal_plan(tmp_path, monkeypatch, account):
    class Process:
        stdin = io.StringIO()
        stdout = io.StringIO(json.dumps({"id": 1, "result": {}}) + "\n" + json.dumps({"id": 2,
            "result": {"account": dict(account, email="private@example.invalid") if account else None}}) + "\n")
        def poll(self): return 0
        def wait(self, timeout): return 0
    captured = []
    monkeypatch.setattr(profile.subprocess, "Popen", lambda *a, **kw: captured.append((a, kw)) or Process())
    if account == {"type": "chatgpt", "planType": "pro"}:
        assert profile.personal_account("fake", {}, tmp_path) == {"type": "chatgpt", "plan": "pro"}
    else:
        with pytest.raises(ValueError, match="personal ChatGPT"):
            profile.personal_account("fake", {}, tmp_path)
    assert captured[0][1]["cwd"] == tmp_path


def test_absence_probe_does_not_treat_unreadability_as_absence(monkeypatch):
    monkeypatch.setattr(Path, "lstat", lambda *args: (_ for _ in ()).throw(PermissionError()))
    with pytest.raises(ValueError, match="cannot establish absent"):
        profile.assert_absent(Path("unreadable"))


def test_unknown_model_or_effort_has_no_fallback():
    catalog = {"models": [{"slug": "known", "supported_reasoning_levels": [{"effort": "high"}]}]}
    with pytest.raises(ValueError, match="exact native"):
        profile.project_model(catalog, "known-new", "high")
    with pytest.raises(ValueError, match="effort"):
        profile.project_model(catalog, "known", "max")
