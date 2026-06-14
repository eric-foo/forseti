# Demand-Durability Indicator Capture Profile — Search Interest v0

```yaml
retrieval_header_version: 1
artifact_role: Product-method spec (per-indicator capture profile; consumes the Capture Envelope durability delta)
scope: >
  Thin capture profile for the SEARCH-INTEREST time-series demand-durability indicator
  (e.g. Google Trends). Names the relative/normalized-series facts, the
  retroactive-native temporal regime, the entity/topic-ID and pull-date pinning, and
  the attention-not-costly-behavior gate role that drop onto the Capture Envelope of
  record + durability delta. Design + spec only.
  TERMINOLOGY: "indicator" is the demand-side observable; "proxy" is reserved for the
  NETWORK sense (ProxyProfile). The keystone delta / taxonomy still say "proxy" for
  this concept — reconciliation pending (see deconfliction note).
use_when:
  - Specifying or reviewing capture of a search-interest series for a demand-durability read.
  - Checking how a normalized, re-normalized-per-pull series sits on the Source Capture packet + durability delta.
  - Checking why search interest cannot clear the costly-behavior floor on its own.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/product/product_lead/orca_demand_read_taxonomy_v0.md                          # trend vector (Layer 1) + attention-volume guard
  - docs/product/product_lead/orca_buyer_proof_packet_v0.md                            # search-interest = G1 UNSOURCED gap; attention caps ceiling
  - docs/product/data_capture_spine/data_capture_source_access_method_plan_v0.md
stale_if:
  - The keystone durability delta changes the five elements.
  - The demand-read taxonomy or Demand-Substrate Hard Gate changes the trend-vector / attention-volume role.
  - The Source Capture packet schema changes PacketTiming or posture vocabularies.
  - An owner decision adopts, narrows, or rejects any search-interest capture fact below.
```

- Status: `PROFILE_DRAFT_V0`
- Artifact type: Per-indicator capture profile (subordinate to the durability delta; not a new envelope)
- Implementation authorized: no · Feature planning authorized: no · Runtime/source-system design authorized: no · Contract hardening authorized: no (owner-gated, out of scope)

## What This Is (And Consumes)

A thin per-indicator profile on the **Capture Envelope of record** (`models.py` +
obligation contract) and the **durability delta**
(`capture_envelope_durability_delta_spec_v0.md`; it calls these observables "proxies" —
same concept, renamed "indicator" here). Adds no provenance field, re-specs no
durability element; supplies only the search-interest bindings. On conflict, the schema /
obligation contract / delta win.

Scope note (owner, 2026-06-15): demand-durability reading is **one decision Orca can
help with**, not Orca's whole job.

## The Demand Read This Indicator Serves (read-trace) — and its hard ceiling

Search interest is a **Layer 1 trend-vector** signal in the demand-read taxonomy: it
carries direction, velocity, and (over a long enough series) **shape/durability** — good
for *what horizon is this on?*, **not** for magnitude comparison across topics.

**The load-bearing gate fact:** search interest is **attention, not costly behavior.**
Per the Demand-Substrate Hard Gate (buyer-proof packet): engagement/attention volume
**never clears the G2 floor** and **caps the action ceiling** instead. Search interest is
additionally a **named G1 *unsourced gap*** in the gate today ("review-surface and
search-interest are unsourced gaps, owner-owned"). So:

| Captured search-interest fact | Serves which read | Floor/ceiling role |
| --- | --- | --- |
| Relative interest series (shape over time) | Trend-vector durability shape (durable-vs-transient *hint*) | **Ceiling-only**; cannot clear the floor alone |
| Rising/falling/plateau shape | Persistence observation input (taxonomy calling sequence) | Context for the durable upgrade; never the costly-behavior anchor |
| Breakout / spike marker (source-exposed) | Transient-spike *candidate* flag | A candidate to corroborate with costly behavior, never a verdict |

Capturing this indicator must **not** let attention masquerade as demand — the profile
captures the series and its limits; the gate (downstream) holds the ceiling.

## Temporal Regime — per durability delta Element 5

Search interest is **retroactive-native**: the source (e.g. Google Trends) natively
exposes its **own** historical series, so a single pull recovers a back-run of prior
states. The series can reach *backward* past Orca's cold start because the **source**
carries the history.

- **Cold-start (delta Element 2)** still applies to *Orca's own* coverage, but
  `pre_coverage_history_posture` is **largely satisfied by retroactive-native history** —
  recorded as such, **with the source as the basis** and bounded by how far the source's
  own history reaches (and its granularity, which the source coarsens for longer
  windows).
- This indicator is therefore **available immediately** for a durability-shape read (no
  forward tracking window required), unlike forward-only price/availability.

## Search-Interest-Specific Capture Facts

Each an observed `VisibleFact`; none a score or judgment.

- **`interest_series`** — the ordered relative-interest values **as the source presents
  them**, captured verbatim with their time buckets. The series is
  **relative/normalized (0–100-style index), not absolute volume** — record this as a
  first-class limitation, not a hidden assumption.
- **`normalization_basis`** — what the source normalized *to* (the series is rescaled so
  the window max = 100); captured as a fact because it makes cross-pull and cross-topic
  comparison invalid unless controlled.
- **`series_shape_window`** — the time window and bucket granularity of the pull (the
  source coarsens granularity for longer windows — daily vs weekly vs monthly).
- **`geo_scope`** — the geographic scope of the series (Trends is geo-scoped).
- **breakout/related markers** — any source-exposed "breakout" or rising/top related
  query/topic, captured verbatim as shown (not re-ranked, not interpreted).

These are source-visible facts (Ob.6). They are **not** a demand magnitude, **not**
comparable in absolute terms across topics/pulls, and **not** ECR fields.

## Pinning (delta Element 1) — search-interest-specific

The pins for this indicator are **different** from the price/availability set, and
getting them wrong silently corrupts the series:

- **`entity_topic_id_pin`** — pin the source's **entity/topic ID, NOT the raw search
  string.** A topic ID (the source's disambiguated entity) is stable across
  spelling/language and excludes homonyms; a raw string conflates unrelated meanings and
  shifts as the source re-disambiguates. **This is the controlling pin.**
- **`pull_date_pin`** — stamp the **date of the pull.** The source **re-normalizes the
  whole series per pull** (the window max defining "100" moves as new data arrives), so
  the *same* historical window pulled on two dates can differ. Two pulls are only
  comparable with their pull dates recorded; capture never silently overwrites an
  earlier pull's series.
- **`geo_locale_pin`** — the geo scope and interface locale of the pull.
- `currency_pin` / `variant_pin` / `session_visibility_pin` → `not_applicable` with
  reason.

Unknown/unexposed → `unknown_with_reason` / `unavailable_by_source`, never guessed.

## Capture Method & Boundary

Per the method plan (discoverable-or-entitled + disclosable; measured-ToS; industrial
scraping rejected):

1. **Structured access** — the source's own export/CSV/unofficial-API surface for the
   normalized series is the natural route (method-plan Method 1 family; structured access
   "does not define what counts as evidence" — availability ≠ validity).
2. **Rendered/headless browser** — when only the rendered widget exposes the series
   (Methods 2/3/10).
3. **Manual human-browser capture** — for one-off pulls (Method 8).

Capture mode disclosed (Ob.4). The **relative/re-normalized** nature is recorded as a
capture limitation regardless of method.

## Series Integrity (delta Element 3)

Two integrity concerns specific to this indicator, both **recorded, not concluded**:

- **Re-normalization drift** — because the source re-normalizes per pull, the series-diff
  must compare **pull-to-pull with pull dates**, and record apparent value changes that
  are re-normalization artifacts (not real interest changes) as a visible limitation.
  Anchored on `PreservedFile.sha256` of each pull's raw export.
- **Topic-ID reassignment** — if the source re-disambiguates the topic/entity between
  pulls, record it as a locator/entity migration (series-diff change event), since it
  breaks comparability.

No deletion-detection role here (the source serves its own history; there is no
disappearing-item integrity signal as in reviews).

## Cadence (delta Element 4)

Cadence is the measurement-resolution + honesty knob; for this retroactive-native
indicator it decides **re-pull frequency** (not forward coverage of otherwise-
unrecoverable state): how often you re-snapshot to catch shape changes and re-normalization
drift, and how honestly you can state that the shape "held" between pulls. **It must be
expressed on the indicator's sampling rhythm — hourly to daily (owner, 2026-06-15)**, not the seconds-scale `CadencePlan`
was built for; `CadencePlan` lends vocabulary only, and a real time-scale series cadence
is a confirmed need whose primitive is a build/hardening step (out of scope). Declare
intended re-pull cadence, record realized pull dates, and record each pull as a distinct
series snapshot (never overwrite).

## Manipulability & Integrity Posture

Search interest is **attention**, and attention is manipulable (coordinated search
campaigns, bot-driven query spikes) — but more fundamentally it is **the wrong tier** to
anchor a demand read on regardless of manipulation. Under the manipulable-input rule it
is **sentiment/attention input** that **caps the ceiling**; it **never clears the
costly-behavior floor.** A search spike is a *transient-spike candidate* to corroborate
with costly behavior (availability/review/forum), never a standalone trigger. Capture
records the shape and the relative-not-absolute limitation; the gate holds the ceiling.

## Deconfliction (per-indicator)

- **Already covered — do NOT re-spec:** envelope/provenance (schema + obligation
  contract); durability elements (delta).
- **Genuinely new here:** the **relative/re-normalized series facts**, the
  **entity/topic-ID-not-raw-string** pin, the **pull-date** pin and per-pull snapshot
  discipline, the **re-normalization-drift** integrity note, and the explicit
  **attention-caps-ceiling / G1-unsourced-gap** read-trace.
- **Not this indicator:** no existing capture lane covers search interest (confirmed by
  source sweep; it is a named G1 unsourced gap). It is not org-motion (EDGAR lane,
  deferred) and not a forum/review surface. This profile scopes the *capture* side of the
  G1 gap; it does not close the gate's sourcing decision (owner-owned).

## INV-1 Preservation

Every element is a captured fact or a capture method/pin/regime — never a weight, score,
threshold, ranking, or durability verdict. The relative index is captured **as the
source's own number**, not as an Orca-computed magnitude or score; durable-vs-transient
shape reading is downstream, consumed from the taxonomy/gate, never decided here.

## Boundaries, Non-Goals, Non-Claims

- No build/scrape/run/deploy; no scheduler/monitor; primitives referenced only.
- No edits to `models.py` or the obligation contract; field promotion is contract
  hardening (owner-gated, out of scope).
- No ECR/Cleaning/Judgment design; no cross-topic magnitude comparison; no
  attention-as-demand inference.
- **Commissioned capture only (Ob.1) today.** Continuous monitoring of this indicator is
  owner-confirmed as wanted (2026-06-15) but is gated on a standing-capture obligation
  home that does not yet exist (see deconfliction note); this profile does not authorize
  standing collection.
- Not validation, readiness, acceptance, source-of-truth promotion, buyer proof,
  implementation/runtime/tooling authorization, source-access boundary amendment, or
  commercial-readiness evidence.
```
