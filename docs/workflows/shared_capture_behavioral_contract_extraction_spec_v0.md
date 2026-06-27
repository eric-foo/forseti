# Shared Capture Behavioral Contract Extraction Spec v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow spec
scope: >
  Planning-only step-4 spec for extracting the stable IG/YouTube behavioral
  contracts into a thin shared capture core after the YouTube-first contract and
  IG back-fix contract are reviewed.
use_when:
  - Scoping shared capture-core contract extraction without implementing a framework.
  - Checking which behavior belongs in the thin core versus platform adapters.
  - Preventing shared acquisition machinery from being smuggled into contract extraction.
authority_boundary: retrieval_only
branch_or_commit: codex/unify-capture-core-planning @ b6d87c23 before this artifact was authored; source basis origin/main @ ba9b36b5 with no orca-harness diff on this branch
open_next:
  - docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md
  - docs/workflows/youtube_first_behavioral_completion_spec_v0.md
  - docs/workflows/ig_backfix_against_youtube_behavioral_contract_spec_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/youtube_first_behavioral_completion_spec_review_adjudication_v0.md
  - orca-harness/source_capture/writer.py
  - orca-harness/cleaning/transcript_product_extractor.py
  - orca-harness/cleaning/transcript_product_lake.py
  - orca-harness/runners/run_transcript_product_extract.py
  - orca-harness/runners/run_ig_reels_product_extract.py
stale_if:
  - The YouTube behavioral spec or IG back-fix spec changes materially.
  - Any named shared writer, transcript extraction, or product lake source changes.
  - The owner selects a framework-core or minimal-extraction-only route instead of thin behavioral core extraction.
  - TikTok source analysis lands and changes the shared platform contract boundary.
```

## Status

Target: `SHARED_BEHAVIORAL_CONTRACT_EXTRACTION_SPEC_READY`.

This is a contract-extraction planning artifact, not implementation authority.
It names the smallest shared core that should survive the IG/YouTube lane loop.
It does not authorize source edits, runtime capture, persistence migration,
shared scheduler work, adapter base classes, production readiness, or TikTok
coverage.

## Extraction Rule

The shared core is a set of observable behavior contracts. It is not a shared
acquisition method.

Extract only fields and invariants that both IG and YouTube can honestly express
without hiding source-specific truth. Keep fetch/render, candidate enumeration,
comment acquisition, transcript priority, media handling, and runner control in
platform-owned adapters.

Do not add a shared framework because the names line up. A shared base class,
scheduler, producer/consumer framework, or acquisition ladder is a later
architecture fork and requires fresh owner authorization.

## Thin Core Contracts

### PlatformBehavioralItem

The shared item contract is the comparable behavioral row. It should carry:

- `platform`: e.g. `youtube` or `instagram`;
- `platform_item_id`: YouTube video id or IG shortcode;
- `platform_item_id_kind`: `youtube_video_id | instagram_shortcode | other`;
- canonical URL or locator when observed;
- source family/surface and route receipt anchor;
- author/channel/creator identity when observed;
- surface type when observed, e.g. `shorts`, `long_form`, `reel`, or `unknown`;
- candidate ranking basis, including `unknown_or_weak` when ranking evidence is
  weak or absent;
- observed metadata and engagement signals, with source paths and limitations;
- comments posture;
- transcript availability and canonical transcript selection reason;
- persistence anchors, canonical extraction status, per-source extraction
  statuses, and per-item extraction rollup;
- non-authoritative, estimated, partial, or weak fields labeled explicitly.

The core must not require one physical storage unit per item. One item can map to
many packet ids, record-set ids, bridge records, or legacy packet paths.

### CaptureRunReceipt

The shared receipt contract should state:

- route used and platform adapter name;
- item count attempted, captured, skipped, failed, and partial;
- public/access posture, wall/block/render posture, and route-specific limits;
- capture timestamp or absence reason;
- artifacts produced and artifacts intentionally not produced;
- byte counts, hashes, packet ids, or record ids where available;
- warnings, limitations, non-claims, and non-authoritative views;
- whether downstream extraction was not attempted, skipped done, extracted,
  failed, or partial-needs-cleanup.

This is receipt shape only. It is not a scheduler, daemon framework, or cadence
runner.

### CommentSet

The shared comment contract should carry:

- `platform` and `platform_item_id`;
- `comments_posture`: `captured | disabled | empty | blocked | render_unavailable | parse_failed | failed | not_attempted`, or a narrower compatible enum;
- source route and capture timestamp;
- bounded comment sample with observed author/display identity, text, published
  time, like/reply signals when present, and source ids when present;
- corpus coverage limitation: full-corpus capture is not implied unless the
  route proves it.

Platform adapters own how comments are acquired: IG rendered DOM / embedded
GraphQL nodes, YouTube `youtubei` continuations, or future platform-specific
routes.

### TranscriptSourceRecord

The shared transcript-source record contract should carry the fields below. This rich behavior-
layer record is distinct from the existing
`schemas.product_mention_models.TranscriptSource` enum, which is only the
current product-mention field type for `asr | caption`; future implementation
must not shadow or overload that enum without an explicit migration decision.

- `platform`;
- `platform_item_id` and `platform_item_id_kind`;
- `source_kind`: `caption | asr`;
- `source_route`: platform-specific route such as `youtube_caption`,
  `youtube_audio_asr`, `ig_deep_capture_render_audio`, or `ig_audio_packet_asr`;
- `caption_kind`: `manual | auto | null`;
- language/original-language fields when caption-based;
- raw or derived anchor: packet id, record-set id, legacy path bridge, or other
  deterministic anchor;
- cue list with millisecond timing;
- posture: `caption_ready | transcribed | no_caption_track | invalid_caption | download_failed | no_speech | failed | render_unavailable | no_audio_handle`, or a narrower compatible enum;
- provenance: tool, tool version, model/tooling metadata, source packet/record id,
  source file id/sha where available, retrieval time, and limitations;
- transient media policy when relevant.

Canonical transcript selection is platform-owned but must be reported through the
shared contract:

- YouTube default: manual caption, then auto caption, then usable ASR.
- IG default for scoping: same-render deep-capture ASR when the comment set comes
  from that render, otherwise latest successful standalone audio-packet ASR.
- All observed transcript sources must remain discoverable with selection reason.

### PersistenceCorrelation

The shared correlation contract should carry:

- `platform` and `platform_item_id`;
- candidate metadata anchors;
- comment anchors;
- transcript source anchors;
- extraction record-set anchors;
- canonical transcript selection reason;
- route receipts and limitations;
- deterministic lookup method, e.g. bridge record, index, adapter query, or
  normalized packet/lake path.

The contract must support one item to many anchors. It must not require one
packet per item, one transcript per item, or one extraction per item. It must not
let a manual folder convention pass as correlation.

### ExtractionFeed

The existing extractor already exposes the minimal shared feed:

- `video_id` is the current field name, but the shared contract should treat it
  as `platform_item_id` at the behavior layer;
- `transcript_anchor` is the packet or record anchor used for derived output;
- `transcript_source` is currently `caption | asr`;
- `cues` are millisecond-timed transcript spans.

The thin core may specify this feed and test adapters against it. It must not
move LLM/model calls into capture. Product extraction remains downstream of
source capture and transcript normalization.

Extraction completion is per transcript anchor. The shared item must expose
`source_extraction_statuses` keyed by transcript anchor and a per-item rollup.
The rollup may read `complete` only when every extraction-eligible observed
transcript source for that item is `extracted` or `skipped_done`, or is
explicitly residualized or marked `not_extraction_eligible` with reason.
Canonical-only completion must be named `canonical_extraction_status`, not the
whole-item `extraction_status`.

### SourceArtifactPersistence

The shared persistence preference is SourceCapturePacket raw artifacts plus
DataLakeRoot derived record sets with completion markers where durable completion
needs to be machine-checkable.

This is a preference, not a forced migration. A bridge or index is acceptable
when it gives deterministic lookup and lower lock-in than rewriting a working
platform lane. Any residual legacy path must be named with a programmatic lookup
route and an upgrade trigger.

## Adapter-Owned Responsibilities

IG adapter owns:

- creator grid enumeration;
- DOM/passive JSON merge;
- ranking basis and hidden-engagement limitations;
- rendered reel deep capture;
- transient media-handle extraction, download, and redaction;
- ASR-only transcript route;
- IG-specific comment parsing and persistence mapping.

YouTube adapter owns:

- per-video and channel/Shorts enumeration;
- served watch HTML parsing;
- `youtubei` comment route;
- caption discovery/download and ASR fallback;
- YouTube-specific transcript selection;
- legacy metadata/comment packet bridging and persistence mapping.

TikTok adapter is intentionally undefined until TikTok source analysis exists.
No TikTok field, route, or access posture may be inferred from IG or YouTube.

## Extraction Sequence

A future source-changing extraction pass should not begin until the owner accepts
or revises this spec after review. If authorized, sequence narrowly:

1. Define testable contract fixtures for `PlatformBehavioralItem`,
   `TranscriptSourceRecord`, `CommentSet`, `PersistenceCorrelation`, and
   `ExtractionFeed` using existing IG/YT fixture patterns.
2. Add platform adapters that project existing lane outputs into the contracts;
   do not move acquisition code.
3. Add deterministic correlation bridge/index only where current persistence is
   not programmatically linked.
4. Keep extraction downstream; use the existing product extraction tests as
   compatibility checks, not as capture-core validation.
5. Reconsider runner/framework consolidation only if duplicate runner mechanics
   cause observable behavior divergence after the contract layer exists.

## Acceptance Criteria

Contract extraction is ready for implementation scoping only if the following
are testable:

1. Both IG and YouTube can produce or project a behavioral item keyed by
   `platform_item_id` without changing their acquisition methods.
2. Comment posture, transcript posture, receipt status, canonical extraction
   status, per-source extraction statuses, and per-item extraction rollup are
   comparable but retain platform-specific route details.
3. Correlation resolves programmatically from item id to candidate, comments,
   transcript sources, source-level extraction statuses, extraction anchors, and
   selection reason.
4. One-item-to-many-anchors is first-class; no contract path assumes one packet or
   one transcript per item.
5. `TranscriptSourceRecord` preserves caption-vs-ASR, route, posture, provenance,
   timing cues, and transient-media limits.
6. Extraction feed remains source-family agnostic and does not import capture or
   model calls into the wrong layer.
7. Legacy or uneven persistence paths are either bridged deterministically or
   explicitly kept as named residuals with lookup paths and upgrade triggers.
8. No implementation claims shared acquisition machinery, shared scheduler,
   production readiness, live-scale validation, owner approval, or TikTok coverage.

## MGT Accepted Residuals

- The first shared core may be a contract plus adapter projection, not a shared
  code package. Acceptable because it avoids locking in a framework before the
  lane loop proves one is needed; upgrade only if projection cannot express both
  lanes without duplicate correlation defects or observable behavior divergence.
- Physical persistence can stay uneven in v0. Acceptable only when deterministic
  correlation prevents human-convention lookup.
- `video_id` may remain the extractor's runtime field name while the behavior
  contract uses `platform_item_id`. Acceptable until source-changing work is
  authorized; upgrade if the name causes platform-mixing bugs.
- TikTok remains excluded. Acceptable because no TikTok source-family analysis is
  present in this pass.
- The patched YouTube behavioral spec has not been adversarially re-reviewed
  after its adjudication patch. Acceptable for planning only; before source-
  changing shared contract extraction uses it as implementation authority,
  either run a post-patch YouTube re-review or record explicit owner acceptance
  of that dependency.

## Review Checkpoint

Adversarial artifact review should happen after this spec and the IG back-fix
spec are authored and before any shared contract extraction implementation uses
them as authority.

Highest value checkpoint: `after_artifact_pre_implementation`.

Review target: this spec, the IG back-fix spec, the parent planning note, the
reviewed/adjudicated YouTube behavioral spec, and the named IG/YT/shared source
files.