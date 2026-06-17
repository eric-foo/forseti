# ECR + SCR Source-Side Migration Inventory v0

```yaml
retrieval_header_version: 1
artifact_role: Migration inventory (ECR/SCR source-side, docs-only)
scope: >
  Inventory-only marking artifact for Evidence Candidate Record (ECR) and
  Signal Content Record (SCR) source-side derived-record surfaces before a
  future spine-first repo migration. Classifies ownership, proposed future
  allocation, risky moves, runtime/code boundaries, stale naming risks, and
  unresolved owner decisions.
use_when:
  - Preparing a future spine-first migration that may move ECR and SCR together or separately.
  - Deciding what belongs to ECR, what belongs to SCR, what is shared, and what stays owned by Capture, Cleaning, Judgment, global overlay, or shared harness.
  - Checking the unresolved SCR allocation decision before moving source-side derived-record artifacts.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/ecr_spine_submap_v0.md
  - docs/product/ecr/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md
  - docs/product/signal_content/core_spine_v0_signal_content_record_architecture_v0.md
  - docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
stale_if:
  - PR #237 or a successor renames Signal Content Record to Signal Statement Record on main.
  - PR #239 or a successor binds a live spine-first workspace root.
  - PR #242 or a successor moves Core Spine / Foundation paths on main.
  - ECR, SCR, Evidence Binding, FinalizationReceipt, or SourceCapturePacket paths move.
  - The owner settles whether SCR is under ECR, a sibling in the same source-side spine, a separate spine, or a shared substrate.
```

## Purpose

This is an inventory, not a migration. It marks the current ECR/SCR
source-side derived-record surfaces that a future spine-first migration must
consider. It does not move files, rename files, change code, ratify doctrine,
validate readiness, or settle SCR's future spine allocation.

Repo evidence uses **Evidence Candidate Record** for ECR. The current user task
uses **Evidence Capture Record**. This inventory preserves that mismatch as a
stale-naming risk rather than silently treating the names as settled aliases.

## Start Preflight Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 + ECR source-side read pack + targeted SCR/ECR searches
  edit_permission: docs-write
  target_scope: docs/migration/ecr_scr_source_side_migration_inventory_v0.md
  dirty_state_checked: yes
  branch_checked: codex/ecr-spine-first-migration-inventory
  working_tree_state: clean in lane worktree before edit
  root_checkout_state: >
    main...origin/main [behind 1] with unrelated untracked .codex/hooks/run_orca_guard.py,
    _scratch/, orca-worktrees/, and an existing permission warning for
    orca-harness/.pytest_tmp/. Root checkout not edited.
  blocked_if_missing: no source files moved; no code changed; SCR allocation remains owner decision
```

Cynefin routing: complicated, source-led migration inventory. Allowed next move:
write one docs-only inventory. Disallowed next move: move/rename source files,
redesign Capture/Cleaning/Judgment, or settle SCR ownership without controlling
evidence.

## Pending Structure Inputs Not Assumed Merged

The following open PRs were checked through the GitHub connector during this
lane. They are not assumed merged into `main`.

| PR | Observed state | Migration implication |
| --- | --- | --- |
| #237 `Rename Signal Statement Record` | Open draft. Renames Signal Content/SCR to Signal Statement Record, including docs, code, tests, and routing. | Any SCR target must be conditional: current `signal_content` paths remain live on this branch; future path may be `signal_statement`. |
| #239 `docs: add commission signal board pilot spine` | Open draft. Proposes `orca/product/spines/<spine>/` and says Commission Signal Board is the pilot. | Spine-first root is proposed, not live. Use `move_later` or `pointer_only`. |
| #242 `docs: rename Core Spine to Foundation Layer` | Open draft. Moves Core Spine lane docs to Foundation Layer paths. | Boundary, IPF, and data-lake target paths must tolerate `core_spine/` until the PR lands. |
| #243 `[codex] docs: add ECR spine-first migration inventory` | Open draft. ECR-only predecessor inventory. | Keep as predecessor/provenance. This artifact is the ECR+SCR source-side successor inventory, not a source move. |
| #232 `docs: add data lake core contract` | Open draft. Adds shared data-lake contract and pointers from capture/ECR maps. | Shared data-lake mechanics should remain pointer-only unless the global structure binding absorbs it. |

## Required Searches Run

```powershell
rg --files docs orca-harness .agents | rg "(^docs/product/ecr/|^docs/product/signal_content/|ecr|ECR|signal_content|Signal Content|SCR|scr)"
rg --files docs\decisions docs\prompts docs\review-outputs docs\workflows docs\migration orca-harness\ecr orca-harness\signal_content orca-harness\tests | rg "(ecr|ECR|signal_content|Signal|SCR|scr|source_side|source-side|receipt|integrity|schema)"
rg -l "ECR|Evidence Capture Record|Evidence Candidate Record|SCR|Signal Content Record|Signal Content|source-side derived record|source-side|source visibility|source-visibility|receipt translator|integrity posture|SP-1|SP-2|SP-3|SP-6|schema evolution|derived-record" docs .agents orca-harness --glob "!_scratch/**" --glob "!orca-worktrees/**" --glob "!docs/review-inputs/**"
rg -n "Evidence Capture Record|Evidence Candidate Record" docs .agents orca-harness --glob "!_scratch/**" --glob "!orca-worktrees/**" --glob "!docs/review-inputs/**"
```

Search exclusions: `_scratch/`, old worktrees, generated caches, and copied
review-input source bundles. Case/source-capture receipts are not listed
individually unless they are directly ECR/SCR migration-relevant; broad
case-receipt hits are Capture/case provenance, not ECR/SCR ownership.

## Migration Mark Values

| Mark | Meaning |
| --- | --- |
| `move_later` | Candidate for a future migration package after spine-first binding and owner decisions settle. |
| `pointer_only` | Future ECR/SCR spine should point to this surface; canonical file/code stays in its owner lane. |
| `do_not_move` | Not ECR/SCR-owned; migration belongs elsewhere or the surface is global. |
| `historical_only` | Preserve as provenance/archive only; do not treat as live authority. |
| `owner_decision` | Future home cannot be selected until the owner settles SCR allocation or naming. |

## Proposed Future Allocation

This inventory keeps two allocation tracks because the repo does not settle the
decision question.

| Allocation question | Current evidence | Proposed migration handling |
| --- | --- | --- |
| ECR integrity postures SP-1/SP-2/SP-3/SP-6 | ECR-owned source-side integrity records, current code under `orca-harness/ecr/`, current docs under `docs/product/ecr/`. | If a combined lane is accepted: `orca/product/spines/ecr_scr_source_side/ecr/`. If separate: `orca/product/spines/ecr/`. |
| SCR content layer | Submap says sibling content layer; SCR direction doc says parallel derived `SignalContentRecord`, keyed to `SourceCapturePacket`, composed by reference, not merged into ECR. | If a combined lane is accepted: `orca/product/spines/ecr_scr_source_side/scr/`. If separate or PR #237 lands: `orca/product/spines/signal_content/` or `orca/product/spines/signal_statement/`. |
| Shared source-side discipline | Carry-or-residualize, re-derive-not-migrate, reference-never-merge, by-key composition. | Shared `authority/` or `workflows/` under combined lane, or pointer docs in both separate spines. |
| Runtime/code | ECR and SCR code exists under `orca-harness/`. | No executable code move in this pass. Future spine gets pointer docs only unless a separate code-root migration is authorized. |

Decision preserved for owner: should SCR be a module under the ECR source-side
spine, a sibling derived-record surface inside the same ECR/SCR source-side
spine, a separate future spine, or a shared substrate consumed by ECR and
Judgment? Current source does not settle this.

## 1. Current Repo Surfaces Found

| Surface | Current path(s) | Owner lane | Proposed future target | Mark | Dependencies | Validation after future move |
| --- | --- | --- | --- | --- | --- | --- |
| ECR/SCR front door | `docs/workflows/ecr_spine_submap_v0.md` | Shared ECR/SCR navigation, ECR-hosted today | Combined: `orca/product/spines/ecr_scr_source_side/workflows/ecr_spine_submap_v0.md`; separate: ECR workflow plus SCR pointer | `move_later` | PR #237, #239, #242 | Repo-map update, stale path search, open-next path check |
| ECR-only predecessor inventory | `docs/migration/ecr_spine_first_migration_inventory_v0.md` | ECR migration/provenance | `orca/product/spines/ecr_scr_source_side/migrations/ecr_spine_first_migration_inventory_v0.md` or ECR archive | `historical_only` | This inventory | Preserve as predecessor; do not replace source authority |
| ECR frame + SP-6 plan | `docs/product/ecr/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md` | ECR-owned integrity plan | Combined: `.../ecr/plans/...`; separate: `orca/product/spines/ecr/plans/...` | `move_later` | Boundary doc, SP-6 Judgment docs | Reference rewrites, source-pin recheck, no JSG-01 claim |
| SP-1/SP-2/SP-3 plan | `docs/product/ecr/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md` | ECR-owned integrity plan | Combined: `.../ecr/plans/...`; separate: `orca/product/spines/ecr/plans/...` | `move_later` | SourceCapturePacket producer fields, ECR frame | ECR deriver/test pointer check |
| JSG-01 EvidenceUnit binding slice plan | `docs/product/ecr/ecr_consolidation_v0_jsg01_evidence_unit_binding_slice_plan_v0.md` | ECR/Judgment boundary plan | Combined: `.../ecr/boundaries/...` plus Judgment pointer | `move_later` | Evidence Binding code, conductor, SP-5 | Recheck reserved full Evidence Unit non-claim |
| SCR direction doc | `docs/product/signal_content/core_spine_v0_signal_content_record_architecture_v0.md` | SCR-owned or SCR-candidate | `.../scr/authority/...`, or `signal_statement/authority/...` if PR #237 lands | `owner_decision` | ECR postures by key, IPF, PR #237 | Rename rebase; no ECR ownership claim |
| SCR deriver plan | `docs/product/signal_content/signal_content_record_deriver_architecture_plan_v0.md` | SCR-owned or SCR-candidate | `.../scr/plans/...`, or `signal_statement/plans/...` if PR #237 lands | `owner_decision` | SCR model/deriver, ECR posture refs | Rename rebase; signal_content test pointer check |
| Boundary/ratification source | `docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Foundation/Core boundary | Foundation/global authority with ECR/SCR pointers | `pointer_only` | PR #242, JSG-01 decisions | Pointer rewrite after Foundation rename |
| IPF Evidence Unit standard | `docs/product/core_spine/core_spine_v0_information_production_foundation_v0.md` | Foundation/IPF | Foundation/global authority with ECR/SCR pointers | `pointer_only` | PR #242 | Pointer rewrite; no Evidence Unit design claim |
| Data-lake mechanics map | `docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md` | Foundation/shared mechanics | Foundation/shared; ECR/SCR pointer only | `pointer_only` | PR #232, #242 | Pointer rewrite; no storage/runtime claim |
| Capture submap | `docs/workflows/data_capture_spine_consolidation_map_v0.md` | Capture-owned navigation | Capture spine workflow with ECR/SCR pointer | `pointer_only` | SourceCapturePacket producer docs | Cross-map pointer check |
| Packet schema evolution | `docs/product/data_capture_spine/source_capture_packet_schema_evolution_architecture_v0.md` | Capture-owned | Capture authority with ECR/SCR pointer | `pointer_only` | ECR/SCR re-derive lifecycle | Ensure ECR/SCR does not fork packet doctrine |
| Packet payload split / attachment boundaries | `docs/product/data_capture_spine/source_capture_core_payload_split_explainer_v0.md`, `docs/product/data_capture_spine/source_capture_tenant_payload_attachment_boundary_v0.md` | Capture-owned | Capture authority with ECR/SCR pointers | `pointer_only` | Data lake, SourceCapturePacket | Pointer check |
| JSG-01 SP-6 plan/routing | `docs/product/judgment_spine/jsg01_sp6_source_visibility_derivation_architecture_plan_v0.md`, `docs/product/judgment_spine/jsg01_sp6_source_visibility_derivation_architecture_routing_v0.md` | Judgment boundary source | Judgment authority/workflow with ECR pointer | `pointer_only` | ECR SP-6 plan | No ECR absorption |
| Source-side receipt translator | `docs/product/judgment_spine/jsg01_source_side_receipt_translator_v0.md` | Judgment/provenance bridge | Judgment archive with ECR pointer | `historical_only` | ECR field-schema ratification | Mark superseded/provenance only |
| Judgment conductor and gate map | `docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md`, `docs/product/judgment_spine/judgment_spine_gate_ownership_map_v0.md` | Judgment-owned | Judgment spine authority with ECR/SCR pointers | `pointer_only` | JSG-01 unfreeze decision | No conductor move with ECR/SCR |
| JSG-01 decisions | `docs/decisions/jsg01_unfreeze_decision_v0.md`, `docs/decisions/jsg01_unfreeze_decision_memo_v0.md` | Judgment decision | Judgment/global decisions home with ECR pointer | `pointer_only` | Conductor, Evidence Binding | Preserve non-claims |
| Finalizer staffing decision | `docs/decisions/ar_01_pre_decision_status_finalizer_staffing_v0.md` | Judgment/SP-5 decision | Judgment/global decision home with ECR pointer | `pointer_only` | FinalizationReceipt | No SP-5 ownership transfer |
| Capture handoff obligation docs | `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md`, `docs/product/data_capture_spine/core_spine_v0_data_capture_context_preservation_note_v0.md`, `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md` | Capture-owned | Capture spine authority/workflows | `pointer_only` | Capture inventory, ECR handoff | Do not move with ECR/SCR |
| Cleaning/foundation adjacency | `docs/product/core_spine/core_spine_v0_cleaning_spine_readme_v0.md`, `docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md` | Cleaning/Foundation boundary | Cleaning/Foundation spine with ECR/SCR pointer | `pointer_only` | PR #245, PR #242 | Cleaning inventory owns moves |

## 2. ECR-Owned Surfaces

| Surface | Current path | Future allocation | Mark | Reason |
| --- | --- | --- | --- | --- |
| ECR integrity frame and SP-6 | `docs/product/ecr/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md` | ECR section of combined lane or separate ECR spine | `move_later` | ECR-owned integrity architecture. |
| ECR SP-1/SP-2/SP-3 reconcile | `docs/product/ecr/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md` | ECR section of combined lane or separate ECR spine | `move_later` | ECR-owned source-side fields. |
| ECR/JSG-01 binding slice plan | `docs/product/ecr/ecr_consolidation_v0_jsg01_evidence_unit_binding_slice_plan_v0.md` | Boundary subsection with Judgment pointer | `move_later` | Under ECR today, but must keep Judgment boundary. |
| ECR source-side code pointer | `orca-harness/ecr/__init__.py`, `models.py`, `deriver.py` | Pointer docs only under ECR harness area | `pointer_only` | Executable code must not move in this pass. |
| ECR unit tests | `orca-harness/tests/unit/test_ecr_*.py`, `_ecr_builders.py` | Pointer docs only under ECR tests area | `pointer_only` | Executable tests must not move in this pass. |

## 3. SCR-Owned Or SCR-Candidate Surfaces

| Surface | Current path | Future allocation | Mark | Reason |
| --- | --- | --- | --- | --- |
| SCR direction/architecture | `docs/product/signal_content/core_spine_v0_signal_content_record_architecture_v0.md` | Owner decision: combined SCR section, separate Signal Content spine, or Signal Statement spine if PR #237 lands | `owner_decision` | Current source says sibling content layer, not ECR-owned. |
| SCR deriver architecture | `docs/product/signal_content/signal_content_record_deriver_architecture_plan_v0.md` | Same as above | `owner_decision` | The deriver shares source-side discipline but has its own content-layer ownership. |
| SCR code | `orca-harness/signal_content/__init__.py`, `models.py`, `deriver.py` | Pointer docs only; future path may become `signal_statement` | `pointer_only` | Sibling implementation; no code move now. |
| SCR tests | `orca-harness/tests/unit/test_signal_content_models.py`, `test_signal_content_deriver.py` | Pointer docs only; future path may become `signal_statement` | `pointer_only` | Sibling tests; no code move now. |
| SCR review bundles | `docs/review-outputs/signal_content_v0_no_repo_review_bundle.zip`, `scr_architecture_no_repo_review_bundle.zip`, `scr_deriver_build_no_repo_review_bundle.zip` | SCR/Signal Statement archive | `historical_only` | Review/provenance bundles, not live authority. |
| SCR handoff prompt | `docs/prompts/handoffs/signal_content_record_deriver_architecture_ecr_lane_handoff_prompt_v0.md` | SCR/Signal Statement prompts with ECR pointer | `historical_only` | It says ECR lane, but the artifact commissioned SCR architecture. |

## 4. Shared ECR/SCR Surfaces

| Shared surface | Current source | Future allocation | Mark | Migration note |
| --- | --- | --- | --- | --- |
| Reference-never-merge invariant | `docs/workflows/ecr_spine_submap_v0.md` | Combined lane `authority/` or mirrored pointers in separate spines | `move_later` | Shared invariant should not be forked in both ECR and SCR. |
| Carry-supplied-or-residualize / never author from prose | ECR frame, SCR deriver plan, submap | Combined lane `authority/derived_record_discipline.md` or pointer docs | `owner_decision` | Useful reason to keep ECR/SCR together, but not enough to settle allocation. |
| Re-derive-not-migrate lifecycle | Capture schema evolution + ECR/SCR plans | Shared discipline pointer | `pointer_only` | Capture owns packet schema evolution; ECR/SCR inherit it. |
| SourceCapturePacket key boundary | Capture docs and `orca-harness/source_capture/` | Capture-owned with ECR/SCR pointers | `pointer_only` | Both ECR and SCR key to packet/slice; neither owns capture. |
| EvidenceUnit composition boundary | Boundary doc + Evidence Binding plan/code | ECR/Judgment boundary area | `pointer_only` | Do not use this to absorb Judgment or full Evidence Unit architecture. |

## 5. Used By ECR/SCR But Owned Elsewhere

| Surface family | Representative paths | Owner | Mark | Boundary |
| --- | --- | --- | --- | --- |
| Capture / raw packet production | `orca-harness/source_capture/**`, `docs/product/data_capture_spine/**`, `docs/workflows/data_capture_spine_consolidation_map_v0.md` | Capture | `pointer_only` | ECR/SCR consume SourceCapturePacket; they do not capture. |
| Cleaning | `docs/product/core_spine/core_spine_v0_cleaning_spine_readme_v0.md`, `docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md` | Cleaning/Foundation | `pointer_only` | Cleaning transforms after ECR/SCR; not redesigned here. |
| Judgment / JSG-01 | `docs/product/judgment_spine/**`, `docs/decisions/jsg01_unfreeze_*` | Judgment | `pointer_only` | JSG-01 consumes ECR outputs; ECR/SCR do not own conductor/gates. |
| SP-5 finalization | `docs/research/judgment-spine/sp5_finalization_receipt_spec_v0.md`, `orca-harness/schemas/finalization_models.py`, `orca-harness/runners/run_finalization_receipt.py` | Judgment/shared harness | `pointer_only` | Finalization is a separate JSG-01 subpredicate. |
| Global overlay/source loading | `.agents/workflow-overlay/source-loading.md`, `safety-rules.md`, `source-of-truth.md` | Global overlay | `do_not_move` | ECR/SCR may point to overlay rules, never relocate them. |
| Repo maps / structure maps | `docs/workflows/orca_repo_map_v0.md`, `repo-structure.yaml` | Global navigation/router | `do_not_move` | Future migration updates them; ECR/SCR does not own them. |

## 6. Prompts, Reviews, And Provenance

| Surface | Current path(s) | Allocation | Mark |
| --- | --- | --- | --- |
| ECR frame architecture prompt | `docs/prompts/architecture/ecr_consolidation_v0_frame_source_visibility_slice_architecture_prompt_v0.md` | ECR prompt archive | `move_later` |
| SP-6 architecture prompt | `docs/prompts/architecture/jsg01_sp6_source_visibility_derivation_architecture_prompt_v0.md` | ECR/Judgment boundary prompt archive | `move_later` |
| Packet schema evolution prompt | `docs/prompts/architecture/source_capture_packet_schema_evolution_architecture_prompt_v0.md` | Capture prompt archive with ECR/SCR pointer | `pointer_only` |
| ECR/JSG-01 lane setup prompt | `docs/prompts/handoffs/ecr_jsg01_source_side_receipt_lane_setup_v0.md` | ECR/Judgment historical prompt | `historical_only` |
| Bounded unfreeze build handoff | `docs/prompts/handoffs/ecr_jsg01_bounded_unfreeze_build_handoff_prompt_v0.md` | ECR/Judgment boundary prompt | `move_later` |
| SCR deriver handoff | `docs/prompts/handoffs/signal_content_record_deriver_architecture_ecr_lane_handoff_prompt_v0.md` | SCR/Signal Statement prompt archive | `historical_only` |
| ECR review prompts | `docs/prompts/reviews/ecr_jsg01_bind_vs_fork_cross_family_review_prompt_v0.md`, `docs/prompts/reviews/ecr_consolidation_v0_plan_cross_family_review_patch_prompt_v0.md` | ECR review prompt archive | `historical_only` |
| Translator review prompt | `docs/prompts/reviews/jsg01_source_side_receipt_translator_adversarial_review_prompt_v0.md` | Judgment/ECR historical prompt | `historical_only` |
| Schema-evolution review prompt | `docs/prompts/reviews/source_capture_packet_schema_evolution_architecture_adversarial_artifact_review_prompt_v0.md` | Capture review prompt with ECR/SCR pointer | `pointer_only` |
| ECR review outputs | `docs/review-outputs/adversarial-artifact-reviews/ecr_consolidation_v0_plan_cross_family_review_v0.md`, `ecr_consolidation_v0_frame_source_visibility_slice_architecture_prompt_adversarial_review_v0.md`, `ecr_consolidation_v0_sp1_sp2_sp3_source_side_reconcile_cross_family_review_v0.md`, `ecr_jsg01_evidence_unit_binding_plan_delegated_adversarial_artifact_review_patch_v0.md` | ECR reviews/provenance | `historical_only` |
| Evidence Binding review output | `docs/review-outputs/adversarial-artifact-reviews/evidence_binding_slice_delegated_adversarial_code_review_patch_v0.md` | Shared harness/Judgment with ECR pointer | `historical_only` |
| Translator review output | `docs/review-outputs/adversarial-artifact-reviews/jsg01_source_side_receipt_translator_adversarial_review_v0.md` | Judgment/ECR provenance | `historical_only` |
| SP-5 review output | `docs/review-outputs/adversarial-artifact-reviews/sp5_finalization_producer_delegated_adversarial_code_review_patch_v0.md` | Judgment/shared harness | `historical_only` |
| SCR review bundles | `docs/review-outputs/signal_content_v0_no_repo_review_bundle.zip`, `scr_architecture_no_repo_review_bundle.zip`, `scr_deriver_build_no_repo_review_bundle.zip` | SCR/Signal Statement archive | `historical_only` |

Review outputs are provenance, not live authority, unless a later owner source
explicitly promotes or routes through them.

## 7. Runtime, Code, Test, And Fixture Surfaces

No executable code or tests move in this pass.

| Runtime/test surface | Current path | Allocation | Mark | Validation if moved later |
| --- | --- | --- | --- | --- |
| ECR package | `orca-harness/ecr/__init__.py`, `models.py`, `deriver.py` | Shared harness, ECR pointer docs | `pointer_only` | ECR unit subset, import path checks, no-LLM/import checks |
| ECR tests/builders | `orca-harness/tests/unit/test_ecr_*.py`, `orca-harness/tests/unit/_ecr_builders.py` | Shared harness tests, ECR pointer docs | `pointer_only` | Unit subset and helper import checks |
| SCR package | `orca-harness/signal_content/__init__.py`, `models.py`, `deriver.py` | Shared harness, SCR pointer docs | `pointer_only` | Signal content/statement tests, import path checks |
| SCR tests | `orca-harness/tests/unit/test_signal_content_models.py`, `test_signal_content_deriver.py` | Shared harness tests, SCR pointer docs | `pointer_only` | Signal tests; rename checks if PR #237 lands |
| Evidence Binding package | `orca-harness/evidence_binding/__init__.py`, `models.py`, `composer.py`, `verifier.py` | Shared harness/Judgment boundary with ECR pointer | `pointer_only` | `test_evidence_binding.py`, verifier tests, no aggregate verdict checks |
| Finalization runtime | `orca-harness/schemas/finalization_models.py`, `orca-harness/runners/run_finalization_receipt.py` | Shared harness/Judgment SP-5 | `pointer_only` | Finalization model, contract, and runner tests |
| JSG-01 binding proof case | `orca-harness/cases/product_learning/jsg01_binding_assembly_proof_v0/evidence/finalization_receipts.yaml` | Judgment/ECR provenance | `historical_only` | Case-path rewrite only under case migration; preserve non-claims |
| Broad source-capture case receipts | `orca-harness/cases/product_learning/**/source_captures/**/{receipt.md,manifest.json}` | Capture/case provenance | `do_not_move` | Capture/case inventory owns any moves |

## 8. Stale Naming Or Stale Placement Risks

| Risk | Evidence | Required handling |
| --- | --- | --- |
| Evidence Capture Record vs Evidence Candidate Record | Search found live controlling docs and code using `Evidence Candidate Record`; no controlling `Evidence Capture Record` hit was found. | Do not rename ECR in this migration. Mark "Evidence Capture Record" as user-facing/ambiguous wording until owner settles name. |
| Signal Content Record vs Signal Statement Record | PR #237 is open and renames active Signal Content/SCR surfaces to Signal Statement Record. | Do not move SCR until PR #237 lands or closes. Future targets must be conditional. |
| `docs/product/core_spine/` vs Foundation | PR #242 is open and may move boundary/IPF/data-lake files. | Use pointers until Foundation rename settles. |
| Spine-first root not live | PR #239 is open; `orca/product/spines/<spine>/` is proposed, not live. | No source moves now. Future migration package should wait for binding. |
| ECR-only inventory now incomplete for this lane | `docs/migration/ecr_spine_first_migration_inventory_v0.md` predates this ECR+SCR inventory. | Treat ECR-only inventory as predecessor/provenance; use this file for combined ECR/SCR source-side lane. |
| Prompt names say ECR lane for SCR work | `signal_content_record_deriver_architecture_ecr_lane_handoff_prompt_v0.md` commissions SCR work through an ECR lane. | Mark as historical/provenance; do not infer SCR is ECR-owned. |
| Review bundles are zip files | SCR/ECR no-repo review bundles under `docs/review-outputs/*.zip`. | Keep as historical/provenance; do not unpack or make authoritative during migration. |

## 9. Open Questions For Owner

1. Should SCR be a module under the ECR source-side spine?
2. Should SCR be a sibling derived-record surface inside a shared ECR/SCR source-side spine?
3. Should SCR be a separate future spine, especially if PR #237 lands as Signal Statement Record?
4. Should SCR be treated as a shared substrate consumed by ECR and Judgment rather than a spine?
5. Is **Evidence Candidate Record** the retained canonical expansion for ECR, or should owner explicitly rename it?
6. If ECR and SCR share one future spine, what is the spine slug: `ecr_scr_source_side`, `source_side_derived_records`, `ecr`, or another owner-selected name?
7. Should review bundles move with their target spine, or stay in a global review archive with moved-path pointers?
8. Should shared harness pointer docs be created before any docs move, or should code-root migration be handled in a separate later package?

## 10. Suggested Migration Order

1. Wait for the global spine-first structure binding to land or be rejected. Do not move ECR/SCR before PR #239 or its successor is resolved.
2. Wait for Signal Content vs Signal Statement naming to settle. PR #237 is directly path-breaking for SCR docs, code, tests, and references.
3. Wait for Foundation rename status. PR #242 affects the boundary/IPF/data-lake sources that ECR and SCR cite.
4. Owner selects SCR allocation: under ECR, sibling in combined source-side spine, separate spine, or shared substrate.
5. Create pointer skeletons only: README, `spine.yaml`, `authority/pointers/`, `harness/`, and `tests/`. No source moves yet.
6. Move docs/prompts/reviews in one bounded package with a moved-path index and stale-reference search.
7. Leave executable code under `orca-harness/` unless a separate code-root migration is accepted. If accepted later, move code/tests together with import and pytest verification.
8. Update global repo map and source-loading pointers after moves, not before.

## 11. Explicit Non-Claims

- Not a file move, code move, rename, doctrine change, or implementation.
- Not validation, readiness, ratification, proof, buyer proof, fixture admission, or judgment-quality evidence.
- Not a claim that SCR is ECR-owned.
- Not a claim that SCR is already a separate spine.
- Not a claim that Signal Statement Record has landed on `main`.
- Not a claim that ECR means Evidence Capture Record; current repo source says Evidence Candidate Record.
- Not Capture redesign, Cleaning redesign, Judgment redesign, or conductor modification.
- Not ownership transfer for SourceCapturePacket, source capture runners, Cleaning, JSG-01, SP-5 finalization, Evidence Binding, or the final Evidence Unit architecture.
- Not authority promotion for review outputs or no-repo zip bundles.
- Not authorization to run ECR/SCR tests; no code was touched.
