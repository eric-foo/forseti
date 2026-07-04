from __future__ import annotations

import argparse
from pathlib import Path
from types import SimpleNamespace
import sys

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness_utils import generate_ulid, sha256_text, utc_now_z, write_yaml_file
from schemas.probe_models import (
    ContestantExecutionIsolation,
    ExecutionSurface,
    GateInterpretation,
    IsolationResult,
    MemorizationProbeArtifact,
    ParsedProbeResponse,
    ProbeInput,
    ToolAccessPolicy,
    ToolCallTraceStatus,
    ToolConfigEvidenceKind,
    classify_probe_response,
    derive_isolation_result,
    interpret_probe_gate,
)


PROBE_PROMPT_TEMPLATE = """You are being tested for prior knowledge contamination.

You will receive a decision question and minimal identifiers. Do not infer from a packet; no packet is provided.

Decision question:
{decision_question}

Known identifiers:
{public_identifiers_if_any}

Decision cutoff:
{decision_date_or_cutoff}

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


def build_probe_prompt(probe_input: ProbeInput) -> str:
    identifiers = probe_input.public_identifiers_if_any
    if isinstance(identifiers, list):
        identifiers_text = "\n".join(f"- {identifier}" for identifier in identifiers)
    else:
        identifiers_text = identifiers
    return PROBE_PROMPT_TEMPLATE.format(
        decision_question=probe_input.decision_question,
        public_identifiers_if_any=identifiers_text,
        decision_date_or_cutoff=probe_input.decision_date_or_cutoff,
    )


def build_isolation_evidence(
    *,
    execution_surface: ExecutionSurface,
    tool_access_policy: ToolAccessPolicy,
    tool_config_evidence: str,
    tool_config_evidence_kind: ToolConfigEvidenceKind,
    tool_call_trace_status: ToolCallTraceStatus,
    web_search_disabled: bool | str,
    browser_tools_disabled: bool | str,
    filesystem_workspace_access_disabled: bool | str,
    external_retrieval_disabled: bool | str,
    hidden_context_boundary: str,
) -> ContestantExecutionIsolation:
    fields = {
        "execution_surface": execution_surface,
        "tool_access_policy": tool_access_policy,
        "tool_config_evidence": tool_config_evidence,
        "tool_config_evidence_kind": tool_config_evidence_kind,
        "tool_call_trace_status": tool_call_trace_status,
        "web_search_disabled": web_search_disabled,
        "browser_tools_disabled": browser_tools_disabled,
        "filesystem_workspace_access_disabled": filesystem_workspace_access_disabled,
        "external_retrieval_disabled": external_retrieval_disabled,
        "hidden_context_boundary": hidden_context_boundary,
    }
    isolation_result = derive_isolation_result(SimpleNamespace(**fields))
    return ContestantExecutionIsolation(
        **fields,
        isolation_result=isolation_result,
    )


def build_probe_artifact(
    *,
    probe_input: ProbeInput,
    parsed_response: ParsedProbeResponse,
    raw_response_text: str,
    isolation: ContestantExecutionIsolation,
    reviewed_by_operator: bool = False,
    model_snapshot_if_available: str | None = None,
) -> MemorizationProbeArtifact:
    probe_prompt = build_probe_prompt(probe_input)
    probe_result = classify_probe_response(parsed_response)
    gate_interpretation = interpret_probe_gate(probe_result, isolation.isolation_result)
    return MemorizationProbeArtifact(
        probe_id=generate_ulid(),
        case_id=probe_input.case_id,
        probe_model_family=probe_input.probe_model_family,
        probe_model_id=probe_input.probe_model_id,
        model_snapshot_if_available=model_snapshot_if_available,
        prompt_hash=sha256_text(probe_prompt),
        raw_response_hash=sha256_text(raw_response_text),
        contestant_execution_isolation=isolation,
        parsed_response=parsed_response,
        probe_result=probe_result,
        gate_interpretation=gate_interpretation,
        reviewed_by_operator=reviewed_by_operator,
        created_at=utc_now_z(),
    )


def run_memorization_probe_dry(
    *,
    probe_input_path: Path,
    raw_response_path: Path,
    output_path: Path,
    isolation: ContestantExecutionIsolation,
    reviewed_by_operator: bool = False,
    model_snapshot_if_available: str | None = None,
) -> MemorizationProbeArtifact:
    probe_input = ProbeInput.model_validate(_load_yaml(probe_input_path))
    raw_response_text = raw_response_path.read_text(encoding="utf-8")
    parsed_response = ParsedProbeResponse.model_validate(yaml.safe_load(raw_response_text))
    artifact = build_probe_artifact(
        probe_input=probe_input,
        parsed_response=parsed_response,
        raw_response_text=raw_response_text,
        isolation=isolation,
        reviewed_by_operator=reviewed_by_operator,
        model_snapshot_if_available=model_snapshot_if_available,
    )
    write_yaml_file(output_path, artifact.model_dump(mode="json"))
    return artifact


def _load_yaml(path: Path) -> object:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"Failed to load YAML file {path}: {exc}") from exc


def _parse_bool_or_unknown(value: str) -> bool | str:
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "unknown":
        return "unknown"
    raise argparse.ArgumentTypeError("expected true, false, or unknown")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a local memorization-probe receipt from a pre-supplied response."
    )
    parser.add_argument("--probe-input", type=Path, required=True)
    parser.add_argument("--raw-response", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--execution-surface", choices=[item.value for item in ExecutionSurface], default="local_fixture")
    parser.add_argument("--tool-access-policy", choices=[item.value for item in ToolAccessPolicy], default="unknown")
    parser.add_argument("--tool-config-evidence", default="local dry-run response; no provider execution")
    parser.add_argument(
        "--tool-config-evidence-kind",
        choices=[item.value for item in ToolConfigEvidenceKind],
        default="operator_assertion_only",
    )
    parser.add_argument(
        "--tool-call-trace-status",
        choices=[item.value for item in ToolCallTraceStatus],
        default="unavailable",
    )
    parser.add_argument("--web-search-disabled", type=_parse_bool_or_unknown, default="unknown")
    parser.add_argument("--browser-tools-disabled", type=_parse_bool_or_unknown, default="unknown")
    parser.add_argument("--filesystem-workspace-access-disabled", type=_parse_bool_or_unknown, default="unknown")
    parser.add_argument("--external-retrieval-disabled", type=_parse_bool_or_unknown, default="unknown")
    parser.add_argument(
        "--hidden-context-boundary",
        default="local dry runner received only probe input and pre-supplied raw response files",
    )
    parser.add_argument("--model-snapshot-if-available", default=None)
    parser.add_argument("--reviewed-by-operator", action="store_true")
    args = parser.parse_args()

    try:
        isolation = build_isolation_evidence(
            execution_surface=ExecutionSurface(args.execution_surface),
            tool_access_policy=ToolAccessPolicy(args.tool_access_policy),
            tool_config_evidence=args.tool_config_evidence,
            tool_config_evidence_kind=ToolConfigEvidenceKind(args.tool_config_evidence_kind),
            tool_call_trace_status=ToolCallTraceStatus(args.tool_call_trace_status),
            web_search_disabled=args.web_search_disabled,
            browser_tools_disabled=args.browser_tools_disabled,
            filesystem_workspace_access_disabled=args.filesystem_workspace_access_disabled,
            external_retrieval_disabled=args.external_retrieval_disabled,
            hidden_context_boundary=args.hidden_context_boundary,
        )
        artifact = run_memorization_probe_dry(
            probe_input_path=args.probe_input,
            raw_response_path=args.raw_response,
            output_path=args.output,
            isolation=isolation,
            reviewed_by_operator=args.reviewed_by_operator,
            model_snapshot_if_available=args.model_snapshot_if_available,
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
