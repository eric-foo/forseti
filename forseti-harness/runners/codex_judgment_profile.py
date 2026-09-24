"""Preventive empty-tool profile for one audited native Codex release.

The registration/dispatch proof is specific to this binary. Unknown binaries,
configuration layers, account plans and executor routes fail before generation.
The controller and OS are trusted; this is not a hostile-host isolation boundary.
"""
from __future__ import annotations

import copy
import ctypes
import hashlib
import json
from pathlib import Path
import queue
import subprocess
import sys
import threading
import time
import tomllib
import uuid

from harness_utils import hash_file

PROFILE_VERSION = "codex_empty_registry_01561_v1"
NATIVE_VERSION = "codex-cli 0.156.1"
NATIVE_SHA256 = "70bcb05f9bf1a4e7306edd0cd1b57d02af3267ad02a34b26f45c8c4bb20a3301"
PERSONAL_PLANS = frozenset({"free", "go", "plus", "pro", "prolite"})
NOISE_ENV = tuple("CODEX_EXEC_SERVER_NOISE_" + suffix for suffix in (
    "REGISTRY_URL", "ENVIRONMENT_ID", "AUTH_TOKEN", "CHATGPT_ACCOUNT_ID"))
DISABLED_FEATURES = (
    "shell_tool", "unified_exec", "multi_agent", "multi_agent_v2", "apps", "plugins",
    "browser_use", "computer_use", "image_generation", "view_image", "code_mode_host", "tool_suggest",
    "deferred_executor", "send_message_to_user_async", "request_permissions_tool", "token_budget",
    "current_time_reminder", "sleep_tool", "code_mode", "code_mode_only", "goals", "memories",
    "hooks", "skill_mcp_dependency_install",
)
CONFIG = (
    "project_doc_max_bytes=0", 'web_search="disabled"', "project_root_markers=[]",
    "tools.experimental_request_user_input.enabled=false", "tools.update_plan.enabled=false",
    "agents.enabled=false", "orchestrator.skills.enabled=false", "skills.include_instructions=false",
)
AUTH_CONFIG = ('cli_auth_credentials_store="file"', 'model_provider="openai"', 'forced_login_method="chatgpt"')
TOOL_PROJECTION = {
    "shell_type": "disabled", "apply_patch_tool_type": None,
    "experimental_supported_tools": [], "tool_mode": "direct", "supports_search_tool": False,
}


def _json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def profile_arguments():
    return ([part for value in AUTH_CONFIG + CONFIG for part in ("--config", value)]
            + [part for feature in DISABLED_FEATURES for part in ("--disable", feature)])


def program_data_path():
    """Match native SHGetKnownFolderPath, without trusting a ProgramData env var."""
    if sys.platform != "win32":
        raise ValueError("direct judgment requires the audited Windows native runtime")
    folder = (ctypes.c_ubyte * 16).from_buffer_copy(uuid.UUID("62ab5d82-fdc1-4dc3-a9dd-070d1d495d97").bytes_le)
    result = ctypes.c_wchar_p()
    shell = ctypes.windll.shell32
    shell.SHGetKnownFolderPath.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_void_p,
                                         ctypes.POINTER(ctypes.c_wchar_p)]
    shell.SHGetKnownFolderPath.restype = ctypes.c_long
    code = shell.SHGetKnownFolderPath(ctypes.byref(folder), 0, None, ctypes.byref(result))
    if code != 0 or not result.value:
        raise ValueError("cannot verify the native ProgramData configuration location")
    try:
        return Path(result.value)
    finally:
        ctypes.windll.ole32.CoTaskMemFree(ctypes.cast(result, ctypes.c_void_p))


def assert_absent(path):
    try:
        path.lstat()
    except FileNotFoundError:
        return
    except OSError:
        raise ValueError(f"cannot establish absent direct-judgment configuration: {path}") from None
    raise ValueError(f"direct judgment does not support inherited configuration: {path}")


def verify_environment(worktree, env):
    conflicts = [name for name in NOISE_ENV if env.get(name)]
    if conflicts:
        raise ValueError("direct judgment rejects executor overrides: " + ", ".join(conflicts))
    if env.get("CODEX_EXEC_SERVER_URL") not in (None, "", "none"):
        raise ValueError("direct judgment rejects CODEX_EXEC_SERVER_URL override")
    paths = configuration_paths(worktree, env["CODEX_HOME"])
    for path in paths:
        assert_absent(path)
    return [str(path) for path in paths]


def configuration_paths(worktree, codex_home):
    system = program_data_path() / "OpenAI" / "Codex"
    return [system / "config.toml", system / "requirements.toml",
            Path(worktree).resolve() / ".codex" / "config.toml",
            Path(codex_home) / "environments.toml"]


def verify_native(selection):
    if (selection.get("version") != NATIVE_VERSION or selection.get("sha256") != NATIVE_SHA256
            or hash_file(Path(selection["path"])) != NATIVE_SHA256):
        raise ValueError("direct judgment native binary is not the audited no-tools release")


def diagnostic_config(env):
    """Diagnostics lack --ignore-user-config; reject only route/catalog overrides."""
    path = Path(env["CODEX_HOME"]) / "config.toml"
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return {"path": str(path), "sha256": None}
    except OSError:
        raise ValueError("cannot inspect native diagnostic configuration") from None
    try:
        value = tomllib.loads(raw.decode("utf-8-sig"))
    except (ValueError, UnicodeError):
        raise ValueError("native diagnostic configuration is not valid TOML") from None
    active = [value]
    if value.get("profile") is not None:
        name = value["profile"]
        profiles = value.get("profiles", {})
        if not isinstance(name, str) or not isinstance(profiles, dict) or not isinstance(profiles.get(name), dict):
            raise ValueError("native diagnostic configuration has an unresolved active profile")
        active.append(profiles[name])
    for layer in active:
        for key in ("model_catalog_json", "openai_base_url", "chatgpt_base_url"):
            if key in layer:
                raise ValueError("direct judgment diagnostic rejects user configuration key: " + key)
        providers = layer.get("model_providers", {})
        if not isinstance(providers, dict) or "openai" in providers:
            raise ValueError("direct judgment diagnostic rejects built-in provider overrides")
    return {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest()}


def personal_account(executable, env, worktree):
    """Ask native auth for a safe account projection; never read or retain credentials."""
    command = [executable, *profile_arguments(), "app-server", "--stdio"]
    process = subprocess.Popen(command, cwd=worktree, env=env, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding="utf-8",
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    replies = queue.Queue()

    def read_lines():
        try:
            for line in process.stdout:
                replies.put(line)
        finally:
            replies.put(None)

    threading.Thread(target=read_lines, daemon=True).start()
    deadline = time.monotonic() + 20

    def send(value):
        process.stdin.write(json.dumps(value) + "\n")
        process.stdin.flush()

    def receive(identifier):
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ValueError("direct judgment native account check timed out")
            try:
                line = replies.get(timeout=remaining)
            except queue.Empty:
                raise ValueError("direct judgment native account check timed out") from None
            if line is None:
                raise ValueError("direct judgment native account check ended without a result")
            try:
                value = json.loads(line)
            except ValueError:
                raise ValueError("direct judgment native account protocol was invalid") from None
            if value.get("id") == identifier:
                if "error" in value or not isinstance(value.get("result"), dict):
                    raise ValueError("direct judgment native account check failed")
                return value["result"]

    try:
        send({"id": 1, "method": "initialize", "params": {
            "clientInfo": {"name": "forseti-judgment-profile", "version": "1"},
            "capabilities": {"experimentalApi": True}}})
        receive(1)
        send({"method": "initialized"})
        send({"id": 2, "method": "account/read", "params": {"refreshToken": False}})
        account = receive(2).get("account")
        if (not isinstance(account, dict) or account.get("type") != "chatgpt"
                or account.get("planType") not in PERSONAL_PLANS):
            raise ValueError("direct judgment requires a verified supported personal ChatGPT plan")
        return {"type": "chatgpt", "plan": account["planType"]}
    finally:
        if process.poll() is None:
            process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
        process.stdin.close()
        process.stdout.close()


def project_model(catalog, model, effort):
    matches = [item for item in catalog.get("models", []) if item.get("slug") == model]
    if len(matches) != 1:
        raise ValueError("direct judgment requires one exact native model catalog entry")
    source = matches[0]
    if effort not in [level.get("effort") for level in source.get("supported_reasoning_levels", [])]:
        raise ValueError("direct judgment effort is not supported by the exact native model")
    projected = copy.deepcopy(source)
    projected.update(TOOL_PROJECTION)
    return source, {"models": [projected]}


def read_catalog(executable, env, worktree):
    command = [executable, *profile_arguments(), "debug", "models"]
    try:
        result = subprocess.run(command, cwd=worktree, env=env, stdin=subprocess.DEVNULL,
            capture_output=True, text=True, encoding="utf-8", timeout=20,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0), check=False)
    except subprocess.TimeoutExpired:
        raise ValueError("direct judgment native model catalog check timed out") from None
    if result.returncode:
        raise ValueError("direct judgment native model catalog check failed")
    try:
        return json.loads(result.stdout)
    except ValueError:
        raise ValueError("direct judgment native model catalog was invalid") from None


def prepare(selection, env, worktree, model, effort):
    verify_native(selection)
    absent = verify_environment(worktree, env)
    user_config = diagnostic_config(env)
    env["CODEX_EXEC_SERVER_URL"] = "none"
    account = personal_account(selection["path"], env, worktree)
    source, projected = project_model(read_catalog(selection["path"], env, worktree), model, effort)
    return {"version": PROFILE_VERSION, "native_sha256": NATIVE_SHA256,
            "account": account, "absent_configuration": absent,
            "diagnostic_config": user_config,
            "executor_environment": {"CODEX_EXEC_SERVER_URL": "none"},
            "disabled_features": list(DISABLED_FEATURES), "config": list(CONFIG)}, source, projected


def recheck(selection, env, worktree, profile, attempt_dir):
    verify_native(selection)
    if (verify_environment(worktree, env) != profile["absent_configuration"]
            or diagnostic_config(env) != profile["diagnostic_config"]):
        raise ValueError("direct judgment configuration changed before generation")
    for name in ("judgment-source-model.json", "judgment-model-catalog.json"):
        if hash_file(attempt_dir / name) != profile[name]["sha256"]:
            raise ValueError("direct judgment catalog changed before generation")


def retain(attempt_dir, profile, source, projected):
    for name, value in (("judgment-source-model.json", source), ("judgment-model-catalog.json", projected)):
        target = (attempt_dir / name).resolve()
        with target.open("xb") as handle:
            handle.write(_json_bytes(value))
        profile[name] = {"path": str(target), "sha256": hash_file(target)}
    return "model_catalog_json=" + json.dumps(profile["judgment-model-catalog.json"]["path"])


def verify_receipt(path, receipt):
    """Re-derive saved profile/catalog restrictions before accepting a judgment."""
    metadata = receipt.get("launch_metadata", {})
    profile = metadata.get("judgment_tool_profile", {})
    selection = metadata.get("codex_selection", {})
    if (profile.get("version") != PROFILE_VERSION or profile.get("native_sha256") != NATIVE_SHA256
            or selection.get("sha256") != NATIVE_SHA256 or selection.get("version") != NATIVE_VERSION
            or profile.get("disabled_features") != list(DISABLED_FEATURES)
            or profile.get("config") != list(CONFIG)
            or profile.get("executor_environment") != {"CODEX_EXEC_SERVER_URL": "none"}
            or profile.get("account", {}).get("type") != "chatgpt"
            or profile.get("account", {}).get("plan") not in PERSONAL_PLANS):
        raise ValueError("provider attempt lacks the audited preventive judgment profile")
    saved = {}
    for name in ("judgment-source-model.json", "judgment-model-catalog.json"):
        record = profile.get(name, {})
        target = (path / name).resolve()
        if record.get("path") != str(target) or record.get("sha256") != hash_file(target):
            raise ValueError("provider attempt judgment catalog binding changed")
        saved[name] = json.loads(target.read_text(encoding="utf-8"))
    source = saved["judgment-source-model.json"]
    projected = copy.deepcopy(source)
    projected.update(TOOL_PROJECTION)
    if saved["judgment-model-catalog.json"] != {"models": [projected]}:
        raise ValueError("provider attempt judgment catalog projection changed")
    command = receipt["command"]
    required_flags = ("--ephemeral", "--ignore-user-config", "--ignore-rules", "--strict-config", "--json")
    valued_flags = {"--sandbox", "-C", "--model", "--config", "--disable", "--output-schema", "--output-last-message"}
    if (not isinstance(command, list) or len(command) < 2
            or not all(isinstance(token, str) for token in command)
            or any(command.count(flag) != 1 for flag in required_flags + ("-C", "--model", "--sandbox"))
            or command[0] != selection.get("path") or command[1] != "exec"):
        raise ValueError("provider attempt preventive judgment invocation changed")
    index = 2
    while index < len(command):
        token = command[index]
        if token in required_flags or token == "-" and index == len(command) - 1:
            index += 1
        elif token in valued_flags and index + 1 < len(command):
            index += 2
        else:
            raise ValueError("provider attempt has an unbound direct judgment argument")
    if command.count("--sandbox") != 1 or command[command.index("--sandbox") + 1] != "read-only":
        raise ValueError("provider attempt judgment sandbox changed")
    diagnostic = profile.get("diagnostic_config")
    if not isinstance(diagnostic, dict) or set(diagnostic) != {"path", "sha256"}:
        raise ValueError("provider attempt lacks diagnostic configuration attestation")
    config_path = diagnostic.get("path")
    digest = diagnostic.get("sha256")
    if (not isinstance(config_path, str) or not Path(config_path).is_absolute()
            or str(Path(config_path).resolve()) != config_path or Path(config_path).name != "config.toml"
            or digest is not None and (not isinstance(digest, str) or len(digest) != 64
                                      or any(char not in "0123456789abcdef" for char in digest))):
        raise ValueError("provider attempt diagnostic configuration attestation changed")
    expected_absent = [str(item) for item in configuration_paths(
        command[command.index("-C") + 1], Path(config_path).parent)]
    if profile.get("absent_configuration") != expected_absent:
        raise ValueError("provider attempt absent configuration attestation changed")
    disabled = [command[i + 1] for i, part in enumerate(command[:-1]) if part == "--disable"]
    if disabled != list(DISABLED_FEATURES):
        raise ValueError("provider attempt judgment feature profile changed")
    settings = [command[i + 1] for i, part in enumerate(command[:-1]) if part == "--config"]
    required = AUTH_CONFIG + CONFIG + (
        "model_catalog_json=" + json.dumps(str((path / "judgment-model-catalog.json").resolve())),)
    for setting in required:
        if [value for value in settings if value.split("=", 1)[0] == setting.split("=", 1)[0]] != [setting]:
            raise ValueError("provider attempt preventive judgment setting changed")
    allowed = {value.split("=", 1)[0] for value in required} | {"model_reasoning_effort", "developer_instructions"}
    if any(value.split("=", 1)[0] not in allowed for value in settings):
        raise ValueError("provider attempt has an unbound direct judgment setting")
    if "--strict-config" not in command or source.get("slug") != command[command.index("--model") + 1]:
        raise ValueError("provider attempt judgment model or strict configuration changed")
    return profile
