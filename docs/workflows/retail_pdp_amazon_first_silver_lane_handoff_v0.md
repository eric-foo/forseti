# Retail/PDP Amazon-First Silver Lane Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record / cold cross-lane handoff packet
scope: >
  Transfers the missing Retail/PDP Silver-lane work to a fresh lane. Amazon is
  the first proof source, but the receiver must prefer one generic Retail/PDP
  producer over a retailer-specific Amazon silo unless fresh contract evidence
  requires a source-specific semantic boundary.
use_when:
  - Starting or resuming the Retail/PDP Silver producer work.
  - Checking why Amazon capture is available but no Amazon or Retail/PDP Silver lane exists.
  - Recovering the pinned logged-out Amazon route and its session-safety constraints.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/amazon_demand_signal_route_candidates_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - forseti-harness/data_lake/lane_registry.py
  - forseti-harness/data_lake/silver_record.py
stale_if:
  - PR 865 changes, closes without landing, or is superseded.
  - A Retail/PDP or Amazon Silver lane is registered or implemented.
  - The Retail/PDP projection row kinds or Silver Vault record contract change.
  - The anonymous Amazon session posture is replaced by a persisted-session policy.
```

# Handoff Packet

## Load Contract

- packet_version: workflow_handoff_v0
- mode: max
- source_loading_mode: repo-overlay-bound
- created_at: 2026-07-11T04:56:44+08:00
- created_by_lane: Amazon capture latency and anonymous-session lane; provenance only
- workspace: Forseti repository
- handoff_path: docs/workflows/retail_pdp_amazon_first_silver_lane_handoff_v0.md
- expected_branch: codex/amazon-capture-latency-session for this packet; receiver uses a separate worktree for implementation
- expected_head: resolve the branch ref and verify it contains this packet; parent before the packet was c0c1a7f013ca5f1e3effa96e34b08354c92dba56
- expected_dirty_state_including_handoff_file: clean after the packet and route-pin commit; stop if unrelated dirt is present
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; this packet is orientation, not authority

## Goal Handoff

- long_term_goal: Make Silver the trustworthy READ layer of the lake, with lineage-anchored and policy-fingerprinted records, explicit sibling handling, enumerated consumers, defined selection, schema-versioned record shapes, and behavior rather than artifact existence as the optimization target.
- anchor_goal: Define and build the smallest complete generic Retail/PDP Silver producer that consumes the existing projection_retail_pdp seam, with Amazon as the first real proof source.
- success_signal: A registered front-door Silver lane emits source-backed, schema-valid records for the selected Retail/PDP semantics; Amazon proof data can be re-derived through the pinned logged-out route; exact unavailable stock or sales values remain unknown rather than inferred; focused and registry gates pass.

## Open Decision / Fork

- decision: Choose the producer boundary, lane namespace, and payload split before implementation.
  - options:
    - One generic cleaning_retail_pdp_silver lane carrying ProductEntity and source-backed observation records from Retail/PDP projection rows. Recommended.
    - One Amazon-specific lane. Reject by default because it duplicates a generic upstream row contract and compounds retailer silos.
    - Keep only projection_retail_pdp and add no Silver producer. Valid only if the receiving lane demonstrates that no downstream semantic read needs a cleaned Silver record.
  - already constrained / off the table:
    - No new Silver grammar.
    - No raw-path guessing when packet, catalog, or Attachment Record refs are available.
    - No Gold or Judgment fields, demand verdicts, manufactured-demand labels, forecasts, or credibility scores.
    - No persisted Amazon cookies, user credentials, seller-account analytics, CAPTCHA solving, or gate defeat.
  - trade-offs:
    - A generic lane has lower lock-in and reuses all Retail/PDP retailers, but requires a careful payload mapping.
    - An Amazon-specific lane is faster to name but creates permanent duplication and should not be selected without a true semantic incompatibility.
    - Projection-only avoids a build but does not satisfy a request for a semantic Silver read layer when consumers require one.
  - owner of the call: receiving Data Lake / Silver lane; escalate to the owner only if current contracts leave a high-lock-in schema or lane-identity choice unresolved.
  - recommendation and why: Use one generic Retail/PDP Silver lane, with Amazon as first proof. The repository already exposes generic retail_pdp_product, retail_variant_offer, and retail_review_substrate rows and registers projection_retail_pdp, while the Silver registry contains no Amazon or Retail/PDP Silver lane.

## Drift Guard

- invariant, non-goal, or scope boundary: Success means captured and derived data passed its content, lineage, and schema gates, not HTTP 200.
  - why it matters: Amazon can return a valid transport response with the wrong locale or a sparse shell.
  - what violating it would break: It would admit false US demand observations.
- invariant, non-goal, or scope boundary: Anonymous Amazon cookies may be reused only inside one ephemeral browser context.
  - why it matters: The validated latency gain came from in-memory reuse after one ZIP setup.
  - what violating it would break: Persisting or exposing cookies would silently create an auth/session product and a new security surface.
- invariant, non-goal, or scope boundary: Every page independently confirms Amazon US pin state and its own data envelope.
  - why it matters: Cookie presence does not prove locale, product data, or content completeness.
  - what violating it would break: A stale or redirected page could be treated as usable.
- invariant, non-goal, or scope boundary: Do not fabricate exact inventory quantity or exact sold units.
  - why it matters: The public page exposed In Stock and a rounded bought-in-past-month badge, not exact quantities.
  - what violating it would break: Silver would convert missing evidence into invented facts.
- invariant, non-goal, or scope boundary: Seller Central BSA-covered analytics remain quarantined internal-only and never enter the sold signal chain.
  - why it matters: The Amazon demand-route record explicitly separates public capture, licensed inputs, and consented SP-API calibration.
  - what violating it would break: It would contaminate the public/authorized input boundary.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: .agents/workflow-overlay/source-loading.md
- targets to enter the ladder:
  - forseti-harness/data_lake/lane_registry.py
  - forseti-harness/data_lake/silver_record.py
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md
  - forseti-harness/source_capture/retail_pdp_projection.py
  - forseti/product/spines/capture/core/source_families/retail_pdp/amazon_demand_signal_route_candidates_v0.md
  - PR 865 and commit c0c1a7f013ca5f1e3effa96e34b08354c92dba56
- already loaded (weak orientation, freshness-marked; not authority): the targets above were read on 2026-07-11 from the Amazon capture worktree
- must load first (before strict or actionable steps): AGENTS.md, .agents/workflow-overlay/README.md, source-loading.md, decision-routing.md, then the Silver and Retail/PDP targets above
- load rule: receiver re-runs progressive source loading per the overlay; this packet only seeds the ladder

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- Silver is the source-backed semantic read layer, not Judgment or Gold.
  - decided in: docs/decisions/silver_vault_goal_frame_ratification_v0.md and the Silver Vault record contract
  - compare target: SHA-256 bd2180f7c632ca0157f6bc4b7923913b7e4b6b8508a90205d7e3a0b66c6040be for the goal record; SHA-256 a43abf02e63270262248948d9128806ff8bbe41c527335929cc3127e8a6ad026 for the record contract
  - verify before: choosing payloads, lane identity, or success gates
- Retail/PDP projection already normalizes source-visible product, offer, availability, and aggregate review substrate while preserving raw lineage and residuals.
  - decided in: forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md
  - compare target: SHA-256 d175c84d465ae1a3e8a1aa55f71b337fd3587e782d1c480d9404ac525b2da168
  - verify before: designing producer input or field mappings
- Amazon logged-out capture uses measured DOM profiles, ZIP 10001, condition waits, and hard content gates.
  - decided in: PR 865, the sidecar playbook, and the Amazon route pin
  - compare target: commit c0c1a7f013ca5f1e3effa96e34b08354c92dba56 plus current branch ref; playbook pre-packet SHA-256 0263cb709e11e3c6dac2df3e62cac1ff4148c19ef1d6a7df8f757a820850e196
  - verify before: any live Amazon proof or capture integration

## Active Objective

Create the missing semantic Silver read path for Retail/PDP data, using Amazon as the first proof source and the existing generic projection seam as input. Do not create a retailer-specific lane unless fresh contract analysis proves the generic route would be false or materially fragile.

## Exact Next Authorized Action

1. Create a separate clean worktree for the Silver work. Confirm whether PR 865 is merged. If it is not merged, use its branch only as source orientation or explicitly declare a stacked dependency; do not silently base a merge claim on unmerged code.
2. Run the Forseti Cynefin routing layer and inventory the current projection rows, Silver front door, lane registry, record payload contract, consumer expectations, and existing Cleaning producers.
3. Lock the smallest complete producer contract: lane namespace, input row kinds, payload kinds, raw and derived refs, observed/captured times, content-hash basis, residual behavior, and selection/consumer implications.
4. If current contracts are sufficient, implement the generic producer, register it as a Silver envelope lane, use append_silver_record, add a bounded runner or existing cadence integration only when needed for the requested producer to function, and add focused tests.
5. Prove the first slice with a fresh Amazon packet and projection produced by the pinned route. Record source-visible values only. A page that lacks exact stock or sales quantity must emit unknown or an explicit residual, never an estimate.
6. Run focused tests, .agents/hooks/check_silver_lane_registry.py --strict, relevant Silver contract tests, git diff --check, and the appropriate full harness suite. Stop on schema ambiguity, missing lineage, a required Attachment Record binding gap, or any need to persist cookies.

## Authority And Source Ledger

- Repository instructions: AGENTS.md
- Overlay or equivalent authority: .agents/workflow-overlay/
- User constraints:
  - Pin the successful Amazon route for future investigations.
  - Determine whether an Amazon Silver lane exists.
  - Hand off the missing lane.
- Source-read ledger:
  - forseti-harness/data_lake/lane_registry.py
    - Role: canonical lane registry and no-blur input
    - Load-bearing: yes
    - Compare target: SHA-256 478cbd1d4a69b82f3c73926a2c4e48cd5ebcafadac3ecba529f4a1c3506055e2
    - Last checked: 2026-07-11
    - Reuse rule: reread and rerun the registry guard before adding a lane
  - forseti-harness/data_lake/silver_record.py
    - Role: validating Silver envelope front door and record schema enforcement
    - Load-bearing: yes
    - Compare target: SHA-256 ab6b79a9cf0c6e62aa841df4a15376a4e13f94550c2371e213188fb31c1f87a2
    - Last checked: 2026-07-11
    - Reuse rule: reread before writing or validating any new Silver record
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md
    - Role: upstream generic Retail/PDP row and binding contract
    - Load-bearing: yes
    - Compare target: SHA-256 d175c84d465ae1a3e8a1aa55f71b337fd3587e782d1c480d9404ac525b2da168
    - Last checked: 2026-07-11
    - Reuse rule: reread before field mapping
  - forseti-harness/source_capture/retail_pdp_projection.py
    - Role: implemented Retail/PDP row, binding, residual, and raw-ref behavior
    - Load-bearing: yes
    - Compare target: SHA-256 e8475691738d13e6c0c5673082d83929d1779ab99d8003bfafce9e2002b9ae30
    - Last checked: 2026-07-11
    - Reuse rule: reread before selecting input rows or extending projection
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    - Role: Silver record placement, common header, Bronze intake, and semantic boundary
    - Load-bearing: yes
    - Compare target: SHA-256 a43abf02e63270262248948d9128806ff8bbe41c527335929cc3127e8a6ad026
    - Last checked: 2026-07-11
    - Reuse rule: reread before choosing payloads or refs
  - forseti/product/spines/capture/core/source_families/retail_pdp/amazon_demand_signal_route_candidates_v0.md
    - Role: Amazon public signal hierarchy, access boundaries, and pinned route
    - Load-bearing: yes
    - Compare target: SHA-256 b12ce485dc44a848703e4eb33bf812a3f640960be43a75618ce0a30ff2005ecb for the committed post-pin file
    - Last checked: 2026-07-11
    - Reuse rule: reread the committed pinned section; do not trust local scratch
  - PR 865
    - Role: branch-only implementation and live-validation lifecycle record for Amazon profiles and condition waits
    - Load-bearing: yes for the pinned capture route; no for Silver semantics
    - Compare target: head commit c0c1a7f013ca5f1e3effa96e34b08354c92dba56 before this packet update; resolve current PR head
    - Last checked: 2026-07-11
    - Reuse rule: verify current PR state and diff; do not assume merged
- Source gaps:
  - No registered Amazon or generic Retail/PDP Silver lane was found.
  - The generic Silver payload mapping for availability, price, rank, bought-badge, histogram, and customer-insight counts is not yet bound.
  - The current Retail/PDP projection carries price, availability, rating, and review count but does not yet carry every Amazon demand field visible in raw capture.
- Strict-only blockers:
  - A required payload or lineage choice that current Silver authority does not resolve.
  - PR 865 drift that invalidates the pinned capture command.
  - A missing Attachment Record or Bronze ref required by the chosen producer contract.
- Not-proven boundaries:
  - No claim that a Silver build is ready before the receiver completes source loading and contract locking.
  - No claim that exact Amazon stock quantity or sold units are publicly available.
  - No claim that the ephemeral cookie experiment is a durable batch runner.

## Current Task State

- Completed:
  - Confirmed the Silver registry has no Amazon or Retail/PDP Silver lane.
  - Implemented and live-validated Amazon grid and PDP capture profiles on PR 865.
  - Demonstrated one anonymous ephemeral context can apply ZIP once and reuse in-memory cookies across PDP and grid pages.
  - Pinned the safe logged-out route and session constraints in the Amazon demand-route record.
- Partially completed:
  - Retail/PDP projection exists and can carry product, offer, availability, aggregate rating, and review count.
  - Amazon demand signals such as bought-in-past-month and best-seller rank are present in raw capture but are not all projected or Silver-bound.
- Broken or uncertain:
  - Silver lane name, payload map, producer location, and runner/cadence integration are open.
  - Exact stock quantity and exact sold units remain unavailable from the validated public route.

## Workspace State

- Branch: codex/amazon-capture-latency-session
- Head: resolve current branch; parent before this handoff was c0c1a7f013ca5f1e3effa96e34b08354c92dba56
- Dirty or untracked state before handoff: clean
- Dirty or untracked state after writing the handoff file: this new handoff file plus the Amazon route-pin edit until committed; expected clean after commit
- Target files or artifacts:
  - this handoff packet
  - Amazon demand-route record
  - PR 865
- Related worktrees or branches: current Amazon capture worktree at C:\tmp\orca-amazon-capture-latency-session; receiver must use a separate worktree for Silver implementation

## Changed / Inspected / Tested Files

- forseti/product/spines/capture/core/source_families/retail_pdp/amazon_demand_signal_route_candidates_v0.md
  - Status: modified by sender to add the route pin
  - Role: durable Amazon investigation entrypoint
  - Important observations: distinguishes implemented single-URL route from runtime-only ephemeral multi-URL proof
  - Symbols or sections: Pinned Logged-Out Investigation Route
- docs/workflows/retail_pdp_amazon_first_silver_lane_handoff_v0.md
  - Status: new
  - Role: cold-reader handoff packet
  - Important observations: routes a generic Retail/PDP Silver lane with Amazon first proof
  - Symbols or sections: Goal Handoff, Open Decision, Exact Next Authorized Action
- forseti-harness/data_lake/lane_registry.py
  - Status: inspected, unchanged
  - Role: confirms no Amazon or Retail/PDP Silver lane
  - Important observations: new Silver envelope lanes must use the front door
  - Symbols or sections: LANE_ROLES, SILVER_LANES, FRONT_DOOR_PENDING
- forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md
  - Status: inspected, unchanged
  - Role: generic upstream producer contract
  - Important observations: row kinds include retail_pdp_product, retail_variant_offer, and retail_review_substrate
  - Symbols or sections: Row Kinds And Bindings
- forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - Status: inspected, unchanged
  - Role: Silver authority
  - Important observations: records are append-only, source-backed, schema-versioned, and non-Judgment
  - Symbols or sections: Derived Record Placement, Common Record Header, Bronze Intake
- PR 865 source and tests
  - Status: implemented and validated before this handoff
  - Role: Amazon capture route
  - Important observations: full harness passed; independent review is still explicitly pending
  - Symbols or sections: Amazon profiles, ZIP condition waits, profile wait-until resolution

## Frozen Decisions

- Decision: Do not default to an Amazon-specific Silver lane.
  - Evidence: generic projection_retail_pdp exists; no source contract requires a retailer silo.
  - Consequence: receiver starts with a generic producer design and proves Amazon first.
- Decision: Keep Amazon sessions anonymous and ephemeral.
  - Evidence: successful cookie reuse required no persistent profile or storage-state file.
  - Consequence: any durable batch interface must reuse one in-memory context and close it after the bounded batch.
- Decision: Reconfirm pin and content on every page.
  - Evidence: cookies are transport state, not proof of locale or content sufficiency.
  - Consequence: no batch-level success shortcut.
- Decision: Exact Amazon quantity and exact sales are unknown on the public route.
  - Evidence: validated page exposed In Stock and a rounded bought-in-past-month badge only.
  - Consequence: Silver carries observed states and residuals, not estimates.
- Decision: Direct HTTP is not authoritative for this US route.
  - Evidence: prior probes landed in Singapore/SGD or lacked the required US offer and review envelope.
  - Consequence: the canonical route remains the rendered anonymous browser profile.

## Mutable Questions

- Question: What is the final lane namespace?
  - Why still mutable: naming is producer-owned, and no Retail/PDP Silver producer contract exists.
  - What would resolve it: receiver contract analysis and registry conventions.
- Question: Which payload kinds represent product identity, price, availability, rank, monthly-bought badge, rating, histogram, and insight counts?
  - Why still mutable: the Silver contract supplies the envelope but does not pre-bind this producer's semantic split.
  - What would resolve it: a thin producer contract grounded in existing payload vocabulary and consumers.
- Question: Should the producer consume projection JSON directly or a typed catalog/Attachment Record view?
  - Why still mutable: the correct source-backed ref and Bronze intake seam must be confirmed.
  - What would resolve it: current catalog/Attachment Record availability and raw-ref requirements.
- Question: Must the upstream projection be extended for Amazon rank, monthly-bought, histogram, and customer-insight counts?
  - Why still mutable: those fields were captured in raw DOM but are not all carried by the current generic projection.
  - What would resolve it: the receiver's smallest complete consumer requirement and field-mapping audit.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: HTTP 200 or direct-HTTP Amazon capture is sufficient.
  - Why stale or dangerous: it can preserve the wrong marketplace or a sparse shell.
  - Current replacement: rendered profile plus US pin and hard per-page content gates.
- Stale instruction, idea, artifact, or finding: persist cookies to gain latency.
  - Why stale or dangerous: it adds credential/session custody that was not needed for the measured gain.
  - Current replacement: one ephemeral anonymous context, in-memory cookie reuse, then close.
- Stale instruction, idea, artifact, or finding: exact public sold or stock quantity is available.
  - Why stale or dangerous: only rounded monthly demand and availability state were observed.
  - Current replacement: carry observed badge/rank/availability and an explicit unknown for exact values.
- Stale instruction, idea, artifact, or finding: create amazon_silver because Amazon was the probe source.
  - Why stale or dangerous: it hard-codes a retailer boundary below a generic Retail/PDP projection contract.
  - Current replacement: generic Retail/PDP Silver producer, Amazon first proof.

## Commands And Verification Evidence

- Command:
    rg -n -i "silver lane|amazon.*silver|silver.*amazon" .
  Result:
  - Passed/failed/not run: passed
  - Important output: no Amazon or Retail/PDP Silver implementation or registry entry found
  - Re-run target so the receiver can confirm rather than trust: repository root
- Command:
    inspect forseti-harness/data_lake/lane_registry.py
  Result:
  - Passed/failed/not run: passed
  - Important output: SILVER_LANES contains no Amazon or Retail/PDP lane; projection_retail_pdp is projection-role only
  - Re-run target so the receiver can confirm rather than trust: current receiver branch
- Command:
    full Amazon capture validation on PR 865
  Result:
  - Passed/failed/not run: passed before handoff
  - Important output: focused 139 tests, contract-adjacent 57 tests, full harness 100 percent, five pre-push gates
  - Re-run target so the receiver can confirm rather than trust: PR 865 diff, checks, and current tests
- Command:
    live anonymous Amazon PDP and grid probes
  Result:
  - Passed/failed/not run: passed before handoff
  - Important output: US pin and content gates passed; ephemeral session reused ZIP state without persistence
  - Re-run target so the receiver can confirm rather than trust: pinned playbook command and a fresh packet; local C:\tmp artifacts are not durable authority

## Blockers And Risks

- Blocker or risk: Generic payload mapping is not yet bound.
  - Evidence: projection row contract and Silver envelope exist, but no producer contract joins them.
  - Likely next action: write the smallest implementation-facing producer contract before source edits if the mapping remains ambiguous after inspection.
- Blocker or risk: Amazon demand fields exceed current projection fields.
  - Evidence: raw capture contains monthly-bought, rank, histogram, and insight count; current projection primarily carries offer and aggregate review substrate.
  - Likely next action: decide which fields the requested Silver consumer actually needs, then extend projection only when omission makes that outcome false.
- Blocker or risk: PR 865 is draft and independent review is pending at packet creation.
  - Evidence: PR state and commit message review disposition.
  - Likely next action: verify current PR state; do not claim main contains the route until observed.
- Blocker or risk: High-lock-in lane or schema fork.
  - Evidence: lane namespace and payload split become durable consumer contracts.
  - Likely next action: stop and request owner steering if more than one complete mapping remains materially different.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - no Amazon or Retail/PDP Silver lane exists
  - current lane registry and front-door rule
  - current Retail/PDP row kinds and raw refs
  - current Silver record envelope and Bronze intake requirements
  - current PR 865 state and Amazon route behavior
  - clean separate worktree and branch base
- Compare target for each:
  - hashes and commit IDs in the Authority And Source Ledger
  - live branch and PR refs
  - rerun registry search and relevant tests
- Load outcomes and what each means:
  - REUSE: all load-bearing facts match; continue from Exact Next Authorized Action
  - PARTIAL_REUSE: only non-load-bearing details drift; re-derive them and continue
  - STALE_REREAD_REQUIRED: a contract, branch, PR, or registry entry drifted but can be refreshed safely
  - BLOCKED_DRIFT: drift conflicts with user scope, dirty-state policy, or the generic-lane boundary
  - BLOCKED_MISSING_PACKET: this packet is absent or unreadable
  - BLOCKED_UNVERIFIABLE: a required source or lineage claim cannot be re-derived
- Sources that must be reread if drift is detected:
  - lane registry
  - Silver Vault record contract
  - Retail/PDP projection contract and implementation
  - Amazon route pin and PR 865
  - source-loading and decision-routing overlay files

## Do Not Forget

The user asked for a future-proof Amazon route and a handoff because Silver is missing. Preserve both outcomes: do not let the Silver build silently weaken the anonymous-session, per-page-pin, captured-data-not-HTTP-success constraints.
