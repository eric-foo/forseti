# Canoo/Walmart Fixture Handoff Source-Loading Wrapper v0

```yaml
retrieval_header_version: 1
artifact_role: Thin wrapper prompt
scope: Source-loading wrapper for a new CA taking over the Canoo/Walmart v0.14 fixture workstream from the accepted docs-only hygiene state.
use_when:
  - Launching a fresh CA thread after the Canoo/Walmart precompact checkpoint.
  - Reconstructing current fixture state from source before selecting the next bounded fixture-authoring gate.
  - Preventing docs-only hygiene acceptance from being upgraded into runtime, scoring, validation, product-proof, or judgment-quality claims.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/hygiene-queue/precompact_canoo_walmart_fixture_handoff_v0.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/fixture_authoring_receipt_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_fixture_hygiene_post_patch_adversarial_recheck_v0.md
input_hashes:
  docs/prompts/hygiene-queue/precompact_canoo_walmart_fixture_handoff_v0.md: C9D41A4D904BB5243296D6AD2708A8C8C777D4549E062BA997733A077C191719
  docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/fixture_authoring_receipt_v0.md: E2AFBEB0D8A9740015BE408D34D19F2A922E5887A9D34D807E63845CCF0B841A
  docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_fixture_hygiene_post_patch_adversarial_recheck_v0.md: 0F09A0C6065234F05383D1B3D98D0A0E1053E80695CFDFE587F0DE5D5A8DDB0F
branch_or_commit: main @ a2aebdd
stale_if: Precompact, receipt, or accepted hygiene recheck hash changes; fixture sources are missing; source state cannot be verified from filesystem; or owner authorizes a different next-gate objective.
```

## 1. Wrapper Status And Purpose

- Prompt family: Thin wrapper / fresh CA source-loading wrapper
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch at wrapper creation: `main`
- Expected HEAD at wrapper creation: `a2aebdd`
- Wrapped guide artifact: `docs/prompts/hygiene-queue/precompact_canoo_walmart_fixture_handoff_v0.md`
- Wrapped guide SHA256 at wrapper creation: `C9D41A4D904BB5243296D6AD2708A8C8C777D4549E062BA997733A077C191719`
- Output mode for receiving CA: `chat-only`
- Edit permission for receiving CA: `read-only`
- Dirty-state allowance: dirty and untracked Orca docs/research/review files are expected and in scope for verification only; do not clean, revert, stage, commit, push, switch branches, or treat dirty state as readiness evidence.

This wrapper does not run a review, execute a patch, implement schema logic,
freeze a ledger, run a memorization probe, run a model, score a fixture,
validate a harness, prove product value, or claim judgment quality. It exists
only to make a fresh CA reconstruct current state from source and optimize the
next decision toward the accepted handoff goal.

## 2. Goal Handoff

```yaml
goal_handoff:
  long_term_goal: Build Orca's Judgment Spine into a disciplined signal-integrity backtest system that distinguishes real corroboration from artificial amplification without overclaiming validation.
  anchor_goal: Hand off Canoo/Walmart v0.14 from an accepted docs-only hygiene state so the next CA verifies current source state and decides the next bounded fixture-authoring gate without upgrading hygiene into readiness.
  success_signal: The next CA reconstructs state from source, preserves claim discipline, excludes wrong-lane contamination, and returns only a bounded next-gate recommendation.
  status: thread_local_handoff_context
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
  if_changed_reason: none
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: goal_handoff.anchor_goal
  output_fit_check: goal_handoff.success_signal
  target_delta_from_prior:
    status: unchanged
    changed_fields: []
    summary: Wrapper preserves the precompact goal frame and route shape for a fresh CA source-loading pass.
  drift_guard: Do not substitute accepted docs-only hygiene for blind-use readiness, scoring readiness, schema implementation readiness, validation, product proof, or judgment quality.
  conflict_behavior: call_out_conflict_before_proceeding
```

## 3. Launch Instruction For Receiving CA

Use this wrapper in a fresh thread only after the owner asks to launch the
handoff. Do not use this wrapper as evidence by itself.

Start in:

`C:\Users\vmon7\Desktop\projects\orca`

First read:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. This wrapper
4. `docs/prompts/hygiene-queue/precompact_canoo_walmart_fixture_handoff_v0.md`

Then verify the wrapped guide hash and the current source hashes from the
filesystem. Treat the precompact as an optimization guide, not source authority
and not proof of current state.

## 4. Required Source-Loading Pack

After authority and wrapper reads, source-load the smallest complete current
state pack:

1. `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/fixture_authoring_receipt_v0.md`
2. `docs/review-outputs/adversarial-artifact-reviews/canoo_walmart_v0_14_fixture_hygiene_post_patch_adversarial_recheck_v0.md`
3. `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/participant_packet_draft_v0.md`
4. `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/source_manifest_participant_safe_adapter_decision_v0.md`
5. `docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/protocol_pydantic_reconciliation_decision_v0.md`

Expected hashes at wrapper creation:

```yaml
expected_hashes:
  precompact_canoo_walmart_fixture_handoff_v0.md: C9D41A4D904BB5243296D6AD2708A8C8C777D4549E062BA997733A077C191719
  fixture_authoring_receipt_v0.md: E2AFBEB0D8A9740015BE408D34D19F2A922E5887A9D34D807E63845CCF0B841A
  canoo_walmart_v0_14_fixture_hygiene_post_patch_adversarial_recheck_v0.md: 0F09A0C6065234F05383D1B3D98D0A0E1053E80695CFDFE587F0DE5D5A8DDB0F
  participant_packet_draft_v0.md: EBA60C529ACBBA07324983FCAA5A48F268454A93F39C0F5D755DB9DCBB068CFB
  source_manifest_participant_safe_adapter_decision_v0.md: D6A0421094A41A19F938714F63A76E50AE94DAA92A2952DFE308A2C3458CCABD
  protocol_pydantic_reconciliation_decision_v0.md: 5109052BBB38B62E4A787E57FAC257797043E752EFF940B8304401996A434AF1
```

Declare one of:

```yaml
source_context_status: SOURCE_CONTEXT_READY
```

or:

```yaml
source_context_status: SOURCE_CONTEXT_INCOMPLETE
missing_or_mismatched_sources:
  - path:
    expected_hash:
    actual_hash:
    impact:
```

If any required source is missing or hash-mismatched, stop and report a blocked
source-state result. Do not reason forward from the precompact or chat context.

## 5. Decision Boundary

After `SOURCE_CONTEXT_READY`, return only a bounded current-state
recommendation for the next fixture-authoring gate.

Allowed recommendation vocabulary:

```yaml
recommendation:
  - proceed_to_owner_next_gate_selection
  - proceed_to_source_hash_and_retrieval_timestamp_gate
  - proceed_to_harness_rendering_linkage_scoping
  - proceed_to_memorization_probe_commissioning_prompt
  - proceed_to_ledger_freeze_preparation_scoping
  - block_for_source_mismatch
  - block_for_goal_or_authority_conflict
```

Choose one recommendation, with a short rationale grounded in verified source
state. Do not create a patch plan, implementation route, review prompt,
memorization probe prompt, schema work plan, ledger-freeze plan, or scoring
plan unless the owner separately asks for that next artifact.

## 6. Forbidden Imports And Non-Claims

Do not import:

- `jb` rules, paths, handoffs, GAP/CV Engine policy, lifecycle mechanics, or validation habits;
- wrong-lane Reddit/attention-lens material unless separately adjudicated;
- old chat summaries as source authority;
- accepted review findings as patch authority without owner authorization;
- TR/Casetext as judgment-quality evidence.

Do not claim:

- blind-use readiness;
- memorization-probe pass;
- model-run authorization;
- scoring readiness;
- schema implementation readiness;
- ledger-freeze readiness;
- validation;
- product proof;
- harness superiority;
- judgment quality.

Accepted docs-only hygiene means source consistency for this fixture-authoring
state only.

## 7. Required Output Shape

Return a compact result:

```yaml
handoff_source_loading_result:
  source_context_status:
  workspace:
  branch_and_head:
  dirty_state:
  verified_hashes:
    precompact:
    receipt:
    hygiene_recheck:
    participant_packet:
    source_manifest_adapter:
    protocol_pydantic_decision:
  current_state_summary:
  accepted_docs_only_hygiene:
  still_blocked:
    - blind use
    - memorization probe execution
    - model runs
    - scoring
    - ledger freeze
    - schema implementation
    - validation
    - proof-run
    - product proof
    - judgment-quality claim
  recommendation:
  rationale:
  next_authorized_step_boundary:
  required_closeout: plumbing works only; not judgment quality
```

If blocked, replace `recommendation` with `block_for_source_mismatch` or
`block_for_goal_or_authority_conflict` and name the exact source or authority
problem.

## 8. Paste-Ready Launch Body

Use this body when the owner asks to launch the fresh CA:

```text
Use the Canoo/Walmart fixture handoff source-loading wrapper.

Workspace:
`C:\Users\vmon7\Desktop\projects\orca`

Required first read:
`docs/prompts/wrappers/canoo_walmart_fixture_handoff_source_loading_wrapper_v0.md`

Follow the wrapper exactly. Treat the precompact file as an optimization guide, not source authority. Verify current source state and hashes from the filesystem before making any recommendation.

Return only the bounded handoff source-loading result requested by the wrapper. Do not create prompts, patch files, run reviews, implement schemas, freeze ledgers, run probes, run models, score fixtures, validate the harness, or claim product proof or judgment quality.

Required closeout: plumbing works only; not judgment quality.
```
