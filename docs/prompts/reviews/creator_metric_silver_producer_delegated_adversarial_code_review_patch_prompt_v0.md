# Creator Metric Silver Producer Delegated Adversarial Code Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca delegated review-and-patch prompt
scope: >
  Commission a de-correlated repo-mode adversarial code review-and-patch pass
  for the lake-native creator-metric Silver producer: a new producer that
  re-emits Instagram reels-grid metric observations and per-account rollups as
  formal Silver Vault derived records (MetricObservation + a new
  MetricRollupObservation payload_kind), plus its producer-owned record contract
  and its unit test.
use_when:
  - Couriering the creator-metric Silver producer for independent review before
    the rollup payload contract and producer are treated as settled.
  - Checking whether a computed rollup may carry observed posture, whether the
    Silver Vault envelope/content_hash discipline is faithfully mirrored, and
    whether the no-drift and lineage guarantees hold.
authority_boundary: retrieval_only
branch_or_commit: claude/creator-silver-metric-producer @ c862c42f1098b1ea2207ff1f08d1634868856414
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/decision-routing.md
  - docs/prompts/templates/shared/orca_preflight_defaults_v0.md
  - orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py
  - orca-harness/tests/unit/test_creator_metric_silver_producer.py
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md
  - orca-harness/cleaning/fragrantica_lake.py
stale_if:
  - The branch is retargeted or the reviewed head moves off c862c42f1098b1ea2207ff1f08d1634868856414.
  - Any target file changes after c862c42f before review, other than this prompt artifact being added in a later commit.
  - The Silver Vault record contract changes record header, MetricObservation, posture, or content_hash semantics before review.
  - Orca delegated-review-patch, review-lanes, prompt-orchestration, or source-loading overlay authority changes before review.
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 — constants bound; deltas stated here.

- output_mode: `file-write` for this prompt artifact, plus `paste-ready-chat` copy for couriering.
- prompt_artifact_path: `docs/prompts/reviews/creator_metric_silver_producer_delegated_adversarial_code_review_patch_prompt_v0.md`.
- template_kind: `review` plus delegated review-and-patch commission semantics from `.agents/workflow-overlay/delegated-review-patch.md` (`delegated_code_review_and_patch` sibling mode: bounded multi-file diff).
- authorization_basis: current owner instruction to implement STEP-01 + STEP-02 and then prepare a delegated adversarial review-and-patch prompt for the result.
- edit_permission_for_receiver: `patch-only` inside the three named target files below; all other paths are read-only / flag-only.
- workspace_path: `C:\Users\vmon7\Desktop\projects\orca`.
- expected_worktree_path: `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-silver-metric-producer`.
- branch_or_commit_reference: `claude/creator-silver-metric-producer @ c862c42f1098b1ea2207ff1f08d1634868856414`.
- reviewed_diff: `74373bb093d3cecd11f5e24a9d2dd2cecbc96223..c862c42f1098b1ea2207ff1f08d1634868856414` (the single commit that introduces the three target files; parent is the branch point off `origin/main`). The PR base when opened will be current `origin/main`.
- pin_note: pinned by commit SHA, not per-file SHA256. The repo is autocrlf (`i/lf w/crlf`), so a working-tree SHA256 will not match a fresh LF checkout; compare against commit `c862c42f` instead.
- target_files_or_dirs:
  - `orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py`
  - `orca-harness/tests/unit/test_creator_metric_silver_producer.py`
  - `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md`
- downstream_report_path: `docs/review-outputs/adversarial-artifact-reviews/creator_metric_silver_producer_adversarial_code_review_v0.md`.
- dirty_state_allowance: target worktree should be clean at `c862c42f` before the receiver starts. If this prompt exists as a later commit on the same branch, review the pinned target diff above and ignore the prompt-file commit except as dispatch context.
- controlling_source_state: checked before prompt creation; worktree clean on `claude/creator-silver-metric-producer`, head `c862c42f`, branched off `origin/main`.
- doctrine_change_decision: introduces a producer-owned `MetricRollupObservation` payload_kind and the contract doc that defines it; this is a source-family architecture-contract addition under the existing creator-registry / lake-native-mapping and Silver Vault record contract boundaries. The load-bearing decision (observed posture for a computed aggregate) is named for review rather than asserted as settled doctrine.
- isolation_decision: existing isolated worktree `worktrees/creator-silver-metric-producer` off `origin/main`; no new worktree required for a bounded review-and-patch pass.
- validation_evidence_already_observed (re-run to confirm; do not trust):
  - `python -m pytest -q -p no:cacheprovider orca-harness\tests\unit\test_creator_metric_silver_producer.py` passed, 4 tests.
  - baseline 5 creator suites passed, 52 tests; new + baseline together: 56 passed.
  - `python orca-harness\runners\run_creator_profile_current_materialize.py --check` reported up to date (read model untouched).
  - `python .agents\hooks\check_map_links.py --strict` passed with 0 findings.
  - `git diff --check` clean.
- receiver_validation_expectation: rerun the producer test and the baseline creator suites for any patch; run `git diff --check`; rerun `check_map_links.py --strict` if the contract doc or any retrieval header changes.
- thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target_in_prompt_scope
  changed_from_input: no
  lifecycle_status: not_applicable

## Delegated Review-And-Patch Commission

### Lane Binding

- overlay_status: `provisional_opt_in`, explicitly invoked by the owner for this work unit.
- operating_contract_pointer: `.agents/workflow-overlay/delegated-review-patch.md`.
- target_kind: `delegated_code_review_and_patch` (bounded multi-file implementation diff; the named three-file set is the only patchable surface and cannot silently widen).
- review_lane: mixed — `workflow-code-review` for `silver_metric_producer.py` and its test (primary), and `workflow-adversarial-artifact-review` for the authored contract doc `creator_metric_silver_record_contract_v0.md`. Implementation/code review and artifact review remain separate lanes; this commission uses both as methods, it does not merge them.
- mode: `base-subagent` / repo-mode controller. Do not use split-executor.
- access: `repo` (default). The receiver inspects the pinned branch/worktree directly.
- actor_model_family_receipt:
  - author_home_model_family: Anthropic / Claude (this commissioning lane).
  - controller_model_family: `operator_to_fill`; must be a different vendor / model lineage from Anthropic to satisfy `cross_vendor_discovery`.
  - current_receiving_actor_role: controller.
  - dispatch_mode: external-controller-courier.
  - de_correlation_status: operator must fill before review; block strict cross-vendor discovery claims if unsatisfied.
- de_correlation: this is a who-constraint, not a model recommendation. Do not recommend, rank, or prescribe a runtime model.
- subagent_authority: no tester/testee shortcut. The commissioning / home model (Anthropic family) must not satisfy this by reviewing its own work. If your runtime is the same author/home family and no different-vendor controller is actually receiving this prompt, stop before review and report the de-correlation gap.
- prompt_rendering: this filed prompt is the orchestrated prompt. Inspect the pinned repo/worktree directly; do not substitute this prompt body, a summary, or a recreated source pack for the source tree.

### Target

- targets:
  - label: `[silver-metric-producer]`
    path: `orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py`
    bounded_patch_scope: only the producer that wraps the reused seed observations/rollups in Silver Vault MetricObservation / MetricRollupObservation envelopes and appends them via `DataLakeRoot.append_record` — envelope fields, content_hash, posture/value coupling, derived_refs lineage, raw_anchor resolution, subject shaping.
  - label: `[silver-metric-producer-tests]`
    path: `orca-harness/tests/unit/test_creator_metric_silver_producer.py`
    bounded_patch_scope: only coverage proving envelope conformance, independent content_hash reproduction, posture/value coupling (including the non-observed branch), rollup→observation lineage, and no-drift vs the seed.
  - label: `[creator-metric-silver-contract]`
    path: `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md`
    bounded_patch_scope: only the producer-owned record contract text — the two payload kinds, the rollup payload shape, the posture rule, lineage, conformance, accepted residuals, and non-claims.
- why_read_only_insufficient: this is the first lake-native creator-metric producer and it defines a new `MetricRollupObservation` payload_kind every future platform producer and the read layer will conform to. If the reviewer finds an envelope-conformance, content_hash, posture-overclaim, lineage, or fake-pass issue, a bounded correction inside these three files is cheaper and safer than a review-only round-trip.
- off_scope: read-only / flag-only for all other files, including the Silver Vault record contract and other data_lake authority docs, `instagram_metric_seed.py` and the seed JSON (the reused computation), `materialize.py` / `validation.py` / the creator_profile_current view, `fragrantica_lake.py`, `data_lake/root.py`, source ledger JSON, product specs, the repo map, SQLite / lake physicalization, live capture, schedulers, dashboards, identity stitching, and all workflow overlay files.

When returning findings, diffs, or citations, carry the label tag for the affected target.

### Source-Gated Method Contract

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md` first.
2. REFERENCE-LOAD `workflow-delegated-review-patch`, `workflow-deep-thinking`, `workflow-code-review`, and `workflow-adversarial-artifact-review`. Do not APPLY them yet.
3. SOURCE-LOAD the target source pack below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before producing findings.
5. Only after source readiness, APPLY `workflow-delegated-review-patch` to enforce receipt, role, scope, patch, and CA-adjudication boundaries.
6. APPLY `workflow-deep-thinking` to frame fake-pass paths and material failure modes (especially the posture decision).
7. APPLY `workflow-code-review` to the producer and its test.
8. APPLY `workflow-adversarial-artifact-review` to the contract doc.
9. If `workflow-code-review` is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE`; do not emulate a strict code review inline. If `workflow-adversarial-artifact-review` is unavailable, do not make strict artifact-review claims about the contract doc; flag the limitation.

### Required Source Pack

Open and inspect these exact sources from the repo/worktree, not from pasted excerpts:

- `AGENTS.md`, `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/delegated-review-patch.md`, `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/decision-routing.md`
- `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
- target diff: `git diff 74373bb093d3cecd11f5e24a9d2dd2cecbc96223..c862c42f1098b1ea2207ff1f08d1634868856414 -- orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py orca-harness/tests/unit/test_creator_metric_silver_producer.py orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md`
- the three target files at `c862c42f`.
- contract and reference behavior the producer must conform to:
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md` (envelope, record_kind enum, MetricObservation, posture/value coupling, content_hash basis).
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md` (derived path grammar), targeted to raw_anchor / lane / record_id.
  - `orca-harness/cleaning/fragrantica_lake.py` (the only existing formal-envelope producer; the content_hash + envelope reference pattern).
  - `orca-harness/data_lake/root.py`, targeted to `append_record`, `for_test`, segment validation, and `anchor_shard`.
- the reused computation and its boundaries:
  - `orca-harness/capture_spine/creator_profile_current/instagram_metric_seed.py` and `orca/product/spines/capture/core/source_families/social_media/instagram/instagram_reels_creator_metric_seed_v0.json`.
  - `orca-harness/capture_spine/creator_profile_current/validation.py`, targeted to the rollup/posture/sample_support invariants the contract reuses.
  - `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md` (the upstream mapping that named this producer and the rollup payload).

Do not bulk-load unrelated review outputs, all prompt files, all product files, all data-lake directories, live capture artifacts, or external sources unless a specific material finding requires one narrow adjacent read.

### Review Questions

Find blocker or major issues first, especially:

- POSTURE (load-bearing): the contract and producer give a computed rollup aggregate (e.g. `average_views`) `metric_posture.kind: observed` with a numeric value when source-backed, reusing the posture vocabulary the Silver Vault contract defines for observed source-visible facts. Is applying `observed` to a derived/computed value sound, or does it overclaim provenance / blur the observed-vs-derived boundary? Should a rollup carry a distinct posture (e.g. `computed`/`derived`) or an explicit recipe/derivation marker so a downstream reader cannot mistake an aggregate for a raw observation? If this is design-level, return `NEEDS_ARCHITECTURE_PASS`.
- ENVELOPE CONFORMANCE: does each emitted record carry the Silver Vault common header correctly (record_id, raw_anchor, lane_namespace, producer_id, schema_version, producer_schema_version, content_hash + basis, record_kind ∈ {entity, relationship, observation}, payload_kind, producer_row_kind, source_surface, observed_at, captured_at, raw_refs, derived_refs)? Any deviation from the `fragrantica_lake.py` working pattern that would fail a future Silver reader?
- CONTENT_HASH: is the canonical-JSON-excluding-content_hash recipe reproduced exactly (sort_keys, compact separators, ensure_ascii, the `sha256:` prefix stored but excluded from the hash)? Does the test reproduce it independently rather than calling the producer's own helper?
- POSTURE/VALUE COUPLING: observed ⇔ numeric value and no reason; non-observed ⇔ null value and a reason; missing never zero. Is it enforced (fail-closed) for both observations and the rollup's per-metric aggregates? Does the test exercise the non-observed branch (the rollup's `posting_cadence` / `recent_velocity` are `not_attempted`)?
- NO-DRIFT: do the emitted rollup numbers equal the reused seed computation exactly? Could the producer silently diverge from `instagram_metric_seed.py` (e.g. by re-deriving instead of transcoding)?
- LINEAGE: does each rollup carry `derived_from_record` edges to its source MetricObservation records with matching content hashes? Is it a defect that the observation records carry `raw_refs` to the raw packet but NO `derived_ref` to the intermediate IG reels-grid projection (recorded only in `provenance`)? Is the `raw_anchor = single selected-projection packet` rule (fail-closed on multiple) correct?
- SUBJECT MODELING: is the `entity_key` subject shape sound (account `native_id` = handle, reel `native_id` = shortcode, plus `orca_platform_account_id` / `published_by_account_native_id`) vs the contract's `{namespace, kind, native_id}`? Does omitting co-emitted PlatformAccountEntity / public_content_object entity records and the `content_published_by_account` relationship leave the observation subject under-identified or unsafe for v0?
- SCOPE / CLAIM DISCIPLINE: does anything exceed the stated v0 scope (does it re-point `creator_profile_current`, write the real lake, emit entity/relationship records, or introduce cross-platform identity)? Are the non-claims adequate, and is there any readiness / validation / buyer-proof overclaim in the contract doc?
- FAKE-PASS: could a non-conformant record pass the test? Where is test coverage thinnest?

### Patch Authority

You may patch only the three target files listed above, and only to close blocker or major issues found in this review. Do not stage, commit, push, open PRs, install dependencies, enable network access, run live capture, write the real data lake, or edit any source ledger / seed / contract outside the three targets.

If the correct fix requires changing the Silver Vault record contract, the lake writer, the reused seed computation, the validator, product specs, or workflow overlay files, do not patch it — flag it as off-scope.

If a design-level problem is found (most likely the posture decision), return `NEEDS_ARCHITECTURE_PASS`, stop patching, revert any partial diff, and report findings only. A partial patch must not survive by inertia.

### Validation Expectations

If you patch, run the narrowest relevant validation, normally from `orca-harness`:

- `python -m pytest -q -p no:cacheprovider tests\unit\test_creator_metric_silver_producer.py`
- the baseline creator suites: `python -m pytest -q -p no:cacheprovider tests\unit\test_creator_registry_index.py tests\unit\test_creator_public_handle_linkage.py tests\unit\test_creator_profile_current_static_view.py tests\unit\test_instagram_reels_creator_metric_seed.py tests\unit\test_youtube_creator_metric_seed.py`

Also run from repo root when relevant:

- `git diff --check`
- `python .agents\hooks\check_map_links.py --strict` if the contract doc or any retrieval header changes.

Report exact commands and results. Preserve real failures; never mask a failing test or gate.

### Output Contract

Write the full review report to:

- `docs/review-outputs/adversarial-artifact-reviews/creator_metric_silver_producer_adversarial_code_review_v0.md`

If the report write fails, return a blocked chat result with `review_location: chat_only_current_thread`, no `report_path`, and enough detail to route.

Report structure: (1) commission, lane binding, and actor/model-family receipt; (2) source context status; (3) findings first, ordered by severity (critical, major, minor); (4) for each finding: severity, target label, location, issue, evidence, impact, minimum_closure_condition, next_authorized_action, and whether patched; (5) unified diff for any target-file changes; (6) per-change neutral source citations, decision-sufficient in substance; (7) controller verdict and residual-risk note; (8) validation run status with exact commands; (9) off-scope flags; (10) CA adjudication packet; (11) review-use boundary.

After writing the report, return this compact chat YAML:

```yaml
review_summary:
  status: completed | blocked
  report_path: docs/review-outputs/adversarial-artifact-reviews/creator_metric_silver_producer_adversarial_code_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | needs_architecture_pass | blocked
  reviewed_by: operator_to_fill
  authored_by: Anthropic Claude (Opus)
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

If no issues are found, say that clearly and name residual risks or test gaps. Your output is decision input only. The commissioning home model must adjudicate before any change is kept.

### Review-Use Boundary

This delegated review-and-patch result is decision input only. The controller's diff, citations, and verdict are claims to adjudicate, not premises to inherit. It is not owner acceptance, validation proof, readiness, deployment, source-capture authorization, live-lake authorization, SQLite adoption, or permission to keep any patch without home-model adjudication.
