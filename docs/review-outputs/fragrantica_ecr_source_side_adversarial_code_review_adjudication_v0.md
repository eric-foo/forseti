# Fragrantica ECR Source-Side Adversarial Code Review Adjudication v0

```yaml
retrieval_header_version: 1
artifact_role: home-model adjudication record for advisory implementation/code review
scope: >
  Records home-model adjudication of the cross-vendor Fragrantica source-side ECR
  advisory code review before assumption-gate, Cleaning, or fused implementation work.
use_when:
  - Deciding what remains before the Fragrantica ECR lane can proceed to assumption-gate or Cleaning.
  - Checking which review findings were accepted, modified, deferred, or treated as non-gating residuals.
authority_boundary: retrieval_only
review_report: docs/review-outputs/fragrantica_ecr_source_side_adversarial_code_review_v0.md
review_report_sha256: 0F75689DF3108C34BAFCE4776980021FEC3674E4DE2176E49BA540F955F56F8C
commission_prompt: docs/prompts/reviews/fragrantica_ecr_source_side_adversarial_code_review_prompt_v0.md
target_branch: codex/fragrantica-ecr-review-prompt
adjudicated_at_head: a3879a1a15f53ed77c92b31a1b2149e8dead6a94
```

## Adjudication Summary

Decision: `accept_with_gates`.

The cross-vendor review report is accepted as a durable advisory review output.
Its bottom line is also accepted with a tighter lane consequence:

- No blocker was found in the current six Fragrantica single-slice ECR record sets.
- The generic source-side ECR sibling structure is the right shape for Fragrantica capture packets.
- Projection content does not feed ECR; ECR derives from raw packet facts only.
- Residuals for timing and source visibility are honest and non-clearing.
- This does **not** mean the lane is ready for assumption-gate, Cleaning, or fused implementation.

The review found two major latent gaps. They are real enough to block the next
strict gate unless the owner explicitly accepts the residuals. The smallest
complete next implementation closure is:

1. Add a fail-closed SP-6 guard for multi-slice or divergent source-visibility
   cases, or record explicit owner ratification of the flat packet-level SP-6 shape.
2. Add a lake-level Fragrantica-shaped packet test through `derive_ecr_into_lake`.
3. Record a downstream selection/supersession convention before any Cleaning or
   Judgment consumer binds projection/ECR record sets.

## Finding Decisions

| Finding | Decision | Lane consequence |
| --- | --- | --- |
| F-01 SP-6 packet-flat source-visibility has no runtime guard | Accepted as major latent | Blocks assumption-gate/fused work unless closed by fail-closed guard, per-slice rollup, or explicit owner ratification. No current six-packet defect because all reviewed Fragrantica packets are single-slice. |
| F-02 no Fragrantica-shaped ECR regression test | Accepted as major durability gap | Blocks assumption-gate/fused work. Add a lake-level test using Fragrantica-shaped packet fields and asserting the expected ECR posture profile plus four-sibling marker integrity. |
| F-03 persisted ECR records vs older "non-persisted" wording | Accepted with modification | Not a runtime defect and not a gate. The current data-lake mechanics map authorizes derived records; the cleanup is traceability wording/citation at the ECR lake boundary. |
| F-04 append-only multiple record sets lack a downstream selection policy | Accepted as downstream gate | Does not invalidate current ECR records. Must be resolved before Cleaning/Judgment consumers bind a projection/ECR set as current or authoritative. |
| F-05 archive-slice detection depends on free-string `slice_id` convention | Accepted as deferred archive-lane residual | Not a Fragrantica gate because current packets are non-archive current captures. Route to archive-capable producer onboarding. |

## Source Checks Performed

This adjudication did not inherit the pasted review blindly. Load-bearing claims
were checked against primary repo sources:

- `orca-harness/ecr/models.py:270-349` confirms `RESIDUAL_SLICE_DIVERGENT_VISIBILITY`
  exists but is not emitted by the flat `EcrSourceVisibilityPosture` shape.
- `orca-harness/ecr/deriver.py:249-366` confirms `derive_source_visibility_postures`
  returns one packet-level posture and has no divergent-slice guard.
- `orca-harness/ecr/lake.py:54-89` confirms `derive_ecr_into_lake` loads the raw
  packet by key, model-validates it, derives the four ECR posture kinds, and appends
  them as sibling records plus `ecr_set`.
- `ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md`
  confirms the SP-6 plan recommends per-slice value/residual plus Ob.10 no-hide
  rollup and flags packet-flat shape as a major inconsistency if unguarded.
- `docs/workflows/ecr_spine_submap_v0.md:44-48` and
  `core_spine_v0_data_lake_mechanics_map_v0.md:63-123` confirm the current
  data-lake/ECR lane allows derived integrity records while preserving raw capture
  as canonical and re-derivable.
- `rg` over the ECR tests confirmed no `fragrance_native_database` or
  `fragrantica_product_page_direct_http` ECR fixture path exists today.

## Validation Evidence

- Fresh read verified the review report exists at
  `docs/review-outputs/fragrantica_ecr_source_side_adversarial_code_review_v0.md`.
- SHA256 of that report was observed as
  `0F75689DF3108C34BAFCE4776980021FEC3674E4DE2176E49BA540F955F56F8C`.
- Focused ECR suite rerun in this worktree exited 0 and emitted 49 pytest progress dots:
  `test_ecr_lake_pilot.py`, `test_ecr_identity_deriver.py`,
  `test_ecr_inspectability_deriver.py`, `test_ecr_timing_deriver.py`,
  `test_ecr_source_visibility_deriver.py`.
- Focused Fragrantica suite rerun in this worktree exited 0 and emitted 10 pytest
  progress dots: `test_fragrantica_projection.py`,
  `test_fragrantica_cleaning_projection_integration.py`,
  `test_fragrantica_projection_lake_pilot.py`.

## Residuals

- The current Fragrantica ECR materialization remains review-supported for the six
  single-slice packets, but it is not assumption-gate clearance.
- F-01 should be closed before multi-source packets or any stricter ECR gate.
- F-02 should be closed before treating Fragrantica ECR as regression-guarded.
- F-04 should be closed before any downstream consumer chooses among multiple
  projection/ECR generations.
- This adjudication does not patch code, rerun live capture, replay projection,
  replay ECR, start Cleaning, bind EvidenceUnit, or authorize Judgment.

## Operator Closeout Source

```yaml
fragrantica_ecr_source_side_review_adjudication:
  status: accept_with_gates
  report_kept: docs/review-outputs/fragrantica_ecr_source_side_adversarial_code_review_v0.md
  accepted_findings: [F-01, F-02, F-04, F-05]
  modified_findings:
    F-03: "accepted as traceability cleanup only; current data-lake map reconciles derived ECR record persistence"
  gate_decision:
    assumption_gate: blocked_until_F01_F02_closed_or_owner_accepts_residuals
    cleaning: blocked_until_record_set_selection_policy_exists
    fused: blocked_until_current_gates_are_closed_or_owner_explicitly_redirects
  recommended_next_patch:
    - add SP-6 multi-slice/divergent-visibility fail-closed guard or owner-ratify flat shape
    - add Fragrantica-shaped derive_ecr_into_lake regression test
    - record downstream record-set selection/supersession convention before consumer binding
  validation:
    review_report_hash_verified: true
    ecr_focused_suite_passed: true
    ecr_focused_progress_dots_observed: 49
    fragrantica_focused_suite_passed: true
    fragrantica_focused_progress_dots_observed: 10
  non_claims:
    - not approval
    - not validation
    - not readiness
    - not assumption-gate clearance
    - not patch authority
    - not live capture execution
    - not Cleaning design
    - not Judgment or buyer proof
```
