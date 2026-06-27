# IG Back-Fix And Shared Capture Contract Review Adjudication v0

```yaml
retrieval_header_version: 1
artifact_role: home-model adjudication record for adversarial artifact review
scope: >
  Records which findings from the IG back-fix and shared capture contract
  adversarial review were accepted and how the planning specs were amended after
  review. This is not a second review of the patched specs.
use_when:
  - Checking how the IG back-fix and shared contract extraction review was closed.
  - Distinguishing the reviewed pre-patch targets from the post-review patched targets.
  - Preparing a future IG back-fix or shared contract extraction scoping pass.
authority_boundary: retrieval_only
review_report: docs/review-outputs/adversarial-artifact-reviews/ig_backfix_shared_capture_contract_adversarial_artifact_review_v0.md
review_report_sha256: 53C9E76F7049018B5CAB693B929928D93FD419292AEEBFC16E5B9516571AD3F1
reviewed_targets:
  docs/workflows/ig_backfix_against_youtube_behavioral_contract_spec_v0.md: FD44B9A9AE00DF9D3F31E2B77F196B05184A4B4F9B04BD8D877616EFEA049E1A
  docs/workflows/shared_capture_behavioral_contract_extraction_spec_v0.md: 13A45F12EF75C1C4E9F55BDEEAD875E4E4B55FF1AB5B627C4AB1BC8EFC1C47B5
patched_targets:
  docs/workflows/ig_backfix_against_youtube_behavioral_contract_spec_v0.md: 2AAB641FFDF4B40DC06DB2B795301E1BBABC76F0CD85EDF77985FD1FB61C5971
  docs/workflows/shared_capture_behavioral_contract_extraction_spec_v0.md: E53DFA226B7981C2AB4257B47CD646038BB68F6F7BBE1DB50783C825C4470A35
review_not_rerun_after_patch: true
```

## Adjudication Summary

Decision: `accept_all_with_author_patch`.

The review's one major finding and two minor findings were accepted. Optional
hardening `OH-01` was also applied because it was a cheap residual-hygiene
improvement. The patch keeps the work planning-only: no source edits, no runtime
capture, no persistence migration, no implementation authorization, no shared
scheduler/framework, and no production-readiness claim.

## Finding Decisions

| Finding | Decision | Kept Action |
| --- | --- | --- |
| AR-01 per-item extraction status under-defined | Accepted | Define extraction completion as per transcript-source anchor; require `source_extraction_statuses`; require a per-item rollup that cannot read complete while an extraction-eligible source is unextracted, failed, or partial unless explicitly residualized or marked non-eligible; require canonical-only completion to use `canonical_extraction_status`. |
| AR-02 `TranscriptSource` name collision | Accepted | Rename the shared rich behavior-layer contract to `TranscriptSourceRecord`; state that it is distinct from the existing `schemas.product_mention_models.TranscriptSource` enum for `asr | caption`; update IG references to the rich contract name. |
| AR-03 patched YouTube dependency not re-reviewed | Accepted | Add explicit MGT residuals in both specs naming the unre-reviewed patched YouTube dependency and requiring post-patch YouTube re-review or explicit owner acceptance before source-changing IG/shared implementation uses it as authority. |
| OH-01 residual triggers | Accepted optional hardening | Add upgrade triggers for separate IG runners and contract-plus-adapter projection residuals; also make the deep-capture transcript extraction residual's upgrade condition explicit. |

## Validation Evidence

- Fresh worktree status before adjudication showed only the review report
  untracked.
- The review report was read from the worktree and its SHA256 matched
  `53C9E76F7049018B5CAB693B929928D93FD419292AEEBFC16E5B9516571AD3F1`.
- Fresh reads of source/control lines verified the existing
  `schemas.product_mention_models.TranscriptSource` enum, the unre-reviewed
  patched YouTube adjudication dependency, and the review report's target hashes.
- Fresh reads of the patched specs verified the amended extraction-status grain,
  `TranscriptSourceRecord` naming, and MGT residuals.
- No implementation, runtime refactor, executable test, network capture, or
  source migration was run; this is a documentation/planning adjudication only.
- The patched IG/shared specs have not been adversarially re-reviewed after this
  patch.

## Residuals

- A future implementation scoping pass must still choose the concrete bridge,
  adapter, index, or test fixture shape for deterministic extraction-status
  resolution.
- The original step-3/4 review prompt and report target the pre-patch hashes.
  They are historical review evidence, not a claim that the patched specs have
  already been re-reviewed.
- The patched YouTube behavioral spec remains unre-reviewed after its own
  adjudication patch; the IG/shared specs now name that dependency explicitly.

## Operator Closeout Source

```yaml
ig_backfix_shared_capture_contract_review_adjudication:
  status: accepted_all_with_author_patch
  report_kept: docs/review-outputs/adversarial-artifact-reviews/ig_backfix_shared_capture_contract_adversarial_artifact_review_v0.md
  targets_patched:
    - docs/workflows/ig_backfix_against_youtube_behavioral_contract_spec_v0.md
    - docs/workflows/shared_capture_behavioral_contract_extraction_spec_v0.md
    - docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md
  accepted_findings: [AR-01, AR-02, AR-03]
  accepted_optional_hardening: [OH-01]
  validation:
    report_hash_verified: true
    patched_specs_fresh_read: true
    implementation_tests_run: not_applicable_docs_only
    post_patch_adversarial_re_review: not_run
  non_claims:
    - not implementation authorization
    - not runtime validation
    - not production readiness
    - not shared acquisition machinery approval
    - not TikTok coverage
```