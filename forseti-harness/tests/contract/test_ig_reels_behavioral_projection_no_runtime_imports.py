from __future__ import annotations

import ast
from pathlib import Path


FORBIDDEN_IMPORT_ROOTS = {
    "aiohttp",
    "anthropic",
    "bs4",
    "httpx",
    "langchain",
    "litellm",
    "openai",
    "playwright",
    "requests",
    "scrapy",
    "selenium",
    "socket",
}
FORBIDDEN_URLLIB_SUBMODULES = {"request", "error"}


def test_ig_reels_behavioral_projection_modules_have_no_runtime_acquisition_or_llm_imports() -> None:
    project_root = Path(__file__).resolve().parents[2]
    targets = [
        project_root / "source_capture" / "ig_reels_behavioral_projection.py",
        project_root / "source_capture" / "ig_reels_behavioral_lake.py",
    ]

    for target in targets:
        assert target.is_file(), f"{target.name} must exist"
        assert not _forbidden_import_roots(target), f"Forbidden import in {target}"


def test_forbidden_import_detector_catches_runtime_acquisition_import(tmp_path: Path) -> None:
    path = tmp_path / "bad_import.py"
    path.write_text("from urllib import request\n", encoding="utf-8")

    assert _forbidden_import_roots(path) == {"urllib.request"}


def test_forbidden_import_detector_catches_llm_import(tmp_path: Path) -> None:
    path = tmp_path / "bad_llm_import.py"
    path.write_text("import openai\n", encoding="utf-8")

    assert _forbidden_import_roots(path) == {"openai"}


def _forbidden_import_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    forbidden: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                parts = alias.name.split(".")
                if parts[0] in FORBIDDEN_IMPORT_ROOTS:
                    forbidden.add(parts[0])
                elif parts[0] == "urllib" and len(parts) > 1 and parts[1] in FORBIDDEN_URLLIB_SUBMODULES:
                    forbidden.add(f"urllib.{parts[1]}")
        if isinstance(node, ast.ImportFrom) and node.module:
            parts = node.module.split(".")
            if parts[0] in FORBIDDEN_IMPORT_ROOTS:
                forbidden.add(parts[0])
            elif parts[0] == "urllib":
                if len(parts) > 1:
                    if parts[1] in FORBIDDEN_URLLIB_SUBMODULES:
                        forbidden.add(f"urllib.{parts[1]}")
                else:
                    forbidden.update(
                        f"urllib.{alias.name}"
                        for alias in node.names
                        if alias.name in FORBIDDEN_URLLIB_SUBMODULES
                    )
    return forbidden
