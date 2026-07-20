# Handoff Packet — Bazaarvoice Retailer Compatibility Implementation

```yaml
retrieval_header_version: 1
artifact_role: Handoff packet
scope: >
  Cold-reader implementation handoff for extending Forseti's proven Sephora
  Bazaarvoice capture route to compatible retailers with retailer-specific
  mappings and packet-backed admission.
use_when:
  - Starting the multi-retailer Bazaarvoice implementation in a fresh lane.
  - Deciding which retailer is ready for implementation versus bounded recon.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md
  - docs/research/forseti_beauty_retailer_surface_probe_results_v0.md
  - forseti-harness/source_capture/sephora_onboarding_capture.py
stale_if:
  - The owning Retail/PDP standard changes the three-role onboarding or Recent-only monitoring target.
  - A newer packet-backed retailer inventory supersedes the 2026-07-21 findings.
  - The Nordstrom production lane lands a stable review-response route or changes its product identity model.
```

## Load Contract

- packet_version: 1
- mode: max
- created_at: 2026-07-21
- created_by_lane: Bazaarvoice compatibility handoff lane; provenance only, not authority
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- handoff_path: `docs/workflows/forseti_bazaarvoice_retailer_compatibility_implementation_handoff_v0.md`
- expected_branch: `codex/bazaarvoice-compat-handoff`; receiver should start implementation from fresh `origin/main`
- expected_head: `2fe20400d7e2c0921de5d4cccc5333b381916ee3`
- expected_dirty_state_including_handoff_file: this handoff is the only intended change on its authoring branch; implementation belongs on a separate branch/worktree
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting
- source-loading_mode: repo-overlay-bound
- durable_destination_status: bound to the repository's `docs/workflows/` handoff surface

## Goal Handoff

- long_term_goal: Give Forseti a reusable, low-footprint Bazaarvoice capture route across supported retailers while preserving all commissioned review, demographic, aggregate, and Q&A evidence without request storms or duplicate derived bodies.
- anchor_goal: Prove retailer compatibility one retailer at a time, beginning with Walmart, and extract only the shared mechanics demonstrated by Sephora plus that second retailer.
- success_signal: Each enabled retailer has a verified product-family mapping, an exact preserved response fixture, a thin retailer adapter, passing unit tests, and a live packet proving the three applicable response roles without silently copying Sephora-only parameters.

## Open Decision / Fork

- decision: How should unchanged `Most Recent` monitoring responses be retained?
  - options:
    - Preserve every exact response: strongest no-change evidence, highest repeated storage.
    - Content-address the unchanged payload and preserve a per-run receipt pointing to it: recommended if the lake can do this without pretending a request was not made.
    - Preserve only a small heartbeat containing anchor, count, and hash: smallest storage, but weaker raw proof of what the source returned on that run.
  - already constrained / off the table: do not discard new review bodies; do not claim deduplication before it exists; do not block onboarding implementation on this choice.
  - trade-offs: defensibility versus repeated storage and added storage semantics.
  - owner of the call: human owner before monitoring-retention behavior is implemented.
  - recommendation and why: continue preserving exact monitoring responses until content-addressed reuse is explicitly designed and verified; it fails visibly and does not weaken evidence.

## Drift Guard

- Nordstrom uses Bazaarvoice; this is owner-confirmed and must not be re-litigated.
  - why it matters: the existing saved Nordstrom packet proves only Bazaarvoice media provenance, not the full adapter mapping. That evidence gap is about capture readiness, not provider identity.
  - what violating it would break: repeating provider recon would waste work and contradict the current owner direction.
- Nordstrom implementation is last.
  - why it matters: the broader Nordstrom capture route is still undergoing production work.
  - what violating it would break: binding an adapter to unstable product or access mechanics would create immediate rework.
- Do not build one universal retailer configuration before the Walmart comparison.
  - why it matters: only Sephora is proven end to end today; premature generalization would encode Sephora assumptions as shared truth.
  - what violating it would break: retailer-specific identifiers, filters, demographics, and Q&A behavior could be silently misrepresented.
- Do not copy Sephora request parameters merely because a page loads Bazaarvoice.
- Do not run full review or Q&A corpora. The accepted route is bounded onboarding plus anchor-based monitoring.
- Do not add schedules, fleet orchestration, Docker-per-page execution, proxy rotation, or anti-block bypass work.
- Do not change Ulta through this lane; Ulta uses PowerReviews/Apollo.
- Beauty Pie remains recon-only until a product-level response and identifier mapping are preserved.
- Existing raw packets are append-only historical evidence; never rewrite them to match the new route.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`, entered through `.agents/workflow-overlay/README.md`
- targets to enter the ladder:
  - owning standard: `forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md`
  - evidence register, section `Bazaarvoice low-footprint route findings (2026-07-21)`: `docs/research/forseti_beauty_retailer_surface_probe_results_v0.md`
  - current Sephora orchestration: `forseti-harness/source_capture/sephora_onboarding_capture.py`
  - current network seam: `forseti-harness/source_capture/adapters/sephora_bazaarvoice.py`
  - current tests: `forseti-harness/tests/unit/test_sephora_onboarding_capture.py`
- already loaded: the five targets above at `origin/main` head `2fe20400`; this is weak orientation, not authority
- must load first: overlay README, owning standard, and evidence-register compatibility section
- load rule: rerun progressive source loading; this packet only seeds the ladder

### Earlier-decided concepts and behaviors

- Onboarding has three roles: Helpful plus supported statistics, Recent, and bounded Q&A.
  - decided in: owning standard, Sephora reference profile
  - compare target: blob `6647b561b567914739ece6f7054d967d16232caf`
  - verify before: changing request construction or packet summaries
- Monitoring requests Recent only and stops when the prior last-seen review ID is found.
  - decided in: owning standard, Sephora `Monitoring` row
  - compare target: same standard blob
  - verify before: implementing monitoring pagination
- Exact bodies stay raw; compact summaries carry IDs, counts, dates, body presence, and raw-file references.
  - decided in: owning standard, `Preservation and adaptation acceptance`
  - compare target: same standard blob
  - verify before: changing summary schemas
- Cross-retailer implementation order is Walmart, Target, Kohl's, then Nordstrom.
  - decided in: packet-backed compatibility findings plus current owner direction
  - compare target: research blob `8e213656c2baee0703482e4603deb3e83c05d8c5`; Nordstrom-last is `reread-required` from the current user direction
  - verify before: starting a retailer work unit

## Active Objective

Deliver the first non-Sephora compatibility unit: prove Walmart's public
Bazaarvoice configuration and product-family mapping from preserved source,
then implement Walmart using the existing request/preservation seam. Extract a
shared Bazaarvoice core only for mechanics now proven identical across Sephora
and Walmart. Leave Target, Kohl's, and Nordstrom as ordered follow-on units.

## Exact Next Authorized Action

1. Start a fresh implementation worktree from current `origin/main`; do not use this documentation branch.
2. Re-verify the owning standard and evidence register against their compare targets.
3. Inspect Walmart packet `01KXSV9HFFEPNEXVA407318KW1` and its parent page state. Bind:
   - public Bazaarvoice client/deployment and locale;
   - retailer item ID to Bazaarvoice parent-family ID;
   - incentive-filter behavior;
   - supported demographic distributions;
   - whether a qualifying Recent response is already passive;
   - Q&A availability and source ordering.
4. Preserve one bounded Walmart response fixture before designing the adapter. If client configuration or parent-family identity is ambiguous, stop with the exact unresolved mapping; do not guess.
5. Compare the proven Walmart mechanics with Sephora. Extract only identical request construction, secret redaction, exact-response preservation, compact raw references, failure fallback, ID deduplication, and last-seen stopping into a shared core.
6. Implement the thin Walmart adapter and fixtures. Keep Sephora behavior backward-compatible at its public runner boundary; use a new parser/record version for materially changed packet shape.
7. Run focused unit tests, the relevant broader capture tests, documentation/placement gates for any touched docs, and one live packet-backed Walmart proof.
8. Land the complete Walmart unit through its own PR. Repeat the same prove-before-adapt sequence for Target, then Kohl's. Begin Nordstrom only after its production owner confirms the underlying route is stable.

## Authority And Source Ledger

- Repository instructions:
  - `AGENTS.md`
    - Role: project behavior, isolation, validation, and PR lifecycle
    - Load-bearing: yes
    - Compare target: `reread-required`
    - Last checked: 2026-07-21
    - Reuse rule: reread before implementation
- Overlay:
  - `.agents/workflow-overlay/README.md`
    - Role: entrypoint to Forseti source loading and implementation routing
    - Load-bearing: yes
    - Compare target: `reread-required`
    - Last checked: earlier in the authoring thread
    - Reuse rule: receiver must reload
- Source-read ledger:
  - `forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md`
    - Role: owning capture-depth and preservation standard
    - Load-bearing: yes
    - Compare target: git blob `6647b561b567914739ece6f7054d967d16232caf`
    - Last checked: 2026-07-21
    - Reuse rule: reread if blob differs
  - `docs/research/forseti_beauty_retailer_surface_probe_results_v0.md`
    - Role: packet-backed storage and compatibility evidence register
    - Load-bearing: yes
    - Compare target: git blob `8e213656c2baee0703482e4603deb3e83c05d8c5`
    - Last checked: 2026-07-21
    - Reuse rule: reread the Bazaarvoice section if blob differs
  - `forseti-harness/source_capture/sephora_onboarding_capture.py`
    - Role: incumbent eight-response acquisition and summary implementation
    - Load-bearing: yes
    - Compare target: git blob `251ede03a015df8688e072fcaf077f0484d4f7af`
    - Last checked: 2026-07-21
    - Reuse rule: reread before refactoring or preserving compatibility
  - `forseti-harness/source_capture/adapters/sephora_bazaarvoice.py`
    - Role: current token-safe request/response seam
    - Load-bearing: yes
    - Compare target: git blob `b160da8bdc5765af2445d507ecc63eba8b350302`
    - Last checked: 2026-07-21
    - Reuse rule: reread before extracting shared code
  - `forseti-harness/tests/unit/test_sephora_onboarding_capture.py`
    - Role: current success, failure-fallback, identity, and pagination coverage
    - Load-bearing: yes
    - Compare target: git blob `7d02153641a24b5ffcf32c65c58ca076df1c450c`
    - Last checked: 2026-07-21
    - Reuse rule: rerun and extend; do not weaken existing failure coverage
- User constraints:
  - Nordstrom is Bazaarvoice and goes last because Nordstrom remains in production.
  - Load-bearing: yes
  - Compare target: `reread-required` from the current owner instruction
- Source gaps:
  - Walmart's exact public client configuration and parent-family mapping are not bound.
  - Target and Kohl's lack archived qualifying API response fixtures.
  - Nordstrom's stable production mapping is intentionally deferred.
- Strict-only blockers:
  - no retailer is enabled without a preserved qualifying fixture and unambiguous identity mapping
- Not-proven boundaries:
  - provider presence does not prove product-family mapping, filter semantics, Q&A support, or scale safety

## Current Task State

- Completed:
  - Sephora route proven end to end in the existing runtime.
  - Low-footprint three-role target and storage implications merged in PR `#1201`, merge commit `2fe20400`.
  - Compatibility evidence recorded for Walmart, Target, Kohl's, Nordstrom, Beauty Pie, and Ulta.
- Partially completed:
  - shared-core shape is identified but must be earned through the Walmart comparison.
- Broken or uncertain:
  - monitoring unchanged-response retention remains owner-unresolved.
  - Walmart, Target, Kohl's, and Nordstrom are not yet admitted adapters.

## Workspace State

- Branch: `codex/bazaarvoice-compat-handoff`
- Head: `2fe20400d7e2c0921de5d4cccc5333b381916ee3`
- Dirty or untracked state before handoff: clean
- Dirty or untracked state after writing handoff: this handoff file is newly added until committed
- Target artifact: this handoff file only
- Related work:
  - PR `#1201` is merged and owns the documented findings.
  - Nordstrom production work is concurrent and must not be modified from this lane.

## Changed / Inspected / Tested Files

- `docs/workflows/forseti_bazaarvoice_retailer_compatibility_implementation_handoff_v0.md`
  - Status: added
  - Role: durable cold-reader implementation handoff
- The five source-ledger files above
  - Status: inspected, unchanged
  - Important observation: current runtime is still Sephora-specific and performs eight response documents
- Runtime tests
  - Status: not run; this work unit changes documentation only

## Frozen Decisions

- Preserve three onboarding response roles, not a full corpus.
- Helpful and Q&A are onboarding-only; monitoring is Recent-only.
- Promote only supported, retailer-proven demographics.
- Preserve exact bodies in raw and avoid repeating them in compact summaries.
- Prove fixture and identity mapping before enabling any adapter.
- Implementation order: Walmart, Target, Kohl's, Nordstrom.
- Nordstrom provider identity is settled; production readiness is not.

## Mutable Questions

- Monitoring unchanged-response retention.
  - Why still mutable: the owner has not chosen the defensibility/storage trade-off.
  - What resolves it: explicit owner ruling or a separately accepted storage design.
- Per-retailer Q&A and demographic support.
  - Why still mutable: provider capabilities and retailer configurations differ.
  - What resolves it: preserved retailer-specific fixtures.

## Superseded / Dangerous-To-Reuse Context

- “Nordstrom Bazaarvoice is unproven” as a provider-level conclusion.
  - Why dangerous: current owner direction confirms the provider.
  - Current replacement: provider is confirmed; adapter readiness remains unproven and deferred.
- The current Sephora eight-response shape as the desired future route.
  - Why dangerous: it repeats four demographic requests and body-heavy summaries.
  - Current replacement: the merged three-role target in the owning standard.
- A universal configuration inferred from Sephora alone.
  - Why dangerous: retailer mechanics differ.
  - Current replacement: prove Walmart, then extract only demonstrated commonality.

## Commands And Verification Evidence

- Authoring-state verification:
  ```powershell
  git rev-parse HEAD
  git status --short --branch
  git hash-object -- <source-ledger-path>
  ```
  Result:
  - head `2fe20400d7e2c0921de5d4cccc5333b381916ee3`
  - clean before the handoff file was added
  - source hashes recorded in the ledger
  - receiver must rerun against current `origin/main`
- Packet evidence:
  - preserved packet identifiers and limitations are in the research-register compatibility table
  - receiver must verified-read the exact packet before adapter claims

## Blockers And Risks

- Premature shared abstraction:
  - Evidence: only Sephora is currently proven end to end.
  - Next action: earn commonality through Walmart.
- Unstable Nordstrom route:
  - Evidence: owner says the broader lane remains in production.
  - Next action: defer without re-proving provider identity.
- Request footprint drift:
  - Evidence: the current Sephora route performs eight response documents.
  - Next action: assert request-role count and no duplicate Recent request in fixtures/tests.
- Summary storage regression:
  - Evidence: current Sephora summary is 1,437,000 bytes because it repeats inventories.
  - Next action: test that bodies remain raw and compact summaries carry references.

## Confirm-Don't-Trust Load Checklist

- Re-verify current `origin/main`, worktree cleanliness, and the five source blobs.
- Reread the owning standard and compatibility section before design.
- Verify each retailer packet and public mapping before implementation.
- Return exactly one load outcome:
  - `REUSE`: all load-bearing sources and owner constraints match; start Walmart proof.
  - `PARTIAL_REUSE`: only non-load-bearing context drifted; re-derive it and continue.
  - `STALE_REREAD_REQUIRED`: source blobs or `origin/main` moved; reread before acting.
  - `BLOCKED_DRIFT`: source changes contradict the three-role target or retailer ordering.
  - `BLOCKED_UNVERIFIABLE`: a product-family mapping cannot be derived from preserved evidence.

## Do Not Forget

- Nordstrom uses Bazaarvoice, but goes last.
- A large demographic subset can be useful without being representative.
- No adapter admission without exact preserved response evidence.
