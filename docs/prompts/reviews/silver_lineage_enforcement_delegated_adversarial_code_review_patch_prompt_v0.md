# Silver Lineage Enforcement Delegated Adversarial Code Review-and-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Commission a de-correlated repo-mode adversarial code review-and-patch pass
  for PR #456, the Silver lineage helper/validator enforcement bridge for
  transcript product mentions.
use_when:
  - Couriering PR #456 for independent review before the Silver lineage enforcement patch is treated as settled.
  - Checking whether transcript product mention records now carry exact raw or derived transcript lineage without creating a second persisted lineage home or broad lake enforcement.
authority_boundary: retrieval_only
branch_or_commit: codex/silver-lineage-enforcement @ f3c9e802f1aed65918b107f4b3c08550ba01ecdb, base codex/silver-lineage-kit @ 48f3e3b43d6de4d73bc2609bb10737b6967c5860
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/safety-rules.md
  - .agents/workflow-overlay/validation-gates.md
  - docs/workflows/silver_lineage_kit_genericity_check_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/silver_lineage_kit_delegated_adversarial_review_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
input_hashes:
  docs/workflows/silver_lineage_kit_genericity_check_v0.md: E2F2580BE3ACE932675A700F4E36F74D0EDD4FEC8D4B0809A857EE3A0A0CBF9F
  docs/review-outputs/adversarial-artifact-reviews/silver_lineage_kit_delegated_adversarial_review_v0.md: E9EEA2CED0CFF9CC9713FA7E08FBCDB83CD626F4273EB79C9C7C8F11682D5205
  orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md: 6891BC540AD9F9347F8A6569D45425657DF47BBDC8F99813B123BE73DCDF215F
  orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md: 688B56B7A9CA2311847637B1139887AC36C7AC31C6954017DAD711DED36A9577
  orca-harness/data_lake/root.py: EA78BCEF550E35A69A7A495FA76D067C1069469C821CCC5A21D1FFA84971AE6D
  orca-harness/cleaning/models.py: A73412ED64574339013F624888C6A949A0954D1CA86AC0C53CB5969139D41D7F
  orca-harness/cleaning/transcript_product_extractor.py: 0E50E019E4B519BD3940434040DC6884972BB8FC0BB5348CAE3409B2BF27F4AD
  orca-harness/cleaning/transcript_product_lake.py: 1EF278A2C4232798AF9B29DCB79A30DB36654716220C28EC6A717BDA56280EBA
  orca-harness/data_lake/silver_lineage.py: F41D49F35D895E05EE16B05B2A6BD8F3AD4DF5CB27AAF5E33ED19279974307D7
  orca-harness/runners/run_ig_reels_product_extract.py: 418F36555C5F2C19E5C0919770C8DE6AE2E2008B52339B09B79231E666889566
  orca-harness/runners/run_transcript_product_extract.py: 9A87E713DCA94E18CFDB7CE71232A64F15CFF605A0654FF143CCBD7A4B520442
  orca-harness/tests/unit/test_silver_lineage.py: C597B191DF0072279DCB9E04F97F8DE31A191C17F143AC4812659B64E3BE25BC
  orca-harness/tests/unit/test_transcript_product_lake.py: 83080C8BF527BD6F34EA3EE47AB84977FF0595A0A22269F6B2EFF3EC24C1B657
stale_if:
  - PR #456 is closed, merged, retargeted, or its head/base changes before review.
  - Target worktree `C:\Users\vmon7\Desktop\projects\orca\worktrees\silver-lineage-enforcement-codex` is not on `codex/silver-lineage-enforcement` at f3c9e802f1aed65918b107f4b3c08550ba01ecdb.
  - Any target file hash differs from the hash recorded here before review starts.
  - Orca delegated-review-patch, review-lanes, prompt-orchestration, source-loading, safety, or validation-gates overlay authority changes before review.
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` constants apply where present; deltas are stated here.

- output_mode: `file-write` for this prompt artifact, plus `paste-ready-chat` copy for couriering.
- prompt_artifact_path: `docs/prompts/reviews/silver_lineage_enforcement_delegated_adversarial_code_review_patch_prompt_v0.md`.
- template_kind: `review` plus delegated review-and-patch commission semantics from `.agents/workflow-overlay/delegated-review-patch.md`.
- authorization_basis: current owner instruction to use delegated review-and-patch for the multi-file PR #456 implementation, with overlay already allowing `delegated_code_review_and_patch`.
- edit_permission_for_receiver: `patch-only` inside the seven named target files below; all other paths are read-only / flag-only.
- workspace_path: `C:\Users\vmon7\Desktop\projects\orca`.
- expected_worktree_path: `C:\Users\vmon7\Desktop\projects\orca\worktrees\silver-lineage-enforcement-codex`.
- branch_or_commit_reference: `codex/silver-lineage-enforcement @ f3c9e802f1aed65918b107f4b3c08550ba01ecdb`.
- reviewed_diff: `48f3e3b43d6de4d73bc2609bb10737b6967c5860..f3c9e802f1aed65918b107f4b3c08550ba01ecdb`.
- target_files_or_dirs:
  - `orca-harness/cleaning/transcript_product_extractor.py`
  - `orca-harness/cleaning/transcript_product_lake.py`
  - `orca-harness/data_lake/silver_lineage.py`
  - `orca-harness/runners/run_ig_reels_product_extract.py`
  - `orca-harness/runners/run_transcript_product_extract.py`
  - `orca-harness/tests/unit/test_silver_lineage.py`
  - `orca-harness/tests/unit/test_transcript_product_lake.py`
- downstream_report_path: `docs/review-outputs/adversarial-artifact-reviews/silver_lineage_enforcement_delegated_adversarial_code_review_patch_v0.md`.
- dirty_state_allowance: target worktree must be clean before review starts. If this prompt exists in a separate prompt branch, do not treat that branch as the implementation target.
- controlling_source_state: checked before prompt creation; PR #456 open/draft, head `f3c9e802f1aed65918b107f4b3c08550ba01ecdb`, base `48f3e3b43d6de4d73bc2609bb10737b6967c5860`; target worktree clean on `codex/silver-lineage-enforcement`.
- doctrine_change_decision: no new doctrine change in this prompt. The multi-file code-diff sibling mode is already present in `.agents/workflow-overlay/delegated-review-patch.md` on the current base.
- validation_evidence_already_observed:
  - `git diff --check` passed before the PR #456 commit.
  - `python -m pytest -q tests\unit\test_silver_lineage.py tests\unit\test_transcript_product_lake.py tests\unit\test_ig_reels_product_extract.py tests\contract\test_no_llm_imports.py` passed, 33 tests.
- receiver_validation_expectation: rerun focused tests after any patch; run broader tests only when the patch changes behavior outside the focused Silver lineage/product extraction surface.
- thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
  if_changed_reason: not_applicable

## Delegated Review-And-Patch Commission

### Lane Binding

- overlay_status: `provisional_opt_in`, explicitly invoked by the owner for PR #456.
- target_kind: `delegated_code_review_and_patch`.
- operating_contract_pointer: `.agents/workflow-overlay/delegated-review-patch.md`.
- review_lane: code / implementation change packet, using `workflow-code-review` after source readiness. This is not artifact review and not a merge of code and artifact review.
- mode: `base-subagent` / repo-mode controller. Do not use split-executor.
- actor_model_family_receipt:
  - author_home_model_family: OpenAI / Codex, this commissioning lane.
  - controller_model_family: `operator_to_fill`; must be a different upstream vendor / model lineage from OpenAI to satisfy `cross_vendor_discovery`.
  - current_receiving_actor_role: controller.
  - dispatch_mode: external-controller-courier.
  - de_correlation_status: operator must fill before review; block strict cross-vendor discovery claims if unsatisfied.
- de_correlation: this is a who-constraint, not a runtime-model recommendation. Do not recommend, rank, prescribe, or imply a concrete runtime model.
- subagent_authority: no tester/testee shortcut. The commissioning/home model must not satisfy this by reviewing its own patch. If your runtime is the same author/home family and no different-family controller is actually receiving this prompt, stop before review.
- prompt_rendering: this filed prompt is the orchestrated prompt. The receiver must inspect the pinned repo/worktree directly; do not substitute this prompt body, a summary, or a recreated source pack for the source tree.

### Target

- targets:
  - label: `[product-input-contract]`
    path: `orca-harness/cleaning/transcript_product_extractor.py`
    bounded_patch_scope: only the transcript input metadata/ref fields needed by product mention extraction.
  - label: `[product-mention-writer]`
    path: `orca-harness/cleaning/transcript_product_lake.py`
    bounded_patch_scope: only wrapping product-mention payloads with the Silver Vault Common Record Header via the helper and requiring full source-backed refs.
  - label: `[silver-lineage-helper]`
    path: `orca-harness/data_lake/silver_lineage.py`
    bounded_patch_scope: only the generic helper/validator for Silver Vault lineage/header records.
  - label: `[ig-product-runner]`
    path: `orca-harness/runners/run_ig_reels_product_extract.py`
    bounded_patch_scope: only exact IG ASR derived-record refs for product extraction inputs.
  - label: `[youtube-product-runner]`
    path: `orca-harness/runners/run_transcript_product_extract.py`
    bounded_patch_scope: only exact YouTube caption raw-packet refs and ASR derived-record refs for product extraction inputs.
  - label: `[silver-lineage-tests]`
    path: `orca-harness/tests/unit/test_silver_lineage.py`
    bounded_patch_scope: only unit tests for helper/validator behavior.
  - label: `[product-lineage-tests]`
    path: `orca-harness/tests/unit/test_transcript_product_lake.py`
    bounded_patch_scope: only product mention persistence and runner lineage tests.
- why_read_only_insufficient: this patch creates the first generic lineage helper and first adopting producer path. A reviewer who finds a fake-full-source-backed path, wrong hash basis, row-locator miss, or duplicate lineage home can often close it with a bounded correction in the same seven files; a read-only loop would force a correlated home-model patch on the exact guardrails under review.
- off_scope: read-only / flag-only for all other files, including Silver Vault contracts, genericity/review docs, `DataLakeRoot`, live F-drive data, historical records, global data-lake enforcement, schema migrations, IG/YT capture mechanics, source packets, ASR producers, and every protected path in `.agents/workflow-overlay/safety-rules.md`.

When returning findings, diffs, or citations, carry the label tag for the affected target.

## Source-Gated Method Contract

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md` first.
2. REFERENCE-LOAD `workflow-delegated-review-patch`, `workflow-deep-thinking`, and `workflow-code-review`. Do not APPLY them yet.
3. SOURCE-LOAD the target source pack below.
4. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` before producing findings.
5. Only after source readiness, APPLY `workflow-delegated-review-patch` to enforce receipt, role, scope, patch, and CA-adjudication boundaries.
6. APPLY `workflow-deep-thinking` to frame material failure modes and fake-success paths.
7. APPLY `workflow-code-review` to the implementation, runners, and tests.
8. If `workflow-code-review` is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE`; do not emulate a strict code review inline.

## Required Source Pack

Open and inspect these exact sources from the repo/worktree, not from pasted excerpts:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.agents/workflow-overlay/validation-gates.md`
- target diff: `git diff 48f3e3b43d6de4d73bc2609bb10737b6967c5860..f3c9e802f1aed65918b107f4b3c08550ba01ecdb -- orca-harness/cleaning/transcript_product_extractor.py orca-harness/cleaning/transcript_product_lake.py orca-harness/data_lake/silver_lineage.py orca-harness/runners/run_ig_reels_product_extract.py orca-harness/runners/run_transcript_product_extract.py orca-harness/tests/unit/test_silver_lineage.py orca-harness/tests/unit/test_transcript_product_lake.py`
- current target files at commit `f3c9e802f1aed65918b107f4b3c08550ba01ecdb`.
- design/review sources:
  - `docs/workflows/silver_lineage_kit_genericity_check_v0.md`, especially the Common Record Header relationship, `row_locator`, product mentions, `lineage_limitations`, and patch implications sections.
  - `docs/review-outputs/adversarial-artifact-reviews/silver_lineage_kit_delegated_adversarial_review_v0.md`, especially AR-01 and AR-02.
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md`, especially Common Record Header and `raw_refs` / `derived_refs`.
  - `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`, targeted to derived-record and re-derive-not-migrate boundaries.
  - `orca-harness/data_lake/root.py`, targeted to record-set member SHA and raw packet load behavior.
  - `orca-harness/cleaning/models.py`, targeted to raw/derived/projection ref precedent.

Do not bulk-load unrelated review outputs, all prompt files, all product files, live data lake contents, all source capture packets, all ASR/caption producers, historical lanes, or external sources unless a specific material finding requires one narrow adjacent read.

## Review Questions

Find blocker or major issues first, especially:

- Does `[silver-lineage-helper]` populate the authoritative Silver Vault Common Record Header fields directly, without creating or allowing a second persisted `silver_lineage` home?
- Does the helper reject payload collisions, missing refs, malformed refs, incomplete `row_locator`, uncontrolled limitations, or `content_hash` states that would create fake full-source-backed records?
- Is `content_hash` deterministic, does it exclude `content_hash` itself, and could it become unstable due to ordering, mutation, or caller-provided header fields?
- Does `[product-mention-writer]` require exact raw or derived transcript refs for product mention records while preserving the existing payload fields downstream consumers expect?
- Do the caption and ASR paths in `[youtube-product-runner]` identify exact consumed artifacts, including packet id, slice/file path/hash for captions and exact `transcript_asr` record + record-set member SHA for ASR?
- Does `[ig-product-runner]` identify the exact consumed IG ASR record, with the same hash-basis discipline and no silent fallback to a shortcode-only anchor?
- Are `source_namespace`, `source_surface`, `observed_at`, and `captured_at` values accurate enough to avoid claiming source completeness or timing certainty that the pipeline does not have?
- Do the tests prove failure visibility for missing lineage, not just happy-path field presence?
- Did the patch accidentally add broad Silver Vault schema redesign, universal wrapper/migration behavior, global `DataLakeRoot.append_record` enforcement, F-drive live writes, or IG/YT capture mechanics?
- If the implementation intentionally starts with product mentions only, is that boundary mechanically enforced without making the helper product-mention-specific?
- Are record-set lane names, marker SHA fallbacks, and hash basis labels consistent with `DataLakeRoot` behavior and existing lane names?
- Does the implementation fail visibly when source refs cannot be resolved, instead of writing apparently source-backed Silver records with empty refs or hand-authored limitations?

## Patch Authority

You may patch only the seven target files listed above, and only to close blocker or major issues found in this review. Do not stage, commit, push, open PRs, install dependencies, run network access, run live capture, or write to F-drive.

If the correct fix requires changing Silver Vault contracts, genericity docs, workflow overlays, `DataLakeRoot`, capture producers, ASR/caption packet producers, lake schemas, live data, or a broader runner architecture, do not patch it. Flag it as off-scope.

If a design-level problem is found, return `NEEDS_ARCHITECTURE_PASS`, stop patching, revert any partial diff, and report findings only. A partial patch must not survive by inertia.

## Validation Expectations

If you patch, run the narrowest relevant validation available.

From repo root:

- `git diff --check`

From `orca-harness`:

- `python -m compileall -q data_lake\silver_lineage.py cleaning\transcript_product_extractor.py cleaning\transcript_product_lake.py runners\run_transcript_product_extract.py runners\run_ig_reels_product_extract.py`
- `python -m pytest -q tests\unit\test_silver_lineage.py tests\unit\test_transcript_product_lake.py tests\unit\test_ig_reels_product_extract.py tests\contract\test_no_llm_imports.py`

Also run `python -m pytest -q tests\unit\test_ig_reels_behavioral_lake.py` if your patch touches IG lane behavior beyond exact derived-ref wiring. Run broader tests only if your patch changes shared helper semantics in a way the focused tests cannot cover. Report exact commands and results. Preserve real failures.

## Output Contract

Write the full review report to:

- `docs/review-outputs/adversarial-artifact-reviews/silver_lineage_enforcement_delegated_adversarial_code_review_patch_v0.md`

If the report write fails, return a blocked chat result with `review_location: chat_only_current_thread`, no `report_path`, and enough detail to route.

Report structure:

1. Commission, lane binding, target kind, and actor/model-family receipt.
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
  report_path: docs/review-outputs/adversarial-artifact-reviews/silver_lineage_enforcement_delegated_adversarial_code_review_patch_v0.md
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

## Review-Use Boundary

This delegated review-and-patch result is decision input only. The controller's diff, citations, and verdict are claims to adjudicate, not premises to inherit. It is not owner acceptance, validation proof, readiness, deployment, Silver Vault contract ratification, live-lake authorization, source-capture authorization, F-drive write authorization, or permission to keep any patch without Chief Architect adjudication.
