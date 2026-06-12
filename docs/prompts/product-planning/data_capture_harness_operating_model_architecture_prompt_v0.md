# Data Capture Harness Operating Model Architecture Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Prompt for producing a bounded Data Capture Harness operating-model architecture artifact against the accepted Data Capture obligation baseline.
use_when:
  - Launching the Data Capture Harness operating-model architecture lane.
  - Ensuring harness architecture plans against the accepted obligation baseline without drifting into runtime, ECR, Cleaning, Judgment, source maps, or implementation.
  - Preserving the manual harness plus BT2-04 dry run as direction-signal evidence only.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/data_capture_obligation_baseline_decision_v0.md
  - docs/product/data_capture_spine/data_capture_harness_product_goal_direction_signal_decision_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - .agents/workflow-overlay/prompt-orchestration.md
stale_if:
  - The accepted Data Capture obligation-baseline decision is amended, rejected, or superseded.
  - The Data Capture obligation contract is materially revised or superseded.
  - The Data Capture Harness Direction Signal decision is superseded.
  - A later operating-model architecture prompt supersedes this prompt.
```

- Prompt target: agent-enabled Claude Opus or another source-grounded
  architecture-planning lane; plain-model fallback is allowed only when the
  launch instruction explicitly says `plain_model_fallback: authorized`.
- Template basis: Orca `generic-claude-opus` prompting scaffold plus Orca prompt-orchestration rules.
- Output mode: `file-write`.
- Downstream target artifact: `docs/product/data_capture_harness_operating_model_architecture_v0.md`.
- Prompt artifact path: `docs/prompts/product-planning/data_capture_harness_operating_model_architecture_prompt_v0.md`.
- Created: 2026-05-28.
- Implementation authorized: no.
- Runtime/source-system design authorized: no.
- ECR/Cleaning/Judgment design authorized: no.
- Harness patching authorized: no.
- Architecture subagents authorized: yes, exactly three advisory architecture
  perspective subagents: directional, adversarial, and grounding.
- Plain-model fallback: authorized only by explicit launch instruction; must
  disclose `Subagents launched: none` and use local directional, adversarial,
  and grounding passes without claiming delegated evidence.
- Source-of-truth promotion claimed: no.

## Cartographer Route Encoded

Boundary: Route map and prompt only. No architecture execution, validation,
patching, implementation route, runtime design, or readiness claim.

Goal: Produce a bounded Data Capture Harness operating-model architecture that
explains how the accepted capture obligations are exercised reliably across
operators, sessions, agents, and source families.

Starting Point: `ACCEPTED_BASELINE_DECISION_V0` is now recorded in
`docs/product/data_capture_obligation_baseline_decision_v0.md`; the manual
harness plus BT2-04 dry run is accepted only as `Data Capture Harness Direction
Signal v0`; no accepted harness operating-model architecture artifact exists.

Route Shape: Move from accepted obligation baseline to operating-model
architecture by pinning the contract, defining roles and session flow, mapping
obligation-discharge surfaces, separating core from satellite guidance, naming
stop/re-architecture triggers, and preserving all non-implementation
boundaries.

Checkpoints:

- Baseline pin: the architecture is version-bound to the accepted obligation
  baseline and carries its non-claims.
- Operating-model frame: the architecture answers how capture work is operated,
  reviewed, resumed, handed off, and stopped, not how software is built.
- Role and session model: human, agent-assisted, reviewer, and multi-operator
  responsibilities are separated without turning into org design or tooling.
- Obligation-discharge flow: each capture obligation can become visible as
  met, partial, blocked, unavailable, not applicable, or not attempted without
  silent omission.
- Core/satellite boundary: source-family guidance adapts the operating model
  but does not become core law unless an accepted future decision promotes it.

Forks / Handoff Signals:

- If the accepted baseline is stale or unavailable, block architecture
  selection and name the source gap.
- If the work requires runtime, source-system, scraper, API, dashboard,
  storage, automation, schema, package, or test design, stop and require
  separate implementation authority.
- If ECR, Cleaning, Judgment, Decision Strength, or Action Ceiling design is
  needed to proceed, stop and name the downstream-lane dependency instead of
  designing it.
- If source-family mechanics dominate the core architecture, move them to a
  satellite/reference-layer boundary.
- If the target architecture cannot preserve obligation discharge, failure
  visibility, and layer discipline, return no target selection.

## Goal Handoff

```yaml
goal_handoff:
  long_term_goal: "Build a Data Capture Harness that operationalizes Orca's accepted capture obligations into repeatable, buyer-trustworthy commissioned capture across operators, sessions, agents, and source families."
  anchor_goal: "Establish the operating-model architecture goal for the harness: define how the accepted obligation baseline is exercised in practice without turning the harness into runtime tooling, ECR, Cleaning, Judgment, source maps, or a one-off manual checklist."
  success_signal: "A later architecture artifact can clearly answer who does what, in what sequence, with what handoffs, failure states, role boundaries, version pins, and stop conditions while preserving the accepted obligation baseline and all non-claims."
  status: user_stated
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  output_fit_check: goal_handoff.success_signal
  target_delta_from_prior:
    status: prior_target_not_supplied
    changed_fields: []
    summary: "No prior thread operating target was supplied for the operating-model architecture lane."
  drift_guard: "Do not substitute runtime/tooling design, ECR/Cleaning/Judgment design, or manual-harness patching for the operating-model architecture goal."
  conflict_behavior: call_out_conflict_before_proceeding
```

## Paste-Ready Prompt

```text
<role>
You are Claude Opus working for Orca as a product-method architecture planner.
Your task is to create a bounded Data Capture Harness operating-model
architecture artifact against Orca's accepted Data Capture obligation baseline.
</role>

<operating_mode>
Reason carefully from the provided Orca sources. Return source-grounded
architecture conclusions, decisive rationale, assumptions, source gaps, and
non-claims.

Do not expose private chain-of-thought. If reasoning is complex, summarize the
decision logic and the evidence that drove it.

This is architecture planning for an operating model. It is not implementation
planning, not runtime/tooling design, not ECR design, not Cleaning design, not
Judgment design, and not harness patch execution.
</operating_mode>

<orca_authority>
Use the Orca source hierarchy:
1. Current launch instruction for this prompt.
2. Orca `AGENTS.md`.
3. Orca overlay under `.agents/workflow-overlay/`.
4. Orca docs under `docs/`, when they do not conflict with the overlay.
5. Reusable workflow methods only for generic mechanics, not Orca facts.

Do not import `jb` rules, paths, lifecycle mechanics, product policy,
validation habits, model lanes, review labels, handoff rules, or artifact roles
as Orca authority.
</orca_authority>

<goal_context>
goal_handoff:
  long_term_goal: "Build a Data Capture Harness that operationalizes Orca's accepted capture obligations into repeatable, buyer-trustworthy commissioned capture across operators, sessions, agents, and source families."
  anchor_goal: "Establish the operating-model architecture goal for the harness: define how the accepted obligation baseline is exercised in practice without turning the harness into runtime tooling, ECR, Cleaning, Judgment, source maps, or a one-off manual checklist."
  success_signal: "A later architecture artifact can clearly answer who does what, in what sequence, with what handoffs, failure states, role boundaries, version pins, and stop conditions while preserving the accepted obligation baseline and all non-claims."
  status: user_stated

thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
  if_changed_reason:
</goal_context>

<cartographer_route>
Boundary: route map and architecture prompt only. No architecture execution,
validation, patching, implementation route, runtime design, or readiness claim.

Goal: produce a bounded Data Capture Harness operating-model architecture that
explains how the accepted capture obligations are exercised reliably across
operators, sessions, agents, and source families.

Starting point: `ACCEPTED_BASELINE_DECISION_V0` is recorded in
`docs/product/data_capture_obligation_baseline_decision_v0.md`; the manual
harness plus BT2-04 dry run is accepted only as `Data Capture Harness Direction
Signal v0`; no accepted harness operating-model architecture artifact exists.

Route shape: move from accepted obligation baseline to operating-model
architecture by pinning the contract, defining roles and session flow, mapping
obligation-discharge surfaces, separating core from satellite guidance, naming
stop/re-architecture triggers, and preserving all non-implementation
boundaries.

Checkpoints:
- baseline pin;
- operating-model frame;
- role and session model;
- obligation-discharge flow;
- core/satellite boundary.

Forks / handoff signals:
- stale or unavailable baseline blocks architecture selection;
- runtime/tooling need requires separate implementation authority;
- ECR/Cleaning/Judgment need must be named as downstream dependency, not
  designed;
- source-family mechanics that dominate core must move to satellite boundary;
- inability to preserve obligation discharge, failure visibility, and layer
  discipline means no target architecture should be selected.
</cartographer_route>

<repo_preflight>
Before source analysis, record an `orca_start_preflight` receipt:

orca_start_preflight:
  agents_read: yes/no
  overlay_read: yes/no
  source_pack: custom S3 bounded Data Capture Harness operating-model architecture pack
  edit_permission: docs-write for the target product artifact only
  target_scope:
    - docs/product/data_capture_harness_operating_model_architecture_v0.md
  dirty_state_checked: yes/no
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/data_capture_obligation_baseline_decision_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md

If `docs/product/data_capture_harness_operating_model_architecture_v0.md`
already exists, read it first and do not silently overwrite it. Either update
only with explicit owner authorization or create the next versioned filename
and report the collision.
</repo_preflight>

<required_method_sequence>
1. REFERENCE-LOAD `workflow-deep-thinking`.
2. REFERENCE-LOAD `workflow-architecture-planning`.
3. Do not APPLY either method yet. Before source readiness, use them only to
   prepare neutral source-reading questions.
4. SOURCE-LOAD the required Orca sources below.
5. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
6. Only after source readiness, APPLY `workflow-deep-thinking` to frame the
   real architecture question, failure modes, and decision criteria.
7. Then APPLY `workflow-architecture-planning` in standard profile. Use exactly
   one evidence mode:

   Evidence mode A - `delegated_three_subagents`:
   Launch exactly three advisory architecture perspective subagents:
   - Directional lane: make the strongest source-backed case for the most
     promising target operating-model architecture.
   - Adversarial lane: make the strongest case against that target, including
     coupling, boundary leakage, hidden assumptions, fake-success paths, and
     premature runtime or implementation gravity.
   - Grounding lane: keep the architecture repo-native, source-bounded,
     anti-bloat, reversible where possible, and planning-only; identify what
     to cut or defer.

   Evidence mode B - `plain_model_local_fallback`:
   Use this mode only if the current launch instruction explicitly says
   `plain_model_fallback: authorized`. In this mode, do not claim subagents
   were launched. Run three separately labeled local passes inside the main
   model context: directional, adversarial, and grounding. The artifact and
   closeout must state:
   - `Subagents launched: none`
   - `Evidence mode: local directional/adversarial/grounding passes`
   - `Evidence caveat: lower independence than delegated subagents`

Subagent requirement:
- Three subagents are explicitly authorized and required for this
  architecture-planning run when `delegated_three_subagents` mode is available.
- Use inherited/default agent type, model, role, and reasoning effort unless
  the host explicitly supports safe overrides.
- Do not combine full-history or full-context forks with agent/model/reasoning
  overrides unless the host explicitly supports that combination.
- Each subagent must receive the same required source pack, or a bounded source
  capsule that names every included and excluded source, and must declare
  `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before producing
  advisory input.
- Each subagent output must state its evidence coverage, source gaps, advisory
  boundary, and any blocker that would change the main synthesis.
- Each subagent is advisory input only, not a verdict, not implementation
  authority, and not proof of readiness.
- The main planner owns synthesis and must not treat subagent agreement as
  proof.
- If subagent tooling is unavailable, rejected, or blocked, return
  `BLOCKED_SUBAGENT_UNAVAILABLE` or the nearest strict blocker instead of
  silently substituting local perspectives, unless the current launch
  instruction explicitly says `plain_model_fallback: authorized`.

Local-fallback requirement:
- If `plain_model_fallback: authorized` is present, local fallback is allowed
  only as an evidence-mode downgrade, not as a substitute claim that subagents
  were launched.
- Local fallback must use the same source-readiness gate as the main planner
  and must use the source capsule below when full source loading would exceed
  the source-loading budget.
- If local fallback is used, the target architecture may still be emitted, but
  the artifact must mark delegated subagent independence as `not proven`.

If the receiving environment cannot apply a named method, report
`SOURCE_CONTEXT_INCOMPLETE` or the nearest blocked/advisory-only result and do
not emit strict architecture claims.
</required_method_sequence>

<subagent_or_local_source_capsule>
Use this capsule for each delegated subagent or local fallback pass when the
lane cannot safely load the full source set. The capsule is a bounded decision
aid, not a substitute source-of-truth promotion.

source_capsule:
  task_objective: "Advise on Data Capture Harness operating-model architecture without executing architecture synthesis."
  source_pack_name: "Data Capture Harness operating-model architecture capsule"
  included_sources:
    - `docs/product/data_capture_obligation_baseline_decision_v0.md`
    - `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
    - `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md`
    - `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
  authority_capsule:
    - Orca `AGENTS.md` and `.agents/workflow-overlay/README.md` control project authority.
    - Orca overlay wins over reusable workflow mechanics for Orca facts.
    - Do not import `jb` policy or generic lifecycle rules.
    - No implementation, runtime, ECR, Cleaning, Judgment, validation,
      readiness, buyer-proof, source-system, scraper, API, dashboard, storage,
      package, deployment, commit, push, or PR work is authorized.
  decisive_context:
    - Baseline decision is accepted for architecture planning but does not
      claim hardening, validation, product readiness, implementation readiness,
      tooling authorization, commercial readiness, or buyer proof.
    - The obligation contract is the controlling source for what capture must
      discharge.
    - The manual harness plus BT2-04 dry run is direction-signal evidence only,
      not controlling architecture.
    - Capture records visible facts, limits, blockers, source identity where
      knowable, timing/cutoff posture, raw observable/source-language evidence,
      and failure states. It must not perform ECR, Cleaning, Judgment,
      credibility, discounting, exclusion, Signal Use, Decision Strength, or
      Action Ceiling.
    - Source-family mechanics are satellite guidance unless a later accepted
      decision promotes a source-family invariant into core.
  excluded_by_default:
    - `docs/_inbox/`
    - method-validation replays
    - proof-run packets
    - all review outputs except when a specific review finding changes a
      decision
    - all product files outside the included capsule unless a source gap would
      change the recommendation
  subagent_output_required:
    - evidence coverage used: full source pack or this capsule
    - source gaps that could change the advice
    - advisory-only boundary statement
    - recommendation to the main planner, not a verdict
</subagent_or_local_source_capsule>

<required_source_loading>
If you have filesystem access, read these sources before answering. If you do
not have filesystem access, return `SOURCE_CONTEXT_INCOMPLETE` and ask for the
smallest source capsule needed. Do not substitute generic architecture
intuition for Orca source grounding.

Core read pack before architecture synthesis:
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `docs/product/data_capture_obligation_baseline_decision_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md`
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`

For long core sources, read the retrieval header and decision-bearing sections
first. Full-file reads are allowed only when a targeted read leaves a concrete
source gap that could change the target architecture.

Conditional expansion only if a concrete source gap could change the target
architecture, source authority, or output boundary:
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/product-proof.md`
- `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`
- `docs/product/core_spine_v0_product_contract.md`
- `docs/product/core_spine_v0_information_production_foundation_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_pressure_test_synthesis_usage_note_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/data_capture_obligation_baseline_decision_adversarial_artifact_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_manual_harness_bt204_dry_run_adversarial_review_v0.md`
- `docs/product/orca_offer_hypothesis_v0.md`
- `docs/product/orca_buyer_proof_packet_v0.md`
- `docs/decisions/turn_08_product_thesis_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_full_fixture_synthesis_adversarial_review_v0.md`

When expanding, read targeted sections first. Do not convert the conditional
expansion list into a read-all list. If source loading would dominate the
architecture work, use the source capsule above or return
`SOURCE_CONTEXT_INCOMPLETE` with the missing claim-specific source.

Default exclusions:
- Do not read `docs/_inbox/`.
- Do not bulk-load all product, prompt, review, research, workflow, proof-run,
  or method-validation replay files.
- Do not read implementation folders or create implementation scope.
- Do not widen into source-system, scraper, API, dashboard, storage,
  automation, schema, test, package, deployment, commit, push, or PR work.
</required_source_loading>

<source_readiness_gate>
Before producing the architecture artifact, declare one of:
- `SOURCE_CONTEXT_READY`
- `SOURCE_CONTEXT_INCOMPLETE`

If ready, include a compact source-read ledger: source, why read, and what
architecture claim or boundary it supports.

If incomplete, name missing sources, what architecture claims cannot be made,
and the smallest complete source capsule needed. Do not write the target
artifact if missing sources could change the target architecture.
</source_readiness_gate>

<architecture_question>
What is the target operating-model architecture for Orca's Data Capture
Harness, now that the Data Capture obligation baseline is accepted?

The architecture must define how the harness is operated across commissioned
captures: roles, session lifecycle, agent assistance boundaries, multi-operator
continuity, obligation-discharge visibility, capture failure visibility,
source-family satellite guidance, handoff boundaries, stop conditions, and
re-architecture triggers.
</architecture_question>

<options_to_consider>
Treat these as candidates, not defaults. Add, merge, or reject options only
when the loaded sources justify it. Fast-reject options that violate the hard
boundaries without detailed runtime, ECR, Cleaning, Judgment, or implementation
design.

- AO-1: Single-operator manual checklist. A lean manual playbook around the
  accepted obligations.
- AO-2: Contract-pinned operating envelope. A core operating model with role,
  session, obligation-state, handoff, and stop-condition boundaries; source
  family guidance stays satellite.
- AO-3: Source-family playbook core. Make source-family mechanics the primary
  harness architecture.
- AO-4: Review/audit-first harness. Make reviewer inspection and audit flow the
  primary architecture, with capture operations subordinate.
- AO-5: Runtime/tooling-first harness. Treat this as a fast-reject boundary
  test under the current commission; do not analyze runtime, storage, scraping,
  screenshots, archives, or automation as an architecture design.
- AO-6: No target selected yet. Defer architecture if source gaps or owner
  decisions still make the target unsafe.
</options_to_consider>

<decision_criteria>
Select or reject target architecture options using these criteria:

- The architecture exercises the accepted obligation baseline without mutating
  it.
- It makes commissioned capture repeatable across operators, sessions, and
  agent assistance.
- It preserves layer discipline: Capture records visible facts, limits,
  blockers, and context; it does not perform ECR, Cleaning, Judgment, Signal
  Use, Decision Strength, or Action Ceiling.
- It makes failure states visible, including blocked, unavailable,
  not-attempted, degraded, fallback, post-window, archive-limited, and
  source-limited states.
- It preserves raw observable and source-language obligations without turning
  the architecture into a schema or data model.
- It keeps source-family mechanics satellite unless an accepted future decision
  promotes a source-family invariant.
- It uses the demoted manual harness / BT2-04 dry run as direction signal only,
  not architecture control.
- It avoids fake success from source volume, checklist completion, review
  theater, or tool-shaped polish.
- It stays future-runtime-aware only as deferred implications, not runtime
  authorization.
</decision_criteria>

<hard_boundaries>
Do not:
- patch the obligation contract;
- patch the manual harness or BT2-04 dry run;
- design ECR fields, schemas, keys, records, tables, or storage;
- design Cleaning transformations;
- design Judgment rules, credibility labels, discounting, exclusion, Signal
  Use Classification, Decision Strength, or Action Ceiling;
- design source systems, source maps, scrapers, APIs, dashboards, archives,
  browser automation, screenshot systems, storage, schemas, tests, packages,
  runtime services, deployment, commits, pushes, or PRs;
- claim validation, hardening, readiness, buyer proof, commercial proof,
  feature readiness, implementation readiness, source-of-truth promotion beyond
  the accepted baseline decision, or tooling authorization;
- treat the manual harness / BT2-04 direction signal as controlling
  architecture;
- turn operating-model architecture into a one-off checklist or source-family
  playbook.
</hard_boundaries>

<target_artifact_contract>
Write a Markdown artifact at:

`docs/product/data_capture_harness_operating_model_architecture_v0.md`

The artifact must include:

1. Title
   - `# Data Capture Harness Operating Model Architecture v0`

2. Retrieval Header
   - Use the Orca retrieval header shape.
   - `artifact_role: Product artifact`
   - `authority_boundary: retrieval_only`
   - Include `open_next` only for genuinely useful controlling sources.

3. Status
   - Use `PROPOSED_ARCHITECTURE_V0` unless the current launch instruction
     explicitly says the owner is accepting the architecture.
   - Do not claim validation, readiness, hardening, implementation authority,
     or source-of-truth promotion.

4. Source Readiness
   - `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
   - Preflight receipt.
   - Compact source ledger.
   - Architecture-planning evidence mode:
     `delegated_three_subagents`, `plain_model_local_fallback`, or blocked.
   - If `delegated_three_subagents`: subagent source-readiness receipts for all
     three lanes, including whether each used the full source pack or the
     bounded source capsule.
   - If `plain_model_local_fallback`: state `Subagents launched: none`,
     identify the three local passes, name the source coverage, and mark
     delegated subagent independence as `not proven`.
   - If any required subagent cannot be launched and
     `plain_model_fallback: authorized` is absent, record the blocker and do
     not emit a target architecture.
   - Dirty/untracked caveats.

5. Architecture Frame
   - Real architecture question.
   - Starting point.
   - Target operators and downstream consumers.
   - Explicit non-targets.

6. Cartographer Route Influence
   - Summarize in 2-4 bullets how the cartographer route shaped the actual
     architecture decision.
   - Do not restate the route field-for-field.

7. Questions This Architecture Must Answer
   - Role model.
   - Session lifecycle.
   - Multi-operator continuity.
   - Human/agent assistance boundaries.
   - Obligation-discharge visibility.
   - Source-family satellite boundary.
   - Handoff to downstream ECR without designing ECR.
   - Stop conditions and re-architecture triggers.

8. Options Compared
   - Compare materially different options, including the candidates above when
     still relevant.
   - Include why each may win, why it may lose, and fake-success risk.

9. Target Architecture
   - Return exactly one architecture result:
     - `TARGET_RECOMMENDED`
     - `OPTIONS_COMPARED_NO_SELECTION`
     - `NEEDS_ARCHITECTURE_QUESTION`
     - `NEEDS_PRODUCT_DECISION`
     - `NEEDS_SOURCE_CONTEXT`
     - `DEFER_OR_REJECT`
     - `AUTHORITY_BLOCKED`
   - If `TARGET_RECOMMENDED`, name the target architecture and why it wins.

10. Core Operating Model
   - Define core responsibilities, invariants, and boundaries.
   - Include roles, sessions, obligation states, capture surfaces, review
     points, handoff points, stop conditions, version pinning, and change
     triggers.
   - Keep this conceptual and product-method oriented, not schema or runtime
     design.

11. Satellite Guidance Boundary
   - Define what belongs in source-family satellite guidance.
   - State how satellite guidance can pressure the core without silently
     becoming core.

12. Operating Flow
   - Describe the capture lifecycle at architecture level:
     commissioned frame intake, capture setup, source inspection, capture
     note/observable preservation, obligation-state marking, interruption and
     resume, review/second-operator check, and downstream handoff.
   - Do not create templates, fields, schemas, or implementation steps.

13. Stop Conditions And Re-Architecture Triggers
   - Name when to stop, block, rerun, patch, escalate, or re-architecture.

14. Deferred Implementation Implications
   - Name future implementation implications only as non-executable notes.
   - Keep runtime/tooling/source-system implications deferred.

15. Bloat-Cut Queue
   - List attractive but rejected scope expansions.

16. Non-Claims
   - Explicitly preserve the non-claims from the accepted baseline decision.

17. Next Authorized Step
   - Name the smallest complete next action after this artifact.
   - Do not authorize implementation, runtime, ECR, Cleaning, or Judgment work.
</target_artifact_contract>

<chat_closeout_contract>
After writing the artifact, return a compact human summary plus artifact
receipt:

- artifact path;
- architecture result;
- target architecture name if selected;
- evidence-mode receipt:
  `delegated_three_subagents`, `plain_model_local_fallback`, or blocked;
- subagent/local-perspective receipt for directional, adversarial, and
  grounding lanes, including launch status, source-readiness status, and
  evidence coverage;
- blocking or advisory gaps;
- next authorized step;
- reminder that no implementation/runtime/ECR/Cleaning/Judgment work was
  performed or authorized.

Do not stage, commit, push, or open a PR unless separately instructed.
</chat_closeout_contract>

<self_check>
Before finalizing, check the artifact against these failure modes:

- treating the operating model as a runtime/tooling architecture;
- designing ECR, Cleaning, Judgment, source maps, storage, schemas, or
  automation;
- turning the demoted manual harness into controlling architecture;
- making source-family mechanics core without accepted promotion;
- hiding blocked, unavailable, not-attempted, fallback, partial, or degraded
  capture states;
- losing raw observable/source-language preservation;
- claiming validation, hardening, readiness, buyer proof, commercial proof, or
  implementation authority;
- selecting a target without a stable invariant, core/satellite split, known
  non-goals, and no unresolved upstream blocker;
- claiming standard three-subagent evidence when the directional, adversarial,
  and grounding subagents were not actually launched;
- claiming `delegated_three_subagents` evidence when local fallback was used;
- omitting the lower-independence caveat for `plain_model_local_fallback`;
- producing a generic operating model that does not pin to the accepted
  obligation baseline.
</self_check>
```
