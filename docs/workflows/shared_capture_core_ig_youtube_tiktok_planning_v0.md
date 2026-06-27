# Shared Capture Core IG / YouTube / TikTok Planning v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow plan
scope: >
  Source-backed planning note for a shared capture core across Instagram Reels,
  YouTube videos/Shorts, and later TikTok. It maps current IG and YouTube
  capture/transcript/save/extraction paths, compares the core architecture
  options, and sequences the IG<->YouTube sync after owner selection. It keeps
  acquisition method, transcript priority, and runner shape open for lane-first
  exploration rather than forcing a common internal capture mechanism.
use_when:
  - Deciding whether to accept a thin shared capture core, defer to minimal shared extraction, or build a heavier capture framework.
  - Planning IG<->YouTube capture-core synchronization without moving code.
  - Checking which current capture/transcript/save responsibilities are already shared versus platform-owned.
  - Choosing a lane-first exploration route where one platform becomes the behavioral reference before backporting contract wins.
authority_boundary: retrieval_only
branch_or_commit: origin/main @ ba9b36b5; handoff orientation read from origin/claude/handoff-unify-capture-core @ d4437209
open_next:
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - orca-harness/source_capture/ig_reels_grid_capture.py
  - orca-harness/source_capture/ig_reels_deep_capture.py
  - orca-harness/source_capture/ig_reels_deep_capture_lake.py
  - orca-harness/source_capture/transcript/ig_reels_audio_packet.py
  - orca-harness/youtube_capture/capture_youtube_v0.py
  - orca-harness/youtube_capture/shorts_scroll_capture_v0.py
  - orca-harness/source_capture/transcript/youtube_captions.py
  - orca-harness/source_capture/transcript/caption_packet.py
  - orca-harness/source_capture/transcript/asr_packet.py
  - orca-harness/source_capture/writer.py
  - orca-harness/cleaning/transcript_product_extractor.py
stale_if:
  - origin/main changes any named IG or YouTube capture, transcript, persistence, or extraction source.
  - The owner selects, rejects, or revises the thin-core / framework-core / minimal-core fork.
  - TikTok capture code or a TikTok source-family contract lands.
  - The IG/TikTok access-mode decision is reconciled against the anonymous/no-stored-auth constraint used by this planning note.
```

## Status

Architecture result: `TARGET_RECOMMENDED`.

Recommended target: `AO-A_THIN_SHARED_CORE`, accepted only after owner review.
This note does not authorize implementation, refactor, runner movement, new
network behavior, source capture, or schema migration.

Hard pushback: defaulting now to a framework-style capture orchestrator is the
wrong move. The current source evidence shows shared pieces, but not a single
capture substrate. YouTube's served-HTML plus `youtubei` path and caption-first
transcript path are not the same shape as IG's browser-rendered Reels grid,
transient media-handle, and ASR-first path. A heavy framework would lock in fake
uniformity before the owner chooses that fork.

Clarification: the thin core is not a decision to freeze each platform exactly
as-is. It should make the lanes behaviorally comparable while leaving room to
explore better acquisition methods, transcript priority rules, persistence
anchors, and runner shapes per platform. The convergence target is shared
observable behavior, not shared internal machinery.

## Confirm-Don't-Trust Receipt

The handoff packet was read from:

- `origin/claude/handoff-unify-capture-core:docs/prompts/handoffs/unify_capture_core_ig_yt_tiktok_planning_handoff_v0.md`
- observed ref: `d4437209`

The working branch was created fresh from `origin/main`:

- branch: `codex/unify-capture-core-planning`
- base: `ba9b36b5`

All claims below are based on fresh reads of the named IG, YouTube, shared
writer/adapter/transcript, extraction, and focused test files at `origin/main @
ba9b36b5`. The YouTube lane is treated here as freshly verified by this pass,
not as inherited from the sender.

Tests rechecked for this planning pass:

- `python -m pytest -p no:cacheprovider tests/contract/test_no_llm_imports.py -q`
  -> passed.
- `python -m pytest -p no:cacheprovider tests/unit/test_ig_reels_product_extract.py tests/unit/test_youtube_caption_product_extract.py -q`
  -> passed after rerunning with sandbox escalation because the normal sandbox
  blocked the worktree-local `_scratch` directory.

These tests support the no-LLM import boundary and the current shared extraction
contract. They do not validate the proposed architecture.

## Current Pipeline Map

### Instagram Reels

Enumeration:

- `ig_reels_grid_capture.py` renders a creator `/reels/` grid through the
  browser observation path and extracts DOM rows plus passive JSON candidates.
- `run_source_capture_ig_reels_creator_deep_capture.py` ranks candidate reels by
  engagement and view fallback, then selects bounded top-N reels for deep
  capture.

Render / scrape:

- `ig_reels_deep_capture.py` uses a rendered DOM pass for the selected reel.
- The same rendered DOM is used to parse comments and locate transient IG media
  URLs. Those media URLs are handles for immediate use, not durable data.

Transcript:

- The deep-capture path downloads the transient audio/media handle immediately
  and transcribes with the ASR function injected by the runner.
- `source_capture/transcript/ig_reels_audio_packet.py` also provides a standalone
  IG Reels audio SourceCapturePacket path using `yt-dlp` and ASR.

Comments:

- `ig_reels_comments.py` parses audience comments from embedded GraphQL comment
  nodes in the rendered DOM and dedupes by comment id.

Persistence:

- `ig_reels_deep_capture_lake.py` writes a per-reel derived record set anchored
  by shortcode, including audience comments, transcript posture/cues, and a
  completion lane.
- That deep-capture record redacts transient media URLs and keeps only
  provenance such as host and whether a media handle was used.
- The standalone IG audio path writes a raw `SourceCapturePacket` for
  `source_family=instagram_creator`, `source_surface=ig_reels_audio`, then
  appends a `transcript_asr` derived record. Unlike YouTube ASR, this path does
  not write the transcript as a completed record set.

Extraction:

- `run_ig_reels_product_extract.py` discovers IG audio packets and feeds
  transcript cues into the shared transcript product extractor and product
  mention lake path.
- Grid metadata packets in the same source family are explicitly skipped by the
  focused IG extraction tests.

### YouTube

Enumeration:

- `shorts_scroll_capture_v0.py` enumerates Shorts from a channel
  `/@handle/shorts` surface, shuffles the bounded pool, and captures within a
  cadence loop.
- `capture_youtube_v0.py` operates per video id for public metadata and comment
  capture.

Render / scrape:

- The default path is not a browser render. `stealth_client.py` performs
  anonymous public HTTP using `curl_cffi` Chrome impersonation when available,
  with no login, no proxy, and no stored auth.
- `capture_youtube_v0.py` reads served watch HTML, extracts
  `ytInitialPlayerResponse` metadata and `ytInitialData` tokens, then fetches
  comment samples through `youtubei/v1/next`.
- `shorts_scroll_capture_v0.py` uses the same served-HTML and `youtubei` comment
  pattern for Shorts volume capture.

Transcript:

- `youtube_captions.py` is caption-first. It uses `yt-dlp` metadata and subtitle
  download routes to find manual captions first, auto captions second, preferring
  original language and only falling back to English when language is unknown.
- `caption_packet.py` writes caption artifacts as a raw
  `SourceCapturePacket` with `source_family=youtube` and
  `source_surface=youtube_captions`. No-caption is a typed ASR-required state.
- `asr_packet.py` writes a YouTube audio SourceCapturePacket and a completed
  `transcript_asr` record set after ASR.

Comments:

- YouTube comments are collected through `youtubei/v1/next` continuation calls
  in the metadata/comment capture lane. They are not yet normalized into the
  same SourceCapturePacket/DataLake shape as the transcript packet lane.

Persistence:

- The older YouTube metadata/comment lane writes lean packet folders under
  `orca-harness/youtube_capture/packets/` and Shorts run JSON under
  `orca-harness/youtube_capture/shorts_scroll_runs/`; both are gitignored local
  capture output paths.
- The caption and ASR transcript lanes use the shared SourceCapturePacket writer
  and DataLakeRoot raw/derived rails.

Extraction:

- `run_transcript_product_extract.py` discovers `source_family=youtube` caption
  and audio packets, converts json3/ASR cues into `TranscriptInput`, and writes
  product mentions through the same extractor and product lake path used by IG.

## Shared Versus Platform-Owned

Already shared or directly reusable:

- SourceCapturePacket writer and DataLakeRoot raw/derived persistence rails in
  `source_capture/writer.py`.
- Transcript cue input shape used by `cleaning/transcript_product_extractor.py`.
- ASR download/transcription machinery for audio-backed transcript packets.
- Product mention extraction, quote anchoring, timestamp derivation, and lake
  record-set writing.
- Cadence-plan calculation in `source_capture/cadence.py`.
- Browser, CloakBrowser, direct HTTP, anti-blocking HTTP, proxy profile, and
  auth-state primitives as platform-selectable adapters.
- Receipt discipline: access posture, archive/media posture, byte caps, wall or
  access-block classification, and provenance metadata.
- The no-LLM boundary for capture/scoring imports.

Platform-owned and should remain outside the first shared core:

- Enumeration: IG grid DOM/passive JSON/ranking versus YouTube channel Shorts
  and per-video ids.
- Fetch substrate: IG browser-rendered pages versus YouTube anonymous served
  HTML plus `youtubei`.
- Transcript priority: IG ASR-first versus YouTube caption-first with ASR
  fallback.
- Comments: IG embedded GraphQL comment nodes from a rendered DOM versus
  YouTube `youtubei` continuation pages.
- Media handling: IG transient signed media handles must be consumed immediately
  and redacted; YouTube caption artifacts and audio packets have different
  provenance and storage posture.
- Current persistence maturity: IG has both shortcode-anchored deep-capture
  record sets and audio SourceCapturePackets; YouTube has legacy local
  metadata/comment packets plus SourceCapturePacket transcript lanes.

TikTok is not inferred. The only safe slot today is "future platform adapter
with its own enumeration, fetch/render, transcript, comments, persistence
mapping, and extraction feed." Any TikTok-specific claim requires a TikTok
source read that does not exist in this pass.

## Architecture Options

### AO-A: Thin Shared Core

Shape:

- Shared policy/receipt envelope for capture runs.
- Shared cadence plan.
- Shared packet/lake persistence contract.
- Shared transcript-source record contract.
- Shared extraction feed into the existing transcript product extractor.
- Fat IG, YouTube, and later TikTok adapters own enumeration, fetch/render,
  comments, platform transcript acquisition, and surface-specific persistence
  mapping.

Why this fits the evidence:

- It preserves existing working platform mechanics instead of pretending they
  are one route.
- It creates a real common contract where one already exists: transcript cues,
  packet/lake rails, ASR outputs, cadence, receipts, and extraction.
- It keeps the high-lock-in scheduler/orchestrator decision out of v0.
- It lets IG<->YouTube sync focus on data contracts and correlation before
  moving any code.

Accepted residuals:

- Some runner duplication remains.
- Metadata/comment persistence remains uneven until the owner accepts a
  persistence normalization pass.
- IG ASR and YouTube ASR completion semantics remain mismatched until the sync
  sequence resolves them.
- Acquisition method, transcript priority, and runner shape remain exploratory;
  they are standardized only after a lane proves that standardization improves
  behavior without hiding source-specific truth.

### AO-B: Framework Core

Shape:

- Shared producer/consumer orchestrator for enumeration, capture tasks,
  transcript tasks, comment tasks, persistence, retries, and pacing.
- Platform plugins provide route details.

Why this is not the recommended default:

- It is high lock-in and would centralize behavior before the actual common
  contract is proven.
- It would obscure critical source-specific risk posture, especially IG
  transient media handles and YouTube caption-first behavior.
- It would likely force legacy YouTube metadata/comment packets and IG
  shortcode-anchored deep-capture records through a common abstraction before
  the owner has decided the migration target.

Use only if the owner explicitly chooses the framework fork after accepting the
lock-in and migration cost.

### AO-C: Minimal Shared Extraction

Shape:

- Treat the current shared extractor/lake and a small transcript-source adapter
  as enough.
- Defer capture-core synchronization.

Why this underfixes the objective:

- It recognizes the strongest existing commonality, but it does not plan the
  requested capture-core boundary.
- It leaves transcript-source posture, persistence correlation, cadence/receipt
  shape, and IG<->YouTube sync unresolved.

## Recommended Target Boundary

Adopt `AO-A_THIN_SHARED_CORE` as the recommended owner decision.

Core responsibilities:

- `CapturePolicy`: platform, public/access posture, no-LLM capture rule, no
  stored secrets by default, no transient signed media URL persistence, cadence
  envelope, byte/volume caps, and wall/block classification.
- `CaptureRunReceipt`: observed route, status, posture, artifact counts, byte
  caps, limitations, and any wall/access-block state. It must preserve
  GO/PARTIAL/NO-GO visibility rather than manufacturing success.
- `CaptureCadencePlan`: use existing fixed/jitter cadence planning; do not
  smuggle in a scheduler.
- `SourceArtifactPersistence`: prefer SourceCapturePacket-shaped raw artifacts
  and DataLakeRoot derived record sets with completion markers where the lane
  needs durable completion semantics.
- `TranscriptSourceRecord`: normalized transcript-source record with platform id, source
  family/surface, caption-or-ASR source, packet/raw anchor, cue list,
  transcript posture, tool/model provenance, and limitations.
- `ExtractionFeed`: feed `TranscriptInput` into the existing product extractor;
  do not move LLM/model calls into capture.

Satellite responsibilities:

- IG adapter: creator grid enumeration, DOM/passive JSON merge, engagement/view
  ranking, browser render, comment parsing, transient media handle extraction,
  media download, ASR posture, and IG persistence mapping.
- YouTube adapter: channel/video enumeration, served HTML parsing,
  `youtubei` comments, caption discovery/download, ASR fallback, legacy packet
  bridging, and YouTube persistence mapping.
- TikTok adapter: not specified until TikTok source analysis exists.

## Lane-First Exploration Strategy

Default exploration route: make YouTube the first complete behavioral lane, then
use that completed YouTube lane to back-fix IG.

This does not mean making YouTube capture like IG. It means borrowing the useful
IG behavioral wins into YouTube first: a complete lifecycle receipt, explicit
comment/transcript/persistence correlation, durable completion semantics, and
clear limits on transient or non-authoritative artifacts. YouTube should still
use served HTML, `youtubei`, captions-first transcript capture, and ASR fallback
where those remain the honest source-specific routes.

Once YouTube has the complete behavioral contract, use it as the reference for
IG. The IG back-fix should normalize only the proven contract surface:
transcript-source fields, completion semantics, run receipt, persistence
correlation, and extraction feed. It should not force IG to adopt YouTube's HTTP
path, caption priority, packet anchors, or runner structure.

This lane-first loop is the SCI-compatible way to reach the MGT target: push one
lane past the cheap parity point until it is behaviorally complete, name the
accepted residuals, then backport only the contract wins. Do not average the
lanes into a vague abstraction, and do not build a framework before the lane
loop proves that a framework is needed.

## IG<->YouTube Sync Sequence

This sequence is planning-only. It starts only after the owner accepts or revises
the recommended thin-core target.

1. Owner fork decision: accept `AO-A_THIN_SHARED_CORE`, choose the heavier
   framework route, or intentionally stop at minimal shared extraction.
2. Accept or revise the YT-first lane exploration route. If the owner chooses
   IG-first instead, keep the same loop but reverse the lane order.
3. YouTube completion pass: use IG's stronger behavioral surfaces as prompts,
   not templates. Bring YouTube metadata/comments, captions/ASR, persistence,
   receipts, and extraction feed into one complete behavioral lane without
   changing YouTube's honest acquisition route.
4. IG back-fix pass: use completed YouTube behavior to normalize IG
   transcript-source fields, completion semantics, run receipts, and persistence
   correlation. Do not force YouTube's caption-first priority or HTTP shape onto
   IG. Step-3 planning spec:
   `docs/workflows/ig_backfix_against_youtube_behavioral_contract_spec_v0.md`.
5. Shared contract extraction: after both lanes express the same behavior,
   extract the stable transcript-source record, receipt, persistence-completion,
   and extraction-feed contracts into the thin core. Step-4 planning spec:
   `docs/workflows/shared_capture_behavioral_contract_extraction_spec_v0.md`.
6. Contract-test plan: after implementation is authorized, add tests around the
   shared transcript-source record and persistence-completion contract, plus existing
   no-LLM and product-extraction tests. Do not use current passing extraction
   tests as proof that the capture core is validated.
7. Framework reconsideration gate: consider runner or scheduler consolidation
   only if the lane loop proves that duplicated mechanics are causing behavioral
   inconsistency or unacceptable maintenance cost.
8. TikTok recon gate: only after the IG<->YouTube contract is stable, run a
   TikTok-specific recon to decide whether TikTok joins through the same thin
   adapter contract or needs a different branch.

## Open Residuals

- Access-mode conflict: this pass follows the user/handoff constraint of
  anonymous/no-stored-auth public capture. The IG findings source mentions a
  later own-account decision for IG/TikTok. That is a real conflict and must be
  resolved by the owner before encoding a shared access policy.
- YouTube metadata/comment capture is not yet SourceCapturePacket/DataLakeRoot
  shaped.
- IG deep-capture transcript/comment persistence is shortcode-anchored and not
  the same as IG standalone audio packet persistence.
- IG ASR and YouTube ASR derived transcript completion semantics differ.
- TikTok has no source-backed adapter shape in this pass.
- No live capture, scale, production readiness, or legal/access approval is
  claimed here.
