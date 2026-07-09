from __future__ import annotations

import argparse
from datetime import UTC, datetime
import json
import sys
from pathlib import Path
from typing import Any, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.reddit_graph_frontier import (
    FrontierDecision,
    build_graph_frontier_register,
    prepare_next_bounded_run_envelope,
    validate_next_run_envelope,
    write_graph_frontier_register,
)


def run_reddit_graph_frontier_register(
    *,
    candidate_intake_output_path: Path,
    output_directory: Path,
    register_id: str,
    access_mode: str,
    source_policy_posture: str,
    prior_register_pointer: str | None = None,
    selected_node_id: str | None = None,
    selected_candidate_value: str | None = None,
    frontier_selection_reason: str | None = None,
    frontier_selection_actor: str = "operator_frontier_selection",
    next_run_id: str | None = None,
    declared_topic_theme_or_query: str | None = None,
    candidate_surface_allowlist: tuple[str, ...] = (),
    caps: dict[str, int] | None = None,
    exclusions: tuple[str, ...] = (),
    next_access_mode: str | None = None,
    next_source_policy_posture: str | None = None,
    stop_condition: str = "caps_reached",
) -> dict[str, str | None]:
    candidate_output = json.loads(candidate_intake_output_path.read_text(encoding="utf-8"))
    base_register = build_graph_frontier_register(
        register_id=register_id,
        candidate_intake_output=candidate_output,
        access_mode=access_mode,
        source_policy_posture=source_policy_posture,
        prior_register_pointer=prior_register_pointer,
    )

    selected_id = _resolve_selected_node_id(
        register=base_register,
        selected_node_id=selected_node_id,
        selected_candidate_value=selected_candidate_value,
    )
    decisions: list[FrontierDecision] = []
    next_envelope: dict[str, Any] | None = None
    if selected_id:
        if not frontier_selection_reason:
            raise ValueError("frontier_selection_reason is required when a frontier node is selected")
        decisions.append(
            FrontierDecision(
                decision_id=f"frontier_decision:{register_id}:{selected_id}",
                selected_node_id=selected_id,
                frontier_selection_reason=frontier_selection_reason,
                frontier_selection_actor=frontier_selection_actor,
                frontier_selection_timestamp=_utc_now(),
                next_run_id_or_none=next_run_id,
            )
        )

    register = build_graph_frontier_register(
        register_id=register_id,
        candidate_intake_output=candidate_output,
        access_mode=access_mode,
        source_policy_posture=source_policy_posture,
        prior_register_pointer=prior_register_pointer,
        frontier_decisions=decisions,
    )
    write_result = write_graph_frontier_register(register=register, output_directory=output_directory)

    if selected_id and next_run_id:
        if not declared_topic_theme_or_query:
            raise ValueError("declared_topic_theme_or_query is required when next_run_id is supplied")
        if not candidate_surface_allowlist:
            raise ValueError("at least one candidate surface is required when next_run_id is supplied")
        if not caps:
            raise ValueError("caps are required when next_run_id is supplied")
        next_envelope = prepare_next_bounded_run_envelope(
            register=register,
            selected_node_id=selected_id,
            next_run_id=next_run_id,
            declared_topic_theme_or_query=declared_topic_theme_or_query,
            candidate_surface_allowlist=candidate_surface_allowlist,
            caps=caps,
            exclusions=exclusions,
            access_mode=next_access_mode or access_mode,
            source_policy_posture=next_source_policy_posture or source_policy_posture,
            stop_condition=stop_condition,
        )
        validate_next_run_envelope(next_envelope)
        next_path = output_directory / "reddit_graph_frontier_next_run_envelope.json"
        next_path.write_text(json.dumps(next_envelope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        next_path = None

    return {
        "register_json_path": write_result["json_path"],
        "register_receipt_path": write_result["receipt_path"],
        "next_run_envelope_path": str(next_path) if next_path else None,
    }


def _resolve_selected_node_id(
    *,
    register: dict[str, Any],
    selected_node_id: str | None,
    selected_candidate_value: str | None,
) -> str | None:
    if selected_node_id and selected_candidate_value:
        raise ValueError("choose selected_node_id or selected_candidate_value, not both")
    if selected_node_id:
        node_ids = {node["node_id"] for node in register["reddit_graph_frontier_register"]["nodes"]}
        if selected_node_id not in node_ids:
            raise ValueError(f"selected_node_id not found in register: {selected_node_id}")
        return selected_node_id
    if not selected_candidate_value:
        return None
    matches = [
        node["node_id"]
        for node in register["reddit_graph_frontier_register"]["nodes"]
        if str(node.get("candidate_value_or_none", "")).lower() == selected_candidate_value.lower()
    ]
    if len(matches) != 1:
        raise ValueError(
            f"selected_candidate_value must match exactly one candidate node; matched {len(matches)}"
        )
    return matches[0]


def _parse_caps(values: Sequence[str]) -> dict[str, int]:
    caps: dict[str, int] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"cap must be name=value: {value}")
        name, raw_number = value.split("=", 1)
        name = name.strip()
        if not name:
            raise ValueError("cap name is required")
        number = int(raw_number)
        if number < 1:
            raise ValueError(f"cap must be positive: {value}")
        caps[name] = number
    return caps


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a bounded Reddit Graph Frontier Register from Candidate URL Intake output."
    )
    parser.add_argument("--candidate-intake-output", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument("--register-id", required=True)
    parser.add_argument("--access-mode", required=True)
    parser.add_argument("--source-policy-posture", required=True)
    parser.add_argument("--prior-register-pointer")
    parser.add_argument("--selected-node-id")
    parser.add_argument("--selected-candidate-value")
    parser.add_argument("--frontier-selection-reason")
    parser.add_argument("--frontier-selection-actor", default="operator_frontier_selection")
    parser.add_argument("--next-run-id")
    parser.add_argument("--declared-topic-theme-or-query")
    parser.add_argument("--candidate-surface", action="append", default=[])
    parser.add_argument("--cap", action="append", default=[])
    parser.add_argument("--exclusion", action="append", default=[])
    parser.add_argument("--next-access-mode")
    parser.add_argument("--next-source-policy-posture")
    parser.add_argument("--stop-condition", default="caps_reached")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        result = run_reddit_graph_frontier_register(
            candidate_intake_output_path=args.candidate_intake_output,
            output_directory=args.output_directory,
            register_id=args.register_id,
            access_mode=args.access_mode,
            source_policy_posture=args.source_policy_posture,
            prior_register_pointer=args.prior_register_pointer,
            selected_node_id=args.selected_node_id,
            selected_candidate_value=args.selected_candidate_value,
            frontier_selection_reason=args.frontier_selection_reason,
            frontier_selection_actor=args.frontier_selection_actor,
            next_run_id=args.next_run_id,
            declared_topic_theme_or_query=args.declared_topic_theme_or_query,
            candidate_surface_allowlist=tuple(args.candidate_surface),
            caps=_parse_caps(args.cap),
            exclusions=tuple(args.exclusion),
            next_access_mode=args.next_access_mode,
            next_source_policy_posture=args.next_source_policy_posture,
            stop_condition=args.stop_condition,
        )
    except Exception as exc:
        parser.exit(status=2, message=f"reddit graph frontier register failed: {exc}\n")

    print(result["register_json_path"])
    if result["next_run_envelope_path"]:
        print(result["next_run_envelope_path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
