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

## Objective And Intended Decision

- objective: obtain a de-correlated (cross-vendor) adversarial read, plus a bounded patch where warranted, on whether the lake-native creator-metric Silver producer and its new `MetricRollupObservation` record contract are sound enough to keep and build on.
- intended_decision: the commissioning home model (Chief Architect) decides `accept` / `accept_with_friction` / `patch_before_acceptance` / `reject` / `NEEDS_ARCHITECTURE_PASS` for STEP-01 (contract) + STEP-02 (producer + test) **before** the deferred STEP-03 (re-pointing `creator_profile_current` onto these records) builds on them.

## What This Is For / Done Looks Like (fitness reference)

Pointer-preferred (the controlling upstream goal is this lane's goal frame anchor; the architecture target is `creator_profile_current_lake_native_record_mapping_v0.md`):

> **Goal:** make the creator registry source-backed and lake-aware so creator metrics derive from Silver / data-lake records (not a hand-kept static seed) and the registry stops going manually stale.
> **Done looks like:** creator metrics exist as Silver Vault-conformant `MetricObservation` + `MetricRollupObservation` records, derived from the source computation with **no drift**, honest posture (missing ≠ zero), and source→rollup lineage — not a Silver-shaped copy of a hand-kept seed.

This reference is the **executor target and an alignment axis the reviewer must ALSO attack** (is the goal/signal itself right — e.g., does "observed posture for a computed aggregate" actually serve "source-backed"?). It is **not** a pass-if-matches bar, and a later review must not grade conformance to this prompt. For the code targets, the fitness bar is the code's own ground truth (the Silver Vault record contract, the no-drift test, the reused seed computation); the fitness-reference axis above is bound for the authored-artifact (contract doc) portion per Orca review doctrine.

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 — constants bound; per-prompt deltas stated here.

```yaml
orca_start_preflight:
  agents_md_read: yes_current_task_context
  overlay_readme_read: yes_current_task_context        # .agents/workflow-overlay/README.md
  source_pack: bounded_custom_creator_metric_silver_producer_review_pack   # enumerated under Required Source Pack
  repo_map_decision: not_needed
  repo_map_reason: >
    Bounded three-file review with an explicitly enumerated source pack and named
    targets; no repo-wide map traversal is required to bound the review.
  workspace_path: C:\Users\vmon7\Desktop\projects\orca                     # per orca_preflight_defaults_v0
  expected_worktree_path: C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-silver-metric-producer
  branch_or_commit_reference: claude/creator-silver-metric-producer @ c862c42f1098b1ea2207ff1f08d1634868856414
  dirty_state_allowance: >
    Target worktree clean at c862c42f before review. The prompt-file commit is
    later on the same branch; review the pinned target diff and ignore the
    prompt-file commit except as dispatch context.
  controlling_source_state: >
    Orca overlay, source-loading, prompt-policy, and review-lane files clean as of
    the branch base; not modified by this lane (checked before prompt creation).
  edit_permission: patch-only            # the three named target files only; all else read-only / flag-only
  output_mode: file-write                # this prompt artifact; the receiver's output mode is review-report; a paste-ready-chat copy carries the courier
  doctrine_change_decision: >
    This review prompt does not change doctrine. The reviewed WORK adds a
    producer-owned MetricRollupObservation payload_kind and contract doc under the
    existing creator-registry / lake-native-mapping / Silver Vault record-contract
    boundaries; that addition's propagation is the reviewed lane's responsibility
    and is surfaced here as a review question, not asserted as settled by this prompt.
  isolation_decision: existing isolated worktree off origin/main; no new worktree for a bounded review-and-patch pass.
  validation_gates: >
    Receiver reruns the producer test + the baseline creator suites, git diff --check,
    and check_map_links --strict if the contract doc or any retrieval header changes;
    evidence recorded in the durable review report.
  external_source_boundary: >
    External workflow source is read-only from Orca work and is not Orca authority;
    jb is not Orca authority; installed skills are deployment copies. No jb or external
    templates are imported by this prompt.
pin_note: >
  Pinned by commit SHA, not per-file SHA256. The repo is autocrlf (i/lf w/crlf), so a
  working-tree SHA256 will not match a fresh LF checkout; compare against c862c42f.
reviewed_diff: 74373bb093d3cecd11f5e24a9d2dd2cecbc96223..c862c42f1098b1ea2207ff1f08d1634868856414
prompt_artifact_path: docs/prompts/reviews/creator_metric_silver_producer_delegated_adversarial_code_review_patch_prompt_v0.md
downstream_report_path: docs/review-outputs/adversarial-artifact-reviews/creator_metric_silver_producer_adversarial_code_review_v0.md
template_kind: review   # delegated-review-patch, delegated_code_review_and_patch sibling mode
template_target: adversarial-artifact-review (registry: model-neutral) for the contract-doc portion; code review lane has no model-target template — prompt-shaping only, never runtime-model routing
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
  note: >
    This review continues the creator-intelligence lane workstream; the anchor goal
    and success signal are carried as the fitness reference above. Thread-local
    orientation only — not authority, evidence, readiness, or routing state.
```

- validation_evidence_already_observed (re-run to confirm; do not trust):
  - `python -m pytest -q -p no:cacheprovider orca-harness\tests\unit\test_creator_metric_silver_producer.py` passed, 4 tests.
  - baseline 5 creator suites passed, 52 tests; together with the new test, 56 passed.
  - `python orca-harness\runners\run_creator_profile_current_materialize.py --check` reported up to date (read model untouched).
  - `python .agents\hooks\check_map_links.py --strict` passed with 0 findings; `git diff --check` clean.

## Delegated Review-And-Patch Commission

### Lane Binding

- overlay_status: `provisional_opt_in`, explicitly invoked by the owner for this work unit.
- operating_contract_pointer: `.agents/workflow-overlay/delegated-review-patch.md`.
- target_kind: `delegated_code_review_and_patch` (bounded multi-file implementation diff; the named three-file set is the only patchable surface and cannot silently widen).
- review_lane: mixed — `workflow-code-review` for `silver_metric_producer.py` and its test (primary), and `workflow-adversarial-artifact-review` for the authored contract doc `creator_metric_silver_record_contract_v0.md`. Implementation/code review and artifact review remain separate lanes; this commission uses both as methods, it does not merge them.
- access: `repo` (default). The receiver inspects the pinned branch/worktree directly.
- actor_model_family_receipt:
  - author_home_model_family: Anthropic / Claude (this commissioning lane).
  - controller_model_family: `operator_to_fill`; must be a different vendor / model lineage from Anthropic to satisfy `cross_vendor_discovery` (vendor = upstream developer/provider, not host/reseller/wrapper).
  - current_receiving_actor_role: controller.
  - dispatch_mode: external-controller-courier.
  - de_correlation_status: operator must fill before review; block strict cross-vendor discovery (no-new-seam) claims if unsatisfied. A same-vendor delegate may claim only bounded `same_vendor_sanity` and must record a `same_vendor_rationale`.
- de_correlation: this is a who-constraint recorded in the commission, not a model recommendation. Do not recommend, rank, prescribe, or imply a runtime model anywhere in the review.
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
- off_scope (read-only / flag-only): the Silver Vault record contract and other `orca/product/spines/data_lake/authority/` docs; `instagram_metric_seed.py` and the seed JSON (the reused computation); `materialize.py` / `validation.py` / the `creator_profile_current` view; `fragrantica_lake.py`; `data_lake/root.py`; source ledger JSON; product specs; the repo map; SQLite / lake physicalization; live capture; schedulers; dashboards; identity stitching; and all `.agents/workflow-overlay/` files.

When returning findings, diffs, or citations, carry the label tag for the affected target.

### Source-Gated Method Contract

REFERENCE-LOAD the method instructions below. Do not APPLY them yet — before source readiness use them only to prepare a neutral source-reading lens. After the source pack is loaded and `SOURCE_CONTEXT_READY` is declared, APPLY the methods to the loaded source context.

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md` first.
2. REFERENCE-LOAD `workflow-delegated-review-patch`, `workflow-deep-thinking`, `workflow-code-review`, and `workflow-adversarial-artifact-review`.
3. Do not APPLY any method yet.
4. SOURCE-LOAD the Required Source Pack below.
5. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` (name missing sources, gaps, exclusions, conflicts).
6. Only after that declaration, APPLY `workflow-delegated-review-patch` to enforce receipt, role, scope, patch, and CA-adjudication boundaries.
7. APPLY `workflow-deep-thinking` to frame the boundary problem, failure modes, and decision criteria (especially the posture decision) before listing findings. It does not widen scope or authorize patching.
8. APPLY `workflow-code-review` to the producer and its test.
9. APPLY `workflow-adversarial-artifact-review` to the contract doc.
10. If `workflow-code-review` is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE`; do not emulate a strict code review inline. If `workflow-adversarial-artifact-review` is unavailable, unresolved, or not applied, do not emit formal verdicts/severity authority/validation/readiness claims for the contract doc — return advisory-only and name the missing skill.

### Required Source Pack (bounded_custom_creator_metric_silver_producer_review_pack)

Open and inspect these exact sources from the repo/worktree, not from pasted excerpts:

- `AGENTS.md`, `.agents/workflow-overlay/README.md`, `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/delegated-review-patch.md`, `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/decision-routing.md`
- `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
- target diff: `git diff 74373bb093d3cecd11f5e24a9d2dd2cecbc96223..c862c42f1098b1ea2207ff1f08d1634868856414 -- orca-harness/capture_spine/creator_profile_current/silver_metric_producer.py orca-harness/tests/unit/test_creator_metric_silver_producer.py orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md`
- the three target files at `c862c42f`.
- contract and reference behavior the producer must conform to: `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`; `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md` (raw_anchor / lane / record_id grammar); `orca-harness/cleaning/fragrantica_lake.py` (the only existing formal-envelope producer — content_hash + envelope reference); `orca-harness/data_lake/root.py` (`append_record`, `for_test`, segment validation, `anchor_shard`).
- the reused computation and its boundaries: `orca-harness/capture_spine/creator_profile_current/instagram_metric_seed.py` and `orca/product/spines/capture/core/source_families/social_media/instagram/instagram_reels_creator_metric_seed_v0.json`; `orca-harness/capture_spine/creator_profile_current/validation.py` (the rollup/posture/sample_support invariants the contract reuses); `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md`.

Do not bulk-load unrelated review outputs, all prompt files, all product files, all data-lake directories, live capture artifacts, or external sources unless a specific material finding requires one narrow adjacent read. Keep source loading within the Orca source-loading budgets; if the pack would overflow live context, split the unit and checkpoint per `.agents/workflow-overlay/prompt-orchestration.md`.

### Review Questions (findings-first; severity critical | major | minor for priority only)

Be maximally adversarial about material decision-relevant failure modes within the commission-bound target. Find blocker/major issues first, especially:

- POSTURE (load-bearing): the contract and producer give a computed rollup aggregate (e.g. `average_views`) `metric_posture.kind: observed` with a numeric value when source-backed, reusing the posture vocabulary the Silver Vault contract defines for observed source-visible facts. Is applying `observed` to a derived/computed value sound, or does it overclaim provenance / blur the observed-vs-derived boundary? Should a rollup carry a distinct posture (e.g. `computed`/`derived`) or an explicit recipe/derivation marker so a reader cannot mistake an aggregate for a raw observation? This is the primary alignment axis to attack; if it is design-level, return `NEEDS_ARCHITECTURE_PASS`.
- ENVELOPE CONFORMANCE: does each record carry the Silver Vault common header correctly (record_id, raw_anchor, lane_namespace, producer_id, schema_version, producer_schema_version, content_hash + basis, record_kind ∈ {entity, relationship, observation}, payload_kind, producer_row_kind, source_surface, observed_at, captured_at, raw_refs, derived_refs)? Any deviation from the `fragrantica_lake.py` working pattern that would fail a future Silver reader?
- CONTENT_HASH: is the canonical-JSON-excluding-content_hash recipe reproduced exactly (sort_keys, compact separators, ensure_ascii, the `sha256:` prefix stored but excluded from the hash)? Does the test reproduce it independently rather than calling the producer's own helper?
- POSTURE/VALUE COUPLING: observed ⇔ numeric value and no reason; non-observed ⇔ null value and a reason; missing never zero. Enforced (fail-closed) for both observations and the rollup's per-metric aggregates? Does the test exercise the non-observed branch (the rollup's `posting_cadence` / `recent_velocity` are `not_attempted`)?
- NO-DRIFT: do the emitted rollup numbers equal the reused seed computation exactly? Could the producer silently diverge from `instagram_metric_seed.py` (e.g. by re-deriving instead of transcoding)?
- LINEAGE: does each rollup carry `derived_from_record` edges to its source MetricObservation records with matching content hashes? Is it a defect that the observation records carry `raw_refs` to the raw packet but NO `derived_ref` to the intermediate IG reels-grid projection (recorded only in `provenance`)? Is the `raw_anchor = single selected-projection packet` rule (fail-closed on multiple) correct?
- SUBJECT MODELING: is the `entity_key` subject shape sound (account `native_id` = handle, reel `native_id` = shortcode, plus `orca_platform_account_id` / `published_by_account_native_id`) vs the contract's `{namespace, kind, native_id}`? Does omitting co-emitted entity / relationship records leave the observation subject under-identified or unsafe for v0?
- SCOPE / CLAIM DISCIPLINE: does anything exceed the stated v0 scope (re-point `creator_profile_current`, write the real lake, emit entity/relationship records, introduce cross-platform identity)? Are the non-claims adequate; any readiness / validation / buyer-proof overclaim in the contract doc?
- FAKE-PASS: could a non-conformant record pass the test? Where is coverage thinnest?

For each actionable finding, state `minimum_closure_condition` (the required end state, not how to implement it) and `next_authorized_action` (what this lane may do next under its authority). Optional hardening must be labeled optional and non-required. Do not emit `patch_queue_entry`; bounded patches go directly to the named target files under Patch Authority.

### Patch Authority

You may patch only the three target files listed above, and only to close blocker or major issues found in this review. Do not stage, commit, push, open PRs, install dependencies, enable network access, run live capture, write the real data lake, or edit any source ledger / seed / contract outside the three targets.

If the correct fix requires changing the Silver Vault record contract, the lake writer, the reused seed computation, the validator, product specs, or workflow overlay files, do not patch it — flag it as off-scope. If a design-level problem is found (most likely the posture decision), return `NEEDS_ARCHITECTURE_PASS`, stop patching, revert any partial diff, and report findings only. A partial patch must not survive by inertia.

### Validation Expectations

If you patch, run the narrowest relevant validation, normally from `orca-harness`:

- `python -m pytest -q -p no:cacheprovider tests\unit\test_creator_metric_silver_producer.py`
- the baseline creator suites: `python -m pytest -q -p no:cacheprovider tests\unit\test_creator_registry_index.py tests\unit\test_creator_public_handle_linkage.py tests\unit\test_creator_profile_current_static_view.py tests\unit\test_instagram_reels_creator_metric_seed.py tests\unit\test_youtube_creator_metric_seed.py`

Also from repo root when relevant: `git diff --check`; `python .agents\hooks\check_map_links.py --strict` if the contract doc or any retrieval header changes. Report exact commands and results. Preserve real failures; never mask a failing test or gate.

### Output Contract

Output mode `review-report`. Write the full review report to:

- `docs/review-outputs/adversarial-artifact-reviews/creator_metric_silver_producer_adversarial_code_review_v0.md`

If the report write fails, return a blocked chat result with `status: failed`, `review_location: chat_only_current_thread`, `recommendation: blocked`, no `report_path`, the failed path named, and enough human-readable detail to route.

Report consumption order (CA-facing): commission → target → authority → decision criteria → evidence → reviewer verdict/recommendation. Report structure: (1) commission, lane binding, and actor/model-family receipt; (2) source context status; (3) findings first, ordered by severity; (4) per finding: severity, target label, location, issue, evidence, impact, `minimum_closure_condition`, `next_authorized_action`, patched?; (5) unified diff for any target-file changes; (6) neutral per-change source citations, decision-sufficient in substance; (7) controller verdict and residual-risk note; (8) validation run status with exact commands; (9) off-scope flags; (10) review-use boundary. Record `reviewed_by` and `authored_by` on the durable report (operator/CA-supplied; `unrecorded` allowed, never fabricated).

After the report is written, return the compact `review_summary` YAML courier:

```yaml
review_summary:
  status: completed | blocked
  report_path: docs/review-outputs/adversarial-artifact-reviews/creator_metric_silver_producer_adversarial_code_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | needs_architecture_pass | blocked
  reviewed_by: operator_to_fill
  authored_by: operator_to_fill   # the model+version that authored the reviewed work; CA/operator-supplied, unrecorded allowed, never fabricated
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

### Adjudicator Next-Moves Pass (after the verdict)

This runs after the verdict and is for the **adjudicator** — the commissioning Chief Architect in this delegated pass, never the delegate mid-review. It does not widen review scope or authorize patching. Close with a next-moves pass: batch all admin/lifecycle follow-ups (commit, push, PR, merge of any adjudicated-kept patch) into **one** named step with no deep-thinking; deep-think only the few **material** moves that need judgment (here: the posture decision's disposition, and whether STEP-03 — re-pointing `creator_profile_current` onto these records — may now proceed). The exact admin/material shape is owned by `.agents/workflow-overlay/communication-style.md` (Review Adjudication Next Step).

### Review-Use Boundary

This delegated review-and-patch result is decision input only. The controller's diff, citations, and verdict are claims to adjudicate, not premises to inherit. It is not owner acceptance, validation proof, readiness, deployment, source-capture authorization, live-lake authorization, SQLite adoption, or permission to keep any patch without home-model (Chief Architect) adjudication. No part of this prompt recommends, ranks, or implies a runtime model; the cross-vendor constraint is a who-constraint only.
