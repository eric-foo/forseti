# TikTok Supervised Onboarding Runner — Delegated Adversarial Code Review-and-Patch Commission v0

~~~yaml
retrieval_header_version: 1
artifact_role: delegated adversarial code review-and-patch commission
scope: >
  Different-vendor review and bounded patch pass for the supervised TikTok
  creator-onboarding runner, its one-context browser lease, response-count stop,
  range-override selector contract, lake declaration, and focused tests.
use_when:
  - Reviewing branch codex/tiktok-supervised-onboarding-runner before merge.
authority_boundary: retrieval_only
~~~

## Forseti Prompt Preflight

~~~text
forseti_prompt_preflight:
  output_mode: review-report
  repository: C:\Users\vmon7\Desktop\projects\orca
  commissioned_branch: codex/tiktok-supervised-onboarding-runner
  commissioned_diff: origin/main...HEAD, observed and recorded by reviewer at start
  author_model_family: OpenAI / Codex
  reviewer_requirement: different vendor and model family; Anthropic Claude is suitable
  operating_mode: repo-visible delegated_code_review_and_patch
  source_loading: confirm, do not trust; read AGENTS.md and named overlay/source files before strict claims
  edit_permission: patch only confirmed defects inside the named target surface
  lifecycle_permission: do not commit, push, merge, open/update PRs, or run live TikTok/browser/data-lake production capture
  required_methods: workflow-deep-thinking, then workflow-code-review
  durable_output: docs/review-outputs/tiktok_supervised_onboarding_runner_delegated_adversarial_code_review_v0.md
  stop_if: wrong branch, dirty pre-existing target files, unavailable source, same-family reviewer, or scope expansion required
~~~

## Commission

Act as the de-correlated delegated controller. First verify and report:

- repository path, current branch, observed HEAD, origin/main...HEAD range, and clean/dirty state;
- that the reviewer is not OpenAI/Codex-family;
- every target file in the diff and any pre-existing dirty overlap;
- SOURCE_CONTEXT_READY only after the required sources and full diff are read.

Read completely before findings:

- AGENTS.md
- .agents/workflow-overlay/README.md
- .agents/workflow-overlay/source-loading.md
- .agents/workflow-overlay/decision-routing.md
- .agents/workflow-overlay/review-lanes.md
- .agents/workflow-overlay/delegated-review-patch.md
- .agents/workflow-overlay/validation-gates.md
- forseti-harness/source_capture/adapters/browser_snapshot.py
- forseti-harness/source_capture/tiktok/creator_onboarding.py
- forseti-harness/source_capture/tiktok/grid_video_selection.py
- forseti-harness/source_capture/tiktok/live_batch_probe.py
- forseti-harness/source_capture/session_profiles.py
- forseti-harness/runners/run_source_capture_tiktok_creator_onboarding.py
- forseti-harness/runners/run_source_capture_tiktok_grid_video_selection.py
- forseti-harness/data_lake/inventory.py
- all changed unit/contract tests and forseti-harness/data_lake/lake_touchpoint_inventory_v0.json
- the complete origin/main...HEAD diff.

Then apply workflow-deep-thinking followed by workflow-code-review.

## Review Target And Fitness Contract

The intended bounded behavior is:

1. A cold agent defaults to logical session alias chowdakr_sg_tiktok; invalid or missing alias/auth state fails closed and never downgrades to logged out.
2. One supervised run owns one CloakBrowser launch and one context across:
   suggested attempt -> grid collection -> window freeze -> selection receipt write -> sequential selected-video deep capture -> one terminal close.
3. CAPTCHA/security markers pause for owner handoff in the still-open browser; automation does not solve the challenge.
4. Suggested-account observation is mandatory as an attempt and records captured, blocked_or_empty, or failed; it does not claim exhaustiveness or mutate the discovery graph.
5. Grid collection defaults to 32 unique source-visible videos and stops as soon as preserved profile-item responses provide enough complete playCount/diggCount rows, subject to a hard scroll cap.
6. The frozen window preserves source-visible grid order and fails before selection when N ordered rows with complete metrics are unavailable.
7. Selection defaults to 25% (8 of 32), permits recorded fraction/window overrides, and preserves the already accepted reach-first rule: an outside candidate may replace an original reach incumbent only at at least 80% of its views and at least 20% higher like rate.
8. The old promotion/promoted vocabulary is absent from the current selection schema and code surface; the concept is range_override.
9. The frozen window and selection receipt are durably written before any selected-video deep capture starts.
10. Selected videos deep-capture sequentially in review-priority order through the same injected engine. Partial failures stay visible and return non-success.
11. Browser/context close is terminal, single, and idempotent; close failure cannot become a success receipt.
12. Optional packet admission is explicit-root-only and its bronze-writer/identity-binding/inventory declarations remain truthful.
13. No standing crawler, parallel browser fan-out, registry mutation, follow/unfollow, private enrichment, paid/organic inference, CAPTCHA solving, or live run belongs in this patch.

## Adversarial Questions

At minimum, challenge:

- Can the session engine accidentally launch twice, create a second context, retain pages, accept changed storage/proxy/viewport settings, or close early on any success/failure path?
- Does calling response.text() during repeated stop checks cause response-body races, repeated side effects, hidden truncation, or false early/late stops?
- Can the response predicate count unrelated repost/recommendation items or author-mismatched rows?
- Can post-scroll DOM order diverge from the response items such that the wrong 32 are frozen, pinned items are mishandled, or complete metrics are silently substituted?
- Can suggested-account blocked_or_empty fake a skipped attempt, or can the View-all action click an unrelated control?
- Can a fraction edge case, float conversion, zero-like incumbent, competing challenger, or renamed field change the accepted selection behavior?
- Is every artifact ordering claim backed by an actual write before the deep-capture call?
- Do exception, partial-capture, admission, and browser-close paths preserve the most important failure and write an honest terminal receipt?
- Does any receipt leak cookie/storage-state/proxy/session secrets or raw sensitive TikTok query material?
- Is the runner honestly classified as explicit-root-only and identity-unbound where end-to-end served-author proof is absent?
- Do tests exercise the same checks they claim, or can injected fakes pass while live wiring is broken?
- Is any changed line unnecessary to the owner-requested bounded runner?

## Patch Authority

You may patch confirmed defects only within the files changed by origin/main...HEAD, plus the required review report. Keep the smallest complete correction. Do not redesign the broader browser framework, build a standing scanner, add registry mutation, weaken failure visibility, alter unrelated lake contracts, or run live capture.

For every behavior defect patched:

- demonstrate same-check red/green evidence when practical;
- rerun the closest focused tests;
- rerun:
  - python -m pytest -q tests/unit/test_tiktok_grid_video_selection.py tests/unit/test_tiktok_creator_onboarding.py tests/unit/test_source_capture_browser_snapshot.py tests/unit/test_tiktok_live_batch_probe.py
  - python -m pytest -q tests/contract
  - git diff --check
  - python .agents/hooks/check_review_routing.py --strict from the repository root, if the current uncommitted review state permits it;
- do not claim tests that were not observed.

Leave all review patches and the report uncommitted. Do not push or touch the PR.

## Required Report

Write:

docs/review-outputs/tiktok_supervised_onboarding_runner_delegated_adversarial_code_review_v0.md

Include:

- preflight and de-correlation evidence;
- SOURCE_CONTEXT_READY;
- findings ordered blocker/major/minor with file/line evidence, impact, confidence, and minimum closure;
- considered-and-defended items;
- exact patch summary and unified diff scope;
- validation commands, exits, and observed results;
- reviewer verdict;
- residual risks and explicit non-claims;
- review_use_boundary stating that findings and patches are decision input for home-model adjudication;
- courier instruction to return the report, findings, patches, verdict, and residuals to the commissioning Chief Architect.

If no defect is confirmed, say so explicitly and do not manufacture a patch.
