# Delegated Adversarial Artifact Review - Near-Half Signal-Reliability Ledger v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (advisory delegated adversarial artifact review + bounded patch report)
scope: >
  Advisory controller review and bounded patch report for
  docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md under
  the provisional delegated review-and-patch convention.
use_when:
  - Adjudicating the delegated patch to the near-half signal-reliability ledger.
authority_boundary: retrieval_only
```

## Review Summary

```yaml
review_summary:
  status: completed
  recommendation: adjudicate_patch
  report_path: docs/review-outputs/adversarial-artifact-reviews/near_half_signal_reliability_ledger_delegated_adversarial_artifact_review_v0.md
  reviewed_target: docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md
  patch_target: docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md
  authored_by: claude-fable-5[1m]
  reviewed_by: OpenAI GPT-5 Codex
  de_correlation_bar: cross_vendor_discovery
  findings:
    - AR-01
  patch_state: working_tree_uncommitted
  non_claims:
    - advisory decision input only
    - not validation
    - not readiness
    - not acceptance
    - not source-family admission
    - not formal review-lane verdict
```

## Advisory-Only Bound

This run used the repo-mode delegated review-and-patch commission and the
runtime-visible Orca sources. The review method was reference-loaded from local
instructions, but no formal Orca review-skill lane execution is claimed here;
the result is advisory decision input unless the Chief Architect adjudicates and
accepts the diff. This report creates no validation, readiness, acceptance,
source-family admission, or formal review-lane verdict.

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_signal_reliability_review
  edit_permission: patch-only single named target + report file-write
  workspace: C:\Users\vmon7\Desktop\projects\orca-worktrees\orca-prospective-loop-wt
  branch: signal-reliability-ledger-hardening-v0
  head_observed: cf531dc
  target_blob_sha256_expected: 388352b83bac9860c3b9959d93af3d04d0c9ccfb69198cd9382f2fbe0a498102
  target_blob_sha256_observed_at_3fe878c: 388352b83bac9860c3b9959d93af3d04d0c9ccfb69198cd9382f2fbe0a498102
  target_blob_sha256_observed_at_HEAD_before_patch: 388352b83bac9860c3b9959d93af3d04d0c9ccfb69198cd9382f2fbe0a498102
  dirty_state_checked: yes; clean at start
  repo_map_decision: not_needed
  external_source_boundary: jb is not Orca authority
```

## Source-Read Ledger

| Source | Why read | Status |
| --- | --- | --- |
| `AGENTS.md` | Project rules, edit authority, verification discipline | clean at start |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint | clean at start |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy and doctrine-change boundaries | clean at start |
| `.agents/workflow-overlay/source-loading.md` | Start preflight and bounded source pack | clean at start |
| `.agents/workflow-overlay/review-lanes.md` | Review lane, advisory/strict boundary, provenance fields | clean at start |
| `.agents/workflow-overlay/prompt-orchestration.md` | Review-report output mode and source-gated method contract | clean at start |
| `.agents/workflow-overlay/validation-gates.md` | Missing-evidence and prompt/review validation boundaries | clean at start |
| `.agents/workflow-overlay/delegated-review-patch.md` | Provisional delegated review-and-patch contract | clean at start |
| `docs/prompts/templates/review/adversarial_artifact_review_v0.md` | Review method reference | clean at start |
| `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md` | Shared behavior contract reference | clean at start |
| `docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md` | Full target review and patch target | clean at start; patched by this run |
| `docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md` | N7 field map authority | clean at start |
| `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md` | Batch-1 K-of-N, report-all, org-motion cap discipline | clean at start |
| `docs/product/judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md` | Product-learning cap and promotion rules | clean at start |
| `orca-harness/schemas/judgement_models.py` | Harness `EvidenceUsed` vocabulary | clean at start |

## Reasoning Before Findings

The load-bearing seam is not the N7 field map; the target maps the far-half
architecture's `signal_id`, `decision_family`, reliability/provenance,
validation status, and staleness fields field-for-field. The strongest risk is
inside the firewall and cherry-pick guard: a row can be pre-committed yet still
let the post-reveal resolver decide what "correct direction" meant, or let many
not-applicable/unscoreable rows disappear behind a scoreable-only denominator.
That would preserve the surface K-of-N discipline while reopening the exact
post-reveal laundering channel the ledger exists to close.

The target correctly preserves the product-learning cap and JSG-01 frozen
boundary, and it uses the harness `EvidenceUsed` vocabulary consistently:
`claim_id`, `claim_text`, `claim_role`, and `evidence_unit_ids`.

## Findings

### AR-01 - Major - Scoreability and denominator were under-specified

**Location:** `docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md`, K-of-N report-all tally and ledger schema.

**Issue:** The target said every pre-committed use is tallied, but the honest
claim was phrased as "K of N pre-committed uses" while the schema denominator
was only `n_scoreable` and excluded `not_applicable` / `unscoreable`. It also
recorded `outcome` and `resolution_ref` but did not require a pre-specified
direction criterion or scoreability rationale per row. That left a gameable
path: after reveal, the resolver could define "correct_direction" loosely or
accumulate many exclusions without the headline denominator forcing them to
travel.

**Evidence:** The target's report-all rule requires correct, wrong,
not-applicable, and unscoreable rows to be tallied, while its original schema
tracked `k_correct`, `n_scoreable`, and `excluded` only. The far-half architecture
requires signal reliability evidence with provenance plus validation status and
staleness. Batch-1 requires all results to be reported and rejects selective
reporting; its org-motion amendment requires the blind signal prediction before
reveal and report-all, including feasibility failures and cases where the signal
did not move the call. The evidence ladder caps this surface at product-learning
and requires explicit promotion gates for stronger claims.

**Strongest defense:** The original text did say not-applicable and unscoreable
are reported, and `excluded` could be read as the missing total context.

**Why the defense fails:** `excluded` is a count, not a denominator invariant or
per-row scoreability explanation. It does not force downstream readers to carry
the total pre-committed population with the scoreable ratio, and it does not
prevent a post-reveal criterion from turning a vague signal direction into a
favorable `correct_direction` row.

**Impact:** Without the patch, the ledger could launder hindsight through
scoreability and denominator presentation while appearing to honor pre-commit
and report-all rules.

**Minimum closure condition:** The target must require total pre-committed uses
to travel with the scoreable ratio, and each per-use row must bind the
pre-specified resolution criterion or scoring key plus a scoreability rationale
before it can count as correct/wrong or be excluded.

**Next authorized action:** Bounded patch to the named target file only, followed
by Chief Architect adjudication of the diff.

**Advisory remediation applied:** Tightened the K-of-N claim wording, defined
`correct_direction` / `wrong_direction` as comparison to a pre-specified
criterion or scoring key, added `resolution_criteria_ref`,
`scoreability_reason`, and `n_pre_committed_total`, and updated the worked
example.

## Non-Findings

- N7 field map matched the far-half architecture's named fields:
  `signal_id`, `decision_family`, reliability evidence with provenance,
  validation status, and staleness marker.
- Product-learning and no-source-family-promotion caps were preserved.
- No evidence-ladder tier or closeout vocabulary was minted.
- Harness vocabulary use was consistent with `EvidenceUsed` fields.
- No design-level defect requiring `NEEDS_ARCHITECTURE_PASS` was found.

## Unified Diff

```diff
diff --git a/docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md b/docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md
index 28215ba..5428f8b 100644
--- a/docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md
+++ b/docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md
@@ -107,12 +107,19 @@ non-negotiable rules carried from batch-1:
 2. **Report all.** Every pre-committed `(signal, case)` use is tallied —
    correct, wrong, not-applicable, and unscoreable alike. Dropping the misses
    voids the property. The honest claim is "signal S pointed the right way in K
-   of N pre-committed uses," never "here is a case where S worked."
+   of S scoreable uses, out of T total pre-committed uses with every exclusion
+   reported," never "here is a case where S worked."
 
 Per use, the outcome is exactly one of: `correct_direction` | `wrong_direction`
 | `not_applicable` (signal didn't bear on this case) | `unscoreable`
-(outcome criterion couldn't be applied). Only `correct`/`wrong` count toward K/N;
-the others are reported but excluded from the ratio.
+(outcome criterion couldn't be applied). `correct_direction` / `wrong_direction`
+mean the pre-reveal predicted direction was compared against a pre-specified
+resolution criterion or scoring key, not a post-reveal restatement of what the
+signal "obviously" meant. If the applicable direction criterion was not fixed
+before reveal, the row is `unscoreable` or contaminated; it must not be rescued
+as a favorable correct/wrong tally after seeing the outcome. Only `correct` /
+`wrong` count toward the scoreable ratio; the total pre-committed count and all
+exclusions travel with the ratio.
 
 ## Ledger Schema v0
 
@@ -127,11 +134,14 @@ signal_reliability_ledger_v0:
           # - case_id:
           #   predicted_direction:        # recorded in the blind call (pre-reveal)
           #   blind_call_ref:             # provenance: the sealed pre-reveal judgment that carries the prediction
+          #   resolution_criteria_ref:     # pre-specified criterion/key used to compute actual direction
           #   outcome: correct_direction | wrong_direction | not_applicable | unscoreable
+          #   scoreability_reason:         # required for not_applicable/unscoreable; optional note for scoreable rows
           #   resolution_ref:             # provenance: where the post-reveal score was computed
         tally:
           k_correct:             # count of correct_direction
           n_scoreable:           # correct + wrong (the denominator)
+          n_pre_committed_total:  # correct + wrong + not_applicable + unscoreable
           excluded:              # not_applicable + unscoreable counts, reported
       validation_status:         # the N7 "validation status": product_learning (default) | <stronger only via a named gate>
       staleness:                 # the N7 "staleness marker"
@@ -199,9 +209,11 @@ reliability:
     - case_id: beautypie_repricing_2023_v0
       predicted_direction: expansion -> supports demand-positive call
       blind_call_ref: <the sealed blind judgment carrying the org-motion prediction>
+      resolution_criteria_ref: <the pre-specified outcome criterion / scoring key used to compute direction>
       outcome: correct_direction
+      scoreability_reason: scoreable under the pre-specified criterion
       resolution_ref: <where the post-reveal score was computed>
-  tally: { k_correct: 1, n_scoreable: 1, excluded: 0 }
+  tally: { k_correct: 1, n_scoreable: 1, n_pre_committed_total: 1, excluded: 0 }
 validation_status: product_learning
 staleness:
   stale_if: [Greenhouse board schema changes, beauty-family drift, N < 3]
```

## Per-Change Neutral Citations

- K-of-S/T wording: supported by the target's own report-all rule and by the
  batch-1 all-results / selective-reporting boundary.
- `resolution_criteria_ref`: supported by the far-half architecture's mechanical
  resolution discipline and the ledger's firewall-clean pre-reveal prediction
  rule.
- `scoreability_reason`: supported by the target's `not_applicable` /
  `unscoreable` categories and the prompt's concern that they could become an
  escape hatch.
- `n_pre_committed_total`: supported by batch-1's pre-commitment and report-all
  discipline; it keeps excluded rows visible beside the scoreable denominator.

## Verdict As Decision Input

Recommendation: keep the bounded patch unless the Chief Architect prefers a
different field name. The patch is narrow, preserves PROPOSED/product-learning
status, does not alter N7 field identity, and closes the main laundering seam
without widening the schema into implementation.

## Residual Risk

The ledger still depends on future step-3 postmortem artifacts to define the
actual row-production mechanics and on future live/far-half resolutions to
provide real rows. This report found no current design-level blocker, but it
does not validate the future row producer, scoring process, or decision-memory
consumer.

## Review-Use Boundary

This review and patch are decision input for home-model adjudication. They are
not approval, validation, readiness, mandatory remediation, source-family
admission, or executor-ready authority beyond the explicit bounded patch already
applied in this lane.

## Home-Model Adjudication (2026-06-13, appended by the commissioning lane)

```yaml
home_model_adjudication:
  adjudicator: claude-fable-5[1m] (author/home model; correlation disclosed — AR-01 re-checked directly against the far-half resolution doctrine, batch-1 report-all, and the firewall, not against the controller's verdict)
  diff_verified: working-tree diff matched the report's Unified Diff exactly before adjudication
  preflight_note: controller's preflight observed the re-pinned branch (signal-reliability-ledger-hardening-v0 @ cf531dc) and the unchanged blob hash 388352b8; this is the post-landing follow-up hardening pass on the ledger already on main
  per_finding:
    - finding: AR-01 (scoreability + denominator under-specified)
      decision: accepted
      basis: >
        Two faithful hardenings, both straight from existing doctrine. (1)
        Requiring a pre-specified resolution_criteria_ref per row mirrors the
        far-half's "resolution_criteria pre-specified and mechanical; resolution
        may apply them, never author them" — it closes the seam where a
        post-reveal resolver could define "correct_direction" loosely. (2)
        n_pre_committed_total forcing the full denominator to travel mirrors
        batch-1's report-all / no-selective-reporting property — it closes the
        seam where exclusions vanish behind a scoreable-only ratio. Mints no
        tier/ladder vocabulary; preserves PROPOSED / product-learning / JSG-01
        frozen; N7 field identity unchanged (these are sub-fields of the
        reliability evidence N7 already names).
  vetoes: none
  modifications: none
  kept_state: AR-01 patch kept in full + this report; committed on the hardening branch (follow-up PR)
  separate_followup_flagged:
    - A cross-lane conflict was discovered during this turn (the read-machinery handoff's backtest-distillation / per-vertical weighting layer overlaps this ledger + the near-half architecture). It does NOT affect this ledger hardening (the per-signal reliability record is the shared substrate both framings need), but it blocks step 3 until reconciled. Surfaced to the owner separately.
  non_claims:
    - adjudication is a keep-decision only; not validation, readiness, ratification, or source-family admission
    - the ledger remains PROPOSED at product-learning tier
```
