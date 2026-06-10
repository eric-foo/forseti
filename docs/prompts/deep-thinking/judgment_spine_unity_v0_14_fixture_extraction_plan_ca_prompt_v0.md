# Judgment Spine Unity v0.14 Fixture Extraction Plan CA Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Chief Architect prompt for creating a docs-only Unity Runtime Fee v0.14 fixture extraction plan.
use_when:
  - Launching a CA lane to convert the Unity bridge recommendation into a fixture-admission work queue.
  - Planning how existing Unity source material would map into v0.14 harness surfaces before implementation.
  - Preserving the hard gates for memorization probe risk, sealed-memo contamination, leakage audit mapping, and Daimler fallback.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md
  - docs/research/judgment-spine/cases/unity-runtime-fee/case_index.md
  - docs/research/judgment-spine/harness/v0_14/index.md
```

- Status: PROPOSED_PROMPT
- Artifact type: Deep-thinking / Chief Architect prompt
- Intended output mode: file-write in the receiving CA lane
- Receiving lane edit permission: docs-write, bounded to the Unity fixture extraction plan artifact and narrow discovery pointers only
- Required primary output path: `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md`
- Optional navigation patch allowed: only if needed to make the new extraction plan discoverable, and only in `docs/research/judgment-spine/harness/v0_14/index.md`, `docs/research/judgment-spine/manifest_v0.md`, or `docs/workflows/orca_repo_map_v0.md`
- Implementation, runtime, package, test, automation, commit, push, PR, model run, memorization-probe execution, scoring execution, proof-run, product-proof, or validation execution authorized: no

## Prompt Author Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus prompt-orchestration overlay, patched bridge foundation, bridge adversarial review, Unity case index, manifest, and v0.14 harness index
  edit_permission: docs-write
  target_scope: Create a CA prompt for a docs-only Unity v0.14 fixture extraction plan lane.
  dirty_state_checked: yes
  blocked_if_missing: no
control_plane_source_state:
  branch: main
  head: b7627d3
  overlay_sources_modified_or_untracked: yes
  bridge_foundation_untracked: yes
  prompt_target_exists: no
  output_target_exists: no
  strict_pass_or_readiness_claimed: no
```

Prompt-author observed SHA256 values:

```yaml
input_hashes:
  docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md: 1E5DCD75FDA955D8796887ECE70F7540F540B93AFA919F6A7A85AC0D67CE2192
  docs/review-outputs/adversarial-artifact-reviews/case_to_v0_14_bridge_foundation_adversarial_review_v0.md: CEE971DF9313D6DF50439F63058F4A2DF92B0FBD5FE4CE2D4F4226E05616C369
```

## Prompt

You are acting as a Chief Architect for Orca's Judgment Spine / v0.14 harness foundation workstream.

Your job is to create the smallest docs-only Unity Runtime Fee v0.14 fixture extraction plan that turns the patched bridge foundation into a concrete fixture-admission work queue, without building the harness, creating actual fixture artifacts, running probes, running models, scoring, validating, or promoting lessons.

This is a fixture extraction planning lane, not a harness implementation lane, not an implementation-scoping lane, not a case-continuation lane, not a fresh blind-judgment lane, not a lesson-promotion lane, not a proof-run lane, and not a product-proof lane.

## Workspace

- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch: current Orca working branch
- Dirty-state allowance: dirty and untracked Orca docs may exist. Read and patch only the bounded target files named in this prompt. Do not treat dirty or untracked files as accepted source-of-truth unless an accepted Orca source says so.
- Output mode: `file-write`
- Required primary output path: `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md`
- Optional navigation patch allowed: only if needed to make the new extraction plan discoverable, and only in `docs/research/judgment-spine/harness/v0_14/index.md`, `docs/research/judgment-spine/manifest_v0.md`, or `docs/workflows/orca_repo_map_v0.md`

## Goal To Consume

You must consume this goal before source analysis. Treat it as thread-local goal context, not source authority, validation evidence, readiness, approval, sequencing authority, or edit permission beyond the explicit edit permission above.

```yaml
goal_handoff:
  long_term_goal: Develop Judgment Spine into a durable judgment-improvement layer where real cases can become repeatable, scored, failure-logged learning material without losing spoiler safety, layer boundaries, or non-claims.
  anchor_goal: Define a case-to-v0.14 bridge CA lane that maps existing Judgment Spine case material into the v0.14 Judgment Harness foundation before any harness implementation.
  success_signal: A CA can determine the minimum harness-entry shape for one real case, identify which v0.14 spec files control it, expose missing or unsafe inputs, and name the smallest later implementation scope without authorizing code.
  status: user_stated
selected_next_move:
  source: incremental-planning
  move: Create a docs-only Unity v0.14 fixture extraction plan with a hard memorization-probe gate and explicit Daimler fallback decision.
  output_fit_check: The plan maps Unity's source packet into participant-packet extraction boundaries, evidence-registry conversion, facilitator-ledger work queue, leakage-audit fields, required decision_shape, sealed-memo contamination handling, parent-only exclusions, and a Daimler fallback trigger without authorizing implementation or scoring.
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  current_output_target: selected_next_move.move
  output_fit_check: selected_next_move.output_fit_check
  target_delta_from_prior:
    status: narrowed
    changed_fields: [current_output_target, output_fit_check]
    summary: Shifted from bridge foundation completion to a concrete Unity fixture extraction plan before implementation.
  drift_guard: Do not let Unity fixture extraction planning become harness implementation, actual fixture creation, blind judgment execution, scoring, product proof, or lesson promotion.
  conflict_behavior: call_out_conflict_before_proceeding
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: yes
  lifecycle_status: active_thread_local
  if_changed_reason: The owner accepted the incremental next move after the bridge foundation patch.
```

Before producing conclusions, state in working notes whether the source-loaded task still fits the `anchor_goal`, `success_signal`, and `selected_next_move.output_fit_check`. If it does not, stop with `BLOCKED_GOAL_CONFLICT`.

## Method Sequencing

If available, `REFERENCE-LOAD` `workflow-deep-thinking` as reasoning discipline. Do not `APPLY` it yet.

Do not apply any method to produce conclusions, extraction plans, fallback decisions, field maps, or recommendations before source readiness.

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
16. `docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md`
17. `docs/review-outputs/adversarial-artifact-reviews/case_to_v0_14_bridge_foundation_adversarial_review_v0.md`
18. `docs/research/judgment-spine/cases/unity-runtime-fee/case_index.md`
19. `docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md`
20. `docs/product/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md`
21. `docs/product/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md`
22. `docs/research/judgment-spine/cases/unity-runtime-fee/reveal_readout_v0.md`
23. `docs/research/judgment-spine/harness/v0_14/judgement_spine_thesis.md`
24. `docs/research/judgment-spine/harness/v0_14/judgement_harness_strategy.md`
25. `docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md`
26. `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md`
27. `docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md`
28. `docs/research/judgment-spine/harness/v0_14/action_band_mapping_table_numbers.md`
29. `docs/research/judgment-spine/harness/v0_14/action_band_mapping_executable_spec.md`
30. `docs/research/judgment-spine/harness/v0_14/scorer_formula_spec.md`
31. `docs/research/judgment-spine/harness/v0_14/blind_judgement_schema_and_harness_protocol.md`
32. `docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md`
33. `docs/research/judgment-spine/harness/v0_14/failure_event_log_spec.md`
34. `docs/research/judgment-spine/harness/v0_14/proof_and_memory_plan.md`

Then check whether these Daimler fallback files exist and read them if present:

35. `docs/research/judgment-spine/cases/daimler-carve-out/case_02_preflight_v0.md`
36. `docs/research/judgment-spine/cases/daimler-carve-out/participant_packet_v0.md`
37. `docs/research/judgment-spine/cases/daimler-carve-out/safety_receipt_v0.md`

Optional targeted reads, only if they can materially change the extraction plan:

- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/research/judgment-spine/harness/v0_14/phase_1_infrastructure_architecture.md`
- `docs/research/judgment-spine/harness/v0_14/changelog.md`
- `docs/product/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md`

Do not read all prompts, all cases, all review outputs, method-validation replays, proof-run packets, `docs/_inbox/`, the full product directory, or implementation code by default. If one of those appears necessary, state the exact source gap first and keep the read targeted.

## Starting Point And Known Source Caveats

Repo-visible starting point from prompt author:

- The patched bridge foundation recommends Unity as the first bridge-from-existing-material candidate, not as a proven scoreable, probe-safe, or first live blind-run candidate.
- The bridge foundation requires the Unity extraction plan to map participant packet, evidence registry, facilitator-ledger work queue, leakage-audit field mapping, memorization-probe risk, sealed-memo contamination handling, required `decision_shape`, and parent-only exclusions.
- The adversarial review report is historical review evidence. The bridge foundation was patched after that report. Use the report to understand failure modes, but the current bridge foundation controls if the two conflict.
- The Unity case is revealed. Reveal readout, outcome calibration, owner blind read, sealed memo conclusions, lessons, and tactical interpretation must not enter any participant-facing fixture plan.
- Unity Runtime Fee has elevated known-event and memorization-probe risk for modern frontier models. Probe failure rejects or quarantines Unity for that contestant/model family.
- Daimler is a lower-fame-risk fresh blind-run candidate but remains unindexed in the manifest and lacks sealed judgment, reveal, calibration, evidence registry, and v0.14 ledger material.
- All strict claims about acceptance, validation, readiness, source-of-truth promotion, implementation authorization, harness superiority, memorization-probe pass, scoring readiness, or product proof remain not proven unless controlling source says otherwise.

## Authority And Boundaries

Allowed:

- create `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md`;
- optionally patch narrow discovery pointers in the allowed navigation files named above;
- define a docs-only extraction plan for Unity's existing source material;
- map source-visible Unity material into plan surfaces for participant packet, evidence registry, facilitator-ledger work queue, leakage-audit fields, blind-judgment seed treatment, memorization-probe admission gate, and parent-only exclusions;
- define missing fields, unsafe inputs, adapter needs, and hard stop/fallback criteria;
- define when Daimler becomes the better next candidate if Unity is blocked for scoring or probe safety;
- name the smallest later implementation implication as non-executable context only.

Not allowed:

- implement the harness;
- create or edit `src`, `tests`, packages, configs, runners, Makefiles, schemas as code, automation, or runtime files;
- create the actual Unity participant packet, safety receipt, evidence registry, facilitator ledger, blind judgment, memorization probe artifact, scoring result, failure event log, or case report;
- run a memorization probe, call a model, run scoring, run tests, or execute validation;
- create a broad Judgment Spine architecture plan;
- continue Unity as a case-writing or lesson-promotion lane;
- run or request a new blind judgment;
- reveal sealed, outcome, owner-read, calibration, or post-cutoff material to a participant-facing packet;
- promote case-local lessons into reusable doctrine;
- create product-proof, buyer-readiness, validation, proof-run, or superiority claims;
- treat v0.14 code-readiness as implementation authorization;
- import `jb` rules, paths, lifecycle mechanics, templates, or validation habits.

## Extraction Questions To Answer

The Unity fixture extraction plan must answer:

1. Which Unity materials are participant-facing candidates, facilitator-only candidates, parent-only materials, or excluded materials?
2. Which source-packet elements can seed v0.14 `ParticipantPacket` frontmatter and body sections, and which participant-facing facts must remain absent?
3. How should source-packet Evidence Units EU-01 through EU-08 map toward v0.14 `EvidenceUnit` fields, and which required fields, hashes, timestamps, or status labels are missing?
4. Which facilitator-ledger fields must be operator-authored later, including band labels, second-label diffs, must-address items, underreach observability, mapping versions, freeze hash, and committed timestamp?
5. How should leakage-audit information map into v0.14 fields such as `leakage_audit_notes`, `spoiler_inventory`, `memorization_probe_required`, and `known_fame_risk` without creating a standalone v0.14 leakage artifact?
6. What exact memorization-probe admission gate must occur before Unity is used for a model family, and what happens for pass, fail, or ambiguous results?
7. How should the sealed Unity memo be treated: advisory, baseline-like, existing contestant-like seed, or excluded from scoring, given required `decision_shape`, run metadata, evidence ID, must-address, prompt hash, and author-context contamination gaps?
8. What must remain parent Judgment Spine material or facilitator-only post-run context, including reveal readout, outcome calibration, owner blind read, reusable lessons, and product-proof implications?
9. When does Daimler become the better next candidate or fallback route?
10. What remains blocked before any v0.14 scoring, failure logging, baseline comparison, proof-run, or implementation scoping may proceed?

## Required Output Artifact Shape

Write the Unity extraction plan to:

```text
docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md
```

The artifact must include:

1. Retrieval header.
2. Source context receipt and dirty/untracked caveats.
3. Consumed goal fit check.
4. Purpose, non-use boundary, and strict non-claims.
5. Unity source-material classification: participant-facing candidate, facilitator-only, parent-only, excluded.
6. Participant packet extraction plan, explicitly not the packet.
7. Evidence registry conversion plan for EU-01 through EU-08, including missing fields.
8. Facilitator-ledger work queue, including band inputs, second-label audit, must-address items, underreach observability, leakage audit, freeze hash, and committed timestamp.
9. Leakage-audit field mapping, explicitly not a standalone v0.14 artifact.
10. Memorization-probe admission gate with pass/fail/ambiguous routing and model-family quarantine rule.
11. Sealed Unity memo treatment, including required `decision_shape`, run metadata gaps, evidence ID gaps, must-address coverage gaps, prompt hash gaps, and author-context contamination.
12. Parent-only and facilitator-only exclusion list.
13. Daimler fallback decision gate.
14. Blocked-before-scoring checklist.
15. Deferred implementation implications, explicitly non-executable.
16. Source-read ledger.
17. Next authorized step.

Keep the artifact compact enough that a future review or implementation-scoping lane can open it before any code without rereading the entire v0.14 docset.

## Required Chat Closeout

After writing the artifact, return a concise chat summary:

1. `Outcome`: what was created or patched.
2. `Goal fit`: whether the artifact satisfies the consumed anchor goal, success signal, and selected next move.
3. `Unity admissibility`: whether Unity is plan-ready, probe-safe, score-ready, or still blocked. Use `not proven` unless the artifact has source-backed proof.
4. `Hard gates`: memorization probe, leakage audit, sealed-memo contamination, required `decision_shape`, and facilitator ledger freeze.
5. `Daimler fallback`: when the plan says to switch or defer to Daimler.
6. `Boundaries preserved`: no implementation, validation, scoring, proof-run, product-proof, lesson-promotion, or harness-superiority claims.
7. `Source-read ledger`: compact list of files read and why.
8. `Not-proven boundaries`: acceptance, validation, readiness, implementation authorization, source-of-truth promotion, memorization-probe pass, score-readiness, and superiority claims.
9. `Next authorized step`: the next docs-only bridge/harness-foundation action only. Do not route directly to implementation unless the output says a later implementation-scoping prompt is the next non-executing artifact and owner authorization is still required.
