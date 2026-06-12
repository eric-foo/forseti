# Company-Aggregate Forward-Signal — Capture-Lane Sibling-Slice Scope Decision (v0)

```yaml
retrieval_header_version: 1
artifact_role: Decision record
scope: >
  Capture-lane ownership + scope decision for the source-agnostic company
  headcount-aggregate forward-trend signal (org-motion net-adds realization) —
  the sibling slice routed by the owner-locked architecture decision
  (company_aggregate_forward_signal_architecture_decision_v0.md). Fixes the
  entity-keyed time-series record shape, the official-first source-selection
  policy, the official adapter set and the separate source-access authorizations
  each one still needs, the attended-fallback cadence posture, and the LinkedIn
  extraction adapter's home (consume, not absorb). Surfaces the standing-capture
  obligation-home gap. Scope/ownership only; NOT a build authorization, NOT a
  source-access authorization, NOT owner-locked.
use_when:
  - Building or reviewing the company-aggregate forward-signal slice in the capture lane.
  - Deciding the source for a company headcount-aggregate trend under official-first.
  - Checking what the capture lane has and has not committed for this slice.
authority_boundary: retrieval_only
branch_or_commit: ecr-sp3-timing-deriver-slice1 (working tree dirty — shared/volatile; uncommitted)
stale_if:
  - The owner changes the official-first policy, the core/satellite split, or the posture recommendation in the parent architecture decision.
  - The owner re-assigns the LinkedIn extraction adapter's home (consume -> absorb), which would re-assign an owner-locked core/satellite boundary.
  - A standing / corpus-capture obligation contract is accepted, giving this slice its obligation home.
  - A build authorization or a per-adapter source-access authorization supersedes this scope-only decision.
  - The capture-lane obligation contract is amended to cover standing / forward time-series capture.
```

## Status

`CAPTURE_LANE_SCOPE_DECISION_v0` (2026-06-12, in-thread). Lane-owned scope.
**Owner-authorized to build (2026-06-12):** the slice build (#3) and the SEC
EDGAR source-access adapter (#2) are owner-authorized; the standing-capture
obligation home is clarified in the dated section below (discharging prerequisite
#1). Cadence is **manual-now**, the periodic scheduler deferred. Remaining
deferrals: the Companies House adapter, the commercial LinkedIn-provider adapter,
and any periodic-scheduler policy. Not validated, not readiness, not
source-of-truth promotion. A lane-scope label, not an evidence-ladder claim tier.

This record answers the cross-lane handoff from the LinkedIn / org-motion
discovery lane under the owner-locked parent decision. It does not edit the
parent. The build and EDGAR source-access authorizations were granted by the
owner in-thread (2026-06-12); this record **documents** that scope and is not
itself the authorizing instrument.

### Build + code-review status (2026-06-12)

The revised three-record architecture below is **BUILT and green**, superseding its
earlier `PROPOSED — not locked` status: STEP-01..06 implemented in
`orca-harness/source_capture/company_aggregate/` (plus the EDGAR adapters + runners),
**108 offline unit tests passing**. A third, **code-level** cross-vendor review ran
(author Anthropic/Claude; reviewer OpenAI/GPT-5-Codex; repo-read, advisory): 1 critical
+ 4 major, **all in the v0 extraction/plumbing — the identity core (AR-04/05/06/07) was
confirmed sound in code.** All five were CA-adjudicated, remediated, and cleared by a
bounded same-vendor recheck (`ALL_CLOSED_NO_NEW_ISSUES`). Record:
`docs/review-outputs/company_aggregate_edgar_slice_code_review_v0.md`. Still not
validation / readiness / source-of-truth promotion; the EDGAR-first series remains a
filer-level UNRESOLVED trend until the entity spine resolves it.

## Owner Refinements (2026-06-12)

Owner input received after this scope was first written. These **sharpen
Decisions 1, 4, 5, 6 and the prerequisites** and take precedence over the inline
wording where they differ.

1. **The obligation-home blocker is *doctrinal*, not legal (Decision 1 / Prereq 1).**
   Correction to the earlier framing: the blocker is **which obligation contract
   governs standing capture**, not legality. The legal / source-access posture is
   *favorable* — Companies House and SEC EDGAR are official public data, cleanly
   in-bounds; the LinkedIn fallback is company-aggregate-only and attended.
   Clearing it is a **clarification**, not necessarily a heavyweight new contract:
   either amend the v0 obligation contract to admit a standing-corpus path, or
   stand up the separate Candidate Signal Intake / Corpus Intake contract v0
   already points to. What is required is an **explicit obligation home**, however
   light.

2. **SEC EDGAR is the first official adapter (Decision 4 / Prereq 2).**
   Authorize + build **EDGAR first** as the reference official adapter; Companies
   House second. Consequence kept visible: EDGAR-first does **not** serve Beauty
   Pie #3 (UK -> Companies House) — consistent with "no urgency"; Companies House
   is sequenced second, **not dropped**, and remains the UK adapter.

3. **Slice build stays gated on #1 (Prereq 3).** Confirmed: the slice build
   authorization comes **after the obligation home is clarified**.

4. **LinkedIn employee-band extension is in-flight (Decision 6 / Prereq 4).**
   Reported by the LinkedIn lane: the `numberOfEmployees` + size-band extractor
   extension is **being built now** under that lane's own authorization. The
   consume path's upstream dependency is being satisfied — no longer a
   pending-unstarted blocker. This does not change the consume decision; it
   confirms the consumed input will exist.

5. **Manual now, structured for additive automation (Decision 5 / Prereq 5).**
   Cadence is **manual / attended for now**. Design constraint: structure the
   capture core so **manual -> automatic is additive** — a **trigger-agnostic
   capture entrypoint** that a manual trigger calls now and a future scheduler can
   call later without re-architecting. This collapses the high-lock-in worry: the
   scheduler becomes a thin add-on over the same entrypoint, not a structural
   change. Note the split — **structure is prepared now; the periodic-scheduler
   *policy* lock (especially periodic-LinkedIn) still defers to a later owner
   call.** Preparing the structure does not take the periodic decision.

## Build Authorization, Obligation Home & Probe Findings (2026-06-12)

Following the owner refinements above, the owner authorized the build and a
read-only EDGAR feasibility probe ran. Current state:

### Authorizations (owner, in-thread 2026-06-12)

- **#3 slice build — AUTHORIZED.** The source-agnostic core (trigger-agnostic
  entrypoint, append-only entity-keyed store, source-adapter interface,
  source-selection) may be built.
- **#2 SEC EDGAR source-access adapter — AUTHORIZED** as the first official
  adapter. EDGAR is official public data, cleanly in-bounds. (Companies House
  remains a separate, still-pending owner-named authorization.)

Bounded to the named scope: not a scheduler authorization, not a commercial-
routing authorization, not a Companies House authorization.

### Standing-capture obligation home (clarification — discharges Prereq #1)

Clarified **lightly and slice-scoped**, per the owner's "clarification, not a
heavyweight contract" call:

- The company-aggregate forward series is **standing / corpus capture** — it
  accretes entity-keyed observations on a cadence before any specific Decision
  Frame.
- It runs under the **existing v0 capture obligations** (minimization, boundary
  compliance, capture-event provenance, decomposed timing, archive/visibility
  posture, failure visibility), reusing the LinkedIn lane's `business_entity_only`
  minimization rails.
- **Rebind rule:** a standing observation row is **not ECR-ready evidence** until
  rebound or re-captured under a Decision Frame (the v0 contract's standing-capture
  carve-out). The series is a corpus that commissioned captures later draw from,
  not pre-cleared evidence.
- **Retention:** append-only; re-observations supplement, never overwrite.
- **Narrow to this slice.** It does not write the general Candidate Signal Intake
  / Corpus Intake contract the v0 contract points to (a future general contract
  may supersede this), and does not amend the v0 obligation-contract file.

### EDGAR feasibility probe finding (read-only scouting, 2026-06-12)

**Finding: SEC EDGAR has no reliably-populated structured employee-count field.**
The DEI XBRL concept `dei:EntityNumberOfEmployees` returned **HTTP 404 for both
Apple (CIK 320193) and Microsoft (CIK 789019)** via the `companyconcept` API,
while a control concept (`dei:EntityCommonStockSharesOutstanding`) returned 200 —
the endpoint works; the employee tag is unpopulated even for two of the most
thoroughly XBRL-tagged filers.

Implication: the EDGAR employee count lives in **10-K Item 1 "Human Capital"
narrative** (annual). The EDGAR adapter is therefore a **text-extraction adapter
over the 10-K at annual cadence** — still official and reliable, but heavier than
an API field and coarser (annual) than assumed.

**Sequencing — RESOLVED (owner, 2026-06-12): EDGAR-first confirmed** (US-leaning
coverage rationale), accepting narrative 10-K extraction; the EDGAR adapter is
authorized. Companies House is **second**, and its clean-structured-count
assumption stays **unverified** — a Companies House probe is deferred to its own
adapter authorization, not run now.

### ToS / commercial-scale posture (owner, 2026-06-12)

ToS risk is **accepted pre-commercial** for the LinkedIn fallback (attended,
low-volume, posture-tagged). At commercial scale the ToS-risky access **routes
through a commercial data provider (BrightData-style) that absorbs the ToS risk**;
Orca does not scale the attended-browser path itself. Design consequence: the
LinkedIn adapter is **thin and disposable** — the pre-commercial attended adapter
and a future provider-feed adapter are two implementations behind the same
source-adapter interface. Durable investment concentrates in the official
adapters (EDGAR/CH) + the core, which carry no ToS risk and are the permanent
surfaces.

## Locked Implementation Call — EDGAR-First Slice (2026-06-12, review-gated)

Produced by the `/fused` pre-implementation lanes (scoping → spec →
micro-lock). **Status: SUPERSEDED by cross-vendor review (2026-06-12) → bounded
architecture revision** (see the adjudication subsection at the end of this
section). The two-layer *instinct* survives; the single-record Layer-2 contract
below does **not** — it is the historical proposal that went into review.
**No code was written.**

### Data-shape call (high lock-in)

Two layers. **Layer 1 (capture) = `SourceCapturePacket`, unmodified** — each
EDGAR reading is one packet preserving the 10-K excerpt; ECR binds packets by
`packet_id`+`evidence_slice_id` (verified firsthand in
`orca-harness/evidence_binding/composer.py`), so packets-as-capture-unit
preserves the ECR binding path. **Layer 2 (series) = a NEW entity-keyed,
append-only derivation record** built on the `reddit_consolidation` pattern
(validate + re-verify sha256 → derive outside the immutable packet →
`schema_version` + `non_claims`), but a new many-packets→one-entity-series fold.
**`entity_key` lives in Layer 2 only**, never the packet (keeps capture
decoupled from the unbuilt entity-resolution spine).

### Layer-2 record contract (thin spec)

- Fields: `schema_version`; `entity_key`; ≥1 `raw_surface_form`; `source` ∈
  {`sec_edgar`,`companies_house`,`linkedin`}; `capture_posture` ∈
  {`official`,`attended_fallback`}; `number_of_employees`; `size_band`;
  `follower_count`; `source_effective_date`; `capture_date`; provenance
  (`packet_id`,`slice_id`,`sha256`).
- **Honesty invariant:** every measured field + `source_effective_date` carries
  a NAMED state (known value | named absence + reason) — never a silent null or
  guess (reuse the existing `VisibleFact` discipline).
- **Append-only:** logical-point identity = (`entity_key`,`source`,
  `source_effective_date`); re-captures appended as new rows, never overwriting;
  trend orders by `source_effective_date`.
- **EDGAR captures only:** the adapter yields the filing + *structured* filing
  metadata (CIK, form, period-of-report, filing date — structured, not
  narrative); the employee count (narrative) is extracted in Layer 2.
  `EdgarSuccess`/`EdgarFailure` carry no interpreted count. For
  `source=sec_edgar`, `follower_count` + `size_band` = `not_applicable`.

### Route (read-only; STEP-01..06)

STEP-01 Layer-2 contract → STEP-02 EDGAR adapter (`fetch_edgar_*`, composes
`direct_http` behind the seam, declared SEC User-Agent) → STEP-03 packet runner
→ STEP-04 derivation (re-hash + narrative extraction) → STEP-05 append-only
series → STEP-06 trigger-agnostic entrypoint (manual now). Offline unit tests
per unit; no live network in unit/contract tests.

### Locked micro-decisions

- Module home: `source_capture/company_aggregate/` (mirrors
  `reddit_consolidation`). [reversible]
- Honesty type: reuse `source_capture` `VisibleFact` (import, don't fork).
  [review-gated]
- `number_of_employees`: VisibleFact state authoritative + a typed int only when
  state=known. [review-gated]
- Series persistence: append-only file artifact outside the packet; **no
  DB/storage** (separately gated, unauthorized). [authority-forced]
- `entity_key` provisional: `{source}:{raw_id}` (e.g.
  `sec_edgar:CIK0000320193`), swappable to canonical. [review-gated]
- EDGAR transport: compose `direct_http.fetch_direct_http_capture`. [reversible]

### Non-claims (this section)

Not implemented (no code this turn). Not validated, not ready. The
review-gated record-contract elements are review proposals, not owner-final.
Not storage/DB/scheduler authorization, not ECR field design, not entity-spine
resolution.

### Cross-Vendor Review Adjudication (2026-06-12)

A cross-vendor delegated review ran (author Anthropic/Claude; controller
OpenAI/GPT; de-correlation satisfied; advisory / `no_repo`). **Verdict:
`NEEDS_ARCHITECTURE_PASS` — accepted by home-model adjudication.** All eight
findings (AR-01..AR-08) were adjudicated as **accepted** (several bounded). The
diff/verdict were treated as claims, not premises. Survivors: the two-layer
instinct, packet-as-capture-unit, ECR-binding, consume-not-absorb. **The
single-record Layer-2 contract above is superseded** by a bounded architecture
revision:

- **Split Layer 2** → an **immutable observation event** keyed on durable source
  facts (source + CIK + accession + period-of-report + packet provenance — **not**
  the provisional `entity_key`) + a **derived entity projection**
  (resolution-map-driven, re-derivable; `entity_key` is a resolved attribute, not
  part of immutable identity). [AR-01, AR-02, AR-06]
- **Capture the full raw filing** in Layer 1, not a hand-selected excerpt;
  region/span selection moves into Layer-2 extraction. [AR-04]
- Add **derivation provenance** (deterministic parser method+version+run) + a
  **supersession relationship**, reusing the packet's `re_capture_relationship`
  idiom. [AR-05]
- Add bounded **value-quality** (exact/approximate/ambiguous) + **measurement
  basis** (full-time/total/average/segment) to a known count. [AR-03, AR-07]
- **Tighten non_claims:** raw observations; cross-year/cross-company
  comparability **not established** (a probability-shifter, not a clean trend).
  [AR-07]
- Do **not** pre-couple non-EDGAR fields (`follower_count`/`size_band`) into the
  durable EDGAR observation; per-source measures, unified at the projection
  layer. [AR-08]

**Implementation does NOT proceed.** Next authorized step: a **bounded
architecture revision** re-derives the Layer-2 contract above; `STEP-01..`
resume only after that revision (owner may commission a lighter re-review of the
revised shape).

## Revised Layer-2 Architecture (2026-06-12, BUILT — see "Build + code-review status" above)

Output of the standard 3-subagent architecture pass that re-derived the Layer-2
contract along the accepted AR-01..AR-08 direction. Three independent,
code-grounded designs **converged** on the shape below (a confidence signal).
**Status: BUILT + green + code-reviewed** — STEP-01..06 implemented, 108 offline tests,
the cross-vendor code review remediated + same-vendor-rechecked (see "Build + code-review
status" under Status above). Supersedes this section's original `PROPOSED — not locked`
status. Still not validation / readiness / source-of-truth promotion.

**Three records, not one** (separates identity that must never move from
identity that will move):

- **Layer 1 — `SourceCapturePacket`, unmodified.** Preserves the **full 10-K
  filing** bytes (`raw_stored_bytes`), one slice; structured filing metadata
  (CIK/accession/form/period_of_report/filing_date) carried as `KNOWN`
  `VisibleFact`s. No excerpt, no employee number, no `entity_key`. Stays
  ECR-bindable by `(packet_id, evidence_slice_id)`; full-filing capture
  *strengthens* the inspectability posture. [AR-04]
- **Layer 2a — `EdgarHeadcountObservation`** (NEW, immutable, append-only, in
  `source_capture/company_aggregate/`):
  - **Durable identity = `(source, cik, accession, period_of_report)`** —
    `entity_key` is **absent** from immutable identity. [AR-01/02/06]
  - **`extraction_span`** = `{preserved_file_id, source_sha256 (re-verified),
    start, end, excerpt_sha256, matched_text, pattern_id}` — the re-derivable
    receipt of where in the immutable bytes the count was read. [AR-04/05]
  - **Measure** = `employee_count: VisibleFact` (known int | named absence +
    reason) + `value_quality` (closed) + `measurement_basis` (closed
    `VisibleFact`). [AR-03/07]
  - **`derivation`** = `{parser_method, parser_version, ruleset_sha256, run_id}`
    — deterministic regex, not an LLM. [AR-05]
  - **`supersedes`** = `{relationship ∈ RE_CAPTURE_RELATIONSHIP_VALUES,
    prior_ref}`. [AR-05]
  - **No** `follower_count`/`size_band`. [AR-08] Append-only file artifact
    outside the packet dir; no DB.
- **Layer 2b — `CompanyHeadcountProjection`** (NEW, DERIVED, **computed-on-read,
  not persisted as truth**): `entity_key` resolved **here** via an injected,
  versioned `ResolutionMap` (v0 default = passthrough `sec_edgar:CIK…`); fold =
  resolve → group by `entity_key` → collapse supersession chains → order by
  `period_of_report` → per-source lanes (source-tagged, NOT inter-converted;
  official-first is a read-time view). **Merge/split/remap handled in the map +
  fold; the immutable log is never touched.** [AR-01/02/06/08]

**Re-extraction vs new-observation:** same `accession` ⇒ re-extraction
(`supersede`/`conflict`); new `accession` + new period ⇒ new (`supplement`); new
`accession` + same period (10-K/A) ⇒ `mixed`. Append-only keeps both rows;
"supersede" is a projection-collapse instruction, never a delete.

**Reuse vs new:** reuses `VisibleFact` (import, don't fork),
`RE_CAPTURE_RELATIONSHIP_VALUES`, the `reddit_consolidation` derive-from-bytes
contract (re-hash gate → derive-outside-packet → `schema_version`+`non_claims`),
the closed-posture validator, `append_yaml_document`. The split + full-filing/span
boundary + per-source-models-unified-only-at-projection are the only new
structural surfaces.

**Open questions for owner / the lighter re-review:**

1. **ResolutionMap / ResolutionEvent ownership (doctrine boundary):** confirm
   this lane only *applies* resolution (consumes the map), never *authors* it —
   else the capture lane silently acquires entity-resolution authority.
2. **Durable key disambiguator:** add `measurement_basis` (or an
   `extraction_target` token) to the key for multi-statement filings, or keep
   the 4-tuple for v0? Lean: 4-tuple now; add only when a real filing forces it.
3. **Full-filing vs the `direct_http` 5 MB cap:** 10-K primary docs can exceed
   it — adapter raises the cap / fetches the primary document only /
   bounded-but-complete. Constrains what "full filing" means.
4. **Minor:** `value_quality`/`measurement_basis` membership; projection conflict
   handling (lean: surface both); `range` encoding (lean: non-known + range in
   reason); structured-metadata as a 2nd preserved file (lean: yes).

**non_claims:** PROPOSED architecture, not locked, not implemented; raw
observations, cross-year/cross-company comparability NOT established; `entity_key`
provisional; not ECR-ready until rebound under a Decision Frame; not storage/DB/
scheduler authorization; not entity-spine authorship.

### Second (Narrow) Cross-Vendor Review Adjudication (2026-06-12)

A narrow cross-vendor re-review ran (author Anthropic/Claude; controller
OpenAI/GPT; de-correlation satisfied; advisory / `no_repo`), scoped to the
identity split + merge/split model + the **#1 ownership boundary**. **Verdict:
sound-with-fixes — accepted.** The core identity split and the #1 boundary are
**confirmed directionally sound and strengthened** — a tightening, not a restart.
All 7 findings accepted; two corrected the author's own claims (AR-04, AR-05).

- **AR-01 (blocker) — merge semantics:** the merge model conflated
  *continuity-remap* (same entity, join histories) with *economic
  rollup/acquisition* (distinct entities — must NOT retroactively flatten). Fix:
  distinguish them; economic rollup needs a temporal/effective boundary and is
  **spine-authored + a hard-STOP for this lane** (reinforces #1). Does NOT gate
  EDGAR-first (passthrough does no merges); recorded for the spine contract.
- **AR-02 (major) — split discriminator:** make the `ResolutionEvent`
  discriminator typed/extensible (period-boundary is one type; also
  effective-date / accession / observation-id). Spine-owned; doesn't gate
  EDGAR-first.
- **AR-03 (major) — filing key vs observation key:** the durable 4-tuple is a
  *filing-period* key; a single 10-K can state total + full-time + segment counts,
  so it is not a safe *observation* key as-is. Fix: add an immutable observation
  discriminator (`measurement_basis`/`extraction_target`) to the key, or
  state+enforce one-canonical-observation-per-filing. **Elevates open-question #2
  from defer to MUST-RESOLVE. Gates EDGAR-first.**
- **AR-04 (major) — passthrough sufficiency [corrects the author]:**
  "passthrough-by-CIK = a company headcount trend" was overstated. CIK is a
  *filer* id, not a company id (consolidated parent filings, multi-CIK businesses,
  re-IPO/successor paths). Fix: the interim output is an **unresolved, filer-level**
  series — type it `provisional_filer_key`, "entity not resolved" visible to every
  consumer. **Gates EDGAR-first.**
- **AR-05 (major) — entity_key leak [corrects the author]:** emitting a
  provisional value in a field named `entity_key` leaks a de-facto canonical id.
  Fix: separate `provisional_filer_key` (interim) from `entity_key` (populated
  only when the spine resolves); `resolution_state ∈ {unresolved, resolved}`;
  unresolved outputs may not be treated as canonical. **Strengthens #1; gates
  EDGAR-first.**
- **AR-06 (major) — reproducibility binding:** bind `(map_version +
  resolver_version + event_ordering + conflict_rule)` on every projection; reads
  pin a version, never float to "latest." **Gates EDGAR-first.**
- **AR-07 (minor) — interface authority creep:** define the consumer interface as
  a deliberately-provisional **port** under a neutral/stub namespace the spine can
  replace, not buried as authoritative.

**Open question #1 — SETTLED + hardened:** entity-resolution **authoring** = the
(unbuilt) spine's; this lane **consumes only** and ships a passthrough-**null**
that emits `provisional_filer_key` + `resolution_state=unresolved` (**never** a
canonical `entity_key`); economic merge/rollup is spine-authored + a hard-STOP;
the consumer interface is a provisional port. The EDGAR-first series is honestly a
**filer-level unresolved trend** until the spine resolves it — correctly labeled.

**Status:** revised architecture adjudicated **sound-with-fixes**; #1 settled.
Gating EDGAR-first fixes (AR-03, AR-04, AR-05, AR-06, AR-07) are the build's first
task; spine-contract fixes (AR-01, AR-02) are recorded and don't gate EDGAR-first.
`STEP-01..` may resume on the corrected shape at the owner's go. Recheck posture:
same-family CA folded the reviewer's explicit minimum-fixes into this record; the
edits transcribe the findings directly.

## Inputs (source-loading, S-route bound)

- **Controlling authority:** `docs/decisions/company_aggregate_forward_signal_architecture_decision_v0.md` — owner-locked AO-3, official-first policy, core/satellite boundary, posture recommendation. This scope obeys it and does not reopen it.
- **Capture-lane obligation contract:** `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md` — the lane's minimization + obligation rails (reconciled below).
- **Source-access tooling authorization:** `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md` — the tranche-gated, owner-named-adapter pattern the official adapters must follow.
- **LinkedIn extraction adapter (the thing to consume or absorb):** `orca-harness/capture_spine/linkedin_live_runtime/` (slice 3c-2b: `extract_company_signal` -> `CompanySignal`).
- **Discovery-tier input (weighed, not authority):** `docs/research/orgmotion_demand_signal_wedge_discovery_v0.md`.

---

## Decision 1 — Ownership: ACCEPT (with one load-bearing condition surfaced)

The capture lane **owns** the sibling company-aggregate forward-signal slice as
routed by the parent. It fits the lane's charter: a source-agnostic,
entity-keyed, official-first capture surface whose official adapters (Companies
House, SEC EDGAR) are capture-lane source surfaces, built against the same
Source Capture Packet / adapter shape the lane already uses.

**Condition surfaced — the obligation-home gap (the bottleneck).** The forward
*trend* is **standing / opportunistic capture**: it accretes an entity-keyed
time series on a cadence **before any specific Decision Frame exists**. The
lane's v0 obligation contract scopes **commissioned capture only** and
**explicitly routes standing / opportunistic corpus capture out** of v0 to "a
separate Candidate Signal Intake or Corpus Intake contract" — which **does not
yet exist**. Consequences:

- This slice's **obligation home is that not-yet-written standing-capture
  contract**, not the v0 commissioned-capture contract. Ownership is accepted;
  the obligation contract for it is a **prerequisite the owner must commission**
  before a clean build.
- Per v0, items captured under standing/corpus intake are **not ECR-ready
  evidence until rebound or recaptured under a Decision Frame**. The forward
  series is therefore a **standing corpus that later commissioned captures draw
  from**, not pre-cleared evidence. That is the correct shape for a
  "leading-indicator / corroboration" signal (per the discovery note), but it
  must be stated, not assumed.

This condition does not block authoring the scope; it blocks a clean build and
is flagged for the owner as the first prerequisite.

## Decision 2 — Record shape (capture-method level, NOT an ECR schema)

A **source-agnostic, entity-keyed observation series**. The atomic unit is one
**observation row**; the **trend** is the ordered set of rows per entity.

Per-observation facts to preserve:

- `entity_key` — a canonical-entity reference the **entity-resolution spine**
  owns and resolves (LinkedIn slug, Companies House number, CIK, brand-vs-parent
  surface forms map to it). Capture **carries** the key and the raw surface form;
  it does **not** invent canonical identity or roll up the brand->parent tree
  (the discovery note flags brand->parent as load-bearing in beauty; that is the
  entity spine's job, not Capture's).
- `numberOfEmployees` — integer, when an official source supplies it.
- `size_band` — coarse band (e.g. `10,001+`), when supplied.
- `follower_count` — coarse count/band, LinkedIn-only corroboration figure.
- `source` tag — `companies_house` | `sec_edgar` | `linkedin` (extensible).
- `capture_posture` tag — `official` | `attended_fallback` (carries the
  legally-defensible posture forward into the row, per the parent).
- **Decomposed timing** (Obligation 8, not one timestamp): source-effective /
  filing / as-of timing **vs** capture timing — divergence is the point for a
  trend.
- Access posture + provenance + visible limitations (Obligations 2, 3, 11, 14).

**Persistence = append-only.** A re-observation **supplements** the prior row
(it does not overwrite it); the trend is preserved (Obligation 15 re-capture
semantics — later access does not erase earlier observations). No single
"current headcount" cell that silently mutates.

Capture records visible facts only. This shape is **not** an ECR field
architecture, key design, table, or storage schema — defining those is a
forbidden Capture output and belongs downstream.

## Decision 3 — Source-selection policy: official-first (locked by parent)

Per entity, select the source in this order:

1. **Companies House** (UK) — official annual employee count, when the entity is
   UK-registered.
2. **SEC EDGAR** (US) — when the entity is US-public.
3. **LinkedIn** — **fallback only**, for **US-private / no-official-source**
   entities, under the attended posture (Decision 5).

Official and LinkedIn rows for the same entity are both retained and
**source-tagged**; the policy chooses the **preferred** row for a given read, it
does not delete the others. The parent locks official-first and LinkedIn-as-least-
defensible; this decision only operationalizes the ordering.

## Decision 4 — Official adapters need their OWN source-access authorizations (NOT granted here)

Companies House and SEC EDGAR are the **preferred** surfaces, and both are
official / disclosable surfaces that sit well inside the unchanged source-access
boundary — a **favorable** posture for a future authorization. But each is a
**new source-access surface** and a **new owner-named adapter**. Under the
existing tooling-build authorization, "additional owner-named source adapters"
are built against the shared packet/adapter contract **only when the owner names
and authorizes them**.

Therefore: **each official adapter (Companies House, SEC EDGAR) requires its own
bounded source-access / build authorization** that names the adapter, the source
family, the access method, the risk posture, and non-claims. This scope decision
**does not** grant them, and does **not** assert either adapter is feasible or
implemented — adapter feasibility (API shape, employee-count availability,
archival/backtest posture) is a build-time verification item, not a claim made
here.

## Decision 5 — Cadence + persistence posture (recommendation carried; high-lock-in axis deferred)

- **LinkedIn fallback:** **attended / low-frequency, posture-tagged — NOT a
  periodic-default scheduler.** Carried verbatim from the parent's posture
  recommendation; it preserves the legally-defensible posture and matches the
  existing attended runtime (the 3c-2b `CdpAttachBrowserDriver` is owner-validated
  and behind the legal/ToS gate).
- **Official adapters:** the official surfaces are inherently low-frequency
  (annual / periodic filings); they are the natural periodic surface and carry
  far lower posture risk than periodic LinkedIn. This decision still does **not**
  lock a scheduler for them.
- **High-lock-in axis, deferred:** a periodic-default **scheduler** (any source,
  LinkedIn especially) is the high-lock-in, owner-flagged axis. Per the parent,
  the final cadence call is the capture lane's **build-time** decision and the
  owner may override then. **Scope-time default = attended / manual-trigger,
  posture-tagged**; the scheduler lock is **not** taken here. This is the single
  line to flip if the owner later accepts a periodic-LinkedIn lock-in for the
  US-private gap.

Standing capture (Decision 1) also routes the cadence question through the
not-yet-written standing-capture obligation contract — another reason not to lock
a scheduler now.

## Decision 6 — LinkedIn extraction adapter home: CONSUME, not absorb

The LinkedIn lane recommends handing its 3c-2b extraction adapter to the capture
lane. **This decision keeps it in the LinkedIn lane and consumes its output.**

- The owner-locked parent **core/satellite table assigns "LinkedIn company-page
  extraction" to the LinkedIn lane.** Absorbing the adapter into the capture
  lane's adapter set would **re-assign an owner-locked boundary** — not a
  capture-lane scope decision's call. Consuming needs no boundary change.
- **Lower downstream lock-in** (the Smallest Complete Intervention tie-breaker):
  the LinkedIn fallback is rarely hit (US-private only; not even needed for
  Beauty Pie #3). Moving its code into the capture lane is premature
  consolidation; consuming keeps absorb available later if the owner re-assigns
  the boundary.
- **Respects the existing one-way import discipline** (`runtime -> adapter ->
  core`) and the lane's minimization gate. The capture lane consumes the
  **already-minimized, gate-passed** observation the LinkedIn lane emits
  (`extract_company_signal` -> `CompanySignal`, then the lane's
  `minimize_capture_to_observation` -> validated `LiveObservation`). It does
  **not** reach into LinkedIn itself.

**Consume mechanics:** the capture lane's source-agnostic core treats the
LinkedIn lane's minimized employee-aggregate observation as **one source-adapter
input behind the same interface** as the Companies House / EDGAR adapters,
tagged `source=linkedin`, `capture_posture=attended_fallback`.

**Dependency to record:** the parent says the LinkedIn adapter still **needs
`numberOfEmployees` + size band added** (the 3c-2b extractor today pulls
`display_name` + follower band and **defers** employee-band extraction). That
extension is the **LinkedIn lane's own pending build** under its own
authorization — a **prerequisite of the consume path**, owned there, not here.

If the owner prefers consolidation, **absorb** is the alternative — but it
re-assigns the owner-locked core/satellite boundary and is not needed now;
surfaced, not taken.

## Minimization reconciliation (against the lane's obligation contract)

Reconciled and **consistent**. The slice is **company-aggregate only**: a
business entity's employee count, size band, and a coarse follower figure — no
individuals, no senior-moves roster, no follower/connection lists, no graphs, no
profile/post content. This sits inside the lane's Boundary Compliance
(Obligation 2) and matches the LinkedIn adapter's already-built `business_entity_only`
rails (the 3c-2b extractor fail-closes out of the social-proof / person region by
construction, and the read-time minimizer default-denies every non-`LiveObservation`
field). The minimization the handoff asks for is the minimization the lane
already enforces; ownership does not loosen it.

## Beauty Pie #3 reality check (carried)

Forward LinkedIn does **not** serve Beauty Pie #3 — a past *UK* case whose
net-adds proxy is **Companies House**, not a go-forward LinkedIn signal. This
slice is **go-forward realization for future cases**; there is **no urgency**
forcing the high-lock-in periodic / scheduled path (LinkedIn or otherwise) now.
The lowest-lock-in moves (official-first, attended fallback, consume-not-absorb,
scheduler deferred) are therefore the correct scope-time defaults.

## Owner prerequisites (what must exist before a clean build)

> **Status (2026-06-12):** #1 clarified above (slice-scoped, light); #2 (SEC
> EDGAR) and #3 authorized; #4 in-flight in the LinkedIn lane; #5 manual-now
> (scheduler deferred). The original framing below is retained for context — the
> dated section above carries current state.

1. A **standing / corpus-capture obligation contract** (the Candidate Signal
   Intake / Corpus Intake contract v0 routes to) — this slice's obligation home.
2. A **per-adapter source-access / build authorization** for Companies House,
   and another for SEC EDGAR.
3. The **build authorization** for the slice itself (record/persistence/cadence).
4. The **LinkedIn lane's** `numberOfEmployees` + size-band extension build (the
   consume path's upstream dependency), under the LinkedIn lane's own authorization.
5. A **cadence/scheduler decision** if any periodic-default is wanted (the
   high-lock-in line).

## Non-Claims

Scope / ownership only. **Not** a build authorization, **not** a source-access
authorization (the official adapters each need their own), **not** owner-locked,
**not** an amendment to the capture-lane obligation contract (the standing-capture
gap is surfaced, not closed), **not** an ECR field/key/schema/storage design,
**not** a cadence/scheduler lock, **not** validation, readiness, or buyer-proof.
Does not assert Companies House or SEC EDGAR adapter feasibility — that is a
build-time verification item. Does not change the LinkedIn lane's obligation
contract or its ownership of the extraction adapter.

## Direction Change Propagation

> **Update (2026-06-12):** the dated "Build Authorization, Obligation Home &
> Probe Findings" section above layers the owner's #2/#3 authorizations, the
> slice-scoped standing-capture obligation-home clarification, and the EDGAR
> probe finding on top of the original scope. The receipt below records the
> **original** scope decision's propagation; the record still does not itself
> grant the authorizations (the owner did, in-thread) and does not amend the v0
> obligation-contract file.

```yaml
direction_change_propagation:
  doctrine_changed: >
    The capture lane accepts ownership of the company-aggregate forward-signal
    sibling slice and scopes it: an append-only, entity-keyed, source-tagged
    observation series; official-first source selection (Companies House, SEC
    EDGAR) with LinkedIn as attended US-private fallback; each official adapter
    requiring its own separate source-access authorization; an attended /
    non-scheduler cadence default with the periodic-scheduler lock deferred; and
    the LinkedIn 3c-2b extraction adapter consumed (kept in the LinkedIn lane),
    not absorbed. It surfaces that the slice's obligation home is a
    not-yet-written standing / corpus-capture contract, since the v0 obligation
    contract scopes commissioned capture only.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/company_aggregate_forward_signal_capture_lane_scope_decision_v0.md
  downstream_surfaces_checked:
    - docs/decisions/company_aggregate_forward_signal_architecture_decision_v0.md
    - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: docs/decisions/company_aggregate_forward_signal_architecture_decision_v0.md
      reason: >
        The parent routed the slice here and named "Capture lane scopes the
        sibling slice" as its Next step; this record is that object. It obeys the
        parent and does not edit it. The parent is itself untracked / in-thread.
    - path: docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
      reason: >
        NOT amended. The standing-capture obligation-home gap is surfaced for the
        owner, not closed here. Writing the standing / corpus-capture obligation
        contract is owner + pressure-test work, out of this scope-only decision.
    - path: docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md
      reason: >
        NOT amended. The official adapters (Companies House, SEC EDGAR) each need
        their own owner-named source-access authorization under its existing
        tranche pattern; this decision states that requirement, it does not grant it.
    - path: docs/workflows/data_capture_spine_consolidation_map_v0.md
      reason: >
        Routing-surface registration DEFERRED. The parent architecture decision
        is itself untracked and not yet registered in the consolidation map,
        source-of-truth known-source list, or repo map. Registering this child
        before the parent is committed/propagated would route agents to an
        uncommitted decision pair. Registration is left to the owner's
        commit/propagation pass for this whole topic.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Known-source registration DEFERRED for the same reason — the parent is
        unregistered and in-thread; this child registers with it, not before it.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Repo map indexes decisions at a path level and the parent is not yet
        listed; deferred to the same topic-level commit/propagation pass.
  stale_language_search: >
    not_run — scope-only decision in a dirty shared working tree whose parent is
    itself uncommitted and unregistered; no live routing surface yet references
    either decision, so there is no stale routing language to search. The
    stale-language sweep belongs to the owner's topic-level commit/propagation
    pass that registers the parent + child together.
  non_claims:
    - not validation
    - not readiness
    - not a build authorization
    - not a source-access authorization
    - not owner-lock
    - not an obligation-contract amendment
    - not ECR, Cleaning, or Judgment design
    - not a cadence/scheduler lock
```
