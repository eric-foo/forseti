# IG Reels-Grid Projection To ECR Consumption Decision

```yaml
retrieval_header_version: 1
artifact_role: Workflow lane decision record (ECR consumption check closeout)
scope: >
  Records the resolved Open Decision from the projection->ECR consumption handoff
  (docs/workflows/ig_reels_projection_to_ecr_consumption_handoff_v0.md): whether any
  existing ECR/SCR consumer needs a by-key reference to the IG reels-grid projection
  rows, or whether the packet_id/slice_id keys they already key to raw suffice. Verdict
  only; adds no code, no schema, no reference surface.
use_when:
  - Checking whether the IG reels projection<->ECR keys-vs-handle fork was resolved and how.
  - Confirming that no projection field was merged into an ECR integrity posture field.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/ig_reels_projection_to_ecr_consumption_handoff_v0.md
  - docs/workflows/ecr_spine_submap_v0.md
  - forseti-harness/source_capture/ig_reels_grid_projection.py
  - forseti-harness/ecr/
stale_if:
  - A new named ECR/SCR consumer must point at the reconciled source-surface disagreement view (re-open Option 2).
  - The IG reels projection row contract (row_id / raw_ref / join_status) changes shape.
  - ECR/SCR carry-or-residualize, reference-never-merge, or one-record-per-kind discipline changes.
  - The owner revives SCR as a default pre-Judgment layer.
```

## Decision

**Option 1 — packet_id/slice_id keys suffice. No reference handle added; no code changed.**

The IG reels-grid projection row is a keyed sibling over the same raw the ECR
integrity postures already key to. Every existing ECR/SCR consumer reaches raw by
`packet_id` (and `slice_id` for per-slice postures); the projection row carries those
same keys. No consumer reads a projection output, and none requires the reconciled
cross-surface metric view. A by-key reference (Option 2) would add a durable reference
field with no consumer that needs it -- speculative lock-in, declined. Option 2 remains
available, by key/reference only, if a future named consumer must point at the
reconciled source-surface disagreement view specifically.

This record changes nothing in code. It satisfies the handoff's success-signal (a):
"confirms packet_id/slice_id keys already suffice and records that."

## Evidence (confirm-don't-trust, read 2026-06-25 from the codex checkout)

Workspace: `C:\Users\vmon7\Desktop\projects\orca`, branch `codex/ig-reels-capture-spine`,
HEAD `056ef74b` (advanced past the authoring head `4162f6e2`; `4162f6e2` confirmed an
ancestor of HEAD). Doctrine compare-targets re-verified by SHA256 against the handoff's
ledger and all matched: ECR submap `B1F2BD6D...`, projection doctrine `BE22FD65...`,
Data/Cleaning boundary `3D50EEA8...`, upstream split packet `2ED2A581...`. The adapter
file is in working-tree flux (`M`) as the handoff warned; it was reread live rather than
trusting a pinned working-tree hash.

Projection row handle (`orca-harness/source_capture/ig_reels_grid_projection.py`):
- `IgReelsGridProjectionRow.raw_ref = IgProjectionRawRef{packet_id, slice_id}`;
  `row_id = "{packet_id}:{slice_id}:{metric}"`; `raw_anchor` carries
  `{file_id, relative_packet_path, sha256, hash_basis, json_pointer}`.
- Enrichment carried for the cross-surface disagreement: `chosen_source_surface`,
  `source_surface_count_candidates[]`, `join_status`
  (`joined_by_shortcode | missing_json | missing_shortcode | ambiguous | not_applicable`),
  `selection_policy_version`, `selection_limitations`, `source_visible_fields`
  (Judgment-field-name guarded), `residuals`. Certification:
  `view_only; not_cleaned; not_normalized; not_judgment_ready`.

ECR consumers (`orca-harness/ecr/`):
- `deriver.py`: all four derivers (`derive_timing_postures` SP-3, `derive_inspectability_postures`
  SP-2, `derive_identity_postures` SP-1, `derive_source_visibility_postures` SP-6) take
  `SourceCapturePacket` as their sole input and read only raw producer fields
  (`timing.cutoff_posture`, `preserved_file_ids` + `PreservedFile.sha256`, `source_locator`,
  `source_family`/`source_surface`/`source_locator`, `archive_history_posture`). None reads a
  projection output.
- `models.py`: postures key by `slice_id` (SP-2/SP-3) or `packet_id` (SP-1/SP-6).
- `lake.py`: `derive_ecr_into_lake` loads the raw packet **by `packet_id`** and appends
  derived records at `derived/<packet_id>/ecr_<kind>/<record_id>.json` -- keyed by the raw
  anchor, the same key the projection row carries.

SCR consumer (`orca-harness/signal_content/`, deprecated/dormant per PR #375):
- `deriver.py` `derive_signal_content` takes `packet` + caller-supplied `preserved_bodies`
  (raw body text), not projection; `ContentReferences` (`models.py`) references provenance and
  integrity **by key** (`packet_id`, `slice_id`, `ecr_posture_ref_ids`), never embedded. Its own
  docstring: "the content<->integrity link is already carried by the shared `packet_id` / `slice_id`."
- Drift Guard forbids reviving SCR to consume projection; the default route is evidence pack ->
  Judgment-authored interpretation. No SCR change.

Doctrine basis: projection and ECR are keyed siblings over raw, neither owns the other
(projection doctrine OD-1); ECR references by key and never merges (ECR submap invariants 1, 3).

## Not done / boundaries held

- No projection field (`source_surface_count_candidates`, `chosen_source_surface`,
  `selection_*`, `source_visible_fields`) copied into any SP-1/2/3/6 posture field.
- No by-key reference field added to any ECR/SCR record.
- No new derived-record kind; no SCR revival; no EvidenceUnit binding; no JSG-01 run.
- No ad/sponsorship/demand/credibility/integrity/Decision-Strength/Action-Ceiling conclusion
  authored anywhere.
- Hard-blocker check (handoff Action 4): no consumer would require merging a projection field
  into a posture field -- none reads projection at all -- so no Drift-Guard stop was triggered.

## Validation

Doc-only decision; no code touched, so the IG projection / ECR test suites are unchanged and
were not re-run for this record (last green at 41 passed, 2026-06-25, per the handoff). Local
check: `git -C C:/Users/vmon7/Desktop/projects/orca diff --check`.

## Landing

This record is written untracked in the `codex/ig-reels-capture-spine` checkout (the lane's
workspace per the handoff). Landing it is the codex lane's call via ordinary `git add` on that
lane, alongside the lane's other uncommitted work; this record neither stages nor commits.

## Non-claims

Not validation, readiness, ratification, an EvidenceUnit binding, a JSG-01 unfreeze, Cleaning
or Judgment design, or buyer proof. It records one bounded structural decision (keys suffice)
backed by the reads above; the projection remains `view_only` and raw stays canonical.
