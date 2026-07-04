from __future__ import annotations

import ast
from pathlib import Path


FORBIDDEN_IMPORT_ROOTS = {
    "aiohttp",
    "bs4",
    "httpx",
    "playwright",
    "requests",
    "scrapy",
    "selenium",
    "socket",
    "urllib",
}


def test_source_quality_report_skeleton_has_no_runtime_acquisition_imports() -> None:
    project_root = Path(__file__).resolve().parents[2]
    target_paths = [
        project_root / "source_capture" / "source_quality.py",
        project_root / "runners" / "run_source_quality_report_skeleton.py",
        project_root / "runners" / "run_source_quality_state_assembler.py",
    ]

    for path in target_paths:
        assert not _forbidden_import_roots(path), f"Forbidden import in {path}"


def _forbidden_import_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    forbidden: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            forbidden.update(
                alias.name.split(".")[0]
                for alias in node.names
                if alias.name.split(".")[0] in FORBIDDEN_IMPORT_ROOTS
            )
        if isinstance(node, ast.ImportFrom) and node.module:
            root = node.module.split(".")[0]
            if root in FORBIDDEN_IMPORT_ROOTS:
                forbidden.add(root)
    return forbidden
