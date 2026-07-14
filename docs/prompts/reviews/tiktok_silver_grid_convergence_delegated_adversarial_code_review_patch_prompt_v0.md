# TikTok Silver Grid Convergence Delegated Adversarial Code Review And Patch

```yaml
retrieval_header_version: 1
artifact_role: Forseti delegated code review-and-patch prompt
scope: >
  Cross-vendor adversarial review and bounded patching of the TikTok Silver
  grid-authority convergence implementation at commit b5973fa8.
use_when:
  - Reviewing the TikTok grid source-surface fence and legacy writer retirement.
  - Hardening the named implementation diff before Chief Architect adjudication.
authority_boundary: retrieval_only
```

## What This Is For

**Goal:** leave TikTok with one automatic, deterministic Silver grid-history
writer and no competing batch metric writer.

**Done looks like:** only declared grid-window Bronze packets derive grid Silver;
batch/deep-capture packets are not applicable even when they embed the same grid
artifact; malformed declared-grid packets fail unacknowledged; replay is
idempotent; exact history reads remain lineage- and policy-checked; the retired
writer has no live imports or inventory registration; focused and full tests
remain green.

Treat this goal and success signal as the review axis to attack, not a pass bar.

## Commission And Preflight

```yaml
forseti_start_preflight:
  agents_read: required
  overlay_read: required
  source_pack: bounded_custom_code_diff
  repo_map_decision: not_needed
  repo_map_reason: named implementation diff and owning seams are explicit
  workspace: C:/Users/vmon7/.codex/worktrees/f75f/orca
  expected_branch: codex/tiktok-silver-grid-convergence
  required_ancestry: b5973fa8
  implementation_commit: b5973fa8
  receiver_mechanism: operator-couriered independent controller
  receiver_write_root: operator_to_fill_and_verify_matches_workspace
  dirty_state_allowance: clean at start; reviewer-created named-scope edits only thereafter
  untracked_files_in_scope: no
  edit_permission: patch-only
  output_mode: chat-only
  target_kind: delegated_code_review_and_patch
  access: repo
  source_hierarchy: AGENTS.md -> Forseti overlay -> accepted plan/current code -> historical reports
  external_source_boundary: jb and external workflow sources are not Forseti authority
```

Before loading review sources:

1. Record the controller identity and vendor/model lineage. The author/home
   family is OpenAI. The controller must be a different vendor/model lineage;
   otherwise return `BLOCKED_CONTROLLER_NOT_DECORRELATED` without reviewing or
   patching. This is a who-constraint, not a runtime-model recommendation.
2. Confirm the current receiving actor is the independent `controller`, not the
   home dispatcher or a mechanical executor. Do not launch another reviewer.
3. Confirm the actual writable workspace is
   `C:/Users/vmon7/.codex/worktrees/f75f/orca`, the branch is
   `codex/tiktok-silver-grid-convergence`, and `b5973fa8` is an ancestor of
   `HEAD`. Confirm no implementation target changed after `b5973fa8` before
   reviewing. If the receiver cannot actually write this root, return
   `BLOCKED_RECEIVER_REROOT_REQUIRED`; discovering the path is not capability
   proof.
4. Require a clean worktree at start. Do not stash, reset, clean, switch branch,
   substitute another checkout, or review a summary/context pack instead.

## Required Reads And Method

Read before findings:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/delegated-review-patch.md`: “When it applies”, “The
  loop”, “Access selection rule”, “De-correlation”, “Code-diff target kind”, and
  “Overlay Interface”
- `.agents/workflow-overlay/review-lanes.md`
- the complete `workflow-code-review` skill instructions available to the
  controller runtime
- `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md` ->
  `environment_baseline`
- the complete `main...b5973fa8` diff and every named target below
- directly called production seams needed to verify a finding, especially the
  Bronze packet writer/manifest grammar, Silver record writer, consumption ack
  seam, and exact-policy history reader

REFERENCE-LOAD the code-review method before reviewing. Do not APPLY it until
the real target diff and required sources are loaded. Then declare
`SOURCE_CONTEXT_READY` or return `SOURCE_CONTEXT_INCOMPLETE` with the exact
missing source. After readiness, APPLY `workflow-code-review` findings-first.
If the review lane is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` and
do not patch.

## Named Patch Scope

Only these implementation targets may be patched. Deleted targets are included
so a finding may explicitly justify restoration; the accepted retirement
direction must not otherwise be reopened.

- `[grid-runner]` `forseti-harness/runners/run_tiktok_grid_observation_producer.py`
- `[grid-test]` `forseti-harness/tests/unit/test_tiktok_grid_observation_producer.py`
- `[test-support]` `forseti-harness/tests/unit/tiktok_batch_test_support.py`
- `[comment-test]` `forseti-harness/tests/unit/test_tiktok_comment_attention_producer.py`
- `[audience-test]` `forseti-harness/tests/unit/test_tiktok_audience_evidence_extract.py`
- `[product-test]` `forseti-harness/tests/unit/test_tiktok_product_extract.py`
- `[inventory-test]` `forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`
- `[inventory]` `forseti-harness/data_lake/lake_touchpoint_inventory_v0.json`
- `[followon]` `docs/workflows/social_grid_longitudinal_followon_v0.md`
- `[retired-runner]` `forseti-harness/runners/run_tiktok_batch_metric_rollup_producer.py` (deleted)
- `[retired-seed]` `forseti-harness/capture_spine/creator_profile_current/tiktok_metric_seed.py` (deleted)
- `[retired-producer]` `forseti-harness/capture_spine/creator_profile_current/tiktok_silver_metric_producer.py` (deleted)
- `[retired-runner-test]` `forseti-harness/tests/unit/test_tiktok_batch_metric_rollup_producer_runner.py` (deleted)
- `[retired-seed-test]` `forseti-harness/tests/unit/test_tiktok_creator_metric_seed.py` (deleted)
- `[retired-producer-test]` `forseti-harness/tests/unit/test_tiktok_creator_metric_silver_producer.py` (deleted)

Everything else is read-only and flag-only. Do not edit this prompt, overlay,
AGENTS.md, CI, hooks, schemas, other platform producers, live data, or historical
review/test reports. A necessary fix outside the named set requires
re-commissioning; do not widen scope yourself.

Read-only review is insufficient because this commission explicitly authorizes
the de-correlated controller to close confirmed bounded defects in the named
implementation while its source context is hot. Patch only findings you can
support with neutral, decision-sufficient citations.

## Review Questions

Coverage-first, report every issue found with severity and confidence:

1. Does source-surface selection happen before filename discovery, so an
   embedded batch copy can never derive grid Silver?
2. Does the numbered `raw/NN_<name>` recovery accept only the canonical staged
   `tiktok_grid_window.json` name and reject suffix lookalikes?
3. Does a declared grid packet missing, duplicating, corrupting, or incompletely
   carrying its required grid artifact fail without acknowledgement?
4. Are deterministic ID, policy fingerprint, lineage, byte readback,
   missing-versus-zero posture, exact reader selection, equal-time ambiguity,
   and completion-before-ack semantics preserved?
5. Does retirement remove only the obsolete TikTok batch metric/rollup writer
   while preserving batch Bronze capture, comments, transcript/product,
   audience, historical immutable records, and generic historical
   revalidation/reading?
6. Is the extracted test fixture neutral, minimal, and faithful enough that the
   surviving consumer tests cannot fake success?
7. Do inventory and current longitudinal documentation match the resulting
   executable surface without rewriting point-in-time historical reports?
8. Did the patch accidentally introduce a creator summary, aggregation cadence,
   policy/schema migration, data rewrite, SQL/index surface, live-lake write, or
   other deferred analytics?

## Validation

Run from the commissioned worktree. Use the repository environment baseline.
Every command may fail; report its exact result. Do not mask failures or weaken
assertions to obtain green.

```powershell
$env:PYTHONDONTWRITEBYTECODE=1
python -m pytest -p no:cacheprovider --basetemp "$env:TEMP\pytest_tiktok_silver_review_focus" forseti-harness/tests/unit/test_tiktok_grid_observation_producer.py forseti-harness/tests/unit/test_tiktok_comment_attention_producer.py forseti-harness/tests/unit/test_tiktok_audience_evidence_extract.py forseti-harness/tests/unit/test_tiktok_product_extract.py forseti-harness/tests/contract/test_capture_runner_lake_seam_coverage.py -q
python -m pytest -p no:cacheprovider --basetemp "$env:TEMP\pytest_tiktok_silver_review_contracts" forseti-harness/tests/unit/test_seam_cadence.py forseti-harness/tests/contract/test_seam_cadence_coverage.py forseti-harness/tests/contract/test_data_lake_inventory_gate.py forseti-harness/tests/contract/test_silver_reader_selection_gate.py forseti-harness/tests/unit/test_silver_lane_registry_guard.py -q
python -m pytest -p no:cacheprovider -n 4 --dist=loadfile --basetemp "$env:TEMP\pytest_tiktok_silver_review_full" forseti-harness/tests -q
git diff --check
```

The implementation author observed: focused suite exit 0, cadence/inventory/
reader-selection/registry suite exit 0, durable mixed-packet dogfood test exit
0, and full harness suite exit 0. Treat these as evidence to independently
reproduce, not as a substitute for review validation.

## Controller Return And Hard Stops

Return findings first. Each actionable finding must include:

- target label and tight `file:line` citation;
- severity (`critical`, `major`, or `minor`) and confidence (`high`, `medium`,
  or `low`);
- concrete failure mechanism and affected behavior;
- `minimum_closure_condition` as the required end state;
- `next_authorized_action` inside the named scope;
- the bounded patch applied, if any.

Also return:

- `considered_and_defended` for steelman-defeated candidates;
- one unified diff covering controller-authored changes, labeled by target;
- neutral, decision-sufficient source citations for every change;
- validation commands and observed results, including failures or not-run gates;
- overall verdict and per-target sub-verdicts where materially different;
- residual risks and off-scope flags;
- `reviewed_by` and `authored_by` provenance values, using `unrecorded` rather
  than fabricating unavailable facts.

If a design-level problem prevents a bounded fix, return
`NEEDS_ARCHITECTURE_PASS`, revert any partial controller diff, and return
findings only.

The controller may edit only the named patch scope. Do not commit, push, open or
update a PR, merge, stash, reset, clean the worktree, run repository hygiene, or
perform any other lifecycle action.

The returned findings, diff, citations, verdict, and residuals are claims for
the home/Chief Architect to adjudicate, not premises to keep. The Chief
Architect must accept, modify, or reject every material change against its
citations, close self-closable issues in the adjudication turn, and keep no
controller patch by inertia. After material closure, the Chief Architect owns
one batched land step and the goal-conditioned next-move check required by
`.agents/workflow-overlay/communication-style.md` -> “Review Adjudication Next
Step”.
