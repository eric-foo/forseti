# IG Behavioral Residual Burn-Down Priority v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Priority record for the next Instagram behavioral residual burn-down step after the read-side Silver lineage gate.
use_when:
  - Deciding what IG behavioral residual to work next.
  - Checking why source-backed lineage is no longer the main blocker.
  - Preparing a bounded follow-up lane for IG behavioral parity without changing capture mechanics.
open_next:
  - docs/workflows/ig_vs_youtube_behavioral_gap_ledger_v0.md
  - docs/workflows/ig_canonical_f_deep_capture_product_extraction_receipt_v0.md
  - orca-harness/source_capture/ig_reels_behavioral_lake.py
  - orca-harness/source_capture/ig_reels_behavioral_projection.py
stale_if:
  - A later IG behavioral residual inventory supersedes the F-lake read below.
  - IG behavioral lake/projection code changes residual or completeness semantics.
  - A later owner-authorized capture or backfill lane changes the F-lake residual mix.
authority_boundary: retrieval_only
```

## Short Answer

The next big step is **not more lineage work**. The read-side lineage gate is in place.

The next useful target is **missing input coverage**: many IG items have grid rows but no comments
or transcript source, so they cannot become behaviorally complete no matter how good the lineage
gate is.

Do not jump straight to shared IG/YT core, scheduler work, media preservation, gold/Judgment, or a
historical lake rewrite.

## Fresh Read

Observed on branch `codex/ig-behavioral-residual-burndown` from `origin/main` at
`aa7b45d9` by reading `F:\orca-data-lake` with
`project_ig_reels_behavioral_index_from_lake`.

```text
items=19
complete: 2
complete_with_residuals: 2
no_extraction_eligible_sources: 12
not_attempted: 3

top residual prefixes:
ig_comments_not_attempted: 8
ig_transcript_source_absent: 8
ig_grid_candidate_absent: 4
ig_transcript_source_not_extraction_eligible: 3
ig_transcript_source_render_unavailable: 2
ig_comments_render_unavailable: 1
ig_transcript_source_no_audio_handle: 1
```

Examples that matter:

```text
DaA8n7EhqTR: complete_with_residuals: grid candidate absent
DZ69knlsDb1: complete_with_residuals: grid candidate absent plus older render_unavailable transcript residual
DaKeK7vMoR0: no_extraction_eligible_sources: grid absent plus no_audio_handle
Eight grid-only items: comments not attempted plus transcript source absent
```

## Priority

1. **First: input coverage for grid-only items.**
   Eight items already appear in the behavioral index but have no comments and no transcript source.
   The likely gain is largest here. This needs an owner-authorized low-interaction capture run or
   an explicit decision to leave those items as missing-source residuals.

2. **Second: direct deep-capture items with missing grid.**
   `DaA8n7EhqTR` has source-backed extraction but still fails overall behavioral completeness because
   it has no grid candidate row. Do not silently mark it complete. First decide whether grid/ranking is
   required for the one overall behavioral-complete flag, or whether extraction completeness should be
   reported separately from ranking/candidate completeness.

3. **Third: stale or duplicate failed sources under a shortcode.**
   `DZ69knlsDb1` shows a successful extraction path but still carries an older failed/render-unavailable
   transcript residual. This may need better source selection or stale-source handling, but patching it
   before the status split above risks hiding real failed sources.

4. **Later: old no-lineage records.**
   They are already blocked by the read-side lineage gate. Backfill or re-extraction is a separate
   owner-authorized lane, not part of this residual burn-down by default.

## Next Allowed Move

Prepare a bounded follow-up lane that does one of these, in this order:

1. If live local capture is authorized: run a low-interaction deep-capture pass for the eight
   grid-only items and re-read the behavioral index.
2. If live capture is not authorized: patch nothing yet; write the status-split decision for
   "extraction complete but grid missing" before changing code.

## Non-Claims

- Not validation of the full IG lane.
- Not proof that every public IG Reel yields comments, audio, transcript, or product extraction.
- Not live capture authorization.
- Not a shared IG/YT capture-core decision.
- Not scheduler, media-preservation, gold/Judgment, or historical lake rewrite work.
