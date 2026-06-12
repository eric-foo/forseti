# Data Capture Harness Operating Model Architecture v2

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Proposed hybrid operating-model architecture for Orca's Data Capture Harness, using v1 as the base while resolving the v0/v1 adversarial review findings and the independent v2 review findings about blocker-resolution authority and primitive stability classification.
use_when:
  - Deciding whether to owner-accept the Data Capture Harness operating-model architecture.
  - Checking how commissioned Data Capture should operate against the accepted obligation baseline without drifting into ECR, Cleaning, Judgment, runtime, source maps, or implementation.
  - Preparing a bounded pressure-test commissioning decision after owner acceptance.
  - Reviewing whether the second-operator check is a capture-visibility control rather than hidden approval, validation, or Judgment.
authority_boundary: retrieval_only
open_next:
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_v0.md
  - docs/product/data_capture_spine/data_capture_harness_operating_model_architecture_v1.md
  - docs/product/data_capture_spine/data_capture_harness_operating_model_architecture_v0.md
  - docs/product/data_capture_spine/data_capture_obligation_baseline_decision_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/product/data_capture_spine/data_capture_harness_product_goal_direction_signal_decision_v0.md
  - docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
stale_if:
  - Owner accepts, rejects, patches, or supersedes this v2 proposed architecture.
  - The Data Capture obligation baseline decision is amended, rejected, or superseded.
  - The Data Capture obligation contract is materially revised or superseded.
  - The Data Capture Harness Direction Signal decision is superseded.
  - An accepted ECR architecture lane changes the categorical handoff boundary.
  - Pressure-test evidence from 3-5 real commissioned captures shows that the operating-model controls here are too heavy, too light, or mis-shaped.
```

## Status

Status: `PROPOSED_ARCHITECTURE_V2`.

Architecture result: `TARGET_RECOMMENDED_FOR_OWNER_ACCEPTANCE_AFTER_INDEPENDENT_REVIEW_PATCH`.

Selected target: `Contract-pinned obligation-discharge operating envelope with second-operator capture-visibility check`.

This artifact is a bounded v0/v1 hybridization patch. It uses v1 as the base because v1 is more source-grounded, more explicit about known operating failure modes, and more protective against per-slice flattening and downstream leakage. It absorbs v0's safer second-operator framing and lighter owner-routing posture before owner acceptance.

It also incorporates the two independent adversarial review findings against the first v2 draft: `F-01` blocker-resolution authority and `F-02` classification of new v2 primitives.

This artifact does not claim validation, hardening, readiness, Data Capture Spine completion, implementation authority, runtime or tooling authorization, ECR/Cleaning/Judgment design authority, buyer proof, commercial readiness, source-of-truth promotion beyond the accepted obligation baseline decision, or pressure-test discharge. Owner acceptance is still required before this proposed architecture becomes controlling for later commissioned-capture work.

## Source Readiness

`SOURCE_CONTEXT_READY`

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3/S4 bounded Data Capture Harness v0/v1 hybridization pack
  edit_permission: docs-write for this product artifact only
  target_scope:
    - docs/product/data_capture_harness_operating_model_architecture_v2.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/data_capture_harness_operating_model_architecture_v0.md
    - docs/product/data_capture_harness_operating_model_architecture_v1.md
    - docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_v0.md
    - docs/product/data_capture_obligation_baseline_decision_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
```

Compact source ledger:

| Source | Why read | Claim supported | Status note |
| --- | --- | --- | --- |
| Current owner instruction | Authorized proceeding after AR-01/AR-02 deliberation | Bounded docs-only hybridization patch is allowed | user-stated |
| Current owner instruction after independent review | Authorized patching all independent-review findings before lane thesis work | Bounded docs-only v2 patch for F-01 and F-02 is allowed | user-stated |
| `AGENTS.md` | Orca project authority and overlay requirement | Docs-only work allowed; implementation requires explicit bounded authorization | clean in named-path status |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint | Orca overlay controls project facts | modified |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy | User instruction, AGENTS, overlay, then Orca docs control | modified |
| `.agents/workflow-overlay/source-loading.md` | Source-pack and not-proven boundaries | Dirty/untracked sources may support advisory docs work but not validation/readiness/proof claims | modified |
| `.agents/workflow-overlay/artifact-roles.md` | Product artifact destination | `docs/product/` is valid for product artifacts | modified |
| `.agents/workflow-overlay/review-lanes.md` | Review authority and read-only boundaries | Prior review findings are decision input, not automatic patch authority | modified |
| `.agents/workflow-overlay/validation-gates.md` | Completion and strict-claim gates | No strict readiness or validation claim from dirty/untracked state | modified |
| `docs/product/data_capture_harness_operating_model_architecture_v1.md` | Hybrid base | v1 strengths: source grounding, per-slice safeguards, known failure-mode coverage, strong bloat-cut queue | untracked |
| `docs/product/data_capture_harness_operating_model_architecture_v0.md` | Safer framing to import | v0 strength: second operator as control surface, not primary architecture or Judgment lane | untracked |
| `docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v0_v1_adversarial_review_v0.md` | Patch trigger | `hybridize_v0_v1_before_acceptance`; AR-01/AR-02 blocking findings; AR-03 advisory wording fix | untracked |
| `docs/review-outputs/adversarial-artifact-reviews/data_capture_harness_operating_model_architecture_v2_independent_adversarial_review_v0.md` | Independent review of first v2 draft | `accept_v2_with_watch_items`; F-01 and F-02 should travel as watch items or be patched before acceptance | untracked |
| `docs/product/data_capture_obligation_baseline_decision_v0.md` | Accepted baseline | Owner accepted current obligation baseline for bounded harness operating-model architecture only | untracked |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Controlling obligation contract | Six discharge states, 16 obligations, forbidden Capture outputs, pressure-test requirement | clean in named-path status |
| `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md` | Product-goal and demotion decision | Manual harness and BT2-04 dry run are direction signal only, not architecture or validation | untracked |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Layer boundary | Capture must stay separate from ECR, Cleaning, Judgment, runtime, and source-system work | clean in named-path status |

Dirty/untracked caveat: the worktree is broadly dirty and includes modified overlay files plus untracked product, prompt, and review artifacts. These sources are sufficient for this proposed docs-only hybrid artifact. They do not prove validation, hardening, readiness, source-of-truth promotion, product proof, implementation authority, or owner acceptance of this v2 architecture.

## Hybridization Decision

The v0/v1 adversarial review recommended `hybridize_v0_v1_before_acceptance`.

This v2 applies that recommendation as a bounded architecture patch:

| Review finding | v2 closure move |
| --- | --- |
| AR-01: Reviewer checkpoint can become hidden approval/refusal authority | Replaces "adversarial reviewer checkpoint" and refusal/approval verbs with a second-operator capture-visibility check. The second operator can record only capture-owned closure blockers and visible capture limitations. |
| AR-02: v1 overweights the operating model before real pressure tests | Distinguishes stable inherited baseline obligations from pressure-test candidate operating controls. Role count, checkpoint naming, declaration form, exact handoff ceremony, and roster details stay mutable until pressure-test evidence returns. |
| AR-03: "locked now" wording overclaims architecture status | Replaces "locked now" with "inherited from the current accepted baseline for this proposed architecture." |

This hybrid does not patch the obligation contract, v0, v1, the manual harness, the BT2-04 dry run, the review report, ECR, Cleaning, Judgment, source systems, runtime, or tooling.

## Independent Review Patch

The independent adversarial review of the first v2 draft recommended `accept_v2_with_watch_items` and found no blocking findings. The owner chose to patch the watch items before treating architecture work as done.

This version incorporates both findings:

| Independent review finding | Patch |
| --- | --- |
| F-01: `capture_closure_blocker` resolution authority is undefined | The Role Model now names blocker-resolution authority. The capture operator owns remediation of capture-owned blockers. The commissioner owns Decision Frame, source-boundary, or stop/re-scope decisions. The second operator remains a recorder of visible blockers and limitations, not a re-approval authority. |
| F-02: New v2 architecture primitives are not classified as stable or candidate | The Pressure-Test Candidate Operating Controls section now classifies the five-role model, two-output second-operator vocabulary, and capture-operator remediation vocabulary as pressure-test candidate primitives, not stable inherited baseline obligations. |

## Architecture Frame

The architecture question remains:

```text
What operating model makes commissioned Orca Data Capture visibly discharge, or visibly fail to discharge, every accepted capture obligation across operators, sessions, modes, and source families without drifting into ECR, Cleaning, Judgment, runtime, tooling, source-family-as-core, or single-operator checklist theater?
```

Starting point:

- The accepted obligation baseline is `ACCEPTED_BASELINE_DECISION_V0`.
- The controlling obligation contract defines 16 core obligations and six discharge states.
- The manual harness plus BT2-04 dry run is a direction signal only.
- v1 is the stronger base but over-weights the reviewer checkpoint.
- v0 supplies the safer second-operator framing to preserve.

## Target Architecture

Architecture result: `TARGET_RECOMMENDED`.

Selected target: `Contract-pinned obligation-discharge operating envelope with second-operator capture-visibility check`.

This target wins because it is the smallest architecture that can satisfy the accepted obligation contract across operators and sessions while avoiding the two false solutions:

- a single-operator checklist that cannot reliably expose silent omission, mode drift, per-slice flattening, or agent-boundary drift;
- a review-first or refusal-first architecture that turns a checking role into hidden approval, validation, or Judgment.

The target keeps v1's core strength: every commissioned capture must expose obligation discharge or obligation failure visibly, including per-slice states when the contract requires them. It keeps v0's safety: the second operator is a control surface, not the architecture's brand, not an approval lane, not a proof lane, and not Judgment.

## Stable Inherited Baseline Obligations

These are inherited from the current accepted obligation baseline for this proposed architecture. They are not newly validated by this artifact and are not hardened by this artifact.

- Commissioned-only scope: no Data Capture session opens without a Decision Frame sufficient to evaluate capture obligations.
- Six discharge states: every core obligation must be marked as `met`, `partial`, `blocked`, `unavailable_by_source`, `not_applicable`, or `not_attempted`.
- Silent omission is forbidden. Obligation absence is not an obligation state.
- Capture modes are disclosed using the obligation contract's mode vocabulary: human-led, agent-assisted, structured access, archive/history, automated extraction, multimodal, and mixed.
- Mid-session mode changes are made visible when they occur.
- Agent assistance stays within the allow/forbid split. Agents may enumerate, fetch, archive, transcribe, link, and mechanically group exact URLs or identical locators. They must not rank relevance, filter candidates before presentation, summarize for admissibility, decide missing context, classify credibility, exclude signals, or decide downstream use.
- When raw source format is too transport-heavy for later inspection, Capture may produce a Data Capture Projection Packet: preserved raw source, mechanical source-projected rows, and a projection receipt. Projection may remove source-envelope noise from the working view. It must not remove evidence rows because they appear low-value, low-score, repetitive, deleted, or unhelpful.
- Capture may not emit forbidden outputs: credibility labels, integrity classifications, discounting decisions, exclusion decisions, Signal Use Classification, Decision Strength, Action Ceiling, semantic dedupe or clustering effects, Cleaning transformations, final ECR field architecture, source-quality scores, source maps as core architecture, or runtime implementation plans.
- Per-slice posture is required for archive/history, source visibility/access, related context, and re-capture semantics when mixed source states or locators would otherwise be hidden.
- Source-family heuristics remain satellite unless promoted under the Source-Family Promotion Rule.

## Pressure-Test Candidate Operating Controls

These controls are part of this proposed architecture, but their exact weight and form remain mutable until 3-5 real commissioned pressure tests return evidence.

- Role count and exact role boundaries.
- Name and ceremony of the second-operator capture-visibility check.
- The five-role model named below: commissioner, capture operator, agent assistant, second operator / capture-visibility checker, and downstream receiver.
- The two-output second-operator vocabulary: `capture_closure_blocker` and `visible_capture_limitation`.
- The capture-operator remediation vocabulary: correction, stop, rerun, and re-capture posture.
- Shape of the per-obligation discharge declaration.
- Exact handoff ceremony between capture operator, second operator, commissioner, and downstream receiver.
- Operator-roster categories for pressure testing.
- Numeric re-architecture thresholds.
- Minimum continuity artifact shape for interruption, resume, and re-capture.

Owner acceptance of this v2 would accept the target operating architecture for pressure testing. It would not harden these controls, validate them, prove repeatability, or authorize implementation.

The named role set and vocabularies above are pressure-test candidate primitives. They are useful operating language for the proposed architecture, but they are not inherited baseline obligations, not validated terminology, and not permanent harness vocabulary until pressure-test evidence supports keeping them.

## Role Model

- **Commissioner.** Supplies the Decision Frame, cutoff posture, downstream-use intent, and source boundary. The commissioner does not certify capture quality, decide source usefulness, or move Judgment into Capture.
- **Capture operator.** Runs the commissioned session, declares mode, records source-visible facts, preserves raw observables and limits, marks obligation states, records blockers, and stops when capture-owned preconditions are not met.
- **Agent assistant.** Performs only allowed agent verbs under the capture operator's direction. It cannot rank relevance, filter candidates before presentation, decide admissibility, classify credibility, exclude signals, or decide downstream use.
- **Second operator / capture-visibility checker.** Checks whether capture-owned obligation visibility, source limits, mode changes, raw observable preservation, failure visibility, and layer boundaries are visible enough for categorical handoff. This role is a control surface, not the primary architecture and not a Judgment lane.
- **Downstream receiver.** ECR, Cleaning, and Judgment consumers may later inspect the captured basis and return layer-owned blockers. They do not redefine capture obligations during the session.

The second operator may record only two kinds of output:

- `capture_closure_blocker`: a capture-owned omission or boundary violation that prevents a clean categorical handoff, such as silent omission, hidden mode change, per-slice rollup where states differ, raw-observable loss, hidden failure, forbidden agent verb, or forbidden Capture output.
- `visible_capture_limitation`: a non-blocking capture limitation that must travel downstream, such as source-limited actor identity, failed archive attempt, fallback access, unknown timing, partial related context, or modality limitation.

The second operator must not:

- approve sources;
- certify quality;
- validate the capture;
- decide inclusion, admissibility, credibility, independence, representativeness, usefulness, or downstream use;
- score operators or captures;
- require Judgment, ECR, or Cleaning changes;
- authorize patches;
- create buyer proof, readiness, acceptance, or source-of-truth promotion;
- convert clean handoff into a pass/fail performance label.

If a `capture_closure_blocker` exists, the reason the session cannot cleanly hand off is the capture-owned condition, not second-operator refusal authority. The capture operator records a correction, a stop, a rerun, or a re-capture posture under the architecture's stop conditions.

Resolution authority is bounded:

- The capture operator decides whether a capture-owned blocker has been corrected enough to declare categorical handoff preconditions visibly satisfied.
- The commissioner decides only Decision Frame, source-boundary, or commission stop/re-scope questions when the blocker exposes an upstream frame problem.
- The second operator does not approve remediation, certify closure, refuse closure, validate the capture, or decide downstream use. After remediation, the second operator may record a newly visible `capture_closure_blocker` or `visible_capture_limitation`, but that record remains evidence of a capture-owned condition, not second-operator approval or refusal authority.

## Session Lifecycle

A commissioned capture session moves through conceptual states. These are architecture states, not a workflow diagram, template, data model, schema, or runtime design.

1. **Commissioned-frame intake.** The Decision Frame, cutoff posture, downstream-use intent, and source boundary are known enough to evaluate capture obligations. If not, Data Capture has not started.
2. **Capture setup.** The operator pins the obligation surface, declares initial mode, records session identity at product-method level, and bounds any agent assistance.
3. **Source inspection and observable preservation.** The operator inspects public, market-level, non-deceptive, non-intrusive source surfaces and preserves raw observable, source identity, actor context, timing, cutoff posture, archive/history posture, access limits, related context, bundled-offer structure where relevant, failures, and blockers.
4. **Obligation-state declaration.** Every core obligation is marked with exactly one discharge state, with per-slice declarations where the contract requires them. `blocked` and `not_attempted` carry visible reasons.
5. **Interruption, resume, and re-capture posture.** Operator changes, session interruptions, and re-captures preserve capture-event provenance, mode state, partial obligation states, raw-observable context, changed source state, and supersede/supplement/conflict relationships where relevant.
6. **Second-operator capture-visibility check.** The second operator records any `capture_closure_blocker` or `visible_capture_limitation`. The check does not approve, validate, or judge source usefulness.
7. **Categorical handoff or visible stop.** The session exits by categorical handoff to ECR per Obligation 16 only when capture-owned handoff preconditions are visibly satisfied. Otherwise it exits as a visible stop, blocker, rerun, or re-capture posture.

There is no silent close. There is no rollup-only close when slice-level states differ. There is no reviewer approval label. There is no Judgment decision inside Capture.

## Obligation-Discharge Visibility Commitment

Each commissioned capture must expose a discharge state for every core obligation in a form a second operator can inspect. The architecture does not specify the artifact form: no ledger schema, no obligation field, no state column, no discharge receipt, no data model, no runtime surface.

The commitment is architectural. The form is deferred to a later pressure-test commissioning decision and may remain a brief operating artifact rather than a runtime data shape.

## Failure And Limitation Visibility

Failures, blockers, fallbacks, and not-attempted states are first-class capture outputs.

A failed exact access attempt, failed archive attempt, fallback source route, unavailable source fact, source-limited actor identity, dynamic-page limitation, or not-attempted route must remain visible. A successful adjacent capture does not erase the failed or limited state.

The second operator records hidden failures as `capture_closure_blocker` when they prevent clean categorical handoff, or as `visible_capture_limitation` when the limitation can travel downstream without capture pretending it is resolved.

## Source-Family Satellite Boundary

Source-family content stays satellite by default: forums and threaded chains, review surfaces, changelogs, docs, pricing pages, API or policy pages, bundled offers, archive/history cases, multimodal or dynamic pages, and per-family operator notes.

The only source-family invariant currently promoted to core is the archive/history per-slice posture and recapture-relationship invariant accepted in the obligation-baseline decision.

Satellite guidance may pressure the core only through the Source-Family Promotion Rule:

- two non-overlapping source families surface the same operating-model gap; or
- the owner signs off on one specific invariant claim.

Satellite guidance does not become core by accumulation, convenience, source volume, or repeated operator preference.

## Handoff Boundary

Capture hands off categorical context to ECR. It names what must be inspectable without designing ECR:

- obligation discharge states and visible reasons;
- raw observables and related context;
- source identity and actor context where knowable;
- decomposed timing and cutoff posture;
- archive/history posture, access limits, fallback paths, and failed attempts;
- per-slice posture where states differ;
- re-capture relationships;
- bundled-offer structure where relevant;
- mode disclosure and material mode changes;
- agent-assistance context within the allow/forbid split;
- capture failures, blockers, and limitations.
- when source projection was used, the preserved raw source reference,
  source-projected row view, and projection receipt warnings.

This architecture does not define ECR fields, IDs, keys, tables, storage, data types, receipt structures, schemas, file formats, Cleaning transformations, Judgment rules, or memo/deck claims.

## Stop Conditions And Re-Architecture Triggers

Stop or block categorical handoff when:

- the Decision Frame is missing or vague enough that capture would become free-floating or standing;
- the source boundary would require private, deceptive, intrusive, or ordinary-person dossier collection;
- mode change occurred but was not made visible;
- per-slice posture required by the contract collapsed into a rollup;
- agent assistance crossed a forbidden verb;
- failure was hidden instead of recorded;
- boundary-violating material was captured and worked around rather than treated as out of bounds;
- forbidden Capture output appeared;
- discharge-state justification imported credibility, integrity, discounting, exclusion, Signal Use, Decision Strength, or Action Ceiling vocabulary;
- raw observable was replaced by paraphrase or summary that loses source language, structure, or modality where it carries signal;
- re-capture relationship was not preserved across material source slices.
- a projection step removed evidence rows instead of only source-envelope noise,
  or presented its own self-check as Cleaning validation.

Open a re-architecture lane when:

- the obligation contract is materially revised or superseded;
- pressure-test results from 3-5 real commissioned captures show a recurring obligation the operating model cannot expose without modification;
- a satellite source-family rule is promoted to core;
- an ECR architecture lane changes the categorical handoff boundary;
- owner-authorized capture modes require session-lifecycle changes;
- repeated stop conditions show that the architecture, not only operator practice, is mis-shaped.

## Deferred Implications

Deferred implications are named only as future pressure. None is designed here.

- Per-obligation discharge artifact form.
- Second-operator check artifact form.
- Multi-operator continuity transport and persistence.
- Agent-session logging shape.
- Per-slice locator representation.
- Re-capture relationship representation.
- Data Capture Projection Packet artifact form and naming conventions.
- Snapshot Integrity Class placement.
- Mandatory archive-attempt defaults by source family.
- Source-family satellite registry.
- Operator-roster and 3-5 capture pressure-test commissioning.
- Numeric re-architecture thresholds.
- Any runtime, source system, archive tooling, scraper, API, dashboard, storage, schema, package, automation, test, deployment, commit, push, or PR.

## Bloat-Cut Queue

This architecture explicitly excludes:

- CPOE-ARC or any other acronymized reviewer-first architecture label as the accepted target name.
- Reviewer approval, refusal, pass/fail, quality certification, admissibility, or validation language.
- Detailed field schemas, key shapes, IDs, receipt structures, ledgers, forms, or data models.
- Source maps or source inventories as harness core.
- Source-family playbooks as core.
- Runtime tooling references or implementation plans.
- ECR field architecture, Cleaning transformations, Judgment rules, credibility labels, discounting, exclusion, Signal Use Classification, Decision Strength, or Action Ceiling.
- Standalone Projection Spine, Filtering Layer, source-purification layer, or
  any projection practice that drops evidence rows before ECR/Cleaning.
- Proof-run, buyer-proof, validation, readiness, or commercial claims.
- Operator scoring, certification, training curriculum, or performance rubric.
- Detailed templates or triage instructions for each obligation.
- Re-architecture of ECR, Cleaning, or Judgment intake.

## Non-Claims

This artifact does not claim:

- owner acceptance of this v2 architecture;
- validation;
- hardening;
- readiness;
- source-of-truth promotion beyond the accepted obligation baseline decision;
- Data Capture Spine completion;
- final harness acceptance;
- manual harness validation;
- BT2-04 source validity, credibility, admissibility, representativeness, or decision usefulness;
- ECR readiness, ECR design, ECR field architecture, ECR receipt design, or ECR field promotion;
- Cleaning readiness, Cleaning design, normalization design, or transformation-ledger design;
- Judgment readiness, Judgment design, credibility labels, integrity classifications, discounting, exclusion, Signal Use Classification, Decision Strength, or Action Ceiling readiness;
- buyer validation, willingness-to-pay proof, repeatability proof, product readiness, feature readiness, implementation readiness, or commercial readiness;
- runtime feasibility, runtime authorization, tooling authorization, scraper authorization, API authorization, dashboard authorization, archival-tool authorization, storage authorization, automation authorization, schema authorization, test authorization, package authorization, deployment authorization, commit, push, or PR authorization;
- source rights or data-rights sufficiency;
- source-system architecture or source maps;
- pressure-test discharge against 3-5 real commissioned captures;
- supersession of v0 or v1 unless and until the owner accepts this v2.

Subagent agreement, model agreement, perspective consensus, review recommendation, fixture count, and lack of P0/P1 findings are not validation or acceptance.

## Next Authorized Step

The independent adversarial review has been completed and its two findings have been patched into this artifact. The smallest complete next step is owner routing:

- accept this v2 as the Data Capture Harness operating-model architecture for later bounded pressure-test commissioning planning;
- request a further bounded patch or review;
- reject v2 and reopen architecture.

Under the current owner instruction, a lane-specific Data Capture Spine product thesis may now be written using this architecture as its operating-model basis.

No implementation, runtime, ECR, Cleaning, Judgment, source-system, scraper, API, dashboard, archive tooling, storage, schema, test, package, deployment, commit, push, PR, buyer-facing appendix, source-family registry, pressure-test execution, or operator-roster execution is authorized by this artifact.
