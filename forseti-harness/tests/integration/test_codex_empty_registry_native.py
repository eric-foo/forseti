"""Opt-in real-native proof; fake credentials and loopback inference only.

Set FORSETI_TEST_CODEX_NATIVE to the audited executable. Optionally set
FORSETI_NATIVE_PROOF_ROOT to a new directory to preserve synthetic evidence.
No model service, production credentials, or installation is needed.
"""
import base64
import copy
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import threading

import pytest

from harness_utils import hash_file
from runners import codex_judgment_profile as profile


def test_native_empty_registry_blocks_forged_calls_and_accepts_json(tmp_path):
    executable = os.environ.get("FORSETI_TEST_CODEX_NATIVE")
    if not executable:
        pytest.skip("set FORSETI_TEST_CODEX_NATIVE for the real-native offline proof")
    selection = {"path": executable, "version": profile.NATIVE_VERSION, "sha256": hash_file(Path(executable))}
    profile.verify_native(selection)
    root = Path(os.environ.get("FORSETI_NATIVE_PROOF_ROOT", str(tmp_path / "proof"))).resolve()
    root.mkdir(parents=True, exist_ok=False)
    # --bundled returns the binary's catalog before config/auth construction.
    result = subprocess.run([executable, "debug", "models", "--bundled"], capture_output=True,
        text=True, encoding="utf-8", timeout=10, check=True)
    catalog = json.loads(result.stdout)
    source, projected = profile.project_model(catalog, "gpt-6-astra", "high")
    async_call = {"type": "function_call", "call_id": "async-probe", "name": "request_user_input_async",
        "arguments": json.dumps({"questions": [{"title": "FORBIDDEN_ASYNC_HANDLER_MARKER"}]})}
    forged = [async_call]
    for name in ("exec_command", "exec", "wait", "get_goal", "list_mcp_resources", "unknown_future_tool"):
        forged.append({"type": "function_call", "call_id": name, "name": name, "arguments": "{}"})
    forged += [
        {"type": "function_call", "call_id": "clock", "namespace": "clock", "name": "curr_time", "arguments": "{}"},
        {"type": "custom_tool_call", "call_id": "patch", "name": "apply_patch",
         "input": "*** Begin Patch\n*** Add File: forbidden-marker.txt\n+FORBIDDEN_PATCH_MARKER\n*** End Patch"},
    ]
    observations = {}
    for label, calls in (("control", [async_call]), ("enforced", forged)):
        case = root / label
        case.mkdir()
        home = case / "home"
        home.mkdir()
        jwt_encode = lambda value: base64.urlsafe_b64encode(json.dumps(value).encode()).decode().rstrip("=")
        token = jwt_encode({"alg": "none"}) + "." + jwt_encode({"exp": 4102444800,
            "https://api.openai.com/auth": {"chatgpt_plan_type": "pro", "chatgpt_account_id": "synthetic-account"}}) + ".synthetic"
        (home / "auth.json").write_text(json.dumps({"tokens": {"id_token": token,
            "access_token": "synthetic-access-token", "refresh_token": "synthetic-refresh-token",
            "account_id": "synthetic-account"}, "last_refresh": "2099-01-01T00:00:00Z"}))
        current = copy.deepcopy(projected)
        if label == "control":
            current["models"][0]["experimental_supported_tools"] = ["send_user_message_async"]
        manifest = {}
        setting = profile.retain(case, manifest, source, current)
        schema = {"type": "object", "properties": {"ok": {"type": "boolean"}},
                  "required": ["ok"], "additionalProperties": False}
        (case / "schema.json").write_text(json.dumps(schema))
        requests, errors = [], []

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"
            def log_message(self, *args): pass
            def send(self, status, value, kind="application/json"):
                raw = value.encode()
                self.send_response(status)
                self.send_header("Content-Type", kind)
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
            def do_GET(self):
                if self.path.endswith("/accounts/check"):
                    self.send(200, json.dumps({"accounts": [{"id": "synthetic-account",
                        "workspace_backend_origin": "https://chatgpt.com", "account_routing_override": "NO_CONSTRAINT"}]}))
                else:
                    self.send(404, "{}")
            def do_POST(self):
                raw = self.rfile.read(int(self.headers.get("Content-Length", "0")))
                if "analytics-events" in self.path:
                    self.send(200, "{}")
                    return
                try:
                    assert self.path == "/backend-api/codex/responses"
                    assert not self.headers.get("Content-Encoding")
                    body = json.loads(raw)
                    requests.append(body)
                    assert len(requests) <= 2, "unexpected sampling loop"
                    items = calls if len(requests) == 1 else [{"type": "message", "role": "assistant",
                        "id": "answer", "content": [{"type": "output_text", "text": '{"ok":true}'}]}]
                    events = [{"type": "response.created", "response": {"id": "synthetic"}}]
                    events.extend({"type": "response.output_item.done", "item": item} for item in items)
                    events.append({"type": "response.completed", "response": {"id": "synthetic",
                        "usage": {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2}}})
                    self.send(200, "".join("data: " + json.dumps(event) + "\n\n" for event in events), "text/event-stream")
                except Exception as exc:
                    errors.append(str(exc))
                    self.send(500, "{}")

        bootstrap = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        inference = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        for server in (bootstrap, inference):
            threading.Thread(target=server.serve_forever, daemon=True).start()
        env = dict(os.environ, CODEX_HOME=str(home), CODEX_EXEC_SERVER_URL="none")
        for key in ("OPENAI_API_KEY", "CODEX_API_KEY", "CODEX_ACCESS_TOKEN", "OPENAI_BASE_URL", *profile.NOISE_ENV):
            env.pop(key, None)
        profile.verify_environment(case, env)
        # Separate origins prevent workspace routing from replacing the local
        # inference destination. The Codex backend suffix preserves capabilities.
        command = [executable, "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules", "--strict-config",
            "--json", "--sandbox", "read-only", "--skip-git-repo-check", "-C", str(case), "--model", "gpt-6-astra",
            "--config", 'model_reasoning_effort="high"', *profile.profile_arguments(), "--config", setting,
            "--config", "openai_base_url=" + json.dumps(f"http://127.0.0.1:{inference.server_port}/backend-api/codex"),
            "--config", "chatgpt_base_url=" + json.dumps(f"http://127.0.0.1:{bootstrap.server_port}"),
            "--disable", "enable_request_compression", "--output-schema", str(case / "schema.json"),
            "--output-last-message", str(case / "response.json"), "-"]
        try:
            run = subprocess.run(command, input='Return {"ok":true}.', capture_output=True,
                text=True, encoding="utf-8", env=env, timeout=40, check=False)
            (case / "events.jsonl").write_text(run.stdout, encoding="utf-8")
            (case / "stderr.log").write_text(run.stderr, encoding="utf-8")
            (case / "requests.json").write_text(json.dumps(requests, indent=2), encoding="utf-8")
            (case / "command.json").write_text(json.dumps(command, indent=2), encoding="utf-8")
            assert not errors, errors
            assert run.returncode == 0, run.stderr
            assert len(requests) == 2
            assert json.loads((case / "response.json").read_text()) == {"ok": True}
            inventories = [[item["tools"] for item in request["input"] if item.get("type") == "additional_tools"]
                           for request in requests]
            outputs = {item["call_id"]: item["output"] for item in requests[1]["input"] if "output" in item}
            if label == "control":
                tools = inventories[0][0][0]["tools"]
                assert [tool["name"] for tool in tools] == ["request_user_input_async"]
                assert "FORBIDDEN_ASYNC_HANDLER_MARKER" in run.stdout
                assert json.loads(outputs["async-probe"]) == {"accepted": True}
            else:
                assert inventories == [[[]], [[]]]
                assert all(request.get("tools", []) == [] for request in requests)
                assert len(outputs) == len(forged)
                assert all(value.startswith("unsupported ") for value in outputs.values()), outputs
                assert "FORBIDDEN_" not in run.stdout
                assert not (case / "forbidden-marker.txt").exists()
            observations[label] = {"requests": len(requests), "outputs": outputs, "inventories": inventories}
        finally:
            for server in (bootstrap, inference):
                server.shutdown()
                server.server_close()
    (root / "proof.json").write_text(json.dumps({"native": selection, "profile_version": profile.PROFILE_VERSION,
        "profile_source_sha256": hash_file(Path(profile.__file__)), "observations": observations}, indent=2), encoding="utf-8")
