# Cleaning Spine Playbook Capture -> ECR -> Cleaning Smoke Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact
scope: >
  Read-only adversarial code/evidence review prompt for the playbook-led real-data
  Source Capture -> ECR source-side receipts -> CleaningPacket smoke on the
  Cleaning Spine continuation branch.
use_when:
  - Commissioning an independent reviewer to inspect the real-data smoke runner,
    emitted evidence, and code patch that preserves source-visible retail capture
    limitations without hiding valid PDP substrates.
  - Checking whether the run honestly links raw/projection/ECR/Cleaning material
    and avoids overclaiming end-to-end readiness.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/review-lanes.md
  - orca/product/spines/capture/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/source_capture_toolbox/capture_recon_index_v0.md
  - orca-harness/docs/source_capture_agent_runbook.md
  - orca/product/spines/capture/source_families/retail_pdp/retail_pdp_sidecar_operator_playbook_v0.md
  - orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md
  - orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
stale_if:
  - The branch is rebased, merged, or materially updated.
  - The smoke output directory is regenerated with different counts or findings.
  - The stitcher, Cleaning models, ECR derivers, Retail/PDP projection, or Reddit consolidation behavior changes.
```

## Orca Prompt Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_cleaning_capture_ecr_smoke_review
  edit_permission: read-only
  target_scope: >
    Read-only adversarial code/evidence review of the Cleaning Spine continuation
    smoke runner, related tests, and generated scratch evidence under
    orca-harness/_test_runs/cleaning_spine_playbook_capture_20260621/.
  dirty_state_checked: yes
  branch: codex/cleaning-spine-continuation
  expected_head: bc950cdfeeb3a02f33bf52217d71e049aa9093f2
  dirty_state_allowance: >
    Dirty/untracked lane state is expected and is part of the review target.
    Do not require a clean tree. Do not modify files. Do not commit.
  output_mode: review-report
  prompt_artifact_path: docs/prompts/reviews/cleaning_spine_playbook_capture_ecr_cleaning_smoke_adversarial_code_review_prompt_v0.md
  review_output_path: docs/review-outputs/cleaning_spine_playbook_capture_ecr_cleaning_smoke_adversarial_code_review_v0.md
  template_kind: review
  blocked_if_missing:
    - orca-harness/runners/run_capture_ecr_cleaning_smoke.py
    - orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py
    - orca-harness/_test_runs/cleaning_spine_playbook_capture_20260621/capture_ecr_cleaning_smoke_manifest.json
    - orca-harness/_test_runs/cleaning_spine_playbook_capture_20260621/stitched_after_recaptcha_patch/smoke_summary.json
    - orca-harness/_test_runs/cleaning_spine_playbook_capture_20260621/stitched_after_recaptcha_patch/cleaning_packet.json
    - orca-harness/_test_runs/cleaning_spine_playbook_capture_20260621/stitched_after_recaptcha_patch/ecr_source_side_receipts.json
```

## Delegated Review-And-Patch Route Decision

The user requested `workflow-delegated-review-patch` after item 5. This target is a multi-file implementation/code plus generated-evidence review, not a single high-stakes authored artifact with bounded patch authority. Per `.agents/workflow-overlay/delegated-review-patch.md`, do not stretch delegated review-and-patch to fit it. Treat this as a read-only adversarial code/evidence review prompt. If a later Chief Architect commission names a single authored artifact and bounded patch scope, that is a separate route.

## Receiver Instructions

REFERENCE-LOAD these method instructions first. Do not APPLY them until after the task sources are loaded and `SOURCE_CONTEXT_READY` is declared:

- `workflow-deep-thinking`
- `workflow-code-review`

Then SOURCE-LOAD the sources named below. If any required source is missing, return `SOURCE_CONTEXT_INCOMPLETE` with the missing path and do not produce strict findings.

After `SOURCE_CONTEXT_READY`, APPLY deep-thinking to frame failure modes, then APPLY code review. This is a read-only review: do not patch, stage, commit, push, run live capture, or regenerate packet artifacts.

## Review Objective

Review whether the branch now has an honest bounded real-data smoke from playbook-led Source Capture outputs into ECR source-side receipts and `CleaningPacket`, while preserving raw/projection/ECR references and visible capture limitations.

Attack especially:

- whether the stitcher can create false success from bad capture substrate;
- whether raw anchors, packet ids, slice ids, file hashes, projection refs, and ECR refs stay coupled;
- whether the real-data run links raw/projection/ECR/Cleaning enough for inspection;
- whether the generic `captcha` heuristic removal fixes the Sephora false positive without hiding Amazon's real failure;
- whether Reddit consolidation creates Cleaning handles without Judgment vocabulary or invented row anchors;
- whether the branch overclaims live capture-to-cleaning E2E readiness.

## Worktree And Target State

Workspace:
`C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\cleaning-spine-continuation`

Expected branch/head:

```text
branch: codex/cleaning-spine-continuation
HEAD: bc950cdfeeb3a02f33bf52217d71e049aa9093f2
status: dirty and untracked files expected
```

Observed status at prompt authoring:

```text
## codex/cleaning-spine-continuation...origin/main [behind 24]
 M docs/workflows/orca_repo_map_v0.md
 M orca-harness/cleaning/models.py
 M orca-harness/source_capture/retail_pdp_projection.py
 M orca-harness/tests/unit/test_cleaning_core.py
 M orca-harness/tests/unit/test_retail_pdp_projection.py
?? docs/prompts/reviews/cleaning_contract_to_code_obligation_comparison_adversarial_review_prompt_v0.md
?? docs/prompts/reviews/cleaning_spine_capture_ecr_cleaning_smoke_adversarial_code_review_prompt_v0.md
?? docs/prompts/reviews/cleaning_spine_live_e2e_adversarial_code_evidence_review_prompt_v0.md
?? docs/prompts/reviews/cleaning_spine_real_data_smoke_raw_to_cleaned_efficacy_adversarial_review_prompt_v0.md
?? docs/review-outputs/adversarial-artifact-reviews/cleaning_contract_to_code_obligation_comparison_adversarial_review_claude_cross_vendor_v0.md
?? docs/review-outputs/adversarial-artifact-reviews/cleaning_contract_to_code_obligation_comparison_adversarial_review_v0.md
?? docs/review-outputs/adversarial-artifact-reviews/cleaning_spine_real_data_smoke_raw_to_cleaned_efficacy_adversarial_review_v0.md
?? docs/review-outputs/cleaning_spine_capture_ecr_cleaning_smoke_adversarial_code_review_v0.md
?? docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md
?? orca-harness/runners/run_capture_ecr_cleaning_smoke.py
?? orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py
```

## Required Task Sources

Read these code/test files:

- `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`
- `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`
- `orca-harness/cleaning/models.py`
- `orca-harness/cleaning/projection.py`
- `orca-harness/source_capture/retail_pdp_projection.py`
- `orca-harness/tests/unit/test_cleaning_core.py`
- `orca-harness/tests/unit/test_cleaning_projection_integration.py`
- `orca-harness/tests/unit/test_retail_pdp_projection.py`

Read these generated run artifacts:

- `orca-harness/_test_runs/cleaning_spine_playbook_capture_20260621/capture_ecr_cleaning_smoke_manifest.json`
- `orca-harness/_test_runs/cleaning_spine_playbook_capture_20260621/reddit_batch/batch_summary.json`
- `orca-harness/_test_runs/cleaning_spine_playbook_capture_20260621/retail/sephora/retail_pdp_projection.json`
- `orca-harness/_test_runs/cleaning_spine_playbook_capture_20260621/retail/ulta/retail_pdp_projection.json`
- `orca-harness/_test_runs/cleaning_spine_playbook_capture_20260621/retail/amazon/retail_pdp_projection.json`
- `orca-harness/_test_runs/cleaning_spine_playbook_capture_20260621/stitched_after_recaptcha_patch/smoke_summary.json`
- `orca-harness/_test_runs/cleaning_spine_playbook_capture_20260621/stitched_after_recaptcha_patch/cleaning_packet.json`
- `orca-harness/_test_runs/cleaning_spine_playbook_capture_20260621/stitched_after_recaptcha_patch/ecr_source_side_receipts.json`

Read these doctrine/runbook sources for boundaries:

- `orca/product/spines/capture/source_capture_toolbox/source_capture_playbook_v0.md`
- `orca/product/spines/capture/source_capture_toolbox/capture_recon_index_v0.md`
- `orca-harness/docs/source_capture_agent_runbook.md`
- `orca/product/spines/capture/source_families/retail_pdp/retail_pdp_sidecar_operator_playbook_v0.md`
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md`
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
- `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`

## Known Real-Run Evidence To Verify

The dispatcher observed these facts from fresh reads. Treat them as hypotheses until verified:

- Reddit exact old-Reddit batch: 3 successful captures and 3 successful consolidations; comments per slot 3, 2, and 7.
- Retail projections: Sephora 11 rows, `structure_preserved=true`, one residual `sephora_ld_json_review_count_differs_from_target_dom`; Ulta 9 rows, `structure_preserved=true`, no residuals; Amazon 1 row, `structure_preserved=false`, residuals for missing variant offer and review substrate.
- Patched stitch output: 6 ECR receipts, 36 Cleaning handles, 1 transform-ledger smoke entry, all 36 handles carry ECR refs.
- Patched summary findings: Amazon only: `retail_capture_validity_not_supported` and `retail_structure_not_preserved`.
- Focused tests passed after filesystem approval:
  `python -m pytest -p no:cacheprovider --no-header --no-summary -q tests\unit\test_capture_ecr_cleaning_smoke_runner.py tests\unit\test_cleaning_core.py tests\unit\test_cleaning_projection_integration.py tests\unit\test_retail_pdp_projection.py`
  observed output: `.......................................................... [100%]`.

## Review Questions

1. Does `run_capture_ecr_cleaning_smoke.py` refuse or visibly flag the right failures, including packet/projection mismatches, hash mismatches, bad retail substrate, and Reddit row anchor downgrades?
2. Does the `captcha` heuristic patch correctly avoid treating hidden reCAPTCHA libraries on valid PDPs as block pages while still catching Amazon's Page Not Found / tiny bad substrate result?
3. Do Cleaning handles preserve `packet_id`, `slice_id`, `file_id`, `relative_packet_path`, `sha256`, `hash_basis`, projection refs for retail rows, and ECR ref packet-key coupling?
4. Are ECR source-side receipts derived for every packet and correctly scoped as source-side postures, without becoming Judgment or sufficiency claims?
5. Does the stitched `CleaningPacket` remain a Cleaning working view, not raw evidence, ECR schema ratification, Judgment scoring, or production E2E proof?
6. Does the run honestly report that Amazon did not yield usable PDP substrate, instead of smoothing it into success because a packet exists?
7. Are any tests missing that would allow this exact class of false-positive/false-success to regress?
8. Are any claims in this prompt or the run artifacts too strong relative to the loaded boundaries?

## Output Contract

Write the review report to:
`docs/review-outputs/cleaning_spine_playbook_capture_ecr_cleaning_smoke_adversarial_code_review_v0.md`

Findings first, ordered by severity. Use this shape:

```yaml
review_summary:
  reviewed_by: <operator/tooling supplied model+version, or unrecorded>
  authored_by: gpt-5-codex
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded
  same_vendor_rationale: <required if same_vendor_sanity>
  source_context: SOURCE_CONTEXT_READY | SOURCE_CONTEXT_INCOMPLETE
  verdict: no_blockers_found | findings_found | blocked
  validation_observed:
    - <commands or not_run_with_reason>
  strict_non_claims:
    - not validation
    - not readiness
    - not production e2e
    - not Judgment scoring
```

Each finding must include:

- severity: blocker | major | minor
- file/path and line when applicable
- evidence from code or generated artifacts
- impact
- minimum_closure_condition
- next_authorized_action

Do not emit a patch queue. Advisory remediation direction is allowed; executor-ready patch instructions are not.

## Review-Use Boundary

Review findings are decision input only. They are not approval, validation, mandatory remediation, readiness, merge authority, fixture admission, production acceptance, or proof-run readiness until separately accepted and authorized.
