# Source Observability Scalability Note

This note records how the local source-observability helper should scale after
the first Slot 3 WSO, Slot 1 M&I/BIWS, and Slot 2 Teal dry-use passes.

It is a harness-local application note. It is subordinate to the Data Capture
obligation contract, the Data Capture/Cleaning/Judgment boundary, and the
source-observability local support authorization. It does not create product
doctrine, source-access authority, fixture policy, or a required handoff gate.

## Current Evidence Base

The helper has been dry-used against three different pressure-test shapes:

- Slot 3 WSO: forum-like venue evidence with bounded source-language anchors,
  discovery inventory, hidden-comment/gated-access posture, and missing raw
  HTML, screenshots, archive body, full thread graph, hidden comments, and
  exact per-page acquisition evidence.
- Slot 1 M&I/BIWS: non-forum offer/pricing evidence with pricing facts, bundle
  structure, redirected pages, archive-availability posture, layout loss, and
  archive-body access failure.
- Slot 2 Teal: full source-body access failure with live-page HTTP 403 posture,
  archive availability without archive bodies, URL inventory, non-verbatim
  search-summary pointers, help/app/job carrier pointers, and no inspectable
  Teal source language, source structure, raw HTML, screenshot, layout, or
  verified pricing/features body content.

The same local record model handled all three without schema expansion. The
evidence supports keeping the current helper small while adding discipline for
future extension.

Slot 2 added a useful negative test: the helper emitted visible limitations for
access failure, archive-body absence, missing source-language anchors, missing
source structure, and missing media/layout evidence without treating the report
as a clean pass. The mild friction was semantic rather than structural:
`access_posture: pointer_only` and generic limitation types can represent
pointer-only inventory and search-summary posture only when `record_summaries`
and `limitation_notes` remain visible. That friction should travel as visible
limitation evidence, not as immediate field-expansion justification.

## Local Helper Boundary

Source-observability records are operator-authored posture observations about a
capture artifact. They are not extracted source truth.

The helper may help an operator record whether source language, visible source
structure, archive body content, media/layout evidence, access posture,
locator context, cutoff context, and limitation notes are visible.

The helper must not:

- acquire sources;
- retrieve archive bodies;
- preserve media or screenshots;
- automate browsers, scrapers, APIs, crawlers, proxies, or source access;
- decide source quality, credibility, relevance, inclusion, exclusion,
  discounting, Signal Use, Decision Strength, or Action Ceiling;
- define ECR fields, receipt IDs, schemas, storage, or file formats;
- perform Cleaning transformations;
- perform Judgment or synthesis;
- claim capture validation, capture readiness, buyer proof, commercial
  readiness, or source adequacy.

Human posture judgment must remain visible. The helper should expose what the
operator says is preserved, paraphrased, pointer-only, inaccessible, failed,
not attempted, or not applicable.

## Source-Slice Posture Record Discipline

The primary local record unit is a source-slice posture record.

Use one record for one source slice whose posture is uniform enough to inspect:
a page, forum thread group, media-bearing slice, archive posture, access
failure, venue unit, or other bounded source surface.

Do not collapse divergent states into one record when that would hide a
limitation. Split records when locator, archive body, access, cutoff, media,
source-language, or visible-structure posture materially differs.

Examples:

- a current live offer page and a failed archive-body attempt should remain
  distinguishable;
- a public anchor pass and hidden-comment access failure should remain
  distinguishable;
- source-language anchors and pointer-only media should not be rolled into a
  clean combined posture;
- archive availability without archive-body retrieval remains a limitation,
  not historical-source preservation.
- URL inventory and non-verbatim search-summary pointers should remain
  distinguishable from preserved source language or verified source claims.

Current structured fields are provisional helper fields. They are not promoted
Core Spine invariants, final capture obligations, or ECR schema fields.

Source-family specifics should remain in `source_family` and
`limitation_notes` until repeated pressure justifies a structured helper field
or a product-level decision accepts a specific invariant.

## Report Output Invariants

The report output should preserve:

- emitted limitations;
- `record_summaries`, so each operator posture record remains inspectable next
  to the emitted limitation types;
- `non_claims`, so reports do not read as validation, readiness, ECR receipt,
  Cleaning output, Judgment output, source acquisition, archive retrieval,
  browser automation, or source-quality scoring.

A report with no emitted limitations is not a pass. It only means the supplied
operator records did not expose limitations the helper knows how to flag.

The helper is not a required handoff gate. It can support pressure-test
inspection and operator consistency, but it must not become the condition for
categorical handoff.

## Extension And Promotion Rule

Prefer `limitation_notes` and record splitting before adding fields.

Add a new structured field or limitation type only when one of these is true:

- at least two non-overlapping source families show the same source-observability
  pressure; or
- the owner explicitly signs off on one specific invariant claim.

Owner signoff attaches to the specific invariant, not a broad category such as
"forums", "pricing pages", or "source observability".

Possible future examples include clearer first-class support for
bounded-anchor-only posture, mixed access posture, pointer-only inventory, or
full-comment-graph absence. Those remain candidate helper refinements until
accepted through the extension rule above.

The first three dry-use passes do not yet justify promoting those examples into
structured fields. Continue using record splitting and `limitation_notes` unless
future source families show repeated pressure that cannot be represented without
losing limitation visibility.

## Forbidden Expansion

Do not use this helper note to authorize or backdoor:

- source-access method planning;
- archive-body retrieval implementation;
- screenshot, media, or multimodal preservation implementation;
- live capture;
- browser automation;
- storage, dashboards, databases, or deployment;
- source-access boundary changes;
- Data Capture obligation-contract hardening;
- ECR, Cleaning, or Judgment design.

If future work needs those capabilities, route it through a separate owner
authorization and the controlling product documents.

## Dry-Run Output Lifecycle

Dry-run outputs are scratch unless a later fixture policy accepts them.

This applies to both:

- operator-authored input YAML; and
- generated report JSON.

The current dry-run path under `orca-harness/reports/source_observability/` is
operator-chosen output, not a blessed durable fixture location.

Do not ignore, delete, move, or bless the whole `orca-harness/reports/`
directory from source-observability cleanup. That directory may contain
live-looking harness files unrelated to these dry-run outputs.

If later cleanup or `.gitignore` work is authorized, target specific dry-run
file patterns, not the entire `orca-harness/reports/` tree. Pattern examples
such as source-observability `*_dry_run.yaml` and `*_dry_run.json` are
illustrative only; the cleanup lane must confirm actual file names before
acting.

If a dry-use case is later promoted to a tracked fixture, the durable fixture
should preserve the operator-record input and regenerate the report
deterministically from it. The generated report may be checked only if a later
fixture policy accepts its location and refresh rule.

The broader untracked `orca-harness/reports/` state is a repo-health issue, not
part of this note's local support scope.

## Non-Claims

This note is not validation, readiness, fixture acceptance, health cleanup
authorization, `.gitignore` policy, file-pattern policy, reports-tree policy,
source-of-truth promotion, source acquisition, archive retrieval, media
preservation, browser automation, ECR receipt, Cleaning output, Judgment
output, source-quality scoring, buyer proof, or commercial-readiness evidence.
