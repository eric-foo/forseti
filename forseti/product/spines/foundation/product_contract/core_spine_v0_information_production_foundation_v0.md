# Core Spine v0 Information Production Foundation

- Status: PROPOSED_FREEZE
- Artifact type: Product-method foundation
- Scope: Manual information-production rules for Core Spine v0
- Source basis: current owner direction, `docs/product/core_spine_v0_product_contract.md`, `forseti/product/shared/engagement_registry/engagement_logic_registry_v0.md`, `docs/product/core_spine_v0_proof_protocol_v0.md`, `docs/product/core_spine_v0_proof_input_selection_v0.md`
- Implementation authorized: no
- Feature planning authorized: no
- Proof run authorized: no

## Purpose

This foundation defines how Orca manually turns raw public evidence into valid
intermediate intelligence objects before any proof run.

It is the product-method layer between Core Spine v0's contract and the proof
protocol. It gives operators or agents rules for producing Evidence Units (EvidenceUnit),
Signal Integrity assessments, Signal Use Classifications, Decision Strength
assessments, Action Ceilings, decision memo (Memo) sections, and backtest records.

## Non-Authority

This artifact does not authorize:

- proof-run execution;
- feature planning;
- implementation planning;
- source collection architecture;
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
- broad OSINT platform work.

Ideas from those systems may inform fields, rubrics, or judgment checks, but
they are not v0 runtime machinery.

## Production Sequence

Use this manual chain for every Core Spine v0 information product:

```text
Decision Frame
-> Evidence Unit
-> Signal Integrity
-> Signal Use Classification
-> Decision Strength
-> Action Ceiling
-> Decision Memo sections
-> Backtest Record, when applicable
```

Do not skip from raw signal to recommendation. Each recommendation must be
traceable through the chain.

## Decision Frame

Before creating Evidence Units, name the decision frame:

- allocation question;
- decision owner or decision context;
- consequence of action or inaction;
- allowed recommendation verbs;
- success criteria;
- kill criteria;
- satellite context, if any;
- what the decision frame does not prove.

If the decision frame is missing, evidence production is blocked. Do not create
free-floating evidence inventories.

## Evidence Unit Standard

An Evidence Unit is one atomic, inspectable public-signal observation tied to
one decision-use claim.

### Required Fields

Each valid Evidence Unit must include:

| Field | Requirement |
| --- | --- |
| Evidence Unit ID | Stable local identifier within the memo, proof packet, or backtest. |
| Decision-frame reference | The decision question this evidence may inform. |
| Source locator or source family | URL, citation, archive reference, source title, or source-family label when exact locator is unavailable. |
| Source actor or audience type | Who produced or carried the signal, when knowable. |
| Event or publication timestamp | When the signal happened or was published, when available. |
| Capture or access timestamp | When Orca observed or captured it. |
| Pre-cutoff visibility | Required for backtests and cutoff-sensitive claims. |
| Excerpt or observed pattern | Quoted excerpt, summarized pattern, or observable behavior with context. |
| Raw claim | What the source says or shows, separated from Orca interpretation. |
| Provenance | How the evidence was found or connected to the source. |
| Transformation history | Any summarization, translation, normalization, or interpretation applied. |
| Relevance to decision | Why this evidence can inform the decision frame. |
| Inclusion state | Included, discounted, excluded, blocked, or unresolved. |
| Source limitations | Known limits, missing context, incentive issues, or visibility constraints. |

### Optional Fields

Use when available:

- engagement counts;
- duplicate or cluster link;
- screenshot or capture reference;
- translation note;
- related counterevidence;
- audience segment;
- satellite-specific costly-behavior note;
- actor-strategy note;
- visibility class such as buyer-visible, market-visible,
  analyst-discoverable, archive-visible, or post-window.

### Evidence Unit States

| State | Meaning |
| --- | --- |
| Valid | Inspectable enough to support a bounded inference. |
| Invalid | Violates admissibility or boundary rules. |
| Blocked | Required source, timing, decision-frame, or owner input is missing. |
| Weak | Usable only with discounting and visible uncertainty. |
| Strong | Inspectable, decision-relevant, integrity-aware, and corroborated enough to affect Decision Strength. |

### Invalid Evidence Unit

An Evidence Unit is invalid when any of these are true:

- no inspectable source or source-family basis exists;
- no usable timing exists for cutoff-sensitive work;
- private, intrusive, ordinary-person dossier, or deceptive material is used;
- post-window evidence is mislabeled as pre-window;
- demand is inferred without source support;
- provenance is broken;
- `jb` assumptions are imported as Orca evidence;
- the evidence cannot be tied to a decision frame.

### Blocked Evidence Unit

An Evidence Unit is blocked when:

- source access is unavailable;
- source visibility cannot be established;
- the decision frame is missing;
- the evidence may violate Orca's product boundary;
- owner input is required to interpret domain-specific costly behavior or
  action threshold.

### Weak Evidence Unit

An Evidence Unit is weak when it has one or more of:

- single-source support;
- low detail;
- incentive distortion;
- copied language;
- poor audience fit;
- unresolved alternative explanations;
- unclear visibility;
- weak or missing costly behavior.

Weak evidence can still be useful for attention, distribution, actor strategy,
manipulation risk, or monitoring. It must not be overclaimed as demand.

### Strong Evidence Unit

An Evidence Unit is strong when it is:

- inspectable;
- pre-cutoff visible when relevant;
- tied to the relevant audience or actor;
- independently repeated or strongly corroborated;
- supported by detailed stakes or costly behavior when the claim is demand;
- paired with counterevidence review;
- honest about source limitations;
- reflected in the final Action Ceiling.

An Evidence Unit may not be marked `Strong` unless the counterevidence review
is recorded as an Evidence Unit note, memo-appendix note, or linked finding. If
counterevidence has not been checked, the strongest available state is `Weak`
until that review is completed.

## Signal Integrity Standard

Signal Integrity judges how much trust to place in an Evidence Unit or signal
pattern.

Judge only visible integrity signals. Do not pretend Orca has automated bot
detection, platform-private data, or hidden source access.

### Manual Integrity Labels

Use these labels, alone or in combination:

| Label | Meaning |
| --- | --- |
| Clean enough | No obvious integrity issue blocks bounded use. |
| Source-limited | Source is inspectable but narrow, incomplete, or context-limited. |
| Incentive-distorted | Rewards, affiliate incentives, promotion, or self-interest may distort the signal. |
| Copied or coordinated | Same language, timing, origin, or campaign mechanics reduce independence. |
| Campaign-driven | Signal likely reflects a campaign, launch, prompt, paid push, or coordinated distribution. |
| Artificial-amplification-risk | Bot-like, low-history, unnatural, or inflated activity may affect interpretation. |
| Ambiguous | Integrity risk exists but cannot be classified cleanly from available evidence. |
| Excluded | Integrity risk or boundary violation prevents use for recommendation support. |

### Integrity Rule

Signal Integrity must affect Decision Strength or Action Ceiling.

If integrity notes do not change the recommendation, discount, uncertainty,
action ceiling, or exclusion state, the integrity assessment is decorative and
invalid.

Every material integrity label must include an Integrity effect statement. The
statement must name the discount, uncertainty, exclusion state, Decision
Strength change, or Action Ceiling cap caused by that integrity label.

### Integrity Ceiling Anchors

Use these minimum anchors. Do not expand them into a full scoring matrix unless
a later Orca decision authorizes one.

- `Excluded` integrity cannot support a recommendation.
- `Ambiguous` integrity defaults to visible discounting and cannot support an
  Action Ceiling above `Probe` unless additional evidence clarifies the risk or
  an explicit owner decision records why proceeding is acceptable.
- `Copied or coordinated` and `Artificial-amplification-risk` cannot support
  `Commit`.
- `Copied or coordinated` and `Artificial-amplification-risk` cannot support
  `Move` unless independent corroboration survives the integrity concern.

## Signal Use Classification Standard

Signal Use Classification states what a signal can validly inform.

Every classified signal must include:

- strong for;
- weak for;
- not valid for;
- decision-use rationale;
- corroboration needed to upgrade confidence;
- discount factors.

### Allowed Signal Uses

Use these categories:

- demand evidence;
- attention evidence;
- resonance evidence;
- positioning evidence;
- objection evidence;
- distribution evidence;
- buyer-belief evidence;
- actor-strategy evidence;
- manipulation-risk evidence;
- social-proof evidence;
- weak or noisy evidence;
- exclusion evidence.

The same Evidence Unit may support multiple uses with different strengths.

### Demand Rule

Engagement never becomes demand by default.

Demand requires relevant audience fit plus stronger support such as:

- costly behavior;
- independent repetition;
- detailed pain;
- switching;
- payment;
- workaround creation;
- churn or abandonment;
- durable buyer-visible pressure;
- repeated objections with stakes.

High engagement, copied language, reward-driven comments, or campaign bursts
may support attention, distribution, actor strategy, or manipulation-risk
claims without supporting demand.

## Decision Strength Standard

Decision Strength is qualitative. It answers:

> What action can this evidence support without overclaiming?

Assess Decision Strength by weighing:

- decision-frame fit;
- audience fit;
- source visibility;
- costly behavior;
- independence;
- Signal Integrity;
- Signal Use Classification;
- counterevidence;
- alternative explanations;
- consequence of being wrong;
- reversibility of the recommended action.

Do not use numeric scores unless a later Orca decision accepts a scoring
method. For v0, use written rationale and Action Ceiling.

## Action Ceiling Standard

Action Ceiling is the strongest action the evidence can support.

| Ceiling | Allowed action | Minimum condition |
| --- | --- | --- |
| Excluded | Ignore for recommendation, or record only as pollution, manipulation, or source-quality evidence. | Evidence is invalid, boundary-unsafe, post-window leaked, or integrity risk prevents decision support. |
| Watch | Monitor. | Evidence is visible and relevant but too thin, weak, or uncertain for action. |
| Probe | Investigate. | Evidence is plausible and decision-relevant, but key uncertainty remains. |
| Test | Run a reversible test; delay irreversible commitment. | Evidence is directional enough for bounded learning with kill criteria. |
| Hold | Delay, narrow, or withhold action. | Counterevidence, integrity risk, or source limitation is material. |
| Move | Reposition or defend with bounded scope. | Evidence is strong enough for bounded action and alternatives have been handled. |
| Commit | Invest or commit. | Rare; requires clean-enough integrity, independence, costly behavior, audience fit, counterevidence handling, and material decision consequence. |

### Action Ceiling Preconditions

Before `Watch`:

- at least one valid signal exists;
- there is a clear reason not to act yet.

Before `Probe`:

- a specific uncertainty is named;
- additional evidence that would resolve it is identified.

Before `Test`:

- directional evidence exists;
- test scope is reversible;
- kill criteria are named.

Before `Hold`:

- material counterevidence, alternative explanation, or integrity risk is
  present.

Before `Move`:

- evidence is strong enough for bounded action;
- major alternatives are handled;
- action is still constrained.

Before `Commit`:

- evidence is strong across integrity, independence, costly behavior, audience
  fit, and consequence;
- counterevidence is handled;
- irreversible downside is justified.

Do not allow `Commit` from engagement alone.

## Memo Production Rules

Every decision memo must include:

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
13. Evidence appendix.
14. Boundary note naming what the memo does not prove.

The recommendation verb must not exceed the Action Ceiling. If the decision
frame allows a stronger verb than the evidence supports, the memo must use the
ceiling-constrained verb and state that stronger action is unsupported.

A memo is invalid if a skeptical reader cannot reconstruct the recommendation
from the Evidence Units and inference chain.

## Backtest Production Rules

A backtest record must capture:

- case-selection policy;
- pre-registration status;
- decision context;
- cutoff date;
- why the cutoff is fair;
- source visibility before cutoff;
- included pre-cutoff Evidence Units;
- excluded post-window evidence;
- recommendation Orca would have made at cutoff;
- Action Ceiling at cutoff;
- later outcome (Outcome);
- whether Orca was early, late, wrong, overconfident, underconfident, useful,
  or inconclusive;
- evidence-standard lesson.

Internal backtests must preserve misses. Cherry-picked wins may become
marketing demos only when labeled as marketing demos and excluded from internal
calibration unless they pass leakage controls.

### Leakage Controls

A backtest case (Case) passes leakage controls only when all of these are recorded:

- the case was selected by a pre-stated policy before evidence interpretation;
- the cutoff date was frozen before the at-cutoff evidence was interpreted;
- post-window evidence was explicitly listed and excluded from the at-cutoff
  judgment;
- the result was recorded, including misses, inconclusive results,
  overconfidence, and underconfidence.

Cases selected because the later outcome already looks persuasive may be used
as marketing demos when labeled that way, but they must not train internal
calibration.

## Invalid / Blocked / Inconclusive Rules

### Invalid

Invalid means the object violates admissibility or boundary rules.

Examples:

- no inspectable source;
- no decision frame;
- post-window leakage;
- unsupported demand inference;
- private or deceptive evidence;
- `jb` assumptions imported as Orca evidence;
- integrity note that does not affect inference.

### Blocked

Blocked means required source, timing, decision-frame, or owner input is
missing.

Examples:

- cutoff visibility cannot be established;
- satellite-specific costly behavior is undefined;
- source access is unavailable;
- action-threshold language requires owner input;
- boundary risk is unresolved.

### Inconclusive

Inconclusive means the object is valid but cannot support a stronger
recommendation.

Examples:

- evidence supports `Watch` or `Probe` but not `Test`, `Move`, or `Commit`;
- integrity risk prevents stronger action;
- counterevidence is material;
- source set is too thin;
- memo narrows uncertainty without producing an allocation recommendation.

Inconclusive is a valid learning outcome. It does not authorize proof-run
success, feature planning, or implementation.

## Boundary Rules

This foundation must stay manual and docs-first.

It must not become:

- a source collection playbook;
- a scraper design;
- a database schema;
- a dashboard concept;
- a scoring engine;
- an automation workflow;
- a feature plan;
- a proof-run output;
- a case library;
- a marketing artifact.

## Bloat Cuts

Cut from this foundation:

- source inventories;
- broad OSINT playbooks;
- exact platform tactics;
- numeric formulas;
- runtime architecture;
- implementation units;
- full memo drafts;
- case-library packaging;
- marketing copy;
- feature-planning labels.

Keep:

- production sequence;
- object validity rules;
- downgrade and exclusion mechanics;
- manual inference rubrics;
- memo preconditions;
- backtest record rules;
- boundary and non-authority statements.

## Open Owner Decisions

- Exact confidence vocabulary beyond Action Ceiling: UNKNOWN - requires owner input.
- Final memo format: UNKNOWN - requires owner input.
- Backtest case or case-selection policy details: UNKNOWN - requires owner input.
- Satellite-specific costly behavior examples: UNKNOWN - requires owner input.
- Whether status vocabulary should normalize `NEEDS_PRODUCT_ARTIFACT`,
  `NEEDS_FOUNDATION_ARTIFACT`, and `NEEDS_FOUNDATION_ACCEPTANCE`: UNKNOWN -
  requires owner input.

## Current Verdict

Current verdict: `NEEDS_FOUNDATION_ACCEPTANCE`.

This artifact defines the manual information-production foundation for Core
Spine v0. It does not claim proof-run readiness, feature-planning readiness, or
implementation readiness.
