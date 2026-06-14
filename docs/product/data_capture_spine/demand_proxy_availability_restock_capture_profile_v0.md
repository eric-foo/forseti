# Demand Proxy — Availability / Restock Capture Profile v0

```yaml
retrieval_header_version: 1
artifact_role: Product-method spec (demand proxy capture profile — availability/restock)
scope: >
  Capture profile for the availability/restock demand-durability proxy. Specifies
  WHAT is captured (in-stock / out-of-stock / waitlist state at variant granularity,
  and restock/backorder signals), the flag-don't-conclude discipline, temporal
  regime, cold-start doctrine, and deconfliction note against existing capture
  surfaces. Design + spec only; no contract hardening, no implementation.
use_when:
  - Specifying or reviewing commissioned availability/restock captures for
    demand-durability proxy purposes.
  - Checking how availability-proxy capture facts sit on top of the existing
    Capture Envelope (models.py + obligation contract).
  - Consuming the forward-only regime or cold-start inherent-limit cap for
    availability/restock.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md   # Lane 1 envelope-delta (Element 1–5 consumed here)
  - orca-harness/source_capture/models.py                                            # Capture Envelope of record (schema)
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/product/data_capture_spine/demand_proxy_price_timeseries_capture_profile_v0.md  # Sibling proxy profile (pinning + cold-start shared doctrine)
stale_if:
  - The Lane 1 envelope-delta spec is superseded by an owner decision that amends
    Element 1 (pinning), Element 2 (cold-start marker), Element 4 (cadence), or
    Element 5 (temporal regimes / cold-start cap) in a way that conflicts with
    this profile.
  - The obligation contract is amended in a way that already names availability /
    restock / variant-level stock state as first-class obligations.
  - An owner decision redefines the flag-don't-conclude rule for availability
    capture or classifies deliberate scarcity-theater separately at capture time.
downstream_consumers:
  - Future commissioned availability/restock capture sessions operating under this profile.
  - demand_proxy_price_timeseries_capture_profile_v0.md (sibling proxy profile).
```

- Status: `CAPTURE_PROFILE_DRAFT_V0`
- Artifact type: Product-method spec (demand proxy capture profile), not an
  envelope authority, contract amendment, or implementation authorization
- Implementation authorized: no
- Contract hardening authorized: no (owner-gated, out of scope)
- Source basis: `capture_envelope_durability_delta_spec_v0.md` (Lane 1, PR #93),
  `orca-harness/source_capture/models.py`,
  `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md`,
  `docs/product/product_lead/orca_buyer_proof_packet_v0.md` (INV-1, costly-behavior,
  Demand-Substrate Hard Gate),
  `docs/product/product_lead/orca_demand_read_taxonomy_v0.md`

---

## Orca Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: S3 (target deepening — Lane 1 delta spec + models.py + obligation contract + sibling price profile)
  edit_permission: docs-write
  target_scope: new product-method spec for availability/restock demand proxy capture
  dirty_state_checked: yes (fresh worktree off origin/main; HEAD 8e54aad)
  blocked_if_missing: Lane 1 envelope-delta spec readable at worktree path (confirmed)
```

---

## What This Is (And Is Not)

This is a **capture profile** for the availability/restock demand-durability
proxy. It specifies what must be captured (in-stock / out-of-stock / waitlist
state at variant granularity), the flag-don't-conclude discipline, the
temporal regime, and how the cold-start gap is treated — all as observed
facts and capture doctrine, never as weights, scores, or judgments.

It is **design + spec only**. It builds nothing, runs nothing, deploys nothing,
hardens no contract, and does not edit `models.py` or the obligation contract.
It **cites** them.

It does not define ECR fields, Cleaning transformations, or Judgment rules. It
does not assess whether a stock-out pattern signals durable demand, deliberate
scarcity theater, or supply-chain failure — that is downstream Judgment's call.

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
   observable fidelity), Ob.8 (decomposed timing), Ob.9 (cutoff posture),
   Ob.10 (archive/history posture), Ob.11 (source visibility), Ob.15
   (re-capture semantics), and Ob.16 (categorical handoff readiness). The
   contract's discharge vocabulary is reused as-is; this profile mints no
   new discharge states.

3. **Lane 1 envelope-delta spec** —
   `docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md`
   (PR #93, `DELTA_SPEC_DRAFT_V0`): this profile CONSUMES Elements 1–5 as
   published in that delta. It does not re-derive, amend, or override any
   Lane 1 element.

**Conflict rule:** if this profile appears to conflict with `models.py` or the
obligation contract, the envelope of record wins. If it appears to conflict
with the Lane 1 delta spec, the Lane 1 spec wins. Treat this profile as stale
and open the controlling source.

---

## Deconfliction Note — Existing Capture Surfaces

**Overlap with existing capture surfaces:** low. The Data Capture Spine
obligation contract's core obligations (Ob.6 raw observable fidelity, Ob.12
related context preservation) already require capturing what the source shows.
For any commissioned capture of a product page, the existing fidelity
obligations would incidentally preserve visible stock indicators if the
operator captures them. However, the obligation contract does not name
availability state, variant-level stock status, waitlist signals, or restock
notices as first-class proxy capture facts. It does not require variant-level
granularity, a flag-don't-conclude discipline, or series-level coverage of
stock state changes.

**What is genuinely new:**

- **Variant-level granularity as a first-class requirement.** Stock state
  varies by size, shade, SKU, and edition; a product-level "in stock" reading
  collapses information that matters for demand reads (a hero SKU selling out
  while backup SKUs remain available is a different signal from uniform
  availability). This profile names variant-level capture as the required
  granularity.
- **Flag-don't-conclude discipline.** Deliberate scarcity-theater (a brand
  artificially constraining stock to signal exclusivity or drive urgency) is
  indistinguishable from genuine sellout at capture time. Capture records
  observed state and visible signals; it does not classify the cause. This
  discipline is not in the obligation contract's general fidelity obligations.
- **Series-level restock/backorder signal capture.** The stock state at one
  observation is less meaningful than the trajectory (went OOS, when, what
  restock signal appeared, when restocked, whether waitlist was opened and
  closed). This profile names restock notices, backorder framing, and
  waitlist open/close events as capture facts across observations.
- **Forward-only regime with no retroactive source.** Unlike price
  time-series (where Amazon/Keepa provides a partial retroactive-native
  addendum), no retroactive source for availability state exists for any
  venue class in scope. The cold-start cap is absolute.

`price_payload_extraction.py` does not overlap with availability capture;
it is a price-amount extractor for JS-hydrated SPA pricing pages and has no
stock-state surface.

---

## INV-1 Preservation

This profile is bound by INV-1 (the Demand-Substrate no-scoring invariant, per
`docs/product/product_lead/orca_buyer_proof_packet_v0.md` and
`docs/product/product_lead/orca_demand_read_taxonomy_v0.md`).

Concretely:

- Every field below describes **what is captured** (an observed fact) — never
  how to weight, score, rank, or interpret it.
- No formula, threshold, or scoring rule appears.
- The flag-don't-conclude discipline is INV-1 in action at the capture layer:
  capture records what is visible; Judgment interprets it.
- Availability state, restock frequency, and waitlist existence are observed
  facts; whether they indicate durable demand, scarcity theater, or supply
  constraints is a downstream Judgment call.
- The buy-side costly-behavior signals (sellouts, restock pressure, waitlists
  resolving) named in the Demand-Substrate Hard Gate are signals Judgment reads
  from captured facts; capture's job is to preserve the facts, not to
  pre-classify them as costly behavior.

---

## What Is Captured: Availability / Restock Fields

Availability/restock capture records the following as separate, named,
first-class observable facts per observation (per `SourceCaptureSlice`) at
**variant granularity**. Each is carried as a `VisibleFact`, so its status is a
`VisibleFactStatus` (`known` / `unknown_with_reason` / `not_attempted` /
`not_applicable`) with a reason. Where the source does not expose a field, the
field's fact status is `unknown_with_reason` (or `not_applicable`) and the
capture **obligation** for that field is discharged as `unavailable_by_source` —
an obligation-discharge state, not a `VisibleFactStatus`, never written as a
fact's status. Silent omission is not allowed.

### Core Stock State Fields (per variant, per observation)

**1. Stock status** (`stock_status`)
The source-visible availability state of the observed variant at capture time.

Vocabulary (source-visible categories — record as observed):

- `in_stock` — the variant is shown as available for purchase with no
  stock-shortage signal visible.
- `out_of_stock` — the variant is shown as unavailable, sold out, or
  no-longer-orderable. Capture the source-visible label verbatim.
- `low_stock` — the source shows an explicit low-stock or "only N left"
  indicator. Capture the numeric quantity if shown; otherwise record the
  label.
- `waitlist_open` — the source offers a waitlist, restock notification
  signup, or "notify me" mechanism without allowing direct purchase.
  Capture the waitlist mechanism (email signup, form, app notification).
- `waitlist_closed` — a previously open waitlist is shown as closed or
  at capacity.
- `backorder` — the variant is purchasable but with a stated or implicit
  delay; may include a ship-date or "pre-order" label. Capture the stated
  lead time if shown.
- `discontinued` — the source shows the variant as no longer produced,
  retired, or permanently unavailable (distinct from a temporary OOS).
  Capture the source-visible label.
When stock state cannot be determined from the observable (e.g. a variant
selector is present but the state is not shown, or the variant does not appear
on this page), `stock_status` takes **no value from the vocabulary above**: its
`VisibleFact` status is `unknown_with_reason` (with the reason) and the field's
capture obligation is discharged `unavailable_by_source`. The list above is the
set of source-visible *known* values only.

When the source aggregates multiple variants onto one page, capture state
per variant; do not roll up to a product-level average or composite status.

**2. Restock / backorder notice** (`restock_notice`)
Any source-visible text, label, or UI element indicating a restock date,
expected availability, backorder fulfillment window, or supply constraint
note. Captured verbatim as shown. When no restock notice is visible,
record `not_observed` as the value with status `known`.

**3. Waitlist signal** (`waitlist_signal`)
Whether a waitlist, notify-me, or pre-order mechanism is active at capture
time. Distinct from `stock_status`: a `waitlist_open` status says the
mechanism exists; this field captures the source-visible details (trigger
text, form endpoint if observable, estimated date if shown). When no
waitlist mechanism is visible, record `not_present` with status `known`.

### The Flag-Don't-Conclude Discipline

**Deliberate scarcity-theater is indistinguishable from genuine sellout at
capture time.**

A brand may intentionally constrain visible inventory (artificial low-stock
warnings, manufactured OOS states, waitlist theater with same-day restock) to
signal exclusivity, drive urgency, or manipulate perceived demand. A supply
constraint, logistics failure, or genuine high-demand sellout produces the
same observable. Capture cannot distinguish these cases; only Judgment — reading
the trajectory, cross-venue signals, org-motion corroboration, and integrity
layer — can.

Therefore:

- Capture RECORDS the source-visible state and signals as observed facts.
- Capture does NOT classify the observed OOS/waitlist/low-stock as
  genuine demand, manufactured scarcity, supply failure, or distortion.
- The `stock_status` and `restock_notice` fields are observations, not
  verdicts.
- No `scarcity_signal_type` or `manufacturing_probability` field appears
  in this profile; such a field would violate INV-1 and the
  flag-don't-conclude discipline.

This discipline is the capture-layer application of the Demand-Substrate
Hard Gate's integrity-label requirement: every venue's evidence carries
integrity labels before it may enter the fused read. The integrity label is
Judgment's output; capture provides the raw input.

### Rendered Capture Requirement

Availability state for beauty DTC, specialty retail, and marketplace venue
classes is not reliably recoverable from static HTML alone. Variant-level
stock state often depends on client-side hydration, variant-selector
interaction, or dynamic page rendering. A rendered capture (browser snapshot
or equivalent) is the required capture mode for these sources.

Capture mode is disclosed per Ob.4; a rendered capture uses
`CaptureModeCategory.MULTIMODAL` or `AUTOMATED_EXTRACTION` as appropriate,
with mode changes visible per Ob.5.

When static HTML contains sufficient stock-state signals (e.g. a structured
data block, an accessibility attribute, or a server-rendered OOS badge), that
source-visible signal is a valid fidelity basis, and the capture mode can be
`STRUCTURED_ACCESS` or `AGENT_ASSISTED`. The operator must disclose what was
captured and how.

### Pinning Facts (per observation — consumed from Lane 1 Element 1)

The following four pinning facts are consumed as defined in Lane 1
(`capture_envelope_durability_delta_spec_v0.md`, Element 1). They are
reproduced here as the application of that element to availability capture:

- **`session_visibility_pin`** — the visibility/auth condition (logged-out /
  anonymous, account-created, entitled). Stock state may vary by login
  state (e.g. member-exclusive restock access). Logged-out is the forward
  primary unless the Decision Frame specifies otherwise.
- **`locale_pin`** — the locale/region context. Stock availability is
  often locale-specific (regional distribution, geo-restricted launches,
  different retailer assortments by market).
- **`currency_pin`** — not directly relevant to stock state, but required
  when backorder or waitlist notices include pricing. Record as
  `not_applicable` with reason when no monetary value appears in the
  availability observable.
- **`variant_pin`** — the specific product/SKU/size/shade/edition observed.
  This is load-bearing for availability capture: the series must hold one
  variant fixed; a variant swap makes two stock-state observations
  non-comparable.

---

## Temporal Regime: Forward-Only (Consumed from Lane 1 Element 5)

The availability/restock proxy is **forward-only** for all venue classes
in scope. There is no retroactive source for any venue.

**What this means, consumed directly from Lane 1 Element 5:**

> "The source exposes only its current state; history exists only as the series
> Orca itself accumulates from cold start forward. There is no way to recover
> pre-cold-start states later — they were never recorded and the source does not
> retain them."

No third-party price-history equivalent exists for availability state. No
archive service, Wayback Machine snapshot, or structured-data history endpoint
reliably preserves variant-level stock status at the observation frequency
needed for a durability series. Unlike price, where Amazon/Keepa provides
retroactive-native data for one venue class, availability is forward-only for
every venue class in scope.

**Cold-start cap (inherent-limit, not a clearable risk):**

The pre-cold-start window is **uncovered by construction**. Lane 1 Element 5
states this is an **inherent-limit cap** — a permanent ceiling on what the
series can claim about the pre-coverage window, not a clearable risk.

The cap is **absolute and unconditional** for availability/restock: unlike
price time-series, there is no retroactive-native addendum for any venue.
Whatever the stock trajectory was before the first commissioned observation,
it is permanently unrecoverable. Capture makes the cap visible; Judgment
determines whether the coverage window is sufficient for the Decision Frame.

**Cold-start marker (consumed from Lane 1 Element 2):**

An availability series must carry a per-series cold-start marker on its
first observation, recording `series_id`, `cold_start_at`, and
`pre_coverage_history_posture` (marked as "uncovered by construction, no
retroactive source available for any venue class" with the reason that the
series began at the first commissioned capture and no source retains prior
availability states). See Lane 1 Element 2 for the full marker spec; it is
consumed here, not re-derived.

**Cadence model (consumed from Lane 1 Element 4):**

An availability series should declare its intended cadence using the existing
`CadencePlan` vocabulary (`orca-harness/source_capture/cadence.py`), record
the realized cadence, and record deviations and gaps as visible limitations.
A gap in the series means the stock state during that gap is unknown — it
could be OOS, restocked, or unchanged. Gap disclosure is required for the
series to be honest; an undisclosed gap masquerades as "no stock change."

---

## Limitations and Non-Claims

- This profile does not capture private inventory data, wholesale allocation,
  or warehouse-level stock levels — only what the source-visible surface shows
  to a public or account-holding observer within Ob.2 boundary compliance.
- Variant-level granularity is required but may not always be achievable
  (some sources aggregate or obscure variant states). When granularity cannot
  be achieved, record the affected variant's status as `unknown_with_reason`
  (with reason) and discharge its capture obligation as `unavailable_by_source`;
  do not aggregate silently.
- Whether an OOS event is meaningful (duration, breadth, restock lag,
  cross-venue corroboration) is Judgment's read; capture records the event
  and its visible signals.
- Whether an observed waitlist / notify-me mechanism represents genuine
  constrained supply or marketing theater cannot be determined at capture
  time; the flag-don't-conclude discipline applies.
- Capture does not decide admissibility for any backtest or cutoff window.
- Availability capture is one proxy: on its own it cannot support a material
  demand commitment. Per the commitment-tiered Demand-Substrate Hard Gate, a
  single origin authorizes only low-commitment, reversible responses; any
  material or irreversible commitment requires ≥2 independent origins that
  converge (a second family is not required at the floor but raises the
  ceiling). See `orca_buyer_proof_packet_v0.md` (AR-02, AR-06).

---

## Series-Diff Application (Lane 1 Element 3)

Stock-state changes across the ordered availability series are recorded using
**Lane 1 Element 3 (series-level recapture-diff)** — consumed, not re-derived
(see `capture_envelope_durability_delta_spec_v0.md` §Element 3). For one
`series_id`, the series-diff records the observed stock-state change events —
`in_stock` ↔ `out_of_stock`, `low_stock` onset, `waitlist_open` /
`waitlist_closed`, `backorder`, `discontinued`, and restock — with the existing
evidence anchors (`PreservedFile.sha256` divergence and/or the source-visible
label change), and `tamper_deletion_visibility` recording whether a delisting /
relisting / back-dated change was source-visibly marked, inferred from hash/value
divergence only, or `cannot_assess`. This is what prevents an **un-sampled gap**
from being read as "stock did not change": absence of an observed change event
within a cadence gap is recorded as un-observed, never as no-change. The
series-diff records observed differences only; whether a change is genuine
scarcity, restock strategy, or manipulation is a downstream Judgment call
(INV-1).

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
    temporal_regime: forward-only (all venue classes; NO retroactive-native addendum)
    cold_start_cap: inherent-limit, absolute and unconditional (Lane 1 Element 5 consumed verbatim)
  deconfliction_status: low overlap with existing surfaces (generic fidelity/recapture only); variant-granularity, flag-don't-conclude, and restock-signal capture are genuinely new
  inv1_status: preserved (flag-don't-conclude is INV-1 applied at capture layer; no scoring, classification, or demand assessment)
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
for availability/restock demand-durability proxy capture.
