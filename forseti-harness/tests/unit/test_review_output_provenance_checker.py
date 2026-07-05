from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_PATH = REPO_ROOT / ".agents" / "hooks" / "check_review_output_provenance.py"
FIXTURE_DIR = REPO_ROOT / "forseti-harness" / "tests" / "fixtures" / "review_outputs"
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


def _valid_text_with_body(body: str) -> str:
    return """# Fixture Review Output

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Fixture review output for provenance checker.
use_when:
  - Testing review-output provenance shape.
authority_boundary: retrieval_only
reviewed_by: gpt-5-codex
authored_by: claude-opus-4.8
review_use_boundary: >
  Findings are decision input only. They are not approval, validation,
  mandatory remediation, or executor-ready patch authority until separately
  accepted or authorized.
```

""" + body


def _codes_for_body(body: str) -> set[str]:
    text = _valid_text_with_body(body)
    return {finding.code for finding in validator.check_text(SCOPE_PREFIX + "inline.md", text)}


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


def test_malformed_diff_fence_fails() -> None:
    codes = _codes_for_body("## Diff\n\n```diff# generated comment\ndiff --git a/x b/x\n```\n")

    assert "malformed_code_fence" in codes


def test_unbalanced_code_fence_fails() -> None:
    codes = _codes_for_body("## Diff\n\n```diff\ndiff --git a/x b/x\n")

    assert "unbalanced_code_fences" in codes


def test_diff_line_outside_diff_fence_fails() -> None:
    codes = _codes_for_body("## Diff\n\ndiff --git a/x b/x\n")

    assert "diff_line_outside_diff_fence" in codes


def test_collapsed_diff_block_fails() -> None:
    codes = _codes_for_body(
        "## Diff\n\n```diff\n"
        "diff --git a/x b/x index 111..222 100644 --- a/x +++ b/x @@ -1 +1 @@\n"
        "```\n"
    )

    assert "collapsed_diff_block" in codes


def test_future_tense_report_check_fails() -> None:
    codes = _codes_for_body(
        "## Validation Evidence\n\n"
        "- Report provenance: must be checked after this report is written.\n"
    )

    assert "future_tense_review_output_check" in codes


def test_trailing_whitespace_fails() -> None:
    assert "trailing_whitespace" in _codes_for_body("## Findings  \n\nNo fixture findings.\n")


def test_future_tense_report_check_variant_wording_fails() -> None:
    codes = _codes_for_body(
        "## Validation Evidence\n\n"
        "- The provenance check will be verified once this report is merged.\n"
    )

    assert "future_tense_review_output_check" in codes


def test_review_use_boundary_missing_one_required_term_fails() -> None:
    text = _text("valid_review_output.md").replace(
        "They are not approval, validation,\n  mandatory remediation, or executor-ready patch authority until separately\n  accepted or authorized.",
        "They are not approval, validation, or readiness until separately accepted or authorized.",
        1,
    )

    assert "missing_review_use_boundary" in {
        finding.code for finding in validator.check_text(SCOPE_PREFIX + "valid_review_output.md", text)
    }


def test_git_lines_raises_on_nonzero_git_exit() -> None:
    with pytest.raises(validator.GitSelectionError):
        validator.git_lines(REPO_ROOT, ["diff", "--name-only", "__definitely_missing_base__...HEAD"])


def test_diff_mode_fails_closed_when_base_is_unresolvable(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = validator.main(["--diff", "__definitely_missing_base__", "--strict"])

    assert exit_code != 0
    assert "could not be evaluated" in capsys.readouterr().err


def test_selftest_expected_codes_catch_a_regressed_detection(monkeypatch: pytest.MonkeyPatch) -> None:
    real_check_text = validator.check_text

    def dropping_check_text(relpath: str, text: str) -> list[validator.Finding]:
        return [f for f in real_check_text(relpath, text) if f.code != "malformed_code_fence"]

    monkeypatch.setattr(validator, "check_text", dropping_check_text)

    assert validator.selftest() == 1


def test_diff_selector_uses_base_triple_dot(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []

    def fake_git_lines(root: Path, args: list[str]) -> list[str]:
        calls.append(args)
        return ["docs/review-outputs/x.md"]

    monkeypatch.setattr(validator, "git_lines", fake_git_lines)

    assert validator.diff_paths(REPO_ROOT, "origin/main") == ["docs/review-outputs/x.md"]
    assert calls == [["diff", "--diff-filter=ACMR", "--find-renames", "--name-only", "origin/main...HEAD"]]
