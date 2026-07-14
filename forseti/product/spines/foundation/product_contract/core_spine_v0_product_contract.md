# Core Spine v0 Product Contract

```yaml
retrieval_header_version: 1
artifact_role: Product artifact (Core Spine product contract)
scope: >
  Market-agnostic contract for Forseti decision adjudication, the initial
  Decision Sprint, evidence admission/refusal, buyer-facing decision artifacts,
  and the gated path toward recurring and software-supported product forms.
use_when:
  - Defining the reusable product contract beneath a vertical application.
  - Checking whether an evidence workflow produces a decision outcome rather than research alone.
  - Separating the initial Decision Sprint from later Decision Desk and platform hypotheses.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_product_thesis_decision_adjudication_v0.md
  - forseti/product/satellites/beauty/beauty_decision_adjudication_product_profile_v0.md
  - forseti/product/shared/engagement_registry/engagement_logic_registry_v0.md
stale_if:
  - The controlling thesis changes the product center or initial product form.
  - Proof shows the Decision Sprint cannot produce a useful action from an admitted evidence world.
```

- Status: PRODUCT_DIRECTION_AND_INITIAL_FORM_BOUND
- Artifact type: Product artifact
- Scope: Market-agnostic Core Spine contract for Forseti v0
- Source basis: current owner direction; `docs/decisions/forseti_product_thesis_decision_adjudication_v0.md`; `forseti/product/shared/engagement_registry/engagement_logic_registry_v0.md`
- Implementation authorized: no

## Product Bet

Core Spine v0 is Forseti's reusable decision-adjudication spine. It turns
decision-relevant public, purchased/entitled, and authorized private evidence
into an inspectable, constrained action without becoming a generic OSINT
platform, research shop, dashboard, deck shop, or `jb`-specific intelligence
tool.

Core Spine owns market-agnostic decision and evidence mechanics. Satellites own
domain context, language, source behavior, entities, and application-specific
relevance. Buyer, first decision family, offer, price, and distribution are
bound only by an accepted GTM/product-proof surface; a pre-GTM application
profile may leave them explicitly unselected.

## Core Rule

Every signal must be interpreted through a decision question:

> What decision can this signal validly inform?

Evidence that is weak for demand may still be strong for attention,
distribution, competitor strategy, manipulation risk, buyer belief, or market
perception.

## Frozen Core Primitives

Core Spine v0 is intentionally compressed into eight primitives. The product
should not add a standalone axis when the concern can be absorbed into one of
these primitives.

| Priority | Primitive | Core responsibility | Absorbs |
| --- | --- | --- | --- |
| 1 | Decision Frame | Name the allocation question, decision owner or context, consequence, allowed recommendation verbs, and kill criteria. | Decision type, owner, consequence, action boundary |
| 2 | Evidence Unit (EvidenceUnit) | Capture source, timestamp, excerpt, claim, provenance, source visibility, transformation history, and relevance. | Source visibility, timing metadata, audit trail |
| 3 | Signal Integrity | Judge credibility, incentives, independence, repetition, manipulation risk, botting, copied language, artificial amplification, and source limitations. | Source quality, fake engagement, dedupe, campaign distortion |
| 4 | Signal Use Classification | Classify what the signal can validly inform: demand, attention, resonance, objection, distribution, buyer belief, actor strategy, manipulation risk, weak evidence, or exclusion. | Competitive intelligence, engagement interpretation, message propagation |
| 5 | Decision Strength | Judge what action the evidence can support by weighing audience fit, costly behavior, counterevidence, alternative explanations, confidence, and action threshold. | Audience fit, costly behavior, counterevidence, confidence, recommendation threshold |
| 6 | Decision Artifact | Produce the recommendation, evidence basis, alternatives, uncertainty, kill criteria, and what would change the answer. The minimum artifact is a decision memo (Memo) plus evidence appendix; the premium buyer-facing artifact is an executive decision deck derived from that substrate. | Memo format, evidence appendix, executive deck, decision accountability |
| 7 | Backtesting and Outcome Memory | Replay past decisions using only pre-cutoff evidence, compare with later outcomes (Outcome), record misses, and update the evidence standard. | Multi-case backtesting, calibration, outcome learning |
| 8 | Boundary Rules | Preserve public, market-level, non-deceptive intelligence and prevent implementation drift. | Ethics, anti-dossier boundary, no runtime authorization, no generic OSINT platform |

Competitive intelligence remains a major use case, but not a standalone core
primitive. It is handled through Signal Use Classification and actor-strategy
evidence. Engagement quality remains a rubric, not a primitive.

## Minimum Required Objects

Core Spine v0 requires only these product objects:

| Object | Purpose |
| --- | --- |
| Decision frame | Keeps analysis tied to allocation value. |
| Evidence admission or hold record | States whether external/purchased evidence is sufficient, bounded private context is required, or a decisive input is missing. |
| Evidence unit | Makes every claim inspectable. |
| Signal integrity assessment | Prevents cited-noise theater, copied-language overcounting, and manipulation blind spots. |
| Signal use classification | Uses `engagement_logic_registry_v0.md` to classify what a signal can support. |
| Decision strength assessment | Converts evidence quality into action threshold without false precision. |
| Decision artifact | Converts evidence into an accountable recommendation. The memo and evidence appendix are the reasoning substrate; the executive decision deck is the premium buyer-facing package when needed. |
| Backtest or outcome note | Creates learning loop and calibration record. |
| Boundary note | Keeps the work public, market-level, non-deceptive, and docs-first. |

## Satellite Requirements

Each production-bound satellite must provide:

- decision type;
- domain language;
- buyer, user, decision owner, and consequence;
- source families and source blind spots;
- decision-specific relevance rules;
- allowed recommendation verbs;
- success criteria and kill criteria;
- what counts as costly behavior in that domain;
- what actor or competitor behavior matters;
- outcome or backtest target when available.

A pre-GTM application profile may leave buyer, first decision family, and
commercial success criteria `UNKNOWN` while still binding domain assets,
admission rules, evidence families, and non-claims. It must not silently fill
those commercial fields from historical artifacts.

## Decision Artifact Model

Raw signals are not final evidence. Core Spine must admit, clean, classify,
source-back, and constrain messy or contradictory eligible inputs before they
can support a decision artifact. Missing decisive evidence produces a visible
hold, not an invented answer.

The decision memo remains the reasoning substrate, minimum viable artifact,
proof gate, and backtest artifact. It carries the recommendation, evidence
basis, alternatives, uncertainty, action ceiling, kill criteria, and what would
change the answer.

The evidence appendix remains mandatory for inspectability. It must preserve
source paths, provenance, signal-use classification, source-integrity notes,
and uncertainty boundaries sufficient for a decision owner or reviewer to
reconstruct the argument.

The executive decision deck is the premium buyer-facing artifact. It may make
the recommendation easier to circulate and decide from, but it must be derived
from the memo and evidence appendix. A deck cannot introduce unsupported
claims, hide uncertainty, or outrun the source-backed evidence boundary.

Core is the repeatable decision spine. Satellites adapt the spine to industry,
decision family, competitor set, and source families; GTM/product-proof binds
the buyer. Bespoke work is permitted only as bounded final adaptation; overage
or repeated custom work is consulting-risk evidence unless it reveals a
repeatable decision family.

## Initial Product Form And Evolution

The initial product form is a **Decision Sprint**: one admitted Decision Frame,
one evidence cutoff, one deadline-bound decision artifact, and one reveal or
outcome plan. The minimum buyer-facing package is the decision memo, mandatory
evidence appendix, evidence-world/gap note, decision trace, and reversal
conditions. A derived executive deck is optional and cannot outrun that
substrate.

The Sprint is complete only when it changes or defends an action, or truthfully
holds because a decisive input is missing. Source volume, a research report, a
dashboard, a feed, or a forecast without that action is incomplete.

A recurring Decision Desk is a later hypothesis gated on repeated admitted
decisions, recurring buyer cadence, reusable evidence structures, observable
reveals/outcomes, and bounded analyst labor. A software system or platform is
later still and is earned only when stable interfaces reduce labor, improve
consistency, or increase throughput without hiding uncertainty or missingness.
This progression is not implementation authorization.

## What Must Not Be Hardcoded From `jb`

Do not promote these into core:

- finance-career avatar names;
- `jb` pain wedges, copy angles, pricing, packaging, or workflow bets;
- `jb` lifecycle mechanics, handoff formats, paths, validation habits, or prompt templates;
- GAP/CV Engine policy or compiler assumptions;
- a single-domain standard for success.

`jb` may validate method usefulness. It does not define Forseti product authority.

## Product Proof Contract

Product proof must test the same decision family the paid Sprint would serve.
The smallest credible proof combines a predeclared Decision Frame, a sealed
pre-cutoff Sprint artifact, a later reveal or outcome, explicit production-
transfer limits, and—when live buyer work is authorized—observable decision- or
budget-adjacent behavior. No component receives a fixed numeric weight before
evidence supports one.

Backtesting is core product learning. It sharpens the evidence standard and
exposes misses, but must remain separate from cherry-picked demonstrations and
cannot by itself prove buyer pull or WTP.

## Backtesting Contract

Internal backtest question:

> Given only eligible evidence genuinely available before date X, would Forseti have produced
> a useful decision memo before the outcome was obvious?

For backtests, the decision memo remains the correct artifact because it
preserves reasoning and timestamp discipline. Any deck-shaped demo must be
derived after the memo and evidence appendix are sealed.

Backtests must record:

- decision context;
- cutoff date;
- source visibility before cutoff;
- excluded post-window evidence;
- recommendation Forseti would have made;
- confidence and action threshold;
- later outcome;
- whether Forseti was early, late, wrong, overconfident, or useful;
- what the evidence standard should learn.

Marketing demos may use selected wins. Internal product judgment should use
preselected cases, leakage controls, and misses.

## Explicit Non-Goals

Core Spine v0 does not authorize:

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
- generalized OSINT platform work.

Ideas may be stolen from those systems as product requirements or judgment
rubrics, but not built as v0 runtime machinery.

## Product Verdict

Current verdict: `PRODUCT_DIRECTION_AND_INITIAL_FORM_BOUND`.

The contract and initial Decision Sprint form are bound. The first buyer,
decision family, buyer proof, WTP, repeatability, distribution, production
economics, Decision Desk, and software form remain unproven. Feature or runtime
implementation still requires a separately accepted scope and explicit
authorization.
