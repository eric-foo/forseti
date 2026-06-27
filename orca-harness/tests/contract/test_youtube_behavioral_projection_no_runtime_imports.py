from __future__ import annotations

import ast
from pathlib import Path
import shutil
import uuid

import pytest


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


def test_youtube_behavioral_projection_has_no_runtime_acquisition_or_llm_imports() -> None:
    project_root = Path(__file__).resolve().parents[2]
    target = project_root / "youtube_capture" / "behavioral_projection.py"

    assert target.is_file(), "youtube behavioral projection module must exist"
    assert not _forbidden_import_roots(target), f"Forbidden import in {target}"


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"youtube_projection_contract_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_forbidden_import_detector_catches_runtime_acquisition_import(scratch_dir: Path) -> None:
    path = scratch_dir / "bad_import.py"
    path.write_text("from urllib import request\n", encoding="utf-8")

    assert _forbidden_import_roots(path) == {"urllib.request"}


def test_forbidden_import_detector_catches_llm_import(scratch_dir: Path) -> None:
    path = scratch_dir / "bad_llm_import.py"
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
