# Delegated Adversarial Code Review-And-Patch Prompt: Reddit Batch Quality Summary

## Commission

You are the de-correlated controller for a bounded Orca delegated review-and-patch pass.

This prompt exists because the home model authored a small foundation slice after `/fused` and then identified a recommended review checkpoint that should have been triggered before closeout. The specific risk is claim inflation in a new quality-summary runner, especially the `usable_for_downstream` label.

## Actor / Model-Family Receipt

- author_home_model_family: OpenAI/Codex family
- current_receiving_actor_role: controller
- required_controller_family: a different vendor or model family from OpenAI/Codex
- de_correlation_rule: This is a who-constraint, not a model recommendation.
- blocked condition: if you are OpenAI-family, Codex, or otherwise not de-correlated from the author/home family, return `BLOCKED_CONTROLLER_NOT_DECORRELATED` and stop.

Do not include any runtime model recommendation in your output.

## Worktree And Preflight

Worktree:

```text
C:\Users\vmon7\Desktop\projects\orca
```

Before review, record:

- current branch
- current HEAD
- `git status --short` for the editable and read-only files below
- whether all editable targets exist

Dirty state is allowed. This worktree has many unrelated dirty/untracked files; do not revert or touch unrelated work.

## Required Authority Reads

Read these first:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/decision-routing.md`
4. `.agents/workflow-overlay/prompt-orchestration.md`
5. `.agents/workflow-overlay/review-lanes.md`
6. `.agents/workflow-overlay/delegated-review-patch.md`

Run the Cynefin router before review. This should remain patch-level unless the implementation creates a design-level overclaim that cannot be fixed inside the editable scope.

## Source-Gated Method Sequence

REFERENCE-LOAD these methods before source loading. Do not APPLY them yet:

- `workflow-deep-thinking`
- `workflow-code-review`

Then SOURCE-LOAD the editable targets and read-only context below. Declare one:

- `SOURCE_CONTEXT_READY`
- `SOURCE_CONTEXT_INCOMPLETE`, with missing files and impact

Only after that declaration, APPLY deep-thinking to frame failure modes, then APPLY `workflow-code-review`.

If `workflow-code-review` is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not patch.

## Editable Scope

You may patch only:

- `orca-harness/runners/run_reddit_batch_quality_summary.py`
- `orca-harness/tests/unit/test_reddit_batch_quality_summary.py`

Everything else is read-only. If the right fix requires another file, flag it and do not edit it.

## Read-Only Context

Read as needed:

- `orca-harness/runners/run_reddit_old_http_batch.py`
- `orca-harness/tests/unit/test_reddit_old_http_batch.py`
- `orca-harness/source_capture/reddit_consolidation/consolidator.py`
- `orca-harness/source_capture/reddit_consolidation/parser.py`
- `orca-harness/tests/unit/test_reddit_consolidation.py`
- `orca-harness/tests/contract/test_reddit_consolidation_contract.py`
- `orca-harness/tests/unit/test_source_capture_direct_http.py`
- `orca-harness/tests/contract/test_source_capture_direct_http_contract.py`

## Review Target

The new foundation slice adds a local post-batch quality summarizer:

- It reads an existing `reddit_old_http_batch` `batch_summary.json`.
- It reads already-preserved packet HTTP metadata.
- It reads already-derived `reddit_thread_consolidation.json`.
- It writes `reddit_batch_quality_summary.json` and `reddit_batch_quality_summary_receipt.md`.
- It should not fetch Reddit, retry, crawl, monitor, use proxy/browser/CloakBrowser, use `.json`, or perform source discovery.

The implemented user-facing statuses are:

- `usable_for_downstream: yes`
- `usable_for_downstream: needs_review`
- `usable_for_downstream: no`

## Highest-Risk Review Questions

Prioritize blocker/major findings over style.

1. Does `usable_for_downstream` overclaim validation, source completeness, readiness, or buyer-proof/judgment usefulness?
2. Are `yes`, `needs_review`, and `no` boundaries honest and cheaply checkable from local artifacts only?
3. Are missing packet metadata, missing consolidation JSON, non-2xx HTTP, failed capture, failed consolidation, and reconciliation mismatch loud enough?
4. Does the runner avoid hidden live capture, retry, crawl, source discovery, browser/proxy/CloakBrowser, `.json`, scheduler, storage, ECR, Cleaning, or Judgment behavior?
5. Are tests sufficient to prevent fake-pass quality summaries and claim inflation?
6. Does the runner preserve packet-first cache behavior, so parser/quality iteration can happen without re-fetching Reddit?

## Patch Authority

If you find blocker or major issues that can be fixed inside the editable scope, patch them directly.

If the issue is design-level, requires off-scope files, or changes the lane boundary, stop patching and return:

```text
NEEDS_ARCHITECTURE_PASS
```

If you made a partial patch before detecting that, revert your own partial patch and return findings only.

Do not stage, commit, push, install dependencies, run live Reddit/network capture, or use browser/proxy tools.

## Validation

Run local tests only:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider -q orca-harness\tests\unit\test_reddit_batch_quality_summary.py orca-harness\tests\unit\test_reddit_old_http_batch.py orca-harness\tests\unit\test_reddit_consolidation.py orca-harness\tests\unit\test_source_capture_direct_http.py orca-harness\tests\contract\test_source_capture_direct_http_contract.py orca-harness\tests\contract\test_reddit_consolidation_contract.py
```

If you cannot run this, state why and do not imply validation passed.

Known pre-review validation from the author lane:

```text
....................................                                     [100%]
```

Treat that as orientation only. Your own observed validation is the review evidence.

## Output Contract

Return findings first, ordered by severity.

Include:

1. De-correlation receipt.
2. Cynefin routing result.
3. Source readiness declaration.
4. Findings with file/line references.
5. Patch summary, if patched.
6. Unified diff, if patched.
7. Validation command and observed result, or not-run reason.
8. Residual risk.
9. Verdict, exactly one:
   - `NO_BLOCKERS_FOUND`
   - `PATCHED_FOR_CA_ADJUDICATION`
   - `NEEDS_ARCHITECTURE_PASS`
   - `BLOCKED_CONTROLLER_NOT_DECORRELATED`
   - `BLOCKED_REVIEW_LANE_UNAVAILABLE`
   - `BLOCKED_TARGET_MISSING`
   - `SOURCE_CONTEXT_INCOMPLETE`

Final boundary: your diff, citations, and verdict are claims for Chief Architect adjudication, not accepted truth. Do not state that the patch is final, approved, validated for production, staged, committed, or kept.
