# Core Spine v0 First Proof Run Charter

- Status: READY_FOR_OWNER_ACCEPTANCE
- Artifact type: Product proof-run charter
- Scope: First manual docs-first proof run for Core Spine v0
- Date context: 2026-05-21, Asia/Singapore
- Source basis: current owner instruction on 2026-05-21, `AGENTS.md`,
  `.agents/workflow-overlay/README.md`,
  `.agents/workflow-overlay/project-authority.md`,
  `.agents/workflow-overlay/source-of-truth.md`,
  `.agents/workflow-overlay/artifact-roles.md`,
  `.agents/workflow-overlay/validation-gates.md`,
  `.agents/workflow-overlay/safety-rules.md`,
  `.agents/workflow-overlay/communication-style.md`,
  `docs/decisions/turn_08_product_thesis_v0.md`,
  `docs/product/core_spine_v0_product_contract.md`,
  `orca/product/shared/engagement_registry/engagement_logic_registry_v0.md`,
  `docs/product/core_spine_v0_information_production_foundation_v0.md`,
  `docs/product/core_spine_v0_proof_protocol_v0.md`,
  `docs/product/core_spine_v0_proof_input_selection_v0.md`,
  `docs/product/core_spine_v0_proof_packet_preflight_v0.md`,
  `docs/product/core_spine_v0_first_proof_packet_preparation_v0.md`
- Repository check: `git status --short --branch` reported
  `## main...origin/main [ahead 3]`; recent log includes
  `c724852 docs: add core spine proof-prep milestone`
- Implementation authorized: no
- Feature planning authorized: no
- Source collection systems authorized: no
- Charter activation: requires explicit owner acceptance

## Purpose

This charter is the permission slip for the first Core Spine v0 proof run.

After explicit owner acceptance, it authorizes only one bounded manual
docs-first proof run. It does not contain the proof itself, collected evidence,
decision memo outputs, source maps, feature plans, implementation plans,
tooling plans, or proof results.

This charter resolves the prior proof-execution blocker only for the bounded
work listed here. All broader Orca boundaries remain in force.

## Proof-Run Scope

The authorized proof run tests whether the same eight Core Spine primitives can
turn noisy public evidence into inspectable allocation recommendations across:

1. `jb` Client 0;
2. one competitor narrative response shadow satellite; and
3. one leakage-controlled historical backtest replay.

The run must stay manual, public, market-level, docs-first, and non-runtime.
It must use the Core Spine v0 primitives from the product contract and the
manual production sequence from the information-production foundation:

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

The proof run may evaluate method usefulness and portability. It may not claim
external willingness to pay, market size, implementation readiness, feature
planning readiness, or generalized OSINT platform readiness.

## Authorized Work

After owner acceptance, this charter authorizes only:

- manual public evidence collection for this proof run only;
- Evidence Unit creation;
- Signal Integrity assessment;
- Signal Use Classification;
- Decision Strength and Action Ceiling assessment;
- one `jb` Client 0 decision memo dry run;
- one competitor narrative response shadow-satellite memo dry run;
- one leakage-controlled historical backtest replay;
- one proof outcome report or proof review packet.

No repeat run, expanded case set, additional satellite, automated collection,
runtime design, or implementation step is authorized by this charter.

## Allowed Outputs

The proof run may produce only docs-first proof-run outputs needed to judge the
bounded run:

- Evidence Units for the selected `jb`, shadow-satellite, and backtest contexts;
- Signal Integrity notes with effect statements;
- Signal Use Classification notes;
- Decision Strength and Action Ceiling assessments;
- one `jb` Client 0 decision memo dry run;
- one competitor narrative response shadow-satellite memo dry run;
- one historical backtest replay record;
- one proof outcome report or proof review packet.

Each output must preserve uncertainty, counterevidence, source limitations,
alternative explanations, update triggers, kill criteria, and Action Ceiling
limits. The outcome report or review packet must distinguish proof result,
backtest calibration result, and any residual blockers.

## Pre-Evidence Locks

The proof runner must complete these locks before collecting or interpreting
proof evidence. If either lock is missing or ambiguous, the proof run is
blocked.

### Shadow Satellite Lock

Before evidence work begins for the competitor narrative response memo dry
run, the runner must record:

- one exact buyer-visible narrative pressure decision;
- decision owner or decision context;
- buyer-visible belief or consequence;
- costly behavior standard;
- allowed recommendation verbs and action-threshold limits;
- source-family admissibility requirements and blind spots, without creating
  exact source maps;
- statement that no proof evidence has been interpreted for this shadow
  satellite before the lock.

This lock keeps the satellite to one decision case. It does not authorize broad
competitor monitoring, source-map creation, or case-hunting after evidence is
seen.

### Backtest Pre-Registration Lock

Before evidence work begins for the historical backtest replay, the runner
must complete the full backtest pre-registration record in this charter,
including case-selection owner or decision source, anti-cherry-pick rationale,
pre-cutoff source visibility requirement, allowed result states, calibration
lesson field, and a statement that no proof evidence has been interpreted
before the lock.

The numbered Backtest Lock Sequence below is the required order of operations.
The backtest is not locked unless the full pre-registration record is also
complete before interpretation.

## Evidence Admissibility Rules

Evidence is admissible only when it is:

- public, market-level, inspectable, and non-deceptively obtained;
- tied to a stated Decision Frame;
- relevant to one of the authorized proof contexts;
- recorded with a source locator, citation, archive reference, or source-family
  basis sufficient for skeptical review;
- recorded with source actor or audience type when knowable;
- recorded with event or publication timestamp when available;
- recorded with capture or access timestamp;
- recorded with source visibility and pre-cutoff visibility for backtest work;
- separated into raw claim, observed pattern, and Orca interpretation;
- recorded with provenance and transformation history;
- recorded with source limitations and known blind spots;
- classified by Signal Use before it affects Decision Strength.

Evidence is inadmissible when any of these are true:

- it is private, intrusive, deceptive, ordinary-person dossier material, or
  outside Orca's public market-level boundary;
- it lacks an inspectable source or source-family basis;
- it cannot be tied to a Decision Frame;
- timing is missing for cutoff-sensitive work;
- post-window evidence is mislabeled as pre-window evidence;
- demand is inferred from engagement without audience fit, independence,
  costly behavior, detailed stakes, or other valid support;
- copied, incentivized, bot-like, campaign-driven, or source-limited material
  is counted as independent pull without discounting;
- `jb` assumptions, paths, lifecycle mechanics, templates, validation habits,
  or success logic are imported as Orca authority.

Weak evidence may still support attention, distribution, actor strategy,
buyer-belief, manipulation-risk, monitoring, or investigation claims. It must
not be overclaimed as demand or commitment support.

## Backtest Pre-Registration Requirements

The proof run includes exactly one leakage-controlled historical backtest
replay.

Before interpreting evidence, the run must record:

- case-selection policy;
- case-selection owner or decision source;
- exact historical case, once selected under the policy;
- decision context;
- why the case is relevant to Core Spine v0;
- why the case was not selected merely because the later outcome is
  persuasive;
- cutoff date;
- why the cutoff is fair and before the outcome was obvious;
- pre-cutoff source visibility requirement;
- post-window exclusion rule;
- allowed result states;
- calibration lesson field.

Misses, overconfidence, underconfidence, early calls, late calls, wrong calls,
useful caution, and inconclusive results must remain calibration input.
Cherry-picked marketing demos do not train the internal evidence standard
unless they pass these leakage controls.

## Backtest Lock Sequence

The backtest is locked only if the full pre-registration record is complete and
this sequence is completed before interpreting evidence:

1. Select or record the case-selection policy.
2. Record the case-selection owner or decision source.
3. Select the exact historical case.
4. Record why the case is relevant to Core Spine v0 and was not selected
   merely because the later outcome is persuasive.
5. Freeze the cutoff date.
6. State why the cutoff is fair and before the outcome was obvious.
7. Define the pre-cutoff source visibility requirement.
8. Define the post-window exclusion rule.
9. Record allowed result states and the calibration lesson field.
10. Record that no proof evidence has been interpreted before this lock.
11. Only then begin evidence interpretation.

If this sequence cannot be followed, the proof run is blocked. No at-cutoff
recommendation, backtest result, calibration lesson, or proof claim may be
produced from an unlocked backtest.

## Stop Criteria

The proof run must stop or return to owner review if any of these occur:

- owner acceptance of this charter is missing or ambiguous;
- the shadow satellite lock is missing, ambiguous, or created after evidence
  collection or interpretation begins;
- the competitor narrative response case lacks one exact buyer-visible
  narrative pressure decision, decision owner or context, buyer-visible
  consequence, costly behavior standard, action-threshold limits, or
  source-family admissibility and blind-spot notes;
- the backtest pre-registration lock is incomplete before evidence collection
  or interpretation begins;
- the backtest lock sequence cannot be followed in order;
- the exact historical case is selected after evidence interpretation;
- the case-selection owner or decision source is not recorded;
- the anti-cherry-pick rationale, pre-cutoff source visibility requirement,
  allowed result states, or calibration lesson field is missing;
- the cutoff date cannot be shown to be fair and before the outcome was
  obvious;
- post-window evidence cannot be separated from pre-cutoff evidence;
- required evidence is unavailable, non-inspectable, private, intrusive,
  deceptive, or outside the public market-level boundary;
- source access requires scrapers, APIs, automation, private access, or
  runtime systems;
- the run needs exact source maps, source collection architecture, tooling
  plans, feature plans, implementation plans, software tests, or stack choices;
- `jb` project-specific authority leaks into Core Spine or into the shadow
  satellite;
- the competitor narrative response satellite becomes broad competitor
  monitoring instead of one buyer-visible narrative pressure decision;
- the shadow satellite requires new Core Spine primitives;
- Signal Integrity labels become decorative and do not affect discounting,
  uncertainty, exclusion, Decision Strength, or Action Ceiling;
- Signal Use Classification allows attention, campaign success, copied
  language, or social proof to be overclaimed as demand;
- recommendation verbs exceed the Action Ceiling;
- satellite-specific costly behavior or action-threshold owner input is
  required and unavailable;
- the run attempts to expand beyond the single authorized `jb` memo, single
  shadow memo, single backtest replay, or single outcome report or review
  packet.

Blocked is not a proof failure. It means the proof cannot be judged within the
authorized inputs and boundaries.

## Owner Acceptance Requirement

The proof run may begin only after the owner explicitly accepts this charter.

Owner acceptance activates only this charter's bounded authority:

- one manual docs-first proof run;
- the authorized work listed above;
- the allowed outputs listed above;
- the pre-evidence locks;
- the evidence admissibility rules;
- the backtest lock sequence;
- the stop criteria and non-claims.

If the owner changes the proof question, adds a satellite, changes the
backtest policy, requests automation, or asks for feature or implementation
work, this charter must be revised or superseded before that work begins.

After the proof run, the owner must review or accept the proof outcome report
or proof review packet before any feature planning, implementation planning,
runtime design, tooling work, broader proof suite, or marketing-demo packaging
can be treated as authorized.

## Proof Result States

The proof outcome report or proof review packet must use these states:

| State | Meaning |
| --- | --- |
| Pass | The `jb` memo, shadow-satellite memo, and backtest replay all use the same Core Spine primitives; material claims are inspectable; Signal Integrity changes inference; Signal Use prevents demand overclaiming; Action Ceilings are respected; and leakage controls hold. |
| Fail | The proof breaks Core Spine boundaries, requires new primitives, imports `jb` authority, overclaims engagement as demand, uses decorative integrity labels, produces non-inspectable claims, violates backtest leakage controls, or recommends action above the evidence-supported ceiling. |
| Blocked | Required authority, source access, inspectable evidence, timing, pre-cutoff visibility, owner input, decision-frame clarity, or backtest lock discipline is missing. |
| Inconclusive | The run is valid and bounded, but evidence is too thin, source-limited, counterevidence-heavy, or integrity-limited to support a stronger recommendation. |

The backtest replay must also record calibration tags where applicable:
`early`, `late`, `wrong`, `useful`, `overconfident`, `underconfident`, and
`inconclusive`.

Inconclusive and blocked outcomes may be useful learning outcomes. They do not
authorize feature planning, implementation, or a stronger proof claim.

## Explicit Non-Claims

This charter does not claim:

- Core Spine v0 works;
- the first proof run will pass;
- any evidence has been collected;
- any decision memo has been produced;
- any historical case has been selected or locked;
- external buyers will pay;
- market size is known;
- `jb` evidence generalizes commercially;
- competitor narrative response evidence exists or will be strong;
- the backtest will be favorable;
- any recommendation should reach `Commit`;
- marketing-demo material has been created;
- a source collection system should be built;
- a dashboard, database, scoring engine, scraper, API, automation runtime,
  clustering pipeline, or software test should be built;
- feature planning is ready;
- implementation planning is ready;
- implementation is authorized;
- workflow-kernel source edits, skill installation, skill promotion, skill
  renaming, or skill shadowing are authorized;
- any future proof run, expanded backtest suite, source map, case library, or
  tooling plan is authorized.

## Forbidden Work

This charter does not authorize:

- scrapers;
- APIs;
- databases;
- dashboards;
- scoring engines;
- automation runtimes;
- clustering pipelines;
- software tests;
- implementation folders;
- stack choices;
- exact source maps or broad source-family inventories;
- feature plans;
- implementation plans;
- tooling plans;
- generalized OSINT platform work;
- private, intrusive, deceptive, or person-level dossier work;
- workflow-kernel source edits;
- skill installation, promotion, renaming, rewriting, or shadowing;
- commits, pushes, pull requests, destructive cleanup, or repository
  reconfiguration.

Ideas from runtime or tooling systems may inform later product requirements
only if separately authorized. They may not be built or planned in this proof
run.

## Current Verdict

Current verdict: `READY_FOR_OWNER_ACCEPTANCE`.

The next valid action is owner acceptance of this charter, targeted revision to
this charter, or explicit refusal to run the proof. Proof execution remains
inactive until owner acceptance occurs.
