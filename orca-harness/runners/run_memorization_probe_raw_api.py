from __future__ import annotations

import argparse
import json
import os
from enum import StrEnum
from pathlib import Path
import sys
from typing import Any, Protocol
from urllib.parse import urlparse
from urllib import request
from urllib.error import HTTPError, URLError

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness_utils import write_yaml_file
from runners.run_memorization_probe import build_isolation_evidence, build_probe_artifact, build_probe_prompt
from schemas.probe_models import (
    ExecutionSurface,
    MemorizationProbeArtifact,
    ParsedProbeResponse,
    ProbeInput,
    ToolAccessPolicy,
    ToolCallTraceStatus,
    ToolConfigEvidenceKind,
)


class RawApiProvider(StrEnum):
    OPENAI_RESPONSES = "openai_responses"
    ANTHROPIC_MESSAGES = "anthropic_messages"


class JsonTransport(Protocol):
    def post_json(self, url: str, headers: dict[str, str], body: dict[str, Any], timeout_seconds: float) -> str:
        """Return the raw response body text."""


class UrllibJsonTransport:
    def post_json(self, url: str, headers: dict[str, str], body: dict[str, Any], timeout_seconds: float) -> str:
        request_body = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        req = request.Request(url, data=request_body, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=timeout_seconds) as response:
                return response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ValueError(f"Provider HTTP error {exc.code}: {_redact_header_secrets(detail, headers)}") from exc
        except URLError as exc:
            raise ValueError(f"Provider request failed: {exc.reason}") from exc


FORBIDDEN_REQUEST_KEYS = {
    "attachment",
    "attachments",
    "available_tools",
    "browser",
    "connector",
    "connectors",
    "developer",
    "document",
    "documents",
    "file",
    "file_ids",
    "file_search",
    "files",
    "function_call",
    "functions",
    "instructions",
    "knowledge_base",
    "mcp_server",
    "mcp_servers",
    "plugin",
    "plugins",
    "retrieval",
    "retrieval_config",
    "search",
    "system",
    "tool",
    "tool_choice",
    "tools",
    "url",
    "urls",
    "vector_store_ids",
    "web_search",
    "web_search_options",
    "workspace",
    "workspace_id",
}

OPENAI_ALLOWED_TOP_LEVEL_KEYS = {"input", "max_output_tokens", "model", "temperature"}
ANTHROPIC_ALLOWED_TOP_LEVEL_KEYS = {"max_tokens", "messages", "model", "temperature"}
STANDARD_PROVIDER_ENDPOINTS = {
    RawApiProvider.OPENAI_RESPONSES: ("api.openai.com", "/v1/responses"),
    RawApiProvider.ANTHROPIC_MESSAGES: ("api.anthropic.com", "/v1/messages"),
}


def build_provider_request(
    *,
    provider: RawApiProvider,
    probe_input: ProbeInput,
    max_tokens: int,
    temperature: float | None = None,
) -> dict[str, Any]:
    prompt = build_probe_prompt(probe_input)
    if provider == RawApiProvider.OPENAI_RESPONSES:
        body: dict[str, Any] = {
            "model": probe_input.probe_model_id,
            "input": prompt,
            "max_output_tokens": max_tokens,
        }
    elif provider == RawApiProvider.ANTHROPIC_MESSAGES:
        body = {
            "model": probe_input.probe_model_id,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
    else:
        raise ValueError(f"Unsupported raw API provider: {provider}")

    if temperature is not None:
        body["temperature"] = temperature
    validate_provider_request_shape(provider, body, prompt)
    return body


def validate_provider_request_shape(provider: RawApiProvider, body: dict[str, Any], prompt: str) -> None:
    forbidden_paths = find_forbidden_request_keys(body)
    if forbidden_paths:
        joined = ", ".join(forbidden_paths)
        raise ValueError(f"Raw no-tools request includes forbidden tool/context key(s): {joined}")

    if provider == RawApiProvider.OPENAI_RESPONSES:
        unexpected = sorted(set(body) - OPENAI_ALLOWED_TOP_LEVEL_KEYS)
        if unexpected:
            raise ValueError(f"Unexpected OpenAI raw request key(s): {', '.join(unexpected)}")
        if body.get("input") != prompt:
            raise ValueError("OpenAI raw request input must equal the generated probe prompt exactly")
    elif provider == RawApiProvider.ANTHROPIC_MESSAGES:
        unexpected = sorted(set(body) - ANTHROPIC_ALLOWED_TOP_LEVEL_KEYS)
        if unexpected:
            raise ValueError(f"Unexpected Anthropic raw request key(s): {', '.join(unexpected)}")
        messages = body.get("messages")
        if messages != [{"role": "user", "content": prompt}]:
            raise ValueError("Anthropic raw request must contain exactly one user message with the probe prompt")
    else:
        raise ValueError(f"Unsupported raw API provider: {provider}")

    if not isinstance(body.get("model"), str) or not body["model"].strip():
        raise ValueError("Raw request model id must be a non-empty string")


def validate_standard_provider_endpoint(provider: RawApiProvider, api_url: str) -> None:
    expected_host, expected_path = STANDARD_PROVIDER_ENDPOINTS[provider]
    parsed = urlparse(api_url)
    if parsed.scheme != "https" or parsed.hostname != expected_host or parsed.path != expected_path:
        raise ValueError(
            "Raw no-tools isolation is proven only for the standard "
            f"{provider.value} endpoint https://{expected_host}{expected_path}"
        )
    if parsed.params or parsed.query or parsed.fragment:
        raise ValueError("Raw no-tools provider endpoint must not include params, query, or fragment")


def find_forbidden_request_keys(value: Any, path: str = "$") -> list[str]:
    matches: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            key_path = f"{path}.{key_text}"
            if key_text.lower() in FORBIDDEN_REQUEST_KEYS:
                matches.append(key_path)
            matches.extend(find_forbidden_request_keys(item, key_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            matches.extend(find_forbidden_request_keys(item, f"{path}[{index}]"))
    return matches


def build_provider_headers(provider: RawApiProvider, api_key: str) -> dict[str, str]:
    if not api_key.strip():
        raise ValueError("API key must be non-empty")
    if provider == RawApiProvider.OPENAI_RESPONSES:
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
    if provider == RawApiProvider.ANTHROPIC_MESSAGES:
        return {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
    raise ValueError(f"Unsupported raw API provider: {provider}")


def extract_model_text(provider: RawApiProvider, raw_response_body: str) -> str:
    try:
        response_data = json.loads(raw_response_body)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Provider response was not JSON: {exc}") from exc

    if provider == RawApiProvider.OPENAI_RESPONSES:
        text = _extract_openai_response_text(response_data)
    elif provider == RawApiProvider.ANTHROPIC_MESSAGES:
        text = _extract_anthropic_response_text(response_data)
    else:
        raise ValueError(f"Unsupported raw API provider: {provider}")

    if not text.strip():
        raise ValueError("Provider response did not contain non-empty model text")
    return text


def extract_model_snapshot_if_available(raw_response_body: str) -> str | None:
    try:
        response_data = json.loads(raw_response_body)
    except json.JSONDecodeError:
        return None
    if not isinstance(response_data, dict):
        return None
    system_fingerprint = response_data.get("system_fingerprint")
    if isinstance(system_fingerprint, str) and system_fingerprint.strip():
        return f"system_fingerprint:{system_fingerprint}"
    response_model = response_data.get("model")
    if isinstance(response_model, str) and response_model.strip():
        return response_model
    return None


def run_memorization_probe_raw_api(
    *,
    probe_input_path: Path,
    output_path: Path,
    provider: RawApiProvider,
    api_url: str,
    api_key: str,
    transport: JsonTransport,
    timeout_seconds: float = 60.0,
    max_tokens: int = 512,
    temperature: float | None = None,
    reviewed_by_operator: bool = False,
) -> MemorizationProbeArtifact:
    """Run an authorized raw-API probe; CLI accidental-live-call guard is in main()."""

    probe_input = ProbeInput.model_validate(_load_yaml(probe_input_path))
    probe_prompt = build_probe_prompt(probe_input)
    validate_standard_provider_endpoint(provider, api_url)
    request_body = build_provider_request(
        provider=provider,
        probe_input=probe_input,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    headers = build_provider_headers(provider, api_key)
    raw_response_body = transport.post_json(api_url, headers, request_body, timeout_seconds)
    model_text = extract_model_text(provider, raw_response_body)
    parsed_response = parse_provider_model_text(model_text)
    isolation = build_isolation_evidence(
        execution_surface=ExecutionSurface.RAW_API_NO_TOOLS,
        tool_access_policy=ToolAccessPolicy.NO_TOOLS,
        tool_config_evidence=(
            "raw API request body supplied only model/provider control fields and the generated "
            "public-identifiers probe prompt; no tool, search, retrieval, browser, file, attachment, "
            "workspace, system, developer, or hidden-context fields were supplied"
        ),
        tool_config_evidence_kind=ToolConfigEvidenceKind.STRUCTURAL_CONFIG,
        tool_call_trace_status=ToolCallTraceStatus.NOT_APPLICABLE,
        web_search_disabled=True,
        browser_tools_disabled=True,
        filesystem_workspace_access_disabled=True,
        external_retrieval_disabled=True,
        hidden_context_boundary=(
            "request body contained only the generated public-identifiers probe prompt and provider "
            "control fields; no participant packet, source, facilitator, outcome, tool, browser, "
            "filesystem, or retrieval context was supplied"
        ),
    )
    artifact = build_probe_artifact(
        probe_input=probe_input,
        parsed_response=parsed_response,
        raw_response_text=raw_response_body,
        isolation=isolation,
        reviewed_by_operator=reviewed_by_operator,
        model_snapshot_if_available=extract_model_snapshot_if_available(raw_response_body),
    )
    write_yaml_file(output_path, artifact.model_dump(mode="json"))
    return artifact


def _extract_openai_response_text(response_data: Any) -> str:
    if not isinstance(response_data, dict):
        raise ValueError("OpenAI response JSON must be an object")
    output_text = response_data.get("output_text")
    if isinstance(output_text, str):
        return output_text

    chunks: list[str] = []
    output = response_data.get("output")
    if isinstance(output, list):
        for item in output:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if isinstance(content, list):
                for content_item in content:
                    if isinstance(content_item, dict) and isinstance(content_item.get("text"), str):
                        chunks.append(content_item["text"])
    if chunks:
        return "".join(chunks)
    raise ValueError("OpenAI response did not contain output_text or text content")


def _extract_anthropic_response_text(response_data: Any) -> str:
    if not isinstance(response_data, dict):
        raise ValueError("Anthropic response JSON must be an object")
    chunks: list[str] = []
    content = response_data.get("content")
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text" and isinstance(item.get("text"), str):
                chunks.append(item["text"])
    if chunks:
        return "".join(chunks)
    raise ValueError("Anthropic response did not contain text content")


def parse_provider_model_text(model_text: str) -> ParsedProbeResponse:
    try:
        parsed_yaml = yaml.safe_load(model_text)
    except Exception as exc:
        raise ValueError(f"Failed to parse provider model text as YAML: {exc}") from exc
    try:
        return ParsedProbeResponse.model_validate(parsed_yaml)
    except Exception as exc:
        raise ValueError(f"Provider model text did not match memorization probe schema: {exc}") from exc


def _redact_header_secrets(text: str, headers: dict[str, str]) -> str:
    redacted = text
    authorization = headers.get("Authorization", "")
    if authorization.startswith("Bearer "):
        token = authorization.removeprefix("Bearer ")
        if token:
            redacted = redacted.replace(token, "[REDACTED]")
    api_key = headers.get("x-api-key", "")
    if api_key:
        redacted = redacted.replace(api_key, "[REDACTED]")
    return redacted


def _load_yaml(path: Path) -> object:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"Failed to load YAML file {path}: {exc}") from exc


def _parse_temperature(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("temperature must be a number") from exc
    if parsed < 0:
        raise argparse.ArgumentTypeError("temperature must be non-negative")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a raw-API no-tools memorization probe and write a v0.14 receipt."
    )
    parser.add_argument("--probe-input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--provider", choices=[item.value for item in RawApiProvider], required=True)
    parser.add_argument("--api-url", required=True)
    parser.add_argument("--api-key-env", required=True)
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--temperature", type=_parse_temperature, default=None)
    parser.add_argument("--timeout-seconds", type=float, default=60.0)
    parser.add_argument("--reviewed-by-operator", action="store_true")
    parser.add_argument("--allow-live-provider-call", action="store_true")
    args = parser.parse_args()

    if not args.allow_live_provider_call:
        parser.exit(status=2, message="Refusing live provider call without --allow-live-provider-call\n")
    if args.max_tokens <= 0:
        parser.exit(status=2, message="--max-tokens must be positive\n")
    if args.timeout_seconds <= 0:
        parser.exit(status=2, message="--timeout-seconds must be positive\n")

    api_key = os.environ.get(args.api_key_env)
    if api_key is None:
        parser.exit(status=2, message=f"Required API key environment variable is not set: {args.api_key_env}\n")

    try:
        artifact = run_memorization_probe_raw_api(
            probe_input_path=args.probe_input,
            output_path=args.output,
            provider=RawApiProvider(args.provider),
            api_url=args.api_url,
            api_key=api_key,
            transport=UrllibJsonTransport(),
            timeout_seconds=args.timeout_seconds,
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            reviewed_by_operator=args.reviewed_by_operator,
        )
    except Exception as exc:
        parser.exit(status=2, message=f"{exc}\n")

    print(args.output)
    print(f"probe_result={artifact.probe_result.value}")
    print(f"isolation_result={artifact.contestant_execution_isolation.isolation_result.value}")
    print(f"gate_interpretation={artifact.gate_interpretation.value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
