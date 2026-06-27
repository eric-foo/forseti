# Creator Signal Spine Pre-Ratification Review Input v0

```yaml
retrieval_header_version: 1
artifact_role: review_input
scope: >
  Pre-ratification review input for the proposed high-level Creator Signal spine
  and creator intelligence product surface. This is a review target only; it
  does not create, bind, route, or propagate the spine.
use_when:
  - Reviewing whether Creator Signal should become a high-level Orca product/signal spine.
  - Checking the proposed boundary between creator-facing signal surfaces and low-level Capture/Data Lake contracts.
  - Preparing the post-review promotion patch if the delegated review is adjudicated as keep.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md
  - orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md
  - .agents/workflow-overlay/artifact-folders.md
  - .agents/workflow-overlay/source-of-truth.md
  - orca/product/README.md
stale_if:
  - The Creator Signal spine is accepted, rejected, or superseded by a later product/architecture decision.
  - The low-level creator profile current view contract moves or is superseded.
  - The owner reopens whether this should remain under Capture or Product Lead instead of a high-level Creator Signal spine.
```

## Status

`PRE_RATIFICATION_REVIEW_INPUT_V0`.

This artifact is intentionally not a bound product contract. It packages the
proposed shape for delegated review before any promotion patch creates
`orca/product/spines/creator_signal/` or updates route surfaces.

## Review Purpose

Attack this proposed move:

> Add `creator_signal` as a high-level Orca product/signal spine for the
> creator-intelligence surface, while keeping identity, metric observation,
> metric rollup, ideal-audience inference, storage, and capture mechanics in
> their existing low-level owners.

The owner wants the eventual surface to be Orca-facing and buyer-facing: a
one-stop view of a creator's identity links, ideal audience, aggregate influence,
freshness, and limitations. The owner does not want the low-level identity ledger
to become one giant ledger.

## Current Accepted Base

Already in place:

- Low-level current-view contract:
  `orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md`
- Public handle linkage contract:
  `orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md`
- Static identity ledger scaffold:
  `orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_v0.json`

The low-level Capture contract already separates:

- identity linkage;
- per-content metric observations;
- aggregate metric rollups such as average views and engagement rate;
- ideal-audience profile snapshots;
- the derived `creator_profile_current` operator surface.

That contract should stay low-level. This review input asks whether a separate
high-level spine should later own the productized creator signal surface.

## Proposed High-Level Spine

Proposed home after review and adjudication:

```text
orca/product/spines/creator_signal/
```

Proposed first promoted artifact after review:

```text
orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md
```

Proposed spine role:

```text
Creator Signal owns the product-facing interpretation and presentation layer for
creator intelligence: which creator facts matter to Orca operators or buyers,
how those facts are grouped into a current profile, what decisions the profile
supports, and which limits must remain visible.
```

This spine would not own source capture, raw storage, rollup computation, or
person identity. It would consume lower-level contracts and decide the product
surface that packages their outputs.

## Proposed Boundary

Creator Signal should own:

- creator intelligence surface contracts;
- dashboard/profile information architecture;
- buyer/operator decision language for creator fit and influence;
- required limitation displays and freshness displays;
- product-facing non-claims for creator signal use;
- the high-level carve-out for creator signals if it grows beyond Capture.

Creator Signal should not own:

- public-handle identity ledger rows;
- platform account linkage evidence;
- individual reel/video metric observations;
- metric rollup computation recipes;
- ideal-audience inference schemas;
- SQLite or other physical storage;
- raw capture, scraping, runners, schedulers, or data lake jobs;
- public person-level directories;
- contact enrichment, outreach authorization, or lead-list export.

## Candidate Surface Contract

A promoted `creator_intelligence_profile_surface_v0.md` should define:

- the first-screen creator profile layout or equivalent product surface;
- required sections: identity links, platform accounts, aggregate influence,
  ideal audience/content fit, freshness, limitations, and source drill-back;
- what aggregate metrics may appear, such as average views and engagement rate,
  and that they are sourced from metric rollups rather than identity rows;
- when an influence summary may be shown and when it must be withheld;
- buyer/operator language that avoids legal-name, real-person, contact, or
  actual-audience demographic claims;
- explicit source pointers back to the low-level sibling records.

## Promotion Patch, If Kept

If delegated review and CA adjudication keep this direction, the later promotion
patch should be a separate doctrine/route propagation pass. Minimum likely
surfaces:

- create `orca/product/spines/creator_signal/README.md`;
- create `orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md`;
- update `orca/product/README.md` to list the new spine;
- update `.agents/workflow-overlay/artifact-folders.md` to list the new spine;
- update `docs/workflows/orca_repo_map_v0.md` to route the spine;
- update `docs/workflows/data_capture_spine_consolidation_map_v0.md` only if it
  needs a cross-pointer back from Capture;
- include a `direction_change_propagation` receipt in the controlling changed
  artifact.

`repo-structure.yaml` is not expected to need an edit because current source says
per-spine structure is owned by the spine-first binding, not the machine map.
The reviewer should challenge that assumption if it is wrong.

## Reviewer Attack Points

Review should focus on these questions:

- Is `creator_signal` a real spine, or is this better as Product Lead offer
  language, Capture surface language, or a satellite?
- Does the proposal preserve the low-level Capture/Data Lake boundary, or does
  it sneak in storage, capture, or runtime obligations?
- Is the surface too early before real-row tests prove the metric and audience
  shapes?
- Does the naming imply public-facing creator directory, outreach, or person
  identity claims?
- Are the promotion surfaces complete enough to avoid a half-bound spine?
- Should the first promoted artifact be a surface contract only, or should there
  be a separate spine README first?

## Non-Claims

This review input does not:

- create the Creator Signal spine;
- update route maps or product README surfaces;
- ratify product or architecture doctrine;
- move the low-level creator profile contract out of Capture;
- create SQLite, a dashboard, a data lake job, runtime code, or real creator
  rows;
- authorize live capture, source access, outreach, contact enrichment, or a
  public creator directory;
- claim validation, readiness, buyer proof, or commercial usefulness.
