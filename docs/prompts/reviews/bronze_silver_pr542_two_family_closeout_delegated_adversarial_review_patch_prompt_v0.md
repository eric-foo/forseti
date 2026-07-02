# Bronze/Silver PR #542 Delegated Adversarial Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Commissions a de-correlated adversarial review-and-patch pass for PR #542's
  Bronze/Silver two-family consumer-proof closeout record and repo-map pointer.
use_when:
  - Couriering PR #542 to an independent controller before using the closeout as the basis for full-GT upgrade planning.
  - Checking whether the two-family proof closeout overclaims, hides residuals, or prematurely stops source-family proof expansion.
  - Requesting a bounded patch only inside the named PR #542 closeout target files.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/bronze_silver_two_family_consumer_proof_closeout_v0.md
  - docs/workflows/orca_repo_map_v0.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
branch_or_commit: codex/bronze-silver-two-family-closeout target closeout commit a778542626fde6bade49b57b2a0950d798cb8fc7
stale_if:
  - PR #542 head moves after this prompt without the receiver refreshing PR state.
  - The closeout artifact or repo-map row is materially rewritten before review.
  - A later prompt supersedes this PR #542 delegated review commission.
```

## Objective

Run a de-correlated adversarial review-and-patch pass on PR #542 before the home
model uses the closeout as the basis for the Bronze full-GT upgrade plan.

Intended decision for the home model after your return:

- `accept`: PR #542 is safe to use as the planning base as written.
- `accept_with_friction`: PR #542 is safe to use, but named residuals or optional
  hardening should travel into the next planning turn.
- `patch_before_acceptance`: you found and patched a bounded target-file defect;
  the home model must adjudicate the diff before keep.
- `NEEDS_ARCHITECTURE_PASS`: the closeout's sequencing decision is wrong or too
  under-sourced to patch locally.
- `reject`: PR #542 should not be used as a planning base without rework.

## Why This Review Happens First

The closeout is small, but it makes a material sequencing call: stop default
source-family proof expansion and move the next material lane into Bronze
full-GT upgrade scoping. That call should not be carried into a full-GT plan on
self-review alone.

## Orca Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S0/S1 plus PR #542 target files, PR metadata, and Data Lake authority docs named by the target artifact
  edit_permission: patch-only inside the two named target files; all other paths read-only / flag-only
  target_scope: delegated adversarial review-and-patch prompt for PR #542 closeout artifacts
  dirty_state_checked: yes; prompt authored on clean branch before this prompt file is added
  blocked_if_missing: repo access to the PR #542 branch or target commit; overlay review rules; target closeout artifact; repo map pointer
```

Prompt contract:

- output_mode: `review-report`
- template_kind: `review`
- prompt_artifact_path: `docs/prompts/reviews/bronze_silver_pr542_two_family_closeout_delegated_adversarial_review_patch_prompt_v0.md`
- required_review_report_path: `docs/review-outputs/adversarial-artifact-reviews/bronze_silver_pr542_two_family_closeout_delegated_adversarial_review_patch_v0.md`
- review_lane: delegated review-and-patch convention plus adversarial artifact review
- access_mode: `repo`
- doctrine_change_decision: none; this prompt commissions review of a workflow closeout, it does not change doctrine
- prompt_author: OpenAI / Codex / GPT-5 home model
- current PR at prompt authoring: `https://github.com/eric-foo/orca/pull/542`, branch `codex/bronze-silver-two-family-closeout`, target closeout commit `a778542626fde6bade49b57b2a0950d798cb8fc7`, base `main@d7d2b62e0f528a8bba2bfe03bcb408bab2cd1358`

## Actor / Model-Family Receipt

This is a who-constraint, not a model recommendation.

- author_home_model_family: OpenAI / GPT (Codex / GPT-5 authored PR #542 and this commission)
- required_controller_family: a different vendor / model lineage from OpenAI / GPT
- current_receiving_actor_role: controller
- dispatch_mode: external-controller-courier
- de_correlation_status: operator_to_verify_before_review

If you are not a different-vendor controller, return
`BLOCKED_CONTROLLER_NOT_DECORRELATED` and do not review. Do not launch another
reviewer from inside your lane. If you are the controller, proceed after recording
your actual `reviewed_by` value in the report.

## Source-Gated Method Contract

REFERENCE-LOAD these methods first. Do not APPLY them yet:

- `workflow-deep-thinking`
- `workflow-adversarial-artifact-review`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/source-loading.md`

Then SOURCE-LOAD the task sources below. Declare either `SOURCE_CONTEXT_READY` or
`SOURCE_CONTEXT_INCOMPLETE`. Only after that declaration, APPLY deep-thinking to
frame the failure modes, then APPLY adversarial artifact review to produce
findings.

If `workflow-adversarial-artifact-review` is unavailable or not applied, return
blocked or advisory-only. Do not emit strict review claims.

## Required Source Loads

Start in repo/worktree access mode. Do not review from this prompt text alone.
If you cannot open the repo and PR branch or target commit, return
`BLOCKED_REPO_ACCESS_MISSING` and request a no-repo review package.

Minimum required reads:

1. `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/delegated-review-patch.md`, and `.agents/workflow-overlay/prompt-orchestration.md`.
3. PR #542 metadata and diff, refreshing current state rather than trusting this prompt. Preferred:
   - `gh pr view 542 --repo eric-foo/orca --json number,title,state,isDraft,url,headRefName,headRefOid,baseRefName,baseRefOid,statusCheckRollup`
   - `git diff origin/main...HEAD -- docs/workflows/bronze_silver_two_family_consumer_proof_closeout_v0.md docs/workflows/orca_repo_map_v0.md`
4. Target files:
   - `docs/workflows/bronze_silver_two_family_consumer_proof_closeout_v0.md`
   - `docs/workflows/orca_repo_map_v0.md` only around the PR #542 route/pointer lines.
5. Controlling Data Lake sources named by the closeout, targeted to the Bronze/Silver boundary rather than full-file bulk reads:
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
6. Producer/test evidence only as needed to verify closeout claims:
   - `orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py`
   - `orca-harness/capture_spine/creator_profile_current/youtube_silver_metric_producer.py`
   - `orca-harness/tests/unit/test_creator_metric_silver_producer.py`
   - `orca-harness/tests/unit/test_youtube_creator_metric_silver_producer.py`

Sources available but excluded by default: all review outputs, all prompt history,
all proof-run packets, all method-validation replays, all product files, and all
unrelated lake/runtime code.

## Fitness Reference

Goal: decide whether PR #542 is a safe, source-backed progress boundary for
moving from Bronze/Silver source-family proof work into full-GT upgrade scoping.

Done looks like: the review either finds no blocker/major issue, or patches the
bounded target files so the closeout no longer overclaims, hides residuals,
misstates evidence, or prematurely narrows the next full-GT planning lane.

Treat this as a review axis to attack, not a pass bar.

## Target And Patch Scope

Target labels:

- `[closeout]` `docs/workflows/bronze_silver_two_family_consumer_proof_closeout_v0.md`
- `[repo-map]` `docs/workflows/orca_repo_map_v0.md` only the PR #542 latest-focused addition and workflow navigation row

Patch scope:

- You may patch only the two target surfaces above.
- Patch only to close a blocker or major finding, or a minor wording defect that would materially misroute the next full-GT plan.
- Do not patch code, tests, Data Lake authority contracts, prompt policy, review-output files, or other repo-map content.
- If the correct fix lies outside the target scope, flag it. Do not edit it.
- Do not commit, push, merge, mark PR ready, or open another PR.

## Review Axes To Attack

Be adversarial about material decision-relevant failure modes:

1. Does `[closeout]` overclaim the two-family proof, or imply Bronze full GT,
   Silver readiness, production lake validation, all-source-family coverage, or
   final AR physicalization?
2. Is the recommendation to stop default source-family proof expansion supported
   tightly enough, or should it be narrowed before full-GT planning uses it?
3. Does `[closeout]` distinguish source families, source-family payloads, and AR
   join shapes accurately enough for future planning?
4. Are missing and ambiguous AR residuals represented accurately against the
   current IG and YouTube producer code and tests?
5. Does `[closeout]` correctly preserve generated Bronze catalog indexes as
   retrieval/read state rather than authority over raw packet material?
6. Are the PR #537/#540 merge facts and current-main claims stated only where
   observed, with enough recheck conditions to avoid stale PR memory?
7. Are the full-GT residuals complete enough to set up the next lane: writer
   discovery, Manifest v2 or equivalent migration, AR body layout/backend,
   retention/lawful-erasure posture, lake-doctor/CI checks, multi-family proof
   threshold, and de-correlated full-GT review?
8. Does `[repo-map]` route to the closeout without upgrading it into authority,
   validation, readiness, or lifecycle completion?
9. Does either target hide `check_placement.py --strict` repo-wide debt as a pass
   or misstate validation evidence?
10. Is there a stronger third-family proof that is a prerequisite rather than an
    optional exception? If yes, name the material raw-body / AR-join difference
    that makes it prerequisite.

## Output Report Contract

Write the durable review report to:

`docs/review-outputs/adversarial-artifact-reviews/bronze_silver_pr542_two_family_closeout_delegated_adversarial_review_patch_v0.md`

The report must include:

- retrieval header with `artifact_role: Review output (delegated adversarial review-and-patch result)` and `authority_boundary: retrieval_only`;
- `reviewed_by`: your actual model/tool identity, or `unrecorded` if the operator cannot provide it;
- `authored_by`: `OpenAI/Codex GPT-5`;
- `de_correlation_bar`: `cross_vendor_discovery` if your vendor/model lineage differs from OpenAI/GPT, otherwise do not proceed past the blocker;
- `same_vendor_rationale`: `not_applicable` for cross-vendor discovery;
- source-read ledger with file paths and the exact sections or line windows used;
- findings first, ordered by severity: `critical`, `major`, `minor`;
- for each finding: target label, citation, impact, `minimum_closure_condition`, and `next_authorized_action`;
- bounded unified diff if you patched, with target labels in nearby prose or hunk explanation;
- verdict and residual-risk note;
- validation run/not-run status, preserving failures and known out-of-scope debt.

Do not emit `patch_queue_entry`. Advisory remediation direction is allowed, but
executor-ready how-to is not.

After writing the report, return a short courier summary in chat with:

```yaml
review_summary:
  status: completed | blocked | advisory_only
  report_path: docs/review-outputs/adversarial-artifact-reviews/bronze_silver_pr542_two_family_closeout_delegated_adversarial_review_patch_v0.md
  verdict: accept | accept_with_friction | patch_before_acceptance | NEEDS_ARCHITECTURE_PASS | reject | blocked
  patched: yes | no
  findings:
    critical: <count>
    major: <count>
    minor: <count>
  next_authorized_action: home_model_adjudicates_returned_report_and_diff
```

## Review-Use Boundary

Your findings, citations, verdict, and any diff are decision input only. They are
not approval, validation, readiness, mandatory remediation, merge safety, or
auto-keep authority. The OpenAI/Codex home model must adjudicate every finding
and every patch before anything is kept.