from __future__ import annotations

import tomllib
from pathlib import Path


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _package_find_config() -> dict[str, list[str]]:
    pyproject = tomllib.loads((_project_root() / "pyproject.toml").read_text(encoding="utf-8"))
    return pyproject["tool"]["setuptools"]["packages"]["find"]


def _pattern_matches(package: str, pattern: str) -> bool:
    if pattern.endswith(".*"):
        prefix = pattern[:-2]
        return package.startswith(f"{prefix}.")
    return package == pattern


def _declared_packages() -> set[str]:
    project_root = _project_root()
    config = _package_find_config()
    includes = config["include"]
    excludes = config.get("exclude", [])
    discovered: set[str] = set()

    for init_file in project_root.rglob("__init__.py"):
        package = ".".join(init_file.parent.relative_to(project_root).parts)
        if any(_pattern_matches(package, pattern) for pattern in includes) and not any(
            _pattern_matches(package, pattern) for pattern in excludes
        ):
            discovered.add(package)
    return discovered


def test_package_config_discovers_all_top_level_runtime_packages() -> None:
    project_root = _project_root()
    expected = {
        path.name
        for path in project_root.iterdir()
        if path.is_dir() and (path / "__init__.py").is_file()
    }

    assert expected <= _declared_packages()


def test_package_config_includes_repaired_runtime_packages() -> None:
    project_root = _project_root()
    pyproject = tomllib.loads((project_root / "pyproject.toml").read_text(encoding="utf-8"))
    includes = set(pyproject["tool"]["setuptools"]["packages"]["find"]["include"])
    expected = {"evidence_binding", "reports", "signal_content"}

    assert expected <= includes
    for package in expected:
        assert (project_root / package / "__init__.py").is_file()
        assert package in _declared_packages()


def test_package_config_excludes_report_data_tree() -> None:
    config = _package_find_config()
    excludes = set(config.get("exclude", []))

    assert {"reports.product_learning", "reports.product_learning.*"} <= excludes
    assert "reports.product_learning" not in _declared_packages()
