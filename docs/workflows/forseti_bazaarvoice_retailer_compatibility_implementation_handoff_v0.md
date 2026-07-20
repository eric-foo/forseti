# Handoff Packet — Remaining Bazaarvoice Retailer Compatibility

```yaml
retrieval_header_version: 1
artifact_role: Handoff packet
scope: >
  Cold-reader handoff for testing Target, Kohl's, and finally Nordstrom against
  the proven Sephora information-extraction target after Walmart's direct
  Bazaarvoice route was exhausted without a usable public configuration.
use_when:
  - Starting the next retailer-compatibility lane.
  - Deciding whether a retailer supports the Sephora-depth evidence target
    through Bazaarvoice or another bounded public route.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md
  - docs/research/forseti_beauty_retailer_surface_probe_results_v0.md
  - forseti-harness/source_capture/sephora_onboarding_capture.py
stale_if:
  - The owning Retail/PDP standard changes the Sephora extraction target.
  - A newer packet-backed retailer probe supersedes this compatibility inventory.
  - The Nordstrom production owner declares its route stable or changes its
    product/review identity model.
```

## Load Contract

- packet_version: 2
- mode: max
- updated_at: 2026-07-21
- updated_by_lane: remaining-retailer handoff lane; provenance only, not authority
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- expected_branch: `codex/bazaarvoice-remaining-retailers-handoff`; receiver should start work from fresh `origin/main`
- expected_base: `12c3fde4fe9f4d98deafb3528e5dbd7caa894908`
- source-loading_mode: repo-overlay-bound
- load_rule: confirm-don't-trust; reread the named sources and verify current retailer evidence before acting
- durable_destination_status: updates the existing compatibility handoff rather than creating a competing continuation artifact

## Goal Handoff

- long_term_goal: Capture the deepest useful retailer product, review, demographic, aggregate, and Q&A evidence available at the lowest defensible request footprint.
- active_goal: Test Target against the Sephora extraction target using Bazaarvoice first and every other bounded public method that can expose the same information without inventing shared mechanics.
- success_signal: The lane either preserves a qualifying Target response fixture and implements a truthful retailer-specific adapter, or returns an exhausted-methods stop naming exactly which target information remains unavailable.

## Short Ask

Use the proven Sephora Bazaarvoice capture as the reference. First inventory the
information Sephora gave us and treat that as the extraction target. Try the
same Bazaarvoice technique on the retailer, then exhaust the other bounded
public methods below. Preserve whatever the retailer actually exposes, state
every missing field, and do not pretend a retailer-native endpoint is
Bazaarvoice.

## Extraction Target From Sephora

The owning standard is authoritative. At minimum, compare the candidate
retailer against these Sephora-proven information classes:

- product identity, full variant/SKU state, price, availability, claims,
  ingredients, usage, media references, and source disagreements;
- one source-ordered `Most Helpful` review response with exact review bodies,
  identifiers, dates, ratings, helpfulness, badges, incentive markers, and
  every other returned row field;
- one `Most Recent` response with exact bodies and a last-seen review ID;
- rating distribution, recommended/not-recommended counts, first/latest review
  dates, photo/video counts, and other returned review aggregates;
- age, skin type, and skin concerns when the retailer exposes them, with exact
  labels, counts, denominators, and missingness;
- one bounded answer-rich Q&A response with exact question and returned answer
  bodies when Q&A exists;
- exact raw responses as evidence, with compact summaries containing IDs,
  counts, dates, body presence, loss notes, and raw-file references rather than
  duplicated bodies.

This is an extraction target, not a parity claim. A retailer may legitimately
lack demographics, incentive filtering, Q&A, or some aggregates. Missing
information must be explicit.

## Bounded Method Order

For one representative product, inspect in this order:

1. existing preserved packet, embedded page state, and public configuration;
2. passive browser network responses produced by an ordinary product-page load;
3. a directly exposed public Bazaarvoice Reviews/Questions route;
4. rendered DOM and embedded JSON/state;
5. a retailer-owned public review endpoint, if it lawfully returns target
   information unavailable through Bazaarvoice.

Stop when these public methods are exhausted or the target is proven. Do not
add authentication bypass, secret recovery, proxy rotation, request floods, or
full-corpus pagination. Preserve one bounded fixture before implementation.

If a retailer-owned endpoint is the winning route, describe and implement it as
a retailer-native adapter. Shared code may normalize evidence roles and
preservation behavior; it must not falsely share request construction,
identifiers, filters, or provider identity.

## Retailer Sequence

1. **Target — active.**
   - Preserved packet: `01KXR823YS3V5M9E01QXP71ETC`.
   - Known clue: deployment `targetcom/main_site/production/en_US`,
     Bazaarvoice markers, and review identities.
   - Missing proof: archived response fixture, public client configuration, and
     product-to-review-family binding.
2. **Kohl's — next after Target.**
   - Preserved packet: `01KXXHBKF2GPK4M96SAV1VQKM3`.
   - Known clue: `api.bazaarvoice.com` and deployment
     `kohls/redesign/production/en_US`.
   - Missing proof: archived response fixture and product-family binding.
   - Reuse the admitted Kohl's browser route; do not reopen its unrelated access
     recovery work from this lane.
3. **Nordstrom — last.**
   - Bazaarvoice provider identity is owner-confirmed and must not be
     re-litigated.
   - Existing packet `01KXR9BNWBP8R8XKPKFJHZJTPN` proves only
     Bazaarvoice-hosted media, not a review response or adapter mapping.
   - Do not begin until the broader Nordstrom production owner confirms the
     route is stable.

Beauty Pie remains recon-only. Ulta remains outside this lane because its
current review route is PowerReviews/Apollo.

## Walmart Closed Result

Walmart is ticked off as an attempted direct Bazaarvoice extension:

- item `2150828728` mapped to product `3Y2AMXE2TTC1` and review-family ID
  `282PMOVUGY9E`;
- `Most Recent` and `Most Helpful` were visible, locale was `en_US`, only
  `Verified purchases only` was exposed, demographics and a non-incentivized
  filter were absent, and Q&A was disabled;
- the current page used Walmart's first-party persisted `ReviewsById` GraphQL
  query through `cegateway`;
- no public Bazaarvoice client/deployment configuration was found;
- no runtime change or qualifying response fixture was produced.

Therefore Walmart is not a remaining direct-Bazaarvoice candidate. A future
Walmart-native adapter is a separate work unit and must not be smuggled into
this lane or labelled Bazaarvoice.

## Exact Next Authorized Action

1. Start a fresh isolated worktree from current `origin/main`.
2. Reread the overlay entrypoint, owning standard, compatibility section, and
   Sephora reference implementation/tests.
3. Verify the Target packet and choose one representative Target beauty PDP.
4. Build a field-by-field extraction-target matrix from the Sephora profile.
5. Run the bounded method order above, preserving the first qualifying raw
   response fixture and its product-family mapping.
6. If Target exposes sufficient information, implement the smallest complete
   Target adapter with failure-visible preservation and focused tests.
7. If the methods are exhausted without a truthful route, stop before runtime
   edits and return `BLOCKED_UNVERIFIABLE` with the matrix of found versus
   missing fields.
8. Land Target independently. Repeat for Kohl's. Start Nordstrom only after its
   production-stability gate clears.

## Frozen Decisions

- Sephora defines the information-depth target, not universal provider mechanics.
- Exact bodies stay in raw evidence; compact summaries do not duplicate them.
- Onboarding uses one Helpful response, one Recent response, and one bounded Q&A
  response when those roles exist.
- Monitoring is Recent-only and stops at the prior last-seen review ID.
- No adapter is admitted without a preserved response fixture and unambiguous
  identity mapping.
- Walmart is closed for this direct-Bazaarvoice lane.
- Order is Target, Kohl's, then Nordstrom.

## Open Decision

Monitoring retention for unchanged responses remains unresolved. Preserve exact
responses until a separately approved and verified content-addressed or
heartbeat design exists; do not claim deduplication is already implemented.

## Authority And Source Ledger

- `AGENTS.md`
  - Role: project behavior, isolation, validation, and PR lifecycle.
  - Reuse: reread before implementation.
- `.agents/workflow-overlay/README.md`
  - Role: Forseti source-loading entrypoint.
  - Reuse: reread before implementation.
- `forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md`
  - Role: authoritative extraction and preservation target.
  - Compare target at this update: git blob `6647b561b567914739ece6f7054d967d16232caf`.
- `docs/research/forseti_beauty_retailer_surface_probe_results_v0.md`
  - Role: packet-backed retailer evidence and explicitly labelled later observations.
  - Compare target: reread required because this handoff update changes Walmart's status.
- `forseti-harness/source_capture/sephora_onboarding_capture.py`
  - Role: incumbent Sephora acquisition and summary implementation.
  - Compare target: git blob `251ede03a015df8688e072fcaf077f0484d4f7af`.
- `forseti-harness/source_capture/adapters/sephora_bazaarvoice.py`
  - Role: incumbent secret-safe Sephora request/response seam.
  - Compare target: git blob `b160da8bdc5765af2445d507ecc63eba8b350302`.
- `forseti-harness/tests/unit/test_sephora_onboarding_capture.py`
  - Role: current success, fallback, identity, and pagination coverage.
  - Compare target: git blob `7d02153641a24b5ffcf32c65c58ca076df1c450c`.

## Drift Guard

- Do not resume Walmart inside this lane.
- Do not copy Sephora parameters or call a retailer-native route Bazaarvoice.
- Do not extract a universal transport layer until at least two retailers prove
  identical public mechanics.
- Do not begin Nordstrom before its production-stability gate clears.
- Do not run full review/Q&A corpora, schedules, fleets, Docker-per-page,
  proxies, or anti-block bypass work.
- Existing raw packets are append-only historical evidence.

## Confirm-Don't-Trust Load Checklist

- Verify current `origin/main`, worktree cleanliness, and source blobs.
- Reread the owning standard and compatibility evidence.
- Verify the named retailer packet and current public product mapping.
- Return one outcome:
  - `REUSE`: sources match; begin Target proof.
  - `PARTIAL_REUSE`: non-load-bearing context drifted; rederive and continue.
  - `STALE_REREAD_REQUIRED`: load-bearing sources moved; reread before acting.
  - `BLOCKED_DRIFT`: the owner constraints or retailer order conflict.
  - `BLOCKED_UNVERIFIABLE`: bounded public methods cannot establish a truthful route.

## Do Not Forget

- Find as much of the Sephora information target as the retailer truly exposes.
- Try Bazaarvoice first, then exhaust the other bounded public methods.
- Missing data is a valid result; invented parity is not.
- Target first, Kohl's second, Nordstrom last.
