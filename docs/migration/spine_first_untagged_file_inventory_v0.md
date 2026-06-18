# Spine-First Untagged File Inventory v0

```yaml
retrieval_header_version: 1
artifact_role: Orca migration inventory record (untagged/tagging-queue marking artifact)
scope: >
  The files and structural decisions the controller and its inventory subagents
  could not place confidently into the spine-first target tree, collected for
  main-CA tagging before migration execution. Each entry names why it is untagged,
  the likely owner candidates, what source would settle it, whether it blocks the
  move table, and a file:line citation (or "no durable citation found"). Inventory
  only: no file moved, renamed, created, or deleted.
use_when:
  - Adjudicating the unplaced files before the spine-first migration executes.
  - Checking whether a tagging decision blocks the move table or is deferrable.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_spine_first_target_structure_binding_v0.md
  - docs/decisions/orca_spine_first_blocker_authorization_v0.md
  - docs/migration/spine_first_target_move_table_v0.md
stale_if:
  - The owner/main-CA tags a listed item (move it to a settled row in the move table).
  - The bound target tree or a convention changes.
  - A sibling per-lane inventory lands and resolves a shared-surface ambiguity.
```

## Status & base

- Status: `INVENTORY_ONLY_V0`. Read against `origin/main @ 8f19b460` (clean).
- These are tagging items for the main CA / owner, not controller decisions. The
  controller proposed a leading candidate in the move table; here it records why
  the call is not confident and what would settle it.
- "Blocks move table?" = whether the migration execution can proceed for that
  surface without the tag. Structural blockers (B1–B7) block broadly; per-file
  ambiguities usually block only their own row.
- Post-merge blocker settlement:
  `docs/decisions/orca_spine_first_blocker_authorization_v0.md` settles B1-B7
  for execution and gives defaults for several per-file ambiguity classes.
  Apply that record before treating these rows as still blocked.

## A. Structural / doctrine tags (block broadly)

| ID | Item | Why untagged | Likely owners | What settles it | Blocks? | Cite |
| --- | --- | --- | --- | --- | --- | --- |
| B1 | `orca/` top-level root | Absent from `known_top_level`; creating it is a root-layout change EP-04 would flag unplaced | owner + repo-structure binding | An amendment authorizing `orca/` in `repo-structure.yaml` + `artifact-folders.md` | **Yes — blocks all `orca/product/` moves** | `repo-structure.yaml:23-30` |
| B2 | Search-lane physical reversal | Dissolving `search/` reverses an owner-adopted binding landed days earlier (#236/#241) | owner | Explicit owner confirmation that spine-first placement supersedes the search-lane home (authority of method docs preserved) | **Yes — blocks Section 3a** | `docs/decisions/orca_search_product_lane_binding_v0.md:43-62` |
| B3 | `docs/doctrine/` vs `docs/decisions/` boundary | Target adds `doctrine/` while keeping `decisions/`; the doctrine **index** already lives in `decisions/`; no source defines membership | owner + artifact-folders | A rule defining what is "doctrine" vs "decision", or dropping the new folder | Yes — blocks any `docs/doctrine/` population (no product file depends on it) | `docs/decisions/orca_doctrine_index_v0.md` (exists) |
| B4 | `ontology_expansion_backlog_v0.json` hook coupling | Read by `.agents/hooks/check_ontology_expansion.py`; a move breaks the path (runtime-adjacent, not docs-only) | owner + hook maintainer | A paired hook-path rewrite authorized alongside the move | Yes — blocks the JSON's row | `docs/product/core_spine/ontology_expansion_backlog_v0.json:3` |
| B5 | Commission Signal Board has no doc home | CSB is "structure, not built runtime"; only precursor is the gate-run commission criteria (in `search/`) | owner | Decide: relocate the gate-run criteria into `commission_signal_board/`, or author a first CSB artifact | Partial — blocks Section 11 + the gate-run criteria row | `docs/product/search/orca_demand_gate_run_commission_criteria_v0.md:4` |
| B6 | Toolbox-vs-Armory name + IG-lane status | Folder/title say both "Toolbox" and "Armory"; IG has 13 docs + creator specs but **no lane binding** | owner | A naming decision + an IG-lane decision (bind a lane, or keep IG under Capture/Toolbox) | Partial — blocks the toolbox-unit row + IG family row | capture inv §6,§11–12 (`docs/migration/capture_spine_source_capture_migration_inventory_v0.md:121,159`) |
| B7 | Sibling inventories not on main | Cleaning, ecr, foundation, ontology, product-lead/buyer-proof, global-prompt-review per-lane inventories are in-flight | their lanes + controller | Those inventories landing; then re-reconcile against this binding | Advisory — does not block, but their classifications may revise rows | search inv §"Companion wave" (`docs/migration/search_demand_signal_migration_inventory_v0.md:39-43`) |

Post-merge status: the structural rows above are settled by
`docs/decisions/orca_spine_first_blocker_authorization_v0.md`. The rows remain
visible as historical blocker origins and execution reminders, not as reasons to
stop before applying the authorization record.

## B. Per-file placement tags (block their own row only)

| ID | File | Why untagged | Likely owners | What settles it | Cite |
| --- | --- | --- | --- | --- | --- |
| U-F1 | `core_spine/core_spine_v0_proof_input_selection_v0.md`, `…proof_packet_preflight_v0.md`, `…method_validation_rubric_v0.md` | Proof-method/protocol-definition vs proof-corpus/validation-machinery | `foundation/product_contract/` vs `case_families/product_learning/` | Owner ruling on whether proof setup/gates are method (foundation) or corpus | `…proof_input_selection_v0.md:13-30` |
| U-F2 | `core_spine/ontology_cards/` beauty/fragrance instance cards (brand_beautypie, case/decision/outcome_beautypie_repricing_2023, venue_basenotes, vertical_beauty) | Ontology infrastructure (governed by backbone) vs beauty-domain instances | `foundation/ontology/ontology_cards/` vs `satellites/beauty/` | Owner ruling: are domain instance cards ontology-infra or satellite content? | `core_spine/ontology_cards/README.md:12` |
| U-F3 | `core_spine/core_spine_v0_first_proof_run_charter_v0.md` | Cross-domain proof-run charter: method machinery vs corpus setup | `foundation/product_contract/` vs `case_families/product_learning/` | Owner ruling (same axis as U-F1) | `…first_proof_run_charter_v0.md:1-5` |
| U-J1 | `judgment_spine/fragrance_level1_product_learning_reconciliation_v0.md` | Machinery-by-role (reconciles pack against the spine) but fragrance-by-subject; convention #4 vs the named `reconciliation/` slot | `judgment/product_learning/` vs `satellites/fragrance/judgment_level1/reconciliation/` | Owner ruling on which convention governs reconciliation artifacts | `…fragrance_level1_product_learning_reconciliation_v0.md:5,52-58` |
| U-J2 | `judgment_spine/judgment_current_state_and_decomposition_v0.md` | Cross-cutting orientation map with no single sub-area anchor | `judgment/conductor/` vs a `judgment/` root | Owner/main-CA decision on whether orientation maps get a root slot | `…judgment_current_state_and_decomposition_v0.md:5-6` |
| U-J3 | `judgment_spine/judgment_spine_reveal_calibration_owner_contract_v0.md` | JSG-08 gate contract vs lifecycle-phased product-learning slot | `judgment/conductor/` vs `judgment/product_learning/reveal_evaluation/` | Owner ruling: conductor reserved for sequence/routing only? | `…judgment_spine_reveal_calibration_owner_contract_v0.md:6` |
| U-J4 | `judgment_spine/conductor_construction_integrity_probe_addendum_proposal_v0.md` | SUPERSEDED + BLOCKED; retained for review history | `judgment/conductor/` vs a `conductor/archive/` | Owner policy on superseded-doc co-location vs archive sub-folder | `…conductor_construction_integrity_probe_addendum_proposal_v0.md:30-33` |
| U-PL1 | `product_lead/orca_claim_defense_doctrine_v0.md` | Owner-signed external-claims policy; subordinate to the evidence ladder | `product_lead/proof_charter/` vs `judgment/` | Owner ruling on claims-doctrine ownership | `…orca_claim_defense_doctrine_v0.md:3,11` |
| U-PL2 | `product_lead/orca_icp_ratification_readiness_report_v0.md`, `…orca_ratification_day_runbook_v0.md`, `…orca_discovery_consumer_demand_target_selection_brief_v0.md` | Lane-process / discovery instruments, not ICP-wedge decisions; no `process/` or `discovery/` sub-slot in the tree | `product_lead/icp_wedge/` vs a new sub-slot | Owner decision: accept `icp_wedge/` catch-all or add a sub-slot | `…orca_icp_ratification_readiness_report_v0.md:4` |
| U-PL3 | `product_lead/orca_discovery_batch_0_{candidate_context_scan,qualification_prep_sentry_clerk,target_selection_brief}_v0.md` | SUPERSEDED / OFF-TARGET (pricing-first era) | `product_lead/icp_wedge/` (historical) vs an archive | Owner policy on migrating dead-lane history into the active spine | `…orca_discovery_batch_0_target_selection_brief_v0.md:3` |
| U-C1 | `data_capture_spine/` pressure-test slot sessions (~12: slot1_mi_biws, slot2_teal, slot3 reddit/wso batches, syntheses, commissioning_plan, execution_authorization) | Capture-spine operational evidence vs capture-case-family corpus | `capture/operating_model/` vs `case_families/` | Owner ruling on capture-evidence vs case-family boundary | capture inv §11.6 (`…capture_spine_source_capture_migration_inventory_v0.md:163`) |
| U-C2 | `source_capture_toolbox/ig_*` (13) + `data_capture_spine/orca_creator_{momentum_pipeline,monitoring_policy}_architecture_v0.md` | IG held under Capture/Toolbox but no IG lane binding (cf. search got one) | `capture/source_families/instagram/` vs a new IG lane | Owner IG-lane decision (B6) | capture inv §6 (`…:121-127`) |
| U-CF1 | The `other_verticals` catch-all (method-validation + first-proof + heavyweight-discovery corpora, ~19 files) | Target `case_families/product_learning/` has only `{fragrance, retail_pdp, other_verticals}`; all SaaS/tech cases fall to `other_verticals` | owner | Confirm `other_verticals` as the accepted catch-all, or add a `saas_competitive/` (or similar) sub-folder | `core_spine/core_spine_v0_method_validation_case_locks_v0.md:17-21` |
| U-CF2 | `core_spine/core_spine_v0_first_proof_run_jb_client0_slice_v0.md` | jb = finance-career/job-board domain; `retail_pdp` sub-folder is a poor fit | `case_families/product_learning/other_verticals/` vs `retail_pdp/` | Owner ruling on where non-fragrance/non-retail cases land | `…first_proof_run_jb_client0_slice_v0.md:4-7` |
| U-CF3 | `core_spine/consumer_demand_candidate_pool_handoff_v0.md` | One-shot beauty discovery handoff: corpus vs domain output | `case_families/product_learning/fragrance/` vs `satellites/beauty/` | Owner ruling (corpus vs satellite frame) | `…consumer_demand_candidate_pool_handoff_v0.md:7-13` |
| U-S1 | `docs/product/search/README.md` | The lane README has no target home once `search/` dissolves | retire vs seed scanning/+foundation READMEs | Owner decision at dissolution (B2) | search inv §1 (`docs/migration/search_demand_signal_migration_inventory_v0.md:75`) |
| U-CASE | `orca-harness/cases/product_learning/` (~14) + `cases/plumbing/` | Runtime case corpora mapping owned by a (pending) case-family inventory | case-family inventory + owner | The case-family inventory landing | capture inv §10 (`…:151-154`) |

## C. Empty target slots (structure ahead of content — not files, noted for completeness)

These target directories have **no current doc** mapping to them; they are
structure the owner accepted ahead of content. Not blockers; flagged so the
migration controller does not treat their emptiness as a coverage gap.

- `foundation/evidence_standard/` (IPF carries the standard but no separate doc),
  `foundation/shared_primitives/`.
- `cleaning/{transformations, integrity_labels, normalization}/`.
- `judgment/product_learning/{forecast_records, decision_logs, receipts}/`;
  `satellites/fragrance/judgment_level1/{source_registry, evaluation_artifacts}/`.
- `commission_signal_board/{commission_contract, signal_board, dispatch_rules, work_orders}/`
  (B5).
- `capture/source_families/{youtube, tiktok}/` and `scanning/source_families/{youtube, tiktok, instagram}/`
  (no YT/TT docs found; IG docs are capture-side per U-C2).

## Non-claims

- Inventory only. No file moved/renamed/created/deleted; no `orca/` tree created;
  no code/tests/imports/hooks touched. Tags are for owner/main-CA adjudication.
- Not validation, readiness, proof, or migration authorization.
- Leading-candidate target homes recorded here and in the move table are
  proposals, not authority transfers; the owner and the spine-first binding govern.
