# Process Improvement Batch 1 — Retired Decision-Gate Evidence

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Preserved cases and retirement state for the former Batch 1 decision-gate economics pilot.
use_when:
  - Interpreting the two preserved Batch 1 cases.
  - Checking why the pilot stopped without a comparative conclusion.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-of-truth.md
```

## Retirement state

- `pilot_status`: `retired_2026-07-16`
- `comparable_cases_observed`: `1`
- `prior_closeout_eligible_at`: `8`
- `prior_hard_stop_at`: `12`
- `standing_obligations`: `none`

The pilot stopped below its own minimum comparative sample. DG-02 was the only
comparable case; DG-01 lacked source-backed method-use evidence. Extending the
collection indefinitely would add case-recording ceremony without a credible
route to the requested economics conclusion. The cases below remain historical
evidence and do not trigger any workflow method.

## DG-01 — EP-34 session-HEAD guard

```yaml
case_id: DG-01
decision_label: EP-34 session-HEAD-drift guard
implementation_bound: "yes"
original_route: >
  Build a PreToolUse guard that compares current HEAD with the session-start
  HEAD emitted by session_context_capsule.py.
load_bearing_assumption: >
  The session-start hook persisted a HEAD baseline that a later PreToolUse hook
  could read.
gate_method_use:
  deep_thinking:
    status: unknown
    evidence_pointer: unknown
  assumption_gate:
    status: unknown
    evidence_pointer: unknown
  fused_entry:
    status: unknown
    evidence_pointer: unknown
outcome: build_blocked
avoided_rework_evidence:
  observation: >
    The source records that the assumed baseline did not exist and that a build
    would instead require a new persisted per-session state substrate, which
    the owner declined.
  evidence_pointers:
    - docs/decisions/overlay_enforcement_placement_classification_v0.md:311
    - docs/decisions/overlay_enforcement_placement_classification_v0.md:318
    - docs/decisions/overlay_enforcement_placement_classification_v0.md:323
  counterfactual_amount: unknown
incremental_minutes: unknown
downstream_reversal:
  status: unknown
  evidence_pointer: unknown
exact_evidence_pointers:
  - docs/decisions/overlay_enforcement_placement_classification_v0.md:304
  - docs/decisions/overlay_enforcement_placement_classification_v0.md:308
  - docs/decisions/overlay_enforcement_placement_classification_v0.md:311
  - docs/decisions/overlay_enforcement_placement_classification_v0.md:318
  - docs/decisions/overlay_enforcement_placement_classification_v0.md:323
comparability:
  status: not_comparable
  reason: >
    The proposed build, false substrate assumption, and blocked-build outcome
    are explicit, but the cited source does not identify use of the measured
    workflow-assumption-gate method. With all method-use fields unknown, this
    case does not satisfy comparability criterion 3.
```

## DG-02 — LinkedIn live-envelope route

```yaml
case_id: DG-02
decision_label: LinkedIn live-layer envelope placement
implementation_bound: "yes"
original_route: >
  Harden the existing core envelope validators for presence and no-bypass
  posture without creating a new package.
load_bearing_assumption: >
  The existing core envelopes already carried the presence-attestation and
  entitlement-bypass fields needed for that route.
gate_method_use:
  deep_thinking:
    status: unknown
    evidence_pointer: unknown
  assumption_gate:
    status: used
    evidence_pointer: docs/review-outputs/adversarial-artifact-reviews/linkedin_live_layer_architecture_cross_vendor_review_v0.md:38
  fused_entry:
    status: unknown
    evidence_pointer: unknown
outcome: route_changed
avoided_rework_evidence:
  observation: >
    The source records that the fields were absent from core and that adding
    them there would violate isolation, so the route changed to a minimal
    satellite adapter contract record.
  evidence_pointers:
    - forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_live_layer_architecture_v0.md:16
    - forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_live_layer_architecture_v0.md:59
    - forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_live_layer_architecture_v0.md:60
    - docs/review-outputs/adversarial-artifact-reviews/linkedin_live_layer_architecture_cross_vendor_review_v0.md:39
  counterfactual_amount: unknown
incremental_minutes: unknown
downstream_reversal:
  status: unknown
  evidence_pointer: unknown
exact_evidence_pointers:
  - forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_live_layer_architecture_v0.md:11
  - forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_live_layer_architecture_v0.md:16
  - forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_live_layer_architecture_v0.md:59
  - forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_live_layer_architecture_v0.md:60
  - forseti/product/spines/scanning/source_families/linkedin/data_capture_spine_linkedin_live_layer_architecture_v0.md:61
  - docs/review-outputs/adversarial-artifact-reviews/linkedin_live_layer_architecture_cross_vendor_review_v0.md:38
  - docs/review-outputs/adversarial-artifact-reviews/linkedin_live_layer_architecture_cross_vendor_review_v0.md:39
comparability:
  status: comparable
  reason: >
    The original route, absent-field assumption, assumption-gate use, and
    adapter-route change are explicit; time and later reversal remain unknown
    without defeating comparability.
```

## Retirement boundary

Do not record DG-03 or infer a comparative economics result from this ledger.
A future owner may commission a new bounded study, but that would be a new work
unit with its own outcome and admission case, not continuation of this pilot.
