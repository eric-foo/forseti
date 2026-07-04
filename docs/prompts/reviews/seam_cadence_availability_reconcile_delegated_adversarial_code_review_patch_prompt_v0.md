# Seam Cadence Availability Reconcile Delegated Adversarial Code Review Patch Prompt (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt draft (delegated_code_review_and_patch; repo-mode code review)
scope: >
  Lane-scoped delegated adversarial code review-and-patch prompt for the
  availability reconcile concurrency hardening diff on branch
  codex/seam-cadence-availability-reconcile-investigation.
use_when:
  - Commissioning an independent de-correlated reviewer to inspect and, if needed,
    patch the availability reconcile lock hardening on this lane.
  - Checking review-routing disposition for the seam cadence concurrent access fix.
authority_boundary: retrieval_only
branch_or_commit: codex/seam-cadence-availability-reconcile-investigation @ 0d9f2a2c
stale_if:
  - The branch head changes after 0d9f2a2c before the review starts.
  - The target files or validation evidence listed below change before review.
```

## Prompt Preflight

- output_mode: review-report
- template_kind: review; delegated_code_review_and_patch sibling mode
- edit_permission: patch-only for the named target files only if the controller finds a fix inside the bounded patch scope; otherwise read-only findings
- workspace: `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\seam-cadence-availability-reconcile-investigation`
- branch: `codex/seam-cadence-availability-reconcile-investigation`
- base: `origin/main` at `045db1966f24c252d45e0780f744eda8b9586294`
- review_head: `0d9f2a2c`
- dirty_state_allowance: clean checkout of `0d9f2a2c`; if dirty, report `BLOCKED_DIRTY_STATE` before reviewing
- input_prompt_source: `docs/prompts/reviews/seam_cadence_availability_reconcile_delegated_adversarial_code_review_patch_prompt_v0.md`
- required_output_report: `docs/review-outputs/seam_cadence_availability_reconcile_delegated_code_review_v0.md`
- review_routing_status_target: reviewer writes a report; home CA adjudicates findings/diff before keep

## Actor / De-Correlation Receipt

- author_home_model_family: OpenAI / GPT-5 Codex
- current_receiving_actor_role: controller
- dispatch_mode: external-controller-courier
- access: repo
- controller_model_family: operator_to_fill
- de_correlation_status: operator_to_fill

The controller must be a different vendor/model lineage from the author/home family to satisfy the cross-vendor discovery bar. This is a who-constraint, not a model recommendation. If the receiving controller cannot establish de-correlation, return `BLOCKED_CONTROLLER_NOT_DECORRELATED` or explicitly mark the pass as same-vendor sanity only; do not claim cross-vendor discovery.

## Required Method Sequence

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-code-review`. Do not APPLY either method yet.
3. SOURCE-LOAD the task sources listed below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
5. Only after source readiness, APPLY `workflow-deep-thinking` to identify likely failure modes, then APPLY `workflow-code-review` to the pinned diff.

If either method is unavailable in the receiving environment, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not patch.

## Task Objective

Review the shared availability reconcile hardening diff for correctness, failure visibility, Windows/filesystem behavior, and scope control. If you find a blocker/major issue whose smallest complete fix is inside the named target files, patch it in the working tree and include the diff in your report. If the correct fix requires touching any off-scope file or changing the design contract, flag it and do not patch off-scope.

## Target Files And Bounded Patch Scope

Patchable target files:

- `orca-harness/data_lake/consumption.py`
- `orca-harness/tests/test_data_lake_consumption.py`

Bounded patch scope:

- The availability reconcile lock around `reconcile_availability_per_packet`.
- Tests proving concurrent helper calls serialize the destructive rebuild and preserve per-packet failure visibility.
- No runner registry edits, no cadence exit-code changes, no live-lake writes, no schema/data-layout changes, no changes to `DataLakeRoot.rebuild_availability`, and no edits outside the two target files unless returned as off-scope findings.

## Source Context To Inspect

Required source reads:

- `orca-harness/data_lake/consumption.py`
- `orca-harness/tests/test_data_lake_consumption.py`
- `orca-harness/data_lake/root.py` around `record_availability`, `list_available`, and `rebuild_availability`
- `orca-harness/runners/run_seam_cadence.py`
- `orca-harness/tests/contract/test_catchup_runner_seam_coverage.py`

Review the diff from `origin/main...0d9f2a2c` before judging the final file state.

## Validation Evidence Already Run By Author

Treat this as evidence to verify, not as proof to inherit:

- `python -m pytest -p no:cacheprovider -q --basetemp pytest_tmp orca-harness\tests\test_data_lake_consumption.py` -> passed: `................. [100%]`
- `python -m pytest -p no:cacheprovider -q --basetemp pytest_tmp_seam orca-harness\tests\contract\test_catchup_runner_seam_coverage.py orca-harness\tests\contract\test_seam_cadence_coverage.py orca-harness\tests\unit\test_seam_cadence.py` -> passed: `................ [100%]`
- `python -m pytest -p no:cacheprovider -q --basetemp pytest_tmp_catchups ...catchup unit suites...` -> passed: progress reached `[100%]`
- `python -m pytest -p no:cacheprovider -q --basetemp pytest_tmp_full orca-harness\tests` with `ORCA_DATA_ROOT` cleared -> passed, with existing warnings only
- `git diff --check` -> passed

The author did not run `run_seam_cadence.py --run --skip-asr --data-root F:\orca-data-lake`; live-lake execution remains owner-gated and must not be performed by the reviewer unless separately authorized.

## Specific Review Questions

Findings-first. Prioritize blocker/major issues.

1. Does the lock actually serialize the destructive availability rebuild across concurrent OS processes on Windows?
2. Can the lock create a new fake-success, indefinite hang, stale-lock, or hidden failure path?
3. Does the helper still preserve `availability_reconcile_failed` per-packet visibility for corrupt manifests and continue healthy packets?
4. Do the tests genuinely exercise the race class, or can they pass while the original failure remains possible?
5. Is the patch smallest complete, or does it leave a same-class race in the shared seam path that this lane is responsible for?

## Off-Scope / Flag-Only

Flag but do not patch:

- Any change outside the two target files.
- Any change to live `F:\orca-data-lake`.
- Any relaxation of `run_seam_cadence.py` fail-loud semantics.
- Any change to the parfumo blocked-capture fix or its tests.
- Any migration, schema, or broad data-lake redesign.

If the correct fix is off-scope, return `NEEDS_ARCHITECTURE_PASS` or an off-scope finding with the minimum closure condition.

## Required Review Report Shape

Write `docs/review-outputs/seam_cadence_availability_reconcile_delegated_code_review_v0.md` with:

- `reviewed_by: operator_to_fill` and `authored_by: OpenAI / GPT-5 Codex`.
- `de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback` plus rationale when not cross-vendor.
- source context status: `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
- findings first, each with severity, confidence, file/line evidence, and `minimum_closure_condition`.
- `considered_and_defended` for plausible findings you rejected.
- any patch diff you applied, fenced as real unified diff.
- validation you ran and observed output.
- residual risk.
- a final boundary: review findings/diff are decision input only; the home CA adjudicates before keep.

Do not claim approval, readiness, validation proof, mergeability, or no-new-seam unless the stated de-correlation and validation evidence actually support that claim.
