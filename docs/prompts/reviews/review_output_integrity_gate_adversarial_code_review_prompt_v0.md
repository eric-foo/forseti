# Review Output Integrity Gate Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed route-out prompt for de-correlated adversarial implementation/code
  review of the review-output provenance and integrity gate lane.
use_when:
  - Commissioning an independent reviewer to inspect the review-output integrity checker, tests, CI wiring, and delegated-review prompt/overlay bindings.
  - Checking the prompt source, target branch, output binding, and de-correlation receipt for this review.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/source-loading.md
implementation_under_review: working_tree_diff_from_946e8e63_on_codex/review-output-integrity-gate
prompt_carrier_note: >
  This prompt is filed in the same lane as the implementation it reviews. The
  review target is the lane diff against 946e8e63, excluding this prompt file
  unless a later carrier commit changes target files after this prompt is filed.
stale_if:
  - Any named implementation target file changes after this prompt is filed and before review.
  - The review-output destination already exists and the operator has not authorized a new version.
  - The receiving actor cannot inspect the named worktree or branch in place.
```

## Orca Prompt Preflight

- Output mode: file-write review prompt; receiver output mode is `review-report` to `docs/review-outputs/adversarial-artifact-reviews/review_output_integrity_gate_adversarial_code_review_v0.md`.
- Template kind: review. Orca-local `repo-code-review` template kind is unbound, so this uses the prompt-orchestrator review frame plus Orca overlay bindings.
- Edit permission, targets, branch: reviewer is read-only. Target worktree is `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\review-output-integrity-gate`, branch `codex/review-output-integrity-gate`, base `946e8e63`. Dirty state allowed only for the lane diff and this prompt artifact.
- Reviews: findings-first. This is advisory implementation/code review unless a later Orca binding grants formal implementation-review authority. Do not emit formal PASS, readiness, mandatory remediation, or patch queue.
- Doctrine change: this lane changes workflow/review-output gate behavior by making review-output integrity mechanically checkable and binding a post-write closeout gate. Treat the propagation receipt or blocker as part of the target.
- Destinations: this prompt is the input artifact; the receiver writes the full report to `docs/review-outputs/adversarial-artifact-reviews/review_output_integrity_gate_adversarial_code_review_v0.md`.

## Commission

Run an adversarial implementation/code review of the review-output integrity gate lane. The implementation under review is the current branch `codex/review-output-integrity-gate` against base `946e8e63`.

This prompt was prepared after a fused implementation closeout where adversarial review was recommended because the lane changes reusable hook/checker behavior, CI gate behavior, review-output closeout doctrine, and prompt/adjudication template behavior. No delegated patch authority is commissioned in this prompt: route it through read-only implementation/code review. The reviewer must not patch source files.

Review purpose:

1. Attack whether `.agents/hooks/check_review_output_provenance.py` now catches the concrete failure modes without overblocking valid review reports: malformed fences such as ```diff#, unbalanced fences, `diff --git` outside a `diff` fence, collapsed one-line diffs, future-tense provenance placeholders, and trailing whitespace.
2. Attack whether `--diff <base>` is the right CI selector and whether the CI wiring actually catches changed review-output artifacts in pull requests without creating a fake green path.
3. Attack whether the tests and bad fixture cover the failure modes that caused the prior lane failure, including direct unit assertions and checker selftest coverage.
4. Attack whether the overlay and adjudication template binding makes the process seamless for future agents without overstating validation, review quality, readiness, or approval.
5. Attack whether this doctrine-changing lane carries sufficient propagation evidence or a visible blocker, and whether any downstream surface still routes future agents by stale review-output closeout doctrine.

## Actor And De-Correlation Receipt

- author_home_model_family: OpenAI / GPT-family Codex, recorded from the authoring lane.
- controller_model_family: `operator_to_fill`; must be a different upstream vendor / model lineage from OpenAI to claim cross-vendor discovery.
- current_receiving_actor_role: controller.
- dispatch_mode: external-controller-courier.
- de_correlation_status: `operator_to_fill`; if controller model family is missing or same-vendor, return advisory findings only and do not claim cross-vendor discovery or no-new-seam.
- no runtime model recommendation is made by this prompt.

## Source-Gated Method Contract

1. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-code-review` if available in your environment. Do not APPLY them yet.
2. Read the required Orca authority and target sources below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, conflicts, unavailable tools, and any target-file drift.
4. Only after source readiness, APPLY deep-thinking to frame material failure modes, then APPLY workflow-code-review to produce findings-first implementation/code review.
5. If `workflow-code-review` is unavailable, use findings-first advisory code-review semantics from this prompt, but mark strict review claims `NOT_CLAIMED`.

## Required Reads

Read these authority and boundary files first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/source-of-truth.md`

Then read the review target:

- `.agents/hooks/check_review_output_provenance.py`
- `orca-harness/tests/unit/test_review_output_provenance_checker.py`
- `orca-harness/tests/fixtures/review_outputs/bad_integrity_shape.md`
- `.github/workflows/ci.yml`
- `.agents/hooks/README.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `docs/prompts/templates/review/delegated_review_return_adjudication_v0.md`

Read adjacent checker/test context only as needed; do not widen into unrelated hooks, prompt doctrine, or review-lane redesign.

## Target Diff And Dirty-State Allowance

Review this implementation diff shape from the target worktree:

```powershell
git status --short
git diff 946e8e63 -- .agents/hooks/README.md .agents/hooks/check_review_output_provenance.py .agents/workflow-overlay/delegated-review-patch.md .github/workflows/ci.yml docs/prompts/templates/review/delegated_review_return_adjudication_v0.md orca-harness/tests/unit/test_review_output_provenance_checker.py
```

Also read the untracked target fixture directly until it is committed:

```text
orca-harness/tests/fixtures/review_outputs/bad_integrity_shape.md
```

Do not treat this prompt file as part of the implementation target unless a later carrier commit changes implementation target files after this prompt is filed.

## Validation Evidence To Inspect

The author reported these observed checks from the target worktree. Treat them as claims to verify against command output or rerun where appropriate:

- `python -B -m pytest -q -p no:cacheprovider orca-harness/tests/unit/test_review_output_provenance_checker.py` exited 0 and printed `................... [100%]`.
- `python -B .agents/hooks/check_review_output_provenance.py --selftest` exited 0 and listed `bad_integrity_shape.md` as expected fail, then `SELFTEST OK`.
- `python -B .agents/hooks/check_review_output_provenance.py --changed --strict` exited 0 with no output.
- `python -B .agents/hooks/check_review_output_provenance.py --diff origin/main --strict` exited 0 and printed `review-output-provenance: no review-output files selected -- OK`.
- `git diff --check` exited 0 with only Git LF-to-CRLF warnings.
- Full `python -B -m pytest -q -p no:cacheprovider` from `orca-harness/` failed in sandbox on `_scratch` and `_test_runs` permission errors, then exited 0 outside the sandbox; warnings were deprecation and unknown-mark warnings only.

## Output Contract

Write the durable review report to:

```text
docs/review-outputs/adversarial-artifact-reviews/review_output_integrity_gate_adversarial_code_review_v0.md
```

The report must include:

- retrieval header with `reviewed_by`, `authored_by`, and `review_use_boundary` fields;
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`;
- findings first, ordered by severity, with file/line citations;
- explicit non-findings for material surfaces inspected;
- minimum closure condition and next authorized action for each actionable finding;
- residual risks and not-proven boundaries;
- whether the author-reported validation evidence was rerun, accepted as reported, or not checked;
- no formal PASS, readiness, approval, mandatory remediation, runtime model recommendation, or patch queue.

After writing the report, run:

```powershell
python .agents/hooks/check_review_output_provenance.py --strict docs/review-outputs/adversarial-artifact-reviews/review_output_integrity_gate_adversarial_code_review_v0.md
```

If the report changes after that command, rerun it and record only the final observed result.