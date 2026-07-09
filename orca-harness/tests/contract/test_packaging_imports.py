from __future__ import annotations

import tomllib
from pathlib import Path


def test_package_config_includes_runtime_packages() -> None:
    project_root = Path(__file__).resolve().parents[2]
    pyproject = tomllib.loads((project_root / "pyproject.toml").read_text(encoding="utf-8"))
    includes = set(pyproject["tool"]["setuptools"]["packages"]["find"]["include"])
    expected = {"evidence_binding", "reports", "signal_content"}

    assert expected <= includes
    for package in expected:
        assert (project_root / package / "__init__.py").is_file()