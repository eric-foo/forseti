# Creator Signal — Product Architecture & Vetting v0 Plan (Proposal v0)

```yaml
retrieval_header_version: 1
artifact_role: product_architecture_plan_pre_ratification
scope: >
  The carve-out product architecture for Creator Signal: turning the built,
  lake-verified creator registry into a customer-facing fragrance creator-
  intelligence product, plus the first customer-facing increment (Vetting v0).
  Names the god-tier north star, the KEEP/REPLACE/DEFER calls, the high-lock-in
  decisions, and the mini-god-tier staged path. Not a ratified contract; awaiting
  owner ratification.
use_when:
  - Deciding what to build next on the creator registry toward a customer product.
  - Checking whether a proposed build is mini-god-tier increment vs deferred infra.
  - Scoping the first customer-facing slice (Vetting v0).
open_next:
  - forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_cutover_architecture_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md
  - docs/decisions/forseti_mini_god_tier_doctrine_v0.md
stale_if:
  - Owner ratifies, amends, or rejects this plan (replace this status).
  - A later accepted product-architecture record supersedes the carve-out shape.
  - The customer/ICP decision changes (currently niche/indie fragrance brands).
authority_boundary: retrieval_only
```

## Status

**`RATIFIED` as the working goal for the Creator Signal carve-out** (owner-merged
via PR #550, 2026-07-01), **and evolved by *Direction Update v0.1* below.** Still
asserts no validation, readiness, buyer proof, or implementation authority — a
direction, not a build claim. Synthesized from three de-correlated in-house
architecture passes (value/WTP, lean-ship, durable-moat), a cross-vendor (ChatGPT)
god-tier pass, and home-model adjudication — see *Provenance*.

## Direction Update v0.1 (2026-07-01) — post adversarial-review + sizing + competitor teardown

Three inputs after the v0 proposal sharpen the direction. **Where this section and
the original sections below conflict, this section wins.**

**1. Sequencing is FOUNDATION-FIRST, not customer-product-first.** The near-term
work is hardening the creator registry into a **scalable, live-fed, formula-validated
data engine** (the substrate every downstream path needs — the "our runs" use). The
customer-facing product (Vetting), the SaaS-vs-consulting model, and the
brands-vs-agencies buyer are **deferred to later, evidence-gated stages** — they are
*how-to-sell* questions, and the registry is buyer-agnostic. This supersedes the
"Vetting v0 is the first build" thrust of the *Vetting v0* and *Staged path* sections
below. (Reason: with today's thin data — 33 shallow, mostly view-only profiles — a
customer product would probe a hollow thing; build the data asset first.)

**2. The moat is a proprietary, longitudinal, vertical EVIDENCE GRAPH** — not "better
influencer software" (commoditized). The defensible asset is `creator × brand ×
product × content × time × proof × relevance`, complete + fresh + provenance-backed,
for the niche. Incumbents can copy screens faster than *capture history* — so the
single most urgent operational move is to **start sustained niche capture now** (the
time-series can't be recreated later). Compete on the **flank** CreatorIQ/Tribe
structurally ignore (indie/DTC + specialist agencies + non-marketer evidence buyers);
**coexist / possibly be-acquired, not head-on displacement.** Competitor landscape +
the EMV/MIV correction are in `creator_signal_market_sizing_v0.md`.

**3. Adversarial-review corrections (accepted).**
- **Do NOT freeze a durable customer "claim contract" now** (supersedes *High-lock-in
  decision #1* below). The `F:\` sanitization forces a *thin, disposable*
  customer-projection step (mandatory) — but the versioned external claim-object schema
  is a product/interface bet to **defer until buyer evidence**, not lock pre-PMF.
- **WTP language is hypothesis, not established demand;** a customer probe's *primary
  output is WTP evidence*.
- **Provenance is data-built, but the customer-facing "verify this number" UX is
  un-designed** (lake `content_hash` lives inside snapshots, not per-shown claim).
- Any eventual customer verdict must **reflect all gaps** (engagement absence,
  freshness, sample, audience-fit), not just thin-sample downgrade; v0-class output is
  honestly a **"reach + provenance + honesty screen," not full spend-vetting** until
  data breadth improves.

**4. Sizing (rough, not demand-validated):** fragrance alone ≈ small business
(~$0.3–1.5M ARR SOM); **beauty/skincare expansion** makes it a credible Series-A-scale
vertical SaaS (~$5M ARR base Yr3); reachable ICP SAM ≈ **$100M** (not the $2B headline).
Fragrance is the **wedge**, beauty the **destination**. See the sizing memo.

**5. Open owner decisions — resolved:** (1) foundation-first — ACCEPTED; (2) buyer
(brands vs agencies) — **deferred; test both** (a GTM question, not a registry one);
(3) placement — this doc sits in the `creator_signal` product spine. New fork to
*test*, not resolve now: whether the primary buyer is a **non-marketer evidence buyer**
(investor / retail / procurement / legal) rather than a marketer.

## Product framing (the carve-out)

**What is being carved out of Orca:** the **creator registry** (Capture-owned data
contracts) + the **Creator Signal** surface (product-facing presentation) become a
standalone, customer-facing **fragrance creator-intelligence product**.

**Customer / ICP:** **niche / indie / challenger / DTC fragrance brands** that run
their own creator marketing and need to decide which creators to partner with for
launches and campaigns. Fragrance/beauty-specialist **agencies** are held as an
adjacent parallel wedge (same product) — design so we don't lock them out, but
lead with brands. Creators themselves are **not** the ICP. No real customers until
the product is built.

**Buyer's core job (design everything backward from this):** *"Tell me which
fragrance creators to spend on, and let me trust the answer enough to write the
check."* The alternative today is eyeballing YouTube/Instagram, guessing whether
numbers are real, and risking a five-figure partnership on a bought, dormant, or
off-vertical channel.

**Trajectory:** a customer-facing vetting/discovery product (primary) and internal
Capture/Scanning spine consumers (secondary) over one shared, provenance-carrying
backbone.

## The moat (why this is not "a nicer scraper")

The defensibility is the combination — none of which a field-copying scraper gets:

1. **Trust / per-number provenance** — every metric traces to a real capture with a
   source pointer + `sha256`, freshness state, sample support, and honest
   missingness (`missing != zero`). **This half is already built and is currently
   un-monetized.**
2. **Vertical depth** — fragrance-specific (the authenticity-driven "FragTok"
   community) is exactly what generic influencer tools can't give a niche brand.
3. **Longitudinal data** — repeated capture over time yields momentum / rising-star
   signal a one-off scrape lacks (not yet accruing — see the v0 note to start the
   clock cheaply).
4. **Cross-platform identity with evidence** — a real creator graph, gated on
   promoted linkage (not naive handle-matching). Reserved, not yet filled.
5. **Honesty as product** — telling a burned marketer what we *don't* know is a
   trust advantage when they're spending real money.

The hard, differentiating half (1) exists. The rest of god tier is making it
**living, broad, cross-platform, and legible to a buyer** — a product problem, not
a trust-engineering problem.

## Target architecture (north star) — a 3-tier layered graph

The existing lake cut-over already made the correct durability decision. **Keep it;
extend it upward with one new tier (the customer contract).**

```
AUTHORITATIVE LAYER   append-only lake rollup/observation records
  (truth + provenance) content-addressed; posture-coupled; per-number sha256
        │  DERIVED PROJECTION (never authoritative, always rebuildable)
        ▼
SERVING LAYER         committed snapshots  →  creator_profile_current view
  (internal read model) + freshness receipts   (denormalized; points back to lake)
        │  CUSTOMER PROJECTION (NEW — the external contract)
        ▼
SIGNAL CLAIM LAYER    per-shown-fact claim object
  (customer surface)   {value_or_none, provenance_state: show|downgrade|withhold,
                        source_ref (sanitized), freshness, sample_support, limitation}
```

### KEEP (right, compounding, do not touch)
- **Lake = append-only authoritative; snapshots + view = derived, rebuildable
  projections.** The single most important durable decision, already shipped.
  Reversibility guarantee: any projection regenerates from records; records never
  move.
- **Discovery as a swappable layer** (Option-1 now, Option-3 index later). Records
  never move; switching is an O(N) read-scan, not a migration. This is the template
  for every "defer" call below.
- **Per-number provenance + posture coupling (`missing != zero`)**, enforced in
  `validation.py`. The moat's built half — the invariant every higher tier inherits.
- **The view-over-siblings decomposition** (identity / observation / rollup /
  audience) — correct separation of update-speed and authority. Identity stays
  fenced in the linkage ledger.

### REPLACE / EVOLVE (v0-shaped; will not carry the customer product)
- **The view is no longer the terminal surface.** For a customer product it becomes
  an *internal* serving projection, and the **Signal claim layer** sits above it.
  The view's job (operator drill-back, denormalized join) and the customer's job
  (trust-calibrated show/downgrade/withhold, sanitized provenance, forbidden-claims
  enforcement) are *different contracts*. Collapsing them leaks customer-presentation
  rules into the Capture-owned validator — the exact boundary the specs already draw
  (Capture owns the view; Creator Signal owns how the buyer sees it).
- **Static JSON export → generated read model** — but only *later*. The static
  committed view stays the mechanism through Vetting v0 (cheap, CI-deterministic,
  reversible). It is replaced by a generated read model only when a write-path or a
  second live consumer forces it (trigger below).

### BUILD (currently empty)
- **The Signal claim layer** — the customer contract (new; the one v0 seam, below).
- **`creator_record` cross-platform identity spine** — schema seam + gating already
  exist (validator gates `creator_record_id` on promoted ≥2-platform linkage); **0
  records occupy it.** Reserve and gate now (costs nothing); *fill* later. Never
  fake it.

### DEFER (safely swappable — cheap now, swap later)
Storage engine (SQLite/DuckDB/OLAP), runtime service/API, vector/search index,
multitenancy/auth, the discovery index (Option 3), the freshness scheduler, and
`creator_metric_observation` reconstruction. All sit on **swappable projections,
never the authoritative layer** — so deferring them is safe by construction.

## High-lock-in decisions (get right *now*) vs safely deferrable

Get these right at or before Vetting v0 — they are expensive to reverse once a
customer binds:

1. **The customer claim contract shape** is the new sticky surface (not the view
   schema — the customer never sees the view). Every shown fact is a **claim
   object**, never a bare value; `provenance_state: show | downgrade | withhold` is
   a first-class field; it carries a stable, **sanitized** `source_ref`. Make the
   external claim object **structurally mirror the internal posture object**
   (`value_or_none` / `posture` / `posture_reason`) so trust flows through unbroken.
   *Retrofitting provenance onto a shipped value-only API is the classic painful
   rebuild; this avoids it.* Version it `_v0` and treat it as sticky from the first
   customer read.
2. **Verdict-assembly rule:** the per-creator vetting verdict is a **deterministic
   projection of stamped fields only** — no LLM/unstamped claims, no performance
   guarantee, missingness explicit. Inherit the forbidden-claims set from the
   surface contract (no zero-filled metrics, no channel-wide implication, no
   outreach/lead-list, no person-level identity/demographics).
3. **`creator_record` gate:** reserve the key, keep the promoted-link gate; **never
   collapse accounts on candidate/soft links** at the customer surface. A wrongly-
   merged creator pollutes every downstream rollup irreversibly.
4. **Vertical specificity as data, not schema:** keep fragrance-specific categories
   in values/reference data; keep the schema vertical-neutral (it already is). This
   preserves the cross-platform / multi-vertical north star without a schema
   migration.

**Safely deferrable (swap later, with the swappable-layer reasoning):** storage
engine, runtime service, discovery index, freshness scheduler, observation
reconstruction — each is a projection; the record shapes are the contract, not the
engine.

## Vetting v0 — the first customer-facing increment

**Ship a read-only "Fragrance Creator Vetting" surface over the committed 33
profiles, no backend — but route it through a thin customer-projection so v0
compounds instead of trapping.**

**Data path (the one seam):**
`creator_profile_current_view_v0.json` → **thin build-time customer projection** →
sanitized claim-object bundle → static frontend. The projection: (a) **scrubs /
relativizes operator-local paths** — the view carries **6 `F:\orca-data-lake\...`
absolute paths in the 3 Instagram profiles' provenance** (verified); these must not
reach a customer; (b) enforces the forbidden-claims set; (c) applies
`show / downgrade / withhold` (v0 can be trivial — reuse the existing
`surface_handling` thin-n downgrade). No DB, no service — a projection *function*,
not infrastructure.

**Stack:** static site (Astro/Vite/vanilla), committed JSON in via the existing
`materialize` build step, client-side filter/sort/compare over 33 rows, host static
(Vercel/Netlify/Pages) behind a shared access gate (not real auth). Refresh = re-run
`materialize` → redeploy (current manual posture). **Effort: S–M / ~3–7 focused days.**

**Feature set:**
1. **Creator list / grid** — 33 creators; card = handle, platform badge, avg/median
   views, engagement *(only the 3 IG; the 30 YT show an explicit "engagement
   unavailable — view-count only" state, never a zero)*, sample-n, freshness date.
2. **Filter + sort** — platform, avg-views band, "has engagement data," freshness.
   (This is the *vetting* verb.)
3. **Profile detail** — the surface-spec section stack: identity, aggregate
   influence, freshness, **limitations/missingness rendered prominently**, and
   **sanitized source drill-back** ("verify this number").
4. **Compare view** — 2–4 creators side-by-side on comparable stamped fields.
   (Mirrors the real buying decision — highest demo "aha.")
5. **Trust chrome** — a persistent, honest "how these numbers are made" panel
   (lake-fed, capture-time, admitted-pool not channel-wide, per-number provenance).
   The honesty *is* the sale.

**Highest-leverage first component:** the **profile-detail card that renders a
sanitized claim object** (verdict + provenance + honest missingness), built against
one IG profile (rich) and one YT profile (view-count-only) so both cases are
exercised day one. Every other view is a projection of it, and it establishes the
claim-layer seam.

**Value prioritization (by fragrance-brand willingness-to-pay):**
1. **Trustworthy per-creator vetting verdict** (verdict + receipts + honest
   missingness) — maps 1:1 to "don't waste the partnership budget." *Non-negotiable.*
2. **Compare / shortlist** — converts vetting into an allocation decision. *Include.*
3. **Engagement / authenticity signal** — the classic spend-driver (bot/bought-audience
   fear), but honestly thin today (real for 3 of 33). Sell it where it exists, name
   its absence loudly, make "extend engagement coverage" the first post-v0 investment.

*(Below the line: discovery — high WTP, blocked on roster scale; rising-star/
longitudinal — highest future margin, blocked on time-series; cross-platform
identity — low WTP until roster + multi-platform depth exist.)*

**v0 also does (cheap, protects the north star):** keep the operator `materialize`
regen cadence running so the **longitudinal time-series quietly accrues** (the future
rising-star moat needs the clock started, even though v0 doesn't sell it).

## Accepted residuals (Vetting v0) — mini-god-tier discipline

Each named, bounded, justified, with an upgrade trigger. None sits on the
authoritative layer; all sit on swappable projections or are honest disclosures.

| Residual | Why acceptable now | Upgrade trigger |
|---|---|---|
| **Static committed JSON as read model (no DB/service)** | 33 rows; client-side is instant; already validated + CI-guarded; zero lock-in | ~1k+ profiles, a write-path, or a 2nd live consumer → DuckDB-over-snapshots (read-only) |
| **Manual refresh (materialize + redeploy), no in-product live refresh** | Single-operator is the current verified posture; freshness provable on demand | Automated capture / 2nd operator / a customer freshness SLA → wire the (already-designed) scheduled drift check |
| **YouTube = view-count-only (30/33); no engagement** | Shown as explicit missingness, not zeros; demonstrates the honesty moat | A YT engagement capture path lands (drops into the same rollup shape) — the first post-v0 value investment |
| **Ideal-audience profile absent (null for all 33)** | Reach + engagement + provenance already clear the vetting bar | Source-backed audience inference is joined (surface contract already has the section) |
| **`creator_record` reserved but empty (0 cross-platform)** | ICP vets per-account; single-platform rows are honest | Source-backed ≥2-platform linkage passes human review |
| **`show/downgrade/withhold` logic minimal (thin-n downgrade only)** | The *seam* is what compounds; richer rules are additive, no contract change | Buyer signal on which claims need finer trust calibration |
| **Shared access gate, not per-customer auth** | It's a sales/design-partner demo, not self-serve SaaS; real auth is pure pre-PMF lock-in | First paying customer needs isolated/self-serve access |
| **Verdict = stamped-field summary, not a predictive score** | Surface contract forbids performance guarantees; honest descriptive verdict is compliant + more credible | Validated, source-backed scoring with named limitations *and* owner sign-off |

## Staged path (mini-god-tier increments, highest-leverage first)

| Stage | Move | Payoff | Lock-in |
|---|---|---|---|
| **0 (done)** | Trust foundation: lake-fed, freshness-checkable, capture-fed, no-drift, provenance | The moat's hard half | — |
| **1 (next)** | **Vetting v0** — customer-facing vetting + compare over the 33, via the thin claim-projection seam | Turns receipts into a "who do I pay?" answer; is the WTP probe | Low |
| **2** | Extend metric breadth where source-accessible (YT engagement capture; per-content drill) | Materially better vetting; fills the biggest honest gap | Medium (capture-side) |
| **3** | Living loop: freshness automation + discovery/admission (registry ↔ Capture/Scanning) | Self-maintaining + self-expanding — the "living" essence | Medium |
| **4** | Cross-platform `creator_record` (fill the reserved spine) | True creator-level intelligence (the cross-platform differentiator) | Medium-high |
| **5** | Query service + read-model + product surfaces (alerts, buyer-proof lists) — *only when scale/customers force it* | Commercial scale | High |

Stage 1 is the whole near-term commitment. Stages 2–3 are demand-pulled and
supply-side; 4–5 are full-god-tier and deferred until triggers fire.

## Non-goals / traps (do not build)

- **The full backend first.** The static view supports v0; backend comes after the
  customer surface proves the query shape.
- **A single vanity "creator score"** that hides sample weakness, missing
  engagement, freshness, or platform differences.
- **Admitted-pool averages presented as channel-wide influence** — keep the
  validator's limitation discipline.
- **Person-level identity, contact enrichment, follower graphs, demographics,
  outreach/lead export** — separate, higher-risk products; the surface contract
  forbids them. Inherit the forbidden set into the UI verbatim.
- **Manufactured cross-platform records** to look complete — graph pollution.
- **"While we're at it" infra** (a DB, an API, a search index mid-build) — the
  mini-god-tier drift cue; route back to owner.

## Open owner decisions (for ratification)

1. **The v0 claim-layer seam (recommended: build it).** The durable-moat lens flags
   the thin customer-projection as the one place we add structure at v0. The
   verified `F:\` path leak + the forbidden-claims requirement make a customer-
   projection step **necessary anyway** (you cannot render the raw view to a
   customer), so building it *as* the versioned claim-object seam is near-free and
   avoids a provenance retrofit later. **Recommendation: ratify the thin seam.**
   Fallback if you want the absolute minimum: render a sanitized view directly and
   accept a known future retrofit cost.
2. **ICP confirmation** — niche/indie fragrance brands as the wedge, agencies
   parallel. (Working assumption; confirm.)
3. **Doc placement** — placed in the `creator_signal` product spine (product
   architecture belongs in the product spine, not the Capture-owned registry data-
   contract folder). Say the word to co-locate it beside the registry instead.

## Provenance

Synthesized 2026-07-01 from: three de-correlated in-house architecture passes
(value/willingness-to-pay, lean-ship, durable-moat lenses); a cross-vendor
(ChatGPT) god-tier pass (overengineered infra detail discounted to north-star-only);
and home-model adjudication. Convergence across all three lenses: keep the static-
view/lake-snapshot spine, build only the thin honest decision surface. Divergence
(render-view-directly vs a claim-layer seam) resolved by the verified `F:\` leak,
which forces a customer-projection step regardless. Not validation, readiness, or
buyer proof.
```
