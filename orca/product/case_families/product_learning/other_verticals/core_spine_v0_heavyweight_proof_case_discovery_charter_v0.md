# Core Spine v0 Heavyweight Proof Case Discovery Charter

- Status: READY_FOR_OWNER_ACCEPTANCE_OF_DISCOVERY_SCOPE
- Artifact type: Product discovery-scope charter
- Scope: Bounded heavyweight discovery phase for first proof-run case candidates
- Date context: 2026-05-21, Asia/Singapore
- Output mode: file-write
- Edit permission used: docs-write for this target artifact only
- Implementation authorized: no
- Feature planning authorized: no
- Proof execution authorized: no
- Evidence collection authorized: no
- Heavyweight discovery authorized by this artifact: no
- Charter activation: requires explicit owner acceptance

## 1. Status, Scope, Source Basis, And Non-Authority

This charter defines the proposed scope for one bounded heavyweight discovery
phase. The phase is intended to create a candidate universe for first proof-run
case selection, not to run the proof.

Heavyweight discovery is allowed only after explicit owner acceptance of this
charter. Until that acceptance exists, this artifact is only a proposed
discovery boundary.

Source basis:

- current owner instruction on 2026-05-21;
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
- `docs/product/core_spine_v0_first_proof_run_locks_v0.md`;
- `docs/product/core_spine_v0_proof_case_selection_brief_v0.md`;
- repository check: `git status --short --branch` reported
  `## main...origin/main [ahead 4]`;
- recent log check: `git log --oneline -5` included
  `dbfbfda docs: add first proof run charter` and
  `c724852 docs: add core spine proof-prep milestone`.

Non-authority:

- This charter does not authorize discovery until owner acceptance.
- This charter does not select cases.
- This charter does not collect or interpret proof evidence.
- This charter does not patch the first proof-run lock record.
- This charter does not run the proof, draft memos, execute a backtest, create
  Evidence Units, create source maps, create source inventories, create
  monitoring, build a data spine, plan features, or authorize implementation.
- This charter does not import `jb` paths, lifecycle mechanics, validation
  habits, finance-career assumptions, or success logic into Orca authority.

## 2. Problem Frame

The first Core Spine v0 proof-run charter has been accepted in chat and
committed, but proof execution remains blocked because the pre-evidence locks
are incomplete.

The lock record is blocked because it lacks:

- one exact buyer-visible competitor narrative pressure decision for the
  shadow satellite;
- one exact historical backtest case (Case);
- a case-selection owner or decision source;
- a cutoff date or cutoff window;
- case-specific anti-cherry-pick and post-window exclusion rationale.

The proof case selection brief returned
`BLOCKED_OWNER_CANDIDATES_NEEDED`. It could not select cases because the owner
had not supplied candidates and Orca does not yet have a data or case memory.

The immediate problem is not lack of proof effort. The immediate problem is
lack of a pre-evidence candidate universe from which the owner can select cases
without cherry-pick leakage.

## 3. Why Heavyweight Discovery Is Needed Now

Lightweight selection has already reached its limit. The current source stack
defines the valid shape of cases, but it does not name real candidate cases.
Asking the owner to supply exact cases remains valid, but it blocks if the
owner does not already have a case memory.

A bounded heavyweight discovery phase is now justified because it can create a
small real candidate universe while still stopping before proof execution. Its
job is to find eligible candidate cases and expose eligibility risks before the
lock record is patched.

This phase should move Orca from
`BLOCKED_OWNER_CANDIDATES_NEEDED` toward
`READY_FOR_HEAVYWEIGHT_DISCOVERY_ACCEPTANCE`. It does not make discovery
active by itself. Owner acceptance is still required before any search,
external inspection, or candidate discovery begins.

## 4. Discovery Authorization Boundary

After owner acceptance, the discovery phase may inspect only enough public,
market-level information to assess case eligibility.

Discovery may inspect:

- whether a candidate case exists;
- candidate names;
- market or domain;
- rough timeline;
- public inspectability at a high level;
- possible decision owner or decision context;
- buyer-visible belief or consequence;
- plausible cutoff date or cutoff window;
- reasons a candidate may or may not fit the first proof-run locks.

Discovery must distinguish eligibility inspection from evidence
interpretation.

Eligibility inspection can ask:

- does this case exist;
- is it buyer-visible or historically bounded;
- is there a plausible decision owner or context;
- is public inspection later plausible;
- can a fair cutoff potentially be defined;
- would this case test Core Spine without obvious cherry-pick risk.

Evidence interpretation cannot ask:

- whether the signal was strong;
- whether the narrative had traction;
- whether buyers actually changed behavior;
- what recommendation Core Spine would make;
- whether the backtest would pass;
- whether the outcome proves anything.

The discovery phase may assess candidate eligibility. It may not interpret the
underlying evidence for decision strength, buyer behavior, backtest judgment,
or proof result.

## 5. Allowed Discovery Activities

If and only if the owner accepts this charter, discovery may perform bounded
candidate-finding and eligibility assessment.

Allowed activities:

- identify candidate shadow-satellite case names;
- identify candidate historical backtest case names;
- identify market or domain for each candidate;
- identify rough timelines without building a source inventory;
- identify plausible decision owner or decision context;
- identify buyer-visible belief or consequence for shadow candidates;
- identify plausible cutoff candidates or cutoff windows for backtest
  candidates;
- assess whether later public inspection appears plausible;
- record known eligibility risks;
- record why a candidate belongs in the candidate universe;
- record why a candidate should be downgraded, excluded, or left unresolved;
- return blocked if the candidate universe cannot be built within this
  boundary.

Discovery may use public, market-level information only. It must remain
manual, docs-first, non-deceptive, and non-runtime.

## 6. Forbidden Activities

The discovery phase must not perform or produce:

- proof execution;
- decision memo (Memo) drafting;
- Evidence Units (EvidenceUnit);
- signal-strength scoring;
- recommendation verbs;
- backtest judgment;
- outcome comparison;
- source maps;
- source inventory;
- recurring monitoring;
- data spine;
- scraper, API, dashboard, database, automation, scoring engine, tests, or
  implementation;
- feature planning;
- customer-discovery claim;
- external willingness-to-pay claim.

The phase also must not:

- collect exact proof evidence for later memo use;
- interpret whether engagement proves demand;
- interpret whether a competitor narrative is strong;
- judge whether a backtest would have passed;
- compare pre-cutoff evidence against post-window outcomes (Outcome);
- create marketing demos;
- package a case library;
- use private, intrusive, deceptive, or ordinary-person dossier material;
- import `jb` paths, lifecycle mechanics, templates, validation habits, or
  success logic as Orca authority.

For avoidance of ambiguity, the later discovery results artifact may make a
case-selection proposal for one shadow decision and one backtest case. It must
not use Core Spine action recommendation verbs or recommend any product,
positioning, pricing, growth, competitive, or investment action.

## 7. Shadow-Satellite Candidate Eligibility

A candidate shadow case must be one buyer-visible competitor narrative
pressure decision.

It must not become broad competitor monitoring. It must stay tied to one
candidate decision in which a decision owner may later need to decide whether
to `Watch`, `Probe`, `Test`, `Hold`, or `Move` in response to buyer-visible
narrative pressure. Discovery may record those allowed proof-run verbs as part
of the existing satellite frame, but it must not apply them to the evidence or
use them as recommendations.

A shadow-satellite candidate is eligible for the candidate universe only if it
can be recorded with:

- candidate name;
- market or domain;
- decision owner or decision context;
- buyer-visible belief or consequence;
- competitor or actor narrative;
- why the case is buyer-visible;
- eligibility-level reason it may create response pressure;
- later public inspectability surface, without source-map detail;
- known eligibility risks;
- reason for inclusion in the candidate universe.

Exclusion or downgrade reasons include:

- no buyer-visible belief or consequence can be named;
- the case is only analyst-visible or operator-interesting;
- the case would require broad competitor monitoring;
- the case appears to require private, deceptive, or intrusive access;
- the case cannot be bounded to one decision;
- the case appears to import `jb` finance-career assumptions;
- the case would require new Core Spine primitives.

## 8. Backtest Candidate Eligibility

A candidate backtest case must be one historical decision case with a later
outcome known.

It must be eligible for leakage-controlled replay only if discovery can record
a plausible pre-interpretation cutoff and a reason the later outcome was not
already obvious at that cutoff. Discovery may identify that a later outcome is
known, but it must not compare the outcome to pre-cutoff evidence or judge
whether Orca would have been right.

A backtest candidate is eligible for the candidate universe only if it can be
recorded with:

- candidate name;
- decision context;
- case-selection owner or source;
- proposed cutoff date or cutoff window;
- why the cutoff may be fair;
- eligibility-level reason the outcome was not already obvious at cutoff;
- plausible pre-cutoff public visibility;
- post-window exclusion rule;
- anti-cherry-pick rationale;
- known leakage risks;
- reason for inclusion in the candidate universe.

Exclusion or downgrade reasons include:

- no plausible fair cutoff can be named;
- the outcome appears already obvious before the cutoff;
- public pre-cutoff visibility is not plausible;
- post-window evidence cannot be cleanly excluded;
- the case is selected only because its later outcome is famous or persuasive;
- the case would function mainly as a marketing demo;
- the case requires private, deceptive, intrusive, or runtime-only access.

## 9. Candidate Universe Requirements

Discovery should produce a small but real candidate universe, not a single
cherry-picked case.

Target universe:

- 3-6 shadow-satellite candidate cases;
- 3-6 historical backtest candidate cases.

The discovery output may return fewer only if it explains why the universe
could not be built within the allowed boundary. A smaller universe is allowed
only when the blocker is source reality or boundary discipline, not convenience.

No candidate is selected for the proof merely by appearing in the universe.
The universe is an input to owner selection and later lock-record patching.

## 10. Candidate Evaluation Fields

Each candidate should be recorded in a concise table or repeated field block.
The discovery results artifact should keep the two candidate classes separate.

Shadow candidate fields:

- candidate ID;
- candidate name;
- market or domain;
- decision owner or context;
- buyer-visible belief or consequence;
- competitor or actor narrative;
- eligibility-level response-pressure rationale;
- later public inspectability surface, without source-map detail;
- eligibility strengths;
- eligibility risks;
- inclusion reason;
- disposition: include, downgrade, exclude, or unresolved.

Backtest candidate fields:

- candidate ID;
- candidate name;
- decision context;
- case-selection owner or source;
- proposed cutoff date or cutoff window;
- eligibility-level cutoff fairness rationale;
- eligibility-level rationale for why the outcome was not already obvious at
  cutoff;
- plausible pre-cutoff public visibility;
- post-window exclusion rule;
- anti-cherry-pick rationale;
- leakage risks;
- inclusion reason;
- disposition: include, downgrade, exclude, or unresolved.

Candidate fields are eligibility fields. They are not Evidence Units, source
maps, source inventories, signal scores, memo sections, or proof conclusions.

## 11. Anti-Leakage Rules

Discovery must preserve proof integrity before any lock record patch.

Anti-leakage rules:

- define candidate eligibility before interpreting evidence;
- do not select a candidate because known evidence looks favorable;
- do not select a backtest case because the later outcome is persuasive;
- do not infer demand from public engagement;
- do not infer buyer behavior from narrative visibility;
- do not compare pre-cutoff material to post-window outcomes;
- do not use post-window knowledge to choose a cutoff that flatters Orca;
- do not record exact source maps or source inventories;
- do not create Evidence Units during discovery;
- do not draft at-cutoff recommendations;
- preserve downgrade, exclusion, blocked, and unresolved states;
- document leakage risks before proposing any case for selection.

If discovery cannot maintain this separation, it must stop and return
`BLOCKED_BY_PROOF_LEAKAGE_RISK`.

## 12. Stop Criteria

Discovery must stop and return to owner review if any of these occur:

- owner acceptance of this charter is missing or ambiguous;
- discovery cannot stay limited to candidate-finding and eligibility
  assessment;
- candidate work starts interpreting signal strength, narrative traction,
  buyer behavior, or backtest result;
- the work requires source maps, source inventory, recurring monitoring, a
  data spine, source collection architecture, scraper, API, dashboard,
  database, automation, scoring engine, tests, implementation, or feature
  planning;
- the shadow-satellite candidate set becomes broad competitor monitoring;
- backtest candidate selection depends on post-window evidence comparison;
- fair cutoff windows cannot be proposed without hindsight leakage;
- private, intrusive, deceptive, or person-level dossier material would be
  needed;
- `jb` authority leaks into Orca or into the shadow-satellite candidate set;
- fewer than the target candidates can be found and the reason cannot be
  explained inside the boundary;
- the discovery output cannot produce a case-selection proposal or a clear
  blocked state.

Stopped discovery is not proof failure. It means the next valid step is owner
review of the blocker, not proof execution.

## 13. Expected Discovery Output

The later discovery pass should produce a separate discovery artifact:

`docs/product/core_spine_v0_heavyweight_proof_case_discovery_results_v0.md`

Do not create that results artifact until heavyweight discovery is explicitly
accepted and run.

The later results artifact should contain:

- source basis and anti-leakage declaration;
- discovery boundary actually used;
- shadow-satellite candidate universe;
- historical backtest candidate universe;
- candidate evaluation fields;
- downgraded, excluded, and unresolved candidates;
- known eligibility risks;
- a case-selection proposal for one shadow decision and one backtest case, or a
  blocked verdict;
- the exact fields needed before the lock record can be patched.

If the results artifact proposes one shadow decision and one backtest case, the
proposal is only for case selection. It is not a Core Spine recommendation,
proof result, backtest judgment, or decision memo.

## 14. How This Feeds The Lock Record

If owner-accepted discovery later produces an acceptable results artifact, the
results may become decision input for
`docs/product/core_spine_v0_first_proof_run_locks_v0.md`.

The lock record can be patched only after all of these are true:

- the results artifact supplies enough case-level fields;
- the owner accepts or selects the exact shadow and backtest cases from the
  candidate universe;
- the owner separately authorizes the lock-record patch.

Required case-level fields:

- exact buyer-visible narrative pressure decision;
- decision owner or decision context;
- buyer-visible belief or consequence;
- selected market or domain;
- case-specific costly behavior standard or the owner decision needed to set
  it;
- actor or competitor behavior that matters;
- admissibility and blind-spot notes without exact source maps;
- exact historical backtest case;
- case-selection owner or decision source;
- cutoff date or cutoff window;
- why the cutoff is fair and before the outcome was obvious;
- anti-cherry-pick rationale;
- case-specific pre-cutoff visibility requirement;
- case-specific post-window exclusion rule;
- leakage risks that must be controlled before evidence interpretation.

Patching the lock record would still not run the proof by itself. It would only
complete the pre-evidence locks needed before proof evidence work can begin
under the accepted first proof-run charter.

## 15. Explicit Non-Claims

This charter does not claim:

- heavyweight discovery is authorized yet;
- candidate discovery has been performed;
- any source has been searched;
- any external source has been inspected;
- any candidate case has been selected;
- the first proof-run lock record can be patched now;
- Core Spine v0 is proof-ready;
- proof execution may begin;
- evidence collection may begin;
- evidence interpretation may begin;
- a decision memo may be drafted;
- a backtest may be executed;
- a backtest will pass;
- a competitor narrative has traction;
- buyers changed behavior;
- external customers will pay;
- a data spine should be built;
- feature planning is ready;
- implementation planning is ready;
- implementation is authorized;
- scrapers, APIs, dashboards, databases, automation runtimes, scoring engines,
  software tests, source maps, source inventories, recurring monitoring, or
  tooling should be created.

## 16. Current Verdict

Current verdict: `READY_FOR_OWNER_ACCEPTANCE_OF_DISCOVERY_SCOPE`.

This charter is coherent enough for owner review. If the owner accepts it, the
next valid step is one bounded heavyweight discovery pass that creates a small
candidate universe for proof-case selection. Discovery is not authorized yet,
and proof execution remains blocked until the first proof-run locks are
completed.
