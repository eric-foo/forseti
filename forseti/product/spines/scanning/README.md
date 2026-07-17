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
  - forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md
  - forseti/product/spines/scanning/scan_core/forseti_demand_scan_core_spec_v0.md
  - forseti/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md
  - forseti/product/spines/foundation/vertical_exploration/forseti_vertical_exploration_guide_v0.md
stale_if:
  - The MGT intelligent-walk operating model changes its shared vocabulary or hard boundaries.
  - The Demand Scan-Core Spec is owner-adjudicated or superseded.
  - A source-family adapter becomes the canonical entry point for the whole scanning spine.
```

## Load Order

1. Start from a Commission Signal Board output when one exists. If no CSB
   board exists and the task is not an owner-authorized seed-first probe,
   commission CSB first; scanning should not silently invent the board shape.
   For a recurring or actively radarred source family, inspect the existing
   Data Lake before external scanning: relevant Silver/current view first, then
   packet or catalog inventory, then raw material when necessary. This is a
   reuse, freshness, and coverage preflight, not proof of current external
   reality. Absence from Silver is not absence from the lake or the world, and
   lack of a relevant read model does not block acquisition.
   Every CSB-first scan then runs a bounded broad-scout phase by default before
   or alongside main deepening.
2. Open the MGT intelligent-walk operating model for shared scanning
   vocabulary, branch-aware walking, default broad-scout rules, recency-first
   frontier ordering, venue-value evaluation, exact-query discovery,
   hidden-venue discovery, precursor handling, and capture-request boundaries.
3. Open the Demand Scan-Core Spec only when the work needs rich promoted
   observation schema, gate preparation, or backward/forward scan-mode detail.
4. Open source-family adapters only for local restrictions: Reddit, LinkedIn,
   answer-engine/search, or future families. For answer-engine/search-interest or
   AEO work, continue from this README to
   `source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md`,
   then to research evidence under `docs/research/answer_engine/`.
5. Open Capture sources only when a `capture_request` or source-access wall is
   present. Scanning cites route state; Capture owns route binding.

## File Classes

| Class | Files | Use |
| --- | --- | --- |
| Core method front door | `scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md` | Bounded intelligent walk, precursor vocabulary, minimum evidence, capture-request bridge. |
| Proposed rich schema | `scan_core/forseti_demand_scan_core_spec_v0.md` | Candidate-observation schema and gate-prep detail after signal promotion. |
| Adjudication / support | `admissibility_checkability/*.md` | Gate-definition and scan-core decision surfaces. |
| Source-family adapters | `source_families/*/*.md` | Local guardrails mapped into shared scanning vocabulary; a family folder may also hold an advisory venue-routing inventory (e.g. the Reddit beauty/fragrance subreddit inventory), which is planning input, not adapter authority. |
| Research / probe evidence | `docs/research/answer_engine/aeo_capture_feasibility_probe_phase0_v0.md` | AEO feasibility evidence; not product-spine authority. |

## Answer-Engine / Search Current Route

For answer-engine, AEO, or search-interest work, use this
current route:

1. Start here, at the scanning spine front door.
2. Open
   `forseti/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md`
   as the proposed product-method source-family spec.
3. Open `docs/research/answer_engine/` only as research/probe evidence for that
   spec.

Do not use `docs/product/search/` or the search-lane binding record as the
current execution route. Those surfaces are historical/governance and migration
context. This route does not ratify the AEO method, authorize source capture,
scraping, scaling, schema hardening, or implementation, or convert AEO evidence
into product authority or a gate-recordable method.

## Shared Output Vocabulary

Scanning emits screen-light `frontier`, `move`, `exact_query`,
`broad_scout_return`, `precursor_signal`, `precursor_surface`, `observation`,
`candidate`, `pointer`, `negative`, `access_note`, `influence_obs`,
`venue_eval`, `hidden_venue_pointer`, `dominance_record`, and
`capture_request` records.

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
Broad-scout and other collection targets are search hygiene only: no count of
sources, rows, observations, venues, queries, or capture targets establishes
completion.

Every included scanning item must perform a named decision-material job and
must not be substitutable by an equal-or-better included item. Record a
`dominance_record` when a plausible route is rejected because another included
route supplies equal-or-better expected decision value at lower or equal cost,
latency, access risk, and duplication.

After CSB routes and hard stops, scanning treats recency/currentness as an
attention-priority signal. For same-strength URL-backed signals, a newer or
current source should normally receive more scan attention than an older source,
even when their direction differs. Prioritize current official or retailer state,
dated buyer language, recent reviews or threads, recent stockout/restock or
availability changes, and recent editorial, partner, or org-motion pointers.
Older sources remain useful for provenance, chronology, or baseline
contradiction, but they should be labeled as historical/contextual and must not
override fresh current-state reads without a load-bearing reason.

Exact-query discovery belongs to scanning. It is a bounded public-query walk
used to test CSB rows, find hidden venues, and record pointers, negatives, or
access notes. It is not search-volume proof, AEO proof, SEO keyword research,
a standing query monitor, or a crawler substitute.

Public-reaction engagement context is a scan-routing input. If a scan observes
source-visible upvotes, helpful votes, likes, views, shares, comment counts,
reply counts, source-native score state, visible sort/rank/order, or
pinned/hearted/official-response markers, it should treat them as qualitative
resonance context by default and may use them to prioritize a frontier, explain
venue value, or request Capture preservation. Direction, visible audience fit,
baseline context, manipulation risk, and ambiguity decide how much routing
priority the context deserves. Scanning must not turn those metrics into demand
proof, credibility, independence, amplification, gate clearance, graph weight,
final resonance weight, or Action Ceiling. Source-family adapters with explicit
counts, visibility, rank, or influence fields inherit this boundary.

Before closeout, a fresh CSB-first scan artifact must pass
`.agents/hooks/check_csb_scanning_artifact.py` or record why the checker was not
run. CI also runs the checker in forward-only diff mode for changed
`docs/research/` artifacts that look like CSB-first scan outputs. The checker
enforces receipt shape and mechanical public-reaction overclaim language only:
source context, caps, broad-scout accounting, CSB-row accountability,
exact-query accounting, venue/hidden-venue accounting, observations,
negatives/access notes, capture-request accounting, candidate closeout, and
explicit engagement/resonance shortcuts into proof, gate clearance, route
binding, graph weight, credibility, amplification, Action Ceiling, or final
resonance weight. It does not grade signal quality, prove buyer demand,
validate candidates, or bind Capture routes.

Scanning owns acquisition closure. Continue only while the best remaining move
has a credible chance of changing the action, action ceiling, rival assessment,
or hold condition enough to justify its marginal cost, latency, access risk,
and duplication. Close only when every material requirement is answered,
contradicted, held as a typed gap, or has no remaining non-dominated acquisition
path whose expected decision value materially exceeds those marginal costs.
A typed gap closes a requirement only when no remaining non-dominated path
whose expected decision value materially exceeds its marginal cost, latency,
access risk, and duplication could still answer it within the commission's
lawful, access, and safety bounds.

`precursor_signal` and `precursor_surface` are routing inputs. They may steer a
walk or explain why a venue deserves inspection. They are not a generic label
for every weak clue. They do not prove demand, clear a gate, authorize capture,
or create a standing source map.

## Boundary

The scanning spine is not a crawler, monitor, registry, atlas, capture runner,
ECR lane, Cleaning lane, Judgment lane, outreach lane, or buyer-contact system.
The default broad-scout phase is a bounded scan step, not a standing crawl or a
runtime mandate that every environment must provide subagents.
Run budgets, read limits, and source-policy caps remain safety boundaries. If a
cap stops a run before the acquisition-closure test is satisfied, the result is
an incomplete run with typed gaps or a hold, not completion.
When a source-family doc repeats that boundary, prefer pointing back here and to
the MGT hard boundaries while preserving source-specific hard stops.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    CSB-first scans now run a bounded broad-scout phase by default, and scanning
    treats recency/currentness as an attention-priority signal: same-strength
    newer/current signals normally receive more scan attention than older context.
    Broad scout may use a route-ledger subagent when available, but the default
    is the bounded phase, not a hard runtime dependency on subagent infrastructure.
    Fresh CSB-first scan artifacts also have a portable receipt-shape checker
    with a forward-only CI diff mode for changed docs/research CSB-first scan
    outputs; the checker enforces reviewable structure, not scan quality or
    proof.
  trigger: product_doctrine
  related_triggers:
    - workflow_authority
    - output_authority
  controlling_sources_updated:
    - forseti/product/spines/scanning/README.md
    - forseti/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - .github/workflows/ci.yml
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/hooks/check_csb_scanning_artifact.py
    - orca-harness/tests/unit/test_csb_scanning_artifact_validator.py
    - .github/workflows/ci.yml
    - forseti/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
  intentionally_not_updated:
    - path: forseti/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
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
    rg -n "broad scout|broad-scout|subagent|recent|recency|freshness|crawler|monitor|registry|atlas|capture route|gate proof|check_csb_scanning_artifact|receipt-shape|changed-file|diff mode|CI"
    forseti/product/spines/scanning docs/workflows/orca_repo_map_v0.md .agents/hooks/check_csb_scanning_artifact.py orca-harness/tests/unit/test_csb_scanning_artifact_validator.py .github/workflows/ci.yml
    (run 2026-06-24)
  stale_language_search_result: >
    Executed 2026-06-24 after edit. Hits are this accepted broad-scout/recency
    default, existing scan-core freshness/monitor safeguards, repo-map registry
    route entries, explicit no-crawler/no-monitor/no-capture-route/no-gate-proof
    boundaries, or the new CI/diff-mode checker wiring. No capless crawl,
    standing monitor, gate-proof leakage, Capture route binding, mandatory
    subagent-runtime claim, or checker-as-proof leakage was found. Checker hits
    are receipt-shape enforcement only.
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
    - forseti/product/spines/scanning/README.md
    - forseti/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
    - forseti/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
    - forseti/product/spines/scanning/source_families/reddit/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md
    - forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_lane_index_v0.md
    - forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_discovery_planning_lane_architecture_v0.md
    - forseti/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md
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
    forseti/product/spines/scanning docs/workflows/orca_repo_map_v0.md
    docs/migration/repo_structure_spine_first_v0
    plus targeted AEO path check:
    rg -n "forseti/product/spines/scanning/source_families/answer_engine/aeo_capture_feasibility_probe_phase0|docs/product/search/aeo_capture_feasibility_probe_phase0|docs/research/answer_engine/aeo_capture_feasibility_probe_phase0"
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

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
