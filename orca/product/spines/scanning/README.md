# Scanning Spine README

```yaml
retrieval_header_version: 1
artifact_role: Scanning spine front-door index
scope: >
  Retrieval-only entry point for the scanning spine: load order, file classes,
  shared vocabulary, CSB-first venue evaluation, default bounded broad-scout
  phase, recency/current-state priority, exact-query discovery,
  precursor-signal placement, and bloat-control boundaries.
use_when:
  - Starting any scanning-lane task cold.
  - Starting or reviewing a CSB-first scan.
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

1. Start from a Commission Signal Board output when one exists. If no CSB
   board exists and the task is not an owner-authorized seed-first probe,
   commission CSB first; scanning should not silently invent the board shape.
   Every CSB-first scan then runs a bounded broad-scout phase by default before
   or alongside main deepening.
2. Open the MGT intelligent-walk operating model for shared scanning
   vocabulary, branch-aware walking, default broad-scout rules, recency-first
   frontier ordering, venue-value evaluation, exact-query discovery,
   hidden-venue discovery, precursor handling, and capture-request boundaries.
3. Open the Demand Scan-Core Spec only when the work needs rich promoted
   observation schema, gate preparation, or backward/forward scan-mode detail.
4. Open source-family adapters only for local restrictions: Reddit, LinkedIn,
   answer-engine/search, or future families.
5. Open Capture sources only when a `capture_request` or source-access wall is
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

Scanning emits screen-light `frontier`, `move`, `exact_query`,
`broad_scout_return`, `precursor_signal`, `precursor_surface`, `observation`,
`candidate`, `pointer`, `negative`, `access_note`, `influence_obs`,
`venue_eval`, `hidden_venue_pointer`, and `capture_request` records.

CSB supplies the starting source-family and signal-route board. Scanning then
tests which venues are actually valuable for the commissioned decision and
whether any high-yield venue or surface was hidden from the board.

For every CSB-first scan, the broad-scout phase is mandatory by default and
bounded by the commission's caps. It may run as one route-ledger subagent when
subagents are available, or inline when they are not. Its job is to miss-check
the board: public buyer-language venues, hidden venues, exact-query risks,
decisive negatives, access walls, and obvious recency/current-state changes.
It does not mint candidates, clear gates, bind Capture routes, or authorize
source expansion. Main scanning owns deepening and final candidate decisions.

After CSB routes and hard stops, scanning prioritizes recent and current-state
sources first when expected decision value is otherwise comparable: current
official or retailer state, dated buyer language, recent reviews or threads,
recent stockout/restock/availability changes, and recent editorial, partner, or
org-motion pointers. Older sources remain useful for provenance, chronology, or
baseline contradiction, but they should be labeled as historical/contextual and
must not override fresh current-state reads.

Exact-query discovery belongs to scanning. It is a bounded public-query walk
used to test CSB rows, find hidden venues, and record pointers, negatives, or
access notes. It is not search-volume proof, AEO proof, SEO keyword research,
a standing query monitor, or a crawler substitute.

`precursor_signal` and `precursor_surface` are routing inputs. They may steer a
walk or explain why a venue deserves inspection. They are not a generic label
for every weak clue. They do not prove demand, clear a gate, authorize capture,
or create a standing source map.

## Boundary

The scanning spine is not a crawler, monitor, registry, atlas, capture runner,
ECR lane, Cleaning lane, Judgment lane, outreach lane, or buyer-contact system.
The default broad-scout phase is a bounded scan step, not a standing crawl or a
runtime mandate that every environment must provide subagents.
When a source-family doc repeats that boundary, prefer pointing back here and to
the MGT hard boundaries while preserving source-specific hard stops.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    CSB-first scans now run a bounded broad-scout phase by default, and scanning
    prioritizes recent/current-state frontiers before older context when
    expected decision value is otherwise comparable. Broad scout may use a
    route-ledger subagent when available, but the default is the bounded phase,
    not a hard runtime dependency on subagent infrastructure.
  trigger: product_doctrine
  related_triggers:
    - workflow_authority
    - output_authority
  controlling_sources_updated:
    - orca/product/spines/scanning/README.md
    - orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
  intentionally_not_updated:
    - path: orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
      reason: >
        The proposed scan-core schema already owns promoted-observation freshness
        and stale_after behavior. This change governs pre-promotion frontier
        ordering and CSB-first scan operating shape in the MGT/front-door layer.
    - path: source-family adapter files
      reason: >
        Source-family local hard stops are unchanged; they inherit the shared
        broad-scout and recency ordering by opening this README and the MGT
        operating model.
  stale_language_search: >
    rg -n "broad scout|broad-scout|subagent|recent|recency|freshness|crawler|monitor|registry|atlas|capture route|gate proof"
    orca/product/spines/scanning docs/workflows/orca_repo_map_v0.md
    (run 2026-06-23)
  stale_language_search_result: >
    Executed 2026-06-23 after edit. Hits are this accepted broad-scout/recency
    default, existing scan-core freshness/monitor safeguards, repo-map registry
    route entries, or explicit no-crawler/no-monitor/no-capture-route/no-gate-proof
    boundaries. No capless crawl, standing monitor, gate-proof leakage,
    Capture route binding, or mandatory subagent-runtime claim was found.
  non_claims:
    - not validation
    - not readiness
    - not scan authorization
    - not capture authorization
    - not source-access authorization
    - not implementation authorization
```
```yaml
direction_change_propagation:
  doctrine_changed: >
    The scanning spine now has a retrieval-only front door that routes source
    loading through CSB when a board exists, then the MGT intelligent-walk
    operating model. Scanning's primary role is venue-value evaluation,
    exact-query discovery, and hidden-venue discovery; precursor_signal and
    precursor_surface are reserved
    for venue/surface routing rather than generic weak evidence labels. The AEO
    Phase-0 probe artifacts live in research rather than product-spine
    authority.
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
