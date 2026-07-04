# Forseti Rename PR #646 Delegated Adversarial Review-And-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Commissions a de-correlated adversarial review-and-patch pass for PR #646,
  the project rename branch that makes Forseti the live project identity across
  authority, doctrine, product, prompt, skill, hook-message, and navigation
  surfaces.
use_when:
  - Couriering PR #646 to an independent controller before the rename branch is merged.
  - Checking whether live authority still leaks stale Orca identity or over-renames historical and compatibility surfaces.
  - Requesting a bounded patch only inside the PR #646 rename scope after branch freshness is verified.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - docs/decisions/forseti_rename_migration_policy_v0.md
branch_or_commit: >
  PR #646 branch codex/forseti-rename-authority; commission drafted from
  branch head 33b24541 before this prompt artifact was added. The reviewer must
  refresh PR state and use the current PR head as source of truth.
stale_if:
  - PR #646 head moves after this prompt without the receiver refreshing PR metadata and branch state.
  - The base branch advances and the PR diff starts showing unrelated current-main drift as rename work.
  - A later prompt supersedes this PR #646 delegated review commission.
```

## Objective

Run a de-correlated adversarial review-and-patch pass on PR #646 before the home
model treats the Forseti rename branch as merge-ready.

Intended decision for the home model after your return:

- `accept`: PR #646 is safe to merge after ordinary branch landing checks.
- `accept_with_friction`: PR #646 is coherent, but named residuals must travel.
- `patch_before_acceptance`: you found and patched a bounded rename defect; the
  home model must adjudicate the diff before keep.
- `BLOCKED_BRANCH_FRESHNESS`: the branch must first merge or rebase current main
  because the PR diff is contaminated by unrelated base drift.
- `NEEDS_ARCHITECTURE_PASS`: the rename policy or authority boundary is wrong at
  doctrine level and cannot be fixed by local patching.
- `reject`: PR #646 should not land without rework.

## Why This Review Happens First

This branch changes live project identity and authority language. A self-review
can easily normalize stale project-name leakage, false path claims, or
compatibility residuals. The review must attack whether the branch cleanly makes
Forseti canonical while preserving intentionally historical, compatibility, and
lowercase path surfaces.

## Forseti Start Preflight

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S0/S1 plus PR #646 metadata, PR diff, rename policy, changed authority/doctrine/product/prompt/skill/hook-message surfaces
  edit_permission: patch-only inside PR #646 rename-scope files; all other paths read-only / flag-only
  target_scope: delegated adversarial review-and-patch prompt for the Forseti rename PR
  dirty_state_checked: yes; authoring branch was clean at 33b24541 before this prompt artifact was added
  blocked_if_missing: repo access to PR #646 branch, current PR metadata, overlay review rules, rename policy, and target diff
```

Prompt contract:

- output_mode: `review-report`
- template_kind: `review`
- prompt_artifact_path: `docs/prompts/reviews/forseti_rename_pr646_delegated_adversarial_review_patch_prompt_v0.md`
- required_review_report_path: `docs/review-outputs/adversarial-artifact-reviews/forseti_rename_pr646_delegated_adversarial_review_patch_v0.md`
- review_lane: delegated review-and-patch convention plus mixed artifact/code review
- access_mode: `repo`
- repo_map_decision: `not_needed`; target selection comes from PR #646 metadata and diff, while changed repo-map sections are receiver target sources
- doctrine_change_decision: none for this prompt artifact; the prompt commissions review of a doctrine-touching rename branch but does not itself change doctrine
- prompt_author: OpenAI / Codex / GPT-5 home model
- current observed PR state at prompt drafting: `https://github.com/eric-foo/orca/pull/646`, branch `codex/forseti-rename-authority`, pre-prompt head `33b24541`, local `origin/main` `a90191bce2bcf1f093b1ff3cc4d01a7b911b7884`, and local divergence `2 8` from `git rev-list --left-right --count origin/main...HEAD`

## Actor / Model-Family Receipt

This is a who-constraint, not a runtime model recommendation.

- author_home_model_family: OpenAI / GPT (Codex / GPT-5 authored the rename branch and this commission)
- required_controller_family: operator_to_fill; must be a different vendor / model lineage from OpenAI / GPT for a cross-vendor discovery pass
- current_receiving_actor_role: controller
- dispatch_mode: external-controller-courier
- de_correlation_status: operator_to_verify_before_review

If you are not a different-vendor controller, return
`BLOCKED_CONTROLLER_NOT_DECORRELATED` and do not review. Do not launch another
reviewer from inside your lane. If you are the controller, proceed after
recording your actual `reviewed_by` value in the report.

## Source-Gated Method Contract

REFERENCE-LOAD these methods first. Do not APPLY them yet:

- `workflow-deep-thinking`
- `workflow-adversarial-artifact-review`
- `workflow-code-review`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/safety-rules.md`

Then SOURCE-LOAD the task sources below. Declare either `SOURCE_CONTEXT_READY`
or `SOURCE_CONTEXT_INCOMPLETE`. Only after that declaration, APPLY
deep-thinking to frame failure modes, then APPLY:

- `workflow-adversarial-artifact-review` to docs, prompts, decisions, product
  artifacts, overlay files, and skill text; and
- `workflow-code-review` to hook, checker, script, workflow, and test-adjacent
  changes.

If a required review method is unavailable or not applied, return blocked or
advisory-only for that target class. Do not emit strict review claims for a lane
you did not apply.

## Required Source Loads

Start in repo/worktree access mode. Do not review from this prompt text alone.
If you cannot open the repo and PR branch or target commit, return
`BLOCKED_REPO_ACCESS_MISSING`.

Minimum required reads:

1. `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/source-of-truth.md`, `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/delegated-review-patch.md`, `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/artifact-roles.md`, and `.agents/workflow-overlay/safety-rules.md`.
3. PR #646 metadata and diff, refreshed from the current PR state rather than
   trusting this prompt. Preferred checks:
   - `gh pr view 646 --repo eric-foo/orca --json number,title,state,isDraft,url,headRefName,headRefOid,baseRefName,baseRefOid,statusCheckRollup`
   - `git status --short --branch`
   - `git rev-list --left-right --count origin/main...HEAD`
   - `git diff --name-status origin/main...HEAD`
4. The rename policy: `docs/decisions/forseti_rename_migration_policy_v0.md`.
5. Changed live authority and doctrine surfaces, especially `AGENTS.md`,
   `CLAUDE.md`, `README.md`, `.agents/workflow-overlay/**`,
   `docs/STRUCTURE.md`, and `docs/workflows/orca_repo_map_v0.md`.
6. Changed product anchor and proof surfaces under
   `orca/product/spines/foundation/product_contract/` and
   `orca/product/spines/product_lead/`.
7. Changed prompt, template, and local skill surfaces under
   `docs/prompts/**`, `.agents/skills/orca-product-lead/SKILL.md`, and
   `.claude/skills/orca-product-lead/SKILL.md`.
8. Changed hook/check/script/workflow surfaces under `.agents/hooks/`,
   `.agents/checks/`, `.github/scripts/`, and `.github/workflows/`.

Sources available but excluded by default: historical DCP archives, historical
review outputs, unrelated runtime source, package/import compatibility
migrations, broad product corpus files not changed by PR #646, and any external
workflow source outside this repository.

## Branch-Freshness Gate

At prompt drafting, the local branch had two commits on `origin/main` not present
in the branch. That does not by itself invalidate the review, but it means the
receiver must not trust a stale local diff blindly.

Before reviewing rename substance:

1. Refresh PR #646 metadata and branch state.
2. Confirm whether the current PR diff contains only the rename branch plus this
   commission prompt.
3. If the diff includes unrelated deletions or additions caused by base drift,
   return `BLOCKED_BRANCH_FRESHNESS` and name the contaminated paths. Do not
   patch those paths as rename work.
4. If the branch is fresh enough or the base drift is irrelevant to the PR diff,
   proceed and record the observed head and base.

## Fitness Reference

Goal: make Forseti the canonical live project identity across project authority,
doctrine, product, prompt, local skill, hook-message, and navigation surfaces
without erasing intentional historical or compatibility evidence.

Done looks like: the review either finds no blocker or major issue, or patches
the bounded PR #646 files so live authority consistently says Forseti, residual
Orca usage is intentionally classified, paths/packages that remain `orca` are
not falsely renamed, and validation gaps are visible rather than hidden.

Treat this as a review axis to attack, not a pass bar.

## Target And Patch Scope

Target labels:

- `[rename-policy]` `docs/decisions/forseti_rename_migration_policy_v0.md`
- `[authority-overlay]` `AGENTS.md`, `CLAUDE.md`, `README.md`, `.agents/workflow-overlay/**`
- `[doctrine-decisions]` changed decision records under `docs/decisions/`
- `[product-proof]` changed product anchors under `orca/product/`
- `[prompts-skills]` changed prompt templates, prompt READMEs, review prompts, handoffs, and local product-lead skills
- `[hooks-checks]` changed hook/check/script/workflow message surfaces
- `[repo-map-nav]` `docs/STRUCTURE.md`, `docs/workflows/orca_repo_map_v0.md`, and `repo-structure.yaml`

Patch scope:

- You may patch only files already changed by PR #646, plus this prompt artifact
  only if a prompt defect blocks the commissioned review.
- Patch only to close a blocker or major finding, or a minor wording/path defect
  that would materially misroute future agents.
- Preserve intentional historical records, archived receipts, old review
  outputs, old prompt bodies, old branch/PR names, package/import compatibility,
  lowercase path compatibility, and repository identifiers unless the rename
  policy or PR #646 explicitly made them live rename targets.
- Do not rename packages, imports, directories, CI job identifiers, repository
  remotes, product spine filenames, or compatibility paths as part of this
  review unless they are already inside the PR #646 rename scope and the policy
  clearly requires it.
- If the correct fix lies outside the target scope, flag it. Do not edit it.
- Do not commit, push, merge, mark the PR ready, open another PR, or change
  branch metadata.

## Review Axes To Attack

Be adversarial about material decision-relevant failure modes:

1. Does any live authority, doctrine, prompt, local skill, hook/check message,
   product anchor, or navigation surface still present Orca as the canonical
   current project identity rather than Forseti?
2. Does the branch over-rename historical records, archived receipts, old review
   outputs, old prompt artifacts, queue IDs, branch names, or evidence that must
   stay point-in-time?
3. Does any file assert filesystem paths, package names, imports, repo names, or
   local paths were renamed to Forseti when they still intentionally contain
   `orca`?
4. Does `docs/decisions/forseti_rename_migration_policy_v0.md` clearly classify
   residual Orca usage into live rename targets, compatibility residuals,
   historical records, and deferred migrations?
5. Do `.agents/workflow-overlay/source-loading.md` and prompt templates prefer
   `forseti_start_preflight` while preserving `orca_start_preflight` only as a
   compatibility alias?
6. Do review/prompt surfaces avoid runtime model recommendations while still
   carrying the required de-correlation who-constraint where applicable?
7. Do hook/check/script changes alter only user-facing project-name messages, or
   did the rename accidentally change behavior, matching logic, or validation
   boundaries?
8. Does `AGENTS.md` still correctly route project facts to the Forseti overlay
   and avoid importing `jb` or stale Orca authority?
9. Are validation claims honest, including the known registration-integrity
   selftest gap and the operator instruction not to rerun the stalled workaround?
10. Does PR #646 leave a coherent residual plan for compatibility paths,
    package/import names, repository identity, historical prompt/review files,
    and older product/harness material?
11. Are grammar and article defects introduced by mechanical rename present,
    such as `an Forseti`, `a Orca`, duplicated words, or broken capitalization?
12. Does the current PR diff include unrelated source deletions or additions
    from base drift that must block review until the branch is refreshed?

## Validation Evidence To Inspect

Use current evidence, not this prompt, for final claims. The home lane previously
reported these checks on the rename branch:

- `git diff --check origin/main..HEAD`: clean at the time run.
- `python .agents\hooks\header_index.py --strict`: pass.
- `python .agents\hooks\check_dcp_receipt.py --strict`: pass.
- `python .agents\hooks\check_map_links.py --strict`: pass.
- `python .agents\hooks\check_review_routing.py --strict`: pass.
- Python syntax parsing for changed hook/check files: pass.
- Changed hook/check selftests passed except `registration_integrity.py --selftest`, which hit temporary-directory permission issues and was not rerun after operator interruption.

Do not rerun the prior stalled registration-integrity workaround command. If
registration-integrity coverage matters to a finding, report the specific
not-run gap or use a fresh, bounded, non-stalling inspection that does not repeat
the stalled command.

If you patch files, run the smallest relevant validation that can fail and
report exact pass, fail, blocked, or not-run status. Preserve real failures.

## Output Report Contract

Write the durable review report to:

`docs/review-outputs/adversarial-artifact-reviews/forseti_rename_pr646_delegated_adversarial_review_patch_v0.md`

The report must include:

- retrieval header with `artifact_role: Review output (delegated adversarial review-and-patch result)` and `authority_boundary: retrieval_only`;
- `reviewed_by`: your actual model/tool identity, or `unrecorded` if the operator cannot provide it;
- `authored_by`: `OpenAI/Codex GPT-5`;
- `de_correlation_bar`: `cross_vendor_discovery` if your vendor/model lineage differs from OpenAI/GPT, otherwise do not proceed past the blocker;
- `same_vendor_rationale`: `not_applicable` for cross-vendor discovery;
- PR metadata and branch-freshness receipt, including observed head, base, and dirty state;
- source-read ledger with file paths and the exact sections, commands, or line windows used;
- findings first, ordered by severity: `critical`, `major`, `minor`;
- for each finding: target label, citation, impact, `minimum_closure_condition`, and `next_authorized_action`;
- bounded unified diff if you patched, with target labels in nearby prose or hunk explanation;
- verdict and residual-risk note;
- validation run/not-run status, preserving failures and the registration-integrity not-run gap.

Do not emit `patch_queue_entry`. Advisory remediation direction is allowed, but
executor-ready how-to is not.

After writing the report, return a short courier summary in chat with:

```yaml
review_summary:
  status: completed | blocked | advisory_only
  report_path:
  reviewed_by:
  authored_by: OpenAI/Codex GPT-5
  de_correlation_bar:
  branch_freshness:
  findings:
    critical: 0
    major: 0
    minor: 0
  patch_applied: yes | no
  validation:
    status: pass | fail | blocked | not_run | mixed
    commands:
      - command:
        result:
  verdict: accept | accept_with_friction | patch_before_acceptance | BLOCKED_BRANCH_FRESHNESS | NEEDS_ARCHITECTURE_PASS | reject
  next_authorized_action:
```

## Controller Return And CA Adjudication

Your diff, citations, and verdict are claims to adjudicate, not premises to
inherit. The home model / Chief Architect decides what is kept.

If you find a design-level problem, return `NEEDS_ARCHITECTURE_PASS`, stop
patching, and leave no partial diff for keep.

The commissioning Chief Architect must adjudicate the findings, diff, verdict,
and residuals as claims; close any self-closable material issue inside its own
authority and the commissioned scope in the same turn; route a smallest-complete
closure step only for issues needing another lane, architecture pass, review
round, or owner decision; then batch admin/lifecycle follow-ups into exactly one
land step and deep-think the 1-5 material next moves that need judgment.

## Forbidden Moves

- Do not review from a summary or context pack instead of inspecting the repo or
  PR branch directly.
- Do not widen the review beyond PR #646 rename scope.
- Do not patch off-scope protected, canonical, generated, test, runtime,
  package/import, or compatibility surfaces.
- Do not claim validation, readiness, approval, mergeability, or lifecycle
  completion from this review.
- Do not suppress branch-freshness contamination.
- Do not recommend, rank, or imply runtime model choice.
- Do not import `jb` project policy or external workflow source as Forseti
  authority.
