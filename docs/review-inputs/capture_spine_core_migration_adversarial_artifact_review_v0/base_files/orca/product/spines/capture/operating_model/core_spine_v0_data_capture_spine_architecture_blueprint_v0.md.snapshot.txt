# Core Spine v0 Data Capture Spine Architecture Blueprint

```yaml
retrieval_header_version: 1
artifact_role: Product architecture blueprint
scope: Canonical v0 product-method blueprint for Data Capture Spine architecture, obligations, capture modes, satellite boundaries, and rejected patterns.
use_when:
  - Preparing the Data Capture Spine obligation contract.
  - Checking whether proposed Data Capture, ECR, Cleaning, Judgment, source-family, or runtime work preserves the Core Spine layer split.
  - Deciding whether a capture rule belongs in core, satellite, deferred runtime, or another layer.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - orca/product/spines/capture/operating_model/core_spine_v0_data_capture_context_preservation_note_v0.md
  - .agents/workflow-overlay/source-loading.md
stale_if:
  - Orca renames Data Capture Spine, Evidence Candidate Record, Cleaning Spine, or Judgment Spine.
  - A later accepted Data Capture Spine obligation contract supersedes this blueprint.
  - Orca authorizes standing/opportunistic capture as part of Data Capture Spine rather than a separate intake lane.
```

- Status: CANONICAL_BLUEPRINT_V0
- Artifact type: Product architecture blueprint
- Scope: Data Capture Spine setup architecture for commissioned, decision-framed capture
- Source basis: Data Capture setup adjudication, owner corrections, `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`, `docs/product/core_spine_v0_data_capture_context_preservation_note_v0.md`
- Implementation authorized: no
- Feature planning authorized: no
- Runtime/source-system design authorized: no

## Purpose

This blueprint defines the v0 architecture for **Data Capture Spine**.

It is the source to open before writing the Data Capture Spine obligation
contract. It is not itself the obligation contract, an Evidence Candidate
Record schema, a Cleaning design, a Judgment ruleset, a source inventory, or a
runtime plan.

## Layer Definition

Data Capture Spine is the product-method layer that makes public/external
signals capturable, inspectable, preserved, contextualized, and safe to hand to
Evidence Candidate Record.

Core principle:

```text
Capture is the obligation. Mode is subordinate.
```

Capture modes may vary. They do not define the product. A mode is acceptable
only when it can discharge the relevant evidence-grade capture obligations for
the decision-framed signal.

Do not use stale "Data Spine" language when it implies Evidence Object Model,
Evidence Unit (EvidenceUnit) content contract, source collection runtime, or generic data
platform.

## Operating Scope

Data Capture Spine v0 is **commissioned-capture-only**.

Commissioned capture means capture for a specific Decision Frame that already
exists. In this mode, heavy evidence-grade obligations make sense because the
decision question, consequence, cutoff, and downstream use are real inputs.

Standing or opportunistic capture is not part of Data Capture Spine v0. If
Orca later wants to collect public signals before a decision frame exists, that
should become a separate Candidate Signal Intake or Corpus Intake contract.
Those items are not ECR-ready evidence. They must be rebound or recaptured under
a Decision Frame before entering Data Capture Spine.

Reason: a single contract covering both commissioned and standing capture would
either weaken commissioned capture or make standing capture infeasible. For v0,
protect the commissioned obligation standard.

## Architecture

```text
Decision Frame
-> Data Capture Spine: obligation-complete signal discovery, access, capture,
   preservation, context, visibility, timing, archive/cutoff posture, and
   categorical handoff
-> Evidence Candidate Record
-> Cleaning Spine
-> Judgment Spine
-> Decision Artifact
-> Outcome Memory
```

Data Capture Spine records capture facts, capture limits, and capture posture.
It does not decide credibility, discounting, exclusion, Signal Use
Classification, Decision Strength, or Action Ceiling.

## Core Obligations

Core owns invariant obligations that must hold across commissioned captures:

- decision-frame gating;
- current Orca source-access boundary compliance;
- capture-event provenance: who captured, with what tool or mode, in what
  session, and under which obligation version;
- capture-mode disclosure: human-led, agent-assisted, structured access,
  archive/history, automated extraction, multimodal, or mixed;
- mode-change disclosure when the capture mode changes within a session;
- raw observable fidelity;
- source claim separated from Orca interpretation;
- source identity and source-actor preservation where knowable;
- decomposed timing where visible: source publication, source last edit,
  capture timestamp, and re-capture timestamp;
- cutoff posture as a first-class capture fact;
- source visibility limits and source-access limits;
- archive posture recorded for every capture: archived, attempt failed, not
  attempted, or not applicable;
- edit, delete, cache, snapshot, and historical visibility posture where
  visible;
- related context preservation when context changes signal meaning;
- bundled-offer structure and visible packaging-cue preservation when a source
  presents a multi-term proposal;
- modality preservation when text alone loses the signal;
- capture failure and blocker visibility;
- re-capture semantics when source state, archive state, or decision frame
  materially changes;
- categorical handoff readiness for Evidence Candidate Record;
- explicit non-claims.

Core must stay market-agnostic. It states what must be true for a captured
signal to be evidence-grade input. It does not encode every source-family
heuristic as core law.

## Captured But Unusable

A signal can be properly captured and still be unusable downstream.

Data Capture should not be blamed for downstream unusability when it has
discharged capture obligations and made limits visible. Examples include weak
audience fit, poor independence, credibility concerns, insufficient costly
behavior, post-cutoff status, or invalid decision use. Those effects belong to
Judgment, ECR consolidation, or the relevant downstream layer.

The obligation contract should preserve this boundary explicitly.

## Satellite Adaptation

Satellites own bounded source-family and decision-family adaptation:

- source-family access and feasibility notes;
- source-family blind spots;
- source-family capture-fidelity heuristics;
- threaded forum or community conventions;
- review-platform moderation, sorting, incentive, and recency conventions;
- docs, changelog, version, deprecation, and cache conventions for a product
  category;
- domain-native language interpretation notes when traceability requires them;
- decision-family language, buyer context, and consequence;
- when human-assisted capture is required for a source family;
- when historical capture is feasible, weak, or unavailable for a source family.

Satellite rules may inform core later, but empirical source-family heuristics
should not be promoted into core until they survive comparison across at least
two non-overlapping source families or the owner explicitly accepts an
exception for one specific invariant claim.

## Capture Modes

Every capture mode is subordinate to obligation discharge.

### Archive / Historical Capture

Archive/history capture is core as a conceptual obligation because
cutoff-sensitive decisions and backtests need to know what was visible when the
decision window mattered.

Runtime tooling is deferred. The product-method obligation is not deferred.

### Human-Assisted Capture

Human-assisted capture is v0 bootstrap, training, governance, quality control,
and escalation for ambiguous, volatile, multimodal, or high-stakes signals.

It should not become Orca's permanent core philosophy. Source families should
graduate toward agent-allowed or automated capture only when repeated captures
show the engine can discharge capture obligations without human correction of
capture sufficiency.

### Agent-Assisted Capture

Agents may: enumerate, fetch, archive, transcribe, link, and mechanically group
exact URLs or identical locators.

Agents must not: rank relevance, filter candidates before presentation,
summarize for admissibility, decide missing context, classify credibility,
exclude signals, or decide downstream use.

Agent-assisted sessions should log query/session context, result batches,
fetched candidates, discarded candidates, and discard reason categories. Silent
pre-filtering is not allowed.

### Structured Access

Structured access is useful when official or clean surfaces exist, but source
availability must not define evidence validity.

APIs, feeds, exports, and orderly source surfaces may be future modes; they are
not the architecture.

### Autonomous Extraction

Autonomous extraction is a future runtime capability only after obligations are
locked.

It is dangerous as a philosophy because it can create fake confidence through
volume while hiding lost context, access bias, or failure to preserve raw
observables.

### Multimodal Capture

Multimodal capture is a triggered obligation when the signal is carried by
image, layout, audio, video, dynamic rendering, visual state, or interaction.

It is not a universal priority over text. It is required when text-only capture
would lose the signal.

## Context Preservation

Data Capture should preserve the smallest source context that keeps the signal
inspectable, meaningfully situated, and safe from misread downstream.

### Bundled Offers And Multi-Term Proposals

When a source presents a counterparty offer, package, settlement, public-sector
deal, regulatory bargain, or similar multi-term proposal, Capture should
preserve source-visible bundle membership, term framing, dependencies,
conditions, severability, sunset or fallback posture, source language, visible
packaging cues, and sequence where visible. The atomic unit is the bundle as
presented before any term-level extraction.

Capture preserves packaging as observable source context. Judgment decides what
the packaging means, whether it supports a counterparty-concession read, and
whether it changes decision use.

### Threaded Forums And Communities

Capture should preserve the related chain, not the entire forum.

Preserve the original post or parent claim, relevant reply chain, corrections,
rebuttals, confirmations, official or moderator replies, resolved or locked
state, edit/deletion posture, actor/audience category when knowable, and timing
where visible.

Operational floor: ECR should be able to reconstruct what the source was
claiming from the slice without re-fetching.

Fairness ceiling: a reasonable observer should agree that the slice represents
what was said.

### Review Surfaces

Review capture should not collapse into aggregate star ratings.

Core captures recency posture and visible experience timing. Satellites and
Judgment decide what recency means for a source family or decision.

Recent negative reviews can reveal live regressions, support failures, quality
breaks, pricing shocks, or operational pain. Long-context five-star reviews can
matter equally when they explain concrete success conditions, buyer fit,
adoption context, or high-value use.

Capture should preserve moderation, incentive, sorting, filtering,
verification, vendor-response, recency, and visible experience-timing posture
where available.

### Changelogs, Docs, And Versioned Pages

Capture must preserve timing and version posture for docs, changelogs, pricing
pages, API docs, policies, and similar public pages.

These pages mutate, can be backfilled, and can leak post-window knowledge into
a pre-cutoff analysis. Preserve whether the content is current, future, beta,
deprecated, removed, edited, backfilled, cached, archived, or prior-versioned
where visible.

### Domain-Native Language

Preserve domain-native language exactly when it carries signal.

Do not sanitize expert terminology into generic paraphrase. Add a short
interpretation note only when needed for traceability, and never replace the
source's language with Orca's gloss.

## Handoff To Evidence Candidate Record

The handoff to Evidence Candidate Record must accomplish these things
categorically:

- make the captured signal inspectable downstream;
- preserve raw observable and related context;
- keep source claim separate from Orca interpretation;
- preserve source identity, actor category, visibility, timing, modality, and
  cutoff/archive posture where knowable;
- expose capture limits and blockers;
- show whether capture obligations were `met`, `partial`,
  `assessed_not_met`, `cannot_assess`, `access_failed`, `blocked`,
  `unavailable_by_source`, `not_applicable`, or `not_attempted`;
- allow Cleaning to proceed without recollecting source history;
- avoid making credibility, discounting, exclusion, or decision-use claims.

This blueprint does not define ECR fields, keys, IDs, tables, data types,
receipt structures, storage, schema, or file formats.

## Rejected Architecture Patterns

### Autonomous Technical Extraction As Philosophy

Reject because it optimizes for capture volume and machine tractability. It can
hide context loss, access bias, dynamic-page failure, deleted-state failure,
and raw-observable loss while producing a false sense of confidence.

### Structured Access As Philosophy

Reject because APIs, feeds, exports, and official surfaces bias capture toward
what platforms expose. Clean availability is useful, but availability must not
define evidence validity.

### Agent-Directed Discovery As Philosophy

Reject because it lets an agent decide what matters before downstream layers
see the signal. Agent work is allowed only as bounded assistance with visible
candidate logs and no silent pre-filtering.

### Multimodal Priority As Philosophy

Reject because it overcorrects. Multimodal capture is required when modality is
load-bearing; it is not a universal priority over textual or structured public
signals.

### Human-Assisted Capture As Permanent Philosophy

Reject because it turns Orca into bespoke research labor. Human assistance is
v0 bootstrap, training, governance, and escalation, not the permanent core.

### Generic Hybrid Mode Mixing

Reject because "use whatever works" erases the obligation standard. The only
acceptable hybrid is obligation-first: modes are permitted only when they
discharge capture obligations.

### Source Maps Or Inventories As Core

Reject because they turn Data Capture Spine into collection planning. Source
maps and inventories may become satellite or runtime artifacts later; they are
not the core architecture.

### Source Volume As Evidence Validity

Reject because more sources can still produce weaker evidence. Orca needs
inspectable, constrained decision evidence, not source-count theater.

### Runtime Design As This Layer

Reject because APIs, scrapers, adapters, storage, dashboards, automation, and
tests are future implementation surfaces. This blueprint defines
product-method obligations only.

### Capture-Time Credibility Scoring

Reject because Capture records visible facts and limits. Judgment decides
credibility effects, discounting, exclusion, and valid use.

### ECR, Cleaning, Or Judgment By Stealth

Reject any capture artifact that starts defining receipt fields, transforming
raw signals, deduplicating semantically, classifying integrity, discounting,
excluding, or deciding action support.

### Paper Contract Before Real Signals

Reject as a philosophy because a clean contract can break on first capture.
The obligation contract should be drafted and then tested against a small set
of real captures, treating failures as contract evidence.

### Capture As Adversarial Defense

Reject because it optimizes for defending Orca from challenge instead of
enabling downstream judgment. Auditability matters, but capture exists to
preserve usable evidence, not to maximize legalistic armor.

## Deferred

Defer:

- standing/opportunistic corpus capture;
- final ECR / Evidence Unit field architecture;
- Cleaning Spine normalization, dedupe, clustering, translation, and
  summarization mechanics;
- Judgment Spine integrity labels, discounting, exclusion, Signal Use
  Classification, Decision Strength, and Action Ceiling;
- runtime access mechanisms, scrapers, APIs, adapters, storage, dashboards,
  automation, deployment, and tests;
- source maps, inventories, and source-family playbooks;
- archive/history tooling implementation;
- commercial readiness or buyer validation claims.

## Open Design Knobs

The obligation contract should resolve or carry these explicitly:

- Which capture obligations are mandatory core in v0.
- Whether archive/history capture requires an archive attempt, a recorded
  attempt, or only a posture mark.
- Whether agent-assisted capture is permitted in v0 and which discharge checks
  are required.
- Which source families require human-assisted capture by default until the
  engine is trained and checked.
- Where ECR should draw the line between related-chain context and irrelevant
  source exhaust.
- Which review-surface recency and long-context rules belong in core versus
  source-family satellites.
- Whether Snapshot Integrity Class belongs in Data Capture core, ECR, or later
  Judgment/ECR consolidation.
- What re-capture requires when source state, archive state, or decision frame
  changes.
- What mode-change rules apply inside a capture session.

## Next Artifact

The next artifact should be:

```text
docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
```

It should turn this blueprint into categorical obligations and discharge
states. It should not design ECR fields, Cleaning mechanics, Judgment rules,
source inventories, runtime systems, or implementation plans.

## Non-Claims

This blueprint does not prove buyer validation, willingness to pay, repeatable
demand, product readiness, feature readiness, implementation readiness,
commercial readiness, source-system feasibility, data rights, runtime
feasibility, Core Spine validation, Judgment Spine validation, Evidence
Candidate Record completion, or Evidence Unit design completion.

It does not authorize implementation, runtime design, source maps, schemas,
scrapers, APIs, storage, dashboards, automation, tests, deployment, proof runs,
feature planning, commits, pushes, PRs, or readiness claims.
