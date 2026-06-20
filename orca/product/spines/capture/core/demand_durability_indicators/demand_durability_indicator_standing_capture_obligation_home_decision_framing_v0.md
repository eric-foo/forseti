# Demand-Durability Indicator — Standing-Capture Obligation Home: Owner-Decision Framing v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact (owner-decision framing; frames a decision, does not make it)
scope: >
  Frames the owner decision surfaced when hourly/daily continuous monitoring of the
  demand-durability indicators (price, availability, search-interest, review) was
  confirmed wanted: these become STANDING capture, which the v0 obligation contract
  has no home for. Names the decisions to make, the shape any answer must keep, and
  the lock-in tradeoffs. Framing only — it is NOT the standing-capture obligation
  contract and makes no decision.
use_when:
  - Deciding how to give standing/continuous capture of the demand-durability indicators an obligation home.
  - Checking why hourly/daily monitoring of these indicators is currently blocked.
  - Coordinating this decision with the company-aggregate/EDGAR lane's identical standing-capture gap.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md   # v0 = commissioned-capture only (the gap)
  - docs/decisions/company_aggregate_forward_signal_capture_lane_scope_decision_v0.md            # the other lane that hit this gap + its light-clarification framing
  - orca/product/spines/capture/core/demand_durability_indicators/demand_durability_indicator_capture_deconfliction_note_v0.md # the four profiles + this consequence
  - orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md                                       # never-a-feed invariant + monitoring-only kill
stale_if:
  - The owner makes this decision (then this framing is consumed; the chosen contract/amendment supersedes it).
  - The v0 obligation contract is amended to admit a standing-corpus path.
  - A general Candidate Signal Intake / Corpus Intake contract is written.
  - The company-aggregate lane's standing-capture obligation home is resolved (it may resolve this jointly).
  - The owner withdraws the continuous-monitoring direction.
```

- Status: `OWNER_DECISION_FRAMING_V0` — direction **SELECTED by owner 2026-06-15** (general contract + scheduler deferred); the contract itself is unwritten (next lane). This artifact frames the decision and records the selection.
- Artifact type: Owner-decision framing (docs-write). Not the obligation contract, not an amendment, not a build authorization.
- Implementation authorized: no · Contract hardening authorized: no (owner-gated) · Scheduler/runtime authorized: no

## Owner Selection (2026-06-15)

The owner adopted the recommended direction:

- **D1 = general.** Write the shared **Candidate Signal Intake / Corpus Intake contract**
  that serves both the demand-durability indicators *and* the EDGAR/org-motion lane — one
  standing-capture regime, not two diverging slice-clarifications.
- **D2 follows from D1** → the separate Corpus/Candidate-Signal-Intake contract (not a
  narrow v0 amendment).
- **D3 = scheduler deferred** behind a trigger-agnostic capture entrypoint (manual trigger
  now; a scheduler is a separate later build authorization).

Authoring that contract is the **next lane** — doctrine-bearing, so recommended for a
delegated/adversarial review (it is not written here). This selection chooses a direction;
it is **not** itself the contract, an amendment, validation, or a build/scheduler
authorization.

## Why This Exists (the trigger)

Owner direction (2026-06-15): the demand-durability indicators should be monitored
**continuously, on an hourly-to-daily rhythm.** That rhythm is **standing capture** — it
accretes a time series *before and across* specific decisions, not capture tied to one
live Decision Frame. The v0 Data Capture obligation contract
(`core_spine_v0_data_capture_spine_obligation_contract_v0.md`) scopes **commissioned
capture only** and **explicitly routes standing/opportunistic corpus capture out** of v0
to "a separate Candidate Signal Intake or Corpus Intake contract" — **which does not yet
exist.** So **continuous monitoring of these indicators is blocked until that obligation
home exists.** This note frames the decision that unblocks it; it does not take it.

The four indicator profiles stay "commissioned capture only" until this is resolved.

## Not a new gap — the same one the EDGAR lane already hit

The company-aggregate/EDGAR forward-signal lane
(`docs/decisions/company_aggregate_forward_signal_capture_lane_scope_decision_v0.md`) is
also standing capture and surfaced the **identical** obligation-home gap. Its owner
refinement is directly reusable input: the blocker is **doctrinal (which contract governs
standing capture), not legal**; clearing it can be a **light, slice-scoped clarification**
rather than a heavyweight new contract — *either* amend v0 to admit a standing-corpus path
*or* stand up the separate Corpus/Candidate Signal Intake contract v0 points to. What is
required is **an explicit obligation home, however light.** That this gap now blocks **two
lanes** is itself a decision input (below).

## The decisions to make (owner)

### D1 — Scope: narrow (this slice) vs general (one contract for both lanes)
- **Narrow:** a slice-scoped clarification for the demand-durability indicators only
  (mirrors what the EDGAR lane did for itself).
- **General:** write the shared **Candidate Signal Intake / Corpus Intake contract** that
  serves both the demand indicators *and* the EDGAR/org-motion lane.
- **Lock-in (framing input, not a decision):** narrow is lower lock-in now but risks **two
  divergent standing-capture clarifications** (this slice + the EDGAR slice) that later
  have to be reconciled. The EDGAR lane already took the narrow path for itself; a *second*
  narrow slice is the point at which the **general contract likely becomes the
  lower-total-lock-in move** — one standing-capture regime, not two diverging ones. Surface,
  do not decide.

### D2 — Weight: light v0 amendment vs full separate contract
- The EDGAR-lane owner leaned **"clarification, not necessarily a heavyweight new
  contract."** The same option set applies here: amend v0 to admit a standing-corpus path,
  or write the separate contract. D2 interacts with D1 (a general scope tends toward the
  separate contract; a narrow scope tends toward a light amendment).

### D3 — Cadence/scheduler lock (the high-lock-in axis)
- Hourly/daily monitoring implies a **scheduler/runtime** to execute the sampling — the
  high-lock-in axis the EDGAR lane explicitly **deferred** (its official sources are
  annual/periodic, so manual-now was fine). **Here it is sharper:** hourly/daily is far too
  frequent to run by hand, so committing to this rhythm pulls the scheduler decision
  forward. Decide: **manual-now (and accept the rhythm won't really be hourly/daily yet)**
  vs **authorize a scheduler** (a separate build authorization; not granted by this
  framing). The EDGAR lane's structural hedge applies — design a *trigger-agnostic capture
  entrypoint* so a manual trigger now and a scheduler later call the same path without
  re-architecting.

## The shape any answer must keep (carried, not decided)

Whatever the owner chooses, the standing-capture obligation home for these indicators must
preserve:

- **Existing v0 obligations + minimization.** It runs under the current capture obligations
  (boundary compliance, capture-event provenance, decomposed timing, archive/visibility
  posture, failure visibility) and the source-access boundary (measured-ToS accepted,
  industrial scraping rejected). It does not loosen them.
- **The rebind rule.** A standing observation row is **not ECR-ready evidence until rebound
  or recaptured under a Decision Frame** (the v0 standing-capture carve-out). The series is
  a **corpus that commissioned reads later draw from**, not pre-cleared evidence.
- **Append-only retention.** Re-observations supplement, never overwrite (Ob.15); the
  series is preserved.
- **The never-a-feed invariant (load-bearing).** Per the buyer-proof packet, **every output
  is a calibrated decision with an action ceiling — never a feed or stream.** A standing
  monitor must feed *recurring decisions*, never become a sold monitoring feed. This is the
  structural lock that keeps continuous monitoring **off the "monitoring-only pull" kill**
  and out of the social-listening category. Capturing a corpus hourly/daily is fine; selling
  a feed is the kill — the obligation home must encode that the corpus is decision-substrate,
  not product output.
- **The manipulability flags ride forward.** The indicators' integrity caveats
  (scarcity-theater for availability, farm/J-curve for reviews, attention-not-costly for
  search, promo-vs-permanent for price) are captured as standing-capture facts too; standing
  capture does not relax "flag, don't conclude."

## What is specifically new here vs the EDGAR lane

- **Frequency.** EDGAR org-motion is annual/periodic official filings; these indicators are
  **hourly/daily** — so the scheduler lock-in (D3) is sharper and arrives sooner.
- **Manipulable substrate.** EDGAR is official public data; these indicators sit on the
  hostile, manipulable demand substrate, so the integrity flags above must survive into the
  standing corpus.
- **Source set.** Retail/beauty price, availability, search-interest, review surfaces — not
  official registries — so the source-access posture (rendered/embedded/manual,
  measured-ToS) is the four profiles', not EDGAR's official-first one.

## Recommendation (framing input — owner decides)

Given the gap now blocks **two** lanes and the demand indicators commit to a **high
frequency** that forces the scheduler question, the **general Corpus/Candidate Signal Intake
contract (D1: general)** is likely the lower-total-lock-in path — one standing-capture
regime serving both lanes — while keeping **D3 (scheduler) deferred** behind a
trigger-agnostic entrypoint until a separate build authorization. This is **input, not a
decision**; a narrow slice-scoped clarification remains valid if the owner wants to keep
lock-in minimal now and reconcile later.

## Boundaries & Non-Claims

- **Framing only.** This is not the standing-capture obligation contract, not an amendment
  to v0, not a decision, not an authorization. Writing the contract/amendment is owner-gated.
- **No build.** No scheduler, monitor, runner, runtime, or storage is specified or
  authorized. The trigger-agnostic-entrypoint note is a design hedge, not a build plan.
- **INV-1 preserved.** No weighting, scoring, ranking, or judgment is introduced.
- Not validation, readiness, acceptance, source-of-truth promotion, buyer proof,
  implementation/runtime/tooling authorization, source-access boundary amendment, or
  commercial-readiness evidence.
```
