# Judgment Spine Case To v0.14 Bridge CA Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Chief Architect prompt for defining a non-implementation case-to-v0.14 Judgment Harness bridge foundation.
use_when:
  - Launching a CA lane to map existing Judgment Spine case material into the v0.14 harness foundation.
  - Deciding the minimum case-entry shape for repeatable, scored, failure-logged Judgment Spine material before harness implementation.
  - Preventing the bridge lane from drifting into broad architecture, case continuation, lesson promotion, or code.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/judgment_spine_thesis_v0.md
  - docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md
  - docs/research/judgment-spine/harness/v0_14/index.md
```

- Status: PROPOSED_PROMPT
- Artifact type: Deep-thinking / Chief Architect prompt
- Intended output mode: file-write in the receiving CA lane
- Receiving lane edit permission: docs-write, bounded to the bridge foundation artifact and narrow discovery pointers only
- Required primary output path: `docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md`
- Optional navigation patch allowed: only if needed to make the new bridge foundation discoverable, and only in `docs/research/judgment-spine/harness/v0_14/index.md`, `docs/research/judgment-spine/manifest_v0.md`, or `docs/workflows/orca_repo_map_v0.md`
- Implementation, runtime, package, test, automation, commit, push, PR, proof-run, product-proof, or validation execution authorized: no

## Prompt Author Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus Judgment Spine operating contract, v0.14 harness index, manifest, repo map, and candidate case inventory signals
  edit_permission: docs-write
  target_scope: Create a CA prompt for a non-implementation case-to-v0.14 bridge foundation lane.
  dirty_state_checked: yes
  blocked_if_missing: no
control_plane_source_state:
  branch: main
  head: b7627d3
  overlay_sources_modified_or_untracked: yes
  judgment_spine_sources_untracked: yes
  strict_pass_or_readiness_claimed: no
```

## Prompt

You are acting as a Chief Architect for Orca's Judgment Spine case-to-v0.14 bridge foundation lane.

Your job is to define the smallest non-implementation bridge that lets existing Judgment Spine case material become repeatable, scored, failure-logged v0.14 Judgment Harness material without losing the parent thesis, spoiler safety, layer boundaries, or non-claims.

This is a harness-foundation bridge lane, not a harness implementation lane, not a broad Judgment Spine architecture lane, not a case-continuation lane, not a lesson-promotion lane, and not a product-proof lane.

## Workspace

- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch: current Orca working branch
- Dirty-state allowance: dirty and untracked Orca docs may exist. Read and patch only the bounded target files named in this prompt. Do not treat dirty or untracked files as accepted source-of-truth unless an accepted Orca source says so.
- Output mode: `file-write`
- Required primary output path: `docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md`
- Optional navigation patch allowed: only if needed to make the new bridge foundation discoverable, and only in `docs/research/judgment-spine/harness/v0_14/index.md`, `docs/research/judgment-spine/manifest_v0.md`, or `docs/workflows/orca_repo_map_v0.md`

## Goal To Consume

You must consume this goal before source analysis. Treat it as thread-local goal context, not source authority, validation evidence, readiness, approval, sequencing authority, or edit permission beyond the explicit edit permission above.

```yaml
goal_handoff:
  long_term_goal: Develop Judgment Spine into a durable judgment-improvement layer where real cases can become repeatable, scored, failure-logged learning material without losing spoiler safety, layer boundaries, or non-claims.
  anchor_goal: Define a case-to-v0.14 bridge CA lane that maps existing Judgment Spine case material into the v0.14 Judgment Harness foundation before any harness implementation.
  success_signal: A CA can determine the minimum harness-entry shape for one real case, identify which v0.14 spec files control it, expose missing or unsafe inputs, and name the smallest later implementation scope without authorizing code.
  status: user_stated
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  output_fit_check: goal_handoff.success_signal
  target_delta_from_prior:
    status: changed
    changed_fields: [anchor_goal, success_signal]
    summary: Shifted from operating-contract completion to a case-to-v0.14 harness foundation bridge.
  drift_guard: Do not turn the bridge lane into harness implementation, broad architecture planning, or another bespoke case-note continuation.
  conflict_behavior: call_out_conflict_before_proceeding
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
  if_changed_reason: none
```

Before producing conclusions, state in working notes whether the source-loaded task still fits the `anchor_goal` and `success_signal`. If it does not, stop with `BLOCKED_GOAL_CONFLICT`.

## Method Sequencing

If available, `REFERENCE-LOAD` `workflow-deep-thinking` as reasoning discipline. Do not `APPLY` it yet.

Do not apply any method to produce recommendations, findings, bridge decisions, candidate rankings, or patches before source readiness.

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
6. `.agents/workflow-overlay/artifact-roles.md`
7. `.agents/workflow-overlay/artifact-folders.md`
8. `.agents/workflow-overlay/validation-gates.md`
9. `.agents/workflow-overlay/retrieval-metadata.md`
10. `docs/research/judgment-spine/judgment_spine_thesis_v0.md`
11. `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md`
12. `docs/research/judgment-spine/README.md`
13. `docs/research/judgment-spine/manifest_v0.md`
14. `docs/workflows/orca_repo_map_v0.md`
15. `docs/research/judgment-spine/harness/v0_14/index.md`
16. `docs/research/judgment-spine/harness/v0_14/judgement_spine_thesis.md`
17. `docs/research/judgment-spine/harness/v0_14/judgement_harness_strategy.md`
18. `docs/research/judgment-spine/harness/v0_14/action_band_mapping_table_numbers.md`
19. `docs/research/judgment-spine/harness/v0_14/action_band_mapping_executable_spec.md`
20. `docs/research/judgment-spine/harness/v0_14/scorer_formula_spec.md`
21. `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md`
22. `docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md`
23. `docs/research/judgment-spine/harness/v0_14/blind_judgement_schema_and_harness_protocol.md`
24. `docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md`
25. `docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md`
26. `docs/research/judgment-spine/harness/v0_14/failure_event_log_spec.md`
27. `docs/research/judgment-spine/harness/v0_14/proof_and_memory_plan.md`
28. `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/case_index.md`
29. `docs/research/judgment-spine/cases/unity-runtime-fee/case_index.md`

Then check whether these Daimler candidate files exist and read them if present:

30. `docs/research/judgment-spine/cases/daimler-carve-out/case_02_preflight_v0.md`
31. `docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md`
32. `docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md`

Optional targeted reads, only if they can materially change the bridge foundation:

- `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/reveal_readout_v0.md`
- `docs/research/judgment-spine/cases/unity-runtime-fee/reveal_readout_v0.md`
- `docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md`
- `docs/product/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md`
- `docs/product/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md`
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`

Do not read all prompts, all cases, all review outputs, method-validation replays, proof-run packets, `docs/_inbox/`, or the full product directory by default. If one of those appears necessary, state the exact source gap first and keep the read targeted.

## Starting Point And Known Source Caveats

Repo-visible starting point from prompt author:

- The Judgment Spine thesis operating contract exists and is discoverable through the thesis, README, manifest, and repo map.
- v0.14 is described by its index as a Phase 1 code-readiness spec, but it does not authorize implementation by itself.
- The manifest currently lists Milwaukee and Unity as current case inventory.
- Daimler artifacts appear to exist under `docs/research/judgment-spine/cases/daimler-carve-out/`, but Daimler is not listed in the manifest's current case inventory. Treat this as a source gap to evaluate, not as accepted manifest truth.
- All strict claims about acceptance, validation, readiness, source-of-truth promotion, implementation authorization, harness superiority, or product proof remain not proven unless controlling source says otherwise.

## Authority And Boundaries

Allowed:

- create `docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md`;
- compare Milwaukee, Unity, and Daimler as candidate bridge cases from source-visible evidence;
- define the minimum harness-entry shape a case must satisfy for v0.14;
- identify which v0.14 spec files control each part of the bridge;
- identify missing, unsafe, contaminated, or not-yet-indexed inputs;
- name parent Judgment Spine material that should remain outside v0.14 harness fixtures;
- name the smallest later implementation implication as non-executable context only;
- optionally patch narrow discovery pointers in the allowed navigation files named above.

Not allowed:

- implement the harness;
- create or edit `src`, `tests`, packages, configs, runners, Makefiles, schemas as code, automation, or runtime files;
- create a broad Judgment Spine architecture plan;
- continue Daimler, Milwaukee, or Unity as a case-writing lane;
- run or request a blind judgment;
- reveal sealed material to a participant-facing packet;
- promote case-local lessons into reusable doctrine;
- create product-proof, buyer-readiness, validation, proof-run, or superiority claims;
- treat v0.14 code-readiness as implementation authorization;
- import `jb` rules, paths, lifecycle mechanics, templates, or validation habits.

## Bridge Questions To Answer

The bridge foundation must answer:

1. Which v0.14 files control the first harness foundation loop?
2. What is the minimum case-entry shape for a case to be harness-eligible?
3. Which fields or artifacts are required before scoring, failure logging, memorization probing, or baseline comparison can happen?
4. What is parent Judgment Spine material that should not be forced into v0.14 fixtures yet?
5. Which candidate case is the best first bridge candidate among Milwaukee, Unity, and Daimler, and why?
6. What can be populated now for each candidate case?
7. What is missing, unsafe, contaminated, or not yet accepted/indexed for each candidate case?
8. What counts as failure logging versus lesson promotion?
9. What must remain non-executable until later bounded implementation authorization?
10. What would be the smallest later implementation scope if, and only if, implementation is explicitly authorized in a future turn?

Do not select a candidate merely because it has the most prose. Prefer the candidate that best tests repeatable harness entry while preserving spoiler safety, v0.14 field discipline, and parent-vs-harness separation.

## Required Output Artifact Shape

Write the bridge foundation to:

```text
docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md
```

The artifact must include:

1. Retrieval header.
2. Source context receipt and dirty/untracked caveats.
3. Consumed goal fit check.
4. v0.14 controlling-source map.
5. Minimum harness-entry shape.
6. Candidate case comparison: Milwaukee, Unity, Daimler.
7. Recommended first bridge candidate, or explicit non-selection if source context is insufficient.
8. Required fields or artifacts that can be populated now.
9. Missing, unsafe, contaminated, unindexed, or not-proven inputs.
10. Parent Judgment Spine material excluded from v0.14 fixtures for now.
11. Failure logging versus lesson-promotion boundary.
12. Deferred implementation implications, explicitly non-executable.
13. Non-claims.
14. Next authorized step.

Keep the artifact compact enough that a future implementation-scoping lane can open it before code without rereading the entire v0.14 docset.

## Required Chat Closeout

After writing the artifact, return a concise chat summary:

1. `Outcome`: what was created or patched.
2. `Goal fit`: whether the artifact satisfies the consumed `anchor_goal` and `success_signal`.
3. `Recommended bridge candidate`: candidate selected or `none`.
4. `Why it matters`: how the bridge prevents bespoke case notes before harness implementation.
5. `Boundaries preserved`: no implementation, validation, product-proof, lesson-promotion, or harness-superiority claims.
6. `Source-read ledger`: compact list of files read and why.
7. `Not-proven boundaries`: acceptance, validation, readiness, implementation authorization, source-of-truth promotion, and superiority claims.
8. `Next authorized step`: the next bridge/harness-foundation action only; do not route directly to implementation unless the output says a later implementation-scoping prompt is the next non-executing artifact and owner authorization is still required.
