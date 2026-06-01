from __future__ import annotations

import ast
from pathlib import Path


FORBIDDEN_IMPORTS = {"openai", "anthropic", "litellm", "langchain"}


def test_no_llm_imports_in_scoring_and_reports() -> None:
    project_root = Path(__file__).resolve().parents[2]
    target_paths = (
        list((project_root / "scoring").glob("*.py"))
        + list((project_root / "reports").glob("*.py"))
        + list((project_root / "runners").glob("*.py"))
        + list((project_root / "schemas").glob("*.py"))
        + [project_root / "harness_utils.py"]
    )
    for path in target_paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported = {alias.name.split(".")[0] for alias in node.names}
                assert not (imported & FORBIDDEN_IMPORTS), f"Forbidden import in {path}"
            if isinstance(node, ast.ImportFrom) and node.module:
                imported = node.module.split(".")[0]
                assert imported not in FORBIDDEN_IMPORTS, f"Forbidden import in {path}"
