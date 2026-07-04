# Core Spine v0 Product Contract

- Status: PROPOSED_FREEZE
- Artifact type: Product artifact
- Scope: Market-agnostic Core Spine contract for Forseti v0
- Source basis: current owner direction, `docs/decisions/turn_08_product_thesis_v0.md`, `docs/workflows/turn_08_workflow_bedrock_maximization.md`, `orca/product/shared/engagement_registry/engagement_logic_registry_v0.md`
- Implementation authorized: no

## Product Bet

Core Spine v0 is Forseti's reusable decision-evidence spine. It turns public market
signals into clean, classified, source-backed, and constrained decision
evidence without becoming a generic OSINT platform, deck shop, or `jb`-specific
finance-career intelligence tool.

Core Spine owns market-agnostic evidence mechanics. Satellites own
decision-specific context, language, source maps, buyers, success criteria, and
kill criteria.

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
| Evidence unit | Makes every claim inspectable. |
| Signal integrity assessment | Prevents cited-noise theater, copied-language overcounting, and manipulation blind spots. |
| Signal use classification | Uses `engagement_logic_registry_v0.md` to classify what a signal can support. |
| Decision strength assessment | Converts evidence quality into action threshold without false precision. |
| Decision artifact | Converts evidence into an accountable recommendation. The memo and evidence appendix are the reasoning substrate; the executive decision deck is the premium buyer-facing package when needed. |
| Backtest or outcome note | Creates learning loop and calibration record. |
| Boundary note | Keeps the work public, market-level, non-deceptive, and docs-first. |

## Satellite Requirements

Each satellite must provide:

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

## Decision Artifact Model

Raw public market signals are not final evidence. Core Spine must clean,
classify, source-back, and constrain messy or contradictory public inputs
before they can support a decision artifact.

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

Core is the repeatable decision spine. Satellites adapt the spine to buyer,
industry, decision family, competitor set, and source families. Bespoke work is
permitted only as bounded final adaptation; overage or repeated custom work is
consulting-risk evidence unless it reveals a repeatable decision family.

## What Must Not Be Hardcoded From `jb`

Do not promote these into core:

- finance-career avatar names;
- `jb` pain wedges, copy angles, pricing, packaging, or workflow bets;
- `jb` lifecycle mechanics, handoff formats, paths, validation habits, or prompt templates;
- GAP/CV Engine policy or compiler assumptions;
- a single-domain standard for success.

`jb` may validate method usefulness. It does not define Forseti product authority.

## Product Proof Weights

| Proof component | Weight | Purpose |
| --- | ---: | --- |
| Client 0 `jb` decision artifact plan | 30% | Tests concrete decision usefulness through the memo substrate, evidence appendix, and any deck-ready shape. |
| Source-quality and engagement evidence standard | 25% | Tests the core differentiator. |
| Core Spine contract | 15% | Establishes the reusable boundary. |
| Shadow satellite portability check | 15% | Tests non-`jb` generality. |
| Backtest replay | 15% | Tests timestamp discipline and outcome calibration. |

Backtesting is super core. It should be used to sharpen the evidence standard
and produce marketing examples, while keeping internal calibration separate
from cherry-picked demos.

## Backtesting Contract

Internal backtest question:

> Given only public evidence available before date X, would Forseti have produced
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

Current verdict: `NEEDS_PRODUCT_ARTIFACT`.

This file is a proposed product artifact. Feature planning is not appropriate
until the Core Spine contract, evidence standard, Client 0 proof plan,
shadow-satellite checks, backtest contract, fail-capable validation gates, and
explicit feature-planning authorization are accepted.
