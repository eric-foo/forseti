# Core Spine v0 Proof Protocol

- Status: PROPOSED_FREEZE
- Artifact type: Product proof protocol
- Scope: Docs-first proof plan for Core Spine v0
- Source basis: current owner direction, `docs/decisions/turn_08_product_thesis_v0.md`, `docs/product/core_spine_v0_product_contract.md`, `docs/product/engagement_logic_registry_v0.md`, `docs/product/core_spine_v0_information_production_foundation_v0.md`
- Implementation authorized: no
- Feature planning authorized: no

## Purpose

This protocol defines what proof is sufficient to show that Core Spine v0 can
produce decision-grade outside-in intelligence across more than one satellite.

It does not run the proof. It defines the proof bundle, memo requirements,
backtest rules, pass/fail gates, and feature-planning boundary.

## Proof Question

Can the same eight Core Spine primitives turn noisy public evidence into
inspectable allocation recommendations across `jb` Client 0 and at least one
materially different non-`jb` satellite?

The proof must show decision discipline, not just polished memo writing.

## What This Can Prove

The protocol can prove:

- Core Spine v0 is usable for decision-grade public-signal interpretation.
- Core Spine v0 can support more than one satellite without adding new core
  primitives.
- Signal Integrity and Signal Use Classification affect recommendation
  strength instead of acting as decorative analysis.
- Engagement evidence is not collapsed into a single demand score.
- Backtesting can preserve timestamp discipline and update Orca's evidence
  standard.

## What This Cannot Prove

The protocol does not prove:

- external willingness to pay;
- market size;
- that `jb` evidence generalizes commercially;
- that runtime collection, scraping, databases, dashboards, scoring engines, or
  automation should be built;
- that feature planning or implementation is ready.

## Minimum Proof Bundle

Core Spine v0 proof requires all of the following:

1. A Client 0 `jb` decision memo dry run.
2. One materially different non-`jb` shadow satellite decision memo dry run.
3. A shared evidence standard based on the eight Core Spine primitives.
4. Shared use of `docs/product/engagement_logic_registry_v0.md`.
5. One leakage-controlled backtest replay.
6. Explicit pass, fail, blocked, and inconclusive states.

## Shared Core Spine Primitives

Both memo dry runs and the backtest must use the same primitives:

| Primitive | Proof role |
| --- | --- |
| Decision Frame | Names the allocation question, decision owner or context, consequence, allowed recommendation verbs, and kill criteria. |
| Evidence Unit | Makes every material claim inspectable through source, timestamp, excerpt, claim, provenance, visibility, transformation history, and relevance. |
| Signal Integrity | Judges credibility, incentives, independence, repetition, manipulation risk, botting, copied language, artificial amplification, and source limitations. |
| Signal Use Classification | Classifies what each signal can validly inform: demand, attention, resonance, objection, distribution, buyer belief, actor strategy, manipulation risk, weak evidence, or exclusion. |
| Decision Strength | Maps evidence quality to action threshold by weighing audience fit, costly behavior, counterevidence, alternative explanations, confidence, and action boundary. |
| Decision Memo | Turns the evidence into a recommendation, alternatives, uncertainty, kill criteria, and what would change the answer. |
| Backtesting and Outcome Memory | Replays past decisions using only pre-cutoff evidence and records later outcome, misses, calibration, and learning. |
| Boundary Rules | Keeps work public, market-level, non-deceptive, docs-first, and non-runtime. |

## Client 0 Memo Dry Run

The Client 0 dry run tests concrete usefulness for the current internal
decision:

> Which finance-career avatar, pain wedge, copy angle, pricing/package, and
> workflow bet has the strongest public market pull?

It validates method usefulness, data-spine pressure, signal-quality judgment,
and decision-memo usefulness. It does not validate external willingness to pay.

The `jb` memo must not turn `jb` categories, lifecycle mechanics, prompt
templates, paths, or validation habits into Core Spine authority.

## Shadow Satellite Memo Dry Run

The shadow satellite must be materially different from `jb`.

It must define its own:

- decision type;
- buyer, user, decision owner, and consequence;
- domain language;
- source families and source blind spots;
- decision-specific relevance rules;
- costly behavior definition;
- allowed recommendation verbs;
- success criteria;
- kill criteria;
- actor or competitor behavior that matters.

The shadow satellite passes portability only if it uses the same Core Spine
primitives without adding new core primitives or importing finance-career
assumptions.

## Memo Dry Run Requirements

Each memo dry run must satisfy the Memo Production Rules in
`docs/product/core_spine_v0_information_production_foundation_v0.md`.

At minimum, each memo dry run must contain:

1. Decision frame.
2. Evidence Unit set.
3. Signal Integrity summary.
4. Signal Use Classification summary.
5. Decision Strength assessment.
6. Action Ceiling.
7. Recommendation and allowed verb.
8. Counterevidence.
9. Alternative explanations.
10. Uncertainty.
11. Kill criteria.
12. Update triggers.
13. Evidence appendix sufficient for a skeptical reader to reconstruct the
    reasoning.
14. Boundary note naming what the memo does not prove.

The recommendation verb must not exceed the Action Ceiling. If the evidence
only supports monitor, investigate, or test, the memo must not recommend
invest, build, or commit.

The memo must be a decision memo, not a generic research summary.

## Backtest Replay Rules

The backtest asks:

> Given only public evidence available before date X, would Orca have produced
> a useful decision memo before the outcome was obvious?

A valid internal backtest must record:

- decision context;
- cutoff date;
- why the cutoff is fair;
- source visibility before cutoff;
- evidence included;
- evidence excluded as post-window;
- recommendation Orca would have made;
- Decision Strength and Action Ceiling at the time;
- later outcome;
- whether Orca was early, late, wrong, overconfident, underconfident, or useful;
- what the evidence standard should learn.

Misses must be retained for internal calibration. Cherry-picked wins may be
used as marketing demos only when labeled as marketing demos. Marketing demos
must not train the internal evidence standard unless they pass leakage controls
as defined in
`docs/product/core_spine_v0_information_production_foundation_v0.md`.

## Pass Criteria

The proof passes only if all are true:

- Client 0 and the shadow satellite both produce decision-grade memos, not
  generic research summaries.
- Both memos use the same eight Core Spine primitives.
- Every material recommendation has inspectable evidence units.
- Signal Integrity records its effect statement and changes Decision Strength
  or Action Ceiling when evidence is copied, incentivized, bot-like, weak,
  noisy, or source-limited.
- Signal Use Classification prevents attention, campaign success, copied
  language, or social proof from being overclaimed as demand.
- Each satellite defines its own costly behavior and action threshold.
- At least one backtest shows source visibility before cutoff and excludes
  post-window evidence.
- Misses, uncertainty, and update triggers are preserved as calibration input.
- The proof remains docs-first and does not imply runtime implementation.

## Fail Criteria

The proof fails if any are true:

- The shadow satellite requires new core primitives.
- `jb` categories, success logic, lifecycle mechanics, workflow assumptions, or
  decision verbs leak into the shadow satellite.
- Engagement is treated as a demand score.
- The same engagement pattern is judged differently across satellites without
  an explicit decision-use rationale.
- Signal Integrity flags are decorative and do not change Decision Strength.
- Copied, incentivized, bot-like, or campaign-driven evidence is counted as
  independent pull without justification.
- The evidence appendix is not inspectable enough for a skeptical reader to
  reconstruct the claim.
- The memo recommends invest, build, or commit when the evidence only supports
  monitor, test, or investigate.
- Backtest cases are chosen after outcome knowledge and treated as internal
  proof instead of marketing demos.
- The protocol cannot separate "Orca helped choose among options" from "Orca
  proved the market is real."

## Blocked Criteria

The proof is blocked when:

- no materially different shadow satellite is selected;
- no decision context is selected for the shadow satellite;
- no historical case is selected for backtesting;
- no pre-cutoff source visibility can be established;
- required evidence is unavailable or not inspectable;
- owner input is needed to define confidence vocabulary, action thresholds, or
  satellite-specific costly behavior.

Blocked is not a failure of Core Spine v0. It means the proof cannot be judged
from the current inputs.

## Inconclusive Criteria

The proof is inconclusive when:

- evidence supports monitor or investigate but not stronger action;
- the shadow satellite works structurally but evidence quality is too thin;
- the backtest shows useful caution but no clear recommendation;
- the memo narrows uncertainty without producing a decisive allocation
  recommendation.

Inconclusive results should update the evidence standard and may justify
another proof run, but they do not authorize feature planning.

## Feature-Planning Gate

Feature planning is appropriate only after:

1. this protocol is accepted;
2. Client 0 and the shadow satellite are selected;
3. the backtest case or case-selection policy is selected;
4. the proof packet is run or the owner explicitly authorizes a feature plan
   from this protocol;
5. pass/fail/blocked/inconclusive results are recorded;
6. explicit feature-planning authorization is given.

Until then, Orca should remain in docs-first product-proof work.

## Explicit Non-Goals

This protocol does not authorize:

- scrapers;
- source APIs;
- databases;
- dashboards;
- scoring engines;
- automation runtimes;
- clustering pipelines;
- software tests;
- implementation folders;
- stack choices;
- generalized OSINT platform work;
- workflow-kernel source edits;
- skill installation, promotion, renaming, or shadowing.

Ideas from those systems may inform product requirements or judgment rubrics,
but they are not v0 runtime machinery.

## Bloat Cuts

Cut from this protocol:

- full memo drafts;
- source collection plans;
- source-family inventories beyond the selected memo contexts;
- numeric scoring formulas;
- dashboard or database design;
- marketing copy;
- case-library packaging;
- broad multi-case backtest suite;
- implementation units or feature plans.

Keep:

- proof bundle;
- memo dry run requirements;
- backtest rules;
- pass/fail/blocked/inconclusive gates;
- feature-planning boundary.

## Open Questions

- Shadow satellite choice: UNKNOWN - requires owner input.
- Backtest case or case-selection policy: UNKNOWN - requires owner input.
- Confidence vocabulary: UNKNOWN - requires owner input.
- Exact action-threshold language: UNKNOWN - requires owner input.
- Whether marketing demo cases belong in this protocol or a later case-library
  artifact: UNKNOWN - requires owner input.

## Current Verdict

Current verdict: `NEEDS_PRODUCT_ARTIFACT`.

This protocol is a proposed product artifact. It becomes a stronger planning
input only after owner acceptance and a selected proof run. It does not claim
feature-planning readiness or implementation readiness.
