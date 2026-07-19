# Beauty Retailer Sampled-Raw With Full-Derived Flip Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Cold handoff packet for sequential beauty-retailer content-mode flips
scope: >
  Commissions field-completeness audits of the already-flipped Sephora and
  Nordstrom PDP routes, then one-retailer-at-a-time flips for the remaining
  successful beauty-retailer surfaces. Full-derived means every valuable,
  claim-bearing captured field survives while shell/chrome loss is explicit;
  sampled-raw means representative raw-plus-derived packets remain available
  for parser-fit and equivalence checks.
use_when:
  - Auditing a beauty retailer before promoting sampled-raw with full-derived.
  - Starting the next sequential Retail/PDP content-mode flip.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/content_mode_lane_flip_handoff_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - docs/research/forseti_beauty_retailer_surface_probe_results_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_storefront_pin_registry_v0.md
stale_if:
  - A listed retailer route flips, changes parser/schema, or gains a newer representative sample packet.
  - A current content record drops or adds claim-bearing fields.
  - A concurrent retailer content-mode PR changes the same runner or projection surface.
```

## Load Contract

- `packet_version`: 0
- `mode`: max
- `created_at`: 2026-07-19 Asia/Singapore
- `created_by_lane`: `codex/beauty-retail-handoffs`; provenance only
- `workspace`: Forseti repository
- `handoff_path`: `docs/workflows/forseti_beauty_retailer_sampled_raw_full_derived_flip_handoff_v0.md`
- `source_baseline`: `origin/main` at `3f606eae5a5300a9f989d4cb1201ba91cbf6f5b1`
- `expected_branch`: one fresh isolated `codex/` lane per retailer from current `origin/main`
- `expected_head`: reread required; do not reuse the baseline as an exact implementation pin
- `expected_dirty_state`: clean isolated lane with no concurrent writer before each retailer
- `load_rule`: confirm-don't-trust; compare preserved raw/sample data with the compact derived record field by field
- `source_loading_mode`: repo-overlay-bound

## Goal Handoff

- `long_term_goal`: Keep the Capture Spine compact without losing the retailer evidence needed for later company-intelligence claims or source replay.
- `anchor_goal`: Prove or repair one retailer at a time so its successful fleet captures retain full valuable derived content, representative samples retain raw plus derived, and trash shell/chrome can be discarded only after hashing.
- `success_signal`: A raw/sample-to-content comparison accounts for every claim-bearing source field, records every intentional loss, passes parser-fit and projection equivalence, and produces a fresh representative sample receipt.

## Open Decision

The first receiver should begin with **Sephora aggregate PDP**, then stop after
its audit/repair lane lands. Nordstrom aggregate PDP follows in the next owner
turn. This order audits the two routes already described as flipped before
adding more default content routes.

After those audits, choose the next retailer from the remaining queue using
current field-model readiness and active-writer state. Do not implement several
retailers in one PR merely because they share the packet seam.

## Drift Guard

- “Already flipped” is not a completeness verdict. Sephora and Nordstrom must
  be checked against the actual data they captured, just as Credo's apparently
  useful projection was found to omit variants, subscription allocations,
  ingredients, packaging claims, and review fields.
- “Full-derived” does not mean preserve the whole raw page. Retain all valuable,
  claim-bearing structured content and provenance; list discarded shell,
  duplicated chrome, and non-evidence UI in the loss ledger.
- `content` mode hashes then discards successful raw shell artifacts only after
  admission and content-record persistence. `sample` mode retains raw and
  derived. Failures and access blocks remain raw.
- Never retroactively delete legacy raw packets.
- Reuse the existing Direct HTTP or CloakBrowser runner and shared retention
  seam. Retailer-owned parsers/content models remain family-specific; do not
  create a generic retailer adapter framework, crawler, public API, or
  monitoring surface.
- One retailer per work unit and protected PR. Stop after landing that retailer.
- Do not infer demand, velocity, revenue, sell-through, market share,
  inventory depth, realized price, or representative performance.

## Inherited Context To Re-establish

- Follow `.agents/workflow-overlay/README.md` and its source-loading,
  decision-routing, validation, and safety owners.
- Read the “Beauty retailer packet audit” in
  `content_mode_lane_flip_handoff_v0.md`; it records 48 cited source packets as
  48 raw, zero content, and zero sample at the audit date.
- Read the retailer's section of
  `docs/research/forseti_beauty_retailer_surface_probe_results_v0.md`, its pin
  registry row, current capture profile, projector, content model, tests, and
  all named lake packets.
- Before selecting isolation, inspect current `origin/main`, open PRs, and
  `git worktree list`. Historical or active-looking content-mode worktrees are
  orientation only; do not write into or duplicate another actor's lane.
- Treat this packet as weak context. Current code, packets, receipts, and live
  dogfood output are the action authority.

## Current Queue And Required Double-Check

| Surface | Starting posture | Required action before promotion |
| --- | --- | --- |
| Sephora aggregate PDP | Current exact route defaults to content; historical beauty packets are raw | Reconstruct the valuable-field inventory from raw/sample data, compare it to the content record, repair any omission, and preserve a representative sample packet |
| Nordstrom aggregate PDP | Current exact route defaults to content; historical beauty packets are raw | Perform the same completeness audit; retain US/USD pin evidence and the explicitly unpinned delivery residual |
| Nordstrom brand grid | Raw | Add a retailer-owned grid content record, equivalence proof, loss ledger, and sample receipt |
| Target brand grid and PDP | Raw | Add grid/PDP content records that retain assortment, offers, review state, claims, and separate shipping/store pin context |
| Luckyscent brand grid and PDP | Raw | Add family-owned grid/PDP records; do not misuse the Walmart/Target-only grid projector |
| Amazon search/discovery and PDP | Raw | Retain seller identity, first-/third-party state, offers, subject binding, reviews, and US pin enforcement |
| Ulta PDP | Raw | Retain bound SKU, all offer/variant state, reviews, claims/ingredients when present, and US/USD assertion evidence |
| Walmart PDP | Raw | Retain bound item, offers, review state, seller/fulfillment, claims/variants when present, and origin-derived US/USD context |
| Credo PDP and Yotpo responses | Raw; generic PDP projection is incomplete | Build full derived retention for all three quantities, availability, single/subscription allocations, ingredients, packaging/sustainability wording, review aggregate/rows, sort context, incentivized state/type, and reviewer age range |
| Kohl's | Raw access-failure packets | Excluded until the separate Kohl's handoff yields a successful subject-bound packet |

Tower 28 DTC PDP/bundles/stores and the PETA/Leaping Bunny directory packets
remain separate-family backlog. They must not be silently counted as
Retail/PDP flips.

## Valuable-Field Inventory

For the selected retailer, inspect the entire admitted source state and account
for every applicable field class:

1. subject, brand, product, SKU/item ID, canonical/final URL;
2. every size, quantity, shade/variant, availability state, and selection;
3. list/current/unit/bundle/subscription/promotion prices, exact currency, and
   allocation arithmetic when the retailer exposes it;
4. aggregate rating, rating/review counts, distribution, review rows, sorting
   context, verification, incentivized state/type, reviewer-declared
   demographics, and pagination/substrate limits;
5. ingredients, directions, product claims, certifications/logos, packaging
   and sustainability wording;
6. seller, first-/third-party identity, fulfillment, stock language, and
   promotion labels;
7. storefront country, currency, delivery/store context, session posture,
   requested/final URL, access status, and pin limitations;
8. source anchors, excerpts or structured bindings, capture time, parser/schema
   versions, raw hashes, warnings, and the loss ledger.

Absence from this generic inventory is not permission to discard another
valuable field discovered in the actual packet. Conversely, duplicated chrome,
navigation, scripts, styling, telemetry, and non-evidence UI may be collapsed
when the loss ledger says so.

## Exact Next Authorized Action: Sephora First

1. Create a fresh isolated `codex/` worktree from current `origin/main`.
   Confirm no open Sephora content-mode PR or concurrent writer owns the same
   files.
2. Fresh-read the current `sephora_pdp_aggregate` runner path, retailer-owned
   content model, parser-fit checker, projection, tests, pin requirements, and
   all Sephora packets cited by the beauty results register.
3. Build a field-by-field expected inventory from the preserved raw evidence
   and the actual live page. Do not infer completeness from existing tests.
4. Run one current **sample-mode** Sephora capture through the exact
   commissioned US/USD route. Preserve raw plus derived and fresh-read its
   manifest, receipt, content record, DOM/text, screenshot, hashes, warnings,
   pin evidence, and limitations.
5. Compare the sample raw state to the compact record using the valuable-field
   inventory above. Classify every source field as retained, intentionally
   collapsed with loss-ledger entry, genuinely absent, or projection gap.
6. If any valuable field is missing, make the smallest complete
   retailer-owned parser/content-model repair, bump the parser version when
   behavior changes, and rederive append-only. Do not weaken fail-closed
   admission.
7. Prove:
   - subject and US/USD pin conjunction;
   - content/sample/raw fallback semantics;
   - parser-fit match;
   - projection and Silver-equivalence expectations;
   - deterministic content record and loss ledger;
   - failure packets retain raw;
   - representative sample retains raw plus derived.
8. Update the owning content-mode handoff and beauty results audit with the new
   receipt and exact completeness verdict. Do not duplicate SOBS evidence.
9. Run focused family tests, cross-retailer capture regressions, full required
   harness/document gates, and `git diff --check`.
10. Commit, push, open and land the protected PR. Stop after Sephora; do not
    automatically begin Nordstrom.

## Frozen Decisions

- Sephora and Nordstrom are audited before expanding the number of default
  content routes.
- One representative sample receipt is required; optional sample-mode support
  without a dogfooded receipt is not sufficient.
- Valuable data is determined from the actual admitted source state, not from
  the fields the current projection already happens to expose.
- Legacy raw evidence stays immutable.
- Failure visibility takes priority over compactness.

## Mutable Questions

- Which currently flipped route, if either, omits valuable fields under live
  sample comparison.
- Whether a selected retailer needs a new family-owned content record or only a
  bounded extension of an existing one.
- The order after Sephora and Nordstrom, which depends on active lanes and
  field-model readiness at that time.

## Source-Read Ledger

| Source | Load-bearing | Compare target |
| --- | --- | --- |
| `content_mode_lane_flip_handoff_v0.md` | yes | current retail audit, flip semantics, and stop conditions |
| `source_capture_playbook_v0.md` | yes | content/sample/raw retention standard |
| Beauty retailer results register | yes | named raw packets and observed valuable fields |
| Retail storefront pin registry | yes | current route and pin dimensions |
| Selected retailer runner/parser/projector/tests | yes | current `origin/main` behavior |
| Selected retailer lake packets | yes | manifests, receipts, preserved files, hashes, and content records |
| Old content-mode worktrees or chat summaries | no | orientation only; verify current PR/branch state |

## Superseded Or Dangerous-To-Reuse Context

- Do not equate “projection succeeded” with “full-derived.”
- Do not treat 10 visible review rows as the full review corpus.
- Do not carry Credo's three-size or Yotpo field shape into another retailer as
  a universal schema.
- Do not promote Kohl's block pages into the flip queue.
- Do not delete historical raw packets after a successful new sample.
- Do not start a new runner merely because a retailer requires a family-owned
  parser; runner lifecycle and content semantics are separate concerns.

## Recovery Outcomes

- `REUSE`: sources match and no concurrent lane owns the selected retailer.
- `PARTIAL_REUSE`: route still exists but parser, schema, packet, or pin state
  advanced; rebuild the field inventory before editing.
- `STALE_REREAD_REQUIRED`: a newer flip/sample receipt supersedes this queue.
- `BLOCKED_DRIFT`: current code or packet state contradicts the handoff.
- `BLOCKED_MISSING_PACKET`: a load-bearing source packet cannot be verified.

## Completion Boundary

Each receiving turn completes exactly one retailer audit/flip and lands its own
protected PR. The first turn stops after Sephora. Kohl's remains excluded until
its separate capture-recovery handoff succeeds.
