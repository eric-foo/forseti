# Kohl's Beauty Retailer Capture Recovery Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Cold handoff packet for the final unresolved beauty-retailer capture
scope: >
  Commissions one bounded Kohl's x Tower 28 capture-recovery lane after the
  anonymous Direct HTTP, header-complete HTTP, and anonymous CloakBrowser
  routes all preserved typed Akamai access denial.
use_when:
  - Starting a fresh lane to obtain current, subject-bound Kohl's US/USD page-state evidence.
  - Deciding whether a proposed Kohl's access route is new evidence or merely repeats an exhausted rung.
authority_boundary: retrieval_only
open_next:
  - docs/research/forseti_beauty_retailer_surface_probe_results_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_storefront_pin_registry_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_anti_block_ladder_usage_guide_v0.md
stale_if:
  - A later Kohl's packet establishes a successful subject-bound route.
  - The commissioned PDP or policy URL changes.
  - A registered US browser/proxy profile or entitled retailer feed becomes available through a different named route.
```

## Load Contract

- `packet_version`: 0
- `mode`: max
- `created_at`: 2026-07-19 Asia/Singapore
- `created_by_lane`: `codex/beauty-retail-handoffs`; provenance only
- `workspace`: Forseti repository
- `handoff_path`: `docs/workflows/forseti_kohls_beauty_retailer_capture_recovery_handoff_v0.md`
- `source_baseline`: `origin/main` at `3f606eae5a5300a9f989d4cb1201ba91cbf6f5b1`
- `expected_branch`: a fresh `codex/` lane from current `origin/main`
- `expected_head`: reread required; the baseline may advance
- `expected_dirty_state`: clean isolated lane before editing; do not use or clean the dirty detached base
- `load_rule`: confirm-don't-trust; re-read every load-bearing source and lake receipt before acting
- `source_loading_mode`: repo-overlay-bound

## Goal Handoff

- `long_term_goal`: Maintain a comparable, retailer-owned US beauty surface evidence set without mistaking access workarounds or contextual geography for verified page state.
- `anchor_goal`: Obtain one current, durable Kohl's x Tower 28 LipSoftie capture that binds the commissioned product, exact USD offer state, and retailer-owned US context, or preserve one honest typed failure from a genuinely new route.
- `success_signal`: Fresh-read packet and receipt evidence supports the subject, USD, and US conjunction without `.com`, dollar-glyph, proxy-geography, search-index, or third-party substitution.

## Open Decision

The remaining access fork is external-state dependent:

1. a user-visible browser session through an owner-operated US consumer egress
   such as Surfshark;
2. a registered US residential Capture Spine profile with internally
   consistent US geo-IP, `en-US`, and US timezone metadata;
3. an entitled Kohl's affiliate feed or an owner-approved paid provider.

The current commission authorizes one bounded public-page browser/VPN
experiment when the owner-operated route is available. It does not authorize
buying access, inventing credentials or a proxy profile, or treating VPN
geography as pin proof. If no admissible external state is available, return
the existing typed blocker without replaying exhausted routes.

## Drift Guard

- Bound PDP:
  `https://www.kohls.com/product/prd-6715879/tower-28-beauty-lipsoftie-hydrating-tinted-lip-treatment-balm.jsp`.
- Bound retailer-owned policy:
  `https://www.kohls.com/faq/article/2552`.
- No cart, checkout, login, credential, raw-cookie injection, stored profile
  import, account mutation, purchase, or delivery-location mutation.
- A US VPN exit, `.com`, absence of `.sg`, a dollar glyph, or search snippet is
  context only. Admission requires the retailer-owned policy plus a
  product-bound exact `USD` signal.
- Do not repeat ordinary Direct HTTP, `anti_blocking_http`, cold anonymous
  CloakBrowser, or homepage-warmed anonymous CloakBrowser merely to obtain the
  same known denial.
- Access failures remain raw evidence. Do not build Kohl's content mode in this
  lane and do not discard a block shell.
- No demand, velocity, revenue, sell-through, inventory-depth, market-share,
  realized-price, seller-authorization, or performance inference.

## Inherited Context To Re-establish

- Follow `.agents/workflow-overlay/README.md`, then its source-loading,
  decision-routing, validation, and safety owners.
- Read the Kohl's section of
  `docs/research/forseti_beauty_retailer_surface_probe_results_v0.md`, the
  Kohl's row in `retail_storefront_pin_registry_v0.md`, and the Kohl's recon
  entry in `capture_recon_index_v0.md`.
- Read the anti-block ladder guide before selecting a route. Its historical
  Daimler/Akamai result is one configuration-specific data point, not proof
  that a header-complete request defeats Kohl's Akamai configuration.
- Treat this handoff and earlier chat as weak context. Lake manifests,
  preserved bytes, current runner code, and the current retailer pages are the
  load-bearing sources.

## Verified Starting State

The following is orientation that the receiver must fresh-read:

| Route | Packet-backed outcome |
| --- | --- |
| Direct HTTP PDP | `01KXT0245PZBHZSYJHM5376BCA`; HTTP 403, 500-byte body |
| Cold anonymous CloakBrowser PDP | `01KXT04HA0TT33RH7BAWQ38H58`; rendered Akamai `Access Denied` |
| Direct HTTP policy | `01KXT09ERZ6584J7M4J07WS706`; HTTP 403 |
| Humanized homepage-warmed policy | `01KXT3432PEF0NXEZE0VWEWMMD`; Akamai denial |
| Humanized homepage-warmed PDP | `01KXT38WKZMXVMMY18CDX3SC66`; Akamai denial |
| Header-complete HTTP PDP | `01KXTZ76J5BGQJTEP2QDCZDYHY`; HTTP 403 block shell |
| Header-complete HTTP policy | `01KXTZ77WYTPH15N1F8XNK87HC`; HTTP 403 block shell |

One separate in-app-browser scouting session reached both routes and observed
the bound product, `$16.00`, product-bound `priceCurrency=USD`, and a policy
statement limiting shipping to US/APO/FPO addresses. That scouting state was
not preserved through Capture Spine and did not isolate browser identity from
exit-IP reputation. It proves route liveness only.

Canonical/bare/mobile hosts, `/api/amp`, typeahead, and anonymous app/config
candidates were unpreserved scouting. They are not admissible exhaustion or
success evidence. The current durable verdict is:
`NO_GO_PACKET_BACKED_ANONYMOUS_HTTP_RUNGS_EXHAUSTED_AKAMAI_DENIAL_US_PROXY_PROFILE_ABSENT`.

## Exact Next Authorized Action

1. Create an isolated `codex/` worktree from fresh `origin/main`; confirm the
   commissioned URLs, runner code, open PRs, dirty state, and concurrent
   writers.
2. Fresh-read all seven named packet manifests, receipts, metadata files,
   hashes, requested/final URLs, access flags, and limitations.
3. If the owner-operated US VPN/browser route is available, capture an
   off-VPN control screenshot only when needed to bind the comparison; the
   existing off-VPN packets normally make another raw control unnecessary.
   Then perform one bounded on-VPN, user-visible browser session:
   - open the Kohl's homepage first;
   - capture the policy and bound PDP in the same session;
   - preserve viewport screenshots for both because access-state comparison is
     material here;
   - record actual egress/posture metadata without exposing secrets.
4. If a Capture Spine-compatible browser cannot consume that session, do not
   call an unpreserved browser view a packet. Diagnose the smallest lawful
   bridge from the successful user-visible session into the existing packet
   seam; add no generic adapter framework.
5. Admit success only when one consistent current evidence set contains:
   - retailer-owned policy text explicitly binding US shipping context;
   - Tower 28 LipSoftie product binding;
   - a product-bound exact `USD` currency signal and source-visible price;
   - no access-block conjunction.
6. On success, run the existing Retail/PDP projection and require anchored
   product and offer rows. Capture review aggregate/rows, variants, claims,
   ingredients, seller/fulfillment wording, and promotion state when present;
   missing fields remain typed residuals.
7. On failure, preserve the new raw block packet and stop. Do not substitute
   search results, caches, fixtures, affiliate claims, or another product.
8. Update the results register, storefront-pin registry, and recon index only
   with freshly verified evidence. Add no duplicate SOBS observations for a
   pure access failure.
9. Run focused tests for any implementation touched, the cross-retailer
   capture regressions, repository document gates, and `git diff --check`.
   Commit, push, open the lane PR, and follow the protected landing flow.

## Frozen Decisions

- Tower 28 LipSoftie is the subject binding.
- Country, currency, and delivery-location are separate dimensions.
- The anonymous no-proxy ladder is exhausted for the two commissioned routes.
- A successful public capture may use ordinary ephemeral session state created
  by the retailer UI, but no hidden state or credential is injected.
- Kohl's stays outside the sampled-raw/full-derived flip queue until a
  successful subject-bound packet exists.

## Mutable Questions

- Whether Surfshark or another owner-operated US consumer egress is active and
  reachable by the capturing browser at execution time.
- Whether success depends on exit IP, browser/TLS identity, or their
  conjunction.
- Whether the policy and PDP remain accessible in one session long enough for
  durable packet preservation.

## Source-Read Ledger

| Source | Load-bearing | Compare target |
| --- | --- | --- |
| `docs/research/forseti_beauty_retailer_surface_probe_results_v0.md` | yes | Kohl's section and seven packet IDs |
| `retail_storefront_pin_registry_v0.md` | yes | Kohl's route verdict and pin dimensions |
| `capture_recon_index_v0.md` | yes | Kohl's current recon outcome |
| `source_capture_anti_block_ladder_usage_guide_v0.md` | yes | rung scope and limitations |
| Seven named lake packets | yes | manifest, receipt, metadata, preserved hashes and bytes |
| In-app-browser scouting observation | no | route-liveness orientation only; not packet evidence |

## Superseded Or Dangerous-To-Reuse Context

- The removed homepage warm-up adapter and CLI flag were disproven; do not
  restore them without materially new evidence.
- Do not generalize the Daimler header-complete Akamai success to Kohl's.
- Do not interpret the unpreserved app catalog envelope with `count=0` as
  product absence.
- Do not report `UNKNOWN_REQUIRED_ACCESS_BLOCKED` as confirmed US, USD, or
  delivery state.

## Recovery Outcomes

- `REUSE`: starting sources and packet receipts match; a new admissible
  external-state route is available.
- `PARTIAL_REUSE`: evidence matches but a URL, runner, or access route changed;
  update the plan before capture.
- `STALE_REREAD_REQUIRED`: a later packet or retailer change supersedes the
  starting verdict.
- `BLOCKED_DRIFT`: packet hashes, subject binding, or concurrent-writer state
  conflicts with the handoff.
- `BLOCKED_MISSING_PACKET`: any load-bearing packet cannot be fresh-read.

## Completion Boundary

Stop after Kohl's is durably captured and landed, or after one genuinely new
route produces a typed, preserved failure. Do not begin retailer content-mode
flips in this lane.
