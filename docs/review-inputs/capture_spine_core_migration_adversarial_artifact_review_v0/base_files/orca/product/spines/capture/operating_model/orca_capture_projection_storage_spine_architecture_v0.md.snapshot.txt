```yaml
retrieval_header_version: 1
artifact_role: proposed target architecture (non-authorizing) — general capture→projection storage spine
scope: >
  Target architecture BACKBONE for a general Orca capture→projection storage / data-pipeline
  lane: the platform-agnostic discipline + envelope + rebuildable columnar projection that
  creator-momentum (IG-first) is the FIRST consumer of, and that org-motion/EDGAR and future
  data types may later sit beside as sibling tenants. Defines the capture-vs-projection seam,
  the storage doctrine, the rebuildable-index invariants, the deferred seams, the irreversibility
  ledger, the probe-grounding requirement, and the smallest complete next object. PROPOSED,
  pre-adoption: produced by a same-vendor 3-perspective architecture pass + home synthesis +
  a de-correlated cross-vendor review (F-01..F-07 CA-adjudicated), AWAITING owner adoption.
  Not a build-go, validation, or readiness claim.
use_when:
  - Deciding how Orca capture satellites, the rebuildable projection, and the derivation layer compose across data types.
  - Scoping the IG capture-shape contract (the next build object) or any future platform/data-type satellite.
  - Checking what is platform-agnostic core vs per-platform/per-consumer satellite, and what is deferred vs build-now.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md   # later accepted attachment-boundary target for tenant payloads
  - orca/product/spines/capture/source_families/instagram/orca_creator_momentum_pipeline_architecture_v0.md   # the IG-first instance (PROPOSED; lives on the ig-cadence-rails lane)
  - docs/decisions/wind_caller_calibration_carveout_v0.md   # capture posture / retention authority (amended 2026-06-15)
  - orca-harness/source_capture/models.py   # the packet model with the capture-shape gap
  - orca-harness/capture_spine/   # the existing satellite/projection-transform idiom to extend
stale_if:
  - The tenant/source-family payload attachment boundary changes.
  - The owner adopts, rejects, or modifies either reframe below (Reframe 1 / Reframe 2) or the capture-shape selection.
  - The IG capture-shape contract is specced + built (moves the next object from proposed to built).
  - A second real consumer (org-motion/EDGAR as a storage tenant, or TikTok/YouTube/Reddit) is authorized — tests the sibling-tenant seam.
status: PROPOSED — general capture→projection storage backbone; same-vendor 3-perspective pass + home synthesis + de-correlated cross-vendor review (F-01..F-07 CA-adjudicated) folded; AWAITING owner adoption
```

# Orca Capture→Projection Storage Spine — Target Architecture Backbone (PROPOSED, v0)

## Result

`TARGET_RECOMMENDED` — a **platform-agnostic capture→projection storage spine** whose *shared*
layer is the **discipline + envelope + rebuildable columnar projection**, with **creator-momentum
(IG-first) as the first and only built schema** and other data types (org-motion/EDGAR,
TikTok/YouTube/Reddit) as **named sibling tenants whose fit is unproven and not designed-in**. The
one decision worth making first is still the **IG capture-shape contract** (a typed value + typed
availability posture + coverage window per metric), because history cannot be re-captured and the
current packet model has no typed home for the metrics. The projection store is rebuildable
(swap-later, low lock-in) and is written as a **spec, not a runtime**, until there is captured typed
data to derive over.

This backbone carries **two reframes away from the originally-stated framing** ("one shared row-shape
with a single `metric_value` column across all data types now"), each hardened by the cross-vendor
review (see *Cross-vendor review disposition*).

## Relationship to existing docs (not a replacement)

- **Later accepted attachment boundary.** `source_capture_tenant_payload_attachment_boundary_v0.md`
  supersedes this PROPOSED backbone on tenant-payload attachment location:
  current slice-attached payload fields are transitional/incumbent, while new
  source-family payloads target packet/slice-keyed logical extension envelopes.
  This note does not change this document's projection store/cache proposal.
- This **sits beside and generalizes-by-reference** the creator-momentum pipeline architecture
  (`orca_creator_momentum_pipeline_architecture_v0.md`, PROPOSED on the `ig-cadence-rails` lane). It
  owns the **cross-data-type invariants**; that doc remains the worked IG instance. It does not
  replace it or discard its adjudicated AR-01..05 review state.
- It **extends, does not invent**, the satellite/projection-transform idiom that already ships in
  `orca-harness/capture_spine/` (`linkedin_lane/`, `linkedin_live_adapter/`, `reddit_candidate_intake/`,
  …) and the typed-posture discipline already in `orca-harness/source_capture/models.py` (`VisibleFact`).
- Placement: `docs/product/data_capture_spine/` — the established neighborhood (it already holds the
  LinkedIn influence-trajectory-watch spec and live-layer architecture, the same coarse-snapshot-series
  shape). A new top-level lane folder would need a recorded role-grammar decision; none is minted here.

## Reframe 1 — the *untyped* "one shared row-shape" is a PROJECTION view, not the CAPTURE contract

The originally-stated shape — one shared row `(entity_id, capture_time, metric_name, metric_value,
availability_posture)` with a single generic **untyped** `metric_value` column — **cannot be the
capture contract**, because:

- A single generic untyped value column **erases the typed-value-per-metric** guarantee that AR-01 names
  as the *critical, irreversible* lock-in: typing collapses into an out-of-band metric registry, which
  AR-02 already ruled makes "rebuildable" dishonest.
- Two **decoupled** value/posture columns reopen the **"absence stored as observed `0`"** fake-success
  leak that `VisibleFact` prevents today by *coupling* status→value (`known` requires a value;
  non-known forbids a value-as-truth and requires a reason).

**Resolution (recommended):**
- The **capture contract** (the packet) must preserve **a typed value per metric + a typed availability
  posture + a coverage/window boundary** — the AR-01 lock-in. What it must NOT do is collapse the value
  into a single generic *untyped* column. It is **open** whether the typed shape is bespoke-field-per-metric
  or a typed *shared* observation row (see *Capture-shape options*); both satisfy AR-01, so the choice is
  made on lower-lock-in grounds **in the IG contract**, not pre-judged here.
- The generic **long-format** row `(entity_id, entity_namespace, capture_time, observation_time,
  metric_name, metric_value, availability_posture, posture_reason, coverage_window_start/end,
  metric_unit, packet_id/slice_id)` lives **only in the derived, rebuildable projection**, where:
  - `availability_posture` is **NOT NULL**, closed-vocabulary, and **coupled to value** (value MUST be
    null when posture ≠ `observed`; value MUST be present when posture = `observed`) — the
    `VisibleFact.validate_fact` invariant ported into the projection as a hard constraint, not a
    convention;
  - the projection is **derivation-output only** (never authored directly), so the leak has no writer.

### Capture-shape options (adjudicate in the IG contract; do NOT pre-judge here)

There are **three** shapes, not two:

- **(a) Bespoke typed field per metric** — highest IG-specific proliferation; a new metric = a new
  packet field + a manifest bump = **higher lock-in**.
- **(b) A typed *shared* observation row / discriminated union** — one typed observation per (metric),
  where `metric_name` selects a **typed value variant** and the posture is coupled per observation.
  This is **shared AND typed AND lower-lock-in**: a new metric = a registry/variant entry, not a new
  field or migration.
- **(c) Generic *untyped* EAV** — **rejected for capture** (erases typing; Reframe 1).

(a) and (b) **both** satisfy AR-01 / AR-02 / the `VisibleFact` value↔posture coupling; **(b) is the
likely lower-lock-in winner** under the kernel's lower-lock-in tie-break. But the final selection — and
whether (b)'s typing is fully recoverable from the packet (vs. depending on an external registry; see
the rebuild input set) — is the **IG capture-shape contract's** job. The "one shared shape is wrong as
the capture layer" claim is specifically about the *untyped* (c); a *typed* shared shape (b) is **not**
excluded.

### Posture vocabulary is a first-class contract, not inherited wording

Today's `VisibleFact` enum is `known / unknown_with_reason / not_attempted / not_applicable`; AR-01's
posture set is `observed / unavailable_with_reason / out_of_capture_window / not_attempted`. These do
**not** map 1:1 — notably **`out_of_capture_window` has no `VisibleFact` equivalent today**, and
`not_applicable` vs `unavailable_with_reason` differ. So the IG contract must bind the **exact AR-01
posture enum** (or a declared *lossless* mapping from `VisibleFact` to it), preserving reason-required
and no-value-unless-`observed` semantics. "Rides the existing `VisibleFact` vocabulary" is insufficient
as stated, because `out_of_capture_window` and the reason taxonomy are essential to failure visibility.

## Reframe 2 — "general for all data types now" → general DISCIPLINE now; data types are sibling tenants

Generalizing one **semantic** row across creator-momentum and org-motion/EDGAR + "future data types"
**now** re-commits the exact "platform-agnostic core is premature" mistake the creator-momentum pass
already corrected (AR-04), because:

- **EDGAR is largely re-fetchable** from EDGAR, which **lowers its capture-urgency** and supports
  sibling-separation — but this is **NOT a blanket exemption from typed discipline**: if/when EDGAR
  becomes a tenant it still owes AR-02 typed canonical fields, and its own provenance is nontrivial
  (filing accession + amendments/restatements, period-boundary interpretation, extraction version). Use
  re-fetchability as a *reason to defer/separate*, not as a reason to under-capture.
- It has **different grain** (filing-event period-pairs, not a sampled curve), **different identity**
  (CIK, regulator-authoritative), and a **different legal regime** (public, no person boundary — the
  carve-out walls org-motion off as a **separate, unchanged** context).
- The repo already uses **sibling slices** (`capture_spine/` holds `linkedin_lane/`, `reddit_*/`), not
  a unified shape; the org-motion/EDGAR landing pattern is a sibling forward-capture slice.

**Resolution (recommended):** "general infra, creators first" is realized as **shared discipline +
shared store mechanics + shared packet/posture pattern**, with **creator-momentum the first and only
built schema** and EDGAR/Reddit/TikTok/YouTube as **named sibling tenants** that inherit the
*discipline*, not the *schema*. Unify a second tenant's schema **only after** its probe (below) proves
the shared columns are genuinely shared, not false friends. Starting unified is the higher-lock-in trap.

## The spine (three planes)

```
CAPTURE PLANE (satellite, per-platform / per-consumer)
  reader → SourceCapturePacket (CapturePacket) + NEW typed Observation fields (value + posture + coverage window)
     packets = SOLE source of truth (raw bytes, provenance, retention unit)
        ▼
PROJECTION PLANE (core, platform-agnostic)
  rebuildable columnar index over the long-format row; one dataset per platform; time-partitioned
     derived, NEVER a 2nd source of truth; purge = drop old partitions
        ▼
DERIVATION PLANE (core invariants; thin per-platform tails)
  pure functions over the projection: tier, momentum, org-motion delta — never stored as state;
     only an ACTED-ON decision writes back (ontology DecisionEvent)
```

The platform-agnostic/platform-specific boundary falls **at the observation row**: how you fetch and
what a metric *means* is satellite; the row, the storage, the rebuild, the purge, and the pure
derivation are core.

## Core / satellite boundary

- **Core (general, this lane owns):** the shared **envelope** (`entity_id` + `entity_namespace`,
  `capture_time` / `observation_time`, coverage window, the typed value↔posture coupling discipline);
  the **rebuildable columnar projection mechanics** (dataset-per-platform, time-partitioned,
  drop-partition purge); the **rebuild + corruption-detection** path; the **pure-derivation rule**
  (tier/promotion/momentum/delta computed, never stored).
- **Satellite (per-platform / per-consumer):** the reader/fetcher; the **typed metric schema + the
  per-platform closed `metric_name` vocabulary + the per-platform `posture_reason` vocabulary**; the
  **identity regime** (IG numeric id, EDGAR CIK); platform-shaped **derivation tails** (velocity
  normalization, EDGAR period-alignment) as named plugin points, not core switches.
- **Interface:** one-way, narrow — satellite → (packet + typed observation) → core. The only write-back
  to durable state is an acted-on decision → ontology `DecisionEvent` (adapter, not hard type-bind;
  the ontology is AWAITING_DISPATCH / HIGH lock-in).

## Storage doctrine + the server trigger

- **Required storage properties (specify now — these ARE the contract):** columnar; **one dataset per
  platform**; **time-partitioned by `capture_time`** (coarse — month/quarter) so purge = **drop old
  partition files**; single-writer-tolerant; rebuildable from the input set. **The concrete engine /
  runtime (e.g. SQLite vs Parquet+DuckDB vs other) is DEFERRED** — pick the engine when there is captured
  data to derive over. "Columnar, partitioned" is a *property* requirement, not an engine selection.
- Be honest that "single file / no server" is really **a partitioned dataset + compaction +
  single-writer + a corruption→rebuild path** — no server, but not *no ops*: Parquet is immutable
  (incremental writes ⇒ many small files ⇒ compaction); single-file DuckDB is single-writer (active and
  passive capture must not write concurrently — which tightens nicely against the no-concurrent-crawler
  posture); a crash mid-write is recoverable **only if** the rebuild path is built and a corrupt index
  is detectable, not asserted.
- **Volume must be re-derived, not assumed.** The prior "≈ sub-million rows over 10yr" justification is
  void: the carve-out (amended 2026-06-15) makes the **subject roster uncapped** ("all creators within
  the vertical"), and passive monitoring runs "faster than human." Total rows = roster × posts-tracked ×
  metrics × recheck-cadence × retention. Ingest is still bounded by ≤10 operating accounts (start ≤5),
  but **recheck-cadence and post-fanout are now load-bearing parameters** that must be recorded, and the
  bound is roster-sensitive. The columnar-single-file choice likely still holds (throughput-bounded), but
  the server trigger could fire earlier than the old estimate implied.
- **Server trigger (name it, don't vibe it):** trip ANY of — concurrent writers to one platform dataset ·
  the carve-out's own commercial-scale trigger (licensed/bought-data posture) · live cross-platform joins
  on a hot path · multi-reader transactional consistency. Until one trips, a server is over-engineering.

## Rebuildable-index invariants (all later work must preserve)

0. **The rebuild INPUT SET is `packets + the versioned metric registry + the versioned identity/conflict
   policy`** — not packets alone. `rebuild(packets, registry@v, id_conflict_policy@v) → projection` is
   deterministic and total; deleting and rebuilding the projection reproduces it. **Each packet must pin
   the registry + policy versions** that apply to it, so the rebuild is reproducible. These named
   versioned inputs are the *only* permitted non-packet rebuild dependencies (see inv. 6).
1. Rebuild reads the **typed observation fields**, not a reparse of raw bytes (AR-02). Raw bytes +
   parser version are audit/provenance only.
2. Tier / promotion / momentum / org-motion-delta are **never stored** in the projection (storing a tier
   is the canonical violation).
3. The **identity + conflict policy is versioned** (numeric id is the stable key; username is mutable;
   `re_capture_relationship: conflict` is a real value). An unversioned policy makes "rebuildable"
   dishonest.
4. Posture survives rebuild — a rebuilt projection still distinguishes "not captured" from "observed 0".
5. The projection introduces **no information that is not derivable from the rebuild input set** (packets
   + the named versioned registry/policy). It is not a second source of truth and enriches in nothing
   else — `metric_unit` and per-metric typing come from the *versioned registry*, which is an explicit,
   pinned rebuild input, **not** "information absent from packets" smuggled in at projection time.

## Deferred seams (named, NOT built)

- **Cross-platform identity stitching** — Tier-2 deferred in the carve-out (separate dated authorization +
  legal gate). `entity_namespace` is the seam (keeps platform id-spaces disjoint); do not build the
  mapping.
- **Velocity / momentum normalization across platforms** — platform-shaped; `metric_unit` is the seam;
  a derivation-plane plugin, deferred.
- **Org-motion / EDGAR as a storage tenant** — the spine must *fit* it structurally (entity=CIK,
  metric=headcount, observation_time=period_end, coverage=filing period) but the EDGAR satellite + its
  period-pair derivation are a **separate consumer lane**, not built here, and its capture authority /
  person-boundary posture stay entirely in their own context (the carve-out keeps org-motion separate
  and unchanged). The backbone must not become a backdoor importing creator-momentum's posture into
  org-motion. If EDGAR becomes a tenant it still owes typed canonical fields + its own provenance
  (accession, amendments, period boundaries, extraction version) — re-fetchability is not an exemption.
- **Server / warehouse** — owner-decided commercial-scale only; not in this backbone.
- **Multi-platform beyond IG** — name the seam, build IG only.

## Irreversibility ledger

| Decision | Reversibility | Implication |
|---|---|---|
| Typed value + posture per metric on the packet | **One-way door** (history un-re-capturable) | Get right now |
| Coverage / window boundary on capture | **One-way door** | Get right now |
| The exact posture enum / lossless `VisibleFact`→AR-01 mapping | **One-way door** (mis-encoded posture = lost failure visibility) | Bind in the IG contract |
| v0 identity + conflict policy | One-way-ish (versions forward; no-policy data can't be retro-disambiguated) | Lock a v0 before first capture |
| Capture shape (a) per-metric vs (b) typed-shared vs (c) untyped-EAV | Partially reversible (shape can migrate; captured rows can't be retro-typed) | Adjudicate in the IG contract (favor lowest lock-in) |
| Shared *cross-platform* shape | Partially reversible (adding columns cheap; wrong-merge expensive) | Defer to probe |
| Store **required properties** (columnar, partitioned, rebuildable) | Conceptual contract | **Specify now** |
| Store **engine / runtime** (SQLite/Parquet/DuckDB/…) | **Fully reversible** (rebuildable from inputs) | **Defer; pick nothing now** |
| Tier / promotion / velocity derivations | **Fully reversible** (pure functions) | Storing them is the violation |
| Org-motion unified vs sibling | Reversible toward unify | Start sibling (low lock-in) |

## Probe-grounding requirement (the cheap de-risker)

Before any **cross-platform shared shape** is locked, a thin **read-only** probe across
IG / TikTok / YouTube / Reddit + one EDGAR sample must confirm, per data source:

1. **absence is distinguishable from 0** — the posture is *observable* (private / blocked / rate-limited /
   metric-hidden / filing-gap), not assumed;
2. a **stable non-handle identity key** exists (IG numeric id, EDGAR CIK);
3. the **coverage window** is expressible per capture (so a gap reads as a gap);
4. the candidate shared columns **genuinely overlap** and are not false friends (IG per-post `view_count`
   vs EDGAR `numberOfEmployees` are NOT one metric; IG `followers` vs Reddit `karma` are NOT one base).

**The probe is a governance-bounded read plan, not just a data-shape check (per-source):** it runs
**active/attended, human-initiated, time-bounded and self-terminating** — never a perpetual or scheduled
crawler — and stays a one-shot read, not passive monitoring. The account-cap rules (≤10 / start ≤5 Orca
operating accounts) apply to the **social** sources (IG/TikTok/YouTube/Reddit); **EDGAR is read under its
own separate, public, non-person posture** (no creator-account rules, no person boundary) — it must not
inherit the creator carve-out. Each source states its method, time bound, and active/passive posture
before the probe runs.

Until the probe confirms 1–4, lock only the **IG** typed-metric capture shape; leave the cross-platform
shared shape **named-but-unlocked**.

## Smallest complete next object

A thin **IG capture-shape contract spec**: a typed value + typed availability posture + coverage window
**per metric** — selecting among shapes (a)/(b)/(c) on lower-lock-in grounds (favor the typed-shared
shape (b) unless the IG contract shows it can't preserve packet-recoverable typing) — and **binding the
exact AR-01 posture enum** (or a declared lossless `VisibleFact` mapping). Plus a **v0 identity/conflict
policy** and the **registry/policy version-pinning** that makes rebuild reproducible. The store, the
cross-platform unification, the velocity layer, and the server are all **named-deferred**. Touch point:
`orca-harness/source_capture/models.py` (`SourceCaptureSlice`).

⚠️ The actual field-add to `models.py` is **runtime work on a `StrictModel` contract + a breaking
manifest bump** (`source_capture_packet_manifest_v1` → v2) under the adopted schema-evolution discipline.
It requires **separate explicit bounded authorization** and is **not** part of this planning doc.

## What would change the recommendation

- Owner overrules Reframe 2 and wants true semantic unification across data types now (accepting the
  higher lock-in).
- The IG contract finds the typed-shared shape (b) cannot preserve packet-recoverable typing without an
  external registry — then capture shape (a) or a packet-carried registry version is required.
- The probe shows a platform cannot express posture / identity / coverage — then the shared *envelope*
  itself needs rework, not just the per-platform schema.
- Capture cadence / uncapped roster pushes volume past columnar-single-file — the server trigger fires
  earlier.

## Cross-vendor review disposition

Hardened by a de-correlated **cross-vendor** (non-Anthropic) `no_repo` advisory review (discovery bar
satisfied), CA-adjudicated:
- **F-01 (critical, capture-shape false dichotomy) ACCEPTED** → the three-way capture-shape adjudication
  (per-metric / typed-shared / untyped-EAV) is now explicit and deferred to the IG contract; "typed
  per-metric fields" is no longer asserted as the only valid capture contract.
- **F-03 (major, posture vocabulary) ACCEPTED** → the exact AR-01 posture enum (or a lossless
  `VisibleFact` mapping) must be bound; "ride VisibleFact" alone is insufficient.
- **F-04 (major, rebuild inputs) ACCEPTED** → the rebuild input set is `packets + versioned registry +
  versioned id/conflict policy`, version-pinned per packet; invariant on "no info absent from packets"
  reworded accordingly.
- **F-05 (major, probe governance) ACCEPTED** → the probe is now a governance-bounded read plan with
  EDGAR read under its own non-person posture.
- **F-06 (major, EDGAR re-fetchability) ACCEPTED** → re-fetchability lowers urgency / supports separation
  but is not a blanket exemption from typed discipline.
- **F-02 (major, source-verification) ACCEPTED (partial)** → a source-read ledger is added below;
  genuinely-observed facts are kept as observed (not downgraded), with authoring-verified vs
  reviewer-visible made explicit.
- **F-07 (minor, store wording) ACCEPTED** → "required properties (now)" separated from "engine/runtime
  (deferred)."

This was an advisory cross-vendor review, CA-adjudicated — **advisory input, not a formal verdict or
owner adoption.** `authored_by: claude-opus-4-8`; `reviewed_by: <cross-vendor model — operator-recorded>`.

## Verified vs proposed vs not-proven (honesty) + source-read ledger

- **Observed this session in the authoring environment (primary source; re-confirmable via the ledger
  below).** These are real observations, not premises — but they were verified in the repo, not provided
  to the no_repo reviewer, so to that reviewer they read as `unverifiable from provided sources`.

  | Claim | Source (path @ revision) | Observed |
  |---|---|---|
  | carve-out 2026-06-15 amendment | `docs/decisions/wind_caller_calibration_carveout_v0.md` (ig-cadence-rails worktree; **working-tree amended**, committed blob `d0334361…`) | ≤10 our operating accounts / start ≤5; uncapped subject roster; active=attended, passive=bounded self-terminating; faster-than-human-not-takedown-risking; 10yr retention UNCHANGED |
  | `capture_spine/` sibling idiom exists | `orca-harness/capture_spine/` (origin/main `e0b939a2`) | `linkedin_lane/`, `linkedin_live_adapter/`, `reddit_candidate_intake/`, `linkedin_graph_frontier/`, `reddit_graph_frontier/` |
  | packet model has no typed metric field | `orca-harness/source_capture/models.py` (ig-cadence-rails `c365dca2`) | `SOURCE_CAPTURE_MANIFEST_VERSION="source_capture_packet_manifest_v1"`; `VisibleFact{known,unknown_with_reason,not_attempted,not_applicable}`; `SourceCaptureSlice` carries no metric field |
  | creator-momentum arch doc PROPOSED, AR-01..05 folded | `…/orca_creator_momentum_pipeline_architecture_v0.md` (blob `ff24252e…`, ig-cadence-rails `c365dca2`) | status PROPOSED; AR-01..05 adjudicated |
  | `data_capture_spine/` holds the LinkedIn analogs | `docs/product/data_capture_spine/` (origin/main `e0b939a2`) | `…linkedin_influence_trajectory_watch_spec_v0.md`, `…linkedin_live_layer_architecture_v0.md` |

- **Proposed (this backbone):** the spine, the two reframes, the capture-shape options, the core/satellite
  split, the storage doctrine + server trigger, the invariants + rebuild input set, the deferred seams,
  the probe plan, the smallest next object.
- **Not proven:** everything is feasibility-level, not at-scale-validated. The exact adopted-status of the
  schema-evolution doctrine (the `manifest_v1→v2` bump rule) is a **pointer to confirm in the building
  lane**, not asserted here.

## Non-claims

PROPOSED target-architecture backbone only — not a build-go, validation, readiness, acceptance, or
commercial/legal authorization. It has had a same-vendor 3-perspective architecture pass + home synthesis
+ a de-correlated cross-vendor advisory review (F-01..F-07 CA-adjudicated) and is **AWAITING owner
adoption** — advisory input, not a formal verdict. Ontology names are forward references to a
not-yet-dispatched ontology. The `models.py` field-add it names is separately-authorized runtime work,
not authorized by this doc.
