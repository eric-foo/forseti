# Review Output Integrity Gate Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: >
  Same-family advisory implementation/code review of the review-output
  provenance and integrity gate lane.
use_when:
  - Adjudicating the review-output integrity checker, tests, CI wiring, and review-output closeout bindings.
authority_boundary: retrieval_only
reviewed_by: gpt-5-codex
authored_by: openai-gpt-family-codex-exact-model-unrecorded
de_correlation_status: same-family/advisory-only
review_use_boundary: >
  Findings are decision input only. They are not approval, validation,
  readiness, mandatory remediation, no-new-seam discovery, or executor-ready
  patch authority until separately accepted or authorized.
```

## Source Context

SOURCE_CONTEXT_READY.

Required authority and target sources were readable in the target worktree. The target branch was `codex/review-output-integrity-gate` at `a951d279eb4100e5309568ed225172946a3b5ad0`. `git status --short` was empty before this report write. The prompt and implementation target files were added or changed in the same lane commit, with no later target-file drift observed.

This is same-family advisory review only. It does not claim cross-vendor discovery, no-new-seam, formal pass, readiness, approval, mandatory remediation, or a patch queue.

## Findings

### ROIG-01 - advisory priority: major - Diff mode can fail open when the base ref is unavailable

Location: `.agents/hooks/check_review_output_provenance.py:97`, `.agents/hooks/check_review_output_provenance.py:105`, `.agents/hooks/check_review_output_provenance.py:128`, `.agents/hooks/check_review_output_provenance.py:401`, `.agents/hooks/check_review_output_provenance.py:405`; `.github/workflows/ci.yml:68`.

Evidence: `git_lines` returns an empty list on any nonzero git subprocess result, and `diff_paths` delegates the CI selector to that helper. `main` then treats an empty selected path list as "no review-output files selected" and returns 0. The CI step uses `python .agents/hooks/check_review_output_provenance.py --diff origin/main --strict`.

Observed probe: `python -B .agents/hooks/check_review_output_provenance.py --diff __definitely_missing_base__ --strict` exited 0 and printed `review-output-provenance: no review-output files selected -- OK`.

Impact: If the CI base ref is unavailable, misspelled, or otherwise not diffable, the gate can report a clean no-selection result instead of failing the review-output gate. That creates the fake-green path the lane is meant to avoid for changed review-output artifacts.

Minimum closure condition: Diff mode distinguishes "no review-output files selected from a successful diff" from "diff selector could not be evaluated", and strict CI mode exits nonzero on the latter unless Orca explicitly accepts and documents fail-open behavior for this checker.

Next authorized action: Advisory only; request patch authorization or CA adjudication. No source patch is authorized by this review.

Verification expectation: Add a CLI or unit test where an invalid base returns nonzero under `--strict`, then rerun the targeted checker tests and the CI command shape.

Patch queue entry: not authorized.

### ROIG-02 - advisory priority: major - Review-use boundary accepts an incomplete non-claim

Location: `.agents/hooks/check_review_output_provenance.py:54`, `.agents/hooks/check_review_output_provenance.py:163`; `.agents/workflow-overlay/review-lanes.md:193`.

Evidence: `_has_review_use_boundary` requires `decision input` plus `NON_APPROVAL_RE`. That regex accepts any one nearby non-claim term from the alternation, not the full boundary required by review doctrine. A synthetic report whose boundary says only that findings are decision input and not approval returned no checker findings.

Impact: A durable review output can pass the mechanical gate while omitting validation, readiness, mandatory-remediation, or patch-authority boundaries. That weakens the overclaim guard this lane is trying to mechanize.

Minimum closure condition: The checker requires the review-use boundary to carry the complete required non-claim set, or an explicitly accepted equivalent, in the boundary text that also states findings are decision input.

Next authorized action: Advisory only; request patch authorization or CA adjudication.

Verification expectation: Add a negative test for an incomplete boundary and a positive test for the complete accepted boundary.

Patch queue entry: not authorized.

### ROIG-03 - advisory priority: major - Future-check placeholder detection is too literal

Location: `.agents/hooks/check_review_output_provenance.py:65`, `.agents/hooks/check_review_output_provenance.py:244`; `orca-harness/tests/unit/test_review_output_provenance_checker.py:146`; `.agents/workflow-overlay/delegated-review-patch.md:92`.

Evidence: `FUTURE_CHECK_RE` enumerates three exact wording families. The direct unit test covers one exact wording family. A synthetic report using a semantically equivalent saved-later checker promise returned no checker findings.

Impact: The gate can still allow future-tense provenance placeholders if a reviewer phrases the placeholder differently. That is a direct miss against the lane's report-finalization failure mode.

Minimum closure condition: The checker rejects the class of saved-later provenance/check promises intended by the overlay rule, not only the current literal examples, or the accepted rule narrows to an explicit fixed phrase list.

Next authorized action: Advisory only; request patch authorization or CA adjudication.

Verification expectation: Add at least one variant negative test that fails before the checker change and passes after it, plus keep the existing exact-phrase test.

Patch queue entry: not authorized.

### ROIG-04 - advisory priority: minor - Selftest expected-fail fixtures do not assert the expected finding codes

Location: `.agents/hooks/check_review_output_provenance.py:352`, `.agents/hooks/check_review_output_provenance.py:363`, `.agents/hooks/check_review_output_provenance.py:370`; `orca-harness/tests/fixtures/review_outputs/bad_integrity_shape.md:1`, `orca-harness/tests/fixtures/review_outputs/bad_integrity_shape.md:27`; `orca-harness/tests/unit/test_review_output_provenance_checker.py:134`.

Evidence: `selftest` reads only `fixture_expected: pass|fail` and treats any non-empty finding set as a passing expected-fail fixture. The bad integrity fixture combines multiple malformed shapes. The observed selftest output for `bad_integrity_shape.md` listed three finding codes, while the collapsed-diff class is protected by the direct unit test rather than by fixture-level selftest expectations.

Impact: The direct unit tests currently cover the concrete failure modes, but `--selftest` can remain green after losing one expected code from a multi-defect fixture as long as another defect still fails. That makes the advertised checker selftest weaker than the prompt's selftest-coverage expectation.

Minimum closure condition: Either split the multi-defect fixture into one fixture per failure class, or extend fixture metadata so `--selftest` checks expected finding codes.

Next authorized action: Advisory only; request patch authorization or CA adjudication.

Verification expectation: Add a selftest fixture or metadata case that fails if `collapsed_diff_block`, malformed fence, outside-diff, and future-placeholder detections regress independently.

Patch queue entry: not authorized.

## Explicit Non-Findings

- The target branch does add direct unit assertions for malformed fence markers, unbalanced fences, `diff --git` outside a `diff` fence, collapsed one-line diffs, the current exact future-placeholder phrase, and trailing whitespace.
- The CI workflow includes a dedicated review-output provenance and integrity step after the review-routing disposition gate and before the handoff-pointer gate.
- The delegated-review overlay and adjudication template bind a post-write review-output checker command and require an observed result rather than a later promise.
- The checker is scoped to `docs/review-outputs/**/*.md` and skips review-output README files, which matches the intended report-output surface.

## Validation Evidence Inspected

- Reran `python -B -m pytest -q -p no:cacheprovider orca-harness/tests/unit/test_review_output_provenance_checker.py`: exit 0; stdout was `................... [100%]`.
- Reran `python -B .agents/hooks/check_review_output_provenance.py --selftest`: exit 0; output listed all fixtures as PASS and ended with `SELFTEST OK`.
- Reran `python -B .agents/hooks/check_review_output_provenance.py --changed --strict`: exit 0; stdout was `review-output-provenance: no review-output files selected -- OK`.
- Reran `python -B .agents/hooks/check_review_output_provenance.py --diff origin/main --strict`: exit 0; stdout and stderr were empty, which differs from the author-reported "no review-output files selected" message.
- Reran `git diff --check`: exit 0; stdout and stderr were empty.
- Attempted full `python -B -m pytest -q -p no:cacheprovider` from `orca-harness/`: exit 1 in this sandbox after repeated `PermissionError` failures creating `_scratch` and `_test_runs`. The reported outside-sandbox full-suite pass is not reverified here.

## Residual Risks And Not-Proven Boundaries

- Same-family advisory review only; de-correlation is not cross-vendor discovery.
- The review did not patch or rerun CI on GitHub.
- The full harness suite was not observed green in this sandbox.
- The checker validates report shape and integrity only. It does not prove reviewer identity, review quality, correctness of findings, readiness, approval, or acceptance.

## Final Post-Write Checker Result

Command: `python .agents/hooks/check_review_output_provenance.py --strict docs/review-outputs/adversarial-artifact-reviews/review_output_integrity_gate_adversarial_code_review_v0.md`.

Final observed result after the report update: exit 0; stdout empty; stderr empty.
