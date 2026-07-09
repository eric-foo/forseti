from __future__ import annotations

import ast
from pathlib import Path
import shutil
import uuid

import pytest


FORBIDDEN_IMPORT_ROOTS = {
    "aiohttp",
    "bs4",
    "httpx",
    "playwright",
    "requests",
    "scrapy",
    "selenium",
    "socket",
}
# `urllib` is stdlib: `urllib.parse` is pure URL string parsing (no acquisition) and
# is allowed at this layer; only its network surfaces are forbidden.
FORBIDDEN_URLLIB_SUBMODULES = {"request", "error"}


def test_source_capture_packet_has_no_runtime_acquisition_imports() -> None:
    project_root = Path(__file__).resolve().parents[2]
    target_paths = sorted((project_root / "source_capture").glob("*.py")) + [
        project_root / "harness_utils.py",
        project_root / "runners" / "run_source_capture_packet.py",
    ]

    assert target_paths, "source_capture package must exist"

    for path in target_paths:
        assert not _forbidden_import_roots(path), f"Forbidden import in {path}"


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"source_capture_contract_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_forbidden_import_detector_catches_from_urllib_import_request(scratch_dir: Path) -> None:
    path = scratch_dir / "bad_import.py"
    path.write_text("from urllib import request\n", encoding="utf-8")

    assert _forbidden_import_roots(path) == {"urllib.request"}


def test_forbidden_import_detector_allows_urllib_parse(scratch_dir: Path) -> None:
    path = scratch_dir / "ok_import.py"
    path.write_text("from urllib.parse import unquote, urlparse\n", encoding="utf-8")

    assert _forbidden_import_roots(path) == set()


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
