# Core Spine v0 Data Capture Context Preservation Note

```yaml
retrieval_header_version: 1
artifact_role: Product-method note
scope: Capture-context preservation rules for Data Capture Spine handoff into future Evidence Candidate Record and Cleaning Spine work.
use_when:
  - Designing or reviewing Data Capture Spine obligations for threaded, reviewed, versioned, domain-specific, human-assisted, or historical public signals.
  - Preparing future Evidence Candidate Record or Cleaning Spine work that must preserve enough capture context without carrying irrelevant source exhaust.
  - Checking whether source-family adaptation is core, satellite, or deferred runtime work.
authority_boundary: retrieval_only
open_next:
  - docs/product/foundation/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - docs/product/foundation/core_spine_v0_product_contract.md
```

- Status: PROPOSED_NOTE
- Artifact type: Product-method note
- Scope: Data Capture context preservation and downstream reduction constraints
- Source basis: owner direction from the Data Capture setup adjudication turn, Core Spine v0 Data Capture/Cleaning boundary, Core Spine product contract
- Implementation authorized: no
- Feature planning authorized: no
- Runtime/source-system design authorized: no

## Purpose

This note preserves capture-context rules that future Evidence Candidate Record
and Cleaning Spine work should open before turning captured public signals into
receipt, cleaning, or transformation artifacts.

The core idea is simple: Data Capture should preserve enough surrounding
context for the signal to remain inspectable and interpretable, while later
Evidence Candidate Record and Cleaning work should reduce that context to the
related chain or relevant source slice instead of carrying unrelated source
exhaust.

## What This Note Is Not

This note is not:

- an Evidence Candidate Record schema;
- a field list;
- a Cleaning Spine design;
- a Judgment Spine rule;
- a source inventory;
- a scraper, archive, API, storage, dashboard, or automation plan;
- a runtime implementation authorization.

Capture records what was visible and what context was needed. Cleaning and
Judgment decide later transformation and inference effects under their own
layers.

## Core Context Rule

Capture must preserve the smallest source context that keeps the signal
inspectable, meaningfully situated, and safe from misread downstream.

That does not mean copying an entire forum, review corpus, docs site, or
historical archive when only one related chain matters. It means preserving the
related chain, surrounding state, source-visible constraints, and timing context
needed for a later reviewer to understand what the signal actually showed at
capture time.

## Bundled Offers And Multi-Term Proposals

Bundled offers need structure context because the source-visible packaging can
change what a later reviewer can inspect. A term inside a package, settlement,
public-sector deal, regulatory bargain, counteroffer, or similar multi-term
proposal is not only a standalone term when the source frames it as part of a
trade, condition, restriction, safeguard, concession, sweetener, penalty, or
fallback.

Capture should preserve, categorically:

- which terms appeared together in the same source-visible bundle;
- how the source framed each term's role in the bundle;
- visible dependencies, severability, conditionality, sunsets, fallback states,
  and acceptance constraints;
- the source's own language for why a term was included when visible;
- visible packaging cues where they carry meaning, including headings, labels,
  bullet order, nesting, emphasis, table placement, grouping, and proximity;
- sequence across drafts, votes, memos, public statements, or negotiation
  artifacts when visible.

The atomic unit is the bundle as presented, not only the term as extracted.

Downstream reduction rule: future Evidence Candidate Record and Cleaning work
should preserve the bundle structure needed to inspect the source-visible trade
or dependency. They should not infer motive, price concessions, or negotiation
strategy from the packaging.

## Threaded Forums And Communities

Threaded sources need chain context because a single post or comment may change
meaning based on surrounding replies.

Capture should preserve, categorically:

- the original post, parent claim, or prompt that created the thread;
- the related reply chain around the signal;
- direct corrections, rebuttals, confirmations, or resolutions;
- vendor, maintainer, moderator, or official responses when visible;
- lock, deletion, edit, merge, accepted-answer, or resolved-state posture when visible;
- actor or audience category when knowable;
- event, publication, and capture timing when visible.

Why: a complaint, workaround, or praise item may be reversed, narrowed,
confirmed, or made irrelevant by the surrounding chain. Capturing only one
sentence can turn a rebutted claim into fake evidence, or hide that many
independent users confirmed the same issue.

Downstream reduction rule: future Evidence Candidate Record and Cleaning work
should preserve the related chain or relevant source slice, not the entire
forum or unrelated discussion.

## Review Surfaces

Review surfaces need visible moderation and incentive context because star
ratings and review text are shaped by platform rules, recency, reviewer
selection, vendor behavior, and sorting.

Capture should preserve, categorically:

- rating and review text together when both are visible;
- review recency and visible experience timing when available;
- long-context positive and negative reviews, not only low ratings;
- recent one-star or low-rating reviews when they describe live regressions,
  support failures, quality breaks, pricing shocks, or operational pain;
- long five-star reviews when they explain concrete success conditions, buyer
  fit, adoption context, or high-value use;
- verified, unverified, invited, incentivized, platform-moderated, or
  vendor-responded posture when visible;
- sorting, filtering, removal, or moderation constraints when visible.

Why: aggregate stars can hide the signal that matters for a decision. Recent
negative reviews may reveal a live product or service failure. Long positive
reviews may be equally important when they explain why the product works for a
specific audience or use case. Capture records these visible constraints;
Judgment later decides credibility, weight, discounting, and valid use.

## Changelogs, Docs, And Versioned Public Pages

Docs and changelogs need version and timing context because they mutate, can be
backfilled, and can expose post-window information.

Capture should preserve, categorically:

- event or publication timing when visible;
- capture timing;
- page update, version, deprecation, or future-state posture when visible;
- whether the content describes current, future, beta, deprecated, or removed
  behavior;
- historical snapshot, archive, cache, or prior-version availability when used;
- whether the source appears edited, backfilled, or materially changed after
  the relevant decision window.

Why: docs can silently change after the fact. Without version/cutoff discipline,
Orca can accidentally treat later knowledge as pre-cutoff evidence or misread a
future/planned state as current behavior.

## Domain-Native Language

Capture should preserve domain-native language, jargon, abbreviations, and
buyer/operator phrasing exactly when that language carries signal.

The risk is not that expert buyers dislike jargon. Expert buyers often trust
precise domain language more than generic paraphrase. The risk is that Orca, a
future reviewer, or a cross-domain artifact may flatten or misread the term.

Downstream work may add a short interpretation note when needed for
traceability, but it must not replace the source's language or normalize away
domain meaning.

## Human-Assisted Capture

Human-assisted capture is the v0 bootstrap and training posture, plus the
future escalation path for ambiguous, volatile, multimodal, or high-stakes
signals.

Humans help:

- identify which surrounding context is load-bearing;
- handle source surfaces where automation loses meaning;
- spot moderation, timing, deletion, edit, and modality issues;
- teach and maintain the future capture engine;
- perform quality control when the engine cannot discharge capture obligations
  confidently.

Human-assisted capture is not the permanent philosophy of the spine. The core
philosophy remains obligation-complete evidence capture. Over time, the engine
should satisfy more obligations repeatably, with humans governing, training,
maintaining, and escalating when needed.

## Archive And Historical Capture

Archive/history-based capture is core as a concept because cutoff discipline
depends on knowing what was publicly visible at the relevant time.

Capture may need to reason about:

- public archives;
- cached pages;
- version histories;
- historical changelog or docs states;
- removed, edited, deleted, or visibility-shifted public material;
- source surfaces visible in the prior decision window.

Why: if a signal disappeared, changed, or was only visible during the relevant
window, Orca still needs a public, non-deceptive way to preserve or recover what
was visible. Runtime tooling for historical capture is deferred, but the
conceptual obligation is core.

## Core Vs Satellite Reading

Core owns the invariant obligations:

- preserve the raw observable and related context;
- keep source claim separate from Orca interpretation;
- preserve event/capture/cutoff timing where visible;
- expose visibility, deletion, edit, archive, and moderation constraints;
- preserve source-visible bundle membership, framing, dependencies, and
  packaging cues when a source presents a multi-term proposal;
- preserve modality when modality carries the signal;
- keep capture inside the current Orca source-access boundary;
- hand off enough categorical context for later Evidence Candidate Record,
  Cleaning, and Judgment work without designing those layers here.

Satellites own source-family adaptation:

- which thread context is load-bearing for a specific community;
- how review-platform constraints appear in a market or industry;
- which offer, settlement, regulatory, or public-sector deal conventions require
  source-family-specific capture guidance;
- which docs/version conventions matter in a product category;
- what domain-native language requires a traceability gloss;
- when human escalation is required for a source family;
- when historical capture is feasible or unreliable for a source family.

Source-family heuristics should not be promoted into core unless they survive
comparison across at least two non-overlapping source families or the owner
explicitly accepts an exception.

## Open Owner Decisions

- Which additional capture-context categories become mandatory in the Data
  Capture Spine obligation contract.
- Whether archive/history capture imposes a mandatory archive attempt, a
  recorded-attempt obligation, or only a categorical posture mark.
- Where the future Evidence Candidate Record should draw the line between
  related chain context and irrelevant source exhaust.
- Which review-surface recency and long-context rules belong in core versus
  source-family satellites.
- Which source families require human-assisted capture by default until the
  engine is trained and checked.

## Non-Claims

This note does not prove buyer validation, product readiness, feature
readiness, implementation readiness, commercial readiness, source-system
feasibility, data rights, runtime feasibility, or Core Spine validation.

It does not authorize implementation, runtime design, source maps, schemas,
scrapers, APIs, storage, dashboards, automation, tests, deployment, proof runs,
feature planning, commits, pushes, PRs, or readiness claims.
