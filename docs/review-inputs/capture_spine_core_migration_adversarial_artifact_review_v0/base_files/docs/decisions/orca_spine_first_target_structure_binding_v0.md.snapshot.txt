# Orca Spine-First Target Structure Binding v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: >
  The single target-structure authority for Orca's spine-first product
  reorganization. Binds the owner-adopted mini-god-tier target tree (rooted at
  orca/product/), the five adjudicated conventions, the Source Capture Toolbox
  shared-capability rule, the source-family phase convention, the
  product-learning three-home rule, the search-dissolution policy, and the
  foregone-limitations ledger. Target design only: it does NOT move files, does
  NOT amend repo-structure.yaml yet, and is NOT validation/readiness/proof or a
  runtime-migration authorization.
use_when:
  - Deciding the target home of a product artifact under the spine-first tree.
  - Binding the authority a later migration-execution controller consumes.
  - Reconciling the per-lane spine-first migration inventories.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_spine_first_blocker_authorization_v0.md
  - docs/migration/spine_first_target_move_table_v0.md
  - docs/migration/spine_first_untagged_file_inventory_v0.md
  - docs/decisions/orca_repo_structure_binding_v0.md
  - docs/decisions/orca_search_product_lane_binding_v0.md
supersedes: []
stale_if:
  - The owner changes the accepted target tree.
  - A later accepted Orca decision amends a convention, the foregone-limitations
    ledger, or the search-dissolution policy bound here.
  - The migration is executed and repo-structure.yaml + artifact-folders.md are
    amended to the new tree (at which point this becomes the historical target
    record and the amended overlay/map govern current placement).
```

## Status

Owner-adopted target design, v0. The folder tree in **Accepted target tree** is
the owner-adopted **mini-god-tier target structure** (a capability-target design
lens per `docs/decisions/orca_mini_god_tier_doctrine_v0.md`), carried into this
binding by the controller prompt
`docs/prompts/product-planning/orca_spine_first_target_structure_controller_prompt_v0.md`.

This binding is **docs-only planning**. It binds the target design as the single
authority a later migration-execution controller will consume. It does **not**:

- move, rename, or create any product file;
- create the `orca/product/` tree;
- amend `repo-structure.yaml`, `.agents/workflow-overlay/artifact-folders.md`, or
  any current placement rule;
- edit `orca-harness/` or any runtime, test, import, hook, or package metadata;
- claim validation, readiness, proof, migration completion, or runtime support.

Current placement authority remains
`.agents/workflow-overlay/artifact-folders.md` +
`docs/decisions/orca_repo_structure_binding_v0.md` +
`repo-structure.yaml`. Files live where they live today (`docs/product/<lane>/`)
until a separately authorized execution pass applies the move and amends those
surfaces.

Post-merge blocker authorization:
`docs/decisions/orca_spine_first_blocker_authorization_v0.md` settles B1-B7 for
the next execution pass. That record authorizes the execution tranche to create
`orca/`, dissolve `docs/product/search/`, define `docs/doctrine/`, seed CSB from
the gate-run commission criteria doc, keep `source_capture_toolbox` as the
folder name, treat IG/YT/TT as source families, and handle the ontology backlog
JSON only with a paired hook-path update. It does not execute the migration.

Post-execution amendment (2026-06-18): the spine-first migration executed (#255),
so this record is now the historical target. One correction since: the Data Lake
is promoted to its own shared-foundation spine `orca/product/spines/data_lake/` by
`docs/decisions/orca_data_lake_spine_promotion_binding_v0.md`, which **supersedes
the `shared/data_lake_mechanics/` entry** in the Accepted target tree below — the
mechanics map's bound home becomes `data_lake/workflows/` and the lake contracts
are `data_lake/authority/`-owned. Content relocation is a separate later move pass;
`shared/projection_doctrine/` and `shared/engagement_registry/` are untouched by
that promotion.

## Base and provenance

- Read against `origin/main @ 8f19b460` (the controller worktree HEAD equals
  origin/main; tree clean).
- Reconciles two **committed** per-lane inventories —
  `docs/migration/capture_spine_source_capture_migration_inventory_v0.md` (#252)
  and `docs/migration/search_demand_signal_migration_inventory_v0.md` (#247) —
  plus three fresh read-only controller inventory passes (foundation/core-spine,
  judgment, product-lead/ecr/signal-content). The remaining sibling per-lane
  inventories (cleaning, ecr, foundation-layer, product-lead/buyer-proof,
  ontology, global-prompt-review) are **in flight and not on main**; they are
  reconciled here only as evidence, and must be re-reconciled against this
  binding when they land (see Blockers).

## Accepted target tree

This is the GOAL design. Deviations are recorded as Blockers / tagging items
below with `file:line` evidence; the tree itself is not redesigned for tidiness.

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

## Adjudication summary (what source reads confirmed / blocked)

| Convention | Status after source reads | Note |
| --- | --- | --- |
| #1 source-family phase separation | **accepted, verified** | `scanning/source_families/` and `capture/source_families/` are intentionally distinct phases; their member sets differ (LinkedIn is scanning-only; retail_pdp is capture-only). README/cross-pointer required. |
| #2 capture owns `demand_durability_indicators/`; judgment owns `demand_read/grading/` | **accepted, verified** | The four capture indicator profiles stay capture-owned; the search-interest profile relocates into `capture/demand_durability_indicators/search_interest/`; the demand-read grading rubric is judgment-owned. |
| #3 rename `gate_run/` -> `admissibility_checkability/`; gate distribution | **accepted as structure; one clause unverified** | scanning-owns-columns ✓ (`docs/product/search/orca_demand_scan_core_spec_v0.md:614`); product-lead-owns-buyer-facing-Hard-Gate ✓ (`docs/product/product_lead/orca_buyer_proof_packet_v0.md:138`; gate-run criteria defers to it, `docs/product/search/orca_demand_gate_run_commission_criteria_v0.md:35`); judgment-consumes-only ✓. **CSB-owns-commission/work-order = UNKNOWN: no CSB artifact exists today** (Blocker B5). Hard Gate is NOT renamed to an indicator. |
| #4 product-learning three homes | **accepted; one boundary ambiguous** | machinery/contracts -> `judgment/product_learning/`; corpora/runs -> `case_families/product_learning/`; domain frame/skeleton/registry -> `satellites/<domain>/`. The fragrance **reconciliation** artifact straddles machinery vs the `satellites/fragrance/judgment_level1/reconciliation/` slot (tagging item U-J1). |
| #5 moved-path indexes stay in `docs/migration/` | **accepted** | Process/navigation artifacts, not product substance; never under `orca/product/shared/`. |

## Bound conventions

### Convention 1 — Source-family phase separation (not duplication)

`scanning/source_families/<family>/` means **where to look / frontier /
recognition** (discovery-side). `capture/source_families/<family>/` means **how
to acquire admissible evidence** (acquisition-side). The repeated family names
(`reddit`, `instagram`, `youtube`, `tiktok`, `answer_engine`) are intentional
phase separation. The member sets are **not identical**: `linkedin` is a
**scanning** source-family (no-live, planning-only, upstream discovery per the
capture inventory §8) and is **not** under `capture/source_families/`;
`retail_pdp` is a **capture** source-family and is not under scanning. Each
populated `source_families/<family>/` directory **must carry a README that
cross-points to its phase sibling** so the duplication reads as phase separation.

### Convention 2 — Capture owns `demand_durability_indicators/`; "indicator" is not a verdict owner

Capture owns the four durability indicator profiles
(`price_timeseries`, `availability_restock`, `search_interest`,
`review_velocity`). Judgment owns `demand_read/` and `demand_read/grading/` and
must **not** use "indicator" as a verdict owner. The `search_interest` profile
(currently `docs/product/search/`) relocates into
`capture/demand_durability_indicators/search_interest/`; the other three
(currently `docs/product/data_capture_spine/`) relocate to their sibling slots.

### Convention 3 — Scanning area renamed `gate_run/` -> `admissibility_checkability/`; gate distribution

The Demand-Substrate Hard Gate is **not** renamed into an "indicator"; it remains
an admissibility/checkability layer. Verified distribution:

- **Commission Signal Board (CSB)** owns commission / work-order criteria for what
  should be checked. **Caveat:** no CSB artifact exists in the repo today; CSB is
  *structure, not built runtime*. The functional precursor is
  `docs/product/search/orca_demand_gate_run_commission_criteria_v0.md`. Whether
  that doc relocates to `commission_signal_board/` or a fresh CSB artifact is
  authored is a main-CA tagging decision (Blocker B5).
- **Scanning** owns the columns/receipts that make admissibility checkable
  (`scan_core` "makes the gate's columns fillable",
  `docs/product/search/orca_demand_scan_core_spec_v0.md:614`).
- **Product Lead / buyer-proof** owns the buyer-facing Demand-Substrate Hard Gate
  commitments (`docs/product/product_lead/orca_buyer_proof_packet_v0.md:138`; the
  gate-run criteria defers to it on conflict,
  `docs/product/search/orca_demand_gate_run_commission_criteria_v0.md:35`).
- **Judgment** consumes the gate + demand indicators; it does not reopen Capture
  or scan authority.

### Convention 4 — Product-learning three-home boundary

- machinery / contracts -> `judgment/product_learning/`;
- corpora / runs / case docs -> `case_families/product_learning/`;
- domain frame / skeleton / source registry -> `satellites/<domain>/`.

Apply this rule to avoid two-home drift. The fragrance Level-1 organizers split
accordingly: frame/skeleton/screens/registry -> `satellites/fragrance/judgment_level1/`;
the actual cases/runs -> `case_families/product_learning/fragrance/`. The
**reconciliation** artifact is machinery-by-role but fragrance-by-subject and is
left as a tagging item (U-J1).

### Convention 5 — Moved-path indexes stay under `docs/migration/`

Moved-path indexes are process/navigation artifacts, not product substance. They
remain under `docs/migration/`, never under `orca/product/shared/`.

## Source Capture Toolbox shared-capability rule

The Source Capture Toolbox (a.k.a. Source Capture Armory) is adopted **as a named
Capture subsystem and shared capability**, not dissolved into vague "capture
docs" and not a peer microservice. Its home is
`orca/product/spines/capture/source_capture_toolbox/` (canonical-name decision —
"Toolbox" vs "Armory" — is a main-CA tagging item, Blocker B6). Scanning pays one
declared dependency hop to the Toolbox; the dependency is explicit, not a merge.

## Search-dissolution policy

The spine-first target **has no `search/` lane**. The demand-signal intelligence
(search-led) lane bound by
`docs/decisions/orca_search_product_lane_binding_v0.md` (#236/#241)
**dissolves by spine function**:

- the demand-read **taxonomy/grammar** -> `foundation/demand_read_taxonomy/`;
- the **scan method** (`scan_core`) -> `scanning/scan_core/`;
- the **gate** docs -> `scanning/admissibility_checkability/` + (commission
  criteria) `commission_signal_board/` + (buyer-facing Hard Gate) `product_lead/`
  per Convention 3;
- the **answer-engine surface** (AEO probe) -> `scanning/source_families/answer_engine/`;
- the **search-interest** durability profile ->
  `capture/demand_durability_indicators/search_interest/`.

This **reverses the search-lane binding's physical placement** (topic-primacy ->
spine-function placement). It does **not** narrow the demand-signal method's
**venue-spanning authority**: the taxonomy and gate grammar remain consumed
across the judgment, capture, and core spines after relocation. Because the
search-lane binding is owner-adopted Orca doctrine landed only days earlier, the
**physical reversal is surfaced as a high-salience supersession** requiring owner
confirmation at execution (Blocker B2). See the dedicated dissolution rows in
`docs/migration/spine_first_target_move_table_v0.md`.

## Foregone-limitations ledger (owner-accepted)

- Runtime stays in `orca-harness/`; code migration is deferred to a global
  runtime-mapping decision. The spine names under `orca/product/spines/` mirror
  but do not relocate harness subtrees.
- Source Capture Toolbox is a Capture subsystem and shared capability, not a peer
  microservice. Scanning pays one declared dependency hop.
- Live docs get rewritten during execution; historical records resolve through
  moved-path indexes; input-hash pin residual is tolerated unless a specific later
  pass re-pins.
- CSB and Scanning are homes/structure, not proof of built runtime.
- SCR (Signal Content Record) is under ECR (`ecr/signal_content/`) unless future
  evidence proves it needs peer-spine status.
- IG/YT/TT are source families under scanning and capture, not peer spines.
- The tree is deliberately deeper for per-concept legibility.

## Supersession / amendment targets (at execution, not now)

When a separately authorized execution pass runs, it must amend:

- **`repo-structure.yaml`** — add `orca` to `known_top_level.dirs` (Blocker B1)
  and add the `orca/product/` second-level axis (spines / satellites /
  case_families / shared); update `docs_roles` for the new `docs/doctrine/` role
  and the dropped `docs/product/` role.
- **`.agents/workflow-overlay/artifact-folders.md`** — replace the `docs/product/`
  lane-axis bullet with the `orca/product/` spine axis; add `docs/doctrine/`.
- **`docs/decisions/orca_repo_structure_binding_v0.md`** — the `docs/product/`
  by-lane parameter is superseded by the `orca/product/` spine axis bound here.
- **`docs/decisions/orca_search_product_lane_binding_v0.md`** — its `search/`
  physical home and topic-primacy precedence are superseded by the
  search-dissolution policy above (authority of the method docs preserved).
- **`docs/workflows/orca_repo_map_v0.md`**, the consolidation maps, and the ECR /
  Judgment / Data-Capture submaps — extensive `docs/product/...` -> `orca/product/...`
  reference rewrites.

None of these are touched by this binding; they are the execution checklist.

## Blockers (load-bearing; do not bury)

Post-merge status: B1-B7 are settled for execution by
`docs/decisions/orca_spine_first_blocker_authorization_v0.md`. The historical
blocker text below is retained to show what was blocked at target-binding time;
execution controllers should apply the authorization record before stopping on
these items.

- **B1 — `orca/` root not authorized.** `repo-structure.yaml`
  `known_top_level.dirs` is `[.agents, .claude, .codex, .git, docs, orca-harness]`
  (`repo-structure.yaml:23-30`); `orca` is absent and does not exist on
  `origin/main`. Creating `orca/product/` is a root-layout change and EP-04
  `check_placement.py` would flag it unplaced. Execution is blocked until the
  machine map authorizes the `orca/` root.
- **B2 — search-lane physical reversal.** The search-dissolution policy reverses
  `orca_search_product_lane_binding_v0.md` placement days after it landed; needs
  explicit owner confirmation before execution.
- **B3 — `docs/doctrine/` boundary undefined.** The target adds `docs/doctrine/`
  while keeping `docs/decisions/` (and the doctrine **index** already lives at
  `docs/decisions/orca_doctrine_index_v0.md`). No loaded source defines what moves
  to `doctrine/` vs stays in `decisions/`. Needs main-CA tagging.
- **B4 — ontology backlog hook coupling.** `.agents/hooks/check_ontology_expansion.py`
  reads `docs/product/core_spine/ontology_expansion_backlog_v0.json`; moving it to
  `foundation/ontology/` breaks the hook path. The move requires a paired hook
  reference rewrite (runtime-adjacent; not a docs-only edit).
- **B5 — CSB has no doc home.** Convention 3's CSB clause is unverified; first CSB
  artifact may need authoring, or the gate-run commission criteria doc relocates.
- **B6 — Toolbox vs Armory canonical name** + **IG-lane status** (no IG binding
  exists; 13 `ig_*` docs + creator specs held under Capture/Toolbox today) — both
  carried from the capture inventory (§6, §11–12) as owner decisions.
- **B7 — sibling inventories not on main.** Cleaning, ECR, foundation, ontology,
  product-lead/buyer-proof, and global-prompt-review per-lane inventories are
  in-flight; this binding reconciles only the two committed ones. Re-reconcile on
  landing.

## Non-claims

- Not validation, readiness, approval, proof, or product proof.
- Not a runtime-migration authorization; no file is moved or created; `orca/`
  is not created; `orca-harness/` is untouched.
- Not an amendment to `repo-structure.yaml`, `artifact-folders.md`, the
  repo-structure binding, or the search-lane binding — those are the execution
  checklist, deferred.
- Not ratification of the in-flight sibling inventories as merged truth.
- A green `check_placement.py` run after any future execution is placement shape,
  not authority.

## Direction change propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca adopts the spine-first target structure (rooted at orca/product/, with
    spines/satellites/case_families/shared and a docs/ doctrine/ role) as the
    single TARGET-structure authority a later migration-execution controller
    binds to, with five adjudicated conventions, the Source Capture Toolbox
    shared-capability rule, the source-family phase convention, the
    product-learning three-home rule, the search-dissolution policy, and the
    foregone-limitations ledger. Target design only: no file move, no orca/
    creation, no repo-structure.yaml / artifact-folders amendment, no runtime
    migration; current placement authority (artifact-folders + repo-structure
    binding + repo-structure.yaml) is unchanged until a separate authorized
    execution pass applies the supersessions listed here.
  trigger: architecture_doctrine
  related_triggers:
    - output_authority
    - workflow_authority
  controlling_sources_updated:
    - docs/decisions/orca_spine_first_target_structure_binding_v0.md
  downstream_surfaces_checked:
    - docs/decisions/orca_repo_structure_binding_v0.md
    - docs/decisions/orca_search_product_lane_binding_v0.md
    - repo-structure.yaml
    - .agents/workflow-overlay/artifact-folders.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/decisions/orca_doctrine_index_v0.md
  intentionally_not_updated:
    - path: repo-structure.yaml
      reason: >
        Adding orca/ to known_top_level and the orca/product/ axis is an
        EXECUTION-time amendment (Blocker B1). This binding defers execution and
        records the amendment as the supersession checklist, so the machine map
        is intentionally left at its current (docs/product by-lane) state.
    - path: .agents/workflow-overlay/artifact-folders.md
      reason: >
        The docs/product by-lane bullet stays current placement authority until
        execution. Amending it now would fork placement authority from the
        un-applied tree.
    - path: docs/decisions/orca_repo_structure_binding_v0.md
      reason: >
        Its docs/product by-lane parameter remains the live rule until execution;
        superseded only when the move applies.
    - path: docs/decisions/orca_search_product_lane_binding_v0.md
      reason: >
        Its search/ home governs current placement; the dissolution supersedes it
        only at execution and preserves the method docs' venue-spanning authority
        (Blocker B2 surfaces it for owner confirmation).
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Reference rewrites (docs/product -> orca/product) are an execution-time
        bulk edit; the map still routes current homes today.
    - path: docs/decisions/orca_doctrine_index_v0.md
      reason: >
        The docs/doctrine/ vs docs/decisions/ boundary is undefined (Blocker B3);
        no index change is made until that boundary is tagged.
  stale_language_search: >
    rg -i "spine-first|spine_first|orca/product/spines|mini.god.tier target" over *.md
    (run 2026-06-18 in worktree youthful-jones-ae658e @ 8f19b460)
  stale_language_search_result: >
    Three hits only: the two committed migration inventories being reconciled
    (capture #252, search #247) and one adversarial-review output with incidental
    phrasing. No pre-existing spine-first / orca/product target-structure doctrine
    exists, so this binding is additive and forks nothing.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not implementation or runtime-migration authorization
    - not creation of the orca/ tree
```
