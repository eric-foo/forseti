# Process Improvement Batch 1 — Decision-Gate Economics

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Active case ledger for the temporary Batch 1 decision-gate economics pilot.
use_when:
  - Recording a closed implementation-bound decision in Batch 1.
  - Checking sample comparability, evidence gaps, or closeout state.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/batch1-decision-gate-economics.md
stale_if:
  - .agents/workflow-overlay/batch1-decision-gate-economics.md changes the case schema, outcome vocabulary, or lifecycle.
  - A cited source is materially rewritten or superseded.
```

## Operating state

- `pilot_status`: `active`
- `comparable_cases_observed`: `1`
- `count_basis`: fresh 2026-07-11 re-derivation; DG-02 qualifies and DG-01 does not have source-backed method-use evidence
- `closeout_eligible_at`: `8`
- `hard_stop_at`: `12`
- `authority`:
  `.agents/workflow-overlay/batch1-decision-gate-economics.md`

Append a case only after the implementation-bound decision is closed enough to
identify its route outcome. Use the overlay-owned case contract exactly. Unknown
values remain unknown; this ledger does not infer method use, elapsed minutes,
non-reversal, or causal savings.
The observed count and each `comparability.status` are cached routing
assessments. The closing Chief Architect re-resolves every counted case and
re-derives comparability from the overlay criteria; these fields never clear a
threshold by assertion alone.

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

## Next recording move

Record `DG-03` only when its required fields have exact evidence. Do not add a
case merely because a gate was mentioned or a prompt was authored.
