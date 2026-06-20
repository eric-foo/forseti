# Prospective Decision Loop — Target Architecture v0 (operational "far half")

```yaml
retrieval_header_version: 1
artifact_role: PROPOSED target architecture (planning artifact; pending owner review — selects nothing into doctrine, builds nothing, ratifies nothing)
scope: >
  Target architecture, dependency map, core/satellite boundary, and sequenced
  roadmap for Orca's operational decision loop: the layer that makes a LIVE
  decision process (DecisionEvent) instrumented, governable, and learnable (decision object,
  shadow mode, assisted mode, action feedback, decision memory, minimal
  governance, learning loop), beyond the retrospective backtest harness and the
  near-half postmortem/lesson loop.
use_when:
  - Deciding whether to adopt, amend, or reject the prospective-decision-loop target.
  - Planning any shadow-mode, assisted-mode, or live-decision instrumentation work.
  - Checking what may be built before a real counterparty decision exists.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md
  - orca/product/spines/judgment/conductor/conductor_construction_integrity_probe_addendum_v1.md
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
branch_or_commit: prospective-decision-loop-architecture-v0 @ f3f0609 (worktree off origin/main; b463c3c verified ancestor)
stale_if:
  - The near-half plan (adversarial-postmortem -> validated-lesson-library -> signal-reliability ledger) lands as a durable artifact (reconcile the decision-memory interface here against it).
  - The owner ratifies, amends, or rejects this target (ratification carries its own propagation; this becomes historical).
  - First real counterparty contact (the decision-object v0 vocabulary must be re-validated against a real decision stream before any build).
  - Evidence-ladder tiers, closeout states, or the conductor firewall doctrine change.
```

## Status

`PROPOSED` — planning artifact only, product-learning tier. This is a **target,
not a capability claim**. It enacts no gate, schema, or protocol; it routes
every owner-territory change out to the owning source. No integration layer,
runtime, or schema code is authorized by this artifact.

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_prospective_loop_architecture (S0 + decision-routing + validation-gates + retrieval-metadata + the three named judgment-spine/decision sources + PR-flow doctrine)
  edit_permission: docs-write
  target_scope:
    - orca/product/spines/judgment/learning_loops/far_half/prospective_decision_loop_target_architecture_v0.md (new, this file only)
  dirty_state_checked: yes
  blocked_if_missing: no
  dirty_or_untracked_notes:
    - Worktree is fresh off origin/main @ f3f0609; clean at start of work.
    - The commissioning prompt cited main @ b463c3c; verified an ancestor of origin/main, so the load contract's sources were re-read at f3f0609.
    - The near-half plan has NO durable artifact in the repo (rg for signal-reliability ledger / lesson-library / adversarial-postmortem: no hits). Treated as an oriented summary per the commission; the decision-memory layer below binds to it as a named pending interface, not as authority.
```

## The Architecture Question

Orca's judgment program currently has (a) a retrospective backtest harness —
blind judgment on frozen historical decision packets, scored against sealed
outcomes, governed by the evidence ladder and the conductor firewall — and (b)
a near-half plan for an adversarial-postmortem -> validated-lesson-library loop
populating a signal-reliability ledger. The question this artifact answers:

**What is the target architecture for the operational layer — the one that
instruments a LIVE decision process so Orca's judgment is exercised, governed,
and improved on decisions whose outcomes do not yet exist — and in what order
can it be built so that nothing is constructed ahead of a real counterparty?**

The main goal is a harness for making **better decisions**, not a wider archive
of scored past decisions: every component below must either improve a future
sealed call or be cut.

## The Structural Insight That Drives The Design

In the retrospective harness, the hardest engineering problem is manufacturing
blindness after the fact: packet freezes, leakage reviews, memorization
screens, tell-audits — all because the outcome already exists somewhere and
must be kept out.

**A live decision gets the blind seal for free.** At recommendation time,
nobody — not the org, not the operator, not the model — holds the outcome (Outcome),
because it has not happened. Prospective evidence is therefore structurally
cleaner at the moment of creation than any backtest can ever be.

The firewall risk does not disappear; it **moves** to three new places:

1. **Disclosure.** The moment Orca's recommendation is shown to the decision
   owner, the org's subsequent path is influenced. The "actual path"
   comparator — the thing a forecast is scored against — is no longer
   Orca-independent.
2. **Resolution.** Whoever scores the sealed call against the outcome is
   outcome-aware by necessity. If "what counts as the outcome" is decided at
   scoring time, the score is motivated reasoning in receipt form.
3. **Post-hoc editing.** A recommendation that can be revised after outcome
   information starts arriving is not a forecast.

Every load-bearing choice below is one of these three risks, closed:
**seal-before-disclose** (the firewall translated to live operation),
**pre-specified mechanical resolution** (outcome criteria, metric, and window
fixed inside the sealed call itself), and an **append-only seal registry**
(amendments are new sealed entries, never edits). These are the live analogs
of the conductor's blind-pre-reveal-only rule, the JSG-08 reveal mechanics, and
the dated-amendment-only ledger discipline — the doctrine carries over rather
than being reinvented.

## Target Architecture (AO-1: one spine, two evidence routes, shadow default)

One decision-object spine serves both modes. The **mode is a pre-declared
per-decision property** — a disclosure switch — not a product split. The two
modes yield categorically different evidence and route to different ladder
tracks; that separation is the firewall, so they are never merged into one
default mode (see "Should Shadow And Assisted Be One Mode?" below).

### 1. Decision object (schema vocabulary v0 — a docs contract, not code)

```yaml
decision_object_v0:
  identity:
    decision_id:
    decision_family:           # keys decision-memory priors and lesson routing
    counterparty:              # org name, or "orca-internal" for dogfood decisions
    decision_owner:            # the human who owns the real decision
    intake_timestamp:
  mode:
    declared_mode: shadow | assisted   # pre-declared at intake, before seal; dated amendment only
  frame:                       # a genuine decision brief — decision-framing, never test-framing (R5 carries over verbatim)
    question:
    options_considered:
    constraints:
    decision_deadline:
    information_set_ref:       # snapshot/hash of everything Orca could see at seal time — the live analog of the backtest cutoff
  sealed_call:                 # the ONLY scoreable forecast for this decision (firewall)
    recommendation:            # option + action shape
    confidence_band:           # reuses the contestant band-claim shape, not a new vocabulary
    expected_outcome:          # metric + band + measurement window — REQUIRED; without it the object is unscoreable by design
    resolution_criteria:       # pre-specified and mechanical; resolution may apply them, never author them
    leading_indicators:        # observable signal + expected direction + check window
    kill_or_adjust_triggers:   # pre-committed conditions under which the call should change
    signals_used:              # each tagged with a signal_id — the live form of the batch-1 signal pre-commitment; feeds the reliability ledger
    assumptions:               # enumerated load-bearing assumptions, each individually resolvable (held / failed / untested)
    lessons_consulted:         # decision-memory citations with retrieval handles (closes the learning loop; see below)
    reasoning_trace:           # required — the JSG-06 analog; doubles as the lesson-extraction and audit surface
    seal:
      content_hash:
      seal_timestamp:
      sealing_actor:           # subagent-delegation norm where feasible (R2 by-hand form carries over)
  disclosure:                  # assisted mode only; structurally empty in shadow
    disclosed_to:
    disclosure_timestamp:      # invariant: strictly after seal_timestamp
    owner_response: accepted | modified | rejected
    owner_response_reasons:
    modification_delta:        # what the owner changed — the highest-value assisted-mode learning surface
  actual_path:                 # passive observation; in shadow mode the org never sees the sealed call
    org_decision:
    org_decision_timestamp:
    divergence_from_recommendation:
  updates: []                  # optional mid-flight re-seals before the relevant outcome/resolution signal is known; each is its own sealed call scored against its own information_set_ref; never an edit or replacement of an earlier scoreable call
  resolution:
    outcome_record:            # what happened, recorded against resolution_criteria
    score:                     # mechanical application of the pre-specified criteria
    indicator_outcomes:        # did the leading indicators actually lead
    trigger_outcomes:          # did pre-committed triggers fire, and would firing have been correct
    assumption_outcomes:       # held | failed | untested, per enumerated assumption
    resolution_actor:
    resolution_timestamp:
  learning_extraction:
    signal_reliability_rows:   # -> near-half signal-reliability ledger (consumed there, not validated here)
    lesson_candidates:         # -> near-half adversarial postmortem (validation owned there)
    calibration_row:           # confidence_band vs outcome, accumulated across decisions
  integrity:
    firewall_state: clean | breached_quarantined
    breach_note:               # a confirmed breach names its gate, exactly like blocked_or_contaminated
```

The schema is **vocabulary**: it is specified now as a docs contract and
exercised by hand; it is not built as code, storage, or tooling by this
artifact. An intake gate applies: a decision whose outcome criterion cannot be
pre-specified is admitted as **unscoreable-by-design** — loggable for decision
memory, permanently excluded from calibration and from any judgment claim.

### 2. Shadow mode (the judgment-evidence route)

Orca seals a recommendation before the org decides; the org acts normally,
unaware of the sealed call; Orca later compares forecast + suggested action to
the actual path and resolves against the pre-specified criteria.

Why this yields prospective evidence **without a customer-facing product**: the
entire mode is passive. Nothing is shown to anyone; no UX, no integration, no
writeback exists or is needed. The deliverables are sealed entries in a
registry and resolution records — by-hand artifacts. The comparator (the org's
uninfluenced path plus the realized outcome) is supplied by reality, not by a
product surface. Shadow mode is the live analog of the backtest with the
packet-construction problem deleted.

The unique value of shadow mode is the **divergence read**: org did X, Orca
sealed Y, the outcome favored one of them. That three-way comparison is the
richest learning surface in the whole loop and it only exists while the
comparator is uncontaminated — which is the core argument for shadow-first
sequencing and for never merging the modes.

Named residuals (disclosed, not gated, consistent with owner decision 4 on the
single-operator memory leak): (a) intake itself can perturb — asking an org for
decision context may change the decision; minimized by passive intake, never
zero; (b) in dogfood operation the same human may be decision owner and Orca
operator, so "sealed but not disclosed" is porous via memory. Mitigation norm:
the sealing actor is an **org-blind subagent** that authors the sealed call
from the decision brief (R2's by-hand form, reused), and the residual is
recorded at product-learning tier.

### 3. Assisted mode (the adoption-evidence route)

The sealed recommendation is disclosed to the decision owner **after sealing**;
the owner's response (accept / modify / reject + reasons) and the realized
outcome are logged.

How the firewall survives a human and an outcome in the loop:

- **The seal precedes disclosure, always.** The pre-disclosure sealed call is
  the only entry with forecast standing. Anything Orca produces after
  disclosure — clarifications, revisions, defenses — is commentary at a lower
  tier, exactly as everything post-reveal is lower-tier in the conductor.
- **Disclosure burns the comparator, and the record says so.** Once the owner
  has seen the call, the realized path includes Orca's influence. The sealed
  call is still scored against the realized outcome, but the result is
  **influenced-path calibration** — never counterfactual accuracy ("the org
  did better because of Orca" is unclaimable from inside one assisted
  decision), and never clean prospective-judgment evidence. The structural
  reason: outcome-USE contamination generalizes — here it is the org using the
  call, not the contestant using the outcome, but the same rule applies: the
  evidence is quarantined *as judgment evidence* while remaining fully valid
  *as adoption evidence*.
- **Adoption evidence routes through the existing buyer-proof surface.** A
  qualified decision owner using an Orca recommendation in a live allocation
  decision, with readback, is a `buyer_proof` typical surface, but it is not
  buyer proof until the complete buyer-proof receipt is satisfied. No new
  promotion path is needed: assisted-mode evidence promotes only through the
  existing product-proof gates (`.agents/workflow-overlay/product-proof.md`) and
  the ladder's buyer-proof receipt, including the memo/evidence appendix,
  readback or use signal, trust state, pull-versus-praise classification, and
  commercial-next-step signal where claimed.
- **Mode is declared at intake, not after.** Post-hoc mode assignment would be
  a cherry-pick channel (disclose-and-count only the calls that look good).
  The pre-declared decision ledger and report-all rule close it.

### 4. Should shadow and assisted be one default mode? (commissioned question)

**One spine, two modes, shadow default — not one merged mode.**

- **Merging is a firewall breach by construction.** A single always-disclose
  mode makes every comparator Orca-influenced; prospective judgment evidence
  never rises above influenced-path calibration, and the divergence read —
  the loop's best learning surface — never exists. This is precisely "weaken
  the firewall to make the loop look more capable," which the commission and
  the doctrine forbid.
- **The ladder already separates the two evidence types.** Shadow output is
  judgment-track (prospective analog of the backtest); assisted output is
  product/buyer-track. One merged mode would invite re-using adoption evidence
  as forecast verification — the exact cross-tier reuse the ladder exists to
  block.
- **What the "one mode" intuition gets right is real and is honored**: one
  decision object, one seal protocol, one resolution protocol, one registry,
  one governance model. The modes differ by exactly one bit — whether
  disclosure happens — plus the evidence routing that bit implies. Per
  decision, the relationship is one-way and irreversible: a sealed call can
  stay dark (shadow) or be disclosed (assisted); it can never be un-disclosed.
  That asymmetric reversibility is itself the argument for shadow as the
  default state of every new decision: shadow keeps both futures open.

### 5. Action feedback (beyond "was the prediction right")

Resolution captures, per decision: usability (could the owner consume the call
at all — assisted only), the modification delta (what the owner changed, and
whether the modification out- or under-performed the sealed call where
distinguishable), which metric moved against the expected-outcome band, which
enumerated assumption failed, whether leading indicators actually led (lead
time, false positives), and whether kill/adjust triggers fired correctly. The
assumption ledger inside the reasoning trace is what makes the loop learnable
rather than merely scored: a wrong call with three named failed assumptions is
worth more than a right call with none.

### 6. Decision memory (consumer, not owner)

Decision memory is a **read-side projection**, not a new store of truth: the
query surface over (validated lesson library + signal-reliability ledger +
resolved decision objects), keyed by `decision_family`. The near half owns
lesson validation and the reliability ledger; this loop only (a) **emits**
signal-reliability rows and lesson candidates at resolution, and (b)
**consumes** validated lessons at seal time via `lessons_consulted` citations.

Interface contract this loop needs from the near-half ledger (pending — the
near-half plan has no durable artifact yet; reconcile on landing): per signal,
a stable `signal_id`, applicable `decision_family`, reliability evidence with
provenance, validation status, and a staleness marker. Until that lands, the
fields above are the named dependency, not an invented ledger.

### 7. The learning loop (how this makes future decisions better)

The loop closes through four channels, each with a named owner:

1. **Signal reliability** (near-half owned): `signals_used` is pre-committed at
   seal; resolution emits per-signal outcome rows to the reliability ledger.
   The live loop is the ledger's prospective data source — the K-of-N
   report-all honesty rule carries over ("signal S moved the call in K of N
   pre-committed decisions"), so signal claims can never be cherry-picked.
2. **Assumption -> lesson candidates** (near-half validates): failed
   assumptions from resolution route into the adversarial postmortem; only
   validated lessons enter decision memory.
3. **Calibration** (this loop owns): confidence-band vs outcome accumulates
   across resolved decisions into calibration curves per decision family.
   Needs N; honest at small N only as product-learning.
4. **Lesson efficacy — the meta-loop** (this loop owns the citation, the near
   half owns the verdict): because every sealed call cites `lessons_consulted`,
   resolution scores not only the call but the lessons used by it. A lesson
   whose citations correlate with worse calls is itself a candidate for
   demotion. This is what makes the memory self-correcting instead of
   monotonically growing.

The non-negotiable boundary: the operational loop **generates** learning inputs
and **consumes** validated outputs; it never validates its own lessons. The
adversarial step lives in the near half — keeping generation and validation in
separate lanes is the same de-correlation discipline the review lanes use.

### 8. Minimal governance for institution-grade trust

Five mechanisms, no more (each closes a named failure; anything beyond these is
bloat at this horizon):

1. **Append-only seal registry.** Every sealed call: content hash + timestamp,
   append-only. Amendments are new sealed entries superseding by reference —
   never edits. (Closes post-hoc editing; this is dated-amendment-only,
   generalized.) Lineage = the registry chain per decision_id.
2. **Three permissioned actions: seal, disclose, resolve.** Who may do each is
   recorded per decision. At pilot tier these may be one human plus a sealing
   subagent — the single-operator residual is disclosed, not gated.
3. **Replay.** A resolved decision must be recomputable by a third party from
   (information_set_ref, sealed_call, outcome_record) alone. If the score
   cannot be re-derived mechanically, the resolution is defective. (The
   derivability doctrine, carried over.)
4. **Pre-declared ledger + report-all.** Decisions enter a pre-declared intake
   ledger; every intaken decision is reported at resolution — including
   unscoreable, abandoned, breached, and embarrassing ones. Selective
   reporting voids the loop's evidence the same way it voids a batch.
5. **Escalation = quarantine, recorded-as-data.** A confirmed firewall breach
   (disclosure before seal; outcome information inside the sealing actor's
   information set; resolution criteria authored or altered post-outcome)
   routes the decision to `breached_quarantined` with the breach named. Never
   deleted — breaches are data (owner decision 2, carried over).

Explicit governance non-goal: **no action writeback.** Orca recommends; the
org executes. "Executable" at this horizon means the org can execute against
Orca's pre-committed triggers and indicators — not that Orca touches real
systems. Writeback is a separate far-future authorization with its own
governance, and excluding it is what keeps this governance set minimal.

### 9. Evidence-ladder integration (own promotion path, existing vocabulary)

This architecture mints **no** tier, closeout state, or ladder vocabulary.

- **Shadow route:** resolved shadow decisions are prospective judgment evidence
  capped at **product-learning** until a prospective gate family clears.
  By-hand seals and resolutions are the live analog of the manual execution
  surface, which is permanently non-gate-clearing per the pre-sale execution
  evidence-tier policy — so the cap is structural, not a formality.
- **Assisted route:** adoption evidence classifies under the existing
  `buyer_proof` receipts and product-proof gates only when the decision owner is
  a qualified external buyer in a live allocation decision and the complete
  buyer-proof receipt is satisfied; otherwise it is product-learning. Its sealed
  pre-disclosure call contributes influenced-path calibration at
  product-learning only.
- **Routed-out (ladder owner enacts, nothing here clears anything):** a future
  **prospective gate family** — requirements sketch: pre-registered decision
  ledger; seal receipts with hash + timestamp + sealing-actor separation;
  information-set boundary evidence; mechanical resolution against
  pre-specified criteria; pre-declared N with report-all; replayability. Until
  the ladder owner authors those gates, every prospective claim closes at the
  weakest cleared gate, and a run with no durable seal/resolution receipts is
  `no_durable_evidence` — the sub-floor rule applies unchanged.

## Architecture Option Ledger (compact)

- **AO-1 — One spine, two modes, seal-first (RECOMMENDED).** As above. Wins on:
  firewall preserved by construction; doctrine reuse (every mechanism is an
  existing rule translated, not invented); one schema/governance set; shadow
  default keeps both evidence futures open per decision. Loses on: two evidence
  routes must be policed (mode pre-declaration is load-bearing).
- **AO-2 — Two separate products (shadow harness and assisted advisor as
  independent layers with separate objects).** Wins: maximal isolation. Loses:
  duplicates schema, registry, governance; loses the sealed-pre-disclosure
  calibration record in assisted mode; 2x maintenance for a boundary AO-1 gets
  from one declared bit plus routing rules. Rejected as oversized.
- **AO-3 — One merged default mode (always disclose, log, score).** Wins:
  simplest story. Loses: burns the comparator on every decision; prospective
  judgment evidence permanently capped at influenced-path calibration; opens
  cross-tier reuse of adoption evidence as forecast verification. Rejected as
  a firewall breach by construction.
- **AO-4 — Oracle-only extension (no operational layer; seal forecasts on
  PUBLIC live decisions — e.g., a brand announces a repricing and Orca seals an
  outcome call before outcomes are observable — resolved later from public
  data).** Wins: prospective evidence with zero counterparty, zero integration;
  the live analog of the backtest. Loses: no decision owner, no action
  feedback, no adoption evidence; it is exactly the "pure prediction oracle"
  the goal says to go beyond. Not selected as the target — but its mechanism is
  sound and counterparty-free, so it is folded into the roadmap as the optional
  Phase 1b public-event shadow ledger.
- **AO-5 — Defer everything until a counterparty exists.** Wins: zero
  speculative spec risk. Loses: the firewall is the one thing that cannot be
  improvised at counterparty-arrival; schemas and protocols are cheap,
  counterparty-independent, and falsifiable by dogfood before any external
  contact. Rejected; its instinct (build no code, no integration) is fully
  preserved — Phases 0–1 are docs and by-hand operation only.

## Core / Satellite Boundary

Core (case- and counterparty-agnostic; stable across engagements):

- decision-object schema vocabulary and the unscoreable-by-design intake gate;
- seal-before-disclose invariant and the append-only registry semantics;
- mode vocabulary (shadow | assisted), pre-declaration rule, and the two
  evidence routes with their ladder mappings;
- mechanical-resolution discipline (criteria pre-specified inside the seal);
- the learning-loop interfaces: signals_used pre-commitment, assumption
  ledger, lessons_consulted citations, and the emit/consume boundary with the
  near half;
- the five governance mechanisms and the no-writeback boundary;
- quarantine-as-data breach handling.

Satellite (per counterparty / per decision; never hardened into core):

- every decision instance, domain metric, and outcome-adjudication source;
- counterparty identity, org context, owner identities, and intake channel;
- disclosure medium and any future assisted-mode UX;
- decision-family priors and the domain content of decision memory;
- integration, data feeds, and (far-future, separately authorized) writeback.

This mirrors the ladder's own split ("the evidence ladder is case-agnostic;
Daimler remains satellite"): the loop's core is a claim-and-protocol
architecture; everything that touches a real org is satellite by definition.

## Dependency Map (central deliverable)

### Now-specifiable with NO counterparty (docs + by-hand only)

| # | Item | Why counterparty-independent |
| --- | --- | --- |
| N1 | Decision-object schema spec (v0 vocabulary above, refined) | Pure vocabulary; falsifiable by dogfood before external contact. |
| N2 | Seal/disclosure protocol (registry semantics, seal-before-disclose, update re-seals) | A protocol over artifacts Orca authors itself. |
| N3 | Resolution protocol (mechanical scoring, unscoreable-by-design gate, quarantine routes) | Defined entirely by the sealed call's own pre-specified fields. |
| N4 | Shadow comparison protocol (divergence taxonomy: org-call vs sealed-call vs outcome) | Comparison rules, not data. |
| N5 | Governance note (five mechanisms, three permissions, no-writeback boundary) | Governs Orca-side conduct only. |
| N6 | Evidence-route mapping + routed-out prospective-gate-family requirements (ladder owner enacts) | Claim architecture; the ladder is already case-agnostic. |
| N7 | Decision-memory interface contract (fields needed from the near-half ledger) | An interface declaration; binds nothing until the near half lands. |
| N8 | Internal dogfood shadow pilot ledger (pre-declared N of Orca-internal decisions, by-hand) | Orca's own operating decisions are real live decisions with real outcomes; requires owner sign-off but no external party. |
| N9 | (Optional) Public-event shadow ledger (AO-4 mechanism as an evidence stream) | Public decisions + public outcomes; zero integration. |

### Counterparty-BLOCKED (must not be built until a real decision/org exists)

| # | Item | Reason for the block |
| --- | --- | --- |
| B1 | Live data integration / indicator feeds | Feed shape is unknowable without the org's systems; any generic connector is speculative infrastructure around an unproven assumption (complex-regime rule). |
| B2 | Assisted-mode disclosure UX | The owner's real workflow surface determines the UX; building first = lock-in plus invented requirements. |
| B3 | Owner-response capture mechanics | The schema (N1) is ready; the capture channel depends on the counterparty's medium. |
| B4 | Domain outcome-adjudication sources | What data resolves "did demand shift" is the counterparty's metric reality. |
| B5 | Action writeback into real systems | Out of scope even WITH a counterparty until a separate authorization; highest-lock-in, highest-trust-burden component. |
| B6 | Prospective gate-family CLEARING | Requirements are draftable (N6); clearing needs real external decisions at pre-declared N. |
| B7 | Domain-level decision-memory population | Priors require resolved decisions in the target domain; dogfood populates loop-mechanics lessons only. |
| B8 | Any schema-as-code, storage, or tooling build | No implementation authorization exists; v0 vocabulary must survive dogfood + first counterparty contact first. |

The map's invariant: **every now-item is docs or by-hand operation; every
build-item is blocked on a counterparty or a separate authorization.** Nothing
is constructed ahead of the thing that would tell us it is wrong.

## Sequenced Roadmap

- **Phase 0 — Specify (now; docs-only; this PR + successor spec slices).**
  This target architecture for owner review; then N1–N7 as one or two spec
  artifacts (smallest complete slices, each its own lane/PR).
- **Phase 1 — Dogfood shadow (no counterparty; by-hand; separate owner-signed
  ledger, modeled on the batch-1 declaration).** Pre-declare a small N of
  Orca-internal operating decisions; org-blind subagent seals calls; owner
  decides normally; resolve mechanically; emit the first calibration rows,
  signal rows, and lesson candidates. Purpose: falsify the schema and protocols
  cheaply. Named residuals: single-operator memory bridge; non-target domain
  (loop-mechanics learning only). **Phase 1b (optional, parallel):** the
  public-event shadow ledger (N9) for counterparty-free prospective evidence in
  the target domain.
- **Phase 2 — External shadow (counterparty-gated).** Trigger: a named org +
  decision stream + owner agreement. The org acts normally; Orca seals and
  resolves. Unlocks B1/B4 narrowly (only the feeds this org's decisions need),
  B7 (real-domain memory), and first B6 clearing attempts.
- **Phase 3 — Assisted (counterparty-gated; shadow record as prerequisite).**
  Trigger: pre-declared baseline of resolved shadow decisions with this
  counterparty + owner decision to disclose. Unlocks B2/B3. Adoption evidence
  flows to the existing buyer-proof path. Sequencing rationale: disclosure is
  irreversible per decision; shadow-first preserves the clean comparator while
  trust is being earned, and the resolved shadow record is a post-resolution
  trust artifact ("here is what we sealed before you decided, and how it
  resolved"). That presentation does not populate the original shadow decision's
  assisted-mode `disclosure` fields, retroactively reclassify its evidence, or
  turn it into a buyer-proof receipt.
- **Phase 4 — Integration/writeback (out of scope).** Separate authorization,
  separate governance; named here only so its exclusion is visible.

Is this sequencing wrong anywhere? The honest stress point is Phase 1's value:
dogfood decisions are low-stakes and self-referential, so its calibration
output is weak. It is kept because its purpose is **protocol falsification**
(does the schema survive contact with real intake, sealing, resolution?), not
evidence accumulation — and Phase 1b exists precisely to supply
target-domain prospective evidence without waiting for an org.

## Smallest First Move Buildable Without A Counterparty

**The Phase-0 spec slice: one artifact carrying N1 + N2 + N3 (decision-object
schema + seal protocol + resolution protocol), authored as a docs contract with
a worked dogfood example.** It is the single unit everything else consumes; it
is pure vocabulary/protocol (zero lock-in beyond a v0 doc); and it converts
this target architecture into something a Phase-1 pilot can actually run.
Second move, gated only on owner sign-off (not on any counterparty): the
Phase-1 dogfood shadow ledger declaration, modeled clause-for-clause on the
batch-1 ledger (pre-declared list, report-all, dated-amendment-only).

## Risks And Residuals (adversarial findings, kept visible)

- **Speculative-schema risk:** v0 vocabulary may not survive real decisions.
  Mitigated by dogfood-first and the `stale_if` on first counterparty contact;
  the schema is deliberately a doc, not code.
- **Single-operator porosity (dogfood):** same human decides and operates;
  sealed-but-undisclosed is bridgeable by memory. Disclosed residual at
  product-learning tier; org-blind sealing subagent as the working norm.
- **Resolution-criteria gaming:** criteria authored vaguely at seal time make
  resolution judgment-shaped again. The unscoreable-by-design gate plus replay
  requirement are the controls; a criteria-quality rubric is deferred to the
  Phase-1 pilot's distillation (the batch-1 pattern: measure first).
- **Observer effect at intake (shadow):** asking for decision context can
  change the decision. Passive intake minimizes; residual named, not solved.
- **Counterfactual overclaim (assisted):** influenced-path calibration must
  never be narrated as "Orca improved the outcome." The route's claim cap is
  the control; this is the loop's most tempting future overclaim.
- **Ledger-interface drift:** the near-half plan is not durable; N7 may need
  rework when it lands. Accepted: an interface declaration is cheaper to amend
  than a re-invented ledger is to merge.

## What Would Change The Recommendation

- The near-half plan landing with a materially different ledger shape (N7 and
  the learning-loop channels re-derive).
- An owner decision that the first counterparty will be assisted-first (e.g., a
  buyer who will not host a silent shadow phase) — AO-1 survives but the
  shadow-default and Phase-2/3 ordering invert, and the judgment-track evidence
  plan must be rebuilt around Phase 1b.
- The conductor addendum failing ratification in a way that retires the
  firewall vocabulary this design translates.
- Evidence that pre-specified mechanical resolution is unachievable for the
  target decision families (would force a judged-resolution design with
  actor-separation gates — a materially different, heavier governance model).

## Non-Claims

- Planning artifact only; product-learning tier; a target, not a capability
  claim. Not Palantir-parity and not a parity roadmap.
- Builds nothing; authorizes no implementation, integration, schema code,
  storage, UX, pilot, or writeback. Phase 1 requires its own owner-signed
  ledger; Phases 2–3 require counterparties that do not exist.
- Mints no evidence-ladder tier, closeout state, or claim vocabulary; clears no
  gate; the prospective gate family is a routed-out requirements sketch for the
  ladder owner, `indeterminate_until_authored`.
- Does not weaken the firewall or any ladder cap; does not ratify the conductor
  addendum (applied here as by-hand discipline per its PROPOSED status).
- Does not create the near-half plan, the signal-reliability ledger, or the
  lesson library; N7 is a pending interface, not a binding.
- Post-resolution presentation of shadow records does not retroactively convert
  shadow evidence into assisted evidence or buyer proof.
- Not validation, readiness, acceptance, buyer proof, or judgment-quality
  evidence; this artifact's own evidence state is classified below.

## Claim Classification (Judgment Spine claim-tier gate)

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface: prospective-decision-loop target architecture (planning/design artifact)
  source_quality_state: design/control artifacts only (three controlling sources re-verified at origin/main @ f3f0609; near-half plan absent from repo)
  execution_quality_state: no run, no live decision, no sealed call, no resolution exists
  closeout_state: no_durable_evidence
  claim_cap: design input / product-learning context only
  weakest_missing_or_failed_gate: no prospective run exists; prospective gate family not authored (indeterminate_until_authored)
  receipt_artifact_or_gap: this artifact is the gap-naming record; first receipts would be Phase-1 seal/resolution artifacts under a future owner-signed ledger
  non_claims:
    - not validation unless separately proven
    - not readiness unless separately proven
    - not buyer proof unless the buyer-proof receipt is complete
    - not judgment-quality evidence unless the judgment-quality receipt is complete
```

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    None enacted. This artifact ADDS a PROPOSED target architecture for the
    prospective decision loop; it edits no controlling source, mints no
    vocabulary, and routes all owner-territory changes out (prospective gate
    family -> evidence-ladder owner; ratification -> owner). If ratified later,
    that ratification carries its own propagation receipt.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - orca/product/spines/judgment/learning_loops/far_half/prospective_decision_loop_target_architecture_v0.md (new; this file only)
  downstream_surfaces_checked:
    - orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md  # consumed, not amended; no prospective path is claimed cleared
    - orca/product/spines/judgment/conductor/conductor_construction_integrity_probe_addendum_v1.md  # firewall translated, not edited; PROPOSED status respected
    - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md  # ledger discipline reused as pattern; batch untouched
    - .agents/workflow-overlay/source-loading.md  # read-pack addition deferred to ratification (commit-once-whole shared file; PROPOSED artifacts do not enter read packs)
    - docs/workflows/orca_repo_map_v0.md  # same deferral, same reason
  intentionally_not_updated:
    - path: all five surfaces above
      reason: this artifact is PROPOSED and enacts nothing; pointing shared navigation/doctrine at an unratified target would launder proposal into authority.
  stale_language_search: >
    rg -n "prospective_decision_loop|prospective decision loop|shadow mode|assisted mode"
    docs/product/judgment_spine .agents/workflow-overlay docs/decisions docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Run 2026-06-13 in the lane worktree before this write: no prior artifact
    claims ownership of shadow/assisted-mode or prospective-loop architecture;
    no conflicting or duplicate doctrine found. Hits for "shadow" elsewhere
    refer to skill-adoption shadow copies (unrelated vocabulary).
  non_claims:
    - not validation
    - not readiness
    - not ratification
    - not implementation authorization
```
