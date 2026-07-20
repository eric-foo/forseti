# Sephora Brand-Grid Capture Implementation Handoff

```yaml
retrieval_header_version: 1
artifact_role: Forseti implementation handoff
scope: >
  Cold-lane implementation handoff for a reusable, raw-preserving,
  pin-confirmed Sephora US/USD brand-grid capture and typed mechanical
  projection, proven on the Summer Fridays brand page.
use_when:
  - Implementing the first reusable Sephora brand-grid capture route.
  - Closing the Summer Fridays Turn A Sephora assortment-grid evidence gap.
  - Establishing retailer-visible parent-product inventory before PDP deepening.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/README.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md
  - forseti-harness/source_capture/retail_grid_projection.py
  - forseti-harness/source_capture/adapters/sephora_us_market.py
stale_if:
  - The owner changes the target from a Sephora retailer-visible assortment to a complete company catalog.
  - The Capture Spine retail-grid or Sephora market-pin authority changes before implementation begins.
  - PR 1201's accepted Sephora PDP/Bazaarvoice route is superseded.
```

## Load Contract

```yaml
packet_version: 1
mode: max
created_at: "2026-07-21"
created_by_lane: /root
source_loading_mode: repo-overlay-bound
workspace_containing_packet: C:\tmp\forseti-summer-fridays-understanding-handoff
handoff_path: docs/workflows/forseti_sephora_brand_grid_capture_implementation_handoff_v0.md
expected_read_branch: codex/summer-fridays-understanding-handoff
expected_head: dispatch commit named in the courier
pre_packet_head: 92209084214365bc5ada4e1bd8bf4d60065e4b16
expected_dirty_state_after_dispatch: clean
load_rule: >
  Confirm, do not trust. Treat this packet as orientation. Re-read the named
  current sources and verify every load-bearing compare target before any
  strict or actionable claim.
```

## Goal Handoff

```yaml
goal_handoff:
  long_term_goal: >
    Build a reliable, provenance-secure view of a beauty company's current
    product portfolio that can support later portfolio graphs and explicitly
    bounded commercial hypotheses.
  anchor_goal: >
    Implement the smallest complete reusable Sephora brand-grid capture route
    and prove it on Summer Fridays' US/USD Sephora brand page before resuming
    product-level evidence acquisition.
  success_signal: >
    One supported command preserves an exact raw Sephora brand-grid packet,
    independently confirms the US/USD storefront, and emits a hash-anchored
    typed projection with one row per visible parent product, source-visible
    price/rating/review/badge facts, grid order, and an explicit completeness
    reconciliation that fails closed rather than calling a partial grid complete.
```

## Open Decision

- Decision: choose the lowest-lock-in Sephora product-tile substrate that
  survives a current live proof.
  - Options:
    - Prefer stable retailer-serialized product state and retain rendered DOM
      anchors as corroboration.
    - Use rendered product-card structure when no stable serialized inventory is
      present, while keeping the parser retailer-local.
  - Constrained / off the table:
    - No private or credentialed API.
    - No invented fields from visual inference.
    - No generic cross-retailer normalization beyond the existing
      `RetailGridProjectionRow` source-visible contract.
    - No silent success when page-declared and extracted counts disagree.
  - Trade-offs: serialized state is usually more complete and less layout
    fragile; rendered cards are closer to visible merchandising but more
    volatile and may omit unloaded rows.
  - Owner of the call: implementation receiver, based on fresh preserved bytes
    and focused tests.
  - Recommendation: structured state first, rendered-card fallback only when
    the live packet proves it necessary. Preserve both raw substrates when
    present.

## Drift Guard

- Implement a **Sephora retailer-visible brand assortment**, not a claim of the
  company's complete global SKU catalog.
- Preserve parent-product rows separately from size, shade, scent, or kit
  variants. Do not inflate product count by treating every variant as an
  independent product.
- Do not implement a sales estimator, demand score, hero ranking, portfolio
  graph, owned-site catalog collector, monitoring scheduler, historical archive
  walk, or another retailer adapter in this work unit.
- Do not change the existing Sephora PDP/Bazaarvoice three-role route from PR
  1201 except for the narrow wiring needed to accept a product ID discovered by
  the grid. Helpful, Recent, and Q&A remain PDP companion roles.
- Review counts, ratings, grid position, badges, availability, and price are
  source-visible facts. They do not establish sales, velocity, revenue,
  sell-through, margin, demand, or commercial importance.
- Preserve every failed or partial live attempt as raw evidence with an explicit
  failure mode. Never manufacture a passing packet or projection.
- Keep delivery location unpinned unless an independent route actually proves
  it; US/USD storefront confirmation is not delivery confirmation.

## Inherited Context (Does Not Flow To A New Lane)

### Source-loading state to re-establish

- Overlay source-loading policy:
  `.agents/workflow-overlay/source-loading.md`.
- Targets to enter the ladder:
  - `forseti-harness/source_capture/retail_grid_projection.py`
  - `forseti-harness/source_capture/adapters/sephora_us_market.py`
  - `forseti-harness/runners/run_source_capture_cloakbrowser_packet.py`
  - `forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md`
- Already loaded by sender, weak orientation only, checked 2026-07-21:
  - PR 1201 metadata and patch
  - the current Summer Fridays acquisition seal and adversarial gap review
  - current retail-grid projection, Sephora profile, market adapter, runner, and
    focused test inventory
- Must load first before strict or actionable work:
  `AGENTS.md`, `.agents/workflow-overlay/README.md`, the source-loading policy,
  and the four targets above.
- Load rule: re-run progressive source loading. This packet's loaded set seeds
  the ladder but does not satisfy it.

### Earlier-decided concepts and behaviors

- PR 1201 accepted a low-footprint Sephora **PDP** companion with Helpful,
  Recent, and Q&A roles; it did not implement a brand-grid capture.
  - Decided in:
    `forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md`
  - Compare target: PR 1201 merge commit
    `2fe20400d7e2c0921de5d4cccc5333b381916ee3`, head
    `2913d0440ba2faddadb7a511f342fcbb90f1e6ba`.
  - Verify before: changing any Sephora PDP or Bazaarvoice behavior.
- The Summer Fridays Turn A seal is blocked until owner-adjudicated supplemental
  evidence is acquired; its pending recommendation includes a pin-confirmed
  Sephora US brand grid.
  - Decided in:
    `docs/workflows/forseti_beauty_summer_fridays_current_understanding_acquisition_seal_v0.md`
  - Compare target:
    SHA-256 `ea8dab59a5d9d0d9b67a8f056187f354e2edf44231a140643ba3ff295101725d`.
  - Verify before: using the live proof as Turn A evidence.
- The generic mechanical retail-grid projection is view-only and currently
  supports only Walmart and Target.
  - Decided in: `forseti-harness/source_capture/retail_grid_projection.py`
  - Compare target:
    SHA-256 `2286cfbf01fb1202081047660303686ada47f8e836e9fc1058a3eb6ea03523af`.
  - Verify before: selecting the implementation boundary.

## Active Objective

In a fresh implementation worktree, add generalized Sephora brand-grid capture
and typed projection support to the existing Capture Spine, then run one
pin-confirmed live proof against
`https://www.sephora.com/brand/summer-fridays?country_switch=us`.

This is implementation-authorized. It includes bounded runtime, tests,
retailer-source documentation, and one append-only live proof. It excludes the
later company-catalog graph and sales/demand model.

## Exact Next Authorized Action

1. Create a fresh worktree and branch `codex/sephora-brand-grid-capture` from
   current `origin/main`. Verify that PR 1201 merge commit
   `2fe20400d7e2c0921de5d4cccc5333b381916ee3` is an ancestor. Do not edit the
   Summer Fridays research worktree.
2. Reproduce the current gap from code:
   - `RetailGridRetailer` accepts only `walmart` and `target`;
   - `sephora_grid_aggregate` is fixture-bound to Laneige text;
   - the Sephora market assertion is PDP-shaped around one Sephora-sold USD
     Offer;
   - the generic runner preserves the grid raw packet but does not emit a
     Sephora grid projection.
3. Implement the smallest complete generalized route:
   - a subject-agnostic Sephora brand-grid capture profile;
   - a grid-appropriate US/USD confirmation requiring independent
     retailer-owned country and currency facts, with the country-routing dialog
     absent;
   - Sephora support in `retail_grid_projection.py`;
   - one typed row per unique parent product, retaining every duplicate
     placement as an anchored placement fact or explicit residual;
   - page-declared result count, extracted unique-parent count, scroll/pagination
     termination, duplicate count, and mismatch residuals;
   - source-visible product ID, canonical product URL, name, brand, grid
     position, category/breadcrumb when present, price/range and currency,
     rating, review count, badges, visible availability, and visible variant
     count when present;
   - raw references and anchors for every promoted field.
4. Keep the existing raw packet as authority and the projection as
   `view_only; not_cleaned; not_normalized; not_judgment_ready`. Do not add a
   new Silver schema in this work unit.
5. Add focused tests for:
   - stable Sephora extraction and parent-product deduplication;
   - missing/partial tiles;
   - count reconciliation and fail-closed mismatch;
   - grid-specific US/USD pin success and failure;
   - hash mismatch and missing raw files;
   - runner/profile wiring without breaking the PDP route.
6. Execute one live Summer Fridays proof through the supported runner. Preserve
   the packet under the explicit data root, recompute every manifest-declared
   hash, run the projection from the preserved packet, and verify:
   - subject binding is Summer Fridays;
   - US and USD are independently confirmed;
   - the page-declared total is captured;
   - every extracted product has a unique parent identity and raw anchor;
   - any mismatch, unloaded tail, duplicate, missing field, or delivery-pin gap
     remains visible.
7. Record the proof, command, packet ID, capture time, hashes, extracted count,
   page-declared count, residuals, and non-claims in
   `docs/research/forseti_sephora_brand_grid_capture_live_proof_v0.md`. Update
   the Retail/PDP standard, storefront-pin registry, and family README only
   where the proven capability changes their current facts.
8. Run focused validation before broader gates. If focused tests fail, stop and
   do not run or report broad success. If the live route cannot confirm the
   market or reconcile completeness, preserve the failed packet and return a
   blocked proof rather than widening to credentials, proxies, or another
   retailer.
9. Commit, push, open the implementation PR, complete the required review and
   validation flow, and merge only under the repository's normal lane rules.
   Return the merged commit plus the live packet/projection locators to the
   Summer Fridays Turn A lane; do not edit its seal or reseal it from the
   implementation branch.

## Forseti Prompt Preflight

```yaml
output_mode: file-write
write_destinations:
  implementation:
    - forseti-harness/source_capture/
    - forseti-harness/runners/
    - forseti-harness/tests/unit/
  proof: docs/research/forseti_sephora_brand_grid_capture_live_proof_v0.md
  bounded_authority_updates:
    - forseti/product/spines/capture/core/source_families/retail_pdp/
edit_permission: implementation-authorized
template_kind: none
receiver_binding:
  repository: C:\Users\vmon7\Desktop\projects\orca
  isolation: fresh worktree from current origin/main
  branch: codex/sephora-brand-grid-capture
  writable_root_requirement: verify before loading implementation sources
  concurrent_writer_rule: no other writer may mutate the implementation worktree
revision_mode: ancestor
minimum_base_revision: 5134bc65ed28e56c10bf9a1945189f7d69253a66
required_ancestor: 2fe20400d7e2c0921de5d4cccc5333b381916ee3
external_source_boundary: >
  Live Sephora access is authorized only for the exact Summer Fridays grid
  proof through the existing anonymous public Capture Spine route. No login,
  credential injection, challenge solving, private API, or unbounded crawl.
```

## Authority And Source Ledger

- Repository instructions:
  `AGENTS.md`.
- Overlay authority:
  `.agents/workflow-overlay/README.md`,
  `.agents/workflow-overlay/source-loading.md`,
  `.agents/workflow-overlay/decision-routing.md`,
  `.agents/workflow-overlay/validation-gates.md`.
- User constraints:
  - Do the Sephora assortment grid first.
  - Use the Capture Spine.
  - The longer-term need is a reliable SKU/product-chain view.
  - Do not misstate review-derived popularity as observed sales.
- Source-read ledger:
  - `forseti-harness/source_capture/retail_grid_projection.py`
    - Role: current typed retail-grid projection implementation.
    - Load-bearing: yes.
    - Compare target: SHA-256
      `2286cfbf01fb1202081047660303686ada47f8e836e9fc1058a3eb6ea03523af`.
    - Last checked: 2026-07-21.
    - Reuse rule: reread if hash differs; preserve existing Walmart/Target
      behavior.
  - `forseti-harness/source_capture/retail_capture_profiles.py`
    - Role: current Sephora grid/PDP capture profiles.
    - Load-bearing: yes.
    - Compare target: SHA-256
      `9cb397a7f3b28098eed248c8fe886101ba81267abc8aeddd2a0e2025232ab62a`.
    - Last checked: 2026-07-21.
    - Reuse rule: reread if hash differs; do not silently repurpose historical
      fixture semantics.
  - `forseti-harness/source_capture/adapters/sephora_us_market.py`
    - Role: current Sephora public US/USD preference and assertion.
    - Load-bearing: yes.
    - Compare target: SHA-256
      `225aae6645984cb17768a94744291dcdfcd21a2e3db7c7447c159d97ba3cacd0`.
    - Last checked: 2026-07-21.
    - Reuse rule: reread if hash differs; keep PDP behavior passing.
  - `forseti-harness/runners/run_source_capture_cloakbrowser_packet.py`
    - Role: existing anonymous raw-preserving browser packet runner.
    - Load-bearing: yes.
    - Compare target: SHA-256
      `0e8b9de2975dfd662e8660f443e51ff313b1f2d07125dd44e2ae544897df2f96`.
    - Last checked: 2026-07-21.
    - Reuse rule: reread if hash differs; reuse this runner instead of adding a
      parallel acquisition path.
  - `forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md`
    - Role: owning Retail/PDP extraction standard and PR 1201 target.
    - Load-bearing: yes.
    - Compare target: SHA-256
      `86d3fd41e0bf81a24a90311473fd95f23bd5f060ae9e646cff8b5e4be283623c`.
    - Last checked: 2026-07-21.
    - Reuse rule: reread before changing runtime or claiming route alignment.
  - `forseti/product/spines/capture/core/source_families/retail_pdp/retail_storefront_pin_registry_v0.md`
    - Role: current retailer pin facts and non-claims.
    - Load-bearing: yes.
    - Compare target: SHA-256
      `59a85b01d0650ad69a60d1c7934878de7ff39cc93a443e566b7c0cc983bcba84`.
    - Last checked: 2026-07-21.
    - Reuse rule: update only after the live proof confirms the grid-specific
      conjunction.
  - `docs/research/forseti_beauty_retailer_surface_probe_results_v0.md`
    - Role: packet-backed PR 1201 evidence and earlier grid-capture precedent.
    - Load-bearing: yes.
    - Compare target: SHA-256
      `ac30627948c451e2d084ff8226f87b8ae0168dc7bf587c5cd2693eb1a2a3b3c3`.
    - Last checked: 2026-07-21.
    - Reuse rule: evidence input only; it does not prove the new Sephora grid
      route.
  - PR 1201, `https://github.com/eric-foo/forseti/pull/1201`
    - Role: accepted low-footprint Sephora PDP/Bazaarvoice target.
    - Load-bearing: yes.
    - Compare target: merged commit
      `2fe20400d7e2c0921de5d4cccc5333b381916ee3`.
    - Last checked: 2026-07-21.
    - Reuse rule: verify from current repository history; do not trust this
      packet's summary.
- Source gaps:
  - No admitted pin-confirmed Summer Fridays Sephora brand-grid packet exists.
  - The exact current Sephora grid substrate must be established from fresh
    preserved bytes.
- Strict-only blockers:
  - PR 1201 is absent from the implementation base.
  - The receiver cannot write an isolated worktree.
  - A current route requires credentials, challenge solving, or prohibited
    access expansion.
  - US/USD or subject binding cannot be independently confirmed.
- Not-proven boundaries:
  - Company-complete SKU inventory.
  - Variant completeness beyond source-visible grid facts.
  - Sales, revenue, velocity, sell-through, margin, demand, or hero status.
  - Historical launches, discontinued products, or non-Sephora distribution.

## Current Task State

- Completed:
  - PR 1201 is merged and is an ancestor of both the current handoff branch and
    `origin/main`.
  - Raw-preserving browser capture, retail-grid projection infrastructure, and
    Sephora PDP US/USD pin machinery exist.
  - The Summer Fridays owner accepted grid-first sequencing.
- Partially completed:
  - A fixture-bound `sephora_grid_aggregate` profile exists.
  - The generic grid projection exists but supports Walmart and Target only.
- Broken or uncertain:
  - No reusable Sephora grid extractor.
  - No grid-specific completeness reconciliation.
  - No admitted Summer Fridays grid packet with a passing US/USD pin.

## Workspace State

- Packet branch: `codex/summer-fridays-understanding-handoff`.
- Pre-packet head: `92209084214365bc5ada4e1bd8bf4d60065e4b16`.
- Dispatch head: supplied in the courier and must contain this packet.
- Dirty state before packet: clean.
- Expected dirty state after packet dispatch: clean.
- Implementation base observed by sender:
  `origin/main` at `5134bc65ed28e56c10bf9a1945189f7d69253a66`;
  PR 1201 merge commit was an ancestor.
- Implementation isolation: fresh worktree and branch
  `codex/sephora-brand-grid-capture`.
- Target artifacts: runtime, focused tests, bounded Retail/PDP authority updates,
  and one live-proof receipt named above.

## Changed / Inspected / Tested Files

- `docs/workflows/forseti_sephora_brand_grid_capture_implementation_handoff_v0.md`
  - Status: added by sender.
  - Role: cold implementation packet.
- `forseti-harness/source_capture/retail_grid_projection.py`
  - Status: inspected, not changed.
  - Important observation: retailer literal is only `walmart | target`.
- `forseti-harness/source_capture/retail_capture_profiles.py`
  - Status: inspected, not changed.
  - Important observation: `sephora_grid_aggregate` requires Laneige-specific
    text and is not a reusable brand-grid profile.
- `forseti-harness/source_capture/adapters/sephora_us_market.py`
  - Status: inspected, not changed.
  - Important observation: confirmation requires a Sephora-sold USD Product
    Offer, which is PDP-shaped.
- `forseti-harness/runners/run_source_capture_cloakbrowser_packet.py`
  - Status: inspected, not changed.
  - Important observation: current Sephora content wiring is PDP-specific.
- Sender tests:
  - Not run; this packet changes no runtime.

## Frozen Decisions

- Decision: implement the Sephora grid before acquiring the remaining
  Summer Fridays PDP/review supplement.
  - Evidence: current owner instruction.
  - Consequence: grid extraction and completeness are the next runtime work,
    not another one-off manual grid read.
- Decision: reuse the Capture Spine.
  - Evidence: current owner preference and existing raw-preserving runner.
  - Consequence: no browser-plugin-only or ad hoc script becomes the evidence
    route.
- Decision: one current grid snapshot cannot support a sales ranking.
  - Evidence: grid facts are cumulative, age-confounded, self-selected, and
    channel-specific.
  - Consequence: preserve the facts needed for a later model, but do not emit
    that model here.

## Mutable Questions

- Which Sephora substrate provides the most stable complete parent-product
  inventory?
  - Why mutable: current live bytes have not been admitted under a passing pin.
  - Resolution: compare structured state and rendered-card rows in the live
    proof, then select the lowest-lock-in source with explicit fallback.
- Does the page expose a source-declared total that can be reconciled to unique
  parent products after all lazy-loading terminates?
  - Why mutable: the prior residual displayed useful product facts but failed
    its market pin.
  - Resolution: capture the current page and preserve termination/count facts.
- Should a later catalog layer merge owned-site variants and multiple retailer
  listings?
  - Why mutable: that is a separate entity-resolution and graphing work unit.
  - Resolution: commission after this grid proof and an owned Shop All capture.

## Superseded / Dangerous-To-Reuse Context

- “PR 1201 implemented Sephora assortment capture.”
  - Why dangerous: PR 1201 is PDP review/Q&A route documentation only.
  - Current replacement: this handoff commissions the missing grid primitive.
- “The Sephora grid is the company's complete SKU list.”
  - Why dangerous: it is one retailer's current parent-product assortment and
    may omit DTC exclusives, regional items, discontinued products, or variants.
  - Current replacement: label it `retailer_visible_assortment` and reconcile it
    later with owned catalog sources.
- “Review-count rank equals sales rank.”
  - Why dangerous: cumulative reviews combine sales, product age, review
    propensity, sampling, syndication, availability, and channel coverage.
  - Current replacement: preserve time-stamped review counts and later estimate
    a popularity/demand proxy with uncertainty and calibration.

## Commands And Verification Evidence

- Current repository verification:
  ```powershell
  git rev-parse HEAD
  git rev-parse origin/main
  git merge-base --is-ancestor 2fe20400d7e2c0921de5d4cccc5333b381916ee3 origin/main
  git status --short --branch
  ```
  Result:
  - Passed on 2026-07-21.
  - Handoff branch head before this packet:
    `92209084214365bc5ada4e1bd8bf4d60065e4b16`.
  - `origin/main`: `5134bc65ed28e56c10bf9a1945189f7d69253a66`.
  - PR 1201 ancestor check exit: `0`.
  - Working tree: clean.
  - Re-run target: receiver before creating the implementation worktree.
- Required focused implementation tests:
  ```powershell
  $env:PYTHONDONTWRITEBYTECODE=1
  python -m pytest -p no:cacheprovider -q --basetemp pytest_sephora_grid_tmp `
    forseti-harness/tests/unit/test_retail_grid_projection.py `
    forseti-harness/tests/unit/test_retail_capture_profiles.py `
    forseti-harness/tests/unit/test_sephora_us_market_wiring.py `
    forseti-harness/tests/unit/test_retail_precapture_flag_matrix.py
  ```
  Result:
  - Not run; implementation does not yet exist.
  - Re-run target: implementation receiver after focused code changes.
- Required documentation/repository gates:
  ```powershell
  python -B .agents/hooks/check_retrieval_header.py --changed --strict
  python -B .agents/hooks/check_repo_map_freshness.py --changed --strict
  python -B .agents/hooks/check_map_links.py --strict
  python -B .agents/hooks/check_placement.py --check
  git diff --check
  ```
  Result:
  - Not run against implementation; run after focused tests pass.

## Blockers And Risks

- Risk: a single scroll pass truncates the grid.
  - Evidence: Sephora uses lazy-loaded product grids and the prior profile uses
    one scroll pass.
  - Likely next action: implement a bounded termination rule based on stable
    unique-product count and page-declared total; stop with an incomplete
    residual when termination cannot be proven.
- Risk: the PDP market-pin assertion rejects a valid grid or falsely passes on
  an unrelated product offer.
  - Evidence: current confirmation searches for any Sephora-sold USD Product
    Offer.
  - Likely next action: separate page-kind-specific confirmation while reusing
    the country-dialog and `Sephora.renderQueryParams` mechanics.
- Risk: review counts are syndicated or variant-collapsed.
  - Evidence: Bazaarvoice and retailer presentation may aggregate identities.
  - Likely next action: preserve retailer product IDs and visible counts exactly;
    defer cross-product interpretation.
- Blocker: live capture cannot satisfy US/USD, subject, or count reconciliation.
  - Evidence: current live packet.
  - Likely next action: return the failed raw packet and a blocked proof; do not
    expand access mode.

## Confirm-Don't-Trust Load Checklist

1. Verify the packet exists on the couriered dispatch commit.
2. Verify the receiver is in a fresh writable implementation worktree with no
   concurrent writer.
3. Fetch current `origin/main`; confirm PR 1201 merge commit is an ancestor.
4. Recompute every SHA-256 in the source ledger or reread the drifted source.
5. Reconfirm from source that the grid projection lacks Sephora, the current
   grid profile is fixture-bound, and the market assertion is PDP-shaped.
6. Re-read the Summer Fridays seal before treating any live packet as Turn A
   evidence.
7. Return exactly one load outcome:
   - `REUSE`: all load-bearing facts confirmed; implement.
   - `PARTIAL_REUSE`: only non-load-bearing context drifted; rederive it.
   - `STALE_REREAD_REQUIRED`: material source drift can be safely reloaded.
   - `BLOCKED_DRIFT`: drift conflicts with target, authority, or writer state.
   - `BLOCKED_MISSING_PACKET`: this packet is unavailable.
   - `BLOCKED_UNVERIFIABLE`: a required claim cannot be rederived.

## Do Not Forget

The deliverable is not “34 products.” It is a reusable fail-closed route that
can prove whatever the current grid contains, preserve how that count was
derived, and remain honest when the page is partial.
