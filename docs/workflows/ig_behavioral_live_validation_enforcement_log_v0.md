# IG Behavioral Live Validation Enforcement Log v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow operational record and proposed enforcement log
scope: >
  Records the 2026-06-29 IG deep-capture live validation lesson, the grid-first
  lane correction, and proposed code-vs-doctrine enforcement cells for future
  IG behavioral parity work.
use_when:
  - Planning or reviewing IG behavioral live validation after the deep-capture e2e pass.
  - Deciding whether an IG run can claim full behavioral completeness or only a subpath result.
  - Scoping the next data-lake record-linkage patch for IG deep capture and product extraction.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca-harness/runners/run_source_capture_ig_reels_grid_packet.py
  - orca-harness/runners/run_source_capture_ig_reels_deep_capture.py
stale_if:
  - IG grid capture, deep-capture, product-extraction, or behavioral-projection record contracts change.
  - A later accepted doctrine artifact binds a different IG live-validation sequence.
  - Data-lake bronze/silver record semantics are renamed or materially redefined.
```

## Purpose

This artifact records a live validation lesson, not a completed doctrine change,
readiness claim, or code patch.

On 2026-06-29, a canonical `F:\orca-data-lake` live run proved the IG
deep-capture subpath for one shortcode, but it did not prove the full grid-first
IG behavioral lane. Future agents should not describe that run as full IG
behavioral completeness.

## Observed Live Result

Canonical data-lake root: `F:\orca-data-lake`.

Shortcode: `DZ69knlsDb1`.

Creator identity source: the IG audio recipe card in the active implementation
worktree identifies `DZ69knlsDb1` as a Jeremy Fragrance reel. The persisted lake
record is currently keyed by shortcode and does not itself carry creator handle.

Fresh readback observed these persisted records under
`F:\orca-data-lake\derived\85a\DZ69knlsDb1\`:

| Lane | Record | Observed result |
| --- | --- | --- |
| `silver__capture__reel_transcript` | `deepcap_DZ69knlsDb1__c36f2b3a8593280e.json` | `transcript_posture=render_unavailable`; `audio_handle_used=false`; `cues=0` |
| `silver__capture__reel_transcript` | `deepcap_DZ69knlsDb1__c746f8a6352b0df8.json` | `transcript_posture=transcribed`; `audio_handle_used=true`; `cues=17` |
| `silver__capture__audience_comments` | `deepcap_DZ69knlsDb1__c746f8a6352b0df8.json` | `comments=15` |
| `silver__cleaning__product_mentions` | `mentions_codex-extraction-v0__0c9b35e92359d7f4.json` | `mention_count=0`; `rejected_count=0` |

The zero product mentions are correct for the observed transcript: the speech
names brands/status language, not specific fragrance product lines. Product
extraction must not invent product-line mentions from brand-only transcript
text.

## Lane Correction

The correct IG behavioral lane shape is grid-first:

1. Run the public IG `/reels/` grid capture for the creator.
2. Select shortcodes from the grid output.
3. Run deep capture on selected shortcodes for detailed audience comments and
   audio-derived transcript.
4. Run product extraction and behavioral projection over persisted lake records.

The live run that produced the records above skipped step 1 and went directly
to a known shortcode. That is valid only as a narrow deep-capture subpath test.
It does not clear the `ig_grid_candidate_absent` residual and must not be used
as full behavioral-completeness proof.

## Proposed Code-Enforced Mechanics

These should be enforced in code because they are deterministic record-shape or
projection-honesty properties.

1. Grid absence remains a residual.
   Projection must not report full IG behavioral completeness when a shortcode
   has deep-capture records but no associated grid packet or grid-row source.

2. Deep-capture records carry source linkage.
   Persisted deep-capture silver records should carry enough provenance to link
   a reel back to the creator/grid context when available: creator handle or
   profile identity, grid packet id, grid row id or slice id, shortcode, and
   render attempt/record id.

3. Product mention records carry exact transcript source identity.
   Product extraction should not key only by shortcode. It should carry the
   transcript record id/source key it consumed, so multiple transcript records
   for the same shortcode do not become ambiguous.

4. Failed render receipts remain visible.
   A later successful deep-capture record must not overwrite, hide, or collapse
   earlier failed records. Projection may select the successful record as
   canonical, but the failed source remains a residual/source problem.

5. Grid comment count and detailed comments stay separate.
   Grid capture may carry comment counts. Deep capture carries audience comment
   text/detail. Projection and downstream consumers must not treat a count as
   comment-detail coverage.

6. Audio handles remain transient by default.
   The signed media handle can be used for immediate transcription, but raw
   media bytes should not be persisted unless explicitly authorized by a later
   source-access/data-retention decision.

## Proposed Doctrine-Enforced Operating Rules

These belong in doctrine or playbook language because they govern run sequencing
and claim discipline rather than one local schema invariant.

1. IG live behavioral validation is grid-first by default.
   Direct shortcode deep-capture is allowed only when explicitly labeled as a
   subpath test or targeted repair.

2. Behavioral parity with YouTube means coverage parity, not identical capture
   mechanics.
   IG can use IG-native grid/deep-capture mechanics while matching the behavioral
   completeness contract.

3. A render failure is not a final NO-GO by itself.
   If a bounded re-probe tests a different route fact or changed environment,
   rerun at human-rate and preserve both the failure and success receipts.

4. Product extraction remains conservative.
   Brand-only transcript speech is not enough to create product-line mentions.
   Preserve zero-mention outputs when that is the honest extraction result.

5. Do not convert subpath success into readiness language.
   Deep-capture success proves audio/comments/transcript for the tested reel.
   Full IG behavioral completeness still requires grid-source linkage and all
   required projection residuals cleared or explicitly accepted.

## Patch Queue

No patch is implemented by this artifact.

Likely next implementation work:

1. Silver-lane provenance patch: add exact source linkage to deep-capture and
   product-mention silver records.
2. Projection patch: consume those links so multiple records for the same
   shortcode remain disambiguated.
3. Doctrine/playbook patch: make the grid-first IG live-validation sequence
   explicit, while allowing clearly labeled direct-shortcode subpath tests.

Bronze/raw packet linkage may be needed for full grid packet admission and row
references, but the immediate ambiguity found in this run is in the silver
derived records.

## Non-Claims

- Not validation or readiness.
- Not a full IG behavioral-completeness proof.
- Not a doctrine change.
- Not a data-lake schema patch.
- Not authorization to persist raw media bytes.
- Not a claim that Instagram render behavior is stable.
