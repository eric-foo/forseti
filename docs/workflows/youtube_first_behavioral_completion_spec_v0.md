# YouTube-First Behavioral Capture Completion Spec v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow plan
scope: >
  Implementation-facing behavioral contract for making the YouTube capture lane
  the first complete behavioral lane before back-fixing Instagram Reels and
  extracting shared capture-core contracts. This is a spec for behavior parity,
  not machinery parity.
use_when:
  - Scoping the next YouTube-only behavioral completion pass after PR #417.
  - Checking what YouTube must emit before IG is back-fixed against it.
  - Preventing a shared capture core implementation from forcing common acquisition machinery.
authority_boundary: retrieval_only
branch_or_commit: codex/unify-capture-core-planning @ 55b2443a before this artifact was authored; source basis origin/main @ ba9b36b5
open_next:
  - docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md
  - orca-harness/youtube_capture/capture_youtube_v0.py
  - orca-harness/youtube_capture/shorts_scroll_capture_v0.py
  - orca-harness/source_capture/transcript/youtube_captions.py
  - orca-harness/source_capture/transcript/caption_packet.py
  - orca-harness/source_capture/transcript/asr_packet.py
  - orca-harness/runners/run_transcript_product_extract.py
  - orca-harness/source_capture/ig_reels_grid.py
  - orca-harness/source_capture/ig_reels_deep_capture.py
  - orca-harness/source_capture/ig_reels_deep_capture_lake.py
stale_if:
  - Any named YouTube capture, transcript, persistence, or extraction source changes.
  - Any named IG grid or deep-capture source changes in a way that changes the comparison prompt.
  - The owner chooses IG-first instead of YouTube-first.
  - A downstream review rejects this spec's behavioral boundary or accepted residuals.
```

## Status

Spec status: `SPEC_COMPLETE_READY_FOR_SCOPING`.

This spec covers the fused-safe one-shot slice:

1. Define the complete YouTube behavioral lane.
2. Use Instagram Reels as the behavioral prompt, not the machinery template.

It does not cover, authorize, or imply implementation of:

3. IG back-fix against completed YouTube behavior.
4. Shared contract extraction after both lanes prove the same behavior.

Those later steps depend on the YouTube behavioral lane existing first.

## Required Behavior

The YouTube lane must become behaviorally complete enough that a downstream Orca
consumer can understand one item from discovery through extraction without
knowing which internal route acquired each piece.

For each captured YouTube video or Short, the lane must be able to express:

- candidate identity and selection basis;
- acquisition route and run receipt;
- metadata and engagement observations;
- comment posture and comment sample when available;
- transcript source, posture, cues, and provenance;
- persistence/correlation anchors tying metadata, comments, transcript, and
  extraction together;
- extraction feed status;
- explicit partial, blocked, disabled, empty, failed, or not-attempted states
  instead of fake success.

The lane may keep using YouTube-specific acquisition methods: served watch HTML,
`ytInitialPlayerResponse`, `ytInitialData`, `youtubei/v1/next`, caption-first
`yt-dlp` acquisition, and ASR fallback. Alternative YouTube acquisition routes
may be explored, but the observable behavior contract below must remain stable.

## Non-Goals

- Do not make YouTube capture use IG's browser-rendered Reels machinery.
- Do not make IG use YouTube's served-HTML, caption-first, or `youtubei` route.
- Do not introduce a shared scheduler, producer/consumer framework, or unified
  acquisition engine in this pass.
- Do not back-fix IG in the YouTube completion pass.
- Do not extract shared core code before the YouTube lane is behaviorally
  complete and IG has been back-fixed against the proven behavior.
- Do not add TikTok behavior without a TikTok source analysis.
- Do not claim live-capture scale, production readiness, legal/access approval,
  or capture validation from this spec.

## Interfaces / Contracts

### BehavioralCandidateRow

A YouTube candidate row should carry, when observed:

- `platform`: `youtube`;
- `platform_video_id`, which is the video-level correlation join key across
  YouTube behavioral surfaces;
- `surface_type`: `shorts | long_form | unknown`;
- `canonical_url` or watch URL;
- `channel_id` and author/channel handle when observed;
- title, publish date, duration, and short description when observed;
- view count and source path for the count;
- like count text and comment count text when observed, labeled as text when not
  parsed to a durable integer;
- `comments_posture`: `captured | disabled | empty | blocked | failed | not_attempted`;
- `transcript_availability`: `caption_manual | caption_auto | asr_required | asr_transcribed | no_speech | failed | not_attempted`;
- `ranking_basis`: explicit basis used to select the candidate, including
  `unknown_or_weak` when the lane does not yet have an IG-like ranking signal;
- source route receipt fields: route name, retrieval time, HTTP/wall posture,
  byte count or artifact hash where available, and limitations.

### CaptureRunReceipt

Every run must preserve visible failure and partial success. It must state:

- route used;
- public/access posture;
- cadence or run envelope when relevant;
- item count attempted and item count captured;
- first-wall or access-block marker when relevant;
- per-item status, including partial states;
- artifacts produced and artifacts intentionally not produced;
- non-authoritative fields, estimates, or text-only views.

### CommentSet

The comments behavior must distinguish:

- comments disabled;
- comments empty;
- comment sample captured;
- comment route blocked or failed;
- comments not attempted.

Captured comments should carry author/display identity as observed, text,
published time, like count when present, reply count when present, and source
route. The contract does not require full comment-corpus exhaustiveness.

### TranscriptSource

YouTube transcript output must normalize captions and ASR into one downstream
shape:

- `platform`: `youtube`;
- `platform_video_id`, which is the video-level correlation join key across
  YouTube behavioral surfaces;
- `source_kind`: `caption | asr`;
- `caption_kind`: `manual | auto | null`;
- `language` and `original_language_assumed` when caption-based;
- raw anchor: caption packet id or audio packet id;
- cue list with millisecond timing;
- posture: `caption_ready | transcribed | no_caption_track | invalid_caption | download_failed | no_speech | failed`
  or a narrower compatible enum. `caption_ready` means usable caption cues are
  preserved; `transcribed` means usable ASR cues are available. A later
  implementation may collapse both success states only if `source_kind` remains
  explicit.
- provenance: tool, tool version, model/tooling metadata, source packet id, and
  source file id or sha when available;
- limitations, including non-authoritative flat-text views.

### PersistenceCorrelation

The completed YouTube behavioral lane must define a durable way to correlate:

- metadata/comment capture output;
- caption packet or audio packet;
- transcript derived record;
- product-extraction record set.

The video-level correlation anchor is `platform_video_id`. Persistence may
remain per capture packet: one video can have many caption packets, audio
packets, transcript records, and extraction record sets across reruns and source
kinds. Correlation must represent that one-video-to-many-packets shape instead
of forcing one packet per video.

The packet-anchored links already exist for caption/audio packet -> transcript
record -> extraction record set. The missing bridge is metadata/comment output
to the packet-anchored transcript/lake surfaces. The implementation may choose a
bridge record, an index, or a packet/lake normalization path, but it must not
leave these surfaces discoverable only by human convention.

When a downstream consumer needs one transcript selection for a video, the
default canonical transcript order is manual caption, then auto caption, then
usable ASR. Preserve all observed transcript sources and record the selection
reason. When multiple successful captures of the same source kind exist for the
same `platform_video_id`, select the latest successful capture by capture time
unless an implementation spec binds a stronger quality rule.

### ExtractionFeed

The extraction feed may continue to use the existing shared transcript product
extractor, but it must consume the normalized `TranscriptSource` behavior rather
than relying on platform-specific guesses.

## IG As Prompt, Not Template

Borrow these IG behavioral wins into YouTube:

- explicit candidate ranking basis, including weak/unknown bases;
- one item has an inspectable path through candidate -> comments -> transcript
  -> persistence -> extraction;
- partial success is preserved, e.g. comments can be captured even when
  transcript fails;
- transient, non-authoritative, and estimated artifacts are labeled rather than
  promoted;
- completion is durable and checkable, not inferred from a stdout summary.

Do not borrow these IG mechanics into YouTube:

- browser-rendered Reels grid acquisition;
- transient IG media-handle extraction;
- ASR-only transcript priority;
- shortcode-anchored persistence as the default YouTube anchor;
- IG runner shape or DOM parser assumptions.

IG source disambiguation: `ig_reels_grid.py` is the ranking-signal/parser source
for the IG behavior borrowed here; `ig_reels_grid_capture.py` is the
browser-render/enumeration capture source named by the parent planning note.

## Acceptance Criteria

Implementation scoping may treat this spec as complete only if it can route a
YouTube-only pass that would make the following testable:

1. A YouTube video or Short has one behavioral record keyed by
   `platform_video_id`, tying candidate identity, metadata, comments posture,
   transcript source selection, one-or-more persistence anchors, and extraction
   status together.
2. Caption and ASR transcript paths both normalize into the same
   `TranscriptSource` contract, while preserving caption-vs-ASR provenance.
3. YouTube comments report one of the explicit comment postures and do not imply
   full corpus capture unless the route actually captured it.
4. Selection and ranking basis is explicit, including `unknown_or_weak` when the
   current YouTube lane lacks IG-grade funnel signals.
5. Metadata/comment legacy packets are either bridged into the correlation
   contract or explicitly kept as a named residual with a deterministic
   programmatic lookup path keyed by `platform_video_id`; manual convention is
   not an acceptable lookup path.
6. Existing no-LLM capture/scoring boundaries remain intact.
7. Existing transcript product extraction behavior remains compatible for both
   YouTube and IG.
8. Given a `platform_video_id`, correlation resolves deterministically to that
   video's metadata/comment capture, available caption/audio packet anchors,
   transcript sources, extraction record-set anchors, and canonical transcript
   selection reason.
9. No implementation claims shared acquisition machinery, production readiness,
   live-scale validation, or TikTok coverage.

## MGT Accepted Residuals

- YouTube ranking may remain weaker than IG ranking in v0. Acceptable because
  the lane can still expose a visible `ranking_basis`; upgrade when weak ranking
  causes poor candidate selection or hidden operator guesswork.
- YouTube comments may remain a bounded sample, not a full corpus. Acceptable
  because the behavioral contract names sample posture; upgrade when downstream
  decisions need corpus-level audience evidence.
- Metadata/comments may initially bridge rather than fully migrate to
  SourceCapturePacket/DataLakeRoot. Acceptable because a durable correlation
  bridge is lower lock-in than a premature migration; upgrade when the bridge
  becomes the main source of lookup errors.
- No shared scheduler/framework. Acceptable because behavioral parity can be
  proven without it; upgrade only if duplicate runner control flow causes
  inconsistent receipts, status, or persistence.
- IG back-fix and TikTok are deferred. Acceptable because completing one lane
  first reduces ambiguity; upgrade only after YouTube's behavior is reviewed and
  stable enough to backport.

## Review Checkpoint

Adversarial artifact review should happen after this spec is authored and before
any YouTube implementation uses it as authority.

Highest value checkpoint: `after_artifact_pre_implementation`.

Review target: this spec plus the PR #417 planning note and the named IG/YT
source files.

Reason: the risky decision is the behavioral contract itself. Reviewing after
runtime edits would be too late; a bad contract would already have shaped code,
persistence, and tests.

## Downstream Handoff

Implementation scoping may rely on the following without reopening intent:

- a fused pass may scope or author implementation-facing docs for YouTube
  behavioral completion only;
- source-changing implementation remains separately authorized;
- use IG as a behavioral comparison prompt, not a machinery template;
- defer IG back-fix and shared contract extraction until after YouTube behavior
  is complete and reviewed;
- keep the acquisition route exploratory and source-specific;
- preserve false-success visibility over cosmetic parity.