# Scanning Spine README

```yaml
retrieval_header_version: 1
artifact_role: Scanning spine front-door index
scope: >
  Retrieval-only entry point for the scanning spine: load order, file classes,
  shared vocabulary, precursor-signal placement, and bloat-control boundaries.
use_when:
  - Starting any scanning-lane task cold.
  - Deciding which scanning source to open before source-family or capture work.
  - Checking whether a scanning artifact should use shared intelligent-walk vocabulary.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
  - orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
  - orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md
stale_if:
  - The MGT intelligent-walk operating model changes its shared vocabulary or hard boundaries.
  - The Demand Scan-Core Spec is owner-adjudicated or superseded.
  - A source-family adapter becomes the canonical entry point for the whole scanning spine.
```

## Load Order

1. Open the MGT intelligent-walk operating model first for shared scanning
   vocabulary, branch-aware walking, precursor handling, and capture-request
   boundaries.
2. Open the Demand Scan-Core Spec only when the work needs rich promoted
   observation schema, gate preparation, or backward/forward scan-mode detail.
3. Open source-family adapters only for local restrictions: Reddit, LinkedIn,
   answer-engine/search, or future families.
4. Open Capture sources only when a `capture_request` or source-access wall is
   present. Scanning cites route state; Capture owns route binding.

## File Classes

| Class | Files | Use |
| --- | --- | --- |
| Core method front door | `scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md` | Bounded intelligent walk, precursor vocabulary, minimum evidence, capture-request bridge. |
| Proposed rich schema | `scan_core/orca_demand_scan_core_spec_v0.md` | Candidate-observation schema and gate-prep detail after signal promotion. |
| Adjudication / support | `admissibility_checkability/*.md` | Gate-definition and scan-core decision surfaces. |
| Source-family adapters | `source_families/*/*.md` | Local guardrails mapped into shared scanning vocabulary. |
| Research / probe evidence | `docs/research/answer_engine/aeo_capture_feasibility_probe_phase0_v0.md` | AEO feasibility evidence; not product-spine authority. |

## Shared Output Vocabulary

Scanning emits screen-light `frontier`, `move`, `precursor_signal`,
`precursor_surface`, `observation`, `candidate`, `pointer`, `negative`,
`access_note`, `influence_obs`, and `capture_request` records.

`precursor_signal` and `precursor_surface` are routing inputs. They may steer a
walk, explain a pivot, support an observation, or justify a capture request.
They do not prove demand, clear a gate, authorize capture, or create a standing
source map.

## Boundary

The scanning spine is not a crawler, monitor, registry, atlas, capture runner,
ECR lane, Cleaning lane, Judgment lane, outreach lane, or buyer-contact system.
When a source-family doc repeats that boundary, prefer pointing back here and to
the MGT hard boundaries while preserving source-specific hard stops.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The scanning spine now has a retrieval-only front door that routes source
    loading through the MGT intelligent-walk operating model first, makes
    precursor_signal and precursor_surface first-class screen-light scanning
    vocabulary, and rehomes the AEO Phase-0 probe artifacts to research rather
    than product-spine authority.
  trigger: product_doctrine
  related_triggers:
    - workflow_authority
    - output_authority
  controlling_sources_updated:
    - orca/product/spines/scanning/README.md
    - orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
    - orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
    - orca/product/spines/scanning/source_families/reddit/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
    - orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_lane_index_v0.md
    - orca/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md
    - orca/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md
    - docs/research/answer_engine/aeo_capture_feasibility_probe_phase0_v0.md
    - docs/research/answer_engine/aeo_capture_feasibility_probe_phase0_v0_evidence.json
    - docs/migration/repo_structure_spine_first_v0/moved_paths_index.md
    - docs/migration/repo_structure_spine_first_v0/moves_manifest.csv
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/validation-gates.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        No scanning-specific read pack exists there today; repo-map routing plus
        this front-door README supplies the new one-hop source-loading path.
    - path: source-family filenames carrying data_capture_spine
      reason: >
        Broad path renames are deferred; this pass clarifies artifact headers and
        vocabulary without invalidating legacy references.
  stale_language_search: >
    rg -n "precursor_signal|precursor_surface|capture-needs list|crawler|monitor|registry|atlas|route binding"
    orca/product/spines/scanning docs/workflows/orca_repo_map_v0.md
    docs/migration/repo_structure_spine_first_v0
    plus targeted AEO path check:
    rg -n "orca/product/spines/scanning/source_families/answer_engine/aeo_capture_feasibility_probe_phase0|docs/product/search/aeo_capture_feasibility_probe_phase0|docs/research/answer_engine/aeo_capture_feasibility_probe_phase0"
    . --glob "!docs/review-inputs/**"
  stale_language_search_result: >
    CA-adjudication recheck 2026-06-21: precursor/gate/capture hits are
    explicit "not proof" safeguards or the intentional capture_request alias;
    current live AEO routing points to docs/research/answer_engine; old
    docs/product/search AEO paths remain only in migration resolver/history
    rows; the old product-spine AEO path appears only as search/audit text
    or review snapshots, not as a live route. No stale live product-spine AEO route found.
  non_claims:
    - not validation
    - not readiness
    - not scan authorization
    - not capture authorization
    - not source-access authorization
    - not implementation authorization
```
