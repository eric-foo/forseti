# Bronze Source Surface Projection Live Convergence Adversarial Code Review Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Delegated adversarial code review-and-patch commission for PR #508's Bronze
  source-surface downstream projection proof and the subsequent real-lake
  convergence evidence.
use_when:
  - Commissioning de-correlated review of the merged Bronze source-surface projection consumption path.
  - Checking whether live projection from the real Bronze catalog should be trusted before building derived/Silver retrieval indexes on top.
authority_boundary: retrieval_only
branch_or_commit: PR #508 head e9376ff9a6fe7065ef416de19f28f16f1b606800; GitHub merge commit observed c7743f7222c53784116a110ebbae79f75c7c25fa
downstream_consumers:
  - docs/review-outputs/bronze_source_surface_projection_live_convergence_adversarial_code_review_patch_v0.md
stale_if:
  - PR #508 is reverted or amended.
  - Any target file changes after the pinned hashes below.
  - The real-lake projection run is repeated with a different prefix or the cited derived records are moved/deleted.
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated below.

```yaml
orca_start_preflight:
  agents_read: yes_supplied_in_current_task_context
  overlay_read: yes_loaded_by_dispatcher
  source_pack: custom_S0_plus_pr508_code_and_live_operation_evidence
  repo_map_decision: not_loaded_for_this_prompt
  repo_map_reason: >
    The task is a pinned code path plus live operation evidence review; repo-map
    navigation is not a target unless the reviewer discovers a retrievability
    placement issue.
  authorization_basis: >
    Owner asked whether to delegate review patch for the previous steps and said
    to proceed with next material steps. Bounded review-and-patch is authorized
    for the submitted code/test scope only. Real-lake files are evidence-only and
    must not be edited, regenerated, deleted, or mutated by this commission.
  objective: >
    Determine whether Bronze source-surface catalog consumption now gives a
    reliable downstream lane path from generated Bronze catalog rows plus typed
    Attachment Record rows to append-only IG reels-grid projection records, and
    harden the code/tests if the reviewer finds bounded defects.
  intended_decision: >
    Give the home model a de-correlated review result and any bounded diff to
    adjudicate before the next material step: building a stable derived/Silver
    retrieval index over the appended projection records.
  edit_permission: patch-only
  reviewer_patch_scope:
    may_edit:
      - orca-harness/data_lake/catalog.py
      - orca-harness/source_capture/ig_reels_grid_projection.py
      - orca-harness/runners/run_ig_reels_grid_projection.py
      - orca-harness/tests/test_data_lake_catalog.py
      - orca-harness/tests/unit/test_source_capture_ig_reels_projection.py
    may_write_report: docs/review-outputs/bronze_source_surface_projection_live_convergence_adversarial_code_review_patch_v0.md
    must_not_edit:
      - F:/orca-data-lake/**
      - docs/prompts/reviews/bronze_source_surface_projection_live_convergence_adversarial_code_review_patch_prompt_v0.md
      - off-scope product doctrine, overlay, repo map, unrelated runners, unrelated tests, generated catalog files, or generated derived records
  output_mode: file-write
  delivery_copy: paste-ready-chat copy may be used after this filed prompt artifact exists
  reviewer_output_mode: review-report plus optional uncommitted bounded working-tree diff
  target_scope:
    code_diff_range:
      base: 86d7686a45609a4f67132b4c07b5bb30b5a9ff68
      head: e9376ff9a6fe7065ef416de19f28f16f1b606800
      merged_pr: https://github.com/eric-foo/orca/pull/508
      github_merge_commit_observed: c7743f7222c53784116a110ebbae79f75c7c25fa
      local_merge_commit_status: not_present_in_dispatcher_local_object_database
    implementation_targets:
      - C:/Users/vmon7/Desktop/projects/orca/worktrees/bronze-projection-review-commission/orca-harness/data_lake/catalog.py
      - C:/Users/vmon7/Desktop/projects/orca/worktrees/bronze-projection-review-commission/orca-harness/source_capture/ig_reels_grid_projection.py
      - C:/Users/vmon7/Desktop/projects/orca/worktrees/bronze-projection-review-commission/orca-harness/runners/run_ig_reels_grid_projection.py
      - C:/Users/vmon7/Desktop/projects/orca/worktrees/bronze-projection-review-commission/orca-harness/tests/test_data_lake_catalog.py
      - C:/Users/vmon7/Desktop/projects/orca/worktrees/bronze-projection-review-commission/orca-harness/tests/unit/test_source_capture_ig_reels_projection.py
    evidence_only_external_lake_root: F:/orca-data-lake
  dirty_state_checked: yes_by_dispatcher
  dirty_state_allowance: >
    Review the pinned target files and PR diff only. Root checkout has unrelated
    dirty/untracked files and is out of scope. This prompt was authored in an
    isolated worktree at C:/Users/vmon7/Desktop/projects/orca/worktrees/bronze-projection-review-commission.
  controlling_source_state: >
    Target code/test files are clean at PR #508 head e9376ff9 before this prompt
    artifact is added; this prompt branch adds only this review prompt unless
    the receiving reviewer creates an uncommitted bounded patch.
  required_review_report_path: docs/review-outputs/bronze_source_surface_projection_live_convergence_adversarial_code_review_patch_v0.md in the receiving review worktree
  doctrine_change_decision: no doctrine change requested; review-and-patch prompt only
  isolation_decision: >
    Branch/worktree off PR #508 head because root checkout is dirty and PR #508 is
    already merged. The review prompt itself is a separate docs work unit.
  thread_operating_target_continuity:
    carried_forward: no
    reason: no_visible_active_target
    changed_from_input: no
    lifecycle_status: not_applicable
    if_changed_reason: not_applicable
  validation_gates:
    - Verify target hash pins before reviewing.
    - Inspect PR #508 diff and merged target files.
    - If repo execution is available, rerun the focused tests named below.
    - If a patch is produced, rerun the focused tests and diff checks or state why not run.
  blocked_if_missing:
    - Any target file is unavailable or hash mismatches.
    - Reviewer cannot distinguish generated Bronze catalog read state from raw-packet authority.
    - Reviewer cannot keep real-lake files read-only.
    - Reviewer cannot invoke or apply workflow-code-review after source context is ready.
```

## Lane Binding

```yaml
overlay_status: bound
operating_contract_pointer:
  - AGENTS.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
review_lane: code (workflow-code-review)
mode: base-subagent
actor_model_family_receipt:
  author_home_model_family: OpenAI/Codex
  controller_model_family: receiving_reviewer_to_record_must_differ_from_author_for_decorrelated_claim
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: blocked_until_receiving_reviewer_records_different_vendor_or_family
de_correlation: >
  The controller must be a different vendor or family than the author/home model
  to claim de-correlated review. This is a who-constraint, not a model
  recommendation. If the receipt is missing, inconsistent, or same-family, return
  the review as non-de-correlated or stop with the nearest receipt blocker.
subagent_authority: >
  No tester/testee shortcut. The authoring or adjudicating model must not satisfy
  this by reviewing its own work. The receiving controller reviews in its own lane.
prompt_rendering: >
  This filed prompt is the orchestrated prompt artifact. Do not substitute a
  summary, context pack, alternate checkout, or recreated-source review for
  inspecting the pinned repo/worktree source.
```

## Commission

Run a delegated adversarial code review-and-patch pass over PR #508's merged
Bronze source-surface projection consumption path and the dispatcher-observed
real-lake convergence evidence.

The code target is patchable only inside `reviewer_patch_scope.may_edit`. The
real lake at `F:/orca-data-lake`, generated Bronze catalog files, and the two
appended derived projection records are evidence-only. You may read them if your
runtime has access. You must not mutate them.

The home model / Chief Architect adjudicates every finding and every diff hunk
before anything is kept. Your diff, citations, and verdict are claims to
adjudicate, not premises to inherit. If the correct fix is architectural,
off-scope, or requires changing the real-lake operation contract, return
`NEEDS_ARCHITECTURE_PASS` or an off-scope flag rather than patching around it.

Fitness reference:

- Goal: make Bronze powerful enough that downstream projection/Silver lanes can
  discover and consume source-family/source-surface evidence through generated
  catalog rows and typed AR entries without path guessing.
- Done looks like: the review either confirms or hardens the code path that
  turned a clean Bronze catalog into two append-only IG reels-grid projection
  records, while preserving view-only/non-judgment semantics and real-lake
  write boundaries.

## Method Order

REFERENCE-LOAD these methods first. Do not APPLY them yet:

- `C:/Users/vmon7/.codex/plugins/cache/agent-workflow-local/agent-workflow/0.1.87/skills/workflow-deep-thinking/SKILL.md`
- `C:/Users/vmon7/.codex/plugins/cache/agent-workflow-local/agent-workflow/0.1.87/skills/workflow-code-review/SKILL.md`
- `C:/Users/vmon7/.codex/plugins/cache/agent-workflow-local/agent-workflow/0.1.87/skills/workflow-delegated-review-patch/SKILL.md`

Then SOURCE-LOAD the target files, the PR #508 diff range, the operation
evidence below, and any controlling overlay files needed to resolve review-output
or patch boundaries. Declare either `SOURCE_CONTEXT_READY` or
`SOURCE_CONTEXT_INCOMPLETE` with missing sources and material gaps. Only after
that declaration, APPLY `workflow-deep-thinking` to frame failure modes, then
APPLY `workflow-code-review` for findings-first review and bounded patching.

## Target Hash Pins

Verify these SHA256 pins before review:

```text
1F790C9AF36BFF368F47D2B71F7BF9F3201A6AF22BAEF24272C228615EF02559  orca-harness/data_lake/catalog.py
158362061F5EEA05EA7C402ABAE86AF50F72740E7F15AB5DB3035F008EABFE04  orca-harness/source_capture/ig_reels_grid_projection.py
4F355F224C87E40D03FA4C3C111C47732CBA6284BA87A4A8770466243F450FAE  orca-harness/runners/run_ig_reels_grid_projection.py
D2B179D0E9755332ADFCAECD343C7C85E10E878537F5A72147221193C2BA01BE  orca-harness/tests/test_data_lake_catalog.py
2AFFC8A52B2EBAC403462B048DE7C082AE16C9886667555D0195812EF4A66874  orca-harness/tests/unit/test_source_capture_ig_reels_projection.py
```

If any hash mismatches, stop with `HASH_MISMATCH` and list the mismatched path,
expected hash, actual hash, and nearest allowed next step.

## Dispatcher-Observed Live Operation Evidence

Treat this as evidence to verify or inspect, not as a formal validation claim.

1. PR #508 state observed through GitHub:
   - URL: `https://github.com/eric-foo/orca/pull/508`
   - state: `MERGED`
   - base: `codex/bronze-v41-clean-verify`
   - head: `e9376ff9a6fe7065ef416de19f28f16f1b606800`
   - merge commit: `c7743f7222c53784116a110ebbae79f75c7c25fa`
   - CI: `orca-harness-tests` passed in `1m35s`
2. Before live projection, real catalog census was stale:
   - status/catalog_status: `issues_found`
   - expected packets: `101`
   - indexed packets: `99`
   - expected generated AR rows: `222`
   - indexed generated AR rows: `216`
   - issue counts included `missing_files=22`, `missing_packets=2`, `stale_files=17`
3. Dispatcher rebuilt the generated catalog:
   - command shape: `python orca-harness/runners/run_data_lake_catalog.py --data-root F:/orca-data-lake --rebuild`
   - result: `status=rebuilt`, `packet_count=101`, `attachment_record_count=222`, `source_surface_count=7`, `file_count=1016`
4. Fresh census after rebuild was clean:
   - status/catalog_status: `ok`
   - expected/indexed packets: `101/101`
   - expected/indexed generated AR rows: `222/222`
   - source surfaces: `7`
   - missing/stale/orphan/read-failure counts: all `0`
5. Live projection command:
   - `python orca-harness/runners/run_ig_reels_grid_projection.py --data-root F:/orca-data-lake --bronze-source-surface --record-id-prefix bronze_catalog_ig_reels_grid_20260630_run1`
6. Projection output paths:
   - `F:/orca-data-lake/derived/ddd/01KW9T6R7BFDJKG7WSW7PMVSMP/projection_ig_reels_grid/bronze_catalog_ig_reels_grid_20260630_run1_0001.json`
   - `F:/orca-data-lake/derived/f00/01KWA193403TYNTBJVWAP5W5NE/projection_ig_reels_grid/bronze_catalog_ig_reels_grid_20260630_run1_0002.json`
7. Fresh-read derived record summaries:
   - `0001`: packet `01KW9T6R7BFDJKG7WSW7PMVSMP`, username `hyram`, row count `10`, certification `view_only; not_cleaned; not_normalized; not_judgment_ready`, SHA256 `2B629ABA95D39E7CB6DB1B440F75B6BF2CF776AA50272CF74E43DADF940267EC`
   - `0002`: packet `01KWA193403TYNTBJVWAP5W5NE`, username `jeremyfragrance`, row count `37`, certification `view_only; not_cleaned; not_normalized; not_judgment_ready`, SHA256 `730A8159FAE025C24E1579FA48841C2AD71A9C46FABA92E3479149306047DA52`
8. Projection record count under `projection_ig_reels_grid` moved from `6` to `8`.
9. Post-run catalog census remained clean:
   - status/catalog_status: `ok`
   - expected/indexed packets: `101/101`
   - expected/indexed generated AR rows: `222/222`
   - source surfaces: `7`
   - missing/stale/orphan/read-failure counts: all `0`

## Review Axes To Attack

Focus on concrete correctness, retrievability, operational safety, schema, and
test durability failures. In particular, inspect:

- Whether `source_surface_catalog_rows` fail-closes on stale generated catalogs
  strongly enough for downstream lanes, and whether the live stale-catalog event
  exposed a missing runner preflight, rebuild affordance, or clearer operator
  failure path.
- Whether downstream code resolves packet rows and full Attachment Record rows
  from generated catalog query paths instead of reimplementing private safe-name
  rules, raw directory layout, positional `file_id` inheritance, or body-path
  guessing.
- Whether `project_ig_reels_grid_from_bronze_catalog` correctly groups AR rows
  by packet, loads body bytes through the AR body resolver, handles missing,
  duplicate, or extra AR rows, and fails with actionable errors.
- Whether the runner's `--bronze-source-surface`, `--packet-id`, and `--packet`
  modes reject incompatible flags and preserve stdout/output behavior.
- Whether explicit `record_id_prefix` is sufficient for live operational
  traceability and rerun safety, or whether the code should expose stronger
  idempotence/collision/error messaging.
- Whether the appended projection records preserve the projection lane's
  mechanical/view-only semantics and avoid Cleaning, Judgment, normalization,
  traction, or certification overclaim.
- Whether repeated live projection on a clean catalog creates expected
  append-only records or surprising duplicates, and whether that behavior is
  documented/tested enough for the next derived/Silver retrieval index.
- Whether post-run catalog cleanliness is expected because the Bronze catalog is
  raw-derived only, and whether any user/operator could mistakenly expect it to
  index derived projection outputs.
- Whether tests cover stale catalog refusal, generated query-path consumption,
  AR-row expansion, runner CLI branching, and multi-packet projection from a
  source surface.
- Whether the code is ready to support future source families without adding
  lake-core fields just because one source family needs a custom identifier.

## Validation Evidence To Inspect

Dispatcher-observed validation before PR #508 was opened:

```powershell
python -m py_compile orca-harness/data_lake/catalog.py orca-harness/source_capture/ig_reels_grid_projection.py orca-harness/runners/run_ig_reels_grid_projection.py
python -m pytest orca-harness/tests/test_data_lake_catalog.py orca-harness/tests/unit/test_source_capture_ig_reels_projection.py --no-header --no-summary
git diff --check
python .agents/hooks/header_index.py --strict
python .agents/hooks/check_map_links.py --strict
```

Observed result summary:

```text
py_compile: passed
focused pytest: 45 passed, 1 skipped in 6.14s
git diff --check: clean except expected LF->CRLF warnings during checkout-sensitive output
header_index.py --strict: OK
check_map_links.py --strict: OK
PR #508 GitHub CI: orca-harness-tests passed in 1m35s
```

If you have repo execution access, rerun at least:

```powershell
python -m py_compile orca-harness/data_lake/catalog.py orca-harness/source_capture/ig_reels_grid_projection.py orca-harness/runners/run_ig_reels_grid_projection.py
python -m pytest orca-harness/tests/test_data_lake_catalog.py orca-harness/tests/unit/test_source_capture_ig_reels_projection.py --no-header --no-summary
git diff --check
```

If you produce a patch, rerun the focused tests and diff checks after patching.
If you cannot run them, report `validation_not_run` with the reason.

Do not rerun the live projection command unless the owner separately authorizes a
new external-lake mutation. Reading the two cited files, counting records, or
running read-only catalog census is allowed only if your runtime has access and
you keep `F:/orca-data-lake` read-only.

## Output Contract

Write the durable review report to:

`docs/review-outputs/bronze_source_surface_projection_live_convergence_adversarial_code_review_patch_v0.md`

If filesystem write is unavailable, return the same findings-first report in
chat and set `review_location: chat_only_current_thread`. Do not claim chat is
equivalent to a missing durable report.

Report findings first, ordered by materiality. Each finding must include:

- `finding_id`
- commissioned target and purpose
- file and line or stable structural anchor
- implementation or operation evidence
- authority or evidence basis
- correctness, retrieval, operation-safety, validation, schema, or review-confidence impact
- `minimum_closure_condition`
- `next_authorized_action`
- verification expectation
- whether a bounded patch was applied

Also include:

- source-read ledger
- actor/model-family receipt and de-correlation status
- target hash verification table
- validation run status
- patch summary and unified diff if a patch was applied
- off-scope flags
- open questions
- residual risk
- review-use boundary: findings and diffs are decision input only; they are not
  approval, validation, readiness, mandatory remediation, source promotion, or
  executor-ready merge authority until separately accepted or authorized

Use these provenance fields in the durable report or chat output:

```yaml
reviewed_by: operator_or_reviewer_to_fill_or_unrecorded
authored_by: OpenAI/Codex
de_correlation_bar: operator_to_fill_cross_vendor_discovery_same_vendor_sanity_self_fallback_or_unrecorded
same_vendor_rationale: not_applicable_unless_same_vendor_sanity_is_claimed
```

Close with this courier block so the home model can adjudicate later:

```text
DELEGATED_CODE_REVIEW_PATCH_RETURN_FOR_HOME_MODEL

Here is the delegated code review-and-patch result. Adjudicate it under the delegated-review-patch return contract.

Include:
- original commission or review target
- implementation context, diff, and reviewed files
- live operation evidence inspected and any external-lake read-only verification
- findings and implementation evidence
- proposed patch, working-tree diff, or exact requested edits
- citations
- reviewer verdict or recommendation, if the review lane binds one
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
```

For this prompt, real-lake mutation, formal approval, readiness, validation
pass/fail, source promotion, and merge authority are `NOT_CLAIMED`.
