# Bronze Data Lake Doctor Delegated Adversarial Code Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca delegated review-and-patch prompt
scope: >
  Commission a de-correlated repo-mode adversarial code review-and-patch pass
  for PR #478, the Bronze v4.1 data-lake doctor runner and focused tests.
use_when:
  - Couriering PR #478 for independent review before the Bronze doctor operator surface is treated as settled.
  - Checking whether the doctor creates fake lake confidence, hides raw/index corruption, over-widens Bronze semantics, or misses operator-grade traceability failures.
authority_boundary: retrieval_only
branch_or_commit: codex/bronze-v41-clean-verify @ 924321bafed3214321cc5817bdc10b8280724f1c
pr: https://github.com/eric-foo/orca/pull/478
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/decision-routing.md
  - docs/prompts/templates/shared/orca_preflight_defaults_v0.md
  - docs/workflows/orca_repo_map_v0.md
  - orca-harness/data_lake/root.py
  - orca-harness/runners/run_data_lake_doctor.py
  - orca-harness/tests/test_data_lake_doctor.py
input_hashes:
  docs/workflows/orca_repo_map_v0.md: 5B2897BFED774EEED0587BE8810A1847FB15DAECA4D27250612290C502DF4DB9
  orca-harness/runners/run_data_lake_doctor.py: 5C68A7E3C53E485C4D1251A2223B3C29566A5B0D3D0325B9D7E37C90207744A8
  orca-harness/tests/test_data_lake_doctor.py: 9215392216273F2E14822958A81189D3CF75A19E7319BEB54A9E6B3EE7931222
stale_if:
  - PR #478 is retargeted away from main.
  - Base commit efc4ed7cd83642acf8119f83f38d50b82b023d14 is no longer the PR base when review starts.
  - Any target file listed in this prompt changes after 924321bafed3214321cc5817bdc10b8280724f1c before review, other than this prompt artifact being added in a later commit.
  - Orca delegated-review-patch, review-lanes, prompt-orchestration, source-loading, or DataLakeRoot v4.1 sharding authority changes before review.
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0, constants bound; deltas stated here.

- output_mode: `file-write` for this prompt artifact, plus `paste-ready-chat` copy for couriering.
- prompt_artifact_path: `docs/prompts/reviews/bronze_data_lake_doctor_delegated_adversarial_code_review_patch_prompt_v0.md`.
- template_kind: `review` plus delegated review-and-patch commission semantics from `.agents/workflow-overlay/delegated-review-patch.md`.
- authorization_basis: current owner invocation `prompt - delegate review patch` after PR #478 was opened for the Bronze data-lake doctor implementation.
- objective / intended_decision: determine whether the Bronze doctor runner is safe to keep, needs bounded patching, or must route back for architecture/scoping before the operator surface is treated as settled.
- source_pack: custom S1 plus pinned implementation diff, lake root API, target files, focused tests, and the relevant Orca prompt/review/delegated-review overlay files named below.
- edit_permission_for_receiver: `patch-only` inside the named target files below, plus report write at the named review-output path; all other paths are read-only / flag-only.
- workspace_path: `C:\Users\vmon7\Desktop\projects\orca`.
- expected_worktree_path: `C:\Users\vmon7\Desktop\projects\orca\worktrees\bronze-v41-clean-verify`.
- branch_or_commit_reference: `codex/bronze-v41-clean-verify @ 924321bafed3214321cc5817bdc10b8280724f1c`.
- reviewed_diff: `efc4ed7cd83642acf8119f83f38d50b82b023d14..924321bafed3214321cc5817bdc10b8280724f1c`.
- target_files_or_dirs:
  - `orca-harness/runners/run_data_lake_doctor.py`
  - `orca-harness/tests/test_data_lake_doctor.py`
  - `docs/workflows/orca_repo_map_v0.md`
- downstream_report_path: `docs/review-outputs/adversarial-artifact-reviews/bronze_data_lake_doctor_delegated_adversarial_code_review_v0.md`.
- dirty_state_allowance: target worktree should be clean before the receiver starts. If this prompt exists as a later commit on the same branch, review the pinned implementation diff above and ignore the prompt-file commit except as dispatch context.
- controlling_source_state: checked before prompt creation; worktree clean on `codex/bronze-v41-clean-verify`, PR #478 open/draft, target implementation head `924321bafed3214321cc5817bdc10b8280724f1c`, base `efc4ed7cd83642acf8119f83f38d50b82b023d14`.
- doctrine_change_decision: no doctrine change intended. This is implementation/test/runner/repo-map hardening under existing Data Lake v4.1, prompt orchestration, and delegated-review-patch boundaries.
- isolation_decision: existing isolated clean worktree `worktrees/bronze-v41-clean-verify` off `origin/main`; no new worktree required for a bounded review-and-patch pass on PR #478.
- cynefin_route: complicated / source-hierarchy and implementation review. Allowed next move is bounded de-correlated review-and-patch of the named files. Disallowed next move is expanding into Bronze architecture, semantic lake folders, live captures, Silver runner redesign, or broad repo cleanup.
- validation_evidence_already_observed:
  - `python -m compileall -q runners\run_data_lake_doctor.py tests\test_data_lake_doctor.py` passed.
  - `python -m pytest -p no:cacheprovider --no-header tests/test_data_lake_doctor.py` passed: `5 passed in 0.67s`.
  - `python -m pytest -p no:cacheprovider --no-header tests/test_data_lake_doctor.py tests/test_data_lake_root.py tests/test_data_lake_availability.py tests/test_data_lake_sharding.py tests/test_data_lake_record_set.py tests/test_data_lake_rebuild_proof.py tests/test_data_lake_read_loader.py tests/test_ecr_lake_pilot.py tests/test_signal_content_lake_pilot.py tests/test_retail_pdp_lake_pilot.py tests/test_ig_projection_lake_pilot.py tests/test_fragrantica_projection_lake_pilot.py tests/test_fragrantica_cleaning_lake_pilot.py tests/test_fragrantica_capture_to_silver_e2e.py tests/unit/test_silver_lineage.py tests/contract/test_capture_runner_lake_seam_coverage.py` passed: `136 passed, 1 skipped in 8.01s`.
  - `git diff --cached --check` was clean before the implementation commit.
- receiver_validation_expectation: rerun the doctor-focused tests for any patch. Run `git diff --check`. Rerun the broader lake suite if the patch changes doctor inspection logic, root API assumptions, availability behavior, or test fixtures beyond formatting/reporting.
- fitness_reference: done looks like a boring, operator-safe Bronze doctor that makes raw/index/shard/read corruption visible without creating semantic Bronze folders, fake success, hidden writes, or downstream Silver authority.
- thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
  if_changed_reason: not_applicable

## Delegated Review-And-Patch Commission

### Lane Binding

- overlay_status: `provisional_opt_in`, explicitly invoked by the owner for this PR.
- operating_contract_pointer: `.agents/workflow-overlay/delegated-review-patch.md`.
- target_kind: `delegated_code_review_and_patch` sibling mode for a bounded multi-file implementation/code diff.
- review_lane: mixed, with `workflow-code-review` for runner/test/implementation behavior and `workflow-adversarial-artifact-review` only for the repo-map route text if a source-backed doc finding is needed. The code review lane is primary.
- mode: `base-subagent` / repo-mode controller. Do not use split-executor.
- actor_model_family_receipt:
  - author_home_model_family: OpenAI / Codex / GPT-5, this commissioning lane.
  - controller_model_family: `operator_to_fill`; must be a different vendor / model lineage from OpenAI to satisfy `cross_vendor_discovery`. If not different-vendor, record `same_vendor_sanity` and do not claim discovery or no-new-seam.
  - current_receiving_actor_role: controller.
  - dispatch_mode: external-controller-courier.
  - de_correlation_status: operator must fill before review; block strict cross-vendor discovery claims if unsatisfied.
- de_correlation: this is a who-constraint, not a model recommendation. Do not recommend, rank, or prescribe a runtime model.
- subagent_authority: no tester/testee shortcut. The commissioning/home model must not satisfy this by reviewing its own patch. If your runtime is the same author/home family and no different-family controller is actually receiving this prompt, stop before review.
- prompt_rendering: this filed prompt is the orchestrated prompt. The receiver must inspect the pinned repo/worktree directly; do not substitute this prompt body, a summary, an alternate checkout, or a recreated source pack for the source tree.

### Target

- targets:
  - label: `[bronze-doctor-runner]`
    path: `orca-harness/runners/run_data_lake_doctor.py`
    bounded_patch_scope: only the data-lake doctor CLI/core inspection logic, JSON report shape, read-only default, explicit availability rebuild path, raw packet candidate classification, availability comparison, packet lookup, and issue/status calculation.
  - label: `[bronze-doctor-tests]`
    path: `orca-harness/tests/test_data_lake_doctor.py`
    bounded_patch_scope: only focused no-network tests for clean inspection, missing/stale availability, explicit rebuild, wrong-shard detection, and CLI JSON behavior.
  - label: `[repo-map-route]`
    path: `docs/workflows/orca_repo_map_v0.md`
    bounded_patch_scope: only the repo-map freshness entries for the new data-lake doctor runner and its tests.
- why_read_only_insufficient: PR #478 adds an operator-facing Bronze integrity surface. If the reviewer finds a fake-pass, hidden mutation, wrong-shard blind spot, availability-index stale/orphan bug, packet lookup misreport, or repo-map overclaim, a bounded correction inside the same three files is cheaper and safer than a review-only loop.
- off_scope: read-only / flag-only for all other files, including `orca-harness/data_lake/root.py`, capture runners, Silver lake adapters, product specs, workflow overlay files, live data roots, generated lake contents, CI/hook infrastructure, and broader Bronze architecture. If the correct fix requires changing those, flag it and do not patch.

When returning findings, diffs, or citations, carry the label tag for the affected target.

### Source-Gated Method Contract

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md` first.
2. REFERENCE-LOAD `workflow-delegated-review-patch`, `workflow-deep-thinking`, `workflow-code-review`, and, only for the repo-map route text, `workflow-adversarial-artifact-review`. Do not APPLY them yet.
3. SOURCE-LOAD the target source pack below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before producing findings.
5. Only after source readiness, APPLY `workflow-delegated-review-patch` to enforce receipt, role, scope, patch, and CA-adjudication boundaries.
6. APPLY `workflow-deep-thinking` to frame false-confidence paths and material failure modes.
7. APPLY `workflow-code-review` to the runner and tests.
8. APPLY `workflow-adversarial-artifact-review` only if needed to review a material repo-map route-text failure.
9. If `workflow-code-review` is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE`; do not emulate a strict code review inline. If `workflow-adversarial-artifact-review` is unavailable, do not make strict artifact-review claims about the repo-map route; flag the limitation.

### Required Source Pack

Open and inspect these exact sources from the repo/worktree, not from pasted excerpts:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/decision-routing.md`
- `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
- target diff: `git diff efc4ed7cd83642acf8119f83f38d50b82b023d14..924321bafed3214321cc5817bdc10b8280724f1c -- docs/workflows/orca_repo_map_v0.md orca-harness/runners/run_data_lake_doctor.py orca-harness/tests/test_data_lake_doctor.py`
- current target files at commit `924321bafed3214321cc5817bdc10b8280724f1c`:
  - `docs/workflows/orca_repo_map_v0.md`
  - `orca-harness/runners/run_data_lake_doctor.py`
  - `orca-harness/tests/test_data_lake_doctor.py`
- Data Lake v4.1 API/contract sources:
  - `orca-harness/data_lake/root.py`, targeted to root marker/epoch marker behavior, `raw_shard`, `record_availability`, `read_availability`, `list_available`, `rebuild_availability`, `find_packet`, and `load_raw_packet`.
  - `orca-harness/tests/test_data_lake_sharding.py`, targeted to wrong-shard and rebuild behavior.
  - `orca-harness/tests/test_data_lake_availability.py`, targeted to capture round-trip and rebuild semantics.
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md` if a finding depends on the storage contract rather than implementation behavior.

Do not bulk-load unrelated review outputs, all prompts, all product files, all capture runners, all Silver adapters, live lake contents, or external sources unless a specific material finding requires one narrow adjacent read.

### Review Questions

Find blocker or major issues first, especially:

- Does the doctor stay read-only by default, with mutation limited to explicit `--rebuild-availability` against the rebuildable index?
- Does it avoid silently initializing, migrating, repairing, deleting, or moving raw material?
- Does it correctly distinguish valid sharded raw packets from wrong-shard, legacy-flat, and malformed raw containers without hiding corruption?
- Does it catch missing, stale, unreadable, invalid-name, and orphan availability records without trusting the index as authority?
- Does it verify raw reads through `DataLakeRoot.load_raw_packet` enough to surface manifest/preserved-file hash, size, missing-file, and path-safety failures?
- Does packet lookup report a missing or unreadable packet as an issue instead of fake success?
- Does `--rebuild-availability` produce a post-rebuild report that still surfaces raw corruption the rebuild intentionally skips?
- Does the JSON report give operators enough traceability to find the affected packet/container without embedding semantic Bronze folder assumptions?
- Are the tests strong enough to prevent the most dangerous false passes: dry-run accidentally mutating, stale availability looking clean, wrong-shard packets being indexed, and CLI output hiding packet errors?
- Does the production `DataLakeRoot.resolve` boundary remain intact, with tests not weakening the outside-repo guard?
- Does the repo-map entry route the doctor accurately without claiming Bronze validation, lake readiness, Silver coordination, deployment, live data-root safety, or operator coverage beyond this runner?
- Does the patch stay inside the current PR scope, or did it smuggle data-lake architecture, semantic-folder organization, live capture/Silver runner coupling, CI, or broad workflow changes?

### Patch Authority

You may patch only the three target files listed above, and only to close blocker or major issues found in this review. You may also write the review report to the named downstream report path. Do not stage, commit, push, open PRs, install dependencies, run network access, touch live `ORCA_DATA_ROOT` data, run live capture, or edit `orca-harness/data_lake/root.py`.

If the correct fix requires changing DataLakeRoot APIs, v4.1 contracts, capture runners, Silver adapters, product docs, workflow overlays, or broader Bronze architecture, do not patch it. Flag it as off-scope.

If a design-level problem is found, return `NEEDS_ARCHITECTURE_PASS`, stop patching, revert any partial diff, and report findings only. A partial patch must not survive by inertia.

### Validation Expectations

If you patch, run the narrowest relevant validation available, normally from `orca-harness`:

- `python -m compileall -q runners\run_data_lake_doctor.py tests\test_data_lake_doctor.py`
- `python -m pytest -p no:cacheprovider --no-header tests/test_data_lake_doctor.py`

Run the broader lake seam suite if behavior changes beyond comments/report wording:

- `python -m pytest -p no:cacheprovider --no-header tests/test_data_lake_doctor.py tests/test_data_lake_root.py tests/test_data_lake_availability.py tests/test_data_lake_sharding.py tests/test_data_lake_record_set.py tests/test_data_lake_rebuild_proof.py tests/test_data_lake_read_loader.py tests/test_ecr_lake_pilot.py tests/test_signal_content_lake_pilot.py tests/test_retail_pdp_lake_pilot.py tests/test_ig_projection_lake_pilot.py tests/test_fragrantica_projection_lake_pilot.py tests/test_fragrantica_cleaning_lake_pilot.py tests/test_fragrantica_capture_to_silver_e2e.py tests/unit/test_silver_lineage.py tests/contract/test_capture_runner_lake_seam_coverage.py`

Also run from repo root when relevant:

- `git diff --check`
- `python .agents\hooks\check_repo_map_freshness.py --changed --strict` if the repo-map route changes.
- `python .agents\hooks\check_map_links.py --strict` if the repo-map route changes.

Report exact commands and results. Preserve real failures.

### Output Contract

Write the full review report to:

- `docs/review-outputs/adversarial-artifact-reviews/bronze_data_lake_doctor_delegated_adversarial_code_review_v0.md`

If the report write fails, return a blocked chat result with `review_location: chat_only_current_thread`, no `report_path`, and enough detail to route.

Report structure:

1. Commission, lane binding, and actor/model-family receipt.
2. Source context status.
3. Findings first, ordered by severity: critical, major, minor.
4. For each finding: severity, target label, location, issue, evidence, impact, minimum_closure_condition, next_authorized_action, and whether patched.
5. Unified diff for any target-file changes.
6. Per-change neutral source citations that are decision-sufficient in substance.
7. Controller verdict and residual-risk note.
8. Validation run status, including exact commands run or not run.
9. Off-scope flags.
10. CA adjudication packet.
11. Review-use boundary.

After writing the report, return this compact chat YAML:

```yaml
review_summary:
  status: completed | blocked
  report_path: docs/review-outputs/adversarial-artifact-reviews/bronze_data_lake_doctor_delegated_adversarial_code_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: operator_to_fill
  authored_by: OpenAI Codex / GPT-5
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

If no issues are found, say that clearly and name residual risks or test gaps. Your output is decision input only. The commissioning CA must adjudicate before any change is kept.

### Review-Use Boundary

This delegated review-and-patch result is decision input only. The controller's diff, citations, and verdict are claims to adjudicate, not premises to inherit. It is not owner acceptance, validation proof, readiness, deployment, live data-lake safety, source-capture authorization, Silver coordination proof, or permission to keep any patch without Chief Architect adjudication.
