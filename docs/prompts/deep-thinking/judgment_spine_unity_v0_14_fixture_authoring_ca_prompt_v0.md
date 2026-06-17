# Judgment Spine Unity v0.14 Fixture Authoring CA Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Chief Architect prompt for authoring a docs-only Unity Runtime Fee v0.14 draft fixture pack from the patched extraction plan.
use_when:
  - Launching the first docs-only Unity v0.14 fixture-authoring lane.
  - Turning the Unity extraction plan into draft participant-packet, evidence-registry, facilitator-ledger, and adapter-status artifacts.
  - Preserving hard boundaries before implementation, probe execution, model runs, scoring, validation, or proof claims.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md
  - docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md
  - docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md
  - docs/product/foundation/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md
input_hashes:
  docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md: DC0C9D64312E7A2BC49FA4EE227DD581E43919FBDD93F25AF83E6DFAB9677CE7
  docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_v0.md: 730A707674756E9EB9B7CE9678EBB1C02A3A1D9A2CD5EF3F1B5BB0746DCC569E
  docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md: FA4F7642ECAFB0488B57076F2DF59F8F4A742AA422331C9E833FA8AF548FFF24
  docs/product/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md: 2DB46EEF3D6ED6F54451693DC33B5B789066EB1BF26946370B702601650A3C30
  docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md: CFFC7BCAC179B752B9A77204ECA6A6399D30DD7CB6B2C52533E3EC0FDC031D8D
  docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md: FDEA14A1767D135A8DD56AF073AF0E5E3206B945FB9E603F597491D795889C71
```

- Status: PROPOSED_PROMPT
- Artifact type: Deep-thinking / Chief Architect prompt
- Intended output mode: file-write in the receiving CA lane
- Receiving lane edit permission: docs-write, bounded to the draft fixture pack and narrow discovery pointers only
- Required draft fixture root: `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/`
- Implementation, runtime, package, test, automation, commit, push, PR, model run, memorization-probe execution, scoring execution, proof-run, product-proof, validation execution, or lesson-promotion authorized: no

## Prompt Author Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus prompt-orchestration overlay, patched Unity extraction plan, Unity review report, v0.14 schema/protocol specs, and prior Unity source hashes
  edit_permission: docs-write
  target_scope: Patch EUP-05/EUP-06 polish and create a CA prompt for a docs-only Unity v0.14 draft fixture-authoring lane.
  dirty_state_checked: yes
  blocked_if_missing: no
control_plane_source_state:
  branch: main
  head: b7627d3
  overlay_sources_modified_or_untracked: yes
  judgment_spine_sources_untracked: yes
  strict_pass_or_readiness_claimed: no
```

## Deep-Thinking Boundary Decision

The real question is not whether to "build the harness" yet. The real question is whether the next lane can create the first concrete v0.14 fixture-shaped artifact pack without fabricating schema-valid readiness, running a model, executing a memorization probe, scoring, or crossing into code.

Rejected route: direct implementation or runnable case-folder creation. It is premature because Unity remains blocked by probe status, ledger freeze, missing per-source hashes, sealed-memo adapter gaps, and score-readiness non-claims.

Selected route: docs-only draft fixture pack. It gives the harness foundation a concrete case-shaped substrate while preserving all hard gates. The output must be useful for later implementation scoping, but must itself remain `BLOCKED_BEFORE_SCORING`.

## Prompt

You are acting as a Chief Architect for Orca's Judgment Spine / v0.14 harness foundation workstream.

Your job is to author the smallest docs-only Unity Runtime Fee v0.14 draft fixture pack from the patched extraction plan. This is the first concrete fixture-authoring lane. It is not an implementation lane, not a probe lane, not a model-run lane, not a scoring lane, not a validation lane, not a proof-run lane, not a product-proof lane, and not a lesson-promotion lane.

The draft fixture pack should make the v0.14 case shape tangible enough for later review and implementation scoping, while remaining explicitly blocked before scoring.

## Workspace

- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch: current Orca working branch
- Dirty-state allowance: dirty and untracked Orca docs may exist. Read and write only the bounded target files named in this prompt. Do not treat dirty or untracked files as accepted source-of-truth unless an accepted Orca source says so.
- Output mode: `file-write`
- Required draft fixture root: `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/`
- Optional navigation patch allowed: only if needed to make the new draft fixture pack discoverable, and only in `docs/research/judgment-spine/harness/v0_14/index.md`, `docs/research/judgment-spine/manifest_v0.md`, or `docs/workflows/orca_repo_map_v0.md`.

## Goal To Consume

Treat this goal as thread-local goal context, not source authority, validation evidence, readiness, approval, sequencing authority, or edit permission beyond the explicit edit permission above.

```yaml
goal_handoff:
  long_term_goal: Develop Judgment Spine into a durable judgment-improvement layer where real cases can become repeatable, scored, failure-logged learning material without losing spoiler safety, layer boundaries, or non-claims.
  anchor_goal: Define a case-to-v0.14 bridge CA lane that maps existing Judgment Spine case material into the v0.14 Judgment Harness foundation before any harness implementation.
  success_signal: A CA can determine the minimum harness-entry shape for one real case, identify which v0.14 spec files control it, expose missing or unsafe inputs, and name the smallest later implementation scope without authorizing code.
  status: user_stated
selected_next_move:
  source: owner_after_fixture_extraction_review_patch
  move: Author a docs-only Unity v0.14 draft fixture pack from the patched extraction plan, still blocked before scoring.
  output_fit_check: The fixture-authoring lane writes a draft participant packet, draft evidence registry, draft facilitator ledger, sealed-memo adapter note, and fixture authoring receipt that expose exact missing fields and hard gates without authorizing implementation, probe execution, model runs, scoring, validation, proof, product proof, or lesson promotion.
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  current_output_target: selected_next_move.move
  output_fit_check: selected_next_move.output_fit_check
  target_delta_from_prior:
    status: narrowed
    changed_fields: [current_output_target, output_fit_check]
    summary: Shifted from extraction-plan repair to docs-only fixture artifact drafting.
  drift_guard: Do not let draft fixture authoring become implementation, runnable case creation, probe execution, model judging, scoring, validation, product proof, lesson promotion, or harness-superiority proof.
  conflict_behavior: call_out_conflict_before_proceeding
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: yes
  lifecycle_status: active_thread_local
  if_changed_reason: The owner asked to proceed to the bounded fixture-authoring CA prompt after EUP-05/EUP-06 polish.
```

Before producing conclusions, state in working notes whether the source-loaded task still fits the `anchor_goal`, `success_signal`, and `selected_next_move.output_fit_check`. If it does not, stop with `BLOCKED_GOAL_CONFLICT`.

## Method Sequencing

If available, `REFERENCE-LOAD` `workflow-deep-thinking` as reasoning discipline. Do not `APPLY` it yet.

Do not apply any method to produce conclusions, fixture artifacts, field maps, fallback decisions, or recommendations before source readiness.

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

Read these authority and routing files first:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-of-truth.md`
4. `.agents/workflow-overlay/source-loading.md`
5. `.agents/workflow-overlay/prompt-orchestration.md`
6. `.agents/workflow-overlay/artifact-roles.md`
7. `.agents/workflow-overlay/artifact-folders.md`
8. `.agents/workflow-overlay/validation-gates.md`
9. `.agents/workflow-overlay/retrieval-metadata.md`
10. `docs/workflows/orca_repo_map_v0.md`

Read these Judgment Spine and bridge-control files:

11. `docs/research/judgment-spine/judgment_spine_thesis_v0.md`
12. `docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md`
13. `docs/research/judgment-spine/README.md`
14. `docs/research/judgment-spine/manifest_v0.md`
15. `docs/research/judgment-spine/harness/v0_14/index.md`
16. `docs/research/judgment-spine/harness/v0_14/case_to_v0_14_bridge_foundation_v0.md`
17. `docs/research/judgment-spine/harness/v0_14/unity_v0_14_fixture_extraction_plan_v0.md`
18. `docs/review-outputs/adversarial-artifact-reviews/unity_v0_14_fixture_extraction_plan_adversarial_review_v0.md`
19. `docs/research/judgment-spine/cases/unity-runtime-fee/case_index.md`

Read these v0.14 schema and protocol files:

20. `docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md`
21. `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md`
22. `docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md`
23. `docs/research/judgment-spine/harness/v0_14/blind_judgement_schema_and_harness_protocol.md`
24. `docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md`
25. `docs/research/judgment-spine/harness/v0_14/action_band_mapping_table_numbers.md`
26. `docs/research/judgment-spine/harness/v0_14/action_band_mapping_executable_spec.md`
27. `docs/research/judgment-spine/harness/v0_14/scorer_formula_spec.md`
28. `docs/research/judgment-spine/harness/v0_14/failure_event_log_spec.md`

Read the packet-safe Unity source before drafting participant-facing content:

29. `docs/product/orca_backtest_specimen_unity_runtime_fee_source_packet_v0.md`

Read these facilitator-only or revealed Unity sources only after participant-facing candidate content is clearly separated from hidden material:

30. `docs/product/orca_backtest_specimen_memo_unity_runtime_fee_at_cutoff_v0.md`
31. `docs/product/orca_backtest_specimen_unity_runtime_fee_outcome_calibration_v0.md`
32. `docs/research/judgment-spine/cases/unity-runtime-fee/reveal_readout_v0.md`

Optional targeted reads, only if they can materially change the draft fixture pack:

- `docs/research/judgment-spine/harness/v0_14/proof_and_memory_plan.md`
- `docs/research/judgment-spine/harness/v0_14/phase_1_infrastructure_architecture.md`
- Daimler fallback files under `docs/research/judgment-spine/cases/daimler-carve-out/`

Do not read all prompts, all cases, all review outputs, method-validation replays, proof-run packets, `docs/_inbox/`, the full product directory, implementation code, tests, packages, or runtime files by default. If one of those appears necessary, state the exact source gap first and keep the read targeted.

## Source Sequencing Rule For Spoiler Safety

The receiving CA may know facilitator-only material, but the participant-facing artifact must not contain it.

When drafting `participant_packet_draft_v0.md`, use only packet-safe facts from the source packet and v0.14 packet requirements. Do not include or imply actual outcome, backlash, revision, cancellation, owner blind read, sealed memo recommendation, calibration verdict, reveal lessons, frozen labels, derived floor or ceiling, must-address items, probe status, or fame-risk classification.

If participant-facing content is contaminated, stop participant-packet drafting, write a blocked receipt, and state `BLOCKED_PACKET_CONTAMINATION`.

## Authority And Boundaries

Allowed:

- create the required draft fixture root under `docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/`;
- create the five required draft fixture artifacts named below;
- optionally patch narrow discovery pointers in the allowed navigation files;
- author docs-only draft fixture surfaces from the patched extraction plan;
- freeze a canonical docs-only `case_id` string for this draft pack, unless source conflict blocks it;
- expose missing fields, unsafe inputs, contaminated inputs, adapter gaps, and hard stop criteria;
- mark draft labels as candidate or unfrozen when second-labeling, freeze hash, probe pass, or source support is missing;
- name the smallest later implementation implication as non-executable context only.

Not allowed:

- create implementation folders such as `src`, `app`, `packages`, `tests`, runners, configs, or automation;
- create runnable `.yaml` case folders intended for execution;
- run a memorization probe, call a model, generate a contestant blind judgment, run scoring, run tests, or execute validation;
- compute or claim participant-packet, ledger, blind-judgment, scoring, or fixture-admission hashes as readiness evidence;
- claim Unity is probe-safe, score-ready, validation-ready, accepted, source-of-truth promoted, or implementation-ready;
- treat the sealed memo as a fresh contestant run or scoring truth;
- reveal hidden facilitator-only material in the participant packet;
- promote case-local lessons into reusable doctrine;
- create product-proof, buyer-readiness, proof-run, or harness-superiority claims;
- import `jb` rules, paths, lifecycle mechanics, templates, or validation habits.

## Required Output Paths

Create these docs-only draft artifacts:

```text
docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/fixture_authoring_receipt_v0.md
docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/participant_packet_draft_v0.md
docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/evidence_registry_draft_v0.md
docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/facilitator_ledger_draft_v0.md
docs/research/judgment-spine/harness/v0_14/fixtures/unity_runtime_fee_2023_v0_14/sealed_memo_adapter_note_v0.md
```

Do not create `probes/`, `runs/`, `scores/`, executable case folders, code, tests, packages, configs, automation, or runtime files.

## Required Artifact Shape

`fixture_authoring_receipt_v0.md` must include:

- retrieval header;
- source context receipt and dirty/untracked caveats;
- consumed goal fit check;
- canonical draft `case_id`;
- draft fixture pack inventory;
- status: `DRAFT_FIXTURE_PACK_BLOCKED_BEFORE_SCORING`;
- exact blockers before scoring;
- leakage and memorization-probe gates;
- not-proven boundaries;
- source-read ledger;
- next authorized step.

`participant_packet_draft_v0.md` must include:

- a v0.14-compatible participant-packet frontmatter draft;
- decision question, cutoff, role frame, authority constraints, capability constraints, permitted assumptions, forbidden-information notice, and source manifest draft;
- participant-facing evidence summaries or references from packet-safe material only;
- known uncertainties and source gaps;
- no facilitator labels, no actual outcome, no sealed memo conclusions, no reveal facts, and no scoring hints.

If exact schema frontmatter conflicts with Orca retrieval metadata, preserve the v0.14 frontmatter first and put any Orca retrieval note below it. Do not break the participant packet shape to satisfy retrieval metadata.

`evidence_registry_draft_v0.md` must include:

- EU-01 through EU-08 mapped toward v0.14 `EvidenceUnit` fields;
- `evidence_id`, `source_id`, `source`, `timestamp`, `retrieval_timestamp`, `hash`, `pre_decision_status`, `pre_decision_basis`, and `summary` for each record when available;
- `TBD`, `UNKNOWN`, or `excluded` labels where fields are missing or unsafe;
- EU-08 adapter decision status;
- explicit note that source packet hash does not replace per-source source-byte hashes.

`facilitator_ledger_draft_v0.md` must include:

- direct Pydantic `FacilitatorLedger` draft fields separated from protocol fixture metadata;
- candidate `case_family` and candidate `decision_shape` as protocol/run metadata, not direct current Pydantic ledger fields;
- candidate or unfrozen `frozen_band_inputs` with enough rationale to review, or explicit `UNFROZEN`/`TBD` when the source does not support a label;
- second-label audit status, even if not performed;
- candidate must-address items with evidence-unit references;
- `underreach_observability` using only the Pydantic basis enum values;
- leakage audit notes and advisory spoiler inventory;
- protocol leakage inputs `memorization_probe_required` and `known_fame_risk` represented in notes or adapter section, not as direct current Pydantic ledger fields;
- `ledger_freeze_hash: NOT_COMPUTED`;
- status that the ledger is not frozen and cannot support scoring.

`sealed_memo_adapter_note_v0.md` must include:

- default treatment of the sealed memo as advisory or baseline-like legacy material, not a fresh contestant run;
- required gaps for `decision_shape`, `judgement_class`, run metadata, prompt hash, participant packet hash, facilitator ledger hash, evidence IDs, must-address coverage, and author-context contamination;
- whether the memo should be excluded, retained as parent Judgment Spine calibration material, or carried as a future adapter candidate;
- explicit non-comparability warning against fresh contestant outputs.

## Required Checks Before Closeout

Run only lightweight document checks:

- required output paths exist;
- required section markers exist;
- participant-facing packet draft does not contain obvious forbidden strings from the exclusion list;
- no trailing whitespace in created files;
- compute SHA256 hashes of created prompt or draft artifacts only as file provenance, not validation or readiness evidence.

Do not run tests, probes, model calls, scoring, validation, packages, automation, or implementation commands.

## Required Chat Closeout

After writing the draft fixture pack, return a concise chat summary:

1. `Outcome`: created files and any navigation pointers patched.
2. `Goal fit`: whether the draft pack satisfies the consumed anchor goal, success signal, and selected next move.
3. `Case ID`: canonical draft ID frozen or why it was blocked.
4. `Fixture status`: draft-only, blocked-before-scoring, not probe-safe, not score-ready, not validation-ready.
5. `Hard blockers`: memorization probe, participant packet hash, evidence hashes/timestamps, ledger freeze, second-label audit, sealed-memo adapter, and any contamination or source gaps.
6. `Boundaries preserved`: no implementation, runtime, tests, packages, automation, model run, probe execution, scoring, validation, proof-run, product-proof, lesson-promotion, or harness-superiority claim.
7. `Source-read ledger`: compact list of files read and why.
8. `Artifact hashes`: SHA256 hashes for created draft artifacts as provenance only.
9. `Next authorized step`: docs-only adversarial artifact review of the draft fixture pack, or owner-authorized patching of specific fixture-authoring defects.
