# Data Capture Spine Source-Observability Requirements Boundary Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Product decision
scope: Post-Slot-3-recapture decision on which source-observability candidate requirements survive as bounded Data Capture requirements context.
use_when:
  - Checking current Source Observability requirements status after Slot 3 recapture.
  - Deciding whether the earlier source-observability requirements scoping artifact is current or stale-alone.
  - Preparing later non-implementation scoping or review around Data Capture source observability.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_all_slot_synthesis_post_slot3_recapture_delta_v0.md
  - forseti/product/spines/capture/core/operating_model/data_capture_spine_source_observability_requirements_scoping_v0.md
  - .agents/workflow-overlay/source-loading.md
stale_if:
  - Slot 3 capture posture is reopened, downgraded, or materially recaptured again.
  - The post-Slot-3-recapture delta is amended, rejected, or superseded.
  - A later owner decision accepts, rejects, narrows, or supersedes these RQ classifications.
  - The Data Capture obligation contract, source-access boundary, source-access method plan, or Capture/ECR/Cleaning/Judgment boundary changes in a way that alters source-observability requirements.
```

## Status And Decision

Status: `SOURCE_OBSERVABILITY_REQUIREMENTS_BOUNDARY_DECIDED_V0`.

Owner instruction basis: proceed through the scoped docs-only route after
`workflow-spec-writing` if the contract was bounded enough.

Decision: carry forward a bounded Source Observability requirements boundary
for Data Capture after the Slot 3 recapture upgrade.

This decision makes current the RQ classification below. It does not authorize
implementation, source acquisition, source-access method changes, contract
amendments, ECR, Cleaning, Judgment, validation, readiness, buyer proof, or
commercial readiness.

## Spec-Writing Gate

`workflow-spec-writing` was invoked before this artifact was written.

Spec status: `SPEC_NOT_NEEDED_READY_FOR_SCOPING`.

Implicit contract used:

- The artifact must decide current requirements-boundary status only.
- It must classify RQ-01 through RQ-05 after Slot 3 recapture.
- It must distinguish accepted post-recapture input from stale candidate
  context.
- It must preserve non-implementation and downstream-layer boundaries.

A separate spec artifact would add ceremony because the scoped route already
fixed required behavior, non-goals, interface boundary, acceptance evidence, and
handoff intent.

## Source Basis

| Source artifact | SHA256 | Role in this decision |
| --- | --- | --- |
| `docs/decisions/data_capture_spine_post_slot3_recapture_delta_lane_local_acceptance_decision_v0.md` | `B4CC4B916CBC35CCDF853650A6F7C4220AF622123D8BD773CF01CED096134E2A` | Accepts the post-recapture delta as lane-local input to this one docs-only requirements-boundary decision. |
| `docs/product/data_capture_spine_pressure_test_all_slot_synthesis_post_slot3_recapture_delta_v0.md` | `43B7903ED3A173A17CC8C9C71780F43158744932A3BF5A72B9C3178F4F4DB302` | Current post-Slot-3-recapture delta and support-threshold classification. |
| `docs/product/data_capture_spine_source_observability_requirements_scoping_v0.md` | `B242238DA1F456949F858115E7E7B7ACF31BD01BEA38D3CC3FEE98BCD4B55625` | Candidate RQ context from the pre-recapture all-slot synthesis; stale-alone after recapture. |
| `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_post_slot3_recapture_delta_adversarial_artifact_review_v0.md` | `C2E894C91ED787D7879579EAA35DF03006F97739F20DE43AC348274D9BB7D544` | Review support for using the post-recapture delta after minor patching. |

## Current Input Versus Stale Candidate Context

The accepted post-Slot-3-recapture delta is the current input for this decision.
It corrects the old all-slot synthesis on Slot 3 posture and media/visible
envelope facts and records that Slot 3 now reaches
`categorical_handoff_to_ECR` with visible limitations.

`docs/product/data_capture_spine_source_observability_requirements_scoping_v0.md`
is stale as a standalone current basis. It was written before the Slot 3
recapture upgrade and still reflects pre-recapture Slot 3 media, gallery,
preview-image, and raw-envelope limitations as active basis.

The old scoping artifact remains valid candidate context for RQ-01 through
RQ-05. It is not current governing doctrine by itself, and future agents should
not use it without this decision or a later superseding decision.

## RQ Classification

| RQ | Current classification | Decision |
| --- | --- | --- |
| RQ-01: Verbatim And Source-Structure Preservation | `carry_forward_modified` | Carry forward as a bounded Data Capture source-observability requirement: capture must preserve enough source language and visible source structure, or visibly record the limitation, when language or structure carries decision-relevant meaning. |
| RQ-02: Archive Snapshot Body Retrieval | `modify_split` | Carry forward archive availability, archive-body retrieval state, and non-retrieval reason visibility now. Defer any default requirement that archived body content must be retrieved before categorical handoff; that default needs source-family scoping or a later owner decision. |
| RQ-03: Screenshot, Media, And Multimodal Preservation | `carry_forward_modified` | Carry forward as modality-triggered preservation: media, screenshots, layout, gallery assets, charts, images, or app-page presentation must be preserved or limitation-visible when they carry source meaning. This is not a universal screenshot or media mandate. |
| RQ-04: In-Bound Public-Host Access Handling | `defer_with_visible_candidate_status` | Defer as a source-access/source-observability candidate. Current evidence keeps access failure handling visible, especially from Slot 2 and bounded WSO limits, but does not change source-access boundary or authorize source-access method-plan amendment. |
| RQ-05: Source-Language Anchors From The Start | `carry_forward` | Carry forward for forum, review, and text-heavy discourse captures: capture artifacts should include bounded source-language anchors from the start when later artifact-internal inspection would otherwise depend on operator paraphrase. |

## Requirements Boundary

Current bounded Source Observability requirements context consists of:

- source-language and visible source-structure preservation or explicit
  limitation state;
- source-language anchors from the start for forum, review, and text-heavy
  discourse captures;
- modality-triggered media, screenshot, layout, and multimodal preservation
  when those modalities carry source meaning;
- archive availability, archive-body retrieval state, and non-retrieval reason
  visibility;
- visible access-failure posture where already encountered, reflecting the
  deferred candidate status of `RQ-04` rather than a current bounded
  requirement, without changing the source-access boundary.

These requirements govern what Capture must make inspectable or limitation
visible. They do not govern credibility, usefulness, inclusion, exclusion,
discounting, Signal Use, Decision Strength, Action Ceiling, buyer proof, or
commercial meaning.

## Boundary Guards

This decision does not authorize source-access expansion. `RQ-04` remains
deferred because source-access handling could otherwise collapse into method
selection. The current hard line remains outside this artifact.

This decision does not authorize tooling. It does not select or build scrapers,
APIs, browser automation, archive automation, media capture systems, storage,
dashboards, tests, packages, or runtime source systems.

This decision does not define ECR fields, keys, IDs, schemas, storage, receipt
mechanics, Cleaning transformations, Judgment rules, scoring, ranking,
credibility assessment, or evidence selection.

This decision does not harden the Data Capture obligation contract or amend the
source-access method plan. Later changes to either surface require a separate
owner authorization naming that scope.

## Current Use Of Prior Scoping Artifact

Future agents may use
`docs/product/data_capture_spine_source_observability_requirements_scoping_v0.md`
for:

- candidate RQ wording;
- pressure-test basis from the first all-slot synthesis;
- owner-decision questions that remain historically useful.

Future agents must not use it for:

- current Slot 3 posture;
- current Slot 3 media/visible-envelope limitation state;
- current RQ classification after recapture;
- implementation, source-access, contract, ECR, Cleaning, Judgment, validation,
  readiness, buyer-proof, or commercial-readiness authority.

## Next Allowed Decision

The next bounded content decision may choose one of these routes:

- write a non-implementation requirements note or implementation-scoping
  authorization for the carried-forward Source Observability requirements;
- narrow the carried-forward requirements before any implementation scoping;
- prioritize the deferred `RQ-04` source-access/access-failure candidate despite
  its lower-confidence evidence base;
- defer support work and run another pressure-test batch.

Any implementation or source-action route requires separate owner authorization.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "The current Data Capture Source Observability requirements boundary is now post-Slot-3-recapture: RQ-01, RQ-03, and RQ-05 carry forward; RQ-02 is split into visibility-now/body-retrieval-default-deferred; RQ-04 is deferred candidate context."
  trigger: product_doctrine
  controlling_sources_updated:
    - "docs/decisions/data_capture_spine_source_observability_requirements_boundary_decision_v0.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
  downstream_surfaces_checked:
    - "AGENTS.md"
    - ".agents/workflow-overlay/README.md"
    - ".agents/workflow-overlay/source-of-truth.md"
    - ".agents/workflow-overlay/source-loading.md"
    - "docs/workflows/orca_repo_map_v0.md"
    - "docs/product/data_capture_spine_source_observability_requirements_scoping_v0.md"
  intentionally_not_updated:
    - path: "AGENTS.md"
      reason: "No agent-wide behavior rule changed; this is a Data Capture product-decision boundary."
    - path: ".agents/workflow-overlay/README.md"
      reason: "Overlay entrypoint and binding rule unchanged."
    - path: ".agents/workflow-overlay/source-of-truth.md"
      reason: "Doctrine-change propagation mechanics unchanged."
    - path: "docs/product/data_capture_spine_source_observability_requirements_scoping_v0.md"
      reason: "Left intact as historical candidate context; this decision records its stale-alone status instead of rewriting its source basis."
  stale_language_search: "executed across touched files; stale Slot 3 query found only the intentional stale-context note in this artifact, and over-authorization query found only non-claims, boundary guards, or overlay/repo-map authority text"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not implementation authorization"
    - "not source-access method-plan amendment"
    - "not obligation-contract amendment"
```

## Validation Readback

Validation checks performed:

- fresh readback of this decision artifact;
- SHA256 computation for this decision artifact, source-loading, and repo map;
- over-authorization scan across touched files for implementation, runtime,
  tooling, scraper/API/browser automation, source-access method-plan,
  obligation-contract, ECR, Cleaning, Judgment, validation, readiness, buyer
  proof, commercial-readiness, and source-of-truth-promotion language;
- stale Slot 3 scan across touched files for pre-recapture posture/media terms;
- `git diff --check` across touched files.

Observed results before this validation section was added:

- fresh readback showed the RQ table, stale-basis section, boundary guards, and
  direction-change propagation receipt in this artifact;
- SHA256 values observed:
  - this artifact:
    `34A39FA79FFB6B384CAACC5B45BBBF0E84CB6D20223E68C3B86C78841D449131`;
  - `.agents/workflow-overlay/source-loading.md`:
    `D584146C7D9E3DBB5E6C65DC1699C1376A22CF87C70136A8F048D9F7969C3E0B`;
  - `docs/workflows/orca_repo_map_v0.md`:
    `735C87F70B443945E07138743610C2A166E865A235086585892BDEB05D174040`;
- over-authorization scan found expected non-claim, boundary-guard,
  source-loading, and repo-map hits only; no operative implementation,
  runtime, source-access, ECR, Cleaning, Judgment, validation, readiness, buyer
  proof, or commercial-readiness authorization was found;
- stale Slot 3 scan found only the intentional stale-context note that the old
  scoping artifact reflected pre-recapture media/gallery/preview-image/raw
  envelope limitations;
- `git diff --check` returned no whitespace-error output; Git printed
  line-ending warnings for the touched source-loading and repo-map files.

This validation readback is not validation, readiness, acceptance, source
promotion, or implementation authorization.

## Non-Claims

This decision is not validation, readiness, source-of-truth promotion,
pressure-test discharge, Data Capture Spine acceptance, production adequacy,
implementation authorization, runtime authorization, tooling authorization,
scraper authorization, API authorization, browser-automation authorization,
archive-automation authorization, source-access method-plan amendment, Data
Capture obligation-contract amendment, contract hardening, ECR design, Cleaning
implementation, Judgment design, buyer proof, or commercial-readiness evidence.
