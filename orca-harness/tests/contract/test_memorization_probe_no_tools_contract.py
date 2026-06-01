from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest
from pydantic import ValidationError

from harness_utils import NON_CLAIM_NOTICE, load_yaml_file
from runners.run_memorization_probe import build_isolation_evidence, build_probe_artifact
from runners.run_memorization_probe_raw_api import (
    RawApiProvider,
    _redact_header_secrets,
    build_provider_request,
    build_provider_headers,
    run_memorization_probe_raw_api,
    validate_standard_provider_endpoint,
    validate_provider_request_shape,
)
from schemas.probe_models import (
    ContestantExecutionIsolation,
    ExecutionSurface,
    GateInterpretation,
    IsolationResult,
    ParsedProbeResponse,
    ProbeInput,
    ProbeResult,
    ToolAccessPolicy,
    ToolCallTraceStatus,
    ToolConfigEvidenceKind,
    derive_isolation_result,
    interpret_probe_gate,
)


def _probe_input() -> ProbeInput:
    return ProbeInput(
        case_id="fixture_probe_case_v0",
        decision_question="Should the board approve the proposed action?",
        public_identifiers_if_any=["Example Corp", "2024 shareholder vote"],
        decision_date_or_cutoff="2024-01-31T23:59:00Z",
        probe_model_family="fixture_family",
        probe_model_id="fixture_model",
        probe_prompt_template_version="memorization_probe_protocol.md#probe-prompt-template-v0_14",
    )


def _unknown_response() -> ParsedProbeResponse:
    return ParsedProbeResponse(
        recognition_status="unknown",
        claimed_outcome=None,
        confidence=0.0,
        notes="unknown",
    )


def _recognized_response() -> ParsedProbeResponse:
    return ParsedProbeResponse(
        recognition_status="recognized",
        claimed_outcome="The proposal was approved.",
        confidence=0.9,
        notes="recognized",
    )


def _write_probe_input(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "case_id: fixture_raw_api_probe_v0",
                "decision_question: Should Example Corp approve the proposed action?",
                "public_identifiers_if_any:",
                "  - Example Corp",
                "  - 2024 shareholder vote",
                "decision_date_or_cutoff: '2024-01-31T23:59:00Z'",
                "probe_model_family: fixture_family",
                "probe_model_id: fixture_model",
                "probe_prompt_template_version: memorization_probe_protocol.md#probe-prompt-template-v0_14",
                "",
            ]
        ),
        encoding="utf-8",
    )


class _FakeTransport:
    def __init__(self, raw_response_body: str) -> None:
        self.raw_response_body = raw_response_body
        self.calls: list[dict[str, object]] = []

    def post_json(self, url: str, headers: dict[str, str], body: dict[str, object], timeout_seconds: float) -> str:
        self.calls.append(
            {
                "url": url,
                "headers": headers,
                "body": body,
                "timeout_seconds": timeout_seconds,
            }
        )
        return self.raw_response_body


def test_raw_probe_pass_with_unproven_isolation_cannot_clear_gate() -> None:
    isolation = build_isolation_evidence(
        execution_surface=ExecutionSurface.LOCAL_FIXTURE,
        tool_access_policy=ToolAccessPolicy.UNKNOWN,
        tool_config_evidence="prompt text said not to search",
        tool_config_evidence_kind=ToolConfigEvidenceKind.PROMPT_INSTRUCTION_ONLY,
        tool_call_trace_status=ToolCallTraceStatus.UNAVAILABLE,
        web_search_disabled="unknown",
        browser_tools_disabled="unknown",
        filesystem_workspace_access_disabled="unknown",
        external_retrieval_disabled="unknown",
        hidden_context_boundary="local fixture response; no structural isolation evidence",
    )

    artifact = build_probe_artifact(
        probe_input=_probe_input(),
        parsed_response=_unknown_response(),
        raw_response_text="recognition_status: unknown\nclaimed_outcome:\nconfidence: 0.0\nnotes: unknown\n",
        isolation=isolation,
    )

    assert artifact.probe_result == ProbeResult.PASS
    assert artifact.contestant_execution_isolation.isolation_result == IsolationResult.NOT_PROVEN
    assert artifact.gate_interpretation == GateInterpretation.INVALID_FOR_CLEAN_PASS


def test_non_empty_tool_trace_invalidates_clean_execution() -> None:
    isolation = build_isolation_evidence(
        execution_surface=ExecutionSurface.API_WRAPPER,
        tool_access_policy=ToolAccessPolicy.NO_TOOLS,
        tool_config_evidence="provider trace captured tool call",
        tool_config_evidence_kind=ToolConfigEvidenceKind.PROVIDER_TRACE,
        tool_call_trace_status=ToolCallTraceStatus.NON_EMPTY_TRACE,
        web_search_disabled=True,
        browser_tools_disabled=True,
        filesystem_workspace_access_disabled=True,
        external_retrieval_disabled=True,
        hidden_context_boundary="only probe prompt was intended",
    )

    artifact = build_probe_artifact(
        probe_input=_probe_input(),
        parsed_response=_unknown_response(),
        raw_response_text="recognition_status: unknown\nclaimed_outcome:\nconfidence: 0.0\nnotes: unknown\n",
        isolation=isolation,
    )

    assert isolation.isolation_result == IsolationResult.VIOLATED
    assert artifact.gate_interpretation == GateInterpretation.EXECUTION_INVALID_TOOL_VIOLATION


def test_probe_fail_with_unproven_isolation_is_gate_closing_with_caveat() -> None:
    isolation = build_isolation_evidence(
        execution_surface=ExecutionSurface.AGENT_HARNESS,
        tool_access_policy=ToolAccessPolicy.NO_TOOLS,
        tool_config_evidence="operator configured no tools but no tool trace was captured",
        tool_config_evidence_kind=ToolConfigEvidenceKind.STRUCTURAL_CONFIG,
        tool_call_trace_status=ToolCallTraceStatus.UNAVAILABLE,
        web_search_disabled=True,
        browser_tools_disabled=True,
        filesystem_workspace_access_disabled=True,
        external_retrieval_disabled=True,
        hidden_context_boundary="only public-identifiers probe prompt was provided",
    )

    artifact = build_probe_artifact(
        probe_input=_probe_input(),
        parsed_response=_recognized_response(),
        raw_response_text=(
            "recognition_status: recognized\nclaimed_outcome: The proposal was approved.\n"
            "confidence: 0.9\nnotes: recognized\n"
        ),
        isolation=isolation,
    )

    assert artifact.probe_result == ProbeResult.FAIL
    assert artifact.contestant_execution_isolation.isolation_result == IsolationResult.NOT_PROVEN
    assert artifact.gate_interpretation == GateInterpretation.FAIL_GATE_CLOSING_WITH_CAVEAT


def test_probe_ambiguous_with_unproven_isolation_cannot_clear_gate() -> None:
    isolation = build_isolation_evidence(
        execution_surface=ExecutionSurface.AGENT_HARNESS,
        tool_access_policy=ToolAccessPolicy.NO_TOOLS,
        tool_config_evidence="operator configured no tools but no tool trace was captured",
        tool_config_evidence_kind=ToolConfigEvidenceKind.STRUCTURAL_CONFIG,
        tool_call_trace_status=ToolCallTraceStatus.UNAVAILABLE,
        web_search_disabled=True,
        browser_tools_disabled=True,
        filesystem_workspace_access_disabled=True,
        external_retrieval_disabled=True,
        hidden_context_boundary="only public-identifiers probe prompt was provided",
    )
    response = ParsedProbeResponse(
        recognition_status="partial",
        claimed_outcome="maybe approved",
        confidence=0.4,
        notes="partial",
    )

    artifact = build_probe_artifact(
        probe_input=_probe_input(),
        parsed_response=response,
        raw_response_text=(
            "recognition_status: partial\nclaimed_outcome: maybe approved\n"
            "confidence: 0.4\nnotes: partial\n"
        ),
        isolation=isolation,
    )

    assert artifact.probe_result == ProbeResult.AMBIGUOUS
    assert artifact.contestant_execution_isolation.isolation_result == IsolationResult.NOT_PROVEN
    assert artifact.gate_interpretation == GateInterpretation.INVALID_FOR_CLEAN_PASS


def test_tools_available_invalidates_clean_execution() -> None:
    isolation = build_isolation_evidence(
        execution_surface=ExecutionSurface.AGENT_HARNESS,
        tool_access_policy=ToolAccessPolicy.TOOLS_AVAILABLE,
        tool_config_evidence="agent was launched with tools available",
        tool_config_evidence_kind=ToolConfigEvidenceKind.STRUCTURAL_CONFIG,
        tool_call_trace_status=ToolCallTraceStatus.EMPTY_TRACE,
        web_search_disabled=True,
        browser_tools_disabled=True,
        filesystem_workspace_access_disabled=True,
        external_retrieval_disabled=True,
        hidden_context_boundary="only probe prompt was intended",
    )

    artifact = build_probe_artifact(
        probe_input=_probe_input(),
        parsed_response=_recognized_response(),
        raw_response_text=(
            "recognition_status: recognized\nclaimed_outcome: The proposal was approved.\n"
            "confidence: 0.9\nnotes: recognized\n"
        ),
        isolation=isolation,
    )

    assert isolation.isolation_result == IsolationResult.VIOLATED
    assert artifact.probe_result == ProbeResult.FAIL
    assert artifact.gate_interpretation == GateInterpretation.EXECUTION_INVALID_TOOL_VIOLATION


def test_agent_harness_missing_trace_is_unavailable_and_not_proven() -> None:
    isolation = build_isolation_evidence(
        execution_surface=ExecutionSurface.AGENT_HARNESS,
        tool_access_policy=ToolAccessPolicy.NO_TOOLS,
        tool_config_evidence="operator configured no tools but no tool trace was captured",
        tool_config_evidence_kind=ToolConfigEvidenceKind.STRUCTURAL_CONFIG,
        tool_call_trace_status=ToolCallTraceStatus.UNAVAILABLE,
        web_search_disabled=True,
        browser_tools_disabled=True,
        filesystem_workspace_access_disabled=True,
        external_retrieval_disabled=True,
        hidden_context_boundary="only public-identifiers probe prompt was provided",
    )

    artifact = build_probe_artifact(
        probe_input=_probe_input(),
        parsed_response=_unknown_response(),
        raw_response_text="recognition_status: unknown\nclaimed_outcome:\nconfidence: 0.0\nnotes: unknown\n",
        isolation=isolation,
    )

    assert isolation.tool_call_trace_status == ToolCallTraceStatus.UNAVAILABLE
    assert isolation.isolation_result == IsolationResult.NOT_PROVEN
    assert artifact.gate_interpretation == GateInterpretation.INVALID_FOR_CLEAN_PASS


def test_not_applicable_trace_status_is_rejected_for_agent_harnesses() -> None:
    with pytest.raises(ValidationError, match="not_applicable is valid only"):
        ContestantExecutionIsolation(
            execution_surface=ExecutionSurface.AGENT_HARNESS,
            tool_access_policy=ToolAccessPolicy.NO_TOOLS,
            tool_config_evidence="operator configured no tools",
            tool_config_evidence_kind=ToolConfigEvidenceKind.STRUCTURAL_CONFIG,
            tool_call_trace_status=ToolCallTraceStatus.NOT_APPLICABLE,
            web_search_disabled=True,
            browser_tools_disabled=True,
            filesystem_workspace_access_disabled=True,
            external_retrieval_disabled=True,
            hidden_context_boundary="only public-identifiers probe prompt was provided",
            isolation_result=IsolationResult.NOT_PROVEN,
        )


def test_empty_tool_trace_evidence_requires_empty_trace_status() -> None:
    with pytest.raises(ValidationError, match="empty tool-trace evidence requires"):
        ContestantExecutionIsolation(
            execution_surface=ExecutionSurface.RAW_API_NO_TOOLS,
            tool_access_policy=ToolAccessPolicy.NO_TOOLS,
            tool_config_evidence="claimed empty trace",
            tool_config_evidence_kind=ToolConfigEvidenceKind.EMPTY_TOOL_TRACE,
            tool_call_trace_status=ToolCallTraceStatus.NOT_APPLICABLE,
            web_search_disabled=True,
            browser_tools_disabled=True,
            filesystem_workspace_access_disabled=True,
            external_retrieval_disabled=True,
            hidden_context_boundary="only public-identifiers probe prompt was provided",
            isolation_result=IsolationResult.PROVEN,
        )


def test_raw_api_no_tool_schema_can_prove_isolation_with_structural_evidence() -> None:
    isolation = build_isolation_evidence(
        execution_surface=ExecutionSurface.RAW_API_NO_TOOLS,
        tool_access_policy=ToolAccessPolicy.NO_TOOLS,
        tool_config_evidence="raw API request supplied no tool schema or retrieval channel",
        tool_config_evidence_kind=ToolConfigEvidenceKind.STRUCTURAL_CONFIG,
        tool_call_trace_status=ToolCallTraceStatus.NOT_APPLICABLE,
        web_search_disabled=True,
        browser_tools_disabled=True,
        filesystem_workspace_access_disabled=True,
        external_retrieval_disabled=True,
        hidden_context_boundary="request body contained only the public-identifiers probe prompt",
    )

    artifact = build_probe_artifact(
        probe_input=_probe_input(),
        parsed_response=_unknown_response(),
        raw_response_text="recognition_status: unknown\nclaimed_outcome:\nconfidence: 0.0\nnotes: unknown\n",
        isolation=isolation,
    )

    assert isolation.isolation_result == IsolationResult.PROVEN
    assert artifact.probe_result == ProbeResult.PASS
    assert artifact.gate_interpretation == GateInterpretation.PASS_VALID


def test_hidden_context_boundary_is_required_for_proven_isolation() -> None:
    class Evidence:
        web_search_disabled = True
        browser_tools_disabled = True
        filesystem_workspace_access_disabled = True
        external_retrieval_disabled = True
        tool_access_policy = ToolAccessPolicy.NO_TOOLS
        tool_config_evidence_kind = ToolConfigEvidenceKind.STRUCTURAL_CONFIG
        tool_call_trace_status = ToolCallTraceStatus.NOT_APPLICABLE
        hidden_context_boundary = ""

    assert derive_isolation_result(Evidence()) == IsolationResult.NOT_PROVEN


def test_ambiguous_with_proven_isolation_routes_to_quarantine_explicitly() -> None:
    assert (
        interpret_probe_gate(ProbeResult.AMBIGUOUS, IsolationResult.PROVEN)
        == GateInterpretation.AMBIGUOUS_QUARANTINE
    )


def test_cli_writes_dry_probe_receipt_with_hashes(copied_project: Path) -> None:
    smoke_dir = copied_project / "_probe_smoke"
    smoke_dir.mkdir()
    probe_input_path = smoke_dir / "probe_input.yaml"
    raw_response_path = smoke_dir / "raw_response.yaml"
    output_path = smoke_dir / "probe_receipt.yaml"

    probe_input_path.write_text(
        "\n".join(
            [
                "case_id: fixture_cli_probe_v0",
                "decision_question: Should Example Corp approve the proposed action?",
                "public_identifiers_if_any:",
                "  - Example Corp",
                "  - 2024 shareholder vote",
                "decision_date_or_cutoff: '2024-01-31T23:59:00Z'",
                "probe_model_family: fixture_family",
                "probe_model_id: fixture_model",
                "probe_prompt_template_version: memorization_probe_protocol.md#probe-prompt-template-v0_14",
                "",
            ]
        ),
        encoding="utf-8",
    )
    raw_response_text = "recognition_status: unknown\nclaimed_outcome:\nconfidence: 0.0\nnotes: unknown\n"
    raw_response_path.write_text(raw_response_text, encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            "runners/run_memorization_probe.py",
            "--probe-input",
            str(probe_input_path),
            "--raw-response",
            str(raw_response_path),
            "--output",
            str(output_path),
            "--execution-surface",
            "raw_api_no_tools",
            "--tool-access-policy",
            "no_tools",
            "--tool-config-evidence",
            "raw API request supplied no tool schema or retrieval channel",
            "--tool-config-evidence-kind",
            "structural_config",
            "--tool-call-trace-status",
            "not_applicable",
            "--web-search-disabled",
            "true",
            "--browser-tools-disabled",
            "true",
            "--filesystem-workspace-access-disabled",
            "true",
            "--external-retrieval-disabled",
            "true",
            "--hidden-context-boundary",
            "request body contained only the public-identifiers probe prompt",
            "--reviewed-by-operator",
        ],
        cwd=copied_project,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert output_path.exists()
    assert "probe_result=pass" in completed.stdout
    assert "isolation_result=proven" in completed.stdout
    assert "gate_interpretation=pass_valid" in completed.stdout

    expected_prompt = """You are being tested for prior knowledge contamination.

You will receive a decision question and minimal identifiers. Do not infer from a packet; no packet is provided.

Decision question:
Should Example Corp approve the proposed action?

Known identifiers:
- Example Corp
- 2024 shareholder vote

Decision cutoff:
2024-01-31T23:59:00Z

Task:
1. State whether you recognize the specific real-world case.
2. If yes, state what outcome or later decision you believe occurred.
3. If no, say "unknown" and do not guess.
4. Do not fabricate.

Output YAML:
recognition_status: recognized | partial | unknown
claimed_outcome:
confidence: 0.0_to_1.0
notes:
"""
    receipt = load_yaml_file(output_path)

    assert receipt["case_id"] == "fixture_cli_probe_v0"
    assert receipt["probe_model_family"] == "fixture_family"
    assert receipt["probe_model_id"] == "fixture_model"
    assert receipt["prompt_hash"] == hashlib.sha256(expected_prompt.encode("utf-8")).hexdigest()
    assert receipt["raw_response_hash"] == hashlib.sha256(raw_response_text.encode("utf-8")).hexdigest()
    assert receipt["parsed_response"]["recognition_status"] == "unknown"
    assert receipt["probe_result"] == "pass"
    assert receipt["gate_interpretation"] == "pass_valid"
    assert receipt["reviewed_by_operator"] is True
    assert receipt["non_claim_notice"] == NON_CLAIM_NOTICE

    isolation = receipt["contestant_execution_isolation"]
    assert isolation["execution_surface"] == "raw_api_no_tools"
    assert isolation["tool_access_policy"] == "no_tools"
    assert isolation["tool_config_evidence_kind"] == "structural_config"
    assert isolation["tool_call_trace_status"] == "not_applicable"
    assert isolation["web_search_disabled"] is True
    assert isolation["browser_tools_disabled"] is True
    assert isolation["filesystem_workspace_access_disabled"] is True
    assert isolation["external_retrieval_disabled"] is True
    assert isolation["isolation_result"] == "proven"


def test_raw_api_provider_runner_with_fake_transport_produces_proven_pass(copied_project: Path) -> None:
    smoke_dir = copied_project / "_probe_raw_api_unit"
    smoke_dir.mkdir()
    probe_input_path = smoke_dir / "probe_input.yaml"
    output_path = smoke_dir / "probe_receipt.yaml"
    _write_probe_input(probe_input_path)

    model_text = "recognition_status: unknown\nclaimed_outcome:\nconfidence: 0.0\nnotes: unknown\n"
    raw_response_body = json.dumps(
        {
            "output_text": model_text,
            "system_fingerprint": "fp_fixture",
        }
    )
    transport = _FakeTransport(raw_response_body)

    artifact = run_memorization_probe_raw_api(
        probe_input_path=probe_input_path,
        output_path=output_path,
        provider=RawApiProvider.OPENAI_RESPONSES,
        api_url="https://api.openai.com/v1/responses",
        api_key="secret-token",
        transport=transport,
        reviewed_by_operator=True,
    )

    assert len(transport.calls) == 1
    request_body = transport.calls[0]["body"]
    assert set(request_body) == {"model", "input", "max_output_tokens"}
    assert request_body["model"] == "fixture_model"
    assert request_body["max_output_tokens"] == 512
    assert "Should Example Corp approve the proposed action?" in str(request_body["input"])
    assert "2024 shareholder vote" in str(request_body["input"])
    assert artifact.probe_result == ProbeResult.PASS
    assert artifact.contestant_execution_isolation.isolation_result == IsolationResult.PROVEN
    assert artifact.gate_interpretation == GateInterpretation.PASS_VALID

    receipt = load_yaml_file(output_path)
    assert receipt["raw_response_hash"] == hashlib.sha256(raw_response_body.encode("utf-8")).hexdigest()
    assert receipt["model_snapshot_if_available"] == "system_fingerprint:fp_fixture"
    assert "secret-token" not in str(receipt)


def test_raw_api_provider_runner_reads_only_probe_input_file(copied_project: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    smoke_dir = copied_project / "_probe_raw_api_read_boundary"
    smoke_dir.mkdir()
    probe_input_path = smoke_dir / "probe_input.yaml"
    output_path = smoke_dir / "probe_receipt.yaml"
    _write_probe_input(probe_input_path)
    model_text = "recognition_status: unknown\nclaimed_outcome:\nconfidence: 0.0\nnotes: unknown\n"
    transport = _FakeTransport(json.dumps({"output_text": model_text}))
    observed_reads: list[Path] = []
    original_read_text = Path.read_text

    def tracked_read_text(path: Path, *args: object, **kwargs: object) -> str:
        observed_reads.append(path.resolve())
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", tracked_read_text)

    run_memorization_probe_raw_api(
        probe_input_path=probe_input_path,
        output_path=output_path,
        provider=RawApiProvider.OPENAI_RESPONSES,
        api_url="https://api.openai.com/v1/responses",
        api_key="secret-token",
        transport=transport,
    )

    assert observed_reads == [probe_input_path.resolve()]


def test_raw_api_provider_rejects_tool_fields_before_transport() -> None:
    with pytest.raises(ValueError, match="forbidden tool/context key"):
        validate_provider_request_shape(
            RawApiProvider.OPENAI_RESPONSES,
            {
                "model": "fixture_model",
                "input": "probe prompt",
                "tools": [],
            },
            "probe prompt",
        )


def test_raw_api_provider_rejects_non_standard_endpoint() -> None:
    with pytest.raises(ValueError, match="standard openai_responses endpoint"):
        validate_standard_provider_endpoint(
            RawApiProvider.OPENAI_RESPONSES,
            "https://provider.invalid/v1/responses",
        )


def test_raw_api_provider_malformed_response_writes_no_artifact(copied_project: Path) -> None:
    smoke_dir = copied_project / "_probe_raw_api_malformed"
    smoke_dir.mkdir()
    probe_input_path = smoke_dir / "probe_input.yaml"
    output_path = smoke_dir / "probe_receipt.yaml"
    _write_probe_input(probe_input_path)
    transport = _FakeTransport(json.dumps({"output_text": "recognition_status: [\n"}))

    with pytest.raises(ValueError):
        run_memorization_probe_raw_api(
            probe_input_path=probe_input_path,
            output_path=output_path,
            provider=RawApiProvider.OPENAI_RESPONSES,
            api_url="https://api.openai.com/v1/responses",
            api_key="secret-token",
            transport=transport,
        )

    assert not output_path.exists()


def test_anthropic_raw_api_request_contains_single_user_prompt_only() -> None:
    probe_input = _probe_input()
    prompt = build_provider_request(
        provider=RawApiProvider.OPENAI_RESPONSES,
        probe_input=probe_input,
        max_tokens=512,
    )["input"]

    body = build_provider_request(
        provider=RawApiProvider.ANTHROPIC_MESSAGES,
        probe_input=probe_input,
        max_tokens=256,
        temperature=0.0,
    )

    assert body == {
        "model": "fixture_model",
        "max_tokens": 256,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
    }


def test_raw_api_provider_rejects_response_text_shortcut(copied_project: Path) -> None:
    smoke_dir = copied_project / "_probe_raw_api_response_text_shortcut"
    smoke_dir.mkdir()
    probe_input_path = smoke_dir / "probe_input.yaml"
    output_path = smoke_dir / "probe_receipt.yaml"
    _write_probe_input(probe_input_path)
    transport = _FakeTransport(
        json.dumps(
            {
                "response_text": "recognition_status: unknown\nclaimed_outcome:\nconfidence: 0.0\nnotes: unknown\n"
            }
        )
    )

    with pytest.raises(ValueError, match="OpenAI response did not contain"):
        run_memorization_probe_raw_api(
            probe_input_path=probe_input_path,
            output_path=output_path,
            provider=RawApiProvider.OPENAI_RESPONSES,
            api_url="https://api.openai.com/v1/responses",
            api_key="secret-token",
            transport=transport,
        )

    assert not output_path.exists()


def test_provider_http_error_redacts_header_secret() -> None:
    headers = build_provider_headers(RawApiProvider.OPENAI_RESPONSES, "secret-token")
    message = _redact_header_secrets("Invalid API key: secret-token", headers)

    assert "secret-token" not in message
    assert "[REDACTED]" in message


def test_raw_api_provider_cli_refuses_live_call_without_explicit_flag(copied_project: Path) -> None:
    smoke_dir = copied_project / "_probe_raw_api_smoke"
    smoke_dir.mkdir()
    probe_input_path = smoke_dir / "probe_input.yaml"
    output_path = smoke_dir / "probe_receipt.yaml"
    _write_probe_input(probe_input_path)

    completed = subprocess.run(
        [
            sys.executable,
            "runners/run_memorization_probe_raw_api.py",
            "--probe-input",
            str(probe_input_path),
            "--output",
            str(output_path),
            "--provider",
            "openai_responses",
            "--api-url",
            "https://provider.invalid/v1/responses",
            "--api-key-env",
            "ORCA_FIXTURE_API_KEY",
        ],
        cwd=copied_project,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 2
    assert "Refusing live provider call" in completed.stderr
    assert not output_path.exists()
