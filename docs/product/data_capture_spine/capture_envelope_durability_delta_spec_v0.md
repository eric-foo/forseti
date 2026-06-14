# Capture Envelope Durability Delta Spec v0

```yaml
retrieval_header_version: 1
artifact_role: Product-method spec (delta on the Capture Envelope of record)
scope: >
  Extension/delta spec for demand-durability proxy capture. Specifies ONLY the
  capture facts the existing Capture Envelope of record does not yet name as
  first-class, plus the cross-cutting temporal-regime / cold-start doctrine the
  four proxy specs (price, availability, search-interest, review) will consume.
  It does not re-derive, replace, or fork the envelope of record.
use_when:
  - Specifying a demand-durability proxy capture (price, availability, search-interest, review) that observes a source repeatedly over time.
  - Checking how durability-over-time capture facts (pinning, cold-start, series-diff, cadence) sit on top of the existing Source Capture packet schema and obligation contract.
  - Consuming the three temporal regimes or the cold-start inherent-limit cap from a downstream proxy spec.
authority_boundary: retrieval_only
open_next:
  - orca-harness/source_capture/models.py                                              # Capture Envelope of record (schema)
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md  # Capture Envelope of record (obligations)
  - docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md # RQ-01..05 source-observability status
  - orca-harness/source_capture/cadence.py                                             # CadencePlan planning primitive
stale_if:
  - The Source Capture packet schema (orca-harness/source_capture/models.py) changes PacketTiming, the closed posture vocabularies, hash_basis, or re_capture_relationship in a way that overlaps these delta facts.
  - The Data Capture obligation contract is amended in a way that already names one of the five new elements below.
  - An owner decision adopts, narrows, or rejects any of the five new elements, or amends the temporal-regime / cold-start doctrine.
  - A proxy spec (price, availability, search-interest, review) supersedes the temporal-regime / cold-start section with its own owner-accepted version.
```

- Status: `DELTA_SPEC_DRAFT_V0`
- Artifact type: Product-method spec (delta), not a fresh keystone and not a second envelope authority
- Implementation authorized: no
- Feature planning authorized: no
- Runtime / source-system design authorized: no
- Contract hardening authorized: no (owner-gated, out of scope)

## What This Is (And Is Not)

This is an **extension/delta note on the Capture Envelope of record**, not a new
Capture Envelope. It exists because demand-durability proxies (price,
availability, search-interest, review) are captured as a **series over time**,
and that durability-over-time reading needs a small set of capture facts named
as first-class that the envelope of record today carries only generically.

It is **design + spec only**. It builds nothing, runs nothing, deploys nothing,
hardens no contract, and does not edit `models.py` or the obligation contract.
It is a new doc that **cites** them.

It does not define Evidence Candidate Record (ECR) fields, Cleaning
transformations, or Judgment rules. It does not weight, score, rank, or judge
any captured fact (see INV-1 below). It captures durability-over-time as
**observed facts and their limits**; whether a series shows durable versus
hollow demand is a downstream Judgment call, not a capture output.

## Envelope Of Record (Cited, Not Re-Derived)

The Capture Envelope of record ALREADY EXISTS. This delta consumes it as-is and
does not re-spec, re-mint, or fork it. The envelope of record is:

1. **The shipped Source Capture packet schema** —
   `orca-harness/source_capture/models.py`. It already provides:
   - `SourceCapturePacket` (the packet), `SourceCaptureSlice` (per-slice
     facts), `PacketTiming`, `PreservedFile`, `ReceiptMetadata`;
   - timestamp / timing decomposition via `PacketTiming`:
     `source_publication_or_event`, `source_edit_or_version`, `capture_time`,
     `archive_snapshot_time` (optional, archive-mode; distinct from
     `capture_time` — the access/fetch time is never repurposed),
     `recapture_time`, `cutoff_posture`;
   - locator and capture method/mode via `source_locator`, `capture_mode`
     (`CaptureModeCategory`), `capture_context`, `visible_mode_changes`;
   - retained raw payload + content hash via `preserved_files`
     (`PreservedFile.sha256` + `hash_basis`, the AR-04 recomputation-bound
     closed token, currently `raw_stored_bytes`);
   - per-capture recapture relationship via `re_capture_relationship` (closed
     vocabulary `supersede | supplement | conflict | mixed`, Ob.15,
     write-time-enforced);
   - the closed access / archive / media posture vocabularies via
     `access_posture` (open per Ob.11), `archive_history_posture` (closed
     `archived | attempt_failed`, Ob.10), `media_modality_posture`,
     `cutoff_posture` (closed `pre_cutoff | post_cutoff | mixed | unknown`,
     Ob.9), all carried as `VisibleFact` so `unknown_with_reason /
     not_attempted / not_applicable` ride on status (AR-05);
   - `limitations` and `warning_notes` at packet and slice level.

2. **The obligation contract** —
   `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md`.
   Load-bearing for this delta: Ob.3 (capture-event provenance), Ob.4 (capture
   mode disclosure), Ob.6 (raw observable fidelity + frame-keyed fidelity
   context), Ob.8 (decomposed timing), Ob.9 (cutoff posture), Ob.10
   (archive/history posture), Ob.11 (source visibility and access limits), and
   Ob.15 (re-capture semantics). The contract's discharge vocabulary (`met`,
   `partial`, `assessed_not_met`, `cannot_assess`, `access_failed`, `blocked`,
   `unavailable_by_source`, `not_applicable`, `not_attempted`) is reused as-is;
   this delta mints no new discharge states.

3. **The source-observability requirements status** —
   `docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md`
   (RQ-01 verbatim/source-structure: carry_forward_modified; RQ-02 archive body
   retrieval: modify_split, availability/retrieval-state visibility now;
   RQ-03 media/multimodal: carry_forward_modified, modality-triggered; RQ-04
   in-bound public-host access: deferred candidate; RQ-05 source-language
   anchors from the start: carry_forward). This delta consumes that boundary; it
   does not re-classify any RQ.

**Already covered — do NOT re-spec here:** envelope basics (capture timestamp,
locator, capture method/mode, retained raw payload, content hash, per-capture
recapture relationship, the access/archive/media/cutoff posture vocabularies,
limitations) are fully owned by (1) and (2) above. Anything in this delta that
appears to restate one of those is a citation, not a new authority.

**Conflict rule:** if this delta ever appears to conflict with the schema or the
obligation contract, the envelope of record wins. Treat this delta as stale and
open the controlling source.

## The Whole Job: Five New Elements

This delta specs ONLY the five elements below. Each is a capture FACT or a
capture DOCTRINE — never a weight, score, threshold, or judgment.

### Element 1 — First-Class Pinning Facts (logged-out / locale / currency / variant)

**Problem the envelope of record leaves open.** Today the conditions under which
a source observation was taken — whether the operator/agent was logged out, what
locale and currency the surface rendered, which product variant was on screen —
are capturable only *generically*, folded into `capture_context` (free-form
`VisibleFact`) or `SourceCaptureSlice.warning_notes`. For a one-shot capture
that is enough. For a **durability series** it is not: a price series silently
mixing GBP and USD, a locale that flips a product in/out of stock, or a variant
swap (50ml vs 100ml) makes two observations non-comparable, and the comparison
break is invisible if the pinning condition is buried in prose.

**Spec (capture fact only).** A demand-durability proxy capture must record the
following as **named, first-class capture facts** per observation (per slice,
since a series observation maps to a `SourceCaptureSlice`), each carried as a
`VisibleFact` so unknown/not-attempted/not-applicable ride on status:

- `session_visibility_pin` — the visibility/auth condition under which the
  surface was observed (e.g. logged-out / anonymous, account-created,
  entitled-session). This is *what condition produced this observation*, kept
  distinct from `access_posture` (which records visibility/access *limits*) and
  from `session_identity` (which distinguishes sessions for provenance, Ob.3).
- `locale_pin` — the locale/region/language context the surface rendered in
  (e.g. `en-GB`, `US`), when locale changes what is shown.
- `currency_pin` — the currency the surface presented values in, when the proxy
  observes priced or monetary surfaces.
- `variant_pin` — the specific product/offer/page variant observed (size, SKU,
  pack, edition, plan tier), when a source exposes multiple variants and the
  series must hold one fixed.

These are **capture facts that fix comparability across a series**. They are not
normalization (Cleaning's job), not currency conversion, and not a decision
about which variant matters (Judgment's job). When a pin is unknown or the source
does not expose it, the capture records the pin's **fact status** as a valid
`VisibleFactStatus` — `unknown_with_reason` (or `not_applicable` where the pin
cannot apply), with a reason — and, where the source's non-exposure discharges
the pin's *capture obligation*, records that separately as the
obligation-discharge state `unavailable_by_source`. `unavailable_by_source` is
an obligation-discharge state, **not** a `VisibleFactStatus`, and is never
written as a fact's status. Silent omission is not allowed (obligation-contract
rule, reused).

**Relationship to the envelope of record.** This narrows, for durability
proxies, what today lives generically inside `capture_context`. It does not
replace `capture_context`; it names the four pins that recur across all four
proxies so a downstream reader can see a comparability break without parsing
prose. Whether these pins eventually become schema fields is a contract-hardening
decision and is **out of scope** (owner-gated).

### Element 2 — Per-Series Cold-Start Marker

**Problem.** A capture *series* (the ordered set of observations of one source
for one decision) has a beginning. Before that beginning the source was
**uncovered**: Orca recorded nothing. The envelope of record marks per-capture
timing (`capture_time`, `recapture_time`) and per-capture re-capture
relationship, but it does not mark the **series' own origin** — the fact that
history before the first observation is absent by construction, not merely
unobserved-this-run.

**Spec (capture fact only).** A demand-durability proxy series must carry a
**per-series cold-start marker** on its first observation, recording:

- `series_id` — the identifier that binds the observations into one series
  (which source surface, for which decision/proxy). This is the join key the
  series-diff (Element 3) operates over.
- `cold_start_at` — the series origin: the timing at/after which coverage
  begins (normally the first `capture_time`), carried as a `VisibleFact`.
- `pre_coverage_history_posture` — a marker that history before `cold_start_at`
  is **uncovered by construction**, with the reason (e.g. "series began at first
  commissioned capture; no prior Orca observation exists"). Where an archive or
  back-historical source *could* extend coverage earlier, that is recorded as a
  visible limitation and routed to the archive/history posture (Ob.10) and the
  temporal-regime classification (Element 5) — it does not erase the cold-start
  marker.

**Why a marker, not just a missing first row.** The marker makes the absence
*visible and inspectable* rather than inferable from "the data starts here." It
is the capture-side anchor that the cold-start inherent-limit cap (Element 5)
points at: downstream layers must be able to see that a series cannot speak to
the window before its cold start, and why.

This is a capture fact about coverage extent. It is **not** a statement that the
pre-coverage demand was high, low, durable, or hollow — that would be judgment
over data Orca does not have.

### Element 3 — Series-Level Recapture-Diff (tamper / deletion detection across a series)

**Problem — and the distinction that makes this NEW.** The envelope of record's
`re_capture_relationship` (Ob.15, closed `supersede | supplement | conflict |
mixed`) is a **per-capture** fact: it relates *this* capture to *the immediately
prior* capture of the same locator. It answers "does this new capture supersede,
supplement, or conflict with the one before it?" It does **not** describe the
**series as a whole**, and it is not designed to surface *tamper or deletion*
patterns that only become visible across many observations (e.g. a value that
was present in observations 1–8, silently edited at 9, and the edit back-dated;
or a review/thread that existed early in the series and was deleted later).

**Spec (capture fact / observed-pattern only).** A demand-durability proxy
series may carry a **series-level recapture-diff** record, distinct from and
additive to the per-capture `re_capture_relationship`. It records, across the
ordered observations of one `series_id`, the **observed source-state changes**:

- `series_diff_id` and the `series_id` it summarizes;
- the ordered observation references it spans (by slice/observation id);
- **observed change events**, each naming: which observation introduced the
  change, what source-visible state changed (value changed, item appeared, item
  disappeared/deleted, item edited, timestamp/back-date shift, locator
  migrated), and the evidence anchor (content-hash difference via the existing
  `PreservedFile.sha256`, or a source-visible edit/deletion marker). Content
  hashes are the existing envelope facility; the series-diff *reads* them across
  observations, it does not introduce a new hashing scheme.
- `tamper_deletion_visibility` — a **visible-limitation** field stating whether
  deletion/edit/back-date was *source-visibly* marked, *inferred from hash/value
  divergence only*, or *cannot be assessed* (reusing the obligation contract's
  `cannot_assess` sense). It records what the series can and cannot show.

**Hard boundary.** The series-diff records **observed differences and their
evidentiary basis**. It does **not** decide whether a change is malicious,
manufactured, astroturfed, or distortion — that integrity *judgment* is Judgment
Spine's (Signal Integrity), per the obligation contract's forbidden outputs
("integrity classifications," "discounting decisions"). The diff makes
tamper/deletion *detectable and inspectable*; it never labels intent. It is the
capture-side substrate the integrity layer consumes, not the integrity verdict.

The per-capture `re_capture_relationship` stays exactly as the schema defines it.
The series-diff is a separate, series-scoped record that *aggregates the observed
state changes*; the two never overwrite each other (consistent with Ob.15's
"re-capture does not erase prior capture history").

### Element 4 — Scheduling / Cadence Model As Capture Doctrine

**Problem.** A durability series is only as trustworthy as the **cadence** of its
observations: irregular, gappy, or undisclosed sampling makes a series-diff and a
durability read fragile, and an undisclosed gap can masquerade as "no change."
The envelope of record does not carry the series' intended sampling cadence as a
capture fact.

**Existing primitive — reference, do not re-invent.**
`orca-harness/source_capture/cadence.py` already provides a **planning
primitive**: `CadencePlan` with modes `fixed` and `bounded_jitter`,
`build_cadence_plan(...)`, planned offsets/waits, and a `to_dict()` projection.
This delta **references** it and does not re-invent scheduling math, a scheduler,
or a runtime.

**Spec (capture doctrine + capture fact).** A demand-durability proxy series
should:

- declare its **intended cadence** for the series, using the existing
  `CadencePlan` shape (`mode`, `slot_count`, planned offsets/waits) as the
  vocabulary — recorded as a capture fact on the series, not invented anew;
- record the **realized cadence**: the actual observation timings (already
  available via per-observation `capture_time` / `recapture_time`), so realized
  versus intended can be compared;
- record **cadence deviations and gaps** as visible limitations: a skipped slot,
  a long gap, a failed observation (discharged with the obligation contract's
  `access_failed` / `not_attempted` vocabulary), so a downstream reader sees
  where the series is thin or interrupted.

This is **capture doctrine** (how a durability series should sample and disclose
its sampling), expressed in the existing cadence vocabulary. It is **not** a
build authorization for a scheduler, monitor, cron, queue, or any runtime. It
does not authorize standing/opportunistic capture (the obligation contract still
requires commissioned capture tied to a Decision Frame). Cadence is disclosed so
gaps are honest; cadence is not a quality score.

### Element 5 — Cross-Cutting Doctrine: The Three Temporal Regimes + Cold-Start As Inherent-Limit Cap

This is the **most valuable output of this delta** and is written to be
**self-contained**: the four proxy specs (price, availability, search-interest,
review) cite this section directly.

#### The three temporal regimes

Every demand-durability proxy source falls into one of three **temporal
regimes**, defined by *what history the source itself makes available at capture
time*. The regime is a **capture-time classification of the source**, not a
judgment about the demand:

1. **Retroactive-native.** The source natively exposes its own history; a single
   capture (or an archive capture) can recover a back-run of prior states. The
   series can reach *backward* past its cold start because the **source**, not
   Orca's prior observation, carries the history. *Capture obligation:* record
   how far back the native/archive history reaches and its fidelity; the
   cold-start marker still applies to *Orca's own* coverage, but
   `pre_coverage_history_posture` may be partly satisfied by retroactive-native
   history (recorded as such, with the source as the basis).

2. **Forward-only.** The source exposes only its *current* state; history exists
   only as the series Orca itself accumulates from cold start forward. There is
   **no way to recover** pre-cold-start states later — they were never recorded
   and the source does not retain them. *Capture obligation:* the cold-start
   marker is load-bearing here; the series can speak only to the window from
   `cold_start_at` forward, and that limit is permanent for the pre-coverage
   window.

3. **Event-based.** The source emits discrete events/changes (e.g. a pricing
   event, a restock, a launch, a discrete review posting) rather than a
   continuously sampled state. History is the set of *observed events*; coverage
   between events is interpolated only as "no observed event," never as "no
   change occurred." *Capture obligation:* record events as observed, and record
   the gap semantics (un-observed interval ≠ no-change) as a visible limitation;
   cadence (Element 4) governs how confidently absence-of-event can be stated.

A single proxy or even a single series may touch more than one regime across its
slices/locators (e.g. a live forward-only surface plus a retroactive-native
archive of the same source). When regimes coexist, the capture records the
regime **per relevant source slice/locator** (the same per-slice discipline
Ob.10/Ob.15 already use), and marks the series `mixed` rather than forcing one
global regime label.

#### Cold-start is an inherent-limit cap, not a clearable risk

The pre-cold-start window is **uncovered by construction**. Capture cannot
retroactively manufacture history it never recorded, and — for **forward-only**
and (between events) **event-based** regimes — no later capture, archive attempt,
or tooling can fill it, because the source itself never retained it.

Therefore the cold-start gap is an **INHERENT-LIMIT cap**: a permanent ceiling on
what the series can claim about the pre-coverage window, **not** a clearable risk
that diligence, more captures, or better tooling will close. The only regime in
which the pre-cold-start window can be (partly) recovered is
**retroactive-native**, and only to the extent the *source's own* history
reaches — recorded explicitly, with the source as the basis, never asserted.

This distinction is load-bearing for downstream consumers: a clearable risk
invites "capture more and the gap closes"; an inherent-limit cap tells Judgment
the ceiling is fixed and must be respected in the action ceiling. Capture's job
is to make the cap **visible and correctly classified** (which regime, how far
back coverage reaches, why earlier is unrecoverable). Capture does **not** decide
whether the cap is acceptable for a given decision — that is Judgment's call.

#### What downstream proxy specs consume from this section

- the three-regime classification (per slice/locator; `mixed` when they coexist);
- the cold-start marker (Element 2) as the anchor of the cap;
- the rule that cold-start is an inherent-limit cap except for retroactive-native
  recovery bounded by the source's own history;
- the cadence model (Element 4) for stating event-based gap/absence semantics
  honestly.

These are capture-side facts and doctrine. They name **what is captured and what
is inherently uncoverable**. They assign no weight, no score, and no durability
verdict.

## INV-1 Preservation (No Scoring / Weighting / Ranking / Judgment)

This delta is bound by INV-1 (the Demand-Substrate no-scoring invariant, per
`docs/product/product_lead/orca_buyer_proof_packet_v0.md` and the demand-read
taxonomy). Concretely, in this spec:

- every new element describes **what is captured** (a fact) or **how capture
  should sample/classify** (doctrine) — never how to weight, score, rank,
  combine, or judge it;
- no formula, threshold, weight, or numeric scoring rule appears;
- the series-diff detects observed change; it does **not** classify
  tamper/astroturf/distortion (Signal Integrity is Judgment's);
- the temporal regimes and cold-start cap classify *coverage*, not *demand
  durability*; "durable versus hollow" is a downstream Judgment read;
- costly-behavior semantics, the Demand-Substrate Hard Gate, and the posture
  vocabularies are **consumed as defined elsewhere**, not redefined here.

## Boundaries And Non-Goals

- **No second envelope.** The envelope of record (`models.py` + obligation
  contract) is the sole Capture Envelope authority. This delta cites it.
- **No edits to `models.py` or the obligation contract.** This is a new doc.
  Whether any of the five elements becomes a schema field or contract obligation
  is **contract hardening**, which is owner-gated and out of scope.
- **No build / scrape / run / deploy.** No scheduler, monitor, runner, scraper,
  API, storage, dashboard, or runtime is specified or authorized. `CadencePlan`
  is referenced as an existing planning primitive only.
- **No ECR / Cleaning / Judgment design.** No ECR fields, keys, schemas,
  Cleaning transformations, normalization rules, currency conversion, or
  Judgment/scoring logic.
- **Out of scope and untouched:** distribution / org-motion proxies and
  repurchase proxies (deferred). This delta does not mention, design, or imply
  them beyond this exclusion.
- **Commissioned capture only.** The obligation contract's commissioning gate
  (Ob.1) still binds; durability series are commissioned against a Decision
  Frame, not standing/opportunistic collection.

## Non-Claims

This spec is not validation, readiness, acceptance, pressure-test discharge,
Data Capture Spine acceptance, contract hardening, source-of-truth promotion,
buyer proof, judgment-quality evidence, implementation authorization, runtime
authorization, tooling authorization, scheduler/monitor authorization,
source-access boundary amendment, obligation-contract amendment, schema change,
ECR design, Cleaning implementation, Judgment design, or commercial-readiness
evidence. It is a design+spec delta that cites the existing Capture Envelope of
record and names the durability-over-time capture facts and doctrine the four
demand-durability proxy specs will consume next.
