# Creator Ledger PR439 Delegated Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: review_prompt
scope: >
  Repo-bound, de-correlated adversarial artifact review prompt for PR #439,
  covering the source-backed creator metric seed and static creator_profile_current
  export. This prompt is read-only because PR #439 is a multi-file artifact set,
  not a single delegated-review-and-patch target file.
use_when:
  - Commissioning an independent reviewer to inspect PR #439 before CA adjudication.
  - Checking whether the creator ledger/profile export preserves source backing,
    account-scoped rollup boundaries, missingness, and MGT accepted residuals.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md
  - orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_v0.json
stale_if:
  - The review target commit changes from 23dce2d4ede2418fb3e73e325b045dc61b5fa03b.
  - The base branch changes from codex/channel-neutral-creator-identity-architecture-prompt-pr412.
  - Any PR #439 target artifact listed below changes after 23dce2d4ede2418fb3e73e325b045dc61b5fa03b.
  - A later prompt-filing commit on the same branch changes target artifacts, not just this prompt.
```

## Orca Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

- authorization_basis: current owner instruction to run `workflow-delegated-review-patch` for PR #439.
- template_kind: `review`; template source `docs/prompts/templates/review/adversarial_artifact_review_v0.md` plus `.agents/workflow-overlay/delegated-review-patch.md`.
- output_mode: `review-report`.
- edit_permission: `read-only`; no patch execution is authorized by this prompt.
- review_report_destination: `docs/review-outputs/adversarial-artifact-reviews/creator_ledger_pr439_delegated_adversarial_artifact_review_v0.md`.
- target_scope: PR #439 changed files listed in this prompt.
- branch_or_commit_reference: `codex/creator-metric-source-audit` at `23dce2d4ede2418fb3e73e325b045dc61b5fa03b`; base `codex/channel-neutral-creator-identity-architecture-prompt-pr412` at `824852fceca6c80ad410bf6fea002e51bd36a05f`.
- dirty_state_allowance: expected clean worktree. If dirty, classify whether changes are in-scope before reviewing; block strict review claims if target files differ from the pinned head without explicit owner acceptance.
- source_pack: custom `creator_ledger_pr439_review_pack`.
- doctrine_change_decision: review prompt only; does not change doctrine. If the reviewer recommends doctrine change, return it as a finding, not a patch.
- isolation_decision: read-only review of existing PR branch; no new branch required by the reviewer.
- validation_gates_to_inspect: tests named in the PR, `git diff --check`, retrieval header check, map-link check, and placement advisory output. Do not rerun gates unless your runtime has repo access and doing so is cheap; report whether you inspected existing evidence, reran it, or did not run it.
- thread_operating_target_continuity: omitted; no visible active `thread_operating_target` block was supplied for this prompt.

## Delegated Review Boundary

This prompt is the MGT/SCI version of the delegated review request:

- MGT target: catch the material creator-ledger/profile failure modes that would make PR #439 unsafe to build on, while avoiding maximal review machinery.
- Accepted residuals: this is read-only, not repo-mode patch authorship; it does not prove buyer readiness, dashboard readiness, SQLite/data-lake physicalization, engagement-rate support, cross-platform identity, or no-new-seam status unless a cross-vendor controller actually runs and records the required provenance.
- SCI boundary: review only the PR #439 creator-ledger artifacts and their tests/evidence. Do not broaden into YouTube capture architecture, lake migration, dashboard design, or creator-signal product strategy beyond findings needed to judge this PR.

De-correlation is a who-constraint, not a runtime model recommendation:

- author_home_vendor_family: OpenAI / GPT-family Codex thread
- controller_vendor_family: operator_to_fill
- de_correlation_bar: `cross_vendor_discovery` only if controller vendor differs from OpenAI / GPT-family; otherwise record `same_vendor_sanity` or `self_fallback` and do not claim no-new-seam.
- reviewed_by: operator_to_fill in the durable report
- authored_by: OpenAI / GPT-family Codex thread, exact runtime version unrecorded unless the operator supplies it

Because PR #439 is a multi-file artifact set, `.agents/workflow-overlay/delegated-review-patch.md` does not authorize treating the whole PR as a single repo-mode delegated patch target. Run this as a de-correlated adversarial artifact review with advisory remediation. Do not edit files. Do not emit `patch_queue_entry`. If you believe patch execution is required, return `BLOCKED_PATCH_EXECUTION_UNBOUND` or `NEEDS_ARCHITECTURE_PASS` with the reason.

## Required Method Sequence

1. REFERENCE-LOAD these method/authority sources. Do not APPLY them yet:
   - `AGENTS.md`
   - `.agents/workflow-overlay/README.md`
   - `.agents/workflow-overlay/source-of-truth.md`
   - `.agents/workflow-overlay/source-loading.md`
   - `.agents/workflow-overlay/delegated-review-patch.md`
   - `.agents/workflow-overlay/review-lanes.md`
   - `.agents/workflow-overlay/prompt-orchestration.md`
   - `.agents/workflow-overlay/validation-gates.md`
   - `docs/decisions/orca_mini_god_tier_doctrine_v0.md`
   - `workflow-deep-thinking`
   - `workflow-adversarial-artifact-review`
2. SOURCE-LOAD the target source pack below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`. If incomplete, name missing sources and whether findings are blocked or advisory-only.
4. APPLY `workflow-deep-thinking` to frame failure modes and decision criteria.
5. APPLY `workflow-adversarial-artifact-review` to produce findings.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot be applied after source readiness, return a blocked or advisory-only result. Do not emit formal validation, readiness, approval, mandatory remediation, or patch authority claims.

## Review Target

PR: https://github.com/eric-foo/orca/pull/439

Base: `codex/channel-neutral-creator-identity-architecture-prompt-pr412`

Review target branch: `codex/creator-metric-source-audit`

Pinned review target commit: `23dce2d4ede2418fb3e73e325b045dc61b5fa03b`

Note: this prompt artifact may be filed in a later commit on the same branch. Review the target artifact set at the pinned review target commit unless the CA explicitly updates this prompt.

Changed files:

- `docs/review-inputs/creator_metric_source_audit_v0.md`
- `docs/review-inputs/creator_metric_source_live_probe_youtube_v0.json`
- `orca-harness/tests/unit/test_creator_profile_current_static_view.py`
- `orca-harness/tests/unit/test_youtube_creator_metric_seed.py`
- `orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_v0.json`
- `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_seed_v0.json`
- `orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md`

## Review Purpose

Decide whether PR #439 is safe for the CA to adjudicate as the current creator-ledger/profile base:

- source-backed YouTube view-count metric observations;
- account-scoped admitted-pool rollups;
- static `creator_profile_current` export over identity + metrics;
- explicit missingness for engagement, likes, total comments, audience, and cross-platform rollups;
- tests that rederive enough of the artifacts to catch self-certification or drift.

Fitness reference:

- `orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md`
- `orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md`
- `docs/decisions/orca_mini_god_tier_doctrine_v0.md`

## Source Pack

Read the PR target files plus these decisive sources:

- `orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_v0.json`
- `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_observation_ledger_v0.json`
- `docs/review-inputs/youtube_shorts_fragrance_retained_recapture_v0.json`
- `docs/review-inputs/youtube_shorts_fragrance_replacement_capture_v0.json`
- `docs/review-inputs/youtube_shorts_fragrance_tone_expansion30_capture_v0.json`
- `docs/review-inputs/youtube_shorts_fragrance_tone_expansion100_capture_v0.json`
- `docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.json`
- `docs/review-inputs/creator_metric_source_audit_v0.md`
- `docs/review-inputs/creator_metric_source_live_probe_youtube_v0.json`

Available but do not bulk-load unless a finding depends on them:

- all review outputs;
- all lake/data-lake contracts;
- all YouTube capture implementation files beyond the live-probe receipt;
- all audience/ideal-audience artifacts, except to verify that PR #439 correctly leaves audience unjoined.

## Review Checks

Attack these failure modes first:

1. Source-backedness: the 196 metric observations and 30 rollups must rederive from the named source captures and ledgers. Source hashes must not be self-certifying if the source can cheaply be re-read.
2. Claim boundary: no artifact may imply channel-wide creator influence, engagement rate, buyer proof, dashboard readiness, public person identity, or cross-platform rollup support.
3. Missingness: unavailable likes/comments/subscribers/engagement/audience fields must remain explicit missingness, not observed zeroes, omitted caveats, or operator-summary overclaim.
4. Identity boundary: `creator_profile_current` rows must remain `platform_account` subjects until promoted public-handle linkage exists. Candidate or absent linkage must not create `creator_record` rollups.
5. Static export risk: the profile export must not become a second source of truth. It should point back to identity and metric sibling records and carry freshness/limitations.
6. MGT residuals: accepted residuals must be named, material, and acceptable for this step. Flag any silent residual that should be explicit before the PR is built on.
7. SCI boundary: flag any excess scope, speculative infrastructure, or avoidable lock-in introduced by the PR.
8. Test strength: tests must catch the important drift classes for this static stage without pretending to validate future lake/SQLite/dashboard behavior.
9. Live-run interpretation: the 3-video live probe must be framed as route sanity only, not as the source of the 200-row seed or proof of like/comment availability.

## Output Contract

Write the durable review report to:

`docs/review-outputs/adversarial-artifact-reviews/creator_ledger_pr439_delegated_adversarial_artifact_review_v0.md`

The report must include:

- retrieval header;
- `reviewed_by` and `authored_by` provenance fields, with `unrecorded` allowed when not supplied;
- `de_correlation_bar`: `cross_vendor_discovery`, `same_vendor_sanity`, or `self_fallback`;
- one compact `review_summary` YAML block using `.agents/workflow-overlay/communication-style.md`;
- findings first, ordered by `critical`, `major`, then `minor`;
- for each finding: severity, location, issue, evidence, impact, `minimum_closure_condition`, `next_authorized_action`, and advisory remediation direction;
- residual-risk note;
- explicit validation evidence inspected or not run.

Return only the compact `review_summary` YAML in chat after the report is written. If the report cannot be written, return the failed `review_summary` shape with `review_location: chat_only_current_thread` and `recommendation: blocked`.

Review-use boundary: findings and non-findings are decision input only. They are not approval, validation, product proof, mandatory remediation, patch authority, or readiness until the CA separately adjudicates them.
