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
  - orca/product/case_families/product_learning/other_verticals/core_spine_v0_heavyweight_proof_case_discovery_charter_v0.md
  - docs/research/judgment-spine/manifest_v0.md   # Selection-Rule-for-Case-2
  - docs/research/judgment-spine/decide_vs_confirm_backtest_case_frame_template_v0.md
  - docs/decisions/orca_moat_judgment_quality_proof_path_decision_chain_v0.md
  - orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md   # WHERE-side vertical exploration guide (owner-adopted shape, subordinate to this frame)
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
- **Non-inducing isolation screen as the pre-judgment backstop** — active "name
  the case" recall is dropped entirely (asking a model to recall manufactures
  recognition — a survivorship trap). Contamination is outcome-USE, not
  recognition capacity: it is caught after the fact by tell-auditing the required
  reasoning trace (JSG-08). A contestant who merely recognized the case but did
  not use the outcome is a legitimate arm, not a swap signal.
- **Default-on identity-masking with sealed crosswalk (owner-adopted 2026-06-16).**
  At packet construction, mask the **target brand's identity only** — its name, its
  own domain, its own theme/copy — to one neutral stand-in (with web search off no
  search-defeating decoy is needed; pick a label checked not to be a real brand, to
  avoid manufacturing a fresh false recognition). **Keep every third-party source
  identity real** (retailers, publications, platforms, forums): those carry
  provenance and do not reveal the target. **Never mask the decision-driving numbers
  / dates / counts** (those stay real so the outcome remains ground truth), and
  **never blur a source's provenance** — rename the source, keep its species
  (first-party vs third-party). Beyond the brand name, genericize **decision-moment
  locators** — specific datable news events, named collaborations, distinctive launch
  episodes, any extraneous flavor that lets a brand-recognizer pin the exact episode
  and its outcome — while keeping the bare cutoff and the decision-driving numbers
  real. Recognition of the brand is not the threat; recall of the specific sealed
  outcome is, and locators are what bridge the two. Supply any decision-relevant brand attribute
  (positioning, reputation, awareness) as **in-packet evidence**, name-free, rather
  than relying on contestant recall; a "signal" that cannot survive name-removal is
  recognition-recall, not evidence — treat it as a contamination tell. Supplied
  attribute evidence is itself contamination-sensitive: it must be source-backed,
  pre-cutoff, and authored under the same outcome-blind construction discipline as
  all packet evidence (the constructor does not hold the sealed outcome) — never
  outcome-shaped prose. Mask at
  construction time (the constructor authors the packet name-free; raw captures stay
  sealed and un-masked); the pseudonym↔real-case map is **operator-only and sealed**
  (like the facilitator ledger). Its owner, storage boundary, access rule, and
  integrity/freshness semantics are a bound construction-contract item routed to the
  packing / interface lane; until that interface lands this is doctrine intent and a
  masked run is not yet executable as a sealed-crosswalk-backed run. Masking stays whitelist-only (no enumerated
  forbidden-category list on any contestant-readable surface), must pass the R6
  pre-freeze leakage gate, and a plain real-name search of the finished contestant
  packet must return nothing before freeze. **Route-out rule:** if the
  decision-relevant attribute cannot be described faithfully without re-identifying
  the brand, do not blind-backtest it — use a post-cutoff or prospective
  seal-and-wait case instead. The maskability test weighs **all** identity-bearing
  evidence kept real — a distinctive retailer / forum / publication, an exact metric,
  a launch date, a singular source relationship — not just the brand attribute;
  masking removes only the name-recall handle and makes no re-identification-resistance
  claim (the tell-audit, not the mask, is the backstop), **recognizability of the brand is not
  grounds to route a case out** — recognition is a legitimate arm; only USE of the
  sealed outcome is contamination, caught by the tell-audit. Route out **only** the
  narrow case where, even after decision-moment-locator anonymization,
  brand-recognition would reliably surface the specific sealed outcome (a famous
  episode where the brand-plus-decision IS the memorable event) — use a post-cutoff
  or prospective seal-and-wait case there. (Owner correction 2026-06-16: this
  supersedes the earlier "route out trivially-re-identifiable cases" reading and
  dissolves the representativeness concern — merely-recognizable cases are kept, so
  the masked-eligible set stays decision-grade.)
- **Masking is a supplement, not the spine.** Web-search-off + the JSG-08 tell-audit
  remain the contamination spine; masking raises the bar on passive recognition and
  makes the tell-audit's job cleaner, but it must **not** relax the tell-audit, and a
  masked case is never assumed "blind" on the strength of the mask alone. The
  tell-audit-unchanged guardrail is a **required acceptance / freeze condition** for
  any masked run — a run is invalid if the tell-audit was weakened to compensate for
  masking; mechanical enforcement of that condition is a pending tail item.
- **Swap on a confirmed outcome-use tell** — recognition capacity alone is not a
  swap; when a swap is warranted, the `Uses` counter ledger + this finder generate
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
