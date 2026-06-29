# Creator Signal Spine Pre-Ratification Delegated Adversarial Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: review_prompt
scope: >
  Filed prompt for a delegated adversarial review-and-patch pass over the
  Creator Signal spine pre-ratification review input.
use_when:
  - Dispatching a different-family reviewer to harden the Creator Signal pre-ratification review input.
  - Running the delegated review-and-patch convention before Creator Signal spine propagation.
authority_boundary: retrieval_only
open_next:
  - docs/review-inputs/creator_signal_spine_pre_ratification_review_input_v0.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
stale_if:
  - The review input is materially changed after this prompt is filed.
  - The Creator Signal spine is accepted, rejected, or superseded before review.
  - The delegated review-and-patch overlay convention or adversarial artifact review template changes.
```

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

## Prompt Preflight Deltas

```yaml
authorization_basis: "Current owner instruction: fused go; propagation deferred until delegated review is adjudicated."
objective: >
  Review and harden the non-authoritative Creator Signal spine pre-ratification
  review input before any promotion patch creates or propagates the high-level
  Creator Signal product spine.
intended_decision: >
  Determine whether the proposed `creator_signal` high-level spine/surface shape
  is coherent enough to promote after CA adjudication, and patch only the review
  input if bounded wording changes would materially improve it.
target_files_or_dirs:
  - docs/review-inputs/creator_signal_spine_pre_ratification_review_input_v0.md
source_pack: custom_creator_signal_pre_ratification_review
output_mode: file-write prompt artifact, with paste-ready-chat copy below for the delegated controller
delegated_controller_return_mode: paste-ready-chat
edit_permission: patch-only for the single review input target; read-only for every other path
dirty_state_allowance: >
  The dispatcher may provide this prompt before the pre-review files are committed.
  Verify current branch, HEAD, and dirty state before review; if the target file
  is absent or changed from the dispatcher-stated scope, return SOURCE_CONTEXT_INCOMPLETE.
controlling_source_state: "Overlay and target sources must be fresh-read by the reviewer; dispatcher did not claim propagated doctrine."
branch_or_commit_reference: "codex/creator-ledger-static-fixture; reviewer must verify current HEAD and target dirty state before review."
doctrine_change_decision: >
  The review input is non-authoritative and deliberately avoids doctrine propagation.
  A later promotion patch would be doctrine-changing and must update route surfaces
  with a direction_change_propagation receipt.
isolation_decision: "Use the existing lane worktree; do not create a new product spine or move files during review."
validation_gates:
  - "If patching: run `git diff --check`."
  - "If patching markdown: run `python .agents/hooks/check_retrieval_header.py --changed --strict`."
  - "If patching markdown: run `python .agents/hooks/header_index.py --strict`."
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
```

## Paste-Ready Review Prompt

```markdown
You are the delegated controller for an Orca review-and-patch hardening pass.

This is a de-correlated review-and-patch commission. The author/home model family
is OpenAI/GPT. To satisfy cross-vendor discovery, the controller must be from a
different vendor/model lineage. If you are not from a different vendor/model
lineage, continue only as `same_vendor_sanity` or `self_fallback` and state that
the cross-vendor discovery bar is not satisfied. Do not present model family as
a quality recommendation; it is only a who-constraint.

Current receiving actor role: controller.
Dispatch mode: external-controller-courier or repo-mode controller, depending on
how the operator launches you.

Workspace:
`C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-ledger-static-fixture`

Expected branch/reference:
`codex/creator-ledger-static-fixture`. Verify current `git rev-parse HEAD` and
`git status --short --branch` before review. The review target may be committed
or uncommitted depending on how the dispatcher hands off this prompt; review only
the named target if present and in scope.

Review target and only editable file:
`docs/review-inputs/creator_signal_spine_pre_ratification_review_input_v0.md`

Prompt source:
`docs/prompts/reviews/creator_signal_spine_pre_ratification_delegated_adversarial_review_patch_prompt_v0.md`

Review purpose:
Adversarially review whether the proposed high-level `creator_signal` spine and
creator-intelligence surface are coherent, correctly bounded, and safe to
promote later without moving the low-level Capture contracts or sneaking in
runtime/storage/dashboard/public-directory claims. Patch only bounded wording
inside the review target when it materially improves that pre-ratification review
input.

Fitness reference:
The target succeeds only if a later CA can use it to decide whether to promote
Creator Signal as a high-level product/signal spine while preserving these
boundaries: low-level Capture/Data Lake contracts stay low-level; route
propagation waits until review adjudication; no runtime, SQLite, dashboard, real
rows, public directory, outreach, contact, or readiness claim is introduced.

Required authority and method loading:
1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. REFERENCE-LOAD these method/contract sources. Do not APPLY them yet:
   - `workflow-deep-thinking`
   - `workflow-adversarial-artifact-review`
   - `.agents/workflow-overlay/delegated-review-patch.md`
   - `.agents/workflow-overlay/review-lanes.md`
   - `.agents/workflow-overlay/prompt-orchestration.md`
4. SOURCE-LOAD these task sources:
   - the review target;
   - `.agents/workflow-overlay/source-of-truth.md`;
   - `.agents/workflow-overlay/artifact-folders.md`;
   - `.agents/workflow-overlay/source-loading.md`;
   - `.agents/workflow-overlay/validation-gates.md`;
   - `orca/product/README.md`;
   - `orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md`;
   - `orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md`;
   - `docs/prompts/templates/review/adversarial_artifact_review_v0.md`.
5. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before
   applying any method. If incomplete, name the missing file/source and stop
   unless the missing source cannot change the finding.
6. After source context is ready, APPLY `workflow-deep-thinking` to frame the
   boundary problem and failure modes, then APPLY
   `workflow-adversarial-artifact-review` to the loaded target and sources.

Patch authority:
- You may patch only
  `docs/review-inputs/creator_signal_spine_pre_ratification_review_input_v0.md`.
- Do not create `orca/product/spines/creator_signal/`.
- Do not update `orca/product/README.md`,
  `.agents/workflow-overlay/artifact-folders.md`,
  `docs/workflows/orca_repo_map_v0.md`, or any route/propagation surface.
- Do not patch prompts, templates, overlay files, runtime files, validators, JSON
  ledgers, data lake contracts, or capture specs. Flag off-scope issues instead.
- Do not stage, commit, push, open a PR, or claim acceptance/readiness.

Escalation valve:
If the proposal is design-level wrong rather than patchably rough, return
`NEEDS_ARCHITECTURE_PASS`, leave no patch, and provide findings only.

Review checks:
- Is `creator_signal` a justified high-level spine rather than Product Lead,
  Capture, Data Lake, a satellite, or a dashboard-only artifact?
- Does the review input preserve low-level contract ownership?
- Does it avoid implying public person identity, outreach, contact enrichment,
  public directory, buyer proof, validation, readiness, SQLite adoption, or live
  capture?
- Does it name a complete enough post-review promotion patch without performing
  that propagation now?
- Are the proposed review attack points sufficient for CA adjudication?

If you patch, run:
- `git diff --check`
- `python .agents/hooks/check_retrieval_header.py --changed --strict`
- `python .agents/hooks/header_index.py --strict`

Return in chat to the commissioning CA:

```yaml
delegated_review_return:
  source_context: SOURCE_CONTEXT_READY | SOURCE_CONTEXT_INCOMPLETE
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback
  controller_family: "<operator/tooling supplied; do not fabricate>"
  author_home_family: "OpenAI/GPT"
  verdict: NEEDS_ARCHITECTURE_PASS | PATCHED_FOR_CA_ADJUDICATION | NO_PATCH_FINDINGS_ONLY
  patch_scope: "target file only"
  validation:
    - command: ""
      result: passed | failed | not_run
      evidence: ""
  residual_risk: ""
  ca_adjudication_required: true
```

Then list findings first, ordered `critical`, `major`, `minor`. For each finding
include severity, location, issue, evidence, impact, minimum_closure_condition,
next_authorized_action, and recommended correction/advisory remediation. Do not
include `patch_queue_entry`.

If you patched, include a unified diff for the target file only. The diff,
citations, and verdict are claims for CA adjudication, not accepted truth. The CA
may accept, modify, or reject any change.

Review-use boundary:
Your findings and patch are decision input only. They are not approval,
validation, readiness, mandatory remediation, product proof, or executor-ready
authority until the commissioning CA adjudicates them.
```
