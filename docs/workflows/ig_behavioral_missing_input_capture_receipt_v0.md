# IG Behavioral Missing-Input Capture And Extraction Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow receipt
scope: Bounded Instagram behavioral residual burn-down for grid-backed items missing comments/transcript, followed by scoped operator product extraction for behavior-visible eligible transcripts.
use_when:
  - Checking what changed after the IG behavioral missing-input burn-down pass.
  - Deciding whether the next blocker is status semantics, no-speech/no-audio handling, grid absence, or stale failed sources.
  - Verifying that this run stayed out of shared-core, scheduler, media-preservation, historical rewrite, and gold/Judgment work.
open_next:
  - docs/workflows/ig_behavioral_residual_burndown_priority_v0.md
  - docs/workflows/ig_canonical_f_deep_capture_product_extraction_receipt_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca-harness/runners/run_source_capture_ig_reels_deep_capture.py
  - orca-harness/runners/run_ig_reels_operator_product_extract.py
  - orca-harness/source_capture/ig_reels_behavioral_lake.py
  - orca-harness/source_capture/ig_reels_behavioral_projection.py
stale_if:
  - A later F-lake residual inventory supersedes the post-run counts below.
  - The IG deep-capture runner, operator extraction runner, behavioral lake adapter, or behavioral projection semantics change.
  - The remaining no-speech/no-audio/render-unavailable/grid-missing items are recaptured or reclassified.
authority_boundary: retrieval_only
```

## Short Answer

The missing-input pass worked, and the follow-on extraction pass cleared every behavior-visible
`not_attempted` extraction residual.

Final observed state after the run: 19 IG behavioral items, 12 complete, 2 complete with residuals,
and 5 with no extraction-eligible source. Before this run, only 2 were complete and 12 had no
extraction-eligible source.

This did not need more lineage work. It did not need shared IG/YT core, scheduler work, durable media
preservation, historical lake rewrite, or gold/Judgment changes.

## Scope And Guard

- Access classification: public Instagram Reel pages under the owner-authorized pre-commercial,
  human-rate public-content posture in the capture playbook.
- Capture route used: rendered reel deep-capture, one render per shortcode, transient media handle
  used immediately for ASR and not persisted.
- Extraction route used: operator-assisted strict JSON packet/import through
  `run_ig_reels_operator_product_extract.py`; imports were validated by the existing parser/writer.
- Volume: eight explicitly named missing-input shortcodes for capture; ten behavior-visible eligible
  transcripts for operator product extraction.
- Not used: login, proxy, scheduler, shared IG/YT core, durable media/video preservation, historical
  lake rewrite, gold/Judgment behavior.

## Target Derivation

The capture targets were derived from the current behavioral index, not copied from memory:

```text
targets=DC9vnmgJWPf,DF3CdyJv79A,DaINMZCCb6N,DaKd8E9skt8,DaKkXGQBE9i,DaKkwCiB_2B,DaLBhRbskFa,DaLK8b9s9z9
count=8
```

Selection rule: `candidate` present, plus both residuals
`ig_comments_not_attempted:<shortcode>` and `ig_transcript_source_absent:<shortcode>`.

After those captures, seven of the eight were extraction-eligible. `DaKkwCiB_2B` had comments plus
`no_speech`, so it was intentionally not sent to product extraction.

A second product-extraction sweep then handled the three remaining behavior-visible `not_attempted`
items already present in the lake: `DaGUhsKsYL9`, `DaH3L1Isdrc`, and `DaIr5aRsp8p`.

## Capture Results

Command shape:

```powershell
python runners\run_source_capture_ig_reels_deep_capture.py --shortcode <shortcode> --model tiny --data-root F:\orca-data-lake
```

Observed writes:

```text
DC9vnmgJWPf: comments=11 transcript_posture=transcribed transcript_cues=26 audio_handle=used
  persisted: deepcap_DC9vnmgJWPf__344e76e8245466a6.json
DF3CdyJv79A: comments=15 transcript_posture=transcribed transcript_cues=17 audio_handle=used
  persisted: deepcap_DF3CdyJv79A__808278ecd3ba53f6.json
DaINMZCCb6N: comments=4 transcript_posture=transcribed transcript_cues=28 audio_handle=used
  persisted: deepcap_DaINMZCCb6N__d59924bcd2f630fd.json
DaKd8E9skt8: comments=0 transcript_posture=transcribed transcript_cues=13 audio_handle=used
  persisted: deepcap_DaKd8E9skt8__1d4b7b46e33bb07a.json
DaKkXGQBE9i: comments=3 transcript_posture=transcribed transcript_cues=9 audio_handle=used
  persisted: deepcap_DaKkXGQBE9i__487c6570b1a27bdd.json
DaKkwCiB_2B: comments=3 transcript_posture=no_speech transcript_cues=0 audio_handle=used
  persisted: deepcap_DaKkwCiB_2B__eb9329d85714d582.json
DaLBhRbskFa: comments=4 transcript_posture=transcribed transcript_cues=3 audio_handle=used
  persisted: deepcap_DaLBhRbskFa__20698e91aef761fb.json
DaLK8b9s9z9: comments=9 transcript_posture=transcribed transcript_cues=9 audio_handle=used
  persisted: deepcap_DaLK8b9s9z9__c466a2ebd70a2cb6.json
```

## Operator Extraction Results

Seven newly eligible transcripts were imported first:

```text
DC9vnmgJWPf: extracted, mention_count=9, rejected_count=0
DF3CdyJv79A: extracted, mention_count=5, rejected_count=0
DaINMZCCb6N: extracted, mention_count=0, rejected_count=0
DaKd8E9skt8: extracted, mention_count=1, rejected_count=0
DaKkXGQBE9i: extracted, mention_count=0, rejected_count=0
DaLBhRbskFa: extracted, mention_count=1, rejected_count=0
DaLK8b9s9z9: extracted, mention_count=1, rejected_count=0
```

Then the three remaining behavior-visible `not_attempted` transcripts were imported:

```text
DaGUhsKsYL9: extracted, mention_count=1, rejected_count=0
DaH3L1Isdrc: extracted, mention_count=10, rejected_count=0
DaIr5aRsp8p: extracted, mention_count=0, rejected_count=0
```

The operator responses were conservative: unclear transcripts were imported as `[]` instead of
forced mentions. Every import went through quote validation and returned `rejected_count=0`.

## Final Behavioral Read

Fresh read of `F:\orca-data-lake` through `project_ig_reels_behavioral_index_from_lake` after all
imports:

```text
pending_default_model
1
partials_default_model
0
items=19
statuses
  complete: 12
  complete_with_residuals: 2
  no_extraction_eligible_sources: 5
residual_prefixes
  ig_grid_candidate_absent: 4
  ig_transcript_source_not_extraction_eligible: 3
  ig_transcript_source_render_unavailable: 2
  ig_comments_render_unavailable: 1
  ig_transcript_source_no_audio_handle: 1
```

The remaining default-model pending candidate is `DaLBRQiMJhQ`; it is already behavior-complete via
an earlier source-backed `codex-operator-assisted-v0` extraction record, so this run did not create a
duplicate `codex-extraction-v0` record for it.

Remaining non-complete items:

```text
DZ69knlsDb1: complete_with_residuals; grid absent plus one older render-unavailable transcript source, but one extracted source is complete.
DaA8n7EhqTR: complete_with_residuals; extraction complete, grid absent.
DaK3uKxBlKy: no_extraction_eligible_sources; comments captured, transcript posture no_speech.
DaK3va8MYT_: no_extraction_eligible_sources; grid absent, comments render_unavailable, transcript render_unavailable.
DaKeK7vMoR0: no_extraction_eligible_sources; grid absent, no_audio_handle.
DaKeXcVM0sx: no_extraction_eligible_sources; comments captured, transcript posture no_speech.
DaKkwCiB_2B: no_extraction_eligible_sources; comments captured, transcript posture no_speech.
```

## Next Move

Stop treating extraction as the main blocker. The next decision is how IG should report items that
have complete extraction but lack grid/ranking context, or have comments but no speech-bearing
creator transcript.

The highest-value narrow follow-up is a status-semantics patch or decision for:

1. extraction-complete but grid-missing items (`DaA8n7EhqTR`, plus part of `DZ69knlsDb1`);
2. stale failed source handling when a newer source for the same shortcode is complete (`DZ69knlsDb1`);
3. no-speech/no-audio records that have audience comments but no creator transcript source eligible
   for product extraction.

## Non-Claims

- Not proof that every public IG Reel yields comments, audio, transcript, or extraction.
- Not durable media/video preservation.
- Not logged-in, proxy, private-account, scheduler, shared-core, historical rewrite, or gold/Judgment
  work.
- Not validation of full IG lane readiness.
