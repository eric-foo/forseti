# Demand-Durability Indicator Capture Profile — Availability / Restock v0

```yaml
retrieval_header_version: 1
artifact_role: Product-method spec (per-indicator capture profile; consumes the Capture Envelope durability delta)
scope: >
  Thin capture profile for the AVAILABILITY / RESTOCK time-series demand-durability
  indicator. Names the variant-granular stock-state facts, the forward-only temporal
  regime, pinning, series-integrity, and the scarcity-theater manipulability posture
  (flag, do not conclude) that drop onto the Capture Envelope of record + durability
  delta. Design + spec only.
  TERMINOLOGY: "indicator" is the demand-side observable; "proxy" is reserved for the
  NETWORK sense (ProxyProfile). The keystone delta / taxonomy still say "proxy" for
  this concept — reconciliation pending (see deconfliction note).
use_when:
  - Specifying or reviewing capture of in-stock / out-of-stock / waitlist state over time.
  - Checking how availability observations sit on the Source Capture packet + durability delta.
  - Deconflicting an availability-capture proposal against existing capture lanes.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/product/data_capture_spine/data_capture_source_access_method_plan_v0.md
  - docs/product/product_lead/orca_demand_read_taxonomy_v0.md
  - docs/product/product_lead/orca_buyer_proof_packet_v0.md                            # Demand-Substrate Hard Gate (costly-behavior floor)
stale_if:
  - The keystone durability delta changes the five elements.
  - The Source Capture packet schema changes PacketTiming or posture vocabularies.
  - The demand-read taxonomy or Demand-Substrate Hard Gate changes the sellout/restock costly-behavior role.
  - An owner decision adopts, narrows, or rejects any availability capture fact below.
```

- Status: `PROFILE_DRAFT_V0`
- Artifact type: Per-indicator capture profile (subordinate to the durability delta; not a new envelope)
- Implementation authorized: no · Feature planning authorized: no · Runtime/source-system design authorized: no · Contract hardening authorized: no (owner-gated, out of scope)

## What This Is (And Consumes)

A thin per-indicator profile on the **Capture Envelope of record** (`models.py` +
obligation contract) and the **durability delta**
(`capture_envelope_durability_delta_spec_v0.md`; it calls these observables "proxies" —
same concept, renamed "indicator" here). It adds no provenance field and re-specs no
durability element; it supplies only the availability-specific bindings. On any
conflict, the schema / obligation contract / delta win.

Scope note (owner, 2026-06-15): demand-durability reading is **one decision Orca can
help with**, not Orca's whole job.

## The Demand Read This Indicator Serves (read-trace)

Availability/restock is among the **strongest costly-behavior signals** in the
demand-read taxonomy (Layer 3 buy-side corroboration: "sellouts, waitlists, restock
pressure"). Unlike search interest, it can **clear the Demand-Substrate Hard Gate
costly-behavior floor (G2)** — a genuine sellout/waitlist is identifiable buyer action,
directional, and checkable. But it is **manipulable** (deliberate scarcity theater), so
it is floor-eligible **only** when the integrity posture below is honored, and
divergence can defeat the floor (buyer-proof packet defeater rule).

| Captured availability fact | Serves which read | Floor/ceiling role |
| --- | --- | --- |
| Out-of-stock / sellout (per variant, over time) | Buy-side costly-behavior read; restock pressure | **Floor-eligible** (gradeable costly behavior) — subject to scarcity-theater integrity check |
| Waitlist / back-in-stock signup exposed | Costly behavior (effortful demand expression) | Floor-eligible |
| Restock cadence / re-sellout pattern | Durable-vs-transient classification (repeated fast sellouts → durable; one-off → transient) | Feeds the persistence read; never decided at capture |

## Temporal Regime — per durability delta Element 5

Availability is **forward-only**. The source exposes only its *current* stock state;
**no retroactive source exists** (you cannot recover what was in/out of stock last
month — neither the source nor archives reliably retain transient stock state).
Therefore:

- **Cold-start (delta Element 2) is a hard inherent-limit cap here** — the strongest
  case among the four indicators. The series can speak **only** to the window from
  `cold_start_at` forward; the pre-coverage window is **permanently unrecoverable** (no
  archive/aggregator/tooling closes it, because the state was never retained).
- Restock/sellout are **events** observed *within* the forward series; an un-observed
  interval is "no observed event," never "no change" (cadence governs how confidently
  absence-of-restock can be stated).

This makes a **tracking window mandatory before any durability read** — capture cannot
manufacture availability history. State this cap honestly; do not let "the series starts
here" imply pre-window demand was low.

## Availability-Specific Capture Facts

Each an observed `VisibleFact`; none a score or judgment.

- **`stock_state`** — source-visible state **at variant granularity**: in-stock,
  out-of-stock, low-stock/limited, waitlist/back-in-stock-signup, pre-order,
  discontinued, not-listed. Captured per variant, never rolled up to a brand- or
  product-level "available" that hides a sold-out hero SKU.
- **`stock_state_qualifier`** — any source-visible quantity/urgency cue ("only 3 left",
  "ships in 4 weeks", countdown), recorded verbatim as shown (Ob.6), not interpreted.
- **`restock_event` / `sellout_event`** — a transition observed between consecutive
  observations of the same variant (in→out = sellout; out→in = restock), anchored on
  the series-diff (delta Element 3), with the observation references it spans.
- **`waitlist_exposed`** — whether a waitlist/notify-me is offered (an effortful-demand
  affordance), distinct from `stock_state`.

These are source-visible states (Ob.6 raw observable). They are **not** inventory counts
(Orca does not have the brand's inventory), **not** ECR fields, and **not** a demand
magnitude.

## Pinning (delta Element 1)

- **`variant_pin`** — the controlling pin here; stock is **per variant** and a series
  must hold the variant fixed.
- **`locale_pin`** — locale/region flips a variant in or out of stock (regional
  fulfilment); record the *effective* rendered locale and hold network exit-geo
  (`ProxyProfile`) constant or record its change as a comparability break.
- **`session_visibility_pin`** — logged-out vs entitled; some stores gate availability
  or early access behind login/membership.
- `currency_pin` — `not_applicable` unless the surface co-presents price (then defer to
  the price profile's currency_pin), recorded with reason.

Unknown/unexposed pins → `unknown_with_reason` / `unavailable_by_source`, never guessed.

## Capture Method & Boundary

Per the method plan (discoverable-or-entitled + disclosable; measured-ToS accepted;
industrial scraping rejected). Stock state is usually in the rendered DOM or an embedded
availability payload:

1. **Rendered/headless browser** — when stock state is render-time only (method-plan
   Methods 2/3/10); the likely default route.
2. **Embedded-payload / structured access** — where the page exposes stock state in a
   parseable embedded payload (the source-agnostic `extract_object_at_anchor` brace-
   matcher in `price_payload_extraction.py` is a reusable utility for this); use only
   where a source is *shown* to expose such a payload.
3. **Manual human-browser capture** — for high-value/infrequent checks (Method 8).

Archive is **not** a useful route here (forward-only regime — archives do not retain
transient stock state reliably). Capture mode disclosed (Ob.4); mode changes visible
(Ob.5).

## Series Integrity (delta Element 3) — the scarcity-theater problem

The series-diff records observed stock-state transitions across the series. **The
load-bearing constraint for this indicator: flag, do not conclude.** A deliberate
scarcity-theater pattern (artificial "sold out" to manufacture urgency; drop-model
limited releases; perpetual "only N left") is **indistinguishable from a genuine
sellout at capture time.** Capture therefore:

- **records** the observed transitions, the qualifier cues, and the restock cadence as
  facts (e.g. "out-of-stock at obs 4–7, restocked obs 8, re-sold-out obs 9");
- **does not** label the pattern as genuine demand vs. manufactured scarcity — that
  integrity classification is Judgment Spine's Signal Integrity (obligation contract
  forbidden output: "integrity classifications"). The read interprets; the capture
  records.

A `tamper_deletion_visibility`-style note states what the series can and cannot show
(e.g. "fast repeated sellouts observed; cannot distinguish genuine demand from
drop-model scarcity from this surface alone").

## Cadence (delta Element 4) — especially load-bearing here

Cadence is the measurement-resolution + honesty knob, and it decides four things —
never the demand verdict: (1) the finest stock change observable between samples; (2)
whether "stayed in stock" is real or an unobserved gap hid a sellout-and-restock; (3)
how confidently repeated sellouts can be called durable vs. a one-off; (4) whether a
drop-model scarcity rhythm is detectable. Because availability is forward-only and
event-based within the window, a sparse/gappy cadence **cannot** distinguish "stayed in
stock" from "sold out and restocked inside an unobserved gap." **It must be expressed on
the indicator's sampling rhythm — hourly to daily (owner, 2026-06-15)**, not the seconds-scale `CadencePlan` was built
for; `CadencePlan` lends vocabulary only, and a real time-scale series cadence is a
confirmed need whose primitive is a build/hardening step (out of scope). Declare
intended cadence, record realized timings + gaps as visible limitations, and never read
an unobserved interval as "no change."

## Manipulability & Integrity Posture

Floor-eligible costly behavior, but **manipulation-suspect by construction.** Under the
manipulable-input rule: a sellout/waitlist clears the floor **only** as one fused signal
with its scarcity-theater limitation visible; **divergence defeats the floor** when the
divergence pattern indicates the sellout is itself likely manufactured (e.g. a drop-model
brand whose "sellouts" are a marketing cadence). Capture surfaces the pattern and the
limitation; the floor/defeater decision is the gate's, downstream.

## Deconfliction (per-indicator)

- **Already covered — do NOT re-spec:** envelope/provenance (schema + obligation
  contract); durability elements (delta); the source-agnostic embedded-payload
  brace-matcher (`extract_object_at_anchor`) is a reusable utility for availability
  payloads — cite, do not re-spec.
- **Genuinely new here:** the **variant-granular `stock_state` vocabulary**, the
  restock/sellout event binding to the series-diff, the **forward-only hard cold-start
  cap** framing, and the **scarcity-theater flag-don't-conclude** integrity posture.
  **No existing capture lane covers availability/restock** as a dedicated indicator
  (confirmed by source sweep).
- **Not this profile:** org-motion / distribution availability (retail placement) is the
  EDGAR/company-aggregate + retail-presence G4 lane (deferred); price co-presented on the
  same surface defers to the price profile.

## INV-1 Preservation

Every element is a captured fact or a capture method/pin/regime — never a weight, score,
threshold, ranking, or durability verdict. Genuine-vs-manufactured-scarcity and
durable-vs-transient are downstream reads, consumed from the taxonomy/gate, never decided
here.

## Boundaries, Non-Goals, Non-Claims

- No build/scrape/run/deploy; no scheduler/monitor; primitives referenced only.
- No edits to `models.py` or the obligation contract; field promotion is contract
  hardening (owner-gated, out of scope).
- No ECR/Cleaning/Judgment design; no inventory inference; no demand magnitude.
- **Commissioned capture only (Ob.1) today.** Continuous monitoring of this indicator is
  owner-confirmed as wanted (2026-06-15) but is gated on a standing-capture obligation
  home that does not yet exist (see deconfliction note); this profile does not authorize
  standing collection.
- Not validation, readiness, acceptance, source-of-truth promotion, buyer proof,
  implementation/runtime/tooling authorization, source-access boundary amendment, or
  commercial-readiness evidence.
```
