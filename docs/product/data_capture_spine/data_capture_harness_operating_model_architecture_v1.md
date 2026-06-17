# Data Capture Harness Operating Model Architecture v1

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Proposed operating-model architecture for Orca's Data Capture Harness against the accepted Data Capture obligation baseline, produced under delegated three-subagent evidence; defines roles, session lifecycle, multi-operator continuity, agent-assistance boundaries, obligation-discharge visibility, source-family satellite boundary, handoff to ECR, stop conditions, and re-architecture triggers without designing runtime, ECR, Cleaning, Judgment, source maps, or implementation.
use_when:
  - Planning, reviewing, or pressure-testing a commissioned Data Capture session against the accepted obligation baseline.
  - Checking whether a proposed harness change is operating-model architecture, satellite guidance, downstream lane work, or a hard-boundary violation.
  - Preparing a bounded operator-roster and pressure-test commissioning decision against this architecture.
  - Comparing this delegated-three-subagent proposal with the prior plain-model-fallback proposal at v0.
  - Checking the non-claims and boundaries that travel with this proposed architecture.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/data_capture_harness_operating_model_architecture_v0.md
  - docs/product/data_capture_spine/data_capture_obligation_baseline_decision_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/product/data_capture_spine/data_capture_harness_product_goal_direction_signal_decision_v0.md
  - docs/product/foundation/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
stale_if:
  - The Data Capture obligation baseline decision is amended, rejected, or superseded.
  - The Data Capture obligation contract is materially revised or superseded.
  - The Data Capture Harness Direction Signal decision is superseded.
  - An accepted ECR architecture lane changes the categorical handoff boundary.
  - Pressure-test evidence from 3-5 real commissioned captures shows the operating-model commitments cannot expose obligation discharge.
  - A later operating-model architecture artifact at v2 or higher supersedes this proposed architecture.
```

## Status

`PROPOSED_ARCHITECTURE_V0`

This artifact proposes an operating-model architecture for owner consideration. It does not claim validation, hardening, readiness, implementation authority, runtime or tooling authorization, ECR/Cleaning/Judgment design authority, harness patch authority, source-of-truth promotion beyond the accepted obligation baseline decision, buyer proof, commercial readiness, or pressure-test discharge. Owner acceptance is required before the architecture becomes controlling for later commissioned-capture work.

## Relationship To v0

A prior proposed architecture artifact exists at `docs/product/data_capture_harness_operating_model_architecture_v0.md`. It was produced under `plain_model_local_fallback` evidence mode (no subagents launched; three locally-labeled passes). It is still a valid proposed architecture.

This v1 was produced under `delegated_three_subagents` evidence mode (three separate advisory subagents — directional, adversarial, grounding — each with its own source-readiness gate against a bounded source capsule). The prompt's `repo_preflight` rule forbids silently overwriting an existing target artifact and requires either explicit owner authorization for an update or the next versioned filename plus a visible collision report. Owner authorization to overwrite v0 was not supplied in this turn's launch instruction, so this artifact is created at v1 and the collision is reported here and in the chat closeout.

Both v0 and v1 select an AO-2-derived base (a contract-pinned operating envelope). The principal differences are:

- **Evidence mode**: v1 is `delegated_three_subagents`; v0 is `plain_model_local_fallback` with delegated subagent independence marked `not proven`.
- **Target architecture name**: v1 names "Contract-Pinned Operating Envelope with Adversarial Reviewer Checkpoint (CPOE-ARC)" and gives the reviewer role an explicit refusal-authority charter; v0 names "Contract-pinned obligation-discharge operating envelope" and treats the second-operator role as a control surface without naming a refusal charter.
- **Failure-mode counterweights**: v1 incorporates explicit countermeasures against twenty named failure modes surfaced by the adversarial subagent (most notably `F-STATE-COLLAPSE`, `F-LEAK-ECR`, `F-LEAK-CLEANING`, `F-LEAK-JUDGMENT`, `F-PER-SLICE-FLATTEN`, `F-HARNESS-OSSIFY`, `F-FAKE-SUCCESS-CHECKLIST`). v0 names review-theater, source-family-playbook, schema-leak, and runtime-leak risks at the option-comparison level but does not bake explicit per-mode counterweights into the core operating model.
- **Smallest-complete surface**: v1 uses the grounding subagent's 14-element smallest-complete surface as the artifact's structural floor. v0 organizes around session lifecycle, role model, satellite boundary, deferred implications, and bloat-cut queue with comparable but not identical scope.
- **Obligation-discharge artifact form**: v1 explicitly defers the artifact form of the per-obligation discharge visibility surface (intentionally avoiding "ledger row," "obligation field," "discharge receipt" vocabulary that the adversarial lane flagged as schema-leak risk). v0 uses similar language ("explicit obligation states", "obligation-state marking") and also defers tool form.
- **Next authorized step**: v1 names a bounded operator-roster and pressure-test commissioning decision as the immediate next authorized step. v0 names an owner routing decision (accept/patch/reject this proposed architecture or commission a separately authorized read-only adversarial review).

v1 does not silently supersede v0. The owner may compare the two proposals and accept, patch, reject, hybridize, or commission a review of either.

## Source Readiness

`SOURCE_CONTEXT_READY`

### Preflight receipt

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3 bounded Data Capture Harness operating-model architecture pack
  edit_permission: docs-write for this product artifact only
  target_scope:
    - docs/product/data_capture_harness_operating_model_architecture_v1.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/data_capture_obligation_baseline_decision_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md
    - docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  target_artifact_collision: yes (v0 already exists; v1 created per repo_preflight rule)
```

### Compact source ledger

| Source | Why read | What it supports | Status note |
| --- | --- | --- | --- |
| Current launch instruction | Bounded the operating-model architecture lane | Architecture planning only; no implementation, runtime, ECR/Cleaning/Judgment, or patch authority; no plain-model fallback authorization | user-stated |
| `AGENTS.md` | Orca project authority and overlay requirement | Docs-only default; explicit-authorization boundary for any other lane | clean in named-path status |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint and binding rule | Orca overlay wins for project facts | modified |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy and conflict rules | No jb/generic substitution; missing-source fails visibly | modified |
| `.agents/workflow-overlay/source-loading.md` | Read packs, budgets, capsule contract | Bounded custom S3 pack selected; subagent capsule respected budgets | modified |
| `.agents/workflow-overlay/prompt-orchestration.md` | Source-gated method contract; output modes; collision rule | REFERENCE-LOAD → SOURCE-LOAD → READY → APPLY sequence respected; file-write closeout shape used; next-version suffix used on collision | modified |
| `.agents/workflow-overlay/artifact-roles.md` | Product artifact role and write boundary | `docs/product/` is the docs-write product artifact destination | modified |
| `.agents/workflow-overlay/product-proof.md` | Product-proof non-claims | No buyer/readiness/proof claims | untracked |
| `.agents/workflow-overlay/safety-rules.md` | Project-specific safety and forbidden drift | No runtime/tooling/install/commit/push; smallest complete intervention | modified |
| `.agents/workflow-overlay/communication-style.md` | Closeout shape | Decision-bearing file-write needs headed human summary then receipt | modified |
| `docs/product/data_capture_harness_operating_model_architecture_v0.md` | Prior proposed architecture | Collision check; evidence-mode delta documented in Relationship To v0 | untracked |
| `docs/product/data_capture_obligation_baseline_decision_v0.md` | Accepted baseline and non-claims | Baseline is accepted for architecture planning only; carries non-claims this artifact inherits | untracked |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Controlling obligation contract | The 16 core obligations and 6 discharge states this architecture operationalizes, not patches | clean in named-path status |
| `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md` | Direction signal demotion | Manual harness + BT2-04 dry run is direction signal only, not controlling architecture | untracked |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Layer boundary | Capture must not perform ECR, Cleaning, or Judgment; named handoff boundary | clean in named-path status |
| `workflow-deep-thinking` SKILL.md (agent-workflow plugin source) | Reference-loaded reasoning discipline | Framed real question, failure modes, decision criteria before applying option comparison | reusable workflow source |
| `workflow-architecture-planning` SKILL.md (agent-workflow plugin source) | Reference-loaded architecture-planning mechanics | Three-perspective evidence; option ledger; target architecture; non-execution | reusable workflow source |

### Architecture-planning evidence mode

`delegated_three_subagents`

Three advisory architecture perspective subagents were launched in parallel: directional, adversarial, and grounding. Each received the bounded source capsule (the four required core files plus the architecture question and hard boundaries) and was required to declare `SOURCE_CONTEXT_READY` before producing advice. Each returned advisory-only output with an explicit advisory-only boundary statement. The main planner owns synthesis and did not treat agreement between lanes as proof.

#### Subagent source-readiness receipts

| Lane | Source-readiness | Evidence coverage | Advisory boundary | Notes |
| --- | --- | --- | --- | --- |
| Directional | `SOURCE_CONTEXT_READY` | All four capsule files read end-to-end | Stated verbatim | Recommended AO-2 base with two AO-4-derived add-ins (per-obligation discharge visibility commitment at session close and adversarial reviewer / second-operator role) |
| Adversarial | `SOURCE_CONTEXT_READY` | All four capsule files read; obligation-contract sections, baseline non-claims, direction-signal demotion, and layer boundary all loaded | Stated verbatim | Surfaced 20 named failure modes against AO-2; named the top three threats as state-collapse-plus-checklist-theater, ECR/Cleaning/Judgment leakage cluster, and per-slice-flatten plus harness-ossification |
| Grounding | `SOURCE_CONTEXT_READY` | All four capsule files read in full | Stated verbatim | Produced a 14-item stop list, 10-item defer list, and 14-element smallest-complete operating-model surface; recommended a bounded operator-roster and pressure-test commissioning decision as the next authorized step |

### Dirty / untracked caveat

The worktree is dirty: the overlay files in the source ledger above are modified, and several core source files (the accepted obligation baseline decision, the direction-signal decision, this artifact's own v0 sibling, and other neighbors under `docs/product/`) are untracked. The accepted baseline decision recorded this same state and was owner-accepted via current owner authority, not via source-status promotion. This architecture artifact inherits the same caveat: dirty or untracked status of named sources does not prove acceptance, readiness, source-of-truth promotion, validation, hardening, or buyer proof. The architecture proposal stands or falls on the controlling content of the named sources, not on their git status.

## Architecture Frame

### Real architecture question

What is the target operating-model architecture for Orca's Data Capture Harness so that each commissioned capture visibly discharges, or visibly fails to discharge, every obligation in the accepted Data Capture obligation contract across operators, sessions, modes, and source families — without the harness drifting into ECR, Cleaning, Judgment, runtime, tooling, source-family-as-core, or a single-operator artisan checklist?

### Starting point

- `ACCEPTED_BASELINE_DECISION_V0` recorded in `docs/product/data_capture_obligation_baseline_decision_v0.md`.
- The Data Capture obligation contract at `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` is the controlling product-method contract; this architecture must operationalize it without patching it.
- The current manual Data Capture harness plus BT2-04 dry run is accepted only as `Data Capture Harness Direction Signal v0` and is explicitly not controlling architecture.
- A prior proposed architecture at v0 exists under a different (weaker) evidence mode; this v1 is a parallel proposal at higher evidence quality, not a silent supersession.
- The Data Capture / Cleaning boundary note at `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` defines the layer boundary and the forbidden adjacencies for Capture.

### Target operators and downstream consumers

- **Operators** of this architecture: future Orca operators who will run, review, or commission Data Capture sessions; subsequent architecture, prompt, review, or proof lanes that read this artifact to understand the operating-model boundary; the eventual operator-roster and pressure-test commissioning decision lane that will name 3-5 real commissioned captures.
- **Downstream consumers** of the architecture's output (captures): the eventual Evidence Candidate Record lane and, through it, the Cleaning Spine, Judgment Spine, Decision Artifact, and Outcome Memory layers. None of those lanes is designed by this artifact.

### Explicit non-targets

This architecture does not:

- design ECR fields, schemas, IDs, keys, tables, receipts, storage, or data types;
- design Cleaning transformations, normalization, translation, summarization, dedupe mechanics, or clustering mechanics;
- design Judgment rules, credibility labels, integrity classifications, discounting, exclusion, Signal Use Classification, Decision Strength, or Action Ceiling;
- design source systems, source maps, scrapers, APIs, dashboards, archives, browser automation, screenshot systems, storage, schemas, tests, packages, runtime services, deployment, commits, pushes, or PRs;
- patch the obligation contract, the manual harness, the BT2-04 dry run, the fixture synthesis, or any review artifact;
- claim validation, hardening, readiness, buyer proof, commercial proof, feature readiness, implementation readiness, or source-of-truth promotion beyond the accepted baseline;
- treat the demoted manual harness or BT2-04 dry run as controlling architecture, validation, or template;
- create operator training programs, certification schemes, evaluation rubrics, or operator scoring;
- produce a source-family playbook for any family (those are deferred satellite guidance under the contract's Source-Family Promotion Rule).

## Cartographer Route Influence

The route shaped the actual architecture decision in four ways:

- The route's baseline-pin checkpoint forced this artifact to anchor on the accepted obligation contract's six discharge states, 16 core obligations, mode list, agent-assistance allow/forbid split, and forbidden outputs, rather than reasoning generically about "what a capture harness needs."
- The route's operating-model-frame checkpoint excluded runtime, tooling, ECR, Cleaning, and Judgment design from the architecture surface, which made AO-5 a fast-reject before option comparison and kept "discharge receipt" or "ledger schema" vocabulary out of the target architecture.
- The route's role-and-session-model checkpoint plus its multi-operator continuity criterion ruled out AO-1 (single-operator manual checklist) without further analysis, because a single-operator checklist cannot satisfy Obligation 3 (capture-event provenance), Obligation 5 (mode-change visibility across operators), or the obligation-discharge visibility criterion across operators.
- The route's core/satellite boundary checkpoint and its fork on source-family mechanics ruled out AO-3 (source-family playbook core) by construction, because the contract's Source-Family Promotion Rule requires source-family heuristics to remain satellite unless promoted across two non-overlapping families or by specific-invariant owner sign-off.

## Questions This Architecture Must Answer

The architecture must answer eight questions in product-method language, not in runtime, schema, or tooling language.

- **Role model.** Who acts in a commissioned capture session, and what are the bounded responsibilities and forbidden verbs for each role, including the agent-assistance allow/forbid split from the obligation contract?
- **Session lifecycle.** What states does a commissioned capture session move through, from commissioning through obligation-discharge visibility through reviewer check through named-handoff exit, and which transitions must be visible?
- **Multi-operator continuity.** When an operator change, interruption, or resume occurs inside or across sessions, what state is preserved, what is treated as a new capture-event provenance event, and how is the re-capture relationship preserved per material source slice?
- **Human / agent assistance boundaries.** What is the operating-model line between human-led, agent-assisted, structured access, archive/history, automated extraction, multimodal, and mixed capture modes; how is the mode disclosed; and how is a mid-session mode change made visible?
- **Obligation-discharge visibility.** How is each of the 16 core obligations forced to carry exactly one of the six discharge states without silent omission, and how is per-slice posture preserved for Obligations 10, 11, 12, and 15 when source states differ?
- **Source-family satellite boundary.** What is core operating-model law versus what stays satellite source-family guidance, and how can satellite guidance pressure the core without silently becoming core?
- **Handoff to ECR without designing ECR.** What is handed off categorically to the eventual ECR lane, and where exactly does the architecture stop so it does not pre-architect ECR field shape, receipt structure, IDs, or storage?
- **Stop conditions and re-architecture triggers.** When does the operating model require a session to stop, a capture not to be handed off, the harness to be patched (under separate authorization), or the architecture itself to be re-opened?

## Options Compared

`AO-*` labels are option identifiers only. They are not execution identifiers, not permission to execute, and not numeric severity.

| Option | Why it may win | Why it may lose | Worst fake-success risk |
| --- | --- | --- | --- |
| `AO-1` Single-operator manual checklist | Cheapest to write; closest in shape to existing direction signal; one person can run it end-to-end | Cannot satisfy Obligation 3 (capture-event provenance across operators), Obligation 5 (mode-change visibility for multi-operator or agent-assisted sessions), or the obligation-discharge visibility criterion across operators; offers no second-operator backstop against state-collapse or checklist-theater; is essentially the demoted Direction Signal | Checklist completion in a single operator's hand reads as discharge without a counterparty to refuse session close on collapsed states |
| `AO-2` Contract-pinned operating envelope | Mirrors the contract's own structure (obligations, states, modes, allow/forbid lists, forbidden outputs); preserves the core/satellite split the contract itself uses; future-runtime-aware only as deferred implications | Vulnerable to ECR/Cleaning/Judgment leakage through "discharge receipt" and per-obligation slot vocabulary; vulnerable to state-collapse and checklist-theater because the envelope binds the contract surface but not behavior; vulnerable to per-slice flattening because one-row-per-obligation reads naturally as rollup; lacks a continuous behavioral check against agent-assistance creep | Tool-shaped envelope inherits the contract's vocabulary and feels rigorous without earning it operationally |
| `AO-3` Source-family playbook core | Concrete guidance per family; aligns with how operators encounter sources in practice; reduces ambiguity for any one family | Inverts the contract's Source-Family Promotion Rule by construction; bakes forum / review / changelog mechanics into core without two-family comparison or specific-invariant owner sign-off; the only currently-promoted source-family invariant (per-slice archive/history) is already obligation-contract core, so this option mostly reintroduces satellite content as core | Per-family completeness reads as architecture completeness while the actual obligation discharge across families remains unproven |
| `AO-4` Review / audit-first harness | Names an explicit adversarial check against state-collapse, checklist-theater, and review-as-confirmation; aligns with the harness's product goal of buyer-trustworthy inspectability | Inverts capture-first ordering — review is a checkpoint within capture, not the architecture spine; pulls toward audit-log and receipt vocabulary (runtime/ECR leakage); audit can become the gate rather than commissioning, weakening Obligation 1 | Audit ceremony reads as obligation discharge; the audit itself becomes the artifact rather than the captured signal |
| `AO-5` Runtime / tooling-first harness | None applicable under current authority | Fast-reject by the obligation baseline decision ("does not authorize runtime/tooling-authorized"), the contract ("Runtime archive tooling is not authorized by this contract"), the Direction Signal decision (harness must not become "scraper plan, API or adapter plan, dashboard or monitoring concept, storage schema, runtime, tooling, package, test, or implementation plan"), and `.agents/workflow-overlay/safety-rules.md` | Tool fluency reads as readiness; runtime concreteness reads as discharge |
| `AO-6` No target selected | Reserved for a real upstream blocker | No such blocker is visible: the obligation baseline is accepted; the obligation contract is the controlling source; the boundary note defines the layer split; the direction signal is demoted. Selecting `AO-6` would defer architecture without source evidence to defer | Apparent rigor of "we need more information" masks an avoidable architecture decision |

## Target Architecture

`TARGET_RECOMMENDED`

**Target architecture name:** Contract-Pinned Operating Envelope with Adversarial Reviewer Checkpoint (CPOE-ARC).

**Base:** `AO-2` (contract-pinned operating envelope).

**Deliberate add-ins from `AO-4`:** a per-obligation discharge visibility commitment at session close, and an adversarial reviewer / second-operator role with the explicit charter to refuse session close on collapsed states, rollups that should be per-slice, checklist theater, hidden mode changes, agent-assistance creep, raw-observable loss, or any forbidden Capture output. The add-ins are operating-model commitments, not log shapes or schemas; the artifact form of how each commitment is exposed is intentionally deferred.

### Why this target wins

- **The accepted baseline is contract-shaped, not playbook-shaped.** The controlling source is an obligation contract with 16 numbered obligations, six discharge states, a closed mode list, and a forbidden-outputs list. A contract-pinned operating envelope mirrors the source's own structure and inherits its core/satellite discipline. `AO-3` would bypass the Source-Family Promotion Rule; `AO-4` alone would invert capture-first ordering; `AO-1` cannot carry Obligations 3, 5, or the visibility criterion.
- **The adversarial reviewer role is the minimum operating control that resists the contract's known operational failure modes.** The direction-signal review surfaced ledger-rollup design (H-09) and paraphrase-only raw observable (CS-08) in practice. The contract's "silent omission is not allowed" rule cannot be self-enforced by the operator who performed the capture. An adversarial reviewer with the explicit refusal-authority charter is the smallest operating-model addition that gives the rule a counterparty.
- **The architecture stays planning-only.** It binds roles, lifecycle, visibility commitments, and stop conditions in product-method language. It does not define obligation-discharge artifact form, log shape, receipt structure, field schema, or runtime. Every deferred implication remains a named pressure, not a design.
- **It carries the baseline non-claims verbatim and adds no new strict claims.** This artifact proposes; it does not validate. Pressure-testing against 3-5 real commissioned captures, per the obligation contract's pressure-test requirement, remains the path to hardening.
- **It refuses fast-reject and stealth-design moves explicitly.** AO-5 is rejected outright. ECR, Cleaning, Judgment, source-family playbook content, source maps, source-system architecture, scoring, training programs, and tool names are listed in the Bloat-Cut Queue below, not designed.

## Core Operating Model

The core operating model commits to nine surfaces. Each surface is conceptual product-method content. None defines artifact form, log shape, receipt structure, schema, or runtime.

### 1. Core invariants (locked now)

These invariants are locked because they are already obligation-contract core and pressure-test evidence is not required to confirm them:

- Commissioned-only scope: no session opens without a Decision Frame entry that names the decision question, owner or owner-context, consequence, cutoff posture (or explicit unknown), and intended downstream use.
- Six discharge states: every core obligation in every commissioned capture must carry exactly one of `met`, `partial`, `blocked`, `unavailable_by_source`, `not_applicable`, or `not_attempted`. `blocked` and `not_attempted` carry a visible reason.
- Silent omission is forbidden. Obligation absence is not an obligation state.
- The seven capture-mode categories from the contract (human-led, agent-assisted, structured access, archive/history, automated extraction, multimodal, mixed) are the operating-model mode vocabulary. Mode disclosure is required at session open. Mid-session mode changes are made visible at the moment of change, not at session close.
- The agent-assistance allow / forbid split is preserved verbatim: agents may enumerate, fetch, archive, transcribe, link, and mechanically group exact URLs or identical locators; agents must not rank relevance, filter candidates before presentation, summarize for admissibility, decide missing context, classify credibility, exclude signals, or decide downstream use.
- Capture's forbidden outputs are preserved verbatim: no credibility labels, integrity classifications, discounting decisions, exclusion decisions, Signal Use Classification, Decision Strength, Action Ceiling, semantic dedupe or clustering effects, Cleaning transformations, ECR field architecture, source-quality scores, source maps as core architecture, or runtime implementation plans.
- Categorical handoff to ECR per Obligation 16 is the only exit. The operating model names the handoff; it does not design ECR.
- Per-slice posture is required (not optional) for Obligations 10 (archive / historical posture), 11 (source visibility and access limits), 12 (related context preservation), and 15 (re-capture semantics) whenever multiple source states or locators coexist. A rollup is allowed only when states are uniform.
- Source-family heuristics remain satellite under the contract's Source-Family Promotion Rule unless a specific invariant is promoted to core through two-non-overlapping-family evidence or specific-invariant owner sign-off.

### 2. Roles (named at category level; no staffing plan)

- **Commissioner.** Establishes the Decision Frame, cutoff posture, downstream-use intent, and source boundary that the session is bound to. May be an Orca decision owner, a project lead, or a downstream consumer. The commissioner does not perform capture and does not certify obligation discharge.
- **Capture operator.** Owns the session inside the boundary the commissioner set. Performs or directs capture; declares mode; records observables and obligation states; cannot self-certify obligation discharge for handoff. Operates the agent-assistance lane within the agent allow/forbid split.
- **Agent assistant (bounded executor).** Performs only the allowed agent verbs. Session must preserve query and session context, result batches, fetched candidates, discarded candidates, and discard-reason categories per the contract. Cannot cross the forbidden-verb line.
- **Adversarial reviewer / second-operator.** Independent verifier at session close. Explicit charter: refuse session close when (a) any obligation is silently omitted; (b) per-slice posture required by the contract is collapsed into a rollup; (c) discharge states have collapsed in operation to "captured / not captured"; (d) raw observable has been paraphrased into a summary that loses domain-native language or modality where modality carries signal; (e) a mode change occurred but was not made visible at the moment of change; (f) agent assistance has crossed a forbidden verb; (g) capture has emitted any forbidden Capture output; (h) discharge-state justification language imports credibility, integrity, discounting, exclusion, Signal Use, Decision Strength, or Action Ceiling language. The reviewer's authority is advisory verification of obligation visibility, not credibility judgment or downstream-use decision.

The role count (three or four operator-side roles plus the commissioner) and exact handoff points between them are kept flexible until pressure-test evidence accumulates. The role set above is the minimum.

### 3. Session lifecycle (state list, not workflow diagram)

A commissioned capture session moves through these states. The names are conceptual; the artifact form of how they are exposed is deferred.

- **Commissioned.** Decision Frame entry recorded; cutoff posture stated or explicitly unknown; downstream-use intent recorded; source boundary recorded.
- **Mode declared.** Initial mode category disclosed; session distinguishable from other sessions; obligation-contract version or equivalent rule surface knowable.
- **Capturing.** Capture work proceeds within the declared mode and within the agent allow/forbid split. Mid-session mode changes are made visible at the moment of change. Raw observable preservation, source identity, decomposed timing, cutoff posture, archive / historical posture (per slice when states differ), source visibility, related context, bundled-offer structure where applicable, and failure / blocker visibility all accrue as the session progresses, not at close.
- **Obligation-discharge declaration.** Every one of the 16 core obligations is declared with exactly one of the six discharge states. Per-slice declarations are made for Obligations 10, 11, 12, and 15 when states differ. `blocked` and `not_attempted` carry visible reasons.
- **Adversarial review.** The reviewer applies the refusal-authority charter above. The reviewer either approves close, requires a fix and re-declaration, or escalates to a stop condition.
- **Categorical handoff exit.** The session exits by handing off categorically to ECR per Obligation 16. What is handed off is named: obligation-discharge declaration, raw observables, per-slice postures where they differ, mode log, agent-session context, and failure visibility. How it is handed off is deferred.

There is no silent close. There is no rollup-only close when slice-level states differ. There is no exit other than categorical handoff or an explicit stop condition.

### 4. Multi-operator continuity

- Any operator change inside a session is treated as a material capture-event provenance event under Obligation 3. The new operator inherits the open obligation-discharge declaration in progress; the declaration is not recreated.
- Session interruption and resume preserve mode disclosure, mid-session mode-change visibility, partial obligation-discharge declarations, and the in-progress raw-observable record.
- Re-capture across sessions preserves the relationship per Obligation 15 — original locator, archive or historical locator, current or migrated locator, fallback path, failed access attempt, changed source state, and supersede / supplement / conflict relationship at the relevant source-slice level. A later capture may supersede the earlier capture for current-state posture while supplementing or conflicting with it for a prior-window or cutoff question; the operating model preserves that mixed relationship.

The mechanism by which continuity is preserved (transport, persistence, storage) is deferred.

### 5. Obligation-discharge visibility commitment

The architecture commits to the property that each commissioned capture exposes a discharge state for every core obligation in a form the reviewer can inspect, including per-slice states where the contract requires them, and that no obligation is silently omitted. The architecture does not specify the artifact form (no "ledger schema," no "obligation field," no "state column," no "discharge receipt"). The form is intentionally deferred to the operator-roster and pressure-test commissioning decision, where it may be a brief operating-model artifact rather than a runtime data shape.

The commitment is the architecture decision. The form is deferred to keep `F-LEAK-ECR`, `F-LEAK-RUNTIME`, and `F-FAKE-SUCCESS-TOOL-POLISH` outside this artifact.

### 6. Capture failure and blocker visibility commitment

Failures, blockers, fallbacks, and not-attempted states are first-class operating-model outputs. The reviewer must refuse close if any failure has been hidden or recorded only as a successful adjacent state. A successful archive or fallback does not erase a failed exact access attempt, failed cache attempt, or non-attempted archive route.

### 7. Source-family satellite boundary

Source-family content (forums / threaded chains, review surfaces, changelogs / docs / pricing / API / policy pages, bundled offers / multi-term proposals, archive / history cases, multimodal / dynamic pages) is satellite guidance. It belongs in a separate, later-authorized satellite registry, not in this architecture. The only source-family invariant currently promoted to core is the archive / history per-slice rule recorded in the baseline decision and the obligation contract.

Satellite guidance can pressure the core through the contract's Source-Family Promotion Rule:

- two non-overlapping source families surface the same operating-model gap, or
- the owner signs off on a specific invariant claim (not a broad category).

Until promotion, satellite guidance informs operator practice; it does not redefine core operating-model law.

### 8. Handoff to ECR (named, not designed)

The architecture commits to a categorical handoff per Obligation 16. The handoff exposes the obligation-discharge declaration, raw observables, per-slice postures where they differ, mode log, agent-session context, and failure visibility. The artifact does not define ECR fields, IDs, keys, tables, data types, receipt structures, storage, schema, or file format. ECR architecture remains a downstream lane whose later authorization may change the categorical handoff exit shape — at which point this artifact would be stale per `stale_if`.

### 9. Version pinning and change-trigger surface

- Every commissioned session is version-bound to the obligation contract version or equivalent rule surface that was in effect at commission time (Obligation 3 — capture-event provenance).
- Every session is version-bound to this operating-model architecture version once owner-accepted.
- Material amendments to the obligation contract, this architecture, or the direction-signal demotion supersede prior session-level binding for sessions commissioned after the amendment date; prior sessions are not retroactively rebound.
- Re-capture across a version change preserves the version pin per Obligation 15.

## Satellite Guidance Boundary

What belongs in source-family satellite guidance, not in this architecture:

- forum and threaded-source playbooks (thread context, related-chain construction, moderator / official response handling);
- review-surface playbooks (rating / text / recency / experience-timing / moderation / incentive / sorting handling);
- changelog / docs / pricing / API / policy playbooks (version / edit / deprecation / future-current / cache / archive / backfill handling);
- bundled-offer / multi-term proposal playbooks (visible packaging cues, dependency framing, sequence preservation);
- archive / history playbooks (when an archive attempt is required versus when posture-only is sufficient);
- multimodal / dynamic-page playbooks (when layout / audio / video / interaction must be captured);
- per-family default mode (e.g., when human-led is the default until operators are trained);
- per-family operator-experience notes.

How satellite guidance pressures the core without silently becoming core:

- A satellite playbook may surface a recurring operating-model gap. The gap is recorded as a re-architecture pressure (see Stop Conditions And Re-Architecture Triggers below); it does not silently rewrite this architecture.
- Promotion to core requires the contract's Source-Family Promotion Rule: cross-family evidence or specific-invariant owner sign-off.
- A promoted invariant is patched into this architecture and the obligation contract as a bounded amendment; satellite content does not become core by accumulation.

## Operating Flow

The capture lifecycle at architecture level. No templates, no fields, no schemas, no implementation steps.

- **Commissioned-frame intake.** The commissioner provides a Decision Frame entry. The capture operator confirms the entry is sufficient to evaluate obligations (decision question; owner or owner-context; consequence; cutoff posture or explicit unknown; downstream-use intent; source boundary). If the frame is insufficient, the session does not open; the commissioner is asked to complete the frame.
- **Capture setup.** The operator declares initial mode; agent-assistance lane (if any) is opened within the allow / forbid split; the session is distinguishable; the obligation-contract version is recorded.
- **Source inspection.** The operator inspects sources within the allowed Orca boundary (public, market-level, non-deceptive, non-intrusive). Boundary-violating material is treated as out-of-bounds, not as a Data Capture blocker to be worked around.
- **Capture-note and observable preservation.** Raw observable is preserved per Obligation 6. Source identity and actor context are preserved per Obligation 7. Decomposed timing is preserved per Obligation 8. Cutoff posture is preserved per Obligation 9. Archive / historical posture is preserved per Obligation 10, per slice where states differ. Source visibility and access limits are preserved per Obligation 11. Related context is preserved per Obligation 12 within the ECR-reconstruction-floor and fairness-ceiling tests. Bundled-offer structure is preserved per Obligation 13 where applicable. Failures and blockers are preserved per Obligation 14.
- **Obligation-state marking.** Every core obligation is marked with one of the six discharge states. Per-slice marks are made where the contract requires them. `blocked` and `not_attempted` carry visible reasons.
- **Interruption and resume.** Continuity rules in Section 4 of Core Operating Model apply. The session is not silently restarted.
- **Adversarial review.** The reviewer applies the refusal-authority charter in Section 2 of Core Operating Model. If the reviewer refuses, the operator either fixes and re-declares, or the session escalates to a stop condition.
- **Categorical handoff.** The session exits by handing off categorically to ECR per Obligation 16. The handoff does not include ECR field definitions, receipt structures, IDs, or storage.

The operating flow is the architecture-level lifecycle. The artifact does not produce a triage flow per obligation, an operator script, or a workflow diagram with concrete tool steps.

## Stop Conditions And Re-Architecture Triggers

### Stop conditions (do not close session; do not hand off)

- Decision Frame is missing or vague enough that capture is free-floating or standing.
- Mode change occurred but was not made visible at the moment of change.
- Per-slice posture required by the contract was collapsed into a rollup.
- Agent assistance crossed a forbidden verb.
- Failure was hidden rather than recorded.
- Boundary-violating material was captured and the operator is working around it rather than treating it as out-of-bounds.
- Any forbidden Capture output appeared (credibility label, integrity classification, discounting decision, exclusion decision, Signal Use Classification, Decision Strength, Action Ceiling, semantic dedupe or clustering effect, Cleaning transformation, ECR field architecture, source-quality score, source map as core architecture, runtime implementation plan).
- Discharge-state justification language imported credibility, integrity, discounting, exclusion, Signal Use, Decision Strength, or Action Ceiling vocabulary.
- Raw observable was replaced by paraphrase or summary that loses domain-native language or modality where modality carries signal.
- Re-capture relationship was not preserved per Obligation 15 across material source slices.

### Re-architecture triggers (open a new architecture lane)

- The obligation contract is materially revised or superseded (also a `stale_if`).
- Pressure-test results from 3-5 real commissioned captures show a recurring obligation that the operating model cannot expose without architectural modification.
- A satellite source-family rule is promoted to core through the Source-Family Promotion Rule, requiring this architecture to add a per-family-invariant commitment.
- An ECR architecture lane is opened and changes the categorical handoff boundary (also a `stale_if`).
- The owner authorizes a future capture mode (for example, automated extraction as a default mode for a specific family) that requires a session-lifecycle change.
- The direction-signal demotion is amended in a way that changes what is accepted as input.
- Repeated occurrences of any stop condition above suggest that the operating-model architecture itself, not just operator practice, needs revision.

Numeric thresholds for re-architecture (how many sessions, how many slice-flatten events, how many continuity drops) are deferred until pressure-test evidence accumulates. The qualitative triggers above are sufficient to open a re-architecture lane in advance of numeric defaults.

## Deferred Implementation Implications

Named only as deferred implications. None is designed in this artifact. Each requires its own bounded authorization before it may be planned, designed, or built.

- Obligation-discharge declaration artifact form (transport, persistence, structure).
- Reviewer-handoff transport between roles.
- Agent-session logging shape that avoids source-log bloat (obligation-contract open knob).
- Multi-operator session-state continuity mechanism (transport and persistence).
- Per-slice locator representation (Obligations 10, 11, 12, 15).
- Re-capture relationship representation (Obligation 15).
- Snapshot Integrity Class placement — open knob in the obligation contract; eventually resolved through an ECR / Capture consolidation decision.
- Recapture threshold defaults — open knob; pressure-test-dependent.
- Mandatory-archive-attempt families — open knob; multi-family pressure-test-dependent.
- Source-family satellite registry — bounded later-authorized decision under the Source-Family Promotion Rule.
- Operator-roster and pressure-test commissioning decision (named as the immediate next authorized step below, but its content is not produced here).
- Operator certification / training curriculum — separate bounded authorization after operator-roster evidence accumulates.
- Buyer-facing visibility surface — separate bounded authorization under the Communication Artifact lane; downstream of memo and evidence appendix.
- Numeric re-architecture-trigger thresholds — pressure-test-dependent.
- Automation of any agent-allowed verb — separate bounded runtime authorization.
- Any tooling, schema, scraper, API, dashboard, storage, package, deployment, commit, push, or PR.

## Bloat-Cut Queue

Attractive expansions that this architecture explicitly does not include, with the boundary each would cross.

- Detailed field schemas, key shapes, IDs, or receipt structures. Crosses ECR / runtime boundary.
- A separate operating-model "data model" or "log shape." Crosses ECR / runtime boundary; introduces tool-shaped polish.
- Source-family playbooks for forums, reviews, changelogs, bundled offers, archive / history, multimodal. Bypasses Source-Family Promotion Rule.
- Runtime tooling references (browser automation, archival services, screenshot systems, API adapters, storage backends). Crosses runtime / tooling boundary.
- ECR field architecture sketches; Cleaning transformations or normalization rules; Judgment rules, credibility labels, discounting, exclusion, Signal Use Classification, Decision Strength, Action Ceiling. All forbidden outputs from Capture.
- Validation execution, proof-run instructions, buyer-proof claims. Bars set by the baseline decision and the Direction Signal decision non-claims.
- Evaluation rubric or scoring of operators or captures. Drifts into credibility / quality / Judgment authority.
- Training program, onboarding curriculum, certification scheme for operators. Separate later-authorized artifact, not architecture.
- Specific tool names, package names, file formats. Runtime / tooling / package boundary.
- Detailed templates or forms. Manual-harness implementation, not architecture; explicitly deferred.
- Automation / workflow diagrams with concrete tool steps. Crosses runtime / automation boundary.
- Detailed "how to triage" instructions for each obligation. Operator-procedure content; not architecture.
- Exhaustive enumeration of every conceivable source family. Invites source-map drift, forbidden by the Direction Signal decision.
- A redesigned manual harness or a patch to the BT2-04 dry run. Explicitly deferred until a bounded patch authorization.
- A re-architecture of ECR / Cleaning / Judgment intake. Reserved layers; forbidden Capture output.

## Non-Claims

This artifact does not claim:

- validation;
- hardening;
- readiness;
- source-of-truth promotion beyond the accepted baseline decision and this architecture's own owner acceptance, if and when granted;
- Data Capture Spine completion;
- harness acceptance, harness patch authority, or final harness shape;
- manual-harness validation, manual-harness patch authority, or template promotion of the manual harness;
- BT2-04 source validity, credibility, admissibility, representativeness, or decision usefulness;
- ECR readiness, ECR design, ECR field architecture, ECR receipt design, or ECR field promotion;
- Cleaning readiness, Cleaning design, normalization design, or transformation-ledger design;
- Judgment readiness, Judgment design, credibility labels, integrity classifications, discounting, exclusion, Signal Use Classification, Decision Strength, or Action Ceiling readiness;
- buyer validation, willingness-to-pay proof, repeatability proof, product readiness, feature readiness, implementation readiness, or commercial readiness;
- runtime feasibility, runtime authorization, tooling authorization, scraper authorization, API authorization, dashboard authorization, archival-tool authorization, storage authorization, automation authorization, schema authorization, test authorization, package authorization, deployment authorization, commit, push, or PR authorization;
- source rights or data-rights sufficiency;
- source-system architecture or source maps;
- pressure-test discharge against 3-5 real commissioned captures;
- supersession of the v0 sibling artifact (v1 is a parallel proposal at higher evidence quality; the owner determines the relationship).

Subagent agreement, model agreement, perspective consensus, fixture count, and lack of P0/P1 findings are not treated as validation or acceptance.

## Next Authorized Step

The smallest complete next authorized step is for the owner to choose one of the following bounded, docs-only actions:

- **Routing decision between v0 and v1.** Compare this v1 proposal with the v0 proposal at `docs/product/data_capture_harness_operating_model_architecture_v0.md`. Accept, patch, reject, or hybridize either or both. Acceptance moves the chosen proposal from `PROPOSED_ARCHITECTURE_V0` to an owner-accepted status; until then both remain proposed.
- **Bounded operator-roster and pressure-test commissioning decision.** Once an architecture is owner-accepted, name the 3-5 real commissioned captures to run against the accepted obligation baseline plus the accepted operating-model commitments (per the obligation contract's pressure-test requirement and the contract's recommended pressure-test source mix); name the operators at category level (commissioner, capture operator, agent-assistance lane if any, adversarial reviewer); define how each capture's per-obligation discharge declaration is exposed for review (the artifact form deferred by the accepted architecture is decided at this commissioning step, not earlier); define version pinning for the obligation contract and the accepted architecture against each commissioned session; preserve all non-claims above.
- **Separately authorized read-only adversarial artifact review.** Commission an Orca read-only adversarial review of this v1 proposal (and / or the v0 proposal) before any acceptance decision.

The owner action is docs-only and planning-only. It does not authorize ECR, Cleaning, Judgment, runtime, tooling, source-system, scraper, API, dashboard, archival-tool, storage, schema, test, package, deployment, commit, push, PR, satellite source-family registry creation, training curriculum, buyer-facing appendix work, or any forbidden Capture output. Each of those needs its own bounded authorization in a later turn.
