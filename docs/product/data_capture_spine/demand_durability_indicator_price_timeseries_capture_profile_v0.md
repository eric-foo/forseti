# Demand-Durability Indicator Capture Profile — Price Time-Series v0

```yaml
retrieval_header_version: 1
artifact_role: Product-method spec (per-indicator capture profile; consumes the Capture Envelope durability delta)
scope: >
  Thin capture profile for the PRICE time-series demand-durability indicator. Names
  the price-specific capture facts (list / effective / promo separated), the capture
  method options, the temporal regime(s), pinning, series-integrity, and
  manipulability posture that drop onto the existing Capture Envelope of record +
  durability delta. Design + spec only.
  TERMINOLOGY: "indicator" is the demand-side observable here; "proxy" is reserved
  for the NETWORK sense (residential exit IPs, ProxyProfile). The keystone delta and
  demand-read taxonomy still call this concept a "proxy" — reconciliation pending
  (see deconfliction note).
use_when:
  - Specifying or reviewing capture of a price series for a demand-durability read.
  - Checking how price observations sit on the Source Capture packet + durability delta.
  - Deconflicting a price-capture proposal against the shipped (narrow) price extractor.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md       # keystone delta (pins, cold-start, series-diff, cadence, regimes)
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md  # envelope of record (obligations)
  - orca-harness/source_capture/price_payload_extraction.py                            # NARROW, source-specific price extractor (cite; does NOT cover this case)
  - docs/product/data_capture_spine/data_capture_source_access_method_plan_v0.md       # capture-method vocabulary + boundary
  - docs/product/product_lead/orca_demand_read_taxonomy_v0.md                          # the read this indicator serves
stale_if:
  - The keystone durability delta changes the five elements (pinning, cold-start, series-diff, cadence, temporal regimes).
  - The Source Capture packet schema (models.py) changes PacketTiming, hash_basis, or posture vocabularies.
  - A price-capture mechanism that actually covers retail/promo price lands (the shipped extractor does not).
  - The demand-read taxonomy or Demand-Substrate Hard Gate (buyer-proof packet) changes the price-signal role (rerouting vs event-triggered pricing).
  - An owner decision adopts, narrows, or rejects any price capture fact below.
```

- Status: `PROFILE_DRAFT_V0`
- Artifact type: Per-indicator capture profile (subordinate to the durability delta; not a new envelope, not a keystone)
- Implementation authorized: no · Feature planning authorized: no · Runtime/source-system design authorized: no · Contract hardening authorized: no (owner-gated, out of scope)

## What This Is (And Consumes)

A **thin per-indicator profile** that drops onto two existing authorities and re-specs
neither:

1. **The Capture Envelope of record** — the shipped `orca-harness/source_capture/models.py`
   packet schema + the obligation contract
   (`core_spine_v0_data_capture_spine_obligation_contract_v0.md`). All generic
   provenance/immutability facts (capture timestamp, locator, capture mode, retained
   raw payload + content hash via `PreservedFile.sha256`/`hash_basis`, decomposed
   timing, posture vocabularies, per-capture `re_capture_relationship`) come from
   there. **This profile adds no provenance field.**
2. **The Capture Envelope durability delta** —
   `capture_envelope_durability_delta_spec_v0.md` (which calls these observables
   "proxies"; same concept, renamed to "indicator" here per owner direction). The five
   durability-over-time elements (pinning, per-series cold-start marker, series-level
   recapture-diff, cadence model, three temporal regimes + cold-start inherent-limit
   cap) come from there. **This profile cites them and supplies only the price-specific
   bindings.**

On any conflict with the schema, obligation contract, or durability delta, **those
win**; treat this profile as stale and open the controlling source.

Scope note (owner, 2026-06-15): demand-durability reading is **one decision Orca can
help with**, not Orca's whole job (the engine is outside-in market & competitive
intelligence). This profile is scoped to capturing one indicator for that one
decision-type.

## The Demand Read This Indicator Serves (read-trace)

Per the demand-read taxonomy and the Demand-Substrate Hard Gate (buyer-proof packet),
price is **not** a costly-behavior signal in itself — it is the **stimulus/event**
whose downstream *effect* (price-driven rerouting: dupe-adoption, trade-down, switching
with stated cause) is the costly behavior. The taxonomy's pricing refinement is
consumed verbatim:

| Captured price fact | Serves which read | Floor/ceiling role |
| --- | --- | --- |
| Effective price level + change over time | **Brand-decision event read** (event-triggered pricing — a price move that happened or is visibly imminent, e.g. Beauty Pie 2023 repricing) | Event context; not a floor pass on its own |
| Price-move event (direction, magnitude, mechanism) | The **event** that price-driven *rerouting* attaches to (rerouting is the costly behavior, captured via review/forum switching mentions — a *different* indicator) | Enables the floor-clearing costly-behavior read elsewhere; price alone does not clear G2 |
| Promo vs full-price separation | Distinguishes a *real* durable price move (permanent defection driver → durable) from a *promo* (transient dupe-wave surge → transient) | Feeds the durable-vs-transient classification; never decided at capture |

Price-complaint **volume** is an **anti-trigger** (taxonomy, owner-ratified): chronic,
non-discriminating, ungradeable — it is **not** a price capture fact and this profile
does not capture it.

## Temporal Regime(s) — per durability delta Element 5

Price is **mixed** across slices/locators (recorded per slice, marked `mixed` at series
level):

- **Event-based** — a price *change* is a discrete event (repricing, sale start/end,
  tier change). Coverage between events is "no observed event," never "no change
  occurred."
- **Forward-only** — the *live* posted price exposes only its current value; the series
  Orca accumulates from `cold_start_at` forward is the only Orca-native history.
- **Retroactive-native (bounded)** — *some* price history is recoverable from the
  **source's own** history: archive snapshots (Wayback; recorded with
  `archive_snapshot_time`, distinct from `capture_time`), and for Amazon, third-party
  price-history aggregators (Keepa/Camel-style). Bounded by what the source/archive
  retained; recorded with the source as basis, never asserted.

**Cold-start (delta Element 2) is an inherent-limit cap** for the forward-only portion:
the pre-cold-start live-price window is uncovered by construction, only partly
recoverable to the extent retroactive-native archive/aggregator history reaches.
Capture makes the cap visible; it does not decide whether the cap is acceptable
(Judgment's call).

## Price-Specific Capture Facts (the whole job of this profile)

Each an observed `VisibleFact` (status rides unknown/not-attempted/not-applicable per
the schema). None is a score, weight, normalization, or judgment.

- **`list_price`** — the source-visible reference/"regular"/struck-through price, when
  shown.
- **`effective_price`** — the price actually charged at observation (sale price if on
  sale, else list).
- **`promo_mechanism`** — the source-visible promotion vehicle, captured as a
  **separate fact, not folded into the amount**: e.g. coded discount, gift-with-
  purchase (GWP), introductory/intro price, bundle, member price, subscribe-&-save.
  Conflating promo with full price destroys the promo-vs-permanent-move read; kept
  separate so downstream can tell a transient promo dupe-wave from a durable repricing.
- **`price_effective_date` / `price_change_event`** — the source-visible
  effective/announcement date of a price state or change, when exposed. Decomposed
  timing (Ob.8) keeps this distinct from `capture_time`.
- **tier/variant structure** — for tiered surfaces, tier name/order/descriptor/per-tier
  amount; for retail, the per-variant price (bound by `variant_pin`).

These describe **source-visible price structure** (Ob.6 raw observable + Ob.13
bundled-offer structure). They are **not** ECR fields and assert no "true"/normalized
price — currency conversion and normalization are Cleaning's, not capture's.

## Pinning (delta Element 1) — load-bearing for price

A price series silently mixing pins is non-comparable. Per observation, pin:

- **`currency_pin`** — the currency the surface presented (record the *displayed*
  currency, never infer it).
- **`locale_pin`** — the rendered locale/region; locale flips both currency and which
  price/variant shows. **Record the *effective* rendered locale**, noting that network
  exit-geo (the `ProxyProfile` timezone/locale in `proxy_profiles.py`) and explicit
  locale selectors both drive it — hold exit-geo constant across the series or record
  its change as a comparability break.
- **`variant_pin`** — the exact SKU/size/pack/edition/plan-tier observed; a 50ml↔100ml
  or tier swap makes two observations non-comparable.
- **`session_visibility_pin`** — logged-out/anonymous vs entitled/member session.
  **Critical for membership-priced brands** (e.g. Beauty Pie): member price and
  logged-out price are different surfaces; a series must hold one fixed or record the
  switch.

Unknown/unexposed pins → `unknown_with_reason` / `unavailable_by_source`, never guessed.

## Capture Method & Boundary

Method vocabulary and boundary come from the source-access method plan
(discoverable-or-entitled + disclosable; measured-ToS accepted; industrial
Bright-Data-style scraping rejected; route bindings stay capture-lane-owned). **Price
capture for this indicator is NOT a solved capability** (owner, 2026-06-15); the route
is source-dependent and, for beauty retail, unproven:

1. **Rendered/headless browser** — the likely route for beauty-retail price surfaces,
   where the price is in the rendered DOM (in-bounds per method-plan Methods 2/3/10).
   Treat as the default expectation for retail until a cheaper route is *proven* for
   the specific source.
2. **Embedded-payload extraction (browser-free) — proven on ONE SaaS source only.** The
   shipped `orca-harness/source_capture/price_payload_extraction.py` recovers tiers +
   amounts + an announcement date from embedded structured payloads over a rung-1 HTTP
   capture **without a browser** — but it is **bound to one SaaS pricing-page shape
   (OpenAI/ChatGPT tiers)** and is **unproven for beauty-retail surfaces**. Its only
   source-agnostic reusable part is the generic `extract_object_at_anchor` brace-matcher
   (a utility, not "price handled"). Use this route only where a beauty-retail source is
   *shown* to expose an equivalent embedded payload; do not assume it generalizes.
3. **Archive (Wayback)** — for retroactive-native history (Method 6); recorded with
   `archive_snapshot_time`.
4. **Third-party price-history aggregator (Keepa/Camel, Amazon)** — structured access
   (Method 1/7 family). In-bounds if disclosable, recorded as a **third-party dependency
   in provenance** (Ob.3/Ob.4 capture mode = structured access), treated as the
   source's-own-history basis, not Orca observation.
5. **Manual human-browser capture** — for high-value/infrequent checks (Method 8).

Capture mode used is disclosed (Ob.4); mode changes within a series are visible (Ob.5).

## Series Integrity (delta Element 3)

The **series-level recapture-diff** records observed price-state changes across the
ordered series (value changed, effective-date back-dated, locator migrated) — anchored
on the existing `PreservedFile.sha256` differences and source-visible change markers.
Price is **comparatively hard to fake** (it is the brand's own posted price); the main
integrity concerns are **back-dated effective dates** and **promo-as-permanent
masking** — both *recorded* as observed differences with a `tamper_deletion_visibility`
note, never *classified* as manipulation (Judgment's Signal Integrity).

## Cadence (delta Element 4)

Cadence is the **measurement-resolution + honesty knob** for the series, and it decides
four things — never the demand verdict: (1) the finest price change observable between
samples; (2) whether "price held" is real vs. an unobserved gap; (3) how confidently a
move can be called durable vs. a transient promo blip; (4) whether a recurring promo
rhythm is detectable. **It must be expressed on the indicator's sampling rhythm — hourly to daily (owner, 2026-06-15),
not the seconds-scale `CadencePlan` was built for** (intra-session anti-block jitter).
`CadencePlan` lends *vocabulary* (mode, slot count, planned offsets) only; a genuine
time-scale series cadence is a confirmed need whose primitive is a build/hardening step
(out of scope). Declare intended cadence, record realized timings + gaps as visible
limitations.

## Manipulability & Integrity Posture

Price is the **least manipulable** of the four indicators (the brand's own declared
price). Under the manipulable-input rule (buyer-proof packet G1/G2): price is
**event/stimulus input**, not a costly-behavior floor pass. The durable-vs-transient
classification of a price move is a downstream read; capture's job is to **separate
list/effective/promo and date the event** so that read is possible. Capture flags, it
does not conclude.

## Deconfliction (per-indicator)

- **Already covered — do NOT re-spec:** all envelope/provenance facts (schema +
  obligation contract); the durability-over-time elements (delta).
- **NOT covered — price capture is genuinely new here (owner, 2026-06-15):** the shipped
  `price_payload_extraction.py` is **narrow and source-specific** (one SaaS pricing-page
  shape) and does **not** handle Orca's demand-durability price capture (retail/beauty,
  promo separation, multi-source). Only its generic `extract_object_at_anchor` brace-
  matcher is reusable as a utility. Do not treat the existing extractor as "price
  handled." Net-new in this profile: the **list/effective/promo separation** for
  retail/beauty, the price-specific **pinning bindings** (esp. member-vs-logged-out for
  membership brands), the **regime classification**, and the read-trace tying price to
  event-triggered pricing + rerouting.
- **Not this profile:** price-driven *rerouting* (the costly behavior) is captured via
  review/forum switching mentions (review indicator + forum capture); org-motion /
  distribution price signals are the EDGAR/company-aggregate lane (deferred); repurchase
  indicators are deferred.

## INV-1 Preservation

Every element is **what is captured** (a fact) or **how to capture it**
(method/pin/regime) — never a weight, score, threshold, ranking, or durability verdict.
No formula or numeric scoring appears. "Promo vs permanent," "durable vs transient," and
any price-driven-demand judgment are downstream reads, consumed from the taxonomy/gate,
never decided here.

## Boundaries, Non-Goals, Non-Claims

- No build/scrape/run/deploy; no scheduler/monitor; `CadencePlan` and
  `price_payload_extraction.py` are referenced as existing primitives only.
- No edits to `models.py` or the obligation contract; whether any price fact becomes a
  schema field is contract hardening (owner-gated, out of scope).
- No ECR/Cleaning/Judgment design; no currency conversion or normalization.
- **Commissioned capture only (Ob.1) today.** Continuous monitoring of this indicator is
  owner-confirmed as wanted (2026-06-15) but is gated on a standing-capture obligation
  home that does not yet exist (see deconfliction note); this profile does not authorize
  standing collection.
- Not validation, readiness, acceptance, pressure-test discharge, source-of-truth
  promotion, buyer proof, implementation/runtime/tooling authorization, source-access
  boundary amendment, or commercial-readiness evidence.
```
