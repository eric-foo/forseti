"""Bounded recovery of immutable provider attempts; never semantic acceptance."""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
import re
import time
from pathlib import Path

from harness_utils import hash_file


def _read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, sort_keys=True, indent=2)
        handle.write("\n")


@contextlib.contextmanager
def _lock(path, *, wait_seconds=0):
    """OS-owned lock; briefly serialize budget claims, reject duplicate jobs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as handle:
        handle.seek(0, os.SEEK_END)
        if not handle.tell():
            handle.write(b"0"); handle.flush()
        handle.seek(0)
        if os.name == "nt":
            import msvcrt
            acquire = lambda: msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            release = lambda: msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            acquire = lambda: fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            release = lambda: fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        deadline = time.monotonic() + wait_seconds
        while True:
            try:
                acquire()
                break
            except OSError:
                if time.monotonic() >= deadline:
                    raise ValueError("provider job or retry budget is already in use") from None
                time.sleep(min(0.05, max(0, deadline - time.monotonic())))
        try:
            yield
        finally:
            release()


def stopped_read_only_timeout(receipt, events):
    """A local stop is recovery permission, not proof of zero remote work."""
    if (receipt.get("outcome") != "TIMED_OUT" or "error" not in receipt or receipt["error"] is not None
            or type(receipt.get("exit_code")) is not int or receipt.get("response_bytes") != 0
            or receipt.get("response_sha256") is not None
            or receipt.get("launch_metadata", {}).get("authentication_observed") != "chatgpt"):
        return False
    command = receipt.get("command", [])
    if len(command) < 3 or command[1] != "exec" or command[-1] != "-":
        return False
    flags, options, settings = set(), {}, {}
    index = 2
    while index < len(command) - 1:
        key = command[index]
        if key in {"--ephemeral", "--ignore-user-config", "--ignore-rules", "--json"}:
            if key in flags: return False
            flags.add(key); index += 1
        elif key in {"--sandbox", "--disable", "-C", "--model", "--output-schema", "--output-last-message", "--config"}:
            if index + 1 >= len(command) - 1: return False
            value = command[index+1]
            target = settings if key == "--config" else options
            if key == "--config":
                key, separator, value = value.partition("=")
                if not separator or key not in {"model_reasoning_effort", "cli_auth_credentials_store",
                        "model_provider", "forced_login_method", "developer_instructions"}: return False
            if key in target: return False
            target[key] = value; index += 2
        else:
            return False
    if (flags != {"--ephemeral", "--ignore-user-config", "--ignore-rules", "--json"}
            or options.get("--sandbox") != "read-only" or options.get("--disable") != "shell_tool"
            or any(settings.get(k) != v for k, v in {
                "cli_auth_credentials_store": '"file"', "model_provider": '"openai"',
                "forced_login_method": '"chatgpt"'}.items())):
        return False
    try:
        rows = [json.loads(line) for line in events.splitlines()]
        return all(isinstance(row, dict) and row.get("type") in {"thread.started", "turn.started"} for row in rows)
    except ValueError:
        return False


def transient_failure(receipt, events, stderr):
    """Recognize bounded transport recovery; never infer success or free usage."""
    if receipt.get("outcome") not in {"PROCESS_FAILED", "TIMED_OUT"}:
        return None
    if receipt.get("outcome") == "TIMED_OUT":
        return "stopped_read_only_timeout" if stopped_read_only_timeout(receipt, events) else None
    messages = []
    for line in events.splitlines():
        try:
            row = json.loads(line)
        except (ValueError, TypeError):
            continue
        if not isinstance(row, dict):
            continue
        # A timeout can coexist with completed answers. Preserve those for the
        # existing validator-owned recovery path instead of paying for another
        # generation because an earlier reconnect warning happened to exist.
        if row.get("type") == "turn.completed" or (
            row.get("type") == "item.completed"
            and isinstance(row.get("item"), dict)
            and row["item"].get("type") == "agent_message"
        ):
            return None
        if row.get("type") == "error":
            messages.append(row.get("message"))
        elif row.get("type") == "turn.failed" and isinstance(row.get("error"), dict):
            messages.append(row["error"].get("message"))
    if messages and all(message in {
        "Selected model is at capacity. Please try a different model.",
        "Selected model is at capacity.",
    } for message in messages):
        return "capacity"
    if not messages and re.search(
        r"(?m)^\d{4}-\d\d-\d\dT\S+\s+WARN\s+codex_core::responses_retry: "
        r"stream disconnected - retrying sampling request[^\n]*"
        r"sampling_error=stream disconnected before completion: WebSocket protocol error: "
        r"Connection reset without closing handshake\s*$", stderr,
    ):
        return "connection_reset"
    return None


def _check_attempt(path, binding):
    receipt = _read(path / "execution_receipt.json")
    command = receipt.get("command", [])
    if not command or command[0] != binding["codex_executable"]:
        raise ValueError("provider attempt executable changed")
    if ("codex_version" in binding and
            receipt.get("launch_metadata", {}).get("codex_version") != binding["codex_version"]):
        raise ValueError("provider attempt executable version changed")
    selection = receipt.get("launch_metadata", {}).get("codex_selection")
    if selection is not None and (selection.get("path") != binding["codex_executable"] or
                                  selection.get("sha256") != binding["codex_sha256"]):
        raise ValueError("provider attempt selected executable bytes changed")
    for option, key in (("--model", "model"), ("-C", "worktree")):
        if command.count(option) != 1 or command[command.index(option)+1] != binding[key]:
            raise ValueError("provider attempt launch binding changed")
    if "reasoning_effort" in binding:
        settings = [command[i+1] for i, part in enumerate(command[:-1]) if part == "--config"]
        efforts = [value for value in settings if value.startswith("model_reasoning_effort=")]
        if efforts != [f'model_reasoning_effort="{binding["reasoning_effort"]}"']:
            raise ValueError("provider attempt reasoning effort changed")
    task_prompt_sha = receipt.get("prompt_sha256")
    if receipt.get("launch_metadata", {}).get("authentication_observed") != "chatgpt":
        raise ValueError("provider attempt lacks subscription authentication evidence")
    if "preloaded_context_sha256" in binding:
        metadata = receipt.get("launch_metadata", {})
        settings = [command[i+1] for i, part in enumerate(command[:-1]) if part == "--config"]
        contexts = [value.split("=", 1)[1] for value in settings if value.startswith("developer_instructions=")]
        transport = metadata.get("preloaded_context_transport")
        if transport is not None:
            from runners.run_codex_provider_attempt import CONTEXT_STDIN_INSTRUCTION, CONTEXT_STDIN_TRANSPORT
            try:
                packet_path = path / "context-input.json"
                raw = packet_path.read_bytes()
                packet = json.loads(raw)
                if (transport != CONTEXT_STDIN_TRANSPORT
                        or len(contexts) != 1 or json.loads(contexts[0]) != CONTEXT_STDIN_INSTRUCTION
                        or not isinstance(receipt.get("prompt_path"), str)
                        or Path(receipt["prompt_path"]).resolve() != packet_path.resolve()
                        or hashlib.sha256(raw).hexdigest() != receipt.get("prompt_sha256")
                        or not isinstance(packet, dict) or set(packet) != {"required_context", "task_prompt"}
                        or not all(isinstance(value, str) for value in packet.values())):
                    raise ValueError("input envelope binding changed")
                task_prompt_sha = hashlib.sha256(packet["task_prompt"].encode("utf-8")).hexdigest()
                contexts = [json.dumps(packet["required_context"])]
            except (OSError, ValueError) as exc:
                raise ValueError("provider attempt preloaded context input changed or unavailable") from exc
        disabled = [command[i+1] for i, part in enumerate(command[:-1]) if part == "--disable"]
        if (metadata.get("preloaded_context_sha256") != binding["preloaded_context_sha256"]
                or len(contexts) != 1
                or hashlib.sha256(json.loads(contexts[0]).encode("utf-8")).hexdigest() != binding["preloaded_context_sha256"]
                or not {"shell_tool"}.issubset(disabled)):
            raise ValueError("provider attempt preloaded context or shell restriction changed")
    if task_prompt_sha != binding["prompt_sha256"] or receipt.get("response_schema_sha256") != binding["schema_sha256"]:
        raise ValueError("provider attempt input binding changed")
    for name, key in (("events.jsonl", "events_sha256"), ("stderr.log", "stderr_sha256")):
        if hash_file(path / name) != receipt.get(key):
            raise ValueError("provider attempt diagnostic bytes changed")
    if receipt.get("outcome") == "PROCESS_COMPLETED" and hash_file(path / "response.json") != receipt.get("response_sha256"):
        raise ValueError("provider response bytes changed")
    return receipt


def _check_context_files(binding):
    for record in binding.get("preloaded_context_files", []):
        try:
            unchanged = hash_file(Path(record["path"])) == record["sha256"]
        except OSError as exc:
            raise ValueError("provider job preloaded context unavailable") from exc
        if not unchanged:
            raise ValueError("provider job preloaded context changed")


def completed_recovery_record(failed: Path, completed: Path, binding: dict):
    """Verify an explicitly supplied completed repeat without restamping it."""
    original = _check_attempt(failed, binding)
    if ((failed / "response.json").exists() or not stopped_read_only_timeout(
            original, (failed / "events.jsonl").read_text(encoding="utf-8"))):
        raise ValueError("completed recovery requires a stopped read-only timeout without output")
    receipt = _check_attempt(completed, binding)
    def request_command(value, directory):
        command = list(value["command"])
        if command.count("--output-last-message") != 1:
            raise ValueError("completed recovery output binding changed")
        index = command.index("--output-last-message") + 1
        if index >= len(command) or Path(command[index]).resolve() != (directory / "response.json").resolve():
            raise ValueError("completed recovery output binding changed")
        command[index] = "<attempt-response>"
        return command
    if (receipt.get("outcome") != "PROCESS_COMPLETED" or receipt.get("exit_code") != 0
            or receipt.get("error") is not None
            or receipt.get("prompt_sha256") != original.get("prompt_sha256")
            or receipt.get("timeout_seconds") != original.get("timeout_seconds")
            or request_command(receipt, completed) != request_command(original, failed)):
        raise ValueError("completed recovery must be a completed repeat of the exact request")
    record = {"mode": "completed_same_request_recovery", "attempt_dir": str(completed.resolve()),
        "execution_receipt_sha256": hash_file(completed / "execution_receipt.json"),
        "failed_attempt_dir": str(failed.resolve()),
        "failed_execution_receipt_sha256": hash_file(failed / "execution_receipt.json")}
    return record, receipt


def _claim_retry(root, limit, job, attempt_id):
    with _lock(root / "budget.lock", wait_seconds=5):
        policy = root / "policy.json"
        expected = {"retry_limit": limit}
        if policy.exists():
            if _read(policy) != expected:
                raise ValueError("run retry budget changed")
        else:
            _new(policy, expected)
        claims = list(root.glob("claim-*.json"))
        claim = {"job": str(job.resolve()), "attempt_id": attempt_id}
        if any(_read(path) == claim for path in claims):
            return
        if len(claims) >= limit:
            raise ValueError("run retry budget exhausted")
        _new(root / f"claim-{len(claims)+1:06d}.json", claim)


def run_provider_job(*, job_dir: Path, attempt_root: Path, binding: dict,
                     launch, retry_budget_dir: Path, run_retry_limit: int,
                     max_retries: int = 1, retry_delay_seconds: float = 10,
                     sleep=time.sleep, completed_recovery: Path | None = None):
    """Return process completion or a failed job; callers still validate meaning.

    `launch(attempt_id)` runs the existing subscription-only runner. A crash
    after launch intent with no completion receipt is unknown and never retried.
    Retry claims count even when usage is missing or a later launch is refused.
    """
    if any(isinstance(x, bool) or not isinstance(x, int) or x < 0 for x in (max_retries, run_retry_limit)):
        raise ValueError("retry limits must be nonnegative integers")
    if not isinstance(retry_delay_seconds, (int, float)) or not 0 <= retry_delay_seconds <= 60:
        raise ValueError("retry delay must be finite and between zero and 60 seconds")
    if completed_recovery is not None and max_retries < 1:
        raise ValueError("completed recovery requires a retry allowance")
    if "preloaded_context_sha256" in binding:
        # Refuse an unusable envelope before freezing a job or recording launch intent.
        try:
            Path(binding["prompt_path"]).read_bytes().decode("utf-8")
        except (OSError, UnicodeError) as exc:
            raise ValueError("prompt must be UTF-8 text to accompany preloaded context; no generation launched") from exc
    policy = dict(binding=binding, max_retries=max_retries, run_retry_limit=run_retry_limit,
        retry_budget_dir=str(retry_budget_dir.resolve()), retry_delay_seconds=retry_delay_seconds,
        attempt_root=str(attempt_root.resolve()))
    with _lock(job_dir / "job.lock"):
        if completed_recovery is not None and not (attempt_root / (job_dir.name + "-attempt-001") / "execution_receipt.json").is_file():
            raise ValueError("completed recovery requires an existing original attempt; no generation launched")
        contract = job_dir / "binding.json"
        if contract.exists():
            if _read(contract) != policy:
                raise ValueError("provider job binding changed")
        else:
            _new(contract, policy)
        for index in range(max_retries + 1):
            for kind in ("codex", "runner"):
                path = binding["codex_executable"] if kind == "codex" else binding["runner_path"]
                if hash_file(Path(path)) != binding[kind + "_sha256"]:
                    raise ValueError("provider execution source changed")
            for kind in ("prompt", "schema"):
                if hash_file(Path(binding[kind + "_path"])) != binding[kind + "_sha256"]:
                    raise ValueError("provider job input changed")
            _check_context_files(binding)
            aid = job_dir.name + f"-attempt-{index+1:03d}"
            attempt = attempt_root / aid
            intent = job_dir / f"launch-{index+1:03d}.json"
            recovery_path = job_dir / "recovery-002.json"
            if index == 1 and (completed_recovery is not None or recovery_path.exists()):
                if intent.exists() or attempt.exists():
                    raise ValueError("second launch already recorded; completed recovery cannot replace it")
                saved = _read(recovery_path) if recovery_path.exists() else None
                completed = Path(saved["attempt_dir"]) if saved else completed_recovery.resolve(strict=True)
                if completed_recovery is not None and completed_recovery.resolve(strict=True) != completed:
                    raise ValueError("completed recovery binding changed")
                record, receipt = completed_recovery_record(attempt_root / (job_dir.name + "-attempt-001"), completed, binding)
                if saved is not None and saved != record:
                    raise ValueError("completed recovery receipt binding changed")
                _claim_retry(retry_budget_dir, run_retry_limit, job_dir, aid)
                if saved is None:
                    _new(recovery_path, record)
                return {"status": "PROCESS_COMPLETED_NOT_VALIDATED", "attempt_dir": str(completed),
                    "execution_receipt": receipt, "attempt_count": 2, "recovery": record}
            if (attempt / "execution_receipt.json").exists() and (
                not intent.exists() or _read(intent) != {"attempt_id": aid}
            ):
                raise ValueError("existing provider attempt does not belong to this job")
            if not (attempt / "execution_receipt.json").exists():
                if attempt.exists():
                    raise ValueError("provider launch outcome unknown; inspect preserved attempt before recovery")
                if intent.exists():
                    # Report absence, not a proven pre-launch refusal: the callable
                    # or missing artifacts cannot establish that nothing generated.
                    # Keep the intent and budget claim; never infer safe relaunch.
                    raise ValueError("provider launch intent exists but its attempt directory is missing; execution is unconfirmed; preserve the launch record and inspect launch diagnostics before recovery")
                if index:
                    _claim_retry(retry_budget_dir, run_retry_limit, job_dir, aid)
                    sleep(retry_delay_seconds)
                    for kind in ("codex", "runner"):
                        source_path = binding["codex_executable"] if kind == "codex" else binding["runner_path"]
                        if hash_file(Path(source_path)) != binding[kind + "_sha256"]:
                            raise ValueError("provider execution source changed during retry delay")
                    for kind in ("prompt", "schema"):
                        if hash_file(Path(binding[kind + "_path"])) != binding[kind + "_sha256"]:
                            raise ValueError("provider job input changed during retry delay")
                    _check_context_files(binding)
                _new(intent, {"attempt_id": aid})
                launch(aid)
                if not (attempt / "execution_receipt.json").exists():
                    raise ValueError("provider launch returned no execution receipt; authentication or launch failure is not retryable")
            receipt = _check_attempt(attempt, binding)
            if receipt["outcome"] == "PROCESS_COMPLETED":
                if completed_recovery is not None or recovery_path.exists():
                    raise ValueError("unused completed recovery; original job already completed")
                return {"status": "PROCESS_COMPLETED_NOT_VALIDATED", "attempt_dir": str(attempt),
                    "execution_receipt": receipt, "attempt_count": index+1}
            cause = transient_failure(receipt, (attempt / "events.jsonl").read_text(encoding="utf-8"),
                (attempt / "stderr.log").read_text(encoding="utf-8"))
            if receipt["outcome"] == "TIMED_OUT" and (attempt / "response.json").exists():
                cause = None
            if cause is None or index == max_retries:
                if completed_recovery is not None or recovery_path.exists():
                    raise ValueError("completed recovery requires an eligible failed attempt and retry allowance")
                return {"status": "JOB_FAILED", "attempt_dir": str(attempt), "cause": cause or "unclassified",
                    "attempt_count": index+1, "execution_receipt": receipt}
        raise AssertionError("unreachable provider job state")
