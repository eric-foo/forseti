from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import Field, field_validator, model_validator

from harness_utils import NON_CLAIM_NOTICE
from schemas.case_models import StrictModel


class ProbeResult(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    AMBIGUOUS = "ambiguous"


class IsolationResult(StrEnum):
    PROVEN = "proven"
    NOT_PROVEN = "not_proven"
    VIOLATED = "violated"


class ToolAccessPolicy(StrEnum):
    NO_TOOLS = "no_tools"
    TOOLS_AVAILABLE = "tools_available"
    UNKNOWN = "unknown"


class ToolCallTraceStatus(StrEnum):
    EMPTY_TRACE = "empty_trace"
    UNAVAILABLE = "unavailable"
    NON_EMPTY_TRACE = "non_empty_trace"
    NOT_APPLICABLE = "not_applicable"


class ExecutionSurface(StrEnum):
    RAW_API_NO_TOOLS = "raw_api_no_tools"
    AGENT_HARNESS = "agent_harness"
    BROWSER_HARNESS = "browser_harness"
    API_WRAPPER = "api_wrapper"
    LOCAL_FIXTURE = "local_fixture"
    MANUAL_UNKNOWN = "manual_unknown"


class ToolConfigEvidenceKind(StrEnum):
    STRUCTURAL_CONFIG = "structural_config"
    PROVIDER_TRACE = "provider_trace"
    EMPTY_TOOL_TRACE = "empty_tool_trace"
    PROMPT_INSTRUCTION_ONLY = "prompt_instruction_only"
    OPERATOR_ASSERTION_ONLY = "operator_assertion_only"
    UNKNOWN = "unknown"


class GateInterpretation(StrEnum):
    PASS_VALID = "pass_valid"
    FAIL_GATE_CLOSING = "fail_gate_closing"
    FAIL_GATE_CLOSING_WITH_CAVEAT = "fail_gate_closing_with_caveat"
    INVALID_FOR_CLEAN_PASS = "invalid_for_clean_pass"
    EXECUTION_INVALID_TOOL_VIOLATION = "execution_invalid_tool_violation"
    AMBIGUOUS_QUARANTINE = "ambiguous_quarantine"


BooleanOrUnknown = bool | Literal["unknown"]


class ProbeInput(StrictModel):
    case_id: str
    decision_question: str
    public_identifiers_if_any: str | list[str] = Field(default_factory=list)
    decision_date_or_cutoff: str
    probe_model_family: str
    probe_model_id: str
    probe_prompt_template_version: str


class ParsedProbeResponse(StrictModel):
    recognition_status: Literal["recognized", "partial", "unknown"]
    claimed_outcome: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    notes: str | None = None

    @field_validator("claimed_outcome", "notes", mode="before")
    @classmethod
    def empty_string_to_none(cls, value: object) -> object:
        if isinstance(value, str) and value.strip() == "":
            return None
        return value


class ContestantExecutionIsolation(StrictModel):
    execution_surface: ExecutionSurface
    tool_access_policy: ToolAccessPolicy
    tool_config_evidence: str
    tool_config_evidence_kind: ToolConfigEvidenceKind
    tool_call_trace_status: ToolCallTraceStatus
    web_search_disabled: BooleanOrUnknown
    browser_tools_disabled: BooleanOrUnknown
    filesystem_workspace_access_disabled: BooleanOrUnknown
    external_retrieval_disabled: BooleanOrUnknown
    hidden_context_boundary: str
    isolation_result: IsolationResult

    @field_validator("tool_config_evidence", "hidden_context_boundary")
    @classmethod
    def reject_blank_evidence(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("execution-isolation evidence fields must be non-empty")
        return value

    @model_validator(mode="after")
    def validate_trace_status_and_result(self) -> "ContestantExecutionIsolation":
        if (
            self.tool_call_trace_status == ToolCallTraceStatus.NOT_APPLICABLE
            and self.execution_surface != ExecutionSurface.RAW_API_NO_TOOLS
        ):
            raise ValueError(
                "tool_call_trace_status not_applicable is valid only for raw_api_no_tools execution"
            )

        if (
            self.tool_config_evidence_kind == ToolConfigEvidenceKind.EMPTY_TOOL_TRACE
            and self.tool_call_trace_status != ToolCallTraceStatus.EMPTY_TRACE
        ):
            raise ValueError("empty tool-trace evidence requires tool_call_trace_status empty_trace")

        expected = derive_isolation_result(self)
        if self.isolation_result != expected:
            raise ValueError(
                f"isolation_result must be {expected.value} for the supplied execution evidence"
            )
        return self


class MemorizationProbeArtifact(StrictModel):
    probe_id: str
    case_id: str
    probe_model_family: str
    probe_model_id: str
    model_snapshot_if_available: str | None = None
    prompt_hash: str
    raw_response_hash: str
    contestant_execution_isolation: ContestantExecutionIsolation
    parsed_response: ParsedProbeResponse
    probe_result: ProbeResult
    gate_interpretation: GateInterpretation
    reviewed_by_operator: bool
    created_at: str
    non_claim_notice: str = NON_CLAIM_NOTICE

    @field_validator("non_claim_notice")
    @classmethod
    def validate_non_claim_notice(cls, value: str) -> str:
        if value != NON_CLAIM_NOTICE:
            raise ValueError("non_claim_notice must match the exact required claim boundary")
        return value

    @model_validator(mode="after")
    def validate_gate_interpretation(self) -> "MemorizationProbeArtifact":
        expected = interpret_probe_gate(
            self.probe_result,
            self.contestant_execution_isolation.isolation_result,
        )
        if self.gate_interpretation != expected:
            raise ValueError(
                f"gate_interpretation must be {expected.value} for probe_result/isolation_result"
            )
        return self


def derive_isolation_result(evidence: ContestantExecutionIsolation) -> IsolationResult:
    disabled_fields = (
        evidence.web_search_disabled,
        evidence.browser_tools_disabled,
        evidence.filesystem_workspace_access_disabled,
        evidence.external_retrieval_disabled,
    )
    if (
        evidence.tool_access_policy == ToolAccessPolicy.TOOLS_AVAILABLE
        or evidence.tool_call_trace_status == ToolCallTraceStatus.NON_EMPTY_TRACE
        or any(value is False for value in disabled_fields)
    ):
        return IsolationResult.VIOLATED

    proof_grade_evidence = {
        ToolConfigEvidenceKind.STRUCTURAL_CONFIG,
        ToolConfigEvidenceKind.PROVIDER_TRACE,
        ToolConfigEvidenceKind.EMPTY_TOOL_TRACE,
    }
    trace_can_prove = {
        ToolCallTraceStatus.EMPTY_TRACE,
        ToolCallTraceStatus.NOT_APPLICABLE,
    }
    if (
        evidence.tool_access_policy == ToolAccessPolicy.NO_TOOLS
        and evidence.tool_config_evidence_kind in proof_grade_evidence
        and evidence.tool_call_trace_status in trace_can_prove
        and all(value is True for value in disabled_fields)
        and bool(str(evidence.hidden_context_boundary).strip())
    ):
        return IsolationResult.PROVEN

    return IsolationResult.NOT_PROVEN


def interpret_probe_gate(
    probe_result: ProbeResult,
    isolation_result: IsolationResult,
) -> GateInterpretation:
    if isolation_result == IsolationResult.VIOLATED:
        return GateInterpretation.EXECUTION_INVALID_TOOL_VIOLATION
    if probe_result == ProbeResult.PASS and isolation_result == IsolationResult.PROVEN:
        return GateInterpretation.PASS_VALID
    if probe_result == ProbeResult.FAIL and isolation_result == IsolationResult.PROVEN:
        return GateInterpretation.FAIL_GATE_CLOSING
    if probe_result == ProbeResult.FAIL and isolation_result == IsolationResult.NOT_PROVEN:
        return GateInterpretation.FAIL_GATE_CLOSING_WITH_CAVEAT
    if probe_result in {ProbeResult.PASS, ProbeResult.AMBIGUOUS} and isolation_result == IsolationResult.NOT_PROVEN:
        return GateInterpretation.INVALID_FOR_CLEAN_PASS
    if probe_result == ProbeResult.AMBIGUOUS and isolation_result == IsolationResult.PROVEN:
        return GateInterpretation.AMBIGUOUS_QUARANTINE
    raise ValueError(f"Unhandled probe gate combination: {probe_result.value}/{isolation_result.value}")


def classify_probe_response(response: ParsedProbeResponse) -> ProbeResult:
    if response.recognition_status == "unknown" or response.claimed_outcome is None:
        return ProbeResult.PASS
    if response.recognition_status == "recognized" and response.confidence >= 0.5:
        return ProbeResult.FAIL
    return ProbeResult.AMBIGUOUS
