# Bronze/Silver IG Proof-Slice Prep Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (handoff family; non-source proof-slice prep)
scope: >
  Forward record and handoff prompt for the first IG Silver-facing proof-slice
  preparation after PR 530 merged into the Bronze MGT baseline stack.
use_when:
  - Continuing Bronze/Silver work after PR 530 closeout and delegated batch-closeout review.
  - Preparing, but not implementing, the first IG proof slice that should consume public Bronze catalog and Attachment Record surfaces.
  - Checking the boundary between admissible review/prompt/spec work and blocked source-changing work while the lower stack is not on main.
authority_boundary: retrieval_only
open_next:
  - docs/review-outputs/adversarial-artifact-reviews/bronze_silver_pr530_batch_closeout_delegated_review_patch_v0.md
  - docs/prompts/handoffs/bronze_silver_post_pr530_goal_frame_handoff_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
  - orca-harness/data_lake/catalog.py
  - orca-harness/source_capture/ig_reels_grid_projection.py
  - orca-harness/tests/test_data_lake_catalog.py
  - orca-harness/tests/unit/test_source_capture_ig_reels_projection.py
branch_or_commit: codex/bronze-silver-ig-proof-prep @ 7119d9af3f4158e1f55b4a3a3247256ea7f51a85
stale_if:
  - PR 523 or PR 478 stack status changes before the next actor starts.
  - The receiving work starts from main before the Bronze MGT stack has landed there.
  - IG catalog/projection source paths change before this handoff is used.
  - A real-lake IG Silver proof run or a true Silver raw_refs producer lands and supersedes the fixture/unit evidence boundary.
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  output_mode: file-write
  template_kind: handoff
  prompt_artifact_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-silver-ig-proof-prep\docs\prompts\handoffs\bronze_silver_ig_proof_slice_prep_handoff_v0.md
  authorization_basis: owner asked to batch steps 2/3/4 with deep-thinking and assumption-gate after admin PR step 1 was done
  edit_permission: docs-write for this handoff only; no runtime/source implementation authorization
  workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-silver-ig-proof-prep
  branch: codex/bronze-silver-ig-proof-prep
  branch_base: origin/codex/bronze-mgt-baseline at 7119d9af3f4158e1f55b4a3a3247256ea7f51a85
  dirty_state_allowance: clean except this handoff while authoring
  workflow_sequence_policy: overlay_owned
  workflow_sequence_source: accepted_project_artifact plus explicit_user_instruction
  workflow_sequence_status: bound_for_non_source_prep_only
  source_pack: custom_pr530_closeout_plus_ig_projection_selection_sources
  downstream_edit_permission: read-only/spec-or-handoff-only unless owner separately authorizes source-changing work
  doctrine_change_decision: no doctrine change; this forwards existing constraints and does not alter prompt, review, validation, or lifecycle doctrine
  validation_gates:
    - prompt/retrieval/header hygiene for this handoff
    - map/link/freshness checks for durable prompt placement
    - no runtime tests required because no source code changes
  non_claims:
    - not implementation authorization
    - not Silver readiness
    - not Bronze full GT
    - not proof that Silver raw_refs production exists
    - not approval or validation of a future implementation
```

## Goal Handoff / Active Objective

Continue the Bronze/Silver convergence lane by preparing the first IG
Silver-facing proof slice without starting source-changing work from `main`
while the lower Bronze stack remains unsettled.

Anchor goal: prove, in a later authorized source-changing unit, that a
Silver-facing consumer can use public Bronze packet/catalog/Attachment Record
surfaces and carry verified raw/source references forward without relying on
private folder semantics.

Success signals for the later proof slice:

- Uses `source_surface_catalog_rows`, Attachment Record rows, and
  `load_attachment_record_body` rather than raw folder discovery.
- Treats generated Bronze catalog content as retrieval aid, not source
  authority.
- Carries hash-checkable raw/source references into the Silver-facing record or
  explicitly records missing AR as a visible residual.
- Does not claim Bronze full God Tier, Silver readiness, AR runtime completion,
  storage/backend choice, Manifest v2, or lake-doctor readiness.

## Current Stack State

Observed before this handoff was written:

- PR 530 is `MERGED` into `codex/bronze-mgt-baseline`; PR head was
  `6d18f9ed6e6dc94d0030ed5e630201d2e507d991` and CI was `SUCCESS`.
- This prep branch starts at `7119d9af3f4158e1f55b4a3a3247256ea7f51a85`, the
  updated `origin/codex/bronze-mgt-baseline` merge commit for PR 530.
- PR 523 is open from `codex/bronze-mgt-baseline` into
  `codex/bronze-v41-clean-verify`, `CLEAN`, with CI `SUCCESS`.
- PR 478 is open draft from `codex/bronze-v41-clean-verify` into `main` and is
  `DIRTY`.

Implication: PR 530 closeout is done for its stack position, but new
source-changing work from `main` remains blocked until the lower stack lands or
the owner explicitly redirects source work to a stack branch. Review, prompt,
handoff, and spec-only prep may continue on an isolated lane based on the PR 530
base.

## Corrected Next-Batch Instructions To Carry

Carry these forward from the delegated batch-closeout review:

1. Branch/lifecycle: the earlier "no commit/push/PR because no source changed"
   applied only to the inspect/test batch. The review prompt and review report
   are now durable artifacts on the PR 530 lane; do not treat the lane as
   "nothing to land."
2. Evidence scoping: the IG proof-slice readiness is selection-grade and
   fixture/unit-level. `project_ig_reels_grid_from_bronze_catalog` consumes
   public Bronze surfaces and writes a `projection_ig_reels_grid` derived record;
   it is not yet a Silver `raw_refs` producer.
3. Admissible lane: prompt/review/spec prep on the PR 530 stack is admissible;
   new source-changing work off `main` remains blocked until the lower stack
   settles or the owner redirects to a stack branch.
4. Wording fix: say the projection consumes public Bronze surfaces:
   `source_surface_catalog_rows` for packet/AR rows plus the separate
   `load_attachment_record_body` helper.

## Deep-Think Decision Frame

The live options were:

- Start source-changing Silver work off `main`: rejected. The needed PR 530
  content is not proven on `main`, and PR 478 remains draft/dirty.
- Start source-changing work on the stack branch now: owner-redirect only. It
  may become appropriate, but this turn did not authorize source implementation.
- Do only admin/wait: too passive after PR 530 merged; it loses the chance to
  preserve the proof-slice contract while the stack settles.
- Prepare a non-source proof-slice handoff on top of the PR 530 base: selected.
  It captures the target and residuals without creating implementation drift.

Recommendation: next actor should use this handoff to prepare or scope the IG
proof slice only after rechecking stack state. Source edits need explicit
bounded authorization and a current branch decision.

## Assumption Gate

```yaml
assumption_gate:
  status: READY_WITH_VERIFIED_LEDGER
  applies_to: non-source IG Silver-facing proof-slice prep after PR 530 merge
  load_bearing_assumptions:
    - assumption: PR 530 content is present on the base used for this prep handoff.
      why_load_bearing: The proof-slice prep depends on the Bronze MGT declaration and delegated closeout artifacts; without them the handoff would target a missing contract.
      verify_by: source_read
      verdict: verified_real
      evidence: prep branch at 7119d9af from origin/codex/bronze-mgt-baseline; PR 530 reported MERGED; batch-closeout review report exists in docs/review-outputs/adversarial-artifact-reviews/.
    - assumption: main-based source-changing work remains blocked even though PR 530 is merged.
      why_load_bearing: Starting implementation from main would bake in a false base-state assumption and likely miss the Bronze MGT stack content.
      verify_by: source_read
      verdict: verified_real
      evidence: PR 523 open/CLEAN/CI-success into codex/bronze-v41-clean-verify; PR 478 open draft/DIRTY into main.
    - assumption: the IG path is suitable as a selected proof-slice scaffold but not yet proof of Silver raw_refs production.
      why_load_bearing: Overstating fixture/unit evidence as Silver proof would create a false readiness claim and aim the implementation at the wrong success bar.
      verify_by: source_read
      verdict: verified_real
      evidence: MGT declaration says full GT item #5 still requires a Silver producer carrying verified refs into raw_refs; projection code consumes source_surface_catalog_rows and load_attachment_record_body but writes projection_ig_reels_grid; tests use DataLakeRoot.for_test.
  prerequisites:
    - item: Recheck PR 523/478/main stack state before any source-changing step.
      triage: blocker
      owner: agent
      order: 1
      basis: Verified current lower stack is not main-settled; stale_if requires refresh.
    - item: Owner redirect is required before source-changing work on a stack branch.
      triage: blocker
      owner: owner
      order: 2
      basis: Current turn authorizes non-source prep, not implementation or stack-branch source edits.
    - item: Real-lake proof and true Silver raw_refs producer evidence.
      triage: deferrable
      owner: agent
      order: 3
      basis: Safe to defer because this artifact is only prep; it explicitly preserves the fixture/unit residual.
    - item: Prompt/handoff hygiene for this durable artifact.
      triage: already-decided
      owner: agent
      order: 4
      basis: AGENTS.md and prompt-orchestration overlay require durable prompt artifacts under docs/prompts/** with retrieval metadata and prompt provenance checks.
  next_authorized_step: Use this handoff for a non-source proof-slice spec/scoping pass, or recheck stack state and obtain explicit source-changing authorization before implementation.
```

## Receiving Actor Instructions

Before making strict or actionable claims, re-open this handoff's `open_next`
sources and recheck the current PR stack. Do not trust the stack observations
above if PR 523, PR 478, or `main` has changed.

If source-changing implementation is not explicitly authorized in the receiving
turn, stop at one of these non-source outputs:

- an implementation-scoping packet for the IG proof slice;
- a spec for the Silver-facing raw-ref success bar;
- a prompt/wrapper for a later implementation lane.

If source-changing implementation is explicitly authorized later, the first
implementation target should be the narrowest proof that an IG Silver-facing
producer or bridge consumes public Bronze catalog/AR surfaces and carries
verified refs into a Silver-facing `raw_refs` shape. It must preserve these
boundaries:

- no raw folder semantics;
- no generated catalog authority claim;
- no Bronze full-GT claim;
- no Silver readiness claim from fixture/unit tests alone;
- missing AR remains explicit residual, not inferred absence.

Do not infer `/fused` from this handoff. If the owner explicitly invokes
`/fused`, run the fused pipeline from current source state after rechecking the
assumption gate prerequisites.

## Non-Claims

This handoff is a prep artifact only. It is not implementation, not validation,
not review approval, not source promotion, not a patch queue, not a PR merge
instruction, not a model-routing recommendation, and not a claim that the lower
Bronze stack has reached `main`.
