from __future__ import annotations

import ast
from pathlib import Path

# The finalization model + validate-only consumer must be a pure, deterministic,
# no-I/O, no-LLM module: block-don't-repair means it never reaches out (no network,
# no provider SDK) and computes only over its inputs.
FORBIDDEN_TOP_LEVEL_IMPORTS = {
    "openai",
    "anthropic",
    "litellm",
    "langchain",
    "urllib",
    "requests",
    "httpx",
    "socket",
    "http",
}


def test_finalization_models_is_pure_no_io_no_llm() -> None:
    project_root = Path(__file__).resolve().parents[2]
    path = project_root / "schemas" / "finalization_models.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported = {alias.name.split(".")[0] for alias in node.names}
            offending = imported & FORBIDDEN_TOP_LEVEL_IMPORTS
            assert not offending, f"Forbidden import {offending} in {path}"
        if isinstance(node, ast.ImportFrom) and node.module:
            top = node.module.split(".")[0]
            assert top not in FORBIDDEN_TOP_LEVEL_IMPORTS, f"Forbidden import {top} in {path}"
