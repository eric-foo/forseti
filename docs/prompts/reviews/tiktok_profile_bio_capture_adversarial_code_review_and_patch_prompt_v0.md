# Delegated adversarial review and patch — TikTok profile bio capture

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial code review-and-patch prompt
scope: >
  Cross-vendor review and bounded patch commission for TikTok onboarding
  profile-bio capture.
use_when:
  - Reproducing or auditing the completed profile-bio review commission.
authority_boundary: retrieval_only
output_mode: review-report
```

## Retrieval and authority

- `retrieval_mode`: repository worktree
- `target_kind`: `delegated_code_review_and_patch`
- `access`: `repo`
- `receiver_to_bind`: preparation only; the executing reviewer must bind the receiver before source loading
- `project_authority`: `AGENTS.md` and `.agents/workflow-overlay/`
- `review_method`: `workflow-code-review`
- `authored_by`: `openai_gpt5_codex`
- `required_de_correlation`: genuinely different model family/vendor from the author

This is a lane-scoped, operator-couriered review-and-patch commission. The prompt author is not the reviewer. Do not begin source review until every receiver-binding and target-state condition below is proved from the live target worktree.

## Forseti Prompt Preflight

1. Read the repository-root `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md` and the overlay sources it routes for delegated code review, validation, sensitive material, lifecycle boundaries, and review provenance.
3. Bind the receiver before source loading: prove cross-vendor/model-family de-correlation from `openai_gpt5_codex`, prove direct write capability in the exact target worktree using a removable self-owned probe, and prove there is no concurrent writer.
4. Fresh-read the target branch, HEAD, dirty set, and exact target-file hashes. Stop on any mismatch.
5. Load only the named target files plus the minimum owning sources and tests needed to adjudicate them.
6. Apply the named review method. Findings must be evidence-backed, severity-ranked, and tied to the commissioned behavior.
7. Patch only confirmed defects and only within the authorized target files. Preserve real failure visibility.
8. Run the named validation gates after any patch. Record real commands, exit codes, and residuals; never infer success.
9. Write the durable review report at the exact output path and run the repository provenance gate against it.
10. Do not commit, push, open or modify a PR, merge, stash, reset, clean, remove a worktree, or perform a live TikTok capture.

## Exact target state

- `target_worktree`: `C:\tmp\orca-tt-profile-bio-20260715`
- `target_branch`: `codex/tiktok-onboarding-profile-bio`
- `target_head`: `d25ba56bd3df3b184d34fa15e12b2803eda0241d`
- `expected_pre_review_dirty_paths`:
  - `forseti-harness/source_capture/tiktok/creator_onboarding.py`
  - `forseti-harness/tests/unit/test_tiktok_creator_onboarding.py`
  - `docs/prompts/reviews/tiktok_profile_bio_capture_adversarial_code_review_and_patch_prompt_v0.md`
- `commissioned_target_hashes_before_prompt_creation`:
  - `forseti-harness/source_capture/tiktok/creator_onboarding.py`: `6d720de8b25ce960279543f78d91307608283e7544d1f75cb5cb236a16d02337`
  - `forseti-harness/tests/unit/test_tiktok_creator_onboarding.py`: `9eb35a09a71b16a29e9318f37b4b40ef825464721328a9832deae5d8dc2defcd`

The prompt file is an authorized pre-existing dirty path but is not patch authority. Compute and report its live hash during receiver binding. If branch, HEAD, the two commissioned target hashes, or the exact three-path dirty set differs, stop and report `BLOCKED_TARGET_STATE_MISMATCH`. If another writer is present, stop and report `BLOCKED_CONCURRENT_WRITER`. If de-correlation or direct write capability cannot be proved, stop with the corresponding explicit blocker before source loading.

## Bound outcome

Review and, where a confirmed defect fits the bounded authority, patch the TikTok creator-onboarding change so a normal onboarding run captures the root creator's exact public profile bio as durable profile evidence without regressing existing suggested-account, external-link, blocker-triage, or artifact-admission behavior.

This change supplies evidence. It must not infer creator location, primary audience geography, US-market priority, Registry rank, or eligibility.

## Patch authority

You may patch only:

- `forseti-harness/source_capture/tiktok/creator_onboarding.py`
- `forseti-harness/tests/unit/test_tiktok_creator_onboarding.py`

You must write the review report at:

- `docs/review-outputs/tiktok_profile_bio_capture_adversarial_code_review_v0.md`

No other repository file may be created, edited, deleted, renamed, staged, or restored. The report is required output, not implementation patch authority.

## Required fitness criteria

1. The primary route captures the root profile's public bio through `[data-e2e="user-bio"]`.
2. The fallback route captures the same evidence when it owns the usable page state.
3. Primary/fallback merging preserves an actually observed primary bio but does not overwrite real fallback evidence with primary absence.
4. Text is trimmed only at its outer boundary; internal line breaks, emoji, punctuation, handles, and public contact text remain intact.
5. The receipt distinguishes `captured`, `visible_empty`, `not_visible`, and `failed` without converting extraction failure into a false empty or absent observation.
6. Bio extraction failure cannot discard or falsify existing suggested-account, overlay, comment, external-link, cadence, or blocker-triage evidence.
7. Existing suggested-account and external-link semantics remain unchanged.
8. The normal runner persists bio evidence to `tiktok_suggested_accounts_attempt.json`, and the existing Bronze boundary carries it to `raw/04_tiktok_suggested_accounts_attempt.json` without top-level packet duplication.
9. No acquisition-layer code infers geography, audience, US-market fit, Registry priority, or eligibility from the bio.
10. The patch does not open candidate profiles, search for an absent Linktree, mutate a TikTok account, or perform a live capture.
11. Public bio content follows repository sensitive-material rules: public contact text may remain source evidence; authentication/session material must never enter artifacts or the report.
12. Tests exercise load-bearing primary, fallback, merge, status, exact-text, failure-visibility, runner-file, and Bronze-boundary behavior to the extent available.

## Required adversarial attacks

Explicitly resolve:

- Could the selector capture a bio from a modal, candidate card, stale SPA subtree, or hidden/non-root node?
- Could primary/fallback merge order erase, misattribute, or manufacture bio evidence?
- Does `visible_empty` require an actually detected root bio element rather than a hidden/stale selector hit?
- Can a JS exception discard the whole DOM extract or turn failure into `not_visible`?
- Are outer whitespace, internal newlines, emoji, and public email/contact text preserved appropriately?
- Can auth tokens, cookies, session identifiers, or non-public sensitive material leak through fields, fixtures, diagnostics, or report?
- Does the normal runner write the evidence-bearing receipt Bronze admits, or do tests prove only an isolated helper?
- Do names, comments, tests, or branches silently encode UK/US/audience inference that belongs downstream?
- Are existing suggested-account and external-link fields changed by fallback merging?

If a defect requires architecture, a new runtime, broader file authority, live capture, or a product decision, report it with `NEEDS_ARCHITECTURE_PASS` or the precise blocker; do not stretch authority.

## Validation gates

Run from the exact target worktree and follow owning repository commands. At minimum record:

1. `git diff --check`
2. the focused TikTok creator-onboarding unit test file
3. all repository TikTok tests matching the established `test_tiktok_*.py` route
4. if source or tests are patched, the full harness suite required by the Forseti overlay
5. the repository review-report provenance gate against the durable report

Author evidence is context, not reviewer validation:

- focused creator-onboarding tests: pass (49 tests/dots, 100%)
- all TikTok tests: pass (100%; two pre-existing datetime deprecation warnings)
- earlier full harness before the current main fast-forward: pass (438.2s)
- current post-fast-forward full harness: not rerun

If no gate executes the relevant browser JavaScript, state that limitation plainly.

## Durable report contract

The report must include:

- retrieval/target header with branch, HEAD, dirty set, and fresh hashes
- `reviewed_by`, `authored_by`, reviewer vendor/model family, and observed de-correlation proof
- receiver-binding proof, direct-write probe removal, and concurrent-writer check
- scope and sources loaded
- severity-ranked findings with evidence and disposition
- patches applied, with reviewer-only unified diff or unambiguous hunk accounting
- validation commands, exit codes, counts, warnings, and failures
- residual risks and untested paths
- a use-boundary saying the review does not establish live-site correctness, creator geography, primary audience geography, US-market fit, or Registry priority/eligibility
- verdict: `no_issues_found`, `issues_found`, `blocked`, or `NEEDS_ARCHITECTURE_PASS`
- lifecycle statement confirming no commit/push/PR/merge/stash/reset/cleanup/live capture
- next action returning the result to the commissioning Codex lane for adjudication

Reviewer-authored hunks are not independently reviewed; return them to the commissioning lane as a named residual.

## Stop conditions

Stop before source loading or mutation if de-correlation, direct write access, no-concurrent-writer state, exact branch/HEAD/hashes/dirty set, or repository authority cannot be proved. After source loading, stop mutation if a necessary fix exceeds the two-file authority, requires live account interaction, or would add geography/audience/ranking policy to acquisition.
