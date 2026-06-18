# Core Spine v0 Proof Packet Preflight

- Status: PROPOSED_FREEZE
- Artifact type: Product proof-preflight artifact
- Scope: Docs-first readiness gate for preparing the first Core Spine v0 proof
  packet
- Source basis: current owner direction, accepted chat-only product-ultraplan
  result from 2026-05-20, `docs/decisions/turn_08_product_thesis_v0.md`,
  `docs/product/core_spine_v0_product_contract.md`,
  `orca/product/shared/engagement_registry/engagement_logic_registry_v0.md`,
  `docs/product/core_spine_v0_information_production_foundation_v0.md`,
  `docs/product/core_spine_v0_proof_protocol_v0.md`,
  `docs/product/core_spine_v0_proof_input_selection_v0.md`
- Implementation authorized: no
- Feature planning authorized: no
- Proof run authorized: no
- Source collection authorized: no

## Purpose

This preflight determines whether Core Spine v0 has enough accepted, coherent
inputs to prepare the first proof packet without yet running the proof.

It is the decision gate between product-foundation theory and proof-packet
preparation. It should make missing inputs visible before Orca spends effort on
memo drafting, evidence gathering, source mapping, or proof execution.

The preflight answers:

- whether the Information Production Foundation is accepted or conditionally
  accepted for proof-prep use;
- whether stale product verdicts have been reconciled;
- whether the first proof packet shape is clear enough to prepare;
- whether the `jb` Client 0 decision frame is bounded without becoming Orca
  authority;
- whether the competitor narrative response shadow satellite is narrow enough
  to stress non-`jb` portability without becoming broad competitor monitoring;
- whether the backtest case-selection policy blocks hindsight and cherry-pick
  leakage;
- what blocks proof execution.

## Non-Authority

This artifact does not authorize:

- proof execution;
- proof-packet evidence collection;
- exact source maps or source-family inventories;
- Client 0 or shadow-satellite memo drafting;
- historical backtest execution;
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
- feature planning;
- implementation planning;
- workflow-kernel source edits;
- skill installation, promotion, renaming, or shadowing.

This artifact may only define the conditions for later preparation of a
docs-first proof packet. Preparation still requires the readiness gates to pass
and the owner to explicitly accept that next step.

## Status And Verdict Reconciliation

The current Core Spine v0 stack contains several earlier verdicts that were
accurate when written but now need a single preflight interpretation.

| Artifact | Existing status or verdict | Preflight interpretation |
| --- | --- | --- |
| `docs/product/core_spine_v0_product_contract.md` | `NEEDS_PRODUCT_ARTIFACT` | Satisfied for preflight input by the Core Spine contract, proof protocol, proof input selection, information-production foundation, and this preflight artifact. It does not imply proof-run readiness. |
| `docs/product/core_spine_v0_proof_protocol_v0.md` | `NEEDS_PRODUCT_ARTIFACT` | Satisfied for proof-preflight input by the protocol plus selected proof inputs. The protocol still requires accepted proof-prep gates before execution. |
| `docs/product/core_spine_v0_proof_input_selection_v0.md` | `NEEDS_FOUNDATION_ARTIFACT` | Stale if the Information Production Foundation is accepted for proof-prep use. The selected input set remains a target, not proof-run readiness. |
| `docs/product/core_spine_v0_information_production_foundation_v0.md` | `NEEDS_FOUNDATION_ACCEPTANCE` | Active blocker resolved only by this preflight's foundation acceptance rule. |

For proof-packet preparation, the controlling status is:

> `NEEDS_PROOF_PREFLIGHT_ACCEPTANCE`

This means the artifact stack is coherent enough to inspect for proof-packet
preparation, but no proof should run until the preflight gates pass and the
owner explicitly authorizes proof execution.

## Foundation Acceptance For Proof-Prep

If this preflight is owner-accepted, the Information Production Foundation is
conditionally accepted as the manual proof-prep standard for the first Core
Spine v0 proof packet.

The proposed conditional acceptance covers:

- Decision Frame requirements;
- Evidence Unit admissibility and state rules;
- Signal Integrity labels and required effect statements;
- Signal Use Classification;
- Demand Rule;
- Decision Strength;
- qualitative Action Ceiling;
- memo production rules;
- backtest production rules;
- invalid, blocked, and inconclusive states;
- docs-first boundary rules and bloat cuts.

This proposed acceptance is limited to proof-packet preparation. It does not
prove that Orca can produce decision-grade memos, that evidence is available,
that the shadow satellite will pass, or that proof execution is authorized.

The foundation is too thin for proof-prep if any of these become true:

- a proof packet cannot name a valid Decision Frame before evidence work;
- Evidence Units cannot be made inspectable enough for skeptical review;
- Signal Integrity labels can remain decorative without changing Decision
  Strength, Action Ceiling, uncertainty, discounting, or exclusion;
- engagement can still be overclaimed as demand without audience fit,
  independence, costly behavior, and counterevidence;
- backtest preparation cannot freeze case-selection policy, cutoff date, and
  post-window exclusions before interpretation;
- owner input is needed for a satellite-specific action threshold or costly
  behavior standard and is not available.

Additional foundation expansion is overengineering if it adds source
inventories, broad OSINT playbooks, numeric formulas, platform tactics,
operator manuals, implementation units, or tooling concepts before the first
proof packet tests the current manual standard.

## First Proof Packet Shape

The first proof packet should contain only the minimum docs-first components
needed to prepare the proof defined by
`docs/product/core_spine_v0_proof_protocol_v0.md`.

Required packet components:

1. Core Spine v0 proof question.
2. Shared evidence and inference standard based on the eight Core Spine
   primitives.
3. Client 0 `jb` decision-frame brief.
4. Competitor narrative response shadow-satellite decision-frame brief.
5. One backtest case-selection and pre-registration note.
6. Proof packet boundary note.
7. Preparation readiness checklist.
8. Proof execution blocker list.

The first proof packet must not contain:

- full decision memos;
- collected evidence;
- source maps;
- proof results;
- marketing demos;
- case library packaging;
- implementation or feature-planning work units.

## `jb` Client 0 Decision-Frame Requirements

The Client 0 `jb` frame tests method usefulness for an internal decision. It
does not validate external willingness to pay and does not make `jb` project
rules Orca authority.

The `jb` decision-frame brief must include:

- allocation question:

  > Which finance-career avatar, pain wedge, copy angle, pricing/package, and
  > workflow bet has the strongest public market pull?

- decision owner or decision context;
- consequence of acting or not acting;
- allowed recommendation verbs constrained by Action Ceiling;
- success criteria for method usefulness;
- kill criteria;
- what counts as costly behavior in the `jb` decision context;
- source blind spots and evidence limitations;
- boundary note stating that `jb` categories, lifecycle mechanics, paths,
  templates, validation habits, and success logic do not become Core Spine
  authority.

The `jb` frame is blocked if it imports `jb` project-specific authority, if it
cannot state what method usefulness means, or if it treats internal Client 0
evidence as external commercial validation.

## Competitor Narrative Response Shadow-Satellite Requirements

The primary non-`jb` shadow satellite remains competitor narrative response.

It must be framed narrowly as one buyer-visible narrative pressure case, not
broad competitor monitoring.

Decision question:

> Should the decision owner monitor, defend, reposition, or test a response to
> a competitor narrative that appears to be gaining market traction?

The shadow-satellite decision-frame brief must include:

- one decision type;
- buyer, user, decision owner, and consequence;
- domain language;
- source-family admissibility requirements and source blind spots, without
  selecting exact source maps;
- decision-specific relevance rules;
- costly behavior definition;
- allowed recommendation verbs: `Watch`, `Probe`, `Test`, `Hold`, or `Move`;
- why `Commit` is not expected from first-pass engagement evidence alone;
- success criteria;
- kill criteria;
- actor or competitor behavior that matters;
- buyer-visible belief or consequence requirement;
- boundary note stating that the satellite cannot add new Core Spine
  primitives or import finance-career assumptions.

This satellite is blocked if it becomes a broad competitor-monitoring program,
requires new Core Spine primitives, cannot show buyer-visible consequence, or
cannot define costly behavior and action thresholds without owner input.

Use the backup satellite, buyer-objection remediation, only if competitor
narrative response cannot produce a narrow buyer-visible decision case with
clean pre-cutoff visibility.

## Backtest Case-Selection Policy Requirements

Preflight should bind the case-selection policy before proof preparation.
It should not select evidence opportunistically.

The first proof packet requires one pre-registered, leakage-controlled
historical case.

The case-selection note must record:

- selection policy before evidence interpretation;
- case-selection owner or decision source;
- decision context;
- why the case is relevant to Core Spine v0;
- why the case is not selected merely because the later outcome is persuasive;
- cutoff date;
- why the cutoff is fair and before the outcome was obvious;
- pre-cutoff source visibility requirement;
- post-window evidence exclusion rule;
- allowed result states: pass, fail, blocked, inconclusive, overconfident,
  underconfident, early, late, wrong, useful;
- rule that misses and inconclusive results remain calibration input;
- rule that cherry-picked marketing demos do not train the internal evidence
  standard unless they pass leakage controls.

Preflight may choose only the policy and pre-registration fields. It should not
choose the exact historical case unless the owner supplies the case before
evidence interpretation and the packet records that no proof evidence has been
inspected.

## Proof-Packet Preparation Readiness Gates

Proof-packet preparation may begin only if all gates pass.

| Gate | Pass condition | Blocked condition |
| --- | --- | --- |
| Artifact stack gate | Product contract, engagement registry, proof protocol, proof input selection, information-production foundation, and preflight are all available as source inputs. | Any required artifact is missing, conflicting, or not allowed as proof-prep input. |
| Preflight acceptance gate | Owner accepts this preflight or accepts a targeted revision to its gates. | This preflight remains only a proposed artifact. |
| Foundation acceptance gate | Information Production Foundation is accepted or conditionally accepted as the manual proof-prep standard. | Foundation acceptance remains unresolved. |
| Verdict reconciliation gate | Earlier `NEEDS_PRODUCT_ARTIFACT`, `NEEDS_FOUNDATION_ARTIFACT`, and `NEEDS_FOUNDATION_ACCEPTANCE` states have a single controlling interpretation. | Active verdict remains ambiguous. |
| Client 0 gate | `jb` decision-frame requirements are complete and bounded. | `jb` authority leaks into Core Spine or external validation is overclaimed. |
| Shadow satellite gate | Competitor narrative response is narrowed to one buyer-visible narrative pressure decision. | Satellite becomes broad monitoring or lacks buyer-visible consequence. |
| Backtest gate | One leakage-controlled case-selection policy is pre-registered before interpretation. | Case is selected after outcome knowledge or cutoff discipline is unclear. |
| Boundary gate | Packet excludes proof execution, evidence collection, source maps, memos, tooling, and feature planning. | Packet requires source collection, runtime design, memo execution, or implementation planning. |
| Result-state gate | Pass, fail, blocked, and inconclusive states are explicit. | Missing evidence can be treated as a pass. |

Passing these gates means Orca may prepare the first docs-first proof packet
when separately authorized. It does not mean Orca may run the proof.

## Proof Execution Blockers

Proof execution remains blocked if any of these are true:

- proof execution is not explicitly authorized by the owner;
- a valid `jb` decision frame is missing;
- the shadow satellite is not selected or narrowed to one decision case;
- the backtest case-selection policy is not pre-registered;
- the exact historical case is selected after evidence interpretation;
- cutoff date or pre-cutoff visibility cannot be established;
- required evidence is unavailable, private, deceptive, intrusive, or not
  inspectable;
- post-window evidence cannot be excluded;
- Signal Integrity can appear without an effect statement;
- Signal Use Classification allows attention, campaign success, copied
  language, or social proof to be overclaimed as demand;
- action thresholds or satellite-specific costly behavior require owner input
  that has not been supplied;
- the proof packet requires source collection architecture, scraper design,
  API design, database design, dashboards, scoring engines, tests, runtime
  systems, feature planning, or implementation planning;
- the proof cannot separate "Orca helped choose among allocation options" from
  "Orca proved the market is real."

Blocked is not a failure of Core Spine v0. It means proof execution cannot be
judged from the current inputs.

## Explicit Non-Claims

This preflight does not prove:

- Core Spine v0 works;
- Orca is proof-run ready;
- Orca is feature-planning ready;
- Orca is implementation ready;
- external buyers will pay;
- `jb` evidence generalizes commercially;
- competitor narrative response evidence exists or will be strong;
- the backtest will pass;
- a source collection system should be built;
- a dashboard, database, scoring engine, or automation runtime should be built;
- any recommendation should reach `Commit`;
- any current artifact is owner-accepted beyond the proposed conditional
  proof-prep acceptance stated here.

## Bloat Cuts

Cut from preflight:

- source inventories;
- broad OSINT playbooks;
- exact platform tactics;
- exact source maps;
- scraper, API, database, dashboard, scoring, test, or runtime concepts;
- numeric formulas;
- operator manuals;
- full decision memo drafts;
- proof outputs;
- case-library packaging;
- marketing copy;
- implementation units;
- feature-planning labels.

Keep in preflight:

- status and verdict reconciliation;
- conditional foundation acceptance;
- first proof packet shape;
- `jb` Client 0 decision-frame requirements;
- competitor narrative response decision-frame requirements;
- backtest case-selection policy requirements;
- readiness gates;
- execution blockers;
- explicit non-claims.

## Current Verdict

Current verdict: `NEEDS_PROOF_PREFLIGHT_ACCEPTANCE`.

Core Spine v0 now has a proposed proof-preflight artifact and a proposed
conditional acceptance of the manual foundation for proof-packet preparation.
The next valid step is owner acceptance of this preflight, or a targeted
revision to the preflight gates. Proof execution, feature planning, and
implementation remain unauthorized.
