"""Execute native judgment jobs through the maintained, subscription-only runner."""
from __future__ import annotations

import json
import math
import os
from pathlib import Path
import subprocess
import sys
from jsonschema.exceptions import ValidationError

from harness_utils import hash_file
from provider_jobs import _lock
from provider_attempts import unique_json_object
from runners.run_codex_provider_attempt import DIRECT_JUDGMENT_INSTRUCTION


def execution_request(job_path, job_sha256):
    return {"command": "execute-judgment-job", "job_path": str(job_path),
            "job_sha256": job_sha256, "transport": "direct_provider_v1"}


def direct_input_tokens(prompt, schema, count):
    # The consumer prompt already contains its required context. Reserve the
    # exact additional developer instruction and separately supplied schema.
    return count(prompt) + count(json.dumps(schema, ensure_ascii=False, sort_keys=True)) + count(DIRECT_JUDGMENT_INSTRUCTION)


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=unique_json_object)


def _attempt_dir(provider_root, job_sha256):
    # The only attempt a direct job may own: no retries are configured.
    return Path(provider_root).resolve() / job_sha256 / "attempts" / "job-attempt-001"


def execute_judgment_job(*, job_path, job_sha256, provider_root, model, reasoning_effort,
                         timeout_seconds, codex_executable=None):
    """One provider attempt; restart reuses the existing provider job/answer.

    A failed or unknown attempt stays failed. The provider job's durable intent
    protects the launch-to-result gap; native submit protects publication.
    """
    from runners import run_semantic_evidence_integration as native
    if not model or not reasoning_effort or not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
        raise ValueError("direct execution requires a model, effort and positive finite timeout")
    job_path = Path(job_path).resolve(strict=True)
    job, inputs = native._load_judgment_job(job_path, job_sha256)
    directory = Path(provider_root).resolve() / job_sha256
    with _lock(directory / "execution.lock"):
        consumer = job.get("version") == "complete_case_consumer_request_v1"
        target = job_path.with_name("response.json") if consumer else Path(job["response_path"])
        if target.exists():
            result = native.submit_judgment_job(job_path=job_path, expected_sha256=job_sha256, response_path=target)
            result.pop("model_api_calls", None)
            return result
        if consumer and target.with_name("response.receipt.json").exists():
            raise ValueError("accepted consumer response missing; restore it without rejudging")
        if not consumer and (job_path.with_suffix(".receipt.json").exists() or target.with_name(target.name + ".tmp").exists()):
            raise ValueError("missing accepted response or staged submission; explicit recovery required")
        context_paths = []
        if consumer:
            prompt, schema = job["prompt"].encode("utf-8"), job["schema"]
            from runners.finite_preparation import offline_tokenizer
            tokenizer, _ = offline_tokenizer(job["capacity"]["encoding"])
            total = direct_input_tokens(job["prompt"], schema,
                lambda s: len(tokenizer.encode(s, disallowed_special=())))
            total += job["capacity"]["output_reserve_tokens"] + job["capacity"]["other_overhead_reserve_tokens"]
            if total > job["capacity"]["effective_context_tokens"]:
                raise ValueError("consumer direct delivery exceeds reserved capacity; no generation launched")
        else:
            prompt, schema = inputs["prompt"], json.loads(inputs["response_schema"])
            for name in ("agents", "overlay", "preflight_defaults", "claim_support"):
                path = directory / (name + ".md")
                native._retain_advance_artifact(path, inputs[name], raw=True)
                context_paths.append(path)
        prompt_path, schema_path = directory / "prompt.md", directory / "schema.json"
        native._retain_advance_artifact(prompt_path, prompt, raw=True)
        native._retain_advance_artifact(schema_path, schema)
        runner = Path(__file__).with_name("run_codex_provider_job.py")
        command = [sys.executable, str(runner), "--job-dir", str(directory / "job"),
            "--attempt-root", str(directory / "attempts"), "--retry-budget-dir", str(directory / "retry-budget"),
            "--run-retry-limit", "0", "--max-retries", "0", "--prompt-file", str(prompt_path),
            "--output-schema", str(schema_path), "--worktree", str(runner.parents[2]),
            "--model", model, "--reasoning-effort", reasoning_effort,
            "--timeout-seconds", str(timeout_seconds), "--direct-judgment"]
        if codex_executable is not None:
            command += ["--codex-executable", str(codex_executable)]
        for path in context_paths:
            command += ["--preload-context", str(path)]
        # Binding is checked even when an earlier result exists, so changed
        # model/effort/input cannot adopt an unrelated saved answer.
        native._retain_advance_artifact(directory / "execution.json", {
            "job_path": str(job_path), "job_sha256": job_sha256, "command": command,
            "prompt_sha256": hash_file(prompt_path), "schema_sha256": hash_file(schema_path)})
        result_path = directory / "provider-result.json"
        if not result_path.exists():
            index = len(list(directory.glob("invoke-*.stdout"))) + 1
            with (directory / f"invoke-{index:03d}.stdout").open("xb") as out, (directory / f"invoke-{index:03d}.stderr").open("xb") as err:
                process = subprocess.run(command + ["--result-out", str(result_path)],
                    cwd=runner.parents[1], stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                    check=False, env=dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1"),
                    creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            if process.returncode:
                raise ValueError(f"provider job failed or unknown; preserve and inspect {directory}")
        result = _read(result_path)
        if result.get("status") != "PROCESS_COMPLETED_NOT_VALIDATED":
            raise ValueError(f"provider did not complete; no retry: {result_path}")
        # Revalidate the maintained runner's saved result/attempt bindings before
        # native submission, including recovery after completion but before submit.
        from provider_jobs import _check_attempt
        policy = _read(directory / "job" / "binding.json")
        attempt = Path(result["attempt_dir"])
        if attempt.resolve() != _attempt_dir(provider_root, job_sha256) or result.get("attempt_count") != 1:
            raise ValueError("direct provider result has a foreign attempt or retry")
        receipt = _check_attempt(attempt, policy["binding"])
        if receipt != result.get("execution_receipt") or receipt.get("outcome") != "PROCESS_COMPLETED":
            raise ValueError("direct provider result differs from its execution receipt")
        # Fail visibly if a provider ever escapes the supplied-input role.
        for line in (attempt / "events.jsonl").read_text(encoding="utf-8").splitlines():
            event = json.loads(line)
            if event.get("type") in {"item.started", "item.completed", "item.updated"}:
                kind = event.get("item", {}).get("type")
                if kind not in {"reasoning", "agent_message"}:
                    raise ValueError(f"direct judgment used a non-judgment item: {kind}")
        submitted = native.submit_judgment_job(job_path=job_path, expected_sha256=job_sha256,
                                             response_path=attempt / "response.json")
        submitted.pop("model_api_calls", None)
        return {**submitted, "provider_result_path": str(result_path)}


def execute_semantic_run(*, advance_kwargs, model, reasoning_effort, timeout_seconds,
                         max_jobs, codex_executable=None):
    """Drive the ordinary advance/submit loop in code with an explicit job bound."""
    from runners import run_semantic_evidence_integration as native
    if isinstance(max_jobs, bool) or not isinstance(max_jobs, int) or max_jobs < 1:
        raise ValueError("--execute requires a positive --max-jobs bound")
    if not model or not reasoning_effort or timeout_seconds is None or not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
        raise ValueError("--execute requires model, reasoning effort and positive finite timeout")
    root = Path(advance_kwargs["run_dir"]).resolve()
    completed = []
    # Count newly recorded launch attempts, including refusals and unknown
    # outcomes. An intent without an attempt directory is still not proof of
    # zero execution. This count is not model-call or token-usage accounting.
    launched = 0
    with _lock(root / "execution.lock"):
        while True:
            state = native.advance_semantic_run(**advance_kwargs)
            state.pop("model_api_calls", None)  # advance's zero covers preparation only
            state["executed_job_count"] = launched
            state["provider_root"] = str(root / "provider")
            requests = state.get("judgment_requests", [])
            if state["status"] != "SEMANTIC_JUDGMENT_REQUIRED" or not requests:
                return state
            if len(completed) == max_jobs:
                state.update(status="SEMANTIC_EXECUTION_LIMIT_REACHED",
                    action="Configured job bound reached; no further judgments launched.")
                return state
            for request in requests[:max_jobs - len(completed)]:
                intent = root / "provider" / request["job_sha256"] / "job" / "launch-001.json"
                existed = intent.exists()
                try:
                    result = execute_judgment_job(job_path=Path(request["job_path"]),
                        job_sha256=request["job_sha256"], provider_root=root / "provider",
                        model=model, reasoning_effort=reasoning_effort, timeout_seconds=timeout_seconds,
                        codex_executable=codex_executable)
                except (OSError, ValueError, ValidationError) as exc:
                    return {"status": "SEMANTIC_EXECUTION_BLOCKED", "error": str(exc),
                        "executed_job_count": launched + (not existed and intent.exists()),
                        "failed_job": request["job_path"],
                        "provider_root": str(root / "provider"), "judgment_requests": []}
                launched += not existed and intent.exists()
                completed.append(result)
