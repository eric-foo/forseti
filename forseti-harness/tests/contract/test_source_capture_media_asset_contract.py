from __future__ import annotations

import ast
from pathlib import Path


FORBIDDEN_IMPORT_ROOTS = {
    "aiohttp",
    "archivebox",
    "bs4",
    "httpx",
    "playwright",
    "praw",
    "requests",
    "scrapy",
    "selenium",
    "webbrowser",
}

ALLOWED_DIRECT_HTTP_IMPORTS = {
    "source_capture.adapters.direct_http",
}


def test_media_asset_adapter_avoids_discovery_browser_api_and_scraper_imports() -> None:
    project_root = Path(__file__).resolve().parents[2]
    target_paths = [
        project_root / "source_capture" / "adapters" / "__init__.py",
        project_root / "source_capture" / "adapters" / "media_asset.py",
        project_root / "runners" / "run_source_capture_media_packet.py",
    ]

    for path in target_paths:
        assert path.exists(), f"media asset path missing: {path}"
        assert not _forbidden_import_roots(path), f"Forbidden import in {path}"
        assert not _forbidden_discovery_imports(path), f"Forbidden discovery import in {path}"


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


def _forbidden_discovery_imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    forbidden: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.startswith("source_capture.adapters.direct_http"):
                continue
            if "html" in node.module or "parser" in node.module:
                forbidden.add(node.module)
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("html") or "parser" in alias.name:
                    forbidden.add(alias.name)
    return forbidden
