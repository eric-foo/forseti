# IG Back-Fix Against YouTube Behavioral Contract Spec v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow spec
scope: >
  Planning-only step-3 spec for back-fixing Instagram Reels against the reviewed
  YouTube-first behavioral contract without copying YouTube acquisition,
  transcript priority, packet anchors, or runner shape.
use_when:
  - Scoping the IG back-fix after the YouTube-first behavioral completion spec.
  - Checking which IG surfaces must normalize before shared contract extraction.
  - Preventing IG from being forced into YouTube machinery while preserving behavioral parity.
authority_boundary: retrieval_only
branch_or_commit: codex/unify-capture-core-planning @ b6d87c23 before this artifact was authored; source basis origin/main @ ba9b36b5 with no orca-harness diff on this branch
open_next:
  - docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md
  - docs/workflows/youtube_first_behavioral_completion_spec_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/youtube_first_behavioral_completion_spec_review_adjudication_v0.md
  - orca-harness/source_capture/ig_reels_grid.py
  - orca-harness/source_capture/ig_reels_grid_capture.py
  - orca-harness/runners/run_source_capture_ig_reels_grid_packet.py
  - orca-harness/source_capture/ig_reels_deep_capture.py
  - orca-harness/source_capture/ig_reels_deep_capture_lake.py
  - orca-harness/source_capture/transcript/ig_reels_audio_packet.py
  - orca-harness/runners/run_ig_reels_product_extract.py
  - orca-harness/runners/run_transcript_product_extract.py
  - orca-harness/cleaning/transcript_product_extractor.py
  - orca-harness/cleaning/transcript_product_lake.py
stale_if:
  - docs/workflows/youtube_first_behavioral_completion_spec_v0.md changes materially.
  - Any named IG grid, deep-capture, audio packet, or extraction source changes.
  - The owner chooses a route other than YouTube-first behavioral reference followed by IG back-fix.
```

## Status

Target: `IG_BACKFIX_BEHAVIORAL_SPEC_READY`.

This spec is planning-only. It does not authorize source edits, runtime capture,
network access, persistence migration, shared machinery, production readiness, or
TikTok coverage. It also does not claim the YouTube runtime lane is already
implemented. It uses the patched YouTube behavioral spec as the reference
contract for a future IG scoping pass. Reviewed/adjudicated here means
pre-patch review plus post-review adjudication; the patched YouTube spec has not
been adversarially re-reviewed.

## Source Basis

Fresh read facts used here:

- The harness source files under `orca-harness/` have no diff from
  `ba9b36b5..HEAD` on this branch.
- IG grid capture writes a SourceCapturePacket with DOM rows, passive JSON
  candidates, metric observations, limitations, and receipt metadata.
- IG deep capture performs one rendered reel pass that yields comments plus a
  transient media handle; the transient handle is used immediately for ASR and
  must not be persisted.
- IG deep-capture persistence writes a shortcode-anchored derived record set
  containing audience comments and reel transcript members with a completion
  marker.
- IG standalone audio capture writes a `source_family=instagram_creator`,
  `source_surface=ig_reels_audio` SourceCapturePacket and appends a
  `transcript_asr` derived record anchored by packet id.
- IG product extraction currently reads only `ig_reels_audio` packets; grid
  packets are skipped and deep-capture transcript records are not currently a
  shared extraction feed.
- The shared transcript product extractor consumes only
  `TranscriptInput(video_id, transcript_anchor, transcript_source, cues)` and
  writes product mentions under the transcript anchor with a completion marker.

## Back-Fix Principle

Back-fix IG behavior, not IG mechanics.

Keep IG-owned:

- browser-rendered creator grid acquisition;
- DOM/passive JSON candidate merge;
- engagement/view ranking basis;
- rendered reel deep capture;
- transient signed media-handle handling and redaction;
- ASR-only transcript reality;
- shortcode as the platform item identity;
- source-specific runners and operator controls.

Normalize only the observable contract surface needed for IG and YouTube to be
comparable:

- candidate identity and ranking basis;
- comments posture;
- transcript source, posture, cues, and provenance;
- run receipt and partial/failure states;
- deterministic persistence correlation;
- extraction-feed compatibility.

## IG Behavioral Contracts

### IGBehavioralCandidateRow

An IG behavioral candidate row should carry, when observed:

- `platform`: `instagram`;
- `platform_item_id`: the reel shortcode;
- `platform_item_id_kind`: `shortcode`;
- `canonical_url`, normally `https://www.instagram.com/reel/<shortcode>/`;
- creator handle/profile locator when observed;
- source surface: grid row, deep-capture reel, or standalone audio packet;
- ranking basis: e.g. `views_then_engagement`, `engagement`,
  `comments_only_likes_hidden`, `unknown_or_weak`, or a narrower compatible enum;
- source metric observations and limitations, including hidden or missing
  engagement signals;
- comment posture and comment source route when deep capture has run;
- transcript availability and transcript source selection when ASR has run;
- persistence anchors for every observed grid, deep-capture, audio, transcript,
  and extraction surface;
- route receipt fields: capture time, access posture, wall/block posture,
  artifact hashes or packet ids where available, and limitations.

### IGCommentSet

IG comments should normalize to the shared comment posture without changing the
underlying route:

- `captured`: one or more parsed comment nodes from the rendered DOM;
- `empty`: the route completed and no comments were observed;
- `render_unavailable`: no rendered DOM was available;
- `parse_failed`: rendered DOM existed but comment parsing failed;
- `blocked`: access wall or platform block was detected;
- `not_attempted`: comment capture was outside this run.

Captured comments keep observed author/display identity, comment id when present,
text, like count, reply or thread signals when present, and source route. The
contract does not require full corpus exhaustiveness.

### IGTranscriptSource

IG has ASR-only transcript reality today. A future back-fix must express both
transcript-bearing IG surfaces as `TranscriptSourceRecord` candidates or explicitly
name one as a non-canonical residual with deterministic lookup.

Required fields:

- `platform`: `instagram`;
- `platform_item_id`: shortcode;
- `platform_item_id_kind`: `shortcode`;
- `source_kind`: `asr`;
- `source_route`: `deep_capture_render_audio | standalone_audio_packet`;
- raw or derived anchor:
  - deep capture: shortcode plus deep-capture record id or record-set anchor;
  - standalone audio: audio packet id plus `transcript_asr` record id;
- cue list with millisecond timing;
- posture: `transcribed | no_speech | failed | render_unavailable | no_audio_handle | download_failed`
  or a narrower compatible enum;
- provenance: ASR tool/model metadata when available, source packet id or
  deep-capture record id, source file id/sha when available, retrieval time, and
  limitations;
- transient media policy: signed media URLs are never durable evidence; keep only
  redacted provenance such as handle-used and media host when present.

Default canonical transcript selection for scoping:

1. Prefer a successful deep-capture ASR transcript when the behavioral record is
   using the same deep-capture comment set, because comments and transcript came
   from one rendered reel pass.
2. Otherwise prefer the latest successful standalone audio-packet ASR transcript.
3. Preserve every observed transcript source and record the selection reason.
4. A later implementation spec may replace this order only with a stronger
   quality rule that keeps source route and correlation explicit.

### IGRunReceipt

Every IG run must preserve visible failure and partial success. It must state:

- route used: grid, deep capture, standalone audio, extraction, or bridge/index;
- item count attempted and item count captured;
- block/wall/render posture;
- per-item status, including partial states such as comments captured but
  transcript unavailable;
- artifacts produced and artifacts intentionally not produced;
- transient media redaction state;
- non-authoritative fields, estimates, and hidden or weak metric limitations;
- whether extraction was skipped, complete, failed, or partially written.

### IGPersistenceCorrelation

The video-level YouTube key maps to IG as a platform item key:
`platform_item_id = platform_shortcode`.

Correlation must represent one shortcode to many anchors:

- grid SourceCapturePacket(s) and joined row(s);
- deep-capture record set(s) anchored by shortcode;
- standalone audio SourceCapturePacket(s);
- ASR derived transcript record(s);
- product-extraction record set(s);
- comment set(s) and run receipt(s).

The future implementation may choose a bridge record, index, or adapter over
existing lake paths. It must not leave these surfaces discoverable only by human
convention. It must also avoid pretending that shortcode anchoring, packet-id
anchoring, and record-set anchoring are the same physical shape.

Completion semantics may remain source-specific. The requirement is that a
future reader can determine whether the transcript/comment/extraction unit is
complete, failed, skipped, or partial without parsing stdout. A single append-only
record may be acceptable only if the implementation spec explains why that record
is the complete unit; otherwise a record-set completion marker or equivalent
index is required.

### IGExtractionFeed

IG is behaviorally complete only when transcript sources that are allowed to
feed product extraction are visible through the normalized extraction feed.

Minimum closure:

- standalone audio-packet ASR continues to feed the existing shared extractor;
- deep-capture transcript records are either adapted into `TranscriptSourceRecord` and
  eligible for extraction, or named as a non-canonical residual with deterministic
  lookup and no hidden extraction-complete claim;
- extraction remains downstream of capture; no LLM/model calls move into capture;
- extraction records keep transcript anchor, source route, model/rubric
  provenance, rejected quote evidence, and completion state.

Extraction completion is per transcript-source anchor, not inherently per item.
The behavioral record must expose `source_extraction_statuses` keyed by
transcript anchor plus a per-item rollup. The rollup may read `complete` only
when every extraction-eligible observed transcript source for that item is
`extracted` or `skipped_done`, or is explicitly residualized or marked
`not_extraction_eligible` with a reason. If a future implementation wants
canonical-only completion, it must name that field `canonical_extraction_status`
and keep non-canonical source statuses visible.

## Sequencing

A disciplined IG back-fix should sequence like this:

1. Bind identity: introduce the contract-level `platform_item_id` alias for IG
   shortcode without renaming every runtime field first.
2. Normalize candidate rows: project grid candidate/ranking/metric limitations
   into `IGBehavioralCandidateRow`.
3. Normalize comments: express deep-capture comment outcomes as `IGCommentSet`
   postures.
4. Normalize transcript sources: expose standalone audio and deep-capture ASR as
   `IGTranscriptSource` candidates or explicitly residualize one with deterministic
   lookup.
5. Bind correlation: create or scope a deterministic lookup from shortcode to
   grid, comments, transcript, and extraction anchors.
6. Bind extraction feed: ensure canonical transcript selection can reach product
   extraction status and record-set anchors.
7. Only after these contracts are reviewed, decide whether any source-changing
   migration is warranted.

## Acceptance Criteria

Implementation scoping may treat the IG back-fix as ready only if it can make the
following testable:

1. A reel has one behavioral record keyed by `platform_item_id` / shortcode that
   ties candidate identity, ranking basis, comments posture, transcript source
   selection, persistence anchors, canonical extraction status, per-source
   extraction statuses, and per-item extraction rollup together.
2. IG grid ranking and metric limitations are explicit; hidden likes or weak
   engagement cannot silently pass as strong ranking evidence.
3. Deep-capture comments can be represented as a comment set with a posture and
   route receipt.
4. Both IG transcript-bearing surfaces are either normalized to `TranscriptSourceRecord`
   candidates or one is explicitly residualized with deterministic lookup and no
   hidden completeness claim.
5. Canonical transcript selection preserves all observed sources and records the
   selection reason.
6. Correlation from shortcode to grid/deep-capture/audio/transcript/extraction
   anchors resolves programmatically; manual convention is not acceptable.
7. Transient media URLs remain non-durable; only redacted provenance may persist.
8. Extraction remains downstream and source-family agnostic; no LLM/model import
   moves into capture.
9. Per-item `extraction_status` cannot read complete while any
   extraction-eligible observed transcript source is unextracted, failed, or
   partial unless that source is explicitly residualized or marked
   `not_extraction_eligible` with reason; canonical-only status uses a separate
   field name.
10. No implementation claims YouTube acquisition shape, caption priority, shared
   runner/framework, production readiness, live-scale validation, or TikTok coverage.

## MGT Accepted Residuals

- IG transcript is ASR-only in v0. Acceptable because the contract names
  `source_kind=asr`; revisit only if an IG caption or transcript surface becomes
  source-backed.
- IG may keep shortcode-anchored deep-capture record sets while audio packets use
  packet ids. Acceptable if deterministic correlation resolves both; upgrade only
  if lookup errors or duplicate canonical transcript selection appear.
- Deep-capture transcript extraction may be a scoped implementation residual if
  standalone audio already covers the canonical transcript. Acceptable only when
  the residual is named and discoverable; not acceptable as silent omission.
  Upgrade when canonical selection depends on same-render comment/transcript
  provenance or when product extraction needs deep-capture transcript evidence.
- Grid and deep-capture runners may remain separate. Acceptable because runner
  consolidation is higher lock-in than behavioral contract parity; upgrade only
  if separate runners produce inconsistent receipts, correlation, or extraction
  completion visibility.
- The patched YouTube behavioral spec has not been adversarially re-reviewed
  after its adjudication patch. Acceptable for planning only; before source-
  changing IG parity or shared-core extraction uses it as implementation
  authority, either run a post-patch YouTube re-review or record explicit owner
  acceptance of that dependency.

## Review Checkpoint

Adversarial artifact review should happen after this spec and the shared
contract extraction spec are authored and before any IG back-fix implementation
uses them as authority.

Highest value checkpoint: `after_artifact_pre_implementation`.

Review target: this spec, the shared contract extraction spec, the parent
planning note, the reviewed/adjudicated YouTube behavioral spec, and the named
IG/YT source files.