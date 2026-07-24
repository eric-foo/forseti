# Sephora Category Bestseller Baseline Interpretation + Timeline Readiness Handoff 2026-07-25 v1

```yaml
retrieval_header_version: 1
artifact_role: Handoff prompt
scope: >
  Read-only analytical commission to interpret five complete Sephora US-route
  category bestseller windows as a cross-sectional baseline and prepare a
  future longitudinal comparison contract without making trend, market-share,
  sales, or causality claims from one observation.
use_when:
  - Interpreting the 2026-07-25 Sephora Makeup, Skincare, Hair, Fragrance, and Bath & Body grid captures.
  - Preparing the next repeated observations and a claim-safe timeline comparison.
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/README.md
stale_if:
  - Any pinned projection is absent or hash-mismatched.
  - A later capture supersedes this five-category T0 baseline.
  - The retail-grid projection schema or interpretation authority changes materially.
authority_boundary: retrieval_only
```

## Commission Status And Prompt Preflight

This is a prepared cross-lane analytical commission. It is not dispatch-ready
until the receiver binds its current checkout, output branch, and access to the
five machine-local projection files. The handoff is orientation, not evidence
authority.

```yaml
forseti_start_preflight:
  agents_read: required_by_receiver
  overlay_read: required_by_receiver
  source_pack: custom
  edit_permission: docs-write
  target_scope: >
    One evidence-linked Sephora baseline interpretation report plus a future
    timeline comparison contract; no capture code, scheduler, monitoring
    runtime, retailer recapture, Reddit collection, or product doctrine.
  dirty_state_checked: receiver_to_verify
  blocked_if_missing: >
    Any pinned projection, a clean bounded receiver, or the current projection
    schema needed to interpret the rows truthfully.

prompt_preflight:
  output_mode: file-write
  write_destination: docs/research/sephora_category_bestseller_baseline_interpretation_20260725_v1.md
  template_kind: handoff
  template_source: workflow-handoff max packet plus project prompt contract
  input_prompt_source: docs/prompts/handoffs/sephora_category_bestseller_baseline_interpretation_timeline_readiness_handoff_20260725_v1.md
  edit_permission: docs-write
  targets:
    - docs/research/sephora_category_bestseller_baseline_interpretation_20260725_v1.md
  branch: fresh codex/ branch from current origin/main in an isolated clean receiver
  dirty_state_allowance: none before work; stop on unexpected modified or untracked paths
  reviews: no formal review implied; findings and evidence limitations precede recommendations
  doctrine_change: none; return to owner before proposing a standing analytics or cadence doctrine
  report_destination: the named research report plus a concise receiver-chat closeout
  external_source_boundary: no new external research or Reddit collection in this lane
  repo_map_decision: not_needed
  repo_map_reason: exact source artifacts, output, and non-goals are bound here

receiver_binding:
  receiver_class: receiver_to_bind
  binding_state: receiver_to_bind
  managed_starting_ref: current_origin_main_at_dispatch
  required_revision: current_origin_main_at_dispatch
  revision_mode: exact
  capability_proof: receiver_must_prove
  no_concurrent_writer_state: receiver_must_prove

thread_operating_target_continuity:
  carried_forward: no
  reason: new_cross_lane_baseline_interpretation
  changed_from_input: no
  lifecycle_status: not_supplied
  if_changed_reason: not_applicable
```

## Load Contract

- packet_version: `workflow-handoff-max-v0`
- mode: `max`
- source_loading_mode: `repo-overlay-bound`
- created_at: `2026-07-25T01:43:20+08:00`
- created_by_lane: `codex/sephora-intelligence-ulta-handoffs`; provenance only
- authoring_workspace: `C:\tmp\forseti-sephora-intelligence-ulta-handoffs`
- handoff_path: `docs/prompts/handoffs/sephora_category_bestseller_baseline_interpretation_timeline_readiness_handoff_20260725_v1.md`
- expected_authoring_branch: `codex/sephora-intelligence-ulta-handoffs`
- expected_authoring_head_before_handoff_write: `b806b2ec64cf1855565610efd7a4c116b47c87ef`
- expected_dirty_state_after_both_handoff_writes: exactly the two handoff files commissioned in this work unit
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting

Return exactly one load outcome before analysis or writing:
`REUSE`, `PARTIAL_REUSE`, `STALE_REREAD_REQUIRED`, `BLOCKED_DRIFT`,
`BLOCKED_MISSING_PACKET`, or `BLOCKED_UNVERIFIABLE`.

## Goal Handoff

- long_term_goal: Identify latent beauty-market problems and budding trends that produce defensible competitive intelligence and useful go-to-market or customer-value wedges.
- anchor_goal: Interpret the current five-category Sephora bestseller capture as a truthful cross-sectional baseline and prepare a repeat-observation timeline contract without treating one snapshot as a trend.
- success_signal: A cold reader can trace every material interpretation to the five pinned projections, distinguish observed baseline facts from hypotheses and non-claims, and run the next comparison without redesigning identity, metrics, cadence questions, or claim thresholds.

## Open Decision / Fork

- decision: Start interpretation now or wait for more observations?
  - options:
    - Wait and produce nothing until multiple time points exist.
    - Interpret T0 now as a baseline, while deferring change/trend claims.
  - already constrained / off the table:
    - One observation cannot prove movement, velocity, persistence, causality, sales, or market share.
    - The receiver must not invent missing history or infer sold units from rank, rating count, review count, or bestseller placement.
  - trade-offs:
    - Waiting avoids premature narrative but wastes the opportunity to define identities, comparison fields, failure checks, and the next-capture information job before the data arrives.
    - Baseline interpretation yields useful assortment and placement intelligence now, provided all temporal claims remain explicitly unavailable.
  - owner of the call: current Forseti owner.
  - recommendation: >
      Do not wait. Produce the cross-sectional baseline and timeline-readiness
      contract now. Treat the next observation as a change measurement, not a
      trend; require repeated scheduled observations before escalating a
      movement into a budding-trend candidate.

## Drift Guard

- Do not call this data Sephora sales, sell-through, market share, consumer demand, or the full Sephora catalog.
- Do not call any rank pattern a trend, velocity, breakout, decline, or persistence from T0 alone.
- Keep the retailer-declared result total separate from the captured top-720 window.
- Preserve category boundaries; the same product may legitimately appear in more than one category and must not be silently deduplicated across categories.
- Preserve source-product identity, placement identity, capture time, and category in every comparison.
- Rating count and projected `review_count` are source-visible grid counts, not verified written-review corpora or sales.
- The persistent geo/shipping shell does not negate the retailer-serialized US country route, but the data does not prove US delivery eligibility, shopper origin, or explicit currency code.
- Do not collect new Reddit evidence in this lane. Produce a later corroboration queue keyed to falsifiable product/brand/problem hypotheses.
- Do not add a scheduler, database, analytics framework, dashboard, standing doctrine, or new product schema.

## Inherited Context (Does Not Flow To A New Lane)

### Source-loading state to re-establish

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder:
  - the five pinned `projection.json` files under `C:\tmp`
  - `forseti-harness/source_capture/retail_grid_projection.py`
  - `forseti-harness/source_capture/sephora_catalog_grid.py`
  - `forseti/product/spines/capture/core/source_families/retail_pdp/README.md`
- already loaded by sender: the five projections and current Sephora projection/capture sources at authoring HEAD; weak orientation only
- must load first: repository instructions and overlay, then independently hash and parse all five projections before making analytical claims
- load rule: re-run progressive source loading; this packet's source list seeds the ladder but never replaces fresh source

### Earlier-decided concepts and behaviors

- The usable Sephora category set is Makeup, Skincare, Hair, Fragrance, and Bath & Body.
  - verify pointer: the five pinned projections below
  - compare target: exact SHA-256 per file
- Each category was captured as twelve consecutive retailer-native `BEST_SELLING` PageJSON pages, 60 placements per page.
  - verify pointer: each projection's completeness object and its packet's retained content/metadata
  - compare target: reread-required after hash match
- The category route certifies `retailer_serialized_country_route_only`; origin and delivery eligibility remain unpinned.
  - verify pointer: current `sephora_catalog_traversal.py` and each packet metadata file adjacent to the projection
  - compare target: current receiver revision plus projection packet root

## Active Objective

Write one evidence-linked research report that extracts the strongest
cross-sectional competitive-intelligence observations available from T0,
records candidate latent problems or GTM wedges as hypotheses rather than
findings, and defines the smallest future comparison contract.

## Exact Next Authorized Action

1. Bind a clean receiver and return the confirm-don't-trust load outcome.
2. Verify each projection file's path, byte count, SHA-256, schema, completeness, category, count, rank sequence, duplicates, and residuals.
3. Build a cross-sectional baseline covering category totals, brand concentration, cross-category footprint, rank distribution, price bands, rating/review-count posture, and source-visible badges.
4. Separate direct observations, derived arithmetic, hypotheses, and unavailable claims.
5. Identify a short queue of candidate latent problems or GTM wedges whose future truth could be tested by repeated retailer observations and later Reddit corroboration.
6. Define the T1+ comparison keys and derived deltas: rank movement, entry/exit, price change, rating/review-count change, badge change, brand/category expansion, and persistence.
7. Recommend a bounded calibration cadence and temporal claim ladder. Label thresholds as analytical heuristics, not product doctrine.
8. Write only the named research report. Stop if any projection is missing, hash-mismatched, incomplete, or semantically incompatible.

## Authority And Source Ledger

- `AGENTS.md`, `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/prompt-orchestration.md`
  - Role: repository behavior, source loading, prompt, and write authority.
  - Load-bearing: yes.
  - Compare target: current receiver checkout; reread-required.
  - Last checked: 2026-07-25 at authoring HEAD.
  - Reuse rule: current source wins.
- `forseti/product/spines/capture/core/source_families/retail_pdp/README.md`
  - Role: current Retail/PDP capture-to-lake route and non-claim boundary.
  - Load-bearing: yes.
  - Compare target: SHA-256 `a858c3d575b758fee8f9bfb88aa3ce269484d48a9b401c7fc3191774338950d6`.
  - Last checked: 2026-07-25.
  - Reuse rule: hash then reread relevant grid and non-claim sections.
- `forseti-harness/source_capture/retail_grid_projection.py`
  - Role: projection schema and Sephora completeness semantics.
  - Load-bearing: yes.
  - Compare target: authoring SHA-256 `c1fd782136b8fea1adaf710bd1a7b1e81c4b6def4bddbdcedffb2731b0c352ff`; receiver must reread current version.
  - Last checked: 2026-07-25.
  - Reuse rule: rebind to receiver revision before interpreting fields.
- `forseti-harness/source_capture/sephora_catalog_grid.py`
  - Role: retailer PageJSON extraction and serialized-country semantics.
  - Load-bearing: yes.
  - Compare target: authoring SHA-256 `89d5d2beb395d44599d4f9288641426d6cc13cc80b4ab9ef6b21da710879810d`.
  - Last checked: 2026-07-25.
  - Reuse rule: rebind to receiver revision before strict field claims.

## Pinned T0 Evidence

| Category | Projection path | Bytes | SHA-256 | Complete window |
|---|---|---:|---|---|
| Makeup | `C:\tmp\sephora_makeup_delivery_shell_12page_dogfood_20260725_v1\projection.json` | 2236943 | `537161e24303f77bdbe5272020aeba526c75abac9fac21f8a6d939b9b896480b` | 720 placements / 720 unique / declared 2513 |
| Skincare | `C:\tmp\sephora_skincare_delivery_shell_12page_dogfood_20260725_v1\projection.json` | 2255155 | `7b5437843d164fd899bddebf2070c2e827b9cf5a08616bd140fcd9404b03945e` | 720 / 720 / declared 2818 |
| Hair | `C:\tmp\sephora_hair_delivery_shell_12page_dogfood_20260725_v1\projection.json` | 2246312 | `3f15df9cbc1c350175a28f150b8163d2ad63db81a1f961b8861bc7ad8a040e69` | 720 / 720 / declared 2305 |
| Fragrance | `C:\tmp\sephora_fragrance_delivery_shell_12page_dogfood_20260725_v1\projection.json` | 2247328 | `10ae3cc0e34384f2d14202b207a4a13b2bf5e2eb2672b7ac1247605ea75e56dd` | 720 / 720 / declared 1886 |
| Bath & Body | `C:\tmp\sephora_bath_body_delivery_shell_12page_dogfood_20260725_v1\projection.json` | 2256923 | `55c5c18517daafa3384593097135f187b21732f494ff24727f8937cf0da8a1cb` | 720 / 720 / declared 830 |

Authoring verification observed for every row above: completeness `complete`,
termination `requested_page_window_reconciled`, ranks `1-720`, zero duplicate
placements, zero projection-level completeness residuals, 12/12 serialized
country values `US`, and `access_blocked=false`. These are claims to re-derive,
not premises to inherit.

## Required Report Shape

1. Executive baseline: what is directly visible now.
2. Category comparison: coverage denominator and captured-window share.
3. Brand and product concentration.
4. Price, rating/review-count, badge, and cross-category observations.
5. Candidate latent problems / budding-trend hypotheses, each with:
   - current observation;
   - alternative explanations;
   - next retailer signal needed;
   - later Reddit corroboration question;
   - kill condition.
6. Timeline-readiness contract:
   - immutable snapshot identity;
   - row and placement keys;
   - comparable fields;
   - delta fields;
   - entry/exit and missing-data rules;
   - cadence recommendation and cost/risk rationale;
   - claim ladder from baseline → change → provisional movement → budding-trend candidate.
7. Explicit non-claims and unresolved evidence.
8. Exact next capture information job; no scheduler implementation.

## Validation And Stop Conditions

- Recompute all counts from the rows; do not copy the table without checking.
- Prove rank uniqueness and category identity independently.
- Spot-check at least three products per category against their raw projected fields.
- Seed a deliberate cross-category product collision and show that the analysis keeps both placements rather than silently deduplicating them.
- Seed or simulate one missing T1 product and show the future contract distinguishes genuine exit from incomplete capture.
- Fail closed on hash mismatch, incomplete projection, mixed schema, missing category, or non-contiguous ranks.
- Run applicable documentation and prompt gates plus `git diff --check`.
- Do not claim the report proves a trend, market share, sales, customer pain, or GTM demand.

## Frozen Decisions

- Interpret T0 now; do not wait to define the baseline and comparison contract.
- One observation supports baseline description only.
- No new capture, Reddit collection, runtime, scheduler, or doctrine in this lane.
- Retailer placement data remains evidence for hypotheses, not sales or market share.

## Mutable Questions

- Calibration cadence and minimum persistence threshold.
- Whether rank movement or entry/exit is the most stable leading indicator.
- Which hypotheses should be routed first to the existing Reddit corroboration lane.
- Whether future observations should retain 720 rows or a larger/lower retailer-native window.

## Superseded / Dangerous-To-Reuse Context

- “Top-720 equals full Sephora category corpus”: false; declared totals are larger.
- “One bestseller snapshot reveals a trend”: false.
- “Review count is demand or sales”: false.
- “US route means US delivery”: false; the route deliberately leaves delivery unpinned.
- “Cross-category duplicate product is bad data”: false unless placement identity also duplicates.

## Workspace State

- authoring branch: `codex/sephora-intelligence-ulta-handoffs`
- authoring HEAD before packet write: `b806b2ec64cf1855565610efd7a4c116b47c87ef`
- dirty state before packet write: clean
- expected dirty state after both packet writes: the two commissioned handoff files only
- receiver output target: `docs/research/sephora_category_bestseller_baseline_interpretation_20260725_v1.md`

## Confirm-Don't-Trust Checklist

- Verify packet path and receiving branch/HEAD/dirty state.
- Hash all five projections before parsing.
- Recompute the table and confirm source schema/current code.
- Treat this packet as a weak source class.
- Return `STALE_REREAD_REQUIRED` when material source drift is safely recoverable.
- Return `BLOCKED_UNVERIFIABLE` when a load-bearing projection or semantic claim cannot be re-derived.

## Receiver Return Contract

```yaml
load_outcome:
receiver_binding:
source_context_status:
projection_verification:
baseline_findings:
hypotheses:
timeline_readiness:
wrong_cause_checks:
validation:
non_claims:
output_path:
exact_next_action:
```

## Do Not Forget

The valuable move now is not to pretend T0 is a trend. It is to make T0
comparable, mine its cross-sectional signal honestly, and ensure T1 can answer
change questions without redefining the evidence after seeing the result.
