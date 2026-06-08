# Data Capture Spine Source-Observability Requirements Scoping v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Docs-only requirements scoping for source-observability pressure surfaced by the first all-slot Data Capture pressure-test synthesis.
use_when:
  - Reviewing the source-observability requirements surfaced by the first all-slot Data Capture pressure-test batch.
  - Deciding whether a later owner gate should authorize implementation scoping, source-access method-plan patch proposal, obligation-contract patch proposal, narrowing, or deferral.
  - Checking that source-observability scoping has not become tooling, runtime, source-access implementation, contract hardening, ECR, Cleaning, or Judgment design.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/data_capture_spine_source_observability_scoping_authorization_v0.md
  - docs/product/data_capture_spine_pressure_test_all_slot_synthesis_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_pressure_test_all_slot_synthesis_blast_radius_recheck_v0.md
  - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
stale_if:
  - A later owner decision accepts, rejects, narrows, or supersedes this scoping artifact.
  - The source-observability authorization is materially revised.
  - The all-slot synthesis or blast-radius recheck is materially revised.
  - The Data Capture obligation contract, source-access boundary, source-access method plan, commissioning plan, or execution authorization is materially amended before owner action on this artifact.
```

## Status

Status: `SOURCE_OBSERVABILITY_REQUIREMENTS_SCOPING_V0`.

This artifact scopes the source-observability requirements surfaced by the first
all-slot Data Capture pressure-test batch. It converts repeated capture pressure
into candidate requirement statements and owner decision questions.

This artifact does not authorize implementation, tools, runtime source systems,
scrapers, APIs, browser automation, source-access method changes, contract
hardening, ECR design, Cleaning implementation, Judgment design, buyer proof, or
commercial-readiness claims.

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes - AGENTS.md supplied in current task context
  overlay_read: yes
  source_pack: custom Data Capture source-observability requirements scoping
  edit_permission: docs-write for one product scoping artifact
  target_scope: docs/product/data_capture_spine_source_observability_requirements_scoping_v0.md
  dirty_state_checked: yes - worktree dirty; this artifact is docs-only scoping and makes no validation, readiness, implementation, runtime, or source-of-truth-promotion claim
  blocked_if_missing: none
```

## Source Basis

| Source artifact | SHA256 | Role in this scoping artifact |
| --- | --- | --- |
| `docs/decisions/data_capture_spine_source_observability_scoping_authorization_v0.md` | `88D846E7F436CDA8B39D340C07D466EE55A815F6EA2E663133CC3E20A863BACB` | Owner authorization for this bounded docs-only scoping lane. |
| `docs/product/data_capture_spine_pressure_test_all_slot_synthesis_v0.md` | `A0021F1EF42F101C2029FADEDE062461A136D082EF03B7339411BE19270FB0E5` | Primary pressure-test evidence and patchable classification. |
| `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_pressure_test_all_slot_synthesis_blast_radius_recheck_v0.md` | `46FE71284AA146971719E153AD710FC92C0CB3D455B0BC37BF495924ABFCC68D` | Review evidence that the patched all-slot synthesis is safe for owner decision input. |
| `docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md` | `3D9AC208A8AF68160A43F3EB3512082BF0F9B10D3840331FE82F544E307820EB` | Pressure-test interpretation rules, including patchable versus architecture-threatening trigger logic. |

## Scoping Boundary

This artifact may define candidate source-observability requirements and the
owner decisions those requirements create.

This artifact may not select tools, specify implementation methods, write worker
prompts, modify the source-access method plan, amend the obligation contract,
define runtime architecture, define storage, or define ECR/Cleaning/Judgment
behavior.

Where a requirement cannot be stated without selecting method or tooling, the
requirement remains an owner decision question rather than a completed
requirement.

## Evidence Summary

The all-slot synthesis found recurring source-observability pressure across all
three pressure-test slots:

- Slot 1 preserved useful M&I / BIWS pricing and bundle facts but did not
  preserve faithful source language, visible structure, or archive body content.
- Slot 2 preserved Teal access-failure posture, URL inventory, archive
  availability, and non-verbatim pointers, but the live and archived source
  bodies remained unavailable.
- Slot 3 preserved the strongest source-language anchors, especially in forum
  evidence, but still carried media, gallery, preview-image, raw-envelope, and
  venue-coverage limits.

The synthesis classified raw-observable fidelity pressure, related-context
pressure, archive/history content gaps, and below-clean handoff readiness as
`patchable` on the current record. It did not classify the batch as
`architecture-threatening`.

## Candidate Requirements

### RQ-01: Verbatim And Source-Structure Preservation

Candidate requirement:

Data Capture should preserve enough source language and visible source structure
for a later reader to inspect what the source actually said and how the source
presented it, when language or structure carries decision-relevant meaning.

Pressure-test basis:

- Slot 1 showed fact-level capture without faithful packaging/source-language
  capture.
- Slot 2 showed that no useful source-body inspection is possible when the body
  is absent.
- Slot 3 showed that bounded source-language anchors materially improve
  artifact-internal inspectability.

Minimum requirement shape:

- Capture records whether the source language is preserved, paraphrased,
  pointer-only, inaccessible, or not attempted.
- Capture records whether visible source structure is preserved, summarized,
  pointer-only, inaccessible, or not material to the source family.
- Capture does not decide whether the language or structure is persuasive,
  credible, sufficient, or useful. That remains downstream Judgment.

Owner decision question:

- Should future capture support require a default source-language and
  source-structure preservation posture for text and offer surfaces, with
  explicit exceptions when structure is not material?

Non-goals:

- no universal screenshot mandate;
- no Cleaning transformation rule;
- no Judgment materiality rule;
- no storage or schema design.

### RQ-02: Archive Snapshot Body Retrieval

Candidate requirement:

Data Capture should distinguish archive availability from archive-body
retrieval, and should preserve whether historical body content was retrieved,
failed, unavailable, or not attempted.

Pressure-test basis:

- Slot 1 and Slot 2 could identify archive availability and dates without
  retrieving archive bodies.
- Slot 3 kept archive posture visible but did not complete archive lookup for
  mutable venue surfaces.

Minimum requirement shape:

- Capture makes the archive retrieval posture visible at requirements level:
  whether current and historical source locations are knowable, whether archive
  body content was retrieved, and why it was not retrieved where applicable.
- This is a visibility requirement, not a minimum field list, schema blueprint,
  storage shape, or implementation record design.
- Capture treats archive availability without body content as a limitation, not
  as historical-source preservation.
- Capture does not infer historical content from search snippets or summaries.

Owner decision question:

- Should archive-body retrieval become a default expected capability for
  pricing, product, changelog, and mutable forum/review surfaces before future
  capture can claim clean categorical handoff?

Non-goals:

- no archive-tool selection;
- no archive API plan;
- no legal/source-rights sufficiency claim;
- no automated recapture scheduler.

### RQ-03: Screenshot, Media, And Multimodal Preservation

Candidate requirement:

Data Capture should preserve media, layout, screenshots, or other modality
evidence when the source's meaning depends on visual presentation, embedded
media, gallery assets, charts, images, app-page layout, or offer packaging.

Pressure-test basis:

- Slot 1 needed layout/packaging preservation for offer structure and pricing
  presentation.
- Slot 3 carried Reddit gallery, preview-image, and resume-image limitations.
- Slot 2 would likely need layout/media preservation if Teal page or app-state
  bodies become accessible and visually material.

Minimum requirement shape:

- Capture records whether the source is text-only, layout-bearing,
  media-bearing, or mixed.
- Capture records whether each material modality was preserved, pointer-only,
  inaccessible, not attempted, or not applicable.
- Capture keeps media limitations visible instead of replacing them with
  paraphrase or downstream assumptions.

Owner decision question:

- Should future capture support include a modality trigger that requires
  screenshot/media preservation only when layout or media carries source meaning?

Non-goals:

- no universal full-page screenshot rule;
- no image OCR/transcription pipeline;
- no computer-vision or media-processing method;
- no final storage format.

### RQ-04: In-Bound Public-Host Access Handling

Candidate requirement:

Data Capture should distinguish in-bound access failure from out-of-bounds
source acquisition, and should preserve the observable state of host, archive,
or page access failure without widening source-access boundaries.

Pressure-test basis:

- Slot 2 produced a full Teal host/source-body access failure while staying
  inside the source boundary.
- The all-slot synthesis treats the pressure as source-access and
  source-observable preservation, not boundary failure.
- Evidence-weight note: this requirement is retained from a single-slot severity
  signal, not a cross-slot count threshold. Future implementation scoping should
  reground this requirement against additional batch evidence before treating it
  as a confirmed cross-slot requirement.

Minimum requirement shape:

- Capture records whether the source attempt was in-bound and which access
  surface failed: live page, app page, archive, linked resource, host block, or
  other source-body failure.
- Capture records what remains inspectable after failure: locator, status,
  archive availability, search-summary pointer, or nothing.
- Capture keeps hard-stop exclusions intact and does not use failure as a
  reason to widen acquisition methods.

Owner decision question:

- Should future source-observability support require a standard access-failure
  posture for in-bound public-host failures before any method or tooling work is
  considered?

Non-goals:

- no source-access boundary change;
- no bypass method;
- no proxy, scraper, API, browser automation, or anti-detect plan;
- no entitlement or credential policy change.

### RQ-05: Source-Language Anchors From The Start

Candidate requirement:

For forum, review, and text-heavy discourse captures, Data Capture should carry
bounded source-language anchors from the start so later artifact-internal
inspection can distinguish source evidence from operator paraphrase.

Pressure-test basis:

- Slot 3 improved after adding source-language anchors.
- Batch 1 Reddit initially exposed that summaries and pointers alone were not
  enough for checker-visible capture closure.
- WSO remained bounded-anchor-only, showing the value and limits of source
  anchors when raw envelope coverage is incomplete.

Minimum requirement shape:

- Capture includes representative source-language anchors with source identity,
  local locator or source pointer, visible score/timing/context when available,
  and limitation notes where the anchor is partial.
- Capture preserves deleted, bot-like, low-score, adjacent, and counter-signal
  material as visible limitations or context when present; it does not remove
  rows because they look low-value.
- Capture labels source-language anchors as anchors, not as synthesis,
  conclusion, or Judgment evidence selection.

Owner decision question:

- Should future forum/text captures require bounded source-language anchors as
  part of minimum handoff readiness, while preserving raw/projection packets
  where available?

Non-goals:

- no semantic selection rule;
- no comment ranking or inclusion algorithm;
- no synthesis or credibility assessment;
- no final Evidence Candidate Record schema.

## Cross-Cutting Requirement Properties

Any later source-observability requirement should preserve these properties:

- inspectability: a later reader can see what is source-language, pointer-only,
  paraphrase, inaccessible, unavailable, or not attempted;
- preservation posture: capture distinguishes preserved raw/source-observable
  material from summary, projection, and limitation;
- failure visibility: failed access, missing media, archive-body absence, and
  pointer-only records remain explicit;
- cutoff visibility: capture records the source state and cutoff posture it
  actually used;
- source-family fit: requirements may vary by source family, but source-family
  variation must be visible rather than implicit;
- downstream boundary: Capture does not decide credibility, usefulness,
  inclusion, exclusion, discounting, Signal Use, Decision Strength, or Action
  Ceiling.

## Candidate Owner Decision Queue

This scoping artifact creates decision inputs only. It does not select any of
these decisions.

| Decision | Question | Current recommendation status |
| --- | --- | --- |
| DQ-01 | Authorize implementation scoping for a narrow source-observability support slice? | Candidate later decision after review. |
| DQ-02 | Authorize a source-access method-plan patch proposal to reflect these requirements? | Candidate later decision if requirements imply method-plan language. |
| DQ-03 | Authorize a Data Capture obligation-contract patch proposal? | Candidate later decision only if requirements expose contract wording gaps. |
| DQ-04 | Narrow the requirement set and rerun scoping? | Available if review finds overbreadth or method drift. |
| DQ-05 | Defer implementation/source-access work and run another pressure-test batch first? | Available if owner wants more evidence before implementation scoping. |

## Review Gate

Adversarial artifact review is recommended before this artifact is used to
authorize implementation scoping, source-access method-plan patch proposal, or
obligation-contract patch proposal.

The review should test:

- whether any candidate requirement smuggles a method, tool, runtime, or schema;
- whether the artifact over-generalizes one-slot evidence;
- whether owner decision questions are clear enough to act on;
- whether the non-goals and stop conditions preserve the source-access boundary;
- whether the artifact should route to implementation scoping, method-plan patch
  proposal, contract patch proposal, narrowing, or more evidence.

## Non-Claims

This artifact is not validation, readiness, pressure-test discharge, Data
Capture Spine acceptance, production adequacy, source-of-truth promotion,
implementation authorization, runtime authorization, tooling authorization,
scraper authorization, API authorization, browser-automation authorization,
source-access method-plan amendment, Data Capture obligation-contract amendment,
contract hardening, ECR design, Cleaning implementation, Judgment design, buyer
proof, or commercial-readiness evidence.

## Direction Change Propagation

No new durable doctrine is introduced by this scoping artifact. It records
candidate requirements and owner-decision questions under the already-authorized
bounded docs-only scoping lane.

The lifecycle-boundary change was already recorded in
`docs/decisions/data_capture_spine_source_observability_scoping_authorization_v0.md`,
whose `direction_change_propagation` receipt updated the source-loading and repo
map discoverability surfaces. Because this artifact does not authorize
downstream work, amend controlling sources, or change the safe set of future
moves beyond that prior authorization, no additional direction-change
propagation receipt is required here. Navigation surfaces may reference this
artifact for discoverability, but those references do not make the candidate
requirements governing doctrine.
