# Core Spine v0 Data Lake Bronze Full-GT Upgrade Scoping Delegated Adversarial Review-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: review_prompt
scope: >
  Filed prompt for a de-correlated delegated adversarial review-and-patch pass
  over the Bronze full-GT A-D upgrade scoping artifact.
use_when:
  - Dispatching an independent reviewer to harden the Bronze A-D full-GT scoping artifact.
  - Checking that the A-D success signals preserve non-claims and do not select runtime physicalization choices.
  - Preparing home-model adjudication of reviewer findings or a bounded patch to the scoping artifact.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
input_hashes:
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md: sha256:DBF60C295E640A3E66F370220EC728E0E02B5AF1104418861550EBD2D4582072
branch_or_commit: >
  Authored on codex/bronze-full-gt-scoping at 89501743dfd6aa0a2b4423e8f1d5fe1042758af7;
  target is branch-based while PR #542 is open and not merged.
stale_if:
  - The target artifact hash differs from the value above.
  - PR #542 is materially rewritten, closed without merge, superseded, or merged with a different proof boundary.
  - Delegated-review-patch, review-lanes, prompt-orchestration, or the adversarial artifact review template changes.
```

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

## Prompt Preflight Deltas

```yaml
authorization_basis: >
  Current owner instruction: finish A-D with fused discipline and create a
  delegated review prompt for all of them after.
objective: >
  Commission an independent de-correlated controller to adversarially review and,
  if bounded wording fixes are needed, patch only the Bronze full-GT A-D scoping
  artifact before home-model adjudication.
intended_decision: >
  Decide whether the scoping artifact correctly names A-D success signals,
  residuals, non-claims, and review checkpoints without selecting Manifest,
  AR layout/backend, retention/lawful-erasure, CI/lake-doctor mechanics, or
  a Bronze full-GT claim.
target_files_or_dirs:
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md
source_pack: custom_bronze_full_gt_a_d_scoping_review_pack
output_mode: file-write prompt artifact, with paste-ready-chat copy below for the delegated controller
delegated_controller_return_mode: paste-ready-chat plus bounded diff; durable report when repo access permits
edit_permission: patch-only for the single review target; read-only for every other path
dirty_state_allowance: >
  Expected dirty state may include this prompt, the scoping artifact, and
  repo-map pointer rows before the dispatching CA commits. The controller must
  classify any dirty state before review and patch only the target artifact.
controlling_source_state: >
  Target hash, branch, and HEAD were checked by the dispatcher before prompt
  filing. Controller must fresh-read and verify before making strict or
  actionable claims.
branch_or_commit_reference: "codex/bronze-full-gt-scoping at 89501743dfd6aa0a2b4423e8f1d5fe1042758af7; PR #542 branch-based, not merged"
doctrine_change_decision: >
  This prompt does not change product doctrine, validation doctrine, workflow
  authority, review authority, or lifecycle boundaries. Reviewer may recommend
  doctrine or architecture changes as findings only. If a design-level correction
  is needed, return NEEDS_ARCHITECTURE_PASS and leave no patch.
isolation_decision: >
  Use the existing codex/bronze-full-gt-scoping worktree for review unless the
  operator creates a separate review worktree. Do not retarget to main unless
  the operator updates the prompt after PR #542 lands.
validation_gates:
  - "Before review: git status --short --branch"
  - "Before review: git rev-parse HEAD"
  - "Before review: Get-FileHash -Algorithm SHA256 -LiteralPath orca\\product\\spines\\data_lake\\workflows\\core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md"
  - "If patching: git diff --check -- orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md"
  - "If patching or writing a report: python .agents/hooks/check_retrieval_header.py --strict orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md"
  - "If writing a durable report: python .agents/hooks/check_retrieval_header.py --strict docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_delegated_adversarial_review_patch_v0.md"
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target_block
```

## Paste-Ready Review Prompt

````markdown
You are the delegated controller for an Orca adversarial artifact review-and-patch hardening pass.

This is a de-correlated delegated review-and-patch commission. The author/home
model family is OpenAI / Codex / GPT-family. To satisfy cross-vendor discovery,
the controller must be from a different vendor/model lineage. If you are not
from a different vendor/model lineage, continue only as `same_vendor_sanity` or
`self_fallback` and state that the cross-vendor discovery bar is not satisfied.
Do not present model family as a runtime quality recommendation; it is only a
who-constraint.

Current receiving actor role: controller.
Dispatch mode: operator_to_fill.
controller_model_family: operator_to_fill.
author_home_model_family: OpenAI / Codex / GPT-family.
de_correlation_status: operator_to_verify_before_review.

Workspace:
`C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-full-gt-scoping`

Expected branch/reference:
`codex/bronze-full-gt-scoping` at `89501743dfd6aa0a2b4423e8f1d5fe1042758af7`.

PR/base state:
This target is branch-based while PR #542 is open and not merged. Do not treat
PR #542 as landed-main proof unless you fresh-read current PR state and the
operator explicitly changes the base.

Prompt source:
`docs/prompts/reviews/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_delegated_adversarial_review_patch_prompt_v0.md`

Review target and only editable file:
`orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md`

Pinned review target hash:
`sha256:DBF60C295E640A3E66F370220EC728E0E02B5AF1104418861550EBD2D4582072`

Review report destination:
`docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_delegated_adversarial_review_patch_v0.md`

Review purpose:
Adversarially review whether the target correctly finishes A-D scoping for the
Bronze full-GT upgrade lane: success signals first, source-backed residuals,
non-claims, no premature runtime physicalization choices, no PR #542 overclaim,
and correct review-patch timing. If bounded wording fixes materially improve the
target, patch only the target file.

Fitness reference:
The target succeeds only if a later CA or implementation-scoping lane can tell
what would make A-D true, what remains not proven, what is docs/scoping versus
implementation, and what evidence or review must exist before any later
full-GT claim. The target must preserve the handoff's drift guard: PR #542 is
consumer proof, generated catalogs are read state rather than raw authority,
missing/ambiguous AR states stay visible, and Manifest/body/backend/retention
choices are lock-in choices.

Required method and authority loading:
1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. REFERENCE-LOAD these method/contract sources. Do not APPLY them yet:
   - `workflow-deep-thinking`
   - `workflow-adversarial-artifact-review`
   - `.agents/workflow-overlay/source-of-truth.md`
   - `.agents/workflow-overlay/source-loading.md`
   - `.agents/workflow-overlay/artifact-folders.md`
   - `.agents/workflow-overlay/artifact-roles.md`
   - `.agents/workflow-overlay/delegated-review-patch.md`
   - `.agents/workflow-overlay/review-lanes.md`
   - `.agents/workflow-overlay/prompt-orchestration.md`
   - `.agents/workflow-overlay/validation-gates.md`
   - `.agents/workflow-overlay/retrieval-metadata.md`
   - `.agents/workflow-overlay/communication-style.md`
   - `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
4. SOURCE-LOAD the review target and these controlling sources:
   - `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md`
   - `docs/prompts/handoffs/bronze_silver_full_gt_promotion_after_pr542_handoff_v0.md`
   - `docs/workflows/bronze_silver_two_family_consumer_proof_closeout_v0.md`
   - `docs/review-outputs/adversarial-artifact-reviews/bronze_silver_pr542_two_family_closeout_delegated_adversarial_review_patch_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
5. Verify before review:
   - `git status --short --branch`
   - `git rev-parse HEAD`
   - `Get-FileHash -Algorithm SHA256 -LiteralPath orca\product\spines\data_lake\workflows\core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md`
6. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before applying
   any method. If incomplete, name the missing file/source and stop unless the
   missing source cannot affect any finding.
7. After source context is ready, APPLY `workflow-deep-thinking` to frame the
   boundary problem and failure modes, then APPLY
   `workflow-adversarial-artifact-review` to the loaded target and sources.

Patch authority:
- You may patch only
  `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md`.
- You may write the review report only to
  `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_delegated_adversarial_review_patch_v0.md`.
- Do not patch this prompt artifact.
- Do not patch `docs/workflows/orca_repo_map_v0.md`, overlay files, prompt
  templates, handoff packets, PR #542 closeout files, Data Lake authority
  contracts, source code, tests, generated JSON, raw data, or external lake
  paths.
- Do not stage, commit, push, open or update PRs, merge, or claim acceptance,
  validation, readiness, mandatory remediation, full GT, or product proof.
- Flag off-scope issues as findings only.

Escalation valve:
If the target is design-level wrong rather than patchably rough, return
`NEEDS_ARCHITECTURE_PASS`, leave no patch, and provide findings only.

Attack these failure modes first:
- Batch A silently selects Manifest v2, packet-index serialization, migration,
  dual-read, replay, or cutoff mechanics instead of preserving a decision fork.
- Batch B silently selects packet-member, sidecar, body-store, backend, engine,
  Manifest v2, migration, or Silver producer implementation.
- Batch C treats retention, lawful-erasure, backend, WORM, crypto-shredding, or
  compliance posture as selected rather than explicitly deferred.
- Batch D treats PR #542 as all-source, cross-domain, production-lake, or
  landed-main proof.
- Batch D hides the YouTube ambiguous-AR residual or treats code-present as
  test-proven.
- The target treats generated Bronze catalog/index files as raw authority.
- The target implies runtime implementation authorization, validation success,
  Silver readiness, real-lake completeness, or Bronze full GT.
- The delegated-review timing is over- or under-stated: no review should block
  scoping, but review must precede ratifying high-lock-in choices and any
  future full-GT claim.
- The retrieval header, stale_if clauses, or source ledger are too thin for a
  future cold reader to avoid stale PR #542 or authority assumptions.

If you patch, run:
- `git diff --check -- orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md`
- `python .agents/hooks/check_retrieval_header.py --strict orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md`
- `python .agents/hooks/check_retrieval_header.py --strict docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_delegated_adversarial_review_patch_v0.md`

Return in chat to the commissioning CA:

```yaml
delegated_review_return:
  source_context: SOURCE_CONTEXT_READY | SOURCE_CONTEXT_INCOMPLETE
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback
  controller_family: "<operator/tooling supplied; do not fabricate>"
  author_home_family: "OpenAI / Codex / GPT-family"
  verdict: NEEDS_ARCHITECTURE_PASS | PATCHED_FOR_CA_ADJUDICATION | NO_PATCH_FINDINGS_ONLY
  patch_scope: "orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md only"
  report_path: "docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_delegated_adversarial_review_patch_v0.md"
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
citations, and verdict are claims for CA adjudication, not accepted truth. The
CA may accept, modify, or reject any change.

Review-use boundary:
Your findings and patch are decision input only. They are not approval,
validation, readiness, mandatory remediation, product proof, executor-ready
authority, full-GT proof, or evidence that A-D is complete until the
commissioning CA adjudicates them.
````
