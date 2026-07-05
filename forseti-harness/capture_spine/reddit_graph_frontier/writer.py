from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from capture_spine.reddit_graph_frontier.validation import validate_graph_frontier_register


def write_graph_frontier_register(
    *,
    register: dict[str, Any],
    output_directory: Path,
    json_name: str = "reddit_graph_frontier_register.json",
    receipt_name: str = "reddit_graph_frontier_register_receipt.md",
) -> dict[str, str]:
    validate_graph_frontier_register(register)
    output_directory.mkdir(parents=True, exist_ok=True)
    json_path = output_directory / json_name
    receipt_path = output_directory / receipt_name
    json_path.write_text(json.dumps(register, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    receipt_path.write_text(_render_receipt(register), encoding="utf-8")
    return {"json_path": str(json_path), "receipt_path": str(receipt_path)}


def _render_receipt(register: dict[str, Any]) -> str:
    graph = register["reddit_graph_frontier_register"]
    provenance = graph["provenance"]
    return "\n".join(
        [
            "# Reddit Graph Frontier Register Receipt",
            "",
            f"Register ID: {graph['register_id']}",
            f"Source intake run ID: {graph['source_intake_run_id']}",
            f"Source surface: {provenance['source_surface']}",
            f"Stop reason: {provenance['stop_reason']}",
            f"Nodes: {len(graph['nodes'])}",
            f"Edges: {len(graph['edges'])}",
            f"Frontier decisions: {len(graph['frontier_decisions'])}",
            "",
            "Non-claims:",
            *[f"- {non_claim}" for non_claim in graph["non_claims"]],
            "",
        ]
    )
