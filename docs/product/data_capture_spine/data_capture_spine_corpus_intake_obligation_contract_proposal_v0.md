# Data Capture Spine — Corpus Intake (Standing-Capture) Obligation Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product-method contract (owner-ratified 2026-06-15; supersedes the prior PROPOSED status)
scope: >
  Proposes the standing-capture sibling to the v0 commissioned Data Capture
  obligation contract — the "Candidate Signal Intake or Corpus Intake contract"
  that v0 routes standing/opportunistic capture out to, and that does not yet
  exist. Defines the obligations for recurring capture of an approved public
  signal into an append-only corpus BEFORE any Decision Frame exists, serving
  both the demand-durability indicators (hourly/daily) and the company-aggregate
  org-motion forward series (periodic). Inherits the v0 obligation set; adds only
  the standing-capture deltas. As a ratified obligation contract it still
  authorizes no build, no scheduler, no runtime, and no source access, and is
  not ECR-ready evidence machinery.
use_when:
  - Deciding whether a recurring / standing / pre-Decision-Frame capture activity has an obligation home.
  - Reviewing or ratifying the general standing-capture / corpus-intake obligation contract.
  - Reconciling the company-aggregate org-motion slice clarification and the demand-durability indicators under one standing-capture regime.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md          # the commissioned sibling (routes standing OUT to here)
  - docs/product/data_capture_spine/data_capture_spine_candidate_url_intake_contract_v0.md               # the locator layer below this contract
  - docs/decisions/company_aggregate_forward_signal_capture_lane_scope_decision_v0.md                    # the org-motion slice clarification this supersedes as obligation home
  - docs/product/data_capture_spine/capture_envelope_durability_delta_spec_v0.md                         # the demand-indicator durability elements this governs standing
  - docs/product/data_capture_spine/demand_durability_indicator_standing_capture_obligation_home_decision_framing_v0.md   # the owner-decision framing (D1=general, D3=deferred) this answers — landed via merged PR #106 (indicator rename)
  - docs/decisions/pre_capture_discovery_spine_charter_recommendation_v0.md                              # WHERE-side discovery (deconflicted; not this contract)
  - docs/product/product_lead/orca_buyer_proof_packet_v0.md                                              # never-a-feed invariant (the structural lock)
stale_if:
  - The owner amends, supersedes, or re-scopes this ratified contract.
  - The v0 commissioned obligation contract changes its standing-capture carve-out, its rebind rule, or its obligation set.
  - The Source Capture packet schema (manifest v1) changes the provenance/timing/posture/re-capture facts this inherits.
  - The company-aggregate slice clarification is re-scoped, or the demand-durability indicator profiles change their captured series.
  - A scheduler/runtime build for standing capture is authorized (a separate, later authorization).
```

## Status

- Status: `CONTRACT_RATIFIED_V0_2026_06_15` — **owner-ratified 2026-06-15**, superseding the prior `PROPOSED_NOT_RATIFIED` status. Ratification accepts the obligation contract; it is **not** a hardening or validation claim — the contract is **not yet pressure-tested** (see Pressure-Test Requirement).
- Artifact type: Product-method contract (ratified; docs-write).
- Direction answered: the owner-selected **D1 = general** (one Candidate-Signal / Corpus Intake contract serving both the demand-durability indicators and the company-aggregate org-motion lane) and **D3 = scheduler deferred** (trigger-agnostic entrypoint), recorded in `demand_durability_indicator_standing_capture_obligation_home_decision_framing_v0.md`. D2 follows D1: a **separate sibling contract**, not a v0 amendment.
- Ratification: **owner-ratified 2026-06-15** · Implementation authorized: **no** · Scheduler/runtime authorized: **no** · Source access authorized: **no** · Hardening: **no** (pressure-tests not yet run). Ratifying the obligation contract authorizes none of build, scheduler, runtime, or source access.
- Ratification path (complete): delegated cross-vendor adversarial review (doctrine-bearing) → R1 hardening → **owner ratification 2026-06-15**. Remaining: (1) propagation to the controlling surfaces listed in `proposed_direction_change` (tracked post-ratification fast-follow); (2) pressure-testing per the Pressure-Test Requirement before any hardening claim.
- **R1 hardening (2026-06-15):** patched against a cross-vendor adversarial review (controller = GPT-5 Codex / OpenAI; `de_correlation_bar: cross_vendor_discovery`). All five findings accepted; the CA-adjudicated remedy was a **bounded patch round** (S1 charter-as-owner-gated-gate; S3 runtime-architecture overreach removed; S5 checkable rebind gate; S7 behavioral never-a-feed boundary; pressure-test closure criteria bound) — **not** a full architecture pass. Adjudication record: `docs/review-outputs/adversarial-artifact-reviews/corpus_intake_contract_cross_vendor_adversarial_review_v0.md`.

## Purpose

The v0 Data Capture obligation contract governs **commissioned capture** — capture performed for an existing Decision Frame. It explicitly routes **standing / opportunistic corpus capture out** of v0 to "a separate Candidate Signal Intake or Corpus Intake contract," and states that standing items are **not ECR-ready evidence until rebound or recaptured under a Decision Frame.** That separate contract does not yet exist. Two lanes have now independently hit the resulting obligation-home gap:

- the **demand-durability indicators** (price, availability/restock, search-interest, review-velocity) the owner confirmed should be monitored continuously on an **hourly-to-daily** rhythm; and
- the **company-aggregate org-motion forward series** (headcount/size-band trend), which accretes entity-keyed observations on a periodic cadence before any Decision Frame.

This contract answers one question:

```text
When Orca captures a public signal recurringly, before any Decision Frame
exists, what obligations must that standing capture satisfy so the resulting
corpus is inspectable, bounded, minimized, and safely re-bindable as
decision-substrate — without becoming evidence-by-stealth or a sold feed?
```

It is a product-method contract. It is **not** an ECR schema, Cleaning design, Judgment ruleset, source inventory, runtime/scheduler plan, scraper/API plan, storage design, dashboard, or build authorization.

## Position In The Capture Stack (the layer this owns)

This contract is deliberately narrow about where it sits, because adjacent landed work bounds it on every side:

| Layer | Owner artifact | What it owns | Relationship to this contract |
| --- | --- | --- | --- |
| Pre-capture discovery (WHERE) | `pre_capture_discovery_spine_charter_recommendation_v0.md` (rec: `DO_NOT_BUILD` a spine) | Direction-driven venue exploration: *where* signal lives, before any capture decision | **Not this contract.** Discovery is WHERE-side; this is capture-side recurring capture of an **already-approved** series. This contract does not discover venues. |
| Candidate locator intake | `data_capture_spine_candidate_url_intake_contract_v0.md` | Bounded candidate **locator** rows + a promotion gate; inert planning context; explicitly *not* fetch/render/runner/capture | **Layer below.** Its promotion gate hands one selected locator to "a later authorized capture path." For a standing series, **this contract is that authorized path.** It does not produce locators. |
| **Corpus Intake / standing capture (this contract)** | **this contract** | The obligations for **recurring capture of an approved series into an append-only corpus, before a Decision Frame** | The standing analog of the v0 commissioned contract; the obligation home the two lanes need. |
| Commissioned capture | `core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Capture **for a Decision Frame** | **Sibling + rebind target.** v0 routes standing OUT to here; standing rows become ECR-ready only by recapture/rebind **back** under a Decision Frame (governed by v0). |
| ECR / Cleaning / Judgment | (downstream spines) | Evidence receipt, transformation, decision use | Never touched directly by standing capture. The corpus is substrate, not evidence. |

### Why this is not the "owner-rejected standing registry"

The pre-capture discovery charter recommendation cautions against "a standing knowledge-home created ahead of proven reuse" and routes such moves through a **promote-on-reuse** owner trigger. This contract is consistent with that doctrine, not in tension with it:

- **It is promoted on proven reuse, not ahead of it.** Two independent lanes (demand indicators + org-motion) hit the identical standing-capture gap. That cross-lane recurrence *is* the promote-on-reuse signal the doctrine asks for; the framing note's D1 rationale ("the gap now blocks two lanes") is that argument.
- **It is an obligation contract, not a data home.** The "standing registry" the owner rejected is a standing *knowledge artifact* accreting ahead of need. This is the *rulebook* that governs standing capture two lanes already need — it accretes no data and stands up no spine. Each lane keeps its own corpus and record shape.
- **It charters no discovery spine.** It governs capture of approved series only; venue discovery stays where the charter recommendation left it.

## Contract Rule

Standing capture inherits the v0 contract's discharge vocabulary unchanged: every obligation is made explicit as one of `met`, `partial`, `assessed_not_met`, `cannot_assess`, `access_failed`, `blocked`, `unavailable_by_source`, `not_applicable`, or `not_attempted` (definitions per the v0 contract). Silent omission is not allowed; unknowns are acceptable only when the unknown state and reason are visible.

## Inherited Obligations (v0, unchanged)

Every observation captured under standing capture must discharge the v0 obligations **2–16** exactly as a commissioned capture would, and standing cadence does **not** loosen any of them:

- **Ob.2 Boundary compliance** — same source-access boundary, same hard stops; standing volume is not a licence to expand it. Recurring access to in-bound material is in-bounds; recurring access does not convert out-of-bound material into in-bound.
- **Ob.3–5 Capture-event provenance, mode disclosure, mode-change visibility** — per re-observation.
- **Ob.6 Raw observable fidelity**, **Ob.7 Source identity/actor context**.
- **Ob.8 Decomposed timing** — source-effective vs capture vs re-capture timing kept separate; divergence across the series is the point.
- **Ob.9 Cutoff posture**, **Ob.10 Archive/historical posture**, **Ob.11 Source visibility/access limits** — closed posture vocabularies, write-time enforced by the Source Capture packet schema (manifest v1).
- **Ob.12 Related context**, **Ob.13 Bundled-offer structure** (where applicable), **Ob.14 Capture failure/blocker visibility**.
- **Ob.15 Re-capture semantics** — extended by S4 below.
- **Ob.16 Categorical handoff readiness** — re-scoped by S5 (rebind) below: a standing row is handoff-ready *as substrate*, not as evidence.

**Ob.1 (Commissioning Gate) is replaced by S1**, because standing capture by definition has no Decision Frame to gate on.

## Standing-Capture Obligations (deltas)

### S1 — Standing Charter Gate (replaces Ob.1)

Standing capture has no Decision Frame, so it must be bound to an approved **Standing Capture Charter** instead. The charter is the boundary; workers, tools, and later continuations inherit it and must not silently expand it. Minimum:

- the **series** being captured (named indicator/observable, or named entity-aggregate) and its approved **source set / locators** (promoted via Candidate URL Intake where the locator came from discovery);
- the **declared cadence model**, its **caps**, and a **stop condition or review date** (S3);
- the **minimization rail** the series runs under (e.g. `business_entity_only` for org-motion; product/listing-scoped for indicators) — inherited from Ob.2, restated per series;
- the **purpose**: which recurring decision family the corpus is meant to feed (S7), so the standing capture is not free-floating collection.

The charter is a **gate, not a description.** Charter approval is **owner-gated** (the same owner gate that governs this contract); the approved charter is a **versioned artifact that proves authorization**; and a change to the series, source set, cadence, caps, or minimization requires a charter **revision**. Standing capture **has not started** — or **must stop** — whenever no current approved charter covers it. *(The exact charter record format stays an open knob; the owner-gated approval and the must-have-a-current-charter condition do not. AR-03.)*

Failure mode: standing capture with no charter is free-floating corpus collection — the exact thing v0's Ob.1 rejects — and has not started.

### S2 — Series Identity & Pinning

A corpus is only a series if its rows are comparable. Each observation must bind to a stable **series identity** and carry the pins that make re-observations comparable:

- the **series key** (target/product/listing + locator for indicators; `entity_key` for org-motion — the entity-resolution spine owns canonical identity, capture only carries it);
- the **comparability pins** the series depends on (e.g. locale/currency/access-method/exit-geo for a price or availability series; source + capture-posture tag for org-motion);
- a **cold-start marker** on the first observation of a series (the corpus before it is inherently limited; the inherent-limit cap is a visible fact, not a defect to hide);
- **pin drift is a visible re-pin event**, never silently absorbed: if a comparability pin changes (currency switch, exit-geo change, locator migration), the break in the series must be recorded so a later read does not treat a pin-induced jump as a real movement.

### S3 — Cadence As A Declared, Capped, Stop-Bounded Fact

Cadence is a first-class capture fact, not an implicit habit:

- the **cadence model** is declared (e.g. hourly/daily for demand indicators; periodic/annual for org-motion filings) with **caps** and a **stop condition or review date**; no standing series runs unbounded;
- **re-observation timing is decomposed** (Ob.8): the cadence is the *intended* rhythm; each row records its actual capture timing, and divergence (missed/late/extra samples) is visible;
- **manual-now; scheduler deferred (D3).** Until a separate build authorization grants a scheduler, the operative cadence is **manual/attended**, and the contract is explicit that "hourly/daily" is the *target* rhythm the manual posture does not yet truly meet — that **manual shortfall is itself a visible cadence fact**, recorded per series, not hidden. Authorizing a scheduler is **not** part of this contract, and this contract specifies **no** runtime, scheduler, entrypoint, or interface shape.

> **Non-binding future-compatibility note (NOT an obligation).** A manual-now / scheduler-later rollout may later find it convenient for both triggers to share one capture entrypoint — but designing or requiring any entrypoint, interface, or runtime shape is **runtime architecture owned by a later build authorization**, not this obligation contract. It is named here only as foregone context, per the contract's own no-runtime-design boundary and v0's "runtime design as this contract" rejection. *(AR-05.)*

### S4 — Append-Only Series Integrity (extends Ob.15)

- re-observations **supplement**, never overwrite; there is **no single mutating "current value" cell**;
- the Ob.15 re-capture relationship (`supersede` / `supplement` / `conflict` / `mixed`) is preserved per observation against the prior row;
- the **series-recapture diff** is preserved: what changed between consecutive observations is recoverable, not flattened into a latest-only snapshot;
- later successful access does not erase an earlier failed access, archive-attempt failure, fallback use, or prior-window uncertainty in the series.

### S5 — Rebind Gate (the exit to evidence)

This is the load-bearing carve-out, lifted from v0 and made the exit obligation:

- a standing observation or series is **not ECR-ready evidence**, and a standing row **never hands off to ECR directly**;
- **"rebound" is not a status label** that can be set on an existing corpus row. A row becomes ECR-ready **only** through a **commissioned recapture or rebind under a Decision Frame** that **re-discharges the v0 commissioned obligations (Ob.1–16)** for that frame — the observation re-enters the v0 contract and is captured/assessed there, not merely re-pointed-at;
- **checkable rebind gate** — before any corpus-derived material is treated as evidence, all three must exist: (a) a Decision Frame; (b) a v0-contract discharge for the rebound or freshly-recaptured observation under that frame; (c) an auditable corpus→evidence provenance link (which standing rows informed the frame, and whether a fresh recapture was triggered). Absent any one, the material stays substrate. *(The gate condition is bound here; only its ECR-side field representation is deferred — see Open Design Knobs — because defining ECR fields is a forbidden capture output. AR-01.)*
- until then the corpus is **decision-substrate that later commissioned reads draw from**, not pre-cleared evidence.

Ob.16 (categorical handoff readiness) is satisfied here **as substrate readiness** — the corpus is inspectable and its limits are visible — not as evidence readiness.

### S6 — Manipulability Flags Ride Forward (INV-1 preserved)

The demand substrate is hostile and manipulable; standing capture does not relax "flag, don't conclude":

- the series' integrity caveats are captured as **standing facts**: scarcity-theater for availability/restock, review-farm / J-curve for review velocity, attention-not-costly for search interest, promo-vs-permanent for price; official-vs-attended-fallback posture for org-motion;
- standing capture **records** these flags; it introduces **no weight, score, ranking, threshold, or judgment** (INV-1). Whether a flagged series is decision-useful is a downstream Judgment call, made at rebind, never by capture.

### S7 — Never-A-Feed Structural Lock

Per the buyer-proof packet's never-a-feed invariant, **every Orca output is a calibrated decision with an action ceiling — never a feed or stream**, including when a read is monitored over time (recurring engagement is sold as recurring *decisions*, never as a monitoring feed). The standing corpus is the place this invariant is most at risk, so the contract encodes it structurally:

- the corpus is **internal decision-substrate**; it must **not** be exposed, sold, or productized as a feed, stream, dashboard, alert subscription, or market-monitoring product;
- **behavioral boundary (not just naming):** corpus-derived material reaches any consumer — buyer, internal workflow, or downstream lane — **only** wrapped in a **calibrated decision with an action ceiling** (a Decision Frame or recurring-decision wrapper). **Periodic raw-series delivery, a dashboard, an alert/threshold subscription, a trend stream, or a market-monitoring view is barred regardless of what it is named** — feed-shaped *behavior* is the kill, not the word "feed." Recurring monitoring is delivered as recurring *decisions*, each with its own frame and ceiling; *(AR-02.)*
- outputs built on the corpus remain **calibrated decisions with action ceilings**; capturing a corpus hourly/daily is fine, **selling a feed is the kill** (it lands Orca on the "monitoring-only pull" kill and in the social-listening category the buyer-proof packet rejects);
- the corpus exists to feed **recurring decisions**; the obligation home must keep it decision-substrate, not product output.

## What This Supersedes (and what it does not re-spec)

On ratification, this contract becomes the **obligation home** for standing capture, superseding the **slice-scoped clarification** the company-aggregate lane made for itself (`company_aggregate_forward_signal_capture_lane_scope_decision_v0.md`, "Standing-capture obligation home" section), whose own `stale_if` anticipates exactly this ("a standing/corpus-capture obligation contract is accepted"). The clarification's content is consistent with this contract (existing v0 obligations + rebind rule + append-only) and is subsumed, not contradicted.

It does **not** re-spec what those lanes own:

- it does **not** redefine the org-motion **observation record shape**, its **official-first source selection**, its adapter set, or its `entity_key` resolution — those stay owned by the company-aggregate decision and the entity-resolution spine;
- it does **not** redefine the **demand-indicator capture profiles** or the keystone durability delta's elements — those stay owned by their profiles; this contract governs *that they are captured standing under these obligations*, not *which series to capture*;
- it does **not** amend the **v0 commissioned obligation contract** file (D2: sibling, not amendment); v0's standing carve-out already points here.

## Forbidden Outputs From Standing Capture

In addition to all v0 forbidden outputs (credibility labels, integrity classifications, discounting/exclusion decisions, Signal-Use Classification, Decision Strength, Action Ceiling, semantic dedupe/clustering, Cleaning transformations, ECR field architecture, source-quality scores, runtime plans), standing capture must not emit:

- a **derived trend score, momentum index, or ranking** over the series (that is Judgment, made at rebind);
- a **threshold/alert** that fires a decision automatically from the series (that is a feed/automation, barred by S7);
- a **"current value"** that silently overwrites series history (barred by S4);
- **discovery output** — new venues/locators are Candidate URL Intake's, not this contract's.

## Rejected Patterns

- standing capture without a charter (free-floating corpus collection);
- treating standing rows as ECR-ready evidence without rebind (S5);
- a sold feed / monitoring product / dashboard subscription over the corpus (S7);
- a single mutating "current value" cell instead of an append-only series (S4);
- pin-induced series breaks absorbed silently as real movement (S2);
- scheduler/runtime build smuggled in as "the cadence obligation" (S3 — scheduler is a separate authorization);
- standing capture as a second venue-discovery spine (deconflicted; that is the pre-capture discovery charter's question);
- paper contract hardening before standing-capture pressure tests (below).

## Pressure-Test Requirement (not hardened)

Per the v0 doctrine ("do not harden this contract from abstract reasoning alone"), this contract must **not** be treated as hardened until pressure-tested against the two real standing-capture lanes:

- at least one **demand-durability indicator** series (e.g. a price or availability series with promo-vs-permanent and exit-geo pin risk), exercising S2/S3/S4/S6;
- the **company-aggregate org-motion** series (entity-keyed, official-first, attended-fallback posture), exercising S1/S2/S4/S5;
- one **rebind** of a standing series into a commissioned Decision-Frame capture, exercising S5 end-to-end.

Pressure-test each against: whether the charter (S1) was sufficient to start; whether series identity/pins (S2) held across re-observation; whether cadence (S3) was bounded and decomposed; whether append-only integrity (S4) survived a conflicting re-observation; whether rebind (S5) produced auditable corpus→evidence provenance; whether manipulability flags (S6) rode forward without becoming judgment; and whether the never-a-feed lock (S7) held. Tighten, relax, split, or move obligations to satellite only after failures are compared.

**Closure criteria — a pressure test passes only on observed evidence, never on a reviewed example** *(AR-04)*:

- **S1** passes iff a real charter gated a real standing run **and** an attempted run with no current approved charter was actually refused/stopped.
- **S2** passes iff a forced pin change (e.g. currency or exit-geo) produced a recorded re-pin break **and** a later read did not treat that break as real movement.
- **S4** passes iff a conflicting re-observation supplemented (did not overwrite) the prior row **and** the series-recapture diff is recoverable.
- **S5** passes iff a standing series rebound into a Decision Frame produced an auditable corpus→evidence provenance link **and** a pre-rebind direct-to-ECR handoff attempt was refused.
- **S6** passes iff a manipulability flag rode forward as a fact with **no** weight, score, or verdict attached.
- **S7** passes iff a corpus-derived deliverable was refused/blocked when shaped as a feed/dashboard/alert **and** accepted only inside a calibrated-decision wrapper.

A pressure test **fails** when its closure evidence is absent, narrative-only, or contradicted; a failed test **blocks any hardening claim** for that obligation. "Reviewed examples" are **not** pressure-test evidence.

## Open Design Knobs (carried, not decided)

- whether a standing series needs a **minimum re-observation interval floor** to avoid churn while preserving meaningful change (the v0 recapture-threshold knob, applied to cadence);
- where the **series-recapture diff** is computed and stored (capture vs a later consolidation) without becoming an ECR/storage design;
- how a **charter** is recorded and versioned (and whether charter approval is owner-gated per series or per source-family);
- whether **scheduler authorization**, when sought, is per series, per lane, or global (deferred; high-lock-in);
- the ECR-side **representation** of the rebind provenance (corpus rows → commissioned recapture) — how it is stored as ECR fields — without defining ECR fields here (the rebind **gate condition** itself is bound in S5, not deferred).

## Non-Claims

This contract does not prove or authorize validation, readiness, hardening, source-of-truth promotion, buyer proof, repeatable demand, product/feature/implementation/commercial readiness, source-system feasibility, data rights, or runtime feasibility; ratification accepts the obligation set but is **not** a pressure-test pass. It authorizes no implementation, scheduler, runtime, source access, storage, dashboard, automation, scraper, API, or ECR/Cleaning/Judgment design. It does not amend the v0 obligation contract, the source-access boundary, the Candidate URL Intake contract, or the company-aggregate decision; it is the standing-capture sibling those surfaces already point to. INV-1 is preserved: no weight, score, ranking, threshold, or judgment is introduced.

## Direction Change (ratified 2026-06-15; propagated 2026-06-15)

```yaml
proposed_direction_change:
  status: ratified_2026_06_15
  what_changed_on_ratification: >
    Creates the standing-capture / Corpus Intake obligation contract that the v0
    commissioned Data Capture obligation contract routes standing/opportunistic
    capture out to. On ratification this becomes the obligation home for standing
    capture, superseding the company-aggregate lane's slice-scoped clarification
    and giving the demand-durability indicators their standing-capture home, under
    D1=general + D3=scheduler-deferred.
  trigger_if_ratified: product_doctrine
  propagation_performed: done
  reason_propagation_done: >
    Owner-ratified 2026-06-15. Propagation to the controlling surfaces below was
    performed 2026-06-15 (additive registration/pointer edits only, no obligation
    change): the v0 commissioned obligation contract now names this ratified
    sibling; the company-aggregate decision records this contract as the
    superseding obligation home (its stale_if fired); the Data Capture Spine lane
    thesis references this contract as the standing-capture obligation home (its
    stale_if fired); the Data Capture Spine consolidation map registers the
    standing-capture layer + this contract; and the Orca repo map indexes it.
  surfaces_to_update_on_ratification:
    - path: docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
      change: Its standing-capture carve-out / stale_if can name this contract as the now-existing sibling (no obligation change).
    - path: docs/decisions/company_aggregate_forward_signal_capture_lane_scope_decision_v0.md
      change: Its slice-scoped clarification is superseded as obligation home (its stale_if already anticipates this).
    - path: docs/product/data_capture_spine/data_capture_spine_lane_product_thesis_v0.md
      change: Its stale_if ("Orca authorizes standing or opportunistic corpus capture") fires; the thesis is updated to reference this contract.
    - path: docs/workflows/data_capture_spine_consolidation_map_v0.md
      change: Register the standing-capture layer + this contract (a discoverability pass, deferred like the sibling lanes deferred theirs).
    - path: docs/workflows/orca_repo_map_v0.md
      change: Index the new contract.
  updated_on_ratification:
    - path: all of the above
      reason: Propagated 2026-06-15 via additive registration/pointer edits; referrers now resolve to this file by path.
  non_claims:
    - not validation
    - not readiness
    - not contract hardening
    - not pressure-tested
    - not a build/scheduler/runtime/source-access authorization
```
