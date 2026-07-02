# Bronze Full-GT Fused Batch Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review prompt
scope: >
  De-correlated adversarial code review prompt for the Bronze full-GT fused
  batch implementation diff: inventory gate, ambiguous Attachment-Record branch
  pin, and materially different raw-body join threshold.
use_when:
  - Dispatching an independent reviewer/controller to review the implementation
    branch for the Bronze full-GT fused batch.
authority_boundary: retrieval_only
```

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

## Orca Prompt Preflight

- authorization_basis: Current owner instruction on 2026-07-01: proceed fused batch; remember delegated review-patch after.
- objective / intended_decision: Decide whether the implementation diff correctly hardens the next Bronze full-GT gates without selecting storage architecture or claiming readiness.
- fitness_reference: Done means future changes trip deterministic tests when they add/remove non-raw lake touchpoints, collapse YouTube ambiguous Attachment-Record lineage into a winning record, or weaken the materially different raw-body join threshold.
- target_files_or_dirs:
  - `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
  - `orca-harness/tests/unit/test_youtube_creator_metric_silver_producer.py`
  - `orca-harness/tests/unit/test_tiktok_batch_projection.py`
- source_pack / bounded_reads:
  - `AGENTS.md`
  - `.agents/workflow-overlay/README.md`
  - `.agents/workflow-overlay/source-loading.md`
  - `.agents/workflow-overlay/decision-routing.md`
  - `.agents/workflow-overlay/review-lanes.md`
  - `.agents/workflow-overlay/prompt-orchestration.md`
  - `.agents/workflow-overlay/delegated-review-patch.md`
  - `C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-full-gt-fused-batch`
  - the diff from `origin/main...codex/bronze-full-gt-fused-batch`
  - source implementation files only as needed to verify the changed tests bind real branches.
- repo_map_decision: not_needed
- repo_map_reason: The review target is a bounded implementation/test diff with explicit files; repo map conflict resolution was already completed in prior PR closeout and no map edit is in this diff.
- output_mode: review-report
- review_output_destination: `docs/review-outputs/bronze_full_gt_fused_batch_adversarial_code_review_v0.md`
- edit_permission: patch-only
- patch_authority: >
  You may patch only the three target files named above. Do not edit runtime
  implementation files, overlay files, prompt files, product docs, CI config, or
  the temporary material-decision packet. If the correct fix requires those
  files, return an off-scope finding instead.
- dirty_state_allowance: Branch may contain only this implementation prompt and the three target test-file changes. Any other dirty or untracked source change is out of scope unless the dispatcher explicitly names it.
- controlling_source_state: Check locally before review. If overlay, prompt-policy, review-lane, or validation-gate files are modified in the review worktree, block strict claims and name the mismatch.
- branch_or_commit_reference: `codex/bronze-full-gt-fused-batch`; base `origin/main` at or after `3fe6a189dfe640419fde7fdee616db6b9571cfa4`. Confirm the PR head or dispatcher-provided head SHA before reviewing.
- doctrine_change_decision: No doctrine change is authorized. This is implementation/test hardening only.
- isolation_decision: Worktree off `main`, because the work runs alongside other active lanes and PRs.
- validation_gates:
  - `python -m pytest -q orca-harness\tests\contract\test_capture_runner_lake_seam_coverage.py`
  - `python -m pytest -q orca-harness\tests\unit\test_youtube_creator_metric_silver_producer.py`
  - `python -m pytest -q orca-harness\tests\unit\test_tiktok_batch_projection.py`
  - from `orca-harness`, with `ORCA_DATA_ROOT` unset: `python -m pytest -q`
  - `python .agents\hooks\check_map_links.py --strict`
  - `python .agents\hooks\header_index.py --strict`
  - `python .agents\hooks\check_csb_scanning_artifact.py --diff origin/main --strict`
  - `python .agents\hooks\check_ontology_ssot.py --strict`
  - `python .agents\hooks\check_ontology_tag_validity.py --strict`
  - `python .agents\hooks\check_ontology_drift.py --strict`
  - `python .agents\hooks\check_deletion_evidence.py --strict`
  - `python .agents\hooks\check_dcp_receipt.py --strict`
  - `python .agents\hooks\check_silver_lane_registry.py --strict`
  - `git diff --check`
- thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  lifecycle_status: not_applicable

## Dispatch Contract

You are the independent receiving controller for this review. This is a who-constraint, not a runtime model recommendation:

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI / GPT-family Codex
  controller_model_family: operator_to_fill
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: satisfied_only_if_controller_vendor_differs_from_author
de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback
same_vendor_rationale: required_if_de_correlation_bar_is_same_vendor_sanity
```

If your controller family is the same vendor/family as the author, you may run only `same_vendor_sanity`; do not claim cross-vendor discovery, no-new-seam coverage, or delegated-review-patch completion. If your controller family is unknown or cannot be recorded, return `BLOCKED_CONTROLLER_NOT_DECORRELATED` for cross-vendor claims.

REFERENCE-LOAD these methods before source loading. Do not APPLY them until `SOURCE_CONTEXT_READY`:

- `workflow-deep-thinking`
- `workflow-code-review`

Then SOURCE-LOAD the bounded sources above. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, source gaps, excluded sources, and conflicts. Only after that declaration, APPLY the methods and perform the review.

## Review Purpose

Review the implementation diff adversarially for these failure modes:

- Batch A inventory gate is too brittle, too broad, or overclaims a Manifest v2 / manifest-equivalent decision.
- The non-raw lake touchpoint inventory misses a real writer/non-raw-touchpoint class or treats tests/generated scratch as runtime surface.
- The YouTube ambiguous Attachment-Record test does not actually pin the ambiguous branch, or lets the producer silently choose one record.
- The TikTok raw-body join threshold test does not materially differ from existing YouTube proof, or accidentally claims a third Silver proof.
- The diff selects or pressures architecture on AR body layout/backend, retention, lawful erasure, storage backend lock-in, Manifest v2, or manifest-equivalent indexing.
- The diff claims Bronze full-GT readiness, validation, buyer proof, runtime proof, or production safety.

## Non-Claims To Preserve

- No Manifest v2 or manifest-equivalent index is selected.
- No AR physicalization layout or backend is selected.
- No retention, lawful-erasure, or backend lock-in decision is made.
- No third proof is started or claimed.
- No Bronze full-GT readiness, validation, deployment readiness, or buyer-proof claim is made.
- The temporary material-decision packet from the planning lane is not permanent architecture authority; it is slated for closeout/supersession after this implementation path is adjudicated.

## Patch Boundary

If you find a blocker or major issue that can be fixed within the three target files, you may patch those files directly. Leave changes unstaged and uncommitted. Include a unified diff in the durable report.

Do not stage, commit, push, merge, close PRs, alter branch protection, change CI, edit product/decision artifacts, or edit implementation/runtime files. If the right fix is outside the target files, return `NEEDS_ARCHITECTURE_PASS` or an off-scope finding instead of patching around it.

## Required Output

Write the full durable review report to:

`docs/review-outputs/bronze_full_gt_fused_batch_adversarial_code_review_v0.md`

The report must be findings-first. Include:

- `reviewed_by` and `authored_by`; use `unrecorded` only if the operator/tooling did not supply the real value.
- `de_correlation_bar` and any required same-vendor rationale.
- source-read ledger with one line per source.
- branch/head checked and dirty-state result.
- findings with location, evidence, impact, `minimum_closure_condition`, and `next_authorized_action`.
- any patch diff, with citations for why each hunk is inside scope.
- validation run/not-run evidence after any patch. If you do not patch, rerun only the focused tests you need for confidence or state `not_run` with rationale.
- `DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL` courier block for later CA adjudication.

After a successful report write, return a compact summary plus courier YAML with `report_path`, finding ids, patch status, validation evidence, residual risk, and next authorized action. The review and any patch are decision input only; the home/CA model adjudicates what is kept.
