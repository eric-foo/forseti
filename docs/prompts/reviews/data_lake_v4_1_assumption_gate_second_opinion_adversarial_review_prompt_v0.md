# Data Lake v4.1 Assumption Gate Second-Opinion Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Source-backed second-opinion adversarial review of the fused-turn assumption
  gate that blocked v4.1 Source Capture runner implementation on missing
  packet_shard grammar and branch-only v4.1 contract authority.
use_when:
  - Deciding whether the v4.1 runner implementation gate is overblocking.
  - Checking whether packet_shard can be safely defaulted or must be specified first.
  - Preparing the next owner decision before DataLakeRoot v4.1 implementation.
open_next:
  - docs/review-outputs/adversarial-artifact-reviews/capture_runner_v4_1_blocker_adversarial_review_v0.md
  - docs/review-outputs/capture_spine_runner_data_lake_v4_1_addendum_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
  - forseti-harness/data_lake/root.py
  - forseti-harness/source_capture/writer.py
  - forseti-harness/source_capture/packet_assembly.py
  - forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
branch_or_commit: codex/ig-reels-capture-spine @ b82551f5
stale_if:
  - The v4.1 forward-epoch contract lands on origin/main, is rejected, or materially changes.
  - packet_shard, lake_epoch, or orca-lake-epoch behavior appears in orca-harness.
  - DataLakeRoot root marker, raw pathing, staging, publishing, or availability behavior changes.
  - Any Source Capture packet runner gains or loses data_root support.
  - The fused assumption-gate decision is superseded by an owner decision.
authority_boundary: retrieval_only
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_second_opinion_review
  edit_permission: read-only
  target_scope: >
    Review whether the assumption-gate blocker for Data Lake v4.1 runner
    implementation is correct, overstated, understated, or missing a better
    owner-decision route.
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
    - orca-harness/data_lake/root.py
```

- authorization_basis: current owner request for a second opinion prompt after fused stopped at the assumption gate.
- objective / intended_decision: decide whether the fused assumption gate should remain blocked, clear with warnings, or reroute to a narrower owner/spec decision before implementation.
- output_mode: `review-report`.
- prompt_artifact_path: `docs/prompts/reviews/data_lake_v4_1_assumption_gate_second_opinion_adversarial_review_prompt_v0.md`.
- required_report_path: `docs/review-outputs/adversarial-artifact-reviews/data_lake_v4_1_assumption_gate_second_opinion_adversarial_review_v0.md`.
- template_kind: `adversarial-artifact-review`; template source `docs/prompts/templates/review/adversarial_artifact_review_v0.md`.
- edit_permission: read-only review; reviewer may write only the required report.
- workspace_path: `C:\Users\vmon7\Desktop\projects\orca`.
- branch_or_commit_reference: expected branch `codex/ig-reels-capture-spine`, expected prompt-authoring HEAD `b82551f5`.
- dirty_state_allowance: unrelated untracked files may exist; they are out of scope unless they touch required sources. Modified or staged required sources block strict review claims until classified.
- controlling_source_state: checked at prompt authoring; branch has unrelated untracked clutter, and no staged changes were observed. Receiver must recheck before review.
- isolation_decision: neither; this is read-only review prompt/report work.
- doctrine_change_decision: no doctrine change requested; this is decision input only.
- validation_gates: source-read verification plus report write/readback; no implementation validation is run.
- thread_operating_target_continuity: no visible active thread_operating_target block to carry.

## Review Commission

You are performing a read-only adversarial artifact review for Orca.

This is a second opinion on the current gate decision:

> Fused implementation to make Source Capture runners v4.1-friendly stopped before implementation because `packet_shard` is named by the v4.1 contract but not defined, and the v4.1 forward-epoch contract exists on the current branch but not on `origin/main`.

The question is not "can you implement it." The question is whether that stop is the right decision, or whether it is overblocking and implementation could safely proceed under a narrower owner/default decision.

## Fitness Reference

Goal: prevent the v4.1 runner implementation from baking in a wrong or unstable lake path contract.

Done looks like: the Chief Architect can make one concrete next decision from the review: keep the fused gate blocked, clear it with named owner authorization, or reroute to a precise spec/contract decision before implementation.

This is an alignment axis to attack, not a pass bar. If the goal or done signal is wrong or incomplete, say so as a finding.

## Required Authority Sources

Read these before strict or actionable claims:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/template-registry.md`
- `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`
- `docs/prompts/templates/review/adversarial_artifact_review_v0.md`

Then read the task sources:

- this prompt;
- `docs/review-outputs/adversarial-artifact-reviews/capture_runner_v4_1_blocker_adversarial_review_v0.md`;
- `docs/review-outputs/capture_spine_runner_data_lake_v4_1_addendum_v0.md`;
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md`;
- `orca-harness/data_lake/root.py`;
- `orca-harness/source_capture/writer.py`;
- `orca-harness/source_capture/packet_assembly.py`;
- `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`;
- `orca-harness/tests/test_data_lake_availability.py`;
- `orca-harness/tests/test_data_lake_root.py`.

Do not read or write `F:\orca-data-lake` for this second opinion unless you can do a strictly read-only check and can explain why repo sources are insufficient. Live-root cleanup, live capture, and external-root writes are out of scope.

## Source-Gated Method Contract

REFERENCE-LOAD these methods before source loading:

- `workflow-deep-thinking`
- `workflow-adversarial-artifact-review`

Do not APPLY them yet. Use them only to prepare a neutral source-reading lens.

SOURCE-LOAD the required sources above. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before any conclusion, recommendation, or finding.

Only after source readiness, APPLY `workflow-deep-thinking` to frame failure modes, then APPLY `workflow-adversarial-artifact-review` to produce findings.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or not applied after `SOURCE_CONTEXT_READY`, return only a blocked or advisory-only result. Do not emit strict review claims, formal verdicts, readiness claims, validation claims, mandatory remediation, patch queues, or executor-ready handoffs.

## Required Fresh Checks

Run or otherwise verify the equivalent of these checks from the local repo:

- branch, HEAD, and dirty state;
- whether `origin/main` contains `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md`;
- whether `packet_shard`, `lake_epoch`, or `orca-lake-epoch` behavior exists in `orca-harness`;
- whether `root.py` still has `ROOT_MARKER_CONTRACT_VERSION = "v0"`;
- whether `root.py` still emits unsharded `raw/{packet_id}` availability refs;
- whether `allocate_raw_packet_dir`, `stage_raw_packet`, and `publish_raw_packet` still use `raw/<packet_id>`;
- the current count of packet-producing runners and how many expose `data_root`;
- whether current tests still assert the v0 raw path or merely seam coverage.

Treat the following as prompt-author observations to verify, not trusted facts:

- observed prompt-authoring branch/head: `codex/ig-reels-capture-spine @ b82551f5`;
- observed contract-on-origin-main check: contract not present on `origin/main`;
- observed harness grep: `packet_shard|lake_epoch|orca-lake-epoch` has no harness implementation;
- observed DataLakeRoot: v0 marker, unsharded raw paths, no epoch marker;
- observed runner count: 12 packet-producing runners, 3 with `data_root`, 9 unsynced.

## Attack Questions

Findings should focus on these decision-relevant questions:

1. Is the assumption gate correctly blocking implementation because `packet_shard` is undefined, or is a defensible rule already derivable from current sources?
2. Is "not on `origin/main`" a real blocker here, or can the current branch contract plus owner "fused go" authorize branch-only implementation without waiting for mainline landing?
3. Would choosing "first three lowercase hex chars of `sha256(packet_id)`" be a safe default, a reasonable owner decision, or an unjustified durable-layout invention?
4. Is the right next step spec writing, owner decision, contract patch, implementation scoping refresh, or direct implementation with warnings?
5. Did the prior blocker review or addendum understate any prerequisite that should block fused even after `packet_shard` is defined?
6. Did the fused gate overstep its authority by stopping on a decision the owner could make in chat?

Do not soften a material failure mode because it would be inconvenient. Also do not preserve the blocker if current source and owner authority make it unnecessary.

## Output Contract

Write the durable review report to:

`docs/review-outputs/adversarial-artifact-reviews/data_lake_v4_1_assumption_gate_second_opinion_adversarial_review_v0.md`

The report must include:

- retrieval header;
- provenance fields: `reviewed_by` and `authored_by` (operator/tooling supplied; use `unrecorded` if not supplied; never fabricate);
- commission, target, authority, and decision criteria;
- source-read ledger with file paths and line references for load-bearing claims;
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`;
- findings first, ordered `critical`, `major`, `minor`;
- for every actionable finding: `minimum_closure_condition` and `next_authorized_action`;
- explicit answer to each attack question;
- non-findings for material checks that held;
- review-use boundary.

Severity labels are finding-priority labels only. They do not create approval, rejection, validation, readiness, mandatory remediation, implementation authority, or patch authority.

Do not include `patch_queue_entry`. This is a read-only adversarial artifact review.

After successfully writing the report, return only the compact `review_summary` YAML from `.agents/workflow-overlay/communication-style.md` with `status: completed` and the report path. If report writing fails, return the failed review-summary shape with `review_location: chat_only_current_thread`; do not pretend chat is the durable report.

## Review-Use Boundary

This review is decision input only. It is not approval, validation, readiness, mandatory remediation, implementation authorization, or executor-ready patch authority. The Chief Architect must separately accept or reject its findings before fused implementation resumes.
