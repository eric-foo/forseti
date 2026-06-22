# Data Capture Harness Operating Model Architecture v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Proposed operating-model architecture for the Data Capture Harness against the accepted Data Capture obligation baseline.
use_when:
  - Reviewing the proposed Data Capture Harness operating model.
  - Checking how accepted capture obligations should be operated across roles, sessions, agent assistance, source-family guidance, and handoff boundaries.
  - Preparing an owner accept/patch/reject decision or read-only adversarial review for this architecture.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/operating_model/data_capture_obligation_baseline_decision_v0.md
  - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_harness_product_goal_direction_signal_decision_v0.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
stale_if:
  - The accepted Data Capture obligation-baseline decision is amended, rejected, or superseded.
  - The Data Capture obligation contract is materially revised or superseded.
  - The Data Capture Harness Direction Signal decision is superseded.
  - The Data Capture / Cleaning / ECR boundary note is superseded in a way that changes capture handoff boundaries.
  - A later Data Capture Harness operating-model architecture supersedes this artifact.
```

## Status

Status: `PROPOSED_ARCHITECTURE_V0`.

Architecture result: `TARGET_RECOMMENDED`.

Target architecture: `Contract-pinned obligation-discharge operating envelope`.

This artifact proposes a bounded Data Capture Harness operating-model
architecture. It does not claim validation, readiness, hardening,
implementation authority, runtime/source-system design, ECR design, Cleaning
design, Judgment design, buyer proof, or source-of-truth promotion.

## Source Readiness

`SOURCE_CONTEXT_READY`

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3 bounded Data Capture Harness operating-model architecture pack
  edit_permission: docs-write for the target product artifact only
  target_scope:
    - docs/product/data_capture_harness_operating_model_architecture_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/data_capture_obligation_baseline_decision_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
```

Compact source ledger:

| Source | Why read | Architecture claim or boundary supported | Status note |
| --- | --- | --- | --- |
| Current launch instruction | Bound execution of the wrapper and full prompt | Plain-model fallback, file-write target, no implementation/runtime/ECR/Cleaning/Judgment work | user-stated |
| `AGENTS.md` | Orca project authority and overlay requirement | Documentation/product artifact work is allowed; implementation requires explicit bounded authorization | clean in repo status |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint | Orca overlay controls project facts and missing authority must be reported visibly | modified |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy and conflict rules | Current user instruction, `AGENTS.md`, overlay, then Orca docs are controlling; `jb` rules are not Orca authority | modified |
| `.agents/workflow-overlay/source-loading.md` | Source-pack, preflight, dirty-state, and Data Capture Spine loading rules | Custom S3 pack and dirty/untracked caveats are valid for advisory architecture but block strict readiness/acceptance claims | modified |
| `.agents/workflow-overlay/prompt-orchestration.md` | Wrapper, output mode, source-gated method, and validation gates | File-write prompt execution can proceed with explicit output mode and source readiness gate | modified |
| `.agents/workflow-overlay/artifact-roles.md` | Product artifact role and write boundary | `docs/product/` is the accepted product artifact destination | modified |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval header contract | Header uses retrieval metadata without creating authority, readiness, or validation proof | clean in repo status |
| `.agents/workflow-overlay/product-proof.md` | Product-proof non-claims | No buyer validation, willingness-to-pay proof, repeatability proof, readiness, or commercial proof is claimed | untracked |
| `docs/prompts/wrappers/data_capture_harness_operating_model_architecture_gpt55_wrapper_v0.md` | Launch wrapper | Plain-model fallback is authorized; subagents must not be falsely claimed | untracked wrapper folder |
| `docs/prompts/product-planning/data_capture_harness_operating_model_architecture_prompt_v0.md` | Full prompt | Target artifact contract, source pack, architecture question, option set, and hard boundaries | untracked product-planning folder |
| `docs/product/data_capture_obligation_baseline_decision_v0.md` | Accepted baseline decision | Current obligation contract may be planned against for bounded harness operating-model architecture | untracked |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Controlling obligation contract | Core capture obligations, explicit obligation states, capture modes, handoff sufficiency, forbidden outputs, source-family promotion, non-claims | clean in repo status |
| `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md` | Product-goal and demotion decision | Manual harness plus BT2-04 dry run is direction signal only, not controlling architecture or validation | untracked |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Layer boundary note | Data Capture, ECR, Cleaning, Judgment, Decision Artifact, and Outcome Memory remain separate | clean in repo status |
| `workflow-deep-thinking` method instructions | Procedural reasoning discipline only | Treat candidate architectures as candidates, compare options, preserve uncertainty and strict-claim boundaries | installed method copy; not Orca authority |
| `workflow-architecture-planning` method instructions | Procedural architecture-planning discipline only | Standard profile with directional, adversarial, and grounding passes; target only if invariant, core/satellite split, non-goals, and blockers are clear | installed method copy; not Orca authority |

Architecture-planning evidence mode: `plain_model_local_fallback`.

Evidence mode: local directional/adversarial/grounding passes.

Subagents launched: none.

Delegated subagent independence: `not proven`.

Evidence caveat: lower independence than delegated subagents.

Local directional pass: advisory input only. The strongest source-backed target
is a contract-pinned operating envelope because the accepted baseline already
defines what capture must discharge, while the direction signal shows the
harness must make that discharge reliable across operators, interruptions, and
agent assistance. This pass supports `TARGET_RECOMMENDED` for AO-2.

Local adversarial pass: advisory input only. The target can still fail if it
becomes a decorated checklist, a review-theater surface, a stealth ECR schema,
a source-family playbook core, or a runtime/tooling design by implication.
Those risks are controlled only if the architecture keeps obligation states
explicit, leaves source-family mechanics satellite, and treats second-operator
review as a boundary check rather than the architecture itself.

Local grounding pass: advisory input only. The architecture should stay small:
pin the obligation contract, define role/session/handoff/failure boundaries,
and cut source maps, dashboards, schemas, automation, scoring, proof claims,
and ECR/Cleaning/Judgment design. The result remains proposed because several
controlling prompt/overlay/product sources are dirty or untracked.

Source gaps: none blocking for a proposed architecture selection. Strict
acceptance, validation, readiness, hardening, implementation readiness, runtime
feasibility, buyer proof, or source-of-truth promotion remain not proven.

Dirty/untracked caveat: the worktree is broadly dirty and includes modified
overlay files plus untracked prompt and product artifacts used by this run.
Those sources are sufficient for this proposed architecture artifact under the
wrapper, but they do not support strict `PASS`, readiness, validation,
acceptance, source-of-truth promotion, buyer proof, implementation readiness,
or architecture correctness claims.

## Architecture Frame

Real architecture question: What operating model should make Orca's accepted
Data Capture obligations reliable across commissioned capture sessions without
turning the harness into runtime tooling, ECR, Cleaning, Judgment, source maps,
or a one-off manual checklist?

Starting point:

- `docs/product/data_capture_obligation_baseline_decision_v0.md` records
  `ACCEPTED_BASELINE_DECISION_V0` and authorizes bounded harness
  operating-model architecture planning against the current obligation
  contract.
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
  defines the obligations the harness must make visible.
- `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md`
  demotes the manual harness plus BT2-04 dry run to direction signal only.
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` keeps
  Data Capture separate from Evidence Candidate Record, Cleaning, Judgment,
  artifacts, and Outcome Memory.

Target operators:

- commissioned capture operator;
- agent-assisted capture operator;
- second operator or reviewer checking discharge visibility and boundary
  discipline;
- owner or decision-frame sponsor commissioning the capture;
- future downstream ECR, Cleaning, Judgment, memo, appendix, and deck consumers.

Explicit non-targets:

- runtime/tooling architecture;
- source-system, source-map, scraper, API, dashboard, archive, screenshot,
  storage, schema, test, package, deployment, commit, push, or PR design;
- ECR field architecture;
- Cleaning transformations;
- Judgment rules, credibility labels, discounting, exclusion, Signal Use
  Classification, Decision Strength, or Action Ceiling;
- manual harness or BT2-04 patching.

## Cartographer Route Influence

- The accepted obligation baseline is treated as the contract pin. The
  architecture explains how to operate it; it does not mutate it.
- The route pushes the architecture toward roles, sessions, handoffs,
  obligation states, failure states, and stop conditions rather than tooling
  or source-system design.
- The direction signal is useful only as pressure evidence. It explains why
  the harness must be repeatable and failure-visible, but it does not control
  the architecture.
- Source-family mechanics remain satellite unless a later accepted decision
  promotes a specific invariant into core.

## Questions This Architecture Must Answer

- Role model: who commissions, captures, assists, checks, resumes, and receives
  the capture output.
- Session lifecycle: how a commissioned capture starts, proceeds, pauses,
  resumes, gets checked, and hands off or stops.
- Multi-operator continuity: how another operator can understand the decision
  frame, source state, capture mode, limitations, and prior session posture.
- Human/agent assistance boundaries: where agents may enumerate, fetch,
  archive, transcribe, link, or mechanically group without ranking relevance,
  filtering candidates, deciding admissibility, or making Judgment calls.
- Obligation-discharge visibility: how every core obligation becomes visibly
  `met`, `partial`, `blocked`, `unavailable_by_source`, `not_applicable`, or
  `not_attempted`.
- Source-family satellite boundary: how source-shaped guidance can adapt
  capture without becoming core law by convenience.
- Handoff to ECR: how Data Capture hands off categorical context without
  designing ECR fields, schemas, IDs, storage, or inclusion logic.
- Stop conditions and re-architecture triggers: when the harness must block,
  rerun, patch, escalate, or reopen the architecture.

## Options Compared

### AO-1: Single-Operator Manual Checklist

Shape: one operator uses a lean playbook around the accepted obligations.

Why it may win: it is small, easy to start, and aligns with the v0 expectation
that human-led capture remains allowed.

Why it loses: the accepted contract is not only a list of checks. It requires
auditable capture-event provenance, mode-change visibility, interruption and
recapture relationship preservation, failure visibility, and categorical
handoff sufficiency. A single-operator checklist would under-model resume,
review, agent assistance, and multi-operator continuity.

Fake-success risk: checklist completion could hide partial, blocked,
unavailable, not-attempted, degraded, fallback, or post-window states.

### AO-2: Contract-Pinned Operating Envelope

Shape: a core operating model pinned to the obligation contract. It defines
roles, session lifecycle, obligation-state visibility, handoff boundaries,
stop conditions, version pinning, and source-family satellite rules.

Why it may win: it directly exercises the accepted baseline without mutating
it. It makes commissioned capture repeatable across operators and sessions,
keeps source-family mechanics subordinate, and preserves failure visibility
without designing runtime tooling or downstream layers.

Why it may lose: if written too broadly, it could become process bloat or
shadow implementation design. If written too narrowly, it could collapse back
into AO-1.

Fake-success risk: polished operating language could still hide whether each
obligation was actually visible. The architecture must therefore require
explicit obligation states and stop conditions.

### AO-3: Source-Family Playbook Core

Shape: make source-family mechanics the primary harness architecture.

Why it may win: source families really do affect context boundaries, timing,
archive posture, modality, actor context, review surfaces, threaded chains,
docs/version pages, and bundled-offer observables.

Why it loses: the obligation contract and boundary note both require
source-family heuristics to start as satellite unless a specific invariant is
accepted into core. Making source-family mechanics core would overfit the
harness and blur the accepted promotion rule.

Fake-success risk: rich source-family detail could feel operationally useful
while silently weakening core invariants and making later capture inconsistent
across families.

### AO-4: Review/Audit-First Harness

Shape: make reviewer inspection and audit flow the primary architecture, with
capture operations subordinate.

Why it may win: the contract needs auditable capture-event provenance and
review should catch hidden omissions, mode changes, and layer boundary drift.

Why it loses: audit is a control point, not the capture architecture. If review
becomes primary, operators may optimize for reviewer pass language instead of
source-grounded capture, raw observable preservation, and explicit limitations.

Fake-success risk: review theater can create confidence without improving
capture completeness, fairness, source-state visibility, or handoff quality.

### AO-5: Runtime/Tooling-First Harness

Shape: treat tooling, archives, dashboards, storage, APIs, screenshots, or
automation as the architecture.

Why it may win: it could later improve repeatability if separately authorized
and if obligations are already testable.

Why it loses: this commission explicitly forbids runtime, source-system,
storage, schema, API, scraper, dashboard, automation, package, test, or
deployment design. The obligation contract also states that runtime archive
tooling and automated extraction are not authorized by the contract.

Fake-success risk: tool-shaped polish could hide that obligation discharge,
source limits, cutoff posture, and layer discipline remain unresolved.

### AO-6: No Target Selected Yet

Shape: defer architecture selection until more sources or decisions are loaded.

Why it may win: it would be correct if the baseline were stale, missing,
unaccepted, or conflicted.

Why it loses: the required source context is present for a proposed
architecture. The baseline is accepted for bounded operating-model planning,
the obligation contract supplies the core invariants, the direction signal is
demoted, and the boundary note preserves non-target layers.

Fake-success risk: unnecessary deferral would preserve ambiguity and delay the
next review or owner decision without improving source grounding.

## Target Architecture

Architecture result: `TARGET_RECOMMENDED`.

Selected target: `Contract-pinned obligation-discharge operating envelope`.

This target wins because it is the smallest architecture that satisfies the
selection threshold:

- stable invariant: every commissioned capture is operated as a
  contract-pinned session whose obligations cannot be silently omitted;
- core/satellite split: core owns obligation discharge, role/session flow,
  failure visibility, handoff boundaries, and version pinning; satellites own
  source-family adaptation;
- known non-goals: runtime, source systems, ECR, Cleaning, Judgment,
  source maps, schemas, automation, and proof claims are excluded;
- no unresolved upstream blocker: the baseline decision authorizes bounded
  harness operating-model architecture planning against the current contract.

The target is not an implementation plan. It is the operating model a later
owner decision, review, or patch prompt can accept, reject, or revise.

## Core Operating Model

Core invariant: every harness run is a commissioned, contract-pinned capture
session that starts from a Decision Frame and ends with visible obligation
states plus an explicit handoff, stop, or re-capture posture. Silent omission
is not allowed.

Core responsibilities:

- preserve the Decision Frame as the start gate;
- pin the obligation-contract version or equivalent rule surface used by the
  session;
- disclose capture mode and material mode changes;
- keep human, agent-assisted, structured, archive/history, automated,
  multimodal, and mixed capture modes subordinate to obligation discharge;
- preserve raw observable/source-language evidence enough for downstream
  inspection without replacing it with Orca interpretation;
- preserve source identity, actor context, timing categories, cutoff posture,
  archive/history posture, source visibility/access limits, related context,
  bundled-offer observables, capture failures, and re-capture relationships
  where applicable and knowable;
- make every core obligation visible as `met`, `partial`, `blocked`,
  `unavailable_by_source`, `not_applicable`, or `not_attempted`;
- hand off categorical context to ECR without defining ECR fields, keys, IDs,
  tables, storage, schemas, or formats;
- expose captured-but-unusable states without turning them into Judgment.

Role model:

- Commission owner: supplies the decision question, owner context,
  consequence, allowed decision verbs, source boundary, cutoff posture, and
  intended downstream use. This role does not authorize boundary violations or
  downstream Judgment inside Capture.
- Capture operator: runs the commissioned session, preserves source-visible
  facts, marks obligation states, records limitations, and stops when boundary
  or source blockers require it.
- Agent assistant: may enumerate, fetch, archive, transcribe, link, and
  mechanically group exact URLs or identical locators. It must not rank
  relevance, filter candidates before presentation, decide missing context,
  classify credibility, exclude signals, or decide downstream use.
- Second operator or reviewer: checks whether obligation discharge, source
  limits, mode changes, raw observable preservation, and layer boundaries are
  visible. This role is a control surface, not the primary architecture and
  not a Judgment lane.
- Downstream receiver: ECR, Cleaning, and Judgment consumers may inspect the
  captured basis and return layer-owned blockers, but they do not redefine
  capture obligations during the session.

Session lifecycle:

1. Commissioned frame intake. Confirm the Decision Frame, owner context,
   consequence, allowed verbs, source boundary, cutoff posture, and intended
   downstream use are known enough to start.
2. Capture setup. Pin the obligation surface, declare capture mode, session
   identity, operator category, allowed agent assistance, and source-family
   satellite guidance to be consulted.
3. Source inspection. Inspect source surfaces under the allowed boundary while
   preserving source-visible language, source identity, actor context, timing,
   visibility, archive/history posture, related context, and access limits.
4. Capture note and observable preservation. Preserve enough raw observable,
   source-language, modality, layout, related chain, version, bundle, or
   packaging context for downstream inspection.
5. Obligation-state marking. Mark each core obligation explicitly as met,
   partial, blocked, unavailable by source, not applicable, or not attempted,
   including the reason for any non-met state.
6. Interruption and resume. Preserve what was inspected, what remains unknown,
   what mode changed, what failed, and whether re-capture is required or should
   be considered.
7. Second-operator check. Inspect discharge visibility, boundary compliance,
   raw observable preservation, and layer discipline before handoff.
8. Downstream handoff or stop. Hand off categorical context to ECR only when
   capture limitations are visible enough for downstream layers to proceed
   without recollecting source history. Otherwise stop, block, rerun, or
   re-capture.

Review points:

- before session start, when the Decision Frame or source boundary is
  incomplete;
- when capture mode changes materially;
- when source access degrades, fails, uses fallback, or becomes archive-only;
- before handoff to ECR;
- when another operator resumes a session;
- when a source-family rule appears to deserve core promotion;
- when repeated failures suggest an obligation, harness, or architecture
  defect.

Handoff boundary:

Capture hands off inspectable categorical context and visible limitations. It
does not decide credibility, independence, source quality, inclusion,
exclusion, admissibility, Signal Use Classification, Decision Strength, Action
Ceiling, cleaning transformations, or memo/deck claims.

Version pinning:

- baseline decision: `ACCEPTED_BASELINE_DECISION_V0`;
- obligation surface: current
  `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`;
- direction signal: `Data Capture Harness Direction Signal v0`, input only;
- this artifact: `PROPOSED_ARCHITECTURE_V0`.

Change triggers:

- accepted baseline amended, rejected, or superseded;
- obligation contract materially revised;
- source-family satellite rule accepted into core;
- repeated source-family failures show a missing core invariant;
- second-operator checks repeatedly catch hidden omission or layer leakage;
- downstream ECR/Cleaning/Judgment cannot proceed without recollecting source
  history despite visible capture states;
- owner later authorizes runtime or implementation planning, changing the
  design lane.

## Satellite Guidance Boundary

Source-family guidance belongs in satellite unless a specific invariant is
accepted into core through the obligation contract's promotion rule.

Satellite guidance may adapt:

- what related context is usually needed for threaded communities;
- what recency, sorting, moderation, incentive, or experience-timing posture
  matters on review surfaces;
- what version, edit, deprecation, future/current, cache, archive, or backfill
  posture matters for docs, changelogs, pricing pages, API docs, and policies;
- what source-visible framing, dependency, sequence, or packaging cues matter
  for bundled offers, settlements, public-sector deals, regulatory bargains,
  or multi-term proposals;
- when multimodal, layout, screenshot, audio/video, or interaction-dependent
  source meaning must be preserved conceptually;
- what source-family access limits, fallback paths, and archive attempts are
  common enough to guide operators.

Satellite guidance must not:

- redefine the obligation-state vocabulary;
- turn source volume into evidence validity;
- decide credibility, admissibility, integrity, exclusion, Decision Strength,
  or Action Ceiling;
- replace raw observable preservation with summaries;
- turn source-family mechanics into core law without accepted promotion;
- become a source map, inventory, runtime plan, or scraper/API plan.

Satellite pressure path:

1. A capture session exposes a repeated source-family pressure or failure.
2. The operator or reviewer records the pressure as a satellite candidate, not
   a core change.
3. A later decision compares the pressure across at least two non-overlapping
   source families or obtains owner sign-off for one specific invariant.
4. Only then may the invariant be promoted into the core obligation surface.

## Operating Flow

The harness operating flow is:

```text
commissioned frame intake
-> capture setup
-> source inspection
-> raw observable and source-language preservation
-> obligation-state marking
-> interruption/resume or re-capture posture
-> second-operator boundary check
-> categorical handoff to ECR or visible stop
```

Commissioned frame intake checks that the capture is tied to a Decision Frame.
Without the decision question, owner context, consequence, allowed decision
verbs, cutoff posture, and intended downstream use, Data Capture has not
started.

Capture setup declares the rule surface, operator category, session boundary,
capture mode, allowed agent assistance, source boundary, and source-family
satellite guidance. This is product-method orientation, not a schema.

Source inspection preserves what the source showed, who or what performed the
capture at the operator/category level, what source surface or source family
was inspected, what actor or audience context was knowable, what timing was
visible, and what visibility or access limits appeared.

Capture-note and observable preservation keeps source claim separate from Orca
interpretation. The harness must preserve enough raw observable, source
language, related context, bundle structure, modality, or layout posture for
downstream inspection.

Obligation-state marking makes every core obligation explicit as met, partial,
blocked, unavailable by source, not applicable, or not attempted. Unknowns are
allowed only when the unknown state and reason are visible.

Interruption and resume preserve what was inspected, what failed, what changed,
what remains unattempted, and whether a re-capture supersedes, supplements, or
conflicts with earlier capture state. Re-capture does not erase prior capture
history.

Second-operator check inspects whether capture preserved the contract boundary
and made failure visible. It must not become Judgment, source scoring, or proof
theater.

Downstream handoff passes categorical capture context to ECR only when ECR,
Cleaning, and Judgment can proceed without recollecting source history.
Otherwise the outcome is a visible stop, block, rerun, or re-capture posture.

## Stop Conditions And Re-Architecture Triggers

Stop or block when:

- there is no Decision Frame;
- the source boundary would require private, deceptive, intrusive, or otherwise
  out-of-bounds collection;
- cutoff posture is load-bearing but cannot be made visible enough for
  downstream exclusion rules;
- source visibility, access, archive, fallback, migration, deletion, edit, or
  cache state hides material source limitations;
- raw observable, related context, source-language meaning, bundle structure,
  or modality cannot be preserved enough for downstream inspection;
- an agent has ranked relevance, filtered candidates, decided admissibility,
  classified credibility, excluded signals, or otherwise crossed into
  downstream Judgment;
- source-family mechanics are required to proceed but are not yet accepted as
  core or available as satellite guidance;
- the capture would need runtime/tooling/source-system design to continue
  under this commission.

Rerun or re-capture when:

- source state, archive state, cutoff posture, Decision Frame, or capture-mode
  confidence materially changes;
- prior capture forced a global rollup that hid per-slice or per-locator
  differences;
- another operator cannot reconstruct the source claim and limitations without
  recollecting source history;
- downstream layers return a capture-owned blocker.

Patch or escalate when:

- repeated sessions show the same obligation is ambiguous, too coarse, too
  broad, too narrow, or misplaced;
- second-operator checks repeatedly discover hidden `partial`, `blocked`,
  `unavailable_by_source`, or `not_attempted` states;
- satellite guidance repeatedly pressures the same core invariant;
- the direction signal's known harness-level issues would distort another dry
  run if left unresolved.

Re-architecture when:

- the obligation baseline is amended or superseded;
- ECR architecture changes the categorical handoff boundary;
- source-family guidance dominates the core operating envelope;
- runtime or implementation work becomes separately authorized and changes the
  relevant architecture question;
- the contract-pinned operating envelope cannot preserve obligation discharge,
  failure visibility, and layer discipline without becoming an implementation
  design.

## Deferred Implementation Implications

These are non-executable implications only:

- A future authorized runtime would need to preserve session identity,
  obligation-contract version, operator category, capture mode, source-state
  limits, interruption/resume posture, and handoff state without turning those
  concepts into this artifact's schema.
- A future authorized tool surface would need to prevent silent omission and
  make `partial`, `blocked`, `unavailable_by_source`, and `not_attempted`
  states as visible as `met`.
- A future authorized agent-assistance workflow would need explicit guardrails
  against relevance ranking, filtering, admissibility calls, credibility
  classification, exclusion, and Judgment-by-stealth.
- A future authorized review workflow would need to check discharge visibility
  and layer discipline without turning reviewer approval into validation or
  acceptance.
- A future authorized source-family satellite system would need a promotion
  route for specific invariants rather than letting source-family playbooks
  overwrite core law.

No implementation, runtime design, source-system design, storage design,
schemas, tests, packages, deployment, commits, pushes, or PRs are authorized
here.

## Bloat-Cut Queue

- Source maps or source inventories as the harness core.
- Dashboards, monitoring, browser automation, screenshot systems, storage, API,
  scraper, archive, or package design.
- ECR field architecture, Cleaning transformation ledgers, Judgment labels, or
  memo/deck claim rules.
- Source-quality scores, credibility labels, discounting rules, exclusion
  rules, Signal Use Classification, Decision Strength, or Action Ceiling.
- Review/audit theater that makes operators optimize for pass language instead
  of obligation discharge.
- Exhaustive forum, review, docs, pricing, API, policy, archive, or multimodal
  source-family playbooks inside core.
- Proof-run, buyer-proof, validation, readiness, or commercial claims.
- A one-off manual checklist that cannot preserve session continuity, mode
  changes, failed access, fallback posture, and re-capture relationships.

## Non-Claims

This artifact does not claim:

- validation;
- hardening;
- readiness;
- source-of-truth promotion;
- Data Capture Spine completion;
- final harness acceptance;
- manual harness validation;
- BT2-04 source validity, credibility, admissibility, representativeness, or
  decision usefulness;
- ECR readiness or design;
- Cleaning readiness or design;
- Judgment readiness or design;
- Signal Use Classification, Decision Strength, or Action Ceiling readiness;
- buyer validation;
- willingness-to-pay proof;
- repeatability proof;
- product readiness;
- feature readiness;
- implementation readiness;
- commercial readiness;
- runtime feasibility;
- source rights or data-rights sufficiency;
- source-system architecture;
- source maps;
- scraper, API, dashboard, archive, browser automation, screenshot, storage,
  schema, test, package, deployment, commit, push, or PR authorization.

Review consensus, model agreement, local-perspective agreement, fixture count,
source volume, and absence of detected blockers in this run are not validation
or acceptance.

## Next Authorized Step

The smallest complete next action is an owner routing decision for this
proposed architecture:

- commission a separately authorized read-only adversarial artifact review
  against the wrapper, full prompt, accepted baseline decision, obligation
  contract, direction-signal decision, and Data Capture / Cleaning boundary
  note; or
- explicitly accept, patch, or reject this proposed architecture without a
  review.

This run does not execute or authorize review work. Any later review must not
execute implementation, runtime, ECR, Cleaning, Judgment, source-system,
schema, package, deployment, commit, push, or PR work unless a separate future
instruction grants that authority.

Until an owner decision is made, this artifact remains
`PROPOSED_ARCHITECTURE_V0`.
