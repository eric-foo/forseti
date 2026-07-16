# ECR Consolidation v0 SP-1/SP-2/SP-3 Source-Side Reconcile Cross-Family Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Cross-family source-side reconciliation review of ECR Consolidation SP-1 through SP-3.
use_when:
  - Inspecting source-side reconciliation findings or residual friction.
  - Tracing SP-1 through SP-3 consolidation decisions to this review.
authority_boundary: retrieval_only
reviewed_by: unrecorded
authored_by: unrecorded
review_use_boundary: Findings are decision input, not approval, validation, mandatory remediation, or patch authority.
```

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/ecr_consolidation_v0_sp1_sp2_sp3_source_side_reconcile_cross_family_review_v0.md
  recommendation: accept_with_friction
  summary: "Producer citations and M1/M2/M3 bindings hold after one bounded frame-fidelity wording patch; residual friction is dirty-state mismatch and owner-reserved ratification."
  findings_count: 1
  blocking_findings: []
  advisory_findings:
    - AR-01: "Patched SP-6 seed wording to avoid implying a ratified standing ECR field or already-bindable schema."
  prior_findings_remediated: []
  next_action: "Chief Architect adjudicates the target diff; no ratification, JSG-01 unfreeze, or readiness claim follows from this review."
```

## Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: patch-only on docs/product/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md; report-write under docs/review-outputs/adversarial-artifact-reviews
  target_scope:
    - docs/product/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md
  dirty_state_checked: yes
  blocked_if_missing: yes
```

```text
decision_routing:
  regime: complicated
  why: Cross-family delegated review-and-patch with source hierarchy, dirty worktree, hash pins, and owner-reserved boundaries.
  decomposition: authority/readiness preflight -> source-load -> adversarial review -> bounded target patch -> durable report.
  current_bottleneck: Confirming whether apparent schema-completion wording was a patch-level frame-fidelity defect or an owner-reserved architecture issue.
  riskiest_assumption: That SP-6 "ratified seed" can be referenced without implying a ratified standing ECR field or JSG-01-clearable schema.
  stop_or_pivot_condition: Design-level conflict with the ratified frame or boundary source would require NEEDS_ARCHITECTURE_PASS and no patch.
  allowed_next_move: Patch only target wording that overclaims the SP-6 seed / schema boundary, then report.
  disallowed_next_move: Edit producer, frame, boundary, translator, overlay, or owner-reserved decisions.
```

Preflight receipt: `author_family=Opus-class`; `delegate_family=GPT-family/non-Opus`; `de_correlation=satisfied`.

Target hash before patch was confirmed by fresh read as `0151FD5A5DE019B2005B5AC6C1BE563512721BA9A751CEF0BC189DC1437A0E23`. The required frame and translator hashes also matched the commission: frame `50DDE207824BCB7CE38DBDDF00C23014CA73E170BB4B62907C209C622174816F`; translator `E8944D13FF8B3FAF62AC24209EC50FDA7C03CC9D4F906687246B2E15C01592B2`.

Dirty-state note: the commission's dirty-state description was stale. The actual worktree was heavily dirty/untracked, and the target plus translator were untracked. This did not block the bounded review because the commission hash-pinned the untracked target/translator and required producer verification from `HEAD`; no unrelated dirty source was used as producer authority.

SOURCE_CONTEXT_READY. Method instructions were reference-loaded before source application; `workflow-deep-thinking` and `workflow-adversarial-artifact-review` were applied only after the authority and source pack were loaded.

## Source-Read Ledger

| Source | Why read | Evidence used | State |
| --- | --- | --- | --- |
| `AGENTS.md` | Orca behavior, smallest complete intervention, overlay trigger | Project work requires overlay and durable verification | tracked |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint | Overlay is Orca authority | tracked |
| `.agents/workflow-overlay/decision-routing.md` | Required router for delegated review/patch | Router output above | tracked |
| `.agents/workflow-overlay/review-lanes.md` | Review and delegated review boundary | Review reports under `docs/review-outputs/`; delegated convention is provisional | tracked |
| `.agents/workflow-overlay/prompt-orchestration.md` | Source-gated method and review-report output mode | REFERENCE-LOAD/SOURCE-LOAD/SOURCE_CONTEXT_READY sequence; durable report before chat summary | tracked |
| `.agents/workflow-overlay/safety-rules.md` | Protected path and no-commit boundary | No commit/push; no edits outside bound scope | tracked |
| `.agents/workflow-overlay/delegated-review-patch.md` | Commissioned patch convention | Patch only named target; CA adjudicates diff | tracked |
| `docs/product/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md` | Target | Lines 33, 35, 79 patched | untracked, hash-pinned |
| `git show HEAD:orca-harness/source_capture/models.py` | Producer at current HEAD | `CUTOFF_POSTURE_VALUES` line 53; `PacketTiming.cutoff_posture` line 87; validator lines 90-94; `HASH_BASIS_VALUES` line 66; `PreservedFile.sha256/hash_basis` lines 101-102; validator lines 105-114; identity inputs lines 164-169 | HEAD tracked |
| `docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md` | Ratified ECR frame and SP-6 seed source | Frame lines 50-56, INV/D3/D4 lines 99-113, SP-6 separation lines 194-207, non-claims lines 300-306 | tracked, hash matched |
| `docs/product/jsg01_source_side_receipt_translator_v0.md` | Reconciled-from SP-1/SP-2/SP-3 definitions | SP-1 lines 111-133, SP-2 lines 135-160, SP-3 lines 162-180, drift/collision lines 437-453 | untracked, hash-pinned |
| `docs/product/judgment_quality_promotion_operating_model_v0.md` | JSG-01 predicate need | Predicate-binding rule lines 173-183; JSG-01 missing fields line 205 | tracked |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Ob.7/Ob.9/Ob.16 basis | Ob.7 lines 228-237; Ob.9 lines 262-274; categorical handoff lines 466-476 | tracked |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Inclusion State Rule and ratified seed boundary | Inclusion state lines 158-167; SP-6 seed/deferral lines 283-285 | tracked |

## Findings

### AR-01

Severity: minor

Seam: Frame fidelity / SP-6 seed boundary / no premature ratification.

Citations:

- Target before patch: `docs/product/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md:33,35,79`.
- Boundary source: `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md:283-285` says the ratified seed is the ECR frame plus SP-6 derivation contract, while standing `source_visibility_posture`, final ECR/Evidence Unit field architecture, SP-6 sufficiency grade, SP-5 finalization, and JSG-01 unfreeze remain deferred.
- Frame source: `docs/product/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md:50-56` describes advisory frame/SP-6 design; lines 300-306 keep ratification, JSG-01 unfreeze, full ECR field architecture, SP-6 grade, and SP-5 finalization as non-claims.
- Conductor: `docs/product/judgment_quality_promotion_operating_model_v0.md:173-183,205` requires exact owner field/schema before JSG-01 source-side subpredicates can clear.

Defect: The target's "four-field source-side ratification (with SP-6)" and "these three complete the source-side schema the gate binds to" wording could be read as if SP-6 already stands as a ratified ECR field and the three fields complete an already-bindable JSG-01 schema. That is too strong against the boundary source: SP-6 is a ratified frame/derivation-contract seed, not a standing ECR field, and JSG-01 remains frozen until owner ratification names the missing field schema.

Minimum closure condition: The target must refer to the SP-6 seed as frame/derivation-contract only, present SP-1/SP-2/SP-3 as ratification candidates, and preserve that JSG-01 can bind them only after owner ratification.

Next authorized action: Patched in target under delegated review-and-patch authority.

Patched: yes.

## Patches Applied

Patch for AR-01, grounded by `core_spine_v0_data_and_cleaning_spine_boundary_v0.md:283-285`, `ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md:50-56,300-306`, and `judgment_quality_promotion_operating_model_v0.md:173-183,205`.

```diff
@@
-- **Status:** advisory design; **non-executing**. Recommends three fields for the owner's four-field source-side ratification (with SP-6). Designs no derivers; the field *implementation* (computing each value from a packet) is post-ratification.
+- **Status:** advisory design; **non-executing**. Recommends three fields for the owner's source-side ratification consideration alongside the already-ratified SP-6 frame/derivation-contract seed. Designs no derivers; the field *implementation* (computing each value from a packet) is post-ratification.
@@
-- **Why these three:** the conductor's JSG-01 predicate returns `indeterminate_until_authored` for the source-identity, inspectability, and timing/cutoff subpredicates because no ECR field schema names them. SP-6 (source-visibility) is ratified as a seed; these three complete the source-side schema the gate binds to.
+- **Why these three:** the conductor's JSG-01 predicate returns `indeterminate_until_authored` for the source-identity, inspectability, and timing/cutoff subpredicates because no ECR field schema names them. SP-6 (source-visibility) is ratified only as the frame/derivation-contract seed; these three would complete the proposed source-side schema candidate the gate could bind to only after owner ratification.
@@
-- Covers **only** SP-1/SP-2/SP-3. SP-4 (the `pre_decision_status` **value** check) is packing/case-level; the **two owner residuals** — SP-5 finalization authority and the SP-6 visibility-sufficiency grade — are owner decisions recorded at ratification, not designed here.
+- Covers **only** SP-1/SP-2/SP-3. SP-4 (the `pre_decision_status` **value** check) is packing/case-level; the **two owner residuals** — SP-5 finalization authority and the SP-6 visibility-sufficiency grade — are owner decisions recorded at ratification, not designed here. The SP-6 standing-field declaration also remains deferred by the ratified seed boundary; this plan does not reopen it.
```

Fresh read after patch shows the patched lines at target lines 33, 35, and 79. Updated target SHA256 from fresh read: `12799649B1FC9B3B4CE9CF667AF61F966A4B7609D72E42BD1037DA5E778AFAB4`.

## Not Patched

No owner-reserved design decision was patched. SP-5 finalization authority, SP-6 visibility-sufficiency grade, SP-6 standing-field declaration, ratification, and JSG-01 unfreeze remain owner-reserved. Minimum closure condition for those items is an explicit owner ratification/decision artifact; this review has no authority to supply it.

Dirty-state mismatch was not patched because it is commission/runtime preflight context, not a target artifact defect. It is recorded here as friction.

## Non-Findings

- SP-3 M1 carry-not-coin holds. At `HEAD`, the producer owns `PacketTiming.cutoff_posture` (`models.py:87`), closes allowed values at `models.py:53`, and validates them at `models.py:90-94`. The target's SP-3 re-seat to carried producer value plus ECR clear-condition is frame-consistent.
- SP-1 M2 plus AR-02 holds. `SourceCapturePacket` carries `source_family`, `source_surface`, `source_locator`, and `actor_audience_context` at `models.py:164-169`; Ob.7 requires actor/audience preservation where knowable and marking unavailability at obligation-contract lines 228-237. The target does not require a hard downstream actor field.
- SP-2 M2 over an M1-carried integrity anchor holds. `PreservedFile.sha256` and `hash_basis` are at `models.py:101-102`; `HASH_BASIS_VALUES` is closed at line 66; validator lines 105-114 enforce the basis. The target correctly treats a hash with no recorded coverage basis as insufficient.
- INV-1 through INV-5, D3, and D4 hold after the patch. The target keeps all three fields derived/carried, non-persisted, source-side producer-owned, and non-coined.
- Fences hold after the patch. The target remains advisory, non-executing, not validation, not readiness, not ratification, and not JSG-01 unfreeze.

## Not-Proven Boundaries

- This review did not run tests. Test status is not claimed.
- This review did not validate the ECR design, ratify the fields, unfreeze JSG-01, accept any field into a standing schema, or prove readiness.
- This review did not inspect every unrelated dirty/untracked file in the worktree. It verified the producer from `HEAD` and used hash-pinned target/translator/frame sources for the commissioned scope.
- The target remains untracked; the report is a new untracked review artifact. No commit or push was performed.

## Closeout

Recommendation: `accept_with_friction` as decision input after the bounded patch. The friction is not a source-side schema defect after patch; it is the dirty-state mismatch and the fact that owner-reserved ratification still has to adjudicate whether the proposed SP-1/SP-2/SP-3 fields are kept.

Review-use boundary: findings and patches are decision input for the Opus home/Chief Architect model. They are not approval, validation, readiness, mandatory remediation, ratification, formal review authority, or JSG-01 unfreeze.
