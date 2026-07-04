from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from harness_utils import utc_now_z
from source_capture.reddit_agent_view import REDDIT_AGENT_VIEW_SCHEMA_VERSION


REDDIT_AGENT_VIEW_AB_PROBE_SCHEMA_VERSION = "reddit_agent_view_ab_probe_v0"

DEFAULT_FULL_NAME = "reddit_agent_view_full.json"
DEFAULT_STRIPPED_NAME = "reddit_agent_view_stripped.json"
DEFAULT_MANIFEST_NAME = "reddit_agent_view_ab_probe_manifest.json"
DEFAULT_RECEIPT_NAME = "reddit_agent_view_ab_probe_receipt.md"

NON_CLAIMS = [
    "not agent output",
    "not model evaluation",
    "not live Reddit access",
    "not source capture",
    "not canonical artifact replacement",
    "not stripped-view default selection",
    "not Data Capture handoff",
    "not source completeness proof",
    "not ECR, Cleaning, Judgment, fixture admission, or commercial readiness",
]


class RedditAgentViewABProbeFailure(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def build_reddit_agent_view_ab_probe(
    *,
    view_directories: list[Path],
    output_directory: Path,
    full_name: str = DEFAULT_FULL_NAME,
    stripped_name: str = DEFAULT_STRIPPED_NAME,
    manifest_name: str = DEFAULT_MANIFEST_NAME,
    receipt_name: str = DEFAULT_RECEIPT_NAME,
) -> dict[str, str]:
    if not view_directories:
        raise RedditAgentViewABProbeFailure(
            "no_cases",
            "at least one agent-view directory is required",
        )

    output_directory = output_directory.resolve()
    manifest_path = output_directory / manifest_name
    receipt_path = output_directory / receipt_name
    output_directory.mkdir(parents=True, exist_ok=True)
    for path in (manifest_path, receipt_path):
        if path.exists():
            raise RedditAgentViewABProbeFailure("output_exists", f"output already exists: {path}")

    cases = [
        _build_case(
            view_directory=view_directory.resolve(),
            output_directory=output_directory,
            full_name=full_name,
            stripped_name=stripped_name,
        )
        for view_directory in view_directories
    ]
    manifest = {
        "reddit_agent_view_ab_probe": {
            "schema_version": REDDIT_AGENT_VIEW_AB_PROBE_SCHEMA_VERSION,
            "generated_at": utc_now_z(),
            "probe_status": "needs_agent_or_owner_outputs",
            "case_count": len(cases),
            "cases": cases,
            "comparison_dimensions": [
                "substantive_claim_parity",
                "missed_context",
                "provenance_sufficiency",
                "context_economy",
                "hallucination_risk",
                "full_json_required_for_task",
            ],
            "non_claims": NON_CLAIMS,
        }
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    receipt_path.write_text(_render_receipt(manifest), encoding="utf-8", newline="\n")
    return {"manifest_path": str(manifest_path), "receipt_path": str(receipt_path)}


def _build_case(
    *,
    view_directory: Path,
    output_directory: Path,
    full_name: str,
    stripped_name: str,
) -> dict[str, Any]:
    full_path = view_directory / full_name
    stripped_path = view_directory / stripped_name
    full = _read_json(full_path, role="full")
    stripped = _read_json(stripped_path, role="stripped")

    full_type = _detect_full_artifact_type(full)
    view = _extract_stripped_view(stripped, stripped_path)
    stripped_type = view["source_artifact_type"]
    if full_type != stripped_type:
        raise RedditAgentViewABProbeFailure(
            "artifact_type_mismatch",
            f"{view_directory} full type {full_type} does not match stripped type {stripped_type}",
        )
    if view.get("schema_version") != REDDIT_AGENT_VIEW_SCHEMA_VERSION:
        raise RedditAgentViewABProbeFailure(
            "stripped_schema_mismatch",
            f"{stripped_path} is not a {REDDIT_AGENT_VIEW_SCHEMA_VERSION} artifact",
        )

    label = _case_label(view_directory)
    case_dir = output_directory / label
    case_dir.mkdir(parents=True, exist_ok=True)
    full_prompt_path = case_dir / "full_prompt.md"
    stripped_prompt_path = case_dir / "stripped_prompt.md"
    worksheet_path = case_dir / "comparison_worksheet.md"
    for path in (full_prompt_path, stripped_prompt_path, worksheet_path):
        if path.exists():
            raise RedditAgentViewABProbeFailure("output_exists", f"output already exists: {path}")

    task = _task_for_artifact_type(full_type)
    full_prompt_path.write_text(
        _render_variant_prompt(
            case_label=label,
            artifact_type=full_type,
            variant="full",
            input_path=full_path,
            task=task,
        ),
        encoding="utf-8",
        newline="\n",
    )
    stripped_prompt_path.write_text(
        _render_variant_prompt(
            case_label=label,
            artifact_type=full_type,
            variant="stripped",
            input_path=stripped_path,
            task=task,
        ),
        encoding="utf-8",
        newline="\n",
    )
    worksheet_path.write_text(
        _render_worksheet(
            case_label=label,
            artifact_type=full_type,
            full_prompt_path=full_prompt_path,
            stripped_prompt_path=stripped_prompt_path,
        ),
        encoding="utf-8",
        newline="\n",
    )

    full_bytes = full_path.stat().st_size
    stripped_bytes = stripped_path.stat().st_size
    return {
        "case_label": label,
        "artifact_type": full_type,
        "view_directory": str(view_directory),
        "full_json_path": str(full_path),
        "stripped_json_path": str(stripped_path),
        "full_bytes": full_bytes,
        "stripped_bytes": stripped_bytes,
        "stripped_to_full_ratio": round(stripped_bytes / full_bytes, 6) if full_bytes else None,
        "full_prompt_path": str(full_prompt_path),
        "stripped_prompt_path": str(stripped_prompt_path),
        "comparison_worksheet_path": str(worksheet_path),
        "probe_status": "needs_agent_or_owner_outputs",
    }


def _read_json(path: Path, *, role: str) -> dict[str, Any]:
    if not path.exists():
        raise RedditAgentViewABProbeFailure(
            f"{role}_missing",
            f"{role} JSON does not exist: {path}",
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RedditAgentViewABProbeFailure(
            f"{role}_not_json",
            f"{role} JSON is invalid: {exc}",
        ) from exc
    if not isinstance(data, dict):
        raise RedditAgentViewABProbeFailure(f"{role}_not_object", f"{role} JSON must be an object")
    return data


def _detect_full_artifact_type(full: dict[str, Any]) -> str:
    for artifact_type in (
        "reddit_thread_consolidation",
        "reddit_candidate_url_intake",
        "reddit_graph_frontier_register",
    ):
        if isinstance(full.get(artifact_type), dict):
            return artifact_type
    raise RedditAgentViewABProbeFailure(
        "unsupported_full_artifact",
        "full JSON must contain a supported Reddit artifact",
    )


def _extract_stripped_view(stripped: dict[str, Any], path: Path) -> dict[str, Any]:
    view = stripped.get("reddit_agent_view")
    if not isinstance(view, dict):
        raise RedditAgentViewABProbeFailure(
            "stripped_view_missing",
            f"{path} does not contain reddit_agent_view",
        )
    if view.get("view_mode") != "stripped_agent_context":
        raise RedditAgentViewABProbeFailure(
            "stripped_view_mode_mismatch",
            f"{path} is not a stripped_agent_context view",
        )
    if not isinstance(view.get("stripped"), dict):
        raise RedditAgentViewABProbeFailure(
            "stripped_payload_missing",
            f"{path} does not contain a stripped payload object",
        )
    artifact_type = view.get("source_artifact_type")
    if not isinstance(artifact_type, str) or not artifact_type:
        raise RedditAgentViewABProbeFailure(
            "stripped_artifact_type_missing",
            f"{path} does not declare source_artifact_type",
        )
    return view


def _case_label(view_directory: Path) -> str:
    raw = view_directory.name.strip() or "case"
    cleaned = "".join(char.lower() if char.isalnum() else "_" for char in raw)
    return "_".join(part for part in cleaned.split("_") if part) or "case"


def _task_for_artifact_type(artifact_type: str) -> str:
    if artifact_type == "reddit_thread_consolidation":
        return (
            "Identify the thread's substantive claims, advice, disagreement, and visible "
            "limitations. Flag any missing context that would change whether this thread "
            "is useful for later semantic projection."
        )
    if artifact_type == "reddit_candidate_url_intake":
        return (
            "Identify the candidate URLs or subreddits, the declared bounds, visible stop "
            "reason, and which candidates look worth a separate promotion decision. Do not "
            "promote anything automatically."
        )
    if artifact_type == "reddit_graph_frontier_register":
        return (
            "Identify graph shape, repeated candidates, selected frontier decisions, and "
            "which next bounded run would be best supported by the evidence. Do not claim "
            "source completeness."
        )
    raise AssertionError(f"unhandled artifact type: {artifact_type}")


def _render_variant_prompt(
    *,
    case_label: str,
    artifact_type: str,
    variant: str,
    input_path: Path,
    task: str,
) -> str:
    return "\n".join(
        [
            f"# Reddit Agent View A/B Probe - {case_label} - {variant}",
            "",
            f"Input variant: `{variant}`",
            f"Artifact type: `{artifact_type}`",
            f"Input JSON path: `{input_path}`",
            "",
            "## Task",
            "",
            task,
            "",
            "## Rules",
            "",
            "- Use only the supplied JSON artifact.",
            "- Preserve uncertainty; do not infer deleted, hidden, or inaccessible content.",
            "- Name when provenance or audit detail is insufficient for the task.",
            "- Do not claim Data Capture handoff, ECR, Cleaning, Judgment, source completeness, or commercial readiness.",
            "",
            "## Output",
            "",
            "Return:",
            "- substantive findings",
            "- missing or weak context",
            "- provenance sufficiency",
            "- hallucination-risk notes",
            "- whether full JSON is required for this task, and why",
            "",
        ]
    )


def _render_worksheet(
    *,
    case_label: str,
    artifact_type: str,
    full_prompt_path: Path,
    stripped_prompt_path: Path,
) -> str:
    return "\n".join(
        [
            f"# Reddit Agent View A/B Comparison - {case_label}",
            "",
            f"Artifact type: `{artifact_type}`",
            f"Full prompt: `{full_prompt_path}`",
            f"Stripped prompt: `{stripped_prompt_path}`",
            "",
            "## Compare",
            "",
            "| Dimension | Full output | Stripped output | Difference | Decision |",
            "| --- | --- | --- | --- | --- |",
            "| Substantive claim parity |  |  |  |  |",
            "| Missed context |  |  |  |  |",
            "| Provenance sufficiency |  |  |  |  |",
            "| Context economy |  |  |  |  |",
            "| Hallucination risk |  |  |  |  |",
            "| Full JSON required for task |  |  |  |  |",
            "",
            "## Decision Options",
            "",
            "- `stripped_default_for_agent_context`",
            "- `full_required_for_this_task`",
            "- `strip_profile_needs_revision`",
            "- `inconclusive_needs_another_case`",
            "",
            "## Non-Claims",
            "",
            "- this worksheet is not agent output",
            "- this worksheet is not validation or readiness",
            "- this worksheet does not choose the default view by itself",
            "",
        ]
    )


def _render_receipt(manifest: dict[str, Any]) -> str:
    data = manifest["reddit_agent_view_ab_probe"]
    lines = [
        "# Reddit Agent View A/B Probe Receipt",
        "",
        f"- Schema: `{data['schema_version']}`",
        f"- Probe status: `{data['probe_status']}`",
        f"- Case count: {data['case_count']}",
        "",
        "## Cases",
    ]
    for case in data["cases"]:
        lines.append(
            f"- `{case['case_label']}`: {case['artifact_type']}, "
            f"{case['full_bytes']} bytes full, {case['stripped_bytes']} bytes stripped, "
            f"ratio {case['stripped_to_full_ratio']}"
        )
    lines.extend(["", "## Non-Claims"])
    lines.extend(f"- {item}" for item in data["non_claims"])
    return "\n".join(lines) + "\n"
