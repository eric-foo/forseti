# ECR Consolidation v0 Plan — Cross-Family Adversarial Review + Bounded Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
review_lane: adversarial artifact review WITH explicitly-assigned patch execution (owner-authorized combined lane)
scope: >
  Independent, model-diverse adversarial review of the ECR consolidation v0
  architecture plan, with bounded authority to PATCH the plan for accepted
  correctness/citation/source-grounding defects — returning the diff and the
  citations for every change. Owner-reserved decisions stay findings-only.
use_when:
  - Dispatching the cross-family review+patch of the ECR consolidation v0 plan.
authority_boundary: retrieval_only
open_next:
  - docs/product/ecr/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md
  - .agents/workflow-overlay/review-lanes.md
input_hashes:
  docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md: 609768AEAB398A8FDDFC2D7B5EBBC1053682E3FD366A1481B54A3E137D8EF5CF
branch_or_commit: main @ d69aeee (worktree dirty; R2 posture-closure + PreservedFile.hash_basis are WORKING-TREE-ONLY, uncommitted — verify this yourself, do not trust the plan's claim)
```

## Commission

Two jobs, in order:

1. **Review** the ECR consolidation v0 plan adversarially and independently (cross-family). Confirm or break its load-bearing claims with cited evidence.
2. **Patch** the plan — under the bounded authority below — for accepted **correctness, citation, source-grounding, and consolidation-consistency** defects. **Return a diff of every change and a citation for every change**, plus the list of findings you did **not** patch (owner-reserved) and why.

The plan is advisory/PROPOSED and untracked; patching improves it before owner ratification. Your patches do not ratify it.

## Operator precondition (owner-set)

Dispatch to a reviewer in a **different model family** from the plan's author (Claude). This prompt is model-neutral; cross-family independence is the entire point (same-family lanes already converged — that is not proof).

## Target (commission-bound)

- `docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md` (SHA256 `609768AE…F5CF`). Confirm the hash before starting; if it differs, stop and report drift.

## Patch authority + boundary (read before editing anything)

You are **explicitly assigned patch execution on the plan artifact ONLY.** Within that:

- **DO patch:** factual/citation errors (wrong or stale `file:line`, an invented or no-longer-true producer fact), missing or incorrect source-grounding, internal inconsistencies, an unfenced overclaim, a derivation-table row that is wrong against the producer, a missing residual, a citation that doesn't support its claim.
- **DO NOT patch (leave as findings-only):**
  - **Owner-reserved decisions** — the AF-7 A/B choice (declare the field vs ratify only the derivation contract); the SP-6 sufficiency grade; SP-5 finalization; materiality; whether to add the missing facts capture-side vs defer (D2); the boundary-doc edit.
  - **The locked scope** — frame + source-visibility slice only; siblings stay named-but-deferred. Do not design a sibling, do not expand toward the full consolidation.
  - **The locked decisions** — D1 (partial-mechanicalness), D3 (upstream-owned/carried), D4 (bind real fields, no coined names), facts-stay-capture-side, JSG-01 frozen.
  - **The advisory fences** — keep every `not_proven` fence (especially the uncommitted-R2 / `hash_basis` fence), the non-claims, and the "supersession is described not performed" boundary. Do **not** strip them; do **not** add any strict readiness/acceptance/ratification claim.
- **Edit only this one file.** Do not touch the boundary doc, the obligation contract, the translator, any code, or any other artifact. Do not commit or push.
- **Surgical patches only.** Preserve the artifact's structure, retrieval header, and contracts. Every edit must be defensible by a citation.

If a defect can only be fixed by crossing one of the DO-NOT lines, **leave it as a finding** with a `minimum_closure_condition`, do not patch it.

## Reviewer start state

```yaml
orca_start_preflight:
  agents_read: required_yes
  overlay_read: required_yes
  source_pack: custom
  edit_permission: docs-write ON docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md ONLY (patch execution); read-only for all other source/code
  target_scope: [docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md]
  dirty_state_checked: required_yes
  blocked_if_missing: yes
controlling_source_state: worktree dirty; controlling sources untracked/modified; R2 uncommitted → advisory; patches improve the advisory plan but claim no readiness/ratification.
external_source_boundary: agent-workflow reusable mechanics only; jb is NOT Orca authority.
```

## Required read-pack — verify the producer yourself (the blind-spot lesson)

A prior review missed a defect by trusting docs over implemented code, and the plan rests on a *moving* producer. So:

- **Target:** the plan (above).
- **Independently verify the R2 / `hash_basis` state** — this is load-bearing (the plan's AF-8 / §2.4 re-point depend on it). Read `orca-harness/source_capture/models.py` in the **working tree** (expect closed posture vocabularies + `PreservedFile.hash_basis = {raw_stored_bytes}`) **and** run `git show HEAD:orca-harness/source_capture/models.py` to confirm it is **uncommitted** (absent from HEAD `d69aeee`). The plan claims working-tree-only/`not_proven`; verify that claim is exactly right — neither overstated nor understated.
- **Producer + dating:** `source_quality.py` (archive dating via `selected_snapshot.timestamp`; `_source_time` decoupled from `cutoff_posture`), `packet_assembly.py`.
- **Slice spec + lineage:** `docs/product/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md`, `docs/product/jsg01_source_side_receipt_translator_v0.md` (the SP-6 it supersedes), `docs/product/data_capture_spine_posture_vocabulary_enforcement_proposal_v0.md`.
- **Reserved boundary + vocab:** `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` (:74-75, 131-134, 281-309), obligation contract Ob.7-16, IPF Evidence Unit standard.
- **Downstream + bridge:** `orca-harness/schemas/case_models.py` (`EvidenceUnit.hash_basis`), `pydantic_schema_reference.md`, `packing_to_harness_foundation_interface_architecture_v3.md`.

## Method sequence (Source-Gated Method Contract)

1. Read authority (`AGENTS.md`, overlay README, review-lanes, prompt-orchestration, source-of-truth).
2. `REFERENCE-LOAD` `workflow-deep-thinking`, then `workflow-adversarial-artifact-review`. Do not APPLY yet.
3. `SOURCE-LOAD` the read-pack; verify the producer state yourself.
4. Declare `SOURCE_CONTEXT_READY` / `SOURCE_CONTEXT_INCOMPLETE`.
5. APPLY deep-thinking to frame failure modes, then adversarial-artifact-review to produce findings (each cited). **Then** apply the bounded patches.

## What to attack (verify independently; cite everything)

1. **Scope held?** Frame + slice only; siblings named-but-deferred and genuinely not designed; no drift toward the full consolidation.
2. **The three-mode binding rule** — is it actually general enough to not pre-commit siblings, and concrete enough that SP-6 instantiates it? Any mode mis-assigned?
3. **D1 residuals** — replay the derivation table against the *current producer*: do rows 7-8 correctly route to `RESIDUAL_COMPARISON_NOT_RECORDED` (no stored comparison)? Any row wrong, missing, or firing a value it can't support?
4. **D3 / `hash_basis` re-point** — is upstream-owned/carried correct, and is the re-point to `PreservedFile.hash_basis` correctly **fenced `not_proven`** given it's uncommitted? Flag any place the plan treats R2 as landed.
5. **D4 / no coined names** — does the slice bind the real Armory fields and read the implemented `cutoff_posture` `VisibleFact` rather than minting a same-named enum?
6. **Citations** — spot-check the plan's `file:line` citations against source. Any stale (like the prior PR-01), wrong, or unsupported? (This is the highest-yield patch class.)
7. **Supersession boundary** — does the plan only *describe* superseding the translator's SP-6, not *perform* it (the JSG-01 consumer is frozen / lane-owned)?
8. **Fences/non-claims intact** — JSG-01 frozen; owner-reserved residuals not leaked; no strict claim.

## Output contract

- **Output mode:** `review-report` + authorized patch execution. Write the durable report to `docs/review-outputs/adversarial-artifact-reviews/ecr_consolidation_v0_plan_cross_family_review_v0.md`.
- Start with the `review_summary` YAML (`recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked`), then findings.
- **Findings:** ID, `severity` (`critical|major|minor`, priority only), seam, **citation(s)** (`file:line`), `minimum_closure_condition`, `next_authorized_action`, and `patched: yes/no`.
- **Patches applied:** for each, return a triplet — **(a) the diff** (a clear unified diff or before/after block of the exact edit), **(b) the finding it fixes**, **(c) the citation(s)** that ground it. Surgical only.
- **Not patched (owner-reserved):** list each, why it's owner-reserved, and the `minimum_closure_condition`.
- **Updated artifact:** report the patched plan's path and **new SHA256** (from a fresh read), and confirm only that one file changed.
- Include non-findings (seams that held) and not-proven boundaries.

## Validation gates (must be able to fail)

- Source readiness declared; the producer state (working-tree vs HEAD) **independently verified**, not taken from the plan.
- Target hash confirmed; drift → BLOCKED.
- Every patch carries a citation and a diff; no uncited edit.
- No owner-reserved decision patched; no scope expansion; no fence/non-claim stripped; only the plan file changed.
- Durable report written before any YAML-only chat summary; new artifact hash reported from a fresh read.
- Cross-family independence stated (or, if same-family, say so and downgrade to advisory).

## Review-use boundary

Findings + patches are decision input for the owner. Patching the advisory plan does not ratify it, unfreeze JSG-01, edit the boundary doc, or land R2. The owner verifies the returned diff + citations before treating the patched plan as the basis for ratification. `agent-workflow` is reusable mechanics only; `jb` is not Orca authority.
```
