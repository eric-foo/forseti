# Orca Memorization-Resistant Case Finder — Doctrine Frame v0

```yaml
retrieval_header_version: 1
artifact_role: Product doctrine frame (decision-prep; proposed, not frozen)
scope: >
  Proposed doctrine for a standing, memorization-resistant case finder that
  surfaces obscure, decision-grade backtest subjects below model recall and feeds
  them to the decide-vs-confirm tests and the judgment-quality proof path. Extends
  Core Spine heavyweight discovery by inverting its fame bias. States requirements
  and boundaries only; designs no mechanism and builds no system.
use_when:
  - Selecting case subjects for decide-vs-confirm tests or judgment-quality runs.
  - Extending or reviewing Core Spine heavyweight discovery for memorization-resistance.
  - Deciding whether the finder warrants an architecture pass yet.
authority_boundary: retrieval_only
open_next:
  - docs/product/core_spine/core_spine_v0_heavyweight_proof_case_discovery_charter_v0.md
  - docs/research/judgment-spine/manifest_v0.md   # Selection-Rule-for-Case-2
  - docs/research/judgment-spine/decide_vs_confirm_backtest_case_frame_template_v0.md
  - docs/decisions/orca_moat_judgment_quality_proof_path_decision_chain_v0.md
  - docs/product/core_spine/orca_venue_exploration_procedure_v0.md   # WHERE-side venue procedure (owner-adopted shape, subordinate to this frame)
stale_if:
  - Owner signs off and promotes this into binding selection doctrine.
  - The deferred-architecture trigger fires (manual screen proven + throughput bottleneck).
  - Core Spine discovery eligibility / anti-leakage doctrine changes.
```

## Status

`PROPOSED_DOCTRINE_FRAME_PENDING_SIGNOFF`. Decision-prep, not frozen doctrine, not
a system design, not validation. It states what the finder must do and must not
become; it designs no screening mechanism and authorizes no build. Smallest form:
a manual selection discipline extending existing discovery. Freezes nothing.

**Operative bar relaxed per owner direction 2026-06-09 — see "Operative bar" below; the strong-memorization machinery in this frame is retained as rationale / rigorous ceiling, not the operative rule.**

Dirty-state (corrected 2026-06-11): tracked at its Phase-2 home
`docs/product/core_spine/`; the original "untracked, durable-home
reconciliation separate" authoring note is retired.

## Operative bar (owner relaxation, 2026-06-09)

With the contestant's **web search OFF**, the only contamination vector is
training-memorization, which mainly bites famous headline cases. So the *operative*
screen at product-learning tier is:

- **Not too prominent** — avoid famous/headline cases; moderately-obscure is fine.
  No independent-signal certification required at this tier.
- **Web search OFF** for the contestant — structural and recorded
  (`web_search_disabled` evidence per the probe protocol), not a prompt instruction.
  Load-bearing: it is what makes "not too prominent" safe.
- **Isolated memory probe as a conservative backstop** — run it in a SEPARATE
  session from the judgment (no priming); treat a fail as a *swap signal*, not a
  verdict (over-rejection is the safe direction). The probe is NOT a gate and NOT
  proof of no-memorization; it errs toward caution by design — asking a model to
  recall can manufacture recognition.
- **Optional flavor-anonymization at packet construction** — genericize company
  name / non-decision flavor only; **never the decision-driving numbers** (those stay
  real so the outcome remains ground truth). It slightly pre-cleans raw signal — a
  small product-faithfulness tax; use sparingly.
- **Swap on recognition** — the `Uses` counter ledger + this finder generate
  lower-count, more-obscure replacements.

The independent-signal / narrow-band / per-model-recertification machinery below is
**retained as rationale and as the rigorous ceiling** for a future judgment-quality
run that needs certified memorization-resistance — it is not the operative bar at
product-learning tier.

## What it is (smallest form)

A **standing selection discipline** — a screen plus a cadence — that surfaces
obscure, decision-grade decision cases for backtesting, and feeds them to the
decide-vs-confirm case-frame template and the judgment-quality path.

Its smallest complete form is **doctrine applied manually**, not a system. It
*extends* Core Spine heavyweight discovery; it does not replace or rebuild it.

What it is NOT, and must not become: a monitoring product, a source map, a source
inventory, a scraper / automation / pipeline, or a standing corpus intake — the
same boundaries Core Spine discovery and the data-capture thesis already draw.

## The bug it fixes

The existing heavyweight discovery selects FOR fame: it optimizes for "later
outcome visible / official surfaces on both sides / clean documented outcome."
That is exactly what frontier models have memorized — so the cases it surfaces
make a "blind" judgment not blind. The finder's one job is to **invert that
criterion**: prefer cases models have *not* memorized.

## The core tension (frame it; do not solve it here)

Finding such cases is a **narrow-band search**, not a simple filter:

- **Memorization-resistance pulls toward obscure; decision-grade + source-depth
  pulls toward covered.** The most obscure cases tend to have the thinnest public
  evidence, failing the source-depth gate. The finder hunts the band that is
  obscure enough to be blind yet covered enough to be decision-grade. That band
  may be small; navigating it is the work.
- **Obscurity is model- and version-specific.** A case obscure to today's
  contestant model is memorized by a later one. So "memorization-resistant" is a
  property re-certified per contestant model/version — not a one-time stamp.
- **Self-reference trap.** A case's obscurity cannot be judged by the contestant
  model's own recall (it is the thing under test). Fame/recall must be estimated
  from an *independent* signal.

These are requirements the finder must satisfy. *How* it satisfies them — the
fame/recall signal, the source-depth floor, the re-certification cadence — is
deferred to a later architecture pass (see the trigger below).

## What the finder must require (the screen)

A subject passes only if ALL hold. These are requirements, not a built mechanism.

- **Memorization-resistant**, estimated from a signal *independent* of the
  contestant model's own recall.
- **Decision-grade + source-depth floor** (manifest Selection-Rule-for-Case-2):
  reconstructable decision, clean cutoff, visible tradeoff, revealed
  action/outcome, enough pre-cutoff source depth to expose judgment misses.
- **Decision-family fit** for the consuming test (e.g. repricing; clean-substrate
  competitor-displacement).
- **Zero-spoiler feasibility**: a clean pre-cutoff packet can be built without the
  outcome leaking.
- **Decide-vs-confirm tension**: at cutoff the outcome was genuinely not obvious.
- **Anti-cherry-pick**: drawn from a pre-declared lane, not chosen because the
  outcome flatters Orca.

## Connection to Core Spine discovery

The finder is an **extension**, not a parallel lane:

- Reuse discovery's eligibility inspection + anti-leakage machinery (it already
  separates eligibility from evidence interpretation and forbids source maps /
  monitoring).
- Add the **obscurity screen** and flip the dominant selection criterion from
  "famous + documented" to "obscure-but-decision-grade."
- The existing discovery results (famous candidates) become the *negative* set —
  examples of what the screen should now downgrade.

## Cadence (the "standing" part)

Standing means the screen is applied each time subjects are needed, against the
*current* contestant model/version (because obscurity decays). Initially this is a
**manual** run of the screen — no scheduler, no monitor, no automated feed.

## Deferred-architecture trigger

Route to an architecture pass (`workflow-architecture-planning`) for an automated
finder ONLY when BOTH hold:

- the manual screen is *proven* to surface obscure-AND-decision-grade subjects
  (it has produced at least one case the tests / judgment path accepted); AND
- a real throughput / cadence bottleneck exists (manual selection cannot keep up
  with demand).

Until both hold, building a finder system is premature infrastructure. Naming the
trigger keeps the deferral honest, not permanent.

## Must / must-not

Must:

- Feed real obscure subjects to the decide-vs-confirm case-frame template and the
  judgment-quality path.
- Estimate obscurity from a signal independent of the contestant model.
- Preserve zero-spoiler, anti-cherry-pick, and the source-depth floor.

Must not:

- Become a monitor, source map, source inventory, scraper, or standing corpus.
- Design or build the screening mechanism inside this frame (that is the deferred
  architecture pass).
- Hand-pick subjects from the authoring model's own memory (self-reference trap).
- Treat a passed subject as validated, captured, or proof.

## Dependencies

- **Downstream consumers:** the decide-vs-confirm case-frame template; the
  judgment-quality proof path (decision-chain D6/D7).
- **Downstream lane:** source capture (cutoff-disciplined) turns a selected
  subject into a real packet — separate, gated.
- **Upstream context:** Core Spine heavyweight discovery (extended here).

## Non-Claims

Not a system, not validation, not readiness, not buyer proof, not judgment-quality,
not a proven screen. Surfaces no subject and asserts no case here. Authorizes no
capture, discovery run, or build. Decision-prep only. Freezes nothing without owner
sign-off.

## Lane Note

Product-lead / method decision-prep frame. The screening *mechanism* and any
automated finder are architecture/implementation-lane work, gated behind the
trigger above and explicit authorization.
