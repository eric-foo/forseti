from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_PATH = REPO_ROOT / ".agents" / "hooks" / "check_review_output_provenance.py"
FIXTURE_DIR = REPO_ROOT / "orca-harness" / "tests" / "fixtures" / "review_outputs"
SCOPE_PREFIX = "docs/review-outputs/adversarial-artifact-reviews/"


def _load_validator():
    spec = importlib.util.spec_from_file_location("check_review_output_provenance", VALIDATOR_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = _load_validator()


def _text(name: str) -> str:
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


def _codes(name: str) -> set[str]:
    return {finding.code for finding in validator.check_text(SCOPE_PREFIX + name, _text(name))}


def test_valid_review_output_passes() -> None:
    assert validator.check_text(SCOPE_PREFIX + "valid_review_output.md", _text("valid_review_output.md")) == []


def test_missing_provenance_fails() -> None:
    codes = _codes("bad_missing_provenance.md")
    assert "missing_reviewed_by" in codes
    assert "missing_authored_by" in codes


def test_missing_review_use_boundary_fails() -> None:
    assert "missing_review_use_boundary" in _codes("bad_missing_boundary.md")


def test_missing_retrieval_header_fails() -> None:
    assert "review_output_retrieval_header_invalid" in _codes("bad_missing_header.md")


def test_unrecorded_provenance_values_pass() -> None:
    text = _text("valid_review_output.md").replace("gpt-5-codex", "unrecorded").replace("claude-opus-4.8", "unrecorded")
    assert validator.check_text(SCOPE_PREFIX + "valid_review_output.md", text) == []


def test_no_nonclaim_wording_passes_review_use_boundary() -> None:
    text = _text("valid_review_output.md").replace(
        "They are not approval, validation,",
        "No validation, readiness, approval,",
        1,
    )

    assert validator.check_text(SCOPE_PREFIX + "valid_review_output.md", text) == []



def test_unrelated_decision_input_and_nonapproval_do_not_pass_boundary() -> None:
    assert "missing_review_use_boundary" in _codes("bad_unrelated_boundary.md")


def test_review_output_readmes_are_skipped() -> None:
    text = _text("bad_missing_provenance.md")

    assert validator.check_text("docs/review-outputs/README.md", text) == []
    assert validator.check_text("docs/review-outputs/adversarial-artifact-reviews/README.md", text) == []

@pytest.mark.parametrize(
    "relpath",
    [
        "docs/prompts/reviews/x.md",
        "docs/review-inputs/x.md",
        "docs/review-outputs/x.txt",
        "orca/product/x.md",
    ],
)
def test_out_of_scope_paths_are_skipped(relpath: str) -> None:
    assert validator.check_text(relpath, _text("bad_missing_provenance.md")) == []
