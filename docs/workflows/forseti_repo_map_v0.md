# Forseti Repo Map v0

```yaml
retrieval_header_version: 1
artifact_role: Repository map
scope: Compact navigation map for Forseti cold starts, source loading, and identity-convergence routing.
use_when:
  - Orienting a new Forseti thread without bulk-loading the repository.
  - Choosing the first source pack for product, prompt, review, research, or workflow work.
  - Checking which Orca-named roots are legacy compatibility paths.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/source-of-truth.md
  - forseti/product/README.md
supersedes:
  - docs/workflows/orca_repo_map_v0.md as the cold-start route card
stale_if:
  - The physical product corpus under orca/product/ is migrated into forseti/product/.
  - The legacy runtime harness under orca-harness/ is migrated or replaced by forseti-harness/.
  - A later accepted repo map supersedes this file.
```

- Status: ACTIVE_RETRIEVAL_MAP (retrieval-only; source authority remains in `.agents/workflow-overlay/source-of-truth.md`)
- Artifact type: Workflow navigation artifact
- Scope: Forseti navigation and source-pack selection
- Refreshed: 2026-07-09 (harness packaging smoke plus high-traffic front doors for Creator Signal, Foundation ontology, Judgment, Capture, and Answer Engine). Prior: 2026-07-09 (Forseti identity convergence front door; legacy Orca physical roots made explicit)
- Implementation authorized: no

## How To Use This Map

Start with this map, not `docs/workflows/orca_repo_map_v0.md`, for new Forseti
work. Use the legacy Orca map only when a needed owner or detailed route still
physically lives under an Orca-named compatibility root.

Do not treat this map as product authority, validation, readiness, proof, or
migration completion evidence. For precedence, open
`.agents/workflow-overlay/source-of-truth.md`. For source-loading budgets, open
`.agents/workflow-overlay/source-loading.md`.

## Canonical Front Doors

| Path | Use for |
| --- | --- |
| `README.md` | Workspace identity and first orientation. |
| `AGENTS.md` | Agent behavior kernel, isolation rule, verification discipline, and Forseti project triggers. |
| `.agents/workflow-overlay/README.md` | Project authority overlay. Some files retain legacy Orca labels during migration. |
| `repo-structure.yaml` | Machine-readable router; points cold starts to this map and `forseti/product/README.md`. |
| `forseti/product/README.md` | Canonical Forseti product front door. |
| `docs/research/README.md` | Research front door; routes answer-engine/AEO, Aphrodite, Judgment Spine research, and other research lanes. |

## Product And Harness Roots

| Path | Current routing status |
| --- | --- |
| `forseti/product/` | Canonical Forseti product root for new entrypoints and newly accepted product artifacts when no existing legacy owner must be updated in place. |
| `forseti/product/spines/creator_signal/` | Live Aphrodite / Creator Signal product records restored for the D-1 bundle. |
| `forseti/product/spines/foundation/ontology/` | Live Forseti ontology reference data for Aphrodite D-1. |
| `orca/product/` | Legacy compatibility product corpus. Most pre-Forseti product files still physically live here; update existing owners in place until a separate migration moves them. |
| `orca-harness/` | Legacy compatibility runtime harness root. Use it for live harness files until a separate migration creates or populates `forseti-harness/`. |
| `forseti-harness/` | Not present in this workspace as of this map. Do not cite it as a live path. |

## High-Traffic Front Doors

| Path | Start here for |
| --- | --- |
| `forseti/product/spines/creator_signal/README.md` | Creator Signal and Aphrodite product-record routing. |
| `forseti/product/spines/foundation/ontology/README.md` | Fragrance reference, foundation ontology, and legacy foundation-owner routing. |
| `orca/product/spines/judgment/README.md` | Legacy Judgment spine product owners and judgment-quality routing. |
| `orca/product/spines/capture/README.md` | Legacy Capture spine, Source Capture Armory, and harness-adjacent routing. |
| `docs/research/answer_engine/README.md` | Answer-engine / AEO research and scanning-source-family bridge. |

## Aphrodite D-1 Bundle Route

Open these live paths for the D-1 bundle:

| Path | Role |
| --- | --- |
| `docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md` | Operative recipe v1 and closeout checklist. |
| `docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md` | Adjudicated second-opinion rulings consumed by recipe v1. |
| `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md` | D-1 corpus freeze and input hash basis. |
| `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json` | D-1 claims JSON. |
| `forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md` | Derived-claim provenance contract. |
| `forseti/product/spines/creator_signal/aphrodite_vetting_sprint_panel_design_v0.md` | Five-panel sprint display design. |
| `forseti/product/spines/foundation/ontology/fragrance_reference_v0.yaml` | Fragrance reference data used by the recipe and panels. |

## Legacy Detailed Map

`docs/workflows/orca_repo_map_v0.md` remains a detailed compatibility map for
pre-Forseti physical roots and historical route detail. It is not the cold-start
route card. When this map is too compact for an owner that still lives under
`orca/product/` or `orca-harness/`, open the legacy map as a second-hop detail
source and verify every referenced live path before claiming it resolves.

## Not-Proven Boundaries

This map does not prove validation, readiness, buyer proof, implementation
authorization, source correctness, product authority, runtime authority, or that
the legacy physical-root migration is complete.

## Direction Change Propagation - Forseti Identity Convergence

```yaml
direction_change_propagation:
  doctrine_changed: >
    Forseti becomes the canonical project identity and cold-start route. The
    repo route card is now docs/workflows/forseti_repo_map_v0.md and the product
    front door is forseti/product/README.md. Orca-named physical roots remain
    explicit legacy compatibility roots only: orca/product/ for existing product
    owners and orca-harness/ for live harness files until a separate migration
    moves or replaces them. This change does not mass-move product or harness
    files and does not create a fake forseti-harness/ path.
  trigger: workflow_authority
  related_triggers:
    - architecture_doctrine
    - lifecycle_boundary
  controlling_sources_updated:
    - README.md
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/project-authority.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/artifact-folders.md
    - repo-structure.yaml
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - forseti/product/README.md
    - docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md
    - docs/research/aphrodite_recipe_v1_second_opinion_adjudication_v0.md
    - docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json
  downstream_surfaces_checked:
    - docs/research/aphrodite_depth_rehearsal_d1_gentsscents_corpus_v0.md
  intentionally_not_updated:
    - path: orca/product/
      reason: Most pre-Forseti product owners still physically live there; mass move is a separate migration.
    - path: orca-harness/
      reason: Live harness implementation still physically lives there; no forseti-harness/ exists to point at honestly.

  stale_language_search: >
    rg -n "Orca|orca/product|orca-harness|orca_repo_map|Forseti|forseti/product|forseti-harness|forseti_repo_map" README.md AGENTS.md repo-structure.yaml docs/workflows/forseti_repo_map_v0.md docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not build or runtime authorization
    - not physical-root migration completion
```

## Direction Change Propagation - Efficiency Front Doors

```yaml
direction_change_propagation:
  doctrine_changed: >
    Forseti adds retrieval-only high-traffic front doors for Creator Signal,
    Foundation ontology, Judgment, Capture, and Answer Engine research so cold
    agents can route one hop before opening the legacy detailed map. Orca-named
    physical roots remain legacy compatibility roots; this change does not move
    product or harness files. The harness package guard checks live top-level
    package discovery and keeps the report-data tree excluded from package
    discovery.
  trigger: workflow_authority
  related_triggers:
    - source_loading
  controlling_sources_updated:
    - docs/workflows/forseti_repo_map_v0.md
    - forseti/product/README.md
    - forseti/product/spines/creator_signal/README.md
    - forseti/product/spines/foundation/ontology/README.md
    - orca/product/spines/judgment/README.md
    - orca/product/spines/capture/README.md
    - docs/research/README.md
    - docs/research/answer_engine/README.md
  intentionally_not_updated:
    - path: orca/product/
      reason: Legacy physical product corpus remains in place until a separate migration moves it.
    - path: orca-harness/
      reason: Harness root remains the live legacy runtime path; the package-guard change only fixes package discovery.
    - path: docs/prompts/** and docs/review-outputs/**
      reason: Historical prompt/review cleanup is intentionally deferred to a later retention/deletion gate.
  non_claims:
    - not validation
    - not readiness
    - not source promotion
    - not physical-root migration completion
    - not prompt or review retention cleanup
```