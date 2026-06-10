# Judgment Spine Thesis Operating Contract CA Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact
scope: Chief Architect prompt for turning the Judgment Spine thesis into an operating contract and patching the thesis if needed.
use_when:
  - Launching a dedicated CA lane for the Judgment Spine thesis.
  - Asking a CA to consume the active goal frame before thesis operating-contract work.
  - Allowing bounded docs-write patches to the Judgment Spine thesis and thesis operating contract only.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/research/judgment-spine/judgment_spine_thesis_v0.md
```

- Status: PROPOSED_PROMPT
- Artifact type: Deep-thinking / Chief Architect prompt
- Intended output mode: file-write in the receiving CA lane
- Receiving lane edit permission: docs-write, bounded to thesis operating-contract work
- Implementation authorized: no
- Runtime, automation, package, test, commit, push, or PR authorized: no

## Prompt

You are acting as a Chief Architect for Orca's Judgment Spine thesis lane.

Your job is to turn the parent Judgment Spine thesis into a practical **Thesis Operating Contract** for future lanes, and to patch the thesis itself if you find wording gaps that would cause drift.

This is a thesis-governance lane, not a Judgment Harness implementation lane, not a broad Judgment Spine architecture lane, and not a review verdict lane.

## Workspace

- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch: current Orca working branch
- Dirty-state allowance: dirty and untracked Orca docs may exist. Read and patch only the bounded target files named below. Do not treat dirty or untracked files as accepted source-of-truth unless an accepted Orca source says so.
- Output mode: `file-write`
- Required primary output path: `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md`
- Thesis patch allowed: yes, bounded to `docs/research/judgment-spine/judgment_spine_thesis_v0.md`
- Navigation patch allowed: only if needed to make the new operating contract discoverable, and only in `docs/research/judgment-spine/README.md`, `docs/research/judgment-spine/manifest_v0.md`, or `docs/workflows/orca_repo_map_v0.md`.

## Goal To Consume

You must consume this goal before source analysis. Treat it as thread-local goal context, not source authority, validation evidence, readiness, approval, sequencing authority, or edit permission beyond the explicit edit permission above.

```yaml
goal_handoff:
  long_term_goal: Develop Judgment Spine into Orca's durable judgment-improvement layer for right-sized action under bounded approved evidence.
  anchor_goal: Define a Thesis Operating Contract for how future lanes should consume, protect, and apply the Judgment Spine thesis.
  success_signal: Future agents can use the thesis to judge fit, prevent drift, and preserve non-claims without re-litigating the long-term goal.
  status: inferred_thread_local
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  output_fit_check: goal_handoff.success_signal
  target_delta_from_prior:
    status: changed
    changed_fields: [anchor_goal]
    summary: Shifted from general Judgment Spine CA setup to a thesis-specific lane goal.
  drift_guard: Do not let the thesis lane become harness implementation planning or broad Judgment Spine architecture work.
  conflict_behavior: call_out_conflict_before_proceeding
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
  if_changed_reason: none
```

Before producing any conclusions, state in your working notes whether the source-loaded task still fits the `anchor_goal` and `success_signal`. If it does not, stop with `BLOCKED_GOAL_CONFLICT`.

## Method Sequencing

If available, `REFERENCE-LOAD` `workflow-deep-thinking` as reasoning discipline. Do not `APPLY` it yet.

Do not apply any method to produce recommendations, findings, or patches before source readiness.

First, source-load the required Orca files. Then declare either:

```yaml
source_context_status: SOURCE_CONTEXT_READY
```

or:

```yaml
source_context_status: SOURCE_CONTEXT_INCOMPLETE
missing_sources:
source_gaps:
why_it_matters:
```

Only after `SOURCE_CONTEXT_READY`, apply deeper reasoning to the loaded source context.

## Required Reads

Read these files first:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-of-truth.md`
4. `.agents/workflow-overlay/source-loading.md`
5. `.agents/workflow-overlay/prompt-orchestration.md`
6. `docs/research/judgment-spine/judgment_spine_thesis_v0.md`
7. `docs/research/judgment-spine/README.md`
8. `docs/research/judgment-spine/manifest_v0.md`
9. `docs/research/judgment-spine/harness/v0_14/index.md`
10. `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`

Optional reads, only if they can materially change the operating contract:

- `docs/product/core_spine_v0_information_production_foundation_v0.md`
- `docs/research/judgment-spine/harness/v0_14/judgement_spine_thesis.md`
- `docs/research/judgment-spine/harness/adjacent-context/README.md`
- `.agents/workflow-overlay/retrieval-metadata.md`

Do not read all prompts, all cases, review outputs, method-validation replays, proof-run packets, `docs/_inbox/`, or the full v0.14 harness docset by default. If one of those appears necessary, state the exact source gap first and keep the read targeted.

## Authority And Boundaries

Current owner instruction for this lane:

```yaml
thesis_allowed_to_patch_thesis: true
```

Allowed:

- create `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md`;
- patch `docs/research/judgment-spine/judgment_spine_thesis_v0.md` if a patch is directly needed to protect the long-term thesis from drift;
- optionally patch narrow navigation pointers if the new contract needs discovery;
- name unresolved owner decisions without resolving them yourself.

Not allowed:

- implement the v0.14 harness;
- create `src`, `tests`, packages, configs, runners, Makefiles, or automation;
- create a broad Judgment Spine architecture plan;
- create a Data Capture Spine, ECR, or Cleaning Spine design;
- create a proof-run plan, product claim, validation claim, or readiness claim;
- treat the thesis as source-of-truth promotion, approval, validation, or implementation authorization;
- import `jb` rules, paths, lifecycle mechanics, templates, or validation habits.

## Thesis Operating Contract Requirements

The operating contract should answer:

1. What the thesis optimizes for.
2. How future lanes should consume the thesis before acting.
3. What counts as thesis-aligned work.
4. What counts as thesis drift.
5. What changes require owner decision before proceeding.
6. How the thesis relates to:
   - parent Judgment Spine work;
   - v0.14 Judgment Harness specs;
   - case-learning artifacts;
   - failure logs and promoted lessons;
   - Data Capture / ECR / Cleaning boundaries;
   - implementation authorization boundaries.
7. How future agents should use the thesis when preparing CA prompts, harness changes, case additions, or lesson-promotion decisions.
8. What the thesis must not be used to claim.

Keep the operating contract compact enough to be opened before future Judgment Spine work without becoming a second architecture manual.

## Thesis Patch Rules

Patch the thesis only when the operating-contract work reveals a wording gap that would cause material future drift.

Valid thesis patches include:

- clarifying goal wording;
- sharpening non-claims;
- tightening parent-vs-harness separation;
- tightening layer boundaries;
- clarifying promotion or hindsight guards;
- clarifying how future lanes consume the thesis.

Invalid thesis patches include:

- adding implementation steps;
- expanding into full architecture;
- importing harness module layout into the parent thesis;
- turning side context into controlling authority;
- adding product-proof, buyer-readiness, validation, or superiority claims.

If you patch the thesis, keep changes small and explain the reason in your final summary.

## Required Output

Write the Thesis Operating Contract to:

```text
docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md
```

The contract must include a retrieval header and visible non-claims.

If you patch the thesis or navigation files, do so directly in the workspace and report the touched files.

Return a concise chat summary after writing:

1. `Outcome`: what was created or patched.
2. `Why it matters`: how it serves the consumed goal.
3. `Thesis patches`: list files and one-line rationale, or `none`.
4. `Boundaries preserved`: implementation, validation, product-proof, and layer-boundary non-claims.
5. `Source-read ledger`: compact list of files read and why.
6. `Not-proven boundaries`: readiness, validation, approval, implementation authorization, and superiority claims that remain not proven.
7. `Next authorized step`: the next thesis-lane action only; do not route to harness implementation.

