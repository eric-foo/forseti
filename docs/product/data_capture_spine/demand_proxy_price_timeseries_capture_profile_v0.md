# Demand Proxy — Price Time-Series Capture Profile v0

```yaml
retrieval_header_version: 1
artifact_role: Product-method spec (demand proxy capture profile — price time-series)
scope: >
  Capture profile for the price time-series demand-durability proxy. Specifies
  WHAT is captured (list price, effective/sale price, promo mechanism as
  separate fields), pinning facts, temporal regime, cold-start doctrine, and
  deconfliction note against the existing price_payload_extraction.py surface.
  Design + spec only; no contract hardening, no implementation.
use_when:
  - Specifying or reviewing commissioned price time-series captures for
    demand-durability proxy purposes.
  - Checking how price-proxy capture facts sit on top of the existing Capture
    Envelope (models.py + obligation contract).
  - Consuming the forward-only regime or cold-start inherent-limit cap for
    price time-series.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md   # Lane 1 envelope-delta (Element 1–5 consumed here)
  - orca-harness/source_capture/models.py                                            # Capture Envelope of record (schema)
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca-harness/source_capture/price_payload_extraction.py                          # Existing price extraction — cite-and-extend, do not re-spec
stale_if:
  - The Lane 1 envelope-delta spec (capture_envelope_durability_delta_spec_v0.md)
    is superseded by an owner decision that amends Element 1 (pinning), Element 2
    (cold-start marker), Element 4 (cadence), or Element 5 (temporal regimes /
    cold-start cap) in a way that conflicts with this profile.
  - The obligation contract is amended in a way that already names list/effective/
    promo price capture as first-class obligations.
  - price_payload_extraction.py is extended to cover rendered-capture variants or
    non-SPA sources in a way that overlaps this profile's scope.
downstream_consumers:
  - Future commissioned price time-series capture sessions operating under this profile.
  - demand_proxy_availability_restock_capture_profile_v0.md (sibling proxy profile).
```

- Status: `CAPTURE_PROFILE_DRAFT_V0`
- Artifact type: Product-method spec (demand proxy capture profile), not an
  envelope authority, contract amendment, or implementation authorization
- Implementation authorized: no
- Contract hardening authorized: no (owner-gated, out of scope)
- Source basis: `capture_envelope_durability_delta_spec_v0.md` (Lane 1, PR #93),
  `orca-harness/source_capture/models.py`,
  `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md`,
  `orca-harness/source_capture/price_payload_extraction.py`,
  `docs/product/product_lead/orca_buyer_proof_packet_v0.md` (INV-1, costly-behavior),
  `docs/product/product_lead/orca_demand_read_taxonomy_v0.md`

---

## Orca Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: S3 (target deepening — Lane 1 delta spec + models.py + obligation contract + price_payload_extraction.py)
  edit_permission: docs-write
  target_scope: new product-method spec for price time-series demand proxy capture
  dirty_state_checked: yes (fresh worktree off origin/main; HEAD 8e54aad)
  blocked_if_missing: Lane 1 envelope-delta spec readable at worktree path (confirmed)
```

---

## What This Is (And Is Not)

This is a **capture profile** for the price time-series demand-durability proxy.
It specifies what must be captured, how pinning works, which temporal regime
applies, and how the cold-start gap is treated — all as observed facts and
capture doctrine, never as weights, scores, or judgments.

It is **design + spec only**. It builds nothing, runs nothing, deploys nothing,
hardens no contract, and does not edit `models.py`, the obligation contract, or
`price_payload_extraction.py`. It **cites** them.

It does not define ECR fields, Cleaning transformations, or Judgment rules. It
does not assess whether any price level, change, or pattern signals durable or
hollow demand — that is downstream Judgment's call.

---

## Envelope of Record (Cited, Not Re-Derived)

The Capture Envelope of record already exists and governs this profile:

1. **Schema** — `orca-harness/source_capture/models.py`:
   `SourceCapturePacket`, `SourceCaptureSlice`, `PacketTiming`,
   `PreservedFile`, `ReceiptMetadata`, and the closed posture vocabularies
   (Ob.9 `cutoff_posture`, Ob.10 `archive_history_posture`, Ob.15
   `re_capture_relationship`, AR-04 `hash_basis`).

2. **Obligation contract** —
   `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md`:
   load-bearing for this profile are Ob.1 (commissioning gate), Ob.3
   (capture-event provenance), Ob.4 (capture mode disclosure), Ob.6 (raw
   observable fidelity), Ob.8 (decomposed timing), Ob.9 (cutoff posture), Ob.10
   (archive/history posture), Ob.11 (source visibility), Ob.15 (re-capture
   semantics), and Ob.16 (categorical handoff readiness). The contract's
   discharge vocabulary (`met`, `partial`, `assessed_not_met`, `cannot_assess`,
   `access_failed`, `blocked`, `unavailable_by_source`, `not_applicable`,
   `not_attempted`) is reused as-is; this profile mints no new discharge states.

3. **Lane 1 envelope-delta spec** —
   `docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md`
   (PR #93, `DELTA_SPEC_DRAFT_V0`): this profile CONSUMES Elements 1–5 (pinning
   facts, cold-start marker, series-level recapture-diff, cadence model, and the
   three temporal regimes + cold-start cap doctrine) as published in that delta.
   It does not re-derive, amend, or override any Lane 1 element.

**Conflict rule:** if this profile appears to conflict with `models.py` or the
obligation contract, the envelope of record wins. If it appears to conflict with
the Lane 1 delta spec, the Lane 1 spec wins. Treat this profile as stale and
open the controlling source.

---

## Deconfliction Note — price_payload_extraction.py

`orca-harness/source_capture/price_payload_extraction.py` is a
**Rung-1.5 structured-payload extractor** for a specific vendor class:
JS-hydrated SPA pricing surfaces (specifically the OpenAI / ChatGPT pricing
page). It recovers tier structure + amounts from two embedded structured
payloads (React Router v7 turbo-stream + static JS prices object), joined by
`priceToken`, without a headless browser. It also provides
`extract_announcement_effective_date` for Next.js RSC announcement bodies, and
a `certify_extraction` / `certify_payload` scaffold for internal-consistency
certification of the recovered payload.

**What it already handles:** list-price tier structure and amounts (in minor
units, by currency), effective price token resolution, token-updated-at
timestamps, and certification that the recovered payload is self-consistent and
non-block-shell. This is scoped to SPA sources whose prices live in embedded JS
payloads retrievable via rung-1 HTTP capture without rendering.

**What this profile adds (cite-and-extend, not re-spec):**

- Extends coverage to **rendered-capture sources** where price state is not
  recoverable from static payloads: the majority of beauty DTC and retail
  venues (Shopify storefronts, PDPs, beauty retailer pages) require a browser
  snapshot to see the priced/on-sale state, promo code field, or variant-level
  price. The existing module does not cover these.
- Names **list price, effective/sale price, and promo mechanism as separate
  first-class capture fields** rather than a single amount. `price_payload_extraction.py`
  recovers a `ResolvedTierPrice` with `amount_minor` and `descriptor`, but does
  not distinguish the effective-price mechanism (promo code / GWP / intro offer
  / auto-applied sale) as a separate observable. Conflating them destroys the
  promo-vs-full-price read downstream.
- Names **Keepa/Camel-style retroactive price history** for Amazon-family sources
  as a retroactive-native regime addendum, unavailable for other venues.
- Applies the Lane 1 pinning facts (Element 1: `session_visibility_pin`,
  `locale_pin`, `currency_pin`, `variant_pin`) as first-class per-observation
  capture facts, which the extraction module carries only generically in
  `capture_context`.
- Applies the Lane 1 cold-start marker (Element 2) and series-level
  recapture-diff (Element 3) as series-scoped capture doctrine.

`price_payload_extraction.py` is the correct surface for SPA/JS-payload
recovery; this profile does not replace or weaken it. For SPA sources where
that module applies, its output is the raw observable fidelity source (Ob.6)
that a price time-series capture records.

---

## INV-1 Preservation

This profile is bound by INV-1 (the Demand-Substrate no-scoring invariant, per
`docs/product/product_lead/orca_buyer_proof_packet_v0.md` and
`docs/product/product_lead/orca_demand_read_taxonomy_v0.md`).

Concretely:

- Every field below describes **what is captured** (an observed fact) or
  **how capture should sample / disclose** (doctrine) — never how to weight,
  score, rank, or judge it.
- No formula, threshold, weight, or numeric scoring rule appears.
- The promo-mechanism field records what the source shows; it does not classify
  the promo as material, meaningful, or demand-relevant (Judgment's call).
- The temporal regime and cold-start cap classify *coverage extent*, not *demand
  durability*. "Durable versus hollow" is a downstream Judgment read.
- Costly-behavior semantics (buyer pressure, sellouts, restock, switching) are
  NOT in scope for price capture: price is a supply-side proxy, not a
  costly-behavior signal on its own. INV-1 forbids injecting demand assessment
  into the capture layer.

---

## What Is Captured: Price Time-Series Fields

Price time-series capture records the following as separate, named,
first-class observable facts per observation (per `SourceCaptureSlice`).
Each is carried as a `VisibleFact`, so its status is a `VisibleFactStatus`
(`known` / `unknown_with_reason` / `not_attempted` / `not_applicable`) with a
reason. Where the source does not expose a field, the field's fact status is
`unknown_with_reason` (or `not_applicable`) and the capture **obligation** for
that field is discharged as `unavailable_by_source` — an obligation-discharge
state, not a `VisibleFactStatus`, never written as a fact's status. Silent
omission is not allowed (obligation contract rule, reused).

### Core Price Fields (per observation, per variant/SKU)

**1. List price** (`list_price`)
The source-visible regular/full/undiscounted price for the observed
variant/SKU. Captured as displayed (amount + currency, in source units).
When no list price is shown separately (e.g. always-sale display), record the
field's status as `unknown_with_reason` (the source does not expose it) and
discharge its capture obligation as `unavailable_by_source` — never as a fact
status. Do not compute or impute.

**2. Effective / sale price** (`effective_price`)
The price a buyer would actually pay at capture time — the active/settled
price after any auto-applied discount, sale, or promo visible on the page.
When identical to list price (no active discount), record the same value and
note "no active discount observed." When the effective price cannot be
determined (e.g. requires checkout to reveal), record `cannot_assess` with
reason.

**3. Promo mechanism** (`promo_mechanism`)
The source-visible mechanism producing any gap between list price and
effective price. This field is the load-bearing reason for capturing list and
effective price separately: the mechanism type determines what the price
difference means analytically. Capture the mechanism as observed; do not
classify its marketing intent or demand significance.

Mechanism vocabulary (source-visible categories — record as observed, not
forced into these labels when the source uses different language):

- `promo_code` — a code must be entered at checkout; capture the code
  (or its existence if not shown) as the raw observable.
- `gwp` (Gift With Purchase) — a gift/bonus item accompanies the purchase
  at or above a threshold; capture the threshold and gift description.
- `intro_offer` — a first-purchase, first-subscription, or
  trial-period price; capture the stated eligibility and duration.
- `auto_applied_sale` — a sale or markdown applied without a code; capture
  the sale label and end date if shown.
- `bundle_discount` — price reduction contingent on purchasing multiple
  items or a kit; capture the bundle structure.
- `subscription_price` — a lower price for subscribe-and-save or
  membership; capture the subscription tier.
- `none_observed` — list price = effective price; no promo mechanism
  visible at capture time.
- `unavailable_by_source` — a promo is inferred or partially visible but
  the mechanism cannot be determined from the observable.

When multiple mechanisms coexist, capture each separately. When the source
shows a promo that changes during the observation window (e.g. sale ends
before recapture), the per-observation record reflects what was visible at
that observation's `capture_time`; the change is recorded in the
series-level recapture-diff (Lane 1 Element 3).

### Rendered Capture Requirement

For the majority of beauty DTC and retail price surfaces, price state is not
recoverable from static HTML or embedded JS payloads without rendering. A
rendered capture (browser snapshot or equivalent) is the required capture
mode for these sources, so that the displayed price, sale badge, promo field,
and variant-level state are preserved as seen. Capture mode is disclosed per
Ob.4 (`capture_mode`); a rendered capture uses `CaptureModeCategory.MULTIMODAL`
or `AUTOMATED_EXTRACTION` as appropriate, with mode changes visible per Ob.5.

**Exception — SPA JS-payload sources.** For sources where
`orca-harness/source_capture/price_payload_extraction.py` applies (SPA pricing
surfaces with recoverable embedded payloads, currently the OpenAI/ChatGPT
venue), the existing extraction output is the fidelity source; the rendering
requirement does not apply. The capture mode is `STRUCTURED_ACCESS` or
`AGENT_ASSISTED` as appropriate.

### Pinning Facts (per observation — consumed from Lane 1 Element 1)

The following four pinning facts are consumed as defined in Lane 1
(`capture_envelope_durability_delta_spec_v0.md`, Element 1). They are
reproduced here as the application of that element to price time-series:

- **`session_visibility_pin`** — the visibility/auth condition under which
  the price surface was observed (e.g. logged-out/anonymous, account-created,
  entitled/subscribed). Price may differ by login state; logged-out is the
  forward primary unless the Decision Frame specifies otherwise.
- **`locale_pin`** — the locale/region/language context the surface rendered
  in (e.g. `en-US`, `en-GB`). Locale changes which prices and promotions are
  shown.
- **`currency_pin`** — the currency in which prices were displayed. Required
  whenever the source exposes multi-currency or the locale implies a
  non-default currency.
- **`variant_pin`** — the specific product/SKU/size/edition observed. Price
  series must hold one variant fixed; a variant swap makes two observations
  non-comparable.

When a pin is unknown or the source does not expose it, the capture records the
pin's fact status as a valid `VisibleFactStatus` (`unknown_with_reason` or
`not_applicable`) with a reason, and discharges the pin's capture obligation as
`unavailable_by_source` — never recording `unavailable_by_source` as a fact
status — rather than guessing. Silent omission is not allowed.

### Retroactive-Native Addendum — Amazon-family sources (Keepa / Camel)

For Amazon-family sources (amazon.com and its locale variants), third-party
price-history services (Keepa, CamelCamelCamel) natively expose historical
price data — list price and effective price back-runs — that a single capture
can recover. This is a **retroactive-native regime** (Lane 1 Element 5,
Regime 1) and is the sole venue class where the pre-cold-start price window
can be (partly) recovered.

Capture obligation for retroactive-native addendum:
- Record the source and depth of the historical price data (how far back the
  native/archive history reaches, its fidelity, and any gaps).
- The cold-start marker (Element 2) still applies to Orca's own coverage;
  `pre_coverage_history_posture` may be partly satisfied by retroactive-native
  history (recorded with the third-party source as the basis, not asserted).
- Whether the retroactive data is admissible for the Decision Frame's cutoff
  window is a downstream Judgment call.

For all non-Amazon venues, retroactive price history is not available; the
forward-only regime applies.

---

## Temporal Regime: Forward-Only (Consumed from Lane 1 Element 5)

The price time-series proxy is **forward-only** for all non-Amazon venues.

**What this means, consumed directly from Lane 1 Element 5:**

> "The source exposes only its current state; history exists only as the series
> Orca itself accumulates from cold start forward. There is no way to recover
> pre-cold-start states later — they were never recorded and the source does not
> retain them."

For most beauty DTC, retail, and marketplace price surfaces, the source shows
only the current price. Once a capture is not taken, that price observation is
permanently lost. No archive, re-scrape, or tooling can recover it.

**Cold-start cap (inherent-limit, not a clearable risk):**

The pre-cold-start window is **uncovered by construction**. Lane 1 Element 5
states this is an **inherent-limit cap** — a permanent ceiling on what the
series can claim about the pre-coverage window, not a clearable risk that
better tooling or more captures will close.

The cap is permanent because the source never retained the prior state.
Capture's job is to make the cap visible and correctly classified. Whether
the cap is acceptable for the Decision Frame's question is Judgment's call.

**Cold-start marker (consumed from Lane 1 Element 2):**

A price time-series must carry a per-series cold-start marker on its first
observation, recording `series_id`, `cold_start_at`, and
`pre_coverage_history_posture` (marked as "uncovered by construction" with the
reason that the series began at the first commissioned capture and the source
does not retain prior price states). See Lane 1 Element 2 for the full
marker spec; it is consumed here, not re-derived.

**Cadence model (consumed from Lane 1 Element 4):**

A price time-series should declare its intended cadence using the existing
`CadencePlan` vocabulary (`orca-harness/source_capture/cadence.py`), record
the realized cadence, and record deviations and gaps as visible limitations.
An undisclosed gap masquerades as "no price change" — gap disclosure is
required for the series to be honest.

---

## Limitations and Non-Claims

- This profile does not capture private or account-specific pricing (loyalty
  prices, negotiated rates, employee discounts) unless the Decision Frame
  explicitly authorizes entitled access and the obligation contract's boundary
  compliance (Ob.2) is met.
- Currency conversion, normalization, and cross-locale price equivalence are
  Cleaning's job; capture records what the source shows.
- Whether a price change signals promotional pressure, margin compression,
  demand softness, or competitive response is Judgment's read.
- Whether the captured promo mechanism is material, temporary, or structurally
  load-bearing for a demand read is Judgment's call.
- Capture does not decide admissibility for any backtest or cutoff window.
- Price capture is one proxy; it is not a standalone costly-behavior signal
  (buyer pull, sellout, restock pressure) and must not be used as such.

---

## Lifecycle Verification Fields

```yaml
lifecycle:
  status: CAPTURE_PROFILE_DRAFT_V0
  authored_at: "2026-06-14"
  authored_by: "Claude Sonnet 4.6 (claude-sonnet-4-6)"
  lane_branch: capture-proxy-price-availability
  worktree: .claude/worktrees/capture-proxy-price-availability
  pr_base: main
  lane_1_consumed:
    spec: docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md
    pr: "#93"
    elements_consumed: [1, 2, 3, 4, 5]
    temporal_regime: forward-only (non-Amazon venues); retroactive-native (Amazon-family addendum)
    cold_start_cap: inherent-limit, not clearable (Lane 1 Element 5 consumed verbatim)
  deconfliction_status: cite-and-extend (price_payload_extraction.py is SPA/JS-payload-only; this profile extends to rendered sources and separate promo-mechanism field)
  inv1_status: preserved (no scoring, no weighting, no demand assessment in capture layer)
  contract_hardening: blocked (owner-gated, out of scope)
  implementation_authorized: no
  validation_status: not_proven (design+spec only; no pressure test run)
```

---

## Non-Claims

This profile is not validation, readiness, acceptance, pressure-test discharge,
Data Capture Spine acceptance, contract hardening, source-of-truth promotion,
buyer proof, judgment-quality evidence, implementation authorization, runtime
authorization, schema change, ECR design, Cleaning implementation, Judgment
design, or commercial-readiness evidence.

It is a design+spec profile that cites the existing Capture Envelope of record
and the Lane 1 envelope-delta, and specifies the capture facts and doctrine
for price time-series demand-durability proxy capture.
