# Core Spine v0 Data Lake Bronze Full-GT Physicalization Decision Brief Delegated Adversarial Review-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: review_prompt
scope: >
  Filed prompt for a de-correlated delegated adversarial review-and-patch pass
  over the landed Bronze full-GT physicalization decision brief (PR #557),
  before Gate 1 / Gate 2 ADR authoring relies on it.
use_when:
  - Dispatching an independent controller to harden the physicalization decision brief.
  - Checking that Gate 1 / Gate 2 framing does not silently select backend, layout, retention, or full-GT posture.
  - Preparing home-model adjudication of controller findings or a bounded patch to the brief.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_plan_v0.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
  - docs/prompts/templates/review/delegated_review_return_adjudication_v0.md
input_hashes:
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md: "git blob ab94bcacf2066cf10e97debf960e32c5170e3267 (authoritative content pin); working-copy SHA256 6E72D054D024F5686E1D3E44E4EBAF1E1DA6C8DD80A8AECB6D63F4B9ED872158 (CRLF checkout) or 403B0B0A7F19471B754B96C7562C80223F2FEA3657F6779CB0591E074F70DECF (LF); EOL normalization explains the two SHA256 forms"
branch_or_commit: >
  Target landed on main at 23f2536238ff9753f9f925652225962b26a8a09f via PR #557.
  Controller must fresh-read current origin/main HEAD at dispatch; the blob pin
  above is the content identity check.
stale_if:
  - The target blob on origin/main differs from the pinned blob hash.
  - Gate 1 or Gate 2 is ratified, superseded, or re-scoped by a later accepted authority.
  - Delegated-review-patch, review-lanes, prompt-orchestration, or the adversarial artifact review template changes materially.
```

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

## Prompt Preflight Deltas

```yaml
authorization_basis: >
  Owner instruction 2026-07-02: "prompt delegate review for the brief itself
  anyway", commissioning a delegated review-and-patch pass on the landed brief
  under the provisional convention in
  .agents/workflow-overlay/delegated-review-patch.md.
objective: >
  Commission an independent de-correlated controller to adversarially review
  and, if bounded fixes materially improve it, patch only the physicalization
  decision brief before Gate 1 / Gate 2 ADR authoring builds on it.
intended_decision: >
  Decide whether the brief is a safe foundation for the Gate 1 / Gate 2 ADR
  batch: gates correctly framed as decide-or-explicitly-defer, option ledgers
  not biased toward any backend, minimum gate outputs sufficient for an ADR
  author, supersession and proof/CI boundaries correct, and no full-GT or
  implementation overclaim.
target_files_or_dirs:
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md
source_pack: custom_bronze_full_gt_physicalization_brief_review_pack
output_mode: file-write prompt artifact, with paste-ready-chat copy below for the delegated controller
delegated_controller_return_mode: chat courier YAML plus bounded working-tree diff plus durable report
edit_permission: patch-only for the single review target; read-only for every other path
access: repo
dirty_state_allowance: >
  The controller reviews in a fresh worktree off origin/main; expected dirty
  state is only the controller's own working-tree patch to the target and the
  durable report file. Any other dirty state must be classified before review.
controlling_source_state: >
  Target blob, branch, and HEAD were checked by the dispatcher at prompt filing
  (main @ 23f25362). Controller must fresh-read and verify before strict or
  actionable claims.
branch_or_commit_reference: "origin/main; target blob ab94bcac... is the content pin; PR #557 merged 2026-07-01"
doctrine_change_decision: >
  This prompt changes no doctrine. The controller may recommend doctrine or
  architecture changes as findings only; a design-level problem returns
  NEEDS_ARCHITECTURE_PASS with no kept patch.
isolation_decision: >
  Operator creates a fresh review worktree off origin/main for the controller
  (for example: git worktree add worktrees/physicalization-brief-review origin/main).
  Do not review in the root checkout or any active lane worktree.
actor_model_family_receipt:
  author_home_model_family: "OpenAI / Codex / GPT-family (authored the brief)"
  commissioning_adjudicator_family: "Anthropic / Claude (records provenance; adjudication is cross-family from the author)"
  controller_model_family: operator_to_fill
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: operator_to_verify_before_review
validation_gates:
  - "Before review: git status --short --branch"
  - "Before review: git rev-parse HEAD; git rev-parse HEAD:orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md"
  - "If patching: git diff --check -- orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md"
  - "If patching: python .agents/hooks/check_retrieval_header.py --strict orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md"
  - "If writing the durable report: python .agents/hooks/check_retrieval_header.py --strict docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_delegated_adversarial_review_patch_v0.md"
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
```

## Paste-Ready Review Prompt

````markdown
You are the delegated controller for an Orca adversarial artifact review-and-patch hardening pass.

This is a de-correlated delegated review-and-patch commission. The artifact
author/home model family is OpenAI / Codex / GPT-family. The commissioning
adjudicator is Anthropic / Claude family (provenance fact, not a model
recommendation). To satisfy the cross-vendor discovery bar, the controller must
be from a different vendor/model lineage than the AUTHOR family (OpenAI/GPT).
If you are OpenAI/GPT-family, continue only as `same_vendor_sanity` and state
that the cross-vendor discovery bar is not satisfied. Model family is a
who-constraint only, never a runtime quality recommendation.

Current receiving actor role: controller.
Dispatch mode: external-controller-courier.
controller_model_family: operator_to_fill.
author_home_model_family: OpenAI / Codex / GPT-family.
commissioning_adjudicator_family: Anthropic / Claude.
de_correlation_status: operator_to_verify_before_review.
access: repo.

Workspace:
A fresh operator-created review worktree off `origin/main` of
`C:\Users\vmon7\Desktop\projects\orca` (for example
`git worktree add worktrees/physicalization-brief-review origin/main`).
Do not use the root checkout or any active lane worktree.

Expected base:
`origin/main`; target landed at `23f2536238ff9753f9f925652225962b26a8a09f`
(PR #557). Fresh-read current HEAD at dispatch.

Prompt source:
`docs/prompts/reviews/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_delegated_adversarial_review_patch_prompt_v0.md`

Review target and only editable file:
`orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md`

Pinned review target content identity:
git blob `ab94bcacf2066cf10e97debf960e32c5170e3267`
(verify with `git rev-parse HEAD:<target path>`). Working-copy SHA256 is
EOL-dependent: `6E72D054D024F5686E1D3E44E4EBAF1E1DA6C8DD80A8AECB6D63F4B9ED872158`
(CRLF checkout) or `403B0B0A7F19471B754B96C7562C80223F2FEA3657F6779CB0591E074F70DECF`
(LF). A mismatch of the BLOB hash is a stop condition; an EOL-only SHA256
difference is not.

Review report destination:
`docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_delegated_adversarial_review_patch_v0.md`

Review purpose:
Adversarially review whether the brief is a safe, decision-sufficient
foundation for the upcoming Gate 1 (Attachment Record body layout/backend
relationship) and Gate 2 (retention/lawful-erasure/backend lock-in) ADRs. If
bounded fixes materially improve the target, patch only the target file.

Goal: the brief must let a later ADR lane decide or explicitly defer both
gates without re-deriving constraints and without backend convenience choosing
the architecture.
Done looks like: an ADR author reading only the brief plus its open_next
contracts can produce the minimum Gate 1 / Gate 2 outputs, knows every rejected
shape, and cannot honestly read any full-GT, implementation, backend,
retention, or third-proof authorization into it.
Treat this goal as an alignment axis to attack, never a pass-if-matches bar.

Required method and authority loading:
1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. REFERENCE-LOAD these method/contract sources. Do not APPLY them yet:
   - `workflow-deep-thinking`
   - `workflow-adversarial-artifact-review`
   - `.agents/workflow-overlay/source-of-truth.md`
   - `.agents/workflow-overlay/source-loading.md`
   - `.agents/workflow-overlay/delegated-review-patch.md`
   - `.agents/workflow-overlay/review-lanes.md`
   - `.agents/workflow-overlay/prompt-orchestration.md`
   - `.agents/workflow-overlay/validation-gates.md`
   - `.agents/workflow-overlay/retrieval-metadata.md`
   - `.agents/workflow-overlay/communication-style.md`
   - `docs/prompts/templates/review/adversarial_artifact_review_v0.md`
4. SOURCE-LOAD the review target and these controlling sources:
   - `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md`
   - `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md`
5. Verify before review (validation gates above): branch/HEAD, target blob
   hash, dirty state.
6. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before
   applying any method. If incomplete, name the missing source and stop unless
   it cannot affect any finding.
7. After source context is ready, APPLY `workflow-deep-thinking` to frame the
   boundary problem and failure modes, then APPLY
   `workflow-adversarial-artifact-review` to the loaded target and sources.

Patch authority:
- You may patch only the review target named above.
- You may write the durable report only to the report destination named above.
- Do not patch this prompt artifact, `docs/workflows/orca_repo_map_v0.md`,
  overlay files, prompt templates, handoff packets, Data Lake authority
  contracts, the batch plan, source code, tests, generated JSON, raw data, or
  external lake paths. Flag off-scope issues as findings only.
- Do not stage, commit, push, open or update PRs, merge, or claim acceptance,
  validation, readiness, mandatory remediation, backend selection, retention
  posture, full GT, or product proof.

Escalation valve:
If the target is design-level wrong rather than patchably rough, return
`NEEDS_ARCHITECTURE_PASS`, revert any partial patch, and provide findings only.

Attack these failure modes first:
- Gate 1 option ledger (G1-A..G1-D) or backend-candidate table silently favors
  or effectively selects a body layout, sidecar shape, backend, engine, or
  Manifest serialization instead of preserving decide-or-defer.
- Gate 2 framing lets retention/lawful-erasure be satisfied by vague deferral:
  an acceptable deferral record's required content (accepted residuals,
  forbidden backend classes, revisit triggers) is under-specified.
- The minimum Gate 1 outputs (body key, hash_basis, physical relationship,
  public read surface, rebuild rule, replay/migration implication, rejected
  shapes) are insufficient or ambiguous for an ADR author to satisfy checkably.
- The supersession boundary misstates what the next-material-decisions packet
  still owns, or the brief's `supersedes`/`open_next` routing misleads a cold
  reader.
- PR #555 is overread as physicalization progress, coverage completeness, or
  full-GT closeness anywhere in the brief.
- The proof/CI boundary leaves a loophole where third-proof or CI hardening
  work could substitute for the gate decisions.
- The Full-GT Distance list omits a material blocker, or the Non-Claims list
  fails to block a claim the body implies.
- Public-read-surface language (`source_surface_catalog_rows`,
  `load_attachment_record_body`) contradicts the Attachment Record or storage
  contract, or implies generated catalogs are raw authority.
- The retrieval header, stale_if clauses, or status vocabulary are too thin for
  a future cold reader to detect staleness after the gates are ratified.

If you patch, run:
- `git diff --check -- orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md`
- `python .agents/hooks/check_retrieval_header.py --strict orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md`
- `python .agents/hooks/check_retrieval_header.py --strict docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_delegated_adversarial_review_patch_v0.md`

Durable report provenance: record `reviewed_by` (your model and version) and
`authored_by: OpenAI / Codex / GPT-family (operator-recorded)` on the report;
values are operator/tooling-supplied, `unrecorded` when not supplied, never
fabricated.

Return in chat to the commissioning CA:

```yaml
delegated_review_return:
  source_context: SOURCE_CONTEXT_READY | SOURCE_CONTEXT_INCOMPLETE
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback
  controller_family: "<operator/tooling supplied; do not fabricate>"
  author_home_family: "OpenAI / Codex / GPT-family"
  verdict: NEEDS_ARCHITECTURE_PASS | PATCHED_FOR_CA_ADJUDICATION | NO_PATCH_FINDINGS_ONLY
  patch_scope: "orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md only"
  report_path: "docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_delegated_adversarial_review_patch_v0.md"
  validation:
    - command: ""
      result: passed | failed | not_run
      evidence: ""
  residual_risk: ""
  ca_adjudication_required: true
```

Then list findings first, ordered `critical`, `major`, `minor`. For each finding
include severity, location, issue, evidence (neutral, decision-sufficient
citations), impact, minimum_closure_condition, next_authorized_action, and
recommended correction/advisory remediation. Do not include `patch_queue_entry`.

If you patched, include a unified diff for the target file only. The diff,
citations, and verdict are claims for CA adjudication, not accepted truth.

Adjudicator tail (for the commissioning CA, not for you): the commissioning
Chief Architect must close this return with
`.agents/workflow-overlay/communication-style.md` -> Review Adjudication Next
Step (template
`docs/prompts/templates/review/delegated_review_return_adjudication_v0.md`):
adjudicate findings/diff/verdict as claims, close self-closable material issues
in the same turn, batch admin into exactly one land step, then deep-think the
1-5 material next moves.

Review-use boundary:
Your findings and patch are decision input only. They are not approval,
validation, readiness, mandatory remediation, gate ratification, backend or
retention selection, full-GT proof, or evidence that the ADR batch may skip
owner ratification.
````
