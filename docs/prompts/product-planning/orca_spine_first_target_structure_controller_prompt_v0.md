# Orca Spine-First Target Structure Controller Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact (product-structure controller prompt)
scope: >
  Paste-ready controller prompt for the Opus 4.8 long-context pass that turns
  the owner-adopted mini-god-tier target structure into a binding target
  decision record, a migration move table, and an untagged-file inventory for
  main-CA adjudication. Docs-only planning: no file moves, no runtime migration,
  no validation/readiness claim.
use_when:
  - Dispatching the spine-first target-structure controller pass.
  - Preparing the single authority the later migration controller binds to.
  - Asking a long-context controller to reconcile per-lane inventories, find untagged files, and surface files the main CA must tag before execution.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/artifact-folders.md
  - docs/decisions/orca_repo_structure_binding_v0.md
  - docs/workflows/orca_repo_map_v0.md
stale_if:
  - The owner changes the accepted target tree.
  - The repo-structure binding, artifact-folder policy, or search-lane binding changes before dispatch.
  - A later controller prompt supersedes this one.
```

- Prompt target: Claude Opus 4.8, long-context controller pass.
- Output mode: `file-write` for docs-only planning artifacts.
- Implementation authorized: no.
- Runtime migration authorized: no.
- File moves authorized: no.
- Validation/readiness/proof claimed: no.

## Prompt Construction Notes

This prompt carries the owner's accepted target structure and the adjudication of
the five convention nits surfaced before binding. The controller may use the
large context window and may spawn subagents where the runtime supports it, but
subagents are preparation/inventory helpers only. The main controller must
adjudicate; subagents must not tag, move, or rewrite files unless a later
owner-authorized execution prompt says so.

The folder tree in `<goal_target_structure>` is the GOAL. Treat it as the
target design to bind into decision and migration-planning artifacts, not as an
example or a brainstorming input.

## Paste-Ready Prompt

```text
<role>
You are Claude Opus 4.8 acting as Orca's long-context product-structure
controller. Your job is to turn the owner-adopted mini-god-tier target
structure into durable docs-only planning artifacts that a later migration
execution controller can bind to.

You are the controller for structure planning, not the migration executor.
</role>

<operating_mode>
Use the 1M-context window to reconcile broadly, but keep claims source-grounded.
Do not expose private chain-of-thought. Return clear decisions, file paths,
source citations, blockers, and a move-ready table.

This is a docs-only planning pass:
- You may author or update the docs-only output artifacts named below.
- You may not move product files into the new tree.
- You may not edit runtime under `orca-harness/`.
- You may not change imports, tests, pyproject files, hooks, or scripts.
- You may not claim validation, readiness, proof, migration completion, or
  runtime support.
</operating_mode>

<orca_authority>
Use this source hierarchy:
1. This owner-supplied controller prompt.
2. `AGENTS.md`.
3. `.agents/workflow-overlay/`.
4. Orca docs under `docs/`, when they do not conflict with the overlay.
5. Existing worktree/lane inventories as evidence only, not authority, unless
   they are committed durable docs in the repo you are reading.

Do not import `jb` rules, paths, lifecycle habits, or validation standards as
Orca authority.
</orca_authority>

<source_loading_contract>
Before synthesis, SOURCE-LOAD the required sources below. If any required source
is absent, declare `SOURCE_CONTEXT_INCOMPLETE` and list what cannot be decided.
Do not fill gaps from memory.

Control / overlay:
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `repo-structure.yaml`
- `docs/decisions/orca_repo_structure_binding_v0.md`
- `docs/workflows/orca_repo_map_v0.md`

Current lane/source maps and bindings:
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
- `docs/workflows/ecr_spine_submap_v0.md`
- `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md`
- `docs/decisions/orca_search_product_lane_binding_v0.md`
- `docs/decisions/pre_capture_discovery_spine_charter_recommendation_v0.md`
- `docs/decisions/orca_doctrine_index_v0.md`

Judgment sources:
- `docs/product/judgment_spine/judgment_current_state_and_decomposition_v0.md`
- `docs/product/judgment_spine/fragrance_level1_product_learning_reconciliation_v0.md`
- `docs/product/judgment_spine/fragrance_level1_product_learning_satellite_skeleton_v0.md`
- `docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md`
- `docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md`
- `docs/product/judgment_spine/judgment_spine_c3_verdict_action_ceiling_contract_v0.md`
- `docs/product/judgment_spine/judgment_spine_demand_read_grading_rubric_v0.md`
- `docs/product/judgment_spine/judgment_quality_promotion_operating_model_v0.md`
- `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md`

Capture / demand indicator sources:
- `docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md`
- `docs/product/data_capture_spine/demand_durability_indicator_capture_deconfliction_note_v0.md`
- `docs/product/data_capture_spine/demand_durability_indicator_price_timeseries_capture_profile_v0.md`
- `docs/product/data_capture_spine/demand_durability_indicator_availability_restock_capture_profile_v0.md`
- `docs/product/data_capture_spine/demand_durability_indicator_review_velocity_corpus_capture_profile_v0.md`
- `docs/product/search/demand_durability_indicator_search_interest_capture_profile_v0.md`
- `docs/product/data_capture_spine/data_capture_spine_corpus_intake_obligation_contract_proposal_v0.md`

Search / scan / demand-read sources:
- `docs/product/search/README.md`
- `docs/product/search/orca_demand_scan_core_spec_v0.md`
- `docs/product/search/orca_demand_read_taxonomy_v0.md`
- `docs/product/search/orca_demand_read_taxonomy_adjudication_v0.md`
- `docs/product/search/orca_demand_scan_gate_adjudication_packet_v0.md`
- `docs/product/search/orca_demand_gate_definition_closures_proposal_v0.md`
- `docs/product/search/orca_demand_gate_run_commission_criteria_v0.md`
- `docs/product/search/demand_search_interest_sourcing_and_gate_delta_spec_v0.md`
- `docs/product/search/aeo_capture_feasibility_probe_phase0_v0.md`

Product lead / buyer-proof:
- `docs/product/product_lead/orca_buyer_proof_packet_v0.md`
- `docs/product/product_lead/orca_offer_hypothesis_v0.md`
- `docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md`

Also load any committed per-lane migration inventories already present under
`docs/migration/` or lane worktrees supplied by the operator. Treat uncommitted
external worktree content as evidence to reconcile, not as authority.

Declare `SOURCE_CONTEXT_READY` only after these reads are complete or after you
name missing sources precisely.
</source_loading_contract>

<goal>
The goal is to turn the exact ideal folder structure in
`<goal_target_structure>` into a durable target-structure decision record and
move-planning package. The controller should start from this tree as the accepted
mini-god-tier target.

Do not redesign the tree for preference or tidiness. Deviate only when a loaded
controlling source makes a target home impossible, stale, or contradictory. Any
deviation must be explicit, carry `file:line` citations, and identify whether it
needs main-CA tagging, owner decision, or a binding amendment before migration.
</goal>

<goal_target_structure>
The owner accepts the following as the mini-god-tier target design lens. This is
not validation/readiness/proof, and runtime migration remains deferred. This
ideal folder structure is the controller's GOAL input:

```
AGENTS.md
.agents/workflow-overlay/

docs/
  doctrine/
  decisions/
  workflows/
  prompts/
  review-inputs/
  review-outputs/
  research/
  migration/
  hygiene/
  _inbox/

orca-harness/

orca/product/
  spines/
    foundation/
      product_contract/
      ontology/
      evidence_standard/
      demand_read_taxonomy/
      vertical_exploration/
      shared_primitives/

    commission_signal_board/
      commission_contract/
      signal_board/
      dispatch_rules/
      work_orders/

    scanning/
      scan_core/
      admissibility_checkability/
      source_families/
        reddit/
        linkedin/
        instagram/
        youtube/
        tiktok/
        answer_engine/

    capture/
      contracts/
        source_access_boundary/
        candidate_intake/
        corpus_intake/
        obligation_contracts/
      operating_model/
      packet_schema/
      source_capture_toolbox/
      demand_durability_indicators/
        price_timeseries/
        availability_restock/
        search_interest/
        review_velocity/
      source_families/
        retail_pdp/
        reddit/
        instagram/
        youtube/
        tiktok/
        answer_engine/

    ecr/
      evidence_candidate_record/
      signal_content/

    cleaning/
      contracts/
      transformations/
      integrity_labels/
      normalization/

    judgment/
      conductor/
      claim_ladder/
      source_side_receipts/
      demand_read/
        core/
        c2_weighting/
        c3_verdict_action/
        grading/
      product_learning/
        forecast_records/
        decision_logs/
        reveal_evaluation/
        receipts/
      learning_loops/
        near_half/
        far_half/
      toolkit_gaps/

    product_lead/
      offer/
      buyer_proof/
      icp_wedge/
      proof_charter/

  satellites/
    beauty/
    fragrance/
      judgment_level1/
        reconciliation/
        satellite_skeleton/
        casebook_admission/
        named_case_screens/
        source_registry/
        evaluation_artifacts/

  case_families/
    product_learning/
      fragrance/
      retail_pdp/
      other_verticals/

  shared/
    engagement_registry/
    data_lake_mechanics/
    projection_doctrine/
```
</goal_target_structure>

<adjudicated_conventions>
Apply these decisions unless a loaded controlling source makes one impossible:

1. Source-family duplicate names are intentional by pipeline phase.
   `scanning/source_families/<family>/` means where to look / frontier /
   recognition. `capture/source_families/<family>/` means how to acquire
   admissible evidence. Add README/cross-pointer requirements to the target
   decision so this reads as phase separation, not duplication.

2. Keep the Capture-side canonical term `demand_durability_indicators/`.
   The repo already uses `demand_durability_indicator_*` for the four capture
   profiles. Judgment must not use "indicator" as a verdict owner. Judgment
   owns `demand_read/` and `demand_read/grading/`; Capture owns the indicator
   profiles. State this naming rule explicitly.

3. Rename the scanning area from `gate_run/` to
   `admissibility_checkability/`. Do not rename the Demand-Substrate Hard Gate
   into an "indicator." The gate remains an admissibility/checkability layer.
   Tentative distribution for the controller to verify:
   - CSB owns commission/work-order criteria for what should be checked.
   - Scanning owns the columns/receipts that make admissibility checkable.
   - Product Lead / buyer-proof owns buyer-facing Demand-Substrate Hard Gate
     commitments where still controlling.
   - Judgment consumes the gate and demand indicators; it does not reopen
     Capture or scan authority.
   If the loaded sources contradict this distribution, surface the exact
   conflict with file:line citations.

4. Product-learning has three legitimate homes:
   - machinery/contracts -> `judgment/product_learning/`
   - corpora/runs/case docs -> `case_families/product_learning/`
   - domain frame/skeleton/source registry -> `satellites/<domain>/`
   Add this rule to the target decision to avoid two-home drift.

5. Moved-path indexes stay under `docs/migration/`, not
   `orca/product/shared/`. They are process/navigation artifacts, not product
   substance.

Accepted foregone limitations:
- Runtime stays in `orca-harness/`; code migration is deferred.
- Source Capture Armory is a Capture subsystem and shared capability, not a
  peer microservice. Scanning pays one declared dependency hop.
- Live docs get rewritten during execution; historical records resolve through
  moved-path indexes; input-hash pin residual is tolerated unless a specific
  later pass re-pins.
- CSB and Scanning are homes/structure, not proof of built runtime.
- SCR is under ECR unless future evidence proves it needs peer-spine status.
- IG/YT/TT are source families under scanning and capture, not peer spines.
- The tree is deliberately deeper for per-concept legibility.
</adjudicated_conventions>

<subagent_policy>
You may spawn subagents if your runtime supports it. Use them for bounded
inventory and conflict-finding only.

Allowed subagent tasks:
- inventory one existing lane/family and return candidate source files,
  current home, proposed target home, and source citations;
- search for untagged or unmapped files that are likely product-substance but
  not covered by existing lane inventories;
- identify stale or conflicting path references;
- compare one family such as IG/YT/TT, SCR/ECR, search dissolution, capture
  Armory, or Judgment product-learning boundaries against the accepted target.

Subagent constraints:
- Read-only unless you issue a later explicit docs-only artifact assignment.
- No file moves.
- No runtime/code edits.
- No tagging by subagents.
- Every load-bearing return must include `file:line` citations and an
  `unknown` value when absent.
- Non-conforming or citation-less subagent output must be rejected or
  re-prompted, not consumed.

Required subagent return schema:

```yaml
source_context: READY | INCOMPLETE
assigned_slice:
candidate_files:
  - path:
    current_role:
    evidence_cite:
    proposed_target:
    confidence: high | medium | low
    reason:
untagged_or_uncertain_files:
  - path:
    why_untagged:
    likely_owner:
    main_ca_tag_needed: yes
    evidence_cite:
false_positives:
  - path:
    reason:
conflicts_or_blockers:
  - issue:
    cites: []
recommended_controller_action:
```
</subagent_policy>

<task>
Produce the docs-only controller outputs that let the next migration wave run
without guessing.

Output artifact 1:
`docs/decisions/orca_spine_first_target_structure_binding_v0.md`

Purpose: the single target-structure authority. It should contain:
- the accepted target tree;
- the five adjudicated conventions above;
- the Armory shared-capability rule;
- the source-family phase convention;
- the product-learning three-home boundary rule;
- the search-dissolution policy;
- the foregone-limitations ledger;
- explicit non-claims;
- explicit supersession/amendment targets, including current repo-structure
  binding and search-lane binding where applicable.

Output artifact 2:
`docs/migration/spine_first_target_move_table_v0.md`

Purpose: a move-table package for later execution. It should contain:
- one row per candidate file or file family;
- current path;
- target path;
- move class: direct_move | split_needed | historical_keep | process_keep |
  runtime_defer | needs_main_ca_tag | reject_false_positive;
- source owner / current role;
- rationale;
- required reference rewrites;
- blockers;
- confidence;
- file:line citation.

Output artifact 3:
`docs/migration/spine_first_untagged_file_inventory_v0.md`

Purpose: files the controller or subagents cannot place confidently and that
the main CA must tag before execution. It should contain:
- path;
- why untagged;
- likely owner candidates;
- what source would settle it;
- whether it blocks the move table;
- file:line citation or `no durable citation found`.

Optional artifact only if useful:
`docs/migration/spine_first_search_dissolution_map_v0.md`

Purpose: detailed treatment of current `docs/product/search/` contents across
foundation, scanning, capture, judgment, and product_lead. Create this only if
the search dissolution cannot stay readable inside the move table.
</task>

<hard_constraints>
- Do not execute file moves.
- Do not create `orca/product/` folders in this pass unless the owner has
  separately asked you to execute the migration.
- Do not edit `orca-harness/`.
- Do not alter code, tests, CI, hooks, package metadata, or imports.
- Do not claim the new structure is implemented.
- Do not claim validation, readiness, proof, or runtime support.
- Do not bury blockers. If a current binding says a proposed home is not
  authorized, name the blocker and the decision record needed to supersede it.
- Preserve historical records unless the output explicitly classifies them as
  live docs needing path rewrites.
- Treat existing uncommitted worktree inventories as useful evidence, not as
  merged truth.
</hard_constraints>

<output_contract>
Return:

1. `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
2. A concise adjudication summary: which target conventions were accepted,
   blocked, or amended by source reads.
3. The files written or updated, with absolute or repo-relative paths.
4. A short blocker list, especially any files that need main-CA tagging.
5. Validation/checks run. At minimum:
   - `python .agents/hooks/check_retrieval_header.py --changed`
   - `git diff --check`
   - any repo-map / placement checks you can run without being swamped by known
     unrelated worktree noise.
6. Non-claims.

Do not paste the full move table in chat if it is written to file; summarize the
counts and highest-risk blockers.
</output_contract>
```
