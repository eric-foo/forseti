# Core Spine v0 First Proof Run Locks

- Status: LOCKS_REVIEWED_AWAITING_PROOF_RUN_AUTHORIZATION
- Artifact type: Product proof-run lock record
- Scope: First Core Spine v0 proof-run starting conditions before evidence collection or interpretation
- Date context: 2026-05-21, Asia/Singapore
- Output mode: file-write
- Edit permission used: docs-write for this target artifact only
- Implementation authorized: no
- Feature planning authorized: no
- Evidence collection authorized by this artifact: no
- Source collection systems authorized: no

## 1. Status, Scope, Source Basis, And Non-Authority

This record freezes only the proof-run starting conditions that can be locked
before evidence work. It exists to prevent cherry-picked backtest case (Case)
selection, cutoff selection after seeing evidence, post-window leakage, broad
competitor monitoring, `jb` authority leakage, and source-map or tooling drift.

Source basis:

- current owner instruction on 2026-05-21 accepting the first proof-run charter
  in chat and authorizing one bounded manual docs-first proof run under that
  charter;
- current owner instruction on 2026-05-21 selecting `BT2-04` Shutterstock
  response to generative image AI as the historical backtest case and
  authorizing a lock-record patch;
- current owner instruction on 2026-05-21 selecting `SH-01` Intercom Fin AI
  Agent pressure on Zendesk customer service positioning as the
  shadow-satellite case and authorizing a lock-record patch with explicit
  volatility controls;
- current owner instruction on 2026-05-21 accepting the read-only SH-01 lock
  review, committing the SH-01 lock milestone, and authorizing this
  review-gate reconciliation patch;
- `AGENTS.md`;
- `.agents/workflow-overlay/README.md`;
- `.agents/workflow-overlay/project-authority.md`;
- `.agents/workflow-overlay/source-of-truth.md`;
- `.agents/workflow-overlay/artifact-roles.md`;
- `.agents/workflow-overlay/validation-gates.md`;
- `.agents/workflow-overlay/safety-rules.md`;
- `.agents/workflow-overlay/communication-style.md`;
- `docs/decisions/turn_08_product_thesis_v0.md`;
- `docs/product/core_spine_v0_product_contract.md`;
- `orca/product/shared/engagement_registry/engagement_logic_registry_v0.md`;
- `docs/product/core_spine_v0_information_production_foundation_v0.md`;
- `docs/product/core_spine_v0_proof_protocol_v0.md`;
- `docs/product/core_spine_v0_proof_input_selection_v0.md`;
- `docs/product/core_spine_v0_proof_packet_preflight_v0.md`;
- `docs/product/core_spine_v0_first_proof_packet_preparation_v0.md`;
- `docs/product/core_spine_v0_first_proof_run_charter_v0.md`;
- `docs/product/core_spine_v0_heavyweight_proof_case_discovery_results_v0.md`;
- `docs/product/core_spine_v0_heavyweight_proof_case_discovery_results_part_2_v0.md`;
- repository check: `git status --short --branch` reported
  `## main...origin/main [ahead 9]` and untracked
  `docs/prompts/hygiene-queue/`;
- recent log check: `git log --oneline -8` included
  `b7d3395 docs: lock SH-01 shadow case`,
  `7492093 docs: lock Shutterstock backtest case`,
  `f596149 docs: add AI-era proof case discovery refresh`,
  `c43cfc6 docs: add proof case discovery results`, and
  `913cfc4 docs: add proof discovery gate`.

Non-authority:

- This record does not collect evidence.
- This record does not interpret proof evidence.
- This record does not draft a decision memo (Memo).
- This record does not execute a backtest.
- This record does not create a source map, source system, source inventory, or
  tooling plan.
- This record does not authorize scrapers, APIs, databases, dashboards, scoring
  engines, automation runtimes, software tests, feature plans,
  implementation plans, or implementation work.
- This record does not import `jb` project paths, lifecycle mechanics,
  templates, validation habits, or success logic into Orca or Core Spine
  authority.

## 2. Charter Acceptance Note

The owner has accepted
`docs/product/core_spine_v0_first_proof_run_charter_v0.md` in chat after the
charter was reviewed and committed.

The local charter file still records `READY_FOR_OWNER_ACCEPTANCE`, but this is
not treated as a conflict with the accepted scope for this turn. The current
owner instruction is the controlling source for this lock record and states
that the charter has been accepted. The accepted scope remains limited to:

- one `jb` Client 0 memo dry run;
- one competitor narrative response shadow memo dry run;
- one leakage-controlled backtest replay;
- one outcome report or review packet.

Evidence collection may not begin until this lock record is complete. This
record has now recorded and reviewed the required shadow-satellite and
backtest locks, but evidence collection and interpretation remain inactive
until the owner explicitly authorizes proof-run start.

## 3. No-Evidence-Interpreted Declaration

No proof evidence has been collected or interpreted for this lock record.

This turn read only Orca authority files, product artifacts, the proof-run
charter, and repository state. It did not inspect buyer-visible competitor
evidence, `jb` market evidence, historical case evidence, post-window outcome (Outcome)
evidence, source URLs, exact source maps, or source systems.

No at-cutoff recommendation, shadow-satellite recommendation, backtest result,
calibration lesson, proof result, or memo draft has been produced.

## 4. `jb` Client 0 Decision-Frame Lock

Lock status: complete for pre-evidence framing.

Decision question:

> Which finance-career avatar, pain wedge, copy angle, pricing/package, and
> workflow bet has the strongest public market pull?

Decision owner or decision context:

`jb` is Orca's first internal Client 0. The decision context is internal method
validation for choosing among finance-career avatars, pain wedges, copy angles,
pricing/packages, and workflow bets using public market signals.

Consequence of acting or not acting:

- Acting on weak or distorted evidence could push `jb` toward the wrong avatar,
  pain wedge, copy angle, pricing/package, or workflow bet.
- Not acting on valid public evidence could leave useful allocation signal
  unused and keep the decision dependent on internal preference or intuition.
- Overclaiming attention as demand would create false confidence.
- Underclaiming valid costly behavior would make the method less useful than
  Core Spine v0 is meant to be.

Allowed recommendation verbs constrained by Action Ceiling:

- `Watch`: monitor a visible but weak or uncertain signal.
- `Probe`: investigate a named uncertainty.
- `Test`: run a reversible test with kill criteria.
- `Hold`: delay, narrow, or withhold action because counterevidence, integrity
  risk, or source limitation is material.
- `Move`: make a bounded repositioning or allocation move only if evidence is
  strong enough and alternatives have been handled.
- `Commit`: allowed only if later evidence satisfies the full Core Spine
  preconditions for clean-enough integrity, independence, audience fit, costly
  behavior, counterevidence handling, and material consequence.

No `jb` recommendation may reach `Commit` from engagement alone.

Method-usefulness success criteria:

- The dry run can distinguish attention, resonance, objection, distribution,
  buyer belief, and demand claims.
- Evidence Units (EvidenceUnit) are inspectable enough for a skeptical reader to reconstruct
  the inference.
- Signal Integrity labels change discounting, uncertainty, exclusion, Decision
  Strength, or Action Ceiling.
- Signal Use Classification prevents copied language, incentive-driven
  engagement, social proof, and campaign success from being overclaimed as
  demand.
- The memo can compare the `jb` options without importing `jb` project rules
  as Orca authority.
- Recommendation language stays within the evidence-supported Action Ceiling.
- Update triggers and kill criteria remain visible.

Kill criteria:

- `jb` categories, lifecycle mechanics, paths, prompt templates, validation
  habits, or success logic become Core Spine authority.
- Internal Client 0 method validation is treated as external willingness to
  pay.
- Costly behavior cannot be distinguished from curiosity, anxiety, status
  signaling, copied advice, or incentive-driven engagement.
- Recommendation verbs exceed the evidence-supported Action Ceiling.
- Evidence cannot separate public market pull from campaign mechanics,
  affiliate incentives, copied language, or artificial amplification risk.
- Source blind spots make the conclusion non-inspectable.

Costly behavior standard for this `jb` context:

Costly behavior means a public signal that plausibly reflects real effort,
stakes, or switching pressure in the finance-career context. Examples include
payment, serious application or job-search effort, repeated portfolio or resume
work, time-intensive interview preparation, switching from another tool or
workflow, sustained workaround creation, or repeated complaints with stakes.

These examples are Client 0 context only. They do not become a universal Core
Spine standard.

Source blind spots and evidence limits:

- Platform incentives may distort visible attention.
- Career advice language is often copied, aspirational, or status-oriented.
- Creator, affiliate, school, employer, or community incentives may distort
  apparent pull.
- Public comments may show anxiety or curiosity without willingness to pay.
- Private conversion data, employer behavior, and actual career outcomes may
  be missing.
- Finance-career audiences may not generalize to other Orca satellites.

Boundary note:

`jb` project paths, lifecycle mechanics, templates, validation habits, and
success logic do not become Orca or Core Spine authority. `jb` can test method
usefulness; it cannot define Orca product authority or prove external
willingness to pay.

## 5. Competitor Narrative Response Shadow-Satellite Lock

Lock status: complete and reviewed for pre-evidence framing.

Exact buyer-visible narrative pressure decision:

Whether the Zendesk customer service product, positioning, or competitive
response context should monitor, defend, reposition, or test a response to
Intercom Fin's buyer-visible "AI agent for customer service" narrative.

Decision owner or decision context:

Zendesk customer service suite product, positioning, or competitive response
context.

Buyer-visible belief or consequence:

Support leaders may evaluate customer service platforms around AI-agent
resolution, support-volume reduction, trust, control, and AI-first customer
experience rather than helpdesk workflow alone.

Domain language:

B2B customer service, helpdesk, CX, support operations, AI support agents, and
AI-first customer experience.

Costly behavior standard:

For this shadow case, costly behavior means public, inspectable market or buyer
behavior that plausibly creates real response pressure for Zendesk. Examples
include public migration or evaluation statements, detailed buyer comparisons,
public trial or switching consideration, support workflow changes,
support-team staffing or budget implications, repeated buyer objections with
stakes, sales-cycle friction, or customer-facing pressure that persists beyond
a campaign burst.

Vendor claims alone, product-positioning repetition, AI resolution benchmarks,
customer logos, customer stories, or comparison pages do not satisfy the costly
behavior standard unless the later proof record also shows why they are
buyer-visible, timing-valid, and not merely self-promotional.

Allowed recommendation verbs:

`Watch`, `Probe`, `Test`, `Hold`, or `Move`.

Action-threshold limits:

- `Commit` is not allowed for this first-pass shadow satellite.
- `Watch` requires visible but weak or uncertain relevance.
- `Probe` requires a named uncertainty.
- `Test` requires reversible scope and kill criteria.
- `Hold` requires material counterevidence, integrity risk, or source
  limitation.
- `Move` requires bounded action, handled alternatives, and evidence strong
  enough for buyer-visible response pressure.

Source-family admissibility requirements and blind spots:

No exact source maps or source systems are introduced by this lock.

Later source families are admissible only if they are public, inspectable,
market-level, non-deceptively obtained, relevant to the locked decision frame,
and capable of supporting bounded inference about buyer belief, actor strategy,
distribution, narrative traction, objection pressure, or manipulation risk.

Blind spots that must remain visible include paid or coordinated campaigns,
affiliate incentives, copied language, analyst-only visibility, platform
sampling bias, weak audience fit, artificial-amplification risk, and ambiguity
between competitor intent and buyer pull.

Volatility controls:

- Product pages, pricing pages, comparison pages, and AI-agent claims may
  change quickly. Later evidence work must record event or publication timing
  and capture or access timing before interpretation.
- Current product-page language must not be used as evidence of earlier buyer
  belief, narrative traction, or response pressure unless timing supports that
  use.
- Vendor benchmark, resolution-rate, automation-rate, deflection-rate,
  support-volume, and productivity claims must be discounted unless the proof
  record explains actor incentive, source limitations, audience fit, and
  independent support.
- Benchmark or customer-story claims may inform actor strategy or buyer-visible
  narrative pressure, but they must not be overclaimed as independent buyer
  pull without additional support.
- No proof evidence collection or interpretation for this shadow satellite may
  begin until the owner explicitly authorizes proof-run start.

Actor or competitor behavior that matters:

Material behavior may include Intercom Fin launch and repeated AI-agent or
customer-service positioning, Zendesk AI positioning and platform response,
buyer-facing comparison pressure between AI-agent support and helpdesk-suite
approaches, public positioning shifts, campaign repetition, distribution
emphasis, customer-story repetition, or coordinated amplification that changes
the response ceiling.

Kill criteria:

- The satellite becomes broad competitor monitoring.
- The case lacks a buyer-visible belief or consequence.
- The case requires new Core Spine primitives.
- Finance-career assumptions leak into the satellite.
- Copied, campaign-driven, affiliate, or bot-like evidence is treated as
  independent buyer pull.
- Action thresholds or costly behavior require owner input that remains
  unavailable.
- Product-page volatility, vendor benchmarks, customer-story claims, or
  comparison pages are treated as stable independent buyer pull without timing
  control and discounting.
- Evidence collection or interpretation begins before explicit proof-run start
  authorization.

This is not broad competitor monitoring. It is one locked buyer-visible
narrative pressure decision. It does not authorize source maps, broad source
inventories, recurring monitoring, feature planning, implementation, or proof
execution before explicit proof-run start authorization.

No proof evidence has been interpreted for this shadow satellite before this
lock.

## 6. Backtest Pre-Registration Lock

Lock status: complete for pre-evidence framing.

Case-selection policy:

Use exactly one pre-registered, leakage-controlled historical case. The case
must be selected before evidence interpretation, and misses, overconfidence,
underconfidence, early calls, late calls, wrong calls, useful caution, and
inconclusive results must remain calibration input.

Case-selection owner or decision source:

Owner-selected in chat on 2026-05-21 from the committed Part 2 AI-era
heavyweight discovery candidate universe:
`docs/product/core_spine_v0_heavyweight_proof_case_discovery_results_part_2_v0.md`.

The selected candidate source is the second heavyweight discovery pass,
generative creative-tools and content-licensing lane. The selection followed
owner concern about familiarity bias toward Chegg and a preference for the more
honest calibration case.

Exact historical case:

`BT2-04`: Shutterstock response to generative image AI.

Decision context:

Stock-image marketplace, contributor economics, licensing, customer creative
workflows, and partnership response to text-to-image AI after Stable Diffusion
and other generative-image tools made synthetic image supply publicly visible.

Why the case is relevant to Core Spine v0:

The case tests whether public pre-cutoff signals could have supported a useful
decision memo before Shutterstock's later partnership, licensing, and product
response outcomes were public. It stresses public market pull, actor strategy,
platform economics, creator/contributor conflict, licensing pressure, and AI
hype control without requiring private data or runtime systems.

It must use the same Core Spine primitives used by the `jb` and shadow
satellite dry runs: Decision Frame, Evidence Unit, Signal Integrity, Signal Use
Classification, Decision Strength, Action Ceiling, Decision Memo, Backtesting
and Outcome Memory, and Boundary Rules.

Why the case was not selected merely because the later outcome is persuasive:

The case was selected from a predeclared AI-era backtest refresh after the
owner rejected the more famous Chegg/ChatGPT case as too familiarity-biased.
Shutterstock has a meaningful but less iconic post-window outcome than Chegg's
stock reaction, and it tests marketplace supply disruption plus licensing and
partnership response rather than a direct AI-substitution story.

The replay must still preserve wrong, overconfident, underconfident, blocked,
early, late, useful, and inconclusive outcomes. It must not treat the later
OpenAI partnership, AI Image Generator launch, expanded data agreement, or
copyright narrative as evidence that the pre-cutoff judgment should have been
obvious.

Cutoff date:

2022-09-15.

Why the cutoff is fair and before the outcome was obvious:

This date is the later edge of the Part 2 proposed cutoff window
`2022-08-23 to 2022-09-15`. It falls after Stable Diffusion's public release
made text-to-image disruption visible, but before Shutterstock announced its
expanded OpenAI partnership on 2022-10-25.

At the cutoff, stock-image platforms could plausibly have responded by banning
AI images, litigating, licensing training data, partnering with AI labs,
creating their own tools, changing contributor economics, or waiting for
copyright clarity. The later Shutterstock partnership, contributor-fund
posture, AI Image Generator, expanded data agreement, and Getty comparison
context were not yet part of the at-cutoff record.

Pre-cutoff source visibility requirement:

Only public evidence published, visible, or reasonably discoverable on or
before 2022-09-15 may inform the at-cutoff judgment. Any evidence without
usable timing for the cutoff-sensitive claim is blocked or excluded.

Admissible pre-cutoff visibility may include public product pages, public
platform statements, official launch or release notes, public market-level
coverage, and public company materials visible by the cutoff. It may not use
post-window material to infer what was knowable at cutoff.

Post-window exclusion rule:

Exclude Shutterstock's 2022-10-25 OpenAI partnership announcement, AI Image
Generator launch, expanded OpenAI data agreement, later Getty litigation or
product moves, later copyright and artist-compensation narratives, and
post-window retrospective coverage from the at-cutoff recommendation, Decision
Strength, Action Ceiling, and backtest judgment.

Post-window material may be used only after the at-cutoff record is complete
to compare later outcome and record calibration.

Allowed result states:

- `pass`;
- `fail`;
- `blocked`;
- `inconclusive`;
- `early`;
- `late`;
- `wrong`;
- `useful`;
- `overconfident`;
- `underconfident`.

Calibration lesson field:

Required but not fillable before the backtest is run. The field must record
what the evidence standard should learn, including misses and inconclusive
results. It must not convert a cherry-picked win into internal calibration
unless leakage controls passed.

No proof evidence has been interpreted before this backtest lock.

## 7. Evidence-Start Permission Gate

Evidence collection can begin only if all locks are complete, the updated lock
record has been reviewed, and the owner explicitly authorizes proof-run start.

| Gate | State |
| --- | --- |
| `jb` decision-frame lock complete | Pass |
| Shadow-satellite lock complete | Pass |
| Backtest pre-registration lock complete | Pass |
| No-evidence-interpreted declaration recorded | Pass |
| Source boundaries preserved | Pass |
| No exact source maps or source systems introduced | Pass |
| Updated lock record reviewed after `SH-01` patch | Pass |
| Explicit proof-run start authorization recorded | Blocked |

Evidence collection and interpretation may not begin under the charter because
explicit proof-run start authorization has not yet been recorded.

## 8. Stop Criteria

Stop before evidence collection or interpretation if any of these are true:

- an exact buyer-visible narrative pressure decision is not supplied for the
  shadow satellite;
- the shadow satellite becomes broad competitor monitoring;
- the shadow satellite lacks buyer-visible belief or consequence, domain
  context, costly behavior standard, action-threshold limits, or actor behavior
  that matters;
- a case-selection owner or decision source is missing for the backtest;
- the exact historical backtest case is missing;
- the cutoff date is missing or cannot be shown to be fair and before the
  outcome was obvious;
- anti-cherry-pick rationale is missing;
- pre-cutoff source visibility cannot be established;
- post-window evidence cannot be excluded from the at-cutoff judgment;
- any proof evidence has already been interpreted before a lock is complete;
- evidence collection or interpretation begins before explicit proof-run start
  authorization is recorded;
- fast-changing product pages, vendor benchmark claims, or customer-story
  claims are used without timing control, discounting, and source-limitation
  notes;
- the work requires source URLs, exact source maps, source systems, broad
  source inventories, broad competitor monitoring, scrapers, APIs, databases,
  dashboards, scoring engines, automation runtimes, software tests, feature
  plans, implementation plans, tooling plans, or generated artifacts;
- `jb` authority leaks into Orca or Core Spine authority;
- recommendation verbs exceed the evidence-supported Action Ceiling.

Blocked is not proof failure. It means the proof cannot be judged within the
authorized inputs and boundaries.

## 9. Explicit Non-Claims

This record does not claim:

- proof success;
- proof readiness beyond the blocked evidence-start gate;
- Core Spine v0 works;
- the selected shadow case proves evidence availability, proof readiness, or
  narrative strength;
- the selected backtest case or cutoff proves evidence availability, proof
  readiness, or backtest success;
- any evidence exists or will be strong;
- any decision memo has been drafted;
- any backtest has been executed;
- any proof result, outcome report, or review packet exists;
- external buyers will pay;
- market size is known;
- `jb` evidence generalizes commercially;
- any recommendation should reach `Commit`;
- feature planning is ready;
- implementation planning is ready;
- implementation is authorized;
- source collection systems, dashboards, databases, scoring engines, APIs,
  scrapers, automation runtimes, or software tests should be built.

## 10. Current Verdict

Current verdict: `LOCKS_REVIEWED_AWAITING_PROOF_RUN_AUTHORIZATION`.

The `jb` Client 0 decision-frame lock is complete, the `SH-01` shadow-satellite
lock is complete for pre-evidence framing, the `BT2-04` backtest
pre-registration lock is complete, the no-evidence declaration is recorded, and
the updated lock record has been reviewed after the `SH-01` patch. Evidence
collection and interpretation may not begin until the owner explicitly
authorizes proof-run start.
