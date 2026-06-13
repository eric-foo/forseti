# Data Capture Spine Source-Observability Requirements Support Implementation-Scoping Authorization v0

```yaml
retrieval_header_version: 1
artifact_role: Product decision
scope: Owner authorization for one bounded implementation-scoping lane for post-Slot-3-recapture Source Observability requirements support.
use_when:
  - Checking whether implementation scoping is authorized from the current Source Observability requirements boundary.
  - Confirming which RQs may be scoped and which remain deferred.
  - Confirming that this authorization does not permit implementation execution, source access, method-plan amendment, contract amendment, ECR, Cleaning, or Judgment work.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_source_observability_requirements_boundary_decision_adversarial_artifact_review_v0.md
  - .agents/workflow-overlay/source-loading.md
stale_if:
  - The requirements-boundary decision is amended, rejected, or superseded.
  - A later owner decision narrows, expands, accepts, rejects, or supersedes this authorization.
  - The Data Capture obligation contract, source-access boundary, source-access method plan, or Capture/ECR/Cleaning/Judgment boundary changes in a way that alters the authorized requirements-support scope.
```

## Status And Decision

Status:
`AUTHORIZED_SOURCE_OBSERVABILITY_REQUIREMENTS_SUPPORT_IMPLEMENTATION_SCOPING_V0`.

Owner decision:
`AUTHORIZE_BOUNDED_SOURCE_OBSERVABILITY_REQUIREMENTS_SUPPORT_IMPLEMENTATION_SCOPING`.

The owner authorizes one bounded implementation-scoping lane for Source
Observability requirements support, using the current post-Slot-3-recapture
requirements-boundary decision as controlling input.

This authorization permits scoping only. It does not authorize implementation
execution, source acquisition, source-access method changes, contract
amendments, ECR, Cleaning, Judgment, validation, readiness, buyer proof, or
commercial readiness.

## Source Basis

Decision inputs:

- Current owner instruction: proceed, write this artifact, then run
  `workflow-implementation-scoping`.
- `docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md`,
  SHA256 `86944E8AFA4B8E821A27C2745108992D4B3339B77E93B79CF2E8320A68F09FC4`.
- `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_source_observability_requirements_boundary_decision_adversarial_artifact_review_v0.md`,
  SHA256 `618883D342F02BFE6A244208359EBE51C4DCF2D7A5D36207016EB641242B7583`,
  recommendation
  `safe_for_owner_use_as_requirements_boundary_basis_with_minor_patches_recommended`.

The two minor review findings were patched in the requirements-boundary
decision before this authorization:

- `AR-SB-01`: RQ-04 access-failure posture is now visibly candidate-status
  only, not a current bounded requirement.
- `AR-SB-02`: RQ-01 no longer uses the undefined capitalized term
  "Decision Frame"; it uses the original scope language around
  decision-relevant meaning.

## Authorized Scoping Scope

Authorized lane: bounded implementation scoping for Source Observability
requirements support.

The scoping lane may plan support for:

- `RQ-01`: source-language and visible source-structure preservation or
  limitation visibility;
- `RQ-05`: source-language anchors from the start for forum, review, and
  text-heavy discourse captures;
- `RQ-03`: modality-triggered media, screenshot, layout, and multimodal
  preservation or limitation visibility when those modalities carry source
  meaning;
- `RQ-02`: archive availability, archive-body retrieval state, and
  non-retrieval reason visibility.

The scoping lane may consider local support surfaces such as operator-record
shape, checklist/doc surfaces, local report semantics, or harness support only
as planning targets. It may not implement them in this lane.

## Deferred And Excluded Scope

`RQ-04` remains deferred candidate context. The scoping lane may keep access
failure visible as encountered evidence, but it must not scope source-access
handling as a current support target unless a later owner decision explicitly
prioritizes `RQ-04`.

Explicitly excluded:

- implementation execution;
- live capture or source acquisition;
- archive body retrieval as a default requirement;
- archive retrieval implementation;
- screenshot capture, browser automation, media capture, OCR, computer-vision,
  scraper, crawler, API, proxy, anti-detect, package, deployment, storage,
  dashboard, or database design;
- source-access method-plan amendment;
- Data Capture obligation-contract amendment or hardening;
- source-access boundary change;
- ECR fields, IDs, keys, schemas, storage, receipt mechanics, or file formats;
- Cleaning normalization, clustering, dedupe, translation, summarization, or
  transformation rules;
- Judgment credibility, usefulness, inclusion, exclusion, discounting, Signal
  Use, Decision Strength, Action Ceiling, ranking, or synthesis logic;
- validation, readiness, buyer proof, production adequacy, or commercial
  readiness claims.

## Stop Conditions

The implementation-scoping lane must stop and route back to the owner if:

- scoping cannot proceed without selecting a concrete archive, browser,
  screenshot, media, scraper, API, crawler, proxy, anti-detect, storage,
  database, or deployment method;
- scoping cannot proceed without changing the source-access boundary;
- scoping cannot proceed without amending the source-access method plan or Data
  Capture obligation contract;
- scoping would make source-observability support mandatory for categorical
  handoff without a separate owner decision;
- scoping would hide human capture/posture judgment behind automated extraction
  or scoring;
- scoping requires ECR, Cleaning, or Judgment schema/behavior decisions;
- scoping requires new captures, live source access, archive retrieval, media
  retrieval, screenshots, browser sessions, pressure-test execution, or
  implementation experiments.

## Relationship To Prior Local-Support Lane

`docs/decisions/data_capture_spine_source_observability_local_support_implementation_scoping_authorization_v0.md`
remains a historical authorization for the earlier local support/helper lane.
It is not the controlling authorization for this post-recapture
requirements-support scoping lane.

This authorization does not supersede the prior local-support artifact. It
creates a narrower current gate from the patched requirements-boundary decision.

## Next Gate

The next gate is implementation scoping from this authorization. That scoping
may produce:

- a bounded implementation route;
- a narrowed route;
- a stop condition;
- or a return to owner decision if the support target cannot stay inside this
  authorization.

It may not implement the route without separate implementation-execution
authorization.

## Review Timing

Adversarial review is not required merely because this authorization exists.

Adversarial review is recommended after implementation scoping and before any
implementation-execution authorization if the scoped route touches helper
behavior, report semantics, record semantics, validation/fake-pass behavior, or
source-access-adjacent support.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "The owner authorized one bounded implementation-scoping lane for post-Slot-3-recapture Source Observability requirements support covering RQ-01, RQ-03, RQ-05, and RQ-02 visibility-only, while keeping RQ-04/source-access handling and implementation execution out of scope."
  trigger: lifecycle_boundary
  controlling_sources_updated:
    - "docs/decisions/data_capture_spine_source_observability_requirements_support_implementation_scoping_authorization_v0.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md"
    - "docs/decisions/data_capture_spine_source_observability_local_support_implementation_scoping_authorization_v0.md"
  intentionally_not_updated:
    - path: "AGENTS.md"
      reason: "The workspace rule already requires explicit bounded authorization for implementation/runtime work; this decision applies that rule without changing top-level instructions."
    - path: ".agents/workflow-overlay/README.md"
      reason: "Overlay entrypoint and binding rule unchanged."
    - path: ".agents/workflow-overlay/source-of-truth.md"
      reason: "The source hierarchy and propagation contract did not change; this decision applies the existing lifecycle-boundary trigger."
    - path: "docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md"
      reason: "The requirements-boundary decision remains the controlling RQ classification; this artifact records a downstream scoping authorization without rewriting the boundary."
    - path: "docs/decisions/data_capture_spine_source_observability_local_support_implementation_scoping_authorization_v0.md"
      reason: "Prior local-support authorization remains historical and is not the controlling gate for this post-recapture requirements-support scoping lane."
  stale_language_search: "executed across touched files; over-authorization query found only non-claims, and navigation query found the new authorization in source-loading/repo-map as intended"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not implementation execution authorization"
    - "not source-access implementation authorization"
    - "not contract hardening"
```

## Validation Readback

Validation checks performed:

- fresh readback of this authorization artifact;
- targeted readback of source-loading and repo-map entries for this
  authorization;
- SHA256 computation for this authorization artifact, source-loading, and repo
  map;
- over-authorization scan across touched files for source-access, archive,
  media, browser, runtime, ECR, Cleaning, Judgment, implementation execution,
  validation-ready, and ready-for-implementation language;
- `git diff --check` across touched files.

Observed results before this validation section was added:

- fresh readback showed the authorization status, authorized scope, excluded
  scope, stop conditions, prior-local-support relationship, and propagation
  receipt in this artifact;
- source-loading and repo-map readback showed the new authorization path and
  the intended bounded-scope descriptions;
- SHA256 values observed:
  - this artifact:
    `054BC37FA8BE38B29FF96D615D8A2546A44FD0B05E57F0742EE4087EFAB8CA86`;
  - `.agents/workflow-overlay/source-loading.md`:
    `67EEA95B60E857E6FBECA0287962BE7E5585918E995E51CED413D704C0A7239C`;
  - `docs/workflows/orca_repo_map_v0.md`:
    `DBA554BD5F98FB6A8C6DA76968ACB2D5338AAB7CA423417394EFC22F00738FB8`;
- over-authorization scan found only the non-claim phrase
  `not implementation execution authorization` and the Non-Claims section's
  `implementation execution authorization` exclusion in this artifact;
- `git diff --check` returned no whitespace-error output; Git printed
  line-ending warnings for the touched source-loading and repo-map files.

This validation readback is not validation, readiness, acceptance, source
promotion, implementation execution authorization, or implementation-start
readiness.

## Non-Claims

This decision is not validation, readiness, source-of-truth promotion,
pressure-test discharge, Data Capture Spine acceptance, production adequacy,
implementation execution authorization, runtime authorization, tooling
authorization, source-system authorization, scraper authorization, API
authorization, browser-automation authorization, archive-retrieval
authorization, media-capture authorization, source-access method-plan
amendment, Data Capture obligation-contract amendment, contract hardening,
schema authorization, ECR design, Cleaning implementation, Judgment design,
buyer proof, or commercial-readiness evidence.
