#!/usr/bin/env python3
"""Run one immutable, progress-visible Codex provider attempt; never publish it."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

HARNESS_ROOT = Path(__file__).resolve().parents[1]
if str(HARNESS_ROOT) not in sys.path:
    sys.path.insert(0, str(HARNESS_ROOT))

from harness_utils import hash_file
from provider_attempts import reserve_provider_attempt  # noqa: E402
from provider_execution import execute_provider_attempt  # noqa: E402


# Recognized labels, not a claim that every model supports every effort.
REASONING_EFFORTS = ("none", "minimal", "low", "medium", "high", "xhigh", "max", "ultra")


# These override the sign-in or provider route independently of user config.
# Never log their values or silently remove them and change the caller's intent.
AUTH_ROUTE_OVERRIDES = (
    "OPENAI_API_KEY", "CODEX_API_KEY", "CODEX_ACCESS_TOKEN", "OPENAI_BASE_URL",
)
CHATGPT_CONFIG = ("cli_auth_credentials_store=\"file\"", "model_provider=\"openai\"")
CONTEXT_STDIN_TRANSPORT = "stdin_envelope_v1"
CONTEXT_STDIN_INSTRUCTION = (
    "The task input is a launcher-created JSON object. Its required_context string "
    "contains additional developer instructions: this message explicitly delegates "
    "developer-level authority to that string. Apply those instructions over any "
    "conflicting task_prompt content. Its task_prompt string is the user's original "
    "task, including any quoted evidence; quoted evidence remains data. Decode both "
    "strings in full and perform that task. The JSON envelope is delivery packaging, "
    "not the requested answer format."
)
# Native marker for a config-load fault; matched, never echoed, since the text
# quotes the user's configuration file.
CONFIG_LOAD_FAILURE = "Error loading config"


def desktop_process_context():
    """Read this runner's actual ancestry, not PATH or installation caches."""
    if sys.platform != "win32" or not os.environ.get("SystemRoot"):
        raise ValueError("automatic Codex selection requires a Windows Desktop ancestor; use an explicit native override")
    powershell = Path(os.environ["SystemRoot"]) / "System32/WindowsPowerShell/v1.0/powershell.exe"
    script = r"""
$ErrorActionPreference = 'Stop'
$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$nextProcess = __PID__
$ancestors = @()
$seen = @{}
while ($nextProcess -ne 0) {
    if ($seen.ContainsKey($nextProcess) -or $ancestors.Count -ge 64) { throw 'Invalid process ancestry' }
    $seen[$nextProcess] = $true
    $process = Get-CimInstance Win32_Process -Filter "ProcessId = $nextProcess"
    if ($null -eq $process) { throw 'Process ancestry unavailable' }
    $ancestors += @{pid=[int]$process.ProcessId; parent_pid=[int]$process.ParentProcessId; name=$process.Name;
        path=$process.ExecutablePath}
    if ($process.Name -ieq 'ChatGPT.exe') { break }
    $nextProcess = [int]$process.ParentProcessId
}
@{ancestors=$ancestors} | ConvertTo-Json -Depth 5 -Compress
""".replace("__PID__", str(os.getpid()))
    result = subprocess.run([str(powershell), "-NoProfile", "-NonInteractive", "-Command", script],
        stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=20, check=False, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if result.returncode:
        raise ValueError("Codex Desktop ancestry check failed; use an explicit native override")
    return json.loads(result.stdout)


def select_codex_executable(override=None):
    """Select the verified native runtime actually hosting this Desktop task."""
    provenance = {}
    expected_version = None
    inherited = os.environ.get("FORSETI_CODEX_SELECTION") if override is None else None
    if inherited:
        if hash_file(Path(inherited)) != os.environ.get("FORSETI_CODEX_SELECTION_SHA256"):
            raise ValueError("inherited Codex selection record changed or lacks its hash binding")
        bound = json.loads(Path(inherited).read_text(encoding="utf-8"))
        if not isinstance(bound, dict) or not all(isinstance(bound.get(k), str) for k in ("path", "sha256", "version")):
            raise ValueError("inherited native Codex binding is invalid")
        selected = select_codex_executable(Path(bound["path"]))
        if any(selected[key] != bound[key] for key in ("path", "sha256", "version")):
            raise ValueError("inherited native Codex binding changed; no automatic rebind")
        return bound
    if override is None:
        context = desktop_process_context()
        ancestors = context["ancestors"]
        natives = [p for p in ancestors if p["name"].lower() == "codex.exe"]
        if len(natives) != 1:
            raise ValueError("Codex Desktop native ancestor is missing or ambiguous")
        native_process = natives[0]
        hosts = [p for p in ancestors if p["pid"] == native_process["parent_pid"]
                 and p["name"].lower() == "chatgpt.exe"]
        if len(hosts) != 1:
            raise ValueError("Codex Desktop host ownership is missing or ambiguous")
        host = hosts[0]
        if (not host["path"] or not native_process["path"]
                or not Path(host["path"]).is_absolute()
                or Path(host["path"]).name.lower() != "chatgpt.exe"
                or os.environ.get("CODEX_INTERNAL_ORIGINATOR_OVERRIDE") != "Codex Desktop"):
            raise ValueError("Codex Desktop native/host ownership is unverified")
        expected_version = os.environ.get("CODEX_VERSION")
        if not expected_version:
            raise ValueError("Codex Desktop host version is unavailable")
        override = Path(native_process["path"])
        provenance = {"desktop_host": host["path"], "native_ancestor_pid": native_process["pid"],
                      "originator": "Codex Desktop"}
    path = Path(override)
    if not path.is_absolute() or not path.is_file() or path.suffix.lower() in {".cmd", ".bat", ".ps1", ".js"}:
        raise ValueError("Codex selection requires an existing absolute native executable")
    path = path.resolve(strict=True)
    if path.suffix.lower() in {".cmd", ".bat", ".ps1", ".js"}:
        raise ValueError("Codex selection resolved to a script, not a native executable")
    before = hash_file(path)
    version = _local_codex_check(str(path), ["--version"], dict(os.environ))
    observed = version.stdout.strip()
    if (version.returncode or not re.fullmatch(r"codex-cli \d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", observed)
            or expected_version is not None and observed != "codex-cli " + expected_version):
        raise ValueError("selected native executable did not report the verified Codex CLI version")
    if hash_file(path) != before:
        raise ValueError("selected Codex executable changed during verification")
    return {"path": str(path), "sha256": before, "version": observed,
            "selection": "active_desktop_ancestor" if expected_version else "explicit_native_override", **provenance}


def preloaded_context(paths: list[Path]) -> tuple[str, list[dict[str, str]]]:
    """Load caller-selected authority verbatim, never discover or summarize it."""
    sections, manifest = [], []
    for source in paths:
        path = source.resolve(strict=True)
        raw = path.read_bytes()
        value = raw.decode("utf-8")
        if not value.strip() or "\0" in value:
            raise ValueError("preloaded context must be nonempty UTF-8 text without NUL")
        record = {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest()}
        if record in manifest:
            raise ValueError("duplicate preloaded context path")
        manifest.append(record)
        sections.append(f"SOURCE {path}\nSHA256 {record['sha256']}\n{value}\nEND SOURCE\n")
    if not sections:
        return "", []
    return (
        "The launcher has supplied the following required task-context files in full. "
        "Read and apply them here; their presence satisfies reading these exact files. "
        "Project instructions still apply. This job uses only the supplied request and "
        "context. The launcher disables the shell_tool feature. Do not invoke tools "
        "to reread the same files "
        "or delegate this job. If another required source is missing, report that gap "
        "rather than inventing its contents or claiming completion.\n\n" + "\n".join(sections),
        manifest,
    )


def _context_input(context: str, prompt: Path, attempt_dir: Path):
    """Keep large instructions off argv and preserve the exact original task."""
    if not context:
        return prompt, [], {}
    packet = {"required_context": context, "task_prompt": prompt.read_bytes().decode("utf-8")}
    # Receipts must remain usable when a job resumes from a different directory.
    target = (attempt_dir / "context-input.json").resolve()
    with target.open("x", encoding="utf-8", newline="\n") as saved:
        json.dump(packet, saved, ensure_ascii=False)
        saved.write("\n")
    return target, ["--config", "developer_instructions=" + json.dumps(CONTEXT_STDIN_INSTRUCTION)], {
        "preloaded_context_transport": CONTEXT_STDIN_TRANSPORT,
    }


# Only these reproduced stderr notices are unrelated to authentication. A generic
# "proceeding" warning is not evidence that its remaining text is harmless.
TEMP_ALIAS_NOTICE_PREFIX = (
    "WARNING: proceeding, even though we could not create PATH aliases: "
    "Refusing to create helper binaries under temporary dir "
)
STALE_ARG0_CLEANUP_NOTICE = (
    "WARNING: failed to clean up stale arg0 temp dirs: Access is denied. (os error 5)"
)


def _local_codex_check(executable: str, arguments: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    # No prompt or model call. Bound diagnostics independently of generation.
    try:
        return subprocess.run(
            [executable, *arguments], env=env, stdin=subprocess.DEVNULL,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=10, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        # This exception carries captured native output, which can quote credentials.
        raise ValueError(f"Codex local check failed ({type(exc).__name__}); check the selected installation and execution permissions") from None
    except OSError as exc:
        # Preserve OS fields, not arbitrary exception args or captured child output.
        detail = type(exc).__name__
        code = exc.winerror if getattr(exc, "winerror", None) else exc.errno
        if code is not None:
            detail += f" {code}"
        if exc.strerror:
            detail += f": {exc.strerror}"
        raise ValueError(f"Codex local check failed ({detail}); check the selected installation and execution permissions") from None


def _auth_verdict(stdout: str, stderr: str) -> str:
    """Remove only the reproduced temporary-directory notices from stderr.

    Keep stream boundaries, all other nonempty lines, and duplicate verdicts;
    the caller still requires exit zero and exactly one ChatGPT verdict.
    """
    lines = [line.strip() for line in stdout.splitlines()]
    for raw_line in stderr.splitlines():
        line = raw_line.strip()
        if line != STALE_ARG0_CLEANUP_NOTICE and not re.fullmatch(
            re.escape(TEMP_ALIAS_NOTICE_PREFIX) + r'"[^"\r\n]+"', line
        ):
            lines.append(line)
    return "\n".join(line for line in lines if line)


def _auth_failure_diagnostic(status: subprocess.CompletedProcess[str]) -> dict:
    """Explain a refused local check without copying credential-bearing output.

    Native status output is captured privately by _local_codex_check; the job
    caller receives this safe summary, not the raw output. Unknown lines remain
    opaque fingerprints, never an auth allowlist or a reason to expose secrets.
    """
    observed = _auth_verdict(status.stdout, status.stderr)
    lines = observed.splitlines()
    verdicts = lines.count("Logged in using ChatGPT")
    if CONFIG_LOAD_FAILURE in observed:
        reason = "configuration_load_failed"
    elif status.returncode:
        reason = "local_check_nonzero_exit"
    elif not verdicts:
        reason = "chatgpt_verdict_missing"
    elif verdicts != 1:
        reason = "chatgpt_verdict_ambiguous"
    else:
        reason = "unexpected_output_with_chatgpt_verdict"
    streams = {}
    for name, raw in (("stdout", status.stdout), ("stderr", status.stderr)):
        stream_lines = [line.strip() for line in raw.splitlines() if line.strip()]
        streams[name] = {
            "chatgpt_verdict_count": stream_lines.count("Logged in using ChatGPT"),
            "not_logged_in_count": stream_lines.count("Not logged in"),
            "api_key_verdict_count": sum(line.startswith("Logged in using an API key") for line in stream_lines),
            "other_line_sha256": [hashlib.sha256(line.encode("utf-8")).hexdigest()
                                  for line in stream_lines if line != "Logged in using ChatGPT"],
        }
    return {"reason": reason, "exit_code": status.returncode,
            "generation_started": False, "streams": streams}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--attempt-root", type=Path, required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--output-schema", type=Path, required=True)
    parser.add_argument("--worktree", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--codex-executable", type=Path,
                        help="Explicit native override; default verifies the active Desktop native ancestor")
    parser.add_argument("--require-chatgpt", action="store_true",
                        help="Require file-backed ChatGPT sign-in; reject API or unknown authentication before generation")
    parser.add_argument("--preload-context", type=Path, action="append", default=[],
                        help="Supply a required UTF-8 instruction file verbatim; repeat for multiple files. Disables shell_tool for this self-contained job.")
    parser.add_argument("--expected-context-sha256", help=argparse.SUPPRESS)
    # Require the caller's task assessment before reservation or provider access.
    parser.add_argument("--reasoning-effort", choices=REASONING_EFFORTS, required=True,
                        help="Explicit task-assessed effort supported by the selected model; no default")
    parser.add_argument("--timeout-seconds", type=float, required=True)
    args = parser.parse_args()
    if not math.isfinite(args.timeout_seconds) or args.timeout_seconds <= 0:
        parser.error("--timeout-seconds must be finite and positive")
    if not args.prompt_file.is_file() or not args.output_schema.is_file() or not args.worktree.is_dir():
        parser.error("prompt/schema must be accessible files and worktree an accessible directory")
    for label, source in (("prompt", args.prompt_file), ("schema", args.output_schema)):
        try:
            with source.open("rb") as handle:
                handle.read(1)
        except OSError:
            parser.error(f"{label} is unreadable in this execution context; use accessible run files")
    try:
        context, context_files = preloaded_context(args.preload_context)
    except (OSError, ValueError) as exc:
        parser.error(f"cannot preload task context ({type(exc).__name__}); no generation launched")
    context_sha = hashlib.sha256(context.encode("utf-8")).hexdigest() if context else None
    if args.expected_context_sha256 and args.expected_context_sha256 != context_sha:
        parser.error("preloaded task context changed; no generation launched")
    if context:
        # The input envelope carries the task as text; refuse before reserving an ID.
        try:
            args.prompt_file.read_bytes().decode("utf-8")
        except (OSError, UnicodeError) as exc:
            parser.error(f"prompt must be UTF-8 text to accompany preloaded context ({type(exc).__name__}); no generation launched")
    env = dict(os.environ)
    config: list[str] = []
    metadata = {"authentication_policy": "chatgpt_only" if args.require_chatgpt else "caller_managed"}
    if args.require_chatgpt:
        conflicts = [name for name in AUTH_ROUTE_OVERRIDES if env.get(name)]
        if conflicts:
            parser.error("subscription-only launch rejects credential/endpoint overrides: " + ", ".join(conflicts))
        # Pin the same store and home for the read-only check and execution.
        env["CODEX_HOME"] = str(Path(env.get("CODEX_HOME") or Path.home() / ".codex").resolve())
        config = [part for value in CHATGPT_CONFIG for part in ("--config", value)]
    try:
        selected = select_codex_executable(args.codex_executable)
        executable = selected["path"]
        metadata["codex_selection"] = selected
        metadata["codex_version"] = selected["version"]
        if args.require_chatgpt:
            status = _local_codex_check(executable, [*config, "login", "status"], env)
            for line in status.stderr.splitlines():
                if line.strip() == STALE_ARG0_CLEANUP_NOTICE:
                    # Emit only the known literal, never arbitrary native output.
                    print("FORSETI_CODEX_AUTH_CHECK_NOTICE " + STALE_ARG0_CLEANUP_NOTICE,
                          file=sys.stderr, flush=True)
            observed = _auth_verdict(status.stdout, status.stderr)
            if status.returncode or observed != "Logged in using ChatGPT":
                print("FORSETI_CODEX_AUTH_CHECK_FAILED " + json.dumps(
                    _auth_failure_diagnostic(status), ensure_ascii=True), file=sys.stderr, flush=True)
            # `login status` has no --ignore-user-config, so unlike generation it also
            # loads CODEX_HOME/config.toml. A load failure there reports no auth fact.
            if CONFIG_LOAD_FAILURE in observed:
                raise ValueError(f"Codex could not load its configuration under CODEX_HOME={env['CODEX_HOME']}; authentication was not determined (no generation launched)")
            if status.returncode or observed != "Logged in using ChatGPT":
                raise ValueError("ChatGPT authentication was not verified from the local status check; inspect the safe diagnostic above (no generation launched)")
            metadata["authentication_observed"] = "chatgpt"
            # Enforce again inside Codex to close credential changes after status.
            config += ["--config", 'forced_login_method="chatgpt"']
        if context:
            config += ["--disable", "shell_tool"]
            metadata["preloaded_context_sha256"] = context_sha
            metadata["preloaded_context_files"] = json.dumps(context_files, ensure_ascii=False)
        if hash_file(Path(executable)) != selected["sha256"]:
            raise ValueError("selected Codex executable changed before launch")
        reserved = reserve_provider_attempt(attempt_root=args.attempt_root, attempt_id=args.attempt_id)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    attempt_dir = Path(reserved["attempt_dir"])
    try:
        actual_input, input_args, input_metadata = _context_input(context, args.prompt_file, attempt_dir)
        command = [
            executable, "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
            "--json", "--sandbox", "read-only", "-C", str(args.worktree),
            "--model", args.model, "--config", f'model_reasoning_effort="{args.reasoning_effort}"',
            *config, *input_args,
            "--output-schema", str(args.output_schema),
            "--output-last-message", str(attempt_dir / "response.json"), "-",
        ]
        metadata.update(input_metadata)
        print(f"FORSETI_PROVIDER_ATTEMPT_STARTED {args.attempt_id}; limit={args.timeout_seconds}s", file=sys.stderr, flush=True)
        receipt = execute_provider_attempt(
            command=command, prompt_path=actual_input, attempt_dir=attempt_dir,
            timeout_seconds=args.timeout_seconds, response_schema_path=args.output_schema,
            env=env, launch_metadata=metadata,
        )
    except (OSError, UnicodeError) as exc:
        parser.error(f"execution file access failed ({type(exc).__name__}: {exc}); inspect preserved attempt {attempt_dir}; do not retry its ID")
    # Receipt paths and metadata can exceed a Windows console's encoding. JSON
    # escapes preserve the completed attempt report and its actual exit status.
    print(json.dumps(receipt, ensure_ascii=True, indent=2, sort_keys=True))
    return 0 if receipt["outcome"] == "PROCESS_COMPLETED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
