# Cleaning Spine Foundation Architecture Planning Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: >
  Source-gated /architecture-planning prompt for final architecture reading of
  the Cleaning Spine foundation draft, with workflow-goal-framing context and
  three standard advisory subagent perspectives.
use_when:
  - Running the final architecture reading of the Cleaning Spine foundation draft.
  - Rechecking whether the Cleaning Spine foundation preserves Data Capture / ECR / Cleaning / Judgment boundaries.
  - Commissioning directional, adversarial, and grounding architecture perspectives before owner reading.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  - orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/projection_doctrine_v0_vendor_ca_closeout_v0.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - orca/product/spines/cleaning/contracts/core_spine_v0_corroboration_vs_amplification_discipline_v0.md
  - orca/product/spines/capture/core/operating_model/core_spine_v0_data_capture_context_preservation_note_v0.md
stale_if:
  - The Cleaning Spine foundation target path changes.
  - Projection Doctrine v0 is amended, superseded, ratified differently, or rejected.
  - Owner changes the installed 2026-06-16 OD-1, OD-4, or OD-7 direction before this prompt is run.
```

## Prompt Metadata

```yaml
prompt_artifact_path: docs/prompts/handoffs/cleaning_spine_foundation_architecture_planning_prompt_v0.md
template_kind: handoff
template_source: workflow-prompt-orchestrator mechanics plus Orca overlay; no project-local architecture template exists.
output_mode: file-write for this prompt artifact; receiver output mode is chat-only.
receiver_edit_permission: read-only
authorization_basis: owner requested a /architecture-planning prompt with three standard subagents authorized, plus workflow-goal-framing for Cleaning Spine.
workspace_path: C:\Users\vmon7\Desktop\projects\orca\orca-worktrees\projection-reddit-enforcement
expected_branch_or_source: codex/cleaning-spine-projection-handoff
dirty_state_allowance: >
  Read-only intake may allow the untracked Cleaning Spine foundation artifact
  and this prompt artifact if present. No unrelated dirty state is in scope.
preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated here.
source_pack: custom_cleaning_spine_architecture_final_reading
repo_map_decision: not_needed
repo_map_reason: >
  The target artifact and this prompt sit under already map-covered folders;
  architecture reading does not choose a new artifact location.
doctrine_change_decision: >
  Receiver is read-only and must not change doctrine. The target may recommend
  a minimal docs patch as a next routing object, but must not apply it.
isolation_decision: neither_for_receiver_read_only
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: yes
  lifecycle_status: new_thread_local_goal_frame_embedded_below
  if_changed_reason: >
    This prompt establishes a Cleaning Spine goal frame for the architecture
    reading rather than carrying a prior active thread target.
```

## Receiver Prompt

You are the home architecture planner for the Orca Cleaning Spine foundation
reading.

Run `/architecture-planning` in **standard** profile with **three advisory
subagents authorized**: directional, adversarial, and grounding. You will review
and adjudicate their returns. You must not treat any subagent output as a
verdict, validation, readiness, owner ratification, or implementation authority.

This prompt explicitly authorizes continuing from goal framing into architecture
planning. The goal frame is context for the architecture question, not a route,
validation gate, or source authority.

### Goal Establishing

Long-term goal: Give Orca a durable Cleaning Spine foundation that can turn raw,
projected, and Evidence Candidate Record material into smaller Judgment-usable
working views without losing raw evidence, flattening source context, or
smuggling interpretation into Cleaning.

Anchor goal: Produce a final architecture reading of
`docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md` that
decides whether the draft is architecturally fit for owner reading as a
foundation draft, and if not, names the smallest complete caveat or patch needed
before that owner reading.

Success signal:

- Core success:
  - Owner-observable: The owner receives one clear architecture result:
    `TARGET_RECOMMENDED`, `OPTIONS_COMPARED_NO_SELECTION`,
    `NEEDS_SOURCE_CONTEXT`, `DEFER_OR_REJECT`, or `AUTHORITY_BLOCKED`, with
    line-cited reasons.
  - Output fit: The final reading makes clear whether the foundation preserves
    Data Capture / ECR / Cleaning / Judgment boundaries, keeps Projection
    Doctrine candidate status visible, avoids runtime schema or object-model
    ratification, applies installed OD-1 / OD-4 / OD-7 direction, and names only the
    smallest necessary next routing object.
  - Boundary: Success is not artifact completion, subagent count, validation,
    readiness, implementation, owner ratification, proof-run authority, or
    accepting Projection Doctrine v0 as ratified.
  - Drift cue: The work has drifted if it turns into implementation scoping,
    schema design, source capture, proof execution, broad product planning,
    Judgment review, or a claim that Cleaning can decide credibility,
    independence, salience, Signal Integrity, Signal Use, Decision Strength, or
    Action Ceiling.
- Secondary success signals:
  - The final reading explicitly separates required pre-owner-reading patch
    from optional hardening.
  - Any invalid subagent return is rejected or rerun rather than counted.
  - Any recommended patch is small, source-backed, and does not broaden the
    foundation beyond the handoff.

Open question: Whether the target is clean enough for owner reading as a
foundation draft, or whether a tiny caveat patch is needed first to keep
candidate/non-schema boundaries adjacent to strict ledger and traceability
language.

```yaml
goal_handoff:
  long_term_goal: >
    Give Orca a durable Cleaning Spine foundation that can turn raw, projected,
    and Evidence Candidate Record material into smaller Judgment-usable working
    views without losing raw evidence, flattening source context, or smuggling
    interpretation into Cleaning.
  anchor_goal: >
    Produce a final architecture reading of
    docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md that
    decides whether the draft is architecturally fit for owner reading as a
    foundation draft, and if not, names the smallest complete caveat or patch
    needed before that owner reading.
  success_signal:
    core_success:
      owner_observable: >
        The owner receives one clear architecture result with line-cited reasons.
      output_fit: >
        The final reading makes clear whether the foundation preserves layer
        boundaries, keeps Projection Doctrine candidate status visible, avoids
        runtime schema or object-model ratification, applies installed OD-1 /
        OD-4 / OD-7 direction, and names only the smallest necessary next
        routing object.
      boundary: >
        Success is not artifact completion, subagent count, validation,
        readiness, implementation, owner ratification, proof-run authority, or
        accepting Projection Doctrine v0 as ratified.
      drift_cue: >
        Drift occurs if the work becomes implementation scoping, schema design,
        source capture, proof execution, broad product planning, Judgment review,
        or a claim that Cleaning can decide Judgment-owned effects.
    secondary_success_signals:
      - Required pre-owner-reading patch is separated from optional hardening.
      - Invalid subagent returns are rejected or rerun rather than counted.
      - Any recommended patch is small, source-backed, and non-broadening.
  status: inferred_thread_local
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  output_fit_check: goal_handoff.success_signal.core_success.output_fit
  target_delta_from_prior:
    status: prior_target_not_supplied
    changed_fields: []
    summary: new Cleaning Spine architecture-reading target for this prompt
  drift_guard: >
    Do not substitute implementation/schema/proof work or generic artifact
    completion for a source-cited architecture reading of the Cleaning Spine
    foundation.
  conflict_behavior: call_out_conflict_before_proceeding
```

## Source-Gated Method Sequence

Follow this order exactly.

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. REFERENCE-LOAD, but do not yet APPLY, these method and overlay sources:
   - `.agents/workflow-overlay/decision-routing.md`
   - `.agents/workflow-overlay/source-loading.md`
   - `.agents/workflow-overlay/prompt-orchestration.md`
   - `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.80\skills\workflow-goal-framing\SKILL.md`
   - `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.80\skills\workflow-architecture-planning\SKILL.md`
3. Run the Orca Cynefin Routing Layer before planning or delegation. You must
   name:
   - smallest complete outcome;
   - regime;
   - current bottleneck;
   - riskiest assumption;
   - stop or pivot condition;
   - allowed next move;
   - disallowed next move.
4. SOURCE-LOAD the task sources:
   - `docs/product/core_spine/core_spine_v0_cleaning_spine_foundation_v0.md`
   - `docs/product/core_spine_v0_projection_doctrine_v0.md`
   - `docs/review-outputs/adversarial-artifact-reviews/projection_doctrine_v0_vendor_ca_closeout_v0.md`
   - `docs/product/core_spine/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
   - `docs/product/core_spine/core_spine_v0_corroboration_vs_amplification_discipline_v0.md`
   - `docs/product/data_capture_spine/core_spine_v0_data_capture_context_preservation_note_v0.md`
5. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
6. If source context is incomplete, stop with `NEEDS_SOURCE_CONTEXT` unless the
   missing source is clearly non-decisive and you label that boundary.
7. After `SOURCE_CONTEXT_READY`, APPLY workflow-goal-framing only to confirm
   whether the embedded goal frame is coherent. Do not mutate the owner goal.
8. After goal-frame confirmation, APPLY workflow-architecture-planning standard
   profile.

## Subagent Authorization And Contract

Three advisory architecture subagents are authorized only after
`SOURCE_CONTEXT_READY`.

Launch separate lanes:

- Directional lane: strongest source-backed case for the target architecture.
- Adversarial lane: strongest source-backed case against final-ready status,
  focusing on implicit owner-decision closure, boundary leakage, schema/runtime
  gravity, fake-success paths, and premature implementation gravity.
- Grounding lane: repo-native, source-bounded, anti-bloat, reversible,
  planning-only check; identify what to cut, soften, defer, or mark.

Runtime-safety rules:

- Use inherited/default agent type and model unless the host explicitly supports
  overrides and an override is required.
- Do not set `agent_type`, `model`, `reasoning_effort`, `service_tier`, or
  equivalent runtime fields to `default`, `null`, empty, or same-as-parent.
- Put lane differences in the task prompt, not runtime fields.
- If delegation is unavailable, run all three perspectives locally and disclose
  the fallback.

Each subagent must return exactly these common fields, one line per field, with
a `file:line` cite for every load-bearing claim and `unknown` for absent fields:

```text
lane:
source_context:
evidence_coverage:
core_position:
architecture_fit_or_failure:
source_alignment_or_conflict:
owner_decision_risk:
boundary_or_schema_risk:
minimum_required_change_before_owner_reading:
optional_hardening:
what_would_change_your_position:
advisory_boundary: This is advisory input only. It is not a verdict, not implementation authority, and not proof of readiness.
```

Reject any subagent return that:

- declares `SOURCE_CONTEXT_INCOMPLETE`;
- lacks `file:line` cites for load-bearing claims;
- emits a prose dump instead of the named fields;
- recommends implementation, schema design, proof execution, or ratification;
- treats subagent agreement as validation or readiness.

You may rerun one invalid subagent once with the same source pack and a tighter
return-shape instruction. If it still fails, disclose the invalid lane and run
that perspective locally. Do not count an invalid delegated return as one of the
three evidence perspectives.

## Architecture Questions To Answer

1. Is the Cleaning Spine foundation target the right architecture shape for a
   foundation draft?
2. Does it preserve raw as canonical and projection/cleaning as traceable working
   views?
3. Does it keep Data Capture / ECR / Cleaning / Judgment boundaries intact?
4. Does it avoid silently ratifying Projection Doctrine v0, "Projected Unit",
   "Cleaned Unit", runtime schema, or a heavier pipeline order than the installed
   OD-1 input-handle direction?
5. Does it keep core v0 dedupe to exact-identity mechanics while leaving
   near-match grouping, clustering promotion, independence, credibility,
   amplification, demand support, Signal Integrity, Signal Use, Decision
   Strength, and Action Ceiling outside core Cleaning?
6. Does it distinguish source-invariant core rules from source-family
   adaptation and unresolved candidates?
7. Are installed OD-1, OD-4, and OD-7 directions applied without widening?
8. Is any minimal caveat patch needed before owner reading, or can the draft go
   to owner reading as-is with explicit non-claims?

## Option Set

Compare at least these options unless source loading reveals a better set:

- `AO-1 Keep as-is for owner reading`: target is architecturally fit as a
  foundation draft with existing caveats.
- `AO-2 Keep with tiny caveat patch`: target architecture is correct, but strict
  ledger/traceability/raw-pull language needs adjacent candidate/non-schema
  caveats before owner reading.
- `AO-3 Block pending owner decision`: a requested widening beyond installed
  OD-1, OD-4, or OD-7 direction, Projection Doctrine candidate status, or
  boundary conflicts make final architecture reading
  premature.
- `AO-4 Defer to adversarial artifact review first`: architecture pass cannot
  responsibly read final-owner fitness without formal artifact review.

Do not create implementation options. Do not propose runtime schemas.

## Final Output Contract

Return headed prose, not YAML-only.

Required sections:

```text
Human Summary:
Decision:
Target Architecture:
Why This Wins:
Core / Satellite Boundary:
Deferred Implementation Implications:
What We Are Not Doing:
Boundary:
Next:

Agent Detail:
Profile / Evidence Mode / Source Mode:
Subagents Launched:
Invalid Or Rejected Subagent Returns:
Source-Read Ledger:
Goal-Frame Check:
Cynefin Routing:
Architecture Option Comparison:
Architecture Result:
Target Architecture Detail:
Validation / Failure Implications:
Bloat-Cut Queue:
Blockers / Not-Proven Boundaries:
What Would Change The Recommendation:
```

Architecture result must be exactly one of:

- `TARGET_RECOMMENDED`
- `OPTIONS_COMPARED_NO_SELECTION`
- `NEEDS_ARCHITECTURE_QUESTION`
- `NEEDS_PRODUCT_DECISION`
- `NEEDS_FEATURE_PLANNING`
- `NEEDS_SOURCE_CONTEXT`
- `DEFER_OR_REJECT`
- `AUTHORITY_BLOCKED`

Next routing object must be one of:

- no-op: owner reading can proceed as foundation draft;
- tiny docs patch recommendation only, with exact target sections and why;
- adversarial artifact review prompt/run;
- owner decision request only if the reading needs to change installed OD-1,
  OD-4, or OD-7 direction;
- source-context blocker.

## Hard Non-Claims

Do not claim:

- validation;
- readiness;
- owner ratification;
- buyer proof;
- Judgment quality;
- implementation authorization;
- runtime schema authorization;
- proof-run authorization;
- Projection Doctrine v0 ratification;
- that a clean mechanical checker run proves architecture quality.

## Validation For This Read-Only Run

Run and report:

- `git status --short --branch`

Do not run write checks unless you edit files, and you are not authorized to edit
files under this prompt. If you recommend a later patch, name the validation
gates that patch lane should run:

- `python .agents/hooks/check_retrieval_header.py --changed`
- `python .agents/hooks/check_repo_map_freshness.py --changed`
- `git diff --check`

## Prompt Verdict At Authoring

```yaml
prompt_verdict: PASS_WITH_WARNINGS
warnings:
  - Receiver must not count a subagent that fails SOURCE_CONTEXT_READY or lacks line-cited claims.
  - The target foundation artifact may be untracked when this prompt is first used.
  - The architecture reading is advisory and planning-only; it is not owner ratification or implementation authorization.
```
