# Core Spine v0 Data Lake Bronze Full-GT Gate ADR Batch Delegated Adversarial Review-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: review_prompt
scope: >
  Filed prompt for the B5 multi-target de-correlated delegated adversarial
  review-and-patch pass over the Gate ADR batch: the Gate 1 body-layout ADR,
  the Gate 2 retention/lawful-erasure posture ADR, and a bounded recheck of the
  patched physicalization brief, before owner ratification of either gate.
use_when:
  - Dispatching the single batch review pass required by the Gate ADR batch plan (B5).
  - Checking cross-gate consistency between the two ADRs before ratification.
  - Discharging the physicalization brief's outstanding cross-vendor discovery bar.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_plan_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - docs/prompts/templates/review/delegated_review_return_adjudication_v0.md
input_hashes:
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md: "git blob 8448df4acb9147649cfa31b668fe6156aaeff123"
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md: "git blob 5fd4aeef3f48da97f403923a49f077c1abaacc3c"
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md: "git blob 4b5e5abf7e5215caad003a2de6713e3f5d8567a3"
branch_or_commit: >
  Targets authored on lane branch claude/bronze-gate-adr-batch at
  68627923f439e717076badf228d418f32477db89 (PR pending at prompt filing).
  Controller must fresh-read the current lane-branch HEAD at dispatch; blob
  hashes above are the content identity checks.
stale_if:
  - Any target blob on the lane branch differs from its pinned hash and the operator has not re-pinned.
  - Either gate is ratified before this pass runs (review-before-ratification is the point).
  - Delegated-review-patch, review-lanes, or prompt-orchestration doctrine changes materially.
```

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

## Prompt Preflight Deltas

```yaml
authorization_basis: >
  Owner instruction 2026-07-02 ("proceed with your ADR stuff") executing the
  Gate ADR batch plan, whose B5 step requires one delegated review-patch pass
  over the authored batch before owner ratification.
objective: >
  Commission one de-correlated controller pass that adversarially reviews and,
  where bounded fixes materially improve them, patches the two Gate ADRs, and
  runs a bounded recheck of the patched physicalization brief.
intended_decision: >
  Decide whether the Gate 1 and Gate 2 ADRs are safe to put in front of the
  owner for ratification: internally consistent, contract-consistent,
  cross-gate consistent, honest about residuals, and free of silent selection
  or claim inflation.
target_files_or_dirs:
  - "[gate1-adr] orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md"
  - "[gate2-adr] orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md"
  - "[brief-recheck] orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md (bounded recheck; patch only for defects this batch exposes)"
source_pack: custom_gate_adr_batch_review_pack
output_mode: file-write prompt artifact, with paste-ready-chat copy below for the delegated controller
delegated_controller_return_mode: chat courier YAML plus bounded working-tree diff plus durable report
edit_permission: patch-only for the three labeled targets; read-only for every other path
access: repo
dirty_state_allowance: >
  Review on the lane branch; expected dirty state is only the controller's own
  working-tree patches to the labeled targets and the durable report file.
controlling_source_state: >
  Target blobs, branch, and HEAD pinned by the dispatcher at prompt filing
  (lane branch @ 68627923). Controller must fresh-read and verify before
  strict or actionable claims.
branch_or_commit_reference: "claude/bronze-gate-adr-batch; blob pins above are the content identity"
doctrine_change_decision: >
  This prompt changes no doctrine. The ADRs become doctrine-changing only at
  owner ratification and contract fold-in, which happen after this pass.
  Design-level problems return NEEDS_ARCHITECTURE_PASS with no kept patch.
isolation_decision: >
  Operator provides a worktree checked out to the lane branch (or a fresh
  worktree added at its HEAD). Do not review in the root checkout.
actor_model_family_receipt:
  author_home_model_family: "[gate1-adr]/[gate2-adr]: Anthropic / Claude (Fable); [brief-recheck]: OpenAI / Codex / GPT-family"
  commissioning_adjudicator_family: "Anthropic / Claude"
  controller_model_family: operator_to_fill
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: operator_to_verify_before_review
validation_gates:
  - "Before review: git status --short --branch; git rev-parse HEAD"
  - "Before review: git rev-parse HEAD:<each labeled target path> and compare to the pinned blobs"
  - "If patching: git diff --check -- <patched paths>"
  - "If patching: python .agents/hooks/check_retrieval_header.py --strict <patched paths>"
  - "If writing the durable report: python .agents/hooks/check_retrieval_header.py --strict docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_delegated_adversarial_review_patch_v0.md"
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
```

## De-correlation Note (who-constraint, not a model recommendation)

The batch ADRs were authored by an Anthropic/Claude lane; the brief was
authored by an OpenAI/Codex lane. One controller reviews all three targets:

- A controller from neither family (for example Google/Gemini lineage, or any
  other non-Anthropic, non-OpenAI vendor) satisfies cross-vendor discovery on
  ALL targets - the preferred dispatch.
- An OpenAI-family controller satisfies discovery on the two ADRs but only
  same-vendor sanity on [brief-recheck], leaving the brief's discovery bar
  open again.
- An Anthropic-family controller satisfies discovery on [brief-recheck] only
  and is same-vendor for the ADRs - do not dispatch this shape.

The controller must state which bar each label actually achieved in the
return; unknown or undisclosed lineage cannot claim discovery.

## Paste-Ready Review Prompt

````markdown
You are the delegated controller for an Orca adversarial artifact
review-and-patch hardening pass over a THREE-TARGET labeled batch.

Who-constraint (not a model recommendation): the ADR targets' author family is
Anthropic/Claude; the brief target's author family is OpenAI/GPT. State your
own vendor lineage. Cross-vendor discovery holds per label only where your
lineage differs from that label's author family; otherwise that label is
same_vendor_sanity. If you are Anthropic-family, stop and report - the
dispatch shape is wrong.

Current receiving actor role: controller.
Dispatch mode: external-controller-courier.
controller_model_family: operator_to_fill.
de_correlation_status: operator_to_verify_before_review.
access: repo.

Workspace: an operator-provided worktree of
`C:\Users\vmon7\Desktop\projects\orca` checked out to branch
`claude/bronze-gate-adr-batch`. Fresh-read HEAD at dispatch; expected authoring
commit `68627923f439e717076badf228d418f32477db89`.

Prompt source:
`docs/prompts/reviews/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_delegated_adversarial_review_patch_prompt_v0.md`

Labeled targets (the ONLY editable files), with pinned git blob identities
(verify each with `git rev-parse HEAD:<path>`):

- `[gate1-adr]`
  `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md`
  blob `8448df4acb9147649cfa31b668fe6156aaeff123`
- `[gate2-adr]`
  `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md`
  blob `5fd4aeef3f48da97f403923a49f077c1abaacc3c`
- `[brief-recheck]`
  `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md`
  blob `4b5e5abf7e5215caad003a2de6713e3f5d8567a3`
  BOUNDED: full adversarial discovery read, but patch only defects that this
  batch exposes (contradiction with an ADR, stale routing, or a gate
  requirement the ADRs reveal as wrong); do not restyle it.

A blob mismatch on any target is a stop condition.

Review report destination:
`docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_delegated_adversarial_review_patch_v0.md`

Review purpose:
Decide whether these ADRs are safe for owner ratification. Goal: after
ratification, an implementation-scoping lane must be able to act on the two
gates without re-deriving constraints, and no reader can honestly extract a
backend selection, erasure capability, or full-GT claim from them.
Done looks like: every Gate 1 output is checkably specific, the Gate 2
deferral record is complete per the hardened brief, the two ADRs cannot be
read to contradict each other or the authority contracts, and every residual
is named rather than smoothed. Treat this as an axis to attack, never a
pass-if-matches bar.

Required method and authority loading:
1. Read `AGENTS.md`, then `.agents/workflow-overlay/README.md`.
2. REFERENCE-LOAD, do not APPLY yet: `workflow-deep-thinking`,
   `workflow-adversarial-artifact-review`,
   `.agents/workflow-overlay/delegated-review-patch.md`,
   `.agents/workflow-overlay/review-lanes.md`,
   `.agents/workflow-overlay/prompt-orchestration.md`,
   `.agents/workflow-overlay/validation-gates.md`,
   `.agents/workflow-overlay/retrieval-metadata.md`,
   `.agents/workflow-overlay/communication-style.md`,
   `docs/prompts/templates/review/adversarial_artifact_review_v0.md`.
3. SOURCE-LOAD the three labeled targets plus:
   - `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_plan_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md`
   - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md`
   - `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_delegated_adversarial_review_patch_v0.md`
4. Verify branch/HEAD/blobs/dirty state (validation gates in the filed prompt).
5. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before
   applying any method.
6. Then APPLY `workflow-deep-thinking` to frame failure modes, then APPLY
   `workflow-adversarial-artifact-review` across the batch.

Patch authority:
- Patch only the three labeled targets, within their stated bounds; write the
  durable report only to the destination above.
- Do not patch this prompt, the batch plan, the repo map, overlay files,
  authority contracts, templates, code, or tests. Flag off-scope issues as
  findings only.
- Do not stage, commit, push, open/update PRs, merge, ratify, or claim
  acceptance, validation, readiness, backend selection, erasure capability,
  or full GT.

Escalation valve:
`NEEDS_ARCHITECTURE_PASS` (per label or whole-batch) on any design-level
problem: stop patching that scope, revert its partial diff, findings only.

Attack these failure modes first (cite per label):
- [gate1-adr] The packet-member selection quietly commits more than a
  relationship: implies a serialization, freezes the raw path grammar the
  physicality contract left unfrozen, or contradicts the raw-admission key
  grammar.
- [gate1-adr] The eight outputs are not checkably specific: hash_basis
  ambiguity survives (compressed/derived bodies), the sidecar reopen trigger
  is vague enough to bypass, or "subsumed G1-A" hides an unratified residual.
- [gate2-adr] The deferral record fails its own bar: residual scope rests on
  an unverified "public-web only" basis without treating that basis as part
  of the residual, the claim ceiling leaks capability language, tombstone
  semantics contradict append-only or rebuild rules, or a forbidden-backend
  class has a convenient loophole.
- [cross-gate] G1-D lockout vs Gate 2 triggers are inconsistent; sidecar
  keying (Gate 1) vs future key-separated erasure (G2-C) conflict; replay/
  migration language (Gate 1) vs tombstone/supersession (Gate 2) diverge.
- [cross-gate] Ratifying both ADRs would still not clear the brief's two
  gates as "decided or explicitly deferred" - any gap between what the brief
  requires and what the ADRs deliver.
- [brief-recheck] The patched brief now disagrees with the ADRs' shape,
  routes readers wrongly, or its gate requirements were satisfied only
  nominally.
- [all] Claim inflation anywhere: ratification-pending records readable as
  selected doctrine, review readable as validation, or full-GT distance
  shortened.

If you patch, run the validation gates from the filed prompt and report real
results; a failing gate is surfaced, never routed around.

Durable report provenance: record `reviewed_by` (your model and version) and
`authored_by: [gate1-adr]/[gate2-adr] Anthropic/Claude; [brief-recheck]
OpenAI/GPT (operator-recorded)`; values operator/tooling-supplied,
`unrecorded` when not supplied, never fabricated.

Return in chat to the commissioning CA:

```yaml
delegated_review_return:
  source_context: SOURCE_CONTEXT_READY | SOURCE_CONTEXT_INCOMPLETE
  de_correlation_bar_per_label:
    gate1_adr: cross_vendor_discovery | same_vendor_sanity | self_fallback
    gate2_adr: cross_vendor_discovery | same_vendor_sanity | self_fallback
    brief_recheck: cross_vendor_discovery | same_vendor_sanity | self_fallback
  controller_family: "<operator/tooling supplied; do not fabricate>"
  verdict_overall: NEEDS_ARCHITECTURE_PASS | PATCHED_FOR_CA_ADJUDICATION | NO_PATCH_FINDINGS_ONLY
  verdict_per_label: { gate1_adr: "", gate2_adr: "", brief_recheck: "" }
  patch_scope: "the three labeled targets only"
  report_path: "docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_delegated_adversarial_review_patch_v0.md"
  validation:
    - command: ""
      result: passed | failed | not_run
      evidence: ""
  residual_risk: ""
  ca_adjudication_required: true
```

Then findings first, ordered `critical`, `major`, `minor`, each tagged with
its label and carrying severity, location, issue, neutral decision-sufficient
evidence, impact, minimum_closure_condition, next_authorized_action, and
recommended correction. No `patch_queue_entry`. If you patched, include a
unified diff with each hunk prefixed by its label tag.

Adjudicator tail (for the commissioning CA, not for you): close this return
per `.agents/workflow-overlay/communication-style.md` -> Review Adjudication
Next Step (template
`docs/prompts/templates/review/delegated_review_return_adjudication_v0.md`):
adjudicate findings/diff/verdicts as claims, close self-closable material
issues same-turn, one batched land step, then deep-think the 1-5 material
moves - which include routing the ratification decision to the owner.

Review-use boundary: findings and patches are decision input only - not
ratification, acceptance, validation, readiness, backend or retention
selection, erasure capability, or Bronze full GT.
````
