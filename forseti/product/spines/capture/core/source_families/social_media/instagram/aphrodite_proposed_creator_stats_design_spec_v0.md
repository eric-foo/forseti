# Aphrodite Proposed Creator Stats — Design Spec (proposed, v0)

```yaml
retrieval_header_version: 1
artifact_role: proposed capability spec (non-authorizing) — Aphrodite proposed creator monitoring / derived stats, design-only recipe cards
scope: >
  Design-only recipe specs for the proposed (not-yet-built) creator monitoring and
  derived stats named in the Aphrodite Silver metric monitoring inventory: temporal
  metrics (SMA, EMA, compatible-window velocity, capture-window delta), event states
  (spike score, breakout state, decay/plateau, active-watch expiry), a momentum /
  wind-calling call score, an interim sub-niche classifier, and a NEW video-format /
  video-type classification with a per-creator format x observed-success rollup. Each
  card names what it computes, its inputs, required history/sample support, posture and
  missingness behavior, Silver routing + a named calculation_recipe_version, the
  provenance fields it must carry, and an honest design-only build-status. Produces
  recipe specs, not runtime code.
use_when:
  - Scoping or authorizing an implementation lane for any proposed Aphrodite creator stat.
  - Checking how a proposed creator stat must route through Silver and satisfy the derived-claim provenance contract.
  - Deciding what history / sample support a proposed stat needs before it may emit an observed value.
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_silver_metric_monitoring_inventory_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md
  - forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_momentum_pipeline_architecture_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_creator_ideal_audience_inference_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_capture_shape_contract_spec_v0.md
  - forseti/product/spines/capture/core/source_families/social_media/instagram/ig_reels_transcript_product_extraction_spec_v0.md
stale_if:
  - A proposed stat here lands with a recipe/version/runner (it then graduates out of this design lane).
  - The creator metric Silver record contract changes MetricObservation / MetricRollupObservation posture, derivation, or lineage semantics.
  - The creator_profile_current contract changes the recent_velocity / posting_cadence declared-deferred fields or its visible field set.
  - The derived-claim provenance contract changes its required field set or display rule.
  - The Aphrodite inventory, monitoring policy, or momentum pipeline is superseded.
  - The ontology SubNiche object type is dispatched (the sub-niche card must then bind to it, not re-invent it).
```

## Status

`PROPOSED_DESIGN_SPEC_V0`. Design only. This document turns the proposed /
deferred creator-channel stats from the Aphrodite Silver metric monitoring
inventory into buildable recipe specs. It does **not** implement, run live
capture, write to the lake, create metric records, choose a backend, or claim
readiness, validation, or buyer proof. Implementation of any card here is a
separate, explicitly authorized step.

This spec is the design-lane discharge of
`docs/workflows/aphrodite_proposed_creator_stats_design_handoff_v0.md` (an
external-worktree handoff). It reads its `open_first` sources at their current
`origin/main` state: PR #777 (the Aphrodite inventory + capture strategy) is
merged into `main` in this worktree, so those sources are read in-tree, not on
the unmerged branch the handoff assumed.

## What this is for / done looks like

**Goal:** each proposed creator stat has a recipe card naming what it computes,
its inputs, required history/sample support, posture/missingness behavior, Silver
routing + a named `calculation_recipe_version`, the provenance fields it must
carry, and an honest design-only build-status — so a later authorized lane can
implement it without re-deciding intent.

**Scope grounding:** creator-channel stats only, from the inventory's
`proposed` / `deferred` rows
(`docs/research/aphrodite_silver_metric_monitoring_inventory_v0.md`, "Aphrodite
Monitoring Recipes: Implemented Versus Absent" + "Deferred Creator Metric
Fields"). AEO / search-interest and other non-creator surfaces are out of scope.

## Shared design contract (every card below inherits this — stated once)

Every recipe card inherits the following. A card only records its **deltas** from
this shared contract; it does not restate these rules.

### S1 — Route through Silver; never compute in the read model

Each stat is a Silver Vault record — a `MetricObservation` or
`MetricRollupObservation` — emitted by a Silver producer, carrying the common
header, a named `calculation_recipe_version`, `source_metric_observation_ids`
and/or `derived_refs` lineage edges, posture/value coupling, `sample_support`,
`freshness_state`, and `limitations`, per
`.../creator_registry/creator_metric_silver_record_contract_v0.md`. **Nothing
here is computed inside `creator_profile_current`** — that read model copies only
accepted, lineage-backed fields
(`.../creator_registry/creator_profile_current_record_contract_v0.md`, "Read
Model Boundary"). This is the inventory's load-bearing rule ("Do not compute
those inside `creator_profile_current` as hidden product logic. Silver owns the
recipe-backed observations and rollups").

### S2 — Posture / value coupling (missing ≠ zero)

```text
observed / resolved  => value present, no reason
non-observed         => value null (or state `insufficient_evidence`), explicit reason
```

Zero is valid only as a real source-backed observed zero. Missing, hidden,
blocked, out-of-window, not-applicable, and not-attempted are **never** zero and
must not be ranked, averaged, or displayed as low performance. Each card names
its **required history window** and **minimum sample support**; below the floor
it abstains with a reason, it does not emit a low/zero value.

### S3 — Compatibility gate (what may be composed)

A recipe that composes prior Silver records may only use **compatible** inputs:
same `platform_scope`, `content_kind_inclusion_rule`, **`source_surface`** (S3.1),
selection policy, and a compatible or explicitly-normalized `rollup_window`, with
visible sample support and no limitation that rules out the composition
(`creator_profile_current_record_contract_v0.md`, "Metric Comparison Rules").
Incompatible inputs → abstain-with-reason, never a silent blend.

### S3.1 — Base-metric source-surface provenance (view counts)

The default base metric `average_views` is defined against a **declared
`source_surface`**, because IG exposes the same `view_count` from surfaces that
disagree. **Current-view is already settled — not a blocker:** the grid/clip
**reels-tab pair supersedes** as the authoritative current-view (grid DOM view text
+ `/api/v1/clips/user/` agree and match what IG shows the viewer), so the base-metric
series **computes on it now**. Every card composes a **same-surface** series on that
current-view pair and never merges surfaces. The rule is recorded on the **grid
capture-shape contract** (`ig_capture_shape_contract_spec_v0.md`, "View-count
source-surface provenance").

- **`web_profile_info`** = a separate provenance-tagged candidate **and** the
  deep-history source (the only surface that paginates back years logged-out); it
  **under-reports current view**, so it is used for **old reels only**, flagged
  lower-trust / cumulative-at-capture, and **never mixed into current-view**.

A series that would have to mix surfaces abstains (`incompatible_source_surface`)
rather than blend. The one open item — `web_profile_info`'s convergence probe (laggy
cache vs a different cumulative metric) — gates that **deep-history fallback's
trust**, **not** the current-view stats, which run on the grid/clip pair today.

### S4 — Two derivation families (which provenance discipline applies)

Every card is one of two kinds. Both are Silver records; they differ in the
lineage/provenance they carry.

- **Calculation-derived** (arithmetic or deterministic rules over source-backed
  observations): SMA, EMA, compatible-window velocity, capture-window delta,
  spike score, breakout state, decay/plateau state, active-watch expiry, the
  momentum-call rule core, and the format x success rollup. These carry the
  Silver `derivation` marker (`kind: computed_*`, `source_record_ref_kind:
  derived_refs`, `metric_posture_semantics:
  source_input_support_not_raw_aggregate_visibility`,
  `calculation_recipe_version`) and `derived_refs` edges to every source record —
  the canonical Silver lineage, not a producer-private sidecar
  (`creator_metric_silver_record_contract_v0.md`, "Posture rule"). They do **not**
  need `extraction_model` (no model reads content).
- **Extraction-derived** (a model/deterministic reader turns captured *content*
  — transcript, caption, bio, comments, graph edges — into a label): the
  sub-niche classifier, the video-format classifier, and the momentum-call's
  optional call-text component. In addition to S1–S3 these are **derived claims**
  and MUST satisfy the derived-claim provenance contract in full before any
  Creator Signal surface may show them.

### S5 — Derived-claim provenance (extraction-derived cards + interpretive states)

Any card whose output is a *derived claim* — every extraction-derived card, plus
the interpretive event states (breakout, decay/plateau, active-watch) and the
momentum call — resolves to `show | downgrade | withhold` and carries, per claim
(`.../creator_signal/aphrodite_derived_claim_provenance_contract_v0.md`):
`source_refs`, `extraction_model` (or the deterministic rule/recipe id for
rule-based states), `extraction_recipe_version`, `input_content_hash`,
`extraction_timestamp`, `receipt` (the supporting quotes / observations /
matched drivers), and `confidence_or_abstention`. **A claim missing any required
field withholds — it is never zero-filled or shown as absence-of-signal.** No
single "vanity" score may collapse multiple derived signals into one figure that
hides its inputs' weakness.

### S6 — Recipe-card skeleton

Each card fills exactly these slots (delta-only against S1–S5):

1. **Computes** — one line.
2. **Inputs** — the source observations/rollups/content it reads.
3. **Recipe** — the formula or decision rule.
4. **Required history / sample support** — window + minimum N; the abstain floor.
5. **Posture & missingness delta** — the specific non-observed reasons.
6. **Silver routing** — record kind, named `calculation_recipe_version`, lineage
   edges, derivation/provenance family (S4/S5).
7. **Build-status & activation prerequisites** — design-only; what must exist
   first.

### S7 — No new visible field is assumed in `creator_profile_current`

Only `recent_velocity` and `posting_cadence` are declared-deferred fields in the
`creator_profile_current` visible surface. Of the cards below, **only
compatible-window velocity binds to an existing field** (`recent_velocity`). All
other cards emit **new Silver records**; surfacing them either requires a
separately-authorized extension of the `creator_profile_current` field set (a
record-surface change) or a Creator Signal surface that reads them from Silver
directly. This spec does not authorize either surface change.

### S8 — Forbidden across all cards

No person-level identity or demographics; no follower/commenter graph capture; no
credibility / durability / fake-bot-paid / manufactured-demand verdict; no action
recommendation, ranking, or performance guarantee from Silver alone; no market
total or cross-platform share; no cross-platform creator rollup without promoted
linkage authority
(`.../data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
forbidden set, as cited in the inventory). Momentum and engagement are
**allocation** signals, not authority
(`forseti_creator_monitoring_policy_architecture_v0.md`, "Result").

## Data-layer flow — Silver computes, the registry rolls up a summary

This is a **capability / recipe spec, not architecture planning**: it rides the
data-layer placement already accepted in the capture strategy
(`aphrodite_creator_capture_strategy_v0.md`, "Data-Layer Placement"), the monitoring
policy, and the momentum-pipeline architecture. That placement, made explicit for
these stats:

```text
raw capture / Bronze packets  →  Silver Vault              →  creator registry            →  Aphrodite Signals
sole system of record;           ALL recipes compute here     creator_profile_current:       buyer/operator display;
per-metric typed value+posture;  as MetricObservation /       a CURRENT read model that      reads accepted fields +
source_surface provenance;       MetricRollupObservation;     COPIES the latest accepted,    limitations/freshness;
history is un-re-capturable       posture + derived_refs       lineage-backed summary —       never the metric
                                  lineage; owns the recipes    it never computes              authority
```

**Where each stat lives (the split):**

- **All 11 recipes compute in Silver.** Nothing computes in the registry read model
  (S1).
- **Per-post / per-reel / per-event records stay Silver, keyed to the
  post/reel/event** — a spike on one reel, a breakout state on one post, a reel's
  `format_label` / `product_density`. They are **not** collapsed into the creator
  profile (that would bloat and misrepresent a current-summary panel).
- **The registry rolls up only the current per-creator SUMMARY** — the fields with
  a home in `creator_profile_current.current_metric_rollups`. Today: the existing
  engagement rollup; on activation, `recent_velocity` (= §1.3). **Only §1.3 binds
  an existing registry field.**
- **The new per-creator aggregates** (SMA/EMA series, momentum call, sub-niche
  label, format×success rollup) have **no registry field**. Default (steerable):
  they stay **Silver-side, read by Signals directly**, rather than expanding the
  fixed `current_metric_rollups` field set — that expansion is a higher-lock-in
  registry-contract change (S7). Materializing any of them into the profile panel
  is a separately-authorized registry surface extension.

## How (and when) each stat computes

These recipes are formulaic *by design*, but "dump new capture data in and it
calculates" is only partly true — and differently for the two families (S4):

- **Existing rollups (`average_views`, `engagement_rate`)** already compute that
  way: a deterministic function over one capture's admitted pool, run by the Silver
  producer when data lands.
- **New calculation-derived stats (§1–§3, §5.3)** are also pure formulas/rules —
  but most are **not** point-in-time over a single capture; they need an accumulated
  **compatible time-series** (S3). Velocity needs ≥2 compatible rollups; SMA needs
  *k*; spike needs a baseline. So they **auto-populate only after enough heartbeat
  cycles have accumulated compatible history** — a single capture cannot produce
  them (this is why the inventory marks them deferred: the *formula* is ready, the
  *history* is the gate). They are **not already coded inside**: the current producer
  computes only `average_*` / `engagement_rate`, and the revalidation module today
  lists velocity/cadence as `_NEVER_COMPUTED`. Implementing each new recipe (formula
  + named `calculation_recipe_version`) in the Silver producer is the step this
  design scopes; then it auto-computes over history.
- **New extraction-derived stats (§4 sub-niche, §5 video-format + product density /
  emphasis)** are **not** pure formulas: they need a model/extractor **pass over
  content** (transcript / caption / bio) to turn text into a label. New data triggers
  an **extraction run** (with cost, provenance, confidence/abstention), not an
  arithmetic auto-calc. The *fusion* step (code deciding the label from cached
  evidence) is formulaic and re-runs free; the *reading* step is a model call that
  re-runs when the model/rubric version changes.

**Net:** dumping data auto-calculates the existing rollups; the new stats need
(a) their recipe implemented in the Silver producer, plus (b) enough accumulated
compatible history (§1–§3, §5.3) or (c) an extraction pass (§4–§5).

---

## 1. Temporal metrics

Shared for §1.1–§1.4: **window basis** is a series of *compatible* Silver rollups
(S3) for one subject/scope/window, ordered by `computed_at`; **base metric**
defaults to `average_views` (a later recipe version may name `engagement_rate` or
another observed rollup key); **degradation** — normalization per elapsed time is
allowed only from `computed_at` / window-endpoint timestamps (which the rollups
carry), never from per-post publication timing. Where per-post publication timing
is unavailable, velocity degrades to the **capture-window delta** (§1.4), which
never implies posting cadence or content-age velocity (inventory + strategy: "If
publication timestamp is missing or unreliable, call the trend `capture-window
delta`, not posting cadence or content age velocity").

### 1.1 `simple_moving_average`

- **Computes:** the arithmetic mean of the base metric over the last *k*
  compatible rollups (a smoothed level, not a single-capture pool mean).
- **Inputs:** *k* consecutive compatible `MetricRollupObservation` base-metric
  values for the subject.
- **Recipe:** `SMA_k = mean(base_metric[t-k+1 .. t])`.
- **Required history / sample support:** ≥ *k* compatible rollups (recipe pins
  *k*, e.g. k=3); `sample_support` records the *k* used. Below *k* → abstain
  (`insufficient_history`).
- **Posture delta:** observed only if all *k* base values are observed; any
  non-observed member → abstain (do not impute).
- **Silver routing:** new `MetricRollupObservation`, `rollup_kind:
  temporal_moving_average`; `calculation_recipe_version:
  creator_metric_sma_ig_reels_grid_average_views_v0`; `derived_refs` → each source
  rollup; calculation-derived (S4). Must not overwrite the raw `average_views`
  rollup — it is a distinct derived series.
- **Build-status:** design-only. Prereq: ≥ *k* compatible rollups exist in Silver
  history for a subject; the Silver record contract admits the new `rollup_kind`
  + derivation `kind: computed_temporal_metric`.

### 1.2 `exponential_moving_average`

- **Computes:** a recency-weighted moving average of the base metric.
- **Inputs:** the compatible base-metric rollup series + a pinned smoothing
  factor α (in the recipe version).
- **Recipe:** `EMA_t = α·base_metric[t] + (1-α)·EMA_{t-1}`, seeded by the first
  observed value (seed policy pinned in the recipe version).
- **Required history / sample support:** a recipe-pinned minimum series length
  before EMA is emitted (an EMA over 1–2 points is not a trend); `sample_support`
  records series length and α. Below the floor → abstain.
- **Posture delta:** observed only over an unbroken run of observed base values;
  a gap breaks the run and forces abstain-with-reason (`series_gap`), never
  carry-forward of a stale value as if observed.
- **Silver routing:** `MetricRollupObservation`, `rollup_kind:
  temporal_exponential_moving_average`; `calculation_recipe_version:
  creator_metric_ema_ig_reels_grid_average_views_v0` (α is part of the version
  identity); calculation-derived.
- **Build-status:** design-only. Prereq as §1.1 + a pinned α and seed policy.

### 1.3 `compatible_window_velocity` — binds to the deferred `recent_velocity`

- **Computes:** rate of change of the base metric between two compatible rollups
  per elapsed time. **This is the recipe that first-populates the declared-deferred
  `recent_velocity` field; it does not create a new field**
  (`creator_profile_current_record_contract_v0.md` §3, `recent_velocity`).
- **Inputs:** the latest and a prior compatible `MetricRollupObservation` for the
  subject; their `computed_at` / window endpoints.
- **Recipe:**
  `recent_velocity = (latest_base − prior_base) / elapsed_days_between_rollups`
  (the contract's pinned target).
- **Required history / sample support:** ≥ 2 compatible rollups; observed base in
  both; **positive** elapsed time; source record ids for both rollups and their
  underlying observations. A single capture cycle cannot produce velocity.
- **Posture delta:** if compatible history does not exist, the field stays
  `not_attempted` / non-observed with a reason (the contract's rule). Population
  changes make the trend directional, not representative → carry that
  `limitations` note.
- **Silver routing:** `MetricRollupObservation` supplying the existing
  `recent_velocity` rollup key; `calculation_recipe_version:
  creator_metric_recent_velocity_ig_reels_grid_average_views_v0`; `derived_refs`
  → both source rollups; calculation-derived. Follows the contract's **First
  Population Rule** (no schema change; the read model copies the observed value
  once Silver emits it with lineage + posture).
- **Build-status:** design-only. Prereq: ≥ 2 compatible rollups with positive
  elapsed time; the named recipe version registered in
  `rollup_formula_revalidation` (which today lists `recent_velocity` under
  `_NEVER_COMPUTED_METRICS`).

### 1.4 `capture_window_delta` — the publication-timing-free degradation

- **Computes:** the raw magnitude change of the base metric between two
  **capture windows**, explicitly labeled by capture window — **not** normalized
  per unit time and never implying posting cadence or content-age velocity.
- **Inputs:** two comparable captures of the base metric with explicit
  capture-window boundaries (the capture-shape contract's coverage boundary).
- **Recipe:** `capture_window_delta = base_metric[capture_B] − base_metric[capture_A]`,
  carrying both capture-window labels; no per-day division.
- **Required history / sample support:** ≥ 2 comparable captures with declared,
  non-overlapping-or-labeled capture windows. If the windows are not comparable →
  abstain (`incomparable_capture_windows`).
- **Posture delta:** this is the honest fallback when velocity's elapsed-time
  normalization would over-claim (missing/unreliable publication timing, or
  changed capture cadence). It states magnitude-between-captures only.
- **Silver routing:** `MetricObservation` (or a `MetricRollupObservation` over
  rollups), `metric_name: capture_window_delta`; `calculation_recipe_version:
  creator_metric_capture_window_delta_ig_reels_grid_average_views_v0`;
  calculation-derived; carries an explicit `capture_window` pair, not a
  `rollup_window` velocity.
- **Build-status:** design-only. Prereq: two comparable captures with recorded
  capture-window boundaries. Distinct from the existing freshness gate, which
  compares snapshots for staleness, not magnitude.

---

## 2. Event states

§2.1 is a numeric derived metric (calculation-derived). §2.2–§2.4 are
**interpretive derived states** — calculation/rule-based, but their output is a
categorical *claim*, so they carry S5 provenance (receipt = the supporting
observations; `extraction_model` = the deterministic rule id + version) and
resolve `show | downgrade | withhold`. State posture coupling: **resolved state
⇔ non-null state label with supporting inputs; unresolved ⇔ state
`insufficient_evidence` + reason** (never a false "stable"/"neither" that reads
as a real observation of no-event). These feed the strategy's promotion gates
(`spike_gate`, `fresh_breakout_gate`, `active_breakout_gate`) as **allocation**
signals, not authority.

### 2.1 `spike_score`

- **Computes:** how unusual the latest observed value is against the creator's
  compatible recent baseline, or a platform/content-kind norm when the creator
  baseline is too thin.
- **Inputs:** latest observed base value; a baseline (SMA/EMA §1.1–§1.2 over the
  subject) or a declared platform/content-kind norm; a dispersion estimate.
- **Recipe:** a normalized deviation, e.g.
  `spike_score = (latest − baseline) / dispersion` (standardized) or a ratio
  form; the recipe version pins the baseline source, dispersion estimator, and
  whether creator-baseline or norm is used (and records which was used).
- **Required history / sample support:** a recipe-pinned minimum baseline length;
  below it, fall back to the declared norm; below both → abstain
  (`no_baseline`). Never treat a missing input as a low value.
- **Posture delta:** observed numeric only when baseline + latest are observed;
  otherwise abstain. A large score over a thin sample carries a
  `thin_baseline` limitation.
- **Silver routing:** `MetricObservation`, `metric_name: spike_score`;
  `calculation_recipe_version: creator_event_spike_score_ig_reels_grid_v0`;
  `derived_refs` → latest value + baseline rollups; calculation-derived. Explicitly
  **not** the parked Data-Lake movement-threshold vocabulary (which is
  gate-blocked and must not be relabeled as an Aphrodite spike).
- **Build-status:** design-only. Prereq: a baseline recipe (§1) exists, or a
  declared, sourced platform/content-kind norm.

### 2.2 `breakout_state` — high **and** still growing

- **Computes:** a state combining a **level** condition (high vs
  baseline/norm — via §2.1) with a **slope** condition (still growing — via §1.3
  velocity / §1.2 EMA slope). High lifetime views alone is not breakout.
- **Inputs:** `spike_score` (§2.1) + velocity/slope (§1.3/§1.2), with pinned
  thresholds in the recipe version.
- **Recipe (decision rule):**
  `breakout_active` iff `level ≥ level_threshold AND slope > 0`; else
  `high_not_growing` / `growing_not_high` / `neither`; `insufficient_evidence`
  when either input abstains.
- **Required history / sample support:** both inputs observed and above their
  sample floors; else `insufficient_evidence`.
- **Posture / provenance:** interpretive derived state → S5. `receipt` = the
  spike + velocity observations; `confidence_or_abstention` from the weaker
  input.
- **Silver routing:** `MetricObservation` state record, `metric_name:
  breakout_state`; `calculation_recipe_version:
  creator_event_breakout_state_ig_reels_grid_v0`; calculation-derived state +
  derived-claim display discipline.
- **Build-status:** design-only. Prereq: §2.1 + §1.3 recipes; pinned thresholds.
  Implements the strategy's `fresh_breakout_gate`.

### 2.3 `decay_or_plateau_state`

- **Computes:** whether a previously-rising subject/post is now decaying,
  plateaued, or still rising, from repeated observations and a declared
  slope/plateau profile.
- **Inputs:** the recent base-metric/EMA series (§1) for the subject/post; a
  pinned slope band and plateau tolerance.
- **Recipe (decision rule):** classify the recent slope: `decaying` (slope <
  −band), `plateaued` (|slope| ≤ tolerance over ≥ m samples), `rising` (slope >
  band); `insufficient_evidence` below the sample floor.
- **Required history / sample support:** ≥ *m* recent observations (recipe pins
  *m*); below → `insufficient_evidence`.
- **Posture / provenance:** interpretive derived state → S5.
- **Silver routing:** `MetricObservation` state record, `metric_name:
  decay_or_plateau_state`; `calculation_recipe_version:
  creator_event_decay_plateau_state_ig_reels_grid_v0`.
- **Build-status:** design-only. Prereq: a base series (§1). Drives demotion
  (strategy: "demote them when their growth decays").

### 2.4 `active_watch_expiry_state` — explicit, source-backed, self-expiring

- **Computes:** whether a promoted breakout/durable-watch item is currently under
  an explicit recheck watch and when that watch **expires** — no hidden
  forever-watch (strategy "Falling Out Of Grid": "explicit, source-backed, and
  self-expiring").
- **Inputs:** the promotion event that opened the watch (its trigger + source
  refs); the declared watch window + recheck cadence; the latest
  decay/slope reading (§2.3).
- **Recipe (state machine):**
  `not_watched` → (promotion trigger) → `watching{opened_at, expires_at,
  recheck_cadence, reason, source_refs}` → `expired` when
  `now ≥ expires_at` OR slope falls below the accepted threshold for the accepted
  number of checks OR an age/read cap is hit. `expired` ⇒ cold by default unless a
  **fresh** trigger re-opens a new watch. Expiry is a hard, recorded timestamp.
- **Required history / sample support:** a real, source-backed opening trigger;
  no watch may exist without one. No standing/global watch list.
- **Posture / provenance:** interpretive derived state → S5; `receipt` = the
  opening trigger + latest recheck reading; the record itself carries `expires_at`
  so the state is auditable and self-terminating.
- **Silver routing:** `MetricObservation` state record, `metric_name:
  active_watch_expiry_state`; `calculation_recipe_version:
  creator_event_active_watch_expiry_ig_reels_grid_v0`. Bounded re-find pagination
  for a fallen-out watched item stops on the strategy's caps (slope floor, check
  count, age/read cap, source block) — this record does not authorize a crawler.
- **Build-status:** design-only. Prereq: promotion events carry source-backed
  triggers; the monitoring policy's bounded-session posture governs any recheck
  (carve-out: human-pre-authorized, bounded, self-terminating — no standing
  daemon).

---

## 3. Momentum / wind-calling call score

- **Computes:** the actual **derived** momentum / breakout-*call* signal that
  does not exist yet. Today "wind-calling" is **capture-only** — the WindCaller
  calls-capture lane preserves call *text* + engagement raw
  (`ig_wind_caller_calls_capture_build_architecture_v0.md`), and the momentum
  harness code is a raw parser that does **not** certify momentum. This card
  designs the certified derived read over those raw captures.
- **Inputs (rule core, calculation-derived):** `spike_score` (§2.1),
  `breakout_state` (§2.2), `compatible_window_velocity` (§1.3),
  `decay_or_plateau_state` (§2.3) for the subject/post. **Optional
  extraction-derived component:** the captured WindCaller call text (an LLM reads
  the call under a fixed rubric and emits evidence, per the audience-inference
  "LLM reads, code decides" discipline) — when included, that component carries
  the full S5 extraction provenance separately.
- **Recipe:** a **transparent composite**, not a vanity score: a bounded score
  plus its component breakdown (each component's value + posture shown), e.g.
  `momentum_call = f(level, slope, persistence)` with pinned weights in the
  recipe version. The composite **must expose its component inputs and their
  postures** — collapsing them into one opaque figure that hides a weak input is
  forbidden (S5 / provenance "no single vanity score").
- **Required history / sample support:** each component's own floor (§1–§2);
  if the load-bearing components abstain, the momentum call **withholds** (it does
  not emit a low score). A call from text alone, with no metric support, is
  flagged text-only and downgraded, never shown as certified momentum.
- **Posture / provenance:** derived claim → S5 in full. `source_refs` = the
  component observations + (if used) the call-text capture; `receipt` = the
  supporting observations / call quotes; `confidence_or_abstention` from the
  weakest load-bearing input.
- **Silver routing:** `MetricObservation` (derived-claim), `metric_name:
  momentum_call`; `calculation_recipe_version:
  creator_momentum_call_ig_reels_grid_v0`; calculation-derived core + optional
  extraction-derived component (separately provenanced).
- **Boundary:** an **allocation** signal and a derived read — never demand proof,
  credibility/independence certification, a partner/action recommendation, or a
  performance guarantee (monitoring policy "Result"; inventory forbidden set). It
  is distinct from, and does not relabel, the raw capture-only wind-caller.
- **Build-status:** design-only. Prereq: §1–§2 recipes exist; if the call-text
  component is included, the WindCaller call-text capture is an admitted lake
  surface and a fixed extraction rubric + model/recipe version are named.

---

## 4. Sub-niche classifier (interim)

- **Computes:** an interim sub-niche label for a creator/account (what topic —
  e.g. fragrance, skincare), pending the ontology `SubNiche` object type
  (`AUTHORED_..._AWAITING_DISPATCH`). Currently zero code exists.
- **Inputs:** bio + caption keywords; graph-cluster membership (co-occurrence /
  snowball edges). **Hashtags are deprioritized** — a 5-tag cap, used to
  *categorize not boost*, contributing only capped **secondary corroboration**
  (never a primary driver).
- **Recipe:** deterministic keyword match + graph clustering emits a label with a
  bounded confidence; **records its raw drivers** (the exact keywords matched and
  graph edges that drove the assignment) so the label **re-expresses under
  `SubNiche` deterministically on adoption, not by re-judgment** (momentum
  pipeline "Ontology coupling"). Abstain (`unknown`) when drivers are too thin or
  contradictory.
- **Required history / sample support:** a recipe-pinned minimum driver count;
  below → `unknown`. Thin/contradictory evidence abstains rather than guessing.
- **Posture / provenance:** extraction-derived claim → S5 in full. `source_refs`
  = the bio/caption/graph units; `receipt` = the matched keywords + edges (the raw
  drivers ARE the receipt); `input_content_hash` over the exact input text;
  `confidence_or_abstention` = an uncalibrated support band (not a calibrated
  probability).
- **Silver routing:** `MetricObservation` (derived-claim), `metric_name:
  sub_niche_label`, carrying `raw_drivers`; `extraction_recipe_version /
  calculation_recipe_version: creator_subniche_interim_keyword_cluster_v0`.
- **Build-status:** design-only. **Activation prerequisite / stale trigger:** when
  `SubNiche` is dispatched, this card binds to it (re-expresses raw drivers under
  the ontology object) and must **not** re-invent a competing classifier. It stays
  in discovery/ontology, not absorbed into the momentum core.

---

## 5. NEW — Video-format / video-type classification

Classify each deep-captured reel into a format/type, then roll up **which format
a given creator succeeds with** (format x observed success, per creator). Three
sub-parts: taxonomy (§5.1), per-reel classifier (§5.2), success rollup (§5.3).

### 5.1 Taxonomy — sourced, not invented; orthogonal to SubNiche

- **SubNiche relation:** **orthogonal.** Sub-niche is the *topic* axis (fragrance,
  skincare); video-format is the *delivery* axis (how the content is made —
  tutorial, review, GRWM…). A reel carries both independently. (Some formats
  correlate with niches, but format is modeled as its own axis, not a SubNiche
  sub-value.) This mirrors the audience-inference spec's own layering
  (sub-niche = what topic; audience = who it's for; format = how it's delivered).
- **Sourcing rule (load-bearing):** the taxonomy **must be sourced, not an ad-hoc
  list** (handoff constraint). No sourced content-format taxonomy exists in-repo
  today (verified: only the audience-inference "content pillars" concept exists,
  not a format taxonomy). So the taxonomy is an **activation prerequisite**, with
  three candidate sourcing paths, in preference order:
  1. **Harvest-from-observed-captures (recommended, lowest lock-in):** derive an
     emergent format taxonomy from what the deep-capture corpus actually shows for
     fragrance reels (record raw drivers per assignment, exactly as §4), then
     ratify the harvested set. Avoids importing an external list that may not fit
     the vertical; matches the repo doctrine of not freezing a schema before data.
  2. **Bind to a named external creative-format vocabulary** (a documented,
     versioned short-form content-format framework), cited and pinned by version —
     only if a suitable one is adopted by the owner.
  3. **An ontology `ContentFormat` dimension**, if one is later defined (defer to
     it as with `SubNiche`).
- The example set in the handoff (tutorial, GRWM, review, unboxing, storytime,
  transition, haul, before/after, talking-head) is recorded here as an
  **illustrative candidate seed only** — explicitly `REQUIRES_SOURCED_TAXONOMY`
  before any build; it is not asserted as the taxonomy.

### 5.2 Per-reel fields — emit SEPARATELY, never collapsed into one

Per deep-captured reel, emit these as **separate typed fields** (do **not** fold
them into a single label or score):

- **`format_label`** — the sourced format/type (§5.1): tutorial / GRWM / review /
  haul / storytime / talking-head / skit / transition / reaction … + confidence /
  abstention. Extraction-derived claim.
- **`product_density`** — the count of product mentions in the reel, consuming the
  transcript→product extraction lane's `ProductMention` records
  (`ig_reels_transcript_product_extraction_spec_v0.md`), **not re-extracted here**.
  A genuine **0 is recorded as an observed `0`** (typed absence: extraction ran and
  found none) — distinct from `not_attempted` (extraction did not run; no value).
  This is the S2 "observed zero is valid" case.
- **per-product `mention_count`** (within the reel) — a creator **emphasis** signal
  (how hard one product is pushed in one reel).

- **Inputs (in precedence order; text-first, "LLM reads, code decides"):**
  - **transcript (ASR)** — the offline VAD-gated faster-whisper `ig_reels_audio`
    surface (`ig_reels_transcript_product_extraction_spec_v0.md`); the ASR caller
    stays owner-gated/deferred, so transcript is a **named, activation-gated
    signal**, not an assumed-live input;
  - **caption / post-text** — via the separate `audience_extractor` /
    `instagram_post_text` seam;
  - **on-screen text (OCR)** — a later signal;
  - **VLM / visual** — an explicit **later upgrade, not available today**.
- **Recipe:** a fixed rubric extracts format + mention evidence with source
  pointers; code decides each field by precedence + caps + abstention (no LLM emits
  a final answer). `format_label = unknown` when evidence is thin/contradictory;
  `product_density` / `mention_count` come from the product-extraction lane's
  located mentions.
- **Guardrails (must hold):**
  - **Emphasis ≠ demand.** `mention_count` / repetition is a creator *emphasis*
    signal only; **demand needs OBSERVED audience response** and is never inferred
    from repetition.
  - **Emphasis + missing disclosure = a review-candidate flag only.** High emphasis
    with no source-visible disclosure emits a `possible_undisclosed_push` **review
    candidate** — **never** a paid/unpaid or stealth-ad **verdict** (forbidden
    Gold/Judgment). `is_paid_partnership` stays **candidate-only**, and observed
    `false` ≠ "not an ad".
  - Every derived field routes through the derived-claim provenance contract (S5):
    source refs, recipe version, confidence/abstention; **withhold, never
    zero-fill** (except `product_density`'s genuine observed 0).
- **Required history / sample support:** at least one usable text signal per reel;
  caption-light + transcript-gated reels abstain on `format_label` (lower coverage,
  higher trust — by design).
- **Silver routing:** one or more `MetricObservation` records (derived-claim) per
  reel — `video_format_label`, `product_density`, per-product `mention_count` —
  each keyed to the reel (public content object, **not** a person);
  `extraction_recipe_version: creator_video_format_class_ig_reels_v0`. Per reel:
  `source_refs` = its transcript/caption/mention units; `input_content_hash` over
  the exact classified text; `receipt` = the driving spans; `confidence_or_abstention`
  = an uncalibrated support band.
- **Build-status:** design-only. Prereqs: §5.1 taxonomy ratified; the
  transcript→product extraction lane for mention counts; the ASR caller authorized
  for the transcript signal (else caption-only, higher abstention).

### 5.3 Per-creator format x emphasis x success rollup — descriptive only

- **Computes:** for one creator, an **emphasis pattern for review** — format ×
  product-density × per-product emphasis × **observed** success — e.g. "this
  creator's GRWMs push one hero product 5× and those out-view the rest."
  **Descriptive only**, per creator; **an emphasis pattern surfaced for review,
  never a demand, ad, causal, or performance claim** (the §5.2 guardrails travel
  with the rollup: emphasis ≠ demand; no undisclosed-push verdict).
- **Inputs:** the creator's per-reel `format_label`, `product_density`, per-product
  `mention_count` (§5.2), joined to each reel's **observed** view/engagement
  metrics; grouped into per-format buckets.
- **Recipe:** per format bucket, summarize the observed success distribution
  (e.g. median views/engagement) with the bucket's sample support; report the
  within-creator format ordering as a descriptive comparison, not a score.
- **Required history / sample support (gate):** a recipe-pinned **minimum reels
  per format bucket** before that bucket is emitted or compared; below it the
  bucket is `insufficient_sample` (shown with reason, never ranked). Only
  `observed` success metrics enter the rollup (S2/S3); non-observed reels are
  excluded with reason, not zero-filled.
- **Posture / provenance:** calculation-derived rollup over the (extraction-derived)
  labels + (observed) metrics; each bucket carries its own `sample_support` and
  `limitations` (labels are inferred; success is a within-creator descriptive
  comparison, not cross-creator ranking).
- **Silver routing:** `MetricRollupObservation`, `rollup_kind:
  format_success_descriptive`; `calculation_recipe_version:
  creator_format_success_rollup_ig_reels_v0`; `derived_refs` → the per-reel format
  labels + the reels' metric observations.
- **Boundary:** **within-creator descriptive only.** No cross-creator format
  ranking, lead list, or "best format" recommendation — those need a separate
  accepted Creator Signal display contract (`creator_profile_current` "does not
  define a multi-creator ranking… require a separate accepted display contract").
- **Build-status:** design-only. Prereq: §5.2 labels + observed per-reel metrics;
  pinned per-bucket sample floor.

---

## Out of scope for this lane

**Tier-2A audience demographics** (`gender_skew`, `age_band`) — separately
owner-gated behind a ledger-schema home (council-confirmed 2026-06-23; legal gate
cleared; still no ledger home). Referenced, **not designed** here
(`ig_creator_ideal_audience_inference_spec_v0.md`, Tier-2-A slice).

## Cross-recipe dependency map

```text
§1.1 SMA ─┐
§1.2 EMA ─┼─► §2.1 spike_score ─┐
§1.3 velocity ──────────────────┼─► §2.2 breakout_state ─┐
                                │                        ├─► §3 momentum_call
§1.3 velocity / §1.2 slope ─► §2.3 decay_or_plateau ─────┤        (allocation signal;
                                                         │         + optional call-text)
§2.2 breakout + promotion trigger ─► §2.4 active_watch_expiry
§1.4 capture_window_delta = §1.3's publication-timing-free fallback

§4 sub_niche_label      ── independent classifier lane (binds to SubNiche on dispatch)
§5.2 format_label + product_density + per-product mention_count (emphasis)
        ── independent classifier lane (orthogonal to §4); separate fields, not collapsed
        └─► §5.3 format x emphasis x observed-success rollup (within-creator, descriptive)
```

All view-based cards (§1–§3, §5.3) compute on the grid/clip current-view series
(S3.1; the reels-tab pair supersedes — settled, not a blocker); `web_profile_info`
is deep-history-only and never mixed in — a series that would mix `source_surface`
values abstains.

Build order implied: temporal (§1) → spike (§2.1) → states (§2.2–§2.4) →
momentum (§3). The two classifier lanes (§4, §5) are independent of the temporal
chain; §5.3 depends only on §5.2 + observed metrics.

## Boundaries

- Design/spec only — no implementation, live capture, lake writes, new metric
  records, scheduler, or runtime.
- Does not claim readiness, validation, buyer proof, or request-budget
  feasibility.
- Does not make Aphrodite Signals the metric authority — Silver owns the recipes;
  the registry/profile read model and Signals surface copy only accepted,
  lineage-backed fields.
- Does not edit the creator metric Silver record contract, the
  `creator_profile_current` contract, or the derived-claim provenance contract;
  cards that need a new `rollup_kind`, `payload_kind`, derivation `kind`, or a new
  visible field name a that as an **activation prerequisite** for a later
  authorized lane (S7).

## Non-claims

- not validation
- not readiness
- not buyer proof
- not implementation, capture, or lake-write authorization
- not a scheduler, crawler, or standing-watch authorization
- not a performance guarantee, causal claim, or cross-creator ranking
- not a demand claim (creator emphasis ≠ audience demand; demand needs observed response)
- not a paid/unpaid or stealth-ad verdict (`is_paid_partnership` stays candidate-only; observed `false` ≠ "not an ad")
- not person-level identity, demographics, or a follower/commenter graph
- not a calibrated confidence (support bands are uncalibrated until a labeled set exists)

## Validation (docs-only output)

Run at authoring; see the session record for observed results:

```powershell
rg -n "orca[/\\]product|orca[-]harness" forseti/product/spines/capture/core/source_families/social_media/instagram/aphrodite_proposed_creator_stats_design_spec_v0.md
python .agents/hooks/check_placement.py --strict
git diff --check
```

If any card drifts into code or lake writes, stop — that exceeds this lane's
design-only authority and needs separate implementation authorization.
