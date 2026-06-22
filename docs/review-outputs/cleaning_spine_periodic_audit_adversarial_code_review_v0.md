# Cleaning Spine Periodic Audit Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (implementation/code review, advisory)
scope: >
  Same-vendor advisory implementation/code review of the Cleaning spine periodic audit.
use_when:
  - Checking advisory findings from the periodic-audit review pass.
  - Reconstructing review scope, source basis, and accepted residuals.
authority_boundary: retrieval_only
```

reviewed_by: openai/gpt-5-codex
authored_by: gpt-family-codex
de_correlation_bar: same_vendor_sanity
same_vendor_rationale: >
  The operator explicitly constrained this execution to same-vendor fallback.
  This is a bounded sanity review of a local multi-file implementation patch,
  not cross-vendor discovery and not a no-new-seam claim.

## Findings

### F-01 - MAJOR - Projection breakpoint comparison is too shallow to catch source-visible row corruption

- Target file: `orca-harness/runners/run_cleaning_spine_periodic_audit.py`
- Stable anchor: `_projection_signature()` at lines 893-905 and `_reddit_consolidation_signature()` at lines 908-925.
- Evidence: Retail/IG projection rebuilds compare only packet id, method/version/certification, row count, row-kind counts, `structure_preserved`, and packet residuals. Reddit consolidation compares packet/raw-file metadata, `thread`, comment count, counts, warnings, and limitations, but not the comment rows themselves.
- Authority or evidence basis: Projection Doctrine requires projected rows to preserve source-visible facts, bindings, raw anchors, and source structure without becoming Judgment. Cleaning does not carry most source-visible row values, so Lane B Cleaning cannot compensate for a shallow projection signature.
- Concrete impact: The audit can report `pass` even if a frozen Retail/PDP projection has a corrupted price, review count, SKU binding, source-visible field, or raw anchor field that does not change row count/residuals. A Reddit consolidation can similarly lose or alter comment body/author/timestamp fields without changing the current signature. That is a false-confidence risk exactly at the projection breakpoint the periodic audit is meant to cover.
- Minimum closure condition: Projection/consolidation signatures include all source-visible row payloads and binding/provenance fields that Cleaning may rely on or that Projection Doctrine requires, with only intentionally volatile fields excluded.
- Next authorized action: Home model should patch the signature shape and add at least one failing fixture mutation for `source_visible_fields` or Reddit comment payload drift.
- Validation expectation: Same no-network pytest suite should fail before the patch on the new projection-payload drift test and pass after the signature is widened.
- patch_queue_entry authorized: no.

### F-02 - MAJOR - Existing smoke findings are counted but do not affect audit status

- Target file: `orca-harness/runners/run_cleaning_spine_periodic_audit.py`
- Stable anchor: Lane A summary handling at lines 314-322; overall status derives only from audit `findings` at lines 156-168.
- Evidence: `_run_lane_a_existing_package_checks()` reads `smoke_summary.json` and stores only `smoke_summary_finding_count`. It never promotes or mirrors those existing smoke findings into audit findings. The smoke stitcher emits capture-validity findings such as `retail_capture_validity_not_supported` in `run_capture_ecr_cleaning_smoke.py` lines 275-281.
- Authority or evidence basis: AGENTS.md requires preserving real failure visibility. The audit goal includes capture preflight plus projection and Cleaning breakpoint detection. Capture-validity failures are not packet hash failures, so capture preflight alone does not surface them.
- Concrete impact: A periodic audit over a Lane A package with a blocked/error retail capture can still compute `overall_status: pass` if packet hashes, ECR refs, and Cleaning handles validate. The only visible signal would be a non-status-affecting count buried in `lane_a_existing_package`, which is weak for a future periodic monitor.
- Minimum closure condition: Non-empty Lane A smoke findings are surfaced as audit findings, at least warning-level, with source labels/codes preserved; capture-validity or anchor-validity findings should prevent a clean `pass` unless explicitly allowlisted as expected residuals.
- Next authorized action: Home model should patch Lane A summary ingestion and add a no-network periodic-audit test using the existing retail error-page fixture path.
- Validation expectation: A fixture with `retail_capture_validity_not_supported` should produce audit `overall_status: warn` or `fail`, not `pass`, with the original smoke finding code visible in the audit report.
- patch_queue_entry authorized: no.

### F-03 - MINOR - Output collision guard checks report files but not rebuild subdirectories

- Target file: `orca-harness/runners/run_cleaning_spine_periodic_audit.py`
- Stable anchor: output guard at lines 105-116; Lane B output subdirectories at lines 142-150.
- Evidence: The runner checks only `cleaning_spine_periodic_audit_report.json` and `.md` before running. It then writes projection rebuilds under `lane_b_projection_rebuild` and Cleaning rebuilds under `lane_b_cleaning_rebuild`. If a prior partial run left those subdirectories behind without report files, the next run can mix overwrite behavior and collision behavior from downstream writers.
- Authority or evidence basis: The prompt asks whether output overwrite guards and scheduler-facing semantics are coherent. A future scheduler needs deterministic rerun behavior.
- Concrete impact: A partial output directory can produce confusing audit failures or stale outputs that look like implementation breakage rather than an output-collision condition.
- Minimum closure condition: The runner either requires an absent/empty output directory, preflights all generated subpaths, or writes all rebuild artifacts under a unique run directory.
- Next authorized action: Home model may patch the output guard or document the caller obligation to supply a fresh output directory.
- Validation expectation: Add a no-network unit test for partial stale `lane_b_projection_rebuild` / `lane_b_cleaning_rebuild` contents.
- patch_queue_entry authorized: no.

## Source Context

SOURCE_CONTEXT_READY with qualification.

Qualification: the prompt-named `docs/hygiene/cleaning_spine_lane_handoff_v0.md` is absent in the target worktree and absent from `git ls-files`. Local prior artifacts also identify it as absent/orientation-only. The review proceeded as advisory implementation/code review because the controlling Cleaning/projection contracts and target patch files were present.

Strict review claims remain NOT_CLAIMED.

## Source-Read Ledger

- `AGENTS.md` - project behavior, source authority, safety, validation/lifecycle boundaries.
- `.agents/workflow-overlay/README.md` - Orca overlay entrypoint and binding rule.
- `.agents/workflow-overlay/source-loading.md` - source-read and strict-claim discipline.
- `.agents/workflow-overlay/prompt-orchestration.md` - output mode and source-gated method contract.
- `.agents/workflow-overlay/review-lanes.md` - read-only review, advisory findings, same-vendor sanity bar.
- `.agents/workflow-overlay/delegated-review-patch.md` - multi-file code diff route-out and de-correlation boundary.
- `.agents/workflow-overlay/validation-gates.md` - failure visibility and missing-evidence semantics.
- `.agents/workflow-overlay/safety-rules.md` - no live capture/network/source edits and no forbidden drift.
- `docs/prompts/reviews/cleaning_spine_periodic_audit_adversarial_code_review_prompt_v0.md` - commission, target files, output path, and strict boundaries.
- `docs/hygiene/cleaning_spine_lane_handoff_v0.md` - missing; absence verified by direct read failure, `rg --files`, and `git ls-files`.
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md` - Cleaning purpose and source-family adaptation boundary.
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md` - non-destructive ledger, raw-pull, no-Judgment, exact-identity core direction.
- `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` - Data Capture / ECR / Cleaning / Judgment split.
- `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md` - projection view contract and no-salience/no-Judgment boundary.
- `orca-harness/runners/run_cleaning_spine_periodic_audit.py` - reviewed target runner.
- `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py` - reviewed target tests and fixture coverage.
- `docs/workflows/orca_repo_map_v0.md` - targeted added runner route at line 485.
- `orca-harness/runners/run_capture_ecr_cleaning_smoke.py` - adjacent stitcher used by Lane B Cleaning and smoke-summary finding source.
- `orca-harness/cleaning/models.py` - CleaningPacket validation and Judgment-token guards.
- `orca-harness/ecr/deriver.py` - source-side posture derivation behavior.
- `orca-harness/source_capture/models.py` - SourceCapturePacket preserved-file and hash-basis contract.
- `orca-harness/source_capture/ig_projection.py` - IG projection rebuild/row shape.
- `orca-harness/source_capture/retail_pdp_projection.py` - Retail/PDP projection rebuild/row/binding shape.
- `orca-harness/source_capture/reddit_consolidation/consolidator.py` - Reddit consolidation rebuild/row shape.

## Open Questions And Residual Risk

- Same-vendor sanity is structurally weaker than cross-vendor discovery; no no-new-seam claim is available.
- Validation was not independently rerun in this review. The author-supplied pytest evidence is recorded below.
- The audit still intentionally excludes scheduler creation, live capture, network access, storage, dashboard, product proof, Judgment readiness, and live E2E readiness.
- The missing handoff file means thread-intent history was not available as a primary source; current prompt and in-repo contracts carried the review instead.

## Validation Rerun Status

Validation was not independently rerun. Status: author-supplied / not independently revalidated.

Author-supplied command:

```powershell
python -B -m pytest -p no:cacheprovider --no-header --no-summary -q tests\unit\test_capture_ecr_cleaning_smoke_runner.py tests\unit\test_cleaning_core.py tests\unit\test_cleaning_projection_integration.py tests\unit\test_source_capture_ig_projection.py tests\unit\test_retail_pdp_projection.py tests\unit\test_reddit_consolidation.py
```

Author-supplied observed output:

```text
........................................................................ [ 84%]
.............                                                            [100%]
```

## Strict-Only Blockers And Non-Claims

- Formal Orca implementation-review verdict: NOT_CLAIMED.
- Cross-vendor discovery / no-new-seam standard: NOT_CLAIMED.
- Validation pass/readiness/approval/acceptance: NOT_CLAIMED.
- Patch queue or executor-ready remediation: NOT_AUTHORIZED.
- Source edits, commit, push, PR, live capture, or network work: NOT_PERFORMED.
- Cleaning E2E readiness, live capture-to-cleaning readiness, product proof, Judgment readiness: NOT_CLAIMED.

DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

Include:
- original commission or review target: `docs/prompts/reviews/cleaning_spine_periodic_audit_adversarial_code_review_prompt_v0.md`; target files were `orca-harness/runners/run_cleaning_spine_periodic_audit.py`, `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`, and the periodic-audit route edit in `docs/workflows/orca_repo_map_v0.md`.
- implementation context, diff, and reviewed files: same-vendor read-only implementation/code review of the no-network periodic Cleaning audit runner patch.
- findings and implementation evidence: F-01 major shallow projection/consolidation signatures; F-02 major Lane A smoke findings counted but not status-affecting; F-03 minor partial-output collision hygiene.
- proposed patch, diff, or exact requested edits, if authorized: no patch queue authorized; advisory closure conditions are listed per finding.
- citations: line anchors in the findings above.
- reviewer verdict: advisory findings found; strict formal verdict NOT_CLAIMED.
- validation evidence and not-run checks: validation not independently rerun; author-supplied no-network pytest output recorded.
- residual risk: same-vendor sanity only, missing handoff source, no scheduler/live-capture/E2E readiness claim.
- blockers, off-scope flags, and not-proven boundaries: no source edits/commit/push/PR/live capture/network; no cross-vendor discovery, validation, readiness, or approval claim.
