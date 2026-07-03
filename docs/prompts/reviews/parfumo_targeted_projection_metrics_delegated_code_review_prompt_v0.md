# Parfumo Targeted Projection Metrics Delegated Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Delegated code review-and-patch prompt for PR #532, Parfumo targeted rendered projection/Cleaning/Silver MetricObservation changes.
use_when:
  - Commissioning a different-family reviewer to inspect and patch PR #532.
  - Re-running a bounded review of the Parfumo targeted projection metrics branch before merge.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - docs/workflows/parfumo_targeted_capture_contract_v0.md
branch_or_commit: codex/parfumo-targeted-projection-metrics @ 3b6452cb6a6f4f906e1f21b3212970ce8745273a
```

## Paste-Ready Delegated Review-And-Patch Prompt

You are the delegated controller for a bounded Orca code review-and-patch pass. This is an operator-couriered repo-mode prompt. You must inspect the pinned repo/worktree directly; do not review from this prompt text alone.

### Actor / Model-Family Receipt

- author_home_model_family: OpenAI / GPT-family Codex
- current_receiving_actor_role: controller
- dispatch_mode: external-controller-courier
- required_controller_family: a different vendor / model lineage from OpenAI / GPT-family
- de_correlation_status: satisfied only if your actual runtime family is not OpenAI / GPT-family
- if your runtime is OpenAI / GPT-family, return `BLOCKED_CONTROLLER_NOT_DECORRELATED` for the cross-vendor delegated pass, or explicitly downgrade to `same_vendor_sanity` if the operator authorizes that weaker bar.
- This is a who-constraint, not a model recommendation. Do not include a recommended-model block.

### Orca Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 -- constants bound; deltas stated below.

- authorization_basis: current owner request: "delegate review patching" for PR #532 after the Parfumo targeted projection metrics implementation.
- objective / intended_decision: find material correctness, no-blur, source-surface, or validation issues in PR #532; apply bounded fixes only inside the submitted scope; return findings, diff, citations, verdict, residual risk, and validation evidence for home-model adjudication.
- output_mode: `review-report` plus bounded source patching.
- required_output_path: `docs/review-outputs/parfumo_targeted_projection_metrics_delegated_code_review_v0.md`
- edit_permission: patch-only inside the bounded patch scope below; all other files are read-only/flag-only.
- workspace_path: `C:\Users\vmon7\Desktop\projects\orca\worktrees\parfumo-targeted-projection-metrics`
- expected_branch: `codex/parfumo-targeted-projection-metrics`
- expected_head: `3b6452cb6a6f4f906e1f21b3212970ce8745273a`
- expected_base: `origin/main` at `65105faddeb73be50bf800c24f99e43c2df5c23e`
- dirty_state_allowance: clean or only your own review report and bounded patch changes. If unrelated dirty files are present, block before review.
- doctrine_change_decision: no doctrine change intended; flag any necessary doctrine or architecture change instead of patching it.
- isolation_decision: use the existing PR worktree above; do not create a new worktree unless the pinned worktree is inaccessible and the operator explicitly authorizes a substitute.
- validation_gates: run the listed validation commands after any patch; if you cannot run them, report `not_run` with reason.
- thread_operating_target_continuity: no visible active thread target is carried; this prompt is bounded to PR #532 review.

### Cynefin Router

Smallest complete outcome: a source-backed delegated code review of PR #532 plus bounded patch only for material issues inside the target files.
Regime: Complicated.
Why: The change crosses projection, Cleaning, and Silver no-blur semantics but has explicit source contracts and a focused file set.
Decomposition: Layer-based review, with no-blur/Silver front-door first, targeted-surface parser semantics second, tests/validation third.
Current bottleneck: Whether targeted rendered slice projection and MetricObservation emission preserve the Parfumo contract without inventing facts or bypassing Silver front-door validation.
Riskiest assumption: Review/high/low bucket selection from `data-rating`/tab labels is source-visible enough and does not infer unavailable 1/4/5-star buckets.
Stop or pivot condition: If the correct fix requires Basenotes work, live capture, anti-bot/proxy work, lane registry changes, raw Silver writes, or a broader architecture change, stop patching and return `NEEDS_ARCHITECTURE_PASS` or an off-scope finding.
Allowed next move: SOURCE-LOAD the named files, APPLY `workflow-deep-thinking`, then APPLY `workflow-code-review`, patch bounded material issues, validate, and write the review report.
Disallowed next move: Do not run live capture, touch Basenotes, alter proxy/Cloudflare behavior, write Silver outside `append_silver_record`, or widen beyond the bounded patch scope.

### Source-Gated Method Contract

1. REFERENCE-LOAD these method instructions before source analysis:
   - `workflow-deep-thinking`
   - `workflow-code-review`
   - `workflow-delegated-review-patch`
2. Do not APPLY them yet. Use them only to prepare a neutral source-reading lens.
3. SOURCE-LOAD the required sources below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources and conflicts.
5. Only after source readiness, APPLY `workflow-deep-thinking` to frame failure modes, then APPLY `workflow-code-review` to produce findings and bounded patches.

### Required Source Load

Load these authority and lane files first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/safety-rules.md`

Load the Parfumo contract and research context:

- `docs/workflows/parfumo_targeted_capture_contract_v0.md`
- `docs/research/orca_fragrance_native_database_live_probe_v0.md`
- Historical handoff packet, if available in the repo object database:
  `git show 5865f4d7a2fdd14114e04d8bac9fecc686fda17c:docs/workflows/fragrance_native_capture_pipeline_parfumo_basenotes_build_handoff_v0.md` # nonresolving: removed on main in 3b23fa3e (PR #529); superseded by the live-probe pin registry above

Load no-blur and front-door infrastructure:

- `orca-harness/data_lake/silver_record.py`
- `orca-harness/data_lake/non_silver_record.py`
- `orca-harness/data_lake/lane_registry.py`
- `.agents/hooks/check_silver_lane_registry.py`

Load Fragrantica reference modules for parity, not copy-paste authority:

- `orca-harness/source_capture/fragrantica_projection.py`
- `orca-harness/cleaning/fragrantica.py`
- `orca-harness/cleaning/fragrantica_lake.py`
- `orca-harness/tests/test_fragrantica_capture_to_silver_e2e.py`
- `orca-harness/tests/test_fragrantica_cleaning_lake_pilot.py`

Load the PR #532 target files:

- `orca-harness/source_capture/parfumo_projection.py`
- `orca-harness/cleaning/parfumo.py`
- `orca-harness/cleaning/parfumo_lake.py`
- `orca-harness/tests/unit/test_parfumo_projection.py`
- `orca-harness/tests/unit/test_parfumo_cleaning_projection_integration.py`
- `orca-harness/tests/test_parfumo_native_pipeline_lake.py`

Inspect the PR diff:

- PR: `https://github.com/eric-foo/orca/pull/532`
- head SHA: `3b6452cb6a6f4f906e1f21b3212970ce8745273a`
- changed files count before this prompt existed: 6 files, 710 insertions, 28 deletions.

### Bounded Patch Scope

You may edit only these six implementation/test files:

- `orca-harness/source_capture/parfumo_projection.py`
- `orca-harness/cleaning/parfumo.py`
- `orca-harness/cleaning/parfumo_lake.py`
- `orca-harness/tests/unit/test_parfumo_projection.py`
- `orca-harness/tests/unit/test_parfumo_cleaning_projection_integration.py`
- `orca-harness/tests/test_parfumo_native_pipeline_lake.py`

Everything else is read-only / flag-only, including this prompt file, overlay files, docs contracts, lane registry, Fragrantica modules, no-blur infrastructure, Basenotes files, runner/live-capture code, and GitHub/CI configuration. If the correct fix lies outside the six files, do not patch it; report an off-scope finding with the minimum closure condition.

### Review Axis

Find material issues where PR #532 could:

- accept the wrong source surface or reject the targeted rendered surface incorrectly;
- parse local rendered artifacts unsafely, duplicate rows across targeted slices, or accidentally parse route receipts/screenshots/plans;
- infer Parfumo high/low/1/4/5-star buckets without source-visible numeric rating/filter/order evidence;
- silently lose latest/recent reviews or statements from targeted packets;
- carry direct-HTTP source surface into Cleaning handles for targeted rendered packets;
- emit MetricObservation records for absent metrics, zero-fill unavailable metrics, or violate observed metric posture coupling;
- bypass `append_silver_record` or blur Cleaning audit evidence into Silver facts;
- break direct-HTTP behavior or Fragrantica parity assumptions;
- leave tests that pass without proving the target surface, slice filtering, residualization, or MetricObservation front-door behavior.

### Non-Goals / Forbidden Work

- No Basenotes work.
- No full Parfumo corpus claim.
- No live capture, browser automation, proxy, Cloudflare, CAPTCHA, anti-bot, cookie, storage, or clearance-token work.
- No Silver writes through the raw writer.
- No Fragrantica rating-scale inheritance.
- No broad refactor or shared abstraction unless required to close a material finding inside the bounded scope.
- No prompt artifact edits; this prompt is read-only review input.

### Validation Evidence From Authoring Lane

The authoring lane reported these local checks green before this prompt was filed:

- `python -m py_compile source_capture\parfumo_projection.py cleaning\parfumo.py cleaning\parfumo_lake.py tests\unit\test_parfumo_projection.py tests\unit\test_parfumo_cleaning_projection_integration.py tests\test_parfumo_native_pipeline_lake.py`
- `python -m pytest -q tests\unit\test_parfumo_projection.py tests\unit\test_parfumo_cleaning_projection_integration.py tests\unit\test_parfumo_non_silver_record_roles.py tests\test_parfumo_native_pipeline_lake.py tests\unit\test_parfumo_mgt_capture_runner.py` -> 22 passed
- `python -m pytest -q tests\contract\test_capture_runner_lake_seam_coverage.py tests\unit\test_silver_record.py` -> 21 passed
- `python .agents\hooks\check_silver_lane_registry.py --selftest --strict` -> SELFTEST OK
- `git diff --check` -> clean

Treat these as evidence to inspect, not proof. Re-run relevant checks after any patch.

### Controller Output Contract

Write the full review report to:

`docs/review-outputs/parfumo_targeted_projection_metrics_delegated_code_review_v0.md`

The report must be findings-first and include:

- `reviewed_by`: your actual model/tool identity, or `unrecorded` if unavailable.
- `authored_by`: `OpenAI / GPT-family Codex`.
- `de_correlation_bar`: `cross_vendor_discovery` if your runtime is not OpenAI/GPT-family; otherwise `same_vendor_sanity` or `self_fallback` with rationale.
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
- Source-read ledger with file paths and line citations for load-bearing claims.
- Findings ordered by materiality, each with:
  - finding id;
  - location;
  - implementation evidence;
  - authority/evidence basis;
  - impact;
  - minimum_closure_condition;
  - next_authorized_action;
  - whether patched in this pass.
- Unified diff for any patches you applied.
- Validation commands run and observed outcomes, or `not_run` with reason.
- Off-scope flags.
- Verdict and residual-risk note. The verdict is decision input only, not approval, validation, or readiness.
- `DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL` courier block for adjudication.

After writing the report, return a compact chat summary plus this courier YAML:

```yaml
review_courier:
  output_mode: filesystem-output
  report_path: docs/review-outputs/parfumo_targeted_projection_metrics_delegated_code_review_v0.md
  commission: delegated code review-and-patch for PR #532
  target: Parfumo targeted rendered projection/Cleaning/Silver MetricObservation PR diff
  authority: provisional delegated review-and-patch; code review lane findings-first; patch-only within six target files
  de_correlation_bar: <cross_vendor_discovery | same_vendor_sanity | self_fallback | blocked>
  reviewer_verdict: <decision input only>
  finding_ids: []
  patched_files: []
  validation: []
  minimum_closure_conditions: []
  next_authorized_action: home-model adjudication of findings/diff
  non_claims:
    - not approval
    - not validation
    - not readiness
    - not merge authorization
```

### Escalation

Return `NEEDS_ARCHITECTURE_PASS` and leave no kept partial patch if the issue is design-level or cannot be fixed inside the bounded six-file scope. Return `BLOCKED_REVIEW_LANE_UNAVAILABLE` if you cannot invoke `workflow-code-review` after source readiness. Return the nearest blocker if the worktree, branch, head SHA, source files, output path, or dirty-state conditions do not match this prompt.
