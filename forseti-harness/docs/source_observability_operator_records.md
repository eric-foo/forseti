# Source Observability Operator Records

Use operator records when a capture artifact already exists and you need a
structured local input for the source-observability report runner.

These records are human observations about what the capture visibly preserves.
They are not extracted source truth, capture validation, capture readiness, ECR
receipt, Cleaning output, Judgment output, source acquisition, archive retrieval,
browser automation, or source-quality scoring.

## When To Write Records

Write records during or after a bounded capture pass, before running:

```powershell
python runners/run_source_observability_report.py <records.yaml> --output <report.json>
```

Use one record for each source slice where limitations should stay inspectable:
a source page, forum thread group, media-bearing slice, archive posture, access
failure, or venue unit.

Do not use records to decide whether a source is credible, useful, sufficient,
included, excluded, discounted, or decision-material.

## Minimal Input Shape

The runner accepts local YAML or JSON containing either a list of records or a
mapping with `records`.

A runnable local template is available at
`forseti-harness/docs/source_observability_operator_records_template.yaml`. It uses
generic example records and is intended as an operator-facing starting shape,
not as a canonical schema, required handoff packet, or source-family rule.

```yaml
records:
  - record_id: EXAMPLE-FORUM-ANCHORS
    source_ref: docs/product/example_capture.md#raw-observable-pointers
    source_family: forum_discourse
    source_language_posture: preserved
    source_structure_posture: paraphrased
    archive_body_posture: not_attempted
    media_posture: pointer_only
    access_posture: preserved
    locator_visible: true
    cutoff_visible: true
    source_language_anchor_count: 4
    source_language_anchor_required: true
    source_structure_required: true
    media_required: true
    archive_body_expected: true
    limitation_notes:
      - "Source-language anchors are visible, but full thread structure, media files, and archive body were not preserved."
```

## Current Data Capture Requirements Boundary

For the current Data Capture source-observability support lane, use records to
keep these surfaces inspectable or limitation-visible:

- source-language anchors and visible source structure when language or
  structure carries decision-relevant meaning;
- source-language anchors from the start for forum, review, and text-heavy
  discourse captures;
- media, screenshots, layout, gallery assets, charts, images, or app-page
  presentation when those modalities carry source meaning;
- archive availability, archive-body retrieval state, and the reason an archive
  body was not retrieved.

Do not treat these records as archive-retrieval, media-capture, browser, API,
scraper, or source-access method instructions. Access failures may be recorded
when encountered so the limitation stays visible, but access handling remains
deferred candidate context rather than a current support target.

Valid posture values are:

- `preserved`
- `paraphrased`
- `pointer_only`
- `inaccessible`
- `failed`
- `not_attempted`
- `not_applicable`

## Common Mappings

Use `preserved` when the capture visibly contains the source-language,
structure, archive body, media, or access state being recorded.

Use `paraphrased` when the capture contains operator-rendered summary or
description instead of inspectable source form.

Use `pointer_only` when the capture keeps a URL, locator, preview, image link,
search-summary pointer, or source reference but not the underlying body or media
needed for direct inspection.

Use `inaccessible` or `failed` when the source attempt stayed in bounds but the
body, archive, linked resource, host, or page state could not be reached. Keep
`locator_visible` and `cutoff_visible` true only if the artifact visibly records
that context.

Use `not_attempted` when the capture did not try to retrieve the archive body,
media, raw envelope, or access surface. Do not convert a non-attempt into a
preserved source state.

Use `not_applicable` only when the source family or slice genuinely does not
have that observable surface.

For archive fields, `archive_body_expected: true` means the operator is marking
that source slice as needing archive-body visibility for later inspection. It is
not a default rule that every archive-available source must retrieve an archive
body before categorical handoff.

## Pressure-Test Examples

Pointer-only media:

```yaml
media_posture: pointer_only
media_required: true
limitation_notes:
  - "The capture preserved image URLs or previews, but not local media files."
```

Archive availability without body:

```yaml
archive_body_posture: not_attempted
archive_body_expected: true
limitation_notes:
  - "Archive availability or dates are visible, but archive body content was not retrieved."
```

In-bound access failure:

```yaml
access_posture: inaccessible
locator_visible: true
cutoff_visible: true
limitation_notes:
  - "The capture records the blocked host/page state and cutoff as candidate-visible access context, but no source body is inspectable."
```

Bounded source-language anchors:

```yaml
source_language_posture: preserved
source_language_anchor_count: 3
source_language_anchor_required: true
limitation_notes:
  - "Representative anchors are visible, but the full raw envelope or complete comment graph is not preserved."
```

## Interpretation Boundary

The runner reports structured visible limitations from these records. It cannot
prove the capture is complete, faithful, clean, or ready. If a report looks
clean, that only means the supplied operator records did not expose limitations
the helper knows how to flag.

The JSON report also includes `record_summaries`, which echo the operator
posture records so limitation notes and posture choices remain inspectable next
to the emitted limitation types.
