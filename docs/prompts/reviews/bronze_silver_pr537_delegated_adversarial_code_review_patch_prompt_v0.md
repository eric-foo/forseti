# Bronze/Silver PR #537 Delegated Adversarial Code Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (review family; delegated adversarial code review-and-patch commission)
scope: >
  Commission an independent, de-correlated repo-mode code review-and-patch pass
  for PR #537's first Bronze/Silver consumer proof: the creator metric Silver
  producer now optionally upgrades observation raw_refs through public Bronze
  source-surface catalog and Attachment Record rows.
use_when:
  - Couriering PR #537 to an independent controller before the Bronze/Silver consumer-proof patch is treated as settled.
  - Checking whether the Silver producer consumes public Bronze helper surfaces instead of private raw-folder semantics.
  - Adjudicating returned findings, bounded diff, validation evidence, or no-patch result before keeping delegated changes.
authority_boundary: retrieval_only
branch_or_commit: codex/bronze-silver-consumer-proof target implementation commit 3a4e81a8cc4bfca01dde9fea962197344e7bfa73
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/decision-routing.md
  - docs/prompts/templates/shared/orca_preflight_defaults_v0.md
  - docs/prompts/handoffs/bronze_silver_post_pr530_goal_frame_handoff_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  - orca-harness/data_lake/catalog.py
  - orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py
  - orca-harness/runners/run_creator_metric_rollup_producer.py
  - orca-harness/tests/unit/test_creator_metric_silver_producer.py
stale_if:
  - The reviewed implementation target commit changes before review.
  - PR #537 is materially rewritten beyond adding this prompt artifact.
  - The Bronze MGT declaration, Silver Vault raw-ref boundary, or Attachment Record contract changes before review.
  - Home-model adjudication for this commission completes.
```

## Objective And Intended Decision

- objective: obtain a de-correlated adversarial code review, plus a bounded patch where warranted, on whether PR #537 correctly proves the first Silver-facing consumer slice over public Bronze packet/catalog/Attachment Record surfaces.
- intended_decision: the commissioning home model decides `accept`, `accept_with_friction`, `patch_before_acceptance`, `reject`, or `NEEDS_ARCHITECTURE_PASS` for PR #537 before asking the owner to land or build the next Bronze/Silver material batch on top of it.

## Thread Operating Target Continuity

```yaml
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
  if_changed_reason: not_applicable
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: >
    Carry PR #530 to a disciplined close, then continue the same direction in a
    fresh thread by selecting the first Silver-facing proving slice that consumes
    public Bronze packet/catalog/Attachment Record surfaces without declaring
    Bronze full GT or starting unbounded runtime work.
  output_fit_check: >
    The next thread can decide or execute the next lake-convergence unit without
    re-litigating why Bronze MGT is enough for Silver intake, and without
    mistaking MGT for full GT.
  target_delta_from_prior:
    status: prior_target_not_supplied
    changed_fields: []
    summary: No prior machine-readable thread target was supplied to the handoff packet.
  drift_guard: "Do not convert PR #530's MGT/Silver-intake boundary into a full-GT, readiness, or runtime-implementation claim."
  conflict_behavior: call_out_conflict_before_proceeding
```

The target above is thread-local orientation only. It is not source authority,
validation evidence, approval, lifecycle completion, workflow sequencing
authority, durable memory, or edit permission.

## What This Is For / Done Looks Like

Success signals the review should attack:

- Silver records produced by this slice can cite public Bronze packet/catalog/AR surfaces with enough hash material to re-resolve raw truth.
- When a matching Attachment Record row exists, observation `raw_refs` become AR-backed instead of private packet-member path guesses.
- When no matching Attachment Record row exists, the fallback remains visible as a typed residual/posture, not inferred absence or silent success.
- The default non-AR producer path remains behaviorally and hash-stable unless `use_bronze_attachment_records` is explicitly enabled.
- The runner flag is explicit, default-off, and operator-readable.
- The tests cover AR hit, missing-AR fallback, and downstream reader/discovery/snapshot compatibility without becoming self-fulfilling.
- Nothing in PR #537 claims Bronze full God Tier, Silver readiness, Manifest v2/body-store/backend selection, runtime lake implementation completeness, validation proof, or authority beyond the bounded implementation slice.

Treat these as review axes, not a pass-if-matches checklist. If the goal or
success signal is wrong, too weak, or too broad, name that as a finding.

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; per-prompt deltas stated here.

```yaml
orca_start_preflight:
  authorization_basis: current owner request to prompt a delegated review patch for the PR #537 batch just implemented
  agents_md_read: yes_current_task_context
  overlay_readme_read: yes_current_task_context
  source_pack: bounded_custom_bronze_silver_pr537_review_pack
  repo_map_decision: not_needed
  repo_map_reason: >
    The review target is an explicitly enumerated three-file implementation diff
    plus named Bronze/Silver contracts; repo-wide routing is not needed to bound
    this prompt.
  workspace_path: C:\Users\vmon7\Desktop\projects\orca
  expected_worktree_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-silver-consumer-proof
  branch_or_commit_reference: codex/bronze-silver-consumer-proof target implementation commit 3a4e81a8cc4bfca01dde9fea962197344e7bfa73
  dirty_state_allowance: >
    Review target files clean at implementation commit 3a4e81a. This prompt may
    be committed later on the same branch; the controller should review the
    pinned implementation diff and ignore the prompt-file commit except as
    dispatch context.
  controlling_source_state: >
    AGENTS.md and Orca overlay sources were read by the dispatcher. PR state was
    freshly observed before authoring: PR #537 open draft, base main, head
    codex/bronze-silver-consumer-proof at 3a4e81a8cc4bfca01dde9fea962197344e7bfa73,
    mergeStateStatus CLEAN, mergeable MERGEABLE, and orca-harness-tests SUCCESS
    completed 2026-06-30T17:16:03Z. The controller must recheck moving PR/CI
    facts if material.
  edit_permission: patch-only
  output_mode: file-write prompt artifact plus paste-ready-chat copy
  receiver_output_mode: review-report plus working-tree patch if warranted
  prompt_artifact_path: docs/prompts/reviews/bronze_silver_pr537_delegated_adversarial_code_review_patch_prompt_v0.md
  downstream_report_path: docs/review-outputs/bronze_silver_pr537_delegated_adversarial_code_review_patch_v0.md
  target_files_or_dirs:
    - orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py
    - orca-harness/runners/run_creator_metric_rollup_producer.py
    - orca-harness/tests/unit/test_creator_metric_silver_producer.py
  doctrine_change_decision: >
    This prompt does not change doctrine. The reviewed implementation consumes
    existing Bronze MGT, Silver raw-ref, and Attachment Record contracts; any
    finding that requires changing those contracts must be flagged off-scope.
  isolation_decision: existing isolated PR worktree; do not create or switch branches/worktrees for review.
  validation_gates: >
    Receiver reruns the targeted producer/runner/catalog/reader/discovery/snapshot
    tests if it patches. If no patch is made, inspect the existing validation
    evidence and state whether any checks were rerun. Always preserve real
    failures and not-run status.
  external_source_boundary: >
    External workflow source is read-only from Orca work and is not Orca
    authority; jb is not Orca authority; installed skills are deployment copies.
  thread_operating_target_continuity:
    carried_forward: yes
    reason: same_workstream
    changed_from_input: no
    lifecycle_status: active_thread_local
```

## Delegated Review-And-Patch Commission

### Lane Binding

- overlay_status: `provisional_opt_in`, explicitly invoked by the owner for this work unit.
- operating_contract_pointer: `.agents/workflow-overlay/delegated-review-patch.md`.
- target_kind: `delegated_adversarial_code_review_and_patch` for a bounded multi-file implementation diff.
- review_lane: code - `workflow-code-review` for the submitted implementation/test/runner diff. Use `workflow-deep-thinking` first under the Source-Gated Method Contract.
- access: `repo` (default). Inspect the pinned branch/worktree directly.
- mode: `base-subagent`; do not split executor unless the controller returns a precise reason that the split-executor selection rule is actually satisfied.
- actor_model_family_receipt:
  - author_home_model_family: OpenAI / GPT (Codex based on GPT-5 authored PR #537 and this commission).
  - controller_model_family: `operator_to_fill`; must be a different vendor / model lineage from OpenAI to satisfy `cross_vendor_discovery` (vendor = upstream developer/provider, not host/reseller/wrapper).
  - current_receiving_actor_role: controller.
  - dispatch_mode: external-controller-courier.
  - de_correlation_status: operator must fill before review; block strict cross-vendor discovery claims if unsatisfied. A same-vendor delegate may claim only bounded `same_vendor_sanity` and must record a `same_vendor_rationale`.
- de_correlation: this is a who-constraint recorded in the commission, not a model recommendation. Do not recommend, rank, prescribe, or imply a runtime model anywhere in the review.
- subagent_authority: no tester/testee shortcut. The commissioning/home model must not satisfy this by reviewing its own work. If your runtime is the same author/home family and no different-vendor controller is actually receiving this prompt, stop before review and report the de-correlation gap.
- prompt_rendering: this filed prompt is the orchestrated prompt. Inspect the pinned repo/worktree directly; do not substitute this prompt body, a summary, or a recreated source pack for the source tree.

### Targets

- label: `[silver-producer]`
  path: `orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py`
  bounded_patch_scope: >
    Only the optional Bronze Attachment Record raw-ref upgrade path,
    default-off behavior, missing-AR residual visibility, content_hash effects,
    and helper integration through `source_surface_catalog_rows`.
- label: `[rollup-runner]`
  path: `orca-harness/runners/run_creator_metric_rollup_producer.py`
  bounded_patch_scope: >
    Only the CLI/operator path for enabling AR-backed raw_refs:
    `--use-bronze-attachment-records`, argument plumbing, default false behavior,
    and fail-closed error/reporting semantics.
- label: `[silver-producer-tests]`
  path: `orca-harness/tests/unit/test_creator_metric_silver_producer.py`
  bounded_patch_scope: >
    Only coverage for AR-backed raw_refs, missing-AR fallback/residual visibility,
    default behavior preservation, content_hash stability, and relevant fixture
    construction.

why_read_only_insufficient: this is the first real Silver-facing proving slice
over public Bronze catalog/AR helper surfaces. If the reviewer finds a concrete
raw-ref contract violation, silent fallback, default-path drift, missing
coverage, or fake-pass test issue, a small bounded patch inside these three
files is cheaper and safer than a review-only round trip.

off_scope (read-only / flag-only): Bronze catalog helper implementation,
generated catalog files, raw packets, source ledgers, data-lake contracts,
other data-lake code, other tests, overlay files, prompt files, CI, Manifest v2,
body-store/backend/retention decisions, Silver Vault contract text, full Bronze
GT declarations, capture/projection runners outside the submitted target, live
capture, and any commit/push/PR action.

If the correct fix requires changing off-scope files, return a finding with
`minimum_closure_condition` and leave the working tree unchanged outside the
three target files.

## Source-Gated Method Contract

REFERENCE-LOAD the method instructions below. Do not APPLY them yet - before
source readiness use them only to prepare a neutral source-reading lens. After
the source pack is loaded and `SOURCE_CONTEXT_READY` is declared, APPLY the
methods to the loaded source context.

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md` first.
2. REFERENCE-LOAD `workflow-delegated-review-patch`, `workflow-deep-thinking`, and `workflow-code-review`.
3. Do not APPLY any method yet.
4. SOURCE-LOAD the Required Source Pack below from the repo/worktree, not from pasted excerpts.
5. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, gaps, exclusions, and conflicts.
6. Only after that declaration, APPLY `workflow-delegated-review-patch` to enforce receipt, role, scope, patch, and CA-adjudication boundaries.
7. APPLY `workflow-deep-thinking` to frame the boundary problem, failure modes, and decision criteria before listing findings. It does not widen scope or authorize patching.
8. APPLY `workflow-code-review` to the producer, runner, and tests.
9. If `workflow-code-review` is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE`; do not emulate a strict code review inline.

## Required Source Pack

Open and inspect these exact sources from the repo/worktree:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/validation-gates.md`
- `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
- `docs/prompts/handoffs/bronze_silver_post_pr530_goal_frame_handoff_v0.md`
- target diff:
  `git diff origin/main...3a4e81a8cc4bfca01dde9fea962197344e7bfa73 -- orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py orca-harness/runners/run_creator_metric_rollup_producer.py orca-harness/tests/unit/test_creator_metric_silver_producer.py`
- target files at the implementation commit:
  - `orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py`
  - `orca-harness/runners/run_creator_metric_rollup_producer.py`
  - `orca-harness/tests/unit/test_creator_metric_silver_producer.py`
- Bronze/Silver authority and helper behavior:
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`
  - `orca-harness/data_lake/catalog.py`
- adjacent validation/reader behavior as needed:
  - `orca-harness/tests/test_data_lake_catalog.py`
  - `orca-harness/tests/unit/test_creator_metric_rollup_producer_runner.py`
  - `orca-harness/tests/unit/test_creator_metric_silver_discovery.py`
  - `orca-harness/tests/unit/test_creator_metric_silver_reader.py`
  - `orca-harness/tests/unit/test_creator_metric_silver_snapshot.py`

Do not bulk-load unrelated review outputs, all prompt files, all product files,
all data-lake directories, live capture artifacts, or external sources unless a
specific material finding requires one narrow adjacent read.

## Worktree Preflight

- Workspace:
  `C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-silver-consumer-proof`
- Branch:
  `codex/bronze-silver-consumer-proof`
- Base branch:
  `main`
- Reviewed implementation commit:
  `3a4e81a8cc4bfca01dde9fea962197344e7bfa73`
- Reviewed implementation diff:
  `3 files changed, 253 insertions(+), 9 deletions(-)`
- GitHub PR orientation:
  PR #537, `https://github.com/eric-foo/orca/pull/537`, open draft at dispatcher read; base `main`; head `codex/bronze-silver-consumer-proof`; target implementation OID `3a4e81a8cc4bfca01dde9fea962197344e7bfa73`.
- GitHub CI observed by dispatcher:
  `orca-harness-tests` `SUCCESS`, completed `2026-06-30T17:16:03Z`.
- Dirty-state allowance:
  the target implementation files should match the pinned target commit. A later branch advance that only adds this prompt artifact may be ignored for target review. Any target-file change beyond the prompt artifact must be surfaced before review.
- Permitted writes:
  the three target files and the review report path only. No staging, commit, push, branch operation, live capture, dependency installation, or off-scope source edit.

## Review Questions

Be maximally adversarial about material decision-relevant failure modes within
the commission-bound target. Find blocker/major issues first, especially:

- PUBLIC BRONZE SURFACE: does `[silver-producer]` consume `source_surface_catalog_rows` as the public helper boundary, or does any logic still depend on private safe-name, folder, or generated-file authority semantics?
- AR MATCHING: is the `(packet_id, file_id, relative_packet_path, sha256/body_sha256)` matching logic sufficient, deterministic, and collision-safe? Are missing or malformed keys handled without fake success?
- AR-BACKED RAW_REF SHAPE: when a matching Attachment Record row exists, does the emitted `raw_ref` carry the Silver-contract-required material to re-resolve and verify the raw body: attachment record id, schema/physicalization, packet/body ref, body hash, hash basis, source family/surface, payload kind/schema, replay/version pins, and producer-owned provenance where needed?
- MISSING-AR RESIDUAL: when no matching AR exists, is fallback explicit enough (`raw_packet_fallback_missing_attachment_record`, missing status, residual, lineage limitation), and does it avoid implying source absence or Bronze completeness?
- DEFAULT PATH PRESERVATION: when `use_bronze_attachment_records` is false, are output shape and content hashes preserved from the pre-PR default except for intended code-internal refactoring? If not proven, is the gap visible?
- CATALOG CURRENTNESS / FAILURE SEMANTICS: does enabling AR refs fail closed when the Bronze catalog is stale or unavailable, matching `source_surface_catalog_rows` behavior, without masking a partial-success output?
- RUNNER OPERATOR PATH: is `--use-bronze-attachment-records` default-off, help text accurate, and argument plumbing complete through `run_producer` and `main`?
- TEST INDEPENDENCE: do `[silver-producer-tests]` construct a real Bronze packet and rebuilt catalog rather than stubbing the exact producer behavior? Could a broken AR match, missing residual, or default-path drift still pass?
- DOWNSTREAM COMPATIBILITY: do reader/discovery/snapshot expectations remain compatible with optional `raw_ref_kind`, AR fields, and `lineage_limitations`?
- CLAIM DISCIPLINE: does the implementation or tests overclaim Bronze full GT, Silver readiness, validation, Manifest v2, body-store/backend selection, or runtime lake completeness?
- SCOPE: does the patch accidentally turn the first consumer proof into a wider AR runtime physicalization, capture/projection rewrite, or storage/layout decision?

For each actionable finding, state `minimum_closure_condition` (the required
end state, not how to implement it) and `next_authorized_action` (what this lane
may do next under its authority). Optional hardening must be labeled optional
and non-required. Do not emit `patch_queue_entry`; bounded patches go directly
to the named target files under Patch Authority.

## Patch Authority

You may patch only the three target files, and only to close blocker or major
issues found in this review:

- `[silver-producer]` `orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py`
- `[rollup-runner]` `orca-harness/runners/run_creator_metric_rollup_producer.py`
- `[silver-producer-tests]` `orca-harness/tests/unit/test_creator_metric_silver_producer.py`

Do not stage, commit, push, open PRs, install dependencies, enable network
access, run live capture, write a real production lake, or edit any off-scope
file. If the correct fix requires a data-lake contract change, Bronze catalog
helper change, migration, storage physicalization, source-capture packet
change, or overlay change, do not patch it - flag it as off-scope.

Design-level problem -> return `NEEDS_ARCHITECTURE_PASS`, stop patching, revert
any partial diff, and report findings only. A partial patch must not survive by
inertia.

## Validation Evidence To Inspect

Dispatcher-observed validation from the implementation turn:

```powershell
python -m pytest -p no:cacheprovider --no-header --no-summary -q orca-harness/tests/unit/test_creator_metric_silver_producer.py orca-harness/tests/unit/test_creator_metric_rollup_producer_runner.py orca-harness/tests/test_data_lake_catalog.py::test_source_surface_catalog_rows_expose_packet_and_ar_query_rows orca-harness/tests/unit/test_creator_metric_silver_discovery.py orca-harness/tests/unit/test_creator_metric_silver_reader.py orca-harness/tests/unit/test_creator_metric_silver_snapshot.py
python orca-harness/runners/run_creator_metric_rollup_producer.py --help
```

Observed results in that turn:

- targeted pytest command reported `49 passed`;
- runner help command succeeded and displayed `--use-bronze-attachment-records`;
- GitHub PR #537 `orca-harness-tests` reported `SUCCESS`.

Treat these as evidence to inspect, not as formal proof. If you patch, rerun the
narrowest relevant validation, normally:

```powershell
python -m pytest -p no:cacheprovider --no-header --no-summary -q orca-harness/tests/unit/test_creator_metric_silver_producer.py orca-harness/tests/unit/test_creator_metric_rollup_producer_runner.py orca-harness/tests/test_data_lake_catalog.py::test_source_surface_catalog_rows_expose_packet_and_ar_query_rows orca-harness/tests/unit/test_creator_metric_silver_discovery.py orca-harness/tests/unit/test_creator_metric_silver_reader.py orca-harness/tests/unit/test_creator_metric_silver_snapshot.py
python orca-harness/runners/run_creator_metric_rollup_producer.py --help
git diff --check
```

If a check is unavailable, report `validation_not_run` with the reason. Preserve
real failures; never mask a failing test or gate.

## Output Contract

Output mode: `review-report`.

Write the full review report to:

`docs/review-outputs/bronze_silver_pr537_delegated_adversarial_code_review_patch_v0.md`

If the report write fails, return a blocked chat result with `status: failed`,
`review_location: chat_only_current_thread`, `recommendation: blocked`, no
`report_path`, the failed path named, and enough human-readable detail to route.

Report consumption order (CA-facing): commission -> target -> authority ->
decision criteria -> evidence -> reviewer verdict/recommendation.

Report structure:

1. commission, lane binding, and actor/model-family receipt;
2. source context status: `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`;
3. findings first, ordered by materiality;
4. per finding: severity, target label, location, issue, evidence, impact, `minimum_closure_condition`, `next_authorized_action`, patched?;
5. unified diff for any target-file changes or `NO_PATCH_NEEDED`;
6. neutral per-change source citations, decision-sufficient in substance;
7. controller verdict and residual-risk note;
8. validation run status with exact commands;
9. off-scope flags;
10. review-use boundary.

Record these provenance fields on the durable report:

```yaml
reviewed_by: operator_or_reviewer_to_fill_or_unrecorded
authored_by: OpenAI/Codex GPT-5
de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded
same_vendor_rationale: not_applicable_unless_same_vendor_sanity_is_claimed
```

Do not fabricate model identity. Do not recommend, prescribe, rank, or imply a
runtime model choice.

After the report is written, return the compact `review_summary` YAML courier:

```yaml
review_summary:
  status: completed | blocked
  report_path: docs/review-outputs/bronze_silver_pr537_delegated_adversarial_code_review_patch_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | needs_architecture_pass | blocked
  reviewed_by: operator_to_fill
  authored_by: OpenAI/Codex GPT-5
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded
  same_vendor_rationale: "required if de_correlation_bar is same_vendor_sanity"
  summary: "One sentence."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  patch_status: no_patch_needed | patch_applied | patch_blocked | needs_architecture_pass
  changed_files: []
  validation_run: []
  validation_not_run: []
  residual_risk: "One sentence."
  next_action: "One concrete next step for the commissioning CA."
```

Close with this courier block so the home model can adjudicate:

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review-and-patch result for PR #537. Adjudicate it
under the delegated-review-patch return contract.

Include:
- original commission and target labels
- reviewed branch/head, target commit, and dirty-state result
- source readiness status and reviewed files
- findings and implementation evidence
- bounded patch diff or NO_PATCH_NEEDED
- citations
- reviewer verdict as decision input
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
```

The delegate's diff, findings, and verdict are claims to adjudicate, not
premises to inherit. This commission is not approval, validation, readiness,
mandatory remediation, source promotion, Bronze full GT declaration, Silver
implementation authority beyond the submitted patch, AR runtime implementation
authorization, runtime model routing, or permission to edit outside the three
target files.
