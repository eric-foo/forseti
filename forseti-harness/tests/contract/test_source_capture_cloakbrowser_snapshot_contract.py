from __future__ import annotations

import ast
import importlib
from pathlib import Path


FORBIDDEN_IMPORT_ROOTS = {
    "aiohttp",
    "archivebox",
    "bs4",
    "cloakbrowser",
    "httpx",
    "patchright",
    "playwright",
    "praw",
    "requests",
    "scrapy",
    "selenium",
    "socket",
    "webbrowser",
}


def test_cloakbrowser_snapshot_module_imports_without_cloakbrowser_installed() -> None:
    module = importlib.import_module("source_capture.adapters.cloakbrowser_snapshot")

    assert hasattr(module, "fetch_cloakbrowser_snapshot_capture")


def test_cloakbrowser_snapshot_adapter_contract_has_no_runtime_acquisition_imports() -> None:
    project_root = Path(__file__).resolve().parents[2]
    target_paths = [
        project_root / "source_capture" / "adapters" / "cloakbrowser_snapshot.py",
        project_root / "runners" / "run_source_capture_cloakbrowser_packet.py",
    ]

    for target in target_paths:
        assert target.exists(), f"CloakBrowser source-capture path missing: {target}"
        forbidden = _forbidden_import_roots(target)

        assert forbidden == set()


def test_cloakbrowser_snapshot_adapter_does_not_expose_secret_or_persistent_profile_terms() -> None:
    project_root = Path(__file__).resolve().parents[2]
    target_paths = [
        project_root / "source_capture" / "adapters" / "cloakbrowser_snapshot.py",
        project_root / "runners" / "run_source_capture_cloakbrowser_packet.py",
    ]
    source = "\n".join(path.read_text(encoding="utf-8") for path in target_paths)

    forbidden_surface_terms = {
        "**kwargs",
        "storage_state_path",
        "launch_persistent_context",
        "proxy_url",
    }

    assert not any(term in source for term in forbidden_surface_terms)
    assert "SECRET_LIKE_QUERY_KEYS" in source
    assert "SECRET_LIKE_WARNING_TERMS" in source


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
