# Forseti Spine-First Blocker Authorization v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: >
  Owner authorization and main-CA settlement for the blockers surfaced by the
  spine-first target-structure controller. Authorizes the next migration
  execution pass to amend placement surfaces and resolve B1-B7 under the
  accepted mini-god-tier target without re-opening the target tree.
use_when:
  - Preparing the spine-first migration execution pass.
  - Deciding whether B1-B7 in the target binding or untagged inventory remain blocking.
  - Checking the owner decisions for search dissolution, CSB placement, IG/source-family status, and docs/doctrine boundaries.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_spine_first_target_structure_binding_v0.md
  - docs/migration/spine_first_target_move_table_v0.md
  - docs/migration/spine_first_untagged_file_inventory_v0.md
  - docs/decisions/forseti_repo_structure_binding_v0.md
  - docs/decisions/orca_search_product_lane_binding_v0.md
stale_if:
  - The owner changes the accepted target tree.
  - The spine-first migration executes and the current placement surfaces are amended.
  - A later blocker authorization supersedes one of the settlements below.
```

## Status

Owner-authorized blocker settlement, v0. This record responds to the post-merge
question "what do for the blockers? I merged. authorize of course for any
needed" after PR #253 landed the spine-first target-structure binding and move
table.

This record authorizes the next execution controller to resolve the blockers in
one controlled migration tranche. It does **not** execute the migration, move
files, create `orca/product/`, edit `orca-harness/`, validate the product tree,
or claim readiness.

## Settlement Summary

| ID | Settlement | Execution instruction |
| --- | --- | --- |
| B1 `orca/` root | **Authorized.** The `orca/` top-level root and `orca/product/` product-substance tree are approved for the spine-first migration. | During execution, amend `repo-structure.yaml`, `.agents/workflow-overlay/artifact-folders.md`, and `docs/decisions/forseti_repo_structure_binding_v0.md` in the same tranche that creates or populates `orca/product/`. Do not add `orca` to the map without creating the tree, because the placement checker treats missing declared roots as stale. |
| B2 search-lane reversal | **Confirmed.** Spine-first placement supersedes the physical `docs/product/search/` lane for future product-substance homes. | Dissolve `docs/product/search/` according to the move table. Preserve the authority and provenance of the demand-signal method docs; only their physical home changes. The search-lane binding becomes historical/superseded for placement after execution. |
| B3 `docs/doctrine/` boundary | **Defined.** `docs/doctrine/` is an index/router home, not a decision-record home. | Keep ratified decisions and adoption records in `docs/decisions/`. Put doctrine indexes, routers, and non-controlling doctrine-like inventories in `docs/doctrine/`. Do not move decision records into `docs/doctrine/` just because they are doctrine-bearing. |
| B4 ontology backlog hook coupling | **Authorized as paired execution.** The ontology backlog JSON may move only with its hook/path update. | Do not move `ontology_expansion_backlog_v0.json` alone. In the migration tranche, either update `.agents/hooks/check_ontology_expansion.py` to the new path or make it bridge old/new paths for the transition, then run the hook's relevant check. |
| B5 CSB first home | **Settled.** The existing gate-run commission criteria doc seeds CSB under dispatch rules. | Move `orca_demand_gate_run_commission_criteria_v0.md` to `orca/product/spines/commission_signal_board/dispatch_rules/`. New CSB home directories may exist empty or with READMEs, but no runtime/build claim is made. |
| B6 Toolbox vs Armory + IG status | **Settled.** Folder name is `source_capture_toolbox`; display name may remain Source Capture Armory. IG/YT/TT are source families, not peer spines. | Keep target folder `capture/source_capture_toolbox/`. Move current IG docs into `capture/source_families/instagram/` unless a later explicit IG lane binding supersedes this. YouTube and TikTok may be empty source-family slots until docs exist. |
| B7 sibling inventories | **Advisory, not a stop.** Missing sibling inventories do not block the authorized migration by themselves. | Before execution, re-reconcile any sibling inventories that have landed on main. If they conflict with the binding or this authorization, surface the exact conflict; otherwise proceed from the bound move table. |

## Tagging Defaults For Per-File Ambiguities

Use these defaults to reduce future main-CA pauses. They are placement
instructions for the migration controller, not validation or product-quality
claims.

- Proof-method and proof-gate definitions belong in
  `orca/product/spines/foundation/product_contract/` unless the artifact is an
  executed run, packet, or corpus instance.
- Executed or prepared case/run corpora belong in
  `orca/product/case_families/product_learning/`, with `other_verticals/` as the
  accepted catch-all for non-fragrance and non-retail-PDP cases.
- Domain-specific frames, source registries, and Level 1 skeletons belong in
  `orca/product/satellites/<domain>/`.
- Judgment-wide orientation maps may live at the relevant Judgment spine root or
  `judgment/conductor/` only when they route the run sequence. Do not create an
  archive folder during this migration merely to house superseded Judgment docs.
- Product-lead discovery instruments and runbooks default to
  `product_lead/icp_wedge/` unless a later product-lead sub-slot decision adds
  `discovery/` or `process/`.
- Historical/superseded product-lead artifacts migrate with their owning subject
  unless a later archive decision creates product archive folders.
- Capture pressure-test operational evidence defaults to
  `capture/operating_model/` unless the case-family inventory proves a durable
  corpus role.

## Non-Claims

- Not migration execution.
- Not validation, readiness, proof, product proof, or judgment-quality evidence.
- Not a runtime migration.
- Not authorization to edit `orca-harness/`.
- Not authorization to run source capture, public web collection, or external
  network probes.
- Not a claim that the target folders currently exist.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Owner-authorized settlement of the spine-first target-structure blockers:
    `orca/` root creation and `orca/product/` axis are authorized for the
    execution tranche; search-lane physical placement is superseded by
    spine-first dissolution; `docs/doctrine/` is index/router-only; CSB's first
    seeded doc home is dispatch_rules; `source_capture_toolbox` is the canonical
    folder name; IG/YT/TT are source families rather than peer spines; sibling
    inventories are advisory unless landed conflicts appear.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/forseti_spine_first_blocker_authorization_v0.md
    - docs/decisions/forseti_spine_first_target_structure_binding_v0.md
    - docs/migration/spine_first_target_move_table_v0.md
    - docs/migration/spine_first_untagged_file_inventory_v0.md
    - docs/decisions/forseti_repo_structure_binding_v0.md
    - docs/decisions/orca_search_product_lane_binding_v0.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - docs/decisions/forseti_spine_first_target_structure_binding_v0.md
    - docs/migration/spine_first_target_move_table_v0.md
    - docs/migration/spine_first_untagged_file_inventory_v0.md
    - docs/decisions/forseti_repo_structure_binding_v0.md
    - docs/decisions/orca_search_product_lane_binding_v0.md
    - .agents/workflow-overlay/artifact-folders.md
    - repo-structure.yaml
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: repo-structure.yaml
      reason: >
        Updating the map before creating `orca/` would make the map stale under
        check_placement.py freshness rules. The map amendment belongs in the
        migration execution tranche that creates/populates the tree.
    - path: .agents/workflow-overlay/artifact-folders.md
      reason: >
        Current placement authority still reflects the live tree until execution.
        This record authorizes the later amendment; it does not pre-apply it.
  stale_language_search: >
    rg -n "B1|B2|B3|B4|B5|B6|B7|orca/product|docs/doctrine|source_capture_toolbox|search-lane"
    docs/decisions docs/migration .agents/workflow-overlay repo-structure.yaml
  stale_language_search_result: >
    Executed 2026-06-18 in the blocker-authorization worktree. Hits were the
    expected current/live placement surfaces (`repo-structure.yaml`,
    artifact-folders.md, repo-structure binding, search-lane binding),
    migration inventories, target binding, and this authorization, plus
    historical source-capture/search migration records. No checked surface
    contradicted the settlement: current placement language remains true until
    execution; the authorization record governs the next migration tranche.
  non_claims:
    - not validation
    - not readiness
    - not migration execution
    - not creation of the orca/ tree
```

Older direction-change propagation receipts live in
`docs/decisions/dcp_receipts_archive_v0.md`.
